"""
立直麻将晋级条件计算器 — 评分脚本
总分: 100 分

维度分配:
  一、文件交付 (15分)
      1. Java 源代码存在        5 分
      2. 可执行 JAR 文件存在    5 分
      3. README 文档存在        5 分

  二、编译与可运行性 (15分)
      1. Java 源码可编译        5 分
      2. JAR 能启动             5 分
      3. 给定输入后产生含义正确的输出  5 分

  三、功能正确性 — 4 组测试集 (55分)
      每组 13.75 分:
        - 晋级条件 (自摸/荣和/放铳/被自摸)  5.5 分
        - 危险区间                          5.5 分
        - 听牌分支 (16 种流局情况)           2.75 分

  四、README 质量 (15分)
      1. 编译和运行指南   5 分
      2. 输入格式说明     5 分
      3. 输出格式与示例   5 分
"""

import os
import re
import json
import subprocess
from typing import Tuple, Dict, Any, List, Optional

try:
    import openai
except ImportError:
    openai = None


# =====================================================================
# 环境 / LLM 工具
# =====================================================================

def _load_env(answer_dir: str) -> dict:
    values: dict = {}
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
                    k = k.strip()
                    if k not in values:
                        values[k] = v.strip().strip("'\"")
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


def _extract_json(text: str) -> Optional[dict]:
    if "```json" in text:
        text = text.split("```json", 1)[1].split("```", 1)[0].strip()
    elif "```" in text:
        text = text.split("```", 1)[1].split("```", 1)[0].strip()
    try:
        return json.loads(text)
    except (json.JSONDecodeError, ValueError):
        return None


# =====================================================================
# 文件查找工具
# =====================================================================

def _find_files_by_ext(directory: str, ext: str) -> List[str]:
    result = []
    for root, _dirs, files in os.walk(directory):
        for f in files:
            if f.endswith(ext):
                result.append(os.path.join(root, f))
    return result


def _find_readme(directory: str) -> Optional[str]:
    for name in ("README.md", "readme.md", "Readme.md", "README.txt", "README"):
        p = os.path.join(directory, name)
        if os.path.exists(p):
            return p
    for root, _dirs, files in os.walk(directory):
        for f in files:
            if f.lower().startswith("readme"):
                return os.path.join(root, f)
    return None


def _run_jar(jar_path: str, stdin_text: str, timeout: int = 60) -> Tuple[bool, str, str]:
    try:
        proc = subprocess.run(
            ["java", "-jar", jar_path],
            input=stdin_text,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=os.path.dirname(jar_path) or ".",
        )
        return True, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired:
        return False, "", "timeout"
    except FileNotFoundError:
        return False, "", "java_not_found"
    except Exception as e:
        return False, "", str(e)


# =====================================================================
# 测试用例加载
# =====================================================================

def _load_test_cases() -> List[Dict[str, str]]:
    md_path = os.path.join(os.path.dirname(__file__), "test_answers.md")
    if not os.path.exists(md_path):
        return []
    try:
        with open(md_path, "r", encoding="utf-8") as fh:
            content = fh.read()
    except Exception:
        return []

    cases: List[Dict[str, str]] = []
    # Split by "# 测试集N" headers
    parts = re.split(r"#\s*测试集\d+[^\n]*\n", content)
    for part in parts[1:]:
        # Input: always a short indented block
        inp_match = re.search(r"##\s*输入[：:]\s*\n((?:    [^\n]*\n)+)", part)
        if not inp_match:
            inp_match = re.search(r"##\s*输入[：:]\s*\n(.+?)(?=##\s*输出)", part, re.DOTALL)
        # Output: everything after "## 输出:" until the next "# " top-level header or EOF
        # Use DOTALL to capture multi-paragraph output including blank lines
        out_match = re.search(r"##\s*输出[：:]\s*\n(.+?)(?=\n#\s测试集|$)", part, re.DOTALL)

        if inp_match and out_match:
            def deindent(t: str) -> str:
                lines = []
                for ln in t.split("\n"):
                    if ln.startswith("    "):
                        lines.append(ln[4:])
                    elif ln.strip():
                        lines.append(ln)
                    else:
                        lines.append("")  # preserve blank lines
                # strip leading/trailing blank lines
                while lines and not lines[0].strip():
                    lines.pop(0)
                while lines and not lines[-1].strip():
                    lines.pop()
                return "\n".join(lines)

            cases.append({
                "input": deindent(inp_match.group(1)),
                "expected": deindent(out_match.group(1)),
            })
    return cases


# =====================================================================
# 一、文件交付 (15 分)
# =====================================================================

def _score_file_delivery(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    info: dict = {}

    java_files = _find_files_by_ext(answer_dir, ".java")
    if java_files:
        score += 5
        info["java_src"] = f"5/5 — {len(java_files)} .java file(s)"
    else:
        info["java_src"] = "0/5 — no .java files"

    jar_files = _find_files_by_ext(answer_dir, ".jar")
    if jar_files:
        score += 5
        info["jar_file"] = f"5/5 — {os.path.basename(jar_files[0])}"
    else:
        info["jar_file"] = "0/5 — no .jar file"

    readme = _find_readme(answer_dir)
    if readme:
        score += 5
        info["readme"] = f"5/5 — {os.path.basename(readme)}"
    else:
        info["readme"] = "0/5 — no README"

    return score, info


# =====================================================================
# 二、编译与可运行性 (15 分)
# =====================================================================

def _score_compilation(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    info: dict = {}

    # 2.1 源码编译 (5 分)
    java_files = _find_files_by_ext(answer_dir, ".java")
    if java_files:
        try:
            proc = subprocess.run(
                ["javac"] + java_files,
                capture_output=True, text=True, timeout=120, cwd=answer_dir,
            )
            if proc.returncode == 0:
                score += 5
                info["compile"] = "5/5 — compilation succeeded"
            else:
                score += 2
                info["compile"] = f"2/5 — compilation failed: {proc.stderr[:150]}"
        except FileNotFoundError:
            score += 3
            info["compile"] = "3/5 — javac unavailable; Java source exists (baseline credit)"
        except subprocess.TimeoutExpired:
            score += 2
            info["compile"] = "2/5 — compilation timed out"
        except Exception as e:
            score += 1
            info["compile"] = f"1/5 — error: {str(e)[:100]}"
    else:
        info["compile"] = "0/5 — no Java source"

    # 2.2 JAR 可启动 (5 分)
    jar_files = _find_files_by_ext(answer_dir, ".jar")
    jar_path = jar_files[0] if jar_files else None

    if jar_path:
        ok, _out, err = _run_jar(jar_path, "", timeout=10)
        if ok:
            score += 5
            info["jar_run"] = "5/5 — JAR executable"
        elif err == "java_not_found":
            score += 3
            info["jar_run"] = "3/5 — java not available; JAR exists (baseline credit)"
        else:
            score += 1
            info["jar_run"] = f"1/5 — JAR run failed: {err[:100]}"
    else:
        info["jar_run"] = "0/5 — no JAR"

    # 2.3 给定输入产生含义正确输出 (5 分)
    if jar_path:
        sample_input = (
            "当前亲家：北\n"
            "座次： 东 南 西 北\n"
            "名字： A B C D\n"
            "开始前总分 0.0 0.0 0.0 0.0\n"
            "当前分数 30000 25000 25000 20000\n"
            "晋级条件：2\n"
            "规则：M-league\n"
            "供托：0\n"
            "本场：0\n"
        )
        ok, stdout, err = _run_jar(jar_path, sample_input, timeout=30)
        if ok and stdout.strip():
            keywords = ["晋级", "自摸", "荣和", "危険", "危险", "听牌", "放铳"]
            hit = sum(1 for kw in keywords if kw in stdout)
            if hit >= 3:
                score += 5
                info["io_test"] = f"5/5 — output contains {hit} mahjong keywords"
            elif hit >= 1:
                score += 3
                info["io_test"] = f"3/5 — output contains {hit} mahjong keyword(s), partial"
            else:
                score += 1
                info["io_test"] = "1/5 — output exists but no mahjong terminology detected"
        elif ok:
            score += 1
            info["io_test"] = "1/5 — ran but produced no output"
        elif err == "java_not_found":
            score += 2
            info["io_test"] = "2/5 — java unavailable, cannot test I/O"
        else:
            info["io_test"] = f"0/5 — run failed: {err[:100]}"
    else:
        info["io_test"] = "0/5 — no JAR"

    return score, info


# =====================================================================
# 三、功能正确性 (55 分)
# =====================================================================

_COMPARE_PROMPT_TEMPLATE = """\
你是立直麻将晋级条件计算器的评测专家。请仔细比较程序输出与标准答案。

## 标准答案
```
{expected}
```

## 程序输出
```
{actual}
```

请从三个维度打分 (整数 0-100)：

1. **promotion_score** — 晋级条件正确性:
   检查每位选手的自摸/荣和/放铳/被自摸条件。
   100=全部数值完全正确, 75=大部分正确少量偏差, 50=约半数正确,
   25=少数正确, 0=完全不正确或缺失

2. **danger_score** — 危险区间正确性:
   检查每位选手的横移动危险区间。
   100=全部正确, 75=大部分正确, 50=约半数, 25=少数, 0=完全不正确

3. **tenpai_score** — 听牌分支正确性 (16 种流局情况):
   100=16 种全对, 75=12+ 正确, 50=8+ 正确, 25=4+ 正确, 0=完全不正确

注意:
- 格式差异 (空格/tab/全角半角) 可忽略
- "・" 与 "·" 等价
- 选手名大小写差异可忽略
- 关注数值语义而非排版

请严格按 JSON 格式回复 (不含其他内容):
```json
{{
  "promotion_score": 0,
  "promotion_reason": "",
  "danger_score": 0,
  "danger_reason": "",
  "tenpai_score": 0,
  "tenpai_reason": ""
}}
```"""


def _keyword_match_ratio(actual: str, expected: str) -> float:
    """归一化关键词匹配率 (降级评估)."""
    def norm(t: str) -> str:
        t = t.replace("\t", " ").replace("・", "·").replace("　", " ")
        return re.sub(r" +", " ", t).strip()

    expected_lines = [
        norm(ln) for ln in expected.split("\n")
        if ln.strip() and "===" not in ln
    ]
    if not expected_lines:
        return 0.0

    actual_clean = re.sub(r"[^\w\u4e00-\u9fa5]", "", norm(actual))
    matches = 0
    for line in expected_lines:
        core = re.sub(r"[^\w\u4e00-\u9fa5]", "", line)
        if core and core in actual_clean:
            matches += 1
    return matches / len(expected_lines)


def _eval_one_test(
    jar_path: str,
    test_input: str,
    expected_output: str,
    llm_cfg: dict,
) -> Tuple[float, dict]:
    """评估单组测试 (满分 13.75)."""
    info: dict = {}

    ok, stdout, err = _run_jar(jar_path, test_input, timeout=60)
    if not ok:
        info["status"] = f"run failed: {err[:120]}"
        return 0.0, info
    if not stdout.strip():
        info["status"] = "no output"
        return 0.0, info

    info["status"] = "ok"

    # 尝试 LLM 评估
    prompt = _COMPARE_PROMPT_TEMPLATE.format(
        expected=expected_output,
        actual=stdout[:5000],
    )
    llm_text = _call_llm_judge(prompt, llm_cfg)
    parsed = _extract_json(llm_text) if llm_text else None

    if parsed and all(k in parsed for k in ("promotion_score", "danger_score", "tenpai_score")):
        promo = max(0, min(100, int(parsed["promotion_score"])))
        danger = max(0, min(100, int(parsed["danger_score"])))
        tenpai = max(0, min(100, int(parsed["tenpai_score"])))

        promo_pts = round(5.5 * promo / 100, 2)
        danger_pts = round(5.5 * danger / 100, 2)
        tenpai_pts = round(2.75 * tenpai / 100, 2)
        total = promo_pts + danger_pts + tenpai_pts

        info["promotion"] = f"{promo_pts}/5.5 ({promo}%) {parsed.get('promotion_reason', '')[:80]}"
        info["danger"] = f"{danger_pts}/5.5 ({danger}%) {parsed.get('danger_reason', '')[:80]}"
        info["tenpai"] = f"{tenpai_pts}/2.75 ({tenpai}%) {parsed.get('tenpai_reason', '')[:80]}"
        return round(total, 2), info

    # 降级: 关键词匹配
    ratio = _keyword_match_ratio(stdout, expected_output)
    fallback = round(13.75 * ratio, 2)
    info["fallback"] = f"{fallback}/13.75 — keyword match {ratio:.0%}"
    return fallback, info


def _score_functionality(answer_dir: str) -> Tuple[int, dict]:
    jar_files = _find_files_by_ext(answer_dir, ".jar")
    if not jar_files:
        return 0, {"error": "no JAR file, skipping functional tests"}

    jar_path = jar_files[0]
    test_cases = _load_test_cases()
    if not test_cases:
        return 0, {"error": "could not load test cases from test_answers.md"}

    llm_cfg = _get_text_eval_config(answer_dir)
    total = 0.0
    details: dict = {}

    for idx, tc in enumerate(test_cases, 1):
        pts, d = _eval_one_test(jar_path, tc["input"], tc["expected"], llm_cfg)
        total += pts
        details[f"test_{idx}"] = {"score": f"{pts}/13.75", **d}

    return int(round(total)), details


# =====================================================================
# 四、README 质量 (15 分)
# =====================================================================

_README_PROMPT = """\
你是软件文档评审专家。这是一个 Java 立直麻将晋级条件计算器的 README。
请从以下三个维度打分 (整数 0-100):

1. **compile_guide** — 编译和运行指南: 是否包含清晰的 javac/maven/gradle 编译步骤与 java -jar 运行命令?
2. **input_format** — 输入格式说明: 是否说明了选手 id、积分、点数、规则、本场、供托等输入字段?
3. **output_example** — 输出格式与使用示例: 是否包含输出格式说明和使用示例?

README 内容:
```
{content}
```

严格按 JSON 格式回复:
```json
{{
  "compile_guide": {{"score": 0, "reason": ""}},
  "input_format": {{"score": 0, "reason": ""}},
  "output_example": {{"score": 0, "reason": ""}}
}}
```"""


def _readme_keyword_fallback(content: str) -> int:
    """README 降级评分 (最高 12)."""
    pts = 0
    lc = content.lower()
    # 编译 / 运行
    if any(k in lc for k in ("javac", "maven", "gradle", "编译", "compile", "build")):
        pts += 2
    if any(k in lc for k in ("java -jar", "运行", "run", "执行")):
        pts += 2
    # 输入格式
    if any(k in content for k in ("输入", "input", "座次", "积分", "点数", "规则")):
        pts += 3
    # 输出格式
    if any(k in content for k in ("输出", "output", "晋级", "危险区间", "听牌")):
        pts += 2
    # 示例
    if any(k in content for k in ("示例", "example", "样例")):
        pts += 2
    return min(pts, 12)


def _score_readme(answer_dir: str) -> Tuple[int, dict]:
    readme = _find_readme(answer_dir)
    if not readme:
        return 0, {"error": "no README found"}

    try:
        with open(readme, "r", encoding="utf-8") as fh:
            content = fh.read()
    except Exception as e:
        return 0, {"error": f"read failed: {e}"}

    if len(content.strip()) < 30:
        return 1, {"note": "README too short (<30 chars)"}

    llm_cfg = _get_text_eval_config(answer_dir)
    llm_text = _call_llm_judge(
        _README_PROMPT.format(content=content[:3000]),
        llm_cfg,
    )
    parsed = _extract_json(llm_text) if llm_text else None

    if parsed:
        try:
            c = max(0, min(100, int(parsed.get("compile_guide", {}).get("score", 0))))
            i = max(0, min(100, int(parsed.get("input_format", {}).get("score", 0))))
            o = max(0, min(100, int(parsed.get("output_example", {}).get("score", 0))))

            c_pts = int(5 * c / 100)
            i_pts = int(5 * i / 100)
            o_pts = int(5 * o / 100)
            total = c_pts + i_pts + o_pts

            return total, {
                "compile_guide": f"{c_pts}/5 ({c}%) {parsed.get('compile_guide', {}).get('reason', '')[:80]}",
                "input_format": f"{i_pts}/5 ({i}%) {parsed.get('input_format', {}).get('reason', '')[:80]}",
                "output_example": f"{o_pts}/5 ({o}%) {parsed.get('output_example', {}).get('reason', '')[:80]}",
            }
        except (TypeError, ValueError):
            pass

    pts = _readme_keyword_fallback(content)
    return pts, {"fallback": f"{pts}/15 — keyword-based (LLM unavailable)"}


# =====================================================================
# 主入口
# =====================================================================

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    评估 agent 的输出。

    Args:
        answer_dir: agent 输出目录的绝对路径

    Returns:
        (score, report)
        - score: 0-100 整数
        - report: dict 详细评估报告
    """
    s1, d1 = _score_file_delivery(answer_dir)
    s2, d2 = _score_compilation(answer_dir)
    s3, d3 = _score_functionality(answer_dir)
    s4, d4 = _score_readme(answer_dir)

    total = max(0, min(100, s1 + s2 + s3 + s4))

    if total >= 90:
        comment = "优秀！代码完整、功能正确、文档齐全。"
    elif total >= 75:
        comment = "良好。基本完成任务，核心功能实现正确。"
    elif total >= 60:
        comment = "及格。有基本实现，但部分测试未通过。"
    elif total >= 40:
        comment = "部分完成。功能不完整或测试未通过。"
    else:
        comment = "不及格。任务完成度不足。"

    report: Dict[str, Any] = {
        "总分": total,
        "分项得分": {
            "文件交付": f"{s1}/15",
            "编译与运行": f"{s2}/15",
            "功能正确性": f"{s3}/55",
            "README质量": f"{s4}/15",
        },
        "详情": {
            "一、文件交付 (15分)": {"得分": f"{s1}/15", **d1},
            "二、编译与运行 (15分)": {"得分": f"{s2}/15", **d2},
            "三、功能正确性 (55分)": {"得分": f"{s3}/55", **d3},
            "四、README质量 (15分)": {"得分": f"{s4}/15", **d4},
        },
        "评语": comment,
    }
    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """打印格式化的评分报告"""
    print("=" * 70)
    print("评分报告：立直麻将晋级条件计算器")
    print("=" * 70)
    print(f"\n总分：{score}/100\n")

    item_scores = report.get("分项得分", {})
    if item_scores:
        print("分项得分:")
        for k, v in item_scores.items():
            print(f"  {k}: {v}")

    for section_name, section_data in report.get("详情", {}).items():
        print(f"\n{'─' * 55}")
        print(f"【{section_name}】")
        print(f"{'─' * 55}")
        if isinstance(section_data, dict):
            for k, v in section_data.items():
                if isinstance(v, dict):
                    print(f"  {k}:")
                    for kk, vv in v.items():
                        print(f"    {kk}: {vv}")
                else:
                    print(f"  {k}: {v}")
        else:
            print(f"  {section_data}")

    print(f"\n{'=' * 55}")
    print(f"评语：{report.get('评语', '')}")
    print("=" * 70)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = os.path.join(os.path.dirname(__file__), "..", "gpt-5", "attempt_1")

    if not os.path.isabs(target):
        target = os.path.join(os.path.dirname(__file__), "..", target)

    if os.path.exists(target):
        print(f"评估目录: {target}\n")
        s, r = evaluate(target)
        print_report(s, r)
    else:
        print(f"目录不存在: {target}")
    sys.exit(0)
