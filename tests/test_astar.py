"""Unit tests for A* Search algorithm."""
from __future__ import annotations
import math
import pytest
from graph.types.node import Node
from graph.types.edge import Edge
from graph.types.graph import UndirectedGraph
from graph.search.astar import AStar
from graph.demo.astar_demo import run_astar_demo


def test_astar_simple_path():
    n1, n2, n3 = Node("1"), Node("2"), Node("3")
    nodes_dict = {"1": n1, "2": n2, "3": n3}
    edges = [
        Edge("e1", n1, n2, weight=2.0),
        Edge("e2", n2, n3, weight=3.0),
        Edge("e3", n1, n3, weight=10.0),
    ]
    graph = UndirectedGraph(edges, nodes_dict)

    # Heuristic returning 0.0
    astar = AStar(graph)
    path, dist = astar.search_with_distance("1", "3")
    assert path is not None
    assert [n.name for n in path] == ["1", "2", "3"]
    assert dist == 5.0


def test_astar_with_heuristic():
    coords = {"A": (0.0, 0.0), "B": (1.0, 0.0), "C": (2.0, 0.0)}
    na, nb, nc = Node("A"), Node("B"), Node("C")
    nodes_dict = {"A": na, "B": nb, "C": nc}
    edges = [
        Edge("e1", na, nb, weight=1.0),
        Edge("e2", nb, nc, weight=1.0),
    ]
    graph = UndirectedGraph(edges, nodes_dict)

    def heuristic(u: Node, v: Node) -> float:
        x1, y1 = coords[u.name]
        x2, y2 = coords[v.name]
        return math.hypot(x2 - x1, y2 - y1)

    astar = AStar(graph, heuristic=heuristic)
    path = astar.search("A", "C")
    assert path is not None
    assert [n.name for n in path] == ["A", "B", "C"]


def test_run_astar_demo(capsys):
    run_astar_demo()
    captured = capsys.readouterr()
    assert "REAL-WORLD DEMO: 2D Spatial Pathfinding" in captured.out
    assert "Dijkstra Search" in captured.out
    assert "A* Search" in captured.out
