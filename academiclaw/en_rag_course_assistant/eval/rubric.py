"""
RAG Intelligent Course Assistant System Implementation — Scoring Rubric

Task: Complete the core modules marked with [TODO] in the RAG-based course
      assistant system, enabling the full pipeline: build database
      (process_data.py) -> interactive Q&A (main.py).

Deliverables:
  - process_data.py  — Completes data processing and database building
  - main.py          — Supports interactive Q&A with citations
  - vector_db/       — Built vector database

Total: 100 points

Scoring Dimensions:
  I. File Delivery & Basic Checks (15 points)
      1.1 process_data.py exists and is parseable (3)
      1.2 main.py exists and is parseable (3)
      1.3 vector_db/ exists and is non-empty (4)
      1.4 Auxiliary modules exist (5): document_loader.py / text_splitter.py /
          vector_store.py / rag_agent.py / config.py (1 point each)

  II. TODO Completion — Static Code Analysis (35 points)
      2.1 DocumentLoader four loaders implemented (8): load_pdf / load_pptx /
          load_docx / load_txt 2 points each
      2.2 TextSplitter.split_text implemented (5)
      2.3 VectorStore implemented (10): get_embedding(3) / add_documents(3) /
          search(4)
      2.4 RAGAgent implemented (12): system_prompt reasonable(3) /
          retrieve_context implemented(4) / generate_response user_text implemented(5)

  III. Functional Correctness — Dynamic Checks (25 points)
      3.1 process_data.py importable without errors (5)
      3.2 main.py importable without errors (5)
      3.3 vector_db has actual data (5) — ChromaDB sqlite3 exists and >10KB
      3.4 Code logic completeness (10) — LLM-as-Judge evaluates whether the code
          truly implements the RAG pipeline

  IV. RAG Quality — LLM-as-Judge (25 points)
      4.1 System prompt quality (8) — Whether course assistant role, citation rules,
          and no-fabrication policy are defined
      4.2 Context formatting (8) — Whether retrieval results include source info
          (filename + page number)
      4.3 Answer citation annotation (9) — Whether user_text guides the model to
          output answers with citations
"""

import os
import re
import ast
import json
import traceback
from typing import Tuple, Dict, Any, List, Optional

try:
    import openai
except ImportError:
    openai = None


# ─────────────────────────────────────────────────────────────────────
# Environment / LLM Utilities
# ─────────────────────────────────────────────────────────────────────

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
    env = _load_env(answer_dir)
    def g(key, default=""):
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
        print(f"[RUBRIC] LLM Judge call failed: {e}")
        return ""


def _safe_read(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception:
        return ""


def _can_parse(code: str) -> bool:
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False


# ─────────────────────────────────────────────────────────────────────
# I. File Delivery & Basic Checks (15 points)
# ─────────────────────────────────────────────────────────────────────

def _evaluate_file_delivery(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    score = 0
    details: Dict[str, str] = {}
    deductions: List[str] = []

    all_files = set(os.listdir(answer_dir)) if os.path.isdir(answer_dir) else set()

    # 1.1 process_data.py (3)
    pdp = os.path.join(answer_dir, "process_data.py")
    if "process_data.py" in all_files:
        code = _safe_read(pdp)
        if _can_parse(code):
            score += 3
            details["1.1 process_data.py"] = "3/3 - exists and syntax correct"
        else:
            score += 1
            details["1.1 process_data.py"] = "1/3 - exists but has syntax errors"
            deductions.append("process_data.py has syntax errors")
    else:
        details["1.1 process_data.py"] = "0/3 - file missing"
        deductions.append("Missing process_data.py")

    # 1.2 main.py (3)
    mp = os.path.join(answer_dir, "main.py")
    if "main.py" in all_files:
        code = _safe_read(mp)
        if _can_parse(code):
            score += 3
            details["1.2 main.py"] = "3/3 - exists and syntax correct"
        else:
            score += 1
            details["1.2 main.py"] = "1/3 - exists but has syntax errors"
            deductions.append("main.py has syntax errors")
    else:
        details["1.2 main.py"] = "0/3 - file missing"
        deductions.append("Missing main.py")

    # 1.3 vector_db/ (4)
    vdb = os.path.join(answer_dir, "vector_db")
    if os.path.isdir(vdb):
        vdb_files = []
        for root, dirs, files in os.walk(vdb):
            vdb_files.extend(files)
        if len(vdb_files) > 0:
            total_size = sum(
                os.path.getsize(os.path.join(r, f))
                for r, _, fls in os.walk(vdb)
                for f in fls
            )
            if total_size > 1024:
                score += 4
                details["1.3 vector_db/"] = f"4/4 - exists, {len(vdb_files)} files, {total_size/1024:.0f}KB"
            else:
                score += 2
                details["1.3 vector_db/"] = f"2/4 - exists but data is very small ({total_size}B)"
                deductions.append("vector_db data size too small")
        else:
            score += 1
            details["1.3 vector_db/"] = "1/4 - directory exists but is empty"
            deductions.append("vector_db directory is empty")
    else:
        details["1.3 vector_db/"] = "0/4 - directory missing"
        deductions.append("Missing vector_db/ directory")

    # 1.4 Auxiliary modules (5)
    aux_modules = ["document_loader.py", "text_splitter.py",
                   "vector_store.py", "rag_agent.py", "config.py"]
    aux_score = 0
    aux_detail = []
    for mod in aux_modules:
        if mod in all_files:
            aux_score += 1
            aux_detail.append(f"{mod} [OK]")
        else:
            aux_detail.append(f"{mod} [X]")
            deductions.append(f"Missing auxiliary module {mod}")
    score += aux_score
    details["1.4 Auxiliary modules (5)"] = f"{aux_score}/5 - " + ", ".join(aux_detail)

    return score, {"score": f"{score}/15", "details": details, "deductions": deductions}


# ─────────────────────────────────────────────────────────────────────
# II. TODO Completion — Static Code Analysis (35 points)
# ─────────────────────────────────────────────────────────────────────

def _evaluate_todo_completion(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    score = 0
    details: Dict[str, str] = {}
    deductions: List[str] = []

    def read_module(name: str) -> str:
        return _safe_read(os.path.join(answer_dir, name))

    # ── 2.1 DocumentLoader four loaders (8 points, 2 each) ──
    dl_code = read_module("document_loader.py")
    loader_score = 0
    loader_detail = []

    for method, label in [("load_pdf", "PDF"), ("load_pptx", "PPTX"),
                           ("load_docx", "DOCX"), ("load_txt", "TXT")]:
        pattern = rf'def {method}\s*\(self.*?\).*?(?=\ndef |\nclass |\Z)'
        match = re.search(pattern, dl_code, re.DOTALL)
        if match:
            body = match.group(0)
            has_impl = (
                ("return" in body and "pass" not in body.split("return")[0].split("\n")[-1])
                or "pages.append" in body
                or "slides.append" in body
                or "docx2txt" in body
                or "open(" in body
                or "PdfReader" in body
                or "Presentation" in body
            )
            if has_impl:
                loader_score += 2
                loader_detail.append(f"{label} [OK]")
            else:
                loader_detail.append(f"{label} [empty implementation]")
                deductions.append(f"{method} not implemented (only pass or empty return)")
        else:
            loader_detail.append(f"{label} [missing]")
            deductions.append(f"Missing {method} method")

    score += loader_score
    details["2.1 DocumentLoader (8)"] = f"{loader_score}/8 - " + ", ".join(loader_detail)

    # ── 2.2 TextSplitter.split_text (5 points) ──
    ts_code = read_module("text_splitter.py")
    ts_score = 0
    split_match = re.search(r'def split_text\s*\(self.*?\).*?(?=\ndef |\nclass |\Z)',
                            ts_code, re.DOTALL)
    if split_match:
        body = split_match.group(0)
        has_loop = "while" in body or "for" in body
        has_chunk = "chunk" in body.lower()
        has_overlap = "overlap" in body.lower() or "self.chunk_overlap" in body
        if has_loop and has_chunk:
            ts_score = 5 if has_overlap else 3
            details["2.2 TextSplitter.split_text (5)"] = f"{ts_score}/5 - " + (
                "loop + splitting + overlap" if ts_score == 5 else "loop + splitting, missing overlap logic"
            )
        else:
            ts_score = 1
            details["2.2 TextSplitter.split_text (5)"] = "1/5 - method exists but implementation is incomplete"
            deductions.append("split_text implementation is incomplete")
    else:
        details["2.2 TextSplitter.split_text (5)"] = "0/5 - method missing"
        deductions.append("Missing split_text method")
    score += ts_score

    # ── 2.3 VectorStore (10 points) ──
    vs_code = read_module("vector_store.py")
    vs_score = 0
    vs_detail = []

    # get_embedding (3)
    ge_match = re.search(r'def get_embedding\s*\(self.*?\).*?(?=\ndef |\nclass |\Z)',
                         vs_code, re.DOTALL)
    if ge_match:
        body = ge_match.group(0)
        has_api_call = "embeddings.create" in body or "embedding" in body.lower()
        has_return = "return" in body
        if has_api_call and has_return:
            vs_score += 3
            vs_detail.append("get_embedding [OK 3/3]")
        else:
            vs_score += 1
            vs_detail.append("get_embedding [partial 1/3]")
            deductions.append("get_embedding implementation is incomplete")
    else:
        vs_detail.append("get_embedding [missing 0/3]")
        deductions.append("Missing get_embedding method")

    # add_documents (3)
    ad_match = re.search(r'def add_documents\s*\(self.*?\).*?(?=\ndef |\nclass |\Z)',
                         vs_code, re.DOTALL)
    if ad_match:
        body = ad_match.group(0)
        has_add = "collection.add" in body or ".add(" in body
        has_loop = "for" in body
        if has_add and has_loop:
            vs_score += 3
            vs_detail.append("add_documents [OK 3/3]")
        elif has_add or has_loop:
            vs_score += 1
            vs_detail.append("add_documents [partial 1/3]")
            deductions.append("add_documents implementation is incomplete")
        else:
            vs_detail.append("add_documents [empty 0/3]")
            deductions.append("add_documents not implemented")
    else:
        vs_detail.append("add_documents [missing 0/3]")
        deductions.append("Missing add_documents method")

    # search (4)
    se_match = re.search(r'def search\s*\(self.*?\).*?(?=\ndef |\nclass |\Z)',
                         vs_code, re.DOTALL)
    if se_match:
        body = se_match.group(0)
        has_query = "collection.query" in body or ".query(" in body
        has_embed = "get_embedding" in body or "embedding" in body.lower()
        if has_query and has_embed:
            vs_score += 4
            vs_detail.append("search [OK 4/4]")
        elif has_query or has_embed:
            vs_score += 2
            vs_detail.append("search [partial 2/4]")
            deductions.append("search implementation is incomplete")
        else:
            vs_detail.append("search [empty 0/4]")
            deductions.append("search not implemented")
    else:
        vs_detail.append("search [missing 0/4]")
        deductions.append("Missing search method")

    score += vs_score
    details["2.3 VectorStore (10)"] = f"{vs_score}/10 - " + ", ".join(vs_detail)

    # ── 2.4 RAGAgent (12 points) ──
    ra_code = read_module("rag_agent.py")
    ra_score = 0
    ra_detail = []

    # system_prompt (3)
    sp_match = re.search(r'self\.system_prompt\s*=\s*(.+)', ra_code)
    if sp_match:
        sp_val = sp_match.group(1).strip()
        is_placeholder = sp_val in ['"""你是这门课程的助教..."""', "''", '""', '"""..."""']
        if not is_placeholder and len(sp_val) > 30:
            ra_score += 3
            ra_detail.append("system_prompt [OK 3/3]")
        elif not is_placeholder:
            ra_score += 1
            ra_detail.append("system_prompt [too short 1/3]")
            deductions.append("system_prompt content is too short")
        else:
            ra_detail.append("system_prompt [placeholder not modified 0/3]")
            deductions.append("system_prompt not modified, still a placeholder")
    else:
        ra_detail.append("system_prompt [missing 0/3]")
        deductions.append("system_prompt not defined")

    # retrieve_context (4)
    rc_match = re.search(r'def retrieve_context\s*\(self.*?\).*?(?=\ndef |\nclass |\Z)',
                         ra_code, re.DOTALL)
    if rc_match:
        body = rc_match.group(0)
        lines = [l.strip() for l in body.split("\n")
                 if l.strip()
                 and not l.strip().startswith("#")
                 and not l.strip().startswith('"""')
                 and not l.strip().startswith("'''")]
        is_only_pass = (
            any(l == "pass" for l in lines)
            and len([l for l in lines
                     if not l.startswith("def")
                     and l != "pass"
                     and not l.startswith("TODO")
                     and not l.startswith("要求")]) < 2
        )
        has_search = "search" in body or "vector_store" in body
        has_format = ("format" in body.lower() or "文件名" in body
                      or "filename" in body or "page" in body or "页" in body)
        has_return = "return" in body

        if has_search and has_format and has_return and not is_only_pass:
            ra_score += 4
            ra_detail.append("retrieve_context [OK 4/4]")
        elif has_search and has_return and not is_only_pass:
            ra_score += 2
            ra_detail.append("retrieve_context [partial 2/4] - missing source formatting")
            deductions.append("retrieve_context missing source info formatting")
        elif not is_only_pass and has_return:
            ra_score += 1
            ra_detail.append("retrieve_context [partial 1/4]")
            deductions.append("retrieve_context implementation is incomplete")
        else:
            ra_detail.append("retrieve_context [not implemented 0/4]")
            deductions.append("retrieve_context not implemented (still pass)")
    else:
        ra_detail.append("retrieve_context [missing 0/4]")
        deductions.append("Missing retrieve_context method")

    # generate_response — user_text (5)
    gr_match = re.search(r'def generate_response\s*\(self.*?\).*?(?=\ndef |\nclass |\Z)',
                         ra_code, re.DOTALL)
    if gr_match:
        body = gr_match.group(0)
        ut_match = re.search(r'user_text\s*=\s*(.+)', body)
        if ut_match:
            ut_val = ut_match.group(1).strip()
            is_empty = ut_val in ['""""""', '""', "''", "f''", 'f""']
            has_context = ("context" in body.lower()
                           and ("query" in body.lower()
                                or "question" in body.lower()
                                or "问题" in body))
            has_source = ("来源" in body or "引用" in body
                          or "source" in body.lower()
                          or "reference" in body.lower()
                          or "citation" in body.lower()
                          or "文件名" in body or "filename" in body)

            if not is_empty and has_context and has_source:
                ra_score += 5
                ra_detail.append("user_text [OK 5/5]")
            elif not is_empty and has_context:
                ra_score += 3
                ra_detail.append("user_text [partial 3/5] - missing citation guidance")
                deductions.append("user_text missing citation annotation guidance")
            elif not is_empty:
                ra_score += 1
                ra_detail.append("user_text [partial 1/5]")
                deductions.append("user_text implementation is incomplete")
            else:
                ra_detail.append("user_text [empty 0/5] - still an empty string")
                deductions.append("user_text not modified, still an empty string")
        else:
            ra_detail.append("user_text [missing 0/5]")
            deductions.append("user_text assignment not found in generate_response")
    else:
        ra_detail.append("generate_response [missing 0/5]")
        deductions.append("Missing generate_response method")

    score += ra_score
    details["2.4 RAGAgent (12)"] = f"{ra_score}/12 - " + ", ".join(ra_detail)

    return score, {"score": f"{score}/35", "details": details, "deductions": deductions}


# ─────────────────────────────────────────────────────────────────────
# III. Functional Correctness — Dynamic Checks (25 points)
# ─────────────────────────────────────────────────────────────────────

def _evaluate_functionality(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    score = 0
    details: Dict[str, str] = {}
    deductions: List[str] = []

    # 3.1 process_data.py structure (5)
    pdp_path = os.path.join(answer_dir, "process_data.py")
    if os.path.exists(pdp_path):
        code = _safe_read(pdp_path)
        if _can_parse(code):
            has_loader = "DocumentLoader" in code or "document_loader" in code
            has_splitter = "TextSplitter" in code or "text_splitter" in code
            has_vstore = "VectorStore" in code or "vector_store" in code
            has_main = "def main" in code or "__main__" in code
            checks = sum([has_loader, has_splitter, has_vstore, has_main])
            if checks >= 3:
                score += 5
                details["3.1 process_data.py structure"] = "5/5 - contains complete data processing pipeline"
            elif checks >= 2:
                score += 3
                details["3.1 process_data.py structure"] = f"3/5 - partial pipeline components ({checks}/4)"
                deductions.append("process_data.py pipeline is incomplete")
            else:
                score += 1
                details["3.1 process_data.py structure"] = f"1/5 - insufficient pipeline components ({checks}/4)"
                deductions.append("process_data.py missing key pipeline components")
        else:
            details["3.1 process_data.py structure"] = "0/5 - syntax error"
            deductions.append("process_data.py has syntax errors, cannot parse")
    else:
        details["3.1 process_data.py structure"] = "0/5 - file missing"
        deductions.append("Missing process_data.py")

    # 3.2 main.py structure (5)
    mp_path = os.path.join(answer_dir, "main.py")
    if os.path.exists(mp_path):
        code = _safe_read(mp_path)
        if _can_parse(code):
            has_agent = "RAGAgent" in code or "rag_agent" in code
            has_chat = "chat" in code
            has_main = "def main" in code or "__main__" in code
            checks = sum([has_agent, has_chat, has_main])
            if checks >= 2:
                score += 5
                details["3.2 main.py structure"] = "5/5 - contains RAGAgent initialization and interaction entry"
            else:
                score += 2
                details["3.2 main.py structure"] = f"2/5 - incomplete structure ({checks}/3)"
                deductions.append("main.py structure is incomplete")
        else:
            details["3.2 main.py structure"] = "0/5 - syntax error"
            deductions.append("main.py has syntax errors")
    else:
        details["3.2 main.py structure"] = "0/5 - file missing"
        deductions.append("Missing main.py")

    # 3.3 vector_db has actual data (5)
    vdb = os.path.join(answer_dir, "vector_db")
    sqlite_path = None
    if os.path.isdir(vdb):
        for root, dirs, files in os.walk(vdb):
            for f in files:
                if f.endswith(".sqlite3"):
                    sqlite_path = os.path.join(root, f)
                    break
            if sqlite_path:
                break

    if sqlite_path:
        size = os.path.getsize(sqlite_path)
        if size > 100 * 1024:
            score += 5
            details["3.3 vector_db data"] = f"5/5 - ChromaDB sqlite3 exists, {size/1024:.0f}KB"
        elif size > 10 * 1024:
            score += 3
            details["3.3 vector_db data"] = f"3/5 - data is somewhat small ({size/1024:.0f}KB)"
        else:
            score += 1
            details["3.3 vector_db data"] = f"1/5 - data is very small ({size/1024:.0f}KB)"
            deductions.append("vector_db data size too small")
    elif os.path.isdir(vdb):
        total_size = sum(
            os.path.getsize(os.path.join(r, f))
            for r, _, fls in os.walk(vdb) for f in fls
        )
        if total_size > 10 * 1024:
            score += 3
            details["3.3 vector_db data"] = f"3/5 - no sqlite3 but has data ({total_size/1024:.0f}KB)"
        else:
            score += 1
            details["3.3 vector_db data"] = f"1/5 - insufficient data"
            deductions.append("vector_db data is insufficient")
    else:
        details["3.3 vector_db data"] = "0/5 - vector_db directory missing"
        deductions.append("Missing vector_db directory")

    # 3.4 Code logic completeness — LLM-as-Judge (10)
    modules_code = {}
    for mod in ["rag_agent.py", "vector_store.py", "document_loader.py",
                "text_splitter.py", "process_data.py", "main.py"]:
        c = _safe_read(os.path.join(answer_dir, mod))
        if c:
            modules_code[mod] = c

    if modules_code:
        code_snippet = ""
        for name, code in modules_code.items():
            lines = code.split("\n")[:150]
            code_snippet += f"\n\n=== {name} ===\n" + "\n".join(lines)

        llm_prompt = f"""You are a code review expert. Below is the code for a RAG course assistant system. Please evaluate whether this code truly implements a complete RAG pipeline.

Task requirements:
1. Document parsing: Support PDF, PPTX, DOCX, TXT four formats
2. Text splitting: Support chunk_size and chunk_overlap
3. Vector database: Generate embeddings and write to ChromaDB, support Top-K retrieval
4. RAG Agent: Define system prompt, retrieve and format context (including filename + page number), answers must include citations

Code:
{code_snippet}

Please score strictly (integer 0-10), evaluating whether the code truly implements all the above features.
Note: If key methods are still pass / empty strings / TODO placeholders, it means the agent did not complete the task and should receive a low score.

Please reply strictly in the following JSON format (do not include other content):
```json
{{
  "score": 0,
  "has_document_loading": true,
  "has_text_splitting": true,
  "has_vector_store": true,
  "has_rag_agent": true,
  "has_citation": true,
  "issues": ["issue 1", "issue 2"],
  "comment": "overall evaluation"
}}
```"""

        config = _get_text_eval_config(answer_dir)
        llm_resp = _call_llm_judge(llm_prompt, config)

        if llm_resp:
            try:
                if "```json" in llm_resp:
                    llm_resp = llm_resp.split("```json")[1].split("```")[0].strip()
                elif "```" in llm_resp:
                    llm_resp = llm_resp.split("```")[1].split("```")[0].strip()
                result = json.loads(llm_resp)
                llm_score = max(0, min(10, int(result.get("score", 0))))
                score += llm_score
                details["3.4 Code completeness (LLM)"] = f"{llm_score}/10 - {result.get('comment', '')}"
                issues = result.get("issues", [])
                if issues:
                    for iss in issues[:3]:
                        deductions.append(f"LLM: {iss}")
            except (json.JSONDecodeError, ValueError):
                score += 3
                details["3.4 Code completeness (LLM)"] = "3/10 - LLM response parsing failed, giving conservative score"
        else:
            score += 3
            details["3.4 Code completeness (LLM)"] = "3/10 - LLM unavailable, giving conservative score"
    else:
        details["3.4 Code completeness (LLM)"] = "0/10 - no code files to evaluate"
        deductions.append("No code files available for LLM evaluation")

    return score, {"score": f"{score}/25", "details": details, "deductions": deductions}


# ─────────────────────────────────────────────────────────────────────
# IV. RAG Quality — LLM-as-Judge (25 points)
# ─────────────────────────────────────────────────────────────────────

def _evaluate_rag_quality(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    score = 0
    details: Dict[str, str] = {}
    deductions: List[str] = []

    ra_code = _safe_read(os.path.join(answer_dir, "rag_agent.py"))
    vs_code = _safe_read(os.path.join(answer_dir, "vector_store.py"))

    if not ra_code:
        return 0, {"score": "0/25", "details": {"error": "rag_agent.py missing or empty"},
                    "deductions": ["Missing rag_agent.py"]}

    llm_prompt = f"""You are a RAG system review expert. Below is the core code of a RAG course assistant system.
Please score strictly across three dimensions.

=== rag_agent.py ===
{ra_code[:4000]}

=== vector_store.py (partial) ===
{vs_code[:2000]}

**Dimension 1: System Prompt Quality (0-8 points)**
Check the content of self.system_prompt:
- 8 points: Clearly defines course assistant role, includes citation rules, no-fabrication policy, answer based on retrieved content, and other complete strategies
- 5-7 points: Defines role but rules are incomplete
- 2-4 points: Has a prompt but content is vague or too simple
- 0-1 points: Still a placeholder (e.g., "You are the course assistant...") or empty

**Dimension 2: Context Formatting (0-8 points)**
Check the retrieve_context method:
- 8 points: Calls vector search, formatted results include filename and page number/slide number, returns clear structure
- 5-7 points: Has search and formatting but source info is incomplete
- 2-4 points: Has basic search but formatting is inadequate
- 0-1 points: Still pass / not implemented

**Dimension 3: Answer Citation Annotation (0-9 points)**
Check user_text in generate_response:
- 9 points: user_text includes retrieved context, user question, and explicitly requires the model to annotate citation sources in the answer
- 5-8 points: Includes context and question but citation requirements are not clear enough
- 2-4 points: Has partial content but incomplete
- 0-1 points: user_text is still an empty string

Please reply strictly in the following JSON format (do not include other content):
```json
{{
  "system_prompt_quality": {{"score": 0, "reason": ""}},
  "context_formatting": {{"score": 0, "reason": ""}},
  "citation_guidance": {{"score": 0, "reason": ""}},
  "total": 0
}}
```"""

    config = _get_text_eval_config(answer_dir)
    llm_resp = _call_llm_judge(llm_prompt, config)

    if llm_resp:
        try:
            if "```json" in llm_resp:
                llm_resp = llm_resp.split("```json")[1].split("```")[0].strip()
            elif "```" in llm_resp:
                llm_resp = llm_resp.split("```")[1].split("```")[0].strip()
            result = json.loads(llm_resp)

            sp = result.get("system_prompt_quality", {})
            cf = result.get("context_formatting", {})
            cg = result.get("citation_guidance", {})

            sp_score = max(0, min(8, int(sp.get("score", 0))))
            cf_score = max(0, min(8, int(cf.get("score", 0))))
            cg_score = max(0, min(9, int(cg.get("score", 0))))

            score = sp_score + cf_score + cg_score
            details["4.1 System prompt (8)"] = f"{sp_score}/8 - {sp.get('reason', '')}"
            details["4.2 Context formatting (8)"] = f"{cf_score}/8 - {cf.get('reason', '')}"
            details["4.3 Citation annotation (9)"] = f"{cg_score}/9 - {cg.get('reason', '')}"

            if sp_score <= 2:
                deductions.append("System prompt quality is low or not modified")
            if cf_score <= 2:
                deductions.append("Context formatting not implemented or missing source info")
            if cg_score <= 2:
                deductions.append("Answer citation annotation not guided or user_text is empty")
        except (json.JSONDecodeError, ValueError):
            score, details, deductions = _fallback_rag_quality(ra_code)
    else:
        score, details, deductions = _fallback_rag_quality(ra_code)

    return score, {"score": f"{score}/25", "details": details, "deductions": deductions}


def _fallback_rag_quality(ra_code: str) -> Tuple[int, Dict[str, str], List[str]]:
    """Fallback static evaluation when LLM is unavailable"""
    score = 0
    details: Dict[str, str] = {}
    deductions: List[str] = []

    # 4.1 system_prompt
    sp_match = re.search(r'self\.system_prompt\s*=\s*(.+)', ra_code)
    if sp_match:
        val = sp_match.group(1)
        if len(val) > 50 and ("助教" in val or "课程" in val or "引用" in val
                               or "assistant" in val.lower() or "course" in val.lower()
                               or "citation" in val.lower() or "reference" in val.lower()):
            score += 4
            details["4.1 System prompt (8)"] = "4/8 - fallback evaluation: has substantive content"
        elif val not in ['"""你是这门课程的助教..."""']:
            score += 2
            details["4.1 System prompt (8)"] = "2/8 - fallback evaluation: modified but content uncertain"
        else:
            details["4.1 System prompt (8)"] = "0/8 - fallback evaluation: still a placeholder"
            deductions.append("system_prompt not modified")
    else:
        details["4.1 System prompt (8)"] = "0/8 - fallback evaluation: not found"
        deductions.append("system_prompt not found")

    # 4.2 retrieve_context
    rc_match = re.search(r'def retrieve_context\b.*?(?=\ndef |\nclass |\Z)',
                         ra_code, re.DOTALL)
    if rc_match:
        body = rc_match.group(0)
        has_search = "search" in body or "vector_store" in body
        has_source = "filename" in body or "文件名" in body or "page" in body
        if has_search and has_source:
            score += 4
            details["4.2 Context formatting (8)"] = "4/8 - fallback evaluation: has search and source info"
        elif has_search:
            score += 2
            details["4.2 Context formatting (8)"] = "2/8 - fallback evaluation: has search but missing source info"
        else:
            details["4.2 Context formatting (8)"] = "0/8 - fallback evaluation: not implemented"
            deductions.append("retrieve_context not implemented")
    else:
        details["4.2 Context formatting (8)"] = "0/8 - fallback evaluation: method missing"
        deductions.append("Missing retrieve_context")

    # 4.3 user_text
    ut_match = re.search(r'user_text\s*=\s*(.+)', ra_code)
    if ut_match:
        val = ut_match.group(1).strip()
        is_empty = val in ['""""""', '""', "''"]
        if not is_empty and ("context" in ra_code.lower() or "引用" in ra_code):
            score += 4
            details["4.3 Citation annotation (9)"] = "4/9 - fallback evaluation: has content"
        elif not is_empty:
            score += 2
            details["4.3 Citation annotation (9)"] = "2/9 - fallback evaluation: modified"
        else:
            details["4.3 Citation annotation (9)"] = "0/9 - fallback evaluation: still empty"
            deductions.append("user_text is empty")
    else:
        details["4.3 Citation annotation (9)"] = "0/9 - fallback evaluation: not found"
        deductions.append("user_text not found")

    details["note"] = "LLM unavailable, using fallback static evaluation, scores may be lower"
    return score, details, deductions


# ═════════════════════════════════════════════════════════════════════
# Entry Point
# ═════════════════════════════════════════════════════════════════════

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Evaluate the agent's RAG course assistant system implementation.

    Args:
        answer_dir: Absolute path to the agent's output directory

    Returns:
        (score, report) — score is an integer from 0-100, report is a detailed evaluation report
    """
    s1, r1 = _evaluate_file_delivery(answer_dir)
    s2, r2 = _evaluate_todo_completion(answer_dir)
    s3, r3 = _evaluate_functionality(answer_dir)
    s4, r4 = _evaluate_rag_quality(answer_dir)

    total = s1 + s2 + s3 + s4
    total = max(0, min(100, total))

    report = {
        "total_score": total,
        "section_scores": {
            "I. File Delivery": f"{s1}/15",
            "II. TODO Completion": f"{s2}/35",
            "III. Functional Correctness": f"{s3}/25",
            "IV. RAG Quality": f"{s4}/25",
        },
        "I. File Delivery & Basic Checks (15pts)": r1,
        "II. TODO Completion (35pts)": r2,
        "III. Functional Correctness (25pts)": r3,
        "IV. RAG Quality (25pts)": r4,
        "comment": "",
    }

    if total >= 90:
        report["comment"] = "Excellent! RAG system implementation is complete, all TODOs are filled in, and code quality is high."
    elif total >= 75:
        report["comment"] = "Good. Core functionality is implemented, but some dimensions have room for improvement."
    elif total >= 60:
        report["comment"] = "Passing. Task is basically completed, but there are notable deficiencies."
    elif total >= 40:
        report["comment"] = "Partially completed. Multiple key TODOs are not filled in or implementation quality is insufficient."
    else:
        report["comment"] = "Failing. Most TODOs are not completed, and the system cannot run properly."

    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print formatted scoring report"""
    print("=" * 70)
    print("RAG Intelligent Course Assistant System — Scoring Report")
    print("=" * 70)
    print(f"\nTotal Score: {score}/100")

    # Section scores overview
    scores = report.get("section_scores", {})
    if scores:
        print("\nSection Scores:")
        for k, v in scores.items():
            print(f"  {k}: {v}")

    for section_key in ["I. File Delivery & Basic Checks (15pts)",
                        "II. TODO Completion (35pts)",
                        "III. Functional Correctness (25pts)",
                        "IV. RAG Quality (25pts)"]:
        section = report.get(section_key, {})
        if not section:
            continue
        print(f"\n{'─' * 50}")
        print(f"[{section_key}] {section.get('score', '')}")
        print(f"{'─' * 50}")

        for k, v in section.get("details", {}).items():
            print(f"  {k}: {v}")

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
        os.path.dirname(__file__), "..", "gpt-5", "attempt_1")
    if os.path.exists(test_dir):
        print(f"Evaluating directory: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"Directory does not exist: {test_dir}")
    sys.exit(0)
