"""
Scoring Rubric — Statistical Analysis of Sleep and Screen Time
Task: Complete statistical analysis of sleep duration and screen time based on context/data.csv (28-day data)

Total: 100 points
  Result Scoring (50 pts):
    1. File Delivery Completeness (10 pts)
    2. Visualization Quality (10 pts)
    3. Statistical Metrics Accuracy (20 pts)
    4. Report Quality (10 pts) — LLM-as-Judge
  Process Scoring (50 pts):
    1. Code Syntax and Runnability (10 pts)
    2. Code Analysis Completeness (25 pts)
    3. Code Standards and Output Completeness (15 pts)
"""
from __future__ import annotations

import ast
import json
import math
import os
import re
from typing import Any, Dict, List, Optional, Tuple

try:
    import openai
except ImportError:
    openai = None

# ---------------------------------------------------------------------------
# Reference values — precisely computed from context/data.csv
# ---------------------------------------------------------------------------
REF_N = 28
REF_SLEEP_MEAN = 7.1736
REF_SLEEP_STD_SAMPLE = 1.1417   # ddof=1
REF_SLEEP_STD_POP = 1.1212      # ddof=0 (MLE)
REF_SCREEN_MEAN = 5.6136
REF_SCREEN_STD_SAMPLE = 1.6482  # ddof=1
REF_SCREEN_STD_POP = 1.6185     # ddof=0 (MLE)
REF_PEARSON_R = 0.5163
# 95% CI for means (t-distribution, df=27, t_crit~2.052)
REF_SLEEP_CI95 = (6.7308, 7.6163)
REF_SCREEN_CI95 = (4.9744, 6.2527)


# ---------------------------------------------------------------------------
# Environment configuration & LLM utilities
# ---------------------------------------------------------------------------

def _load_env(answer_dir: str) -> dict:
    """Load .env configuration from answer_dir and query root directory"""
    values: Dict[str, str] = {}
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
    env = _load_env(answer_dir)
    def g(key: str, default: str = "") -> str:
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


# ---------------------------------------------------------------------------
# General utilities
# ---------------------------------------------------------------------------

def _ls(directory: str) -> List[str]:
    try:
        return os.listdir(directory)
    except Exception:
        return []


def _find(answer_dir: str, names: List[str], subdirs: bool = True) -> Optional[str]:
    """Search for a file in answer_dir (and one level of subdirectories), return relative path"""
    files = _ls(answer_dir)
    lower_map = {f.lower(): f for f in files}
    for n in names:
        if n.lower() in lower_map:
            return lower_map[n.lower()]
    if subdirs:
        for f in files:
            sub = os.path.join(answer_dir, f)
            if os.path.isdir(sub):
                sub_map = {sf.lower(): sf for sf in _ls(sub)}
                for n in names:
                    if n.lower() in sub_map:
                        return os.path.join(f, sub_map[n.lower()])
    return None


def _read_json(filepath: str) -> Optional[dict]:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _read_text(filepath: str, max_chars: int = 50000) -> str:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read(max_chars)
    except Exception:
        return ""


def _close(actual: float, expected: float, tol: float) -> bool:
    return abs(actual - expected) <= tol


def _get_metric(data: dict, flat_key: str, paths: List[List[str]]) -> Optional[float]:
    """Try to extract a numeric metric from the metrics dict"""
    # flat key
    v = data.get(flat_key)
    if v is not None:
        try:
            return float(v)
        except (TypeError, ValueError):
            pass
    # nested paths
    for path in paths:
        obj = data
        for k in path:
            if isinstance(obj, dict):
                obj = obj.get(k)
            else:
                obj = None
                break
        if obj is not None:
            try:
                return float(obj)
            except (TypeError, ValueError):
                pass
    return None


def _get_ci(data: dict, flat_key: str, paths: List[List[str]]) -> Optional[List[float]]:
    """Extract confidence interval [lo, hi]"""
    v = data.get(flat_key)
    if isinstance(v, (list, tuple)) and len(v) == 2:
        try:
            return [float(v[0]), float(v[1])]
        except (TypeError, ValueError):
            pass
    for path in paths:
        obj = data
        for k in path:
            if isinstance(obj, dict):
                obj = obj.get(k)
            else:
                obj = None
                break
        if isinstance(obj, (list, tuple)) and len(obj) == 2:
            try:
                return [float(obj[0]), float(obj[1])]
            except (TypeError, ValueError):
                pass
    return None


# ===================================================================
# Part 1: Result Scoring (50 pts)
# ===================================================================

def _score_file_delivery(answer_dir: str) -> Tuple[int, Dict[str, str]]:
    """1. File Delivery Completeness (10 pts)"""
    score = 0
    det: Dict[str, str] = {}

    # 1a. analysis.py (3 pts)
    files = _ls(answer_dir)
    files_lower = [f.lower() for f in files]
    if "analysis.py" in files_lower:
        score += 3
        det["analysis.py"] = "3/3 - exists"
    elif any(f.endswith(".py") for f in files):
        score += 2
        py = next(f for f in files if f.endswith(".py"))
        det["analysis.py"] = f"2/3 - Python file {py} exists, but non-standard name"
    else:
        det["analysis.py"] = "0/3 - not found"

    # 1b. report.md / report.pdf (3 pts)
    rpt = _find(answer_dir, ["report.md", "report.pdf"], subdirs=False)
    if rpt:
        score += 3
        det["report"] = f"3/3 - {rpt}"
    else:
        other_doc = [f for f in files if f.endswith((".md", ".pdf"))]
        if other_doc:
            score += 1
            det["report"] = f"1/3 - document {other_doc[0]} exists but not report.md/pdf"
        else:
            det["report"] = "0/3 - no report file found"

    # 1c. metrics.json (2 pts)
    mj = _find(answer_dir, ["metrics.json"], subdirs=False)
    if mj:
        score += 2
        det["metrics.json"] = "2/2 - exists"
    else:
        det["metrics.json"] = "0/2 - not found"

    # 1d. scatter.png (2 pts)
    sc = _find(answer_dir, ["scatter.png"])
    if sc:
        score += 2
        det["scatter.png"] = f"2/2 - {sc}"
    else:
        det["scatter.png"] = "0/2 - scatter plot not found"

    return score, det


def _score_visualization(answer_dir: str) -> Tuple[int, Dict[str, str]]:
    """2. Visualization Quality (10 pts)"""
    score = 0
    det: Dict[str, str] = {}

    # 2a. scatter.png exists and valid (5 pts)
    sc = _find(answer_dir, ["scatter.png"])
    if sc:
        fpath = os.path.join(answer_dir, sc)
        fsize = os.path.getsize(fpath) if os.path.isfile(fpath) else 0
        if fsize >= 5000:
            score += 5
            det["scatter plot"] = f"5/5 - {sc} ({fsize // 1024}KB)"
        elif fsize > 0:
            score += 3
            det["scatter plot"] = f"3/5 - {sc} file is small ({fsize}B)"
        else:
            det["scatter plot"] = f"0/5 - {sc} file is empty"
    else:
        det["scatter plot"] = "0/5 - scatter.png not found"

    # 2b. Distribution plot / box plot at least one (5 pts)
    dist_candidates = ["hist_sleep.png", "hist_screen.png", "boxplot.png"]
    found = []
    for name in dist_candidates:
        p = _find(answer_dir, [name])
        if p:
            found.append(p)

    if len(found) >= 2:
        score += 5
        det["distribution/box plot"] = f"5/5 - {len(found)} found: {', '.join(found)}"
    elif len(found) == 1:
        score += 4
        det["distribution/box plot"] = f"4/5 - 1 found: {found[0]}"
    else:
        # Check visualizations/ subdirectory
        vis_dir = os.path.join(answer_dir, "visualizations")
        if os.path.isdir(vis_dir):
            pngs = [f for f in os.listdir(vis_dir) if f.lower().endswith(".png")]
            if pngs:
                score += 2
                det["distribution/box plot"] = f"2/5 - visualizations/ has {len(pngs)} images but non-standard names"
            else:
                det["distribution/box plot"] = "0/5 - not found"
        else:
            det["distribution/box plot"] = "0/5 - not found"

    return score, det


def _score_metrics_accuracy(answer_dir: str) -> Tuple[int, Dict[str, str]]:
    """3. Statistical Metrics Accuracy (20 pts)"""
    score = 0
    det: Dict[str, str] = {}

    mp = _find(answer_dir, ["metrics.json"], subdirs=False)
    if not mp:
        return 0, {"error": "0/20 - metrics.json does not exist"}
    data = _read_json(os.path.join(answer_dir, mp))
    if data is None:
        return 0, {"error": "0/20 - metrics.json parse failed"}

    # --- helper: nested key paths for each metric ---
    sleep_mu_paths = [["sleep", "mean"], ["sleep", "mu"], ["sleep_mean"]]
    sleep_sigma_paths = [
        ["sleep", "std_sample"], ["sleep", "sigma"], ["sleep", "std"],
        ["sleep", "std_pop_mle"], ["sleep_std"],
    ]
    sleep_ci_paths = [
        ["sleep", "mu_ci_95"], ["sleep", "mu_ci_95_boot"],
        ["sleep", "mu_ci_95_param"], ["sleep", "ci95"],
    ]
    screen_mu_paths = [["screen", "mean"], ["screen", "mu"], ["screen_mean"]]
    screen_sigma_paths = [
        ["screen", "std_sample"], ["screen", "sigma"], ["screen", "std"],
        ["screen", "std_pop_mle"], ["screen_std"],
    ]
    screen_ci_paths = [
        ["screen", "mu_ci_95"], ["screen", "mu_ci_95_boot"],
        ["screen", "mu_ci_95_param"], ["screen", "ci95"],
    ]

    # 3a. sleep_mu (3 pts)
    val = _get_metric(data, "sleep_mu", sleep_mu_paths)
    if val is not None and _close(val, REF_SLEEP_MEAN, 0.5):
        score += 3
        det["sleep_mu"] = f"3/3 - {val:.4f} (ref {REF_SLEEP_MEAN})"
    elif val is not None:
        score += 1
        det["sleep_mu"] = f"1/3 - {val:.4f} large deviation (ref {REF_SLEEP_MEAN})"
    else:
        det["sleep_mu"] = "0/3 - not found"

    # 3b. sleep_sigma (3 pts) — accept sample or population std
    val = _get_metric(data, "sleep_sigma", sleep_sigma_paths)
    if val is not None and (_close(val, REF_SLEEP_STD_SAMPLE, 0.3) or _close(val, REF_SLEEP_STD_POP, 0.3)):
        score += 3
        det["sleep_sigma"] = f"3/3 - {val:.4f} (ref sample={REF_SLEEP_STD_SAMPLE}, pop={REF_SLEEP_STD_POP})"
    elif val is not None:
        score += 1
        det["sleep_sigma"] = f"1/3 - {val:.4f} large deviation"
    else:
        det["sleep_sigma"] = "0/3 - not found"

    # 3c. sleep_ci95 (2 pts)
    ci = _get_ci(data, "sleep_ci95", sleep_ci_paths)
    if ci is not None:
        lo, hi = ci
        if lo < REF_SLEEP_MEAN < hi and (hi - lo) < 5:
            score += 2
            det["sleep_ci95"] = f"2/2 - [{lo:.3f}, {hi:.3f}]"
        else:
            score += 1
            det["sleep_ci95"] = f"1/2 - [{lo:.3f}, {hi:.3f}] unreasonable interval"
    else:
        det["sleep_ci95"] = "0/2 - not found"

    # 3d. screen_mu (3 pts)
    val = _get_metric(data, "screen_mu", screen_mu_paths)
    if val is not None and _close(val, REF_SCREEN_MEAN, 0.5):
        score += 3
        det["screen_mu"] = f"3/3 - {val:.4f} (ref {REF_SCREEN_MEAN})"
    elif val is not None:
        score += 1
        det["screen_mu"] = f"1/3 - {val:.4f} large deviation (ref {REF_SCREEN_MEAN})"
    else:
        det["screen_mu"] = "0/3 - not found"

    # 3e. screen_sigma (3 pts)
    val = _get_metric(data, "screen_sigma", screen_sigma_paths)
    if val is not None and (_close(val, REF_SCREEN_STD_SAMPLE, 0.3) or _close(val, REF_SCREEN_STD_POP, 0.3)):
        score += 3
        det["screen_sigma"] = f"3/3 - {val:.4f} (ref sample={REF_SCREEN_STD_SAMPLE}, pop={REF_SCREEN_STD_POP})"
    elif val is not None:
        score += 1
        det["screen_sigma"] = f"1/3 - {val:.4f} large deviation"
    else:
        det["screen_sigma"] = "0/3 - not found"

    # 3f. screen_ci95 (2 pts)
    ci = _get_ci(data, "screen_ci95", screen_ci_paths)
    if ci is not None:
        lo, hi = ci
        if lo < REF_SCREEN_MEAN < hi and (hi - lo) < 5:
            score += 2
            det["screen_ci95"] = f"2/2 - [{lo:.3f}, {hi:.3f}]"
        else:
            score += 1
            det["screen_ci95"] = f"1/2 - [{lo:.3f}, {hi:.3f}] unreasonable interval"
    else:
        det["screen_ci95"] = "0/2 - not found"

    # 3g. pearson_r (2 pts)
    val = _get_metric(data, "pearson_r", [
        ["pearson", "r"], ["correlation", "r"], ["pearson_correlation"],
    ])
    if val is not None and _close(val, REF_PEARSON_R, 0.15):
        score += 2
        det["pearson_r"] = f"2/2 - {val:.4f} (ref {REF_PEARSON_R})"
    elif val is not None:
        score += 1
        det["pearson_r"] = f"1/2 - {val:.4f} large deviation (ref {REF_PEARSON_R})"
    else:
        det["pearson_r"] = "0/2 - not found"

    # 3h. pearson_p (2 pts)
    val = _get_metric(data, "pearson_p", [
        ["pearson", "p_value"], ["pearson", "p"],
        ["pearson", "p_value_permutation"],
        ["correlation", "p_value"], ["correlation", "p"],
    ])
    if val is not None and val < 0.05:
        score += 2
        det["pearson_p"] = f"2/2 - {val:.6f} (significant, p < 0.05)"
    elif val is not None:
        score += 1
        det["pearson_p"] = f"1/2 - {val:.6f} (not significant)"
    else:
        det["pearson_p"] = "0/2 - not found"

    return score, det


def _score_report_quality(answer_dir: str) -> Tuple[int, Dict[str, str]]:
    """4. Report Quality (10 pts) — LLM-as-Judge"""
    det: Dict[str, str] = {}

    rpt = _find(answer_dir, ["report.md"], subdirs=False)
    if not rpt:
        rpt = _find(answer_dir, ["report.pdf"], subdirs=False)
    if not rpt:
        return 0, {"error": "0/10 - report not found"}

    fpath = os.path.join(answer_dir, rpt)

    # PDF — cannot evaluate precisely, give conservative score
    if rpt.lower().endswith(".pdf"):
        fsize = os.path.getsize(fpath) if os.path.isfile(fpath) else 0
        if fsize > 5000:
            det["PDF"] = "5/10 - PDF exists with content, cannot evaluate in depth"
            return 5, det
        det["PDF"] = "2/10 - PDF too small"
        return 2, det

    content = _read_text(fpath, max_chars=20000)
    if not content.strip():
        return 0, {"error": "0/10 - report is empty"}

    # Basic structure check (fallback when LLM unavailable)
    base = 0
    if len(content) >= 200:
        base += 2
    if len(content) >= 500:
        base += 1
    cl = content.lower()
    has_stats = any(kw in cl for kw in ["mean", "std", "standard deviation", "average"])
    has_corr = any(kw in cl for kw in ["correlation", "pearson", "corr"])
    if has_stats:
        base += 1
    if has_corr:
        base += 1

    # LLM evaluation
    config = _get_text_eval_config(answer_dir)
    prompt = f"""You are a statistical analysis report reviewer. Please evaluate the quality of the following analysis report.

The report should be based on 28 days of personal data, analyzing the relationship between sleep duration and screen time.
The report should include: data description, statistical method explanation, parameter estimation results (mean, standard deviation, confidence intervals),
correlation analysis (Pearson r and p-value), visualization description, and conclusions.

Please score independently on the following dimensions (integers), with brief justification:
1. Method description (0-2 pts): Are the statistical methods used explained?
2. Results presentation (0-3 pts): Are statistical results fully presented (mean, std, CI, correlation coefficient)?
3. Conclusions and interpretation (0-2 pts): Are reasonable interpretations and summaries given for the results?
4. Format standards (0-3 pts): Is the section structure clear? Are charts referenced?

Please reply strictly in the following JSON format (no other text):
```json
{{{{
  "method_score": 0,
  "result_score": 0,
  "conclusion_score": 0,
  "format_score": 0,
  "total": 0,
  "comment": ""
}}}}
```

===== Report Content =====
{content[:8000]}
"""
    llm_resp = _call_llm_judge(prompt, config)
    if llm_resp:
        try:
            if "```json" in llm_resp:
                llm_resp = llm_resp.split("```json")[1].split("```")[0].strip()
            elif "```" in llm_resp:
                llm_resp = llm_resp.split("```")[1].split("```")[0].strip()
            result = json.loads(llm_resp)
            llm_score = min(10, max(0, int(result.get("total", 0))))
            det["LLM evaluation"] = (
                f"{llm_score}/10 - "
                f"method:{result.get('method_score',0)}/2, "
                f"results:{result.get('result_score',0)}/3, "
                f"conclusions:{result.get('conclusion_score',0)}/2, "
                f"format:{result.get('format_score',0)}/3"
            )
            if result.get("comment"):
                det["LLM comment"] = result["comment"]
            return llm_score, det
        except (json.JSONDecodeError, ValueError):
            det["LLM parse"] = "JSON parse failed, falling back to basic scoring"

    fallback = min(5, base)
    det["basic scoring"] = f"{fallback}/10 - LLM unavailable, conservative scoring"
    det["keyword check"] = f"statistics:{has_stats}, correlation:{has_corr}"
    return fallback, det


# ===================================================================
# Part 2: Process Scoring (50 pts)
# ===================================================================

def _score_code_syntax(answer_dir: str) -> Tuple[int, Dict[str, str]]:
    """1. Code Syntax and Runnability (10 pts)"""
    det: Dict[str, str] = {}
    files = _ls(answer_dir)
    py_files = [f for f in files if f.endswith(".py")]
    if not py_files:
        return 0, {"error": "0/10 - no Python files found"}

    target = "analysis.py" if "analysis.py" in py_files else py_files[0]
    code_path = os.path.join(answer_dir, target)
    try:
        with open(code_path, "r", encoding="utf-8") as f:
            code = f.read()
    except Exception as e:
        return 0, {"error": f"0/10 - read failed: {e}"}

    score = 0

    # AST syntax check (5 pts)
    try:
        ast.parse(code)
        score += 5
        det["syntax"] = f"5/5 - {target} syntax correct"
    except SyntaxError as e:
        det["syntax"] = f"0/5 - syntax error: {str(e)[:80]}"
        return 0, det

    # Effective code lines (2 pts)
    lines = [l for l in code.split("\n") if l.strip() and not l.strip().startswith("#")]
    if len(lines) >= 30:
        score += 2
        det["code lines"] = f"2/2 - {len(lines)} effective lines"
    elif len(lines) >= 10:
        score += 1
        det["code lines"] = f"1/2 - {len(lines)} lines (somewhat few)"
    else:
        det["code lines"] = f"0/2 - {len(lines)} lines (too few)"

    # No hardcoded absolute paths/network dependencies (3 pts)
    sub = 3
    if re.search(r'https?://', code):
        sub -= 1
        det["network dependency"] = "deduct 1 pt: contains URL"
    if re.search(r'["\'][A-Z]:\\|["\']/home/|["\']/root/', code):
        sub -= 1
        det["absolute path"] = "deduct 1 pt: contains hardcoded path"
    sub = max(0, sub)
    score += sub
    det["reproducibility"] = f"{sub}/3"

    return score, det


def _score_code_completeness(answer_dir: str) -> Tuple[int, Dict[str, str]]:
    """2. Code Analysis Completeness (25 pts)"""
    det: Dict[str, str] = {}
    files = _ls(answer_dir)
    py_files = [f for f in files if f.endswith(".py")]
    if not py_files:
        return 0, {"error": "0/25 - no Python files found"}

    target = "analysis.py" if "analysis.py" in py_files else py_files[0]
    code = _read_text(os.path.join(answer_dir, target))
    if not code:
        return 0, {"error": "0/25 - code is empty"}

    cl = code.lower()
    score = 0

    # 2a. Data loading (5 pts)
    has_csv = "data.csv" in code and (
        "csv" in cl or "pandas" in cl or "read_csv" in cl or "open(" in cl
    )
    if has_csv:
        score += 5
        det["data loading"] = "5/5 - references data.csv and reads it"
    elif "data.csv" in code:
        score += 3
        det["data loading"] = "3/5 - references data.csv but read method unclear"
    else:
        det["data loading"] = "0/5 - does not read data.csv"

    # 2b. Descriptive statistics (5 pts)
    stat_kw = [
        "mean", "std", "var", "quartile", "median", "percentile",
        "describe(", "np.mean", "np.std",
    ]
    cnt = sum(1 for kw in stat_kw if kw in cl)
    if cnt >= 4:
        score += 5
        det["descriptive statistics"] = f"5/5 - matched {cnt} keywords"
    elif cnt >= 2:
        score += 3
        det["descriptive statistics"] = f"3/5 - matched {cnt} keywords"
    elif cnt >= 1:
        score += 1
        det["descriptive statistics"] = f"1/5 - matched {cnt} keywords"
    else:
        det["descriptive statistics"] = "0/5 - no statistical computation found"

    # 2c. Normal distribution parameter estimation & confidence intervals (5 pts)
    ci_kw = [
        "ci", "confidence", "interval",
        "norm.fit", "norm.interval", "t.interval", "bootstrap",
        "z_crit", "t_crit", "sem", "margin", "ppf",
    ]
    ci_cnt = sum(1 for kw in ci_kw if kw in cl)
    if ci_cnt >= 3:
        score += 5
        det["confidence intervals"] = f"5/5 - matched {ci_cnt} CI keywords"
    elif ci_cnt >= 1:
        score += 3
        det["confidence intervals"] = f"3/5 - matched {ci_cnt} CI keywords"
    else:
        det["confidence intervals"] = "0/5 - no confidence interval computation found"

    # 2d. Correlation analysis (5 pts)
    corr_kw = [
        "pearson", "corrcoef", "corr(", "pearsonr",
        "correlation", "scipy.stats",
    ]
    corr_cnt = sum(1 for kw in corr_kw if kw in cl)
    has_p = any(kw in cl for kw in ["p_val", "p-val", "pvalue", "t_stat"])
    if corr_cnt >= 2 and has_p:
        score += 5
        det["correlation analysis"] = "5/5 - Pearson correlation + significance test"
    elif corr_cnt >= 1:
        score += 3
        det["correlation analysis"] = f"3/5 - has correlation coefficient but significance test unclear"
    else:
        det["correlation analysis"] = "0/5 - no correlation analysis found"

    # 2e. Visualization code (5 pts)
    vis_kw = [
        "matplotlib", "pyplot", "plt.scatter", "plt.hist", "plt.boxplot",
        "seaborn", "sns.", "savefig", "scatter", "hist",
        "boxplot", "figure", "subplot",
    ]
    vis_cnt = sum(1 for kw in vis_kw if kw in cl)
    has_save = "savefig" in cl or "save" in cl
    if vis_cnt >= 4 and has_save:
        score += 5
        det["visualization code"] = f"5/5 - matched {vis_cnt} keywords, has save"
    elif vis_cnt >= 2:
        score += 3
        det["visualization code"] = f"3/5 - matched {vis_cnt} keywords"
    elif vis_cnt >= 1:
        score += 1
        det["visualization code"] = f"1/5 - matched {vis_cnt} keywords"
    else:
        det["visualization code"] = "0/5 - no visualization code found"

    return score, det


def _score_code_standards(answer_dir: str) -> Tuple[int, Dict[str, str]]:
    """3. Code Standards and Output Completeness (15 pts)"""
    det: Dict[str, str] = {}
    score = 0

    files = _ls(answer_dir)
    py_files = [f for f in files if f.endswith(".py")]
    if not py_files:
        return 0, {"error": "0/15 - no Python files found"}

    target = "analysis.py" if "analysis.py" in py_files else py_files[0]
    code = _read_text(os.path.join(answer_dir, target))
    if not code:
        return 0, {"error": "0/15 - code is empty"}

    cl = code.lower()

    # 3a. metrics.json output logic (5 pts)
    if "metrics.json" in code:
        if "json.dump" in cl or "json.dumps" in cl:
            score += 5
            det["JSON output"] = "5/5 - code generates metrics.json with json.dump"
        else:
            score += 3
            det["JSON output"] = "3/5 - references metrics.json but no explicit json.dump"
    elif "json" in cl:
        score += 2
        det["JSON output"] = "2/5 - uses json module but does not target metrics.json"
    else:
        det["JSON output"] = "0/5 - no JSON output code found"

    # 3b. Report generation logic (5 pts)
    has_report_name = any(kw in code for kw in ["report.md", "report.pdf"])
    has_write = "write(" in cl or "to_pdf" in cl or "markdown" in cl
    if has_report_name and has_write:
        score += 5
        det["report generation"] = "5/5 - code generates report"
    elif has_report_name:
        score += 3
        det["report generation"] = "3/5 - references report filename but write method unclear"
    elif has_write:
        score += 2
        det["report generation"] = "2/5 - has write operations but no report filename specified"
    else:
        det["report generation"] = "0/5 - no report generation code found"

    # 3c. metrics.json field completeness (5 pts)
    mp = _find(answer_dir, ["metrics.json"], subdirs=False)
    if mp:
        data = _read_json(os.path.join(answer_dir, mp))
        if data:
            found = _count_metric_fields(data)
            if found >= 7:
                score += 5
                det["field completeness"] = f"5/5 - {found}/8 fields"
            elif found >= 5:
                score += 3
                det["field completeness"] = f"3/5 - {found}/8 fields"
            elif found >= 3:
                score += 2
                det["field completeness"] = f"2/5 - {found}/8 fields"
            elif found >= 1:
                score += 1
                det["field completeness"] = f"1/5 - {found}/8 fields"
            else:
                det["field completeness"] = "0/5 - no valid fields"
        else:
            det["field completeness"] = "0/5 - metrics.json parse failed"
    else:
        det["field completeness"] = "0/5 - metrics.json does not exist"

    return score, det


def _count_metric_fields(data: dict) -> int:
    """Count valid metric fields in metrics.json (max 8)"""
    flat_keys = ["sleep_mu", "sleep_sigma", "sleep_ci95",
                 "screen_mu", "screen_sigma", "screen_ci95",
                 "pearson_r", "pearson_p"]
    flat_cnt = sum(1 for k in flat_keys if k in data)

    nested_cnt = 0
    if isinstance(data.get("sleep"), dict):
        s = data["sleep"]
        if any(k in s for k in ("mean", "mu")):
            nested_cnt += 1
        if any(k in s for k in ("std_sample", "sigma", "std")):
            nested_cnt += 1
        if any(k in s for k in ("mu_ci_95", "mu_ci_95_boot", "ci95")):
            nested_cnt += 1
    if isinstance(data.get("screen"), dict):
        s = data["screen"]
        if any(k in s for k in ("mean", "mu")):
            nested_cnt += 1
        if any(k in s for k in ("std_sample", "sigma", "std")):
            nested_cnt += 1
        if any(k in s for k in ("mu_ci_95", "mu_ci_95_boot", "ci95")):
            nested_cnt += 1
    if isinstance(data.get("pearson"), dict):
        p = data["pearson"]
        if "r" in p:
            nested_cnt += 1
        if any(k in p for k in ("p_value", "p", "p_value_permutation")):
            nested_cnt += 1

    return max(flat_cnt, nested_cnt)


# ===================================================================
# Entry Function
# ===================================================================

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Evaluate agent output.

    Args:
        answer_dir: absolute path to agent output directory

    Returns:
        (score, report) — score 0-100 integer, report dict
    """
    # Result scoring (50 pts)
    s1, d1 = _score_file_delivery(answer_dir)
    s2, d2 = _score_visualization(answer_dir)
    s3, d3 = _score_metrics_accuracy(answer_dir)
    s4, d4 = _score_report_quality(answer_dir)
    result_score = s1 + s2 + s3 + s4

    # Process scoring (50 pts)
    s5, d5 = _score_code_syntax(answer_dir)
    s6, d6 = _score_code_completeness(answer_dir)
    s7, d7 = _score_code_standards(answer_dir)
    process_score = s5 + s6 + s7

    total = result_score + process_score

    report: Dict[str, Any] = {
        "total_score": total,
        "Result Scoring (50 pts)": {
            "score": result_score,
            "details": {
                "1. File Delivery (10 pts)": d1,
                "2. Visualization (10 pts)": d2,
                "3. Metrics Accuracy (20 pts)": d3,
                "4. Report Quality (10 pts)": d4,
            },
        },
        "Process Scoring (50 pts)": {
            "score": process_score,
            "details": {
                "1. Code Syntax (10 pts)": d5,
                "2. Code Completeness (25 pts)": d6,
                "3. Code Standards (15 pts)": d7,
            },
        },
        "verdict": "",
    }

    if total >= 90:
        report["verdict"] = "Excellent. Analysis is comprehensive and accurate, code is well-structured, report is complete."
    elif total >= 75:
        report["verdict"] = "Good. Task basically completed, some dimensions can be further improved."
    elif total >= 60:
        report["verdict"] = "Passing. Core functionality completed but with gaps."
    elif total >= 40:
        report["verdict"] = "Partially complete. Please supplement key steps or fix issues."
    else:
        report["verdict"] = "Failing. Task completion is severely insufficient."

    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print formatted scoring report"""
    print("=" * 70)
    print("Scoring Report: Statistical Analysis of Sleep and Screen Time")
    print("=" * 70)
    print(f"\nTotal Score: {score}/100\n")

    for section_key in ("Result Scoring (50 pts)", "Process Scoring (50 pts)"):
        section = report.get(section_key, {})
        sec_score = section.get("score", 0)
        print("-" * 60)
        print(f"[{section_key}] Score: {sec_score}")
        print("-" * 60)
        for cat, items in section.get("details", {}).items():
            print(f"\n  {cat}")
            if isinstance(items, dict):
                for k, v in items.items():
                    print(f"    {k}: {v}")
            else:
                print(f"    {items}")

    print(f"\n{'=' * 70}")
    print(f"Verdict: {report.get('verdict', '')}")
    print("=" * 70)


if __name__ == "__main__":
    import sys
    test_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(__file__), "..", "gpt-5", "attempt_1")
    if not os.path.isabs(test_dir):
        test_dir = os.path.join(os.path.dirname(__file__), "..", test_dir)
    if os.path.exists(test_dir):
        print(f"Evaluating directory: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"Directory does not exist: {test_dir}")
    sys.exit(0)
