"""Real-World Demonstration: Package Dependency Resolution using Topological Sort."""
from __future__ import annotations
import sys
from pathlib import Path

# Bootstrap sys.path so direct script execution in VS Code / IDE works seamlessly
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from graph.types.node import Node
from graph.types.edge import Edge
from graph.types.graph import DirectedGraph
from graph.search.topological_sort import TopologicalSort

__author__ = "alunkeit"


def run_topological_sort_demo() -> None:
    """
    Demonstrates Package Dependency Resolution (pip/npm build ordering) using Topological Sort.
    """
    print("\n==========================================================================")
    print("REAL-WORLD DEMO: Software Package Build & Dependency Resolution")
    print("==========================================================================")

    # Define software packages and dependencies (A -> B means "A depends on B / B must be built before A")
    dependencies = [
        ("web_app", "react"),
        ("web_app", "redux"),
        ("react", "jsx_parser"),
        ("react", "core_utils"),
        ("redux", "core_utils"),
        ("jsx_parser", "babel"),
        ("babel", "core_utils"),
        ("database_driver", "c_bindings"),
        ("web_app", "database_driver"),
    ]

    nodes_dict: dict[str, Node] = {}
    all_packages = set()
    for pkg_a, pkg_b in dependencies:
        all_packages.add(pkg_a)
        all_packages.add(pkg_b)

    for pkg in sorted(all_packages):
        nodes_dict[pkg] = Node(pkg)

    edges: list[Edge] = []
    # Directed edge: prerequisite -> dependent (e.g., core_utils -> babel -> jsx_parser -> react -> web_app)
    for idx, (dependent, prereq) in enumerate(dependencies):
        e = Edge(f"dep_{idx}", nodes_dict[prereq], nodes_dict[dependent], directed=True)
        edges.append(e)

    dag = DirectedGraph(edges, nodes_dict)

    print(f"Package Ecosystem: {len(nodes_dict)} packages and {len(edges)} dependency links.")
    print("\nDependency Rules (Prerequisite -> Dependent):")
    print("-" * 60)
    for prereq, dependent in dependencies:
        print(f"  [{prereq}] must be installed before [{dependent}]")
    print("-" * 60)

    print("\nComputing optimal build and installation sequence using Topological Sort...")

    top_sort = TopologicalSort(dag)
    build_order = top_sort.sort()

    print("\nValid Build Sequence:")
    print(" -> ".join([pkg.name for pkg in build_order]))

    # Circular Dependency Error Demonstration
    print("\nSimulating Circular Dependency Error (A -> B -> C -> A)...")
    circular_edges = list(edges)
    # Add circular edge: web_app -> core_utils
    circular_edges.append(Edge("circ_1", nodes_dict["web_app"], nodes_dict["core_utils"], directed=True))
    cyclic_graph = DirectedGraph(circular_edges, nodes_dict)

    try:
        TopologicalSort(cyclic_graph).sort()
    except ValueError as err:
        print(f"BUILD ERROR CATCH: {err}")

    print("\nReal-World Takeaway:")
    print("   Package managers (pip, npm, cargo) and build systems (Make, Bazel) use")
    print("   Topological Sorting to guarantee correct library installation order and detect circular deadlocks.")
    print("==========================================================================\n")


if __name__ == "__main__":
    run_topological_sort_demo()
