"""
Scoring Script - DQN Reinforcement Learning Algorithm Migration from TensorFlow to PyTorch

Total score: 100 points, six dimensions:
  1. File Delivery              10 points
  2. PyTorch Migration and Code Structure  30 points
  3. Functional Correctness     25 points
  4. Hyperparameter Tuning Module  15 points
  5. Visualization Module       10 points
  6. Code Standards and Comments  10 points
"""

from __future__ import annotations

import ast
import os
import re
import json
import base64
from typing import Any, Dict, List, Tuple

try:
    from PIL import Image
except ImportError:
    Image = None

try:
    import openai
except ImportError:
    openai = None


# -- Environment and LLM Utilities ------------------------------------------

def _load_env(answer_dir: str) -> dict:
    values: dict = {}
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
    def g(key: str, default: str = "") -> str:
        return os.environ.get(key) or env.get(key) or default
    return {
        "api_key": g("EVAL_TEXT_API_KEY", g("ANTHROPIC_API_KEY")),
        "api_base": g("EVAL_TEXT_API_BASE_URL", g("ANTHROPIC_BASE_URL")),
        "model": g("EVAL_TEXT_MODEL", "openai/gpt-5.2"),
    }


def _get_vision_eval_config(answer_dir: str) -> dict:
    env = _load_env(answer_dir)
    def g(key: str, default: str = "") -> str:
        return os.environ.get(key) or env.get(key) or default
    return {
        "api_key": g("EVAL_VISION_API_KEY", g("ANTHROPIC_API_KEY")),
        "api_base": g("EVAL_VISION_API_BASE_URL", g("ANTHROPIC_BASE_URL")),
        "model": g("EVAL_VISION_MODEL", "openai/gpt-5.2"),
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


def _call_vision_llm(image_path: str, prompt: str, config: dict) -> str:
    if not openai or not config.get("api_key"):
        return ""
    try:
        with open(image_path, "rb") as f:
            image_b64 = base64.b64encode(f.read()).decode("utf-8")
        ext = os.path.splitext(image_path)[1].lower()
        mime = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".webp": "image/webp",
        }.get(ext, "image/png")
        base_url = config["api_base"].rstrip("/")
        if not base_url.endswith("/v1"):
            base_url += "/v1"
        client = openai.OpenAI(api_key=config["api_key"], base_url=base_url)
        resp = client.chat.completions.create(
            model=config["model"],
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url",
                     "image_url": {"url": f"data:{mime};base64,{image_b64}"}},
                ],
            }],
            max_tokens=1024,
            temperature=0,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        print(f"[RUBRIC] Vision LLM error: {e}")
        return ""


# -- Helpers -----------------------------------------------------------------

def _read_file(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except Exception:
        return ""


def _find_dqn_file(answer_dir: str) -> str:
    """Prefer dqn_torch.py, otherwise find any .py containing torch"""
    exact = os.path.join(answer_dir, "dqn_torch.py")
    if os.path.isfile(exact):
        return exact
    for root, _, files in os.walk(answer_dir):
        if "dqn_torch.py" in files:
            return os.path.join(root, "dqn_torch.py")
    for root, _, files in os.walk(answer_dir):
        for f in files:
            if f.endswith(".py"):
                content = _read_file(os.path.join(root, f))
                if "torch" in content.lower():
                    return os.path.join(root, f)
    return ""


def _find_png_files(answer_dir: str) -> List[str]:
    results: List[str] = []
    for root, _, files in os.walk(answer_dir):
        for f in files:
            if f.lower().endswith(".png"):
                results.append(os.path.join(root, f))
    return results


def _parse_json_from_text(text: str) -> dict:
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0].strip()
    elif "```" in text:
        text = text.split("```")[1].split("```")[0].strip()
    try:
        return json.loads(text)
    except Exception:
        return {}


# -- 1. File Delivery (10 points) -------------------------------------------

def _eval_file_delivery(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details: Dict[str, str] = {}
    issues: List[str] = []

    # 1a. dqn_torch.py exists (6 points)
    dqn = _find_dqn_file(answer_dir)
    if dqn and os.path.basename(dqn) == "dqn_torch.py":
        score += 6
        details["dqn_torch.py"] = "6/6"
    elif dqn:
        score += 3
        details["dqn_torch.py"] = f"3/6 - found {os.path.basename(dqn)} but filename is not dqn_torch.py"
        issues.append("Filename is not dqn_torch.py")
    else:
        details["dqn_torch.py"] = "0/6 - DQN code file not found"
        issues.append("Missing dqn_torch.py")

    # 1b. Training visualization PNG (4 points)
    pngs = _find_png_files(answer_dir)
    if len(pngs) >= 2:
        score += 4
        names = [os.path.basename(p) for p in pngs[:5]]
        details["Visualization PNG"] = f"4/4 - {len(pngs)} files: {', '.join(names)}"
    elif len(pngs) == 1:
        score += 2
        details["Visualization PNG"] = f"2/4 - only 1 file ({os.path.basename(pngs[0])})"
        issues.append("Only 1 visualization image, expected >= 2 (reward + loss curves)")
    else:
        details["Visualization PNG"] = "0/4 - no PNG found"
        issues.append("Missing training visualization images")

    return score, {"score": score, "max": 10, "details": details, "issues": issues}


# -- 2. PyTorch Migration and Code Structure (30 points) --------------------

def _eval_pytorch_migration(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details: Dict[str, str] = {}
    issues: List[str] = []

    dqn = _find_dqn_file(answer_dir)
    if not dqn:
        return 0, {"score": 0, "max": 30, "details": {"error": "no code file"}, "issues": ["no code"]}

    code = _read_file(dqn)
    if not code.strip():
        return 0, {"score": 0, "max": 30, "details": {"error": "code is empty"}, "issues": ["code is empty"]}

    code_lower = code.lower()

    # 2.1 PyTorch imports (6 points)
    has_torch = bool(re.search(r'import\s+torch|from\s+torch', code))
    has_nn = bool(re.search(r'import\s+torch\.nn|from\s+torch\.nn|from\s+torch\s+import\s+nn', code))
    has_optim = bool(re.search(r'torch\.optim|from\s+torch\.optim', code))
    no_tf = "tensorflow" not in code_lower and "import tf" not in code_lower

    s = 0
    if has_torch:
        s += 2
    if has_nn:
        s += 2
    if has_optim:
        s += 1
    if no_tf:
        s += 1
    else:
        issues.append("Still contains TensorFlow imports")
    score += s
    details["2.1 PyTorch imports (6)"] = f"{s}/6"

    # 2.2 Gymnasium (4 points)
    has_gymnasium = bool(re.search(r'import\s+gymnasium|from\s+gymnasium', code))
    has_gym = bool(re.search(r'import\s+gym\b', code)) and not has_gymnasium
    has_mc = "mountaincar" in code_lower or "mountain_car" in code_lower

    s = 0
    if has_gymnasium:
        s += 3
    elif has_gym:
        s += 1
        issues.append("Used old gym instead of gymnasium")
    if has_mc:
        s += 1
    score += s
    details["2.2 Gymnasium (4)"] = f"{s}/4"

    # 2.3 nn.Module network (6 points)
    has_module = bool(re.search(r'class\s+\w+\s*\(\s*(?:nn\.Module|torch\.nn\.Module)\s*\)', code))
    has_forward = bool(re.search(r'def\s+forward\s*\(\s*self', code))
    has_linear = "nn.Linear" in code or "nn.linear" in code_lower
    has_relu = "relu" in code_lower

    s = 0
    if has_module:
        s += 3
    if has_forward:
        s += 1
    if has_linear:
        s += 1
    if has_relu:
        s += 1
    score += s
    details["2.3 nn.Module (6)"] = f"{s}/6"

    # 2.4 ReplayBuffer (5 points)
    has_rb_class = bool(re.search(r'class\s+\w*[Rr]eplay\w*', code))
    has_store = bool(re.search(r'def\s+(?:store|add|push|append|store_tuple)', code))
    has_sample = bool(re.search(r'def\s+(?:sample|get_batch|sample_buffer)', code))
    has_storage = bool(re.search(r'deque|np\.zeros|self\.(?:buffer|memory|storage|state_buffer)', code))

    s = 0
    if has_rb_class:
        s += 2
    if has_store:
        s += 1
    if has_sample:
        s += 1
    if has_storage:
        s += 1
    score += s
    details["2.4 ReplayBuffer (5)"] = f"{s}/5"

    # 2.5 Target network (5 points)
    has_target = bool(re.search(r'target|q_target', code_lower))
    has_wt_copy = bool(re.search(r'load_state_dict|state_dict\(\)|copy\.deepcopy|\.parameters\(\)', code))
    has_upd_rate = bool(re.search(r'update_rate|target_update|update_freq|update_every|sync', code_lower))

    s = 0
    if has_target:
        s += 2
    if has_wt_copy:
        s += 2
    if has_upd_rate:
        s += 1
    score += s
    details["2.5 Target network (5)"] = f"{s}/5"

    # 2.6 Loss and optimization (4 points)
    has_loss = bool(re.search(r'mse_loss|MSELoss|smooth_l1|SmoothL1Loss|huber', code, re.IGNORECASE))
    has_adam = bool(re.search(r'Adam', code))
    has_backward = ".backward()" in code
    has_step = "optimizer.step()" in code or ".step()" in code

    s = 0
    if has_loss:
        s += 1
    if has_adam:
        s += 1
    if has_backward:
        s += 1
    if has_step:
        s += 1
    score += s
    details["2.6 Loss and optimization (4)"] = f"{s}/4"

    return score, {"score": score, "max": 30, "details": details, "issues": issues}


# -- 3. Functional Correctness (25 points) ----------------------------------

def _eval_functionality(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details: Dict[str, Any] = {}
    issues: List[str] = []

    dqn = _find_dqn_file(answer_dir)
    if not dqn:
        return 0, {"score": 0, "max": 25, "details": {"error": "no code"}, "issues": ["no code"]}

    code = _read_file(dqn)

    # 3.1 Syntax correctness (5 points)
    try:
        ast.parse(code)
        score += 5
        details["3.1 Syntax (5)"] = "5/5"
    except SyntaxError as e:
        details["3.1 Syntax (5)"] = f"0/5 - {str(e)[:80]}"
        issues.append("Syntax error")
        return score, {"score": score, "max": 25, "details": details, "issues": issues}

    # 3.2 epsilon-greedy (4 points)
    has_eps = bool(re.search(r'epsilon|eps', code, re.IGNORECASE))
    has_rand = bool(re.search(r'random\.\w+|np\.random|torch\.rand', code))
    has_argmax = bool(re.search(r'argmax|\.max\(', code))
    has_decay = bool(re.search(r'epsilon.*decay|eps.*decay|epsilon.*min|epsilon_final|epsilon_end', code, re.IGNORECASE))

    s = 0
    if has_eps and has_rand:
        s += 2
    if has_argmax:
        s += 1
    if has_decay:
        s += 1
    score += s
    details["3.2 epsilon-greedy (4)"] = f"{s}/4"

    # 3.3 Training loop (6 points)
    has_ep_loop = bool(re.search(r'for\s+\w+\s+in\s+range', code))
    has_step_loop = bool(re.search(r'while\s+not\s+(?:done|terminated|truncated)', code)) or \
                    bool(re.search(r'while\s+(?:True|not\s+\w*done)', code, re.IGNORECASE))
    has_env_step = bool(re.search(r'env\.step\s*\(', code))
    has_env_reset = bool(re.search(r'env\.reset\s*\(', code))
    has_score_track = bool(re.search(r'score|reward.*total|episode_reward|total_reward', code, re.IGNORECASE))

    s = 0
    if has_ep_loop:
        s += 2
    if has_step_loop:
        s += 1
    if has_env_step:
        s += 1
    if has_env_reset:
        s += 1
    if has_score_track:
        s += 1
    score += s
    details["3.3 Training loop (6)"] = f"{s}/6"

    # 3.4 LLM in-depth evaluation (10 points)
    config = _get_text_eval_config(answer_dir)

    ctx_dir = os.path.join(os.path.dirname(__file__), "..", "context")
    tf_agent = _read_file(os.path.join(ctx_dir, "agent.py")) if os.path.isdir(ctx_dir) else ""

    llm_prompt = f"""You are a reinforcement learning code review expert. Below is a DQN code migrated from TensorFlow to PyTorch.

Please evaluate from three dimensions (total 10 points) and return strict JSON:

1. **algorithm_completeness** (0-4): Is the DQN core complete?
   - Q network and target network definition and usage
   - Experience replay storage and sampling
   - TD target computation (reward + gamma * max Q(s', a'))
   - Loss computation and backpropagation

2. **migration_accuracy** (0-3): Is the original TF version's core logic preserved?
   - Network structure (fc1=256, fc2=256)
   - Hyperparameters (lr=0.001, discount=0.99, batch_size=64, buffer=1000000)
   - Epsilon decay strategy (decay=0.001, min=0.01)

3. **pytorch_conventions** (0-3): Does it follow PyTorch conventions?
   - nn.Module + forward()
   - Tensor operations (.detach(), torch.no_grad())
   - Training flow (zero_grad -> loss -> backward -> step)

Return JSON (no other content):
```json
{{"algorithm_completeness": {{"score": 0, "reason": ""}}, "migration_accuracy": {{"score": 0, "reason": ""}}, "pytorch_conventions": {{"score": 0, "reason": ""}}, "total": 0}}
```

=== PyTorch Code ===
{code[:6000]}

=== Original TF agent.py (reference) ===
{tf_agent[:3000]}
"""

    llm_text = _call_llm_judge(llm_prompt, config)
    llm_result = _parse_json_from_text(llm_text) if llm_text else {}

    if llm_result and "algorithm_completeness" in llm_result:
        ac = max(0, min(4, int(llm_result.get("algorithm_completeness", {}).get("score", 0))))
        ma = max(0, min(3, int(llm_result.get("migration_accuracy", {}).get("score", 0))))
        pc = max(0, min(3, int(llm_result.get("pytorch_conventions", {}).get("score", 0))))
        llm_s = ac + ma + pc
        score += llm_s
        details["3.4 LLM evaluation (10)"] = {
            "Algorithm completeness": f"{ac}/4 - {llm_result.get('algorithm_completeness', {}).get('reason', '')}",
            "Migration accuracy": f"{ma}/3 - {llm_result.get('migration_accuracy', {}).get('reason', '')}",
            "PyTorch conventions": f"{pc}/3 - {llm_result.get('pytorch_conventions', {}).get('reason', '')}",
            "Subtotal": f"{llm_s}/10",
        }
    else:
        fallback = 4
        score += fallback
        details["3.4 LLM evaluation (10)"] = f"{fallback}/10 - LLM unavailable, conservative score"

    return score, {"score": score, "max": 25, "details": details, "issues": issues}


# -- 4. Hyperparameter Tuning Module (15 points) ----------------------------

def _eval_hyperparameter_tuning(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details: Dict[str, str] = {}
    issues: List[str] = []

    dqn = _find_dqn_file(answer_dir)
    if not dqn:
        return 0, {"score": 0, "max": 15, "details": {"error": "no code"}, "issues": ["no code"]}

    code = _read_file(dqn)
    code_lower = code.lower()

    # 4.1 Tuning function/module (5 points)
    has_tune_func = bool(re.search(
        r'def\s+(?:tune|hyperparameter|grid_search|param_search|run_experiments|sweep)',
        code, re.IGNORECASE,
    ))
    has_product = "itertools.product" in code or "product(" in code
    has_param_combo = bool(re.search(r'(?:param|hyper).*(?:grid|combinations|configs|search_space)', code, re.IGNORECASE))
    has_param_loop = bool(re.search(r'for\s+\w+\s+in\s+\[.*(?:0\.\d+|1e).*\]', code, re.IGNORECASE))
    has_param_list = bool(re.search(
        r'(?:learning_rate|lr|batch_size|gamma|discount|epsilon)s?\s*=\s*\[.*,.*\]',
        code, re.IGNORECASE,
    ))

    s = 0
    if has_tune_func:
        s += 3
    elif has_param_combo or has_product:
        s += 2
    if has_param_loop or has_param_list:
        s += 2
    elif has_param_combo:
        s += 1
    score += s
    details["4.1 Tuning module (5)"] = f"{s}/5"

    # 4.2 Multiple parameter variations (5 points)
    param_names: set = set()
    param_patterns = [
        (r'(?:learning_rate|lr)s?\s*=\s*\[(.+?)\]', "learning_rate"),
        (r'batch_size[s]?\s*=\s*\[(.+?)\]', "batch_size"),
        (r'(?:gamma|discount)s?\s*=\s*\[(.+?)\]', "gamma"),
        (r'epsilon[s]?\s*=\s*\[(.+?)\]', "epsilon"),
    ]
    for pat, name in param_patterns:
        if re.search(pat, code, re.IGNORECASE):
            param_names.add(name)

    generic = re.findall(r'(\w+)\s*=\s*\[\s*(?:\d+\.?\d*\s*,\s*){1,}', code)
    for name in generic:
        nl = name.lower()
        if any(k in nl for k in ["lr", "learn", "rate", "batch", "gamma", "discount",
                                   "eps", "hidden", "fc", "layer", "update"]):
            param_names.add(nl)

    cnt = len(param_names)
    s = 0
    if cnt >= 3:
        s = 5
    elif cnt >= 2:
        s = 3
    elif cnt >= 1:
        s = 2
    elif has_tune_func or has_param_loop:
        s = 1
    score += s
    details["4.2 Multiple parameters (5)"] = f"{s}/5 - detected {cnt} types: {', '.join(sorted(param_names)) if param_names else 'none'}"

    # 4.3 Recording and comparison (5 points)
    has_result_store = bool(re.search(r'results?\s*(?:\[|\.append|=\s*\{)', code))
    has_print_res = bool(re.search(r'print\s*\(.*(?:result|best|param|config)', code, re.IGNORECASE))
    has_best = bool(re.search(r'best_(?:score|reward|param|config|result)', code, re.IGNORECASE))
    has_cmp_viz = bool(re.search(r'(?:plot|bar|scatter).*(?:param|config|tune|comparison)', code, re.IGNORECASE))

    s = 0
    if has_result_store:
        s += 2
    if has_best:
        s += 1
    if has_print_res:
        s += 1
    if has_cmp_viz:
        s += 1
    score += s
    details["4.3 Recording and comparison (5)"] = f"{s}/5"

    if score == 0:
        issues.append("Hyperparameter tuning module not implemented")

    return score, {"score": score, "max": 15, "details": details, "issues": issues}


# -- 5. Visualization Module (10 points) ------------------------------------

def _eval_visualization(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details: Dict[str, Any] = {}
    issues: List[str] = []

    dqn = _find_dqn_file(answer_dir)
    code = _read_file(dqn) if dqn else ""

    # 5.1 matplotlib usage (3 points)
    has_plt_import = bool(re.search(r'import\s+matplotlib|from\s+matplotlib', code))
    has_plt_plot = bool(re.search(r'plt\.plot|ax\.plot|axes.*\.plot', code))
    has_savefig = bool(re.search(r'(?:plt|fig|figure)\.savefig', code))

    s = 0
    if has_plt_import:
        s += 1
    if has_plt_plot:
        s += 1
    if has_savefig:
        s += 1
    score += s
    details["5.1 matplotlib (3)"] = f"{s}/3"

    # 5.2 Reward curve (3 points)
    has_reward_plot = bool(re.search(
        r'(?:reward|score|episode_reward).*(?:plot|curve|fig)|(?:plot|curve).*(?:reward|score)',
        code, re.IGNORECASE,
    ))
    has_reward_label = bool(re.search(r'(?:label|title|ylabel).*(?:reward|score)', code, re.IGNORECASE))
    has_avg = bool(re.search(r'(?:avg|average|mean).*(?:score|reward)', code, re.IGNORECASE))

    s = 0
    if has_reward_plot:
        s += 1
    if has_reward_label:
        s += 1
    if has_avg:
        s += 1
    score += s
    details["5.2 Reward curve (3)"] = f"{s}/3"

    # 5.3 Loss curve (2 points)
    has_loss_track = bool(re.search(r'loss(?:es|_list|_history|_values)?\s*(?:\.|\.append|\[)', code, re.IGNORECASE))
    has_loss_plot = bool(re.search(
        r'(?:loss).*(?:plot|curve|fig)|(?:plot|curve).*(?:loss)', code, re.IGNORECASE,
    ))

    s = 0
    if has_loss_track:
        s += 1
    if has_loss_plot:
        s += 1
    score += s
    details["5.3 Loss curve (2)"] = f"{s}/2"

    # 5.4 Actual image check (2 points)
    pngs = _find_png_files(answer_dir)
    if pngs:
        vis_config = _get_vision_eval_config(answer_dir)
        vis_prompt = """You are a chart evaluation expert. This image should be a visualization of the DQN reinforcement learning training process (reward curves, loss curves, etc.).

Evaluate:
1. Is this a training process visualization chart?
2. Does it have axis labels, title, legend?
3. Is the data trend reasonable?

Return JSON:
```json
{"is_training_chart": true, "score": 0, "reason": ""}
```
score range 0-2."""

        vis_text = _call_vision_llm(pngs[0], vis_prompt, vis_config)
        vis_result = _parse_json_from_text(vis_text) if vis_text else {}

        if vis_result and "score" in vis_result:
            vs = max(0, min(2, int(vis_result.get("score", 0))))
            score += vs
            details["5.4 Image quality (2)"] = f"{vs}/2 - {vis_result.get('reason', '')}"
        else:
            try:
                fsize = os.path.getsize(pngs[0])
                if fsize > 10000:
                    score += 1
                    details["5.4 Image quality (2)"] = f"1/2 - Vision unavailable, {fsize // 1024}KB (conservative score)"
                else:
                    details["5.4 Image quality (2)"] = f"0/2 - Vision unavailable, file only {fsize // 1024}KB"
            except Exception:
                details["5.4 Image quality (2)"] = "0/2 - unable to check"
    else:
        details["5.4 Image quality (2)"] = "0/2 - no PNG"
        issues.append("No visualization image output")

    return score, {"score": score, "max": 10, "details": details, "issues": issues}


# -- 6. Code Standards and Comments (10 points) -----------------------------

def _eval_code_quality(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details: Dict[str, str] = {}
    issues: List[str] = []

    dqn = _find_dqn_file(answer_dir)
    if not dqn:
        return 0, {"score": 0, "max": 10, "details": {"error": "no code"}, "issues": ["no code"]}

    code = _read_file(dqn)
    lines = code.split("\n")
    total_lines = len(lines)

    # 6.1 __main__ entry (2 points)
    has_main = "__name__" in code and "__main__" in code
    if has_main:
        score += 2
        details["6.1 __main__ (2)"] = "2/2"
    else:
        details["6.1 __main__ (2)"] = "0/2"
        issues.append("Missing if __name__ == '__main__'")

    # 6.2 Comment count (3 points)
    comment_lines = sum(1 for l in lines if l.strip().startswith("#"))
    inline_comments = sum(1 for l in lines if "#" in l and not l.strip().startswith("#"))
    docstrings = len(re.findall(r'"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'', code))
    total_comments = comment_lines + inline_comments + docstrings

    s = 0
    if total_comments >= 15:
        s = 3
    elif total_comments >= 8:
        s = 2
    elif total_comments >= 3:
        s = 1
    score += s
    details["6.2 Comments (3)"] = f"{s}/3 - {total_comments} occurrences"

    # 6.3 Header instructions (2 points)
    header = "\n".join(lines[:30]).lower()
    has_install = bool(re.search(r'pip\s+install|requirements|dependencies|install', header))
    has_run = bool(re.search(r'run|usage|how\s+to|python\s+dqn', header))

    s = 0
    if has_install:
        s += 1
    if has_run:
        s += 1
    score += s
    details["6.3 Header instructions (2)"] = f"{s}/2"

    # 6.4 Code structure (3 points)
    num_classes = len(re.findall(r'^class\s+', code, re.MULTILINE))
    num_funcs = len(re.findall(r'^def\s+', code, re.MULTILINE))

    s = 0
    if num_classes >= 2 and num_funcs >= 3:
        s = 3
    elif num_classes >= 1 and num_funcs >= 2:
        s = 2
    elif num_classes >= 1 or num_funcs >= 2:
        s = 1

    if total_lines < 50:
        s = max(0, s - 1)
        issues.append(f"Code too short ({total_lines} lines)")

    score += s
    details["6.4 Structure (3)"] = f"{s}/3 - {num_classes} classes, {num_funcs} functions, {total_lines} lines"

    return score, {"score": score, "max": 10, "details": details, "issues": issues}


# -- Entry Point -------------------------------------------------------------

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Evaluate the agent's output.

    Args:
        answer_dir: Absolute path to the agent output directory

    Returns:
        (score, report)  score: 0-100 integer, report: dict
    """
    s1, r1 = _eval_file_delivery(answer_dir)
    s2, r2 = _eval_pytorch_migration(answer_dir)
    s3, r3 = _eval_functionality(answer_dir)
    s4, r4 = _eval_hyperparameter_tuning(answer_dir)
    s5, r5 = _eval_visualization(answer_dir)
    s6, r6 = _eval_code_quality(answer_dir)

    total = max(0, min(100, s1 + s2 + s3 + s4 + s5 + s6))

    all_issues: List[str] = []
    for r in [r1, r2, r3, r4, r5, r6]:
        all_issues.extend(r.get("issues", []))

    report: Dict[str, Any] = {
        "total_score": total,
        "section_scores": {
            "I. File delivery": f"{s1}/10",
            "II. PyTorch migration": f"{s2}/30",
            "III. Functional correctness": f"{s3}/25",
            "IV. Hyperparameter tuning": f"{s4}/15",
            "V. Visualization": f"{s5}/10",
            "VI. Code standards": f"{s6}/10",
        },
        "detailed_report": {
            "I. File delivery (10)": r1,
            "II. PyTorch migration (30)": r2,
            "III. Functional correctness (25)": r3,
            "IV. Hyperparameter tuning (15)": r4,
            "V. Visualization (10)": r5,
            "VI. Code standards (10)": r6,
        },
        "deduction_reasons_summary": all_issues,
    }

    if total >= 85:
        report["comment"] = "Excellent! Successfully completed TF->PyTorch migration with hyperparameter tuning and visualization."
    elif total >= 70:
        report["comment"] = "Good. Core migration complete, some dimensions have room for improvement."
    elif total >= 50:
        report["comment"] = "Passing. Basic migration complete, notable deficiencies exist."
    elif total >= 30:
        report["comment"] = "Partially complete. Code incomplete or key features missing."
    else:
        report["comment"] = "Failing. Task completion is severely insufficient."

    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print formatted evaluation report."""
    print("=" * 70)
    print("DQN Migration Evaluation Report")
    print("Task: DQN Reinforcement Learning Algorithm Migration from TensorFlow to PyTorch")
    print("=" * 70)
    print(f"\nTotal score: {score}/100\n")

    scores = report.get("section_scores", {})
    if scores:
        print("Section scores:")
        for k, v in scores.items():
            print(f"  {k}: {v}")

    for sec_name, sec_data in report.get("detailed_report", {}).items():
        print(f"\n{'─' * 60}")
        print(f"[{sec_name}] {sec_data.get('score', 0)}/{sec_data.get('max', '?')}")
        print(f"{'─' * 60}")
        for k, v in sec_data.get("details", {}).items():
            if isinstance(v, dict):
                print(f"  {k}:")
                for kk, vv in v.items():
                    print(f"    {kk}: {vv}")
            else:
                print(f"  {k}: {v}")
        iss = sec_data.get("issues", [])
        if iss:
            print("  Issues:")
            for i in iss:
                print(f"    - {i}")

    all_iss = report.get("deduction_reasons_summary", [])
    if all_iss:
        print(f"\n{'─' * 60}")
        print("Deduction reasons summary:")
        for idx, i in enumerate(all_iss, 1):
            print(f"  {idx}. {i}")

    print(f"\n{'=' * 70}")
    print(f"Comment: {report.get('comment', '')}")
    print("=" * 70)


if __name__ == "__main__":
    import sys
    test_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(__file__), "..", "workspace")
    if os.path.exists(test_dir):
        print(f"Evaluating directory: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"Directory not found: {test_dir}")
    sys.exit(0)
