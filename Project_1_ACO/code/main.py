import time
import csv
from maps.grid_map import create_grid_map
from algorithms.ant_colony import AntColony
from algorithms.astar import astar
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from utils.highlight_best import visualize_best_paths  #  hàm hiển thị overlay
from utils.visualization import visualize  # (nếu muốn xem từng trial)
import warnings
warnings.filterwarnings("ignore")

# ===== CẤU HÌNH =====
TRIALS = 30
MAP_SIZE = (30, 30)
OBSTACLE_RATIO = 0.2

# ===== HÀM PHỤ TRỢ =====
def compute_path_length(path):
    if not path:
        return float('inf')
    return len(path) - 1

def save_summary_to_csv(summary, filename="summary.csv"):
    fieldnames = ["Algorithm", "Success Rate (%)", "Avg Path Length", "Avg Time (s)"]
    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for res in summary:
            writer.writerow(res)

def save_detailed_trials(trials, filename="detailed_trials.csv"):
    fieldnames = ["Trial", "Algorithm", "Success", "Path Length", "Time (s)"]
    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in trials:
            writer.writerow(row)

# ===== DANH SÁCH THUẬT TOÁN =====
algorithms = {
    "ACO": lambda grid, s, g: AntColony(grid, s, g, n_ants=50, iterations=50).run(),
    "A*": astar,
    "BFS": bfs,
    "DFS": dfs,
}

# ===== KHỞI TẠO BẢN ĐỒ MỘT LẦN =====
grid = create_grid_map(size=MAP_SIZE, obstacle_ratio=OBSTACLE_RATIO)
start, goal = (0, 0), (MAP_SIZE[0] - 1, MAP_SIZE[1] - 1)

# ===== BIẾN THỐNG KÊ =====
stats = {alg: {"success": 0, "total_length": 0, "total_time": 0.0} for alg in algorithms}
trial_log = []
all_paths = {alg: [] for alg in algorithms}

# ===== CHẠY THỬ NGHIỆM =====
for trial in range(TRIALS):
    print(f"\n--- Trial {trial + 1}/{TRIALS} ---")

    for name, func in algorithms.items():
        start_time = time.time()
        try:
            path = func(grid, start, goal)
        except:
            path = None
        elapsed = time.time() - start_time

        success = path is not None
        length = compute_path_length(path) if success else 0

        stats[name]["success"] += int(success)
        stats[name]["total_length"] += length
        stats[name]["total_time"] += elapsed
        all_paths[name].append(path)

        trial_log.append({
            "Trial": trial + 1,
            "Algorithm": name,
            "Success": "Yes" if success else "No",
            "Path Length": length,
            "Time (s)": round(elapsed, 4)
        })

        print(f"{name}: {'OK' if success else 'FAIL'} | Length: {length} | Time: {elapsed:.4f}s")

# ===== HIỂN THỊ TỔNG HỢP ĐƯỜNG ĐI =====
for name in algorithms:
    paths = [p for p in all_paths[name] if p]
    if not paths:
        print(f"{name}: No path found.")
        continue
    best_path = min(paths, key=lambda p: len(p))
    visualize_best_paths(grid, paths, best_path, start, goal, algorithm_name=name)

# ===== GHI FILE CSV =====
summary = []
for name, data in stats.items():
    success_rate = 100.0 * data["success"] / TRIALS
    avg_length = round(data["total_length"] / data["success"], 2) if data["success"] else "-"
    avg_time = round(data["total_time"] / TRIALS, 4)
    summary.append({
        "Algorithm": name,
        "Success Rate (%)": round(success_rate, 2),
        "Avg Path Length": avg_length,
        "Avg Time (s)": avg_time
    })

save_summary_to_csv(summary)
save_detailed_trials(trial_log)
print("\n Save 'summary.csv' & 'detailed_trials.csv'")
