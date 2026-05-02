Query 2: A3C + PPO on Pendulum-v1

You are a deep reinforcement learning expert. Implement and train both A3C and PPO algorithms in this working directory, using Gymnasium's Pendulum-v1 environment.

Requirements and deliverables:
- train.py: Training entry point. Supports --algo a3c|ppo, sets hyperparameters, and calls the corresponding algorithm.
- a3c.py: A3C training implementation (torch.multiprocessing for multi-process, n-step updates, async global network updates).
- ppo.py: PPO training implementation (GAE advantage estimation, clipped surrogate objective, mini-batch multi-epoch iteration).
- models.py: Actor-Critic network. Actor output mapped to the action space [-2, 2] (tanh + scaling), Critic outputs V(s).
- utils.py: Logging, checkpoint save/load, TensorBoard recording.
- evaluate.py: Load a model and evaluate it, with rendering support.
- README.md: Describe dependency installation, run commands, and TensorBoard usage.

Training objective:
- Within 500-1000 episodes, average reward should converge to -300 or higher.
- Use reward normalization or gradient clipping to ensure stability.

Notes:
- All code and output files should be written directly into the current working directory.
- You may use context/A3C+PPO.pdf as a reference, but do not copy reference answers or scoring criteria into this file.
- The evaluation script will call eval/rubric.py after each attempt to score and generate feedback.
