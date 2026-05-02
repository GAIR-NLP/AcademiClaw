# AcademiClaw

**A benchmark for evaluating AI agents on realistic academic workflows.**

AcademiClaw is a collection of 80 open-ended tasks that require an AI agent
to plan, write code, run experiments inside a sandboxed environment, and
produce a concrete deliverable (a script, a report, a figure, a dataset,
etc.). Tasks are drawn from real graduate-level academic work across
disciplines including systems programming, machine learning, NLP,
scientific writing, data analysis, and domain-specific simulations.

- **80 tasks** — 49 English, 31 Chinese
- **Grounded in real academic work** — each task has a concrete deliverable
  and a deterministic-where-possible rubric
- **Mixed resource requirements** — 64 CPU-only tasks and 16 GPU tasks
  (flagged via `Dockerfile.cuda`)
- **Reproducible** — every task runs in an isolated Docker container with
  pinned dependencies
- **Multi-agent harness** — supports Claude Code, generic OpenAI-compatible
  backends (`openclaw`), and manual mode out of the box

The repository accompanies the paper _"AcademiClaw: A Benchmark for
Evaluating AI Agents on Realistic Academic Workflows"_ (GAIR-NLP, 2026).
See `CITATION.cff` for how to cite.


## Repository layout

```
academiclaw/                     80 task directories (en_* + zh_*)
  <task_id>/
    description.json             task metadata: id, name, deliverables
    Dockerfile | Dockerfile.cuda image spec (CPU or GPU)
    eval_task.py                 harness entry point
    workspace/                   initial files handed to the agent
    context/                     read-only reference data
    eval/rubric.py               scoring logic
    openclaw/<model_name>/
      conversation_log.json      full agent trajectory (sanitized)
      meta_eval.json             rubric scores and per-dimension breakdown
  QUERY_CATALOG.md               auto-generated per-task index (English)
  QUERY_SUMMARY_ZH.md            auto-generated per-task index (Chinese)

docker/                          base Docker images shared by all tasks
  Dockerfile                     CPU base image (agencybench-sandbox)
  Dockerfile.cuda                GPU base image (agencybench-sandbox-cuda)
  docker-entrypoint.sh
  requirements.txt

run_in_docker.sh                 main entry point for running a task
.env.example                     template for the per-task .env file
```

Each task's `openclaw/` subdirectory contains the evaluation trajectories
we ran for the paper. The full per-attempt workspace snapshots
(`attempt_*`) are **not** included in this repository to keep it small;
only the final conversation log and score metadata are shipped.


## Quick start

### Prerequisites

- Docker ≥ 20.10 (`docker --version`)
- A POSIX shell (bash / zsh)
- For GPU tasks: NVIDIA Container Toolkit and a visible NVIDIA device

### 1. Build the base images

```bash
docker build -t agencybench-sandbox        -f docker/Dockerfile      docker/
docker build -t agencybench-sandbox-cuda   -f docker/Dockerfile.cuda docker/   # GPU tasks only
```

### 2. Configure credentials

Copy the example env file into the task you want to run and fill in your
keys. All the keys are documented inline:

```bash
cp .env.example academiclaw/en_graph_algorithms/.env
$EDITOR academiclaw/en_graph_algorithms/.env
```

### 3. Run a task

```bash
./run_in_docker.sh academiclaw/en_graph_algorithms
```

Common flags:

| Flag | Effect |
| ---- | ------ |
| `-a <type>` | pick the agent backend: `claude_code`, `openclaw`, `manual` |
| `-m <name>` | override the model name |
| `-n <k>`    | max retry attempts (default 1) |
| `-e`        | evaluation-only (don't run the agent, just score the existing workspace) |
| `-r`        | force rebuild of the task-specific image |
| `--debug`   | drop into an interactive shell inside the container |

Output is written to `academiclaw/<task_id>/openclaw/<model_name>/`:
- `attempt_<k>/`   — snapshot of the workspace after attempt k
- `conversation_log.json` — full agent dialogue
- `meta_eval.json`        — final rubric scores


## Evaluating a new agent

Any agent that can be driven programmatically fits either the
`claude_code` or `openclaw` slot:

- **`claude_code`** expects the `ANTHROPIC_API_KEY` / `ANTHROPIC_BASE_URL`
  pair (Anthropic-compatible chat completion endpoint).
- **`openclaw`** expects `OPENCLAW_API_KEY` / `OPENCLAW_BASE_URL` /
  `OPENCLAW_MODEL` and speaks the OpenAI-compatible chat completion
  protocol — any proxy that emits this shape (vLLM, SGLang, LiteLLM, etc.)
  works as a drop-in.

To add a new backend, implement a new agent class under the agent
registry in the harness and wire it up through `AGENT_TYPE` in `.env`.


## Dataset statistics (paper)

| Split | Count | Notes |
| ----- | ----- | ----- |
| English (`en_*`) | 49 | CS, ML, NLP, scientific writing, data analysis |
| Chinese (`zh_*`) | 31 | course-integrated tasks, sciences, humanities |
| GPU required     | 16 | training, rendering, or inference workloads |
| CPU only         | 64 | |
| **Total**        | **80** | |

We release evaluation trajectories for seven frontier models
(`claude-opus-4-6`, `claude-sonnet-4-6`, `gpt-5.4`,
`gemini-3.1-pro-preview`, `glm51`, `MiniMax-M2.7`,
`Qwen3.5-397B-A17B`). Full details are in the paper.


## Citing

If you use AcademiClaw, please cite the paper — see `CITATION.cff` for
the structured citation record.


## License

AcademiClaw is released under the Apache License 2.0. See `LICENSE`.

Task `context/` directories sometimes bundle third-party materials (e.g.
course textbooks, open-source reference repositories). Those retain their
original licenses; see the task-level `README.md` or `NOTICE` where
applicable. Please review the licensing of any content you redistribute.


## Responsible use

AcademiClaw contains realistic prompts that reflect authentic graduate
research workflows. This includes tasks that touch on security analysis,
privacy auditing, and bias-sensitive subject matter. These tasks are
provided for **evaluation of model capability and safety** — not for
running against production systems. The dataset is offered under the
assumption that users are building better AI agents, not circumventing
safeguards.

## Acknowledgements

AcademiClaw is maintained by the GAIR-NLP group. Many tasks derive from
open-source course materials, benchmarks, and research projects — their
original authors are credited in task-level `context/` files wherever
relevant.
