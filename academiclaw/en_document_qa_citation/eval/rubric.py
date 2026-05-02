"""
Rubric — nisong-query3: Evidence-based QA on Long Documents (with Page Citations)

Task overview:
  Agent needs to read context/the-state-of-ai-in-2025.pdf (McKinsey "The state of AI in 2025"),
  answer 4 questions in context/q.md, with each factual statement annotated with [Page N].
  If the document does not mention the answer to a question, must answer "Context mentions nothing about this".
  Deliverable: answers.md

Scoring (100 points, 25 per question):
  Q1 (25): Adoption rate change — 2023: 33%, 2024: 65%, with page citations
  Q2 (25): AI high-performance organization definition — EBIT over 10%, with page citations
  Q3 (25): Risk terminology and ranking — Inaccuracy, top/first, 63%, with page citations
  Q4 (25): Negative constraint — clear negative (Sora/Gemini have no benchmark scores), no fabrication
"""

import os
import re
import json
from typing import Tuple, Dict, Any, List

try:
    import openai
except ImportError:
    openai = None


# ---------------------------------------------------------------------------
# Environment / LLM Configuration
# ---------------------------------------------------------------------------

def _load_env(answer_dir: str) -> dict:
    """Read .env key-value pairs from answer_dir and query root directory"""
    values: Dict[str, str] = {}
    for d in [answer_dir, os.path.join(os.path.dirname(__file__), "..")]:
        p = os.path.join(d, ".env")
        if not os.path.exists(p):
            continue
        try:
            with open(p, "r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    key = k.strip()
                    if key not in values:
                        values[key] = v.strip().strip("'\"")
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
        print(f"[RUBRIC] LLM Judge error: {e}")
        return ""


# ---------------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------------

PAGE_CITE_RE = re.compile(r"\[\s*[Pp]age\s+\d+\s*\]")


def _find_answer_file(answer_dir: str) -> str:
    """Find the answer file in answer_dir, return content (empty string if not found)"""
    candidates = ["answers.md", "answer.md", "answers.txt", "answer.txt"]
    for name in candidates:
        fp = os.path.join(answer_dir, name)
        if os.path.isfile(fp):
            try:
                with open(fp, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception:
                pass
    return ""


def _split_answers(text: str) -> Dict[int, str]:
    """Split answers by number 1./2./3./4. into per-question text"""
    # Supports "1." "1:" "1)" "## 1." and similar numbering formats
    pat = re.compile(r"^\s*(?:#{1,3}\s*)?(\d+)\s*[\.\:、\)]\s", re.MULTILINE)
    matches = [(m.start(), int(m.group(1))) for m in pat.finditer(text)]
    if not matches:
        return {1: text}
    matches.append((len(text), None))
    sections: Dict[int, str] = {}
    for i in range(len(matches) - 1):
        start, num = matches[i]
        end = matches[i + 1][0]
        if isinstance(num, int) and 1 <= num <= 4:
            sections[num] = text[start:end].strip()
    return sections


def _has_citation(text: str) -> bool:
    return bool(PAGE_CITE_RE.search(text))


# ---------------------------------------------------------------------------
# Q1 — Adoption Rate Change (25 pts)
# ---------------------------------------------------------------------------

def _score_q1(text: str) -> Tuple[int, dict, List[str]]:
    """
    Scoring criteria:
      - 2023 value 33%  (10 pts)
      - 2024 value 65%  (10 pts)
      - Page citation [Page N] (5 pts)
    """
    pts = 0
    detail: Dict[str, str] = {}
    notes: List[str] = []

    # 33%
    if re.search(r"33\s*%", text):
        pts += 10
        detail["2023 value (33%)"] = "10/10"
    else:
        detail["2023 value (33%)"] = "0/10"
        notes.append("Q1: Missing 2023 value 33%")

    # 65%
    if re.search(r"65\s*%", text):
        pts += 10
        detail["2024 value (65%)"] = "10/10"
    else:
        detail["2024 value (65%)"] = "0/10"
        notes.append("Q1: Missing 2024 value 65%")

    # Citation
    if _has_citation(text):
        pts += 5
        detail["page_citation"] = "5/5"
    else:
        detail["page_citation"] = "0/5"
        notes.append("Q1: Missing [Page N] citation")

    return pts, detail, notes


# ---------------------------------------------------------------------------
# Q2 — AI High-Performance Organization Definition (25 pts)
# ---------------------------------------------------------------------------

def _score_q2(text: str) -> Tuple[int, dict, List[str]]:
    """
    Scoring criteria:
      - Mentions EBIT            (10 pts)
      - Threshold >10%           (10 pts, partial 5 pts if >5%)
      - Page citation            (5 pts)
    """
    pts = 0
    detail: Dict[str, str] = {}
    notes: List[str] = []
    lower = text.lower()

    # EBIT
    if "ebit" in lower:
        pts += 10
        detail["mentions EBIT"] = "10/10"
    else:
        detail["mentions EBIT"] = "0/10"
        notes.append("Q2: Did not mention EBIT")

    # Threshold
    threshold_scored = False
    # Exact match 10%
    if re.search(
        r"(?:超过|大于|>|more\s+than|over|exceed|至少|above)\s*10\s*%",
        text,
        re.IGNORECASE,
    ) or re.search(r"10\s*%", text):
        pts += 10
        detail["threshold (>10%)"] = "10/10"
        threshold_scored = True

    if not threshold_scored:
        # Partial credit: wrote >5%
        if re.search(r"(?:超过|大于|>)\s*5\s*%", text, re.IGNORECASE):
            pts += 5
            detail["threshold (>10%)"] = "5/10 (wrote >5%, partial credit)"
            notes.append("Q2: Threshold should be >10% EBIT, answer wrote >5%")
        else:
            detail["threshold (>10%)"] = "0/10"
            notes.append("Q2: Did not provide correct threshold >10% EBIT")

    # Citation
    if _has_citation(text):
        pts += 5
        detail["page_citation"] = "5/5"
    else:
        detail["page_citation"] = "0/5"
        notes.append("Q2: Missing [Page N] citation")

    return pts, detail, notes


# ---------------------------------------------------------------------------
# Q3 — Risk Terminology and Ranking (25 pts)
# ---------------------------------------------------------------------------

_RANK_FIRST_TOKENS = [
    "top risk", "top-ranked", "ranked first", "first", "#1", "no.1",
    "most commonly", "most frequently", "highest",
    "排名第一", "居于首位", "首位", "第一", "最高",
    "最常", "占比最高", "最为突出",
]


def _score_q3(text: str) -> Tuple[int, dict, List[str]]:
    """
    Scoring criteria:
      - Term Inaccuracy (8 pts)
      - Ranked highest / first         (7 pts)
      - Specific percentage 63%        (5 pts)
      - Page citation                  (5 pts)
    """
    pts = 0
    detail: Dict[str, str] = {}
    notes: List[str] = []
    lower = text.lower()

    # Term
    if "inaccuracy" in lower or "不准确" in text:
        pts += 8
        detail["risk_term (Inaccuracy)"] = "8/8"
    else:
        detail["risk_term (Inaccuracy)"] = "0/8"
        notes.append("Q3: Did not provide term Inaccuracy")

    # Ranking
    if any(tok in lower for tok in _RANK_FIRST_TOKENS):
        pts += 7
        detail["ranked_highest/first"] = "7/7"
    else:
        detail["ranked_highest/first"] = "0/7"
        notes.append("Q3: Did not clearly state this risk ranks first/highest")

    # 63%
    if re.search(r"63\s*%", text):
        pts += 5
        detail["specific_percentage (63%)"] = "5/5"
    else:
        detail["specific_percentage (63%)"] = "0/5"
        notes.append("Q3: Did not provide the 63% concern level data")

    # Citation
    if _has_citation(text):
        pts += 5
        detail["page_citation"] = "5/5"
    else:
        detail["page_citation"] = "0/5"
        notes.append("Q3: Missing [Page N] citation")

    return pts, detail, notes


# ---------------------------------------------------------------------------
# Q4 — Negative Constraint (25 pts)
# ---------------------------------------------------------------------------

_NEGATIVE_PHRASES = [
    "context mentions nothing about this",
    "no mention", "not mentioned", "does not mention",
    "未提及", "没有提到", "未涉及", "文档未提及",
    "没有列出", "未列出", "未提供", "没有提供",
    "没有涉及", "没有记载", "未给出",
]

_HALLUCINATION_RE = re.compile(
    r"(?:基准测试分数|benchmark\s*(?:test\s*)?score|具体.*分数|得分.*为|scored?\s+\d)",
    re.IGNORECASE,
)


def _score_q4(text: str) -> Tuple[int, dict, List[str]]:
    """
    Scoring criteria:
      - Provides clear negative answer (15 pts)
      - No fabricated benchmark scores  (10 pts)
    Total 25 pts. Fabricated content results in major deductions.
    """
    pts = 0
    detail: Dict[str, str] = {}
    notes: List[str] = []
    lower = text.lower()

    has_negative = any(ph in lower for ph in _NEGATIVE_PHRASES)

    # Detect fabrication: mentioning Sora/Gemini while providing specific scores
    has_hallucination = False
    if "sora" in lower or "gemini" in lower:
        if _HALLUCINATION_RE.search(text):
            has_hallucination = True
        if re.search(r"\b\d+[\.\d]*\s*%?\s*(?:分|score|point)", lower):
            has_hallucination = True

    if has_negative and not has_hallucination:
        pts = 25
        detail["negative_answer"] = "15/15"
        detail["no_fabrication"] = "10/10"
    elif has_negative and has_hallucination:
        pts = 5
        detail["negative_answer"] = "5/15 (contains fabricated content, major deduction)"
        detail["no_fabrication"] = "0/10"
        notes.append("Q4: Gave negative answer but still fabricated benchmark scores")
    elif not has_negative and not has_hallucination:
        pts = 0
        detail["negative_answer"] = "0/15"
        detail["no_fabrication"] = "0/10"
        notes.append("Q4: Did not provide clear negative answer (should answer 'Context mentions nothing about this')")
    else:
        pts = 0
        detail["negative_answer"] = "0/15"
        detail["no_fabrication"] = "0/10"
        notes.append("Q4: Did not give negative answer and fabricated benchmark scores")

    return pts, detail, notes


# ---------------------------------------------------------------------------
# LLM Auxiliary Verification (does not contribute to score, supplementary info only)
# ---------------------------------------------------------------------------

_LLM_VERIFY_PROMPT = """\
You are a strict document QA evaluation expert. Below are the agent's answers to 4 questions about the McKinsey "The state of AI in 2025" report.
Please judge factual correctness and page citation reasonableness for each question.

Reference points:
- Q1: In 2023, 33% of organizations "regularly use" generative AI; in 2024, 65%
- Q2: "AI high-performance organization" definition: EBIT attributable to AI exceeds 10%
- Q3: "Model producing incorrect information/hallucinations" term is Inaccuracy, 63% of respondents concerned, ranked first
- Q4: The report does not list specific benchmark test scores for OpenAI Sora or Google Gemini 1.5 Pro on video generation tasks; the correct answer should be negative

Agent's answers:
---
{answer_text}
---

Please return in JSON format (no other content):
```json
{{
  "q1_correct": true/false,
  "q1_comment": "brief explanation",
  "q2_correct": true/false,
  "q2_comment": "brief explanation",
  "q3_correct": true/false,
  "q3_comment": "brief explanation",
  "q4_correct": true/false,
  "q4_comment": "brief explanation",
  "overall_quality": "excellent/good/fair/poor"
}}
```"""


def _llm_verify(answer_text: str, config: dict) -> dict:
    raw = _call_llm_judge(
        _LLM_VERIFY_PROMPT.format(answer_text=answer_text[:3000]), config
    )
    if not raw:
        return {}
    try:
        if "```json" in raw:
            raw = raw.split("```json")[1].split("```")[0].strip()
        elif "```" in raw:
            raw = raw.split("```")[1].split("```")[0].strip()
        return json.loads(raw)
    except Exception:
        return {"raw": raw[:500]}


# ---------------------------------------------------------------------------
# Main Entry
# ---------------------------------------------------------------------------

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Evaluate the agent's output.

    Args:
        answer_dir: absolute path to the agent output directory (e.g., .../gpt-5/attempt_1)

    Returns:
        (score, report) — score: 0-100 integer; report: detailed evaluation report dict
    """
    content = _find_answer_file(answer_dir)

    # ---------- File missing ----------
    if not content.strip():
        return 0, {
            "total_score": 0,
            "result_score": {
                "score": 0,
                "details": {},
                "deductions": ["answers.md file not found or is empty"],
            },
            "process_score": {"score": 0, "details": {}, "deductions": []},
            "comment": "Failing: Answer file is missing.",
        }

    # ---------- Split each question ----------
    sections = _split_answers(content)
    all_details: Dict[str, Any] = {}
    all_notes: List[str] = []

    q1_pts, q1_det, q1_n = _score_q1(sections.get(1, ""))
    all_details["Q1 Adoption Rate Change (25 pts)"] = {"score": q1_pts, **q1_det}
    all_notes.extend(q1_n)

    q2_pts, q2_det, q2_n = _score_q2(sections.get(2, ""))
    all_details["Q2 High-Performance Org Definition (25 pts)"] = {"score": q2_pts, **q2_det}
    all_notes.extend(q2_n)

    q3_pts, q3_det, q3_n = _score_q3(sections.get(3, ""))
    all_details["Q3 Risk Terminology & Ranking (25 pts)"] = {"score": q3_pts, **q3_det}
    all_notes.extend(q3_n)

    q4_pts, q4_det, q4_n = _score_q4(sections.get(4, ""))
    all_details["Q4 Negative Constraint (25 pts)"] = {"score": q4_pts, **q4_det}
    all_notes.extend(q4_n)

    total = q1_pts + q2_pts + q3_pts + q4_pts

    # ---------- Paragraph parsing diagnostics ----------
    parsed = {f"Q{i}": ("parsed" if i in sections else "not found") for i in range(1, 5)}
    if len(sections) < 4:
        all_notes.append(f"Answer format issue: only parsed {len(sections)} numbered paragraph(s) (expected 4)")

    # ---------- LLM auxiliary verification ----------
    llm_info: dict = {}
    try:
        cfg = _get_text_eval_config(answer_dir)
        if cfg.get("api_key"):
            llm_info = _llm_verify(content, cfg)
    except Exception:
        pass

    # ---------- Comment ----------
    if total >= 90:
        comment = "Excellent: Answers are complete, facts are accurate, citations are well-formatted."
    elif total >= 75:
        comment = "Good: Core points are correct, some details or citations could be improved."
    elif total >= 60:
        comment = "Passing: Main requirements met, but key information is missing or citations are non-standard."
    elif total >= 40:
        comment = "Partially complete: Multiple key pieces of information are missing."
    else:
        comment = "Failing: Key information is largely missing or fabricated content is present."

    report: Dict[str, Any] = {
        "total_score": total,
        "result_score": {
            "score": total,
            "details": all_details,
            "deductions": all_notes,
        },
        "process_score": {"score": 0, "details": {}, "deductions": []},
        "comment": comment,
    }
    if parsed:
        report["paragraph_parsing"] = parsed
    if llm_info:
        report["LLM_auxiliary_verification"] = llm_info

    return total, report


# ---------------------------------------------------------------------------
# Report Output
# ---------------------------------------------------------------------------

def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print a formatted scoring report"""
    print("=" * 70)
    print("Scoring Report: nisong-query3 — Evidence-based QA on Long Documents (with Page Citations)")
    print("=" * 70)
    print(f"Total Score: {score}/100\n")

    res = report.get("result_score", {})
    details = res.get("details", {})
    for section_name, det in details.items():
        if isinstance(det, dict):
            pts = det.get("score", "?")
            print(f"  {section_name}: {pts}")
            for k, v in det.items():
                if k != "score":
                    print(f"    - {k}: {v}")
        else:
            print(f"  {section_name}: {det}")
        print()

    notes = res.get("deductions", [])
    if notes:
        print("Deductions:")
        for i, n in enumerate(notes, 1):
            print(f"  {i}. {n}")
        print()

    parsed = report.get("paragraph_parsing", {})
    if parsed:
        print("Paragraph parsing:", ", ".join(f"{k}={v}" for k, v in parsed.items()))

    llm = report.get("LLM_auxiliary_verification", {})
    if llm and "raw" not in llm:
        print("\nLLM Auxiliary Verification:")
        for k, v in llm.items():
            print(f"  {k}: {v}")

    print(f"\nComment: {report.get('comment', '')}")
    print("=" * 70)


# ---------------------------------------------------------------------------
# CLI Entry
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    test_dir = (
        sys.argv[1]
        if len(sys.argv) > 1
        else os.path.join(os.path.dirname(__file__), "..", "gpt-5", "attempt_1")
    )
    if os.path.exists(test_dir):
        print(f"Evaluating directory: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"Directory does not exist: {test_dir}")
    sys.exit(0)
