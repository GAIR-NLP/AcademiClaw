#!/usr/bin/env python3
"""
Scoring Script: Extract Task List from Meeting Minutes
Total: 100 points

Scoring Dimensions:
  1. File Delivery (10 pts)
      - action_items.json exists and parseable (4 pts)
      - dependency_graph.json exists and parseable (3 pts)
      - transcript.txt exists and non-empty (3 pts)

  2. Structural Validity (20 pts)
      - action_items is a non-empty list (3 pts)
      - Each item contains all required fields (5 pts)
      - task_id unique and non-empty (3 pts)
      - dependency_graph contains edges array (3 pts)
      - edges reference task_ids that exist in action_items (3 pts)
      - Dependency graph is a DAG (acyclic) (3 pts)

  3. Span Grounding (25 pts)
      - source_span format is valid (5 pts)
      - Action item content corresponds to transcript text (20 pts) - LLM evaluation

  4. Content Quality (30 pts)
      - Action item extraction reasonableness (15 pts) - LLM evaluation
      - Dependency relationship reasonableness (15 pts) - LLM evaluation

  5. Extraction Standards (15 pts)
      - Reasonable task density (5 pts)
      - No duplicates/redundancy (5 pts)
      - Consistent deadline format (5 pts)
"""

from __future__ import annotations

import json
import os
import re
from typing import Any, Dict, List, Tuple

try:
    import openai
except ImportError:
    openai = None


# ─────────────────────────────────────────────────────────────────────
# Environment and LLM Utilities
# ─────────────────────────────────────────────────────────────────────

def _load_env(answer_dir: str) -> dict:
    """Load .env configuration from answer_dir and query root directory"""
    values: Dict[str, str] = {}
    for env_dir in [answer_dir, os.path.join(os.path.dirname(__file__), "..")]:
        env_path = os.path.join(env_dir, ".env")
        if os.path.exists(env_path):
            with open(env_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    if k.strip() not in values:
                        values[k.strip()] = v.strip().strip("'\"")
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
    """Parse JSON from LLM response"""
    if not text:
        return {}
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0].strip()
    elif "```" in text:
        text = text.split("```")[1].split("```")[0].strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", text, re.DOTALL)
        if m:
            try:
                return json.loads(m.group())
            except json.JSONDecodeError:
                pass
    return {}


# ─────────────────────────────────────────────────────────────────────
# 1. File Delivery (10 pts)
# ─────────────────────────────────────────────────────────────────────

REQUIRED_ITEM_FIELDS = {"task_id", "assignee", "action", "object", "deadline", "source_span"}


def _check_deliverables(answer_dir: str) -> Tuple[int, Dict[str, Any], dict]:
    """Check whether the three deliverable files exist and are parseable.
    Returns (score, details, loaded_data)"""
    score = 0
    details: Dict[str, Any] = {}
    data: Dict[str, Any] = {
        "action_items": None,
        "dependency_graph": None,
        "transcript": None,
    }

    # action_items.json (4 pts)
    ai_path = os.path.join(answer_dir, "action_items.json")
    if os.path.isfile(ai_path):
        try:
            with open(ai_path, "r", encoding="utf-8") as f:
                data["action_items"] = json.load(f)
            score += 4
            details["action_items.json"] = "4/4 Exists and parseable"
        except Exception as e:
            score += 1
            details["action_items.json"] = f"1/4 File exists but parsing failed: {e}"
    else:
        details["action_items.json"] = "0/4 File does not exist"

    # dependency_graph.json (3 pts)
    dg_path = os.path.join(answer_dir, "dependency_graph.json")
    if os.path.isfile(dg_path):
        try:
            with open(dg_path, "r", encoding="utf-8") as f:
                data["dependency_graph"] = json.load(f)
            score += 3
            details["dependency_graph.json"] = "3/3 Exists and parseable"
        except Exception as e:
            score += 1
            details["dependency_graph.json"] = f"1/3 File exists but parsing failed: {e}"
    else:
        details["dependency_graph.json"] = "0/3 File does not exist"

    # transcript.txt (3 pts)
    tr_path = os.path.join(answer_dir, "transcript.txt")
    if os.path.isfile(tr_path):
        try:
            with open(tr_path, "r", encoding="utf-8") as f:
                text = f.read().strip()
            if len(text) > 20:
                data["transcript"] = text
                score += 3
                details["transcript.txt"] = f"3/3 Exists, {len(text)} characters"
            else:
                score += 1
                details["transcript.txt"] = f"1/3 File too short ({len(text)} characters)"
        except Exception as e:
            score += 1
            details["transcript.txt"] = f"1/3 File exists but read failed: {e}"
    else:
        details["transcript.txt"] = "0/3 File does not exist"

    return score, details, data


# ─────────────────────────────────────────────────────────────────────
# 2. Structural Validity (20 pts)
# ─────────────────────────────────────────────────────────────────────

def _check_structure(data: dict) -> Tuple[int, Dict[str, Any]]:
    score = 0
    details: Dict[str, Any] = {}

    ai = data.get("action_items")
    dg = data.get("dependency_graph")

    # 2.1 action_items is a non-empty list (3 pts)
    if isinstance(ai, list) and len(ai) > 0:
        score += 3
        details["action_items_format"] = f"3/3 List with {len(ai)} items"
    elif isinstance(ai, list):
        details["action_items_format"] = "0/3 Empty list"
        return score, details
    else:
        details["action_items_format"] = "0/3 Not a list or is null"
        return score, details

    # 2.2 Each item contains all required fields (5 pts)
    total = len(ai)
    complete = sum(1 for item in ai if REQUIRED_ITEM_FIELDS.issubset(set(item.keys())))
    ratio = complete / total if total else 0
    field_score = round(ratio * 5)
    score += field_score
    details["required_fields"] = f"{field_score}/5 ({complete}/{total} items contain all fields)"

    # 2.3 task_id unique and non-empty (3 pts)
    ids = [item.get("task_id") for item in ai if item.get("task_id")]
    if ids and len(ids) == len(set(ids)) and len(ids) == total:
        score += 3
        details["unique_ids"] = "3/3 All task_ids are unique and non-empty"
    elif ids and len(ids) == len(set(ids)):
        score += 2
        details["unique_ids"] = f"2/3 task_ids are unique but {total - len(ids)} items missing task_id"
    elif ids:
        dup = len(ids) - len(set(ids))
        score += 1
        details["unique_ids"] = f"1/3 {dup} duplicate task_id(s) found"
    else:
        details["unique_ids"] = "0/3 No valid task_ids"

    id_set = set(ids)

    # 2.4 dependency_graph contains edges array (3 pts)
    edges: List[dict] = []
    if isinstance(dg, dict) and "edges" in dg and isinstance(dg["edges"], list):
        edges = dg["edges"]
        score += 3
        details["edges_format"] = f"3/3 edges array with {len(edges)} edge(s)"
    elif isinstance(dg, dict):
        score += 1
        details["edges_format"] = "1/3 Is an object but missing edges array"
    else:
        details["edges_format"] = "0/3 Format incorrect or null"

    # 2.5 edges reference task_ids that exist in action_items (3 pts)
    if edges and id_set:
        bad = 0
        for edge in edges:
            fr = edge.get("from") or edge.get("source") or ""
            to = edge.get("to") or edge.get("target") or ""
            if fr not in id_set or to not in id_set:
                bad += 1
        if bad == 0:
            score += 3
            details["valid_refs"] = "3/3 All references are valid"
        else:
            s = max(0, 3 - bad)
            score += s
            details["valid_refs"] = f"{s}/3 {bad} edge(s) reference non-existent task_id"
    elif not edges and isinstance(dg, dict):
        score += 1
        details["valid_refs"] = "1/3 No edges, cannot verify"
    else:
        details["valid_refs"] = "0/3 Cannot verify"

    # 2.6 Dependency graph is a DAG (acyclic) (3 pts) - Kahn's topological sort
    if edges and id_set:
        adj: Dict[str, List[str]] = {tid: [] for tid in id_set}
        for edge in edges:
            fr = edge.get("from") or edge.get("source") or ""
            to = edge.get("to") or edge.get("target") or ""
            if fr in adj and to in adj:
                adj[fr].append(to)

        in_deg = {n: 0 for n in adj}
        for n in adj:
            for nb in adj[n]:
                in_deg[nb] = in_deg.get(nb, 0) + 1
        queue = [n for n in in_deg if in_deg[n] == 0]
        visited = 0
        while queue:
            node = queue.pop(0)
            visited += 1
            for nb in adj.get(node, []):
                in_deg[nb] -= 1
                if in_deg[nb] == 0:
                    queue.append(nb)

        if visited == len(adj):
            score += 3
            details["dag_valid"] = "3/3 Acyclic (DAG validation passed)"
        else:
            details["dag_valid"] = "0/3 Cycle detected (DAG validation failed)"
    else:
        score += 1
        details["dag_valid"] = "1/3 No edges or no IDs, skipping DAG validation"

    return score, details


# ─────────────────────────────────────────────────────────────────────
# 3. Span Grounding (25 pts)
# ─────────────────────────────────────────────────────────────────────

def _check_span_grounding(data: dict, config: dict) -> Tuple[int, Dict[str, Any]]:
    score = 0
    details: Dict[str, Any] = {}

    ai = data.get("action_items")
    transcript = data.get("transcript")

    if not isinstance(ai, list) or len(ai) == 0:
        details["skip"] = "action_items is empty or invalid, skipping"
        return 0, details

    total = len(ai)

    if not transcript:
        details["no_transcript"] = "No transcript, giving conservative score 10/25"
        return 10, details

    # 3.1 source_span format is valid (5 pts)
    valid_span = 0
    for item in ai:
        sp = item.get("source_span")
        if sp is not None and sp != "" and sp != "null":
            if isinstance(sp, (dict, str, int)):
                valid_span += 1
    ratio = valid_span / total if total > 0 else 0
    span_fmt_score = round(ratio * 5)
    score += span_fmt_score
    details["span_format"] = f"{span_fmt_score}/5 ({valid_span}/{total} have valid source_span)"

    # 3.2 LLM evaluation of span grounding (20 pts)
    items_json = json.dumps(ai, ensure_ascii=False, indent=2)
    if len(items_json) > 3000:
        items_json = items_json[:3000] + "\n... (truncated)"
    transcript_text = transcript[:5000] if len(transcript) > 5000 else transcript

    prompt = f"""You are a rigorous evaluation expert. Please evaluate whether the following action items extracted from meeting minutes are consistent with the original meeting transcript content.

## Meeting Transcript
{transcript_text}

## Extracted Action Items
{items_json}

Please evaluate:
1. Does each action item's assignee (person responsible) appear in the transcript?
2. Can each action item's action (action description) and object (target) be found in corresponding content in the transcript?
3. Does source_span reasonably point to the corresponding position in the transcript?
4. Are there any "hallucinations" - i.e., action items describing content that does not exist in the transcript?

Please strictly return results in the following JSON format:
```json
{{
  "grounding_score": 0,
  "total_items": 0,
  "grounded_items": 0,
  "hallucinated_items": 0,
  "reason": ""
}}
```

Where grounding_score is an integer from 0-20:
- 18-20: All action items precisely correspond to transcript content, source_span points accurately
- 13-17: Most action items are grounded, a few have deviations
- 7-12: Some action items can be matched, but there are obvious omissions or hallucinations
- 0-6: Many hallucinations or seriously inconsistent with transcript"""

    llm_resp = _call_llm_judge(prompt, config)
    result = _parse_json_from_llm(llm_resp)

    if result and "grounding_score" in result:
        gs = max(0, min(20, int(result["grounding_score"])))
        score += gs
        details["llm_grounding"] = {
            "score": f"{gs}/20",
            "grounded": result.get("grounded_items", "?"),
            "hallucinated": result.get("hallucinated_items", "?"),
            "reason": result.get("reason", ""),
        }
    else:
        # Fallback: simple token overlap check
        grounded = 0
        for item in ai:
            assignee = str(item.get("assignee", "")).strip()
            action = str(item.get("action", "")).strip()
            if assignee and assignee in transcript:
                if action:
                    action_words = set(action.lower().split())
                    tr_words = set(transcript.lower().split())
                    overlap = len(action_words & tr_words) / max(len(action_words), 1)
                    if overlap >= 0.3:
                        grounded += 1
                else:
                    grounded += 1
        ratio = grounded / total if total > 0 else 0
        fallback_score = round(ratio * 12)  # Conservative upper limit 12/20
        score += fallback_score
        details["fallback_grounding"] = (
            f"{fallback_score}/20 (LLM unavailable, token overlap fallback, "
            f"{grounded}/{total} items matched)"
        )

    return score, details


# ─────────────────────────────────────────────────────────────────────
# 4. Content Quality (30 pts)
# ─────────────────────────────────────────────────────────────────────

def _check_content_quality(data: dict, config: dict) -> Tuple[int, Dict[str, Any]]:
    score = 0
    details: Dict[str, Any] = {}

    ai = data.get("action_items")
    dg = data.get("dependency_graph")
    transcript = data.get("transcript")

    if not isinstance(ai, list) or len(ai) == 0:
        details["skip"] = "action_items is empty"
        return 0, details

    items_json = json.dumps(ai, ensure_ascii=False, indent=2)
    if len(items_json) > 3000:
        items_json = items_json[:3000] + "\n... (truncated)"

    edges_json = "[]"
    if isinstance(dg, dict) and "edges" in dg:
        edges_json = json.dumps(dg["edges"], ensure_ascii=False, indent=2)
        if len(edges_json) > 2000:
            edges_json = edges_json[:2000] + "\n... (truncated)"

    transcript_text = ""
    if transcript:
        transcript_text = transcript[:5000] if len(transcript) > 5000 else transcript

    total = len(ai)

    # ---- 4.1 Action item extraction reasonableness (15 pts) ---- LLM evaluation
    prompt_items = f"""You are a rigorous evaluation expert. Please evaluate the quality of the following action items extracted from meeting minutes.

## Meeting Transcript
{transcript_text if transcript_text else "(no transcript)"}

## Extracted Action Items
{items_json}

Please score on the following dimensions (integers):

1. **Completeness** (0-5 pts): Were all explicit or implicit action items in the transcript extracted? Heavy omissions result in point deductions.
2. **Accuracy** (0-5 pts): Is each action item's assignee/action/object/deadline accurate?
3. **Standardization** (0-5 pts): Are fields filled in properly? E.g., is action concise and clear, is object appropriate, is deadline format consistent?

Please strictly return in the following JSON format:
```json
{{
  "completeness": {{"score": 0, "reason": ""}},
  "accuracy": {{"score": 0, "reason": ""}},
  "standardization": {{"score": 0, "reason": ""}},
  "total": 0
}}
```"""

    llm_resp = _call_llm_judge(prompt_items, config)
    result = _parse_json_from_llm(llm_resp)

    if result and "total" in result:
        item_score = max(0, min(15, int(result["total"])))
        score += item_score
        details["item_quality"] = {
            "score": f"{item_score}/15",
            "completeness": result.get("completeness", {}),
            "accuracy": result.get("accuracy", {}),
            "standardization": result.get("standardization", {}),
        }
    else:
        # Fallback: basic heuristics
        fb = 0
        if 3 <= total <= 30:
            fb += 3
        elif total > 0:
            fb += 1
        filled = sum(1 for item in ai if item.get("assignee") and item.get("action"))
        fb += round((filled / total) * 4) if total > 0 else 0
        fb = min(fb, 8)
        score += fb
        details["item_quality_fallback"] = f"{fb}/15 (LLM unavailable, heuristic scoring)"

    # ---- 4.2 Dependency relationship reasonableness (15 pts) ---- LLM evaluation
    prompt_deps = f"""You are a rigorous evaluation expert. Please evaluate the quality of the following task dependency graph.

## Action Items List
{items_json}

## Dependencies (edges)
{edges_json}

Please score on the following dimensions (integers):

1. **Semantic plausibility** (0-5 pts): Does each dependency relationship make semantic sense? Are there unreasonable dependencies?
2. **Completeness** (0-5 pts): Were important dependency relationships captured? Deduct points for obviously missing dependencies.
3. **Dependency types** (0-5 pts): Are dependency types correctly labeled (semantic, temporal, logical dependencies)? Are the types reasonable?

Please strictly return in the following JSON format:
```json
{{
  "semantic_plausibility": {{"score": 0, "reason": ""}},
  "completeness": {{"score": 0, "reason": ""}},
  "dependency_types": {{"score": 0, "reason": ""}},
  "total": 0
}}
```"""

    llm_resp2 = _call_llm_judge(prompt_deps, config)
    result2 = _parse_json_from_llm(llm_resp2)

    if result2 and "total" in result2:
        dep_score = max(0, min(15, int(result2["total"])))
        score += dep_score
        details["dep_quality"] = {
            "score": f"{dep_score}/15",
            "semantic_plausibility": result2.get("semantic_plausibility", {}),
            "completeness": result2.get("completeness", {}),
            "dependency_types": result2.get("dependency_types", {}),
        }
    else:
        # Fallback
        fb = 0
        edges = []
        if isinstance(dg, dict) and isinstance(dg.get("edges"), list):
            edges = dg["edges"]
        if len(edges) > 0:
            fb += 3
            typed = sum(1 for e in edges if e.get("type") or e.get("reason"))
            fb += round((typed / len(edges)) * 4) if edges else 0
        fb = min(fb, 8)
        score += fb
        details["dep_quality_fallback"] = f"{fb}/15 (LLM unavailable, heuristic scoring)"

    return score, details


# ─────────────────────────────────────────────────────────────────────
# 5. Extraction Standards (15 pts)
# ─────────────────────────────────────────────────────────────────────

def _check_extraction_norms(data: dict) -> Tuple[int, Dict[str, Any]]:
    score = 0
    details: Dict[str, Any] = {}

    ai = data.get("action_items")
    transcript = data.get("transcript")

    if not isinstance(ai, list) or len(ai) == 0:
        details["skip"] = "action_items is empty"
        return 0, details

    total = len(ai)

    # 5.1 Reasonable task density (5 pts)
    if transcript:
        char_count = len(transcript)
        ratio = char_count / total if total > 0 else 0
        if 30 <= ratio <= 500:
            score += 5
            details["density"] = f"5/5 Reasonable density ({total} items/{char_count} characters)"
        elif 10 <= ratio <= 1000:
            score += 3
            details["density"] = f"3/5 Density slightly off ({total} items/{char_count} characters)"
        else:
            score += 1
            details["density"] = f"1/5 Abnormal density ({total} items/{char_count} characters)"
    else:
        if 3 <= total <= 30:
            score += 3
            details["density"] = f"3/5 No transcript, {total} items seems reasonable"
        else:
            score += 1
            details["density"] = f"1/5 No transcript, {total} items"

    # 5.2 No duplicates/redundancy (5 pts)
    signatures = [
        f"{str(item.get('assignee', '')).strip().lower()}_"
        f"{str(item.get('action', '')).strip().lower()}_"
        f"{str(item.get('object', '')).strip().lower()}"
        for item in ai
    ]
    unique_sigs = set(signatures)
    if len(unique_sigs) == total:
        score += 5
        details["no_duplicates"] = "5/5 No duplicate items"
    elif len(unique_sigs) >= total * 0.8:
        dup = total - len(unique_sigs)
        score += 3
        details["no_duplicates"] = f"3/5 {dup} suspected duplicate item(s)"
    else:
        dup = total - len(unique_sigs)
        score += 1
        details["no_duplicates"] = f"1/5 Too many duplicates ({dup} item(s))"

    # 5.3 Consistent deadline format (5 pts)
    deadlines_raw = [item.get("deadline") for item in ai]
    has_deadline = [
        d for d in deadlines_raw
        if d is not None and str(d).strip().lower() not in ("", "null", "none", "n/a")
    ]
    no_deadline_count = total - len(has_deadline)

    if len(has_deadline) == 0 and total > 2:
        # All empty - transcript may genuinely have no deadlines, give moderate score
        score += 3
        details["deadline_format"] = "3/5 All deadlines are empty/null (transcript may have no deadlines)"
    elif len(has_deadline) > 0:
        types = set()
        for d in has_deadline:
            ds = str(d).strip()
            if re.match(r"^\d{4}-\d{2}-\d{2}", ds):
                types.add("iso_date")
            elif re.match(r"^\d{4}/\d{2}/\d{2}", ds):
                types.add("slash_date")
            else:
                types.add("text")

        if len(types) <= 1:
            score += 5
            details["deadline_format"] = (
                f"5/5 Consistent deadline format (example: {str(has_deadline[0])!r}, "
                f"{len(has_deadline)}/{total} have deadlines)"
            )
        elif len(types) == 2:
            score += 3
            details["deadline_format"] = f"3/5 Slightly inconsistent deadline format (mixed: {types})"
        else:
            score += 1
            details["deadline_format"] = f"1/5 Inconsistent deadline format (mixed: {types})"
    else:
        score += 2
        details["deadline_format"] = "2/5 Limited deadline information"

    return score, details


# ─────────────────────────────────────────────────────────────────────
# Main Evaluation Entry
# ─────────────────────────────────────────────────────────────────────

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Evaluate the agent's output.

    Args:
        answer_dir: Absolute path to the agent output directory

    Returns:
        (score, report)
        - score: integer 0-100
        - report: dict containing detailed evaluation report
    """
    config = _get_text_eval_config(answer_dir)

    # 1. File Delivery (10 pts)
    s1, d1, data = _check_deliverables(answer_dir)

    # 2. Structural Validity (20 pts)
    s2, d2 = _check_structure(data)

    # 3. Span Grounding (25 pts)
    s3, d3 = _check_span_grounding(data, config)

    # 4. Content Quality (30 pts)
    s4, d4 = _check_content_quality(data, config)

    # 5. Extraction Standards (15 pts)
    s5, d5 = _check_extraction_norms(data)

    total = s1 + s2 + s3 + s4 + s5
    total = max(0, min(100, total))

    report = {
        "total_score": total,
        "1. File Delivery (10 pts)": {"score": s1, "details": d1},
        "2. Structural Validity (20 pts)": {"score": s2, "details": d2},
        "3. Span Grounding (25 pts)": {"score": s3, "details": d3},
        "4. Content Quality (30 pts)": {"score": s4, "details": d4},
        "5. Extraction Standards (15 pts)": {"score": s5, "details": d5},
    }

    if total >= 85:
        report["comment"] = "Excellent - Action items extracted accurately, dependencies reasonable, highly consistent with original text"
    elif total >= 65:
        report["comment"] = "Good - Task basically completed, some dimensions have room for improvement"
    elif total >= 40:
        report["comment"] = "Passing - Core functionality implemented but significant deficiencies exist"
    else:
        report["comment"] = "Failing - Task completion severely insufficient"

    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print a formatted scoring report"""
    print("=" * 70)
    print("  Extract Task List from Meeting Minutes - Scoring Report")
    print("=" * 70)
    print(f"\nTotal Score: {score}/100")
    print(f"Comment: {report.get('comment', '')}\n")

    sections = [
        "1. File Delivery (10 pts)",
        "2. Structural Validity (20 pts)",
        "3. Span Grounding (25 pts)",
        "4. Content Quality (30 pts)",
        "5. Extraction Standards (15 pts)",
    ]

    for sec_name in sections:
        sec = report.get(sec_name, {})
        sec_score = sec.get("score", 0)
        print(f"{'─' * 50}")
        print(f"[{sec_name}] Score: {sec_score}")
        details = sec.get("details", {})
        for k, v in details.items():
            if isinstance(v, dict):
                print(f"  {k}:")
                for kk, vv in v.items():
                    if isinstance(vv, dict):
                        print(f"    {kk}: score={vv.get('score', '?')} reason={vv.get('reason', '')}")
                    else:
                        print(f"    {kk}: {vv}")
            else:
                print(f"  {k}: {v}")

    print("=" * 70)


if __name__ == "__main__":
    import sys

    test_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    if not os.path.isabs(test_dir):
        test_dir = os.path.join(os.path.dirname(__file__), "..", test_dir)
    test_dir = os.path.abspath(test_dir)

    if os.path.isdir(test_dir):
        print(f"Evaluating directory: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"Directory does not exist: {test_dir}")
    sys.exit(0)
