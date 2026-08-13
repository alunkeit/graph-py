"""Implementation of the Bellman-Ford Shortest Path Algorithm."""
from __future__ import annotations
from typing import TYPE_CHECKING
from graph.search.base import SearchAlgorithm
from graph.types.node import Node

__author__ = "alunkeit"

if TYPE_CHECKING:
    from graph.types.graph import Graph


class BellmanFord(SearchAlgorithm):
    """
    Class implementing the Bellman-Ford algorithm to find shortest paths
    in graphs with positive or negative edge weights, and detect negative weight cycles.
    """

    def search(self, s: str | Node, t: str | Node) -> list[Node] | None:
        """
        Find the shortest path from start node s to target node t using the Bellman-Ford algorithm.

        :param s: Start node or name of the start node
        :param t: Target node or name of the target node
        :return: List of Node objects on the shortest path from s to t,
                 or None if no path exists.
        :raises ValueError: If a negative weight cycle is reachable from source node s.
        """
        path, _distance = self.search_with_distance(s, t)
        return path

    def search_with_distance(self, s: str | Node, t: str | Node) -> tuple[list[Node] | None, float]:
        """
        Find the shortest path and its total distance from start node s to target node t.

        :param s: Start node or name of the start node
        :param t: Target node or name of the target node
        :return: Tuple of (path_nodes, total_distance). If no path exists, returns (None, float('inf')).
        :raises ValueError: If a negative weight cycle is reachable from source node s.
        """
        if self._graph is None:
            raise ValueError("Graph instance cannot be None.")

        start_name = s.name if isinstance(s, Node) else s
        target_name = t.name if isinstance(t, Node) else t

        start_node = self._graph.node(start_name)
        target_node = self._graph.node(target_name)

        if start_node.name == target_node.name:
            return [start_node], 0.0

        num_nodes = len(self._graph.nodes)
        distances: dict[str, float] = {n_name: float("inf") for n_name in self._graph.nodes}
        distances[start_node.name] = 0.0
        parent: dict[str, Node | None] = {start_node.name: None}

        # Relax edges up to |V| - 1 times
        for _ in range(num_nodes - 1):
            changed = False
            for u_name, u_node in self._graph.nodes.items():
                if distances[u_name] == float("inf"):
                    continue

                for v_node, edge in self._graph.get_neighbors(u_node):
                    new_dist = distances[u_name] + edge.weight
                    if new_dist < distances[v_node.name]:
                        distances[v_node.name] = new_dist
                        parent[v_node.name] = u_node
                        changed = True

            if not changed:
                break

        # Pass |V|: Check for negative weight cycles reachable from start node
        for u_name, u_node in self._graph.nodes.items():
            if distances[u_name] == float("inf"):
                continue

            for v_node, edge in self._graph.get_neighbors(u_node):
                if distances[u_name] + edge.weight < distances[v_node.name]:
                    raise ValueError(
                        f"Graph contains a negative weight cycle reachable from source node '{start_node.name}'."
                    )

        if target_node.name not in distances or distances[target_node.name] == float("inf"):
            return None, float("inf")

        path: list[Node] = []
        curr: Node | None = target_node
        while curr is not None:
            path.append(curr)
            curr = parent.get(curr.name)

        return path[::-1], distances[target_node.name]


# Alias for consistency
BellmanFordSearch = BellmanFord
