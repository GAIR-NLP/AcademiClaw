FROM agencybench-sandbox-cuda

LABEL query="en_ppo_pendulum"
LABEL task="PPO Algorithm Implementation for Pendulum-v1 Continuous Environment"

RUN pip3 install --no-cache-dir \
    gymnasium \
    "gymnasium[classic_control]" \
    "torch>=2.0.0" \
    numpy matplotlib

ENV PYTHONUNBUFFERED=1
WORKDIR /agencybench
CMD []
