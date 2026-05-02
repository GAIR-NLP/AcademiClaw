"""
ruitao-query3: Locking Dance Choreography Evaluation Rubric (rewritten from scratch)

Task Overview
-------------
Agent must design a Locking choreography for an 8x8 counts (64 beats) Funk track
"Funky Master Lock" (115 BPM, F minor), output file answer.txt, strictly following
output_format.md format.

Music structure: Intro(1-8) -> Verse1(9-24) -> Chorus1(25-40) -> Bridge(41-48)
          -> Chorus2(49-64) -> Outro(65-72)
Key sounds: cowbell Chorus 2&4, congas transitions, DJ scratch Bridge opening

Total score 100:
  Dim-1  Structure and Format Completeness   15 pts  (auto)
  Dim-2  Musical Treatment Depth              15 pts  (auto)
  Dim-3  Technical Element Completeness       10 pts  (auto)
  Dim-4  LLM Comprehensive Evaluation         60 pts  (LLM-as-Judge)
         4a Musical treatment ability    24
         4b Technical presentation       18
         4c Creative choreography        12
         4d Format compliance             6
"""

import os
import re
import json
from typing import Tuple, Dict, Any, List

try:
    import openai
except ImportError:
    openai = None


# ═══════════════════════════════════════════════════════════════════════════
# Common Utilities
# ═══════════════════════════════════════════════════════════════════════════

def _load_env(answer_dir: str) -> dict:
    """Load .env from answer_dir and query root directory."""
    values: dict = {}
    for d in [answer_dir, os.path.join(os.path.dirname(__file__), "..")]:
        p = os.path.join(d, ".env")
        if not os.path.exists(p):
            continue
        try:
            with open(p, "r", encoding="utf-8") as fh:
                for ln in fh:
                    ln = ln.strip()
                    if not ln or ln.startswith("#") or "=" not in ln:
                        continue
                    k, v = ln.split("=", 1)
                    k = k.strip()
                    if k not in values:
                        values[k] = v.strip().strip("'\"")
        except Exception:
            pass
    return values


def _get_text_eval_config(answer_dir: str) -> dict:
    env = _load_env(answer_dir)
    def g(key: str, fallback: str = "") -> str:
        return os.environ.get(key) or env.get(key) or fallback
    return {
        "api_key": g("EVAL_TEXT_API_KEY", g("ANTHROPIC_API_KEY")),
        "api_base": g("EVAL_TEXT_API_BASE_URL", g("ANTHROPIC_BASE_URL")),
        "model":   g("EVAL_TEXT_MODEL", "openai/gpt-5.2"),
    }


def _call_llm_judge(prompt: str, config: dict) -> str:
    """Call LLM; return empty string on failure."""
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
    except Exception as exc:
        print(f"[RUBRIC] LLM call failed: {exc}")
        return ""


def _read_answer(answer_dir: str) -> str:
    """Read answer.txt, try multiple locations."""
    for name in ["answer.txt"]:
        for sub in ["", "workspace"]:
            fp = os.path.join(answer_dir, sub, name) if sub else os.path.join(answer_dir, name)
            if os.path.isfile(fp):
                try:
                    with open(fp, "r", encoding="utf-8", errors="replace") as f:
                        return f.read().strip()
                except Exception:
                    pass
    return ""


# ═══════════════════════════════════════════════════════════════════════════
# Dim-1  Structure and Format Completeness  (15 pts)
# ═══════════════════════════════════════════════════════════════════════════
# 10 required sections -> 1 pt each (max 10)
# Segment subfield coverage -> max 5 pts

_REQUIRED_SECTIONS = [
    "Routine Overview",
    "Music Structure Mapping",
    "Intro",
    "Verse 1",
    "Chorus 1",
    "Bridge",
    "Chorus 2",
    "Outro",
    "Technical Elements Summary",
    "Creative Highlights",
]

_SECTION_SUBFIELDS: Dict[str, List[str]] = {
    "Intro":     ["Music Features", "Counts Breakdown", "Locking Elements", "Rhythm Treatment"],
    "Verse 1":   ["Music Features", "Counts Breakdown", "Locking Elements", "Rhythm Treatment",
                   "Element Repetition Logic"],
    "Chorus 1":  ["Music Features", "Counts Breakdown", "Locking Elements", "Rhythm Treatment",
                   "Syncopation", "Performance Energy"],
    "Bridge":    ["Music Features", "Counts Breakdown", "Locking Elements", "Rhythm Treatment",
                   "Syncopation", "Transition Logic"],
    "Chorus 2":  ["Music Features", "Counts Breakdown", "Locking Elements", "Rhythm Treatment",
                   "Syncopation", "Performance Peak"],
    "Outro":     ["Music Features", "Counts Breakdown", "Locking Elements", "Rhythm Treatment",
                   "Final Impact"],
}


def _has_section(text: str, name: str) -> bool:
    return bool(re.search(r"##\s+" + re.escape(name), text, re.IGNORECASE))


def _section_body(text: str, name: str) -> str:
    """Extract text from a section heading to the next ## heading."""
    m = re.search(
        r"##\s+" + re.escape(name) + r"[^\n]*\n(.*?)(?=\n##\s|\Z)",
        text, re.IGNORECASE | re.DOTALL,
    )
    return m.group(1) if m else ""


def _dim1_structure(text: str) -> Tuple[int, Dict[str, Any]]:
    info: Dict[str, Any] = {}

    # --- 10 sections ---
    found, missing = [], []
    for sec in _REQUIRED_SECTIONS:
        (found if _has_section(text, sec) else missing).append(sec)
    sec_pts = min(10, len(found))
    info["sections_found"]   = found
    info["sections_missing"] = missing
    info["section_pts"]      = f"{sec_pts}/10"

    # --- subfield coverage ---
    total_sf, hit_sf = 0, 0
    for sec_name, fields in _SECTION_SUBFIELDS.items():
        body = _section_body(text, sec_name)
        for f in fields:
            total_sf += 1
            # Prefer finding in section body; fallback to finding **Field**: in full text
            if re.search(re.escape(f), body, re.IGNORECASE):
                hit_sf += 1
            elif re.search(r"\*\*" + re.escape(f) + r"\*?\*?\s*:", text, re.IGNORECASE):
                hit_sf += 1

    sf_ratio = hit_sf / total_sf if total_sf else 0
    sf_pts = round(min(5.0, sf_ratio * 5.0), 1)
    info["subfields"] = f"{hit_sf}/{total_sf}"
    info["subfield_pts"] = f"{sf_pts}/5"

    score = int(round(min(15, sec_pts + sf_pts)))
    return score, info


# ═══════════════════════════════════════════════════════════════════════════
# Dim-2  Musical Treatment Depth  (15 pts)
# ═══════════════════════════════════════════════════════════════════════════
# 2a Instrument reference variety (5)
# 2b Syncopation mention count (5)
# 2c Rhythm layer descriptions (5)

_INSTR_KW = [
    "cowbell", "hi-hat", "snare", "kick", "bass", "guitar",
    "vocal", "drum", "rhodes", "keyboard", "synth", "congas",
    "cymbal",
]
_SYNC_KW = ["syncopation", "syncopated", "off-beat"]
_RLAYER_KW = [
    "rhythm layer", "polyrhythm",
    "multi-layer", "triple", "layer",
]


def _dim2_music(text: str) -> Tuple[int, Dict[str, Any]]:
    info: Dict[str, Any] = {}
    lo = text.lower()
    pts = 0

    # 2a instruments
    found_instr = list({kw for kw in _INSTR_KW if kw.lower() in lo})
    n = len(found_instr)
    ip = 5 if n >= 5 else (3 if n >= 3 else (1 if n >= 1 else 0))
    pts += ip
    info["instruments"] = found_instr
    info["instrument_pts"] = f"{ip}/5"

    # 2b syncopation
    sc = sum(len(re.findall(re.escape(k), text, re.IGNORECASE)) for k in _SYNC_KW)
    sp = 5 if sc >= 4 else (3 if sc >= 2 else (1 if sc >= 1 else 0))
    pts += sp
    info["syncopation_count"] = sc
    info["syncopation_pts"] = f"{sp}/5"

    # 2c rhythm layers
    rc = sum(1 for k in _RLAYER_KW if k.lower() in lo)
    rp = 5 if rc >= 3 else (3 if rc >= 2 else (2 if rc >= 1 else 0))
    pts += rp
    info["rhythm_layer_kw"] = rc
    info["rhythm_layer_pts"] = f"{rp}/5"

    return min(15, pts), info


# ═══════════════════════════════════════════════════════════════════════════
# Dim-3  Technical Element Completeness  (10 pts)
# ═══════════════════════════════════════════════════════════════════════════
# 3a Core Locking element coverage (6)
# 3b Technical Elements Summary sub-items completeness (4)

_CORE_ELEMENTS = [
    "Lock", "Point", "Wrist roll", "Scooby Doo",
    "Up lock", "Which-a-way", "Stop & Go", "Funky guitar",
]
_TECH_LABELS = [
    "Core Locking Elements Used",
    "Rhythm Complexity",
    "Musicality Demonstration",
    "Performance Elements",
]


def _dim3_technical(text: str) -> Tuple[int, Dict[str, Any]]:
    info: Dict[str, Any] = {}
    lo = text.lower()
    pts = 0.0

    # 3a elements
    core_hit = [e for e in _CORE_ELEMENTS if e.lower() in lo]
    nc = len(core_hit)
    cp = 6 if nc >= 7 else (4 if nc >= 5 else (2 if nc >= 3 else 0))
    pts += cp
    info["core_elements"] = core_hit
    info["core_pts"] = f"{cp}/6"

    # 3b summary
    has_sum = _has_section(text, "Technical Elements Summary")
    tp = 0.0
    if has_sum:
        tp += 1.0
        body = _section_body(text, "Technical Elements Summary")
        for lab in _TECH_LABELS:
            if lab.lower() in body.lower() or lab.lower() in lo:
                tp += 0.75
    tp = min(4.0, tp)
    pts += tp
    info["summary_present"] = has_sum
    info["summary_pts"] = f"{tp:.1f}/4"

    return min(10, int(round(pts))), info


# ═══════════════════════════════════════════════════════════════════════════
# Dim-4  LLM-as-Judge Comprehensive Evaluation  (60 pts)
# ═══════════════════════════════════════════════════════════════════════════

_LLM_PROMPT = """\
You are a professional Locking street dance choreography evaluation expert. Please strictly evaluate the following choreography plan.

## Task Background
Track: "Funky Master Lock", 115 BPM, F minor funk
Structure: Intro(1-8) -> Verse1(9-24) -> Chorus1(25-40) -> Bridge(41-48) -> Chorus2(49-64) -> Outro(65-72)
Instruments: Electric bass (slap/pop), electric guitar (wah-wah chunking, chorus has solo), Rhodes electric piano,
      standard funk drum kit (snare 2&4, hi-hat eighth notes, kick 1&3), vocals (verse narrative/chorus excited)
Key sounds: Cowbell Chorus 2&4, congas transitions, DJ scratch Bridge opening, riser (Verse->Chorus transition)
Requirements: Pure Locking style, >=5 core elements, >=2 syncopation instances, full 8x8 counts coverage.
Output: answer.txt strictly following output_format.md section and subfield requirements.

## Choreography to Evaluate
{answer}

## Scoring Dimensions — Grade strictly, err on the lower side

### 1. Musical Treatment Ability (0-24)

1a. Sound timing correspondence (0-8)
  Does the Counts Breakdown explicitly specify which instruments (cowbell/snare/bass/guitar) are on which beats, and how movements respond?
  7-8: Multiple instruments with precise beat-level correspondence, specific descriptions (e.g., "count 2 chest lock matching snare")
  4-6: Mentions instruments but correspondence is vague, or only broadly described in Music Features
  0-3: Movements lack connection to instruments

1b. Syncopation treatment (0-8)
  Are there explicit, executable movements on "&" beats or finer "e/a" positions? Not merely mentioning "syncopation" verbally.
  7-8: >=3 specific off-beat movements (specifying what happens on which & or e), creatively rich
  4-6: 1-2 specific syncopated movements
  0-3: Only mentions "syncopation" without specific movements, or lacking

1c. Section emotional arc (0-8)
  Is there significant differentiation in energy/texture across Intro->Verse->Chorus->Bridge->Chorus2->Outro?
  7-8: Each section has distinct character, choreographic approaches clearly differ, overall arc is complete
  4-6: Some section differentiation but not distinct enough
  0-3: Sections are homogeneous

### 2. Technical Presentation Quality (0-18)

2a. Locking style purity (0-6)
  Do movement names/descriptions conform to Locking technical standards? Is there mixing of breaking/popping/freestyle?
  5-6: Pure and accurate  3-4: Mostly accurate  0-2: Clear deviations

2b. Movement executability (0-6)
  Can a dancer directly follow the Counts Breakdown descriptions? Are direction/body part/texture specified?
  5-6: Specific and executable  3-4: Partially vague  0-2: Too general to execute

2c. Combination transition reasonability (0-6)
  Do transitions between elements consider weight transfer, timing allowance, body physics?
  5-6: Smooth and reasonable  3-4: Occasionally abrupt  0-2: Stiff/unworkable

### 3. Creative Choreography Level (0-12)

3a. Innovation and originality (0-6)
  Does it go beyond template-style content from output_format.md examples? Are there unique choreographic highlights?
  5-6: Significantly innovative  3-4: Some novelty  0-2: Copies template

3b. Performance layers (0-6)
  Are energy progression, spatial usage (front/side/back/high/low), sight-line/focus management rich?
  5-6: Multi-layered  3-4: Present but thin  0-2: Lacking

### 4. Format Compliance (0-6)

4a. Format adherence (0-6)
  Does it include all required sections (10) and subfields? Are heading levels correct? No instructional language?
  5-6: Fully compliant  3-4: Minor deviations  0-2: Format chaotic

Please reply strictly in the following JSON format, do not output any other text:
```json
{{
  "1a_score": 0, "1a_reason": "",
  "1b_score": 0, "1b_reason": "",
  "1c_score": 0, "1c_reason": "",
  "2a_score": 0, "2a_reason": "",
  "2b_score": 0, "2b_reason": "",
  "2c_score": 0, "2c_reason": "",
  "3a_score": 0, "3a_reason": "",
  "3b_score": 0, "3b_reason": "",
  "4a_score": 0, "4a_reason": ""
}}
```
"""

_LLM_LIMITS = {
    "1a_score": 8, "1b_score": 8, "1c_score": 8,
    "2a_score": 6, "2b_score": 6, "2c_score": 6,
    "3a_score": 6, "3b_score": 6,
    "4a_score": 6,
}


def _parse_llm_json(raw: str) -> dict:
    if not raw:
        return {}
    try:
        t = raw
        if "```json" in t:
            t = t.split("```json")[1].split("```")[0].strip()
        elif "```" in t:
            t = t.split("```")[1].split("```")[0].strip()
        return json.loads(t)
    except (json.JSONDecodeError, IndexError):
        print(f"[RUBRIC] LLM JSON parse error: {raw[:300]}")
        return {}


def _dim4_llm(text: str, config: dict) -> Tuple[int, Dict[str, Any]]:
    prompt = _LLM_PROMPT.format(answer=text[:12000])
    raw = _call_llm_judge(prompt, config)
    parsed = _parse_llm_json(raw)

    if not parsed:
        return 24, {
            "note": "LLM unavailable or JSON parse failed; fallback 24/60",
            "raw_snippet": raw[:500] if raw else "(empty)",
        }

    total = 0
    details: Dict[str, Any] = {}
    for key, cap in _LLM_LIMITS.items():
        v = max(0, min(cap, int(parsed.get(key, 0))))
        total += v
        details[key] = v
        details[key.replace("_score", "_reason")] = parsed.get(
            key.replace("_score", "_reason"), "")

    total = max(0, min(60, total))
    details["llm_total"] = total
    return total, details


# ═══════════════════════════════════════════════════════════════════════════
# Main Entry
# ═══════════════════════════════════════════════════════════════════════════

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Evaluate the agent's output directory.

    Args:
        answer_dir: Absolute path to agent output (e.g., .../gpt-5/attempt_1)

    Returns:
        (score, report) — score: 0-100 int; report: details dict
    """
    text = _read_answer(answer_dir)
    if not text:
        return 0, {"error": "answer.txt not found or empty"}

    s1, d1 = _dim1_structure(text)
    s2, d2 = _dim2_music(text)
    s3, d3 = _dim3_technical(text)

    cfg = _get_text_eval_config(answer_dir)
    s4, d4 = _dim4_llm(text, cfg)

    total = max(0, min(100, s1 + s2 + s3 + s4))

    report: Dict[str, Any] = {
        "total": total,
        "breakdown": {
            "Dim1_structure": f"{s1}/15",
            "Dim2_music":     f"{s2}/15",
            "Dim3_technical": f"{s3}/10",
            "Dim4_llm":       f"{s4}/60",
        },
        "auto_details": {
            "structure": d1,
            "music":     d2,
            "technical": d3,
        },
        "llm_details": d4,
        "answer_dir": answer_dir,
    }
    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print formatted evaluation report."""
    sep = "=" * 65
    print(sep)
    print("  ruitao-query3 · Locking Choreography Evaluation Report")
    print(sep)

    if "error" in report:
        print(f"\n  ERROR: {report['error']}\n")
        return

    print(f"\n  TOTAL SCORE: {score} / 100\n")

    # breakdown
    bd = report.get("breakdown", {})
    if bd:
        print("  Breakdown:")
        for k, v in bd.items():
            print(f"    {k:20s} {v}")

    # auto details
    print(f"\n{'─' * 60}")
    print("  Auto-evaluation details")
    print(f"{'─' * 60}")
    for cat, items in report.get("auto_details", {}).items():
        print(f"\n  [{cat}]")
        if isinstance(items, dict):
            for k, v in items.items():
                if isinstance(v, list):
                    print(f"    {k}: {', '.join(str(x) for x in v)}")
                else:
                    print(f"    {k}: {v}")

    # llm details
    print(f"\n{'─' * 60}")
    print("  LLM Judge details")
    print(f"{'─' * 60}")
    llm = report.get("llm_details", {})
    if isinstance(llm, dict):
        for k, v in llm.items():
            print(f"    {k}: {v}")

    print(f"\n{sep}")


# ═══════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = os.path.join(os.path.dirname(__file__), "..", "gpt-5", "attempt_1")

    if os.path.exists(target):
        print(f"Evaluating: {target}\n")
        sc, rp = evaluate(target)
        print_report(sc, rp)
    else:
        print(f"Directory not found: {target}")
    sys.exit(0)
