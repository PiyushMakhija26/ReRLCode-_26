# Neo-Grid: Multi-Agent Autonomous Logistics Optimizer

A premium Reinforcement Learning project that demonstrates multi-agent coordination, collision avoidance, and efficiency in a warehouse environment.

## 📁 Project Structure
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
