import csv
import datetime
import os
import numpy as np
import glob
import argparse
from pathlib import Path
from tqdm import tqdm

from gymnasium.spaces import Box, Discrete

from pettingzoo.classic import rps_v2

import ray
from ray import tune
from ray.tune.registry import register_env
from ray.rllib.env.wrappers.pettingzoo_env import PettingZooEnv
from ray.rllib.algorithms.ppo import (
    PPO,
    PPOConfig,
)
from ray.rllib.models import ModelCatalog
from ray.rllib.core.rl_module.rl_module import SingleAgentRLModuleSpec
from ray.tune.logger import pretty_print
from ray.rllib.policy.policy import Policy

from ChineseChecker import chinese_checker_v0
from ChineseChecker.models.action_masking_rlm import TorchActionMaskRLM
from ChineseChecker.models.action_masking import ActionMaskModel
from ChineseChecker.logger import custom_log_creator

# Policies
from agents import (
    ChineseCheckersRandomPolicy,
    GreedyPolicy,
)


def train(config, model_name: str, train_config):
    """
    训练函数：执行训练循环，定期评估策略
    
    参数:
        config: PPO配置对象
        model_name: 模型名称（用于日志和检查点）
        train_config: 训练参数配置字典
    """
    # 创建时间戳和日志目录
    timestr = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    logdir = f"logs/chinese_checkers_{model_name}_{timestr}"
    
    # 构建PPO算法实例，使用自定义日志创建器
    algo = config.build(logger_creator=custom_log_creator(os.path.join(os.curdir, logdir), ''))

    # 提取训练配置参数
    triangle_size = train_config["triangle_size"]
    train_iters = train_config["train_iters"]
    eval_period = train_config["eval_period"]
    
    # 评估配置
    eval_config = {
        "triangle_size": train_config["triangle_size"],
        "eval_num_trials": train_config["eval_num_trials"],
        "eval_max_iters": train_config["eval_max_iters"],
        "render_mode": train_config["render_mode"],
        "logdir": logdir  # 日志目录
    }

    # 手动训练循环
    for i in range(train_iters):
        # 执行一次训练迭代
        result = algo.train()
        
        # 保存检查点
        checkpoint_dir = f"{logdir}/checkpoint{i}"
        save_result = algo.save(checkpoint_dir=checkpoint_dir)
        path_to_checkpoint = save_result.checkpoint.path
        print(
            "An Algorithm checkpoint has been created inside directory: "
            f"'{path_to_checkpoint}'."
        )
        
        # 打印训练结果
        print(f"""
              Iteration {i}: episode_reward_mean = {result['episode_reward_mean']},
                             episode_reward_max  = {result['episode_reward_max']},
                             episode_reward_min  = {result['episode_reward_min']},
                             episode_len_mean    = {result['episode_len_mean']}
              """)

        # 组织训练结果
        train_results = {
            "iteration": i,
            "env_steps": result["num_env_steps_sampled"],
            "episode_reward_mean": result["episode_reward_mean"],
            "episode_reward_max": result["episode_reward_max"],
            "episode_reward_min": result["episode_reward_min"],
            "episode_len_mean": result["episode_len_mean"]
        } 
        
        # 记录每个策略的奖励
        for policy_id in [0, 3]:
            if f"policy_{policy_id}" in result["policy_reward_mean"]:
                train_results[f"policy_{policy_id}_reward_mean"] = result["policy_reward_mean"][f"policy_{policy_id}"]
            else:
                train_results[f"policy_{policy_id}_reward_mean"] = np.nan
                                    

        # 获取策略用于评估
        policy = None
        if algo.get_policy("default_policy"):
            policy = algo.get_policy("default_policy")
        else:
            policy = algo.get_policy("policy_0")
            
        # 定期评估策略
        if i % eval_period == 0:
            # 评估策略对抗贪心策略
            t_size = eval_config['triangle_size']
            eval_results = { "iteration": i } | evaluate_policies(policy, GreedyPolicy(t_size), eval_config)

    return algo


def eval(policy_name: str = "default_policy", checkpoint_path: str = None, against_mode: str = 'greedy', eval_config=None):
    """
    评估函数：加载训练好的策略并进行评估
    
    参数:
        policy_name: 策略名称
        checkpoint_path: 检查点路径
        against_mode: 对抗模式
        eval_config: 评估配置
    """
    # 从检查点恢复策略
    policy = Policy.from_checkpoint(checkpoint_path)
    policy = policy[policy_name]

    # 使用恢复的策略进行动作选择
    if against_mode == 'self':
        # 与自身对抗
        evaluate_policies(policy, policy, eval_config)
    elif against_mode == 'random':
        # 与随机策略对抗
        triangle_size = eval_config['triangle_size']
        evaluate_policies(policy, ChineseCheckersRandomPolicy(triangle_size), eval_config)
    else:
        # 与贪心策略对抗
        triangle_size = eval_config['triangle_size']
        evaluate_policies(policy, GreedyPolicy(triangle_size), eval_config)



def evaluate_policies(eval_policy, baseline_policy, eval_config):
    """
    评估两个策略相互对抗
    
    参数:
        eval_policy: 评估策略（扮演player_0）
        baseline_policy: 基准策略（扮演其他玩家）
        eval_config: 评估配置
    """
    triangle_size = eval_config["triangle_size"]
    eval_num_trials = eval_config["eval_num_trials"]
    eval_max_iters = eval_config["eval_max_iters"]
    render_mode = eval_config["render_mode"]

    # 创建环境
    env = chinese_checker_v0.env(render_mode=render_mode, triangle_size=triangle_size, max_iters=eval_max_iters)
    print(
        f"Starting evaluation of {eval_policy} against baseline {baseline_policy}. Trained agent will play as {env.possible_agents[0]}."
    )

    # 初始化统计变量
    total_rewards = {agent: 0 for agent in env.possible_agents}
    wins = {agent: 0 for agent in env.possible_agents}
    iters = []  # 存储每局游戏的迭代次数
    num_moves = []  # 存储每局游戏的移动次数

    # 进行多次试验
    for i in tqdm(range(eval_num_trials)):
        env.reset(seed=i)
        for a in range(len(env.possible_agents)):
            env.action_space(env.possible_agents[a]).seed(i)
        
        # 游戏循环
        for agent in env.agent_iter():
            obs, reward, termination, truncation, info = env.last()
            total_rewards[agent] += reward
            if termination or truncation:
                break
            else:
                # 根据代理选择策略
                if agent == env.possible_agents[0]:
                    action = eval_policy.compute_single_action(obs)
                else:
                    action = baseline_policy.compute_single_action(obs)
            act = int(action[0])
            if render_mode:
                env.render()
            env.step(act)

        # 记录游戏统计
        iters.append(env.unwrapped.iters)
        num_moves.append(env.unwrapped.num_moves)

        # 累加游戏结束后的奖励
        for agent in env.possible_agents:
            rew = env._cumulative_rewards[agent]
            total_rewards[agent] += rew
            
        # 记录胜利者
        if env.unwrapped.winner:
            wins[env.unwrapped.winner] += 1
   
    env.close()

    # 计算统计指标
    winrate = wins[env.possible_agents[0]] / eval_num_trials
    average_rewards = {agent: total_rewards[agent] / eval_num_trials for agent in env.possible_agents}
    
    # 打印评估结果
    print("Total rewards (incl. negative rewards): ", total_rewards)
    print("Average rewards (incl. negative rewards): ", average_rewards)
    print("Winrate: ", winrate)
    print("Average iterations:", np.mean(iters))
    print("Average moves:", np.mean(num_moves))
    print(iters)
    
    # 返回评估结果
    return {
        "eval_num_trials": eval_num_trials,
        "eval_total_rewards": total_rewards["player_0"],
        "eval_average_rewards": average_rewards["player_0"],
        "eval_win_rate": winrate,
        "eval_average_iters": np.mean(iters),
        "eval_average_moves": np.mean(num_moves)
    }


