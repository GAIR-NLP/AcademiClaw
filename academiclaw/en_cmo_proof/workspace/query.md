# CMO 2024 Problem 6 - Mathematical Competition Solution

## Task Description

Please solve Problem 6 from the Chinese Mathematical Olympiad (CMO) 2024 competition. This is a mathematical proof problem consisting of two parts:

## Problem Content

Given real numbers $a_1, a_2, \ldots, a_n$ satisfying:
$$\sum_{i=1}^{n} a_i = n, \quad \sum_{i=1}^{n} a_i^2 = 2n, \quad \sum_{i=1}^{n} a_i^3 = 3n.$$

Define the **width** $\Delta = \max\{a_1, a_2, \ldots, a_n\} - \min\{a_1, a_2, \ldots, a_n\}$.

### Part 1: Prove C = sqrt(5)

**(1)** Find the largest constant $C$ such that for all $n \geq 4$, we have $\Delta \geq C$.

Required:
- Provide a concrete example showing the width can approach arbitrarily close to C = sqrt(5)
- Prove the lower bound of the width: i.e., $\Delta \geq \sqrt{5}$ holds for all sequences satisfying the conditions

### Part 2: Higher-Order Exact Lower Bound

**(2)** Prove there exists a constant $C_2 > 0$ such that $\Delta \geq C + C_2 n^{-3/2}$, where $C$ is the constant from part (1).

## Submission Requirements

Please write your complete mathematical proof in an `answer.md` file and save it in the current working directory.

Format requirements:
- Use Markdown format
- Use mathematical notation clearly
- The proof process must be logically rigorous with no critical steps omitted
- Divide into "## Part 1" and "## Part 2" sections

## Hints

- Non-negative polynomial methods may be used
- Construct auxiliary functions
- Analyze discrete obstructions
- Use lower bounds on irrational number approximation errors
