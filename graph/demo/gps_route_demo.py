"""Real-World Demonstration: German Cities GPS Route Navigation using Graph Search Algorithms."""
from __future__ import annotations
import sys
from pathlib import Path

# Bootstrap sys.path so direct script execution in VS Code / IDE works seamlessly
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from graph.util.read_graph import load_graphml
from graph.search.bfs import BreadthFirstSearch
from graph.search.dijkstra import Dijkstra

__author__ = "alunkeit"


def format_time(minutes: float) -> str:
    """Helper to format minutes into hours and minutes."""
    hrs = int(minutes // 60)
    mins = int(minutes % 60)
    if hrs > 0:
        return f"{hrs}h {mins}m ({minutes:.0f} mins)"
    return f"{mins} mins"


def calculate_path_weight(graph, path) -> float:
    """Calculates the total edge weight for a given node path in the graph."""
    if not path or len(path) < 2:
        return 0.0
    total_weight = 0.0
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        for edge in u.edges:
            if edge.directed:
                if edge.s == u and edge.t == v:
                    total_weight += edge.weight
                    break
            else:
                if (edge.s == u and edge.t == v) or (edge.s == v and edge.t == u):
                    total_weight += edge.weight
                    break
    return total_weight


def run_gps_demo(
    filepath: str | Path = "in/germany_cities_graph.graphml",
    start_city: str = "Flensburg",
    target_city: str = "Muenchen",
) -> None:
    """
    Demonstrates real-world GPS navigation route selection across German cities (>50k citizens).
    Compares Breadth-First Search (fewest city hops) vs Dijkstra's Shortest Path (fastest Autobahn duration).
    """
    print("\n==========================================================================")
    print("REAL-WORLD DEMO: German Cities GPS Route Navigation (Autobahn Network)")
    print("==========================================================================")
    
    path = Path(filepath)
    if not path.exists():
        print(f"Error: GraphML file '{filepath}' not found.")
        return

    g, nodes = load_graphml(path)
    print(f"Loaded German Road Network: {len(nodes)} major cities (>50k pop) and {len(g.edges)} Autobahn links.")

    if start_city not in nodes or target_city not in nodes:
        print(f"Error: '{start_city}' or '{target_city}' not present in graph.")
        return

    print(f"\nNavigation Request: Route from '{start_city}' to '{target_city}'")
    print("-" * 74)

    # 1. Breadth-First Search (Unweighted - Fewest City Hops)
    bfs_alg = BreadthFirstSearch(g)
    bfs_path = bfs_alg.search(start_city, target_city)
    bfs_duration = calculate_path_weight(g, bfs_path)

    # 2. Dijkstra Search (Weighted - Fastest Autobahn Driving Time)
    dijkstra_alg = Dijkstra(g)
    dijkstra_path, dijkstra_duration = dijkstra_alg.search_with_distance(start_city, target_city)

    # Display Results Comparison
    print("\n1. Breadth-First Search (BFS - Unweighted Route)")
    print("   Goal: Minimize the number of intermediate cities / turns (fewest hops).")
    if bfs_path:
        bfs_cities = [node.name for node in bfs_path]
        print(f"   - Route ({len(bfs_path)-1} hops): {' -> '.join(bfs_cities)}")
        print(f"   - Total Estimated Driving Duration: {format_time(bfs_duration)}")
    else:
        print("   - No route found.")

    print("\n2. Dijkstra's Algorithm (Weighted GPS Route)")
    print("   Goal: Minimize total driving duration in minutes taking speed limits & Autobahn speeds into account.")
    if dijkstra_path:
        dijkstra_cities = [node.name for node in dijkstra_path]
        print(f"   - Route ({len(dijkstra_path)-1} hops): {' -> '.join(dijkstra_cities)}")
        print(f"   - Total Estimated Driving Duration: {format_time(dijkstra_duration)}")
    else:
        print("   - No route found.")

    print("\nReal-World Takeaway:")
    if dijkstra_duration < bfs_duration:
        saved_time = bfs_duration - dijkstra_duration
        print(f"   Dijkstra's algorithm found a route that is {format_time(saved_time)} FASTER than BFS!")
        print("   Even though BFS took fewer city hops, Dijkstra routed via high-speed Autobahnen,")
        print("   demonstrating why modern GPS systems (Google Maps, Waze) rely on weighted graph search.")
    elif dijkstra_duration == bfs_duration:
        print("   Both algorithms reached the destination with equal travel duration.")
    print("==========================================================================\n")


if __name__ == "__main__":
    run_gps_demo()
