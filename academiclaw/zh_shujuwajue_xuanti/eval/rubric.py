"""
eval/rubric.py — 数据挖掘课程项目选题与实施计划制定
Task: create/plan/jingyuzhou-query4

任务概述:
  Agent 需要阅读《AI3602 数据挖掘 期末课程项目安排》PDF，产出 plan.md 文件，内容包含：
  1. 选题策划 — 从"源代码数据挖掘"或"图数据挖掘"中选方向，构思创新题目
  2. 项目执行方案 — 数据集、核心算法、实验设置
  3. 展示材料设计 — A1 海报结构大纲

评分维度 (总分 100):
  D1. 文件交付与格式 (10 分) — 确定性检查
  D2. 选题合规性与创新性 (25 分) — 关键词 + LLM
  D3. 方案科学性与完整性 (30 分) — 关键词 + LLM
  D4. 展示设计针对性 (20 分) — 关键词 + LLM
  D5. 文档约束遵循 (15 分) — 关键词 + LLM
"""

import os
import re
import json
from typing import Tuple, Dict, Any, Optional, List

try:
    import openai
except ImportError:
    openai = None


# ============================================================
# 环境与 LLM 工具
# ============================================================

def _load_env(answer_dir: str) -> dict:
    """从 answer_dir 和 query 根目录加载 .env"""
    values: dict = {}
    query_root = os.path.join(os.path.dirname(__file__), "..")
    for d in [answer_dir, query_root]:
        env_path = os.path.join(d, ".env")
        if not os.path.exists(env_path):
            continue
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    key = k.strip()
                    if key not in values:
                        values[key] = v.strip().strip("'\"")
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
            max_tokens=4096,
            temperature=0,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        print(f"[RUBRIC] LLM Judge 调用失败: {e}")
        return ""


def _extract_json(text: str) -> Optional[dict]:
    """从 LLM 回复中提取 JSON 对象"""
    # 尝试 ```json ... ``` 块
    for pat in [r"```json\s*([\s\S]*?)\s*```", r"```\s*([\s\S]*?)\s*```"]:
        for m in re.finditer(pat, text):
            try:
                obj = json.loads(m.group(1))
                if isinstance(obj, dict):
                    return obj
            except json.JSONDecodeError:
                continue
    # 尝试整段
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        pass
    # 尝试从后向前找最外层 {}
    depth = 0
    end = -1
    for i in range(len(text) - 1, -1, -1):
        if text[i] == "}":
            if depth == 0:
                end = i
            depth += 1
        elif text[i] == "{":
            depth -= 1
            if depth == 0 and end != -1:
                try:
                    obj = json.loads(text[i : end + 1])
                    if isinstance(obj, dict):
                        return obj
                except json.JSONDecodeError:
                    pass
    return None


# ============================================================
# D1. 文件交付与格式 (10 分)
# ============================================================

def _locate_plan(answer_dir: str) -> Optional[str]:
    """在 answer_dir 中定位计划文档，优先精确匹配 plan.md"""
    if not os.path.isdir(answer_dir):
        return None
    primary = ["plan.md", "Plan.md", "PLAN.md"]
    for name in primary:
        p = os.path.join(answer_dir, name)
        if os.path.exists(p):
            return p
    # 回退：任意 .md（排除输入文件）
    skip = {"query.md", "TASK_PROMPT.md", "README.md"}
    for f in sorted(os.listdir(answer_dir)):
        if f.lower().endswith(".md") and f not in skip:
            return os.path.join(answer_dir, f)
    # 回退：.txt
    for f in sorted(os.listdir(answer_dir)):
        if f.lower().endswith(".txt"):
            return os.path.join(answer_dir, f)
    return None


def _eval_delivery(answer_dir: str) -> Tuple[int, dict, str]:
    """
    D1 (10 分):
      plan.md 存在 (4) | 文件名精确匹配 (2) | 长度 >= 1000 字 (2) | >= 3 个标题 (2)
    返回 (score, details, content)
    """
    score = 0
    details: dict = {}
    content = ""

    path = _locate_plan(answer_dir)
    if path is None:
        details["文件存在"] = "0/4 — 未找到计划文档"
        details["文件名"] = "0/2"
        details["长度"] = "0/2"
        details["标题数"] = "0/2"
        return 0, details, ""

    # 存在 +4
    score += 4
    basename = os.path.basename(path)
    details["文件存在"] = f"4/4 — {basename}"

    # 精确文件名 +2
    if basename == "plan.md":
        score += 2
        details["文件名"] = "2/2 — plan.md"
    else:
        details["文件名"] = f"0/2 — 实际 {basename}"

    # 读取内容
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        details["长度"] = f"0/2 — 读取失败: {e}"
        details["标题数"] = "0/2"
        return score, details, ""

    # 长度 +2
    clen = len(content.strip())
    if clen >= 1000:
        score += 2
        details["长度"] = f"2/2 — {clen} 字符"
    elif clen >= 500:
        score += 1
        details["长度"] = f"1/2 — {clen} 字符 (偏短)"
    else:
        details["长度"] = f"0/2 — {clen} 字符 (过短)"

    # 标题数 +2
    headings = re.findall(r"^#{1,3}\s+.+", content, re.MULTILINE)
    if len(headings) >= 3:
        score += 2
        details["标题数"] = f"2/2 — {len(headings)} 个"
    elif len(headings) >= 1:
        score += 1
        details["标题数"] = f"1/2 — {len(headings)} 个"
    else:
        details["标题数"] = "0/2 — 未检测到标题"

    return score, details, content


# ============================================================
# D2-D5 关键词 fallback 评分
# ============================================================

def _keyword_fallback(content: str) -> Tuple[int, int, int, int, dict]:
    """
    当 LLM 不可用时，用关键词给保守分。
    返回 (d2, d3, d4, d5, kw_info)
    """
    low = content.lower()
    info: dict = {}

    # --- D2 选题 (max 25) ---
    d2 = 0
    dir_kws = ["源代码数据挖掘", "图数据挖掘", "source code mining",
                "graph data mining", "graph mining", "code mining"]
    dir_hit = any(k.lower() in low for k in dir_kws)
    if dir_hit:
        d2 += 8
    info["方向命中"] = dir_hit

    inn_kws = ["创新", "innovation", "novel", "改进", "propose", "提出",
               "新颖", "独特", "首次"]
    inn_cnt = sum(1 for k in inn_kws if k.lower() in low)
    if inn_cnt >= 3:
        d2 += 9
    elif inn_cnt >= 1:
        d2 += 4
    info["创新关键词"] = inn_cnt

    # --- D3 方案 (max 30) ---
    d3 = 0
    ds_hit = any(k.lower() in low for k in ["数据集", "dataset", "corpus", "语料"])
    alg_hit = any(k.lower() in low for k in [
        "算法", "algorithm", "模型", "model", "gnn", "bert",
        "transformer", "gcn", "gat", "random walk", "node2vec",
    ])
    exp_hit = any(k.lower() in low for k in [
        "实验", "experiment", "baseline", "对比", "评估指标",
        "accuracy", "auc", "f1", "消融", "ablation",
    ])
    elem = sum([ds_hit, alg_hit, exp_hit])
    d3 += min(12, elem * 4)
    info["三要素"] = f"数据集{'Y' if ds_hit else 'N'} 算法{'Y' if alg_hit else 'N'} 实验{'Y' if exp_hit else 'N'}"

    comp_hit = any(k.lower() in low for k in [
        "对比实验", "baseline", "消融实验", "ablation",
    ])
    if comp_hit:
        d3 += 5
    info["对比/消融"] = comp_hit

    # --- D4 展示 (max 20) ---
    d4 = 0
    poster_kws = ["海报", "poster", "a1", "板块", "展示材料"]
    poster_cnt = sum(1 for k in poster_kws if k.lower() in low)
    if poster_cnt >= 3:
        d4 += 7
    elif poster_cnt >= 1:
        d4 += 3
    think_hit = any(k.lower() in low for k in [
        "思考过程", "problem solving", "解决思路", "动机", "motivation",
    ])
    result_hit = any(k.lower() in low for k in [
        "结果分析", "result analysis", "讨论", "discussion", "实验结果",
    ])
    if think_hit and result_hit:
        d4 += 5
    elif think_hit or result_hit:
        d4 += 2
    info["海报关键词"] = poster_cnt
    info["思考过程"] = think_hit
    info["结果分析"] = result_hit

    # --- D5 文档约束 (max 15) ---
    d5 = 0
    ref_kws = [
        "评分标准", "选题（10%）", "选题(10%)", "问题与创新性（20%）",
        "工作量", "完成度", "技术正确性", "展示材料",
        "汇报", "参考选题", "ai3602", "期末项目",
    ]
    ref_cnt = sum(1 for k in ref_kws if k.lower() in low)
    if ref_cnt >= 5:
        d5 += 9
    elif ref_cnt >= 3:
        d5 += 6
    elif ref_cnt >= 1:
        d5 += 3
    info["文档引用词数"] = ref_cnt

    return d2, d3, d4, d5, info


# ============================================================
# D2-D5 LLM-as-Judge 综合评估
# ============================================================

_JUDGE_PROMPT = """\
你是一位严格的数据挖掘课程教授。请对以下学生提交的项目选题与实施计划文档进行评分。

## 课程背景
课程为 AI3602 数据挖掘，期末课程项目评分标准（摘自课程文档）：
- 选题 (10%): 数据挖掘相关、有实际意义
- 问题与创新性 (20%): 问题定义清楚、有创新性
- 工作量/完成度 (15%): 工作量充分、实验或系统完整
- 技术正确性 (15%): 科学方法正确、实现与实验设计合理
- 展示材料 (20%): 清晰、重点突出、吸引人
- 汇报 (20%): 表达清晰、流畅
参考选题范围包括但不限于：推荐系统、图数据挖掘、源代码数据挖掘、时间序列等。

## 任务要求
学生需要选择"源代码数据挖掘"或"图数据挖掘"方向，完成：
1. 选题策划（含创新性阐述、对应评分标准中的"选题10%"和"问题与创新性20%"）
2. 项目执行方案（数据集、算法、实验设置，满足"工作量/完成度15%"和"技术正确性15%"）
3. A1 海报结构大纲（各板块标题和内容摘要，体现"思考过程"和"结果分析"）

## 评分维度

### 维度 A — 选题合规性与创新性 (0-25 分)
- 是否选择了指定方向（源代码数据挖掘/图数据挖掘）(0-8)
  0: 未选指定方向 | 4: 选了但理由不充分 | 8: 方向正确且理由充分
- 创新性论述是否清晰，是否对应"选题10%"和"问题与创新性20%" (0-17)
  0: 未提创新 | 7: 提了但模糊 | 13: 有明确创新点且对应评分 | 17: 论证严密

### 维度 B — 方案科学性与完整性 (0-30 分)
- 数据集/算法/实验三要素 (0-12): 缺2+ = 0 | 1个 = 4 | 2个 = 8 | 3个 = 12
- 实验设计体现技术正确性 (0-10): 无对比且指标缺 = 0 | 有指标无对比 = 5 | 有对比且合理 = 10
- 工作量是否充足 (0-8): 仅复现 = 0-3 | 有改进 = 4-5 | 显著工作量 = 6-8

### 维度 C — 展示设计针对性 (0-20 分)
- 海报大纲结构 (0-8): 无 = 0 | 有标题但不完整 = 4 | 清晰完整 = 8
- "思考过程"和"结果分析"板块 (0-8): 均无 = 0 | 一项 = 4 | 均有 = 8
- 吸引听众/突出重点 (0-4): 未考虑 = 0 | 有考虑 = 2-4

### 维度 D — 文档约束遵循 (0-15 分)
- 是否利用课程文档信息（评分权重、参考选题等）(0-15)
  0-4: 未体现 | 5-9: 部分利用 | 10-15: 全面利用

## 学生提交文档

{content}

## 输出要求
1. 对每个维度给分并附 1-2 句理由
2. 严格评分，空洞泛泛不给高分
3. 以如下 JSON 格式输出（放在 ```json ``` 块中）：

```json
{{
  "topic_innovation": {{"score": 0, "reason": ""}},
  "plan_completeness": {{"score": 0, "reason": ""}},
  "presentation_design": {{"score": 0, "reason": ""}},
  "document_compliance": {{"score": 0, "reason": ""}},
  "total": 0
}}
```
"""


def _clamp(val: Any, lo: int, hi: int) -> int:
    try:
        return max(lo, min(hi, int(val)))
    except (TypeError, ValueError):
        return lo


def _llm_judge(content: str, config: dict) -> Optional[Tuple[int, int, int, int, dict]]:
    """用 LLM 评估维度 D2-D5，返回 (d2, d3, d4, d5, details) 或 None"""
    prompt = _JUDGE_PROMPT.format(content=content[:12000])
    raw = _call_llm_judge(prompt, config)
    if not raw:
        return None
    data = _extract_json(raw)
    if not data:
        print("[RUBRIC] LLM 返回无法解析为 JSON，降级到关键词评分")
        return None

    ti = data.get("topic_innovation", {})
    pc = data.get("plan_completeness", {})
    pd_ = data.get("presentation_design", {})
    dc = data.get("document_compliance", {})

    d2 = _clamp(ti.get("score"), 0, 25)
    d3 = _clamp(pc.get("score"), 0, 30)
    d4 = _clamp(pd_.get("score"), 0, 20)
    d5 = _clamp(dc.get("score"), 0, 15)

    details = {
        "选题合规性与创新性": f"{d2}/25 — {ti.get('reason', '')}",
        "方案科学性与完整性": f"{d3}/30 — {pc.get('reason', '')}",
        "展示设计针对性": f"{d4}/20 — {pd_.get('reason', '')}",
        "文档约束遵循": f"{d5}/15 — {dc.get('reason', '')}",
        "_raw": raw,
    }
    return d2, d3, d4, d5, details


# ============================================================
# 主入口
# ============================================================

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    评估 agent 的输出。

    Args:
        answer_dir: agent 输出目录的绝对路径

    Returns:
        (score, report)
        - score: 0-100 整数
        - report: dict，包含详细评估报告
    """
    answer_dir = os.path.abspath(answer_dir)
    print(f"[RUBRIC] 评估目录: {answer_dir}")

    # D1: 文件交付
    s1, d1, plan_content = _eval_delivery(answer_dir)
    print(f"[RUBRIC] D1 文件交付: {s1}/10")

    if not plan_content.strip():
        report = {
            "总分": 0,
            "结果评分": {
                "分数": 0,
                "详情": {"D1 文件交付 (10)": d1},
                "扣分原因": ["未找到有效的计划文档"],
            },
            "过程评分": {"分数": 0, "详情": {}, "扣分原因": []},
            "评语": "未提交计划文档或文档内容为空。",
        }
        return 0, report

    # D2-D5: 内容评估
    config = _get_text_eval_config(answer_dir)
    llm_res = _llm_judge(plan_content, config)

    if llm_res is not None:
        s2, s3, s4, s5, content_info = llm_res
        method = "LLM-as-Judge"
        print(f"[RUBRIC] LLM 评估: 选题={s2} 方案={s3} 展示={s4} 文档={s5}")
    else:
        s2, s3, s4, s5, kw_info = _keyword_fallback(plan_content)
        content_info = {
            "选题合规性与创新性": f"{s2}/25 (关键词估分)",
            "方案科学性与完整性": f"{s3}/30 (关键词估分)",
            "展示设计针对性": f"{s4}/20 (关键词估分)",
            "文档约束遵循": f"{s5}/15 (关键词估分)",
            "_kw_detail": kw_info,
        }
        method = "关键词备用评分 (LLM 不可用)"
        print(f"[RUBRIC] 关键词备用: 选题={s2} 方案={s3} 展示={s4} 文档={s5}")

    total = max(0, min(100, s1 + s2 + s3 + s4 + s5))

    # 扣分原因汇总
    result_ded: List[str] = []
    process_ded: List[str] = []
    if s2 <= 8:
        result_ded.append("选题方向或创新性论述不足")
    if s3 <= 12:
        result_ded.append("项目执行方案要素不完整或技术深度不够")
    if s4 <= 8:
        process_ded.append("展示材料/海报大纲设计不充分")
    if s5 <= 5:
        process_ded.append("未充分利用课程文档中的评分标准和参考信息")

    # 评语
    if total >= 85:
        comment = "优秀。选题方向正确、方案完整、展示设计到位、充分利用了课程文档。"
    elif total >= 70:
        comment = "良好。基本完成任务要求，但部分维度有改进空间。"
    elif total >= 50:
        comment = "及格。核心内容有涉及但深度不足或存在明显缺失。"
    elif total >= 30:
        comment = "部分完成。关键维度缺失或内容过于空洞。"
    else:
        comment = "不及格。任务完成度严重不足。"

    # 分离 LLM 原始响应
    raw_resp = content_info.pop("_raw", None)
    content_info.pop("_kw_detail", None)

    report: Dict[str, Any] = {
        "总分": total,
        "评分方式": method,
        "结果评分": {
            "分数": s1 + s2 + s3,
            "详情": {
                "D1 文件交付 (10)": d1,
                "D2 选题合规性与创新性 (25)": content_info.get("选题合规性与创新性", ""),
                "D3 方案科学性与完整性 (30)": content_info.get("方案科学性与完整性", ""),
            },
            "扣分原因": result_ded,
        },
        "过程评分": {
            "分数": s4 + s5,
            "详情": {
                "D4 展示设计针对性 (20)": content_info.get("展示设计针对性", ""),
                "D5 文档约束遵循 (15)": content_info.get("文档约束遵循", ""),
            },
            "扣分原因": process_ded,
        },
        "评语": comment,
        "分项得分": {
            "D1 文件交付": f"{s1}/10",
            "D2 选题合规性与创新性": f"{s2}/25",
            "D3 方案科学性与完整性": f"{s3}/30",
            "D4 展示设计针对性": f"{s4}/20",
            "D5 文档约束遵循": f"{s5}/15",
        },
    }

    if raw_resp:
        report["llm_judge_response"] = raw_resp

    print(f"[RUBRIC] 最终得分: {total}/100")
    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """打印格式化的评分报告"""
    sep = "=" * 70
    print(sep)
    print("评分报告 — 数据挖掘课程项目选题与实施计划制定")
    print("任务: create/plan/jingyuzhou-query4")
    print(sep)
    print(f"\n总分: {score}/100")

    scores = report.get("分项得分", {})
    if scores:
        print("\n分项得分:")
        for k, v in scores.items():
            print(f"  {k}: {v}")

    for key, label in [
        ("结果评分", "结果评分 (文件 + 选题 + 方案)"),
        ("过程评分", "过程评分 (展示 + 文档遵循)"),
    ]:
        section = report.get(key, {})
        print(f"\n{'─' * 50}")
        print(f"【{label}】 {section.get('分数', 0)} 分")
        print(f"{'─' * 50}")
        for cat, items in section.get("详情", {}).items():
            if isinstance(items, dict):
                print(f"\n  {cat}:")
                for k2, v2 in items.items():
                    print(f"    {k2}: {v2}")
            else:
                print(f"  {cat}: {items}")
        deds = section.get("扣分原因", [])
        if deds:
            print("\n  扣分原因:")
            for i, r in enumerate(deds, 1):
                print(f"    {i}. {r}")

    if report.get("评分方式"):
        print(f"\n评分方式: {report['评分方式']}")
    print(f"\n{sep}")
    print(f"评语: {report.get('评语', '')}")
    print(sep)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        test_dir = sys.argv[1]
    else:
        test_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "workspace")

    if os.path.exists(test_dir):
        print(f"正在评估目录: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"目录不存在: {test_dir}")
    sys.exit(0)
