# Mathematics of Dijkstra's Algorithm

This document provides the mathematical foundation, greedy choice proof, relaxation invariants, and complexity formulation for **Dijkstra's Shortest Path Algorithm** as implemented in [`Dijkstra`](../graph/search/dijkstra.py).

---

## 1. Problem Formulation & Constraints

Given a weighted graph $G = (V, E)$ with edge weight function $w: E \to \mathbb{R}$ and source vertex $s \in V$:
- **Non-Negative Weight Constraint**: $w(u, v) \ge 0$ for all $(u, v) \in E$.
- **Goal**: Compute the shortest path distance $\delta(s, v)$ for all $v \in V$:
  $$\delta(s, v) = \min \{ w(p) : s \overset{p}{\rightsquigarrow} v \}$$

---

## 2. Mathematical Invariants & Edge Relaxation

### Triangle Inequality Theorem
For any edge $(u, v) \in E$, the true shortest path distances satisfy:
$$\delta(s, v) \le \delta(s, u) + w(u, v)$$

### Edge Relaxation Invariant
Dijkstra's algorithm maintains an upper bound estimate $d[v]$ of the shortest path distance from $s$ to $v$.
The operation **Relax(u, v)** updates $d[v]$:

$$\text{Relax}(u, v): \quad \text{if } d[u] + w(u, v) < d[v] \text{ then } d[v] \gets d[u] + w(u, v)$$

> **Invariant 1 (Upper Bound Property)**:
> At all times during execution, $d[v] \ge \delta(s, v)$ for all $v \in V$. Once $d[v] = \delta(s, v)$, its value never changes.

---

## 3. Correctness Proof (Greedy Choice Property)

Let $S \subseteq V$ be the set of vertices whose final shortest path distances have been determined.

> **Theorem (Dijkstra's Correctness)**:
> When a vertex $u \in V \setminus S$ with the minimum tentative distance $d[u]$ is selected and added to $S$, its tentative distance is exact:
> $$d[u] = \delta(s, u)$$

### Proof by Contradiction
1. Suppose $u$ is the first vertex added to $S$ for which $d[u] \neq \delta(s, u)$.
2. Since $d[u] \ge \delta(s, u)$ (Upper Bound Property), it must be that $d[u] > \delta(s, u)$.
3. Consider a true shortest path $p$ from $s$ to $u$. Path $p$ starts in $S$ at $s$ and leaves $S$ to reach $u \notin S$.
4. Let $(x, y)$ be the first edge along path $p$ such that $x \in S$ and $y \notin S$.
5. Because $x \in S$, by inductive hypothesis $d[x] = \delta(s, x)$. When $x$ was added to $S$, edge $(x, y)$ was relaxed, so:
   $$d[y] \le d[x] + w(x, y) = \delta(s, x) + w(x, y) = \delta(s, y)$$
6. Because edge weights are non-negative ($w(e) \ge 0$), distance along path $p$ cannot decrease:
   $$\delta(s, y) \le \delta(s, u)$$
7. Combining inequalities:
   $$d[y] \le \delta(s, y) \le \delta(s, u) < d[u]$$
8. Hence $d[y] < d[u]$. But Dijkstra selected $u$ from $V \setminus S$ because $u$ had the minimum tentative distance $d$, contradicting $d[y] < d[u]$.
9. Therefore, $d[u] = \delta(s, u)$. $\blacksquare$

---

## 4. Failure on Negative Edge Weights

If negative edge weights exist ($w(u, v) < 0$), the non-decreasing distance assumption $\delta(s, y) \le \delta(s, u)$ fails. Once a vertex $u$ is added to $S$, Dijkstra never re-evaluates edges originating from $u$, which can miss shorter paths formed by subsequent negative edges.

*(For graphs with negative edge weights, use the [Bellman-Ford Algorithm](03_bellman_ford.md)).*

---

## 5. Complexity Analysis

Using a Min-Heap (Priority Queue, as implemented in `heapq` in `graph-py`):
- **Vertex Insertions / Extractions**: $|V|$ extractions from min-heap $\implies O(|V| \log |V|)$.
- **Edge Relaxations**: At most $|E|$ decrease-key / insertion operations $\implies O(|E| \log |V|)$.
- **Total Time Complexity**:
  $$O((|V| + |E|) \log |V|)$$
- **Space Complexity**: $O(|V|)$ to store distance dictionaries, parent maps, and heap elements.
