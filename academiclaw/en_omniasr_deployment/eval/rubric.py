#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OmniASR Multilingual Speech Recognition Model Deployment — Rubric (rubric.py)

Total: 100 points

Scoring dimensions:
1. File Delivery (10 pts)
   - dockerfile exists (3 pts)
   - load.py exists (4 pts)
   - answer.md exists (3 pts)

2. Dockerfile Quality (20 pts)
   - Reasonable base image (3 pts)
   - fairseq2 source compilation (7 pts)
   - omnilingual-asr installation (5 pts)
   - Key system/Python dependencies (5 pts)

3. load.py Code Quality (35 pts)
   - Valid syntax (5 pts)
   - Key imports (5 pts)
   - Correct ckpt loading approach (10 pts)
   - Model architecture construction (5 pts)
   - Tokenizer loading and encoding (5 pts)
   - Audio processing and inference logic (5 pts)

4. answer.md Content Quality (15 pts) — LLM-as-Judge
   - Environment setup description (5 pts)
   - Model loading description (5 pts)
   - Demo implementation description (5 pts)

5. Overall Solution Correctness (20 pts) — LLM-as-Judge
   - fairseq2 problem solution (7 pts)
   - ckpt loading technical correctness (7 pts)
   - End-to-end solution completeness (6 pts)
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


# ─────────────────────────────────────────────────────────────────────
# Environment config & LLM calls
# ─────────────────────────────────────────────────────────────────────

def _load_env(answer_dir: str) -> dict:
    """Load .env config from answer_dir and query root directory"""
    values = {}
    for env_dir in [answer_dir, os.path.join(os.path.dirname(__file__), "..")]:
        env_path = os.path.join(env_dir, ".env")
        if os.path.exists(env_path):
            try:
                with open(env_path, "r") as f:
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
        print(f"[RUBRIC] LLM Judge call failed: {e}")
        return ""


def _parse_llm_json(text: str) -> dict:
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


# ─────────────────────────────────────────────────────────────────────
# Helpers: file lookup
# ─────────────────────────────────────────────────────────────────────

def _list_files(d: str) -> List[str]:
    if os.path.isdir(d):
        return os.listdir(d)
    return []


def _find_file(answer_dir: str, name: str, case_insensitive: bool = False) -> str:
    """Find a file in answer_dir, return absolute path or empty string"""
    for f in _list_files(answer_dir):
        if case_insensitive and f.lower() == name.lower():
            return os.path.join(answer_dir, f)
        elif f == name:
            return os.path.join(answer_dir, f)
    return ""


def _read_file(path: str, max_chars: int = 0) -> str:
    if not path or not os.path.exists(path):
        return ""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        if max_chars > 0:
            return content[:max_chars]
        return content
    except Exception:
        return ""


# ─────────────────────────────────────────────────────────────────────
# 1. File Delivery (10 pts)
# ─────────────────────────────────────────────────────────────────────

def _eval_file_delivery(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details = {}
    files = _list_files(answer_dir)

    # dockerfile (3 pts) — case-insensitive
    dockerfile_found = any(f.lower() == "dockerfile" for f in files)
    if dockerfile_found:
        score += 3
        details["dockerfile"] = "3/3 — present"
    else:
        details["dockerfile"] = "0/3 — not found"

    # load.py (4 pts)
    if "load.py" in files:
        score += 4
        details["load.py"] = "4/4 — present"
    else:
        py_files = [f for f in files if f.endswith(".py")]
        if py_files:
            score += 1
            details["load.py"] = f"1/4 — load.py not found, but exists: {py_files[0]}"
        else:
            details["load.py"] = "0/4 — not found"

    # answer.md (3 pts)
    if "answer.md" in files:
        score += 3
        details["answer.md"] = "3/3 — present"
    else:
        md_files = [f for f in files if f.endswith(".md")]
        if md_files:
            score += 1
            details["answer.md"] = f"1/3 — answer.md not found, but exists: {md_files[0]}"
        else:
            details["answer.md"] = "0/3 — not found"

    return score, {"score": f"{score}/10", "details": details}


# ─────────────────────────────────────────────────────────────────────
# 2. Dockerfile Quality (20 pts)
# ─────────────────────────────────────────────────────────────────────

def _eval_dockerfile(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details = {}

    path = _find_file(answer_dir, "dockerfile", case_insensitive=True)
    if not path:
        return 0, {"score": "0/20", "details": {"error": "Dockerfile not found"}}

    content = _read_file(path)
    if not content.strip():
        return 0, {"score": "0/20", "details": {"error": "Dockerfile is empty"}}

    raw = content
    cl = content.lower()

    # 2.1 Base image (3 pts) — has FROM directive
    has_from = bool(re.search(r"^\s*FROM\s+", raw, re.MULTILINE | re.IGNORECASE))
    if has_from:
        score += 3
        details["base_image"] = "3/3 — FROM directive present"
    else:
        details["base_image"] = "0/3 — missing FROM"

    # 2.2 fairseq2 source compilation (7 pts)
    has_fairseq2_clone = ("fairseq2" in raw) and ("git clone" in cl)
    has_cmake_build = "cmake" in cl
    has_ninja = "ninja" in cl
    has_pip_fairseq2 = ("pip" in cl) and ("fairseq2" in raw)

    fs2_score = 0
    if has_fairseq2_clone and has_cmake_build:
        fs2_score = 7
        details["fairseq2_install"] = "7/7 — git clone + cmake source compilation"
    elif has_fairseq2_clone and has_pip_fairseq2:
        fs2_score = 5
        details["fairseq2_install"] = "5/7 — git clone + pip, but missing cmake build step"
    elif has_pip_fairseq2:
        fs2_score = 3
        details["fairseq2_install"] = "3/7 — pip install fairseq2 but no source compilation"
    elif "fairseq" in cl:
        fs2_score = 1
        details["fairseq2_install"] = "1/7 — mentions fairseq but installation method unclear"
    else:
        details["fairseq2_install"] = "0/7 — no fairseq2 coverage"
    score += fs2_score

    # 2.3 omnilingual-asr installation (5 pts)
    has_omnilingual = "omnilingual-asr" in raw or "omnilingual_asr" in raw
    if has_omnilingual and "pip" in cl:
        score += 5
        details["omnilingual_asr"] = "5/5 — pip install omnilingual-asr"
    elif has_omnilingual:
        score += 2
        details["omnilingual_asr"] = "2/5 — mentioned but installation method unclear"
    else:
        if "omnilingual" in cl:
            score += 1
            details["omnilingual_asr"] = "1/5 — indirect mention"
        else:
            details["omnilingual_asr"] = "0/5 — omnilingual-asr not installed"

    # 2.4 Key dependencies (5 pts)
    dep_hits = 0
    dep_list = []
    checks = [
        ("libsndfile", "libsndfile" in cl or "sndfile" in cl),
        ("git", "git" in cl),
        ("cmake/ninja", has_cmake_build or has_ninja),
        ("torch/pytorch", "torch" in cl or "pytorch" in cl),
        ("torchaudio", "torchaudio" in cl),
        ("sentencepiece", "sentencepiece" in cl),
        ("apt-get/pip", "apt-get" in cl or "pip" in cl),
    ]
    for name, found in checks:
        if found:
            dep_hits += 1
            dep_list.append(name)
    dep_score = min(5, dep_hits)
    score += dep_score
    details["key_dependencies"] = f"{dep_score}/5 — detected: {', '.join(dep_list) if dep_list else 'none'}"

    return score, {"score": f"{score}/20", "details": details}


# ─────────────────────────────────────────────────────────────────────
# 3. load.py Code Quality (35 pts)
# ─────────────────────────────────────────────────────────────────────

def _eval_load_py(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details = {}

    # Find load.py or fall back to other .py files
    load_path = os.path.join(answer_dir, "load.py")
    if not os.path.exists(load_path):
        files = _list_files(answer_dir)
        py_files = [f for f in files if f.endswith(".py")]
        if py_files:
            load_path = os.path.join(answer_dir, py_files[0])
            details["note"] = f"load.py not found, using {py_files[0]}"
        else:
            return 0, {"score": "0/35", "details": {"error": "No Python files found"}}

    code = _read_file(load_path)
    if not code.strip():
        return 0, {"score": "0/35", "details": {"error": "File is empty"}}

    cl = code.lower()

    # 3.1 Valid syntax (5 pts)
    try:
        ast.parse(code)
        score += 5
        details["syntax"] = "5/5 — syntax OK"
    except SyntaxError as e:
        details["syntax"] = f"0/5 — syntax error: {str(e)[:80]}"
        return score, {"score": f"{score}/35", "details": details}

    # 3.2 Key imports (5 pts)
    imp_score = 0
    imp_found = []
    if "import torch" in code or "from torch" in code:
        imp_score += 2
        imp_found.append("torch")
    if "fairseq2" in code:
        imp_score += 2
        imp_found.append("fairseq2")
    if any(k in cl for k in ["torchaudio", "soundfile", "librosa", "scipy.io.wavfile"]):
        imp_score += 1
        imp_found.append("audio_lib")
    imp_score = min(5, imp_score)
    score += imp_score
    details["key_imports"] = f"{imp_score}/5 — {', '.join(imp_found) if imp_found else 'none'}"

    # 3.3 ckpt loading approach (10 pts) — core scoring item
    has_torch_load = "torch.load" in code
    has_ckpt_ref = any(k in code for k in ["omniASR", "CTC_300M", "CTC-300M", ".pt"])
    has_load_state_dict = "load_state_dict" in code
    uses_load_model_api = bool(re.search(r"(?:hub\.)?load_model\s*\(", code))

    ckpt_score = 0
    if has_torch_load and has_ckpt_ref and has_load_state_dict:
        if uses_load_model_api:
            ckpt_score = 6
            details["ckpt_loading"] = "6/10 — torch.load+load_state_dict present, but also uses load_model"
        else:
            ckpt_score = 10
            details["ckpt_loading"] = "10/10 — torch.load + load_state_dict, no load_model"
    elif has_torch_load and has_load_state_dict:
        ckpt_score = 7
        details["ckpt_loading"] = "7/10 — torch.load+load_state_dict but no explicit ckpt filename reference"
    elif has_torch_load and has_ckpt_ref:
        ckpt_score = 6
        details["ckpt_loading"] = "6/10 — torch.load references ckpt but no load_state_dict"
    elif has_torch_load:
        ckpt_score = 4
        details["ckpt_loading"] = "4/10 — has torch.load but missing key steps"
    elif uses_load_model_api:
        ckpt_score = 0
        details["ckpt_loading"] = "0/10 — uses load_model (forbidden network download method)"
    else:
        details["ckpt_loading"] = "0/10 — no model loading logic detected"
    score += ckpt_score

    # 3.4 Model architecture construction (5 pts)
    arch_score = 0
    has_hub_get = "get_wav2vec2_asr_model_hub" in code
    has_arch_config = "get_arch_config" in code
    has_create_model = "create_new_model" in code or "create_model" in code
    has_wav2vec2_mention = "wav2vec2" in cl or "Wav2Vec2" in code

    if has_hub_get and has_create_model:
        arch_score = 5
        details["model_architecture"] = "5/5 — hub + create_new_model"
    elif has_hub_get or (has_arch_config and has_create_model):
        arch_score = 4
        details["model_architecture"] = "4/5 — partial architecture construction logic"
    elif has_create_model or has_arch_config:
        arch_score = 3
        details["model_architecture"] = "3/5 — architecture-related code present but incomplete"
    elif has_wav2vec2_mention:
        arch_score = 2
        details["model_architecture"] = "2/5 — mentions wav2vec2 but architecture construction unclear"
    else:
        details["model_architecture"] = "0/5 — no model architecture construction detected"
    score += arch_score

    # 3.5 Tokenizer loading and encoding (5 pts)
    tok_score = 0
    has_tokenizer_load = any(k in code for k in [
        "TokenizerHubAccessor", "load_custom_tokenizer",
        "SentencePieceModel", "sentencepiece",
    ])
    has_tokenizer_ref = "tokenizer" in cl
    has_create_encoder = "create_encoder" in code
    has_encode = "encode" in cl

    if has_tokenizer_load and (has_create_encoder or has_encode):
        tok_score = 5
        details["tokenizer"] = "5/5 — loads tokenizer and uses encoding"
    elif has_tokenizer_load:
        tok_score = 3
        details["tokenizer"] = "3/5 — loads tokenizer but no encoding usage detected"
    elif has_tokenizer_ref and has_encode:
        tok_score = 2
        details["tokenizer"] = "2/5 — mentions tokenizer and encoding but loading method unclear"
    elif has_tokenizer_ref:
        tok_score = 1
        details["tokenizer"] = "1/5 — only mentions tokenizer"
    else:
        details["tokenizer"] = "0/5 — no tokenizer code detected"
    score += tok_score

    # 3.6 Audio processing and inference logic (5 pts)
    audio_score = 0
    has_audio_load = bool(re.search(
        r"torchaudio\.load|soundfile\.read|librosa\.load|wavfile\.read", code
    ))
    has_inference = any(k in code for k in ["model(", "model.forward", "torch.no_grad"])
    has_ctc_decode = any(k in cl for k in ["ctc", "argmax", "greedy", "pred_ids"])
    has_resample = "resample" in cl or "16000" in code or "16khz" in cl

    if has_audio_load and has_inference and has_ctc_decode:
        audio_score = 5
        details["audio_inference"] = "5/5 — audio loading + inference + CTC decoding"
    elif has_audio_load and has_inference:
        audio_score = 4
        details["audio_inference"] = "4/5 — audio loading + inference, but CTC decoding unclear"
    elif has_audio_load or has_inference:
        audio_score = 2
        what = "audio loading" if has_audio_load else "inference logic"
        details["audio_inference"] = f"2/5 — has {what} but incomplete"
    elif "wav" in cl or "audio" in cl:
        audio_score = 1
        details["audio_inference"] = "1/5 — mentions audio but lacks processing logic"
    else:
        details["audio_inference"] = "0/5 — no audio processing detected"
    score += audio_score

    return score, {"score": f"{score}/35", "details": details}


# ─────────────────────────────────────────────────────────────────────
# 4. answer.md Content Quality (15 pts) — LLM-as-Judge
# ─────────────────────────────────────────────────────────────────────

def _eval_answer_md(answer_dir: str) -> Tuple[int, dict]:
    details = {}

    md_path = os.path.join(answer_dir, "answer.md")
    if not os.path.exists(md_path):
        md_files = [f for f in _list_files(answer_dir) if f.endswith(".md")]
        if md_files:
            md_path = os.path.join(answer_dir, md_files[0])
        else:
            return 0, {"score": "0/15", "details": {"error": "answer.md not found"}}

    content = _read_file(md_path)
    if len(content.strip()) < 50:
        return 0, {"score": "0/15", "details": {"error": "Content too short (<50 chars)"}}

    # ── Keyword-based fallback scoring ──
    cl = content.lower()

    env_kw = ["docker", "fairseq2", "pip", "install", "environment", "config", "compile",
              "cmake", "ninja", "source"]
    env_hits = sum(1 for k in env_kw if k in cl)
    env_base = min(5, env_hits)

    model_kw = ["load", "ckpt", "checkpoint", "torch.load", "state_dict", "model",
                "omniasr", "wav2vec2", "architecture", "parameter"]
    model_hits = sum(1 for k in model_kw if k in cl)
    model_base = min(5, model_hits)

    demo_kw = ["demo", "audio", "recognition", "transcri", "wer", "tokenizer",
               "inference", "ctc", "decode"]
    demo_hits = sum(1 for k in demo_kw if k in cl)
    demo_base = min(5, demo_hits)

    base_score = env_base + model_base + demo_base

    # ── LLM evaluation ──
    config = _get_text_eval_config(answer_dir)
    prompt = f"""You are a strict technical documentation evaluator. Below is an implementation walkthrough document for an "OmniASR Multilingual Speech Recognition Model Deployment" task.

Task requirements:
1. Configure the omnilingual-asr environment and solve the fairseq2 installation problem (requires source compilation of fairseq2n)
2. Implement checkpoint-based model loading (omniASR_CTC_300M.pt) — cannot use load_model to download from network
3. Build a speech recognition demo (audio transcription + tokenizer encode/decode)

Score the following three dimensions (integer 0-5 each):

**Dimension 1: Environment Setup Description** (0-5)
- 5: Detailed description of fairseq2 source compilation (git clone + cmake + ninja) and Dockerfile configuration
- 3-4: Has environment setup description but lacks detail
- 1-2: Only briefly mentions environment setup
- 0: No environment setup description at all

**Dimension 2: Model Loading Description** (0-5)
- 5: Detailed description of checkpoint-based model loading, including using fairseq2 model hub to construct architecture, torch.load and load_state_dict
- 3-4: Has model loading description but lacks detail
- 1-2: Only briefly mentioned
- 0: Not present at all

**Dimension 3: Demo Implementation Description** (0-5)
- 5: Detailed description of audio inference pipeline (audio loading, resampling, model inference, CTC decoding, tokenizer usage)
- 3-4: Has description but incomplete
- 1-2: Only briefly mentioned
- 0: Not present at all

Reply strictly in the following JSON format:
```json
{{"env_config": {{"score": 0, "reason": ""}}, "model_loading": {{"score": 0, "reason": ""}}, "demo_impl": {{"score": 0, "reason": ""}}, "total": 0}}
```

Document content:
---
{content[:4000]}
---"""

    llm_resp = _call_llm_judge(prompt, config)
    result = _parse_llm_json(llm_resp)

    if result and "env_config" in result:
        env_s = max(0, min(5, int(result.get("env_config", {}).get("score", 0))))
        mod_s = max(0, min(5, int(result.get("model_loading", {}).get("score", 0))))
        dem_s = max(0, min(5, int(result.get("demo_impl", {}).get("score", 0))))
        llm_total = env_s + mod_s + dem_s
        details["llm_evaluation"] = {
            "env_config": f"{env_s}/5 — {result.get('env_config', {}).get('reason', '')}",
            "model_loading": f"{mod_s}/5 — {result.get('model_loading', {}).get('reason', '')}",
            "demo_description": f"{dem_s}/5 — {result.get('demo_impl', {}).get('reason', '')}",
        }
        return llm_total, {"score": f"{llm_total}/15", "details": details}
    else:
        details["fallback_scoring"] = (
            f"env: {env_base}/5, model: {model_base}/5, demo: {demo_base}/5"
        )
        if llm_resp:
            details["llm_raw_response"] = llm_resp[:200]
        return base_score, {"score": f"{base_score}/15", "details": details}


# ─────────────────────────────────────────────────────────────────────
# 5. Overall Solution Correctness (20 pts) — LLM-as-Judge
# ─────────────────────────────────────────────────────────────────────

def _eval_overall(answer_dir: str) -> Tuple[int, dict]:
    details = {}

    # Collect all file contents
    file_contents = {}
    for fname in ["load.py", "answer.md"]:
        fpath = os.path.join(answer_dir, fname)
        content = _read_file(fpath, max_chars=5000)
        if content:
            file_contents[fname] = content

    # dockerfile
    df_path = _find_file(answer_dir, "dockerfile", case_insensitive=True)
    df_content = _read_file(df_path, max_chars=4000)
    if df_content:
        file_contents["dockerfile"] = df_content

    if not file_contents:
        return 0, {"score": "0/20", "details": {"error": "No evaluable files found"}}

    # ── Keyword-based fallback ──
    all_text = " ".join(file_contents.values()).lower()
    base_score = 0

    # fairseq2 solution
    if ("source" in all_text or "git clone" in all_text) and "fairseq2" in all_text:
        base_score += 5
    elif "fairseq2" in all_text:
        base_score += 2

    # ckpt loading
    if "torch.load" in all_text and "load_state_dict" in all_text:
        base_score += 5
    elif "torch.load" in all_text:
        base_score += 3

    # completeness
    if len(file_contents) >= 3:
        base_score += 4
    elif len(file_contents) >= 2:
        base_score += 2

    # ── LLM evaluation ──
    config = _get_text_eval_config(answer_dir)
    content_block = "\n\n".join(f"=== {k} ===\n{v}" for k, v in file_contents.items())

    prompt = f"""You are a strict AI/ML deployment solution evaluator. Below is a complete submission for the "OmniASR Multilingual Speech Recognition Model Deployment" task.

Task background:
- omnilingual-asr is Facebook's open-source multilingual speech recognition model, depending on fairseq2
- fairseq2 has no precompiled packages for aarch64/NPU — source compilation of fairseq2n is required (git clone + cmake + ninja)
- The model must be loaded via checkpoint (omniASR_CTC_300M.pt) — using load_model to download from network is forbidden
- Correct workflow: get_wav2vec2_asr_model_hub → get_arch_config("300m") → create_new_model → torch.load ckpt → load_state_dict
- Model parameter count must be strictly 325,494,996
- Tokenizer encoding of "hello world" must output [113, 9346, 1875, 1875, 8749, 4, 4618, 8749, 6712, 1875, 1133]
- Audio transcription WER ≤ 20% (reference text: "book spot in Lebanon for ten weeks from now")

Score strictly on the following three dimensions:

**Dimension 1: fairseq2 Problem Solution** (0-7)
- 6-7: Correctly solves fairseq2 installation via source compilation (git clone + cmake + ninja)
- 3-5: Has a solution approach but incomplete or has technical issues
- 0-2: Solution has obvious errors or does not address the core problem

**Dimension 2: ckpt Loading Approach** (0-7)
- 6-7: Correctly uses fairseq2 model hub to construct architecture + torch.load + load_state_dict, technically sound
- 3-5: Has ckpt loading but technical details are problematic
- 0-2: Uses forbidden load_model or loading approach has obvious errors

**Dimension 3: End-to-End Solution Completeness** (0-6)
- 5-6: Dockerfile + model loading + audio inference + CTC decoding + tokenizer usage, complete pipeline
- 3-4: Most of the pipeline is complete but missing some components
- 0-2: Solution is incomplete

Reply strictly in the following JSON format:
```json
{{"fairseq2_solution": {{"score": 0, "reason": ""}}, "ckpt_loading": {{"score": 0, "reason": ""}}, "completeness": {{"score": 0, "reason": ""}}, "total": 0}}
```

Submission content:
---
{content_block[:10000]}
---"""

    llm_resp = _call_llm_judge(prompt, config)
    result = _parse_llm_json(llm_resp)

    if result and "fairseq2_solution" in result:
        fs_s = max(0, min(7, int(result.get("fairseq2_solution", {}).get("score", 0))))
        ck_s = max(0, min(7, int(result.get("ckpt_loading", {}).get("score", 0))))
        cp_s = max(0, min(6, int(result.get("completeness", {}).get("score", 0))))
        llm_total = fs_s + ck_s + cp_s
        details["llm_evaluation"] = {
            "fairseq2_solution": f"{fs_s}/7 — {result.get('fairseq2_solution', {}).get('reason', '')}",
            "ckpt_loading": f"{ck_s}/7 — {result.get('ckpt_loading', {}).get('reason', '')}",
            "completeness": f"{cp_s}/6 — {result.get('completeness', {}).get('reason', '')}",
        }
        return llm_total, {"score": f"{llm_total}/20", "details": details}
    else:
        details["fallback_scoring"] = f"base score: {base_score}/20"
        if llm_resp:
            details["llm_raw_response"] = llm_resp[:200]
        return base_score, {"score": f"{base_score}/20", "details": details}


# ─────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Evaluate agent output.

    Args:
        answer_dir: absolute path to agent output directory

    Returns:
        (score, report)
        - score: int 0-100
        - report: dict with detailed evaluation report
    """
    s1, r1 = _eval_file_delivery(answer_dir)
    s2, r2 = _eval_dockerfile(answer_dir)
    s3, r3 = _eval_load_py(answer_dir)
    s4, r4 = _eval_answer_md(answer_dir)
    s5, r5 = _eval_overall(answer_dir)

    total = max(0, min(100, s1 + s2 + s3 + s4 + s5))

    report = {
        "total": total,
        "section_scores": {
            "1_file_delivery": f"{s1}/10",
            "2_dockerfile_quality": f"{s2}/20",
            "3_load_py_quality": f"{s3}/35",
            "4_answer_md_content": f"{s4}/15",
            "5_overall_correctness": f"{s5}/20",
        },
        "section_reports": {
            "1_file_delivery_10pts": r1,
            "2_dockerfile_quality_20pts": r2,
            "3_load_py_quality_35pts": r3,
            "4_answer_md_content_15pts": r4,
            "5_overall_correctness_20pts": r5,
        },
    }

    if total >= 85:
        report["comment"] = "Excellent! Complete solution, correct technical approach, clear documentation."
    elif total >= 65:
        report["comment"] = "Good. Task mostly completed, some dimensions have room for improvement."
    elif total >= 45:
        report["comment"] = "Passing. Core functionality implemented but notable shortcomings."
    elif total >= 25:
        report["comment"] = "Partial. Key components missing or technical approach has obvious errors."
    else:
        report["comment"] = "Failing. Task completion is severely insufficient."

    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print formatted evaluation report"""
    print("=" * 70)
    print("OmniASR Multilingual Speech Recognition Deployment — Evaluation Report")
    print("=" * 70)
    print(f"\nTotal: {score}/100")
    print(f"Comment: {report.get('comment', '')}")

    scores = report.get("section_scores", {})
    if scores:
        print(f"\n{'─' * 50}")
        print("Section scores:")
        for k, v in scores.items():
            print(f"  {k}: {v}")

    sections = report.get("section_reports", {})
    for section_name, section_data in sections.items():
        print(f"\n{'─' * 50}")
        print(f"[{section_name}]")
        if isinstance(section_data, dict):
            for key, val in section_data.items():
                if isinstance(val, dict):
                    print(f"  {key}:")
                    for k2, v2 in val.items():
                        print(f"    {k2}: {v2}")
                else:
                    print(f"  {key}: {val}")

    print(f"\n{'=' * 70}")


# ─────────────────────────────────────────────────────────────────────
# Standalone execution
# ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    test_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(__file__), "..", "gpt-5", "attempt_1")
    if not os.path.isabs(test_dir):
        test_dir = os.path.join(os.path.dirname(__file__), "..", test_dir)
    test_dir = os.path.abspath(test_dir)

    if os.path.exists(test_dir):
        print(f"Evaluating directory: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"Directory does not exist: {test_dir}")
        print("Usage: python rubric.py <answer_dir>")
    sys.exit(0)
