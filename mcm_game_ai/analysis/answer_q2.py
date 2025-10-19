# analysis/answer_q2.py
import os
import json
from collections import Counter
from openai import OpenAI

# ==================== Configuration ====================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("""
❌ OPENAI_API_KEY is not set!

👉 Please set your API key from SiliconFlow:
1. Go to: https://cloud.siliconflow.cn
2. Create an API Key
3. Then run:
   - Windows (CMD): set OPENAI_API_KEY=sk-xxxxxxxx
   - Mac/Linux: export OPENAI_API_KEY=sk-xxxxxxxx
   - PowerShell: $env:OPENAI_API_KEY="sk-xxxxxxxx"

Then run this script again.
""")

# ✅ 使用 SiliconFlow 支持的模型
OPENAI_MODEL = "Qwen/Qwen2-7B-Instruct"
# =======================================================

def load_games():
    project_root = os.path.dirname(os.path.abspath(__file__))
    #log_path = os.path.join(project_root, "..", "data_output", "game_logs.jsonl")
    log_path = r"C:\Users\lenovo\mcm_game_ai\data_output\game_logs.jsonl"
    print("🔍 Current working directory:", os.getcwd())
    data_output_path = os.path.join(project_root, "..", "data_output")
    if os.path.exists(data_output_path):
        print("📂 Contents of data_output:", os.listdir(data_output_path))
    else:
        print("❌ data_output directory not found!")

    print(f"📊 Loading log file: {log_path}")

    if not os.path.exists(log_path):
        raise FileNotFoundError(f"❌ Log file not found: {log_path}")
    if os.path.getsize(log_path) == 0:
        raise ValueError("❌ Log file is empty")

    games = []
    with open(log_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                games.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"⚠️ JSON decode error at line {line_num}: {e}")
                continue

    print(f"✅ Successfully loaded {len(games)} games")
    return games

def analyze_locally(games):
    print("📊 Performing local data analysis...\n")

    alice_wins = [g for g in games if g["winner"] == "Alice"]
    bob_wins = [g for g in games if g["winner"] == "Bob"]
    alice_win_rate = len(alice_wins) / len(games)

    winning_x1 = [g["alice_first"] for g in alice_wins if g["alice_first"] is not None]
    x1_counter = Counter(winning_x1)
    top_openings = x1_counter.most_common(5)

    all_numbers = []
    for g in games:
        all_numbers.extend(g["chain"])
    freq = Counter(all_numbers)
    key_numbers = [n for n, c in freq.most_common(10)]

    print(f"🏆 Alice's win rate: {alice_win_rate:.1%}")
    print(f"🎯 Most common winning opening: {top_openings[0][0]} ({top_openings[0][1]} times)")
    print(f"🔑 Top 6 frequent numbers: {', '.join(map(str, [n for n, c in freq.most_common(6)]))}")

    return {
        "alice_win_rate": alice_win_rate,
        "top_openings": top_openings,
        "key_numbers": key_numbers
    }

def ask_openai_for_english_answer(data_summary):
    if not OPENAI_API_KEY or "your-api-key" in OPENAI_API_KEY:
        print("⚠️ OpenAI API Key not set or invalid, skipping API call")
        return None

    try:
        client = OpenAI(
            api_key=OPENAI_API_KEY,
            base_url="https://api.siliconflow.cn/v1"
        )

        # ✅ 强引导：先数学分析，再批判数据，最后精炼策略
        prompt = f"""
You are a world-class mathematical modeler. Derive the optimal strategy for Alice in the 1-100 number chain game.

⚠️ WARNING: Data shows Alice often wins by opening with 100. Do not accept this at face value.

### Step 1: Mathematical Structure
- Model the game as a directed graph: edge a→b exists if b = k×a ≤ 100.
- Prove that playing a large prime (>50) forces Bob to play 1.
- Show that 64 = 2^6 enables the longest chain: 64→32→16→8→4→2→1 (7 moves).
- Explain why controlling such nodes is superior to taking 100.

### Step 2: Critique the Data
- Why might 100 appear frequently in winning games?
- Could this reflect a limitation of the training method (e.g., short-term reward bias)?
- Is it a local optimum, not global?

### Step 3: Optimal Strategy (Be Concise)
Write a rigorous, academic answer. Requirements:
1. Sections: Opening, Mid-game, End-game, Core Principle.
2. Focus on **control of game flow**, not score.
3. Use precise reasoning.
4. Output in Markdown.
5. 400–500 words.
6. Never mention "neural network" or "reinforcement learning".
7. End with one-sentence summary of the core principle.
""".strip()

        print("☁️ Calling OpenAI (v1 API) to generate English answer...")

        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a precise and academic math modeling expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=800
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"❌ OpenAI API call failed: {e}")
        return None

def save_english_answer(final_answer, local_summary, openai_answer=None):
    project_root = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(project_root, "..", "results_q2_en.md")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# MCM Game AI - Question (2) Answer\n\n")
        f.write("## Experimental Summary\n")
        f.write(f"- Alice's win rate: {local_summary['alice_win_rate']:.1%}\n")
        f.write(f"- Top winning openings: {local_summary['top_openings'][:3]}\n")
        f.write(f"- Key frequent numbers: {local_summary['key_numbers'][:6]}\n\n")

        f.write("## Final Answer\n")
        if openai_answer:
            f.write(openai_answer)
        else:
            top_open, count = local_summary['top_openings'][0]
            fallback = f"""
### Optimal Strategy for Alice

The optimal strategy prioritizes control over immediate gain.

#### Opening: Force Bob to Play 1
- Play a large prime (>50), e.g., 97: Bob can only respond with 1.
- Or play 64 (2⁶): starts the longest chain (64→32→...→1).
- Avoid 100: though large, it allows Bob to start a long chain.

#### Mid-game: Control Hubs
- Target numbers with many divisors (e.g., 60, 48): they offer multiple continuation paths.

#### End-game: Control Parity
- Aim to end on an odd move to maximize turns.
- Force Bob to play 1 when the longest remaining chain has odd length.

#### Core Principle: Sacrifice for Control
- Occasionally forgo a high score (e.g., 50) to deny Bob a long chain.
- Victory comes from **"Block → Expand → Dominate"**, not maximizing single-move gain.

In summary, Alice should seize control early through primes or 64, then dominate the game structure.
"""
            f.write(fallback)

    print(f"\n✅ English answer saved to: {output_path}")

if __name__ == "__main__":
    games = load_games()
    local_summary = analyze_locally(games)
    openai_answer = ask_openai_for_english_answer(local_summary)
    
    print("\n" + "="*60)
    print("📝 FINAL ENGLISH ANSWER (for MCM paper):")
    print("="*60)
    if openai_answer:
        print(openai_answer)
    else:
        print("⚠️ Failed to generate OpenAI answer. Using fallback explanation (see results_q2_en.md).")

    save_english_answer(openai_answer, local_summary, openai_answer)