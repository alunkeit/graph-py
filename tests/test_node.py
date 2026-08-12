import pytest
from graph.types.node import Node


def test_node_creation():
    node = Node("n1")
    assert node.name == "n1"
    assert node.edges == set()
    assert node.edge_count() == 0
    assert len(node) == 0


def test_node_str_and_repr():
    node = Node("n1")
    assert str(node) == "n1"
    assert repr(node) == "n1"


def test_node_add_and_remove_edge():
    node = Node("n1")
    dummy_edge1 = "edge1"
    dummy_edge2 = "edge2"

    node.add_edge(dummy_edge1)
    assert node.edges == {"edge1"}
    assert node.edge_count() == 1
    assert len(node) == 1

    # Adding same edge twice should be ignored
    node.add_edge(dummy_edge1)
    assert node.edge_count() == 1

    node.add_edge(dummy_edge2)
    assert node.edge_count() == 2
    assert len(node) == 2

    # Remove edge
    node.remove_edge(dummy_edge1)
    assert node.edges == {"edge2"}
    assert node.edge_count() == 1

    # Removing non-existent edge should not raise error
    node.remove_edge("non_existent")
    assert node.edge_count() == 1


def test_node_equality_and_hash():
    node1 = Node("n1")
    node2 = Node("n1")
    node3 = Node("n2")

    assert node1 == node2
    assert node1 != node3
    assert node1 != "n1"
    assert hash(node1) == hash(node2)
    assert hash(node1) != hash(node3)

