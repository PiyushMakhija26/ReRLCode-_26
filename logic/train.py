import os
import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.monitor import Monitor
from warehouse_env import WarehouseEnv

def train():
    # 1. Initialize environment
    grid_size = 8
    num_agents = 2
    env = WarehouseEnv(grid_size=grid_size, num_agents=num_agents)
    
    # 2. Check environment (SB3 requirement)
    # check_env(env) # Ensure it follows Gymnasium API

    # 3. Path setup
    model_path = os.path.join("models", "ppo_warehouse")
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    os.makedirs("models", exist_ok=True)

    # Wrap for logging
    env = Monitor(env, log_dir)

    # 4. Initialize Model
    # Policy: MultiInputPolicy (if obs is dict) or MlpPolicy (if box)
    model = PPO("MlpPolicy", env, verbose=1, 
                learning_rate=3e-4, 
                n_steps=2048, 
                batch_size=64, 
                n_epochs=10, 
                gamma=0.99,
                device="auto")

    # 5. Train
    print(f"Starting training on {grid_size}x{grid_size} grid with {num_agents} agents...")
    model.learn(total_timesteps=100000, progress_bar=True)

    # 6. Save
    model.save(model_path)
    print(f"Training complete. Model saved to {model_path}")

    # 7. Evaluate (Optional quick run)
    obs, info = env.reset()
    for _ in range(50):
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        if terminated or truncated:
            break
    print("Example evaluation run finished.")

if __name__ == "__main__":
    train()
