"""
pengyichen-query6 评分标准 (Rubric)
任务：基于个人叙事风格的文本续写与修改

文章是一篇关于 CS 游戏经历的个人叙事。上半部分（1-4节）已润色完毕作为风格参考，
下半部分（第5节起：低谷期、校队选拔、新生杯、年末复兴、收获、结语等）是待修改的原始草稿。
Agent 需模仿上半部分的写作风格，对下半部分进行优化改写，输出包含上下两部分的完整文章。

总分：100 分

评分维度：
一、文件交付 (10 分) — 程序化检查
  1. 输出文件存在且非空 (5 分)
  2. 文章结构合理（包含上下两部分） (5 分)

二、风格一致性 (30 分) — LLM-as-Judge
  上半部分风格示范与修改后下半部分的风格匹配程度

三、内容完整性 (25 分) — LLM-as-Judge
  修改后文本是否保留了原始草稿中的核心事实和关键细节

四、语言质量 (15 分) — LLM-as-Judge
  语言表达的流畅度、生动性和提升程度

五、情感表达 (20 分) — LLM-as-Judge
  情感表达的丰富度、自然度和与上半部分的一致性
"""

import os
import re
import json
from typing import Tuple, Dict, Any

try:
    import openai
except ImportError:
    openai = None

try:
    from docx import Document as DocxDocument
except ImportError:
    DocxDocument = None


# ============================================================================
# 环境与 LLM 配置
# ============================================================================

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
                        key = k.strip()
                        if key not in values:
                            values[key] = v.strip().strip("'\"")
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
        text = resp.choices[0].message.content
        if not text:
            msg = resp.choices[0].message
            text = getattr(msg, "reasoning_content", None) or ""
        return text.strip()
    except Exception as e:
        print("[RUBRIC] LLM Judge 调用失败: %s" % e)
        return ""


def _parse_json_from_llm(text: str) -> dict:
    """从 LLM 回复中提取 JSON"""
    if not text:
        return {}
    m = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            pass
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end > start:
        try:
            return json.loads(text[start:end + 1])
        except json.JSONDecodeError:
            pass
    return {}


# ============================================================================
# 文件 / 文本工具
# ============================================================================

def _read_text(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


def _read_docx(path: str) -> str:
    if DocxDocument is None:
        return ""
    try:
        doc = DocxDocument(path)
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    except Exception:
        return ""


def _locate_article_docx(answer_dir: str) -> str:
    """在 answer_dir/context 和 query根/context 中查找 article.docx"""
    for base in [answer_dir, os.path.join(os.path.dirname(__file__), "..")]:
        p = os.path.join(base, "context", "article.docx")
        if os.path.exists(p):
            return p
    return ""


def _split_upper_lower(full_text: str) -> Tuple[str, str]:
    """将完整文章拆为上半部分（已润色）和下半部分（原始草稿）。

    文章结构：1-4节是已润色的上半部分，从第5节开始是待修改的下半部分。
    """
    markers = [
        "5.短暂的低谷期",
        "5.赛事经历",
        "5. 短暂的低谷期",
        "5.",
    ]
    for marker in markers:
        idx = full_text.find(marker)
        if idx != -1:
            return full_text[:idx].strip(), full_text[idx:].strip()
    # 回退：按段落对半分
    lines = full_text.split("\n")
    mid = len(lines) // 2
    return "\n".join(lines[:mid]), "\n".join(lines[mid:])


def _find_output_file(answer_dir: str) -> str:
    """在 answer_dir 中查找 agent 输出的文章文件（.md 或 .txt）"""
    skip = {"query.md", "readme.md", "task_prompt.md", "evaluation_feedback.txt"}
    candidates = []
    for root, dirs, files in os.walk(answer_dir):
        dirs[:] = [d for d in dirs if d not in {"__pycache__", ".sii", "context", "node_modules"}]
        for f in files:
            lower = f.lower()
            if lower in skip:
                continue
            if lower.endswith(".md") or lower.endswith(".txt"):
                full = os.path.join(root, f)
                candidates.append(full)
    if not candidates:
        return ""
    candidates.sort(key=lambda p: os.path.getsize(p), reverse=True)
    return candidates[0]


# ============================================================================
# 一、文件交付 (10 分)
# ============================================================================

def _eval_file_delivery(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details = {}
    deductions = []

    output_path = _find_output_file(answer_dir)
    if not output_path:
        return 0, {
            "分数": 0,
            "详情": {"输出文件": "未找到 .md 或 .txt 文件"},
            "扣分原因": ["未找到输出文件"],
            "output_path": "",
        }

    content = _read_text(output_path).strip()
    char_count = len(content)

    # 1a. 文件存在且非空 (5 分)
    if char_count >= 500:
        score += 5
        details["文件存在"] = "5/5 — %s (%d 字符)" % (os.path.basename(output_path), char_count)
    elif char_count >= 100:
        score += 3
        details["文件存在"] = "3/5 — 文件偏短 (%d 字符)" % char_count
        deductions.append("输出文件偏短")
    elif char_count > 0:
        score += 1
        details["文件存在"] = "1/5 — 文件过短 (%d 字符)" % char_count
        deductions.append("输出文件过短")
    else:
        details["文件存在"] = "0/5 — 文件为空"
        deductions.append("输出文件为空")

    # 1b. 文章结构 (5 分) — 应包含上下两部分
    upper_kw = ["CS1.6", "半条命", "二姑", "网吧"]
    lower_kw = ["低谷", "S17", "校队", "新生杯", "复兴", "收获", "结语"]
    has_upper = any(kw in content for kw in upper_kw)
    has_lower = any(kw in content for kw in lower_kw)
    para_count = len([p for p in content.split("\n") if p.strip()])

    if has_upper and has_lower and para_count >= 15:
        struct_score = 5
        details["文章结构"] = "5/5 — 包含上下两部分，段落充足 (%d 段)" % para_count
    elif has_upper and has_lower:
        struct_score = 4
        details["文章结构"] = "4/5 — 包含上下部分，段落偏少 (%d 段)" % para_count
    elif has_upper or has_lower:
        struct_score = 2
        details["文章结构"] = "2/5 — 仅检测到部分内容"
        deductions.append("文章结构不完整")
    elif para_count >= 5:
        struct_score = 1
        details["文章结构"] = "1/5 — 有内容但缺少标志性关键词"
    else:
        struct_score = 0
        details["文章结构"] = "0/5 — 内容过少"
    score += struct_score

    return score, {
        "分数": score,
        "详情": details,
        "扣分原因": deductions,
        "output_path": output_path,
    }


# ============================================================================
# 二、风格一致性 (30 分) — LLM-as-Judge
# ============================================================================

def _eval_style(output_lower: str, upper_ref: str, config: dict) -> Tuple[int, dict]:
    """评估 agent 修改后下半部分与上半部分风格的匹配程度。"""
    if not upper_ref or not output_lower:
        return _style_fallback(output_lower)

    prompt = (
        "你是一位资深的中文文本风格分析专家。下面给出两段文本：\n"
        "- 【参考文本】是一篇个人叙事文章的上半部分（已经过风格润色）\n"
        "- 【待评估文本】是 Agent 对下半部分原始草稿的修改产出\n\n"
        "请评估【待评估文本】是否成功模仿了【参考文本】的写作风格。\n"
        "从以下 5 个子维度打分（每项 0-6 分，总分 30 分）：\n"
        "1. 词汇选择相似度 — 口语化/书面化比例、情感词汇的使用是否相似\n"
        "2. 句式结构匹配度 — 长短句比例、是否有类似的独立短句作为情感强调\n"
        "3. 叙事节奏一致性 — 时间推进方式、场景转换、段落长度\n"
        "4. 语气语调统一性 — 第一人称叙述的随意程度、幽默感、插入语\n"
        "5. 细节描写密度 — 具体描述与概括叙述的比例\n\n"
        "评分应严格。如果待评估文本明显与参考风格不同（如过于正式、缺乏个人色彩），"
        "相关项最多给 2 分。\n\n"
        "请严格按 JSON 格式返回：\n"
        '```json\n'
        '{\n'
        '  "词汇选择相似度": {"score": 0, "comment": ""},\n'
        '  "句式结构匹配度": {"score": 0, "comment": ""},\n'
        '  "叙事节奏一致性": {"score": 0, "comment": ""},\n'
        '  "语气语调统一性": {"score": 0, "comment": ""},\n'
        '  "细节描写密度": {"score": 0, "comment": ""},\n'
        '  "overall": ""\n'
        '}\n'
        '```\n\n'
        "【参考文本（上半部分，截取前 4000 字）】：\n%s\n\n"
        "【待评估文本（Agent 修改后的下半部分，截取前 5000 字）】：\n%s"
    ) % (upper_ref[:4000], output_lower[:5000])

    raw = _call_llm_judge(prompt, config)
    result = _parse_json_from_llm(raw)
    if not result:
        return _style_fallback(output_lower)

    dims = [
        ("词汇选择相似度", 6),
        ("句式结构匹配度", 6),
        ("叙事节奏一致性", 6),
        ("语气语调统一性", 6),
        ("细节描写密度", 6),
    ]
    score = 0
    details = {}
    for name, mx in dims:
        entry = result.get(name, {})
        if isinstance(entry, dict):
            s = min(max(int(entry.get("score", 0)), 0), mx)
            comment = entry.get("comment", "")
        else:
            s = 0
            comment = ""
        score += s
        details[name] = "%d/%d — %s" % (s, mx, comment)
    score = min(score, 30)
    details["总评"] = result.get("overall", "")
    return score, {"分数": score, "详情": details, "扣分原因": []}


def _style_fallback(text: str) -> Tuple[int, dict]:
    """LLM 不可用时的关键词回退评估"""
    if not text:
        return 0, {"分数": 0, "详情": {}, "扣分原因": ["无输出文本"]}
    score = 0
    details = {}

    # 口语化叙事标记
    narr = ["我", "当时", "记得", "后来", "终于", "其实", "不过", "于是", "结果", "可是", "然而"]
    found = sum(1 for m in narr if m in text)
    ns = min(found * 2, 12)
    score += ns
    details["叙事标记词"] = "%d/12 — 匹配 %d 个" % (ns, found)

    # 情感标记
    emo = ["激动", "难受", "开心", "期待", "失落", "热情", "坚持", "梦想"]
    ef = sum(1 for m in emo if m in text)
    es = min(ef * 2, 8)
    score += es
    details["情感标记词"] = "%d/8 — 匹配 %d 个" % (es, ef)

    # 专有名词
    proper = ["NFD", "CS", "nuke", "博子", "cook", "马嘉祺", "陈sir", "Thrash"]
    pf = sum(1 for m in proper if m in text)
    ps = min(pf, 6)
    score += ps
    details["专有名词"] = "%d/6 — 匹配 %d 个" % (ps, pf)

    base = 4 if len(text) >= 1000 else 2
    score += base
    details["基准分"] = "%d/4" % base
    score = min(score, 30)

    return score, {
        "分数": score,
        "详情": {"风格一致性(回退)": details},
        "扣分原因": ["LLM 不可用，使用关键词回退评估"],
    }


# ============================================================================
# 三、内容完整性 (25 分) — LLM-as-Judge
# ============================================================================

# 下半部分原始草稿中应保留的关键事件/信息（用于回退）
_KEY_EVENTS = [
    ("低谷期/队伍分裂", ["低谷", "分崩离析", "转瓦", "退出"]),
    ("S17赛季/单排到A+", ["S17", "A+", "单排"]),
    ("校队选拔", ["校队", "选拔"]),
    ("新生杯major/Navi Up", ["新生杯", "major", "Navi"]),
    ("八强淘汰赛/四杀", ["八强", "四杀"]),
    ("年末NFD复兴/11.25", ["复兴", "11.25"]),
    ("CS带来的精神收获", ["收获", "责任", "友谊", "信任"]),
    ("剪辑/自媒体/HLAE", ["剪辑", "自媒体", "HLAE"]),
    ("结语感悟", ["结语", "CS之路"]),
]


def _eval_content(output_lower: str, original_lower: str, config: dict) -> Tuple[int, dict]:
    """评估修改后文本是否保留了原始草稿的核心事实和关键细节。"""
    if not original_lower or not output_lower:
        return _content_fallback(output_lower)

    prompt = (
        "你是内容完整性评估专家。Agent 的任务是在保留原始草稿核心事实的前提下优化语言。\n\n"
        "请对照【原始草稿】和【修改后文本】，评估以下 5 个维度（每项 0-5 分，总分 25 分）：\n"
        "1. 核心事实保留度 — 主要事件（低谷期、校队选拔、新生杯比赛、年末复兴、个人收获）是否完整\n"
        "2. 关键细节完整性 — 重要数据（赛季编号S17、段位A+、人名、队名Navi Up）是否保留\n"
        "3. 逻辑关系保持度 — 因果和时间顺序是否清晰合理\n"
        "4. 主题一致性 — 核心情感基调（热爱CS、坚持、团队友谊、成长反省）是否一致\n"
        "5. 信息准确性 — 是否存在事实错误或扭曲（如把A+写成S、弄错比赛名称等）\n\n"
        "评分应严格。如果某个重要事件被删除或严重变形，对应项最多给 2 分。\n\n"
        "请严格按 JSON 格式返回：\n"
        '```json\n'
        '{\n'
        '  "核心事实保留度": {"score": 0, "comment": ""},\n'
        '  "关键细节完整性": {"score": 0, "comment": ""},\n'
        '  "逻辑关系保持度": {"score": 0, "comment": ""},\n'
        '  "主题一致性": {"score": 0, "comment": ""},\n'
        '  "信息准确性": {"score": 0, "comment": ""},\n'
        '  "overall": ""\n'
        '}\n'
        '```\n\n'
        "【原始草稿（下半部分，截取前 4000 字）】：\n%s\n\n"
        "【修改后文本（Agent 产出，截取前 5000 字）】：\n%s"
    ) % (original_lower[:4000], output_lower[:5000])

    raw = _call_llm_judge(prompt, config)
    result = _parse_json_from_llm(raw)
    if not result:
        return _content_fallback(output_lower)

    dims = [
        ("核心事实保留度", 5),
        ("关键细节完整性", 5),
        ("逻辑关系保持度", 5),
        ("主题一致性", 5),
        ("信息准确性", 5),
    ]
    score = 0
    details = {}
    for name, mx in dims:
        entry = result.get(name, {})
        if isinstance(entry, dict):
            s = min(max(int(entry.get("score", 0)), 0), mx)
            comment = entry.get("comment", "")
        else:
            s = 0
            comment = ""
        score += s
        details[name] = "%d/%d — %s" % (s, mx, comment)
    score = min(score, 25)
    details["总评"] = result.get("overall", "")
    return score, {"分数": score, "详情": details, "扣分原因": []}


def _content_fallback(text: str) -> Tuple[int, dict]:
    """LLM 不可用时基于关键词的回退"""
    if not text:
        return 0, {"分数": 0, "详情": {}, "扣分原因": ["无输出文本"]}
    matched = 0
    details = {}
    for label, keywords in _KEY_EVENTS:
        if any(kw in text for kw in keywords):
            matched += 1
            details[label] = "匹配"
        else:
            details[label] = "缺失"
    total = len(_KEY_EVENTS)
    score = int(matched / total * 25) if total else 0
    score = min(score, 25)
    return score, {
        "分数": score,
        "详情": {"内容完整性(回退)": details, "匹配率": "%d/%d" % (matched, total)},
        "扣分原因": ["LLM 不可用，使用关键词回退评估"],
    }


# ============================================================================
# 四、语言质量 (15 分) — LLM-as-Judge
# ============================================================================

def _eval_language(output_lower: str, config: dict) -> Tuple[int, dict]:
    """评估修改后文本的语言表达质量。"""
    if not output_lower:
        return 0, {"分数": 0, "详情": {}, "扣分原因": ["无输出文本"]}

    prompt = (
        "你是中文语言质量评估专家。请评估以下个人叙事文本的语言表达质量。\n\n"
        "从以下 3 个维度打分（每项 0-5 分，总分 15 分）：\n"
        "1. 语法与表达流畅度 — 是否有语病、句子衔接是否自然、有无生硬翻译腔\n"
        "2. 词汇丰富度与修辞 — 用词是否多样恰当、修辞手法（比喻、排比等）是否自然\n"
        "3. 可读性与节奏感 — 阅读体验是否顺畅、长短句搭配是否得当\n\n"
        "评分应严格。普通质量给 3 分，只有确实出色才给 4-5 分。\n\n"
        "请严格按 JSON 格式返回：\n"
        '```json\n'
        '{\n'
        '  "语法与表达流畅度": {"score": 0, "comment": ""},\n'
        '  "词汇丰富度与修辞": {"score": 0, "comment": ""},\n'
        '  "可读性与节奏感": {"score": 0, "comment": ""},\n'
        '  "overall": ""\n'
        '}\n'
        '```\n\n'
        "【待评估文本（截取前 5000 字）】：\n%s"
    ) % output_lower[:5000]

    raw = _call_llm_judge(prompt, config)
    result = _parse_json_from_llm(raw)
    if not result:
        return _language_fallback(output_lower)

    dims = [
        ("语法与表达流畅度", 5),
        ("词汇丰富度与修辞", 5),
        ("可读性与节奏感", 5),
    ]
    score = 0
    details = {}
    for name, mx in dims:
        entry = result.get(name, {})
        if isinstance(entry, dict):
            s = min(max(int(entry.get("score", 0)), 0), mx)
            comment = entry.get("comment", "")
        else:
            s = 0
            comment = ""
        score += s
        details[name] = "%d/%d — %s" % (s, mx, comment)
    score = min(score, 15)
    details["总评"] = result.get("overall", "")
    return score, {"分数": score, "详情": details, "扣分原因": []}


def _language_fallback(text: str) -> Tuple[int, dict]:
    """LLM 不可用时的回退"""
    if not text:
        return 0, {"分数": 0, "详情": {}, "扣分原因": ["无输出文本"]}
    score = 0
    details = {}

    # 标点多样性
    puncts = set()
    for ch in text:
        if ch in "，。！？；：、""''（）——……":
            puncts.add(ch)
    ps = min(len(puncts), 5)
    score += ps
    details["标点多样性"] = "%d/5 — %d 种" % (ps, len(puncts))

    # 修辞标记
    rhetorics = ["仿佛", "就像", "如同", "不仅", "而且", "虽然", "但是", "与其", "不如"]
    rf = sum(1 for r in rhetorics if r in text)
    rs = min(rf * 2, 5)
    score += rs
    details["修辞标记"] = "%d/5 — 匹配 %d 个" % (rs, rf)

    base = 3 if len(text) >= 1000 else 1
    score += base
    details["基准分"] = "%d/5" % base

    score = min(score, 15)
    return score, {
        "分数": score,
        "详情": {"语言质量(回退)": details},
        "扣分原因": ["LLM 不可用，使用回退评估"],
    }


# ============================================================================
# 五、情感表达 (20 分) — LLM-as-Judge
# ============================================================================

def _eval_emotion(output_lower: str, upper_ref: str, config: dict) -> Tuple[int, dict]:
    """评估修改后文本的情感表达质量。"""
    if not output_lower:
        return 0, {"分数": 0, "详情": {}, "扣分原因": ["无输出文本"]}

    ref_snippet = upper_ref[:3000] if upper_ref else "（参考文本不可用）"

    prompt = (
        "你是情感表达评估专家。以下是一篇关于 CS 游戏经历的个人叙事文章。\n"
        "【参考文本】展示了上半部分的情感表达风格，"
        "【待评估文本】是 Agent 修改后的下半部分。\n\n"
        "请评估【待评估文本】的情感表达质量，从以下 4 个维度打分（每项 0-5 分，总分 20 分）：\n"
        "1. 情感词汇恰当性 — 情感词汇的使用是否丰富且贴切\n"
        "2. 情感变化自然度 — 情感起伏是否合理（如失落→坚持→复兴→感恩）\n"
        "3. 情感与内容匹配度 — 情感表达是否贴合具体情境（低谷时的失落、比赛时的激动）\n"
        "4. 读者共鸣度 — 是否能引发读者共鸣，文字是否有感染力\n\n"
        "评分应严格。情感表达平淡给 2-3 分，只有真正有感染力才给 4-5 分。\n\n"
        "请严格按 JSON 格式返回：\n"
        '```json\n'
        '{\n'
        '  "情感词汇恰当性": {"score": 0, "comment": ""},\n'
        '  "情感变化自然度": {"score": 0, "comment": ""},\n'
        '  "情感与内容匹配度": {"score": 0, "comment": ""},\n'
        '  "读者共鸣度": {"score": 0, "comment": ""},\n'
        '  "overall": ""\n'
        '}\n'
        '```\n\n'
        "【情感参考（上半部分风格示范）】：\n%s\n\n"
        "【待评估文本（Agent 修改后的下半部分）】：\n%s"
    ) % (ref_snippet, output_lower[:5000])

    raw = _call_llm_judge(prompt, config)
    result = _parse_json_from_llm(raw)
    if not result:
        return _emotion_fallback(output_lower)

    dims = [
        ("情感词汇恰当性", 5),
        ("情感变化自然度", 5),
        ("情感与内容匹配度", 5),
        ("读者共鸣度", 5),
    ]
    score = 0
    details = {}
    for name, mx in dims:
        entry = result.get(name, {})
        if isinstance(entry, dict):
            s = min(max(int(entry.get("score", 0)), 0), mx)
            comment = entry.get("comment", "")
        else:
            s = 0
            comment = ""
        score += s
        details[name] = "%d/%d — %s" % (s, mx, comment)
    score = min(score, 20)
    details["总评"] = result.get("overall", "")
    return score, {"分数": score, "详情": details, "扣分原因": []}


def _emotion_fallback(text: str) -> Tuple[int, dict]:
    """LLM 不可用时的回退"""
    if not text:
        return 0, {"分数": 0, "详情": {}, "扣分原因": ["无输出文本"]}
    score = 0
    details = {}

    positive = ["激动", "开心", "快乐", "期待", "热情", "兴奋", "自豪", "欣慰"]
    negative = ["难受", "失落", "寒心", "失望", "遗憾", "无奈", "沮丧"]
    complex_ = ["百感交集", "矛盾", "纠结", "感慨", "释然", "顿悟"]

    pos_n = sum(1 for w in positive if w in text)
    neg_n = sum(1 for w in negative if w in text)
    cplx_n = sum(1 for w in complex_ if w in text)

    # 词汇丰富度 (0-5)
    total_emo = pos_n + neg_n + cplx_n
    vs = min(total_emo, 5)
    score += vs
    details["情感词汇"] = "%d/5 — 正%d+负%d+复合%d" % (vs, pos_n, neg_n, cplx_n)

    # 多样性 (0-5)
    diversity = 0
    if pos_n > 0:
        diversity += 2
    if neg_n > 0:
        diversity += 2
    if cplx_n > 0:
        diversity += 1
    diversity = min(diversity, 5)
    score += diversity
    details["情感多样性"] = "%d/5" % diversity

    # 感叹/强调 (0-5)
    excl = text.count("！") + text.count("……")
    exc_s = min(excl, 5)
    score += exc_s
    details["感叹/强调"] = "%d/5 — %d 处" % (exc_s, excl)

    base = 3 if len(text) >= 1000 else 1
    score += base
    details["基准分"] = "%d/5" % base

    score = min(score, 20)
    return score, {
        "分数": score,
        "详情": {"情感表达(回退)": details},
        "扣分原因": ["LLM 不可用，使用回退评估"],
    }


# ============================================================================
# 辅助：从完整输出中提取下半部分
# ============================================================================

def _extract_lower_from_output(output_content: str) -> str:
    """从 agent 输出的完整文章中提取下半部分（修改后的部分）。"""
    markers = [
        "5.短暂的低谷期",
        "5. 短暂的低谷期",
        "短暂的低谷期",
        "5.赛事经历",
        "5.",
    ]
    for marker in markers:
        idx = output_content.find(marker)
        if idx != -1:
            return output_content[idx:].strip()
    # 如果找不到明确的分界标记，使用整篇文章进行评估
    return output_content


# ============================================================================
# 主评估函数
# ============================================================================

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    评估 agent 的输出。

    Args:
        answer_dir: agent 输出目录的绝对路径

    Returns:
        (score, report) — score: 0-100 整数, report: 详细评估报告
    """

    # --- 1. 文件交付 (10 分) ---
    file_score, file_report = _eval_file_delivery(answer_dir)
    output_path = file_report.get("output_path", "")

    if not output_path:
        report = {
            "总分": 0,
            "文件交付": file_report,
            "风格一致性": {"分数": 0, "详情": {}, "扣分原因": ["未找到输出文件"]},
            "内容完整性": {"分数": 0, "详情": {}, "扣分原因": ["未找到输出文件"]},
            "语言质量": {"分数": 0, "详情": {}, "扣分原因": ["未找到输出文件"]},
            "情感表达": {"分数": 0, "详情": {}, "扣分原因": ["未找到输出文件"]},
            "评语": "未找到有效的输出文件，无法进行评估。",
        }
        return 0, report

    output_content = _read_text(output_path)

    # 从 agent 输出中提取下半部分（agent 修改的部分）
    output_lower = _extract_lower_from_output(output_content)

    # 获取参考文本（来自 article.docx）
    article_path = _locate_article_docx(answer_dir)
    upper_ref = ""
    original_lower = ""
    if article_path:
        full_text = _read_docx(article_path)
        if full_text:
            upper_ref, original_lower = _split_upper_lower(full_text)

    config = _get_text_eval_config(answer_dir)

    # --- 2. 风格一致性 (30 分) ---
    style_score, style_report = _eval_style(output_lower, upper_ref, config)

    # --- 3. 内容完整性 (25 分) ---
    content_score, content_report = _eval_content(output_lower, original_lower, config)

    # --- 4. 语言质量 (15 分) ---
    lang_score, lang_report = _eval_language(output_lower, config)

    # --- 5. 情感表达 (20 分) ---
    emo_score, emo_report = _eval_emotion(output_lower, upper_ref, config)

    total = file_score + style_score + content_score + lang_score + emo_score
    total = min(total, 100)

    if total >= 90:
        comment = "优秀！修改后的文本风格高度一致，内容完整，语言出色，情感丰富。"
    elif total >= 75:
        comment = "良好。整体修改质量不错，个别方面可进一步打磨。"
    elif total >= 60:
        comment = "及格。完成了基本修改，但风格模仿或内容保留有待提升。"
    elif total >= 40:
        comment = "部分完成。多个维度存在明显不足。"
    else:
        comment = "不及格。修改质量较差，未能有效模仿参考风格或保留核心内容。"

    report = {
        "总分": total,
        "文件交付": file_report,
        "风格一致性": style_report,
        "内容完整性": content_report,
        "语言质量": lang_report,
        "情感表达": emo_report,
        "评语": comment,
    }
    return total, report


# ============================================================================
# 报告打印
# ============================================================================

def print_report(score: int, report: Dict[str, Any]) -> None:
    """打印格式化的评分报告"""
    print("=" * 70)
    print("pengyichen-query6 评分报告")
    print("任务：基于个人叙事风格的文本续写与修改")
    print("=" * 70)
    print("\n总分：%d/100\n" % score)

    sections = [
        ("文件交付", "一、文件交付 (10 分)", 10),
        ("风格一致性", "二、风格一致性 (30 分)", 30),
        ("内容完整性", "三、内容完整性 (25 分)", 25),
        ("语言质量", "四、语言质量 (15 分)", 15),
        ("情感表达", "五、情感表达 (20 分)", 20),
    ]

    for key, title, mx in sections:
        sec = report.get(key, {})
        sec_score = sec.get("分数", 0)
        print("-" * 50)
        print("【%s】 %d/%d" % (title, int(sec_score), mx))
        print("-" * 50)
        for k, v in sec.get("详情", {}).items():
            if isinstance(v, dict):
                print("  %s:" % k)
                for kk, vv in v.items():
                    vv_str = str(vv)
                    if len(vv_str) > 120:
                        vv_str = vv_str[:120] + "..."
                    print("    %s: %s" % (kk, vv_str))
            else:
                v_str = str(v)
                if len(v_str) > 120:
                    v_str = v_str[:120] + "..."
                print("  %s: %s" % (k, v_str))
        deductions = sec.get("扣分原因", [])
        if deductions:
            print("  扣分原因:")
            for i, d in enumerate(deductions, 1):
                print("    %d. %s" % (i, d))
        print()

    print("=" * 50)
    print("评语：%s" % report.get("评语", ""))
    print("=" * 70)


# ============================================================================
# CLI 入口
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
        print("正在评估目录: %s\n" % test_dir)
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print("目录不存在: %s" % test_dir)
    sys.exit(0)
