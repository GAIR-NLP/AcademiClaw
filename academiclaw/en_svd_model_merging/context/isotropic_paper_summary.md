# Paper Summary: No Task Left Behind - Isotropic Model Merging

**Title:** No Task Left Behind: Isotropic Model Merging with Common and Task-Specific Subspaces  
**Authors:** Daniel Marczak et al.  
**Source:** arXiv:2502.04959v3 [cs.LG] 11 Jun 2025

## 1. Introduction & Problem Definition

The paper proposes a new framework for **Model Merging**, specifically focusing on merging multiple task-specific models fine-tuned from a shared pre-trained model into a single multi-task model without additional training.

### 1.1 Notation
*   $\theta_0$: Weights of the **pre-trained model**.
*   $\theta_t$: Weights of the fine-tuned model for task $t$ ($t = 1, \dots, T$).
*   $\Delta_t = \theta_t - \theta_0$: **Task Matrix** (or Task Vector) for task $t$.
*   $\theta_M$: Weights of the merged model.
*   **Layer-wise Application**: The methods described are applied layer-by-layer. The notation refers to a specific layer's weight matrix $W \in \mathbb{R}^{m \times n}$.

### 1.2 Motivation
Existing methods like Task Arithmetic (TA) simply sum the task vectors ($\Delta_{TA} = \sum \Delta_t$). The authors find that:
1.  **Cosine Similarity** between task vectors does not correlate well with merging performance.
2.  **Subspace Alignment Ratio (SAR)** *does* correlate strongly with performance. SAR measures how well the principal directions of individual tasks align with the merged model.
3.  TA results in a skewed singular value spectrum dominated by a few components, underrepresenting some tasks.
4.  **Solution**: Flattening the singular value spectrum (**Isotropic Merging**) improves alignment and performance.

---

## 2. Method 1: Isotropic Merging in Common Subspace (Iso-C)

**Core Idea**: Replace the skewed singular values of the summed task matrix with a uniform (isotropic) value equal to the average singular value.

### Algorithm Steps (Per Layer)

**Input**: Task matrices $\Delta_1, \dots, \Delta_T$ where $\Delta_t \in \mathbb{R}^{m \times n}$.

1.  **Sum Task Matrices**:
    $$ \Delta_{TA} = \sum_{t=1}^{T} \Delta_t $$

2.  **SVD Decomposition**:
    Compute the SVD of the summed matrix:
    $$ \Delta_{TA} = U \Sigma V^\top $$
    Where $U \in \mathbb{R}^{m \times r}$, $\Sigma \in \mathbb{R}^{r \times r}$, $V \in \mathbb{R}^{n \times r}$, and $r$ is the rank.

3.  **Calculate Isotropic Factor ($\bar{\sigma}$)**:
    Compute the average of the singular values $\{\sigma_i\}$:
    $$ \bar{\sigma} = \frac{1}{r} \sum_{i=1}^{r} \sigma_i $$

4.  **Reconstruct Matrix**:
    Create the merged update matrix using the isotropic scaling factor:
    $$ \Delta_{\text{Iso-C}} = \bar{\sigma} U V^\top $$

5.  **Final Merged Weights**:
    $$ \theta_{\text{Iso-C}} = \theta_0 + \alpha \Delta_{\text{Iso-C}} $$
    Where $\alpha$ is a scaling coefficient (hyperparameter).

---

## 3. Method 2: Isotropic Merging with Common and Task-Specific Subspaces (Iso-CTS)

**Core Idea**: Iso-C relies only on the "Common Subspace" defined by $\Delta_{TA}$. Iso-CTS explicitly adds "Task-Specific Subspaces" (directions orthogonal to the common subspace) to ensure no task is left behind.

### Algorithm Steps (Per Layer)

**Input**: Task matrices $\Delta_1, \dots, \Delta_T$, Pre-trained $\theta_0$, Hyperparameters $k$ (common dim) and $\alpha$.

1.  **Common Subspace Extraction**:
    *   Compute $\Delta_{TA} = \sum \Delta_t$.
    *   Compute SVD: $\Delta_{TA} = U \Sigma V^\top$.
    *   Retain the **top-k** singular vectors/values:
        *   $U^{1:k} = [u_1 | \dots | u_k]$
        *   $V^{1:k} = [v_1 | \dots | v_k]$
        *   $\sigma^{cm} = \text{diag}(\Sigma)_{1:k}$ (Common singular values).

2.  **Task-Specific Projection**:
    For each task $t = 1 \dots T$:
    *   Project $\Delta_t$ onto the subspace **orthogonal** to the common subspace $U^{1:k}$:
        $$ \overline{\Delta}_t = \Delta_t - U^{1:k} (U^{1:k})^\top \Delta_t $$
    *   Compute SVD of the residual: $\overline{\Delta}_t = \overline{U}_t \overline{\Sigma}_t \overline{V}_t^\top$.
    *   Retain top **s** components, where $s = \lfloor \frac{r - k}{T} \rfloor$:
        *   $\overline{U}_t^{1:s}$, $\overline{V}_t^{1:s}$, and $\sigma_t^{ts} = \text{diag}(\overline{\Sigma}_t)_{1:s}$.

3.  **Combine Subspaces**:
    Concatenate the common basis and all task-specific bases:
    $$ U_* = [ U^{1:k} | \overline{U}_1^{1:s} | \dots | \overline{U}_T^{1:s} ] \in \mathbb{R}^{m \times r} $$
    $$ V_* = [ V^{1:k} | \overline{V}_1^{1:s} | \dots | \overline{V}_T^{1:s} ] \in \mathbb{R}^{n \times r} $$

4.  **Orthogonalization (Whitening)**:
    Since the concatenated bases $U_*$ and $V_*$ are not necessarily orthogonal, apply whitening via SVD:
    *   Compute SVD of $U_*$: $U_* = P_{U_*} \Sigma_{U_*} Q_{U_*}^\top$.
    *   Update $U_* \leftarrow P_{U_*} Q_{U_*}^\top$.
    *   Compute SVD of $V_*$: $V_* = P_{V_*} \Sigma_{V_*} Q_{V_*}^\top$.
    *   Update $V_* \leftarrow P_{V_*} Q_{V_*}^\top$.

5.  **Calculate Isotropic Factor ($\bar{\sigma}$)**:
    Average all selected singular values (both common and task-specific):
    $$ \bar{\sigma} = \frac{1}{r} \left( \sum_{i=1}^k \sigma^{cm}_i + \sum_{t=1}^T \sum_{i=1}^s \sigma^{ts}_{t,i} \right) $$

6.  **Reconstruct Matrix**:
    $$ \Delta_{\text{Iso-CTS}} = \bar{\sigma} U_* V_*^\top $$

7.  **Final Merged Weights**:
    $$ \theta_{\text{Iso-CTS}} = \theta_0 + \alpha \Delta_{\text{Iso-CTS}} $$

---

## 4. Implementation Details & Hyperparameters

### 4.1 Implementation Constraints (Appendix C.2)
*   **2D Matrices**: The SVD-based methods (Iso-C, Iso-CTS) are applied **only to 2D weight matrices** (e.g., Linear layers, Conv2d reshaped).
*   **1D Vectors**: For parameters that are vectors (e.g., Bias terms `bias`, LayerNorm parameters `weight` and `bias`), **standard averaging (Task Arithmetic)** is used instead of SVD.
    *   Equation: $\theta_{merged}^{(1D)} = \theta_0^{(1D)} + \alpha \sum \Delta_t^{(1D)}$.

### 4.2 Hyperparameters
*   **Common Subspace Ratio ($k/r$)**:
    *   For Iso-CTS, the optimal fraction of subspace assigned to the common subspace is **0.8**.
    *   $k = \lfloor 0.8 \times \text{rank} \rfloor$.
    *   $s = \lfloor (r - k) / T \rfloor$.
*   **Scaling Coefficient ($\alpha$)**:
    *   The paper suggests optimal $\alpha$ values in **Table 5**.
    *   **Iso-C**: $\alpha \approx 1.3$ (range 0.8 - 1.5 depending on model/tasks).
    *   **Iso-CTS**: $\alpha \approx 1.4$ (range 1.1 - 1.9).
    *   General recommendation: Iso methods are more robust to $\alpha$ than TA.

### 4.3 Computational Complexity (Appendix B)
*   **Iso-C**: $\mathcal{O}(L n^3)$ (One SVD per layer).
*   **Iso-CTS**: $\mathcal{O}(T L n^3)$ (SVD on $\Delta_{TA}$ + SVD on each of $T$ tasks + 2 small SVDs for whitening).

---

## 5. Key Differences Summary

| Feature | Task Arithmetic (TA) | Iso-C | Iso-CTS |
| :--- | :--- | :--- | :--- |
| **Formula** | Summation | SVD + Flatten Spectrum | SVD + Projection + Flatten |
| **Spectrum** | Skewed (Dominant directions) | Flat (Isotropic) | Flat (Isotropic) |
| **Subspaces** | Implicitly Common | Common Only | Common + Task-Specific |
| **Handling 1D Params** | Sum | Sum | Sum |
| **Complexity** | Low | Medium | High |