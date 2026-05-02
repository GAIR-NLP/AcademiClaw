import time
from dijkstra_original import Graph
import random

# Create a graph for testing with varying edge densities
def create_test_graph(size, density=0.2):
    """创建测试图
    
    Args:
        size: 图的节点数量
        density: 边密度 (0-1), 0表示稀疏图，1表示完全图
    """
    g = Graph()
    
    # 确保每个节点至少有一个边
    for i in range(size - 1):
        weight = random.randint(1, 10)
        g.add_edge(i, i + 1, weight)
    
    # 根据密度添加额外的边
    max_additional_edges = int((size * (size - 1) / 2) * density)
    added_edges = set()
    
    while len(added_edges) < max_additional_edges:
        u = random.randint(0, size - 1)
        v = random.randint(0, size - 1)
        if u != v and (u, v) not in added_edges and (v, u) not in added_edges:
            weight = random.randint(1, 10)
            g.add_edge(u, v, weight)
            added_edges.add((u, v))
    
    return g

# Performance test
if __name__ == "__main__":
    # 小图: 5张，节点数10-50
    print("=== 测试小图 ===")
    small_sizes = [10, 20, 30, 40, 50]
    small_densities = [0.1, 0.2, 0.3, 0.4, 0.5]
    for i in range(5):
        size = small_sizes[i]
        density = small_densities[i]
        g = create_test_graph(size, density)
        start_time = time.time()
        distances = g.dijkstra(0)
        end_time = time.time()
        print(f"小图{i+1}: 节点数={size}, 密度={density}, 耗时={end_time - start_time:.6f}秒")
    
    # 中图: 10张，节点数100-500
    print("\n=== 测试中图 ===")
    medium_sizes = [100, 150, 200, 250, 300, 350, 400, 450, 500, 500]
    medium_densities = [0.1, 0.15, 0.2, 0.25, 0.3, 0.1, 0.15, 0.2, 0.25, 0.3]
    for i in range(10):
        size = medium_sizes[i]
        density = medium_densities[i]
        g = create_test_graph(size, density)
        start_time = time.time()
        distances = g.dijkstra(0)
        end_time = time.time()
        print(f"中图{i+1}: 节点数={size}, 密度={density}, 耗时={end_time - start_time:.6f}秒")
    
    # 大图: 10张，节点数1000-5000
    print("\n=== 测试大图 ===")
    large_sizes = [1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5000]
    large_densities = [0.05, 0.075, 0.1, 0.125, 0.15, 0.05, 0.075, 0.1, 0.125, 0.15]
    for i in range(10):
        size = large_sizes[i]
        density = large_densities[i]
        g = create_test_graph(size, density)
        start_time = time.time()
        distances = g.dijkstra(0)
        end_time = time.time()
        print(f"大图{i+1}: 节点数={size}, 密度={density}, 耗时={end_time - start_time:.6f}秒")