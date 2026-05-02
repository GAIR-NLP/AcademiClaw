# Contributing to AcademiClaw

Thank you for your interest in contributing! This document describes how to
propose new tasks, improve evaluation rubrics, or report bugs.

## Reporting issues

Please open a GitHub issue describing:

- The task (directory name under `academiclaw/`) affected, if any.
- The model / agent backend and the command you used.
- What you expected to happen and what actually happened.
- Any relevant logs (please redact API keys before pasting).

## Proposing a new task

AcademiClaw tasks follow a uniform layout. To propose a new task:

1. Fork this repository and create a new branch.
2. Create a directory `academiclaw/<lang>_<task_id>/` (prefix with `en_` or
   `zh_` depending on the language of the task prompt).
3. Populate the required files (see below).
4. Run the task end-to-end locally with at least one strong model to verify
   the rubric produces sensible scores.
5. Open a pull request. Please include the model-vs-rubric numbers from
   your local run in the PR description.

### Required files

```
academiclaw/<task_id>/
├── description.json     # task_id, task_name, description, deliverables
├── Dockerfile           # extends agencybench-sandbox (or ...-cuda for GPU)
├── eval_task.py         # harness entry point (usually unchanged template)
├── eval/rubric.py       # scoring logic; must expose evaluate(answer_dir)
├── workspace/query.md   # the task prompt the agent reads
└── context/             # any data files the agent is allowed to read
```

### Task design guidelines

- **Reproducibility.** All external dependencies must be pinned in the
  Dockerfile or `context/` directory. Tasks that rely on network services
  must declare the required API keys and document how to obtain them.
- **Privacy.** Do not include personal identifiers, private API keys, or
  copyrighted materials in `context/`. Use placeholders and provide a
  download script if the real data cannot be redistributed.
- **Rubric determinism.** Numerical checks should be deterministic.
  LLM-as-Judge rubrics must use fixed seeds / temperature=0 where the API
  allows it, and the prompt must be included verbatim in `rubric.py`.

## Improving an existing rubric

Rubric changes that alter scoring must be accompanied by:

1. A justification in the pull-request description.
2. Rerun results on at least two models already present in the benchmark
   so reviewers can compare score changes.

## Code style

- Python 3.10+, standard library preferred inside rubric code.
- Keep `rubric.py` self-contained; import only from the standard library or
  from packages already declared in `docker/requirements.txt`.

## Security / secrets

Never commit real API keys. The repository's `.gitignore` blocks common
`.env` patterns, but please review your diffs manually before pushing.
If you accidentally push a key, revoke it at the provider immediately —
rewriting git history is not sufficient once a commit is public.
