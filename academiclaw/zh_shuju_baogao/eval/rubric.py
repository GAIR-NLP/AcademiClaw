"""
评分脚本 — yiwang-query5: 亚洲男子短跑100米世界大赛奖牌可能性调研报告

任务: agent 需阅读 questions.json 中的研究问题，撰写一份多学科交叉的调研报告，
      系统分析未来10年亚洲男子短跑运动员在奥运会/世锦赛100米项目获得奖牌的可能性。

交付物:
  1. report.md     — 详细调研报告
  2. data_analysis.csv — 数据分析结果
  3. visualization.png — 数据可视化图表

总分: 100 分

评分维度:
  一、文件交付完整性  (15分)
  二、报告结构与格式  (15分)
  三、报告内容深度    (50分) — LLM-as-Judge 逐项检查 57 个评分要点
  四、数据分析质量    (10分)
  五、可视化质量      (10分)
"""

import os
import re
import csv
import json
import base64
import traceback
from typing import Tuple, Dict, Any, List, Optional

try:
    from PIL import Image
except ImportError:
    Image = None

try:
    import openai
except ImportError:
    openai = None


# ─────────────────────────────────────────────────────────────────────────────
# 配置与工具函数
# ─────────────────────────────────────────────────────────────────────────────

def _load_env(answer_dir: str) -> dict:
    """从 answer_dir 和 query 根目录加载 .env"""
    vals: dict = {}
    query_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    for d in [answer_dir, query_root]:
        p = os.path.join(d, ".env")
        if not os.path.isfile(p):
            continue
        try:
            with open(p, "r", encoding="utf-8") as fh:
                for raw in fh:
                    raw = raw.strip()
                    if not raw or raw.startswith("#") or "=" not in raw:
                        continue
                    k, v = raw.split("=", 1)
                    k = k.strip()
                    if k not in vals:
                        vals[k] = v.strip().strip("'\"")
        except Exception:
            pass
    return vals


def _cfg(answer_dir: str, kind: str = "text") -> dict:
    """获取 LLM 评估配置 (text 或 vision)"""
    env = _load_env(answer_dir)
    prefix = "EVAL_VISION" if kind == "vision" else "EVAL_TEXT"

    def g(key: str, default: str = "") -> str:
        return os.environ.get(key) or env.get(key) or default

    api_key = g(f"{prefix}_API_KEY", g("ANTHROPIC_API_KEY"))
    api_base = g(f"{prefix}_API_BASE_URL", g("ANTHROPIC_BASE_URL"))
    model = g(f"{prefix}_MODEL", "openai/gpt-5.2")

    if api_base:
        api_base = api_base.rstrip("/")
        if not api_base.endswith("/v1"):
            api_base += "/v1"

    return {"api_key": api_key, "api_base": api_base, "model": model}


def _llm_text(prompt: str, config: dict, max_tokens: int = 4096) -> str:
    """调用文本 LLM"""
    if not openai or not config.get("api_key"):
        return ""
    try:
        client = openai.OpenAI(api_key=config["api_key"], base_url=config["api_base"])
        resp = client.chat.completions.create(
            model=config["model"],
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0,
        )
        return resp.choices[0].message.content.strip()
    except Exception as exc:
        print(f"[RUBRIC] text-LLM error: {exc}")
        return ""


def _llm_vision(prompt: str, img_path: str, config: dict) -> str:
    """调用 vision LLM"""
    if not openai or not config.get("api_key"):
        return ""
    try:
        with open(img_path, "rb") as fh:
            b64 = base64.b64encode(fh.read()).decode()
        ext = os.path.splitext(img_path)[1].lower()
        mime = {".png": "image/png", ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg", ".webp": "image/webp"}.get(ext, "image/png")
        client = openai.OpenAI(api_key=config["api_key"], base_url=config["api_base"])
        resp = client.chat.completions.create(
            model=config["model"],
            messages=[{"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url",
                 "image_url": {"url": f"data:{mime};base64,{b64}"}},
            ]}],
            max_tokens=1024,
            temperature=0,
        )
        return resp.choices[0].message.content.strip()
    except Exception as exc:
        print(f"[RUBRIC] vision-LLM error: {exc}")
        return ""


def _extract_json(text: str) -> dict:
    if not text:
        return {}
    try:
        if "```json" in text:
            text = text.split("```json", 1)[1].split("```", 1)[0]
        elif "```" in text:
            text = text.split("```", 1)[1].split("```", 1)[0]
        return json.loads(text.strip())
    except Exception:
        return {}


# ─────────────────────────────────────────────────────────────────────────────
# 评分要点 (来源: rubric.json — 57 个要点，总权重 ~87)
# ─────────────────────────────────────────────────────────────────────────────

RUBRIC_POINTS: List[Dict[str, Any]] = [
    {"id": 1,  "w": 3, "pt": "分析未来10年内世界大赛中男子百米奖牌成绩,并与9秒77作比较"},
    {"id": 2,  "w": 3, "pt": "提到泰国运动员汶颂的最新成绩9秒94，并分析他的天赋与社会条件"},
    {"id": 3,  "w": 2, "pt": "解释男子100米成绩由多因素耦合决定的理论框架(遗传、生理、技术、装备、环境)"},
    {"id": 4,  "w": 2, "pt": "梳理亚洲男性短跑运动员的历史成绩演变趋势和突破节点(如苏炳添9.83、谢震业、山縣亮太等)"},
    {"id": 5,  "w": 2, "pt": "引用并分析与短跑成绩相关的遗传学研究(如ACTN3、ACE基因多态性在不同族群中的分布)"},
    {"id": 6,  "w": 2, "pt": "讨论亚洲人群在短跑相关的肌纤维组成(I型/II型比例)与爆发力潜力之间的关系"},
    {"id": 7,  "w": 2, "pt": "根据苏炳添、谢振业等成功运动员特点,分析中国短跑的选材标准"},
    {"id": 8,  "w": 2, "pt": "结合苏炳添换起跑脚取得成功,分析跑动技术大幅度更改对运动员的影响"},
    {"id": 9,  "w": 2, "pt": "分析最大无氧功率、ATP-PC能量系统输出速度、肌肉收缩速度对百米成绩的影响机理"},
    {"id": 10, "w": 2, "pt": "阐述亚洲选手在加速阶段(0-30m)与最大速度阶段(60-80m)的典型特征和差异"},
    {"id": 11, "w": 2, "pt": "论述短跑步态参数(步长、步频、接触时间、地面反作用力)对成绩的精细化影响机制"},
    {"id": 12, "w": 2, "pt": "描述国际顶尖短跑技术模型(如高速跑步的垂直力原则)及其对亚洲运动员的适用性"},
    {"id": 13, "w": 2, "pt": "分析现代高水平周期化训练体系(如短周期块训练法)对亚洲运动员可能产生的增益"},
    {"id": 14, "w": 1, "pt": "解释力量训练指标(RFD、最大力量、SSC利用效率)在亚洲运动员中的发展潜力"},
    {"id": 15, "w": 1, "pt": "讨论亚洲国家在短跑科技投入(如中日训练中心,3D动作捕捉实验室)对成绩的推动作用"},
    {"id": 16, "w": 2, "pt": "分析现代短跑装备(碳板钉鞋、能量回弹跑道)对亚洲运动员成绩的边际提升幅度"},
    {"id": 17, "w": 1, "pt": "评估风速、温度、海拔等外部环境对亚洲选手在世界大赛表现的潜在影响"},
    {"id": 18, "w": 2, "pt": "分析亚洲选手平均身体形态(身高、腿段比、肌腱刚度)与世界顶尖短跑选手的差异及可补偿空间"},
    {"id": 19, "w": 2, "pt": "引用短跑生物力学研究,分析亚洲选手提升地面反作用力峰值和身体刚度的潜力与路径"},
    {"id": 20, "w": 2, "pt": "总结世界大赛近20年男子100米奖牌成绩趋势,并预测未来奖牌门槛(如9.75-9.88)"},
    {"id": 21, "w": 2, "pt": "构建亚洲选手10-15年提升速度极限的统计模型(基于历史进步率和体能天花板)"},
    {"id": 22, "w": 1, "pt": "分析全球兴奋剂监管与合规趋势对亚洲选手与欧美非选手竞争格局的影响"},
    {"id": 23, "w": 1, "pt": "评估速度力量训练、神经驱动训练等项目对亚洲选手的可迁移性与优化方向"},
    {"id": 24, "w": 1, "pt": "讨论教练团队、科研支持(生物力学分析、运动营养)、康复团队对成绩的综合影响"},
    {"id": 25, "w": 2, "pt": "提出亚洲国家未来可能涌现更多短跑人才的原因(如人口基数、体教融合、专业训练体系)"},
    {"id": 26, "w": 1, "pt": "分析多国训练交流(如中日合作、中美训练营、日本与牙买加合作)的潜在增益"},
    {"id": 27, "w": 1, "pt": "说明心理压力管理、大赛心态和亚洲运动员典型心理特征对发挥的影响"},
    {"id": 28, "w": 1, "pt": "讨论亚洲运动员加入NCAA或欧洲职业训练体系后可能获得的速度提升空间"},
    {"id": 29, "w": 2, "pt": "预测未来10年AI训练、个性化生物力学建模、可穿戴技术将如何提升亚洲短跑"},
    {"id": 30, "w": 2, "pt": "评估亚洲选手在世锦赛/奥运会晋级决赛(Top 8)的概率及影响因素"},
    {"id": 31, "w": 2, "pt": "分析主要竞争对手国家(美国、牙买加、非洲诸国)未来实力变化对亚洲奖牌机会的影响"},
    {"id": 32, "w": 3, "pt": "构建综合预测模型：生理潜力×技术进步×训练科技×装备×对手水平×环境因素"},
    {"id": 33, "w": 3, "pt": "给出亚洲选手在未来10年内取得世界大赛男子100米奖牌的概率估计(如10%-25%)"},
    {"id": 34, "w": 2, "pt": "提出科学、可执行的训练体系建议以提升亚洲短跑奖牌可能性"},
    {"id": 35, "w": 2, "pt": "分析爆发力相关肌腱结构(如跟腱长度、肌腱刚度)在亚洲人群中的特点及对短跑的影响"},
    {"id": 36, "w": 1, "pt": "讨论神经肌肉激活速率(neural drive)在亚洲运动员中提升空间与科学手段"},
    {"id": 37, "w": 2, "pt": "研究青少年训练窗口期(敏感期)在亚洲运动员系统培养体系中的重要性及潜力"},
    {"id": 38, "w": 1, "pt": "分析亚洲运动员在高水平比赛中出现起跑反应时差异的原因及优化方法"},
    {"id": 39, "w": 1, "pt": "评估中枢神经系统疲劳、赛程密度对亚洲选手大赛表现的影响"},
    {"id": 40, "w": 1, "pt": "探讨营养学(肌酸、β-丙氨酸、咖啡因等)对亚洲运动员短跑能力提升的可行性"},
    {"id": 41, "w": 2, "pt": "分析亚洲运动员典型训练误区(如速度训练比例偏低)与优化路径"},
    {"id": 42, "w": 1, "pt": "讨论运动损伤模式(腘绳肌损伤发生率)在亚洲选手中的数据特征与防护策略"},
    {"id": 43, "w": 2, "pt": "引用生物信息学研究评估亚洲群体在速度相关基因的潜在上限与可进化空间"},
    {"id": 44, "w": 1, "pt": "分析经济投入、国家专项支持计划(如日本JAAF、中国短跑重点扶持)对速度项目的重要性"},
    {"id": 45, "w": 1, "pt": "评估高水平比赛风向与起跑道位优势对亚洲选手可能造成的边际影响"},
    {"id": 46, "w": 1, "pt": "讨论未来短跑装备可预期的技术突破(如新型碳纤维板结构、AI设计钉鞋)对亚洲运动员的贡献"},
    {"id": 47, "w": 1, "pt": "分析亚洲各国不同体育文化对短跑项目人才密度与投入度的影响"},
    {"id": 48, "w": 2, "pt": "总结影响奖牌概率的不可控因素(临场状态、伤病、对手失误等)并量化其影响范围"},
    {"id": 49, "w": 2, "pt": "分析起跑器角度与身体姿态的协同作用,最大化地面作用力的水平分量,利用拉长-缩短周期"},
    {"id": 50, "w": 2, "pt": "起跑技术中两抵脚板间距应为运动员胫骨长度(约占腿长45%),前抵脚板到起跑线距离为胫骨长度60%"},
    {"id": 51, "w": 2, "pt": "前抵脚板角度从70°减至30°时运动员最大蹬力显著增加,起跑速度加快"},
    {"id": 52, "w": 2, "pt": "短跑加速阶段身体重心前倾角度是决定水平加速力效率的核心生物力学因素"},
    {"id": 53, "w": 2, "pt": "短跑起跑及加速阶段能量供应高度依赖无氧代谢,由磷酸原系统(ATP-PCr)驱动"},
    {"id": 54, "w": 2, "pt": "通过优化身体姿态减小迎风面积和穿紧身比赛服降低阻力系数,减少空气阻力提高后程速度"},
    {"id": 55, "w": 2, "pt": "途中跑中高垂直力有助于减少触地时间,加速蹬伸进入下一步"},
    {"id": 56, "w": 2, "pt": "前摆期应尽量折叠以及勾脚尖以降低摆动力矩,提升摆动速度"},
    {"id": 57, "w": 2, "pt": "高海拔环境下低空气密度有益于运动员提升成绩"},
]

_TOTAL_W = sum(p["w"] for p in RUBRIC_POINTS)  # ~87


# ─────────────────────────────────────────────────────────────────────────────
# 辅助：查找文件
# ─────────────────────────────────────────────────────────────────────────────

def _ls(d: str) -> List[str]:
    return os.listdir(d) if os.path.isdir(d) else []


def _find(files: List[str], exact: str, fallback_ext: Optional[str] = None,
          fallback_kw: Optional[str] = None) -> Optional[str]:
    """在文件列表中按优先级查找"""
    for f in files:
        if f == exact:
            return f
    if fallback_kw:
        for f in files:
            if fallback_kw in f.lower() and (not fallback_ext or f.lower().endswith(fallback_ext)):
                return f
    if fallback_ext:
        for f in files:
            if f.lower().endswith(fallback_ext):
                return f
    return None


def _read_text(path: str) -> str:
    for enc in ("utf-8", "gbk", "latin-1"):
        try:
            with open(path, "r", encoding=enc) as fh:
                return fh.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
        except Exception:
            return ""
    return ""


# ─────────────────────────────────────────────────────────────────────────────
# 一、文件交付完整性 (15分)
# ─────────────────────────────────────────────────────────────────────────────

def _score_file_delivery(answer_dir: str) -> Tuple[int, dict]:
    files = _ls(answer_dir)
    score = 0
    det: Dict[str, str] = {}

    # --- report.md (5分) ---
    rf = _find(files, "report.md", ".md", "report")
    if rf:
        fp = os.path.join(answer_dir, rf)
        sz = os.path.getsize(fp)
        if sz >= 500:
            s = 5 if rf == "report.md" else 3
        elif sz > 0:
            s = 2
        else:
            s = 0
        score += s
        det["report.md"] = f"{s}/5 — {'存在' if rf == 'report.md' else '文件名不匹配: ' + rf} ({sz} B)"
    else:
        det["report.md"] = "0/5 — 未找到"

    # --- data_analysis.csv (5分) ---
    cf = _find(files, "data_analysis.csv", ".csv")
    if cf:
        fp = os.path.join(answer_dir, cf)
        sz = os.path.getsize(fp)
        if sz >= 50:
            s = 5 if cf == "data_analysis.csv" else 3
        elif sz > 0:
            s = 1
        else:
            s = 0
        score += s
        det["data_analysis.csv"] = f"{s}/5 — {'存在' if cf == 'data_analysis.csv' else '文件名不匹配: ' + cf} ({sz} B)"
    else:
        det["data_analysis.csv"] = "0/5 — 未找到"

    # --- visualization.png (5分) ---
    img_exts = (".png", ".jpg", ".jpeg", ".webp", ".svg")
    vf = _find(files, "visualization.png")
    if not vf:
        for f in files:
            if f.lower().endswith(img_exts):
                vf = f
                break
    if vf:
        fp = os.path.join(answer_dir, vf)
        sz = os.path.getsize(fp)
        valid = False
        if Image:
            try:
                Image.open(fp).verify()
                valid = True
            except Exception:
                pass
        else:
            valid = sz >= 1024
        if valid and sz >= 1024:
            s = 5 if vf == "visualization.png" else 3
        elif sz > 0:
            s = 1
        else:
            s = 0
        score += s
        det["visualization.png"] = f"{s}/5 — {'存在' if vf == 'visualization.png' else '文件名不匹配: ' + vf} ({sz} B)"
    else:
        det["visualization.png"] = "0/5 — 未找到"

    return score, det


# ─────────────────────────────────────────────────────────────────────────────
# 二、报告结构与格式 (15分)
# ─────────────────────────────────────────────────────────────────────────────

def _score_report_structure(answer_dir: str) -> Tuple[int, dict]:
    files = _ls(answer_dir)
    rf = _find(files, "report.md", ".md", "report")
    if not rf:
        return 0, {"错误": "无报告文件"}

    text = _read_text(os.path.join(answer_dir, rf))
    if not text.strip():
        return 0, {"错误": "报告文件为空"}

    score = 0
    det: Dict[str, str] = {}

    # --- 2a. 必要章节 (6分) ---
    checks = {
        "摘要/引言":   r"摘要|引言|简介|概述|背景|introduction|abstract|summary",
        "数据/方法":   r"方法|数据|methodology|method|data|分析方法|研究方法|分析框架",
        "结果/讨论":   r"结果|发现|讨论|result|finding|discussion|分析结果",
        "结论/建议":   r"结论|建议|总结|展望|conclusion|recommendation",
    }
    found = 0
    sec_detail = {}
    for name, pat in checks.items():
        if re.search(pat, text, re.IGNORECASE):
            found += 1
            sec_detail[name] = "有"
        else:
            sec_detail[name] = "缺"
    sec_s = min(6, found * 2 if found <= 3 else 6)
    score += sec_s
    det["章节"] = f"{sec_s}/6 — 命中 {found}/4"
    det["章节明细"] = str(sec_detail)

    # --- 2b. 报告长度 (5分) ---
    cn = len(re.findall(r"[\u4e00-\u9fff]", text))
    total_len = len(text)
    eff = max(total_len, cn * 2)
    if eff >= 8000:
        ls = 5
    elif eff >= 5000:
        ls = 4
    elif eff >= 3000:
        ls = 3
    elif eff >= 1000:
        ls = 1
    else:
        ls = 0
    score += ls
    det["长度"] = f"{ls}/5 — 字符 {total_len}, 中文 {cn}"

    # --- 2c. Markdown 格式 (4分) ---
    headings = re.findall(r"^#{1,4}\s+.+", text, re.MULTILINE)
    multi_level = len(set(re.findall(r"^(#{1,4})\s", text, re.MULTILINE))) >= 2
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    fs = 0
    if len(headings) >= 5:
        fs += 2
    elif len(headings) >= 2:
        fs += 1
    if multi_level:
        fs += 1
    if len(paras) >= 8:
        fs += 1
    fs = min(4, fs)
    score += fs
    det["格式"] = f"{fs}/4 — {len(headings)} 标题, {len(paras)} 段落, {'多级' if multi_level else '单级'}"

    return score, det


# ─────────────────────────────────────────────────────────────────────────────
# 三、报告内容深度 (50分) — LLM-as-Judge
# ─────────────────────────────────────────────────────────────────────────────

def _score_content(answer_dir: str) -> Tuple[int, dict]:
    files = _ls(answer_dir)
    rf = _find(files, "report.md", ".md", "report")
    if not rf:
        return 0, {"错误": "无报告文件"}

    text = _read_text(os.path.join(answer_dir, rf))
    if len(text.strip()) < 200:
        return 0, {"错误": "报告过短，无法评估内容"}

    # 截断以适应上下文
    text_trunc = text[:30000]

    pts_str = "\n".join(
        f"  {p['id']}. [权重{p['w']}] {p['pt']}" for p in RUBRIC_POINTS
    )

    prompt = f"""你是一个严格的学术调研报告评估专家。

待评估报告的主题是：未来10年亚洲男子短跑运动员在奥运会/世锦赛100米项目获得奖牌的可能性。

请逐一检查以下 {len(RUBRIC_POINTS)} 个评分要点在报告中的覆盖情况:

{pts_str}

评估标准:
- "full": 报告中有实质性、具体的讨论（有数据、论证或专业分析）→ 得分 = 权重值
- "partial": 提到了但不够深入，缺少具体支撑 → 得分 = 权重值 × 0.5
- "none": 完全未涉及 → 得分 = 0

请严格返回如下 JSON（不要包含其他内容）:
```json
{{
  "scores": [
    {{"id": 1, "c": "full", "s": 3}},
    {{"id": 2, "c": "none", "s": 0}}
  ],
  "comment": "总评一两句话"
}}
```
其中 id 是要点编号, c 是 full/partial/none, s 是该要点得分（上限为权重值）。
请确保 scores 数组包含全部 {len(RUBRIC_POINTS)} 个要点。

---报告原文---
{text_trunc}
---报告结束---"""

    config = _cfg(answer_dir, "text")
    raw = _llm_text(prompt, config)
    parsed = _extract_json(raw)

    if parsed and "scores" in parsed:
        return _process_llm_scores(parsed)

    # fallback: 关键词
    return _keyword_fallback(text)


def _process_llm_scores(parsed: dict) -> Tuple[int, dict]:
    raw_total = 0
    full_ct = partial_ct = none_ct = 0
    for item in parsed.get("scores", []):
        pid = item.get("id", 0)
        coverage = item.get("c", "none")
        s = item.get("s", 0)
        # 安全校验
        ref = next((p for p in RUBRIC_POINTS if p["id"] == pid), None)
        if ref:
            s = max(0, min(ref["w"], s))
            if coverage == "full":
                s = max(s, ref["w"])
                full_ct += 1
            elif coverage == "partial":
                s = min(s, ref["w"] * 0.5)
                partial_ct += 1
            else:
                s = 0
                none_ct += 1
        else:
            s = 0
        raw_total += s

    mapped = round(raw_total / max(_TOTAL_W, 1) * 50)
    mapped = max(0, min(50, mapped))

    det = {
        "得分": f"{mapped}/50",
        "原始加权": f"{raw_total:.1f}/{_TOTAL_W}",
        "完全覆盖": full_ct,
        "部分覆盖": partial_ct,
        "未覆盖": none_ct,
        "覆盖率": f"{(full_ct + partial_ct) / max(len(RUBRIC_POINTS), 1) * 100:.0f}%",
        "总评": parsed.get("comment", ""),
    }
    return mapped, det


def _keyword_fallback(text: str) -> Tuple[int, dict]:
    """LLM 不可用时关键词匹配（上限 25/50）"""
    tl = text.lower()
    groups = [
        (3, ["9秒77", "9.77", "奖牌成绩", "奖牌线"]),
        (3, ["汶颂", "bunsong", "泰国"]),
        (2, ["actn3", "ace基因", "遗传学"]),
        (2, ["苏炳添", "9.83", "9秒83"]),
        (2, ["谢震业", "山縣亮太", "桐生祥秀"]),
        (2, ["肌纤维", "ii型", "快肌", "爆发力"]),
        (2, ["步长", "步频", "触地时间", "地面反作用力", "生物力学"]),
        (2, ["atp", "磷酸原", "无氧代谢"]),
        (2, ["碳板", "钉鞋", "装备", "跑道"]),
        (2, ["训练", "周期化", "力量训练", "rfd"]),
        (3, ["预测", "概率", "模型", "10%", "25%"]),
        (2, ["起跑", "加速", "前倾", "蹬力"]),
        (2, ["海拔", "风速", "环境", "温度"]),
        (1, ["心理", "压力", "大赛心态"]),
        (1, ["营养", "肌酸", "咖啡因"]),
        (1, ["腘绳肌", "损伤", "康复"]),
        (2, ["牙买加", "美国", "竞争对手"]),
    ]
    hit_w = 0
    total_w = sum(w for w, _ in groups)
    hits = 0
    for w, kws in groups:
        if any(k in tl for k in kws):
            hit_w += w
            hits += 1
    mapped = min(25, round(hit_w / max(total_w, 1) * 25))
    return mapped, {"fallback": f"关键词匹配 {hits}/{len(groups)} 组, 得分 {mapped}/50 (上限25)"}


# ─────────────────────────────────────────────────────────────────────────────
# 四、数据分析质量 (10分)
# ─────────────────────────────────────────────────────────────────────────────

def _score_csv(answer_dir: str) -> Tuple[int, dict]:
    files = _ls(answer_dir)
    cf = _find(files, "data_analysis.csv", ".csv")
    if not cf:
        return 0, {"CSV": "0/10 — 未找到"}

    content = _read_text(os.path.join(answer_dir, cf))
    if not content.strip():
        return 0, {"CSV": "0/10 — 为空"}

    score = 0
    det: Dict[str, str] = {}

    # 解析
    try:
        rows = list(csv.reader(content.strip().split("\n")))
    except Exception:
        rows = [l.split(",") for l in content.strip().split("\n")]

    nr = len(rows)
    nc = len(rows[0]) if rows else 0

    # 格式 (3分)
    if nr >= 3 and nc >= 2:
        score += 3
        det["格式"] = f"3/3 — {nr} 行 × {nc} 列"
    elif nr >= 2:
        score += 1
        det["格式"] = f"1/3 — {nr} 行 × {nc} 列"
    else:
        det["格式"] = f"0/3 — 数据不足"

    # 数据量 (3分)
    data_rows = nr - 1  # 减去表头
    if data_rows >= 10:
        score += 3
        det["数据量"] = f"3/3 — {data_rows} 行数据"
    elif data_rows >= 3:
        score += 2
        det["数据量"] = f"2/3 — {data_rows} 行"
    elif data_rows >= 1:
        score += 1
        det["数据量"] = f"1/3 — 仅 {data_rows} 行"
    else:
        det["数据量"] = "0/3"

    # 内容相关性 (4分)
    cl = content.lower()
    kws = ["100m", "100米", "sprint", "短跑", "athlete", "运动员",
           "time", "成绩", "medal", "奖牌", "speed", "速度",
           "country", "国家", "year", "年", "record", "纪录",
           "苏炳添", "asia", "亚洲"]
    matched = sum(1 for k in kws if k in cl)
    if matched >= 5:
        score += 4
        det["相关性"] = f"4/4 — {matched} 个关键词命中"
    elif matched >= 3:
        score += 3
        det["相关性"] = f"3/4 — {matched} 个关键词"
    elif matched >= 1:
        score += 1
        det["相关性"] = f"1/4 — {matched} 个关键词"
    else:
        det["相关性"] = "0/4 — 无相关内容"

    return score, det


# ─────────────────────────────────────────────────────────────────────────────
# 五、可视化质量 (10分)
# ─────────────────────────────────────────────────────────────────────────────

def _score_vis(answer_dir: str) -> Tuple[int, dict]:
    files = _ls(answer_dir)
    img_exts = (".png", ".jpg", ".jpeg", ".webp")
    vf = _find(files, "visualization.png")
    if not vf:
        for f in files:
            if f.lower().endswith(img_exts):
                vf = f
                break
    if not vf:
        return 0, {"可视化": "0/10 — 未找到图片"}

    fp = os.path.join(answer_dir, vf)
    fsize = os.path.getsize(fp)
    score = 0
    det: Dict[str, Any] = {}

    # 基础检查 (3分)
    if Image:
        try:
            img = Image.open(fp)
            w, h = img.size
            if w >= 400 and h >= 300 and fsize >= 5120:
                score += 3
                det["基础"] = f"3/3 — {w}×{h}, {fsize // 1024}KB"
            elif w >= 200 and h >= 150:
                score += 2
                det["基础"] = f"2/3 — {w}×{h}, {fsize // 1024}KB"
            else:
                score += 1
                det["基础"] = f"1/3 — {w}×{h}"
        except Exception as e:
            det["基础"] = f"0/3 — 无法打开: {e}"
    else:
        if fsize >= 5120:
            score += 2
        elif fsize > 0:
            score += 1
        det["基础"] = f"{min(score,3)}/3 — {fsize // 1024}KB (PIL不可用)"

    # Vision LLM (7分)
    vis_prompt = """你是数据可视化评估专家。这张图片应该是关于「亚洲男子短跑100米」的数据可视化。

请按如下维度打分并返回 JSON:
```json
{
  "type_score": 0,
  "relevance_score": 0,
  "readability_score": 0,
  "total": 0,
  "comment": ""
}
```

维度:
- type_score (0-2): 图表类型是否合理(柱状图/折线图/散点图等)
- relevance_score (0-3): 内容是否与短跑/运动/成绩相关
- readability_score (0-2): 标题、轴标签、图例是否清晰"""

    config = _cfg(answer_dir, "vision")
    raw = _llm_vision(vis_prompt, fp, config)
    parsed = _extract_json(raw)

    if parsed and "total" in parsed:
        vs = max(0, min(7, int(parsed["total"])))
        score += vs
        det["Vision"] = {
            "类型": f"{parsed.get('type_score', '?')}/2",
            "相关": f"{parsed.get('relevance_score', '?')}/3",
            "可读": f"{parsed.get('readability_score', '?')}/2",
            "小计": f"{vs}/7",
            "评语": parsed.get("comment", ""),
        }
    else:
        # 降级: 文件大小
        fb = 3 if fsize >= 10240 else (2 if fsize >= 5120 else 1)
        score += fb
        det["Vision"] = f"{fb}/7 — LLM不可用，保守评分"

    return score, det


# ─────────────────────────────────────────────────────────────────────────────
# 主入口
# ─────────────────────────────────────────────────────────────────────────────

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    评估 agent 的输出。

    Args:
        answer_dir: agent 输出目录的绝对路径

    Returns:
        (score, report)
        - score: 0-100 整数
        - report: 评估详情 dict
    """
    s1, d1 = _score_file_delivery(answer_dir)
    s2, d2 = _score_report_structure(answer_dir)
    s3, d3 = _score_content(answer_dir)
    s4, d4 = _score_csv(answer_dir)
    s5, d5 = _score_vis(answer_dir)

    total = max(0, min(100, s1 + s2 + s3 + s4 + s5))

    if total >= 85:
        comment = "优秀！报告内容全面深入，数据分析和可视化质量高。"
    elif total >= 70:
        comment = "良好。报告覆盖了大部分要点，但部分维度有提升空间。"
    elif total >= 50:
        comment = "及格。基本完成任务但内容深度或覆盖面不足。"
    elif total >= 30:
        comment = "部分完成。交付物不全或内容严重不足。"
    else:
        comment = "不及格。任务未能有效完成。"

    report = {
        "总分": total,
        "分项得分": {
            "一、文件交付": f"{s1}/15",
            "二、报告结构": f"{s2}/15",
            "三、报告内容": f"{s3}/50",
            "四、数据分析": f"{s4}/10",
            "五、可视化":   f"{s5}/10",
        },
        "详细评估": {
            "一、文件交付 (15分)": d1,
            "二、报告结构 (15分)": d2,
            "三、报告内容 (50分)": d3,
            "四、数据分析 (10分)": d4,
            "五、可视化 (10分)":   d5,
        },
        "评语": comment,
    }
    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """打印格式化的评分报告"""
    print("=" * 70)
    print("yiwang-query5 评分报告")
    print("任务: 亚洲男子短跑100米世界大赛奖牌可能性调研报告")
    print("=" * 70)
    print(f"\n总分: {score}/100\n")

    for k, v in report.get("分项得分", {}).items():
        print(f"  {k}: {v}")

    for sec, data in report.get("详细评估", {}).items():
        print(f"\n{'─' * 60}")
        print(f"【{sec}】")
        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, dict):
                    print(f"  {k}:")
                    for kk, vv in v.items():
                        print(f"    {kk}: {vv}")
                else:
                    print(f"  {k}: {v}")
        else:
            print(f"  {data}")

    print(f"\n{'=' * 70}")
    print(f"评语: {report.get('评语', '')}")
    print("=" * 70)


# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        td = sys.argv[1]
    else:
        td = os.path.join(os.path.dirname(__file__), "..", "gpt-5", "attempt_1")

    if not os.path.isabs(td):
        td = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", td)
    td = os.path.abspath(td)

    if os.path.isdir(td):
        print(f"评估目录: {td}\n")
        s, r = evaluate(td)
        print_report(s, r)
    else:
        print(f"目录不存在: {td}")
        ws = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "workspace")
        if os.path.isdir(ws):
            print(f"使用 workspace/ 测试 (预期低分)\n")
            s, r = evaluate(ws)
            print_report(s, r)
    sys.exit(0)
