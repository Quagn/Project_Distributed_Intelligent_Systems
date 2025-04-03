import matplotlib.pyplot as plt
import numpy as np

def visualize_overlay(grid, paths_dict, start=None, goal=None, trial_num=1):
    plt.figure(figsize=(6, 6))
    plt.imshow(grid, cmap='gray_r')

    # Vẽ đường đi cho từng thuật toán
    for name, path in paths_dict.items():
        if path:
            path = np.array(path)
            plt.plot(path[:, 1], path[:, 0], label=name, linewidth=2)

    # Vẽ điểm bắt đầu và kết thúc
    if start:
        plt.plot(start[1], start[0], 'go', markersize=8, label="Start")
    if goal:
        plt.plot(goal[1], goal[0], 'ro', markersize=8, label="Goal")

    plt.title(f"Trial {trial_num} - All Algorithms")
    plt.legend()
    plt.gca().invert_yaxis()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
