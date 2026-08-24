# Mathematics of Bellman-Ford & Negative Cycles

This document presents the mathematical structure, dynamic programming formulation, negative cycle detection theorems, and financial currency arbitrage transformations for the **Bellman-Ford Algorithm** as implemented in [`BellmanFord`](../graph/search/bellman_ford.py).

---

## 1. Problem Formulation & Dynamic Programming Recurrence

Unlike Dijkstra's algorithm, the Bellman-Ford algorithm handles general edge weights $w: E \to \mathbb{R}$, supporting both positive and **negative edge weights**.

### DP Recurrence Relation
Let $d^{(k)}[v]$ denote the length of the shortest path from source $s$ to vertex $v$ using **at most $k$ edges**.

$$\begin{aligned}
d^{(0)}[s] &= 0 \\
d^{(0)}[v] &= \infty \quad \text{for all } v \neq s \\
d^{(k)}[v] &= \min \left( d^{(k-1)}[v], \min_{(u, v) \in E} \left( d^{(k-1)}[u] + w(u, v) \right) \right)
\end{aligned}$$

Since any simple shortest path in a graph with $|V|$ vertices contains at most $|V| - 1$ edges, relaxing all edges $|V| - 1$ times computes exact shortest paths if no negative weight cycles exist.

---

## 2. Negative Weight Cycle Theorem

A **negative weight cycle** is a directed cycle $C = \langle v_0, v_1, \dots, v_k, v_0 \rangle$ such that:
$$w(C) = \sum_{i=1}^k w(v_{i-1}, v_i) < 0$$

If such a cycle is reachable from source $s$, shortest path distances to vertices on or reachable from $C$ become $-\infty$.

> **Theorem (Negative Cycle Detection)**:
> If no negative weight cycle reachable from $s$ exists in $G$, then after $|V| - 1$ relaxation passes, $d[v] = \delta(s, v)$ for all $v \in V$.
> If an edge $(u, v) \in E$ can STILL be relaxed on pass $|V|$ (i.e. $d[u] + w(u, v) < d[v]$), then $G$ contains a negative weight cycle reachable from $s$.

### Proof Sketch
1. Suppose no edge can be relaxed on pass $|V|$. Then for all $(u, v) \in E$, $d[v] \le d[u] + w(u, v)$.
2. For any cycle $C = \langle v_0, v_1, \dots, v_k, v_0 \rangle$, summing the relaxation inequalities around the cycle gives:
   $$\sum_{i=1}^k d[v_i] \le \sum_{i=1}^k d[v_{i-1}] + \sum_{i=1}^k w(v_{i-1}, v_i)$$
3. Since $\sum d[v_i] = \sum d[v_{i-1}]$, canceling terms yields:
   $$0 \le w(C)$$
4. Therefore, no cycle $C$ in $G$ can have negative weight $w(C) < 0$. Conversely, if $d[u] + w(u, v) < d[v]$ holds on pass $|V|$, a negative weight cycle must exist. $\blacksquare$

---

## 3. Financial Currency Arbitrage Logarithmic Transformation

In foreign exchange (Forex) markets, an arbitrage opportunity exists if a chain of conversions yields a net profit multiplier $> 1.0$:
$$R_{\text{total}} = r_{c_1 \to c_2} \times r_{c_2 \to c_3} \times \dots \times r_{c_k \to c_1} > 1.0$$

### Mathematical Reduction to Negative Weight Cycles
By taking the negative natural logarithm of exchange rates:
$$w(u \to v) = -\ln(r_{u \to v})$$

The product of exchange rates transforms into a sum of logarithmic edge weights:
$$\sum_{i=1}^k w(e_i) = \sum_{i=1}^k -\ln(r_i) = -\ln \left( \prod_{i=1}^k r_i \right) = -\ln(R_{\text{total}})$$

### Equivalence Condition
$$R_{\text{total}} > 1.0 \iff \ln(R_{\text{total}}) > 0 \iff -\ln(R_{\text{total}}) < 0 \iff \sum w(e_i) < 0$$

Thus, detecting a profitable currency arbitrage loop is **mathematically identical** to finding a negative weight cycle using the Bellman-Ford algorithm!

---

## 4. Complexity Analysis

- **Time Complexity**: $O(|V| \cdot |E|)$ (relaxes $|E|$ edges for $|V|-1$ passes, plus 1 validation pass).
- **Space Complexity**: $O(|V|)$ to maintain distance and parent pointer arrays.
