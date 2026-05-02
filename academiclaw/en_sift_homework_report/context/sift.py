#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implement:
1) DoG keypoint detection (Gaussian pyramid + DoG + 3x3x3 extrema + contrast + edge suppression)
2) Orientation assignment (36-bin, Gaussian-weighted)
3) 128-D descriptor (4x4 cells x 8 bins, tri-linear interpolation, normalize -> clamp -> renormalize)

Only use: numpy, cv2
"""

from typing import List, Tuple
import numpy as np
import cv2 as cv

Keypoint = Tuple[float, float, float]                 # (x, y, sigma)
OrientedKeypoint = Tuple[float, float, float, float]  # (x, y, sigma, theta)

# ----------------------------
# Utilities
# ----------------------------
def to_gray_float01(image: np.ndarray) -> np.ndarray:
    """Convert to grayscale float32 in [0,1]."""
    if image.ndim == 3:
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    img = image.astype(np.float32)
    if img.max() > 1.0:
        img /= 255.0
    return img

def gaussian_blur(img: np.ndarray, sigma: float) -> np.ndarray:
    """OpenCV Gaussian blur with sigma; ksize=(0,0) lets cv choose size."""
    return cv.GaussianBlur(img, ksize=(0, 0), sigmaX=sigma, sigmaY=sigma, borderType=cv.BORDER_REPLICATE)

def gradient(img: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Return (mag, ori in [0, 2pi)) using Sobel."""
    gx = cv.Sobel(img, cv.CV_32F, 1, 0, ksize=1)
    gy = cv.Sobel(img, cv.CV_32F, 0, 1, ksize=1)
    mag = np.hypot(gx, gy)
    ori = np.mod(np.arctan2(gy, gx), 2.0 * np.pi)
    return mag, ori
# ----------------------------
# 0) Build Gaussian pyramid & DoG
# ----------------------------
def build_gaussian_pyramid(
    image: np.ndarray,
    sigma_base: float = 1.6,
    num_octaves: int = 4,
    num_scales: int = 3
) -> Tuple[List[List[np.ndarray]], List[List[float]]]:
    """
    Return:
      gauss_pyr: list over octaves, each is list of Gaussian images (length s+3 recommended)
      sigmas:    list over octaves, each is list of absolute sigmas for corresponding images
    """
    # TODO: implement
    s = num_scales
    k = 2**(1.0 / s)

    gauss_pyr = []
    sigmas = []
            
    return gauss_pyr, sigmas
        
def build_dog_pyramid(gauss_pyr: List[List[np.ndarray]]) -> List[List[np.ndarray]]:
    """DoG = G[i+1] - G[i] for each octave."""
    # TODO: implement
    # 直接让Gaussian Pyramid中相邻图像相减，一个Octave有s+3的高斯，得s+2 DoG imgs
    dog_pyr = []
        
    return dog_pyr

# ----------------------------
# 1) DoG keypoint detection
# ----------------------------
def detect_dog_keypoints(
    image: np.ndarray,
    sigma: float = 1.6,
    num_octaves: int = 4,
    num_scales: int = 3,
    contrast_thresh: float = 0.03,
    edge_r: float = 10.0
) -> List[Keypoint]:
    """
    Steps:
      - build Gaussian pyramid (s+3 images per octave)
      - DoG pyramid (s+2 per octave)
      - 3x3x3 extrema (skip border & top/bottom DoG layers)
      - contrast threshold on |DoG|
      - edge suppression via Hessian ratio test: (TrH)^2/detH < (r+1)^2/r, detH>0
    Return list of (x, y, sigma)
    """
    # TODO: implement
    gauss_pyr, sigmas = build_gaussian_pyramid(image, sigma, num_octaves, num_scales)
    dog_pyr = build_dog_pyramid(gauss_pyr)
    
    s = num_scales
    keypoints:list[int,int,float] = []

    return keypoints
                    
# ----------------------------
# 2) Orientation assignment
# ----------------------------
def compute_keypoint_orientation(
    image: np.ndarray,
    keypoints: List[Keypoint],
    sigma_ori_mul: float = 1.5,
    num_bins: int = 36
) -> List[OrientedKeypoint]:
    """
    For each (x,y,sigma):
      - window radius = round(3*sigma)
      - gradients weighted by Gaussian (sigma_ori = 1.5*sigma)
      - 36-bin histogram on [0,2pi); smooth; peaks >= 0.8*max create additional orientations
    Return (x, y, sigma, theta in radians)
    """
    # TODO: implement
    oriented_keypoints = []
    bin_width = 2.0 * np.pi / num_bins

    return oriented_keypoints    

# ----------------------------
# 3) 128-D SIFT descriptor
# ----------------------------
def compute_sift_descriptor(
    image: np.ndarray,
    oriented_keypoints: List[OrientedKeypoint],
    grid_size: int = 4,
    bin_per_cell: int = 8
) -> np.ndarray:
    """
    For each (x, y, sigma, theta):
      - sample a 16x16 region scaled by sigma (do NOT rotate patch; rotate gradient by -theta)
      - Gaussian window over region
      - accumulate histograms with tri-linear interpolation (x,y within cells + orientation)
      - L2 normalize -> clamp 0.2 -> L2 normalize
    Return: (N, 128) float32
    """
    # TODO: implement
    descriptors = []
    
    return np.array(descriptors, dtype=np.float32)

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", type=str, required=True)
    args = ap.parse_args()

    img0 = cv.imread(args.image, cv.IMREAD_GRAYSCALE)
    assert img0 is not None, "Failed to load image"
    img = to_gray_float01(img0)

    # 1) keypoints
    kps = detect_dog_keypoints(img)
    print(f"detected keypoints: {len(kps)}")

    # 2) orientation
    okps = compute_keypoint_orientation(img, kps)
    print(f"oriented keypoints: {len(okps)}")

    # 3) descriptors
    desc = compute_sift_descriptor(img, okps)
    print(f"descriptors: {desc}")

    vis = cv.cvtColor((img * 255).astype(np.uint8), cv.COLOR_GRAY2BGR)
    for (x, y, s, th) in okps[:300]:  # draw at most 300
        p = (int(round(x)), int(round(y)))
        q = (int(round(x + 5 * np.cos(th))), int(round(y + 5 * np.sin(th))))
        cv.circle(vis, p, 1, (0, 255, 0), -1)
        cv.line(vis, p, q, (0, 0, 255), 1)
    cv.imwrite("sift_keypoints_vis.png", vis)
    print("Saved: sift_keypoints_vis.png")

if __name__ == "__main__":
    main()
