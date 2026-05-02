#!/usr/bin/env python3
"""
k-SAT Random Walk Algorithm Solutions — Evaluation Script
Task: answer/questions/xuankunyang-query4

Task Summary:
  The agent must solve 6 problems about extending the 2-SAT random walk
  algorithm to k-SAT. Output: an answer file in .md or .tex format
  containing complete solutions for Q1-Q6 with LaTeX formulas.

Scoring Dimensions (Total: 100):
  Dimension 1 — File Delivery and Format (10 pts)
      File exists, non-empty, sufficient length, uses LaTeX formulas
  Dimension 2 — Key Formula Detection (30 pts)
      Regex matching of core mathematical conclusions for 6 problems (5 pts each)
  Dimension 3 — Proof Depth and Logic (60 pts)
      LLM-as-Judge per-problem evaluation of derivation completeness and correctness
"""

import json
import os
import re
import sys
from typing import Any, Dict, List, Tuple

try:
    import openai
except ImportError:
    openai = None


# =====================================================================
# Environment / LLM Utilities
# =====================================================================

def _load_env(answer_dir: str) -> dict:
    """Load .env configuration from answer_dir and query root directory."""
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
                        k = k.strip()
                        if k not in values:
                            values[k] = v.strip().strip("'\"")
            except Exception:
                pass
    return values


def _get_text_eval_config(answer_dir: str) -> dict:
    """Get text evaluation LLM configuration."""
    env = _load_env(answer_dir)

    def g(key: str, default: str = "") -> str:
        return os.environ.get(key) or env.get(key) or default

    return {
        "api_key": g("EVAL_TEXT_API_KEY", g("ANTHROPIC_API_KEY")),
        "api_base": g("EVAL_TEXT_API_BASE_URL", g("ANTHROPIC_BASE_URL")),
        "model": g("EVAL_TEXT_MODEL", "openai/gpt-5.2"),
    }


def _call_llm_judge(prompt: str, config: dict) -> str:
    """Call the LLM for text evaluation."""
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
            max_tokens=4096,
            temperature=0,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        print(f"[RUBRIC] LLM Judge call failed: {e}")
        return ""


def _parse_json_from_llm(text: str) -> dict:
    """Extract JSON from LLM response text."""
    if not text:
        return {}
    cleaned = re.sub(r"```json\s*", "", text)
    cleaned = re.sub(r"```\s*$", "", cleaned).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass
    m = re.search(r"\{[\s\S]*\}", cleaned)
    if m:
        try:
            return json.loads(m.group(0))
        except json.JSONDecodeError:
            pass
    return {}


# =====================================================================
# Read Answer Files
# =====================================================================

_SKIP_NAMES = {
    "query.md", "TASK_PROMPT.md", "EVALUATION_FEEDBACK.txt",
    "README.md", "TASK_DESCRIPTION.md",
}


def _read_answer(answer_dir: str) -> str:
    """Read and concatenate all .md / .tex / .txt answer files in answer_dir."""
    parts: List[str] = []
    if not os.path.isdir(answer_dir):
        return ""
    for fname in sorted(os.listdir(answer_dir)):
        if fname in _SKIP_NAMES:
            continue
        if fname.endswith((".md", ".tex", ".txt")):
            fpath = os.path.join(answer_dir, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                if content.strip():
                    parts.append(content)
            except Exception:
                pass
    return "\n\n".join(parts)


# =====================================================================
# Dimension 1: File Delivery and Format (10 pts)
# =====================================================================

def _check_delivery(answer_dir: str, answer_text: str) -> Tuple[int, Dict[str, Any]]:
    detail: Dict[str, Any] = {}
    score = 0

    if not os.path.isdir(answer_dir):
        detail["error"] = "answer directory not found"
        return 0, detail

    # 1a. Answer file exists (3 pts)
    files = [
        f for f in os.listdir(answer_dir)
        if f.endswith((".md", ".tex", ".txt")) and f not in _SKIP_NAMES
    ]
    if not files:
        detail["files"] = "no answer files found (.md/.tex/.txt)"
        return 0, detail

    detail["files"] = files
    score += 3

    # 1b. Content length (4 pts)
    length = len(answer_text)
    if length >= 4000:
        score += 4
        detail["length"] = f"{length} chars (sufficient)"
    elif length >= 2000:
        score += 2
        detail["length"] = f"{length} chars (somewhat short)"
    elif length >= 500:
        score += 1
        detail["length"] = f"{length} chars (short)"
    else:
        detail["length"] = f"{length} chars (too short)"

    # 1c. LaTeX formula usage (3 pts)
    latex_hits = len(re.findall(
        r"\$[^$]+\$|\$\$[\s\S]+?\$\$|\\frac|\\mathbb|\\sqrt|\\binom|\\Pr|\\le\b|\\ge\b",
        answer_text,
    ))
    if latex_hits >= 15:
        score += 3
        detail["latex"] = f"detected {latex_hits} LaTeX formulas (good)"
    elif latex_hits >= 5:
        score += 2
        detail["latex"] = f"detected {latex_hits} LaTeX formulas (fair)"
    elif latex_hits >= 1:
        score += 1
        detail["latex"] = f"detected {latex_hits} LaTeX formulas (insufficient)"
    else:
        detail["latex"] = "no LaTeX formulas detected"

    return min(score, 10), detail


# =====================================================================
# Dimension 2: Key Formula Detection (30 pts, 5 pts per problem)
# =====================================================================

def _check_key_formulas(answer: str) -> Tuple[int, Dict[str, Any]]:
    score = 0
    detail: Dict[str, Any] = {}

    # --- Q1 (5 pts): Success probability >= 1 - (1/2)^50 i.e. 1 - 2^{-50} ---
    q1_patterns = [
        r"1\s*-\s*\(?1\s*/\s*2\)?\s*\^\s*\{?\s*50\s*\}?",
        r"1\s*-\s*2\s*\^\s*\{?\s*-\s*50\s*\}?",
        r"1\s*-\s*\\frac\s*\{1\}\s*\{2\s*\^\s*\{?\s*50\s*\}?\s*\}",
        r"1\s*-\s*\\left\s*\(\s*\\frac\s*\{1\}\s*\{2\}\s*\\right\s*\)\s*\^\s*\{?\s*50\s*\}?",
        r"2\s*\^\s*\{?\s*-\s*50\s*\}?",
    ]
    q1 = any(re.search(p, answer) for p in q1_patterns)
    if q1:
        score += 5
        detail["Q1_probability"] = "PASS (+5): contains 1-2^{-50} or equivalent form"
    else:
        detail["Q1_probability"] = "FAIL (0/5): 1-(1/2)^50 or equivalent form not detected"

    # --- Q2 (5 pts): Transition probabilities 1/k and (k-1)/k ---
    has_1k = bool(re.search(
        r"\\frac\s*\{1\}\s*\{k\}|\\tfrac\s*\{1\}\s*\{k\}|1\s*/\s*k|\bge\s*\\frac\{1\}\{k\}",
        answer,
    ))
    has_k1k = bool(re.search(
        r"\\frac\s*\{?\s*k\s*-\s*1\s*\}?\s*\{k\}|\\tfrac\s*\{k\s*-\s*1\}\s*\{k\}"
        r"|\(k\s*-\s*1\)\s*/\s*k|1\s*-\s*1\s*/\s*k|1\s*-\s*\\frac\s*\{1\}\s*\{k\}",
        answer,
    ))
    if has_1k and has_k1k:
        score += 5
        detail["Q2_transition"] = "PASS (+5): contains 1/k and (k-1)/k"
    elif has_1k or has_k1k:
        score += 2
        detail["Q2_transition"] = (
            f"PARTIAL (+2): 1/k={'Y' if has_1k else 'N'}, "
            f"(k-1)/k={'Y' if has_k1k else 'N'}"
        )
    else:
        detail["Q2_transition"] = "FAIL (0/5): transition probabilities not detected"

    # --- Q3 (5 pts): O((k-1)^n) ---
    q3_patterns = [
        r"O\s*\(\s*\(?\s*k\s*-\s*1\s*\)?\s*\^\s*\{?\s*n\s*\}?\s*\)",
        r"\(\s*k\s*-\s*1\s*\)\s*\^\s*\{?\s*n\s*\}?",
        r"\(k-1\)\^n",
    ]
    q3 = any(re.search(p, answer) for p in q3_patterns)
    if q3:
        score += 5
        detail["Q3_complexity"] = "PASS (+5): contains (k-1)^n expression"
    else:
        detail["Q3_complexity"] = "FAIL (0/5): (k-1)^n not detected"

    # --- Q4 (5 pts): C*(k-1)^{-i} / sqrt(i) ---
    has_k1_neg_i = bool(re.search(
        r"\(k\s*-\s*1\)\s*\^\s*\{?\s*-\s*i\s*\}?",
        answer,
    ))
    has_sqrt_i = bool(re.search(
        r"\\sqrt\s*\{?\s*i\s*\}?|1\s*/\s*\\sqrt\s*\{?\s*i\s*\}?|i\s*\^\s*\{?\s*-?\s*1\s*/\s*2\s*\}?",
        answer,
    ))
    if has_k1_neg_i and has_sqrt_i:
        score += 5
        detail["Q4_bound"] = "PASS (+5): contains C*(k-1)^{-i}/sqrt(i) form"
    elif has_k1_neg_i or has_sqrt_i:
        score += 2
        detail["Q4_bound"] = (
            f"PARTIAL (+2): (k-1)^{{-i}}={'Y' if has_k1_neg_i else 'N'}, "
            f"sqrt(i)={'Y' if has_sqrt_i else 'N'}"
        )
    else:
        detail["Q4_bound"] = "FAIL (0/5): Q4 core conclusion not detected"

    # --- Q5 (5 pts): Probability lower bound containing k/(2(k-1)) or equivalent (k/(2(k-1)))^n ---
    q5_patterns = [
        r"\\frac\s*\{k\}\s*\{2\s*\(?\s*k\s*-\s*1\s*\)?\s*\}",
        r"k\s*/\s*\(?\s*2\s*\(?\s*k\s*-\s*1\s*\)?\s*\)?",
        r"\\frac\s*\{k\}\s*\{2k\s*-\s*2\}",
    ]
    q5 = any(re.search(p, answer) for p in q5_patterns)
    if q5:
        score += 5
        detail["Q5_probability"] = "PASS (+5): contains k/(2(k-1)) probability lower bound"
    else:
        detail["Q5_probability"] = "FAIL (0/5): Q5 probability lower bound not detected"

    # --- Q6 (5 pts): c = 2(k-1)/k  or equivalent form  c = 2 - 2/k ---
    q6_patterns = [
        r"c\s*=\s*\\frac\s*\{2\s*\(?\s*k\s*-\s*1\s*\)?\s*\}\s*\{k\}",
        r"c\s*=\s*\\tfrac\s*\{2\s*\(?\s*k\s*-\s*1\s*\)?\s*\}\s*\{k\}",
        r"c\s*=\s*2\s*\(?\s*k\s*-\s*1\s*\)?\s*/\s*k",
        r"c\s*=\s*2\s*-\s*2\s*/\s*k",
        r"c\s*=\s*2\s*-\s*\\frac\s*\{2\}\s*\{k\}",
        r"c\s*=\s*\\frac\s*\{2\s*k\s*-\s*2\}\s*\{k\}",
    ]
    q6 = any(re.search(p, answer) for p in q6_patterns)
    if q6:
        score += 5
        detail["Q6_constant"] = "PASS (+5): contains c=2(k-1)/k or equivalent form"
    else:
        detail["Q6_constant"] = "FAIL (0/5): c=2(k-1)/k not detected"

    return min(score, 30), detail


# =====================================================================
# Dimension 3: LLM-as-Judge Proof Depth Evaluation (60 pts)
# =====================================================================

_JUDGE_PROMPT = """\
You are a senior teaching assistant for a theoretical computer science course, \
grading an assignment about extending the 2-SAT random walk algorithm to \
k-SAT (k>=3). Please strictly follow the scoring rubric below to grade the \
student's solution problem by problem.

### Scoring Rubric (out of 100)

**Q1 Probability Bound Calculation (10 pts)**
- (5 pts) Correctly explains that a single run of 2n^2 steps has success probability >=1/2 \
(using expected value <= n^2 + Markov's inequality).
- (5 pts) Correctly derives that after 50 independent repetitions, the success probability \
>= 1-(1/2)^50 = 1-2^{{-50}}.

**Q2 Transition Probability Proof (15 pts)**
- (5 pts) Explicitly states P[X_{{t+1}}=X_t+1 | sigma_t] >= 1/k.
- (5 pts) Explicitly states P[X_{{t+1}}=X_t-1 | sigma_t] <= (k-1)/k.
- (5 pts) The reasoning includes the key argument: all k literals in an unsatisfied clause \
are false under sigma_t, but at least one is true under the satisfying assignment sigma, \
so flipping that variable increases X_t by 1 with probability >= 1/k.

**Q3 Time Complexity Bound (15 pts)**
- (5 pts) Establishes a one-dimensional biased random walk model (right probability 1/k, \
left probability (k-1)/k).
- (5 pts) Uses gambler's ruin / hitting time analysis to derive the expectation.
- (5 pts) Arrives at the correct conclusion that starting from the farthest point X_0=0 \
requires O((k-1)^n) steps.

**Q4 Core Difficulty Proof (25 pts)**
- (5 pts) Following the hint, considers the event of exactly L=i/(k-2) left steps and \
R=(k-1)i/(k-2) right steps in T=ki/(k-2) steps.
- (5 pts) Correctly writes the probability of this event = C(T,L) * p^L * q^R, \
where p=(k-1)/k, q=1/k.
- (5 pts) Uses Stirling's approximation n! ~ sqrt(2*pi*n)*(n/e)^n to approximate \
binomial coefficients / factorials.
- (5 pts) Correctly computes the exponential part of p^L * q^R to obtain (k-1)^{{-i}}.
- (5 pts) Arrives at the final probability lower bound of the form C*(k-1)^{{-i}}/sqrt(i).

**Q5 Uniform Distribution Probability (15 pts)**
- (5 pts) Considers that when the initial assignment is uniformly random, X_0 ~ Bin(n, 1/2).
- (5 pts) Sums/integrates the Q4 result over the distribution of X_0 \
(main contribution comes from i near n/2).
- (5 pts) Derives a single-run success probability lower bound of approximately \
(C'/sqrt(n)) * (k/(2(k-1)))^n.

**Q6 Algorithm Design and Constant (20 pts)**
- (5 pts) Designs a restart strategy: multiple independent runs (each with uniform random \
initialization + 3n steps of random walk).
- (5 pts) Gives the correct number of repetitions m = O(sqrt(n) * (2(k-1)/k)^n) so that \
the total success probability >= 99%.
- (10 pts) Explicitly gives the minimal constant c = 2(k-1)/k (or equivalent form c=2-2/k), \
and explains that total running time is poly(|phi|) * c^n.

---

### Student's Solution

{answer}

---

### Grading Instructions
1. Check each problem item by item against the rubric. Mathematical formulas are acceptable \
as long as the meaning is correct (specific LaTeX formatting is not required).
2. If a problem is not answered at all, give 0 points for that problem.
3. If the derivation has obvious errors (e.g., wrong conclusion), give 0 for that rubric item.
4. For Q4 (bonus problem), if the student gives a correct proof via a different approach \
than the hint, award full credit.
5. Score strictly according to the rubric; do not award sympathy points.
6. Output only a single JSON object (do not include markdown code block markers):

{{"Q1": {{"score": <0-10>, "reason": "..."}}, \
"Q2": {{"score": <0-15>, "reason": "..."}}, \
"Q3": {{"score": <0-15>, "reason": "..."}}, \
"Q4": {{"score": <0-25>, "reason": "..."}}, \
"Q5": {{"score": <0-15>, "reason": "..."}}, \
"Q6": {{"score": <0-20>, "reason": "..."}}, \
"total": <0-100>, \
"summary": "..."}}
"""


def _llm_evaluation(answer: str, answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """Use LLM for comprehensive proof depth and logic evaluation, scaled to 60 pts."""
    config = _get_text_eval_config(answer_dir)
    prompt = _JUDGE_PROMPT.replace("{answer}", answer[:16000])
    raw = _call_llm_judge(prompt, config)
    result = _parse_json_from_llm(raw)

    if not result or "total" not in result:
        return _keyword_fallback(answer)

    llm_total = max(0, min(100, int(result.get("total", 0))))
    scaled = round(llm_total / 100 * 60)

    detail: Dict[str, Any] = {
        "llm_raw_score": llm_total,
        "scaled_score": scaled,
        "summary": result.get("summary", ""),
    }
    for q in ("Q1", "Q2", "Q3", "Q4", "Q5", "Q6"):
        if q in result and isinstance(result[q], dict):
            detail[q] = {
                "score": result[q].get("score", 0),
                "max": {"Q1": 10, "Q2": 15, "Q3": 15, "Q4": 25, "Q5": 15, "Q6": 20}[q],
                "reason": result[q].get("reason", ""),
            }

    return scaled, detail


def _keyword_fallback(answer: str) -> Tuple[int, Dict[str, Any]]:
    """Conservative keyword-based scoring when LLM is unavailable, capped at 30/60."""
    score = 0
    checks: List[str] = []
    lower = answer.lower()

    keyword_groups = [
        (["markov", "markov's inequality"], 4, "uses Markov's inequality"),
        (["unsatisfied", "not satisfied", "unsatisfied clause"], 3, "Q2: mentions unsatisfied clause"),
        (["random walk", "one-dimensional", "1-dimensional"], 3, "Q3: mentions random walk"),
        (["stirling", "n!"], 4, "Q4: mentions Stirling's approximation"),
        (["\\binom", "binomial", "binomial coefficient", "c(t,l)"], 3, "Q4: mentions binomial coefficient"),
        (["binomial distribution", "bin(n", "uniform random"], 3, "Q5: mentions initial distribution"),
        (["restart", "repeated", "multiple runs", "independent runs"], 3, "Q6: mentions restart strategy"),
        (["coupling"], 2, "mentions coupling method"),
        (["gambler's ruin", "gambler", "ruin"], 2, "mentions gambler's ruin problem"),
        (["2(k-1)/k", "2-2/k", "2(k-1)\\over k"], 3, "Q6: contains expression for constant c"),
    ]

    for keywords, pts, desc in keyword_groups:
        if any(kw in lower for kw in keywords):
            score += pts
            checks.append(f"{desc} (+{pts})")

    score = min(score, 30)
    return score, {"method": "keyword_fallback", "score": score, "checks": checks}


# =====================================================================
# Main Evaluation Entry
# =====================================================================

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Evaluate the agent's output.

    Args:
        answer_dir: absolute path to the agent's output directory
                    (e.g., /path/to/query/gpt-5/attempt_1)

    Returns:
        (score, report) — score: 0-100, report: dict
    """
    answer = _read_answer(answer_dir)

    if not answer.strip():
        return 0, {
            "error": "no answer files found or answer is empty",
            "dim1_delivery": {"score": 0, "max": 10},
            "dim2_formulas": {"score": 0, "max": 30},
            "dim3_llm": {"score": 0, "max": 60},
        }

    # Dimension 1: File Delivery and Format (10 pts)
    s1, d1 = _check_delivery(answer_dir, answer)

    # Dimension 2: Key Formula Detection (30 pts)
    s2, d2 = _check_key_formulas(answer)

    # Dimension 3: LLM Proof Depth Evaluation (60 pts)
    s3, d3 = _llm_evaluation(answer, answer_dir)

    total = max(0, min(100, s1 + s2 + s3))

    report = {
        "total": total,
        "dim1_delivery": {"score": s1, "max": 10, "detail": d1},
        "dim2_formulas": {"score": s2, "max": 30, "detail": d2},
        "dim3_llm": {"score": s3, "max": 60, "detail": d3},
    }
    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print a formatted evaluation report."""
    print("=" * 64)
    print("  k-SAT Random Walk Algorithm Solutions — Evaluation Report")
    print("=" * 64)

    if "error" in report:
        print(f"\n  Error: {report['error']}")
        print(f"  Total Score: {score}/100")
        print("=" * 64)
        return

    # --- Dimension 1 ---
    d1 = report.get("dim1_delivery", {})
    print(f"\n[Dimension 1] File Delivery and Format: {d1.get('score', 0)}/{d1.get('max', 10)}")
    for k, v in d1.get("detail", {}).items():
        print(f"  {k}: {v}")

    # --- Dimension 2 ---
    d2 = report.get("dim2_formulas", {})
    print(f"\n[Dimension 2] Key Formula Detection (regex): {d2.get('score', 0)}/{d2.get('max', 30)}")
    for k, v in d2.get("detail", {}).items():
        print(f"  {k}: {v}")

    # --- Dimension 3 ---
    d3 = report.get("dim3_llm", {})
    print(f"\n[Dimension 3] Proof Depth (LLM): {d3.get('score', 0)}/{d3.get('max', 60)}")
    detail = d3.get("detail", {})
    if isinstance(detail, dict):
        if detail.get("method") == "keyword_fallback":
            print("  (LLM unavailable, using keyword fallback scoring)")
            for chk in detail.get("checks", []):
                print(f"    - {chk}")
        else:
            if "llm_raw_score" in detail:
                print(
                    f"  LLM raw score: {detail['llm_raw_score']}/100 "
                    f"-> scaled: {detail.get('scaled_score', 0)}/60"
                )
            if detail.get("summary"):
                print(f"  Comment: {detail['summary']}")
            for q in ("Q1", "Q2", "Q3", "Q4", "Q5", "Q6"):
                qi = detail.get(q)
                if qi and isinstance(qi, dict):
                    print(
                        f"    {q}: {qi.get('score', '?')}/{qi.get('max', '?')} "
                        f"— {qi.get('reason', '')}"
                    )

    print(f"\n{'=' * 64}")
    grade = "pass" if score >= 60 else "fail"
    print(f"  Total Score: {score}/100  ({grade})")
    print("=" * 64)


# =====================================================================
if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    if not os.path.isabs(target):
        target = os.path.join(os.path.dirname(os.path.dirname(__file__)), target)
    s, r = evaluate(target)
    print_report(s, r)
    sys.exit(0)
