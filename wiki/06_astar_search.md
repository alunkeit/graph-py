# Mathematics of A* Search & Heuristics

This document details the cost evaluation function, heuristic bounds, admissibility and consistency conditions, and search space pruning theory for **A\* (A-Star) Search** as implemented in [`AStar`](../graph/search/astar.py).

---

## 1. Cost Evaluation Function Formulation

A\* Search is a heuristic-guided graph pathfinding algorithm that extends Dijkstra's algorithm by using a heuristic function $h(n)$ to estimate the remaining cost to the target destination.

For any vertex $n \in V$, the evaluation function $f(n)$ is defined as:
$$f(n) = g(n) + h(n)$$

Where:
- $g(n)$: The exact cost of the path from start node $s$ to node $n$ computed so far.
- $h(n)$: The estimated cost of the cheapest path from node $n$ to target node $t$.
- $f(n)$: The estimated total cost of the cheapest path from $s$ to $t$ passing through node $n$.

---

## 2. Admissibility Condition (Optimality Theorem)

Let $h^*(n)$ denote the true, exact optimal path distance from node $n$ to target node $t$.

> **Definition (Admissible Heuristic)**:
> A heuristic function $h: V \to \mathbb{R}_{\ge 0}$ is **admissible** if it never overestimates the actual cost to reach the target:
> $$\forall n \in V, \quad 0 \le h(n) \le h^*(n)$$
> Additionally, $h(t) = 0$ at the target node.

> **Theorem (A\* Optimality under Admissibility)**:
> If the heuristic function $h(n)$ is admissible, A\* Search is guaranteed to return an **optimal shortest path**.

### Proof Sketch (Contradiction)
1. Let $t^*$ be an optimal target node with optimal cost $f^* = g(t^*) = h^*(s)$.
2. Suppose A\* terminates by selecting a sub-optimal target node $t'$ with cost $g(t') > f^*$.
3. Prior to choosing $t'$, there must exist an un-extracted node $n$ in the priority queue that lies on the true optimal path to $t^*$.
4. For this optimal path node $n$:
   $$f(n) = g(n) + h(n) \le g(n) + h^*(n) = f^*$$
5. Combining inequalities:
   $$f(n) \le f^* < g(t') = f(t')$$
6. Because A\* selects nodes from the priority queue in order of non-decreasing $f$-scores, node $n$ with $f(n) < f(t')$ would have been extracted before $t'$.
7. This contradicts the choice of $t'$. Therefore, A\* must return an optimal path. $\blacksquare$

---

## 3. Consistency (Monotonicity) Condition

> **Definition (Consistent / Monotonic Heuristic)**:
> A heuristic $h(n)$ is **consistent** (or monotonic) if for every node $u$ and every neighbor $v$ connected by edge $(u, v)$ with weight $w(u, v)$:
> $$h(u) \le w(u, v) + h(v)$$

### Consequences of Consistency
1. **Monotonic $f$-scores**: Along any path, $f(n)$ values are non-decreasing.
2. **No Re-opening of Nodes**: When A\* selects a node $u$ from the priority queue under a consistent heuristic, $g(u) = g^*(u)$ (its computed distance is optimal), so nodes never need to be re-visited or re-opened.
3. Every consistent heuristic is automatically admissible.

---

## 4. Special Cases & Heuristic Spectrum

The choice of heuristic $h(n)$ places A\* on a spectrum between BFS/Dijkstra and Greedy Best-First Search:

1. **$h(n) = 0$ for all $n$**:
   - Reduces $f(n) = g(n)$.
   - A\* becomes **Dijkstra's Algorithm**. (Guaranteed optimal, explores in all directions).
2. **$h(n) = h^*(n)$ (Exact Heuristic)**:
   - A\* explores only nodes directly along the optimal path without expanding extra nodes.
3. **$g(n) = 0$ ($f(n) = h(n)$)**:
   - A\* becomes **Greedy Best-First Search**. (Fast, but loses optimality guarantee).

---

## 5. Spatial Heuristics for 2D Maps

For 2D grid/spatial maps (such as [`WAYPOINT_COORDINATES`](../graph/demo/astar_demo.py#L21)):

- **Euclidean Distance** (Allowed in any continuous 2D space):
  $$h(u, v) = \sqrt{(x_v - x_u)^2 + (y_v - y_u)^2}$$
- **Manhattan Distance** (Grid with 4-directional movement):
  $$h(u, v) = |x_v - x_u| + |y_v - y_u|$$

Both Euclidean and Manhattan distances obey the Triangle Inequality and are consistent/admissible heuristics.
