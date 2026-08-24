"""Interactive Console Menu for graph-py without third-party dependencies."""
from __future__ import annotations
import sys
from typing import Callable

from graph.demo.create_nodes import run_main_demo
from graph.demo.bfs_main import run_bfs_demo
from graph.demo.dfs_main import run_dfs_demo
from graph.demo.dijkstra_main import run_dijkstra_demo
from graph.demo.bellman_ford_demo import run_bellman_ford_demo
from graph.demo.gps_route_demo import run_gps_demo
from graph.demo.currency_arbitrage_demo import run_currency_arbitrage_demo
from graph.demo.topological_sort_demo import run_topological_sort_demo
from graph.demo.kruskal_demo import run_kruskal_demo
from graph.demo.astar_demo import run_astar_demo

__author__ = "alunkeit"


def get_menu_options() -> list[tuple[str, Callable[[], None]]]:
    """Returns the list of available menu option titles and their corresponding handler functions."""
    return [
        ("Basic Graph Demonstration (create_nodes.py)", run_main_demo),
        ("Load GraphML & BFS Search (bfs_main.py)", run_bfs_demo),
        ("Load GraphML & DFS Search (dfs_main.py)", run_dfs_demo),
        ("Dijkstra Shortest Path Demonstration (dijkstra_main.py)", run_dijkstra_demo),
        ("Bellman-Ford Shortest Path Demonstration (bellman_ford_demo.py)", run_bellman_ford_demo),
        ("Real-World GPS German Cities Demo (gps_route_demo.py)", run_gps_demo),
        ("Real-World Forex Currency Arbitrage Demo (currency_arbitrage_demo.py)", run_currency_arbitrage_demo),
        ("Package Dependency Resolution & Topological Sort (topological_sort_demo.py)", run_topological_sort_demo),
        ("Fiber Optic Network Cable Grid & Kruskal MST (kruskal_demo.py)", run_kruskal_demo),
        ("2D Spatial Pathfinding & A* Search (astar_demo.py)", run_astar_demo),
    ]


def display_menu() -> None:
    """Displays the formatted CLI menu options to stdout."""
    options = get_menu_options()
    print("\n==========================================================================")
    print("                      Graph-Py Console Menu")
    print("==========================================================================")
    for idx, (title, _func) in enumerate(options, 1):
        print(f" {idx:2d}. {title}")
    print("  0. Exit")
    print("==========================================================================")


def run_menu_loop(input_func: Callable[[str], str] = input, loop_once: bool = False) -> None:
    """
    Runs the main interactive menu loop.

    :param input_func: Function to read user input (defaults to builtin input, overridable for tests).
    :param loop_once: If True, exits after handling a single selection (useful for non-interactive environments).
    """
    options = get_menu_options()

    while True:
        display_menu()
        try:
            choice = input_func("\nSelect an option (0-10): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting Graph-Py menu.")
            break

        if choice in ("0", "exit", "quit", "q"):
            print("Exiting Graph-Py menu.")
            break

        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(options):
                _title, func = options[idx - 1]
                try:
                    func()
                except Exception as e:
                    print(f"\nError executing demonstration: {e}")
            else:
                print(f"Invalid selection: {choice}. Please enter a number between 0 and {len(options)}.")
        else:
            print(f"Invalid input: '{choice}'. Please enter a valid option number.")

        if loop_once:
            break


def main() -> None:
    """Main entry point for running the interactive menu."""
    run_menu_loop()


if __name__ == "__main__":
    main()
