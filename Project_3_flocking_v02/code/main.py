import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from agent import Agent
from environment import Environment
from metrics import compute_order, compute_entropy
import os

# Cài đặt tham số
NUM_AGENTS = 20
ENV_SIZE = 180
NUM_STEPS = 2000
MODES = [False, True]  # Chạy cho cả 2 trường hợp: không vật cản và có vật cản

WAYPOINTS = [np.array([20, 20]), np.array([150, 20]), np.array([150, 150]), np.array([20, 150])]
WAYPOINT_THRESHOLD = 5  # Ngưỡng khoảng cách để chuyển waypoint

all_results = {
    "with_obstacles": {"order": [], "entropy": []},
    "no_obstacles": {"order": [], "entropy": []}
}

current_wp_idx = 0  # Toàn cục cho cả vòng lặp

for mode in MODES:
    mode_name = "with_obstacles" if mode else "no_obstacles"
    print(f"Running mode: {mode_name}")

    env = Environment(ENV_SIZE, obstacle=mode)
    agents = [Agent(env) for _ in range(NUM_AGENTS)]

    orders = []
    entropies = []

    fig, ax = plt.subplots()
    sc = ax.scatter([], [], s=30)
    wp_scatter = ax.scatter(*zip(*WAYPOINTS), c='red', marker='x')  # Hiển thị các waypoint
    txt = ax.text(0.5, 1.01, '', transform=ax.transAxes, horizontalalignment='center', fontsize=10)

    ax.set_xlim(0, ENV_SIZE)
    ax.set_ylim(0, ENV_SIZE)
    ax.set_title(f"Swarm Simulation - {mode_name}", pad=20)

    if mode:
        for obs in env.obstacles:
            circle = plt.Circle(obs['center'], obs['radius'], color='gray', alpha=0.5)
            ax.add_patch(circle)

    current_wp_idx = 0  # waypoint hiện tại

    def init():
        sc.set_offsets(np.empty((0, 2)))
        txt.set_text('')
        return sc, txt

    def update(frame):
        global current_wp_idx

        goal = WAYPOINTS[current_wp_idx]
        avg_pos = np.mean([agent.position for agent in agents], axis=0)
        if np.linalg.norm(avg_pos - goal) < WAYPOINT_THRESHOLD:
            current_wp_idx = (current_wp_idx + 1) % len(WAYPOINTS)
            goal = WAYPOINTS[current_wp_idx]

        for agent in agents:
            agent.update(agents, env, goal)

        positions = np.array([agent.position for agent in agents])
        sc.set_offsets(positions)

        order = compute_order(agents)
        entropy = compute_entropy(agents, ENV_SIZE)
        orders.append(order)
        entropies.append(entropy)

        txt.set_text(f"Step: {frame}   Order: {order:.2f}   Entropy: {entropy:.2f}")
        return sc, txt

    output_dir = f"results/{mode_name}"
    os.makedirs(output_dir, exist_ok=True)

    ani = FuncAnimation(fig, update, frames=NUM_STEPS, init_func=init, blit=True)
    ani.save(f"{output_dir}/video.mp4", writer="ffmpeg", fps=20)

    plt.figure()
    plt.plot(orders, label="Order")
    plt.title(f"Order over Time - {mode_name}")
    plt.xlabel("Step")
    plt.ylabel("Order")
    plt.savefig(f"{output_dir}/order_plot.png")

    plt.figure()
    plt.plot(entropies, label="Entropy", color="orange")
    plt.title(f"Entropy over Time - {mode_name}")
    plt.xlabel("Step")
    plt.ylabel("Entropy")
    plt.savefig(f"{output_dir}/entropy_plot.png")

    fig, ax1 = plt.subplots()
    color1 = "tab:blue"
    ax1.set_xlabel("Step")
    ax1.set_ylabel("Order", color=color1)
    ax1.plot(orders, color=color1, label="Order")
    ax1.tick_params(axis='y', labelcolor=color1)

    ax2 = ax1.twinx()
    color2 = "tab:orange"
    ax2.set_ylabel("Entropy", color=color2)
    ax2.plot(entropies, color=color2, label="Entropy")
    ax2.tick_params(axis='y', labelcolor=color2)

    fig.suptitle(f"Order & Entropy over Time (Dual Axis) - {mode_name}")
    fig.tight_layout()
    plt.savefig(f"{output_dir}/order_entropy_dual_axis.png")

    all_results[mode_name]["order"] = orders
    all_results[mode_name]["entropy"] = entropies

plt.figure()
plt.plot(all_results["no_obstacles"]["order"], label="Order - No Obstacles", linestyle="--", color="blue")
plt.plot(all_results["with_obstacles"]["order"], label="Order - With Obstacles", linestyle="-", color="blue")
plt.title("Comparison of Order")
plt.xlabel("Step")
plt.ylabel("Order")
plt.legend()
plt.savefig("results/comparison_order.png")

plt.figure()
plt.plot(all_results["no_obstacles"]["entropy"], label="Entropy - No Obstacles", linestyle="--", color="orange")
plt.plot(all_results["with_obstacles"]["entropy"], label="Entropy - With Obstacles", linestyle="-", color="orange")
plt.title("Comparison of Entropy")
plt.xlabel("Step")
plt.ylabel("Entropy")
plt.legend()
plt.savefig("results/comparison_entropy.png")

plt.close('all')
