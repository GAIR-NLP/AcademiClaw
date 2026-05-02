#!/usr/bin/env python3
"""
IOL 2025 语言学奥林匹克竞赛评估脚本
任务: 求解第22届国际语言学奥林匹克竞赛 (IOL 2025) 个人赛五道题目
交付物: linguistics_solutions.md
总分: 100 分

评分维度:
  一、文件交付与基本内容  (10 分) — 程序化检查
  二、题目覆盖完整性      (15 分) — 程序化检查
  三、答案正确性与质量    (65 分) — LLM-as-Judge
  四、格式与结构          (10 分) — 程序化检查
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
# 环境与 LLM 配置
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
# 一、文件交付与基本内容 (10 分)
# ---------------------------------------------------------------------------

def _check_file_delivery(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    7 分: linguistics_solutions.md 存在 (文件名完全匹配)
          若文件名不匹配但有其他 .md 文件, 给 3 分
    3 分: 内容长度 ≥3000 字符 → 3, ≥1000 → 2, >0 → 1, 空 → 0
    """
    score = 0
    details = {}

    target = os.path.join(answer_dir, "linguistics_solutions.md")

    alt_md = []
    if os.path.isdir(answer_dir):
        for f in os.listdir(answer_dir):
            if f.endswith(".md") and f != "query.md":
                alt_md.append(f)

    # 文件存在 (7 分)
    chosen_file = None
    if os.path.isfile(target):
        score += 7
        details["文件名匹配"] = "7/7 — linguistics_solutions.md 存在"
        chosen_file = target
    elif alt_md:
        score += 3
        details["文件名匹配"] = f"3/7 — 未找到 linguistics_solutions.md, 备选: {', '.join(alt_md[:3])}"
        chosen_file = os.path.join(answer_dir, alt_md[0])
    else:
        details["文件名匹配"] = "0/7 — 未找到任何 .md 答案文件"

    # 内容充实度 (3 分)
    if chosen_file and os.path.isfile(chosen_file):
        try:
            with open(chosen_file, "r", encoding="utf-8") as f:
                content = f.read()
            n = len(content.strip())
            if n >= 3000:
                score += 3
                details["内容充实度"] = f"3/3 — {n} 字符"
            elif n >= 1000:
                score += 2
                details["内容充实度"] = f"2/3 — {n} 字符（偏短）"
            elif n > 0:
                score += 1
                details["内容充实度"] = f"1/3 — {n} 字符（过短）"
            else:
                details["内容充实度"] = "0/3 — 文件为空"
        except Exception as e:
            details["内容充实度"] = f"0/3 — 读取失败: {e}"
    else:
        details["内容充实度"] = "0/3 — 无可读取文件"

    return score, details


# ---------------------------------------------------------------------------
# 二、题目覆盖完整性 (15 分)
# ---------------------------------------------------------------------------

def _check_coverage(content: str) -> Tuple[int, Dict[str, Any]]:
    """每道题 3 分, 5 题共 15 分。通过关键词检测题目是否被提及。"""
    problems = [
        ("第一题 — 宗卡语", ["第一题", "宗卡语", "第1题", "问题一", "Problem 1", "Dzongkha", "题一"]),
        ("第二题 — 加姆语", ["第二题", "加姆语", "第2题", "问题二", "Problem 2", "Gaam", "题二"]),
        ("第三题 — 库利亚语", ["第三题", "库利亚语", "第3题", "问题三", "Problem 3", "Kuria", "题三"]),
        ("第四题 — 克瓦语", ["第四题", "克瓦语", "第4题", "问题四", "Problem 4", "Kewa", "题四"]),
        ("第五题 — 卡奇克尔语", ["第五题", "卡奇克尔语", "第5题", "问题五", "Problem 5", "Kaqchikel", "题五"]),
    ]

    score = 0
    details = {}
    found = 0
    lower = content.lower()
    for label, kws in problems:
        hit = any(kw.lower() in lower for kw in kws)
        if hit:
            found += 1
            score += 3
            details[label] = "3/3 — 已覆盖"
        else:
            details[label] = "0/3 — 未找到相关内容"

    details["总结"] = f"覆盖 {found}/5 道题目"
    return score, details


# ---------------------------------------------------------------------------
# 三、答案正确性与质量 (65 分) — LLM-as-Judge
# ---------------------------------------------------------------------------

# 参考答案：整理自 IOL 2025 官方解答
_REFERENCE = r"""
## 第一题参考答案（宗卡语数字系统, 20 分）

### 数字系统规则
基本数词: 1=ci, 2=ni/pi, 3=sum, 4=zi, 5=qa/pa, 6=du, 7=dyn, 8=ge, 9=gu, 10=cu/cutar, 15=ko, 半=pje
系统 A（二十进制）:
  n×20 = ke [n], n×20+m = ke [n] da [m]
  n×20+10 → ke pje-da [n的下一位], n×20+15 → ke ko-da [n的下一位]
  n×400 = pieu [n], pieu [n] da ke [m] da [r]
系统 B（十进制）:
  n×10 = (n)-cu (n≥3; 2×10=tsacu 或类似)
  n×10+m = (n的十位前缀)-(m)
  n×100 = (n)-ja

### (a) 填写 X, Y, Z
  X = dukcu（系统 B 中的 60）或等价
  Y = ke sum da ni (62 的系统 A 写法)
  Z = pieu ni da ke zi da qa (885 的系统 A 写法) 或等价

### (b) 等式的阿拉伯数字
  (1) 13 + 70 = 83
  (2) 800 = 20 × 40
  (3) 469 = (50 × 9) + 19
  (4) 600 + 110 = 500 + 210
  (5) (2 × 15) + 10 = 40 或 (pi × ko) + pje = pi（涉及 pje=半）
  (6) (1100 × 半) + 50 = 600
  (7) 736 = (84 × 4) + 400
  (8) 2 × 609 = (x × 400) + 18 → X = dukcu (60)
  (9) Y(62) + 24 = 86
  (10) Z(885) + 115 = 700 + 300

### (c)
  75: 系统 A = ke ko-da zi; 系统 B = dynpa (或 dyn-pa)
  570: 系统 A = pieu ci da ke pje-da gu; 系统 B = padyncu (或 pa-ja dyncu)

## 第二题参考答案（加姆语, 20 分）

### 形态学规则
  不可让渡领属（亲属/身体部位）: 所有者标记 + 名词
  可让渡领属: 名词 + 所有者标记
  复数: 亲属 -(VV)d; 身体部位/其他 -(VV)g
  人称: 1sg/2sg/3sg = a/o/e (变体)

### (a) 配对
  1-J, 2-A, 3-D, 4-T, 5-E, 6-S, 7-F, 8-B, 9-P, 10-L,
  11-H, 12-N, 13-G, 14-M, 15-Q, 16-K, 17-O, 18-I, 19-C, 20-R

### (b)
  tááðà = "他的奶奶"
  ē mǎo = "他的爷爷"
  解释: 这些词形式上看似不规则, 但亲属称谓的第三人称标记在某些情况下有特殊形式。

### (c) 翻译成汉语
  21. āg bòòrāāg — 我们的肩膀（复数）
  22. djōn rēg ǒyàg — 你的锤子（复数）
  23. ē bōōrààg — 他的肩膀（复数）
  24. ǒ túndúlìng — 你的手肘
  25. ó máàn — 你的阿姨

### (d) 翻译成加姆语
  26. 我的石磨 — gùùr ǒyàn
  27. 他们的脸颊（复数） — ēg fěndēg (或类似)
  28. 你们的锚 — tě lútìn (或类似)
  29. 我们的叔叔 — āg ābéé
  30. 你的狗（复数） — áðág ǔyùg (或类似)

## 第三题参考答案（库利亚语, 20 分）

### 声调与动词形态规则
  动词结构: (确实标记 n-)+ 主语标记 + 时态标记 + 词干
  主语标记: 1sg=n/nd, 1pl=to, 3sg=a, 3pl=βa
  时态: 现在=-V-, 过去=-aa-/-oo-, 将来=-ra-
  声调: 不同时态有不同的声调轮廓分配方式

### (a)
  20. ahéétóka

### (b) 翻译成汉语
  21. βasukură — 他们擦过（某物）
  22. toosya ifjímbéyo — 我们研磨过种子
  23. ndóma — 我咬（某物）
  24. naaβína — 确实, 他唱过（某物）

### (c) 翻译成库利亚语
  25. 我们要吃种子 — torarya ifjímbéyo (或 torarya itʃíimbéyo)
  26. 我唱（某物） — mbína (或 ndaβına)
  27. 确实, 我们测量过蛇鹭 — ntooβíímá íritáárákímúra (或类似)
  28. 我们要燃烧（某物） — torasaambă (或 torasáámba)
  29. 他想起过（某物） — aaheetóka

## 第四题参考答案（克瓦语, 20 分）

### 构词规则
  克瓦语用复合构词表达语义, 核心词素包括:
  repena=树/火, agaa=嘴/言语, iri=头发/草, ini=眼睛/种子,
  ada=女人, naaki=大/男人, uni=骨, yaa=鸟, mena=猪,
  ki=手/中间, komaa=臂, boke=洞, aga=林投, poripu=大/风,
  nogo=小, suku=闪亮, ora=真的/非常, bali/balina=白(外来)

### (a) 配对 (15-39 → A-Y)
  15-D, 16-N, 17-T, 18-L, 19-W, 20-O, 21-Y, 22-H, 23-I, 24-G,
  25-A, 26-Q, 27-C, 28-V, 29-P, 30-K, 31-U, 32-F, 33-M, 34-E,
  35-J, 36-X, 37-S, 38-R, 39-B

### (b) 翻译成汉语
  40. repena — 树; 火
  41. agaa — 嘴; 言语
  42. iri — 头发; 草
  43. yagaa — 下巴
  44. nida dia — 不是我
  45. yaa-iri — 鸟的羽毛
  46. nogo-naaki — 孩子 (小+大人)

### (c) 翻译成克瓦语
  47. 白人 — balina naaki 或 bali
  48. 骨 — uni
  49. 树的种子 — repena-ini  (与第1题形式相同)
  50. 洞 — boke
  51. 非常大 — ora adaa 或 ora poripu
  52. 林投 — aga
  53. 老女人的眼睛 — pannogae ada ini-agaa (或类似)

## 第五题参考答案（卡奇克尔语, 20 分）

### 语序与脑区规则
  颜色词: kāq=蓝, sāq=白, q'ēq=黑, xar=黄/绿
  数标记: ri=单数定冠词, taq=复数标记
  动词: xerunim=推, xkich'āy=抓, xeroyoj=追, xkinīm=推(复数主语),
        xeruq'eley=推倒, xerachik'aj=拖, xektiz'ēt=推

  语序模式与脑区活跃度:
    VOS → 听觉高, 额叶低 (最常见语序)
    VSO → 听觉高, 额叶高
    SVO → 听觉低, 额叶低
    OVS → 听觉低, 额叶高

### (a) 填空
  A = q'ēq
  B = ri
  C = Xeroyoj
  D = ri taq xar
  E = Xkinīm ri taq kāq (或 Ri taq kāq xkinīm)
  F = ri xar ri taq sāq
  G = Ri taq xar
  H = ri kāq
  I = Ri sāq xeruch'āy ri taq q'ēq

### (b) 图片描述
  9. Ri taq sāq xkinīm ri q'ēq — 多个白色追/推一个黑色
  10. Xekich'āy ri taq xar ri taq kāq — 多个黄色抓多个蓝色

### (c) 多种合法语序均可
### (d) 脑区活跃度预测
  11. Xeruq'eley ri kāq ri taq q'ēq → 额叶: 高, 听觉: 高 (VSO)
  12. Xerachik'aj ri taq sāq ri xar → 额叶: 低, 听觉: 高 (VOS)
  13. Ri taq q'ēq xektiz'ēt ri taq sāq → 额叶: 不确定(可能高或低), 听觉: 低 (SVO 或 OVS)
"""


def _build_judge_prompt(content: str) -> str:
    return f"""你是国际语言学奥林匹克竞赛 (IOL) 的专业评委。请根据官方参考答案, 严格评估参赛者提交的解答。

## 官方参考答案
{_REFERENCE}

## 参赛者提交的解答
{content[:30000]}

## 评分标准（总计 65 分）

逐题评分:

### 第一题 (13 分)
- 规则归纳 (0-3): 是否正确描述了二十进制(A)和十进制(B)系统
- (a) X/Y/Z 填空 (0-4): 每个正确约 1.3 分
- (b) 10 个等式的阿拉伯数字 (0-3): 大部分正确 3, 半数正确 2, 少数正确 1
- (c) 75 和 570 的双系统表达 (0-3): 每个系统每个数约 0.75 分

### 第二题 (13 分)
- 形态学规则 (0-3)
- (a) 20 对配对正确率 (0-4): ≥16 对 4 分, 12-15 对 3 分, 8-11 对 2 分, 4-7 对 1 分
- (b) tááðà 和 ē mǎo 翻译与解释 (0-2)
- (c)(d) 翻译 (0-4): 共 10 小题, 根据正确率给分

### 第三题 (13 分)
- 声调与形态规则 (0-3)
- (a) ahéétóka 声调标注 (0-2)
- (b) 4 题汉语翻译 (0-3): 人称/时态/动词均须正确
- (c) 5 题库利亚语翻译 (0-5): 含声调正确性

### 第四题 (13 分)
- (a) 25 对配对正确率 (0-5): ≥20 对 5 分, 15-19 对 4 分, 10-14 对 3 分, 5-9 对 2 分
- (b) 7 题汉语翻译 (0-3): 多义词需涵盖关键义项
- (c) 7 题克瓦语翻译 (0-5): 含 "与 1-39 中形式相同" 的识别

### 第五题 (13 分)
- 语序与脑区规则 (0-3)
- (a) A-I 共 9 个填空 (0-4): ≥7 个 4 分, 5-6 个 3 分, 3-4 个 2 分
- (b) 句子 9/10 图片描述 (0-2)
- (c) 句子写出 (0-2)
- (d) 3 句脑区活跃度预测 (0-2)

## 评分原则
1. 转写变体允许合理差异, 关键看语言学规律理解是否正确
2. 完全跳过某题 → 该题 0 分
3. 仅给答案不描述规则 → 规则分 0
4. 明显错误不给分, 严格评分
5. 每道题的 subtotal 不得超过该题满分

## 输出格式（严格 JSON, 不要有额外文字）
```json
{{
  "problem1": {{"rules": 0, "a_score": 0, "b_score": 0, "c_score": 0, "subtotal": 0, "comment": ""}},
  "problem2": {{"rules": 0, "a_score": 0, "bcd_score": 0, "subtotal": 0, "comment": ""}},
  "problem3": {{"rules": 0, "a_score": 0, "b_score": 0, "c_score": 0, "subtotal": 0, "comment": ""}},
  "problem4": {{"a_score": 0, "b_score": 0, "c_score": 0, "subtotal": 0, "comment": ""}},
  "problem5": {{"rules": 0, "a_score": 0, "b_score": 0, "c_score": 0, "d_score": 0, "subtotal": 0, "comment": ""}},
  "total": 0,
  "overall_comment": ""
}}
```"""


def _parse_llm_json(raw: str) -> dict:
    if not raw:
        return {}
    try:
        text = raw
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        return json.loads(text)
    except (json.JSONDecodeError, IndexError):
        m = re.search(r'"total"\s*:\s*(\d+)', raw)
        if m:
            return {"total": int(m.group(1)), "_parse_error": True}
        return {}


def _evaluate_correctness(content: str, answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    config = _get_text_eval_config(answer_dir)
    prompt = _build_judge_prompt(content)
    raw = _call_llm_judge(prompt, config)

    if not raw:
        print("[RUBRIC] LLM 不可用, 使用保守评分")
        return _fallback_correctness(content)

    scores = _parse_llm_json(raw)
    if not scores:
        print(f"[RUBRIC] LLM 返回解析失败, 使用保守评分")
        print(f"[RUBRIC] 原始响应片段: {raw[:500]}")
        return _fallback_correctness(content)

    details: Dict[str, Any] = {}
    total = 0

    prob_specs = [
        ("problem1", "第一题 — 宗卡语", 13),
        ("problem2", "第二题 — 加姆语", 13),
        ("problem3", "第三题 — 库利亚语", 13),
        ("problem4", "第四题 — 克瓦语", 13),
        ("problem5", "第五题 — 卡奇克尔语", 13),
    ]

    for key, label, cap in prob_specs:
        prob = scores.get(key, {})
        if isinstance(prob, dict):
            sub = min(cap, max(0, int(prob.get("subtotal", 0))))
            total += sub
            details[label] = f"{sub}/{cap} — {prob.get('comment', '')}"
        else:
            details[label] = f"0/{cap} — 无法解析"

    # 以 LLM 给出的 total 做交叉验证
    llm_total = scores.get("total", 0)
    if isinstance(llm_total, (int, float)):
        llm_total = min(65, max(0, int(llm_total)))
        if abs(llm_total - total) <= 5:
            total = llm_total

    total = min(65, max(0, total))
    details["使用模型"] = config.get("model", "unknown")
    details["LLM 原始响应长度"] = len(raw)

    return total, details


def _fallback_correctness(content: str) -> Tuple[int, Dict[str, Any]]:
    """LLM 不可用时的保守评分, 上限 25/65"""
    score = 0
    details: Dict[str, Any] = {"注意": "LLM 不可用, 采用保守降级评分（上限 25 分）"}
    n = len(content)

    # 基于长度
    if n > 10000:
        score += 10
    elif n > 5000:
        score += 6
    elif n > 2000:
        score += 3

    # 是否有配对格式 (数字-字母)
    if re.search(r'\d+\s*[-—:：]\s*[A-Y]', content):
        score += 5
        details["配对格式"] = "检测到"

    # 是否有翻译/解答内容
    if re.search(r'(翻译|→|——|—|汉语|加姆语|库利亚语|克瓦语|卡奇克尔语)', content):
        score += 5
        details["翻译内容"] = "检测到"

    # 是否有规则描述
    if re.search(r'(规[律则]|模式|pattern|rule|声调|语序|构词|形态)', content, re.IGNORECASE):
        score += 5
        details["规则描述"] = "检测到"

    score = min(25, score)
    details["降级得分"] = f"{score}/65 (上限 25)"
    return score, details


# ---------------------------------------------------------------------------
# 四、格式与结构 (10 分)
# ---------------------------------------------------------------------------

def _check_format(content: str) -> Tuple[int, Dict[str, Any]]:
    score = 0
    details = {}

    # 4a. Markdown 标题 (3 分)
    headings = re.findall(r'^#{1,4}\s+.+', content, re.MULTILINE)
    if len(headings) >= 10:
        score += 3
        details["标题结构"] = f"3/3 — {len(headings)} 个标题"
    elif len(headings) >= 5:
        score += 2
        details["标题结构"] = f"2/3 — {len(headings)} 个标题"
    elif headings:
        score += 1
        details["标题结构"] = f"1/3 — {len(headings)} 个标题（偏少）"
    else:
        details["标题结构"] = "0/3 — 无 Markdown 标题"

    # 4b. 题号标记 (3 分)
    markers = re.findall(
        r'(第[一二三四五1-5]题|题[一二三四五]|Problem\s*[1-5])',
        content, re.IGNORECASE,
    )
    unique = len(set(m.lower() for m in markers))
    if unique >= 5:
        score += 3
        details["题号标记"] = "3/3 — 五题均有标记"
    elif unique >= 3:
        score += 2
        details["题号标记"] = f"2/3 — {unique} 道题有标记"
    elif unique >= 1:
        score += 1
        details["题号标记"] = f"1/3 — {unique} 道题有标记"
    else:
        details["题号标记"] = "0/3 — 无题号标记"

    # 4c. 子问题标记 (2 分)
    subs = re.findall(r'\([a-e]\)', content, re.IGNORECASE)
    if len(subs) >= 10:
        score += 2
        details["子问题标记"] = f"2/2 — {len(subs)} 个"
    elif len(subs) >= 5:
        score += 1
        details["子问题标记"] = f"1/2 — {len(subs)} 个"
    else:
        details["子问题标记"] = f"0/2 — {len(subs)} 个（过少）"

    # 4d. 表格或列表 (2 分)
    has_table = bool(re.search(r'\|.*\|.*\|', content))
    has_list = bool(re.search(r'^[\-\*]\s+', content, re.MULTILINE))
    if has_table and has_list:
        score += 2
        details["表格与列表"] = "2/2 — 均使用"
    elif has_table or has_list:
        score += 1
        details["表格与列表"] = "1/2 — 仅使用了一种"
    else:
        details["表格与列表"] = "0/2 — 均未使用"

    return score, details


# ---------------------------------------------------------------------------
# 辅助: 读取答案文件
# ---------------------------------------------------------------------------

def _read_answer(answer_dir: str) -> str:
    target = os.path.join(answer_dir, "linguistics_solutions.md")
    if os.path.isfile(target):
        try:
            with open(target, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            pass

    if os.path.isdir(answer_dir):
        for fname in sorted(os.listdir(answer_dir)):
            if fname.endswith(".md") and fname != "query.md":
                try:
                    with open(os.path.join(answer_dir, fname), "r", encoding="utf-8") as f:
                        return f.read()
                except Exception:
                    continue
    return ""


# ---------------------------------------------------------------------------
# 入口: evaluate / print_report
# ---------------------------------------------------------------------------

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    评估 agent 的输出。

    Args:
        answer_dir: agent 输出目录的绝对路径

    Returns:
        (score, report) — score: 0-100, report: 详细评估报告
    """
    report: Dict[str, Any] = {}

    # 一、文件交付 (10)
    s1, r1 = _check_file_delivery(answer_dir)
    report["一、文件交付 (10分)"] = r1
    report["一、得分"] = f"{s1}/10"

    # 读取答案
    content = _read_answer(answer_dir)
    if not content:
        report["二、题目覆盖 (15分)"] = {"错误": "无法读取答案内容"}
        report["三、答案正确性 (65分)"] = {"错误": "无答案内容"}
        report["四、格式结构 (10分)"] = {"错误": "无答案内容"}
        total = s1
        report["总分"] = total
        return total, report

    # 二、题目覆盖 (15)
    s2, r2 = _check_coverage(content)
    report["二、题目覆盖 (15分)"] = r2
    report["二、得分"] = f"{s2}/15"

    # 三、答案正确性 (65)
    s3, r3 = _evaluate_correctness(content, answer_dir)
    report["三、答案正确性 (65分)"] = r3
    report["三、得分"] = f"{s3}/65"

    # 四、格式结构 (10)
    s4, r4 = _check_format(content)
    report["四、格式结构 (10分)"] = r4
    report["四、得分"] = f"{s4}/10"

    total = min(100, max(0, s1 + s2 + s3 + s4))
    report["总分"] = total

    if total >= 85:
        report["评语"] = "优秀。解答完整准确, 规则描述清晰, 格式规范。"
    elif total >= 70:
        report["评语"] = "良好。大部分答案正确, 部分题目有错误或不完整。"
    elif total >= 50:
        report["评语"] = "及格。覆盖了大部分题目, 但正确率和完整性有待提升。"
    elif total >= 30:
        report["评语"] = "不及格。较多题目未完成或答案错误严重。"
    else:
        report["评语"] = "严重不足。大部分题目缺失或完全错误。"

    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """打印格式化的评分报告"""
    print("=" * 70)
    print("IOL 2025 语言学奥林匹克竞赛 — 评分报告")
    print("=" * 70)
    print(f"\n总分: {score}/100")

    if "评语" in report:
        print(f"评语: {report['评语']}\n")

    sections = [
        "一、文件交付 (10分)",
        "二、题目覆盖 (15分)",
        "三、答案正确性 (65分)",
        "四、格式结构 (10分)",
    ]

    for sec in sections:
        score_key = sec[:2] + "得分"
        data = report.get(sec, {})
        sec_score = report.get(score_key, "?")
        print(f"\n{'─' * 50}")
        print(f"【{sec}】 {sec_score}")
        print(f"{'─' * 50}")
        if isinstance(data, dict):
            for k, v in data.items():
                if k == "LLM 原始响应长度":
                    print(f"  {k}: {v} 字符")
                else:
                    val = str(v)
                    if len(val) > 200:
                        val = val[:200] + "..."
                    print(f"  {k}: {val}")
        else:
            print(f"  {data}")

    print(f"\n{'=' * 70}")
    print(f"最终得分: {score}/100")
    print("=" * 70)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        test_dir = sys.argv[1]
    else:
        test_dir = os.path.join(os.path.dirname(__file__), "..", "gpt-5", "attempt_1")
    if not os.path.isabs(test_dir):
        test_dir = os.path.join(os.path.dirname(__file__), "..", test_dir)
    if os.path.exists(test_dir):
        print(f"[INFO] 评估目录: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"[ERROR] 目录不存在: {test_dir}")
        sys.exit(0)
