"""
Rubric — LLM-based Reddit Privacy Information Automated Identification and Audit System

Total: 100 points

Scoring Dimensions:
I.   File Delivery (10 pts)
  - main.py exists (3 pts)
  - final_privacy_dataset.csv exists (3 pts)
  - Figure_1.png exists (2 pts)
  - Figure_2.png exists (2 pts)

II.  Code Quality (15 pts)
  - Python syntax correct (3 pts)
  - Data cleaning logic (3 pts)
  - LLM classification call logic (3 pts)
  - Audit logic (3 pts)
  - Visualization logic (3 pts)

III. Dataset Quality (30 pts)
  - Data size >= 50 records (8 pts)
  - Required columns exist (5 pts)
  - Data cleaning quality (7 pts)
  - Classification label quality (5 pts)
  - Audit result quality (5 pts)

IV.  Visualization Quality (15 pts) — Vision LLM
  - Figure_1.png privacy distribution chart (8 pts)
  - Figure_2.png confusion matrix chart (7 pts)

V.   System Integrity — LLM-as-Judge (30 pts)
  - End-to-end pipeline completeness (10 pts)
  - Privacy classification criteria reasonableness (10 pts)
  - Code-output consistency (10 pts)
"""

import os
import re
import ast
import csv
import json
import base64
import traceback
from typing import Tuple, Dict, Any, List, Optional

try:
    from PIL import Image
except ImportError:
    Image = None

try:
    import openai
except ImportError:
    openai = None


# ---------------------------------------------------------------------------
# Environment & LLM Calls
# ---------------------------------------------------------------------------

def _load_env(answer_dir: str) -> dict:
    """Load .env configuration from answer_dir and query root directory"""
    values = {}
    for env_dir in [answer_dir, os.path.join(os.path.dirname(__file__), "..")]:
        env_path = os.path.join(env_dir, ".env")
        if os.path.exists(env_path):
            with open(env_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    if k.strip() not in values:
                        values[k.strip()] = v.strip().strip("'\"")
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


def _get_vision_eval_config(answer_dir: str) -> dict:
    env = _load_env(answer_dir)
    def g(key, default=""):
        return os.environ.get(key) or env.get(key) or default
    return {
        "api_key": g("EVAL_VISION_API_KEY", g("ANTHROPIC_API_KEY")),
        "api_base": g("EVAL_VISION_API_BASE_URL", g("ANTHROPIC_BASE_URL")),
        "model": g("EVAL_VISION_MODEL", "openai/gpt-5.2"),
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


def _call_vision_judge(image_path: str, prompt: str, config: dict) -> str:
    if not openai or not config.get("api_key"):
        return ""
    try:
        with open(image_path, "rb") as f:
            image_b64 = base64.b64encode(f.read()).decode("utf-8")
        ext = os.path.splitext(image_path)[1].lower()
        mime = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".webp": "image/webp",
        }.get(ext, "image/png")
        base = config["api_base"].rstrip("/")
        if not base.endswith("/v1"):
            base += "/v1"
        client = openai.OpenAI(api_key=config["api_key"], base_url=base)
        resp = client.chat.completions.create(
            model=config["model"],
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url",
                     "image_url": {"url": f"data:{mime};base64,{image_b64}"}},
                ],
            }],
            max_tokens=1024,
            temperature=0,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        print(f"[RUBRIC] Vision Judge call failed: {e}")
        return ""


def _parse_json_from_llm(text: str) -> Optional[dict]:
    if not text:
        return None
    try:
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        return json.loads(text)
    except (json.JSONDecodeError, IndexError):
        return None


# ---------------------------------------------------------------------------
# Predefined 12 Privacy Categories
# ---------------------------------------------------------------------------

PRIVACY_CATEGORIES = [
    "Name", "Email", "Phone", "Address", "Location",
    "DOB_Age", "Financial", "Health", "Education",
    "Employment", "Credentials", "Government_ID",
]


# ---------------------------------------------------------------------------
# I. File Delivery (10 pts)
# ---------------------------------------------------------------------------

def _eval_file_delivery(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details: Dict[str, str] = {}
    files = os.listdir(answer_dir) if os.path.isdir(answer_dir) else []
    files_lower = {f.lower(): f for f in files}

    # main.py (3 pts)
    if "main.py" in files:
        score += 3
        details["main.py"] = "3/3 — exists"
    elif any(f.endswith(".py") for f in files):
        alt = next(f for f in files if f.endswith(".py"))
        score += 1
        details["main.py"] = f"1/3 — Python file exists but filename is wrong ({alt})"
    else:
        details["main.py"] = "0/3 — No Python file found"

    # final_privacy_dataset.csv (3 pts)
    if "final_privacy_dataset.csv" in files:
        score += 3
        details["final_privacy_dataset.csv"] = "3/3 — exists"
    elif any(f.endswith(".csv") for f in files):
        alt = next(f for f in files if f.endswith(".csv"))
        score += 1
        details["final_privacy_dataset.csv"] = f"1/3 — CSV exists but filename is wrong ({alt})"
    else:
        details["final_privacy_dataset.csv"] = "0/3 — No CSV file found"

    # Figure_1.png (2 pts)
    if "Figure_1.png" in files:
        score += 2
        details["Figure_1.png"] = "2/2 — exists"
    elif "figure_1.png" in files_lower:
        score += 2
        details["Figure_1.png"] = f"2/2 — exists (case mismatch: {files_lower['figure_1.png']})"
    elif any(f.lower().endswith(".png") for f in files):
        score += 1
        alt = next(f for f in files if f.lower().endswith(".png"))
        details["Figure_1.png"] = f"1/2 — PNG exists but filename mismatch ({alt})"
    else:
        details["Figure_1.png"] = "0/2 — not found"

    # Figure_2.png (2 pts)
    if "Figure_2.png" in files:
        score += 2
        details["Figure_2.png"] = "2/2 — exists"
    elif "figure_2.png" in files_lower:
        score += 2
        details["Figure_2.png"] = f"2/2 — exists (case mismatch: {files_lower['figure_2.png']})"
    else:
        other_pngs = [f for f in files if f.lower().endswith(".png")
                      and f.lower() not in ("figure_1.png",)]
        if other_pngs:
            score += 1
            details["Figure_2.png"] = f"1/2 — other PNG exists ({other_pngs[0]})"
        else:
            details["Figure_2.png"] = "0/2 — second image not found"

    return score, details


# ---------------------------------------------------------------------------
# II. Code Quality (15 pts)
# ---------------------------------------------------------------------------

def _find_main_py(answer_dir: str) -> Optional[str]:
    files = os.listdir(answer_dir) if os.path.isdir(answer_dir) else []
    if "main.py" in files:
        return os.path.join(answer_dir, "main.py")
    py_files = [f for f in files if f.endswith(".py")]
    if py_files:
        return os.path.join(answer_dir, py_files[0])
    return None


def _eval_code_quality(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details: Dict[str, str] = {}

    code_path = _find_main_py(answer_dir)
    if not code_path:
        details["error"] = "No Python file found, code quality score is 0"
        return 0, details

    try:
        with open(code_path, "r", encoding="utf-8", errors="ignore") as f:
            code = f.read()
    except Exception as e:
        details["error"] = f"Unable to read code: {e}"
        return 0, details

    # 2.1 Syntax check (3 pts)
    try:
        ast.parse(code)
        score += 3
        details["syntax_check"] = "3/3 — syntax correct"
    except SyntaxError as e:
        details["syntax_check"] = f"0/3 — syntax error: {str(e)[:80]}"
        return score, details

    code_lower = code.lower()

    # 2.2 Data cleaning logic (3 pts): HTML tag removal + escape handling + RSS/XML parsing
    clean_pts = 0
    has_html_strip = any(kw in code_lower for kw in [
        "beautifulsoup", "bs4", "re.sub", "html.unescape",
        "strip_tags", "get_text", "lxml", "htmlparser",
    ])
    has_escape = any(kw in code_lower for kw in [
        "unescape", "&amp;", "html.unescape", "escape",
    ])
    has_reddit_suffix = any(kw in code_lower for kw in [
        "submitted by", "submitted_by",
    ])
    has_xml_parse = any(kw in code_lower for kw in [
        "xml.etree", "elementtree", "feedparser", "rss",
        "xml.dom", "parsestring", "fromstring",
    ])
    if has_html_strip:
        clean_pts += 1
    if has_reddit_suffix or has_escape:
        clean_pts += 1
    if has_xml_parse:
        clean_pts += 1
    score += clean_pts
    details["data_cleaning"] = (
        f"{clean_pts}/3 — HTML removal:{'Y' if has_html_strip else 'N'} "
        f"Reddit suffix/escape:{'Y' if (has_reddit_suffix or has_escape) else 'N'} "
        f"XML parsing:{'Y' if has_xml_parse else 'N'}"
    )

    # 2.3 LLM/classification call (3 pts)
    cls_pts = 0
    has_llm_call = any(kw in code_lower for kw in [
        "openai", "chat.completions", "api_key", "client.chat",
        "anthropic", "llm_model",
    ])
    has_classification = any(kw in code_lower for kw in [
        "classif", "categoriz", "privacy_label", "predict",
        "category", "label",
    ])
    has_privacy_prompt = any(kw in code for kw in [
        "privacy", "Privacy", "classify", "Classify",
    ])
    if has_llm_call:
        cls_pts += 1
    if has_classification:
        cls_pts += 1
    if has_privacy_prompt:
        cls_pts += 1
    score += cls_pts
    details["classification_logic"] = (
        f"{cls_pts}/3 — LLM call:{'Y' if has_llm_call else 'N'} "
        f"Classification impl:{'Y' if has_classification else 'N'} "
        f"Privacy prompt:{'Y' if has_privacy_prompt else 'N'}"
    )

    # 2.4 Audit logic (3 pts)
    aud_pts = 0
    has_audit_concept = any(kw in code_lower for kw in [
        "audit", "verify", "review", "judge",
        "confirmed", "false positive", "false_positive",
    ])
    has_second_model = any(kw in code_lower for kw in [
        "judge_model", "audit_model", "reviewer",
        "llm_judge", "second", "higher",
    ])
    if has_audit_concept:
        aud_pts += 2
    if has_second_model:
        aud_pts += 1
    aud_pts = min(3, aud_pts)
    score += aud_pts
    details["audit_logic"] = (
        f"{aud_pts}/3 — Audit concept:{'Y' if has_audit_concept else 'N'} "
        f"Secondary model:{'Y' if has_second_model else 'N'}"
    )

    # 2.5 Visualization logic (3 pts)
    vis_pts = 0
    has_plot_lib = any(kw in code_lower for kw in [
        "matplotlib", "plt.bar", "plt.savefig", "seaborn", "sns.",
    ])
    has_confusion = any(kw in code_lower for kw in [
        "confusion", "heatmap", "matrix",
    ])
    has_distribution = any(kw in code_lower for kw in [
        "bar", "hist", "distribution", "countplot",
        "value_counts",
    ])
    if has_plot_lib:
        vis_pts += 1
    if has_confusion:
        vis_pts += 1
    if has_distribution:
        vis_pts += 1
    score += vis_pts
    details["visualization_logic"] = (
        f"{vis_pts}/3 — Plot library:{'Y' if has_plot_lib else 'N'} "
        f"Confusion matrix:{'Y' if has_confusion else 'N'} "
        f"Distribution chart:{'Y' if has_distribution else 'N'}"
    )

    return score, details


# ---------------------------------------------------------------------------
# III. Dataset Quality (30 pts)
# ---------------------------------------------------------------------------

def _find_csv(answer_dir: str) -> Optional[str]:
    files = os.listdir(answer_dir) if os.path.isdir(answer_dir) else []
    if "final_privacy_dataset.csv" in files:
        return os.path.join(answer_dir, "final_privacy_dataset.csv")
    csv_files = [f for f in files if f.endswith(".csv")]
    if csv_files:
        return os.path.join(answer_dir, csv_files[0])
    return None


def _eval_dataset_quality(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details: Dict[str, str] = {}

    csv_path = _find_csv(answer_dir)
    if not csv_path:
        details["error"] = "CSV dataset not found"
        return 0, details

    try:
        with open(csv_path, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames or []
            rows = list(reader)
    except Exception as e:
        details["error"] = f"CSV read failed: {e}"
        return 0, details

    num_rows = len(rows)
    headers_lower = [h.lower() for h in headers]

    # 3.1 Data size (8 pts): require >= 50 records
    if num_rows >= 50:
        s = 8
    elif num_rows >= 30:
        s = 5
    elif num_rows >= 10:
        s = 3
    elif num_rows > 0:
        s = 1
    else:
        s = 0
    score += s
    details["data_size"] = f"{s}/8 — {num_rows} records"

    # 3.2 Required columns (5 pts): raw_text, cleaned_text, label, audit, true_label
    has_text = any("text" in h or "content" in h or "body" in h for h in headers_lower)
    has_cleaned = any("clean" in h for h in headers_lower)
    has_label = any("label" in h or "tag" in h or "categor" in h or "class" in h
                     for h in headers_lower)
    has_audit = any("audit" in h or "confirm" in h or "review" in h or "verif" in h
                     for h in headers_lower)
    has_raw = any("raw" in h or "original" in h for h in headers_lower)

    col_pts = 0
    if has_text or has_raw:
        col_pts += 1
    if has_cleaned:
        col_pts += 1
    if has_label:
        col_pts += 1
    if has_audit:
        col_pts += 1
    if len(headers) >= 4:
        col_pts += 1
    col_pts = min(5, col_pts)
    score += col_pts
    details["required_columns"] = f"{col_pts}/5 — columns: {headers[:8]}"

    # 3.3 Data cleaning quality (7 pts): check if cleaned text contains HTML / escapes / Reddit suffix
    clean_col = None
    for h in headers:
        if "clean" in h.lower():
            clean_col = h
            break
    if not clean_col:
        for h in headers:
            if "text" in h.lower() and "raw" not in h.lower():
                clean_col = h
                break

    if clean_col and num_rows > 0:
        total_check = min(num_rows, 80)
        dirty_count = 0
        empty_count = 0
        for row in rows[:total_check]:
            txt = row.get(clean_col, "")
            if not txt or len(txt.strip()) < 5:
                empty_count += 1
                continue
            if re.search(r"<[a-z][a-z0-9]*[\s>]", txt, re.IGNORECASE):
                dirty_count += 1
            elif "&amp;" in txt or "&lt;" in txt or "&gt;" in txt:
                dirty_count += 1
            elif "submitted by" in txt.lower() and "u/" in txt:
                dirty_count += 1

        non_empty = max(1, total_check - empty_count)
        clean_ratio = 1.0 - (dirty_count / non_empty)
        empty_ratio = empty_count / max(1, total_check)

        if clean_ratio >= 0.95 and empty_ratio < 0.1:
            cs = 7
        elif clean_ratio >= 0.8 and empty_ratio < 0.2:
            cs = 5
        elif clean_ratio >= 0.5:
            cs = 3
        elif num_rows > 0:
            cs = 1
        else:
            cs = 0
        score += cs
        details["cleaning_quality"] = (
            f"{cs}/7 — checked {total_check} records: dirty {dirty_count}, "
            f"empty {empty_count}, clean ratio {clean_ratio:.0%}"
        )
    else:
        details["cleaning_quality"] = "0/7 — cleaned text column not found"

    # 3.4 Classification label quality (5 pts)
    label_col = None
    for h in headers:
        hl = h.lower()
        if "predicted" in hl or "label" in hl or "tag" in hl or "categor" in hl:
            label_col = h
            break

    if label_col and num_rows > 0:
        labels = [row.get(label_col, "").strip() for row in rows
                  if row.get(label_col, "").strip()]
        unique_labels = set(labels)
        matched = sum(
            1 for cat in PRIVACY_CATEGORIES
            if any(cat.lower() in lbl.lower() for lbl in unique_labels)
        )
        if len(unique_labels) >= 5 and matched >= 3:
            ls = 5
        elif len(unique_labels) >= 3 and matched >= 2:
            ls = 3
        elif len(unique_labels) >= 2:
            ls = 2
        elif len(unique_labels) >= 1:
            ls = 1
        else:
            ls = 0
        score += ls
        details["classification_labels"] = (
            f"{ls}/5 — {len(unique_labels)} unique labels, "
            f"matched {matched}/12 privacy categories"
        )
    else:
        details["classification_labels"] = "0/5 — classification label column not found or no data"

    # 3.5 Audit result quality (5 pts)
    audit_col = None
    for h in headers:
        hl = h.lower()
        if "audit" in hl and "json" not in hl:
            audit_col = h
            break
    if not audit_col:
        for h in headers:
            if "audit" in h.lower() or "confirm" in h.lower() or "review" in h.lower():
                audit_col = h
                break

    if audit_col and num_rows > 0:
        audit_vals = [row.get(audit_col, "").strip().lower() for row in rows
                      if row.get(audit_col, "").strip()]
        unique_audit = set(audit_vals)
        has_confirmed = any("confirm" in v for v in unique_audit)
        has_fp = any("false" in v or v == "fp" for v in unique_audit)
        has_missing = any("missing" in v or v == "fn" for v in unique_audit)
        coverage = len(audit_vals) / max(1, num_rows)

        if has_confirmed and coverage >= 0.8:
            if has_fp or has_missing:
                aus = 5
            else:
                aus = 3
        elif len(audit_vals) > 0:
            aus = 2
        else:
            aus = 0
        score += aus
        details["audit_results"] = (
            f"{aus}/5 — audit values: {sorted(unique_audit)[:5]}, "
            f"coverage {len(audit_vals)}/{num_rows}"
        )
    else:
        details["audit_results"] = "0/5 — audit result column not found"

    return score, details


# ---------------------------------------------------------------------------
# IV. Visualization Quality (15 pts) — Vision LLM
# ---------------------------------------------------------------------------

_FIG1_PROMPT = """\
You are a strict data visualization review expert. This image should be a distribution chart of Reddit user privacy information (e.g., bar chart / pie chart).

Please score the following dimensions (integers) and provide brief justifications:

**Dimension 1: Chart Type Correctness** (0-3 pts)
  - 3: Appropriate distribution chart (bar / pie / etc.), suitable for showing category distributions
  - 1-2: Has a chart but the type is not very appropriate
  - 0: Not a distribution chart / blank / error

**Dimension 2: Labels and Title** (0-3 pts)
  - 3: Clear title, X/Y axis labels, privacy category names are readable
  - 1-2: Some labels are missing or unclear
  - 0: No labels

**Dimension 3: Data Reasonableness** (0-2 pts)
  - 2: Data is reasonable, multiple categories have distribution
  - 1: Data exists but distribution is extreme (e.g., only 1-2 categories)
  - 0: No data or obvious errors

Please respond strictly in the following JSON format:
```json
{
  "chart_type": {"score": 0, "reason": ""},
  "labels": {"score": 0, "reason": ""},
  "data_quality": {"score": 0, "reason": ""},
  "total": 0
}
```"""

_FIG2_PROMPT = """\
You are a strict data visualization review expert. This image should be a confusion matrix or error rate chart for privacy classification.

Please score the following dimensions (integers) and provide brief justifications:

**Dimension 1: Chart Type Correctness** (0-3 pts)
  - 3: Is a confusion matrix heatmap or a reasonable classification error rate chart
  - 1-2: Has a chart but not a standard confusion matrix / error rate chart
  - 0: Not a confusion matrix / error rate chart / blank / error

**Dimension 2: Labels and Title** (0-2 pts)
  - 2: Clear title, axis labels, category names
  - 1: Some labels are missing
  - 0: No labels

**Dimension 3: Data Reasonableness** (0-2 pts)
  - 2: Matrix / data looks reasonable
  - 1: Data exists but has obvious issues
  - 0: No data or obvious errors

Please respond strictly in the following JSON format:
```json
{
  "chart_type": {"score": 0, "reason": ""},
  "labels": {"score": 0, "reason": ""},
  "data_quality": {"score": 0, "reason": ""},
  "total": 0
}
```"""


def _find_figure(answer_dir: str, target_name: str) -> Optional[str]:
    """Find image file with case-insensitive matching."""
    files = os.listdir(answer_dir) if os.path.isdir(answer_dir) else []
    if target_name in files:
        return os.path.join(answer_dir, target_name)
    target_lower = target_name.lower()
    for f in files:
        if f.lower() == target_lower:
            return os.path.join(answer_dir, f)
    return None


def _eval_single_figure(answer_dir: str, target_name: str, prompt: str,
                        max_score: int, config: dict) -> Tuple[int, dict]:
    img_path = _find_figure(answer_dir, target_name)
    if not img_path:
        # Try matching any PNG
        files = os.listdir(answer_dir) if os.path.isdir(answer_dir) else []
        pngs = [f for f in files if f.lower().endswith(".png")]
        if target_name == "Figure_2.png":
            pngs = [f for f in pngs if f.lower() != "figure_1.png"]
        if pngs:
            img_path = os.path.join(answer_dir, pngs[0])
        else:
            return 0, {"error": f"Image {target_name} does not exist"}

    fsize = os.path.getsize(img_path)
    if fsize < 1024:
        return 0, {"error": f"Image file too small ({fsize} bytes)"}

    # Vision LLM evaluation
    raw = _call_vision_judge(img_path, prompt, config)
    result = _parse_json_from_llm(raw)

    if result:
        ct = max(0, min(3, int(result.get("chart_type", {}).get("score", 0))))
        lb_max = 3 if max_score == 8 else 2
        lb = max(0, min(lb_max, int(result.get("labels", {}).get("score", 0))))
        dq = max(0, min(2, int(result.get("data_quality", {}).get("score", 0))))
        raw_total = ct + lb + dq
        denom = 8 if max_score == 8 else 7
        scaled = round(raw_total / denom * max_score)
        return scaled, {
            "chart_type": f"{ct}/3 — {result.get('chart_type', {}).get('reason', '')}",
            "labels_title": f"{lb}/{lb_max} — {result.get('labels', {}).get('reason', '')}",
            "data_reasonableness": f"{dq}/2 — {result.get('data_quality', {}).get('reason', '')}",
            "raw_score": f"{raw_total}/{denom}",
            "scaled_score": f"{scaled}/{max_score}",
        }
    else:
        # Fallback: basic file check
        fb_score = 0
        if Image:
            try:
                img = Image.open(img_path)
                w, h = img.size
                if w >= 300 and h >= 200 and fsize >= 10 * 1024:
                    fb_score = max(1, max_score // 3)
                else:
                    fb_score = 1
                return fb_score, {
                    "fallback_eval": f"{fb_score}/{max_score} — {w}x{h}, {fsize / 1024:.0f}KB (Vision unavailable)"
                }
            except Exception:
                return 0, {"fallback_eval": f"0/{max_score} — image cannot be opened"}
        else:
            if fsize >= 10 * 1024:
                fb_score = max(1, max_score // 4)
            return fb_score, {
                "fallback_eval": f"{fb_score}/{max_score} — {fsize / 1024:.0f}KB (PIL+Vision unavailable)"
            }


def _eval_visualization(answer_dir: str) -> Tuple[int, dict]:
    config = _get_vision_eval_config(answer_dir)
    s1, d1 = _eval_single_figure(answer_dir, "Figure_1.png", _FIG1_PROMPT, 8, config)
    s2, d2 = _eval_single_figure(answer_dir, "Figure_2.png", _FIG2_PROMPT, 7, config)
    return s1 + s2, {
        "Figure_1 privacy distribution (8 pts)": d1,
        "Figure_2 confusion matrix (7 pts)": d2,
    }


# ---------------------------------------------------------------------------
# V. System Integrity — LLM-as-Judge (30 pts)
# ---------------------------------------------------------------------------

def _eval_system_integrity(answer_dir: str) -> Tuple[int, dict]:
    config = _get_text_eval_config(answer_dir)
    details: Dict[str, str] = {}
    files = os.listdir(answer_dir) if os.path.isdir(answer_dir) else []

    # Read code
    code_content = ""
    code_path = _find_main_py(answer_dir)
    if code_path:
        try:
            with open(code_path, "r", encoding="utf-8", errors="ignore") as f:
                code_content = f.read()[:5000]
        except Exception:
            pass

    # Read CSV sample
    csv_sample = ""
    csv_path = _find_csv(answer_dir)
    if csv_path:
        try:
            with open(csv_path, "r", encoding="utf-8", errors="ignore") as f:
                csv_sample = "".join(f.readlines()[:12])
        except Exception:
            pass

    if not code_content and not csv_sample:
        details["error"] = "No code or data available for evaluation"
        return 0, details

    prompt = f"""\
You are a strict code review expert. Please evaluate the following Reddit privacy information automated identification and audit system.

Task requirements:
1. Data cleaning: Parse Reddit RSS XML data, extract post bodies, remove HTML tags, escape characters, and Reddit-specific suffixes
2. Privacy classification: Use an LLM to classify and label text according to 12 predefined privacy categories
3. Closed-loop audit: Call a higher-tier model as an auditor to verify classification results, outputting Confirmed/False Positive/Missing
4. Visual report: Compute privacy distribution statistics, calculate Accuracy/FPR/FNR, generate distribution chart and confusion matrix

Code (first 5000 characters):
```python
{code_content[:5000]}
```

CSV data sample (first 12 rows):
```
{csv_sample[:2500]}
```

Output files: {[f for f in files if not f.startswith('.')]}

Please strictly evaluate the following three dimensions:

**Dimension A: End-to-end Pipeline Completeness** (0-10 pts)
  - 10: Fully implements cleaning -> classification -> audit -> visualization pipeline
  - 7-9: Mostly complete but one stage has defects
  - 4-6: Missing 1-2 key stages
  - 0-3: Severely incomplete

**Dimension B: Privacy Classification Criteria Reasonableness** (0-10 pts)
  - 10: Fully uses 12 privacy categories with clear classification logic
  - 7-9: Uses most categories, classification is mostly reasonable
  - 4-6: Incomplete categories or simplistic classification logic
  - 0-3: Classification criteria missing or highly unreasonable

**Dimension C: Code-Output Consistency** (0-10 pts)
  - 10: Code logic and CSV output are fully consistent, data is trustworthy
  - 7-9: Mostly consistent, minor issues
  - 4-6: Obviously inconsistent (e.g., code calls LLM but all results use heuristic fallback)
  - 0-3: Code and output severely mismatched

Please respond strictly in the following JSON format:
```json
{{
  "pipeline_completeness": {{"score": 0, "reason": ""}},
  "classification_quality": {{"score": 0, "reason": ""}},
  "consistency": {{"score": 0, "reason": ""}},
  "total": 0
}}
```"""

    raw = _call_llm_judge(prompt, config)
    result = _parse_json_from_llm(raw)

    if result:
        pc = max(0, min(10, int(result.get("pipeline_completeness", {}).get("score", 0))))
        cq = max(0, min(10, int(result.get("classification_quality", {}).get("score", 0))))
        co = max(0, min(10, int(result.get("consistency", {}).get("score", 0))))
        total = pc + cq + co
        details["end_to_end_pipeline"] = f"{pc}/10 — {result.get('pipeline_completeness', {}).get('reason', '')}"
        details["classification_criteria"] = f"{cq}/10 — {result.get('classification_quality', {}).get('reason', '')}"
        details["code_output_consistency"] = f"{co}/10 — {result.get('consistency', {}).get('reason', '')}"
        return total, details
    else:
        # Fallback: keyword-based detection
        fb_score = 0
        if code_content:
            cl = code_content.lower()
            stages = 0
            if any(kw in cl for kw in ["xml", "rss", "beautifulsoup", "html"]):
                stages += 1
            if any(kw in cl for kw in ["classif", "label", "categor"]):
                stages += 1
            if any(kw in cl for kw in ["audit", "confirm", "review"]):
                stages += 1
            if any(kw in cl for kw in ["plt.", "matplotlib", "figure", "savefig"]):
                stages += 1
            fb_score = min(15, stages * 4)
            details["fallback_eval"] = f"{fb_score}/30 — detected {stages}/4 pipeline stages (LLM unavailable)"
        else:
            details["fallback_eval"] = "0/30 — no code and LLM unavailable"
        return fb_score, details


# ---------------------------------------------------------------------------
# Main Evaluation Function
# ---------------------------------------------------------------------------

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Evaluate the agent's output.

    Args:
        answer_dir: Absolute path to the agent's output directory

    Returns:
        (score, report)
        - score: integer from 0 to 100
        - report: dict containing the detailed evaluation report
    """
    report: Dict[str, Any] = {}

    s1, d1 = _eval_file_delivery(answer_dir)
    report["I. File Delivery (10 pts)"] = {"score": s1, "details": d1}

    s2, d2 = _eval_code_quality(answer_dir)
    report["II. Code Quality (15 pts)"] = {"score": s2, "details": d2}

    s3, d3 = _eval_dataset_quality(answer_dir)
    report["III. Dataset Quality (30 pts)"] = {"score": s3, "details": d3}

    s4, d4 = _eval_visualization(answer_dir)
    report["IV. Visualization Quality (15 pts)"] = {"score": s4, "details": d4}

    s5, d5 = _eval_system_integrity(answer_dir)
    report["V. System Integrity (30 pts)"] = {"score": s5, "details": d5}

    total = max(0, min(100, s1 + s2 + s3 + s4 + s5))

    report["section_scores"] = {
        "file_delivery": f"{s1}/10",
        "code_quality": f"{s2}/15",
        "dataset_quality": f"{s3}/30",
        "visualization_quality": f"{s4}/15",
        "system_integrity": f"{s5}/30",
    }

    if total >= 85:
        report["comment"] = "Excellent. The system fully implements data cleaning, classification, audit, and visualization pipeline."
    elif total >= 70:
        report["comment"] = "Good. Task mostly completed, but some areas have room for improvement."
    elif total >= 50:
        report["comment"] = "Acceptable. Core features partially implemented, with notable deficiencies."
    elif total >= 30:
        report["comment"] = "Partial completion. Key stages missing or output quality insufficient."
    else:
        report["comment"] = "Insufficient. Task completion severely lacking."

    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print formatted scoring report."""
    print("=" * 70)
    print("  en_privacy_audit Scoring Report")
    print("  Task: Build an LLM-based Reddit Privacy Information Automated Identification and Audit System")
    print("=" * 70)
    print(f"\n  Total Score: {score}/100\n")

    scores = report.get("section_scores", {})
    if scores:
        print("  Section Scores:")
        for k, v in scores.items():
            print(f"    {k}: {v}")
        print()

    for section_key in [
        "I. File Delivery (10 pts)",
        "II. Code Quality (15 pts)",
        "III. Dataset Quality (30 pts)",
        "IV. Visualization Quality (15 pts)",
        "V. System Integrity (30 pts)",
    ]:
        section = report.get(section_key, {})
        if not section:
            continue
        print(f"  {'─' * 60}")
        print(f"  [{section_key}] Score: {section.get('score', 0)}")
        print(f"  {'─' * 60}")
        details = section.get("details", {})
        for k, v in details.items():
            if isinstance(v, dict):
                print(f"    {k}:")
                for kk, vv in v.items():
                    print(f"      {kk}: {vv}")
            else:
                print(f"    {k}: {v}")
        print()

    print(f"  {'=' * 60}")
    print(f"  Comment: {report.get('comment', '')}")
    print("=" * 70)


if __name__ == "__main__":
    import sys
    test_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(__file__), "..", "gpt-5", "attempt_1")
    if os.path.exists(test_dir):
        print(f"Evaluating directory: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"Directory does not exist: {test_dir}")
    sys.exit(0)
