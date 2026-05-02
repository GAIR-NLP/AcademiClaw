"""
Scoring Rubric for Docker Environment Configuration
Task: Write a reproducible Dockerfile for the VARSTok speech synthesis Python project
Deliverable: Dockerfile

Total Score: 100 points

Scoring Dimensions:
I.   File Delivery and Basic Validity (15 points)
II.  Base Image and Python Environment (20 points)
III. Dependency Installation and Project Adaptation (35 points)
IV.  Dockerfile Best Practices (15 points)
V.   LLM Comprehensive Evaluation (15 points)
"""

import os
import re
import json
from typing import Any, Dict, List, Tuple

try:
    import openai
except ImportError:
    openai = None


# ---------------------------------------------------------------------------
# Environment and LLM Utilities
# ---------------------------------------------------------------------------

def _load_env(answer_dir: str) -> dict:
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
        print(f"[RUBRIC] LLM Judge error: {e}")
        return ""


# ---------------------------------------------------------------------------
# Dockerfile Parsing Utilities
# ---------------------------------------------------------------------------

def _read_dockerfile(answer_dir: str) -> Tuple[str, List[str]]:
    """Return (raw_text, effective_lines_without_comments)"""
    for name in ("Dockerfile", "dockerfile"):
        path = os.path.join(answer_dir, name)
        if os.path.exists(path):
            try:
                raw = open(path, "r", encoding="utf-8", errors="replace").read()
            except Exception:
                return "", []
            lines = []
            for ln in raw.splitlines():
                s = ln.strip()
                if s and not s.startswith("#"):
                    lines.append(s)
            return raw, lines
    return "", []


def _join_continued(lines: List[str]) -> str:
    """Join effective lines into one string for searching (preserving newlines)"""
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# VARSTok Project Key Information
# ---------------------------------------------------------------------------

REQUIREMENTS_PACKAGES = [
    "torch", "torchaudio", "scipy", "einops", "pyyaml",
    "huggingface_hub", "encodec", "matplotlib", "transformers",
    "pytorch-lightning", "tensorboardX", "soundfile", "numpy",
    "jsonargparse", "fairseq", "torchcrepe", "librosa", "pesq",
]

# Most critical packages - these are essential for VARSTok core runtime
CRITICAL_PACKAGES = ["torch", "torchaudio", "soundfile", "librosa",
                     "transformers", "encodec", "fairseq"]

SYSTEM_DEPS = {
    "libsndfile": ["libsndfile", "libsndfile1", "libsndfile1-dev"],
    "ffmpeg": ["ffmpeg"],
    "build_tools": ["build-essential", "gcc", "g++"],
    "git": ["git"],
}


# ---------------------------------------------------------------------------
# I. File Delivery and Basic Validity (15 points)
# ---------------------------------------------------------------------------

def _eval_delivery(answer_dir: str) -> Tuple[int, Dict[str, str]]:
    score = 0
    details: Dict[str, str] = {}

    raw, lines = _read_dockerfile(answer_dir)

    # 1.1 Dockerfile exists (5 points)
    if not raw:
        details["Dockerfile exists"] = "0/5 - Dockerfile does not exist"
        return 0, details
    score += 5
    details["Dockerfile exists"] = "5/5"

    # 1.2 Non-empty with meaningful instruction lines >= 3 (5 points)
    if len(lines) >= 5:
        score += 5
        details["Effective instruction count"] = f"5/5 - {len(lines)} effective instructions"
    elif len(lines) >= 3:
        score += 3
        details["Effective instruction count"] = f"3/5 - {len(lines)} effective instructions (too few)"
    elif len(lines) >= 1:
        score += 1
        details["Effective instruction count"] = f"1/5 - only {len(lines)} effective instructions"
    else:
        details["Effective instruction count"] = "0/5 - file is empty or contains only comments"

    # 1.3 Contains FROM and RUN basic instructions (5 points)
    has_from = any(l.upper().startswith("FROM ") for l in lines)
    has_run = any(l.upper().startswith("RUN ") for l in lines)
    has_copy = any(re.match(r"(?i)^(COPY|ADD)\s+", l) for l in lines)

    sub = 0
    if has_from:
        sub += 2
    if has_run:
        sub += 2
    if has_copy:
        sub += 1
    score += sub
    parts = []
    if has_from:
        parts.append("FROM")
    if has_run:
        parts.append("RUN")
    if has_copy:
        parts.append("COPY/ADD")
    details["Basic instructions"] = f"{sub}/5 - contains: {', '.join(parts) if parts else 'none'}"

    return score, details


# ---------------------------------------------------------------------------
# II. Base Image and Python Environment (20 points)
# ---------------------------------------------------------------------------

def _eval_base_image(answer_dir: str) -> Tuple[int, Dict[str, str]]:
    score = 0
    details: Dict[str, str] = {}
    raw, lines = _read_dockerfile(answer_dir)
    if not lines:
        details["error"] = "0/20 - unable to parse Dockerfile"
        return 0, details

    # Extract FROM line
    from_line = ""
    for l in lines:
        if l.upper().startswith("FROM "):
            from_line = l
            break

    if not from_line:
        details["FROM"] = "0/10 - missing FROM instruction"
        details["Python version compatibility"] = "0/6 - no FROM"
        details["WORKDIR"] = "0/4 - missing"
        return 0, details

    from_lower = from_line.lower()

    # 2.1 Selected a base image containing Python (10 points)
    is_python_img = bool(re.search(r'\bpython\b', from_lower))
    is_pytorch_img = bool(re.search(r'\b(pytorch|torch)\b', from_lower))
    is_nvidia = bool(re.search(r'\b(nvidia|cuda|nvcr)\b', from_lower))
    is_conda = bool(re.search(r'\b(conda|miniconda|anaconda)\b', from_lower))

    if is_python_img:
        score += 10
        details["FROM image"] = f"10/10 - Python base image: {from_line}"
    elif is_pytorch_img:
        score += 9
        details["FROM image"] = f"9/10 - PyTorch image (includes Python): {from_line}"
    elif is_nvidia:
        score += 6
        details["FROM image"] = f"6/10 - NVIDIA/CUDA image (requires additional Python installation): {from_line}"
    elif is_conda:
        score += 7
        details["FROM image"] = f"7/10 - Conda image: {from_line}"
    else:
        score += 2
        details["FROM image"] = f"2/10 - not a Python-specific image: {from_line}"

    # 2.2 Python version compatible with torch 2.0.0 (6 points)
    # torch 2.0.0 supports Python 3.8-3.11; README recommends 3.9
    ver_match = re.search(r'python\s*[:.]?\s*(3\.(?:9|10|11))', from_lower)
    ver_match_38 = re.search(r'python\s*[:.]?\s*3\.8', from_lower)
    ver_match_any = re.search(r'python\s*[:.]?\s*(3\.\d+)', from_lower)

    if ver_match:
        score += 6
        details["Python version compatibility"] = f"6/6 - Python {ver_match.group(1)} compatible with torch 2.0.0"
    elif ver_match_38:
        score += 4
        details["Python version compatibility"] = "4/6 - Python 3.8 usable but not recommended"
    elif ver_match_any:
        ver_str = ver_match_any.group(1)
        score += 2
        details["Python version compatibility"] = f"2/6 - Python {ver_str} may not be compatible with torch 2.0.0"
    elif is_python_img or is_pytorch_img or is_conda:
        score += 3
        details["Python version compatibility"] = "3/6 - includes Python but version not explicitly specified"
    else:
        details["Python version compatibility"] = "0/6 - unable to determine Python version"

    # 2.3 WORKDIR setting (4 points)
    has_workdir = any(re.match(r"(?i)^WORKDIR\s+", l) for l in lines)
    if has_workdir:
        score += 4
        details["WORKDIR"] = "4/4"
    else:
        details["WORKDIR"] = "0/4 - missing WORKDIR"

    return score, details


# ---------------------------------------------------------------------------
# III. Dependency Installation and Project Adaptation (35 points)
# ---------------------------------------------------------------------------

def _eval_dependencies(answer_dir: str) -> Tuple[int, Dict[str, str]]:
    score = 0
    details: Dict[str, str] = {}
    raw, lines = _read_dockerfile(answer_dir)
    if not lines:
        details["error"] = "0/35 - unable to parse Dockerfile"
        return 0, details

    blob = _join_continued(lines).lower()
    raw_lower = raw.lower()

    # 3.1 Install requirements.txt (12 points)
    has_req_install = bool(re.search(
        r'pip3?\s+install\b.*-r\s+\S*requirements\.txt', blob
    ))
    has_req_copy = bool(re.search(
        r'(?i)^(COPY|ADD)\b.*requirements\.txt', "\n".join(lines), re.MULTILINE
    ))

    if has_req_install and has_req_copy:
        score += 12
        details["requirements.txt installation"] = "12/12 - COPY + pip install -r"
    elif has_req_install:
        score += 8
        details["requirements.txt installation"] = "8/12 - pip install -r but did not separately COPY requirements.txt"
    elif has_req_copy:
        score += 3
        details["requirements.txt installation"] = "3/12 - COPY requirements.txt but no pip install -r"
    else:
        # Check if key packages were manually installed
        manual = sum(1 for pkg in CRITICAL_PACKAGES if pkg.lower() in blob)
        if manual >= 5:
            score += 6
            details["requirements.txt installation"] = f"6/12 - did not use requirements.txt, manually installed {manual}/{len(CRITICAL_PACKAGES)} critical packages"
        elif manual >= 3:
            score += 3
            details["requirements.txt installation"] = f"3/12 - manually installed {manual} critical packages (insufficient)"
        else:
            details["requirements.txt installation"] = "0/12 - did not install requirements.txt and did not manually install critical packages"

    # 3.2 System dependency installation (10 points)
    sys_score = 0
    sys_parts = []

    # libsndfile (3 points)
    if any(alias in raw_lower for alias in SYSTEM_DEPS["libsndfile"]):
        sys_score += 3
        sys_parts.append("libsndfile: 3/3")
    else:
        sys_parts.append("libsndfile: 0/3")

    # ffmpeg (3 points)
    if any(alias in raw_lower for alias in SYSTEM_DEPS["ffmpeg"]):
        sys_score += 3
        sys_parts.append("ffmpeg: 3/3")
    else:
        sys_parts.append("ffmpeg: 0/3")

    # build tools (2 points)
    if any(alias in raw_lower for alias in SYSTEM_DEPS["build_tools"]):
        sys_score += 2
        sys_parts.append("build-essential/gcc: 2/2")
    else:
        sys_parts.append("build-essential/gcc: 0/2")

    # git (2 points) - fairseq needs git
    if any(alias in raw_lower for alias in SYSTEM_DEPS["git"]):
        sys_score += 2
        sys_parts.append("git: 2/2")
    else:
        sys_parts.append("git: 0/2")

    score += sys_score
    details["System dependencies"] = f"{sys_score}/10 - {'; '.join(sys_parts)}"

    # 3.3 Copy project files into image (8 points)
    copy_lines = [l for l in lines if re.match(r"(?i)^(COPY|ADD)\s+", l)]
    copies_project = False
    for cl in copy_lines:
        cl_lower = cl.lower()
        # Exclude lines that only COPY requirements.txt
        if "requirements.txt" in cl_lower:
            # If this line only has requirements.txt, skip
            parts = cl.split()
            if len(parts) <= 3 and all("requirements" in p.lower() for p in parts[1:-1]):
                continue
        # Check if project files were copied
        if any(kw in cl_lower for kw in ["varstok", ".", "context", "src", "app", "project"]):
            copies_project = True
            break
        if re.search(r"(?i)^(COPY|ADD)\s+\./?(\s|$)", cl):
            copies_project = True
            break

    if copies_project:
        score += 8
        details["Copy project files"] = "8/8 - copied VARSTok project files into image"
    elif copy_lines:
        score += 3
        details["Copy project files"] = "3/8 - has COPY but only copied requirements.txt"
    else:
        details["Copy project files"] = "0/8 - missing COPY/ADD instructions"

    # 3.4 apt-get update/install present (5 points)
    has_apt = bool(re.search(r'apt(-get)?\s+(update|install)', blob))
    if has_apt:
        score += 5
        details["apt-get installation"] = "5/5 - uses apt-get to install system dependencies"
    else:
        # Some FROM images may already have them built-in
        details["apt-get installation"] = "0/5 - missing apt-get install (system dependencies may not be installed)"

    return score, details


# ---------------------------------------------------------------------------
# IV. Dockerfile Best Practices (15 points)
# ---------------------------------------------------------------------------

def _eval_best_practices(answer_dir: str) -> Tuple[int, Dict[str, str]]:
    score = 0
    details: Dict[str, str] = {}
    raw, lines = _read_dockerfile(answer_dir)
    if not lines:
        details["error"] = "0/15 - unable to parse Dockerfile"
        return 0, details

    blob = _join_continued(lines)
    blob_lower = blob.lower()

    # 4.1 Layer caching strategy (5 points)
    # COPY requirements.txt first -> pip install -> then COPY project files
    req_copy_idx = []
    req_install_idx = []
    project_copy_idx = []
    for i, l in enumerate(lines):
        if re.search(r"(?i)^(COPY|ADD)\b.*requirements\.txt", l):
            req_copy_idx.append(i)
        if re.search(r"(?i)pip3?\s+install\b.*-r\s+\S*requirements", l):
            req_install_idx.append(i)
        if re.match(r"(?i)^(COPY|ADD)\s+", l) and "requirements.txt" not in l.lower():
            project_copy_idx.append(i)

    layer_ok = False
    if req_copy_idx and req_install_idx and project_copy_idx:
        if (min(req_copy_idx) < min(req_install_idx) <
                min(project_copy_idx)):
            layer_ok = True

    if layer_ok:
        score += 5
        details["Layer caching"] = "5/5 - COPY requirements.txt first -> install -> COPY project"
    elif req_copy_idx and req_install_idx:
        score += 3
        details["Layer caching"] = "3/5 - requirements.txt separated but order not ideal"
    else:
        details["Layer caching"] = "0/5 - layer caching strategy not implemented"

    # 4.2 --no-cache-dir (2 points)
    if re.search(r"--no-cache-dir", blob_lower) or re.search(r"PIP_NO_CACHE_DIR", raw):
        score += 2
        details["pip no-cache-dir"] = "2/2"
    else:
        details["pip no-cache-dir"] = "0/2 - --no-cache-dir not used"

    # 4.3 Clean apt cache (2 points)
    if re.search(r"rm\s+-rf\s+/var/lib/apt/lists", blob_lower):
        score += 2
        details["Clean apt cache"] = "2/2"
    else:
        details["Clean apt cache"] = "0/2 - apt cache not cleaned"

    # 4.4 CMD or ENTRYPOINT (3 points)
    has_cmd = any(re.match(r"(?i)^(CMD|ENTRYPOINT)\s+", l) for l in lines)
    if has_cmd:
        score += 3
        details["CMD/ENTRYPOINT"] = "3/3 - default command defined"
    else:
        score += 1
        details["CMD/ENTRYPOINT"] = "1/3 - CMD/ENTRYPOINT not defined"

    # 4.5 No sudo (1 point)
    if any(re.search(r"\bsudo\b", l) for l in lines):
        details["sudo usage"] = "0/1 - unnecessarily used sudo"
    else:
        score += 1
        details["sudo usage"] = "1/1 - no sudo"

    # 4.6 Python import self-check (2 points)
    if re.search(r'(?i)RUN\s+python3?\s+-c\s+["\'].*import', blob):
        score += 2
        details["Import self-check"] = "2/2 - includes import verification"
    else:
        details["Import self-check"] = "0/2 - no import self-check included"

    return score, details


# ---------------------------------------------------------------------------
# V. LLM Comprehensive Evaluation (15 points)
# ---------------------------------------------------------------------------

_LLM_PROMPT = """\
You are a strict review expert in Docker and Python environment configuration. Please evaluate whether the following Dockerfile can create a reproducible runtime environment for the VARSTok speech synthesis project.

## VARSTok Project Key Information
- PyTorch-based variable frame rate speech tokenizer
- Recommended Python 3.9 or 3.10 (conda create -n varstok python=3.9)
- requirements.txt key packages: torch==2.0.0, torchaudio==2.0.1, scipy, einops, transformers, pytorch-lightning, soundfile, librosa, encodec, fairseq, torchcrepe, pesq
- System dependencies required: libsndfile1 (soundfile), ffmpeg (audio processing), build-essential (compiling native extensions), git (fairseq installation)
- Training script: torchrun --nproc_per_node=4 train.py fit --config configs/xxx.yaml
- Inference script: python infer.py

## Agent-submitted Dockerfile
```dockerfile
{dockerfile_content}
```

Please score the following three aspects (integer 0-5 each) and return strict JSON:
1. **buildability** - Correct syntax, reasonable build process, no obvious build errors
2. **dependency_completeness** - Are Python and system dependencies complete, can they satisfy all VARSTok imports
3. **runnability** - Can the built image actually run infer.py or train.py

```json
{{
  "buildability": {{"score": 0, "reason": ""}},
  "dependency_completeness": {{"score": 0, "reason": ""}},
  "runnability": {{"score": 0, "reason": ""}},
  "total": 0,
  "overall_comment": ""
}}
```
Only output the JSON above, no other content."""


def _eval_llm(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    raw, lines = _read_dockerfile(answer_dir)
    if not raw:
        return 0, {"error": "Dockerfile does not exist", "score": 0}

    config = _get_text_eval_config(answer_dir)
    prompt = _LLM_PROMPT.format(dockerfile_content=raw)
    resp = _call_llm_judge(prompt, config)

    if not resp:
        return 0, {"error": "LLM unavailable, conservative score 0", "score": 0}

    try:
        text = resp
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        result = json.loads(text)
        total = int(result.get("total", 0))
        total = max(0, min(15, total))
        result["score"] = total
        return total, result
    except (json.JSONDecodeError, ValueError):
        print(f"[RUBRIC] LLM returned non-JSON: {resp[:300]}")
        return 0, {"error": "LLM response parsing failed", "raw": resp[:500], "score": 0}


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Evaluate the agent-produced Dockerfile.

    Args:
        answer_dir: Absolute path to the agent output directory

    Returns:
        (score, report)  score: 0-100 integer; report: dict
    """

    # Dimension I: File delivery (15 points)
    s1, r1 = _eval_delivery(answer_dir)

    # If Dockerfile does not exist at all, score 0
    if s1 == 0:
        report = {
            "total_score": 0,
            "section_scores": {
                "I. File delivery": "0/15",
                "II. Base image": "0/20",
                "III. Dependency installation": "0/35",
                "IV. Best practices": "0/15",
                "V. LLM comprehensive": "0/15",
            },
            "details": {
                "I. File delivery": r1,
                "II. Base image": {"error": "Dockerfile does not exist"},
                "III. Dependency installation": {"error": "Dockerfile does not exist"},
                "IV. Best practices": {"error": "Dockerfile does not exist"},
                "V. LLM comprehensive": {"error": "Dockerfile does not exist"},
            },
        }
        return 0, report

    # Dimension II: Base image and Python environment (20 points)
    s2, r2 = _eval_base_image(answer_dir)

    # Dimension III: Dependency installation and project adaptation (35 points)
    s3, r3 = _eval_dependencies(answer_dir)

    # Dimension IV: Best practices (15 points)
    s4, r4 = _eval_best_practices(answer_dir)

    # Dimension V: LLM comprehensive evaluation (15 points)
    s5, r5 = _eval_llm(answer_dir)

    total = min(s1 + s2 + s3 + s4 + s5, 100)

    report = {
        "total_score": total,
        "section_scores": {
            "I. File delivery": f"{s1}/15",
            "II. Base image": f"{s2}/20",
            "III. Dependency installation": f"{s3}/35",
            "IV. Best practices": f"{s4}/15",
            "V. LLM comprehensive": f"{s5}/15",
        },
        "details": {
            "I. File delivery": r1,
            "II. Base image": r2,
            "III. Dependency installation": r3,
            "IV. Best practices": r4,
            "V. LLM comprehensive": r5,
        },
    }

    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print formatted evaluation report"""
    print("=" * 70)
    print("Docker Environment Configuration - Evaluation Report")
    print("Task: Write a reproducible Dockerfile for the VARSTok speech synthesis project")
    print("=" * 70)
    print(f"\nTotal score: {score}/100\n")

    scores = report.get("section_scores", {})
    if scores:
        print("Section scores:")
        for k, v in scores.items():
            print(f"  {k}: {v}")

    for section_name, section_data in report.get("details", {}).items():
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

    print(f"\n{'=' * 70}")


if __name__ == "__main__":
    import sys

    test_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(__file__), "..", "gpt-5", "attempt_1"
    )

    if not os.path.isabs(test_dir):
        test_dir = os.path.join(os.path.dirname(__file__), "..", test_dir)

    test_dir = os.path.abspath(test_dir)

    if os.path.exists(test_dir):
        print(f"Evaluating directory: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"Directory not found: {test_dir}")
    sys.exit(0)
