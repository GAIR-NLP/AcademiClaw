### [Query: Code Migration - DQN Reinforcement Learning]

You are a reinforcement learning researcher who needs to migrate an existing DQN (Deep Q-Network) reinforcement learning algorithm implemented in TensorFlow to the PyTorch framework, and replace the deprecated Gym library with Gymnasium.

**Requirements:**
1. Maintain the core structure of the DQN algorithm (including the neural network model, experience replay buffer, target network updates, etc.) and configuration (including model parameters, loss function, optimizer, etc.) unchanged.
2. Ensure it can run properly in a PyTorch environment, including model training, inference, and interaction with the Gymnasium environment.
3. Add a hyperparameter tuning module to tune some key parameters, record and visualize the performance under different hyperparameter combinations.
4. Visualize the training process, including reward curves, loss function values, etc., to facilitate model performance analysis.
5. Implement all functionality in a single Python file, ensure clear code structure, provide comments at key sections, and add necessary instructions at the beginning of the code (required libraries, how to run, etc.).

**Expected Output:**
- `dqn_torch.py` - A runnable single-file implementation containing:
  - DQN implementation using PyTorch
  - Experience Replay (ReplayBuffer)
  - Target network updates
  - Hyperparameter tuning module
  - Training visualization (reward curves, loss curves, etc.)
  - Able to train and evaluate in a Gymnasium environment (MountainCar-v0)
  - Output training logs and image files

**Context:**
Original TensorFlow code files:
- `context/agent.py` - TensorFlow version DQN agent
- `context/replay_buffer.py` - Experience replay buffer
- `context/main.py` - Main program entry point
- `context/ReadMe.txt` - Original configuration description
- `context/requirements.txt` - Original dependency list
