"""
Algorithm Optimization Task 3 — Rubric
Task: Optimize Dijkstra's algorithm performance to improve execution speed on large-scale graphs

Total: 100 points

Scoring dimensions:
I. File Delivery (10 pts)
  1. dijkstra_optimized.py exists (4 pts)
  2. performance_report.md exists (3 pts)
  3. comparison.csv exists (3 pts)

II. Algorithm Correctness (25 pts)
  1. Code can be imported and Graph class exists (5 pts)
  2. Graph class has add_edge and dijkstra methods (5 pts)
  3. Small graph correctness — 20 nodes (5 pts)
  4. Medium graph correctness — 200 nodes (5 pts)
  5. Large graph correctness — 1000 nodes (5 pts)

III. Performance Improvement (40 pts)
  1. Small graph performance (8 pts)  — nodes 15-55
  2. Medium graph performance (12 pts) — nodes 100-500
  3. Large graph performance (20 pts) — nodes 1000-2500

IV. Code Quality and Report (25 pts)
  1. Uses efficient data structures such as priority queue/heap (8 pts)
  2. Code has comments and docstrings (4 pts)
  3. performance_report.md content quality (8 pts) — LLM-as-Judge
  4. comparison.csv format and content are reasonable (5 pts)
"""

import os
import sys
import csv
import re
import time
import random
import math
import importlib.util
from typing import Tuple, Dict, Any, List

try:
    import openai
except ImportError:
    openai = None


# =============================================================================
# Environment Configuration
# =============================================================================

def _load_env(answer_dir: str) -> dict:
    """Load .env configuration from answer_dir and query root directory"""
    values = {}
    for env_dir in [answer_dir, os.path.join(os.path.dirname(__file__), "..")]:
        env_path = os.path.join(env_dir, ".env")
        if os.path.exists(env_path):
            try:
                with open(env_path, "r", encoding="utf-8") as f:
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
    """Get text evaluation LLM configuration"""
    env = _load_env(answer_dir)
    def g(key, default=""):
        return os.environ.get(key) or env.get(key) or default
    return {
        "api_key": g("EVAL_TEXT_API_KEY", g("ANTHROPIC_API_KEY")),
        "api_base": g("EVAL_TEXT_API_BASE_URL", g("ANTHROPIC_BASE_URL")),
        "model": g("EVAL_TEXT_MODEL", "openai/gpt-5.2"),
    }


def _call_llm_judge(prompt: str, config: dict) -> str:
    """Call LLM for text evaluation"""
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


# =============================================================================
# Utility Functions: Graph Generation and Performance Testing
# =============================================================================

def _generate_edges(size: int, density: float) -> List[Tuple[int, int, int]]:
    """Generate edge list for graph (ensure connectivity + add random edges by density)"""
    edges = []
    for i in range(size - 1):
        w = random.randint(1, 10)
        edges.append((i, i + 1, w))

    max_extra = int((size * (size - 1) / 2) * density)
    added = set()
    attempts = 0
    while len(added) < max_extra and attempts < max_extra * 3:
        attempts += 1
        u = random.randint(0, size - 1)
        v = random.randint(0, size - 1)
        if u != v and (u, v) not in added and (v, u) not in added:
            w = random.randint(1, 10)
            edges.append((u, v, w))
            added.add((u, v))
    return edges


def _run_original_dijkstra(edges, start=0):
    """Run dijkstra using original O(V^2) implementation and return distance dict"""
    graph = {}
    for u, v, w in edges:
        if u not in graph:
            graph[u] = []
        graph[u].append((v, w))
        if v not in graph:
            graph[v] = []
        graph[v].append((u, w))

    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    visited = set()
    while visited != set(graph.keys()):
        min_node = None
        min_dist = float('infinity')
        for node in graph:
            if node not in visited and distances[node] < min_dist:
                min_node = node
                min_dist = distances[node]
        if min_node is None:
            break
        visited.add(min_node)
        for neighbor, weight in graph.get(min_node, []):
            if neighbor not in visited:
                new_distance = distances[min_node] + weight
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
    return distances


def _time_original(edges, start=0, iterations=1):
    """Measure execution time of original implementation"""
    t0 = time.time()
    for _ in range(iterations):
        _run_original_dijkstra(edges, start)
    return (time.time() - t0) / iterations


def _time_optimized(GraphClass, edges, start=0, iterations=1):
    """Measure execution time of optimized implementation (rebuild graph each time for fair comparison)"""
    t0 = time.time()
    for _ in range(iterations):
        g = GraphClass()
        for u, v, w in edges:
            g.add_edge(u, v, w)
        g.dijkstra(start)
    return (time.time() - t0) / iterations


def _compute_speedup(orig_t, opt_t):
    """Compute speedup ratio"""
    if opt_t <= 0:
        return float("inf") if orig_t > 0 else 1.0
    return orig_t / opt_t


# =============================================================================
# I. File Delivery (10 pts)
# =============================================================================

def _eval_file_delivery(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details = {}
    files = os.listdir(answer_dir) if os.path.isdir(answer_dir) else []

    # 1.1 dijkstra_optimized.py (4 pts)
    if "dijkstra_optimized.py" in files:
        score += 4
        details["dijkstra_optimized.py"] = "4/4 - File exists"
    else:
        alt = [f for f in files if f.endswith(".py") and "dijkstra" in f.lower()
               and "original" not in f.lower() and not f.startswith("test_")]
        if alt:
            score += 2
            details["dijkstra_optimized.py"] = f"2/4 - Found similar file: {alt[0]}"
        else:
            details["dijkstra_optimized.py"] = "0/4 - File does not exist"

    # 1.2 performance_report.md (3 pts)
    if "performance_report.md" in files:
        score += 3
        details["performance_report.md"] = "3/3 - File exists"
    else:
        alt = [f for f in files if f.endswith(".md") and "report" in f.lower()]
        if alt:
            score += 1
            details["performance_report.md"] = f"1/3 - Found similar file: {alt[0]}"
        else:
            details["performance_report.md"] = "0/3 - File does not exist"

    # 1.3 comparison.csv (3 pts)
    if "comparison.csv" in files:
        score += 3
        details["comparison.csv"] = "3/3 - File exists"
    else:
        alt = [f for f in files if f.endswith(".csv")]
        if alt:
            score += 1
            details["comparison.csv"] = f"1/3 - Found CSV file: {alt[0]}"
        else:
            details["comparison.csv"] = "0/3 - File does not exist"

    return score, details


# =============================================================================
# II. Algorithm Correctness (25 pts)
# =============================================================================

def _load_graph_class(answer_dir: str):
    """Dynamically load the submitted Graph class; returns (GraphClass, error_msg)"""
    files = os.listdir(answer_dir) if os.path.isdir(answer_dir) else []
    target = None
    if "dijkstra_optimized.py" in files:
        target = "dijkstra_optimized.py"
    else:
        cands = [f for f in files if f.endswith(".py") and "dijkstra" in f.lower()
                 and "original" not in f.lower() and not f.startswith("test_")]
        if cands:
            target = cands[0]
    if not target:
        return None, "dijkstra_optimized.py not found"

    mod_path = os.path.join(answer_dir, target)
    try:
        spec = importlib.util.spec_from_file_location("dijkstra_optimized", mod_path)
        mod = importlib.util.module_from_spec(spec)
        saved = sys.path[:]
        sys.path.insert(0, answer_dir)
        try:
            spec.loader.exec_module(mod)
        finally:
            sys.path[:] = saved
    except Exception as e:
        return None, f"Import failed: {str(e)[:200]}"

    if not hasattr(mod, "Graph"):
        return None, "Graph class not found in module"
    return mod.Graph, None


def _verify_correctness(GraphClass, size: int, density: float) -> Tuple[bool, str]:
    """Compare results of original and optimized implementations on the same graph"""
    random.seed(42 + size)
    edges = _generate_edges(size, density)
    orig_dist = _run_original_dijkstra(edges, 0)

    try:
        g = GraphClass()
        for u, v, w in edges:
            g.add_edge(u, v, w)
        opt_dist = g.dijkstra(0)
    except Exception as e:
        return False, f"Execution error: {str(e)[:100]}"

    for node in orig_dist:
        orig_val = orig_dist[node]
        opt_val = opt_dist.get(node, None)
        if opt_val is None:
            return False, f"Node {node} not found in optimized result"
        if orig_val == float('infinity'):
            if opt_val == float('infinity') or (isinstance(opt_val, (int, float)) and opt_val >= 10 ** 15):
                continue
            return False, f"Node {node}: original=inf, optimized={opt_val}"
        else:
            if isinstance(opt_val, float) and opt_val == float('infinity'):
                return False, f"Node {node}: original={orig_val}, optimized=inf"
            if abs(float(orig_val) - float(opt_val)) > 1e-6:
                return False, f"Node {node}: original={orig_val}, optimized={opt_val}"

    return True, "Correct"


def _eval_correctness(answer_dir: str) -> Tuple[int, dict, Any]:
    """Evaluate correctness; returns (score, details, GraphClass)"""
    score = 0
    details = {}

    GraphClass, err = _load_graph_class(answer_dir)
    if GraphClass is None:
        details["import"] = f"0/10 - {err}"
        return 0, details, None

    # 2.1 Import successful (5 pts)
    score += 5
    details["import_success"] = "5/5 - Graph class imported successfully"

    # 2.2 Interface check (5 pts)
    has_add = hasattr(GraphClass, "add_edge") and callable(getattr(GraphClass, "add_edge"))
    has_dij = hasattr(GraphClass, "dijkstra") and callable(getattr(GraphClass, "dijkstra"))
    if has_add and has_dij:
        score += 5
        details["interface_check"] = "5/5 - Both add_edge and dijkstra methods exist"
    elif has_add or has_dij:
        score += 2
        present = "add_edge" if has_add else "dijkstra"
        details["interface_check"] = f"2/5 - Only {present} exists"
    else:
        details["interface_check"] = "0/5 - Both add_edge and dijkstra are missing"
        return score, details, None

    # 2.3 Small graph correctness (5 pts)
    ok, msg = _verify_correctness(GraphClass, 20, 0.3)
    if ok:
        score += 5
        details["small_graph_correctness"] = "5/5 - 20-node graph results correct"
    else:
        details["small_graph_correctness"] = f"0/5 - {msg}"
        return score, details, GraphClass

    # 2.4 Medium graph correctness (5 pts)
    ok, msg = _verify_correctness(GraphClass, 200, 0.15)
    if ok:
        score += 5
        details["medium_graph_correctness"] = "5/5 - 200-node graph results correct"
    else:
        details["medium_graph_correctness"] = f"0/5 - {msg}"

    # 2.5 Large graph correctness (5 pts)
    ok, msg = _verify_correctness(GraphClass, 1000, 0.05)
    if ok:
        score += 5
        details["large_graph_correctness"] = "5/5 - 1000-node graph results correct"
    else:
        details["large_graph_correctness"] = f"0/5 - {msg}"

    return score, details, GraphClass


# =============================================================================
# III. Performance Improvement (40 pts)
# =============================================================================

def _eval_performance(GraphClass, correctness_score: int) -> Tuple[int, dict]:
    """Evaluate performance improvement; requires correctness score >= 15 pts to test"""
    score = 0
    details = {}

    if GraphClass is None or correctness_score < 15:
        details["skipped"] = "Correctness not passed (<15 pts), skipping performance test"
        return 0, details

    random.seed(999)

    # 3.1 Small graph performance (8 pts) — nodes 15-55, density 0.3-0.5
    small_sizes = [15, 25, 35, 45, 55]
    small_densities = [0.3, 0.35, 0.4, 0.45, 0.5]
    try:
        total_orig = 0.0
        total_opt = 0.0
        for sz, den in zip(small_sizes, small_densities):
            edges = _generate_edges(sz, den)
            total_orig += _time_original(edges, iterations=50)
            total_opt += _time_optimized(GraphClass, edges, iterations=50)

        spd = _compute_speedup(total_orig, total_opt)
        spd_str = "inf" if math.isinf(spd) else f"{spd:.2f}x"

        if spd >= 5:
            score += 8
            details["small_graph_perf"] = f"8/8 - Speedup {spd_str} (>=5x)"
        elif spd >= 3:
            score += 5
            details["small_graph_perf"] = f"5/8 - Speedup {spd_str} (>=3x)"
        elif spd > 1:
            score += 2
            details["small_graph_perf"] = f"2/8 - Speedup {spd_str} (>1x)"
        else:
            details["small_graph_perf"] = f"0/8 - Speedup {spd_str} (no improvement)"
    except Exception as e:
        details["small_graph_perf"] = f"0/8 - Test error: {str(e)[:100]}"

    # 3.2 Medium graph performance (12 pts) — nodes 100-500, density 0.1-0.3
    medium_sizes = [100, 200, 300, 400, 500]
    medium_densities = [0.1, 0.15, 0.2, 0.25, 0.3]
    try:
        total_orig = 0.0
        total_opt = 0.0
        for sz, den in zip(medium_sizes, medium_densities):
            edges = _generate_edges(sz, den)
            total_orig += _time_original(edges, iterations=3)
            total_opt += _time_optimized(GraphClass, edges, iterations=3)

        spd = _compute_speedup(total_orig, total_opt)
        spd_str = "inf" if math.isinf(spd) else f"{spd:.2f}x"

        if spd >= 5:
            score += 12
            details["medium_graph_perf"] = f"12/12 - Speedup {spd_str} (>=5x)"
        elif spd >= 3:
            score += 8
            details["medium_graph_perf"] = f"8/12 - Speedup {spd_str} (>=3x)"
        elif spd > 1:
            score += 4
            details["medium_graph_perf"] = f"4/12 - Speedup {spd_str} (>1x)"
        else:
            details["medium_graph_perf"] = f"0/12 - Speedup {spd_str} (no improvement)"
    except Exception as e:
        details["medium_graph_perf"] = f"0/12 - Test error: {str(e)[:100]}"

    # 3.3 Large graph performance (20 pts) — nodes 1000-2500, density 0.05-0.1
    large_sizes = [1000, 1500, 2000, 2500]
    large_densities = [0.05, 0.075, 0.1, 0.05]
    try:
        total_orig = 0.0
        total_opt = 0.0
        for sz, den in zip(large_sizes, large_densities):
            edges = _generate_edges(sz, den)
            total_orig += _time_original(edges, iterations=1)
            total_opt += _time_optimized(GraphClass, edges, iterations=1)

        spd = _compute_speedup(total_orig, total_opt)
        spd_str = "inf" if math.isinf(spd) else f"{spd:.2f}x"

        if spd >= 10:
            score += 20
            details["large_graph_perf"] = f"20/20 - Speedup {spd_str} (>=10x)"
        elif spd >= 5:
            score += 14
            details["large_graph_perf"] = f"14/20 - Speedup {spd_str} (>=5x)"
        elif spd >= 2:
            score += 8
            details["large_graph_perf"] = f"8/20 - Speedup {spd_str} (>=2x)"
        elif spd > 1:
            score += 3
            details["large_graph_perf"] = f"3/20 - Speedup {spd_str} (>1x)"
        else:
            details["large_graph_perf"] = f"0/20 - Speedup {spd_str} (no improvement)"
    except Exception as e:
        details["large_graph_perf"] = f"0/20 - Test error: {str(e)[:100]}"

    return score, details


# =============================================================================
# IV. Code Quality and Report (25 pts)
# =============================================================================

def _read_file(path: str) -> str:
    """Safely read file contents"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


def _fallback_report_score(content: str) -> int:
    """Fallback report scoring when LLM is unavailable (conservative, max 5/8)"""
    s = 0
    cl = content.lower()
    if any(kw in cl for kw in ["heapq", "优先队列", "priority queue", "heap", "堆"]):
        s += 1
    if any(kw in cl for kw in ["优化", "optimize", "improve", "加速"]):
        s += 1
    if any(kw in cl for kw in ["加速比", "speedup", "倍", "秒", "second"]):
        s += 1
    if re.search(r'\d+\.\d+', content):
        s += 1
    if len(content) >= 500:
        s += 1
    if len(content) >= 1000:
        s += 1
    return min(5, s)


def _eval_quality_report(answer_dir: str) -> Tuple[int, dict]:
    """Evaluate code quality and report"""
    score = 0
    details = {}
    files = os.listdir(answer_dir) if os.path.isdir(answer_dir) else []

    # Find optimized code file
    code_file = None
    if "dijkstra_optimized.py" in files:
        code_file = "dijkstra_optimized.py"
    else:
        cands = [f for f in files if f.endswith(".py") and "dijkstra" in f.lower()
                 and "original" not in f.lower() and not f.startswith("test_")]
        if cands:
            code_file = cands[0]

    # ---- 4.1 Uses efficient data structures (8 pts) ----
    if code_file:
        code = _read_file(os.path.join(answer_dir, code_file))
        cl = code.lower()

        ds_score = 0
        ds_notes = []

        has_heapq = "heapq" in cl or "heappush" in cl or "heappop" in cl
        has_heap_import = "import heapq" in code or "from heapq" in code
        has_pq = "priorityqueue" in cl or "priority_queue" in cl
        if has_heapq or has_heap_import or has_pq:
            ds_score += 5
            ds_notes.append("Uses priority queue/heap")

        has_numpy = "import numpy" in code or "from numpy" in code
        if has_numpy:
            ds_score += 2
            ds_notes.append("Uses NumPy")

        has_collections = "defaultdict" in cl or "deque" in cl
        if has_collections:
            ds_score += 1
            ds_notes.append("Uses efficient collection types")

        ds_score = min(8, ds_score)
        score += ds_score
        details["efficient_data_structures"] = f"{ds_score}/8 - {'; '.join(ds_notes) if ds_notes else 'No efficient data structures detected'}"

        # ---- 4.2 Comments and documentation (4 pts) ----
        has_comments = code.count("#") >= 5
        has_docstrings = '"""' in code or "'''" in code
        doc_score = 0
        if has_comments and has_docstrings:
            doc_score = 4
        elif has_comments or has_docstrings:
            doc_score = 2
        score += doc_score
        details["comments_and_docs"] = (
            f"{doc_score}/4 - "
            f"{'Has comments' if has_comments else 'Missing comments'}, "
            f"{'Has docstrings' if has_docstrings else 'Missing docstrings'}"
        )
    else:
        details["efficient_data_structures"] = "0/8 - Code file not found"
        details["comments_and_docs"] = "0/4 - Code file not found"

    # ---- 4.3 performance_report.md content quality (8 pts) — LLM-as-Judge ----
    report_file = None
    if "performance_report.md" in files:
        report_file = "performance_report.md"
    else:
        alt = [f for f in files if f.endswith(".md") and "report" in f.lower()]
        if alt:
            report_file = alt[0]

    if report_file:
        report_content = _read_file(os.path.join(answer_dir, report_file))
        if len(report_content.strip()) < 50:
            details["report_content"] = "0/8 - Report content too short or empty"
        else:
            import json as _json
            config = _get_text_eval_config(answer_dir)
            prompt = (
                "You are a strict code review expert. Please evaluate the quality of the following Dijkstra algorithm optimization performance report.\n\n"
                "Report content:\n---\n"
                f"{report_content[:3000]}\n---\n\n"
                "Scoring criteria (total 8 points):\n"
                "1. Optimization strategy explanation (0-2 pts): Does it clearly explain the optimization strategies (e.g., using priority queue, more efficient data structures, etc.)?\n"
                "2. Performance test data (0-3 pts): Does it include specific performance test data (test times for different graph scales, speedup ratios, etc.)?\n"
                "3. Analysis and summary (0-3 pts): Does it analyze the reasons for performance improvement? Is there a reasonable summary?\n\n"
                "Please reply strictly in the following JSON format (do not include any other content):\n"
                "```json\n"
                '{"optimization_strategy": {"score": 0, "reason": ""}, '
                '"test_data": {"score": 0, "reason": ""}, '
                '"analysis": {"score": 0, "reason": ""}, '
                '"total": 0}\n'
                "```"
            )

            llm_result = _call_llm_judge(prompt, config)
            if llm_result:
                try:
                    if "```json" in llm_result:
                        llm_result = llm_result.split("```json")[1].split("```")[0].strip()
                    elif "```" in llm_result:
                        llm_result = llm_result.split("```")[1].split("```")[0].strip()
                    parsed = _json.loads(llm_result)
                    report_score = min(8, max(0, int(parsed.get("total", 0))))
                    score += report_score
                    opt_s = parsed.get("optimization_strategy", {}).get("score", 0)
                    test_s = parsed.get("test_data", {}).get("score", 0)
                    ana_s = parsed.get("analysis", {}).get("score", 0)
                    details["report_content"] = (
                        f"{report_score}/8 - LLM evaluation: "
                        f"optimization_strategy={opt_s}/2, test_data={test_s}/3, analysis_summary={ana_s}/3"
                    )
                except Exception:
                    fb = _fallback_report_score(report_content)
                    score += fb
                    details["report_content"] = f"{fb}/8 - LLM returned abnormal format, fallback evaluation"
            else:
                fb = _fallback_report_score(report_content)
                score += fb
                details["report_content"] = f"{fb}/8 - LLM unavailable, fallback evaluation"
    else:
        details["report_content"] = "0/8 - Report file does not exist"

    # ---- 4.4 comparison.csv format and content (5 pts) ----
    csv_file = None
    if "comparison.csv" in files:
        csv_file = "comparison.csv"
    else:
        alt = [f for f in files if f.endswith(".csv")]
        if alt:
            csv_file = alt[0]

    if csv_file:
        try:
            csv_path = os.path.join(answer_dir, csv_file)
            with open(csv_path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                rows = list(reader)

            csv_score = 0
            csv_notes = []

            if len(rows) >= 2:
                csv_score += 1
                csv_notes.append("Has header and data rows")

                header_lower = [h.lower() for h in rows[0]] if rows else []
                has_time_col = any(
                    kw in h for h in header_lower
                    for kw in ["time", "耗时", "sec", "speed", "加速"]
                )
                has_size_col = any(
                    kw in h for h in header_lower
                    for kw in ["size", "节点", "node", "graph", "规模"]
                )

                if has_time_col:
                    csv_score += 2
                    csv_notes.append("Contains time/performance data column")
                if has_size_col:
                    csv_score += 1
                    csv_notes.append("Contains graph scale data column")

                if len(rows) >= 5:
                    csv_score += 1
                    csv_notes.append(f"Sufficient data ({len(rows) - 1} rows)")
            else:
                csv_notes.append("Insufficient data rows")

            csv_score = min(5, csv_score)
            score += csv_score
            details["csv_data"] = f"{csv_score}/5 - {'; '.join(csv_notes)}"
        except Exception as e:
            details["csv_data"] = f"0/5 - Read failed: {str(e)[:100]}"
    else:
        details["csv_data"] = "0/5 - CSV file does not exist"

    return score, details


# =============================================================================
# Entry
# =============================================================================

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """Evaluate the agent's output.

    Args:
        answer_dir: Absolute path to the agent output directory

    Returns:
        (score, report) — score is an integer 0-100, report is a detailed report dict
    """
    s1, r1 = _eval_file_delivery(answer_dir)
    s2, r2, GraphClass = _eval_correctness(answer_dir)
    s3, r3 = _eval_performance(GraphClass, s2)
    s4, r4 = _eval_quality_report(answer_dir)

    total = s1 + s2 + s3 + s4

    report = {
        "total_score": total,
        "section_scores": {
            "I. File Delivery": f"{s1}/10",
            "II. Algorithm Correctness": f"{s2}/25",
            "III. Performance Improvement": f"{s3}/40",
            "IV. Code Quality and Report": f"{s4}/25",
        },
        "details": {
            "I. File Delivery (10 pts)": r1,
            "II. Algorithm Correctness (25 pts)": r2,
            "III. Performance Improvement (40 pts)": r3,
            "IV. Code Quality and Report (25 pts)": r4,
        },
    }

    if total >= 90:
        report["comment"] = "Excellent! Algorithm optimization is highly effective, code quality is high, and the report is complete."
    elif total >= 75:
        report["comment"] = "Good. Algorithm is correct with significant performance improvement; some dimensions have room for improvement."
    elif total >= 60:
        report["comment"] = "Passing. Basic optimization task completed, but performance improvement or report quality is insufficient."
    elif total >= 35:
        report["comment"] = "Partially complete. Algorithm implementation has issues or performance improvement is not significant."
    else:
        report["comment"] = "Failing. Task completion is severely insufficient."

    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print formatted scoring report"""
    print("=" * 70)
    print("Algorithm Optimization Task 3 — Scoring Report")
    print("Task: Optimize Dijkstra's algorithm performance")
    print("=" * 70)
    print(f"\nTotal Score: {score}/100")

    scores = report.get("section_scores", {})
    if scores:
        print("\nSection Scores:")
        for k, v in scores.items():
            print(f"  {k}: {v}")

    for section_name, section_details in report.get("details", {}).items():
        print(f"\n{'─' * 50}")
        print(f"[{section_name}]")
        print(f"{'─' * 50}")
        if isinstance(section_details, dict):
            for k, v in section_details.items():
                print(f"  {k}: {v}")
        else:
            print(f"  {section_details}")

    print(f"\n{'=' * 70}")
    print(f"Comment: {report.get('comment', '')}")
    print("=" * 70)


if __name__ == "__main__":
    test_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(__file__), "..", "gpt-5", "attempt_1")
    if not os.path.exists(test_dir):
        test_dir = os.path.join(os.path.dirname(__file__), "..", "workspace")
    if os.path.exists(test_dir):
        print(f"Evaluating directory: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"Directory does not exist: {test_dir}")
    sys.exit(0)
