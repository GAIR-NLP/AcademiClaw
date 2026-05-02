"""
川西社会实践动态重规划与审计决策 — 评分脚本 (从零重写)
总分 100 分

任务概述:
  8人大学生社会实践团，7天川西学术调研，预算20000元。
  Phase A: 基于初始数据设计理塘-稻城7天方案（海拔递进安全、住宿合规）
  Phase B: 第4天(7/4) G318桥断，从雅江出发重新规划D4-D7

评分维度:
  一、文件交付完整性 (10分)
    1.1 执行档案存在 (4分)
    1.2 财务审计报告存在 (3分)
    1.3 Python 决策代码存在 (3分)

  二、财务审计与预算合规 (30分)
    2.1 总预算不超标 (8分): 总支出 <= 20000
    2.2 酒店退改损失核算 (12分): LT01/DC02/DC03 退改逻辑
    2.3 开支明细完整性 (10分): LLM 检查逐项列支与自洽

  三、危机决策与安全合理性 (30分)
    3.1 识别G318中断并放弃理塘/稻城 (10分)
    3.2 路线重构可行性 (10分): S215/塔公/新都桥/四姑娘山 等
    3.3 安全保障措施 (10分): 氧气、海拔递进、应急预案、医疗

  四、方案完整性与学术质量 (30分) — LLM
    4.1 Phase A 初始规划 (12分): 完整7天计划、海拔递进合理、住宿合规
    4.2 Phase B 重构方案 (12分): D4-D7 新行程闭环回成都
    4.3 学术主题切换 (6分): 合理调整调研主题与理由
"""

import os
import re
import json
from typing import Tuple, Dict, Any, List

try:
    import openai
except ImportError:
    openai = None


# =============================================================================
# 环境配置
# =============================================================================

def _load_env(answer_dir: str) -> dict:
    """从 answer_dir 和 query 根目录加载 .env 配置"""
    values = {}
    eval_dir = os.path.dirname(os.path.abspath(__file__))
    query_dir = os.path.join(eval_dir, "..")
    for env_dir in [answer_dir, query_dir]:
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
            max_tokens=2048,
            temperature=0,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        print(f"[RUBRIC] LLM Judge 调用失败: {e}")
        return ""


def _parse_llm_json(text: str) -> dict:
    """解析 LLM 返回的 JSON"""
    if not text:
        return {}
    cleaned = re.sub(r"^```json\s*", "", text.strip())
    cleaned = re.sub(r"\s*```$", "", cleaned.strip())
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        m = re.search(r'\{[^{}]*\}', text, re.DOTALL)
        if m:
            try:
                return json.loads(m.group())
            except json.JSONDecodeError:
                pass
    return {}


# =============================================================================
# 文件辅助
# =============================================================================

def _list_files(answer_dir: str) -> Dict[str, List[str]]:
    """列出 answer_dir 中的文件，按类型分类"""
    if not os.path.isdir(answer_dir):
        return {"all": [], "md": [], "py": [], "txt": []}
    all_files = os.listdir(answer_dir)
    md = [f for f in all_files if f.lower().endswith(".md")]
    py = [f for f in all_files if f.lower().endswith(".py")]
    txt = [f for f in all_files if f.lower().endswith(".txt")]
    return {"all": all_files, "md": md, "py": py, "txt": txt}


def _read_file(path: str, max_chars: int = 30000) -> str:
    """安全读取文件内容"""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read(max_chars)
    except Exception:
        return ""


def _find_doc_by_keywords(answer_dir: str, files: List[str],
                          positive_kw: List[str],
                          negative_kw: List[str] = None) -> str:
    """根据关键词从文件列表中找到最匹配的文档内容"""
    if negative_kw is None:
        negative_kw = []
    candidates = []
    for f in files:
        content = _read_file(os.path.join(answer_dir, f))
        pos_score = sum(1 for kw in positive_kw
                        if kw.lower() in content.lower() or kw.lower() in f.lower())
        neg_score = sum(1 for kw in negative_kw
                        if kw.lower() in content.lower() or kw.lower() in f.lower())
        net = pos_score - neg_score * 3
        candidates.append((f, net, len(content), content))
    if not candidates:
        return ""
    candidates.sort(key=lambda x: (x[1], x[2]), reverse=True)
    best = candidates[0]
    if best[1] > 0 or best[2] > 500:
        return best[3]
    return ""


def _collect_all_text(answer_dir: str, files: Dict[str, List[str]]) -> str:
    """收集所有文本内容供综合分析"""
    parts = []
    for f in files["md"] + files["txt"]:
        content = _read_file(os.path.join(answer_dir, f), max_chars=10000)
        if content:
            parts.append(f"=== {f} ===\n{content}")
    for f in files["py"]:
        content = _read_file(os.path.join(answer_dir, f), max_chars=8000)
        if content:
            parts.append(f"=== {f} (Python) ===\n{content}")
    return "\n\n".join(parts)


# =============================================================================
# 一、文件交付完整性 (10分)
# =============================================================================

def _eval_file_delivery(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """检查三类交付物是否存在"""
    score = 0
    details = {}
    files = _list_files(answer_dir)

    # 1.1 执行档案 (4分) — Markdown/txt 文件中包含行程/方案/执行相关内容
    archive_kw = ["执行档案", "全流程", "archive", "plan", "execution", "行程",
                  "方案", "Phase A", "D1", "第1天", "Day 1"]
    found_archive = False
    for f in files["md"] + files["txt"]:
        content = _read_file(os.path.join(answer_dir, f), max_chars=3000)
        hits = sum(1 for kw in archive_kw if kw.lower() in content.lower() or kw in f)
        if hits >= 2 or (len(content) > 800 and hits >= 1):
            found_archive = True
            break

    if found_archive:
        score += 4
        details["1.1 执行档案"] = "4/4 - 找到执行档案"
    elif files["md"]:
        score += 1
        details["1.1 执行档案"] = "1/4 - 有 Markdown 文件但未识别为执行档案"
    else:
        details["1.1 执行档案"] = "0/4 - 未找到执行档案"

    # 1.2 财务审计报告 (3分)
    fin_kw = ["财务", "审计", "financial", "audit", "预算", "开支", "budget"]
    found_financial = False
    for f in files["md"] + files["txt"]:
        content = _read_file(os.path.join(answer_dir, f), max_chars=2000)
        if any(kw in f or kw in content for kw in fin_kw):
            found_financial = True
            break

    if found_financial:
        score += 3
        details["1.2 财务审计报告"] = "3/3 - 找到财务审计报告"
    elif len(files["md"]) >= 2:
        score += 1
        details["1.2 财务审计报告"] = "1/3 - 有多个文档但未识别财务报告"
    else:
        details["1.2 财务审计报告"] = "0/3 - 未找到财务审计报告"

    # 1.3 Python 代码 (3分)
    if files["py"]:
        has_meaningful = False
        for f in files["py"]:
            content = _read_file(os.path.join(answer_dir, f), max_chars=5000)
            if len(content) > 200:
                has_meaningful = True
                break
        if has_meaningful:
            score += 3
            details["1.3 Python 代码"] = f"3/3 - 找到: {', '.join(files['py'][:3])}"
        else:
            score += 1
            details["1.3 Python 代码"] = "1/3 - Python 文件存在但内容过少"
    else:
        details["1.3 Python 代码"] = "0/3 - 未找到 Python 代码文件"

    return score, details


# =============================================================================
# 二、财务审计与预算合规 (30分)
# =============================================================================

def _eval_financial(answer_dir: str, config: dict) -> Tuple[int, Dict[str, Any]]:
    """评估财务审计的准确性和完整性"""
    score = 0
    details = {}
    files = _list_files(answer_dir)

    # 找财务文档
    fin_kw = ["财务", "审计", "financial", "audit", "预算", "开支", "budget", "合计"]
    neg_kw = ["执行档案", "学术", "研究", "成果", "research"]
    financial_text = _find_doc_by_keywords(
        answer_dir, files["md"] + files["txt"], fin_kw, neg_kw)

    if not financial_text:
        all_text = _collect_all_text(answer_dir, files)
        if not all_text:
            return 0, {"error": "未找到任何文本输出"}
        financial_text = all_text

    # ─── 2.1 总预算不超标 (8分) ─── 规则检查
    budget_pattern = re.compile(
        r'(?:合计|总[计额支花销]|Total|总支出|净额|实际支出)[^\d]*?'
        r'(\d[\d,]*(?:\.\d+)?)',
        re.IGNORECASE
    )
    budget_match = budget_pattern.search(financial_text)
    total_amount = None
    if budget_match:
        try:
            total_amount = float(budget_match.group(1).replace(',', ''))
        except ValueError:
            pass

    if total_amount is not None:
        if total_amount <= 20000:
            score += 8
            details["2.1 预算不超标"] = f"8/8 - 总支出 {total_amount:.0f} 元 <= 20000 元"
        elif total_amount <= 22000:
            score += 3
            details["2.1 预算不超标"] = f"3/8 - 总支出 {total_amount:.0f} 元，略超支"
        else:
            details["2.1 预算不超标"] = f"0/8 - 总支出 {total_amount:.0f} 元，严重超支"
    else:
        # 尝试从所有金额推断
        nums = re.findall(r'(\d[\d,]*(?:\.\d+)?)\s*元', financial_text)
        big_nums = []
        for n in nums:
            try:
                val = float(n.replace(',', ''))
                if val > 5000:
                    big_nums.append(val)
            except ValueError:
                pass
        if big_nums and max(big_nums) <= 20000:
            score += 4
            details["2.1 预算不超标"] = "4/8 - 无明确总计行，但检测到金额 <= 20000"
        elif big_nums:
            score += 2
            details["2.1 预算不超标"] = "2/8 - 有金额数据但无法确定是否超支"
        else:
            details["2.1 预算不超标"] = "0/8 - 未找到金额数据"

    # ─── 2.2 酒店退改损失核算 (12分) ─── 规则检查
    # 参考答案:
    #   LT01: 1920预付, 不可抗力80%退款-4间*50手续费 = 1920*0.8-200 = 1336退款, 584损失 (4分)
    #   DC02: 1520预付, 7/4 14:00前免费取消 = 全额退回 (4分)
    #   DC03: 1680预付, 不可退 = 全损 (4分)

    # LT01 理塘酒店 (4分)
    lt01_score = 0
    if re.search(r'584', financial_text):
        lt01_score = 4
        details["2.2a LT01 理塘"] = "4/4 - 正确计算损失 584 元"
    elif re.search(r'560', financial_text):
        lt01_score = 3
        details["2.2a LT01 理塘"] = "3/4 - 损失约 560 元（参考值 584 元）"
    elif re.search(r'1336', financial_text):
        lt01_score = 3
        details["2.2a LT01 理塘"] = "3/4 - 正确计算退款 1336 元（但未明确显示损失）"
    elif ("1920" in financial_text and
          ("20%" in financial_text or "80%" in financial_text or "不可抗力" in financial_text)):
        lt01_score = 2
        details["2.2a LT01 理塘"] = "2/4 - 提到计算逻辑但结果不明确"
    elif "LT01" in financial_text or "理塘" in financial_text:
        lt01_score = 1
        details["2.2a LT01 理塘"] = "1/4 - 提及理塘酒店但未正确核算"
    else:
        details["2.2a LT01 理塘"] = "0/4 - 未提及理塘酒店退改"

    # DC02 稻城圣地影像 (4分)
    dc02_score = 0
    if re.search(r'(?:免费取消|全额退|free.*cancel|1520.*退|DC02.*退|退.*1520)',
                 financial_text, re.IGNORECASE):
        dc02_score = 4
        details["2.2b DC02 稻城"] = "4/4 - 正确识别免费取消/全额退款"
    elif "DC02" in financial_text or "圣地影像" in financial_text:
        dc02_score = 1
        details["2.2b DC02 稻城"] = "1/4 - 提及但未明确免费取消"
    else:
        details["2.2b DC02 稻城"] = "0/4 - 未提及 DC02"

    # DC03 香格里拉镇 (4分)
    dc03_score = 0
    if re.search(r'(?:不可退|Non.?Refund|1680.*损|DC03.*损|全损|不可退.*1680|1680.*不可退)',
                 financial_text, re.IGNORECASE):
        dc03_score = 4
        details["2.2c DC03 香格里拉镇"] = "4/4 - 正确识别不可退/全额损失 1680 元"
    elif "1680" in financial_text:
        dc03_score = 2
        details["2.2c DC03 香格里拉镇"] = "2/4 - 提到 1680 元但未明确不可退"
    elif "DC03" in financial_text or "日松" in financial_text or "香格里拉" in financial_text:
        dc03_score = 1
        details["2.2c DC03 香格里拉镇"] = "1/4 - 提及但未核算损失"
    else:
        details["2.2c DC03 香格里拉镇"] = "0/4 - 未提及 DC03"

    hotel_cancel_score = lt01_score + dc02_score + dc03_score
    score += hotel_cancel_score

    # ─── 2.3 开支明细完整性 (10分) ─── LLM Judge
    llm_prompt = f"""你是一位严格的财务审计评估员。请评估以下财务审计报告的完整性和准确性。

### 背景
- 8人大学生社会实践团，7天川西调研
- 总预算 20000 元
- 第4天 G318 桥断，需要重新规划，产生酒店退改损失
- 住宿标准：200元/人/天（即 ≤400 元/间，2人1间，需增值税发票）
- 伙食补助：60元/人/天，不凭票
- 交通：合规营运车辆，需增值税专用发票

### 需要检查的退改项
- LT01 理塘丁真珍珠大酒店: 预付1920元, 不可抗力退80%但每间扣50元手续费, 损失约584元
- DC02 圣地影像精品酒店: 预付1520元, 14:00前免费取消, 应全额退回
- DC03 香格里拉镇日松贡布酒店: 预付1680元, 不可退

### Agent 提交的财务报告内容
{financial_text[:8000]}

### 评分标准 (0-10分)
- 9-10: 开支逐日逐项列出（住宿/交通/伙食/退改损失），有合计行，金额内部自洽，注明合规依据
- 6-8: 主要开支项列出但缺少部分细节（如某日住宿缺价格或缺退改明细）
- 3-5: 有部分开支信息但不完整，格式混乱或遗漏重要项
- 0-2: 几乎没有具体开支明细

请严格输出 JSON: {{"score": 0, "reason": ""}}"""

    llm_raw = _call_llm_judge(llm_prompt, config)
    llm_result = _parse_llm_json(llm_raw)
    if llm_result and "score" in llm_result:
        s23 = max(0, min(10, int(llm_result["score"])))
        score += s23
        details["2.3 明细完整性 (LLM)"] = f"{s23}/10 - {llm_result.get('reason', '')[:120]}"
    else:
        # fallback: 统计开支条目数量
        expense_lines = len(re.findall(
            r'[\-\•\|]\s*.*?[\d,]+\.?\d*\s*元', financial_text))
        if expense_lines >= 10:
            s23 = 7
        elif expense_lines >= 6:
            s23 = 5
        elif expense_lines >= 3:
            s23 = 3
        elif expense_lines >= 1:
            s23 = 1
        else:
            s23 = 0
        score += s23
        details["2.3 明细完整性 (fallback)"] = (
            f"{s23}/10 - 检测到 {expense_lines} 条开支记录 (LLM 不可用)")

    return score, details


# =============================================================================
# 三、危机决策与安全合理性 (30分)
# =============================================================================

def _eval_crisis_decision(answer_dir: str, config: dict) -> Tuple[int, Dict[str, Any]]:
    """评估面对 G318 中断时的决策合理性和安全措施"""
    score = 0
    details = {}
    files = _list_files(answer_dir)
    all_text = _collect_all_text(answer_dir, files)

    if not all_text:
        return 0, {"error": "未找到任何文本输出"}

    # ─── 3.1 识别 G318 中断并放弃理塘/稻城 (10分) ───
    # 危险信号: 仍计划强行前往
    danger_words = ["继续前往理塘", "强行通过", "死守原路线", "不顾封锁",
                    "强闯", "强行前往", "冒险通过"]
    found_danger = [w for w in danger_words if w in all_text]

    # 放弃信号
    abandon_patterns = [
        r"放弃理塘", r"取消理塘", r"不前往理塘", r"改道", r"绕行",
        r"无法前往理塘", r"无法抵达理塘", r"G318.*中断", r"桥梁.*移位",
        r"塌方", r"封路", r"禁行", r"不可通行", r"路线重构",
    ]
    found_abandon = any(re.search(pat, all_text) for pat in abandon_patterns)

    if found_danger:
        score += 0
        details["3.1 放弃理塘/稻城"] = f"0/10 - 发现危险决策: {found_danger[:2]}"
    elif found_abandon:
        score += 10
        details["3.1 放弃理塘/稻城"] = "10/10 - 正确识别路况问题并放弃理塘/稻城"
    else:
        # 检查 Phase B 部分是否隐含放弃
        phase_b_text = ""
        for marker in ["Phase B", "重构", "重规划", "D4", "第4天", "7月4日", "动态"]:
            idx = all_text.find(marker)
            if idx >= 0:
                phase_b_text = all_text[idx:]
                break
        if phase_b_text and "理塘" not in phase_b_text:
            score += 6
            details["3.1 放弃理塘/稻城"] = "6/10 - Phase B 中未提及理塘（隐含放弃）"
        else:
            score += 2
            details["3.1 放弃理塘/稻城"] = "2/10 - 未明确说明放弃理塘"

    # ─── 3.2 路线重构可行性 (10分) ─── 规则 + LLM
    reroute_destinations = ["塔公", "新都桥", "四姑娘山", "泸定", "丹巴",
                            "日隆", "小金", "映秀", "海螺沟"]
    reroute_roads = ["S215", "G350"]
    found_dest = [r for r in reroute_destinations if r in all_text]
    found_road = [r for r in reroute_roads if r in all_text]

    # 基础分: 有备选目的地 (5分)
    if len(found_dest) >= 3:
        dest_score = 5
    elif len(found_dest) >= 2:
        dest_score = 4
    elif len(found_dest) >= 1:
        dest_score = 2
    else:
        dest_score = 0
    details["3.2a 备选地点"] = (
        f"{dest_score}/5 - 提及: {', '.join(found_dest) if found_dest else '无'}")

    # LLM 评估路线合理性 (5分)
    route_prompt = f"""请评估以下川西社会实践方案中路线重构的合理性。

### 背景
2026年7月4日上午9:30，G318雅江至理塘段桥梁因塌方禁行（≥72小时）。
团队(8人)当前在雅江县，需要重新规划D4-D7(共4天)。
可用路线：S215 雅江->塔公/新都桥(已开放)，G350 映秀->四姑娘山(开放)。
不可用：G318 雅江->理塘 (禁行)。

### Agent 的重构方案
{all_text[:8000]}

### 评分 (0-5分)
- 5: 新路线全部使用可通行道路，目的地海拔安全(循序渐进)，行程闭环最终回成都
- 3-4: 基本合理但有小问题（如海拔跳跃、未明确返程路线）
- 1-2: 路线勉强可行但存在明显问题
- 0: 路线不合理或仍前往封路区域

请严格输出 JSON: {{"score": 0, "reason": ""}}"""

    llm_raw = _call_llm_judge(route_prompt, config)
    llm_result = _parse_llm_json(llm_raw)
    if llm_result and "score" in llm_result:
        route_llm_score = max(0, min(5, int(llm_result["score"])))
        details["3.2b 路线合理性 (LLM)"] = (
            f"{route_llm_score}/5 - {llm_result.get('reason', '')[:120]}")
    else:
        # fallback: 有备选道路得分
        route_llm_score = min(3, len(found_road) * 2) if found_dest else 0
        details["3.2b 路线合理性 (fallback)"] = (
            f"{route_llm_score}/5 - 道路: {', '.join(found_road) if found_road else '无'} (LLM 不可用)")

    score += dest_score + route_llm_score

    # ─── 3.3 安全保障措施 (10分) ─── 规则检查
    safety_checklist = {
        "氧气配备": ["氧气", "oxygen", "氧气瓶", "便携氧", "氧气罐"],
        "海拔递进": ["海拔", "altitude", "适应", "2560", "2530", "循序渐进",
                    "首晚", "第一晚", "逐级"],
        "应急预案": ["应急", "预案", "emergency", "撤退", "预留", "机动经费"],
        "医院/医疗": ["医院", "医疗", "急救", "hospital", "救治", "卫生院",
                    "华西", "甘孜州人民医院"],
        "健康监测": ["血氧", "心率", "健康监测", "高反", "高原反应"],
    }
    found_items = []
    for item, keywords in safety_checklist.items():
        if any(kw in all_text for kw in keywords):
            found_items.append(item)

    safety_score = min(10, len(found_items) * 2)
    score += safety_score
    details["3.3 安全保障"] = (
        f"{safety_score}/10 - 涵盖 {len(found_items)}/5: "
        f"{', '.join(found_items) if found_items else '无'}")

    return score, details


# =============================================================================
# 四、方案完整性与学术质量 (30分) — LLM
# =============================================================================

def _eval_plan_and_academic(answer_dir: str, config: dict) -> Tuple[int, Dict[str, Any]]:
    """LLM 评估 Phase A 初始规划、Phase B 重构方案、学术主题切换"""
    score = 0
    details = {}
    files = _list_files(answer_dir)
    all_text = _collect_all_text(answer_dir, files)

    if not all_text:
        return 0, {"error": "未找到任何文本输出"}

    # 加载参考答案
    ref_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "reference_answer.md")
    ref_text = _read_file(ref_path) if os.path.exists(ref_path) else ""

    llm_prompt = f"""你是一位严格的社会实践项目评审专家。请评估以下 Agent 的川西社会实践方案。

### 任务要求
8人大学生团队，7天川西调研，预算20000元。
- Phase A (规划时点): 基于初始数据设计理塘-稻城7天方案。要求海拔递进（首晚<=2600m）、住宿合规（<=400元/间、需增值税发票）、配备氧气等
- Phase B (执行时点 7/4): G318桥断（≥72h），从雅江出发重构D4-D7方案

### 参考答案要点
{ref_text[:3000]}

### Agent 输出
{all_text[:12000]}

### 请从以下三个维度评分:

**4.1 Phase A 初始规划 (0-12分)**
- 10-12: 完整7天计划（每天有目的地、住宿酒店名称及价格、活动安排），海拔递进合理（D1: 成都->康定2560m），住宿全部合规（<=400元/间、VAT发票），有氧气和医疗准备
- 7-9: 有完整行程但部分细节不够（如缺少酒店价格、或某天住宿超标、或海拔跳跃）
- 4-6: 有部分规划但不完整（缺少多天的安排）
- 0-3: 几乎没有初始规划

**4.2 Phase B 重构方案 (0-12分)**
- 10-12: D4-D7 新行程完整闭环（每天有目的地/住宿/活动），最终回到成都，使用可通行道路，住宿合规，含酒店退改处理
- 7-9: 有重构方案但部分天数不够详细或未回到成都
- 4-6: 提到要重构但方案不完整
- 0-3: 几乎没有重构方案

**4.3 学术主题切换 (0-6分)**
- 5-6: 明确提出新研究主题，与实际到达地点匹配，给出了调整理由（引用路况变化），有研究方法和初步发现
- 3-4: 有主题调整但理由不充分或研究方法缺失
- 1-2: 简单提及学术调研
- 0: 未调整学术主题

请严格输出 JSON:
{{"phase_a": {{"score": 0, "reason": ""}}, "phase_b": {{"score": 0, "reason": ""}}, "academic": {{"score": 0, "reason": ""}}}}"""

    llm_raw = _call_llm_judge(llm_prompt, config)
    llm_result = _parse_llm_json(llm_raw)

    if llm_result and ("phase_a" in llm_result or "phase_b" in llm_result):
        pa = llm_result.get("phase_a", {})
        pb = llm_result.get("phase_b", {})
        ac = llm_result.get("academic", {})

        s_pa = max(0, min(12, int(pa.get("score", 0))))
        s_pb = max(0, min(12, int(pb.get("score", 0))))
        s_ac = max(0, min(6, int(ac.get("score", 0))))

        score = s_pa + s_pb + s_ac
        details["4.1 Phase A 初始规划"] = f"{s_pa}/12 - {pa.get('reason', '')[:120]}"
        details["4.2 Phase B 重构方案"] = f"{s_pb}/12 - {pb.get('reason', '')[:120]}"
        details["4.3 学术主题切换"] = f"{s_ac}/6 - {ac.get('reason', '')[:120]}"
    else:
        # fallback: 基于规则的粗略评估
        # Phase A: 检查 D1-D7 天标记
        day_markers = sum(
            1 for d in range(1, 8)
            if f"D{d}" in all_text or f"第{d}天" in all_text or f"Day {d}" in all_text
        )
        has_altitude = "海拔" in all_text or "altitude" in all_text
        has_hotel = "酒店" in all_text or "住宿" in all_text
        s_pa = min(12, day_markers + (2 if has_altitude else 0) + (2 if has_hotel else 0))
        score += s_pa
        details["4.1 Phase A (fallback)"] = (
            f"{s_pa}/12 - {day_markers}/7 天标记, 海拔={'有' if has_altitude else '无'}")

        # Phase B: 检查重构标记
        reroute_markers = sum(
            1 for kw in ["重构", "重规划", "Phase B", "新方案", "调整后", "备选"]
            if kw in all_text
        )
        has_d4_d7 = sum(1 for d in [4, 5, 6, 7]
                        if f"D{d}" in all_text or f"第{d}天" in all_text)
        s_pb = min(12, reroute_markers * 2 + has_d4_d7 * 2)
        score += s_pb
        details["4.2 Phase B (fallback)"] = (
            f"{s_pb}/12 - 重构标记: {reroute_markers}, D4-D7天: {has_d4_d7}")

        # Academic pivot
        academic_kw = ["调研主题", "学术", "研究", "课题", "选题", "调研"]
        has_academic = sum(1 for kw in academic_kw if kw in all_text)
        s_ac = min(6, has_academic * 2)
        score += s_ac
        details["4.3 学术主题 (fallback)"] = f"{s_ac}/6 (LLM 不可用)"

    return score, details


# =============================================================================
# 主入口
# =============================================================================

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    评估 agent 的输出。

    Args:
        answer_dir: agent 输出目录的绝对路径

    Returns:
        (score, report)
        - score: 0-100 的整数
        - report: dict，包含详细评估报告
    """
    config = _get_text_eval_config(answer_dir)

    s1, r1 = _eval_file_delivery(answer_dir)
    s2, r2 = _eval_financial(answer_dir, config)
    s3, r3 = _eval_crisis_decision(answer_dir, config)
    s4, r4 = _eval_plan_and_academic(answer_dir, config)

    total = s1 + s2 + s3 + s4
    total = max(0, min(100, total))

    report = {
        "总分": total,
        "结果评分": {
            "分数": s1 + s2,
            "详情": {
                "一、文件交付完整性 (10分)": r1,
                "二、财务审计与预算合规 (30分)": r2,
            },
            "扣分原因": [],
        },
        "过程评分": {
            "分数": s3 + s4,
            "详情": {
                "三、危机决策与安全合理性 (30分)": r3,
                "四、方案完整性与学术质量 (30分)": r4,
            },
            "扣分原因": [],
        },
        "评语": "",
        "分项得分": {
            "文件交付": f"{s1}/10",
            "财务审计": f"{s2}/30",
            "危机决策": f"{s3}/30",
            "方案与学术": f"{s4}/30",
        },
    }

    if total >= 85:
        report["评语"] = "优秀。方案完整，财务合规，危机决策得当，学术调整合理。"
    elif total >= 70:
        report["评语"] = "良好。基本完成任务，但部分维度有改进空间。"
    elif total >= 50:
        report["评语"] = "及格。核心功能有实现但存在明显不足。"
    elif total >= 30:
        report["评语"] = "部分完成。关键步骤缺失或决策存在问题。"
    else:
        report["评语"] = "不及格。任务完成度严重不足。"

    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """打印格式化的评分报告"""
    print("=" * 70)
    print("川西社会实践动态重规划与审计决策 — 评分报告")
    print("=" * 70)
    print(f"\n总分: {score}/100")

    scores = report.get("分项得分", {})
    if scores:
        print("\n分项得分:")
        for k, v in scores.items():
            print(f"  {k}: {v}")

    for section_key, section_label in [
        ("结果评分", "结果评分 (文件交付 + 财务审计)"),
        ("过程评分", "过程评分 (危机决策 + 方案与学术)")
    ]:
        section = report.get(section_key, {})
        print(f"\n{'─' * 50}")
        print(f"【{section_label}】 {section.get('分数', 0)}分")
        print(f"{'─' * 50}")
        for cat, items in section.get("详情", {}).items():
            print(f"\n  {cat}:")
            if isinstance(items, dict):
                for k, v in items.items():
                    print(f"    {k}: {v}")
            else:
                print(f"    {items}")

    print(f"\n{'=' * 50}")
    print(f"评语: {report.get('评语', '')}")
    print("=" * 70)


if __name__ == "__main__":
    import sys
    test_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(__file__), "..", "gpt-5", "attempt_1")
    if os.path.exists(test_dir):
        print(f"评估目录: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"目录不存在: {test_dir}")
    sys.exit(0)
