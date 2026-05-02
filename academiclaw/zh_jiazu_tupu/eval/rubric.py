"""
《百年孤独》布恩迪亚家族图谱构建 — 评分脚本

任务：
  Agent 需从 context/raw_text.txt 中分析《百年孤独》全文，
  提取布恩迪亚家族的人物姓名、代际、性格命运特征及亲属关系，
  输出为 solution.json（含 characters 列表）。

总分：100 分

维度          | 分值  | 说明
--------------+-------+--------------------------------------------------
一、文件交付  | 10 分 | solution.json 存在、可解析、字段完整
二、成员覆盖  | 15 分 | 是否覆盖全部核心家族成员
三、关键事实  | 50 分 | 5 个关键情节 / 关系测试点（每个 10 分）
四、LLM 评估  | 25 分 | 实体消歧 / 关系网络 / 特征描述综合评价
"""

import json
import os
import re
from typing import Any, Dict, List, Optional, Tuple

try:
    import openai
except ImportError:
    openai = None


# ────────────────────────────────────────────────────────────
# 环境与 LLM 工具
# ────────────────────────────────────────────────────────────

def _load_env(answer_dir: str) -> dict:
    values: dict = {}
    for d in [answer_dir, os.path.join(os.path.dirname(__file__), "..")]:
        p = os.path.join(d, ".env")
        if not os.path.exists(p):
            continue
        with open(p, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k, v = k.strip(), v.strip().strip("'\"")
                if k not in values:
                    values[k] = v
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
    except Exception as exc:
        print(f"[RUBRIC] LLM Judge error: {exc}")
        return ""


# ────────────────────────────────────────────────────────────
# 名字匹配工具
# ────────────────────────────────────────────────────────────

def _norm(name: str) -> str:
    """去除分隔符并转小写"""
    return re.sub(r"[·・\.\-\s（）()\[\]【】]", "", name).lower()


def _has_all(text: str, keywords: List[str]) -> bool:
    nt = _norm(text)
    return all(_norm(kw) in nt for kw in keywords)


def _has_any_set(text: str, kw_sets: List[List[str]]) -> bool:
    return any(_has_all(text, kws) for kws in kw_sets)


def _find_char(
    chars: List[dict],
    kw_sets: List[List[str]],
    gen: Optional[int] = None,
) -> Optional[dict]:
    for c in chars:
        name = c.get("name", "")
        if not _has_any_set(name, kw_sets):
            continue
        if gen is not None:
            cg = c.get("generation")
            if cg is not None and int(cg) != gen:
                continue
        return c
    return None


def _rel_text(char: dict, key: str) -> str:
    val = char.get("relations", {}).get(key, "")
    if isinstance(val, list):
        return " ".join(str(v) for v in val)
    return str(val)


def _all_rel_text(char: dict) -> str:
    """将人物的全部 relations 转为平坦文本以便模糊搜索"""
    rel = char.get("relations", {})
    parts: List[str] = []
    for v in rel.values():
        if isinstance(v, list):
            parts.extend(str(x) for x in v)
        else:
            parts.append(str(v))
    return " ".join(parts)


# ────────────────────────────────────────────────────────────
# 维度一：文件交付与格式 (10 分)
# ────────────────────────────────────────────────────────────

def _eval_file_format(answer_dir: str) -> Tuple[int, dict, Optional[List[dict]]]:
    score = 0
    details: dict = {}
    path = os.path.join(answer_dir, "solution.json")

    # 1) 文件存在 (3 分)
    if not os.path.exists(path):
        details["solution.json"] = "不存在 (0/3)"
        return 0, details, None
    score += 3
    details["solution.json"] = "存在 (3/3)"

    # 2) 合法 JSON + characters 列表 (3 分)
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        details["JSON 解析"] = f"失败: {e} (0/3)"
        return score, details, None

    # Accept "characters" or common alternatives like "members", "人物", "family_members"
    chars = data.get("characters")
    _field_used = "characters"
    if not isinstance(chars, list) or len(chars) == 0:
        for alt_key in ["members", "人物", "family_members", "roles", "people", "角色"]:
            chars = data.get(alt_key)
            if isinstance(chars, list) and len(chars) > 0:
                _field_used = alt_key
                break
    if not isinstance(chars, list) or len(chars) == 0:
        details["JSON 解析"] = "缺少非空 characters 列表 (0/3)"
        return score, details, None
    score += 3
    if _field_used != "characters":
        details["JSON 解析"] = f"成功 (字段名 '{_field_used}' 而非 'characters'), {len(chars)} 个角色 (3/3)"
    else:
        details["JSON 解析"] = f"成功, {len(chars)} 个角色 (3/3)"

    # 3) 字段完整性 (4 分)
    required = {"name", "generation", "traits", "relations"}
    ok = sum(1 for c in chars if required.issubset(c.keys()))
    ratio = ok / len(chars)
    if ratio >= 0.9:
        pts = 4
    elif ratio >= 0.7:
        pts = 3
    elif ratio >= 0.5:
        pts = 2
    elif ratio > 0:
        pts = 1
    else:
        pts = 0
    score += pts
    details["字段完整性"] = f"{ok}/{len(chars)} 完整 ({pts}/4)"

    return score, details, chars


# ────────────────────────────────────────────────────────────
# 维度二：成员覆盖度 (15 分)
# ────────────────────────────────────────────────────────────

# (关键词集合列表, 期望代数/None, 显示名)
_CORE = [
    ([["何塞", "阿尔卡蒂奥", "布恩迪亚"]], 1, "何塞·阿尔卡蒂奥·布恩迪亚 (始祖)"),
    ([["乌尔苏拉"]], 1, "乌尔苏拉"),
    ([["何塞", "阿尔卡蒂奥"]], 2, "何塞·阿尔卡蒂奥 (二代)"),
    ([["奥雷里亚诺"]], 2, "奥雷里亚诺上校 (二代)"),
    ([["阿玛兰妲"]], 2, "阿玛兰妲 (二代)"),
    ([["庇拉尔"]], None, "庇拉尔·特尔内拉"),
    ([["阿尔卡蒂奥"]], 3, "阿尔卡蒂奥 (三代)"),
    ([["奥雷里亚诺", "何塞"]], 3, "奥雷里亚诺·何塞 (三代)"),
    ([["美人儿"], ["美人"]], None, "美人儿蕾梅黛丝"),
    ([["奥雷里亚诺", "第二"], ["奥雷里亚诺", "segundo"], ["奥雷里亚诺", "二"]], 4, "奥雷里亚诺第二 (四代)"),
    ([["费尔南达"]], None, "费尔南达·德尔·卡皮奥"),
    ([["梅梅"], ["蕾梅黛丝"]], 5, "梅梅 / 雷娜塔·蕾梅黛丝 (五代)"),
    ([["阿玛兰妲", "乌尔苏拉"]], None, "阿玛兰妲·乌尔苏拉"),
    ([["奥雷里亚诺", "巴比伦"], ["奥雷里亚诺", "巴比倫"]], None, "奥雷里亚诺·巴比伦 (六代)"),
    ([["猪尾"]], None, "末代婴儿 (猪尾巴)"),
]


def _eval_coverage(chars: List[dict]) -> Tuple[int, dict]:
    found: List[str] = []
    missed: List[str] = []
    for kw_sets, gen, label in _CORE:
        c = _find_char(chars, kw_sets, gen)
        if c is None and gen is not None:
            c = _find_char(chars, kw_sets)
        # 末代婴儿：也尝试找 generation==7
        if c is None and "猪尾" in str(kw_sets):
            for x in chars:
                if x.get("generation") == 7:
                    c = x
                    break
                t = str(x.get("traits", ""))
                if "猪尾" in t or "猪尾巴" in t:
                    c = x
                    break
        # 梅梅备选
        if c is None and "梅梅" in str(kw_sets):
            c = _find_char(chars, [["蕾梅黛丝"]], gen=5)
        (found if c else missed).append(label)

    ratio = len(found) / len(_CORE) if _CORE else 0
    pts = min(15, round(ratio * 15))
    details = {
        "覆盖率": f"{len(found)}/{len(_CORE)} 核心成员 ({pts}/15)",
        "总角色数": len(chars),
    }
    if missed:
        details["未识别"] = ", ".join(missed[:6])
    return pts, details


# ────────────────────────────────────────────────────────────
# 维度三：关键事实检验 (50 分 = 5×10)
# ────────────────────────────────────────────────────────────

def _test_pilar(chars: List[dict]) -> Tuple[int, str]:
    """庇拉尔·特尔内拉分别与第二代两兄弟有私生子 (10 分)"""
    count = 0

    # 检查何塞·阿尔卡蒂奥 (二代) 是否记录庇拉尔
    jose2 = _find_char(chars, [["何塞", "阿尔卡蒂奥"]], gen=2)
    if jose2 is None:
        for c in chars:
            g = c.get("generation")
            n = c.get("name", "")
            if g == 2 and "何塞" in n and "阿尔卡蒂奥" in n and "上校" not in n:
                jose2 = c
                break
    if jose2:
        txt = _all_rel_text(jose2) + " " + str(jose2.get("traits", ""))
        if "庇拉尔" in txt or "特尔内拉" in txt:
            count += 1

    # 检查奥雷里亚诺上校 (二代)
    aur = _find_char(chars, [["奥雷里亚诺"]], gen=2)
    if aur is None:
        for c in chars:
            n = c.get("name", "")
            if ("上校" in n or "colonel" in n.lower()) and "奥雷里亚诺" in n:
                aur = c
                break
    if aur:
        txt = _all_rel_text(aur) + " " + str(aur.get("traits", ""))
        if "庇拉尔" in txt or "特尔内拉" in txt:
            count += 1

    # 再从庇拉尔自身条目交叉验证
    pilar = _find_char(chars, [["庇拉尔"]])
    if pilar and count < 2:
        ch_text = _rel_text(pilar, "children") + " " + str(pilar.get("traits", ""))
        has_j = "阿尔卡蒂奥" in ch_text
        has_a = "奥雷里亚诺" in ch_text
        if has_j and has_a:
            count = 2
        elif count == 0 and (has_j or has_a):
            count = 1
        # 也检查 traits 中的描述
        traits = str(pilar.get("traits", ""))
        if "两兄弟" in traits or ("何塞" in traits and "奥雷里亚诺" in traits):
            count = max(count, 2)

    if count >= 2:
        return 10, "正确识别庇拉尔与两兄弟的关系"
    elif count == 1:
        return 5, "仅识别出庇拉尔与一位兄弟的关系"
    elif pilar:
        return 3, "庇拉尔存在但关系不完整"
    return 0, "未识别庇拉尔·特尔内拉"


def _test_remedios(chars: List[dict]) -> Tuple[int, str]:
    """美人儿蕾梅黛丝飞升 (10 分)"""
    r = _find_char(chars, [["美人儿"], ["美人"]])
    if r is None:
        r = _find_char(chars, [["蕾梅黛丝"]], gen=4)
    if r is None:
        for c in chars:
            n = c.get("name", "") + " " + str(c.get("traits", ""))
            if "美人" in n and "蕾梅黛丝" in n:
                r = c
                break
    if r is None:
        return 0, "未识别美人儿蕾梅黛丝"

    t = str(r.get("traits", ""))
    fly_kw = ["升天", "飞升", "飞天", "升空", "脱离尘世", "消失在空中",
              "飘向天空", "床单", "升上", "飘走", "ascen", "飞走"]
    if any(k in t for k in fly_kw):
        return 10, "正确记录飞升结局"
    return 4, "存在但未提及飞升"


def _test_aur2(chars: List[dict]) -> Tuple[int, str]:
    """奥雷里亚诺第二：正式妻子费尔南达 + 情人佩特拉·科特斯 (10 分)"""
    a2 = None
    for c in chars:
        n = c.get("name", "")
        g = c.get("generation")
        if "奥雷里亚诺" in n and "上校" not in n and "何塞" not in n and "巴比伦" not in n and "巴比倫" not in n:
            if g == 4 or "第二" in n or "segundo" in n.lower() or "二" in n:
                a2 = c
                break
    if a2 is None:
        a2 = _find_char(chars, [["奥雷里亚诺", "第二"]], gen=4)
    if a2 is None:
        a2 = _find_char(chars, [["奥雷里亚诺", "二"]], gen=4)
    if a2 is None:
        return 0, "未识别奥雷里亚诺第二"

    all_txt = _all_rel_text(a2)
    spouse_txt = _rel_text(a2, "spouse")
    mistress_txt = _rel_text(a2, "mistress")

    has_fer = "费尔南达" in spouse_txt or "费尔南达" in all_txt
    has_pet = "佩特拉" in mistress_txt or "科特斯" in mistress_txt or \
              "佩特拉" in all_txt or "科特斯" in all_txt

    if has_fer and has_pet:
        return 10, "正确识别配偶(费尔南达)与情人(佩特拉)"
    if has_fer or has_pet:
        tag = f"配偶{'✓' if has_fer else '✗'} 情人{'✓' if has_pet else '✗'}"
        return 5, f"部分正确: {tag}"
    return 2, "存在但关系描述缺失"


def _test_pigtail(chars: List[dict]) -> Tuple[int, str]:
    """猪尾巴婴儿：其父母为奥雷里亚诺·巴比伦 & 阿玛兰妲·乌尔苏拉 (10 分)"""
    baby = None
    for c in chars:
        n = c.get("name", "")
        t = str(c.get("traits", ""))
        g = c.get("generation")
        if g == 7 or "猪尾" in n or "猪尾" in t:
            baby = c
            break
    if baby is None:
        return 0, "未识别猪尾巴婴儿"

    par = _rel_text(baby, "parents")
    # 也检查整个关系文本
    full = _all_rel_text(baby) + " " + str(baby.get("traits", ""))

    has_aur = ("巴比伦" in par or "巴比倫" in par or
               "巴比伦" in full or "巴比倫" in full)
    has_ama = (("阿玛兰妲" in par and "乌尔苏拉" in par) or
               "阿玛兰妲·乌尔苏拉" in full or
               _has_all(par, ["阿玛兰妲", "乌尔苏拉"]))

    if has_aur and has_ama:
        return 10, "正确记录父母 (奥雷里亚诺·巴比伦 & 阿玛兰妲·乌尔苏拉)"
    if has_aur or has_ama:
        return 6, "父母仅部分正确"
    traits = str(baby.get("traits", ""))
    if "猪尾" in traits:
        return 4, "有猪尾巴特征但父母缺失"
    return 2, "第七代存在但信息不完整"


def _test_generations(chars: List[dict]) -> Tuple[int, str]:
    """代际正确性抽查 (10 分)"""
    probes = [
        ([["乌尔苏拉"]], 1, "乌尔苏拉=Gen1"),
        ([["奥雷里亚诺"]], 2, "奥雷里亚诺上校=Gen2"),
        ([["美人儿"], ["美人"]], 4, "美人儿蕾梅黛丝=Gen4"),
        ([["阿玛兰妲", "乌尔苏拉"]], 5, "阿玛兰妲·乌尔苏拉=Gen5"),
        ([["奥雷里亚诺", "巴比伦"], ["奥雷里亚诺", "巴比倫"]], 6, "奥雷里亚诺·巴比伦=Gen6"),
    ]
    ok = 0
    checked = 0
    wrong: List[str] = []
    for kw_sets, expect, label in probes:
        c = _find_char(chars, kw_sets)
        if c is None:
            continue
        checked += 1
        actual = c.get("generation")
        if actual is not None and int(actual) == expect:
            ok += 1
        else:
            wrong.append(f"{label}(实际{actual})")

    if checked == 0:
        return 0, "关键人物缺失，无法验证"
    ratio = ok / checked
    pts = min(10, round(ratio * 10))
    msg = f"{ok}/{checked} 正确"
    if wrong:
        msg += f"; 错误: {'; '.join(wrong[:3])}"
    return pts, msg


def _eval_key_facts(chars: List[dict]) -> Tuple[int, dict]:
    tests = [
        ("3.1 庇拉尔·特尔内拉关系 (10分)", _test_pilar),
        ("3.2 美人儿蕾梅黛丝飞升 (10分)", _test_remedios),
        ("3.3 奥雷里亚诺第二双重关系 (10分)", _test_aur2),
        ("3.4 猪尾巴婴儿及父母 (10分)", _test_pigtail),
        ("3.5 代际正确性 (10分)", _test_generations),
    ]
    total = 0
    details: dict = {}
    for label, fn in tests:
        s, reason = fn(chars)
        total += s
        max_s = label.split("(")[1].rstrip("分)")
        details[label] = f"{s}/{max_s} — {reason}"
    return total, details


# ────────────────────────────────────────────────────────────
# 维度四：LLM 深度评估 (25 分)
# ────────────────────────────────────────────────────────────

_LLM_PROMPT = """\
你是熟读《百年孤独》（加西亚·马尔克斯）的文学评估专家。
以下是一份将布恩迪亚家族结构化为 JSON 的尝试。请从三个维度严格打分（整数）并简要说明理由。

**维度 1：实体消歧质量 (0-10 分)**
家族中大量同名：多个"何塞·阿尔卡蒂奥"、多个"奥雷里亚诺"、多个"蕾梅黛丝"。
- 9-10: 所有同名人物通过代际/职业/特征清楚区分
- 6-8: 大部分区分正确，少量混淆
- 3-5: 区分不清，明显混淆
- 0-2: 严重混淆

**维度 2：关系网络准确性 (0-8 分)**
- 7-8: 父母/配偶/子女/情人关系准确，乱伦/姨甥关系也正确
- 4-6: 主要关系正确，细节有误
- 2-3: 较多错误
- 0-1: 严重错误

**维度 3：人物特征描述质量 (0-7 分)**
- 6-7: traits 准确反映核心性格、职业、命运结局
- 4-5: 基本正确但缺乏关键细节
- 2-3: 过于笼统或有错误
- 0-1: 严重错误或缺失

严格按以下 JSON 回复（不含其他内容）：
```json
{{
  "disambiguation": {{"score": 0, "reason": ""}},
  "relations": {{"score": 0, "reason": ""}},
  "traits": {{"score": 0, "reason": ""}},
  "total": 0
}}
```

待评估 JSON:
```json
{json_content}
```"""


def _eval_llm(chars: List[dict], answer_dir: str) -> Tuple[int, dict]:
    config = _get_text_eval_config(answer_dir)
    js = json.dumps({"characters": chars}, ensure_ascii=False, indent=2)
    if len(js) > 12000:
        js = js[:12000] + "\n... (truncated)"

    raw = _call_llm_judge(_LLM_PROMPT.format(json_content=js), config)
    details: dict = {}

    if not raw:
        # fallback 保守分
        fb = 0
        if len(chars) >= 15:
            fb += 5
        elif len(chars) >= 10:
            fb += 3
        has_traits = sum(1 for c in chars if len(str(c.get("traits", ""))) > 10)
        if has_traits >= 10:
            fb += 4
        elif has_traits >= 5:
            fb += 2
        fb = min(fb, 15)
        details["LLM 状态"] = "不可用, 保守评分"
        details["保守分"] = f"{fb}/25"
        return fb, details

    try:
        text = raw
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        result = json.loads(text)
    except (json.JSONDecodeError, IndexError):
        details["LLM 状态"] = f"解析失败: {raw[:200]}"
        return 8, details

    dis = result.get("disambiguation", {})
    rel = result.get("relations", {})
    tra = result.get("traits", {})

    ds = max(0, min(10, int(dis.get("score", 0))))
    rs = max(0, min(8, int(rel.get("score", 0))))
    ts = max(0, min(7, int(tra.get("score", 0))))
    total = ds + rs + ts

    details["4.1 实体消歧 (10分)"] = f"{ds}/10 — {dis.get('reason', '')}"
    details["4.2 关系准确性 (8分)"] = f"{rs}/8 — {rel.get('reason', '')}"
    details["4.3 特征描述 (7分)"] = f"{ts}/7 — {tra.get('reason', '')}"
    details["评估模型"] = config.get("model", "unknown")
    return total, details


# ────────────────────────────────────────────────────────────
# 入口：evaluate / print_report
# ────────────────────────────────────────────────────────────

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    s1, d1, chars = _eval_file_format(answer_dir)

    if chars is None:
        report = {
            "总分": s1,
            "一、文件交付 (10分)": {"分数": s1, "详情": d1},
            "二、成员覆盖 (15分)": {"分数": 0, "详情": {"错误": "无法加载 characters"}},
            "三、关键事实 (50分)": {"分数": 0, "详情": {"错误": "无法加载 characters"}},
            "四、LLM评估 (25分)": {"分数": 0, "详情": {"错误": "无法加载 characters"}},
        }
        return s1, report

    s2, d2 = _eval_coverage(chars)
    s3, d3 = _eval_key_facts(chars)
    s4, d4 = _eval_llm(chars, answer_dir)

    total = s1 + s2 + s3 + s4

    report: Dict[str, Any] = {
        "总分": total,
        "一、文件交付 (10分)": {"分数": s1, "详情": d1},
        "二、成员覆盖 (15分)": {"分数": s2, "详情": d2},
        "三、关键事实 (50分)": {"分数": s3, "详情": d3},
        "四、LLM评估 (25分)": {"分数": s4, "详情": d4},
        "分项得分": {
            "文件交付": f"{s1}/10",
            "成员覆盖": f"{s2}/15",
            "关键事实": f"{s3}/50",
            "LLM评估": f"{s4}/25",
        },
    }
    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    print("=" * 70)
    print("《百年孤独》家族图谱构建 — 评分报告")
    print("=" * 70)
    print(f"\n总分: {score}/100\n")

    summary = report.get("分项得分", {})
    if summary:
        print("分项得分:")
        for k, v in summary.items():
            print(f"  {k}: {v}")

    for section in [
        "一、文件交付 (10分)",
        "二、成员覆盖 (15分)",
        "三、关键事实 (50分)",
        "四、LLM评估 (25分)",
    ]:
        sec = report.get(section, {})
        print(f"\n{'─' * 50}")
        print(f"【{section}】 {sec.get('分数', 0)} 分")
        print(f"{'─' * 50}")
        for k, v in sec.get("详情", {}).items():
            print(f"  {k}: {v}")

    print(f"\n{'=' * 70}")


if __name__ == "__main__":
    import sys
    d = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(__file__), "..", "gpt-5", "attempt_1")
    if os.path.exists(d):
        print(f"评估目录: {d}\n")
        s, r = evaluate(d)
        print_report(s, r)
    else:
        print(f"目录不存在: {d}")
    sys.exit(0)
