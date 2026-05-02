"""
CSRankings Data Extraction Script - Evaluation Rubric
Task: write/script/xuankunyang-query7

Hybrid evaluation strategy:
  Dynamic (100 pts) — run the agent's Playwright script, validate JSON output
    1) URL Logic        (40 pts): year/region/area params in final_url
    2) Data Accuracy    (40 pts): rank & count vs ground truth
    3) Code Robustness  (20 pts): script ran + valid JSON produced
  Static fallback (max 40 pts) — only if dynamic execution fails
    1) Playwright usage (10 pts)
    2) Selector usage   (10 pts)
    3) Business logic   (10 pts)
    4) Wait mechanism   (10 pts)
"""

import os
import re
import json
import subprocess
import sys
from typing import Tuple, Dict, Any, Optional, List


# ---------------------------------------------------------------------------
# Ground truth — default fallback when live fetch is unavailable
# These are the expected values for SJTU, AI area, 2020-2025, World.
# ---------------------------------------------------------------------------

DEFAULT_GROUND_TRUTH = {
    "institution": "Shanghai Jiao Tong University",
    "rank": 3,
    "count": 66.2,
    "faculty": 128,
}

# AI-related keywords expected in the URL hash
AI_URL_KEYWORDS = ["ai", "vision", "mlmining", "nlp", "inforet"]

# Non-AI keywords — their presence suggests the agent did not filter correctly
NON_AI_URL_KEYWORDS = ["systems", "theory"]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _load_env(answer_dir: str) -> dict:
    """Load .env variables from answer_dir and the query root directory."""
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
                        key = k.strip()
                        if key not in values:
                            values[key] = v.strip().strip("'\"")
            except Exception:
                pass
    return values


def _find_py_files(answer_dir: str) -> List[str]:
    """Return all .py files in answer_dir (non-recursive, sorted)."""
    if not os.path.isdir(answer_dir):
        return []
    return sorted(
        os.path.join(answer_dir, f)
        for f in os.listdir(answer_dir)
        if f.endswith(".py")
    )


def _read_file(path: str) -> str:
    """Safely read a text file."""
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except Exception:
        return ""


def _execute_script(script_path: str, timeout: int = 120) -> Tuple[str, str, int]:
    """Execute a Python script; return (stdout, stderr, returncode)."""
    env = os.environ.copy()
    if "PLAYWRIGHT_BROWSERS_PATH" not in env:
        for candidate in ["/opt/pw-browsers", "/ms-playwright"]:
            if os.path.isdir(candidate):
                env["PLAYWRIGHT_BROWSERS_PATH"] = candidate
                break

    try:
        proc = subprocess.Popen(
            [sys.executable, script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=os.path.dirname(script_path),
            env=env,
        )
        stdout_bytes, stderr_bytes = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.communicate()
        return "", "Execution timed out", -1
    except Exception as e:
        return "", str(e), -1

    def _decode(b: bytes) -> str:
        if not b:
            return ""
        try:
            return b.decode("utf-8")
        except Exception:
            return b.decode("utf-8", errors="replace")

    return _decode(stdout_bytes), _decode(stderr_bytes), proc.returncode


def _fetch_live_ground_truth() -> Optional[Dict]:
    """Try to get live ground truth by running Playwright ourselves."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return None

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://csrankings.org/", timeout=60000)
            page.select_option("#regions", "world")
            page.select_option("#fromyear", "2020")
            page.select_option("#toyear", "2025")
            page.click("#all_areas_off")
            page.click("#ai_areas_on")

            target = "Shanghai Jiao Tong University"
            row_sel = f'tr:has-text("{target}")'
            page.wait_for_selector(row_sel, timeout=30000)

            rank = page.locator(row_sel).locator("td:nth-child(1)").inner_text().strip()
            count = page.locator(row_sel).locator("td:nth-child(3)").inner_text().strip()
            faculty = page.locator(row_sel).locator("td:nth-child(4)").inner_text().strip()
            browser.close()

        return {
            "institution": target,
            "rank": int(rank) if rank.isdigit() else rank,
            "count": float(count),
            "faculty": int(faculty),
        }
    except Exception:
        return None


def _get_ground_truth() -> Dict:
    """Get ground truth — prefer live data, fall back to defaults."""
    live = _fetch_live_ground_truth()
    if live is not None:
        return live
    return dict(DEFAULT_GROUND_TRUTH)


def _extract_json(text: str) -> Optional[dict]:
    """Extract the first JSON object from text."""
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group())
    except json.JSONDecodeError:
        return None


# ---------------------------------------------------------------------------
# Dynamic scoring (max 100)
# ---------------------------------------------------------------------------


def _score_dynamic(stdout: str, gt: Dict) -> Tuple[int, Dict[str, Any]]:
    """Score the dynamic execution output against ground truth. Max 100."""
    score = 0
    details = {}
    deductions = []

    output = _extract_json(stdout)
    if output is None:
        raise ValueError("No valid JSON object found in stdout")

    final_url = output.get("final_url", "").lower()
    data = output.get("data", {})

    # ---- 1. URL Logic (40 pts) ----
    url_score = 0
    url_details = {}

    # 1a. Year params (10 pts)
    has_2020 = "2020" in final_url
    has_2025 = "2025" in final_url
    if has_2020 and has_2025:
        url_score += 10
        url_details["year_params"] = "10/10 — contains 2020 and 2025"
    elif has_2020 or has_2025:
        url_score += 5
        url_details["year_params"] = "5/10 — only one year param found"
        deductions.append("URL missing one of the year params (2020/2025)")
    else:
        url_details["year_params"] = "0/10 — missing year params"
        deductions.append("URL missing year params (2020 and 2025)")

    # 1b. Region (10 pts)
    if "world" in final_url:
        url_score += 10
        url_details["region"] = "10/10 — contains 'world'"
    else:
        url_details["region"] = "0/10 — missing 'world'"
        deductions.append("URL missing region param (world)")

    # 1c. Area purity (20 pts)
    ai_found = [k for k in AI_URL_KEYWORDS if k in final_url]
    non_ai_found = [k for k in NON_AI_URL_KEYWORDS if k in final_url]

    if len(ai_found) >= 3 and not non_ai_found:
        url_score += 20
        url_details["area_purity"] = f"20/20 — AI keywords present ({', '.join(ai_found)}), no non-AI keywords"
    elif ai_found and not non_ai_found:
        url_score += 15
        url_details["area_purity"] = f"15/20 — some AI keywords ({', '.join(ai_found)}), no non-AI keywords"
        deductions.append(f"URL only has {len(ai_found)}/5 AI area keywords")
    elif ai_found and non_ai_found:
        url_score += 8
        url_details["area_purity"] = f"8/20 — AI keywords present but non-AI keywords also found ({', '.join(non_ai_found)})"
        deductions.append(f"URL contains non-AI area keywords: {', '.join(non_ai_found)}")
    else:
        url_details["area_purity"] = "0/20 — no AI area keywords in URL"
        deductions.append("URL missing AI area keywords entirely")

    score += url_score
    details["1. URL Logic (40)"] = {"score": f"{url_score}/40", "breakdown": url_details}

    # ---- 2. Data Accuracy (40 pts) ----
    data_score = 0
    data_details = {}

    # 2a. Rank (20 pts)
    agent_rank = data.get("rank")
    gt_rank = gt["rank"]
    try:
        if int(agent_rank) == int(gt_rank):
            data_score += 20
            data_details["rank"] = f"20/20 — match ({agent_rank})"
        elif abs(int(agent_rank) - int(gt_rank)) <= 2:
            data_score += 10
            data_details["rank"] = f"10/20 — close (agent={agent_rank}, gt={gt_rank})"
            deductions.append(f"rank close but not exact: agent={agent_rank} vs gt={gt_rank}")
        else:
            data_details["rank"] = f"0/20 — mismatch (agent={agent_rank}, gt={gt_rank})"
            deductions.append(f"rank mismatch: agent={agent_rank} vs gt={gt_rank}")
    except (TypeError, ValueError):
        if str(agent_rank) == str(gt_rank):
            data_score += 20
            data_details["rank"] = f"20/20 — match ({agent_rank})"
        else:
            data_details["rank"] = f"0/20 — mismatch (agent={agent_rank}, gt={gt_rank})"
            deductions.append(f"rank mismatch: agent={agent_rank} vs gt={gt_rank}")

    # 2b. Count (20 pts) — allow small tolerance
    agent_count = data.get("count", 0)
    gt_count = gt["count"]
    try:
        diff = abs(float(agent_count) - float(gt_count))
        if diff < 0.5:
            data_score += 20
            data_details["count"] = f"20/20 — match (agent={agent_count}, gt={gt_count})"
        elif diff < 5.0:
            data_score += 10
            data_details["count"] = f"10/20 — close (agent={agent_count}, gt={gt_count}, diff={diff:.2f})"
            deductions.append(f"count close but off: agent={agent_count} vs gt={gt_count}")
        else:
            data_details["count"] = f"0/20 — mismatch (agent={agent_count}, gt={gt_count}, diff={diff:.2f})"
            deductions.append(f"count mismatch: agent={agent_count} vs gt={gt_count}")
    except (TypeError, ValueError):
        data_details["count"] = f"0/20 — cannot parse (agent={agent_count})"
        deductions.append(f"count cannot be parsed: {agent_count}")

    score += data_score
    details["2. Data Accuracy (40)"] = {"score": f"{data_score}/40", "breakdown": data_details}

    # ---- 3. Code Robustness (20 pts) ----
    # If we reached here, the code ran and produced valid JSON
    robustness_score = 0
    robustness_details = {}

    # 3a. Script ran without error (10 pts)
    robustness_score += 10
    robustness_details["execution"] = "10/10 — script executed successfully"

    # 3b. Output is valid JSON with correct schema (10 pts)
    has_final_url = "final_url" in output
    has_data = "data" in output and isinstance(output.get("data"), dict)
    has_institution = data.get("institution", "") != ""
    has_rank = "rank" in data
    has_count = "count" in data

    schema_checks = sum([has_final_url, has_data, has_institution, has_rank, has_count])
    if schema_checks == 5:
        robustness_score += 10
        robustness_details["schema"] = "10/10 — output has all required fields"
    elif schema_checks >= 3:
        robustness_score += 5
        robustness_details["schema"] = f"5/10 — output has {schema_checks}/5 required fields"
        deductions.append(f"Output JSON missing some required fields ({schema_checks}/5)")
    else:
        robustness_details["schema"] = f"0/10 — output schema is incomplete ({schema_checks}/5)"
        deductions.append("Output JSON schema is largely incomplete")

    score += robustness_score
    details["3. Code Robustness (20)"] = {"score": f"{robustness_score}/20", "breakdown": robustness_details}

    return score, {"score": score, "details": details, "deductions": deductions}


# ---------------------------------------------------------------------------
# Static fallback scoring (max 40, only when dynamic fails)
# ---------------------------------------------------------------------------


def _score_static(code: str) -> Tuple[int, Dict[str, Any]]:
    """Static code analysis fallback. Max 40 points."""
    score = 0
    details = {}
    deductions = []
    code_lower = code.lower()

    # 1. Playwright usage (10 pts)
    has_import = "playwright" in code_lower
    has_launch = "launch" in code_lower and ("chromium" in code_lower or "browser" in code_lower)
    if has_import and has_launch:
        score += 10
        details["playwright_usage"] = "10/10 — playwright import + browser launch detected"
    elif has_import:
        score += 7
        details["playwright_usage"] = "7/10 — playwright imported but no clear browser launch"
    else:
        details["playwright_usage"] = "0/10 — playwright not detected"
        deductions.append("Code does not use Playwright")

    # 2. Selector reasoning (10 pts) — key DOM selectors from dom_snippets.html
    sel_score = 0
    found_selectors = []
    key_selectors = {
        "#fromyear": 2,
        "#toyear": 2,
        "#regions": 2,
        "#all_areas_off": 2,
        "ai": 2,  # ai_areas_on, ai_header, or similar AI-related selector
    }
    for sel, pts in key_selectors.items():
        if sel in code:
            sel_score += pts
            found_selectors.append(sel)

    sel_score = min(10, sel_score)
    if found_selectors:
        details["selector_reasoning"] = f"{sel_score}/10 — found: {', '.join(found_selectors)}"
    else:
        details["selector_reasoning"] = "0/10 — no key selectors found"
        deductions.append("Code missing key DOM selectors")
    score += sel_score

    # 3. Business logic (10 pts)
    biz_score = 0
    if "world" in code_lower:
        biz_score += 5
    if "shanghai jiao tong" in code_lower or "sjtu" in code_lower:
        biz_score += 5
    biz_score = min(10, biz_score)
    if biz_score >= 10:
        details["business_logic"] = "10/10 — contains 'world' and target institution"
    elif biz_score > 0:
        details["business_logic"] = f"{biz_score}/10 — partially present"
    else:
        details["business_logic"] = "0/10 — missing key business logic keywords"
        deductions.append("Code missing business logic keywords")
    score += biz_score

    # 4. Wait mechanism (10 pts)
    wait_score = 0
    if "wait_for_selector" in code_lower:
        wait_score = 10
    elif "wait_for_function" in code_lower:
        wait_score = 10
    elif "wait_for" in code_lower:
        wait_score = 7
    elif "sleep" in code_lower or "timeout" in code_lower:
        wait_score = 3

    if wait_score > 0:
        details["wait_mechanism"] = f"{wait_score}/10 — wait logic detected"
    else:
        details["wait_mechanism"] = "0/10 — no wait mechanism found"
        deductions.append("Code lacks explicit wait mechanism")
    score += wait_score

    return score, {"score": score, "details": details, "deductions": deductions}


# ---------------------------------------------------------------------------
# Main evaluation
# ---------------------------------------------------------------------------


def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Evaluate agent output for the CSRankings data extraction task.

    Args:
        answer_dir: absolute path to the agent output directory

    Returns:
        (score, report) — score is 0-100, report is a dict with details
    """
    answer_dir = os.path.abspath(answer_dir)
    py_files = _find_py_files(answer_dir)

    if not py_files:
        return 0, {
            "total": 0,
            "mode": "no_files",
            "result_score": {
                "score": 0,
                "details": {},
                "deductions": ["No .py files found in answer directory"],
            },
            "process_score": {"score": 0, "details": {}, "deductions": []},
            "comment": "No Python script was submitted.",
        }

    # Collect all code for potential static analysis
    all_code = ""
    for pf in py_files:
        all_code += _read_file(pf) + "\n"

    # Try dynamic execution with the first .py file
    script_path = py_files[0]
    stdout, stderr, rc = _execute_script(script_path, timeout=120)

    dynamic_ok = False
    dynamic_score = 0
    dynamic_report = {}

    if rc == 0 and stdout.strip():
        try:
            gt = _get_ground_truth()
            dynamic_score, dynamic_report = _score_dynamic(stdout, gt)
            dynamic_ok = True
        except Exception as e:
            dynamic_report = {
                "score": 0,
                "details": {"error": f"Dynamic scoring failed: {str(e)[:300]}"},
                "deductions": [f"Dynamic scoring error: {str(e)[:150]}"],
            }

    if dynamic_ok:
        total = dynamic_score
        report = {
            "total": total,
            "mode": "dynamic",
            "result_score": dynamic_report,
            "process_score": {"score": 0, "details": {}, "deductions": []},
            "comment": "",
        }
    else:
        static_score, static_report = _score_static(all_code)
        total = static_score
        exec_info = {}
        if stderr:
            exec_info["stderr"] = stderr[:500]
        if rc is not None:
            exec_info["returncode"] = rc
        report = {
            "total": total,
            "mode": "static_fallback",
            "execution_info": exec_info,
            "result_score": static_report,
            "process_score": {"score": 0, "details": {}, "deductions": []},
            "comment": "",
        }

    # Generate comment
    if total >= 90:
        report["comment"] = "Excellent. Script runs correctly, data extraction is accurate, URL logic is complete."
    elif total >= 70:
        report["comment"] = "Good. Core data extraction works but some metrics are slightly off."
    elif total >= 50:
        report["comment"] = "Partial. Some functionality works but key data or URL logic has issues."
    elif total >= 20:
        report["comment"] = "Minimal. Code shows basic web automation structure but execution fails or data is incorrect."
    else:
        report["comment"] = "Insufficient. Script not submitted or entirely non-functional."

    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print a formatted evaluation report."""
    print("=" * 70)
    print("CSRankings Data Extraction Script — Evaluation Report")
    print("Task: write/script/xuankunyang-query7")
    print("=" * 70)
    print(f"\nTotal Score: {score}/100")
    print(f"Evaluation Mode: {report.get('mode', 'N/A')}\n")

    # Execution info (static fallback only)
    exec_info = report.get("execution_info")
    if exec_info:
        print("-" * 50)
        print("[Execution Info]")
        print("-" * 50)
        if "returncode" in exec_info:
            print(f"  Return code: {exec_info['returncode']}")
        if "stderr" in exec_info:
            print(f"  Stderr (truncated): {exec_info['stderr'][:400]}")
        print()

    # Result score
    result_report = report.get("result_score", {})
    mode = report.get("mode", "")
    print("-" * 50)
    if mode == "dynamic":
        print("[Dynamic Execution Scoring (max 100)]")
    else:
        print("[Static Analysis Fallback Scoring (max 40)]")
    print("-" * 50)
    print(f"  Score: {result_report.get('score', 0)}")

    details = result_report.get("details", {})
    if isinstance(details, dict):
        for section, content in details.items():
            if section in ("score", "deductions"):
                continue
            print(f"\n  [{section}]")
            if isinstance(content, dict):
                for k, v in content.items():
                    print(f"    {k}: {v}")
            else:
                print(f"    {content}")

    # Deductions summary
    all_deductions = []
    all_deductions.extend(result_report.get("deductions", []))
    all_deductions.extend(report.get("process_score", {}).get("deductions", []))

    if all_deductions:
        print("\n" + "-" * 50)
        print("Deductions:")
        print("-" * 50)
        for i, reason in enumerate(all_deductions, 1):
            print(f"  {i}. {reason}")

    print("\n" + "=" * 50)
    print(f"Comment: {report.get('comment', '')}")
    print("=" * 70)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_dir = os.path.abspath(sys.argv[1])
    else:
        test_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "gpt-5", "attempt_1"
        )

    if os.path.exists(test_dir):
        print(f"Evaluating directory: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"Directory does not exist: {test_dir}")
    sys.exit(0)
