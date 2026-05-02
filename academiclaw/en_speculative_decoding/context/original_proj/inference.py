import torch
import time
import os
import sys

# 动态导入模型
sys.path.append(os.path.dirname(__file__))
from gpt_lite import GPTConfig, GPTLite

def load_target_model(device):
    # 加载 4层 大模型 (模拟延迟 20ms)
    config = GPTConfig(n_layer=4, n_embd=64, vocab_size=1000)
    model = GPTLite(config, simulate_latency=True)
    
    # 加载预训练权重
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(base_dir, "models/target_model.pt")
    
    if os.path.exists(model_path):
        model.load_state_dict(torch.load(model_path, map_location=device))
        print(">>> Loaded Target Model (Simulated Latency = 20ms)")
    else:
        print("⚠️ Warning: Model weights not found. Run setup_benchmark.py first.")
    
    model.to(device)
    model.eval()
    return model

def load_draft_model(device):
    # 加载 1层 小模型 (无延迟)
    config = GPTConfig(n_layer=1, n_embd=64, vocab_size=1000)
    model = GPTLite(config, simulate_latency=False)
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(base_dir, "models/draft_model.pt")
    
    if os.path.exists(model_path):
        model.load_state_dict(torch.load(model_path, map_location=device))
        print(">>> Loaded Draft Model (No Latency)")
    
    model.to(device)
    model.eval()
    return model

def autoregressive_sampling(model, prompt, max_new_tokens=50):
    """
    标准的串行贪婪搜索 (Baseline)
    Agent 需要参考这个函数来实现 speculative_sampling
    """
    idx = prompt.clone()
    past_key_values = None
    
    for _ in range(max_new_tokens):
        # 1. Forward
        if past_key_values is None:
            logits, past_key_values = model(idx)
        else:
            logits, past_key_values = model(idx[:, -1:], past_key_values)
            
        # 2. Greedy Search (Argmax)
        last_logit = logits[:, -1, :]
        next_token = torch.argmax(last_logit, dim=-1, keepdim=True)
        
        # 3. Append
        idx = torch.cat((idx, next_token), dim=1)
        
    return idx

if __name__ == "__main__":
    device = "cuda" if torch.cuda.is_available() else "cpu"
    target_model = load_target_model(device)
    prompt = torch.randint(0, 1000, (1, 10)).to(device)
    
    print("\n[Baseline] Running Autoregressive Sampling...")
    torch.cuda.synchronize()
    start = time.time()
    output = autoregressive_sampling(target_model, prompt, max_new_tokens=20)
    torch.cuda.synchronize()
    end = time.time()
    
    print(f"Time: {end - start:.2f}s")
    print(f"Output: {output.tolist()}")