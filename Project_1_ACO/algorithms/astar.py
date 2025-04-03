import heapq

def heuristic(node, goal):
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

def is_valid_move(grid, node):
    x, y = node
    rows, cols = grid.shape
    return 0 <= x < rows and 0 <= y < cols and grid[x, y] == 0

def astar(grid, start, goal):
    heap = [(0 + heuristic(start, goal), 0, start, [start])]
    visited = set()

    while heap:
        (f, g, node, path) = heapq.heappop(heap)
        if node in visited:
            continue
        if node == goal:
            return path

        visited.add(node)
        for move in [(0,1),(1,0),(0,-1),(-1,0)]:
            next_node = (node[0]+move[0], node[1]+move[1])
            if is_valid_move(grid, next_node):
                heapq.heappush(heap, (g + 1 + heuristic(next_node, goal), g + 1, next_node, path + [next_node]))

    return None
