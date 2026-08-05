"""Implementation of Breadth First Search."""
__author__ = "alunkeit"
from collections import deque
from graph.types.node import Node
from graph.types.graph import UndirectedGraph


class BreadthFirstSearch:
    """
    Class implementing breadth-first search (BFS) on an instance of
    UndirectedGraph.
    """

    def __init__(self):
        pass

    @staticmethod
    def search(graph: UndirectedGraph, s: str, t: str) -> list[Node] | None:
        """
        Find the shortest path from the start node s to the target node t.

        :param graph: The graph as an UndirectedGraph object
        :param s: Name of the start node (e.g. 'n0')
        :param t: Name of the target node (e.g. 'n49')
        :return: List of Node objects on the shortest path from s to t,
                 or None if no path exists.
        """
        if graph is None:
            raise ValueError("Kein UndirectedGraph übergeben.")

        start_node = graph.node(s)
        target_node = graph.node(t)

        if start_node.name == target_node.name:
            return [start_node]

        # BFS queue stores paths of Node objects
        # deque is a double-ended queue
        queue = deque([[start_node]])
        # stores _nodes that have already been visited
        visited = {start_node.name}

        while queue:
            path = queue.popleft()
            current_node = path[-1]

            # Target reached?
            if current_node.name == target_node.name:
                return path

            # Iterate over all _edges outgoing from the node
            for edge in current_node.edges:
                # Determine the neighbor node via edge.other(current_node._name)
                neighbor = edge.other(current_node.name)

                if neighbor.name not in visited:
                    visited.add(neighbor.name)
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)

        return None


if __name__ == "__main__":
    import os
    from graph.util.read_graph import load_graphml

    graph_file = os.path.join("in/random_graph.graphml")
    g, _ = load_graphml(graph_file)

    path = BreadthFirstSearch.search(g, "n0", "n49")

    if path:
        print(f"BFS Pfad von n0 nach n49 ({len(path)-1} Kanten):")
        print(" -> ".join([node._name for node in path]))
    else:
        print("Kein Pfad gefunden.")
