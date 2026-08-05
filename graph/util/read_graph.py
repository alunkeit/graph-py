import xml.etree.ElementTree as ET
from graph.types.node import Node, Edge
from graph.types.graph import UndirectedGraph


def load_graphml(filepath: str) -> UndirectedGraph:
    """
    Read a GraphML file and convert it into a graph object.
    """
    tree = ET.parse(filepath)
    root = tree.getroot()
    ns = {'g': 'http://graphml.graphdrawing.org/xmlns'}

    nodes_dict = {}

    # Read _nodes
    for node_elem in root.findall('.//g:node', ns):
        node_id = node_elem.attrib['id']
        nodes_dict[node_id] = Node(node_id)

    # Read _edges
    edges = []
    for edge_elem in root.findall('.//g:edge', ns):
        edge_id = edge_elem.attrib.get('id', f"e_{len(edges)}")
        src_id = edge_elem.attrib['source']
        tgt_id = edge_elem.attrib['target']

        src_node = nodes_dict[src_id]
        tgt_node = nodes_dict[tgt_id]

        e = Edge(edge_id, src_node, tgt_node)
        src_node.add_edge(e)
        tgt_node.add_edge(e)
        edges.append(e)

    graph = UndirectedGraph(edges, nodes_dict)
    return graph, nodes_dict


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
