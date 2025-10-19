# explain/strategy_explainer.py
import torch
import numpy as np

def get_top_moves(policy, state_vec, legal_moves, k=5):
    with torch.no_grad():
        logits = policy(torch.tensor(state_vec).unsqueeze(0))
        probs = torch.softmax(logits, dim=-1)[0]
    move_probs = [(i+1, probs[i].item()) for i in range(100) if (i+1) in legal_moves]
    move_probs.sort(key=lambda x: x[1], reverse=True)
    return move_probs[:k]

def explain_strategy(policy, env):
    state_vec = env.get_state_vec()
    legal = env.get_legal_moves()
    top_moves = get_top_moves(policy, state_vec, legal, 5)
    sa, sb = env.scores

    explanation = f"🔍 当前局面分析：\n"
    explanation += f"- 当前链: {env.chain}\n"
    explanation += f"- 合法动作: {sorted(legal)[:10]}...\n"
    explanation += f"- 我最可能选: {[m[0] for m in top_moves]}\n"

    if env.chain:
        last = env.chain[-1]
        divisors = [i for i in range(1,101) if i != last and (i%last==0 or last%i==0)]
        explanation += f"- 上一个数 {last} 有 {len(divisors)} 个连接点。\n"

    if sa > sb:
        explanation += "- 我领先，倾向于控制路径而非抢大数。\n"
    else:
        explanation += "- 我落后，必须冒险选大数逆转。\n"

    best_move = top_moves[0][0]
    if best_move > 50:
        explanation += f"- 推荐选 {best_move}，因为它大且能开启新分支。\n"
    elif best_move < 10:
        explanation += f"- 推荐选 {best_move}，用于封锁你的路径。\n"

    return explanation