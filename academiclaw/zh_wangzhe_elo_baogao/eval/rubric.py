"""
wendiwu-query2 评分脚本
任务：撰写《王者荣耀ELO机制研究报告》

总分：100 分

评分维度
─────────────────────────────────────
一、文件交付 (10 分)
    answer.md 是否存在、非空、字符数达标
二、格式与结构 (15 分)
    Markdown 标题层级、四大模块标题、结构化元素
三、内容完整性 — LLM-as-Judge (45 分)
    机制猜测与验证 (12) / 典型现象分析 (12) / 娜可露露策略 (12) / 总结反思 (9)
四、内容质量 — LLM-as-Judge (30 分)
    深度与专业性 (15) / 逻辑与可落地性 (15)
"""

import os
import re
import json
import traceback
from typing import Tuple, Dict, Any, Optional

try:
    import openai
except ImportError:
    openai = None


# ─────────────────────────────────────────────────────────────────────────────
# 环境与 LLM 工具
# ─────────────────────────────────────────────────────────────────────────────

def _load_env(answer_dir: str) -> dict:
    """从 answer_dir 和 query 根目录加载 .env"""
    values: dict = {}
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
            max_tokens=2048,
            temperature=0,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        print(f"[RUBRIC] LLM Judge 调用失败: {e}")
        traceback.print_exc()
        return ""


def _extract_json(text: str) -> dict:
    """从 LLM 回复中提取 JSON 对象"""
    if not text:
        return {}
    try:
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        return json.loads(text)
    except (json.JSONDecodeError, IndexError):
        m = re.search(r"\{[\s\S]*\}", text)
        if m:
            try:
                return json.loads(m.group())
            except json.JSONDecodeError:
                pass
        print(f"[RUBRIC] JSON 解析失败: {text[:300]}")
        return {}


# ─────────────────────────────────────────────────────────────────────────────
# 辅助：定位 answer.md
# ─────────────────────────────────────────────────────────────────────────────

def _find_answer_md(answer_dir: str) -> Optional[str]:
    """在 answer_dir 及常见子目录中查找 answer.md"""
    for sub in ["", "workspace"]:
        if sub:
            p = os.path.join(answer_dir, sub, "answer.md")
        else:
            p = os.path.join(answer_dir, "answer.md")
        if os.path.isfile(p):
            return p
    return None


def _read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read().strip()


# ─────────────────────────────────────────────────────────────────────────────
# 一、文件交付 (10 分)
# ─────────────────────────────────────────────────────────────────────────────

def _eval_file_delivery(answer_dir: str) -> Tuple[int, dict]:
    details: dict = {}
    answer_path = _find_answer_md(answer_dir)

    if answer_path is None:
        details["answer.md"] = "未找到"
        return 0, details

    text = _read_text(answer_path)
    if not text:
        details["answer.md"] = "文件为空"
        return 0, details

    char_count = len(text)
    details["路径"] = os.path.relpath(answer_path, answer_dir)
    details["字符数"] = char_count

    score = 4  # 文件存在且非空
    details["基础交付"] = "4/4"

    if char_count >= 5000:
        score += 6
        details["长度"] = "6/6 (>= 5000 字符)"
    elif char_count >= 3000:
        score += 4
        details["长度"] = "4/6 (>= 3000 字符)"
    elif char_count >= 1500:
        score += 2
        details["长度"] = "2/6 (>= 1500 字符)"
    else:
        details["长度"] = f"0/6 (仅 {char_count} 字符，过短)"

    return score, details


# ─────────────────────────────────────────────────────────────────────────────
# 二、格式与结构 (15 分)
# ─────────────────────────────────────────────────────────────────────────────

_MODULE_KEYWORDS = [
    ["机制", "验证", "猜测", "猜想", "隐藏分", "胜率调控"],
    ["现象", "鸡爪", "牢玩家", "人机"],
    ["娜可露露", "策略", "发力", "出装"],
    ["总结", "反思", "影响"],
]


def _eval_format(text: str) -> Tuple[int, dict]:
    details: dict = {}
    score = 0

    # 标题统计
    h1 = len(re.findall(r"^#\s+.+", text, re.M))
    h2 = len(re.findall(r"^##\s+.+", text, re.M))
    h3 = len(re.findall(r"^###\s+.+", text, re.M))
    total_h = h1 + h2 + h3
    details["标题数"] = f"H1={h1} H2={h2} H3={h3} 总计={total_h}"

    if total_h >= 10 and h2 >= 4:
        score += 6
        details["标题结构"] = "6/6"
    elif total_h >= 6 and h2 >= 3:
        score += 4
        details["标题结构"] = "4/6"
    elif total_h >= 3:
        score += 2
        details["标题结构"] = "2/6"
    else:
        details["标题结构"] = "0/6"

    # 结构化元素
    bullets = len(re.findall(r"^\s*[-*+]\s+.+", text, re.M))
    numbered = len(re.findall(r"^\s*\d+[.)]\s+.+", text, re.M))
    tables = len(re.findall(r"^\|.+\|", text, re.M))
    struct_total = bullets + numbered + tables
    details["结构化元素"] = f"无序={bullets} 有序={numbered} 表格行={tables}"

    if struct_total >= 15:
        score += 5
        details["结构化评分"] = "5/5"
    elif struct_total >= 8:
        score += 3
        details["结构化评分"] = "3/5"
    elif struct_total >= 3:
        score += 1
        details["结构化评分"] = "1/5"
    else:
        details["结构化评分"] = "0/5"

    # 四大模块标题覆盖（4 分）
    headings_text = "\n".join(re.findall(r"^#{1,3}\s+.+", text, re.M))
    module_hits = 0
    for kws in _MODULE_KEYWORDS:
        if any(kw in headings_text for kw in kws):
            module_hits += 1
    if module_hits >= 4:
        score += 4
        details["模块标题覆盖"] = "4/4 (四大模块全有)"
    elif module_hits >= 3:
        score += 3
        details["模块标题覆盖"] = f"3/4 ({module_hits}/4)"
    elif module_hits >= 2:
        score += 2
        details["模块标题覆盖"] = f"2/4 ({module_hits}/4)"
    elif module_hits >= 1:
        score += 1
        details["模块标题覆盖"] = f"1/4 ({module_hits}/4)"
    else:
        details["模块标题覆盖"] = "0/4"

    return score, details


# ─────────────────────────────────────────────────────────────────────────────
# 三、内容完整性 — LLM-as-Judge (45 分)
# ─────────────────────────────────────────────────────────────────────────────

_COMPLETENESS_PROMPT = """\
你是一个严格的游戏研究报告评审专家。下面是一份《王者荣耀ELO机制研究报告》。

请严格评估该报告在以下四个必需模块上的覆盖程度，并给出整数评分和简短理由。

**模块 1：机制猜测与验证** (0-12 分)
- 12: 明确提出隐藏分/胜率调控等具体猜想，给出可执行的验证方案（数据采集方法、统计检验方式），描述预期结果
- 8-11: 有猜想和验证方案，但方案不够具体或缺少预期结果
- 4-7: 提到了 ELO 概念和猜想，但验证方案模糊或缺失
- 0-3: 几乎未涉及

**模块 2：典型现象关联分析** (0-12 分)  必须至少覆盖"鸡爪流""牢玩家""人机对局"三类
- 12: 三类现象均有详细分析，解释了形成原因、特征及与 ELO 机制的内在关联
- 8-11: 三类均涉及但部分不够深入
- 4-7: 仅覆盖 1-2 类或分析表面
- 0-3: 几乎未分析

**模块 3：万战娜可露露实战发力策略** (0-12 分)
- 12: 按不同 ELO 分段/对局环境给出了具体打法、出装、铭文、节奏、队伍协同与风险控制建议
- 8-11: 有分段策略但部分方面不够具体
- 4-7: 提到了策略但缺分段区分或具体建议
- 0-3: 几乎未涉及

**模块 4：机制影响总结反思** (0-9 分)
- 9: 辩证分析了 ELO 对高玩体验的正负面影响，给出认知纠偏与应对建议
- 6-8: 有反思但辩证性不足或建议笼统
- 3-5: 有简单总结但缺深度
- 0-2: 几乎无

请严格按以下 JSON 格式回复（不要包含其他内容）：
```json
{{
  "mechanism_verification": {{"score": 0, "reason": ""}},
  "phenomena_analysis": {{"score": 0, "reason": ""}},
  "nakelu_strategy": {{"score": 0, "reason": ""}},
  "reflection": {{"score": 0, "reason": ""}}
}}
```

报告全文：
---
{text}
---
"""


def _eval_completeness_llm(text: str, config: dict) -> Tuple[int, dict]:
    details: dict = {}
    eval_text = text[:12000] if len(text) > 12000 else text
    prompt = _COMPLETENESS_PROMPT.format(text=eval_text)
    raw = _call_llm_judge(prompt, config)
    result = _extract_json(raw)

    if result:
        mv = result.get("mechanism_verification", {})
        pa = result.get("phenomena_analysis", {})
        ns = result.get("nakelu_strategy", {})
        rf = result.get("reflection", {})

        mv_s = max(0, min(12, int(mv.get("score", 0))))
        pa_s = max(0, min(12, int(pa.get("score", 0))))
        ns_s = max(0, min(12, int(ns.get("score", 0))))
        rf_s = max(0, min(9, int(rf.get("score", 0))))
        total = mv_s + pa_s + ns_s + rf_s

        details["机制猜测与验证 (12)"] = f"{mv_s}/12 — {mv.get('reason', '')}"
        details["典型现象分析 (12)"] = f"{pa_s}/12 — {pa.get('reason', '')}"
        details["娜可露露策略 (12)"] = f"{ns_s}/12 — {ns.get('reason', '')}"
        details["总结反思 (9)"] = f"{rf_s}/9 — {rf.get('reason', '')}"
        details["评估模型"] = config.get("model", "unknown")
        return total, details

    # fallback
    print("[RUBRIC] LLM 不可用，使用关键词降级评分")
    return _fallback_completeness(text)


def _fallback_completeness(text: str) -> Tuple[int, dict]:
    """关键词降级评分，最高约 25/45"""
    t = text.lower()
    details: dict = {"注意": "LLM 不可用，关键词降级"}
    score = 0

    # 机制验证 (max 7)
    kw1 = ["验证", "隐藏分", "胜率调控", "mmr", "假设", "数据", "统计", "实验", "样本", "假说"]
    h1 = sum(1 for k in kw1 if k in t)
    s1 = min(7, h1 * 2) if h1 >= 2 else (1 if h1 else 0)
    score += s1
    details["机制猜测与验证 (12)"] = f"{s1}/12 (关键词 {h1})"

    # 现象分析 (max 7)
    p_jz = "鸡爪" in t
    p_lw = "牢玩家" in t or "牢号" in t
    p_rj = "人机" in t
    pc = sum([p_jz, p_lw, p_rj])
    s2 = min(7, pc * 3) if pc >= 1 else 0
    score += s2
    details["典型现象分析 (12)"] = f"{s2}/12 (覆盖 {pc}/3)"

    # 娜可露露 (max 7)
    kw3 = ["娜可露露", "出装", "铭文", "打野", "节奏", "发力", "抓人", "控龙", "强势期", "分段"]
    h3 = sum(1 for k in kw3 if k in t)
    s3 = min(7, h3 * 2) if h3 >= 2 else (1 if h3 else 0)
    score += s3
    details["娜可露露策略 (12)"] = f"{s3}/12 (关键词 {h3})"

    # 反思 (max 4)
    kw4 = ["反思", "总结", "影响", "辩证", "体验", "公平", "建议", "纠偏"]
    h4 = sum(1 for k in kw4 if k in t)
    s4 = min(4, h4) if h4 >= 1 else 0
    score += s4
    details["总结反思 (9)"] = f"{s4}/9 (关键词 {h4})"

    return score, details


# ─────────────────────────────────────────────────────────────────────────────
# 四、内容质量 — LLM-as-Judge (30 分)
# ─────────────────────────────────────────────────────────────────────────────

_QUALITY_PROMPT = """\
你是一个严格的研究报告质量评审专家。下面是一份《王者荣耀ELO机制研究报告》。
请从两个维度评估质量。

**维度 1：深度与专业性** (0-15 分)
- 13-15: 分析深入透彻，结合具体数据/案例/游戏机制细节，展示专业理解
- 9-12: 有一定深度但部分论述停留表面
- 5-8: 较浅，泛泛之谈，缺少具体机制解读
- 0-4: 空洞或明显错误

**维度 2：逻辑与可落地性** (0-15 分)
- 13-15: 论述逻辑严密，验证方案可执行，策略建议具体可操作
- 9-12: 逻辑基本清晰但部分建议缺操作性
- 5-8: 逻辑有跳跃，建议笼统
- 0-4: 逻辑混乱或建议不可操作

请严格按以下 JSON 格式回复（不要包含其他内容）：
```json
{{
  "depth": {{"score": 0, "reason": ""}},
  "logic": {{"score": 0, "reason": ""}},
  "overall_comment": ""
}}
```

报告全文：
---
{text}
---
"""


def _eval_quality_llm(text: str, config: dict) -> Tuple[int, dict]:
    details: dict = {}
    eval_text = text[:12000] if len(text) > 12000 else text
    prompt = _QUALITY_PROMPT.format(text=eval_text)
    raw = _call_llm_judge(prompt, config)
    result = _extract_json(raw)

    if result:
        dp = result.get("depth", {})
        lp = result.get("logic", {})
        dp_s = max(0, min(15, int(dp.get("score", 0))))
        lp_s = max(0, min(15, int(lp.get("score", 0))))
        total = dp_s + lp_s

        details["深度与专业性 (15)"] = f"{dp_s}/15 — {dp.get('reason', '')}"
        details["逻辑与可落地性 (15)"] = f"{lp_s}/15 — {lp.get('reason', '')}"
        details["总评"] = result.get("overall_comment", "")
        details["评估模型"] = config.get("model", "unknown")
        return total, details

    print("[RUBRIC] LLM 不可用，使用降级质量评分")
    return _fallback_quality(text)


def _fallback_quality(text: str) -> Tuple[int, dict]:
    """降级质量评分，最高约 15/30"""
    details: dict = {"注意": "LLM 不可用，降级评分"}
    clen = len(text)

    if clen >= 8000:
        d_score = 8
    elif clen >= 4000:
        d_score = 5
    elif clen >= 2000:
        d_score = 3
    else:
        d_score = 1

    action_kw = ["方案", "步骤", "建议", "策略", "具体", "例如", "比如", "案例"]
    hits = sum(1 for k in action_kw if k in text)
    if hits >= 5:
        l_score = 7
    elif hits >= 3:
        l_score = 5
    elif hits >= 1:
        l_score = 3
    else:
        l_score = 1

    details["深度与专业性 (15)"] = f"{d_score}/15 (基于长度)"
    details["逻辑与可落地性 (15)"] = f"{l_score}/15 (基于关键词)"
    return d_score + l_score, details


# ─────────────────────────────────────────────────────────────────────────────
# 主入口
# ─────────────────────────────────────────────────────────────────────────────

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    评估 agent 的输出。

    Args:
        answer_dir: agent 输出目录的绝对路径

    Returns:
        (score, report) — score: 0-100 整数, report: dict
    """
    report: Dict[str, Any] = {}

    # ── 一、文件交付 (10 分) ──
    s1, r1 = _eval_file_delivery(answer_dir)
    report["一、文件交付 (10分)"] = {"得分": s1, "详情": r1}

    if s1 == 0:
        for sec in ["二、格式与结构 (15分)", "三、内容完整性 (45分)", "四、内容质量 (30分)"]:
            report[sec] = {"得分": 0, "详情": {"原因": "answer.md 不存在或为空"}}
        report["总分"] = 0
        report["分项得分"] = {"文件交付": "0/10", "格式与结构": "0/15",
                             "内容完整性": "0/45", "内容质量": "0/30"}
        return 0, report

    # 读取全文
    answer_path = _find_answer_md(answer_dir)
    text = _read_text(answer_path)

    # ── 二、格式与结构 (15 分) ──
    s2, r2 = _eval_format(text)
    report["二、格式与结构 (15分)"] = {"得分": s2, "详情": r2}

    # ── LLM 配置 ──
    config = _get_text_eval_config(answer_dir)

    # ── 三、内容完整性 (45 分) ──
    s3, r3 = _eval_completeness_llm(text, config)
    report["三、内容完整性 (45分)"] = {"得分": s3, "详情": r3}

    # ── 四、内容质量 (30 分) ──
    s4, r4 = _eval_quality_llm(text, config)
    report["四、内容质量 (30分)"] = {"得分": s4, "详情": r4}

    total = max(0, min(100, s1 + s2 + s3 + s4))
    report["总分"] = total
    report["分项得分"] = {
        "文件交付": f"{s1}/10",
        "格式与结构": f"{s2}/15",
        "内容完整性": f"{s3}/45",
        "内容质量": f"{s4}/30",
    }

    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """打印格式化的评分报告"""
    print("=" * 70)
    print("wendiwu-query2 评分报告")
    print("任务：撰写《王者荣耀ELO机制研究报告》")
    print("=" * 70)
    print(f"\n总分：{score}/100\n")

    scores = report.get("分项得分", {})
    if scores:
        print("分项得分:")
        for k, v in scores.items():
            print(f"  {k}: {v}")

    for key in ["一、文件交付 (10分)", "二、格式与结构 (15分)",
                "三、内容完整性 (45分)", "四、内容质量 (30分)"]:
        section = report.get(key, {})
        if not section:
            continue
        print(f"\n{'─' * 50}")
        print(f"【{key}】 得分: {section.get('得分', 0)}")
        print(f"{'─' * 50}")
        for k, v in section.get("详情", {}).items():
            print(f"  {k}: {v}")

    print(f"\n{'=' * 70}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        test_dir = sys.argv[1]
    else:
        test_dir = os.path.join(os.path.dirname(__file__), "..", "gpt-5", "attempt_1")

    if not os.path.isabs(test_dir):
        test_dir = os.path.join(os.getcwd(), test_dir)

    if os.path.exists(test_dir):
        print(f"正在评估目录: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"目录不存在: {test_dir}")
    sys.exit(0)
