FROM agencybench-sandbox-cuda

LABEL query="en_sphere_uformer_export"
LABEL task="Sphere UFormer Model Implementation"

RUN pip3 install --no-cache-dir \
    torch --index-url https://download.pytorch.org/whl/cpu
RUN pip3 install --no-cache-dir \
    opencv-python-headless \
    trimesh \
    scipy

WORKDIR /agencybench
CMD []
