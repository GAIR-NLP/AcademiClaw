"""
化学竞赛试题解答任务 — 评分脚本 (rubric.py)

任务：解答第 36 届中国化学奥林匹克（初赛）试题，产出 answers.md
评分总分：100 分

评分维度：
  一、文件交付与基本格式 (10 分)
      1.1 answers.md 存在且命名正确 (3 分)
      1.2 文件内容非空且长度合理 (2 分)
      1.3 LaTeX 化学式/数学公式使用 (3 分)
      1.4 章节结构与子题编号 (2 分)

  二、内容正确性 — Vision LLM 逐题对照参考答案 (90 分)
      10 道大题 38 个子题，原始满分 100 分，缩放至 90 分
      使用 eval/reference/ 目录下 参考答案1-12.jpg 作为评分依据
"""

import os
import sys
import json
import re
import base64
from typing import Tuple, Dict, Any, List, Optional

try:
    import openai
except ImportError:
    openai = None


# ============================================================================
# 环境与 LLM 配置
# ============================================================================

def _load_env(answer_dir: str) -> dict:
    """从 answer_dir 和 query 根目录加载 .env"""
    values: Dict[str, str] = {}
    root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    for env_dir in [answer_dir, root_dir]:
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


def _get_vision_eval_config(answer_dir: str) -> dict:
    """获取 Vision LLM 评估配置"""
    env = _load_env(answer_dir)

    def g(key: str, default: str = "") -> str:
        return os.environ.get(key) or env.get(key) or default

    return {
        "api_key": g("EVAL_VISION_API_KEY", g("ANTHROPIC_API_KEY")),
        "api_base": g("EVAL_VISION_API_BASE_URL", g("ANTHROPIC_BASE_URL")),
        "model": g("EVAL_VISION_MODEL", "openai/gpt-5.2"),
    }


def _call_vision_llm(prompt: str, image_paths: List[str], config: dict) -> str:
    """调用 Vision LLM，发送文字 + 多张图片"""
    if not openai or not config.get("api_key"):
        return ""
    try:
        base = config["api_base"].rstrip("/")
        if not base.endswith("/v1"):
            base += "/v1"

        content: list = [{"type": "text", "text": prompt}]
        for img_path in image_paths:
            if not os.path.exists(img_path):
                continue
            with open(img_path, "rb") as f:
                img_b64 = base64.b64encode(f.read()).decode("utf-8")
            ext = os.path.splitext(img_path)[1].lower()
            mime = {".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                    ".png": "image/png"}.get(ext, "image/jpeg")
            content.append({
                "type": "image_url",
                "image_url": {"url": f"data:{mime};base64,{img_b64}"},
            })

        client = openai.OpenAI(api_key=config["api_key"], base_url=base)
        resp = client.chat.completions.create(
            model=config["model"],
            messages=[{"role": "user", "content": content}],
            max_tokens=2048,
            temperature=0,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        print(f"[RUBRIC] Vision LLM 调用失败: {e}")
        return ""


# ============================================================================
# 题目与权重映射
# ============================================================================

# 每道题对应的参考答案图片编号（参考答案X.jpg）
PROBLEM_TO_REF_IMAGES: Dict[str, List[int]] = {
    "1": [1],
    "2": [1, 2],
    "3": [2],
    "4": [3],
    "5": [4],
    "6": [5],
    "7": [6],
    "8": [7, 8],
    "9": [8, 9, 10],
    "10": [11, 12],
}

# 各子题权重（原始满分合计 100 分）
SUB_WEIGHTS: Dict[str, Dict[str, int]] = {
    "1":  {"1-1": 2, "1-2": 2, "1-3": 2, "1-4": 2, "1-5": 2},
    "2":  {"2-1": 3, "2-2": 4},
    "3":  {"3-1": 6, "3-2": 1},
    "4":  {"4-1": 2, "4-2": 6},
    "5":  {"5-1": 5, "5-2": 4, "5-3": 3, "5-4": 2},
    "6":  {"6-1": 2, "6-2": 2, "6-3": 3, "6-4": 2},
    "7":  {"7-1": 2, "7-2": 4, "7-3": 3, "7-4-1": 1, "7-4-2": 1},
    "8":  {"8-1-1": 1, "8-1-2": 1, "8-1-3": 1, "8-1-4": 1,
           "8-1-5": 1, "8-2": 4, "8-3": 3},
    "9":  {"9-1": 2, "9-2": 3, "9-3": 4, "9-4": 2},
    "10": {"10-1-1": 1, "10-1-2": 1, "10-2": 2, "10-3": 4, "10-4": 3},
}

PROBLEM_MAX: Dict[str, int] = {k: sum(v.values()) for k, v in SUB_WEIGHTS.items()}


# ============================================================================
# 辅助函数
# ============================================================================

def _find_answers_file(answer_dir: str) -> Optional[str]:
    """在 answer_dir 中寻找 answers.md（或最大的 .md 文件作为回退）"""
    if not os.path.isdir(answer_dir):
        return None
    primary = os.path.join(answer_dir, "answers.md")
    if os.path.isfile(primary):
        return primary
    md_files = sorted(
        [f for f in os.listdir(answer_dir)
         if f.lower().endswith(".md") and not f.startswith(".")],
        key=lambda x: os.path.getsize(os.path.join(answer_dir, x)),
        reverse=True,
    )
    if md_files:
        return os.path.join(answer_dir, md_files[0])
    return None


def _read_text(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


def _extract_problem_text(content: str, prob_num: int) -> str:
    """从 answers.md 中提取第 prob_num 题的文本"""
    # 尝试匹配 "## 第 X 题" 或 "### 第 X 题"
    pattern = rf'#{1,3}\s*第\s*{prob_num}\s*题(.*?)(?=#{1,3}\s*第\s*\d+\s*题|#{1,3}\s*最终|$)'
    m = re.search(pattern, content, re.DOTALL)
    if m:
        return m.group(1).strip()
    # 回退匹配 "第 X 题"
    pattern2 = rf'第\s*{prob_num}\s*题(.*?)(?=第\s*\d+\s*题|$)'
    m2 = re.search(pattern2, content, re.DOTALL)
    if m2:
        return m2.group(1).strip()
    return ""


# ============================================================================
# 维度一：文件交付与基本格式 (10 分)
# ============================================================================

def _eval_file_and_format(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    score = 0
    details: Dict[str, str] = {}

    answers_path = _find_answers_file(answer_dir)

    # 1.1 文件存在 (3 分)
    if not answers_path:
        details["1.1 文件存在"] = "0/3 - 未找到 answers.md 或任何 .md 文件"
        details["1.2 内容长度"] = "0/2 - 无文件"
        details["1.3 LaTeX 使用"] = "0/3 - 无文件"
        details["1.4 章节结构"] = "0/2 - 无文件"
        return 0, {"score": 0, "details": details}

    fname = os.path.basename(answers_path)
    if fname == "answers.md":
        score += 3
        details["1.1 文件存在"] = "3/3 - answers.md 存在"
    else:
        score += 1
        details["1.1 文件存在"] = f"1/3 - 找到 {fname}（非标准文件名）"

    content = _read_text(answers_path)

    # 1.2 内容长度 (2 分)
    clen = len(content)
    if clen >= 2000:
        score += 2
        details["1.2 内容长度"] = f"2/2 - {clen} 字符"
    elif clen >= 500:
        score += 1
        details["1.2 内容长度"] = f"1/2 - {clen} 字符（偏短）"
    else:
        details["1.2 内容长度"] = f"0/2 - {clen} 字符（过短）"

    # 1.3 LaTeX 使用 (3 分)
    latex_pats = [r'\$[^$]+\$', r'\$\$[^$]+\$\$', r'\\ce\{',
                  r'\\frac', r'\\Delta', r'\\mathrm', r'\\text']
    latex_hits = sum(len(re.findall(p, content, re.DOTALL)) for p in latex_pats)
    if latex_hits >= 20:
        score += 3
        details["1.3 LaTeX 使用"] = f"3/3 - 大量使用 LaTeX（{latex_hits} 处）"
    elif latex_hits >= 8:
        score += 2
        details["1.3 LaTeX 使用"] = f"2/3 - 适量使用 LaTeX（{latex_hits} 处）"
    elif latex_hits >= 2:
        score += 1
        details["1.3 LaTeX 使用"] = f"1/3 - 少量使用 LaTeX（{latex_hits} 处）"
    else:
        details["1.3 LaTeX 使用"] = f"0/3 - 几乎未使用 LaTeX（{latex_hits} 处）"

    # 1.4 章节结构 (2 分)
    prob_headers = len(re.findall(r'#{1,3}\s*第\s*\d+\s*题', content))
    sub_labels = len(re.findall(r'\*\*\d+-\d+', content))
    s14 = 0
    if prob_headers >= 8:
        s14 += 1
    if sub_labels >= 10:
        s14 += 1
    score += s14
    details["1.4 章节结构"] = (
        f"{s14}/2 - 大题标题 {prob_headers} 个"
        f"{'(OK)' if prob_headers >= 8 else '(不足)'}, "
        f"子题标签 {sub_labels} 个{'(OK)' if sub_labels >= 10 else '(不足)'}"
    )

    return score, {"score": score, "details": details}


# ============================================================================
# 维度二：内容正确性 — 逐题 Vision LLM 评估 (90 分)
# ============================================================================

def _build_grading_prompt(prob_num: int, student_text: str,
                          sub_weights: Dict[str, int], max_pts: int) -> str:
    """构造单题评分 prompt"""
    sub_desc = ", ".join(f"{k}({v}分)" for k, v in sub_weights.items())
    prompt = (
        f"你是化学竞赛评审专家。请根据附带的参考答案图片，严格评估学生第 {prob_num} 题的答案。\n\n"
        f"该题满分 {max_pts} 分。子题及分值：{sub_desc}\n\n"
        f"【学生答案 — 第 {prob_num} 题】\n"
        f"{student_text[:4000]}\n\n"
        "【评分规则】\n"
        "- 逐子题对照参考答案图片中的标准答案进行评分。\n"
        "- 化学方程式必须配平正确、产物正确才给满分。\n"
        "- 计算题需过程合理且最终数值正确（允许合理的有效数字差异）。\n"
        "- 结构式/构型（R/S、顺反）需正确。\n"
        '- 只写了模板占位（如"解题思路与关键化学原理"）或泛泛而谈不给分。\n'
        "- 部分正确可给部分分。\n\n"
        "请严格返回以下 JSON 格式（不要有其他内容）：\n"
        '{"sub_scores": {'
    )
    items = ", ".join(
        f'"{k}": {{"score": 0, "max": {v}, "reason": ""}}'
        for k, v in sub_weights.items()
    )
    prompt += items + '}, "total": 0, "brief_comment": ""}'
    return prompt


def _parse_llm_score(raw: str, max_pts: int) -> Tuple[int, str]:
    """从 LLM 输出中解析分数和评语"""
    if not raw:
        return 0, "LLM 无输出"
    # 尝试 JSON 解析
    try:
        json_match = re.search(r'\{[\s\S]*\}', raw)
        if json_match:
            obj = json.loads(json_match.group())
            total = int(obj.get("total", 0))
            comment = str(obj.get("brief_comment", ""))[:150]
            return max(0, min(max_pts, total)), comment
    except (json.JSONDecodeError, ValueError, TypeError):
        pass
    # 回退：正则提取 total 字段
    m = re.search(r'"total"\s*:\s*(\d+)', raw)
    if m:
        return max(0, min(max_pts, int(m.group(1)))), "JSON 解析部分失败"
    return 0, "LLM 返回格式无法解析"


def _fallback_heuristic_score(text: str, max_pts: int) -> int:
    """LLM 不可用时的保守启发式评分"""
    if not text:
        return 0
    tlen = len(text)
    has_chem = bool(re.search(r'\\ce\{|→|->|\$.*\\', text))
    has_nums = bool(re.search(r'\d+\.\d+', text))
    chem_terms = len(re.findall(
        r'(?:mol|kJ|eV|pm|cm|g/cm|K\b|atm|Pa|密度|摩尔|焓|自由能|方程|反应|催化|氧化|还原'
        r'|配位|晶胞|空间群|构型|手性|合成)',
        text
    ))
    # 检查是否只是模板占位
    is_template = bool(re.search(
        r'题意与已知条件.*由多模态识别提取|解题思路与关键化学原理|计算与推导.*公式与数值结果',
        text
    ))
    if is_template and tlen < 500:
        return 0

    if tlen > 800 and has_chem and has_nums and chem_terms >= 3:
        return max(1, max_pts // 4)
    elif tlen > 300 and (has_chem or has_nums or chem_terms >= 2):
        return max(1, max_pts // 5)
    elif tlen > 100:
        return max(1, max_pts // 8)
    return 0


def _eval_content(answer_dir: str, content: str) -> Tuple[int, Dict[str, Any]]:
    """逐题评分，原始满分 100 分，缩放至 90 分"""
    config = _get_vision_eval_config(answer_dir)
    ref_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reference")

    raw_total = 0
    per_problem: Dict[str, int] = {}
    details: Dict[str, str] = {}

    for prob_num in range(1, 11):
        pk = str(prob_num)
        max_pts = PROBLEM_MAX[pk]
        subs = SUB_WEIGHTS[pk]

        student_text = _extract_problem_text(content, prob_num)
        if not student_text:
            per_problem[pk] = 0
            details[f"第{prob_num}题"] = f"0/{max_pts} - 未找到该题答案"
            continue

        # 收集参考答案图片路径
        ref_img_ids = PROBLEM_TO_REF_IMAGES[pk]
        ref_paths = []
        for rid in ref_img_ids:
            p = os.path.join(ref_dir, f"参考答案{rid}.jpg")
            if os.path.isfile(p):
                ref_paths.append(p)

        if not ref_paths:
            per_problem[pk] = 0
            details[f"第{prob_num}题"] = f"0/{max_pts} - 参考答案图片缺失"
            continue

        prompt = _build_grading_prompt(prob_num, student_text, subs, max_pts)
        llm_out = _call_vision_llm(prompt, ref_paths, config)

        if llm_out:
            prob_score, comment = _parse_llm_score(llm_out, max_pts)
            per_problem[pk] = prob_score
            details[f"第{prob_num}题"] = f"{prob_score}/{max_pts} - {comment}"
        else:
            prob_score = _fallback_heuristic_score(student_text, max_pts)
            per_problem[pk] = prob_score
            details[f"第{prob_num}题"] = f"{prob_score}/{max_pts} - LLM 不可用，启发式评分"

        raw_total += per_problem[pk]

    scaled = int(round(raw_total * 90 / 100))

    return scaled, {
        "score": scaled,
        "raw_total_of_100": raw_total,
        "per_problem": per_problem,
        "details": details,
    }


# ============================================================================
# 入口函数
# ============================================================================

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    评估 agent 的输出。

    Args:
        answer_dir: agent 输出目录的绝对路径

    Returns:
        (score, report)
        - score: 0-100 整数
        - report: dict 详细评分报告
    """
    answers_path = _find_answers_file(answer_dir)
    content = _read_text(answers_path) if answers_path else ""

    # 维度一：文件交付与基本格式 (10 分)
    s1, r1 = _eval_file_and_format(answer_dir)

    if not content:
        return s1, {
            "total_score": s1,
            "dim1_file_format_10": r1,
            "dim2_content_90": {
                "score": 0, "details": {"error": "无内容可评估"}
            },
            "comment": "未提交有效的答案文件。",
        }

    # 维度二：内容正确性 (90 分)
    s2, r2 = _eval_content(answer_dir, content)

    total = max(0, min(100, s1 + s2))

    comment = ""
    if total >= 90:
        comment = "优秀！试题解答完整、准确，格式规范。"
    elif total >= 75:
        comment = "良好。大部分题目解答正确。"
    elif total >= 60:
        comment = "及格。基本完成试题解答，但存在较多错误。"
    elif total >= 40:
        comment = "部分完成。有一定解答但错误较多或缺失严重。"
    else:
        comment = "不及格。解答严重不足或大量缺失。"

    return total, {
        "total_score": total,
        "dim1_file_format_10": r1,
        "dim2_content_90": r2,
        "comment": comment,
    }


def print_report(score: int, report: Dict[str, Any]) -> None:
    """打印格式化的评分报告"""
    print("=" * 70)
    print("化学竞赛试题解答任务 — 评分报告")
    print("第 36 届中国化学奥林匹克（初赛）")
    print("=" * 70)
    print(f"\n总分: {score}/100\n")

    # 维度一
    r1 = report.get("dim1_file_format_10", {})
    print("-" * 50)
    print(f"【一、文件交付与基本格式】 得分: {r1.get('score', 0)}/10")
    print("-" * 50)
    for k, v in r1.get("details", {}).items():
        print(f"  {k}: {v}")

    # 维度二
    r2 = report.get("dim2_content_90", {})
    print()
    print("-" * 50)
    print(f"【二、内容正确性】 得分: {r2.get('score', 0)}/90")
    if "raw_total_of_100" in r2:
        print(f"    原始分 (满分100): {r2['raw_total_of_100']}")
    print("-" * 50)
    for k, v in r2.get("details", {}).items():
        print(f"  {k}: {v}")

    if "per_problem" in r2:
        print("\n  各题得分:")
        for pk in sorted(r2["per_problem"], key=lambda x: int(x)):
            s = r2["per_problem"][pk]
            mx = PROBLEM_MAX.get(pk, "?")
            print(f"    第{pk}题: {s}/{mx}")

    print()
    print("=" * 50)
    print(f"评语: {report.get('comment', '')}")
    print("=" * 70)


# ============================================================================
# 命令行入口
# ============================================================================

if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_dir = sys.argv[1]
    else:
        test_dir = os.path.join(os.path.dirname(__file__), "..", "workspace")

    if not os.path.isabs(test_dir):
        test_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", test_dir
        )

    if os.path.exists(test_dir):
        print(f"正在评估目录: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"目录不存在: {test_dir}")
    sys.exit(0)
