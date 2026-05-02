#!/bin/bash
# =============================================================================
# AcademiClaw — Batch build of per-task Docker images
#
# Walks the `academiclaw/` directory tree, ensures the two base images
# (agencybench-sandbox for CPU, agencybench-sandbox-cuda for GPU) exist,
# then builds a per-task image for every task that ships its own
# Dockerfile (or Dockerfile.cuda).
#
# Usage:
#   ./build_all_images.sh                 # default: 8 parallel builds
#   ./build_all_images.sh -j 16           # 16 parallel builds
#   ./build_all_images.sh --rebuild       # force rebuild everything
#   ./build_all_images.sh --only en_cmo_proof,en_bibtex_reference_gen
#                                         # only build selected tasks
#   ./build_all_images.sh --gpu-only      # only GPU tasks
#   ./build_all_images.sh --cpu-only      # only CPU tasks
#
# Image names:
#   - CPU base:   agencybench-sandbox
#   - GPU base:   agencybench-sandbox-cuda
#   - Per-task:   agencybench-academiclaw-<task_id>
# =============================================================================

set -eo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
log_info()    { echo -e "${BLUE}[INFO]${NC} $1"; }
log_ok()      { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn()    { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error()   { echo -e "${RED}[ERROR]${NC} $1"; }

PARALLEL=8
REBUILD=false
ONLY_FILTER=""
MODE="all"   # all | cpu | gpu

while [[ $# -gt 0 ]]; do
  case $1 in
    -j|--parallel) PARALLEL="$2"; shift 2 ;;
    --rebuild)     REBUILD=true; shift ;;
    --only)        ONLY_FILTER="$2"; shift 2 ;;
    --cpu-only)    MODE="cpu"; shift ;;
    --gpu-only)    MODE="gpu"; shift ;;
    -h|--help)
      sed -n '3,24p' "$0"
      exit 0 ;;
    *) log_error "Unknown arg: $1"; exit 1 ;;
  esac
done

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_ROOT"
TASK_ROOT="$PROJECT_ROOT/academiclaw"
DOCKER_DIR="$PROJECT_ROOT/docker"
LOG_DIR="/tmp/academiclaw_build_logs"
mkdir -p "$LOG_DIR"

# -- is_gpu_task: four-heuristic GPU detector (matches the paper) ------------
is_gpu_task() {
  local dir="$1"
  if [[ -f "$dir/Dockerfile.cuda" ]]; then return 0; fi
  if [[ -f "$dir/Dockerfile" ]] && \
     grep -qE "FROM\s+(agencybench-sandbox-cuda|nvidia/cuda)" "$dir/Dockerfile"; then
    return 0
  fi
  if find "$dir/context" -maxdepth 3 -name '*.cu' 2>/dev/null | grep -q .; then
    return 0
  fi
  if [[ -f "$dir/.env.example" ]] && \
     grep -qiE "CUDA|GPU_ENABLED" "$dir/.env.example"; then
    return 0
  fi
  return 1
}

# -- Phase 0: base images ----------------------------------------------------
build_base() {
  local tag="$1" df="$2"
  if [[ "$REBUILD" != "true" ]] && [[ -n "$(docker images -q "$tag" 2>/dev/null)" ]]; then
    log_ok "Base image present: $tag (skip)"
    return 0
  fi
  log_info "Building base image: $tag"
  docker build -t "$tag" -f "$DOCKER_DIR/$df" "$DOCKER_DIR"
  log_ok "Built: $tag"
}

log_info "Phase 0 — Base images"
if [[ "$MODE" != "gpu" ]]; then
  build_base "agencybench-sandbox" "Dockerfile"
fi
if [[ "$MODE" != "cpu" ]]; then
  # only build cuda base if we have any .cuda dockerfile OR user forced gpu mode
  if [[ "$MODE" == "gpu" ]] || find "$TASK_ROOT" -maxdepth 2 -name 'Dockerfile.cuda' | grep -q .; then
    build_base "agencybench-sandbox-cuda" "Dockerfile.cuda"
  fi
fi
echo

# -- Collect tasks -----------------------------------------------------------
IFS=',' read -ra ONLY_ARR <<< "$ONLY_FILTER"
declare -a TASKS=()
for task_dir in "$TASK_ROOT"/*/; do
  task_id=$(basename "$task_dir")
  # skip non-task directories (e.g. QUERY_CATALOG.md lives at the same depth)
  [[ ! -f "$task_dir/description.json" ]] && continue

  # --only filter
  if [[ -n "$ONLY_FILTER" ]]; then
    local_keep=false
    for k in "${ONLY_ARR[@]}"; do [[ "$k" == "$task_id" ]] && local_keep=true; done
    $local_keep || continue
  fi

  # CPU/GPU filter
  if is_gpu_task "$task_dir"; then
    [[ "$MODE" == "cpu" ]] && continue
  else
    [[ "$MODE" == "gpu" ]] && continue
  fi

  TASKS+=("$task_dir")
done

TOTAL=${#TASKS[@]}
log_info "Phase 1 — Per-task images (parallel=$PARALLEL, total=$TOTAL)"
echo

build_one() {
  local task_dir="$1" idx="$2" total="$3"
  local task_id; task_id=$(basename "$task_dir")
  local image="agencybench-academiclaw-$task_id"
  local log="$LOG_DIR/$task_id.log"

  # pick Dockerfile
  local df
  if [[ -f "$task_dir/Dockerfile.cuda" ]]; then
    df="$task_dir/Dockerfile.cuda"
  elif [[ -f "$task_dir/Dockerfile" ]]; then
    df="$task_dir/Dockerfile"
  else
    printf "[%d/%d] %bSKIP%b %-40s (no Dockerfile)\n" "$idx" "$total" "$YELLOW" "$NC" "$task_id"
    return 0
  fi

  if [[ "$REBUILD" != "true" ]] && [[ -n "$(docker images -q "$image" 2>/dev/null)" ]]; then
    printf "[%d/%d] %bCACHED%b %-40s\n" "$idx" "$total" "$GREEN" "$NC" "$task_id"
    return 0
  fi

  if docker build -t "$image" -f "$df" "$task_dir" > "$log" 2>&1; then
    printf "[%d/%d] %bOK%b    %-40s -> %s\n" "$idx" "$total" "$GREEN" "$NC" "$task_id" "$image"
  else
    printf "[%d/%d] %bFAIL%b  %-40s (see %s)\n" "$idx" "$total" "$RED" "$NC" "$task_id" "$log"
    return 1
  fi
}
export -f build_one; export LOG_DIR REBUILD GREEN RED YELLOW NC

declare -A PIDS
FAIL_COUNT=0
for i in "${!TASKS[@]}"; do
  # throttle
  while [[ ${#PIDS[@]} -ge $PARALLEL ]]; do
    for pid in "${!PIDS[@]}"; do
      if ! kill -0 "$pid" 2>/dev/null; then
        wait "$pid" 2>/dev/null || FAIL_COUNT=$((FAIL_COUNT+1))
        unset "PIDS[$pid]"
      fi
    done
    (( ${#PIDS[@]} >= PARALLEL )) && sleep 0.3
  done
  build_one "${TASKS[$i]}" "$((i+1))" "$TOTAL" &
  PIDS[$!]=1
done
for pid in "${!PIDS[@]}"; do
  wait "$pid" 2>/dev/null || FAIL_COUNT=$((FAIL_COUNT+1))
done

echo
if [[ $FAIL_COUNT -eq 0 ]]; then
  log_ok "All images built successfully ($TOTAL tasks)"
else
  log_warn "$FAIL_COUNT task(s) failed — build logs in $LOG_DIR/"
  exit 1
fi
