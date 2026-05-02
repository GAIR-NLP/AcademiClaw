"""
ChCore Lab3 Lab Report — Scoring Script (rubric.py)

Task: Write a ChCore Lab3 (Processes and Threads) lab report
Deliverable: report.md (Markdown lab report)

Total Score: 100 points

Scoring Dimensions:
  I. File Delivery (10 pts)
      1. report.md file exists with correct name (5 pts)
      2. Markdown basic format: has headings, has code blocks, sufficient word count (5 pts)

  II. Report Structure (20 pts)
      1. Contains Parts 1-4 four main sections (12 pts, 3 pts each)
      2. Covers 7 exercises + 2 discussion questions (8 pts)

  III. Core Code Content (40 pts)
      - Exercise 1: cap_group / create_root_cap_group related code (8 pts)
      - Exercise 2: create_root_thread / ELF loading code (8 pts)
      - Exercise 3: init_thread_ctx context initialization code (5 pts)
      - Exercise 5: Exception vector table filling code (5 pts)
      - Exercise 6: exception_enter / exception_exit code (8 pts)
      - Exercise 8: put / chcore_syscall system call code (3 pts)
      - Exercise 9: Hello ChCore user program code (3 pts)

  IV. Discussion Questions & Overall Quality — LLM-as-Judge (30 pts)
      - Question 4: Complete flow from kernel to user mode (10 pts)
      - Question 7: printf to terminal output call chain (10 pts)
      - Overall report quality and formatting (10 pts)
"""

import os
import re
import json
from typing import Tuple, Dict, Any

try:
    import openai
except ImportError:
    openai = None


# ---------------------------------------------------------------------------
# Environment & LLM utilities
# ---------------------------------------------------------------------------

def _load_env(answer_dir: str) -> dict:
    """Load .env configuration from answer_dir and query root directory"""
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
# Report file search
# ---------------------------------------------------------------------------

def _find_report(answer_dir: str) -> str:
    """Find the report file in answer_dir, prioritizing report.md"""
    primary = os.path.join(answer_dir, "report.md")
    if os.path.isfile(primary):
        return primary
    # fallback: other .md files (excluding non-report files)
    skip = {"query.md", "readme.md", "task_prompt.md"}
    try:
        for f in sorted(os.listdir(answer_dir)):
            if f.lower() in skip or f.startswith("."):
                continue
            if f.lower().endswith(".md") and os.path.isfile(os.path.join(answer_dir, f)):
                return os.path.join(answer_dir, f)
    except Exception:
        pass
    return ""


# ---------------------------------------------------------------------------
# I. File Delivery (10 pts)
# ---------------------------------------------------------------------------

def _eval_file_delivery(report_path: str, content: str) -> Tuple[int, dict]:
    score = 0
    details: dict = {}

    if not report_path:
        details["report.md"] = "0/5 — Report file not found"
        details["format_and_length"] = "0/5 — No file"
        return 0, details

    fname = os.path.basename(report_path)
    if fname == "report.md":
        score += 5
        details["report.md"] = "5/5 — Correct filename"
    else:
        score += 2
        details["report.md"] = f"2/5 — Found {fname}, but not report.md"

    char_len = len(content)
    has_heading = bool(re.search(r"^#{1,3}\s+", content, re.MULTILINE))
    code_blocks = len(re.findall(r"```", content)) // 2  # pairs
    has_lang_tag = bool(re.search(r"```(?:c|asm|assembly|makefile)", content, re.IGNORECASE))

    if char_len >= 3000 and has_heading and code_blocks >= 4 and has_lang_tag:
        score += 5
        details["format_and_length"] = f"5/5 — {char_len} chars, {code_blocks} code blocks, has headings, has language tags"
    elif char_len >= 2000 and has_heading and code_blocks >= 3:
        score += 4
        details["format_and_length"] = f"4/5 — {char_len} chars, {code_blocks} code blocks"
    elif char_len >= 1500 and (has_heading or code_blocks >= 2):
        score += 3
        details["format_and_length"] = f"3/5 — {char_len} chars, {code_blocks} code blocks"
    elif char_len >= 800:
        score += 1
        details["format_and_length"] = f"1/5 — {char_len} chars, content is sparse"
    else:
        details["format_and_length"] = f"0/5 — {char_len} chars, severely insufficient content"

    return score, details


# ---------------------------------------------------------------------------
# II. Report Structure (20 pts)
# ---------------------------------------------------------------------------

def _eval_structure(content: str) -> Tuple[int, dict]:
    score = 0
    details: dict = {}

    # 2a. Four main parts (12 pts, 3 pts each)
    parts = [
        ("Part 1 / Thread Lifecycle Management", r"(?:Part\s*1|Thread Lifecycle|Thread.*Management|Processes and Threads)"),
        ("Part 2 / Exception Management", r"(?:Part\s*2|Exception Management|Exception Handling)"),
        ("Part 3 / System Calls", r"(?:Part\s*3|System Call)"),
        ("Part 4 / User Program", r"(?:Part\s*4|User Program|User.?Mode Program)"),
    ]
    found_parts = 0
    for label, pattern in parts:
        if re.search(pattern, content, re.IGNORECASE):
            found_parts += 1
            details[label] = "OK"
        else:
            details[label] = "Missing"

    part_score = found_parts * 3
    score += part_score
    details["parts_score"] = f"{part_score}/12 — Found {found_parts}/4 parts"

    # 2b. Exercise + discussion question coverage (8 pts, 9 items total)
    items = {
        "Exercise 1": r"Exercise\s*1",
        "Exercise 2": r"Exercise\s*2",
        "Exercise 3": r"Exercise\s*3",
        "Exercise 5": r"Exercise\s*5",
        "Exercise 6": r"Exercise\s*6",
        "Exercise 8": r"Exercise\s*8",
        "Exercise 9": r"Exercise\s*9",
        "Question 4": r"(?:Thinking|Discussion|Question)\s*4",
        "Question 7": r"(?:Thinking|Discussion|Question)\s*7",
    }
    found_items = 0
    for label, pattern in items.items():
        if re.search(pattern, content, re.IGNORECASE):
            found_items += 1

    item_score = min(8, round(found_items * 8 / 9))
    score += item_score
    details["item_coverage"] = f"{item_score}/8 — Found {found_items}/9 item markers"

    return score, details


# ---------------------------------------------------------------------------
# III. Core Code Content (40 pts)
# ---------------------------------------------------------------------------

def _kw(content: str, *keywords: str) -> int:
    """Count how many keywords appear in content"""
    return sum(1 for kw in keywords if kw in content)


def _eval_code_content(content: str) -> Tuple[int, dict]:
    score = 0
    details: dict = {}

    # ---- Exercise 1: cap_group / create_root_cap_group (8 pts) ----
    s1 = 0
    # Core: obj_alloc TYPE_CAP_GROUP, cap_group_init, cap_alloc, obj_alloc TYPE_VMSPACE, vmspace_init
    if "obj_alloc" in content and "TYPE_CAP_GROUP" in content:
        s1 += 3
    elif "cap_group" in content and ("alloc" in content.lower() or "create" in content.lower()):
        s1 += 1
    if "obj_alloc" in content and "TYPE_VMSPACE" in content:
        s1 += 2
    if _kw(content, "cap_group_init", "cap_alloc") >= 1:
        s1 += 1
    if _kw(content, "vmspace_init", "ROOT_CAP_GROUP_BADGE", "BASE_OBJECT_NUM") >= 1:
        s1 += 1
    # sys_create_cap_group part
    if "sys_create_cap_group" in content:
        s1 += 1
    s1 = min(8, s1)
    score += s1
    details["exercise_1_cap_group_8pts"] = f"{s1}/8"

    # ---- Exercise 2: create_root_thread / ELF loading (8 pts) ----
    s2 = 0
    if "binary_procmgr_bin_start" in content:
        s2 += 2
    if "create_pmo" in content:
        s2 += 2
    if "VMR_READ" in content and "VMR_WRITE" in content:
        s2 += 1
    if "vmspace_map_range" in content:
        s2 += 1
    if _kw(content, "ROOT_THREAD_STACK_BASE", "ROOT_THREAD_STACK_SIZE", "thread_init") >= 1:
        s2 += 1
    if _kw(content, "memcpy", "phnum", "phdr", "PHDR") >= 2:
        s2 += 1
    s2 = min(8, s2)
    score += s2
    details["exercise_2_create_root_thread_8pts"] = f"{s2}/8"

    # ---- Exercise 3: init_thread_ctx (5 pts) ----
    s3 = 0
    if "SP_EL0" in content:
        s3 += 2
    if "ELR_EL1" in content:
        s3 += 2
    if "SPSR_EL1" in content:
        s3 += 1
    s3 = min(5, s3)
    score += s3
    details["exercise_3_init_thread_ctx_5pts"] = f"{s3}/5"

    # ---- Exercise 5: Exception vector table (5 pts) ----
    s5 = 0
    if "exception_entry" in content:
        s5 += 2
    if re.search(r"sync_el1[th]|irq_el1[th]", content):
        s5 += 1
    if re.search(r"fiq_el1|error_el1", content):
        s5 += 1
    if re.search(r"\.align|EXPORT|handle_entry_c|unexpected_handler", content):
        s5 += 1
    s5 = min(5, s5)
    score += s5
    details["exercise_5_exception_vector_5pts"] = f"{s5}/5"

    # ---- Exercise 6: exception_enter / exception_exit (8 pts) ----
    s6 = 0
    # exception_enter: sub sp, stp to save registers, mrs to read system registers
    if re.search(r"sub\s+sp", content):
        s6 += 1
    if "stp" in content:
        s6 += 1
    if "mrs" in content:
        s6 += 1
    if re.search(r"ARCH_EXEC_CONT_SIZE|TPIDR_EL1|switch_to_cpu_stack", content):
        s6 += 1
    # exception_exit: ldp to restore, msr to write system registers, eret to return
    if "ldp" in content:
        s6 += 1
    if "msr" in content:
        s6 += 1
    if "eret" in content:
        s6 += 2
    s6 = min(8, s6)
    score += s6
    details["exercise_6_exception_enter_exit_8pts"] = f"{s6}/8"

    # ---- Exercise 8: put / syscall (3 pts) ----
    s8 = 0
    if _kw(content, "chcore_syscall", "CHCORE_SYS_putstr") >= 1:
        s8 += 2
    if _kw(content, "putstr", "put_str", "sys_putstr") >= 1:
        s8 += 1
    s8 = min(3, s8)
    score += s8
    details["exercise_8_put_syscall_3pts"] = f"{s8}/3"

    # ---- Exercise 9: Hello ChCore (3 pts) ----
    s9 = 0
    if "Hello ChCore" in content:
        s9 += 1
    if _kw(content, "musl", "gcc", "chcore-libc", "toolchain") >= 1:
        s9 += 1
    if _kw(content, "hello_world.bin", "Makefile", "CMakeLists", "ramdisk") >= 1:
        s9 += 1
    s9 = min(3, s9)
    score += s9
    details["exercise_9_hello_chcore_3pts"] = f"{s9}/3"

    return score, details


# ---------------------------------------------------------------------------
# IV. Discussion Questions & Overall Quality — LLM-as-Judge (30 pts)
# ---------------------------------------------------------------------------

_LLM_PROMPT_TEMPLATE = """\
You are a teaching assistant for an operating systems course, grading a ChCore Lab3 (Processes and Threads) lab report.
Please strictly score on the following three dimensions based on the report content below.

## Scoring Dimensions

### Dimension 1: Question 4 — Complete flow from kernel to first user mode (0-10 pts)
Question 4 requires explaining "the process from kernel initialization completion to the first switch to a user-mode program".
Key steps should include:
  create_root_thread -> create_root_cap_group (allocate cap_group + vmspace)
  -> read ELF info from procmgr binary -> create_pmo to allocate memory
  -> vmspace_map_range to map ELF segments -> create thread -> init_thread_ctx to initialize context
  -> sched() scheduling -> switch_context -> eret_to_thread -> exception_exit -> eret to EL0

Scoring criteria:
- 9-10: Completely covers all key steps above, principles are clear, logic is coherent
- 6-8: Covers most key steps, explanation is basically correct but incomplete
- 3-5: Mentions some key concepts but explanation is unclear or has obvious omissions
- 0-2: Not answered, very little content, or completely wrong

### Dimension 2: Question 7 — printf to terminal output call chain (0-10 pts)
Question 7 requires explaining "how user-mode printf ultimately outputs to the terminal".
Key call chain should include:
  printf -> vfprintf -> __stdout_write -> __stdio_write
  -> chcore_stdout_write -> put -> chcore_syscall (svc)
  -> kernel sys_putstr -> uart_send

Scoring criteria:
- 9-10: Completely covers the full chain above, principles are clear, accurately explains libc -> system call -> kernel output
- 6-8: Covers most of the call chain, explanation is basically correct but incomplete
- 3-5: Mentions some key functions but logic is unclear
- 0-2: Not answered, very little content, or completely wrong

### Dimension 3: Overall report quality and formatting (0-10 pts)
- 9-10: Markdown formatting is proper, code blocks specify language (c/assembly), each exercise has clear code display + text explanation, logic is coherent, formatting is neat
- 6-8: Formatting is acceptable, most exercises have code and explanations, but some explanations are insufficient or formatting is messy
- 3-5: Formatting is poor or many exercises only have code without explanation
- 0-2: Severely lacking structure and content

Please reply strictly in the following JSON format, do not include anything else:
```json
{{
  "q4_score": 0,
  "q4_reason": "",
  "q7_score": 0,
  "q7_reason": "",
  "quality_score": 0,
  "quality_reason": ""
}}
```

## Report Content (first 8000 characters)

{content}
"""


def _parse_llm_json(raw: str) -> dict:
    """Extract JSON from LLM response"""
    if "```json" in raw:
        raw = raw.split("```json")[1].split("```")[0].strip()
    elif "```" in raw:
        raw = raw.split("```")[1].split("```")[0].strip()
    return json.loads(raw)


def _eval_thinking_and_quality(content: str, answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details: dict = {}

    config = _get_text_eval_config(answer_dir)
    truncated = content[:8000]
    prompt = _LLM_PROMPT_TEMPLATE.format(content=truncated)
    raw = _call_llm_judge(prompt, config)

    if raw:
        try:
            result = _parse_llm_json(raw)
            q4 = max(0, min(10, int(result.get("q4_score", 0))))
            q7 = max(0, min(10, int(result.get("q7_score", 0))))
            qual = max(0, min(10, int(result.get("quality_score", 0))))
            score = q4 + q7 + qual

            details["question_4_10pts"] = f"{q4}/10 — {result.get('q4_reason', '')}"
            details["question_7_10pts"] = f"{q7}/10 — {result.get('q7_reason', '')}"
            details["overall_quality_10pts"] = f"{qual}/10 — {result.get('quality_reason', '')}"
            details["llm_evaluation"] = "Success"
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            print(f"[RUBRIC] LLM response parse failed: {e}")
            print(f"[RUBRIC] Raw response: {raw[:500]}")
            score, details = _fallback_thinking_eval(content)
    else:
        print("[RUBRIC] LLM unavailable, falling back to keyword evaluation")
        score, details = _fallback_thinking_eval(content)

    return score, details


def _fallback_thinking_eval(content: str) -> Tuple[int, dict]:
    """Conservative fallback evaluation when LLM is unavailable (lower score ceiling)"""
    score = 0
    details: dict = {}

    # Question 4 keywords (ceiling 6 pts)
    q4_kws = ["create_root_thread", "cap_group", "vmspace", "sched", "eret",
              "EL0", "switch_context", "init_thread_ctx", "eret_to_thread"]
    q4_found = sum(1 for kw in q4_kws if kw in content)
    if q4_found >= 5:
        q4_score = 6
    elif q4_found >= 3:
        q4_score = 4
    elif q4_found >= 1:
        q4_score = 2
    else:
        q4_score = 0
    score += q4_score
    details["question_4_10pts"] = f"{q4_score}/10 — Fallback, matched {q4_found}/{len(q4_kws)} keywords"

    # Question 7 keywords (ceiling 6 pts)
    q7_kws = ["printf", "vfprintf", "write", "chcore_write", "chcore_stdout_write",
              "syscall", "fd_ops", "uart", "putstr", "sys_putstr"]
    q7_found = sum(1 for kw in q7_kws if kw in content)
    if q7_found >= 5:
        q7_score = 6
    elif q7_found >= 3:
        q7_score = 4
    elif q7_found >= 1:
        q7_score = 2
    else:
        q7_score = 0
    score += q7_score
    details["question_7_10pts"] = f"{q7_score}/10 — Fallback, matched {q7_found}/{len(q7_kws)} keywords"

    # Overall quality (ceiling 5 pts)
    code_blocks = len(re.findall(r"```", content)) // 2
    lang_tagged = len(re.findall(r"```(?:c|asm|assembly|makefile)", content, re.IGNORECASE))
    char_len = len(content)

    if char_len >= 5000 and code_blocks >= 7 and lang_tagged >= 3:
        qual = 5
    elif char_len >= 3000 and code_blocks >= 4:
        qual = 3
    elif char_len >= 1500:
        qual = 2
    elif char_len >= 500:
        qual = 1
    else:
        qual = 0
    score += qual
    details["overall_quality_10pts"] = f"{qual}/10 — Fallback, {char_len} chars, {code_blocks} code blocks, {lang_tagged} with language tags"
    details["llm_evaluation"] = "Unavailable, using fallback keyword evaluation (lower score ceiling)"

    return score, details


# ---------------------------------------------------------------------------
# Main entry
# ---------------------------------------------------------------------------

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Evaluate the agent's output.

    Args:
        answer_dir: absolute path to the agent output directory

    Returns:
        (score, report)
        - score: integer 0-100
        - report: dict containing detailed evaluation report
    """
    report_path = _find_report(answer_dir)

    if not report_path:
        return 0, {
            "total_score": 0,
            "error": "Report file not found (report.md or other .md)",
            "search_directory": answer_dir,
        }

    try:
        with open(report_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception as e:
        return 0, {"total_score": 0, "error": f"Failed to read report file: {e}"}

    if not content.strip():
        return 0, {"total_score": 0, "error": "Report file is empty"}

    s1, r1 = _eval_file_delivery(report_path, content)
    s2, r2 = _eval_structure(content)
    s3, r3 = _eval_code_content(content)
    s4, r4 = _eval_thinking_and_quality(content, answer_dir)

    total = max(0, min(100, s1 + s2 + s3 + s4))

    report: Dict[str, Any] = {
        "total_score": total,
        "evaluated_file": os.path.basename(report_path),
        "dimension_scores": {
            "I_file_delivery": f"{s1}/10",
            "II_report_structure": f"{s2}/20",
            "III_core_code_content": f"{s3}/40",
            "IV_discussion_and_quality": f"{s4}/30",
        },
        "details": {
            "I_file_delivery_10pts": r1,
            "II_report_structure_20pts": r2,
            "III_core_code_content_40pts": r3,
            "IV_discussion_and_quality_30pts": r4,
        },
    }

    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print a formatted scoring report"""
    print("=" * 70)
    print("ChCore Lab3 Lab Report — Scoring Report")
    print("=" * 70)
    print(f"\nTotal Score: {score}/100\n")

    if "error" in report:
        print(f"Error: {report['error']}")
        if "search_directory" in report:
            print(f"Search directory: {report['search_directory']}")
        print("=" * 70)
        return

    print(f"Evaluated file: {report.get('evaluated_file', '?')}")

    scores_map = report.get("dimension_scores", {})
    if scores_map:
        print("\nDimension Scores:")
        for k, v in scores_map.items():
            print(f"  {k}: {v}")

    detail_map = report.get("details", {})
    for section_name, items in detail_map.items():
        print(f"\n{'─' * 60}")
        print(f"[{section_name}]")
        print(f"{'─' * 60}")
        if isinstance(items, dict):
            for k, v in items.items():
                print(f"  {k}: {v}")
        else:
            print(f"  {items}")

    print(f"\n{'=' * 70}")


# ---------------------------------------------------------------------------
# CLI entry
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        test_dir = sys.argv[1]
    else:
        test_dir = os.path.join(os.path.dirname(__file__), "..", "workspace")

    if os.path.isdir(test_dir):
        print(f"Evaluating directory: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"Directory not found: {test_dir}")
    sys.exit(0)
