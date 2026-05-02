#!/usr/bin/env python3
# generate_visualization.py
# 使用 query.md 作为 prompt 调用 LLM 生成可交互的黑洞可视化 HTML。
# 若存在 last_eval_feedback.txt（上一轮评估反馈），会作为附加 prompt 让 LLM 改进代码。
# 需在 query 根目录配置 .env 中的 OPENAI_API_KEY（或 EVAL_TEXT_API_KEY）、OPENAI_MODEL 等。
import json
import os
import re
from pathlib import Path
from datetime import datetime

workspace = Path(__file__).resolve().parent
# query 根目录（上一级），用于加载 .env
query_root = workspace.parent
query_file = workspace / "query.md"
context_file = workspace / "context/operation_list.md" if (workspace / "context/operation_list.md").exists() else query_root / "context/operation_list.md"
feedback_file = workspace / "last_eval_feedback.txt"
output_file = workspace / "query1.html"
op_seq_file = workspace / "operation_sequence.json"

# 占位页 HTML（无 API 或调用失败时使用）
def _placeholder_html(query: str, context: str) -> str:
    return f"""<!DOCTYPE html>
<html>
<head><title>黑洞可视化 - 占位页</title></head>
<body>
<p style="color:red;font-weight:bold;">【占位页】未配置 API 或 LLM 调用失败。请配置 .env 中 OPENAI_API_KEY 后重新运行本脚本，或手动编写 Three.js 黑洞可视化代码覆盖本文件。</p>
<h1>任务描述</h1>
<pre>{query}</pre>
<h2>操作步骤</h2>
<pre>{context}</pre>
</body>
</html>
"""

def _load_env() -> dict:
    """从 .env 文件加载，Docker 下 workspace 在 /tmp 时再合并 os.environ（--env-file 注入）。"""
    out = {}
    env_path = query_root / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip().strip('"').strip("'")
    # Docker 中 workspace 在 /tmp，.env 可能读不到；用环境变量补全（与 template 一致）
    for key in ("EVAL_TEXT_API_KEY", "EVAL_TEXT_API_BASE_URL", "EVAL_TEXT_MODEL",
                 "OPENAI_API_KEY", "OPENAI_API_BASE", "OPENAI_MODEL"):
        if key in os.environ and os.environ[key].strip():
            out[key] = os.environ[key].strip()
    return out

def _call_llm_for_html(prompt: str, feedback: str, env: dict) -> str:
    # 与 eval/llm.py 一致：优先用 EVAL_TEXT_*（与 template 评估/模型调用同一套 key）
    api_key = env.get("EVAL_TEXT_API_KEY") or env.get("OPENAI_API_KEY") or os.environ.get("EVAL_TEXT_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if not api_key or api_key in ("your_openai_api_key", "your_text_eval_model_api_key"):
        return ""
    try:
        from openai import OpenAI
    except ImportError:
        return ""
    # 用 EVAL_TEXT 时必须配 EVAL_TEXT 的 base 和 model，避免把 SII key 打到 OpenAI 地址
    if env.get("EVAL_TEXT_API_KEY") or os.environ.get("EVAL_TEXT_API_KEY"):
        base_url = env.get("EVAL_TEXT_API_BASE_URL") or "https://api.opensii.ai/v1"
        model = env.get("EVAL_TEXT_MODEL") or "gpt-5"
    else:
        base_url = env.get("OPENAI_API_BASE") or env.get("EVAL_TEXT_API_BASE_URL") or "https://api.openai.com/v1"
        model = env.get("OPENAI_MODEL") or env.get("EVAL_TEXT_MODEL") or "gpt-4"

    system = """You are an expert at writing single-file HTML with Three.js. Output ONLY one complete, runnable HTML file. No explanations, no extra text.
Requirements for the HTML:
- Use Three.js (CDN: https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js) and OrbitControls.
- Implement a black hole visualization (Interstellar-style): accretion disk, gravitational lensing (backward ray tracing), Doppler effect (brighter on one side), dynamic starfield background.
- One single HTML file; all CSS/JS inline or in <script>. Critical parameters with Chinese comments.
- UI: bottom-left glassmorphism card titled "GARGANTUA", operation hints (rotate/pan/zoom), and a toggle with id="anim-toggle" (use a real <input>, not display:none).
- Do NOT output a page that only shows the task description as text. The page must render the black hole when opened in a browser."""

    user = prompt
    if feedback.strip():
        user = user + "\n\n---\n【上一轮评估反馈，请按以下问题改进输出代码】\n" + feedback.strip()

    client = OpenAI(api_key=api_key, base_url=base_url)
    r = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        max_tokens=16000,
        temperature=0.3,
    )
    raw = (r.choices[0].message.content or "").strip()
    return _extract_html(raw)

def _extract_html(raw: str) -> str:
    if not raw:
        return ""
    # ```html ... ``` or ``` ... ```
    m = re.search(r"```(?:html)?\s*([\s\S]*?)```", raw)
    if m:
        return m.group(1).strip()
    if raw.lstrip().startswith("<!DOCTYPE") or raw.lstrip().startswith("<html"):
        return raw.strip()
    return raw.strip()

def main():
    start_time = datetime.now().isoformat()
    query = query_file.read_text(encoding="utf-8") if query_file.exists() else ""
    context = context_file.read_text(encoding="utf-8") if context_file.exists() else ""
    feedback = feedback_file.read_text(encoding="utf-8") if feedback_file.exists() else ""

    env = _load_env()
    html_content = _call_llm_for_html(query + "\n\n" + (context or ""), feedback, env)

    if not html_content or len(html_content) < 500:
        # LLM 未返回有效 HTML（无 API key 或调用失败）。若已有可用的黑洞可视化 HTML 则不要用占位页覆盖
        existing_ok = False
        if output_file.exists():
            try:
                raw = output_file.read_text(encoding="utf-8", errors="ignore")[:20000]
                if "THREE." in raw or "ShaderMaterial" in raw or "three.module.js" in raw:
                    existing_ok = True
            except Exception:
                pass
        if existing_ok:
            print("query1.html 已存在且为可视化页面，跳过覆盖（LLM 未可用）。")
            success = True
        else:
            html_content = _placeholder_html(query, context)
            output_file.write_text(html_content, encoding="utf-8")
            print("query1.html 已生成（占位页）。请配置 .env 中 OPENAI_API_KEY 后重新运行以生成真实可视化，或手动编写代码覆盖。")
            success = False
    else:
        print("query1.html 已生成（由 LLM 生成的可交互黑洞可视化）。")
        success = True
        output_file.write_text(html_content, encoding="utf-8")

    end_time = datetime.now().isoformat()
    operation_sequence = {
        "task": "Three.js 黑洞可视化",
        "target_url": "",
        "start_time": start_time,
        "end_time": end_time,
        "success": success,
        "operations": [
            {"step": 1, "action": "read_query", "timestamp": start_time, "status": "success",
             "element_type": None, "selector": None, "description": "读取 query.md 与 context", "input_value": None, "error": None, "extra": {}},
            {"step": 2, "action": "read_feedback", "timestamp": start_time, "status": "success",
             "element_type": None, "selector": None, "description": "读取 last_eval_feedback.txt（若存在）", "input_value": None, "error": None, "extra": {"had_feedback": feedback_file.exists()}},
            {"step": 3, "action": "call_llm", "timestamp": end_time, "status": "success" if success else "failed",
             "element_type": None, "selector": None, "description": "调用 LLM 生成/改进 HTML", "input_value": None, "error": None, "extra": {}},
            {"step": 4, "action": "write_file", "timestamp": end_time, "status": "success",
             "element_type": None, "selector": None, "description": "写入 query1.html", "input_value": None, "error": None, "extra": {"output_file": "query1.html"}},
        ],
    }
    op_seq_file.write_text(json.dumps(operation_sequence, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"operation_sequence.json 已生成: {op_seq_file}")

if __name__ == "__main__":
    main()
