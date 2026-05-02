"""
Rubric for CMO 2024 Problem 6 — Mathematical Proof

Task
----
Given real numbers a_1, ..., a_n satisfying  sum a_i = n,  sum a_i^2 = 2n,
sum a_i^3 = 3n.  Define width  Delta = max a_i - min a_i.

(1)  Find the largest constant C such that Delta >= C for all n >= 4.
     Answer: C = sqrt(5).   (9 raw points)

(2)  Prove there exists C_2 > 0 such that Delta >= C + C_2 * n^{-3/2}.
     (12 raw points)

Scoring: raw 0-21 normalised to 0-100.

Strategy
--------
1. File delivery checks (answer.md present, non-trivial).
2. Structure / format checks (has Part 1 & Part 2 sections, uses maths).
3. LLM-as-Judge with the official scoring rubric for fine-grained grading.
4. Rule-based keyword fallback when LLM is unavailable.
"""

import os
import sys
import json
import re
from typing import Tuple, Dict, Any

try:
    import openai
except ImportError:
    openai = None


# ============================================================================
# Environment & LLM helpers
# ============================================================================

def _load_env(answer_dir: str) -> dict:
    """Load .env from answer_dir and from the query root."""
    values: dict = {}
    query_root = os.path.join(os.path.dirname(__file__), "..")
    for env_dir in [answer_dir, query_root]:
        env_path = os.path.join(env_dir, ".env")
        if os.path.exists(env_path):
            try:
                with open(env_path, "r", encoding="utf-8") as fh:
                    for line in fh:
                        line = line.strip()
                        if not line or line.startswith("#") or "=" not in line:
                            continue
                        k, v = line.split("=", 1)
                        k = k.strip()
                        v = v.strip().strip("'\"")
                        if k not in values:
                            values[k] = v
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
    """Call LLM for text evaluation."""
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
        return ""


def _extract_json(text: str) -> dict:
    """Extract a JSON object from LLM response text."""
    if not text:
        return {}
    if "```json" in text:
        text = text.split("```json", 1)[1].split("```", 1)[0]
    elif "```" in text:
        text = text.split("```", 1)[1].split("```", 1)[0]
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r"\{[\s\S]*\}", text)
        if m:
            try:
                return json.loads(m.group(0))
            except json.JSONDecodeError:
                pass
    return {}


# ============================================================================
# LLM-as-Judge prompt  (mirrors the official scoring rubric)
# ============================================================================

_JUDGE_PROMPT = r"""You are a professional mathematical competition grading expert. Please strictly grade the given CMO 2024 Problem 6 solution according to the following official scoring rubric.

## Problem

Given real numbers a_1, a_2, ..., a_n satisfying:
  sum(a_i) = n,  sum(a_i^2) = 2n,  sum(a_i^3) = 3n.
Define width Delta = max a_i - min a_i.

(1) Find the largest constant C such that Delta >= C for all n >= 4.
(2) Prove there exists C_2 > 0 such that Delta >= C + C_2 * n^{-3/2}, where C is from part (1).

## Scoring Rubric

This problem is divided into parts (A) and (B), which are independent and scores can be added.

### Part (A): Complete part (1), prove C = sqrt(5) — Full marks 9 points

If this part's proof is fully completed (including constructing approximating examples and lower bound proof), award 9 points directly.

If not fully completed, score by the following sub-items:

**Stacking rule:** (A2), (A3), (A4) are mutually exclusive (take highest score), but (A1) can stack with (A2)/(A3)/(A4). Part A score = min(9, A1 + max(A2, A3, A4)).

(A1) Provide a concrete example or existence proof — 3 points
  - Give a two-point distribution construction (k values take A, n-k values take B), whose width can approach sqrt(5) arbitrarily closely
  - Must explicitly give parameters (proportion lambda_0 = (5-sqrt(5))/10 or similar expression), cannot just say "exists"
  - 3 pts: Complete construction with verification
  - 2 pts: Two-point distribution idea but incomplete parameters
  - 1 pt: Only mentions construction without details
  - 0 pts: Not addressed

(A2) Prove the maximum is >= (sqrt(5)+1)/2 — 3 points
  - Requires rigorous mathematical derivation, not just stating the conclusion
  - 3 pts: Complete correct proof; 1-2 pts: Partially correct; 0 pts: Not addressed

(A3) Prove the minimum is <= (1-sqrt(5))/2 — 3 points
  - Requires rigorous mathematical derivation, not just stating the conclusion
  - 3 pts: Complete correct proof; 1-2 pts: Partially correct; 0 pts: Not addressed

(A4) Prove the width is always >= C = sqrt(5) — 6 points
  - Typical method: Non-negative polynomial method — construct P_1(x)=(x-A)^2(B-x) and P_2(x)=(B-x)^2(x-A), sum over all x_i to get inequalities, derive u^2-u-1>=0 (u=-min x_i), thus u>=phi=(1+sqrt(5))/2, finally Delta>=sqrt(5)
  - 6 pts: Complete correct proof (including specific polynomial construction, expansion, derivation)
  - 4-5 pts: Main idea and key calculations present but not fully rigorous or missing one or two steps
  - 2-3 pts: Correct methodological approach but incomplete calculations
  - 1 pt: Only mentions method name (e.g. "non-negative polynomial method") without substantial derivation
  - 0 pts: Not addressed or proof direction is wrong

### Part (B): Complete part (2) — Full marks 12 points

If this part's proof is fully completed, award 12 points directly.

If not fully completed, score by the following sub-items:

**Stacking rule:** (B1), (B2), (B3) are mutually exclusive, take highest score.

(B1) For alpha in (1.5, 2], prove width > C + lambda/n^alpha — 6 points
  - Requires Diophantine approximation (lambda_0 is irrational, k/n cannot exactly equal lambda_0) and stability analysis
  - 6 pts: Complete correct proof; 3-5 pts: Main idea present; 1-2 pts: Partial approach; 0 pts: Not addressed

(B2) Give h(z) (auxiliary function) — 3 points
  - Give the correct auxiliary function expression
  - 3 pts: Correct; 1-2 pts: Partially correct; 0 pts: Not addressed

(B3) Prove ||z_1||^2 + ||z_2||^2 + ... + ||z_n||^2 >= c/n — 6 points
  - 6 pts: Complete correct proof; 3-5 pts: Main idea present; 1-2 pts: Partial approach; 0 pts: Not addressed

## Important Scoring Principles

1. **Rigor**: Mathematical proofs must be logically rigorous, critical steps cannot be missing
2. **Distinguish "framework descriptions" from "substantive derivations"**:
   - Merely describing a "methodological framework" in words (e.g. "can use non-negative polynomial method to reach contradiction") without specific formulas and calculations cannot earn high marks
   - Using "it can be verified", "it is easy to prove" to skip critical steps should result in significant deductions
3. **Calculation correctness**: Specific mathematical calculations (such as expanding polynomials, solving equations) must be correct
4. **Only stating C=sqrt(5) without complete proof**: At most 1 point in A4
5. **Part 2 only provides framework without substantive derivation**: At most 1 point each for B1/B2/B3

## Output Format

Please output strictly in the following JSON format (do not include other content):

```json
{
  "part_a": {
    "complete": false,
    "a1": 0,
    "a2": 0,
    "a3": 0,
    "a4": 0,
    "score": 0,
    "notes": ""
  },
  "part_b": {
    "complete": false,
    "b1": 0,
    "b2": 0,
    "b3": 0,
    "score": 0,
    "notes": ""
  },
  "total_raw": 0,
  "overall_feedback": ""
}
```

Field descriptions:
- part_a.complete: whether Part 1 is fully completed (if true, score is directly 9)
- a1/a2/a3/a4: sub-item scores (integers)
- part_a.score: per stacking rule min(9, A1 + max(A2,A3,A4))
- part_b.complete: whether Part 2 is fully completed (if true, score is directly 12)
- b1/b2/b3: sub-item scores (integers)
- part_b.score: max(B1,B2,B3), upper limit 12
- total_raw: part_a.score + part_b.score (0-21)
"""


# ============================================================================
# Apply scoring rules to parsed LLM output
# ============================================================================

def _apply_scoring_rules(parsed: dict) -> dict:
    """Validate ranges and enforce stacking rules on LLM-returned scores."""
    pa = parsed.get("part_a", {})
    pb = parsed.get("part_b", {})

    # Clamp individual items
    a1 = max(0, min(3, int(pa.get("a1", 0))))
    a2 = max(0, min(3, int(pa.get("a2", 0))))
    a3 = max(0, min(3, int(pa.get("a3", 0))))
    a4 = max(0, min(6, int(pa.get("a4", 0))))

    if pa.get("complete"):
        score_a = 9
    else:
        # A2/A3/A4 mutually exclusive; A1 stacks
        score_a = min(9, a1 + max(a2, a3, a4))

    b1 = max(0, min(6, int(pb.get("b1", 0))))
    b2 = max(0, min(3, int(pb.get("b2", 0))))
    b3 = max(0, min(6, int(pb.get("b3", 0))))

    if pb.get("complete"):
        score_b = 12
    else:
        # B1/B2/B3 mutually exclusive
        score_b = min(12, max(b1, b2, b3))

    total_raw = score_a + score_b

    return {
        "a1": a1, "a2": a2, "a3": a3, "a4": a4,
        "score_a": score_a,
        "b1": b1, "b2": b2, "b3": b3,
        "score_b": score_b,
        "total_raw": total_raw,
        "notes_a": pa.get("notes", ""),
        "notes_b": pb.get("notes", ""),
        "feedback": parsed.get("overall_feedback", ""),
    }


# ============================================================================
# Rule-based fallback  (conservative keyword scoring)
# ============================================================================

def _keyword_fallback(text: str) -> dict:
    """Conservative scoring when LLM is unavailable."""
    if not text or len(text.strip()) < 100:
        return {
            "a1": 0, "a2": 0, "a3": 0, "a4": 0, "score_a": 0,
            "b1": 0, "b2": 0, "b3": 0, "score_b": 0,
            "total_raw": 0,
            "notes_a": "Answer too short for meaningful evaluation",
            "notes_b": "",
            "feedback": "No meaningful mathematical content detected",
        }

    # Normalise for matching
    t = text

    # ---- Detect key mathematical content ----
    has_sqrt5 = any(k in t for k in [
        "sqrt(5)", "\\sqrt{5}", "\\sqrt5", "sqrt5",
    ])
    has_proof_words = any(k in t for k in [
        "prove", "proof", "therefore", "hence", "thus", "we get",
        "conclude", "it follows", "we have", "which gives",
        "Therefore", "Hence", "Thus", "Proof",
    ])

    # Part A indicators
    # A1: concrete construction / example
    example_kw = [
        "two-point distribution", "two point", "two-point",
        "construction", "concrete example", "explicit example",
        "lambda_0", "\\lambda_0",
        "(5-sqrt(5))/10", "(5-\\sqrt{5})/10",
        "k values", "n-k values",
    ]
    a1 = 0
    if any(k in t for k in example_kw):
        a1 = 2
        # Check for actual parameter detail
        if any(k in t for k in [
            "(5-sqrt(5))/10", "(5-\\sqrt{5})/10", "\\frac{5-\\sqrt{5}}{10}",
            "\\frac{5 - \\sqrt{5}}{10}", "5 - sqrt(5))/10",
        ]):
            a1 = 3
        elif "approach" in t.lower() or "converge" in t.lower():
            a1 = 2

    # A4: lower bound proof
    has_nonneg_poly = any(k in t for k in [
        "non-negative polynomial", "SOS", "P_1(x)", "P_2(x)", "P(x)",
        "(x-A)^2", "(x-A)", "(B-x)^2", "(B-x)",
        "(x - A)^2", "(B - x)^2",
        "\\left(x-A\\right)^2", "(x_i - A)^2(B - x_i)",
    ])
    has_golden = any(k in t for k in [
        "golden ratio", "phi", "\\varphi", "varphi",
        "(1+sqrt(5))/2", "(1+\\sqrt{5})/2", "\\frac{1+\\sqrt{5}}{2}",
        "\\frac{1 + \\sqrt{5}}{2}",
    ])
    has_quadratic_eq = any(k in t for k in [
        "u^2 - u - 1", "u^2-u-1",
        "5\\lambda^2 - 5\\lambda + 1", "5lambda^2-5lambda+1",
    ])

    a4 = 0
    if has_sqrt5 and has_proof_words:
        if has_nonneg_poly and has_golden and has_quadratic_eq:
            a4 = 5  # Near complete proof
        elif has_nonneg_poly and (has_golden or has_quadratic_eq):
            a4 = 4
        elif has_nonneg_poly:
            a4 = 3
        elif has_golden:
            a4 = 2
        else:
            a4 = 1  # Just mentions sqrt(5) but no real proof

    # A2/A3: endpoint bounds
    a2, a3 = 0, 0
    upper_endpoint_kw = [
        "(sqrt(5)+1)/2", "(\\sqrt{5}+1)/2", "\\frac{\\sqrt{5}+1}{2}",
        "\\frac{1+\\sqrt{5}}{2}",
    ]
    lower_endpoint_kw = [
        "(1-sqrt(5))/2", "(1-\\sqrt{5})/2",
        "\\frac{1-\\sqrt{5}}{2}", "\\frac{1 - \\sqrt{5}}{2}",
    ]
    if any(k in t for k in upper_endpoint_kw) and has_proof_words:
        a2 = 2
    if any(k in t for k in lower_endpoint_kw) and has_proof_words:
        a3 = 2

    score_a = min(9, a1 + max(a2, a3, a4))

    # ---- Part B ----
    has_part_b_section = any(k in t for k in [
        "Part 2", "Part B", "part (2)", "Part Two",
        "## Part 2", "higher-order", "Higher-order",
    ])
    has_diophantine = any(k in t for k in [
        "Diophantine", "irrational approximation", "Hurwitz",
        "continued fraction",
    ])
    has_discrete = any(k in t for k in [
        "discrete obstruction", "discrete barrier",
    ])
    has_n_power = any(k in t for k in [
        "n^{-3/2}", "n^(-3/2)", "n^{-\\alpha}", "n^{-alpha}",
        "n^{-2}", "n^(-2)",
    ])
    has_stability = any(k in t for k in [
        "stability", "perturbation",
    ])

    b1 = 0
    if has_part_b_section:
        if has_diophantine and has_n_power and has_stability:
            b1 = 3
        elif has_diophantine and has_n_power:
            b1 = 2
        elif has_discrete or has_n_power or has_diophantine:
            b1 = 1

    b2 = 0
    if "h(z)" in t or ("auxiliary function" in t and has_part_b_section):
        b2 = 1

    b3 = 0
    if any(k in t for k in ["||z", "\\|z"]):
        b3 = 1

    score_b = min(12, max(b1, b2, b3))
    total_raw = score_a + score_b

    return {
        "a1": a1, "a2": a2, "a3": a3, "a4": a4, "score_a": score_a,
        "b1": b1, "b2": b2, "b3": b3, "score_b": score_b,
        "total_raw": total_raw,
        "notes_a": "Rule-based fallback (conservative)",
        "notes_b": "Rule-based fallback (conservative)",
        "feedback": "LLM unavailable — scores are conservative keyword estimates",
    }


# ============================================================================
# Dimension 1: File delivery  (10 points)
# ============================================================================

def _check_delivery(answer_dir: str) -> Tuple[int, str, str]:
    """
    Check answer.md exists and has meaningful content.
    Returns (score_10, answer_text, file_path).
    """
    answer_path = os.path.join(answer_dir, "answer.md")

    # Fallback: look for other .md files
    if not os.path.exists(answer_path):
        try:
            for fname in sorted(os.listdir(answer_dir)):
                if fname.endswith(".md") and fname.lower() not in (
                    "query.md", "task_prompt.md", "readme.md",
                ):
                    answer_path = os.path.join(answer_dir, fname)
                    break
        except OSError:
            pass

    if not os.path.exists(answer_path):
        return 0, "", ""

    try:
        with open(answer_path, "r", encoding="utf-8") as fh:
            text = fh.read()
    except Exception:
        return 0, "", answer_path

    stripped = text.strip()
    if len(stripped) < 50:
        return 2, text, answer_path  # File exists but nearly empty

    # Check basic structure
    score = 5  # file exists and has content
    has_part1 = bool(re.search(r"Part\s*1|Part\s*A|part\s*[\(]1", text, re.IGNORECASE))
    has_part2 = bool(re.search(r"Part\s*2|Part\s*B|part\s*[\(]2", text, re.IGNORECASE))
    has_math = bool(re.search(r"\\[\(\[]|\\frac|\\sum|\\sqrt|\$.*\$", text))

    if has_part1 and has_part2:
        score += 3  # Both sections present
    elif has_part1 or has_part2:
        score += 1  # Only one section

    if has_math:
        score += 2  # Uses mathematical notation

    return min(10, score), text, answer_path


# ============================================================================
# Dimension 2: Mathematical content — LLM + fallback  (90 points)
# ============================================================================

def _evaluate_math_content(answer_text: str, answer_dir: str) -> Tuple[int, dict]:
    """
    Score mathematical proof quality.
    Raw 0-21 from rubric, scaled to 0-90.
    Returns (score_90, details_dict).
    """
    config = _get_text_eval_config(answer_dir)
    llm_used = False
    scores = {}

    if config.get("api_key") and config.get("api_base"):
        full_prompt = (
            _JUDGE_PROMPT
            + "\n\n---\n\n## Solution to be graded\n\n"
            + answer_text[:15000]  # cap to avoid token overflow
        )
        raw_response = _call_llm_judge(full_prompt, config)
        parsed = _extract_json(raw_response)

        if parsed and ("part_a" in parsed or "total_raw" in parsed):
            scores = _apply_scoring_rules(parsed)
            llm_used = True
            print(f"[RUBRIC] LLM evaluation successful (model: {config['model']})")
        else:
            print("[RUBRIC] LLM returned invalid/empty JSON, falling back to rules")

    if not llm_used:
        print("[RUBRIC] Using rule-based fallback evaluation")
        scores = _keyword_fallback(answer_text)

    # Scale raw 0-21 -> 0-90
    total_raw = scores["total_raw"]
    score_90 = round(total_raw / 21 * 90)
    score_90 = max(0, min(90, score_90))

    details = {
        "method": f"LLM ({config.get('model', '?')})" if llm_used else "Rule-based fallback",
        "raw_total": f"{total_raw}/21",
        "part_a": {
            "score": f"{scores['score_a']}/9",
            "A1_example": f"{scores['a1']}/3",
            "A2_max_bound": f"{scores['a2']}/3",
            "A3_min_bound": f"{scores['a3']}/3",
            "A4_width_proof": f"{scores['a4']}/6",
            "notes": scores.get("notes_a", ""),
        },
        "part_b": {
            "score": f"{scores['score_b']}/12",
            "B1_full_proof": f"{scores['b1']}/6",
            "B2_aux_func": f"{scores['b2']}/3",
            "B3_norm_bound": f"{scores['b3']}/6",
            "notes": scores.get("notes_b", ""),
        },
        "feedback": scores.get("feedback", ""),
    }

    return score_90, details


# ============================================================================
# Main evaluate()
# ============================================================================

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Evaluate agent output for CMO 2024 Problem 6.

    Args:
        answer_dir: absolute path to agent output directory

    Returns:
        (score, report) where score is 0-100
    """
    report: Dict[str, Any] = {
        "result_score": {"score": 0, "max": 100, "deductions": []},
        "process_score": {"score": 0, "max": 0, "deductions": []},
        "comment": "",
    }

    # ---- Dimension 1: File delivery (10 pts) ----
    delivery_score, answer_text, answer_path = _check_delivery(answer_dir)

    if delivery_score == 0:
        report["result_score"]["deductions"].append("No answer.md or any .md solution file found")
        report["comment"] = "No solution file submitted, score 0"
        return 0, report

    print(f"[RUBRIC] Answer file: {answer_path}  ({len(answer_text)} chars)")

    if len(answer_text.strip()) < 50:
        report["result_score"]["score"] = delivery_score
        report["result_score"]["deductions"].append("Solution content too short (< 50 characters)")
        report["comment"] = f"File exists but content too short, only file delivery score {delivery_score}/100"
        return delivery_score, report

    # ---- Dimension 2: Mathematical content (90 pts) ----
    math_score, math_details = _evaluate_math_content(answer_text, answer_dir)

    # ---- Combine ----
    total_score = min(100, delivery_score + math_score)

    # Build deductions list
    deductions = []
    if delivery_score < 10:
        deductions.append(f"File delivery: {delivery_score}/10 (format or structure incomplete)")
    if math_score < 90:
        deductions.append(f"Mathematical content: {math_score}/90 (raw score {math_details.get('raw_total', '?')})")

    report["result_score"]["score"] = total_score
    report["result_score"]["deductions"] = deductions
    report["result_score"]["details"] = {
        "file_delivery (10 pts)": f"{delivery_score}/10",
        "mathematical_content (90 pts)": math_details,
    }
    report["comment"] = (
        f"Total score {total_score}/100. "
        f"File delivery {delivery_score}/10, mathematical content {math_score}/90"
        f" (raw score {math_details.get('raw_total', '?')}). "
        f"Evaluation method: {math_details.get('method', 'unknown')}. "
        f" {math_details.get('feedback', '')}"
    )

    return total_score, report


# ============================================================================
# print_report()
# ============================================================================

def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print formatted evaluation report."""
    print("=" * 64)
    print("  CMO 2024 Problem 6 — Evaluation Report")
    print("=" * 64)
    print(f"\n  Final Score: {score}/100\n")

    details = report.get("result_score", {}).get("details", {})

    # File delivery
    fd = details.get("file_delivery (10 pts)", "N/A")
    print(f"  [1] File Delivery:  {fd}")

    # Math content
    mc = details.get("mathematical_content (90 pts)", {})
    if isinstance(mc, dict):
        print(f"\n  [2] Mathematical Content:")
        print(f"      Method:     {mc.get('method', 'N/A')}")
        print(f"      Raw Total:  {mc.get('raw_total', 'N/A')}")

        pa = mc.get("part_a", {})
        if isinstance(pa, dict):
            print(f"\n      --- Part A: Prove C = sqrt(5)  (score: {pa.get('score', '?')}) ---")
            print(f"        A1 Concrete example:    {pa.get('A1_example', '?')}")
            print(f"        A2 Max >= (sqrt(5)+1)/2: {pa.get('A2_max_bound', '?')}")
            print(f"        A3 Min <= (1-sqrt(5))/2: {pa.get('A3_min_bound', '?')}")
            print(f"        A4 Width >= sqrt(5):     {pa.get('A4_width_proof', '?')}")
            if pa.get("notes"):
                print(f"        Notes: {pa['notes']}")

        pb = mc.get("part_b", {})
        if isinstance(pb, dict):
            print(f"\n      --- Part B: Higher-order bound  (score: {pb.get('score', '?')}) ---")
            print(f"        B1 Full proof:           {pb.get('B1_full_proof', '?')}")
            print(f"        B2 Auxiliary function:    {pb.get('B2_aux_func', '?')}")
            print(f"        B3 Norm lower bound:     {pb.get('B3_norm_bound', '?')}")
            if pb.get("notes"):
                print(f"        Notes: {pb['notes']}")

        if mc.get("feedback"):
            print(f"\n      Feedback: {mc['feedback']}")

    # Deductions
    deds = report.get("result_score", {}).get("deductions", [])
    if deds:
        print(f"\n  Deductions:")
        for d in deds:
            print(f"    - {d}")

    # Overall comment
    comment = report.get("comment", "")
    if comment:
        print(f"\n  {comment}")

    print("=" * 64)


# ============================================================================
# CLI entry point
# ============================================================================

if __name__ == "__main__":
    test_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    if not os.path.isabs(test_dir):
        test_dir = os.path.join(os.path.dirname(__file__), "..", test_dir)
    test_dir = os.path.abspath(test_dir)

    if os.path.isdir(test_dir):
        print(f"Evaluating: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"Directory not found: {test_dir}")
        sys.exit(0)
