import numpy as np

def create_grid_map(size=(10, 10), obstacle_ratio=0.2):
    grid = np.zeros(size, dtype=int)
    num_obstacles = int(size[0] * size[1] * obstacle_ratio)
    obstacles = np.random.choice(size[0]*size[1], num_obstacles, replace=False)
    grid[np.unravel_index(obstacles, size)] = 1
    return grid
