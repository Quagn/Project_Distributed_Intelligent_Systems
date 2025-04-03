import pandas as pd
import matplotlib.pyplot as plt

# Đọc file chi tiết từng lần chạy
df = pd.read_csv("detailed_trials.csv")

# Chuyển Success thành số (Yes=1, No=0)
df["Success (num)"] = df["Success"].apply(lambda x: 1 if x.strip().lower() == "yes" else 0)

# Lấy danh sách thuật toán
algorithms = df["Algorithm"].unique()
trials = sorted(df["Trial"].unique())

# Thiết lập biểu đồ
fig, axs = plt.subplots(3, 1, figsize=(12, 12), sharex=True)
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red']

# === 1. Độ dài đường đi theo trial ===
for i, alg in enumerate(algorithms):
    data = df[df["Algorithm"] == alg]
    axs[0].plot(data["Trial"], data["Path Length"], label=alg, marker='o', color=colors[i])
axs[0].set_title("Path Length per Trial")
axs[0].set_ylabel("Path Length")
axs[0].grid(True)
axs[0].legend()

# === 2. Thời gian chạy theo trial ===
for i, alg in enumerate(algorithms):
    data = df[df["Algorithm"] == alg]
    axs[1].plot(data["Trial"], data["Time (s)"], label=alg, marker='o', color=colors[i])
axs[1].set_title("Execution Time per Trial")
axs[1].set_ylabel("Time (s)")
axs[1].grid(True)

# === 3. Success theo trial ===
for i, alg in enumerate(algorithms):
    data = df[df["Algorithm"] == alg]
    axs[2].plot(data["Trial"], data["Success (num)"], label=alg, marker='o', color=colors[i])
axs[2].set_title("Success per Trial (1 = success)")
axs[2].set_ylabel("Success")
axs[2].set_xlabel("Trial")
axs[2].set_yticks([0, 1])
axs[2].grid(True)

plt.suptitle("Biểu đồ thống kê theo từng lần thử nghiệm", fontsize=16)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
