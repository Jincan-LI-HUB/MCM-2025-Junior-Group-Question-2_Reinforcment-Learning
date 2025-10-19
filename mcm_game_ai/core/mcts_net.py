# mcts_net.py
import math
import numpy as np
from core.game import GameEnv
import torch

# 可以将 GNN 的输出作为先验概率的初始化
from gnn_model import DivisibilityGNN, build_divisibility_graph

gnn = DivisibilityGNN()
gnn.load_state_dict(torch.load("gnn.pth"))  # 假设已训练
graph_data = build_divisibility_graph()
with torch.no_grad():
    gnn_prior = torch.softmax(gnn(graph_data)[0], dim=-1).numpy()
# 然后在 MCTS 中加权融合 gnn_prior 和 policy_prior

# MCTS 节点
class MCTSNode:
    def __init__(self, state: GameEnv, parent=None, prior=0.):
        self.state = state
        self.parent = parent
        self.children = {}
        self.visit_count = 0
        self.value_sum = 0.
        self.prior = prior

    def value(self):
        if self.visit_count == 0:
            return 0
        return self.value_sum / self.visit_count

    def ucb_score(self, parent, cpuct=1.0):
        if self.visit_count == 0:
            return float('inf')
        exploration = math.sqrt(parent.visit_count) / (1 + self.visit_count)
        return self.value() + cpuct * self.prior * exploration

def mcts_search_with_net(state: GameEnv, alice_policy, bob_policy, num_simulations=800):
    """
    使用神经网络作为先验的 MCTS 搜索
    支持 Alice 和 Bob 轮流使用各自的策略网络
    """
    root = MCTSNode(state)

    for _ in range(num_simulations):
        node = root
        search_path = [node]

        # Selection
        while node.children:
            children = node.children.values()
            node = max(children, key=lambda x: x.ucb_score(node))
            search_path.append(node)

        # Expansion
        if not node.state.is_terminal():
            # 获取当前玩家的策略网络
            policy_net = alice_policy if node.state.player == 0 else bob_policy
            state_vec = torch.tensor(node.state.get_state_vec(), dtype=torch.float32).unsqueeze(0)
            with torch.no_grad():
                logits = policy_net(state_vec)[0]
                probs = torch.softmax(logits, dim=-1)[0].numpy()

            legal_moves = node.state.get_legal_moves()
            masked_probs = np.array([probs[m-1] if m in legal_moves else 0 for m in range(1,101)])
            if masked_probs.sum() > 0:
                masked_probs /= masked_probs.sum()
            else:
                # fallback
                masked_probs = np.array([1 if m in legal_moves else 0 for m in range(1,101)])
                masked_probs /= masked_probs.sum()

            for action in legal_moves:
                child_state = node.state.make_move(action)
                prior = masked_probs[action-1]
                node.children[action] = MCTSNode(child_state, parent=node, prior=prior)

        # Simulation & Backpropagation
        if node.state.is_terminal():
            sa, sb, winner = node.state.get_result()
            value = 1.0 if winner == "Alice" else -1.0 if winner == "Bob" else 0.0
        else:
            value = 0  # 不使用 rollout，依赖网络

        for node in search_path:
            node.visit_count += 1
            # Alice 的视角：赢 +1，输 -1
            v = value if node.state.player == 0 else -value
            node.value_sum += v

    # 返回访问次数最多的动作
    best_action = max(root.children.items(), key=lambda x: x[1].visit_count)[0]
    return best_action