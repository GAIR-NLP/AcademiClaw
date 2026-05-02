"""
Rubric for solve_puzzle_zeyuli_query3: 基于约束的解谜推理

总分 100 分，分配如下:

  一、文件交付与结构 (10分)
      - solution.json 存在且为合法 JSON 对象 (5)
      - reasoning.md 存在且非空 (5)

  二、犯罪事实正确性 (20分)
      - murderer / weapon / location / time / motive 各 4 分
      - 精确匹配参考答案

  三、角色分配正确性 (15分)
      - 12 名嫌疑人各自的角色 (murderer/accomplice/liar/truth_teller/innocent)
      - 按正确比例给分

  四、真值表正确性 (15分)
      - 12 名嫌疑人 × 6 条陈述 = 72 项 bool
      - 按平均准确率给分

  五、推理合理性 (40分)
      - LLM-as-Judge 评估 reasoning.md
      - fallback: 基于长度与关键词的启发式 (上限 20)

参考数据来源: context/Q3/ultimate_chinese_puzzles.json -> hidden_data
"""

import json
import os
import sys
from typing import Any, Dict, List, Tuple

try:
    import openai
except ImportError:
    openai = None

# ─────────────────────────────────────────────────────────────────────────────
# 常量
# ─────────────────────────────────────────────────────────────────────────────

CRIME_FACT_KEYS = ["murderer", "weapon", "location", "time", "motive"]
VALID_ROLES = {"murderer", "accomplice", "liar", "truth_teller", "innocent"}
SOURCE_JSON_REL = os.path.join("context", "Q3", "ultimate_chinese_puzzles.json")

# ─────────────────────────────────────────────────────────────────────────────
# 工具: 环境 / LLM / IO
# ─────────────────────────────────────────────────────────────────────────────


def _load_env(answer_dir: str) -> dict:
    """从 answer_dir 和 query 根目录加载 .env"""
    values: Dict[str, str] = {}
    rubric_dir = os.path.dirname(os.path.abspath(__file__))
    query_root = os.path.dirname(rubric_dir)
    for env_dir in [answer_dir, query_root]:
        env_path = os.path.join(env_dir, ".env")
        if os.path.exists(env_path):
            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
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
        print(f"[RUBRIC] LLM Judge 调用失败: {e}")
        return ""


def _read_text(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


def _load_json(path: str) -> Any:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


# ─────────────────────────────────────────────────────────────────────────────
# 加载参考答案
# ─────────────────────────────────────────────────────────────────────────────


def _find_reference_puzzle(answer_dir: str, puzzle_id: int) -> dict:
    """在多个候选路径中找到对应 puzzle_id 的源谜题，返回其 dict (含 hidden_data)。"""
    rubric_dir = os.path.dirname(os.path.abspath(__file__))
    query_root = os.path.dirname(rubric_dir)
    candidates = [
        os.path.join(answer_dir, SOURCE_JSON_REL),
        os.path.join(query_root, SOURCE_JSON_REL),
    ]
    for path in candidates:
        data = _load_json(path)
        if not isinstance(data, list) or not data:
            continue
        for p in data:
            if isinstance(p, dict) and p.get("id") == puzzle_id:
                return p
        # 如果没找到精确 id，返回第一个
        return data[0]
    return {}


# ─────────────────────────────────────────────────────────────────────────────
# 一、文件交付与结构 (10 分)
# ─────────────────────────────────────────────────────────────────────────────


def _score_deliverables(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    details: Dict[str, str] = {}

    # solution.json (5 分)
    sol_path = os.path.join(answer_dir, "solution.json")
    if os.path.isfile(sol_path):
        sol = _load_json(sol_path)
        if isinstance(sol, dict) and sol:
            has_cf = isinstance(sol.get("crime_facts"), dict)
            has_roles = isinstance(sol.get("roles"), dict)
            has_tv = isinstance(sol.get("truth_values"), dict)
            if has_cf and has_roles and has_tv:
                score += 5
                details["solution.json"] = "5/5 — 存在且包含 crime_facts / roles / truth_values"
            elif has_cf or has_roles or has_tv:
                score += 3
                details["solution.json"] = "3/5 — 存在但缺少部分必要字段"
            else:
                score += 1
                details["solution.json"] = "1/5 — 存在但缺少全部核心字段"
        else:
            score += 1
            details["solution.json"] = "1/5 — 文件存在但非有效 JSON 对象"
    else:
        details["solution.json"] = "0/5 — 文件不存在"

    # reasoning.md (5 分)
    reas_path = os.path.join(answer_dir, "reasoning.md")
    if os.path.isfile(reas_path):
        content = _read_text(reas_path).strip()
        if len(content) >= 500:
            score += 5
            details["reasoning.md"] = "5/5 — 存在且内容充实"
        elif len(content) >= 100:
            score += 3
            details["reasoning.md"] = "3/5 — 存在但内容偏短"
        elif content:
            score += 1
            details["reasoning.md"] = "1/5 — 存在但内容过短"
        else:
            details["reasoning.md"] = "0/5 — 文件存在但为空"
    else:
        details["reasoning.md"] = "0/5 — 文件不存在"

    return score, details


# ─────────────────────────────────────────────────────────────────────────────
# 二、犯罪事实正确性 (20 分, 每项 4 分)
# ─────────────────────────────────────────────────────────────────────────────


def _normalize(s: str) -> str:
    """去除首尾空白和引号，统一为小写比较。"""
    return str(s).strip().strip("'\"").lower()


def _score_crime_facts(sol_cf: dict, ref_cf: dict) -> Tuple[int, dict]:
    score = 0
    details: Dict[str, Any] = {}
    for key in CRIME_FACT_KEYS:
        expected = ref_cf.get(key, "")
        actual = sol_cf.get(key, "")
        match = _normalize(actual) == _normalize(expected)
        pts = 4 if match else 0
        score += pts
        details[key] = {
            "expected": expected,
            "actual": actual,
            "match": match,
            "score": f"{pts}/4",
        }
    return score, details


# ─────────────────────────────────────────────────────────────────────────────
# 三、角色分配正确性 (15 分)
# ─────────────────────────────────────────────────────────────────────────────


def _score_roles(sol_roles: dict, ref_roles: dict) -> Tuple[int, dict]:
    if not ref_roles:
        return 0, {"error": "无参考角色数据"}

    total = len(ref_roles)
    correct = 0
    mismatches: List[dict] = []
    for person, expected_role in ref_roles.items():
        actual_role = sol_roles.get(person, "")
        if _normalize(actual_role) == _normalize(expected_role):
            correct += 1
        else:
            mismatches.append({
                "person": person,
                "expected": expected_role,
                "actual": actual_role or "(missing)",
            })

    ratio = correct / total if total > 0 else 0
    score = int(15 * ratio)
    details = {
        "correct": correct,
        "total": total,
        "accuracy": f"{ratio:.2%}",
        "score": f"{score}/15",
        "mismatches": mismatches[:10],  # 最多展示 10 条
    }
    return score, details


# ─────────────────────────────────────────────────────────────────────────────
# 四、真值表正确性 (15 分)
# ─────────────────────────────────────────────────────────────────────────────


def _score_truth_values(sol_tv: dict, ref_tv: dict) -> Tuple[int, dict]:
    if not ref_tv:
        return 0, {"error": "无参考真值数据"}

    total_items = 0
    total_correct = 0
    per_person: Dict[str, Any] = {}

    for person, ref_vals in ref_tv.items():
        n = len(ref_vals)
        total_items += n
        sol_vals = sol_tv.get(person)

        if not isinstance(sol_vals, list) or len(sol_vals) != n:
            per_person[person] = {
                "expected_len": n,
                "actual_len": len(sol_vals) if isinstance(sol_vals, list) else None,
                "correct": 0,
                "note": "长度不匹配或类型错误",
            }
            continue

        correct = sum(
            1
            for i in range(n)
            if isinstance(sol_vals[i], bool) and sol_vals[i] == ref_vals[i]
        )
        total_correct += correct
        per_person[person] = {
            "correct": correct,
            "total": n,
        }

    rate = total_correct / total_items if total_items > 0 else 0
    score = int(15 * rate)
    details = {
        "overall_accuracy": f"{rate:.2%}",
        "total_correct": total_correct,
        "total_items": total_items,
        "score": f"{score}/15",
        "per_person": per_person,
    }
    return score, details


# ─────────────────────────────────────────────────────────────────────────────
# 五、推理合理性 (40 分)
# ─────────────────────────────────────────────────────────────────────────────

_REASONING_JUDGE_PROMPT = """\
你是一位严格的逻辑推理评审专家。以下是一个解谜任务的推理过程文档（reasoning.md）。

任务背景：
给定 12 名武侠角色嫌疑人，每人有 6 条陈述。结合全局约束条件，需要推导出：
1. 犯罪事实（凶手、凶器、地点、时间、动机）
2. 各嫌疑人角色（murderer / accomplice / liar / truth_teller / innocent）
3. 每条陈述的真伪（truth_values）

请从以下 4 个维度评估推理质量（总分 40 分），严格按 JSON 格式返回：

1. **结构完整性** (0-10分)
   - 9-10: 包含明确的问题分析、假设建立、逐步验证、排除过程、最终结论
   - 6-8: 大部分步骤齐全，但某些环节粗略
   - 3-5: 仅有结论或简单罗列，缺乏推理链
   - 0-2: 几乎没有推理过程

2. **逻辑严密性** (0-12分)
   - 10-12: 每一步结论都有充分依据，无逻辑跳跃，推理链完整
   - 7-9: 整体逻辑合理，有少量跳跃但不影响结论
   - 4-6: 逻辑链有明显断裂或自相矛盾
   - 0-3: 基本无逻辑推理，直接给出答案

3. **约束利用** (0-10分)
   - 8-10: 明确引用并利用了多个全局约束来缩小推理空间，形成有效的排除链
   - 5-7: 提到了一些约束但未充分利用
   - 2-4: 很少引用约束
   - 0-1: 完全忽略约束

4. **表述清晰度** (0-8分)
   - 7-8: 条理清晰、易于跟踪推理过程、结论与推理步骤一致
   - 5-6: 基本清晰但部分内容冗余或混乱
   - 2-4: 难以理解推理过程
   - 0-1: 无法理解

请严格按以下 JSON 格式回复，不要包含其他内容：
```json
{{
  "structure": {{"score": 0, "reason": ""}},
  "logic": {{"score": 0, "reason": ""}},
  "constraints": {{"score": 0, "reason": ""}},
  "clarity": {{"score": 0, "reason": ""}},
  "total": 0,
  "overall_comment": ""
}}
```

--- 推理文档内容开始 ---
{reasoning_content}
--- 推理文档内容结束 ---
"""


def _score_reasoning(answer_dir: str) -> Tuple[int, dict]:
    reas_path = os.path.join(answer_dir, "reasoning.md")
    content = _read_text(reas_path).strip()
    if not content:
        return 0, {"error": "reasoning.md 不存在或为空", "score": "0/40"}

    config = _get_text_eval_config(answer_dir)

    # 截断至 12000 字符，防止 token 超限
    max_chars = 12000
    truncated = content[:max_chars]
    if len(content) > max_chars:
        truncated += "\n... (内容已截断)"

    prompt = _REASONING_JUDGE_PROMPT.format(reasoning_content=truncated)
    raw = _call_llm_judge(prompt, config)

    if raw:
        try:
            text = raw
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            result = json.loads(text)

            structure = max(0, min(10, int(result.get("structure", {}).get("score", 0))))
            logic = max(0, min(12, int(result.get("logic", {}).get("score", 0))))
            constraints = max(0, min(10, int(result.get("constraints", {}).get("score", 0))))
            clarity = max(0, min(8, int(result.get("clarity", {}).get("score", 0))))
            score = structure + logic + constraints + clarity

            details = {
                "structure": f"{structure}/10 — {result.get('structure', {}).get('reason', '')}",
                "logic": f"{logic}/12 — {result.get('logic', {}).get('reason', '')}",
                "constraints": f"{constraints}/10 — {result.get('constraints', {}).get('reason', '')}",
                "clarity": f"{clarity}/8 — {result.get('clarity', {}).get('reason', '')}",
                "score": f"{score}/40",
                "overall_comment": result.get("overall_comment", ""),
                "method": "LLM-as-Judge",
            }
            return score, details
        except (json.JSONDecodeError, ValueError, TypeError) as e:
            print(f"[RUBRIC] LLM 返回解析失败: {e}")
            print(f"[RUBRIC] raw: {raw[:300]}")

    # Fallback: 启发式评分 (上限 20/40)
    return _reasoning_fallback(content)


def _reasoning_fallback(content: str) -> Tuple[int, dict]:
    length = len(content)
    score = 0

    # 长度分 (0-8)
    if length >= 5000:
        score += 8
    elif length >= 3000:
        score += 6
    elif length >= 1500:
        score += 4
    elif length >= 500:
        score += 2
    elif length >= 100:
        score += 1

    # 结构性关键词 (0-12)
    keywords = [
        ("假设", 1), ("验证", 1), ("排除", 1), ("结论", 1),
        ("约束", 2), ("陈述", 1), ("凶手", 1), ("真伪", 1),
        ("矛盾", 1), ("推理", 1), ("角色", 1),
    ]
    kw_score = 0
    found_kw = []
    for kw, pts in keywords:
        if kw in content:
            kw_score += pts
            found_kw.append(kw)
    score += min(12, kw_score)

    score = min(20, score)
    details = {
        "method": "fallback (LLM 不可用)",
        "length": length,
        "keywords_found": found_kw,
        "score": f"{score}/40 (上限20)",
        "note": "LLM 评估不可用，使用保守启发式评分",
    }
    return score, details


# ─────────────────────────────────────────────────────────────────────────────
# 主入口: evaluate / print_report
# ─────────────────────────────────────────────────────────────────────────────


def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    评估 agent 的输出。

    Args:
        answer_dir: agent 输出目录的绝对路径

    Returns:
        (score, report) — score 为 0-100 整数, report 为详细报告 dict
    """
    report: Dict[str, Any] = {}

    # 一、文件交付 (10 分)
    s1, d1 = _score_deliverables(answer_dir)
    report["一、文件交付与结构 (10分)"] = d1

    # 尝试加载 solution.json
    sol = _load_json(os.path.join(answer_dir, "solution.json"))
    if not isinstance(sol, dict) or not sol:
        # 无法解析，后续正确性全部 0 分，仍评估推理
        s2, s3, s4 = 0, 0, 0
        d_err = {"error": "solution.json 无法解析，正确性维度无法评估"}
        report["二、犯罪事实正确性 (20分)"] = d_err
        report["三、角色分配正确性 (15分)"] = d_err
        report["四、真值表正确性 (15分)"] = d_err
        s5, d5 = _score_reasoning(answer_dir)
        report["五、推理合理性 (40分)"] = d5
        total = min(100, s1 + s5)
        report["分项得分"] = {
            "文件交付": f"{s1}/10",
            "犯罪事实": "0/20",
            "角色分配": "0/15",
            "真值表": "0/15",
            "推理合理性": f"{s5}/40",
        }
        report["总分"] = total
        return total, report

    # 确定 puzzle_id 并加载参考数据
    puzzle_id = sol.get("puzzle_id", 1)
    if not isinstance(puzzle_id, int):
        try:
            puzzle_id = int(puzzle_id)
        except (ValueError, TypeError):
            puzzle_id = 1

    src = _find_reference_puzzle(answer_dir, puzzle_id)
    hidden = src.get("hidden_data", {})

    if not hidden:
        s2, s3, s4 = 0, 0, 0
        d_err = {"error": "无法加载参考数据 (hidden_data)，正确性无法评估"}
        report["二、犯罪事实正确性 (20分)"] = d_err
        report["三、角色分配正确性 (15分)"] = d_err
        report["四、真值表正确性 (15分)"] = d_err
    else:
        ref_cf = hidden.get("crime_facts", {})
        ref_roles = hidden.get("roles", {})
        ref_tv = hidden.get("truth_values", {})

        s2, d2 = _score_crime_facts(sol.get("crime_facts", {}), ref_cf)
        report["二、犯罪事实正确性 (20分)"] = d2

        s3, d3 = _score_roles(sol.get("roles", {}), ref_roles)
        report["三、角色分配正确性 (15分)"] = d3

        s4, d4 = _score_truth_values(sol.get("truth_values", {}), ref_tv)
        report["四、真值表正确性 (15分)"] = d4

    # 五、推理合理性 (40 分)
    s5, d5 = _score_reasoning(answer_dir)
    report["五、推理合理性 (40分)"] = d5

    total = min(100, s1 + s2 + s3 + s4 + s5)

    report["分项得分"] = {
        "文件交付": f"{s1}/10",
        "犯罪事实": f"{s2}/20",
        "角色分配": f"{s3}/15",
        "真值表": f"{s4}/15",
        "推理合理性": f"{s5}/40",
    }
    report["总分"] = total
    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """打印格式化的评分报告。"""
    print("=" * 70)
    print(f"评分报告: 基于约束的解谜推理 | 总分: {score}/100")
    print("=" * 70)

    if "error" in report:
        print(f"\n[错误] {report['error']}")

    scores = report.get("分项得分", {})
    if scores:
        print("\n分项得分:")
        for k, v in scores.items():
            print(f"  {k}: {v}")

    sections = [
        "一、文件交付与结构 (10分)",
        "二、犯罪事实正确性 (20分)",
        "三、角色分配正确性 (15分)",
        "四、真值表正确性 (15分)",
        "五、推理合理性 (40分)",
    ]
    for section_key in sections:
        section = report.get(section_key)
        if not section:
            continue
        print(f"\n{'─' * 55}")
        print(f"【{section_key}】")
        print(f"{'─' * 55}")
        if isinstance(section, dict):
            for k, v in section.items():
                if isinstance(v, dict):
                    print(f"  {k}:")
                    for kk, vv in v.items():
                        if isinstance(vv, list):
                            print(f"    {kk}:")
                            for item in vv[:5]:
                                print(f"      - {item}")
                        else:
                            print(f"    {kk}: {vv}")
                elif isinstance(v, list):
                    print(f"  {k}:")
                    for item in v[:5]:
                        print(f"    - {item}")
                else:
                    print(f"  {k}: {v}")

    print("\n" + "=" * 70)


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    test_dir = (
        sys.argv[1]
        if len(sys.argv) > 1
        else os.path.join(os.path.dirname(__file__), "..", "gpt-5", "attempt_1")
    )
    test_dir = os.path.abspath(test_dir)
    if os.path.isdir(test_dir):
        print(f"评估目录: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"目录不存在: {test_dir}")
    sys.exit(0)
