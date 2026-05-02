"""
人工智能专业培养计划生成与排程 — 评分 rubric (从零重写)

总分 100 分，分 5 个维度:
  一、文件交付与格式 (15 分)
  二、课程覆盖 (30 分)
  三、排课逻辑 (20 分)
  四、实践环节与通识教育 (15 分)
  五、内容质量 — LLM-as-Judge (20 分)
"""

import os
import re
import json
from typing import Tuple, Dict, Any, List, Optional

try:
    import openai
except ImportError:
    openai = None

# ─── 路径常量 ───
EVAL_DIR = os.path.dirname(os.path.abspath(__file__))
QUERY_ROOT = os.path.dirname(EVAL_DIR)

# ─── 环境与 LLM 配置 ───

def _load_env(answer_dir: str) -> dict:
    """从 .env 文件加载环境变量。"""
    vals = {}
    for d in [answer_dir, QUERY_ROOT]:
        p = os.path.join(d, ".env")
        if not os.path.isfile(p):
            continue
        with open(p, "r") as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k, v = k.strip(), v.strip().strip("'\"")
                if k and k not in vals:
                    vals[k] = v
    return vals


def _llm_config(answer_dir: str) -> dict:
    env = _load_env(answer_dir)
    def g(key, fallback=""):
        return os.environ.get(key) or env.get(key) or fallback
    return {
        "api_key": g("EVAL_TEXT_API_KEY", g("ANTHROPIC_API_KEY")),
        "api_base": g("EVAL_TEXT_API_BASE_URL", g("ANTHROPIC_BASE_URL")),
        "model": g("EVAL_TEXT_MODEL", "openai/gpt-5.2"),
    }


def _call_llm(prompt: str, cfg: dict) -> str:
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


# ─── 文件读取与解析 ───

def _read_file(path: str) -> str:
    for enc in ("utf-8", "gbk", "gb18030", "gb2312", "latin-1"):
        try:
            with open(path, "r", encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, LookupError):
            continue
    return ""


def _find_schedule_file(answer_dir: str) -> Optional[str]:
    """在 answer_dir 中找到最合适的课程表 .txt 文件。"""
    if not os.path.isdir(answer_dir):
        return None
    skip = {"readme.txt"}
    candidates = []
    for fn in os.listdir(answer_dir):
        if fn.lower().endswith(".txt") and fn.lower() not in skip:
            fp = os.path.join(answer_dir, fn)
            content = _read_file(fp)
            if "\t" in content:
                nlines = len(content.strip().split("\n"))
                candidates.append((fn, nlines))
    if not candidates:
        # 回退: 任何 .txt
        for fn in os.listdir(answer_dir):
            if fn.lower().endswith(".txt") and fn.lower() not in skip:
                return fn
        return None
    candidates.sort(key=lambda x: -x[1])
    return candidates[0][0]


def _parse_tsv(text: str) -> Tuple[List[str], List[List[str]]]:
    """解析 TSV 文本为 (header_cols, data_rows)。"""
    lines = [l.rstrip("\r") for l in text.strip().split("\n") if l.strip()]
    if not lines:
        return [], []
    header = lines[0].split("\t")
    rows = []
    for line in lines[1:]:
        cols = line.split("\t")
        if any(c.strip() for c in cols):
            rows.append(cols)
    return header, rows


def _col_index(header: List[str], keywords: List[str]) -> Optional[int]:
    """在 header 中找包含关键词的列索引。"""
    for i, h in enumerate(header):
        for kw in keywords:
            if kw in h.strip():
                return i
    return None


def _extract_names(rows: List[List[str]], header: List[str]) -> List[str]:
    idx = _col_index(header, ["课程名称", "课程"])
    if idx is None:
        # 启发式: 如果第一列像学期, 用第二列
        if rows and rows[0] and re.match(r"(第?\d|[一二三四])", rows[0][0].strip()):
            idx = 1 if len(rows[0]) > 1 else 0
        else:
            idx = 0
    return [r[idx].strip() for r in rows if idx < len(r)]


def _extract_credits(rows: List[List[str]], header: List[str]) -> List[float]:
    idx = _col_index(header, ["学分"])
    if idx is None:
        return [0.0] * len(rows)
    result = []
    for r in rows:
        try:
            result.append(float(r[idx].strip()) if idx < len(r) else 0.0)
        except (ValueError, TypeError):
            result.append(0.0)
    return result


def _extract_semesters(rows: List[List[str]], header: List[str]) -> List[str]:
    """提取每行的学期信息(原始字符串)。"""
    idx = _col_index(header, ["学期", "学年"])
    if idx is not None:
        return [r[idx].strip() if idx < len(r) else "" for r in rows]
    # 尝试组合 "建议修读学年" + "建议修读学期"
    y_idx = _col_index(header, ["修读学年", "学年"])
    t_idx = _col_index(header, ["修读学期"])
    if y_idx is not None and t_idx is not None:
        sems = []
        for r in rows:
            y = r[y_idx].strip() if y_idx < len(r) else ""
            t = r[t_idx].strip() if t_idx < len(r) else ""
            sems.append(f"{y}-{t}")
        return sems
    if rows and rows[0] and re.match(r"(第?\d|[一二三四])", rows[0][0].strip()):
        return [r[0].strip() if r else "" for r in rows]
    return [""] * len(rows)


def _extract_category(rows: List[List[str]], header: List[str]) -> List[str]:
    """提取课程类别/性质列。"""
    idx = _col_index(header, ["类别", "课程性质", "性质", "类型"])
    if idx is None:
        return [""] * len(rows)
    return [r[idx].strip() if idx < len(r) else "" for r in rows]


CN_MAP = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8}


def _sem_to_order(raw: str) -> Optional[int]:
    """将学期字符串转成序号 (1=大一上, 2=大一下, 3=大二上, ...)。"""
    raw = raw.strip()
    # "第N学期"
    m = re.match(r"第(\d+)学期", raw)
    if m:
        return int(m.group(1))
    # "X-Y" or "X_Y" 其中 X 是年级 (中文或数字), Y 是学期
    m = re.match(r"([一二三四五六七八\d])\s*[-—_]\s*(\d+)", raw)
    if m:
        y_str, t = m.group(1), int(m.group(2))
        y = CN_MAP.get(y_str)
        if y is None:
            try:
                y = int(y_str)
            except ValueError:
                return None
        return (y - 1) * 2 + t  # 假设每年2个学期
    # 纯数字
    m = re.match(r"(\d+)", raw)
    if m:
        return int(m.group(1))
    return None


def _contains_any(text: str, keywords: List[str]) -> bool:
    t = text.lower()
    return any(kw.lower() in t for kw in keywords)


# ═════════════════════════════════════════════════════════════════════════════
# 一、文件交付与格式 (15 分)
# ═════════════════════════════════════════════════════════════════════════════

def _dim1_file_format(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details = {}
    deductions = []

    all_files = os.listdir(answer_dir) if os.path.isdir(answer_dir) else []
    txt_files = [f for f in all_files if f.lower().endswith(".txt") and f.lower() != "readme.txt"]
    py_files = [f for f in all_files if f.endswith(".py")]

    # 1a. .txt 结果文件存在且有实质内容 (4 分)
    schedule_fn = _find_schedule_file(answer_dir)
    if schedule_fn:
        content = _read_file(os.path.join(answer_dir, schedule_fn))
        header, rows = _parse_tsv(content)
        if rows and len(rows) >= 5:
            score += 4
            details["结果文件"] = f"4/4 — {schedule_fn}, {len(rows)} 行"
        else:
            score += 1
            details["结果文件"] = f"1/4 — 文件存在但数据不足 ({len(rows)} 行)"
            deductions.append("结果文件数据行不足")
    else:
        details["结果文件"] = "0/4 — 未找到 .txt 结果文件"
        deductions.append("缺少 .txt 结果文件")

    # 1b. 制表符分隔 (3 分)
    if schedule_fn:
        content = _read_file(os.path.join(answer_dir, schedule_fn))
        tab_count = content.count("\t")
        nlines = len(content.strip().split("\n"))
        if tab_count >= nlines:
            score += 3
            details["制表符"] = f"3/3 — 共 {tab_count} 个 tab"
        elif tab_count > 0:
            score += 1
            details["制表符"] = f"1/3 — tab 数偏少 ({tab_count})"
            deductions.append("部分行未使用制表符分隔")
        else:
            details["制表符"] = "0/3 — 无制表符"
            deductions.append("未使用制表符分隔")
    else:
        details["制表符"] = "0/3 — 无文件"

    # 1c. 表头列结构 (3 分)
    if schedule_fn:
        content = _read_file(os.path.join(answer_dir, schedule_fn))
        header, _ = _parse_tsv(content)
        hset = {h.strip() for h in header}
        has_name = any("课程" in h or "名称" in h for h in hset)
        has_credit = any("学分" in h for h in hset)
        has_semester = any("学期" in h or "学年" in h for h in hset)
        if has_name and has_credit and len(header) >= 4:
            score += 3
            details["表头"] = f"3/3 — {len(header)} 列, 含课程名/学分"
        elif has_name or has_credit:
            score += 1
            details["表头"] = f"1/3 — 列名不完整: {header[:5]}"
            deductions.append("表头缺少关键列")
        else:
            details["表头"] = f"0/3 — 无法识别关键列"
            deductions.append("表头不规范")
    else:
        details["表头"] = "0/3 — 无文件"

    # 1d. Python 脚本存在 (3 分)
    if py_files:
        score += 3
        details["Python 脚本"] = f"3/3 — {', '.join(py_files[:3])}"
    else:
        details["Python 脚本"] = "0/3 — 无 Python 脚本"
        deductions.append("缺少 Python 脚本")

    # 1e. 数据行数充足 (2 分)
    if schedule_fn:
        content = _read_file(os.path.join(answer_dir, schedule_fn))
        _, rows = _parse_tsv(content)
        if len(rows) >= 40:
            score += 2
            details["行数"] = f"2/2 — {len(rows)} 行"
        elif len(rows) >= 15:
            score += 1
            details["行数"] = f"1/2 — {len(rows)} 行 (偏少)"
            deductions.append("课程数偏少")
        else:
            details["行数"] = f"0/2 — {len(rows)} 行 (不足)"
            deductions.append("课程数严重不足")
    else:
        details["行数"] = "0/2 — 无文件"

    return score, {"分数": score, "满分": 15, "详情": details, "扣分原因": deductions}


# ═════════════════════════════════════════════════════════════════════════════
# 二、课程覆盖 (30 分)
# ═════════════════════════════════════════════════════════════════════════════

# 需要覆盖的课程类别, 关键词列表, 权重
COVERAGE_CHECKS = {
    # --- AI 核心 (15 权重) ---
    "机器学习": (["机器学习", "machine learning"], 3),
    "深度学习": (["深度学习", "deep learning", "神经网络"], 3),
    "AI应用(NLP/CV)": (["自然语言处理", "NLP", "计算机视觉", "CV", "图像", "语音"], 3),
    "强化学习/AI导论": (["强化学习", "人工智能导论", "人工智能思维", "AI导论",
                         "人工智能基本原理", "人工智能基础", "人工智能前沿"], 3),
    "AI无关课程(反向)": ([], 3),  # 特殊: 检查无过多非相关课程

    # --- 数学与编程基础 (15 权重) ---
    "微积分/高数": (["微积分", "高等数学", "数学分析", "数学(A"], 3),
    "线性代数": (["线性代数"], 3),
    "概率论与统计": (["概率", "统计", "随机过程", "概率论"], 3),
    "离散数学/最优化": (["离散数学", "最优化", "凸优化", "优化算法"], 3),
    "数据结构/算法": (["数据结构", "算法设计", "算法分析", "算法"], 3),
}


def _dim2_course_coverage(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details = {}
    deductions = []

    fn = _find_schedule_file(answer_dir)
    if not fn:
        return 0, {"分数": 0, "满分": 30, "详情": {"错误": "无文件"}, "扣分原因": ["无结果文件"]}

    content = _read_file(os.path.join(answer_dir, fn))
    header, rows = _parse_tsv(content)
    names = _extract_names(rows, header)
    categories = _extract_category(rows, header)

    total_weight = sum(w for _, w in COVERAGE_CHECKS.values())
    covered_weight = 0

    for cat, (keywords, weight) in COVERAGE_CHECKS.items():
        if cat == "AI无关课程(反向)":
            # 特殊处理: 检查是否包含过多明显不相关的课程
            irrelevant_kw = ["兽医", "天然药物", "插花", "园林", "动物解剖",
                             "护理伦理", "天文", "医学生职业"]
            irrelevant_count = sum(1 for n in names if _contains_any(n, irrelevant_kw))
            ratio = irrelevant_count / len(names) if names else 1.0
            if ratio <= 0.05:
                covered_weight += weight
                details[cat] = f"+{weight} — 无明显不相关课程"
            elif ratio <= 0.15:
                covered_weight += weight // 2
                details[cat] = f"+{weight // 2} — 有 {irrelevant_count} 门疑似不相关课程"
                deductions.append(f"有 {irrelevant_count} 门可能不相关的课程")
            else:
                details[cat] = f"0 — {irrelevant_count}/{len(names)} 门课不相关"
                deductions.append(f"大量非 AI 专业课程 ({irrelevant_count} 门)")
            continue

        found = any(_contains_any(n, keywords) for n in names)
        if found:
            covered_weight += weight
            details[cat] = f"+{weight} — 已覆盖"
        else:
            details[cat] = f"0 — 未找到 (关键词: {', '.join(keywords[:3])})"
            deductions.append(f"缺少 {cat}")

    score = round(30 * covered_weight / total_weight) if total_weight else 0
    details["覆盖率"] = f"{covered_weight}/{total_weight}"
    details["课程总数"] = str(len(names))

    return score, {"分数": score, "满分": 30, "详情": details, "扣分原因": deductions}


# ═════════════════════════════════════════════════════════════════════════════
# 三、排课逻辑 (20 分)
# ═════════════════════════════════════════════════════════════════════════════

def _dim3_scheduling(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details = {}
    deductions = []

    fn = _find_schedule_file(answer_dir)
    if not fn:
        return 0, {"分数": 0, "满分": 20, "详情": {"错误": "无文件"}, "扣分原因": ["无结果文件"]}

    content = _read_file(os.path.join(answer_dir, fn))
    header, rows = _parse_tsv(content)
    if not rows:
        return 0, {"分数": 0, "满分": 20, "详情": {"错误": "无数据行"}, "扣分原因": ["无课程数据"]}

    names = _extract_names(rows, header)
    credits = _extract_credits(rows, header)
    sem_raw = _extract_semesters(rows, header)

    # 解析每行的学期序号
    orders = [_sem_to_order(s) for s in sem_raw]

    # 按学期序号分组
    sem_credits: Dict[int, float] = {}
    for i, order in enumerate(orders):
        if order is None:
            continue
        c = credits[i] if i < len(credits) else 0.0
        sem_credits[order] = sem_credits.get(order, 0.0) + c

    num_semesters = len(sem_credits)

    # 3a. 学期跨度 (5 分) — 至少覆盖 6 个学期
    if num_semesters >= 7:
        score += 5
        details["学期跨度"] = f"5/5 — {num_semesters} 个学期"
    elif num_semesters >= 5:
        score += 3
        details["学期跨度"] = f"3/5 — {num_semesters} 个学期"
        deductions.append(f"学期数偏少 ({num_semesters})")
    elif num_semesters >= 3:
        score += 1
        details["学期跨度"] = f"1/5 — {num_semesters} 个学期"
        deductions.append("学期分布不足")
    else:
        details["学期跨度"] = f"0/5 — {num_semesters} 个学期"
        deductions.append("学期信息严重不足")

    # 3b. 每学期学分分布 (5 分)
    if sem_credits:
        reasonable = 0
        for sem, tc in sem_credits.items():
            if sem <= 4:  # 大一大二
                reasonable += 1 if 8 <= tc <= 40 else 0
            elif sem <= 6:  # 大三
                reasonable += 1 if 2 <= tc <= 30 else 0
            else:  # 大四
                reasonable += 1 if 1 <= tc <= 25 else 0
        ratio = reasonable / len(sem_credits)
        if ratio >= 0.7:
            score += 5
            details["学分分布"] = f"5/5 — {reasonable}/{len(sem_credits)} 个学期合理"
        elif ratio >= 0.4:
            score += 3
            details["学分分布"] = f"3/5 — {reasonable}/{len(sem_credits)} 个学期合理"
            deductions.append("部分学期学分不合理")
        else:
            score += 1
            details["学分分布"] = f"1/5 — {reasonable}/{len(sem_credits)} 合理"
            deductions.append("学分分布大面积不合理")
        details["各学期学分"] = {f"第{s}学期": round(tc, 1) for s, tc in sorted(sem_credits.items())}
    else:
        details["学分分布"] = "0/5 — 无学期信息"
        deductions.append("无法解析学分分布")

    # 3c. 总学分 (4 分)
    total_c = sum(credits)
    if 80 <= total_c <= 220:
        score += 4
        details["总学分"] = f"4/4 — {total_c:.1f}"
    elif 50 <= total_c <= 260:
        score += 2
        details["总学分"] = f"2/4 — {total_c:.1f} (偏离合理范围)"
        deductions.append(f"总学分 {total_c:.1f} 偏离常规 80-220 范围")
    else:
        details["总学分"] = f"0/4 — {total_c:.1f} (严重偏离)"
        deductions.append(f"总学分 {total_c:.1f} 严重偏离")

    # 3d. 先修关系 (6 分) — 数学 & 编程 应早于 AI 核心
    math_kw = ["微积分", "高等数学", "数学分析", "线性代数", "概率论", "概率统计",
               "离散数学", "数学(A"]
    prog_kw = ["数据结构", "算法", "程序设计", "Python", "JAVA", "C++"]
    ai_kw = ["机器学习", "深度学习", "强化学习", "自然语言处理", "计算机视觉"]
    thesis_kw = ["毕业设计", "毕业论文"]

    math_orders = []
    prog_orders = []
    ai_orders = []
    thesis_orders = []
    for i, nm in enumerate(names):
        o = orders[i] if i < len(orders) else None
        if o is None:
            continue
        if _contains_any(nm, math_kw):
            math_orders.append(o)
        if _contains_any(nm, prog_kw):
            prog_orders.append(o)
        if _contains_any(nm, ai_kw):
            ai_orders.append(o)
        if _contains_any(nm, thesis_kw):
            thesis_orders.append(o)

    prereq_score = 0
    # 数学/编程平均 < AI 平均
    basis = math_orders + prog_orders
    if basis and ai_orders:
        avg_basis = sum(basis) / len(basis)
        avg_ai = sum(ai_orders) / len(ai_orders)
        if avg_basis < avg_ai:
            prereq_score += 4
            details["数学→AI 先修"] = "4/4 — 基础课平均早于 AI 课"
        elif avg_basis <= avg_ai + 1:
            prereq_score += 2
            details["数学→AI 先修"] = "2/4 — 大致同期"
            deductions.append("数学/编程与 AI 课时间接近")
        else:
            details["数学→AI 先修"] = "0/4 — 基础课偏晚"
            deductions.append("基础课排在 AI 课之后")
    else:
        prereq_score += 1
        details["数学→AI 先修"] = "1/4 — 无法检测 (课程不足)"

    # 毕业设计在后期
    if thesis_orders:
        if min(thesis_orders) >= 7:
            prereq_score += 2
            details["毕设安排"] = "2/2 — 毕设在大四"
        elif min(thesis_orders) >= 5:
            prereq_score += 1
            details["毕设安排"] = "1/2 — 毕设偏早 (第{}学期)".format(min(thesis_orders))
            deductions.append("毕业设计安排偏早")
        else:
            details["毕设安排"] = "0/2 — 毕设过早"
            deductions.append("毕业设计安排过早")
    else:
        details["毕设安排"] = "0/2 — 未包含毕业设计"

    score += prereq_score

    return score, {"分数": score, "满分": 20, "详情": details, "扣分原因": deductions}


# ═════════════════════════════════════════════════════════════════════════════
# 四、实践环节与通识教育 (15 分)
# ═════════════════════════════════════════════════════════════════════════════

def _dim4_practice_general(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details = {}
    deductions = []

    fn = _find_schedule_file(answer_dir)
    if not fn:
        return 0, {"分数": 0, "满分": 15, "详情": {"错误": "无文件"}, "扣分原因": ["无结果文件"]}

    content = _read_file(os.path.join(answer_dir, fn))
    header, rows = _parse_tsv(content)
    names = _extract_names(rows, header)
    categories = _extract_category(rows, header)
    sem_raw = _extract_semesters(rows, header)

    # 4a. 实践环节 (8 分)
    prac_score = 0

    # 独立实验课
    lab_kw = ["实验", "实验课"]
    has_lab = any(_contains_any(n, lab_kw) for n in names)
    if has_lab:
        prac_score += 2
        details["独立实验课"] = "2/2 — 有"
    else:
        details["独立实验课"] = "0/2 — 无独立实验课程"
        deductions.append("缺少独立实验课程")

    # 课程设计/项目实践
    design_kw = ["课程设计", "项目实践", "综合实践", "综合实验", "实训", "工程实践"]
    has_design = any(_contains_any(n, design_kw) for n in names)
    if has_design:
        prac_score += 2
        details["课程设计/项目"] = "2/2 — 有"
    else:
        details["课程设计/项目"] = "0/2 — 无"
        deductions.append("缺少课程设计或项目实践")

    # 实习
    intern_kw = ["实习", "科研实践", "生产实习"]
    has_intern = any(_contains_any(n, intern_kw) for n in names)
    if has_intern:
        prac_score += 2
        details["实习环节"] = "2/2 — 有"
    else:
        details["实习环节"] = "0/2 — 无实习"
        deductions.append("缺少实习环节")

    # 毕业设计
    thesis_kw = ["毕业设计", "毕业论文"]
    has_thesis = any(_contains_any(n, thesis_kw) for n in names)
    if has_thesis:
        prac_score += 2
        details["毕业设计"] = "2/2 — 有"
    else:
        details["毕业设计"] = "0/2 — 无"
        deductions.append("缺少毕业设计")

    score += prac_score

    # 4b. 通识/思政 (7 分)
    ge_score = 0

    # 思政课 (3 分)
    ideo_kw_list = [
        ("思想道德", ["思想道德", "法治"]),
        ("近代史", ["近现代史", "近代史", "中国近代"]),
        ("马克思", ["马克思"]),
        ("毛泽东/中特", ["毛泽东思想", "中国特色社会主义理论"]),
        ("习近平思想", ["习近平"]),
        ("形势与政策", ["形势与政策"]),
    ]
    ideo_found = sum(1 for _, kws in ideo_kw_list if any(_contains_any(n, kws) for n in names))
    if ideo_found >= 5:
        ge_score += 3
        details["思政课"] = f"3/3 — 覆盖 {ideo_found}/{len(ideo_kw_list)}"
    elif ideo_found >= 3:
        ge_score += 2
        details["思政课"] = f"2/3 — 覆盖 {ideo_found}/{len(ideo_kw_list)}"
        deductions.append(f"思政课仅覆盖 {ideo_found}/{len(ideo_kw_list)} 门")
    elif ideo_found >= 1:
        ge_score += 1
        details["思政课"] = f"1/3 — 覆盖 {ideo_found}/{len(ideo_kw_list)}"
        deductions.append("思政课严重不足")
    else:
        details["思政课"] = "0/3 — 无思政课"
        deductions.append("完全缺少思政课")

    # 体育课 (2 分) — 应安排多学期
    pe_kw = ["体育"]
    pe_sems = set()
    for i, n in enumerate(names):
        if _contains_any(n, pe_kw):
            s = sem_raw[i] if i < len(sem_raw) else ""
            o = _sem_to_order(s)
            if o is not None:
                pe_sems.add(o)
    if len(pe_sems) >= 3:
        ge_score += 2
        details["体育课"] = f"2/2 — {len(pe_sems)} 个学期"
    elif len(pe_sems) >= 1:
        ge_score += 1
        details["体育课"] = f"1/2 — {len(pe_sems)} 个学期 (建议4学期)"
        deductions.append(f"体育课仅 {len(pe_sems)} 个学期")
    else:
        if any(_contains_any(n, pe_kw) for n in names):
            ge_score += 1
            details["体育课"] = "1/2 — 有体育课但学期未识别"
        else:
            details["体育课"] = "0/2 — 无体育课"
            deductions.append("缺少体育课")

    # 英语课 (2 分)
    eng_kw = ["英语", "English", "大学英语"]
    has_eng = any(_contains_any(n, eng_kw) for n in names)
    if has_eng:
        ge_score += 2
        details["英语课"] = "2/2 — 有"
    else:
        details["英语课"] = "0/2 — 无英语课"
        deductions.append("缺少英语课")

    score += ge_score

    return score, {"分数": score, "满分": 15, "详情": details, "扣分原因": deductions}


# ═════════════════════════════════════════════════════════════════════════════
# 五、内容质量 — LLM-as-Judge (20 分)
# ═════════════════════════════════════════════════════════════════════════════

_JUDGE_PROMPT = """\
你是一位严格的大学教务专家，正在评估一份「人工智能专业本科培养计划」的质量。

以下是该培养计划的内容（制表符分隔文本）：

```
{text}
```

请从以下维度严格打分（整数），并给出简短理由：

**维度 A：课程体系完整性** (0-7分)
- 7: 涵盖 AI 核心(ML/DL/RL/NLP/CV)、数学基础(高数/线代/概率/离散)、编程基础(数据结构/算法)、实践环节(实验/实习/毕设)、通识(思政/英语/体育)，体系完整
- 4-6: 涵盖大部分但缺少某些重要类别
- 1-3: 明显缺失多个重要课程类别
- 0: 课程体系严重不完整

**维度 B：排课时序合理性** (0-7分)
- 7: 先修关系正确（数学→编程→AI基础→AI应用→毕设），学期学分分布均匀合理
- 4-6: 基本合理但有少量时序问题
- 1-3: 存在明显的时序问题
- 0: 排课时序混乱

**维度 C：专业针对性与质量** (0-6分)
- 6: 课程选择精准、针对 AI 专业特点，无无关课程，体现专业深度
- 3-5: 基本合理但有少量不相关课程
- 1-2: 存在较多不相关课程或专业性不足
- 0: 课程选择与 AI 专业严重不匹配

请严格按以下 JSON 格式回复（不要包含其他内容）：
```json
{{
  "completeness": {{"score": 0, "reason": ""}},
  "scheduling": {{"score": 0, "reason": ""}},
  "relevance": {{"score": 0, "reason": ""}},
  "total": 0,
  "overall_comment": ""
}}
```"""


def _dim5_llm_quality(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details = {}
    deductions = []

    fn = _find_schedule_file(answer_dir)
    if not fn:
        return 0, {"分数": 0, "满分": 20, "详情": {"错误": "无文件"}, "扣分原因": ["无结果文件"]}

    content = _read_file(os.path.join(answer_dir, fn))
    text = content[:8000]

    cfg = _llm_config(answer_dir)
    prompt = _JUDGE_PROMPT.format(text=text)
    raw = _call_llm(prompt, cfg)

    if raw:
        try:
            body = raw
            if "```json" in body:
                body = body.split("```json")[1].split("```")[0].strip()
            elif "```" in body:
                body = body.split("```")[1].split("```")[0].strip()
            result = json.loads(body)

            comp = max(0, min(7, int(result.get("completeness", {}).get("score", 0))))
            sched = max(0, min(7, int(result.get("scheduling", {}).get("score", 0))))
            relev = max(0, min(6, int(result.get("relevance", {}).get("score", 0))))
            score = comp + sched + relev

            details["完整性 (7)"] = f"{comp}/7 — {result.get('completeness', {}).get('reason', '')}"
            details["时序性 (7)"] = f"{sched}/7 — {result.get('scheduling', {}).get('reason', '')}"
            details["针对性 (6)"] = f"{relev}/6 — {result.get('relevance', {}).get('reason', '')}"
            details["总评"] = result.get("overall_comment", "")
            details["模型"] = cfg.get("model", "")
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            print(f"[RUBRIC] LLM 返回解析失败: {exc}")
            details["解析错误"] = str(exc)
            details["原始返回"] = raw[:300]
            score = 8
            details["降级说明"] = "8/20 — LLM 返回解析失败, 给保守分"
    else:
        score = 8
        details["降级说明"] = "8/20 — LLM 不可用, 给保守分"

    return score, {"分数": score, "满分": 20, "详情": details, "扣分原因": deductions}


# ═════════════════════════════════════════════════════════════════════════════
# 主入口
# ═════════════════════════════════════════════════════════════════════════════

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """评估 agent 提交的培养计划。返回 (总分, 报告字典)。"""
    s1, r1 = _dim1_file_format(answer_dir)
    s2, r2 = _dim2_course_coverage(answer_dir)
    s3, r3 = _dim3_scheduling(answer_dir)
    s4, r4 = _dim4_practice_general(answer_dir)
    s5, r5 = _dim5_llm_quality(answer_dir)

    total = s1 + s2 + s3 + s4 + s5

    report = {
        "总分": total,
        "分项得分": {
            "一、文件交付与格式": f"{s1}/15",
            "二、课程覆盖": f"{s2}/30",
            "三、排课逻辑": f"{s3}/20",
            "四、实践与通识": f"{s4}/15",
            "五、内容质量(LLM)": f"{s5}/20",
        },
        "详细报告": {
            "一、文件交付与格式 (15分)": r1,
            "二、课程覆盖 (30分)": r2,
            "三、排课逻辑 (20分)": r3,
            "四、实践与通识 (15分)": r4,
            "五、内容质量 (20分)": r5,
        },
    }

    if total >= 85:
        report["评语"] = "优秀！培养计划全面且排课合理。"
    elif total >= 70:
        report["评语"] = "良好。基本完成但部分维度有改进空间。"
    elif total >= 50:
        report["评语"] = "及格。课程覆盖或排课存在明显不足。"
    elif total >= 30:
        report["评语"] = "部分完成。培养计划不够完善。"
    else:
        report["评语"] = "不及格。任务完成度严重不足。"

    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """打印格式化的评分报告。"""
    print("=" * 70)
    print("人工智能专业培养计划 — 评分报告")
    print("=" * 70)
    print(f"\n总分: {score}/100")

    for k, v in report.get("分项得分", {}).items():
        print(f"  {k}: {v}")

    for section_key, section in report.get("详细报告", {}).items():
        print(f"\n{'─' * 50}")
        print(f"【{section_key}】 {section.get('分数', '?')}/{section.get('满分', '?')}")
        print(f"{'─' * 50}")
        for k, v in section.get("详情", {}).items():
            if isinstance(v, dict):
                print(f"  {k}:")
                for kk, vv in v.items():
                    print(f"    {kk}: {vv}")
            else:
                print(f"  {k}: {v}")
        deds = section.get("扣分原因", [])
        if deds:
            print("  扣分原因:")
            for i, d in enumerate(deds, 1):
                print(f"    {i}. {d}")

    print(f"\n{'=' * 50}")
    print(f"评语: {report.get('评语', '')}")
    print("=" * 70)


if __name__ == "__main__":
    import sys
    test_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(QUERY_ROOT, "gpt-5", "attempt_1")
    if os.path.isdir(test_dir):
        print(f"评估目录: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"目录不存在: {test_dir}")
    sys.exit(0)
