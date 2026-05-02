#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scoring Script — Speech Foundation Model Research Report

Task: Write a comprehensive research report on speech foundation model technology
based on provided reference papers.

Deliverables:
  - report.md   — Detailed research report
  - data_analysis.csv — Data analysis results
  - visualization.png — Data visualization chart

Total: 100 points

Scoring Dimensions:
  I.   File Delivery and Basic Checks (10 pts)
      1. report.md exists and has content (5 pts)
      2. data_analysis.csv exists and is valid (3 pts)
      3. visualization.png exists and is valid (2 pts)

  II.  Report Structure and Formatting (15 pts)
      1. Section structure completeness (5 pts)
      2. Word count meets threshold (5 pts): rubric requires >= 15000 words
      3. Markdown/LaTeX formatting compliance (5 pts)

  III. Reference Standards (10 pts)
      1. Number of references >= 10 (4 pts)
      2. IEEE format (3 pts)
      3. 2024-2025 references >= 5 (3 pts)

  IV.  Content Completeness and Depth — LLM-as-Judge (45 pts)
      1. Technology evolution timeline (7 pts)
      2. Frontier architecture analysis (8 pts)
      3. Key technical challenges (7 pts)
      4. Evaluation framework analysis (7 pts)
      5. Application scenarios and industry cases (8 pts)
      6. Ethics and safety (8 pts)

  V.   Academic Expression and Innovation — LLM-as-Judge (20 pts)
      1. Academic language standards (5 pts)
      2. Mathematical formulas / algorithm pseudocode (5 pts)
      3. Critical analysis and original insights (5 pts)
      4. Future outlook roadmap (5 pts)
"""

import os
import re
import json
import csv
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


# ---------------------------------------------------------------------------
# Environment Configuration & LLM Calls
# ---------------------------------------------------------------------------

def _load_env(answer_dir: str) -> dict:
    """Load .env configuration from answer_dir and query root directory."""
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
    env = _load_env(answer_dir)

    def g(key, default=""):
        return os.environ.get(key) or env.get(key) or default

    return {
        "api_key": g("EVAL_TEXT_API_KEY", g("ANTHROPIC_API_KEY")),
        "api_base": g("EVAL_TEXT_API_BASE_URL", g("ANTHROPIC_BASE_URL")),
        "model": g("EVAL_TEXT_MODEL", "openai/gpt-5.2"),
    }


def _get_vision_eval_config(answer_dir: str) -> dict:
    env = _load_env(answer_dir)

    def g(key, default=""):
        return os.environ.get(key) or env.get(key) or default

    return {
        "api_key": g("EVAL_VISION_API_KEY", g("ANTHROPIC_API_KEY")),
        "api_base": g("EVAL_VISION_API_BASE_URL", g("ANTHROPIC_BASE_URL")),
        "model": g("EVAL_VISION_MODEL", "openai/gpt-5.2"),
    }


def _call_llm_judge(prompt: str, config: dict) -> str:
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
            max_tokens=4096,
            temperature=0,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        print(f"[RUBRIC] LLM Judge call failed: {e}")
        return ""


# ---------------------------------------------------------------------------
# General Utilities
# ---------------------------------------------------------------------------

def _read_file(filepath: str) -> str:
    for enc in ("utf-8", "gbk", "latin-1"):
        try:
            with open(filepath, "r", encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, Exception):
            continue
    return ""


def _count_words(text: str) -> int:
    """Mixed CJK/English word count: CJK character count + English word count."""
    chinese = len(re.findall(r'[\u4e00-\u9fff]', text))
    no_cn = re.sub(r'[\u4e00-\u9fff]', ' ', text)
    english = len(no_cn.split())
    return chinese + english


def _extract_ieee_refs(text: str) -> List[str]:
    """Extract reference entries starting with [N]."""
    return re.findall(r'^\s*\[\d+\]\s+.+', text, re.MULTILINE)


def _count_year_refs(refs: List[str], years: List[int]) -> int:
    count = 0
    for ref in refs:
        for y in years:
            if str(y) in ref:
                count += 1
                break
    return count


def _parse_llm_json(text: str) -> dict:
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


# ---------------------------------------------------------------------------
# I. File Delivery and Basic Checks (10 pts)
# ---------------------------------------------------------------------------

def _eval_file_delivery(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details = {}
    deductions = []
    files = os.listdir(answer_dir) if os.path.isdir(answer_dir) else []

    # 1) report.md (5 pts)
    report_found = None
    if "report.md" in files:
        report_found = "report.md"
    else:
        candidates = [f for f in files
                      if f.lower().endswith(".md")
                      and "report" in f.lower()
                      and f.lower() not in ("query.md", "readme.md",
                                            "operation_list.md", "context.md")]
        if not candidates:
            candidates = [f for f in files
                          if f.lower().endswith(".md")
                          and f.lower() not in ("query.md", "readme.md",
                                                "operation_list.md", "context.md")]
        if candidates:
            report_found = candidates[0]

    if report_found:
        content = _read_file(os.path.join(answer_dir, report_found))
        length = len(content.strip())
        exact_name = (report_found == "report.md")
        if length > 200 and exact_name:
            score += 5
            details["report.md"] = "5/5 — file exists and has content"
        elif length > 200:
            score += 3
            details["report.md"] = f"3/5 — filename mismatch (actual: {report_found})"
            deductions.append(f"Report filename is not report.md (actual: {report_found})")
        elif length > 0:
            s = 2 if exact_name else 1
            score += s
            details["report.md"] = f"{s}/5 — file content too short ({length} chars)"
            deductions.append("report.md content too short")
        else:
            score += 1
            details["report.md"] = "1/5 — file is empty"
            deductions.append("report.md is an empty file")
    else:
        details["report.md"] = "0/5 — report file not found"
        deductions.append("Missing report.md")

    # 2) data_analysis.csv (3 pts)
    csv_files = [f for f in files if f.lower().endswith(".csv")]
    if "data_analysis.csv" in files:
        fpath = os.path.join(answer_dir, "data_analysis.csv")
        fsize = os.path.getsize(fpath) if os.path.exists(fpath) else 0
        if fsize > 50:
            # Try parsing CSV to validate format
            try:
                with open(fpath, "r", encoding="utf-8") as cf:
                    reader = csv.reader(cf)
                    rows = list(reader)
                if len(rows) >= 2 and len(rows[0]) >= 2:
                    score += 3
                    details["data_analysis.csv"] = f"3/3 — valid CSV ({len(rows)} rows, {len(rows[0])} cols)"
                else:
                    score += 2
                    details["data_analysis.csv"] = f"2/3 — CSV has little data ({len(rows)} rows)"
            except Exception:
                score += 2
                details["data_analysis.csv"] = "2/3 — file exists but parsing failed"
        else:
            score += 1
            details["data_analysis.csv"] = "1/3 — file too small"
    elif csv_files:
        score += 1
        details["data_analysis.csv"] = f"1/3 — CSV filename mismatch ({csv_files[0]})"
        deductions.append("CSV filename is not data_analysis.csv")
    else:
        details["data_analysis.csv"] = "0/3 — no CSV file found"
        deductions.append("Missing data_analysis.csv")

    # 3) visualization.png (2 pts)
    img_exts = {".png", ".jpg", ".jpeg", ".svg", ".pdf"}
    img_files = [f for f in files if os.path.splitext(f)[1].lower() in img_exts]
    if "visualization.png" in files:
        fpath = os.path.join(answer_dir, "visualization.png")
        fsize = os.path.getsize(fpath) if os.path.exists(fpath) else 0
        if fsize > 1024:
            score += 2
            details["visualization.png"] = f"2/2 — file exists ({fsize // 1024}KB)"
        else:
            score += 1
            details["visualization.png"] = f"1/2 — file too small ({fsize}B)"
    elif img_files:
        score += 1
        details["visualization.png"] = f"1/2 — image filename mismatch ({img_files[0]})"
    else:
        details["visualization.png"] = "0/2 — visualization image not found"
        deductions.append("Missing visualization.png")

    return score, {"score": f"{score}/10", "details": details, "deductions": deductions}


# ---------------------------------------------------------------------------
# II. Report Structure and Formatting (15 pts)
# ---------------------------------------------------------------------------

def _eval_structure_format(report_text: str) -> Tuple[int, dict]:
    score = 0
    details = {}
    deductions = []

    if not report_text or len(report_text.strip()) < 50:
        return 0, {"score": "0/15", "details": {"error": "Report is empty or extremely short"},
                    "deductions": ["Cannot evaluate formatting"]}

    # --- 2.1 Section structure (5 pts) ---
    required = {
        "Abstract": r'abstract|summary',
        "Introduction": r'introduction',
        "Conclusion": r'conclusion',
        "References": r'references|bibliography',
    }
    sec_found = 0
    sec_detail = {}
    for name, pat in required.items():
        if re.search(pat, report_text, re.IGNORECASE):
            sec_found += 1
            sec_detail[name] = "[OK]"
        else:
            sec_detail[name] = "[MISSING]"
            deductions.append(f"Missing {name} section")

    # Main body section count
    headings = re.findall(r'^#{1,3}\s+.+', report_text, re.MULTILINE)
    main_headings = [h for h in headings if not re.search(
        r'abstract|introduction|conclusion|references|appendix',
        h, re.IGNORECASE)]

    if main_headings and len(main_headings) >= 4:
        sec_found += 1
        sec_detail["body_sections"] = f"[OK] detected {len(main_headings)}"
    elif main_headings:
        sec_detail["body_sections"] = f"[PARTIAL] only {len(main_headings)} (recommend >= 4)"
    else:
        sec_detail["body_sections"] = "[MISSING]"
        deductions.append("No main body section headings detected")

    sec_score = min(5, sec_found)
    score += sec_score
    details["2.1 section_structure (5 pts)"] = {"score": f"{sec_score}/5", **sec_detail}

    # --- 2.2 Word count (5 pts) ---
    wc = _count_words(report_text)
    if wc >= 15000:
        wc_score = 5
    elif wc >= 8000:
        wc_score = 4
    elif wc >= 5000:
        wc_score = 3
    elif wc >= 2000:
        wc_score = 2
    elif wc >= 1000:
        wc_score = 1
    else:
        wc_score = 0
    score += wc_score
    details["2.2 word_count (5 pts)"] = f"{wc_score}/5 — approx. {wc} words"
    if wc < 2000:
        deductions.append(f"Word count severely insufficient ({wc})")

    # --- 2.3 Formatting compliance (5 pts) ---
    fmt_pts = 0
    fmt_items = []
    if re.search(r'^#\s+', report_text, re.MULTILINE):
        fmt_pts += 1
        fmt_items.append("Markdown headings")
    if re.search(r'\|.*\|.*\|', report_text):
        fmt_pts += 1
        fmt_items.append("tables")
    if re.search(r'\$[^$]+\$|\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)', report_text):
        fmt_pts += 1
        fmt_items.append("math formulas")
    if "```" in report_text:
        fmt_pts += 1
        fmt_items.append("code blocks")
    if re.search(r'^\s*[-*+]\s+', report_text, re.MULTILINE) or \
       re.search(r'^\s*\d+\.\s+', report_text, re.MULTILINE):
        fmt_pts += 1
        fmt_items.append("lists")
    fmt_pts = min(5, fmt_pts)
    score += fmt_pts
    details["2.3 formatting (5 pts)"] = f"{fmt_pts}/5 — {', '.join(fmt_items) if fmt_items else 'no notable formatting elements'}"

    return score, {"score": f"{score}/15", "details": details, "deductions": deductions}


# ---------------------------------------------------------------------------
# III. Reference Standards (10 pts)
# ---------------------------------------------------------------------------

def _eval_references(report_text: str) -> Tuple[int, dict]:
    score = 0
    details = {}
    deductions = []

    if not report_text:
        return 0, {"score": "0/10", "details": {"error": "No report content"},
                    "deductions": ["Cannot evaluate references"]}

    refs = _extract_ieee_refs(report_text)
    inline_nums = set(re.findall(r'\[(\d+)\]', report_text))

    # 3.1 Quantity (4 pts)
    n = len(refs)
    if n >= 15:
        q = 4
    elif n >= 10:
        q = 3
    elif n >= 5:
        q = 2
    elif n >= 1:
        q = 1
    else:
        q = 0
        deductions.append("No references found")
    score += q
    details["3.1 quantity (4 pts)"] = f"{q}/4 — {n} references"

    # 3.2 IEEE format (3 pts)
    ieee_ok = sum(1 for r in refs if re.match(r'\[\d+\]\s+\S', r))
    if n == 0:
        f_score = 0
    elif ieee_ok >= n * 0.8:
        f_score = 3
    elif ieee_ok >= n * 0.5:
        f_score = 2
    elif ieee_ok > 0:
        f_score = 1
    else:
        f_score = 0
        deductions.append("References do not use IEEE format")
    score += f_score
    details["3.2 IEEE_format (3 pts)"] = f"{f_score}/3 — {ieee_ok}/{n} compliant"

    # 3.3 Recent papers (3 pts)
    recent = _count_year_refs(refs, [2024, 2025])
    if recent >= 5:
        y = 3
    elif recent >= 3:
        y = 2
    elif recent >= 1:
        y = 1
    else:
        y = 0
        if n > 0:
            deductions.append("Missing 2024-2025 papers")
    score += y
    details["3.3 recent_papers (3 pts)"] = f"{y}/3 — {recent} from 2024-2025"
    details["inline_citations"] = f"{len(inline_nums)} distinct citation numbers"

    return score, {"score": f"{score}/10", "details": details, "deductions": deductions}


# ---------------------------------------------------------------------------
# IV. Content Completeness and Depth — LLM-as-Judge (45 pts)
# ---------------------------------------------------------------------------

_CONTENT_PROMPT = """\
You are a senior review expert in the field of Speech Foundation Models. Please carefully read the following research report and strictly score it on 6 dimensions.

**Scoring Dimensions and Criteria**:

1. **Technology Evolution Timeline** (0-7 pts)
   - 7: Comprehensively traces the progression from traditional speech processing to large-scale pre-trained models, with accurate key milestones (e.g., wav2vec, HuBERT, WavLM, etc.)
   - 4-6: Covers major stages but lacks depth
   - 1-3: Only briefly mentioned
   - 0: Completely missing

2. **Frontier Architecture Analysis** (0-8 pts)
   - 7-8: Detailed analysis of self-supervised learning, multimodal models, speech language models, speech generation models, with quantitative performance data (SUPERB scores, parameter counts, training data volume) and tabular comparisons
   - 4-6: Covers major architectures but lacks quantitative comparisons
   - 1-3: Simple listing
   - 0: Completely missing

3. **Key Technical Challenges** (0-7 pts)
   - 6-7: In-depth analysis of data efficiency, computational efficiency, multilingual support, zero-shot learning, ethical safety, etc., each with theoretical analysis + frontier solutions + latest progress
   - 3-5: Covers major challenges but lacks depth
   - 1-2: Only briefly mentioned
   - 0: Completely missing

4. **Evaluation Framework Analysis** (0-7 pts)
   - 6-7: Systematically reviews SUPERB, AudioSet, LibriSpeech and other evaluation frameworks, with specific data comparisons and analysis
   - 3-5: Mentions evaluation methods but lacks systematic analysis
   - 1-2: Only briefly mentioned
   - 0: Completely missing

5. **Application Scenarios and Industry Cases** (0-8 pts)
   - 7-8: Covers >= 4 real industry systems (e.g., Gemini 1.5, GPT-4o, SeamlessM4T, Qwen-Audio, Alexa LLM, Microsoft Copilot), with technical architecture, performance metrics (RTF/MOS), and deployment data
   - 4-6: Mentions major systems but lacks detailed data
   - 1-3: Simple listing
   - 0: Completely missing

6. **Ethics and Safety** (0-8 pts)
   - 7-8: Covers data privacy (DPIA, GDPR/CCPA), algorithmic fairness, deepfake detection (ASVspoof 5 system AUC/EER data), environmental impact, each with specific technical paths (differential privacy epsilon values, federated learning architecture), citing policy regulations (EU AI Act, etc.)
   - 4-6: Covers major ethical topics but lacks technical paths
   - 1-3: Only briefly mentioned
   - 0: Completely missing

Reply strictly in the following JSON format (no other content):
```json
{{
  "tech_evolution": {{"score": 0, "reason": ""}},
  "architecture_analysis": {{"score": 0, "reason": ""}},
  "tech_challenges": {{"score": 0, "reason": ""}},
  "evaluation_framework": {{"score": 0, "reason": ""}},
  "applications": {{"score": 0, "reason": ""}},
  "ethics_safety": {{"score": 0, "reason": ""}},
  "total": 0
}}
```

**Research report to evaluate**:

{report_text}
"""


def _eval_content_depth(report_text: str, answer_dir: str) -> Tuple[int, dict]:
    details = {}
    deductions = []

    if not report_text or len(report_text.strip()) < 200:
        return 0, {"score": "0/45", "details": {"error": "Report content is empty or extremely short"},
                    "deductions": ["Cannot evaluate content"]}

    config = _get_text_eval_config(answer_dir)
    truncated = report_text[:30000] if len(report_text) > 30000 else report_text
    prompt = _CONTENT_PROMPT.format(report_text=truncated)

    llm_resp = _call_llm_judge(prompt, config)
    result = _parse_llm_json(llm_resp)

    dims = {
        "tech_evolution": ("technology_evolution", 7),
        "architecture_analysis": ("frontier_architecture", 8),
        "tech_challenges": ("key_technical_challenges", 7),
        "evaluation_framework": ("evaluation_framework", 7),
        "applications": ("applications_and_industry", 8),
        "ethics_safety": ("ethics_and_safety", 8),
    }

    if result:
        total = 0
        for key, (name, mx) in dims.items():
            dd = result.get(key, {})
            s = max(0, min(mx, int(dd.get("score", 0))))
            reason = dd.get("reason", "")
            total += s
            details[f"{name} ({mx} pts)"] = f"{s}/{mx} — {reason}"
            if s <= mx * 0.3:
                deductions.append(f"{name} score too low ({s}/{mx})")
        details["llm_model"] = config.get("model", "unknown")
        return total, {"score": f"{total}/45", "details": details, "deductions": deductions}

    # LLM unavailable — keyword fallback
    print("[RUBRIC] LLM content evaluation unavailable, falling back to keyword evaluation")
    kw_checks = {
        "technology_evolution": (["wav2vec", "hubert", "wavlm", "pre-train", "self-supervised",
                       "mfcc", "i-vector"], 7),
        "frontier_architecture": (["transformer", "encoder", "decoder", "attention",
                    "diffusion", "language model", "codec", "autoregressive"], 8),
        "technical_challenges": (["computational efficiency", "data efficiency", "multilingual", "zero-shot",
                    "low-resource", "scalab"], 7),
        "evaluation_framework": (["superb", "librispeech", "audioset", "evaluation", "benchmark",
                    "wer", "mos"], 7),
        "applications": (["gemini", "gpt-4o", "whisper", "qwen", "alexa",
                    "copilot", "seamless"], 8),
        "ethics_safety": (["privacy", "ethic", "deepfake", "fairness", "safety", "asvspoof",
                    "gdpr", "federated learning"], 8),
    }
    fb_total = 0
    for dim, (kws, mx) in kw_checks.items():
        low = report_text.lower()
        hits = sum(1 for kw in kws if kw.lower() in low)
        ratio = hits / len(kws)
        s = min(mx, int(ratio * mx * 0.6))
        fb_total += s
        details[f"{dim} ({mx} pts)"] = f"{s}/{mx} — fallback: {hits}/{len(kws)} keywords matched"
    details["note"] = "LLM unavailable, keyword fallback evaluation"
    return fb_total, {"score": f"{fb_total}/45", "details": details, "deductions": deductions}


# ---------------------------------------------------------------------------
# V. Academic Expression and Innovation — LLM-as-Judge (20 pts)
# ---------------------------------------------------------------------------

_QUALITY_PROMPT = """\
You are an academic paper review expert. Please evaluate the academic expression quality and innovation of the following speech foundation model research report.

**Scoring Dimensions**:

1. **Academic Language Standards** (0-5 pts)
   - 5: Entire text uses third person and passive voice, terminology is clearly and consistently defined, figures and tables are properly numbered (e.g., "Table 1", "Figure 2"), no colloquial expressions
   - 3-4: Generally compliant but with occasional inconsistencies
   - 1-2: Language is not sufficiently formal
   - 0: Severely non-compliant

2. **Mathematical Formulas / Algorithm Pseudocode** (0-5 pts)
   - 5: Key technical sections all contain rigorous mathematical formulas or pseudocode directly related to speech foundation model principles (e.g., CTC loss, self-supervised learning objective functions, attention mechanisms, diffusion processes), with complexity analysis (Big-O)
   - 3-4: Contains some formulas but not comprehensive
   - 1-2: Only a few simple formulas
   - 0: None at all

3. **Critical Analysis and Original Insights** (0-5 pts)
   - 5: Provides original insights in >= 2 dimensions such as evaluation frameworks, governance mechanisms, industry analysis, with in-depth critical analysis
   - 3-4: Some depth but not sufficiently prominent
   - 1-2: Primarily material compilation
   - 0: Purely assembled

4. **Future Outlook Roadmap** (0-5 pts)
   - 5: Provides a 2025-2030 technology roadmap with clear short-term / mid-term / long-term milestones, including specific technical metrics and expected timelines
   - 3-4: Has future outlook but lacks specific roadmap
   - 1-2: Only briefly mentioned
   - 0: Missing

Reply strictly in the following JSON format:
```json
{{
  "academic_language": {{"score": 0, "reason": ""}},
  "math_formulas": {{"score": 0, "reason": ""}},
  "critical_analysis": {{"score": 0, "reason": ""}},
  "future_roadmap": {{"score": 0, "reason": ""}},
  "total": 0
}}
```

**Research report to evaluate**:

{report_text}
"""


def _eval_quality_innovation(report_text: str, answer_dir: str) -> Tuple[int, dict]:
    details = {}
    deductions = []

    if not report_text or len(report_text.strip()) < 200:
        return 0, {"score": "0/20", "details": {"error": "Report content is empty or extremely short"},
                    "deductions": ["Cannot evaluate quality"]}

    config = _get_text_eval_config(answer_dir)
    truncated = report_text[:30000] if len(report_text) > 30000 else report_text
    prompt = _QUALITY_PROMPT.format(report_text=truncated)

    llm_resp = _call_llm_judge(prompt, config)
    result = _parse_llm_json(llm_resp)

    dims = {
        "academic_language": ("academic_language_standards", 5),
        "math_formulas": ("math_formulas_pseudocode", 5),
        "critical_analysis": ("critical_analysis_and_insights", 5),
        "future_roadmap": ("future_outlook_roadmap", 5),
    }

    if result:
        total = 0
        for key, (name, mx) in dims.items():
            dd = result.get(key, {})
            s = max(0, min(mx, int(dd.get("score", 0))))
            reason = dd.get("reason", "")
            total += s
            details[f"{name} ({mx} pts)"] = f"{s}/{mx} — {reason}"
            if s <= 1:
                deductions.append(f"{name} score too low")
        details["llm_model"] = config.get("model", "unknown")
        return total, {"score": f"{total}/20", "details": details, "deductions": deductions}

    # Fallback
    print("[RUBRIC] LLM quality evaluation unavailable, falling back")
    fb = 0

    # Academic language
    informal = ["i think", "awesome", "cool", "amazing", "pretty good"]
    inf_cnt = sum(1 for p in informal if p in report_text.lower())
    ls = 3 if inf_cnt == 0 else (2 if inf_cnt <= 2 else 1)
    fb += ls
    details["academic_language_standards (5 pts)"] = f"{ls}/5 — fallback"

    # Math formulas
    fc = len(re.findall(r'\$[^$]+\$|\\\[[\s\S]*?\\\]', report_text))
    ms = 3 if fc >= 5 else (2 if fc >= 2 else (1 if fc >= 1 else 0))
    fb += ms
    details["math_formulas_pseudocode (5 pts)"] = f"{ms}/5 — fallback: {fc} formulas found"

    # Conservative scores
    fb += 2
    details["critical_analysis_and_insights (5 pts)"] = "2/5 — conservative fallback"
    fb += 2
    details["future_outlook_roadmap (5 pts)"] = "2/5 — conservative fallback"
    details["note"] = "LLM unavailable, fallback evaluation"

    return fb, {"score": f"{fb}/20", "details": details, "deductions": deductions}


# ---------------------------------------------------------------------------
# Main Entry
# ---------------------------------------------------------------------------

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Evaluate the agent's output.

    Args:
        answer_dir: Absolute path to the agent's output directory

    Returns:
        (score, report) — score: 0-100 int, report: dict
    """
    if not os.path.isdir(answer_dir):
        return 0, {"total_score": 0, "error": f"Directory does not exist: {answer_dir}"}

    # Find report file
    files = os.listdir(answer_dir)
    report_file = None
    if "report.md" in files:
        report_file = "report.md"
    else:
        candidates = [f for f in files
                      if f.lower().endswith(".md")
                      and f.lower() not in ("query.md", "readme.md",
                                            "operation_list.md", "context.md")]
        if candidates:
            report_file = candidates[0]

    report_text = ""
    if report_file:
        report_text = _read_file(os.path.join(answer_dir, report_file))

    s1, r1 = _eval_file_delivery(answer_dir)
    s2, r2 = _eval_structure_format(report_text)
    s3, r3 = _eval_references(report_text)
    s4, r4 = _eval_content_depth(report_text, answer_dir)
    s5, r5 = _eval_quality_innovation(report_text, answer_dir)

    total = max(0, min(100, s1 + s2 + s3 + s4 + s5))

    if total >= 85:
        comment = "Excellent! Report structure is complete, content is in-depth, and academic expression is well-structured."
    elif total >= 70:
        comment = "Good. Task mostly completed, with room for improvement in some dimensions."
    elif total >= 50:
        comment = "Acceptable. Has some content but depth or completeness has notable shortcomings."
    elif total >= 30:
        comment = "Partial completion. Key content missing or quality below standards."
    else:
        comment = "Insufficient. Task completion severely lacking."

    report = {
        "total_score": total,
        "comment": comment,
        "section_scores": {
            "I. File Delivery": f"{s1}/10",
            "II. Structure and Formatting": f"{s2}/15",
            "III. References": f"{s3}/10",
            "IV. Content Depth": f"{s4}/45",
            "V. Academic Quality": f"{s5}/20",
        },
        "detailed_report": {
            "I. File Delivery (10 pts)": r1,
            "II. Report Structure and Formatting (15 pts)": r2,
            "III. Reference Standards (10 pts)": r3,
            "IV. Content Completeness and Depth (45 pts)": r4,
            "V. Academic Expression and Innovation (20 pts)": r5,
        },
    }

    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print formatted scoring report."""
    print("=" * 70)
    print("Speech Foundation Model Research Report — Scoring Report")
    print("=" * 70)
    print(f"\nTotal Score: {score}/100")
    print(f"Comment: {report.get('comment', '')}")

    scores = report.get("section_scores", {})
    if scores:
        print(f"\n{'─' * 40}")
        print("Section Scores:")
        for k, v in scores.items():
            print(f"  {k}: {v}")

    for sec_name, sec_data in report.get("detailed_report", {}).items():
        print(f"\n{'─' * 50}")
        print(f"[{sec_name}] {sec_data.get('score', '')}")
        print(f"{'─' * 50}")

        for k, v in sec_data.get("details", {}).items():
            if isinstance(v, dict):
                print(f"  {k}:")
                for kk, vv in v.items():
                    print(f"    {kk}: {vv}")
            else:
                print(f"  {k}: {v}")

        deds = sec_data.get("deductions", [])
        if deds:
            print("  Deductions:")
            for i, d in enumerate(deds, 1):
                print(f"    {i}. {d}")

    print(f"\n{'=' * 70}")


if __name__ == "__main__":
    import sys

    test_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(__file__), "..", "gpt-5", "attempt_1")

    if not os.path.exists(test_dir):
        test_dir = os.path.join(os.path.dirname(__file__), "..", "workspace")

    if os.path.exists(test_dir):
        print(f"Evaluating directory: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"Directory does not exist: {test_dir}")
    sys.exit(0)
