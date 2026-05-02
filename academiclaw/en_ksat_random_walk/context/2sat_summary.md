## Random Walk Algorithm for 2-SAT

### Problem Background

The SAT problem is the problem of determining whether a given CNF (Conjunctive Normal Form) formula is satisfiable, and it is one of the core problems in computer science. For any \(k \ge 2\), \(k\)-SAT is a special case of SAT in which each clause contains exactly \(k\) variables.

**2-SAT** refers to CNF formulas where each clause contains two literals (a variable or its negation), for example:

\[
\varphi = (x \lor y) \land (y \lor z) \land (x \lor z)
\]

This formula is a 2-CNF formula, and the assignment \(x = y = z = \text{true}\) satisfies it.

Known results:
- SAT is NP-complete;
- When \(k \ge 3\), \(k\)-SAT is NP-complete;
- **2-SAT can be solved deterministically in polynomial time** (e.g., via the strongly connected components algorithm).

This section introduces a **simple randomized algorithm with high probability of correctness** for solving 2-SAT.

---

### Random Walk Algorithm Description

Let:
- \(\varphi\) be a 2-CNF formula;
- \(V = \{v_1, v_2, \dots, v_n\}\) be the set of variables.

The algorithm proceeds as follows:

1. **Random Initialization**

   Randomly choose an assignment
   \[
   \sigma_0 : V \to \{\text{true}, \text{false}\}
   \]

2. **Random Walk Iteration**

   For \(t = 0, 1, 2, \dots, 100n^2\):
   - If the current assignment \(\sigma_t\) satisfies the formula \(\varphi\), output \(\sigma_t\) and terminate;
   - Otherwise:
     - Randomly select an **unsatisfied clause**, say \(c = x \lor y\);
     - **Uniformly at random** choose one variable from \(\{x, y\}\);
     - Flip that variable's assignment to obtain the new assignment \(\sigma_{t+1}\).

3. **Failure Output**

   If the iteration ends without finding a satisfying assignment, output:

   > "\(\varphi\) is not satisfiable".

---

### Time Complexity

- Each step checks at most \(m\) clauses;
- Total number of steps is \(O(n^2)\);

Therefore, the total time complexity of the algorithm is:
\[
O(n^2 \cdot m)
\]

---

### Correctness Guarantee

**Theorem**:
> If the 2-SAT instance is satisfiable, the algorithm outputs a correct satisfying assignment with probability at least \(1 - \frac{1}{100}\).

If the instance is unsatisfiable, the algorithm obviously will not erroneously output "satisfiable." Therefore, we only need to analyze the **probability of failure in the satisfiable case**.

---

### Overview of the Analysis

At first glance, this result seems counterintuitive:
- There are \(2^n\) possible assignments in total;
- There may be only a very few (or even exactly one) that satisfy the formula;
- Yet the algorithm only performs \(O(n^2)\) random walk steps and still finds a solution with high probability.

The key insight is:
- The algorithm does not independently sample random assignments;
- Rather, it is a **biased random walk process** that gradually "approaches" a satisfying assignment.

---

### Distance to the Target Solution

Fix a satisfying assignment \(\sigma\).

Define a sequence of random variables:
\[
X_t := |\{ v \in V \mid \sigma_t(v) = \sigma(v) \}|
\]

That is:
- \(X_t\) represents the **number of variables on which the current assignment agrees with the target assignment** \(\sigma\);
- Its range is \(0, 1, \dots, n\).

When \(X_t = n\), we have \(\sigma_t = \sigma\), and the algorithm succeeds.

---

### Key Property of a Single Step

When \(\sigma_t\) does not yet satisfy the formula:

- \(\mathbb{P}[X_{t+1} = X_t + 1 \mid \sigma_t] \ge \tfrac{1}{2}\)
- \(\mathbb{P}[X_{t+1} = X_t - 1 \mid \sigma_t] \le \tfrac{1}{2}\)

Intuitive explanation:
- We flip a variable from an unsatisfied clause;
- There is at least a 50% chance that the current assignment moves **closer** to some satisfying solution.

---

### Lower Bound via Random Walk Construction

Construct a one-dimensional random walk \(\{Y_t\}_{t \ge 0}\) on \(\{0,1,\dots,n\}\):

- \(Y_0 = X_0\);
- When \(0 < Y_t < n\):
  - Move right with probability \(\tfrac{1}{2}\);
  - Move left with probability \(\tfrac{1}{2}\);
- At the boundaries:
  - When \(Y_t = 0\), it must move right;
  - When \(Y_t = n\), it must move left.

By a coupling argument:
\[
Y_t \le X_t \quad \text{for all } t
\]

Therefore:
\[
\mathbb{P}(\exists t \le 100n^2 : X_t = n)
\;\ge\;
\mathbb{P}(\exists t \le 100n^2 : Y_t = n)
\]

---

### Hitting Time Analysis

Let \(T_{i \to n}\) be the first hitting time for the random walk from \(i\) to \(n\). We can compute:

\[
\mathbb{E}[T_{i \to n}] = n^2 - i^2 \le n^2
\]

Using **Markov's inequality**:
\[
\mathbb{P}(T_{i \to n} > 100n^2)
\le \frac{\mathbb{E}[T_{i \to n}]}{100n^2}
\le \frac{1}{100}
\]

---

### Final Conclusion

Combining the above analysis:

\[
\mathbb{P}(\text{algorithm finds a satisfying assignment within } 100n^2 \text{ steps})
\ge 1 - \frac{1}{100}
\]

That is:

> **The random walk algorithm solves 2-SAT with high probability in polynomial time.**

---

### Summary

- This algorithm is a classic example of **randomized algorithm + random walk analysis**;
- The key to its success is:
  - Random repair of unsatisfied clauses has a bias "toward the solution";
  - A one-dimensional symmetric random walk can be used for lower-bound analysis;
- While it is neither the optimal nor the most practical method for solving 2-SAT, it is theoretically elegant and demonstrates the power of probabilistic methods in algorithm design.
