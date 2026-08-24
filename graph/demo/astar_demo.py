"""Real-World Demonstration: 2D Spatial Map Pathfinding using A* (A-Star) Search."""
from __future__ import annotations
import math
import sys
from pathlib import Path

# Bootstrap sys.path so direct script execution in VS Code / IDE works seamlessly
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from graph.types.node import Node
from graph.types.edge import Edge
from graph.types.graph import UndirectedGraph
from graph.search.dijkstra import Dijkstra
from graph.search.astar import AStar

__author__ = "alunkeit"

# 2D Grid Waypoint Coordinates (x, y) in kilometers
WAYPOINT_COORDINATES: dict[str, tuple[float, float]] = {
    "Start_Base": (0.0, 0.0),
    "Waypoint_A": (2.0, 1.0),
    "Waypoint_B": (1.0, 4.0),
    "Waypoint_C": (4.0, 2.0),
    "Waypoint_D": (3.0, 6.0),
    "Waypoint_E": (6.0, 4.0),
    "Waypoint_F": (5.0, 8.0),
    "Goal_Tower": (8.0, 8.0),
}


def euclidean_heuristic(u: Node, v: Node) -> float:
    """Euclidean distance heuristic between 2D coordinates of u and v."""
    x1, y1 = WAYPOINT_COORDINATES[u.name]
    x2, y2 = WAYPOINT_COORDINATES[v.name]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def run_astar_demo() -> None:
    """
    Demonstrates A* Search vs Dijkstra Search on a 2D spatial grid map.
    """
    print("\n==========================================================================")
    print("REAL-WORLD DEMO: 2D Spatial Pathfinding (A* Search vs Dijkstra)")
    print("==========================================================================")

    # Road network connecting waypoints
    road_connections = [
        ("Start_Base", "Waypoint_A", 2.2),
        ("Start_Base", "Waypoint_B", 4.1),
        ("Waypoint_A", "Waypoint_C", 2.2),
        ("Waypoint_B", "Waypoint_D", 2.8),
        ("Waypoint_C", "Waypoint_D", 4.1),
        ("Waypoint_C", "Waypoint_E", 2.8),
        ("Waypoint_D", "Waypoint_F", 2.8),
        ("Waypoint_E", "Waypoint_F", 4.1),
        ("Waypoint_E", "Goal_Tower", 4.5),
        ("Waypoint_F", "Goal_Tower", 3.0),
    ]

    nodes_dict = {name: Node(name) for name in WAYPOINT_COORDINATES}
    edges = [
        Edge(f"road_{idx}", nodes_dict[u], nodes_dict[v], weight=dist, directed=False)
        for idx, (u, v, dist) in enumerate(road_connections)
    ]

    graph = UndirectedGraph(edges, nodes_dict)
    start_node = "Start_Base"
    goal_node = "Goal_Tower"

    print(f"Map Grid: {len(nodes_dict)} spatial waypoints and {len(edges)} connecting roads.")
    print(f"Pathfinding Query: Find optimal route from [{start_node}] to [{goal_node}].")
    print("-" * 65)

    # 1. Dijkstra (un-guided search)
    dijkstra = Dijkstra(graph)
    dijkstra_path, dijkstra_dist = dijkstra.search_with_distance(start_node, goal_node)

    # 2. A* Search (heuristic-guided)
    astar = AStar(graph, heuristic=euclidean_heuristic)
    astar_path, astar_dist = astar.search_with_distance(start_node, goal_node)

    print("\n1. Dijkstra Search (Un-guided Breadth-First Priority Search)")
    if dijkstra_path:
        print(f"   - Route: {' -> '.join([n.name for n in dijkstra_path])}")
        print(f"   - Total Distance: {dijkstra_dist:.2f} km")

    print("\n2. A* Search (Euclidean Distance Heuristic Guided)")
    if astar_path:
        print(f"   - Route: {' -> '.join([n.name for n in astar_path])}")
        print(f"   - Total Distance: {astar_dist:.2f} km")

    print("-" * 65)
    print("\nReal-World Takeaway:")
    print("   A* Search combines exact path cost g(n) with estimated distance to goal h(n).")
    print("   In robotics, video games, and autonomous driving, A* focuses the search beam")
    print("   towards the target destination, exploring significantly fewer nodes than Dijkstra.")
    print("==========================================================================\n")


if __name__ == "__main__":
    run_astar_demo()
