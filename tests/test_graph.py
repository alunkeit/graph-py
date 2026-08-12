import pytest
from graph.types.node import Node
from graph.types.edge import Edge
from graph.types.graph import UndirectedGraph


def test_graph_initialization():
    n1 = Node("n1")
    n2 = Node("n2")
    e1 = Edge("e1", n1, n2)

    nodes = {"n1": n1, "n2": n2}
    edges = [e1]
    graph = UndirectedGraph(edges, nodes)

    assert graph.nodes == nodes
    assert graph.edges == edges
    assert len(graph) == 2
    assert str(graph) == "UndirectedGraph(1 _edges, 2 _nodes)"
    assert repr(graph) == "<UndirectedGraph(1 _edges, 2 _nodes)>"


def test_graph_node_lookup_and_keyerror():
    n1 = Node("n1")
    graph = UndirectedGraph([], {"n1": n1})

    assert graph.node("n1") == n1
    assert graph["n1"] == n1

    with pytest.raises(KeyError) as exc_info:
        graph.node("non_existent")
    assert "non_existent" in str(exc_info.value)


def test_graph_contains_and_iter():
    n1 = Node("n1")
    n2 = Node("n2")
    graph = UndirectedGraph([], {"n1": n1, "n2": n2})

    assert "n1" in graph
    assert n1 in graph
    assert "n3" not in graph
    assert Node("n3") not in graph

    nodes_list = list(graph)
    assert nodes_list == [n1, n2]


def test_insert_from_nodes_reuses_existing_nodes():
    graph = UndirectedGraph([], {})
    s = Node("n1")
    t = Node("n2")

    graph.insert_from_nodes("e1", s, t)
    assert len(graph.nodes) == 2
    assert len(graph.edges) == 1

    # Insert another edge sharing node n1
    s2 = Node("n1")  # duplicate node instance for n1
    t2 = Node("n3")
    graph.insert_from_nodes("e2", s2, t2)

    assert len(graph.nodes) == 3
    assert len(graph.edges) == 2
    # Ensure n1 object in graph retains both edges
    n1_ref = graph["n1"]
    assert len(n1_ref.edges) == 2


def test_insert_edge():
    graph = UndirectedGraph([], {})
    n1 = Node("n1")
    n2 = Node("n2")
    e1 = Edge("e1", n1, n2)

    graph.insert_edge(e1)
    assert len(graph.edges) == 1
    assert "n1" in graph
    assert "n2" in graph

    # Inserting another edge referencing a new instance of n1
    n1_alt = Node("n1")
    n3 = Node("n3")
    e2 = Edge("e2", n1_alt, n3)
    graph.insert_edge(e2)

    assert len(graph.edges) == 2
    assert len(graph.nodes) == 3
    # Verify existing n1 node in graph has edge e2 added
    assert e2 in graph["n1"].edges


def test_remove_edge():
    n1 = Node("n1")
    n2 = Node("n2")
    e1 = Edge("e1", n1, n2)
    graph = UndirectedGraph([e1], {"n1": n1, "n2": n2})

    assert e1 in graph.edges
    assert e1 in n1.edges
    assert e1 in n2.edges

    graph.remove_edge(e1)
    assert e1 not in graph.edges
    assert e1 not in n1.edges
    assert e1 not in n2.edges
