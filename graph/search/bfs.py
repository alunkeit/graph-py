"""Implementation of Breadth-First Search (BFS)."""
from __future__ import annotations
from collections import deque
from typing import TYPE_CHECKING
from graph.search.base import SearchAlgorithm
from graph.types.node import Node

__author__ = "alunkeit"

if TYPE_CHECKING:
    from graph.types.graph import Graph


class BreadthFirstSearch(SearchAlgorithm):
    """Class implementing breadth-first search (BFS) on an instance of Graph."""

    def search(self, s: str | Node, t: str | Node) -> list[Node] | None:
        """
        Find the shortest path from start node s to target node t.

        :param s: Start node or name of the start node
        :param t: Target node or name of the target node
        :return: List of Node objects on the shortest path from s to t,
                 or None if no path exists.
        """
        if self._graph is None:
            raise ValueError("Graph instance cannot be None.")

        start_name = s.name if isinstance(s, Node) else s
        target_name = t.name if isinstance(t, Node) else t

        start_node = self._graph.node(start_name)
        target_node = self._graph.node(target_name)

        if start_node.name == target_node.name:
            return [start_node]

        queue: deque[Node] = deque([start_node])
        parent: dict[str, Node | None] = {start_node.name: None}

        while queue:
            current = queue.popleft()

            if current.name == target_node.name:
                path: list[Node] = []
                curr: Node | None = target_node
                while curr is not None:
                    path.append(curr)
                    curr = parent[curr.name]
                return path[::-1]

            for neighbor, _edge in self._graph.get_neighbors(current):
                if neighbor.name not in parent:
                    parent[neighbor.name] = current
                    queue.append(neighbor)

        return None
