"""
Qwen2.5-1.5B Mixed-Precision Quantization Deployment — Scoring Script (rewritten from scratch)

Total: 100 points

Scoring dimensions:
  1. File Delivery Check (15 pts)
    1.1 solution/requirements.txt exists (5 pts)
    1.2 validation.jsonl exists and first line is parseable (5 pts)
    1.3 solution/qwen_quantized.pth exists and non-empty (5 pts)

  2. requirements.txt Quality (10 pts)
    2.1 Contains torch (4 pts)
    2.2 Contains transformers (3 pts)
    2.3 Contains other reasonable ML dependencies (3 pts)

  3. validation.jsonl Data Conversion Quality (25 pts)
    3.1 JSONL format correct (5 pts)
    3.2 Record count matches original parquet — 1221 records (5 pts)
    3.3 Field completeness — id/question/choices/answerKey (10 pts)
    3.4 Sampled comparison with parquet for data consistency (5 pts)

  4. Quantized Model File Quality (25 pts)
    4.1 torch.load can load it (10 pts)
    4.2 File size in reasonable range (10 pts)
    4.3 state_dict contains Qwen architecture parameter keys (5 pts)

  5. Overall Solution Quality — LLM-as-Judge (25 pts)
    5.1 Quantization approach reasonableness (10 pts)
    5.2 Code quality (8 pts)
    5.3 Solution completeness (7 pts)
"""

import os
import re
import json
import sys
from typing import Tuple, Dict, Any, List

try:
    import openai
except ImportError:
    openai = None


# ============================================================================
# Environment & LLM Utilities
# ============================================================================

def _load_env(answer_dir: str) -> dict:
    """Load .env key-value pairs from answer_dir and query root directory."""
    values: Dict[str, str] = {}
    search_dirs = [answer_dir, os.path.join(os.path.dirname(__file__), "..")]
    for d in search_dirs:
        env_path = os.path.join(d, ".env")
        if not os.path.exists(env_path):
            continue
        try:
            with open(env_path, "r") as fh:
                for line in fh:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    k, v = k.strip(), v.strip().strip("'\"")
                    if k not in values:
                        values[k] = v
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
    """Call LLM and return text response; returns empty string on failure."""
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


# ============================================================================
# Helper: Load parquet reference data
# ============================================================================

def _load_reference_parquet() -> List[dict]:
    """Read the parquet file from context/ for comparison."""
    parquet_path = os.path.join(
        os.path.dirname(__file__), "..", "context",
        "validation-00000-of-00001.parquet",
    )
    if not os.path.exists(parquet_path):
        return []
    try:
        import pyarrow.parquet as pq
        table = pq.read_table(parquet_path)
        cols = table.to_pydict()
        n = len(next(iter(cols.values())))
        rows: List[dict] = []
        for i in range(n):
            rows.append({c: cols[c][i] for c in cols})
        return rows
    except Exception:
        return []


# ============================================================================
# Dimension 1: File Delivery (15 pts)
# ============================================================================

def _eval_file_delivery(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details: Dict[str, str] = {}

    # 1.1 solution/requirements.txt (5 pts)
    req_path = os.path.join(answer_dir, "solution", "requirements.txt")
    if os.path.isfile(req_path) and os.path.getsize(req_path) > 0:
        score += 5
        details["1.1 solution/requirements.txt"] = "5/5 — exists and non-empty"
    elif os.path.isfile(req_path):
        score += 2
        details["1.1 solution/requirements.txt"] = "2/5 — exists but empty"
    else:
        details["1.1 solution/requirements.txt"] = "0/5 — missing"

    # 1.2 validation.jsonl (5 pts)
    jsonl_path = os.path.join(answer_dir, "validation.jsonl")
    if os.path.isfile(jsonl_path):
        try:
            with open(jsonl_path, "r", encoding="utf-8") as fh:
                first = fh.readline().strip()
            if first:
                json.loads(first)
                score += 5
                details["1.2 validation.jsonl"] = "5/5 — exists and first line is valid JSON"
            else:
                score += 2
                details["1.2 validation.jsonl"] = "2/5 — exists but file is empty"
        except (json.JSONDecodeError, Exception):
            score += 2
            details["1.2 validation.jsonl"] = "2/5 — exists but first line is not valid JSON"
    else:
        details["1.2 validation.jsonl"] = "0/5 — missing"

    # 1.3 solution/qwen_quantized.pth (5 pts)
    pth_path = os.path.join(answer_dir, "solution", "qwen_quantized.pth")
    if os.path.isfile(pth_path):
        fsize = os.path.getsize(pth_path)
        if fsize > 1024:
            score += 5
            details["1.3 solution/qwen_quantized.pth"] = (
                f"5/5 — exists ({fsize / 1024 / 1024:.1f} MB)"
            )
        else:
            score += 2
            details["1.3 solution/qwen_quantized.pth"] = (
                f"2/5 — exists but abnormally small ({fsize} bytes)"
            )
    else:
        details["1.3 solution/qwen_quantized.pth"] = "0/5 — missing"

    return score, details


# ============================================================================
# Dimension 2: requirements.txt Quality (10 pts)
# ============================================================================

def _eval_requirements(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details: Dict[str, str] = {}

    req_path = os.path.join(answer_dir, "solution", "requirements.txt")
    if not os.path.isfile(req_path):
        details["error"] = "File does not exist, skipping this dimension"
        return 0, details

    try:
        with open(req_path, "r", encoding="utf-8") as fh:
            content = fh.read().lower()
    except Exception as exc:
        details["error"] = f"Read failed: {exc}"
        return 0, details

    lines = [
        l.strip()
        for l in content.splitlines()
        if l.strip() and not l.strip().startswith("#")
    ]

    # 2.1 torch (4 pts)
    if any(re.search(r"\btorch\b", l) for l in lines):
        score += 4
        details["2.1 torch/pytorch"] = "4/4 — found"
    else:
        details["2.1 torch/pytorch"] = "0/4 — not found"

    # 2.2 transformers (3 pts)
    if any("transformers" in l for l in lines):
        score += 3
        details["2.2 transformers"] = "3/3 — found"
    else:
        details["2.2 transformers"] = "0/3 — not found"

    # 2.3 Other reasonable dependencies (3 pts)
    useful_pkgs = [
        "numpy", "pandas", "pyarrow", "accelerate", "sentencepiece",
        "tokenizers", "safetensors", "scipy", "tqdm", "datasets",
        "bitsandbytes", "auto-gptq", "optimum",
    ]
    found = [p for p in useful_pkgs if any(p in l for l in lines)]
    if len(found) >= 2:
        score += 3
        details["2.3 Other dependencies"] = f"3/3 — found: {', '.join(found)}"
    elif len(found) == 1:
        score += 2
        details["2.3 Other dependencies"] = f"2/3 — only found: {found[0]}"
    elif len(lines) >= 3:
        score += 1
        details["2.3 Other dependencies"] = f"1/3 — listed {len(lines)} packages but no common ML dependencies"
    else:
        details["2.3 Other dependencies"] = "0/3 — too few dependencies"

    return score, details


# ============================================================================
# Dimension 3: validation.jsonl Conversion Quality (25 pts)
# ============================================================================

def _eval_validation_jsonl(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details: Dict[str, str] = {}

    jsonl_path = os.path.join(answer_dir, "validation.jsonl")
    if not os.path.isfile(jsonl_path):
        details["error"] = "validation.jsonl does not exist"
        return 0, details

    # Parse all lines
    records: List[dict] = []
    parse_errors = 0
    try:
        with open(jsonl_path, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    parse_errors += 1
    except Exception as exc:
        details["error"] = f"File read failed: {exc}"
        return 0, details

    total_lines = len(records) + parse_errors

    # 3.1 JSONL format (5 pts)
    if total_lines == 0:
        details["3.1 JSONL format"] = "0/5 — file is empty"
        return 0, details

    if parse_errors == 0:
        score += 5
        details["3.1 JSONL format"] = f"5/5 — all {len(records)} lines are valid JSON"
    elif parse_errors <= total_lines * 0.05:
        score += 3
        details["3.1 JSONL format"] = f"3/5 — {parse_errors}/{total_lines} lines failed to parse"
    else:
        score += 1
        details["3.1 JSONL format"] = f"1/5 — {parse_errors}/{total_lines} lines failed to parse (too many)"

    # 3.2 Record count (5 pts) — original parquet has 1221 rows
    EXPECTED = 1221
    n = len(records)
    if n == EXPECTED:
        score += 5
        details["3.2 Record count"] = f"5/5 — exactly {n} records (matches parquet)"
    elif abs(n - EXPECTED) <= 5:
        score += 4
        details["3.2 Record count"] = f"4/5 — {n} records (close to expected {EXPECTED})"
    elif n >= EXPECTED * 0.9:
        score += 3
        details["3.2 Record count"] = f"3/5 — {n} records (>=90% of expected {EXPECTED})"
    elif n >= 100:
        score += 2
        details["3.2 Record count"] = f"2/5 — {n} records (expected {EXPECTED})"
    elif n >= 10:
        score += 1
        details["3.2 Record count"] = f"1/5 — only {n} records"
    else:
        details["3.2 Record count"] = f"0/5 — only {n} records"

    if not records:
        return score, details

    # 3.3 Field completeness (10 pts)
    sample = records[: min(20, len(records))]
    has_question = all("question" in r for r in sample)
    has_answer_key = all(
        "answerKey" in r or "answer_key" in r or "answer" in r for r in sample
    )
    has_choices = all("choices" in r for r in sample)
    has_id = all("id" in r for r in sample)

    field_pts = 0
    found_fields: List[str] = []

    if has_question:
        field_pts += 3
        found_fields.append("question")
    if has_answer_key:
        field_pts += 3
        found_fields.append("answerKey")
    if has_choices:
        found_fields.append("choices")
        # Check choices structure
        first_ch = sample[0].get("choices", {})
        if isinstance(first_ch, dict) and "label" in first_ch and "text" in first_ch:
            field_pts += 3  # Matches original parquet structure
        elif isinstance(first_ch, list) and first_ch:
            if isinstance(first_ch[0], dict) and (
                "label" in first_ch[0] or "text" in first_ch[0]
            ):
                field_pts += 3
            else:
                field_pts += 1
        else:
            field_pts += 1
    if has_id:
        field_pts += 1
        found_fields.append("id")

    score += field_pts
    details["3.3 Field completeness"] = f"{field_pts}/10 — found: {', '.join(found_fields)}"

    # 3.4 Data content correctness (5 pts) — sampled comparison with parquet
    ref_data = _load_reference_parquet()
    if ref_data and records:
        ref_by_id: Dict[str, dict] = {}
        ref_by_q: Dict[str, dict] = {}
        for r in ref_data:
            rid = r.get("id", "")
            if rid:
                ref_by_id[str(rid)] = r
            q = str(r.get("question", "")).strip()
            if q:
                ref_by_q[q] = r

        matched = 0
        checked = 0
        for rec in records[:50]:
            checked += 1
            rid = str(rec.get("id", ""))
            rq = ""
            q_val = rec.get("question", "")
            if isinstance(q_val, str):
                rq = q_val.strip()
            elif isinstance(q_val, dict):
                rq = q_val.get("stem", "").strip()

            ref = ref_by_id.get(rid) or ref_by_q.get(rq)
            if ref:
                rec_ans = rec.get("answerKey", rec.get("answer_key", rec.get("answer", "")))
                ref_ans = ref.get("answerKey", "")
                if str(rec_ans) == str(ref_ans):
                    matched += 1

        if checked > 0:
            rate = matched / checked
            if rate >= 0.9:
                score += 5
                details["3.4 Data consistency"] = f"5/5 — {matched}/{checked} sampled records match reference"
            elif rate >= 0.7:
                score += 3
                details["3.4 Data consistency"] = f"3/5 — {matched}/{checked} matched"
            elif rate >= 0.3:
                score += 2
                details["3.4 Data consistency"] = f"2/5 — {matched}/{checked} matched"
            elif matched > 0:
                score += 1
                details["3.4 Data consistency"] = f"1/5 — {matched}/{checked} matched"
            else:
                details["3.4 Data consistency"] = f"0/5 — none of {checked} sampled records matched"
        else:
            details["3.4 Data consistency"] = "0/5 — no records to check"
    else:
        # Reference data unavailable, give conservative score
        if len(records) >= 100 and has_question and has_answer_key:
            score += 2
            details["3.4 Data consistency"] = "2/5 — reference unavailable, conservative score based on structure"
        else:
            details["3.4 Data consistency"] = "0/5 — reference unavailable and data insufficient"

    return score, details


# ============================================================================
# Dimension 4: Quantized Model File Quality (25 pts)
# ============================================================================

def _eval_quantized_model(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details: Dict[str, str] = {}

    pth_path = os.path.join(answer_dir, "solution", "qwen_quantized.pth")
    if not os.path.isfile(pth_path):
        details["error"] = "qwen_quantized.pth does not exist"
        return 0, details

    fsize = os.path.getsize(pth_path)
    fsize_mb = fsize / (1024 * 1024)

    # 4.1 torch.load can load (10 pts)
    state_dict = None
    loaded = False
    try:
        import torch
        state_dict = torch.load(pth_path, map_location="cpu", weights_only=False)
        score += 10
        details["4.1 torch.load"] = "10/10 — loaded successfully"
        loaded = True
    except ImportError:
        # Evaluation environment has no torch, give conservative score based on file size
        if fsize > 100 * 1024:
            score += 5
            details["4.1 torch.load"] = f"5/10 — torch unavailable, file is {fsize_mb:.1f} MB"
        else:
            details["4.1 torch.load"] = f"0/10 — torch unavailable and file too small ({fsize_mb:.2f} MB)"
    except Exception as exc:
        details["4.1 torch.load"] = f"0/10 — load failed: {str(exc)[:200]}"

    # 4.2 File size (10 pts)
    # Qwen2.5-1.5B: FP32 ~6GB, FP16 ~3GB, INT8 ~1.5GB, mixed-precision ~1-4GB
    if 100 <= fsize_mb <= 5000:
        score += 10
        details["4.2 File size"] = f"10/10 — {fsize_mb:.1f} MB (reasonable range for mixed-precision 1.5B model)"
    elif 50 <= fsize_mb <= 6000:
        score += 7
        details["4.2 File size"] = f"7/10 — {fsize_mb:.1f} MB (borderline)"
    elif fsize_mb >= 10:
        score += 4
        details["4.2 File size"] = f"4/10 — {fsize_mb:.1f} MB (too small)"
    elif fsize_mb >= 1:
        score += 2
        details["4.2 File size"] = f"2/10 — {fsize_mb:.1f} MB (too small)"
    else:
        details["4.2 File size"] = f"0/10 — {fsize_mb:.2f} MB (too small)"

    # 4.3 state_dict key analysis (5 pts)
    if loaded and state_dict is not None:
        if isinstance(state_dict, dict):
            keys = list(state_dict.keys())
            num_keys = len(keys)
            qwen_patterns = [
                "model.layers", "lm_head", "embed_tokens",
                "self_attn", "mlp", "norm", "model.",
            ]
            has_qwen = any(
                any(pat in k for pat in qwen_patterns) for k in keys[:100]
            )
            if has_qwen and num_keys >= 50:
                score += 5
                details["4.3 state_dict keys"] = (
                    f"5/5 — {num_keys} keys, Qwen architecture parameters detected"
                )
            elif num_keys >= 50:
                score += 3
                details["4.3 state_dict keys"] = (
                    f"3/5 — {num_keys} keys, but no Qwen features detected."
                    f" Sample: {keys[:3]}"
                )
            elif num_keys >= 10:
                score += 2
                details["4.3 state_dict keys"] = f"2/5 — only {num_keys} keys"
            elif num_keys > 0:
                score += 1
                details["4.3 state_dict keys"] = f"1/5 — only {num_keys} keys"
            else:
                details["4.3 state_dict keys"] = "0/5 — empty dict"
        else:
            # Not a dict, may be a complete model object
            score += 3
            details["4.3 state_dict keys"] = (
                f"3/5 — loaded object type is {type(state_dict).__name__} (not a dict)"
            )
    elif not loaded:
        details["4.3 state_dict keys"] = "0/5 — model could not be loaded"

    return score, details


# ============================================================================
# Dimension 5: Overall Solution Quality — LLM-as-Judge (25 pts)
# ============================================================================

def _collect_py_files(answer_dir: str) -> List[str]:
    """Recursively search for Python files in answer_dir."""
    results: List[str] = []
    skip = {"__pycache__", "vendor", ".git", "node_modules"}
    for root, dirs, files in os.walk(answer_dir):
        dirs[:] = [d for d in dirs if d not in skip]
        for f in files:
            if f.endswith(".py"):
                results.append(os.path.join(root, f))
    return results


def _fallback_code_heuristic(code: str) -> int:
    """Heuristic scoring when LLM is unavailable, capped at 15/25."""
    pts = 0
    cl = code.lower()

    quant_kw = [
        "quantize", "quantization", "qint8", "qint4", "int8", "int4",
        "dynamic_quantization", "static_quantization",
        "gptq", "awq", "bitsandbytes", "bnb", "half()", "float16",
        "mixed_precision", "mixed precision", "calibrat",
    ]
    if any(k in cl for k in quant_kw):
        pts += 5

    if "from_pretrained" in cl or "automodel" in cl:
        pts += 3

    if "parquet" in cl and ("jsonl" in cl or "json" in cl):
        pts += 3

    if "torch.save" in cl:
        pts += 2

    if len(code) > 500:
        pts += 2

    return min(15, pts)


def _eval_solution_quality(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details: Dict[str, str] = {}

    py_files = _collect_py_files(answer_dir)
    if not py_files:
        details["error"] = "No Python files found"
        return 0, details

    snippets: List[str] = []
    for fp in py_files[:10]:
        try:
            with open(fp, "r", encoding="utf-8") as fh:
                content = fh.read()
            rel = os.path.relpath(fp, answer_dir)
            snippets.append(f"=== {rel} ===\n{content[:3000]}")
        except Exception:
            pass

    if not snippets:
        details["error"] = "Cannot read any Python files"
        return 0, details

    combined = "\n\n".join(snippets)[:8000]

    # requirements.txt content
    req_path = os.path.join(answer_dir, "solution", "requirements.txt")
    req_content = ""
    if os.path.isfile(req_path):
        try:
            with open(req_path, "r", encoding="utf-8") as fh:
                req_content = fh.read()[:500]
        except Exception:
            pass

    has_jsonl = os.path.isfile(os.path.join(answer_dir, "validation.jsonl"))
    has_pth = os.path.isfile(os.path.join(answer_dir, "solution", "qwen_quantized.pth"))

    prompt = f"""You are an evaluation expert for AI model quantization deployment. Please evaluate the following agent submission for Qwen2.5-1.5B mixed-precision quantization deployment.

Task requirements:
1. Create a virtual environment and submit requirements.txt
2. Download the Qwen2.5-1.5B-Instruct original model
3. Convert the Parquet-format validation set to validation.jsonl (original parquet has 1221 records, fields: id, question, question_concept, choices, answerKey)
4. Write a script to generate the mixed-precision qwen_quantized.pth

Deliverable status:
- requirements.txt: {'exists' if req_content else 'missing'}
- validation.jsonl: {'exists' if has_jsonl else 'missing'}
- qwen_quantized.pth: {'exists' if has_pth else 'missing'}

{f'requirements.txt content:{chr(10)}{req_content}' if req_content else ''}

Code files:
{combined}

Please score strictly on the following dimensions:

1. Quantization approach reasonableness (0-10 pts):
   - Is a reasonable quantization method used (e.g., PyTorch dynamic/static quantization, GPTQ, AWQ, bitsandbytes, etc.)?
   - Is "mixed-precision" quantization correctly implemented (different layers using different precision)?
   - Is the quantization logic complete (load model -> quantize -> save)?
   - 0-3: No actual quantization logic or serious errors
   - 4-6: Has quantization logic but not mixed-precision or incomplete implementation
   - 7-8: Reasonable mixed-precision quantization approach with minor issues
   - 9-10: Excellent mixed-precision quantization approach

2. Code quality (0-8 pts):
   - Can the code logically run correctly?
   - Is there appropriate error handling?
   - Is the data conversion (parquet -> jsonl) implemented correctly?
   - 0-2: Code has serious errors or confused logic
   - 3-5: Basically runnable but with obvious issues
   - 6-8: Good code quality

3. Solution completeness (0-7 pts):
   - Does it include all necessary steps (env setup/model download/data conversion/quantization)?
   - Is requirements.txt reasonable?
   - Is the overall solution reproducible?
   - 0-2: Missing multiple key steps
   - 3-4: Has some steps but incomplete
   - 5-7: Steps complete and reproducible

Please reply strictly in the following JSON format:
```json
{{
  "quantization_approach": {{"score": 0, "reason": ""}},
  "code_quality": {{"score": 0, "reason": ""}},
  "completeness": {{"score": 0, "reason": ""}},
  "total": 0,
  "summary": ""
}}
```"""

    config = _get_text_eval_config(answer_dir)
    response = _call_llm_judge(prompt, config)

    if response:
        try:
            text = response
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            result = json.loads(text)

            qa = result.get("quantization_approach", {})
            cq = result.get("code_quality", {})
            cp = result.get("completeness", {})

            qa_score = max(0, min(10, int(qa.get("score", 0))))
            cq_score = max(0, min(8, int(cq.get("score", 0))))
            cp_score = max(0, min(7, int(cp.get("score", 0))))
            score = qa_score + cq_score + cp_score

            details["5.1 Quantization approach"] = f"{qa_score}/10 — {qa.get('reason', '')}"
            details["5.2 Code quality"] = f"{cq_score}/8 — {cq.get('reason', '')}"
            details["5.3 Solution completeness"] = f"{cp_score}/7 — {cp.get('reason', '')}"
            details["summary"] = result.get("summary", "")
        except (json.JSONDecodeError, Exception) as exc:
            details["llm_parse_error"] = f"LLM response parse failed: {str(exc)[:200]}"
            details["llm_raw"] = response[:500]
            score = _fallback_code_heuristic(combined)
            details["fallback"] = f"Heuristic score: {score}/25"
    else:
        score = _fallback_code_heuristic(combined)
        details["llm_unavailable"] = "LLM unavailable, using heuristic scoring"
        details["fallback_score"] = f"{score}/25"

    return score, details


# ============================================================================
# Main Entry
# ============================================================================

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """Evaluate agent output, returns (score, report)."""
    s1, r1 = _eval_file_delivery(answer_dir)
    s2, r2 = _eval_requirements(answer_dir)
    s3, r3 = _eval_validation_jsonl(answer_dir)
    s4, r4 = _eval_quantized_model(answer_dir)
    s5, r5 = _eval_solution_quality(answer_dir)

    total = s1 + s2 + s3 + s4 + s5

    report: Dict[str, Any] = {
        "total_score": total,
        "section_scores": {
            "1_file_delivery": f"{s1}/15",
            "2_requirements_quality": f"{s2}/10",
            "3_validation_jsonl_conversion": f"{s3}/25",
            "4_quantized_model_file": f"{s4}/25",
            "5_overall_solution_quality": f"{s5}/25",
        },
        "details": {
            "1. File Delivery (15 pts)": r1,
            "2. requirements.txt Quality (10 pts)": r2,
            "3. validation.jsonl Conversion (25 pts)": r3,
            "4. Quantized Model File (25 pts)": r4,
            "5. Overall Solution Quality (25 pts)": r5,
        },
    }

    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print formatted scoring report."""
    print("=" * 65)
    print(f"Qwen2.5-1.5B Mixed-Precision Quantization Deployment — Score: {score}/100")
    print("=" * 65)

    sec_scores = report.get("section_scores", {})
    if sec_scores:
        print("\nDimension scores:")
        for k, v in sec_scores.items():
            print(f"  {k}: {v}")

    for section, items in report.get("details", {}).items():
        print(f"\n--- {section} ---")
        if isinstance(items, dict):
            for k, v in items.items():
                print(f"  {k}: {v}")
        else:
            print(f"  {items}")

    print("\n" + "=" * 65)


# ============================================================================
# CLI Entry
# ============================================================================

if __name__ == "__main__":
    test_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(__file__), "..", "gpt-5", "attempt_1",
    )
    if not os.path.isabs(test_dir):
        test_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", test_dir,
        )
    if os.path.exists(test_dir):
        print(f"Evaluating: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"Directory does not exist: {test_dir}")
    sys.exit(0)
