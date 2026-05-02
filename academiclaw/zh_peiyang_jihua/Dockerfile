FROM agencybench-sandbox

LABEL query="T39_zh_peiyang_jihua"
LABEL task="人工智能专业培养计划生成与排程"

# 评测与任务执行的必要依赖（agent 不负责配环境）
RUN pip3 install --no-cache-dir \
    openai>=1.0.0 \
    pandas \
    numpy \
    chardet

WORKDIR /agencybench
CMD []
