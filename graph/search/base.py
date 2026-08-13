"""Base class for graph search algorithms."""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

__author__ = "alunkeit"

from graph.types.node import Node

if TYPE_CHECKING:
    from graph.types.graph import Graph


class SearchAlgorithm(ABC):
    """Abstract base class for graph search algorithms."""

    def __init__(self, graph: Graph | None) -> None:
        self._graph: Graph | None = graph

    @property
    def graph(self) -> Graph | None:
        return self._graph

    @abstractmethod
    def search(self, s: str | Node, t: str | Node) -> list[Node] | None:
        """
        Find a path from start node s to target node t.

        :param s: Start node or name of start node
        :param t: Target node or name of target node
        :return: List of Node objects on path from s to t, or None if no path exists.
        """
        if self._graph is None:
            raise ValueError("Graph instance cannot be None.")
