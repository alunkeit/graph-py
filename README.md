# graph-py

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A clean, modular Python library for graph data structures and graph search algorithms, featuring implementations of **Undirected Graph**, **Directed Graph**, **Breadth-First Search (BFS)**, **Depth-First Search (DFS)**, **Dijkstra's Shortest Path Algorithm**, and **Bellman-Ford Algorithm**.

> **Note**: This library is built for personal learning, exploration, and hands-on experiments with graph theory topics and algorithm implementations.

---

## 🌟 Features

- **Object-Oriented Graph Hierarchy**:
  - `Graph(ABC)`: Abstract base class defining common graph interface and neighbor traversal.
  - `UndirectedGraph`: Supports bidirectional edge relationships.
  - `DirectedGraph`: Supports directed edge relationships ($s \to t$).
  - `Node` & `Edge`: Rich node and edge objects with weight support (`weight: float`).
- **Search Algorithm Suite**:
  - `SearchAlgorithm(ABC)`: Abstract base class for search algorithms.
  - `BreadthFirstSearch` (`BFS`): Unweighted shortest path search using queue traversal.
  - `DepthFirstSearch` (`DFS`): Stack-based graph traversal.
  - `Dijkstra` / `DijkstraSearch`: Min-heap (`heapq`) priority queue shortest path search for non-negative edge weights.
  - `BellmanFord` / `BellmanFordSearch`: Shortest path algorithm supporting positive and **negative edge weights**, with negative weight cycle detection.
- **GraphML I/O Support**:
  - Read GraphML format files (`load_graphml`) with node IDs, edge connections, edge weights, and `edgedefault` graph types.
- **Interactive Console Menu & Demos**:
  - Built-in interactive CLI menu (`menu.py`) and standalone demonstration scripts.
- **Unit Tested**: Full test suite using `pytest`.

---

## 🚀 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/alunkeit/graph-py.git
   cd graph-py
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   *(Optional: Install `console-menu` for interactive terminal menus)*:
   ```bash
   pip install console-menu
   ```

---

## 💡 Quick Start & Usage Examples

### 1. Creating Graphs & Running Dijkstra's Shortest Path

```python
from graph.types import Node, Edge, DirectedGraph
from graph.search import Dijkstra

# Create a directed weighted graph
g = DirectedGraph()
n1, n2, n3, n4 = Node("n1"), Node("n2"), Node("n3"), Node("n4")

g.insert_from_nodes("e1", n1, n2, weight=4.0)
g.insert_from_nodes("e2", n1, n3, weight=1.0)
g.insert_from_nodes("e3", n3, n2, weight=2.0)
g.insert_from_nodes("e4", n2, n4, weight=1.0)

dijkstra = Dijkstra(g)
path, distance = dijkstra.search_with_distance("n1", "n4")
```

### 2. Running Bellman-Ford (with Negative Edge Weights)

```python
from graph.types import DirectedGraph, Node
from graph.search import BellmanFord

g = DirectedGraph()
na, nb, nc, nd = Node("A"), Node("B"), Node("C"), Node("D")

g.insert_from_nodes("e_ab", na, nb, weight=4.0)
g.insert_from_nodes("e_ac", na, nc, weight=2.0)
g.insert_from_nodes("e_cb", nc, nb, weight=-3.0)  # Negative edge weight
g.insert_from_nodes("e_bd", nb, nd, weight=2.0)

bf = BellmanFord(g)
path, distance = bf.search_with_distance("A", "D")
# Output path: A -> C -> B -> D (distance: 1.0)
```

### 3. Breadth-First Search (BFS) and Depth-First Search (DFS)

```python
from graph.types import UndirectedGraph, Node, Edge
from graph.search import BreadthFirstSearch, DepthFirstSearch

g = UndirectedGraph()
n0, n1, n2 = Node("n0"), Node("n1"), Node("n2")
g.insert_edge(Edge("e0", n0, n1))
g.insert_edge(Edge("e1", n1, n2))

bfs_path = BreadthFirstSearch(g).search("n0", "n2")
dfs_path = DepthFirstSearch(g).search("n0", "n2")
```

### 4. Loading GraphML Files

```python
from graph.util.read_graph import load_graphml
from graph.search import BellmanFord

# Load graph and node dictionary from GraphML file
graph, nodes = load_graphml("in/bellman_ford_graph.graphml")

# Run search on loaded graph
alg = BellmanFord(graph)
path, distance = alg.search_with_distance("n0", "n29")
```

---

## 🖥️ Running Demonstrations

You can execute the included demonstration modules directly from the command line:

```bash
# Run Bellman-Ford demonstration on bellman_ford_graph.graphml (with negative weights)
python -m graph.demo.bellman_ford_main

# Run Dijkstra demonstration on weighted_graph.graphml
python -m graph.demo.dijkstra_main

# Run BFS demonstration on random_graph.graphml
python -m graph.demo.bfs_main

# Run DFS demonstration on random_graph.graphml
python -m graph.demo.dfs_main

# Run basic graph creation demo
python -m graph.demo.main
```

### Interactive Console Menu

Run the interactive terminal menu:
```bash
python menu.py
```

---

## 🧪 Running Tests

Execute unit tests with `pytest`:

```bash
pytest
```

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
