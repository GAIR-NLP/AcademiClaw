# Background

Your large model inference team is maintaining a high-frequency generative text service. The business scenario requires the model to have a certain level of **creativity (Temperature > 0)**. The current online flagship model (Target Model) is constrained by GPU memory bandwidth, and its response latency cannot meet real-time interaction requirements.

The team has decided to introduce a **Speculative Decoding** architecture. You have already obtained a Draft Model whose vocabulary is aligned with the main model.

---

# Task Objective

You need to refactor the existing serial inference pipeline (`inference.py`) to implement a high-performance speculative inference engine that **supports Stochastic Sampling**.

## Core Challenges (Hard Mode)

### 1. Implement Rejection Sampling
   - **Algorithm difficulty upgrade**: The business requires `temperature > 0`. You cannot simply do token comparison.
   - You must implement standard **Rejection Sampling** logic:
     - When $p_{draft}(x) \le p_{target}(x)$, accept unconditionally.
     - When $p_{draft}(x) > p_{target}(x)$, accept with probability $p_{target}(x) / p_{draft}(x)$.
     - **Key constraint**: Upon rejection, you must resample from the **corrected distribution** (Normed Difference Distribution), strictly ensuring the final output distribution $P(x)$ is completely identical to sampling from the Target Model alone (mathematically lossless).

### 2. Zero-Copy KV-Cache Rollback
   - **Engineering difficulty upgrade**: Under extremely high concurrency, frequent `torch.cat` or Tensor reallocation leads to GPU memory fragmentation.
   - You need to implement **efficient rollback**:
     - When speculation is rejected, only modify the "valid length pointer" or perform slice view operations on the KV Cache, **avoiding creation of new KV Tensors as much as possible**.

### 3. Performance Optimization and Verification
   - Analyze the Baseline bottleneck and prove that your parallel verification mechanism can break through that bottleneck.

---

# Key Operation Instructions (Must Read)

To accurately test the acceleration effect of speculative decoding, you need to simulate the ideal case where "Draft Model predictions are very accurate" (i.e., high acceptance rate scenario), otherwise the speedup ratio will not be apparent.

**Please be sure to follow these steps:**
1.  **Run `setup_benchmark.py`**: This script generates vocabulary-aligned `target_model.pt` and `draft_model.pt` (by applying Identity Patch to the last few layers of the Target, making the two distributions converge).
2.  **Write `inference.py`**: Load the generated model weights in the code for testing.

---

# Performance Verification

You need to build test scripts to verify the refactored inference engine:

- **Distribution Consistency (Distribution Match)**:
  - Since randomness is involved, token-by-token comparison is not possible. You need to prove under a fixed Random Seed that the Speculative Decoding output is **bitwise identical** to the Baseline, thereby proving the mathematical correctness of your Rejection Sampling logic.
- **Speedup**:
  - Under conditions of `gamma=4` and `temperature=0.8`, end-to-end throughput (Tokens/Sec) should improve by **1.3x or more** compared to the baseline.

---

# Expected Output

1. **`inference.py`**: Complete implementation containing Baseline and Rejection Sampling Speculative Decoding.
2. **`benchmark_report.md`**: Performance comparison report, must include analysis of speedup ratio changes under different Temperature values.

---

# Technical Requirements

- **Environment constraint**: Do not modify `gpt_lite.py`.
- **Verification mechanism**: The Target Model must compute probability distributions for all Draft Tokens in parallel.
- **Robustness**: The algorithm must handle both `temperature=0` (degenerates to Greedy) and `temperature > 0` cases.
- **Memory safety**: GPU memory peak fluctuations during the Rollback phase are strictly prohibited.

---

# Success Criteria

- [Math] Under stochastic sampling mode, output results are completely identical to Baseline under a fixed seed.
- [Perf] Inference speed is significantly improved (>1.3x).
- [Code] Memory operations are efficient, with no redundant Tensor allocations.
