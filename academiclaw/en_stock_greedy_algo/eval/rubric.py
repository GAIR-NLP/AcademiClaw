"""
en_stock_greedy_algo Scoring Script
Task: Stock Trading Maximum Profit - Regret-Based Greedy Algorithm C++ Implementation

Total: 100 points

Dimensions:
  1. File Delivery        10 pts  - solution.cpp exists and non-empty
  2. Compilation Check    15 pts  - g++ -std=c++17 compiles successfully
  3. Code Quality         15 pts  - long long / greedy or heap logic / I/O standards
  4. Functional Correctness 60 pts  - Comparison against eval/example.cpp reference solution
"""

import os
import re
import random
import subprocess
import tempfile
from pathlib import Path
from typing import Tuple, Dict, Any, List


# ---------------------------------------------------------------------------
# Utility Functions
# ---------------------------------------------------------------------------

def _compile(src: str, out: str, extra_flags: List[str] = None) -> Tuple[bool, str]:
    """Compile C++ source code, return (success, error_message)"""
    cmd = ["g++", src, "-o", out, "-std=c++17", "-O2"]
    if extra_flags:
        cmd.extend(extra_flags)
    try:
        proc = subprocess.run(cmd, capture_output=True, timeout=30)
        if proc.returncode == 0:
            return True, ""
        return False, proc.stderr.decode("utf-8", errors="replace")[:500]
    except subprocess.TimeoutExpired:
        return False, "Compilation timed out (>30s)"
    except FileNotFoundError:
        return False, "g++ not installed"
    except Exception as e:
        return False, str(e)[:300]


def _run(exe: str, stdin_data: str, timeout: float = 5.0) -> Tuple[bool, str]:
    """Run an executable, return (success, stdout or error description)"""
    try:
        proc = subprocess.run(
            [exe], input=stdin_data.encode(), capture_output=True, timeout=timeout
        )
        if proc.returncode == 0:
            return True, proc.stdout.decode("utf-8", errors="replace").strip()
        return False, f"Exit code {proc.returncode}"
    except subprocess.TimeoutExpired:
        return False, "TLE"
    except Exception as e:
        return False, str(e)[:200]


# ---------------------------------------------------------------------------
# 1. File Delivery (10 points)
# ---------------------------------------------------------------------------

def _score_file_delivery(answer_dir: str) -> Tuple[int, dict]:
    sol = os.path.join(answer_dir, "solution.cpp")
    if not os.path.exists(sol):
        others = [f for f in os.listdir(answer_dir) if f.endswith(".cpp")]
        if others:
            return 0, {"solution.cpp": f"0/10 - solution.cpp not found, but found: {others}"}
        return 0, {"solution.cpp": "0/10 - No .cpp files found"}
    size = os.path.getsize(sol)
    if size == 0:
        return 0, {"solution.cpp": "0/10 - File is empty"}
    if size < 50:
        return 3, {"solution.cpp": f"3/10 - File too small ({size} B)"}
    return 10, {"solution.cpp": f"10/10 - Exists ({size} B)"}


# ---------------------------------------------------------------------------
# 2. Compilation Check (15 points)
# ---------------------------------------------------------------------------

def _score_compilation(answer_dir: str, tmp: str) -> Tuple[int, dict, str]:
    """Return (score, details, student executable path or empty string)"""
    sol = os.path.join(answer_dir, "solution.cpp")
    if not os.path.exists(sol):
        return 0, {"compilation": "0/15 - solution.cpp does not exist"}, ""
    exe = os.path.join(tmp, "stu")
    ok, err = _compile(sol, exe)
    if ok:
        return 15, {"compilation": "15/15 - Compilation successful"}, exe
    return 0, {"compilation": f"0/15 - Compilation failed: {err[:200]}"}, ""


# ---------------------------------------------------------------------------
# 3. Code Quality (15 points)
# ---------------------------------------------------------------------------

def _score_code_quality(answer_dir: str) -> Tuple[int, dict]:
    sol = os.path.join(answer_dir, "solution.cpp")
    if not os.path.exists(sol):
        return 0, {"code_quality": "0/15 - No file"}
    try:
        with open(sol, "r", encoding="utf-8", errors="replace") as f:
            code = f.read()
    except Exception as e:
        return 0, {"code_quality": f"0/15 - Read failed: {e}"}

    pts = 0
    detail: Dict[str, str] = {}

    # 3a. long long usage (5 points)
    if "long long" in code:
        pts += 5
        detail["long long"] = "5/5"
    elif "int64_t" in code or "#define ll" in code.lower():
        pts += 3
        detail["long long"] = "3/5 - Using alternative type"
    else:
        detail["long long"] = "0/5 - No long long used, may overflow on large data"

    # 3b. Greedy / priority queue logic (5 points)
    lo = code.lower()
    has_pq = "priority_queue" in code
    has_heap_like = has_pq or "heap" in lo or "pq" in lo
    has_push_pop = ("push" in code) and ("pop" in code or "top" in code)
    has_greedy_keyword = bool(re.search(r"price|buy|sell|profit|fee|cost|greedy|regret", lo))

    if has_pq and has_push_pop:
        pts += 5
        detail["algorithm_logic"] = "5/5 - priority_queue + regret operations"
    elif has_heap_like and has_push_pop:
        pts += 4
        detail["algorithm_logic"] = "4/5 - Heap structure + push/pop"
    elif has_greedy_keyword:
        pts += 3
        detail["algorithm_logic"] = "3/5 - Contains greedy/trading keywords but no heap"
    elif "for" in code or "while" in code:
        pts += 1
        detail["algorithm_logic"] = "1/5 - Has loop structure but no greedy/heap detected"
    else:
        detail["algorithm_logic"] = "0/5 - No algorithm logic detected"

    # 3c. I/O (5 points)
    has_in = "cin" in code or "scanf" in code
    has_out = "cout" in code or "printf" in code
    has_fast = "sync_with_stdio" in code or "ios::" in code
    io = 0
    if has_in and has_out:
        io += 3
    elif has_in or has_out:
        io += 1
    if has_fast:
        io += 2
    io = min(io, 5)
    pts += io
    parts = []
    if has_in and has_out:
        parts.append("I/O complete")
    if has_fast:
        parts.append("fast I/O")
    detail["I/O"] = f"{io}/5 - {', '.join(parts) if parts else 'incomplete'}"

    return pts, detail


# ---------------------------------------------------------------------------
# 4. Functional Correctness - Comparison Testing (60 points)
# ---------------------------------------------------------------------------

def _make_test_cases() -> List[str]:
    """Generate a set of test data (fixed + random)"""
    cases: List[str] = []

    # --- Boundary / manual test cases ---
    cases.append("1 0\n42")                              # Single day
    cases.append("2 0\n1 2")                              # Two days with profit
    cases.append("2 5\n1 2")                              # Fee eats up profit
    cases.append("5 0\n5 4 3 2 1")                        # Monotonically decreasing
    cases.append("5 0\n1 2 3 4 5")                        # Monotonically increasing
    cases.append("3 0\n1 1000000 1")                      # Large price difference
    cases.append("4 1000000\n1 2 3 4")                    # Very large fee
    cases.append("2 0\n1000000 1000000")                  # Same prices
    cases.append("10 5\n" + " ".join(["100"] * 10))       # All same
    cases.append("6 1\n1 3 2 8 4 9")                      # Requires regret
    cases.append("9 0\n10 5 4 7 9 12 6 2 10")             # Example
    cases.append("10 0\n" + " ".join(                     # Alternating up/down
        [str(100 + ((-1) ** i) * 50) for i in range(10)]
    ))

    # --- Random small scale ---
    rng = random.Random(2024)
    for _ in range(10):
        n = rng.randint(2, 50)
        c = rng.randint(0, 50)
        prices = [rng.randint(1, 1000) for _ in range(n)]
        cases.append(f"{n} {c}\n" + " ".join(map(str, prices)))

    # --- Random medium scale ---
    for _ in range(5):
        n = rng.randint(100, 1000)
        c = rng.randint(0, 200)
        prices = [rng.randint(1, 100000) for _ in range(n)]
        cases.append(f"{n} {c}\n" + " ".join(map(str, prices)))

    # --- Random large scale ---
    for _ in range(3):
        n = rng.randint(10000, 50000)
        c = rng.randint(0, 1000)
        prices = [rng.randint(1, 1000000) for _ in range(n)]
        cases.append(f"{n} {c}\n" + " ".join(map(str, prices)))

    return cases


def _score_correctness(stu_exe: str, tmp: str) -> Tuple[int, dict]:
    if not stu_exe:
        return 0, {"comparison": "0/60 - No executable student program"}

    # Compile reference solution (eval/example.cpp)
    ref_src = str(Path(__file__).parent.resolve() / "example.cpp")
    if not os.path.exists(ref_src):
        return 0, {"comparison": "0/60 - Missing reference solution example.cpp"}
    ref_exe = os.path.join(tmp, "ref")
    ok, err = _compile(ref_src, ref_exe)
    if not ok:
        return 0, {"comparison": f"0/60 - Reference solution compilation failed: {err[:200]}"}

    test_cases = _make_test_cases()
    total = len(test_cases)
    passed = 0
    tle_cnt = 0
    wrong: List[str] = []

    for idx, inp in enumerate(test_cases):
        ref_ok, ref_out = _run(ref_exe, inp)
        if not ref_ok:
            total -= 1  # Reference solution itself failed, skip
            continue

        stu_ok, stu_out = _run(stu_exe, inp)
        if not stu_ok:
            if stu_out == "TLE":
                tle_cnt += 1
            if len(wrong) < 5:
                header = inp.split("\n")[0]
                wrong.append(f"Case {idx + 1} ({header}): Execution failed - {stu_out}")
            continue

        if stu_out == ref_out:
            passed += 1
        else:
            if len(wrong) < 5:
                header = inp.split("\n")[0]
                wrong.append(
                    f"Case {idx + 1} ({header}): Expected={ref_out}, Actual={stu_out}"
                )

    if total == 0:
        return 0, {"comparison": "0/60 - No valid test cases"}

    rate = passed / total
    score = int(rate * 60)

    detail: Dict[str, Any] = {
        "pass_rate": f"{passed}/{total} ({rate * 100:.1f}%)",
        "score": f"{score}/60",
    }
    if tle_cnt:
        detail["timed_out_cases"] = tle_cnt
    if wrong:
        detail["failed_cases (first 5)"] = wrong

    return score, detail


# ===========================================================================
# Public Interface
# ===========================================================================

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Evaluate the agent's output.

    Args:
        answer_dir: Absolute path to the agent output directory

    Returns:
        (score, report)
        - score: integer 0-100
        - report: dict containing detailed evaluation report
    """
    with tempfile.TemporaryDirectory(prefix="rubric_") as tmp:
        s1, r1 = _score_file_delivery(answer_dir)
        s2, r2, stu_exe = _score_compilation(answer_dir, tmp)
        s3, r3 = _score_code_quality(answer_dir)
        s4, r4 = _score_correctness(stu_exe, tmp)

    total = s1 + s2 + s3 + s4
    report: Dict[str, Any] = {
        "total_score": total,
        "dimension_scores": {
            "1. File Delivery (10)": s1,
            "2. Compilation Check (15)": s2,
            "3. Code Quality (15)": s3,
            "4. Functional Correctness (60)": s4,
        },
        "details": {
            "1. File Delivery": r1,
            "2. Compilation Check": r2,
            "3. Code Quality": r3,
            "4. Functional Correctness": r4,
        },
    }
    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print a formatted scoring report"""
    sep = "=" * 60
    print(sep)
    print("Stock Trading Regret-Based Greedy Algorithm - Scoring Report")
    print(sep)
    print(f"\nTotal Score: {score}/100\n")

    for dim, pts in report.get("dimension_scores", {}).items():
        max_pt = dim.split("(")[1].rstrip(")") if "(" in dim else "?"
        print(f"  {dim}: {pts}/{max_pt}")
    print()

    for section, detail in report.get("details", {}).items():
        print(f"--- {section} ---")
        if isinstance(detail, dict):
            for k, v in detail.items():
                if isinstance(v, list):
                    print(f"  {k}:")
                    for item in v:
                        print(f"    - {item}")
                else:
                    print(f"  {k}: {v}")
        else:
            print(f"  {detail}")
        print()

    print(sep)


# ===========================================================================
# Command Line Entry
# ===========================================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = os.path.join(os.path.dirname(__file__), "..", "gpt-5", "attempt_1")

    if not os.path.isabs(target):
        target = os.path.join(os.path.dirname(__file__), "..", target)

    if os.path.exists(target):
        print(f"Evaluating directory: {target}\n")
        s, r = evaluate(target)
        print_report(s, r)
    else:
        print(f"Directory does not exist: {target}")
    sys.exit(0)
