## Reinforcement Learning and Game Theory Assignment 4: Alpha-Beta Pruning Search Implementation in Checkers Environment

### 1. Query (Task Description)

**Task Background**:
In a simplified checkers environment (`triangle_size = 2`), the traditional greedy strategy (Greedy) only considers the immediate reward of the current step and easily falls into local optima. This task requires implementing a **Minimax algorithm with Alpha-Beta pruning** in `agents.py` to predict opponent actions through game tree search and formulate better strategies.

**Task Requirements**:

1. **Algorithm Implementation**: Implement the Minimax algorithm in the designated interface in `agents.py`.
* Must include **Alpha-Beta pruning** logic to improve search efficiency.
* Design a custom heuristic evaluation function (Heuristic Function), for example considering the total distance of pieces to the target area.


2. **Search Depth**: Set a reasonable search depth based on computational resources (recommended depth >= 3).
3. **Runtime Environment**: Code must run under the `triangle_size 2` configuration.
4. **Performance Requirement**:
* Submit `agents.py` code.
* **Win rate requirement**: In test matches against the built-in `Greedy` strategy, the **win rate must exceed 80%** after 20 games.


### 2. Context (Context Files)

* **Environment code**: `ChineseChecker/env/` directory, defining board layout, legal action generation (including consecutive jump rules), and win/loss determination.
* **Baseline code**: `RandomAgent` and `GreedyAgent` format references already present in `agents.py`.
* **Rule logic**:
* Movement: Move one cell or jump over adjacent pieces (consecutive jumps allowed).
* Victory: The first player to fully occupy the opponent's initial triangle area wins.


* **Execution command reference**: `python play.py --triangle_size 2`.
