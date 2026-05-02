# Using CUDA base image: when the host has a GPU and runs with -g, Chromium can use GPU for WebGL rendering, avoiding black screen.
# Without GPU or without --gpus all, the evaluation script will automatically fall back to SwiftShader software WebGL.
FROM agencybench-sandbox-cuda

LABEL query="en_blackhole_visualization"
LABEL task="Three.js Black Hole Visualization"

WORKDIR /agencybench

# Chromium dependencies + software WebGL (SwiftShader) needed when no GPU is available
RUN apt-get update && apt-get install -y \
    libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
    libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 \
    libasound2 libpangocairo-1.0-0 libpango-1.0-0 libcairo2 libxshmfence1 \
    libx11-xcb1 libatspi2.0-0 libgtk-3-0 \
    libegl1-mesa libgles2-mesa libgl1-mesa-dri libgl1 libgl1-mesa-dri \
    && rm -rf /var/lib/apt/lists/*

# Evaluation requires Chromium for screenshots (multimodal evaluation: screenshot page + LLM visual comparison)
# Install to /opt/pw-browsers, consistent with entrypoint convention, accessible when container runs as non-root user
RUN pip3 install --no-cache-dir playwright && \
    playwright install-deps chromium && \
    mkdir -p /opt/pw-browsers && \
    PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers playwright install chromium && \
    chmod -R a+rX /opt/pw-browsers

ENV PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers

CMD []
