## Experiment Task: Double DQN-Based MountainCar Energy Hill-Climbing Optimization

### 1. Query (Task Description)

**Task Objective**:
Train an agent in the `MountainCar-v0` environment using the **Double DQN (DDQN)** algorithm. Due to extremely sparse rewards in this environment (-1 per step until reaching the goal), standard DQN tends to produce severe overestimation problems. You need to implement the core DDQN logic to improve training stability.

**Specific Requirements**:

1. **Algorithm Logic**: Modify the standard DQN target value computation. Use the **policy network** (Policy Net) to select the optimal action, and use the **target network** (Target Net) to compute the Q-value for that action.
2. **Network Architecture**: Since the state space is only 2-dimensional, simple fully connected layers (MLP) are sufficient; no convolutional layers needed.
3. **Output Requirements**:
* Submit a `ddqn_main.py` script containing model training and testing code.
* Record and save `loss` and `reward` data during training.
* **Performance Target**: The trained model must be able to reach the hilltop from the car's starting position within **200 steps** (i.e., single test reward > -200).

* **Environment Documentation**: [Gymnasium MountainCar-v0 Official Docs](https://gymnasium.farama.org/environments/classic_control/mountain_car/).
* **Algorithm Reference**: Paper "Deep Reinforcement Learning with Double Q-learning (Hasselt et al., 2015)".
