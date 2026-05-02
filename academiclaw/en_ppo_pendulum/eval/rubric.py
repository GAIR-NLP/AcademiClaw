"""
Scoring Rubric — PPO Algorithm Implementation for Pendulum-v1 Continuous Environment
Total: 100 points

Dimension 1  File Delivery              10 pts
Dimension 2  Code Syntax & Structure    15 pts
Dimension 3  PPO Core Mechanisms        35 pts
Dimension 4  Continuous Action Space    10 pts
Dimension 5  Training Performance       30 pts
"""

import os
import re
import ast
import json
import sys
from typing import Tuple, Dict, Any, List, Optional

try:
    import openai
except ImportError:
    openai = None


# ============================================================================
# Environment / LLM Utilities
# ============================================================================

def _load_env(answer_dir: str) -> dict:
    """Load .env configuration from answer_dir and query root directory"""
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


# ============================================================================
# File Reading Utilities
# ============================================================================

def _read_file(path: str) -> Optional[str]:
    if not os.path.isfile(path):
        return None
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except Exception:
        return None


def _find_main_py(answer_dir: str) -> Optional[str]:
    """Find the main Python file (preferring ppo_pendulum.py)"""
    target = os.path.join(answer_dir, "ppo_pendulum.py")
    if os.path.isfile(target):
        return target
    # Fallback: py files containing ppo
    if os.path.isdir(answer_dir):
        for f in sorted(os.listdir(answer_dir)):
            if f.endswith(".py") and "ppo" in f.lower():
                return os.path.join(answer_dir, f)
        # Then any py file
        for f in sorted(os.listdir(answer_dir)):
            if f.endswith(".py"):
                return os.path.join(answer_dir, f)
    return None


def _collect_log_content(answer_dir: str) -> str:
    """Collect all log (txt/log/csv) content"""
    content = ""
    if not os.path.isdir(answer_dir):
        return content
    for fname in sorted(os.listdir(answer_dir)):
        if fname.endswith((".txt", ".log", ".csv")) and fname != "query.md":
            fp = os.path.join(answer_dir, fname)
            try:
                with open(fp, "r", encoding="utf-8", errors="replace") as f:
                    content += f.read() + "\n"
            except Exception:
                pass
    return content


# ============================================================================
# Dimension 1: File Delivery (10 pts)
# ============================================================================

def _dim1_file_delivery(answer_dir: str) -> Tuple[int, Dict[str, str]]:
    """
    1.1 ppo_pendulum.py exists and is valid (5 pts)
    1.2 Training log file exists             (5 pts)
    """
    score = 0
    details: Dict[str, str] = {}

    # --- 1.1 ppo_pendulum.py ---
    exact = os.path.join(answer_dir, "ppo_pendulum.py")
    if os.path.isfile(exact):
        sz = os.path.getsize(exact)
        if sz >= 500:
            score += 5
            details["1.1 ppo_pendulum.py"] = f"5/5 — exists ({sz} B)"
        elif sz > 0:
            score += 3
            details["1.1 ppo_pendulum.py"] = f"3/5 — file too small ({sz} B)"
        else:
            details["1.1 ppo_pendulum.py"] = "0/5 — file is empty"
    else:
        alt = _find_main_py(answer_dir)
        if alt:
            name = os.path.basename(alt)
            if "ppo" in name.lower():
                score += 2
                details["1.1 ppo_pendulum.py"] = f"2/5 — filename does not fully match, found {name}"
            else:
                score += 1
                details["1.1 ppo_pendulum.py"] = f"1/5 — ppo_pendulum.py not found, found {name}"
        else:
            details["1.1 ppo_pendulum.py"] = "0/5 — no Python file found"

    # --- 1.2 Training log ---
    log_files: List[str] = []
    if os.path.isdir(answer_dir):
        log_files = [
            f for f in os.listdir(answer_dir)
            if f.endswith((".txt", ".log", ".csv")) and f != "query.md"
        ]
    if log_files:
        total_sz = sum(
            os.path.getsize(os.path.join(answer_dir, lf))
            for lf in log_files
        )
        if total_sz >= 500:
            score += 5
            details["1.2 Training log"] = f"5/5 — {', '.join(log_files)} ({total_sz} B)"
        elif total_sz > 0:
            score += 3
            details["1.2 Training log"] = f"3/5 — log too small ({total_sz} B)"
        else:
            details["1.2 Training log"] = "0/5 — log file is empty"
    else:
        # Check if code has print logging
        py_path = _find_main_py(answer_dir)
        code = _read_file(py_path) if py_path else None
        if code and re.search(r'print\s*\(.*(?:return|reward|episode)', code, re.I):
            score += 2
            details["1.2 Training log"] = "2/5 — no separate log, code has print output"
        else:
            details["1.2 Training log"] = "0/5 — no training log found"

    return score, details


# ============================================================================
# Dimension 2: Code Syntax & Structure (15 pts)
# ============================================================================

def _dim2_code_structure(code: Optional[str]) -> Tuple[int, Dict[str, str]]:
    """
    2.1 Python syntax correct       (5 pts)
    2.2 Key library imports          (3 pts)
    2.3 Actor-Critic structure       (4 pts)
    2.4 Training loop                (3 pts)
    """
    if code is None:
        return 0, {"error": "0/15 — cannot read code"}

    score = 0
    details: Dict[str, str] = {}

    # 2.1 Syntax
    try:
        ast.parse(code)
        score += 5
        details["2.1 Syntax"] = "5/5 — passed"
    except SyntaxError as e:
        details["2.1 Syntax"] = f"0/5 — {str(e)[:120]}"
        return 0, details  # Syntax error makes subsequent checks unreliable

    # 2.2 Key libraries
    pts = 0
    has_torch = bool(re.search(r'(?:import\s+torch|from\s+torch)', code))
    has_gym = bool(re.search(r'(?:import\s+gymnasium|import\s+gym|from\s+gymnasium|from\s+gym)', code))
    has_numpy = bool(re.search(r'(?:import\s+numpy|from\s+numpy)', code))
    if has_torch:
        pts += 1
    if has_gym:
        pts += 1
    if has_numpy:
        pts += 1
    score += pts
    missing = []
    if not has_torch:
        missing.append("torch")
    if not has_gym:
        missing.append("gymnasium/gym")
    if not has_numpy:
        missing.append("numpy")
    details["2.2 Key imports"] = f"{pts}/3" + (f" — missing {', '.join(missing)}" if missing else "")

    # 2.3 Actor-Critic
    ac = 0
    has_actor = bool(re.search(
        r'class\s+\w*(?:Actor|Policy|ActorCritic)\w*|'
        r'(?:actor|policy)[\w_]*\s*=\s*.*(?:nn\.|Sequential|Linear)|'
        r'mu_layer|mean_layer|policy_net|actor_net',
        code, re.I
    ))
    has_critic = bool(re.search(
        r'class\s+\w*(?:Critic|Value|ActorCritic)\w*|'
        r'(?:critic|value)[\w_]*\s*=\s*.*(?:nn\.|Sequential|Linear)|'
        r'v_layer|value_layer|value_net|critic_net',
        code, re.I
    ))
    if has_actor:
        ac += 2
    if has_critic:
        ac += 2
    score += ac
    parts = []
    if has_actor:
        parts.append("Actor")
    if has_critic:
        parts.append("Critic")
    details["2.3 Actor-Critic"] = f"{ac}/4" + (f" — found {', '.join(parts)}" if parts else " — not detected")

    # 2.4 Training loop
    has_loop = bool(re.search(
        r'(?:for\s+\w+\s+in\s+range|while\s+.*(?:step|timestep|episode))',
        code, re.I
    ))
    has_env_step = ".step(" in code
    tl = 0
    if has_loop and has_env_step:
        tl = 3
    elif has_loop or has_env_step:
        tl = 1
    score += tl
    details["2.4 Training loop"] = f"{tl}/3"

    return score, details


# ============================================================================
# Dimension 3: PPO Core Mechanisms (35 pts)
# ============================================================================

def _dim3_ppo_core(code: Optional[str]) -> Tuple[int, Dict[str, str]]:
    """
    3.1 Probability ratio              (7 pts)
    3.2 Clipped Surrogate              (8 pts)
    3.3 Advantage / GAE                (7 pts)
    3.4 Multi-epoch updates            (6 pts)
    3.5 Value Function Loss            (4 pts)
    3.6 Entropy Bonus / Regularization (3 pts)
    """
    if code is None:
        return 0, {"error": "0/35 — no code"}

    score = 0
    details: Dict[str, str] = {}

    # ---- 3.1 ratio (7) ----
    has_ratio_exp = bool(re.search(r'ratio\s*=\s*.*(?:exp|torch\.exp)', code, re.I))
    has_log_diff = bool(re.search(
        r'(?:new_log|log_prob|logprob)\w*\s*-\s*(?:old_log|log_prob|logprob)|log_ratio',
        code, re.I
    ))
    has_old_logp = bool(re.search(r'old_log_prob|old_logprob|mb_old_logprob|b_logprob', code, re.I))

    r_pts = 0
    if has_ratio_exp and (has_log_diff or has_old_logp):
        r_pts = 7
    elif has_ratio_exp:
        r_pts = 4
    elif has_old_logp or has_log_diff:
        r_pts = 2
    score += r_pts
    details["3.1 Probability ratio"] = f"{r_pts}/7"

    # ---- 3.2 Clipped Surrogate (8) ----
    has_clamp = bool(re.search(
        r'(?:torch\.)?clamp\s*\(\s*ratio.*(?:1\s*[-+]|clip|epsilon)',
        code, re.I
    ))
    has_clip_fn = bool(re.search(r'(?:torch\.)?clip\s*\(\s*ratio', code, re.I))
    has_min_surr = bool(re.search(
        r'(?:torch\.)?min\s*\(.*(?:surr|clip|unclip|ratio.*adv)',
        code, re.I
    ))
    has_surr_terms = bool(re.search(
        r'ratio\s*\*\s*(?:adv|advantage|mb_adv)|'
        r'(?:adv|advantage|mb_adv)\s*\*\s*ratio|'
        r'surr1|surr2|clipped_ratio|ratio_clipped',
        code, re.I
    ))

    c_pts = 0
    if (has_clamp or has_clip_fn) and has_min_surr and has_surr_terms:
        c_pts = 8
    elif (has_clamp or has_clip_fn) and has_surr_terms:
        c_pts = 6
    elif has_clamp or has_clip_fn:
        c_pts = 4
    elif has_surr_terms:
        c_pts = 2
    score += c_pts
    details["3.2 Clipped Surrogate"] = f"{c_pts}/8"

    # ---- 3.3 Advantage / GAE (7) ----
    has_gae = bool(re.search(r'gae|generalized.*advantage', code, re.I))
    has_adv_idx = bool(re.search(r'(?:advantage|adv)\s*[\[\(]', code, re.I))
    has_td = bool(re.search(r'(?:delta|td_error)\s*=\s*.*reward', code, re.I))
    has_gamma_lam = bool(re.search(r'gamma.*lambda|gae_lambda|lam\s*=', code, re.I))
    has_adv_norm = bool(re.search(r'(?:advantage|adv).*(?:mean|std|normalize)', code, re.I))

    g_pts = 0
    if has_gae and (has_td or has_adv_idx) and has_gamma_lam:
        g_pts = 7
    elif (has_td or has_adv_idx) and has_adv_norm:
        g_pts = 5
    elif has_td or has_adv_idx:
        g_pts = 3
    elif has_gamma_lam:
        g_pts = 2
    score += g_pts
    details["3.3 Advantage/GAE"] = f"{g_pts}/7"

    # ---- 3.4 Multi-epoch (6) ----
    has_epoch_loop = bool(re.search(
        r'for\s+\w+\s+in\s+range\s*\(\s*(?:\w*epochs?\w*|K_epochs|update_epochs|n_epochs|ppo_epochs)',
        code, re.I
    ))
    has_epoch_param = bool(re.search(
        r'(?:update_epochs|n_epochs|ppo_epochs|K_epochs|num_epochs)\s*[=:]\s*\d+',
        code, re.I
    ))
    has_mb = bool(re.search(r'minibatch|mini_batch|mb_', code, re.I))

    e_pts = 0
    if has_epoch_loop and has_mb:
        e_pts = 6
    elif has_epoch_loop or (has_epoch_param and has_mb):
        e_pts = 4
    elif has_epoch_param:
        e_pts = 2
    score += e_pts
    details["3.4 Multi-epoch"] = f"{e_pts}/6"

    # ---- 3.5 Value Loss (4) ----
    has_vloss = bool(re.search(r'v_loss|value_loss|critic_loss', code, re.I))
    has_vpred = bool(re.search(r'v_pred|value_pred|new_value|pred_value|newvalue', code, re.I))

    v_pts = 0
    if has_vloss and has_vpred:
        v_pts = 4
    elif has_vloss:
        v_pts = 2
    score += v_pts
    details["3.5 Value Loss"] = f"{v_pts}/4"

    # ---- 3.6 Entropy (3) ----
    has_entropy = bool(re.search(r'entropy|ent_coef|ent_bonus|entropy_loss', code, re.I))
    has_combined = bool(re.search(
        r'loss\s*=.*(?:pg_loss|policy_loss|actor_loss).*(?:v_loss|value_loss|vf)',
        code, re.I
    ))

    en_pts = 0
    if has_entropy and has_combined:
        en_pts = 3
    elif has_entropy:
        en_pts = 2
    elif has_combined:
        en_pts = 1
    score += en_pts
    details["3.6 Entropy/Regularization"] = f"{en_pts}/3"

    return score, details


# ============================================================================
# Dimension 4: Continuous Action Space Handling (10 pts)
# ============================================================================

def _dim4_continuous_action(code: Optional[str]) -> Tuple[int, Dict[str, str]]:
    """
    4.1 Gaussian (Normal) distribution  (4 pts)
    4.2 Actor outputs mu / sigma        (3 pts)
    4.3 Action space boundary handling   (3 pts)
    """
    if code is None:
        return 0, {"error": "0/10 — no code"}

    score = 0
    details: Dict[str, str] = {}

    # 4.1 Normal distribution + sample
    has_normal = bool(re.search(r'Normal|MultivariateNormal', code))
    has_sample = bool(re.search(r'\.sample\(|\.rsample\(', code))

    d_pts = 0
    if has_normal and has_sample:
        d_pts = 4
    elif has_normal:
        d_pts = 3
    elif has_sample:
        d_pts = 1
    score += d_pts
    details["4.1 Gaussian distribution"] = f"{d_pts}/4"

    # 4.2 mu + sigma/std
    has_mu = bool(re.search(r'(?:mu|mean|action_mean)(?:\s|_)', code, re.I))
    has_sigma = bool(re.search(r'(?:sigma|std|log_std|log_sigma|action_std)', code, re.I))

    ms_pts = 0
    if has_mu and has_sigma:
        ms_pts = 3
    elif has_mu or has_sigma:
        ms_pts = 1
    score += ms_pts
    details["4.2 mu/sigma"] = f"{ms_pts}/3"

    # 4.3 Action boundaries
    has_clip_action = bool(re.search(
        r'(?:clamp|clip).*(?:action|act).*(?:-?2|low|high)|'
        r'(?:action|act).*(?:clamp|clip)|'
        r'tanh.*(?:action_scale|act_limit)',
        code, re.I
    ))
    has_tanh = bool(re.search(r'TanhTransform|torch\.tanh|\.tanh\(\)', code))
    has_pendulum = bool(re.search(r'[Pp]endulum', code))

    b_pts = 0
    if (has_clip_action or has_tanh) and has_pendulum:
        b_pts = 3
    elif has_clip_action or has_tanh:
        b_pts = 2
    elif has_pendulum:
        b_pts = 1
    score += b_pts
    details["4.3 Action boundaries"] = f"{b_pts}/3"

    return score, details


# ============================================================================
# Dimension 5: Training Performance (30 pts)
# ============================================================================

def _extract_episode_rewards(text: str) -> List[float]:
    """Extract episode-level reward/return values from log text"""
    rewards: List[float] = []
    patterns = [
        r'return[=:\s]+(-?\d+\.?\d*)',
        r'reward[=:\s]+(-?\d+\.?\d*)',
        r'AvgReturn[=:\s]+(-?\d+\.?\d*)',
        r'avg_return[=:\s]+(-?\d+\.?\d*)',
        r'ep_reward[=:\s]+(-?\d+\.?\d*)',
        r'episode_reward[=:\s]+(-?\d+\.?\d*)',
    ]
    for pat in patterns:
        found = re.findall(pat, text, re.I)
        if found:
            for v in found:
                try:
                    rewards.append(float(v))
                except ValueError:
                    pass
            break  # Use the first matched pattern to avoid double counting
    return rewards


def _extract_final_eval(text: str) -> Optional[float]:
    """Extract the average return from the final 5-episode evaluation"""
    pats = [
        r'[Ff]inal\s+[Ee]valuation.*?average\s+return\s*[=:]\s*(-?\d+\.?\d*)',
        r'[Ee]valuation\s+over\s+\d+\s+episodes.*?[Aa]verage\s+[Rr]eturn\s*[=:]\s*(-?\d+\.?\d*)',
        r'[Ee]val.*?[Aa]vg.*?[Rr]eturn\s*[=:]\s*(-?\d+\.?\d*)',
        r'[Ff]inal.*?[Rr]eward\s*[=:]\s*(-?\d+\.?\d*)',
        r'[Aa]verage\s+[Rr]eturn\s*=\s*(-?\d+\.?\d*)',
    ]
    for pat in pats:
        m = re.search(pat, text)
        if m:
            try:
                return float(m.group(1))
            except ValueError:
                pass
    return None


def _dim5_performance(answer_dir: str, code: Optional[str]) -> Tuple[int, Dict[str, str]]:
    """
    5.1 Log shows training progress  (10 pts)
    5.2 Final evaluation performance  (20 pts)
    """
    score = 0
    details: Dict[str, str] = {}

    log_text = _collect_log_content(answer_dir)
    rewards = _extract_episode_rewards(log_text)

    # ---- 5.1 Training progress (10) ----
    if len(rewards) >= 20:
        q = max(1, len(rewards) // 4)
        avg_first = sum(rewards[:q]) / q
        avg_last = sum(rewards[-q:]) / q
        if avg_last > avg_first:
            score += 10
            details["5.1 Training progress"] = (
                f"10/10 — {len(rewards)} entries, "
                f"early {avg_first:.1f} -> late {avg_last:.1f} (improved)"
            )
        else:
            score += 6
            details["5.1 Training progress"] = (
                f"6/10 — {len(rewards)} entries, "
                f"early {avg_first:.1f} -> late {avg_last:.1f} (no clear improvement)"
            )
    elif len(rewards) >= 5:
        score += 5
        details["5.1 Training progress"] = f"5/10 — only {len(rewards)} entries"
    elif log_text.strip():
        score += 2
        details["5.1 Training progress"] = "2/10 — log exists but very few reward records"
    else:
        details["5.1 Training progress"] = "0/10 — no training log"

    # ---- 5.2 Final evaluation (20) ----
    final_eval = _extract_final_eval(log_text)

    if final_eval is not None:
        perf = _score_from_return(final_eval, exact=True)
        score += perf
        details["5.2 Final evaluation"] = f"{perf}/20 — return={final_eval:.2f}"
    else:
        # Infer from tail rewards in log
        if rewards:
            tail = rewards[-5:] if len(rewards) >= 5 else rewards
            avg_tail = sum(tail) / len(tail)
            # Inferred score capped at 15 (less reliable than explicit eval)
            perf = min(15, _score_from_return(avg_tail, exact=False))
            score += perf
            details["5.2 Final evaluation"] = (
                f"{perf}/20 — no explicit eval, tail {len(tail)} entries avg {avg_tail:.2f} (inferred)"
            )
        else:
            # LLM fallback
            if code:
                llm_perf = _llm_estimate_perf(code, answer_dir)
                score += llm_perf
                details["5.2 Final evaluation"] = f"{llm_perf}/20 — no log, LLM code quality estimate"
            else:
                details["5.2 Final evaluation"] = "0/20 — no code or log"

    return score, details


def _score_from_return(avg_return: float, exact: bool) -> int:
    """Map average return to a score"""
    if avg_return > -350:
        return 20
    elif avg_return > -500:
        return 15
    elif avg_return > -800:
        return 10
    elif avg_return > -1200:
        return 5
    else:
        return 2 if exact else 1


def _llm_estimate_perf(code: str, answer_dir: str) -> int:
    """When no log is available, use LLM to estimate potential performance from code"""
    snippet = code[:6000]
    prompt = (
        "You are a reinforcement learning expert. Please evaluate the potential performance "
        "of the following PPO implementation on Pendulum-v1.\n\n"
        f"```python\n{snippet}\n```\n\n"
        "Score 0-20:\n"
        "18-20: Complete and correct, expected avg return > -350\n"
        "13-17: Mostly correct, expected -350~-600\n"
        "8-12: Has deficiencies, expected -600~-1000\n"
        "3-7: Incomplete\n"
        "0-2: Poor quality\n\n"
        "Reply strictly in JSON: {\"score\": 0, \"reason\": \"\"}"
    )
    config = _get_text_eval_config(answer_dir)
    raw = _call_llm_judge(prompt, config)
    if not raw:
        return 0
    try:
        text = raw
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        data = json.loads(text)
        return max(0, min(20, int(data.get("score", 0))))
    except (json.JSONDecodeError, ValueError, TypeError):
        m = re.search(r'"score"\s*:\s*(\d+)', raw)
        if m:
            return max(0, min(20, int(m.group(1))))
        return 0


# ============================================================================
# Entry Point
# ============================================================================

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """Evaluate PPO Pendulum-v1 implementation, returns (0-100 score, report)."""
    py_path = _find_main_py(answer_dir)
    code = _read_file(py_path) if py_path else None

    s1, d1 = _dim1_file_delivery(answer_dir)
    s2, d2 = _dim2_code_structure(code)
    s3, d3 = _dim3_ppo_core(code)
    s4, d4 = _dim4_continuous_action(code)
    s5, d5 = _dim5_performance(answer_dir, code)

    total = s1 + s2 + s3 + s4 + s5

    if total >= 85:
        verdict = "Excellent — PPO implementation is complete and training performance meets the target."
    elif total >= 70:
        verdict = "Good — core functionality is correct, with room for improvement in some dimensions."
    elif total >= 50:
        verdict = "Passing — basic PPO implemented, but with notable deficiencies."
    elif total >= 30:
        verdict = "Partially complete — core mechanisms or performance have significant issues."
    else:
        verdict = "Failing — task completion is severely insufficient."

    report: Dict[str, Any] = {
        "total_score": total,
        "section_scores": {
            "1. File Delivery": f"{s1}/10",
            "2. Code Structure": f"{s2}/15",
            "3. PPO Core Mechanisms": f"{s3}/35",
            "4. Continuous Action Space": f"{s4}/10",
            "5. Training Performance": f"{s5}/30",
        },
        "details": {
            "1. File Delivery (10)": d1,
            "2. Code Syntax & Structure (15)": d2,
            "3. PPO Core Mechanisms (35)": d3,
            "4. Continuous Action Space Handling (10)": d4,
            "5. Training Performance (30)": d5,
        },
        "verdict": verdict,
    }
    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print formatted scoring report."""
    sep = "=" * 65
    thin = "-" * 50
    print(sep)
    print("PPO Pendulum-v1 Scoring Report")
    print(sep)
    print(f"\nTotal Score: {score}/100\n")

    for k, v in report.get("section_scores", {}).items():
        print(f"  {k}: {v}")

    for section, items in report.get("details", {}).items():
        print(f"\n{thin}")
        print(f"  [{section}]")
        print(thin)
        if isinstance(items, dict):
            for k, v in items.items():
                print(f"    {k}: {v}")

    print(f"\n{sep}")
    print(f"Verdict: {report.get('verdict', '')}")
    print(sep)


# ============================================================================
# CLI
# ============================================================================

if __name__ == "__main__":
    test_dir = (
        sys.argv[1]
        if len(sys.argv) > 1
        else os.path.join(os.path.dirname(__file__), "..", "gpt-5", "attempt_1")
    )
    if os.path.exists(test_dir):
        print(f"Evaluating directory: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"Directory does not exist: {test_dir}")
    sys.exit(0)
