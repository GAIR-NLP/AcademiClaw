FROM agencybench-sandbox-cuda

LABEL query="en_ddqn_mountaincar"
LABEL task="Double DQN-Based MountainCar Energy Hill-Climbing Optimization"

RUN pip3 install --no-cache-dir \
    gymnasium \
    "gymnasium[classic_control]" \
    "torch>=2.0.0" \
    numpy matplotlib

ENV PYTHONUNBUFFERED=1
WORKDIR /agencybench
CMD []
