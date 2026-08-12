"""Helper module to load GraphML format files into graph structures."""
from __future__ import annotations
import xml.etree.ElementTree as ET
from pathlib import Path

__author__ = "alunkeit"

from graph.types.node import Node
from graph.types.edge import Edge
from graph.types.graph import UndirectedGraph


def load_graphml(filepath: str | Path) -> tuple[UndirectedGraph, dict[str, Node]]:
    """
    Read a GraphML file and convert it into an UndirectedGraph object.
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

        e = Edge(edge_id, src_node, tgt_node)
        edges.append(e)

    graph = UndirectedGraph(edges, nodes_dict)
    return graph, nodes_dict




