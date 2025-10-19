# forever_train.py
# AI 永动机启动脚本 —— 让训练自动持续进行

import time
import subprocess
import os
from datetime import datetime

# ================== 配置区 ==================
# 你可以自由修改这些参数
TOTAL_ROUNDS = None        # 总轮数：设为 None 表示无限运行；设为 5 就是跑 5 轮
SLEEP_BETWEEN_ROUNDS = 5   # 每轮之间休息几秒（防止瞬时重启，0 表示不休息）
# ===========================================

def run_training():
    """运行一次训练脚本"""
    print(f"🚀 开始训练: {datetime.now().strftime('%H:%M:%S')}")
    result = subprocess.run(["python", "agents/train_marl.py"], 
                          capture_output=False)  # 实时输出日志
    if result.returncode == 0:
        print("✅ 训练完成。")
    else:
        print("❌ 训练失败，错误码:", result.returncode)
    return result.returncode == 0

if __name__ == "__main__":
    print("🔥 AI 永动机已启动，开始自动训练...")
    print(f"📊 所有数据将保存在: E:/mcm_training_data")
    print(f"🔄 模式: {'无限循环' if TOTAL_ROUNDS is None else f'共 {TOTAL_ROUNDS} 轮'}")
    print("="*60)

    round_count = 0

    while True:
        # 检查是否达到最大轮数
        if TOTAL_ROUNDS is not None and round_count >= TOTAL_ROUNDS:
            print(f"🏁 已完成 {TOTAL_ROUNDS} 轮训练，任务结束。")
            break

        round_count += 1
        print("\n" + "="*60)
        print(f"🔁 第 {round_count} 轮训练开始 | {datetime.now().strftime('%H:%M:%S')}")
        print("="*60)

        success = run_training()

        if not success:
            print("⚠️ 上一轮训练失败，是否继续？等待 10 秒后重试...")
            time.sleep(10)
            continue  # 失败也继续下一轮

        # 轮次间小憩
        if SLEEP_BETWEEN_ROUNDS > 0:
            time.sleep(SLEEP_BETWEEN_ROUNDS)

    print("💤 训练任务全部完成，程序退出。")