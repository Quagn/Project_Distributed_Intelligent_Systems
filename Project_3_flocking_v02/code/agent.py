import numpy as np

class Agent:
    def __init__(self, env, max_speed=2.0, radius=10):
        self.env = env
        self.position = np.random.rand(2) * env.size
        angle = np.random.rand() * 2 * np.pi
        self.velocity = max_speed * np.array([np.cos(angle), np.sin(angle)])
        self.max_speed = max_speed
        self.radius = radius

    def limit_velocity(self):
        speed = np.linalg.norm(self.velocity)
        if speed > self.max_speed:
            self.velocity = (self.velocity / speed) * self.max_speed

    def update(self, agents, env, goal=None):
        sep = self.separation(agents)
        ali = self.alignment(agents)
        coh = self.cohesion(agents)
        obs = self.avoid_obstacles(env) if env.obstacle else np.zeros(2)

        self.velocity += 1.5 * sep + 1.0 * ali + 1.0 * coh + 2.0 * obs

        if goal is not None:
            goal_force = (goal - self.position) * 0.002
            self.velocity += goal_force

        self.limit_velocity()
        self.position += self.velocity
        self.position = np.clip(self.position, 0, env.size)

        center_force = (env.size / 2 - self.position) * 0.001
        self.velocity += center_force

        if env.obstacle:
            for obs in env.obstacles:
                diff = self.position - obs['center']
                dist = np.linalg.norm(diff)
                min_dist = obs['radius'] + 1.0  # khoảng cách an toàn

                if dist < min_dist:
                    correction = (diff / dist) * (min_dist - dist)
                    self.position += correction



    def get_neighbors(self, agents):
        return [a for a in agents if a is not self and np.linalg.norm(self.position - a.position) < self.radius]

    def separation(self, agents):
        steer = np.zeros(2)
        neighbors = self.get_neighbors(agents)
        for other in neighbors:
            diff = self.position - other.position
            dist = np.linalg.norm(diff)
            if dist > 0:
                steer += diff / dist**2
        return steer

    def alignment(self, agents):
        neighbors = self.get_neighbors(agents)
        if not neighbors:
            return np.zeros(2)
        avg_velocity = np.mean([a.velocity for a in neighbors], axis=0)
        return (avg_velocity - self.velocity) * 0.05

    def cohesion(self, agents):
        neighbors = self.get_neighbors(agents)
        if not neighbors:
            return np.zeros(2)
        center_of_mass = np.mean([a.position for a in neighbors], axis=0)
        return (center_of_mass - self.position) * 0.01

    def avoid_obstacles(self, env):
        steer = np.zeros(2)
        for obs in env.obstacles:
            diff = self.position - obs['center']
            dist = np.linalg.norm(diff)
            if dist < obs['radius'] + 5:
                steer += diff / (dist**2 + 1e-5)
        return steer
