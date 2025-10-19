# analysis/discover_strategy.py
import json
from collections import Counter

# === 1. 读取日志 ===
games = []
with open("../data_output/game_logs.jsonl", "r") as f:
    for line in f:
        games.append(json.loads(line))

print(f"共分析 {len(games)} 局游戏\n")

# === 2. 分析 Alice 赢的开局 X1 ===
winning_x1 = [g["alice_first"] for g in games if g["winner"] == "Alice" and g["alice_first"] is not None]
x1_counter = Counter(winning_x1)
print("🏆 Alice 赢的开局 X1（前10名）：")
for x1, count in x1_counter.most_common(10):
    print(f"  {x1}: {count} 次")

# === 3. 分析链长 vs 胜负 ===
long_games = [g for g in games if g["length"] > 5]
short_games = [g for g in games if g["length"] <= 5]

alice_win_rate_long = sum(1 for g in long_games if g["winner"] == "Alice") / len(long_games)
alice_win_rate_short = sum(1 for g in short_games if g["winner"] == "Alice") / len(short_games)

print(f"\n📈 长链游戏（>5步）中 Alice 胜率: {alice_win_rate_long:.1%}")
print(f"📈 短链游戏（≤5步）中 Alice 胜率: {alice_win_rate_short:.1%}")

# === 4. 分析平均得分 ===
alice_scores = [g["scores"][0] for g in games]
bob_scores = [g["scores"][1] for g in games]
print(f"\n📊 平均得分: Alice={sum(alice_scores)/len(alice_scores):.1f}, Bob={sum(bob_scores)/len(bob_scores):.1f}")