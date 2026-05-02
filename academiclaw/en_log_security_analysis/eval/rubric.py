"""
Security Log Analysis Task — eval/rubric.py
Task: Analyze Apache web server logs to identify security threats.

Deliverables:
  - analyze_logs.py  (Python script that parses log files)
  - security_report.txt  (security report with threat analysis)

Total: 100 points

Scoring dimensions:
  1. File Delivery          (10 pts)
  2. Script Quality         (25 pts)
  3. Report Structure       (25 pts)
  4. Threat Detection       (40 pts)

Known threats embedded in the log data (via generate_logs.py seed=42):
  IP 10.0.0.50 — Admin/sensitive endpoint probing (/admin/config.php, /wp-admin/)
  IP 10.0.0.51 — SQL injection (OR '1'='1, UNION SELECT ... FROM users--)
  IP 10.0.0.52 — Directory traversal (../../../../etc/passwd, URL-encoded)
  IP 10.0.0.53 — Attack-tool user agents (sqlmap/1.0, nmap NSE script)
"""

import os
import re
import sys
import json
from typing import Tuple, Dict, Any, List

try:
    import openai
except ImportError:
    openai = None


# ============================================================================
# Environment / LLM helpers
# ============================================================================

def _load_env(answer_dir: str) -> dict:
    """Load .env values from answer_dir and query root."""
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

    def g(key, default=""):
        return os.environ.get(key) or env.get(key) or default

    return {
        "api_key": g("EVAL_TEXT_API_KEY", g("ANTHROPIC_API_KEY")),
        "api_base": g("EVAL_TEXT_API_BASE_URL", g("ANTHROPIC_BASE_URL")),
        "model": g("EVAL_TEXT_MODEL", "openai/gpt-5.2"),
    }


def _call_llm_judge(prompt: str, config: dict) -> str:
    """Call LLM for text evaluation. Returns empty string on failure."""
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


def _parse_llm_json(raw: str) -> dict:
    """Extract JSON from LLM output (handles markdown fences)."""
    text = raw
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0].strip()
    elif "```" in text:
        text = text.split("```")[1].split("```")[0].strip()
    return json.loads(text)


# ============================================================================
# Helper: read file safely
# ============================================================================

def _read_file(path: str) -> str:
    """Read a text file, returning empty string on any error."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except Exception:
        return ""


# ============================================================================
# 1. File Delivery  (10 pts)
#    - analyze_logs.py present & non-empty  (5 pts)
#    - security_report.txt present & non-empty  (5 pts)
# ============================================================================

def _check_file_delivery(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    score = 0
    details: Dict[str, str] = {}
    deductions: List[str] = []

    script_path = os.path.join(answer_dir, "analyze_logs.py")
    report_path = os.path.join(answer_dir, "security_report.txt")

    # analyze_logs.py (5 pts)
    if os.path.isfile(script_path):
        size = os.path.getsize(script_path)
        if size > 0:
            score += 5
            details["analyze_logs.py"] = f"5/5 — present ({size} bytes)"
        else:
            score += 1
            details["analyze_logs.py"] = "1/5 — file exists but empty"
            deductions.append("analyze_logs.py is empty")
    else:
        details["analyze_logs.py"] = "0/5 — missing"
        deductions.append("analyze_logs.py not found")

    # security_report.txt (5 pts)
    if os.path.isfile(report_path):
        size = os.path.getsize(report_path)
        if size > 0:
            score += 5
            details["security_report.txt"] = f"5/5 — present ({size} bytes)"
        else:
            score += 1
            details["security_report.txt"] = "1/5 — file exists but empty"
            deductions.append("security_report.txt is empty")
    else:
        details["security_report.txt"] = "0/5 — missing"
        deductions.append("security_report.txt not found")

    return score, {"score": score, "max": 10, "details": details, "deductions": deductions}


# ============================================================================
# 2. Script Quality  (25 pts)
#    Checks analyze_logs.py for correctness and completeness.
#    2a. Valid Python syntax  (3 pts)
#    2b. Log file reading logic  (4 pts)
#    2c. Log parsing (regex / split)  (4 pts)
#    2d. SQL injection detection patterns  (4 pts)
#    2e. Directory traversal detection  (3 pts)
#    2f. Report generation logic  (4 pts)
#    2g. Implementation size  (3 pts)
# ============================================================================

def _check_script_quality(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    score = 0
    details: Dict[str, str] = {}
    deductions: List[str] = []

    script_path = os.path.join(answer_dir, "analyze_logs.py")
    if not os.path.isfile(script_path):
        return 0, {"score": 0, "max": 25, "details": {"error": "script missing"},
                    "deductions": ["No script to evaluate"]}

    code = _read_file(script_path)
    if not code:
        return 0, {"score": 0, "max": 25, "details": {"error": "script unreadable"},
                    "deductions": ["Cannot read script"]}

    code_lower = code.lower()

    # 2a. Syntax validity (3 pts)
    try:
        compile(code, script_path, "exec")
        score += 3
        details["syntax"] = "3/3 — valid Python"
    except SyntaxError as e:
        details["syntax"] = f"0/3 — SyntaxError: {e}"
        deductions.append("Script has syntax errors")

    # 2b. Log file reading logic (4 pts)
    has_log_ref = bool(re.search(r"(logs/|log.*dir|access_log|\.log)", code, re.IGNORECASE))
    has_open = "open(" in code or "read(" in code_lower or "readlines" in code_lower
    has_glob = "glob" in code_lower
    if (has_log_ref and has_open) or has_glob:
        score += 4
        details["log_reading"] = "4/4 — references log files and reads them"
    elif has_log_ref:
        score += 2
        details["log_reading"] = "2/4 — references log paths but unclear reading logic"
    else:
        details["log_reading"] = "0/4 — no log file reading detected"
        deductions.append("Script does not appear to read log files")

    # 2c. Log parsing with regex/split (4 pts)
    has_regex = "re." in code or "import re" in code
    has_parsing = bool(re.search(r"(split|match|search|findall|group|parse)", code_lower))
    if has_regex and has_parsing:
        score += 4
        details["log_parsing"] = "4/4 — uses regex for parsing"
    elif has_parsing:
        score += 2
        details["log_parsing"] = "2/4 — uses string parsing without regex"
    elif has_regex:
        score += 1
        details["log_parsing"] = "1/4 — imports re but no clear parsing"
    else:
        details["log_parsing"] = "0/4 — no parsing logic detected"
        deductions.append("No log parsing logic found")

    # 2d. SQL injection detection patterns (4 pts)
    sqli_groups = [
        (r"(sql.*inject|union.*select)", "SQL injection keyword"),
        (r"(or\s*['\"]?1['\"]?\s*=\s*['\"]?1|or\s+1\s*=\s*1)", "OR 1=1 pattern"),
        (r"(select\s.*from|drop\s+table|information_schema)", "SQL keywords"),
    ]
    sqli_found = sum(1 for pat, _ in sqli_groups if re.search(pat, code, re.IGNORECASE))
    sqli_score = min(4, sqli_found * 2)
    score += sqli_score
    details["sqli_detection"] = f"{sqli_score}/4 — {sqli_found}/3 pattern groups"

    # 2e. Directory traversal detection (3 pts)
    trav_groups = [
        (r"(directory.*traversal|path.*traversal)", "traversal keyword"),
        (r"(\.\./|\.\.%2[fF]|%2e%2e)", "traversal path pattern"),
        (r"(etc/passwd|boot\.ini)", "sensitive file target"),
    ]
    trav_found = sum(1 for pat, _ in trav_groups if re.search(pat, code, re.IGNORECASE))
    trav_score = min(3, trav_found)
    score += trav_score
    details["traversal_detection"] = f"{trav_score}/3 — {trav_found}/3 pattern groups"

    # 2f. Report generation logic (4 pts)
    has_report_ref = "security_report" in code_lower or "report" in code_lower
    has_write = "'w'" in code or '"w"' in code or "write(" in code
    if has_report_ref and has_write:
        score += 4
        details["report_generation"] = "4/4 — references report and writes output"
    elif has_report_ref:
        score += 2
        details["report_generation"] = "2/4 — references report but no write logic"
    elif has_write:
        score += 1
        details["report_generation"] = "1/4 — has write logic but unclear report ref"
    else:
        details["report_generation"] = "0/4 — no report generation detected"
        deductions.append("No report generation logic found")

    # 2g. Implementation size (3 pts)
    non_comment_lines = [l for l in code.split("\n") if l.strip() and not l.strip().startswith("#")]
    loc = len(non_comment_lines)
    if loc >= 80:
        score += 3
        details["implementation_size"] = f"3/3 — {loc} non-comment lines"
    elif loc >= 40:
        score += 2
        details["implementation_size"] = f"2/3 — {loc} non-comment lines"
    elif loc >= 15:
        score += 1
        details["implementation_size"] = f"1/3 — {loc} non-comment lines (minimal)"
    else:
        details["implementation_size"] = f"0/3 — only {loc} lines (too short)"
        deductions.append("Script is too short for meaningful analysis")

    return score, {"score": score, "max": 25, "details": details, "deductions": deductions}


# ============================================================================
# 3. Report Structure  (25 pts)
#    Checks security_report.txt for required sections.
#    3a. Suspicious IPs section  (5 pts)
#    3b. Attack patterns section  (5 pts)
#    3c. Timeline of suspicious activities  (5 pts)
#    3d. Recommendations / mitigation  (5 pts)
#    3e. Report depth (length)  (5 pts)
# ============================================================================

def _check_report_structure(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    score = 0
    details: Dict[str, str] = {}
    deductions: List[str] = []

    report_path = os.path.join(answer_dir, "security_report.txt")
    if not os.path.isfile(report_path):
        return 0, {"score": 0, "max": 25, "details": {"error": "report missing"},
                    "deductions": ["No report to evaluate"]}

    content = _read_file(report_path)
    if not content:
        return 0, {"score": 0, "max": 25, "details": {"error": "report unreadable"},
                    "deductions": ["Cannot read report"]}

    content_lower = content.lower()

    # 3a. Suspicious IPs section (5 pts)
    has_ip_section = bool(re.search(
        r"(suspicious.*ip|top.*ip|ip.*address|malicious.*ip|threat.*ip)", content_lower))
    has_ip_with_count = bool(re.search(r"\d+\.\d+\.\d+\.\d+.*\d+", content))
    if has_ip_section and has_ip_with_count:
        ip_score = 5
    elif has_ip_section:
        ip_score = 3
    elif has_ip_with_count:
        ip_score = 2
    else:
        ip_score = 0
    score += ip_score
    details["suspicious_ips"] = f"{ip_score}/5"

    # 3b. Attack patterns section (5 pts)
    has_attack_header = bool(re.search(
        r"(attack.*pattern|detected.*attack|threat.*type|attack.*categor)", content_lower))
    has_sqli = bool(re.search(r"sql.*inject", content_lower))
    has_trav = bool(re.search(r"(directory.*traversal|path.*traversal|\.\.\/)", content_lower))
    if has_attack_header and has_sqli and has_trav:
        atk_score = 5
    elif has_sqli and has_trav:
        atk_score = 4
    elif has_sqli or has_trav:
        atk_score = 2
    elif has_attack_header:
        atk_score = 1
    else:
        atk_score = 0
    score += atk_score
    details["attack_patterns"] = (
        f"{atk_score}/5 — sqli={'yes' if has_sqli else 'no'}, "
        f"traversal={'yes' if has_trav else 'no'}"
    )

    # 3c. Timeline section (5 pts)
    has_timeline_header = bool(re.search(
        r"(timeline|time.*analysis|chronolog|temporal|activity.*over.*time)", content_lower))
    has_timestamps = bool(re.search(r"\d{1,2}/\w{3}/\d{4}|\d{4}-\d{2}-\d{2}", content))
    if has_timeline_header and has_timestamps:
        tl_score = 5
    elif has_timeline_header:
        tl_score = 3
    elif has_timestamps:
        tl_score = 2
    else:
        tl_score = 0
        deductions.append("Report lacks timeline of suspicious activities")
    score += tl_score
    details["timeline"] = f"{tl_score}/5"

    # 3d. Recommendations (5 pts)
    has_rec = bool(re.search(
        r"(recommend|suggestion|mitigation|countermeasure|block|firewall|"
        r"prevention|remediation|action.*item)", content_lower))
    rec_score = 5 if has_rec else 0
    score += rec_score
    details["recommendations"] = f"{rec_score}/5"
    if not has_rec:
        deductions.append("Report lacks recommendations/mitigation section")

    # 3e. Report depth (5 pts)
    char_count = len(content)
    line_count = len(content.strip().split("\n"))
    if char_count >= 2000 and line_count >= 30:
        depth_score = 5
    elif char_count >= 1000 and line_count >= 15:
        depth_score = 3
    elif char_count >= 300:
        depth_score = 1
    else:
        depth_score = 0
    score += depth_score
    details["report_depth"] = f"{depth_score}/5 — {char_count} chars, {line_count} lines"

    return score, {"score": score, "max": 25, "details": details, "deductions": deductions}


# ============================================================================
# 4. Threat Detection Accuracy  (40 pts)
#    4a. Known-IP detection in report  (20 pts — 5 per IP)
#    4b. Attack-type classification  (12 pts — 4 per type)
#    4c. LLM-as-Judge quality assessment  (8 pts)
# ============================================================================

EXPECTED_THREAT_IPS = {
    "10.0.0.50": "Admin/sensitive endpoint probing",
    "10.0.0.51": "SQL injection attempts",
    "10.0.0.52": "Directory traversal attempts",
    "10.0.0.53": "Scanner/attack tool user agents",
}

ATTACK_TYPE_PATTERNS = {
    "SQL injection": [
        r"sql.*inject", r"union.*select", r"or\s*['\"]?1['\"]?\s*=",
    ],
    "Directory traversal": [
        r"directory.*travers", r"path.*travers", r"\.\./", r"etc/passwd",
    ],
    "Scanner/tool detection": [
        r"sqlmap", r"nmap", r"scanner", r"suspicious.*user.?agent",
        r"attack.*tool", r"automated.*scan",
    ],
}


def _check_threat_detection(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    score = 0
    details: Dict[str, str] = {}
    deductions: List[str] = []

    report_path = os.path.join(answer_dir, "security_report.txt")
    report = _read_file(report_path)

    if not report:
        return 0, {"score": 0, "max": 40,
                    "details": {"error": "No report content to verify"},
                    "deductions": ["Cannot verify threat detection without report"]}

    # 4a. Known IP detection (20 pts — 5 pts per IP)
    ip_score = 0
    for ip, desc in EXPECTED_THREAT_IPS.items():
        if ip in report:
            ip_score += 5
            details[f"IP {ip}"] = f"5/5 — detected ({desc})"
        else:
            details[f"IP {ip}"] = f"0/5 — NOT detected ({desc})"
            deductions.append(f"Failed to detect {ip} ({desc})")
    score += ip_score

    # 4b. Attack type classification (12 pts — 4 pts per type)
    type_score = 0
    for attack_type, patterns in ATTACK_TYPE_PATTERNS.items():
        found = any(re.search(pat, report, re.IGNORECASE) for pat in patterns)
        if found:
            type_score += 4
            details[f"Type: {attack_type}"] = "4/4 — mentioned in report"
        else:
            details[f"Type: {attack_type}"] = "0/4 — NOT mentioned"
            deductions.append(f"Report does not mention {attack_type}")
    score += type_score

    # 4c. LLM-as-Judge quality assessment (8 pts)
    llm_score = _llm_report_quality(answer_dir, report)
    score += llm_score["score"]
    details["LLM_quality_assessment"] = llm_score["detail"]

    return score, {"score": score, "max": 40, "details": details, "deductions": deductions}


def _llm_report_quality(answer_dir: str, report: str) -> Dict[str, Any]:
    """Use LLM to assess overall report quality (0-8 pts)."""
    config = _get_text_eval_config(answer_dir)
    report_excerpt = report[:5000]

    prompt = f"""You are evaluating a security analysis report generated from web server access logs.

The logs contain the following known threats that should be detected:
1. IP 10.0.0.50: Admin access / sensitive endpoint probing (/admin/config.php, /wp-admin/) returning 403
2. IP 10.0.0.51: SQL injection attempts (OR '1'='1, UNION SELECT * FROM users--)
3. IP 10.0.0.52: Directory traversal (../../../../etc/passwd, URL-encoded variants (%2e%2e%2f)) returning 404
4. IP 10.0.0.53: Attack tool usage identified by user agent strings (sqlmap/1.0, nmap NSE script)

Normal traffic comes from 192.168.x.x IPs visiting /index.html, /about.html, /products.html, /contact.html, /login.

Here is the security report:
---
{report_excerpt}
---

Score this report on a scale of 0-8 based on:
- Accuracy: Are the four real threat IPs correctly identified and distinguished from normal traffic?
- Depth: Are attack patterns explained with examples, not just listed?
- Actionability: Are recommendations specific and useful?
- False positives: Does the report avoid flagging many normal 192.168.x.x IPs as malicious?

Return ONLY a JSON object:
{{"score": <integer 0-8>, "reason": "<one-sentence explanation>"}}"""

    raw = _call_llm_judge(prompt, config)
    if raw:
        try:
            result = _parse_llm_json(raw)
            s = max(0, min(8, int(result.get("score", 0))))
            reason = result.get("reason", "N/A")
            return {"score": s, "detail": f"{s}/8 — {reason}"}
        except Exception:
            # Parse error fallback
            s = 3 if len(report) > 1000 else 1
            return {"score": s, "detail": f"{s}/8 — LLM response parse error, conservative fallback"}
    else:
        # LLM unavailable fallback
        s = 3 if len(report) > 1000 else 1
        return {"score": s, "detail": f"{s}/8 — LLM unavailable, conservative fallback"}


# ============================================================================
# Entry points
# ============================================================================

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Evaluate the agent's security log analysis output.

    Args:
        answer_dir: absolute path to the agent's output directory

    Returns:
        (score, report) where score is 0-100
    """
    s1, r1 = _check_file_delivery(answer_dir)
    s2, r2 = _check_script_quality(answer_dir)
    s3, r3 = _check_report_structure(answer_dir)
    s4, r4 = _check_threat_detection(answer_dir)

    total = min(100, s1 + s2 + s3 + s4)

    report = {
        "total_score": total,
        "dimensions": {
            "1_file_delivery": r1,
            "2_script_quality": r2,
            "3_report_structure": r3,
            "4_threat_detection": r4,
        },
        "summary": {
            "file_delivery": f"{s1}/10",
            "script_quality": f"{s2}/25",
            "report_structure": f"{s3}/25",
            "threat_detection": f"{s4}/40",
        },
    }

    if total >= 90:
        report["comment"] = "Excellent — comprehensive analysis with accurate threat detection."
    elif total >= 75:
        report["comment"] = "Good — solid analysis with minor gaps."
    elif total >= 60:
        report["comment"] = "Acceptable — basic analysis done but notable omissions."
    elif total >= 40:
        report["comment"] = "Partial — significant gaps in detection or reporting."
    else:
        report["comment"] = "Insufficient — critical deliverables missing or incorrect."

    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print a formatted evaluation report."""
    print("=" * 70)
    print("Security Log Analysis — Evaluation Report")
    print("=" * 70)
    print(f"\nTotal Score: {score}/100\n")

    summary = report.get("summary", {})
    print("Score Breakdown:")
    for dim, val in summary.items():
        print(f"  {dim}: {val}")

    dims = report.get("dimensions", {})
    for dim_name, dim_data in dims.items():
        print(f"\n{'─' * 50}")
        print(f"[{dim_name}] — {dim_data.get('score', 0)}/{dim_data.get('max', '?')}")
        print(f"{'─' * 50}")
        for k, v in dim_data.get("details", {}).items():
            print(f"  {k}: {v}")
        deds = dim_data.get("deductions", [])
        if deds:
            print("  Deductions:")
            for i, d in enumerate(deds, 1):
                print(f"    {i}. {d}")

    print(f"\n{'=' * 70}")
    print(f"Comment: {report.get('comment', '')}")
    print("=" * 70)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_dir = sys.argv[1]
    else:
        test_dir = os.path.join(os.path.dirname(__file__), "..", "workspace")

    # Resolve relative paths based on script location
    if not os.path.isabs(test_dir):
        test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", test_dir)

    if os.path.exists(test_dir):
        print(f"Evaluating directory: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"Directory does not exist: {test_dir}")
    sys.exit(0)
