"""
Sphere UFormer Data Export Scoring Script (rubric.py)

Task Overview:
  Read data_rgb.png and data_depth.png, export them as icosphere point cloud
  files in Sphere UFormer (CVPR 2025) format: rgb.npy (n,6) and depth.npy (n,4).
  Also implement model.py (model architecture), train.py (training script),
  answer/compare_npy.py (comparison script), and answer/export.py (export script).

Total Score: 100 points

Scoring Dimensions:
  I.   File Delivery              15 points
  II.  Code Quality               20 points
  III. Data Correctness           45 points (including RMSE comparison with reference)
  IV.  Implementation Depth (LLM) 20 points
"""

import os
import ast
import json
import traceback
from typing import Tuple, Dict, Any, List, Optional

try:
    import numpy as np
except ImportError:
    np = None

try:
    import openai
except ImportError:
    openai = None


# =========================================================================
# Environment / LLM Utilities
# =========================================================================

def _load_env(answer_dir: str) -> dict:
    """Load .env configuration, answer_dir takes priority"""
    values: Dict[str, str] = {}
    for d in [answer_dir, os.path.join(os.path.dirname(__file__), "..")]:
        p = os.path.join(d, ".env")
        if os.path.exists(p):
            try:
                with open(p, "r") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#") or "=" not in line:
                            continue
                        k, v = line.split("=", 1)
                        k, v = k.strip(), v.strip().strip("'\"")
                        if k not in values:
                            values[k] = v
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


# =========================================================================
# File Search Utilities
# =========================================================================

_REF_DIR = os.path.join(os.path.dirname(__file__), "..", "_answers_backup", "answer")


def _find_file(base: str, rel: str) -> str:
    """Flexibly search for a deliverable in answer_dir."""
    # Exact path
    exact = os.path.join(base, rel)
    if os.path.isfile(exact):
        return exact
    # Flattened (filename only)
    bn = os.path.basename(rel)
    flat = os.path.join(base, bn)
    if os.path.isfile(flat):
        return flat
    # Recursive search
    for root, _dirs, files in os.walk(base):
        if bn in files:
            return os.path.join(root, bn)
    return ""


def _read_text(path: str, limit: int = 0) -> Optional[str]:
    if not path or not os.path.isfile(path):
        return None
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
        if limit and len(text) > limit:
            text = text[:limit] + "\n... (truncated)"
        return text
    except Exception:
        return None


# =========================================================================
# I. File Delivery (15 points)
# =========================================================================

DELIVERABLES = {
    "model.py":              2,
    "train.py":              2,
    "answer/compare_npy.py": 2,
    "answer/export.py":      3,
    "answer/rgb.npy":        3,
    "answer/depth.npy":      3,
}


def _eval_file_delivery(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details: Dict[str, str] = {}
    found: Dict[str, str] = {}
    for rel, pts in DELIVERABLES.items():
        path = _find_file(answer_dir, rel)
        if path:
            score += pts
            details[rel] = f"{pts}/{pts} - found ({os.path.relpath(path, answer_dir)})"
            found[rel] = path
        else:
            details[rel] = f"0/{pts} - missing"
    return score, {"score": score, "max": 15, "details": details, "found": found}


# =========================================================================
# II. Code Quality (20 points)
# =========================================================================

def _syntax_and_patterns(path: str, patterns: List[str], max_pts: int) -> Tuple[int, str]:
    code = _read_text(path)
    if code is None:
        return 0, "file missing"
    if len(code.strip()) < 20:
        return 0, "file nearly empty"
    try:
        ast.parse(code)
    except SyntaxError as e:
        return max(1, round(max_pts * 0.1)), f"syntax error: {str(e)[:80]}"
    low = code.lower()
    hit = sum(1 for p in patterns if p.lower() in low)
    ratio = hit / len(patterns) if patterns else 1.0
    if ratio >= 0.7:
        pts = max_pts
    elif ratio >= 0.4:
        pts = round(max_pts * 0.65)
    elif ratio > 0:
        pts = round(max_pts * 0.35)
    else:
        pts = round(max_pts * 0.15)
    return pts, f"syntax ok, matched {hit}/{len(patterns)} patterns"


def _eval_code_quality(answer_dir: str, found: dict) -> Tuple[int, dict]:
    total = 0
    details: Dict[str, str] = {}

    # model.py (7 pts): expect NN / Transformer architecture
    pts, msg = _syntax_and_patterns(
        found.get("model.py", ""),
        ["class", "torch", "forward", "self", "nn.module",
         "attention", "encoder", "decoder"],
        7,
    )
    total += pts
    details["model.py (7)"] = f"{pts}/7 - {msg}"

    # train.py (5 pts): training loop
    pts, msg = _syntax_and_patterns(
        found.get("train.py", ""),
        ["train", "loss", "optimizer", "epoch", "torch",
         "backward", "dataloader"],
        5,
    )
    total += pts
    details["train.py (5)"] = f"{pts}/5 - {msg}"

    # export.py (5 pts): sphere export logic
    pts, msg = _syntax_and_patterns(
        found.get("answer/export.py", ""),
        ["numpy", "npy", "sphere", "rgb", "depth",
         "save", "image", "grid_sample"],
        5,
    )
    total += pts
    details["export.py (5)"] = f"{pts}/5 - {msg}"

    # compare_npy.py (3 pts): comparison
    pts, msg = _syntax_and_patterns(
        found.get("answer/compare_npy.py", ""),
        ["numpy", "npy", "load", "rmse", "score", "distance"],
        3,
    )
    total += pts
    details["compare_npy.py (3)"] = f"{pts}/3 - {msg}"

    return total, {"score": total, "max": 20, "details": details}


# =========================================================================
# III. Data Correctness (45 points)
#     rgb.npy  22.5 points
#     depth.npy 22.5 points
#
#   Score composition (percentage of per-file max_pts):
#     - Loadable as 2D array      8%
#     - Correct number of columns 12%
#     - Row count > 100            5%
#     - No NaN/Inf                 5%
#     - xyz approximately unit sphere 10%
#     - RMSE comparison with reference 60% (closer is better)
# =========================================================================

def _rmse(a, b):
    diff = a.astype(np.float64) - b.astype(np.float64)
    return float(np.sqrt(np.mean(diff * diff)))


def _score_npy(filepath: str, expected_cols: int, ref_path: str,
               max_pts: float) -> Tuple[float, dict]:
    """Evaluate a single npy file and return the score and details."""
    info: Dict[str, str] = {}
    if not filepath or not os.path.isfile(filepath):
        return 0.0, {"result": f"0/{max_pts:.0f} - file not found"}
    if np is None:
        return 0.0, {"result": f"0/{max_pts:.0f} - numpy unavailable"}

    try:
        data = np.load(filepath, allow_pickle=False)
    except Exception as e:
        return 0.0, {"result": f"0/{max_pts:.0f} - load error: {str(e)[:80]}"}

    pts = 0.0

    # --- Basic shape checks ---
    if data.ndim != 2:
        info["shape"] = f"wrong ndim={data.ndim}"
        return round(max_pts * 0.03), info

    pts += max_pts * 0.08
    info["shape"] = f"{data.shape[0]} x {data.shape[1]}"

    if data.shape[1] == expected_cols:
        pts += max_pts * 0.12
        info["cols"] = f"correct ({expected_cols})"
    else:
        info["cols"] = f"wrong ({data.shape[1]} vs expected {expected_cols})"

    if data.shape[0] > 100:
        pts += max_pts * 0.05
        info["rows"] = f"{data.shape[0]} (ok)"
    else:
        info["rows"] = f"{data.shape[0]} (too few)"

    # --- NaN / Inf ---
    has_nan = bool(np.isnan(data).any()) if not np.issubdtype(data.dtype, np.integer) else False
    has_inf = bool(np.isinf(data).any()) if not np.issubdtype(data.dtype, np.integer) else False
    if not has_nan and not has_inf:
        pts += max_pts * 0.05
        info["integrity"] = "no NaN/Inf"
    else:
        info["integrity"] = f"NaN={int(np.isnan(data).sum())} Inf={int(np.isinf(data).sum())}"

    # --- xyz unit sphere check ---
    if data.shape[1] >= 3 and data.shape[0] > 0:
        xyz = data[:, :3].astype(np.float64)
        norms = np.linalg.norm(xyz, axis=1)
        mn, sd = float(np.mean(norms)), float(np.std(norms))
        if 0.95 <= mn <= 1.05 and sd < 0.05:
            pts += max_pts * 0.10
            info["xyz"] = f"unit sphere (mean={mn:.4f} std={sd:.4f})"
        elif 0.8 <= mn <= 1.2 and sd < 0.3:
            pts += max_pts * 0.05
            info["xyz"] = f"approx unit sphere (mean={mn:.4f} std={sd:.4f})"
        else:
            info["xyz"] = f"not unit sphere (mean={mn:.4f} std={sd:.4f})"

    # --- Reference answer RMSE comparison (60%) ---
    ref_weight = 0.60
    if ref_path and os.path.isfile(ref_path):
        try:
            ref = np.load(ref_path, allow_pickle=False)
            if ref.shape == data.shape:
                dist = _rmse(data, ref)
                # Map to [0,1] using 1/(1+dist)
                sim = 1.0 / (1.0 + dist)
                earned = max_pts * ref_weight * sim
                pts += earned
                info["ref_compare"] = (
                    f"RMSE={dist:.4f} sim={sim:.4f} => {earned:.1f}/{max_pts * ref_weight:.1f}"
                )
            elif data.shape[1] == ref.shape[1]:
                # Different row counts => truncate and compare with scaling
                min_r = min(data.shape[0], ref.shape[0])
                dist = _rmse(data[:min_r], ref[:min_r])
                sim = 1.0 / (1.0 + dist)
                row_ratio = min_r / max(data.shape[0], ref.shape[0])
                earned = max_pts * ref_weight * sim * row_ratio
                pts += earned
                info["ref_compare"] = (
                    f"RMSE={dist:.4f} (first {min_r} rows), row_ratio={row_ratio:.2f}, "
                    f"earned={earned:.1f}/{max_pts * ref_weight:.1f}"
                )
            else:
                info["ref_compare"] = f"shape mismatch: {data.shape} vs ref {ref.shape}"
        except Exception as e:
            info["ref_compare"] = f"compare error: {str(e)[:80]}"
    else:
        # No reference => conservative base score only
        pts += max_pts * 0.05
        info["ref_compare"] = "reference not available, conservative score"

    return pts, info


def _eval_data_correctness(answer_dir: str, found: dict) -> Tuple[int, dict]:
    rgb_path = found.get("answer/rgb.npy", "")
    depth_path = found.get("answer/depth.npy", "")
    rgb_ref = os.path.join(_REF_DIR, "rgb.npy")
    depth_ref = os.path.join(_REF_DIR, "depth.npy")

    s_rgb, d_rgb = _score_npy(rgb_path, 6, rgb_ref, 22.5)
    s_dep, d_dep = _score_npy(depth_path, 4, depth_ref, 22.5)
    total = round(s_rgb + s_dep)
    return total, {
        "score": total,
        "max": 45,
        "details": {
            "rgb.npy (22.5)": d_rgb,
            "depth.npy (22.5)": d_dep,
        },
    }


# =========================================================================
# IV. Implementation Depth - LLM-as-Judge (20 points)
#   Dimensions:
#     Spherical processing correctness  0-8
#     Model architecture completeness   0-7
#     Code engineering quality           0-5
# =========================================================================

_LLM_PROMPT = """\
You are a strict code review expert evaluating a Sphere UFormer spherical image processing model implementation.

### Task Background
Sphere UFormer (CVPR 2025) maps ERP panoramic images to icosphere point clouds, then uses a U-shaped
Transformer for spherical self-attention processing. The agent needs to:
1. model.py - Implement the model architecture (spherical attention, U-Net encoder-decoder, etc.)
2. train.py - Training script
3. export.py - Convert ERP images to icosphere point clouds and save as .npy
4. compare_npy.py - Compare two .npy files

### Core Technical Points
- icosphere representation + trimesh_utils
- Spherical Local Self-Attention
- grid_sample spherical sampling
- U-shaped encoder-decoder
- Point cloud (n,6) / (n,4) format

### Code to Evaluate
{code_block}

### Scoring Requirements (integers, provide brief justification)

**Dimension 1: Spherical Processing Correctness (0-8)**
  8: icosphere representation correct, spherical sampling accurate, coordinate transformations correct
  5-7: Basic understanding but details are wrong
  2-4: Attempted but obvious problems
  0-1: Not implemented or completely wrong

**Dimension 2: Model Architecture Completeness (0-7)**
  7: Complete U-shaped Transformer (encoder + decoder + attention modules)
  4-6: Architecture exists but missing key components
  1-3: Model definition exists but incomplete
  0: No model

**Dimension 3: Code Engineering Quality (0-5)**
  5: Clear, modular, with error handling
  3-4: Runnable but average organization
  1-2: Code exists but poor quality
  0: Unusable

Please respond strictly in the following JSON format with no other content:
```json
{{
  "sphere_processing": {{"score": 0, "reason": ""}},
  "model_architecture": {{"score": 0, "reason": ""}},
  "code_quality": {{"score": 0, "reason": ""}},
  "total": 0
}}
```"""


def _eval_implementation(answer_dir: str, found: dict) -> Tuple[int, dict]:
    """LLM-as-Judge evaluation of code implementation depth"""
    code_parts: List[str] = []
    for name in ["model.py", "train.py", "answer/export.py", "answer/compare_npy.py"]:
        text = _read_text(found.get(name, ""), limit=3500)
        if text:
            code_parts.append(f"=== {name} ===\n{text}")

    if not code_parts:
        return 0, {"score": 0, "max": 20, "details": {"error": "no code files to evaluate"}}

    prompt = _LLM_PROMPT.format(code_block="\n\n".join(code_parts))
    config = _get_text_eval_config(answer_dir)
    raw = _call_llm_judge(prompt, config)

    if not raw:
        # fallback: conservative score = 2 points per code file found
        fb = min(8, len(code_parts) * 2)
        return fb, {
            "score": fb, "max": 20,
            "details": {"fallback": f"{fb}/20 - LLM unavailable, {len(code_parts)} code files found"},
        }

    # Parse JSON
    try:
        text = raw
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        result = json.loads(text)

        sp = max(0, min(8, int(result.get("sphere_processing", {}).get("score", 0))))
        ma = max(0, min(7, int(result.get("model_architecture", {}).get("score", 0))))
        cq = max(0, min(5, int(result.get("code_quality", {}).get("score", 0))))
        total = sp + ma + cq

        details = {
            "sphere_processing (8)": f"{sp}/8 - {result.get('sphere_processing', {}).get('reason', '')}",
            "model_architecture (7)": f"{ma}/7 - {result.get('model_architecture', {}).get('reason', '')}",
            "code_quality (5)": f"{cq}/5 - {result.get('code_quality', {}).get('reason', '')}",
        }
        return total, {"score": total, "max": 20, "details": details}

    except (json.JSONDecodeError, TypeError, ValueError) as e:
        return 5, {
            "score": 5, "max": 20,
            "details": {"parse_error": f"5/20 - {str(e)[:80]}", "raw": raw[:300]},
        }


# =========================================================================
# Main Entry
# =========================================================================

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Evaluate agent output.

    Args:
        answer_dir: Absolute path to the agent output directory

    Returns:
        (score, report)  score: 0-100 integer, report: dict
    """
    s1, r1 = _eval_file_delivery(answer_dir)
    found = r1.get("found", {})

    s2, r2 = _eval_code_quality(answer_dir, found)
    s3, r3 = _eval_data_correctness(answer_dir, found)
    s4, r4 = _eval_implementation(answer_dir, found)

    total = max(0, min(100, s1 + s2 + s3 + s4))

    report: Dict[str, Any] = {
        "total": total,
        "breakdown": {
            "file_delivery":        f"{s1}/15",
            "code_quality":         f"{s2}/20",
            "data_correctness":     f"{s3}/45",
            "implementation_depth": f"{s4}/20",
        },
        "section_details": {
            "1_file_delivery (15)":        r1.get("details", {}),
            "2_code_quality (20)":         r2.get("details", {}),
            "3_data_correctness (45)":     r3.get("details", {}),
            "4_implementation_depth (20)": r4.get("details", {}),
        },
    }

    if total >= 85:
        report["comment"] = "Excellent - complete implementation with correct data conversion."
    elif total >= 65:
        report["comment"] = "Good - mostly complete but room for improvement."
    elif total >= 45:
        report["comment"] = "Partial - core parts exist but significant issues."
    elif total >= 20:
        report["comment"] = "Weak - key deliverables missing or data incorrect."
    else:
        report["comment"] = "Insufficient - task barely attempted."

    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print formatted evaluation report."""
    sep = "=" * 70
    print(sep)
    print("Sphere UFormer Data Export - Evaluation Report")
    print(sep)
    print(f"\nTotal score: {score}/100\n")

    bd = report.get("breakdown", {})
    if bd:
        print("Breakdown:")
        for k, v in bd.items():
            print(f"  {k}: {v}")

    for section, items in report.get("section_details", {}).items():
        print(f"\n{'─' * 60}")
        print(f"[{section}]")
        print(f"{'─' * 60}")
        if isinstance(items, dict):
            for k, v in items.items():
                if isinstance(v, dict):
                    print(f"  {k}:")
                    for kk, vv in v.items():
                        print(f"    {kk}: {vv}")
                else:
                    print(f"  {k}: {v}")
        else:
            print(f"  {items}")

    print(f"\n{sep}")
    print(f"Comment: {report.get('comment', '')}")
    print(sep)


# =========================================================================
# CLI
# =========================================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = os.path.join(os.path.dirname(__file__), "..", "gpt-5", "attempt_1")

    if not os.path.isabs(target):
        target = os.path.join(os.path.dirname(__file__), "..", target)
    target = os.path.abspath(target)

    if os.path.exists(target):
        print(f"Evaluating: {target}\n")
        s, r = evaluate(target)
        print_report(s, r)
    else:
        print(f"Directory not found: {target}")
    sys.exit(0)
