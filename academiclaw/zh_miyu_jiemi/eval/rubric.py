#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
谜语解谜任务 — 评分脚本 (rubric.py)

任务概述:
  给定 135 条中文谜语（66 动物类 + 69 水果类），agent 需要在 workspace 中
  阅读 query.json，为每条谜语输出预测谜底，生成 submission.json。

交付物: submission.json

总分 100 分，分为四个维度:
  一、文件交付与格式规范  (10 分)
  二、覆盖完整性          (15 分)
  三、答案准确率          (60 分)
  四、预测质量            (15 分)
"""

import os
import re
import json
import sys
from typing import Tuple, Dict, Any, List


# ============================================================================
# 标准答案（硬编码，确保评分不依赖外部文件）
# ============================================================================

GROUND_TRUTH: Dict[str, str] = {
    "动物类/001": "狼",
    "动物类/002": "蜻蜓",
    "动物类/003": "蛇",
    "动物类/004": "大雁",
    "动物类/005": "萤火虫",
    "动物类/006": "萤火虫",
    "动物类/007": "鸵鸟",
    "动物类/008": "猫头鹰",
    "动物类/009": "蚕",
    "动物类/010": "狗",
    "动物类/011": "蜻蜓",
    "动物类/012": "黄蜂",
    "动物类/013": "狗",
    "动物类/014": "猴子",
    "动物类/015": "猫",
    "动物类/016": "鱼",
    "动物类/017": "蚯蚓",
    "动物类/018": "山羊",
    "动物类/019": "刀螂",
    "动物类/020": "虾",
    "动物类/021": "鸭子",
    "动物类/022": "刺猬",
    "动物类/023": "青蛙",
    "动物类/024": "鱼",
    "动物类/025": "蛇",
    "动物类/026": "螃蟹",
    "动物类/027": "羊",
    "动物类/028": "蜻蜓",
    "动物类/029": "青蛙",
    "动物类/030": "鱼",
    "动物类/031": "鹅",
    "动物类/032": "蝎子",
    "动物类/033": "螺蛳",
    "动物类/034": "鸭子",
    "动物类/035": "金钱豹",
    "动物类/036": "麋鹿",
    "动物类/037": "狐狸",
    "动物类/038": "青蛙",
    "动物类/039": "蚊子",
    "动物类/040": "牛",
    "动物类/041": "蛇",
    "动物类/042": "马",
    "动物类/043": "燕子",
    "动物类/044": "蚂蚁",
    "动物类/045": "鹿",
    "动物类/046": "蚂蚁",
    "动物类/047": "鸵鸟",
    "动物类/048": "鲸鱼",
    "动物类/049": "猪",
    "动物类/050": "乌龟",
    "动物类/051": "纺织娘",
    "动物类/052": "壁虎",
    "动物类/053": "乌贼",
    "动物类/054": "苍蝇",
    "动物类/055": "鱼鹰",
    "动物类/056": "鸳鸯",
    "动物类/057": "猫",
    "动物类/058": "梅花鹿",
    "动物类/059": "骡子",
    "动物类/060": "马蜂",
    "动物类/061": "海鸥",
    "动物类/062": "蛐蛐儿",
    "动物类/063": "蜈蚣",
    "动物类/064": "蜗牛",
    "动物类/065": "蜗牛",
    "动物类/066": "虾",
    "水果类/001": "桔子",
    "水果类/002": "核桃",
    "水果类/003": "香蕉",
    "水果类/004": "菱角",
    "水果类/005": "香蕉",
    "水果类/006": "桔子",
    "水果类/007": "花生",
    "水果类/008": "西瓜",
    "水果类/009": "桃子",
    "水果类/010": "桔子",
    "水果类/011": "桂圆",
    "水果类/012": "杨桃",
    "水果类/013": "菱角",
    "水果类/014": "黑枣",
    "水果类/015": "桔子",
    "水果类/016": "桑葚",
    "水果类/017": "白果",
    "水果类/018": "草莓",
    "水果类/019": "莲子",
    "水果类/020": "柚子",
    "水果类/021": "桔子",
    "水果类/022": "草莓",
    "水果类/023": "杨梅",
    "水果类/024": "核桃",
    "水果类/025": "红枣",
    "水果类/026": "荔枝",
    "水果类/027": "山竹",
    "水果类/028": "荔枝",
    "水果类/029": "西瓜",
    "水果类/030": "香蕉",
    "水果类/031": "石榴",
    "水果类/032": "甘蔗",
    "水果类/033": "梨",
    "水果类/034": "石榴",
    "水果类/035": "枣树",
    "水果类/036": "生梨",
    "水果类/037": "甘蔗",
    "水果类/038": "石榴",
    "水果类/039": "桃子",
    "水果类/040": "香蕉",
    "水果类/041": "核桃",
    "水果类/042": "柿子",
    "水果类/043": "枣",
    "水果类/044": "栗子",
    "水果类/045": "葡萄",
    "水果类/046": "橘子",
    "水果类/047": "桔子",
    "水果类/048": "石榴",
    "水果类/049": "橘子",
    "水果类/050": "？子",
    "水果类/051": "樱桃",
    "水果类/052": "杨梅",
    "水果类/053": "香蕉",
    "水果类/054": "石榴",
    "水果类/055": "菱",
    "水果类/056": "荔枝",
    "水果类/057": "香蕉",
    "水果类/058": "樱桃",
    "水果类/059": "桃子",
    "水果类/060": "花生",
    "水果类/061": "苹果",
    "水果类/062": "花生",
    "水果类/063": "梨",
    "水果类/064": "桃子",
    "水果类/065": "梅子",
    "水果类/066": "椰子",
    "水果类/067": "石榴",
    "水果类/068": "石榴",
    "水果类/069": "枇杷",
}

# 同义词/别名映射: 如果 agent 的预测归一化后命中别名，也视为正确
SYNONYMS: Dict[str, set] = {
    "蜻蜓": {"蜻蜒"},
    "刀螂": {"螳螂"},
    "鸭子": {"鸭"},
    "螃蟹": {"蟹"},
    "蚂蚁": {"蚁"},
    "猴子": {"猴"},
    "蚊子": {"蚊"},
    "鲸鱼": {"鲸", "蓝鲸"},
    "桔子": {"橘子", "橘", "桔"},
    "橘子": {"桔子", "桔", "橘"},
    "梨": {"生梨", "鸭梨"},
    "生梨": {"梨", "鸭梨"},
    "枣": {"红枣", "大枣"},
    "红枣": {"枣", "大枣"},
    "枣树": {"枣"},
    "菱角": {"菱"},
    "菱": {"菱角"},
    "山羊": {"羊"},
    "羊": {"山羊"},
    "黄蜂": {"马蜂", "蜜蜂"},
    "马蜂": {"黄蜂"},
    "蛐蛐儿": {"蛐蛐", "蟋蟀"},
    "鹿": {"梅花鹿"},
    "梅花鹿": {"鹿"},
    "萤火虫": {"荧火虫"},
    "鸵鸟": {"鸵鸟"},
    "猫头鹰": {"夜猫子", "鸮"},
    "狐狸": {"狐"},
}

TOTAL_ITEMS = len(GROUND_TRUTH)  # 135


# ============================================================================
# 文本归一化
# ============================================================================

def _normalize(text: str) -> str:
    """轻量级中文文本归一化"""
    s = (text or "").strip()
    # 去前导冒号/标点
    s = re.sub(r"^[\s:：\-—]+", "", s)
    s = s.strip()
    # 去包裹括号
    if (s.startswith("（") and s.endswith("）")) or (s.startswith("(") and s.endswith(")")):
        s = s[1:-1].strip()
    # 去内部空白
    s = re.sub(r"\s+", "", s)
    return s


def _is_match(pred: str, gold: str) -> bool:
    """判断预测是否匹配标准答案（精确匹配 + 同义词）"""
    np = _normalize(pred)
    ng = _normalize(gold)
    if not np:
        return False
    if np == ng:
        return True
    synonyms = SYNONYMS.get(gold, set())
    return np in {_normalize(s) for s in synonyms}


# ============================================================================
# 一、文件交付与格式规范 (10 分)
#
#   1.1 submission.json 存在            4 分
#   1.2 JSON 可正确解析                 3 分
#   1.3 包含 predictions 数组且元素格式  3 分
# ============================================================================

def _evaluate_file_delivery(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    score = 0
    details: Dict[str, Any] = {}
    deductions: List[str] = []

    all_files = os.listdir(answer_dir) if os.path.isdir(answer_dir) else []
    json_files = [f for f in all_files if f.endswith(".json")]
    submission_path = os.path.join(answer_dir, "submission.json")

    # 1.1 文件存在 (4分)
    if os.path.isfile(submission_path):
        score += 4
        details["1.1 文件存在"] = "4/4 - submission.json 存在"
        target_path = submission_path
    elif json_files:
        score += 1
        target_path = os.path.join(answer_dir, json_files[0])
        details["1.1 文件存在"] = f"1/4 - 文件名不正确 (找到 {json_files[0]})"
        deductions.append(f"文件名应为 submission.json，实际为 {json_files[0]}")
    else:
        details["1.1 文件存在"] = "0/4 - 未找到任何 JSON 文件"
        deductions.append("缺少 submission.json")
        return 0, {"分数": 0, "详情": details, "扣分原因": deductions}

    # 1.2 JSON 可解析 (3分)
    try:
        with open(target_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        score += 3
        details["1.2 JSON解析"] = "3/3 - 合法 JSON"
    except json.JSONDecodeError as e:
        details["1.2 JSON解析"] = f"0/3 - 解析失败: {str(e)[:80]}"
        deductions.append("JSON 格式错误，无法解析")
        return score, {"分数": score, "详情": details, "扣分原因": deductions}
    except Exception as e:
        details["1.2 JSON解析"] = f"0/3 - 读取异常: {str(e)[:80]}"
        deductions.append("文件读取失败")
        return score, {"分数": score, "详情": details, "扣分原因": deductions}

    # 1.3 predictions 数组格式 (3分)
    preds = data.get("predictions")
    if isinstance(preds, list) and len(preds) > 0:
        valid = sum(
            1 for p in preds
            if isinstance(p, dict) and "id" in p and "prediction" in p
        )
        if valid == len(preds):
            score += 3
            details["1.3 数据结构"] = f"3/3 - predictions 含 {len(preds)} 条，格式正确"
        elif valid > 0:
            score += 1
            details["1.3 数据结构"] = f"1/3 - {valid}/{len(preds)} 条格式正确"
            deductions.append(f"{len(preds) - valid} 条记录缺少 id 或 prediction 字段")
        else:
            details["1.3 数据结构"] = "0/3 - 元素格式不正确（缺少 id/prediction）"
            deductions.append("predictions 元素缺少必要字段")
    elif isinstance(preds, list):
        details["1.3 数据结构"] = "0/3 - predictions 数组为空"
        deductions.append("predictions 为空数组")
    else:
        details["1.3 数据结构"] = "0/3 - 缺少 predictions 字段"
        deductions.append("JSON 中缺少 predictions 字段")

    return score, {"分数": score, "详情": details, "扣分原因": deductions}


# ============================================================================
# 辅助: 加载 agent 的预测
# ============================================================================

def _load_predictions(answer_dir: str) -> Dict[str, str]:
    """从 answer_dir 加载预测结果，返回 {id: prediction}"""
    submission_path = os.path.join(answer_dir, "submission.json")
    if not os.path.isfile(submission_path):
        all_files = os.listdir(answer_dir) if os.path.isdir(answer_dir) else []
        json_files = [f for f in all_files if f.endswith(".json")]
        if json_files:
            submission_path = os.path.join(answer_dir, json_files[0])
        else:
            return {}

    try:
        with open(submission_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return {}

    preds_list = data.get("predictions", [])
    if not isinstance(preds_list, list):
        return {}

    result: Dict[str, str] = {}
    for item in preds_list:
        if isinstance(item, dict) and "id" in item and "prediction" in item:
            rid = str(item["id"]).strip()
            pred = str(item["prediction"]) if item["prediction"] is not None else ""
            if rid:
                result[rid] = pred
    return result


# ============================================================================
# 二、覆盖完整性 (15 分)
#
#   线性: 覆盖率 × 15
#   覆盖率 = 有效预测数 / 总题目数 (135)
# ============================================================================

def _evaluate_coverage(predictions: Dict[str, str]) -> Tuple[int, Dict[str, Any]]:
    details: Dict[str, Any] = {}
    deductions: List[str] = []

    covered = sum(1 for rid in GROUND_TRUTH if rid in predictions)
    missing = TOTAL_ITEMS - covered
    extra = sum(1 for rid in predictions if rid not in GROUND_TRUTH)
    coverage_rate = covered / TOTAL_ITEMS if TOTAL_ITEMS > 0 else 0.0

    score = round(coverage_rate * 15)

    details["总题目数"] = TOTAL_ITEMS
    details["已覆盖"] = covered
    details["未覆盖"] = missing
    details["多余ID"] = extra
    details["覆盖率"] = f"{coverage_rate * 100:.1f}%"

    if missing > 0:
        deductions.append(f"缺少 {missing}/{TOTAL_ITEMS} 个题目的预测")
    if extra > 0:
        deductions.append(f"包含 {extra} 个不在题目中的多余 ID")

    return score, {"分数": score, "详情": details, "扣分原因": deductions}


# ============================================================================
# 三、答案准确率 (60 分)
#
#   线性: 准确率 × 60
#   匹配规则: 精确匹配 (归一化后) + 同义词别名
#   按类别分别统计，便于分析
# ============================================================================

def _evaluate_accuracy(predictions: Dict[str, str]) -> Tuple[int, Dict[str, Any]]:
    details: Dict[str, Any] = {}
    deductions: List[str] = []

    correct = 0
    wrong = 0
    missing = 0
    wrong_samples: List[Dict[str, str]] = []

    # 按类别统计
    cat_stats: Dict[str, Dict[str, int]] = {}

    for rid, gold in GROUND_TRUTH.items():
        cat = rid.split("/")[0]
        if cat not in cat_stats:
            cat_stats[cat] = {"total": 0, "correct": 0, "wrong": 0, "missing": 0}
        cat_stats[cat]["total"] += 1

        if rid not in predictions:
            missing += 1
            cat_stats[cat]["missing"] += 1
            continue

        pred = predictions[rid]
        if _is_match(pred, gold):
            correct += 1
            cat_stats[cat]["correct"] += 1
        else:
            wrong += 1
            cat_stats[cat]["wrong"] += 1
            if len(wrong_samples) < 15:
                wrong_samples.append({"id": rid, "预测": pred, "正确答案": gold})

    accuracy = correct / TOTAL_ITEMS if TOTAL_ITEMS > 0 else 0.0
    score = round(accuracy * 60)

    details["正确数"] = correct
    details["错误数"] = wrong
    details["缺失数"] = missing
    details["准确率"] = f"{accuracy * 100:.1f}%"

    for cat in sorted(cat_stats.keys()):
        s = cat_stats[cat]
        cat_acc = s["correct"] / s["total"] if s["total"] > 0 else 0.0
        details[f"  {cat}"] = f"{s['correct']}/{s['total']} ({cat_acc * 100:.1f}%)"

    if wrong_samples:
        details["错误样例(前15)"] = wrong_samples

    if accuracy < 0.3:
        deductions.append(f"准确率极低 ({accuracy * 100:.1f}%)")
    elif accuracy < 0.5:
        deductions.append(f"准确率低于 50% ({accuracy * 100:.1f}%)")

    return score, {"分数": score, "详情": details, "扣分原因": deductions}


# ============================================================================
# 四、预测质量 (15 分)
#
#   4.1 简洁性 (8分): prediction 应该是简短答案，不含解释
#   4.2 ID 一致性 (4分): 提交的 ID 都在题目范围内
#   4.3 无重复 ID (3分): 不应出现重复 ID
# ============================================================================

def _evaluate_prediction_quality(
    answer_dir: str, predictions: Dict[str, str]
) -> Tuple[int, Dict[str, Any]]:
    score = 0
    details: Dict[str, Any] = {}
    deductions: List[str] = []

    if not predictions:
        return 0, {"分数": 0, "详情": {"错误": "无预测数据"}, "扣分原因": ["无预测数据"]}

    total_preds = len(predictions)

    # ---- 4.1 简洁性 (8分) ----
    long_count = 0
    explanation_count = 0
    empty_count = 0

    for rid, pred in predictions.items():
        stripped = pred.strip()
        if not stripped:
            empty_count += 1
        elif len(stripped) > 10:
            long_count += 1
        if re.search(r"(因为|所以|解释|答案是|谜底是|应该是|我认为|分析|推理)", pred):
            explanation_count += 1

    problem_count = long_count + explanation_count + empty_count
    clean_rate = max(0.0, 1.0 - problem_count / total_preds)
    concise_score = round(clean_rate * 8)
    score += concise_score

    details["4.1 简洁性"] = f"{concise_score}/8"
    if long_count > 0:
        details["  过长预测数"] = long_count
    if explanation_count > 0:
        details["  含解释的预测数"] = explanation_count
        deductions.append(f"{explanation_count} 条预测包含多余解释文字")
    if empty_count > 0:
        details["  空预测数"] = empty_count
        deductions.append(f"{empty_count} 条预测为空")

    # ---- 4.2 ID 一致性 (4分) ----
    valid_ids = sum(1 for rid in predictions if rid in GROUND_TRUTH)
    invalid_ids = total_preds - valid_ids
    id_rate = valid_ids / total_preds if total_preds > 0 else 0.0
    id_score = round(id_rate * 4)
    score += id_score

    details["4.2 ID一致性"] = f"{id_score}/4"
    if invalid_ids > 0:
        details["  无效ID数"] = invalid_ids
        deductions.append(f"{invalid_ids} 个预测 ID 不在题目中")

    # ---- 4.3 无重复 ID (3分) ----
    dup_score = 3
    submission_path = os.path.join(answer_dir, "submission.json")
    try:
        if os.path.isfile(submission_path):
            with open(submission_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
            raw_preds = raw_data.get("predictions", [])
            ids = [p.get("id") for p in raw_preds if isinstance(p, dict)]
            if len(ids) != len(set(ids)):
                dup_count = len(ids) - len(set(ids))
                dup_score = max(0, 3 - dup_count)
                deductions.append(f"存在 {dup_count} 个重复 ID")
    except Exception:
        pass
    score += dup_score
    details["4.3 无重复ID"] = f"{dup_score}/3"

    return score, {"分数": score, "详情": details, "扣分原因": deductions}


# ============================================================================
# 入口: evaluate() + print_report()
# ============================================================================

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
    # 一、文件交付与格式
    s1, r1 = _evaluate_file_delivery(answer_dir)

    # 加载预测数据
    predictions = _load_predictions(answer_dir)

    # 二、覆盖完整性
    s2, r2 = _evaluate_coverage(predictions)

    # 三、答案准确率
    s3, r3 = _evaluate_accuracy(predictions)

    # 四、预测质量
    s4, r4 = _evaluate_prediction_quality(answer_dir, predictions)

    total = min(100, s1 + s2 + s3 + s4)

    # 评语
    if total >= 85:
        comment = "优秀！谜语解答准确率高，提交格式规范。"
    elif total >= 65:
        comment = "良好。大部分谜语解答正确，存在少量错误。"
    elif total >= 45:
        comment = "及格。部分谜语解答正确，但准确率仍有较大提升空间。"
    elif total >= 20:
        comment = "不及格。谜语解答准确率低，请检查解题策略。"
    else:
        comment = "任务完成度严重不足，请检查是否生成了 submission.json 并包含有效预测。"

    report: Dict[str, Any] = {
        "总分": total,
        "评语": comment,
        "分项得分": {
            "文件交付与格式": f"{s1}/10",
            "覆盖完整性": f"{s2}/15",
            "答案准确率": f"{s3}/60",
            "预测质量": f"{s4}/15",
        },
        "一、文件交付与格式 (10分)": r1,
        "二、覆盖完整性 (15分)": r2,
        "三、答案准确率 (60分)": r3,
        "四、预测质量 (15分)": r4,
    }

    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """打印格式化的评分报告"""
    print("=" * 60)
    print("  谜语解谜任务 — 评分报告")
    print("=" * 60)
    print(f"\n  总分: {score}/100")
    print(f"  评语: {report.get('评语', '')}\n")

    scores_summary = report.get("分项得分", {})
    if scores_summary:
        print("  分项得分:")
        for k, v in scores_summary.items():
            print(f"    {k}: {v}")
        print()

    section_keys = [
        "一、文件交付与格式 (10分)",
        "二、覆盖完整性 (15分)",
        "三、答案准确率 (60分)",
        "四、预测质量 (15分)",
    ]

    for key in section_keys:
        section = report.get(key, {})
        if not section:
            continue

        print(f"{'─' * 55}")
        print(f"  【{key}】 得分: {section.get('分数', 0)}")
        print(f"{'─' * 55}")

        details = section.get("详情", {})
        for dk, dv in details.items():
            if isinstance(dv, list):
                print(f"    {dk}:")
                for item in dv[:10]:
                    if isinstance(item, dict):
                        parts = [f"{kk}={vv}" for kk, vv in item.items()]
                        print(f"      - {', '.join(parts)}")
                    else:
                        print(f"      - {item}")
                if len(dv) > 10:
                    print(f"      ... (还有 {len(dv) - 10} 条)")
            else:
                print(f"    {dk}: {dv}")

        deds = section.get("扣分原因", [])
        if deds:
            print("    扣分原因:")
            for d in deds:
                print(f"      - {d}")
        print()

    print("=" * 60)


# ============================================================================
# 直接运行入口
# ============================================================================

if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_dir = sys.argv[1]
    else:
        test_dir = os.path.join(os.path.dirname(__file__), "..", "gpt-5", "attempt_1")

    test_dir = os.path.abspath(test_dir)

    if os.path.exists(test_dir):
        print(f"评估目录: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"目录不存在: {test_dir}")
        sys.exit(0)
