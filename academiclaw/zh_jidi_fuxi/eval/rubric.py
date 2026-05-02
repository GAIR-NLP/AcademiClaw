"""
走进极地课程复习与模拟试卷生成 — 评分 Rubric
task_id: zhutianxiang_query2_polar_course_review

Deliverables:
  - study_notes.md  (复习笔记)
  - mock_exam.md    (模拟试卷，含答案解析与引用)

总分 100 分，分 6 个维度:
  一、文件交付          10 分
  二、复习笔记结构      20 分
  三、课件覆盖度        15 分
  四、模拟试卷结构      25 分
  五、引用规范          15 分
  六、内容质量 (LLM)    15 分
"""

from __future__ import annotations

import json
import os
import re
from typing import Any, Dict, List, Set, Tuple

try:
    import openai
except ImportError:
    openai = None

# ---------------------------------------------------------------------------
# 课件列表（来自 query.md Context 文件列表）
# ---------------------------------------------------------------------------

PDF_FILES: List[str] = [
    "第一课.pdf",
    "第二课.pdf",
    "第三课.pdf",
    "第四课.pdf",
    "第五课.pdf",
    "第六课.pdf",
    "第七课-Part1.pdf",
    "第七课-Part2.pdf",
    "第八课.pdf",
    "第十三课-极地资源与治理.pdf",
    "走进极地2025-第10节.pdf",
    "走进极地2025-第11节.pdf",
    "走进极地2025-第12节.pdf",
]

# ---------------------------------------------------------------------------
# 引用正则
#   严格格式: 【来源：第三课.pdf，第 4-6 页】
#   宽松格式: 【来源】第三课.pdf p.4-6
# ---------------------------------------------------------------------------

_CITE_STRICT = re.compile(
    r"【来源[：:]\s*([^，,\]]+)[，,]\s*第\s*(\d+)(?:\s*[-–]\s*(\d+))?\s*页】"
)
_CITE_LOOSE = re.compile(
    r"【来源】\s*([^\n]+?)\s*p\.?\s*(\d+)(?:\s*[-–]\s*(\d+))?",
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------


def _safe_read(path: str) -> str:
    """读取文件内容，失败返回空字符串。"""
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except Exception:
        return ""


def _locate_file(base_dir: str, filename: str) -> str:
    """在 base_dir 及常见子目录中查找文件，返回完整路径或空字符串。"""
    for sub in ["", "answer", "answer_dir"]:
        candidate = os.path.join(base_dir, sub, filename) if sub else os.path.join(base_dir, filename)
        if os.path.isfile(candidate):
            return candidate
    return ""


def _extract_section(text: str, start_hdr: str, end_hdrs: List[str]) -> str:
    """从 text 中提取 start_hdr 开始、end_hdrs 之一结束的段落。"""
    idx = text.find(start_hdr)
    if idx == -1:
        return ""
    tail = idx + len(start_hdr)
    end = len(text)
    for eh in end_hdrs:
        pos = text.find(eh, tail)
        if pos != -1 and pos < end:
            end = pos
    return text[idx:end]


def _count_md_tables(md: str) -> Tuple[int, int]:
    """统计 Markdown 表格数量和最大行数。"""
    lines = md.splitlines()
    table_count = 0
    max_rows = 0
    i = 0
    while i < len(lines) - 1:
        if "|" in lines[i] and re.search(r"\|\s*-{2,}", lines[i + 1]):
            table_count += 1
            row_count = 0
            j = i + 2
            while j < len(lines) and "|" in lines[j] and lines[j].strip():
                row_count += 1
                j += 1
            max_rows = max(max_rows, row_count)
            i = j
        else:
            i += 1
    return table_count, max_rows


def _check_mindmap_depth(md: str) -> bool:
    """检查思维导图是否达到 4 层以上深度。"""
    # 编号形式 1.2.3.4
    if re.search(r"\b\d+(?:\.\d+){3,}\b", md):
        return True
    # 缩进形式 >= 3 层（6+ 空格缩进 + bullet）
    for line in md.splitlines():
        if re.match(r"^\s{6,}[-*+]\s+\S", line):
            return True
        # 或者用 markdown heading 嵌套达到 4 层
        if re.match(r"^#{4,}\s+\S", line):
            return True
    return False


def _collect_citations(text: str) -> Tuple[int, int, Set[str]]:
    """收集引用信息，返回 (严格引用数, 宽松引用数, 被引用的 PDF 集合)。"""
    strict_matches = _CITE_STRICT.findall(text)
    loose_matches = _CITE_LOOSE.findall(text)
    cited: Set[str] = set()
    for m in strict_matches:
        raw_name = m[0].strip()
        for pdf in PDF_FILES:
            if pdf in raw_name or pdf.replace(".pdf", "") in raw_name:
                cited.add(pdf)
    for m in loose_matches:
        blob = m[0]
        for pdf in PDF_FILES:
            if pdf in blob or pdf.replace(".pdf", "") in blob:
                cited.add(pdf)
    return len(strict_matches), len(loose_matches), cited


# ---------------------------------------------------------------------------
# LLM-as-Judge 工具
# ---------------------------------------------------------------------------


def _load_env(answer_dir: str) -> Dict[str, str]:
    """从 answer_dir 及 query 根目录加载 .env 配置。"""
    values: Dict[str, str] = {}
    search_dirs = [answer_dir, os.path.join(os.path.dirname(__file__), "..")]
    for d in search_dirs:
        env_file = os.path.join(d, ".env")
        if not os.path.exists(env_file):
            continue
        with open(env_file, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k = k.strip()
                if k not in values:
                    values[k] = v.strip().strip("'\"")
    return values


def _text_eval_config(answer_dir: str) -> Dict[str, str]:
    env = _load_env(answer_dir)

    def g(key: str, fallback: str = "") -> str:
        return os.environ.get(key) or env.get(key) or fallback

    return {
        "api_key": g("EVAL_TEXT_API_KEY", g("ANTHROPIC_API_KEY")),
        "api_base": g("EVAL_TEXT_API_BASE_URL", g("ANTHROPIC_BASE_URL")),
        "model": g("EVAL_TEXT_MODEL", "openai/gpt-5.2"),
    }


def _call_llm(prompt: str, cfg: Dict[str, str]) -> str:
    """调用 LLM 进行评估，返回原始回复字符串。"""
    if not openai or not cfg.get("api_key"):
        return ""
    try:
        base = cfg["api_base"].rstrip("/")
        if not base.endswith("/v1"):
            base += "/v1"
        client = openai.OpenAI(api_key=cfg["api_key"], base_url=base)
        resp = client.chat.completions.create(
            model=cfg["model"],
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2048,
            temperature=0,
        )
        return resp.choices[0].message.content.strip()
    except Exception as exc:
        print(f"[RUBRIC] LLM 调用失败: {exc}")
        return ""


# ===================================================================
# 维度一：文件交付 (10 分)
# ===================================================================


def _dim1_file_delivery(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    detail: Dict[str, Any] = {}
    score = 0

    for fname, pts in [("study_notes.md", 5), ("mock_exam.md", 5)]:
        path = _locate_file(answer_dir, fname)
        if path:
            sz = os.path.getsize(path)
            if sz >= 500:
                score += pts
                detail[fname] = f"{pts}/{pts} — 存在 ({sz} 字节)"
            elif sz > 0:
                partial = max(1, pts // 2)
                score += partial
                detail[fname] = f"{partial}/{pts} — 存在但过短 ({sz} 字节)"
            else:
                detail[fname] = f"0/{pts} — 文件为空"
        else:
            detail[fname] = f"0/{pts} — 缺失"

    return score, detail


# ===================================================================
# 维度二：复习笔记结构 (20 分)
# ===================================================================


def _dim2_notes_structure(notes: str) -> Tuple[int, Dict[str, Any]]:
    detail: Dict[str, Any] = {}
    score = 0

    # 2a 必要标题 (8 分)
    headers_spec = [
        ("# 走进极地 期末复习笔记", 2),
        ("## 0. 使用说明", 1),
        ("## 1. 全课程知识结构图（文本思维导图）", 2),
        ("## 2. 逐课件总结（必须覆盖全部课件）", 2),
        ("## 3. 高频概念对照表（≥1个表）", 1),
    ]
    hdr_pts = 0
    hdr_info: Dict[str, str] = {}
    for hdr, pts in headers_spec:
        if hdr in notes:
            hdr_pts += pts
            hdr_info[hdr] = f"+{pts}"
        else:
            hdr_info[hdr] = "缺失"
    score += hdr_pts
    detail["标题检查"] = f"{hdr_pts}/8"
    detail["标题明细"] = hdr_info

    # 2b 思维导图深度 (6 分)
    mm_sec = _extract_section(
        notes,
        "## 1. 全课程知识结构图（文本思维导图）",
        ["## 2. 逐课件总结（必须覆盖全部课件）"],
    )
    mm_deep = _check_mindmap_depth(mm_sec)
    mm_len = len(mm_sec.strip())
    if mm_deep and mm_len >= 300:
        mm_pts = 6
    elif mm_deep:
        mm_pts = 4
    elif mm_len >= 100:
        mm_pts = 2
    else:
        mm_pts = 0
    score += mm_pts
    detail["思维导图"] = f"{mm_pts}/6 (深度{'达标' if mm_deep else '不足'}, {mm_len} 字符)"

    # 2c 高频概念对照表 (6 分)
    tbl_sec = _extract_section(notes, "## 3. 高频概念对照表（≥1个表）", [])
    tbl_cnt, tbl_max_rows = _count_md_tables(tbl_sec)
    if tbl_cnt >= 1 and tbl_max_rows >= 8:
        tbl_pts = 6
    elif tbl_cnt >= 1 and tbl_max_rows >= 4:
        tbl_pts = 4
    elif tbl_cnt >= 1:
        tbl_pts = 2
    else:
        tbl_pts = 0
    score += tbl_pts
    detail["对照表"] = f"{tbl_pts}/6 ({tbl_cnt} 个表, 最大 {tbl_max_rows} 行)"

    return score, detail


# ===================================================================
# 维度三：课件覆盖度 (15 分)
# ===================================================================


def _dim3_pdf_coverage(notes: str) -> Tuple[int, Dict[str, Any]]:
    detail: Dict[str, Any] = {}

    sec2 = _extract_section(
        notes,
        "## 2. 逐课件总结（必须覆盖全部课件）",
        ["## 3. 高频概念对照表（≥1个表）"],
    )
    search_in = sec2 if sec2 else notes  # fallback to entire notes

    covered: List[str] = []
    missing: List[str] = []
    for pdf in PDF_FILES:
        name_bare = pdf.replace(".pdf", "")
        if pdf in search_in or name_bare in search_in:
            covered.append(pdf)
        else:
            missing.append(pdf)

    ratio = len(covered) / max(1, len(PDF_FILES))
    pts = int(15 * ratio)
    detail["覆盖"] = f"{len(covered)}/{len(PDF_FILES)}"
    if missing:
        detail["缺失课件"] = missing
    detail["得分"] = f"{pts}/15"
    return pts, detail


# ===================================================================
# 维度四：模拟试卷结构 (25 分)
# ===================================================================


def _count_q(section: str) -> int:
    """统计 ### Q<编号> 形式的题目数量。"""
    return len(re.findall(r"^###\s*Q\d+", section, flags=re.MULTILINE))


def _validate_mcq_fields(section: str) -> Tuple[int, List[str]]:
    """校验选择题字段完整性，返回 (合格数, 错误列表)。"""
    parts = re.split(r"^###\s*(Q\d+)\s*$", section, flags=re.MULTILINE)
    ok = 0
    errs: List[str] = []
    for i in range(1, len(parts), 2):
        qid = parts[i]
        body = parts[i + 1] if i + 1 < len(parts) else ""
        has_opts = all(
            re.search(rf"^{opt}\.\s+.+", body, flags=re.MULTILINE)
            for opt in ("A", "B", "C", "D")
        )
        has_ans = "【答案】" in body
        has_exp = "【解析】" in body
        has_src = "【来源】" in body or "【来源：" in body or "【来源:" in body
        if has_opts and has_ans and has_exp and has_src:
            ok += 1
        else:
            errs.append(f"{qid}: 选项={has_opts} 答案={has_ans} 解析={has_exp} 来源={has_src}")
    return ok, errs


def _validate_short_fields(section: str) -> Tuple[int, List[str]]:
    """校验简答题字段完整性。"""
    parts = re.split(r"^###\s*(Q\d+)\s*$", section, flags=re.MULTILINE)
    ok = 0
    errs: List[str] = []
    for i in range(1, len(parts), 2):
        qid = parts[i]
        body = parts[i + 1] if i + 1 < len(parts) else ""
        has_ref = "【参考答案】" in body
        has_pts = "【评分点】" in body
        has_src = "【来源】" in body or "【来源：" in body or "【来源:" in body
        if has_ref and has_pts and has_src:
            ok += 1
        else:
            errs.append(f"{qid}: 参考答案={has_ref} 评分点={has_pts} 来源={has_src}")
    return ok, errs


def _validate_essay_fields(section: str) -> Tuple[int, List[str]]:
    """校验论述题字段完整性，要求引用 >= 2 份不同课件。"""
    parts = re.split(r"^###\s*(Q\d+)\s*$", section, flags=re.MULTILINE)
    ok = 0
    errs: List[str] = []
    for i in range(1, len(parts), 2):
        qid = parts[i]
        body = parts[i + 1] if i + 1 < len(parts) else ""
        has_ref = "【参考答案】" in body
        has_rub = "【评分Rubric】" in body or "【评分 Rubric】" in body or "【评分rubric】" in body.lower()
        has_src = "【来源】" in body or "【来源：" in body or "【来源:" in body
        # 需要引用至少 2 份不同课件
        cited_pdfs: Set[str] = set()
        for pdf in PDF_FILES:
            if pdf in body or pdf.replace(".pdf", "") in body:
                cited_pdfs.add(pdf)
        has_2pdf = len(cited_pdfs) >= 2
        if has_ref and has_rub and has_src and has_2pdf:
            ok += 1
        else:
            errs.append(
                f"{qid}: 参考答案={has_ref} Rubric={has_rub} 来源={has_src} ≥2课件={has_2pdf}"
            )
    return ok, errs


def _dim4_exam_structure(exam: str) -> Tuple[int, Dict[str, Any]]:
    detail: Dict[str, Any] = {}
    score = 0

    # 4a 试卷标题 (5 分)
    exam_hdrs = [
        "# 走进极地 期末模拟试卷",
        "## 0. 说明",
        "## 1. 单项选择题（20题×2.5分=50分）",
        "## 2. 简答题（6题×5分=30分）",
        "## 3. 论述题（2题×10分=20分）",
    ]
    hdr_hit = sum(1 for h in exam_hdrs if h in exam)
    hdr_pts = hdr_hit  # 每个 1 分，共 5
    score += hdr_pts
    detail["试卷标题"] = f"{hdr_pts}/5 ({hdr_hit}/{len(exam_hdrs)} 命中)"

    # 4b 题目数量 (9 分)
    mcq_sec = _extract_section(
        exam,
        "## 1. 单项选择题（20题×2.5分=50分）",
        ["## 2. 简答题（6题×5分=30分）"],
    )
    short_sec = _extract_section(
        exam,
        "## 2. 简答题（6题×5分=30分）",
        ["## 3. 论述题（2题×10分=20分）"],
    )
    essay_sec = _extract_section(exam, "## 3. 论述题（2题×10分=20分）", [])

    mcq_n = _count_q(mcq_sec)
    short_n = _count_q(short_sec)
    essay_n = _count_q(essay_sec)

    cnt_pts = 0
    if mcq_n >= 20:
        cnt_pts += 3
    elif mcq_n >= 15:
        cnt_pts += 2
    elif mcq_n >= 10:
        cnt_pts += 1
    if short_n >= 6:
        cnt_pts += 3
    elif short_n >= 4:
        cnt_pts += 2
    elif short_n >= 2:
        cnt_pts += 1
    if essay_n >= 2:
        cnt_pts += 3
    elif essay_n >= 1:
        cnt_pts += 1
    score += cnt_pts
    detail["题目数量"] = f"{cnt_pts}/9 (选择={mcq_n}/20 简答={short_n}/6 论述={essay_n}/2)"

    # 4c 字段完整性 (11 分: 选择 5 + 简答 3 + 论述 3)
    field_pts = 0

    mcq_ok, mcq_errs = _validate_mcq_fields(mcq_sec)
    mcq_field_pts = int(5 * mcq_ok / max(1, mcq_n)) if mcq_n > 0 else 0
    field_pts += mcq_field_pts
    detail["选择题字段"] = f"{mcq_field_pts}/5 ({mcq_ok}/{mcq_n} 合格)"

    short_ok, short_errs = _validate_short_fields(short_sec)
    short_field_pts = int(3 * short_ok / max(1, short_n)) if short_n > 0 else 0
    field_pts += short_field_pts
    detail["简答题字段"] = f"{short_field_pts}/3 ({short_ok}/{short_n} 合格)"

    essay_ok, essay_errs = _validate_essay_fields(essay_sec)
    essay_field_pts = int(3 * essay_ok / max(1, essay_n)) if essay_n > 0 else 0
    field_pts += essay_field_pts
    detail["论述题字段"] = f"{essay_field_pts}/3 ({essay_ok}/{essay_n} 合格)"

    score += field_pts
    detail["字段得分"] = f"{field_pts}/11"

    # 收集前几条错误供报告
    all_errs = (
        [f"MCQ: {e}" for e in mcq_errs[:3]]
        + [f"Short: {e}" for e in short_errs[:3]]
        + [f"Essay: {e}" for e in essay_errs[:3]]
    )
    if all_errs:
        detail["字段问题"] = all_errs

    return score, detail


# ===================================================================
# 维度五：引用规范 (15 分)
# ===================================================================


def _dim5_citations(notes: str, exam: str) -> Tuple[int, Dict[str, Any]]:
    detail: Dict[str, Any] = {}
    combined = notes + "\n" + exam

    strict_n, loose_n, cited_pdfs = _collect_citations(combined)
    total_n = strict_n + loose_n
    score = 0

    # 5a 引用数量 (8 分)
    if total_n >= 50:
        qty_pts = 8
    elif total_n >= 30:
        qty_pts = 6
    elif total_n >= 15:
        qty_pts = 4
    elif total_n >= 5:
        qty_pts = 2
    else:
        qty_pts = 0
    score += qty_pts

    # 5b 格式奖励——严格引用 (4 分)
    if strict_n >= 20:
        fmt_pts = 4
    elif strict_n >= 10:
        fmt_pts = 3
    elif strict_n >= 5:
        fmt_pts = 2
    elif strict_n >= 1:
        fmt_pts = 1
    else:
        fmt_pts = 0
    score += fmt_pts

    # 5c 引用 PDF 覆盖 (3 分)
    if len(cited_pdfs) >= 10:
        cov_pts = 3
    elif len(cited_pdfs) >= 7:
        cov_pts = 2
    elif len(cited_pdfs) >= 4:
        cov_pts = 1
    else:
        cov_pts = 0
    score += cov_pts

    detail["引用总数"] = f"{total_n} (严格={strict_n} 宽松={loose_n})"
    detail["数量得分"] = f"{qty_pts}/8"
    detail["格式得分"] = f"{fmt_pts}/4"
    detail["覆盖PDF"] = f"{len(cited_pdfs)}/{len(PDF_FILES)} → {cov_pts}/3"
    detail["总得分"] = f"{score}/15"

    return score, detail


# ===================================================================
# 维度六：内容质量 — LLM-as-Judge (15 分)
# ===================================================================

_LLM_EVAL_PROMPT = """\
你是一位严格的学术内容评估专家。请评估以下《走进极地》课程复习材料的质量。

## 背景
学生需要基于 13 份课程 PDF 课件生成系统复习笔记和模拟试卷，
课程涵盖极地基础概念、海冰物理、冰盖冰架、南北极快速变化、极地遥感监测、极地资源与治理。

## 复习笔记 (节选前 3000 字符):
{notes_excerpt}

## 模拟试卷 (节选前 3000 字符):
{exam_excerpt}

## 评分维度 (请给整数分，并附简短理由)

**维度A: 笔记内容深度** (0-5 分)
- 5: 各课件核心概念均有实质性总结，知识结构清晰完整
- 3-4: 大部分课件有涉及，但部分内容流于泛泛
- 1-2: 覆盖面窄或内容浅薄
- 0: 基本无实质内容

**维度B: 试卷题目质量** (0-5 分)
- 5: 题目紧贴课程内容，答案解析详实有推理链条，选项设置合理
- 3-4: 题目基本合理但解析不够深入
- 1-2: 部分题目偏离课程或解析缺失
- 0: 题目质量极差

**维度C: 整体规范性** (0-5 分)
- 5: 格式统一、表述专业、无编造嫌疑
- 3-4: 格式大致规范，偶有不一致
- 1-2: 格式混乱或有明显编造嫌疑
- 0: 严重不规范

请严格按以下 JSON 格式返回 (不要添加其他内容):
```json
{{
  "notes_depth": {{"score": 0, "reason": "..."}},
  "exam_quality": {{"score": 0, "reason": "..."}},
  "overall_norm": {{"score": 0, "reason": "..."}},
  "total": 0
}}
```"""


def _dim6_content_quality(
    notes: str, exam: str, answer_dir: str
) -> Tuple[int, Dict[str, Any]]:
    detail: Dict[str, Any] = {}

    cfg = _text_eval_config(answer_dir)
    prompt = _LLM_EVAL_PROMPT.format(
        notes_excerpt=notes[:3000],
        exam_excerpt=exam[:3000],
    )
    raw = _call_llm(prompt, cfg)

    if not raw:
        # 降级：基于长度的保守评分
        fb = 0
        if len(notes) >= 3000:
            fb += 3
        elif len(notes) >= 1000:
            fb += 2
        if len(exam) >= 5000:
            fb += 3
        elif len(exam) >= 2000:
            fb += 2
        # 完整性惩罚
        lower_all = (notes + exam).lower()
        for bad in ["维基", "wikipedia", "google", "百度", "bing"]:
            if bad in lower_all:
                fb = max(0, fb - 1)
        fb = min(fb, 8)
        detail["模式"] = "LLM 不可用，降级评估"
        detail["得分"] = f"{fb}/15"
        return fb, detail

    # 解析 LLM 返回
    try:
        cleaned = raw
        if "```json" in cleaned:
            cleaned = cleaned.split("```json")[1].split("```")[0].strip()
        elif "```" in cleaned:
            cleaned = cleaned.split("```")[1].split("```")[0].strip()
        result = json.loads(cleaned)

        s_a = max(0, min(5, int(result.get("notes_depth", {}).get("score", 0))))
        s_b = max(0, min(5, int(result.get("exam_quality", {}).get("score", 0))))
        s_c = max(0, min(5, int(result.get("overall_norm", {}).get("score", 0))))
        total = s_a + s_b + s_c

        detail["笔记深度"] = f"{s_a}/5 — {result.get('notes_depth', {}).get('reason', '')}"
        detail["试卷质量"] = f"{s_b}/5 — {result.get('exam_quality', {}).get('reason', '')}"
        detail["规范性"] = f"{s_c}/5 — {result.get('overall_norm', {}).get('reason', '')}"
        detail["得分"] = f"{total}/15"
        return total, detail
    except Exception as exc:
        detail["解析错误"] = str(exc)
        detail["原始回复"] = raw[:300]
        # 保守给中间分
        return 5, detail


# ===================================================================
# 主入口
# ===================================================================


def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    评估 agent 的输出。

    Args:
        answer_dir: agent 输出目录的绝对路径

    Returns:
        (score, report) — score 0-100, report 含详细评估信息
    """
    report: Dict[str, Any] = {"维度": {}, "总分": 0}

    # 定位文件
    notes_path = _locate_file(answer_dir, "study_notes.md")
    exam_path = _locate_file(answer_dir, "mock_exam.md")
    notes = _safe_read(notes_path) if notes_path else ""
    exam = _safe_read(exam_path) if exam_path else ""

    # 维度 1: 文件交付 (10)
    s1, d1 = _dim1_file_delivery(answer_dir)
    report["维度"]["一、文件交付 (10分)"] = d1

    if not notes and not exam:
        report["总分"] = s1
        return s1, report

    # 维度 2: 复习笔记结构 (20)
    s2, d2 = _dim2_notes_structure(notes)
    report["维度"]["二、复习笔记结构 (20分)"] = d2

    # 维度 3: 课件覆盖度 (15)
    s3, d3 = _dim3_pdf_coverage(notes)
    report["维度"]["三、课件覆盖度 (15分)"] = d3

    # 维度 4: 模拟试卷结构 (25)
    s4, d4 = _dim4_exam_structure(exam)
    report["维度"]["四、模拟试卷结构 (25分)"] = d4

    # 维度 5: 引用规范 (15)
    s5, d5 = _dim5_citations(notes, exam)
    report["维度"]["五、引用规范 (15分)"] = d5

    # 维度 6: 内容质量 LLM (15)
    s6, d6 = _dim6_content_quality(notes, exam, answer_dir)
    report["维度"]["六、内容质量 (15分)"] = d6

    total = max(0, min(100, s1 + s2 + s3 + s4 + s5 + s6))
    report["总分"] = total
    report["分项"] = {
        "文件交付": f"{s1}/10",
        "笔记结构": f"{s2}/20",
        "课件覆盖": f"{s3}/15",
        "试卷结构": f"{s4}/25",
        "引用规范": f"{s5}/15",
        "内容质量": f"{s6}/15",
    }

    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """打印格式化的评分报告。"""
    print("=" * 60)
    print("走进极地课程复习与模拟试卷 — 评分报告")
    print("=" * 60)
    print(f"\n总分: {score}/100\n")

    items = report.get("分项", {})
    if items:
        print("分项得分:")
        for k, v in items.items():
            print(f"  {k}: {v}")
        print()

    for dim_name, dim_detail in report.get("维度", {}).items():
        print(f"--- {dim_name} ---")
        if isinstance(dim_detail, dict):
            for k, v in dim_detail.items():
                if isinstance(v, (list, dict)):
                    print(f"  {k}: {json.dumps(v, ensure_ascii=False, indent=4)[:400]}")
                else:
                    print(f"  {k}: {v}")
        print()

    print("=" * 60)


# ===================================================================
# CLI 入口
# ===================================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        test_dir = sys.argv[1]
    else:
        test_dir = os.path.join(os.path.dirname(__file__), "..", "gpt-5", "attempt_1")

    if os.path.exists(test_dir):
        print(f"评估目录: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"目录不存在: {test_dir}")
    sys.exit(0)
