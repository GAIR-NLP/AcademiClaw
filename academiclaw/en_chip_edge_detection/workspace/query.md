# Query 4: Chip Ring Inner Edge Detection Algorithm Implementation

## Task Description

Based on the requirements below, implement a complete chip ring inner edge detection algorithm. The algorithm must handle high-resolution grayscale images (up to 30,000 x 30,000 pixels), precisely detect the circle center coordinates and radius of the chip's inner edge, and generate high-quality mask images.

Specific task requirements:
1. Implement an image preprocessing module, including downsampling, Gaussian blur, and background subtraction
2. Implement a coarse localization algorithm using maximum contour detection to obtain the initial center and radius
3. Implement a fine localization algorithm using radial gradient scanning and a dual-edge detection strategy
4. Implement a robust statistics module using MAD (Median Absolute Deviation) technique and the 3-sigma rule to filter out outliers
5. Implement feature point detection to identify chord midpoints, high-intensity points, and outlier points
6. Generate a high-quality circular mask with chord-adaptive horizontal cropping support
7. Provide comprehensive processing visualization and debugging capabilities

Performance requirements:
- For 30,000 x 30,000 pixel images, processing time should not exceed 5 seconds (target: under 1 second)
- Circle center coordinate error within +/-40 pixels
- Radius error inward should not exceed 40 pixels

## Context

File list (see context/ directory):
- `ground_truth_data.json` - Contains ground truth circle center coordinates and radius values for 5 test images

```
Note: Due to actual project requirements, raw data and actual images are not provided here; only the file framework needed for the Query is given.
```

## Expected Output

Complete Python implementation code, including the following main modules:
- `preprocess.py` - Image preprocessing module (downsampling, Gaussian blur, background subtraction)
- `coarse_detection.py` - Coarse localization implementation (maximum contour detection, initial center and radius estimation)
- `fine_detection.py` - Fine localization implementation (radial gradient scanning, dual-edge detection strategy)
- `statistical_analysis.py` - Robust statistical analysis (MAD technique, 3-sigma rule outlier filtering)
- `mask_generation.py` - Mask generation module (circular mask, chord-adaptive horizontal cropping)
- `main.py` - Main program entry point (command-line argument configuration, logging, visualization output)
- `test.py` - Testing and evaluation module (load ground truth, compute errors, evaluate performance)

The code uses a modular design, supports command-line argument configuration, and provides comprehensive logging and visualization output.
