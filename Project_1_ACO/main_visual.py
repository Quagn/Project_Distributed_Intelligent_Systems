import time
import csv
from maps.grid_map import create_grid_map
from algorithms.ant_colony import AntColony
from algorithms.astar import astar
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from utils.visualization import visualize

# === HÀM PHỤ TRỢ ===

def compute_path_length(path):
    if not path:
        return float('inf')
    return len(path) - 1

def save_results_to_csv(results, filename="results.csv"):
    fieldnames = ["Algorithm", "Success", "Path Length", "Time (s)"]
    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for res in results:
            writer.writerow(res)

# === TẠO BẢN ĐỒ ===

grid = create_grid_map(size=(10, 10), obstacle_ratio=0.2)
start, goal = (0, 0), (9, 9)

results = []

# === ACO ===
start_time = time.time()
aco = AntColony(grid, start, goal, n_ants=50, iterations=50)
path_aco = aco.run()
time_aco = time.time() - start_time
results.append({
    "Algorithm": "ACO",
    "Success": path_aco is not None,
    "Path Length": compute_path_length(path_aco),
    "Time (s)": round(time_aco, 4)
})
visualize(grid, path_aco, start, goal, "ACO Path")

# === A* ===
start_time = time.time()
path_astar = astar(grid, start, goal)
time_astar = time.time() - start_time
results.append({
    "Algorithm": "A*",
    "Success": path_astar is not None,
    "Path Length": compute_path_length(path_astar),
    "Time (s)": round(time_astar, 4)
})
visualize(grid, path_astar, start, goal, "A* Path")

# === BFS ===
start_time = time.time()
path_bfs = bfs(grid, start, goal)
time_bfs = time.time() - start_time
results.append({
    "Algorithm": "BFS",
    "Success": path_bfs is not None,
    "Path Length": compute_path_length(path_bfs),
    "Time (s)": round(time_bfs, 4)
})
visualize(grid, path_bfs, start, goal, "BFS Path")

# === DFS ===
start_time = time.time()
path_dfs = dfs(grid, start, goal)
time_dfs = time.time() - start_time
results.append({
    "Algorithm": "DFS",
    "Success": path_dfs is not None,
    "Path Length": compute_path_length(path_dfs),
    "Time (s)": round(time_dfs, 4)
})
visualize(grid, path_dfs, start, goal, "DFS Path")

# === GHI KẾT QUẢ RA FILE CSV ===
save_results_to_csv(results)
print("Save results.csv.")

