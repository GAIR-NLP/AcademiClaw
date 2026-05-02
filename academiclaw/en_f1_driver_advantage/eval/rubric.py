"""
F1 Driver Stable Advantage Index Analysis — Scoring Script (rubric.py)

Scoring is based solely on submitted result files (numerical values, structure,
consistency, verifiable prediction performance); no specific model type is
required or checked.

Total: 100 points
  A. Output Completeness & Basic Consistency (15 points)
     A1 Completeness (8 points): 6 files present, column names valid, parseable
     A2 Logical Consistency (7 points): interval ordering, teammate diff consistency, reasonable magnitude
  B. Generalization Prediction Performance (35 points)
     B1 MAE (25 points): test set prediction MAE, lower is better
     B2 Robustness (10 points): fold MAE standard deviation, more stable is better
  C. Uncertainty Interval Quality (25 points)
     C1 Coverage (15 points): proportion of true values falling within prediction interval, close to declared interval_level
     C2 Sharpness (10 points): given adequate coverage, narrower interval width is better
  D. Environment Stripping Effectiveness (20 points)
     D1 Cross-Circuit Consistency (10 points): StableAdv should not correlate strongly with circuit fixed features
     D2 Within-Team Separability & Stability (10 points): differences reasonable, not extreme
  E. Anti-Gaming & Evidence Coverage (5 points)
     E1 Anomaly Exclusion Reasonableness (2.5 points): anomalies proportion not too high
     E2 Fold Coverage Sufficiency (2.5 points): generalization evaluation covers enough circuits/sessions
"""

import csv
import json
import math
import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

try:
    import numpy as np

    _HAS_NUMPY = True
except ImportError:
    np = None  # type: ignore[assignment]
    _HAS_NUMPY = False

try:
    import openai
except ImportError:
    openai = None  # type: ignore[assignment]


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

def _clip01(x: float) -> float:
    """Clamp *x* to [0, 1]."""
    return max(0.0, min(1.0, float(x)))


def _to_float(val: Any) -> float:
    """Best-effort conversion to float; returns NaN on failure."""
    if val is None:
        return float("nan")
    try:
        return float(val)
    except (TypeError, ValueError):
        return float("nan")


def _isfinite(x: float) -> bool:
    return not (math.isnan(x) or math.isinf(x))


def _median(values: List[float]) -> float:
    if not values:
        return float("inf")
    s = sorted(values)
    n = len(s)
    if n % 2 == 1:
        return s[n // 2]
    return (s[n // 2 - 1] + s[n // 2]) / 2.0


def _std_pop(values: List[float]) -> float:
    """Population standard deviation."""
    if len(values) < 2:
        return float("inf")
    m = sum(values) / len(values)
    return (sum((v - m) ** 2 for v in values) / len(values)) ** 0.5


def _pearson_corr(xs: List[float], ys: List[float]) -> Optional[float]:
    """Pearson r between two equal-length lists; None if degenerate."""
    if len(xs) != len(ys) or len(xs) < 5:
        return None
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = sum((x - mx) ** 2 for x in xs) ** 0.5
    dy = sum((y - my) ** 2 for y in ys) ** 0.5
    if dx < 1e-12 or dy < 1e-12:
        return None
    r = num / (dx * dy)
    return r if _isfinite(r) else None


# ---------------------------------------------------------------------------
# CSV / JSON I/O (stdlib only — no pandas required)
# ---------------------------------------------------------------------------

def _read_csv(path: str) -> List[Dict[str, str]]:
    """Read a CSV into a list of row-dicts. Returns [] on any failure."""
    if not os.path.isfile(path):
        return []
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            reader = csv.DictReader(fh)
            return list(reader)
    except Exception:
        return []


def _count_csv_rows(path: str) -> int:
    """Count data rows (excluding header) in a CSV."""
    if not os.path.isfile(path):
        return 0
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return max(0, sum(1 for _ in fh) - 1)
    except Exception:
        return 0


def _read_json_file(path: str) -> Any:
    if not os.path.isfile(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return None


def _missing_columns(rows: List[Dict], required: List[str]) -> List[str]:
    """Return which *required* columns are absent from the first row."""
    if not rows:
        return required[:]
    present = set(rows[0].keys())
    return [c for c in required if c not in present]


# ---------------------------------------------------------------------------
# Load lap_level_predictions (CSV or Parquet)
# ---------------------------------------------------------------------------

def _load_lap_predictions(answer_dir: str) -> List[Dict[str, str]]:
    """Try parquet first, then CSV."""
    parquet_path = os.path.join(answer_dir, "lap_level_predictions.parquet")
    csv_path = os.path.join(answer_dir, "lap_level_predictions.csv")
    if os.path.isfile(parquet_path):
        try:
            import pandas as pd  # only needed here
            df = pd.read_parquet(parquet_path)
            # Convert everything to str for uniform handling
            records: List[Dict[str, str]] = []
            for _, row in df.iterrows():
                records.append({str(k): str(v) for k, v in row.items()})
            return records
        except Exception:
            pass
    return _read_csv(csv_path)


# ---------------------------------------------------------------------------
# Dataset helpers — locate f1_2023_data for cross-checks
# ---------------------------------------------------------------------------

def _find_data_dir() -> str:
    """Locate the f1_2023_data directory shipped with the query."""
    base = os.path.dirname(os.path.abspath(__file__))
    for rel in [
        os.path.join(base, "..", "workspace", "f1_2023_data"),
        os.path.join(base, "..", "f1_2023_data"),
    ]:
        abspath = os.path.abspath(rel)
        if os.path.isdir(abspath):
            return abspath
    return ""


def _total_dataset_laps(data_dir: str) -> int:
    """Count total data rows across all laps.csv in the dataset."""
    if not data_dir:
        return 0
    total = 0
    for child in os.listdir(data_dir):
        cpath = os.path.join(data_dir, child)
        if not os.path.isdir(cpath) or not child.startswith("Round_"):
            continue
        for sess in os.listdir(cpath):
            spath = os.path.join(cpath, sess)
            if not os.path.isdir(spath):
                continue
            laps_csv = os.path.join(spath, "laps.csv")
            if os.path.isfile(laps_csv):
                total += _count_csv_rows(laps_csv)
    return total


def _expected_folds(data_dir: str) -> Dict[str, List[str]]:
    """Return expected LOCO circuit_ids and LOSO session_types from the dataset."""
    circuits: set = set()
    session_types: set = set()
    if not data_dir:
        return {"LOCO": [], "LOSO": []}

    # Build round -> circuit_id map from schedule + circuits CSVs
    round_to_circuit: Dict[int, str] = {}
    schedule_path = os.path.join(data_dir, "schedule.csv")
    circuits_path = os.path.join(data_dir, "circuits.csv")
    if os.path.isfile(schedule_path) and os.path.isfile(circuits_path):
        try:
            sched_rows = _read_csv(schedule_path)
            circ_rows = _read_csv(circuits_path)
            country_to_cid: Dict[str, set] = {}
            for cr in circ_rows:
                cid = cr.get("CircuitId", "").strip()
                country = cr.get("Country", "").strip().lower()
                if cid and country:
                    country_to_cid.setdefault(country, set()).add(cid)
            for sr in sched_rows:
                rnd_str = sr.get("RoundNumber", "")
                country = sr.get("Country", "").strip().lower()
                if rnd_str and country:
                    cids = country_to_cid.get(country, set())
                    if len(cids) == 1:
                        round_to_circuit[int(rnd_str)] = list(cids)[0]
        except Exception:
            pass

    for child in sorted(os.listdir(data_dir)):
        cpath = os.path.join(data_dir, child)
        if not os.path.isdir(cpath) or not child.startswith("Round_"):
            continue
        m = re.match(r"Round_(\d+)_", child)
        rnd = int(m.group(1)) if m else None
        if rnd is not None and rnd in round_to_circuit:
            circuits.add(round_to_circuit[rnd])
        elif rnd is not None:
            # Fallback: use folder-name derived identifier
            circuits.add(re.sub(r"Round_\d+_", "", child))
        for sess in sorted(os.listdir(cpath)):
            spath = os.path.join(cpath, sess)
            if os.path.isdir(spath) and os.path.isfile(os.path.join(spath, "laps.csv")):
                session_types.add(sess)

    return {"LOCO": sorted(circuits), "LOSO": sorted(session_types)}


# ---------------------------------------------------------------------------
# Circuit features lookup for D1
# ---------------------------------------------------------------------------

def _load_circuit_features(data_dir: str) -> Dict[str, Dict[str, float]]:
    """Return {circuit_id: {length, turns}} from circuits.csv."""
    result: Dict[str, Dict[str, float]] = {}
    if not data_dir:
        return result
    path = os.path.join(data_dir, "circuits.csv")
    rows = _read_csv(path)
    for r in rows:
        cid = r.get("CircuitId", "").strip()
        length = _to_float(r.get("Length"))
        turns = _to_float(r.get("Turns"))
        if cid:
            result[cid] = {"length": length, "turns": turns}
    return result


# ============================================================================
# A — Output Validity & Consistency (15 pts)
# ============================================================================

_FILE_SPECS: Dict[str, List[str]] = {
    "stable_advantage.csv": [
        "driver_id", "StableAdv_mean_s_per_lap",
        "StableAdv_low_s_per_lap", "StableAdv_high_s_per_lap",
        "sample_laps_used",
    ],
    "teammate_comparison.csv": [
        "season", "team_id", "driver_id_a", "driver_id_b",
        "adv_diff_mean_s_per_lap", "adv_diff_low_s_per_lap",
        "adv_diff_high_s_per_lap", "laps_used_a", "laps_used_b",
    ],
    "generalization_report.csv": [
        "protocol", "fold_id", "n_laps_test", "error_mae_s",
    ],
    "anomalies.csv": [
        "season", "round", "session_type", "circuit_id",
        "driver_id", "lap_number", "reason",
    ],
    "manifest.json": [],
}

_PRED_REQUIRED_COLS = [
    "lap_time_s_true", "lap_time_s_pred_mean",
    "lap_time_s_pred_low", "lap_time_s_pred_high",
    "split_tag",
]


def _score_a(answer_dir: str) -> Tuple[float, Dict[str, Any]]:
    details: Dict[str, Any] = {}
    issues: List[str] = []

    # A1 — completeness (8 pts, proportional to files ok out of 6)
    files_ok = 0

    for fname, req_cols in _FILE_SPECS.items():
        fpath = os.path.join(answer_dir, fname)
        if not os.path.isfile(fpath):
            issues.append(f"Missing: {fname}")
            continue
        if fname.endswith(".json"):
            obj = _read_json_file(fpath)
            if obj is not None:
                files_ok += 1
            else:
                issues.append(f"Cannot parse JSON: {fname}")
        else:
            rows = _read_csv(fpath)
            if not rows:
                issues.append(f"Empty or unreadable: {fname}")
                continue
            missing = _missing_columns(rows, req_cols)
            if missing:
                issues.append(f"{fname} missing columns: {missing}")
            else:
                files_ok += 1

    # lap_level_predictions (parquet or csv)
    pred_rows = _load_lap_predictions(answer_dir)
    if pred_rows:
        missing_pred = _missing_columns(pred_rows, _PRED_REQUIRED_COLS)
        if missing_pred:
            issues.append(f"lap_level_predictions missing columns: {missing_pred}")
        else:
            files_ok += 1
    else:
        issues.append("Missing or empty: lap_level_predictions (.csv or .parquet)")

    a1 = 8.0 * (files_ok / 6.0)

    details["a1_files_ok"] = f"{files_ok}/6"
    details["a1_issues"] = issues if issues else "none"
    details["a1_score"] = round(a1, 2)

    # A2 — logical consistency (7 pts)
    sa_rows = _read_csv(os.path.join(answer_dir, "stable_advantage.csv"))
    tc_rows = _read_csv(os.path.join(answer_dir, "teammate_comparison.csv"))

    # (a) Interval ordering: low <= mean <= high
    interval_ok = 0
    interval_total = 0
    for r in sa_rows:
        lo = _to_float(r.get("StableAdv_low_s_per_lap"))
        mu = _to_float(r.get("StableAdv_mean_s_per_lap"))
        hi = _to_float(r.get("StableAdv_high_s_per_lap"))
        if _isfinite(lo) and _isfinite(mu) and _isfinite(hi):
            interval_total += 1
            if lo <= mu + 1e-9 and mu <= hi + 1e-9:
                interval_ok += 1
    frac_interval = interval_ok / interval_total if interval_total else 0.0

    # (b) Teammate diff consistency: adv_diff ~ SA(a) - SA(b)
    sa_map: Dict[str, float] = {}
    for r in sa_rows:
        did = r.get("driver_id", "").strip()
        val = _to_float(r.get("StableAdv_mean_s_per_lap"))
        if did and _isfinite(val):
            sa_map[did] = val

    diff_match = 0
    diff_total = 0
    for r in tc_rows:
        da = r.get("driver_id_a", "").strip()
        db = r.get("driver_id_b", "").strip()
        got = _to_float(r.get("adv_diff_mean_s_per_lap"))
        if da in sa_map and db in sa_map and _isfinite(got):
            diff_total += 1
            expected = sa_map[da] - sa_map[db]
            if abs(expected - got) < 0.01:
                diff_match += 1
    frac_team = diff_match / diff_total if diff_total else 0.0

    # (c) Magnitude sanity: |StableAdv_mean| should be < 30 s/lap
    mag_ok = 0
    mag_total = 0
    for r in sa_rows:
        val = _to_float(r.get("StableAdv_mean_s_per_lap"))
        if _isfinite(val):
            mag_total += 1
            if abs(val) < 30.0:
                mag_ok += 1
    frac_mag = mag_ok / mag_total if mag_total else 0.0

    a2 = 7.0 * (0.4 * frac_interval + 0.4 * frac_team + 0.2 * frac_mag)

    details["a2_interval_order"] = f"{interval_ok}/{interval_total}"
    details["a2_diff_consistency"] = f"{diff_match}/{diff_total}"
    details["a2_magnitude_ok"] = f"{mag_ok}/{mag_total}"
    details["a2_score"] = round(a2, 2)

    total = round(a1 + a2, 2)
    details["total"] = total
    return total, details


# ============================================================================
# B — Generalization Prediction Performance (35 pts)
# ============================================================================

def _extract_test_preds(answer_dir: str) -> Tuple[List[Dict], str]:
    """Return (test_pred_rows, note). note is non-empty if fallback used."""
    all_rows = _load_lap_predictions(answer_dir)
    if not all_rows:
        return [], "lap_level_predictions not found or empty"
    test_rows = [
        r for r in all_rows
        if str(r.get("split_tag", "")).strip().lower() == "test"
    ]
    if test_rows:
        return test_rows, ""
    return all_rows, "No split_tag='test' rows; using all rows as fallback"


def _score_b(answer_dir: str) -> Tuple[float, Dict[str, Any]]:
    details: Dict[str, Any] = {}

    test_preds, note = _extract_test_preds(answer_dir)
    if note:
        details["note"] = note
    if not test_preds:
        details["error"] = "No prediction data available"
        details["total"] = 0.0
        return 0.0, details

    # Absolute errors
    abs_errors: List[float] = []
    for r in test_preds:
        yt = _to_float(r.get("lap_time_s_true"))
        yp = _to_float(r.get("lap_time_s_pred_mean"))
        if _isfinite(yt) and _isfinite(yp):
            abs_errors.append(abs(yt - yp))

    if not abs_errors:
        details["error"] = "No valid true/pred pairs"
        details["total"] = 0.0
        return 0.0, details

    mae = sum(abs_errors) / len(abs_errors)
    # B1: MAE<=0.5 -> 25 pts; MAE>=4.0 -> 0 pts (linear)
    b1 = 25.0 * _clip01((4.0 - mae) / (4.0 - 0.5))

    # B2: fold MAE stability
    folds: Dict[str, List[float]] = {}
    for r in test_preds:
        fid = str(r.get("fold_id", "unknown"))
        yt = _to_float(r.get("lap_time_s_true"))
        yp = _to_float(r.get("lap_time_s_pred_mean"))
        if _isfinite(yt) and _isfinite(yp):
            folds.setdefault(fid, []).append(abs(yt - yp))

    fold_maes = [sum(errs) / len(errs) for errs in folds.values() if errs]
    if len(fold_maes) >= 2:
        mae_std = _std_pop(fold_maes)
        # std<=0.2 -> 10 pts; std>=1.5 -> 0 pts
        b2 = 10.0 * _clip01((1.5 - mae_std) / (1.5 - 0.2))
        details["fold_mae_std"] = round(mae_std, 4)
        details["n_folds"] = len(fold_maes)
    else:
        b2 = 0.0
        details["fold_mae_std"] = "N/A (fewer than 2 folds)"

    details["mae"] = round(mae, 4)
    details["n_test_samples"] = len(abs_errors)
    details["b1_score"] = round(b1, 2)
    details["b2_score"] = round(b2, 2)
    total = round(b1 + b2, 2)
    details["total"] = total
    return total, details


# ============================================================================
# C — Uncertainty Quality (25 pts)
# ============================================================================

def _score_c(answer_dir: str) -> Tuple[float, Dict[str, Any]]:
    details: Dict[str, Any] = {}

    manifest = _read_json_file(os.path.join(answer_dir, "manifest.json"))
    interval_level = 0.95
    if isinstance(manifest, dict):
        il = _to_float(manifest.get("interval_level", 0.95))
        if _isfinite(il) and 0.0 < il < 1.0:
            interval_level = il
    details["declared_interval_level"] = interval_level

    test_preds, note = _extract_test_preds(answer_dir)
    if note:
        details["note"] = note
    if not test_preds:
        details["error"] = "No prediction data"
        details["total"] = 0.0
        return 0.0, details

    covered = 0
    widths: List[float] = []
    valid = 0
    for r in test_preds:
        yt = _to_float(r.get("lap_time_s_true"))
        lo = _to_float(r.get("lap_time_s_pred_low"))
        hi = _to_float(r.get("lap_time_s_pred_high"))
        if not (_isfinite(yt) and _isfinite(lo) and _isfinite(hi)):
            continue
        valid += 1
        if lo <= yt <= hi:
            covered += 1
        widths.append(hi - lo)

    if valid == 0:
        details["error"] = "No valid prediction intervals"
        details["total"] = 0.0
        return 0.0, details

    coverage = covered / valid
    # C1: coverage deviation from declared level -> up to 15 pts
    # 0 deviation -> 15; >=0.10 deviation -> 0
    c1 = 15.0 * _clip01(1.0 - abs(coverage - interval_level) / 0.10)

    med_width = _median(widths)

    # C2: sharpness (only if coverage is adequate, i.e. >= target - 0.03)
    if coverage >= interval_level - 0.03:
        # med_width <= 1.5 -> 10; >= 6.0 -> 0
        c2 = 10.0 * _clip01((6.0 - med_width) / (6.0 - 1.5))
    else:
        c2 = 0.0

    details["coverage"] = round(coverage, 4)
    details["median_interval_width_s"] = (
        round(med_width, 4) if _isfinite(med_width) else "inf"
    )
    details["n_valid_intervals"] = valid
    details["c1_score"] = round(c1, 2)
    details["c2_score"] = round(c2, 2)
    total = round(c1 + c2, 2)
    details["total"] = total
    return total, details


# ============================================================================
# D — Environment-Adjusted Signal (20 pts)
# ============================================================================

def _score_d(answer_dir: str) -> Tuple[float, Dict[str, Any]]:
    details: Dict[str, Any] = {}

    data_dir = _find_data_dir()
    sa_rows = _read_csv(os.path.join(answer_dir, "stable_advantage.csv"))
    tc_rows = _read_csv(os.path.join(answer_dir, "teammate_comparison.csv"))

    # --- D1 (10 pts): StableAdv not overly correlated with track features ---
    d1 = 5.0  # conservative default when we can't compute
    if data_dir and sa_rows:
        circ_feats = _load_circuit_features(data_dir)
        pred_rows = _load_lap_predictions(answer_dir)
        if circ_feats and pred_rows:
            # Compute mean track features per driver
            driver_lens: Dict[str, List[float]] = {}
            driver_turns: Dict[str, List[float]] = {}
            for r in pred_rows:
                did = str(r.get("driver_id", "")).strip()
                cid = str(r.get("circuit_id", "")).strip()
                if did and cid in circ_feats:
                    feat = circ_feats[cid]
                    if _isfinite(feat["length"]):
                        driver_lens.setdefault(did, []).append(feat["length"])
                    if _isfinite(feat["turns"]):
                        driver_turns.setdefault(did, []).append(feat["turns"])

            # Build SA map
            sa_map: Dict[str, float] = {}
            for r in sa_rows:
                did = r.get("driver_id", "").strip()
                val = _to_float(r.get("StableAdv_mean_s_per_lap"))
                if did and _isfinite(val):
                    sa_map[did] = val

            common_drivers = [
                d for d in sa_map
                if d in driver_lens and d in driver_turns
            ]
            if len(common_drivers) >= 5:
                adv = [sa_map[d] for d in common_drivers]
                avg_l = [sum(driver_lens[d]) / len(driver_lens[d]) for d in common_drivers]
                avg_t = [sum(driver_turns[d]) / len(driver_turns[d]) for d in common_drivers]

                abs_corrs: List[float] = []
                for feat_vals in [avg_l, avg_t]:
                    r = _pearson_corr(adv, feat_vals)
                    if r is not None:
                        abs_corrs.append(abs(r))
                if abs_corrs:
                    max_corr = max(abs_corrs)
                    # |corr| <= 0 -> 10; |corr| >= 0.6 -> 0
                    d1 = 10.0 * _clip01((0.6 - max_corr) / 0.6)
                    details["d1_max_abs_corr"] = round(max_corr, 4)
    else:
        details["d1_note"] = "Cannot compute (missing data or stable_advantage)"

    details["d1_score"] = round(d1, 2)

    # --- D2 (10 pts): teammate diffs reasonable and balanced ---
    d2 = 0.0
    if tc_rows:
        abs_diffs: List[float] = []
        sig_count = 0
        valid_count = 0
        for r in tc_rows:
            dm = _to_float(r.get("adv_diff_mean_s_per_lap"))
            dl = _to_float(r.get("adv_diff_low_s_per_lap"))
            dh = _to_float(r.get("adv_diff_high_s_per_lap"))
            if not _isfinite(dm):
                continue
            valid_count += 1
            abs_diffs.append(abs(dm))
            if _isfinite(dl) and _isfinite(dh):
                if dl > 0 or dh < 0:
                    sig_count += 1

        if valid_count > 0:
            reasonable = sum(1 for d in abs_diffs if d <= 2.5) / valid_count
            sig_rate = sig_count / valid_count
            # Ideal sig_rate ~ 0.5 (not all significant, not none)
            sig_balance = 1.0 - abs(sig_rate - 0.5) / 0.5
            d2 = 10.0 * (0.5 * reasonable + 0.5 * _clip01(sig_balance))
            details["d2_reasonable_ratio"] = round(reasonable, 4)
            details["d2_sig_rate"] = round(sig_rate, 4)
        else:
            details["d2_note"] = "No valid teammate comparison rows"
    else:
        details["d2_note"] = "teammate_comparison.csv not found or empty"

    details["d2_score"] = round(d2, 2)
    total = round(d1 + d2, 2)
    details["total"] = total
    return total, details


# ============================================================================
# E — Anti-Gaming & Evidence Coverage (5 pts)
# ============================================================================

def _score_e(answer_dir: str) -> Tuple[float, Dict[str, Any]]:
    details: Dict[str, Any] = {}

    data_dir = _find_data_dir()

    # E1 (2.5 pts): anomalies ratio
    anom_rows = _read_csv(os.path.join(answer_dir, "anomalies.csv"))
    total_laps = _total_dataset_laps(data_dir)

    if anom_rows and total_laps > 0:
        anom_ratio = len(anom_rows) / total_laps
        # ratio <= 0.05 -> full; >= 0.25 -> 0
        e1 = 2.5 * _clip01((0.25 - anom_ratio) / (0.25 - 0.05))
        details["anomaly_count"] = len(anom_rows)
        details["total_dataset_laps"] = total_laps
        details["anomaly_ratio"] = round(anom_ratio, 4)
    elif not anom_rows:
        e1 = 0.0
        details["e1_note"] = "anomalies.csv missing or empty"
    else:
        e1 = 1.0
        details["e1_note"] = "Cannot determine total dataset lap count"

    details["e1_score"] = round(e1, 2)

    # E2 (2.5 pts): fold coverage in generalization_report
    gen_rows = _read_csv(os.path.join(answer_dir, "generalization_report.csv"))
    if gen_rows and data_dir:
        exp = _expected_folds(data_dir)
        protocols_present: set = set()
        folds_by_prot: Dict[str, set] = {}
        for r in gen_rows:
            prot = str(r.get("protocol", "")).strip().upper()
            fid = str(r.get("fold_id", "")).strip()
            protocols_present.add(prot)
            folds_by_prot.setdefault(prot, set()).add(fid)

        cover_scores: List[float] = []
        for prot in ["LOCO", "LOSO"]:
            if prot not in protocols_present:
                continue
            expected_folds_list = exp.get(prot, [])
            got_folds = folds_by_prot.get(prot, set())
            if expected_folds_list:
                ratio = len(got_folds) / (0.8 * len(expected_folds_list))
                cover_scores.append(_clip01(ratio))

        e2 = 2.5 * (max(cover_scores) if cover_scores else 0.0)
        details["protocols_found"] = sorted(protocols_present)
        details["folds_by_protocol"] = {
            k: len(v) for k, v in folds_by_prot.items()
        }
    elif gen_rows:
        e2 = 1.0
        details["e2_note"] = "Cannot verify fold coverage (data_dir not found)"
    else:
        e2 = 0.0
        details["e2_note"] = "generalization_report.csv missing or empty"

    details["e2_score"] = round(e2, 2)
    total = round(e1 + e2, 2)
    details["total"] = total
    return total, details


# ============================================================================
# Public API
# ============================================================================

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Evaluate agent output for the F1 Stable Advantage Index task.

    Args:
        answer_dir: absolute path to the agent output directory
                    (e.g. /path/to/query/gpt-5/attempt_1)

    Returns:
        (score, report)
        - score: 0-100 integer
        - report: dict with detailed breakdown
    """
    answer_dir = os.path.abspath(answer_dir)
    if not os.path.isdir(answer_dir):
        return 0, {"error": f"Directory not found: {answer_dir}"}

    sa, ra = _score_a(answer_dir)
    sb, rb = _score_b(answer_dir)
    sc, rc = _score_c(answer_dir)
    sd, rd = _score_d(answer_dir)
    se, re_ = _score_e(answer_dir)

    raw_total = sa + sb + sc + sd + se
    total = int(max(0, min(100, round(raw_total))))

    report: Dict[str, Any] = {
        "total_score": total,
        "dimensions": {
            "A_output_validity_consistency": {
                "score": round(sa, 2), "max": 15, "details": ra,
            },
            "B_generalization_performance": {
                "score": round(sb, 2), "max": 35, "details": rb,
            },
            "C_uncertainty_quality": {
                "score": round(sc, 2), "max": 25, "details": rc,
            },
            "D_environment_adjusted_signal": {
                "score": round(sd, 2), "max": 20, "details": rd,
            },
            "E_anti_gaming_evidence": {
                "score": round(se, 2), "max": 5, "details": re_,
            },
        },
    }
    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print a human-readable evaluation report."""
    print("=" * 70)
    print("F1 Driver Stable Advantage Index Analysis — Evaluation Report")
    print("=" * 70)
    print(f"\nTotal Score: {score}/100\n")

    dims = report.get("dimensions", {})

    # Summary table
    _DIM_LABELS = {
        "A_output_validity_consistency": "A. Output Completeness & Consistency",
        "B_generalization_performance": "B. Generalization Prediction Performance",
        "C_uncertainty_quality": "C. Uncertainty Interval Quality",
        "D_environment_adjusted_signal": "D. Environment Stripping Effectiveness",
        "E_anti_gaming_evidence": "E. Anti-Gaming & Evidence Coverage",
    }
    for key, dim in dims.items():
        label = _DIM_LABELS.get(key, key)
        s = dim.get("score", 0)
        m = dim.get("max", 0)
        print(f"  {label}: {s}/{m}")

    # Detailed breakdown
    print(f"\n{'─' * 50}")
    print("Detailed Scores:")
    print(f"{'─' * 50}\n")

    for key, dim in dims.items():
        label = _DIM_LABELS.get(key, key)
        print(f"[{label}] {dim.get('score', 0)}/{dim.get('max', 0)}")
        details = dim.get("details", {})
        for dk, dv in details.items():
            if dk == "total":
                continue
            if isinstance(dv, list):
                print(f"    {dk}: {', '.join(str(x) for x in dv)}")
            else:
                print(f"    {dk}: {dv}")
        print()

    # Grade comment
    if score >= 80:
        comment = "Excellent. Files complete, good prediction performance, reasonable intervals, effective environment stripping."
    elif score >= 60:
        comment = "Good. Task basically completed, with room for improvement in some dimensions."
    elif score >= 40:
        comment = "Passing. Core functionality implemented but significant deficiencies exist."
    elif score >= 20:
        comment = "Partially completed. Key files missing or prediction performance is poor."
    else:
        comment = "Failing. Submitted files severely lacking or data quality is extremely poor."
    print(f"Comment: {comment}")
    print("=" * 70)


# ============================================================================
# CLI entry point
# ============================================================================

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "gpt-5", "attempt_1",
    )
    target = os.path.abspath(target)
    if os.path.isdir(target):
        print(f"Evaluating directory: {target}\n")
        s, r = evaluate(target)
        print_report(s, r)
    else:
        print(f"Directory not found: {target}")
        sys.exit(0)
