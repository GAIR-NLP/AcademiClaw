import time
import random

class Graph:
    def __init__(self):
        self.graph = {}
        
    def add_edge(self, u, v, weight):
        if u not in self.graph:
            self.graph[u] = []
        self.graph[u].append((v, weight))
        
        if v not in self.graph:
            self.graph[v] = []
        self.graph[v].append((u, weight))
    
    def dijkstra(self, start):
        distances = {node: float('infinity') for node in self.graph}
        distances[start] = 0
        visited = set()
        
        while visited != set(self.graph.keys()):
            min_node = None
            min_dist = float('infinity')
            for node in self.graph:
                if node not in visited and distances[node] < min_dist:
                    min_node = node
                    min_dist = distances[node]
            
            visited.add(min_node)
            
            for neighbor, weight in self.graph.get(min_node, []):
                if neighbor not in visited:
                    new_distance = distances[min_node] + weight
                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
        
        return distances