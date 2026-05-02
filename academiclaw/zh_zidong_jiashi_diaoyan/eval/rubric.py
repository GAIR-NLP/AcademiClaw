"""
lushenhang_query2 评分标准 (Rubric)
任务：基于 5 篇学术文献撰写「自动驾驶产业发展路径及技术路线比较」调研报告

总分：100 分

评分维度：
一、文件交付 (10 分)
  1. Markdown 报告文件存在 (5 分)
  2. 文件非空且可读、长度合理 (5 分)

二、格式规范 (20 分)
  1. 标题 (3 分)
  2. 摘要 (4 分)
  3. 目录 (3 分)
  4. 正文分章节 (5 分)
  5. 参考文献 (5 分)

三、字数合规 (15 分)
  正文中文字数在 3000–5000 范围

四、内容完整性 — LLM-as-Judge (35 分)
  覆盖：产业发展路径(SAE分级/L2-L5演进)、技术路线比较(单车智能vs车路协同、
  模块化vs端到端)、未来挑战与展望、引用5篇文献

五、内容质量 — LLM-as-Judge (20 分)
  深度、准确性、逻辑性、学术规范
"""

import os
import re
import json
import traceback
from typing import Tuple, Dict, Any, List

try:
    import openai
except ImportError:
    openai = None


# =============================================================================
# 环境配置
# =============================================================================

def _load_env(answer_dir: str) -> dict:
    """从 answer_dir 和 query 根目录加载 .env 配置"""
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
    """获取文本评估 LLM 配置"""
    env = _load_env(answer_dir)

    def g(key, default=""):
        return os.environ.get(key) or env.get(key) or default

    return {
        "api_key": g("EVAL_TEXT_API_KEY", g("ANTHROPIC_API_KEY")),
        "api_base": g("EVAL_TEXT_API_BASE_URL", g("ANTHROPIC_BASE_URL")),
        "model": g("EVAL_TEXT_MODEL", "openai/gpt-5.2"),
    }


def _call_llm_judge(prompt: str, config: dict) -> str:
    """调用 LLM 进行文本评估"""
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


# =============================================================================
# 辅助函数
# =============================================================================

def _find_report_file(answer_dir: str) -> str:
    """查找 Markdown 报告文件，返回文件名或空字符串"""
    if not os.path.isdir(answer_dir):
        return ""
    files = os.listdir(answer_dir)
    # 优先精确匹配 report.md
    if "report.md" in files:
        return "report.md"
    # 查找其他 .md 文件（排除常见非报告文件）
    skip = {"readme.md", "changelog.md", "license.md", "query.md",
            "operation_list.md", "evaluation_feedback.txt"}
    md_files = [f for f in files
                if f.lower().endswith(".md") and f.lower() not in skip]
    if md_files:
        return md_files[0]
    return ""


def _count_chinese_chars(text: str) -> int:
    """统计中文字符数（CJK 统一汉字）"""
    return sum(1 for ch in text if '\u4e00' <= ch <= '\u9fff')


def _extract_body_text(content: str) -> str:
    """尝试提取正文（去掉摘要和参考文献部分），用于字数统计"""
    lines = content.split("\n")
    body_lines = []
    in_abstract = False
    in_references = False
    past_toc = False

    for line in lines:
        stripped = line.strip().lower()
        # 检测摘要
        if re.match(r'^#{1,3}\s*(摘要|abstract)', stripped):
            in_abstract = True
            continue
        # 检测目录
        if re.match(r'^#{1,3}\s*(目录|table of contents|toc)', stripped):
            in_abstract = False  # 结束摘要
            past_toc = True
            continue
        # 检测参考文献
        if re.match(r'^#{1,3}\s*(参考文献|references|bibliography)', stripped):
            in_references = True
            continue
        # 检测正文开始（第一个非摘要非目录的标题）
        if not past_toc and re.match(r'^#{1,3}\s*\d', stripped):
            past_toc = True
            in_abstract = False

        if in_abstract:
            continue
        if in_references:
            continue
        if not past_toc:
            continue
        # 跳过目录行（以 - 开头加数字/链接的行）
        if re.match(r'^\s*-\s*\[?\d', line):
            continue

        body_lines.append(line)

    return "\n".join(body_lines)


# =============================================================================
# 一、文件交付 (10 分)
# =============================================================================

def _eval_file_delivery(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    score = 0
    details = {}

    report_name = _find_report_file(answer_dir)
    if not report_name:
        details["报告文件"] = "0/5 - 未找到 Markdown 报告文件"
        details["文件可读性"] = "0/5 - 无文件"
        return 0, details

    # 5 分：文件存在
    if report_name == "report.md":
        score += 5
        details["报告文件"] = "5/5 - report.md 存在"
    else:
        score += 3
        details["报告文件"] = f"3/5 - 找到 {report_name}（非标准文件名 report.md）"

    # 5 分：文件非空、长度合理
    filepath = os.path.join(answer_dir, report_name)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        char_count = len(content)
        if char_count >= 2000:
            score += 5
            details["文件可读性"] = f"5/5 - 文件可读，长度 {char_count} 字符"
        elif char_count >= 500:
            score += 3
            details["文件可读性"] = f"3/5 - 文件偏短，{char_count} 字符"
        elif char_count > 0:
            score += 1
            details["文件可读性"] = f"1/5 - 文件过短，{char_count} 字符"
        else:
            details["文件可读性"] = "0/5 - 文件为空"
    except Exception as e:
        details["文件可读性"] = f"0/5 - 读取失败: {e}"

    return score, details


# =============================================================================
# 二、格式规范 (20 分)
# =============================================================================

def _eval_format(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    score = 0
    details = {}

    report_name = _find_report_file(answer_dir)
    if not report_name:
        return 0, {"错误": "0/20 - 无报告文件"}

    filepath = os.path.join(answer_dir, report_name)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return 0, {"错误": "0/20 - 文件读取失败"}

    lines_lower = content.lower()

    # 2a. 标题 (3 分) — 第一行以 # 开头，包含"自动驾驶"相关关键词
    has_title = False
    for line in content.split("\n")[:10]:
        if line.strip().startswith("#") and ("自动驾驶" in line or "autonomous" in line.lower()):
            has_title = True
            break
        if line.strip().startswith("#") and len(line.strip()) > 5:
            has_title = True
            break

    if has_title:
        score += 3
        details["标题"] = "3/3 - 存在"
    else:
        details["标题"] = "0/3 - 缺失或不明确"

    # 2b. 摘要 (4 分)
    has_abstract = bool(re.search(r'#{1,3}\s*(摘要|abstract)', lines_lower))
    if has_abstract:
        # 检查摘要内容长度
        abstract_match = re.search(
            r'#{1,3}\s*(?:摘要|abstract)\s*\n([\s\S]*?)(?=\n#{1,3}\s|\Z)',
            content, re.IGNORECASE
        )
        abstract_len = 0
        if abstract_match:
            abstract_len = _count_chinese_chars(abstract_match.group(1))
        if abstract_len >= 100:
            score += 4
            details["摘要"] = f"4/4 - 存在，约 {abstract_len} 字"
        elif abstract_len >= 30:
            score += 3
            details["摘要"] = f"3/4 - 存在但偏短（{abstract_len} 字）"
        else:
            score += 2
            details["摘要"] = f"2/4 - 存在但内容过少（{abstract_len} 字）"
    else:
        details["摘要"] = "0/4 - 缺失摘要章节"

    # 2c. 目录 (3 分)
    has_toc = bool(re.search(r'#{1,3}\s*(目录|table of contents|toc)', lines_lower))
    # 或者有多个超链接列表模式（也算目录）
    if not has_toc:
        toc_links = re.findall(r'^\s*-\s*\[.+\]\(#', content, re.MULTILINE)
        if len(toc_links) >= 3:
            has_toc = True
    # 或者有编号列表紧邻在一起（目录模式）
    if not has_toc:
        toc_lines = re.findall(r'^\s*-\s*\d+[\.\s]', content, re.MULTILINE)
        if len(toc_lines) >= 3:
            has_toc = True

    if has_toc:
        score += 3
        details["目录"] = "3/3 - 存在"
    else:
        details["目录"] = "0/3 - 缺失目录"

    # 2d. 正文分章节 (5 分)
    # 统计 ## 或 ### 级别的标题数量
    section_headings = re.findall(r'^#{2,3}\s+.+', content, re.MULTILINE)
    num_sections = len(section_headings)
    if num_sections >= 5:
        score += 5
        details["正文分章节"] = f"5/5 - {num_sections} 个章节标题"
    elif num_sections >= 3:
        score += 3
        details["正文分章节"] = f"3/5 - {num_sections} 个章节标题（偏少）"
    elif num_sections >= 1:
        score += 1
        details["正文分章节"] = f"1/5 - 仅 {num_sections} 个章节标题"
    else:
        details["正文分章节"] = "0/5 - 未分章节"

    # 2e. 参考文献 (5 分)
    has_ref_section = bool(re.search(
        r'#{1,3}\s*(参考文献|references|bibliography)', lines_lower
    ))
    if has_ref_section:
        # 统计参考文献条目数
        ref_match = re.search(
            r'#{1,3}\s*(?:参考文献|references|bibliography)\s*\n([\s\S]*)',
            content, re.IGNORECASE
        )
        ref_count = 0
        if ref_match:
            ref_text = ref_match.group(1)
            # 统计列表项或编号条目
            ref_count = len(re.findall(
                r'(?:^\s*[-\*]\s+\[?\d*\]?|^\s*\d+[\.\)]\s+|\[\d+\])',
                ref_text, re.MULTILINE
            ))
        if ref_count >= 5:
            score += 5
            details["参考文献"] = f"5/5 - 参考文献章节存在，{ref_count} 条引用"
        elif ref_count >= 3:
            score += 4
            details["参考文献"] = f"4/5 - 参考文献章节存在，但仅 {ref_count} 条（要求引用 5 篇）"
        elif ref_count >= 1:
            score += 3
            details["参考文献"] = f"3/5 - 参考文献章节存在，仅 {ref_count} 条引用"
        else:
            score += 2
            details["参考文献"] = "2/5 - 有参考文献标题但无明确条目"
    else:
        # 检查正文是否有引用标记
        inline_refs = re.findall(r'\[\d+\]', content)
        if len(inline_refs) >= 3:
            score += 1
            details["参考文献"] = "1/5 - 正文有引用标记但缺少参考文献章节"
        else:
            details["参考文献"] = "0/5 - 缺失参考文献"

    return score, details


# =============================================================================
# 三、字数合规 (15 分)
# =============================================================================

def _eval_word_count(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    score = 0
    details = {}

    report_name = _find_report_file(answer_dir)
    if not report_name:
        return 0, {"错误": "0/15 - 无报告文件"}

    filepath = os.path.join(answer_dir, report_name)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return 0, {"错误": "0/15 - 文件读取失败"}

    body = _extract_body_text(content)
    cn_chars = _count_chinese_chars(body)

    # 全文中文字数（作为兜底参考）
    total_cn = _count_chinese_chars(content)

    details["正文中文字数"] = cn_chars
    details["全文中文字数"] = total_cn

    if 3000 <= cn_chars <= 5000:
        score = 15
        details["判定"] = f"15/15 - 正文 {cn_chars} 字，在 3000-5000 范围内"
    elif 2500 <= cn_chars < 3000:
        score = 10
        details["判定"] = f"10/15 - 正文 {cn_chars} 字，略低于 3000 下限"
    elif 5000 < cn_chars <= 6000:
        score = 10
        details["判定"] = f"10/15 - 正文 {cn_chars} 字，略超 5000 上限"
    elif 2000 <= cn_chars < 2500:
        score = 7
        details["判定"] = f"7/15 - 正文 {cn_chars} 字，明显不足"
    elif 6000 < cn_chars <= 8000:
        score = 7
        details["判定"] = f"7/15 - 正文 {cn_chars} 字，明显超出"
    elif 1000 <= cn_chars < 2000:
        score = 4
        details["判定"] = f"4/15 - 正文 {cn_chars} 字，严重不足"
    elif cn_chars > 8000:
        score = 4
        details["判定"] = f"4/15 - 正文 {cn_chars} 字，严重超出"
    else:
        # 正文提取可能不准确，用全文字数兜底
        if 3000 <= total_cn <= 7000:
            score = 8
            details["判定"] = (
                f"8/15 - 正文提取仅 {cn_chars} 字，但全文 {total_cn} 字；"
                "提取可能不准确，给予中间分"
            )
        elif total_cn >= 2000:
            score = 4
            details["判定"] = (
                f"4/15 - 正文 {cn_chars} 字，全文 {total_cn} 字，字数不足"
            )
        else:
            score = 0
            details["判定"] = f"0/15 - 正文仅 {cn_chars} 字，全文 {total_cn} 字"

    return score, details


# =============================================================================
# 四、内容完整性 — LLM-as-Judge (35 分)
# =============================================================================

_COMPLETENESS_PROMPT_TEMPLATE = """\
你是一个严格的学术报告评审专家。请评估以下调研报告在「内容完整性」维度的表现。

**任务要求**：基于 5 篇学术文献，撰写一篇关于「自动驾驶产业发展路径及技术路线比较」的调研报告。

**内容完整性的评分标准**（总分 35 分）：

1. **产业发展路径分析** (0-10 分)
   - 10: 充分讨论了 SAE L0-L5 分级、从 L2 到 L3/L4/L5 的产业演进路径，有具体事例或论据
   - 7-9: 讨论了分级与演进但不够深入或缺少部分层级
   - 4-6: 仅简单提及分级，缺乏分析
   - 0-3: 几乎未涉及产业发展路径

2. **技术路线比较** (0-15 分)
   - 13-15: 全面比较了至少 2 个维度（如：单车智能 vs 车路协同/V2X；模块化 vs 端到端/大模型），论述有深度，有技术细节
   - 9-12: 比较了多个维度但深度一般
   - 5-8: 仅浅层罗列技术路线，缺乏实质性比较
   - 0-4: 技术路线比较严重不足

3. **未来挑战与展望** (0-5 分)
   - 5: 有独立章节讨论挑战、趋势或建议，内容具体
   - 3-4: 有提及但不够深入
   - 0-2: 缺失或仅一句带过

4. **文献引用完整性** (0-5 分)
   - 5: 正文中引用了全部 5 篇文献，引用自然融入论述
   - 3-4: 引用了 3-4 篇文献
   - 1-2: 引用了 1-2 篇文献
   - 0: 未引用任何文献

请严格按以下 JSON 格式回复（不要包含任何其他内容）：
```json
{{
  "industry_path": {{"score": 0, "reason": ""}},
  "tech_comparison": {{"score": 0, "reason": ""}},
  "future_challenges": {{"score": 0, "reason": ""}},
  "citation_completeness": {{"score": 0, "reason": ""}},
  "total": 0
}}
```

以下是待评估的报告内容：

---
{report_content}
---
"""


def _eval_completeness(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    score = 0
    details = {}

    report_name = _find_report_file(answer_dir)
    if not report_name:
        return 0, {"错误": "0/35 - 无报告文件"}

    filepath = os.path.join(answer_dir, report_name)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return 0, {"错误": "0/35 - 文件读取失败"}

    # 截取前 12000 字符送入 LLM（避免超 token）
    truncated = content[:12000]
    if len(content) > 12000:
        truncated += "\n\n[... 内容已截断 ...]"

    config = _get_text_eval_config(answer_dir)
    prompt = _COMPLETENESS_PROMPT_TEMPLATE.format(report_content=truncated)
    raw = _call_llm_judge(prompt, config)

    if raw:
        try:
            # 提取 JSON
            if "```json" in raw:
                raw_json = raw.split("```json")[1].split("```")[0].strip()
            elif "```" in raw:
                raw_json = raw.split("```")[1].split("```")[0].strip()
            else:
                raw_json = raw
            result = json.loads(raw_json)

            ip = max(0, min(10, int(result.get("industry_path", {}).get("score", 0))))
            tc = max(0, min(15, int(result.get("tech_comparison", {}).get("score", 0))))
            fc = max(0, min(5, int(result.get("future_challenges", {}).get("score", 0))))
            cc = max(0, min(5, int(result.get("citation_completeness", {}).get("score", 0))))
            score = ip + tc + fc + cc

            details["产业发展路径 (10分)"] = f"{ip}/10 - {result.get('industry_path', {}).get('reason', '')}"
            details["技术路线比较 (15分)"] = f"{tc}/15 - {result.get('tech_comparison', {}).get('reason', '')}"
            details["未来挑战与展望 (5分)"] = f"{fc}/5 - {result.get('future_challenges', {}).get('reason', '')}"
            details["文献引用完整性 (5分)"] = f"{cc}/5 - {result.get('citation_completeness', {}).get('reason', '')}"
            details["评估模型"] = config.get("model", "unknown")

        except (json.JSONDecodeError, ValueError) as e:
            print(f"[RUBRIC] LLM 返回解析失败: {e}")
            details["LLM 解析错误"] = str(raw[:500])
            score = _fallback_completeness(content)
            details["降级评估"] = f"{score}/35 - LLM 返回格式错误，使用降级评估"
    else:
        # LLM 不可用，降级评估
        score = _fallback_completeness(content)
        details["降级评估"] = f"{score}/35 - LLM 不可用，基于关键词匹配"

    return score, details


def _fallback_completeness(content: str) -> int:
    """LLM 不可用时的降级内容完整性评估（基于关键词匹配，最高 20/35）"""
    score = 0
    lower = content.lower()

    # 产业发展路径关键词
    path_keywords = ["sae", "l2", "l3", "l4", "l5", "分级", "演进", "产业化",
                     "辅助驾驶", "量产", "robotaxi"]
    path_hits = sum(1 for kw in path_keywords if kw in lower)
    score += min(6, path_hits)

    # 技术路线比较关键词
    tech_keywords = ["单车智能", "车路协同", "v2x", "模块化", "端到端",
                     "end-to-end", "bev", "大模型", "感知", "规划",
                     "多任务", "vad", "transformer"]
    tech_hits = sum(1 for kw in tech_keywords if kw in lower)
    score += min(8, tech_hits)

    # 未来挑战
    future_keywords = ["挑战", "展望", "趋势", "未来", "建议", "瓶颈"]
    future_hits = sum(1 for kw in future_keywords if kw in lower)
    score += min(3, future_hits)

    # 文献引用
    ref_markers = re.findall(r'\[\d+\]', content)
    unique_refs = len(set(ref_markers))
    score += min(3, unique_refs)

    return min(20, score)


# =============================================================================
# 五、内容质量 — LLM-as-Judge (20 分)
# =============================================================================

_QUALITY_PROMPT_TEMPLATE = """\
你是一个严格的学术报告评审专家。请评估以下调研报告在「内容质量」维度的表现。

**任务背景**：这是一篇关于「自动驾驶产业发展路径及技术路线比较」的调研报告，\
要求基于 5 篇学术文献撰写。

**内容质量的评分标准**（总分 20 分）：

1. **论述深度** (0-7 分)
   - 7: 对技术原理和产业逻辑有深入分析，不是浅层堆砌
   - 4-6: 有一定深度但部分论述流于表面
   - 0-3: 内容浅薄，多为空洞的概括性描述

2. **逻辑性与连贯性** (0-6 分)
   - 6: 章节间衔接自然，论述有清晰的逻辑链条
   - 3-5: 基本有逻辑但部分过渡生硬
   - 0-2: 章节割裂、缺乏逻辑主线

3. **学术规范与准确性** (0-7 分)
   - 7: 用语专业准确，无明显事实错误，引用规范（无博客/非学术来源）
   - 4-6: 基本准确但有个别不规范
   - 0-3: 存在明显事实错误或大量非学术用语/来源

请严格按以下 JSON 格式回复（不要包含任何其他内容）：
```json
{{
  "depth": {{"score": 0, "reason": ""}},
  "coherence": {{"score": 0, "reason": ""}},
  "academic_quality": {{"score": 0, "reason": ""}},
  "total": 0
}}
```

以下是待评估的报告内容：

---
{report_content}
---
"""


def _eval_quality(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    score = 0
    details = {}

    report_name = _find_report_file(answer_dir)
    if not report_name:
        return 0, {"错误": "0/20 - 无报告文件"}

    filepath = os.path.join(answer_dir, report_name)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return 0, {"错误": "0/20 - 文件读取失败"}

    truncated = content[:12000]
    if len(content) > 12000:
        truncated += "\n\n[... 内容已截断 ...]"

    config = _get_text_eval_config(answer_dir)
    prompt = _QUALITY_PROMPT_TEMPLATE.format(report_content=truncated)
    raw = _call_llm_judge(prompt, config)

    if raw:
        try:
            if "```json" in raw:
                raw_json = raw.split("```json")[1].split("```")[0].strip()
            elif "```" in raw:
                raw_json = raw.split("```")[1].split("```")[0].strip()
            else:
                raw_json = raw
            result = json.loads(raw_json)

            dp = max(0, min(7, int(result.get("depth", {}).get("score", 0))))
            co = max(0, min(6, int(result.get("coherence", {}).get("score", 0))))
            aq = max(0, min(7, int(result.get("academic_quality", {}).get("score", 0))))
            score = dp + co + aq

            details["论述深度 (7分)"] = f"{dp}/7 - {result.get('depth', {}).get('reason', '')}"
            details["逻辑性与连贯性 (6分)"] = f"{co}/6 - {result.get('coherence', {}).get('reason', '')}"
            details["学术规范与准确性 (7分)"] = f"{aq}/7 - {result.get('academic_quality', {}).get('reason', '')}"
            details["评估模型"] = config.get("model", "unknown")

        except (json.JSONDecodeError, ValueError) as e:
            print(f"[RUBRIC] LLM 返回解析失败: {e}")
            details["LLM 解析错误"] = str(raw[:500])
            score = _fallback_quality(content)
            details["降级评估"] = f"{score}/20 - LLM 返回格式错误，使用降级评估"
    else:
        score = _fallback_quality(content)
        details["降级评估"] = f"{score}/20 - LLM 不可用，基于启发式评估"

    return score, details


def _fallback_quality(content: str) -> int:
    """LLM 不可用时的降级质量评估（最高 12/20）"""
    score = 0
    cn_chars = _count_chinese_chars(content)

    # 基于内容长度和结构复杂度粗略估分
    if cn_chars >= 3000:
        score += 4
    elif cn_chars >= 1500:
        score += 2

    # 章节数
    sections = len(re.findall(r'^#{2,3}\s+.+', content, re.MULTILINE))
    if sections >= 5:
        score += 4
    elif sections >= 3:
        score += 2

    # 引用标记密度
    refs = len(re.findall(r'\[\d+\]', content))
    if refs >= 10:
        score += 4
    elif refs >= 5:
        score += 2

    return min(12, score)


# =============================================================================
# 入口
# =============================================================================

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """评估 agent 的输出。"""
    s1, r1 = _eval_file_delivery(answer_dir)
    s2, r2 = _eval_format(answer_dir)
    s3, r3 = _eval_word_count(answer_dir)
    s4, r4 = _eval_completeness(answer_dir)
    s5, r5 = _eval_quality(answer_dir)

    total = s1 + s2 + s3 + s4 + s5

    report = {
        "总分": total,
        "分项得分": {
            "一、文件交付": f"{s1}/10",
            "二、格式规范": f"{s2}/20",
            "三、字数合规": f"{s3}/15",
            "四、内容完整性": f"{s4}/35",
            "五、内容质量": f"{s5}/20",
        },
        "详情": {
            "一、文件交付 (10分)": r1,
            "二、格式规范 (20分)": r2,
            "三、字数合规 (15分)": r3,
            "四、内容完整性 (35分)": r4,
            "五、内容质量 (20分)": r5,
        },
        "评语": "",
    }

    if total >= 90:
        report["评语"] = "优秀：结构完整、字数与论述符合要求，产业发展路径与技术路线均有充分论述。"
    elif total >= 75:
        report["评语"] = "良好：基本完成任务要求，部分维度有改进空间。"
    elif total >= 60:
        report["评语"] = "及格：核心内容有涵盖但存在明显不足（字数/格式/深度等）。"
    elif total >= 40:
        report["评语"] = "部分完成：关键内容或格式缺失较多。"
    else:
        report["评语"] = "不及格：任务完成度严重不足。"

    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """打印格式化的评分报告"""
    print("=" * 70)
    print("lushenhang_query2 评分报告")
    print("任务：自动驾驶产业发展路径及技术路线比较调研报告")
    print("=" * 70)
    print(f"\n总分：{score}/100\n")

    scores = report.get("分项得分", {})
    if scores:
        print("分项得分:")
        for k, v in scores.items():
            print(f"  {k}: {v}")

    for section_name, section_data in report.get("详情", {}).items():
        print(f"\n{'─' * 60}")
        print(f"【{section_name}】")
        print(f"{'─' * 60}")
        if isinstance(section_data, dict):
            for k, v in section_data.items():
                if isinstance(v, dict):
                    print(f"  {k}:")
                    for kk, vv in v.items():
                        print(f"    {kk}: {vv}")
                else:
                    print(f"  {k}: {v}")
        else:
            print(f"  {section_data}")

    print(f"\n{'=' * 70}")
    print(f"评语：{report.get('评语', '')}")
    print("=" * 70)


if __name__ == "__main__":
    import sys
    test_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(__file__), "..", "gpt-5", "attempt_1")
    if os.path.exists(test_dir):
        print(f"正在评估目录: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"目录不存在: {test_dir}")
    sys.exit(0)
