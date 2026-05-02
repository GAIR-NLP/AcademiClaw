#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scoring script — yiyang-query1: Cutting-edge TTS Technology Research Report
Total score: 100 points

Scoring dimensions:
  1. File Delivery              10 pts
  2. Report Structure & Format  15 pts
  3. Content Completeness (LLM) 25 pts
  4. Technical Depth (LLM)      20 pts
  5. Academic Standards         15 pts
  6. Data Analysis & Visualization 15 pts
"""

import os
import re
import json
import csv
import base64
import traceback
from typing import Tuple, Dict, Any, List

try:
    from PIL import Image
except ImportError:
    Image = None

try:
    import openai
except ImportError:
    openai = None


# ============================================================================
# Environment / LLM Helper Functions
# ============================================================================

def _load_env(answer_dir: str) -> dict:
    """Load .env configuration from answer_dir and the query root directory"""
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
    """Get text evaluation LLM configuration"""
    env = _load_env(answer_dir)

    def g(key, default=""):
        return os.environ.get(key) or env.get(key) or default

    return {
        "api_key": g("EVAL_TEXT_API_KEY", g("ANTHROPIC_API_KEY")),
        "api_base": g("EVAL_TEXT_API_BASE_URL", g("ANTHROPIC_BASE_URL")),
        "model": g("EVAL_TEXT_MODEL", "openai/gpt-5.2"),
    }


def _get_vision_eval_config(answer_dir: str) -> dict:
    """Get vision evaluation LLM configuration"""
    env = _load_env(answer_dir)

    def g(key, default=""):
        return os.environ.get(key) or env.get(key) or default

    return {
        "api_key": g("EVAL_VISION_API_KEY", g("ANTHROPIC_API_KEY")),
        "api_base": g("EVAL_VISION_API_BASE_URL", g("ANTHROPIC_BASE_URL")),
        "model": g("EVAL_VISION_MODEL", "openai/gpt-5.2"),
    }


def _call_llm_judge(prompt: str, config: dict) -> str:
    """Call LLM for text evaluation"""
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
        print(f"[RUBRIC] LLM Judge call failed: {e}")
        return ""


def _parse_json_from_llm(text: str) -> dict:
    """Extract JSON from LLM response text"""
    if not text:
        return {}
    try:
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        return json.loads(text)
    except (json.JSONDecodeError, IndexError):
        return {}


def _read_file(path: str, max_chars: int = 80000) -> str:
    """Safely read a file"""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read(max_chars)
    except Exception:
        return ""


def _safe_listdir(d: str) -> List[str]:
    """Safely list directory contents"""
    try:
        return os.listdir(d)
    except Exception:
        return []


# ============================================================================
# 1. File Delivery (10 pts)
# ============================================================================

def _eval_file_delivery(answer_dir: str) -> Tuple[int, dict]:
    """
    Check whether three deliverable files exist and are non-empty:
      - report.md   (4 pts)
      - data_analysis.csv  (3 pts)
      - visualization.png  (3 pts)
    """
    score = 0
    details = {}
    all_files = _safe_listdir(answer_dir)

    # 1) report.md (4 pts)
    report_path = os.path.join(answer_dir, "report.md")
    if os.path.isfile(report_path):
        sz = os.path.getsize(report_path)
        if sz >= 1000:
            score += 4
            details["report.md"] = f"4/4 — exists ({sz} bytes)"
        elif sz > 0:
            score += 2
            details["report.md"] = f"2/4 — exists but too small ({sz} bytes)"
        else:
            details["report.md"] = "0/4 — file is empty"
    else:
        md_files = [f for f in all_files
                    if f.endswith(".md") and f.lower() not in
                    ("query.md", "operation_list.md", "context.md", "readme.md")]
        if md_files:
            score += 1
            details["report.md"] = f"1/4 — not found, but found {md_files[0]}"
        else:
            details["report.md"] = "0/4 — not found"

    # 2) data_analysis.csv (3 pts)
    csv_path = os.path.join(answer_dir, "data_analysis.csv")
    if os.path.isfile(csv_path):
        sz = os.path.getsize(csv_path)
        if sz >= 50:
            score += 3
            details["data_analysis.csv"] = f"3/3 — exists ({sz} bytes)"
        elif sz > 0:
            score += 1
            details["data_analysis.csv"] = f"1/3 — exists but too small ({sz} bytes)"
        else:
            details["data_analysis.csv"] = "0/3 — file is empty"
    else:
        csv_files = [f for f in all_files if f.endswith(".csv")]
        if csv_files:
            score += 1
            details["data_analysis.csv"] = f"1/3 — not found, but found {csv_files[0]}"
        else:
            details["data_analysis.csv"] = "0/3 — not found"

    # 3) visualization.png (3 pts)
    viz_path = os.path.join(answer_dir, "visualization.png")
    if os.path.isfile(viz_path):
        sz = os.path.getsize(viz_path)
        if sz >= 1024:
            score += 3
            details["visualization.png"] = f"3/3 — exists ({sz} bytes)"
        elif sz > 0:
            score += 1
            details["visualization.png"] = f"1/3 — exists but too small ({sz} bytes)"
        else:
            details["visualization.png"] = "0/3 — file is empty"
    else:
        img_exts = {".png", ".jpg", ".jpeg", ".svg", ".webp"}
        img_files = [f for f in all_files
                     if os.path.splitext(f)[1].lower() in img_exts]
        if img_files:
            score += 1
            details["visualization.png"] = f"1/3 — not found, but found {img_files[0]}"
        else:
            details["visualization.png"] = "0/3 — not found"

    return score, details


# ============================================================================
# 2. Report Structure & Format (15 pts)
# ============================================================================

def _eval_report_structure(answer_dir: str) -> Tuple[int, dict]:
    """
    Deterministic checks:
      2.1 Section structure completeness (5 pts)
      2.2 Report length >= 15000 words (5 pts)
      2.3 Markdown formatting standards (5 pts)
    """
    report_path = os.path.join(answer_dir, "report.md")
    content = _read_file(report_path)
    if not content:
        return 0, {"error": "report.md does not exist or is empty, skipping structure check"}

    score = 0
    details = {}

    # ---- 2.1 Section structure (5 pts) ----
    h2_matches = re.findall(r'^##\s+.+', content, re.MULTILINE)
    h3_matches = re.findall(r'^###\s+.+', content, re.MULTILINE)
    total_headings = len(h2_matches) + len(h3_matches)

    cl = content.lower()
    has_abstract = bool(re.search(r'(摘要|abstract)', cl))
    has_intro = bool(re.search(r'(引言|introduction|前言)', cl))
    has_conclusion = bool(re.search(r'(结论|conclusion|总结|展望)', cl))
    has_references = bool(re.search(r'(参考文献|references|bibliography)', cl))

    key_sections = sum([has_abstract, has_intro, has_conclusion, has_references])
    if key_sections >= 4 and total_headings >= 10:
        score += 5
        details["section_structure"] = f"5/5 — all key sections present ({key_sections}/4), {total_headings} headings total"
    elif key_sections >= 3 and total_headings >= 6:
        score += 3
        details["section_structure"] = f"3/5 — key sections {key_sections}/4, {total_headings} headings"
    elif key_sections >= 2:
        score += 1
        details["section_structure"] = f"1/5 — key sections {key_sections}/4, {total_headings} headings"
    else:
        details["section_structure"] = f"0/5 — key sections {key_sections}/4, incomplete structure"

    # ---- 2.2 Report length (5 pts) ----
    cn_chars = len(re.findall(r'[\u4e00-\u9fff]', content))
    en_words = len(re.findall(r'[a-zA-Z]+', content))
    approx_words = cn_chars + en_words

    if approx_words >= 15000:
        score += 5
        details["report_length"] = f"5/5 — approx. {approx_words} words (Chinese {cn_chars} + English {en_words})"
    elif approx_words >= 10000:
        score += 3
        details["report_length"] = f"3/5 — approx. {approx_words} words, below 15000 requirement"
    elif approx_words >= 5000:
        score += 2
        details["report_length"] = f"2/5 — approx. {approx_words} words, relatively short"
    elif approx_words >= 2000:
        score += 1
        details["report_length"] = f"1/5 — approx. {approx_words} words, too short"
    else:
        details["report_length"] = f"0/5 — approx. {approx_words} words, severely insufficient"

    # ---- 2.3 Markdown formatting standards (5 pts) ----
    fmt_score = 0
    fmt_notes = []

    # Tables
    if re.search(r'\|.+\|.+\|', content):
        fmt_score += 1
        fmt_notes.append("contains tables")

    # LaTeX math formulas
    has_display_formula = bool(re.search(r'(\$\$.+?\$\$|\\\[.+?\\\])', content, re.DOTALL))
    has_inline_formula = bool(re.search(r'(?<!\$)\$[^$\n]+\$(?!\$)', content))
    if has_display_formula and has_inline_formula:
        fmt_score += 2
        fmt_notes.append("contains inline + display formulas")
    elif has_display_formula or has_inline_formula:
        fmt_score += 1
        fmt_notes.append("contains math formulas")

    # Code blocks
    if re.search(r'```', content):
        fmt_score += 1
        fmt_notes.append("contains code blocks")

    # Lists
    if re.search(r'^[\-\*]\s+', content, re.MULTILINE):
        fmt_score += 1
        fmt_notes.append("contains lists")

    fmt_score = min(5, fmt_score)
    details["formatting"] = f"{fmt_score}/5 — {', '.join(fmt_notes) if fmt_notes else 'insufficient formatting elements'}"
    score += fmt_score

    return score, details


# ============================================================================
# 3. Content Completeness (25 pts) — LLM Judge
# ============================================================================

_CONTENT_PROMPT = """\
You are a strict academic report reviewer. Please evaluate the content completeness of the following TTS (Text-to-Speech) technology research report.

The report should cover the following 5 core aspects, each scored 0-5, totaling 25 points:

1. **TTS Technology Evolution** (0-5)
   - 5: Comprehensively traces the evolution from traditional methods (concatenative synthesis, parametric synthesis) to WaveNet/Tacotron and then to modern deep learning
   - 3-4: Mentions major stages but lacks detail
   - 1-2: Only briefly mentioned
   - 0: Not covered

2. **Cutting-edge Architecture Analysis** (0-5)
   - 5: Detailed analysis of at least 4 architectures including autoregressive, non-autoregressive, diffusion models, flow models, with technical principles and representative works (FastSpeech, VITS, Diff-TTS, Glow-TTS, VALL-E, etc.)
   - 3-4: Analyzes 2-3 architectures
   - 1-2: Only lists model names
   - 0: Not covered

3. **Key Technical Challenges** (0-5)
   - 5: In-depth discussion of core challenges including generation speed vs. quality balance, expressive diversity, cross-lingual/cross-speaker, data efficiency, with solution analysis
   - 3-4: Discusses some challenges
   - 1-2: Only briefly mentioned
   - 0: Not covered

4. **Evaluation Framework Analysis** (0-5)
   - 5: Systematic review of subjective evaluation (MOS, preference tests) and objective evaluation (PESQ, STOI, MCD, FAD), discussing advantages/disadvantages and frontier methods
   - 3-4: Mentions major evaluation metrics
   - 1-2: Only simple enumeration
   - 0: Not covered

5. **Future Development Directions** (0-5)
   - 5: Insightful predictions based on research trends, with specific technical roadmap or short/medium/long-term planning
   - 3-4: Proposes reasonable future directions
   - 1-2: Only generic discussion
   - 0: Not covered

Please strictly return in the following JSON format (do not include other content):
```json
{{
  "development_history": {{"score": 0, "reason": ""}},
  "architecture_analysis": {{"score": 0, "reason": ""}},
  "technical_challenges": {{"score": 0, "reason": ""}},
  "evaluation_framework": {{"score": 0, "reason": ""}},
  "future_directions": {{"score": 0, "reason": ""}},
  "total": 0
}}
```

Below is the report content to evaluate:

{report_text}
"""


def _eval_content_completeness(answer_dir: str) -> Tuple[int, dict]:
    report_path = os.path.join(answer_dir, "report.md")
    content = _read_file(report_path, max_chars=60000)
    if not content:
        return 0, {"error": "report.md does not exist or is empty"}

    config = _get_text_eval_config(answer_dir)
    prompt = _CONTENT_PROMPT.format(report_text=content[:55000])
    raw = _call_llm_judge(prompt, config)
    result = _parse_json_from_llm(raw)

    if not result:
        # Fallback: keyword-based heuristic
        score = 0
        details = {"note": "LLM unavailable, using keyword heuristic evaluation"}
        cl = content.lower()

        kw_groups = {
            "technology_evolution": ["拼接合成", "参数合成", "wavenet", "tacotron",
                         "concatenative", "parametric", "unit selection",
                         "statistical parametric"],
            "architecture_analysis": ["自回归", "非自回归", "扩散模型", "流模型",
                         "fastspeech", "vits", "diffusion", "autoregressive",
                         "non-autoregressive", "flow model", "flow-based",
                         "glow-tts", "grad-tts"],
            "technical_challenges": ["生成速度", "质量", "跨语言", "表达多样性",
                         "说话人", "real-time", "zero-shot", "speed",
                         "quality", "cross-lingual", "multilingual",
                         "speaker", "expressiveness", "prosody", "diversity"],
            "evaluation_framework": ["mos", "评估", "evaluation", "pesq",
                         "主观评估", "客观评估", "mean opinion",
                         "subjective", "objective", "naturalness"],
            "future_directions": ["未来", "展望", "趋势", "发展方向",
                         "future", "路线图", "roadmap", "trend",
                         "direction", "prospect", "outlook"],
        }
        for name, kws in kw_groups.items():
            found = sum(1 for kw in kws if kw.lower() in cl)
            if found >= 3:
                score += 4
            elif found >= 2:
                score += 3
            elif found >= 1:
                score += 2
            details[name] = f"matched {found}/{len(kws)} keywords"

        return min(25, score), details

    dims = [
        ("development_history", "technology_evolution"),
        ("architecture_analysis", "architecture_analysis"),
        ("technical_challenges", "technical_challenges"),
        ("evaluation_framework", "evaluation_framework"),
        ("future_directions", "future_directions"),
    ]
    score = 0
    details = {}
    for key, label in dims:
        d = result.get(key, {})
        s = max(0, min(5, int(d.get("score", 0))))
        score += s
        details[label] = f"{s}/5 — {d.get('reason', '')}"

    return min(25, score), details


# ============================================================================
# 4. Technical Depth (20 pts) — LLM Judge
# ============================================================================

_DEPTH_PROMPT = """\
You are a strict academic report reviewer. Please evaluate the technical depth of the following TTS technology research report.

Evaluate 4 dimensions, totaling 20 points:

1. **Mathematical Formulas & Algorithms** (0-5)
   - 5: Key technical sections include rigorous mathematical formulas or algorithm pseudocode (attention mechanism, diffusion forward/reverse process, flow model transformations, VAE/ELBO, etc.), with computational complexity analysis (Big-O)
   - 3-4: Contains some formulas but incomplete or lacks complexity analysis
   - 1-2: Only a few simple formulas
   - 0: No formulas

2. **Industry Case Analysis** (0-5)
   - 5: Covers >= 4 real-world industry systems (e.g., Google Cloud TTS, Microsoft VALL-E 2, NVIDIA Riva, iFlytek, Baidu, etc.), with technical architecture, performance metrics, deployment data
   - 3-4: Mentions 2-3 systems but analysis lacks depth
   - 1-2: Only mentions 1 system or generic discussion
   - 0: No industry cases

3. **Ethics & Security Analysis** (0-5)
   - 5: In-depth discussion of deepfake detection (with specific systems and AUC/EER data), data privacy (DPIA/GDPR/CCPA), algorithmic fairness, environmental impact, providing specific technical implementation paths (e.g., differential privacy epsilon values, federated learning architecture) and governance roadmap
   - 3-4: Discusses some ethical issues
   - 1-2: Only briefly mentioned
   - 0: Not covered

4. **Quantitative Comparative Analysis** (0-5)
   - 5: Uses tables to clearly compare performance metrics of different architectures (MOS, RTF, parameter count, etc.), analyzing technical root causes of differences rather than simple enumeration
   - 3-4: Some quantitative data but not systematic
   - 1-2: Only qualitative comparison
   - 0: No comparative analysis

Please strictly return in the following JSON format (do not include other content):
```json
{{
  "math_formulas": {{"score": 0, "reason": ""}},
  "industry_cases": {{"score": 0, "reason": ""}},
  "ethics_security": {{"score": 0, "reason": ""}},
  "quantitative_comparison": {{"score": 0, "reason": ""}},
  "total": 0
}}
```

Below is the report content to evaluate:

{report_text}
"""


def _eval_technical_depth(answer_dir: str) -> Tuple[int, dict]:
    report_path = os.path.join(answer_dir, "report.md")
    content = _read_file(report_path, max_chars=60000)
    if not content:
        return 0, {"error": "report.md does not exist or is empty"}

    config = _get_text_eval_config(answer_dir)
    prompt = _DEPTH_PROMPT.format(report_text=content[:55000])
    raw = _call_llm_judge(prompt, config)
    result = _parse_json_from_llm(raw)

    if not result:
        # Fallback
        score = 0
        details = {"note": "LLM unavailable, using keyword heuristic evaluation"}
        cl = content.lower()

        # Math formulas
        if re.search(r'(\$\$.+?\$\$|\\\[.+?\\\])', content, re.DOTALL):
            score += 3
            details["math_formulas"] = "LaTeX formulas detected"
        else:
            details["math_formulas"] = "No LaTeX formulas detected"

        # Industry cases
        industry_kws = ["google", "microsoft", "nvidia", "amazon", "讯飞",
                        "iflytek", "baidu", "百度", "riva", "cloud tts"]
        matched = sum(1 for kw in industry_kws if kw.lower() in cl)
        if matched >= 3:
            score += 3
            details["industry_cases"] = f"Detected {matched} industry system names"
        elif matched >= 1:
            score += 1
            details["industry_cases"] = f"Detected {matched} industry system name(s)"
        else:
            details["industry_cases"] = "No industry system names detected"

        # Ethics
        ethics_kws = ["深度伪造", "deepfake", "隐私", "gdpr", "伦理",
                      "ethics", "asvspoof", "公平", "fairness", "bias",
                      "privacy", "security"]
        matched_e = sum(1 for kw in ethics_kws if kw.lower() in cl)
        if matched_e >= 3:
            score += 3
            details["ethics_security"] = f"Detected {matched_e} ethics/security keywords"
        elif matched_e >= 1:
            score += 2
            details["ethics_security"] = f"Detected {matched_e} ethics/security keyword(s)"
        else:
            details["ethics_security"] = "No ethics/security discussion detected"

        # Quantitative comparison
        if re.search(r'\|.+\|.+\|', content):
            score += 3
            details["quantitative_comparison"] = "Tables detected"
        else:
            details["quantitative_comparison"] = "No comparison tables detected"

        return min(20, score), details

    dims = [
        ("math_formulas", "math_formulas"),
        ("industry_cases", "industry_cases"),
        ("ethics_security", "ethics_security"),
        ("quantitative_comparison", "quantitative_comparison"),
    ]
    score = 0
    details = {}
    for key, label in dims:
        d = result.get(key, {})
        s = max(0, min(5, int(d.get("score", 0))))
        score += s
        details[label] = f"{s}/5 — {d.get('reason', '')}"

    return min(20, score), details


# ============================================================================
# 5. Academic Standards (15 pts)
# ============================================================================

def _eval_academic_quality(answer_dir: str) -> Tuple[int, dict]:
    """
    5.1 Reference count (4 pts) — deterministic
    5.2 IEEE citation format (3 pts) — deterministic
    5.3 Terminology & writing style (8 pts) — LLM Judge
    """
    report_path = os.path.join(answer_dir, "report.md")
    content = _read_file(report_path, max_chars=60000)
    if not content:
        return 0, {"error": "report.md does not exist or is empty"}

    score = 0
    details = {}

    # ---- 5.1 Reference count (4 pts) ----
    # IEEE: [1], [2], ...
    inline_refs = set(re.findall(r'\[(\d+)\]', content))
    num_inline = len(inline_refs)

    # Find reference list section
    ref_match = re.search(
        r'(?:参考文献|references|bibliography)\s*\n([\s\S]*?)(?:\n#|\Z)',
        content, re.IGNORECASE
    )
    ref_entries = []
    if ref_match:
        ref_text = ref_match.group(1)
        ref_entries = re.findall(r'\[\d+\]', ref_text)
    num_ref = len(ref_entries)
    ref_count = max(num_inline, num_ref)

    if ref_count >= 10:
        score += 4
        details["reference_count"] = (
            f"4/4 — {ref_count} references"
            f" (inline citations {num_inline}, reference list {num_ref})"
        )
    elif ref_count >= 7:
        score += 3
        details["reference_count"] = f"3/4 — {ref_count} references, below 10"
    elif ref_count >= 4:
        score += 2
        details["reference_count"] = f"2/4 — only {ref_count} references"
    elif ref_count >= 1:
        score += 1
        details["reference_count"] = f"1/4 — only {ref_count} reference(s)"
    else:
        details["reference_count"] = "0/4 — no references detected"

    # ---- 5.2 IEEE format (3 pts) ----
    # Check [n] Author, "Title" pattern
    has_ieee_pattern = bool(re.search(r'\[\d+\]\s+[A-Z]', content))
    has_proper_ref_section = num_ref >= 5

    if has_ieee_pattern and has_proper_ref_section:
        score += 3
        details["IEEE_format"] = "3/3 — standard IEEE numbered citation format detected"
    elif has_ieee_pattern:
        score += 2
        details["IEEE_format"] = "2/3 — partially uses IEEE format"
    elif num_inline > 0:
        score += 1
        details["IEEE_format"] = "1/3 — has numbered citations but not standard IEEE format"
    else:
        details["IEEE_format"] = "0/3 — no standard citation format"

    # ---- 5.3 Terminology & writing style (8 pts) — LLM Judge ----
    _ACADEMIC_PROMPT = """\
You are an academic writing reviewer. Please evaluate the academic writing quality of the following TTS research report.

Evaluate 2 aspects, totaling 8 points:

1. **Terminology Usage & Consistency** (0-4)
   - 4: Terminology is clearly defined and consistent throughout, figures/tables are properly numbered (Table 1, Figure 2), technical terms are defined/explained on first appearance, bilingual terminology used appropriately
   - 2-3: Terminology is basically accurate but occasionally inconsistent
   - 0-1: Terminology is confused or frequently misused

2. **Writing Style** (0-4)
   - 4: Uses third person, passive voice, no colloquial expressions, objective and rigorous, logically clear
   - 2-3: Basically academic but occasionally informal
   - 0-1: Overly colloquial, not professional enough

Please strictly return in the following JSON format (do not include other content):
```json
{{{{
  "terminology": {{"score": 0, "reason": ""}},
  "writing_style": {{"score": 0, "reason": ""}},
  "total": 0
}}}}
```

Below is the report to evaluate (first half):

{report_text}
"""
    config = _get_text_eval_config(answer_dir)
    raw = _call_llm_judge(
        _ACADEMIC_PROMPT.format(report_text=content[:30000]), config
    )
    result = _parse_json_from_llm(raw)

    if result:
        t_s = max(0, min(4, int(result.get("terminology", {}).get("score", 0))))
        w_s = max(0, min(4, int(result.get("writing_style", {}).get("score", 0))))
        score += t_s + w_s
        details["terminology_consistency"] = (
            f"{t_s}/4 — {result.get('terminology', {}).get('reason', '')}"
        )
        details["writing_style"] = (
            f"{w_s}/4 — {result.get('writing_style', {}).get('reason', '')}"
        )
    else:
        # Fallback: give conservative 4/8
        score += 4
        details["academic_expression"] = "4/8 — LLM unavailable, giving conservative score"

    return min(15, score), details


# ============================================================================
# 6. Data Analysis & Visualization (15 pts)
# ============================================================================

def _eval_data_and_viz(answer_dir: str) -> Tuple[int, dict]:
    """
    6.1 CSV data quality (7 pts)
    6.2 Visualization image quality (8 pts)
    """
    score = 0
    details = {}
    all_files = _safe_listdir(answer_dir)

    # ---- 6.1 CSV data quality (7 pts) ----
    csv_path = os.path.join(answer_dir, "data_analysis.csv")
    if not os.path.isfile(csv_path):
        csv_files = [f for f in all_files if f.endswith(".csv")]
        csv_path = os.path.join(answer_dir, csv_files[0]) if csv_files else None

    if csv_path and os.path.isfile(csv_path):
        try:
            with open(csv_path, "r", encoding="utf-8", errors="replace") as f:
                reader = csv.reader(f)
                rows = list(reader)

            if len(rows) >= 2:
                header = rows[0]
                data_rows = rows[1:]
                num_cols = len(header)

                # Basic structure (3 pts)
                if num_cols >= 3 and len(data_rows) >= 3:
                    score += 3
                    details["CSV_structure"] = (
                        f"3/3 — {len(rows)} rows x {num_cols} columns"
                    )
                elif num_cols >= 2 and len(data_rows) >= 1:
                    score += 2
                    details["CSV_structure"] = (
                        f"2/3 — {len(rows)} rows x {num_cols} columns (relatively few)"
                    )
                else:
                    score += 1
                    details["CSV_structure"] = f"1/3 — {len(rows)} rows x {num_cols} columns"

                # Content relevance (4 pts) — header keyword matching
                header_text = " ".join(header).lower()
                tts_kws = [
                    "model", "模型", "mos", "rtf", "architecture", "架构",
                    "score", "分数", "speed", "quality", "accuracy",
                    "tts", "speech", "语音", "method", "方法",
                    "year", "年份", "parameter", "参数", "type", "类型",
                    "dataset", "数据集", "wer", "pesq", "latency",
                ]
                matched = sum(1 for kw in tts_kws if kw in header_text)
                if matched >= 3:
                    score += 4
                    details["CSV_relevance"] = (
                        f"4/4 — header matches {matched} TTS keywords"
                    )
                elif matched >= 1:
                    score += 2
                    details["CSV_relevance"] = (
                        f"2/4 — header matches {matched} keyword(s)"
                    )
                else:
                    score += 1
                    details["CSV_relevance"] = "1/4 — header has no TTS-related keywords detected"
            else:
                score += 1
                details["CSV_structure"] = f"1/7 — only {len(rows)} row(s), insufficient data"
        except Exception as e:
            details["CSV_parsing"] = f"0/7 — parsing failed: {str(e)[:100]}"
    else:
        details["CSV_file"] = "0/7 — not found"

    # ---- 6.2 Visualization image quality (8 pts) ----
    viz_path = os.path.join(answer_dir, "visualization.png")
    if not os.path.isfile(viz_path):
        img_exts = {".png", ".jpg", ".jpeg", ".svg", ".webp"}
        img_files = [f for f in all_files
                     if os.path.splitext(f)[1].lower() in img_exts]
        viz_path = os.path.join(answer_dir, img_files[0]) if img_files else None

    if viz_path and os.path.isfile(viz_path):
        fsize = os.path.getsize(viz_path)

        # Basic validity (3 pts)
        if Image is not None:
            try:
                img = Image.open(viz_path)
                w, h = img.size
                if w >= 400 and h >= 300 and fsize >= 10240:
                    score += 3
                    details["image_validity"] = f"3/3 — {w}x{h}, {fsize / 1024:.0f}KB"
                elif w >= 200 and h >= 150:
                    score += 2
                    details["image_validity"] = (
                        f"2/3 — {w}x{h}, {fsize / 1024:.0f}KB (somewhat small)"
                    )
                else:
                    score += 1
                    details["image_validity"] = (
                        f"1/3 — {w}x{h}, {fsize / 1024:.0f}KB (too small)"
                    )
            except Exception as e:
                details["image_validity"] = f"0/3 — cannot open: {str(e)[:80]}"
        else:
            if fsize >= 10240:
                score += 2
                details["image_validity"] = f"2/3 — {fsize / 1024:.0f}KB (PIL unavailable)"
            elif fsize > 0:
                score += 1
                details["image_validity"] = f"1/3 — {fsize / 1024:.0f}KB (PIL unavailable)"
            else:
                details["image_validity"] = "0/3 — file is empty"

        # Vision LLM evaluation of image content (5 pts)
        vision_config = _get_vision_eval_config(answer_dir)
        can_vision = (
            openai
            and vision_config.get("api_key")
            and viz_path.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
        )
        if can_vision:
            try:
                with open(viz_path, "rb") as f:
                    img_b64 = base64.b64encode(f.read()).decode("utf-8")
                ext = os.path.splitext(viz_path)[1].lower()
                mime = {
                    ".png": "image/png",
                    ".jpg": "image/jpeg",
                    ".jpeg": "image/jpeg",
                    ".webp": "image/webp",
                }.get(ext, "image/png")

                viz_prompt = """\
You are a data visualization evaluation expert. This image should be a data visualization chart related to TTS (Text-to-Speech) technology.

Please evaluate the quality of this image, total 5 points:

- 5: Clear data chart (bar chart/line chart/heatmap/radar chart, etc.), content directly related to TTS technology, title/labels/legend all present
- 3-4: Is a data chart but some information missing, or weak relevance to TTS
- 1-2: Poor image quality or unrelated to data analysis
- 0: Blank/corrupted/completely irrelevant

Please strictly return in the following JSON format:
```json
{"score": 0, "reason": ""}
```"""

                base = vision_config["api_base"].rstrip("/")
                if not base.endswith("/v1"):
                    base += "/v1"
                client = openai.OpenAI(
                    api_key=vision_config["api_key"], base_url=base
                )
                resp = client.chat.completions.create(
                    model=vision_config["model"],
                    messages=[{
                        "role": "user",
                        "content": [
                            {"type": "text", "text": viz_prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{mime};base64,{img_b64}"
                                },
                            },
                        ],
                    }],
                    max_tokens=512,
                    temperature=0,
                )
                viz_text = resp.choices[0].message.content.strip()
                viz_result = _parse_json_from_llm(viz_text)
                if viz_result:
                    vs = max(0, min(5, int(viz_result.get("score", 0))))
                    score += vs
                    details["image_content_eval"] = (
                        f"{vs}/5 — {viz_result.get('reason', '')}"
                    )
                else:
                    score += 2
                    details["image_content_eval"] = "2/5 — LLM response parsing failed, giving conservative score"
            except Exception as e:
                score += 2
                details["image_content_eval"] = (
                    f"2/5 — Vision evaluation failed: {str(e)[:80]}, giving conservative score"
                )
        else:
            score += 2
            details["image_content_eval"] = "2/5 — Vision LLM unavailable, giving conservative score"
    else:
        details["image_file"] = "0/8 — not found"

    return min(15, score), details


# ============================================================================
# Main Entry
# ============================================================================

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Evaluate the agent's output.

    Args:
        answer_dir: absolute path to the agent output directory

    Returns:
        (score, report) — score is a 0-100 integer, report is a detailed dict
    """
    if not os.path.isdir(answer_dir):
        return 0, {"error": f"Directory does not exist: {answer_dir}"}

    s1, r1 = _eval_file_delivery(answer_dir)
    s2, r2 = _eval_report_structure(answer_dir)
    s3, r3 = _eval_content_completeness(answer_dir)
    s4, r4 = _eval_technical_depth(answer_dir)
    s5, r5 = _eval_academic_quality(answer_dir)
    s6, r6 = _eval_data_and_viz(answer_dir)

    total = s1 + s2 + s3 + s4 + s5 + s6

    report = {
        "total_score": total,
        "dimension_scores": {
            "1. File Delivery (10)": s1,
            "2. Report Structure & Format (15)": s2,
            "3. Content Completeness (25)": s3,
            "4. Technical Depth (20)": s4,
            "5. Academic Standards (15)": s5,
            "6. Data Analysis & Visualization (15)": s6,
        },
        "details": {
            "1. File Delivery": r1,
            "2. Report Structure & Format": r2,
            "3. Content Completeness": r3,
            "4. Technical Depth": r4,
            "5. Academic Standards": r5,
            "6. Data Analysis & Visualization": r6,
        },
    }

    if total >= 85:
        report["comment"] = "Excellent: Report is well-structured, content is thorough, academically rigorous, with high-quality data analysis and visualization."
    elif total >= 70:
        report["comment"] = "Good: Report is mostly complete, main content is well-covered, but some dimensions have room for improvement."
    elif total >= 50:
        report["comment"] = "Passing: Report framework is basically established, but content depth, academic standards, or data analysis have notable deficiencies."
    elif total >= 25:
        report["comment"] = "Below passing: Report completion is low, multiple dimensions are severely lacking."
    else:
        report["comment"] = "Failing: Task not completed or deliverables are severely insufficient."

    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print a formatted scoring report"""
    print("=" * 70)
    print("yiyang-query1 Scoring Report — Cutting-edge TTS Technology Research Report")
    print("=" * 70)
    print(f"\nTotal Score: {score}/100\n")

    scores = report.get("dimension_scores", {})
    if scores:
        print("Dimension Scores:")
        for k, v in scores.items():
            print(f"  {k}: {v}")

    details = report.get("details", {})
    for section, items in details.items():
        print(f"\n{'─' * 50}")
        print(f"[{section}]")
        print(f"{'─' * 50}")
        if isinstance(items, dict):
            for k, v in items.items():
                if isinstance(v, dict):
                    print(f"  {k}:")
                    for kk, vv in v.items():
                        print(f"    {kk}: {vv}")
                else:
                    print(f"  {k}: {v}")
        else:
            print(f"  {items}")

    if "comment" in report:
        print(f"\n{'=' * 50}")
        print(f"Comment: {report['comment']}")
    print("=" * 70)


if __name__ == "__main__":
    import sys

    test_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(__file__), "..", "gpt-5", "attempt_1"
    )
    if os.path.isdir(test_dir):
        print(f"Evaluating directory: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"Directory does not exist: {test_dir}")
        ws = os.path.join(os.path.dirname(__file__), "..", "workspace")
        if os.path.isdir(ws):
            print(f"Using workspace directory for testing: {ws}\n")
            s, r = evaluate(ws)
            print_report(s, r)
    sys.exit(0)
