FROM agencybench-sandbox

LABEL query="en_bvh_path_tracing"
LABEL task="BVH Path Tracing Renderer"

# cmake is required by rubric to compile the C++ renderer
RUN apt-get update && apt-get install -y cmake && rm -rf /var/lib/apt/lists/*
RUN pip3 install --no-cache-dir scikit-image Pillow

WORKDIR /agencybench
CMD []
