#!/usr/bin/env python3
"""
Token efficiency evaluation for AcademiClaw.

Scans all `academiclaw/<task_id>/openclaw/<model>/meta_eval.json` files,
computes per-task token usage, then ranks models by average total tokens.

Scoring (ratio-based):
    efficiency_score = 100 * (best_avg_tokens / model_avg_tokens)

The most efficient model scores 100; a model consuming 2x tokens scores 50.

Usage:
    python3 analysis/token_efficiency.py
    python3 analysis/token_efficiency.py --base-dir academiclaw
    python3 analysis/token_efficiency.py --output reports/token_efficiency.json
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List


def scan_results(base_dir: Path) -> List[Dict[str, Any]]:
    """Scan <base_dir>/<task_id>/openclaw/<model>/meta_eval.json files."""
    results: List[Dict[str, Any]] = []
    for task_dir in sorted(base_dir.iterdir()):
        if not task_dir.is_dir():
            continue
        if not (task_dir / "description.json").exists():
            continue
        # openclaw is the dominant backend; also allow claude-code/ layout
        for agent in ("openclaw", "claude-code"):
            agent_dir = task_dir / agent
            if not agent_dir.is_dir():
                continue
            for model_dir in sorted(agent_dir.iterdir()):
                if not model_dir.is_dir():
                    continue
                meta_path = model_dir / "meta_eval.json"
                if not meta_path.exists():
                    continue
                try:
                    data = json.loads(meta_path.read_text(encoding="utf-8"))
                except (json.JSONDecodeError, OSError) as exc:
                    print(f"  [WARN] {meta_path}: {exc}", file=sys.stderr)
                    continue

                agg = data.get("aggregate_metrics", {})
                tokens = agg.get("total_tokens", {})
                total = tokens.get("total", 0)
                if total <= 0:
                    continue

                results.append({
                    "task_id": task_dir.name,
                    "agent": agent,
                    "model": model_dir.name,
                    "best_score": data.get("best_score", 0),
                    "total_tokens": total,
                    "input_tokens": tokens.get("input", 0),
                    "output_tokens": tokens.get("output", 0),
                    "total_tool_calls": agg.get("total_tool_calls", 0),
                    "duration_seconds": agg.get("total_duration_seconds", 0),
                })
    return results


def compute_rankings(results: List[Dict]) -> Dict[str, Any]:
    """Aggregate by model, rank by average total tokens."""
    model_data: Dict[str, List[Dict]] = defaultdict(list)
    for r in results:
        model_data[r["model"]].append(r)

    models = sorted(model_data.keys())
    if not models:
        return {"error": "no results with token data found"}

    model_summary: Dict[str, Dict[str, Any]] = {}
    for model in models:
        entries = model_data[model]
        totals = [e["total_tokens"] for e in entries]
        inputs = [e["input_tokens"] for e in entries]
        outputs = [e["output_tokens"] for e in entries]
        scores = [e["best_score"] for e in entries]
        durations = [e["duration_seconds"] for e in entries]
        tool_calls = [e["total_tool_calls"] for e in entries]

        model_summary[model] = {
            "task_count": len(entries),
            "avg_total_tokens": round(sum(totals) / len(totals)),
            "avg_input_tokens": round(sum(inputs) / len(inputs)),
            "avg_output_tokens": round(sum(outputs) / len(outputs)),
            "avg_tool_calls": round(sum(tool_calls) / len(tool_calls), 1),
            "avg_duration_seconds": round(sum(durations) / len(durations), 1),
            "avg_best_score": round(sum(scores) / len(scores), 1),
            "total_tokens_all": sum(totals),
        }

    # Rank by avg_total_tokens (ascending — lower is more efficient)
    ranked = sorted(models, key=lambda m: model_summary[m]["avg_total_tokens"])
    best_avg = model_summary[ranked[0]]["avg_total_tokens"]
    for i, model in enumerate(ranked):
        avg = model_summary[model]["avg_total_tokens"]
        model_summary[model]["rank"] = i + 1
        model_summary[model]["efficiency_score"] = (
            round(100 * best_avg / avg, 1) if avg > 0 else 0
        )

    # Per-task comparison (only tasks covered by multiple models)
    task_models: Dict[str, Dict[str, int]] = defaultdict(dict)
    for r in results:
        task_models[r["task_id"]][r["model"]] = r["total_tokens"]

    per_task: List[Dict[str, Any]] = []
    for task_id in sorted(task_models.keys()):
        entry = task_models[task_id]
        if len(entry) < 2:
            continue
        best = min(entry.values())
        row: Dict[str, Any] = {"task_id": task_id}
        for model, tokens in sorted(entry.items()):
            row[model] = {
                "tokens": tokens,
                "ratio": round(tokens / best, 2) if best > 0 else 0,
            }
        per_task.append(row)

    return {
        "model_count": len(models),
        "total_results": len(results),
        "ranking": ranked,
        "models": model_summary,
        "per_task_comparison": per_task,
    }


def print_report(report: Dict) -> None:
    print("=" * 72)
    print("AcademiClaw — Token Efficiency Report")
    print("=" * 72)
    print(f"Models evaluated:  {report['model_count']}")
    print(f"Task-model pairs:  {report['total_results']}")
    print()

    print("OVERALL RANKING  (lower avg tokens = more efficient)")
    print("-" * 72)
    print(f"{'Rank':<5} {'Model':<32} {'Avg Tokens':>12} {'Score':>8} {'Tasks':>7}")
    print("-" * 72)
    for model in report["ranking"]:
        s = report["models"][model]
        print(
            f"{s['rank']:<5} {model:<32} {s['avg_total_tokens']:>12,} "
            f"{s['efficiency_score']:>7.1f} {s['task_count']:>7}"
        )
    print()

    print("DETAILED METRICS")
    print("-" * 72)
    for model in report["ranking"]:
        s = report["models"][model]
        print(f"\n  {model}  (rank #{s['rank']}, score {s['efficiency_score']})")
        print(f"    Avg input tokens:   {s['avg_input_tokens']:>12,}")
        print(f"    Avg output tokens:  {s['avg_output_tokens']:>12,}")
        print(f"    Avg total tokens:   {s['avg_total_tokens']:>12,}")
        print(f"    Avg tool calls:     {s['avg_tool_calls']:>12}")
        print(f"    Avg duration (s):   {s['avg_duration_seconds']:>12.1f}")
        print(f"    Avg task score:     {s['avg_best_score']:>12.1f} / 100")
    print()

    pq = report.get("per_task_comparison", [])
    if pq:
        print(f"PER-TASK COMPARISON  ({len(pq)} tasks covered by >=2 models)")
        print("-" * 72)
        for row in pq[:20]:
            parts = [row["task_id"]]
            for model, data in sorted(row.items()):
                if model == "task_id":
                    continue
                parts.append(f"{model}={data['tokens']:,}({data['ratio']}x)")
            print(f"  {' | '.join(parts)}")
        if len(pq) > 20:
            print(f"  ... and {len(pq) - 20} more tasks")
    print()
    print("=" * 72)


def main() -> None:
    parser = argparse.ArgumentParser(description="Token efficiency ranking")
    parser.add_argument(
        "--base-dir", type=Path, default=Path("academiclaw"),
        help="Directory containing <task_id>/openclaw/<model>/meta_eval.json",
    )
    parser.add_argument("--output", "-o", type=Path, help="Write JSON report here")
    args = parser.parse_args()

    if not args.base_dir.is_dir():
        print(f"Error: {args.base_dir} not found", file=sys.stderr)
        sys.exit(1)

    print(f"Scanning {args.base_dir} ...")
    results = scan_results(args.base_dir)
    print(f"Found {len(results)} task-model pairs with token data")
    if not results:
        print("No results. Run evaluations first.")
        sys.exit(1)

    report = compute_rankings(results)
    print_report(report)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(report, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        print(f"JSON report saved to: {args.output}")


if __name__ == "__main__":
    main()
