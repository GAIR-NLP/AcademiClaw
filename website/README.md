# AcademiClaw — Leaderboard Website

A Vite + React + TypeScript app that renders the AcademiClaw leaderboard
from this repository's evaluation results. The site is statically built
and deployed to GitHub Pages via `.github/workflows/deploy-website.yml`.

## What it shows

- **Leaderboard** — each of the six paper models ranked on pass rate, safety,
  token efficiency, and cost per task. Language pills filter to EN/ZH subsets.
- **Expanded row (per model)** with three tabs:
  - **Tasks** — per-task score, safety, and tokens
  - **Tool Usage** — stacked bar of read / write / edit / exec / process
    tool calls per task, with model averages in the legend
  - **Safety** — S1 · Destructive Ops, S2 · Info Leakage, S3 · Boundary,
    S4 · Privilege, S5 · Network / Supply; per-task and aggregate scores
- **Tasks page** — the full 80-task catalog with language, category, and
  query snippets.

## Data source

`scripts/sync-data.sh` scans `../academiclaw/<task>/openclaw/<model>/meta_eval.json`
for every task, and emits into `public/data/`:

- `<model>_openclaw.json` — per-model summary + per-task results
- `manifest.json` — list of the per-model files
- `tasks-catalog.json` — task metadata for the Tasks page

The script excludes any model that is missing results for some tasks, and
embeds the public list prices from `analysis/pricing.example.json` so the
site can display cost-per-task. Override the tree location with
`ACADEMICLAW_DIR=/path/to/academiclaw`.

## Scripts

```bash
npm install        # install deps
npm run sync       # regenerate public/data/ from ../academiclaw/
npm run dev        # dev server (runs sync first)
npm run build      # production build into dist/
npm run preview    # serve dist/ locally
```

`dev` and `build` automatically run `sync` first via the `predev` and
`prebuild` npm lifecycle hooks, so a fresh clone can go straight to
`npm run dev`.

## Deployment

Pushes to `main` that touch `website/**` or any `academiclaw/**/meta_eval.json`
rebuild the site and publish it to GitHub Pages. See
`.github/workflows/deploy-website.yml`.
