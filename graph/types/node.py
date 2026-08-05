"""a very basic implementation of nodes and edges to be used in demonstration graph algorithms"""
__author__ = "alunkeit"

class Node:
    """
    Class representing a node in the graph
    """

    def __init__(self, name: str):
        self._name = name
        self._edges = []

    def __repr__(self):
        return f"{self.name}"

    def __str__(self):
        return self.name

    def add_edge(self, edge):
        if edge not in self._edges:
            self._edges.append(edge)

    def remove_edge(self, edge):
        if edge in self._edges:
            self._edges.remove(edge)

    def edge_count(self):
        return len(self._edges)

    @property
    def name(self):
        return self._name

    @property
    def edges(self):
        return self._edges


class Edge:
    """
    Class representing an edge in the graph
    """

    def __init__(self, name: str, s: Node, t: Node, directed: bool = False):
        self.name = name
        self._s = s
        self._t = t
        self.directed = directed
        s.add_edge(self)
        t.add_edge(self)

    def __repr__(self):
        return f"{self.name}: {self.s.name} -> {self.t.name}"

    def __str__(self):
        return f"{self.s.name} -> {self.t.name}"

    @property
    def t(self):
        return self._t

    @property
    def s(self):
        return self._s

    def other(self, name: str) -> Node:
        if self.s.name == name:
            return self.t
        elif self.t.name == name:
            return self.s
        raise ValueError(
            f"Knoten '{name}' ist kein Endpunkt der Kante '{self.name}' "
            f"({self.s.name} -> {self.t.name})."
        )

    def is_directed(self) -> bool:
        return self.directed

