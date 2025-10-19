import sys
import os
import torch

# === 添加项目根目录到路径 ===
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

# === 修复 audioop 缺失问题（Anaconda 兼容性）===
try:
    import audioop
except ImportError:
    import sys
    sys.modules['audioop'] = type(sys)(name='audioop')

# === 导入模块 ===
import gradio as gr
from core.game import GameEnv
from agents.policy_net import SimplePolicy
from explain.strategy_explainer import explain_strategy  # 确保这个文件存在

# === 加载模型 ===
alice_policy = SimplePolicy()
model_path = os.path.join(project_root, "data_output", "alice_policy.pth")
alice_policy.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))  # 加上 map_location 防止 GPU/CPU 冲突
alice_policy.eval()

# === 推理函数 ===
def play_and_explain(chain_str):
    try:
        chain = list(map(int, chain_str.split()))
        if not chain or any(c <= 0 for c in chain):
            return "请输入正整数，用空格分隔。"

        env = GameEnv()
        env.chain = chain
        env.scores = [sum(chain[i] for i in range(0, len(chain), 2)),
                      sum(chain[i] for i in range(1, len(chain), 2))]
        env.player = len(chain) % 2  # 0=Alice, 1=Bob

        with torch.no_grad():
            explanation = explain_strategy(alice_policy, env)

        return explanation

    except Exception as e:
        return f"输入错误: {e}"

# === 创建 Gradio 界面 ===
iface = gr.Interface(
    fn=play_and_explain,
    inputs=gr.Textbox(placeholder="输入当前数字链，如：60 30 15", label="数字链"),
    outputs=gr.Textbox(label="AI 解释"),
    title="🎮 整除链博弈 AI 策略解释器",
    description="输入当前数字链（空格分隔），AI 将告诉你它的思考过程。",
    examples=[["60 30 15"], ["2 4 8 16"], ["97"]],
    theme="soft"
)

# === 启动服务 ===
if __name__ == "__main__":
    iface.launch()