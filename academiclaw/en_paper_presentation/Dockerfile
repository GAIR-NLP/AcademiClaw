# =============================================================================
# Query-specific Dockerfile
# Task: generate/ppt/query3 - Generate Detailed Analysis PPT from Multiple Academic Papers
#
# This task requires:
#   - python-pptx: PPT generation
#   - openai: LLM evaluation in rubric
#   - PyPDF2/pdfplumber: Reading PDF paper content
# =============================================================================


# =============================================================================
# Base Image Selection
# =============================================================================

# CPU task (default) - PPT generation does not require GPU
FROM agencybench-sandbox


# =============================================================================
# Metadata
# =============================================================================

LABEL query="T42_en_paper_presentation"
LABEL task="Generate Detailed Analysis PPT from Multiple Academic Papers"


# =============================================================================
# Task-specific Dependencies
# =============================================================================

# python-pptx for PPT generation, openai for rubric LLM evaluation
# PyPDF2 and pdfplumber for reading PDF paper content
RUN pip3 install --no-cache-dir \
    python-pptx \
    openai \
    PyPDF2 \
    pdfplumber


# =============================================================================
# Environment Variables (optional)
# =============================================================================

# ENV MY_VAR=value


# =============================================================================
# Working Directory
# =============================================================================

WORKDIR /agencybench


# =============================================================================
# Important Notes
#
# 1. Do not define ENTRYPOINT - the base image already defines the correct entrypoint
# 2. Do not define CMD - unless you have special requirements
# 3. The entrypoint automatically handles:
#    - Preparing an isolated working directory
#    - Copying workspace and context to the isolated directory
#    - Running eval_task.py (with correct arguments)
#    - Copying results back to the host
# =============================================================================

CMD []
