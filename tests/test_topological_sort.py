"""Unit tests for Topological Sort algorithm."""
from __future__ import annotations
import pytest
from graph.types.node import Node
from graph.types.edge import Edge
from graph.types.graph import DirectedGraph
from graph.search.topological_sort import TopologicalSort
from graph.demo.topological_sort_demo import run_topological_sort_demo


def test_topological_sort_linear_dag():
    n1, n2, n3, n4 = Node("1"), Node("2"), Node("3"), Node("4")
    nodes_dict = {"1": n1, "2": n2, "3": n3, "4": n4}
    # 1 -> 2 -> 3 -> 4
    edges = [
        Edge("e1", n1, n2, directed=True),
        Edge("e2", n2, n3, directed=True),
        Edge("e3", n3, n4, directed=True),
    ]
    graph = DirectedGraph(edges, nodes_dict)
    ts = TopologicalSort(graph)
    order = ts.sort()
    names = [node.name for node in order]
    assert names == ["1", "2", "3", "4"]


def test_topological_sort_cycle_raises_error():
    n1, n2, n3 = Node("1"), Node("2"), Node("3")
    nodes_dict = {"1": n1, "2": n2, "3": n3}
    # Cycle: 1 -> 2 -> 3 -> 1
    edges = [
        Edge("e1", n1, n2, directed=True),
        Edge("e2", n2, n3, directed=True),
        Edge("e3", n3, n1, directed=True),
    ]
    graph = DirectedGraph(edges, nodes_dict)
    ts = TopologicalSort(graph)
    with pytest.raises(ValueError, match="contains a cycle"):
        ts.sort()


def test_topological_sort_search():
    n1, n2, n3 = Node("1"), Node("2"), Node("3")
    nodes_dict = {"1": n1, "2": n2, "3": n3}
    edges = [
        Edge("e1", n1, n2, directed=True),
        Edge("e2", n2, n3, directed=True),
    ]
    graph = DirectedGraph(edges, nodes_dict)
    ts = TopologicalSort(graph)
    path = ts.search("1", "3")
    assert path is not None
    assert [n.name for n in path] == ["1", "2", "3"]


def test_run_topological_sort_demo(capsys):
    run_topological_sort_demo()
    captured = capsys.readouterr()
    assert "REAL-WORLD DEMO: Software Package Build & Dependency Resolution" in captured.out
    assert "Valid Build Sequence:" in captured.out
    assert "BUILD ERROR CATCH" in captured.out
