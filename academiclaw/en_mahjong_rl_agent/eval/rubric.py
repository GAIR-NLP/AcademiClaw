"""
Scoring Rubric — Reinforcement Learning-Based Mahjong Agent Development and Implementation
Total Score: 100 points

Dimensions:
  I. Functional Correctness (30 pts)
    1.1 Python code files exist and are loadable        (8 pts)
    1.2 Inherits MahjongAgent and implements act()      (7 pts)
    1.3 Returns legal action for standard obs           (10 pts)
    1.4 All legal actions for multiple random obs       (5 pts)

  II. Algorithm Implementation (25 pts)
    2.1 RL / neural network component static check      (10 pts)
    2.2 State encoding/action space/reward design (LLM) (15 pts)

  III. Performance Evaluation (20 pts)
    Run games via embedded game environment, evaluate discard quality and results

  IV. Code Quality (15 pts)
    4.1 Syntax correct, no serious import errors        (5 pts)
    4.2 Code structure/comments/engineering (LLM)       (10 pts)

  V. Documentation Completeness (10 pts)
    5.1 README.md exists                                (3 pts)
    5.2 README content covers key sections (LLM)        (7 pts)
"""

import os
import sys
import json
import ast
import re
import importlib.util
import random
import traceback
from collections import Counter
from typing import Dict, List, Tuple, Any, Optional

try:
    import openai
except ImportError:
    openai = None


# ===================================================================
# Mahjong tile definitions
# ===================================================================

ALL_TILE_TYPES: List[str] = (
    [f"{s}{i}" for s in "BTM" for i in range(1, 10)]
    + ["E", "S", "W", "N", "P", "F", "D"]
)

TILE_TO_ID: Dict[str, int] = {t: i for i, t in enumerate(ALL_TILE_TYPES)}


# ===================================================================
# Mahjong game environment (evaluation-only, embedded in rubric)
# ===================================================================

def _generate_tiles() -> List[str]:
    tiles = []
    for t in ALL_TILE_TYPES:
        tiles += [t] * 4
    random.shuffle(tiles)
    return tiles


def _can_form_sets(counter: Counter) -> bool:
    if not counter:
        return True
    tile = next(iter(counter))
    if counter[tile] >= 3:
        counter[tile] -= 3
        if counter[tile] == 0:
            del counter[tile]
        if _can_form_sets(counter):
            return True
        counter[tile] = counter.get(tile, 0) + 3
    if len(tile) == 2 and tile[0] in "BTM":
        suit, num = tile[0], int(tile[1])
        if num <= 7:
            seq = [f"{suit}{num + i}" for i in range(3)]
            if all(counter.get(t, 0) >= 1 for t in seq):
                for t in seq:
                    counter[t] -= 1
                    if counter[t] == 0:
                        del counter[t]
                if _can_form_sets(counter):
                    return True
                for t in seq:
                    counter[t] = counter.get(t, 0) + 1
    return False


def _is_complete_hand(tiles: List[str]) -> bool:
    counter = Counter(tiles)
    for t in list(counter):
        if counter[t] >= 2:
            counter[t] -= 2
            if counter[t] == 0:
                del counter[t]
            if _can_form_sets(counter.copy()):
                return True
            counter[t] = counter.get(t, 0) + 2
    return False


def _shanten_approx(tiles: List[str]) -> int:
    """Rough estimate of Shanten number (used for discard quality evaluation)"""
    counter = Counter(tiles)
    melds = 0
    tmp = dict(counter)
    for t in list(tmp):
        while tmp.get(t, 0) >= 3:
            melds += 1
            tmp[t] -= 3
    pairs = sum(1 for c in tmp.values() if c >= 2)
    taatsu = 0
    for suit in "BTM":
        nums = sorted(set(int(t[1]) for t in tmp if len(t) == 2 and t[0] == suit and tmp.get(t, 0) > 0))
        i = 0
        while i < len(nums):
            if i + 1 < len(nums) and nums[i + 1] - nums[i] <= 2:
                taatsu += 1
                i += 2
            else:
                i += 1
    return max(0, 8 - melds * 2 - pairs - taatsu)


def _is_tenpai(tiles: List[str]) -> bool:
    return any(_is_complete_hand(tiles + [t]) for t in ALL_TILE_TYPES)


def _can_riichi_check(hand: List[str], melds: List[List[str]]) -> bool:
    full = hand + [x for m in melds for x in m]
    for d in set(hand):
        test = full.copy()
        test.remove(d)
        if _is_tenpai(test):
            return True
    return False


class _EvalPlayer:
    def __init__(self, pid: int, agent=None):
        self.pid = pid
        self.agent = agent
        self.hand: List[str] = []
        self.discards: List[str] = []
        self.melds: List[List[str]] = []
        self.riichi = False
        self.last_draw: Optional[str] = None

    def draw(self, tile: str):
        self.hand.append(tile)
        self.last_draw = tile

    def discard(self, tile: str) -> str:
        self.hand.remove(tile)
        self.discards.append(tile)
        return tile


class _EvalGame:
    """Simplified Mahjong game for evaluation"""

    def __init__(self, agent):
        self.tiles = _generate_tiles()
        self.players = [_EvalPlayer(0, agent)] + [_EvalPlayer(i) for i in range(1, 4)]
        self.dealer = random.randint(0, 3)
        self.turn = self.dealer
        self.first_turn = True
        self.game_over = False

        # Statistics
        self.total_actions = 0
        self.invalid_actions = 0
        self.action_quality_sum = 0
        self.agent_won = False
        self.agent_deal_in = False

        # Deal tiles
        for _ in range(13):
            for p in self.players:
                if self.tiles:
                    p.draw(self.tiles.pop())
        if self.tiles:
            self.players[self.dealer].draw(self.tiles.pop())

    def _get_obs(self, p: _EvalPlayer) -> Dict:
        return {
            "hand": p.hand.copy(),
            "melds": [m.copy() for m in p.melds],
            "riichi": p.riichi,
            "last_draw": p.last_draw,
            "can_riichi": _can_riichi_check(p.hand, p.melds) and not p.riichi,
            "other_players": [
                {
                    "pid": o.pid,
                    "discards": o.discards.copy(),
                    "melds": [m.copy() for m in o.melds],
                    "riichi": o.riichi,
                }
                for o in self.players if o != p
            ],
        }

    def _score_action(self, before: List[str], after: List[str], tile: str, obs: Dict) -> float:
        """Evaluate the quality of a single discard (0~60)"""
        sc = 0.0
        if tile not in before:
            return 0.0
        sc += 10  # Base score for legal discard

        s_before = _shanten_approx(before)
        s_after = _shanten_approx(after)
        if s_after < s_before:
            sc += 20  # Shanten decreased
        elif s_after == s_before:
            sc += 10  # Shanten maintained
        else:
            sc += 0   # Shanten increased

        # Preserve pair/triplet structure
        pairs_before = sum(1 for c in Counter(before).values() if c >= 2)
        pairs_after = sum(1 for c in Counter(after).values() if c >= 2)
        if pairs_after >= pairs_before:
            sc += 15
        else:
            sc += 5

        # Dangerous tile check
        danger = set()
        for p in obs.get("other_players", []):
            if p.get("riichi"):
                danger |= set(ALL_TILE_TYPES) - set(p.get("discards", []))
        if tile not in danger:
            sc += 15
        else:
            sc += 3

        return sc

    def step(self):
        if self.game_over:
            return
        p = self.players[self.turn]

        if not self.first_turn:
            if not self.tiles:
                self.game_over = True
                return
            draw_tile = self.tiles.pop()
            p.draw(draw_tile)
            # Self-draw win check
            if p.riichi and _is_complete_hand(p.hand):
                if p.agent:
                    self.agent_won = True
                self.game_over = True
                return
        self.first_turn = False

        obs = self._get_obs(p)

        # Get action
        if p.agent:
            try:
                action = p.agent.act(obs)
            except Exception:
                action = {"type": "discard", "tile": random.choice(p.hand)}
            self.total_actions += 1
        else:
            action = {"type": "discard", "tile": random.choice(p.hand)}

        tile = action.get("tile", "") if isinstance(action, dict) else ""
        action_type = action.get("type", "discard") if isinstance(action, dict) else "discard"

        if tile not in p.hand:
            if p.agent:
                self.invalid_actions += 1
            tile = random.choice(p.hand)

        if action_type == "riichi_discard":
            p.riichi = True

        before = p.hand.copy()
        p.discard(tile)
        after = p.hand.copy()

        if p.agent:
            self.action_quality_sum += self._score_action(before, after, tile, obs)

        # Check if other players win from this discard
        for o in self.players:
            if o.pid != p.pid and o.riichi:
                if _is_complete_hand(o.hand + [tile]):
                    if p.agent:
                        self.agent_deal_in = True
                    self.game_over = True
                    return

        self.turn = (self.turn + 1) % 4


# ===================================================================
# LLM-as-Judge helper functions
# ===================================================================

def _load_env(answer_dir: str) -> dict:
    values: Dict[str, str] = {}
    for env_dir in [answer_dir, os.path.join(os.path.dirname(__file__), "..")]:
        env_path = os.path.join(env_dir, ".env")
        if os.path.exists(env_path):
            try:
                with open(env_path, "r") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#") or "=" not in line:
                            continue
                        k, v = line.split("=", 1)
                        if k.strip() not in values:
                            values[k.strip()] = v.strip().strip("'\"")
            except Exception:
                pass
    return values


def _get_text_eval_config(answer_dir: str) -> dict:
    env = _load_env(answer_dir)
    def g(key, default=""):
        return os.environ.get(key) or env.get(key) or default
    return {
        "api_key": g("EVAL_TEXT_API_KEY", g("ANTHROPIC_API_KEY")),
        "api_base": g("EVAL_TEXT_API_BASE_URL", g("ANTHROPIC_BASE_URL")),
        "model": g("EVAL_TEXT_MODEL", "openai/gpt-5.2"),
    }


def _call_llm_judge(prompt: str, config: dict) -> str:
    if not openai or not config.get("api_key"):
        return ""
    try:
        base = config["api_base"].rstrip("/")
        if not base.endswith("/v1"):
            base += "/v1"
        client = openai.OpenAI(api_key=config["api_key"], base_url=base)
        resp = client.chat.completions.create(
            model=config["model"],
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2048,
            temperature=0,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        print(f"[RUBRIC] LLM Judge call failed: {e}")
        return ""


def _parse_llm_json(text: str) -> dict:
    if not text:
        return {}
    try:
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        return json.loads(text)
    except Exception:
        m = re.search(r"\{[^{}]*\}", text, re.DOTALL)
        if m:
            try:
                return json.loads(m.group())
            except Exception:
                pass
    return {}


# ===================================================================
# Agent loading
# ===================================================================

def _find_py_files(directory: str) -> List[str]:
    result = []
    if not os.path.isdir(directory):
        return result
    for f in os.listdir(directory):
        if f.endswith(".py") and f != "__init__.py":
            result.append(os.path.join(directory, f))
    return result


def _load_agent(answer_dir: str):
    """Try to load an Agent instance with an act() method from answer_dir.

    Returns: (agent_instance, error_message, agent_file_path)
    """
    py_files = _find_py_files(answer_dir)
    if not py_files:
        return None, "No .py files found", None

    # Add answer_dir and context to sys.path
    context_dir = os.path.join(os.path.dirname(__file__), "..", "context")
    for d in [answer_dir, context_dir]:
        d = os.path.abspath(d)
        if os.path.isdir(d) and d not in sys.path:
            sys.path.insert(0, d)

    errors = []

    # Prioritize files with agent/rl/dqn/ppo in the name
    priority_files = []
    other_files = []
    for fpath in py_files:
        fname = os.path.basename(fpath).lower()
        if any(kw in fname for kw in ("agent", "rl", "dqn", "ppo", "sac", "a3c")):
            priority_files.append(fpath)
        else:
            other_files.append(fpath)
    ordered_files = priority_files + other_files

    skip_names = {"MahjongAgent", "RandomAgent"}

    # First pass: find non-base, non-RandomAgent agents
    for fpath in ordered_files:
        try:
            spec = importlib.util.spec_from_file_location("_agent_mod", fpath)
            if spec is None or spec.loader is None:
                continue
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            for name in dir(mod):
                obj = getattr(mod, name)
                if not isinstance(obj, type):
                    continue
                if name in skip_names:
                    continue
                if hasattr(obj, "act") and callable(getattr(obj, "act", None)):
                    try:
                        instance = obj()
                        return instance, "", fpath
                    except Exception as e:
                        errors.append(f"Instantiation of {name} ({os.path.basename(fpath)}) failed: {e}")
        except Exception as e:
            errors.append(f"Loading {os.path.basename(fpath)} failed: {e}")

    # Second pass: relax conditions, find any class with act method (including RandomAgent)
    for fpath in ordered_files:
        try:
            spec = importlib.util.spec_from_file_location("_agent_mod2", fpath)
            if spec is None or spec.loader is None:
                continue
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            for name in dir(mod):
                obj = getattr(mod, name)
                if isinstance(obj, type) and hasattr(obj, "act") and name != "MahjongAgent":
                    try:
                        return obj(), "", fpath
                    except Exception:
                        pass
        except Exception:
            pass

    return None, "; ".join(errors) if errors else "No Agent class implementing act() found", None


# ===================================================================
# I. Functional Correctness (30 pts)
# ===================================================================

def _eval_functionality(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details: Dict[str, Any] = {}

    # 1.1 Code files exist (8 pts)
    py_files = _find_py_files(answer_dir)
    if py_files:
        score += 8
        details["1.1 code_files_exist"] = f"8/8 — Found {len(py_files)} .py file(s)"
    else:
        details["1.1 code_files_exist"] = "0/8 — No .py files found"
        details["1.2 agent_loading"] = "0/7 — Skipped"
        details["1.3 standard_action_test"] = "0/10 — Skipped"
        details["1.4 multi_round_random_test"] = "0/5 — Skipped"
        return score, details

    # 1.2 Inherits MahjongAgent and implements act (7 pts)
    agent, err, agent_file = _load_agent(answer_dir)
    if agent is not None:
        score += 7
        details["1.2 agent_loading"] = f"7/7 — Success ({os.path.basename(agent_file or '')})"
    else:
        details["1.2 agent_loading"] = f"0/7 — {err}"
        details["1.3 standard_action_test"] = "0/10 — Agent loading failed, skipped"
        details["1.4 multi_round_random_test"] = "0/5 — Skipped"
        return score, details

    # 1.3 Returns legal action for standard obs (10 pts)
    test_obs = {
        "hand": ["B1", "B2", "B3", "T1", "T2", "T3", "M5", "M6", "M7",
                 "E", "E", "S", "W"],
        "melds": [],
        "riichi": False,
        "last_draw": "W",
        "can_riichi": False,
        "other_players": [
            {"pid": 1, "discards": ["B5", "T8"], "melds": [], "riichi": False},
            {"pid": 2, "discards": ["M1"], "melds": [], "riichi": False},
            {"pid": 3, "discards": [], "melds": [], "riichi": False},
        ],
    }
    try:
        action = agent.act(test_obs)
        if not isinstance(action, dict):
            details["1.3 standard_action_test"] = f"0/10 — act() returned non-dict ({type(action).__name__})"
        elif "type" not in action or "tile" not in action:
            score += 2
            details["1.3 standard_action_test"] = f"2/10 — Returned dict missing type/tile: {action}"
        elif action["type"] not in ("discard", "riichi_discard"):
            score += 4
            details["1.3 standard_action_test"] = f"4/10 — Invalid type: {action['type']}"
        elif action["tile"] not in test_obs["hand"]:
            score += 5
            details["1.3 standard_action_test"] = f"5/10 — tile '{action['tile']}' not in hand"
        else:
            score += 10
            details["1.3 standard_action_test"] = f"10/10 — Legal action: {action}"
    except Exception as e:
        details["1.3 standard_action_test"] = f"0/10 — act() exception: {e}"

    # 1.4 Multi-round random obs test (5 pts)
    if agent is not None and score >= 15:
        ok_count = 0
        n_tests = 20
        for _ in range(n_tests):
            tiles = _generate_tiles()
            hand = tiles[:13]
            rnd_obs = {
                "hand": hand,
                "melds": [],
                "riichi": False,
                "last_draw": hand[-1],
                "can_riichi": False,
                "other_players": [
                    {"pid": i, "discards": tiles[13 + i * 3: 13 + (i + 1) * 3],
                     "melds": [], "riichi": False}
                    for i in range(1, 4)
                ],
            }
            try:
                a = agent.act(rnd_obs)
                if (isinstance(a, dict)
                        and a.get("tile") in hand
                        and a.get("type") in ("discard", "riichi_discard")):
                    ok_count += 1
            except Exception:
                pass
        pts = int(ok_count / n_tests * 5)
        score += pts
        details["1.4 multi_round_random_test"] = f"{pts}/5 — {ok_count}/{n_tests} legal"
    else:
        details["1.4 multi_round_random_test"] = "0/5 — Basic functionality not passed, skipped"

    return score, details


# ===================================================================
# II. Algorithm Implementation (25 pts)
# ===================================================================

RL_KEYWORDS = {
    "dqn": 2, "ppo": 2, "a3c": 2, "a2c": 2, "reinforce": 2,
    "actor.critic": 2, "sac": 2, "rainbow": 2, "ddpg": 2,
    "q.learning": 1, "q_learning": 1, "q_value": 1, "q_network": 1,
    "policy.gradient": 1, "experience.replay": 1, "replay.buffer": 1,
    "target.network": 1, "epsilon": 1, "exploration": 1,
    "bellman": 1, "temporal.difference": 1, "td.error": 1,
    "reward": 1, "discount": 1, "gamma": 1,
}

NN_KEYWORDS = {
    "nn.module": 2, "nn.linear": 2, "nn.conv": 1, "nn.lstm": 1, "nn.gru": 1,
    "forward": 1, "backward": 1, "optimizer": 1, "loss": 1,
    "torch": 1, "tensorflow": 1, "keras": 1,
    "state_dim": 1, "action_dim": 1, "hidden": 1,
}


def _eval_algorithm(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details: Dict[str, Any] = {}

    # Collect all code
    all_code = ""
    for fpath in _find_py_files(answer_dir):
        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                all_code += "\n" + f.read()
        except Exception:
            pass

    if not all_code.strip():
        details["2.1 rl_component_check"] = "0/10 — No code content"
        details["2.2 algorithm_design_llm"] = "0/15 — Skipped"
        return 0, details

    code_lower = all_code.lower()

    # 2.1 Static keyword check (10 pts)
    rl_pts = 0
    rl_found = []
    for kw, pt in RL_KEYWORDS.items():
        pattern = kw.replace(".", r"[\s_\-.]?")
        if re.search(pattern, code_lower):
            rl_pts += pt
            rl_found.append(kw)

    nn_pts = 0
    nn_found = []
    for kw, pt in NN_KEYWORDS.items():
        pattern = kw.replace(".", r"[\s_\-.]?")
        if re.search(pattern, code_lower):
            nn_pts += pt
            nn_found.append(kw)

    component_score = min(10, rl_pts + nn_pts)
    if rl_pts == 0 and nn_pts == 0:
        component_score = 0
    elif rl_pts == 0:
        component_score = min(component_score, 3)  # Has NN but no RL
    elif nn_pts == 0:
        component_score = min(component_score, 5)  # Has RL but no NN

    score += component_score
    details["2.1 rl_component_check"] = (
        f"{component_score}/10 — RL: {rl_found[:6]}, NN: {nn_found[:6]}"
    )

    # 2.2 Algorithm design soundness — LLM-as-Judge (15 pts)
    agent_code_snippet = ""
    for fpath in _find_py_files(answer_dir):
        fname = os.path.basename(fpath).lower()
        if any(kw in fname for kw in ("agent", "rl", "dqn", "ppo")):
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    agent_code_snippet = "".join(f.readlines()[:250])
            except Exception:
                pass
            break
    if not agent_code_snippet:
        for fpath in _find_py_files(answer_dir):
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    agent_code_snippet = "".join(f.readlines()[:250])
            except Exception:
                pass
            break

    llm_config = _get_text_eval_config(answer_dir)
    algo_prompt = f"""\
You are a reinforcement learning algorithm evaluation expert. Below is a student's implementation of a Mahjong RL agent.

Please score on the following three dimensions (0-5 each), and return JSON:

1. **state_encoding** (0-5): Is the state encoding reasonable?
   - 5: Multi-channel encoding (hand + seen tiles + game state info), information-rich
   - 3: Basic hand count encoding (34-dim)
   - 1: Very coarse
   - 0: No state encoding

2. **action_space** (0-5): Is the action space design reasonable?
   - 5: 34-dim action space + legal action mask
   - 3: Has action space design but masking is incomplete
   - 1: Directly picks randomly from hand
   - 0: No action space design

3. **rl_algorithm** (0-5): Is the RL algorithm implementation complete?
   - 5: Complete DQN/PPO etc., with network, loss function, update logic
   - 3: Has network definition but training logic is incomplete
   - 1: Framework only, core logic missing
   - 0: Pure rule-based strategy, no RL component

Please strictly return only:
```json
{{"state_encoding": 0, "action_space": 0, "rl_algorithm": 0, "comment": ""}}
```

Code:
```python
{agent_code_snippet[:6000]}
```"""

    llm_raw = _call_llm_judge(algo_prompt, llm_config)
    llm_result = _parse_llm_json(llm_raw)

    if llm_result:
        se = max(0, min(5, int(llm_result.get("state_encoding", 0))))
        asp = max(0, min(5, int(llm_result.get("action_space", 0))))
        rla = max(0, min(5, int(llm_result.get("rl_algorithm", 0))))
        algo_llm_score = se + asp + rla
        score += algo_llm_score
        details["2.2 algorithm_design_llm"] = (
            f"{algo_llm_score}/15 — state_encoding:{se}/5, action_space:{asp}/5, rl_algorithm:{rla}/5"
            f" | {llm_result.get('comment', '')[:120]}"
        )
    else:
        fallback = min(8, component_score)
        score += fallback
        details["2.2 algorithm_design_llm"] = f"{fallback}/15 — LLM unavailable, conservative score based on static analysis"

    return score, details


# ===================================================================
# III. Performance Evaluation (20 pts)
# ===================================================================

def _eval_performance(answer_dir: str) -> Tuple[int, dict]:
    details: Dict[str, Any] = {}

    agent, err, _ = _load_agent(answer_dir)
    if agent is None:
        details["performance_evaluation"] = f"0/20 — Agent cannot be loaded: {err}"
        return 0, details

    num_games = 10
    total_action_quality = 0.0
    total_invalid = 0
    total_actions = 0
    wins = 0
    deal_ins = 0

    for _ in range(num_games):
        game = _EvalGame(agent)
        steps = 0
        while not game.game_over and steps < 200:
            game.step()
            steps += 1
        total_action_quality += min(60.0, game.action_quality_sum)
        total_invalid += game.invalid_actions
        total_actions += game.total_actions
        if game.agent_won:
            wins += 1
        if game.agent_deal_in:
            deal_ins += 1

    avg_action = total_action_quality / max(1, num_games)
    invalid_rate = total_invalid / max(1, total_actions)

    # Discard quality (12 pts): avg_action max 60, mapped to 12 pts
    action_pts = min(12, int(avg_action / 60 * 12))

    # Game results (8 pts)
    # Win bonus (each win +2, max 4 pts)
    win_pts = min(4, wins * 2)
    # No deal-in bonus (fewer deal-ins in 10 games -> higher score)
    safe_pts = 4 if deal_ins == 0 else (2 if deal_ins <= 2 else 0)
    result_pts = win_pts + safe_pts

    # Illegal action penalty
    penalty = 0
    if invalid_rate > 0.5:
        penalty = 6
    elif invalid_rate > 0.3:
        penalty = 4
    elif invalid_rate > 0.1:
        penalty = 2

    total_pts = max(0, action_pts + result_pts - penalty)
    total_pts = min(20, total_pts)

    details["discard_quality"] = f"{action_pts}/12 — Average action quality: {avg_action:.1f}/60"
    details["game_results"] = f"{result_pts}/8 — Won {wins} game(s)(+{win_pts}), dealt in {deal_ins} time(s)(safe+{safe_pts})"
    details["illegal_actions"] = f"Rate {invalid_rate*100:.1f}% ({total_invalid}/{total_actions})"
    if penalty > 0:
        details["illegal_action_penalty"] = f"-{penalty} pts"
    details["total"] = f"{total_pts}/20"

    return total_pts, details


# ===================================================================
# IV. Code Quality (15 pts)
# ===================================================================

def _eval_code_quality(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details: Dict[str, Any] = {}

    py_files = _find_py_files(answer_dir)
    if not py_files:
        details["4.1 syntax_check"] = "0/5 — No .py files"
        details["4.2 code_quality_llm"] = "0/10 — Skipped"
        return 0, details

    # 4.1 Syntax check (5 pts)
    syntax_errors = []
    for fpath in py_files:
        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                code = f.read()
            ast.parse(code)
        except SyntaxError as e:
            syntax_errors.append(f"{os.path.basename(fpath)}: {e.msg}")

    if not syntax_errors:
        score += 5
        details["4.1 syntax_check"] = f"5/5 — All {len(py_files)} file(s) passed"
    elif len(syntax_errors) == 1:
        score += 3
        details["4.1 syntax_check"] = f"3/5 — {syntax_errors[0]}"
    else:
        score += 1
        details["4.1 syntax_check"] = f"1/5 — Multiple syntax errors: {syntax_errors[:3]}"

    # 4.2 Code quality LLM evaluation (10 pts)
    agent_code = ""
    for fpath in py_files:
        fname = os.path.basename(fpath).lower()
        if any(kw in fname for kw in ("agent", "rl")):
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    agent_code = f.read()
            except Exception:
                pass
            break
    if not agent_code and py_files:
        try:
            with open(py_files[0], "r", encoding="utf-8", errors="ignore") as f:
                agent_code = f.read()
        except Exception:
            pass

    if not agent_code:
        details["4.2 code_quality_llm"] = "0/10 — Cannot read code"
        return score, details

    llm_config = _get_text_eval_config(answer_dir)
    quality_prompt = f"""\
You are a code quality review expert. Below is a Python implementation of a Mahjong RL agent.
Please score on two dimensions (0-5), return JSON:

1. **structure** (0-5): Code structure clarity, modularity, separation of concerns
   - 5: Excellent structure, clearly modular
   - 3: Acceptable structure
   - 1: Messy code
   - 0: Incomprehensible

2. **engineering** (0-5): Engineering standards, comments, error handling
   - 5: Thorough comments, complete type hints, error handling present
   - 3: Basic comments and error handling
   - 1: Almost no comments
   - 0: None at all

Please strictly return:
```json
{{"structure": 0, "engineering": 0, "comment": ""}}
```

Code:
```python
{agent_code[:6000]}
```"""

    llm_raw = _call_llm_judge(quality_prompt, llm_config)
    llm_result = _parse_llm_json(llm_raw)

    if llm_result:
        st = max(0, min(5, int(llm_result.get("structure", 0))))
        eng = max(0, min(5, int(llm_result.get("engineering", 0))))
        q_score = st + eng
        score += q_score
        details["4.2 code_quality_llm"] = (
            f"{q_score}/10 — structure:{st}/5, engineering:{eng}/5"
            f" | {llm_result.get('comment', '')[:120]}"
        )
    else:
        lines = agent_code.split("\n")
        total_lines = len(lines)
        comment_lines = sum(
            1 for ln in lines
            if ln.strip().startswith("#") or ln.strip().startswith('"""') or ln.strip().startswith("'''")
        )
        ratio = comment_lines / max(1, total_lines)
        fallback = 4 if ratio > 0.08 else (2 if ratio > 0.03 else 1)
        score += fallback
        details["4.2 code_quality_llm"] = (
            f"{fallback}/10 — LLM unavailable, comment ratio {ratio:.1%}, conservative score"
        )

    return score, details


# ===================================================================
# V. Documentation Completeness (10 pts)
# ===================================================================

def _eval_documentation(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details: Dict[str, Any] = {}

    # 5.1 README.md exists (3 pts)
    readme_path = None
    for name in ("README.md", "readme.md", "Readme.md", "README.MD"):
        p = os.path.join(answer_dir, name)
        if os.path.exists(p):
            readme_path = p
            break

    if readme_path is None:
        md_files = [
            f for f in os.listdir(answer_dir)
            if f.lower().endswith(".md") and os.path.isfile(os.path.join(answer_dir, f))
        ]
        if md_files:
            score += 1
            readme_path = os.path.join(answer_dir, md_files[0])
            details["5.1 readme_exists"] = f"1/3 — Non-standard .md: {md_files[0]}"
        else:
            details["5.1 readme_exists"] = "0/3 — README.md not found"
            details["5.2 content_coverage_llm"] = "0/7 — Skipped"
            return score, details
    else:
        score += 3
        details["5.1 readme_exists"] = "3/3 — README.md exists"

    try:
        with open(readme_path, "r", encoding="utf-8", errors="ignore") as f:
            readme_content = f.read()
    except Exception:
        details["5.2 content_coverage_llm"] = "0/7 — Cannot read"
        return score, details

    if len(readme_content.strip()) < 50:
        details["5.2 content_coverage_llm"] = "0/7 — Document too short (< 50 characters)"
        return score, details

    # 5.2 LLM evaluation (7 pts)
    llm_config = _get_text_eval_config(answer_dir)
    doc_prompt = f"""\
You are a technical documentation review expert. Below is a README for a reinforcement learning-based Mahjong agent project.
The project requires documentation covering: (1) Algorithm description (2) State/action/reward design (3) Model architecture (4) Training method and parameters (5) Running guide (6) Dependency list.

Please evaluate coverage and quality, return JSON (0-7 score):
- 7: Covers all 6 aspects, detailed and clear
- 5-6: Covers 4-5 aspects
- 3-4: Covers 2-3 aspects
- 1-2: Only basic description
- 0: No useful content

```json
{{"doc_score": 0, "covered_sections": [], "missing_sections": [], "comment": ""}}
```

Document:
{readme_content[:4000]}"""

    llm_raw = _call_llm_judge(doc_prompt, llm_config)
    llm_result = _parse_llm_json(llm_raw)

    if llm_result:
        doc_score = max(0, min(7, int(llm_result.get("doc_score", 0))))
        score += doc_score
        covered = llm_result.get("covered_sections", [])
        missing = llm_result.get("missing_sections", [])
        details["5.2 content_coverage_llm"] = (
            f"{doc_score}/7 — Covered: {covered[:5]}, Missing: {missing[:5]}"
        )
    else:
        keywords = [
            "algorithm", "state", "action",
            "reward", "train", "require",
            "install", "run", "network",
        ]
        found = sum(1 for kw in keywords if kw in readme_content.lower())
        fallback = min(4, found // 2)
        score += fallback
        details["5.2 content_coverage_llm"] = (
            f"{fallback}/7 — LLM unavailable, {found} keywords found, conservative score"
        )

    return score, details


# ===================================================================
# Main evaluation function
# ===================================================================

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Evaluate the agent's output.

    Args:
        answer_dir: absolute path to the agent output directory

    Returns:
        (score, report)
        - score: integer 0-100
        - report: dict containing detailed evaluation report
    """
    report: Dict[str, Any] = {}

    # I. Functional Correctness (30 pts)
    s1, d1 = _eval_functionality(answer_dir)
    report["I_functional_correctness_30pts"] = {"score": s1, "details": d1}

    # II. Algorithm Implementation (25 pts)
    s2, d2 = _eval_algorithm(answer_dir)
    report["II_algorithm_implementation_25pts"] = {"score": s2, "details": d2}

    # III. Performance Evaluation (20 pts) — only run if basic functionality passes
    if s1 >= 15:
        try:
            s3, d3 = _eval_performance(answer_dir)
        except Exception as e:
            s3 = 0
            d3 = {"error": f"Performance evaluation exception: {traceback.format_exc()[:300]}"}
    else:
        s3 = 0
        d3 = {"skipped": "Functional correctness score < 15, skipping performance evaluation"}
    report["III_performance_evaluation_20pts"] = {"score": s3, "details": d3}

    # IV. Code Quality (15 pts)
    s4, d4 = _eval_code_quality(answer_dir)
    report["IV_code_quality_15pts"] = {"score": s4, "details": d4}

    # V. Documentation Completeness (10 pts)
    s5, d5 = _eval_documentation(answer_dir)
    report["V_documentation_completeness_10pts"] = {"score": s5, "details": d5}

    total = s1 + s2 + s3 + s4 + s5

    if total >= 85:
        comment = "Excellent: Agent implementation is complete, algorithm is sound, performance is outstanding"
    elif total >= 65:
        comment = "Good: Basic functionality is complete, some dimensions have room for improvement"
    elif total >= 45:
        comment = "Passing: Can run but has notable deficiencies"
    else:
        comment = "Failing: Implementation is incomplete or has serious issues"

    report["total_score"] = total
    report["comment"] = comment
    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print a formatted scoring report"""
    print("\n" + "=" * 65)
    print("  Reinforcement Learning Mahjong Agent — Evaluation Report")
    print("=" * 65)

    sections = [
        "I_functional_correctness_30pts",
        "II_algorithm_implementation_25pts",
        "III_performance_evaluation_20pts",
        "IV_code_quality_15pts",
        "V_documentation_completeness_10pts",
    ]
    for key in sections:
        section = report.get(key, {})
        sec_score = section.get("score", 0)
        print(f"\n[{key}] Score: {sec_score}")
        for k, v in section.get("details", {}).items():
            print(f"  {k}: {v}")

    print(f"\n{'=' * 65}")
    print(f"  Total Score: {score}/100")
    print(f"  Comment: {report.get('comment', '')}")
    print("=" * 65)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_dir = sys.argv[1]
    else:
        test_dir = "."

    if not os.path.isabs(test_dir):
        test_dir = os.path.join(os.path.dirname(__file__), "..", test_dir)

    test_dir = os.path.abspath(test_dir)
    print(f"Evaluating directory: {test_dir}")
    s, r = evaluate(test_dir)
    print_report(s, r)
    sys.exit(0)
