# config.py

# 游戏设置
NUM_PLAYERS = 2
MIN_NUM = 1
MAX_NUM = 100

# 训练设置
TRAIN_EPISODES = 5000
BATCH_SIZE = 64
LR = 3e-4
GAMMA = 0.99
ALPHA = 1.0      # score coefficient
BETA = 100.0     # win bonus coefficient

# MCTS 设置
MCTS_SIMULATIONS = 800
MCTS_CPUCT = 1.0

# 模型设置
POLICY_HIDDEN_SIZE = 128
GNR_HIDDEN_DIM = 64

# 路径设置
DATA_DIR = "data_output"
LOG_DIR = "logs"
MODEL_ALICE = f"{DATA_DIR}/alice_policy.pth"
MODEL_BOB = f"{DATA_DIR}/bob_policy.pth"

# 探索设置
EPSILON_START = 0.3
EPSILON_END = 0.05
EPSILON_DECAY = 0.995

# 评估设置
EVAL_EVERY = 500
NUM_EVALUATIONS = 10