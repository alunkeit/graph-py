import pytest
from graph.types.node import Node
from graph.types.edge import Edge
from graph.types.graph import Graph, UndirectedGraph, DirectedGraph
from graph.search.base import SearchAlgorithm
from graph.search.bfs import BreadthFirstSearch
from graph.search.dfs import DepthFirstSearch


def test_graph_hierarchy_is_abstract():
    with pytest.raises(TypeError):
        Graph()  # type: ignore[abstract]


def test_directed_graph_properties():
    dg = DirectedGraph()
    assert dg.is_directed is True
    assert repr(dg) == "<DirectedGraph(0 _edges, 0 _nodes)>"
    assert str(dg) == "DirectedGraph(0 _edges, 0 _nodes)"

    ug = UndirectedGraph()
    assert ug.is_directed is False
    assert repr(ug) == "<UndirectedGraph(0 _edges, 0 _nodes)>"
    assert str(ug) == "UndirectedGraph(0 _edges, 0 _nodes)"


def test_directed_graph_edge_insertion_and_neighbors():
    dg = DirectedGraph()
    n1 = Node("n1")
    n2 = Node("n2")
    dg.insert_from_nodes("e1", n1, n2, weight=3.5)

    assert len(dg.edges) == 1
    assert dg.edges[0].directed is True
    assert dg.edges[0].weight == 3.5

    # Outgoing neighbors from n1 should include n2
    n1_neighbors = dg.get_neighbors(n1)
    assert len(n1_neighbors) == 1
    assert n1_neighbors[0][0] == n2
    assert n1_neighbors[0][1].name == "e1"

    # Outgoing neighbors from n2 should be empty
    n2_neighbors = dg.get_neighbors(n2)
    assert len(n2_neighbors) == 0


def test_search_algorithm_base_class():
    ug = UndirectedGraph()
    bfs = BreadthFirstSearch(ug)
    dfs = DepthFirstSearch(ug)

    assert isinstance(bfs, SearchAlgorithm)
    assert isinstance(dfs, SearchAlgorithm)
    assert bfs.graph is ug
    assert dfs.graph is ug

    bfs_none = BreadthFirstSearch(None)
    with pytest.raises(ValueError) as exc_info:
        bfs_none.search("n0", "n1")
    assert "Graph instance cannot be None." in str(exc_info.value)
