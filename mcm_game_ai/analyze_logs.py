# analyze_logs.py

import json
import os

log_path = "E:/mcm_training_data/game_logs.jsonl"

def load_logs():
    logs = []
    with open(log_path, 'r') as f:
        for line in f:
            if line.strip():
                logs.append(json.loads(line))
    return logs

def analyze_performance():
    logs = load_logs()
    if not logs:
        print("❌ 日志为空！")
        return

    # 提取数据
    alice_scores = [log['alice_score'] for log in logs]
    bob_scores = [log['bob_score'] for log in logs]
    total_scores = [log['total_score'] for log in logs]
    lengths = [log['length'] for log in logs]
    winners = [log['winner'] for log in logs]

    # 统计
    num_games = len(logs)
    alice_wins = winners.count("Alice")
    bob_wins = winners.count("Bob")
    avg_alice = sum(alice_scores) / num_games
    avg_bob = sum(bob_scores) / num_games
    avg_total = sum(total_scores) / num_games
    max_total = max(total_scores)
    max_length = max(lengths)

    # 找出最高分那一局
    best_game = max(logs, key=lambda x: x['total_score'])

    # 输出报告
    print("\n" + "="*50)
    print("🎮 AI 模型性能评估报告")
    print("="*50)
    print(f"📊 总对局数: {num_games}")
    print(f"🏆 Alice 胜率: {alice_wins/num_games:.1%} ({alice_wins} 胜)")
    print(f"🏆 Bob 胜率: {bob_wins/num_games:.1%} ({bob_wins} 胜)")
    print(f"📈 Alice 平均得分: {avg_alice:.1f}")
    print(f"📈 Bob 平均得分: {avg_bob:.1f}")
    print(f"🔥 平均总分: {avg_total:.1f}")
    print(f"🎯 最高总分: {max_total}")
    print(f"🔗 最长链长度: {max_length}")
    print("="*50)
    print("🏆 最强一局:")
    print(f"   Chain: {best_game['chain']}")
    print(f"   Scores: Alice={best_game['alice_score']}, Bob={best_game['bob_score']}")
    print(f"   Total: {best_game['total_score']}")
    print(f"   Length: {best_game['length']}")
    print("="*50)

if __name__ == "__main__":
    analyze_performance()