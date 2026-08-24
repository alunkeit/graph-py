# Mathematics of Graph Traversals: BFS and DFS

This document details the mathematical formalisms, traversal invariants, edge classification theorems, and complexity analyses for **Breadth-First Search (BFS)** and **Depth-First Search (DFS)** as implemented in [`BreadthFirstSearch`](../graph/search/bfs.py) and [`DepthFirstSearch`](../graph/search/dfs.py).

---

## 1. Breadth-First Search (BFS)

### Formal Definition
Breadth-First Search systematically explores a graph $G = (V, E)$ starting from a source vertex $s \in V$ by discovering all vertices at distance $k$ from $s$ before discovering any vertices at distance $k+1$.

### Unweighted Shortest Path Theorem
Let $G = (V, E)$ be an unweighted graph (where each edge has implicit weight $w(e) = 1$). For every vertex $v \in V$, let $d(s, v)$ denote the shortest path distance in terms of edge count (hops).

> **Theorem (BFS Shortest Path Correctness)**:
> Upon termination of BFS initialized at source vertex $s$, for every reachable vertex $v \in V$, the computed distance $v.\text{dist}$ satisfies:
> $$v.\text{dist} = \delta(s, v)$$
> Furthermore, the precursor pointers formed by BFS yield a shortest path tree rooted at $s$.

#### Proof Sketch (Induction on Distance)
1. **Base Case**: At initialization, $s.\text{dist} = 0 = \delta(s, s)$.
2. **Inductive Step**: Assume for all vertices $u$ discovered at step $k$, $u.\text{dist} = \delta(s, u) = k$.
3. When relaxing an unvisited neighbor $v$ of $u$, we assign $v.\text{dist} = u.\text{dist} + 1 = k + 1$.
4. By the Triangle Inequality for unweighted graphs, $\delta(s, v) \le \delta(s, u) + 1 = k + 1$.
5. Since $v$ was not discovered at any step $< k + 1$, $\delta(s, v) \ge k + 1$.
6. Therefore, $v.\text{dist} = \delta(s, v) = k + 1$. $\blacksquare$

### Queue Monotonicity Invariant
At any point during BFS execution, the queue $Q = \langle q_1, q_2, \dots, q_r \rangle$ satisfies:
1. $q_1.\text{dist} \le q_2.\text{dist} \le \dots \le q_r.\text{dist}$
2. $q_r.\text{dist} \le q_1.\text{dist} + 1$

---

## 2. Depth-First Search (DFS)

### Formal Definition
Depth-First Search explores $G = (V, E)$ by searching deeper into the graph whenever possible, discovering unvisited neighbors of the most recently discovered vertex $u$ before backtracking.

### Timestamp Property & Parenthesis Theorem
For each vertex $u \in V$, DFS records two timestamps:
- $u.d$: Discovery time (when $u$ is first enqueued/pushed onto stack).
- $u.f$: Finishing time (when all neighbors of $u$ have been fully explored).

> **Theorem (Parenthesis Theorem)**:
> For any two vertices $u$ and $v$ in a DFS forest, exactly one of the following three conditions holds:
> 1. The intervals $[u.d, u.f]$ and $[v.d, v.f]$ are completely disjoint, and neither vertex is an ancestor of the other in the DFS forest.
> 2. The interval $[u.d, u.f]$ is strictly contained within $[v.d, v.f]$, and $u$ is a descendant of $v$ in the DFS forest.
> 3. The interval $[v.d, v.f]$ is strictly contained within $[u.d, u.f]$, and $v$ is a descendant of $u$ in the DFS forest.

### Edge Classification
DFS partitions graph edges $(u, v) \in E$ into four distinct structural classes:
1. **Tree Edges**: Edges in the DFS forest. Edge $(u, v)$ is a tree edge if $v$ was first discovered from $u$.
2. **Back Edges**: Edges $(u, v)$ connecting $u$ to an ancestor $v$ in a DFS tree. Self-loops are back edges.
3. **Forward Edges**: Non-tree edges $(u, v)$ connecting $u$ to a descendant $v$ in a DFS tree.
4. **Cross Edges**: All other edges. They connect vertices in different DFS trees or non-ancestor vertices in the same DFS tree.

> **Cycle Criterion Theorem**: A graph $G$ contains a cycle if and only if a DFS traversal produces at least one **Back Edge**.

---

## 3. Complexity Summary

| Algorithm | Time Complexity | Space Complexity | Best Suited For |
| :--- | :--- | :--- | :--- |
| **BFS** | $O(\|V\| + \|E\|)$ | $O(\|V\|)$ | Unweighted shortest paths, level-by-level traversal. |
| **DFS** | $O(\|V\| + \|E\|)$ | $O(\|V\|)$ | Cycle detection, topological structure analysis, component exploration. |
