"""
Scoring Rubric — German Vocabulary App Frontend-Backend Integration Debug
task_id: en_fullstack_debug

Total: 100 points

Scoring dimensions:
1. File Delivery Check (10 pts)
  1. backend/ directory and key backend files exist (5 pts)
  2. frontend/ directory and key frontend files exist (5 pts)

2. Backend Static Analysis (15 pts)
  1. main.py syntax correct and importable (5 pts)
  2. CORS cross-origin configuration correct (5 pts)
  3. models.py / data.py syntax correct (5 pts)

3. E2E Functional Tests (75 pts) — Playwright driven
  1. Home page accessible and shows title (10 pts)
  2. Can navigate to verb list page (10 pts)
  3. Verb list loads correctly (15 pts)
  4. Verb conjugation table expands and renders (15 pts)
  5. Add verb functionality works (15 pts)
  6. No frontend runtime errors (10 pts)
"""

import ast
import json
import os
import re
import signal
import socket
import subprocess
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# ────────────────────────────────────────────────────────────
# Utility functions
# ────────────────────────────────────────────────────────────

def _find_free_port(start: int = 8000) -> int:
    """Find an available port."""
    for port in range(start, start + 200):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("", port))
                return port
        except OSError:
            continue
    raise RuntimeError(f"Cannot find an available port ({start}-{start + 199})")


def _kill_process_tree(proc: Optional[subprocess.Popen], label: str) -> None:
    """Terminate a process and all its children."""
    if proc is None:
        return
    try:
        pgid = os.getpgid(proc.pid)
        os.killpg(pgid, signal.SIGTERM)
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            os.killpg(pgid, signal.SIGKILL)
            proc.wait(timeout=3)
        print(f"  [{label}] stopped")
    except ProcessLookupError:
        pass
    except Exception as exc:
        print(f"  [{label}] stop error: {exc}")


def _wait_for_port(port: int, timeout: float = 15.0) -> bool:
    """Wait for a TCP port to become connectable."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=1):
                return True
        except OSError:
            time.sleep(0.5)
    return False


# ────────────────────────────────────────────────────────────
# 1. File Delivery Check (10 pts)
# ────────────────────────────────────────────────────────────

def _check_file_delivery(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Check whether backend/ and frontend/ directories and key files exist.
    backend (5 pts): main.py, models.py, data.py all present 5 pts, 1-2 present 3 pts,
                     directory exists but no files 1 pt, directory missing 0 pts.
    frontend (5 pts): src/ and package.json both present 5 pts, partial 3 pts,
                      directory exists but no key files 1 pt, directory missing 0 pts.
    """
    score = 0
    details: Dict[str, str] = {}

    backend_dir = os.path.join(answer_dir, "backend")
    frontend_dir = os.path.join(answer_dir, "frontend")

    # -- backend (5 pts) --
    if os.path.isdir(backend_dir):
        required = ["main.py", "models.py", "data.py"]
        found = [f for f in required if os.path.isfile(os.path.join(backend_dir, f))]
        if len(found) == 3:
            score += 5
            details["backend"] = "5/5 — main.py, models.py, data.py all present"
        elif found:
            score += 3
            missing = sorted(set(required) - set(found))
            details["backend"] = f"3/5 — missing: {', '.join(missing)}"
        else:
            score += 1
            details["backend"] = "1/5 — backend/ exists but no key files"
    else:
        details["backend"] = "0/5 — backend/ directory does not exist"

    # -- frontend (5 pts) --
    if os.path.isdir(frontend_dir):
        has_src = os.path.isdir(os.path.join(frontend_dir, "src"))
        has_pkg = os.path.isfile(os.path.join(frontend_dir, "package.json"))
        if has_src and has_pkg:
            score += 5
            details["frontend"] = "5/5 — src/ and package.json both present"
        elif has_src or has_pkg:
            score += 3
            details["frontend"] = "3/5 — some key files missing"
        else:
            score += 1
            details["frontend"] = "1/5 — frontend/ exists but missing src/ and package.json"
    else:
        details["frontend"] = "0/5 — frontend/ directory does not exist"

    return score, {"score": score, "max": 10, "details": details}


# ────────────────────────────────────────────────────────────
# 2. Backend Static Analysis (15 pts)
# ────────────────────────────────────────────────────────────

def _check_backend_static(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Static analysis of backend code:
    - main.py syntax correct (5 pts)
    - CORS configuration (5 pts): both CORSMiddleware import and add_middleware call get 5 pts
    - models.py / data.py syntax (5 pts): 2.5 pts per file
    """
    score = 0
    details: Dict[str, str] = {}
    backend_dir = os.path.join(answer_dir, "backend")

    if not os.path.isdir(backend_dir):
        return 0, {"score": 0, "max": 15, "details": {"error": "backend/ directory does not exist"}}

    # -- 2a. main.py syntax (5 pts) --
    main_path = os.path.join(backend_dir, "main.py")
    main_code = ""
    if os.path.isfile(main_path):
        try:
            with open(main_path, "r", encoding="utf-8") as f:
                main_code = f.read()
            ast.parse(main_code)
            score += 5
            details["main.py syntax"] = "5/5 — syntax correct"
        except SyntaxError as e:
            details["main.py syntax"] = f"0/5 — syntax error: {e}"
    else:
        details["main.py syntax"] = "0/5 — main.py does not exist"

    # -- 2b. CORS configuration (5 pts) --
    if main_code:
        has_cors_import = "CORSMiddleware" in main_code
        has_cors_add = "add_middleware" in main_code
        if has_cors_import and has_cors_add:
            score += 5
            details["CORS config"] = "5/5 — CORSMiddleware imported and add_middleware called"
        elif has_cors_import or has_cors_add:
            score += 2
            details["CORS config"] = "2/5 — partial CORS configuration (import or call missing)"
        else:
            details["CORS config"] = "0/5 — no CORS configuration (frontend cross-origin requests will fail)"
    else:
        details["CORS config"] = "0/5 — main.py not readable"

    # -- 2c. models.py / data.py syntax (5 pts) --
    sub_score = 0
    notes = []
    for fname in ("models.py", "data.py"):
        fpath = os.path.join(backend_dir, fname)
        if os.path.isfile(fpath):
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    ast.parse(f.read())
                sub_score += 2.5
            except SyntaxError as e:
                notes.append(f"{fname} syntax error: {e}")
        else:
            notes.append(f"{fname} does not exist")
    sub_score = int(sub_score)
    score += sub_score
    if sub_score == 5:
        details["models/data syntax"] = "5/5 — both files have correct syntax"
    else:
        details["models/data syntax"] = f"{sub_score}/5 — {'; '.join(notes)}"

    return score, {"score": score, "max": 15, "details": details}


# ────────────────────────────────────────────────────────────
# 3. E2E Functional Tests (75 pts)
# ────────────────────────────────────────────────────────────

def _install_backend_deps(backend_dir: str) -> bool:
    """Install FastAPI and other backend dependencies."""
    try:
        subprocess.run(
            ["pip3", "install", "-q", "fastapi", "uvicorn[standard]", "pydantic"],
            cwd=backend_dir,
            capture_output=True, text=True, timeout=120,
        )
        return True
    except Exception as e:
        print(f"  [BACKEND] Failed to install dependencies: {e}")
        return False


def _start_backend(answer_dir: str, port: int) -> Optional[subprocess.Popen]:
    """Start the FastAPI backend, return process handle."""
    backend_dir = os.path.join(answer_dir, "backend")
    main_py = os.path.join(backend_dir, "main.py")
    if not os.path.isfile(main_py):
        print("  [BACKEND] main.py does not exist, skipping startup")
        return None

    _install_backend_deps(backend_dir)

    cmd = [
        "python3", "-m", "uvicorn", "main:app",
        "--host", "0.0.0.0", "--port", str(port),
    ]
    print(f"  [BACKEND] Starting: {' '.join(cmd)}")
    proc = subprocess.Popen(
        cmd, cwd=backend_dir,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        preexec_fn=os.setsid,
    )

    if not _wait_for_port(port, timeout=15):
        if proc.poll() is not None:
            out, err = proc.communicate()
            print(f"  [BACKEND] Startup failed:\n    stdout={out[:400]}\n    stderr={err[:400]}")
        else:
            print(f"  [BACKEND] Timeout: port {port} not ready")
            _kill_process_tree(proc, "BACKEND")
        return None

    print(f"  [BACKEND] PID={proc.pid}  port={port}")
    return proc


def _patch_frontend_api_url(frontend_dir: str, backend_port: int) -> None:
    """
    If the frontend API calls have hardcoded localhost:8000, replace with the actual backend port.
    This ensures E2E tests can connect even if the agent didn't modify the port number.
    """
    api_dir = os.path.join(frontend_dir, "src", "api")
    if not os.path.isdir(api_dir):
        return
    for fname in os.listdir(api_dir):
        fpath = os.path.join(api_dir, fname)
        if not os.path.isfile(fpath):
            continue
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
            # Replace common hardcoded backend addresses
            patched = content
            patched = patched.replace("localhost:8000", f"localhost:{backend_port}")
            patched = patched.replace("127.0.0.1:8000", f"127.0.0.1:{backend_port}")
            if patched != content:
                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(patched)
                print(f"  [PATCH] Updated backend address in {fname} to port {backend_port}")
        except Exception:
            pass


def _start_frontend(answer_dir: str, port: int) -> Optional[subprocess.Popen]:
    """Install dependencies and start the Vite frontend dev server."""
    frontend_dir = os.path.join(answer_dir, "frontend")
    pkg_json_path = os.path.join(frontend_dir, "package.json")
    if not os.path.isfile(pkg_json_path):
        print("  [FRONTEND] package.json does not exist, skipping startup")
        return None

    import shutil

    # Clean existing node_modules to avoid version conflicts
    nm = os.path.join(frontend_dir, "node_modules")
    if os.path.exists(nm):
        shutil.rmtree(nm, ignore_errors=True)
    lock = os.path.join(frontend_dir, "package-lock.json")
    if os.path.isfile(lock):
        try:
            os.remove(lock)
        except OSError:
            pass

    # Remove potentially interfering preinstall scripts
    try:
        with open(pkg_json_path, "r", encoding="utf-8") as fh:
            pkg = json.load(fh)
        if pkg.get("scripts", {}).get("preinstall"):
            del pkg["scripts"]["preinstall"]
            with open(pkg_json_path, "w", encoding="utf-8") as fh:
                json.dump(pkg, fh, indent=2, ensure_ascii=False)
    except Exception:
        pass

    env = os.environ.copy()
    env["npm_config_cache"] = "/tmp/npm-cache"

    print("  [FRONTEND] npm install ...")
    res = subprocess.run(
        ["npm", "install"], cwd=frontend_dir, env=env,
        capture_output=True, text=True, timeout=300,
    )
    if res.returncode != 0:
        print(f"  [FRONTEND] npm install failed:\n    {res.stderr[:500]}")
        return None

    # Fix .bin permissions
    bin_dir = os.path.join(frontend_dir, "node_modules", ".bin")
    if os.path.isdir(bin_dir):
        import stat
        for fn in os.listdir(bin_dir):
            fp = os.path.join(bin_dir, fn)
            if os.path.isfile(fp):
                os.chmod(
                    fp,
                    os.stat(fp).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH,
                )

    cmd = ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", str(port)]
    print(f"  [FRONTEND] Starting: {' '.join(cmd)}")
    proc = subprocess.Popen(
        cmd, cwd=frontend_dir,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        preexec_fn=os.setsid,
    )

    if not _wait_for_port(port, timeout=30):
        if proc.poll() is not None:
            out, err = proc.communicate()
            print(f"  [FRONTEND] Startup failed:\n    stdout={out[:400]}\n    stderr={err[:400]}")
        else:
            print(f"  [FRONTEND] Timeout: port {port} not ready")
            _kill_process_tree(proc, "FRONTEND")
        return None

    print(f"  [FRONTEND] PID={proc.pid}  port={port}")
    return proc


def _run_e2e_tests(e2e_dir: str, base_url: str) -> Tuple[bool, str]:
    """Run Playwright E2E tests and return (all passed, output)."""
    if not os.path.isdir(e2e_dir):
        return False, f"E2E test directory does not exist: {e2e_dir}"

    env = os.environ.copy()
    env["npm_config_cache"] = "/tmp/npm-cache"

    # npm install
    print("  [E2E] npm install ...")
    inst = subprocess.run(
        ["npm", "install"], cwd=e2e_dir, env=env,
        capture_output=True, text=True, timeout=300,
    )
    if inst.returncode != 0:
        return False, f"npm install failed:\n{inst.stderr[:500]}"

    # Fix .bin permissions
    bin_dir = os.path.join(e2e_dir, "node_modules", ".bin")
    if os.path.isdir(bin_dir):
        import stat
        for fn in os.listdir(bin_dir):
            fp = os.path.join(bin_dir, fn)
            if os.path.isfile(fp):
                os.chmod(
                    fp,
                    os.stat(fp).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH,
                )

    # Playwright browsers
    pw_browsers = os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers")
    if os.path.isdir(pw_browsers):
        env["PLAYWRIGHT_BROWSERS_PATH"] = pw_browsers
    else:
        print("  [E2E] Installing Chromium browser ...")
        subprocess.run(
            ["npx", "playwright", "install", "chromium", "--with-deps"],
            cwd=e2e_dir, env=env,
            capture_output=True, text=True, timeout=600,
        )

    env["BASE_URL"] = base_url

    cmd = ["npx", "playwright", "test", "--reporter=list"]
    print(f"  [E2E] Running: {' '.join(cmd)}  BASE_URL={base_url}")
    result = subprocess.run(
        cmd, cwd=e2e_dir, env=env,
        capture_output=True, text=True, timeout=120,
    )
    combined_output = result.stdout + "\n" + result.stderr
    return result.returncode == 0, combined_output


def _parse_e2e_results(output: str) -> Dict[str, bool]:
    """
    Parse scoring marker lines from E2E test output.
    E2E test scripts output: \u2705 <name> (<score> pts) or \u274c <name> (<score> pts)
    """
    checks = {
        "\u9996\u9875\u53ef\u8bbf\u95ee": False,
        "\u8fdb\u5165\u52a8\u8bcd\u5217\u8868\u9875": False,
        "\u52a8\u8bcd\u5217\u8868\u52a0\u8f7d": False,
        "\u52a8\u8bcd\u53d8\u4f4d\u8868\u5c55\u5f00\u4e0e\u6e32\u67d3": False,
        "\u65b0\u589e\u52a8\u8bcd\u529f\u80fd": False,
        "\u65e0\u524d\u7aef\u8fd0\u884c\u65f6\u9519\u8bef": False,
    }
    for line in output.splitlines():
        for name in checks:
            if name in line and "\u2705" in line:  # checkmark
                checks[name] = True
    return checks


# Rubric score allocation for each E2E checkpoint (total 75 pts)
_E2E_SCORE_MAP = {
    "\u9996\u9875\u53ef\u8bbf\u95ee":          10,
    "\u8fdb\u5165\u52a8\u8bcd\u5217\u8868\u9875":      10,
    "\u52a8\u8bcd\u5217\u8868\u52a0\u8f7d":        15,
    "\u52a8\u8bcd\u53d8\u4f4d\u8868\u5c55\u5f00\u4e0e\u6e32\u67d3": 15,
    "\u65b0\u589e\u52a8\u8bcd\u529f\u80fd":        15,
    "\u65e0\u524d\u7aef\u8fd0\u884c\u65f6\u9519\u8bef":    10,
}


def _run_e2e_scoring(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Start frontend and backend services -> run E2E Playwright tests -> calculate scores.
    Total: 75 pts.
    """
    backend_proc: Optional[subprocess.Popen] = None
    frontend_proc: Optional[subprocess.Popen] = None

    try:
        backend_port = _find_free_port(8000)
        frontend_port = _find_free_port(5173)

        # -- Start backend --
        backend_proc = _start_backend(answer_dir, backend_port)
        if backend_proc is None:
            return 0, {
                "score": 0, "max": 75,
                "details": {"error": "Backend service failed to start, E2E tests skipped"},
            }

        # -- Patch frontend backend address (adapt to dynamic port) --
        if backend_port != 8000:
            _patch_frontend_api_url(
                os.path.join(answer_dir, "frontend"),
                backend_port,
            )

        # -- Start frontend --
        frontend_proc = _start_frontend(answer_dir, frontend_port)
        if frontend_proc is None:
            return 0, {
                "score": 0, "max": 75,
                "details": {"error": "Frontend service failed to start, E2E tests skipped"},
            }

        # -- Run E2E tests --
        e2e_dir = str(Path(__file__).resolve().parent / "e2e")
        base_url = f"http://localhost:{frontend_port}"
        all_passed, output = _run_e2e_tests(e2e_dir, base_url)

        # Print test output for debugging
        sep = "\u2500" * 60
        print(f"\n  [E2E] Test output:\n{sep}")
        for line in output.splitlines():
            print(f"    {line}")
        print(sep)

        # -- Parse and score --
        results = _parse_e2e_results(output)
        score = 0
        details: Dict[str, str] = {}
        failed_items: List[str] = []

        for name, passed in results.items():
            pts = _E2E_SCORE_MAP[name]
            if passed:
                score += pts
                details[name] = f"\u2705 {pts}/{pts}"
            else:
                details[name] = f"\u274c 0/{pts}"
                failed_items.append(name)

        return score, {
            "score": score,
            "max": 75,
            "details": details,
            "failed_items": failed_items,
            "Playwright all passed": all_passed,
        }

    except Exception as exc:
        import traceback
        return 0, {
            "score": 0, "max": 75,
            "details": {
                "exception": str(exc),
                "traceback": traceback.format_exc(),
            },
        }
    finally:
        _kill_process_tree(frontend_proc, "FRONTEND")
        _kill_process_tree(backend_proc, "BACKEND")


# ────────────────────────────────────────────────────────────
# Main entry
# ────────────────────────────────────────────────────────────

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Evaluate the agent's output.

    Args:
        answer_dir: absolute path to the agent output directory
                    (e.g., /path/to/query/gpt-5/attempt_1)

    Returns:
        (score, report)
        - score: integer 0-100
        - report: dict with detailed evaluation report
    """
    answer_dir = os.path.abspath(answer_dir)
    print(f"\n{'=' * 70}")
    print("Evaluation task: German Vocabulary App Frontend-Backend Integration Debug")
    print(f"Answer directory: {answer_dir}")
    print(f"{'=' * 70}\n")

    # 1. File delivery (10 pts)
    s1, r1 = _check_file_delivery(answer_dir)
    print(f"[1] File delivery: {s1}/10")

    # 2. Backend static analysis (15 pts)
    s2, r2 = _check_backend_static(answer_dir)
    print(f"[2] Backend static analysis: {s2}/15")

    # 3. E2E functional tests (75 pts)
    s3, r3 = _run_e2e_scoring(answer_dir)
    print(f"[3] E2E functional tests: {s3}/75")

    total = s1 + s2 + s3
    total = max(0, min(100, total))

    if total >= 90:
        comment = "Excellent! Frontend-backend integration successful, all core features work correctly."
    elif total >= 75:
        comment = "Good. Most features work, with minor issues."
    elif total >= 60:
        comment = "Passing. Basic features work, but some key features failed E2E tests."
    elif total >= 40:
        comment = "Partially complete. Multiple features do not work correctly."
    else:
        comment = "Failing. Frontend-backend integration has serious issues, core features are non-functional."

    report = {
        "total_score": total,
        "section_scores": {
            "1. File Delivery (10)": s1,
            "2. Backend Static Analysis (15)": s2,
            "3. E2E Functional Tests (75)": s3,
        },
        "details": {
            "File Delivery": r1,
            "Backend Static Analysis": r2,
            "E2E Functional Tests": r3,
        },
        "verdict": comment,
    }

    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print a formatted scoring report."""
    print(f"\n{'=' * 70}")
    print("German Vocabulary App Frontend-Backend Integration Debug — Scoring Report")
    print(f"{'=' * 70}")
    print(f"\nTotal Score: {score}/100\n")

    # Section scores overview
    print("-" * 50)
    print("[Section Scores]")
    print("-" * 50)
    for k, v in report.get("section_scores", {}).items():
        print(f"  {k}: {v}")

    # Dimension details
    for section_name, section_data in report.get("details", {}).items():
        print(f"\n{'-' * 50}")
        print(f"[{section_name}]")
        print("-" * 50)
        if isinstance(section_data, dict):
            for k, v in section_data.items():
                if isinstance(v, dict):
                    print(f"  {k}:")
                    for kk, vv in v.items():
                        print(f"    {kk}: {vv}")
                elif isinstance(v, list):
                    items_str = ", ".join(str(x) for x in v) if v else "None"
                    print(f"  {k}: {items_str}")
                else:
                    print(f"  {k}: {v}")

    print(f"\n{'=' * 50}")
    print(f"Verdict: {report.get('verdict', '')}")
    print(f"{'=' * 70}\n")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = str(Path(__file__).resolve().parent.parent / "workspace")

    if os.path.exists(target):
        print(f"Evaluating directory: {target}\n")
        s, r = evaluate(target)
        print_report(s, r)
        sys.exit(0)
    else:
        print(f"Directory does not exist: {target}")
        sys.exit(0)
