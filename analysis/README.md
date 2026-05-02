# Analysis scripts

Post-evaluation analysis for AcademiClaw. Run after `batch_eval.sh`
finishes — these scripts read every `academiclaw/<task_id>/<agent>/<model>/meta_eval.json`
and produce summary reports.

## Scripts

### `token_efficiency.py`

Ranks models by average total tokens per task (lower = more efficient).
Emits a human-readable console report and an optional JSON dump.

```bash
# Console report only
python3 analysis/token_efficiency.py

# Also write JSON
python3 analysis/token_efficiency.py --output reports/token_efficiency.json

# Custom task tree
python3 analysis/token_efficiency.py --base-dir /path/to/academiclaw
```

Scoring formula:
```
efficiency_score = 100 * (best_model_avg_tokens / this_model_avg_tokens)
```
The most efficient model gets 100; one spending 2× tokens gets 50.

### `aggregate_report.py`

Produces a Markdown report mirroring the paper's evaluation appendix:
efficiency, tool usage, safety (S1–S5), quality tradeoffs, timeouts,
cross-model correlations, per-task variation, and key findings.

```bash
# Minimal — no pricing, cost sections are skipped
python3 analysis/aggregate_report.py

# With pricing for cost estimation
python3 analysis/aggregate_report.py \
    --pricing analysis/pricing.example.json \
    --output reports/aggregate_report.md

# Restrict to a subset of models
python3 analysis/aggregate_report.py \
    --models claude-opus-4-6,gpt-5.4
```

#### Pricing file format

`pricing.example.json` ships with the public list prices in effect during
the paper's experiments, but those rates change. Update before using for
cost estimation. Keys are directory names under `<task_id>/<agent>/`;
values are USD per **million** tokens:

```json
{
  "claude-opus-4-6": {"input": 15.0, "output": 75.0},
  "gpt-5.4":         {"input":  2.0, "output":  8.0}
}
```

Models missing from the pricing file are still included in non-cost
sections; cost columns show as blank.

## Dependencies

Both scripts use only `numpy` (already in `docker/requirements.txt`).
`scipy` is used opportunistically for exact Pearson p-values if
installed; otherwise a normal-approximation fallback is used.

## Reproducing the paper

```bash
# 1. Build images and run all 80 tasks across the six paper models
./build_all_images.sh -j 8
OPENCLAW_MODEL=claude-opus-4-6  ./batch_eval.sh -j 4
OPENCLAW_MODEL=claude-sonnet-4-6 ./batch_eval.sh -j 4 --resume
# ... repeat for gpt-5.4, gemini-3.1-pro-preview, Qwen3.5-397B-A17B, MiniMax-M2.7

# 2. Aggregate
python3 analysis/token_efficiency.py --output reports/token_efficiency.json
python3 analysis/aggregate_report.py --pricing analysis/pricing.example.json
```
