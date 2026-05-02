"""
评分标准 (Rubric) — 识别小鹤双拼输入序列中的多余字母索引

任务：给定 100 个奇数长度的小写字母字符串（每个是用小鹤双拼输入一个通顺中文句子
所按下的字母序列，但多插入了一个字母），找出每个字符串中多余字母的索引，
使得删掉该字母后字符串恢复成有效的双拼编码。

总分：100 分

评分维度：
一、文件交付与格式规范 (15分)
  1.1 output.json 存在                         5 分
  1.2 JSON 格式有效且为列表                    5 分
  1.3 列表长度为 100 且全部为整数              5 分

二、索引合法性 (10分)
  按比例计分：每个索引在对应字符串的合法范围内（0 <= idx < len(s)）

三、答案准确率 (75分)
  按正确答案数量线性计分：score = round(correct / 100 * 75)
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Tuple

# ---------------------------------------------------------------------------
# 参考数据路径
# ---------------------------------------------------------------------------
_BASE_DIR = Path(__file__).resolve().parent
_ANSWERS_PATH = _BASE_DIR / "rubric_assets" / "answers.json"
_PROBLEMS_PATH = _BASE_DIR / ".." / "context" / "problems.json"


def _load_json(path: Path) -> Any:
    """安全地加载 JSON 文件"""
    return json.loads(path.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# evaluate
# ---------------------------------------------------------------------------

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    评估 agent 的输出。

    Args:
        answer_dir: agent 输出目录的绝对路径

    Returns:
        (score, report)
        - score: 0-100 的整数
        - report: dict，包含详细评估报告
    """
    base = Path(answer_dir).resolve()
    output_path = base / "output.json"

    dim1_score = 0          # 文件交付与格式（满分 15）
    dim1_details: Dict[str, str] = {}
    dim1_deductions: List[str] = []

    dim2_score = 0          # 索引合法性（满分 10）
    dim2_details: Dict[str, str] = {}
    dim2_deductions: List[str] = []

    dim3_score = 0          # 答案准确率（满分 75）
    dim3_details: Dict[str, str] = {}
    dim3_deductions: List[str] = []

    data: List[int] = []    # 最终解析出的预测列表

    # =====================================================================
    # 一、文件交付与格式规范 (15 分)
    # =====================================================================

    # 1.1 output.json 存在 (5 分)
    if not output_path.exists():
        dim1_details["1.1 output.json 存在"] = "0/5 — 文件不存在"
        dim1_deductions.append("未找到 output.json")
        return _build_report(0, dim1_score, dim1_details, dim1_deductions,
                             dim2_score, dim2_details, dim2_deductions,
                             dim3_score, dim3_details, dim3_deductions)

    dim1_score += 5
    dim1_details["1.1 output.json 存在"] = "5/5 — 文件存在"

    # 1.2 JSON 格式有效且为列表 (5 分)
    try:
        raw_text = output_path.read_text(encoding="utf-8")
        parsed = json.loads(raw_text)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        dim1_details["1.2 JSON 格式有效"] = f"0/5 — 解析失败: {str(exc)[:80]}"
        dim1_deductions.append(f"output.json JSON 解析失败: {str(exc)[:80]}")
        return _build_report(dim1_score, dim1_score, dim1_details, dim1_deductions,
                             dim2_score, dim2_details, dim2_deductions,
                             dim3_score, dim3_details, dim3_deductions)

    if not isinstance(parsed, list):
        dim1_details["1.2 JSON 格式有效"] = (
            f"0/5 — 不是列表，类型为 {type(parsed).__name__}"
        )
        dim1_deductions.append("output.json 内容不是 JSON 列表")
        return _build_report(dim1_score, dim1_score, dim1_details, dim1_deductions,
                             dim2_score, dim2_details, dim2_deductions,
                             dim3_score, dim3_details, dim3_deductions)

    dim1_score += 5
    dim1_details["1.2 JSON 格式有效"] = "5/5 — 有效 JSON 列表"

    # 1.3 列表长度为 100 且全部为整数 (5 分)
    all_int = all(isinstance(x, int) for x in parsed)
    correct_length = len(parsed) == 100

    if correct_length and all_int:
        dim1_score += 5
        dim1_details["1.3 长度与类型"] = "5/5 — 长度 100，全部为整数"
        data = parsed
    elif correct_length and not all_int:
        # 尝试将元素转为整数
        try:
            data = [int(x) for x in parsed]
            dim1_score += 3
            dim1_details["1.3 长度与类型"] = (
                "3/5 — 长度正确，但元素非全部为 int（已尝试转换）"
            )
            dim1_deductions.append("列表元素不全是整数类型")
        except (ValueError, TypeError):
            dim1_score += 1
            dim1_details["1.3 长度与类型"] = "1/5 — 长度正确，但包含无法转为整数的元素"
            dim1_deductions.append("列表包含无法转换为整数的元素")
            data = []
    elif not correct_length and all_int:
        dim1_score += 2
        dim1_details["1.3 长度与类型"] = (
            f"2/5 — 全部为整数，但长度 {len(parsed)} != 100"
        )
        dim1_deductions.append(f"列表长度不正确：期望 100，实际 {len(parsed)}")
        data = parsed
    else:
        dim1_details["1.3 长度与类型"] = (
            f"0/5 — 长度 {len(parsed)}，且元素非全部整数"
        )
        dim1_deductions.append(f"列表长度 {len(parsed)} 且元素类型不正确")
        # 尽量转换以便后续部分评分
        converted: List[int] = []
        for x in parsed:
            try:
                converted.append(int(x))
            except (ValueError, TypeError):
                converted.append(-1)
        data = converted

    # =====================================================================
    # 加载参考数据
    # =====================================================================
    try:
        reference: List[int] = _load_json(_ANSWERS_PATH)
    except Exception as exc:
        # 参考答案加载失败，无法继续评分
        dim3_details["错误"] = f"参考答案加载失败: {exc}"
        return _build_report(
            dim1_score, dim1_score, dim1_details, dim1_deductions,
            0, dim2_details, dim2_deductions,
            0, dim3_details, dim3_deductions,
        )

    try:
        problems: List[str] = _load_json(_PROBLEMS_PATH)
    except Exception:
        problems = []

    # =====================================================================
    # 二、索引合法性 (10 分)
    # =====================================================================
    if data and problems and len(problems) == 100:
        valid_count = 0
        invalid_examples: List[str] = []
        check_len = min(len(data), len(problems))
        for i in range(check_len):
            idx = data[i]
            s_len = len(problems[i])
            if isinstance(idx, int) and 0 <= idx < s_len:
                valid_count += 1
            elif len(invalid_examples) < 5:
                invalid_examples.append(
                    f"#{i}: idx={idx}, strlen={s_len}"
                )
        # 未覆盖的部分算无效
        total_invalid = 100 - valid_count
        validity_ratio = valid_count / 100
        dim2_score = round(validity_ratio * 10)
        dim2_details["合法索引数"] = f"{valid_count}/100 ({validity_ratio:.0%})"
        if invalid_examples:
            dim2_details["非法示例"] = "; ".join(invalid_examples)
            dim2_deductions.append(f"存在 {total_invalid} 个索引超出字符串合法范围")
    elif data:
        # 没有 problems 时无法校验范围，给保守分
        dim2_score = 5
        dim2_details["说明"] = "5/10 — 无法加载 problems.json，跳过范围校验，给保守分"
    else:
        dim2_details["说明"] = "0/10 — 无有效预测数据"

    # =====================================================================
    # 三、答案准确率 (75 分)
    # =====================================================================
    if not data:
        dim3_details["说明"] = "0/75 — 无有效预测数据"
    else:
        preds = data
        min_len = min(len(preds), len(reference))
        correct = sum(1 for i in range(min_len) if preds[i] == reference[i])
        # 短了的部分算错误
        accuracy = correct / len(reference)
        dim3_score = round(accuracy * 75)
        dim3_details["准确率"] = f"{correct}/{len(reference)} ({accuracy:.2%})"

        incorrect_indices = [
            i for i in range(min_len) if preds[i] != reference[i]
        ]
        incorrect_indices += list(range(min_len, len(reference)))

        if len(preds) != len(reference):
            dim3_details["长度不匹配"] = (
                f"提交 {len(preds)} 条，参考 {len(reference)} 条"
            )
            dim3_deductions.append(
                f"长度不匹配: 提交 {len(preds)} / 参考 {len(reference)}"
            )

        if incorrect_indices:
            dim3_deductions.append(f"错误条目数: {len(incorrect_indices)}")
            # 显示前 10 个错误
            shown = incorrect_indices[:10]
            error_samples = []
            for idx in shown:
                pred_val = preds[idx] if idx < len(preds) else "N/A"
                ref_val = reference[idx]
                error_samples.append(f"#{idx}: pred={pred_val}, ref={ref_val}")
            dim3_details["错误示例（前10条）"] = "; ".join(error_samples)

    # =====================================================================
    # 汇总
    # =====================================================================
    total = dim1_score + dim2_score + dim3_score

    return _build_report(
        total, dim1_score, dim1_details, dim1_deductions,
        dim2_score, dim2_details, dim2_deductions,
        dim3_score, dim3_details, dim3_deductions,
    )


# ---------------------------------------------------------------------------
# 报告构建
# ---------------------------------------------------------------------------

def _build_report(
    total: int,
    dim1_score: int,
    dim1_details: Dict[str, str],
    dim1_deductions: List[str],
    dim2_score: int,
    dim2_details: Dict[str, str],
    dim2_deductions: List[str],
    dim3_score: int,
    dim3_details: Dict[str, str],
    dim3_deductions: List[str],
) -> Tuple[int, Dict[str, Any]]:
    """构建统一格式的评分报告"""

    all_deductions = dim1_deductions + dim2_deductions + dim3_deductions

    if total >= 95:
        comment = "优秀！几乎完美地识别了所有多余字母的索引。"
    elif total >= 80:
        comment = "良好。大部分索引正确，少数条目有误。"
    elif total >= 60:
        comment = "及格。超过半数的索引正确，但仍有不少错误。"
    elif total >= 30:
        comment = "部分完成。正确率偏低，推理逻辑可能存在缺陷。"
    elif total > 15:
        comment = "不及格。正确率极低，基本未能完成推理任务。"
    else:
        comment = "未有效完成任务。"

    report: Dict[str, Any] = {
        "总分": total,
        "分项得分": {
            "文件交付与格式 (15)": dim1_score,
            "索引合法性 (10)": dim2_score,
            "答案准确率 (75)": dim3_score,
        },
        "结果评分": {
            "得分": total,
            "满分": 100,
            "扣分原因": all_deductions,
        },
        "过程评分": {
            "得分": total,
            "满分": 100,
            "扣分原因": [],
        },
        "评语": comment,
        "raw": {
            "dim1_score": dim1_score,
            "dim2_score": dim2_score,
            "dim3_score": dim3_score,
            "dim1_details": dim1_details,
            "dim2_details": dim2_details,
            "dim3_details": dim3_details,
        },
    }

    return total, report


# ---------------------------------------------------------------------------
# print_report
# ---------------------------------------------------------------------------

def print_report(score: int, report: Dict[str, Any]) -> None:
    """打印格式化的评分报告"""
    print("=" * 60)
    print("识别小鹤双拼多余字母索引 — 评分报告")
    print("=" * 60)
    print(f"\n总分: {score}/100")

    # 分项得分
    scores_map = report.get("分项得分", {})
    if scores_map:
        print("\n分项得分:")
        for k, v in scores_map.items():
            print(f"  {k}: {v}")

    # 各维度详情
    raw = report.get("raw", {})

    sections = [
        ("dim1_details", "一、文件交付与格式规范 (15分)"),
        ("dim2_details", "二、索引合法性 (10分)"),
        ("dim3_details", "三、答案准确率 (75分)"),
    ]
    for key, title in sections:
        details = raw.get(key, {})
        if details:
            print(f"\n{'─' * 50}")
            print(f"【{title}】")
            for k, v in details.items():
                print(f"  {k}: {v}")

    # 扣分原因汇总
    deductions = report.get("结果评分", {}).get("扣分原因", [])
    if deductions:
        print(f"\n扣分原因:")
        for i, d in enumerate(deductions, 1):
            print(f"  {i}. {d}")

    print(f"\n{'=' * 50}")
    print(f"评语: {report.get('评语', '')}")
    print("=" * 60)


# ---------------------------------------------------------------------------
# CLI 入口
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    test_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(__file__), "..", "gpt-5", "attempt_1"
    )
    test_dir = os.path.abspath(test_dir)

    if os.path.exists(test_dir):
        print(f"正在评估目录: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"目录不存在: {test_dir}")
    sys.exit(0)
