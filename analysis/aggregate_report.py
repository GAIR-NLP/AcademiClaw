#!/usr/bin/env python3
"""
AcademiClaw — cross-model aggregate report.

Reads every `academiclaw/<task_id>/<agent>/<model>/meta_eval.json`, then
produces a Markdown report mirroring the appendix of the paper:

    A. Efficiency metrics (per model, aggregated across tasks)
    B. Tool usage patterns
    C. Safety analysis (overall + S1–S5 category breakdown)
    D. Efficiency-quality tradeoffs
    E. Timeout analysis
    F. Cross-model behavioral differences
    G. Per-task efficiency variation
    H. Key findings / summary table

Pricing is optional; pass `--pricing analysis/pricing.example.json` to turn
on $-per-task and score-per-dollar columns. Without pricing, cost sections
are skipped.

Usage:
    python3 analysis/aggregate_report.py
    python3 analysis/aggregate_report.py --base-dir academiclaw \
        --output reports/aggregate_report.md \
        --pricing analysis/pricing.example.json

Dependencies: numpy (standard dep). scipy is used if present but not required.
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import statistics
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

try:  # scipy gives us exact two-sided p-values but we can live without it
    from scipy import stats as sp_stats  # type: ignore
    _HAS_SCIPY = True
except ImportError:
    _HAS_SCIPY = False


# ── Pearson correlation ───────────────────────────────────────────────────
def _pearsonr_pure(x: np.ndarray, y: np.ndarray) -> Tuple[float, float]:
    """Pearson r and two-sided p-value (t-distribution approximation)."""
    n = len(x)
    if n < 3:
        return float("nan"), float("nan")
    xm, ym = x.mean(), y.mean()
    num = ((x - xm) * (y - ym)).sum()
    den = np.sqrt(((x - xm) ** 2).sum() * ((y - ym) ** 2).sum())
    if den == 0:
        return float("nan"), float("nan")
    r = float(num / den)
    # two-sided t-test on r
    t = r * np.sqrt((n - 2) / max(1e-12, 1 - r * r))
    # Survival fn for Student-t via numerical approximation
    # Fall back to large-n normal approximation (OK for n ≥ 30)
    try:
        from math import erf, sqrt as msqrt
        z = abs(t) / msqrt(2)
        p = 1.0 - erf(z)
    except Exception:
        p = float("nan")
    return r, float(p)


def pearsonr_safe(x_list, y_list) -> Tuple[float, float]:
    x = np.asarray(x_list, dtype=float)
    y = np.asarray(y_list, dtype=float)
    mask = np.isfinite(x) & np.isfinite(y)
    x, y = x[mask], y[mask]
    if len(x) < 3:
        return float("nan"), float("nan")
    if _HAS_SCIPY:
        r, p = sp_stats.pearsonr(x, y)
        return float(r), float(p)
    return _pearsonr_pure(x, y)


# ── Data loading ──────────────────────────────────────────────────────────
def extract_dir_model(filepath: str) -> Tuple[str, str]:
    """Return (agent, model) extracted from .../<agent>/<model>/meta_eval.json."""
    parts = filepath.split(os.sep)
    for i, p in enumerate(parts):
        if p in ("openclaw", "claude-code") and i + 1 < len(parts):
            return p, parts[i + 1]
    # fallback
    return "unknown", parts[-2] if len(parts) >= 2 else "unknown"


def load_all_data(base_dir: Path, allowed_models: Optional[List[str]]) -> List[Dict]:
    """Load every meta_eval.json found under base_dir."""
    patterns = [
        str(base_dir / "*" / "openclaw" / "*" / "meta_eval.json"),
        str(base_dir / "*" / "claude-code" / "*" / "meta_eval.json"),
    ]
    files = set()
    for pat in patterns:
        files.update(glob.glob(pat))

    records: List[Dict] = []
    skipped = 0
    for fp in sorted(files):
        try:
            with open(fp, encoding="utf-8") as f:
                d = json.load(f)
        except Exception as exc:
            print(f"  [WARN] {fp}: {exc}", file=sys.stderr)
            continue

        agent, model = extract_dir_model(fp)
        if allowed_models and model not in allowed_models:
            skipped += 1
            continue

        # Task id is <base_dir>/<task_id>/<agent>/<model>/meta_eval.json
        try:
            task_id = Path(fp).relative_to(base_dir).parts[0]
        except ValueError:
            task_id = Path(fp).parent.parent.parent.name

        d["_filepath"] = fp
        d["model_name"] = model
        d["agent"] = agent
        d["task_id"] = task_id
        records.append(d)

    print(f"Loaded {len(records)} records"
          + (f" (skipped {skipped} not in --models list)" if allowed_models else ""))
    return records


def group_by_model(records: List[Dict]) -> Dict[str, List[Dict]]:
    g: Dict[str, List[Dict]] = defaultdict(list)
    for r in records:
        g[r["model_name"]].append(r)
    return g


def group_by_task(records: List[Dict]) -> Dict[str, List[Dict]]:
    g: Dict[str, List[Dict]] = defaultdict(list)
    for r in records:
        g[r["task_id"]].append(r)
    return g


# ── Helpers ───────────────────────────────────────────────────────────────
def safe_mean(lst):
    lst = [x for x in lst if x is not None]
    return statistics.mean(lst) if lst else 0.0


def safe_median(lst):
    lst = [x for x in lst if x is not None]
    return statistics.median(lst) if lst else 0.0


def safe_stdev(lst):
    lst = [x for x in lst if x is not None]
    return statistics.stdev(lst) if len(lst) > 1 else 0.0


def extract_metrics(record: Dict) -> Dict[str, Any]:
    agg = record.get("aggregate_metrics", {})
    dur = agg.get("total_duration_seconds", 0)
    tokens = agg.get("total_tokens", {})
    inp = tokens.get("input", 0)
    out = tokens.get("output", 0)
    cached = tokens.get("cached", 0)
    total = tokens.get("total", inp + out)
    tool_calls = agg.get("total_tool_calls", 0)
    tool_freq = agg.get("tool_frequency", {})

    api_calls = 0
    for att in record.get("attempts", []):
        m = att.get("metrics", {})
        api_calls += m.get("api_call_count", 0)

    return {
        "duration": dur,
        "input_tokens": inp,
        "output_tokens": out,
        "cached_tokens": cached,
        "total_tokens": total,
        "tool_calls": tool_calls,
        "api_calls": api_calls,
        "tool_freq": tool_freq,
        "score": record.get("best_score", 0),
        "timed_out": record.get("timed_out", False),
        "passed": record.get("passed", False),
    }


def estimate_cost(pricing: Dict[str, Dict[str, float]], model: str,
                  inp_tokens: int, out_tokens: int) -> float:
    p = pricing.get(model, {"input": 0, "output": 0})
    return (inp_tokens / 1e6) * p["input"] + (out_tokens / 1e6) * p["output"]


def short_name(model: str) -> str:
    """Deterministic, compact display name (first 16 chars)."""
    return model if len(model) <= 16 else model[:14] + ".."


# ── Report sections ───────────────────────────────────────────────────────
def section_efficiency(models: List[str], by_model: Dict, pricing: Dict, out: List[str]) -> Dict[str, float]:
    out.append("# A. Efficiency Metrics\n")

    has_pricing = bool(pricing)
    cost_col = "| Est. Cost ($) " if has_pricing else ""
    cost_sep = "|---------------" if has_pricing else ""
    out.append("| Model | Tasks | Mean Dur (s) | Med Dur (s) | Mean Tokens | Med Tokens | Mean ToolCalls | Mean APICalls | Timeout% " + cost_col + "|")
    out.append("|-------|-------|-------------|------------|-------------|------------|----------------|---------------|----------" + cost_sep + "|")

    model_costs: Dict[str, float] = {}
    for model in models:
        recs = by_model.get(model, [])
        if not recs:
            continue
        metrics = [extract_metrics(r) for r in recs]
        durs = [m["duration"] for m in metrics]
        toks = [m["total_tokens"] for m in metrics]
        tcs = [m["tool_calls"] for m in metrics]
        acs = [m["api_calls"] for m in metrics]
        tos = [m["timed_out"] for m in metrics]
        timeout_rate = 100.0 * sum(tos) / len(tos) if tos else 0

        row = (
            f"| {short_name(model)} | {len(recs)} "
            f"| {safe_mean(durs):.1f} | {safe_median(durs):.1f} "
            f"| {safe_mean(toks):,.0f} | {safe_median(toks):,.0f} "
            f"| {safe_mean(tcs):.1f} | {safe_mean(acs):.1f} "
            f"| {timeout_rate:.1f}% "
        )
        if has_pricing:
            total_cost = sum(estimate_cost(pricing, model, m["input_tokens"], m["output_tokens"]) for m in metrics)
            model_costs[model] = total_cost
            row += f"| {total_cost:.2f} "
        row += "|"
        out.append(row)
    out.append("")

    if has_pricing:
        out.append("### Estimated Cost Breakdown\n")
        out.append("| Model | Input Cost ($) | Output Cost ($) | Total Cost ($) | Cost/Task ($) |")
        out.append("|-------|---------------|-----------------|----------------|---------------|")
        for model in models:
            recs = by_model.get(model, [])
            if not recs or model not in pricing:
                continue
            metrics = [extract_metrics(r) for r in recs]
            p = pricing[model]
            total_inp = sum(m["input_tokens"] for m in metrics)
            total_out = sum(m["output_tokens"] for m in metrics)
            inp_cost = (total_inp / 1e6) * p["input"]
            out_cost = (total_out / 1e6) * p["output"]
            total_cost = inp_cost + out_cost
            out.append(
                f"| {short_name(model)} "
                f"| {inp_cost:.2f} | {out_cost:.2f} | {total_cost:.2f} "
                f"| {total_cost / len(recs):.2f} |"
            )
        out.append("")

    return model_costs


def section_tool_usage(models: List[str], by_model: Dict, out: List[str]) -> None:
    out.append("# B. Tool Usage Patterns\n")
    tool_names = ["read", "write", "edit", "exec", "process"]

    out.append("### Average Tool Frequency Per Task\n")
    out.append("| Model | read | write | edit | exec | process | Total |")
    out.append("|-------|------|-------|------|------|---------|-------|")

    model_tool_data: Dict[str, Dict[str, float]] = {}
    for model in models:
        recs = by_model.get(model, [])
        if not recs:
            continue
        freq_sums: Dict[str, float] = defaultdict(float)
        for r in recs:
            tf = r.get("aggregate_metrics", {}).get("tool_frequency", {})
            for t in tool_names:
                freq_sums[t] += tf.get(t, 0)
        n = len(recs)
        avgs = {t: freq_sums[t] / n for t in tool_names}
        total_avg = sum(avgs.values())
        model_tool_data[model] = avgs
        out.append(
            f"| {short_name(model)} "
            f"| {avgs['read']:.1f} | {avgs['write']:.1f} | {avgs['edit']:.1f} "
            f"| {avgs['exec']:.1f} | {avgs['process']:.1f} | {total_avg:.1f} |"
        )
    out.append("")

    out.append("### Tool Mix Ratios\n")
    out.append("| Model | exec/(read+write+edit) | write/edit | exec share (%) | read share (%) |")
    out.append("|-------|------------------------|------------|----------------|----------------|")
    for model in models:
        avgs = model_tool_data.get(model)
        if not avgs:
            continue
        rwe = avgs["read"] + avgs["write"] + avgs["edit"]
        debug_ratio = avgs["exec"] / rwe if rwe > 0 else float("inf")
        we_ratio = avgs["write"] / avgs["edit"] if avgs["edit"] > 0 else float("inf")
        total = sum(avgs.values())
        exec_share = 100 * avgs["exec"] / total if total > 0 else 0
        read_share = 100 * avgs["read"] / total if total > 0 else 0
        out.append(
            f"| {short_name(model)} "
            f"| {debug_ratio:.2f} | {we_ratio:.2f} "
            f"| {exec_share:.1f}% | {read_share:.1f}% |"
        )
    out.append("")


def section_safety(models: List[str], by_model: Dict, out: List[str]) -> None:
    out.append("# C. Safety Analysis\n")

    cats = ["S1_destructive_ops", "S2_info_leakage", "S3_boundary", "S4_privilege", "S5_network_supply"]

    out.append("### Mean Safety Scores (per S-category)\n")
    out.append("| Model | Overall | S1-Destr | S2-Leak | S3-Bound | S4-Priv | S5-Net |")
    out.append("|-------|---------|----------|---------|----------|---------|--------|")

    for model in models:
        recs = by_model.get(model, [])
        if not recs:
            continue
        overall_scores: List[float] = []
        cat_scores: Dict[str, List[float]] = defaultdict(list)
        for r in recs:
            ss = r.get("safety_scores", {}) or {}
            sv = ss.get("safety_score")
            if sv is not None:
                overall_scores.append(sv)
            categories = ss.get("categories", {}) or {}
            for c in cats:
                cs = (categories.get(c) or {}).get("score")
                if cs is not None:
                    cat_scores[c].append(cs)

        cat_avgs = {c: safe_mean(cat_scores[c]) for c in cats}
        out.append(
            f"| {short_name(model)} | {safe_mean(overall_scores):.1f} "
            f"| {cat_avgs[cats[0]]:.1f} | {cat_avgs[cats[1]]:.1f} | {cat_avgs[cats[2]]:.1f} "
            f"| {cat_avgs[cats[3]]:.1f} | {cat_avgs[cats[4]]:.1f} |"
        )
    out.append("")

    out.append("### Total Violation Counts by Severity\n")
    out.append("| Model | CRITICAL | HIGH | MEDIUM | LOW | Total |")
    out.append("|-------|----------|------|--------|-----|-------|")
    for model in models:
        recs = by_model.get(model, [])
        if not recs:
            continue
        vcounts: Dict[str, int] = defaultdict(int)
        for r in recs:
            vc = (r.get("safety_scores") or {}).get("violation_count", {}) or {}
            for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
                vcounts[sev] += vc.get(sev, 0)
        total_v = sum(vcounts.values())
        out.append(
            f"| {short_name(model)} "
            f"| {vcounts['CRITICAL']} | {vcounts['HIGH']} | {vcounts['MEDIUM']} | {vcounts['LOW']} "
            f"| {total_v} |"
        )
    out.append("")

    out.append("### Correlation: Safety Score vs Task Score (per model)\n")
    for model in models:
        recs = by_model.get(model, [])
        if not recs:
            continue
        scores: List[float] = []
        safety: List[float] = []
        for r in recs:
            sv = (r.get("safety_scores") or {}).get("safety_score")
            if sv is not None:
                scores.append(r.get("best_score", 0))
                safety.append(sv)
        r_val, p_val = pearsonr_safe(scores, safety)
        sig = "***" if p_val < 0.001 else "**" if p_val < 0.01 else "*" if p_val < 0.05 else "n.s."
        out.append(f"- **{short_name(model)}**: r = {r_val:.3f}, p = {p_val:.4f} ({sig})")
    out.append("")


def section_tradeoffs(models: List[str], by_model: Dict, model_costs: Dict[str, float],
                      pricing: Dict, out: List[str]) -> None:
    out.append("# D. Efficiency-Quality Tradeoffs\n")

    out.append("### Correlation: Tokens vs Score (per model)\n")
    out.append("| Model | r(tokens,score) | p | r(duration,score) | p | r(toolcalls,score) | p |")
    out.append("|-------|-----------------|---|-------------------|---|--------------------|---|")
    for model in models:
        recs = by_model.get(model, [])
        if not recs:
            continue
        metrics = [extract_metrics(r) for r in recs]
        scores = [m["score"] for m in metrics]
        r1, p1 = pearsonr_safe([m["total_tokens"] for m in metrics], scores)
        r2, p2 = pearsonr_safe([m["duration"] for m in metrics], scores)
        r3, p3 = pearsonr_safe([m["tool_calls"] for m in metrics], scores)
        out.append(
            f"| {short_name(model)} "
            f"| {r1:.3f} | {p1:.4f} "
            f"| {r2:.3f} | {p2:.4f} "
            f"| {r3:.3f} | {p3:.4f} |"
        )
    out.append("")

    # Pooled correlation
    all_toks, all_scores, all_durs, all_tcs = [], [], [], []
    for model in models:
        for r in by_model.get(model, []):
            m = extract_metrics(r)
            all_toks.append(m["total_tokens"])
            all_scores.append(m["score"])
            all_durs.append(m["duration"])
            all_tcs.append(m["tool_calls"])
    r1, p1 = pearsonr_safe(all_toks, all_scores)
    r2, p2 = pearsonr_safe(all_durs, all_scores)
    r3, p3 = pearsonr_safe(all_tcs, all_scores)
    out.append("### Overall Pooled Correlation\n")
    out.append(f"- Tokens vs Score: r = {r1:.3f}, p = {p1:.6f}")
    out.append(f"- Duration vs Score: r = {r2:.3f}, p = {p2:.6f}")
    out.append(f"- Tool Calls vs Score: r = {r3:.3f}, p = {p3:.6f}")
    out.append("")

    if pricing:
        out.append("### Score Efficiency (cost-weighted)\n")
        out.append("| Model | Mean Score | Total Tokens (M) | Total Cost ($) | Cost/Task ($) | Score/Dollar |")
        out.append("|-------|-----------|-------------------|----------------|---------------|-------------|")
        for model in models:
            recs = by_model.get(model, [])
            if not recs or model not in pricing:
                continue
            metrics = [extract_metrics(r) for r in recs]
            scores = [m["score"] for m in metrics]
            total_tok_m = sum(m["total_tokens"] for m in metrics) / 1e6
            mean_score = safe_mean(scores)
            tc = model_costs.get(model, 0)
            score_per_dollar = mean_score / (tc / len(recs)) if tc > 0 else 0
            out.append(
                f"| {short_name(model)} "
                f"| {mean_score:.1f} | {total_tok_m:.1f} "
                f"| {tc:.2f} | {tc / len(recs):.2f} | {score_per_dollar:.1f} |"
            )
        out.append("")


def section_timeout(models: List[str], by_model: Dict, by_task: Dict, out: List[str]) -> None:
    out.append("# E. Timeout Analysis\n")
    out.append("### Timeout Rate by Model\n")
    out.append("| Model | Tasks | Timed Out | Timeout % | Score (TO) | Score (OK) | Gap |")
    out.append("|-------|-------|-----------|-----------|-----------|-----------|-----|")
    for model in models:
        recs = by_model.get(model, [])
        if not recs:
            continue
        to_recs = [r for r in recs if r.get("timed_out", False)]
        comp_recs = [r for r in recs if not r.get("timed_out", False)]
        to_scores = [r.get("best_score", 0) for r in to_recs]
        comp_scores = [r.get("best_score", 0) for r in comp_recs]
        to_pct = 100 * len(to_recs) / len(recs)
        ms_to = safe_mean(to_scores) if to_scores else 0
        ms_comp = safe_mean(comp_scores) if comp_scores else 0
        gap = ms_comp - ms_to
        out.append(
            f"| {short_name(model)} | {len(recs)} | {len(to_recs)} "
            f"| {to_pct:.1f}% | {ms_to:.1f} | {ms_comp:.1f} | {gap:+.1f} |"
        )
    out.append("")

    out.append("### Tasks with Most Timeouts (Top 15)\n")
    task_timeouts: Dict[str, int] = defaultdict(int)
    task_total: Dict[str, int] = defaultdict(int)
    for model in models:
        for r in by_model.get(model, []):
            tid = r["task_id"]
            task_total[tid] += 1
            if r.get("timed_out", False):
                task_timeouts[tid] += 1
    sorted_tasks = sorted(task_timeouts.items(), key=lambda x: x[1], reverse=True)
    out.append("| Task | Timeouts / Models | Timeout % |")
    out.append("|------|-------------------|-----------|")
    for tid, count in sorted_tasks[:15]:
        pct = 100 * count / task_total[tid]
        out.append(f"| {tid} | {count}/{task_total[tid]} | {pct:.0f}% |")
    out.append("")


def section_cross_model(models: List[str], by_model: Dict, out: List[str]) -> None:
    out.append("# F. Cross-Model Behavioral Differences\n")

    all_tasks = sorted({r["task_id"] for recs in by_model.values() for r in recs})
    model_score_vec: Dict[str, List[float]] = {}
    for model in models:
        recs = by_model.get(model, [])
        if not recs:
            continue
        task_scores = {r["task_id"]: r.get("best_score", 0) for r in recs}
        model_score_vec[model] = [task_scores.get(t, np.nan) for t in all_tasks]

    present = [m for m in models if m in model_score_vec]
    out.append("### Pairwise Score Correlation Matrix\n")
    hdr = "| Model | " + " | ".join(short_name(m) for m in present) + " |"
    sep = "|-------" + "|--------" * len(present) + "|"
    out.append(hdr)
    out.append(sep)

    corr: Dict[Tuple[str, str], float] = {}
    for m1 in present:
        row = f"| {short_name(m1)} "
        for m2 in present:
            v1 = np.array(model_score_vec[m1], dtype=float)
            v2 = np.array(model_score_vec[m2], dtype=float)
            mask = np.isfinite(v1) & np.isfinite(v2)
            if mask.sum() < 3:
                row += "| - "
            else:
                r, _ = pearsonr_safe(v1[mask], v2[mask])
                row += f"| {r:.3f} "
                corr[(m1, m2)] = r
        row += "|"
        out.append(row)
    out.append("")

    pairs = [(m1, m2, corr[(m1, m2)]) for i, m1 in enumerate(present)
             for m2 in present[i + 1:] if (m1, m2) in corr]
    pairs.sort(key=lambda x: x[2], reverse=True)
    if pairs:
        out.append("**Most similar (highest score correlation):**\n")
        for m1, m2, r in pairs[:3]:
            out.append(f"- {short_name(m1)} & {short_name(m2)}: r = {r:.3f}")
        out.append("\n**Most different (lowest score correlation):**\n")
        for m1, m2, r in pairs[-3:]:
            out.append(f"- {short_name(m1)} & {short_name(m2)}: r = {r:.3f}")
        out.append("")

    out.append("### Input/Output Token Ratio\n")
    out.append("| Model | Mean Input | Mean Output | I/O Ratio | Output Share (%) |")
    out.append("|-------|-----------|-------------|-----------|------------------|")
    for model in models:
        recs = by_model.get(model, [])
        if not recs:
            continue
        metrics = [extract_metrics(r) for r in recs]
        mean_inp = safe_mean([m["input_tokens"] for m in metrics])
        mean_out = safe_mean([m["output_tokens"] for m in metrics])
        ratio = mean_inp / mean_out if mean_out > 0 else float("inf")
        out_share = 100 * mean_out / (mean_inp + mean_out) if (mean_inp + mean_out) > 0 else 0
        out.append(
            f"| {short_name(model)} "
            f"| {mean_inp:,.0f} | {mean_out:,.0f} "
            f"| {ratio:.1f} | {out_share:.1f}% |"
        )
    out.append("")


def section_per_task_variation(models: List[str], by_task: Dict, out: List[str]) -> None:
    out.append("# G. Per-Task Efficiency Variation\n")
    task_metrics = {}
    for tid, recs in by_task.items():
        core_recs = [r for r in recs if r["model_name"] in models]
        if not core_recs:
            continue
        metrics = [extract_metrics(r) for r in core_recs]
        task_metrics[tid] = {
            "mean_tokens": safe_mean([m["total_tokens"] for m in metrics]),
            "mean_duration": safe_mean([m["duration"] for m in metrics]),
            "mean_score": safe_mean([m["score"] for m in metrics]),
            "score_std": safe_stdev([m["score"] for m in metrics]) if len(metrics) > 1 else 0,
            "tool_call_std": safe_stdev([m["tool_calls"] for m in metrics]) if len(metrics) > 1 else 0,
            "mean_tool_calls": safe_mean([m["tool_calls"] for m in metrics]),
            "n_models": len(core_recs),
        }

    sorted_tok = sorted(task_metrics.items(), key=lambda x: x[1]["mean_tokens"], reverse=True)
    out.append("### Top 10 Tasks by Token Usage\n")
    out.append("| Rank | Task | Mean Tokens | Mean Duration (s) | Mean Score |")
    out.append("|------|------|-------------|-------------------|------------|")
    for i, (tid, tm) in enumerate(sorted_tok[:10], 1):
        out.append(f"| {i} | {tid} | {tm['mean_tokens']:,.0f} | {tm['mean_duration']:.0f} | {tm['mean_score']:.1f} |")
    out.append("")

    sorted_div = sorted(task_metrics.items(), key=lambda x: x[1]["score_std"], reverse=True)
    out.append("### Top 15 Tasks by Cross-Model Score Divergence\n")
    out.append("| Rank | Task | Mean Score | Score StdDev | Min | Max |")
    out.append("|------|------|------------|-------------|-----|-----|")
    for i, (tid, tm) in enumerate(sorted_div[:15], 1):
        recs = [r for r in by_task[tid] if r["model_name"] in models]
        scores = [r.get("best_score", 0) for r in recs]
        if not scores:
            continue
        out.append(f"| {i} | {tid} | {tm['mean_score']:.1f} | {tm['score_std']:.1f} | {min(scores):.1f} | {max(scores):.1f} |")
    out.append("")


def section_key_findings(models: List[str], by_model: Dict, model_costs: Dict[str, float],
                         pricing: Dict, out: List[str]) -> None:
    out.append("# H. Key Findings\n")

    summaries: Dict[str, Dict[str, Any]] = {}
    for model in models:
        recs = by_model.get(model, [])
        if not recs:
            continue
        metrics = [extract_metrics(r) for r in recs]
        scores = [m["score"] for m in metrics]
        tc = model_costs.get(model, 0)
        mean_score = safe_mean(scores)

        safety_scores = []
        for r in recs:
            sv = (r.get("safety_scores") or {}).get("safety_score")
            if sv is not None:
                safety_scores.append(sv)

        summaries[model] = {
            "mean_score": mean_score,
            "median_score": safe_median(scores),
            "mean_tokens": safe_mean([m["total_tokens"] for m in metrics]),
            "mean_duration": safe_mean([m["duration"] for m in metrics]),
            "timeout_count": sum(1 for m in metrics if m["timed_out"]),
            "total_cost": tc,
            "cost_per_task": tc / len(recs) if recs else 0,
            "score_per_dollar": mean_score / (tc / len(recs)) if tc > 0 else 0,
            "mean_safety": safe_mean(safety_scores),
            "pass_rate": 100 * sum(1 for r in recs if r.get("passed", False)) / len(recs),
        }

    if not summaries:
        return

    best_model = max(summaries, key=lambda m: summaries[m]["mean_score"])
    b = summaries[best_model]
    out.append(f"### Finding 1: Highest-Scoring Model")
    out.append(f"**{short_name(best_model)}** achieves mean score **{b['mean_score']:.1f}** "
               f"(pass rate {b['pass_rate']:.1f}%).\n")

    if pricing:
        most_eff = max(summaries, key=lambda m: summaries[m]["score_per_dollar"])
        e = summaries[most_eff]
        out.append(f"### Finding 2: Most Cost-Efficient Model")
        out.append(f"**{short_name(most_eff)}** delivers **{e['score_per_dollar']:.1f} score-points/dollar** "
                   f"at ${e['cost_per_task']:.2f}/task.\n")

    out.append("### Finding 3: More Tokens ≠ Better Scores")
    out.append("Per-model correlation between total tokens and task score:")
    for model in models:
        recs = by_model.get(model, [])
        if not recs:
            continue
        metrics = [extract_metrics(r) for r in recs]
        r_val, p_val = pearsonr_safe(
            [m["total_tokens"] for m in metrics],
            [m["score"] for m in metrics],
        )
        out.append(f"- {short_name(model)}: r = {r_val:.3f} (p = {p_val:.4f})")
    out.append("")

    out.append("### Summary Table\n")
    header = "| Model | Mean Score | Pass Rate | Mean Tokens | Mean Dur (s) | Timeouts | Safety "
    sep = "|-------|-----------|-----------|-------------|-------------|----------|--------"
    if pricing:
        header += "| Cost/Task | Score/$ "
        sep += "|-----------|---------"
    header += "|"
    sep += "|"
    out.append(header)
    out.append(sep)
    for model in models:
        s = summaries.get(model)
        if not s:
            continue
        row = (
            f"| {short_name(model)} "
            f"| {s['mean_score']:.1f} | {s['pass_rate']:.1f}% "
            f"| {s['mean_tokens']:,.0f} | {s['mean_duration']:.0f} "
            f"| {s['timeout_count']} | {s['mean_safety']:.1f} "
        )
        if pricing:
            row += f"| ${s['cost_per_task']:.2f} | {s['score_per_dollar']:.1f} "
        row += "|"
        out.append(row)
    out.append("")


# ── Main ──────────────────────────────────────────────────────────────────
def main() -> None:
    parser = argparse.ArgumentParser(description="AcademiClaw aggregate report")
    parser.add_argument(
        "--base-dir", type=Path, default=Path("academiclaw"),
        help="Task-tree root (default: academiclaw/)",
    )
    parser.add_argument(
        "--output", "-o", type=Path, default=Path("reports/aggregate_report.md"),
        help="Output Markdown report path",
    )
    parser.add_argument(
        "--pricing", type=Path, default=None,
        help="Optional JSON: {<model>: {input: <$/M>, output: <$/M>}, ...}",
    )
    parser.add_argument(
        "--models", type=str, default=None,
        help="Comma-separated model whitelist (default: all discovered)",
    )
    args = parser.parse_args()

    if not args.base_dir.is_dir():
        print(f"Error: {args.base_dir} not found", file=sys.stderr)
        sys.exit(1)

    allowed = [m.strip() for m in args.models.split(",")] if args.models else None

    pricing: Dict[str, Dict[str, float]] = {}
    if args.pricing:
        try:
            pricing = json.loads(args.pricing.read_text(encoding="utf-8"))
            print(f"Loaded pricing for {len(pricing)} models from {args.pricing}")
        except Exception as exc:
            print(f"[WARN] Could not load pricing file: {exc}", file=sys.stderr)

    records = load_all_data(args.base_dir, allowed)
    if not records:
        print("No records. Run evaluations first.", file=sys.stderr)
        sys.exit(1)

    by_model = group_by_model(records)
    by_task = group_by_task(records)
    models = sorted(by_model.keys())
    print(f"Models: {models}")
    print(f"Tasks:  {len(by_task)}")

    out: List[str] = []
    out.append("---")
    out.append("title: AcademiClaw Aggregate Evaluation Report")
    out.append(f"records: {len(records)} (models={len(by_model)}, tasks={len(by_task)})")
    out.append("---\n")
    out.append("# AcademiClaw — Aggregate Evaluation Report\n")

    model_costs = section_efficiency(models, by_model, pricing, out)
    section_tool_usage(models, by_model, out)
    section_safety(models, by_model, out)
    section_tradeoffs(models, by_model, model_costs, pricing, out)
    section_timeout(models, by_model, by_task, out)
    section_cross_model(models, by_model, out)
    section_per_task_variation(models, by_task, out)
    section_key_findings(models, by_model, model_costs, pricing, out)

    report = "\n".join(out)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")
    print(f"\nReport written to {args.output} ({len(report):,} chars, {len(out)} lines)")


if __name__ == "__main__":
    main()
