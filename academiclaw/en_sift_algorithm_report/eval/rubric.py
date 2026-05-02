"""
Rubric — SIFT Algorithm Research Report Writing

The agent should produce answer.md: a rigorously structured SIFT algorithm research report
that combines theoretical depth with practical guidance.

Total: 100 points

Scoring Dimensions:
I. File Delivery (10 points)
  - answer.md exists, is readable, non-empty, and of reasonable length

II. Format & Structure (15 points)
  - Markdown section structure (6 points)
  - Document length (5 points)
  - Contains math formulas/expressions (4 points)

III. Content Completeness — LLM-as-Judge (45 points)
  - Section 1: Core Algorithm Principles and Mathematical Foundations (9 points)
  - Section 2: Key Implementation Details (9 points)
  - Section 3: Feature Matching and Robust Estimation (9 points)
  - Section 4: Algorithm Performance Evaluation (9 points)
  - Section 5: Improved/Alternative Algorithm Comparison (9 points)

IV. Content Quality — LLM-as-Judge (30 points)
  - Theoretical depth and accuracy (15 points)
  - Practical guidance and reproducibility (15 points)
"""

import os
import re
import json
import traceback
from typing import Tuple, Dict, Any

try:
    import openai
except ImportError:
    openai = None


# ---------------------------------------------------------------------------
# Environment & LLM Tools
# ---------------------------------------------------------------------------

def _load_env(answer_dir: str) -> dict:
    """Load .env from answer_dir and query root directory"""
    values: Dict[str, str] = {}
    query_root = os.path.join(os.path.dirname(__file__), "..")
    for d in [answer_dir, query_root]:
        env_path = os.path.join(d, ".env")
        if not os.path.exists(env_path):
            continue
        try:
            with open(env_path, "r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    k, v = k.strip(), v.strip().strip("'\"")
                    if k not in values:
                        values[k] = v
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
    except Exception as exc:
        print(f"[RUBRIC] LLM Judge call failed: {exc}")
        traceback.print_exc()
        return ""


def _parse_json_from_llm(raw: str) -> dict:
    if not raw:
        return {}
    text = raw
    if "```json" in text:
        text = text.split("```json", 1)[1].split("```", 1)[0].strip()
    elif "```" in text:
        text = text.split("```", 1)[1].split("```", 1)[0].strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r"\{[\s\S]*\}", text)
        if m:
            try:
                return json.loads(m.group())
            except json.JSONDecodeError:
                pass
    print(f"[RUBRIC] JSON parsing failed: {raw[:300]}")
    return {}


# ---------------------------------------------------------------------------
# Read answer.md
# ---------------------------------------------------------------------------

def _read_answer(answer_dir: str) -> str:
    for sub in ["answer.md", os.path.join("workspace", "answer.md")]:
        p = os.path.join(answer_dir, sub)
        if os.path.isfile(p):
            try:
                with open(p, "r", encoding="utf-8", errors="replace") as fh:
                    return fh.read().strip()
            except Exception:
                pass
    return ""


# ---------------------------------------------------------------------------
# I. File Delivery (10 points)
# ---------------------------------------------------------------------------

def _check_file_delivery(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    details: Dict[str, Any] = {}

    # Search for answer.md
    for sub in ["answer.md", os.path.join("workspace", "answer.md")]:
        path = os.path.join(answer_dir, sub)
        if os.path.isfile(path):
            break
    else:
        path = None

    if path is None:
        details["answer.md"] = "0/10 — File does not exist"
        return 0, details

    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            content = fh.read().strip()
    except Exception as exc:
        details["answer.md"] = f"0/10 — Read failed: {exc}"
        return 0, details

    if not content:
        details["answer.md"] = "0/10 — File is empty"
        return 0, details

    n = len(content)
    if n >= 2000:
        score = 10
    elif n >= 500:
        score = 6
    else:
        score = 3

    details["answer.md"] = f"{score}/10 — Exists and valid ({n} characters)"
    details["file_path"] = path
    details["char_count"] = n
    return score, details


# ---------------------------------------------------------------------------
# II. Format & Structure (15 points)
# ---------------------------------------------------------------------------

def _check_format(text: str) -> Tuple[int, Dict[str, Any]]:
    score = 0
    details: Dict[str, Any] = {}

    # 2.1 Markdown heading levels (6 points)
    headings = re.findall(r"^#{1,6}\s+.+$", text, re.MULTILINE)
    hcount = len(headings)
    if hcount >= 12:
        hs = 6
    elif hcount >= 8:
        hs = 4
    elif hcount >= 4:
        hs = 2
    elif hcount >= 1:
        hs = 1
    else:
        hs = 0
    score += hs
    details["section_heading_count"] = hcount
    details["section_structure"] = f"{hs}/6"

    # 2.2 Document total length (5 points)
    n = len(text)
    if n >= 6000:
        ls = 5
    elif n >= 4000:
        ls = 4
    elif n >= 2500:
        ls = 3
    elif n >= 1500:
        ls = 2
    else:
        ls = 1
    score += ls
    details["char_count"] = n
    details["length"] = f"{ls}/5"

    # 2.3 Math formulas / mathematical expressions (4 points)
    has_latex_inline = bool(re.search(r"\$[^$\n]{2,}\$", text))
    has_latex_block = bool(re.search(r"\$\$[\s\S]{2,}?\$\$", text))
    has_math_sym = bool(re.search(
        r"(?:\u03c3|\u2207|\u2202|\u03a3|\u03c0|\u03b5|\u03b1|\u03b2|\u2265|\u2264|\u2192|\u2190|\u21d2|\u2208|\u221a|\u221e|\u00b2|\u00b3|\u207b\u00b9|argmin|argmax)", text
    ))
    has_formula_kw = bool(re.search(
        r"(?:exp\s*\(|log\s*\(|sigma|nabla|partial|gradient|\u2207\u00b2|L\(x|G\(x|D\(x)",
        text, re.IGNORECASE,
    ))
    indicators = sum([has_latex_inline or has_latex_block, has_math_sym, has_formula_kw])
    if indicators >= 2:
        fs = 4
    elif indicators >= 1:
        fs = 2
    else:
        fs = 0
    score += fs
    details["has_latex_formula"] = has_latex_inline or has_latex_block
    details["has_math_symbols"] = has_math_sym
    details["formula"] = f"{fs}/4"

    return score, details


# ---------------------------------------------------------------------------
# III. Content Completeness — LLM-as-Judge (45 points)
# ---------------------------------------------------------------------------

_COMPLETENESS_PROMPT = """\
You are a strict computer vision expert evaluating the content completeness of a SIFT Algorithm Research Report.

The report should cover the following five sections. Please carefully read the report and score each section's coverage.

**Section 1: Core Algorithm Principles and Mathematical Foundations (0-9 points)**
Must include: scale-space theory, Gaussian function and Difference of Gaussians (DoG) approximation, LoG-DoG relationship, \
3D extrema detection, Taylor expansion for precise localization, Hessian matrix / curvature ratio edge suppression.
- 8-9: Comprehensive coverage with core formula derivations
- 5-7: Covers most points but missing some derivations
- 2-4: Only briefly mentioned, lacking mathematical detail
- 0-1: Not addressed or only one sentence

**Section 2: Key Implementation Details (0-9 points)**
Must include: scale-space construction (octave / layers / parameters), keypoint detection and precise localization, \
orientation assignment (36-bin histogram), 128-dimensional descriptor generation (4x4x8, trilinear interpolation, normalization and truncation).
- 8-9: Each step has clear parameter descriptions and implementation logic
- 5-7: Covers main steps but some details missing
- 2-4: Only outlines the process, lacks implementation-level detail
- 0-1: Not addressed

**Section 3: Feature Matching and Robust Estimation (0-9 points)**
Must include: distance metrics, Lowe ratio test, RANSAC (Random Sample Consensus), \
homography / fundamental matrix estimation.
- 8-9: Complete coverage of matching and robust estimation pipeline, with parameter discussion
- 5-7: Covers ratio test and RANSAC but insufficient detail
- 2-4: Only mentions matching concepts
- 0-1: Not addressed

**Section 4: Algorithm Performance Evaluation (0-9 points)**
Must include: scale invariance verification, rotation invariance verification, illumination robustness, noise/blur impact analysis; \
should have experimental design ideas or reproducible verification plans.
- 8-9: Systematic experimental design including evaluation metrics and verification plans
- 5-7: Discusses performance characteristics but experimental design is not specific enough
- 2-4: Only qualitative description, no experimental design
- 0-1: Not addressed

**Section 5: Improved/Alternative Algorithm Comparison (0-9 points)**
Must include: SIFT vs SURF comparison, SIFT vs ORB comparison; should discuss speed, accuracy, applicable scenarios, etc.
- 8-9: Detailed comparison of at least SURF and ORB, multi-dimensional analysis
- 5-7: Has comparison but dimensions are incomplete or analysis is shallow
- 2-4: Only lists algorithm names, lacks substantive comparison
- 0-1: Not addressed

Reply ONLY with valid JSON in the following format (no other content):
```json
{{
  "section1_math_foundation": {{"score": 0, "reason": ""}},
  "section2_implementation": {{"score": 0, "reason": ""}},
  "section3_matching_ransac": {{"score": 0, "reason": ""}},
  "section4_performance": {{"score": 0, "reason": ""}},
  "section5_comparison": {{"score": 0, "reason": ""}},
  "total": 0
}}
```

The report to evaluate follows:

---
{report_text}
---
"""


def _check_completeness_llm(text: str, config: dict) -> Tuple[int, Dict[str, Any]]:
    eval_text = text[:15000] if len(text) > 15000 else text
    prompt = _COMPLETENESS_PROMPT.format(report_text=eval_text)
    raw = _call_llm_judge(prompt, config)
    result = _parse_json_from_llm(raw)
    if not result:
        return _check_completeness_fallback(text)

    sections = [
        ("section1_math_foundation", "Section 1: Principles & Mathematical Foundations", 9),
        ("section2_implementation", "Section 2: Implementation Details", 9),
        ("section3_matching_ransac", "Section 3: Matching & Robust Estimation", 9),
        ("section4_performance", "Section 4: Performance Evaluation", 9),
        ("section5_comparison", "Section 5: Algorithm Comparison", 9),
    ]
    total = 0
    details: Dict[str, Any] = {}
    for key, label, mx in sections:
        sec = result.get(key, {})
        s = max(0, min(mx, int(sec.get("score", 0))))
        total += s
        details[label] = f"{s}/{mx} — {sec.get('reason', '')}"

    details["evaluation_method"] = "LLM-as-Judge"
    return total, details


def _check_completeness_fallback(text: str) -> Tuple[int, Dict[str, Any]]:
    """Keyword-based fallback evaluation (conservative, max ~30/45)"""
    t = text.lower()
    details: Dict[str, Any] = {}
    total = 0

    kw_map = {
        "Section 1: Principles & Mathematical Foundations": [
            "scale space", "dog", "difference of gaussian",
            "hessian", "curvature", "extrema", "octave", "laplacian", "log", "taylor",
            "nabla",
        ],
        "Section 2: Implementation Details": [
            "keypoint", "orientation", "descriptor",
            "128", "gradient", "histogram", "trilinear",
            "normalize",
        ],
        "Section 3: Matching & Robust Estimation": [
            "matching", "ratio test", "lowe", "ransac",
            "homography", "fundamental", "inlier",
        ],
        "Section 4: Performance Evaluation": [
            "invariance", "robust", "illumination",
            "noise", "blur", "rotation", "experiment", "evaluation",
        ],
        "Section 5: Algorithm Comparison": [
            "surf", "orb", "comparison", "speed",
            "real-time", "binary", "application",
        ],
    }
    for label, keywords in kw_map.items():
        hits = sum(1 for kw in keywords if kw.lower() in t)
        if hits >= 5:
            s = 6
        elif hits >= 3:
            s = 4
        elif hits >= 1:
            s = 2
        else:
            s = 0
        total += s
        details[label] = f"{s}/9 — {hits} keyword hits (fallback)"

    details["evaluation_method"] = "Keyword fallback (LLM unavailable)"
    return total, details


# ---------------------------------------------------------------------------
# IV. Content Quality — LLM-as-Judge (30 points)
# ---------------------------------------------------------------------------

_QUALITY_PROMPT = """\
You are a senior reviewer in the field of computer vision, evaluating the content quality of a SIFT Algorithm Research Report.

Please score strictly on the following two dimensions:

**Dimension A: Theoretical Depth and Accuracy (0-15 points)**
- Are mathematical formulas correct (Gaussian function, DoG, Hessian, Taylor expansion, etc.)?
- Are concept explanations accurate and error-free?
- Is there in-depth principle analysis rather than just surface-level coverage?
- Are key references or data sources cited?
- 13-15: Rigorous and accurate derivations, precise concepts, deep insights
- 9-12: Basically accurate, some depth but parts lack rigor
- 5-8: Notable errors or concept confusion, insufficient depth
- 0-4: Numerous errors or overly superficial

**Dimension B: Practical Guidance and Reproducibility (0-15 points)**
- Are specific parameter recommendations provided (e.g., sigma_0, number of octaves, ratio test threshold, etc.)?
- Are code snippets or pseudocode provided for comprehension?
- Are experimental designs specific and reproducible?
- Is there practical application guidance (e.g., image stitching, object detection scenarios)?
- 13-15: Detailed parameters, code examples, directly reproducible experimental plans
- 9-12: Some practical guidance but not specific enough
- 5-8: Leans theoretical, lacks practical details
- 0-4: Pure theoretical description, no practical guidance

Reply ONLY with valid JSON in the following format (no other content):
```json
{{
  "theory_depth": {{"score": 0, "reason": ""}},
  "practical_guidance": {{"score": 0, "reason": ""}},
  "total": 0
}}
```

The report to evaluate follows:

---
{report_text}
---
"""


def _check_quality_llm(text: str, config: dict) -> Tuple[int, Dict[str, Any]]:
    eval_text = text[:15000] if len(text) > 15000 else text
    prompt = _QUALITY_PROMPT.format(report_text=eval_text)
    raw = _call_llm_judge(prompt, config)
    result = _parse_json_from_llm(raw)
    if not result:
        return _check_quality_fallback(text)

    td = result.get("theory_depth", {})
    pg = result.get("practical_guidance", {})
    td_s = max(0, min(15, int(td.get("score", 0))))
    pg_s = max(0, min(15, int(pg.get("score", 0))))

    details: Dict[str, Any] = {
        "theoretical_depth_accuracy": f"{td_s}/15 — {td.get('reason', '')}",
        "practical_guidance_reproducibility": f"{pg_s}/15 — {pg.get('reason', '')}",
        "evaluation_method": "LLM-as-Judge",
    }
    return td_s + pg_s, details


def _check_quality_fallback(text: str) -> Tuple[int, Dict[str, Any]]:
    """Fallback quality evaluation (conservative, max ~18/30)"""
    t = text.lower()
    details: Dict[str, Any] = {}

    # Theoretical depth
    theory_hits = sum([
        bool(re.search(r"\$[^$]{2,}\$", text)),
        "derivation" in t,
        "proof" in t,
        bool(re.search(r"[\u03c3\u2207\u2202\u03a3\u03c0]", text)),
        "theorem" in t,
        "formula" in t or "equation" in t,
    ])
    if theory_hits >= 4:
        td_s = 9
    elif theory_hits >= 2:
        td_s = 6
    else:
        td_s = 3
    details["theoretical_depth_accuracy"] = f"{td_s}/15 — {theory_hits} theory indicators (fallback)"

    # Practical guidance
    prac_hits = sum([
        "```" in text,
        bool(re.search(r"(?:python|import|def |class )", t)),
        bool(re.search(r"\u03c3[\u2080 0]\s*[=\u2248]|sigma.*=|threshold", t)),
        "experiment" in t,
        "stitching" in t or "object detection" in t,
        "opencv" in t or "cv2" in t,
    ])
    if prac_hits >= 4:
        pg_s = 9
    elif prac_hits >= 2:
        pg_s = 6
    else:
        pg_s = 3
    details["practical_guidance_reproducibility"] = f"{pg_s}/15 — {prac_hits} practical indicators (fallback)"
    details["evaluation_method"] = "Fallback evaluation (LLM unavailable)"
    return td_s + pg_s, details


# ---------------------------------------------------------------------------
# Main Entry
# ---------------------------------------------------------------------------

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Evaluate the agent's output.

    Args:
        answer_dir: Absolute path to the agent's output directory

    Returns:
        (score, report)
        - score: integer from 0-100
        - report: dict containing detailed evaluation report
    """
    report: Dict[str, Any] = {}

    # I. File Delivery (10 points)
    s1, r1 = _check_file_delivery(answer_dir)
    report["I. File Delivery (10 pts)"] = {"score": s1, "details": r1}

    text = _read_answer(answer_dir)
    if not text:
        report["total_score"] = s1
        report["comment"] = "answer.md does not exist or is empty; content evaluation is not possible."
        return s1, report

    # II. Format & Structure (15 points)
    s2, r2 = _check_format(text)
    report["II. Format & Structure (15 pts)"] = {"score": s2, "details": r2}

    # LLM configuration
    config = _get_text_eval_config(answer_dir)

    # III. Content Completeness (45 points)
    s3, r3 = _check_completeness_llm(text, config)
    report["III. Content Completeness (45 pts)"] = {"score": s3, "details": r3}

    # IV. Content Quality (30 points)
    s4, r4 = _check_quality_llm(text, config)
    report["IV. Content Quality (30 pts)"] = {"score": s4, "details": r4}

    total = max(0, min(100, s1 + s2 + s3 + s4))

    report["total_score"] = total
    report["section_scores"] = {
        "File Delivery": f"{s1}/10",
        "Format & Structure": f"{s2}/15",
        "Content Completeness": f"{s3}/45",
        "Content Quality": f"{s4}/30",
    }

    if total >= 85:
        report["comment"] = "Excellent. Report is structurally complete, theoretically rigorous, and practically useful."
    elif total >= 70:
        report["comment"] = "Good. Covers most sections, but some dimensions have room for improvement."
    elif total >= 50:
        report["comment"] = "Passing. Main content is addressed, but depth or completeness is insufficient."
    elif total >= 30:
        report["comment"] = "Partially complete. Multiple sections are missing or content is too shallow."
    else:
        report["comment"] = "Failing. Report content is severely insufficient."

    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print formatted scoring report"""
    print("=" * 60)
    print("SIFT Algorithm Research Report — Scoring Report")
    print("=" * 60)
    print(f"\nTotal Score: {score}/100")

    scores = report.get("section_scores", {})
    if scores:
        print("\nSection Scores:")
        for k, v in scores.items():
            print(f"  {k}: {v}")

    for key in [
        "I. File Delivery (10 pts)",
        "II. Format & Structure (15 pts)",
        "III. Content Completeness (45 pts)",
        "IV. Content Quality (30 pts)",
    ]:
        sec = report.get(key, {})
        if not sec:
            continue
        print(f"\n{'─' * 50}")
        print(f"[{key}] {sec.get('score', 0)} pts")
        for dk, dv in sec.get("details", {}).items():
            print(f"  {dk}: {dv}")

    print(f"\n{'=' * 60}")
    print(f"Comment: {report.get('comment', '')}")
    print("=" * 60)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        test_dir = sys.argv[1]
    else:
        test_dir = os.path.join(os.path.dirname(__file__), "..", "gpt-5", "attempt_1")

    # Support relative paths
    if not os.path.isabs(test_dir):
        test_dir = os.path.join(
            os.path.dirname(__file__), "..", test_dir
        )
    test_dir = os.path.normpath(test_dir)

    if os.path.exists(test_dir):
        print(f"Evaluating directory: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"Directory does not exist: {test_dir}")
    sys.exit(0)
