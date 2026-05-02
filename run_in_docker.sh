#!/bin/bash

# =============================================================================
# AgencyBench Docker Runner
# 用于在完全隔离的 Docker 环境中运行评估任务
# 
# 支持两种模式:
#   1. 通用环境: 使用 docker/Dockerfile 构建的基础镜像
#   2. 专用环境: 使用 query 目录下的 Dockerfile 构建的专属镜像
#
# 隔离保证:
#   - Agent 只能访问隔离的 /tmp/isolated_workspace 目录
#   - 评估结果复制回宿主机的 query 目录
#   - 容器以宿主机用户身份运行，所有文件操作都使用宿主机用户权限
# =============================================================================

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# =============================================================================
# 配置
# =============================================================================

BASE_DOCKERFILE_DIR="$(dirname "$0")/docker"
PROJECT_ROOT=$(pwd)

# 默认配置（可通过环境变量覆盖）
MODEL_NAME="${MODEL_NAME:-}"
AGENT_TYPE="${AGENT_TYPE:-}"
MAX_ATTEMPTS="${MAX_ATTEMPTS:-1}"
REBUILD_IMAGE="${REBUILD_IMAGE:-false}"
NETWORK_MODE="${NETWORK_MODE:-bridge}"
EVAL_ONLY="${EVAL_ONLY:-false}"
DEBUG_MODE="${DEBUG_MODE:-false}"
GPU_ENABLED="${GPU_ENABLED:-auto}"  # auto, true, false

# =============================================================================
# 帮助信息
# =============================================================================

show_help() {
    cat << EOF
用法: ./run_in_docker.sh [选项] <Query目录路径>

参数:
    <Query目录路径>     相对于项目根目录的 Query 路径
                       示例: AgencyBench-v3/write/code/query1

选项:
    -h, --help          显示此帮助信息
    -m, --model NAME    指定模型名称 (默认从 .env 读取)
    -a, --agent TYPE    Agent 类型: claude_code, openclaw, manual
    -n, --attempts N    最大尝试次数 (默认: 3)
    -r, --rebuild       强制重新构建 Docker 镜像
    -e, --eval-only     仅评估模式，不运行 Agent
    -g, --gpu           启用 GPU 支持 (CUDA 任务需要)
    --no-gpu            禁用 GPU 支持
    --network MODE      网络模式: host, bridge, none (默认: bridge)
    --debug             调试模式，进入容器 shell

环境变量:
    MODEL_NAME          模型名称
    AGENT_TYPE          Agent 类型
    MAX_ATTEMPTS        最大尝试次数
    REBUILD_IMAGE       是否重新构建镜像 (true/false)
    NETWORK_MODE        网络模式
    EVAL_ONLY           仅评估模式 (true/false)
    DEBUG_MODE          调试模式 (true/false)
    GPU_ENABLED         GPU 支持: auto, true, false (默认: auto)

示例:
    # 基本用法
    ./run_in_docker.sh AgencyBench-v3/write/code/query1

    # 指定模型和 Agent 类型
    ./run_in_docker.sh -m claude-sonnet-4-20250514 -a claude_code AgencyBench-v3/write/code/query1

    # 强制重新构建镜像
    ./run_in_docker.sh -r AgencyBench-v3/write/code/query1

    # 仅评估模式
    ./run_in_docker.sh -e AgencyBench-v3/write/code/query1

    # 启用 GPU 支持 (CUDA 任务)
    ./run_in_docker.sh -g AgencyBench-v3/implement/code/yiwang-query1

    # 调试模式 - 进入容器 shell
    ./run_in_docker.sh --debug AgencyBench-v3/write/code/query1

EOF
    exit 0
}

# =============================================================================
# 参数解析
# =============================================================================

QUERY_PATH=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            ;;
        -m|--model)
            MODEL_NAME="$2"
            shift 2
            ;;
        -a|--agent)
            AGENT_TYPE="$2"
            shift 2
            ;;
        -n|--attempts)
            MAX_ATTEMPTS="$2"
            shift 2
            ;;
        -r|--rebuild)
            REBUILD_IMAGE="true"
            shift
            ;;
        -e|--eval-only)
            EVAL_ONLY="true"
            shift
            ;;
        -g|--gpu)
            GPU_ENABLED="true"
            shift
            ;;
        --no-gpu)
            GPU_ENABLED="false"
            shift
            ;;
        --network)
            NETWORK_MODE="$2"
            shift 2
            ;;
        --debug)
            DEBUG_MODE="true"
            shift
            ;;
        -*)
            log_error "未知选项: $1"
            show_help
            ;;
        *)
            QUERY_PATH="$1"
            shift
            ;;
    esac
done

# =============================================================================
# 验证
# =============================================================================

# 检查 Docker 是否可用
if ! command -v docker &> /dev/null; then
    log_error "未找到 Docker。请先安装 Docker。"
    exit 1
fi

# 检查 Query 路径
if [ -z "$QUERY_PATH" ]; then
    log_error "请指定 Query 目录路径"
    show_help
fi

# 移除尾部斜杠
QUERY_PATH="${QUERY_PATH%/}"

# 确保路径存在
if [ ! -d "$QUERY_PATH" ]; then
    log_error "目录不存在: $QUERY_PATH"
    exit 1
fi

# 确保 eval_task.py 存在
if [ ! -f "$QUERY_PATH/eval_task.py" ]; then
    log_error "未找到评估脚本: $QUERY_PATH/eval_task.py"
    exit 1
fi

# =============================================================================
# 读取 .env 配置
# =============================================================================

ENV_FILE="$QUERY_PATH/.env"
if [ -f "$ENV_FILE" ]; then
    log_info "读取配置文件: $ENV_FILE"
    
    # 读取 AGENT_TYPE（如果未通过命令行指定）
    if [ -z "$AGENT_TYPE" ]; then
        AGENT_TYPE=$(grep -E "^AGENT_TYPE=" "$ENV_FILE" | cut -d= -f2 | tr -d '"'"'" || echo "manual")
    fi
    
# 读取 MODEL_NAME（如果未通过命令行指定）
    # 根据 AGENT_TYPE 选择正确的模型名称
    if [ -z "$MODEL_NAME" ]; then
        # MODEL_OVERRIDE 环境变量优先（用于并行跑不同模型）
        if [ -n "${MODEL_OVERRIDE:-}" ]; then
            MODEL_NAME="$MODEL_OVERRIDE"
        else
            case "$AGENT_TYPE" in
            claude_code)
                MODEL_NAME=$(grep -E "^CLAUDE_CODE_MODEL=" "$ENV_FILE" | cut -d= -f2 | tr -d '"'"'" || echo "")
                ;;
            openclaw)
                MODEL_NAME=$(grep -E "^OPENCLAW_MODEL=" "$ENV_FILE" | cut -d= -f2 | tr -d '"'"'" || echo "")
                ;;
            manual)
                MODEL_NAME=$(grep -E "^MANUAL_MODEL_NAME=" "$ENV_FILE" | cut -d= -f2 | tr -d '"'"'" || echo "")
                ;;
            *)
                MODEL_NAME=$(grep -E "^MODEL_NAME=" "$ENV_FILE" | cut -d= -f2 | tr -d '"'"'" || echo "")
                ;;
        esac

        # 如果还是空的，尝试通用的 MODEL_NAME
        if [ -z "$MODEL_NAME" ]; then
            MODEL_NAME=$(grep -E "^MODEL_NAME=" "$ENV_FILE" | cut -d= -f2 | tr -d '"'"'" || echo "")
        fi
        fi
    fi
fi

# 设置默认值
MODEL_NAME="${MODEL_NAME:-unknown_model}"
AGENT_TYPE="${AGENT_TYPE:-manual}"

# 生成安全的目录名: <agent_type>/<model_name> (两层目录)
# 这样同一模型在不同 scaffold 下的结果不会互相覆盖
SAFE_MODEL_NAME=$(echo "$MODEL_NAME" | sed 's/[^a-zA-Z0-9._-]/_/g')
SAFE_AGENT_TYPE=$(echo "$AGENT_TYPE" | sed 's/_/-/g; s/[^a-zA-Z0-9._-]/_/g')
RUN_DIR_NAME="${SAFE_AGENT_TYPE}/${SAFE_MODEL_NAME}"

log_info "模型名称: $MODEL_NAME"
log_info "Agent 类型: $AGENT_TYPE"
log_info "输出目录名: $RUN_DIR_NAME"
log_info "最大尝试次数: $MAX_ATTEMPTS"

# =============================================================================
# 构建 Docker 镜像
# =============================================================================

# CPU 基础镜像
BASE_IMAGE_NAME="agencybench-sandbox"
# CUDA 基础镜像
CUDA_BASE_IMAGE_NAME="agencybench-sandbox-cuda"

ensure_base_image() {
    local image_name="$1"
    local dockerfile_name="$2"
    local need_build=false
    
    if [ "$REBUILD_IMAGE" = "true" ]; then
        log_info "强制重新构建基础镜像 ($image_name)..."
        need_build=true
    elif [[ "$(docker images -q $image_name 2> /dev/null)" == "" ]]; then
        log_info "基础镜像 ($image_name) 不存在，开始构建..."
        need_build=true
    fi
    
    if [ "$need_build" = "true" ]; then
        log_info "正在构建基础镜像 ($image_name)... 这可能需要几分钟。"
        docker build -t $image_name -f "$BASE_DOCKERFILE_DIR/$dockerfile_name" "$BASE_DOCKERFILE_DIR"
        if [ $? -ne 0 ]; then
            log_error "基础镜像 ($image_name) 构建失败。"
            exit 1
        fi
        log_success "基础镜像 ($image_name) 构建成功。"
    fi
}

# 确定使用哪个 Dockerfile
QUERY_DOCKERFILE="$QUERY_PATH/Dockerfile"
if [ -f "$QUERY_DOCKERFILE" ]; then
    log_info "检测到 Query 专属 Dockerfile: $QUERY_DOCKERFILE"
    
    # 检查 Dockerfile 继承自哪个基础镜像（只匹配非注释的 FROM 行）
    if grep -E "^[[:space:]]*FROM[[:space:]]+(agencybench-sandbox-cuda|$CUDA_BASE_IMAGE_NAME)" "$QUERY_DOCKERFILE" | grep -v "^[[:space:]]*#" | head -1 | grep -q .; then
        log_info "Query Dockerfile 继承自 CUDA 基础镜像，确保 CUDA 基础镜像存在..."
        ensure_base_image "$CUDA_BASE_IMAGE_NAME" "Dockerfile.cuda"
    elif grep -E "^[[:space:]]*FROM[[:space:]]+(agencybench-sandbox|$BASE_IMAGE_NAME)" "$QUERY_DOCKERFILE" | grep -v "^[[:space:]]*#" | head -1 | grep -q .; then
        log_info "Query Dockerfile 继承自 CPU 基础镜像，确保 CPU 基础镜像存在..."
        ensure_base_image "$BASE_IMAGE_NAME" "Dockerfile"
    fi
    
    # 根据 query 路径生成唯一镜像名称
    QUERY_IMAGE_NAME="agencybench-$(echo "$QUERY_PATH" | sed 's/[^a-zA-Z0-9._-]/-/g' | tr '[:upper:]' '[:lower:]')"
    IMAGE_NAME="$QUERY_IMAGE_NAME"
    
    # 检查是否需要构建
    NEED_BUILD=false
    if [ "$REBUILD_IMAGE" = "true" ]; then
        NEED_BUILD=true
    elif [[ "$(docker images -q $IMAGE_NAME 2> /dev/null)" == "" ]]; then
        NEED_BUILD=true
    fi
    
    if [ "$NEED_BUILD" = "true" ]; then
        log_info "正在构建 Query 专属镜像 ($IMAGE_NAME)..."
        docker build -t $IMAGE_NAME "$QUERY_PATH"
        if [ $? -ne 0 ]; then
            log_error "Query 专属镜像构建失败。"
            exit 1
        fi
        log_success "Query 专属镜像构建成功。"
    else
        log_info "使用已存在的 Query 专属镜像: $IMAGE_NAME"
    fi
else
    log_info "未检测到 Query 专属 Dockerfile，使用通用基础镜像。"
    IMAGE_NAME="$BASE_IMAGE_NAME"
    ensure_base_image "$BASE_IMAGE_NAME" "Dockerfile"
fi

# =============================================================================
# 准备输出目录
# =============================================================================

OUTPUT_DIR="$QUERY_PATH/$RUN_DIR_NAME"
mkdir -p "$OUTPUT_DIR"
log_info "输出目录: $OUTPUT_DIR"

# =============================================================================
# GPU 支持检测
# =============================================================================

detect_gpu_requirement() {
    # 检测任务是否需要 GPU
    local requires_gpu=false
    
    # 方法 1: 检查 Dockerfile 是否使用 CUDA 镜像（只匹配非注释的 FROM 行）
    if [ -f "$QUERY_DOCKERFILE" ]; then
        if grep -E "^[[:space:]]*FROM[[:space:]]+.*(nvidia/cuda|agencybench-sandbox-cuda)" "$QUERY_DOCKERFILE" | grep -v "^[[:space:]]*#" | head -1 | grep -q .; then
            requires_gpu=true
            log_info "检测到 Dockerfile 使用 CUDA 镜像" >&2
        fi
    fi
    
    # 方法 2: 检查目录中是否有 .cu 文件
    if find "$QUERY_PATH" -name "*.cu" -type f 2>/dev/null | head -1 | grep -q .; then
        requires_gpu=true
        log_info "检测到 CUDA 源代码文件 (.cu)" >&2
    fi
    
    # 方法 3: 检查 .env 中是否有 CUDA 相关配置
    if [ -f "$ENV_FILE" ]; then
        if grep -qi "CUDA" "$ENV_FILE" || grep -qi "GPU" "$ENV_FILE"; then
            requires_gpu=true
            log_info "检测到 .env 中有 CUDA/GPU 配置" >&2
        fi
    fi
    
    # 方法 4: 检查 query.md 或 description.json 中是否提到 CUDA
    if [ -f "$QUERY_PATH/workspace/query.md" ]; then
        if grep -qi "cuda\|nvcc\|gpu" "$QUERY_PATH/workspace/query.md"; then
            requires_gpu=true
            log_info "检测到任务描述中提到 CUDA/GPU" >&2
        fi
    fi
    if [ -f "$QUERY_PATH/description.json" ]; then
        if grep -qi "cuda\|nvcc\|gpu" "$QUERY_PATH/description.json"; then
            requires_gpu=true
            log_info "检测到任务描述中提到 CUDA/GPU" >&2
        fi
    fi
    
    echo "$requires_gpu"
}

check_gpu_available() {
    # 检查宿主机是否有可用的 GPU
    if command -v nvidia-smi &> /dev/null; then
        if nvidia-smi &> /dev/null; then
            return 0  # GPU 可用
        fi
    fi
    return 1  # GPU 不可用
}

# 确定是否启用 GPU
GPU_ARGS=""
if [ "$GPU_ENABLED" = "auto" ]; then
    REQUIRES_GPU=$(detect_gpu_requirement)
    if [ "$REQUIRES_GPU" = "true" ]; then
        if check_gpu_available; then
            GPU_ENABLED="true"
            log_info "自动检测: 任务需要 GPU，且 GPU 可用，启用 GPU 支持"
        else
            log_warn "自动检测: 任务需要 GPU，但宿主机没有可用的 GPU"
            log_warn "评测可能会失败，建议在有 GPU 的机器上运行"
            GPU_ENABLED="false"
        fi
    else
        GPU_ENABLED="false"
        log_info "自动检测: 任务不需要 GPU"
    fi
fi

if [ "$GPU_ENABLED" = "true" ]; then
    if check_gpu_available; then
        # 并行运行时每个容器只分配 1 张 GPU，通过容器名 hash 轮询
        GPU_COUNT=$(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null | wc -l)
        if [ "$GPU_COUNT" -gt 1 ]; then
            GPU_HASH=$(echo "$CONTAINER_NAME" | cksum | awk '{print $1}')
            GPU_ID=$((GPU_HASH % GPU_COUNT))
            GPU_ARGS="--gpus device=$GPU_ID"
            log_success "GPU 支持已启用 (GPU $GPU_ID/$GPU_COUNT)"
        else
            GPU_ARGS="--gpus all"
            log_success "GPU 支持已启用 (--gpus all)"
        fi
    else
        log_error "请求启用 GPU，但宿主机没有可用的 GPU"
        log_error "请确保:"
        log_error "  1. 宿主机安装了 NVIDIA GPU"
        log_error "  2. 安装了 NVIDIA 驱动 (nvidia-smi 可正常运行)"
        log_error "  3. 安装了 NVIDIA Container Toolkit"
        exit 1
    fi
fi

# =============================================================================
# 运行容器
# =============================================================================

CONTAINER_NAME="agencybench-$(date +%s)-$$"

echo ""
echo "============================================================"
echo " AgencyBench Docker 隔离评估"
echo "============================================================"
echo " 容器名称:   $CONTAINER_NAME"
echo " 使用镜像:   $IMAGE_NAME"
echo " Query路径:  $QUERY_PATH"
echo " 输出目录:   $OUTPUT_DIR"
echo " 网络模式:   $NETWORK_MODE"
echo " GPU 支持:   $([ "$GPU_ENABLED" = "true" ] && echo "启用" || echo "禁用")"
echo "============================================================"
echo ""

# 检测是否有 TTY
DOCKER_FLAGS=()
if [ -t 0 ]; then
    DOCKER_FLAGS=(-it)
fi

# 构建环境变量参数
# 注意: --env-file 必须在 -e 之前，这样命令行 -e 参数可以覆盖 .env 文件的值
ENV_ARGS=()

# 先加载 .env 文件（作为基础配置）
if [ -f "$ENV_FILE" ]; then
    ENV_ARGS+=(--env-file "$ENV_FILE")
fi

# 再用 -e 覆盖（命令行参数优先级更高）
ENV_ARGS+=(-e "QUERY_PATH=$QUERY_PATH")
ENV_ARGS+=(-e "MODEL_NAME=$RUN_DIR_NAME")
ENV_ARGS+=(-e "AGENT_TYPE=$AGENT_TYPE")
ENV_ARGS+=(-e "MAX_ATTEMPTS=$MAX_ATTEMPTS")
ENV_ARGS+=(-e "EVAL_ONLY=$EVAL_ONLY")

# MODEL_OVERRIDE: 覆盖容器内的模型名（用于并行跑不同模型）
if [ -n "${MODEL_OVERRIDE:-}" ]; then
    ENV_ARGS+=(-e "OPENCLAW_MODEL=$MODEL_OVERRIDE")
    ENV_ARGS+=(-e "CLAUDE_CODE_MODEL=$MODEL_OVERRIDE")
fi

# 构建挂载参数
# 只挂载整个项目目录，entrypoint 脚本会处理隔离
MOUNT_ARGS=(-v "$PROJECT_ROOT:/agencybench")

# 以宿主机用户身份运行容器，所有文件操作都使用宿主机用户权限
# 这样容器内创建的文件不需要额外修改所有权
ENV_ARGS+=(--user "$(id -u):$(id -g)")

# 调试模式
if [ "$DEBUG_MODE" = "true" ]; then
    log_info "调试模式 - 进入容器 shell"
    docker run --rm "${DOCKER_FLAGS[@]}" \
        --name $CONTAINER_NAME \
        --network $NETWORK_MODE \
        $GPU_ARGS \
        "${ENV_ARGS[@]}" \
        "${MOUNT_ARGS[@]}" \
        --entrypoint /bin/bash \
        $IMAGE_NAME
    exit $?
fi

# 正常运行模式
log_info "启动评估容器..."

# 构建运行命令
# 检查专属 Dockerfile 是否定义了自己的 ENTRYPOINT
# 如果有自定义 ENTRYPOINT 且支持 eval 命令，则传递 eval
# 否则不传递命令，让基础镜像的 main 函数执行
RUN_CMD=""
if [ -f "$QUERY_DOCKERFILE" ]; then
    # 检查 Dockerfile 是否定义了 ENTRYPOINT
    if grep -qi "^ENTRYPOINT" "$QUERY_DOCKERFILE"; then
        # 有自定义 ENTRYPOINT，传递 eval 命令
        RUN_CMD="eval"
        log_info "检测到专属 ENTRYPOINT，使用 eval 命令"
    else
        # 继承基础镜像的 ENTRYPOINT，不传递命令
        log_info "使用基础镜像的 ENTRYPOINT"
    fi
fi

docker run --rm "${DOCKER_FLAGS[@]}" \
    --name $CONTAINER_NAME \
    --network $NETWORK_MODE \
    $GPU_ARGS \
    "${ENV_ARGS[@]}" \
    "${MOUNT_ARGS[@]}" \
    $IMAGE_NAME \
    $RUN_CMD

EXIT_CODE=$?

echo ""
echo "============================================================"
if [ $EXIT_CODE -eq 0 ]; then
    log_success "评估完成 - 通过"
else
    log_warn "评估完成 - 未通过 (退出码: $EXIT_CODE)"
fi
echo " 结果保存在: $OUTPUT_DIR"
echo "============================================================"

exit $EXIT_CODE
