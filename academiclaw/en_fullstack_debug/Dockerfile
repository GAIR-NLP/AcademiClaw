# =============================================================================
# Query-specific Dockerfile - German Vocabulary App Frontend-Backend Integration Debug
#
# Task requirements:
#   - Frontend: React + TypeScript + Vite
#   - Backend: FastAPI + Python
#   - Evaluation: Playwright E2E tests
# =============================================================================


# =============================================================================
# Base image selection
# =============================================================================

# CPU task (default)
FROM agencybench-sandbox


# =============================================================================
# Metadata
# =============================================================================

LABEL query="en_fullstack_debug"
LABEL task="German Vocabulary App Frontend-Backend Integration Debug"


# =============================================================================
# Task-specific dependencies
# =============================================================================

# ----- Python backend dependencies (FastAPI) -----
RUN pip3 install --no-cache-dir \
    fastapi \
    uvicorn[standard] \
    pydantic

# ----- Playwright + browser (E2E testing) -----
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


# =============================================================================
# Environment variables
# =============================================================================

ENV PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers


# =============================================================================
# Working directory
# =============================================================================

WORKDIR /agencybench


# =============================================================================
# Important notes
#
# 1. Do not define ENTRYPOINT - the base image already defines the correct entrypoint
# 2. Do not define CMD - unless you have special requirements
# 3. The entrypoint automatically handles:
#    - Preparing the isolated working directory
#    - Copying workspace and context to the isolated directory
#    - Running eval_task.py (with correct arguments)
#    - Copying results back to the host
# =============================================================================

CMD []
