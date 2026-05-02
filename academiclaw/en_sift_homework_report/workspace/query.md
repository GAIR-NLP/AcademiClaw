# SIFT Homework Report Writing Task (Query 4)

Please complete a high-quality course homework report `report.md` based on the following context:

- context/hw_sift.pdf: Homework requirements (theoretical and programming problems)
- context/sift.py: Your completed SIFT algorithm implementation (for reference)

The report should contain two parts:

## 1. Theoretical Proof (Written Assignment)
- Perspective Projection:
  - (a) Rigorously establish the projection model. From a 3D point $(X,Y,Z)$ through perspective projection to the image plane $(x,y,-f)$, prove that a circle parallel to the image plane still projects as a circle, and derive the standard equation $(x - x_c)^2 + (y - y_c)^2 = r^2$.
  - (b) Derive the vanishing point $(x_v, y_v)$ of a set of parallel lines on the plane $Ax + By + Cz + D = 0$ in the image.
  - (c) Prove that these vanishing points are collinear, and derive the vanishing line equation $Ax_v + By_v + Cf = 0$.
- Verification: Use special cases (e.g., lines on the $y=0$ or $x=0$ plane) to check formula correctness.

It is recommended to include formula blocks (LaTeX), step-by-step derivations, and necessary geometric diagrams.

## 2. Programming Experiment Report (Programming Assignment)
- Core Algorithm Analysis:
  - Explain why DoG is used to approximate LoG and its efficiency advantage in scale space.
  - Describe 3x3x3 extrema detection, contrast threshold, and Hessian edge response suppression.
  - Describe the role of histogram smoothing and parabolic interpolation in orientation assignment.
  - Provide a detailed description of the 128-D descriptor construction process (16x16 region, rotation alignment, trilinear interpolation, normalization-truncation-renormalization).
- Results Presentation:
  - You may insert generated visualizations (e.g., `sift_keypoints_vis.png`) into the report:
    - `![SIFT Keypoints](sift_keypoints_vis.png)`

Please save the completed `report.md` in the root of the current working directory (the workspace root at the same level as this file), and ensure the Markdown structure is well-formatted with LaTeX syntax for formulas.
