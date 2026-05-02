## Query Description

**Task Background**:
You are an AI researcher reproducing the core algorithms from the paper "No Task Left Behind: Isotropic Model Merging". This paper proposes a merging method that smooths the singular value spectrum of model parameters via SVD (Singular Value Decomposition) to address interference problems in multi-task model merging.

**Task Objective**:
The context provides a code template `merging_interface.py` and a paper summary. Based on the function signatures in `merging_interface.py`, **fill in the missing code** to implement the two core algorithms from the paper:

1.  **Iso-C (Algorithm 1)**: Isotropic Merging in Common Subspace.
2.  **Iso-CTS (Algorithm 2)**: Isotropic Merging with Common and Task-Specific Subspaces.

**Core Implementation Requirements**:
1.  **Interface-based Programming**:
    *   Please strictly follow the input/output definitions of `iso_c_merging` and `iso_cts_merging`.
    *   Do not modify the function signatures.
    *   Do not include file read/save logic (File I/O); focus only on tensor computation.

2.  **Dimension Handling Strategy (Important)**:
    *   **2D Weight Matrices (Weight Matrix)**: Apply the SVD merging algorithm from the paper.
    *   **0D/1D Tensors (Bias, LayerNorm)**: Do not apply SVD. Directly use **Task Arithmetic (Mean)**, i.e., compute the mean of all task vectors, then multiply by scaling coefficient $\alpha$ and add back to the pre-trained weights.

3.  **Algorithm Details**:
    *   **Iso-C**:
        *   Compute the SVD of the Task Matrix sum ($\Delta_{TA}$).
        *   Compute the mean of the singular values $\bar{\sigma}$.
        *   Reconstruct the update matrix using $\bar{\sigma}$: $\Delta_{new} = \alpha \cdot \bar{\sigma} \cdot (U V^\top)$.
        *   Recommended Scaling Coefficient $\alpha = 1.3$ (default parameter).
    *   **Iso-CTS**:
        *   Extract the Common Subspace.
        *   Project each task onto the Orthogonal Complement of the common subspace to extract task-specific directions.
        *   Concatenate the common basis and all task-specific bases.
        *   **Key Step**: Apply **Whitening (Orthogonalization)** to the concatenated basis to ensure orthogonality.
        *   Compute the isotropic factor and reconstruct.
        *   Recommended Scaling Coefficient $\alpha = 1.4$ (default parameter).

**Output Format**:
Please save the completed code as `merging_interface.py`.
