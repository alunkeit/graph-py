"""Implementation of edges in a graph structure."""
from __future__ import annotations
from typing import Any
from graph.types.node import Node

__author__ = "alunkeit"


class Edge:
    """Class representing an edge in the graph."""

    __slots__ = ("_name", "_s", "_t", "_directed", "_weight")

    def __init__(self, name: str, s: Node, t: Node, weight: float = 1.0, directed: bool = False) -> None:
        self._name: str = name
        self._s: Node = s
        self._t: Node = t
        self._weight: float = float(weight)
        self._directed: bool = directed
        s.add_edge(self)
        t.add_edge(self)

    def __repr__(self) -> str:
        if self._weight != 1.0:
            return f"{self._name}: {self._s.name} -> {self._t.name} (weight: {self._weight})"
        return f"{self._name}: {self._s.name} -> {self._t.name}"

    def __str__(self) -> str:
        return f"{self._s.name} -> {self._t.name}"

    @property
    def t(self) -> Node:
        return self._t

    @property
    def s(self) -> Node:
        return self._s

    @property
    def name(self) -> str:
        return self._name

    @property
    def weight(self) -> float:
        return self._weight

    @property
    def directed(self) -> bool:
        return self._directed

    def other(self, name: str) -> Node:
        if self._s.name == name:
            return self._t
        elif self._t.name == name:
            return self._s
        raise ValueError(
            f"Node '{name}' is not an endpoint of edge '{self._name}' "
            f"({self._s.name} -> {self._t.name})."
        )

    def is_directed(self) -> bool:
        return self._directed

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Edge):
            return NotImplemented
        return self._name == other._name

    def __hash__(self) -> int:
        return hash(self._name)


