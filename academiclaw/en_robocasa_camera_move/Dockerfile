# =============================================================================
# Query: dengjianbin-query1
# Task: Robocasa Camera Movement Implementation
#
# Task description:
#   Implement camera movement functionality in the Robocasa simulation environment,
#   write a minimal example script and functionality documentation,
#   and record a camera trajectory video. Must support setting different poses
#   for the same camera at each timestep.
#
# Environment requirements (based on environment.yaml):
#   - Python 3.10
#   - PyTorch 2.3.0 + CUDA 12
#   - Mujoco 3.2.6 + mujoco-py 2.1.2.14
#   - Robosuite 1.5.0
#   - EGL rendering support
# =============================================================================


# =============================================================================
# Base image selection
# =============================================================================

# CUDA task (required, supports EGL rendering and PyTorch CUDA)
FROM agencybench-sandbox-cuda


# =============================================================================
# Metadata
# =============================================================================

LABEL query="en_robocasa_camera_move"
LABEL task="Robocasa Camera Movement Implementation"


# =============================================================================
# System dependencies
# =============================================================================

RUN apt-get update && apt-get install -y \
    # MuJoCo rendering dependencies
    libgl1-mesa-dev \
    libgl1-mesa-dri libgl1 \
    libglew-dev \
    libosmesa6-dev \
    # EGL rendering support
    libegl1-mesa-dev \
    libgles2-mesa-dev \
    # mujoco-py compilation dependencies
    patchelf \
    libglfw3 \
    libglfw3-dev \
    # Video processing
    ffmpeg \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    # X11/display related
    xvfb \
    libxrandr2 \
    libxinerama1 \
    libxcursor1 \
    libxi6 \
    # Open3D dependencies
    libusb-1.0-0 \
    # VTK/Mayavi dependencies
    libxrender1 \
    libsm6 \
    # Other
    unzip \
    && rm -rf /var/lib/apt/lists/*


# =============================================================================
# Python dependencies
#
# Note: The base image already includes common libraries; only task-specific
# dependencies are installed here
# =============================================================================

# Core simulation environment
RUN pip3 install --no-cache-dir \
    mujoco==3.2.6 \
    robosuite==1.5.0 \
    robosuite-models==1.0.0 \
    gymnasium==1.1.1 \
    gym==0.26.2

# Video/image processing
RUN pip3 install --no-cache-dir \
    imageio==2.37.0 \
    imageio-ffmpeg==0.6.0 \
    opencv-python==4.11.0.86

# 3D processing and transforms
RUN pip3 install --no-cache-dir \
    transforms3d==0.4.2 \
    pyquaternion==0.9.9 \
    trimesh==4.6.5

# Scientific computing (specify compatible versions)
RUN pip3 install --no-cache-dir \
    numpy==1.23.2 \
    scipy==1.13.1

# Configuration and utilities
RUN pip3 install --no-cache-dir \
    hydra-core==1.3.2 \
    omegaconf==2.3.0 \
    h5py==3.12.1 \
    pyyaml==6.0.2

# EGL probing
RUN pip3 install --no-cache-dir \
    egl-probe==1.0.2 \
    pyopengl==3.1.9

# mujoco-py (optional, may be needed by some legacy code)
# RUN pip3 install --no-cache-dir mujoco-py==2.1.2.14


# =============================================================================
# Environment variables
# =============================================================================

# MuJoCo rendering backend - use EGL for GPU offscreen rendering
ENV MUJOCO_GL=egl

# Alternative: use osmesa for CPU offscreen rendering
# ENV MUJOCO_GL=osmesa

# Python environment
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Disable interactive frontend
ENV DEBIAN_FRONTEND=noninteractive


# =============================================================================
# Working directory
# =============================================================================

WORKDIR /agencybench


# =============================================================================
# Important notes
#
# 1. Do not define ENTRYPOINT - the base image already defines the correct entrypoint
# 2. The agent needs to work in the workspace to:
#    - Clone the Robocasa repository (https://github.com/robocasa/robocasa)
#    - Implement camera movement functionality
#    - Write functionality documentation
#    - Record camera trajectory video (kitchen scene such as PnPCounterToSink)
# =============================================================================

CMD []
