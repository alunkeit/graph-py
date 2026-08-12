"""Implementation of nodes in a graph structure."""
from __future__ import annotations
from typing import TYPE_CHECKING, Any

__author__ = "alunkeit"

if TYPE_CHECKING:
    from graph.types.edge import Edge


class Node:
    """Class representing a node in the graph."""

    __slots__ = ("_name", "_edges")

    def __init__(self, name: str) -> None:
        self._name: str = name
        self._edges: set[Edge] = set()

    def __repr__(self) -> str:
        return f"{self._name}"

    def __str__(self) -> str:
        return self._name

    def add_edge(self, edge: Edge) -> None:
        self._edges.add(edge)

    def remove_edge(self, edge: Edge) -> None:
        self._edges.discard(edge)

    def edge_count(self) -> int:
        return len(self._edges)

    def __len__(self) -> int:
        return len(self._edges)

    @property
    def name(self) -> str:
        return self._name

    @property
    def edges(self) -> set[Edge]:
        return self._edges

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Node):
            return NotImplemented
        return self._name == other._name

    def __hash__(self) -> int:
        return hash(self._name)
  


