import pytest
from graph.types.node import Node
from graph.types.edge import Edge
from graph.types.graph import UndirectedGraph
from graph.search.dfs import DepthFirstSearch


@pytest.fixture
def sample_graph():
    """
    Creates a sample graph:
    n0 --- n1 --- n2
     |      |
    n3 --- n4
    """
    nodes = {f"n{i}": Node(f"n{i}") for i in range(5)}
    edges = [
        Edge("e0", nodes["n0"], nodes["n1"]),
        Edge("e1", nodes["n1"], nodes["n2"]),
        Edge("e2", nodes["n0"], nodes["n3"]),
        Edge("e3", nodes["n3"], nodes["n4"]),
        Edge("e4", nodes["n1"], nodes["n4"]),
    ]
    return UndirectedGraph(edges, nodes)


def test_dfs_path(sample_graph):
    alg = DepthFirstSearch(sample_graph)
    path = alg.search("n0", "n4")
    assert path is not None
    assert path[0].name == "n0"
    assert path[-1].name == "n4"
    # Verify that returned path is valid (adjacent nodes connected by an edge)
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        assert any(e.other(u.name) is v for e in u.edges)


def test_dfs_start_equals_target(sample_graph):
    alg = DepthFirstSearch(sample_graph)
    path = alg.search("n0", "n0")
    assert path is not None
    assert [node.name for node in path] == ["n0"]


def test_dfs_unreachable_node():
    n0 = Node("n0")
    n1 = Node("n1")
    e1 = Edge("e1", n0, n1)

    n2 = Node("n2")  # Isolated node
    graph = UndirectedGraph([e1], {"n0": n0, "n1": n1, "n2": n2})

    alg = DepthFirstSearch(graph)
    path = alg.search("n0", "n2")
    assert path is None


def test_dfs_path_with_nodes(sample_graph):
    alg = DepthFirstSearch(sample_graph)
    path = alg.search(sample_graph["n0"], sample_graph["n4"])
    assert path is not None
    assert path[0] is sample_graph["n0"]
    assert path[-1] is sample_graph["n4"]


def test_dfs_none_graph():
    alg = DepthFirstSearch(None)
    with pytest.raises(ValueError) as exc_info:
        alg.search("n0", "n1")
    assert "Graph instance cannot be None." in str(exc_info.value)


def test_dfs_invalid_node_names(sample_graph):
    alg = DepthFirstSearch(sample_graph)
    with pytest.raises(KeyError):
        alg.search("invalid", "n1")

    with pytest.raises(KeyError):
        alg.search("n0", "invalid")


def test_dfs_graph_property(sample_graph):
    alg = DepthFirstSearch(sample_graph)
    assert alg.graph is sample_graph
