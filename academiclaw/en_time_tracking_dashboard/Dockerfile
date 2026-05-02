FROM agencybench-sandbox 
 
LABEL query="en_time_tracking_dashboard"
LABEL task="Time Tracking Dashboard Frontend Implementation" 
 
# Task-specific dependencies: frontend testing with Playwright 
RUN apt-get update && apt-get install -y \ 
    unzip \ 
    libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 \ 
    libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 \ 
    libxrandr2 libgbm1 libasound2t64 libpangocairo-1.0-0 libpango-1.0-0 \ 
    libcairo2 libxshmfence1 libx11-xcb1 libatspi2.0-0 libgtk-3-0 \ 
    && rm -rf /var/lib/apt/lists/* 
 
RUN npm install -g playwright && \ 
    mkdir -p /opt/pw-browsers && \ 
    PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers playwright install chromium && \ 
    playwright install-deps chromium 
 
WORKDIR /agencybench 
CMD [] 
