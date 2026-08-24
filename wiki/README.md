# Graph-Py Mathematical Wiki

Welcome to the **Graph-Py Mathematical Wiki**. This documentation suite provides rigorous mathematical definitions, formal theorems, complexity analyses, and proofs for all graph data structures and search algorithms implemented in [`graph-py`](../README.md).

---

## Table of Contents

| Topic | Article | Primary Mathematical Concepts |
| :--- | :--- | :--- |
| **01. Graph Traversals** | [Graph Traversals: BFS & DFS](01_bfs_dfs.md) | Unweighted shortest path theorem, queue/stack state invariants, tree/back edge classification. |
| **02. Dijkstra's Algorithm** | [Dijkstra's Algorithm](02_dijkstra.md) | Relaxation invariant $d(v) \le d(u) + w(u, v)$, non-negative weight constraint $w(e) \ge 0$, min-heap complexity. |
| **03. Bellman-Ford & Negative Cycles** | [Bellman-Ford & Arbitrage](03_bellman_ford.md) | Dynamic programming formulation, $|V|$-th relaxation pass, negative cycle theorem, Forex logarithmic mapping $w = -\ln(r)$. |
| **04. Topological Sort** | [Topological Sort & DAGs](04_topological_sort.md) | Strict partial ordering $\preceq$ on DAGs, Kahn's in-degree reduction invariant, acyclicity cycle detection. |
| **05. Kruskal's MST** | [Kruskal's MST & Union-Find](05_kruskal_mst.md) | Cut & Cycle properties of MSTs, Disjoint-Set Union-Find with path compression and rank optimization $\alpha(|V|)$. |
| **06. A\* Search** | [A\* Search & Heuristics](06_astar_search.md) | Cost function $f(n) = g(n) + h(n)$, admissibility condition $h(n) \le h^*(n)$, consistency / monotonicity $h(u) \le w(u,v) + h(v)$. |

---

## Formal Notation & Definitions

Throughout this mathematical wiki, we adopt standard graph theory notation:

- **Graph**: $G = (V, E)$, where $V$ is the set of vertices (nodes) and $E$ is the set of edges.
  - $|V| = n$: Number of vertices.
  - $|E| = m$: Number of edges.
- **Directed Graph**: $E \subseteq V \times V$, where edges $(u, v)$ have direction from $u$ to $v$.
- **Undirected Graph**: Edges $\{u, v\}$ are unordered pairs of vertices.
- **Edge Weight Function**: $w: E \to \mathbb{R}$, assigning a real-valued scalar weight $w(u, v)$ to edge $(u, v)$.
- **Path**: A sequence of vertices $p = \langle v_0, v_1, \dots, v_k \rangle$ such that $(v_{i-1}, v_i) \in E$ for all $1 \le i \le k$.
- **Path Weight**: The sum of weights along path $p$:
  $$w(p) = \sum_{i=1}^k w(v_{i-1}, v_i)$$
- **Shortest Path Distance**: The minimum weight over all valid paths from $u$ to $v$:
  $$\delta(u, v) = \begin{cases} \min \{ w(p) : u \overset{p}{\rightsquigarrow} v \} & \text{if a path exists} \\ \infty & \text{otherwise} \end{cases}$$
