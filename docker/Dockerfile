# =============================================================================
# AgencyBench-v3 Docker Sandbox
#
# 功能：在完全隔离的环境中运行整个评估流程
#       包括 Agent 分析、规划、执行和评估
#       支持 Claude Code 和 OpenClaw Agent
#
# 构建命令: docker build -t agencybench-sandbox ./docker
# =============================================================================

FROM ubuntu:24.04

# 设置环境变量
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV TZ=Asia/Shanghai
ENV PYTHONUNBUFFERED=1
ENV PATH="/usr/local/bin:/root/.local/bin:${PATH}"

# 设置时区
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 更换 Ubuntu 镜像源为阿里云（加速国内构建）
# Ubuntu 24.04 使用 deb822 格式的 sources 文件
RUN sed -i 's|http://archive.ubuntu.com/ubuntu/|http://mirrors.aliyun.com/ubuntu/|g' /etc/apt/sources.list.d/ubuntu.sources 2>/dev/null || \
    sed -i 's@/archive.ubuntu.com/@/mirrors.aliyun.com/@g' /etc/apt/sources.list 2>/dev/null || true
RUN sed -i 's|http://security.ubuntu.com/ubuntu/|http://mirrors.aliyun.com/ubuntu/|g' /etc/apt/sources.list.d/ubuntu.sources 2>/dev/null || \
    sed -i 's@/security.ubuntu.com/@/mirrors.aliyun.com/@g' /etc/apt/sources.list 2>/dev/null || true

# 安装基础工具和系统依赖
RUN apt-get update && apt-get install -y \
    # 基础工具
    python3 \
    python3-pip \
    python3-venv \
    git \
    wget \
    curl \
    vim \
    jq \
    unzip \
    zip \
    ca-certificates \
    gnupg \
    # 编译工具
    build-essential \
    gcc \
    g++ \
    make \
    cmake \
    # 常用系统库
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    # 字体（用于生成图表等）
    fonts-noto-cjk \
    fonts-liberation \
    # 网络工具
    iputils-ping \
    net-tools \
    # 进程管理
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# 安装 Node.js 22+ (Claude Code CLI 要求, OpenClaw 要求 >= 22.16.0)
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# 验证 Python 和 Node.js 版本
RUN python3 --version && node --version && npm --version

# 配置 npm 镜像源（加速国内构建）
RUN npm config set registry https://registry.npmmirror.com

# 安装 Claude Code CLI (claude-code-sdk Python 包需要此 CLI 二进制)
RUN npm install -g @anthropic-ai/claude-code --registry https://registry.npmjs.org && \
    claude --version

# 安装 OpenClaw CLI (openclaw agent --local 模式需要此 CLI)
RUN npm install -g openclaw@latest --registry https://registry.npmjs.org && \
    openclaw --version

# 配置 pip 镜像源（Ubuntu 24.04 自带 pip 24.0，不升级）
# Ubuntu 24.04 (PEP 668) 需要 --break-system-packages
RUN pip3 config set global.index-url https://mirrors.aliyun.com/pypi/simple/ && \
    pip3 config set global.break-system-packages true

# 复制 requirements.txt 并安装所有依赖
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

# 安装额外的 Python 依赖
RUN pip3 install --no-cache-dir \
    python-dotenv \
    anthropic>=0.18.0 \
    openai>=1.0.0 \
    rich>=13.0.0

# 创建脚本目录并复制启动脚本
RUN mkdir -p /scripts /tmp/isolated_workspace /tmp/isolated_output

# 复制 entrypoint 脚本
COPY docker-entrypoint.sh /scripts/docker-entrypoint.sh
RUN chmod +x /scripts/docker-entrypoint.sh

# 设置工作目录
WORKDIR /agencybench

# 默认入口点 - 使用我们的隔离启动脚本
ENTRYPOINT ["/scripts/docker-entrypoint.sh"]

# 默认命令（可被覆盖）
CMD []
