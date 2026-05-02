"""
guanfeng_query8 — 概率统计往年试题参考答案编写 评分脚本
总分 100 分

评分维度:
一、文件交付 (10 分)
    answers.md 存在、非空、文件名正确
二、格式规范 (20 分)
    选择题/简答题分区标题、正确答案/解题思路/知识点说明/解：等格式要素、Markdown 质量
三、选择题正确性 (30 分)
    Q1-Q12 逐题核对答案字母 (每题 2.5 分)
四、计算题质量 (40 分)
    LLM-as-Judge 对 Q13-Q19 评估完整性与正确性
"""

import os
import re
import json
from typing import Tuple, Dict, Any, Optional, List

try:
    import openai
except ImportError:
    openai = None


# ============================================================================
# 选择题参考答案 (Q1-Q12)
# ============================================================================

MCQ_ANSWERS: Dict[int, str] = {
    1: "A",   # k=1/(9σ²), l=1/σ² → χ² 分布构造
    2: "B",   # E[(X-c)²] ≥ E[(X-μ)²]
    3: "A",   # 仅 (ii) 错误 → 1 个错误
    4: "B",   # (i)(iii) 错误 → 2 个错误
    5: "B",   # 假设检验统计量与 p 值
    6: "A",   # P(X=1)=P(X=2)→λ=2, P(X=3)>P(X=4)
    7: "A",   # 对立事件 A̅=B, P(B|B)=1
    8: "D",   # Bayes: P(谨慎|事故)=0.01/0.175≈0.0571
    9: "B",   # (i)(ii) 正确, (iii)(iv) 错误 → 2 个
    10: "C",  # 矩估计 N=7
    11: "A",  # E(Z)=2, Var(Z)=2 (几何分布 p=0.5)
    12: "D",  # X̄ ± (S/3)·t_{0.005}(8)
}


# ============================================================================
# 环境与 LLM 工具函数
# ============================================================================

def _load_env(answer_dir: str) -> dict:
    """从 answer_dir 和 query 根目录加载 .env 配置"""
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
    """获取文本评估 LLM 配置"""
    env = _load_env(answer_dir)

    def g(key: str, default: str = "") -> str:
        return os.environ.get(key) or env.get(key) or default

    return {
        "api_key": g("EVAL_TEXT_API_KEY", g("ANTHROPIC_API_KEY")),
        "api_base": g("EVAL_TEXT_API_BASE_URL", g("ANTHROPIC_BASE_URL")),
        "model": g("EVAL_TEXT_MODEL", "openai/gpt-5.2"),
    }


def _call_llm_judge(prompt: str, config: dict) -> str:
    """调用 LLM 进行文本评估"""
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
            max_tokens=4096,
            temperature=0,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        print(f"[RUBRIC] LLM Judge 调用失败: {e}")
        return ""


# ============================================================================
# 文件查找
# ============================================================================

_CANDIDATE_NAMES = ["answers.md", "answer.md", "Answers.md", "Answer.md",
                    "solution.md", "参考答案.md"]
_EXCLUDED = {"query.md", "TASK_PROMPT.md", "README.md", ".DS_Store"}


def _find_answer_file(answer_dir: str) -> Optional[str]:
    """在 answer_dir 中查找答案 Markdown 文件"""
    if not os.path.isdir(answer_dir):
        return None
    files = os.listdir(answer_dir)
    for name in _CANDIDATE_NAMES:
        if name in files:
            return os.path.join(answer_dir, name)
    for f in sorted(files):
        if f.lower().endswith(".md") and f not in _EXCLUDED and not f.startswith("."):
            return os.path.join(answer_dir, f)
    return None


# ============================================================================
# 一、文件交付 (10 分)
# ============================================================================

def _eval_file_delivery(answer_dir: str) -> Tuple[int, dict]:
    path = _find_answer_file(answer_dir)
    if path is None:
        return 0, {"得分": "0/10", "原因": "未找到 answers.md 或任何 .md 答案文件"}

    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception as e:
        return 0, {"得分": "0/10", "原因": f"文件读取失败: {e}"}

    fname = os.path.basename(path)
    length = len(content.strip())

    if length < 50:
        return 2, {"得分": "2/10", "文件": fname, "原因": "文件内容过短 (< 50 字符)"}
    if length < 200:
        return 4, {"得分": "4/10", "文件": fname, "原因": "文件内容偏短 (< 200 字符)"}

    if fname == "answers.md":
        return 10, {"得分": "10/10", "文件": fname}

    return 7, {"得分": "7/10", "文件": fname,
               "原因": f"文件名不是 answers.md (实际: {fname}), 扣 3 分"}


# ============================================================================
# 二、格式规范 (20 分)
# ============================================================================

def _eval_format(content: str) -> Tuple[int, dict]:
    score = 0
    details: Dict[str, str] = {}

    # 2.1 选择题/简答题分区标题 (4 分)
    has_choice = bool(re.search(r"[#一二三四五六七八九十]+.*选择", content))
    has_calc = bool(re.search(r"[#一二三四五六七八九十]+.*(简答|计算|解答|填空)", content))
    s21 = (2 if has_choice else 0) + (2 if has_calc else 0)
    score += s21
    details["2.1 分区标题 (4分)"] = (
        f"{s21}/4 -- 选择题标题{'有' if has_choice else '无'}, "
        f"简答/计算题标题{'有' if has_calc else '无'}"
    )

    # 2.2 "正确答案" 字段 (4 分)
    ans_hits = len(re.findall(r"正确答案[：:]\s*[A-D]", content))
    s22 = min(4, ans_hits)
    score += s22
    details["2.2 正确答案字段 (4分)"] = f"{s22}/4 -- 找到 {ans_hits} 处"

    # 2.3 "解题思路" 字段 (3 分)
    thought_hits = len(re.findall(r"解题思路[：:]", content))
    s23 = min(3, thought_hits)
    score += s23
    details["2.3 解题思路字段 (3分)"] = f"{s23}/3 -- 找到 {thought_hits} 处"

    # 2.4 "知识点说明" 字段 (4 分)
    kp_hits = len(re.findall(r"知识点说明[：:]", content))
    s24 = min(4, kp_hits)
    score += s24
    details["2.4 知识点说明字段 (4分)"] = f"{s24}/4 -- 找到 {kp_hits} 处"

    # 2.5 "解：" 标记 (3 分)
    sol_hits = len(re.findall(r"解[：:]", content))
    s25 = min(3, sol_hits) if sol_hits <= 30 else 3
    score += s25
    details["2.5 解答标记 (3分)"] = f"{s25}/3 -- 找到 {sol_hits} 处"

    # 2.6 Markdown 总体质量 (2 分)
    has_headers = bool(re.search(r"^#{1,3}\s", content, re.MULTILINE))
    has_math = bool(re.search(r"[\$\\]", content))
    s26 = (1 if has_headers else 0) + (1 if has_math else 0)
    score += s26
    details["2.6 Markdown质量 (2分)"] = (
        f"{s26}/2 -- 标题{'有' if has_headers else '无'}, "
        f"数学公式{'有' if has_math else '无'}"
    )

    return score, details


# ============================================================================
# 三、选择题正确性 (30 分)
# ============================================================================

def _extract_mcq_answers(content: str) -> Dict[int, str]:
    """从文档中提取每道选择题的答案字母"""
    found: Dict[int, str] = {}
    for m in re.finditer(r"正确答案[：:]\s*([A-D])", content):
        letter = m.group(1)
        prefix = content[:m.start()]
        q_matches = list(re.finditer(r"(?:^|\n)\s*(\d{1,2})\s*[\.、．)\）]", prefix))
        if q_matches:
            q_num = int(q_matches[-1].group(1))
            if 1 <= q_num <= 12 and q_num not in found:
                found[q_num] = letter
    return found


def _eval_mcq(content: str) -> Tuple[int, dict]:
    extracted = _extract_mcq_answers(content)
    score = 0.0
    details: Dict[str, str] = {}
    per_q = 2.5

    for q in range(1, 13):
        correct = MCQ_ANSWERS[q]
        if q in extracted:
            if extracted[q] == correct:
                score += per_q
                details[f"Q{q}"] = f"正确 {extracted[q]}"
            else:
                details[f"Q{q}"] = f"错误 {extracted[q]} (应为 {correct})"
        else:
            details[f"Q{q}"] = f"未找到答案 (应为 {correct})"

    int_score = int(round(score))
    details["总分"] = f"{int_score}/30"
    return int_score, details


# ============================================================================
# 四、计算题质量 — LLM-as-Judge (40 分)
# ============================================================================

_CALC_JUDGE_PROMPT = """\
你是一名概率统计课程的严格阅卷老师。请评估以下学生对计算题/简答题 (Q13-Q19) 的作答。

## 各题参考答案要点

Q13 (极大似然估计, 6 分):
设总体 X 的密度为 f(x,theta)=(1/theta)*exp(-(x-mu)/theta), x>=mu。
要点: 写出似然函数; mu 的 MLE 为 X_(1)(最小次序统计量); theta 的 MLE 为 X_bar - X_(1)。

Q14 (最大值分布与条件分布, 6 分):
f(x,y)=6e^(-2x-3y), x>0, y>0, 即 X~Exp(2), Y~Exp(3) 独立。
(1) Z=max(X,Y) 的密度: F_Z(z)=(1-e^(-2z))(1-e^(-3z)), 求导得 f_Z(z)=2e^(-2z)+3e^(-3z)-5e^(-5z), z>0。
(2) 求 P(Z<=z | X>x): 对 z>x, 结果为 (1-e^(-2(z-x)))(1-e^(-3z)) 等形式。

Q15 (切比雪夫不等式与中心极限定理, 6 分):
便利店日均 200 名顾客, 消费 X 为三角分布 (0,60), E(X)=30, Var(X)=150。
日总营业额 T=sum Xi, E(T)=6000, Var(T)=30000。
(1) Chebyshev: P(5800<=T<=6200) >= 1 - 30000/200^2 = 0.25。
(2) CLT: P(|T-6000|<=200) = 2*Phi(200/sqrt(30000)) - 1 ≈ 2*Phi(1.155) - 1 ≈ 0.752。

Q16 (假设检验, 6 分):
脉搏数据 n=9, x_bar=67.4, s=4.93, mu_0=72, sigma_0^2=36。
(1) H0:mu=72, 用 t 检验: t=(67.4-72)/(4.93/3)=-2.80, |t|>t_0.025(8)=2.306, 拒绝 H0。
(2) H0:sigma^2=36, 左侧检验: chi^2=8*24.3/36≈5.40, chi^2_0.95(8)=2.733, 不拒绝 H0。

Q17 (条件密度, 6 分):
X~Exp(lambda), Y given X=x ~ Exp(x)。
(1) 联合密度: f(x,y) = lambda*x*e^(-x(lambda+y)), x>0, y>0。
(2) 边缘密度: f_Y(y) = lambda/(lambda+y)^2, y>0。
(3) 条件密度: f(x given y) = x*(lambda+y)^2 * e^(-x(lambda+y)), Gamma(2, 1/(lambda+y))。

Q18 (匹配/信封问题, 5 分):
n 封信随机放入 n 个信封, S_n = 匹配数。
E(S_n)=1, Var(S_n)=1。
Chebyshev: P(|S_n - 1| >= n*epsilon) <= 1/(n^2 * epsilon^2) -> 0。

Q19 (估计量有效性, 5 分):
X_bar = (1/(n-1)) sum_{i=1}^{n-1} Xi, Y_bar = (1/(n-1)) sum_{i=2}^n Xi.
(1) Cov(X_bar, Y_bar) = (n-2)*sigma^2 / (n-1)^2。
(2) mu_hat = c*X_bar + (1-c)*Y_bar 对任意 c 都是 mu 的无偏估计。
(3) c=1/2 时 Var(mu_hat) 最小, 最有效。

## 学生作答内容

---
{calc_content}
---

## 评分要求

对每道题分别评分, 总共 40 分:
- Q13: 6 分    Q14: 6 分    Q15: 6 分    Q16: 6 分
- Q17: 6 分    Q18: 5 分    Q19: 5 分

评分标准:
- 满分: 思路完整、推导正确、结论正确
- 部分分: 思路正确但计算有误, 或过程不完整但结果接近正确
- 0 分: 完全未作答, 或内容与题目无关

请严格按以下 JSON 格式回复 (不要包含其他文字):
```json
{
  "Q13": {"score": 0, "max": 6, "reason": ""},
  "Q14": {"score": 0, "max": 6, "reason": ""},
  "Q15": {"score": 0, "max": 6, "reason": ""},
  "Q16": {"score": 0, "max": 6, "reason": ""},
  "Q17": {"score": 0, "max": 6, "reason": ""},
  "Q18": {"score": 0, "max": 5, "reason": ""},
  "Q19": {"score": 0, "max": 5, "reason": ""},
  "total": 0,
  "overall_comment": ""
}
```"""


def _extract_calc_section(content: str) -> str:
    """提取 Q13 及之后的计算题/简答题部分"""
    patterns = [
        r"(?:^|\n)\s*(?:#{1,3}\s*)?(?:第?\s*)?(?:十三|13)\s*[\.、．题)\）]",
        r"(?:^|\n)\s*13\s*[\.、．)\）]",
        r"(?:^|\n)\s*(?:#{1,3}\s*)?[二三四五六七八九十]+[、．.\s].*(?:简答|计算|解答|填空)",
    ]
    best_pos = len(content)
    for pat in patterns:
        m = re.search(pat, content)
        if m and m.start() < best_pos:
            best_pos = m.start()

    if best_pos < len(content):
        return content[best_pos:]
    # 降级: 取后 60%
    return content[int(len(content) * 0.4):]


def _eval_calc_llm(content: str, answer_dir: str) -> Tuple[int, dict]:
    """通过 LLM 评估计算题"""
    calc_content = _extract_calc_section(content)

    has_any = bool(re.search(r"(?:13|14|15|16|17|18|19)\s*[\.、．)\）]", calc_content))
    if not has_any and len(calc_content.strip()) < 200:
        return 0, {"得分": "0/40", "原因": "未找到任何计算题内容"}

    config = _get_text_eval_config(answer_dir)
    prompt = _CALC_JUDGE_PROMPT.replace("{calc_content}", calc_content[:8000])
    raw = _call_llm_judge(prompt, config)

    if raw:
        try:
            text = raw
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            result = json.loads(text)
            total = int(result.get("total", 0))
            total = max(0, min(40, total))
            details: Dict[str, str] = {}
            recalc = 0
            for q_key in ["Q13", "Q14", "Q15", "Q16", "Q17", "Q18", "Q19"]:
                qi = result.get(q_key, {})
                q_max = int(qi.get("max", 6))
                q_score = max(0, min(q_max, int(qi.get("score", 0))))
                recalc += q_score
                details[q_key] = f"{q_score}/{q_max} -- {qi.get('reason', '')}"
            total = max(0, min(40, recalc))
            details["总分"] = f"{total}/40"
            details["总评"] = result.get("overall_comment", "")
            details["评估方式"] = "LLM-as-Judge"
            return total, details
        except (json.JSONDecodeError, ValueError, TypeError) as e:
            print(f"[RUBRIC] LLM 返回解析失败: {e}")

    # 降级到关键词评估
    return _eval_calc_heuristic(calc_content)


def _eval_calc_heuristic(calc_content: str) -> Tuple[int, dict]:
    """LLM 不可用时的关键词降级评估 (最高 20/40)"""
    score = 0
    details: Dict[str, str] = {}

    checks = {
        "Q13": (6, [r"极大似然", r"X_?\{?\(?1\)?\}?|最小次序|最小值", r"似然函数"]),
        "Q14": (6, [r"max\s*\(|最大值", r"e\^?\{?-[23]|密度函数|f_Z|f\(z\)", r"条件分布|条件概率"]),
        "Q15": (6, [r"切比雪夫", r"中心极限", r"0\.25|0\.75|6000|30000"]),
        "Q16": (6, [r"假设检验|H_?0", r"t\s*[统检=]|chi|卡方|χ", r"拒绝|不拒绝|显著"]),
        "Q17": (6, [r"条件密度|f_?\{?[XY]\|[XY]\}?|条件分布", r"边缘密度|f_[XY]", r"Gamma|伽马"]),
        "Q18": (5, [r"匹配|信封", r"E\(?S|Var\(?S|期望.*=.*1|方差.*=.*1", r"切比雪夫"]),
        "Q19": (5, [r"有效|无偏|协方差", r"c\s*=|Cov|1/2", r"方差|MSE"]),
    }

    for q, (q_max, patterns) in checks.items():
        hits = sum(1 for p in patterns if re.search(p, calc_content, re.IGNORECASE))
        q_score = min(q_max, int(q_max * hits / len(patterns) * 0.55))
        score += q_score
        details[q] = f"{q_score}/{q_max} -- 关键词 {hits}/{len(patterns)}"

    score = min(20, score)
    details["总分"] = f"{score}/40 (降级评估, 上限 20 分)"
    details["评估方式"] = "关键词降级评估 (LLM 不可用)"
    return score, details


# ============================================================================
# 入口函数
# ============================================================================

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    评估 agent 的输出。

    Args:
        answer_dir: agent 输出目录的绝对路径

    Returns:
        (score, report) — score 为 0-100 的整数, report 为详细报告 dict
    """
    # 一、文件交付
    s1, r1 = _eval_file_delivery(answer_dir)
    if s1 == 0:
        return 0, {
            "总分": 0,
            "一、文件交付 (10分)": r1,
            "原因": "未找到答案文件, 无法继续评估",
        }

    # 读取文件
    path = _find_answer_file(answer_dir)
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # 二、格式规范
    s2, r2 = _eval_format(content)

    # 三、选择题正确性
    s3, r3 = _eval_mcq(content)

    # 四、计算题质量
    s4, r4 = _eval_calc_llm(content, answer_dir)

    total = max(0, min(100, s1 + s2 + s3 + s4))

    report = {
        "总分": total,
        "一、文件交付 (10分)": r1,
        "二、格式规范 (20分)": r2,
        "三、选择题正确性 (30分)": r3,
        "四、计算题质量 (40分)": r4,
        "分项得分": {
            "文件交付": f"{s1}/10",
            "格式规范": f"{s2}/20",
            "选择题": f"{s3}/30",
            "计算题": f"{s4}/40",
        },
    }
    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """打印格式化的评分报告"""
    print("=" * 65)
    print("guanfeng_query8 评分报告")
    print("任务: 概率统计往年试题参考答案编写")
    print("=" * 65)
    print(f"\n总分: {score}/100\n")

    scores = report.get("分项得分", {})
    if scores:
        print("分项得分:")
        for k, v in scores.items():
            print(f"  {k}: {v}")
        print()

    for section in ["一、文件交付 (10分)", "二、格式规范 (20分)",
                     "三、选择题正确性 (30分)", "四、计算题质量 (40分)"]:
        data = report.get(section, {})
        if not data:
            continue
        print("-" * 50)
        print(f"[{section}]")
        print("-" * 50)
        if isinstance(data, dict):
            for k, v in data.items():
                print(f"  {k}: {v}")
        else:
            print(f"  {data}")
        print()

    print("=" * 65)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        test_dir = sys.argv[1]
    else:
        test_dir = os.path.join(os.path.dirname(__file__), "..", "gpt-5", "attempt_1")
    if not os.path.exists(test_dir):
        test_dir = os.path.join(os.path.dirname(__file__), "..", "workspace")
    if os.path.exists(test_dir):
        print(f"正在评估目录: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"目录不存在: {test_dir}")
    sys.exit(0)
