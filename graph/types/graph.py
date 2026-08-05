"""a very basic implementation of graphs for demonstration purposes"""
__author__ = "alunkeit"

from graph.types.node import Node, Edge


class UndirectedGraph:
    """
    Representing an undirected graph
    """

    def __init__(self, edges: list, nodes: dict):
        self._edges = edges
        self._nodes = nodes

    def __repr__(self):
        return f"{len(self._edges)} _edges"

    def __str__(self):
        return f"{len(self._edges)} _edges"

    @property
    def nodes(self):
        return self._nodes

    @property
    def edges(self):
        return self._edges

    def insert_from_nodes(self, name: str, s: Node, t: Node):
        """
        Insert an edge given its two endpoint _nodes.

        Reuses an existing node with the same _name instead of overwriting
        it, otherwise the edge lists of what should be the same logical
        node would diverge (two different Node objects sharing one _name).
        """
        s = self._nodes.setdefault(s.name, s)
        t = self._nodes.setdefault(t.name, t)
        self._edges.append(Edge(name, s, t))

    def insert_edge(self, e: Edge):
        self._edges.append(e)
        self._nodes[e.s.name] = e.s
        self._nodes[e.t.name] = e.t

    def node(self, name: str) -> Node:
        try:
            return self._nodes[name]
        except KeyError:
            raise KeyError(f"Kein Knoten mit dem Namen '{name}' im Graphen vorhanden.") from None

    def remove_edge(self, edge: Edge):
        """
        Remove an edge completely from the graph: from both endpoint
        _nodes (Node._edges) and from the graph's own edge list.
        """
        edge.s.remove_edge(edge)
        edge.t.remove_edge(edge)
        if edge in self._edges:
            self._edges.remove(edge)
