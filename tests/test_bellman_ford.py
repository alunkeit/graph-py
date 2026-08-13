import pytest
from graph.types.node import Node
from graph.types.edge import Edge
from graph.types.graph import UndirectedGraph, DirectedGraph
from graph.search.base import SearchAlgorithm
from graph.search.bellman_ford import BellmanFord, BellmanFordSearch


def test_bellman_ford_inheritance():
    g = DirectedGraph()
    alg = BellmanFord(g)
    assert isinstance(alg, SearchAlgorithm)
    assert alg.graph is g


def test_bellman_ford_negative_edge_weights():
    # Directed graph with negative edge weights (no negative cycles)
    # A -> B (weight 4)
    # A -> C (weight 2)
    # C -> B (weight -3)  -> Path A -> C -> B cost is -1
    # B -> D (weight 2)
    g = DirectedGraph()
    na, nb, nc, nd = Node("A"), Node("B"), Node("C"), Node("D")

    g.insert_from_nodes("e_ab", na, nb, weight=4.0)
    g.insert_from_nodes("e_ac", na, nc, weight=2.0)
    g.insert_from_nodes("e_cb", nc, nb, weight=-3.0)
    g.insert_from_nodes("e_bd", nb, nd, weight=2.0)

    bf = BellmanFord(g)
    path, dist = bf.search_with_distance("A", "D")

    assert path == [na, nc, nb, nd]
    assert dist == 1.0  # 2 + (-3) + 2 = 1.0


def test_bellman_ford_negative_cycle_detection():
    # A -> B (1), B -> C (-4), C -> A (1) -> cycle sum = -2
    g = DirectedGraph()
    na, nb, nc = Node("A"), Node("B"), Node("C")
    g.insert_from_nodes("e_ab", na, nb, weight=1.0)
    g.insert_from_nodes("e_bc", nb, nc, weight=-4.0)
    g.insert_from_nodes("e_ca", nc, na, weight=1.0)

    bf = BellmanFordSearch(g)
    with pytest.raises(ValueError) as exc_info:
        bf.search("A", "C")
    assert "negative weight cycle" in str(exc_info.value)


def test_bellman_ford_same_start_and_target():
    g = DirectedGraph()
    na = Node("A")
    g.insert_from_nodes("e_aa", na, na, weight=1.0)

    bf = BellmanFord(g)
    path, dist = bf.search_with_distance("A", "A")
    assert path == [na]
    assert dist == 0.0


def test_bellman_ford_unreachable_target():
    g = DirectedGraph()
    na, nb, nc = Node("A"), Node("B"), Node("C")
    g.insert_from_nodes("e_ab", na, nb, weight=1.0)
    g.insert_from_nodes("e_cc", nc, nc, weight=1.0)

    bf = BellmanFord(g)
    path, dist = bf.search_with_distance("A", "C")
    assert path is None
    assert dist == float("inf")


def test_bellman_ford_none_graph():
    bf = BellmanFord(None)
    with pytest.raises(ValueError) as exc_info:
        bf.search("A", "B")
    assert "Graph instance cannot be None." in str(exc_info.value)
