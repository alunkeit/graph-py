"""Demonstration of Dijkstra's Shortest Path Algorithm."""
from __future__ import annotations
from pathlib import Path
from graph.util.read_graph import load_graphml
from graph.search.dijkstra import Dijkstra

__author__ = "alunkeit"


def run_dijkstra_demo(
    filepath: str | Path = "in/weighted_graph.graphml",
    start_node: str = "n0",
    target_node: str = "n34",
) -> None:
    """Loads a GraphML file and performs Dijkstra's Shortest Path Search."""
    print("\n--- Dijkstra Demonstration (dijkstra_main.py) ---")
    path = Path(filepath)
    if not path.exists():
        print(f"Error: File '{filepath}' not found.")
        return

    g, nodes = load_graphml(path)
    print(f"Successfully loaded: {len(nodes)} nodes and {len(g.edges)} edges.")

    print("\nSample nodes (first 5):")
    for n in list(nodes.values())[:5]:
        print(f"  Node {n.name} (Degree: {len(n.edges)})")

    print("\nSample edges (first 5):")
    for e in g.edges[:5]:
        print(f"  Edge {e}")

    print(f"\nSearching Dijkstra shortest path from '{start_node}' to '{target_node}':")
    alg = Dijkstra(g)
    dijkstra_path, distance = alg.search_with_distance(start_node, target_node)

    if dijkstra_path:
        print(f"Dijkstra shortest path from {start_node} to {target_node} ({len(dijkstra_path)-1} edges, total distance: {distance:.2f}):")
        print(" -> ".join([node.name for node in dijkstra_path]))
    else:
        print(f"No path found between '{start_node}' and '{target_node}'.")


if __name__ == "__main__":
    run_dijkstra_demo()
