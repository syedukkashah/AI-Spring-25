maze = [
    [1,1,0],
    [0,1,0],
    [0,1,1]
]

def createGraph(maze):
    directions = [[0,1], [1,0]]
    graph = {}
    rows = len(maze)
    cols = len(maze[0])
    for i in range(rows):
        for j in range(cols):
            if maze[i][j] == 1: #if path is open we check if open path neighbors exist
                neighbors = []
                for dx, dy in directions:
                    nx, ny = i + dx, j + dy #neighbor indices (right and down according to the given direction constraints)
                    if 0<=nx<rows and 0<=ny<cols and maze[nx][ny]==1: #checking if neighbors are open path
                        neighbors.append((nx,ny)) #adding to neighbor list
                        graph[(i,j)] = neighbors #init dict ket to neighbor list
    
    return graph

def bfs(graph, start, goal):
    visited = [] #keeping track of visited nodes
    queue = []
    visited.append(start)
    queue.append(start)
    while queue:
        node = queue.pop(0) #popping the first node in the queue
        if node == goal:
            print("Goal reached")
            break
        for neighbor in graph[node]:
            if neighbor not in visited: #if a neighbor of the node hasn't been visited we visit it
                print(f"Visiting {neighbor}")
                visited.append(neighbor)
                queue.append(neighbor)
                

