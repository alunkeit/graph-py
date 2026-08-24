"""Real-World Demonstration: Fiber Optic Network Design using Kruskal's Minimum Spanning Tree (MST)."""
from __future__ import annotations
import sys
from pathlib import Path

# Bootstrap sys.path so direct script execution in VS Code / IDE works seamlessly
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from graph.types.node import Node
from graph.types.edge import Edge
from graph.types.graph import UndirectedGraph
from graph.search.kruskal import Kruskal

__author__ = "alunkeit"


def run_kruskal_demo() -> None:
    """
    Demonstrates Minimum Infrastructure Cabling Network design using Kruskal's MST algorithm.
    """
    print("\n==========================================================================")
    print("REAL-WORLD DEMO: Fiber Optic Cable Grid Infrastructure (Kruskal MST)")
    print("==========================================================================")

    # Regional hubs and candidate cable routes (cost in thousands of Euros)
    candidate_cables = [
        ("Berlin", "Hamburg", 280.0),
        ("Berlin", "Leipzig", 190.0),
        ("Berlin", "Dresden", 190.0),
        ("Hamburg", "Bremen", 120.0),
        ("Hamburg", "Hannover", 150.0),
        ("Hannover", "Bremen", 125.0),
        ("Hannover", "Kassel", 165.0),
        ("Hannover", "Leipzig", 260.0),
        ("Leipzig", "Dresden", 120.0),
        ("Frankfurt", "Kassel", 190.0),
        ("Frankfurt", "Mannheim", 80.0),
        ("Frankfurt", "Wuerzburg", 120.0),
        ("Kassel", "Wuerzburg", 200.0),
        ("Mannheim", "Stuttgart", 110.0),
        ("Stuttgart", "Muenchen", 220.0),
        ("Wuerzburg", "Nuernberg", 110.0),
        ("Nuernberg", "Muenchen", 170.0),
    ]

    city_names = set()
    for c1, c2, _cost in candidate_cables:
        city_names.add(c1)
        city_names.add(c2)

    nodes_dict = {name: Node(name) for name in sorted(city_names)}
    edges = [
        Edge(f"cable_{idx}", nodes_dict[c1], nodes_dict[c2], weight=cost, directed=False)
        for idx, (c1, c2, cost) in enumerate(candidate_cables)
    ]

    graph = UndirectedGraph(edges, nodes_dict)
    total_candidate_cost = sum(e.weight for e in edges)

    print(f"Network Scope: {len(nodes_dict)} regional city hubs and {len(edges)} candidate cable routes.")
    print(f"Total Cost of Laying ALL Candidate Cables: EUR {total_candidate_cost:,.2f}k")
    print("-" * 65)

    print("\nComputing Minimum Spanning Tree using Kruskal's algorithm...")
    kruskal = Kruskal(graph)
    mst_edges, mst_cost = kruskal.compute_mst()

    print(f"\nMinimum Spanning Tree Solution ({len(mst_edges)} cable links):")
    for idx, e in enumerate(mst_edges, 1):
        print(f"  {idx:2d}. Connect [{e.s.name}] <---> [{e.t.name}]  |  Cost: EUR {e.weight:,.2f}k")

    savings = total_candidate_cost - mst_cost
    savings_pct = (savings / total_candidate_cost) * 100

    print("-" * 65)
    print(f"  Total Minimum Grid Cabling Cost: EUR {mst_cost:,.2f}k")
    print(f"  Cost Savings vs Full Network:   EUR {savings:,.2f}k (-{savings_pct:.1f}%)")

    print("\nReal-World Takeaway:")
    print("   Telecommunications and utility companies use Kruskal's MST algorithm to connect")
    print("   all locations to a shared network backbone at the absolute lowest total infrastructure cost.")
    print("==========================================================================\n")


if __name__ == "__main__":
    run_kruskal_demo()
