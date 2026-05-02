"""
中国车牌识别系统 — 评分脚本 (rubric.py)

任务: 编写 Python 程序识别中国绿色车牌, 包含 GUI 界面, 测试集 378 张绿色车牌图片.

总分 100 分, 三个维度:
  一、文件交付          10 分
  二、代码质量          20 分
  三、识别准确率        70 分
"""

import os
import re
import ast
import json
import random
import sys
from typing import Tuple, Dict, Any, List, Optional

try:
    import openai
except ImportError:
    openai = None


# ─────────────────────────────────────────────────────────────────────
# 环境 / LLM 辅助
# ─────────────────────────────────────────────────────────────────────

def _load_env(answer_dir: str) -> dict:
    """从 answer_dir 和 query 根目录加载 .env 配置"""
    values: Dict[str, str] = {}
    query_root = os.path.join(os.path.dirname(__file__), "..")
    for d in [answer_dir, query_root]:
        env_path = os.path.join(d, ".env")
        if not os.path.exists(env_path):
            continue
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    k, v = k.strip(), v.strip().strip("'\"")
                    if k not in values:
                        values[k] = v
        except Exception:
            pass
    return values


def _get_text_eval_config(answer_dir: str) -> dict:
    """获取文本评估 LLM 配置"""
    env = _load_env(answer_dir)

    def g(key, default=""):
        return os.environ.get(key) or env.get(key) or default

    return {
        "api_key": g("EVAL_TEXT_API_KEY", g("ANTHROPIC_API_KEY")),
        "api_base": g("EVAL_TEXT_API_BASE_URL", g("ANTHROPIC_BASE_URL")),
        "model": g("EVAL_TEXT_MODEL", "openai/gpt-5.2"),
    }


def _call_llm_judge(prompt: str, config: dict) -> str:
    """调用 LLM 进行文本评估"""
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
    except Exception as e:
        print(f"[RUBRIC] LLM Judge 调用失败: {e}")
        return ""


# ─────────────────────────────────────────────────────────────────────
# CCPD 文件名解码
# ─────────────────────────────────────────────────────────────────────

PROVINCES = "皖沪津渝冀晋蒙辽吉黑苏浙京闽赣鲁豫鄂湘粤桂琼川贵云藏陕甘青宁新"
LETTERS = "ABCDEFGHJKLMNPQRSTUVWXYZ"
CHARS = LETTERS + "0123456789"


def _decode_plate(filepath: str) -> Optional[str]:
    """从 CCPD 文件名解码真实车牌号"""
    try:
        name = os.path.basename(filepath)
        parts = name.split("-")
        if len(parts) < 5:
            return None
        codes = list(map(int, parts[4].split("_")))
        if len(codes) < 3:
            return None
        plate = PROVINCES[codes[0]] + LETTERS[codes[1]]
        for c in codes[2:]:
            plate += CHARS[c]
        return plate
    except Exception:
        return None


# ─────────────────────────────────────────────────────────────────────
# 辅助: 查找主程序文件
# ─────────────────────────────────────────────────────────────────────

def _find_main_py(answer_dir: str) -> Optional[str]:
    """查找 agent 提交的主 Python 程序文件"""
    # 优先精确匹配
    target = os.path.join(answer_dir, "license_plate_recognition.py")
    if os.path.isfile(target):
        return target
    # 模糊匹配
    try:
        all_files = os.listdir(answer_dir)
    except Exception:
        return None
    keywords = ["license", "plate", "recognition", "lpr", "gui", "main", "app"]
    py_files = [f for f in all_files if f.endswith(".py") and not f.startswith(("test_", "eval_", "."))]
    for f in sorted(py_files):
        if any(kw in f.lower() for kw in keywords):
            return os.path.join(answer_dir, f)
    if py_files:
        return os.path.join(answer_dir, py_files[0])
    return None


# ─────────────────────────────────────────────────────────────────────
# 辅助: 查找测试图片目录
# ─────────────────────────────────────────────────────────────────────

def _find_test_images_dir(answer_dir: str) -> Optional[str]:
    """在 answer_dir 及 query 根目录中查找含有 .jpg 图片的 ccpd_green 目录"""
    query_root = os.path.join(os.path.dirname(__file__), "..")
    candidates = [
        os.path.join(answer_dir, "test_images", "ccpd_green"),
        os.path.join(answer_dir, "test_images"),
        os.path.join(answer_dir, "context", "test_images", "ccpd_green"),
        os.path.join(query_root, "context", "test_images", "ccpd_green"),
        os.path.join(query_root, "context", "test_images"),
    ]
    for cand in candidates:
        if os.path.isdir(cand):
            imgs = [f for f in os.listdir(cand) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
            if len(imgs) >= 10:
                return cand
    return None


# ─────────────────────────────────────────────────────────────────────
# 辅助: 标准化车牌文本
# ─────────────────────────────────────────────────────────────────────

def _normalize_plate(text: Optional[str]) -> str:
    """去除车牌中常见的分隔符"""
    if not text:
        return ""
    return re.sub(r"[·.\s\-_]", "", str(text).strip())


# ─────────────────────────────────────────────────────────────────────
# 辅助: 解析 recognition_results.json (兼容多种格式)
# ─────────────────────────────────────────────────────────────────────

def _parse_results_json(filepath: str) -> Dict[str, Dict[str, str]]:
    """
    解析识别结果 JSON, 兼容多种格式.
    返回: { image_basename: { "plate": str, "color": str } }
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return {}

    parsed: Dict[str, Dict[str, str]] = {}

    def _extract_plate(item: dict) -> str:
        for k in ["pred_plate", "plate_number", "plate", "code", "license", "number"]:
            if k in item and item[k]:
                return _normalize_plate(str(item[k]))
        return ""

    def _extract_color(item: dict) -> str:
        for k in ["pred_color", "plate_color", "color"]:
            if k in item and item[k]:
                return str(item[k])
        return ""

    def _extract_filename(item: dict) -> str:
        for k in ["file", "image", "filename", "image_path", "path", "name"]:
            if k in item and item[k]:
                return os.path.basename(str(item[k]))
        return ""

    if isinstance(data, dict):
        # 格式 A: { "results": [...], "summary": {...} }
        if "results" in data and isinstance(data["results"], list):
            for item in data["results"]:
                if not isinstance(item, dict):
                    continue
                bname = _extract_filename(item)
                if bname:
                    parsed[bname] = {
                        "plate": _extract_plate(item),
                        "color": _extract_color(item),
                    }
        # 格式 B: { "samples": [...] }
        elif "samples" in data and isinstance(data["samples"], list):
            for item in data["samples"]:
                if not isinstance(item, dict):
                    continue
                bname = _extract_filename(item)
                inner = item.get("results", [])
                if isinstance(inner, list) and inner:
                    first = inner[0] if isinstance(inner[0], dict) else {}
                    plate = _extract_plate(first) or _extract_plate(item)
                    color = _extract_color(first) or _extract_color(item)
                else:
                    plate = _extract_plate(item)
                    color = _extract_color(item)
                if bname:
                    parsed[bname] = {"plate": plate, "color": color}
        # 格式 C: 扁平字典 { "image.jpg": { "plate_number": ..., ... } }
        else:
            for key, val in data.items():
                if isinstance(val, dict):
                    parsed[os.path.basename(key)] = {
                        "plate": _extract_plate(val),
                        "color": _extract_color(val),
                    }
    elif isinstance(data, list):
        # 格式 D: 顶层数组 [{ "file": ..., "pred_plate": ..., ... }, ...]
        for item in data:
            if not isinstance(item, dict):
                continue
            bname = _extract_filename(item)
            if bname:
                parsed[bname] = {
                    "plate": _extract_plate(item),
                    "color": _extract_color(item),
                }

    return parsed


# ═════════════════════════════════════════════════════════════════════
# 一、文件交付 (10 分)
# ═════════════════════════════════════════════════════════════════════

def _eval_file_delivery(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    1.1 license_plate_recognition.py 存在 (5 分)
    1.2 recognition_results.json 存在 (3 分)
    1.3 主程序 Python 语法正确 (2 分)
    """
    score = 0
    details: Dict[str, str] = {}
    issues: List[str] = []

    try:
        all_files = os.listdir(answer_dir)
    except Exception:
        all_files = []

    py_files = [f for f in all_files if f.endswith(".py") and not f.startswith(("test_", "eval_", "."))]

    # 1.1 主程序文件 (5 分)
    if "license_plate_recognition.py" in all_files:
        score += 5
        details["主程序文件"] = "5/5 — license_plate_recognition.py 存在"
    elif py_files:
        score += 2
        details["主程序文件"] = f"2/5 — 存在 Python 文件 ({py_files[0]}) 但文件名不符"
        issues.append(f"主程序应命名为 license_plate_recognition.py, 实际: {py_files[0]}")
    else:
        details["主程序文件"] = "0/5 — 未找到 Python 程序文件"
        issues.append("缺少 Python 程序文件")

    # 1.2 识别结果 JSON (3 分)
    if "recognition_results.json" in all_files:
        score += 3
        details["识别结果文件"] = "3/3 — recognition_results.json 存在"
    else:
        json_files = [f for f in all_files if f.endswith(".json") and not f.startswith(".")]
        if json_files:
            score += 1
            details["识别结果文件"] = f"1/3 — 存在 JSON ({json_files[0]}) 但名称不符"
        else:
            details["识别结果文件"] = "0/3 — 未找到识别结果文件"

    # 1.3 语法可解析 (2 分)
    py_path = _find_main_py(answer_dir)
    if py_path:
        try:
            with open(py_path, "r", encoding="utf-8", errors="ignore") as f:
                source = f.read()
            ast.parse(source)
            score += 2
            details["语法检查"] = "2/2 — Python 语法正确"
        except SyntaxError as e:
            details["语法检查"] = f"0/2 — 语法错误: {str(e)[:80]}"
            issues.append("代码存在语法错误")
    else:
        details["语法检查"] = "0/2 — 无 Python 文件可检查"

    return score, {"得分": f"{score}/10", "详情": details, "问题": issues}


# ═════════════════════════════════════════════════════════════════════
# 二、代码质量 (20 分)
# ═════════════════════════════════════════════════════════════════════

def _eval_code_quality(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    2.1 GUI 实现 (6 分)
    2.2 OCR/识别库 (5 分)
    2.3 图像处理库 (4 分)
    2.4 批量模式 (3 分)
    2.5 颜色识别逻辑 (2 分)
    """
    py_path = _find_main_py(answer_dir)
    if not py_path:
        return 0, {"得分": "0/20", "详情": {"错误": "无 Python 文件"}, "问题": ["缺少代码文件"]}

    try:
        with open(py_path, "r", encoding="utf-8", errors="ignore") as f:
            code = f.read()
    except Exception:
        return 0, {"得分": "0/20", "详情": {"错误": "读取失败"}, "问题": ["代码文件读取失败"]}

    score = 0
    details: Dict[str, str] = {}
    issues: List[str] = []

    # 2.1 GUI 实现 (6 分)
    gui_libs = {
        "tkinter": bool(re.search(r"import\s+tkinter|from\s+tkinter", code)),
        "PyQt": bool(re.search(r"import\s+PyQt|from\s+PyQt", code)),
        "gradio": bool(re.search(r"import\s+gradio|from\s+gradio", code)),
        "streamlit": bool(re.search(r"import\s+streamlit|from\s+streamlit", code)),
        "wx": bool(re.search(r"import\s+wx|from\s+wx", code)),
    }
    found_gui = [k for k, v in gui_libs.items() if v]

    gui_features = {
        "文件选择": bool(re.search(r"filedialog|askopenfilename|QFileDialog|upload|browse|file_uploader", code, re.IGNORECASE)),
        "图像显示": bool(re.search(r"PhotoImage|QPixmap|Label|Canvas|imshow|Image\.open|ImageTk", code)),
        "交互按钮": bool(re.search(r"Button|QPushButton|st\.button|command\s*=", code)),
    }
    feat_count = sum(1 for v in gui_features.values() if v)

    if found_gui and feat_count >= 2:
        score += 6
        details["GUI 实现"] = f"6/6 — 使用 {', '.join(found_gui)}, {feat_count}/3 项交互功能"
    elif found_gui and feat_count >= 1:
        score += 4
        details["GUI 实现"] = f"4/6 — 使用 {', '.join(found_gui)}, 仅 {feat_count}/3 项功能"
    elif found_gui:
        score += 2
        details["GUI 实现"] = f"2/6 — 导入了 {', '.join(found_gui)} 但交互功能不完整"
        issues.append("GUI 交互功能不完整")
    else:
        details["GUI 实现"] = "0/6 — 未发现 GUI 库导入"
        issues.append("缺少 GUI 实现")

    # 2.2 OCR/识别库 (5 分)
    ocr_libs = {
        "HyperLPR3": bool(re.search(r"hyperlpr|LicensePlateCatcher|lpr3", code, re.IGNORECASE)),
        "PaddleOCR": bool(re.search(r"paddleocr|PaddleOCR", code, re.IGNORECASE)),
        "EasyOCR": bool(re.search(r"easyocr|EasyOCR", code, re.IGNORECASE)),
        "Tesseract": bool(re.search(r"tesseract|pytesseract", code, re.IGNORECASE)),
    }
    found_ocr = [k for k, v in ocr_libs.items() if v]

    if "HyperLPR3" in found_ocr:
        score += 5
        details["OCR 库"] = "5/5 — 使用推荐的 HyperLPR3"
    elif found_ocr:
        score += 3
        details["OCR 库"] = f"3/5 — 使用 {', '.join(found_ocr)} (非推荐)"
    elif re.search(r"ocr|recognize|detect.*plate", code, re.IGNORECASE):
        score += 1
        details["OCR 库"] = "1/5 — 有识别相关代码但未使用主流 OCR 库"
    else:
        details["OCR 库"] = "0/5 — 未发现 OCR/车牌识别代码"
        issues.append("缺少 OCR/车牌识别实现")

    # 2.3 图像处理库 (4 分)
    has_cv2 = bool(re.search(r"import\s+cv2|from\s+cv2", code))
    has_pil = bool(re.search(r"from\s+PIL|import\s+PIL", code, re.IGNORECASE))
    has_np = bool(re.search(r"import\s+numpy|from\s+numpy", code))
    has_color_detect = bool(re.search(r"HSV|cvtColor|inRange|COLOR_BGR2HSV|color_detect", code))
    has_crop = bool(re.search(r"crop|roi|region|bounding|contour|rectangle", code, re.IGNORECASE))

    img_score = min(4, sum([has_cv2, has_pil, has_np]) + (1 if has_color_detect else 0) + (1 if has_crop else 0))
    score += img_score
    libs = []
    if has_cv2:
        libs.append("OpenCV")
    if has_pil:
        libs.append("PIL")
    if has_np:
        libs.append("NumPy")
    extras = []
    if has_color_detect:
        extras.append("颜色检测")
    if has_crop:
        extras.append("区域提取")
    detail_str = f"{img_score}/4 — 库: {', '.join(libs) or '无'}"
    if extras:
        detail_str += f", 功能: {', '.join(extras)}"
    details["图像处理"] = detail_str

    # 2.4 批量模式 (3 分)
    has_batch_arg = bool(re.search(r"--batch|argparse.*batch|batch_mode", code, re.IGNORECASE))
    has_json_output = bool(re.search(r"recognition_results|json\.dump|json_output", code, re.IGNORECASE))

    if has_batch_arg and has_json_output:
        score += 3
        details["批量模式"] = "3/3 — 支持 --batch 参数和 JSON 输出"
    elif has_batch_arg or has_json_output:
        score += 1
        details["批量模式"] = "1/3 — 部分实现批量模式"
    else:
        details["批量模式"] = "0/3 — 未实现批量识别模式"

    # 2.5 颜色识别逻辑 (2 分)
    color_patterns = [r"绿色|蓝色|黄色", r"green|blue|yellow", r"HSV|inRange|颜色|color"]
    color_hits = sum(1 for pat in color_patterns if re.search(pat, code, re.IGNORECASE))
    if color_hits >= 2:
        score += 2
        details["颜色识别"] = "2/2 — 包含颜色识别逻辑"
    elif color_hits >= 1:
        score += 1
        details["颜色识别"] = "1/2 — 部分颜色识别逻辑"
    else:
        details["颜色识别"] = "0/2 — 未发现颜色识别逻辑"

    return score, {"得分": f"{score}/20", "详情": details, "问题": issues}


# ═════════════════════════════════════════════════════════════════════
# 三、识别准确率 (70 分)
# ═════════════════════════════════════════════════════════════════════

def _find_results_json(answer_dir: str) -> Optional[str]:
    """查找识别结果 JSON 文件"""
    for name in ["recognition_results.json", "results.json", "output.json", "batch_results.json"]:
        p = os.path.join(answer_dir, name)
        if os.path.isfile(p):
            return p
    try:
        for f in sorted(os.listdir(answer_dir)):
            if f.endswith(".json") and not f.startswith("."):
                return os.path.join(answer_dir, f)
    except Exception:
        pass
    return None


def _eval_accuracy(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    评估识别准确率 (70 分).
    优先用 recognition_results.json 做量化评估;
    若不存在, 退化为 LLM 代码审查 (上限 35/70).
    """
    results_file = _find_results_json(answer_dir)
    test_img_dir = _find_test_images_dir(answer_dir)

    if not results_file or not test_img_dir:
        return _eval_accuracy_fallback(answer_dir)

    predictions = _parse_results_json(results_file)
    if not predictions:
        return _eval_accuracy_fallback(answer_dir)

    # 收集测试图片列表
    test_images: List[str] = []
    for root, _, files in os.walk(test_img_dir):
        for f in files:
            if f.lower().endswith((".jpg", ".jpeg", ".png")):
                test_images.append(os.path.join(root, f))

    if not test_images:
        return _eval_accuracy_fallback(answer_dir)

    # 随机采样 200 张 (固定种子保证可复现)
    random.seed(42)
    sample_size = min(200, len(test_images))
    samples = random.sample(test_images, sample_size)

    # 逐张对比评分
    color_correct = 0
    province_correct = 0
    rest_correct = 0
    full_correct = 0
    matched_count = 0
    total_weighted = 0.0
    sample_details: List[Dict[str, Any]] = []

    for img_path in samples:
        img_name = os.path.basename(img_path)
        gt_plate = _decode_plate(img_path)
        if gt_plate is None:
            continue

        # 查找预测结果 (尝试多种匹配方式)
        pred = predictions.get(img_name)
        if pred is None:
            for k in predictions:
                if os.path.basename(k) == img_name:
                    pred = predictions[k]
                    break

        if pred is None:
            sample_details.append({
                "image": img_name, "gt": gt_plate,
                "pred": "", "color": "", "weighted": 0.0,
            })
            continue

        matched_count += 1
        pred_plate = _normalize_plate(pred.get("plate", ""))
        pred_color = pred.get("color", "")

        w = 0.0

        # 颜色 (权重 0.15) — 全部应为绿色
        if pred_color and ("绿" in pred_color or "green" in pred_color.lower()):
            w += 0.15
            color_correct += 1

        # 省份汉字 (权重 0.20)
        if pred_plate and gt_plate and len(pred_plate) >= 1 and pred_plate[0] == gt_plate[0]:
            w += 0.20
            province_correct += 1

        # 城市字母 + 其余字符 (权重 0.65)
        if len(pred_plate) > 1 and len(gt_plate) > 1 and pred_plate[1:] == gt_plate[1:]:
            w += 0.65
            rest_correct += 1

        if pred_plate == gt_plate:
            full_correct += 1

        total_weighted += w
        sample_details.append({
            "image": img_name, "gt": gt_plate,
            "pred": pred_plate, "color": pred_color,
            "weighted": round(w, 2),
        })

    # 计算最终分数
    avg_weighted = total_weighted / sample_size if sample_size > 0 else 0.0
    raw_score = avg_weighted * 70.0

    # 覆盖率惩罚: 若匹配到结果的比例 < 50%, 线性降低
    coverage = matched_count / sample_size if sample_size > 0 else 0.0
    if coverage < 0.5:
        raw_score *= coverage * 2.0

    final_score = min(70, max(0, round(raw_score)))

    # 统计信息
    def _pct(n: int) -> str:
        return f"{n}/{sample_size} ({n / sample_size * 100:.1f}%)" if sample_size > 0 else "N/A"

    stats = {
        "采样数": sample_size,
        "匹配结果数": matched_count,
        "覆盖率": f"{coverage * 100:.1f}%",
        "颜色正确": _pct(color_correct),
        "省份正确": _pct(province_correct),
        "城市+字符正确": _pct(rest_correct),
        "完全匹配": _pct(full_correct),
        "加权平均": round(avg_weighted, 4),
        "示例 (前5)": sample_details[:5],
    }

    # 准确率等级
    full_acc = full_correct / sample_size if sample_size > 0 else 0.0
    if full_acc >= 0.85:
        level = "优秀 (>=85%)"
    elif full_acc >= 0.60:
        level = "良好 (>=60%)"
    elif full_acc >= 0.30:
        level = "一般 (>=30%)"
    else:
        level = "较差 (<30%)"

    details: Dict[str, Any] = {"量化评估": stats, "准确率等级": level}
    issues: List[str] = []
    if full_acc < 0.30:
        issues.append("车牌识别准确率较低")

    return final_score, {"得分": f"{final_score}/70", "详情": details, "问题": issues}


def _eval_accuracy_fallback(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    无 recognition_results.json 时的退化评估 (上限 35/70).
    先尝试 LLM 代码审查, 再退化为正则检查.
    """
    details: Dict[str, Any] = {}
    issues: List[str] = ["未找到可用的识别结果文件或测试图片, 退化为代码审查 (上限35/70)"]

    py_path = _find_main_py(answer_dir)
    if not py_path:
        return 0, {"得分": "0/70", "详情": {"错误": "无代码, 无结果文件"}, "问题": issues}

    try:
        with open(py_path, "r", encoding="utf-8", errors="ignore") as f:
            code = f.read()
    except Exception:
        return 0, {"得分": "0/70", "详情": {"错误": "代码读取失败"}, "问题": issues}

    # 尝试 LLM-as-Judge
    config = _get_text_eval_config(answer_dir)
    llm_score = None

    if config.get("api_key"):
        prompt = f"""你是一个严格的代码评审专家。请评估以下中国车牌识别系统的 Python 代码。

任务要求:
1. GUI 界面让用户选择车牌图像并展示识别结果
2. 车牌区域定位和提取
3. 车牌颜色识别 (绿色)
4. 车牌文字识别 (省份汉字 + 城市字母 + 其余字符)
5. 支持 --batch 批量模式, 输出 recognition_results.json
6. 推荐使用 HyperLPR3, 准确率目标 >=85%

请从以下维度打分 (满分 35 分):
- 车牌定位/提取实现 (0-8分): 是否有合理的车牌定位逻辑
- 颜色识别实现 (0-5分): 是否能识别车牌颜色
- 文字识别实现 (0-12分): OCR 选择是否合理, 是否处理中文省份汉字
- 批量模式 (0-5分): 是否支持批量处理和结果输出
- 代码工程质量 (0-5分): 错误处理、模块化、可运行性

请严格按 JSON 格式回复:
```json
{{"plate_detection": 0, "color_recognition": 0, "text_recognition": 0, "batch_mode": 0, "engineering": 0, "total": 0, "comment": ""}}
```

代码 (截取前 15000 字符):
```python
{code[:15000]}
```"""

        raw = _call_llm_judge(prompt, config)
        if raw:
            try:
                if "```json" in raw:
                    raw = raw.split("```json")[1].split("```")[0].strip()
                elif "```" in raw:
                    raw = raw.split("```")[1].split("```")[0].strip()
                result = json.loads(raw)
                llm_score = max(0, min(35, int(result.get("total", 0))))
                details["LLM 代码审查"] = result
            except Exception:
                pass

    # 正则退化
    if llm_score is None:
        regex_score = 0
        checks = {
            "OCR 库": bool(re.search(r"hyperlpr|paddleocr|easyocr|tesseract|ocr", code, re.IGNORECASE)),
            "颜色识别": bool(re.search(r"HSV|颜色|color|绿色|蓝色|黄色|green|blue|yellow", code, re.IGNORECASE)),
            "GUI": bool(re.search(r"tkinter|PyQt|gradio|streamlit", code, re.IGNORECASE)),
            "批量模式": bool(re.search(r"--batch|batch|json\.dump", code, re.IGNORECASE)),
            "省份处理": bool(re.search(r"皖沪津渝|provinces|省份", code)),
        }
        for k, v in checks.items():
            if v:
                regex_score += 5
        regex_score = min(25, regex_score)  # 正则上限更低
        details["正则代码审查"] = {k: ("有" if v else "无") for k, v in checks.items()}
        llm_score = regex_score

    final = min(35, llm_score)
    return final, {"得分": f"{final}/70 (退化评估, 上限35)", "详情": details, "问题": issues}


# ═════════════════════════════════════════════════════════════════════
# 主入口
# ═════════════════════════════════════════════════════════════════════

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    评估 agent 的输出.

    Args:
        answer_dir: agent 输出目录的绝对路径

    Returns:
        (score, report) — score: 0-100 整数, report: 详细评估报告
    """
    s1, r1 = _eval_file_delivery(answer_dir)
    s2, r2 = _eval_code_quality(answer_dir)
    s3, r3 = _eval_accuracy(answer_dir)

    total = s1 + s2 + s3

    report: Dict[str, Any] = {
        "总分": total,
        "分项得分": {
            "文件交付": f"{s1}/10",
            "代码质量": f"{s2}/20",
            "识别准确率": f"{s3}/70",
        },
        "详情": {
            "一、文件交付 (10分)": r1,
            "二、代码质量 (20分)": r2,
            "三、识别准确率 (70分)": r3,
        },
        "评语": "",
    }

    if total >= 90:
        report["评语"] = "优秀! 程序完整, 识别准确率高, GUI 功能齐全."
    elif total >= 75:
        report["评语"] = "良好. 核心功能完整, 识别效果较好."
    elif total >= 60:
        report["评语"] = "及格. 基本完成任务但识别准确率或功能有不足."
    elif total >= 40:
        report["评语"] = "部分完成. 有一定实现但关键功能缺失或准确率低."
    else:
        report["评语"] = "不及格. 任务完成度严重不足."

    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """打印格式化的评分报告"""
    print("=" * 70)
    print("中国车牌识别系统 — 评分报告")
    print("=" * 70)
    print(f"\n总分: {score}/100\n")

    scores = report.get("分项得分", {})
    if scores:
        print("分项得分:")
        for k, v in scores.items():
            print(f"  {k}: {v}")

    for section, content in report.get("详情", {}).items():
        print(f"\n{'─' * 50}")
        print(f"【{section}】")
        print(f"{'─' * 50}")
        if isinstance(content, dict):
            _print_nested(content, indent=2)
        else:
            print(f"  {content}")

    print(f"\n{'=' * 50}")
    print(f"评语: {report.get('评语', '')}")
    print("=" * 70)


def _print_nested(d: dict, indent: int = 0) -> None:
    """递归打印嵌套字典"""
    prefix = " " * indent
    for k, v in d.items():
        if isinstance(v, dict):
            print(f"{prefix}{k}:")
            _print_nested(v, indent + 2)
        elif isinstance(v, list):
            print(f"{prefix}{k}:")
            for item in v[:10]:
                if isinstance(item, dict):
                    _print_nested(item, indent + 4)
                    print(f"{' ' * (indent + 4)}---")
                else:
                    print(f"{prefix}  - {item}")
        else:
            print(f"{prefix}{k}: {v}")


# ═════════════════════════════════════════════════════════════════════
# CLI
# ═════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_dir = sys.argv[1]
    else:
        test_dir = os.path.join(os.path.dirname(__file__), "..", "workspace")

    if not os.path.isabs(test_dir):
        test_dir = os.path.join(os.path.dirname(__file__), "..", test_dir)

    if os.path.exists(test_dir):
        print(f"评估目录: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"目录不存在: {test_dir}")
    sys.exit(0)
