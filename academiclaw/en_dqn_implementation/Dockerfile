FROM agencybench-sandbox-cuda

LABEL query="en_dqn_implementation"
LABEL task="DQN Algorithm Implementation and Comparison"

RUN pip3 install --no-cache-dir \
    cupy-cuda12x \
    pycuda

RUN pip3 install --no-cache-dir \
    "gymnasium[classic_control]==0.29.1" \
    "torch>=2.0.0" \
    "numpy>=1.21.0" \
    "matplotlib>=3.5.0" \
    "pygame>=2.1.0" \
    tqdm

WORKDIR /agencybench

CMD []
