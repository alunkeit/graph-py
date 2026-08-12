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

    menu.append_item(item_main)
    menu.append_item(item_bfs)

    return menu


def main() -> None:
    menu = create_menu()
    if menu is not None:
        menu.show()


if __name__ == "__main__":
    main()


