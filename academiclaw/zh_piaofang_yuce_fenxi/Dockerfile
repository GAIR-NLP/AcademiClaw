# =============================================================================
# Query 专属 Dockerfile
# Task: predict/box-office/query5 - 分析并预测电影《阿凡达：火与烬》的票房表现
#
# 该任务需要:
#   - Playwright + Chromium: 访问票房数据网站采集实时数据
#   - openai: rubric中的LLM评估（分析质量和预测质量评分）
#   - requests/beautifulsoup4: 辅助网页数据采集
# =============================================================================


# =============================================================================
# 选择基础镜像
# =============================================================================

# CPU 任务（默认）- 数据采集和分析无需GPU
FROM agencybench-sandbox


# =============================================================================
# 元数据
# =============================================================================

LABEL query="T37_zh_piaofang_yuce_fenxi"
LABEL task="分析并预测电影《阿凡达：火与烬》的票房表现"


# =============================================================================
# 任务特定依赖
# =============================================================================

# openai 用于 rubric LLM评估（分析质量和预测质量评分）
# beautifulsoup4 和 lxml 用于辅助网页数据解析
RUN pip3 install --no-cache-dir \
    openai \
    beautifulsoup4 \
    lxml

# ----- Playwright + 浏览器（用于访问票房网站采集数据） -----
# 该任务需要访问猫眼、Box Office Mojo等网站获取实时票房数据
RUN apt-get update && apt-get install -y \
    libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 \
    libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 \
    libxrandr2 libgbm1 libasound2t64 libpangocairo-1.0-0 libpango-1.0-0 \
    libcairo2 libxshmfence1 libx11-xcb1 libatspi2.0-0 libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*
RUN pip3 install --no-cache-dir playwright && \
    mkdir -p /opt/pw-browsers && \
    PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers playwright install chromium && \
    playwright install-deps chromium

# 设置 Playwright 浏览器路径
ENV PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers


# =============================================================================
# 环境变量（可选）
# =============================================================================

# ENV MY_VAR=value


# =============================================================================
# 工作目录
# =============================================================================

WORKDIR /agencybench


# =============================================================================
# 重要提醒
#
# 1. 不要定义 ENTRYPOINT - 基础镜像已经定义了正确的 entrypoint
# 2. 不要定义 CMD - 除非你有特殊需求
# 3. entrypoint 会自动处理:
#    - 准备隔离的工作目录
#    - 复制 workspace 和 context 到隔离目录
#    - 运行 eval_task.py（带正确的参数）
#    - 复制结果回宿主机
# =============================================================================

CMD []
