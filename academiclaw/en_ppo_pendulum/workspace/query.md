## Reinforcement Learning Assignment 2: PPO Algorithm Implementation for Pendulum-v1 Continuous Environment

### 1. Task Description

**Background**:
In continuous action space environments such as `Pendulum-v1`, traditional Policy Gradient algorithms often suffer from extremely unstable training due to difficulty in determining the step size. This task requires implementing the **Proximal Policy Optimization (PPO)** algorithm, which introduces a **Clipped Surrogate Objective** to constrain the magnitude of policy updates.

**Requirements**:

1. **Algorithm Implementation**: Implement the PPO algorithm based on an Actor-Critic architecture.
* **Actor**: Outputs the mean (mu) and standard deviation (sigma) of a Gaussian distribution.
* **Critic**: Estimates the state value function.


2. **Core Mechanism**: Must include PPO's Clipping mechanism, ensuring the probability ratio between new and old policies stays within a safe interval.
3. **Output Requirements**:
* Submit the `ppo_pendulum.py` code.
* **Performance Target**: After training is complete, perform 5 independent evaluation episodes. **The average return must be greater than -350**.

