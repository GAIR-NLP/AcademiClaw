FROM agencybench-sandbox

LABEL query="en_rag_course_assistant"
LABEL task="RAG Intelligent Course Assistant System Implementation"

# Switch to official PyPI source
RUN pip3 config set global.index-url https://pypi.org/simple/ && pip3 config set global.timeout 300

# System dependency for pytesseract OCR
RUN apt-get update && apt-get install -y tesseract-ocr && rm -rf /var/lib/apt/lists/*

# Task-specific dependencies
COPY workspace/requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /agencybench
CMD []
