"""Implementation of Kruskal's Minimum Spanning Tree (MST) Algorithm."""
from __future__ import annotations
from typing import TYPE_CHECKING
from graph.types.node import Node
from graph.types.edge import Edge

__author__ = "alunkeit"

if TYPE_CHECKING:
    from graph.types.graph import Graph


class DisjointSet:
    """Disjoint-Set (Union-Find) data structure with path compression and rank optimization."""

    def __init__(self, elements: list[str]) -> None:
        self.parent: dict[str, str] = {el: el for el in elements}
        self.rank: dict[str, int] = {el: 0 for el in elements}

    def find(self, i: str) -> str:
        """Finds root of set containing element i with path compression."""
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, x: str, y: str) -> bool:
        """Unites sets containing x and y. Returns True if united, False if already in same set."""
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False

        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        return True


class Kruskal:
    """
    Class implementing Kruskal's algorithm to compute the Minimum Spanning Tree (MST)
    for connected undirected weighted graphs.
    """

    def __init__(self, graph: Graph | None) -> None:
        self._graph: Graph | None = graph

    @property
    def graph(self) -> Graph | None:
        return self._graph

    def compute_mst(self) -> tuple[list[Edge], float]:
        """
        Computes the Minimum Spanning Tree of the graph.

        :return: Tuple of (mst_edges, total_weight)
        :raises ValueError: If graph is None or graph is disconnected.
        """
        if self._graph is None:
            raise ValueError("Graph instance cannot be None.")

        node_names = list(self._graph.nodes.keys())
        if not node_names:
            return [], 0.0

        ds = DisjointSet(node_names)

        # Sort all edges by weight
        sorted_edges = sorted(self._graph.edges, key=lambda e: e.weight)

        mst_edges: list[Edge] = []
        total_weight: float = 0.0

        for edge in sorted_edges:
            if ds.union(edge.s.name, edge.t.name):
                mst_edges.append(edge)
                total_weight += edge.weight

            if len(mst_edges) == len(node_names) - 1:
                break

        return mst_edges, total_weight


# Alias for consistency
KruskalMST = Kruskal
