"""
Rubric: SIFT Homework Report Scoring (Total 100 points)

Task: Based on hw_sift.pdf (homework requirements) and sift.py (existing framework code), write a
high-quality report report.md containing a Written Assignment (projective geometry theoretical proofs)
and a Programming Assignment (SIFT algorithm analysis + results presentation).

Scoring Dimensions (from description.json rubric.breakdown):
  1. Theoretical_Derivation  (40 points) — Projective geometry theoretical derivation
  2. Algorithm_Understanding  (35 points) — SIFT algorithm core principle analysis
  3. Report_Structure_Clarity  (15 points) — Report structure and formatting
  4. Completeness              (10 points) — Coverage completeness

Evaluation Strategy:
  - Deterministic checks: File existence, Markdown structure, key formula/terminology coverage
  - LLM-as-Judge: Theoretical derivation quality, algorithm understanding depth (parts requiring semantic judgment)
"""

from __future__ import annotations

import os
import re
import json
import sys
from typing import Tuple, Dict, Any, List

try:
    import openai
except ImportError:
    openai = None

# ---------------------------------------------------------------------------
# Environment / LLM Utilities
# ---------------------------------------------------------------------------

def _load_env(answer_dir: str) -> dict:
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
    def g(key, default=""):
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
        print(f"[RUBRIC] LLM Judge error: {e}")
        return ""


def _parse_json(raw: str) -> dict:
    if not raw:
        return {}
    try:
        if "```json" in raw:
            raw = raw.split("```json")[1].split("```")[0].strip()
        elif "```" in raw:
            raw = raw.split("```")[1].split("```")[0].strip()
        return json.loads(raw)
    except (json.JSONDecodeError, IndexError):
        print(f"[RUBRIC] LLM non-JSON response: {raw[:300]}")
        return {}


def _read_file(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


# ---------------------------------------------------------------------------
# 1. Theoretical_Derivation  (40 points)
#
#    Based on hw_sift.pdf Written Assignment:
#    (a) 15 points — Perspective projection model + circle projects as circle + standard equation
#    (b) 15 points — Vanishing point derivation for parallel lines on plane Ax+By+Cz+D=0
#                     + special case (y=0 plane, x=0 plane) verification
#    (c) 10 points — Prove vanishing points are collinear + vanishing line equation Ax_v+By_v+Cf=0
# ---------------------------------------------------------------------------

_THEORY_PROMPT = """\
You are a strict mathematics evaluation expert. Below is a theoretical proof report on projective \
geometry (Markdown). Please score each of the following three sub-problems according to the criteria.

**Sub-problem (a) — Maximum 15 points: Perspective projection model and circle projection**
- Establish the pinhole camera perspective projection model: from 3D point (X,Y,Z) to image plane (x,y,-f),
  giving formulas x=-fX/Z, y=-fY/Z
- Prove that when a circle lies on a plane Z=Z_0 parallel to the image plane, its projection is still a circle
- Derive the standard equation of the projected circle (x-x_c)^2+(y-y_c)^2=r^2, giving expressions for x_c, y_c, r
Scoring:
  13-15: Model complete, derivation logically rigorous, equations correct
  9-12:  Derivation basically correct but with minor flaws or skipped steps
  5-8:   Only conclusions given or missing key derivation steps
  0-4:   Missing or with major errors

**Sub-problem (b) — Maximum 15 points: Vanishing point derivation + special case verification**
- For parallel lines along direction (d_x,d_y,d_z) on plane Ax+By+Cz+D=0, derive vanishing point
  x_v=-f*d_x/d_z, y_v=-f*d_y/d_z
- Verify with special cases: discuss at least the y=0 plane (A=0,B=1,C=0) and x=0 plane (A=1,B=0,C=0)
  vanishing lines, checking formula correctness
Scoring:
  13-15: Derivation clear and complete, special case verification thorough (>=2 cases)
  9-12:  Derivation correct but verification only 1 case or not detailed enough
  5-8:   Derivation incomplete or with obvious omissions
  0-4:   Missing or serious errors

**Sub-problem (c) — Maximum 10 points: Vanishing points are collinear + vanishing line equation**
- Prove that vanishing points from different directions on the same plane are collinear
- Derive the vanishing line equation Ax_v + By_v + Cf = 0
Scoring:
  8-10: Proof rigorous, equation correct
  5-7:  Equation given but proof not complete enough
  2-4:  Only mentions the concept, no rigorous proof given
  0-1:  Missing or incorrect

Please reply strictly in the following JSON format, do not output anything else:
```json
{{
  "part_a": {{"score": 0, "reason": ""}},
  "part_b": {{"score": 0, "reason": ""}},
  "part_c": {{"score": 0, "reason": ""}},
  "total": 0
}}
```

Below is the report to evaluate (only the theory-related sections):

---
{text}
---
"""


def _deterministic_theory(text: str) -> Tuple[int, int, int]:
    """Deterministic baseline score based on keywords/formulas."""
    # (a) Projection model + circle equation
    has_proj = bool(re.search(
        r"x\s*=\s*-?\s*f.*X.*Z|x\s*=\s*-f\s*\\frac|"
        r"-f\\,\\frac\{X\}\{Z\}|"
        r"-f\s*X\s*/\s*Z",
        text
    ))
    has_circle_eq = bool(re.search(
        r"\(x\s*-\s*x_c\).*2.*\+.*\(y\s*-\s*y_c\).*2.*=.*r.*2|"
        r"x_c.*y_c.*r",
        text
    ))
    has_z_z0 = bool(re.search(r"Z\s*=\s*Z_0|Z\s*=\s*Z\u2080|Z\s*=\s*z_0", text))
    if has_proj and has_circle_eq and has_z_z0:
        base_a = 12
    elif has_proj and (has_circle_eq or has_z_z0):
        base_a = 8
    elif has_proj:
        base_a = 5
    else:
        base_a = 0

    # (b) Vanishing point + special cases
    has_vp_formula = bool(re.search(
        r"x_v\s*=\s*-\s*f|vanishing\s*point", text, re.I
    ))
    has_plane_eq = bool(re.search(
        r"A\s*[xX]\s*\+\s*B\s*[yY]\s*\+\s*C\s*[zZ]", text
    ))
    has_special_case = bool(re.search(
        r"[yY]\s*=\s*0|[xX]\s*=\s*0|B\s*=\s*1.*C\s*=\s*0|A\s*=\s*1.*C\s*=\s*0|"
        r"special\s*case|verification",
        text
    ))
    if has_vp_formula and has_plane_eq and has_special_case:
        base_b = 12
    elif has_vp_formula and has_plane_eq:
        base_b = 8
    elif has_vp_formula:
        base_b = 5
    else:
        base_b = 0

    # (c) Vanishing line
    has_vl = bool(re.search(
        r"A\s*x_v\s*\+\s*B\s*y_v\s*\+\s*C\s*f\s*=\s*0|"
        r"Ax.*By.*Cf.*=.*0|"
        r"vanishing\s*line",
        text, re.I
    ))
    has_collinear_proof = bool(re.search(
        r"collinear|colinear", text, re.I
    ))
    if has_vl and has_collinear_proof:
        base_c = 8
    elif has_vl:
        base_c = 5
    else:
        base_c = 0

    return base_a, base_b, base_c


def score_theory(text: str, config: dict) -> Tuple[int, Dict[str, Any]]:
    """Evaluate theoretical derivation (40 points)."""
    detail: Dict[str, Any] = {}
    base_a, base_b, base_c = _deterministic_theory(text)

    llm = {}
    if config.get("api_key"):
        # Take first 8000 characters to cover the theory section
        llm = _parse_json(_call_llm_judge(
            _THEORY_PROMPT.format(text=text[:8000]), config
        ))

    if llm:
        sa = max(0, min(15, int(llm.get("part_a", {}).get("score", base_a))))
        sb = max(0, min(15, int(llm.get("part_b", {}).get("score", base_b))))
        sc = max(0, min(10, int(llm.get("part_c", {}).get("score", base_c))))
        detail["(a) Projection model + circle equation [15]"] = f"{sa}/15 — {llm.get('part_a',{}).get('reason','')}"
        detail["(b) Vanishing point + special cases [15]"] = f"{sb}/15 — {llm.get('part_b',{}).get('reason','')}"
        detail["(c) Vanishing line equation [10]"] = f"{sc}/10 — {llm.get('part_c',{}).get('reason','')}"
        detail["method"] = "LLM-as-Judge"
    else:
        sa, sb, sc = base_a, base_b, base_c
        detail["(a) Projection model + circle equation [15]"] = f"{sa}/15 (keyword)"
        detail["(b) Vanishing point + special cases [15]"] = f"{sb}/15 (keyword)"
        detail["(c) Vanishing line equation [10]"] = f"{sc}/10 (keyword)"
        detail["method"] = "deterministic fallback"

    return sa + sb + sc, detail


# ---------------------------------------------------------------------------
# 2. Algorithm_Understanding  (35 points)
#
#    Programming Assignment experiment report:
#    (i)   DoG and LoG relationship + efficiency advantage     (10 points)
#    (ii)  Extrema detection + contrast threshold + Hessian suppression  (10 points)
#    (iii) Orientation assignment (histogram + smoothing + interpolation)  (8 points)
#    (iv)  128-D descriptor construction                        (7 points)
# ---------------------------------------------------------------------------

_ALGO_PROMPT = """\
You are a strict computer vision algorithm evaluation expert. Below is a SIFT algorithm programming \
experiment report (Markdown). Please score each of the following four dimensions.

**Dimension 1 — DoG and LoG (0-10 points)**
- Does it explain how DoG (Difference of Gaussians) approximates LoG (Laplacian of Gaussian)?
- Is there mathematical derivation (e.g., dG/d_sigma ~ sigma * nabla^2 G)?
- Does it explain the efficiency advantage (avoids second derivatives, only requires subtracting adjacent Gaussians)?
Scoring: 9-10 complete derivation + efficiency analysis; 6-8 explanation but not deep enough; 3-5 only mentions concept; 0-2 missing

**Dimension 2 — Extrema detection + contrast threshold + Hessian edge suppression (0-10 points)**
- 3x3x3 neighborhood extrema (26 neighbor comparison)
- Contrast threshold |D(x)| > threshold
- Hessian edge suppression: Tr(H)^2/Det(H) < (r+1)^2/r, Det(H)>0
Scoring: 9-10 all three comprehensive + with formulas; 6-8 basic coverage; 3-5 partial coverage; 0-2 missing

**Dimension 3 — Orientation assignment (0-8 points)**
- 36-bin orientation histogram + Gaussian weighting
- Histogram smoothing (circular averaging)
- Parabolic/quadratic interpolation for peak angle refinement
- Multi-peak detection (>=0.8*max -> additional orientations)
Scoring: 7-8 comprehensive; 5-6 basic coverage; 2-4 only briefly mentioned; 0-1 missing

**Dimension 4 — 128-D descriptor (0-7 points)**
- 16x16 region, 4x4 grid, 8-bin per cell -> 4x4x8=128 dimensions
- Rotation alignment (rotate gradient direction, not image)
- Trilinear interpolation (spatial + orientation)
- Normalization -> truncation at 0.2 -> renormalization
Scoring: 6-7 comprehensive; 4-5 basic coverage; 2-3 partial; 0-1 missing

Please reply strictly in the following JSON format:
```json
{{
  "dog_log": {{"score": 0, "reason": ""}},
  "extrema": {{"score": 0, "reason": ""}},
  "orientation": {{"score": 0, "reason": ""}},
  "descriptor": {{"score": 0, "reason": ""}},
  "total": 0
}}
```

Below is the report to evaluate (programming experiment section):

---
{text}
---
"""


def _deterministic_algo(text: str) -> Tuple[int, int, int, int]:
    """Keyword baseline."""
    t = text.lower()
    # DoG/LoG
    has_dog = bool(re.search(r"\bdog\b|difference\s*of\s*gaussian", t))
    has_log = bool(re.search(r"\blog\b|laplacian", t))
    has_efficiency = bool(re.search(r"efficient|only.*subtract|avoid.*second", t))
    d1 = 0
    if has_dog and has_log and has_efficiency:
        d1 = 8
    elif has_dog and has_log:
        d1 = 5
    elif has_dog:
        d1 = 3

    # extrema + contrast + hessian
    has_extrema = bool(re.search(r"3.*3.*3|extrema|26.*neighbor", t))
    has_contrast = bool(re.search(r"contrast.*thresh", t))
    has_hessian = bool(re.search(r"hessian|tr.*h.*det|edge.*suppress", t))
    d2 = min(10, (4 if has_extrema else 0) + (3 if has_contrast else 0) + (3 if has_hessian else 0))

    # orientation
    has_hist = bool(re.search(r"orientation.*histogram|36.*bin", t))
    has_smooth = bool(re.search(r"smooth", t))
    has_parabola = bool(re.search(r"parabolic|quadratic.*interpol", t))
    d3 = min(8, (3 if has_hist else 0) + (2 if has_smooth else 0) + (2 if has_parabola else 0))

    # descriptor
    has_128 = bool(re.search(r"128|4.*4.*8|16.*16", t))
    has_trilinear = bool(re.search(r"trilinear", t))
    has_norm = bool(re.search(r"normalize.*clamp|normalize.*truncat|l2.*0\.2|truncat.*0\.2", t))
    d4 = min(7, (3 if has_128 else 0) + (2 if has_trilinear else 0) + (2 if has_norm else 0))

    return d1, d2, d3, d4


def score_algorithm(text: str, config: dict) -> Tuple[int, Dict[str, Any]]:
    """Evaluate algorithm understanding (35 points)."""
    detail: Dict[str, Any] = {}
    b1, b2, b3, b4 = _deterministic_algo(text)

    llm = {}
    if config.get("api_key"):
        llm = _parse_json(_call_llm_judge(
            _ALGO_PROMPT.format(text=text[:8000]), config
        ))

    if llm:
        s1 = max(0, min(10, int(llm.get("dog_log", {}).get("score", b1))))
        s2 = max(0, min(10, int(llm.get("extrema", {}).get("score", b2))))
        s3 = max(0, min(8, int(llm.get("orientation", {}).get("score", b3))))
        s4 = max(0, min(7, int(llm.get("descriptor", {}).get("score", b4))))
        detail["DoG/LoG [10]"] = f"{s1}/10 — {llm.get('dog_log',{}).get('reason','')}"
        detail["Extrema+Contrast+Hessian [10]"] = f"{s2}/10 — {llm.get('extrema',{}).get('reason','')}"
        detail["Orientation assignment [8]"] = f"{s3}/8 — {llm.get('orientation',{}).get('reason','')}"
        detail["128-D descriptor [7]"] = f"{s4}/7 — {llm.get('descriptor',{}).get('reason','')}"
        detail["method"] = "LLM-as-Judge"
    else:
        s1, s2, s3, s4 = b1, b2, b3, b4
        detail["DoG/LoG [10]"] = f"{s1}/10 (keyword)"
        detail["Extrema+Contrast+Hessian [10]"] = f"{s2}/10 (keyword)"
        detail["Orientation assignment [8]"] = f"{s3}/8 (keyword)"
        detail["128-D descriptor [7]"] = f"{s4}/7 (keyword)"
        detail["method"] = "deterministic fallback"

    return s1 + s2 + s3 + s4, detail


# ---------------------------------------------------------------------------
# 3. Report_Structure_Clarity  (15 points)
#
#    (A) Markdown heading hierarchy               (4 points)
#    (B) Mathematical formula usage (LaTeX)        (5 points)
#    (C) Paragraph/list organization + code blocks (3 points)
#    (D) Image/visualization references            (3 points)
# ---------------------------------------------------------------------------

def score_structure(text: str, answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """Evaluate report structure (15 points)."""
    detail: Dict[str, Any] = {}

    # (A) Heading hierarchy: has h1/h2/h3 levels
    h1 = bool(re.search(r"^# ", text, re.M))
    h2 = bool(re.search(r"^## ", text, re.M))
    h3 = bool(re.search(r"^### ", text, re.M))
    n_headings = len(re.findall(r"^#{1,4} ", text, re.M))
    heading_levels = sum([h1, h2, h3])
    if heading_levels >= 3 and n_headings >= 5:
        sa = 4
    elif heading_levels >= 2 and n_headings >= 3:
        sa = 3
    elif heading_levels >= 1:
        sa = 1
    else:
        sa = 0
    detail["Heading hierarchy"] = f"{sa}/4 (levels={heading_levels}, count={n_headings})"

    # (B) Mathematical formulas
    inline_math = len(re.findall(r"(?<!\$)\$(?!\$)[^$]+\$(?!\$)", text))
    block_math = len(re.findall(r"\$\$", text)) // 2
    total_math = inline_math + block_math
    if block_math >= 3 and total_math >= 8:
        sb = 5
    elif block_math >= 1 and total_math >= 4:
        sb = 3
    elif total_math >= 1:
        sb = 1
    else:
        sb = 0
    detail["Math formulas"] = f"{sb}/5 (inline={inline_math}, block={block_math})"

    # (C) Lists/paragraphs/code blocks
    has_list = bool(re.search(r"^\s*[-*+]\s+|^\s*\d+\.\s", text, re.M))
    has_code = bool(re.search(r"```", text))
    char_count = len(text)
    sc = 0
    if has_list:
        sc += 1
    if has_code:
        sc += 1
    if char_count >= 3000:
        sc += 1
    sc = min(3, sc)
    detail["Lists/code/length"] = f"{sc}/3 (list={has_list}, code={has_code}, chars={char_count})"

    # (D) Image references + actual file existence
    img_refs = re.findall(r"!\[.*?\]\((.*?)\)", text)
    imgs_exist = 0
    for ref in img_refs:
        # Only check relative path images
        candidate = os.path.join(answer_dir, ref)
        if os.path.isfile(candidate):
            imgs_exist += 1
    if imgs_exist >= 2:
        sd = 3
    elif imgs_exist >= 1:
        sd = 2
    elif len(img_refs) >= 1:
        sd = 1  # Referenced but file doesn't exist
    else:
        sd = 0
    detail["Image references"] = f"{sd}/3 (refs={len(img_refs)}, exist={imgs_exist})"

    return sa + sb + sc + sd, detail


# ---------------------------------------------------------------------------
# 4. Completeness  (10 points)
#
#    (A) Written Assignment sub-problems (a)(b)(c) coverage  (5 points)
#    (B) Programming Assignment four major steps coverage     (5 points)
# ---------------------------------------------------------------------------

def score_completeness(text: str) -> Tuple[int, Dict[str, Any]]:
    """Evaluate coverage completeness (10 points)."""
    detail: Dict[str, Any] = {}
    t = text

    # Written Assignment three sub-problems
    pa = bool(re.search(r"\(a\)|circular.*disk|circle.*project", t, re.I))
    pb = bool(re.search(r"\(b\)|vanishing\s*point", t, re.I))
    pc = bool(re.search(r"\(c\)|vanishing\s*line", t, re.I))
    written_count = sum([pa, pb, pc])
    if written_count == 3:
        sw = 5
    elif written_count == 2:
        sw = 3
    elif written_count == 1:
        sw = 1
    else:
        sw = 0
    detail["Written Assignment coverage"] = f"{sw}/5 (a={pa}, b={pb}, c={pc})"

    # Programming Assignment four topics
    p_dog = bool(re.search(r"\bDoG\b|difference.*gaussian|gaussian\s*pyramid", t, re.I))
    p_kp = bool(re.search(r"keypoint|extrema", t, re.I))
    p_ori = bool(re.search(r"orientation|orientation.*histogram", t, re.I))
    p_desc = bool(re.search(r"descriptor|128", t, re.I))
    prog_count = sum([p_dog, p_kp, p_ori, p_desc])
    if prog_count >= 4:
        sp = 5
    elif prog_count == 3:
        sp = 4
    elif prog_count == 2:
        sp = 2
    elif prog_count == 1:
        sp = 1
    else:
        sp = 0
    detail["Programming Assignment coverage"] = f"{sp}/5 (DoG={p_dog}, kp={p_kp}, ori={p_ori}, desc={p_desc})"

    return sw + sp, detail


# ---------------------------------------------------------------------------
# Main Entry Point
# ---------------------------------------------------------------------------

REPORT_FILE = "report.md"


def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """Evaluate agent output.

    Args:
        answer_dir: Absolute path to the agent output directory

    Returns:
        (score, report) — score 0-100, report contains detailed information
    """
    md_path = os.path.join(answer_dir, REPORT_FILE)

    # File does not exist -> 0 points
    if not os.path.isfile(md_path):
        return 0, {
            "total_score": 0,
            "result_scores": {"basic": "report.md not found"},
            "process_scores": {},
            "deduction_reasons": ["Missing report file report.md"],
            "comment": "No report submitted, cannot evaluate.",
        }

    text = _read_file(md_path)
    if len(text.strip()) < 50:
        return 0, {
            "total_score": 0,
            "result_scores": {"basic": "report.md is empty or has very little content"},
            "process_scores": {},
            "deduction_reasons": ["report.md has insufficient content"],
            "comment": "Report is empty or has almost no content.",
        }

    config = _get_text_eval_config(answer_dir)

    s1, r1 = score_theory(text, config)
    s2, r2 = score_algorithm(text, config)
    s3, r3 = score_structure(text, answer_dir)
    s4, r4 = score_completeness(text)

    total = s1 + s2 + s3 + s4

    deductions: List[str] = []
    if s1 == 0:
        deductions.append("Theoretical derivation section completely missing")
    if s2 == 0:
        deductions.append("Algorithm understanding section completely missing")
    if len(text) < 800:
        deductions.append("Report is too short, content seriously insufficient")

    if total >= 90:
        comment = "Excellent: Theoretical derivation is complete and rigorous, algorithm analysis is deep and comprehensive, report structure is clear and well-formatted."
    elif total >= 75:
        comment = "Good: Covers the main content, some derivations or descriptions could be further improved."
    elif total >= 60:
        comment = "Passing: Covers most content, but some derivations are not deep enough or have gaps."
    elif total >= 40:
        comment = "Partially complete: Many key contents are missing, needs significant supplementation of theoretical proofs and algorithm analysis."
    else:
        comment = "Failing: Report content is seriously insufficient, needs comprehensive improvement."

    report: Dict[str, Any] = {
        "total_score": int(total),
        "result_scores": {
            "Theoretical_Derivation (40)": {"score": s1, "details": r1},
            "Algorithm_Understanding (35)": {"score": s2, "details": r2},
        },
        "process_scores": {
            "Report_Structure_Clarity (15)": {"score": s3, "details": r3},
            "Completeness (10)": {"score": s4, "details": r4},
        },
        "deduction_reasons": deductions,
        "comment": comment,
        "dimension_scores": {
            "Theoretical_Derivation": f"{s1}/40",
            "Algorithm_Understanding": f"{s2}/35",
            "Report_Structure_Clarity": f"{s3}/15",
            "Completeness": f"{s4}/10",
        },
    }

    return int(total), report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print formatted scoring report."""
    print("=" * 70)
    print("SIFT Homework Report Scoring")
    print("=" * 70)
    print(f"\nTotal score: {score}/100\n")

    scores = report.get("dimension_scores", {})
    if scores:
        print("Dimension scores:")
        for k, v in scores.items():
            print(f"  {k}: {v}")

    for section_key, label in [
        ("result_scores", "Result Scores (Theory + Algorithm)"),
        ("process_scores", "Process Scores (Structure + Completeness)"),
    ]:
        section = report.get(section_key, {})
        print(f"\n{'─' * 60}")
        print(f"  [{label}]")
        print(f"{'─' * 60}")
        for cat, cat_data in section.items():
            if isinstance(cat_data, dict):
                print(f"\n  {cat}: {cat_data.get('score', '?')} points")
                for k, v in cat_data.get("details", {}).items():
                    print(f"    {k}: {v}")
            else:
                print(f"  {cat}: {cat_data}")

    deductions = report.get("deduction_reasons", [])
    if deductions:
        print(f"\nDeduction reasons:")
        for i, r in enumerate(deductions, 1):
            print(f"  {i}. {r}")

    print(f"\nComment: {report.get('comment', '')}")
    print("=" * 70)


if __name__ == "__main__":
    test_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(__file__), "..", "gpt-5", "attempt_1"
    )
    if os.path.isdir(test_dir):
        print(f"Evaluating directory: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"Directory does not exist: {test_dir}")
    sys.exit(0)
