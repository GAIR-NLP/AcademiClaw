# Task: DQN and Double DQN Algorithm Implementation

## 1. Task Objective
In this experiment, you need to implement and compare **DQN** and **Double DQN** algorithms in the `MountainCar-v0` environment. The core of the task is to fill in the missing logic and demonstrate that your implementation achieves significant convergence.

## 2. Context Files
All necessary files are in the `context/` folder within the working directory:
- `context/dqn_task.py`: Contains the task skeleton with `TODO` markers for code to be completed.

## 3. Standardized Development Workflow (TODO List)
Please modify `dqn_task.py` according to the following stages:

### TODO 1: Network Architecture (`QNetwork`)
- Build a feedforward neural network.
- **Requirements**: Input layer adapted to the environment state space (2-dimensional), output layer adapted to the action space (3-dimensional). Two hidden layers with 64 units each and ReLU activation are recommended.

### TODO 2: Experience Replay (`ReplayBuffer`)
- Maintain a circular queue.
- **Requirements**: Implement `push` to store transition tuples, implement `sample` to randomly return batch data (must convert to Numpy arrays to facilitate Tensor conversion).

### TODO 3: Training Logic (`train_dqn`)
- **Exploration strategy**: Implement $\epsilon$-greedy decay logic.
- **Target computation**:
  - `double_dqn=False`: $y_j = r_j + \gamma \max_{a'} \hat{Q}(s_{j+1}, a')$
  - `double_dqn=True`: $y_j = r_j + \gamma \hat{Q}(s_{j+1}, \text{argmax}_{a'} Q(s_{j+1}, a'))$
- **Data return**: Must return the `all_rewards` list for later performance evaluation.

## 4. Submission
Please save the completed **`dqn_task.py`** file in the current working directory.
