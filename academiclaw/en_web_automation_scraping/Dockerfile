FROM agencybench-sandbox

LABEL query="T51_en_web_automation_scraping"
LABEL task="CSRankings Data Extraction Script"

RUN pip3 install --no-cache-dir playwright && \
    mkdir -p /opt/pw-browsers && \
    PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers playwright install chromium && \
    playwright install-deps chromium

WORKDIR /agencybench

CMD []
