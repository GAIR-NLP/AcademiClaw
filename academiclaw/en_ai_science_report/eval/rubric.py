"""
Rubric for liyan-query3: AI Scientific Research Technology, Industry, and Policy Analysis Report

Task: Write a LaTeX research analysis report on AI technology in scientific
research (4-6 pages English body, >=10 references, no CSDN/Zhihu sources).
Cover technical applications, scientific impact, industry trends, challenges,
and policy/ethics.

Deliverables:
  - report.tex (required)
  - report.pdf (optional)

Total: 100 points
  1. File Delivery              (10 pts)
  2. LaTeX Format & Structure   (20 pts)
  3. References                 (15 pts)
  4. Content Quality (LLM)      (40 pts)
  5. Academic Integrity         (15 pts)
"""

import os
import re
import json
from typing import Tuple, Dict, Any, List

try:
    import openai
except ImportError:
    openai = None


# ============================================================================
# Environment / LLM helpers
# ============================================================================

def _load_env(answer_dir: str) -> dict:
    """Load .env files from answer_dir and query root."""
    values: Dict[str, str] = {}
    for env_dir in [answer_dir, os.path.join(os.path.dirname(__file__), "..")]:
        env_path = os.path.join(env_dir, ".env")
        if os.path.exists(env_path):
            try:
                with open(env_path, "r", encoding="utf-8") as f:
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


def _parse_json_response(raw: str) -> dict:
    """Parse JSON from LLM output, tolerating markdown fences."""
    if not raw:
        return {}
    text = raw.strip()
    if "```json" in text:
        text = text.split("```json", 1)[1].split("```", 1)[0].strip()
    elif "```" in text:
        text = text.split("```", 1)[1].split("```", 1)[0].strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", text, re.DOTALL)
        if m:
            try:
                return json.loads(m.group(0))
            except json.JSONDecodeError:
                pass
    return {}


# ============================================================================
# File helpers
# ============================================================================

def _find_tex(answer_dir: str) -> str:
    """Find the main .tex file. Priority: report.tex > main.tex > first .tex."""
    for name in ("report.tex", "main.tex"):
        p = os.path.join(answer_dir, name)
        if os.path.isfile(p):
            return p
    try:
        for f in sorted(os.listdir(answer_dir)):
            if f.lower().endswith(".tex") and not f.startswith("."):
                return os.path.join(answer_dir, f)
    except OSError:
        pass
    return ""


def _find_pdf(answer_dir: str) -> str:
    for name in ("report.pdf", "main.pdf"):
        p = os.path.join(answer_dir, name)
        if os.path.isfile(p):
            return p
    try:
        for f in sorted(os.listdir(answer_dir)):
            if f.lower().endswith(".pdf") and not f.startswith("."):
                return os.path.join(answer_dir, f)
    except OSError:
        pass
    return ""


def _read_text(path: str) -> str:
    if not path or not os.path.isfile(path):
        return ""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except Exception:
        return ""


def _extract_body(tex: str) -> str:
    """Extract body text between \\begin{document} and \\end{document}, strip
    LaTeX commands, bibliography, and comments for word counting."""
    m = re.search(r"\\begin\{document\}(.*?)\\end\{document\}", tex, re.DOTALL)
    body = m.group(1) if m else tex
    # Strip comments
    body = re.sub(r"%.*", "", body)
    # Remove bibliography environment
    body = re.sub(
        r"\\begin\{thebibliography\}.*?\\end\{thebibliography\}",
        "", body, flags=re.DOTALL,
    )
    # Strip commands but keep text arguments
    body = re.sub(r"\\[a-zA-Z]+\*?\{([^}]*)\}", r"\1", body)
    body = re.sub(r"\\[a-zA-Z]+\*?", "", body)
    body = re.sub(r"[{}]", "", body)
    body = re.sub(r"\s+", " ", body).strip()
    return body


# ============================================================================
# Dimension 1: File Delivery (10 pts)
# ============================================================================

def _eval_file_delivery(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details: Dict[str, str] = {}

    tex_path = _find_tex(answer_dir)
    pdf_path = _find_pdf(answer_dir)

    # 1a. .tex exists and non-empty (7 pts)
    if tex_path:
        content = _read_text(tex_path)
        name = os.path.basename(tex_path)
        if len(content.strip()) > 100:
            score += 7
            details["tex_file"] = f"7/7 - {name} ({len(content)} chars)"
        elif content.strip():
            score += 3
            details["tex_file"] = f"3/7 - {name} exists but very short ({len(content)} chars)"
        else:
            score += 1
            details["tex_file"] = f"1/7 - {name} exists but empty"
    else:
        details["tex_file"] = "0/7 - No .tex file found"

    # 1b. PDF exists (3 pts, optional)
    if pdf_path:
        try:
            sz = os.path.getsize(pdf_path)
        except OSError:
            sz = 0
        if sz > 2048:
            score += 3
            details["pdf_file"] = f"3/3 - {os.path.basename(pdf_path)} ({sz // 1024}KB)"
        elif sz > 0:
            score += 1
            details["pdf_file"] = f"1/3 - PDF very small ({sz}B)"
        else:
            details["pdf_file"] = "0/3 - PDF empty"
    else:
        details["pdf_file"] = "0/3 - No PDF (optional)"

    return score, {"score": score, "max": 10, "details": details}


# ============================================================================
# Dimension 2: LaTeX Format & Structure (20 pts)
# ============================================================================

def _eval_latex_format(tex: str) -> Tuple[int, dict]:
    score = 0
    details: Dict[str, str] = {}

    if not tex.strip():
        return 0, {"score": 0, "max": 20, "details": {"error": "No LaTeX content"}}

    # 2a. Basic LaTeX structure (5 pts): documentclass + begin/end document
    has_docclass = bool(re.search(r"\\documentclass", tex))
    has_begin = "\\begin{document}" in tex
    has_end = "\\end{document}" in tex

    if has_docclass and has_begin and has_end:
        score += 5
        details["structure"] = "5/5 - Valid LaTeX skeleton"
    elif has_docclass and has_begin:
        score += 3
        details["structure"] = "3/5 - Missing \\end{document}"
    elif has_docclass:
        score += 2
        details["structure"] = "2/5 - Only \\documentclass present"
    else:
        details["structure"] = "0/5 - Not a valid LaTeX document"

    # 2b. Academic sections (7 pts)
    tex_lower = tex.lower()
    checks = {
        "title": bool(re.search(r"\\title\s*\{", tex)),
        "abstract": bool(re.search(r"\\begin\{abstract\}", tex_lower)),
        "introduction": bool(
            re.search(r"\\section\*?\{[^}]*(?:introduction|intro)[^}]*\}", tex_lower)
        ),
        "body_sections": len(re.findall(r"\\section\*?\{", tex)) >= 3,
        "conclusion": bool(
            re.search(
                r"\\section\*?\{[^}]*(?:conclusion|summary|concluding)[^}]*\}",
                tex_lower,
            )
        ),
    }
    n_ok = sum(1 for v in checks.values() if v)
    pts = min(7, round(n_ok * 7 / 5))
    score += pts
    found = [k for k, v in checks.items() if v]
    missing = [k for k, v in checks.items() if not v]
    details["sections"] = (
        f"{pts}/7 - Found: {', '.join(found) or 'none'}; "
        f"Missing: {', '.join(missing) or 'none'}"
    )

    # 2c. Length estimation (5 pts)
    # ~500 words/page with standard margins; 4-6 pages => 2000-3000 words typical
    body = _extract_body(tex)
    wc = len(body.split())
    if 1500 <= wc <= 4500:
        score += 5
        details["length"] = f"5/5 - ~{wc} words (good range)"
    elif 1000 <= wc < 1500:
        score += 3
        details["length"] = f"3/5 - ~{wc} words (possibly < 4 pages)"
    elif 4500 < wc <= 6500:
        score += 3
        details["length"] = f"3/5 - ~{wc} words (possibly > 6 pages)"
    elif wc > 6500:
        score += 1
        details["length"] = f"1/5 - ~{wc} words (way over limit)"
    elif wc > 0:
        score += 1
        details["length"] = f"1/5 - ~{wc} words (too short)"
    else:
        details["length"] = "0/5 - No body text extracted"

    # 2d. Metadata: author, date, maketitle (3 pts)
    meta = 0
    if re.search(r"\\author\s*\{", tex):
        meta += 1
    if "\\maketitle" in tex:
        meta += 1
    if re.search(r"\\date\s*\{", tex):
        meta += 1
    score += meta
    details["metadata"] = f"{meta}/3"

    return score, {"score": score, "max": 20, "details": details}


# ============================================================================
# Dimension 3: References (15 pts)
# ============================================================================

FORBIDDEN_SOURCES = [
    "csdn", "csdn.net", "blog.csdn",
    "zhihu", "zhihu.com", "zhuanlan.zhihu",
    "jianshu", "jianshu.com",
    "baidu.com/baike", "baidubaike",
    "百度文库", "百度百科",
]


def _count_refs(tex: str) -> int:
    """Count references (bibitem or unique cite keys)."""
    bibitems = len(re.findall(r"\\bibitem", tex))
    if bibitems > 0:
        return bibitems
    # BibTeX style: count unique cite keys
    cites = set()
    for m in re.findall(r"\\cite\{([^}]+)\}", tex):
        for key in m.split(","):
            k = key.strip()
            if k:
                cites.add(k)
    return len(cites)


def _find_forbidden(tex: str) -> List[str]:
    tex_lower = tex.lower()
    found = []
    for src in FORBIDDEN_SOURCES:
        if src.lower() in tex_lower:
            found.append(src)
    return list(set(found))


def _eval_references(tex: str) -> Tuple[int, dict]:
    score = 0
    details: Dict[str, str] = {}
    ref_count = _count_refs(tex)
    forbidden = _find_forbidden(tex)

    # 3a. Reference count (10 pts)
    if ref_count >= 10:
        score += 10
        details["count"] = f"10/10 - {ref_count} references"
    elif ref_count >= 7:
        score += 6
        details["count"] = f"6/10 - {ref_count} references (need >= 10)"
    elif ref_count >= 4:
        score += 3
        details["count"] = f"3/10 - {ref_count} references (need >= 10)"
    elif ref_count > 0:
        score += 1
        details["count"] = f"1/10 - {ref_count} references (need >= 10)"
    else:
        details["count"] = "0/10 - No references found"

    # 3b. No forbidden sources (5 pts)
    if not forbidden:
        score += 5
        details["forbidden"] = "5/5 - No prohibited sources"
    else:
        details["forbidden"] = f"0/5 - Prohibited sources: {', '.join(forbidden)}"

    return score, {
        "score": score,
        "max": 15,
        "details": details,
        "ref_count": ref_count,
        "has_forbidden": len(forbidden) > 0,
    }


# ============================================================================
# Dimension 4: Content Quality — LLM-as-Judge (40 pts)
# ============================================================================

_CONTENT_PROMPT = """\
You are a strict academic evaluator. Assess the following LaTeX research report
on "AI technology applications in scientific research".

The report should cover:
1. Technical depth: specific AI techniques applied in scientific domains
   (protein folding, climate modeling, materials, drug discovery, etc.)
2. Scientific impact: how AI transforms research workflows and discoveries
3. Industry trends: commercial applications, investment, startups
4. Challenges: data quality, reproducibility, interpretability, compute cost
5. Policy/ethics: responsible AI, regulation, bias, data governance

REPORT (LaTeX source, possibly truncated):
---
{content}
---

Score strictly on these sub-dimensions. Return ONLY valid JSON:

{{
  "technical_depth": {{"score": <0-15>, "reason": "<brief>"}},
  "coverage_and_impact": {{"score": <0-10>, "reason": "<brief>"}},
  "industry_policy": {{"score": <0-10>, "reason": "<brief>"}},
  "writing_clarity": {{"score": <0-5>, "reason": "<brief>"}},
  "total": <sum, 0-40>,
  "comment": "<1-2 sentences>"
}}

Scoring guide:
- technical_depth (0-15): 13-15 expert with specific examples; 9-12 good; 5-8 surface; 0-4 missing
- coverage_and_impact (0-10): 8-10 comprehensive; 5-7 adequate; 0-4 thin
- industry_policy (0-10): 8-10 substantive; 5-7 present but shallow; 0-4 absent
- writing_clarity (0-5): 4-5 well-organized; 2-3 acceptable; 0-1 poor

If content is clearly irrelevant to the topic, total must be 0.
If content is mostly filler with little substance, cap total at 10.
"""


def _heuristic_content(tex: str) -> Tuple[int, dict]:
    """Keyword-based fallback when LLM is unavailable. Conservative: max 20/40."""
    body = _extract_body(tex).lower()
    wc = len(body.split())

    ai_kw = [
        "artificial intelligence", "machine learning", "deep learning",
        "neural network", "transformer", "large language model",
        "reinforcement learning", "generative model",
    ]
    sci_kw = [
        "protein", "drug discovery", "climate", "materials science",
        "genomics", "alphafold", "scientific discovery", "biomedical",
        "weather", "molecular",
    ]
    ind_kw = ["industry", "startup", "investment", "commercial", "market"]
    pol_kw = ["policy", "regulation", "ethics", "governance", "responsible ai", "bias"]

    ai_hits = sum(1 for k in ai_kw if k in body)
    sci_hits = sum(1 for k in sci_kw if k in body)
    ind_hits = sum(1 for k in ind_kw if k in body)
    pol_hits = sum(1 for k in pol_kw if k in body)

    td = min(7, (ai_hits + sci_hits) * 2)
    cv = min(5, sci_hits * 2)
    ip = min(5, (ind_hits + pol_hits) * 2)
    wr = 3 if wc >= 1500 else (2 if wc >= 800 else (1 if wc > 0 else 0))
    total = min(20, td + cv + ip + wr)

    return total, {
        "note": "LLM unavailable; heuristic scoring (max 20/40)",
        "tech": td, "coverage": cv, "ind_pol": ip, "writing": wr,
    }


def _eval_content(tex: str, answer_dir: str) -> Tuple[int, dict]:
    details: Dict[str, Any] = {}

    if not tex.strip():
        return 0, {"score": 0, "max": 40, "details": {"error": "No content"}}

    prompt = _CONTENT_PROMPT.format(content=tex[:40000])
    config = _get_text_eval_config(answer_dir)
    raw = _call_llm_judge(prompt, config)
    parsed = _parse_json_response(raw)

    if parsed and "total" in parsed:
        td = parsed.get("technical_depth", {})
        ci = parsed.get("coverage_and_impact", {})
        ip = parsed.get("industry_policy", {})
        wc = parsed.get("writing_clarity", {})

        td_s = max(0, min(15, int(td.get("score", 0))))
        ci_s = max(0, min(10, int(ci.get("score", 0))))
        ip_s = max(0, min(10, int(ip.get("score", 0))))
        wc_s = max(0, min(5, int(wc.get("score", 0))))
        total = max(0, min(40, td_s + ci_s + ip_s + wc_s))

        details["technical_depth"] = f"{td_s}/15 - {td.get('reason', '')}"
        details["coverage_impact"] = f"{ci_s}/10 - {ci.get('reason', '')}"
        details["industry_policy"] = f"{ip_s}/10 - {ip.get('reason', '')}"
        details["writing_clarity"] = f"{wc_s}/5 - {wc.get('reason', '')}"
        details["comment"] = parsed.get("comment", "")
        details["eval_model"] = config.get("model", "unknown")
        return total, {"score": total, "max": 40, "details": details}

    # Fallback
    fb_score, fb_info = _heuristic_content(tex)
    details.update(fb_info)
    if raw:
        details["llm_raw_snippet"] = raw[:200]
    return fb_score, {"score": fb_score, "max": 40, "details": details}


# ============================================================================
# Dimension 5: Academic Integrity (15 pts)
# ============================================================================

def _eval_integrity(tex: str, ref_count: int, has_forbidden: bool) -> Tuple[int, dict]:
    score = 0
    details: Dict[str, str] = {}

    # 5a. No forbidden sources — hard penalty (5 pts)
    if not has_forbidden:
        score += 5
        details["no_forbidden"] = "5/5 - Clean"
    else:
        details["no_forbidden"] = "0/5 - Prohibited sources detected"

    # 5b. In-text citations (5 pts)
    cite_count = len(re.findall(r"\\cite\{", tex))
    if cite_count >= 8:
        score += 5
        details["citations"] = f"5/5 - {cite_count} \\cite calls"
    elif cite_count >= 5:
        score += 3
        details["citations"] = f"3/5 - {cite_count} \\cite calls"
    elif cite_count >= 2:
        score += 2
        details["citations"] = f"2/5 - {cite_count} \\cite calls"
    elif cite_count > 0:
        score += 1
        details["citations"] = f"1/5 - {cite_count} \\cite call"
    else:
        details["citations"] = "0/5 - No \\cite found"

    # 5c. Originality indicators (5 pts)
    body = _extract_body(tex)
    wc = len(body.split())
    unique = len(set(body.lower().split())) if wc > 0 else 0
    vocab_ratio = unique / wc if wc > 0 else 0
    section_count = len(re.findall(r"\\(?:sub)*section\*?\{", tex))

    if vocab_ratio >= 0.30 and section_count >= 4 and wc >= 1200:
        score += 5
        details["originality"] = (
            f"5/5 - Vocab diversity {vocab_ratio:.2f}, {section_count} sections"
        )
    elif vocab_ratio >= 0.20 and section_count >= 3:
        score += 3
        details["originality"] = (
            f"3/5 - Vocab diversity {vocab_ratio:.2f}, {section_count} sections"
        )
    elif wc > 500:
        score += 1
        details["originality"] = (
            f"1/5 - Low diversity {vocab_ratio:.2f} or few sections ({section_count})"
        )
    else:
        details["originality"] = "0/5 - Insufficient content"

    return score, {"score": score, "max": 15, "details": details}


# ============================================================================
# Main entry points
# ============================================================================

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Evaluate agent output for liyan-query3.

    Args:
        answer_dir: Absolute path to agent output directory.

    Returns:
        (score, report) where score is 0-100 and report is a detailed dict.
    """
    tex_path = _find_tex(answer_dir)
    tex = _read_text(tex_path)

    # --- Dimension 1: File Delivery (10 pts) ---
    s1, r1 = _eval_file_delivery(answer_dir)

    if not tex.strip():
        report = {
            "total": s1,
            "result_score": {"score": s1, "details": r1["details"], "deductions": []},
            "process_score": {"score": 0, "details": {}, "deductions": []},
            "comment": "No LaTeX report found or file is empty.",
            "breakdown": {
                "file_delivery": f"{s1}/10",
                "latex_format": "0/20",
                "references": "0/15",
                "content_quality": "0/40",
                "academic_integrity": "0/15",
            },
        }
        return s1, report

    # --- Dimension 2: LaTeX Format & Structure (20 pts) ---
    s2, r2 = _eval_latex_format(tex)

    # --- Dimension 3: References (15 pts) ---
    s3, r3 = _eval_references(tex)

    # --- Dimension 4: Content Quality (40 pts) ---
    s4, r4 = _eval_content(tex, answer_dir)

    # --- Dimension 5: Academic Integrity (15 pts) ---
    s5, r5 = _eval_integrity(
        tex, r3.get("ref_count", 0), r3.get("has_forbidden", False)
    )

    total = s1 + s2 + s3 + s4 + s5
    penalties: List[str] = []

    # Penalty: forbidden sources -> score to 0
    if r3.get("has_forbidden", False):
        total = 0
        penalties.append("Score zeroed: prohibited sources (CSDN/Zhihu/etc.) detected")

    # Penalty: fewer than 10 references -> cap at 60
    if r3.get("ref_count", 0) < 10 and total > 60:
        total = 60
        penalties.append(
            f"Capped at 60: only {r3['ref_count']} references (need >= 10)"
        )

    # Penalty: not valid LaTeX -> cap at 60
    if not re.search(r"\\documentclass", tex) and total > 60:
        total = 60
        penalties.append("Capped at 60: not a valid LaTeX document")

    total = max(0, min(100, total))

    # Qualitative comment
    if total >= 90:
        comment = "Excellent report: comprehensive, well-structured, fully compliant."
    elif total >= 75:
        comment = "Good report: meets most requirements with minor gaps."
    elif total >= 60:
        comment = "Adequate: basic requirements met but notable weaknesses."
    elif total >= 40:
        comment = "Below expectations: significant issues in content or compliance."
    else:
        comment = "Unsatisfactory: major requirements unmet."

    report = {
        "total": total,
        "result_score": {
            "score": s1 + s4,
            "details": {
                "1_file_delivery": r1["details"],
                "4_content_quality": r4["details"],
            },
            "deductions": [],
        },
        "process_score": {
            "score": s2 + s3 + s5,
            "details": {
                "2_latex_format": r2["details"],
                "3_references": r3["details"],
                "5_academic_integrity": r5["details"],
            },
            "deductions": [],
        },
        "comment": comment,
        "breakdown": {
            "file_delivery": f"{s1}/10",
            "latex_format": f"{s2}/20",
            "references": f"{s3}/15",
            "content_quality": f"{s4}/40",
            "academic_integrity": f"{s5}/15",
        },
        "penalty_notes": penalties,
    }
    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print formatted evaluation report."""
    print("=" * 70)
    print("Rubric Report: liyan-query3")
    print("Task: AI in Scientific Research - Technical/Industry/Policy Report")
    print("=" * 70)
    print(f"\nTotal Score: {score}/100\n")

    breakdown = report.get("breakdown", {})
    if breakdown:
        print("Score Breakdown:")
        for dim, val in breakdown.items():
            print(f"  {dim:25s} {val}")

    penalties = report.get("penalty_notes", [])
    if penalties:
        print("\nPenalties:")
        for p in penalties:
            print(f"  * {p}")

    for key, label in [
        ("result_score", "Result (File + Content)"),
        ("process_score", "Process (Format + Refs + Integrity)"),
    ]:
        section = report.get(key, {})
        print(f"\n{'─' * 55}")
        print(f"  [{label}]  {section.get('score', 0)} pts")
        print(f"{'─' * 55}")
        for cat, items in section.get("details", {}).items():
            print(f"\n  {cat}:")
            if isinstance(items, dict):
                for k, v in items.items():
                    print(f"    {k}: {v}")
            else:
                print(f"    {items}")

    print(f"\n{'=' * 55}")
    print(f"Comment: {report.get('comment', '')}")
    print("=" * 70)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        test_dir = sys.argv[1]
    else:
        test_dir = os.path.join(os.path.dirname(__file__), "..")

    # Resolve relative paths from the query root
    if not os.path.isabs(test_dir):
        test_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            test_dir,
        )

    if os.path.exists(test_dir):
        print(f"Evaluating: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"Directory not found: {test_dir}")
    sys.exit(0)
