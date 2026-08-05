"""a very basic implementation of graphs for demonstration purposes"""
from os import name
__author__ = "alunkeit"

from graph.types.node import Node, Edge


class UndirectedGraph:
    """
    Representing an undirected graph
    """

    def __init__(self, edges: list[Edge], nodes: dict[str, Node]):
        self._edges = edges
        self._nodes = nodes

    def __repr__(self):
        return f"<UndirectedGraph({len(self._edges)} _edges, {len(self._nodes)} _nodes)>"

    def __str__(self):
        return f"UndirectedGraph({len(self._edges)} _edges, {len(self._nodes)} _nodes)"

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
        """
        Insert an edge into the graph.

        :param e: The edge to insert
        """
        self._edges.append(e)
        # Knoten s im Graphen registrieren oder Kante beim bestehenden Knoten anmelden
        if e.s.name not in self._nodes:
            self._nodes[e.s.name] = e.s
        elif self._nodes[e.s.name] is not e.s:
            self._nodes[e.s.name].add_edge(e)

        # Knoten t im Graphen registrieren oder Kante beim bestehenden Knoten anmelden
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

    def __getitem__(self, name: str) -> Node:
        """Ermöglicht den Zugriff per graph["n0"] anstelle von graph.node("n0")."""
        return self.node(name)

    def __contains__(self, item: str | Node) -> bool:
        """Ermöglicht 'n0' in graph oder node in graph."""
        if isinstance(item, Node):
            return item.name in self._nodes
        return item in self._nodes

    def __len__(self) -> int:
        """Gibt die Anzahl der Knoten im Graphen zurück (len(graph))."""
        return len(self._nodes)

    def __iter__(self):
        """Ermöglicht 'for node in graph:'."""
        return iter(self._nodes.values())

