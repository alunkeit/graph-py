"""Implementation of the A* (A-Star) Pathfinding Algorithm."""
from __future__ import annotations
import heapq
from typing import TYPE_CHECKING, Callable
from graph.search.base import SearchAlgorithm
from graph.types.node import Node

__author__ = "alunkeit"

if TYPE_CHECKING:
    from graph.types.graph import Graph


class AStar(SearchAlgorithm):
    """
    Class implementing the A* (A-Star) Search Algorithm.
    
    A* uses a priority queue and a heuristic function h(n) to estimate the cost
    from node n to the target node, guiding the search efficiently: f(n) = g(n) + h(n).
    """

    def __init__(
        self,
        graph: Graph | None,
        heuristic: Callable[[Node, Node], float] | None = None,
    ) -> None:
        super().__init__(graph)
        # Default heuristic returns 0.0 (equivalent to Dijkstra)
        self._heuristic: Callable[[Node, Node], float] = (
            heuristic if heuristic is not None else (lambda _u, _v: 0.0)
        )

    @property
    def heuristic(self) -> Callable[[Node, Node], float]:
        return self._heuristic

    @heuristic.setter
    def heuristic(self, func: Callable[[Node, Node], float]) -> None:
        self._heuristic = func

    def search(self, s: str | Node, t: str | Node) -> list[Node] | None:
        """
        Find the shortest path from start node s to target node t using A* Search.

        :param s: Start node or name of the start node
        :param t: Target node or name of the target node
        :return: List of Node objects on the path from s to t, or None if no path exists.
        """
        path, _distance = self.search_with_distance(s, t)
        return path

    def search_with_distance(self, s: str | Node, t: str | Node) -> tuple[list[Node] | None, float]:
        """
        Find the shortest path and its total distance from start node s to target node t.

        :param s: Start node or name of start node
        :param t: Target node or name of target node
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

        # Priority Queue stores: (f_score, g_score, current_node_name)
        pq: list[tuple[float, float, str]] = []
        
        g_score: dict[str, float] = {start_node.name: 0.0}
        parent: dict[str, Node | None] = {start_node.name: None}
        visited: set[str] = set()

        h_start = self._heuristic(start_node, target_node)
        heapq.heappush(pq, (h_start, 0.0, start_node.name))

        while pq:
            f_curr, g_curr, curr_name = heapq.heappop(pq)

            if curr_name in visited:
                continue
            visited.add(curr_name)

            if curr_name == target_node.name:
                break

            curr_node = self._graph.node(curr_name)
            for neighbor, edge in self._graph.get_neighbors(curr_node):
                if neighbor.name in visited:
                    continue

                tentative_g = g_curr + edge.weight
                if tentative_g < g_score.get(neighbor.name, float("inf")):
                    g_score[neighbor.name] = tentative_g
                    parent[neighbor.name] = curr_node
                    h_val = self._heuristic(neighbor, target_node)
                    f_val = tentative_g + h_val
                    heapq.heappush(pq, (f_val, tentative_g, neighbor.name))

        if target_node.name not in g_score or target_node.name not in visited:
            return None, float("inf")

        path: list[Node] = []
        curr: Node | None = target_node
        while curr is not None:
            path.append(curr)
            curr = parent.get(curr.name)

        return path[::-1], g_score[target_node.name]


# Alias for consistency
AStarSearch = AStar
