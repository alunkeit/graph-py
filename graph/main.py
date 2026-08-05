from graph.types.node import *

if __name__ == "__main__":
    x1 = Node("x1")
    x2 = Node("x2")
    e1 = Edge("e0", x1, x2)

    nodes = []
    edges = []

    for i in range(10):
        x = Node("x" + str(i))
        print(f"new node: {x}")
        nodes.append(x)

    for i in range(10):
        if i == 9:
            break
        s = nodes[i]
        t = nodes[i + 1]
        e = Edge("e" + str(i), s, t)
        edges.append(e)
        print(f"new edge: {e}")

    for e in edges:
        print(e)

