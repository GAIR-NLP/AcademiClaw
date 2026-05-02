"""
xiaoshen-query1 评分脚本
任务：高中物理答题卡自动化阅卷

总分 100 分，分四个维度：
  一、文件交付与格式        15 分
  二、数据字段完整性        10 分
  三、评分准确性（逐人比对） 55 分
  四、分数分布合理性        20 分
"""

import json
import math
import os
import sys
from typing import Any, Dict, List, Optional, Tuple

try:
    import openai
except ImportError:
    openai = None

# ───────────────────────────────────────────────────────────────────────
# 教师批改标准分（学生编号 1-46，按图片序号排列）
# 客观题 30 道选择题 × 3 分 = 90 分；主观题（解答题）满分 10 分；总分满分 100 分
# ───────────────────────────────────────────────────────────────────────
TEACHER_SCORES: List[int] = [
    74, 72, 66, 66, 66,  # 学生 01-05
    63, 63, 63, 63, 63,  # 学生 06-10
    62, 61, 60, 60, 59,  # 学生 11-15
    57, 56, 54, 54, 54,  # 学生 16-20
    54, 51, 51, 51, 51,  # 学生 21-25
    48, 48, 48, 48, 47,  # 学生 26-30
    45, 45, 45, 45, 45,  # 学生 31-35
    42, 42, 42, 39, 39,  # 学生 36-40
    39, 36, 36, 33, 33,  # 学生 41-45
    30,                   # 学生 46
]
TOTAL_STUDENTS = 46


# ───────────────────────────────────────────────────────────────────────
# 环境 / LLM 工具
# ───────────────────────────────────────────────────────────────────────

def _load_env(answer_dir: str) -> dict:
    """从 answer_dir 和 query 根目录依次加载 .env"""
    values: Dict[str, str] = {}
    search_dirs = [answer_dir, os.path.join(os.path.dirname(__file__), "..")]
    for d in search_dirs:
        env_file = os.path.join(d, ".env")
        if not os.path.isfile(env_file):
            continue
        with open(env_file, "r", encoding="utf-8") as fh:
            for raw in fh:
                raw = raw.strip()
                if not raw or raw.startswith("#") or "=" not in raw:
                    continue
                k, v = raw.split("=", 1)
                k, v = k.strip(), v.strip().strip("'\"")
                if k not in values:
                    values[k] = v
    return values


def _get_text_eval_config(answer_dir: str) -> dict:
    env = _load_env(answer_dir)

    def g(key: str, fallback: str = "") -> str:
        return os.environ.get(key) or env.get(key) or fallback

    return {
        "api_key": g("EVAL_TEXT_API_KEY", g("ANTHROPIC_API_KEY")),
        "api_base": g("EVAL_TEXT_API_BASE_URL", g("ANTHROPIC_BASE_URL")),
        "model": g("EVAL_TEXT_MODEL", "openai/gpt-5.2"),
    }


def _call_llm_judge(prompt: str, config: dict) -> str:
    """调用文本 LLM，返回原始响应文本；失败返回空字符串"""
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
        print(f"[RUBRIC] LLM Judge 调用失败: {exc}")
        return ""


def _parse_llm_json(text: str) -> Optional[dict]:
    """尝试从 LLM 响应中提取 JSON 对象"""
    if not text:
        return None
    # 去掉 markdown code block
    if "```json" in text:
        text = text.split("```json", 1)[1].split("```", 1)[0].strip()
    elif "```" in text:
        text = text.split("```", 1)[1].split("```", 1)[0].strip()
    try:
        return json.loads(text)
    except (json.JSONDecodeError, ValueError):
        return None


# ───────────────────────────────────────────────────────────────────────
# 辅助：加载 & 解析 agent 产出
# ───────────────────────────────────────────────────────────────────────

def _load_grading_json(answer_dir: str) -> Tuple[Optional[list], Optional[str], str]:
    """
    在 answer_dir 中查找 grading_results.json（或兜底搜索其它 JSON 文件）。
    返回 (parsed_list | None, filepath | None, error_msg)
    """
    if not os.path.isdir(answer_dir):
        return None, None, "answer_dir 不是有效目录"

    primary = os.path.join(answer_dir, "grading_results.json")
    if os.path.isfile(primary):
        try:
            with open(primary, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, list) else None, primary, (
                "" if isinstance(data, list)
                else f"grading_results.json 顶层不是列表 (实际类型: {type(data).__name__})"
            )
        except Exception as e:
            return None, primary, f"grading_results.json 解析失败: {e}"

    # 兜底：尝试所有 .json 文件
    for fname in sorted(os.listdir(answer_dir)):
        if not fname.endswith(".json"):
            continue
        fpath = os.path.join(answer_dir, fname)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list) and len(data) > 0:
                return data, fpath, ""
            # 嵌套在 dict 中
            if isinstance(data, dict):
                for key in ("results", "students", "grading_results", "data"):
                    if key in data and isinstance(data[key], list) and len(data[key]) > 0:
                        return data[key], fpath, ""
        except Exception:
            continue

    return None, None, "未找到 grading_results.json 或任何有效的学生成绩 JSON 文件"


def _build_student_map(entries: List[dict]) -> List[Optional[int]]:
    """
    把 agent 输出映射到学生 1-46 的 total_score。
    优先按 student_id 匹配，不足时退化为按顺序匹配。
    返回长度 TOTAL_STUDENTS 的列表，每项为 total_score 或 None。
    """
    result: List[Optional[int]] = [None] * TOTAL_STUDENTS

    # 尝试 student_id 匹配
    id_to_score: Dict[str, int] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        raw_id = str(entry.get("student_id", "")).strip().lstrip("0") or "0"
        raw_ts = entry.get("total_score")
        if raw_ts is not None:
            try:
                id_to_score[raw_id] = int(round(float(raw_ts)))
            except (ValueError, TypeError):
                pass

    matched = 0
    for idx in range(TOTAL_STUDENTS):
        key = str(idx + 1)
        if key in id_to_score:
            result[idx] = id_to_score[key]
            matched += 1

    # 如果按 ID 匹配率不足一半，回退按顺序
    if matched < TOTAL_STUDENTS * 0.5:
        result = [None] * TOTAL_STUDENTS
        for i, entry in enumerate(entries[:TOTAL_STUDENTS]):
            if not isinstance(entry, dict):
                continue
            raw_ts = entry.get("total_score")
            if raw_ts is not None:
                try:
                    result[i] = int(round(float(raw_ts)))
                except (ValueError, TypeError):
                    pass

    return result


# ───────────────────────────────────────────────────────────────────────
# 维度一：文件交付与格式（15 分）
# ───────────────────────────────────────────────────────────────────────

def _dim1_file_delivery(answer_dir: str) -> Tuple[int, dict]:
    pts = 0
    info: Dict[str, str] = {}

    entries, fpath, err = _load_grading_json(answer_dir)

    # 1.1 文件存在 (5 分)
    if fpath and os.path.isfile(fpath):
        basename = os.path.basename(fpath)
        if basename == "grading_results.json":
            pts += 5
            info["1.1 文件存在"] = "5/5 — grading_results.json 存在"
        else:
            pts += 3
            info["1.1 文件存在"] = f"3/5 — 找到 JSON 但文件名不是 grading_results.json（实际: {basename}）"
    else:
        info["1.1 文件存在"] = f"0/5 — {err or '未找到 JSON 文件'}"
        return pts, info

    # 1.2 合法 JSON 列表 (5 分)
    if entries is not None and len(entries) > 0:
        pts += 5
        info["1.2 JSON 格式"] = f"5/5 — 合法列表，{len(entries)} 条"
    elif entries is not None:
        pts += 2
        info["1.2 JSON 格式"] = "2/5 — 列表为空"
    else:
        info["1.2 JSON 格式"] = f"0/5 — {err}"
        return pts, info

    # 1.3 条目数量 = 46 (5 分)
    n = len(entries)
    if n == TOTAL_STUDENTS:
        pts += 5
        info["1.3 条目数量"] = f"5/5 — 正好 {TOTAL_STUDENTS} 条"
    elif abs(n - TOTAL_STUDENTS) <= 2:
        pts += 3
        info["1.3 条目数量"] = f"3/5 — {n} 条（偏差 ≤2）"
    elif 40 <= n <= 50:
        pts += 2
        info["1.3 条目数量"] = f"2/5 — {n} 条（接近但偏差较大）"
    elif n > 0:
        pts += 1
        info["1.3 条目数量"] = f"1/5 — 仅 {n} 条"
    else:
        info["1.3 条目数量"] = "0/5 — 无条目"

    return pts, info


# ───────────────────────────────────────────────────────────────────────
# 维度二：数据字段完整性（10 分）
# ───────────────────────────────────────────────────────────────────────

def _dim2_field_completeness(entries: Optional[List[dict]]) -> Tuple[int, dict]:
    pts = 0
    info: Dict[str, str] = {}

    if not entries:
        info["错误"] = "无数据条目，跳过字段检查"
        return 0, info

    n = len(entries)
    dicts = [e for e in entries if isinstance(e, dict)]

    # 2.1 total_score (5 分)
    cnt_ts = sum(1 for d in dicts if "total_score" in d)
    if cnt_ts == n:
        pts += 5
        info["2.1 total_score"] = f"5/5 — 全部 {n} 条含 total_score"
    elif cnt_ts >= n * 0.8:
        pts += 3
        info["2.1 total_score"] = f"3/5 — {cnt_ts}/{n} 条含 total_score"
    elif cnt_ts > 0:
        pts += 1
        info["2.1 total_score"] = f"1/5 — 仅 {cnt_ts}/{n} 条含 total_score"
    else:
        info["2.1 total_score"] = "0/5 — 无 total_score 字段"

    # 2.2 student_id (3 分)
    cnt_id = sum(1 for d in dicts if "student_id" in d)
    if cnt_id == n:
        pts += 3
        info["2.2 student_id"] = f"3/3 — 全部含 student_id"
    elif cnt_id >= n * 0.8:
        pts += 2
        info["2.2 student_id"] = f"2/3 — {cnt_id}/{n} 条含 student_id"
    elif cnt_id > 0:
        pts += 1
        info["2.2 student_id"] = f"1/3 — 仅 {cnt_id}/{n} 条含 student_id"
    else:
        info["2.2 student_id"] = "0/3 — 无 student_id 字段"

    # 2.3 objective_score / subjective_score (2 分)
    cnt_obj = sum(1 for d in dicts if "objective_score" in d)
    cnt_sub = sum(1 for d in dicts if "subjective_score" in d)
    if cnt_obj >= n * 0.8 and cnt_sub >= n * 0.8:
        pts += 2
        info["2.3 分项得分"] = f"2/2 — objective: {cnt_obj}/{n}, subjective: {cnt_sub}/{n}"
    elif cnt_obj >= n * 0.5 or cnt_sub >= n * 0.5:
        pts += 1
        info["2.3 分项得分"] = f"1/2 — objective: {cnt_obj}/{n}, subjective: {cnt_sub}/{n}"
    else:
        info["2.3 分项得分"] = f"0/2 — objective: {cnt_obj}/{n}, subjective: {cnt_sub}/{n}"

    return pts, info


# ───────────────────────────────────────────────────────────────────────
# 维度三：评分准确性 — 逐人比对（55 分）
# ───────────────────────────────────────────────────────────────────────

def _dim3_score_accuracy(entries: Optional[List[dict]]) -> Tuple[int, dict]:
    """
    将 agent 输出的 total_score 与教师标准逐人比较。

    每名学生按误差给加权分：
      差 = 0  → 权重 1.0
      差 ≤ 3  → 权重 0.8（约 1 道选择题偏差）
      差 ≤ 6  → 权重 0.5（约 2 道或主观题偏差）
      差 ≤ 10 → 权重 0.25
      差 > 10 → 权重 0
    总分 = 55 × (加权总和 / 46)
    """
    info: Dict[str, Any] = {}

    if not entries:
        info["错误"] = "无数据条目"
        return 0, info

    model_scores = _build_student_map(entries)

    weight_sum = 0.0
    exact = 0
    close = 0  # diff ≤ 3
    missing = 0
    sample_lines: List[str] = []

    for i in range(TOTAL_STUDENTS):
        ref = TEACHER_SCORES[i]
        ms = model_scores[i]
        if ms is None:
            missing += 1
            sample_lines.append(f"  #{i+1:02d}: 缺失 (标准={ref})")
            continue

        diff = abs(ms - ref)
        if diff == 0:
            w = 1.0
            exact += 1
            close += 1
        elif diff <= 3:
            w = 0.8
            close += 1
        elif diff <= 6:
            w = 0.5
        elif diff <= 10:
            w = 0.25
        else:
            w = 0.0

        weight_sum += w
        sample_lines.append(f"  #{i+1:02d}: 模型={ms}, 标准={ref}, 差={diff}, w={w}")

    raw = 55.0 * weight_sum / TOTAL_STUDENTS
    pts = int(round(raw))
    pts = max(0, min(55, pts))

    info["完全匹配"] = f"{exact}/{TOTAL_STUDENTS}"
    info["近似匹配(≤3)"] = f"{close}/{TOTAL_STUDENTS}"
    info["缺失"] = f"{missing}/{TOTAL_STUDENTS}"
    info["加权得分"] = f"{pts}/55 (原始 {raw:.2f})"
    # 展示前 10 和后 5 条以控制报告长度
    info["前10人"] = sample_lines[:10]
    info["后5人"] = sample_lines[-5:]

    return pts, info


# ───────────────────────────────────────────────────────────────────────
# 维度四：分数分布合理性（20 分）
#   确定性检查 12 分 + LLM-as-Judge 8 分
# ───────────────────────────────────────────────────────────────────────

def _dim4_distribution(entries: Optional[List[dict]], answer_dir: str) -> Tuple[int, dict]:
    info: Dict[str, Any] = {}

    if not entries:
        info["错误"] = "无数据条目"
        return 0, info

    raw_map = _build_student_map(entries)
    scores = [s for s in raw_map if s is not None]

    if not scores:
        info["错误"] = "无有效分数"
        return 0, info

    # ---------- 确定性子项（12 分） ----------
    det = 0

    # 4.1 分数范围 [0, 100] (4 分)
    all_in_range = all(0 <= s <= 100 for s in scores)
    if all_in_range:
        det += 4
        info["4.1 分数范围"] = f"4/4 — 全部在 [0,100]，范围 [{min(scores)},{max(scores)}]"
    else:
        out = [s for s in scores if s < 0 or s > 100]
        info["4.1 分数范围"] = f"0/4 — 存在超出 [0,100] 的分数: {out[:5]}"

    # 4.2 3 的倍数比例 (4 分)
    # 客观题每题 3 分，合理结果中大量分数应是 3 的倍数
    cnt3 = sum(1 for s in scores if s % 3 == 0)
    ratio3 = cnt3 / len(scores)
    if ratio3 >= 0.6:
        det += 4
        info["4.2 3倍数比例"] = f"4/4 — {cnt3}/{len(scores)} ({ratio3:.0%})"
    elif ratio3 >= 0.3:
        det += 2
        info["4.2 3倍数比例"] = f"2/4 — {cnt3}/{len(scores)} ({ratio3:.0%})"
    else:
        info["4.2 3倍数比例"] = f"0/4 — {cnt3}/{len(scores)} ({ratio3:.0%})"

    # 4.3 分数多样性 (4 分)
    unique_cnt = len(set(scores))
    if unique_cnt >= 10:
        det += 4
        info["4.3 多样性"] = f"4/4 — {unique_cnt} 种不同分数"
    elif unique_cnt >= 5:
        det += 2
        info["4.3 多样性"] = f"2/4 — {unique_cnt} 种不同分数"
    elif unique_cnt >= 2:
        det += 1
        info["4.3 多样性"] = f"1/4 — 仅 {unique_cnt} 种"
    else:
        info["4.3 多样性"] = f"0/4 — 所有分数相同 ({scores[0]})"

    # ---------- LLM-as-Judge 子项（8 分） ----------
    avg_model = sum(scores) / len(scores)
    avg_teacher = sum(TEACHER_SCORES) / TOTAL_STUDENTS
    teacher_sorted = sorted(TEACHER_SCORES, reverse=True)
    model_sorted = sorted(scores, reverse=True)

    llm_prompt = f"""你是一个高中物理考试阅卷评估专家。以下是一次自动化批改结果的分数分布分析任务。

背景：
- 46 名高一学生参加物理期中考试
- 客观题 30 道选择题，每题 3 分，满分 90 分
- 主观题（解答题）满分 10 分
- 总分满分 100 分

教师手工批改分数（参考标准）：
- 平均分: {avg_teacher:.1f}
- 范围: [{min(TEACHER_SCORES)}, {max(TEACHER_SCORES)}]
- 前10高分: {teacher_sorted[:10]}
- 后10低分: {teacher_sorted[-10:]}

自动阅卷系统输出分数：
- 有效人数: {len(scores)}
- 平均分: {avg_model:.1f}
- 范围: [{min(scores)}, {max(scores)}]
- 前10高分: {model_sorted[:10]}
- 后10低分: {model_sorted[-10:]}

请从以下维度综合评分（0-8 整数）：
1. 平均分是否接近教师标准（~52 分）
2. 分数范围是否合理（应在 30-74 左右）
3. 分数是否有合理差异（不应全部相同或过度集中）
4. 整体趋势是否与教师评分接近

严格按以下 JSON 格式回复，不要输出其他内容：
```json
{{"score": 0, "reason": "简短理由"}}
```
分数为 0-8 的整数。"""

    config = _get_text_eval_config(answer_dir)
    llm_text = _call_llm_judge(llm_prompt, config)
    llm_parsed = _parse_llm_json(llm_text)

    if llm_parsed and "score" in llm_parsed:
        llm_pts = max(0, min(8, int(llm_parsed["score"])))
        info["4.4 LLM分布评估"] = f"{llm_pts}/8 — {llm_parsed.get('reason', '')}"
    else:
        # LLM 不可用或解析失败，使用确定性降级
        llm_pts = _fallback_distribution(scores)
        tag = "LLM 解析失败" if llm_text else "LLM 不可用"
        info["4.4 LLM分布评估"] = f"{llm_pts}/8 — {tag}，使用降级评估"

    total = det + llm_pts
    info["确定性得分"] = f"{det}/12"
    info["LLM得分"] = f"{llm_pts}/8"
    return total, info


def _fallback_distribution(scores: List[int]) -> int:
    """LLM 不可用时的简单分布评估（保守，上限 8 分）"""
    pts = 0
    avg = sum(scores) / len(scores)
    avg_teacher = sum(TEACHER_SCORES) / TOTAL_STUDENTS

    # 平均分接近度
    if abs(avg - avg_teacher) <= 10:
        pts += 3
    elif abs(avg - avg_teacher) <= 20:
        pts += 1

    # 范围合理性
    if max(scores) <= 100 and min(scores) >= 0:
        if max(scores) >= 50 and min(scores) <= 50:
            pts += 3
        else:
            pts += 1

    # 多样性
    if len(set(scores)) >= 10:
        pts += 2
    elif len(set(scores)) >= 3:
        pts += 1

    return min(8, pts)


# ───────────────────────────────────────────────────────────────────────
# 主入口
# ───────────────────────────────────────────────────────────────────────

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    评估 agent 的自动阅卷输出。

    Args:
        answer_dir: agent 输出目录的绝对路径

    Returns:
        (score, report) — score 为 0-100 整数
    """
    report: Dict[str, Any] = {}

    # 预加载数据
    raw_data, _, _ = _load_grading_json(answer_dir)
    entries: Optional[List[dict]] = None
    if isinstance(raw_data, list):
        entries = raw_data

    # 维度一
    s1, r1 = _dim1_file_delivery(answer_dir)
    report["一、文件交付与格式 (15分)"] = r1

    # 维度二
    s2, r2 = _dim2_field_completeness(entries)
    report["二、数据字段完整性 (10分)"] = r2

    # 维度三
    s3, r3 = _dim3_score_accuracy(entries)
    report["三、评分准确性 (55分)"] = r3

    # 维度四
    s4, r4 = _dim4_distribution(entries, answer_dir)
    report["四、分数分布合理性 (20分)"] = r4

    total = max(0, min(100, s1 + s2 + s3 + s4))

    report["分项得分"] = {
        "文件交付与格式": f"{s1}/15",
        "数据字段完整性": f"{s2}/10",
        "评分准确性": f"{s3}/55",
        "分数分布合理性": f"{s4}/20",
    }

    if total >= 85:
        report["评语"] = "优秀！自动阅卷结果与教师评分高度一致。"
    elif total >= 65:
        report["评语"] = "良好。大部分学生分数识别准确，部分有偏差。"
    elif total >= 45:
        report["评语"] = "及格。基本完成阅卷，但准确性有明显不足。"
    elif total >= 25:
        report["评语"] = "部分完成。能输出结果文件但分数准确性较差。"
    else:
        report["评语"] = "不及格。任务完成度严重不足。"

    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """打印格式化的评分报告"""
    print("=" * 70)
    print("高中物理答题卡自动阅卷 — 评分报告")
    print("=" * 70)
    print(f"\n总分: {score}/100\n")

    # 分项得分
    sub = report.get("分项得分", {})
    if sub:
        print("分项得分:")
        for k, v in sub.items():
            print(f"  {k}: {v}")

    # 各维度详情
    section_keys = [
        "一、文件交付与格式 (15分)",
        "二、数据字段完整性 (10分)",
        "三、评分准确性 (55分)",
        "四、分数分布合理性 (20分)",
    ]
    for key in section_keys:
        section = report.get(key, {})
        if not section:
            continue
        print(f"\n{'─' * 50}")
        print(f"【{key}】")
        print(f"{'─' * 50}")
        for k, v in section.items():
            if isinstance(v, list):
                print(f"  {k}:")
                for line in v:
                    print(f"    {line}")
            else:
                print(f"  {k}: {v}")

    # 评语
    print(f"\n{'=' * 70}")
    print(f"评语: {report.get('评语', '')}")
    print("=" * 70)


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(__file__), "..", "gpt-5", "attempt_1"
    )
    if os.path.isdir(target):
        print(f"评估目录: {target}\n")
        s, r = evaluate(target)
        print_report(s, r)
    else:
        print(f"目录不存在: {target}")
    sys.exit(0)
