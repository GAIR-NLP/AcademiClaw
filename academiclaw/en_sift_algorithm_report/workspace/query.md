Query:
---

Based on the materials in `context/`, complete a rigorously structured SIFT Algorithm Research Report that combines theoretical depth with practical guidance.

**Materials**
- `context/query3.txt` (task description and output requirements)
- `context/reference1.txt`
- `context/reference2.txt`
- `context/reference3.txt` (if available)
- `context/query3.docx` (may be used as reference if needed)

**The report must include the following five sections:**
1. Core Algorithm Principles and Mathematical Foundations: scale space, DoG approximation, extrema detection, Hessian/curvature, etc.
2. Key Implementation Details: scale-space construction, keypoint detection and localization, orientation assignment, descriptor generation
3. Feature Matching and Robust Estimation: matching criteria, ratio test (Lowe ratio test), RANSAC, etc.
4. Algorithm Performance Evaluation: scale/rotation invariance, illumination robustness, noise/blur impact; provide experimental design and reproducible verification plans
5. Improved/Alternative Algorithm Comparison: compare at least SIFT vs. SURF and ORB in terms of advantages, disadvantages, and applicable scenarios

**Output**
- Save the final version as `answer.md` in the current directory
