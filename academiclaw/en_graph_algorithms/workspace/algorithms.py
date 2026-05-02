"""
Graph Algorithms - Spec-only stubs

This file contains only the public API (signatures and docstrings)
for the required algorithms used by the grader. Implementations were
removed to leave a minimal code spec for students to complete.

Required functions (stubbed here):
- dijkstra
- bellman_ford
- floyd_warshall
- kruskal_mst
- topological_sort

Keep signatures and documentation; raise NotImplementedError for bodies.
"""
from __future__ import annotations
from typing import Dict, List, Optional, Tuple
# Import Graph from context module.
from context.graph import Graph


def dijkstra(graph: Graph, source: int) -> Tuple[Dict[int, float], Dict[int, Optional[int]]]:
    """
    Dijkstra's single-source shortest paths.
    Returns `(dist, predecessor)` where `dist[v]` is the shortest distance from `source`.
    """
    raise NotImplementedError


def bellman_ford(graph: Graph, source: int) -> Tuple[Dict[int, float], Dict[int, Optional[int]], bool]:
    """
    Bellman-Ford single-source shortest paths.
    Returns `(dist, predecessor, has_negative_cycle)`.
    """
    raise NotImplementedError


def floyd_warshall(graph: Graph) -> Tuple[Dict[int, Dict[int, float]], Dict[int, Dict[int, Optional[int]]]]:
    """
    Floyd-Warshall all-pairs shortest paths.
    Returns `(dist, next)` where `dist[i][j]` is shortest distance and `next` is used for paths.
    """
    raise NotImplementedError
def kruskal_mst(graph: Graph) -> Tuple[List[Tuple[int, int, float]], float]:
    """
    Kruskal's minimum spanning tree for undirected graphs.
    Returns `(mst_edges, total_weight)`.
    """
    raise NotImplementedError


def topological_sort(graph: Graph) -> List[int]:
    """
    Topological sort for directed acyclic graphs.
    Returns a list of vertices in topological order.
    """
    raise NotImplementedError


