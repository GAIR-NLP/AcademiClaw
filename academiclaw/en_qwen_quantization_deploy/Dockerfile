FROM agencybench-sandbox-cuda

LABEL query="en_qwen_quantization_deploy"
LABEL task="Qwen2.5-1.5B Mixed-Precision Quantization Deployment"

RUN pip3 install --no-cache-dir \
    torch \
    transformers \
    pyarrow \
    accelerate \
    sentencepiece

WORKDIR /agencybench
CMD []
