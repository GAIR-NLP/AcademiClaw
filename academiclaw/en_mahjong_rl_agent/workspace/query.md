# Query 1: Reinforcement Learning-Based Mahjong Agent

## [Query Description]

Design a reinforcement learning-based Mahjong agent that can learn reasonable tile-discarding strategies given a hand of tiles and rule constraints, achieving a high win rate across multiple rounds of play. This task aims to apply deep reinforcement learning theory to a complex multi-player game environment, evaluating core abilities in state space modeling, action selection strategy, and reward function design.

## [Background]

Mahjong is a highly complex multi-player imperfect information game involving multiple factors: randomness (drawing tiles), strategy (tile selection), and competition (multi-player rivalry). Designing Mahjong AI requires handling:
- **Large-scale state space**: Hand tile combinations, discard history, inference about other players' possible hands
- **Partial observability**: Cannot directly observe other players' hands
- **Long-term rewards**: The value of a single discard must consider the impact of subsequent multiple steps
- **Multi-agent interaction**: Must respond to strategy changes by other players

Reinforcement learning provides a powerful tool for solving such problems. Through interaction with the environment and receiving reward feedback, the agent can gradually learn effective strategies.

## [Context]

### 1. Mahjong Rules:

**Basic Information:**
- Players: 4
- Total tiles: 136
- Tile types:
  - Characters (1-9), 4 of each, 36 total
  - Bamboo (1-9), 4 of each, 36 total
  - Dots (1-9), 4 of each, 36 total
  - Winds (East, South, West, North), 4 of each, 16 total
  - Dragons (Red, Green, White), 4 of each, 12 total

**Basic Flow:**
1. **Dice Roll to Determine Dealer**: Randomly determine the dealer position
2. **Drawing Tiles**: The dealer draws 14 tiles, the other three players each draw 13 tiles
3. **Taking Turns**: The dealer plays first, then turns proceed clockwise. Each turn, a player draws one tile and then discards one tile
4. **Chow/Pung/Kong Operations**:
   - **Pung**: When you have two identical tiles and someone discards a third identical tile, you may "Pung" to claim it, then discard one tile from your hand. The three tiles are placed face-up on the table
   - **Kong**:
     - **Exposed Kong**: When you have three identical tiles and someone discards the fourth, you may "Kong"
     - **Concealed Kong**: When you have four identical tiles in hand, you may declare a "Concealed Kong"
     - **Added Kong**: After a Pung, when you draw the fourth identical tile, you may "Added Kong"
   - After a Kong, draw one tile from the end of the wall (Kong replacement draw), then discard one tile
5. **Riichi (Optional Rule)**: When in Tenpai (one tile away from winning), you may declare "Riichi", announcing your ready state. After this, you cannot change your waiting pattern, but you receive extra points upon winning
6. **Winning Settlement**: When the winning condition is met (generally 4 sets of sequences/triplets + 1 pair, or special hands like Seven Pairs, Full Flush, etc.), you may declare a win. Points are calculated based on the hand and scores are settled
7. **Draw Game**: If the wall is exhausted and no one wins, it is a draw, with no settlement or special rules applied

**Points:**

| Type | Points | Description |
|------|--------|-------------|
| Basic Win | 1 pt | Basic winning hand, composed of sequences and triplets |
| All Triplets | 2 pts | Entirely composed of triplets (three identical tiles) |
| Full Flush | 4 pts | All tiles are of the same suit (Characters/Bamboo/Dots) |
| Seven Pairs | 4 pts | Composed of seven pairs |
| Win After Kong | +1 pt | Winning immediately with the tile drawn after a Kong |
| Self-Draw | x2 | Winning by drawing your own tile (not from another's discard), score doubled |

Final Score = Base Points x Tile Value Bonus + Kong Points

**Kong Rules and Points:**
- **Exposed Kong** (Kong from another's discard): Each of the other three players pays 1 point
- **Concealed Kong** (Four identical tiles in hand): Each of the other three players pays 2 points
- **Added Kong** (Drawing the fourth tile after a Pung): 1 point

### 2. Agent Interface Requirements

You need to implement the following Agent interface so your agent can interact with the Mahjong game environment:

**Important: Please strictly follow the interface specification below to ensure data formats match exactly, otherwise evaluation will fail!**

```python
# =========================================================
# Agent Interface
# =========================================================

class MahjongAgent:
    """Mahjong agent base class"""

    def act(self, obs: Dict) -> Dict:
        """
        Select an action based on the observation

        Parameters:
        -----------
        obs: Dict
            Observation information (note: this is the actual format passed by the evaluation environment):
            {
                "hand": List[str],          # Current hand tiles, format e.g. ["B1", "B2", "T3", "M5", "E", "S"]
                                            # Characters=B, Bamboo=T, Dots=M; Winds=E/S/W/N; Dragons=P/F/D
                "melds": List[List[str]],   # Punged/Konged tile groups, e.g. [["B1", "B1", "B1"]]
                "riichi": bool,             # Whether currently in Riichi state
                "last_draw": str or None,   # Last drawn tile, e.g. "B5"
                "can_riichi": bool,         # Whether Riichi is currently available
                "other_players": List[Dict] # Other players' information, format:
                    [
                        {
                            "pid": int,            # Player ID
                            "discards": List[str], # Discarded tiles
                            "melds": List[List[str]], # Punged/Konged tile groups
                            "riichi": bool         # Whether in Riichi state
                        },
                        ...
                    ]
            }

        Tile representation format (must be strictly followed):
        - Character tiles: "B1" ~ "B9"  (B = Characters)
        - Bamboo tiles: "T1" ~ "T9"  (T = Bamboo)
        - Dot tiles: "M1" ~ "M9"  (M = Dots)
        - Wind tiles: "E" (East), "S" (South), "W" (West), "N" (North)
        - Dragon tiles: "P" (Red), "F" (Green), "D" (White)

        Returns:
        --------
        action: Dict
            Action dictionary, must contain:
            {
                "type": str,  # Action type, must be "discard" or "riichi_discard"
                "tile": str   # Tile to discard, must be in obs["hand"], format e.g. "B3"
            }

        Notes:
        1. The returned tile must exist in obs["hand"], otherwise it is treated as an illegal action
        2. type only supports "discard" and "riichi_discard"
        3. Tile format must match the input format (e.g. "B1" not "1-Character")

        Example:
        --------
        >>> obs = {
        ...     "hand": ["B1", "B2", "B3", "T1", "T2", "T3", "E", "E"],
        ...     "melds": [],
        ...     "riichi": False,
        ...     "last_draw": "E",
        ...     "can_riichi": False,
        ...     "other_players": [...]
        ... }
        >>> action = agent.act(obs)
        >>> print(action)  # {"type": "discard", "tile": "E"}
        """
        raise NotImplementedError("Subclass must implement the act method")


class RandomAgent(MahjongAgent):
    """Random strategy agent (baseline)"""

    def act(self, obs):
        import random
        hand = obs.get("hand", [])
        if not hand:
            # Edge case: if hand is empty, return a safe action
            return {"type": "discard", "tile": ""}

        tile = random.choice(hand)

        # 10% chance of Riichi (if available)
        if obs.get("can_riichi", False) and random.random() < 0.1:
            return {"type": "riichi_discard", "tile": tile}

        return {"type": "discard", "tile": tile}
```

### 3. Reference Files

- `context/before.py`: Basic implementation code for the Mahjong game environment, including game logic, state management, action execution, etc. You can reference this file to understand the environment interface, but you do not need to modify it.

## [Deliverable Requirements]

### 1. **Python Code Files** (Required)

Implement a reinforcement learning-based Mahjong agent. Suggested file name: `rl_mahjong_agent.py` or similar.

**Core Requirements:**
- **Must implement the `MahjongAgent` interface**, overriding the `act(obs)` method
- **Must correctly handle data formats in obs** (see interface description above), ensure tile representation format is consistent
- Suggested agent class name: `RLMahjongAgent` or `DQNMahjongAgent`, etc.
- Any reinforcement learning algorithm may be used:
  - Value function methods: Q-Learning, Deep Q-Network (DQN), Double DQN, Dueling DQN
  - Policy gradient methods: REINFORCE, Actor-Critic, A3C, A2C
  - Combined methods: Proximal Policy Optimization (PPO), Soft Actor-Critic (SAC)
- Code structure should be clear with necessary comments

**Key Design Points:**
- **State Representation**: How to encode current hand, discards, possible actions, etc. as neural network input
  - Suggested: 34-dimensional tile count vector (Characters 1-9, Bamboo 1-9, Dots 1-9, East/South/West/North, Red/Green/White)
  - Handle tile format conversion ("B1" -> Character 1)
- **Action Space**: Define all possible discard actions
  - Suggested: 34-dimensional action space, each action corresponds to discarding one type of tile
  - Must filter illegal actions (tiles not in hand)
- **Reward Function**: How to design reward signals to guide agent learning
  - Sparse reward: Win +100, Draw 0, Deal-in -50
  - Dense reward (optional): Small reward each step based on changes in Shanten number
  - Combined reward: Incorporate final score, winning hand type, etc.
- **Neural Network Architecture**: What network structure to use (FC, CNN, RNN, etc.)

**Special Note (Regarding Training):**
- Warning: **RL models need training to be effective**; untrained or undertrained models may perform poorly
- Warning: **The evaluation environment will NOT perform training**, it will only call the `act()` method
- Two recommended approaches:
  1. **Pre-trained model**: Provide trained model weight files (e.g., `model.pth`), auto-loaded in `__init__`
  2. **Rule-assisted strategy**: Use heuristic rules as fallback when training is insufficient (e.g., prioritize discarding isolated tiles, preserve sequence/triplet structures, etc.)
- If using a pre-trained model, describe the training process and hyperparameters in the README

### 2. **Training Code** (Optional)

If the agent requires training, provide a training script. Suggested file name: `train.py`.

**Contents should include:**
- Training loop code
- Hyperparameter settings (learning rate, batch size, exploration rate, etc.)
- Training log recording (loss, reward, win rate curves, etc.)
- Model save and load logic

If the model is already trained, provide the **model weight file** (`model.pth`, `model.h5`, etc.) and explain how to load and use it in the README.

### 3. **README.md** (Required)

Detailed documentation that includes at least the following:

```markdown
# Reinforcement Learning-Based Mahjong Agent

## Algorithm Description
- RL algorithm used (e.g., DQN / PPO / A3C)
- State space design: how observation information is represented
- Action space design: how actions are defined
- Reward function design: how reward signals are designed
- Neural network architecture: network structure diagram or description

## Dependency List
```
python >= 3.8
torch >= 1.10  (or tensorflow >= 2.6)
numpy >= 1.20
...
```

## Installation and Usage
```bash
# Install dependencies
pip install -r requirements.txt

# Run the agent (load pre-trained model)
python run_agent.py

# Train the agent (optional)
python train.py
```

## Performance
- Game testing: Win rate statistics from 100 game tests
- Comparison with random strategy: Win rate improvement
- Training curves (optional): Reward/win rate changes over training episodes

## References (Optional)
List referenced papers, blog posts, open-source projects, etc.
```

### 4. **Performance Test Report** (Optional)

Provide agent performance test results. Suggested file name: `test_results.txt` or `performance_report.md`.

**Suggested contents:**
- Win rate statistics from at least 100 games
- Comparative experiments with RandomAgent
- Average score per game
- Training curve plots (if available)

## [Performance Requirements]

1. **Functionality**: The agent must run normally and be able to receive observations and output legal actions
2. **Effectiveness**: The agent's strategy should significantly outperform the random strategy (win rate improvement of at least 10% recommended)
3. **Reproducibility**: Provide clear instructions for others to reproduce results

## [Hints]

### Data Format Conversion (Important!)

The evaluation environment uses a tile representation format different from common representations. **Format conversion must be handled correctly**:

| Common Representation | Evaluation Format | Description |
|----------------------|-------------------|-------------|
| 1-Character ~ 9-Character | B1 ~ B9 | B = Characters |
| 1-Bamboo ~ 9-Bamboo | T1 ~ T9 | T = Bamboo |
| 1-Dot ~ 9-Dot | M1 ~ M9 | M = Dots |
| East/South/West/North | E, S, W, N | Wind tiles |
| Red/Green/White | P, F, D | Dragon tiles (Red=P, Green=F, White=D) |

**Example conversion code:**
```python
# Tile mapping table (34 tile types)
TILES_34 = [
    "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9",  # Characters
    "T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9",  # Bamboo
    "M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9",  # Dots
    "E", "S", "W", "N",  # East, South, West, North
    "P", "F", "D"        # Red, Green, White
]

TILE_TO_ID = {tile: i for i, tile in enumerate(TILES_34)}
ID_TO_TILE = {i: tile for i, tile in enumerate(TILES_34)}

def hand_to_counts(hand: List[str]) -> np.ndarray:
    """Convert hand tile list to count vector (34-dimensional)"""
    counts = np.zeros(34, dtype=np.int32)
    for tile in hand:
        if tile in TILE_TO_ID:
            counts[TILE_TO_ID[tile]] += 1
    return counts
```

### Algorithm Selection Suggestions
- **DQN series** (Recommended for beginners): Deep Q-Network and variants (Double DQN, Dueling DQN), suitable for discrete action spaces
- **PPO** (Recommended for intermediate): Proximal Policy Optimization, good training stability, suitable for complex environments
- **A3C/A2C**: Asynchronous Advantage Actor-Critic, suitable for parallel training
- **Rule-assisted methods** (Recommended for quick implementation): Heuristic rules + minimal learning, can quickly achieve reasonable performance
- **Others**: REINFORCE, SAC, Rainbow DQN, etc.

### State Representation Suggestions
- **Hand encoding**: 34-dimensional count vector (quantity of each tile 0-4)
- **Seen tile statistics**: Count remaining tiles of each type (inferred from discards)
- **Game state**: Whether Riichi is available, last drawn tile (one-hot encoding), other players' Riichi status
- **Feature engineering**: May add advanced features like Shanten number, effective tile count

### Reward Function Design Suggestions
- **Sparse reward**: Win +100, Draw 0, Deal-in -50
- **Dense reward**: Small reward each step based on hand value changes (e.g., Shanten decrease +5)
- **Combined reward**: Incorporate final score, winning hand type, Kong rewards, etc.
- **Risk penalty**: Negative reward for discarding dangerous tiles (when other players are in Riichi)

### Training Tips
- Use **Experience Replay** to improve sample efficiency
- Use **Target Network** to stabilize training
- Gradually decay **Exploration Rate**: from 1.0 to 0.05
- Consider **Self-play** to improve strategy robustness
- **Training duration**: DQN typically needs 10,000 ~ 100,000 games to converge
- **Pre-training strategy**: Can use imitation learning for pre-training, then fine-tune with RL

### Quick Implementation Suggestions (For Limited Time)

Since RL training takes a long time, consider one of the following strategies:

**Option 1: Rules + Minimal Learning (Recommended)**
```python
class HybridAgent(MahjongAgent):
    def act(self, obs):
        hand = obs["hand"]

        # Use simple rules to select candidate actions
        candidates = self.get_rule_based_candidates(hand)

        # If a trained model is available, use the model to select among candidates
        if self.model and self.is_trained:
            tile = self.model_select(candidates, obs)
        else:
            # Fall back to rule-based strategy
            tile = self.rule_select(candidates, obs)

        return {"type": "discard", "tile": tile}

    def get_rule_based_candidates(self, hand):
        # Rules: prioritize discarding isolated tiles, honor tiles, edge tiles
        # ...
        pass
```

**Option 2: Use a Pre-trained Model**
- Train the model locally and save weight files (e.g., `model.pth`)
- Load the model during Agent initialization
- Note: Training requires at least several hours (GPU recommended)

**Option 3: Pure Rule-Based Strategy (Baseline)**
- Implement heuristic rules, such as:
  - Discard the tile that increases Shanten number the least
  - Prioritize preserving sequence/triplet structures
  - Discard isolated and edge tiles
  - Avoid discarding dangerous tiles (when other players are in Riichi)
- While not RL, this serves as a Baseline reference

### Tools and Frameworks
- **Deep learning frameworks**: PyTorch (recommended), TensorFlow, JAX
- **Reinforcement learning libraries**: Stable-Baselines3 (recommended), RLlib, TF-Agents
- **Environment interface**: Reference context/before.py for environment interaction
- **Shanten calculation**: Can reference open-source implementations (e.g., mahjong-python)


