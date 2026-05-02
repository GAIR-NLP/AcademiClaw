"""
Speculative Decoding Inference Engine Implementation — Scoring Script (rubric.py)

Total 100 points, divided into five dimensions:

I.   File Delivery (10 points)
     1.1 inference.py exists and is non-empty (5)
     1.2 benchmark_report.md exists and is non-empty (5)

II.  Code Structure & Imports (15 points)
     2.1 inference.py syntax is correct and parseable (3)
     2.2 Contains baseline/autoregressive sampling function (3)
     2.3 Contains speculative / spec_decod related function (3)
     2.4 Speculative function signature contains target_model, draft_model, prompt (3)
     2.5 Imports gpt_lite module (GPTLite / GPTConfig) (3)

III. Algorithm Correctness — Static Code Analysis (30 points)
     3.1 Stochastic sampling logic (multinomial / torch.rand) (5)
     3.2 Rejection Sampling accept/reject logic (p_target/p_draft ratio + uniform comparison) (7)
     3.3 Corrected distribution (Residual Distribution) resampling (max(0,p_t-p_d) normalized then sampled) (7)
     3.4 KV-Cache rollback/slice operations (zero-copy view) (6)
     3.5 Temperature handling (including T=0 degeneration to greedy / argmax) (5)

IV.  Benchmark Report Quality (15 points)
     4.1 Markdown format + headings + tables (3)
     4.2 Multiple Temperature comparison data (>=2 groups) (4)
     4.3 Speedup ratio values (4)
     4.4 Analysis and explanation text (4)

V.   LLM-as-Judge Deep Review (30 points)
     5.1 Algorithm correctness (0-12)
     5.2 Engineering implementation quality (0-10)
     5.3 Completeness and robustness (0-8)
"""

import os
import re
import ast
import json
import traceback
from typing import Tuple, Dict, Any, List

try:
    import openai
except ImportError:
    openai = None


# --------------------------------------------------------------------------
# Environment Configuration
# --------------------------------------------------------------------------

def _load_env(answer_dir: str) -> dict:
    """Load .env configuration from answer_dir and query root directory"""
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


# --------------------------------------------------------------------------
# Utility Functions
# --------------------------------------------------------------------------

def _read_file(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


def _find_file(answer_dir: str, filename: str) -> str:
    """Find a file in answer_dir (directly or one subdirectory level)"""
    direct = os.path.join(answer_dir, filename)
    if os.path.isfile(direct):
        return direct
    if os.path.isdir(answer_dir):
        for item in os.listdir(answer_dir):
            sub = os.path.join(answer_dir, item)
            if os.path.isdir(sub):
                candidate = os.path.join(sub, filename)
                if os.path.isfile(candidate):
                    return candidate
    return ""


# --------------------------------------------------------------------------
# I. File Delivery (10 points)
# --------------------------------------------------------------------------

def _check_files(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details: Dict[str, str] = {}

    # 1.1 inference.py (5)
    inf_path = _find_file(answer_dir, "inference.py")
    if inf_path:
        sz = os.path.getsize(inf_path)
        if sz >= 500:
            score += 5
            details["1.1 inference.py"] = f"5/5 — Exists ({sz} bytes)"
        elif sz > 0:
            score += 2
            details["1.1 inference.py"] = f"2/5 — Exists but too short ({sz} bytes)"
        else:
            details["1.1 inference.py"] = "0/5 — File is empty"
    else:
        details["1.1 inference.py"] = "0/5 — Does not exist"

    # 1.2 benchmark_report.md (5)
    rpt_path = _find_file(answer_dir, "benchmark_report.md")
    if rpt_path:
        sz = os.path.getsize(rpt_path)
        if sz >= 100:
            score += 5
            details["1.2 benchmark_report.md"] = f"5/5 — Exists ({sz} bytes)"
        elif sz > 0:
            score += 2
            details["1.2 benchmark_report.md"] = f"2/5 — Exists but too short ({sz} bytes)"
        else:
            details["1.2 benchmark_report.md"] = "0/5 — File is empty"
    else:
        details["1.2 benchmark_report.md"] = "0/5 — Does not exist"

    return score, details


# --------------------------------------------------------------------------
# II. Code Structure & Imports (15 points)
# --------------------------------------------------------------------------

def _check_structure(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details: Dict[str, str] = {}

    inf_path = _find_file(answer_dir, "inference.py")
    if not inf_path:
        return 0, {"error": "inference.py does not exist, skipping code structure check"}

    code = _read_file(inf_path)
    if not code.strip():
        return 0, {"error": "inference.py is empty"}

    # 2.1 Syntax correct (3)
    try:
        tree = ast.parse(code)
        score += 3
        details["2.1 Syntax correct"] = "3/3"
    except SyntaxError as e:
        details["2.1 Syntax correct"] = f"0/3 — SyntaxError: {str(e)[:80]}"
        return score, details

    # Collect function names
    func_names: List[str] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            func_names.append(node.name)
    fn_lower = [n.lower() for n in func_names]

    # 2.2 Baseline function (3)
    baseline_kw = ["autoregressive", "baseline", "greedy_sampling", "greedy_generate"]
    has_baseline = any(any(k in fn for k in baseline_kw) for fn in fn_lower)
    if has_baseline:
        score += 3
        details["2.2 Baseline function"] = "3/3"
    else:
        details["2.2 Baseline function"] = "0/3 — No baseline/autoregressive function found"

    # 2.3 Speculative function (3)
    spec_kw = ["speculative", "spec_decod", "spec_sample"]
    has_spec = any(any(k in fn for k in spec_kw) for fn in fn_lower)
    if has_spec:
        score += 3
        details["2.3 Speculative function"] = "3/3"
    else:
        details["2.3 Speculative function"] = "0/3 — No speculative-related function found"

    # 2.4 Speculative function signature (3)
    sig_score = 0
    if has_spec:
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if any(k in node.name.lower() for k in spec_kw):
                    arg_names = " ".join(a.arg for a in node.args.args).lower()
                    has_target = any(x in arg_names for x in ["target", "main", "large"])
                    has_draft = any(x in arg_names for x in ["draft", "small", "approx"])
                    has_prompt = any(x in arg_names for x in ["prompt", "input", "idx", "tokens", "prefix"])
                    cnt = sum([has_target, has_draft, has_prompt])
                    if cnt >= 3:
                        sig_score = 3
                    elif cnt >= 2:
                        sig_score = 2
                    else:
                        sig_score = 1
                    break
    score += sig_score
    details["2.4 Function signature"] = f"{sig_score}/3"

    # 2.5 Import gpt_lite (3)
    has_import = bool(re.search(r'(?:from|import)\s+.*gpt_lite', code))
    has_class = "GPTLite" in code or "GPTConfig" in code
    if has_import and has_class:
        score += 3
        details["2.5 GPTLite import"] = "3/3"
    elif has_import or has_class:
        score += 2
        details["2.5 GPTLite import"] = "2/3 — Partial import"
    else:
        details["2.5 GPTLite import"] = "0/3"

    return score, details


# --------------------------------------------------------------------------
# III. Algorithm Correctness — Static Code Analysis (30 points)
# --------------------------------------------------------------------------

def _check_algorithm(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details: Dict[str, str] = {}

    inf_path = _find_file(answer_dir, "inference.py")
    if not inf_path:
        return 0, {"error": "inference.py does not exist"}

    code = _read_file(inf_path)
    if not code.strip():
        return 0, {"error": "inference.py is empty"}

    try:
        ast.parse(code)
    except SyntaxError:
        return 0, {"error": "inference.py has syntax errors, cannot analyze algorithm"}

    # -- 3.1 Stochastic sampling logic (5) --
    has_multinomial = "multinomial" in code
    has_rand = bool(re.search(r'torch\.rand\b', code))
    if has_multinomial and has_rand:
        s = 5
    elif has_multinomial:
        s = 4
    elif has_rand:
        s = 2
    else:
        s = 0
    score += s
    details["3.1 Stochastic sampling (5)"] = f"{s}/5"

    # -- 3.2 Rejection Sampling accept/reject logic (7) --
    # Key patterns: p_target / p_draft ratio, accept/reject judgment, uniform < ratio
    has_ratio = bool(re.search(
        r'p.*target.*\/.*p.*draft|p_t.*\/.*p_d|target.*prob.*\/.*draft.*prob|'
        r'ratio\b|alpha\b.*=.*p.*\/.*p|accept.*prob',
        code, re.IGNORECASE
    ))
    has_accept_reject = bool(re.search(r'accept|reject', code, re.IGNORECASE))
    has_uniform_cmp = bool(re.search(
        r'(?:torch\.rand|uniform)\s*\(.*\).*(?:<|<=|>|>=)|'
        r'(?:u|r)\s*(?:<|<=|>|>=)\s*(?:alpha|ratio|accept)',
        code, re.IGNORECASE
    ))
    # Also check for the classic pattern: p_d <= p_t (unconditional accept)
    has_unconditional_accept = bool(re.search(
        r'p.*d.*<=\s*p.*t|p_draft.*<=.*p_target|p.*target.*>=.*p.*draft',
        code, re.IGNORECASE
    ))

    rj = 0
    if has_ratio and has_accept_reject and (has_uniform_cmp or has_unconditional_accept):
        rj = 7
    elif has_ratio and has_accept_reject:
        rj = 5
    elif has_accept_reject and (has_ratio or has_uniform_cmp or has_unconditional_accept):
        rj = 4
    elif has_accept_reject:
        rj = 2
    score += rj
    details["3.2 Rejection Sampling (7)"] = f"{rj}/7"

    # -- 3.3 Corrected distribution (Residual Distribution) resampling (7) --
    # Core: max(0, p_t - p_d) or torch.clamp(..., min=0) -> normalize -> sample
    has_residual_keyword = bool(re.search(
        r'residual|corrected|adjusted|normed.*diff|difference.*dist',
        code, re.IGNORECASE
    ))
    has_prob_subtract = bool(re.search(
        r'p.*target.*-.*p.*draft|p_t.*-.*p_d|target.*prob.*-.*draft.*prob|'
        r'p.*-.*min.*vec|p.*-.*torch\.minimum',
        code, re.IGNORECASE
    ))
    has_clamp_relu = bool(re.search(
        r'clamp.*min.*0|torch\.clamp\(.*min\s*=\s*0|F\.relu|'
        r'torch\.maximum.*0|max\(.*0',
        code, re.IGNORECASE
    ))
    has_renormalize = bool(re.search(
        r'\.sum\(\)|normalize|\/\s*(?:residual|mass|total|norm)',
        code, re.IGNORECASE
    ))

    rd = 0
    if (has_residual_keyword or has_prob_subtract) and (has_clamp_relu or has_renormalize):
        rd = 7
    elif has_prob_subtract and has_renormalize:
        rd = 7
    elif has_residual_keyword or has_prob_subtract:
        rd = 4
    elif has_clamp_relu:
        rd = 2
    score += rd
    details["3.3 Corrected distribution resampling (7)"] = f"{rd}/7"

    # -- 3.4 KV-Cache rollback/slice (6) --
    has_kv_cache = bool(re.search(
        r'kv.*cache|past.*key.*value|past_kv|key_values|kv_cache',
        code, re.IGNORECASE
    ))
    has_rollback = bool(re.search(
        r'rollback|roll.*back|truncat|revert|restore|_kv_slice|kv_slice',
        code, re.IGNORECASE
    ))
    # Tensor slicing patterns like k[:, :, :new_len, :]
    has_tensor_slice = bool(re.search(
        r'\[\s*:\s*,\s*:\s*,\s*:.*(?:len|pos|idx|count|total)',
        code, re.IGNORECASE
    ))
    has_zero_copy = bool(re.search(
        r'zero.*copy|view|narrow',
        code, re.IGNORECASE
    ))

    kv = 0
    if has_kv_cache and (has_rollback or has_tensor_slice) and (has_tensor_slice or has_zero_copy):
        kv = 6
    elif has_kv_cache and (has_rollback or has_tensor_slice):
        kv = 5
    elif has_kv_cache:
        kv = 2
    score += kv
    details["3.4 KV-Cache rollback (6)"] = f"{kv}/6"

    # -- 3.5 Temperature handling (5) --
    has_temp_param = bool(re.search(r'temperature|temp\b', code, re.IGNORECASE))
    has_temp_zero = bool(re.search(
        r'temperature\s*(?:==|<=|<|is)\s*0|temp\s*(?:==|<=|<)\s*0|argmax',
        code, re.IGNORECASE
    ))
    has_temp_divide = bool(re.search(
        r'logits?\s*\/\s*(?:temperature|temp)|'
        r'softmax.*(?:temperature|temp)|'
        r'\/\s*temperature',
        code, re.IGNORECASE
    ))

    tp = 0
    if has_temp_param and has_temp_zero and has_temp_divide:
        tp = 5
    elif has_temp_param and (has_temp_zero or has_temp_divide):
        tp = 3
    elif has_temp_param:
        tp = 1
    score += tp
    details["3.5 Temperature handling (5)"] = f"{tp}/5"

    return score, details


# --------------------------------------------------------------------------
# IV. Benchmark Report Quality (15 points)
# --------------------------------------------------------------------------

def _check_report(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details: Dict[str, str] = {}

    rpt_path = _find_file(answer_dir, "benchmark_report.md")
    if not rpt_path:
        return 0, {"error": "benchmark_report.md does not exist"}

    content = _read_file(rpt_path)
    if not content.strip():
        return 0, {"error": "benchmark_report.md is empty"}

    # 4.1 Format (3)
    has_header = bool(re.search(r'^#+\s', content, re.MULTILINE))
    has_table = "|" in content and "---" in content
    has_length = len(content) > 200
    fmt = 0
    if has_header and has_table and has_length:
        fmt = 3
    elif has_header and (has_table or has_length):
        fmt = 2
    elif has_header or has_table:
        fmt = 1
    score += fmt
    details["4.1 Format (3)"] = f"{fmt}/3"

    # 4.2 Multiple Temperature comparisons (4)
    temp_vals = set()
    for m in re.finditer(r'(?:temperature|temp)\s*[=:]\s*([\d.]+)', content, re.IGNORECASE):
        try:
            temp_vals.add(float(m.group(1)))
        except ValueError:
            pass
    # Also look in table rows: | 0.80 | ... |
    for m in re.finditer(r'\|\s*([\d]+\.[\d]+)\s*\|', content):
        try:
            v = float(m.group(1))
            if 0 <= v <= 2.0:
                temp_vals.add(v)
        except ValueError:
            pass

    n = len(temp_vals)
    td = 0
    if n >= 3:
        td = 4
    elif n >= 2:
        td = 3
    elif n >= 1:
        td = 1
    score += td
    details["4.2 Temperature comparison (4)"] = f"{td}/4 — Found {n} temperature values"

    # 4.3 Speedup metrics (4)
    has_speedup_kw = bool(re.search(r'speed\s*up|speedup', content, re.IGNORECASE))
    has_numeric = bool(re.search(r'\d+\.\d+x', content))
    has_time = bool(re.search(r'\d+\.\d+\s*s|time|latency', content, re.IGNORECASE))
    has_table_num = bool(re.search(r'\|\s*\d+\.\d+\s*\|', content))

    sp = 0
    if has_speedup_kw and (has_numeric or has_table_num) and has_time:
        sp = 4
    elif has_speedup_kw and (has_numeric or has_table_num):
        sp = 3
    elif has_speedup_kw or has_time:
        sp = 1
    score += sp
    details["4.3 Speedup metrics (4)"] = f"{sp}/4"

    # 4.4 Analysis and explanation (4)
    has_section = bool(re.search(
        r'##\s*(?:notes|analysis|discussion|conclusion)',
        content, re.IGNORECASE
    ))
    has_technical = bool(re.search(
        r'rejection.*sampling|speculative|kv.*cache|parallel.*verif',
        content, re.IGNORECASE
    ))
    text_lines = [l for l in content.split("\n")
                  if l.strip() and not l.strip().startswith("|") and not l.strip().startswith("#")]
    has_text = len(text_lines) >= 3

    an = 0
    if has_section and has_technical and has_text:
        an = 4
    elif has_technical and has_text:
        an = 3
    elif has_technical or has_text:
        an = 2
    elif len(content) > 300:
        an = 1
    score += an
    details["4.4 Analysis and explanation (4)"] = f"{an}/4"

    return score, details


# --------------------------------------------------------------------------
# V. LLM-as-Judge Deep Review (30 points)
# --------------------------------------------------------------------------

_LLM_PROMPT_TEMPLATE = """\
You are a strict code review expert specializing in evaluating the implementation quality of \
Speculative Decoding inference engines.

Below is an agent's submitted inference.py implementation code. The task requirements are:
1. Implement a speculative inference engine supporting stochastic sampling (Temperature > 0)
2. Implement standard Rejection Sampling logic (lossless guarantee that the final distribution matches the Target Model)
   - When p_draft(x) <= p_target(x), accept unconditionally
   - When p_draft(x) > p_target(x), accept with probability p_target(x)/p_draft(x)
   - Upon rejection, resample from the corrected distribution max(0, p_target - p_draft) after normalization
3. Implement efficient KV-Cache rollback (zero-copy, using slice view operations, not using torch.cat reallocation)
4. Include both Baseline (autoregressive sampling) and Speculative Decoding implementations
5. Target Model verifies all Draft Tokens in parallel (single forward pass computing probabilities for all draft tokens)
6. Handle both temperature=0 (degenerates to greedy) and temperature>0 (stochastic sampling) modes

Please strictly evaluate the code quality on the following three dimensions (integer scores):

**Dimension 1: Algorithm Correctness (0-12 points)**
- 11-12: Rejection Sampling logic fully correct: includes p_target/p_draft acceptance probability calculation, \
uniform random number comparison, resampling from corrected distribution (residual/normed difference distribution) \
upon rejection. Mathematically guarantees lossless distribution.
- 8-10: Basically correct but with minor flaws (e.g., corrected distribution normalization not rigorous enough, \
boundary case handling not complete)
- 4-7: Partially correct, with obvious algorithm defects (e.g., missing corrected distribution resampling, \
or acceptance probability calculation errors)
- 0-3: Algorithm logic seriously wrong or missing

**Dimension 2: Engineering Implementation Quality (0-10 points)**
- 9-10: KV-Cache zero-copy rollback (through tensor slicing [:, :, :len, :] rather than torch.cat), \
Target single forward pass parallel verification of all draft tokens, clear modular code structure
- 6-8: Basically correct but efficiency not optimal (e.g., uses torch.cat reallocation instead of slice views)
- 3-5: Rough implementation, redundant memory operations or serial verification
- 0-2: Engineering implementation missing or completely wrong

**Dimension 3: Completeness and Robustness (0-8 points)**
- 7-8: Handles both temperature=0 (greedy/argmax) and temperature>0 (stochastic), supports gamma parameter, \
handles boundary cases like sequence end, both Baseline and Speculative are complete and runnable
- 4-6: Basically complete but missing some boundary handling
- 0-3: Implementation incomplete, missing Baseline or key parameter handling

Please reply strictly in the following JSON format (do not include anything else):
```json
{{
  "algorithm_correctness": {{"score": 0, "reason": ""}},
  "engineering_quality": {{"score": 0, "reason": ""}},
  "completeness": {{"score": 0, "reason": ""}},
  "total": 0,
  "overall_comment": ""
}}
```

--- Below is the submitted code ---

{code}
"""


def _check_llm_review(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details: Dict[str, str] = {}

    inf_path = _find_file(answer_dir, "inference.py")
    if not inf_path:
        return 0, {"error": "inference.py does not exist, cannot perform LLM review"}

    code = _read_file(inf_path)
    if not code.strip():
        return 0, {"error": "inference.py is empty"}

    # Truncate overly long code
    if len(code) > 15000:
        code_trimmed = code[:15000] + "\n... (code truncated, total {} characters)".format(len(code))
    else:
        code_trimmed = code

    config = _get_text_eval_config(answer_dir)
    prompt = _LLM_PROMPT_TEMPLATE.format(code=code_trimmed)
    raw = _call_llm_judge(prompt, config)

    if not raw:
        score = 10
        details["LLM review"] = "10/30 — LLM unavailable, giving conservative score"
        return score, details

    try:
        text = raw
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()

        result = json.loads(text)

        algo = result.get("algorithm_correctness", {})
        eng = result.get("engineering_quality", {})
        comp = result.get("completeness", {})

        algo_s = max(0, min(12, int(algo.get("score", 0))))
        eng_s = max(0, min(10, int(eng.get("score", 0))))
        comp_s = max(0, min(8, int(comp.get("score", 0))))

        score = algo_s + eng_s + comp_s

        details["5.1 Algorithm correctness (12)"] = f"{algo_s}/12 — {algo.get('reason', '')}"
        details["5.2 Engineering quality (10)"] = f"{eng_s}/10 — {eng.get('reason', '')}"
        details["5.3 Completeness and robustness (8)"] = f"{comp_s}/8 — {comp.get('reason', '')}"
        details["Overall comment"] = result.get("overall_comment", "")
        details["Evaluation model"] = config.get("model", "unknown")

    except (json.JSONDecodeError, Exception) as e:
        print(f"[RUBRIC] LLM response parsing failed: {e}")
        print(f"[RUBRIC] Raw response: {raw[:500]}")
        score = 10
        details["LLM review"] = "10/30 — LLM response parsing failed, giving conservative score"
        details["raw_response"] = raw[:300]

    return score, details


# --------------------------------------------------------------------------
# Entry Function
# --------------------------------------------------------------------------

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
    s1, r1 = _check_files(answer_dir)
    s2, r2 = _check_structure(answer_dir)
    s3, r3 = _check_algorithm(answer_dir)
    s4, r4 = _check_report(answer_dir)
    s5, r5 = _check_llm_review(answer_dir)

    total = max(0, min(100, s1 + s2 + s3 + s4 + s5))

    report: Dict[str, Any] = {
        "total_score": total,
        "result_scores": {
            "score": s1 + s4,
            "details": {
                "I. File Delivery (10pts)": r1,
                "IV. Report Quality (15pts)": r4,
            },
        },
        "process_scores": {
            "score": s2 + s3 + s5,
            "details": {
                "II. Code Structure (15pts)": r2,
                "III. Algorithm Correctness (30pts)": r3,
                "V. LLM Review (30pts)": r5,
            },
        },
        "dimension_scores": {
            "File Delivery": f"{s1}/10",
            "Code Structure": f"{s2}/15",
            "Algorithm Correctness": f"{s3}/30",
            "Report Quality": f"{s4}/15",
            "LLM Review": f"{s5}/30",
        },
        "comment": "",
    }

    if total >= 90:
        report["comment"] = "Excellent! Speculative decoding engine implementation is complete, algorithm is correct, engineering quality is high."
    elif total >= 75:
        report["comment"] = "Good. Core algorithm is basically correct, with room for improvement."
    elif total >= 60:
        report["comment"] = "Passing. Basic functionality implemented but with notable deficiencies."
    elif total >= 40:
        report["comment"] = "Partially complete. Core algorithm or key functionality is missing."
    else:
        report["comment"] = "Failing. Task completion is seriously insufficient."

    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print formatted scoring report"""
    print("=" * 70)
    print("Speculative Decoding Inference Engine Implementation — Scoring Report")
    print("=" * 70)
    print(f"\nTotal score: {score}/100")

    scores = report.get("dimension_scores", {})
    if scores:
        print("\nDimension scores:")
        for k, v in scores.items():
            print(f"  {k}: {v}")

    for section_key, section_label in [
        ("result_scores", "Result Scores (File Delivery + Report Quality)"),
        ("process_scores", "Process Scores (Code Structure + Algorithm + LLM Review)"),
    ]:
        section = report.get(section_key, {})
        print(f"\n{'─' * 50}")
        print(f"[{section_label}] {section.get('score', 0)} points")
        print(f"{'─' * 50}")
        for cat, items in section.get("details", {}).items():
            print(f"\n  {cat}:")
            if isinstance(items, dict):
                for k, v in items.items():
                    print(f"    {k}: {v}")
            else:
                print(f"    {items}")

    print(f"\n{'=' * 50}")
    print(f"Comment: {report.get('comment', '')}")
    print("=" * 70)


if __name__ == "__main__":
    import sys
    test_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(__file__), "..", "gpt-5", "attempt_1")
    if os.path.exists(test_dir):
        print(f"Evaluating directory: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"Directory does not exist: {test_dir}")
    sys.exit(0)
