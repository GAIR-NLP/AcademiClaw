"""
Rubric for train_model_haoqiu_query2
Task: Implement A3C and PPO on Gymnasium Pendulum-v1

Total: 100 points
  Result score (60):
    1. File delivery          10
    2. Algorithm key points   35
    3. LLM code quality       15
  Process score (40):
    4. Code structure         15
    5. README reproducibility 15
    6. Training toolchain     10
"""

import os
import re
import ast
import json
from typing import Tuple, Dict, Any

try:
    import openai
except ImportError:
    openai = None


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _read(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except Exception:
        return ""


def _file_exists(d: str, name: str) -> bool:
    return os.path.isfile(os.path.join(d, name))


def _syntax_ok(path: str) -> bool:
    try:
        ast.parse(_read(path))
        return True
    except Exception:
        return False


def _pat(code: str, pattern: str) -> bool:
    return bool(re.search(pattern, code, re.IGNORECASE))


# ---------------------------------------------------------------------------
# LLM infrastructure
# ---------------------------------------------------------------------------

def _load_env(answer_dir: str) -> dict:
    values = {}
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


def _parse_json(text: str) -> dict:
    if not text:
        return {}
    try:
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        return json.loads(text)
    except Exception:
        return {}


# ---------------------------------------------------------------------------
# 1. File delivery (10 pts)
# ---------------------------------------------------------------------------

DELIVERABLES = [
    "train.py",
    "a3c.py",
    "ppo.py",
    "models.py",
    "utils.py",
    "evaluate.py",
    "README.md",
]

PY_DELIVERABLES = [f for f in DELIVERABLES if f.endswith(".py")]


def _score_file_delivery(d: str) -> Tuple[int, dict]:
    """Each required file present = 1 pt (7 total).
    Each python file with valid syntax = +0.5 pt (max 3 bonus).
    Capped at 10."""
    pts = 0.0
    info = {}
    missing = []

    for f in DELIVERABLES:
        if _file_exists(d, f):
            pts += 1.0
            info[f] = "present"
        else:
            info[f] = "MISSING"
            missing.append(f)

    syntax_bonus = 0.0
    for f in PY_DELIVERABLES:
        p = os.path.join(d, f)
        if os.path.isfile(p):
            if _syntax_ok(p):
                syntax_bonus += 0.5
                info[f] += " | syntax OK"
            else:
                info[f] += " | SYNTAX ERROR"

    score = min(10, int(pts + syntax_bonus))
    return score, {"score": score, "files": info, "missing": missing}


# ---------------------------------------------------------------------------
# 2. Algorithm key points (35 pts)
# ---------------------------------------------------------------------------

def _score_models(code: str) -> Tuple[int, list]:
    """models.py  (10 pts)
    - nn.Module + PyTorch        2
    - tanh scaled to [-2,2]      3
    - Critic value head          2
    - Normal distribution        2
    - Weight init                1
    """
    s = 0
    notes = []
    if not code:
        return 0, ["models.py empty or missing"]

    if _pat(code, r"nn\.Module") and _pat(code, r"import\s+torch"):
        s += 2; notes.append("nn.Module+torch: 2/2")
    else:
        notes.append("nn.Module+torch: 0/2")

    has_tanh = _pat(code, r"tanh")
    has_scale = _pat(code, r"\*\s*2|action_scale|2\.0|\[-?\s*2")
    if has_tanh and has_scale:
        s += 3; notes.append("tanh scale [-2,2]: 3/3")
    elif has_tanh:
        s += 1; notes.append("tanh present, scale unclear: 1/3")
    else:
        notes.append("tanh scale: 0/3")

    if _pat(code, r"value|v_head|critic"):
        s += 2; notes.append("Critic head: 2/2")
    else:
        notes.append("Critic head: 0/2")

    if _pat(code, r"Normal\("):
        s += 2; notes.append("Normal dist: 2/2")
    elif _pat(code, r"log_prob|log_std"):
        s += 1; notes.append("Normal dist partial: 1/2")
    else:
        notes.append("Normal dist: 0/2")

    if _pat(code, r"orthogonal_|xavier|kaiming|init_weight"):
        s += 1; notes.append("Weight init: 1/1")
    else:
        notes.append("Weight init: 0/1")

    return min(10, s), notes


def _score_ppo(code: str) -> Tuple[int, list]:
    """ppo.py  (13 pts)
    - Clipped surrogate objective   4
    - GAE advantage estimation      4
    - Mini-batch multi-epoch        3
    - Gradient clipping             2
    """
    s = 0
    notes = []
    if not code:
        return 0, ["ppo.py empty or missing"]

    has_ratio = _pat(code, r"ratio|log_prob.*old|logp_old|logprob")
    has_clamp = _pat(code, r"clamp|clip")
    has_min = _pat(code, r"torch\.min|\.min\(")
    if has_ratio and has_clamp and has_min:
        s += 4; notes.append("Clipped surrogate: 4/4")
    elif has_ratio and has_clamp:
        s += 3; notes.append("Clipped surrogate (no min): 3/4")
    elif has_ratio:
        s += 1; notes.append("Clipped surrogate (ratio only): 1/4")
    else:
        notes.append("Clipped surrogate: 0/4")

    has_reversed = _pat(code, r"reversed\(range")
    has_delta = _pat(code, r"delta|td_error")
    has_lam = _pat(code, r"lam|lambda|gae")
    if has_reversed and has_delta and has_lam:
        s += 4; notes.append("GAE: 4/4")
    elif (has_reversed and has_delta) or (has_delta and has_lam):
        s += 2; notes.append("GAE partial: 2/4")
    elif _pat(code, r"advantage|adv"):
        s += 1; notes.append("GAE (advantage var only): 1/4")
    else:
        notes.append("GAE: 0/4")

    has_epoch = _pat(code, r"update_epoch|n_epoch|ppo_epoch|range\(.*epoch")
    has_mb = _pat(code, r"minibatch|mini_batch|batch_size|shuffle")
    if has_epoch and has_mb:
        s += 3; notes.append("Mini-batch multi-epoch: 3/3")
    elif has_epoch or has_mb:
        s += 1; notes.append("Mini-batch multi-epoch partial: 1/3")
    else:
        notes.append("Mini-batch multi-epoch: 0/3")

    if _pat(code, r"clip_grad_norm|clip_grad_value|max_grad_norm"):
        s += 2; notes.append("Grad clip: 2/2")
    else:
        notes.append("Grad clip: 0/2")

    return min(13, s), notes


def _score_a3c(code: str) -> Tuple[int, list]:
    """a3c.py  (12 pts)
    - Multiprocessing async        4
    - Global net + share_memory    3
    - N-step returns               3
    - Async update                 2
    """
    s = 0
    notes = []
    if not code:
        return 0, ["a3c.py empty or missing"]

    has_mp = _pat(code, r"torch\.multiprocessing|multiprocessing")
    has_proc = _pat(code, r"Process\(|mp\.Process")
    if has_mp and has_proc:
        s += 4; notes.append("Multiprocessing: 4/4")
    elif has_mp:
        s += 2; notes.append("Multiprocessing (import only): 2/4")
    else:
        notes.append("Multiprocessing: 0/4")

    has_global = _pat(code, r"global.*net|shared.*model|global.*model|global_net|shared_net")
    has_share = _pat(code, r"share_memory")
    if has_global and has_share:
        s += 3; notes.append("Global net + share_memory: 3/3")
    elif has_share:
        s += 2; notes.append("share_memory (global net unclear): 2/3")
    elif has_global:
        s += 1; notes.append("Global net (no share_memory): 1/3")
    else:
        notes.append("Global net + share_memory: 0/3")

    has_nstep = _pat(code, r"n[_-]?step|nstep")
    has_rollout = _pat(code, r"rollout|buffer|returns")
    has_discount = _pat(code, r"gamma\s*\*\*|gamma\s*\*|discount")
    if has_nstep or (has_rollout and has_discount):
        s += 3; notes.append("N-step returns: 3/3")
    elif has_rollout:
        s += 1; notes.append("N-step returns (rollout only): 1/3")
    else:
        notes.append("N-step returns: 0/3")

    has_shared_optim = _pat(code, r"shared.*optim|SharedAdam")
    has_update = _pat(code, r"optimizer\.step|optim\.step|\.backward\(\)")
    if has_shared_optim or (has_update and has_mp):
        s += 2; notes.append("Async update: 2/2")
    elif has_update:
        s += 1; notes.append("Async update (update only): 1/2")
    else:
        notes.append("Async update: 0/2")

    return min(12, s), notes


def _score_algo_total(d: str) -> Tuple[int, dict]:
    s1, n1 = _score_models(_read(os.path.join(d, "models.py")))
    s2, n2 = _score_ppo(_read(os.path.join(d, "ppo.py")))
    s3, n3 = _score_a3c(_read(os.path.join(d, "a3c.py")))
    total = min(35, s1 + s2 + s3)
    return total, {
        "score": total,
        "models.py (10)": {"score": s1, "notes": n1},
        "ppo.py (13)": {"score": s2, "notes": n2},
        "a3c.py (12)": {"score": s3, "notes": n3},
    }


# ---------------------------------------------------------------------------
# 3. LLM code quality assessment (15 pts)
# ---------------------------------------------------------------------------

_LLM_QUALITY_PROMPT = """\
You are a deep reinforcement learning code reviewer. Below is student code
implementing A3C and PPO for Gymnasium Pendulum-v1. Evaluate strictly.

## models.py
```python
{models}
```

## ppo.py
```python
{ppo}
```

## a3c.py
```python
{a3c}
```

## train.py
```python
{train}
```

Score each dimension (integer). Give a brief reason.

**Dim 1: PPO correctness** (0-5)
5 = GAE correct, clip obj correct, mini-batch correct, advantage normalization
3-4 = mostly correct, minor issues
1-2 = core logic errors
0 = not implemented

**Dim 2: A3C correctness** (0-5)
5 = multiprocessing correct, share_memory, n-step, global net update
3-4 = mostly correct
1-2 = core logic errors
0 = not implemented

**Dim 3: Model design & engineering** (0-5)
5 = good Actor-Critic, correct action scale, reasonable hyper-params, clean code
3-4 = acceptable
1-2 = obvious design flaws
0 = unreasonable

Reply strictly in this JSON (no other text):
```json
{{
  "ppo_correctness": {{"score": 0, "reason": ""}},
  "a3c_correctness": {{"score": 0, "reason": ""}},
  "engineering": {{"score": 0, "reason": ""}},
  "total": 0
}}
```
"""


def _score_llm_quality(d: str) -> Tuple[int, dict]:
    config = _get_text_eval_config(d)
    models = _read(os.path.join(d, "models.py"))[:3000]
    ppo = _read(os.path.join(d, "ppo.py"))[:5000]
    a3c = _read(os.path.join(d, "a3c.py"))[:5000]
    train = _read(os.path.join(d, "train.py"))[:2000]

    if not (models or ppo or a3c):
        return 0, {"score": 0, "note": "core files empty"}

    prompt = _LLM_QUALITY_PROMPT.format(models=models, ppo=ppo, a3c=a3c, train=train)
    raw = _call_llm_judge(prompt, config)
    result = _parse_json(raw)

    if not result:
        fb = 0
        for f in ["models.py", "ppo.py", "a3c.py"]:
            if _file_exists(d, f) and _syntax_ok(os.path.join(d, f)):
                fb += 2
        fb = min(5, fb)
        return fb, {"score": fb, "note": "LLM unavailable, conservative fallback"}

    ppo_s = max(0, min(5, int(result.get("ppo_correctness", {}).get("score", 0))))
    a3c_s = max(0, min(5, int(result.get("a3c_correctness", {}).get("score", 0))))
    eng_s = max(0, min(5, int(result.get("engineering", {}).get("score", 0))))
    total = min(15, ppo_s + a3c_s + eng_s)

    return total, {
        "score": total,
        "ppo": f"{ppo_s}/5 - {result.get('ppo_correctness', {}).get('reason', '')}",
        "a3c": f"{a3c_s}/5 - {result.get('a3c_correctness', {}).get('reason', '')}",
        "eng": f"{eng_s}/5 - {result.get('engineering', {}).get('reason', '')}",
    }


# ---------------------------------------------------------------------------
# 4. Code structure & modularity (15 pts)
# ---------------------------------------------------------------------------

def _score_code_structure(d: str) -> Tuple[int, dict]:
    """
    - train.py references modules correctly   (4)
    - evaluate.py loads checkpoint & evals     (4)
    - Module separation                        (4)
    - Pendulum-v1 env usage                    (3)
    """
    notes = []
    train_c = _read(os.path.join(d, "train.py"))
    eval_c = _read(os.path.join(d, "evaluate.py"))
    ppo_c = _read(os.path.join(d, "ppo.py"))
    a3c_c = _read(os.path.join(d, "a3c.py"))
    models_c = _read(os.path.join(d, "models.py"))

    # train.py module references
    ts = 0
    if _pat(train_c, r"--algo|argparse"):
        ts += 1
    if _pat(train_c, r"from\s+ppo|import\s+ppo"):
        ts += 1
    if _pat(train_c, r"from\s+a3c|import\s+a3c"):
        ts += 1
    if _pat(train_c, r"from\s+models|import\s+models"):
        ts += 1
    ts = min(4, ts)
    notes.append(f"train.py refs: {ts}/4")

    # evaluate.py
    es = 0
    if _pat(eval_c, r"load_state_dict|load_checkpoint|torch\.load"):
        es += 2
    if _pat(eval_c, r"Pendulum|gymnasium|gym"):
        es += 1
    if _pat(eval_c, r"render|eval|reward|episode"):
        es += 1
    es = min(4, es)
    notes.append(f"evaluate.py: {es}/4")

    # module separation
    ms = 0
    if _pat(models_c, r"class\s+\w+.*nn\.Module"):
        ms += 2
    if _pat(ppo_c, r"from\s+models|import\s+models"):
        ms += 1
    if _pat(a3c_c, r"from\s+models|import\s+models"):
        ms += 1
    ms = min(4, ms)
    notes.append(f"module separation: {ms}/4")

    # Pendulum-v1
    combined = ppo_c + a3c_c + train_c
    ps = 0
    if _pat(combined, r"Pendulum-v1|Pendulum"):
        ps += 2
    if _pat(combined, r"gymnasium|gym"):
        ps += 1
    ps = min(3, ps)
    notes.append(f"Pendulum-v1: {ps}/3")

    total = min(15, ts + es + ms + ps)
    return total, {"score": total, "notes": notes}


# ---------------------------------------------------------------------------
# 5. README reproducibility (15 pts)
# ---------------------------------------------------------------------------

def _score_readme(d: str) -> Tuple[int, dict]:
    """
    - Dependency install instructions   (5)
    - Training run commands             (5)
    - TensorBoard / evaluation docs     (5)
    """
    notes = []
    readme = _read(os.path.join(d, "README.md"))
    if not readme:
        return 0, {"score": 0, "notes": ["README.md empty or missing"]}

    # deps
    ds = 0
    if _pat(readme, r"pip\s+install|requirements\.txt|conda"):
        ds += 3
    if _pat(readme, r"torch|pytorch|gymnasium|gym"):
        ds += 2
    ds = min(5, ds)
    notes.append(f"deps: {ds}/5")

    # training cmds
    cs = 0
    if _pat(readme, r"python\s+train\.py"):
        cs += 3
    if _pat(readme, r"--algo\s+(ppo|a3c)"):
        cs += 2
    cs = min(5, cs)
    notes.append(f"train cmds: {cs}/5")

    # TB / eval
    xs = 0
    if _pat(readme, r"tensorboard"):
        xs += 2
    if _pat(readme, r"evaluate\.py|python\s+evaluate"):
        xs += 2
    if _pat(readme, r"checkpoint|ckpt|\.pt|\.pth"):
        xs += 1
    xs = min(5, xs)
    notes.append(f"TB/eval docs: {xs}/5")

    total = min(15, ds + cs + xs)
    return total, {"score": total, "notes": notes}


# ---------------------------------------------------------------------------
# 6. Training toolchain (10 pts)
# ---------------------------------------------------------------------------

def _score_utils(d: str) -> Tuple[int, dict]:
    """
    - Checkpoint save/load    (4)
    - TensorBoard / logging   (4)
    - Seed / env helpers      (2)
    """
    notes = []
    code = _read(os.path.join(d, "utils.py"))
    if not code:
        return 0, {"score": 0, "notes": ["utils.py empty or missing"]}

    # checkpoint
    cs = 0
    if _pat(code, r"torch\.save|save_checkpoint"):
        cs += 2
    if _pat(code, r"torch\.load|load_checkpoint"):
        cs += 2
    cs = min(4, cs)
    notes.append(f"checkpoint: {cs}/4")

    # TB
    ts = 0
    if _pat(code, r"SummaryWriter|tensorboard"):
        ts += 3
    if _pat(code, r"add_scalar|log"):
        ts += 1
    ts = min(4, ts)
    notes.append(f"TensorBoard: {ts}/4")

    # aux
    ax = 0
    if _pat(code, r"seed|set_seed|random"):
        ax += 1
    if _pat(code, r"make_env|gymnasium|gym\.make"):
        ax += 1
    ax = min(2, ax)
    notes.append(f"seed/env: {ax}/2")

    total = min(10, cs + ts + ax)
    return total, {"score": total, "notes": notes}


# ===========================================================================
# Public interface
# ===========================================================================

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Evaluate agent output for the A3C + PPO Pendulum-v1 task.

    Args:
        answer_dir: absolute path to agent output directory

    Returns:
        (score, report)  where score is 0-100 int
    """
    # --- Result score (60) ---
    s1, d1 = _score_file_delivery(answer_dir)       # 10
    s2, d2 = _score_algo_total(answer_dir)           # 35
    s3, d3 = _score_llm_quality(answer_dir)          # 15
    result = min(60, s1 + s2 + s3)

    # --- Process score (40) ---
    s4, d4 = _score_code_structure(answer_dir)       # 15
    s5, d5 = _score_readme(answer_dir)               # 15
    s6, d6 = _score_utils(answer_dir)                # 10
    process = min(40, s4 + s5 + s6)

    total = result + process

    if total >= 90:
        comment = "Excellent: complete, correct implementations with good engineering."
    elif total >= 75:
        comment = "Good: mostly meets requirements, minor gaps."
    elif total >= 60:
        comment = "Passing: core parts implemented but notable issues."
    elif total >= 40:
        comment = "Partial: significant files or algorithms missing."
    else:
        comment = "Failing: major requirements unmet."

    report = {
        "total": total,
        "result_score": {
            "score": result,
            "1_file_delivery_10": d1,
            "2_algorithm_keys_35": d2,
            "3_llm_quality_15": d3,
        },
        "process_score": {
            "score": process,
            "4_code_structure_15": d4,
            "5_readme_15": d5,
            "6_toolchain_10": d6,
        },
        "comment": comment,
    }
    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print formatted evaluation report."""
    sep = "=" * 70
    dash = "-" * 50

    print(sep)
    print("Evaluation Report — A3C & PPO on Pendulum-v1")
    print(sep)
    print(f"\nTotal score: {score}/100\n")

    for section_key, label in [
        ("result_score", "Result Score (60)"),
        ("process_score", "Process Score (40)"),
    ]:
        section = report.get(section_key, {})
        print(dash)
        print(f"[{label}]  {section.get('score', 0)}")
        print(dash)
        for k, v in section.items():
            if k == "score":
                continue
            print(f"\n  {k}:")
            if isinstance(v, dict):
                for kk, vv in v.items():
                    if isinstance(vv, list):
                        for item in vv:
                            print(f"      - {item}")
                    elif isinstance(vv, dict):
                        for kkk, vvv in vv.items():
                            if isinstance(vvv, list):
                                for item in vvv:
                                    print(f"          - {item}")
                            else:
                                print(f"        {kkk}: {vvv}")
                    else:
                        print(f"    {kk}: {vv}")
            else:
                print(f"    {v}")

    print(f"\n{sep}")
    print(f"Comment: {report.get('comment', '')}")
    print(sep)


if __name__ == "__main__":
    import sys

    test_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(__file__), "..", "gpt-5", "attempt_1"
    )
    if os.path.isdir(test_dir):
        print(f"Evaluating: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"Directory does not exist: {test_dir}")
    sys.exit(0)
