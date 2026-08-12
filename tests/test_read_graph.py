import os
import pytest
from graph.util.read_graph import load_graphml
from graph.types.graph import UndirectedGraph


def test_load_graphml_existing_file():
    filepath = os.path.join("in", "random_graph.graphml")
    assert os.path.exists(filepath), f"Test graphml file not found at {filepath}"

    graph, nodes_dict = load_graphml(filepath)

    assert isinstance(graph, UndirectedGraph)
    assert isinstance(nodes_dict, dict)
    assert len(graph.nodes) > 0
    assert len(graph.edges) > 0
    assert "n0" in graph.nodes


def test_load_graphml_custom_content(tmp_path):
    graphml_content = """<?xml version="1.0" encoding="UTF-8"?>
<graphml xmlns="http://graphml.graphdrawing.org/xmlns">
  <graph id="G" edgedefault="undirected">
    <node id="nA"/>
    <node id="nB"/>
    <edge id="e1" source="nA" target="nB"/>
  </graph>
</graphml>"""

    file_path = tmp_path / "test.graphml"
    file_path.write_text(graphml_content, encoding="utf-8")

    graph, nodes_dict = load_graphml(str(file_path))

    assert len(graph.nodes) == 2
    assert len(graph.edges) == 1
    assert "nA" in graph.nodes
    assert "nB" in graph.nodes
    assert graph.edges[0].name == "e1"
