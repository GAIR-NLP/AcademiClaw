"""
Query 5 Rubric — Personalized 30-Day Data Analysis Interview Study Plan

Total: 100 points

Scoring dimensions (from description.json evaluation_criteria):
1. Skill Coverage Comprehensiveness & Relevance (30 pts) — Deterministic keywords + LLM
2. Difficulty Progression Reasonableness (25 pts) — Structure detection + LLM
3. Resource Authenticity & Quality (20 pts) — Deterministic detection + LLM
4. Practicality & Executability (15 pts) — Deterministic detection + LLM
5. Document Format & Extras (10 pts) — Deterministic checks
"""

import os
import re
import sys
import json
from typing import Tuple, Dict, Any, List

try:
    import openai
except ImportError:
    openai = None


# =============================================================================
# Environment & LLM Configuration
# =============================================================================

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
                        k = k.strip()
                        v = v.strip().strip("'\"")
                        if k not in values:
                            values[k] = v
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
    """Call LLM for evaluation, return raw text"""
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


def _extract_json(text: str) -> dict:
    """Extract JSON from LLM response text"""
    if not text:
        return {}
    m = re.search(r"```json\s*(.*?)```", text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1).strip())
        except json.JSONDecodeError:
            pass
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group())
        except json.JSONDecodeError:
            pass
    return {}


# =============================================================================
# Helpers: File finding & reading
# =============================================================================

def _find_plan_md(answer_dir: str) -> str:
    """Find the study plan Markdown file"""
    if not os.path.isdir(answer_dir):
        return ""
    md_files = [f for f in os.listdir(answer_dir) if f.endswith(".md") and not f.startswith(".")]
    if not md_files:
        return ""
    priority_kw = ["学习计划", "study", "plan", "30天", "30day"]
    for f in md_files:
        fl = f.lower()
        for kw in priority_kw:
            if kw in fl or kw in f:
                return os.path.join(answer_dir, f)
    return os.path.join(answer_dir, md_files[0])


def _find_ics(answer_dir: str) -> str:
    """Find .ics calendar file"""
    if not os.path.isdir(answer_dir):
        return ""
    for f in os.listdir(answer_dir):
        if f.endswith(".ics"):
            return os.path.join(answer_dir, f)
    return ""


def _safe_read(path: str, max_chars: int = 0) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        return content[:max_chars] if max_chars > 0 else content
    except Exception:
        return ""


# =============================================================================
# 1. Skill Coverage Comprehensiveness & Relevance (30 pts)
#   1a. Deterministic keyword detection (15 pts)
#   1b. LLM depth evaluation (15 pts)
# =============================================================================

_SKILL_GROUPS = {
    "SQL_basics": ["SELECT", "WHERE", "ORDER BY", "GROUP BY", "HAVING"],
    "SQL_advanced": ["JOIN", "INNER JOIN", "LEFT JOIN", "子查询", "CTE", "窗口函数",
                 "WINDOW", "RANK", "ROW_NUMBER"],
    "Pandas": ["Pandas", "DataFrame", "pd.read", "groupby", "merge", "concat"],
    "NumPy": ["NumPy", "numpy", "ndarray", "np.array", "np."],
    "Matplotlib": ["Matplotlib", "pyplot", "plt.plot", "plt.show"],
    "Seaborn": ["Seaborn", "sns.", "seaborn"],
    "statistics": ["统计", "假设检验", "概率分布", "p值", "t检验", "正态分布",
               "描述性统计", "statistics", "hypothesis", "回归"],
    "machine_learning": ["机器学习", "machine learning", "scikit-learn", "sklearn",
                 "线性回归", "逻辑回归", "决策树", "随机森林", "分类", "预测模型"],
}

# Bonus: skills mentioned in task but not mandatory
_BONUS_SKILLS = {
    "A/B_testing": ["A/B测试", "A/B test", "ab test"],
    "data_cleaning": ["数据清洗", "缺失值", "异常值", "data cleaning", "missing value"],
    "interview_prep": ["面试", "interview", "面经", "笔试"],
}


def _eval_skill_coverage(content: str, config: dict) -> Tuple[int, Dict[str, Any]]:
    score = 0
    details: Dict[str, Any] = {}

    content_upper = content.upper()
    covered: List[str] = []
    missed: List[str] = []

    for skill, keywords in _SKILL_GROUPS.items():
        hit = any(kw.upper() in content_upper for kw in keywords)
        if hit:
            covered.append(skill)
        else:
            missed.append(skill)

    # 8 core skill groups, each hit scores ~1.875, max 15
    kw_score = min(15, round(len(covered) * 15 / len(_SKILL_GROUPS)))
    score += kw_score
    details["1a_keyword_detection"] = f"{kw_score}/15 — covered {len(covered)}/{len(_SKILL_GROUPS)} core skill groups"
    details["1a_covered"] = ", ".join(covered) if covered else "none"
    details["1a_missed"] = ", ".join(missed) if missed else "none"

    # 1b. LLM depth evaluation
    prompt = f"""You are a senior data analysis training expert. Please evaluate the skill coverage of the following 30-day data analysis interview study plan.

[Target User] Intermediate Python learner (mastered basic syntax and data structures), target position: Data Analyst
[Core Requirements] Plan should cover: SQL querying (basic to advanced), Python data processing (Pandas/NumPy), data visualization (Matplotlib/Seaborn), statistics fundamentals (hypothesis testing/probability distributions), machine learning introduction (at least 2-3 algorithms)

[Study Plan Content (first 8000 chars)]
{content[:8000]}

Please evaluate skill coverage (total 0-15):
1. SQL coverage depth (0-4): Is there systematic arrangement from basic SELECT to JOIN, aggregation, subqueries, and window functions?
2. Python data processing (0-4): Are Pandas core operations (read/clean/aggregate/merge) and NumPy fundamentals sufficient?
3. Visualization + Statistics (0-4): Are Matplotlib/Seaborn charting skills + statistics fundamentals (descriptive stats/hypothesis testing/probability distributions) both covered?
4. Machine learning introduction (0-3): Does it cover at least 2 basic algorithms (e.g., linear regression, logistic regression, decision trees)?

Score strictly. Missing important modules should result in major deductions. Reply in JSON format:
```json
{{"sql_depth": 0, "python_data": 0, "viz_stats": 0, "ml_intro": 0, "total": 0, "comment": ""}}
```"""

    llm_raw = _call_llm_judge(prompt, config)
    llm_res = _extract_json(llm_raw)

    if llm_res and "total" in llm_res:
        llm_score = max(0, min(15, int(llm_res["total"])))
        score += llm_score
        details["1b_LLM_evaluation"] = f"{llm_score}/15"
        details["1b_sub_items"] = {
            "SQL_depth": f"{llm_res.get('sql_depth', '?')}/4",
            "Python_processing": f"{llm_res.get('python_data', '?')}/4",
            "visualization_stats": f"{llm_res.get('viz_stats', '?')}/4",
            "ML_intro": f"{llm_res.get('ml_intro', '?')}/3",
        }
        details["1b_comment"] = llm_res.get("comment", "")
    else:
        fallback = min(8, kw_score)
        score += fallback
        details["1b_LLM_evaluation"] = f"{fallback}/15 (LLM unavailable, degraded estimate)"

    return score, details


# =============================================================================
# 2. Difficulty Progression Reasonableness (25 pts)
#   2a. Deterministic structure check (5 pts)
#   2b. LLM progression evaluation (20 pts)
# =============================================================================

def _eval_progression(content: str, config: dict) -> Tuple[int, Dict[str, Any]]:
    score = 0
    details: Dict[str, Any] = {}

    # 2a. Deterministic: check week/day structure
    week_matches = re.findall(r"第.{1,3}周|Week\s*\d+", content, re.IGNORECASE)
    day_matches = re.findall(r"Day\s*(\d+)|第\s*(\d+)\s*天", content, re.IGNORECASE)
    day_nums = set()
    for m in day_matches:
        n = m[0] or m[1]
        if n:
            day_nums.add(int(n))

    struct_score = 0
    has_week = len(week_matches) >= 4
    if has_week:
        struct_score += 2

    if len(day_nums) >= 28:
        struct_score += 3
    elif len(day_nums) >= 20:
        struct_score += 2
    elif len(day_nums) >= 10:
        struct_score += 1

    score += struct_score
    details["2a_structure_detection"] = (
        f"{struct_score}/5 — "
        f"{'has' if has_week else 'no'} complete week division ({len(week_matches)} weeks), "
        f"detected {len(day_nums)} distinct Day(s)"
    )

    # 2b. LLM progression evaluation
    prompt = f"""You are an educational curriculum design expert. Please evaluate the difficulty progression design of the following 30-day data analysis study plan.

[Target User] Intermediate Python learner (mastered basic Python syntax and data structures)
[Recommended Progression] SQL basics -> Python data processing (Pandas/NumPy) -> Data visualization + Statistics -> ML introduction -> Comprehensive projects

[Study Plan Content (first 8000 chars)]
{content[:8000]}

Please evaluate difficulty progression reasonableness (total 0-20):
1. Starting point reasonableness (0-5): Is the Week 1 starting point appropriate for an intermediate Python learner? (Should not start from Python basics, nor jump directly to ML)
2. Inter-week progression (0-5): Do weekly themes have a reasonable easy-to-hard progression? SQL -> Pandas -> Viz/Stats -> ML is the recommended route
3. Intra-day progression (0-5): Within each week, does the daily arrangement progress from basic concepts to comprehensive application?
4. Comprehensive project (0-5): Is there a comprehensive project arranged at the end (e.g., end-to-end analysis using Kaggle datasets) to consolidate learning?

Score strictly. No comprehensive project = full 5-point deduction, confused progression = major deduction.
Reply in JSON format:
```json
{{"starting_point": 0, "weekly_prog": 0, "daily_prog": 0, "project": 0, "total": 0, "comment": ""}}
```"""

    llm_raw = _call_llm_judge(prompt, config)
    llm_res = _extract_json(llm_raw)

    if llm_res and "total" in llm_res:
        llm_score = max(0, min(20, int(llm_res["total"])))
        score += llm_score
        details["2b_LLM_progression_eval"] = f"{llm_score}/20"
        details["2b_sub_items"] = {
            "starting_point": f"{llm_res.get('starting_point', '?')}/5",
            "weekly_progression": f"{llm_res.get('weekly_prog', '?')}/5",
            "daily_progression": f"{llm_res.get('daily_prog', '?')}/5",
            "comprehensive_project": f"{llm_res.get('project', '?')}/5",
        }
        details["2b_comment"] = llm_res.get("comment", "")
    else:
        fallback = 8 if struct_score >= 4 else 4
        score += fallback
        details["2b_LLM_progression_eval"] = f"{fallback}/20 (LLM unavailable, degraded estimate)"

    return score, details


# =============================================================================
# 3. Resource Authenticity & Quality (20 pts)
#   3a. Deterministic: link count & diversity (8 pts)
#   3b. LLM: resource quality depth evaluation (12 pts)
# =============================================================================

_KNOWN_QUALITY_DOMAINS = {
    "youtube.com", "www.youtube.com",
    "coursera.org", "www.coursera.org",
    "kaggle.com", "www.kaggle.com",
    "w3schools.com", "www.w3schools.com",
    "mode.com",
    "sqlbolt.com",
    "leetcode.com", "www.leetcode.com",
    "datacamp.com", "www.datacamp.com",
    "freecodecamp.org", "www.freecodecamp.org",
    "stratascratch.com", "www.stratascratch.com",
    "hackerrank.com", "www.hackerrank.com",
    "geeksforgeeks.org", "www.geeksforgeeks.org",
    "matplotlib.org",
    "seaborn.pydata.org",
    "pandas.pydata.org",
    "numpy.org",
    "scikit-learn.org",
    "docs.python.org",
    "github.com",
    "medium.com",
    "khanacademy.org", "www.khanacademy.org",
    "bilibili.com", "www.bilibili.com",
}


def _eval_resources(content: str, config: dict) -> Tuple[int, Dict[str, Any]]:
    score = 0
    details: Dict[str, Any] = {}

    # 3a. Link count & quality domains
    urls = re.findall(r"https?://[^\s\)\"'>\]]+", content)
    domains = set()
    quality_domains = set()
    for url in urls:
        m = re.search(r"https?://([^/\s]+)", url)
        if m:
            d = m.group(1).lower()
            domains.add(d)
            if d in _KNOWN_QUALITY_DOMAINS:
                quality_domains.add(d)

    link_score = 0
    # Count score (0-4)
    if len(urls) >= 30:
        link_score += 4
    elif len(urls) >= 15:
        link_score += 3
    elif len(urls) >= 5:
        link_score += 2
    elif len(urls) >= 1:
        link_score += 1

    # Quality domain score (0-4)
    if len(quality_domains) >= 6:
        link_score += 4
    elif len(quality_domains) >= 4:
        link_score += 3
    elif len(quality_domains) >= 2:
        link_score += 2
    elif len(quality_domains) >= 1:
        link_score += 1

    score += link_score
    details["3a_link_detection"] = (
        f"{link_score}/8 — {len(urls)} links, {len(domains)} domains, "
        f"{len(quality_domains)} well-known learning platforms"
    )
    if quality_domains:
        details["3a_quality_platforms"] = ", ".join(sorted(quality_domains))

    # 3b. LLM resource quality evaluation
    prompt = f"""You are an online education resource review expert. Please evaluate the quality of learning resources recommended in the following 30-day data analysis study plan.

[Study Plan Content (first 8000 chars)]
{content[:8000]}

Please evaluate resource quality (total 0-12):
1. Resource authenticity (0-4): Do recommended links point to real, well-known learning platforms? (e.g., Coursera, Kaggle, freeCodeCamp, W3Schools, SQLBolt, Mode Analytics, YouTube, etc.). Deduct for fabricated links or links to non-existent pages.
2. Resource description specificity (0-4): Does each resource have a specific description (course name, chapter number, video duration, etc.)? Or just vague "watch a tutorial"?
3. Resource type diversity (0-4): Does it simultaneously include videos, articles/documentation, interactive practice platforms, books, and other resource types?

Score strictly. Plain link listing without descriptions should be deducted.
Reply in JSON format:
```json
{{"authenticity": 0, "specificity": 0, "diversity": 0, "total": 0, "comment": ""}}
```"""

    llm_raw = _call_llm_judge(prompt, config)
    llm_res = _extract_json(llm_raw)

    if llm_res and "total" in llm_res:
        llm_score = max(0, min(12, int(llm_res["total"])))
        score += llm_score
        details["3b_LLM_resource_eval"] = f"{llm_score}/12"
        details["3b_sub_items"] = {
            "authenticity": f"{llm_res.get('authenticity', '?')}/4",
            "specificity": f"{llm_res.get('specificity', '?')}/4",
            "diversity": f"{llm_res.get('diversity', '?')}/4",
        }
        details["3b_comment"] = llm_res.get("comment", "")
    else:
        fallback = min(6, link_score)
        score += fallback
        details["3b_LLM_resource_eval"] = f"{fallback}/12 (LLM unavailable, degraded estimate)"

    return score, details


# =============================================================================
# 4. Practicality & Executability (15 pts)
#   4a. Deterministic: practice task keyword detection (5 pts)
#   4b. LLM: practice design and time arrangement (10 pts)
# =============================================================================

def _eval_practicality(content: str, config: dict) -> Tuple[int, Dict[str, Any]]:
    score = 0
    details: Dict[str, Any] = {}

    # 4a. Practice keyword detection
    practice_kw = [
        "实践任务", "练习", "实战", "项目", "Kaggle", "LeetCode",
        "作业", "动手", "实操", "综合项目", "数据集", "练习题",
        "完成", "exercise", "practice", "project", "dataset",
    ]
    content_lower = content.lower()
    hit_count = 0
    for kw in practice_kw:
        hit_count += len(re.findall(re.escape(kw.lower()), content_lower))

    # Estimated time detection
    time_mentions = len(re.findall(r"预计用时|学习时间|小时|hours?|2-3.*时|estimated time", content, re.IGNORECASE))

    prac_score = 0
    if hit_count >= 25 and time_mentions >= 5:
        prac_score = 5
    elif hit_count >= 15:
        prac_score = 4
    elif hit_count >= 8:
        prac_score = 3
    elif hit_count >= 3:
        prac_score = 2
    elif hit_count >= 1:
        prac_score = 1

    score += prac_score
    details["4a_practice_detection"] = (
        f"{prac_score}/5 — {hit_count} practice-related mentions, "
        f"{time_mentions} time estimates"
    )

    # 4b. LLM practicality evaluation
    prompt = f"""You are a professional training course evaluation expert. Please evaluate the practicality and executability of the following 30-day study plan.

[User Info] Can study 2-3 hours daily, intermediate Python learner, target: data analyst job interview

[Study Plan Content (first 8000 chars)]
{content[:8000]}

Please evaluate practicality (total 0-10):
1. Daily practice tasks (0-4): Is there a clear practice/exercise task arranged every day? Are task descriptions clear and specific?
2. Time arrangement feasibility (0-3): Does daily content match 2-3 hours? Are any days overloaded/underloaded? Is estimated daily time marked?
3. Comprehensive project quality (0-3): Does the final stage's comprehensive project use real datasets (e.g., Kaggle)? Does it integrate SQL + Python + visualization and other skills?

Score strictly. No daily practice tasks should result in major deduction.
Reply in JSON format:
```json
{{"daily_practice": 0, "time_feasibility": 0, "project_quality": 0, "total": 0, "comment": ""}}
```"""

    llm_raw = _call_llm_judge(prompt, config)
    llm_res = _extract_json(llm_raw)

    if llm_res and "total" in llm_res:
        llm_score = max(0, min(10, int(llm_res["total"])))
        score += llm_score
        details["4b_LLM_practicality_eval"] = f"{llm_score}/10"
        details["4b_sub_items"] = {
            "daily_practice": f"{llm_res.get('daily_practice', '?')}/4",
            "time_feasibility": f"{llm_res.get('time_feasibility', '?')}/3",
            "comprehensive_project": f"{llm_res.get('project_quality', '?')}/3",
        }
        details["4b_comment"] = llm_res.get("comment", "")
    else:
        fallback = min(5, prac_score)
        score += fallback
        details["4b_LLM_practicality_eval"] = f"{fallback}/10 (LLM unavailable, degraded estimate)"

    return score, details


# =============================================================================
# 5. Document Format & Extras (10 pts)
#   5a. Markdown formatting standards (3 pts)
#   5b. Document structure completeness (4 pts)
#   5c. ICS calendar file (3 pts)
# =============================================================================

def _eval_format(content: str, answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    score = 0
    details: Dict[str, Any] = {}

    # 5a. Markdown formatting standards (3 pts)
    has_h1 = bool(re.search(r"^# ", content, re.MULTILINE))
    has_h2 = bool(re.search(r"^## ", content, re.MULTILINE))
    has_h3 = bool(re.search(r"^### ", content, re.MULTILINE))
    has_list = bool(re.search(r"^[-*]\s", content, re.MULTILINE))
    has_hr = bool(re.search(r"^---", content, re.MULTILINE))

    md_score = 0
    if has_h1 and has_h2 and has_h3:
        md_score += 2
    elif has_h2 and has_h3:
        md_score += 1
    if has_list or has_hr:
        md_score += 1
    md_score = min(3, md_score)

    score += md_score
    details["5a_markdown_format"] = (
        f"{md_score}/3 — H1:{'Y' if has_h1 else 'N'} "
        f"H2:{'Y' if has_h2 else 'N'} H3:{'Y' if has_h3 else 'N'} "
        f"Lists:{'Y' if has_list else 'N'} Dividers:{'Y' if has_hr else 'N'}"
    )

    # 5b. Document structure completeness (4 pts): user profile, 4-week division, appendix/tips, daily time estimate
    content_lower = content.lower()
    has_profile = bool(re.search(r"用户画像|学习者信息|个人背景|当前技能|user profile|current skill", content_lower))
    week_headers = re.findall(r"第.{1,3}周|Week\s*\d+", content, re.IGNORECASE)
    has_4weeks = len(week_headers) >= 4
    has_appendix = bool(re.search(r"附录|推荐资源汇总|学习建议|面试准备|总结|appendix|summary|study tips", content_lower))
    has_time = bool(re.search(r"预计用时|预估时间|学习时长|estimated time", content_lower))

    struct_score = 0
    if has_profile:
        struct_score += 1
    if has_4weeks:
        struct_score += 1
    if has_appendix:
        struct_score += 1
    if has_time:
        struct_score += 1

    score += struct_score
    details["5b_structure_completeness"] = (
        f"{struct_score}/4 — User profile:{'Y' if has_profile else 'N'} "
        f"4-week division:{'Y' if has_4weeks else 'N'}({len(week_headers)} weeks) "
        f"Appendix/Tips:{'Y' if has_appendix else 'N'} "
        f"Daily time:{'Y' if has_time else 'N'}"
    )

    # 5c. ICS calendar file (3 pts)
    ics_path = _find_ics(answer_dir)
    if ics_path:
        ics_content = _safe_read(ics_path)
        has_vcalendar = "BEGIN:VCALENDAR" in ics_content and "END:VCALENDAR" in ics_content
        vevent_count = ics_content.count("BEGIN:VEVENT")
        has_dtstart = "DTSTART" in ics_content
        has_alarm = "VALARM" in ics_content
        has_summary = "SUMMARY" in ics_content

        ics_score = 0
        if has_vcalendar and vevent_count >= 25 and has_dtstart and has_summary:
            ics_score = 3
        elif has_vcalendar and vevent_count >= 15 and has_dtstart:
            ics_score = 2
        elif has_vcalendar and vevent_count >= 1:
            ics_score = 1

        score += ics_score
        details["5c_ICS_calendar"] = (
            f"{ics_score}/3 — {vevent_count} events, "
            f"VCALENDAR:{'Y' if has_vcalendar else 'N'} "
            f"DTSTART:{'Y' if has_dtstart else 'N'} "
            f"SUMMARY:{'Y' if has_summary else 'N'} "
            f"VALARM:{'Y' if has_alarm else 'N'}"
        )
    else:
        details["5c_ICS_calendar"] = "0/3 — .ics file not provided (optional item)"

    return score, details


# =============================================================================
# Main Entry
# =============================================================================

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Evaluate the agent's output.

    Args:
        answer_dir: absolute path to the agent output directory

    Returns:
        (score, report) — score: 0-100 integer, report: detailed evaluation report
    """
    report: Dict[str, Any] = {}

    # Find study plan file
    plan_path = _find_plan_md(answer_dir)
    if not plan_path:
        report["termination_reason"] = "No Markdown study plan file found, cannot evaluate"
        report["dimension_scores"] = {
            "skill_coverage": "0/30", "difficulty_progression": "0/25",
            "resource_quality": "0/20", "practicality": "0/15", "document_format": "0/10",
        }
        return 0, report

    content = _safe_read(plan_path)
    if not content or len(content) < 100:
        report["termination_reason"] = f"Study plan file content too short ({len(content)} chars), considered incomplete"
        report["dimension_scores"] = {
            "skill_coverage": "0/30", "difficulty_progression": "0/25",
            "resource_quality": "0/20", "practicality": "0/15", "document_format": "0/10",
        }
        return 0, report

    report["file_info"] = {
        "filename": os.path.basename(plan_path),
        "content_length": f"{len(content)} chars",
    }

    config = _get_text_eval_config(answer_dir)

    # 1. Skill Coverage (30 pts)
    s1, r1 = _eval_skill_coverage(content, config)
    report["1. Skill Coverage Comprehensiveness (30 pts)"] = r1

    # 2. Difficulty Progression (25 pts)
    s2, r2 = _eval_progression(content, config)
    report["2. Difficulty Progression Reasonableness (25 pts)"] = r2

    # 3. Resource Quality (20 pts)
    s3, r3 = _eval_resources(content, config)
    report["3. Resource Authenticity & Quality (20 pts)"] = r3

    # 4. Practicality (15 pts)
    s4, r4 = _eval_practicality(content, config)
    report["4. Practicality & Executability (15 pts)"] = r4

    # 5. Format (10 pts)
    s5, r5 = _eval_format(content, answer_dir)
    report["5. Document Format & Extras (10 pts)"] = r5

    total = max(0, min(100, s1 + s2 + s3 + s4 + s5))

    report["dimension_scores"] = {
        "skill_coverage": f"{s1}/30",
        "difficulty_progression": f"{s2}/25",
        "resource_quality": f"{s3}/20",
        "practicality": f"{s4}/15",
        "document_format": f"{s5}/10",
    }

    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print a formatted scoring report"""
    print("=" * 65)
    print("Query 5 Scoring Report: Personalized 30-Day Data Analysis Interview Study Plan")
    print("=" * 65)
    print(f"\nTotal Score: {score}/100")

    level = (
        "Excellent" if score >= 85
        else "Good" if score >= 70
        else "Passing" if score >= 60
        else "Failing"
    )
    print(f"Grade: {level}")

    # File info
    fi = report.get("file_info", {})
    if fi:
        print(f"\nFile: {fi.get('filename', '?')} ({fi.get('content_length', '?')})")

    # Dimension scores overview
    sub = report.get("dimension_scores", {})
    if sub:
        print("\nDimension Scores:")
        for k, v in sub.items():
            print(f"  {k}: {v}")

    # Detailed per-dimension breakdown
    for key in [
        "1. Skill Coverage Comprehensiveness (30 pts)",
        "2. Difficulty Progression Reasonableness (25 pts)",
        "3. Resource Authenticity & Quality (20 pts)",
        "4. Practicality & Executability (15 pts)",
        "5. Document Format & Extras (10 pts)",
    ]:
        section = report.get(key, {})
        if section:
            print(f"\n{'─' * 50}")
            print(f"[{key}]")
            for k, v in section.items():
                if isinstance(v, dict):
                    print(f"  {k}:")
                    for kk, vv in v.items():
                        print(f"    {kk}: {vv}")
                else:
                    print(f"  {k}: {v}")

    if "termination_reason" in report:
        print(f"\n[!] {report['termination_reason']}")

    print(f"\n{'=' * 65}")


if __name__ == "__main__":
    # Default to gpt-5/attempt_1 if no args
    if len(sys.argv) < 2:
        sys.argv.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gpt-5", "attempt_1"))

    answer_dir = sys.argv[1]
    if not os.path.isabs(answer_dir):
        answer_dir = os.path.join(os.getcwd(), answer_dir)

    s, r = evaluate(answer_dir)
    print_report(s, r)
