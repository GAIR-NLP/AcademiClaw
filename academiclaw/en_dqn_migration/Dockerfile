FROM agencybench-sandbox-cuda

LABEL query="en_dqn_migration"
LABEL task="DQN Reinforcement Learning Algorithm Migration from TensorFlow to PyTorch"

# Task-specific dependencies: PyTorch + Gymnasium + visualization
RUN pip3 install --no-cache-dir \
    torch \
    gymnasium \
    matplotlib \
    pandas

WORKDIR /agencybench
CMD []
