# =============================================================================
# Query 3 Dockerfile
# Task: Alpha-Beta Pruning Search Implementation in Checkers Environment
# =============================================================================

# CPU task
FROM agencybench-sandbox

LABEL query="en_checkers_alphabeta_pruning"
LABEL task="Alpha-Beta Pruning Search Implementation in Checkers Environment"

# =============================================================================
# Task-specific dependencies
# =============================================================================

# Install base dependencies
RUN pip3 install --no-cache-dir \
    gymnasium \
    pettingzoo \
    ray[rllib] \
    pygame \
    tqdm \
    matplotlib \
    numpy

# Set relevant environment variables
ENV PYTHONUNBUFFERED=1


# =============================================================================
# Environment variables (optional)
# =============================================================================

# ENV MY_VAR=value


# =============================================================================
# Working directory
# =============================================================================

WORKDIR /agencybench


# =============================================================================
# Important Notes
#
# 1. Do not define ENTRYPOINT - the base image already defines the correct entrypoint
# 2. Do not define CMD - unless you have special requirements
# 3. The entrypoint will automatically handle:
#    - Preparing an isolated working directory
#    - Copying workspace and context to the isolated directory
#    - Running eval_task.py (with correct arguments)
#    - Copying results back to the host
# =============================================================================

CMD []
