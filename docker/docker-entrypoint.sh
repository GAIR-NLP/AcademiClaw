#!/bin/bash
# =============================================================================
# AgencyBench Docker Entrypoint
# 
# 功能：在完全隔离的环境中运行评估流程
#   1. 验证 Agent 依赖
#   2. 复制 workspace 到隔离目录
#   3. 执行评估脚本
#   4. 复制结果回宿主机挂载目录
#
# 注意：容器以宿主机用户身份运行（通过 --user 参数）
#       所有文件操作都使用宿主机用户权限，无需额外修改文件所有权
#
# 环境变量：
#   QUERY_PATH      - Query 目录路径（相对于 /agencybench）
#   MODEL_NAME      - 模型名称（用于组织输出目录）
#   AGENT_TYPE      - Agent 类型：claude_code, openclaw, manual
#   MAX_ATTEMPTS    - 最大尝试次数（默认 3）
#   EVAL_ONLY       - 仅评估模式（默认 false）
# =============================================================================

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# =============================================================================
# 配置
# =============================================================================

# 确保 HOME 指向可写目录（容器以 --user 运行时，HOME 可能是 / 或不存在）
if [ ! -w "${HOME:-/}" ]; then
    export HOME="/tmp/home_$(id -u)"
    mkdir -p "$HOME"
fi

# 基础路径
AGENCYBENCH_ROOT="/agencybench"
# 使用用户专属的临时目录，避免与其他用户/之前的 root 运行冲突
ISOLATED_WORKSPACE="/tmp/isolated_workspace_$(id -u)"
ISOLATED_OUTPUT="/tmp/isolated_output_$(id -u)"

# 从环境变量读取配置
QUERY_PATH="${QUERY_PATH:-}"
MODEL_NAME="${MODEL_NAME:-unknown_model}"
AGENT_TYPE="${AGENT_TYPE:-manual}"
MAX_ATTEMPTS="${MAX_ATTEMPTS:-1}"
EVAL_ONLY="${EVAL_ONLY:-false}"

# =============================================================================
# 函数定义
# =============================================================================

# 验证必要的环境变量
validate_env() {
    if [ -z "$QUERY_PATH" ]; then
        log_error "QUERY_PATH 环境变量未设置"
        exit 1
    fi
    
    FULL_QUERY_PATH="$AGENCYBENCH_ROOT/$QUERY_PATH"
    if [ ! -d "$FULL_QUERY_PATH" ]; then
        log_error "Query 目录不存在: $FULL_QUERY_PATH"
        exit 1
    fi
    
    log_info "Query 路径: $FULL_QUERY_PATH"
    log_info "模型名称: $MODEL_NAME"
    log_info "Agent 类型: $AGENT_TYPE"
}

# 验证 Agent 依赖
verify_agent_deps() {
    if [ "$AGENT_TYPE" = "claude_code" ]; then
        # Claude Code SDK 需要 claude CLI 二进制
        if command -v claude &> /dev/null; then
            log_success "claude CLI 已安装: $(which claude)"
        else
            log_warn "claude CLI 未安装，claude-code-sdk 可能无法正常工作"
        fi
    elif [ "$AGENT_TYPE" = "openclaw" ]; then
        log_info "OpenClaw Agent 模式: 使用 openclaw CLI (agent --local)"
        if command -v openclaw &> /dev/null; then
            log_success "openclaw CLI 已安装: $(which openclaw)"
        else
            log_warn "openclaw CLI 未安装，请确保已运行 npm install -g openclaw@latest"
        fi
        # 写入 openclaw 配置文件
        mkdir -p ~/.openclaw
        cat > ~/.openclaw/openclaw.json <<OCEOF
{
  "models": {
    "providers": {
      "relay": {
        "baseUrl": "${OPENCLAW_BASE_URL:-https://api.openai.com/v1}",
        "apiKey": "${OPENCLAW_API_KEY:-}",
        "api": "openai-completions",
        "models": [{
          "id": "${OPENCLAW_MODEL:-claude-sonnet-4-6}",
          "name": "${OPENCLAW_MODEL:-claude-sonnet-4-6}",
          "contextWindow": 200000,
          "maxTokens": 8192
        }]
      }
    }
  },
  "agents": {
    "defaults": {
      "workspace": "${ISOLATED_WORKSPACE:-/tmp/isolated_workspace}",
      "model": { "primary": "relay/${OPENCLAW_MODEL:-claude-sonnet-4-6}" },
      "timeoutSeconds": 600
    }
  },
  "gateway": {
    "mode": "local"
  },
  "tools": {
    "exec": { "host": "gateway", "security": "full", "ask": "off" }
  }
}
OCEOF
        log_success "openclaw 配置已写入 ~/.openclaw/openclaw.json"
    elif [ "$AGENT_TYPE" = "manual" ]; then
        log_info "手动模式: 跳过 Agent 依赖检查"
    else
        log_warn "未知的 Agent 类型: $AGENT_TYPE"
    fi
    return 0
}

# 准备隔离的工作目录
prepare_isolated_workspace() {
    log_info "准备隔离的工作目录..."
    log_info "工作目录: $ISOLATED_WORKSPACE"
    log_info "输出目录: $ISOLATED_OUTPUT"

    # 清理旧的隔离目录（忽略错误，可能是权限问题或目录不存在）
    rm -rf "$ISOLATED_WORKSPACE" 2>/dev/null || true
    rm -rf "$ISOLATED_OUTPUT" 2>/dev/null || true
    mkdir -p "$ISOLATED_WORKSPACE" "$ISOLATED_OUTPUT"

    # 注意: workspace/context/.env 的复制由 eval_task.py 负责
    # entrypoint 只负责创建隔离目录并确保权限正确

    log_success "隔离工作目录准备完成: $ISOLATED_WORKSPACE"
}

# 运行评估
run_evaluation() {
    log_info "开始运行评估 (流程: Agent 在隔离目录生成 pipeline → 对同一目录运行 rubric 评估)..."
    
    cd "$FULL_QUERY_PATH"
    
    # 构建 eval_task.py 的参数
    EVAL_ARGS=""
    
    # 添加隔离工作目录参数
    EVAL_ARGS="$EVAL_ARGS --isolated-workspace $ISOLATED_WORKSPACE"
    
    # 添加输出目录参数
    EVAL_ARGS="$EVAL_ARGS --output-dir $ISOLATED_OUTPUT"
    
    # 如果有 .env 文件，加载它（但不覆盖 Docker -e 传入的关键变量）
    if [ -f ".env" ]; then
        log_info "加载 .env 文件"
        # 保存命令行传入的关键变量（优先级高于 .env）
        local _saved_agent_type="$AGENT_TYPE"
        local _saved_model_name="$MODEL_NAME"
        local _saved_max_attempts="$MAX_ATTEMPTS"
        local _saved_eval_only="$EVAL_ONLY"
        set -a
        source .env
        set +a
        # 恢复命令行传入的值（如果非空）
        [ -n "$_saved_agent_type" ] && export AGENT_TYPE="$_saved_agent_type"
        [ -n "$_saved_model_name" ] && export MODEL_NAME="$_saved_model_name"
        [ -n "$_saved_max_attempts" ] && export MAX_ATTEMPTS="$_saved_max_attempts"
        [ -n "$_saved_eval_only" ] && export EVAL_ONLY="$_saved_eval_only"
    fi
    # Fallback: 如果关键评估/Agent变量缺失或为占位符，则尝试从模板回填
    TEMPLATE_ENV="$AGENCYBENCH_ROOT/template_here/.env"
    is_placeholder() {
        case "$1" in
            ""|*"your_"*) return 0 ;;
            *) return 1 ;;
        esac
    }
    load_from_template_if_needed() {
        local key="$1"
        local curr_val="${!key}"
        if is_placeholder "$curr_val"; then
            if [ -f "$TEMPLATE_ENV" ]; then
                local tpl_val
                tpl_val=$(grep -E "^${key}=" "$TEMPLATE_ENV" | head -1 | cut -d= -f2- | sed 's/^"//' | sed 's/"$//' | sed "s/^'\(.*\)'$/\1/")
                if ! is_placeholder "$tpl_val"; then
                    export "$key=$tpl_val"
                    log_info "使用模板 .env 回填 ${key}"
                fi
            fi
        fi
    }
    # 回填常见关键变量（按需增减）
    for k in EVAL_TEXT_API_KEY EVAL_TEXT_API_BASE_URL EVAL_TEXT_MODEL \
             ANTHROPIC_API_KEY ANTHROPIC_BASE_URL CLAUDE_CODE_MODEL \
             OPENCLAW_API_KEY OPENCLAW_BASE_URL OPENCLAW_MODEL; do
        load_from_template_if_needed "$k"
    done
    
    # 设置预装工具的环境变量（如果存在）
    # 这些环境变量会传递给 Agent 执行的命令
    [ -d "/opt/pw-browsers" ] && export PLAYWRIGHT_BROWSERS_PATH="/opt/pw-browsers"
    
    # 仅评估模式
    if [ "$EVAL_ONLY" = "true" ]; then
        EVAL_ARGS="$EVAL_ARGS --eval-only"
    fi
    
    log_info "执行: python3 eval_task.py $EVAL_ARGS"
    
    # 运行评估脚本
    python3 eval_task.py $EVAL_ARGS
    EVAL_EXIT_CODE=$?
    
    if [ $EVAL_EXIT_CODE -eq 0 ]; then
        log_success "评估完成，退出码: $EVAL_EXIT_CODE"
    else
        log_warn "评估完成，退出码: $EVAL_EXIT_CODE"
    fi
    
    return $EVAL_EXIT_CODE
}

# 复制结果回宿主机
copy_results_back() {
    log_info "复制结果回宿主机..."
    
    # 目标目录
    OUTPUT_DIR="$FULL_QUERY_PATH/$MODEL_NAME"
    mkdir -p "$OUTPUT_DIR"
    
    # 复制隔离输出目录的内容
    if [ -d "$ISOLATED_OUTPUT" ] && [ "$(ls -A $ISOLATED_OUTPUT)" ]; then
        log_info "复制输出目录: $ISOLATED_OUTPUT -> $OUTPUT_DIR"
        cp -r "$ISOLATED_OUTPUT"/* "$OUTPUT_DIR/" 2>/dev/null || true
    fi
    
    # 如果隔离工作目录有 meta_eval.json，也复制
    if [ -f "$ISOLATED_OUTPUT/meta_eval.json" ]; then
        log_info "复制 meta_eval.json"
        cp "$ISOLATED_OUTPUT/meta_eval.json" "$OUTPUT_DIR/"
    fi
    
    # 容器以宿主机用户身份运行，文件所有权已经正确，无需修改
    
    log_success "结果已复制到: $OUTPUT_DIR"
    ls -la "$OUTPUT_DIR"
}

# 清理
cleanup() {
    log_info "清理临时文件..."

    # 清理隔离目录（可选，容器销毁时会自动清理）
    # rm -rf "$ISOLATED_WORKSPACE" "$ISOLATED_OUTPUT"

    log_success "清理完成"
}

# 信号处理
trap cleanup EXIT INT TERM

# =============================================================================
# 主流程
# =============================================================================

main() {
    echo "============================================================"
    echo " AgencyBench Docker 隔离评估环境"
    echo "============================================================"
    echo ""
    
    # 1. 验证环境
    validate_env
    
    # 2. 验证 Agent 依赖
    verify_agent_deps
    
    # 3. 准备隔离的工作目录
    prepare_isolated_workspace
    
    # 4. 运行评估
    # 注意: set -e 会导致非零退出码时立即退出
    # 所以需要显式处理退出码，确保后续步骤能执行
    set +e  # 临时禁用 set -e
    run_evaluation
    EVAL_RESULT=$?
    set -e  # 重新启用 set -e
    
    # 5. 复制结果回宿主机 (无论评估是否通过，都需要复制结果)
    copy_results_back
    
    echo ""
    echo "============================================================"
    if [ $EVAL_RESULT -eq 0 ]; then
        log_success "评估流程完成 - 通过"
    else
        log_warn "评估流程完成 - 未通过 (退出码: $EVAL_RESULT)"
    fi
    echo "============================================================"
    
    exit $EVAL_RESULT
}

# 支持直接传入命令（用于调试）
if [ $# -gt 0 ]; then
    exec "$@"
else
    main
fi
