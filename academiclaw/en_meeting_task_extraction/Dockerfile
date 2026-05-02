# =============================================================================
# Query 2: Extract Task List from Meeting Minutes - Dockerfile
#
# Task type: NLP Text Processing + Structured Information Extraction
# Base image: agencybench-sandbox (CPU)
#
# Task requirements:
#   - Extract action items from meeting transcription text
#   - Model task dependency relationships (DAG)
#   - Requires NLP processing capability and graph algorithm libraries
#
# Dependency notes:
#   - networkx: for DAG validation and graph operations
#   - Other NLP libraries can be optionally installed as needed (base image includes common libraries)
# =============================================================================


# =============================================================================
# Base Image
# =============================================================================

FROM agencybench-sandbox


# =============================================================================
# Metadata
# =============================================================================

LABEL query="en_meeting_task_extraction"
LABEL task="Extract Task List from Meeting Minutes"


# =============================================================================
# Task-Specific Dependencies
# =============================================================================

# Install graph algorithm library (for DAG validation)
RUN pip3 install --no-cache-dir \
    networkx

# Optional: uncomment below if more advanced NLP processing is needed
# RUN pip3 install --no-cache-dir \
#     spacy \
#     nltk \
#     transformers

# Optional: uncomment below if datetime parsing is needed
# RUN pip3 install --no-cache-dir \
#     python-dateutil \
#     dateparser


# =============================================================================
# Working Directory
# =============================================================================

WORKDIR /agencybench


# =============================================================================
# Notes
#
# 1. Base image already includes:
#    - Python 3 + pip + common libraries (numpy, pandas, requests, etc.)
#    - Node.js 20+ + npm + sii-cli
#    - sii-agent-sdk, openai, anthropic
#    - Correct entrypoint (automatically handles evaluation flow)
#
# 2. This Dockerfile additionally installs:
#    - networkx: for DAG validation in rubric.py
#
# 3. The entrypoint will automatically:
#    - Prepare an isolated working directory
#    - Copy workspace to the isolated directory
#    - Run eval_task.py
#    - Copy results back to the host
# =============================================================================

CMD []
