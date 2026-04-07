import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pygame
import random

class WarehouseEnv(gym.Env):
    """
    Custom Multi-Agent Warehouse Environment for Reinforcement Learning.
    Each agent must navigate to its target while avoiding others.
    """
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 10}

    def __init__(self, grid_size=10, num_agents=2, render_mode=None):
        super(WarehouseEnv, self).__init__()
        
        self.grid_size = grid_size
        self.num_agents = num_agents
        self.render_mode = render_mode
        self.max_steps = 200
        self.current_step = 0

        # Actions: 0: Up, 1: Down, 2: Left, 3: Right, 4: Wait (per agent)
        self.action_space = spaces.MultiDiscrete([5] * num_agents)
        
        # State: Agent [x, y] positions + Target [x, y] positions (all agents)
        # Total state size: (num_agents * 2) + (num_agents * 2) = num_agents * 4
        self.observation_space = spaces.Box(
            low=0, high=grid_size-1, shape=(num_agents * 4,), dtype=np.float32
        )

        # Pygame for rendering
        self.window = None
        self.clock = None
        self.cell_size = 50

    def _get_obs(self):
        obs = []
        for a in self.agents:
            obs.extend(a)
        for t in self.targets:
            obs.extend(t)
        return np.array(obs, dtype=np.float32)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.current_step = 0
        self.target_reached = [False] * self.num_agents
        
        occupied = set()
        # Initial positions
        self.agents = []
        while len(self.agents) < self.num_agents:
            pos = [random.randint(0, self.grid_size-1), random.randint(0, self.grid_size-1)]
            if tuple(pos) not in occupied:
                self.agents.append(pos)
                occupied.add(tuple(pos))
        
        # Target positions
        self.targets = []
        while len(self.targets) < self.num_agents:
            pos = [random.randint(0, self.grid_size-1), random.randint(0, self.grid_size-1)]
            if tuple(pos) not in occupied:
                self.targets.append(pos)
                occupied.add(tuple(pos))

        if self.render_mode == "human":
            self._render_frame()

        return self._get_obs(), {}

    def step(self, actions):
        self.current_step += 1
        rewards = 0
        terminated = False
        
        # 1. Update Positions
        new_positions = []
        for i, (agent, action) in enumerate(zip(self.agents, actions)):
            if self.target_reached[i]: 
                new_positions.append(agent)
                continue # Agent is done

            nx, ny = agent[0], agent[1]
            if action == 0: nx -= 1 # Up (assuming grid row coordinate)
            elif action == 1: nx += 1 # Down
            elif action == 2: ny -= 1 # Left
            elif action == 3: ny += 1 # Right

            # Bound checking
            nx = np.clip(nx, 0, self.grid_size-1)
            ny = np.clip(ny, 0, self.grid_size-1)
            new_positions.append([nx, ny])

        # 2. Collision Detection & Reward Calculation
        # Simple rule: If collision, penalize and don't move
        real_positions = []
        for i, pos in enumerate(new_positions):
            if self.target_reached[i]:
                real_positions.append(pos)
                continue

            # Collision with other agents
            collision = any(p == pos for j, p in enumerate(new_positions) if i != j)
            if collision:
                rewards -= 5 # Collision penalty
                real_positions.append(self.agents[i]) # Stay put
            else:
                real_positions.append(pos)
                
            # Success check (reached target)
            dist_to_target = abs(real_positions[i][0] - self.targets[i][0]) + abs(real_positions[i][1] - self.targets[i][1])
            if dist_to_target == 0:
                rewards += 20 # Success reward
                self.target_reached[i] = True
            else:
                # Potential shaping (moving closer)
                old_dist = abs(self.agents[i][0] - self.targets[i][0]) + abs(self.agents[i][1] - self.targets[i][1])
                rewards += (old_dist - dist_to_target) * 0.5 # Small incentive
                rewards -= 0.1 # Time step penalty

        self.agents = real_positions
        
        # Terminate if all agents reached goal or max steps reached
        terminated = all(self.target_reached)
        truncated = self.current_step >= self.max_steps
        
        if self.render_mode == "human":
            self._render_frame()

        return self._get_obs(), rewards, terminated, truncated, {}

    def render(self):
        if self.render_mode == "rgb_array":
            return self._render_frame()

    def _render_frame(self):
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode((self.grid_size * self.cell_size, self.grid_size * self.cell_size))
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

        canvas = pygame.Surface((self.grid_size * self.cell_size, self.grid_size * self.cell_size))
        canvas.fill((20, 20, 30)) # Dark background

        # Draw Grid
        for x in range(self.grid_size + 1):
            pygame.draw.line(canvas, (40, 40, 50), (0, x * self.cell_size), (self.grid_size * self.cell_size, x * self.cell_size))
            pygame.draw.line(canvas, (40, 40, 50), (x * self.cell_size, 0), (x * self.cell_size, self.grid_size * self.cell_size))

        # Draw Targets (Package spots)
        for i, t in enumerate(self.targets):
            color = (0, 255, 127) if self.target_reached[i] else (0, 200, 255)
            pygame.draw.rect(canvas, color, (t[1] * self.cell_size + 10, t[0] * self.cell_size + 10, self.cell_size - 20, self.cell_size - 20), 3)

        # Draw Agents
        for i, a in enumerate(self.agents):
            color = (0, 255, 0) if self.target_reached[i] else (255, 50, 50)
            pygame.draw.circle(canvas, color, (a[1] * self.cell_size + self.cell_size // 2, a[0] * self.cell_size + self.cell_size // 2), self.cell_size // 3)

        if self.render_mode == "human":
            self.window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()
            self.clock.tick(self.metadata["render_fps"])
        else: # rgb_array
            return np.transpose(np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2))

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
