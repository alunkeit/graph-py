"""Implementation of Topological Sort for Directed Acyclic Graphs (DAGs)."""
from __future__ import annotations
from collections import deque
from typing import TYPE_CHECKING
from graph.search.base import SearchAlgorithm
from graph.types.node import Node

__author__ = "alunkeit"

if TYPE_CHECKING:
    from graph.types.graph import Graph


class TopologicalSort(SearchAlgorithm):
    """
    Class implementing Topological Sort using Kahn's Algorithm (indegree-based processing).
    
    Topological sorting produces a linear ordering of nodes in a Directed Acyclic Graph (DAG)
    such that for every directed edge u -> v, node u appears before node v.
    """

    def sort(self) -> list[Node]:
        """
        Computes a topological ordering of all nodes in the graph.

        :return: List of Node objects in topological order.
        :raises ValueError: If the graph is None or contains a cycle (not a DAG).
        """
        if self._graph is None:
            raise ValueError("Graph instance cannot be None.")

        # Compute in-degree for each node
        in_degree: dict[str, int] = {node_name: 0 for node_name in self._graph.nodes}
        for u_name, u_node in self._graph.nodes.items():
            for v_node, _edge in self._graph.get_neighbors(u_node):
                in_degree[v_node.name] += 1

        # Initialize queue with all nodes having in-degree = 0
        queue: deque[Node] = deque(
            [self._graph.node(name) for name, deg in in_degree.items() if deg == 0]
        )

        topological_order: list[Node] = []

        while queue:
            curr = queue.popleft()
            topological_order.append(curr)

            for neighbor, _edge in self._graph.get_neighbors(curr):
                in_degree[neighbor.name] -= 1
                if in_degree[neighbor.name] == 0:
                    queue.append(neighbor)

        # If topological order does not contain all nodes, a cycle exists
        if len(topological_order) != len(self._graph.nodes):
            raise ValueError("Graph contains a cycle and cannot be topologically sorted (not a DAG).")

        return topological_order

    def search(self, s: str | Node, t: str | Node) -> list[Node] | None:
        """
        Finds a valid path from start node s to target node t in DAG topological order.

        :param s: Start node or node name
        :param t: Target node or node name
        :return: List of Node objects on path from s to t, or None if no path exists.
        """
        if self._graph is None:
            raise ValueError("Graph instance cannot be None.")

        start_name = s.name if isinstance(s, Node) else s
        target_name = t.name if isinstance(t, Node) else t

        # Execute topological sort (verifies DAG property)
        order = self.sort()
        node_names = [n.name for n in order]

        if start_name not in node_names or target_name not in node_names:
            return None

        # Reachability via DAG DP
        parent: dict[str, Node | None] = {start_name: None}
        reachable = {start_name}

        for node in order:
            if node.name in reachable:
                for neighbor, _edge in self._graph.get_neighbors(node):
                    if neighbor.name not in reachable:
                        reachable.add(neighbor.name)
                        parent[neighbor.name] = node

        if target_name not in reachable:
            return None

        path: list[Node] = []
        curr_node: Node | None = self._graph.node(target_name)
        while curr_node is not None:
            path.append(curr_node)
            curr_node = parent.get(curr_node.name)

        return path[::-1]


# Alias for consistency
TopologicalSortSearch = TopologicalSort
