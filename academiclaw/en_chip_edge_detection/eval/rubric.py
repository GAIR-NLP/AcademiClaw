"""
Scoring Script — Chip Ring Inner Edge Detection Algorithm Implementation

Total: 100 points, divided into four dimensions:
  I.   File Delivery Completeness  (15 pts)  — Programmatic check
  II.  Code Executability          (25 pts)  — Programmatic check
  III. Algorithm Implementation Quality (35 pts)  — LLM-as-Judge + fallback
  IV.  Code Engineering Quality    (25 pts)  — Programmatic + LLM hybrid
"""

import os
import re
import sys
import json
import ast
from typing import Tuple, Dict, Any, List

try:
    import openai
except ImportError:
    openai = None

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

REQUIRED_FILES: List[str] = [
    "preprocess.py",
    "coarse_detection.py",
    "fine_detection.py",
    "statistical_analysis.py",
    "mask_generation.py",
    "main.py",
    "test.py",
]

# Point value per file (total = 15)
_FILE_PTS: Dict[str, int] = {
    "preprocess.py": 2,
    "coarse_detection.py": 2,
    "fine_detection.py": 3,
    "statistical_analysis.py": 2,
    "mask_generation.py": 2,
    "main.py": 2,
    "test.py": 2,
}

# ---------------------------------------------------------------------------
# Environment / LLM Tools
# ---------------------------------------------------------------------------

def _load_env(answer_dir: str) -> dict:
    values: Dict[str, str] = {}
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


def _parse_json_from_text(text: str) -> dict:
    m = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            pass
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1:
        try:
            return json.loads(text[start : end + 1])
        except json.JSONDecodeError:
            pass
    return {}


# ---------------------------------------------------------------------------
# File Helpers
# ---------------------------------------------------------------------------

_SKIP_DIRS = {"__pycache__", ".git", "context", ".sii", "eval_out", "eval_out2", "eval_out_final", "output"}


def _find_file(answer_dir: str, filename: str) -> str:
    direct = os.path.join(answer_dir, filename)
    if os.path.isfile(direct):
        return direct
    for root, dirs, files in os.walk(answer_dir):
        dirs[:] = [d for d in dirs if d not in _SKIP_DIRS]
        if filename in files:
            return os.path.join(root, filename)
    return ""


def _read_file(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except Exception:
        return ""


def _collect_all_py(answer_dir: str) -> Dict[str, str]:
    result: Dict[str, str] = {}
    for root, dirs, files in os.walk(answer_dir):
        dirs[:] = [d for d in dirs if d not in _SKIP_DIRS]
        for f in sorted(files):
            if f.endswith(".py"):
                content = _read_file(os.path.join(root, f))
                if content.strip():
                    result[f] = content
    return result


# ===================================================================
# I. File Delivery Completeness (15 pts)
# ===================================================================

def _dim1_file_delivery(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    items: Dict[str, str] = {}

    for fname in REQUIRED_FILES:
        pts = _FILE_PTS[fname]
        path = _find_file(answer_dir, fname)
        if not path:
            items[fname] = f"0/{pts} - missing"
            continue
        content = _read_file(path)
        if len(content.strip()) < 30:
            items[fname] = f"0/{pts} - too little content (<30 chars)"
            continue
        # Must contain at least one of import / def / class to qualify as Python code
        if re.search(r"(import\s|from\s|def\s|class\s)", content):
            score += pts
            items[fname] = f"{pts}/{pts} - OK ({len(content)} chars)"
        else:
            half = max(1, pts // 2)
            score += half
            items[fname] = f"{half}/{pts} - exists but no Python code structure"

    score = min(score, 15)
    return score, {"score": score, "max": 15, "items": items}


# ===================================================================
# II. Code Executability (25 pts)
# ===================================================================

def _dim2_executability(answer_dir: str) -> Tuple[int, dict]:
    total = 0
    sections: Dict[str, Any] = {}

    # 2.1 Syntax correctness (10 pts)
    syntax_pts_map = {
        "preprocess": 1,
        "coarse_detection": 2,
        "fine_detection": 2,
        "statistical_analysis": 2,
        "mask_generation": 2,
        "main": 1,
    }
    syntax_score = 0
    syntax_items: Dict[str, str] = {}
    for module, pts in syntax_pts_map.items():
        path = _find_file(answer_dir, module + ".py")
        if not path:
            syntax_items[module] = f"0/{pts} - not found"
            continue
        content = _read_file(path)
        if not content.strip():
            syntax_items[module] = f"0/{pts} - empty file"
            continue
        try:
            compile(content, path, "exec")
            syntax_score += pts
            syntax_items[module] = f"{pts}/{pts} - compilable"
        except SyntaxError as e:
            syntax_items[module] = f"0/{pts} - SyntaxError: {str(e)[:80]}"

    syntax_score = min(syntax_score, 10)
    total += syntax_score
    sections["2.1_syntax"] = {"score": syntax_score, "max": 10, "items": syntax_items}

    # 2.2 Key function existence (10 pts)
    all_code = _collect_all_py(answer_dir)
    combined = "\n".join(all_code.values())

    # (description, regex_for_func_def, points)
    func_checks: List[tuple] = [
        ("downsample/preprocess function", r"def\s+\w*(downsample|resize|preprocess)\w*\s*\(", 1),
        ("gaussian blur function", r"def\s+\w*(gaussian|blur|smooth)\w*\s*\(", 1),
        ("background subtraction", r"def\s+\w*(background|subtract)\w*\s*\(", 1),
        ("coarse detection/contour", r"def\s+\w*(coarse|contour|detect.*circle|enclosing)\w*\s*\(", 2),
        ("fine detection/radial scan", r"def\s+\w*(fine|radial|gradient|scan|edge|detect_inner)\w*\s*\(", 2),
        ("MAD/outlier detection", r"def\s+\w*(mad|outlier|robust|statist|sigma)\w*\s*\(", 1),
        ("mask generation", r"def\s+\w*(mask|create_mask|generate_mask)\w*\s*\(", 1),
        ("test entry", r"def\s+\w*(test|run|evaluate|assess)\w*\s*\(", 1),
    ]

    func_score = 0
    func_items: Dict[str, str] = {}
    for desc, pattern, pts in func_checks:
        m = re.search(pattern, combined, re.IGNORECASE)
        if m:
            func_score += pts
            func_items[desc] = f"{pts}/{pts} - found"
        else:
            func_items[desc] = f"0/{pts} - not found"

    func_score = min(func_score, 10)
    total += func_score
    sections["2.2_functions"] = {"score": func_score, "max": 10, "items": func_items}

    # 2.3 Core dependency usage (5 pts)
    dep_score = 0
    dep_items: Dict[str, str] = {}
    deps: List[tuple] = [
        (r"import\s+cv2|from\s+cv2", 2, "OpenCV"),
        (r"import\s+numpy|from\s+numpy", 1, "NumPy"),
        (r"import\s+scipy|from\s+scipy", 1, "SciPy"),
        (r"import\s+(?:tifffile|matplotlib)|from\s+(?:tifffile|matplotlib)", 1, "tifffile/matplotlib"),
    ]
    for pattern, pts, name in deps:
        if re.search(pattern, combined):
            dep_score += pts
            dep_items[name] = f"{pts}/{pts} - used"
        else:
            dep_items[name] = f"0/{pts} - not found"

    dep_score = min(dep_score, 5)
    total += dep_score
    sections["2.3_dependencies"] = {"score": dep_score, "max": 5, "items": dep_items}

    total = min(total, 25)
    return total, {"score": total, "max": 25, "sections": sections}


# ===================================================================
# III. Algorithm Implementation Quality (35 pts) — LLM-as-Judge
# ===================================================================

_ALGO_PROMPT = """\
You are a computer vision expert evaluating a chip ring inner edge detection implementation.

## Task Requirements
The code should implement:
1. Image preprocessing: downsampling (handling 30000×30000 images), Gaussian blur, background subtraction
2. Coarse detection: maximum contour detection, minimum enclosing circle for initial center/radius
3. Fine detection: radial gradient scanning along 360 directions, dual-edge detection (rising/falling), sub-pixel edge refinement
4. Robust statistics: MAD (Median Absolute Deviation), 3-sigma outlier rejection for radius estimation
5. Mask generation: circular mask creation, chord detection, adaptive horizontal cropping based on chords
6. Feature point detection: chord midpoints, high-intensity points, outlier coordinate identification

Performance targets (for reference):
- Process 30000×30000 images within 5 seconds
- Center coordinate error within ±40 pixels
- Radius error inward ≤40 pixels

## Code Files
{file_list}

## Code Content
{code_content}

## Evaluation Dimensions (score each 0-7, integer only)

### 3.1 Preprocessing Pipeline (0-7)
- Does it implement downsampling with configurable scale factor?
- Does it apply Gaussian blur with appropriate kernel size?
- Does it perform background subtraction (e.g., subtract blurred image)?
- Award 7 for excellent complete implementation, 5 for good, 3 for basic, 0 for missing.

### 3.2 Coarse Detection (0-7)
- Does it find contours and identify the largest one?
- Does it compute minimum enclosing circle or equivalent?
- Does it convert coordinates between downsampled and original scales?
- Award 7 for excellent, 5 for good, 3 for basic, 0 for missing.

### 3.3 Fine Detection (0-7)
- Does it implement radial gradient scanning (multiple angles)?
- Does it use gradient-based edge detection (Gaussian derivative, Sobel, etc.)?
- Does it implement dual-edge or threshold-based edge selection?
- Award 7 for excellent, 5 for good, 3 for basic, 0 for missing.

### 3.4 Robust Statistical Analysis (0-7)
- Does it compute MAD (Median Absolute Deviation)?
- Does it apply 3-sigma rule or equivalent outlier rejection?
- Does the final radius estimation use robust statistics?
- Award 7 for excellent, 5 for good, 3 for basic, 0 for missing.

### 3.5 Mask Generation & Feature Detection (0-7)
- Does it create a circular mask of appropriate size?
- Does it detect chords (low-gradient regions on the circle)?
- Does it identify chord midpoints, high-intensity points, outlier points?
- Does it implement chord-adaptive cropping on the mask?
- Award 7 for excellent, 5 for good, 3 for basic, 0 for missing.

Reply ONLY with valid JSON (no markdown fences):
{{"preprocessing": {{"score": 0, "reason": ""}}, "coarse_detection": {{"score": 0, "reason": ""}}, "fine_detection": {{"score": 0, "reason": ""}}, "statistical_analysis": {{"score": 0, "reason": ""}}, "mask_generation": {{"score": 0, "reason": ""}}}}
"""


def _dim3_algorithm_llm(answer_dir: str) -> Tuple[int, dict]:
    all_code = _collect_all_py(answer_dir)
    if not all_code:
        return 0, {"score": 0, "max": 35, "error": "no Python files found"}

    # Build truncated code
    parts: List[str] = []
    for name, content in all_code.items():
        parts.append(f"# ===== {name} =====\n{content[:6000]}")
    combined = "\n\n".join(parts)
    if len(combined) > 30000:
        combined = combined[:30000] + "\n# ... (truncated)"

    prompt = _ALGO_PROMPT.format(
        file_list=", ".join(all_code.keys()),
        code_content=combined,
    )

    config = _get_text_eval_config(answer_dir)
    raw = _call_llm_judge(prompt, config)

    if not raw:
        return _dim3_fallback(all_code)

    result = _parse_json_from_text(raw)
    if not result:
        return _dim3_fallback(all_code)

    score = 0
    items: Dict[str, str] = {}
    for key in ["preprocessing", "coarse_detection", "fine_detection",
                "statistical_analysis", "mask_generation"]:
        entry = result.get(key, {})
        raw_s = entry.get("score", 0)
        if isinstance(raw_s, str):
            try:
                raw_s = int(raw_s)
            except ValueError:
                raw_s = 0
        s = max(0, min(7, int(raw_s)))
        score += s
        items[key] = f"{s}/7 - {entry.get('reason', '')}"

    score = min(score, 35)
    return score, {"score": score, "max": 35, "items": items, "source": "llm"}


def _dim3_fallback(all_code: Dict[str, str]) -> Tuple[int, dict]:
    """Keyword-based conservative scoring when LLM is unavailable."""
    combined = "\n".join(all_code.values()).lower()
    score = 0
    items: Dict[str, str] = {}

    checks: List[tuple] = [
        ("preprocessing", [
            (r"resize|downsample|inter_area|scale_factor", 2),
            (r"gaussianblur|gaussian.*blur|blur", 2),
            (r"background|subtract|cv2\.subtract", 3),
        ]),
        ("coarse_detection", [
            (r"findcontours|contour", 3),
            (r"minenclosingcircle|enclosing.*circle", 2),
            (r"contourarea|largest.*contour|max.*contour", 2),
        ]),
        ("fine_detection", [
            (r"radial|gradient.*scan|scan.*gradient", 3),
            (r"edge.*detect|canny|sobel|threshold", 2),
            (r"linspace.*2.*pi|angles.*linspace|cos.*sin", 2),
        ]),
        ("statistical_analysis", [
            (r"mad|median.*absolute", 3),
            (r"3.*sigma|sigma.*3|outlier", 2),
            (r"np\.median|robust|reject", 2),
        ]),
        ("mask_generation", [
            (r"create.*mask|generate.*mask|mask.*circle", 3),
            (r"cv2\.circle|np\.zeros", 2),
            (r"chord|crop|truncat|low.*region", 2),
        ]),
    ]

    for dim_name, kw_list in checks:
        dim_s = 0
        for pattern, pts in kw_list:
            if re.search(pattern, combined):
                dim_s += pts
        dim_s = min(dim_s, 7)
        score += dim_s
        items[dim_name] = f"{dim_s}/7 - keyword fallback"

    score = min(score, 35)
    return score, {"score": score, "max": 35, "items": items, "source": "fallback"}


# ===================================================================
# IV. Code Engineering Quality (25 pts)
# ===================================================================

def _dim4_engineering(answer_dir: str) -> Tuple[int, dict]:
    all_code = _collect_all_py(answer_dir)
    combined = "\n".join(all_code.values())
    total = 0
    items: Dict[str, str] = {}

    # 4.1 Modular design (5 pts)
    file_count = len(all_code)
    func_count = len(re.findall(r"def\s+\w+\s*\(", combined))
    class_count = len(re.findall(r"class\s+\w+", combined))
    mod_s = 0
    if file_count >= 7:
        mod_s += 3
    elif file_count >= 5:
        mod_s += 2
    elif file_count >= 3:
        mod_s += 1
    if func_count >= 15:
        mod_s += 2
    elif func_count >= 8:
        mod_s += 1
    mod_s = min(mod_s, 5)
    total += mod_s
    items["4.1_modularity"] = f"{mod_s}/5 - {file_count} files, {func_count} funcs, {class_count} classes"

    # 4.2 Documentation & comments (5 pts)
    docstring_count = len(re.findall(r'"""[\s\S]*?"""', combined))
    comment_lines = len(re.findall(r"^\s*#\s*.+", combined, re.MULTILINE))
    doc_s = 0
    if docstring_count >= 10:
        doc_s += 3
    elif docstring_count >= 5:
        doc_s += 2
    elif docstring_count >= 2:
        doc_s += 1
    if comment_lines >= 30:
        doc_s += 2
    elif comment_lines >= 15:
        doc_s += 1
    doc_s = min(doc_s, 5)
    total += doc_s
    items["4.2_documentation"] = f"{doc_s}/5 - {docstring_count} docstrings, {comment_lines} comment lines"

    # 4.3 CLI & logging (5 pts)
    cli_s = 0
    if re.search(r"argparse|ArgumentParser", combined):
        cli_s += 2
    elif re.search(r"sys\.argv", combined):
        cli_s += 1
    if re.search(r"import\s+logging|logging\.\w+|getLogger", combined):
        cli_s += 2
    elif re.search(r"print\s*\(", combined):
        cli_s += 1
    if re.search(r'__name__\s*==\s*["\']__main__["\']', combined):
        cli_s += 1
    cli_s = min(cli_s, 5)
    total += cli_s
    items["4.3_cli_logging"] = f"{cli_s}/5"

    # 4.4 Error handling (5 pts)
    try_count = combined.count("try:")
    err_s = 0
    if try_count >= 5:
        err_s += 3
    elif try_count >= 2:
        err_s += 2
    elif try_count >= 1:
        err_s += 1
    if re.search(
        r"if\s+.*is\s+None|if\s+not\s+os\.path\.exists|raise\s+(ValueError|TypeError|FileNotFoundError)",
        combined,
    ):
        err_s += 2
    elif re.search(r"assert\s+|if\s+not\s+", combined):
        err_s += 1
    err_s = min(err_s, 5)
    total += err_s
    items["4.4_error_handling"] = f"{err_s}/5 - {try_count} try blocks"

    # 4.5 Test module completeness (5 pts)
    test_content = all_code.get("test.py", "")
    test_s = 0
    if test_content:
        if re.search(r"ground.?truth|json\.load|load.*json", test_content, re.IGNORECASE):
            test_s += 2
        if re.search(r"error|deviation|accuracy|precision|abs\s*\(|diff|sqrt", test_content, re.IGNORECASE):
            test_s += 2
        if re.search(r"def\s+\w+", test_content):
            test_s += 1
    test_s = min(test_s, 5)
    total += test_s
    items["4.5_test_module"] = f"{test_s}/5"

    total = min(total, 25)
    return total, {"score": total, "max": 25, "items": items}


# ===================================================================
# Main Entry
# ===================================================================

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Evaluate the agent's output.

    Args:
        answer_dir: Absolute path to the agent's output directory

    Returns:
        (score, report) — score: 0-100 int, report: detailed scoring dict
    """
    s1, r1 = _dim1_file_delivery(answer_dir)
    s2, r2 = _dim2_executability(answer_dir)
    s3, r3 = _dim3_algorithm_llm(answer_dir)
    s4, r4 = _dim4_engineering(answer_dir)

    total = s1 + s2 + s3 + s4
    total = max(0, min(100, total))

    if total >= 90:
        comment = "Excellent — complete implementation with high quality algorithm design."
    elif total >= 75:
        comment = "Good — solid implementation with minor gaps."
    elif total >= 60:
        comment = "Acceptable — basic implementation present but notable weaknesses."
    elif total >= 40:
        comment = "Partial — significant modules or functions missing."
    else:
        comment = "Insufficient — major deliverables missing or code severely incomplete."

    report: Dict[str, Any] = {
        "total_score": total,
        "dim1_file_delivery": r1,
        "dim2_executability": r2,
        "dim3_algorithm_quality": r3,
        "dim4_engineering_quality": r4,
        "comment": comment,
    }
    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print formatted scoring report."""
    print("=" * 70)
    print("pengyichen-query4 Evaluation Report")
    print("Task: Chip Ring Inner Edge Detection Algorithm")
    print("=" * 70)
    print(f"\nTotal Score: {score}/100\n")

    dim_info = [
        ("dim1_file_delivery", "1. File Delivery (15 pts)"),
        ("dim2_executability", "2. Code Executability (25 pts)"),
        ("dim3_algorithm_quality", "3. Algorithm Quality (35 pts)"),
        ("dim4_engineering_quality", "4. Engineering Quality (25 pts)"),
    ]

    for key, title in dim_info:
        sec = report.get(key, {})
        sec_score = sec.get("score", 0)
        sec_max = sec.get("max", 0)
        print("-" * 55)
        print(f"[{title}]  {sec_score}/{sec_max}")
        print("-" * 55)

        # Print items (flat)
        for k, v in sec.get("items", {}).items():
            line = f"{v}" if isinstance(v, str) else str(v)
            if len(line) > 120:
                line = line[:120] + "..."
            print(f"  {k}: {line}")

        # Print sub-sections (nested, e.g. dim2)
        for sub_key, sub_val in sec.get("sections", {}).items():
            sub_s = sub_val.get("score", 0)
            sub_m = sub_val.get("max", 0)
            print(f"\n  [{sub_key}] {sub_s}/{sub_m}")
            for k, v in sub_val.get("items", {}).items():
                line = f"{v}" if isinstance(v, str) else str(v)
                if len(line) > 100:
                    line = line[:100] + "..."
                print(f"    {k}: {line}")

        if sec.get("source"):
            print(f"  (source: {sec['source']})")
        if sec.get("error"):
            print(f"  ERROR: {sec['error']}")
        print()

    print("=" * 55)
    print(f"Comment: {report.get('comment', '')}")
    print("=" * 70)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_dir = sys.argv[1]
    else:
        test_dir = os.path.join(os.path.dirname(__file__), "..", "gpt-5", "attempt_1")

    if not os.path.isabs(test_dir):
        test_dir = os.path.join(os.getcwd(), test_dir)

    if os.path.exists(test_dir):
        print(f"Evaluating: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"Directory not found: {test_dir}")
    sys.exit(0)
