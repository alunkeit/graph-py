"""Implementation of Dijkstra's Shortest Path Algorithm."""
from __future__ import annotations
import heapq
from typing import TYPE_CHECKING
from graph.search.base import SearchAlgorithm
from graph.types.node import Node

__author__ = "alunkeit"

if TYPE_CHECKING:
    from graph.types.graph import Graph


class Dijkstra(SearchAlgorithm):
    """
    Class implementing Dijkstra's algorithm to find shortest paths in weighted graphs.
    """

    def search(self, s: str | Node, t: str | Node) -> list[Node] | None:
        """
        Find the shortest path from start node s to target node t using Dijkstra's algorithm.

        :param s: Start node or name of the start node
        :param t: Target node or name of the target node
        :return: List of Node objects on the shortest path from s to t,
                 or None if no path exists.
        """
        path, _distance = self.search_with_distance(s, t)
        return path

    def search_with_distance(self, s: str | Node, t: str | Node) -> tuple[list[Node] | None, float]:
        """
        Find the shortest path and its total distance from start node s to target node t.

        :param s: Start node or name of the start node
        :param t: Target node or name of the target node
        :return: Tuple of (path_nodes, total_distance). If no path exists, returns (None, float('inf')).
        """
        if self._graph is None:
            raise ValueError("Graph instance cannot be None.")

        start_name = s.name if isinstance(s, Node) else s
        target_name = t.name if isinstance(t, Node) else t

        start_node = self._graph.node(start_name)
        target_node = self._graph.node(target_name)

        if start_node.name == target_node.name:
            return [start_node], 0.0

        distances: dict[str, float] = {start_node.name: 0.0}
        parent: dict[str, Node | None] = {start_node.name: None}
        visited: set[str] = set()

        # Priority queue stores tuples: (distance, insertion_counter, node)
        counter = 0
        pq: list[tuple[float, int, Node]] = [(0.0, counter, start_node)]

        while pq:
            curr_dist, _, current = heapq.heappop(pq)

            if current.name in visited:
                continue
            visited.add(current.name)

            if current.name == target_node.name:
                break

            for neighbor, edge in self._graph.get_neighbors(current):
                if edge.weight < 0:
                    raise ValueError(
                        f"Dijkstra's algorithm does not support negative edge weights "
                        f"(edge '{edge.name}' has weight {edge.weight})."
                    )

                new_dist = curr_dist + edge.weight
                if neighbor.name not in distances or new_dist < distances[neighbor.name]:
                    distances[neighbor.name] = new_dist
                    parent[neighbor.name] = current
                    counter += 1
                    heapq.heappush(pq, (new_dist, counter, neighbor))

        if target_node.name not in visited:
            return None, float("inf")

        path: list[Node] = []
        curr: Node | None = target_node
        while curr is not None:
            path.append(curr)
            curr = parent[curr.name]

        return path[::-1], distances[target_node.name]


# Alias for consistency
DijkstraSearch = Dijkstra
