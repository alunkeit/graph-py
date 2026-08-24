"""Real-World Demonstration: Currency Arbitrage Detection using Bellman-Ford Negative Cycle Search."""
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
from graph.types.graph import DirectedGraph
from graph.search.bellman_ford import BellmanFord
from graph.util.read_graph import load_graphml

__author__ = "alunkeit"

# Realistic Forex Exchange Rates table
DEFAULT_EXCHANGE_RATES: dict[tuple[str, str], float] = {
    ("USD", "EUR"): 0.92,
    ("EUR", "GBP"): 0.86,
    ("GBP", "JPY"): 195.50,
    ("JPY", "USD"): 0.0066,  # Loop USD -> EUR -> GBP -> JPY -> USD yields 1.02102 (2.1% profit)
    ("EUR", "USD"): 1.087,
    ("GBP", "USD"): 1.280,
    ("USD", "JPY"): 155.00,
    ("JPY", "EUR"): 0.0059,
    ("USD", "CAD"): 1.350,
    ("CAD", "USD"): 0.740,
    ("EUR", "CHF"): 0.950,
    ("CHF", "EUR"): 1.050,
}


def build_forex_graph(rates: dict[tuple[str, str], float]) -> tuple[DirectedGraph, dict[str, Node]]:
    """
    Builds a DirectedGraph where edge weights are -ln(exchange_rate).
    
    Mathematical Property:
    - Currency conversion rates multiply: Rate_total = r1 * r2 * ... * rk
    - Profitability condition: Rate_total > 1.0
    - Taking -ln transformation: sum(-ln(ri)) = -ln(Rate_total) < 0
    - Therefore: A profitable currency arbitrage loop IS a negative weight cycle!
    """
    nodes_dict: dict[str, Node] = {}
    edges: list[Edge] = []

    # Create node objects for unique currency codes
    currencies = set()
    for src, tgt in rates.keys():
        currencies.add(src)
        currencies.add(tgt)

    for curr in sorted(currencies):
        nodes_dict[curr] = Node(curr)

    edge_idx = 0
    for (src_code, tgt_code), rate in rates.items():
        src_node = nodes_dict[src_code]
        tgt_node = nodes_dict[tgt_code]
        # Weight transformation w = -ln(rate)
        weight = -math.log(rate)
        e = Edge(f"e_{edge_idx}", src_node, tgt_node, weight=weight, directed=True)
        edges.append(e)
        edge_idx += 1

    graph = DirectedGraph(edges, nodes_dict)
    return graph, nodes_dict


def find_arbitrage_cycle(graph: DirectedGraph, rates: dict[tuple[str, str], float], start_code: str = "USD") -> list[str] | None:
    """
    Finds a negative weight cycle (arbitrage loop) starting from start_code using edge relaxation tracing.
    """
    if start_code not in graph.nodes:
        return None

    num_nodes = len(graph.nodes)
    distances: dict[str, float] = {code: float("inf") for code in graph.nodes}
    distances[start_code] = 0.0
    parent: dict[str, str | None] = {code: None for code in graph.nodes}

    # Relax edges |V| - 1 times
    for _ in range(num_nodes - 1):
        for u_name, u_node in graph.nodes.items():
            if distances[u_name] == float("inf"):
                continue
            for v_node, edge in graph.get_neighbors(u_node):
                new_dist = distances[u_name] + edge.weight
                if new_dist < distances[v_node.name]:
                    distances[v_node.name] = new_dist
                    parent[v_node.name] = u_name

    # Check for edge that can still be relaxed (|V|-th pass)
    cycle_node: str | None = None
    for u_name, u_node in graph.nodes.items():
        if distances[u_name] == float("inf"):
            continue
        for v_node, edge in graph.get_neighbors(u_node):
            if distances[u_name] + edge.weight < distances[v_node.name]:
                cycle_node = v_node.name
                parent[v_node.name] = u_name
                break
        if cycle_node is not None:
            break

    if cycle_node is None:
        return None

    # Step back |V| times to ensure we are inside the cycle
    for _ in range(num_nodes):
        if cycle_node in parent and parent[cycle_node] is not None:
            cycle_node = parent[cycle_node]

    # Trace cycle backwards
    cycle: list[str] = [cycle_node]
    curr = parent.get(cycle_node)
    while curr is not None and curr != cycle_node and curr not in cycle:
        cycle.append(curr)
        curr = parent.get(curr)
    cycle.append(cycle_node)
    cycle.reverse()
    return cycle


def run_currency_arbitrage_demo(
    graphml_path: str | Path | None = "in/forex_arbitrage_graph.graphml",
    initial_investment: float = 10000.0,
    start_currency: str = "USD",
) -> None:
    """
    Demonstrates Currency Arbitrage Detection using Bellman-Ford Algorithm.
    """
    print("\n==========================================================================")
    print("REAL-WORLD DEMO: Forex Currency Arbitrage Detection (Bellman-Ford)")
    print("==========================================================================")

    rates = DEFAULT_EXCHANGE_RATES
    graph, nodes = build_forex_graph(rates)

    print(f"Loaded Forex Market Graph: {len(nodes)} currencies and {len(graph.edges)} directed conversion pairs.")
    print("\nSample Currency Exchange Rates & Log Weights (w = -ln(rate)):")
    print("-" * 65)
    for (src, tgt), rate in list(rates.items())[:6]:
        log_w = -math.log(rate)
        print(f"  1 {src} -> {rate:.4f} {tgt}  |  Edge Weight w = {log_w:+.5f}")

    print("-" * 65)
    print(f"\nExecuting Bellman-Ford search to detect negative weight cycles starting at '{start_currency}'...")

    # Run standard BellmanFord search
    bf = BellmanFord(graph)
    has_negative_cycle = False
    try:
        bf.search_with_distance(start_currency, "EUR")
    except ValueError as err:
        has_negative_cycle = True
        print(f"\nALERT: Bellman-Ford detected a negative weight cycle!")
        print(f"   ({err})")

    # Extract the arbitrage trade cycle
    arbitrage_cycle = find_arbitrage_cycle(graph, rates, start_currency)

    if arbitrage_cycle:
        print("\nARBITRAGE OPPORTUNITY DETECTED!")
        print("   Sequence of trades:")
        print("   " + " -> ".join(arbitrage_cycle))

        print(f"\nTrade Simulation (Starting Capital: ${initial_investment:,.2f} {arbitrage_cycle[0]}):")
        print("-" * 65)
        current_amount = initial_investment
        current_curr = arbitrage_cycle[0]

        for next_curr in arbitrage_cycle[1:]:
            rate = rates[(current_curr, next_curr)]
            next_amount = current_amount * rate
            print(f"   Trade: {current_amount:,.2f} {current_curr}  x  {rate:.4f}  =  {next_amount:,.2f} {next_curr}")
            current_amount = next_amount
            current_curr = next_curr

        profit = current_amount - initial_investment
        roi_pct = (profit / initial_investment) * 100
        print("-" * 65)
        print(f"   Final Capital: ${current_amount:,.2f} {arbitrage_cycle[-1]}")
        print(f"   Net Profit:    +${profit:,.2f} ({roi_pct:+.2f}% yield)")

    else:
        print("\n No arbitrage opportunities detected in the market.")

    print("\nReal-World Takeaway:")
    print("   Quantitative trading firms and hedge funds use Bellman-Ford's negative cycle")
    print("   detection algorithm on logarithmic FX rate graphs to execute high-frequency")
    print("   arbitrage trades in sub-milliseconds before markets re-align.")
    print("==========================================================================\n")


if __name__ == "__main__":
    run_currency_arbitrage_demo()
