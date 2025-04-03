from collections import deque

def is_valid_move(grid, node):
    x, y = node
    rows, cols = grid.shape
    return 0 <= x < rows and 0 <= y < cols and grid[x, y] == 0

def bfs(grid, start, goal):
    queue = deque([(start, [start])])
    visited = set()

    while queue:
        (node, path) = queue.popleft()
        if node in visited:
            continue

        if node == goal:
            return path

        visited.add(node)
        for move in [(0,1), (1,0), (0,-1), (-1,0)]:
            next_node = (node[0]+move[0], node[1]+move[1])
            if is_valid_move(grid, next_node):
                queue.append((next_node, path + [next_node]))

    return None
