"""
Rubric for en_os_lab3_debug: OS Course Lab3 Debug and Fix

Task: Find and fix bugs in the OS-Course-Lab Lab3 code,
      so the code passes make grade tests, and write a bug_report.md.

Known Bug Information (from wrong.png error screenshot):
  - CMake error: system-servers/tmpfs/CMakeLists.txt cannot find tmpfs.c source file,
    causing tmpfs.srv to have no SOURCES, leading to compilation failure
  - Memory management bug: use-after-free in sys_handle_mprotect() in
    kernel/object/memory.c — obj_put(vmspace) is called before flush_tlb_by_range(vmspace,...)

Correctly passing make grade should output 5 tests (each 20/20):
  Cap Create Pretest, Root Thread Pretest, Userland, Printf, Userland App
  Final Score: 100/100

Total score: 100 points

Scoring dimensions:
I. File Delivery (15 points)
    1. OS-Course-Lab/ directory exists and contains Lab3 subdirectory with source code (10 points)
    2. bug_report.md exists with reasonable content (5 points)

II. make grade Functional Verification (50 points)
    Plan A: When Docker is available, actually run make grade and score by test pass ratio
    Plan B: When Docker is unavailable, check agent-generated grade result files + code completeness

III. Code Modification Quality (15 points)
    1. Key source files exist (7 points): memory.c, CMakeLists.txt, etc.
    2. Evidence of substantive code modifications (8 points): files are non-empty and contain fix-related keywords

IV. Bug Report Quality — LLM-as-Judge (20 points)
    1. Problem description (6 points)
    2. Root cause analysis (8 points)
    3. Fix solution (6 points)
"""

import os
import re
import sys
import json
import subprocess
from typing import Tuple, Dict, Any, List

try:
    import openai
except ImportError:
    openai = None


# ---------------------------------------------------------------------------
# Environment & LLM Utilities
# ---------------------------------------------------------------------------

def _load_env(answer_dir: str) -> dict:
    """Load .env config from answer_dir and the query root directory"""
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
    """Get text evaluation LLM configuration"""
    env = _load_env(answer_dir)

    def g(key: str, default: str = "") -> str:
        return os.environ.get(key) or env.get(key) or default

    return {
        "api_key": g("EVAL_TEXT_API_KEY", g("ANTHROPIC_API_KEY")),
        "api_base": g("EVAL_TEXT_API_BASE_URL", g("ANTHROPIC_BASE_URL")),
        "model": g("EVAL_TEXT_MODEL", "openai/gpt-5.2"),
    }


def _call_llm_judge(prompt: str, config: dict) -> str:
    """Call LLM for text evaluation"""
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


def _read_file(path: str, max_chars: int = 50000) -> str:
    """Safely read file content"""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read(max_chars)
    except Exception:
        return ""


# ---------------------------------------------------------------------------
# Location Helpers
# ---------------------------------------------------------------------------

def _find_os_lab_dir(answer_dir: str) -> str:
    """Find the OS-Course-Lab directory within answer_dir"""
    direct = os.path.join(answer_dir, "OS-Course-Lab")
    if os.path.isdir(direct):
        return direct
    for item in os.listdir(answer_dir):
        p = os.path.join(answer_dir, item)
        if os.path.isdir(p) and "os-course-lab" in item.lower():
            return p
    return ""


def _find_bug_report(answer_dir: str) -> str:
    """Find bug_report.md or similarly named report in answer_dir"""
    exact = os.path.join(answer_dir, "bug_report.md")
    if os.path.isfile(exact):
        return exact
    for f in os.listdir(answer_dir):
        low = f.lower()
        if low.endswith(".md") and any(kw in low for kw in ("bug", "report", "fix", "debug")):
            return os.path.join(answer_dir, f)
    return ""


def _count_source_files(directory: str) -> int:
    """Recursively count .c / .h / .S files"""
    n = 0
    for root, _dirs, files in os.walk(directory):
        for f in files:
            if f.endswith((".c", ".h", ".S", ".s")):
                n += 1
    return n


# ---------------------------------------------------------------------------
# I. File Delivery (15 points)
# ---------------------------------------------------------------------------

def _eval_file_delivery(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details: Dict[str, str] = {}
    deductions: List[str] = []

    # 1.1 OS-Course-Lab directory (10 points)
    lab_dir = _find_os_lab_dir(answer_dir)
    if lab_dir:
        lab3 = os.path.join(lab_dir, "Lab3")
        if os.path.isdir(lab3):
            src_count = _count_source_files(lab3)
            if src_count >= 5:
                score += 10
                details["OS-Course-Lab/Lab3"] = f"10/10 — exists, contains {src_count} source files"
            elif src_count >= 1:
                score += 6
                details["OS-Course-Lab/Lab3"] = f"6/10 — exists but few source files ({src_count})"
                deductions.append(f"Lab3 has few source files ({src_count})")
            else:
                score += 3
                details["OS-Course-Lab/Lab3"] = "3/10 — directory exists but no source code"
                deductions.append("No source code files under Lab3")
        else:
            score += 2
            details["OS-Course-Lab/Lab3"] = "2/10 — OS-Course-Lab exists but missing Lab3"
            deductions.append("Missing Lab3 subdirectory")
    else:
        details["OS-Course-Lab/Lab3"] = "0/10 — OS-Course-Lab directory not found"
        deductions.append("OS-Course-Lab directory not submitted")

    # 1.2 bug_report.md (5 points)
    rp = _find_bug_report(answer_dir)
    if rp:
        content = _read_file(rp)
        clen = len(content)
        if clen >= 500:
            score += 5
            details["bug_report.md"] = f"5/5 — exists ({clen} characters)"
        elif clen >= 100:
            score += 3
            details["bug_report.md"] = f"3/5 — exists but short ({clen} characters)"
            deductions.append("Bug report is too short")
        else:
            score += 1
            details["bug_report.md"] = f"1/5 — exists but nearly empty ({clen} characters)"
            deductions.append("Bug report has very little content")
    else:
        details["bug_report.md"] = "0/5 — not found"
        deductions.append("Missing bug_report.md")

    return score, {"score": f"{score}/15", "details": details, "deductions": deductions}


# ---------------------------------------------------------------------------
# II. make grade Functional Verification (50 points)
# ---------------------------------------------------------------------------

# Known 5 test names (from the reference grade_result.json)
_KNOWN_TESTS = [
    "Cap Create Pretest",
    "Root Thread Pretest",
    "Userland",
    "Printf",
    "Userland App",
]


def _run_docker_grade(lab_dir: str) -> Tuple[bool, str, bool]:
    """Try running make grade via Docker. Returns (success, output, docker_available)

    Note: To avoid destroying the agent's original output (the Docker command contains rm -rf build),
    we copy OS-Course-Lab to a temporary directory before running.
    """
    import shutil
    import tempfile

    lab3 = os.path.join(lab_dir, "Lab3")
    if not os.path.isdir(lab3):
        return False, "Lab3 directory does not exist", False

    # Check if Lab3 has a Makefile (otherwise make grade is meaningless)
    if not os.path.isfile(os.path.join(lab3, "Makefile")) and not os.path.isfile(
        os.path.join(lab3, "CMakeLists.txt")
    ):
        return False, "No Makefile/CMakeLists in Lab3, skipping Docker", False

    tmp_dir = None
    try:
        tmp_dir = tempfile.mkdtemp(prefix="oslab_eval_")
        tmp_lab = os.path.join(tmp_dir, "OS-Course-Lab")
        shutil.copytree(lab_dir, tmp_lab, symlinks=True)

        cmd = [
            "docker", "run", "--rm", "-i", "--platform=linux/amd64",
            "-e", "LAB=3", "-e", "TIMEOUT=20",
            "-v", f"{os.path.abspath(tmp_lab)}:/workspaces/OS-Course-Lab",
            "-w", "/workspaces/OS-Course-Lab/Lab3",
            "ipads/oslab:25.03",
            "bash", "-lc", "set -euxo pipefail; rm -rf build; make DOCKER_RUN= V=2 grade",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        output = (result.stdout + "\n" + result.stderr).strip()
        return result.returncode == 0, output, True
    except FileNotFoundError:
        return False, "Docker not available", False
    except subprocess.TimeoutExpired:
        return False, "Docker command timed out (5 minutes)", True
    except Exception as e:
        return False, str(e), False
    finally:
        if tmp_dir and os.path.isdir(tmp_dir):
            shutil.rmtree(tmp_dir, ignore_errors=True)


def _parse_grade_output(output: str) -> dict:
    """Parse scores from make grade output"""
    result = {"score": 0, "passed": 0, "total": 0, "tests": []}
    for line in output.split("\n"):
        line = line.strip()
        # "Score: 100/100"
        m = re.match(r"Score:\s*(\d+)/(\d+)", line, re.IGNORECASE)
        if m:
            result["score"] = int(m.group(1))
            result["total_score"] = int(m.group(2))
        # Each sub-test: e.g. "Cap Create Pretest: 20/20"
        m2 = re.match(r"(.+?):\s*(\d+)/(\d+)", line)
        if m2:
            name, got, full = m2.group(1).strip(), int(m2.group(2)), int(m2.group(3))
            if name.lower() != "score":
                result["tests"].append({"name": name, "score": got, "max": full})
                if got >= full:
                    result["passed"] += 1
                result["total"] += 1
    return result


def _find_agent_grade_results(lab_dir: str) -> dict:
    """Search for grade result files produced by the agent"""
    info: Dict[str, Any] = {"found": False, "score": 0, "passed": 0, "total": 0, "source": ""}
    search = [
        os.path.join(lab_dir, "Lab3", "build"),
        os.path.join(lab_dir, "Lab3"),
        lab_dir,
    ]
    for d in search:
        # JSON format
        jp = os.path.join(d, "grade_result.json")
        if os.path.isfile(jp):
            try:
                with open(jp, "r") as f:
                    data = json.load(f)
                info["found"] = True
                info["score"] = int(data.get("score", 0))
                info["passed"] = int(data.get("passed", 0))
                info["total"] = int(data.get("total", 0))
                info["status"] = data.get("status", "")
                info["source"] = jp
                return info
            except Exception:
                pass
        # TXT format
        tp = os.path.join(d, "grade_result.txt")
        if os.path.isfile(tp):
            content = _read_file(tp, 2000)
            info["found"] = True
            info["source"] = tp
            for line in content.split("\n"):
                line = line.strip()
                if line.startswith("score="):
                    try:
                        info["score"] = int(line.split("=", 1)[1])
                    except ValueError:
                        pass
                if line.startswith("passed="):
                    try:
                        info["passed"] = int(line.split("=", 1)[1])
                    except ValueError:
                        pass
                if line.startswith("total="):
                    try:
                        info["total"] = int(line.split("=", 1)[1])
                    except ValueError:
                        pass
                if line.startswith("status="):
                    info["status"] = line.split("=", 1)[1]
            if info["score"] > 0:
                return info
        # Plain score file
        sp = os.path.join(d, "score")
        if os.path.isfile(sp):
            try:
                val = int(_read_file(sp, 100).strip())
                info["found"] = True
                info["score"] = val
                info["source"] = sp
                return info
            except ValueError:
                pass
    # Also check local_grade_output.txt
    for d in search:
        lp = os.path.join(d, "local_grade_output.txt")
        if os.path.isfile(lp):
            content = _read_file(lp, 5000)
            m = re.search(r"SCORE:\s*(\d+)", content, re.IGNORECASE)
            if m:
                info["found"] = True
                info["score"] = int(m.group(1))
                info["source"] = lp
                pm = re.search(r"(\d+)/(\d+)\s*passed", content, re.IGNORECASE)
                if pm:
                    info["passed"] = int(pm.group(1))
                    info["total"] = int(pm.group(2))
                return info
    return info


def _eval_make_grade(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details: Dict[str, Any] = {}
    deductions: List[str] = []

    lab_dir = _find_os_lab_dir(answer_dir)
    if not lab_dir:
        return 0, {"score": "0/50", "details": {"error": "No OS-Course-Lab directory"}, "deductions": ["Cannot evaluate"]}

    # Save agent self-test results first (Docker's rm -rf build will delete them)
    pre_grade = _find_agent_grade_results(lab_dir)

    # Plan A: Docker
    success, output, docker_ok = _run_docker_grade(lab_dir)
    if docker_ok and success:
        parsed = _parse_grade_output(output)
        gs = parsed.get("score", 0)
        if gs >= 100:
            score = 50
            details["Docker make grade"] = f"50/50 — PASS, Score: {gs}/100"
        elif gs >= 60:
            score = int(gs * 50 / 100)
            details["Docker make grade"] = f"{score}/50 — partially passed, Score: {gs}/100"
            deductions.append(f"make grade score {gs}/100, not full marks")
        elif gs > 0:
            score = max(5, int(gs * 50 / 100))
            details["Docker make grade"] = f"{score}/50 — low score, Score: {gs}/100"
            deductions.append(f"make grade score too low: {gs}/100")
        else:
            tests = parsed.get("tests", [])
            if tests:
                total_pts = sum(t["score"] for t in tests)
                total_max = sum(t["max"] for t in tests)
                ratio = total_pts / total_max if total_max else 0
                score = max(5, int(ratio * 50))
                details["Docker make grade"] = f"{score}/50 — test score {total_pts}/{total_max}"
            else:
                score = 5
                details["Docker make grade"] = "5/50 — command succeeded but could not parse score"
            deductions.append("make grade output parsing anomaly")
        return score, {"score": f"{score}/50", "details": details, "deductions": deductions}

    # Docker failed or unavailable -> use fallback evaluation
    if docker_ok:
        # Docker available but make grade failed
        # First check if Docker output has partial scores
        parsed = _parse_grade_output(output)
        tests = parsed.get("tests", [])
        if tests:
            total_pts = sum(t["score"] for t in tests)
            total_max = sum(t["max"] for t in tests)
            ratio = total_pts / total_max if total_max else 0
            docker_partial = max(0, int(ratio * 50))
            if docker_partial > 0:
                score = docker_partial
                details["Docker make grade"] = f"{score}/50 — some tests passed {total_pts}/{total_max}"
                deductions.append("make grade tests not all passed")
                return score, {"score": f"{score}/50", "details": details, "deductions": deductions}
        details["Docker make grade"] = "FAIL (compilation or test failure)"
        details["error_output_snippet"] = output[-400:] if len(output) > 400 else output
    else:
        details["Docker status"] = "unavailable"

    # Fallback evaluation: Agent-generated grade results + code completeness
    # Agent self-test results (0-30 points) — using results saved before Docker run
    grade = pre_grade
    b1 = 0
    if grade["found"]:
        gs = grade["score"]
        if gs >= 100:
            b1 = 30
            details["agent_self_test"] = f"30/30 — PASS, Score={gs}"
        elif gs >= 60:
            b1 = int(gs * 30 / 100)
            details["agent_self_test"] = f"{b1}/30 — Score={gs}"
            deductions.append(f"Agent self-test not full marks: {gs}")
        elif gs > 0:
            b1 = max(3, int(gs * 30 / 100))
            details["agent_self_test"] = f"{b1}/30 — low Score={gs}"
            deductions.append(f"Agent self-test score low: {gs}")
        else:
            details["agent_self_test"] = "0/30 — result file exists but score is 0"
            deductions.append("Agent self-test score is 0")
    else:
        details["agent_self_test"] = "0/30 — no grade result file found"
        deductions.append("Agent did not produce make grade results")

    score += b1

    # Code completeness (0-20 points)
    lab3 = os.path.join(lab_dir, "Lab3")
    b2 = 0
    if os.path.isdir(lab3):
        src_n = _count_source_files(lab3)
        has_kernel = os.path.isdir(os.path.join(lab3, "kernel"))
        has_makefile = os.path.isfile(os.path.join(lab3, "Makefile")) or os.path.isfile(
            os.path.join(lab3, "CMakeLists.txt")
        )
        if src_n >= 10 and has_kernel and has_makefile:
            b2 = 20
            details["code_completeness"] = f"20/20 — {src_n} source files, kernel/ + Makefile"
        elif src_n >= 5 and has_kernel:
            b2 = 15
            details["code_completeness"] = f"15/20 — {src_n} source files, kernel/ exists"
        elif src_n >= 1:
            b2 = 8
            details["code_completeness"] = f"8/20 — {src_n} source files"
            deductions.append("Lab3 code is incomplete")
        else:
            details["code_completeness"] = "0/20 — Lab3 has no source code"
            deductions.append("No source code under Lab3 directory")
    else:
        details["code_completeness"] = "0/20 — Lab3 directory does not exist"
        deductions.append("Lab3 directory does not exist")

    score += b2
    score = min(50, score)
    return score, {"score": f"{score}/50", "details": details, "deductions": deductions}


# ---------------------------------------------------------------------------
# III. Code Modification Quality (15 points)
# ---------------------------------------------------------------------------

# Key files and corresponding point values
_KEY_FILES: List[Tuple[str, int, List[str]]] = [
    # (path relative to Lab3, points, fix-related keywords)
    ("kernel/object/memory.c", 3, [
        "flush_tlb", "obj_put", "vmspace", "mprotect",
    ]),
]

# Check for CMake/tmpfs fix — path may be in user-space side
_CMAKE_PATTERNS: List[Tuple[str, int]] = [
    ("**/tmpfs/CMakeLists.txt", 2),
    ("**/tmpfs/tmpfs.c", 2),
]


def _glob_match(base: str, pattern: str) -> List[str]:
    """Simple recursive glob matching"""
    import fnmatch
    results = []
    for root, _dirs, files in os.walk(base):
        for f in files:
            full = os.path.join(root, f)
            rel = os.path.relpath(full, base)
            if fnmatch.fnmatch(rel, pattern):
                results.append(full)
    return results


def _eval_code_quality(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details: Dict[str, str] = {}
    deductions: List[str] = []

    lab_dir = _find_os_lab_dir(answer_dir)
    if not lab_dir:
        return 0, {"score": "0/15", "details": {"error": "No OS-Course-Lab"}, "deductions": ["Cannot evaluate"]}

    lab3 = os.path.join(lab_dir, "Lab3")
    if not os.path.isdir(lab3):
        return 0, {"score": "0/15", "details": {"error": "No Lab3"}, "deductions": ["Lab3 does not exist"]}

    # 3.1 Key source files exist (7 points)
    key_pts = 0

    # memory.c (3 points)
    mem_path = os.path.join(lab3, "kernel", "object", "memory.c")
    if os.path.isfile(mem_path):
        content = _read_file(mem_path, 50000)
        if len(content) > 200:
            key_pts += 3
            details["kernel/object/memory.c"] = f"3/3 — exists ({len(content)} characters)"
        else:
            key_pts += 1
            details["kernel/object/memory.c"] = "1/3 — exists but content is very short"
    else:
        details["kernel/object/memory.c"] = "0/3 — not found"

    # tmpfs CMakeLists.txt (2 points)
    cmake_hits = _glob_match(lab3, "**/tmpfs/CMakeLists.txt")
    if cmake_hits:
        content = _read_file(cmake_hits[0], 10000)
        if "tmpfs" in content.lower():
            key_pts += 2
            details["tmpfs/CMakeLists.txt"] = "2/2 — exists"
        else:
            key_pts += 1
            details["tmpfs/CMakeLists.txt"] = "1/2 — exists but content is suspicious"
    else:
        details["tmpfs/CMakeLists.txt"] = "0/2 — not found"

    # tmpfs.c source file (2 points)
    tmpfs_hits = _glob_match(lab3, "**/tmpfs/tmpfs.c")
    if tmpfs_hits:
        content = _read_file(tmpfs_hits[0], 10000)
        if len(content) > 100:
            key_pts += 2
            details["tmpfs/tmpfs.c"] = f"2/2 — exists ({len(content)} characters)"
        else:
            key_pts += 1
            details["tmpfs/tmpfs.c"] = "1/2 — exists but content is very short"
    else:
        details["tmpfs/tmpfs.c"] = "0/2 — not found"

    score += min(7, key_pts)

    # 3.2 Fix evidence check (8 points)
    fix_pts = 0

    # Check for fix keywords in memory.c
    if os.path.isfile(mem_path):
        mc = _read_file(mem_path, 50000).lower()
        # Key fix: call order of flush_tlb and obj_put
        has_flush = "flush_tlb" in mc
        has_obj_put = "obj_put" in mc
        has_mprotect = "mprotect" in mc
        if has_flush and has_obj_put and has_mprotect:
            fix_pts += 4
            details["memory.c fix keywords"] = "4/4 — contains flush_tlb / obj_put / mprotect"
        elif has_flush or has_obj_put:
            fix_pts += 2
            details["memory.c fix keywords"] = "2/4 — some keywords present"
        else:
            details["memory.c fix keywords"] = "0/4 — fix-related keywords not detected"
            deductions.append("memory.c lacks key fix-related code")
    else:
        details["memory.c fix keywords"] = "0/4 — file does not exist"
        deductions.append("memory.c does not exist, cannot check fix")

    # Check if tmpfs CMakeLists references tmpfs.c
    if cmake_hits:
        cc = _read_file(cmake_hits[0], 10000)
        if "tmpfs.c" in cc:
            fix_pts += 4
            details["CMakeLists tmpfs fix"] = "4/4 — CMakeLists references tmpfs.c"
        elif "tmpfs" in cc.lower():
            fix_pts += 2
            details["CMakeLists tmpfs fix"] = "2/4 — CMakeLists mentions tmpfs but not explicitly tmpfs.c"
        else:
            details["CMakeLists tmpfs fix"] = "0/4 — CMakeLists does not reference tmpfs source file"
            deductions.append("CMakeLists.txt does not correctly reference tmpfs source file")
    else:
        details["CMakeLists tmpfs fix"] = "0/4 — CMakeLists does not exist"
        deductions.append("tmpfs CMakeLists.txt does not exist, cannot check fix")

    score += min(8, fix_pts)
    return score, {"score": f"{score}/15", "details": details, "deductions": deductions}


# ---------------------------------------------------------------------------
# IV. Bug Report Quality — LLM-as-Judge (20 points)
# ---------------------------------------------------------------------------

_REPORT_EVAL_PROMPT = """\
You are a teaching assistant for an operating systems course, evaluating a student's bug analysis report.

Task Background:
The student needs to find and fix bugs in Lab3 of OS-Course-Lab (ChCore OS lab),
so the code passes make grade (5 tests: Cap Create Pretest, Root Thread Pretest,
Userland, Printf, Userland App, each worth 20 points, total 100).

Known bugs include but are not limited to:
1. **CMake configuration error**: system-servers/tmpfs/CMakeLists.txt is missing the tmpfs.c source file,
   causing tmpfs.srv to have no SOURCES, leading to compilation failure.
2. **Use-after-free**: In kernel/object/memory.c, sys_handle_mprotect()
   calls obj_put(vmspace) to release the reference first, then calls flush_tlb_by_range(vmspace, ...),
   resulting in access to already-freed memory.

Please evaluate the report quality along the following three dimensions, giving an integer score for each:

**Dimension 1: Problem Description (0-6 points)**
- 6: Clearly describes bug symptoms (compilation error / runtime crash / test failure) with specific file and function names
- 4: Has description but lacks specific locations
- 2: Vague description
- 0: No description

**Dimension 2: Root Cause Analysis (0-8 points)**
- 8: In-depth analysis of the bug's root cause (e.g., CMakeLists missing source file, use-after-free object lifetime issue),
     technically correct and thorough analysis
- 5: Some analysis but not thorough enough or partially inaccurate
- 2: Surface-level description only
- 0: No root cause analysis

**Dimension 3: Fix Solution (0-6 points)**
- 6: Clearly explains the fix method, including specific code change descriptions or diff, solution is correct and reasonable
- 4: Has fix solution but not detailed enough
- 2: Briefly mentions fix
- 0: No fix solution

Please respond strictly in the following JSON format (do not include other content):
```json
{{
  "problem_description": {{"score": 0, "reason": ""}},
  "root_cause_analysis": {{"score": 0, "reason": ""}},
  "fix_solution": {{"score": 0, "reason": ""}},
  "total": 0,
  "overall_comment": ""
}}
```

Below is the student's bug report:

---
{report_content}
---
"""


def _eval_bug_report(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details: Dict[str, str] = {}
    deductions: List[str] = []

    rp = _find_bug_report(answer_dir)
    if not rp:
        return 0, {"score": "0/20", "details": {"error": "Report not found"}, "deductions": ["Missing bug report"]}

    content = _read_file(rp, 30000)
    if len(content) < 50:
        return 0, {"score": "0/20", "details": {"error": "Report is nearly empty"}, "deductions": ["Bug report has insufficient content"]}

    # Try LLM evaluation
    config = _get_text_eval_config(answer_dir)
    prompt = _REPORT_EVAL_PROMPT.format(report_content=content[:15000])
    llm_resp = _call_llm_judge(prompt, config)

    if llm_resp:
        try:
            text = llm_resp
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            result = json.loads(text)

            pd = max(0, min(6, int(result.get("problem_description", {}).get("score", 0))))
            rc = max(0, min(8, int(result.get("root_cause_analysis", {}).get("score", 0))))
            fs = max(0, min(6, int(result.get("fix_solution", {}).get("score", 0))))
            score = pd + rc + fs

            details["problem_description"] = f"{pd}/6 — {result.get('problem_description', {}).get('reason', '')}"
            details["root_cause_analysis"] = f"{rc}/8 — {result.get('root_cause_analysis', {}).get('reason', '')}"
            details["fix_solution"] = f"{fs}/6 — {result.get('fix_solution', {}).get('reason', '')}"
            details["overall_comment"] = result.get("overall_comment", "")
            details["evaluation_model"] = config.get("model", "unknown")

            if pd <= 2:
                deductions.append("Problem description is unclear")
            if rc <= 2:
                deductions.append("Lacks in-depth root cause analysis")
            if fs <= 2:
                deductions.append("Fix solution is insufficient")

            return score, {"score": f"{score}/20", "details": details, "deductions": deductions}

        except (json.JSONDecodeError, KeyError, TypeError) as e:
            print(f"[RUBRIC] LLM response parsing failed: {e}")
            details["LLM_parse_failure"] = str(e)

    # Fallback: keyword matching (max 14/20)
    details["evaluation_method"] = "fallback: keyword matching (LLM unavailable)"
    cl = content.lower()

    # Problem description (0-6)
    pd_score = 0
    symptom_kw = ["bug", "error", "issue", "problem", "fail", "crash", "cmake", "compile"]
    location_kw = ["memory.c", "tmpfs", "cmake", "kernel/", "lab3", "mprotect", "function"]
    if any(k in cl for k in symptom_kw):
        pd_score += 2
    if any(k in cl for k in location_kw):
        pd_score += 2
    if len(content) >= 800:
        pd_score += 2
    pd_score = min(6, pd_score)

    # Root cause analysis (0-8)
    cause_kw = [
        "use-after-free", "obj_put", "flush_tlb", "lifetime",
        "refcount", "reference count", "cmakelist", "source file", "tmpfs.c",
        "root cause", "cause", "because", "due to", "release",
    ]
    cause_count = sum(1 for k in cause_kw if k in cl)
    if cause_count >= 5:
        rc_score = 6
    elif cause_count >= 3:
        rc_score = 4
    elif cause_count >= 1:
        rc_score = 2
    else:
        rc_score = 0

    # Fix solution (0-6)
    fix_kw = [
        "fix", "repair", "modify", "resolve", "patch", "reorder",
        "obj_put", "flush", "add", "include", "tmpfs.c",
    ]
    fix_count = sum(1 for k in fix_kw if k in cl)
    if fix_count >= 4:
        fs_score = 4
    elif fix_count >= 2:
        fs_score = 3
    elif fix_count >= 1:
        fs_score = 1
    else:
        fs_score = 0

    score = min(14, pd_score + rc_score + fs_score)
    details["problem_description (keywords)"] = f"{pd_score}/6"
    details["root_cause_analysis (keywords)"] = f"{rc_score}/8"
    details["fix_solution (keywords)"] = f"{fs_score}/6"
    if score < 8:
        deductions.append("Bug report content insufficient (fallback evaluation)")

    return score, {"score": f"{score}/20", "details": details, "deductions": deductions}


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Evaluate the agent's output.

    Args:
        answer_dir: Absolute path to the agent's output directory

    Returns:
        (score, report)
        - score: integer from 0-100
        - report: dict containing the detailed evaluation report
    """
    print(f"[RUBRIC] Evaluation directory: {answer_dir}")
    print("=" * 60)

    if not os.path.isdir(answer_dir):
        return 0, {"error": f"Answer directory does not exist: {answer_dir}"}

    s1, r1 = _eval_file_delivery(answer_dir)
    s2, r2 = _eval_make_grade(answer_dir)
    s3, r3 = _eval_code_quality(answer_dir)
    s4, r4 = _eval_bug_report(answer_dir)

    total = min(100, s1 + s2 + s3 + s4)

    all_deductions = (
        r1.get("deductions", [])
        + r2.get("deductions", [])
        + r3.get("deductions", [])
        + r4.get("deductions", [])
    )

    if total >= 90:
        comment = "Excellent: Code fix successful, bug report is thorough."
    elif total >= 70:
        comment = "Good: Task mostly completed, some dimensions have room for improvement."
    elif total >= 50:
        comment = "Passing: Some fix work done, but verification insufficient or report quality lacking."
    elif total >= 30:
        comment = "Partially completed: Files submitted but fix results are unsatisfactory."
    else:
        comment = "Failing: Task completion is severely insufficient."

    report = {
        "result_score": {
            "score": total,
            "max_score": 100,
            "deductions": all_deductions,
        },
        "process_score": {
            "score": 0,
            "max_score": 0,
            "deductions": [],
        },
        "comment": comment,
        "breakdown": {
            "I. File Delivery": r1.get("score", "0/15"),
            "II. make grade Test": r2.get("score", "0/50"),
            "III. Code Modification Quality": r3.get("score", "0/15"),
            "IV. Bug Report Quality": r4.get("score", "0/20"),
        },
        "breakdown_details": {
            "I. File Delivery (15 pts)": r1.get("details", {}),
            "II. make grade Test (50 pts)": r2.get("details", {}),
            "III. Code Modification Quality (15 pts)": r3.get("details", {}),
            "IV. Bug Report Quality (20 pts)": r4.get("details", {}),
        },
    }

    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print a formatted scoring report"""
    print()
    print("=" * 60)
    print("OS Lab3 Bug Fix — Scoring Report")
    print("=" * 60)
    print(f"\nTotal Score: {score}/100")

    scores_map = report.get("breakdown", {})
    if scores_map:
        print("\nBreakdown:")
        for k, v in scores_map.items():
            print(f"  {k}: {v}")

    detail_map = report.get("breakdown_details", {})
    for section, items in detail_map.items():
        print(f"\n{'─' * 50}")
        print(f"[{section}]")
        print(f"{'─' * 50}")
        if isinstance(items, dict):
            for k, v in items.items():
                print(f"  {k}: {v}")
        else:
            print(f"  {items}")

    result_info = report.get("result_score", {})
    deds = result_info.get("deductions", [])
    if deds:
        print(f"\nDeductions:")
        for i, d in enumerate(deds, 1):
            print(f"  {i}. {d}")

    print(f"\nComment: {report.get('comment', '')}")
    print("=" * 60)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_dir = sys.argv[1]
    else:
        test_dir = os.path.join(os.path.dirname(__file__), "..", "gpt-5", "attempt_1")

    if not os.path.isabs(test_dir):
        test_dir = os.path.join(os.path.dirname(__file__), "..", test_dir)

    test_dir = os.path.abspath(test_dir)
    print(f"Evaluation directory: {test_dir}\n")

    if os.path.isdir(test_dir):
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"Directory does not exist: {test_dir}")
    sys.exit(0)
