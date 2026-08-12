import pytest
from graph.types.node import Node
from graph.types.edge import Edge
from graph.types.graph import UndirectedGraph
from graph.search.bfs_search import BreadthFirstSearch


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


def test_bfs_shortest_path(sample_graph):
    # Shortest path n0 to n4: n0 -> n1 -> n4 (length 3 nodes / 2 edges)
    alg = BreadthFirstSearch(sample_graph)
    path = alg.search("n0", "n4")
    assert path is not None
    node_names = [node.name for node in path]
    assert node_names == ["n0", "n1", "n4"] or node_names == ["n0", "n3", "n4"]


def test_bfs_start_equals_target(sample_graph):
    alg = BreadthFirstSearch(sample_graph)
    path = alg.search("n0", "n0")
    assert path is not None
    assert [node.name for node in path] == ["n0"]


def test_bfs_unreachable_node():
    n0 = Node("n0")
    n1 = Node("n1")
    e1 = Edge("e1", n0, n1)

    n2 = Node("n2")  # Isolated node
    graph = UndirectedGraph([e1], {"n0": n0, "n1": n1, "n2": n2})

    alg = BreadthFirstSearch(graph)
    path = alg.search( "n0", "n2")
    assert path is None


def test_bfs_shortest_path_with_nodes(sample_graph):
    alg = BreadthFirstSearch(sample_graph)
    path = alg.search(sample_graph["n0"], sample_graph["n4"])
    assert path is not None
    node_names = [node.name for node in path]
    assert node_names in (["n0", "n1", "n4"], ["n0", "n3", "n4"])


def test_bfs_none_graph():
    with pytest.raises(ValueError) as exc_info:
        alg = BreadthFirstSearch(None)
        alg.search("n0", "n1")
    assert "Graph instance cannot be None." in str(exc_info.value)



def test_bfs_invalid_node_names(sample_graph):
    with pytest.raises(KeyError):
        alg = BreadthFirstSearch(sample_graph)
        alg.search("invalid", "n1")

    with pytest.raises(KeyError):
        alg = BreadthFirstSearch(sample_graph)
        alg.search("n0", "invalid")
