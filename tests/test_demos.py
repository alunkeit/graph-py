import pytest
from graph.demo.create_nodes import run_main_demo
from graph.demo.bfs_main import run_bfs_demo
from graph.demo.dfs_main import run_dfs_demo
from graph.demo.dijkstra_main import run_dijkstra_demo
from graph.demo.bellman_ford_demo import run_bellman_ford_demo
from menu import get_menu_options, display_menu, run_menu_loop


def test_run_main_demo(capsys):
    run_main_demo()
    captured = capsys.readouterr()
    assert "Graph Demonstration (create_nodes.py)" in captured.out
    assert "New node: x0" in captured.out
    assert "New edge: x0 -> x1" in captured.out


def test_run_bfs_demo(capsys):
    run_bfs_demo()
    captured = capsys.readouterr()
    assert "BFS Demonstration (bfs_main.py)" in captured.out
    assert "Successfully loaded" in captured.out
    assert "BFS path from n0 to n49" in captured.out


def test_run_bfs_demo_file_not_found(capsys):
    run_bfs_demo(filepath="non_existent.graphml")
    captured = capsys.readouterr()
    assert "Error: File 'non_existent.graphml' not found." in captured.out


def test_run_dfs_demo(capsys):
    run_dfs_demo()
    captured = capsys.readouterr()
    assert "DFS Demonstration (dfs_main.py)" in captured.out
    assert "Successfully loaded" in captured.out
    assert "DFS path from n0 to n49" in captured.out


def test_run_dfs_demo_file_not_found(capsys):
    run_dfs_demo(filepath="non_existent.graphml")
    captured = capsys.readouterr()
    assert "Error: File 'non_existent.graphml' not found." in captured.out


def test_run_dijkstra_demo(capsys):
    run_dijkstra_demo()
    captured = capsys.readouterr()
    assert "Dijkstra Demonstration (dijkstra_main.py)" in captured.out
    assert "Successfully loaded" in captured.out
    assert "Dijkstra shortest path from n0 to n34" in captured.out


def test_run_dijkstra_demo_file_not_found(capsys):
    run_dijkstra_demo(filepath="non_existent.graphml")
    captured = capsys.readouterr()
    assert "Error: File 'non_existent.graphml' not found." in captured.out


def test_run_bellman_ford_demo(capsys):
    run_bellman_ford_demo()
    captured = capsys.readouterr()
    assert "Bellman-Ford Demonstration (bellman_ford_demo.py)" in captured.out
    assert "Successfully loaded" in captured.out
    assert "Bellman-Ford shortest path from n0 to n29" in captured.out


def test_run_bellman_ford_demo_file_not_found(capsys):
    run_bellman_ford_demo(filepath="non_existent.graphml")
    captured = capsys.readouterr()
    assert "Error: File 'non_existent.graphml' not found." in captured.out


def test_menu_options():
    options = get_menu_options()
    assert len(options) == 10
    assert options[0][0] == "Basic Graph Demonstration (create_nodes.py)"
    assert options[1][0] == "Load GraphML & BFS Search (bfs_main.py)"
    assert options[2][0] == "Load GraphML & DFS Search (dfs_main.py)"
    assert options[3][0] == "Dijkstra Shortest Path Demonstration (dijkstra_main.py)"
    assert options[4][0] == "Bellman-Ford Shortest Path Demonstration (bellman_ford_demo.py)"


def test_display_menu(capsys):
    display_menu()
    captured = capsys.readouterr()
    assert "Graph-Py Console Menu" in captured.out
    assert "0. Exit" in captured.out


def test_run_menu_loop_exit(capsys):
    # Test exiting via option 0
    inputs = ["0"]
    run_menu_loop(input_func=lambda _: inputs.pop(0), loop_once=True)
    captured = capsys.readouterr()
    assert "Exiting Graph-Py menu." in captured.out
