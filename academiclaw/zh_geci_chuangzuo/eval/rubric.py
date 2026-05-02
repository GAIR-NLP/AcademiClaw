"""
boruizhang-query2 评分脚本
任务：从唐诗宋词元散曲中选择素材，以现代歌曲为结构模板，创作一首意象丰富的现代歌词
交付物：lyrics.md

总分 100 分

评分维度：
一、文件交付与格式规范 (15 分) — 确定性检查
   1. lyrics.md 存在且非空、长度达标 (6 分)
   2. 歌曲结构标注 verse/chorus 等 (5 分)
   3. 注明古典素材来源与现代歌曲模板 (4 分)

二、歌词内容质量 LLM 评估 (85 分) — 10 个维度
   基于意象融合和歌词创作标准，每维度 8.5 分：
   1. 造境能力
   2. 借境技巧
   3. 通俗易懂与雅俗共赏
   4. 真情实感
   5. 生动立体形象
   6. 明确价值判断
   7. 社会大众心理反映
   8. 人心社会洞察
   9. 情感内涵丰富细腻
   10. 文化厚重感
"""

import os
import re
import json
from typing import Tuple, Dict, Any

try:
    import openai
except ImportError:
    openai = None


# ---------------------------------------------------------------------------
# 环境与 LLM 工具
# ---------------------------------------------------------------------------

def _load_env(answer_dir: str) -> dict:
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
            max_tokens=4096,
            temperature=0,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        print(f"[RUBRIC] LLM Judge 调用失败: {e}")
        return ""


# ---------------------------------------------------------------------------
# 辅助：查找 lyrics.md
# ---------------------------------------------------------------------------

def _find_lyrics(answer_dir: str) -> str:
    candidates = [
        os.path.join(answer_dir, "lyrics.md"),
        os.path.join(answer_dir, "workspace", "lyrics.md"),
        os.path.join(answer_dir, "Lyrics.md"),
        os.path.join(answer_dir, "workspace", "Lyrics.md"),
        os.path.join(answer_dir, "LYRICS.md"),
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return ""


def _read_lyrics(answer_dir: str) -> str:
    path = _find_lyrics(answer_dir)
    if not path:
        return ""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read().strip()
    except Exception:
        return ""


# ---------------------------------------------------------------------------
# 一、文件交付与格式规范  (15 分)
# ---------------------------------------------------------------------------

def _eval_file_and_format(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details = {}

    lyrics_path = _find_lyrics(answer_dir)
    if not lyrics_path:
        return 0, {"错误": "未找到 lyrics.md", "得分": "0/15"}

    text = _read_lyrics(answer_dir)
    if not text:
        return 0, {"错误": "lyrics.md 为空", "得分": "0/15"}

    non_empty_lines = [ln for ln in text.splitlines() if ln.strip()]
    char_count = len(text)

    # --- 1.1 文件存在、非空且长度达标 (6 分) ---
    if len(non_empty_lines) >= 20 and char_count >= 300:
        score += 6
        details["文件与长度"] = f"6/6 — {len(non_empty_lines)} 行, {char_count} 字"
    elif len(non_empty_lines) >= 12 and char_count >= 150:
        score += 4
        details["文件与长度"] = f"4/6 — {len(non_empty_lines)} 行, {char_count} 字（偏短）"
    elif len(non_empty_lines) >= 5:
        score += 2
        details["文件与长度"] = f"2/6 — {len(non_empty_lines)} 行, {char_count} 字（过短）"
    else:
        score += 1
        details["文件与长度"] = f"1/6 — 仅 {len(non_empty_lines)} 行（严重过短）"

    # --- 1.2 歌曲结构标注 (5 分) ---
    lowered = text.lower()
    structure_kw = [
        "verse", "chorus", "bridge", "pre-chorus", "outro", "intro",
        "hook", "interlude", "coda",
        "副歌", "主歌", "桥段", "前奏", "尾声", "间奏",
    ]
    found = [kw for kw in structure_kw if kw in lowered]
    if len(found) >= 3:
        score += 5
        details["结构标注"] = f"5/5 — 含 {', '.join(found[:6])}"
    elif len(found) == 2:
        score += 3
        details["结构标注"] = f"3/5 — 仅含 {', '.join(found)}"
    elif len(found) == 1:
        score += 2
        details["结构标注"] = f"2/5 — 仅含 {found[0]}"
    else:
        details["结构标注"] = "0/5 — 未发现 verse/chorus 等结构标注"

    # --- 1.3 注明古典素材与现代歌曲模板 (4 分) ---
    has_classical = bool(re.search(
        r"(唐诗|宋词|元散曲|元曲|诗经|楚辞|古诗|古典|"
        r"李白|杜甫|苏轼|辛弃疾|李清照|柳永|白居易|王维|陶渊明|王昌龄|"
        r"张继|岳飞|陆游|纳兰|温庭筠|杜牧|刘禹锡|韦应物|孟浩然|"
        r"静夜思|水调歌头|青玉案|声声慢|如梦令|虞美人|蝶恋花|念奴娇|"
        r"满江红|天净沙|渔家傲|雨霖铃|临江仙|浣溪沙|鹧鸪天|"
        r"素材|选自|改编自|化用)", text
    ))
    has_template = bool(re.search(
        r"(模板|参考歌曲|结构模板|歌曲模板|结构参考|旋律参考|"
        r"《[^》]{2,}》)", text
    ))
    if has_classical and has_template:
        score += 4
        details["素材与模板"] = "4/4 — 标注了古典素材和歌曲模板"
    elif has_classical:
        score += 2
        details["素材与模板"] = "2/4 — 有古典素材说明但缺少歌曲模板"
    elif has_template:
        score += 1
        details["素材与模板"] = "1/4 — 有模板说明但缺少古典素材来源"
    else:
        details["素材与模板"] = "0/4 — 未注明古典素材或歌曲模板"

    details["文件路径"] = os.path.relpath(lyrics_path, answer_dir)
    return score, details


# ---------------------------------------------------------------------------
# 二、歌词内容质量 LLM 评估  (85 分)
# ---------------------------------------------------------------------------

DIMENSION_NAMES = [
    "造境能力",
    "借境技巧",
    "通俗易懂与雅俗共赏",
    "真情实感",
    "生动立体形象",
    "明确价值判断",
    "社会大众心理反映",
    "人心社会洞察",
    "情感内涵丰富细腻",
    "文化厚重感",
]

_LLM_PROMPT_TEMPLATE = """\
你是一位歌词创作和古典文学改编专家。请对以下现代歌词改编作品进行严格评估。
该歌词应当是基于唐诗宋词元散曲中的素材，以一首现代歌曲为结构模板创作而成。

【待评歌词】
---
{lyrics}
---

请从以下 10 个维度评分，每个维度 1-10 分（整数）。

**意象融合评估：**
1. 造境能力 — 是否通过创造具体景象来传达心理感受，而非直接抒情。如用"冷雨夜""寒冬""漫天大雪"等意象表达失落，做到情景交融。
2. 借境技巧 — 是否从古典诗词大师笔下"借境"，将古代经典意象巧妙融入现代歌词，实现古今对话。

**歌词创作标准评估：**
3. 通俗易懂与雅俗共赏 — 是否面向大众但不失品位，既不晦涩也不沦为口水歌。
4. 真情实感 — 是否投入了真实感情、描写了真实生活，避免假大空。
5. 生动立体形象 — 是否通过具体细致描述创造了可感画面，聚焦细节而非宏大叙事。
6. 明确价值判断 — 是否有独特的生活观点和深刻价值判断，能引发共鸣。
7. 社会大众心理反映 — 是否能反映某个群体或时期的普遍感知，引起广泛认同。
8. 人心社会洞察 — 是否有发人深省的金句，展现对人心人性的深刻洞察。
9. 情感内涵丰富细腻 — 是否敏锐捕捉特定情境下的情感震荡，呈现细致独到的内心世界。
10. 文化厚重感 — 是否通过化用典故、历史事件展现文化底蕴和历史厚度。

评分标准：
- 9-10: 杰出，专业水准
- 7-8: 优秀，有明显亮点
- 5-6: 良好，基本达标但有改进空间
- 3-4: 一般，表现不足
- 1-2: 较差，几乎无体现

注意：请严格评分。AI 生成的歌词通常在真情实感、人心洞察、社会心理等维度偏弱，请如实反映。
如果歌词明显不是古典诗词改编或缺乏歌曲结构，应在相应维度大幅扣分。

请严格按以下 JSON 格式返回（不要包含其他内容）：
```json
{{
  "dimensions": [
    {{"name": "造境能力", "score": 0, "reason": ""}},
    {{"name": "借境技巧", "score": 0, "reason": ""}},
    {{"name": "通俗易懂与雅俗共赏", "score": 0, "reason": ""}},
    {{"name": "真情实感", "score": 0, "reason": ""}},
    {{"name": "生动立体形象", "score": 0, "reason": ""}},
    {{"name": "明确价值判断", "score": 0, "reason": ""}},
    {{"name": "社会大众心理反映", "score": 0, "reason": ""}},
    {{"name": "人心社会洞察", "score": 0, "reason": ""}},
    {{"name": "情感内涵丰富细腻", "score": 0, "reason": ""}},
    {{"name": "文化厚重感", "score": 0, "reason": ""}}
  ],
  "overall_comment": ""
}}
```"""


def _parse_llm_json(raw: str) -> dict:
    text = raw
    if "```json" in text:
        text = text.split("```json", 1)[1].split("```", 1)[0].strip()
    elif "```" in text:
        text = text.split("```", 1)[1].split("```", 1)[0].strip()
    return json.loads(text)


def _eval_content_llm(answer_dir: str) -> Tuple[int, dict]:
    text = _read_lyrics(answer_dir)
    if not text:
        return 0, {"错误": "未找到或无法读取 lyrics.md", "得分": "0/85"}

    # 截断防止 token 溢出
    if len(text) > 8000:
        text = text[:8000] + "\n[...文本过长，已截断...]"

    config = _get_text_eval_config(answer_dir)
    prompt = _LLM_PROMPT_TEMPLATE.format(lyrics=text)
    raw = _call_llm_judge(prompt, config)

    if not raw:
        return _fallback_eval(text)

    try:
        result = _parse_llm_json(raw)
    except (json.JSONDecodeError, IndexError):
        print(f"[RUBRIC] LLM 返回解析失败，使用 fallback: {raw[:300]}")
        return _fallback_eval(text)

    dimensions = result.get("dimensions", [])
    details = {}
    total = 0.0

    for dim in dimensions:
        name = dim.get("name", "")
        raw_score = dim.get("score", 0)
        reason = dim.get("reason", "")
        clamped = max(1, min(10, int(raw_score)))
        # 映射 1-10 → 0.85-8.5（每维度满分 8.5）
        mapped = round(clamped * 0.85, 2)
        if name in DIMENSION_NAMES:
            total += mapped
            details[name] = f"{mapped}/8.5 — {reason}"

    # 补齐缺失维度
    for name in DIMENSION_NAMES:
        if name not in details:
            details[name] = "0/8.5 — LLM 未返回该维度"

    total = int(round(min(85, max(0, total))))
    details["LLM 总评"] = result.get("overall_comment", "")
    details["评估模型"] = config.get("model", "unknown")
    return total, details


def _fallback_eval(text: str) -> Tuple[int, dict]:
    """LLM 不可用时的保守降级评分（上限 34/85）"""
    details = {"注意": "LLM 不可用，使用降级评分（上限 34 分）"}
    score = 0
    lines = [ln for ln in text.splitlines() if ln.strip()]

    # 长度
    if len(lines) >= 25:
        score += 10
        details["长度"] = f"10 — {len(lines)} 行，充足"
    elif len(lines) >= 12:
        score += 5
        details["长度"] = f"5 — {len(lines)} 行，一般"
    else:
        score += 2
        details["长度"] = f"2 — {len(lines)} 行，过短"

    # 古典意象词汇
    classical = re.findall(
        r"(月|明月|霜|东风|花|柳|山|水|春|秋|夜|雪|雨|"
        r"故乡|相思|离别|思念|漂泊|天涯|归|远方|"
        r"唐|宋|诗人|词人|意象|长安|洛阳|江南|西风|"
        r"楼|酒|剑|琴|烟|云|船|桥)", text
    )
    if len(classical) >= 10:
        score += 12
        details["古典意象"] = f"12 — 发现 {len(classical)} 处"
    elif len(classical) >= 5:
        score += 6
        details["古典意象"] = f"6 — 发现 {len(classical)} 处"
    else:
        score += 2
        details["古典意象"] = f"2 — 仅 {len(classical)} 处"

    # 现代元素
    modern = re.findall(
        r"(手机|地铁|霓虹|城市|高楼|外卖|空调|广告|屏幕|公交|快递|"
        r"网络|电话|咖啡|耳机|wifi|出租车|朋友圈)", text
    )
    if len(modern) >= 3:
        score += 12
        details["现代元素"] = f"12 — 发现 {len(modern)} 处"
    elif len(modern) >= 1:
        score += 6
        details["现代元素"] = f"6 — 发现 {len(modern)} 处"
    else:
        score += 2
        details["现代元素"] = "2 — 未发现明显现代元素"

    score = min(34, score)
    details["降级总分"] = f"{score}/85（上限 34）"
    return score, details


# ---------------------------------------------------------------------------
# 入口
# ---------------------------------------------------------------------------

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """评估 agent 的输出。返回 (0-100 分, 报告 dict)。"""
    s1, r1 = _eval_file_and_format(answer_dir)
    s2, r2 = _eval_content_llm(answer_dir)

    total = min(100, max(0, s1 + s2))

    report = {
        "总分": total,
        "分项得分": {
            "文件交付与格式 (15)": s1,
            "歌词内容 LLM 评估 (85)": s2,
        },
        "一、文件交付与格式 (15 分)": r1,
        "二、歌词内容 LLM 评估 (85 分)": r2,
    }

    if total >= 80:
        report["评语"] = "优秀 — 歌词意象融合出色，古典与现代结合自然。"
    elif total >= 60:
        report["评语"] = "良好 — 有一定水准，但部分维度仍有提升空间。"
    elif total >= 40:
        report["评语"] = "一般 — 基本完成任务但创作质量有限。"
    elif total >= 15:
        report["评语"] = "较差 — 歌词存在明显不足。"
    else:
        report["评语"] = "不及格 — 未提交有效歌词。"

    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """打印格式化的评分报告。"""
    sep = "=" * 70
    thin = "-" * 50

    print(sep)
    print("boruizhang-query2  评分报告")
    print("任务：古典诗词改编现代歌词")
    print(sep)
    print(f"\n总分: {score}/100\n")

    parts = report.get("分项得分", {})
    if parts:
        print("分项得分:")
        for k, v in parts.items():
            print(f"  {k}: {v}")

    # 一、文件交付
    print(f"\n{thin}")
    print("【一、文件交付与格式 (15 分)】")
    print(thin)
    for k, v in report.get("一、文件交付与格式 (15 分)", {}).items():
        print(f"  {k}: {v}")

    # 二、LLM 评估
    print(f"\n{thin}")
    print("【二、歌词内容 LLM 评估 (85 分)】")
    print(thin)
    for k, v in report.get("二、歌词内容 LLM 评估 (85 分)", {}).items():
        if k in ("LLM 总评", "评估模型", "注意", "降级总分"):
            print(f"  [{k}] {v}")
        else:
            print(f"  {k}: {v}")

    print(f"\n{sep}")
    print(f"评语: {report.get('评语', '')}")
    print(sep)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        test_dir = sys.argv[1]
    else:
        test_dir = os.path.join(os.path.dirname(__file__), "..", "gpt-5", "attempt_1")

    # 支持相对路径
    if not os.path.isabs(test_dir):
        test_dir = os.path.join(
            os.path.dirname(__file__), "..", test_dir
        )
    test_dir = os.path.normpath(test_dir)

    if os.path.exists(test_dir):
        print(f"评估目录: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"目录不存在: {test_dir}")
    sys.exit(0)
