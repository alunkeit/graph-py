import pytest
from graph.types.node import Node
from graph.types.edge import Edge

def test_edge_creation_registers_on_nodes():
    n1 = Node("n1")
    n2 = Node("n2")
    edge = Edge("e1", n1, n2)

    assert edge.name == "e1"
    assert edge.s == n1
    assert edge.t == n2
    assert not edge.directed
    assert not edge.is_directed()

    # Verify edge was automatically registered on both endpoint nodes
    assert edge in n1.edges
    assert edge in n2.edges


def test_directed_edge_creation():
    n1 = Node("n1")
    n2 = Node("n2")
    edge = Edge("e1", n1, n2, directed=True)

    assert edge.directed
    assert edge.is_directed()


def test_edge_other():
    n1 = Node("n1")
    n2 = Node("n2")
    edge = Edge("e1", n1, n2)

    assert edge.other("n1") == n2
    assert edge.other("n2") == n1

    with pytest.raises(ValueError) as exc_info:
        edge.other("n3")
    assert "n3" in str(exc_info.value)


def test_edge_str_and_repr():
    n1 = Node("n1")
    n2 = Node("n2")
    edge = Edge("e1", n1, n2)

    assert str(edge) == "n1 -> n2"
    assert repr(edge) == "e1: n1 -> n2"


def test_edge_equality_and_hash():
    n1 = Node("n1")
    n2 = Node("n2")
    e1 = Edge("e1", n1, n2)
    e2 = Edge("e1", n1, n2)
    e3 = Edge("e2", n1, n2)

    assert e1 == e2
    assert e1 != e3
    assert e1 != "e1"
    assert hash(e1) == hash(e2)
    assert hash(e1) != hash(e3)

