"""
Scoring Rubric — Double DQN-Based MountainCar Energy Hill-Climbing Optimization

Total: 100 points

Scoring Dimensions:
  1. File Delivery (10 pts)  — Does ddqn_main.py exist and is non-empty, does training_logs directory exist with data
  2. Code Quality (15 pts)  — Syntax correct, key library imports, neural network definition (with dual networks)
  3. DDQN Core Logic (30 pts) — Double DQN target computation, experience replay, epsilon-greedy, target network sync
  4. Training Log Quality (15 pts)  — loss/reward data volume and trend, test result records
  5. Performance Target (30 pts) — Test code, performance evidence (reward > -200), training convergence
"""

import ast
import csv
import json
import os
import re
import sys
from typing import Any, Dict, List, Tuple

try:
    import openai
except ImportError:
    openai = None


# ---------------------------------------------------------------------------
# Environment & LLM utility functions
# ---------------------------------------------------------------------------

def _load_env(answer_dir: str) -> dict:
    values: dict = {}
    for d in [answer_dir, os.path.join(os.path.dirname(__file__), "..")]:
        p = os.path.join(d, ".env")
        if not os.path.exists(p):
            continue
        try:
            with open(p, "r", encoding="utf-8") as fh:
                for raw in fh:
                    raw = raw.strip()
                    if not raw or raw.startswith("#") or "=" not in raw:
                        continue
                    k, v = raw.split("=", 1)
                    k, v = k.strip(), v.strip().strip("'\"")
                    if k not in values:
                        values[k] = v
        except Exception:
            pass
    return values


def _cfg(answer_dir: str) -> dict:
    env = _load_env(answer_dir)
    def g(key: str, fallback: str = "") -> str:
        return os.environ.get(key) or env.get(key) or fallback
    return {
        "api_key": g("EVAL_TEXT_API_KEY", g("ANTHROPIC_API_KEY")),
        "api_base": g("EVAL_TEXT_API_BASE_URL", g("ANTHROPIC_BASE_URL")),
        "model": g("EVAL_TEXT_MODEL", "openai/gpt-5.2"),
    }


def _llm(prompt: str, cfg: dict) -> str:
    if not openai or not cfg.get("api_key"):
        return ""
    try:
        base = cfg["api_base"].rstrip("/")
        if not base.endswith("/v1"):
            base += "/v1"
        client = openai.OpenAI(api_key=cfg["api_key"], base_url=base)
        resp = client.chat.completions.create(
            model=cfg["model"],
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2048,
            temperature=0,
        )
        return resp.choices[0].message.content.strip()
    except Exception as exc:
        print(f"[RUBRIC] LLM call failed: {exc}")
        return ""


def _json_from_llm(text: str) -> dict:
    if not text:
        return {}
    try:
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        return json.loads(text)
    except (json.JSONDecodeError, IndexError):
        return {}


# ---------------------------------------------------------------------------
# General utilities
# ---------------------------------------------------------------------------

def _read_file(path: str, limit: int = 0) -> str:
    if not os.path.isfile(path):
        return ""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            if limit > 0:
                return f.read(limit)
            return f.read()
    except Exception:
        return ""


def _find_main_py(answer_dir: str) -> str:
    """Return path to ddqn_main.py; if absent, return first .py with dqn; else empty string."""
    target = os.path.join(answer_dir, "ddqn_main.py")
    if os.path.isfile(target):
        return target
    for f in sorted(os.listdir(answer_dir)):
        if f.endswith(".py") and ("dqn" in f.lower() or "ddqn" in f.lower()):
            return os.path.join(answer_dir, f)
    for f in sorted(os.listdir(answer_dir)):
        if f.endswith(".py"):
            return os.path.join(answer_dir, f)
    return ""


def _find_log_dir(answer_dir: str) -> str:
    """Find training_logs or a subdirectory containing 'log'."""
    d = os.path.join(answer_dir, "training_logs")
    if os.path.isdir(d):
        return d
    for item in os.listdir(answer_dir):
        full = os.path.join(answer_dir, item)
        if os.path.isdir(full) and "log" in item.lower():
            return full
    return ""


def _csv_col(filepath: str, col: int = 1, max_rows: int = 10000) -> List[float]:
    """Read float values from a specific column of a CSV."""
    vals: List[float] = []
    if not os.path.isfile(filepath):
        return vals
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)  # skip header
            for i, row in enumerate(reader):
                if i >= max_rows:
                    break
                if len(row) > col:
                    try:
                        vals.append(float(row[col]))
                    except ValueError:
                        pass
    except Exception:
        pass
    return vals


# =========================================================================
# Dimension 1: File Delivery (10 pts)
# =========================================================================

def _dim1_file_delivery(answer_dir: str) -> Tuple[int, dict]:
    pts = 0
    info: dict = {}

    # 1a. ddqn_main.py (5 pts)
    main_path = os.path.join(answer_dir, "ddqn_main.py")
    if os.path.isfile(main_path):
        sz = os.path.getsize(main_path)
        if sz >= 500:
            pts += 5
            info["ddqn_main.py"] = f"5/5 — exists ({sz} B)"
        elif sz > 0:
            pts += 3
            info["ddqn_main.py"] = f"3/5 — too small ({sz} B)"
        else:
            info["ddqn_main.py"] = "0/5 — empty file"
    else:
        alt = _find_main_py(answer_dir)
        if alt:
            pts += 2
            info["ddqn_main.py"] = f"2/5 — not named ddqn_main.py, but found {os.path.basename(alt)}"
        else:
            info["ddqn_main.py"] = "0/5 — missing"

    # 1b. training_logs (5 pts)
    log_dir = _find_log_dir(answer_dir)
    if log_dir:
        files = [f for f in os.listdir(log_dir)
                 if f.endswith((".csv", ".txt", ".json", ".log"))]
        if len(files) >= 2:
            pts += 5
            info["training_logs"] = f"5/5 — {len(files)} data files"
        elif len(files) == 1:
            pts += 3
            info["training_logs"] = f"3/5 — only 1 data file"
        else:
            pts += 1
            info["training_logs"] = "1/5 — directory exists but no data files"
    else:
        # Check for scattered csv files in root directory
        root_logs = [f for f in os.listdir(answer_dir)
                     if f.endswith((".csv", ".log"))
                     and ("loss" in f.lower() or "reward" in f.lower())]
        if root_logs:
            pts += 2
            info["training_logs"] = f"2/5 — no directory, but root has {root_logs}"
        else:
            info["training_logs"] = "0/5 — missing"

    return pts, info


# =========================================================================
# Dimension 2: Code Quality & Runnability (15 pts)
# =========================================================================

def _dim2_code_quality(answer_dir: str) -> Tuple[int, dict]:
    pts = 0
    info: dict = {}

    code_path = _find_main_py(answer_dir)
    code = _read_file(code_path)
    if not code:
        info["error"] = "0/15 — no readable code"
        return 0, info

    # 2a. Syntax (5 pts)
    try:
        ast.parse(code)
        pts += 5
        info["syntax"] = "5/5 — passed"
    except SyntaxError as e:
        info["syntax"] = f"0/5 — {str(e)[:120]}"
        return pts, info

    lo = code.lower()

    # 2b. Key libraries (5 pts)
    lib_pts = 0
    lib_notes: List[str] = []
    if "import gymnasium" in code or "import gym" in code:
        lib_pts += 2; lib_notes.append("gym OK")
    else:
        lib_notes.append("gym MISSING")
    if "import torch" in code or "from torch" in code:
        lib_pts += 2; lib_notes.append("torch OK")
    elif "import numpy" in code:
        lib_pts += 2; lib_notes.append("numpy-ML OK")
    else:
        lib_notes.append("ML framework MISSING")
    if "import numpy" in code or "from numpy" in code:
        lib_pts += 1; lib_notes.append("numpy OK")
    else:
        lib_notes.append("numpy MISSING")
    pts += lib_pts
    info["key_libraries"] = f"{lib_pts}/5 — {', '.join(lib_notes)}"

    # 2c. Network structure & dual networks (5 pts)
    net_pts = 0
    net_notes: List[str] = []

    has_net_def = bool(
        re.search(r"class\s+\w*(net|network|mlp|dqn)\w*", lo, re.I)
        or "nn.sequential" in lo or "nn.linear" in lo
    )
    if has_net_def:
        net_pts += 3; net_notes.append("network definition OK")
    else:
        net_notes.append("network definition MISSING")

    dual = (
        ("policy_net" in lo and "target_net" in lo)
        or ("eval_net" in lo and "target_net" in lo)
        or ("q_net" in lo and "target" in lo)
        or ("online" in lo and "target" in lo)
    )
    if dual:
        net_pts += 2; net_notes.append("dual networks OK")
    else:
        net_notes.append("dual networks MISSING")

    pts += net_pts
    info["network_structure"] = f"{net_pts}/5 — {', '.join(net_notes)}"

    return pts, info


# =========================================================================
# Dimension 3: DDQN Core Logic (30 pts)  —  LLM + Static Analysis
# =========================================================================

_DDQN_PROMPT = """\
You are a reinforcement learning algorithm review expert. Please analyze whether the following Python code correctly implements **Double DQN (DDQN)**.

Core checkpoints:
1. **DDQN Target Computation** (most critical):
   - Standard DQN: target = r + gamma * max_a Q_target(s', a)
   - DDQN: a* = argmax_a Q_policy(s', a), target = r + gamma * Q_target(s', a*)
   - Does the code first use policy/eval net on next_state to select action (argmax), then use target net to compute Q value for that action?
2. **Experience Replay**: Is there a replay buffer that stores (s,a,r,s',done) and randomly samples batches?
3. **Epsilon-Greedy**: Does epsilon decay during training?
4. **Target Network Sync**: Are policy net parameters periodically copied to target net?

Please reply strictly in JSON:
```json
{{
  "ddqn_target": {{"score": 0, "max": 12, "reason": ""}},
  "replay_buffer": {{"score": 0, "max": 8, "reason": ""}},
  "epsilon_greedy": {{"score": 0, "max": 5, "reason": ""}},
  "target_sync": {{"score": 0, "max": 5, "reason": ""}}
}}
```

ddqn_target scoring (0-12):
  10-12 = Fully correct DDQN (policy selects action, target evaluates)
  6-9   = Has DDQN idea but implementation has flaws
  1-5   = Standard DQN (target net max) rather than Double
  0     = No target value computation

replay_buffer scoring (0-8):
  7-8 = Complete (storage/sampling/capacity limit)
  4-6 = Incomplete functionality
  1-3 = Simple storage only
  0   = None

epsilon_greedy scoring (0-5):
  4-5 = Has decay
  2-3 = Fixed epsilon
  0-1 = None

target_sync scoring (0-5):
  4-5 = Periodic hard/soft update
  2-3 = Has update but unreasonable frequency
  0-1 = None

```python
{code}
```
"""


def _dim3_ddqn_logic(answer_dir: str) -> Tuple[int, dict]:
    pts = 0
    info: dict = {}

    code_path = _find_main_py(answer_dir)
    code = _read_file(code_path)
    if not code:
        info["error"] = "0/30 — no code"
        return 0, info

    lo = code.lower()

    # ---------- Static analysis (fallback) ----------
    sa_pts = 0
    sa_info: dict = {}

    # 3a DDQN target
    has_argmax = "argmax" in lo
    has_policy_sel = (
        ("policy_net" in lo or "eval_net" in lo or "q_net" in lo or "online" in lo)
        and has_argmax
    )
    has_target = "target_net" in lo or "target_network" in lo
    has_index = "gather" in lo or "next_actions" in lo or "[np.arange" in code or "batch_indices" in lo

    if has_policy_sel and has_target and has_index:
        sa_pts += 12; sa_info["DDQN_target"] = "12/12"
    elif has_policy_sel and has_target:
        sa_pts += 8;  sa_info["DDQN_target"] = "8/12 — indexing unclear"
    elif has_target and has_argmax:
        sa_pts += 5;  sa_info["DDQN_target"] = "5/12 — possibly standard DQN"
    else:
        sa_info["DDQN_target"] = "0/12"

    # 3b Experience replay
    has_buf = any(k in lo for k in ["replay", "buffer", "experience", "memory"])
    has_sample = "sample" in lo and ("batch" in lo or "random" in lo)
    has_cap = "deque" in lo or "maxlen" in lo or "capacity" in lo

    if has_buf and has_sample and has_cap:
        sa_pts += 8; sa_info["experience_replay"] = "8/8"
    elif has_buf and has_sample:
        sa_pts += 6; sa_info["experience_replay"] = "6/8"
    elif has_buf:
        sa_pts += 3; sa_info["experience_replay"] = "3/8"
    else:
        sa_info["experience_replay"] = "0/8"

    # 3c epsilon
    has_eps = "epsilon" in lo or "eps" in lo
    has_decay = "decay" in lo or "eps_end" in lo or "eps_min" in lo
    has_rand_act = "random" in lo and "action" in lo

    if has_eps and has_decay and has_rand_act:
        sa_pts += 5; sa_info["Epsilon"] = "5/5"
    elif has_eps and has_rand_act:
        sa_pts += 3; sa_info["Epsilon"] = "3/5"
    elif has_rand_act:
        sa_pts += 1; sa_info["Epsilon"] = "1/5"
    else:
        sa_info["Epsilon"] = "0/5"

    # 3d target sync
    has_copy = any(k in lo for k in [
        "load_state_dict", "copy_from", "hard_update", "soft_update",
    ])
    has_freq = any(k in lo for k in [
        "target_update", "update_freq", "sync", "update_target",
    ])
    if has_copy and has_freq:
        sa_pts += 5; sa_info["target_network_sync"] = "5/5"
    elif has_copy:
        sa_pts += 3; sa_info["target_network_sync"] = "3/5"
    elif "target" in lo and "update" in lo:
        sa_pts += 2; sa_info["target_network_sync"] = "2/5"
    else:
        sa_info["target_network_sync"] = "0/5"

    # ---------- LLM evaluation ----------
    config = _cfg(answer_dir)
    code_trunc = code[:15000]
    raw = _llm(_DDQN_PROMPT.format(code=code_trunc), config)
    parsed = _json_from_llm(raw)

    if parsed and "ddqn_target" in parsed:
        try:
            d_s = max(0, min(12, int(parsed["ddqn_target"]["score"])))
            r_s = max(0, min(8, int(parsed["replay_buffer"]["score"])))
            e_s = max(0, min(5, int(parsed["epsilon_greedy"]["score"])))
            t_s = max(0, min(5, int(parsed["target_sync"]["score"])))
            pts = d_s + r_s + e_s + t_s
            info["DDQN_target (12)"] = f"{d_s}/12 — {parsed['ddqn_target'].get('reason','')}"
            info["experience_replay (8)"] = f"{r_s}/8 — {parsed['replay_buffer'].get('reason','')}"
            info["Epsilon (5)"] = f"{e_s}/5 — {parsed['epsilon_greedy'].get('reason','')}"
            info["target_network_sync (5)"] = f"{t_s}/5 — {parsed['target_sync'].get('reason','')}"
            info["evaluation_method"] = "LLM-as-Judge"
        except (KeyError, ValueError, TypeError):
            pts = sa_pts
            info.update(sa_info)
            info["evaluation_method"] = "Static analysis (LLM format error)"
    else:
        pts = sa_pts
        info.update(sa_info)
        info["evaluation_method"] = "Static analysis (LLM unavailable)"

    return pts, info


# =========================================================================
# Dimension 4: Training Log Quality (15 pts)
# =========================================================================

def _dim4_training_logs(answer_dir: str) -> Tuple[int, dict]:
    pts = 0
    info: dict = {}

    log_dir = _find_log_dir(answer_dir)

    # Helper: search for csv/txt with keyword in log_dir and answer_dir
    def _find_values(keyword: str) -> List[float]:
        best: List[float] = []
        search_dirs = []
        if log_dir:
            search_dirs.append(log_dir)
        search_dirs.append(answer_dir)
        for sd in search_dirs:
            if not os.path.isdir(sd):
                continue
            for fn in os.listdir(sd):
                if keyword in fn.lower() and fn.endswith((".csv", ".txt")):
                    v = _csv_col(os.path.join(sd, fn))
                    if len(v) > len(best):
                        best = v
        return best

    # 4a. Loss (7 pts)
    loss_vals = _find_values("loss")
    if len(loss_vals) >= 1000:
        pts += 5
        if len(loss_vals) >= 100:
            first_avg = sum(loss_vals[:100]) / 100
            last_avg = sum(loss_vals[-100:]) / 100
            if last_avg < first_avg:
                pts += 2
                info["Loss"] = f"7/7 — {len(loss_vals)} entries, decreasing trend ({first_avg:.4f}->{last_avg:.4f})"
            else:
                info["Loss"] = f"5/7 — {len(loss_vals)} entries, but no clear decrease"
        else:
            info["Loss"] = f"5/7 — {len(loss_vals)} entries"
    elif len(loss_vals) >= 100:
        pts += 3
        info["Loss"] = f"3/7 — {len(loss_vals)} entries (insufficient)"
    elif loss_vals:
        pts += 1
        info["Loss"] = f"1/7 — only {len(loss_vals)} entries"
    else:
        info["Loss"] = "0/7 — not found"

    # 4b. Reward (5 pts)
    rew_vals = _find_values("reward")
    if len(rew_vals) >= 100:
        pts += 3
        if len(rew_vals) >= 20:
            f10 = sum(rew_vals[:10]) / 10
            l10 = sum(rew_vals[-10:]) / 10
            if l10 > f10:
                pts += 2
                info["Reward"] = f"5/5 — {len(rew_vals)} entries, increasing ({f10:.1f}->{l10:.1f})"
            else:
                info["Reward"] = f"3/5 — {len(rew_vals)} entries, no clear increase"
        else:
            info["Reward"] = f"3/5 — {len(rew_vals)} entries"
    elif len(rew_vals) >= 10:
        pts += 2
        info["Reward"] = f"2/5 — {len(rew_vals)} entries"
    elif rew_vals:
        pts += 1
        info["Reward"] = f"1/5 — {len(rew_vals)} entries"
    else:
        info["Reward"] = "0/5 — not found"

    # 4c. Test result record (3 pts)
    test_found = False
    test_val = None
    for sd in ([log_dir] if log_dir else []) + [answer_dir]:
        if not sd or not os.path.isdir(sd):
            continue
        for fn in os.listdir(sd):
            if "test" in fn.lower() and fn.endswith((".txt", ".log", ".json", ".csv")):
                content = _read_file(os.path.join(sd, fn), limit=4096)
                if content.strip():
                    test_found = True
                    for tok in content.replace(",", " ").replace(":", " ").split():
                        try:
                            v = float(tok)
                            if -500 <= v <= 0:
                                test_val = v
                        except ValueError:
                            pass
                    break
        if test_found:
            break

    if test_found and test_val is not None:
        pts += 3
        info["test_result"] = f"3/3 — reward={test_val}"
    elif test_found:
        pts += 2
        info["test_result"] = "2/3 — file found but cannot parse value"
    else:
        info["test_result"] = "0/3 — no test result file found"

    return pts, info


# =========================================================================
# Dimension 5: Performance Target (30 pts)   —  LLM + Static Analysis
# =========================================================================

_PERF_PROMPT = """\
You are a reinforcement learning experiment reviewer. Based on the following information, determine whether this Double DQN model was successfully trained on MountainCar-v0.

Target criterion: single test reward > -200 (i.e., car reaches hilltop within 200 steps).

## Test Results
{test_info}

## Last 20 Episode Rewards
{reward_tail}

## Test Code Snippet
{test_snippet}

Please reply strictly in JSON:
```json
{{
  "test_code": {{"score": 0, "max": 8, "reason": ""}},
  "perf_evidence": {{"score": 0, "max": 12, "reason": ""}},
  "convergence": {{"score": 0, "max": 10, "reason": ""}}
}}
```

test_code (0-8): Does the code have a complete test / greedy evaluation logic
  7-8 = Complete greedy test loop
  4-6 = Simple test
  0-3 = None or minimal

perf_evidence (0-12): Is there evidence reward > -200
  10-12 = Clearly meets target
  6-9   = Close to target / positive trend
  2-5   = Has test but does not meet target
  0-1   = No evidence

convergence (0-10): Has training converged
  8-10 = Reward clearly improved and stable > -200 in later episodes
  4-7  = Some improvement but unstable
  1-3  = Almost no improvement
  0    = No data
"""


def _dim5_performance(answer_dir: str) -> Tuple[int, dict]:
    pts = 0
    info: dict = {}

    code_path = _find_main_py(answer_dir)
    code = _read_file(code_path)
    lo = code.lower() if code else ""
    log_dir = _find_log_dir(answer_dir)

    # --- Collect information ---
    test_info = "No test result file"
    test_val = None

    for sd in ([log_dir] if log_dir else []) + [answer_dir]:
        if not sd or not os.path.isdir(sd):
            continue
        for fn in os.listdir(sd):
            if "test" in fn.lower() and fn.endswith((".txt", ".log", ".json", ".csv")):
                c = _read_file(os.path.join(sd, fn), limit=4096).strip()
                if c:
                    test_info = c
                    for tok in c.replace(",", " ").replace(":", " ").split():
                        try:
                            v = float(tok)
                            if -500 <= v <= 0:
                                test_val = v
                        except ValueError:
                            pass
                    break
        if test_val is not None:
            break

    # reward data
    rew_vals: List[float] = []
    for sd in ([log_dir] if log_dir else []) + [answer_dir]:
        if not sd or not os.path.isdir(sd):
            continue
        for fn in os.listdir(sd):
            if "reward" in fn.lower() and fn.endswith((".csv", ".txt")):
                v = _csv_col(os.path.join(sd, fn))
                if len(v) > len(rew_vals):
                    rew_vals = v

    tail_str = str([round(x, 1) for x in rew_vals[-20:]]) if rew_vals else "None"

    # Test code snippet
    snippet = ""
    if code:
        lines = code.split("\n")
        for i, l in enumerate(lines):
            ll = l.lower()
            if ("def " in ll or "# " in ll) and any(k in ll for k in ["test", "evaluate", "greedy"]):
                snippet = "\n".join(lines[i:i + 30])
                break

    # ---------- Static analysis fallback ----------
    sa_pts = 0
    sa_info: dict = {}

    # 5a Test code
    has_test_func = bool(re.search(
        r"(def\s+(test|evaluate)|#\s*(test|evaluation|greedy))", lo, re.I
    ))
    has_loop = ("for " in lo or "while " in lo) and ("step" in lo or "episode" in lo)
    if has_test_func and has_loop:
        sa_pts += 8; sa_info["test_code"] = "8/8"
    elif has_test_func:
        sa_pts += 5; sa_info["test_code"] = "5/8"
    elif "test" in lo or "evaluate" in lo:
        sa_pts += 3; sa_info["test_code"] = "3/8"
    else:
        sa_info["test_code"] = "0/8"

    # 5b Performance evidence
    if test_val is not None and test_val > -200:
        sa_pts += 12; sa_info["perf_evidence"] = f"12/12 — reward={test_val}"
    elif test_val is not None and test_val > -220:
        sa_pts += 8; sa_info["perf_evidence"] = f"8/12 — reward={test_val} close"
    elif test_val is not None:
        sa_pts += 4; sa_info["perf_evidence"] = f"4/12 — reward={test_val} below target"
    elif rew_vals:
        best = max(rew_vals[-20:]) if len(rew_vals) >= 20 else max(rew_vals)
        if best > -200:
            sa_pts += 8; sa_info["perf_evidence"] = f"8/12 — training best reward={best:.1f}"
        elif best > -220:
            sa_pts += 5; sa_info["perf_evidence"] = f"5/12 — training best reward={best:.1f}"
        else:
            sa_pts += 2; sa_info["perf_evidence"] = f"2/12 — training best reward={best:.1f}"
    else:
        sa_info["perf_evidence"] = "0/12 — no data"

    # 5c Convergence
    if rew_vals and len(rew_vals) >= 20:
        f10 = sum(rew_vals[:10]) / 10
        l10 = sum(rew_vals[-10:]) / 10
        imp = l10 - f10
        if l10 > -200 and imp > 0:
            sa_pts += 10; sa_info["convergence"] = f"10/10 — late avg={l10:.1f}"
        elif l10 > -210 and imp > 0:
            sa_pts += 7; sa_info["convergence"] = f"7/10 — late avg={l10:.1f}"
        elif imp > 10:
            sa_pts += 5; sa_info["convergence"] = f"5/10 — improved ({f10:.1f}->{l10:.1f})"
        elif imp > 0:
            sa_pts += 3; sa_info["convergence"] = f"3/10 — slight improvement"
        else:
            sa_pts += 1; sa_info["convergence"] = f"1/10 — no improvement ({f10:.1f}->{l10:.1f})"
    elif rew_vals:
        sa_pts += 2; sa_info["convergence"] = f"2/10 — insufficient data ({len(rew_vals)} ep)"
    else:
        sa_info["convergence"] = "0/10 — no training data"

    # ---------- LLM ----------
    config = _cfg(answer_dir)
    raw = _llm(_PERF_PROMPT.format(
        test_info=test_info,
        reward_tail=tail_str,
        test_snippet=snippet[:3000],
    ), config)
    parsed = _json_from_llm(raw)

    if parsed and "test_code" in parsed:
        try:
            tc = max(0, min(8, int(parsed["test_code"]["score"])))
            pe = max(0, min(12, int(parsed["perf_evidence"]["score"])))
            cv = max(0, min(10, int(parsed["convergence"]["score"])))
            pts = tc + pe + cv
            info["test_code (8)"] = f"{tc}/8 — {parsed['test_code'].get('reason','')}"
            info["perf_evidence (12)"] = f"{pe}/12 — {parsed['perf_evidence'].get('reason','')}"
            info["convergence (10)"] = f"{cv}/10 — {parsed['convergence'].get('reason','')}"
            info["evaluation_method"] = "LLM-as-Judge"
        except (KeyError, ValueError, TypeError):
            pts = sa_pts
            info.update(sa_info)
            info["evaluation_method"] = "Static analysis (LLM format error)"
    else:
        pts = sa_pts
        info.update(sa_info)
        info["evaluation_method"] = "Static analysis (LLM unavailable)"

    return pts, info


# =========================================================================
# Entry point
# =========================================================================

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Evaluate agent output.

    Args:
        answer_dir: absolute path to agent output directory

    Returns:
        (score, report)  score: 0-100 integer, report: detailed report dict
    """
    s1, r1 = _dim1_file_delivery(answer_dir)
    s2, r2 = _dim2_code_quality(answer_dir)
    s3, r3 = _dim3_ddqn_logic(answer_dir)
    s4, r4 = _dim4_training_logs(answer_dir)
    s5, r5 = _dim5_performance(answer_dir)

    total = min(100, s1 + s2 + s3 + s4 + s5)

    report: Dict[str, Any] = {
        "total_score": total,
        "dimension_scores": {
            "1. File Delivery": f"{s1}/10",
            "2. Code Quality": f"{s2}/15",
            "3. DDQN Core Logic": f"{s3}/30",
            "4. Training Logs": f"{s4}/15",
            "5. Performance Target": f"{s5}/30",
        },
        "details": {
            "1. File Delivery (10 pts)": r1,
            "2. Code Quality (15 pts)": r2,
            "3. DDQN Core Logic (30 pts)": r3,
            "4. Training Logs (15 pts)": r4,
            "5. Performance Target (30 pts)": r5,
        },
    }

    if total >= 90:
        report["comment"] = "Excellent — DDQN implementation complete, training converged, performance target met."
    elif total >= 75:
        report["comment"] = "Good — Core logic correct, some dimensions have room for improvement."
    elif total >= 60:
        report["comment"] = "Passing — Basic DDQN implementation but significant deficiencies exist."
    elif total >= 40:
        report["comment"] = "Partially completed — Key components missing or performance target not met."
    else:
        report["comment"] = "Failing — Task completion seriously insufficient."

    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print formatted evaluation report."""
    print("=" * 70)
    print("Evaluation Report — Double DQN-Based MountainCar Energy Hill-Climbing Optimization")
    print("=" * 70)
    print(f"\nTotal Score: {score}/100\n")

    for k, v in report.get("dimension_scores", {}).items():
        print(f"  {k}: {v}")

    for section, data in report.get("details", {}).items():
        print(f"\n{'─'*50}")
        print(f"[{section}]")
        print(f"{'─'*50}")
        if isinstance(data, dict):
            for dk, dv in data.items():
                print(f"  {dk}: {dv}")
        else:
            print(f"  {data}")

    print(f"\n{'='*70}")
    print(f"Comment: {report.get('comment', '')}")
    print("=" * 70)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(__file__), "..", "gpt-5", "attempt_1")
    if not os.path.isabs(target):
        target = os.path.join(os.getcwd(), target)
    if os.path.isdir(target):
        print(f"Evaluating directory: {target}\n")
        s, r = evaluate(target)
        print_report(s, r)
    else:
        print(f"Directory not found: {target}")
        sys.exit(0)
