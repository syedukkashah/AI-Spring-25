maze = [
    [1,1,0],
    [0,1,0],
    [0,1,1]
]

directions = [[1,0], [0,1]]

def create_graph(maze):
    directions = [[1,0], [0,1]]
    graph = {}
    rows = len(maze)
    cols = len(maze[0])
    for i in range(rows):
        for j in range(cols):
            if maze[i][j] == 1:
                neighbors = []
                for dx, dy in directions:
                    nx, ny = dx + i, dy + j
                    if 0<=nx<rows and 0<=ny<cols and maze[nx][ny] == 1:
                        neighbors.append((nx,ny))
                        graph[(i,j)] = neighbors
    return graph

def bfs(graph, start, goal):
    visited = []
    queue = []
    visited.append(start)
    queue.append(start)
    while queue:
        node = queue.pop(0)
        if node == goal:
            print("Goal found")
            break
        for neighbor in graph[node]:
            if neighbor not in visited:
                print(f"visiting {neighbor}")
                queue.append(neighbor)
                visited.append(neighbor)
                
graph = create_graph(maze)
print(graph)
bfs(graph, (0,0), (2,2))
