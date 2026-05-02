"""
Isotropic Model Merging Algorithm Implementation — Scoring Script (rewritten from scratch)

Task: Implement iso_c_merging (Algorithm 1) and iso_cts_merging (Algorithm 2) from the paper
      "No Task Left Behind: Isotropic Model Merging"
      Save as merging_interface.py

Deliverable: merging_interface.py — containing iso_c_merging and iso_cts_merging functions

Total 100 points:
  A. File Delivery & Basic Compliance  (10 points)
  B. Dynamic Functional Tests (Core)   (60 points)  — Iso-C 30 + Iso-CTS 30
  C. Static Code Analysis (Fallback)   (30 points)  — Iso-C 15 + Iso-CTS 15

Notes:
  - Dynamic tests use deterministic dummy data, comparing agent code output with ground truth (torch.allclose, atol=1e-5)
  - If dynamic test passes, the corresponding static score is automatically full marks
  - If dynamic test fails, partial score is given through code pattern matching
"""

import os
import re
import sys
import importlib.util
from typing import Tuple, Dict, Any, Optional

# ---------------------------------------------------------------------------
# Attempt to import torch — core dependency for dynamic tests
# ---------------------------------------------------------------------------
try:
    import torch
    import torch.nn as nn
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False


# ===================================================================
# Ground-Truth Reference Implementation (embedded in rubric, not exposed)
# ===================================================================

def _gt_iso_c(ptm, fts, alpha=1.3):
    """Iso-C (Algorithm 1) reference answer"""
    merged = {}
    for key in ptm:
        w0 = ptm[key]
        if w0.dim() < 2:
            # 0D/1D: Task Arithmetic (Mean)
            task_vecs = torch.stack([ft[key] - w0 for ft in fts])
            merged[key] = w0 + alpha * torch.mean(task_vecs, dim=0)
        else:
            # 2D: SVD-based Iso-C
            task_vecs = [ft[key] - w0 for ft in fts]
            delta_ta = torch.sum(torch.stack(task_vecs), dim=0)
            U, S, Vh = torch.linalg.svd(delta_ta, full_matrices=False)
            sigma_bar = S.mean()
            merged[key] = w0 + alpha * sigma_bar * (U @ Vh)
    return merged


def _gt_iso_cts(ptm, fts, alpha=1.4, common_ratio=0.8):
    """Iso-CTS (Algorithm 2) reference answer"""
    merged = {}
    T = len(fts)
    for key in ptm:
        w0 = ptm[key]
        if w0.dim() < 2:
            task_vecs = torch.stack([ft[key] - w0 for ft in fts])
            merged[key] = w0 + alpha * torch.mean(task_vecs, dim=0)
            continue

        task_vecs = [ft[key] - w0 for ft in fts]
        delta_ta = torch.sum(torch.stack(task_vecs), dim=0)

        # Step 1: Common subspace
        U, S, Vh = torch.linalg.svd(delta_ta, full_matrices=False)
        r = S.shape[0]
        k_dim = int(r * common_ratio)
        s_dim = max(1, int((r - k_dim) / T))

        U_cm = U[:, :k_dim]
        S_cm = S[:k_dim]
        V_cm = Vh.T[:, :k_dim]

        all_U = [U_cm]
        all_S = [S_cm]
        all_V = [V_cm]

        # Step 2: Task-specific projection
        P_cm = U_cm @ U_cm.T
        for i in range(T):
            residual = task_vecs[i] - P_cm @ task_vecs[i]
            Ui, Si, Vhi = torch.linalg.svd(residual, full_matrices=False)
            all_U.append(Ui[:, :s_dim])
            all_S.append(Si[:s_dim])
            all_V.append(Vhi.T[:, :s_dim])

        # Step 3: Concatenate
        U_cat = torch.cat(all_U, dim=1)
        V_cat = torch.cat(all_V, dim=1)

        # Step 4: Whitening (orthogonalization)
        Pu, _, Qu = torch.linalg.svd(U_cat, full_matrices=False)
        U_final = Pu @ Qu
        Pv, _, Qv = torch.linalg.svd(V_cat, full_matrices=False)
        V_final = Pv @ Qv

        # Step 5: Isotropic factor
        sigma_bar = torch.mean(torch.cat(all_S))

        # Step 6: Reconstruct
        merged[key] = w0 + alpha * sigma_bar * (U_final @ V_final.T)
    return merged


# ===================================================================
# Deterministic Test Data Generation
# ===================================================================

if TORCH_AVAILABLE:
    class _TinyModel(nn.Module):
        """Tiny model containing 2D (Linear) and 1D (LayerNorm) parameters"""
        def __init__(self):
            super().__init__()
            self.fc1 = nn.Linear(10, 8)   # Weight [8,10], Bias [8]
            self.ln = nn.LayerNorm(8)      # Weight [8], Bias [8]
            self.fc2 = nn.Linear(8, 4)     # Weight [4,8], Bias [4]

    def _generate_test_data():
        """Generate deterministic dummy data (3 fine-tuned tasks)"""
        torch.manual_seed(42)
        ptm = _TinyModel().state_dict()
        fts = []
        for _ in range(3):
            ft = {k: v + torch.randn_like(v) * 0.1 for k, v in ptm.items()}
            fts.append(ft)
        return ptm, fts


# ===================================================================
# Helper Functions
# ===================================================================

def _find_code_file(answer_dir: str) -> str:
    """Find the agent's submitted code file, preferring merging_interface.py"""
    primary = os.path.join(answer_dir, "merging_interface.py")
    if os.path.isfile(primary):
        return primary
    # Fallback: search for other .py files in the directory
    skip = {"setup_dummy_data.py", "set_up_dummy_data.py", "eval.py", "test.py"}
    if os.path.isdir(answer_dir):
        for f in sorted(os.listdir(answer_dir)):
            if f.endswith(".py") and f not in skip:
                return os.path.join(answer_dir, f)
    return ""


def _read_code(answer_dir: str) -> str:
    """Read the agent's submitted code content"""
    path = _find_code_file(answer_dir)
    if not path:
        return ""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


def _load_module(file_path: str):
    """Dynamically load a .py file as a module, returns module on success, (None, error_msg) on failure"""
    try:
        spec = importlib.util.spec_from_file_location("agent_merging", file_path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules["agent_merging"] = mod
        spec.loader.exec_module(mod)
        return mod
    except Exception as e:
        return None, str(e)


# ===================================================================
# Dimension A: File Delivery & Basic Compliance (10 points)
# ===================================================================

def _eval_file_delivery(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    10 points:
      - 5 points: merging_interface.py exists (exact filename match 5 points, other .py file 2 points)
      - 3 points: Code is non-empty (>50 characters)
      - 2 points: Contains both target function names (iso_c_merging + iso_cts_merging)
    """
    score = 0
    details = {}
    code_path = _find_code_file(answer_dir)
    code = ""

    # (1) File exists (5 points)
    target = os.path.join(answer_dir, "merging_interface.py")
    if os.path.isfile(target):
        score += 5
        details["File exists"] = "5/5 — merging_interface.py exists"
    elif code_path:
        score += 2
        details["File exists"] = f"2/5 — Filename mismatch (actual: {os.path.basename(code_path)})"
    else:
        details["File exists"] = "0/5 — No .py file found"

    # (2) Code non-empty (3 points)
    if code_path:
        try:
            with open(code_path, "r", encoding="utf-8") as f:
                code = f.read()
            if len(code.strip()) > 50:
                score += 3
                details["Code non-empty"] = "3/3 — Content is non-empty"
            else:
                details["Code non-empty"] = "0/3 — File content too short (<=50 characters)"
        except Exception as e:
            details["Code non-empty"] = f"0/3 — Read failed: {e}"
    else:
        details["Code non-empty"] = "0/3 — No file"

    # (3) Function definitions (2 points)
    if code:
        has_c = "iso_c_merging" in code
        has_cts = "iso_cts_merging" in code
        if has_c and has_cts:
            score += 2
            details["Function definitions"] = "2/2 — Both iso_c_merging and iso_cts_merging present"
        elif has_c or has_cts:
            score += 1
            found = "iso_c_merging" if has_c else "iso_cts_merging"
            details["Function definitions"] = f"1/2 — Only found {found}"
        else:
            details["Function definitions"] = "0/2 — Target function names not found"
    else:
        details["Function definitions"] = "0/2 — No file"

    return min(score, 10), details


# ===================================================================
# Dimension B: Dynamic Functional Tests (60 points)
# ===================================================================

def _eval_dynamic(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    60 points: Iso-C 30 + Iso-CTS 30
    Uses deterministic dummy data, comparing agent output with ground truth
    """
    if not TORCH_AVAILABLE:
        return 0, {"error": "torch not installed, skipping dynamic tests"}

    code_path = _find_code_file(answer_dir)
    if not code_path:
        return 0, {"error": "No evaluable .py file found"}

    # Load module
    result = _load_module(code_path)
    if isinstance(result, tuple):
        return 0, {"error": f"Module loading failed: {result[1]}"}
    agent_mod = result

    ptm, fts = _generate_test_data()
    score = 0
    details = {}

    # --- Iso-C (30 points) ---
    if hasattr(agent_mod, "iso_c_merging"):
        try:
            user_out = agent_mod.iso_c_merging(ptm, fts, alpha=1.3)
            gt_out = _gt_iso_c(ptm, fts, alpha=1.3)

            if not isinstance(user_out, dict) or len(user_out) == 0:
                details["Iso-C"] = "0/30 — Return value is not a valid state_dict"
            else:
                all_match = True
                max_diff = 0.0
                for k in ptm:
                    if k not in user_out:
                        all_match = False
                        details["Iso-C"] = f"0/30 — Missing key: {k}"
                        break
                    diff = (user_out[k] - gt_out[k]).abs().max().item()
                    max_diff = max(max_diff, diff)
                    if not torch.allclose(user_out[k], gt_out[k], atol=1e-5):
                        all_match = False

                if all_match:
                    score += 30
                    details["Iso-C"] = f"30/30 — Passed (max_diff={max_diff:.2e})"
                elif "Iso-C" not in details:
                    details["Iso-C"] = f"0/30 — Output mismatch (max_diff={max_diff:.2e})"
        except Exception as e:
            details["Iso-C"] = f"0/30 — Runtime exception: {e}"
    else:
        details["Iso-C"] = "0/30 — Function iso_c_merging not defined"

    # --- Iso-CTS (30 points) ---
    if hasattr(agent_mod, "iso_cts_merging"):
        try:
            user_out = agent_mod.iso_cts_merging(ptm, fts, alpha=1.4, common_ratio=0.8)
            gt_out = _gt_iso_cts(ptm, fts, alpha=1.4, common_ratio=0.8)

            if not isinstance(user_out, dict) or len(user_out) == 0:
                details["Iso-CTS"] = "0/30 — Return value is not a valid state_dict"
            else:
                all_match = True
                max_diff = 0.0
                for k in ptm:
                    if k not in user_out:
                        all_match = False
                        details["Iso-CTS"] = f"0/30 — Missing key: {k}"
                        break
                    diff = (user_out[k] - gt_out[k]).abs().max().item()
                    max_diff = max(max_diff, diff)
                    if not torch.allclose(user_out[k], gt_out[k], atol=1e-5):
                        all_match = False

                if all_match:
                    score += 30
                    details["Iso-CTS"] = f"30/30 — Passed (max_diff={max_diff:.2e})"
                elif "Iso-CTS" not in details:
                    details["Iso-CTS"] = f"0/30 — Output mismatch (max_diff={max_diff:.2e})"
        except Exception as e:
            details["Iso-CTS"] = f"0/30 — Runtime exception: {e}"
    else:
        details["Iso-CTS"] = "0/30 — Function iso_cts_merging not defined"

    return score, details


# ===================================================================
# Dimension C: Static Code Analysis (30 points)
# ===================================================================

def _eval_static(
    code: str,
    iso_c_passed: bool,
    iso_cts_passed: bool,
) -> Tuple[int, Dict[str, Any]]:
    """
    30 points: Iso-C static 15 + Iso-CTS static 15
    If the corresponding dynamic test passed, the sub-item gets full marks automatically;
    otherwise partial score is given via code pattern matching
    """
    score = 0
    details = {}

    # ---------- Iso-C Static (15 points) ----------
    if iso_c_passed:
        score += 15
        details["Iso-C static"] = "15/15 — Dynamic test passed, automatic full marks"
    else:
        sub = 0
        reasons = []
        # (5 points) Uses SVD
        if "torch.linalg.svd" in code or "torch.svd" in code:
            sub += 5
            reasons.append("SVD call (+5)")
        # (5 points) Uses mean to compute isotropic factor
        if ".mean()" in code or "torch.mean" in code:
            sub += 5
            reasons.append("Mean computation (+5)")
        # (5 points) Dimension check — distinguishes 2D from 0D/1D
        dim_patterns = [r"\.dim\(\)", r"\.ndim", r"len\(.*\.shape\)"]
        if any(re.search(p, code) for p in dim_patterns):
            sub += 5
            reasons.append("Dimension check (+5)")
        score += sub
        details["Iso-C static"] = (
            f"{sub}/15 — {'; '.join(reasons)}" if reasons
            else "0/15 — No key algorithm patterns detected"
        )

    # ---------- Iso-CTS Static (15 points) ----------
    if iso_cts_passed:
        score += 15
        details["Iso-CTS static"] = "15/15 — Dynamic test passed, automatic full marks"
    else:
        sub = 0
        reasons = []
        # (5 points) Orthogonal projection — projection onto orthogonal complement of common subspace
        proj_patterns = [
            r"P_common\s*@",
            r"U_common\s*@\s*U_common",
            r"@\s*U_common\.T",
            r"@\s*U_common\.t\(\)",
            r"\-\s*.*@\s*.*@",           # residual = x - P @ x
            r"orthogonal",
        ]
        if any(re.search(p, code, re.IGNORECASE) for p in proj_patterns):
            sub += 5
            reasons.append("Orthogonal projection (+5)")
        # (5 points) Concatenation torch.cat
        if "torch.cat" in code:
            sub += 5
            reasons.append("Concatenation torch.cat (+5)")
        # (5 points) Secondary orthogonalization (Whitening) — at least 3 SVD calls
        svd_count = len(re.findall(r"(?:torch\.linalg\.)?svd\(", code))
        if svd_count >= 3:
            sub += 5
            reasons.append(f"Whitening (SVD x{svd_count}) (+5)")
        score += sub
        details["Iso-CTS static"] = (
            f"{sub}/15 — {'; '.join(reasons)}" if reasons
            else "0/15 — No key algorithm patterns detected"
        )

    return score, details


# ===================================================================
# Main Evaluation Entry Point
# ===================================================================

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Evaluate agent's merging_interface.py implementation.

    Args:
        answer_dir: Absolute path to the agent output directory

    Returns:
        (score, report)
        - score: Integer 0-100
        - report: dict containing detailed evaluation report
    """
    report: Dict[str, Any] = {}

    # A. File Delivery (10 points)
    a_score, a_details = _eval_file_delivery(answer_dir)
    report["A. File Delivery (10pts)"] = {"score": a_score, "details": a_details}

    # Read code (for static analysis)
    code = _read_code(answer_dir)

    # B. Dynamic Functional Tests (60 points)
    b_score, b_details = _eval_dynamic(answer_dir)
    report["B. Dynamic Functional Tests (60pts)"] = {"score": b_score, "details": b_details}

    iso_c_passed = "30/30" in b_details.get("Iso-C", "")
    iso_cts_passed = "30/30" in b_details.get("Iso-CTS", "")

    # C. Static Code Analysis (30 points)
    c_score, c_details = _eval_static(code, iso_c_passed, iso_cts_passed)
    report["C. Static Code Analysis (30pts)"] = {"score": c_score, "details": c_details}

    total = a_score + b_score + c_score
    report["total_score"] = total
    report["dimension_scores"] = {
        "File Delivery": f"{a_score}/10",
        "Dynamic Tests": f"{b_score}/60",
        "Static Analysis": f"{c_score}/30",
    }

    return total, report


# ===================================================================
# Report Printing
# ===================================================================

def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print formatted evaluation report"""
    print("=" * 65)
    print(f"  Isotropic Model Merging Evaluation Report  |  Total: {score}/100")
    print("=" * 65)

    summary = report.get("dimension_scores", {})
    for k, v in summary.items():
        print(f"  {k}: {v}")
    print("-" * 65)

    for section in [
        "A. File Delivery (10pts)",
        "B. Dynamic Functional Tests (60pts)",
        "C. Static Code Analysis (30pts)",
    ]:
        sec = report.get(section, {})
        sec_score = sec.get("score", 0)
        print(f"\n[{section}]  Score: {sec_score}")
        for k, v in sec.get("details", {}).items():
            print(f"    {k}: {v}")

    print("\n" + "=" * 65)


# ===================================================================
# Command Line Entry
# ===================================================================

if __name__ == "__main__":
    test_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(__file__), "..", "gpt-5", "attempt_1",
    )
    test_dir = os.path.abspath(test_dir)
    if os.path.exists(test_dir):
        print(f"Evaluating directory: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"Directory does not exist: {test_dir}")
    sys.exit(0)
