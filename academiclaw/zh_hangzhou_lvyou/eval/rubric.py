"""
rubric.py — 杭州旅行规划任务评分脚本

任务概述:
  用户需要 agent 基于 workspace 中提供的信息源（official_attractions.md、
  travel_guides.md、evaluation_criteria.md）为一位首次去杭州的旅客规划
  3 天轻松行程（偏好自然风景 + 历史文化）。

交付物: travel_plan.md
总分: 100 分

评分维度（来自 description.json）:
  一、输出完整性与格式   (20 分)
  二、需求符合度         (30 分)
  三、行程合理性         (30 分)
  四、信息整合与附加值   (20 分)
"""

from __future__ import annotations

import os
import re
import json
from typing import Tuple, Dict, Any, List

try:
    import openai
except ImportError:
    openai = None


# ============================================================================
# 环境与 LLM 工具
# ============================================================================

def _load_env(answer_dir: str) -> dict:
    """从 answer_dir 和 query 根目录加载 .env"""
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
        print(f"[RUBRIC] LLM Judge 调用失败: {e}")
        return ""


def _parse_llm_json(text: str) -> dict:
    if not text:
        return {}
    m = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
    if m:
        text = m.group(1)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start >= 0 and end > start:
            try:
                return json.loads(text[start:end + 1])
            except json.JSONDecodeError:
                pass
    return {}


def _read_file(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception:
        return ""


# ============================================================================
# 辅助: 提取某一天的内容块
# ============================================================================

def _extract_day_block(text: str, day: int) -> str:
    """提取 Day N 对应的文本块"""
    cn_map = {1: "一", 2: "二", 3: "三"}
    cn = cn_map.get(day, str(day))
    patterns = [
        rf"((?:#{1,3}\s*)?Day\s*{day}\b.*?)(?=(?:#{1,3}\s*)?Day\s*\d|\Z)",
        rf"((?:#{1,3}\s*)?第[{cn}{day}]天.*?)(?=(?:#{1,3}\s*)?第[一二三四]天|(?:#{1,3}\s*)?Day\s*\d|\Z)",
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE | re.DOTALL)
        if m:
            return m.group(1)
    return ""


# ============================================================================
# 一、输出完整性与格式 (20 分)
# ============================================================================

def _eval_format(plan: str) -> Tuple[int, dict, List[str]]:
    """
    子维度:
      1a. 文件非空且内容充实     (3 分)
      1b. 包含 3 天行程标记      (6 分, 每天 2 分)
      1c. 每天含上午/下午/晚上   (6 分, 每天每时段 ~0.67 → 取整共 6 分)
      1d. 包含实用贴士/建议部分  (3 分)
      1e. Markdown 结构与可读性  (2 分)
    """
    score = 0
    details: Dict[str, str] = {}
    deductions: List[str] = []

    if not plan.strip():
        return 0, {"错误": "文件为空"}, ["travel_plan.md 为空"]

    char_count = len(plan)

    # 1a. 文件长度 (3 分)
    if char_count >= 2000:
        score += 3
        details["1a 文件长度"] = f"3/3 — {char_count} 字符"
    elif char_count >= 800:
        score += 2
        details["1a 文件长度"] = f"2/3 — {char_count} 字符（偏短）"
    elif char_count >= 200:
        score += 1
        details["1a 文件长度"] = f"1/3 — {char_count} 字符（较短）"
    else:
        details["1a 文件长度"] = f"0/3 — {char_count} 字符（过短）"
        deductions.append("文件内容过短")

    # 1b. 三天行程标记 (6 分)
    day_pats = [
        r"(?:#{1,3}\s*)?(?:Day\s*1|第[一1]天|DAY\s*1)",
        r"(?:#{1,3}\s*)?(?:Day\s*2|第[二2]天|DAY\s*2)",
        r"(?:#{1,3}\s*)?(?:Day\s*3|第[三3]天|DAY\s*3)",
    ]
    day_score = 0
    day_found = []
    for i, pat in enumerate(day_pats, 1):
        if re.search(pat, plan, re.IGNORECASE):
            day_score += 2
            day_found.append(f"Day{i}")
    score += day_score
    details["1b 三天结构"] = f"{day_score}/6 — 找到 {', '.join(day_found) if day_found else '无'}"
    if day_score < 6:
        deductions.append(f"三天行程结构不完整（仅找到 {', '.join(day_found)}）")

    # 1c. 时段覆盖 (6 分, 共 9 个时段 slot，每命中一个 +0.67，四舍五入取整，上限 6)
    slot_pats = {
        "上午": r"(?:上午|Morning|早[上晨]|AM\b)",
        "下午": r"(?:下午|Afternoon|午后|PM\b)",
        "晚上": r"(?:晚上|Evening|夜[间晚游]|晚间)",
    }
    slot_hits = 0
    for day_num in range(1, 4):
        block = _extract_day_block(plan, day_num) or plan
        for _, sp in slot_pats.items():
            if re.search(sp, block, re.IGNORECASE):
                slot_hits += 1
    slot_score = min(6, round(slot_hits * 6 / 9))
    score += slot_score
    details["1c 时段覆盖"] = f"{slot_score}/6 — 命中 {slot_hits}/9 个时段"
    if slot_hits < 7:
        deductions.append(f"部分天的时段划分不完整（{slot_hits}/9）")

    # 1d. 实用贴士/建议部分 (3 分)
    tips_pats = [
        r"(?:#{1,3}\s*)?(?:实用(?:信息|贴士)|贴士|建议|Tips|注意事项|温馨提示|风险提示)",
        r"(?:#{1,3}\s*)?(?:交通.*建议|用餐.*建议|穿着|天气)",
    ]
    if any(re.search(p, plan, re.IGNORECASE) for p in tips_pats):
        score += 3
        details["1d 实用信息"] = "3/3 — 存在实用信息/贴士部分"
    else:
        details["1d 实用信息"] = "0/3 — 未找到实用信息/贴士部分"
        deductions.append("缺少实用贴士或建议部分")

    # 1e. Markdown 结构 (2 分)
    has_headings = bool(re.search(r"^#{1,3}\s", plan, re.MULTILINE))
    has_lists = bool(re.search(r"^[-*]\s", plan, re.MULTILINE))
    md_score = 0
    if has_headings:
        md_score += 1
    if has_lists:
        md_score += 1
    score += md_score
    details["1e Markdown 结构"] = f"{md_score}/2 — 标题={'有' if has_headings else '无'}, 列表={'有' if has_lists else '无'}"

    return score, details, deductions


# ============================================================================
# 二、需求符合度 (30 分) — LLM-as-Judge + 关键词降级
# ============================================================================

_PREFERENCE_PROMPT = """\
你是一位严格的旅行规划评审专家。请评估以下杭州 3 天旅行计划是否符合用户需求。

**用户需求**:
- 6 月去杭州旅游 3 天，第一次去
- 偏好自然风景和历史文化
- 不想太累，希望行程合理

请从以下三个子维度打分（整数），并给出简短理由：

**维度 1: 自然风景覆盖 (0-10)**
- 8-10: 行程包含多个知名自然景点（西湖、西溪湿地、虎跑公园、九溪烟树等），分布合理
- 5-7: 有一些自然景点但覆盖不全
- 2-4: 自然景点偏少
- 0-1: 基本没有自然景点

**维度 2: 历史文化覆盖 (0-10)**
- 8-10: 包含多个历史文化景点（灵隐寺/飞来峰、岳王庙、良渚遗址、运河老街等），有文化介绍
- 5-7: 有一些但不够丰富
- 2-4: 较少
- 0-1: 基本没有

**维度 3: 轻松节奏设计 (0-10)**
- 8-10: 每天 2-3 个主要景点，有休息或弹性安排，避免长距离奔波
- 5-7: 基本合理但部分天偏紧
- 2-4: 行程偏赶
- 0-1: 非常紧凑

请严格按以下 JSON 格式回复（不要包含其他内容）：
```json
{{
  "nature_score": 0,
  "nature_reason": "",
  "culture_score": 0,
  "culture_reason": "",
  "pace_score": 0,
  "pace_reason": ""
}}
```

以下是待评估的旅行计划：

---
{plan}
---
"""


def _eval_preference(plan: str, config: dict) -> Tuple[int, dict, List[str]]:
    details: Dict[str, Any] = {}
    deductions: List[str] = []

    # ---- LLM 评估 ----
    prompt = _PREFERENCE_PROMPT.format(plan=plan[:8000])
    raw = _call_llm_judge(prompt, config)
    parsed = _parse_llm_json(raw)

    if parsed and all(k in parsed for k in ("nature_score", "culture_score", "pace_score")):
        ns = max(0, min(10, int(parsed["nature_score"])))
        cs = max(0, min(10, int(parsed["culture_score"])))
        ps = max(0, min(10, int(parsed["pace_score"])))
        details["2a 自然风景 (LLM)"] = f"{ns}/10 — {parsed.get('nature_reason', '')}"
        details["2b 历史文化 (LLM)"] = f"{cs}/10 — {parsed.get('culture_reason', '')}"
        details["2c 轻松节奏 (LLM)"] = f"{ps}/10 — {parsed.get('pace_reason', '')}"
        details["评估方式"] = "LLM-as-Judge"
        total = ns + cs + ps
    else:
        # ---- 降级: 关键词检查 ----
        details["评估方式"] = "关键词降级（LLM 不可用）"

        nature_kw = ["西湖", "湿地", "公园", "山", "湖", "溪", "森林", "自然",
                     "风景", "植物园", "虎跑", "九溪", "龙井", "三台山"]
        culture_kw = ["寺", "庙", "博物", "古", "遗址", "文化", "历史", "灵隐",
                      "岳", "钱王", "良渚", "运河", "万松书院", "飞来峰"]
        pace_kw = ["轻松", "慢", "休息", "午休", "不累", "舒适", "节奏",
                   "弹性", "机动", "可选", "不赶"]

        n_hits = sum(1 for k in nature_kw if k in plan)
        c_hits = sum(1 for k in culture_kw if k in plan)
        p_hits = sum(1 for k in pace_kw if k in plan)

        ns = 8 if n_hits >= 5 else (5 if n_hits >= 2 else 2)
        cs = 8 if c_hits >= 5 else (5 if c_hits >= 2 else 2)
        ps = 7 if p_hits >= 3 else (4 if p_hits >= 1 else 2)

        details["2a 自然风景 (KW)"] = f"{ns}/10 — 命中 {n_hits} 词"
        details["2b 历史文化 (KW)"] = f"{cs}/10 — 命中 {c_hits} 词"
        details["2c 轻松节奏 (KW)"] = f"{ps}/10 — 命中 {p_hits} 词"
        total = ns + cs + ps

    if ns < 5:
        deductions.append("自然风景覆盖不足")
    if cs < 5:
        deductions.append("历史文化覆盖不足")
    if ps < 5:
        deductions.append("未体现轻松节奏")

    return total, details, deductions


# ============================================================================
# 三、行程合理性 (30 分) — LLM-as-Judge + 关键词降级
# ============================================================================

_LOGISTICS_PROMPT = """\
你是一位严格的旅行规划评审专家。请评估以下杭州 3 天旅行计划的行程合理性。

请从以下三个子维度打分（整数），并给出简短理由：

**维度 1: 时空安排合理性 (0-10)**
- 8-10: 每天景点数量适中（2-3 个），景点间距离合理（同区域串联），无大量折返
- 5-7: 基本合理但部分安排欠优化
- 2-4: 景点过多或路线不合理
- 0-1: 完全不合理

**维度 2: 交通与时间信息 (0-10)**
- 8-10: 有具体交通方式（地铁/公交/打车）、景点开放时间、合理时间分配
- 5-7: 部分信息不够完整
- 2-4: 信息较少
- 0-1: 基本没有

**维度 3: 用餐与休息安排 (0-10)**
- 8-10: 每天有用餐建议（餐厅或菜品推荐）和适当休息安排
- 5-7: 有一些但不够全面
- 2-4: 很少
- 0-1: 完全没有

请严格按以下 JSON 格式回复（不要包含其他内容）：
```json
{{
  "routing_score": 0,
  "routing_reason": "",
  "transport_score": 0,
  "transport_reason": "",
  "dining_score": 0,
  "dining_reason": ""
}}
```

以下是待评估的旅行计划：

---
{plan}
---
"""


def _eval_logistics(plan: str, config: dict) -> Tuple[int, dict, List[str]]:
    details: Dict[str, Any] = {}
    deductions: List[str] = []

    prompt = _LOGISTICS_PROMPT.format(plan=plan[:8000])
    raw = _call_llm_judge(prompt, config)
    parsed = _parse_llm_json(raw)

    if parsed and all(k in parsed for k in ("routing_score", "transport_score", "dining_score")):
        rs = max(0, min(10, int(parsed["routing_score"])))
        ts = max(0, min(10, int(parsed["transport_score"])))
        ds = max(0, min(10, int(parsed["dining_score"])))
        details["3a 时空安排 (LLM)"] = f"{rs}/10 — {parsed.get('routing_reason', '')}"
        details["3b 交通时间 (LLM)"] = f"{ts}/10 — {parsed.get('transport_reason', '')}"
        details["3c 用餐休息 (LLM)"] = f"{ds}/10 — {parsed.get('dining_reason', '')}"
        details["评估方式"] = "LLM-as-Judge"
        total = rs + ts + ds
    else:
        details["评估方式"] = "关键词降级（LLM 不可用）"

        # 时空安排: 检查 3 天各自内容量
        day_blocks = [_extract_day_block(plan, d) for d in (1, 2, 3)]
        days_rich = sum(1 for b in day_blocks if len(b) > 100)
        rs = 7 if days_rich == 3 else (5 if days_rich >= 2 else 2)
        details["3a 时空安排 (KW)"] = f"{rs}/10 — {days_rich}/3 天有充实内容"

        # 交通与时间
        transport_kw = ["地铁", "公交", "打车", "步行", "骑行", "网约车",
                        "出租车", "车程", "交通", "到达"]
        time_kw = ["开放", "闭馆", "营业", "门票", "预约", "时间"]
        t_hits = sum(1 for k in transport_kw if k in plan)
        tm_hits = sum(1 for k in time_kw if k in plan)
        combined_t = t_hits + tm_hits
        ts = 7 if combined_t >= 8 else (5 if combined_t >= 4 else 2)
        details["3b 交通时间 (KW)"] = f"{ts}/10 — 命中 {combined_t} 词"

        # 用餐与休息
        dining_kw = ["午餐", "晚餐", "早餐", "用餐", "餐厅", "小吃", "美食",
                     "杭帮菜", "片儿川", "东坡肉", "龙井虾仁"]
        rest_kw = ["休息", "午休", "回酒店", "放松", "咖啡", "茶", "歇脚"]
        d_hits = sum(1 for k in dining_kw if k in plan)
        r_hits = sum(1 for k in rest_kw if k in plan)
        combined_d = d_hits + r_hits
        ds = 7 if combined_d >= 5 else (5 if combined_d >= 2 else 2)
        details["3c 用餐休息 (KW)"] = f"{ds}/10 — 命中 {combined_d} 词"

        total = rs + ts + ds

    if total < 15:
        deductions.append("行程合理性总体不足")

    return total, details, deductions


# ============================================================================
# 四、信息整合与附加值 (20 分) — LLM-as-Judge + 关键词降级
# ============================================================================

_ADDED_VALUE_PROMPT = """\
你是一位严格的旅行规划评审专家。请评估以下杭州 3 天旅行计划的信息整合质量与附加价值。

**背景**: agent 可参考的信息源有:
1. official_attractions.md — 杭州官方旅游局景点介绍（含开放时间、地址等）
2. travel_guides.md — 多篇旅游平台攻略（含路线建议、美食推荐；也含广告/导游推广）
3. evaluation_criteria.md — 信息可靠性评估标准（官方＞平台＞用户讨论）

请从以下两个子维度打分（整数），并给出简短理由：

**维度 1: 信息整合质量 (0-10)**
- 8-10: 有效整合多个信息源（官方开放时间 + 平台路线灵感），信息准确，有来源说明或冲突处理
- 5-7: 信息较完整但缺少来源说明或整合深度不够
- 2-4: 信息零散
- 0-1: 基本没有整合

**维度 2: 实用贴士与附加值 (0-10)**
- 8-10: 高质量贴士（天气、穿着、防蚊、人流、消费提醒等），有超越基本行程安排的额外价值
- 5-7: 有一些但数量或质量不够
- 2-4: 很少
- 0-1: 没有

请严格按以下 JSON 格式回复（不要包含其他内容）：
```json
{{
  "integration_score": 0,
  "integration_reason": "",
  "tips_score": 0,
  "tips_reason": ""
}}
```

以下是待评估的旅行计划：

---
{plan}
---
"""


def _eval_added_value(plan: str, config: dict) -> Tuple[int, dict, List[str]]:
    details: Dict[str, Any] = {}
    deductions: List[str] = []

    prompt = _ADDED_VALUE_PROMPT.format(plan=plan[:8000])
    raw = _call_llm_judge(prompt, config)
    parsed = _parse_llm_json(raw)

    if parsed and all(k in parsed for k in ("integration_score", "tips_score")):
        ig = max(0, min(10, int(parsed["integration_score"])))
        tp = max(0, min(10, int(parsed["tips_score"])))
        details["4a 信息整合 (LLM)"] = f"{ig}/10 — {parsed.get('integration_reason', '')}"
        details["4b 实用贴士 (LLM)"] = f"{tp}/10 — {parsed.get('tips_reason', '')}"
        details["评估方式"] = "LLM-as-Judge"
        total = ig + tp
    else:
        details["评估方式"] = "关键词降级（LLM 不可用）"

        # 信息整合
        src_kw = ["官方", "信息源", "来源", "参考", "可靠", "交叉验证",
                  "official", "评估", "采信", "冲突"]
        s_hits = sum(1 for k in src_kw if k in plan)
        ig = 7 if s_hits >= 3 else (4 if s_hits >= 1 else 2)
        details["4a 信息整合 (KW)"] = f"{ig}/10 — 命中 {s_hits} 词"

        # 实用贴士 — 统计贴士条数
        tip_lines = re.findall(r"^[-*•]\s+.{10,}", plan, re.MULTILINE)
        t_count = len(tip_lines)
        tp = 7 if t_count >= 8 else (5 if t_count >= 4 else (3 if t_count >= 1 else 1))
        details["4b 实用贴士 (KW)"] = f"{tp}/10 — 约 {t_count} 条贴士"

        total = ig + tp

    if total < 10:
        deductions.append("信息整合或贴士质量不足")

    return total, details, deductions


# ============================================================================
# 主入口
# ============================================================================

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    评估 agent 的旅行规划输出。

    Args:
        answer_dir: agent 输出目录绝对路径（如 .../gpt-5/attempt_1）

    Returns:
        (score, report)  score: 0-100 整数; report: 详细评估报告
    """
    plan_path = os.path.join(answer_dir, "travel_plan.md")

    # ---------- 文件不存在 ----------
    if not os.path.exists(plan_path) or os.path.getsize(plan_path) == 0:
        return 0, {
            "总分": 0,
            "结果评分": {
                "分数": 0,
                "详情": {"错误": "travel_plan.md 不存在或为空"},
                "扣分原因": ["缺少 travel_plan.md"],
            },
            "过程评分": {"分数": 0, "详情": {}, "扣分原因": []},
            "评语": "未提交有效的旅行规划文件",
        }

    plan = _read_file(plan_path)
    config = _get_text_eval_config(answer_dir)

    # 四个维度
    s1, d1, dd1 = _eval_format(plan)
    s2, d2, dd2 = _eval_preference(plan, config)
    s3, d3, dd3 = _eval_logistics(plan, config)
    s4, d4, dd4 = _eval_added_value(plan, config)

    total = s1 + s2 + s3 + s4

    if total >= 90:
        comment = "优秀！行程完整、合理，充分满足用户偏好和实用性。"
    elif total >= 75:
        comment = "良好。基本满足需求，有少量细节可改进。"
    elif total >= 60:
        comment = "及格。完成了基本规划，但偏好匹配或实用性方面存在不足。"
    elif total >= 40:
        comment = "部分完成。关键要素缺失或不够合理。"
    else:
        comment = "不及格。规划不完整或不符合要求。"

    report = {
        "总分": total,
        "结果评分": {
            "分数": s1,
            "详情": {"一、输出完整性与格式 (20分)": d1},
            "扣分原因": dd1,
        },
        "过程评分": {
            "分数": s2 + s3 + s4,
            "详情": {
                "二、需求符合度 (30分)": d2,
                "三、行程合理性 (30分)": d3,
                "四、信息整合与附加值 (20分)": d4,
            },
            "扣分原因": dd2 + dd3 + dd4,
        },
        "评语": comment,
        "分项得分": {
            "输出完整性与格式": f"{s1}/20",
            "需求符合度": f"{s2}/30",
            "行程合理性": f"{s3}/30",
            "信息整合与附加值": f"{s4}/20",
        },
    }

    return total, report


# ============================================================================
# 报告打印
# ============================================================================

def print_report(score: int, report: Dict[str, Any]) -> None:
    print("=" * 70)
    print("杭州旅行规划任务 — 评分报告")
    print("任务: 检索有效信息规划杭州 3 天旅行")
    print("=" * 70)
    print(f"\n总分: {score}/100\n")

    scores = report.get("分项得分", {})
    if scores:
        print("分项得分:")
        for k, v in scores.items():
            print(f"  {k}: {v}")

    for sec_key, sec_label in [
        ("结果评分", "结果评分（格式与完整性）"),
        ("过程评分", "过程评分（内容质量）"),
    ]:
        section = report.get(sec_key, {})
        print(f"\n{'─' * 50}")
        print(f"【{sec_label}】 {section.get('分数', 0)} 分")
        print(f"{'─' * 50}")
        for cat, items in section.get("详情", {}).items():
            print(f"\n  {cat}:")
            if isinstance(items, dict):
                for k, v in items.items():
                    print(f"    {k}: {v}")
            else:
                print(f"    {items}")
        deds = section.get("扣分原因", [])
        if deds:
            print(f"\n  扣分原因:")
            for i, r in enumerate(deds, 1):
                print(f"    {i}. {r}")

    print(f"\n{'=' * 50}")
    print(f"评语: {report.get('评语', '')}")
    print("=" * 70)


# ============================================================================
# CLI
# ============================================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        test_dir = sys.argv[1]
    else:
        test_dir = os.path.join(os.path.dirname(__file__), "..", "gpt-5", "attempt_1")

    if not os.path.isabs(test_dir):
        test_dir = os.path.join(os.path.dirname(__file__), "..", test_dir)

    if os.path.exists(test_dir):
        print(f"正在评估目录: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"目录不存在: {test_dir}")
    sys.exit(0)
