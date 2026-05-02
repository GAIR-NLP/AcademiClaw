"""
Graph Algorithms Task — Evaluation Rubric
Task: Implement graph algorithms for network analysis

Total: 100 points

Scoring Dimensions:
  1. File Delivery          (10 pts) — algorithms.py (5) + performance_report.txt (5)
  2. Code Loadability       (10 pts) — algorithms.py imports without error, 5 functions callable (2 each)
  3. Algorithm Correctness  (60 pts) — run test cases against each algorithm (12 each)
  4. Performance Report     (10 pts) — mentions all 5 algorithms, reasonable length and content
  5. Code Documentation     (10 pts) — LLM-as-Judge evaluates docstrings, comments, complexity analysis
"""

import os
import sys
import re
import math
import json
import importlib.util
from typing import Tuple, Dict, Any, List, Optional

try:
    import openai
except ImportError:
    openai = None

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

QUERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REQUIRED_FILES = ["algorithms.py", "performance_report.txt"]

EXPECTED_FUNCTIONS = [
    "dijkstra",
    "bellman_ford",
    "floyd_warshall",
    "kruskal_mst",
    "topological_sort",
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _load_module(name: str, path: str):
    """Dynamically load a Python module from a file path."""
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _dicts_close(d1: dict, d2: dict, rel_tol: float = 1e-6, abs_tol: float = 1e-6) -> bool:
    """Check if two dicts of numeric values are close."""
    if set(d1.keys()) != set(d2.keys()):
        return False
    for k in d1:
        v1, v2 = d1[k], d2[k]
        if v1 == float("inf") or v2 == float("inf"):
            if v1 != v2:
                return False
        else:
            if not math.isclose(v1, v2, rel_tol=rel_tol, abs_tol=abs_tol):
                return False
    return True


def _load_env(answer_dir: str) -> dict:
    """Load .env configuration from answer_dir and query root."""
    values = {}
    for env_dir in [answer_dir, QUERY_ROOT]:
        env_path = os.path.join(env_dir, ".env")
        if os.path.exists(env_path):
            with open(env_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    if k.strip() not in values:
                        values[k.strip()] = v.strip().strip("'\"")
    return values


def _get_text_eval_config(answer_dir: str) -> dict:
    """Get text evaluation LLM configuration."""
    env = _load_env(answer_dir)

    def g(key, default=""):
        return os.environ.get(key) or env.get(key) or default

    return {
        "api_key": g("EVAL_TEXT_API_KEY", g("ANTHROPIC_API_KEY")),
        "api_base": g("EVAL_TEXT_API_BASE_URL", g("ANTHROPIC_BASE_URL")),
        "model": g("EVAL_TEXT_MODEL", "openai/gpt-5.2"),
    }


def _call_llm_judge(prompt: str, config: dict) -> str:
    """Call LLM for text evaluation."""
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


# ---------------------------------------------------------------------------
# Graph class & test data (embedded for self-containment)
# ---------------------------------------------------------------------------


def _get_graph_class():
    """Load the Graph class from context/graph.py."""
    graph_path = os.path.join(QUERY_ROOT, "context", "graph.py")
    if not os.path.exists(graph_path):
        graph_path = os.path.join(os.path.dirname(__file__), "graph.py")
    if not os.path.exists(graph_path):
        return None
    mod = _load_module("_rubric_graph_mod", graph_path)
    return mod.Graph


def _create_small_undirected_graph(Graph):
    """Small undirected graph with 5 vertices and 7 edges."""
    g = Graph(directed=False)
    for u, v, w in [
        (0, 1, 4), (0, 2, 1), (1, 2, 2),
        (1, 3, 5), (2, 3, 8), (2, 4, 10),
        (3, 4, 2),
    ]:
        g.add_edge(u, v, w)
    return g


def _create_negative_edge_graph(Graph):
    """Directed graph with negative edges for Bellman-Ford."""
    g = Graph(directed=True)
    for u, v, w in [
        (0, 1, 5), (0, 2, 4),
        (1, 3, 3), (2, 1, 6),
        (3, 2, -2),
    ]:
        g.add_edge(u, v, w)
    return g


def _create_dag(Graph):
    """DAG with 6 vertices for topological sort."""
    g = Graph(directed=True)
    for u, v in [(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1)]:
        g.add_edge(u, v)
    return g


# Expected shortest-path distances for the small undirected graph
EXPECTED_DIJKSTRA = {
    0: {0: 0, 1: 3, 2: 1, 3: 8, 4: 10},
    1: {1: 0, 0: 3, 2: 2, 3: 5, 4: 7},
    2: {2: 0, 0: 1, 1: 2, 3: 7, 4: 9},
    3: {3: 0, 1: 5, 0: 8, 2: 7, 4: 2},
    4: {4: 0, 3: 2, 1: 7, 0: 10, 2: 9},
}

# Expected shortest-path distances for the negative-edge directed graph
EXPECTED_BELLMAN_FORD = {
    0: {0: 0, 1: 5, 2: 4, 3: 8},
    1: {0: float("inf"), 1: 0, 2: 1, 3: 3},
    2: {0: float("inf"), 1: 6, 2: 0, 3: 9},
    3: {0: float("inf"), 1: 4, 2: -2, 3: 0},
}

# Expected MST total weight for the small undirected graph
EXPECTED_MST_WEIGHT = 10.0


# ===========================================================================
# Dimension 1: File Delivery (10 pts)
# ===========================================================================


def _check_files(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details = {}
    for fname, pts in [("algorithms.py", 5), ("performance_report.txt", 5)]:
        path = os.path.join(answer_dir, fname)
        if os.path.isfile(path):
            score += pts
            details[fname] = f"{pts}/{pts} - present"
        else:
            details[fname] = f"0/{pts} - MISSING"
    return score, details


# ===========================================================================
# Dimension 2: Code Loadability (10 pts)
# ===========================================================================


def _check_loadability(answer_dir: str) -> Tuple[int, dict, Any]:
    """Check algorithms.py can be imported and has all 5 required functions.
    Returns (score, details, loaded_module_or_None)."""
    algo_path = os.path.join(answer_dir, "algorithms.py")
    if not os.path.isfile(algo_path):
        return 0, {"error": "algorithms.py not found"}, None

    # Ensure import paths work for both `from context.graph import Graph`
    # and `from graph import Graph` patterns
    for p in [answer_dir, QUERY_ROOT]:
        if p not in sys.path:
            sys.path.insert(0, p)

    try:
        mod = _load_module("_student_algorithms", algo_path)
    except Exception as e:
        return 0, {"error": f"Failed to import algorithms.py: {e}"}, None

    score = 0
    details = {}
    per_fn = 2  # 2 pts each, 5 functions = 10 pts
    for fn_name in EXPECTED_FUNCTIONS:
        fn = getattr(mod, fn_name, None)
        if callable(fn):
            score += per_fn
            details[fn_name] = f"{per_fn}/{per_fn} - callable"
        else:
            details[fn_name] = f"0/{per_fn} - not found or not callable"
    return score, details, mod


# ===========================================================================
# Dimension 3: Algorithm Correctness (60 pts — 12 per algorithm)
# ===========================================================================


def _test_dijkstra(mod, Graph) -> Tuple[int, str]:
    fn = getattr(mod, "dijkstra", None)
    if not callable(fn):
        return 0, "not implemented"
    g = _create_small_undirected_graph(Graph)
    for src, expected in EXPECTED_DIJKSTRA.items():
        try:
            res = fn(g, src)
        except Exception as e:
            return 0, f"error on source {src}: {e}"
        dist = res[0] if isinstance(res, tuple) else res
        if not isinstance(dist, dict) or not _dicts_close(dist, expected):
            return 0, f"wrong result for source {src}"
    return 12, "all sources correct"


def _test_bellman_ford(mod, Graph) -> Tuple[int, str]:
    fn = getattr(mod, "bellman_ford", None)
    if not callable(fn):
        return 0, "not implemented"
    g = _create_negative_edge_graph(Graph)
    for src, expected in EXPECTED_BELLMAN_FORD.items():
        try:
            res = fn(g, src)
        except Exception as e:
            return 0, f"error on source {src}: {e}"
        dist = res[0] if isinstance(res, tuple) else res
        if not isinstance(dist, dict) or not _dicts_close(dist, expected):
            return 0, f"wrong result for source {src}"
    return 12, "all sources correct"


def _test_floyd_warshall(mod, Graph) -> Tuple[int, str]:
    fn = getattr(mod, "floyd_warshall", None)
    if not callable(fn):
        return 0, "not implemented"
    g = _create_small_undirected_graph(Graph)
    try:
        res = fn(g)
    except Exception as e:
        return 0, f"error: {e}"
    dist_all = res[0] if isinstance(res, tuple) else res
    if not isinstance(dist_all, dict):
        return 0, "result is not a dict"
    for src, expected in EXPECTED_DIJKSTRA.items():
        row = dist_all.get(src)
        if row is None or not _dicts_close(row, expected):
            return 0, f"wrong result for source {src}"
    return 12, "all-pairs correct"


def _test_kruskal(mod, Graph) -> Tuple[int, str]:
    fn = getattr(mod, "kruskal_mst", None)
    if not callable(fn):
        return 0, "not implemented"
    g = _create_small_undirected_graph(Graph)
    try:
        res = fn(g)
    except Exception as e:
        return 0, f"error: {e}"

    weight = None
    if isinstance(res, tuple) and len(res) >= 2:
        weight = float(res[1])
    elif isinstance(res, list):
        w = 0.0
        for edge in res:
            if len(edge) >= 3:
                w += float(edge[2])
        weight = w
    elif isinstance(res, (int, float)):
        weight = float(res)

    if weight is None:
        return 0, "could not extract MST weight from return value"
    if not math.isclose(weight, EXPECTED_MST_WEIGHT, rel_tol=1e-6, abs_tol=1e-6):
        return 0, f"wrong MST weight: expected {EXPECTED_MST_WEIGHT}, got {weight}"

    # Also verify MST has correct number of edges (V-1)
    if isinstance(res, tuple) and len(res) >= 1 and isinstance(res[0], list):
        edge_count = len(res[0])
        expected_edges = g.vertex_count() - 1
        if edge_count != expected_edges:
            return 8, f"weight correct but wrong edge count: {edge_count} (expected {expected_edges})"

    return 12, f"MST weight correct ({weight})"


def _test_topological_sort(mod, Graph) -> Tuple[int, str]:
    fn = getattr(mod, "topological_sort", None)
    if not callable(fn):
        return 0, "not implemented"
    g = _create_dag(Graph)
    try:
        res = fn(g)
    except Exception as e:
        return 0, f"error: {e}"

    if res is None:
        return 0, "returned None"
    if not isinstance(res, list):
        try:
            res = list(res)
        except Exception:
            return 0, "result not iterable"

    if len(res) != g.vertex_count():
        return 0, f"wrong length: expected {g.vertex_count()}, got {len(res)}"

    # Verify topological ordering: for every edge u->v, pos(u) < pos(v)
    pos = {v: i for i, v in enumerate(res)}
    for u, v, _ in g.get_edges():
        if u in pos and v in pos and pos[u] >= pos[v]:
            return 0, f"edge {u}->{v} violates topological order"
    return 12, "valid topological order"


def _check_correctness(mod, Graph) -> Tuple[int, dict]:
    score = 0
    details = {}
    tests = [
        ("dijkstra", _test_dijkstra),
        ("bellman_ford", _test_bellman_ford),
        ("floyd_warshall", _test_floyd_warshall),
        ("kruskal_mst", _test_kruskal),
        ("topological_sort", _test_topological_sort),
    ]
    for name, test_fn in tests:
        try:
            pts, msg = test_fn(mod, Graph)
        except Exception as e:
            pts, msg = 0, f"unexpected error: {e}"
        score += pts
        details[name] = f"{pts}/12 - {msg}"
    return score, details


# ===========================================================================
# Dimension 4: Performance Report (10 pts)
# ===========================================================================


def _check_report(answer_dir: str) -> Tuple[int, dict]:
    report_path = os.path.join(answer_dir, "performance_report.txt")
    if not os.path.isfile(report_path):
        return 0, {"error": "performance_report.txt not found"}

    try:
        with open(report_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
    except Exception as e:
        return 0, {"error": f"cannot read: {e}"}

    lower = content.lower()
    score = 0
    details = {}

    # 4a. Mentions each algorithm (1 pt each = 5 pts)
    algo_keywords = [
        ("dijkstra", "dijkstra"),
        ("bellman_ford", "bellman"),
        ("floyd_warshall", "floyd"),
        ("kruskal", "kruskal"),
        ("topological_sort", "topological"),
    ]
    mention_score = 0
    for label, keyword in algo_keywords:
        if keyword in lower:
            mention_score += 1
            details[f"mentions_{label}"] = "1/1"
        else:
            details[f"mentions_{label}"] = "0/1 - not mentioned"
    score += mention_score

    # 4b. Reasonable length (3 pts)
    word_count = len(content.split())
    if word_count >= 100:
        score += 3
        details["length"] = f"3/3 - {word_count} words"
    elif word_count >= 50:
        score += 2
        details["length"] = f"2/3 - {word_count} words (somewhat short)"
    elif word_count >= 20:
        score += 1
        details["length"] = f"1/3 - {word_count} words (short)"
    else:
        details["length"] = f"0/3 - {word_count} words (too short)"

    # 4c. Contains performance/complexity discussion (2 pts)
    has_numbers = bool(re.search(r"\d+\.\d+", content))
    perf_words = ["time", "complexity", "o(", "performance", "second", "ms",
                  "benchmark", "runtime", "efficient", "asymptotic"]
    has_perf_words = any(w in lower for w in perf_words)
    if has_numbers and has_perf_words:
        score += 2
        details["perf_data"] = "2/2 - contains numeric data and performance discussion"
    elif has_numbers or has_perf_words:
        score += 1
        details["perf_data"] = "1/2 - partial performance data"
    else:
        details["perf_data"] = "0/2 - no performance data found"

    return score, details


# ===========================================================================
# Dimension 5: Code Documentation (10 pts) — LLM-as-Judge
# ===========================================================================


_DOC_EVAL_PROMPT = """\
You are a strict code documentation evaluator. You will be given a Python file \
implementing graph algorithms (Dijkstra, Bellman-Ford, Floyd-Warshall, Kruskal MST, \
Topological Sort).

Evaluate the code's documentation quality on these criteria:

1. **Docstrings** (0-3 pts): Do functions have clear docstrings explaining parameters, \
return values, and behavior?
2. **Time Complexity Comments** (0-4 pts): Does the code include time complexity \
analysis (Big-O notation) for each algorithm? The task explicitly requires this.
3. **Inline Comments** (0-3 pts): Are there helpful inline comments explaining \
non-obvious logic?

Score each criterion strictly. Respond ONLY with a JSON object:
```json
{
  "docstrings": {"score": 0, "reason": ""},
  "complexity_comments": {"score": 0, "reason": ""},
  "inline_comments": {"score": 0, "reason": ""},
  "total": 0
}
```

Here is the code:

```python
%s
```
"""


def _check_documentation(answer_dir: str) -> Tuple[int, dict]:
    algo_path = os.path.join(answer_dir, "algorithms.py")
    if not os.path.isfile(algo_path):
        return 0, {"error": "algorithms.py not found"}

    try:
        with open(algo_path, "r", encoding="utf-8", errors="replace") as f:
            code = f.read()
    except Exception as e:
        return 0, {"error": f"cannot read: {e}"}

    config = _get_text_eval_config(answer_dir)
    prompt = _DOC_EVAL_PROMPT % code[:8000]  # limit code length
    raw = _call_llm_judge(prompt, config)

    if not raw:
        # Fallback: basic heuristic checks
        return _fallback_doc_check(code)

    try:
        # Parse JSON from LLM response
        text = raw
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        result = json.loads(text)
        doc_score = max(0, min(3, int(result.get("docstrings", {}).get("score", 0))))
        comp_score = max(0, min(4, int(result.get("complexity_comments", {}).get("score", 0))))
        inline_score = max(0, min(3, int(result.get("inline_comments", {}).get("score", 0))))
        total = doc_score + comp_score + inline_score
        details = {
            "docstrings": f"{doc_score}/3 - {result.get('docstrings', {}).get('reason', '')}",
            "complexity_comments": f"{comp_score}/4 - {result.get('complexity_comments', {}).get('reason', '')}",
            "inline_comments": f"{inline_score}/3 - {result.get('inline_comments', {}).get('reason', '')}",
            "eval_method": "LLM-as-Judge",
        }
        return total, details
    except (json.JSONDecodeError, ValueError, TypeError):
        return _fallback_doc_check(code)


def _fallback_doc_check(code: str) -> Tuple[int, dict]:
    """Heuristic fallback when LLM is unavailable."""
    score = 0
    details = {}

    # Docstrings: count triple-quoted strings
    docstring_count = code.count('"""') // 2 + code.count("'''") // 2
    if docstring_count >= 5:
        score += 3
        details["docstrings"] = f"3/3 - {docstring_count} docstrings found"
    elif docstring_count >= 3:
        score += 2
        details["docstrings"] = f"2/3 - {docstring_count} docstrings found"
    elif docstring_count >= 1:
        score += 1
        details["docstrings"] = f"1/3 - {docstring_count} docstrings found"
    else:
        details["docstrings"] = "0/3 - no docstrings"

    # Complexity comments: look for O(...) patterns
    complexity_matches = re.findall(r"O\([^)]+\)", code)
    if len(complexity_matches) >= 4:
        score += 4
        details["complexity_comments"] = f"4/4 - {len(complexity_matches)} complexity annotations"
    elif len(complexity_matches) >= 2:
        score += 2
        details["complexity_comments"] = f"2/4 - {len(complexity_matches)} complexity annotations"
    elif len(complexity_matches) >= 1:
        score += 1
        details["complexity_comments"] = f"1/4 - {len(complexity_matches)} complexity annotations"
    else:
        details["complexity_comments"] = "0/4 - no complexity annotations"

    # Inline comments
    comment_lines = [line for line in code.split("\n") if line.strip().startswith("#")]
    if len(comment_lines) >= 10:
        score += 3
        details["inline_comments"] = f"3/3 - {len(comment_lines)} comment lines"
    elif len(comment_lines) >= 5:
        score += 2
        details["inline_comments"] = f"2/3 - {len(comment_lines)} comment lines"
    elif len(comment_lines) >= 2:
        score += 1
        details["inline_comments"] = f"1/3 - {len(comment_lines)} comment lines"
    else:
        details["inline_comments"] = "0/3 - very few comments"

    details["eval_method"] = "heuristic fallback (LLM unavailable)"
    return score, details


# ===========================================================================
# Main Entry Points
# ===========================================================================


def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Evaluate agent output for the graph algorithms task.

    Args:
        answer_dir: absolute path to agent output directory
                    (e.g. /path/to/query/gpt-5/attempt_1)

    Returns:
        (score, report) where score is 0-100 integer
    """
    report: Dict[str, Any] = {}
    total = 0

    # 1. File Delivery (10 pts)
    s1, d1 = _check_files(answer_dir)
    total += s1
    report["1_file_delivery"] = {"score": s1, "max": 10, "details": d1}

    # 2. Code Loadability (10 pts)
    s2, d2, mod = _check_loadability(answer_dir)
    total += s2
    report["2_code_loadability"] = {"score": s2, "max": 10, "details": d2}

    # 3. Algorithm Correctness (60 pts)
    if mod is not None:
        try:
            Graph = _get_graph_class()
        except Exception as e:
            Graph = None
        if Graph is not None:
            s3, d3 = _check_correctness(mod, Graph)
        else:
            s3, d3 = 0, {"error": f"cannot load Graph class"}
    else:
        s3, d3 = 0, {"error": "algorithms.py not loadable, skipping correctness tests"}
    total += s3
    report["3_algorithm_correctness"] = {"score": s3, "max": 60, "details": d3}

    # 4. Performance Report (10 pts)
    s4, d4 = _check_report(answer_dir)
    total += s4
    report["4_performance_report"] = {"score": s4, "max": 10, "details": d4}

    # 5. Code Documentation (10 pts)
    s5, d5 = _check_documentation(answer_dir)
    total += s5
    report["5_code_documentation"] = {"score": s5, "max": 10, "details": d5}

    total = max(0, min(100, total))
    report["total"] = total
    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print a formatted evaluation report."""
    print("=" * 70)
    print("Graph Algorithms Task - Evaluation Report")
    print("=" * 70)
    print(f"\nTotal score: {score}/100\n")

    sections = [
        ("1_file_delivery", "1. File Delivery (10 pts)"),
        ("2_code_loadability", "2. Code Loadability (10 pts)"),
        ("3_algorithm_correctness", "3. Algorithm Correctness (60 pts)"),
        ("4_performance_report", "4. Performance Report (10 pts)"),
        ("5_code_documentation", "5. Code Documentation (10 pts)"),
    ]
    for key, title in sections:
        sec = report.get(key, {})
        print("-" * 50)
        print(f"  {title}: {sec.get('score', 0)}/{sec.get('max', '?')}")
        print("-" * 50)
        details = sec.get("details", {})
        for k, v in details.items():
            print(f"    {k}: {v}")
        print()

    if score >= 90:
        comment = "Excellent! All graph algorithms implemented correctly with good documentation."
    elif score >= 70:
        comment = "Good. Most algorithms work correctly."
    elif score >= 50:
        comment = "Partial. Some algorithms have issues."
    elif score >= 30:
        comment = "Below expectations. Significant issues with correctness."
    else:
        comment = "Insufficient. Major problems with the implementation."
    print(f"Comment: {comment}")
    print("=" * 70)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_dir = sys.argv[1]
    else:
        test_dir = os.path.join(QUERY_ROOT, "workspace")

    if not os.path.isabs(test_dir):
        test_dir = os.path.join(QUERY_ROOT, test_dir)

    if os.path.exists(test_dir):
        print(f"Evaluating directory: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"Directory not found: {test_dir}")
    sys.exit(0)
