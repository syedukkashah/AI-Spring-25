from queue import PriorityQueue

# Given grid with costs and impassable cells ('#')from queue import PriorityQueue

# Given grid with costs and impassable cells ('#')
grid = [
    [1, 2, 3, '#', 4],
    [1, '#', 1, 2, 2],
    [2, 3, 1, '#', 1],
    ['#', '#', 2, 1, 1],
    [1, 1, 2, 2, 1]
]

# Directions: Right, Down, Left, Up
directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def heuristic(x, y, goal_x, goal_y):
    """Heuristic function using Manhattan distance."""
    return abs(goal_x - x) + abs(goal_y - y)

def a_star(grid):
    """A* algorithm to find the optimal path in an N x M weighted grid."""
    N, M = len(grid), len(grid[0])
    start, goal = (0, 0), (N - 1, M - 1)
    
    if grid[0][0] == '#' or grid[N-1][M-1] == '#':
        print("No possible path: Start or Goal is impassable.")
        return []
    
    pq = PriorityQueue()  # Min-heap based on f(n) = g(n) + h(n)
    pq.put((0, 0, 0))  # (f(n), x, y) starting at (0,0)
    
    g_cost = {(0, 0): 0}  # Cost from start to each node
    parent = {(0, 0): None}  # Parent tracking for path reconstruction
    
    while not pq.empty():
        f, x, y = pq.get()  # Get node with smallest f(n)

        if (x, y) == goal:
            # Reconstruct path
            path = []
            while (x, y) is not None:
                path.append((x, y))
                x, y = parent[(x, y)]
            return path[::-1]  # Reverse path from goal to start
        
        # Explore neighbors
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            if 0 <= nx < N and 0 <= ny < M and grid[nx][ny] != '#':  # Valid move
                new_cost = g_cost[(x, y)] + grid[nx][ny]
                
                if (nx, ny) not in g_cost or new_cost < g_cost[(nx, ny)]:
                    g_cost[(nx, ny)] = new_cost
                    f_cost = new_cost + heuristic(nx, ny, N - 1, M - 1)
                    pq.put((f_cost, nx, ny))
                    parent[(nx, ny)] = (x, y)
    
    print("No possible path found.")
    return []

# Run A* and print the optimal path
optimal_path = a_star(grid)
print("Optimal Path:", optimal_path)

grid = [
    [1, 2, 3, '#', 4],
    [1, '#', 1, 2, 2],
    [2, 3, 1, '#', 1],
    ['#', '#', 2, 1, 1],
    [1, 1, 2, 2, 1]
]

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def heuristic(x, y, goal_x, goal_y):
    """Heuristic function using Manhattan distance."""
    return abs(goal_x - x) + abs(goal_y - y)

def a_star(grid):
    """A* algorithm to find the optimal path in an N x M weighted grid."""
    N, M = len(grid), len(grid[0])
    start, goal = (0, 0), (N - 1, M - 1)
    
    if grid[0][0] == '#' or grid[N-1][M-1] == '#':
        print("No possible path: Start or Goal is impassable.")
        return []
    
    pq = PriorityQueue()  # Min-heap based on f(n) = g(n) + h(n)
    pq.put((0, 0, 0))  # (f(n), x, y) starting at (0,0)
    
    g_cost = {(0, 0): 0}  # Cost from start to each node
    parent = {(0, 0): None}  # Parent tracking for path reconstruction
    
    while not pq.empty():
        f, x, y = pq.get()  # Get node with smallest f(n)

        if (x, y) == goal:
            # Reconstruct path
            path = []
            while (x, y) is not None:
                path.append((x, y))
                x, y = parent[(x, y)]
            return path[::-1]  # Reverse path from goal to start
        
        # Explore neighbors
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            if 0 <= nx < N and 0 <= ny < M and grid[nx][ny] != '#':  # Valid move
                new_cost = g_cost[(x, y)] + grid[nx][ny]
                
                if (nx, ny) not in g_cost or new_cost < g_cost[(nx, ny)]:
                    g_cost[(nx, ny)] = new_cost
                    f_cost = new_cost + heuristic(nx, ny, N - 1, M - 1)
                    pq.put((f_cost, nx, ny))
                    parent[(nx, ny)] = (x, y)
    
    print("No possible path found.")
    return []

# Run A* and print the optimal path
optimal_path = a_star(grid)
print("Optimal Path:", optimal_path)
