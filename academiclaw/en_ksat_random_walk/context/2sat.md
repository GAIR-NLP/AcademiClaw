## 2 Random Walk Algorithm for 2-SAT

The SAT problem — determining whether a given CNF (Conjunctive Normal Form) formula is satisfiable — is a central problem in computer science. For any \(k \ge 2\), \(k\)-SAT is a special case of SAT in which each clause of the CNF formula consists of exactly \(k\) variables. For example,

\[
\varphi = (x \lor y) \land (y \lor z) \land (x \lor z)
\]

is a 2-CNF formula, and \(x = y = z = \text{true}\) is one of the assignments that satisfies it. SAT is NP-complete, and when \(k \ge 3\), \(k\)-SAT is also NP-complete. As we learned in the algorithms course, 2-SAT can be solved in linear time using an algorithm for finding strongly connected components. Today, we introduce a simple randomized algorithm that also solves this problem with high probability in polynomial time.

Let \(\varphi\) be a 2-CNF formula and \(V = \{v_1, v_2, \ldots, v_n\}\) be its set of variables. The algorithm proceeds as follows:

- Randomly choose an assignment \(\sigma_0 : V \to \{\text{true}, \text{false}\}\).

- For \(t = 0, 1, 2, \ldots, 100n^2\):

  - If \(\sigma_t\) satisfies \(\varphi\), output \(\sigma_t\);

  - Otherwise, randomly pick an unsatisfied clause, say \(c = x \lor y\). Uniformly at random choose one variable from \(\{x, y\}\) and flip its assignment. Denote the resulting assignment as \(\sigma_{t+1}\).

- Output "\(\varphi\) is not satisfiable".

The running time of this algorithm is clearly \(O(n^2 \cdot m)\), where \(m\) is the number of clauses in the formula. We now establish its correctness guarantee.

**Theorem 7.** The algorithm outputs the correct answer with probability at least \(1 - \tfrac{1}{100}\).

**Proof.** Clearly, if the 2-SAT input instance has no solution, then our algorithm always gives the correct answer. Therefore, we only need to consider the probability that the algorithm outputs "unsatisfiable" when the instance actually has a feasible assignment.

At first glance, this result seems somewhat strange, even counterintuitive: the total number of assignments is \(2^n\), and possibly only one of them satisfies the formula. Why can we, by randomly sampling only \(O(n^2)\) assignments, guarantee with high probability that we find the satisfying assignment?

Our algorithm generates \(100n^2 + 1\) assignments \(\sigma_0, \sigma_1, \ldots, \sigma_{100n^2}\). We will now show that, with probability at least \(1 - \tfrac{1}{100}\), some \(\sigma_k\) (where \(k \in \{0, \ldots, 100n^2\}\)) is a satisfying assignment. We fix an arbitrary satisfying assignment \(\sigma : V \to \{\text{true}, \text{false}\}\). In fact, we prove the following proposition: for sufficiently large \(k\), conditioned on the event that none of \(\sigma_0, \sigma_1, \ldots, \sigma_k\) is a satisfying assignment, the probability that \(\sigma_{k+1} = \sigma\) is high.

Let \(\{X_t\}_{t=0}^{100n^2}\) be a sequence of random variables, where

\[
X_t := |\{ v \in V \mid \sigma_t(v) = \sigma(v) \}|
\]

Note that \(\{X_t\}\) is not a Markov chain, because it only contains partial information about \(\sigma_t\), so we cannot determine the distribution of \(X_{t+1}\) from \(X_t\) alone. First, we verify that

\[
\mathbb{P}[X_{t+1} = X_t + 1 \mid \sigma_t] \ge \tfrac{1}{2}, \quad
\mathbb{P}[X_{t+1} = X_t - 1 \mid \sigma_t] \le \tfrac{1}{2}.
\]

Without loss of generality, assume that in round \(t\) we selected clause \(c = x \lor y\). Since \(\sigma_t\) does not satisfy \(c\), we have \(\sigma_t(x) = \sigma_t(y) = \text{false}\). Similarly, \(x \lor y\) is satisfied under \(\sigma\), so \(\sigma(x)\) and \(\sigma(y)\) have three possible assignments:

- If \(\sigma(x) = \text{true}\) and \(\sigma(y) = \text{false}\), then
  \(\mathbb{P}[X_{t+1} = X_t + 1 \mid \sigma_t] = \mathbb{P}[\text{flip } x] = \tfrac{1}{2}\),
  \(\mathbb{P}[X_{t+1} = X_t - 1 \mid \sigma_t] = \mathbb{P}[\text{flip } y] = \tfrac{1}{2}\).

- If \(\sigma(x) = \text{false}\) and \(\sigma(y) = \text{true}\), the same conclusion holds.

- If \(\sigma(x) = \text{true}\) and \(\sigma(y) = \text{true}\), then
  \(\mathbb{P}[X_{t+1} = X_t + 1 \mid \sigma_t] = 1\).

Therefore, conditioned on none of \(\sigma_0, \sigma_1, \ldots, \sigma_t\) being a satisfying assignment, we always have
\(\mathbb{P}[X_{t+1} = X_t + 1 \mid \sigma_t] \ge \tfrac{1}{2}\).

Consider the one-dimensional random walk \(\{Y_t\}_{t \ge 0}\) defined on \(\{0,1,\ldots,n\}\), where \(Y_0 = X_0\), and when \(Y_t \notin \{0,n\}\),

\[
Y_{t+1} = \begin{cases}
Y_t + 1, & \text{w.p. } \tfrac{1}{2}, \\
Y_t - 1, & \text{w.p. } \tfrac{1}{2}.
\end{cases}
\]

If \(Y_t = 0\), then \(Y_{t+1} = 1\); if \(Y_t = n\), then \(Y_{t+1} = n-1\). Then we have

\[
\mathbb{P}[\text{algorithm is correct}] \ge \mathbb{P}[\exists t \le 100n^2 : X_t = n]
\ge \mathbb{P}[\exists t \le 100n^2 : Y_t = n].
\]

Suppose initially \(Y_0 = X_0 = i\). Let \(T_{i \to n}\) denote the first hitting time from \(i\) to \(n\). Then

\[
\mathbb{E}[T_{i \to n}] = \sum_{k=i}^{n-1} \mathbb{E}[T_{k \to k+1}].
\]

For \(i > 0\),

\[
\mathbb{E}[T_{i \to i+1}] = 2 + \mathbb{E}[T_{i-1 \to i}],
\]

and \(T_{0 \to 1} = 1\). Therefore

\[
\mathbb{E}[T_{i \to n}] = \sum_{k=i}^{n-1} (2k + 1) = n^2 - i^2 \le n^2.
\]

By Markov's inequality,

\[
\mathbb{P}[T_{Y_0 \to n} > 100n^2] \le \frac{\mathbb{E}[T_{Y_0 \to n}]}{100n^2} \le \tfrac{1}{100}.
\]

Therefore

\[
\mathbb{P}[\text{algorithm outputs correct solution}] \ge 1 - \tfrac{1}{100}.
\]

Q.E.D.
