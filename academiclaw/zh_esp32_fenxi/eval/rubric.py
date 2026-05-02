"""
pengyichen-query3 评分标准 (Rubric) — 从零重写
任务：代码功能识别与分析报告生成 - ESP32多媒体运动传感系统

总分：100 分

评分维度：
一、文件交付与基本完整性 (15分) — 程序化检查
    1.1 报告文件存在且格式合理 (5分)
    1.2 必需的 7 个章节存在 (10分)

二、技术关键词深度 (10分) — 程序化检查
    检查报告中对硬件型号、协议名称等核心技术术语的覆盖

三、内容覆盖性 (30分) — LLM-as-Judge
    3.1 功能模块覆盖 (10分)
    3.2 技术细节覆盖 (10分)
    3.3 问题分析与优化建议覆盖 (10分)

四、文档质量 (45分) — LLM-as-Judge
    4.1 技术准确性 (15分)
    4.2 结构逻辑性 (12分)
    4.3 实用价值 (10分)
    4.4 表达规范性 (8分)
"""

import os
import re
import json
from typing import Tuple, Dict, Any, List

try:
    import openai
except ImportError:
    openai = None


# =============================================================================
# 环境与 LLM 配置
# =============================================================================

def _load_env(answer_dir: str) -> dict:
    """从 answer_dir 和 query 根目录加载 .env 配置"""
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
        print("[RUBRIC] LLM Judge 调用失败: %s" % e)
        return ""


def _parse_json_from_llm(text: str) -> dict:
    """从 LLM 返回中提取 JSON"""
    if not text:
        return {}
    try:
        m = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
        if m:
            return json.loads(m.group(1))
        m2 = re.search(r"\{.*\}", text, re.DOTALL)
        if m2:
            return json.loads(m2.group(0))
        return json.loads(text)
    except (json.JSONDecodeError, ValueError):
        return {}


# =============================================================================
# 辅助函数
# =============================================================================

def _find_report(answer_dir: str) -> str:
    """在 answer_dir 中查找技术分析报告（.md 或 .txt），返回拼接文本"""
    parts = []
    if not os.path.isdir(answer_dir):
        return ""
    for root, dirs, files in os.walk(answer_dir):
        dirs[:] = [d for d in dirs if d not in {
            "__pycache__", ".sii", "context", "node_modules", ".git"
        }]
        for f in sorted(files):
            low = f.lower()
            # 跳过任务描述和评估反馈文件
            if low in ("query.md", "readme.md", "task_prompt.md"):
                continue
            if "evaluation_feedback" in low:
                continue
            if low.endswith(".md") or (low.endswith(".txt") and "evaluation" not in low):
                path = os.path.join(root, f)
                try:
                    with open(path, "r", encoding="utf-8") as fh:
                        content = fh.read()
                    if content.strip():
                        parts.append(content)
                except Exception:
                    pass
    return "\n\n".join(parts)


def _load_source_code_summary() -> str:
    """从 context/Code 加载代码摘要供 LLM 验证技术准确性"""
    query_root = os.path.join(os.path.dirname(os.path.dirname(__file__)))
    code_dir = os.path.join(query_root, "context", "Code")
    if not os.path.isdir(code_dir):
        return ""
    parts = []
    exts = {".cpp", ".c", ".h", ".ino"}
    for root, dirs, files in os.walk(code_dir):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for f in sorted(files):
            _, ext = os.path.splitext(f)
            if ext.lower() in exts:
                path = os.path.join(root, f)
                try:
                    with open(path, "r", encoding="utf-8", errors="replace") as fh:
                        text = fh.read()
                    # 截取每个文件前 2500 字符
                    parts.append("=== %s ===\n%s" % (f, text[:2500]))
                except Exception:
                    pass
    return "\n\n".join(parts)[:10000]


# =============================================================================
# 一、文件交付与基本完整性 (15分) — 程序化检查
# =============================================================================

def _evaluate_delivery(answer_dir: str) -> Tuple[float, Dict[str, Any]]:
    score = 0.0
    details = {}
    deductions = []

    content = _find_report(answer_dir)

    # --- 1.1 报告文件存在且格式合理 (5分) ---
    if not content:
        details["1.1 报告文件"] = "0/5 - 未找到报告文件（.md 或 .txt）"
        deductions.append("未找到技术分析报告文件")
        return 0, {"分数": 0, "详情": details, "扣分原因": deductions}

    char_count = len(content)
    if char_count >= 5000:
        file_score = 5
    elif char_count >= 2000:
        file_score = 3
    elif char_count >= 500:
        file_score = 1
    else:
        file_score = 0
        deductions.append("报告内容过短（%d 字符）" % char_count)
    score += file_score
    details["1.1 报告文件 (5分)"] = "%d/5 - 约 %d 字符" % (file_score, char_count)

    # --- 1.2 必需的 7 个章节存在 (10分) ---
    # description.json 明确要求 7 个章节, 每个约 1.4 分
    required_sections = [
        ("系统概述", 1.5),
        ("硬件架构", 1.5),
        ("软件模块", 1.5),
        ("核心算法", 1.5),
        ("性能评估", 1.5),
        ("优化建议", 1.5),
        ("总结", 1.0),
    ]
    section_details = {}
    section_score = 0.0
    content_lower = content.lower()
    for section_name, pts in required_sections:
        found = False
        # 模糊匹配：章节名前两个字或完整名
        variants = [section_name]
        if len(section_name) >= 4:
            variants.append(section_name[:2])
        for variant in variants:
            if variant in content:
                found = True
                break
        if found:
            section_score += pts
            section_details[section_name] = "%.1f/%.1f - 存在" % (pts, pts)
        else:
            section_details[section_name] = "0/%.1f - 缺失" % pts
            deductions.append("缺少章节: %s" % section_name)

    score += section_score
    details["1.2 必需章节 (10分)"] = section_details

    score = min(score, 15)
    return score, {"分数": score, "详情": details, "扣分原因": deductions}


# =============================================================================
# 二、技术关键词深度 (10分) — 程序化检查
# =============================================================================

def _evaluate_keywords(answer_dir: str) -> Tuple[float, Dict[str, Any]]:
    content = _find_report(answer_dir)
    if not content:
        return 0, {"分数": 0, "详情": {"错误": "无报告内容"}, "扣分原因": ["报告不存在"]}

    # 核心硬件型号与协议关键词, 每个有固定分值
    keywords_map = {
        # 硬件型号 (高权重)
        "ESP32": 1.5,
        "QMI8658": 1.5,
        "ES8311": 1.0,
        "ST7735": 1.0,
        # 通信协议
        "I2C": 0.5,
        "I2S": 0.5,
        "SPI": 0.5,
        # 功能关键词
        "蓝牙": 0.5,
        "IMU": 0.5,
        "Edge Impulse": 1.0,
        "PWM": 0.5,
        "Wi-Fi": 0.5,
    }

    found_kws = []
    kw_score = 0.0
    content_lower = content.lower()
    for kw, pts in keywords_map.items():
        if kw.lower() in content_lower:
            kw_score += pts
            found_kws.append(kw)

    kw_score = min(kw_score, 10)
    details = "%.1f/10 - 找到: %s" % (kw_score, ", ".join(found_kws) if found_kws else "无")
    deductions = []
    if kw_score < 4:
        deductions.append("技术关键词覆盖严重不足（%.1f/10）" % kw_score)
    elif kw_score < 6:
        deductions.append("技术关键词覆盖不足（%.1f/10）" % kw_score)

    return kw_score, {"分数": kw_score, "详情": {"技术关键词": details}, "扣分原因": deductions}


# =============================================================================
# 三、内容覆盖性 (30分) — LLM-as-Judge
# =============================================================================

def _evaluate_coverage(answer_dir: str) -> Tuple[float, Dict[str, Any]]:
    content = _find_report(answer_dir)
    if not content:
        return 0, {"分数": 0, "详情": {"错误": "无报告内容"}, "扣分原因": ["报告不存在"]}

    config = _get_text_eval_config(answer_dir)
    code_summary = _load_source_code_summary()

    prompt = """你是嵌入式系统领域的技术评审专家。你需要评估一份 ESP32 多媒体运动传感系统的技术分析报告对项目功能模块的覆盖程度。

## 项目背景
该项目基于 ESP32-S3, 由两个端组成:
- 端A (手势识别端): ESP32-S3 + QMI8658 IMU + ST7735S TFT + ES8311 音频 + 蓝牙主机 + Wi-Fi。采集 IMU 数据, 调用 Edge Impulse 推理, 通过蓝牙发送控制指令。
- 端B (小车执行端): ESP32-S3 + 蓝牙从机 + TFT 显示 + 双路电机驱动。

源代码文件:
- guestureTimer.cpp: IMU 采集 + Edge Impulse 推理 + 蓝牙主机
- Blink.cpp: TFT 显示 + Wi-Fi/MP3 播放 + ES8311/I2S 初始化
- canon.c: PCM 原始音频数据
- 2024122612.ino: 蓝牙从机 + 电机控制 + TFT 显示

## 项目源代码摘要 (用于验证覆盖性):
%s

## 待评估的技术报告 (截取前 6000 字符):
%s

## 评估维度 (总共 30 分):

### 3.1 功能模块覆盖 (0-10分)
是否覆盖了以下核心模块:
- 音频子系统 (ES8311 编解码, I2S 接口, MP3 播放): 0-2分
- 显示子系统 (ST7735S TFT, SPI): 0-2分
- 运动传感子系统 (QMI8658 IMU, 定时采样, 手势识别): 0-2分
- 蓝牙通信 (SPP 协议, 主从机, 指令传输): 0-2分
- 小车执行端 (电机控制, 命令解析): 0-2分

### 3.2 技术细节覆盖 (0-10分)
- 硬件接口引脚配置 (I2C SDA/SCL, I2S BCLK/WS/DOUT, SPI CS/DC/MOSI/SCLK): 0-3分
- 通信协议参数 (采样率, I2C 地址, Wi-Fi 配置): 0-3分
- 软件架构 (文件组织, 模块划分, 定时器+信号量模式): 0-2分
- 算法实现 (Edge Impulse 推理流程, 数据窗口组织): 0-2分

### 3.3 问题分析与优化建议覆盖 (0-10分)
- 对现有代码问题的识别 (如 delay() 阻塞, 硬编码, 缺乏错误处理): 0-4分
- 优化建议的具体性与可行性: 0-3分
- 性能/资源评估 (内存, Flash, 功耗): 0-3分

请严格按以下 JSON 格式回复:
```json
{
  "功能模块覆盖": {"score": 0, "reason": ""},
  "技术细节覆盖": {"score": 0, "reason": ""},
  "问题分析与优化": {"score": 0, "reason": ""},
  "total": 0
}
```""" % (code_summary[:5000] if code_summary else "代码摘要不可用", content[:6000])

    result_text = _call_llm_judge(prompt, config)
    result = _parse_json_from_llm(result_text)

    if result:
        dims = [
            ("功能模块覆盖", 10),
            ("技术细节覆盖", 10),
            ("问题分析与优化", 10),
        ]
        score = 0.0
        details = {}
        for dim_name, max_pts in dims:
            dim_data = result.get(dim_name, {})
            raw = dim_data.get("score", 0)
            if isinstance(raw, str):
                try:
                    raw = float(raw)
                except ValueError:
                    raw = 0
            dim_score = max(0, min(int(raw), max_pts))
            score += dim_score
            reason = dim_data.get("reason", "")
            details[dim_name] = "%d/%d - %s" % (dim_score, max_pts, reason)
        score = min(score, 30)
        return score, {"分数": score, "详情": details, "扣分原因": []}

    # Fallback: 关键词计数
    return _coverage_fallback(content)


def _coverage_fallback(content: str) -> Tuple[float, Dict[str, Any]]:
    """LLM 不可用时的降级覆盖性评估"""
    coverage_kws = {
        # 功能模块 (每个 2 分)
        "音频": 2, "显示": 2, "传感": 2, "蓝牙": 2, "电机": 2,
        # 技术细节 (每个 1 分)
        "ES8311": 1, "ST7735": 1, "QMI8658": 1, "SPI": 1,
        "I2C": 1, "I2S": 1, "采样率": 1, "引脚": 1,
        # 优化建议相关 (每个 1 分)
        "优化": 1, "问题": 1, "建议": 1, "改进": 1,
        "功耗": 1, "内存": 1, "延迟": 1,
    }
    found = []
    kw_score = 0
    for kw, pts in coverage_kws.items():
        if kw in content:
            kw_score += pts
            found.append(kw)
    score = min(kw_score, 30)
    return score, {
        "分数": score,
        "详情": {"降级评估": "%d/30 - 关键词: %s" % (score, ", ".join(found))},
        "扣分原因": ["LLM 不可用，使用关键词降级评估"],
    }


# =============================================================================
# 四、文档质量 (45分) — LLM-as-Judge
# =============================================================================

def _evaluate_quality(answer_dir: str) -> Tuple[float, Dict[str, Any]]:
    content = _find_report(answer_dir)
    if not content:
        return 0, {"分数": 0, "详情": {"错误": "无报告内容"}, "扣分原因": ["报告不存在"]}

    config = _get_text_eval_config(answer_dir)
    code_summary = _load_source_code_summary()

    prompt = """你是嵌入式系统领域的资深技术评审专家。你需要评估一份 ESP32 多媒体运动传感系统的技术分析报告质量。

## 项目背景
该项目基于 ESP32-S3 平台, 实现了手势识别与小车控制的端到端嵌入式系统:
- 核心硬件: ESP32-S3 + QMI8658 IMU + ES8311 音频编解码 + ST7735S TFT
- 通信方式: I2C, I2S, SPI, 蓝牙 SPP, Wi-Fi
- 核心功能: IMU 数据采集 → Edge Impulse 推理 → 蓝牙指令 → 小车控制
- 多媒体: HTTP MP3 流播放, TFT 图形显示

## 项目源代码摘要 (用于验证技术准确性):
%s

## 待评估的技术报告 (截取前 8000 字符):
%s

## 请从以下 4 个维度评分 (总共 45 分):

### A. 技术准确性 (0-15分)
- 硬件接口描述 (引脚号、协议参数) 是否与源代码一致
- 软件模块分析是否正确反映了代码逻辑
- 技术术语使用是否准确
- 是否存在明显的技术错误或臆造内容

评分标准:
- 13-15: 技术描述全面准确, 与代码高度吻合, 无明显错误
- 9-12: 基本准确, 少量不精确之处
- 5-8: 有一些技术错误或含糊描述
- 0-4: 技术描述有严重错误或大量臆造

### B. 结构逻辑性 (0-12分)
- 章节组织是否符合技术报告规范 (概述→架构→详细→评估→建议→总结)
- 内容层次是否清晰, 各章节之间是否有逻辑衔接
- 分析是否有足够的深度, 不是流于表面的罗列

评分标准:
- 10-12: 结构清晰完善, 逻辑严密, 层次分明
- 7-9: 结构基本合理, 少量章节衔接不佳
- 4-6: 结构粗糙, 逻辑不够清晰
- 0-3: 结构混乱或过于简略

### C. 实用价值 (0-10分)
- 优化建议是否具体可行 (如能指出具体函数/模块)
- 问题分析是否有针对性 (能点出代码中的具体问题)
- 性能评估是否有参考价值
- 是否具备工程指导意义

评分标准:
- 8-10: 建议具体可行, 紧扣代码, 有工程参考价值
- 5-7: 建议基本合理, 部分较笼统
- 2-4: 建议过于泛化或缺乏实际操作性
- 0-1: 基本没有实用价值

### D. 表达规范性 (0-8分)
- Markdown 格式是否规范 (标题层级、代码块、列表)
- 语言表达是否清晰专业
- 是否恰当引用了代码片段作为技术分析的佐证
- 技术参数是否以适当形式展示 (表格、列表等)

评分标准:
- 7-8: 格式规范, 表达清晰专业, 善用代码引用和结构化展示
- 5-6: 格式基本规范, 少量表达不够精炼
- 3-4: 格式粗糙, 表达含糊
- 0-2: 格式混乱, 表达不规范

请严格按以下 JSON 格式回复:
```json
{
  "技术准确性": {"score": 0, "reason": ""},
  "结构逻辑性": {"score": 0, "reason": ""},
  "实用价值": {"score": 0, "reason": ""},
  "表达规范性": {"score": 0, "reason": ""},
  "total": 0
}
```""" % (code_summary[:5000] if code_summary else "代码摘要不可用", content[:8000])

    result_text = _call_llm_judge(prompt, config)
    result = _parse_json_from_llm(result_text)

    if result:
        dims = [
            ("技术准确性", 15),
            ("结构逻辑性", 12),
            ("实用价值", 10),
            ("表达规范性", 8),
        ]
        score = 0.0
        details = {}
        for dim_name, max_pts in dims:
            dim_data = result.get(dim_name, {})
            raw = dim_data.get("score", 0)
            if isinstance(raw, str):
                try:
                    raw = float(raw)
                except ValueError:
                    raw = 0
            dim_score = max(0, min(int(raw), max_pts))
            score += dim_score
            reason = dim_data.get("reason", "")
            details[dim_name] = "%d/%d - %s" % (dim_score, max_pts, reason)
        score = min(score, 45)
        return score, {"分数": score, "详情": details, "扣分原因": []}

    # Fallback
    return _quality_fallback(content)


def _quality_fallback(content: str) -> Tuple[float, Dict[str, Any]]:
    """LLM 不可用时的降级质量评估"""
    score = 0.0
    details = {}

    char_count = len(content)

    # A. 内容充实度代替技术准确性 (0-15)
    if char_count >= 8000:
        a = 10
    elif char_count >= 4000:
        a = 7
    elif char_count >= 2000:
        a = 4
    else:
        a = 1
    score += a
    details["技术准确性(降级-按篇幅)"] = "%d/15 - 约 %d 字符" % (a, char_count)

    # B. 结构逻辑性 - 标题层级 (0-12)
    h2_count = len(re.findall(r"^#{2}\s", content, re.MULTILINE))
    h3_count = len(re.findall(r"^#{3}\s", content, re.MULTILINE))
    total_headings = h2_count + h3_count
    if total_headings >= 15:
        b = 10
    elif total_headings >= 10:
        b = 7
    elif total_headings >= 5:
        b = 4
    else:
        b = 1
    score += b
    details["结构逻辑性(降级-按标题)"] = "%d/12 - %d 个二/三级标题" % (b, total_headings)

    # C. 实用价值 - 建议相关关键词 (0-10)
    practical_kws = ["建议", "优化", "改进", "问题", "缺陷", "不足",
                     "方案", "应该", "可以考虑", "推荐"]
    p_count = sum(1 for kw in practical_kws if kw in content)
    if p_count >= 6:
        c = 7
    elif p_count >= 3:
        c = 4
    else:
        c = 1
    score += c
    details["实用价值(降级-按关键词)"] = "%d/10 - 找到 %d 个相关关键词" % (c, p_count)

    # D. 表达规范性 (0-8)
    code_blocks = len(re.findall(r"```", content)) // 2
    has_lists = bool(re.search(r"^[-*]\s", content, re.MULTILINE))
    has_bold = "**" in content
    d_score = 0
    if code_blocks >= 3:
        d_score += 3
    elif code_blocks >= 1:
        d_score += 1
    if has_lists:
        d_score += 3
    if has_bold:
        d_score += 2
    d_score = min(d_score, 8)
    score += d_score
    details["表达规范性(降级)"] = "%d/8 - %d 代码块, 列表=%s, 粗体=%s" % (
        d_score, code_blocks, "有" if has_lists else "无", "有" if has_bold else "无"
    )

    score = min(score, 45)
    return score, {
        "分数": score,
        "详情": details,
        "扣分原因": ["LLM 不可用，使用降级评估"],
    }


# =============================================================================
# 主评估入口
# =============================================================================

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    评估 agent 的输出。

    Args:
        answer_dir: agent 输出目录的绝对路径
                    （例如 /path/to/query/gpt-5/attempt_1）

    Returns:
        (score, report)
        - score: 0-100 的整数
        - report: dict，包含详细评估报告
    """
    s1, r1 = _evaluate_delivery(answer_dir)
    s2, r2 = _evaluate_keywords(answer_dir)
    s3, r3 = _evaluate_coverage(answer_dir)
    s4, r4 = _evaluate_quality(answer_dir)

    total = int(s1 + s2 + s3 + s4)
    total = max(0, min(100, total))

    report = {
        "总分": total,
        "分项得分": {
            "文件交付与完整性": "%.1f/15" % s1,
            "技术关键词深度": "%.1f/10" % s2,
            "内容覆盖性": "%.1f/30" % s3,
            "文档质量": "%.1f/45" % s4,
        },
        "一_文件交付与完整性": r1,
        "二_技术关键词深度": r2,
        "三_内容覆盖性": r3,
        "四_文档质量": r4,
        "评语": "",
    }

    if total >= 90:
        report["评语"] = "优秀！报告内容全面深入、技术准确、结构规范，对 ESP32 项目的分析具有很好的工程参考价值。"
    elif total >= 75:
        report["评语"] = "良好。报告整体质量不错，覆盖了主要技术内容，个别方面可进一步深入。"
    elif total >= 60:
        report["评语"] = "及格。完成了基本的技术分析，但在内容深度或覆盖广度方面有待改进。"
    elif total >= 40:
        report["评语"] = "部分完成。报告有一定技术内容但存在明显不足，需要补充完善。"
    else:
        report["评语"] = "不及格。报告缺失严重或内容质量存在重大问题。"

    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """打印格式化的评分报告"""
    print("=" * 70)
    print("pengyichen-query3 评分报告")
    print("任务：代码功能识别与分析报告生成 - ESP32多媒体运动传感系统")
    print("=" * 70)
    print("\n总分：%d/100\n" % score)

    # 分项得分
    scores_summary = report.get("分项得分", {})
    if scores_summary:
        print("分项得分:")
        for k, v in scores_summary.items():
            print("  %s: %s" % (k, v))

    section_map = [
        ("一_文件交付与完整性", "一、文件交付与基本完整性 (15分)"),
        ("二_技术关键词深度", "二、技术关键词深度 (10分)"),
        ("三_内容覆盖性", "三、内容覆盖性 (30分)"),
        ("四_文档质量", "四、文档质量 (45分)"),
    ]

    for report_key, title in section_map:
        dim = report.get(report_key, {})
        print("\n" + "-" * 50)
        print("【%s】 得分: %s" % (title, dim.get("分数", "N/A")))
        print("-" * 50)
        for section, details in dim.get("详情", {}).items():
            if isinstance(details, dict):
                print("  %s:" % section)
                for item, val in details.items():
                    text = str(val)
                    if len(text) > 120:
                        text = text[:120] + "..."
                    print("    %s: %s" % (item, text))
            else:
                text = str(details)
                if len(text) > 120:
                    text = text[:120] + "..."
                print("  %s: %s" % (section, text))

        deds = dim.get("扣分原因", [])
        if deds:
            print("  扣分原因:")
            for i, reason in enumerate(deds, 1):
                print("    %d. %s" % (i, reason))

    print("\n" + "=" * 50)
    print("评语：%s" % report.get("评语", ""))
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
        print("正在评估目录: %s\n" % test_dir)
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print("目录不存在: %s" % test_dir)
    sys.exit(0)
