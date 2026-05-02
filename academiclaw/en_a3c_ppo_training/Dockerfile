# Query-specific Dockerfile for haoqiu-query2: A3C + PPO on Pendulum-v1
FROM agencybench-sandbox-cuda

LABEL query="en_a3c_ppo_training"
LABEL task="Implement A3C and PPO and train on Pendulum-v1"

# Install RL-specific Python dependencies (kept lightweight; gymnasium/torch may be preinstalled)
# Note: Use default PyPI for Gymnasium; use PyTorch CPU index only for torch
RUN pip3 install --no-cache-dir gymnasium[classic-control]==0.29.1 tensorboard
RUN pip3 install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch

WORKDIR /agencybench

CMD []