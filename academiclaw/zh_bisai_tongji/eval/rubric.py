"""
pengyichen-query5 评分标准 (Rubric) — 从零重写
任务：比赛数据统计分析与实力预测报告

总分：100 分

评分维度：
一、文件交付 (10分)
    - 存在 Markdown 格式的分析报告
    - 文件长度合理（内容充实）
二、报告结构与章节完整性 (15分)
    - 包含总体统计章节
    - 包含队伍详细统计章节（地图胜率、赛制胜率、连胜连败、对阵历史、特殊事件）
    - 包含实力预测分析章节
三、统计数据准确性 (40分)
    - 程序化验证报告中的关键数据与 CSV 源数据一致 (15分)
    - LLM-as-Judge 评估数据准确性和完整性 (25分)
四、预测分析质量 (20分) — LLM-as-Judge
    - 排名预测合理性
    - 趋势分析深度
    - 建议具体性
五、报告格式与可读性 (15分)
    - Markdown 格式规范（标题层次、表格、列表）
    - 数据密度
"""

import os
import re
import csv
import json
from typing import Tuple, Dict, Any, List
from collections import defaultdict

try:
    import openai
except ImportError:
    openai = None


# ============================================================================
# 环境 / LLM 工具函数
# ============================================================================

def _load_env(answer_dir: str) -> dict:
    """从 answer_dir 和 query 根目录加载 .env 配置"""
    values = {}
    for env_dir in [answer_dir, os.path.join(os.path.dirname(__file__), "..")]:
        env_path = os.path.join(env_dir, ".env")
        if os.path.exists(env_path):
            try:
                with open(env_path, "r") as f:
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
    def g(key, default=""):
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
        text = resp.choices[0].message.content
        if not text:
            msg = resp.choices[0].message
            text = getattr(msg, "reasoning_content", None) or ""
        return text.strip()
    except Exception as e:
        print("[RUBRIC] LLM Judge call failed: %s" % e)
        return ""


def _parse_json_from_llm(text: str) -> dict:
    """从 LLM 返回文本中提取 JSON"""
    m = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            pass
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1:
        try:
            return json.loads(text[start:end + 1])
        except json.JSONDecodeError:
            pass
    return {}


# ============================================================================
# 辅助：CSV 数据解析（用于程序化验证）
# ============================================================================

def _safe_int(s):
    try:
        return int(s)
    except (ValueError, TypeError):
        return 0


def _parse_single_csv(file_path: str) -> dict:
    """解析单个比赛 CSV 文件，提取结构化数据"""
    try:
        with open(file_path, newline="", encoding="gbk") as f:
            reader = csv.reader(f)
            data = list(reader)
    except Exception:
        return {}

    if not data or data[0][0].strip() != "6657":
        return {}

    try:
        year = int(data[1][0])
        month = int(data[1][1])
        day = int(data[1][2])
        n = int(data[2][0])
    except (IndexError, ValueError):
        return {}

    teams = {}
    for i in range(n):
        if 3 + i >= len(data):
            break
        row = data[3 + i]
        team_name = row[0].strip()
        teams[team_name] = {
            "bo1_wins": 0, "bo1_losses": 0, "bo1_count": 0,
            "bo3_wins": 0, "bo3_losses": 0, "bo3_count": 0,
            "bo5_wins": 0, "bo5_losses": 0, "bo5_count": 0,
            "match_wins": 0, "match_losses": 0, "match_count": 0,
            "game_wins": 0, "game_losses": 0,
            "map_stats": defaultdict(lambda: {"wins": 0, "losses": 0}),
            "win_streak_seq": [],
            "late_count": 0, "forfeit_count": 0,
            "opponents": defaultdict(lambda: {"wins": 0, "losses": 0}),
        }

    matches = []
    for row in data[3 + n:]:
        if not row or row[0].strip() == "123321":
            break
        if not row[0].strip():
            continue
        try:
            match_type = int(row[0])
        except ValueError:
            continue
        try:
            importance = int(row[1])
        except (ValueError, IndexError):
            importance = 1

        team1 = row[2].strip() if len(row) > 2 else ""
        team2 = row[3].strip() if len(row) > 3 else ""
        if team1 not in teams or team2 not in teams:
            continue

        scores_raw = row[4:]
        scores = []
        for j in range(0, len(scores_raw), 3):
            if j + 2 >= len(scores_raw):
                break
            s1 = scores_raw[j].strip() if scores_raw[j].strip() else "0"
            s2 = scores_raw[j + 1].strip() if scores_raw[j + 1].strip() else "0"
            map_name = scores_raw[j + 2].strip()
            if map_name in ("*", ""):
                map_name = None
            scores.append((s1, s2, map_name))

        matches.append({
            "type": match_type, "importance": importance,
            "team1": team1, "team2": team2, "scores": scores,
        })

        teams[team1]["match_count"] += 1
        teams[team2]["match_count"] += 1

        if not scores:
            continue

        first_s1, first_s2, _ = scores[0]

        # Special events (late / forfeit / default loss)
        if first_s1 in ("-1", "-2", "-3") or first_s2 in ("-1", "-2", "-3"):
            if first_s1 in ("-1", "-2", "-3"):
                losing, winning, special = team1, team2, first_s1
            else:
                losing, winning, special = team2, team1, first_s2
            teams[winning]["match_wins"] += 1
            teams[losing]["match_losses"] += 1
            teams[winning]["opponents"][losing]["wins"] += 1
            teams[losing]["opponents"][winning]["losses"] += 1
            if special == "-1":
                teams[losing]["late_count"] += 1
            elif special == "-2":
                teams[losing]["forfeit_count"] += 1
            continue

        # Normal match processing
        bo_key = "bo%d" % match_type if match_type in (1, 3, 5) else "bo1"
        teams[team1][bo_key + "_count"] += 1
        teams[team2][bo_key + "_count"] += 1

        t1_wins = sum(1 for s in scores if _safe_int(s[0]) > _safe_int(s[1]))
        t2_wins = sum(1 for s in scores if _safe_int(s[1]) > _safe_int(s[0]))

        if t1_wins > t2_wins:
            winner, loser = team1, team2
        else:
            winner, loser = team2, team1

        teams[winner]["match_wins"] += 1
        teams[loser]["match_losses"] += 1
        teams[winner][bo_key + "_wins"] += 1
        teams[loser][bo_key + "_losses"] += 1
        teams[winner]["opponents"][loser]["wins"] += 1
        teams[loser]["opponents"][winner]["losses"] += 1
        teams[winner]["win_streak_seq"].append(1)
        teams[loser]["win_streak_seq"].append(0)

        for s in scores:
            s1v, s2v = _safe_int(s[0]), _safe_int(s[1])
            if s1v > s2v:
                teams[team1]["game_wins"] += 1
                teams[team2]["game_losses"] += 1
            elif s2v > s1v:
                teams[team2]["game_wins"] += 1
                teams[team1]["game_losses"] += 1
            if s[2] is not None:
                if s1v > s2v:
                    teams[team1]["map_stats"][s[2]]["wins"] += 1
                    teams[team2]["map_stats"][s[2]]["losses"] += 1
                elif s2v > s1v:
                    teams[team2]["map_stats"][s[2]]["wins"] += 1
                    teams[team1]["map_stats"][s[2]]["losses"] += 1

    return {
        "date": "%d-%02d-%02d" % (year, month, day),
        "num_teams": n,
        "team_names": list(teams.keys()),
        "match_count": len(matches),
        "teams": teams,
    }


def _load_all_csv_data() -> List[dict]:
    """加载 context/match_data 下所有 CSV 数据"""
    base = os.path.join(os.path.dirname(__file__), "..")
    md_dir = os.path.join(base, "context", "match_data")
    if not os.path.isdir(md_dir):
        return []

    results = []
    for fname in sorted(os.listdir(md_dir)):
        if fname.endswith(".csv"):
            parsed = _parse_single_csv(os.path.join(md_dir, fname))
            if parsed:
                parsed["file_name"] = fname
                results.append(parsed)
    return results


# ============================================================================
# 辅助：查找报告文件
# ============================================================================

def _find_report(answer_dir: str) -> str:
    """查找 answer_dir 中最可能的 Markdown 分析报告"""
    if not os.path.isdir(answer_dir):
        return ""

    skip_dirs = {"__pycache__", "node_modules", ".sii", ".git", "context", "match_data"}
    skip_names = {"query.md", "task_prompt.md", "readme.md"}
    candidates = []

    for root, dirs, files in os.walk(answer_dir):
        dirs[:] = [d for d in dirs if d.lower() not in skip_dirs and not d.startswith(".")]
        for f in files:
            lower = f.lower()
            if not lower.endswith(".md"):
                continue
            if lower in skip_names:
                continue
            full = os.path.join(root, f)
            size = os.path.getsize(full)
            priority = 2
            for kw in ("report", "analysis", "统计", "分析", "报告", "stat"):
                if kw in lower:
                    priority = 0
                    break
            candidates.append((priority, -size, full))

    if not candidates:
        return ""
    candidates.sort()
    return candidates[0][2]


def _load_file(path: str) -> str:
    """多编码加载文本文件"""
    for enc in ("utf-8", "gbk", "latin-1"):
        try:
            with open(path, "r", encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, Exception):
            continue
    return ""


def _build_csv_summary(csv_data_list: List[dict]) -> str:
    """构建 CSV 数据摘要（给 LLM 参考）"""
    if not csv_data_list:
        return "(无 CSV 数据)"
    parts = []
    all_teams = set()
    total_matches = 0
    for d in csv_data_list:
        parts.append("- %s: date=%s, teams=%d, matches=%d" % (
            d["file_name"], d["date"], d["num_teams"], d["match_count"]))
        all_teams.update(d["team_names"])
        total_matches += d["match_count"]
    header = "CSV 文件共 %d 个, 总比赛场次 %d, 出现过的队伍 %d 支\n" % (
        len(csv_data_list), total_matches, len(all_teams))
    return header + "\n".join(parts)


def _build_team_ground_truth(csv_data_list: List[dict]) -> str:
    """构建主要队伍的跨赛季汇总统计（给 LLM 做真值参考）"""
    if not csv_data_list:
        return ""
    agg = {}
    for d in csv_data_list:
        for tname, tdata in d["teams"].items():
            if tname not in agg:
                agg[tname] = {
                    "match_wins": 0, "match_losses": 0,
                    "late_count": 0, "forfeit_count": 0,
                    "bo1_wins": 0, "bo1_losses": 0,
                    "bo3_wins": 0, "bo3_losses": 0,
                    "bo5_wins": 0, "bo5_losses": 0,
                    "appearances": 0,
                }
            a = agg[tname]
            a["match_wins"] += tdata["match_wins"]
            a["match_losses"] += tdata["match_losses"]
            a["late_count"] += tdata["late_count"]
            a["forfeit_count"] += tdata["forfeit_count"]
            a["bo1_wins"] += tdata["bo1_wins"]
            a["bo1_losses"] += tdata["bo1_losses"]
            a["bo3_wins"] += tdata["bo3_wins"]
            a["bo3_losses"] += tdata["bo3_losses"]
            a["bo5_wins"] += tdata["bo5_wins"]
            a["bo5_losses"] += tdata["bo5_losses"]
            a["appearances"] += 1

    sorted_teams = sorted(agg.items(),
                          key=lambda x: (-x[1]["appearances"], -x[1]["match_wins"]))
    lines = []
    for tname, t in sorted_teams[:20]:
        total = t["match_wins"] + t["match_losses"]
        wr = (t["match_wins"] / total * 100) if total > 0 else 0
        lines.append(
            "%s: %d赛季, %d场(%d胜%d负, %.1f%%), BO1:%d胜%d负, BO3:%d胜%d负, 迟到:%d, 弃赛:%d"
            % (tname, t["appearances"], total, t["match_wins"], t["match_losses"], wr,
               t["bo1_wins"], t["bo1_losses"], t["bo3_wins"], t["bo3_losses"],
               t["late_count"], t["forfeit_count"]))
    return "\n".join(lines)


# ============================================================================
# 一、文件交付 (10分)
# ============================================================================

def _eval_file_delivery(answer_dir: str) -> Tuple[int, dict]:
    """检查报告文件是否存在且内容充实"""
    details = {}
    score = 0

    report_path = _find_report(answer_dir)
    if not report_path:
        details["报告文件"] = "0/6 — 未找到任何 .md 分析报告文件"
        details["内容长度"] = "0/4 — N/A"
        return 0, {"score": 0, "details": details}

    rel = os.path.relpath(report_path, answer_dir)
    content = _load_file(report_path)
    length = len(content)

    if content and length > 0:
        score += 6
        details["报告文件"] = "6/6 — 找到 %s (%d 字符)" % (rel, length)
    else:
        details["报告文件"] = "0/6 — 文件为空"
        details["内容长度"] = "0/4 — N/A"
        return 0, {"score": 0, "details": details}

    if length >= 8000:
        score += 4
        details["内容长度"] = "4/4 — %d 字符，内容充实" % length
    elif length >= 4000:
        score += 3
        details["内容长度"] = "3/4 — %d 字符，基本充实" % length
    elif length >= 1500:
        score += 2
        details["内容长度"] = "2/4 — %d 字符，偏短" % length
    elif length >= 500:
        score += 1
        details["内容长度"] = "1/4 — %d 字符，过短" % length
    else:
        details["内容长度"] = "0/4 — %d 字符，严重不足" % length

    return min(score, 10), {"score": min(score, 10), "details": details}


# ============================================================================
# 二、报告结构与章节完整性 (15分)
# ============================================================================

def _eval_structure(answer_dir: str) -> Tuple[int, dict]:
    """检查报告是否包含三大必要章节及其子内容"""
    report_path = _find_report(answer_dir)
    if not report_path:
        return 0, {"score": 0, "details": {"错误": "未找到报告"}}

    content = _load_file(report_path)
    if not content:
        return 0, {"score": 0, "details": {"错误": "报告为空"}}

    score = 0
    details = {}

    # 2a. 总体统计 (4分)
    overall_kw = ["总体统计", "总体概况", "赛事概览", "比赛概况",
                  "数据概览", "比赛日期", "参赛队伍", "比赛场次",
                  "队伍数量", "数据文件"]
    found = sum(1 for kw in overall_kw if kw in content)
    if found >= 4:
        s = 4
    elif found >= 2:
        s = 3
    elif found >= 1:
        s = 2
    else:
        s = 0
    score += s
    details["总体统计 (4分)"] = "%d/4 — 命中 %d/%d 个关键词" % (s, found, len(overall_kw))

    # 2b. 队伍详细统计 (7分)
    team_detail_kw = [
        "地图胜率", "赛制胜率", "连胜", "连败",
        "对阵", "对战记录", "BO1", "BO3", "BO5",
        "特殊事件", "迟到", "弃赛", "判负",
    ]
    found = sum(1 for kw in team_detail_kw if kw in content)
    if found >= 7:
        s = 7
    elif found >= 5:
        s = 5
    elif found >= 3:
        s = 4
    elif found >= 1:
        s = 2
    else:
        s = 0
    score += s
    details["队伍详细统计 (7分)"] = "%d/7 — 命中 %d/%d 个关键词" % (s, found, len(team_detail_kw))

    # 2c. 实力预测分析 (4分)
    pred_kw = [
        "实力预测", "预测分析", "实力排名", "排名预测",
        "趋势分析", "改进建议", "优势", "实力评估",
        "未来表现", "综合评估", "走势",
    ]
    found = sum(1 for kw in pred_kw if kw in content)
    if found >= 4:
        s = 4
    elif found >= 2:
        s = 3
    elif found >= 1:
        s = 1
    else:
        s = 0
    score += s
    details["实力预测分析 (4分)"] = "%d/4 — 命中 %d/%d 个关键词" % (s, found, len(pred_kw))

    return min(score, 15), {"score": min(score, 15), "details": details}


# ============================================================================
# 三、统计数据准确性 (40分)
# ============================================================================

def _eval_accuracy(answer_dir: str) -> Tuple[int, dict]:
    """验证报告中的统计数据是否与 CSV 源数据一致"""
    report_path = _find_report(answer_dir)
    if not report_path:
        return 0, {"score": 0, "details": {"错误": "未找到报告"}}

    content = _load_file(report_path)
    if not content:
        return 0, {"score": 0, "details": {"错误": "报告为空"}}

    csv_data_list = _load_all_csv_data()
    score = 0
    details = {}

    # --- 3a. 程序化验证：基本数据正确性 (15分) ---
    prog_score = 0

    # (1) CSV 文件数量 (3分)
    actual_file_count = len(csv_data_list)
    file_count_found = False
    for pattern in [r"(?:数据文件|CSV|文件)[^0-9]*%d" % actual_file_count,
                    r"%d[^0-9]*(?:个|份).*(?:文件|CSV|数据)" % actual_file_count]:
        if re.search(pattern, content):
            file_count_found = True
            break
    if not file_count_found and str(actual_file_count) in content:
        file_count_found = True

    if file_count_found:
        prog_score += 3
        details["CSV文件数 (3分)"] = "3/3 — 正确识别 %d 个文件" % actual_file_count
    else:
        details["CSV文件数 (3分)"] = "0/3 — 未找到正确的文件数量 %d" % actual_file_count

    # (2) 主要队伍名覆盖 (5分)
    team_appearances = defaultdict(int)
    for d in csv_data_list:
        for t in d["team_names"]:
            team_appearances[t] += 1
    major_teams = [t for t, c in team_appearances.items() if c >= 3]
    if not major_teams:
        major_teams = [t for t, c in team_appearances.items() if c >= 2]

    if major_teams:
        found_count = sum(1 for t in major_teams if t in content)
        ratio = found_count / len(major_teams) if major_teams else 0
        if ratio >= 0.7:
            s = 5
        elif ratio >= 0.5:
            s = 4
        elif ratio >= 0.3:
            s = 3
        elif ratio >= 0.1:
            s = 2
        else:
            s = 0
        prog_score += s
        details["主要队伍覆盖 (5分)"] = "%d/5 — 覆盖 %d/%d 个主要队伍(%.0f%%)" % (
            s, found_count, len(major_teams), ratio * 100)
    else:
        details["主要队伍覆盖 (5分)"] = "0/5 — 无法确定主要队伍"

    # (3) 总比赛场次 (3分)
    total_matches = sum(d["match_count"] for d in csv_data_list)
    match_score = 0
    if str(total_matches) in content:
        match_score = 3
    else:
        for delta in range(-5, 6):
            if delta != 0 and str(total_matches + delta) in content:
                match_score = 1
                break
    prog_score += match_score
    details["总比赛场次 (3分)"] = "%d/3 — %s (实际 %d)" % (
        match_score,
        "正确" if match_score == 3 else ("接近" if match_score == 1 else "未找到"),
        total_matches)

    # (4) 比赛日期正确性 (4分)
    dates_found = 0
    for d in csv_data_list:
        date_str = d["date"]
        parts = date_str.split("-")
        found_this = False
        # Various date formats
        checks = [
            date_str,
            "%s年%s月%s日" % (parts[0], int(parts[1]), int(parts[2])),
            "%s年%02d月%02d日" % (parts[0], int(parts[1]), int(parts[2])),
            "%s/%s/%s" % (parts[0], int(parts[1]), int(parts[2])),
            "%s-%s-%s" % (parts[0], int(parts[1]), int(parts[2])),
        ]
        for check in checks:
            if check in content:
                found_this = True
                break
        if found_this:
            dates_found += 1

    if dates_found >= 5:
        date_s = 4
    elif dates_found >= 3:
        date_s = 3
    elif dates_found >= 1:
        date_s = 2
    else:
        date_s = 0
    prog_score += date_s
    details["比赛日期 (4分)"] = "%d/4 — 找到 %d/%d 个日期" % (
        date_s, dates_found, len(csv_data_list))

    prog_score = min(prog_score, 15)
    details["程序化验证小计"] = "%d/15" % prog_score

    # --- 3b. LLM-as-Judge 验证数据一致性 (25分) ---
    csv_summary = _build_csv_summary(csv_data_list)
    ground_truth = _build_team_ground_truth(csv_data_list)
    config = _get_text_eval_config(answer_dir)
    llm_score = 0

    if config.get("api_key") and openai:
        prompt = """你是电竞数据分析评审专家。请对比 CSV 源数据摘要与分析报告，评估报告的数据准确性。

## CSV 源数据摘要
%s

## 主要队伍统计真值（跨赛季汇总）
%s

## 待评估的报告内容（前 15000 字符）
%s

## 评分要求
请从以下 5 个子维度各给 0-5 分，共 25 分：

1. **总体数据一致性** (0-5): 文件数、队伍数、总场次等宏观数据是否与源数据一致
2. **胜率数据准确性** (0-5): 各队伍总胜率、各赛制(BO1/BO3/BO5)胜率是否合理
3. **地图统计准确性** (0-5): 地图胜率统计是否有具体地图名和数值，是否合理
4. **对阵历史完整性** (0-5): 是否统计了队伍间对战记录，数据是否合理
5. **特殊事件准确性** (0-5): 迟到/弃赛/判负统计是否有涉及且数据合理

评分原则：
- 报告中完全没涉及某个维度 → 0 分
- 有涉及但数据明显错误或不完整 → 1-2 分
- 数据基本正确但有小误差 → 3-4 分
- 数据完全正确且详细 → 5 分

请严格按以下 JSON 格式返回：
```json
{
    "overall_consistency": {"score": 0, "reason": ""},
    "win_rate_accuracy": {"score": 0, "reason": ""},
    "map_stats_accuracy": {"score": 0, "reason": ""},
    "matchup_completeness": {"score": 0, "reason": ""},
    "special_events": {"score": 0, "reason": ""}
}
```""" % (csv_summary[:3000], ground_truth[:4000], content[:15000])

        result = _call_llm_judge(prompt, config)
        if result:
            parsed = _parse_json_from_llm(result)
            if parsed:
                dims = [
                    ("overall_consistency", "总体数据一致性"),
                    ("win_rate_accuracy", "胜率数据准确性"),
                    ("map_stats_accuracy", "地图统计准确性"),
                    ("matchup_completeness", "对阵历史完整性"),
                    ("special_events", "特殊事件准确性"),
                ]
                for key, label in dims:
                    d = parsed.get(key, {})
                    raw = d.get("score", 0)
                    if isinstance(raw, str):
                        try:
                            raw = int(raw)
                        except ValueError:
                            raw = 0
                    s = max(0, min(5, int(raw)))
                    llm_score += s
                    reason = d.get("reason", "")
                    details["LLM-%s (5分)" % label] = "%d/5 — %s" % (s, reason[:150])
                llm_score = min(llm_score, 25)
                details["LLM评估小计"] = "%d/25" % llm_score
            else:
                details["LLM评估"] = "JSON 解析失败，使用回退评分"
                llm_score = _accuracy_fallback_score(content)
                details["LLM回退评分"] = "%d/25" % llm_score
        else:
            details["LLM评估"] = "LLM 调用失败，使用回退评分"
            llm_score = _accuracy_fallback_score(content)
            details["LLM回退评分"] = "%d/25" % llm_score
    else:
        details["LLM评估"] = "LLM 不可用，使用回退评分"
        llm_score = _accuracy_fallback_score(content)
        details["LLM回退评分"] = "%d/25" % llm_score

    total = prog_score + llm_score
    total = min(total, 40)
    return total, {"score": total, "details": details}


def _accuracy_fallback_score(content: str) -> int:
    """LLM 不可用时的回退评分（保守，最高 15/25）"""
    score = 0
    terms = {"胜率": 2, "BO1": 1, "BO3": 1, "BO5": 1,
             "连胜": 1, "地图": 1, "对阵": 1, "迟到": 1, "弃赛": 1}
    for kw, pts in terms.items():
        if kw in content:
            score += pts

    pct_count = len(re.findall(r"\d+\.?\d*%", content))
    if pct_count >= 30:
        score += 3
    elif pct_count >= 10:
        score += 2
    elif pct_count >= 3:
        score += 1

    table_rows = len(re.findall(r"\|.*\|.*\|", content))
    if table_rows >= 20:
        score += 3
    elif table_rows >= 5:
        score += 2

    return min(score, 15)


# ============================================================================
# 四、预测分析质量 (20分) — LLM-as-Judge
# ============================================================================

def _eval_prediction(answer_dir: str) -> Tuple[int, dict]:
    """评估实力预测分析部分的质量"""
    report_path = _find_report(answer_dir)
    if not report_path:
        return 0, {"score": 0, "details": {"错误": "未找到报告"}}

    content = _load_file(report_path)
    if not content:
        return 0, {"score": 0, "details": {"错误": "报告为空"}}

    config = _get_text_eval_config(answer_dir)
    details = {}

    if config.get("api_key") and openai:
        prompt = """你是电竞数据分析专家。请评估以下比赛统计报告中"实力预测分析"部分的质量。

## 报告内容（前 15000 字符）
%s

## 评估维度（共 20 分）

1. **排名预测合理性** (0-8):
   - 是否基于统计数据给出了明确的队伍实力排名？
   - 排名是否与报告中的胜率/战绩数据一致？
   - 是否有具体的评分或积分数值支撑排名？
   - 8: 排名合理且有详细数据支撑
   - 4-7: 有排名但部分缺少支撑
   - 1-3: 有排名但缺乏数据依据
   - 0: 完全没有排名预测

2. **趋势分析深度** (0-6):
   - 是否分析了队伍跨赛季的表现变化？
   - 是否使用了不同赛季的数据对比？
   - 6: 详细的跨赛季趋势分析
   - 3-5: 有一定趋势分析
   - 1-2: 简单提及趋势
   - 0: 无趋势分析

3. **改进建议具体性** (0-6):
   - 是否为主要队伍提供了具体的优势和改进方向？
   - 建议是否基于具体数据（如地图偏好、赛制适应性）？
   - 6: 针对多支队伍的具体可操作建议
   - 3-5: 有建议但泛泛而谈
   - 1-2: 非常笼统的建议
   - 0: 无建议

请严格按以下 JSON 格式返回：
```json
{
    "ranking_quality": {"score": 0, "reason": ""},
    "trend_analysis": {"score": 0, "reason": ""},
    "suggestion_quality": {"score": 0, "reason": ""}
}
```""" % content[:15000]

        result = _call_llm_judge(prompt, config)
        if result:
            parsed = _parse_json_from_llm(result)
            if parsed:
                score = 0
                dims = [
                    ("ranking_quality", "排名预测合理性", 8),
                    ("trend_analysis", "趋势分析深度", 6),
                    ("suggestion_quality", "建议具体性", 6),
                ]
                for key, label, maxs in dims:
                    d = parsed.get(key, {})
                    raw = d.get("score", 0)
                    if isinstance(raw, str):
                        try:
                            raw = int(raw)
                        except ValueError:
                            raw = 0
                    s = max(0, min(maxs, int(raw)))
                    score += s
                    reason = d.get("reason", "")
                    details["%s (%d分)" % (label, maxs)] = "%d/%d — %s" % (
                        s, maxs, reason[:150])
                score = min(score, 20)
                return score, {"score": score, "details": details}

    # Fallback
    return _prediction_fallback(content)


def _prediction_fallback(content: str) -> Tuple[int, dict]:
    """LLM 不可用时的预测评估回退"""
    score = 0
    details = {}

    has_ranking = bool(re.search(r"第[一二三四五六七八九十\d]+名", content)) or \
                  bool(re.search(r"排名.*[:：]", content))
    has_score_val = bool(re.search(r"积分|得分|评分|rating", content, re.IGNORECASE))
    rank_s = 0
    if has_ranking:
        rank_s += 4
    if has_score_val:
        rank_s += 2
    rank_s = min(rank_s, 8)
    score += rank_s
    details["排名预测 (8分)"] = "%d/8" % rank_s

    trend_kw = ["趋势", "走势", "变化", "提升", "下降", "进步", "退步", "跨赛季"]
    trend_found = sum(1 for kw in trend_kw if kw in content)
    trend_s = min(trend_found * 2, 6)
    score += trend_s
    details["趋势分析 (6分)"] = "%d/6" % trend_s

    sug_kw = ["建议", "改进", "优势", "劣势", "加强", "提高", "侧重"]
    sug_found = sum(1 for kw in sug_kw if kw in content)
    sug_s = min(sug_found * 2, 6)
    score += sug_s
    details["建议具体性 (6分)"] = "%d/6" % sug_s

    score = min(score, 20)
    details["注意"] = "LLM 不可用，使用关键词回退评分"
    return score, {"score": score, "details": details}


# ============================================================================
# 五、报告格式与可读性 (15分)
# ============================================================================

def _eval_readability(answer_dir: str) -> Tuple[int, dict]:
    """评估报告的 Markdown 格式质量和可读性"""
    report_path = _find_report(answer_dir)
    if not report_path:
        return 0, {"score": 0, "details": {"错误": "未找到报告"}}

    content = _load_file(report_path)
    if not content:
        return 0, {"score": 0, "details": {"错误": "报告为空"}}

    score = 0
    details = {}

    # 5a. 标题层次 (4分)
    h1_count = len(re.findall(r"^# ", content, re.MULTILINE))
    h2_count = len(re.findall(r"^## ", content, re.MULTILINE))
    h3_count = len(re.findall(r"^### ", content, re.MULTILINE))

    if h2_count >= 3 and h3_count >= 3:
        s = 4
    elif h2_count >= 3 or (h2_count >= 2 and h3_count >= 2):
        s = 3
    elif h2_count >= 2 or h3_count >= 2:
        s = 2
    elif h2_count >= 1 or h3_count >= 1:
        s = 1
    else:
        s = 0
    score += s
    details["标题层次 (4分)"] = "%d/4 — H1:%d H2:%d H3:%d" % (s, h1_count, h2_count, h3_count)

    # 5b. 表格使用 (4分)
    table_rows = len(re.findall(r"^\|.+\|.+\|", content, re.MULTILINE))
    if table_rows >= 30:
        s = 4
    elif table_rows >= 10:
        s = 3
    elif table_rows >= 3:
        s = 2
    elif table_rows >= 1:
        s = 1
    else:
        s = 0
    score += s
    details["表格使用 (4分)"] = "%d/4 — %d 行表格" % (s, table_rows)

    # 5c. 列表使用 (3分)
    has_ul = bool(re.search(r"^\s*[-*+]\s", content, re.MULTILINE))
    has_ol = bool(re.search(r"^\s*\d+\.\s", content, re.MULTILINE))
    ul_count = len(re.findall(r"^\s*[-*+]\s", content, re.MULTILINE))

    if has_ul and has_ol and ul_count >= 10:
        s = 3
    elif has_ul and ul_count >= 5:
        s = 2
    elif has_ul or has_ol:
        s = 1
    else:
        s = 0
    score += s
    details["列表使用 (3分)"] = "%d/3 — 无序:%d 有序:%s" % (
        s, ul_count, "有" if has_ol else "无")

    # 5d. 数据密度 (4分)
    pct_count = len(re.findall(r"\d+\.?\d*%", content))
    wl_count = len(re.findall(r"\d+胜\d+负", content))
    num_count = pct_count + wl_count

    if num_count >= 40:
        s = 4
    elif num_count >= 20:
        s = 3
    elif num_count >= 8:
        s = 2
    elif num_count >= 3:
        s = 1
    else:
        s = 0
    score += s
    details["数据密度 (4分)"] = "%d/4 — 百分比:%d 胜负记录:%d" % (s, pct_count, wl_count)

    return min(score, 15), {"score": min(score, 15), "details": details}


# ============================================================================
# 主函数
# ============================================================================

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    评估 agent 的输出。

    Args:
        answer_dir: agent 输出目录的绝对路径

    Returns:
        (score, report) — score: 0-100 的整数, report: 详细评估报告
    """
    s1, r1 = _eval_file_delivery(answer_dir)
    s2, r2 = _eval_structure(answer_dir)
    s3, r3 = _eval_accuracy(answer_dir)
    s4, r4 = _eval_prediction(answer_dir)
    s5, r5 = _eval_readability(answer_dir)

    total = s1 + s2 + s3 + s4 + s5
    total = max(0, min(100, total))

    report = {
        "total": total,
        "dimensions": {
            "一、文件交付 (10分)": r1,
            "二、报告结构 (15分)": r2,
            "三、统计准确性 (40分)": r3,
            "四、预测质量 (20分)": r4,
            "五、格式可读性 (15分)": r5,
        },
        "breakdown": {
            "文件交付": "%d/10" % s1,
            "报告结构": "%d/15" % s2,
            "统计准确性": "%d/40" % s3,
            "预测质量": "%d/20" % s4,
            "格式可读性": "%d/15" % s5,
        },
    }

    if total >= 90:
        report["comment"] = "优秀！报告数据完整准确，预测合理，格式规范。"
    elif total >= 75:
        report["comment"] = "良好。报告整体质量不错，部分维度可进一步完善。"
    elif total >= 60:
        report["comment"] = "及格。完成了基本要求，但准确性或预测部分有待提升。"
    elif total >= 40:
        report["comment"] = "部分完成。报告有一定内容但存在明显不足。"
    else:
        report["comment"] = "不及格。报告缺失严重或内容质量较差。"

    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """打印格式化的评分报告"""
    print("=" * 70)
    print("pengyichen-query5 评分报告")
    print("任务：比赛数据统计分析与实力预测报告")
    print("=" * 70)
    print("\n总分：%d/100\n" % score)

    breakdown = report.get("breakdown", {})
    if breakdown:
        print("分项得分：")
        for k, v in breakdown.items():
            print("  %s: %s" % (k, v))
        print()

    for dim_name, dim_data in report.get("dimensions", {}).items():
        print("-" * 55)
        print("【%s】得分: %d" % (dim_name, dim_data.get("score", 0)))
        print("-" * 55)
        for k, v in dim_data.get("details", {}).items():
            text = str(v)
            if len(text) > 200:
                text = text[:200] + "..."
            print("  %s: %s" % (k, text))
        print()

    print("=" * 55)
    print("评语：%s" % report.get("comment", ""))
    print("=" * 70)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        test_dir = sys.argv[1]
    else:
        test_dir = os.path.join(os.path.dirname(__file__), "..", "gpt-5", "attempt_1")

    if not os.path.isabs(test_dir):
        test_dir = os.path.join(os.getcwd(), test_dir)

    if os.path.exists(test_dir):
        print("Evaluating: %s\n" % test_dir)
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print("Directory not found: %s" % test_dir)
    sys.exit(0)
