import os
import argparse
from tqdm import tqdm

import ray
from ray.tune.registry import register_env
from ray.rllib.env.wrappers.pettingzoo_env import PettingZooEnv
from ray.rllib.policy.policy import Policy

from ChineseChecker import chinese_checker_v0

# Policies
from agents import *


def load_policy(
    checkpoint_path,
    policy_name = 'default_policy'
):
    policy = Policy.from_checkpoint(checkpoint_path)
    policy = policy[policy_name]
    return policy


def play(args):
    env = chinese_checker_v0.env(render_mode=args.render_mode, triangle_size=args.triangle_size, max_iters=200)

    # Greedy Policy
    greedy_policy = GreedyPolicy(args.triangle_size)
    # RL Baseline
    rl_baseline_policy = load_policy(
        os.path.join(
            os.path.dirname(__file__),
            'pretrained',
        )
    )

    if not args.use_rl:
        #############################
        # TODO: 导入你的minimax agent
        #############################
        your_policy = None
    else:
        # 若你实现了基于强化学习的agent，在此处导入
        your_policy = load_policy(args.checkpoint)

    # Play with Greedy
    print('Play with Greedy')
    wr1 = evaluate_20_trials(env, your_policy, greedy_policy, args.render_mode)
    print(f"Winrate: {wr1}")
    # Play with RL Baseline
    print('Play with RL Baseline')
    wr2 = evaluate_20_trials(env, your_policy, rl_baseline_policy, args.render_mode)
    print(f"Winrate: {wr2}")

    env.close()


def evaluate_20_trials(env, your_policy, baseline_policy, render_mode=None):
    won = 0

    for i in tqdm(range(20)):
        env.reset(seed=i)
        for a in range(len(env.possible_agents)):
            env.action_space(env.possible_agents[a]).seed(i)
        
        # 游戏循环
        for agent in env.agent_iter():
            obs, reward, termination, truncation, info = env.last()
            if termination or truncation:
                break
            else:
                # 根据代理选择策略
                if agent == env.possible_agents[0]:
                    action = your_policy.compute_single_action(obs)
                else:
                    action = baseline_policy.compute_single_action(obs)
            act = int(action[0])
            if render_mode:
                env.render()
            env.step(act)
            
        # 记录胜利者
        if env.unwrapped.winner == env.possible_agents[0]:
            won += 1
    
    return won / 20.0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--triangle_size', type=int, default=2)  # 三角区域大小
    parser.add_argument('--render_mode', type=str, default=None)  # 渲染模式
    parser.add_argument('--use_rl', action='store_true')  # 渲染模式
    parser.add_argument('--checkpoint', type=str, required=True)
    args = parser.parse_args()
    play(args)