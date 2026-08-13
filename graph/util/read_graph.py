"""Helper module to load GraphML format files into graph structures."""
from __future__ import annotations
import xml.etree.ElementTree as ET
from pathlib import Path

__author__ = "alunkeit"

from graph.types.node import Node
from graph.types.edge import Edge
from graph.types.graph import Graph, UndirectedGraph, DirectedGraph


def load_graphml(filepath: str | Path) -> tuple[Graph, dict[str, Node]]:
    """
    Read a GraphML file and convert it into a Graph object (DirectedGraph or UndirectedGraph).
    Supports reading edge weights if defined via <data key="d0"> or <data key="weight">.
    """
    path = Path(filepath)
    if not path.is_file():
        raise FileNotFoundError(f"GraphML file not found at '{filepath}'")

    try:
        tree = ET.parse(path)
    except ET.ParseError as e:
        raise ValueError(f"Invalid XML syntax in GraphML file '{filepath}': {e}") from e

    root = tree.getroot()
    ns = {'g': 'http://graphml.graphdrawing.org/xmlns'}

    graph_elem = root.find('.//g:graph', ns)
    is_directed = False
    if graph_elem is not None and graph_elem.attrib.get('edgedefault') == 'directed':
        is_directed = True

    nodes_dict: dict[str, Node] = {}

    for node_elem in root.findall('.//g:node', ns):
        node_id = node_elem.attrib['id']
        nodes_dict[node_id] = Node(node_id)

    edges: list[Edge] = []
    for edge_elem in root.findall('.//g:edge', ns):
        edge_id = edge_elem.attrib.get('id', f"e_{len(edges)}")
        src_id = edge_elem.attrib['source']
        tgt_id = edge_elem.attrib['target']

        src_node = nodes_dict[src_id]
        tgt_node = nodes_dict[tgt_id]

        weight = 1.0
        for data_elem in edge_elem.findall('g:data', ns):
            key = data_elem.attrib.get('key', '')
            if key in ('d0', 'weight') and data_elem.text is not None:
                try:
                    weight = float(data_elem.text)
                except ValueError:
                    pass

        if 'weight' in edge_elem.attrib:
            try:
                weight = float(edge_elem.attrib['weight'])
            except ValueError:
                pass

        e = Edge(edge_id, src_node, tgt_node, weight=weight, directed=is_directed)
        edges.append(e)

    if is_directed:
        graph: Graph = DirectedGraph(edges, nodes_dict)
    else:
        graph = UndirectedGraph(edges, nodes_dict)

    return graph, nodes_dict
