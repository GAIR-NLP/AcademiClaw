"""Graph data structure implementation."""

from typing import Dict, List, Tuple, Set, Optional
import heapq


class Graph:
    """Weighted graph implementation using adjacency list."""
    
    def __init__(self, directed: bool = False):
        self.adjacency_list: Dict[int, List[Tuple[int, float]]] = {}
        self.directed = directed
        self.vertices: Set[int] = set()
    
    def add_vertex(self, vertex: int) -> None:
        """Add a vertex to the graph."""
        if vertex not in self.vertices:
            self.vertices.add(vertex)
            self.adjacency_list[vertex] = []
    
    def add_edge(self, u: int, v: int, weight: float = 1.0) -> None:
        """Add an edge to the graph."""
        # Add vertices if they don't exist
        self.add_vertex(u)
        self.add_vertex(v)
        
        # Add edge
        self.adjacency_list[u].append((v, weight))
        
        # Add reverse edge for undirected graphs
        if not self.directed:
            self.adjacency_list[v].append((u, weight))
    
    def remove_edge(self, u: int, v: int) -> None:
        """Remove an edge from the graph."""
        if u in self.adjacency_list:
            self.adjacency_list[u] = [(x, w) for x, w in self.adjacency_list[u] if x != v]
        
        if not self.directed and v in self.adjacency_list:
            self.adjacency_list[v] = [(x, w) for x, w in self.adjacency_list[v] if x != u]
    
    def get_neighbors(self, vertex: int) -> List[Tuple[int, float]]:
        """Get neighbors of a vertex."""
        return self.adjacency_list.get(vertex, [])
    
    def get_vertices(self) -> List[int]:
        """Get all vertices in the graph."""
        return list(self.vertices)
    
    def get_edges(self) -> List[Tuple[int, int, float]]:
        """Get all edges in the graph."""
        edges = []
        for u in self.adjacency_list:
            for v, weight in self.adjacency_list[u]:
                if not self.directed:
                    # Avoid duplicate edges in undirected graphs
                    if (v, u, weight) not in edges:
                        edges.append((u, v, weight))
                else:
                    edges.append((u, v, weight))
        return edges
    
    def has_edge(self, u: int, v: int) -> bool:
        """Check if an edge exists."""
        if u not in self.adjacency_list:
            return False
        return any(x == v for x, _ in self.adjacency_list[u])
    
    def get_edge_weight(self, u: int, v: int) -> Optional[float]:
        """Get the weight of an edge."""
        if u not in self.adjacency_list:
            return None
        for x, weight in self.adjacency_list[u]:
            if x == v:
                return weight
        return None
    
    def is_empty(self) -> bool:
        """Check if the graph is empty."""
        return len(self.vertices) == 0
    
    def vertex_count(self) -> int:
        """Get the number of vertices."""
        return len(self.vertices)
    
    def edge_count(self) -> int:
        """Get the number of edges."""
        return len(self.get_edges())
    
    def __str__(self) -> str:
        """String representation of the graph."""
        result = f"Graph(directed={self.directed}, vertices={len(self.vertices)})\n"
        for vertex in sorted(self.vertices):
            neighbors = self.adjacency_list[vertex]
            if neighbors:
                result += f"  {vertex}: {neighbors}\n"
        return result