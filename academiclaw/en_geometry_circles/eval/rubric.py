"""
Geometry Optimization: Find the Maximum Value of MN and Its Relation to the Radius — Scoring Script

Total score: 100 points, 4 scoring dimensions:
  I.   File Delivery              (10 pts)  — Answer file exists and contains valid content
  II.  MN Maximum Correctness     (35 pts)  — Clearly states MN max = 6
  III. Radius Relationship        (25 pts)  — States |MN|_max = 2R (diameter relationship)
  IV.  Derivation Quality         (30 pts)  — LLM-as-Judge evaluates the derivation process
"""

import os
import re
import json
from typing import Tuple, Dict, Any, List

try:
    import openai
except ImportError:
    openai = None


# -- Environment / LLM utilities ----------------------------------------

def _load_env(answer_dir: str) -> dict:
    values: dict = {}
    for d in [answer_dir, os.path.join(os.path.dirname(__file__), "..")]:
        p = os.path.join(d, ".env")
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as fh:
                    for line in fh:
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
        base = config.get("api_base", "").rstrip("/")
        if base and not base.endswith("/v1"):
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
        print(f"[RUBRIC] LLM Judge error: {e}")
        return ""


# -- Helpers -------------------------------------------------------------

_TEXT_EXTS = {".md", ".txt", ".tex"}


def _find_answer_files(answer_dir: str) -> List[str]:
    """Collect all readable text files in the answer directory, preferring answer/solution names."""
    if not os.path.isdir(answer_dir):
        return []
    candidates = []
    for fn in os.listdir(answer_dir):
        fp = os.path.join(answer_dir, fn)
        if os.path.isfile(fp) and os.path.splitext(fn)[1].lower() in _TEXT_EXTS:
            candidates.append(fp)
    if not candidates:
        return []
    preferred = [
        fp for fp in candidates
        if any(kw in os.path.basename(fp).lower()
               for kw in ("answer", "solution", "result"))
    ]
    return preferred if preferred else candidates


def _read_text(files: List[str]) -> str:
    parts: List[str] = []
    for fp in files:
        try:
            with open(fp, "r", encoding="utf-8", errors="ignore") as fh:
                parts.append(fh.read())
        except Exception:
            continue
    return "\n".join(parts)


# -- I. File Delivery (10 pts) ------------------------------------------

def _score_file_delivery(answer_dir: str) -> Tuple[int, dict]:
    info: dict = {}
    if not os.path.isdir(answer_dir):
        info["status"] = "Directory does not exist"
        return 0, info

    files = _find_answer_files(answer_dir)
    if not files:
        info["status"] = "No answer files found (.md / .txt)"
        return 0, info

    text = _read_text(files).strip()
    names = [os.path.basename(f) for f in files]

    if len(text) == 0:
        info["status"] = f"File exists but is empty: {names}"
        return 2, info
    if len(text) < 20:
        info["status"] = f"Content too short ({len(text)} chars): {names}"
        return 5, info

    info["status"] = f"OK — {names}, {len(text)} chars"
    return 10, info


# -- II. MN Maximum Correctness (35 pts) --------------------------------
#
# Correct answer: |MN|_max = 6
# Scoring tiers:
#   35  — Clearly states MN max = 6
#   30  — Writes MN = 6 but does not label it as "maximum"
#   25  — Vaguely mentions maximum is 6
#   10  — Number 6 appears in text but not associated with MN maximum
#    0  — Not provided

def _score_max_value(text: str) -> Tuple[int, dict]:
    info: dict = {}
    if not text.strip():
        info["detail"] = "No content"
        return 0, info

    SIX = r"6(?:\.0+)?(?!\d)"

    # Compact text (for whitespace-free matching)
    compact = re.sub(r"\s+", "", text)

    # High confidence: explicit "MN max = 6" variants
    high_pats = [
        rf"[|｜]?MN[|｜]?_?\{{?(?:max|\\max)\}}?\s*=\s*{SIX}",
        rf"MN\s*(?:的)?\s*最大值\s*(?:=|为|是|等于|：|:)\s*{SIX}",
        rf"MN[^\n]{{0,50}}(?:最大值|maximum|max)[^\n]{{0,40}}(?:=|为|是|等于)\s*{SIX}",
        rf"(?:最大值|maximum|max)\s*(?:=|为|是|等于|：|:)\s*{SIX}",
    ]
    high_compact = [
        rf"MN[^a-zA-Z]{{0,30}}(?:最大值|max).*?(?:=|为|是){SIX}",
        rf"\|MN\|_?max=?{SIX}",
        rf"MNmax=?{SIX}",
    ]

    # Medium confidence: MN = 6
    mid_pats = [
        rf"[|｜]?MN[|｜]?\s*=\s*{SIX}",
    ]

    # Low confidence: max...6
    low_pats = [
        rf"(?:最大|max).*?(?:为|=|是|：|:)\s*{SIX}",
        rf"{SIX}\s*(?:即|就是|为).*?(?:最大)",
    ]

    def _any(patterns: list, target: str) -> bool:
        return any(re.search(p, target, re.IGNORECASE) for p in patterns)

    if _any(high_pats, text) or _any(high_compact, compact):
        info["detail"] = "Clearly states MN maximum = 6"
        return 35, info

    if _any(mid_pats, text):
        info["detail"] = "States MN = 6 but does not label it as maximum"
        return 30, info

    if _any(low_pats, text):
        info["detail"] = "Vaguely mentions maximum is 6"
        return 25, info

    if re.search(r"(?<!\d)6(?!\d)", text):
        info["detail"] = "Number 6 appears in text but not associated with MN maximum"
        return 10, info

    info["detail"] = "MN maximum not provided (should be 6)"
    return 0, info


# -- III. Radius Relationship (25 pts) ----------------------------------
#
# Correct answer: |MN|_max = 2R  (R = small circle radius = 3, max chord = diameter)
# Scoring tiers:
#   25  — Clearly states 2R / 2r_B
#   20  — Expresses "diameter" relationship but doesn't write 2R
#    5  — Mentions radius but relationship unclear
#    0  — Not provided

def _score_radius_relation(text: str) -> Tuple[int, dict]:
    info: dict = {}
    if not text.strip():
        info["detail"] = "No content"
        return 0, info

    compact = re.sub(r"\s+", "", text)

    # Explicit 2R
    r2_pats = [
        r"[|｜]?MN[|｜]?_?\{?(?:max|\\max)\}?\s*=\s*2\s*[·*×]?\s*[Rr]",
        r"MN[^\n]{0,50}(?:最大值|max)\s*(?:=|为|是|等于|：|:)\s*2\s*[·*×]?\s*[Rr]",
        r"(?:最大值|max)\s*(?:=|为|是|等于|：|:)\s*2\s*[·*×]?\s*[Rr]",
        r"2\s*[·*×]?\s*[Rr]_?[BbAa]",
    ]
    r2_compact = [
        r"2[·*]?[Rr]_?[BbAa]?",
    ]

    # Diameter
    diam_pats = [
        r"(?:等于|为|是|equals?|is)\s*(?:小圆|⊙B|⊙b|the small circle)?\s*(?:的|'s)?\s*(?:直径|diameter)",
        r"(?:最大|max).*?(?:弦|chord).*?(?:直径|diameter)",
        r"(?:最大值|maximum)\s*(?:恒)?(?:为|等于|=|is|equals?)\s*(?:小圆|the small circle)?\s*(?:直径|diameter)",
        r"(?:等于|是|为|equals?|is)\s*(?:该圆|小圆|the circle|the small circle)?\s*(?:的|'s)?\s*(?:一条)?(?:直径|diameter)",
        r"diameter",
    ]

    def _any(pats: list, target: str) -> bool:
        return any(re.search(p, target, re.IGNORECASE) for p in pats)

    if _any(r2_pats, text) or _any(r2_compact, compact):
        info["detail"] = "Clearly states |MN|_max = 2R"
        return 25, info

    if _any(diam_pats, text):
        info["detail"] = "Expresses diameter relationship but not in 2R form"
        return 20, info

    if re.search(r"(?:半径|radius|[Rr]\s*=)", text):
        info["detail"] = "Mentions radius but relationship unclear"
        return 5, info

    info["detail"] = "Radius relationship not provided"
    return 0, info


# -- IV. Derivation Quality (30 pts) — LLM-as-Judge ---------------------

_REASONING_PROMPT = """\
You are a rigorous mathematics evaluation expert. Please evaluate the derivation quality \
of the following student's solution to a geometry optimization problem.

**Problem Overview**:
Two circles, circle_A (large) and circle_B (small), intersect at C and D. CD is the common chord.
E, C, B, D, N are on circle_A (B, the center of the small circle, lies on the large circle).
H, C, D, M are on circle_B. D lies on segment MN. F is the intersection of CD and EH.
EH is a common tangent of the two circles. CH is perpendicular to CD. EF = sqrt(2).
Find the maximum value of |MN| and its relationship with the radius.

**Reference Answer**:
- |MN|_max = 6
- |MN|_max = 2R (R = small circle radius = 3, maximum chord = diameter)
- Key derivation path: use equal tangent lengths, power of a point theorem, \
and the CH perpendicular to CD condition to derive the small circle radius R = 3.

**Student's Solution**:
{answer_text}

Please score on the following three sub-dimensions (integers) and provide brief justifications:

**A. Derivation Logic** (0-12 pts)
  10-12: Complete derivation, rigorous steps, clear logic
  7-9:   Derivation mostly correct but has gaps or lacks rigor
  4-6:   Partially correct derivation but incoherent logic
  0-3:   Almost no valid derivation or fundamental errors

**B. Mathematical Tools Usage** (0-10 pts)
  8-10: Correctly uses power of a point theorem, tangent properties, perpendicularity conditions, etc.
  5-7:  Uses some relevant tools
  2-4:  Mentions but does not correctly use
  0-1:  Does not use any relevant tools

**C. Expression Clarity** (0-8 pts)
  7-8: Proper notation, clear steps, explicit conclusions
  4-6: Mostly readable but some unclear expressions
  0-3: Confusing or overly brief expressions

Please reply strictly in the following JSON format (do not include any other content):
```json
{{
  "logic": {{"score": 0, "reason": ""}},
  "math_tools": {{"score": 0, "reason": ""}},
  "clarity": {{"score": 0, "reason": ""}},
  "total": 0,
  "comment": ""
}}
```"""


def _fallback_reasoning(text: str) -> int:
    """Heuristic scoring when LLM is unavailable, capped at 15/30."""
    score = 0
    n = len(text.strip())
    if n > 500:
        score += 5
    elif n > 200:
        score += 3
    elif n > 50:
        score += 1

    terms = [
        r"幂定理|幂|power",
        r"切线|tangent",
        r"垂直|perpendicular|⊥",
        r"直径|diameter",
        r"半径|radius",
        r"公共弦|公弦|common chord",
        r"圆心|center",
        r"(?:设|令|因为|所以|由此|therefore|since|let|because|hence)",
    ]
    cnt = sum(1 for p in terms if re.search(p, text, re.IGNORECASE))
    if cnt >= 6:
        score += 7
    elif cnt >= 4:
        score += 5
    elif cnt >= 2:
        score += 3

    if re.search(r"[=≈].*\d", text):
        score += 3

    return min(score, 15)


def _score_reasoning(text: str, answer_dir: str) -> Tuple[int, dict]:
    info: dict = {}
    if not text.strip():
        info["detail"] = "No content"
        return 0, info

    config = _get_text_eval_config(answer_dir)
    snippet = text[:3000]
    raw = _call_llm_judge(
        _REASONING_PROMPT.format(answer_text=snippet), config
    )

    if not raw:
        sc = _fallback_reasoning(text)
        info["detail"] = f"LLM unavailable, heuristic evaluation (capped at 15)"
        info["score_breakdown"] = f"{sc}/30"
        return sc, info

    try:
        cleaned = raw
        if "```json" in cleaned:
            cleaned = cleaned.split("```json")[1].split("```")[0].strip()
        elif "```" in cleaned:
            cleaned = cleaned.split("```")[1].split("```")[0].strip()
        result = json.loads(cleaned)

        s_logic = max(0, min(12, int(result.get("logic", {}).get("score", 0))))
        s_tools = max(0, min(10, int(result.get("math_tools", {}).get("score", 0))))
        s_clear = max(0, min(8, int(result.get("clarity", {}).get("score", 0))))
        total = s_logic + s_tools + s_clear

        info["Derivation logic (12)"] = f"{s_logic} — {result.get('logic', {}).get('reason', '')}"
        info["Math tools (10)"] = f"{s_tools} — {result.get('math_tools', {}).get('reason', '')}"
        info["Expression clarity (8)"] = f"{s_clear} — {result.get('clarity', {}).get('reason', '')}"
        info["Overall comment"] = result.get("comment", "")
        return total, info
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"[RUBRIC] LLM parse error: {exc}")
        sc = _fallback_reasoning(text)
        info["detail"] = f"LLM response parse failed, heuristic evaluation"
        return sc, info


# -- evaluate / print_report --------------------------------------------

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Evaluate the agent's output.

    Args:
        answer_dir: Absolute path to the agent's output directory

    Returns:
        (score, report)  score in [0, 100], report contains per-dimension details
    """
    report: Dict[str, Any] = {}
    total = 0

    # I. File Delivery (10)
    s1, d1 = _score_file_delivery(answer_dir)
    total += s1
    report["I. File Delivery (10 pts)"] = {"score": s1, "detail": d1}

    if s1 == 0:
        report["II. MN Maximum (35 pts)"] = {"score": 0, "detail": {"detail": "No answer file"}}
        report["III. Radius Relationship (25 pts)"] = {"score": 0, "detail": {"detail": "No answer file"}}
        report["IV. Derivation Quality (30 pts)"] = {"score": 0, "detail": {"detail": "No answer file"}}
        return 0, report

    files = _find_answer_files(answer_dir)
    text = _read_text(files)

    # II. MN Maximum (35)
    s2, d2 = _score_max_value(text)
    total += s2
    report["II. MN Maximum (35 pts)"] = {"score": s2, "detail": d2}

    # III. Radius Relationship (25)
    s3, d3 = _score_radius_relation(text)
    total += s3
    report["III. Radius Relationship (25 pts)"] = {"score": s3, "detail": d3}

    # IV. Derivation Quality (30)
    s4, d4 = _score_reasoning(text, answer_dir)
    total += s4
    report["IV. Derivation Quality (30 pts)"] = {"score": s4, "detail": d4}

    total = max(0, min(100, total))
    return int(total), report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print a formatted scoring report."""
    print("=" * 60)
    print("Geometry Optimization — Scoring Report")
    print("Task: Find the Maximum Value of MN and Its Relation to the Radius")
    print("=" * 60)
    print(f"\nTotal Score: {score}/100\n")

    for section, data in report.items():
        pts = data.get("score", 0)
        print(f"{'─' * 50}")
        print(f"[{section}] Score: {pts}")
        for k, v in data.get("detail", {}).items():
            print(f"  {k}: {v}")

    print(f"\n{'=' * 60}")
    if score >= 90:
        print("Comment: Excellent! Correct answer with complete derivation.")
    elif score >= 70:
        print("Comment: Good. Answer mostly correct; some dimensions can be improved.")
    elif score >= 50:
        print("Comment: Passing. Core answer partially correct but has gaps.")
    elif score >= 30:
        print("Comment: Partially complete. Key answers missing or incorrect.")
    else:
        print("Comment: Incomplete. Answer file missing or seriously insufficient content.")
    print("=" * 60)


# -- CLI -----------------------------------------------------------------

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        test_dir = sys.argv[1]
    else:
        test_dir = os.path.join(
            os.path.dirname(__file__), "..", "gpt-5", "attempt_1"
        )

    if not os.path.isabs(test_dir):
        test_dir = os.path.join(os.getcwd(), test_dir)

    if os.path.isdir(test_dir):
        print(f"Evaluation directory: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"Directory not found: {test_dir}")
    sys.exit(0)
