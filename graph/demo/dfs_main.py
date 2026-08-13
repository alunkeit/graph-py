from pathlib import Path
from graph.util.read_graph import load_graphml
from graph.search.dfs import DepthFirstSearch

__author__ = "alunkeit"


def run_dfs_demo(
    filepath: str | Path = "in/random_graph.graphml",
    start_node: str = "n0",
    target_node: str = "n49",
) -> None:
    """Loads a GraphML file and performs a Depth-First Search (DFS)."""
    print("\n--- DFS Demonstration (dfs_main.py) ---")
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

    print(f"\nSearching DFS path from '{start_node}' to '{target_node}':")
    alg = DepthFirstSearch(g)
    dfs_path = alg.search(start_node, target_node)

    if dfs_path:
        print(f"DFS path from {start_node} to {target_node} ({len(dfs_path)-1} edges):")
        print(" -> ".join([node.name for node in dfs_path]))
    else:
        print(f"No path found between '{start_node}' and '{target_node}'.")


if __name__ == "__main__":
    run_dfs_demo()
