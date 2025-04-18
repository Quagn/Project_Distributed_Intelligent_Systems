import numpy as np

class AntColony:
    def __init__(self, grid, start, goal, n_ants=20, alpha=1, beta=2, rho=0.5, iterations=30):
        self.grid = grid
        self.start = start
        self.goal = goal
        self.n_ants = n_ants
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.iterations = iterations
        self.pheromone = np.ones(grid.shape)

    # Đã thêm kiểm tra tránh chia cho 0
    def heuristic(self, node):
        dist = np.linalg.norm(np.array(node) - np.array(self.goal))
        return dist if dist != 0 else 1e-6

    def neighbors(self, node):
        moves = [(0,1), (1,0), (0,-1), (-1,0)]
        valid = []
        for dx, dy in moves:
            next_node = (node[0] + dx, node[1] + dy)
            if 0 <= next_node[0] < self.grid.shape[0] and 0 <= next_node[1] < self.grid.shape[1]:
                if self.grid[next_node] == 0:
                    valid.append(next_node)
        return valid

    def run(self):
        best_path, best_length = None, np.inf

        for _ in range(self.iterations):
            paths, lengths = [], []

            for _ in range(self.n_ants):
                path, current = [self.start], self.start
                visited = set([current])

                while current != self.goal:
                    moves = [n for n in self.neighbors(current) if n not in visited]
                    if not moves:
                        break
                    probs = np.array([
                        (self.pheromone[m] ** self.alpha) * ((1.0 / self.heuristic(m)) ** self.beta)
                        for m in moves
                    ])
                    # Kiểm tra tổng probs để tránh chia cho 0
                    total_probs = probs.sum()
                    if total_probs == 0 or np.isnan(total_probs):
                        probs = np.ones(len(moves)) / len(moves)
                    else:
                        probs /= total_probs

                    current = moves[np.random.choice(len(moves), p=probs)]
                    path.append(current)
                    visited.add(current)

                if current == self.goal:
                    paths.append(path)
                    lengths.append(len(path))

            self.pheromone *= (1 - self.rho)

            for path, length in zip(paths, lengths):
                for node in path:
                    self.pheromone[node] += 1.0 / length

            if lengths and min(lengths) < best_length:
                best_length = min(lengths)
                best_path = paths[lengths.index(best_length)]

        return best_path
