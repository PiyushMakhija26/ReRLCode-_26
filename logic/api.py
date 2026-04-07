import sys
import os
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
import numpy as np

# Add logic folder to path to import WarehouseEnv
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from warehouse_env import WarehouseEnv
from stable_baselines3 import PPO

app = FastAPI()

# Allow CORS for dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/status")
def get_status():
    return {"status": "RL API Running", "project": "Neo-Grid Logistics"}

@app.websocket("/ws/simulation")
async def websocket_simulation(websocket: WebSocket):
    print("New WebSocket client trying to connect...")
    await websocket.accept()
    print("Client connected successfully.")
    
    # Initialize simulation
    grid_size = 10
    num_agents = 3
    env = WarehouseEnv(grid_size=grid_size, num_agents=num_agents)
    
    # Load model if it exists, otherwise use random
    model_path = os.path.join("models", "ppo_warehouse.zip")
    model = None
    if os.path.exists(model_path):
        model = PPO.load(model_path)
    
    obs, _ = env.reset()
    
    try:
        while True:
            # Predict action
            if model:
                action, _ = model.predict(obs, deterministic=True)
            else:
                action = env.action_space.sample()
                
            obs, reward, terminated, truncated, info = env.step(action)
            
            # Prepare data for frontend
            data = {
                "grid_size": grid_size,
                "agents": [{"id": i, "x": a[0], "y": a[1], "reached": env.target_reached[i]} for i, a in enumerate(env.agents)],
                "targets": [{"id": i, "x": t[0], "y": t[1]} for i, t in enumerate(env.targets)],
                "reward": float(reward),
                "step": env.current_step,
                "terminated": terminated or truncated
            }
            
            await websocket.send_json(data)
            
            if terminated or truncated:
                await asyncio.sleep(2) # Show the final state for a bit
                obs, _ = env.reset()
            
            await asyncio.sleep(0.3) # Slow down for visibility
            
    except Exception as e:
        print(f"WebSocket closed: {e}")
    finally:
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7777)
