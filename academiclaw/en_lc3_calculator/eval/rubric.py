"""
Query 5 Scoring Rubric — LC-3 Stack-Based Calculator
Total: 100 points

Scoring dimensions:
  I. File Delivery (10 pts)
      - lab2.asm / answer.asm / solution.asm exists
      - File is non-empty, contains .ORIG and .END
  II. Structural Completeness (25 pts) — Deterministic code checks
      - .ORIG x3000
      - PUSH / POP subroutines
      - Main loop command dispatch (X, C, +, *, %, @, neg, D)
      - RangeCheck [-999, 999]
      - Data section (stack area, prompt strings, constants)
  III. Operation Implementation (25 pts) — Deterministic code checks
      - OpAdd, OpMult, Opmod, OpXOR, Opneg
      - OpClear, OpDisplay
      - Stack restore
  IV. Code Quality — LLM-as-Judge (40 pts)
      - Logical correctness, assembleability, edge case handling, completeness
"""

import os
import re
import json
from typing import Tuple, Dict, Any, Optional, List

try:
    import openai
except ImportError:
    openai = None


# =============================================================================
# Environment & LLM Utilities
# =============================================================================

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


# =============================================================================
# Helper Functions
# =============================================================================

def _find_asm_file(answer_dir: str) -> Optional[str]:
    """Find the answer file: prefer lab2.asm, answer.asm, solution.asm, otherwise any .asm"""
    for name in ("lab2.asm", "answer.asm", "solution.asm"):
        p = os.path.join(answer_dir, name)
        if os.path.isfile(p):
            return p
    try:
        for f in os.listdir(answer_dir):
            if f.lower().endswith(".asm") and os.path.isfile(os.path.join(answer_dir, f)):
                return os.path.join(answer_dir, f)
    except Exception:
        pass
    return None


def _read_file(path: str) -> str:
    """Safely read a file"""
    if not os.path.isfile(path):
        return ""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except Exception:
        return ""


# =============================================================================
# I. File Delivery (10 pts)
# =============================================================================

def _evaluate_file_delivery(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    1.1 File exists (5 pts): lab2.asm/answer.asm/solution.asm = 5, other .asm = 3, none = 0
    1.2 Content validity (5 pts): .ORIG(2) + .END(2) + valid code lines >= 50 (1)
    """
    score = 0
    details: Dict[str, str] = {}
    deductions: List[str] = []

    asm_path = _find_asm_file(answer_dir)

    # 1.1 File exists (5 pts)
    if asm_path is None:
        details["1.1 File exists"] = "0/5 - No .asm file found"
        deductions.append("Missing lab2.asm / answer.asm / solution.asm")
        return 0, {"score": 0, "details": details, "deductions": deductions}

    fname = os.path.basename(asm_path)
    if fname in ("lab2.asm", "answer.asm", "solution.asm"):
        score += 5
        details["1.1 File exists"] = f"5/5 - {fname}"
    else:
        score += 3
        details["1.1 File exists"] = f"3/5 - Found {fname} (non-standard filename)"
        deductions.append(f"Filename {fname} is not lab2.asm/answer.asm/solution.asm")

    # 1.2 Content validity (5 pts)
    content = _read_file(asm_path)
    cu = content.upper()
    if not content.strip():
        details["1.2 Content validity"] = "0/5 - File is empty"
        deductions.append("Answer file is empty")
        return score, {"score": score, "details": details, "deductions": deductions}

    sub = 0
    has_orig = ".ORIG" in cu
    has_end = ".END" in cu
    if has_orig:
        sub += 2
    else:
        deductions.append("Missing .ORIG pseudo-instruction")
    if has_end:
        sub += 2
    else:
        deductions.append("Missing .END pseudo-instruction")

    # Valid code line count (excluding blank lines and pure comment lines)
    line_count = len([
        l for l in content.splitlines()
        if l.strip() and not l.strip().startswith(";")
    ])
    if line_count >= 50:
        sub += 1
    else:
        deductions.append(f"Too few valid code lines ({line_count} lines)")

    score += sub
    details["1.2 Content validity"] = (
        f"{sub}/5 - .ORIG={'yes' if has_orig else 'no'}, "
        f".END={'yes' if has_end else 'no'}, {line_count} valid code lines"
    )

    return score, {"score": score, "details": details, "deductions": deductions}


# =============================================================================
# II. Structural Completeness (25 pts)
# =============================================================================

def _evaluate_structure(content: str) -> Tuple[int, Dict[str, Any]]:
    """
    2.1 .ORIG x3000 (3 pts)
    2.2 PUSH subroutine (4 pts)
    2.3 POP subroutine (4 pts)
    2.4 Main loop command dispatch (8 pts) — detect 8 commands: X,C,+,*,%,@,D,neg
    2.5 RangeCheck (3 pts)
    2.6 Data section (3 pts)
    """
    score = 0
    details: Dict[str, str] = {}
    deductions: List[str] = []
    cu = content.upper()

    # 2.1 .ORIG x3000 (3 pts)
    if re.search(r'\.ORIG\s+[xX]3000', content, re.IGNORECASE):
        score += 3
        details["2.1 .ORIG x3000"] = "3/3"
    else:
        details["2.1 .ORIG x3000"] = "0/3 - .ORIG x3000 not found"
        deductions.append("Does not start with .ORIG x3000")

    # 2.2 PUSH subroutine (4 pts)
    push_score = 0
    if re.search(r'\bPUSH\b', cu):
        push_score += 2
        # STR R0,R6,#0 — the actual push store
        if re.search(r'STR\s+R0\s*,\s*R6', cu):
            push_score += 1
        # ADD R6,R6,#-1 — decrement stack pointer
        if re.search(r'ADD\s+R6\s*,\s*R6\s*,\s*#-1', cu):
            push_score += 1
    details["2.2 PUSH subroutine"] = f"{push_score}/4"
    if push_score < 2:
        deductions.append("PUSH subroutine missing or incomplete")
    score += push_score

    # 2.3 POP subroutine (4 pts)
    pop_score = 0
    if re.search(r'\bPOP\b', cu):
        pop_score += 2
        # LDR R0,R6,#0 — the actual pop load
        if re.search(r'LDR\s+R0\s*,\s*R6', cu):
            pop_score += 1
        # ADD R6,R6,#1 — increment stack pointer
        if re.search(r'ADD\s+R6\s*,\s*R6\s*,\s*#1', cu):
            pop_score += 1
    details["2.3 POP subroutine"] = f"{pop_score}/4"
    if pop_score < 2:
        deductions.append("POP subroutine missing or incomplete")
    score += pop_score

    # 2.4 Main loop command dispatch (8 pts) — 1 pt per command
    dispatch_score = 0
    commands_found = []
    cmd_patterns = {
        "X":   [r'NEGX\b|NEG_X\b|NEGX|xFFA8'],
        "C":   [r'NEGC\b|NEG_C\b|NEGC|xFFBD'],
        "+":   [r'NEGPLUS\b|NEG_PLUS\b|NEGPLUS|xFFD5'],
        "*":   [r'NEGMULT\b|NEG_MULT\b|NEGMULT|xFFD6'],
        "%":   [r'NEGMOD\b|NEG_MOD\b|NEGMOD|xFFDB'],
        "@":   [r'NEGXOR\b|NEG_XOR\b|NEGXOR|xFFC0'],
        "D":   [r'NEGD\b|NEG_D\b|NEGD|xFFBC'],
        "neg": [r'NEGNEG\b|NEG_NEG\b|NEGNEG|xFFD3|xFFD2'],
    }
    for cmd, patterns in cmd_patterns.items():
        for pat in patterns:
            if re.search(pat, cu):
                commands_found.append(cmd)
                dispatch_score += 1
                break
    dispatch_score = min(8, dispatch_score)
    details["2.4 Command dispatch"] = (
        f"{dispatch_score}/8 - Detected: "
        f"{', '.join(commands_found) if commands_found else 'none'}"
    )
    if dispatch_score < 6:
        deductions.append(
            f"Command dispatch incomplete, only detected {len(commands_found)}/8 commands"
        )
    score += dispatch_score

    # 2.5 RangeCheck (3 pts)
    rc_score = 0
    if re.search(r'RANGECHECK\b', cu):
        rc_score += 2
        # Check for -999 or 999 constants
        if re.search(r'#?-?999|xFF03|x03E7', cu):
            rc_score += 1
    details["2.5 RangeCheck"] = f"{rc_score}/3"
    if rc_score == 0:
        deductions.append("Missing RangeCheck subroutine")
    score += rc_score

    # 2.6 Data section (3 pts)
    data_score = 0
    if re.search(r'\.STRINGZ', cu):
        data_score += 1
    if re.search(r'\.FILL', cu):
        data_score += 1
    if re.search(r'\.BLKW|STACKBASE|STACKMAX', cu):
        data_score += 1
    details["2.6 Data section"] = f"{data_score}/3"
    score += data_score

    return score, {"score": score, "details": details, "deductions": deductions}


# =============================================================================
# III. Operation Implementation (25 pts)
# =============================================================================

def _evaluate_operations(content: str) -> Tuple[int, Dict[str, Any]]:
    """
    3.1 OpAdd (4 pts)
    3.2 OpMult (5 pts)
    3.3 Opmod (4 pts)
    3.4 OpXOR (4 pts)
    3.5 Opneg (3 pts)
    3.6 OpClear (2 pts)
    3.7 OpDisplay (2 pts)
    3.8 Stack restore (1 pt)
    """
    score = 0
    details: Dict[str, str] = {}
    deductions: List[str] = []
    cu = content.upper()

    # 3.1 OpAdd (4 pts)
    add_s = 0
    if re.search(r'OPADD\b', cu):
        add_s += 2
        # Two POPs + ADD of two registers
        if re.search(r'ADD\s+R0\s*,\s*R0\s*,\s*R1', cu):
            add_s += 2
        elif re.search(r'ADD\s+R\d\s*,\s*R\d\s*,\s*R\d', cu):
            add_s += 1
    details["3.1 OpAdd"] = f"{add_s}/4"
    if add_s == 0:
        deductions.append("OpAdd not implemented")
    score += add_s

    # 3.2 OpMult (5 pts)
    mult_s = 0
    if re.search(r'OPMULT\b', cu):
        mult_s += 2
        # Multiplication loop
        if re.search(r'MULTLOOP\b|MULTIPLYLOOP\b|MULT_LOOP\b|MUL_LOOP\b', cu):
            mult_s += 2
        elif re.search(r'ADD\s+R\d\s*,\s*R\d\s*,\s*#-1', cu):
            mult_s += 1
        # Sign handling
        if re.search(
            r'NOT\s+R\d\s*,\s*R\d', cu
        ) and re.search(
            r'POSMULTIPLIER\b|POS_MULT|SIGNCHECK', cu, re.IGNORECASE
        ):
            mult_s += 1
    details["3.2 OpMult"] = f"{mult_s}/5"
    if mult_s == 0:
        deductions.append("OpMult not implemented")
    score += mult_s

    # 3.3 Opmod (4 pts)
    mod_s = 0
    if re.search(r'OPMOD\b', cu):
        mod_s += 2
        # Repeated subtraction loop
        if re.search(r'MODLOOP\b|PMODLOOP\b|NMODLOOP\b|MOD_LOOP', cu):
            mod_s += 2
        elif re.search(r'ADD\s+R0\s*,\s*R0\s*,\s*R1', cu):
            mod_s += 1
    details["3.3 Opmod"] = f"{mod_s}/4"
    if mod_s == 0:
        deductions.append("Opmod not implemented")
    score += mod_s

    # 3.4 OpXOR (4 pts)
    xor_s = 0
    if re.search(r'OPXOR\b', cu):
        xor_s += 2
        # Bit-by-bit XOR loop
        if re.search(r'XORLOOP\b|XOR_LOOP\b', cu):
            xor_s += 2
        elif re.search(r'AND\s+R\d\s*,\s*R\d\s*,\s*R\d', cu):
            xor_s += 1
    details["3.4 OpXOR"] = f"{xor_s}/4"
    if xor_s == 0:
        deductions.append("OpXOR not implemented")
    score += xor_s

    # 3.5 Opneg (3 pts)
    neg_s = 0
    if re.search(r'OPNEG\b', cu):
        neg_s += 2
        # NOT R0,R0 + ADD R0,R0,#1 pattern
        if re.search(r'NOT\s+R0\s*,\s*R0', cu):
            neg_s += 1
    details["3.5 Opneg"] = f"{neg_s}/3"
    if neg_s == 0:
        deductions.append("Opneg not implemented")
    score += neg_s

    # 3.6 OpClear (2 pts)
    clear_s = 0
    if re.search(r'OPCLEAR\b', cu):
        clear_s += 1
        # LEA R6, StackBase
        if re.search(r'LEA\s+R6\s*,\s*STACKBASE', cu):
            clear_s += 1
    details["3.6 OpClear"] = f"{clear_s}/2"
    score += clear_s

    # 3.7 OpDisplay (2 pts)
    disp_s = 0
    if re.search(r'OPDISPLAY\b', cu):
        disp_s += 1
        # Display pushes back: ADD R6,R6,#-1
        if re.search(r'ADD\s+R6\s*,\s*R6\s*,\s*#-1', cu):
            disp_s += 1
    details["3.7 OpDisplay"] = f"{disp_s}/2"
    score += disp_s

    # 3.8 Stack restore (1 pt)
    restore_s = 0
    if re.search(r'RESTORE\d?\b', cu):
        restore_s += 1
    details["3.8 Stack restore (Restore)"] = f"{restore_s}/1"
    if restore_s == 0:
        deductions.append("Missing stack restore (Restore) logic for operation failures")
    score += restore_s

    return score, {"score": score, "details": details, "deductions": deductions}


# =============================================================================
# IV. Code Quality — LLM-as-Judge (40 pts)
# =============================================================================

_JUDGE_ASM_MAX_CHARS = 14000

_JUDGE_PROMPT = """\
You are an expert grader for LC-3 assembly programs. You are evaluating a \
student's LC-3 stack-based calculator implementation.

## Task Requirements
The program should:
1. Read commands from user input: X (exit), C (clear stack), + (add), \
* (multiply), % (modulo), @ (XOR), neg (negate), D (display top), \
digits (push number)
2. Use a stack (R6 = stack pointer) with PUSH/POP subroutines \
(R5=0 success, R5=1 failure)
3. Stack grows from high address to low address
4. Range check results to [-999, 999], restore stack on error
5. Start at .ORIG x3000, include all subroutines and data area

## Submitted Program
```asm
{asm_content}
```

## Grading Criteria (score 0-40)
Evaluate the following aspects and provide a total score out of 40:

1. **Logical correctness** (0-15): Is the main loop dispatching commands \
correctly? Are PUSH/POP implementations sound? Do binary operations (add, \
mult, mod, xor) correctly POP two operands and PUSH the result? Does neg \
POP one operand?

2. **Assembleability** (0-10): Would this assemble without errors on a \
standard LC-3 assembler? Are all labels defined? Are .FILL/.STRINGZ/.BLKW \
used correctly? Is addressing within range?

3. **Edge case handling** (0-10): Does RangeCheck work correctly for \
[-999, 999]? Does the program restore the stack on range errors? Does it \
handle stack underflow and overflow? Is the ASCIItoBinary / BinarytoASCII \
conversion correct?

4. **Completeness** (0-5): Are all 8 commands implemented? Is PushValue \
(digit input) implemented? Are all helper routines present?

Please respond in strict JSON format:
```json
{{
  "logical_correctness": {{"score": 0, "comment": ""}},
  "assembleability": {{"score": 0, "comment": ""}},
  "edge_case_handling": {{"score": 0, "comment": ""}},
  "completeness": {{"score": 0, "comment": ""}},
  "total": 0,
  "summary": ""
}}
```
"""


def _evaluate_llm_judge(content: str, answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """LLM-as-Judge code quality evaluation, 40 pts"""
    details: Dict[str, str] = {}
    deductions: List[str] = []

    config = _get_text_eval_config(answer_dir)

    asm_content = content
    if len(asm_content) > _JUDGE_ASM_MAX_CHARS:
        asm_content = (
            asm_content[:_JUDGE_ASM_MAX_CHARS]
            + "\n\n[... truncated for grading ...]"
        )

    prompt = _JUDGE_PROMPT.format(asm_content=asm_content)
    raw_output = _call_llm_judge(prompt, config)

    if not raw_output:
        fb_score, fb_details = _heuristic_fallback(content)
        details["evaluation_method"] = "Heuristic fallback (LLM unavailable)"
        details.update(fb_details)
        return fb_score, {"score": fb_score, "details": details, "deductions": deductions}

    # Parse JSON from LLM output
    try:
        text = raw_output
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        result = json.loads(text)
    except (json.JSONDecodeError, IndexError):
        # Fallback: try to extract total score directly
        m = re.search(r'"total"\s*:\s*(\d+)', raw_output)
        if m:
            total = max(0, min(40, int(m.group(1))))
            details["evaluation_method"] = "LLM Judge (partial JSON parse failure)"
            details["raw_output"] = raw_output[:500]
            return total, {"score": total, "details": details, "deductions": deductions}
        # Full heuristic fallback
        fb_score, fb_details = _heuristic_fallback(content)
        details["evaluation_method"] = "Heuristic fallback (LLM output unparseable)"
        details["LLM raw output"] = raw_output[:300]
        details.update(fb_details)
        return fb_score, {"score": fb_score, "details": details, "deductions": deductions}

    # Extract sub-scores with bounds
    lc = result.get("logical_correctness", {})
    ab = result.get("assembleability", {})
    ec = result.get("edge_case_handling", {})
    cp = result.get("completeness", {})

    lc_score = max(0, min(15, int(lc.get("score", 0))))
    ab_score = max(0, min(10, int(ab.get("score", 0))))
    ec_score = max(0, min(10, int(ec.get("score", 0))))
    cp_score = max(0, min(5, int(cp.get("score", 0))))
    total = max(0, min(40, lc_score + ab_score + ec_score + cp_score))

    details["evaluation_method"] = "LLM-as-Judge"
    details["4.1 Logical correctness (15)"] = f"{lc_score}/15 - {lc.get('comment', '')}"
    details["4.2 Assembleability (10)"] = f"{ab_score}/10 - {ab.get('comment', '')}"
    details["4.3 Edge case handling (10)"] = f"{ec_score}/10 - {ec.get('comment', '')}"
    details["4.4 Completeness (5)"] = f"{cp_score}/5 - {cp.get('comment', '')}"
    details["LLM summary"] = str(result.get("summary", ""))[:300]

    if lc_score < 8:
        deductions.append("Insufficient logical correctness")
    if ab_score < 5:
        deductions.append("Assembleability issues detected")

    return total, {"score": total, "details": details, "deductions": deductions}


def _heuristic_fallback(content: str) -> Tuple[int, Dict[str, str]]:
    """Heuristic scoring when LLM is unavailable (0-40, capped at 30)"""
    cu = content.upper()
    score = 0
    details: Dict[str, str] = {}

    checks = [
        ("JSR PUSH", 3, "Calls PUSH"),
        ("JSR POP", 3, "Calls POP"),
        ("JSR RANGECHECK", 3, "Calls RangeCheck"),
        ("GETC", 2, "Reads input (GETC)"),
        ("PUTS", 2, "Outputs string (PUTS)"),
        ("HALT", 2, "Program exit (HALT)"),
        ("ASCIITOBINARY", 3, "ASCII to binary"),
        ("BINARYTOASCII", 3, "Binary to ASCII"),
        ("NEWCOMMAND", 2, "Main loop (NewCommand)"),
    ]

    found = []
    for keyword, pts, desc in checks:
        if keyword in cu:
            score += pts
            found.append(desc)

    # JSR call count bonus
    jsr_count = len(re.findall(r'\bJSR\b', cu))
    if jsr_count >= 10:
        score += 3
    elif jsr_count >= 5:
        score += 2

    # Label count bonus
    label_count = len(
        re.findall(r'^[A-Za-z]\w+\s', content, re.MULTILINE)
    )
    if label_count >= 15:
        score += 4
    elif label_count >= 8:
        score += 2

    score = max(0, min(30, score))
    details["heuristic_checks"] = f"Detected: {'; '.join(found)}"
    details["JSR call count"] = str(jsr_count)
    details["label count"] = str(label_count)
    return score, details


# =============================================================================
# Entry Point
# =============================================================================

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Evaluate the agent's output.

    Args:
        answer_dir: Absolute path to the agent's output directory
                    (e.g., /path/to/query/gpt-5/attempt_1)

    Returns:
        (score, report)
        - score: integer from 0 to 100
        - report: dict containing the detailed evaluation report
    """
    # I. File Delivery (10 pts)
    s1, r1 = _evaluate_file_delivery(answer_dir)

    # If no file found, return 0 immediately
    asm_path = _find_asm_file(answer_dir)
    if asm_path is None:
        report = {
            "total_score": 0,
            "result_score": {
                "score": 0,
                "details": r1.get("details", {}),
                "deductions": r1.get("deductions", []),
            },
            "process_score": {"score": 0, "details": {}, "deductions": []},
            "comment": "No LC-3 assembly answer file found.",
        }
        return 0, report

    content = _read_file(asm_path)
    if not content.strip():
        report = {
            "total_score": s1,
            "result_score": {
                "score": s1,
                "details": r1.get("details", {}),
                "deductions": r1.get("deductions", []),
            },
            "process_score": {"score": 0, "details": {}, "deductions": []},
            "comment": "Answer file is empty.",
        }
        return s1, report

    # II. Structural Completeness (25 pts)
    s2, r2 = _evaluate_structure(content)

    # III. Operation Implementation (25 pts)
    s3, r3 = _evaluate_operations(content)

    # IV. LLM-as-Judge (40 pts)
    s4, r4 = _evaluate_llm_judge(content, answer_dir)

    total = max(0, min(100, s1 + s2 + s3 + s4))

    # Comment
    if total >= 90:
        comment = "Excellent. The LC-3 stack calculator implementation is complete and logically correct."
    elif total >= 75:
        comment = "Good. Main features are correct; some details could be improved."
    elif total >= 60:
        comment = "Passing. Basic stack and operation implementation present; range checking or some operations need improvement."
    elif total >= 40:
        comment = "Partially complete. Significant omissions or logical errors exist."
    else:
        comment = "Below standard. Please check PUSH/POP and operation implementations."

    report = {
        "total_score": total,
        "result_score": {
            "score": s1 + s2 + s3,
            "details": {
                "I. File Delivery (10 pts)": r1.get("details", {}),
                "II. Structural Completeness (25 pts)": r2.get("details", {}),
                "III. Operation Implementation (25 pts)": r3.get("details", {}),
            },
            "deductions": (
                r1.get("deductions", [])
                + r2.get("deductions", [])
                + r3.get("deductions", [])
            ),
        },
        "process_score": {
            "score": s4,
            "details": {"IV. Code Quality LLM Judge (40 pts)": r4.get("details", {})},
            "deductions": r4.get("deductions", []),
        },
        "comment": comment,
        "breakdown": {
            "File Delivery": f"{s1}/10",
            "Structural Completeness": f"{s2}/25",
            "Operation Implementation": f"{s3}/25",
            "LLM Judge": f"{s4}/40",
        },
    }
    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print a formatted scoring report"""
    print("=" * 70)
    print("Query 5 Scoring Report — LC-3 Stack-Based Calculator")
    print("=" * 70)
    print(f"\nTotal Score: {score}/100\n")

    scores = report.get("breakdown", {})
    if scores:
        print("Breakdown:")
        for k, v in scores.items():
            print(f"  {k}: {v}")

    for section_key, section_label in [
        ("result_score", "Result Score (File + Structure + Operations)"),
        ("process_score", "Process Score (LLM Judge)"),
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
        os.path.dirname(__file__), "..", "gpt-5", "attempt_1"
    )
    if os.path.exists(test_dir):
        print(f"Evaluating directory: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"Directory not found: {test_dir}")
    sys.exit(0)
