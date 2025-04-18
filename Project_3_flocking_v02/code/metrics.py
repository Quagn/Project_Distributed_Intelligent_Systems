import numpy as np

def compute_order(agents):
    headings = np.array([a.velocity / np.linalg.norm(a.velocity) for a in agents])
    avg_heading = np.linalg.norm(np.mean(headings, axis=0))
    return avg_heading


def compute_entropy(agents, grid_size, bin_size=10):
    bins = int(grid_size / bin_size)
    heatmap = np.zeros((bins, bins))
    for a in agents:
        x_bin = int(a.position[0] / bin_size)
        y_bin = int(a.position[1] / bin_size)
        x_bin = min(max(x_bin, 0), bins - 1)
        y_bin = min(max(y_bin, 0), bins - 1)
        heatmap[x_bin, y_bin] += 1
    probs = heatmap.flatten() / np.sum(heatmap)
    probs = probs[probs > 0]
    entropy = -np.sum(probs * np.log(probs))
    return entropy
