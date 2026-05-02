# Dijkstra Algorithm Performance Optimization Project Description

## Project Overview
This project provides an original implementation of Dijkstra's shortest path algorithm. The project aims to improve execution performance on large-scale graphs by optimizing the algorithm implementation.

## File Structure Description

### 1. query.md
Project requirements document containing the original task description, optimization goals, and evaluation requirements.

### 2. dijkstra_original.py
Original implementation of Dijkstra's algorithm using a simple traversal method to find shortest paths:
- Uses dictionaries to store graph structure
- Uses sets to track visited nodes
- Finds the node with minimum distance by traversing all nodes
- Time complexity is O(V^2); the main bottleneck is the linear-time search for the minimum-distance unvisited node at each step

### 3. test_dijkstra.py
Test script for manually testing and verifying the functionality and performance of the Dijkstra algorithm. Includes test cases of different scales (small graph, medium graph, large graph).

### 4. requirements.txt
Python dependency configuration file.
