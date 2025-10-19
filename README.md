# MCM-2025-Junior-Group-Question-2_Reinforcment-Learning
##1.this file are structured as below:
mcm_game_ai/

├── core/

│   ├── __init__.py

│   ├── game.py

│   ├── mcts_net.py

│   └── gnn_model.py

├── agents/

│   ├── __init__.py

│   ├── policy_net.py

│   └── train_marl.py

├── explain/

│   ├── __init__.py

│   └── strategy_explainer.py

├── web/

│   └── app.py

├── data_output/

│   ├── alice_policy.pth

│   ├── bob_policy.pth

│   ├── game_logs.jsonl

│   └── test.txt

├── analysis/

│   ├── question_q2

│   └── discover_strategy.py

├── config.py

├── analyze_logs.py

├── forevr_train.py

└── README.md

##2.Here is a brief description of the main scripts in the repository:


train_marl.py
**Multi-Agent Reinforcement Learning Trainer**

Trains Alice and Bob (two neural agents) through self-play in the competitive 1-100 number chain game. Uses policy gradient with strategic reward shaping (win bonus, prime control, chain length). Implements adaptive opponent evolution: every 1000 episodes, Bob inherits Alice's policy with noise to become a stronger challenger.

Key features: Action masking for valid moves, MLP policy network, Adam optimizer.


analysis/answer_q2.py
**Strategy Analysis & Performance Evaluation**

Analyzes trained policies and extracts key insights for Question 2. Computes Alice's win rate, average scores, chain lengths, and identifies high-frequency optimal opening moves (e.g., 64, 97). Generates statistical summaries used in the final report.

Ideal for generating data to support claims about strategic behavior.


forever_train.py
**Long-Term Policy Evolution & Robustness Training**

Extends training over many iterations with periodic evaluation and policy saving. Designed for long-horizon refinement and stability testing. Logs performance every 500 episodes and saves best models, enabling analysis of learning progression and strategy convergence.

**Tip:** Run train_marl.py first to get initial policies, then use answer_q2.py for analysis. Use forever_train.py for extended training and robustness validation.


##3. 🚀 How to Run This Project

This guide walks you through setting up the environment and running the key scripts. All code is written in Python.

---

### 1. 🛠️ Prerequisites

- **Python 3.8 or higher**
- (Optional) **CUDA-enabled GPU** for faster training (but CPU is supported)

---

### 2. 📦 Install Dependencies

#### clone the repo
```bash
git clone https://github.com/Jincan_LI_HUB/mcm-game-ai.git
cd mcm-game-ai
