# =============================================================================
# Query 1: Reinforcement Learning-Based Mahjong Agent - Dockerfile
# =============================================================================

FROM agencybench-sandbox-cuda

# =============================================================================
# Metadata
# =============================================================================

LABEL query="en_mahjong_rl_agent"
LABEL task="Reinforcement Learning-Based Mahjong Agent Development and Implementation"

# =============================================================================
# Task-specific dependencies
# =============================================================================

# Reinforcement learning and deep learning libraries
RUN pip3 install --no-cache-dir \
    numpy \
    torch \
    gymnasium \
    stable-baselines3 \
    matplotlib \
    seaborn

# =============================================================================
# Working directory
# =============================================================================

WORKDIR /agencybench

CMD []
