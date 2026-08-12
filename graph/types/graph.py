"""Implementation of undirected graphs for algorithm demonstration."""
from __future__ import annotations
from types import MappingProxyType
from typing import Iterator

__author__ = "alunkeit"

from graph.types.node import Node
from graph.types.edge import Edge


class UndirectedGraph:
    """Class representing an undirected graph."""

    def __init__(self, edges: list[Edge] | None = None, nodes: dict[str, Node] | None = None) -> None:
        self._edges: list[Edge] = edges if edges is not None else []
        self._nodes: dict[str, Node] = nodes if nodes is not None else {}

    def __repr__(self) -> str:
        return f"<UndirectedGraph({len(self._edges)} _edges, {len(self._nodes)} _nodes)>"

    def __str__(self) -> str:
        return f"UndirectedGraph({len(self._edges)} _edges, {len(self._nodes)} _nodes)"

    @property
    def nodes(self) -> dict[str, Node]:
        return self._nodes

    @property
    def edges(self) -> list[Edge]:
        return self._edges

    def insert_from_nodes(self, name: str, s: Node, t: Node) -> None:
        """
        Insert an edge given its two endpoint nodes.

        Reuses an existing node with the same name instead of overwriting
        it to ensure node edge lists remain synchronized.
        """
        s = self._nodes.setdefault(s.name, s)
        t = self._nodes.setdefault(t.name, t)
        self._edges.append(Edge(name, s, t))

    def insert_edge(self, e: Edge) -> None:
        """
        Insert an edge into the graph.

        :param e: The edge to insert
        """
        self._edges.append(e)

        if e.s.name not in self._nodes:
            self._nodes[e.s.name] = e.s
        elif self._nodes[e.s.name] is not e.s:
            self._nodes[e.s.name].add_edge(e)

        if e.t.name not in self._nodes:
            self._nodes[e.t.name] = e.t
        elif self._nodes[e.t.name] is not e.t:
            self._nodes[e.t.name].add_edge(e)

    def node(self, name: str) -> Node:
        """
        Get a node by its name.

        :param name: The name of the node
        :return: The node with the given name
        """
        try:
            return self._nodes[name]
        except KeyError:
            raise KeyError(f"No node with name '{name}' exists in the graph.") from None

    def remove_edge(self, edge: Edge) -> None:
        """
        Remove an edge completely from the graph and endpoint nodes.
        """
        edge.s.remove_edge(edge)
        edge.t.remove_edge(edge)
        if edge in self._edges:
            self._edges.remove(edge)

    def __getitem__(self, name: str) -> Node:
        """Allows access via graph["n0"] instead of graph.node("n0")."""
        return self.node(name)

    def __contains__(self, item: str | Node) -> bool:
        """Allows 'n0' in graph or node in graph."""
        if isinstance(item, Node):
            return item.name in self._nodes
        return item in self._nodes

    def __len__(self) -> int:
        """Returns the number of nodes in the graph."""
        return len(self._nodes)

    def __iter__(self) -> Iterator[Node]:
        """Allows 'for node in graph:'."""
        return iter(self._nodes.values())


