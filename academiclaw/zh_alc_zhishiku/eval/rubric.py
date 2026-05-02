"""
百年孤独 ALC 知识库构建 — 评分脚本 (从零重写)

任务：分析 context/context.txt 中《百年孤独》文本，构建 ALC 知识库 alc_kb.txt
      包含 TBox (概念包含公理 C ⊑ D)、ABox (断言 C(a) / R(a,b))、Non-ALC 分析

总分 100 分，分 6 个维度：
  一、文件交付          10 分
  二、结构与格式        20 分
  三、Evidence 标注     15 分
  四、信息覆盖率        30 分
  五、Non-ALC 分析      15 分
  六、内容质量 (LLM)    10 分
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
# 参考数据：从 context.txt 提取的 ground truth
# ============================================================

# 家谱中明确出现的人物名称
KNOWN_PERSONS = [
    "霍·阿·布恩蒂亚", "乌苏娜", "霍·阿卡蒂奥", "雷贝卡",
    "奥雷连诺上校", "雷麦黛丝·摩斯柯特", "阿玛兰塔", "皮拉·苔列娜",
    "阿卡蒂奥", "圣索菲娅·德拉佩德", "奥雷连诺·霍塞",
    "俏姑娘雷麦黛丝", "霍·阿卡蒂奥第二", "奥雷连诺第二",
    "菲兰达·德卡皮奥", "佩特娜·柯特", "梅梅",
    "阿玛兰塔·乌苏娜", "加斯东", "奥雷连诺·布恩蒂亚",
    "有尾巴的婴儿",
]

# 家谱关系关键词（应出现在 ABox 中）
RELATION_KEYWORDS = ["妻", "夫", "子", "女", "情妇", "后代", "长子", "次子", "小女儿"]

# 叙事段落中的关键实体
NARRATIVE_ENTITIES = ["马孔多", "梅尔加德斯", "吉卜赛人"]

# 叙事段落中的关键事实词（至少部分应被建模）
FACT_KEYWORDS = [
    "播种", "教养", "饲养", "勤劳", "磁铁", "天文",
    "金子", "套索", "鸟笼", "沼泽", "玻璃球",
    "族长", "斗鸡", "栗树",
]


# ============================================================
# 环境配置与 LLM 工具函数
# ============================================================

def _load_env(answer_dir: str) -> dict:
    """从 answer_dir 及 query 根目录加载 .env"""
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


# ============================================================
# 通用工具函数
# ============================================================

def _read_file(path: str) -> str:
    if not os.path.exists(path):
        return ""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


def _locate_answer(answer_dir: str) -> str:
    """定位 agent 输出的 alc_kb.txt（允许回退到其他 txt 文件）"""
    primary = os.path.join(answer_dir, "alc_kb.txt")
    if os.path.exists(primary):
        return primary
    if os.path.isdir(answer_dir):
        for fname in sorted(os.listdir(answer_dir)):
            if fname.endswith((".txt", ".md")) and "readme" not in fname.lower() and "context" not in fname.lower():
                return os.path.join(answer_dir, fname)
    return ""


def _strip_whitespace(text: str) -> str:
    """去除空白和常见标点，用于模糊子串匹配"""
    text = "".join(text.split())
    return re.sub(r'[.,;:!?\-"\'，。；：！？、""''（）()\[\]【】]', "", text)


def _split_sections(content: str):
    """将 alc_kb.txt 拆分为 TBox / ABox / Non-ALC 三段行列表"""
    tbox_lines: List[str] = []
    abox_lines: List[str] = []
    non_alc_lines: List[str] = []
    current = None

    for raw_line in content.split("\n"):
        line = raw_line.strip()
        lower = line.lower()

        if "tbox" in lower and "non" not in lower:
            current = "TBOX"
            continue
        if "abox" in lower and "non" not in lower:
            current = "ABOX"
            continue
        if "non-alc" in lower or "non_alc" in lower or "非alc" in lower or "不可表达" in lower or ("non" in lower and "alc" in lower):
            current = "NON"
            continue

        if not line or line.startswith("===") or line.startswith("```") or line.startswith("---"):
            continue

        if current == "TBOX":
            tbox_lines.append(line)
        elif current == "ABOX":
            abox_lines.append(line)
        elif current == "NON":
            non_alc_lines.append(line)

    return tbox_lines, abox_lines, non_alc_lines


# ============================================================
# 一、文件交付  (10 分)
# ============================================================

def _score_file_delivery(answer_dir: str) -> Tuple[int, dict]:
    pts = 0
    det = {}

    path = _locate_answer(answer_dir)

    # 1.1 文件存在且非空 (5 分)
    if not path:
        det["文件存在"] = "0/5 — 未找到 alc_kb.txt 或其他文本输出"
        det["文件名"] = "0/3 — N/A"
        det["内容长度"] = "0/2 — N/A"
        return 0, det

    content = _read_file(path)
    if not content.strip():
        det["文件存在"] = "0/5 — 文件存在但为空"
        det["文件名"] = "0/3 — N/A"
        det["内容长度"] = "0/2 — N/A"
        return 0, det

    pts += 5
    det["文件存在"] = "5/5 — 文件存在且非空"

    # 1.2 文件名正确 (3 分)
    fname = os.path.basename(path)
    if fname == "alc_kb.txt":
        pts += 3
        det["文件名"] = "3/3 — alc_kb.txt"
    elif "alc" in fname.lower():
        pts += 1
        det["文件名"] = f"1/3 — 含 alc 但非标准: {fname}"
    else:
        det["文件名"] = f"0/3 — 文件名不符: {fname}"

    # 1.3 内容长度合理 (2 分) — ALC KB 应有可观长度
    clen = len(content)
    if clen >= 2000:
        pts += 2
        det["内容长度"] = f"2/2 — {clen} 字符"
    elif clen >= 500:
        pts += 1
        det["内容长度"] = f"1/2 — {clen} 字符（偏短）"
    else:
        det["内容长度"] = f"0/2 — {clen} 字符（过短）"

    return pts, det


# ============================================================
# 二、结构与格式  (20 分)
# ============================================================

def _score_structure(content: str) -> Tuple[int, dict]:
    pts = 0
    det = {}
    tbox, abox, non_alc = _split_sections(content)

    # 2.1 三区域完整性 (6 分: 每区 2 分)
    sec = 0
    if tbox:
        sec += 2
    if abox:
        sec += 2
    if non_alc:
        sec += 2
    pts += sec
    det["区域完整性"] = f"{sec}/6 — TBox:{len(tbox)} ABox:{len(abox)} Non-ALC:{len(non_alc)}"

    # 2.2 TBox 语法: 应包含 ⊑ (5 分)
    if tbox:
        valid = sum(1 for l in tbox if "⊑" in l)
        ratio = valid / len(tbox)
        if ratio >= 0.8:
            s = 5
        elif ratio >= 0.5:
            s = 3
        elif valid > 0:
            s = 1
        else:
            s = 0
        pts += s
        det["TBox 语法"] = f"{s}/5 — {valid}/{len(tbox)} 含 ⊑ ({ratio:.0%})"
    else:
        det["TBox 语法"] = "0/5 — TBox 为空"

    # 2.3 ABox 语法: 应含 C(a) 或 R(a,b) (5 分)
    if abox:
        valid = sum(1 for l in abox if re.search(r'\w+\([^)]+\)', l))
        ratio = valid / len(abox)
        if ratio >= 0.8:
            s = 5
        elif ratio >= 0.5:
            s = 3
        elif valid > 0:
            s = 1
        else:
            s = 0
        pts += s
        det["ABox 语法"] = f"{s}/5 — {valid}/{len(abox)} 含断言格式 ({ratio:.0%})"
    else:
        det["ABox 语法"] = "0/5 — ABox 为空"

    # 2.4 命名规范: 使用原文中文命名 (4 分)
    combined = "\n".join(tbox + abox)
    hits = sum(1 for p in KNOWN_PERSONS[:10] if p in combined)
    if hits >= 8:
        s = 4
    elif hits >= 5:
        s = 2
    elif hits >= 2:
        s = 1
    else:
        s = 0
    pts += s
    det["中文命名"] = f"{s}/4 — 前 10 个人物命中 {hits}/10"

    return pts, det


# ============================================================
# 三、Evidence 标注  (15 分)
# ============================================================

def _score_evidence(content: str, context_text: str) -> Tuple[int, dict]:
    pts = 0
    det = {}
    tbox, abox, _ = _split_sections(content)
    stmts = tbox + abox

    if not stmts:
        det["标注覆盖"] = "0/7 — 无 TBox/ABox 条目"
        det["引文真实"] = "0/8 — N/A"
        return 0, det

    # 3.1 标注覆盖率 (7 分) — 每条应有 // evidence:
    with_ev = sum(1 for l in stmts if "evidence" in l.lower() or "原文" in l)
    ratio = with_ev / len(stmts)
    if ratio >= 0.9:
        s = 7
    elif ratio >= 0.6:
        s = 4
    elif ratio >= 0.3:
        s = 2
    else:
        s = 0
    pts += s
    det["标注覆盖"] = f"{s}/7 — {with_ev}/{len(stmts)} 含 evidence ({ratio:.0%})"

    # 3.2 引文真实性 (8 分) — 引用片段能否在 context.txt 中找到
    ctx_flat = _strip_whitespace(context_text) if context_text else ""
    if not ctx_flat:
        pts += 4
        det["引文真实"] = "4/8 — 无法加载 context.txt，给保守分"
        return pts, det

    checked = 0
    found = 0
    for line in stmts:
        parts = re.split(r'//\s*evidence\s*[:：]|//\s*原文\s*[:：]', line, flags=re.IGNORECASE)
        if len(parts) < 2:
            continue
        snippet = parts[-1].strip().strip('"').strip('\u201c\u201d\u201e\u201f')
        snippet_flat = _strip_whitespace(snippet)
        if len(snippet_flat) < 3:
            continue
        checked += 1
        if snippet_flat in ctx_flat:
            found += 1

    if checked == 0:
        det["引文真实"] = "0/8 — 未能提取有效 evidence 片段"
    else:
        vr = found / checked
        if vr >= 0.7:
            s = 8
        elif vr >= 0.4:
            s = 5
        elif vr >= 0.2:
            s = 2
        else:
            s = 0
        pts += s
        det["引文真实"] = f"{s}/8 — {found}/{checked} 可回溯原文 ({vr:.0%})"

    return pts, det


# ============================================================
# 四、信息覆盖率  (30 分)
# ============================================================

def _score_coverage(content: str) -> Tuple[int, dict]:
    pts = 0
    det = {}
    tbox, abox, _ = _split_sections(content)
    blob = "\n".join(tbox + abox)

    if not blob:
        det["人物覆盖"] = "0/12 — 无 TBox/ABox"
        det["关系覆盖"] = "0/8 — N/A"
        det["叙事实体"] = "0/4 — N/A"
        det["事实覆盖"] = "0/6 — N/A"
        return 0, det

    # 4.1 人物覆盖 (12 分)
    p_total = len(KNOWN_PERSONS)
    p_hits = sum(1 for p in KNOWN_PERSONS if p in blob)
    p_ratio = p_hits / p_total
    s = min(12, int(p_ratio * 12))
    pts += s
    det["人物覆盖"] = f"{s}/12 — {p_hits}/{p_total} ({p_ratio:.0%})"

    # 4.2 关系覆盖 (8 分)
    r_total = len(RELATION_KEYWORDS)
    r_hits = sum(1 for r in RELATION_KEYWORDS if r in blob)
    r_ratio = r_hits / r_total
    s = min(8, int(r_ratio * 8))
    pts += s
    det["关系覆盖"] = f"{s}/8 — {r_hits}/{r_total} ({r_ratio:.0%})"

    # 4.3 叙事实体 (4 分)
    n_total = len(NARRATIVE_ENTITIES)
    n_hits = sum(1 for n in NARRATIVE_ENTITIES if n in blob)
    n_ratio = n_hits / n_total
    s = min(4, int(n_ratio * 4))
    pts += s
    det["叙事实体"] = f"{s}/4 — {n_hits}/{n_total}"

    # 4.4 叙事事实 (6 分)
    f_total = len(FACT_KEYWORDS)
    f_hits = sum(1 for kw in FACT_KEYWORDS if kw in blob)
    f_ratio = f_hits / f_total
    s = min(6, int(f_ratio * 6))
    pts += s
    det["事实覆盖"] = f"{s}/6 — {f_hits}/{f_total} ({f_ratio:.0%})"

    return pts, det


# ============================================================
# 五、Non-ALC 分析  (15 分)
# ============================================================

def _score_non_alc(content: str) -> Tuple[int, dict]:
    pts = 0
    det = {}
    _, _, non_alc = _split_sections(content)
    blob = "\n".join(non_alc)

    if not non_alc:
        det["条目数量"] = "0/5 — Non-ALC 区域为空"
        det["解释深度"] = "0/10 — N/A"
        return 0, det

    # 5.1 至少 5 条 (5 分)
    # 尝试按编号匹配
    numbered = re.findall(r'^\s*\d+\s*[\.\)\]、]', blob, re.MULTILINE)
    count = len(numbered)
    if count == 0:
        # 回退：含"原因"/"无法"的行对数
        reason_lines = sum(1 for l in non_alc if "原因" in l or "无法" in l or "不能" in l)
        count = max(reason_lines, len(non_alc) // 3)

    if count >= 5:
        s = 5
    elif count >= 3:
        s = 3
    elif count >= 1:
        s = 1
    else:
        s = 0
    pts += s
    det["条目数量"] = f"{s}/5 — 检测到约 {count} 条"

    # 5.2 解释深度 (10 分) — 是否准确指出 ALC 无法表达的原因
    depth_keywords = [
        "计数", "数量", "基数", "数目",          # number restriction
        "时间", "时态", "过去", "未来", "变化",    # temporal
        "否定", "模态", "可能", "必然",            # modal
        "相信", "知道", "认为",                    # epistemic
        "概率", "程度", "比较", "最",              # comparative / degree
        "量词", "具体数值",                        # qualified number
        "传递", "对称", "自反",                    # role properties
        "n元", "多元",                            # n-ary
        "ALC", "限制", "表达",                     # meta
        "角色", "复合",                            # role composition
    ]
    kw_hits = sum(1 for kw in depth_keywords if kw in blob)
    if kw_hits >= 8:
        s = 10
    elif kw_hits >= 5:
        s = 7
    elif kw_hits >= 3:
        s = 4
    elif kw_hits >= 1:
        s = 2
    else:
        s = 0
    pts += s
    det["解释深度"] = f"{s}/10 — 命中 {kw_hits} 个 ALC 表达限制关键词"

    return pts, det


# ============================================================
# 六、内容质量 — LLM-as-Judge  (10 分)
# ============================================================

_LLM_PROMPT = """\
你是描述逻辑 (Description Logic) 和知识表示领域的专家评审。
请评估以下 ALC 知识库构建结果的质量。

**任务背景**
根据《百年孤独》的一段中文文本（含人物家谱及叙事段落），构建 ALC 知识库 K=<T,A>：
- TBox：概念包含公理 C ⊑ D
- ABox：断言 C(a) 或 R(a,b)
- Non-ALC：列举无法用标准 ALC 表达的信息并解释原因

**评分维度（整数打分，附简短理由）**

维度 1：TBox/ABox 建模质量 (0-5)
  5 = 概念层次合理，关系建模准确，充分利用 ALC 构造子（交、并、存在/全称量词、否定）
  3-4 = 基本合理但有遗漏或不够精细
  1-2 = 过于简单或有明显错误
  0 = 严重错误或几乎没有有效建模

维度 2：Non-ALC 分析深度 (0-5)
  5 = 准确识别 ALC 表达边界，给出形式化解释（数量限制、传递性、时态等）
  3-4 = 识别了部分边界但解释不够深入
  1-2 = 少量或不正确
  0 = 未有效分析

请严格按以下 JSON 格式回复，不要包含其他内容：
```json
{{"modeling_quality": {{"score": 0, "reason": ""}}, "non_alc_depth": {{"score": 0, "reason": ""}}, "total": 0}}
```

以下是待评估的内容（截取前 4000 字符）：
---
{content}
---
"""


def _score_llm_quality(content: str, answer_dir: str) -> Tuple[int, dict]:
    pts = 0
    det = {}

    if len(content.strip()) < 100:
        det["LLM 评估"] = "0/10 — 内容过少"
        return 0, det

    config = _get_text_eval_config(answer_dir)
    prompt = _LLM_PROMPT.format(content=content[:4000])
    raw = _call_llm_judge(prompt, config)

    if not raw:
        pts = 4
        det["LLM 评估"] = "4/10 — LLM 不可用，给保守分"
        return pts, det

    try:
        text = raw
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        result = json.loads(text)

        mq = result.get("modeling_quality", {})
        nd = result.get("non_alc_depth", {})
        mq_s = max(0, min(5, int(mq.get("score", 0))))
        nd_s = max(0, min(5, int(nd.get("score", 0))))
        pts = mq_s + nd_s

        det["建模质量"] = f"{mq_s}/5 — {mq.get('reason', '')}"
        det["Non-ALC 深度"] = f"{nd_s}/5 — {nd.get('reason', '')}"
        det["评估模型"] = config.get("model", "unknown")
    except Exception as e:
        pts = 4
        det["LLM 评估"] = f"4/10 — LLM 返回解析失败 ({str(e)[:80]})"
        if raw:
            det["LLM 原始返回"] = raw[:300]

    return pts, det


# ============================================================
# 主入口
# ============================================================

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """评估 agent 的 ALC 知识库构建输出。"""
    report: Dict[str, Any] = {}
    total = 0

    # 一、文件交付 (10 分)
    s1, d1 = _score_file_delivery(answer_dir)
    total += s1
    report["一、文件交付 (10分)"] = {"分数": s1, "详情": d1}

    # 无文件则终止
    path = _locate_answer(answer_dir)
    if not path:
        report["总分"] = 0
        report["评语"] = "未找到输出文件，无法评估。"
        return 0, report

    content = _read_file(path)

    # 加载 context.txt（用于 evidence 验证）
    ctx_path = os.path.join(os.path.dirname(__file__), "..", "context", "context.txt")
    context_text = _read_file(ctx_path)

    # 二、结构与格式 (20 分)
    s2, d2 = _score_structure(content)
    total += s2
    report["二、结构与格式 (20分)"] = {"分数": s2, "详情": d2}

    # 三、Evidence 标注 (15 分)
    s3, d3 = _score_evidence(content, context_text)
    total += s3
    report["三、Evidence 标注 (15分)"] = {"分数": s3, "详情": d3}

    # 四、信息覆盖率 (30 分)
    s4, d4 = _score_coverage(content)
    total += s4
    report["四、信息覆盖率 (30分)"] = {"分数": s4, "详情": d4}

    # 五、Non-ALC 分析 (15 分)
    s5, d5 = _score_non_alc(content)
    total += s5
    report["五、Non-ALC 分析 (15分)"] = {"分数": s5, "详情": d5}

    # 六、内容质量 (10 分)
    s6, d6 = _score_llm_quality(content, answer_dir)
    total += s6
    report["六、内容质量 (10分)"] = {"分数": s6, "详情": d6}

    total = min(100, total)

    report["总分"] = total
    report["分项得分"] = {
        "文件交付": f"{s1}/10",
        "结构格式": f"{s2}/20",
        "Evidence": f"{s3}/15",
        "覆盖率": f"{s4}/30",
        "Non-ALC": f"{s5}/15",
        "内容质量": f"{s6}/10",
    }

    if total >= 85:
        report["评语"] = "优秀。知识库结构完整，覆盖全面，Non-ALC 分析深入。"
    elif total >= 70:
        report["评语"] = "良好。基本完成任务，部分维度有改进空间。"
    elif total >= 50:
        report["评语"] = "及格。核心内容存在但不够完善。"
    elif total >= 30:
        report["评语"] = "部分完成。缺少关键内容或格式不规范。"
    else:
        report["评语"] = "不及格。任务完成度严重不足。"

    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """打印格式化的评分报告"""
    print("=" * 70)
    print("百年孤独 ALC 知识库构建 — 评分报告")
    print("=" * 70)
    print(f"\n总分：{score}/100\n")

    scores = report.get("分项得分", {})
    if scores:
        print("分项得分:")
        for k, v in scores.items():
            print(f"  {k}: {v}")

    section_keys = [
        "一、文件交付 (10分)",
        "二、结构与格式 (20分)",
        "三、Evidence 标注 (15分)",
        "四、信息覆盖率 (30分)",
        "五、Non-ALC 分析 (15分)",
        "六、内容质量 (10分)",
    ]
    for key in section_keys:
        sec = report.get(key, {})
        if not sec:
            continue
        print(f"\n{'─' * 50}")
        print(f"【{key}】 {sec.get('分数', 0)} 分")
        print(f"{'─' * 50}")
        for k, v in sec.get("详情", {}).items():
            print(f"  {k}: {v}")

    print(f"\n{'=' * 50}")
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
