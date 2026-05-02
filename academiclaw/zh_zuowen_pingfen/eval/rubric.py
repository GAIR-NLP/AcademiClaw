#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
作文评分系统 — 评估脚本 (rubric.py)

任务概述:
  Agent 需阅读 ~111 篇上海高考模拟议论文, 按评分细则 (57-70 分) 逐篇评分,
  输出 Markdown 格式的评分结果文件 "作文评分结果.md".

评分维度 (总分 100):
  1. 文件交付        10 分
  2. 格式规范        15 分
  3. 评分完整性      20 分
  4. 评分合理性      25 分
  5. 评语质量        30 分 (LLM-as-Judge)
"""

import os
import re
import json
import math
from collections import Counter
from typing import Tuple, Dict, Any, List, Optional

try:
    import openai
except ImportError:
    openai = None

# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------
EXPECTED_ESSAY_COUNT = 111

# ---------------------------------------------------------------------------
# 环境 / LLM 工具
# ---------------------------------------------------------------------------

def _load_env(answer_dir: str) -> dict:
    """从 answer_dir 和 query 根目录加载 .env"""
    values: Dict[str, str] = {}
    query_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    for env_dir in [answer_dir, query_root]:
        env_path = os.path.join(env_dir, ".env")
        if os.path.exists(env_path):
            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#") or "=" not in line:
                            continue
                        k, v = line.split("=", 1)
                        k, v = k.strip(), v.strip().strip("'\"")
                        if k not in values:
                            values[k] = v
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
        print(f"[RUBRIC] LLM Judge error: {e}")
        return ""

# ---------------------------------------------------------------------------
# 解析
# ---------------------------------------------------------------------------

def _find_result_file(answer_dir: str) -> Optional[str]:
    """查找评分结果文件, 优先精确匹配, 再模糊匹配."""
    exact = os.path.join(answer_dir, "作文评分结果.md")
    if os.path.exists(exact):
        return exact
    if not os.path.isdir(answer_dir):
        return None
    for f in os.listdir(answer_dir):
        if f.endswith(".md") and "评分" in f:
            return os.path.join(answer_dir, f)
    return None


def _read_file(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


def _parse_results(raw: str) -> List[Dict[str, Any]]:
    """解析 Markdown 评分结果, 返回 [{title, score, reason}, ...]."""
    results: List[Dict[str, Any]] = []
    sections = re.split(r'(?:^|\n)##\s+', raw)
    for sec in sections:
        sec = sec.strip()
        if not sec:
            continue
        lines = sec.split("\n")
        header = lines[0].strip()
        if header.startswith("#"):
            continue
        title = re.sub(r'^作文\s*\d+\s*[：:]\s*', '', header).strip()
        full = "\n".join(lines)
        score = None
        m = re.search(r'\*\*分数\*\*[：:]\s*(\d+)\s*分', full)
        if m:
            score = int(m.group(1))
        else:
            m2 = re.search(r'(\d+)\s*分', full)
            if m2:
                v = int(m2.group(1))
                if 50 <= v <= 80:
                    score = v
        reason_lines: List[str] = []
        capture = False
        for line in lines[1:]:
            if "评分理由" in line:
                capture = True
                after = re.sub(r'.*评分理由.*?[：:]\s*', '', line).strip()
                if after:
                    reason_lines.append(after)
                continue
            if capture or (not line.startswith("**分数**") and line.strip()):
                reason_lines.append(line)
        reason = "\n".join(reason_lines).strip()
        results.append({"title": title, "score": score, "reason": reason})
    return results


def _extract_reference_scores(answer_dir: str) -> Dict[str, float]:
    """从 context.txt 目录区域提取带分数的条目."""
    query_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    for loc in [
        os.path.join(answer_dir, "context.txt"),
        os.path.join(query_root, "workspace", "context.txt"),
    ]:
        if os.path.exists(loc):
            content = _read_file(loc)
            break
    else:
        return {}
    refs: Dict[str, float] = {}
    for m in re.finditer(r'\d+\.\s*(.+?)[（\(](\d+(?:\.\d+)?)\s*分[）\)]', content):
        title = m.group(1).strip().rstrip(".")
        title = re.sub(r'\.+$', '', title).strip()
        sc = float(m.group(2))
        if 50 <= sc <= 70:
            refs[title] = sc
    return refs

# ---------------------------------------------------------------------------
# 维度 1: 文件交付 (10 分)
# ---------------------------------------------------------------------------

def _dim_file_delivery(answer_dir: str) -> Tuple[int, Dict[str, str]]:
    d: Dict[str, str] = {}
    path = _find_result_file(answer_dir)
    exact_name = os.path.exists(os.path.join(answer_dir, "作文评分结果.md"))
    if path is None:
        md_files = [f for f in (os.listdir(answer_dir) if os.path.isdir(answer_dir) else [])
                     if f.endswith(".md") and f != "query.md"]
        if md_files:
            d["文件"] = f"0/10 — 未找到评分文件, 仅有: {', '.join(md_files[:3])}"
        else:
            d["文件"] = "0/10 — 未找到任何 .md 文件"
        return 0, d

    fsize = os.path.getsize(path)
    fname = os.path.basename(path)
    score = 0
    if exact_name:
        if fsize >= 2000:
            score = 10
            d["文件"] = f"10/10 — 作文评分结果.md 存在 ({fsize / 1024:.1f} KB)"
        elif fsize > 0:
            score = 5
            d["文件"] = f"5/10 — 文件存在但偏小 ({fsize} B)"
        else:
            score = 2
            d["文件"] = "2/10 — 文件存在但为空"
    else:
        score = 3 if fsize >= 2000 else 1
        d["文件"] = f"{score}/10 — 文件名不匹配 (实际: {fname})"
    return score, d

# ---------------------------------------------------------------------------
# 维度 2: 格式规范 (15 分)
# ---------------------------------------------------------------------------

def _dim_format(results: List[Dict], raw: str) -> Tuple[int, Dict[str, str]]:
    d: Dict[str, str] = {}
    if not results:
        return 0, {"格式": "0/15 — 无法解析任何评分结果"}
    n = len(results)
    score = 0

    # 2a. **分数**：XX分 格式 (8 分)
    correct_fmt = len(re.findall(r'\*\*分数\*\*[：:]\s*\d+\s*分', raw))
    ratio = correct_fmt / n
    if ratio >= 0.95:
        s = 8
    elif ratio >= 0.80:
        s = 6
    elif ratio >= 0.50:
        s = 4
    elif ratio > 0:
        s = 2
    else:
        s = 0
    d["分数格式"] = f"{s}/8 — {correct_fmt}/{n} 篇正确格式"
    score += s

    # 2b. ## 作文N 章节结构 (4 分)
    sec_count = len(re.findall(r'##\s+作文\s*\d+', raw))
    sr = sec_count / n
    if sr >= 0.90:
        s = 4
    elif sr >= 0.50:
        s = 2
    else:
        s = 1 if sec_count > 0 else 0
    d["章节结构"] = f"{s}/4 — {sec_count}/{n} 篇使用 ## 作文N 结构"
    score += s

    # 2c. 评分理由存在 (3 分)
    with_reason = sum(1 for r in results if r.get("reason") and len(r["reason"]) > 10)
    rr = with_reason / n
    if rr >= 0.95:
        s = 3
    elif rr >= 0.80:
        s = 2
    elif rr >= 0.50:
        s = 1
    else:
        s = 0
    d["评分理由"] = f"{s}/3 — {with_reason}/{n} 篇含理由 (>10字)"
    score += s

    return score, d

# ---------------------------------------------------------------------------
# 维度 3: 评分完整性 (20 分)
# ---------------------------------------------------------------------------

def _dim_completeness(results: List[Dict]) -> Tuple[int, Dict[str, str]]:
    d: Dict[str, str] = {}
    n = len(results)
    with_score = sum(1 for r in results if r.get("score") is not None)
    score = 0

    # 3a. 评分篇数 (12 分)
    if n >= 105 and with_score >= 105:
        s = 12
    elif n >= 100 and with_score >= 100:
        s = 10
    elif n >= 90 and with_score >= 90:
        s = 8
    elif n >= 70 and with_score >= 70:
        s = 5
    elif n >= 50 and with_score >= 50:
        s = 3
    elif n > 0:
        s = 1
    else:
        s = 0
    d["评分篇数"] = f"{s}/12 — 共 {n} 篇, {with_score} 篇有分数"
    score += s

    # 3b. 分数为有效整数 (4 分)
    valid_int = [r["score"] for r in results
                 if r.get("score") is not None and isinstance(r["score"], int)]
    if with_score > 0 and len(valid_int) == with_score:
        s = 4
    elif with_score > 0 and len(valid_int) >= with_score * 0.9:
        s = 3
    elif valid_int:
        s = 1
    else:
        s = 0
    d["整数分数"] = f"{s}/4 — {len(valid_int)}/{with_score} 为有效整数"
    score += s

    # 3c. 无遗漏 (4 分)
    if n == 0:
        s = 0
    elif n >= 105 and with_score == n:
        s = 4
    elif n >= 100 and with_score >= n - 5:
        s = 3
    elif with_score >= n * 0.90:
        s = 2
    elif with_score > 0:
        s = 1
    else:
        s = 0
    missing = n - with_score
    d["遗漏检查"] = f"{s}/4 — {missing} 篇缺少分数"
    score += s

    return score, d

# ---------------------------------------------------------------------------
# 维度 4: 评分合理性 (25 分)
# ---------------------------------------------------------------------------

def _pearson(x: List[float], y: List[float]) -> float:
    n = len(x)
    if n < 3:
        return 0.0
    mx = sum(x) / n
    my = sum(y) / n
    cov = sum((x[i] - mx) * (y[i] - my) for i in range(n))
    sx = math.sqrt(sum((xi - mx) ** 2 for xi in x))
    sy = math.sqrt(sum((yi - my) ** 2 for yi in y))
    if sx == 0 or sy == 0:
        return 0.0
    return cov / (sx * sy)


def _dim_score_quality(results: List[Dict], ref_scores: Dict[str, float]) -> Tuple[int, Dict[str, str]]:
    d: Dict[str, str] = {}
    valid = [r for r in results if r.get("score") is not None]
    scores = [r["score"] for r in valid]
    if not scores:
        return 0, {"合理性": "0/25 — 无有效分数"}
    total = 0

    # 4a. 分数范围 57-70 (8 分)
    in_range = sum(1 for s in scores if 57 <= s <= 70)
    ratio = in_range / len(scores)
    if ratio >= 0.95:
        s = 8
    elif ratio >= 0.85:
        s = 6
    elif ratio >= 0.70:
        s = 4
    elif ratio >= 0.50:
        s = 2
    else:
        s = 0
    d["分数范围"] = f"{s}/8 — {in_range}/{len(scores)} 在 57-70 内"
    total += s

    # 4b. 分数分布 (10 分): 标准差, 独特分数数, 最频繁分数占比
    ctr = Counter(scores)
    unique_n = len(ctr)
    most_pct = ctr.most_common(1)[0][1] / len(scores) if scores else 1
    mean_s = sum(scores) / len(scores)
    std_s = math.sqrt(sum((x - mean_s) ** 2 for x in scores) / len(scores))

    if std_s >= 2.5 and unique_n >= 8 and most_pct <= 0.25:
        s = 10
    elif std_s >= 2.0 and unique_n >= 6 and most_pct <= 0.30:
        s = 8
    elif std_s >= 1.5 and unique_n >= 5 and most_pct <= 0.35:
        s = 6
    elif std_s >= 1.0 and unique_n >= 4:
        s = 4
    elif unique_n >= 3:
        s = 2
    else:
        s = 0
    d["分数分布"] = (f"{s}/10 — 均值={mean_s:.1f}, σ={std_s:.2f}, "
                     f"{unique_n} 种分数, 最集中={most_pct * 100:.0f}%")
    total += s

    # 4c. 与参考分相关 (7 分)
    if ref_scores:
        matched: List[Tuple[float, float]] = []
        for r in valid:
            t = r.get("title", "")
            t_clean = re.sub(r'[\s\u3000，。、；：""''？！…—（）()\[\]]+', '', t)
            for rt, rs in ref_scores.items():
                rc = re.sub(r'[\s\u3000，。、；：""''？！…—（）()\[\]]+', '', rt)
                if t_clean and rc and (t_clean in rc or rc in t_clean):
                    matched.append((float(r["score"]), rs))
                    break
        if len(matched) >= 10:
            xs = [a for a, _ in matched]
            ys = [b for _, b in matched]
            mae = sum(abs(a - b) for a, b in matched) / len(matched)
            corr = _pearson(xs, ys)
            if mae <= 2.0 and corr >= 0.3:
                s = 7
            elif mae <= 3.0 and corr >= 0.15:
                s = 5
            elif mae <= 4.0:
                s = 3
            elif mae <= 5.0:
                s = 2
            else:
                s = 1
            d["参考分相关"] = (f"{s}/7 — 匹配 {len(matched)} 篇, "
                              f"MAE={mae:.2f}, r={corr:.3f}")
        else:
            s = 3
            d["参考分相关"] = f"{s}/7 — 仅匹配 {len(matched)} 篇 (<10), 保守分"
    else:
        s = 3
        d["参考分相关"] = f"{s}/7 — 无参考分可用, 保守分"
    total += s

    return total, d

# ---------------------------------------------------------------------------
# 维度 5: 评语质量 (30 分) — LLM-as-Judge + 降级
# ---------------------------------------------------------------------------

def _dim_comment_quality(results: List[Dict], answer_dir: str) -> Tuple[int, Dict[str, str]]:
    d: Dict[str, str] = {}
    if not results:
        return 0, {"评语质量": "0/30 — 无评分结果"}

    n = len(results)
    # 采样: 前 5 + 中间 5 + 后 5
    if n <= 15:
        indices = list(range(n))
    else:
        indices = (list(range(5))
                   + list(range(n // 2 - 2, n // 2 + 3))
                   + list(range(n - 5, n)))
    samples = [results[i] for i in indices if i < n]

    reason_lens = [len(r.get("reason", "")) for r in results]
    avg_len = sum(reason_lens) / len(reason_lens) if reason_lens else 0
    short_count = sum(1 for l in reason_lens if l < 20)

    sample_text = ""
    for i, s in enumerate(samples, 1):
        sample_text += (f"\n【样本{i}】标题: {s.get('title', '未知')}\n"
                        f"分数: {s.get('score', '无')}分\n"
                        f"评分理由: {(s.get('reason') or '无')[:300]}\n")

    prompt = f"""你是一位资深作文评分审核专家。请评估以下 AI 对上海高考模拟作文的评分理由质量。

评分标准 (满分 30):

1. **针对性** (0-10): 评语是否针对每篇作文的具体内容, 而非通用模板。
   - 10: 精准提及该作文具体论点、论据或语言特点
   - 7-9: 大部分有针对性, 少数模板化
   - 4-6: 有一定针对性但模板化严重
   - 0-3: 几乎全部模板化

2. **专业性** (0-10): 评语是否体现作文评价的专业素养。
   - 10: 从思想内容、结构逻辑、语言表达、规范文面多维度分析
   - 7-9: 涵盖多维度, 分析较深入
   - 4-6: 涉及部分维度, 分析较浅
   - 0-3: 过于简单

3. **区分度** (0-10): 不同分数段作文评语是否体现明显质量差异。
   - 10: 高分明确优秀之处, 低分明确不足
   - 7-9: 可看出差异
   - 4-6: 差异不够明显
   - 0-3: 无法区分

样本 ({len(samples)} 篇):
{sample_text}

统计: 共 {n} 篇, 平均评语 {avg_len:.0f} 字, {short_count} 篇 <20 字。

请严格按 JSON 输出 (不含其他内容):
```json
{{
  "specificity": {{"score": 0, "reason": ""}},
  "professionalism": {{"score": 0, "reason": ""}},
  "differentiation": {{"score": 0, "reason": ""}},
  "summary": ""
}}
```"""

    config = _get_text_eval_config(answer_dir)
    llm_resp = _call_llm_judge(prompt, config)

    if llm_resp:
        try:
            jm = re.search(r'\{.*\}', llm_resp, re.DOTALL)
            if jm:
                obj = json.loads(jm.group())
                s1 = max(0, min(10, int(obj.get("specificity", {}).get("score", 0))))
                s2 = max(0, min(10, int(obj.get("professionalism", {}).get("score", 0))))
                s3 = max(0, min(10, int(obj.get("differentiation", {}).get("score", 0))))
                total = s1 + s2 + s3
                d["针对性"] = f"{s1}/10 — {obj.get('specificity', {}).get('reason', '')}"
                d["专业性"] = f"{s2}/10 — {obj.get('professionalism', {}).get('reason', '')}"
                d["区分度"] = f"{s3}/10 — {obj.get('differentiation', {}).get('reason', '')}"
                d["总评"] = obj.get("summary", "")
                d["评估模型"] = config.get("model", "unknown")
                return total, d
        except (json.JSONDecodeError, ValueError, TypeError) as e:
            d["LLM 解析错误"] = str(e)

    # 降级评估 (上限 12/30)
    print("[RUBRIC] LLM 不可用, 使用降级评估")
    fb = 0
    if avg_len >= 80:
        fb += 5
    elif avg_len >= 40:
        fb += 3
    elif avg_len >= 20:
        fb += 1
    d["平均评语长度"] = f"{avg_len:.0f} 字"

    unique_starts = len(set(
        (r.get("reason") or "")[:50] for r in results if r.get("reason")
    ))
    div = unique_starts / n if n else 0
    if div >= 0.80:
        fb += 5
    elif div >= 0.50:
        fb += 3
    elif div >= 0.30:
        fb += 1
    d["评语多样性"] = f"{unique_starts}/{n} 篇前50字不同 ({div * 100:.0f}%)"

    if short_count == 0:
        fb += 2
    elif short_count <= n * 0.10:
        fb += 1
    d["过短评语"] = f"{short_count} 篇 <20 字"
    d["注意"] = "LLM 不可用, 降级评估 (上限 12/30)"

    return min(fb, 12), d

# ---------------------------------------------------------------------------
# 主入口
# ---------------------------------------------------------------------------

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    评估 Agent 的作文评分输出.

    Args:
        answer_dir: Agent 输出目录绝对路径 (如 .../gpt-5/attempt_1)

    Returns:
        (score, report)  score: 0-100 整数; report: dict
    """
    result_path = _find_result_file(answer_dir)
    raw = _read_file(result_path) if result_path else ""
    results = _parse_results(raw) if raw else []
    ref_scores = _extract_reference_scores(answer_dir)

    s1, d1 = _dim_file_delivery(answer_dir)
    s2, d2 = _dim_format(results, raw)
    s3, d3 = _dim_completeness(results)
    s4, d4 = _dim_score_quality(results, ref_scores)
    s5, d5 = _dim_comment_quality(results, answer_dir)

    total = max(0, min(100, s1 + s2 + s3 + s4 + s5))

    report: Dict[str, Any] = {
        "总分": total,
        "维度得分": {
            "文件交付": f"{s1}/10",
            "格式规范": f"{s2}/15",
            "评分完整性": f"{s3}/20",
            "评分合理性": f"{s4}/25",
            "评语质量": f"{s5}/30",
        },
        "详情": {
            "一、文件交付 (10分)": d1,
            "二、格式规范 (15分)": d2,
            "三、评分完整性 (20分)": d3,
            "四、评分合理性 (25分)": d4,
            "五、评语质量 (30分)": d5,
        },
        "统计": {
            "解析篇数": len(results),
            "有分数篇数": sum(1 for r in results if r.get("score") is not None),
            "参考分数量": len(ref_scores),
        },
    }
    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """打印格式化评分报告."""
    print("=" * 70)
    print("作文评分系统 — 评估报告")
    print("=" * 70)
    print(f"\n总分: {score}/100\n")

    dims = report.get("维度得分", {})
    if dims:
        print("维度得分:")
        for k, v in dims.items():
            print(f"  {k}: {v}")

    stats = report.get("统计", {})
    if stats:
        print(f"\n统计:")
        for k, v in stats.items():
            print(f"  {k}: {v}")

    details = report.get("详情", {})
    for sec_name, sec_data in details.items():
        print(f"\n{'─' * 50}")
        print(f"【{sec_name}】")
        print(f"{'─' * 50}")
        if isinstance(sec_data, dict):
            for k, v in sec_data.items():
                print(f"  {k}: {v}")
        else:
            print(f"  {sec_data}")

    print(f"\n{'=' * 70}")


if __name__ == "__main__":
    import sys
    test_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "gpt-5", "attempt_1"
    )
    if os.path.exists(test_dir):
        print(f"评估目录: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"目录不存在: {test_dir}")
    sys.exit(0)
