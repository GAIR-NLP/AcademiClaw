"""
Rubric for xiazhou-query3: 生物信息学综述报告撰写

Task: Agent must read a courseware PDF on "生物数据库及其检索" (biological databases
and retrieval), pick a related topic, and write a ≥5000-Chinese-character review
report as PDF.  References must come only from sites listed in context/link.md:
  Google Scholar, CNKI, Google, Wikipedia, PubMed.

Scoring (100 pts total):
  1. File Delivery          (10)
  2. Word Count             (10)
  3. Format Completeness    (20)
  4. Content Quality — LLM  (35)
  5. References             (25)
"""

import os
import re
import sys
import json
from typing import Tuple, Dict, Any, List

try:
    import openai
except ImportError:
    openai = None


# ============================================================================
# Environment / LLM helpers
# ============================================================================

def _load_env(answer_dir: str) -> dict:
    """Load .env from answer_dir first, then from the query root."""
    values: Dict[str, str] = {}
    query_root = os.path.join(os.path.dirname(__file__), "..")
    for env_dir in [answer_dir, query_root]:
        env_path = os.path.join(env_dir, ".env")
        if not os.path.exists(env_path):
            continue
        try:
            with open(env_path, "r", encoding="utf-8") as fh:
                for line in fh:
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
    env = _load_env(answer_dir)

    def g(key: str, default: str = "") -> str:
        return os.environ.get(key) or env.get(key) or default

    return {
        "api_key": g("EVAL_TEXT_API_KEY", g("ANTHROPIC_API_KEY")),
        "api_base": g("EVAL_TEXT_API_BASE_URL", g("ANTHROPIC_BASE_URL")),
        "model": g("EVAL_TEXT_MODEL", "openai/gpt-5.2"),
    }


def _call_llm_judge(prompt: str, config: dict) -> str:
    """Call LLM for text evaluation.  Returns empty string on failure."""
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
            max_tokens=3000,
            temperature=0,
        )
        return resp.choices[0].message.content.strip()
    except Exception as exc:
        print(f"[RUBRIC] LLM Judge call failed: {exc}")
        return ""


# ============================================================================
# PDF / text extraction
# ============================================================================

def _extract_pdf_text(pdf_path: str) -> str:
    """Extract text from a PDF file using available libraries."""
    for _try_fn in [_try_pypdf2, _try_pdfplumber, _try_pdfminer]:
        text = _try_fn(pdf_path)
        if text.strip():
            return text
    return ""


def _try_pypdf2(path: str) -> str:
    try:
        import PyPDF2
        with open(path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            parts = []
            for page in reader.pages:
                t = page.extract_text()
                if t:
                    parts.append(t)
            return "\n".join(parts)
    except Exception:
        return ""


def _try_pdfplumber(path: str) -> str:
    try:
        import pdfplumber
        with pdfplumber.open(path) as pdf:
            parts = []
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    parts.append(t)
            return "\n".join(parts)
    except Exception:
        return ""


def _try_pdfminer(path: str) -> str:
    try:
        from pdfminer.high_level import extract_text
        return extract_text(path)
    except Exception:
        return ""


# ============================================================================
# Small helpers
# ============================================================================

def _count_chinese_chars(text: str) -> int:
    """Count CJK Unified Ideographs."""
    return sum(1 for ch in text if "\u4e00" <= ch <= "\u9fff")


def _find_report(answer_dir: str) -> Tuple[str, str]:
    """Locate the report file.  Returns (abs_path, type) where type is
    'pdf', 'md', 'txt', or '' if not found."""
    if not os.path.isdir(answer_dir):
        return "", ""
    files = os.listdir(answer_dir)

    # Priority 1: report.pdf
    if "report.pdf" in files:
        return os.path.join(answer_dir, "report.pdf"), "pdf"

    # Priority 2: any PDF
    for f in sorted(files):
        if f.lower().endswith(".pdf"):
            return os.path.join(answer_dir, f), "pdf"

    # Priority 3: markdown (skip query.md, readme.md)
    skip = {"query.md", "readme.md", "task_prompt.md"}
    for f in sorted(files):
        if f.lower().endswith((".md", ".markdown")) and f.lower() not in skip:
            return os.path.join(answer_dir, f), "md"

    # Priority 4: txt
    for f in sorted(files):
        if f.lower().endswith(".txt") and not f.lower().startswith("evaluation"):
            return os.path.join(answer_dir, f), "txt"

    return "", ""


def _read_text_file(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


# ============================================================================
# Dimension 1 — File Delivery (10 pts)
# ============================================================================

def _eval_file_delivery(answer_dir: str) -> Tuple[int, dict]:
    """
    10 pts total:
      - PDF file exists (4 pts; non-PDF formats get 1 pt)
      - Named exactly report.pdf (3 pts; wrong name 1 pt)
      - Valid non-trivial file (3 pts based on size)
    """
    score = 0
    details: Dict[str, str] = {}

    path, ftype = _find_report(answer_dir)
    if not path:
        details["verdict"] = "0/10 — No report file found"
        return 0, details

    basename = os.path.basename(path)
    details["file"] = basename
    details["type"] = ftype

    if ftype == "pdf":
        score += 4
        details["format"] = "4/4 — PDF found"
    else:
        score += 1
        details["format"] = f"1/4 — Found {ftype} instead of PDF"

    if basename == "report.pdf":
        score += 3
        details["name"] = "3/3 — Exact name report.pdf"
    elif ftype == "pdf":
        score += 1
        details["name"] = f"1/3 — PDF but named {basename}"
    else:
        details["name"] = "0/3 — Not named report.pdf"

    fsize = os.path.getsize(path)
    if fsize >= 10240:
        score += 3
        details["size"] = f"3/3 — {fsize // 1024} KB"
    elif fsize >= 2048:
        score += 1
        details["size"] = f"1/3 — {fsize // 1024} KB (small)"
    else:
        details["size"] = f"0/3 — {fsize} B (too small)"

    return min(score, 10), details


# ============================================================================
# Dimension 2 — Word Count (10 pts)
# ============================================================================

def _eval_word_count(text: str) -> Tuple[int, dict]:
    """
    10 pts:
      >=5000 → 10
      4500-4999 → 8
      4000-4499 → 6
      3500-3999 → 4
      3000-3499 → 2
      <3000 → 0
    """
    cc = _count_chinese_chars(text)
    details = {"chinese_chars": cc}

    if cc >= 5000:
        s = 10
    elif cc >= 4500:
        s = 8
    elif cc >= 4000:
        s = 6
    elif cc >= 3500:
        s = 4
    elif cc >= 3000:
        s = 2
    else:
        s = 0

    details["verdict"] = f"{s}/10 — {cc} Chinese chars"
    return s, details


# ============================================================================
# Dimension 3 — Format Completeness (20 pts)
# ============================================================================

def _eval_format(text: str) -> Tuple[int, dict]:
    """
    20 pts (5 each for Abstract, Body sections, Conclusion, References):
    """
    score = 0
    details: Dict[str, str] = {}

    # --- 3a. Abstract (5) ---
    abstract_markers = ["摘要", "摘 要", "Abstract", "ABSTRACT"]
    found_abstract = any(m in text for m in abstract_markers)
    if found_abstract:
        # Estimate abstract length
        for m in abstract_markers:
            idx = text.find(m)
            if idx >= 0:
                snippet = text[idx:idx + 1200]
                ac = _count_chinese_chars(snippet)
                break
        else:
            ac = 0
        if ac >= 100:
            score += 5
            details["abstract"] = f"5/5 — Present (~{ac} chars)"
        elif ac >= 30:
            score += 3
            details["abstract"] = f"3/5 — Present but short (~{ac} chars)"
        else:
            score += 2
            details["abstract"] = "2/5 — Marker found but very brief"
    else:
        details["abstract"] = "0/5 — Not found"

    # --- 3b. Body with sections (5) ---
    heading_re = re.compile(
        r"(?:^|\n)\s*(?:"
        r"#{1,3}\s"
        r"|第[一二三四五六七八九十\d]+[章节]"
        r"|[\d]+[\.、]\s"
        r"|[一二三四五六七八九十]+[、\.]"
        r")"
    )
    headings = heading_re.findall(text)
    nh = len(headings)
    if nh >= 5:
        score += 5
        details["body"] = f"5/5 — {nh} section headings"
    elif nh >= 3:
        score += 4
        details["body"] = f"4/5 — {nh} section headings"
    elif nh >= 1:
        score += 2
        details["body"] = f"2/5 — {nh} heading(s)"
    else:
        body_kws = ["引言", "介绍", "背景", "正文", "Introduction"]
        if any(kw in text for kw in body_kws):
            score += 2
            details["body"] = "2/5 — Body keywords found, no clear sections"
        else:
            details["body"] = "0/5 — No section structure detected"

    # --- 3c. Conclusion (5) ---
    conclusion_kws = ["总结", "结论", "结语", "Conclusion", "CONCLUSION", "Summary", "展望"]
    found_conclusion = [kw for kw in conclusion_kws if kw in text]
    if found_conclusion:
        # Should be in latter half
        text_len = len(text)
        pos = min(text.find(kw) for kw in found_conclusion)
        if pos > text_len * 0.4:
            score += 5
            details["conclusion"] = "5/5 — Found in latter portion"
        else:
            score += 3
            details["conclusion"] = "3/5 — Keyword found but early"
    else:
        details["conclusion"] = "0/5 — Not found"

    # --- 3d. References section (5) ---
    ref_kws = ["参考文献", "References", "REFERENCES", "参考资料", "引用文献"]
    found_ref = any(kw in text for kw in ref_kws)
    if found_ref:
        numbered = re.findall(r"\[\d+\]", text)
        unique_num = len(set(numbered))
        if unique_num >= 5:
            score += 5
            details["references"] = f"5/5 — Section present, {unique_num} numbered entries"
        elif unique_num >= 1:
            score += 4
            details["references"] = f"4/5 — Section present, {unique_num} numbered entry(ies)"
        else:
            score += 3
            details["references"] = "3/5 — Section present, entries not clearly numbered"
    else:
        details["references"] = "0/5 — Not found"

    return min(score, 20), details


# ============================================================================
# Dimension 4 — Content Quality (35 pts) via LLM-as-Judge
# ============================================================================

_CONTENT_PROMPT = """\
你是一位生物信息学课程的评审专家。请评估以下学生撰写的与"生物数据库及其检索"相关的综述报告。

## 评分维度（严格打分，总计 35 分）

### A. 主题选择与相关性 (0-10 分)
- 10: 主题明确来自课件"生物数据库及其检索"内容，高度相关，有深度展开价值
- 7-9: 与课件内容相关，但不够紧密
- 4-6: 有一定关联但偏离较远
- 0-3: 与课件内容无关

### B. 内容准确性 (0-10 分)
- 10: 技术描述准确，研究进展介绍正确，无明显错误
- 7-9: 大部分准确，有少量不准确
- 4-6: 有较多不准确之处
- 0-3: 严重错误

### C. 内容深度 (0-8 分)
- 8: 深入介绍关键技术/方法/突破，有深入分析
- 5-7: 有一定深度但某些方面不够
- 2-4: 较浅，主要是表面介绍
- 0-1: 极其浅显

### D. 内容广度 (0-7 分)
- 7: 全面涵盖主要研究进展、技术突破、应用场景
- 5-6: 较全面但遗漏某些方面
- 2-4: 不够全面
- 0-1: 极其片面

## 报告内容（已截取前12000字符）

{report_text}

## 输出要求

严格按以下 JSON 格式输出，不要包含任何其他文字：
```json
{{
  "topic_relevance": {{"score": 0, "reason": "..."}},
  "accuracy": {{"score": 0, "reason": "..."}},
  "depth": {{"score": 0, "reason": "..."}},
  "breadth": {{"score": 0, "reason": "..."}},
  "total": 0,
  "overall_comment": "..."
}}
```
"""


def _eval_content_quality(text: str, config: dict) -> Tuple[int, dict]:
    """35 pts via LLM, with rule-based fallback."""
    details: Dict[str, Any] = {}

    # Truncate to ~12k chars for context limits
    truncated = text[:12000]
    prompt = _CONTENT_PROMPT.format(report_text=truncated)
    llm_raw = _call_llm_judge(prompt, config)

    if llm_raw:
        try:
            m = re.search(r"\{[\s\S]*\}", llm_raw)
            if not m:
                raise ValueError("No JSON found in LLM response")
            result = json.loads(m.group(0))

            topic = max(0, min(10, int(result.get("topic_relevance", {}).get("score", 0))))
            accuracy = max(0, min(10, int(result.get("accuracy", {}).get("score", 0))))
            depth = max(0, min(8, int(result.get("depth", {}).get("score", 0))))
            breadth = max(0, min(7, int(result.get("breadth", {}).get("score", 0))))
            total = topic + accuracy + depth + breadth

            details["A_topic"] = f"{topic}/10 — {result.get('topic_relevance', {}).get('reason', '')}"
            details["B_accuracy"] = f"{accuracy}/10 — {result.get('accuracy', {}).get('reason', '')}"
            details["C_depth"] = f"{depth}/8 — {result.get('depth', {}).get('reason', '')}"
            details["D_breadth"] = f"{breadth}/7 — {result.get('breadth', {}).get('reason', '')}"
            details["overall_comment"] = result.get("overall_comment", "")
            details["method"] = "LLM-as-Judge"
            return min(total, 35), details
        except Exception as exc:
            print(f"[RUBRIC] LLM response parse error: {exc}")
            details["llm_parse_error"] = str(exc)

    # ---- Fallback: rule-based (conservative, max ~20/35) ----
    return _content_fallback(text, details)


def _content_fallback(text: str, details: dict) -> Tuple[int, dict]:
    """Conservative keyword-based estimation when LLM is unavailable."""
    score = 0
    text_lower = text.lower()

    bio_db_kws = [
        "数据库", "检索", "bioinformatics", "database", "NCBI", "UniProt",
        "PubMed", "GenBank", "BLAST", "序列", "基因", "蛋白质", "genome",
        "protein", "核酸", "DNA", "RNA", "基因组", "Swiss-Prot", "DDBJ",
        "EMBL", "Ensembl", "GO", "KEGG", "生物信息",
    ]
    kw_hits = sum(1 for kw in bio_db_kws if kw.lower() in text_lower)
    if kw_hits >= 10:
        topic = 7
    elif kw_hits >= 6:
        topic = 5
    elif kw_hits >= 3:
        topic = 3
    else:
        topic = 1
    score += topic
    details["A_topic"] = f"{topic}/10 — {kw_hits} bio-DB keywords (fallback)"

    # Accuracy: conservative
    acc = 5
    score += acc
    details["B_accuracy"] = f"{acc}/10 — conservative (no LLM)"

    depth_kws = [
        "算法", "方法", "架构", "原理", "机制", "技术", "分析", "比较",
        "优势", "局限", "应用", "发展", "研究进展", "突破", "创新", "实现",
    ]
    depth_hits = sum(1 for kw in depth_kws if kw in text)
    if depth_hits >= 8:
        dep = 4
    elif depth_hits >= 4:
        dep = 3
    else:
        dep = 1
    score += dep
    details["C_depth"] = f"{dep}/8 — {depth_hits} depth indicators (fallback)"

    brd = 3
    score += brd
    details["D_breadth"] = f"{brd}/7 — conservative (no LLM)"

    details["method"] = "Rule-based fallback (LLM unavailable)"
    return min(score, 35), details


# ============================================================================
# Dimension 5 — References (25 pts)
# ============================================================================

# Allowed reference source domains
_ALLOWED_DOMAINS = [
    "scholar.google",
    "cnki.net",
    "google.com",
    "google.com.hk",
    "wikipedia.org",
    "pubmed.ncbi.nlm.nih.gov",
    "ncbi.nlm.nih.gov",
]


def _eval_references(text: str) -> Tuple[int, dict]:
    """
    25 pts:
      A. Source compliance  (10)
      B. Relevance          (8)
      C. Quantity & quality  (7)
    """
    score = 0
    details: Dict[str, Any] = {}

    # Locate references section
    ref_section = ""
    for kw in ["参考文献", "References", "REFERENCES", "参考资料"]:
        idx = text.find(kw)
        if idx >= 0:
            ref_section = text[idx:]
            break

    if not ref_section:
        details["compliance"] = "0/10 — No references section"
        details["relevance"] = "0/8 — No references"
        details["quantity"] = "0/7 — No references"
        return 0, details

    # --- Count references ---
    numbered_entries = set(re.findall(r"\[\d+\]", ref_section))
    num_refs = len(numbered_entries)
    # Also count by non-trivial lines in the reference section
    ref_lines = [
        ln.strip() for ln in ref_section.split("\n")
        if ln.strip() and len(ln.strip()) > 20
    ]
    estimated_count = max(num_refs, len(ref_lines) - 1)  # -1 for header

    # --- 5C. Quantity & quality (7 pts) ---
    if estimated_count >= 10:
        qty = 7
    elif estimated_count >= 7:
        qty = 5
    elif estimated_count >= 5:
        qty = 4
    elif estimated_count >= 3:
        qty = 2
    elif estimated_count >= 1:
        qty = 1
    else:
        qty = 0
    score += qty
    details["quantity"] = f"{qty}/7 — ~{estimated_count} references"

    # --- 5A. Source compliance (10 pts) ---
    urls_in_refs = re.findall(r"https?://[^\s\)\]>\"']+", ref_section)

    if urls_in_refs:
        compliant = sum(
            1 for u in urls_in_refs
            if any(d in u for d in _ALLOWED_DOMAINS)
        )
        total_urls = len(urls_in_refs)
        ratio = compliant / total_urls

        if ratio >= 0.9:
            comp = 10
        elif ratio >= 0.7:
            comp = 7
        elif ratio >= 0.5:
            comp = 5
        elif ratio >= 0.3:
            comp = 3
        else:
            comp = 1

        non_compliant = [
            u[:60] for u in urls_in_refs
            if not any(d in u for d in _ALLOWED_DOMAINS)
        ][:3]
        details["compliance"] = f"{comp}/10 — {compliant}/{total_urls} URLs compliant ({ratio:.0%})"
        if non_compliant:
            details["non_compliant_samples"] = non_compliant
    else:
        # No URLs — references may be standard academic citations without links.
        # Check if they look academic.
        academic_re = re.compile(
            r"(?:et\s+al|等\s*[\.,]|journal|期刊|IEEE|ACM|Nature|Science|PLoS|BMC|"
            r"Nucleic\s+Acids|Bioinformatics|Genome|年)",
            re.IGNORECASE,
        )
        if academic_re.search(ref_section):
            comp = 6
            details["compliance"] = (
                "6/10 — No URLs, references look academic; cannot verify domains"
            )
        else:
            comp = 4
            details["compliance"] = "4/10 — No URLs and references don't look academic"
    score += comp

    # --- 5B. Relevance (8 pts) ---
    bio_kws = [
        "生物", "基因", "蛋白", "数据库", "序列", "genome", "protein",
        "bioinformatics", "database", "gene", "molecular", "NCBI",
        "nucleotide", "BLAST", "alignment", "分子",
    ]
    ref_lower = ref_section.lower()
    bio_hits = sum(1 for kw in bio_kws if kw.lower() in ref_lower)

    if bio_hits >= 6:
        rel = 8
    elif bio_hits >= 3:
        rel = 5
    elif bio_hits >= 1:
        rel = 3
    else:
        rel = 1
    score += rel
    details["relevance"] = f"{rel}/8 — {bio_hits} bio-related keywords in references"

    return min(score, 25), details


# ============================================================================
# Main evaluate()
# ============================================================================

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Evaluate the agent's bioinformatics review report.

    Args:
        answer_dir: Absolute path to the agent's output directory.

    Returns:
        (score, report) where score is 0-100.
    """
    report: Dict[str, Any] = {"dimensions": {}, "deductions": [], "summary": ""}

    print("[RUBRIC] Evaluating xiazhou-query3: 生物信息学综述报告")
    print("=" * 60)

    # ---- 1. File Delivery (10) ----
    print("\n[1/5] File delivery …")
    s1, d1 = _eval_file_delivery(answer_dir)
    report["dimensions"]["1_file_delivery"] = {"score": s1, "max": 10, "details": d1}
    print(f"  Score: {s1}/10")

    # ---- Load text ----
    path, ftype = _find_report(answer_dir)
    if path and ftype == "pdf":
        text = _extract_pdf_text(path)
        # If PDF extraction yields no Chinese chars, fall back to .md/.txt
        if _count_chinese_chars(text) == 0:
            print("  WARNING: PDF text extraction returned 0 Chinese chars — trying fallback to .md/.txt")
            md_fallback = ""
            skip = {"query.md", "readme.md", "task_prompt.md"}
            for f in sorted(os.listdir(answer_dir)):
                if f.lower().endswith((".md", ".markdown")) and f.lower() not in skip:
                    md_fallback = _read_text_file(os.path.join(answer_dir, f))
                    if _count_chinese_chars(md_fallback) > 0:
                        print(f"  Fallback to {f}: {_count_chinese_chars(md_fallback)} Chinese chars")
                        text = md_fallback
                        break
            if _count_chinese_chars(text) == 0:
                for f in sorted(os.listdir(answer_dir)):
                    if f.lower().endswith(".txt") and not f.lower().startswith("evaluation"):
                        txt_fallback = _read_text_file(os.path.join(answer_dir, f))
                        if _count_chinese_chars(txt_fallback) > 0:
                            print(f"  Fallback to {f}: {_count_chinese_chars(txt_fallback)} Chinese chars")
                            text = txt_fallback
                            break
    elif path:
        text = _read_text_file(path)
    else:
        text = ""

    if not text.strip():
        print("  WARNING: Could not extract text from report!")
        report["deductions"].append("Failed to extract text — only file delivery scored")
        report["summary"] = "Report text unreadable."
        return s1, report

    cc = _count_chinese_chars(text)
    print(f"  Extracted {len(text)} chars ({cc} Chinese)")

    # ---- 2. Word Count (10) ----
    print("\n[2/5] Word count …")
    s2, d2 = _eval_word_count(text)
    report["dimensions"]["2_word_count"] = {"score": s2, "max": 10, "details": d2}
    print(f"  Score: {s2}/10  ({cc} Chinese chars)")

    # ---- 3. Format Completeness (20) ----
    print("\n[3/5] Format completeness …")
    s3, d3 = _eval_format(text)
    report["dimensions"]["3_format"] = {"score": s3, "max": 20, "details": d3}
    print(f"  Score: {s3}/20")

    # ---- 4. Content Quality (35) ----
    print("\n[4/5] Content quality (LLM-as-Judge) …")
    config = _get_text_eval_config(answer_dir)
    s4, d4 = _eval_content_quality(text, config)
    report["dimensions"]["4_content_quality"] = {"score": s4, "max": 35, "details": d4}
    print(f"  Score: {s4}/35  [{d4.get('method', 'unknown')}]")

    # ---- 5. References (25) ----
    print("\n[5/5] References …")
    s5, d5 = _eval_references(text)
    report["dimensions"]["5_references"] = {"score": s5, "max": 25, "details": d5}
    print(f"  Score: {s5}/25")

    # ---- Total ----
    total = max(0, min(100, s1 + s2 + s3 + s4 + s5))

    if total >= 85:
        report["summary"] = "Excellent bioinformatics review report."
    elif total >= 70:
        report["summary"] = "Good report with room for improvement."
    elif total >= 55:
        report["summary"] = "Adequate report but with notable deficiencies."
    elif total >= 30:
        report["summary"] = "Incomplete report with significant issues."
    else:
        report["summary"] = "Report is severely deficient or missing."

    print(f"\n{'=' * 60}")
    print(f"TOTAL SCORE: {total}/100")
    print(f"{'=' * 60}")

    return total, report


# ============================================================================
# print_report()
# ============================================================================

def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print a formatted evaluation report."""
    print("\n" + "=" * 60)
    print("Bioinformatics Review Report — xiazhou-query3")
    print("=" * 60)
    print(f"\nTotal Score: {score}/100")
    print(f"Summary: {report.get('summary', '')}")

    dims = report.get("dimensions", {})
    for key in sorted(dims.keys()):
        dim = dims[key]
        print(f"\n--- {key} ({dim['score']}/{dim['max']}) ---")
        for k, v in dim.get("details", {}).items():
            if isinstance(v, list):
                print(f"  {k}:")
                for item in v:
                    print(f"    - {item}")
            else:
                print(f"  {k}: {v}")

    deductions = report.get("deductions", [])
    if deductions:
        print("\nDeductions:")
        for d in deductions:
            print(f"  - {d}")

    print("=" * 60)


# ============================================================================
# CLI entry
# ============================================================================

if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_dir = sys.argv[1]
    else:
        test_dir = os.path.join(os.path.dirname(__file__), "..", "gpt-5", "attempt_1")

    if not os.path.isabs(test_dir):
        test_dir = os.path.join(os.getcwd(), test_dir)

    if os.path.exists(test_dir):
        print(f"Evaluating: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"Directory not found: {test_dir}")
    sys.exit(0)
