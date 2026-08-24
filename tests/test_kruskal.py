"""Unit tests for Kruskal's Minimum Spanning Tree algorithm."""
from __future__ import annotations
import pytest
from graph.types.node import Node
from graph.types.edge import Edge
from graph.types.graph import UndirectedGraph
from graph.search.kruskal import Kruskal, DisjointSet
from graph.demo.kruskal_demo import run_kruskal_demo


def test_disjoint_set():
    ds = DisjointSet(["A", "B", "C", "D"])
    assert ds.find("A") == "A"
    assert ds.union("A", "B") is True
    assert ds.find("A") == ds.find("B")
    assert ds.union("A", "B") is False  # Already in same set
    assert ds.union("C", "D") is True
    assert ds.union("B", "C") is True
    assert ds.find("A") == ds.find("D")


def test_kruskal_mst():
    na, nb, nc, nd = Node("A"), Node("B"), Node("C"), Node("D")
    nodes_dict = {"A": na, "B": nb, "C": nc, "D": nd}
    # Square with diagonal:
    # A - (1) - B
    # |    \    |
    # (4)  (2) (3)
    # |         |
    # C - (5) - D
    edges = [
        Edge("e1", na, nb, weight=1.0),
        Edge("e2", na, nc, weight=4.0),
        Edge("e3", na, nd, weight=2.0),
        Edge("e4", nb, nd, weight=3.0),
        Edge("e5", nc, nd, weight=5.0),
    ]
    graph = UndirectedGraph(edges, nodes_dict)
    kruskal = Kruskal(graph)
    mst_edges, total_weight = kruskal.compute_mst()

    assert len(mst_edges) == 3  # |V| - 1 = 3
    assert total_weight == 7.0  # 1.0 (A-B) + 2.0 (A-D) + 4.0 (A-C) = 7.0


def test_run_kruskal_demo(capsys):
    run_kruskal_demo()
    captured = capsys.readouterr()
    assert "REAL-WORLD DEMO: Fiber Optic Cable Grid Infrastructure" in captured.out
    assert "Minimum Spanning Tree Solution" in captured.out
    assert "Total Minimum Grid Cabling Cost" in captured.out
