"""
Rubric for BibTeX Reference Generation
Task: Generate a complete BibTeX reference file ref.bib for 65 papers listed in paper_title.md

Total: 100 points

Scoring Dimensions:
I. File Delivery (10 points)
  1. ref.bib file exists with correct filename (5 points)
  2. File is non-empty and parseable as valid BibTeX (5 points)

II. Entry Coverage (35 points)
  Via fuzzy title matching, calculate how many of the 65 papers the agent output covers

III. Entry Quality — Field Completeness and Accuracy (35 points)
  For matched entries, check key fields like author / year / venue / entry type
  and compare accuracy against eval/ref.bib reference answers

IV. BibTeX Format Compliance (20 points)
  - Deterministic checks (10 points): duplicate keys, duplicate titles, brace matching, entry count
  - LLM-as-Judge (10 points): format compliance, information completeness, usability
"""

import os
import re
import json
import sys
from typing import Tuple, Dict, Any, List, Optional

try:
    import openai
except ImportError:
    openai = None

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REF_BIB_PATH = os.path.join(SCRIPT_DIR, "ref.bib")
TOTAL_EXPECTED_PAPERS = 65


# =============================================================================
# BibTeX Parsing
# =============================================================================

def _normalize_text(s: str) -> str:
    """Remove LaTeX commands, braces, quotes, punctuation; lowercase."""
    if not s:
        return ""
    # Strip LaTeX commands like \textit{...}
    s = re.sub(r"\\[a-zA-Z]+\{([^}]*)\}", r"\1", s)
    s = s.replace("{", "").replace("}", "").replace('"', "")
    s = re.sub(r"[^a-zA-Z0-9\s]", "", s)
    return re.sub(r"\s+", " ", s).strip().lower()


def _extract_brace_value(text: str, start: int) -> Optional[str]:
    """Extract a brace-delimited value starting at '{', handling nesting."""
    if start >= len(text) or text[start] != "{":
        return None
    depth = 0
    i = start
    while i < len(text):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[start + 1 : i]
        i += 1
    return text[start + 1 :]


def _parse_bibtex(content: str) -> List[Dict[str, str]]:
    """Parse BibTeX content into a list of entry dicts."""
    entries: List[Dict[str, str]] = []
    raw_entries = re.split(r"(?m)^@", content)

    for raw in raw_entries:
        raw = raw.strip()
        if not raw:
            continue
        header = re.match(r"([a-zA-Z]+)\s*\{\s*([^,]*),", raw)
        if not header:
            continue
        entry: Dict[str, str] = {
            "type": header.group(1).lower(),
            "key": header.group(2).strip(),
        }
        fields = [
            "title",
            "author",
            "year",
            "journal",
            "booktitle",
            "doi",
            "volume",
            "number",
            "pages",
            "publisher",
            "isbn",
            "issn",
            "series",
        ]
        for field in fields:
            pat = re.compile(
                rf"(?<![a-zA-Z]){field}\s*=\s*\{{", re.IGNORECASE
            )
            m = pat.search(raw)
            if m:
                val = _extract_brace_value(raw, m.end() - 1)
                if val is not None:
                    entry[field] = re.sub(r"\s+", " ", val).strip()
                    continue
            pat2 = re.compile(
                rf'(?<![a-zA-Z]){field}\s*=\s*"([^"]*)"',
                re.IGNORECASE | re.DOTALL,
            )
            m2 = pat2.search(raw)
            if m2:
                entry[field] = re.sub(r"\s+", " ", m2.group(1)).strip()
                continue
            if field == "year":
                m3 = re.search(r"year\s*=\s*(\d{4})", raw, re.IGNORECASE)
                if m3:
                    entry["year"] = m3.group(1)
        entries.append(entry)
    return entries


def _jaccard(s1: str, s2: str) -> float:
    """Word-level Jaccard similarity."""
    w1 = set(s1.split())
    w2 = set(s2.split())
    if not w1 or not w2:
        return 0.0
    return len(w1 & w2) / len(w1 | w2)


# =============================================================================
# Environment & LLM
# =============================================================================

def _load_env(answer_dir: str) -> dict:
    values: Dict[str, str] = {}
    for d in [answer_dir, os.path.join(SCRIPT_DIR, "..")]:
        p = os.path.join(d, ".env")
        if os.path.exists(p):
            try:
                with open(p, "r") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#") or "=" not in line:
                            continue
                        k, v = line.split("=", 1)
                        if k.strip() not in values:
                            values[k.strip()] = v.strip().strip("'\"")
            except Exception:
                pass
    return values


def _get_text_eval_config(answer_dir: str) -> dict:
    env = _load_env(answer_dir)

    def g(key: str, default: str = "") -> str:
        return os.environ.get(key) or env.get(key) or default

    return {
        "api_key": g("EVAL_TEXT_API_KEY", g("ANTHROPIC_API_KEY")),
        "api_base": g("EVAL_TEXT_API_BASE_URL", g("ANTHROPIC_BASE_URL")),
        "model": g("EVAL_TEXT_MODEL", "openai/gpt-5.2"),
    }


def _call_llm_judge(prompt: str, config: dict) -> str:
    if not openai or not config.get("api_key"):
        return ""
    try:
        base = config["api_base"].rstrip("/")
        if not base.endswith("/v1"):
            base += "/v1"
        client = openai.OpenAI(api_key=config["api_key"], base_url=base)
        resp = client.chat.completions.create(
            model=config["model"],
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2048,
            temperature=0,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        print(f"[RUBRIC] LLM Judge call failed: {e}")
        return ""


# =============================================================================
# Load Reference Data
# =============================================================================

def _load_ref_entries() -> List[Dict[str, str]]:
    if not os.path.exists(REF_BIB_PATH):
        return []
    with open(REF_BIB_PATH, "r", encoding="utf-8") as f:
        return _parse_bibtex(f.read())


def _load_paper_titles() -> List[str]:
    path = os.path.join(SCRIPT_DIR, "..", "context", "paper_title.md")
    titles: List[str] = []
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                m = re.match(r"\[\d+\]\s*(.*)", line.strip())
                if m and m.group(1).strip():
                    titles.append(m.group(1).strip())
    return titles


# =============================================================================
# Find Agent's bib File
# =============================================================================

def _find_bib(answer_dir: str) -> Optional[str]:
    candidates = ["ref.bib", "references.bib", "bibliography.bib", "output.bib"]
    for name in candidates:
        p = os.path.join(answer_dir, name)
        if os.path.isfile(p):
            return p
    if os.path.isdir(answer_dir):
        for f in sorted(os.listdir(answer_dir)):
            if f.lower().endswith(".bib") and not f.startswith("."):
                return os.path.join(answer_dir, f)
    return None


# =============================================================================
# I. File Delivery (10 points)
# =============================================================================

def _eval_file_delivery(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    score = 0
    details: Dict[str, str] = {}

    bib_path = _find_bib(answer_dir)
    exact = os.path.join(answer_dir, "ref.bib")

    # 1a. File exists with correct name (5 points)
    if os.path.isfile(exact):
        score += 5
        details["ref.bib file"] = "5/5 - Filename matches exactly"
    elif bib_path:
        score += 2
        details["ref.bib file"] = (
            f"2/5 - A .bib file exists but is not named ref.bib: {os.path.basename(bib_path)}"
        )
    else:
        details["ref.bib file"] = "0/5 - No .bib file found"

    # 1b. File is non-empty and parseable (5 points)
    if bib_path:
        try:
            with open(bib_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            if not content.strip():
                details["File content"] = "0/5 - File is empty"
            else:
                entries = _parse_bibtex(content)
                if len(entries) >= 1:
                    score += 5
                    details["File content"] = (
                        f"5/5 - Parseable, contains {len(entries)} BibTeX entries"
                    )
                else:
                    score += 1
                    details["File content"] = "1/5 - File is non-empty but no valid entries parsed"
        except Exception as e:
            details["File content"] = f"0/5 - File read failed: {e}"
    else:
        details["File content"] = "0/5 - No file to check"

    return score, {"score": f"{score}/10", "details": details}


# =============================================================================
# II. Entry Coverage (35 points)
# =============================================================================

def _match_titles(
    paper_titles: List[str],
    ai_entries: List[Dict[str, str]],
    ref_entries: List[Dict[str, str]],
) -> Tuple[int, List[tuple], List[str]]:
    """Match paper titles to AI entries. Returns (matched_count, matched_pairs, unmatched)."""
    matched_pairs: List[tuple] = []
    unmatched: List[str] = []
    used_indices: set = set()

    for title in paper_titles:
        norm = _normalize_text(title)
        if not norm:
            continue
        best_sim = 0.0
        best_idx = -1
        for idx, ai_e in enumerate(ai_entries):
            if idx in used_indices:
                continue
            ai_norm = _normalize_text(ai_e.get("title", ""))
            if not ai_norm:
                continue
            sim = 1.0 if norm == ai_norm else _jaccard(norm, ai_norm)
            if sim > best_sim:
                best_sim = sim
                best_idx = idx
        if best_sim >= 0.65 and best_idx >= 0:
            matched_pairs.append((title, ai_entries[best_idx]))
            used_indices.add(best_idx)
        else:
            unmatched.append(title)

    return len(matched_pairs), matched_pairs, unmatched


def _eval_coverage(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    bib_path = _find_bib(answer_dir)
    if not bib_path:
        return 0, {"score": "0/35", "details": {"error": "No .bib file"}, "_pairs": []}

    try:
        with open(bib_path, "r", encoding="utf-8", errors="ignore") as f:
            ai_content = f.read()
    except Exception as e:
        return 0, {"score": "0/35", "details": {"error": f"Read failed: {e}"}, "_pairs": []}

    paper_titles = _load_paper_titles()
    ref_entries = _load_ref_entries()
    ai_entries = _parse_bibtex(ai_content)
    total = len(paper_titles) if paper_titles else TOTAL_EXPECTED_PAPERS

    matched_count, matched_pairs, unmatched = _match_titles(
        paper_titles if paper_titles else [e.get("title", "") for e in ref_entries],
        ai_entries,
        ref_entries,
    )

    ratio = matched_count / total if total > 0 else 0.0
    score = round(ratio * 35)
    score = max(0, min(35, score))

    details: Dict[str, Any] = {
        "Required papers": total,
        "Agent output entries": len(ai_entries),
        "Matched count": matched_count,
        "Coverage": f"{ratio * 100:.1f}%",
    }
    if unmatched:
        sample = [t[:80] for t in unmatched[:8]]
        if len(unmatched) > 8:
            sample.append(f"... {len(unmatched)} total unmatched")
        details["Unmatched samples"] = sample

    return score, {"score": f"{score}/35", "details": details, "_pairs": matched_pairs}


# =============================================================================
# III. Entry Quality (35 points)
# =============================================================================

def _eval_quality(answer_dir: str, matched_pairs: List[tuple]) -> Tuple[int, Dict[str, Any]]:
    if not matched_pairs:
        return 0, {"score": "0/35", "details": {"error": "No matched entries to evaluate"}}

    ref_entries = _load_ref_entries()
    ref_by_title: Dict[str, Dict[str, str]] = {}
    for e in ref_entries:
        nt = _normalize_text(e.get("title", ""))
        if nt:
            ref_by_title[nt] = e

    total_score = 0.0
    n_checked = 0
    stats = {
        "author_correct": 0,
        "year_correct": 0,
        "venue_present": 0,
        "type_valid": 0,
        "extra_fields": 0,
    }

    for title, ai_entry in matched_pairs:
        if not ai_entry:
            continue

        norm_t = _normalize_text(title)

        # Find matching reference entry
        ref_entry = ref_by_title.get(norm_t)
        if not ref_entry:
            best_s = 0.0
            for nt, re_ in ref_by_title.items():
                s = _jaccard(norm_t, nt)
                if s > best_s and s >= 0.65:
                    best_s = s
                    ref_entry = re_

        n_checked += 1
        entry_pts = 0.0  # max 5 per entry

        # (a) author (1.5 pts)
        if "author" in ai_entry and ai_entry["author"].strip():
            if ref_entry and "author" in ref_entry:
                ref_a = _normalize_text(ref_entry["author"])
                ai_a = _normalize_text(ai_entry["author"])
                sim = _jaccard(ref_a, ai_a)
                if sim >= 0.5:
                    entry_pts += 1.5
                    stats["author_correct"] += 1
                elif sim >= 0.3:
                    entry_pts += 0.7
                else:
                    entry_pts += 0.2
            else:
                entry_pts += 1.0
                stats["author_correct"] += 1
        # else 0

        # (b) year (1.0 pt)
        if "year" in ai_entry and ai_entry["year"].strip():
            if ref_entry and "year" in ref_entry:
                if ai_entry["year"].strip() == ref_entry["year"].strip():
                    entry_pts += 1.0
                    stats["year_correct"] += 1
                else:
                    entry_pts += 0.1
            else:
                entry_pts += 0.7
                stats["year_correct"] += 1
        # else 0

        # (c) venue — journal or booktitle (1.0 pt)
        has_venue = bool(
            (ai_entry.get("journal") or "").strip()
            or (ai_entry.get("booktitle") or "").strip()
        )
        if has_venue:
            entry_pts += 1.0
            stats["venue_present"] += 1

        # (d) entry type valid (0.5 pt)
        valid_types = {
            "article", "inproceedings", "book", "inbook", "incollection",
            "phdthesis", "mastersthesis", "techreport", "misc", "online",
            "conference", "proceedings", "unpublished",
        }
        if ai_entry.get("type", "").lower() in valid_types:
            entry_pts += 0.5
            stats["type_valid"] += 1

        # (e) extra useful fields: doi, pages, volume, number, publisher (0.5 pt)
        extra_count = sum(
            1
            for f in ["doi", "pages", "volume", "number", "publisher"]
            if (ai_entry.get(f) or "").strip()
        )
        if extra_count >= 3:
            entry_pts += 0.5
            stats["extra_fields"] += 1
        elif extra_count >= 1:
            entry_pts += 0.2

        total_score += entry_pts  # max 5.0 per entry

    if n_checked == 0:
        return 0, {"score": "0/35", "details": {"error": "No valid entries"}}

    avg = total_score / (n_checked * 5.0)
    score = round(avg * 35)
    score = max(0, min(35, score))

    details: Dict[str, Any] = {
        "Entries evaluated": n_checked,
        "Average field quality": f"{avg * 100:.1f}%",
        "Field statistics": {
            "author correct/matched": f"{stats['author_correct']}/{n_checked}",
            "year correct/matched": f"{stats['year_correct']}/{n_checked}",
            "venue present": f"{stats['venue_present']}/{n_checked}",
            "type valid": f"{stats['type_valid']}/{n_checked}",
            "rich extra fields (>=3)": f"{stats['extra_fields']}/{n_checked}",
        },
    }

    return score, {"score": f"{score}/35", "details": details}


# =============================================================================
# IV. BibTeX Format Compliance (20 points)
# =============================================================================

def _eval_format(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    bib_path = _find_bib(answer_dir)
    if not bib_path:
        return 0, {"score": "0/20", "details": {"error": "No .bib file"}}

    try:
        with open(bib_path, "r", encoding="utf-8", errors="ignore") as f:
            bib_content = f.read()
    except Exception as e:
        return 0, {"score": "0/20", "details": {"error": f"Read failed: {e}"}}

    if not bib_content.strip():
        return 0, {"score": "0/20", "details": {"error": "File is empty"}}

    entries = _parse_bibtex(bib_content)

    # ---- Deterministic checks (10 points) ----
    det_score = 0
    det: Dict[str, str] = {}

    # (a) No duplicate keys (3 points)
    keys = [e.get("key", "") for e in entries]
    dup_keys = len(keys) - len(set(keys))
    if dup_keys == 0:
        det_score += 3
        det["No duplicate keys"] = "3/3"
    elif dup_keys <= 2:
        det_score += 1
        det["No duplicate keys"] = f"1/3 - {dup_keys} duplicate keys"
    else:
        det["No duplicate keys"] = f"0/3 - {dup_keys} duplicate keys"

    # (b) No duplicate titles (3 points)
    titles = [_normalize_text(e.get("title", "")) for e in entries if e.get("title")]
    dup_titles = len(titles) - len(set(titles))
    if dup_titles == 0:
        det_score += 3
        det["No duplicate entries"] = "3/3"
    elif dup_titles <= 3:
        det_score += 1
        det["No duplicate entries"] = f"1/3 - {dup_titles} duplicate titles"
    else:
        det["No duplicate entries"] = f"0/3 - {dup_titles} duplicate titles"

    # (c) Brace matching (2 points)
    opens = bib_content.count("{")
    closes = bib_content.count("}")
    diff = abs(opens - closes)
    if diff == 0:
        det_score += 2
        det["Brace matching"] = "2/2"
    elif diff <= 3:
        det_score += 1
        det["Brace matching"] = f"1/2 - diff {diff}"
    else:
        det["Brace matching"] = f"0/2 - diff {diff}"

    # (d) Reasonable entry count (2 points)
    if len(entries) >= TOTAL_EXPECTED_PAPERS * 0.8:
        det_score += 2
        det["Entry count"] = f"2/2 - {len(entries)} entries"
    elif len(entries) >= TOTAL_EXPECTED_PAPERS * 0.5:
        det_score += 1
        det["Entry count"] = f"1/2 - {len(entries)} entries (low)"
    else:
        det["Entry count"] = f"0/2 - {len(entries)} entries (severely insufficient)"

    det_score = min(10, det_score)

    # ---- LLM evaluation (10 points) ----
    llm_score = 0
    llm_details: Dict[str, Any] = {}

    sample = bib_content[:8000] if len(bib_content) > 8000 else bib_content
    config = _get_text_eval_config(answer_dir)

    prompt = f"""You are a BibTeX format review expert. Please evaluate the format quality of the following BibTeX file.

This file should contain approximately {TOTAL_EXPECTED_PAPERS} BibTeX entries for academic papers, intended for LaTeX citation.

Please score on the following dimensions (integer 0-10):

1. **Format Compliance** (0-4 points):
   - Whether entry types are appropriate (article / inproceedings / book etc. matching actual publication type)
   - Whether field format is standard (values wrapped in braces, fields separated by commas)
   - Whether key naming is conventional (e.g., authorTitleYear or similar format)

2. **Information Completeness** (0-3 points):
   - Whether entries generally contain required fields (author, title, year, journal/booktitle)
   - Whether additional useful fields are present (doi, pages, volume, number, publisher)

3. **Usability** (0-3 points):
   - Whether it can be directly used for LaTeX compilation
   - No obvious garbled text or format errors
   - Special characters handled correctly (e.g., LaTeX escaping)

Please respond strictly in the following JSON format (no other content):
```json
{{{{
  "format_score": 0,
  "completeness_score": 0,
  "usability_score": 0,
  "total": 0,
  "issues": ["issue1"],
  "comment": ""
}}}}
```

BibTeX file content (may be truncated):
```bibtex
{sample}
```"""

    raw = _call_llm_judge(prompt, config)
    if raw:
        try:
            if "```json" in raw:
                raw = raw.split("```json")[1].split("```")[0].strip()
            elif "```" in raw:
                raw = raw.split("```")[1].split("```")[0].strip()
            result = json.loads(raw)
            llm_score = max(0, min(10, int(result.get("total", 0))))
            llm_details = {
                "Format compliance": f"{result.get('format_score', 0)}/4",
                "Information completeness": f"{result.get('completeness_score', 0)}/3",
                "Usability": f"{result.get('usability_score', 0)}/3",
                "Issues": result.get("issues", []),
                "Comment": result.get("comment", ""),
            }
        except (json.JSONDecodeError, ValueError, TypeError):
            llm_score = 5
            llm_details = {"note": "LLM response parsing failed, conservative score 5/10"}
    else:
        llm_score = 5
        llm_details = {"note": "LLM unavailable, conservative score 5/10"}

    total = min(20, det_score + llm_score)

    details: Dict[str, Any] = {
        "Deterministic checks": det,
        "Deterministic score": f"{det_score}/10",
        "LLM evaluation": llm_details,
        "LLM score": f"{llm_score}/10",
    }

    return total, {"score": f"{total}/20", "details": details}


# =============================================================================
# Entry Point
# =============================================================================

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """Evaluate agent's BibTeX reference output."""
    s1, r1 = _eval_file_delivery(answer_dir)
    s2, r2 = _eval_coverage(answer_dir)

    matched_pairs = r2.pop("_pairs", [])
    s3, r3 = _eval_quality(answer_dir, matched_pairs)

    s4, r4 = _eval_format(answer_dir)

    total = max(0, min(100, s1 + s2 + s3 + s4))

    report: Dict[str, Any] = {
        "total_score": total,
        "section_scores": {
            "I. File Delivery": f"{s1}/10",
            "II. Entry Coverage": f"{s2}/35",
            "III. Entry Quality": f"{s3}/35",
            "IV. Format Compliance": f"{s4}/20",
        },
        "details": {
            "I. File Delivery (10pts)": r1,
            "II. Entry Coverage (35pts)": r2,
            "III. Entry Quality (35pts)": r3,
            "IV. Format Compliance (20pts)": r4,
        },
    }

    if total >= 90:
        report["comment"] = "Excellent! BibTeX file fully covers all papers with proper format and accurate field information."
    elif total >= 75:
        report["comment"] = "Good. Most papers covered with decent entry quality, room for improvement."
    elif total >= 60:
        report["comment"] = "Passing. Basic task completed but notable gaps in coverage or field completeness."
    elif total >= 40:
        report["comment"] = "Partial completion. Low paper coverage or poor entry quality."
    else:
        report["comment"] = "Failing. Task completion severely insufficient."

    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print formatted scoring report."""
    print("=" * 70)
    print("BibTeX Reference Generation - Scoring Report")
    print("Task: Generate complete BibTeX reference file ref.bib for 65 papers")
    print("=" * 70)
    print(f"\nTotal Score: {score}/100")

    scores = report.get("section_scores", {})
    if scores:
        print("\nSection Scores:")
        for k, v in scores.items():
            print(f"  {k}: {v}")

    for section_name, section_data in report.get("details", {}).items():
        print(f"\n{'─' * 60}")
        print(f"[{section_name}] {section_data.get('score', '')}")
        print(f"{'─' * 60}")
        details = section_data.get("details", {})
        if isinstance(details, dict):
            for k, v in details.items():
                if isinstance(v, dict):
                    print(f"  {k}:")
                    for kk, vv in v.items():
                        print(f"    {kk}: {vv}")
                elif isinstance(v, list):
                    print(f"  {k}:")
                    for item in v:
                        print(f"    - {item}")
                else:
                    print(f"  {k}: {v}")

    print(f"\n{'=' * 70}")
    print(f"Comment: {report.get('comment', '')}")
    print("=" * 70)


if __name__ == "__main__":
    test_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        SCRIPT_DIR, "..", "gpt-5", "attempt_1"
    )
    if os.path.exists(test_dir):
        print(f"Evaluating directory: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"Directory does not exist: {test_dir}")
        print("Using workspace directory for testing...")
        fallback = os.path.join(SCRIPT_DIR, "..", "workspace")
        if os.path.exists(fallback):
            s, r = evaluate(fallback)
            print_report(s, r)
        else:
            print(f"Directory also does not exist: {fallback}")
    sys.exit(0)
