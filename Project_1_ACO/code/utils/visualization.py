import matplotlib.pyplot as plt
import numpy as np

def visualize(grid, path=None, start=None, goal=None, title='Pathfinding'):
    plt.figure(figsize=(6, 6))
    plt.imshow(grid, cmap='gray_r')
    plt.title(title)

    if path:
        path = np.array(path)
        plt.plot(path[:, 1], path[:, 0], 'b-', linewidth=2)

    if start:
        plt.plot(start[1], start[0], 'go', markersize=8)

    if goal:
        plt.plot(goal[1], goal[0], 'ro', markersize=8)

    plt.gca().invert_yaxis()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
