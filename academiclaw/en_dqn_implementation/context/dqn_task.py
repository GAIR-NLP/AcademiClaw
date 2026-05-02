# dqn_task.py
import gymnasium as gym
import numpy as np
import random
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque

# 建议超参数
ENV_NAME = 'MountainCar-v0'
GAMMA = 0.99
LR = 1e-3
BATCH_SIZE = 64
BUFFER_SIZE = 10000
TARGET_UPDATE = 1000
EPS_START = 1.0
EPS_END = 0.01
EPS_DECAY = 5000
NUM_EPISODES = 2000
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# TODO 1: 网络结构要求
# 实现一个包含两层隐藏层（每层 64 单元）的全连接网络，使用 ReLU 激活。
class QNetwork(nn.Module):
    def __init__(self, state_dim, action_dim):
        super(QNetwork, self).__init__()
        # --- 补全代码 ---
        pass

    def forward(self, x):
        # --- 补全代码 ---
        pass

# TODO 2: 经验回放要求
# 实现 push 方法存储五元组，实现 sample 方法返回 numpy 数组格式的批量数据。
class ReplayBuffer:
    def __init__(self, capacity):
        self.buffer = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        # --- 补全代码 ---
        pass

    def sample(self, batch_size):
        # --- 补全代码，确保返回 (s, a, r, s_, d) 的元组 ---
        pass

    def __len__(self):
        return len(self.buffer)

def epsilon_by_frame(frame_idx):
    return EPS_END + (EPS_START - EPS_END) * np.exp(-1. * frame_idx / EPS_DECAY)

# TODO 3: 训练逻辑要求
# 1. 必须支持 double_dqn 开关。
# 2. 必须返回 all_rewards 列表。
# 3. DDQN 需实现：y = r + gamma * Q_target(s', argmax(Q_online(s')))
def train_dqn(env, double_dqn=False):
    state_dim = env.observation_space.shape[0]
    action_dim = env.action_space.n
    online_net = QNetwork(state_dim, action_dim).to(DEVICE)
    target_net = QNetwork(state_dim, action_dim).to(DEVICE)
    target_net.load_state_dict(online_net.state_dict())
    optimizer = optim.Adam(online_net.parameters(), lr=LR)
    replay_buffer = ReplayBuffer(BUFFER_SIZE)
    all_rewards = []
    frame_idx = 0

    for episode in range(NUM_EPISODES):
        state, _ = env.reset()
        episode_reward = 0
        done = False
        while not done:
            # --- TODO: epsilon-greedy 动作选择 ---
            action = 0 
            
            next_state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated
            
            # --- TODO: 存储样本并更新状态 ---
            
            if len(replay_buffer) > BATCH_SIZE:
                # --- TODO: 计算 Loss 并更新 Online Network ---
                # 注意区分 DQN 与 Double DQN 的目标值计算逻辑
                pass

            if frame_idx % TARGET_UPDATE == 0:
                target_net.load_state_dict(online_net.state_dict())
            
            state = next_state
            episode_reward += reward
            frame_idx += 1
            
        all_rewards.append(episode_reward)
    return all_rewards

if __name__ == "__main__":
    # --- TODO: 执行训练 ---
    pass