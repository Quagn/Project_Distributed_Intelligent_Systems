import numpy as np

class Environment:
    def __init__(self, size, obstacle=False):
        self.size = size
        self.obstacle = obstacle
        self.obstacles = []
        if obstacle:
            self.generate_obstacles()

    def generate_obstacles(self):
        # Thêm một số vật cản hình tròn ngẫu nhiên
        self.obstacles.append({'center': np.array([self.size / 2, self.size / 2]), 'radius': 10})
        self.obstacles.append({'center': np.array([self.size * 0.75, self.size * 0.25]), 'radius': 7})
