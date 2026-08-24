"""Demonstration of Bellman-Ford Shortest Path Algorithm."""
from __future__ import annotations
from pathlib import Path
from graph.util.read_graph import load_graphml
from graph.search.bellman_ford import BellmanFord

__author__ = "alunkeit"


def run_bellman_ford_demo(
    filepath: str | Path = "in/bellman_ford_graph.graphml",
    start_node: str = "n0",
    target_node: str = "n29",
) -> None:
    """Loads a GraphML file with positive/negative edge weights and performs Bellman-Ford Search."""
    print("\n--- Bellman-Ford Demonstration (bellman_ford_demo.py) ---")
    path = Path(filepath)
    if not path.exists():
        print(f"Error: File '{filepath}' not found.")
        return

    g, nodes = load_graphml(path)
    print(f"Successfully loaded: {len(nodes)} nodes and {len(g.edges)} edges.")

    negative_edges = [e for e in g.edges if e.weight < 0]
    print(f"Graph contains {len(negative_edges)} edges with negative weights.")

    print("\nSample edges with negative weights (first 5):")
    for e in negative_edges[:5]:
        print(f"  Edge {e}")

    print(f"\nSearching Bellman-Ford shortest path from '{start_node}' to '{target_node}':")
    alg = BellmanFord(g)
    try:
        bf_path, distance = alg.search_with_distance(start_node, target_node)

        if bf_path:
            print(f"Bellman-Ford shortest path from {start_node} to {target_node} ({len(bf_path)-1} edges, total distance: {distance:.2f}):")
            print(" -> ".join([node.name for node in bf_path]))
        else:
            print(f"No path found between '{start_node}' and '{target_node}'.")
    except ValueError as e:
        print(f"Negative weight cycle detected: {e}")


if __name__ == "__main__":
    run_bellman_ford_demo()
