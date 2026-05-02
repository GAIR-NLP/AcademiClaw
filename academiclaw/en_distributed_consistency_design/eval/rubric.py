"""
en_distributed_consistency_design Scoring Rubric
Task: Distributed E-Commerce System Data Consistency Design

Total: 100 points

Scoring Dimensions:
  1. File Delivery and Basic Standards (10 points)
  2. Problem Analysis Accuracy         (20 points) - Keywords + LLM
  3. Solution Design Reasonableness    (30 points) - Keywords + LLM
  4. Technical Implementation Completeness (25 points) - Keywords + LLM
  5. Performance and Reliability Assessment (15 points) - Keywords + LLM
"""

import os
import re
import json
from typing import Any, Dict, List, Tuple

try:
    import openai
except ImportError:
    openai = None


# =========================================================================
# Environment and LLM Utilities
# =========================================================================

def _load_env(answer_dir: str) -> dict:
    """Load .env configuration from answer_dir and query root directory"""
    values: Dict[str, str] = {}
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


def _parse_llm_json(raw: str) -> dict:
    """Extract JSON from LLM response"""
    if not raw:
        return {}
    try:
        if "```json" in raw:
            raw = raw.split("```json")[1].split("```")[0].strip()
        elif "```" in raw:
            raw = raw.split("```")[1].split("```")[0].strip()
        return json.loads(raw)
    except Exception:
        return {}


# =========================================================================
# File Loading
# =========================================================================

def _find_design_doc(answer_dir: str) -> Tuple[str, str]:
    """Find the design document in answer_dir, return (filename, content)."""
    if not os.path.isdir(answer_dir):
        return "", ""

    candidates = []
    for name in os.listdir(answer_dir):
        low = name.lower()
        if not os.path.isfile(os.path.join(answer_dir, name)):
            continue
        if not (low.endswith(".md") or low.endswith(".txt")):
            continue
        # Exclude known non-document files
        if low in ("run.md", "readme.md", "evaluation_feedback.txt"):
            continue
        priority = 0
        for kw in ["consistency", "design", "analysis", "report",
                    "一致", "设计", "方案", "架构"]:
            if kw in low:
                priority = 2
                break
        candidates.append((priority, name))

    candidates.sort(key=lambda x: -x[0])
    for _, name in candidates:
        path = os.path.join(answer_dir, name)
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            if len(content) > 100:
                return name, content
        except Exception:
            pass
    return "", ""


def _load_code_files(answer_dir: str) -> str:
    """Load all .py code file contents in answer_dir (excluding eval-related files)."""
    parts = []
    if not os.path.isdir(answer_dir):
        return ""
    for name in sorted(os.listdir(answer_dir)):
        if not name.endswith(".py"):
            continue
        low = name.lower()
        if "rubric" in low or "eval_task" in low:
            continue
        path = os.path.join(answer_dir, name)
        if not os.path.isfile(path):
            continue
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                parts.append(f"# === {name} ===\n{f.read()}")
        except Exception:
            pass
    return "\n\n".join(parts)


def _load_all_text(answer_dir: str) -> str:
    """Load all readable text file contents in answer_dir."""
    parts = []
    if not os.path.isdir(answer_dir):
        return ""
    for name in sorted(os.listdir(answer_dir)):
        path = os.path.join(answer_dir, name)
        if not os.path.isfile(path):
            continue
        low = name.lower()
        if low in ("evaluation_feedback.txt",):
            continue
        if "rubric" in low or "eval_task" in low:
            continue
        valid_exts = (".md", ".txt", ".py", ".sql", ".yaml", ".yml", ".json")
        if not any(low.endswith(ext) for ext in valid_exts):
            continue
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                parts.append(f.read())
        except Exception:
            pass
    return "\n\n".join(parts)


def _extract_code_blocks(doc: str) -> str:
    """Extract all code blocks from a markdown document."""
    blocks = re.findall(r"```(?:python|py|sql|yaml|json)?\n(.*?)```", doc, re.DOTALL)
    return "\n\n".join(blocks)


# =========================================================================
# Dimension 1: File Delivery and Basic Standards (10 points)
# =========================================================================

def _eval_file_delivery(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Check whether the agent's deliverable files exist and meet basic requirements.

    Sub-items:
      1a. Design document exists (.md or .txt, >200 bytes) - 5 points
      1b. Implementation code/pseudocode (standalone .py or >=2 code blocks in doc) - 3 points
      1c. Document length (>= 3000 bytes: 2 pts, >= 1000 bytes: 1 pt) - 2 points
    """
    score = 0
    details: Dict[str, str] = {}
    deductions: List[str] = []

    if not os.path.isdir(answer_dir):
        return 0, {"score": 0, "details": {"error": "Answer directory does not exist"}, "deductions": ["Answer directory does not exist"]}

    doc_name, doc_content = _find_design_doc(answer_dir)

    # 1a. Design document (5 points)
    if doc_name and len(doc_content) > 200:
        score += 5
        details["design_document"] = f"5/5 - Found: {doc_name} ({len(doc_content)} chars)"
    elif doc_name:
        score += 2
        details["design_document"] = f"2/5 - {doc_name} content too short ({len(doc_content)} chars)"
        deductions.append("Design document content too short (<200 chars)")
    else:
        details["design_document"] = "0/5 - No design document found (.md/.txt)"
        deductions.append("Missing design document")

    # 1b. Implementation code/pseudocode (3 points)
    code_text = _load_code_files(answer_dir)
    py_files = [f for f in os.listdir(answer_dir) if f.endswith(".py")
                and "rubric" not in f.lower() and "eval_task" not in f.lower()
                and os.path.isfile(os.path.join(answer_dir, f))]
    if py_files:
        score += 3
        details["code_files"] = f"3/3 - {len(py_files)} .py file(s): {', '.join(py_files[:5])}"
    elif doc_content:
        blocks_count = doc_content.count("```python") + doc_content.count("```py")
        if blocks_count >= 3:
            score += 3
            details["code_files"] = f"3/3 - No standalone .py but document contains {blocks_count} Python code blocks"
        elif blocks_count >= 2:
            score += 2
            details["code_files"] = f"2/3 - No standalone .py, document contains {blocks_count} code blocks"
        elif blocks_count >= 1:
            score += 1
            details["code_files"] = f"1/3 - Only {blocks_count} code block(s)"
        else:
            details["code_files"] = "0/3 - No code files or code blocks"
            deductions.append("Missing implementation code or pseudocode")
    else:
        details["code_files"] = "0/3 - No code files or documents"
        deductions.append("Missing implementation code or pseudocode")

    # 1c. Document length (2 points)
    if doc_content:
        doc_len = len(doc_content)
        if doc_len >= 3000:
            score += 2
            details["document_length"] = f"2/2 - {doc_len} chars, substantial content"
        elif doc_len >= 1000:
            score += 1
            details["document_length"] = f"1/2 - {doc_len} chars, somewhat brief"
        else:
            details["document_length"] = f"0/2 - {doc_len} chars, too short"
            deductions.append("Design document length insufficient")
    else:
        details["document_length"] = "0/2 - No design document"

    return score, {"score": score, "details": details, "deductions": deductions}


# =========================================================================
# Dimension 2: Problem Analysis Accuracy (20 points)
#   2a. Keyword detection - up to 10 points
#   2b. LLM evaluation   - up to 10 points
# =========================================================================

# Each problem matches if any pattern group is matched
_PROBLEM_KEYWORDS: Dict[str, List[List[str]]] = {
    "Inventory overselling": [["库存", "超卖"], ["库存", "并发"], ["oversell"], ["over-sell"],
                               ["inventory", "oversell"], ["inventory", "concurrent"]],
    "Order status inconsistency": [["订单", "不一致"], ["订单", "状态", "一致"], ["order", "inconsisten"]],
    "Duplicate payment processing": [["支付", "重复"], ["支付", "幂等"], ["重复扣款"], ["duplicate", "payment"],
                                      ["payment", "idempoten"]],
    "Distributed transaction challenges": [["分布式", "事务"], ["distributed", "transaction"], ["跨服务", "事务"],
                                            ["cross-service", "transaction"]],
}

_PROBLEM_ANALYSIS_PROMPT = """\
You are a rigorous technical review expert. Below is a design document about "distributed e-commerce system data consistency."

Please evaluate only the quality of its "Problem Analysis" section (i.e., the identification and analysis depth of existing system consistency issues).

Evaluation criteria:
1. Does it accurately identify the inventory overselling problem (caused by concurrent deductions)?
2. Does it identify the order status and payment/inventory inconsistency issue?
3. Does it identify the duplicate payment processing / idempotency requirement?
4. Does it identify the inherent challenges of cross-service distributed transactions?
5. Does the analysis have depth (not just listing problem names, but also explaining causes, scenarios, and impacts)?
6. Does it analyze specific code issues from current_order_flow.py?

Scoring scale:
- 0-3: Almost no analysis or only lists names
- 4-6: Identified some problems but shallow analysis
- 7-8: Comprehensive identification with some depth
- 9-10: Comprehensive, in-depth analysis with specific scenarios and root cause analysis

Please respond strictly in the following JSON format:
```json
{{"score": 0, "reason": ""}}
```

The following is the content to evaluate (first 4000 characters):

{content}
"""


def _keyword_match(text: str, patterns: Dict[str, List[List[str]]]) -> List[str]:
    """Perform keyword matching on text, return list of matched items."""
    found = []
    for item, pat_groups in patterns.items():
        for pat in pat_groups:
            if all(kw.lower() in text.lower() or kw in text for kw in pat):
                found.append(item)
                break
    return found


def _eval_problem_analysis(all_text: str, doc_content: str, config: dict) -> Tuple[int, Dict[str, Any]]:
    details: Dict[str, Any] = {}
    deductions: List[str] = []

    # 2a. Keywords (10 points): 2.5 points per identified problem
    kw_found = _keyword_match(all_text, _PROBLEM_KEYWORDS)
    kw_score = min(10, int(len(kw_found) * 2.5))
    details["keyword_detection (10pts)"] = f"{kw_score}/10 - Identified: {', '.join(kw_found) if kw_found else 'none'}"

    # 2b. LLM (10 points)
    content = (doc_content or all_text)[:4000]
    llm_score = 0
    if content.strip():
        raw = _call_llm_judge(_PROBLEM_ANALYSIS_PROMPT.format(content=content), config)
        parsed = _parse_llm_json(raw)
        if parsed and "score" in parsed:
            llm_score = max(0, min(10, int(parsed["score"])))
            details["LLM_evaluation (10pts)"] = f"{llm_score}/10 - {parsed.get('reason', '')}"
        else:
            llm_score = min(5, kw_score)
            details["LLM_evaluation (10pts)"] = f"{llm_score}/10 - LLM unavailable, conservative score based on keywords"
    else:
        details["LLM_evaluation (10pts)"] = "0/10 - No content to evaluate"

    total = kw_score + llm_score
    if total < 10:
        deductions.append(f"Problem analysis not comprehensive or lacks depth ({total}/20)")
    return total, {"score": total, "details": details, "deductions": deductions}


# =========================================================================
# Dimension 3: Solution Design Reasonableness (30 points)
#   3a. Keyword detection - up to 15 points
#   3b. LLM evaluation   - up to 15 points
# =========================================================================

_SOLUTION_KEYWORDS: Dict[str, List[List[str]]] = {
    "Distributed lock/concurrency control": [["分布式锁"], ["distributed lock"], ["乐观锁"], ["悲观锁"],
                          ["optimistic lock"], ["pessimistic lock"], ["原子操作"], ["atomic operation"], ["CAS"]],
    "TCC/Saga pattern": [["TCC"], ["Saga"], ["Try", "Confirm", "Cancel"],
                       ["补偿事务"], ["saga orchestrat"]],
    "Message queue/event-driven": [["消息队列"], ["message queue"], ["事件驱动"], ["event driven"],
                          ["Outbox"], ["消息总线"], ["Kafka"], ["RabbitMQ"]],
    "Idempotency design": [["幂等"], ["idempoten"], ["去重表"], ["唯一约束"],
                   ["idempotency_key"], ["idem_key"], ["dedup"]],
    "Compensation and reconciliation": [["补偿"], ["对账"], ["reconcil"], ["compensation"], ["死信"],
                                         ["dead letter"]],
}

_SOLUTION_DESIGN_PROMPT = """\
You are a rigorous technical review expert. Below is a design document about "distributed e-commerce system data consistency."

Please evaluate the quality of its "Solution Design" section, focusing on:
1. Whether it proposes a reasonable distributed transaction solution (e.g., TCC, Saga, two-phase commit) and explains the rationale
2. Whether it designs an inventory concurrency control solution (e.g., distributed lock, optimistic lock, atomic operations)
3. Whether it uses message queues/event-driven approach for eventual consistency (e.g., Outbox pattern, reliable messaging)
4. Whether it designs an idempotency solution (e.g., idempotency keys, deduplication tables, unique constraints)
5. Whether it designs a compensation/reconciliation mechanism (scheduled reconciliation, dead-letter handling)
6. Whether the architecture is clear (with service interaction descriptions, flowcharts/sequence diagrams or equivalent text descriptions)
7. Whether the overall solution is feasible and has engineering practical value

Scoring scale:
- 0-4: Solution is rough or unreasonable
- 5-8: Covers some key points but incomplete
- 9-12: Comprehensive coverage, reasonable design
- 13-15: Detailed design, strong engineering feasibility, innovative aspects

Please respond strictly in the following JSON format:
```json
{{"score": 0, "reason": ""}}
```

The following is the content to evaluate (first 6000 characters):

{content}
"""


def _eval_solution_design(all_text: str, doc_content: str, config: dict) -> Tuple[int, Dict[str, Any]]:
    details: Dict[str, Any] = {}
    deductions: List[str] = []

    # 3a. Keywords (15 points): 3 points per solution
    kw_found = _keyword_match(all_text, _SOLUTION_KEYWORDS)
    kw_score = min(15, len(kw_found) * 3)
    details["keyword_detection (15pts)"] = f"{kw_score}/15 - Includes: {', '.join(kw_found) if kw_found else 'none'}"

    # 3b. LLM (15 points)
    content = (doc_content or all_text)[:6000]
    llm_score = 0
    if content.strip():
        raw = _call_llm_judge(_SOLUTION_DESIGN_PROMPT.format(content=content), config)
        parsed = _parse_llm_json(raw)
        if parsed and "score" in parsed:
            llm_score = max(0, min(15, int(parsed["score"])))
            details["LLM_evaluation (15pts)"] = f"{llm_score}/15 - {parsed.get('reason', '')}"
        else:
            llm_score = min(7, kw_score)
            details["LLM_evaluation (15pts)"] = f"{llm_score}/15 - LLM unavailable, conservative score based on keywords"
    else:
        details["LLM_evaluation (15pts)"] = "0/15 - No content to evaluate"

    total = kw_score + llm_score
    if total < 15:
        deductions.append(f"Solution design incomplete or lacks depth ({total}/30)")
    return total, {"score": total, "details": details, "deductions": deductions}


# =========================================================================
# Dimension 4: Technical Implementation Completeness (25 points)
#   4a. Key component coverage detection - up to 10 points
#   4b. LLM evaluation                   - up to 15 points
# =========================================================================

# Each component requires >=2 keyword hits to be considered covered
_IMPL_COMPONENTS: Dict[str, List[str]] = {
    "Inventory deduction": ["inventory", "deduct", "reduce", "扣减", "预留", "reserved",
                  "try_reserve", "reserve_stock", "stock"],
    "Order service": ["order", "create_order", "订单", "order_service", "OrderService",
                  "order_status", "PAID", "CANCELED"],
    "Payment service": ["payment", "支付", "pay", "create_payment", "PaymentService",
                  "payment_intent", "idem_key"],
    "Event handling": ["event", "handle_event", "consume", "事件", "message_bus",
                  "MessageBus", "publish", "subscribe", "outbox"],
    "Monitoring/reconciliation": ["reconcil", "对账", "监控", "check_inconsist", "补偿",
                   "ReconciliationJob", "monitor", "dead_letter", "死信"],
}

_IMPL_PROMPT = """\
You are a rigorous technical review expert. Below is the implementation code or pseudocode for a "distributed e-commerce system data consistency solution."

Please evaluate the completeness and quality of its technical implementation, focusing on:
1. Inventory deduction implementation (TCC reserve/confirm/release or distributed lock-protected atomic operations)
2. Order service implementation (create/confirm/cancel flow, state machine)
3. Payment service implementation (idempotent payment, result callback notification)
4. Event handling implementation (message publish/consume, Outbox pattern, consumer deduplication)
5. Monitoring and reconciliation implementation (inconsistency detection, compensation triggers, dead-letter handling)
6. Whether the code has demonstrative value (not required to be runnable, but should show key logic and exception handling)
7. Whether the code covers idempotency guarantees and exception recovery

Scoring scale:
- 0-4: Code snippets are scattered or lack key logic
- 5-8: Covers some components but incomplete
- 9-12: Key components are all implemented with clear logic
- 13-15: Complete implementation, proper exception handling, high code quality

Please respond strictly in the following JSON format:
```json
{{"score": 0, "reason": ""}}
```

The following is the code/pseudocode to evaluate (first 8000 characters):

{content}
"""


def _eval_implementation(all_text: str, doc_content: str, code_text: str,
                         config: dict) -> Tuple[int, Dict[str, Any]]:
    details: Dict[str, Any] = {}
    deductions: List[str] = []

    # 4a. Component coverage (10 points): 2 points each
    found_components = []
    text_lower = all_text.lower()
    for comp, keywords in _IMPL_COMPONENTS.items():
        matched = sum(1 for kw in keywords
                      if kw.lower() in text_lower or kw in all_text)
        if matched >= 2:
            found_components.append(comp)
    kw_score = min(10, len(found_components) * 2)
    details["component_coverage (10pts)"] = (
        f"{kw_score}/10 - Covered: {', '.join(found_components) if found_components else 'none'}"
    )

    # 4b. LLM (15 points)
    # Prefer standalone code files, otherwise extract code blocks from document
    eval_content = code_text
    if not eval_content.strip() and doc_content:
        eval_content = _extract_code_blocks(doc_content)
    if not eval_content.strip():
        eval_content = all_text
    eval_content = eval_content[:8000]

    llm_score = 0
    if eval_content.strip():
        raw = _call_llm_judge(_IMPL_PROMPT.format(content=eval_content), config)
        parsed = _parse_llm_json(raw)
        if parsed and "score" in parsed:
            llm_score = max(0, min(15, int(parsed["score"])))
            details["LLM_evaluation (15pts)"] = f"{llm_score}/15 - {parsed.get('reason', '')}"
        else:
            llm_score = min(7, kw_score)
            details["LLM_evaluation (15pts)"] = f"{llm_score}/15 - LLM unavailable, conservative score based on keywords"
    else:
        details["LLM_evaluation (15pts)"] = "0/15 - No code content to evaluate"

    total = kw_score + llm_score
    if total < 12:
        deductions.append(f"Technical implementation incomplete ({total}/25)")
    return total, {"score": total, "details": details, "deductions": deductions}


# =========================================================================
# Dimension 5: Performance and Reliability Assessment (15 points)
#   5a. Keyword detection - up to 8 points
#   5b. LLM evaluation   - up to 7 points
# =========================================================================

_PERF_KEYWORDS: Dict[str, List[str]] = {
    "Performance impact analysis": ["性能", "延迟", "吞吐", "performance", "latency", "throughput", "QPS"],
    "High availability design": ["高可用", "可用性", "availability", "HA", "failover", "故障转移", "多副本",
                                  "high availability"],
    "Fault tolerance and retry": ["容错", "重试", "retry", "fault", "超时", "timeout", "降级", "熔断",
                                   "circuit breaker", "fallback"],
    "Scalability": ["扩展", "scalab", "scale", "分片", "分区", "partition", "读写分离",
                     "read-write split", "horizontal scaling"],
}

_PERF_PROMPT = """\
You are a rigorous technical review expert. Below is a document about a "distributed e-commerce system data consistency solution."

Please evaluate the quality of its "Performance and Reliability Assessment" section, focusing on:
1. Whether it analyzes the solution's impact on system performance (lock contention, message latency, retry overhead, etc.)
2. Whether it describes high availability and fault tolerance design (failover, multi-replica, degradation strategies, etc.)
3. Whether it discusses scalability (sharding, read-write separation, horizontal scaling, etc.)
4. Whether the analysis has depth (not just qualitative descriptions, but also specific measures or quantitative considerations)

Scoring scale:
- 0-2: Almost no assessment
- 3-4: Only brief mentions
- 5-6: Covers major aspects but lacks depth
- 7: Comprehensive and in-depth

Please respond strictly in the following JSON format:
```json
{{"score": 0, "reason": ""}}
```

The following is the content to evaluate (first 4000 characters):

{content}
"""


def _eval_performance(all_text: str, doc_content: str, config: dict) -> Tuple[int, Dict[str, Any]]:
    details: Dict[str, Any] = {}
    deductions: List[str] = []

    # 5a. Keywords (8 points): 2 points per aspect
    found_aspects = []
    text_lower = all_text.lower()
    for aspect, keywords in _PERF_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in text_lower or kw in all_text:
                found_aspects.append(aspect)
                break
    kw_score = min(8, len(found_aspects) * 2)
    details["keyword_detection (8pts)"] = (
        f"{kw_score}/8 - Covered: {', '.join(found_aspects) if found_aspects else 'none'}"
    )

    # 5b. LLM (7 points)
    content = (doc_content or all_text)[:4000]
    llm_score = 0
    if content.strip():
        raw = _call_llm_judge(_PERF_PROMPT.format(content=content), config)
        parsed = _parse_llm_json(raw)
        if parsed and "score" in parsed:
            llm_score = max(0, min(7, int(parsed["score"])))
            details["LLM_evaluation (7pts)"] = f"{llm_score}/7 - {parsed.get('reason', '')}"
        else:
            llm_score = min(3, kw_score)
            details["LLM_evaluation (7pts)"] = f"{llm_score}/7 - LLM unavailable, conservative score based on keywords"
    else:
        details["LLM_evaluation (7pts)"] = "0/7 - No content to evaluate"

    total = kw_score + llm_score
    if total < 8:
        deductions.append(f"Performance and reliability assessment insufficient ({total}/15)")
    return total, {"score": total, "details": details, "deductions": deductions}


# =========================================================================
# Entry Point
# =========================================================================

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Evaluate the agent's output.

    Args:
        answer_dir: Absolute path to the agent output directory

    Returns:
        (score, report) - score is an integer from 0-100, report is a detailed evaluation report
    """
    config = _get_text_eval_config(answer_dir)

    # Load all needed text
    doc_name, doc_content = _find_design_doc(answer_dir)
    code_text = _load_code_files(answer_dir)
    all_text = _load_all_text(answer_dir)

    # If directory does not exist or is empty
    if not all_text.strip() and not doc_content.strip() and not code_text.strip():
        return 0, {
            "total_score": 0,
            "result_score": {"score": 0, "details": {}, "deductions": ["Answer directory is empty or does not exist"]},
            "process_score": {"score": 0, "details": {}, "deductions": []},
            "dimension_scores": {},
            "comment": "Answer directory is empty, cannot evaluate.",
        }

    # Score each dimension
    s1, r1 = _eval_file_delivery(answer_dir)
    s2, r2 = _eval_problem_analysis(all_text, doc_content, config)
    s3, r3 = _eval_solution_design(all_text, doc_content, config)
    s4, r4 = _eval_implementation(all_text, doc_content, code_text, config)
    s5, r5 = _eval_performance(all_text, doc_content, config)

    total = min(100, s1 + s2 + s3 + s4 + s5)

    if total >= 90:
        comment = "Excellent: comprehensive problem analysis, complete and reasonable solution design, sufficient implementation examples, thorough performance assessment."
    elif total >= 75:
        comment = "Good: major dimensions are covered, some dimensions could be further strengthened."
    elif total >= 60:
        comment = "Passing: has design solution and partial implementation, but lacks analysis depth or implementation completeness."
    elif total >= 40:
        comment = "Partially complete: has output but many key dimensions are missing."
    else:
        comment = "Failing: missing complete consistency design document and implementation examples."

    report = {
        "total_score": total,
        "result_score": {
            "score": s1 + s2 + s3,
            "details": {
                "1. File Delivery (10pts)": r1.get("details", {}),
                "2. Problem Analysis (20pts)": r2.get("details", {}),
                "3. Solution Design (30pts)": r3.get("details", {}),
            },
            "deductions": (r1.get("deductions", [])
                        + r2.get("deductions", [])
                        + r3.get("deductions", [])),
        },
        "process_score": {
            "score": s4 + s5,
            "details": {
                "4. Technical Implementation (25pts)": r4.get("details", {}),
                "5. Performance and Reliability (15pts)": r5.get("details", {}),
            },
            "deductions": r4.get("deductions", []) + r5.get("deductions", []),
        },
        "dimension_scores": {
            "File Delivery": f"{s1}/10",
            "Problem Analysis": f"{s2}/20",
            "Solution Design": f"{s3}/30",
            "Technical Implementation": f"{s4}/25",
            "Performance and Reliability": f"{s5}/15",
        },
        "comment": comment,
    }

    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print a formatted scoring report."""
    print("=" * 70)
    print("Distributed Data Consistency Design - Scoring Report")
    print("=" * 70)
    print(f"\nTotal Score: {score}/100\n")

    scores = report.get("dimension_scores", {})
    if scores:
        print("Dimension Scores:")
        for k, v in scores.items():
            print(f"  {k}: {v}")

    for section_key, section_label in [
        ("result_score", "Result Score (File + Analysis + Design)"),
        ("process_score", "Process Score (Implementation + Performance)"),
    ]:
        section = report.get(section_key, {})
        print(f"\n{'─' * 50}")
        print(f"[{section_label}] {section.get('score', 0)} pts")
        print(f"{'─' * 50}")
        for cat, items in section.get("details", {}).items():
            print(f"\n  {cat}:")
            if isinstance(items, dict):
                for k, v in items.items():
                    print(f"    {k}: {v}")
            else:
                print(f"    {items}")
        deds = section.get("deductions", [])
        if deds:
            print(f"\n  Deductions:")
            for i, r in enumerate(deds, 1):
                print(f"    {i}. {r}")

    print(f"\n{'=' * 50}")
    print(f"Comment: {report.get('comment', '')}")
    print("=" * 70)


if __name__ == "__main__":
    import sys
    test_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(__file__), "..", "workspace")
    if os.path.isdir(test_dir):
        print(f"Evaluating directory: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"Directory does not exist: {test_dir}")
    sys.exit(0)
