"""
Alpha-Beta Pruning Search Implementation in Checkers Environment — Scoring Script
Task ID: write_code_junzhixue_query3

Total 100 points, divided into four scoring dimensions:

1. File Delivery & Basic Usability (15 points)
   - 1.1 agents.py exists and is non-empty (5)
   - 1.2 Python syntax is correct (5)
   - 1.3 File has substantive modifications (not the original template) (5)

2. Algorithm Implementation — Static Code Analysis (35 points)
   - 2.1 Minimax recursive search structure (10)
   - 2.2 Alpha-Beta pruning logic (10)
   - 2.3 Heuristic evaluation function (10)
   - 2.4 Search depth >= 3 (5)

3. Code Integration & Interface (20 points)
   - 3.1 Custom Policy subclass exists (5)
   - 3.2 compute_actions / compute_single_action interface (5)
   - 3.3 Uses environment API (Move, Direction, etc.) (5)
   - 3.4 Legal action traversal and optimal selection (5)

4. LLM-as-Judge Deep Code Review (30 points)
   - 4.1 Minimax logic completeness (10)
   - 4.2 Alpha-Beta pruning correctness (10)
   - 4.3 Heuristic function quality (10)
"""

import os
import re
import ast
import sys
import json
from typing import Tuple, Dict, Any, List, Optional

try:
    import openai
except ImportError:
    openai = None


# ============================================================================
# Environment / LLM Configuration
# ============================================================================

def _load_env(answer_dir: str) -> dict:
    """Load .env configuration from answer_dir and query root directory"""
    values: Dict[str, str] = {}
    for env_dir in [answer_dir, os.path.join(os.path.dirname(__file__), "..")]:
        env_path = os.path.join(env_dir, ".env")
        if os.path.exists(env_path):
            with open(env_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    if k.strip() not in values:
                        values[k.strip()] = v.strip().strip("'\"")
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


# ============================================================================
# Utility Functions
# ============================================================================

def _read_file(path: str) -> Optional[str]:
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except Exception:
        return None


def _find_classes(tree: ast.AST) -> List[ast.ClassDef]:
    return [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]


def _class_has_base(cls: ast.ClassDef, base_name: str) -> bool:
    for b in cls.bases:
        if isinstance(b, ast.Name) and b.id == base_name:
            return True
        if isinstance(b, ast.Attribute) and b.attr == base_name:
            return True
    return False


def _class_has_method(cls: ast.ClassDef, method_name: str) -> bool:
    return any(
        isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
        and item.name == method_name
        for item in cls.body
    )


def _get_non_baseline_policy_classes(classes: List[ast.ClassDef]) -> List[ast.ClassDef]:
    """Find non-Greedy/Random Policy subclasses or classes with minimax/alpha/beta naming"""
    baseline_keywords = {"greedy", "random", "chinesecheckers"}
    result: List[ast.ClassDef] = []
    for cls in classes:
        name_lower = cls.name.lower()
        if any(kw in name_lower for kw in baseline_keywords):
            continue
        if _class_has_base(cls, "Policy"):
            result.append(cls)
            continue
        if any(kw in name_lower for kw in ("minimax", "alpha", "beta", "ab", "search")):
            result.append(cls)
    return result


# ============================================================================
# 1. File Delivery & Basic Usability (15 points)
# ============================================================================

def _eval_file_delivery(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details: Dict[str, str] = {}

    agents_path = os.path.join(answer_dir, "agents.py")

    # 1.1 File exists and is non-empty (5 points)
    if not os.path.exists(agents_path):
        details["1.1 File exists"] = "0/5 — agents.py does not exist"
        return 0, details

    content = _read_file(agents_path)
    if not content or len(content.strip()) == 0:
        details["1.1 File exists"] = "0/5 — agents.py is empty"
        return 0, details

    score += 5
    details["1.1 File exists"] = f"5/5 — agents.py exists ({len(content)} bytes)"

    # 1.2 Syntax correct (5 points)
    try:
        ast.parse(content)
        score += 5
        details["1.2 Syntax correct"] = "5/5"
    except SyntaxError as e:
        details["1.2 Syntax correct"] = f"0/5 — Syntax error: {e.msg} (line {e.lineno})"
        return score, details

    # 1.3 Substantive modification (5 points)
    # Original template ~7900 bytes, has # TODO: Your Policy placeholder.
    # If agent made no modifications, file should be essentially the same as template.
    has_todo_placeholder = "# TODO: Your Policy" in content and content.strip().endswith("pass")
    file_size = len(content)

    if has_todo_placeholder and file_size < 9000:
        details["1.3 Substantive modification"] = "0/5 — File is essentially the same as original template, no substantive modifications"
    elif file_size > 5000:
        score += 5
        details["1.3 Substantive modification"] = f"5/5 — {file_size} bytes, has substantive content"
    elif file_size > 2000:
        score += 3
        details["1.3 Substantive modification"] = f"3/5 — {file_size} bytes, content is sparse"
    else:
        score += 1
        details["1.3 Substantive modification"] = f"1/5 — {file_size} bytes, content is too little"

    return score, details


# ============================================================================
# 2. Algorithm Implementation — Static Analysis (35 points)
# ============================================================================

def _eval_algorithm(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details: Dict[str, str] = {}

    content = _read_file(os.path.join(answer_dir, "agents.py"))
    if not content:
        details["error"] = "0/35 — Cannot read"
        return 0, details

    try:
        ast.parse(content)
    except SyntaxError:
        details["error"] = "0/35 — Syntax error"
        return 0, details

    lower = content.lower()

    # ------------------------------------------------------------------
    # 2.1 Minimax recursive search (10 points)
    # ------------------------------------------------------------------
    has_minimax_func = bool(re.search(r"def\s+\w*minimax\w*\s*\(", content, re.I))
    has_recursive_call = bool(re.search(
        r"(?:minimax|_minimax|alpha_beta|alphabeta|ab_search)\s*\(", content
    ))
    has_maxmin = (
        "maximizing" in lower
        or "is_max" in lower
        or "max_player" in lower
        or ("max(" in content and "min(" in content)
        or bool(re.search(r"float\(['\"](-?)inf['\"]\)", content))
    )
    has_depth_dec = bool(re.search(r"depth\s*-\s*1", content))

    if has_minimax_func and has_recursive_call and has_maxmin and has_depth_dec:
        s = 10
        details["2.1 Minimax recursion"] = "10/10 — Complete recursive search structure"
    elif has_minimax_func and has_recursive_call:
        s = 7
        details["2.1 Minimax recursion"] = "7/10 — Has function and recursive call but max/min or depth control incomplete"
    elif has_minimax_func or (has_maxmin and has_depth_dec):
        s = 4
        details["2.1 Minimax recursion"] = "4/10 — Partial structure present"
    else:
        s = 0
        details["2.1 Minimax recursion"] = "0/10 — No Minimax search found"
    score += s

    # ------------------------------------------------------------------
    # 2.2 Alpha-Beta pruning (10 points)
    # ------------------------------------------------------------------
    has_ab_params = bool(re.search(r"def\s+\w+\s*\([^)]*alpha[^)]*beta", content, re.I))
    has_ab_vars = "alpha" in content and "beta" in content
    has_pruning_cond = bool(re.search(r"beta\s*<=\s*alpha|alpha\s*>=\s*beta", content))
    has_alpha_upd = bool(re.search(r"alpha\s*=\s*max\s*\(", content))
    has_beta_upd = bool(re.search(r"beta\s*=\s*min\s*\(", content))

    if has_ab_params and has_pruning_cond and (has_alpha_upd or has_beta_upd):
        s = 10
        details["2.2 Alpha-Beta pruning"] = "10/10 — Complete pruning logic"
    elif has_ab_vars and has_pruning_cond:
        s = 7
        details["2.2 Alpha-Beta pruning"] = "7/10 — Has variables and pruning condition but updates incomplete"
    elif has_ab_vars and (has_alpha_upd or has_beta_upd):
        s = 5
        details["2.2 Alpha-Beta pruning"] = "5/10 — Has variables and updates but pruning condition unclear"
    elif has_ab_vars:
        s = 3
        details["2.2 Alpha-Beta pruning"] = "3/10 — Only alpha/beta variables present"
    else:
        s = 0
        details["2.2 Alpha-Beta pruning"] = "0/10 — No Alpha-Beta found"
    score += s

    # ------------------------------------------------------------------
    # 2.3 Heuristic evaluation function (10 points)
    # ------------------------------------------------------------------
    has_eval_func = bool(re.search(
        r"def\s+\w*(evaluat|heuristic|score_board|utility|estimate)\w*\s*\(", content, re.I
    ))
    has_distance = any(kw in lower for kw in ("distance", "hex_dist", "target", "goal"))
    has_piece_analysis = any(kw in lower for kw in ("pieces", "position", "board", "observation"))
    has_both_sides = (
        bool(re.search(r"(my|own|player|self).*(?:pieces|score|sum)", content, re.I))
        and bool(re.search(r"(opp|enemy|other|rival).*(?:pieces|score|sum)", content, re.I))
    )

    if has_eval_func and has_distance and has_both_sides:
        s = 10
        details["2.3 Heuristic function"] = "10/10 — Complete heuristic considering distance and both-side evaluation"
    elif has_eval_func and has_distance:
        s = 7
        details["2.3 Heuristic function"] = "7/10 — Has evaluation function and distance computation"
    elif has_eval_func or has_distance:
        s = 4
        details["2.3 Heuristic function"] = "4/10 — Partial evaluation logic"
    elif has_piece_analysis:
        s = 2
        details["2.3 Heuristic function"] = "2/10 — Has piece analysis but no explicit evaluation function"
    else:
        s = 0
        details["2.3 Heuristic function"] = "0/10 — No evaluation function found"
    score += s

    # ------------------------------------------------------------------
    # 2.4 Search depth >= 3 (5 points)
    # ------------------------------------------------------------------
    depth_vals: List[int] = []
    for pat in (r"depth\s*[=:]\s*(\d+)", r"max_depth\s*[=:]\s*(\d+)",
                r"search_depth\s*[=:]\s*(\d+)", r"self\.depth\s*=\s*(\d+)"):
        depth_vals.extend(int(m) for m in re.findall(pat, content))
    # Also check default parameter depth=N
    depth_vals.extend(int(m) for m in re.findall(r"depth\s*=\s*(\d+)", content))
    depth_vals = list(set(depth_vals))

    if depth_vals:
        max_d = max(depth_vals)
        if max_d >= 3:
            s = 5
            details["2.4 Search depth"] = f"5/5 — depth={max_d} (>=3)"
        elif max_d == 2:
            s = 3
            details["2.4 Search depth"] = f"3/5 — depth={max_d} (recommended >=3)"
        else:
            s = 1
            details["2.4 Search depth"] = f"1/5 — depth={max_d} (too shallow)"
    else:
        s = 0
        details["2.4 Search depth"] = "0/5 — No depth setting found"
    score += s

    return score, details


# ============================================================================
# 3. Code Integration & Interface (20 points)
# ============================================================================

def _eval_integration(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details: Dict[str, str] = {}

    content = _read_file(os.path.join(answer_dir, "agents.py"))
    if not content:
        details["error"] = "0/20 — Cannot read"
        return 0, details

    try:
        tree = ast.parse(content)
    except SyntaxError:
        details["error"] = "0/20 — Syntax error"
        return 0, details

    classes = _find_classes(tree)
    target_classes = _get_non_baseline_policy_classes(classes)

    # ------------------------------------------------------------------
    # 3.1 Custom Policy subclass (5 points)
    # ------------------------------------------------------------------
    if target_classes:
        names = [c.name for c in target_classes]
        has_policy_base = any(_class_has_base(c, "Policy") for c in target_classes)
        if has_policy_base:
            score += 5
            details["3.1 Policy subclass"] = f"5/5 — {', '.join(names)}"
        else:
            score += 3
            details["3.1 Policy subclass"] = f"3/5 — Class exists but does not inherit from Policy: {', '.join(names)}"
    else:
        details["3.1 Policy subclass"] = "0/5 — No custom policy class found"

    # ------------------------------------------------------------------
    # 3.2 Interface methods (5 points)
    # ------------------------------------------------------------------
    if target_classes:
        tc = target_classes[0]
        has_ca = _class_has_method(tc, "compute_actions")
        has_csa = _class_has_method(tc, "compute_single_action")
        if has_ca and has_csa:
            score += 5
            details["3.2 Interface methods"] = f"5/5 — {tc.name} has compute_actions + compute_single_action"
        elif has_ca:
            score += 3
            details["3.2 Interface methods"] = f"3/5 — Only compute_actions"
        elif has_csa:
            score += 2
            details["3.2 Interface methods"] = f"2/5 — Only compute_single_action"
        else:
            details["3.2 Interface methods"] = f"0/5 — {tc.name} missing interface methods"
    else:
        details["3.2 Interface methods"] = "0/5 — Target class not found"

    # ------------------------------------------------------------------
    # 3.3 Environment API usage (5 points)
    # ------------------------------------------------------------------
    has_move = "Move" in content
    has_direction = "Direction" in content
    has_position_or_encode = ("Position" in content
                              or bool(re.search(r"def\s+\w*action_to_move\w*", content)))
    count = sum([has_move, has_direction, has_position_or_encode])
    if count >= 3:
        score += 5
        details["3.3 Environment API"] = "5/5 — Move, Direction, Position/encoding all used"
    elif count >= 2:
        score += 3
        details["3.3 Environment API"] = f"3/5 — Partially used ({count}/3)"
    elif count >= 1:
        score += 2
        details["3.3 Environment API"] = f"2/5 — Minimal usage ({count}/3)"
    else:
        details["3.3 Environment API"] = "0/5 — Environment API not used"

    # ------------------------------------------------------------------
    # 3.4 Legal action traversal and optimal selection (5 points)
    # ------------------------------------------------------------------
    has_mask = "action_mask" in content
    has_iter = (
        bool(re.search(r"for\s+\w+\s+in\s+range\s*\(\s*self\.\w*action", content))
        or "legal_actions" in content.lower()
        or "valid_actions" in content.lower()
        or bool(re.search(r"mask\[.*\]\s*==\s*1", content))
        or bool(re.search(r"mask\[.*\]\s*!=\s*0", content))
    )
    has_best = any(kw in content for kw in ("best_action", "best_move", "best_value", "best_score"))

    if has_mask and has_iter and has_best:
        score += 5
        details["3.4 Action selection"] = "5/5 — Traverses legal actions and selects optimal"
    elif has_mask and has_best:
        score += 3
        details["3.4 Action selection"] = "3/5 — Has mask and optimal selection"
    elif has_best:
        score += 2
        details["3.4 Action selection"] = "2/5 — Has optimal selection but missing mask check"
    else:
        details["3.4 Action selection"] = "0/5 — No action traversal logic found"

    return score, details


# ============================================================================
# 4. LLM-as-Judge Deep Code Review (30 points)
# ============================================================================

_LLM_REVIEW_PROMPT = """\
You are an expert in artificial intelligence and game theory. Please review the following Python code, \
which should implement a Minimax search algorithm with Alpha-Beta pruning in a checkers (Chinese Checkers, \
triangle_size=2 simplified version) environment.

**Task Requirements**:
1. Implement the Minimax algorithm in agents.py, must include Alpha-Beta pruning
2. Design a custom heuristic evaluation function (e.g., considering total distance of pieces to the target area)
3. Search depth recommended >= 3
4. Code must be able to play against the built-in Greedy strategy

**Please score strictly on the following three dimensions (integers) with brief justification:**

Dimension 1: Minimax Logic Completeness (0-10)
  10: Complete Minimax recursive search, alternating max/min layers, correct depth control, reasonable termination conditions
  7-9: Basically complete, minor defects
  4-6: Has search structure but logic incomplete or with obvious errors
  0-3: Not implemented or serious errors

Dimension 2: Alpha-Beta Pruning Correctness (0-10)
  10: Pruning logic fully correct (initialization, updates, pruning conditions, propagation)
  7-9: Basically correct, possible minor boundary issues
  4-6: Has pruning code but logic has errors
  0-3: Not implemented or serious errors

Dimension 3: Heuristic Function Quality (0-10)
  10: High quality (considers piece-to-target distance, target occupation count, opponent analysis, etc.)
  7-9: Reasonable (at least considers distance, correct logic)
  4-6: Simple but effective
  0-3: No heuristic or logic errors

Please reply strictly in the following JSON format (no other content):
```json
{{
  "minimax_completeness": {{"score": 0, "reason": ""}},
  "alpha_beta_correctness": {{"score": 0, "reason": ""}},
  "heuristic_quality": {{"score": 0, "reason": ""}},
  "total": 0,
  "overall_comment": ""
}}
```

**Code to review**:
```python
{code}
```"""


def _eval_llm_review(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details: Dict[str, str] = {}

    content = _read_file(os.path.join(answer_dir, "agents.py"))
    if not content:
        details["error"] = "0/30 — Cannot read"
        return 0, details

    # Truncate to avoid excessive length
    code = content[:12000]
    if len(content) > 12000:
        code += "\n# ... (code truncated) ..."

    config = _get_text_eval_config(answer_dir)
    raw = _call_llm_judge(_LLM_REVIEW_PROMPT.format(code=code), config)

    if not raw:
        # LLM unavailable -> conservative scoring (based on static detection)
        has_mm = bool(re.search(r"def\s+\w*minimax", content, re.I))
        has_ab = ("alpha" in content and "beta" in content
                  and bool(re.search(r"beta\s*<=\s*alpha|alpha\s*>=\s*beta", content)))
        has_h = bool(re.search(r"def\s+\w*(evaluat|heuristic)", content, re.I))
        fb = (5 if has_mm else 0) + (5 if has_ab else 0) + (5 if has_h else 0)
        score = fb
        details["Fallback evaluation"] = f"{fb}/30 — LLM unavailable, conservative scoring based on static analysis"
        details["Detection"] = (
            f"Minimax={'Yes' if has_mm else 'No'}, "
            f"Alpha-Beta={'Yes' if has_ab else 'No'}, "
            f"Heuristic={'Yes' if has_h else 'No'}"
        )
        return score, details

    # Parse JSON
    try:
        text = raw
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        result = json.loads(text)
    except (json.JSONDecodeError, IndexError):
        print(f"[RUBRIC] LLM response parsing failed: {raw[:300]}")
        details["error"] = "LLM response format parsing failed"
        details["raw_response"] = raw[:500]
        return 10, details  # Conservative 10 points

    mc = result.get("minimax_completeness", {})
    ab = result.get("alpha_beta_correctness", {})
    hq = result.get("heuristic_quality", {})

    mc_s = max(0, min(10, int(mc.get("score", 0))))
    ab_s = max(0, min(10, int(ab.get("score", 0))))
    hq_s = max(0, min(10, int(hq.get("score", 0))))
    score = mc_s + ab_s + hq_s

    details["4.1 Minimax completeness"] = f"{mc_s}/10 — {mc.get('reason', '')}"
    details["4.2 Alpha-Beta correctness"] = f"{ab_s}/10 — {ab.get('reason', '')}"
    details["4.3 Heuristic function quality"] = f"{hq_s}/10 — {hq.get('reason', '')}"
    details["Overall comment"] = result.get("overall_comment", "")
    details["Evaluation model"] = config.get("model", "unknown")

    return score, details


# ============================================================================
# Main Entry Point
# ============================================================================

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Evaluate agent output.

    Args:
        answer_dir: Absolute path to the agent output directory

    Returns:
        (score, report)
        - score: Integer 0-100
        - report: dict containing detailed evaluation report
    """
    s1, r1 = _eval_file_delivery(answer_dir)
    s2, r2 = _eval_algorithm(answer_dir)
    s3, r3 = _eval_integration(answer_dir)
    s4, r4 = _eval_llm_review(answer_dir)

    total = min(100, s1 + s2 + s3 + s4)

    report: Dict[str, Any] = {
        "total_score": total,
        "dimension_scores": {
            "1. File Delivery (15)": s1,
            "2. Algorithm Implementation (35)": s2,
            "3. Code Integration (20)": s3,
            "4. LLM Review (30)": s4,
        },
        "detailed_report": {
            "1. File Delivery & Basic Usability": r1,
            "2. Algorithm Implementation — Static Analysis": r2,
            "3. Code Integration & Interface": r3,
            "4. LLM Deep Code Review": r4,
        },
    }

    if total >= 85:
        report["comment"] = "Excellent! Alpha-Beta Minimax implementation is complete with high code quality."
    elif total >= 70:
        report["comment"] = "Good. Core algorithm is correct, with room for improvement."
    elif total >= 50:
        report["comment"] = "Passing. Implemented partial functionality but with notable deficiencies."
    elif total >= 30:
        report["comment"] = "Failing. Key algorithms are missing or have serious errors."
    else:
        report["comment"] = "Incomplete. Core deliverables are missing or code is unusable."

    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print formatted scoring report"""
    print("=" * 70)
    print("Scoring Report: Alpha-Beta Pruning Search Implementation in Checkers Environment")
    print("=" * 70)
    print(f"\nTotal score: {score}/100")

    scores = report.get("dimension_scores", {})
    if scores:
        print("\nDimension scores:")
        for k, v in scores.items():
            print(f"  {k}: {v}")

    detail_sections = report.get("detailed_report", {})
    for section_name, section_data in detail_sections.items():
        print(f"\n{'─' * 55}")
        print(f"[{section_name}]")
        print(f"{'─' * 55}")
        if isinstance(section_data, dict):
            for k, v in section_data.items():
                if isinstance(v, dict):
                    print(f"  {k}:")
                    for kk, vv in v.items():
                        print(f"    {kk}: {vv}")
                else:
                    print(f"  {k}: {v}")
        else:
            print(f"  {section_data}")

    print(f"\n{'=' * 55}")
    print(f"Comment: {report.get('comment', '')}")
    print("=" * 70)


if __name__ == "__main__":
    test_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(__file__), "..", "gpt-5", "attempt_1"
    )
    if not os.path.isabs(test_dir):
        test_dir = os.path.join(os.path.dirname(__file__), "..", test_dir)
    test_dir = os.path.normpath(test_dir)

    if os.path.exists(test_dir):
        print(f"Evaluating directory: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"Directory does not exist: {test_dir}")
    sys.exit(0)
