# agents/train_marl.py

import os
import sys
import json

# === 1. 添加项目根目录到 Python 路径 ===
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

# === 2. 创建 data_output 目录（必须放前面！）===
output_dir = os.path.join(project_root, "data_output")
os.makedirs(output_dir, exist_ok=True)

log_path = os.path.join(output_dir, "game_logs.jsonl")

# === 3. 导入配置和环境 ===
from config import *
from core.game import GameEnv

# === 4. 导入其他依赖 ===
import torch
import torch.optim as optim
from torch.distributions import Categorical
from agents.policy_net import SimplePolicy
import numpy as np


# === 新增：判断质数（用于奖励大质数）===
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


# === 新增：计算带折扣的回报（Return）===
def compute_returns(rewards, gamma=0.99):
    R = 0
    returns = []
    for r in reversed(rewards):
        R = r + gamma * R
        returns.insert(0, R)
    return returns


# === 5. 初始化策略网络和优化器，并尝试加载已有模型 ===
alice_policy = SimplePolicy()
bob_policy = SimplePolicy()

# 模型保存路径
alice_path = os.path.join(output_dir, "alice_policy.pth")
bob_path = os.path.join(output_dir, "bob_policy.pth")

# 尝试加载已有模型
if os.path.exists(alice_path):
    print(f"🔁 Loading Alice's policy from {alice_path}")
    alice_policy.load_state_dict(torch.load(alice_path, map_location='cpu'))
else:
    print("🆕 Initializing Alice's policy from scratch")

if os.path.exists(bob_path):
    print(f"🔁 Loading Bob's policy from {bob_path}")
    bob_policy.load_state_dict(torch.load(bob_path, map_location='cpu'))
else:
    print("🆕 Initializing Bob's policy from scratch")

# 定义优化器
alice_opt = optim.Adam(alice_policy.parameters(), lr=3e-4)
bob_opt = optim.Adam(bob_policy.parameters(), lr=3e-4)


# === 6. 动作选择函数 ===
def select_action(policy, state, legal_moves):
    state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
    logits = policy(state_tensor)
    mask = torch.tensor([0 if (i + 1) in legal_moves else -1e9 for i in range(100)], dtype=torch.float32)
    logits += mask
    dist = Categorical(logits=logits)
    action_idx = dist.sample()
    return action_idx.item() + 1, dist.log_prob(action_idx)


# === 7. 训练主循环 ===
for episode in range(5000):
    env = GameEnv()
    log_probs_a, rewards_a = [], []
    log_probs_b, rewards_b = [], []

    while not env.done:
        state = env.get_state_vec()
        legal = env.get_legal_moves()

        if env.player == 0:  # Alice
            action, lp = select_action(alice_policy, state, legal)
            log_probs_a.append(lp)

            # ✅ 战略性奖励：大质数 + 高次幂
            control_bonus = 0.0
            if is_prime(action) and action > 50:  # 大质数，如 97, 89
                control_bonus = 1.5
            elif action in [64, 32, 16, 8, 4, 2]:  # 2 的高次幂，可开启长链
                control_bonus = 1.0

            step_reward = action + control_bonus
            rewards_a.append(step_reward)

        else:  # Bob
            action, lp = select_action(bob_policy, state, legal)
            log_probs_b.append(lp)

            # Bob 同样奖励控制权
            control_bonus = 1.5 if (is_prime(action) and action > 50) else 0.0
            step_reward = action + control_bonus
            rewards_b.append(step_reward)

        env = env.make_move(action)
        if env is None:
            break

    # === 使用 Return 计算损失（鼓励长期策略）===
    returns_a = compute_returns(rewards_a)
    returns_b = compute_returns(rewards_b)

    loss_a = -sum(lp * ret for lp, ret in zip(log_probs_a, returns_a))
    loss_b = -sum(lp * ret for lp, ret in zip(log_probs_b, returns_b))

    alice_opt.zero_grad()
    loss_a.backward()
    alice_opt.step()

    bob_opt.zero_grad()
    loss_b.backward()
    bob_opt.step()

    # ✅ 每一局结束后记录
    game_log = {
        "episode": episode,
        "chain": env.chain.copy(),
        "scores": env.scores.copy(),
        "winner": "Alice" if env.scores[0] > env.scores[1] else "Bob",
        "alice_first": env.chain[0] if len(env.chain) > 0 else None,
        "length": len(env.chain)
    }

    with open(log_path, "a") as f:
        f.write(json.dumps(game_log) + "\n")

    if episode % 500 == 0:
        sa, sb, _ = env.get_result()
        print(f"Episode {episode} | Alice: {sa}, Bob: {sb} | Winner: {env.get_result()[2]}")


# === 8. 保存模型（覆盖旧模型）===
torch.save(alice_policy.state_dict(), alice_path)
torch.save(bob_policy.state_dict(), bob_path)

print(f"\n✅ 模型已成功保存至：")
print(f"   {alice_path}")
print(f"   {bob_path}")
print(f"✅ 对弈日志已保存至：{log_path}")