# Mathematics of Topological Sorting & DAGs

This document details the algebraic order theory, acyclicity properties, and queue invariants for **Topological Sort** as implemented in [`TopologicalSort`](../graph/search/topological_sort.py).

---

## 1. Strict Partial Ordering on DAGs

Let $G = (V, E)$ be a **Directed Acyclic Graph (DAG)**.

### Strict Partial Order Relation
We define a binary relation $\prec$ on $V$ such that $u \prec v$ if and only if there exists a directed path from $u$ to $v$ in $G$ ($u \overset{+}{\rightsquigarrow} v$).

The relation $\prec$ satisfies:
1. **Irreflexivity**: $\neg(u \prec u)$ for all $u \in V$ (no self-loops or cycles).
2. **Asymmetry**: If $u \prec v$, then $\neg(v \prec u)$.
3. **Transitivity**: If $u \prec v$ and $v \prec w$, then $u \prec w$.

### Definition of Topological Sort
A **Topological Sort** of a DAG $G = (V, E)$ is a linear extension of the strict partial order $\prec$ into a total order $\le_T = \langle v_1, v_2, \dots, v_n \rangle$ such that:
$$\forall (u, v) \in E \implies u \le_T v \quad (u \text{ appears before } v \text{ in the linear order})$$

---

## 2. Kahn's Algorithm (In-Degree Reduction)

### In-Degree Definition
For a vertex $v \in V$, the in-degree $\text{in-deg}(v)$ is the number of incoming directed edges:
$$\text{in-deg}(v) = | \{ u \in V : (u, v) \in E \} |$$

> **Lemma (Minimal Element Existence)**: Every finite non-empty DAG $G = (V, E)$ contains at least one vertex $v \in V$ with $\text{in-deg}(v) = 0$.

#### Proof Sketch
1. Pick any vertex $v_0 \in V$. If $\text{in-deg}(v_0) = 0$, we are done.
2. Otherwise, pick an incoming neighbor $v_1$ such that $(v_1, v_0) \in E$.
3. Repeat this process to form a path $\dots \to v_2 \to v_1 \to v_0$.
4. Since $V$ is finite, this process must either revisit a vertex (forming a directed cycle) or terminate at a vertex with in-degree 0.
5. Since $G$ is acyclic (no cycles), the process cannot revisit a vertex. Thus it must terminate at a vertex $v$ with $\text{in-deg}(v) = 0$. $\blacksquare$

---

## 3. Algorithm Invariants & Acyclicity Criterion

Kahn's algorithm repeatedly removes vertices with in-degree 0 and decrements the in-degrees of their outgoing neighbors.

### Algorithm Invariant
At step $k$:
- All vertices currently in the output sequence $L = \langle v_1, \dots, v_k \rangle$ have had all their incoming edge dependencies fully satisfied.
- The remaining subgraph $G_k = G \setminus L$ remains a valid DAG.

> **Theorem (Acyclicity & Cycle Detection)**:
> The topological sort output sequence $L$ contains all $|V|$ vertices if and only if $G$ is a Directed Acyclic Graph (DAG).
> If $|L| < |V|$ upon queue exhaustion, $G$ contains at least one directed cycle.

---

## 4. Complexity Analysis

- **In-Degree Computation**: Inspects all $|V|$ nodes and $|E|$ edges $\implies O(|V| + |E|)$.
- **Queue Operations**: Each vertex is enqueued and dequeued exactly once $\implies O(|V|)$.
- **Edge Reductions**: Each edge is traversed and decremented exactly once $\implies O(|E|)$.
- **Total Time Complexity**: $O(|V| + |E|)$
- **Space Complexity**: $O(|V|)$ for storing in-degrees, queue state, and output list.
