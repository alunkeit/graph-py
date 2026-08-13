"""Console menu for graph-py using console-menu."""
from __future__ import annotations
try:
    from consolemenu import ConsoleMenu
    from consolemenu.items import FunctionItem
    CONSOLE_MENU_AVAILABLE = True
except ImportError:
    ConsoleMenu = None  # type: ignore
    FunctionItem = None  # type: ignore
    CONSOLE_MENU_AVAILABLE = False

from graph.demo.main import run_main_demo
from graph.demo.bfs_main import run_bfs_demo
from graph.demo.dfs_main import run_dfs_demo
from graph.demo.dijkstra_main import run_dijkstra_demo
from graph.demo.bellman_ford_main import run_bellman_ford_demo
__author__ = "alunkeit"


def create_menu() -> ConsoleMenu | None:
    """Creates and configures the main console menu."""
    if not CONSOLE_MENU_AVAILABLE:
        print("The 'console-menu' package is not installed. Please install it using 'pip install console-menu'.")
        return None

    menu = ConsoleMenu(
        title="Graph-Py Console Menu",
        subtitle="Select a demonstration or function:"
    )

    item_main = FunctionItem(
        text="Basic Graph Demonstration (main.py)",
        function=run_main_demo
    )

    item_bfs = FunctionItem(
        text="Load GraphML & BFS Search (bfs_main.py)",
        function=run_bfs_demo
    )

    item_dfs = FunctionItem(
        text="Load GraphML & DFS Search (dfs_main.py)",
        function=run_dfs_demo
    )

    item_dijkstra = FunctionItem(
        text="Dijkstra Shortest Path Demonstration (dijkstra_main.py)",
        function=run_dijkstra_demo
    )

    item_bellman_ford = FunctionItem(
        text="Bellman-Ford Shortest Path Demonstration (bellman_ford_main.py)",
        function=run_bellman_ford_demo
    )

    menu.append_item(item_main)
    menu.append_item(item_bfs)
    menu.append_item(item_dfs)
    menu.append_item(item_dijkstra)
    menu.append_item(item_bellman_ford)

    return menu


def main() -> None:
    menu = create_menu()
    if menu is not None:
        menu.show()


if __name__ == "__main__":
    main()


