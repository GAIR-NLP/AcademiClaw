FROM agencybench-sandbox

LABEL query="T13_zh_datika_yueju"
LABEL task="高中物理答题卡自动阅卷"

RUN apt-get update && apt-get install -y \
    libgl1-mesa-dri libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir \
    opencv-python-headless \
    easyocr \
    Pillow \
    numpy \
    pandas

WORKDIR /agencybench

CMD []