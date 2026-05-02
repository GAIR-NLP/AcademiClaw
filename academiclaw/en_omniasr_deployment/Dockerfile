FROM agencybench-sandbox-cuda

LABEL query="en_omniasr_deployment"
LABEL task="OmniASR Multilingual Speech Recognition Model Deployment"

RUN apt-get update && apt-get install -y \
    cmake \
    ninja-build \
    libsndfile1-dev \
    && rm -rf /var/lib/apt/lists/*
RUN pip3 install --no-cache-dir \
    torch \
    torchaudio \
    sentencepiece

WORKDIR /agencybench
CMD []
