# Neo-Grid: Multi-Agent Autonomous Logistics Optimizer

**Neo-Grid** is a premium Multi-Agent Reinforcement Learning (MARL) system that demonstrates decentralized coordination, collision avoidance, and efficiency in a high-density warehouse environment. 

### 🚀 Overview
The project tackles the complex challenge of autonomous robot coordination in dynamic grids. Using **Proximal Policy Optimization (PPO)**, multiple independent agents learn to navigate to their respective targets while avoiding collisions and minimizing path length. It serves as a comprehensive demonstration of applying modern RL techniques to real-world logistics and supply chain optimization.

### ✨ Key Features
- **MARL Architecture:** Decentralized agents learning from local and global observations.
- **Real-time Telemetry:** A high-end React dashboard for live simulation monitoring.
- **FastAPI Bridge:** High-speed WebSocket communication between the RL engine (Python) and the UI (JS).
- **Scalable Design:** Easily configurable for grid size, agent count, and obstacle density.
- `logic/`: Custom Gymnasium environment and RL agent logic.
- `simulation/`: Performance evaluation and comparison scripts.
- `dashboard/`: A high-end React-based visualization interface.
- `models/`: Saved training weights and checkpoints.
- `archive/`: Old or experimental code.

## 🚀 Getting Started
1. Install dependencies: `pip install -r requirements.txt`
2. Train the agents: `python logic/train.py`
3. Launch the dashboard: `cd dashboard && npm run dev`
4. Run the API bridge: `python logic/api.py`

## 🧠 Core RL Architecture
- **Environment:** Custom `WarehouseEnv` (OpenAI Gymnasium API).
- **Algorithm:** PPO (Proximal Policy Optimization) for decentralized-centralized coordination.
- **Reward Shaping:** Weighted sum of distance-to-goal, collision penalties, and time-efficiency bonuses.

---
*Created by AI for an impressive RL project submission.*
