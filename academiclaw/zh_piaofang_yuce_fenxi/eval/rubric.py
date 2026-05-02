"""
评分标准 (Rubric) — 从零重写
任务：访问票房数据网站，分析并预测电影《阿凡达：火与烬》(Avatar: Fire and Ash) 的票房表现

总分：100分

评分维度：
一、文件交付与格式 (15分)
  1. 5个必需文件是否存在且非空 (10分)
  2. JSON 文件是否可解析、MD 文件是否有基本结构 (5分)

二、数据采集质量 (25分)
  1. 数据源数量与多样性 (8分)
  2. 有效数据提取率 (9分)
  3. 结构化数据字段完整度 (8分)

三、分析深度与质量 (30分) — LLM-as-Judge + 降级
  1. 票房走势分析 (8分)
  2. 竞品对比分析 (7分)
  3. 历史前作对比 (7分)
  4. 市场环境/口碑分析 (4分)
  5. 数据一致性 (4分)

四、预测质量 (30分) — LLM-as-Judge + 降级
  1. 预测方法论 (8分)
  2. 日度预测完整性 (8分)
  3. 总票房预测与区间 (8分)
  4. 不确定性与风险说明 (6分)
"""

import os
import re
import json
from typing import Tuple, Dict, Any, Optional, List

try:
    import openai
except ImportError:
    openai = None


# =========================================================================
# 环境与 LLM 配置
# =========================================================================

def _load_env(answer_dir: str) -> dict:
    """从 answer_dir 和 query 根目录加载 .env 配置"""
    values: dict = {}
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

    def g(key: str, default: str = "") -> str:
        return os.environ.get(key) or env.get(key) or default

    return {
        "api_key": g("EVAL_TEXT_API_KEY", g("ANTHROPIC_API_KEY")),
        "api_base": g("EVAL_TEXT_API_BASE_URL", g("ANTHROPIC_BASE_URL")),
        "model": g("EVAL_TEXT_MODEL", "openai/gpt-5.2"),
    }


def _call_llm_judge(prompt: str, config: dict) -> str:
    """调用 LLM 进行文本评估，失败时返回空字符串"""
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


def _parse_llm_json(raw: str) -> Optional[dict]:
    """从 LLM 输出中提取 JSON"""
    if not raw:
        return None
    m = re.search(r"```json\s*(.*?)\s*```", raw, re.DOTALL)
    text = m.group(1) if m else raw
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        try:
            return json.loads(text[start:end + 1])
        except json.JSONDecodeError:
            pass
    return None


# =========================================================================
# 辅助：加载文件
# =========================================================================

def _load_json(path: str) -> Optional[dict]:
    """加载 JSON 文件，失败返回 None"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _load_text(path: str) -> Optional[str]:
    """加载文本文件，失败返回 None"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return None


def _file_exists_and_nonempty(path: str, min_bytes: int = 50) -> bool:
    """检查文件存在且内容不少于 min_bytes"""
    return os.path.isfile(path) and os.path.getsize(path) >= min_bytes


# =========================================================================
# 一、文件交付与格式 (15分)
# =========================================================================

_DELIVERABLES = [
    ("raw_data_collection.json", "json", 2, "原始数据采集记录"),
    ("competitor_analysis.json", "json", 2, "竞品分析数据"),
    ("historical_comparison.json", "json", 2, "历史对比数据"),
    ("box_office_data.json", "json", 2, "数据摘要（结构化）"),
    ("box_office_analysis.md", "md", 2, "完整分析报告（主文件）"),
]


def _eval_file_delivery(answer_dir: str) -> Tuple[int, dict]:
    """
    子项1: 文件存在且非空 (10分)
    子项2: JSON 可解析 / MD 有标题结构 (5分)
    """
    score = 0
    details: Dict[str, str] = {}
    deductions: List[str] = []

    # 子项1: 存在性 (10分)
    existence_score = 0
    for fname, ftype, pts, label in _DELIVERABLES:
        fpath = os.path.join(answer_dir, fname)
        if _file_exists_and_nonempty(fpath, 50):
            existence_score += pts
            details[f"{label} ({fname})"] = f"{pts}/{pts} - 存在 ({os.path.getsize(fpath)}B)"
        elif os.path.isfile(fpath):
            half = max(1, pts // 2)
            existence_score += half
            details[f"{label} ({fname})"] = (
                f"{half}/{pts} - 存在但内容极少 ({os.path.getsize(fpath)}B)"
            )
            deductions.append(f"{fname} 文件内容过少")
        else:
            details[f"{label} ({fname})"] = f"0/{pts} - 缺失"
            deductions.append(f"缺少必需文件 {fname}")

    score += existence_score

    # 子项2: 格式有效性 (5分)
    format_score = 0
    json_files = [
        "raw_data_collection.json", "competitor_analysis.json",
        "historical_comparison.json", "box_office_data.json",
    ]

    parsable_count = 0
    for jf in json_files:
        data = _load_json(os.path.join(answer_dir, jf))
        if data is not None:
            parsable_count += 1

    if parsable_count >= 4:
        format_score += 3
        details["JSON 可解析"] = f"3/3 - 全部 {parsable_count}/4 个 JSON 可正确解析"
    elif parsable_count >= 3:
        format_score += 2
        details["JSON 可解析"] = f"2/3 - {parsable_count}/4 个 JSON 可解析"
    elif parsable_count >= 2:
        format_score += 1
        details["JSON 可解析"] = f"1/3 - 仅 {parsable_count}/4 个 JSON 可解析"
    else:
        details["JSON 可解析"] = f"0/3 - 仅 {parsable_count}/4 个 JSON 可解析"
        deductions.append("大多数 JSON 文件无法解析")

    md_text = _load_text(os.path.join(answer_dir, "box_office_analysis.md"))
    if md_text:
        heading_count = len(re.findall(r"^#{1,3}\s+", md_text, re.MULTILINE))
        if heading_count >= 4 and len(md_text) >= 1000:
            format_score += 2
            details["MD 报告结构"] = f"2/2 - {heading_count}个标题, {len(md_text)}字"
        elif heading_count >= 2 or len(md_text) >= 500:
            format_score += 1
            details["MD 报告结构"] = f"1/2 - {heading_count}个标题, {len(md_text)}字"
        else:
            details["MD 报告结构"] = (
                f"0/2 - 结构不足 ({heading_count}标题, {len(md_text)}字)"
            )
    else:
        details["MD 报告结构"] = "0/2 - 报告文件不可读"

    score += format_score

    return score, {"分数": score, "满分": 15, "详情": details, "扣分原因": deductions}


# =========================================================================
# 二、数据采集质量 (25分)
# =========================================================================

def _eval_data_quality(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details: Dict[str, Any] = {}
    deductions: List[str] = []

    # --- 2.1 数据源数量与多样性 (8分) ---
    raw_data = _load_json(os.path.join(answer_dir, "raw_data_collection.json"))
    sub1: Dict[str, str] = {}
    sub1_score = 0

    if raw_data:
        sources = raw_data.get("sources", [])
        src_count = len(sources)

        # 来源数量 (4分)
        if src_count >= 8:
            sub1_score += 4
            sub1["来源数量"] = f"4/4 - 访问了 {src_count} 个数据源（优秀）"
        elif src_count >= 5:
            sub1_score += 3
            sub1["来源数量"] = f"3/4 - 访问了 {src_count} 个数据源"
        elif src_count >= 3:
            sub1_score += 2
            sub1["来源数量"] = f"2/4 - 访问了 {src_count} 个数据源（偏少）"
        elif src_count >= 1:
            sub1_score += 1
            sub1["来源数量"] = f"1/4 - 仅 {src_count} 个数据源"
        else:
            sub1["来源数量"] = "0/4 - 无数据源记录"
            deductions.append("raw_data_collection 中无数据源记录")

        # 来源多样性 (4分) — 检查是否覆盖了国内外不同类型平台
        urls = [s.get("source_url", "") for s in sources]
        url_text = " ".join(urls).lower()

        diversity_markers = {
            "国际票房平台": any(
                d in url_text for d in ["boxofficemojo", "the-numbers"]
            ),
            "影评平台": any(
                d in url_text for d in ["rottentomatoes", "imdb", "metacritic"]
            ),
            "国内平台": any(
                d in url_text for d in [
                    "maoyan", "piaofang", "douban", "dengta", "taopiaopiao"
                ]
            ),
            "行业新闻": any(
                d in url_text for d in [
                    "deadline", "variety", "hollywoodreporter",
                    "boxofficepro", "screenrant", "thewrap",
                ]
            ),
        }
        diversity_count = sum(1 for v in diversity_markers.values() if v)
        if diversity_count >= 4:
            sub1_score += 4
            sub1["来源多样性"] = f"4/4 - 覆盖 {diversity_count}/4 类平台"
        elif diversity_count >= 3:
            sub1_score += 3
            sub1["来源多样性"] = f"3/4 - 覆盖 {diversity_count}/4 类平台"
        elif diversity_count >= 2:
            sub1_score += 2
            sub1["来源多样性"] = f"2/4 - 覆盖 {diversity_count}/4 类平台"
        elif diversity_count >= 1:
            sub1_score += 1
            sub1["来源多样性"] = f"1/4 - 仅覆盖 {diversity_count}/4 类平台"
        else:
            sub1["来源多样性"] = "0/4 - 未覆盖任何已知平台类型"
    else:
        sub1["错误"] = "0/8 - raw_data_collection.json 缺失或无法解析"
        deductions.append("原始数据采集文件缺失")

    details["2.1 数据源数量与多样性 (8分)"] = sub1
    score += sub1_score

    # --- 2.2 有效数据提取率 (9分) ---
    sub2: Dict[str, str] = {}
    sub2_score = 0

    if raw_data:
        sources = raw_data.get("sources", [])
        src_count = len(sources)
        effective = 0
        for s in sources:
            rc = s.get("raw_content", {})
            if not isinstance(rc, dict):
                if rc:
                    effective += 1
                continue
            err_val = str(rc.get("error", ""))
            title_val = str(rc.get("page_title", "")).lower()
            blocked_keywords = [
                "403", "forbidden", "cloudflare", "blocked",
                "timeout", "captcha", "access denied",
            ]
            if err_val:
                continue
            if any(kw in title_val for kw in blocked_keywords):
                continue
            meaningful_keys = [k for k in rc.keys() if k != "page_title"]
            if meaningful_keys:
                effective += 1

        # 记录完整性
        complete_count = 0
        for s in sources:
            has_url = bool(s.get("source_url"))
            has_time = bool(s.get("access_time"))
            has_content = bool(s.get("raw_content") or s.get("data_extracted"))
            if has_url and has_time and has_content:
                complete_count += 1

        if src_count > 0:
            completeness_ratio = complete_count / src_count
        else:
            completeness_ratio = 0

        # 有效提取数 (6分)
        if effective >= 5:
            sub2_score += 6
            sub2["有效提取"] = (
                f"6/6 - {effective}/{src_count} 个源成功提取有意义数据"
            )
        elif effective >= 3:
            sub2_score += 4
            sub2["有效提取"] = f"4/6 - {effective}/{src_count} 个源成功提取"
        elif effective >= 2:
            sub2_score += 2
            sub2["有效提取"] = f"2/6 - {effective}/{src_count} 个源成功提取"
        elif effective >= 1:
            sub2_score += 1
            sub2["有效提取"] = f"1/6 - 仅 {effective}/{src_count} 个源有效"
        else:
            sub2["有效提取"] = "0/6 - 无有效数据提取"
            deductions.append("所有数据源均未成功提取有意义的数据")

        # 记录完整性 (3分)
        if completeness_ratio >= 0.8:
            sub2_score += 3
            sub2["记录完整性"] = (
                f"3/3 - {complete_count}/{src_count} 条记录包含 URL+时间+内容"
            )
        elif completeness_ratio >= 0.5:
            sub2_score += 2
            sub2["记录完整性"] = f"2/3 - {complete_count}/{src_count} 条完整"
        elif completeness_ratio > 0:
            sub2_score += 1
            sub2["记录完整性"] = f"1/3 - {complete_count}/{src_count} 条完整"
        else:
            sub2["记录完整性"] = "0/3 - 无完整记录"
    else:
        sub2["错误"] = "0/9 - 无法评估（文件缺失）"

    details["2.2 有效数据提取率 (9分)"] = sub2
    score += sub2_score

    # --- 2.3 结构化数据字段完整度 (8分) ---
    sub3: Dict[str, str] = {}
    sub3_score = 0

    box_data = _load_json(os.path.join(answer_dir, "box_office_data.json"))
    if box_data:
        cd = box_data.get("current_data", {})

        # 核心票房字段 (4分)
        core_fields = [
            "total_box_office", "total_box_office_usd",
            "release_date", "release_days",
        ]
        filled_core = 0
        for f in core_fields:
            val = cd.get(f)
            if val is not None and val != "N/A" and val != "" and val != "暂缺":
                filled_core += 1

        if filled_core >= 3:
            sub3_score += 4
            sub3["核心字段"] = (
                f"4/4 - {filled_core}/{len(core_fields)} 个核心字段有值"
            )
        elif filled_core >= 2:
            sub3_score += 2
            sub3["核心字段"] = (
                f"2/4 - {filled_core}/{len(core_fields)} 个核心字段有值"
            )
        elif filled_core >= 1:
            sub3_score += 1
            sub3["核心字段"] = f"1/4 - 仅 {filled_core} 个核心字段"
        else:
            sub3["核心字段"] = "0/4 - 无有效核心数据"
            deductions.append("box_office_data.json 核心票房字段全为空")

        # 扩展字段: 评分、趋势、预测 (4分)
        ext_checks = 0

        rating_fields = [
            "maoyan_score", "douban_score", "imdb_score",
            "rotten_tomatoes_score", "audience_score",
        ]
        has_rating = any(
            cd.get(f) is not None
            and cd.get(f) != "N/A"
            and cd.get(f) != ""
            and cd.get(f) != "暂缺"
            for f in rating_fields
        )
        if has_rating:
            ext_checks += 1

        if box_data.get("daily_trend") and len(box_data["daily_trend"]) > 0:
            ext_checks += 1

        if box_data.get("predictions") and len(box_data["predictions"]) > 0:
            ext_checks += 1

        fp = box_data.get("final_prediction", {})
        if fp and (fp.get("most_likely") or fp.get("min_estimate")):
            ext_checks += 1

        if ext_checks >= 4:
            sub3_score += 4
            sub3["扩展字段"] = "4/4 - 全部 4 项扩展数据完备"
        elif ext_checks >= 3:
            sub3_score += 3
            sub3["扩展字段"] = f"3/4 - {ext_checks}/4 项扩展数据"
        elif ext_checks >= 2:
            sub3_score += 2
            sub3["扩展字段"] = f"2/4 - {ext_checks}/4 项扩展数据"
        elif ext_checks >= 1:
            sub3_score += 1
            sub3["扩展字段"] = f"1/4 - {ext_checks}/4 项扩展数据"
        else:
            sub3["扩展字段"] = "0/4 - 无扩展数据"
    else:
        sub3["错误"] = "0/8 - box_office_data.json 缺失或无法解析"
        deductions.append("数据摘要文件缺失")

    details["2.3 结构化数据字段完整度 (8分)"] = sub3
    score += sub3_score

    return score, {"分数": score, "满分": 25, "详情": details, "扣分原因": deductions}


# =========================================================================
# 三、分析深度与质量 (30分) — LLM-as-Judge + 降级
# =========================================================================

def _eval_analysis_quality(answer_dir: str) -> Tuple[int, dict]:
    analysis = _load_text(os.path.join(answer_dir, "box_office_analysis.md"))
    box_data = _load_json(os.path.join(answer_dir, "box_office_data.json"))
    comp_data = _load_json(os.path.join(answer_dir, "competitor_analysis.json"))
    hist_data = _load_json(os.path.join(answer_dir, "historical_comparison.json"))

    if not analysis:
        return 0, {
            "分数": 0, "满分": 30,
            "详情": {"错误": "box_office_analysis.md 缺失或为空"},
            "扣分原因": ["分析报告不存在"],
        }

    config = _get_text_eval_config(answer_dir)

    ref_snippets = ""
    if box_data:
        cd_str = json.dumps(
            box_data.get("current_data", {}), ensure_ascii=False, indent=2
        )[:1500]
        ref_snippets += f"\n[box_office_data.json - current_data]:\n{cd_str}"
    if comp_data:
        comps = comp_data.get("competitors", [])[:5]
        cmp_str = json.dumps(comps, ensure_ascii=False, indent=2)[:1000]
        ref_snippets += f"\n[competitor_analysis.json - 前5条]:\n{cmp_str}"
    if hist_data:
        preds = hist_data.get("predecessor_comparison", [])
        hist_str = json.dumps(preds, ensure_ascii=False, indent=2)[:800]
        ref_snippets += f"\n[historical_comparison.json]:\n{hist_str}"

    prompt = f"""你是一位严格的电影票房分析报告评审专家。请评估以下《阿凡达：火与烬》票房分析报告的质量。

## 评分维度（严格打分，不要偏高）

### A. 票房走势分析 (0-8分)
- 0-2: 无走势分析或只有一句话概述
- 3-4: 有基本走势描述但缺乏数据支撑或深度
- 5-6: 有数据支撑的走势分析，包含日票房变化、环比等
- 7-8: 深入的走势分析，含衰减曲线、周末效应、拐点识别等

### B. 竞品对比分析 (0-7分)
- 0-2: 无竞品分析或仅列出名字
- 3-4: 列出了竞品但缺乏对比分析
- 5-6: 有对比数据和市场份额分析
- 7: 深入的竞争格局分析，含市场影响评估

### C. 历史前作对比 (0-7分)
- 0-2: 无历史对比或仅提及前作名字
- 3-4: 有基本的前作票房数据但缺乏分析
- 5-6: 与阿凡达1、水之道做了同期对比分析
- 7: 深入对比含比值、市场环境差异分析

### D. 市场环境/口碑分析 (0-4分)
- 0: 完全没有
- 1-2: 提及了评分或市场状况
- 3-4: 综合分析了口碑评分、档期特点、排片占比、观众画像等

### E. 数据一致性 (0-4分)
- 0: 报告中数据明显错误或自相矛盾
- 1-2: 部分数据有不一致
- 3-4: 报告内数据自洽，与JSON数据文件匹配

## 待评估的分析报告（截取前6000字）：
{analysis[:6000]}

## 参考数据（用于一致性检查）：
{ref_snippets}

请严格按以下 JSON 格式输出，不要输出其他内容：
```json
{{
  "A_trend": {{"score": 0, "reason": ""}},
  "B_competitor": {{"score": 0, "reason": ""}},
  "C_historical": {{"score": 0, "reason": ""}},
  "D_market": {{"score": 0, "reason": ""}},
  "E_consistency": {{"score": 0, "reason": ""}},
  "overall_comment": ""
}}
```"""

    raw = _call_llm_judge(prompt, config)
    result = _parse_llm_json(raw)

    if result:
        dim_map = {
            "A_trend":       ("票房走势分析", 8),
            "B_competitor":  ("竞品对比分析", 7),
            "C_historical":  ("历史前作对比", 7),
            "D_market":      ("市场环境/口碑", 4),
            "E_consistency": ("数据一致性", 4),
        }
        total_score = 0
        det: Dict[str, str] = {}
        for key, (label, mx) in dim_map.items():
            entry = result.get(key, {})
            s = max(0, min(mx, int(entry.get("score", 0))))
            total_score += s
            det[f"{label} ({mx}分)"] = f"{s}/{mx} - {entry.get('reason', '')}"
        det["总评"] = result.get("overall_comment", "")
        return total_score, {
            "分数": total_score, "满分": 30, "详情": det,
            "扣分原因": [], "评估方式": "LLM",
        }
    else:
        return _analysis_fallback(analysis, comp_data, hist_data)


def _analysis_fallback(
    text: str,
    comp_data: Optional[dict],
    hist_data: Optional[dict],
) -> Tuple[int, dict]:
    """LLM 不可用时的降级评估（基于关键词匹配，保守打分）"""
    score = 0
    details: Dict[str, str] = {}

    # A. 走势分析 (8分) → 降级最高 5 分
    trend_kws = [
        "走势", "趋势", "变化", "环比", "衰减", "日票房", "长尾", "工作日", "周末",
    ]
    trend_found = sum(1 for kw in trend_kws if kw in text)
    if trend_found >= 4:
        s = 5
    elif trend_found >= 2:
        s = 3
    elif trend_found >= 1:
        s = 1
    else:
        s = 0
    score += s
    details["走势分析 (8分)"] = f"{s}/8 (降级) - 匹配 {trend_found} 个关键词"

    # B. 竞品分析 (7分) → 降级最高 4 分
    comp_kws = ["竞品", "同档期", "竞争", "市场份额", "排片"]
    has_comp_data = (
        comp_data is not None and len(comp_data.get("competitors", [])) > 0
    )
    comp_found = sum(1 for kw in comp_kws if kw in text)
    if has_comp_data and comp_found >= 2:
        s = 4
    elif comp_found >= 2 or has_comp_data:
        s = 2
    elif comp_found >= 1:
        s = 1
    else:
        s = 0
    score += s
    details["竞品分析 (7分)"] = f"{s}/7 (降级)"

    # C. 历史对比 (7分) → 降级最高 4 分
    hist_kws = ["前作", "水之道", "阿凡达2", "2009", "Way of Water", "对比"]
    has_hist_data = (
        hist_data is not None
        and len(hist_data.get("predecessor_comparison", [])) > 0
    )
    hist_found = sum(1 for kw in hist_kws if kw in text)
    if has_hist_data and hist_found >= 2:
        s = 4
    elif hist_found >= 2 or has_hist_data:
        s = 2
    elif hist_found >= 1:
        s = 1
    else:
        s = 0
    score += s
    details["历史对比 (7分)"] = f"{s}/7 (降级)"

    # D. 市场/口碑 (4分) → 降级最高 2 分
    market_kws = ["口碑", "评分", "档期", "市场", "观众", "排片占比"]
    mk_found = sum(1 for kw in market_kws if kw in text)
    s = min(2, mk_found)
    score += s
    details["市场/口碑 (4分)"] = f"{s}/4 (降级)"

    # E. 一致性 (4分) → 降级给 2 分（无法验证）
    score += 2
    details["一致性 (4分)"] = "2/4 (降级 - 无法验证)"

    return score, {
        "分数": score, "满分": 30, "详情": details,
        "扣分原因": [], "评估方式": "降级（关键词匹配）",
    }


# =========================================================================
# 四、预测质量 (30分) — LLM-as-Judge + 降级
# =========================================================================

def _eval_prediction_quality(answer_dir: str) -> Tuple[int, dict]:
    analysis = _load_text(os.path.join(answer_dir, "box_office_analysis.md"))
    box_data = _load_json(os.path.join(answer_dir, "box_office_data.json"))

    if not analysis and not box_data:
        return 0, {
            "分数": 0, "满分": 30,
            "详情": {"错误": "分析报告和数据摘要均缺失"},
            "扣分原因": ["无预测内容可评估"],
        }

    config = _get_text_eval_config(answer_dir)

    pred_text = ""
    if analysis:
        idx = analysis.find("预测")
        if idx >= 0:
            pred_text = analysis[max(0, idx - 300):min(len(analysis), idx + 4000)]
        else:
            pred_text = analysis[-3000:]

    pred_data = ""
    if box_data:
        preds = box_data.get("predictions", [])[:7]
        fp = box_data.get("final_prediction", {})
        pred_data = json.dumps(
            {"predictions": preds, "final_prediction": fp},
            ensure_ascii=False, indent=2,
        )

    prompt = f"""你是一位严格的电影票房预测评审专家。请评估以下《阿凡达：火与烬》票房预测的质量。

## 评分维度（严格打分，不要偏高）

### A. 预测方法论 (0-8分)
- 0-2: 无方法说明，预测数字凭空出现
- 3-4: 简单提到了"基于趋势"但无具体方法
- 5-6: 说明了预测逻辑（如衰减模型、同比法等）和关键假设
- 7-8: 详细的方法论，含多种参考依据、假设条件、调整因子

### B. 日度预测完整性 (0-8分)
- 0-2: 无日度预测或仅预测1-2天
- 3-4: 预测了3-4天但缺乏细节
- 5-6: 预测了5-7天，含预测值和基本依据
- 7-8: 预测了3-7天以上，每天有具体数值、预测区间、置信度和依据

### C. 总票房预测与区间 (0-8分)
- 0-2: 无总票房预测
- 3-4: 有单点总票房预测但无区间
- 5-6: 有总票房预测区间（乐观/基准/悲观）
- 7-8: 有多场景预测，区间合理（参考:阿凡达1全球$29.2亿,水之道$23.4亿），含条件假设

### D. 不确定性与风险说明 (0-6分)
- 0-1: 无风险提示
- 2-3: 简单提及了风险
- 4-5: 列出了多个风险因素和不确定性来源
- 6: 系统性风险分析，含影响程度评估

## 预测相关报告段落：
{pred_text}

## 预测结构化数据：
{pred_data}

请严格按以下 JSON 格式输出，不要输出其他内容：
```json
{{
  "A_methodology": {{"score": 0, "reason": ""}},
  "B_daily_forecast": {{"score": 0, "reason": ""}},
  "C_total_forecast": {{"score": 0, "reason": ""}},
  "D_uncertainty": {{"score": 0, "reason": ""}},
  "overall_comment": ""
}}
```"""

    raw = _call_llm_judge(prompt, config)
    result = _parse_llm_json(raw)

    if result:
        dim_map = {
            "A_methodology":    ("预测方法论", 8),
            "B_daily_forecast": ("日度预测完整性", 8),
            "C_total_forecast": ("总票房预测与区间", 8),
            "D_uncertainty":    ("不确定性与风险", 6),
        }
        total_score = 0
        det: Dict[str, str] = {}
        for key, (label, mx) in dim_map.items():
            entry = result.get(key, {})
            s = max(0, min(mx, int(entry.get("score", 0))))
            total_score += s
            det[f"{label} ({mx}分)"] = f"{s}/{mx} - {entry.get('reason', '')}"
        det["总评"] = result.get("overall_comment", "")
        return total_score, {
            "分数": total_score, "满分": 30, "详情": det,
            "扣分原因": [], "评估方式": "LLM",
        }
    else:
        return _prediction_fallback(analysis, box_data)


def _prediction_fallback(
    analysis: Optional[str], box_data: Optional[dict]
) -> Tuple[int, dict]:
    """LLM 不可用时的降级评估"""
    score = 0
    details: Dict[str, str] = {}
    text = analysis or ""

    # A. 方法论 (8分) → 降级最高 5 分
    method_kws = ["方法", "依据", "基于", "模型", "假设", "衰减", "回归", "外推"]
    m_found = sum(1 for kw in method_kws if kw in text)
    if m_found >= 3:
        s = 5
    elif m_found >= 1:
        s = 2
    else:
        s = 0
    score += s
    details["方法论 (8分)"] = f"{s}/8 (降级)"

    # B. 日度预测 (8分) → 降级检查 box_data
    if box_data:
        preds = box_data.get("predictions", [])
        pred_count = len(preds)
        if pred_count >= 5:
            s = 6
        elif pred_count >= 3:
            s = 4
        elif pred_count >= 1:
            s = 2
        else:
            s = 0
        score += s
        details["日度预测 (8分)"] = f"{s}/8 (降级) - {pred_count} 天预测"
    else:
        details["日度预测 (8分)"] = "0/8 (降级) - 无数据"

    # C. 总票房预测 (8分) → 降级检查 final_prediction
    if box_data:
        fp = box_data.get("final_prediction", {})
        has_total = bool(fp.get("most_likely") or fp.get("min_estimate"))
        has_range = bool(fp.get("min_estimate") and fp.get("max_estimate"))
        if has_total and has_range:
            s = 5
        elif has_total:
            s = 3
        else:
            s = 0
        score += s
        details["总票房预测 (8分)"] = f"{s}/8 (降级)"
    else:
        details["总票房预测 (8分)"] = "0/8 (降级)"

    # D. 不确定性 (6分) → 降级最高 3 分
    risk_kws = ["风险", "不确定", "置信", "假设", "可能", "risk"]
    r_found = sum(1 for kw in risk_kws if kw in text)
    if r_found >= 3:
        s = 3
    elif r_found >= 1:
        s = 1
    else:
        s = 0
    score += s
    details["不确定性 (6分)"] = f"{s}/6 (降级)"

    return score, {
        "分数": score, "满分": 30, "详情": details,
        "扣分原因": [], "评估方式": "降级（结构检查）",
    }


# =========================================================================
# 入口函数
# =========================================================================

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    评估 agent 的输出。

    Args:
        answer_dir: agent 输出目录的绝对路径

    Returns:
        (score, report) — score 为 0-100 的整数, report 为详细评估报告
    """
    s1, r1 = _eval_file_delivery(answer_dir)
    s2, r2 = _eval_data_quality(answer_dir)
    s3, r3 = _eval_analysis_quality(answer_dir)
    s4, r4 = _eval_prediction_quality(answer_dir)

    total = max(0, min(100, int(s1 + s2 + s3 + s4)))

    if total >= 90:
        comment = "优秀！数据采集全面、分析深入、预测合理有据。"
    elif total >= 75:
        comment = "良好。基本完成各项要求，部分维度有提升空间。"
    elif total >= 60:
        comment = "及格。完成了基本数据收集和分析，但深度或规范性不足。"
    elif total >= 40:
        comment = "部分完成。存在明显的数据缺失或分析不足。"
    else:
        comment = "不及格。文件缺失严重或数据/分析/预测质量不达标。"

    report = {
        "总分": total,
        "一、文件交付与格式 (15分)": r1,
        "二、数据采集质量 (25分)": r2,
        "三、分析深度与质量 (30分)": r3,
        "四、预测质量 (30分)": r4,
        "评语": comment,
    }
    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """打印格式化的评分报告"""
    print("=" * 70)
    print("评分报告")
    print("任务：分析并预测电影《阿凡达：火与烬》的票房表现")
    print("=" * 70)
    print(f"\n总分：{score}/100\n")

    for section_key in [
        "一、文件交付与格式 (15分)",
        "二、数据采集质量 (25分)",
        "三、分析深度与质量 (30分)",
        "四、预测质量 (30分)",
    ]:
        section = report.get(section_key, {})
        sec_score = section.get("分数", 0)
        sec_max = section.get("满分", "?")
        eval_mode = section.get("评估方式", "")

        print("-" * 50)
        title = f"【{section_key}】 {sec_score}/{sec_max}"
        if eval_mode:
            title += f"  ({eval_mode})"
        print(title)
        print("-" * 50)

        for k, v in section.get("详情", {}).items():
            if isinstance(v, dict):
                print(f"  {k}:")
                for kk, vv in v.items():
                    line = str(vv)
                    if len(line) > 120:
                        line = line[:120] + "..."
                    print(f"    {kk}: {line}")
            else:
                line = str(v)
                if len(line) > 120:
                    line = line[:120] + "..."
                print(f"  {k}: {line}")

        deds = section.get("扣分原因", [])
        if deds:
            print("  扣分原因:")
            for i, d in enumerate(deds, 1):
                print(f"    {i}. {d}")
        print()

    print("=" * 50)
    print(f"评语：{report.get('评语', '')}")
    print("=" * 70)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        test_dir = sys.argv[1]
    else:
        test_dir = os.path.join(
            os.path.dirname(__file__), "..", "gpt-5", "attempt_1"
        )

    if not os.path.isabs(test_dir):
        test_dir = os.path.join(os.getcwd(), test_dir)

    if os.path.exists(test_dir):
        print(f"正在评估目录: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"目录不存在: {test_dir}")
    sys.exit(0)
