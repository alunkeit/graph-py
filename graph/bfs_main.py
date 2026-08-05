from graph.util.read_graph import load_graphml

if __name__ == "__main__":

    filepath = "in/random_graph.graphml"
    g, nodes = load_graphml(filepath)

    print(f"Erfolgreich geladen: {len(nodes)} Knoten und {len(g.edges)} Kanten.")

    # Example output of the first 5 _nodes and _edges
    print("\nBeispiel-Knoten:")
    for n in list(nodes.values())[:5]:
        print(f"  Knoten {n._name} (Grad: {len(n.edges)})")

    print("\nBeispiel-Kanten:")
    for e in g.edges[:5]:
        print(f"  Kante {e}")