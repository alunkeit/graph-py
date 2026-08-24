# Mathematics of Kruskal's MST & Union-Find

This document presents the matroid structure, cut/cycle properties, greedy correctness proofs, and disjoint-set amortized complexity analysis for **Kruskal's Minimum Spanning Tree Algorithm** as implemented in [`Kruskal`](../graph/search/kruskal.py).

---

## 1. Problem Formulation & Definitions

Let $G = (V, E)$ be a connected, undirected graph with real edge weight function $w: E \to \mathbb{R}$.

- **Spanning Tree**: A subgraph $T = (V, E_T)$ with $E_T \subseteq E$ such that $T$ is acyclic and connects all vertices in $V$. ($|E_T| = |V| - 1$).
- **Minimum Spanning Tree (MST)**: A spanning tree $T^*$ that minimizes total edge weight:
  $$w(T^*) = \sum_{e \in E_{T^*}} w(e) = \min_{T \text{ is a spanning tree}} \sum_{e \in E_T} w(e)$$

---

## 2. Fundamental Theorems: Cut & Cycle Properties

### Cut Property
A **cut** $(S, V \setminus S)$ is a partition of $V$ into two non-empty disjoint sets $S$ and $V \setminus S$.
An edge $e = (u, v)$ **crosses** the cut if $u \in S$ and $v \in V \setminus S$.

> **Theorem (Cut Property)**:
> For any cut $(S, V \setminus S)$ of $G$, if an edge $e^*$ is the strictly minimum-weight edge crossing the cut, then $e^*$ MUST belong to every Minimum Spanning Tree of $G$.

#### Proof Sketch
1. Suppose $T$ is an MST that does not contain $e^* = (u, v)$.
2. Adding $e^*$ to $T$ creates a unique simple cycle $C$ containing $e^*$.
3. Since $u \in S$ and $v \in V \setminus S$, cycle $C$ must cross the cut at least once more via another edge $e' = (x, y)$.
4. Removing $e'$ from $T \cup \{e^*\}$ yields a new spanning tree $T' = (T \setminus \{e'\}) \cup \{e^*\}$.
5. Total weight of $T'$:
   $$w(T') = w(T) - w(e') + w(e^*)$$
6. Since $e^*$ is the strictly minimum-weight edge crossing the cut, $w(e^*) < w(e')$, implying $w(T') < w(T)$.
7. This contradicts the assumption that $T$ was a Minimum Spanning Tree. Thus $e^*$ must belong to $T$. $\blacksquare$

### Cycle Property
> **Theorem (Cycle Property)**:
> For any simple cycle $C$ in $G$, if an edge $e^*$ is the strictly maximum-weight edge in $C$, then $e^*$ CANNOT belong to any Minimum Spanning Tree of $G$.

---

## 3. Kruskal's Greedy Algorithm Correctness

Kruskal's algorithm sorts all edges $E$ in non-decreasing order of weight:
$$w(e_1) \le w(e_2) \le \dots \le w(e_m)$$

It iterates through sorted edges, adding $e_i = (u, v)$ to $E_T$ if and only if $u$ and $v$ belong to different connected components (i.e. adding $e_i$ does not form a cycle).

> **Correctness Theorem**: Kruskal's greedy edge selection correctly constructs an MST $T^*$.

---

## 4. Disjoint-Set (Union-Find) Amortized Complexity

Kruskal's algorithm relies on a **Disjoint-Set (Union-Find)** data structure with two key optimizations:
1. **Path Compression**: During `find(i)`, flattens tree height by attaching visited nodes directly to the root.
2. **Union by Rank**: During `union(x, y)`, attaches the tree with smaller rank (height bound) under the root of the tree with larger rank.

### Inverse Ackermann Complexity Theorem
> **Theorem (Tarjan)**:
> A sequence of $m$ Disjoint-Set operations (`find`, `union`) on $n$ elements using path compression and rank optimization runs in time:
> $$O(m \cdot \alpha(n))$$
> where $\alpha(n)$ is the **inverse Ackermann function**.

For all practical values $n \le 10^{80}$ (atoms in the observable universe), $\alpha(n) \le 4$, making operations effectively $O(1)$ amortized time.

---

## 5. Total Complexity Summary

- **Sorting Edges**: $O(|E| \log |E|) = O(|E| \log |V|)$
- **Union-Find Operations**: $O(|E| \cdot \alpha(|V|))$
- **Total Time Complexity**:
  $$O(|E| \log |V|)$$
- **Space Complexity**: $O(|V| + |E|)$ for storing disjoint sets and edge lists.
