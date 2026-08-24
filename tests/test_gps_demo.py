"""Unit tests for the German Cities GPS Route Navigation demonstration."""
from __future__ import annotations
import pytest
from graph.demo.gps_route_demo import run_gps_demo, format_time, calculate_path_weight
from graph.util.read_graph import load_graphml


def test_format_time():
    assert format_time(45.0) == "45 mins"
    assert format_time(125.0) == "2h 5m (125 mins)"
    assert format_time(60.0) == "1h 0m (60 mins)"


def test_run_gps_demo(capsys):
    run_gps_demo(start_city="Flensburg", target_city="Muenchen")
    captured = capsys.readouterr()
    assert "REAL-WORLD DEMO: German Cities GPS Route Navigation" in captured.out
    assert "Breadth-First Search" in captured.out
    assert "Dijkstra's Algorithm" in captured.out
    assert "Flensburg" in captured.out
    assert "Muenchen" in captured.out


def test_gps_demo_nonexistent_file(capsys):
    run_gps_demo(filepath="nonexistent.graphml")
    captured = capsys.readouterr()
    assert "Error: GraphML file 'nonexistent.graphml' not found." in captured.out


def test_gps_demo_invalid_city(capsys):
    run_gps_demo(start_city="NonExistentCity", target_city="Muenchen")
    captured = capsys.readouterr()
    assert "Error: 'NonExistentCity' or 'Muenchen' not present in graph." in captured.out


def test_calculate_path_weight():
    graph, nodes = load_graphml("in/germany_cities_graph.graphml")
    flensburg = nodes["Flensburg"]
    kiel = nodes["Kiel"]
    hamburg = nodes["Hamburg"]

    # Flensburg -> Kiel (55 min), Kiel -> Hamburg (60 min) = 115 min total
    path = [flensburg, kiel, hamburg]
    assert calculate_path_weight(graph, path) == 115.0
