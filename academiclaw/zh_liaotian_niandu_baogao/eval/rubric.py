"""
Rubric — DeepSeek 聊天记录年度总结报告生成
总分 100

评分维度（与 description.json rubric.breakdown 一致）：
一、内容完整性（40 分）
    文件交付 (5)  + 结构覆盖 (10) + LLM 完整性评估 (25)
二、分析深度与洞察力（35 分）
    静态深度信号 (10) + LLM 深度评估 (25)
三、数据支持与具体性（25 分）
    静态数据指标 (10) + LLM 具体性评估 (15)
"""

import os
import re
import json
from typing import Tuple, Dict, Any

try:
    import openai
except ImportError:
    openai = None


# ============================================================================
# 环境 / LLM 工具
# ============================================================================

def _load_env(answer_dir: str) -> dict:
    values: dict = {}
    for env_dir in [answer_dir, os.path.join(os.path.dirname(__file__), "..")]:
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
        print(f"[RUBRIC] LLM Judge 调用失败: {e}")
        return ""


def _parse_json(text: str) -> dict:
    if not text:
        return {}
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0].strip()
    elif "```" in text:
        text = text.split("```")[1].split("```")[0].strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r"\{[\s\S]+\}", text)
        if m:
            try:
                return json.loads(m.group())
            except json.JSONDecodeError:
                pass
    return {}


def _read_text(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


def _count_words(text: str) -> int:
    """中文字符数 + 英文单词数（粗略字数统计）"""
    cn = len(re.findall(r"[\u4e00-\u9fff]", text))
    en = len(re.findall(r"[a-zA-Z]+", text))
    return cn + en


# ============================================================================
# 维度一：内容完整性（40 分）
# ============================================================================

def _eval_completeness(report_text: str, has_analysis: bool,
                       answer_dir: str) -> Tuple[int, dict]:
    detail: dict = {}
    score = 0

    # ---- 1a. 文件交付 (5 分) ----
    file_pts = 0
    if report_text:
        file_pts += 4
        detail["report.md"] = "存在 (4/4)"
    else:
        detail["report.md"] = "缺失 (0/4)"
    if has_analysis:
        file_pts += 1
        detail["analysis.json"] = "存在且可解析 (1/1)"
    else:
        detail["analysis.json"] = "缺失或不可解析 (0/1, 可选文件)"
    score += file_pts
    detail["文件交付得分"] = f"{file_pts}/5"

    if not report_text:
        detail["后续检查"] = "report.md 缺失，跳过结构与 LLM 检查"
        return score, detail

    # ---- 1b. 结构覆盖 (10 分) ----
    struct_pts = 0

    # 三大章节 (6 分，每章 2 分)
    chapter_patterns = [
        (r"对话(内容)?分析|内容分析|聊天(记录)?分析", "对话内容分析"),
        (r"用户画像|用户分析|用户(特征|行为)分析", "用户画像分析"),
        (r"年终总结|年度总结|总结(与|和|及)建议|总结.*展望", "年终总结与建议"),
    ]
    chapter_hits = []
    for pat, name in chapter_patterns:
        hit = bool(re.search(pat, report_text))
        chapter_hits.append((name, hit))
        if hit:
            struct_pts += 2

    detail["章节覆盖"] = {n: ("有" if h else "无") for n, h in chapter_hits}

    # 子主题 (4 分)
    sub_patterns = [
        (r"主题(分类|分布|类别|归类)", "主题分类"),
        (r"频次|频率|次数", "频次统计"),
        (r"时间(分布|特征)|活跃时段|时段", "时间分布"),
        (r"高频问题|对话模式|交互模式|常见(问题|模式)", "对话模式"),
        (r"(模型)?回复(类型|特点|风格)|DeepSeek.*回答", "模型回复特点"),
        (r"专业背景|兴趣领域|职业|教育(阶段)?", "用户背景推断"),
        (r"使用场景|需求类型", "使用场景"),
        (r"(对话|交互)(风格|特征)", "交互特征"),
        (r"(关键|重要)(对话|年度)?(成果|亮点)|里程碑", "关键成果"),
        (r"(优化|改进|未来)(的)?建议|下一步", "优化建议"),
    ]
    sub_hits = [(name, bool(re.search(pat, report_text)))
                for pat, name in sub_patterns]
    sub_hit_count = sum(1 for _, h in sub_hits if h)

    if sub_hit_count >= 8:
        struct_pts += 4
    elif sub_hit_count >= 6:
        struct_pts += 3
    elif sub_hit_count >= 4:
        struct_pts += 2
    elif sub_hit_count >= 2:
        struct_pts += 1

    detail["子主题命中"] = f"{sub_hit_count}/{len(sub_patterns)}"
    detail["子主题详情"] = {n: ("有" if h else "无") for n, h in sub_hits}
    score += struct_pts
    detail["结构覆盖得分"] = f"{struct_pts}/10"

    # ---- 1c. LLM 完整性评估 (25 分) ----
    snippet = report_text[:5000]
    wc = _count_words(report_text)
    config = _get_text_eval_config(answer_dir)

    prompt = f"""你是一位严格的报告评审专家。以下是一份基于 107 条 DeepSeek 聊天记录生成的年度总结报告（可能截断），实际全文约 {wc} 字。

任务要求报告包含：
1) 对话内容分析：主题分类与频次分布、高频问题与关键对话模式、时间分布特征、模型回复类型与特点
2) 用户画像分析：专业背景/兴趣领域、使用场景与需求类型、对话风格与交互特征、职业/教育阶段推断
3) 年终总结与建议：年度关键对话成果、协作模式演变、亮点与特殊时刻、未来对话优化建议
4) 格式要求：结构化章节（标题+要点列表）、数据可视化描述（文字描述统计图表）、具体示例引用、长度约 1000 字

请从【内容完整性】角度评分（0-25 分）：
- 22-25: 三大部分充实完整，子主题覆盖 >=90%，有可视化描述，长度合理
- 17-21: 三大部分基本完整，子主题覆盖 >=70%，有部分可视化描述
- 12-16: 覆盖两大部分或三部分内容单薄，子主题覆盖 50-70%
- 7-11: 只覆盖一到两部分，内容较少
- 0-6: 内容严重不足或与任务无关

请严格返回 JSON：
```json
{{"completeness_score": 0, "reason": ""}}
```

报告内容：
---
{snippet}
---"""

    llm_raw = _call_llm_judge(prompt, config)
    llm_data = _parse_json(llm_raw)
    llm_pts = max(0, min(25, int(llm_data.get("completeness_score", 0))))

    if not llm_data:
        llm_pts = min(15, struct_pts * 2)
        detail["LLM完整性评估"] = f"{llm_pts}/25 (LLM 不可用，回退)"
    else:
        detail["LLM完整性评估"] = f"{llm_pts}/25"
        detail["LLM完整性理由"] = llm_data.get("reason", "")

    score += llm_pts
    detail["内容完整性总分"] = f"{score}/40"
    return score, detail


# ============================================================================
# 维度二：分析深度与洞察力（35 分）
# ============================================================================

def _eval_depth(report_text: str, answer_dir: str) -> Tuple[int, dict]:
    detail: dict = {}
    score = 0

    if not report_text:
        return 0, {"错误": "report.md 缺失"}

    # ---- 2a. 静态深度信号 (10 分) ----
    depth_signals = [
        (r"(偏好|喜好|倾向|兴趣|习惯)", "用户偏好/兴趣"),
        (r"(趋势|变化|演变|发展|转变|过渡)", "趋势/演变"),
        (r"(推断|推测|表明|说明|反映|可见)", "推断与归因"),
        (r"(因为|由于|导致|原因|因此|所以)", "因果分析"),
        (r"(对比|比较|不同|区别|差异|相较)", "对比分析"),
    ]
    hits = [(name, bool(re.search(pat, report_text)))
            for pat, name in depth_signals]
    hit_count = sum(1 for _, h in hits if h)

    if hit_count >= 4:
        static_pts = 10
    elif hit_count >= 3:
        static_pts = 7
    elif hit_count >= 2:
        static_pts = 4
    elif hit_count >= 1:
        static_pts = 2
    else:
        static_pts = 0

    detail["深度信号命中"] = f"{hit_count}/{len(depth_signals)}"
    detail["深度信号详情"] = {n: ("有" if h else "无") for n, h in hits}
    detail["静态深度得分"] = f"{static_pts}/10"
    score += static_pts

    # ---- 2b. LLM 深度评估 (25 分) ----
    snippet = report_text[:5000]
    config = _get_text_eval_config(answer_dir)

    prompt = f"""你是一位严格的分析报告评审专家。以下是一份基于 107 条用户与 DeepSeek 模型聊天记录的年度总结报告。

请从【分析深度与洞察力】角度评分（0-25 分），考虑三个子维度：

A. 用户画像深度（0-10）：
- 是否有超越表面的深入推断？（如从对话推断"研究生，从事 AI 语音方向"而非仅说"使用了 DeepSeek"）
- 是否总结了使用习惯、偏好模式、对话风格？
- 是否结合多条记录进行交叉推断？

B. 洞察力与趋势识别（0-10）：
- 是否识别出内容趋势变化？（如"从基础配置过渡到深入技术讨论"）
- 是否发现异常或亮点时刻？（如"某段时间密集讨论 CosyVoice"）
- 是否有非显而易见的洞察？

C. 建议可操作性（0-5）：
- 建议是否具体可操作？（如"建议使用更结构化的 prompt"而非"继续使用 DeepSeek"）
- 是否基于前面分析得出？

评分标准：
- 21-25: 深入画像、敏锐趋势洞察、具体可操作建议
- 16-20: 分析较深入，有一定洞察，建议基本可操作
- 11-15: 分析停留表面，洞察平庸，建议笼统
- 6-10: 分析浅薄，缺乏洞察
- 0-5: 几乎没有分析

请严格返回 JSON：
```json
{{"depth_score": 0, "portrait_score": 0, "insight_score": 0, "suggestion_score": 0, "reason": ""}}
```

报告内容：
---
{snippet}
---"""

    llm_raw = _call_llm_judge(prompt, config)
    llm_data = _parse_json(llm_raw)
    llm_pts = max(0, min(25, int(llm_data.get("depth_score", 0))))

    if not llm_data:
        llm_pts = min(12, static_pts)
        detail["LLM深度评估"] = f"{llm_pts}/25 (LLM 不可用，回退)"
    else:
        detail["LLM深度评估"] = f"{llm_pts}/25"
        detail["LLM深度子项"] = {
            "用户画像": llm_data.get("portrait_score", "N/A"),
            "洞察力": llm_data.get("insight_score", "N/A"),
            "建议可操作性": llm_data.get("suggestion_score", "N/A"),
        }
        detail["LLM深度理由"] = llm_data.get("reason", "")

    score += llm_pts
    detail["分析深度总分"] = f"{score}/35"
    return score, detail


# ============================================================================
# 维度三：数据支持与具体性（25 分）
# ============================================================================

def _eval_data_support(report_text: str, analysis_data: dict,
                       answer_dir: str) -> Tuple[int, dict]:
    detail: dict = {}
    score = 0

    if not report_text:
        return 0, {"错误": "report.md 缺失"}

    # ---- 3a. 静态数据指标 (10 分) ----
    static_pts = 0

    # 数字/百分比/频次引用
    num_matches = re.findall(
        r"\d+%|\d+\s*条|\d+\s*次|\d+\s*篇|\d+\s*个|约\s*\d+|共\s*\d+"
        r"|\d{1,2}点|\d{1,2}时|周[一二三四五六日]",
        report_text,
    )
    num_count = len(num_matches)
    if num_count >= 10:
        static_pts += 4
    elif num_count >= 6:
        static_pts += 3
    elif num_count >= 3:
        static_pts += 2
    elif num_count >= 1:
        static_pts += 1
    detail["数据引用数量"] = num_count

    # 示例引用（引用具体聊天记录名或内容）
    example_pats = [
        r"(例如|如：|比如|举例)",
        r"DeepSeek-[^\s\"）)]+\.md",
        r"[「「](.*?)[」」]",
        r'"[^"]{5,}"',
    ]
    example_hits = sum(bool(re.search(p, report_text)) for p in example_pats)
    if example_hits >= 3:
        static_pts += 3
    elif example_hits >= 2:
        static_pts += 2
    elif example_hits >= 1:
        static_pts += 1
    detail["示例引用命中"] = f"{example_hits}/{len(example_pats)}"

    # analysis.json 加分
    if analysis_data:
        useful_keys = ["topics", "theme_counts", "time_distribution",
                       "total_records", "categories", "top_keywords",
                       "reply_type_counts"]
        key_hits = sum(
            1 for k in useful_keys
            if any(k in str(ak).lower() for ak in analysis_data.keys())
        )
        if key_hits >= 2:
            static_pts += 3
        elif key_hits >= 1:
            static_pts += 2
        detail["analysis.json有效键"] = key_hits
    else:
        detail["analysis.json"] = "未提供"

    static_pts = min(10, static_pts)
    score += static_pts
    detail["静态数据检查得分"] = f"{static_pts}/10"

    # ---- 3b. LLM 具体性评估 (15 分) ----
    snippet = report_text[:5000]
    config = _get_text_eval_config(answer_dir)

    prompt = f"""你是一位严格的报告评审专家。以下是一份基于 107 条 DeepSeek 聊天记录的年度总结报告。

请从【数据支持与具体性】角度评分（0-15 分），考虑：

A. 数据准确性（0-5）：
- 统计数据是否合理？（如主题分布频次加起来是否接近 107 条）
- 百分比和数字是否自洽？
- 是否有明显编造的数据？

B. 具体示例引用（0-5）：
- 是否引用了具体的聊天记录标题或内容？
- 引用是否恰当支撑论点？
- 注意：107 条记录以 "DeepSeek-*.md" 命名的 Markdown 文件形式存在

C. 避免笼统空泛（0-5）：
- 结论是否有具体数据/事实支撑？
- 是否避免了"广泛涉猎""积极互动"等空泛描述？

评分标准：
- 13-15: 数据准确、示例丰富准确、结论扎实
- 10-12: 数据基本准确、有示例引用、偶有笼统
- 7-9: 数据一般、示例较少、部分结论空泛
- 4-6: 数据稀少或不准确、缺少示例
- 0-3: 几乎没有数据支持

请严格返回 JSON：
```json
{{"data_support_score": 0, "accuracy_score": 0, "example_score": 0, "specificity_score": 0, "reason": ""}}
```

报告内容：
---
{snippet}
---"""

    llm_raw = _call_llm_judge(prompt, config)
    llm_data = _parse_json(llm_raw)
    llm_pts = max(0, min(15, int(llm_data.get("data_support_score", 0))))

    if not llm_data:
        llm_pts = min(8, static_pts)
        detail["LLM具体性评估"] = f"{llm_pts}/15 (LLM 不可用，回退)"
    else:
        detail["LLM具体性评估"] = f"{llm_pts}/15"
        detail["LLM具体性子项"] = {
            "数据准确性": llm_data.get("accuracy_score", "N/A"),
            "示例引用": llm_data.get("example_score", "N/A"),
            "具体性": llm_data.get("specificity_score", "N/A"),
        }
        detail["LLM具体性理由"] = llm_data.get("reason", "")

    score += llm_pts
    detail["数据支持总分"] = f"{score}/25"
    return score, detail


# ============================================================================
# 主入口
# ============================================================================

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    评估 agent 的输出。

    Args:
        answer_dir: agent 输出目录的绝对路径

    Returns:
        (score, report) — score: 0-100 整数, report: 详细评估报告
    """
    # 加载文件
    files = os.listdir(answer_dir) if os.path.isdir(answer_dir) else []

    report_file = next((f for f in files if f.lower() == "report.md"), None)
    analysis_file = next((f for f in files if f.lower() == "analysis.json"), None)

    report_text = ""
    if report_file:
        report_text = _read_text(os.path.join(answer_dir, report_file))

    analysis_data: dict = {}
    has_analysis = False
    if analysis_file:
        try:
            with open(os.path.join(answer_dir, analysis_file), "r",
                       encoding="utf-8") as f:
                analysis_data = json.load(f)
            has_analysis = True
        except Exception:
            pass

    # 三个维度评估
    s1, r1 = _eval_completeness(report_text, has_analysis, answer_dir)
    s2, r2 = _eval_depth(report_text, answer_dir)
    s3, r3 = _eval_data_support(report_text, analysis_data, answer_dir)

    total = s1 + s2 + s3

    if total >= 90:
        comment = "优秀！报告结构完整、分析深入、数据支持充分。"
    elif total >= 75:
        comment = "良好。报告覆盖主要内容，分析较充分，仍有提升空间。"
    elif total >= 60:
        comment = "及格。基本覆盖要求内容，但分析深度或数据支持有不足。"
    elif total >= 40:
        comment = "部分完成。有一定内容，但关键维度存在明显不足。"
    else:
        comment = "不达标。请补充结构、分析与数据支持。"

    report: Dict[str, Any] = {
        "总分": total,
        "结果评分": {
            "一、内容完整性 (40分)": {"得分": s1, "详情": r1},
            "二、分析深度与洞察力 (35分)": {"得分": s2, "详情": r2},
            "三、数据支持与具体性 (25分)": {"得分": s3, "详情": r3},
        },
        "过程评分": {},
        "评语": comment,
        "分项得分": {
            "内容完整性": f"{s1}/40",
            "分析深度与洞察力": f"{s2}/35",
            "数据支持与具体性": f"{s3}/25",
        },
    }

    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """打印格式化的评分报告"""
    print("=" * 70)
    print("DeepSeek 聊天记录年度总结报告 — 评分报告")
    print("=" * 70)
    print(f"\n总分：{score}/100\n")

    scores = report.get("分项得分", {})
    if scores:
        print("分项得分:")
        for k, v in scores.items():
            print(f"  {k}: {v}")

    for section_name, section_data in report.get("结果评分", {}).items():
        print(f"\n{'─' * 60}")
        print(f"【{section_name}】 得分: {section_data.get('得分', 0)}")
        print(f"{'─' * 60}")
        detail = section_data.get("详情", {})
        for k, v in detail.items():
            if isinstance(v, dict):
                print(f"  {k}:")
                for kk, vv in v.items():
                    print(f"    {kk}: {vv}")
            else:
                print(f"  {k}: {v}")

    print(f"\n{'=' * 70}")
    print(f"评语：{report.get('评语', '')}")
    print("=" * 70)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        test_dir = sys.argv[1]
    else:
        test_dir = os.path.join(os.path.dirname(__file__), "..", "gpt-5", "attempt_1")
    if os.path.isdir(test_dir):
        print(f"正在评估目录: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"目录不存在: {test_dir}")
    sys.exit(0)
