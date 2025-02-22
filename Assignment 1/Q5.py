import heapq
from collections import deque

# Graph representation with cities as nodes and distances as edge weights
graph = {
    "Arad": {"Zerind": 75, "Sibiu": 140, "Timisoara": 118},
    "Zerind": {"Arad": 75, "Oradea": 71},
    "Oradea": {"Zerind": 71, "Sibiu": 151},
    "Sibiu": {"Arad": 140, "Oradea": 151, "Fagaras": 99, "Rimnicu Vilcea": 80},
    "Timisoara": {"Arad": 118, "Lugoj": 111},
    "Lugoj": {"Timisoara": 111, "Mehadia": 70},
    "Mehadia": {"Lugoj": 70, "Drobeta": 75},
    "Drobeta": {"Mehadia": 75, "Craiova": 120},
    "Craiova": {"Drobeta": 120, "Rimnicu Vilcea": 146, "Pitesti": 138},
    "Rimnicu Vilcea": {"Sibiu": 80, "Craiova": 146, "Pitesti": 97},
    "Fagaras": {"Sibiu": 99, "Bucharest": 211},
    "Pitesti": {"Rimnicu Vilcea": 97, "Craiova": 138, "Bucharest": 101},
    "Bucharest": {"Fagaras": 211, "Pitesti": 101, "Giurgiu": 90, "Urziceni": 85},
    "Giurgiu": {"Bucharest": 90},
    "Urziceni": {"Bucharest": 85, "Vaslui": 142, "Hirsova": 98},
    "Hirsova": {"Urziceni": 98, "Eforie": 86},
    "Eforie": {"Hirsova": 86},
    "Vaslui": {"Urziceni": 142, "Iasi": 92},
    "Iasi": {"Vaslui": 92, "Neamt": 87},
    "Neamt": {"Iasi": 87}
}

# Heuristic values (straight-line distance to Bucharest)
heuristics = {
    "Arad": 366, "Bucharest": 0, "Craiova": 160, "Drobeta": 242,
    "Eforie": 161, "Fagaras": 176, "Giurgiu": 77, "Hirsova": 151,
    "Iasi": 226, "Lugoj": 244, "Mehadia": 241, "Neamt": 234,
    "Oradea": 380, "Pitesti": 100, "Rimnicu Vilcea": 193, "Sibiu": 253,
    "Timisoara": 329, "Urziceni": 80, "Vaslui": 199, "Zerind": 374
}

# Breadth-First Search (BFS) Algorithm
def breadth_first_search(start, goal):
    queue = deque([(start, [start], 0)])
    visited = set()
    while queue:
        node, path, cost = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        if node == goal:
            return path, cost
        for neighbor, weight in graph[node].items():
            queue.append((neighbor, path + [neighbor], cost + weight))
    return None, float("inf")

# Uniform Cost Search (UCS) Algorithm
def uniform_cost_search(start, goal):
    pq = [(0, start, [start])]
    visited = set()
    while pq:
        cost, node, path = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)
        if node == goal:
            return path, cost
        for neighbor, weight in graph[node].items():
            heapq.heappush(pq, (cost + weight, neighbor, path + [neighbor]))
    return None, float("inf")

# Greedy Best-First Search (GBFS) Algorithm
def greedy_best_first_search(start, goal):
    pq = [(heuristics[start], start, [start])]
    visited = set()
    while pq:
        _, node, path = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)
        if node == goal:
            return path, sum(graph[path[i]][path[i+1]] for i in range(len(path)-1))
        for neighbor in graph[node]:
            heapq.heappush(pq, (heuristics[neighbor], neighbor, path + [neighbor]))
    return None, float("inf")

# Iterative Deepening Depth-First Search (IDDFS) Algorithm
def iterative_deepening_dfs(start, goal):
    def dls(node, depth, path, cost):
        if depth == 0 and node == goal:
            return path, cost
        if depth > 0:
            for neighbor, weight in graph[node].items():
                if neighbor not in path:
                    result = dls(neighbor, depth-1, path + [neighbor], cost + weight)
                    if result:
                        return result
        return None
    depth = 0
    while True:
        result = dls(start, depth, [start], 0)
        if result:
            return result
        depth += 1

# Function to compare different search algorithms
def compare_algorithms(start, goal):
    results = {
        "BFS": breadth_first_search(start, goal),
        "UCS": uniform_cost_search(start, goal),
        "GBFS": greedy_best_first_search(start, goal),
        "IDDFS": iterative_deepening_dfs(start, goal)
    }
    sorted_results = sorted(results.items(), key=lambda x: x[1][1])
    for algo, (path, cost) in sorted_results:
        print(f"{algo}: Path = {path}, Cost = {cost}")

# Define start and goal cities and run the comparison
start_city = "Arad"
goal_city = "Bucharest"
compare_algorithms(start_city, goal_city)
