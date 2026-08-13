import pytest
from graph.types.node import Node
from graph.types.edge import Edge
from graph.types.graph import UndirectedGraph, DirectedGraph
from graph.search.base import SearchAlgorithm
from graph.search.dijkstra import Dijkstra, DijkstraSearch


def test_dijkstra_inheritance():
    g = UndirectedGraph()
    alg = Dijkstra(g)
    assert isinstance(alg, SearchAlgorithm)
    assert alg.graph is g


def test_dijkstra_undirected_weighted_shortest_path():
    # Graph layout:
    # A --(10)-- B --(1)-- C
    # A --(2)-- D --(2)-- E --(2)-- C
    # Direct path A->B->C cost: 11
    # Indirect path A->D->E->C cost: 6
    g = UndirectedGraph()
    na, nb, nc, nd, ne = Node("A"), Node("B"), Node("C"), Node("D"), Node("E")

    g.insert_edge(Edge("e_ab", na, nb, weight=10.0))
    g.insert_edge(Edge("e_bc", nb, nc, weight=1.0))
    g.insert_edge(Edge("e_ad", na, nd, weight=2.0))
    g.insert_edge(Edge("e_de", nd, ne, weight=2.0))
    g.insert_edge(Edge("e_ec", ne, nc, weight=2.0))

    dijkstra = Dijkstra(g)

    # Test search returning path list
    path = dijkstra.search("A", "C")
    assert path == [na, nd, ne, nc]

    # Test search_with_distance
    path, distance = dijkstra.search_with_distance(na, nc)
    assert path == [na, nd, ne, nc]
    assert distance == 6.0


def test_dijkstra_directed_graph_directionality():
    # A -> B (weight 1), B -> C (weight 1), C -> A (weight 1)
    g = DirectedGraph()
    na, nb, nc = Node("A"), Node("B"), Node("C")
    g.insert_from_nodes("e_ab", na, nb, weight=1.0)
    g.insert_from_nodes("e_bc", nb, nc, weight=1.0)
    g.insert_from_nodes("e_ca", nc, na, weight=1.0)

    dijkstra = DijkstraSearch(g)

    path_ac, dist_ac = dijkstra.search_with_distance("A", "C")
    assert path_ac == [na, nb, nc]
    assert dist_ac == 2.0

    # Path from C to B: C -> A -> B (cost 2.0)
    path_cb, dist_cb = dijkstra.search_with_distance("C", "B")
    assert path_cb == [nc, na, nb]
    assert dist_cb == 2.0


def test_dijkstra_same_start_and_target():
    g = UndirectedGraph()
    na = Node("A")
    g.insert_edge(Edge("e_aa", na, na, weight=0.0))

    dijkstra = Dijkstra(g)
    path, dist = dijkstra.search_with_distance("A", "A")
    assert path == [na]
    assert dist == 0.0


def test_dijkstra_unreachable_node():
    g = UndirectedGraph()
    na = Node("A")
    nb = Node("B")
    g.insert_from_nodes("e_ab", na, nb, weight=1.0)

    nc = Node("C")
    g.insert_edge(Edge("e_dummy", nc, nc, weight=1.0))

    dijkstra = Dijkstra(g)
    path = dijkstra.search("A", "C")
    assert path is None

    path_dist = dijkstra.search_with_distance("A", "C")
    assert path_dist == (None, float("inf"))


def test_dijkstra_non_existent_node():
    g = UndirectedGraph()
    na = Node("A")
    g.insert_from_nodes("e_ab", na, Node("B"))

    dijkstra = Dijkstra(g)
    with pytest.raises(KeyError):
        dijkstra.search("A", "NonExistent")


def test_dijkstra_negative_weight_exception():
    g = UndirectedGraph()
    na, nb = Node("A"), Node("B")
    g.insert_edge(Edge("e_ab", na, nb, weight=-5.0))

    dijkstra = Dijkstra(g)
    with pytest.raises(ValueError) as exc_info:
        dijkstra.search("A", "B")
    assert "negative edge weights" in str(exc_info.value)
