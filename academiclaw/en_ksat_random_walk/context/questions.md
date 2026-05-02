## Problem 3 (Random Walk Algorithm for k-SAT)

In class, we covered the random walk algorithm for 2-SAT. In this problem, we extend it to the k-SAT problem, where
\(k \ge 3\) is a fixed constant. Since k-SAT is NP-complete when \(k \ge 3\), we cannot hope to design an algorithm that halts in polynomial time and outputs the correct answer with high probability, as that would imply
\(\mathrm{NP} = \mathrm{RP}\). However, we can still find algorithms whose exponential factor is better than brute-force enumeration. We use the same notation as in the lecture.

---

### 1.

In the 2-SAT algorithm introduced in class, we performed \(100n^2\) random variable-flip operations and proved that the probability of outputting the correct answer is \(\ge 1 - \frac{1}{100}\).

Consider the following approach to boost the success probability: repeat 50 times, each time independently generating a uniformly random initial assignment and performing \(2n^2\) random variable-flip operations (so the total number of operations remains \(100n^2\)). If a satisfying assignment is found in any run, output that assignment; if none is found across all runs, output "not satisfiable."

What is the minimum probability that this new 2-SAT algorithm outputs the correct answer?

---

### 2.

Now apply the algorithm from class to the k-SAT problem. Similarly, if \(\sigma_t\) is not a satisfying assignment, choose an unsatisfied clause, uniformly at random select one of its \(k\) variables, and flip its assignment to obtain \(\sigma_{t+1}\).

Prove that for any non-satisfying assignment \(\sigma_t\),

\[
\mathbb{P}\bigl[X_{t+1} = X_t + 1 \mid \sigma_t\bigr] \ge \frac{1}{k},
\quad
\mathbb{P}\bigl[X_{t+1} = X_t - 1 \mid \sigma_t\bigr] \le \frac{k-1}{k}.
\]

---

### 3.

Prove that after \(O((k-1)^n)\) random variable-flip operations, the algorithm outputs the correct answer with probability

\[
\ge 1 - \frac{1}{100}.
\]

Note that a brute-force algorithm enumerating all \(2^n\) possible assignments is no worse than \((k-1)^n\) in the exponential term. How can we obtain a more efficient algorithm?

A key observation is that we do not always start from \(X_0 = 0\); if \(\sigma_0\) is a uniformly random assignment,

\[
\mathbb{E}[X_0] = \frac{n}{2},
\]

and the closer we start to \(n\), the higher the probability that a fixed number of random walk steps will reach \(n\).

---

### 4. (Bonus Problem)

Prove that there exists a constant \(C > 0\) (depending only on \(k\)) such that if the initial assignment satisfies

\[
X_0 = n - i \quad (i > 0),
\]

then

\[
\mathbb{P}\bigl[\exists\, 1 \le t \le 3n,\; X_t = n\bigr]
\;\ge\;
\frac{C \cdot (k-1)^{-i}}{\sqrt{i}}.
\]

#### Hint

Consider a random walk on \(\mathbb{Z}\) with left-step probability \(\frac{k-1}{k}\) and right-step probability \(\frac{1}{k}\),
and the probability that among the first \(\frac{k}{k-2} \cdot i\) steps, exactly \(\frac{1}{k-2} \cdot i\) steps go left.

You may find the following approximation useful:

\[
n! = \sqrt{2\pi n}\left(\frac{n}{e}\right)^n (1 + o(1)).
\]

---

### 5.

Suppose the input k-CNF formula is satisfiable. Observe that \(X_t\) is more likely to decrease, and when \(t\) is large, \(X_t\) is more likely to be near 0. This suggests that we should not perform a long sequence of random flips starting from a single initial assignment.

Suppose we start from a uniformly random initial assignment \(\sigma_0\) and perform \(3n\) random variable-flip operations. Using the result of Problem 4, what is the minimum probability of finding a satisfying assignment?

---

### 6.

Design an algorithm that outputs the correct answer for the k-SAT problem with probability at least

\[
1 - \frac{1}{100}.
\]

Suppose your algorithm has running time at most

\[
\mathrm{poly}(|\varphi|)\cdot c^n,
\]

where \(\mathrm{poly}(|\varphi|)\) denotes a polynomial in the input formula length \(|\varphi|\).

What is the smallest constant \(c \in (1,2)\) (which may depend on \(k\)) that you can achieve?
