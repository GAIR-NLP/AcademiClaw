#!/bin/bash
# =============================================================================
# AcademiClaw — Batch evaluation
#
# Dispatches `./run_in_docker.sh` in parallel across every task in
# `academiclaw/` (or a filtered subset) for one or more agent backends.
# Assumes per-task Docker images are already built (see build_all_images.sh).
#
# Usage:
#   # 1. configure credentials once in the repo root
#   cp .env.example .env
#   $EDITOR .env         # fill in keys, set OPENCLAW_MODEL, etc.
#
#   # 2. dispatch
#   ./batch_eval.sh                         # run all 80 tasks, openclaw agent, 8-wide
#   ./batch_eval.sh -j 16                   # 16 parallel containers
#   ./batch_eval.sh --agents claude_code,openclaw
#                                           # run both agents per task
#   ./batch_eval.sh --only en_cmo_proof,zh_huaxue_jingsai
#                                           # only these two tasks
#   ./batch_eval.sh --resume                # skip tasks with existing meta_eval.json
#   ./batch_eval.sh --cpu-only              # skip GPU tasks
#   ./batch_eval.sh --gpu-only              # only GPU tasks (1 GPU/container)
#   ./batch_eval.sh --dry-run               # print plan without running
#
# Required: docker, a POSIX shell, optionally nvidia-container-toolkit
# for GPU tasks.
# =============================================================================

set -eo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; CYAN='\033[0;36m'; NC='\033[0m'

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
TASK_ROOT="$PROJECT_ROOT/academiclaw"
LOG_DIR="$PROJECT_ROOT/logs/$(date +%Y%m%d_%H%M%S)"

# defaults
PARALLEL=8
AGENTS=("openclaw")
ONLY_FILTER=""
RESUME=false
MODE="all"         # all | cpu | gpu
DRY_RUN=false
MAX_ATTEMPTS=1
ROOT_ENV="$PROJECT_ROOT/.env"

show_help() { sed -n '3,27p' "$0"; exit 0; }

while [[ $# -gt 0 ]]; do
  case $1 in
    -j|--jobs|--parallel) PARALLEL="$2"; shift 2 ;;
    --agents)       IFS=',' read -ra AGENTS <<< "$2"; shift 2 ;;
    --only)         ONLY_FILTER="$2"; shift 2 ;;
    --resume)       RESUME=true; shift ;;
    --cpu-only)     MODE="cpu"; shift ;;
    --gpu-only)     MODE="gpu"; shift ;;
    --attempts)     MAX_ATTEMPTS="$2"; shift 2 ;;
    --env)          ROOT_ENV="$2"; shift 2 ;;
    --dry-run)      DRY_RUN=true; shift ;;
    -h|--help)      show_help ;;
    *) echo -e "${RED}[ERROR] Unknown arg: $1${NC}"; show_help ;;
  esac
done

if [[ ! -f "$ROOT_ENV" ]]; then
  echo -e "${RED}[ERROR]${NC} Root env file not found: $ROOT_ENV"
  echo "   cp .env.example .env  &&  \$EDITOR .env"
  exit 1
fi

mkdir -p "$LOG_DIR"
echo -e "${BLUE}[INFO]${NC} Log directory: $LOG_DIR"

# -- Task discovery ----------------------------------------------------------
is_gpu_task() {
  local d="$1"
  [[ -f "$d/Dockerfile.cuda" ]] && return 0
  [[ -f "$d/Dockerfile" ]] && grep -qE "FROM\s+(agencybench-sandbox-cuda|nvidia/cuda)" "$d/Dockerfile" && return 0
  find "$d/context" -maxdepth 3 -name '*.cu' 2>/dev/null | grep -q . && return 0
  return 1
}

IFS=',' read -ra ONLY_ARR <<< "$ONLY_FILTER"
declare -a TASKS=()
for td in "$TASK_ROOT"/*/; do
  tid=$(basename "$td")
  [[ ! -f "$td/description.json" ]] && continue
  if [[ -n "$ONLY_FILTER" ]]; then
    keep=false
    for k in "${ONLY_ARR[@]}"; do [[ "$k" == "$tid" ]] && keep=true; done
    $keep || continue
  fi
  if is_gpu_task "$td"; then
    [[ "$MODE" == "cpu" ]] && continue
  else
    [[ "$MODE" == "gpu" ]] && continue
  fi
  TASKS+=("$td")
done

TOTAL=${#TASKS[@]}
NUM_AGENTS=${#AGENTS[@]}

# -- Plan --------------------------------------------------------------------
echo -e "${BLUE}============================================================${NC}"
echo -e "${BLUE}  AcademiClaw Batch Evaluation${NC}"
echo -e "${BLUE}============================================================${NC}"
echo "  Tasks:        $TOTAL"
echo "  Agents:       ${AGENTS[*]}"
echo "  Parallel:     $PARALLEL containers (across ${NUM_AGENTS} agent(s))"
echo "  Env file:     $ROOT_ENV"
echo "  Resume mode:  $RESUME"
echo "  Mode filter:  $MODE"
echo "  Attempts:     $MAX_ATTEMPTS"
echo

if $DRY_RUN; then
  for td in "${TASKS[@]}"; do
    tid=$(basename "$td")
    for a in "${AGENTS[@]}"; do echo "  [plan] $a  $tid"; done
  done
  exit 0
fi

# -- Stage .env into each task dir we are about to run -----------------------
# run_in_docker.sh reads .env from the task dir.  We copy the root .env there
# (non-destructive: only if task dir has no .env already) so users only need
# to maintain one credentials file at the repo root.
stage_env() {
  local td="$1"
  if [[ ! -f "$td/.env" ]]; then
    cp "$ROOT_ENV" "$td/.env"
    echo "__staged__" > "$td/.env.staged"
  fi
}
unstage_env() {
  local td="$1"
  if [[ -f "$td/.env.staged" ]]; then
    rm -f "$td/.env" "$td/.env.staged"
  fi
}
trap 'for td in "${TASKS[@]}"; do unstage_env "$td"; done' EXIT

# -- Launch ------------------------------------------------------------------
declare -A PIDS              # pid -> "task_id|agent"
declare -A OK_BY_AGENT
declare -A FAIL_BY_AGENT
for a in "${AGENTS[@]}"; do OK_BY_AGENT[$a]=0; FAIL_BY_AGENT[$a]=0; done
DONE=0; START_TS=$(date +%s)

launch_one() {
  local td="$1" agent="$2"
  local tid; tid=$(basename "$td")
  local safe_agent=${agent/_/-}
  local log="$LOG_DIR/${safe_agent}__${tid}.log"

  stage_env "$td"

  local extra=()
  if is_gpu_task "$td"; then extra+=("--gpu"); else extra+=("--no-gpu"); fi

  (
    cd "$PROJECT_ROOT"
    MAX_ATTEMPTS="$MAX_ATTEMPTS" \
    ./run_in_docker.sh -a "$agent" -n "$MAX_ATTEMPTS" "${extra[@]}" \
        "academiclaw/$tid" > "$log" 2>&1
  ) &
  local pid=$!
  PIDS[$pid]="$tid|$agent"
}

reap_one() {
  local finished=""
  wait -n -p finished 2>/dev/null || true
  if [[ -z "${finished:-}" ]]; then
    for pid in "${!PIDS[@]}"; do
      if ! kill -0 "$pid" 2>/dev/null; then finished=$pid; break; fi
    done
  fi
  [[ -z "${finished:-}" ]] && { sleep 2; return; }

  local code=0; wait "$finished" 2>/dev/null || code=$?
  local info="${PIDS[$finished]}"; unset "PIDS[$finished]"
  local tid="${info%%|*}" agent="${info##*|}"
  local safe_agent=${agent/_/-}

  if [[ $code -eq 0 ]]; then
    OK_BY_AGENT[$agent]=$(( OK_BY_AGENT[$agent] + 1 ))
    echo -e "  ${GREEN}[OK]${NC}   $safe_agent  $tid"
  else
    FAIL_BY_AGENT[$agent]=$(( FAIL_BY_AGENT[$agent] + 1 ))
    echo -e "  ${RED}[FAIL]${NC} $safe_agent  $tid  (exit=$code, log=$LOG_DIR/${safe_agent}__${tid}.log)"
  fi
  DONE=$(( DONE + 1 ))
}

echo -e "${CYAN}[Phase 2] Running evaluations...${NC}"
total_jobs=$(( TOTAL * NUM_AGENTS ))
job_idx=0

for td in "${TASKS[@]}"; do
  tid=$(basename "$td")
  for agent in "${AGENTS[@]}"; do
    if $RESUME; then
      # skip if meta_eval.json already exists under any openclaw/<model>/ or claude-code/<model>/
      safe_agent=${agent/_/-}
      shopt -s nullglob
      found=0
      for f in "$td/$safe_agent"/*/meta_eval.json "$td/openclaw"/*/meta_eval.json; do
        [[ -f "$f" ]] && found=1 && break
      done
      shopt -u nullglob
      if [[ $found -eq 1 ]]; then
        echo -e "  ${YELLOW}[SKIP]${NC} $safe_agent  $tid  (meta_eval.json present)"
        DONE=$(( DONE + 1 ))
        continue
      fi
    fi

    # throttle
    while [[ ${#PIDS[@]} -ge $PARALLEL ]]; do
      reap_one
    done
    job_idx=$(( job_idx + 1 ))
    echo -e "  [${job_idx}/${total_jobs}] launch: ${agent}  ${tid}"
    launch_one "$td" "$agent"
  done
done

# drain
while [[ ${#PIDS[@]} -gt 0 ]]; do reap_one; done

# -- Summary -----------------------------------------------------------------
ELAPSED=$(( $(date +%s) - START_TS ))
echo
echo -e "${GREEN}============================================================${NC}"
echo -e "${GREEN}  Batch evaluation complete${NC}"
echo -e "${GREEN}============================================================${NC}"
printf "  Elapsed:   %dm %ds\n" $((ELAPSED/60)) $((ELAPSED%60))
for a in "${AGENTS[@]}"; do
  printf "  %-14s  ok=%d  fail=%d\n" "$a" "${OK_BY_AGENT[$a]}" "${FAIL_BY_AGENT[$a]}"
done
echo "  Log dir:   $LOG_DIR"
echo
