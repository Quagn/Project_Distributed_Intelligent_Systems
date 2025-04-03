import matplotlib.pyplot as plt
import numpy as np

def visualize_best_paths(grid, paths, best_path, start, goal, algorithm_name):
    plt.figure(figsize=(6, 6))
    plt.imshow(grid, cmap='gray_r')

    for path in paths:
        if path:
            path = np.array(path)
            plt.plot(path[:, 1], path[:, 0], linewidth=1, alpha=0.3, color='blue')

    if best_path:
        best_path = np.array(best_path)
        plt.plot(best_path[:, 1], best_path[:, 0], linewidth=3, color='red', label='Best Path')

    plt.plot(start[1], start[0], 'go', markersize=8, label='Start')
    plt.plot(goal[1], goal[0], 'ro', markersize=8, label='Goal')

    plt.title(f"All Trials - {algorithm_name}")
    plt.legend()
    plt.gca().invert_yaxis()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
