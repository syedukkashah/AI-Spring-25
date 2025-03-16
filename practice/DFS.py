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
            if maze[i][j] == 1:
                neighbors = []
                for dx, dy in directions:
                    nx, ny = i + dx, j + dy
                    if 0<=nx<rows and 0<=ny<cols and maze[nx][ny]==1:
                        neighbors.append((nx,ny))
                        graph[(i,j)] = neighbors
    
    return graph

def dfs(graph, start, goal):
    visited = set()
    stack = []
    visited.add(start)
    stack.append(start)
    while stack:
        node = stack.pop() #we pop the last element instead of the first element
        if node == goal:
            print("Goal found")
            break
        for node in reversed(graph[node]): #we use reversed to ensure L->R traversal
            if node not in visited:
                visited.add(node)
                print(node)
                stack.append(node)
                
graph = createGraph(maze)
dfs(graph, (0,0), (2,2))
