# =============================================================================
# write/report/liyan-query3 - AI Scientific Research Technology/Industry/Policy Analysis Report
# CPU task, requires Python, requests (Judge API)
# Optional: uncomment texlive lines below to compile LaTeX inside the container
# =============================================================================

FROM agencybench-sandbox

LABEL query="en_ai_science_report"
LABEL task="AI Scientific Research Technology, Industry, and Policy Analysis Report"

RUN pip3 install --no-cache-dir requests openai 2>/dev/null || true

# Optional: install LaTeX to compile PDF inside the container (uncomment as needed)
# RUN apt-get update && apt-get install -y --no-install-recommends texlive-latex-base texlive-latex-extra texlive-fonts-recommended \
#     && rm -rf /var/lib/apt/lists/*

WORKDIR /agencybench

CMD []
