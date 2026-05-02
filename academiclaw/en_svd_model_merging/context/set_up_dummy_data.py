# setup_dummy_data.py
import torch
import torch.nn as nn
import os
import shutil

# 1. 定义一个简单的 Tiny Model
# 包含 Linear (2D weight + 1D bias) 和 LayerNorm (1D weight + 1D bias)
# 确保能测试到论文中关于不同维度处理的要求
class TinyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(10, 8)  # Weight: [8, 10], Bias: [8]
        self.ln = nn.LayerNorm(8)    # Weight: [8], Bias: [8]
        self.fc2 = nn.Linear(8, 4)   # Weight: [4, 8], Bias: [4]

    def forward(self, x):
        return self.fc2(self.ln(self.fc1(x)))

def generate_data(root_dir="./mock_data"):
    # 清理旧数据
    if os.path.exists(root_dir):
        shutil.rmtree(root_dir)
    os.makedirs(root_dir)

    model_name = "Tiny-ViT"
    datasets = ["Task_A", "Task_B", "Task_C"]
    
    base_path = os.path.join(root_dir, "checkpoints", model_name)
    os.makedirs(base_path, exist_ok=True)

    # 1. 生成 Pre-trained Model (Zero-shot)
    torch.manual_seed(42)
    ptm = TinyModel()
    ptm_path = os.path.join(base_path, "zeroshot.pt")
    torch.save(ptm.state_dict(), ptm_path)
    print(f"Generated Pre-trained model at {ptm_path}")

    # 2. 生成各个 Task 的 Fine-tuned Models
    # 通过在 PTM 基础上加随机噪声来模拟微调
    for task in datasets:
        task_path = os.path.join(base_path, task)
        os.makedirs(task_path, exist_ok=True)
        
        # 模拟微调：加一些噪声
        ft_state_dict = {}
        for k, v in ptm.state_dict().items():
            noise = torch.randn_like(v) * 0.1
            ft_state_dict[k] = v + noise
        
        save_path = os.path.join(task_path, "finetuned.pt")
        torch.save(ft_state_dict, save_path)
        print(f"Generated Fine-tuned model for {task} at {save_path}")

    print("\n✅ Dummy data generation complete!")
    print(f"Root Directory: {os.path.abspath(root_dir)}")

if __name__ == "__main__":
    generate_data()