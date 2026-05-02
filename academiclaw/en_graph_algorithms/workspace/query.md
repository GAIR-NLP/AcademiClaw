**Task: Implement graph algorithms for network analysis**

You are tasked with implementing several graph algorithms to analyze network topology and find optimal paths. The implementation should be efficient and well-documented.

**Context:**
- A graph representation module is provided in `context/graph.py`
- You need to implement the algorithms in `algorithms.py`

**Requirements:**
1. Implement the following algorithms in `algorithms.py`:
   - Dijkstra's shortest path algorithm
   - Bellman-Ford algorithm (for graphs with negative edges)
   - Floyd-Warshall all-pairs shortest paths
   - Kruskal's minimum spanning tree
   - Topological sort for directed acyclic graphs
2. Each algorithm should:
   - Handle edge cases (empty graph, disconnected components, etc.)
   - Return appropriate data structures (paths, distances, trees)
   - Include time complexity analysis in comments
3. Create a performance comparison report `performance_report.txt` that compares the algorithms on different graph sizes

**Important - Deliverable Location:**
- **Put all deliverables directly in this directory (outside of `context/`)**
- Do NOT put deliverables inside `context/` - they will not be evaluated

**Deliverable:**
- `algorithms.py` - Implemented algorithms (in this directory, not in context/)
- `performance_report.txt` - Performance comparison report (in this directory, not in context/)

**Evaluation:**
The implementation will be evaluated based on correctness, efficiency, and documentation quality.

Note: the spec is in `algorithms.py`.