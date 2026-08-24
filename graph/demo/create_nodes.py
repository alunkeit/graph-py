from graph.types.node import Node
from graph.types.edge import Edge
__author__ = "alunkeit"


def run_main_demo() -> None:
    """Demonstrates basic Node and Edge creation."""
    print("\n--- Graph Demonstration (create_nodes.py) ---")
    x1 = Node("x1")
    x2 = Node("x2")
    Edge("e0", x1, x2)

    nodes: list[Node] = []
    edges: list[Edge] = []

    for i in range(10):
        x = Node(f"x{i}")
        print(f"New node: {x}")
        nodes.append(x)

    for i in range(9):
        s = nodes[i]
        t = nodes[i + 1]
        e = Edge(f"e{i}", s, t)
        edges.append(e)
        print(f"New edge: {e}")

    print("\nCreated edges:")
    for e in edges:
        print(f"  {e}")


if __name__ == "__main__":
    run_main_demo()


