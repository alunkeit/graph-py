"""Implementation of graph data structures for algorithm demonstration."""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Iterator

__author__ = "alunkeit"

from graph.types.node import Node
from graph.types.edge import Edge


class Graph(ABC):
    """Abstract base class representing a graph data structure."""

    def __init__(self, edges: list[Edge] | None = None, nodes: dict[str, Node] | None = None) -> None:
        self._edges: list[Edge] = edges if edges is not None else []
        self._nodes: dict[str, Node] = nodes if nodes is not None else {}

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({len(self._edges)} _edges, {len(self._nodes)} _nodes)>"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({len(self._edges)} _edges, {len(self._nodes)} _nodes)"

    @property
    def nodes(self) -> dict[str, Node]:
        return self._nodes

    @property
    def edges(self) -> list[Edge]:
        return self._edges

    @property
    @abstractmethod
    def is_directed(self) -> bool:
        """Return True if the graph is directed, False otherwise."""

    @abstractmethod
    def get_neighbors(self, node: str | Node) -> list[tuple[Node, Edge]]:
        """
        Get outgoing neighbor nodes and connecting edges for a given node.

        :param node: Node object or node name.
        :return: List of tuples (neighbor_node, connecting_edge).
        """

    def insert_from_nodes(self, name: str, s: Node, t: Node, weight: float = 1.0) -> None:
        """
        Insert an edge given its two endpoint nodes.

        Reuses an existing node with the same name instead of overwriting
        it to ensure node edge lists remain synchronized.
        """
        s = self._nodes.setdefault(s.name, s)
        t = self._nodes.setdefault(t.name, t)
        self.insert_edge(Edge(name, s, t, weight=weight, directed=self.is_directed))

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


class UndirectedGraph(Graph):
    """Class representing an undirected graph."""

    @property
    def is_directed(self) -> bool:
        return False

    def get_neighbors(self, node: str | Node) -> list[tuple[Node, Edge]]:
        n = self.node(node.name) if isinstance(node, Node) else self.node(node)
        neighbors: list[tuple[Node, Edge]] = []
        for edge in n.edges:
            neighbor = edge.other(n.name)
            neighbors.append((neighbor, edge))
        return neighbors


class DirectedGraph(Graph):
    """Class representing a directed graph."""

    @property
    def is_directed(self) -> bool:
        return True

    def get_neighbors(self, node: str | Node) -> list[tuple[Node, Edge]]:
        n = self.node(node.name) if isinstance(node, Node) else self.node(node)
        neighbors: list[tuple[Node, Edge]] = []
        for edge in n.edges:
            if not edge.directed or edge.s.name == n.name:
                neighbor = edge.other(n.name)
                neighbors.append((neighbor, edge))
        return neighbors
