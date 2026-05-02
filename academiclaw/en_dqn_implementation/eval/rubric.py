"""
DQN and Double DQN Algorithm Implementation - Scoring Script

Task: Complete the TODOs in dqn_task.py, implement DQN and Double DQN algorithms,
      train in the MountainCar-v0 environment and return the reward list.

Total Score: 100 points

Scoring Dimensions:
1. File Delivery and Importability (10 points)
   - dqn_task.py exists (3 points)
   - Syntax correct, parseable by ast.parse (3 points)
   - QNetwork / ReplayBuffer / train_dqn all importable (4 points)

2. Code Structure Static Check (20 points)
   - QNetwork layers (5 points): nn.Linear x3 + ReLU + forward
   - ReplayBuffer push/sample (5 points): append + random.sample
   - epsilon-greedy action selection (5 points): epsilon + random check + env.sample + argmax
   - Double DQN branch logic (5 points): if double_dqn + argmax(dim=1) + gather

3. Dynamic Run - Functional Correctness (50 points)
   - DQN training runs and returns all_rewards list (10 points)
   - Double DQN training runs and returns all_rewards list (10 points)
   - DQN convergence (15 points): late reward significantly improved over early
   - DDQN convergence (15 points): late reward significantly improved over early

4. Code Quality - LLM Evaluation (20 points)
   - QNetwork implementation (5 points)
   - ReplayBuffer implementation (5 points)
   - Training logic (5 points)
   - Double DQN implementation (5 points)
"""

import os
import re
import sys
import ast
import json
import traceback
import numpy as np
from typing import Tuple, Dict, Any, List

try:
    import openai
except ImportError:
    openai = None


# ---------------------------------------------------------------------------
# Environment Configuration & LLM Utilities
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Dimension 1: File Delivery and Importability (10 points)
# ---------------------------------------------------------------------------

def _check_delivery(answer_dir: str) -> Tuple[int, Dict[str, str]]:
    score = 0
    details: Dict[str, str] = {}

    filepath = os.path.join(answer_dir, "dqn_task.py")

    # 1a. File exists (3 points)
    if not os.path.isfile(filepath):
        details["File exists"] = "0/3 - dqn_task.py does not exist"
        return 0, details
    score += 3
    details["File exists"] = "3/3"

    # 1b. Syntax correct (3 points)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
        ast.parse(source)
        score += 3
        details["Syntax check"] = "3/3"
    except SyntaxError as e:
        details["Syntax check"] = f"0/3 - {str(e)[:80]}"
        return score, details

    # 1c. Importable & core symbols exist (4 points)
    if answer_dir not in sys.path:
        sys.path.insert(0, answer_dir)
    try:
        if "dqn_task" in sys.modules:
            del sys.modules["dqn_task"]
        import dqn_task as _stu
        names = ["QNetwork", "ReplayBuffer", "train_dqn"]
        present = [n for n in names if hasattr(_stu, n)]
        missing = [n for n in names if n not in present]
        pts = min(4, len(present) * 2)  # 2 points each, max 4
        score += pts
        if missing:
            details["Importability"] = f"{pts}/4 - missing {', '.join(missing)}"
        else:
            details["Importability"] = "4/4"
    except Exception as e:
        details["Importability"] = f"0/4 - import failed: {str(e)[:100]}"

    return score, details


# ---------------------------------------------------------------------------
# Dimension 2: Code Structure Static Check (20 points)
# ---------------------------------------------------------------------------

def _check_static(answer_dir: str) -> Tuple[int, Dict[str, str]]:
    score = 0
    details: Dict[str, str] = {}
    filepath = os.path.join(answer_dir, "dqn_task.py")
    if not os.path.isfile(filepath):
        return 0, {"error": "file does not exist"}

    with open(filepath, "r", encoding="utf-8") as f:
        code = f.read()

    # 2a. QNetwork layers (5 points)
    has_linear = bool(re.search(r"nn\.Linear", code))
    has_relu = bool(re.search(r"(?:nn\.ReLU|torch\.relu|F\.relu|torch\.nn\.functional\.relu)", code, re.I))
    has_forward = bool(re.search(r"def\s+forward\s*\(", code))
    has_sequential = bool(re.search(r"nn\.Sequential", code))
    linear_count = len(re.findall(r"nn\.Linear", code))

    pts = 0
    if has_sequential and has_relu:
        pts = 5 if linear_count >= 3 else 4
    elif has_linear and has_relu and has_forward:
        pts = 5 if linear_count >= 3 else 3
    elif has_linear and has_forward:
        pts = 2
    details["2a_QNetwork"] = f"{pts}/5 - Linear x{linear_count}, ReLU={has_relu}, forward={has_forward}, Sequential={has_sequential}"
    score += pts

    # 2b. ReplayBuffer push / sample (5 points)
    has_push = bool(re.search(r"def\s+push\s*\(", code))
    has_sample = bool(re.search(r"def\s+sample\s*\(", code))
    has_append = bool(re.search(r"self\.buffer\.append", code))
    has_rand_sample = bool(re.search(r"random\.sample", code))

    pts = 0
    if has_push and has_append:
        pts += 2
    elif has_push:
        pts += 1
    if has_sample and has_rand_sample:
        pts += 3
    elif has_sample:
        pts += 1
    pts = min(5, pts)
    details["2b_ReplayBuffer"] = f"{pts}/5 - push={has_push and has_append}, sample={has_sample and has_rand_sample}"
    score += pts

    # 2c. epsilon-greedy action selection (5 points)
    has_eps = bool(re.search(r"epsilon|eps", code, re.I))
    has_rand_check = bool(re.search(r"random\.random\(\)\s*<", code))
    has_env_sample = bool(re.search(r"env\.action_space\.sample", code))
    has_argmax = bool(re.search(r"argmax|\.max\(", code))

    pts = 0
    if has_eps and has_rand_check:
        pts += 3
    elif has_eps:
        pts += 1
    if has_env_sample:
        pts += 1
    if has_argmax:
        pts += 1
    pts = min(5, pts)
    details["2c_EpsilonGreedy"] = f"{pts}/5 - eps={has_eps}, rand_check={has_rand_check}, sample={has_env_sample}, argmax={has_argmax}"
    score += pts

    # 2d. Double DQN logic (5 points)
    has_dbl_flag = bool(re.search(r"double_dqn", code))
    has_if_dbl = bool(re.search(r"if\s+double_dqn", code))
    has_argmax_d1 = bool(re.search(r"argmax.*dim=1|argmax\(.*1", code))
    has_gather = bool(re.search(r"\.gather\(", code))

    pts = 0
    if has_dbl_flag and has_if_dbl:
        pts += 2
    elif has_dbl_flag:
        pts += 1
    if has_argmax_d1 and has_gather:
        pts += 3
    elif has_gather:
        pts += 1
    pts = min(5, pts)
    details["2d_DoubleDQN"] = f"{pts}/5 - flag={has_dbl_flag}, if_branch={has_if_dbl}, argmax_d1={has_argmax_d1}, gather={has_gather}"
    score += pts

    return score, details


# ---------------------------------------------------------------------------
# Dimension 3: Dynamic Run - Functional Correctness (50 points)
# ---------------------------------------------------------------------------

def _check_dynamic(answer_dir: str) -> Tuple[int, Dict[str, str]]:
    score = 0
    details: Dict[str, str] = {}

    # Ensure path is in sys.path
    if answer_dir not in sys.path:
        sys.path.insert(0, answer_dir)

    try:
        if "dqn_task" in sys.modules:
            del sys.modules["dqn_task"]
        import dqn_task as stu
    except Exception as e:
        return 0, {"error": f"import failed: {str(e)[:120]}"}

    if not hasattr(stu, "train_dqn"):
        return 0, {"error": "missing train_dqn function"}

    try:
        import gymnasium as gym
    except ImportError:
        return 0, {"error": "gymnasium not installed"}

    # Limit episode count for faster evaluation
    orig_ep = getattr(stu, "NUM_EPISODES", 2000)
    eval_ep = min(orig_ep, 500)
    stu.NUM_EPISODES = eval_ep

    # --- 3a. DQN training (10 points) ---
    res_dqn = None
    try:
        env = gym.make("MountainCar-v0")
        print(f"[RUBRIC] Training DQN ({eval_ep} episodes) ...")
        res_dqn = stu.train_dqn(env, double_dqn=False)
        env.close()
        if isinstance(res_dqn, list) and len(res_dqn) > 0:
            score += 10
            details["3a_DQN_run"] = f"10/10 - returned {len(res_dqn)} rewards"
        else:
            details["3a_DQN_run"] = f"0/10 - return type: {type(res_dqn).__name__}"
            res_dqn = None
    except Exception as e:
        details["3a_DQN_run"] = f"0/10 - crashed: {str(e)[:120]}"
        traceback.print_exc()

    # --- 3b. Double DQN training (10 points) ---
    res_ddqn = None
    try:
        env = gym.make("MountainCar-v0")
        print(f"[RUBRIC] Training Double DQN ({eval_ep} episodes) ...")
        res_ddqn = stu.train_dqn(env, double_dqn=True)
        env.close()
        if isinstance(res_ddqn, list) and len(res_ddqn) > 0:
            score += 10
            details["3b_DDQN_run"] = f"10/10 - returned {len(res_ddqn)} rewards"
        else:
            details["3b_DDQN_run"] = f"0/10 - return type: {type(res_ddqn).__name__}"
            res_ddqn = None
    except Exception as e:
        details["3b_DDQN_run"] = f"0/10 - crashed: {str(e)[:120]}"
        traceback.print_exc()

    # Restore original episode count
    stu.NUM_EPISODES = orig_ep

    # --- Helper: convergence analysis ---
    def _convergence_score(rewards: List[float], max_pts: int, label: str) -> int:
        """Score based on reward improvement magnitude"""
        if not rewards or len(rewards) < 20:
            details[f"{label}_convergence"] = f"0/{max_pts} - insufficient episodes ({len(rewards) if rewards else 0})"
            return 0
        window = max(10, len(rewards) // 10)
        early = float(np.mean(rewards[:window]))
        late = float(np.mean(rewards[-window:]))
        improvement = late - early
        details[f"{label}_stats"] = f"early={early:.1f}, late={late:.1f}, improvement={improvement:.1f}"

        # MountainCar starts around -200, solved around -110
        if improvement >= 50:
            pts = max_pts
        elif improvement >= 30:
            pts = int(max_pts * 0.67)
        elif improvement >= 10:
            pts = int(max_pts * 0.33)
        elif late > -180:
            pts = int(max_pts * 0.2)
        else:
            pts = 0
        details[f"{label}_convergence"] = f"{pts}/{max_pts} - improvement {improvement:.1f}"
        return pts

    # --- 3c. DQN convergence (15 points) ---
    if res_dqn:
        score += _convergence_score(res_dqn, 15, "3c_DQN")
    else:
        details["3c_DQN_convergence"] = "0/15 - DQN did not run successfully"

    # --- 3d. DDQN convergence (15 points) ---
    if res_ddqn:
        score += _convergence_score(res_ddqn, 15, "3d_DDQN")
    else:
        details["3d_DDQN_convergence"] = "0/15 - DDQN did not run successfully"

    return score, details


# ---------------------------------------------------------------------------
# Dimension 4: Code Quality - LLM Evaluation (20 points)
# ---------------------------------------------------------------------------

_LLM_QUALITY_PROMPT = """\
You are a code review expert in the reinforcement learning field. Below is a student's submitted DQN / Double DQN implementation.
Please score strictly (integers) according to the following dimensions:

**Dimension A: QNetwork Implementation (0-5)**
- 5: Two hidden layers (64 units), ReLU activation, forward correct
- 3-4: Basically correct but minor issues (dimension mismatch, missing activation, etc.)
- 0-2: Obvious errors or not implemented

**Dimension B: ReplayBuffer Implementation (0-5)**
- 5: push correctly stores five-tuples, sample randomly samples returning numpy arrays
- 3-4: Basically correct but minor issues
- 0-2: Implementation errors or not implemented

**Dimension C: Training Logic (0-5)**
- 5: epsilon-greedy correct, target value computation correct, network update complete
- 3-4: Core logic correct but minor flaws
- 0-2: Training logic has obvious errors

**Dimension D: Double DQN Implementation (0-5)**
- 5: Correctly uses online_net argmax to select actions, target_net gather to get Q values, formula completely correct
- 3-4: Branch exists but has minor issues
- 0-2: Not correctly implemented or no difference from standard DQN

Reply strictly in the following JSON format (no other content):
```json
{{"a_qnetwork": {{"score": 0, "reason": ""}}, "b_replay_buffer": {{"score": 0, "reason": ""}}, "c_training": {{"score": 0, "reason": ""}}, "d_double_dqn": {{"score": 0, "reason": ""}}}}
```

Student code:
```python
{code}
```"""


def _check_quality(answer_dir: str) -> Tuple[int, Dict[str, str]]:
    score = 0
    details: Dict[str, str] = {}
    filepath = os.path.join(answer_dir, "dqn_task.py")
    if not os.path.isfile(filepath):
        return 0, {"error": "file does not exist"}

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            code = f.read()
    except Exception as e:
        return 0, {"error": f"read failed: {e}"}

    config = _get_text_eval_config(answer_dir)
    raw = _call_llm_judge(_LLM_QUALITY_PROMPT.format(code=code[:8000]), config)

    if not raw:
        details["LLM_unavailable"] = "conservative score 10/20"
        return 10, details

    try:
        text = raw
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        result = json.loads(text)
        a = max(0, min(5, int(result.get("a_qnetwork", {}).get("score", 0))))
        b = max(0, min(5, int(result.get("b_replay_buffer", {}).get("score", 0))))
        c = max(0, min(5, int(result.get("c_training", {}).get("score", 0))))
        d = max(0, min(5, int(result.get("d_double_dqn", {}).get("score", 0))))
        score = a + b + c + d
        details["4a_QNetwork"] = f"{a}/5 - {result.get('a_qnetwork', {}).get('reason', '')}"
        details["4b_ReplayBuffer"] = f"{b}/5 - {result.get('b_replay_buffer', {}).get('reason', '')}"
        details["4c_Training"] = f"{c}/5 - {result.get('c_training', {}).get('reason', '')}"
        details["4d_DoubleDQN"] = f"{d}/5 - {result.get('d_double_dqn', {}).get('reason', '')}"
    except Exception as e:
        print(f"[RUBRIC] LLM response parsing failed: {e}")
        print(f"[RUBRIC] Raw response: {raw[:300]}")
        details["LLM_parse_failed"] = f"conservative score 10/20 - {raw[:200]}"
        score = 10

    return score, details


# ---------------------------------------------------------------------------
# Entry Function
# ---------------------------------------------------------------------------

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Evaluate the agent's DQN implementation output.

    Args:
        answer_dir: Absolute path to the agent output directory

    Returns:
        (score, report) - score: 0-100 integer, report: detailed report dict
    """
    s1, r1 = _check_delivery(answer_dir)
    s2, r2 = _check_static(answer_dir)

    # Skip dynamic run and LLM if file delivery fails
    if s1 < 6:
        s3, r3 = 0, {"skipped": "File delivery did not pass, skipping dynamic run"}
        s4, r4 = 0, {"skipped": "File delivery did not pass, skipping LLM evaluation"}
    else:
        s3, r3 = _check_dynamic(answer_dir)
        s4, r4 = _check_quality(answer_dir)

    total = min(100, s1 + s2 + s3 + s4)

    report: Dict[str, Any] = {
        "total_score": total,
        "section_scores": {
            "1_file_delivery": f"{s1}/10",
            "2_code_structure": f"{s2}/20",
            "3_functional_correctness": f"{s3}/50",
            "4_code_quality": f"{s4}/20",
        },
        "details": {
            "1_file_delivery": r1,
            "2_code_structure": r2,
            "3_functional_correctness": r3,
            "4_code_quality": r4,
        },
    }
    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print formatted evaluation report"""
    print("=" * 60)
    print("DQN & Double DQN Implementation - Evaluation Report")
    print("=" * 60)
    print(f"\nTotal score: {score}/100\n")

    scores = report.get("section_scores", {})
    if scores:
        print("Section scores:")
        for k, v in scores.items():
            print(f"  {k}: {v}")

    for section, items in report.get("details", {}).items():
        print(f"\n{'─' * 50}")
        print(f"[{section}]")
        print(f"{'─' * 50}")
        if isinstance(items, dict):
            for k, v in items.items():
                print(f"  {k}: {v}")
        else:
            print(f"  {items}")

    print("\n" + "=" * 60)
    if score >= 80:
        print("Comment: Excellent! DQN and Double DQN implementation complete, algorithm converges well.")
    elif score >= 60:
        print("Comment: Good. Core functionality implemented but some dimensions have room for improvement.")
    elif score >= 40:
        print("Comment: Partially complete. Key modules missing or algorithm did not converge.")
    else:
        print("Comment: Failing. Implementation incomplete or unable to run.")
    print("=" * 60)


if __name__ == "__main__":
    test_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(__file__), "..", "gpt-5", "attempt_1")
    if os.path.exists(test_dir):
        print(f"Evaluating directory: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"Directory not found: {test_dir}")
    sys.exit(0)
