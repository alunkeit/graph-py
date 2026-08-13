import pytest
from graph.demo.main import run_main_demo
from graph.demo.bfs_main import run_bfs_demo
from graph.demo.dfs_main import run_dfs_demo
from graph.demo.dijkstra_main import run_dijkstra_demo
from graph.demo.bellman_ford_main import run_bellman_ford_demo

try:
    import consolemenu
    from menu import create_menu
    HAS_CONSOLE_MENU = True
except ImportError:
    create_menu = None  # type: ignore
    HAS_CONSOLE_MENU = False


def test_run_main_demo(capsys):
    run_main_demo()
    captured = capsys.readouterr()
    assert "Graph Demonstration (main.py)" in captured.out
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
    assert "Bellman-Ford Demonstration (bellman_ford_main.py)" in captured.out
    assert "Successfully loaded" in captured.out
    assert "Bellman-Ford shortest path from n0 to n29" in captured.out


def test_run_bellman_ford_demo_file_not_found(capsys):
    run_bellman_ford_demo(filepath="non_existent.graphml")
    captured = capsys.readouterr()
    assert "Error: File 'non_existent.graphml' not found." in captured.out


@pytest.mark.skipif(not HAS_CONSOLE_MENU, reason="console-menu package not installed")
def test_create_menu():
    menu = create_menu()
    assert menu is not None
    assert menu.title == "Graph-Py Console Menu"
    assert len(menu.items) == 5
    assert menu.items[0].text == "Basic Graph Demonstration (main.py)"
    assert menu.items[1].text == "Load GraphML & BFS Search (bfs_main.py)"
    assert menu.items[2].text == "Load GraphML & DFS Search (dfs_main.py)"
    assert menu.items[3].text == "Dijkstra Shortest Path Demonstration (dijkstra_main.py)"
    assert menu.items[4].text == "Bellman-Ford Shortest Path Demonstration (bellman_ford_main.py)"
