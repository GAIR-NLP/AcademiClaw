"""
评分脚本 — 根据学术文章生成通俗演讲稿（量子计算基础原理 面向高中生）

总分 100 分，评分维度:
  一、文件交付 (10 分)            — 确定性检查
  二、专业术语转化率 (25 分)      — 确定性预检 + LLM-as-Judge
  三、受众适应性 (25 分)          — 确定性预检 + LLM-as-Judge
  四、教育效果与结构 (25 分)      — 结构化检测 + LLM-as-Judge
  五、创造性与比喻质量 (15 分)    — LLM-as-Judge

交付物:
  1. speech_transcript.md  — 完整演讲稿
  2. qa_preparation.md     — 预计问题及回答准备
"""

import os
import re
import json
from typing import Tuple, Dict, Any, List

try:
    import openai
except ImportError:
    openai = None


# ============================================================
# 工具函数
# ============================================================

def _load_env(answer_dir: str) -> dict:
    """从 answer_dir 和 query 根目录加载 .env 配置"""
    values: Dict[str, str] = {}
    query_root = os.path.join(os.path.dirname(__file__), "..")
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
                        key = k.strip()
                        val = v.strip().strip("'\"")
                        if key not in values:
                            values[key] = val
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
    """调用 LLM 进行评估，返回原始文本响应"""
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


def _extract_json(text: str) -> dict:
    """从 LLM 回复中提取 JSON"""
    if not text:
        return {}
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    m = re.search(r"```(?:json)?\s*\n?(.*?)```", text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1).strip())
        except json.JSONDecodeError:
            pass
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(0))
        except json.JSONDecodeError:
            pass
    return {}


def _read_file(path: str, max_bytes: int = 0) -> str:
    if not os.path.isfile(path):
        return ""
    try:
        with open(path, "r", encoding="utf-8") as f:
            if max_bytes > 0:
                return f.read(max_bytes)
            return f.read()
    except Exception:
        return ""


def _find_deliverable(directory: str, primary_name: str, fallback_keywords: List[str]) -> str:
    """在目录中查找交付文件：先精确匹配，再模糊匹配"""
    if not os.path.isdir(directory):
        return ""
    exact = os.path.join(directory, primary_name)
    if os.path.isfile(exact):
        return _read_file(exact)
    try:
        for fname in os.listdir(directory):
            if not fname.lower().endswith(".md"):
                continue
            fl = fname.lower()
            for kw in fallback_keywords:
                if kw in fl:
                    return _read_file(os.path.join(directory, fname))
    except Exception:
        pass
    return ""


def _count_text_length(text: str) -> int:
    """中英文混合计数：中文字符数 + 英文单词数"""
    cn = len(re.findall(r"[\u4e00-\u9fff]", text))
    en = len(re.findall(r"[a-zA-Z]+", text))
    return cn + en


# ============================================================
# 一、文件交付 (10 分)
# ============================================================

def _eval_delivery(answer_dir: str) -> Tuple[int, dict]:
    """
    检查两个交付文件是否存在并具有合理长度。
    speech_transcript.md: 存在 3分, 长度充足 3分
    qa_preparation.md:    存在 2分, 长度充足 2分
    """
    score = 0
    details: Dict[str, str] = {}

    speech = _find_deliverable(answer_dir, "speech_transcript.md",
                               ["speech", "transcript", "演讲"])
    qa = _find_deliverable(answer_dir, "qa_preparation.md",
                           ["qa", "question", "问答", "preparation"])

    # speech_transcript.md 存在 (3 分)
    if speech:
        score += 3
        details["speech_transcript.md"] = "存在"
    else:
        details["speech_transcript.md"] = "缺失 (-3)"

    # speech 长度 (3 分) — 一小时演讲至少 3000 字/词
    if speech:
        slen = _count_text_length(speech)
        if slen >= 3000:
            score += 3
            details["演讲稿长度"] = f"{slen} 字/词 — 充分"
        elif slen >= 1500:
            score += 2
            details["演讲稿长度"] = f"{slen} 字/词 — 偏短 (-1)"
        elif slen >= 500:
            score += 1
            details["演讲稿长度"] = f"{slen} 字/词 — 过短 (-2)"
        else:
            details["演讲稿长度"] = f"{slen} 字/词 — 严重不足"
    else:
        details["演讲稿长度"] = "N/A"

    # qa_preparation.md 存在 (2 分)
    if qa:
        score += 2
        details["qa_preparation.md"] = "存在"
    else:
        details["qa_preparation.md"] = "缺失 (-2)"

    # qa 长度 (2 分)
    if qa:
        qlen = _count_text_length(qa)
        if qlen >= 800:
            score += 2
            details["QA 长度"] = f"{qlen} 字/词 — 充分"
        elif qlen >= 300:
            score += 1
            details["QA 长度"] = f"{qlen} 字/词 — 偏短 (-1)"
        else:
            details["QA 长度"] = f"{qlen} 字/词 — 过短"
    else:
        details["QA 长度"] = "N/A"

    return score, details


# ============================================================
# 二、专业术语转化率 (25 分)
# ============================================================

# 任务要求覆盖的核心量子术语
_CORE_TERMS = [
    ("quantum superposition", "叠加", "superposition"),
    ("entanglement", "纠缠", "entanglement"),
    ("qubit", "量子比特", "qubit"),
    ("decoherence", "退相干", "decoherence"),
    ("quantum gate", "量子门", "quantum gate"),
    ("quantum algorithm", "量子算法", "quantum algorithm"),
    ("measurement", "测量", "观测", "measurement", "observation"),
    ("interference", "干涉", "interference"),
]

_TERM_LLM_PROMPT = """\
你是一个科技传播评估专家。请评估以下面向高中生的量子计算演讲稿，是否有效地将关键专业术语转化为通俗易懂的语言。

任务要求识别并转化 5-8 个关键术语。核心术语包括：
quantum superposition（量子叠加）、entanglement（量子纠缠）、qubit（量子比特）、
decoherence（退相干）、quantum gate（量子门）、quantum algorithm（量子算法）、
measurement/observation（测量/观测）、interference（干涉）

评估标准：
- 22-25 分（优秀）：5 个以上术语都有清晰的类比或通俗解释，解释准确且生动
- 16-21 分（良好）：大部分术语有解释，但部分解释不够深入或类比不贴切
- 10-15 分（中等）：只有少数术语被解释，多数术语直接使用未做转化
- 0-9 分（差）：几乎没有术语转化，或解释存在科学错误

[演讲稿]
{speech}

请严格按 JSON 格式返回（不含其他内容）：
{{"score": <0-25>, "covered_terms": ["已被通俗解释的术语"], "uncovered_terms": ["未被解释的术语"], "reasoning": "简短评分理由"}}
"""


def _eval_terminology(speech: str, config: dict) -> Tuple[int, dict]:
    if not speech:
        return 0, {"error": "演讲稿缺失，无法评估术语转化"}

    # 确定性预检：统计哪些核心术语在文中被提及
    speech_lower = speech.lower()
    mentioned = []
    not_mentioned = []
    for term_group in _CORE_TERMS:
        found = False
        for alias in term_group:
            if alias.lower() in speech_lower:
                found = True
                break
        if found:
            mentioned.append(term_group[0])
        else:
            not_mentioned.append(term_group[0])

    details: Dict[str, Any] = {
        "提及的术语": mentioned,
        "未提及的术语": not_mentioned,
        "提及数量": f"{len(mentioned)}/{len(_CORE_TERMS)}",
    }

    # LLM-as-Judge 深度评估
    prompt = _TERM_LLM_PROMPT.format(speech=speech[:12000])
    raw = _call_llm_judge(prompt, config)
    result = _extract_json(raw)

    if result and "score" in result:
        llm_score = max(0, min(25, int(result["score"])))
        details["LLM评分"] = llm_score
        details["LLM已覆盖术语"] = result.get("covered_terms", [])
        details["LLM评分理由"] = result.get("reasoning", "")
        return llm_score, details

    # Fallback：基于提及数量保守评分
    if len(mentioned) >= 6:
        fallback = 15
    elif len(mentioned) >= 4:
        fallback = 10
    elif len(mentioned) >= 2:
        fallback = 6
    else:
        fallback = 2
    details["fallback"] = f"LLM 不可用，基于术语提及数保守给分 {fallback}/25"
    return fallback, details


# ============================================================
# 三、受众适应性 (25 分)
# ============================================================

_AUDIENCE_LLM_PROMPT = """\
你是一个教育评估专家。请评估以下面向 15-18 岁高中生的量子计算演讲稿在受众适应性方面的表现。

目标受众：高中生（15-18 岁），理科与文科混合，已学过经典力学但几乎没有量子物理基础，
82% 觉得量子计算"很神秘很难懂"。注意力集中时间约 15-20 分钟。

评估两个子维度：

**A. 语言通俗性 (13 分)**
- 12-13 分：句式简短通俗，避免公式，使用日常口语化表达，流畅自然
- 9-11 分：大部分语言适合高中生，但偶有复杂学术句式
- 5-8 分：语言偏学术化，部分段落晦涩
- 0-4 分：语言过于学术，充斥专业用语和公式

**B. 生活化例子与场景 (12 分)**
- 11-12 分：使用了多个贴近青少年生活的例子（手机、游戏、硬币、考试、电影如复仇者联盟/星际穿越/三体等）
- 8-10 分：有生活化例子但数量较少或关联性不够强
- 4-7 分：例子较为抽象，与青少年日常关联不大
- 0-3 分：缺乏生活化例子

[演讲稿]
{speech}

请严格按 JSON 格式返回：
{{"readability_score": <0-13>, "example_score": <0-12>, "readability_reason": "...", "example_reason": "...", "examples_found": ["列出发现的生活化例子/类比"]}}
"""


def _eval_audience(speech: str, config: dict) -> Tuple[int, dict]:
    if not speech:
        return 0, {"error": "演讲稿缺失"}

    details: Dict[str, Any] = {}

    # 确定性预检
    speech_lower = speech.lower()
    # 公式符号密度
    formula_chars = len(re.findall(
        r"[∫∑∏√∂αβγδεζηθλμνξπρστφχψω∈∉⊂⊃∧∨¬→↔∀∃]", speech))
    formula_ratio = formula_chars / max(len(speech), 1)
    details["公式符号密度"] = f"{formula_ratio:.5f}"

    # 生活化关键词
    life_keywords = [
        "手机", "游戏", "硬币", "骰子", "考试", "电影", "漫威",
        "三体", "星际穿越", "抖音", "复仇者", "学校", "教室", "朋友",
        "音乐", "拼图", "迷宫", "旋转", "灯泡", "开关", "猫",
        "phone", "game", "coin", "dice", "movie", "imagine",
    ]
    found_keywords = [kw for kw in life_keywords if kw.lower() in speech_lower]
    details["生活化关键词"] = found_keywords

    # LLM-as-Judge
    prompt = _AUDIENCE_LLM_PROMPT.format(speech=speech[:12000])
    raw = _call_llm_judge(prompt, config)
    result = _extract_json(raw)

    if result and "readability_score" in result:
        r_score = max(0, min(13, int(result["readability_score"])))
        e_score = max(0, min(12, int(result["example_score"])))
        total = r_score + e_score
        details["语言通俗性"] = f"{r_score}/13 — {result.get('readability_reason', '')}"
        details["生活化例子"] = f"{e_score}/12 — {result.get('example_reason', '')}"
        details["发现的例子"] = result.get("examples_found", [])
        return total, details

    # Fallback
    r_fallback = 7 if formula_ratio < 0.003 else 4
    e_fallback = min(9, 3 + len(found_keywords))
    fallback = r_fallback + e_fallback
    details["fallback"] = f"LLM 不可用，保守给分 {fallback}/25"
    return fallback, details


# ============================================================
# 四、教育效果与结构 (25 分)
# ============================================================

_EDUCATION_LLM_PROMPT = """\
你是一个教育评估专家。请评估以下面向高中生的量子计算演讲稿的教育效果。

这是一个约一小时（或 20 分钟 + 10 分钟 Q&A）的讲座，在学校报告厅进行。

评估三个子维度：

**A. 演讲结构完整性 (8 分)**
- 7-8 分：结构清晰完整，有明确的引入（开场白/破冰）→ 核心概念讲解（叠加、纠缠等）→ 总结/收尾，有时间标记或章节划分
- 5-6 分：有基本结构但不够清晰，缺少明确的章节划分
- 3-4 分：结构松散，各部分衔接不自然
- 0-2 分：结构混乱或缺失

**B. 互动设计 (8 分)**
- 7-8 分：包含多种互动形式（提问、举手调查、想象实验、小讨论、投票等），分布合理
- 5-6 分：有一些互动设计但种类或频次不足
- 3-4 分：互动较少
- 0-2 分：几乎没有互动设计

**C. QA 准备质量 (9 分)**
（如果没有 QA 文件，此项给 0 分）
- 8-9 分：准备了 8 个以上有针对性的问题，回答质量高，覆盖不同层次
- 6-7 分：准备了 5-7 个问题，回答较为充分
- 3-5 分：问题数量不足或回答不够深入
- 0-2 分：QA 准备严重不足

[演讲稿]
{speech}

[QA 准备]
{qa}

请严格按 JSON 格式返回：
{{"structure_score": <0-8>, "interaction_score": <0-8>, "qa_score": <0-9>, "structure_reason": "...", "interaction_reason": "...", "qa_reason": "...", "interactions_found": ["发现的互动设计"]}}
"""


def _eval_education(speech: str, qa: str, config: dict) -> Tuple[int, dict]:
    details: Dict[str, Any] = {}
    if not speech:
        return 0, {"error": "演讲稿缺失"}

    speech_lower = speech.lower()

    # 确定性预检：结构标记
    has_intro = bool(re.search(
        r"开场|引入|引言|开头|破冰|大家好|同学们好|下午好|上午好|introduction|opening", speech_lower))
    has_core = bool(re.search(
        r"叠加|纠缠|量子比特|superposition|entanglement|qubit", speech_lower))
    has_summary = bool(re.search(
        r"总结|回顾|结尾|结语|小结|收尾|今天.*学|记住|conclusion|summary", speech_lower))
    has_sections = bool(re.search(
        r"\d+:\d+|第[一二三四五六七八九十]部分|part\s*\d|章节|\[.*?分钟\]|\[.*?:.*?\]", speech_lower))

    details["结构预检"] = {
        "引入": "有" if has_intro else "无",
        "核心概念": "有" if has_core else "无",
        "总结": "有" if has_summary else "无",
        "章节标记": "有" if has_sections else "无",
    }

    # 确定性预检：互动标记
    interaction_patterns = [
        (r"举手|请.*举", "举手调查"),
        (r"提问|请.*回答|谁.*知道|有.*同学", "课堂提问"),
        (r"想象|假设.*你|如果.*你|试着|闭上眼", "想象/思维实验"),
        (r"互动|实验|活动|讨论|小组", "互动活动"),
        (r"投票|选择|猜.*一下|挑战", "投票/挑战"),
        (r"调查|统计|现场", "现场调查"),
    ]
    found_interactions = []
    for pat, label in interaction_patterns:
        if re.search(pat, speech):
            found_interactions.append(label)
    details["互动预检"] = found_interactions if found_interactions else ["未检测到"]

    # 确定性预检：QA 问答对数量
    qa_question_count = 0
    if qa:
        qa_question_count = len(re.findall(
            r"(?:问[：:]|Q[：:]|\d+[)）.]\s*问|\d+[)）.]\s*[^\n]*[？?])", qa))
        details["QA问答对数"] = qa_question_count
    else:
        details["QA问答对数"] = "N/A（文件缺失）"

    # LLM-as-Judge
    qa_text = qa[:6000] if qa else "（QA 准备文件缺失）"
    prompt = _EDUCATION_LLM_PROMPT.format(speech=speech[:10000], qa=qa_text)
    raw = _call_llm_judge(prompt, config)
    result = _extract_json(raw)

    if result and "structure_score" in result:
        s_score = max(0, min(8, int(result["structure_score"])))
        i_score = max(0, min(8, int(result["interaction_score"])))
        q_score = max(0, min(9, int(result["qa_score"])))
        total = s_score + i_score + q_score
        details["结构完整性"] = f"{s_score}/8 — {result.get('structure_reason', '')}"
        details["互动设计"] = f"{i_score}/8 — {result.get('interaction_reason', '')}"
        details["QA准备质量"] = f"{q_score}/9 — {result.get('qa_reason', '')}"
        details["发现的互动"] = result.get("interactions_found", [])
        return total, details

    # Fallback：基于确定性检查保守给分
    struct_fb = 0
    if has_intro:
        struct_fb += 2
    if has_core:
        struct_fb += 2
    if has_summary:
        struct_fb += 2
    if has_sections:
        struct_fb += 1
    struct_fb = min(6, struct_fb)

    interact_fb = min(6, len(found_interactions) * 2)

    qa_fb = 0
    if qa:
        if qa_question_count >= 8:
            qa_fb = 6
        elif qa_question_count >= 5:
            qa_fb = 4
        elif qa_question_count >= 2:
            qa_fb = 2

    fallback = struct_fb + interact_fb + qa_fb
    details["fallback"] = f"LLM 不可用，保守给分 {fallback}/25"
    details["结构完整性(fallback)"] = f"{struct_fb}/8"
    details["互动设计(fallback)"] = f"{interact_fb}/8"
    details["QA准备(fallback)"] = f"{qa_fb}/9"
    return fallback, details


# ============================================================
# 五、创造性与比喻质量 (15 分)
# ============================================================

_CREATIVITY_LLM_PROMPT = """\
你是一个科技传播评估专家。请评估以下面向高中生的量子计算演讲稿的创造性。

**A. 比喻与类比质量 (10 分)**
- 9-10 分：使用了多个（5+）生动、准确、易懂的比喻/类比来解释复杂概念，比喻恰当且富有创意
- 7-8 分：有多个比喻但部分不够贴切或创意一般
- 4-6 分：比喻较少（1-2个）或质量一般
- 0-3 分：缺乏比喻或比喻不当、有科学误导

**B. 呈现方式创新 (5 分)**
- 5 分：呈现方式新颖（融合故事线、游戏、思想实验、视频引用、角色扮演等创新形式）
- 3-4 分：有一定创新但不够突出
- 0-2 分：呈现方式传统，纯讲授式

[演讲稿]
{speech}

请严格按 JSON 格式返回：
{{"metaphor_score": <0-10>, "innovation_score": <0-5>, "metaphors_found": ["列出发现的比喻/类比及其解释对象"], "innovation_elements": ["列出创新呈现元素"], "reasoning": "简短评分理由"}}
"""


def _eval_creativity(speech: str, config: dict) -> Tuple[int, dict]:
    if not speech:
        return 0, {"error": "演讲稿缺失"}

    details: Dict[str, Any] = {}

    # 确定性预检：比喻关键词
    metaphor_keywords = [
        "像", "好比", "类似于", "比喻", "就如", "仿佛", "想象", "比作",
        "就像", "如同", "好像", "相当于", "打个比方",
        "like", "analogy", "imagine", "as if", "think of",
    ]
    speech_lower = speech.lower()
    found_metaphor_kw = [kw for kw in metaphor_keywords if kw in speech_lower]
    details["比喻关键词"] = found_metaphor_kw

    # LLM-as-Judge
    prompt = _CREATIVITY_LLM_PROMPT.format(speech=speech[:12000])
    raw = _call_llm_judge(prompt, config)
    result = _extract_json(raw)

    if result and "metaphor_score" in result:
        m_score = max(0, min(10, int(result["metaphor_score"])))
        i_score = max(0, min(5, int(result["innovation_score"])))
        total = m_score + i_score
        details["比喻质量"] = f"{m_score}/10"
        details["呈现创新"] = f"{i_score}/5"
        details["发现的比喻"] = result.get("metaphors_found", [])
        details["创新元素"] = result.get("innovation_elements", [])
        details["评分理由"] = result.get("reasoning", "")
        return total, details

    # Fallback
    metaphor_count = len(found_metaphor_kw)
    m_fallback = min(6, metaphor_count)
    i_fallback = 2
    fallback = m_fallback + i_fallback
    details["fallback"] = f"LLM 不可用，保守给分 {fallback}/15"
    return fallback, details


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
        - report: dict 详细评估报告
    """
    report: Dict[str, Any] = {}

    # 读取交付文件
    speech = _find_deliverable(answer_dir, "speech_transcript.md",
                               ["speech", "transcript", "演讲"])
    qa = _find_deliverable(answer_dir, "qa_preparation.md",
                           ["qa", "question", "问答", "preparation"])

    # 如果两个文件都不存在，直接 0 分
    if not speech and not qa:
        report["error"] = "未找到任何交付文件 (speech_transcript.md / qa_preparation.md)"
        return 0, report

    # 如果只有 QA 没有演讲稿
    if not speech:
        report["error"] = "缺少核心交付物 speech_transcript.md"
        s1, d1 = _eval_delivery(answer_dir)
        report["一、文件交付"] = d1
        return min(s1, 4), report

    config = _get_text_eval_config(answer_dir)

    # 一、文件交付 (10 分)
    s1, d1 = _eval_delivery(answer_dir)

    # 二、专业术语转化率 (25 分)
    s2, d2 = _eval_terminology(speech, config)

    # 三、受众适应性 (25 分)
    s3, d3 = _eval_audience(speech, config)

    # 四、教育效果与结构 (25 分)
    s4, d4 = _eval_education(speech, qa, config)

    # 五、创造性与比喻质量 (15 分)
    s5, d5 = _eval_creativity(speech, config)

    total = s1 + s2 + s3 + s4 + s5
    total = max(0, min(100, total))

    report = {
        "总分": total,
        "分项得分": {
            "一、文件交付": f"{s1}/10",
            "二、专业术语转化率": f"{s2}/25",
            "三、受众适应性": f"{s3}/25",
            "四、教育效果与结构": f"{s4}/25",
            "五、创造性与比喻质量": f"{s5}/15",
        },
        "详细报告": {
            "一、文件交付": d1,
            "二、专业术语转化率": d2,
            "三、受众适应性": d3,
            "四、教育效果与结构": d4,
            "五、创造性与比喻质量": d5,
        },
    }

    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """打印格式化的评分报告"""
    print("=" * 70)
    print("评估报告 — 根据学术文章生成通俗演讲稿（量子计算 面向高中生）")
    print("=" * 70)
    print(f"\n总分: {score}/100\n")

    if "error" in report:
        print(f"[错误] {report['error']}")

    # 分项得分
    scores = report.get("分项得分", {})
    if scores:
        print("分项得分:")
        for k, v in scores.items():
            print(f"  {k}: {v}")

    # 详细报告
    details = report.get("详细报告", {})
    for section, content in details.items():
        print(f"\n{'─' * 55}")
        print(f"【{section}】")
        print(f"{'─' * 55}")
        if isinstance(content, dict):
            for k, v in content.items():
                if isinstance(v, list):
                    print(f"  {k}:")
                    for item in v:
                        print(f"    - {item}")
                elif isinstance(v, dict):
                    print(f"  {k}:")
                    for kk, vv in v.items():
                        print(f"    {kk}: {vv}")
                else:
                    print(f"  {k}: {v}")
        else:
            print(f"  {content}")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        test_dir = sys.argv[1]
    else:
        test_dir = os.path.join(os.path.dirname(__file__), "..", "gpt-5", "attempt_1")

    # 如果是相对路径，转为绝对路径
    if not os.path.isabs(test_dir):
        test_dir = os.path.join(os.path.dirname(__file__), "..", test_dir)
    test_dir = os.path.normpath(test_dir)

    if os.path.isdir(test_dir):
        print(f"正在评估目录: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"目录不存在: {test_dir}")
    sys.exit(0)
