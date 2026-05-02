"""
第38届全国中学生物理竞赛复赛 — 评分脚本（从零重写）

任务：考生在 answer.md 中逐题给出推导与最终答案（8 道大题）
评估方式：
  一、文件交付与基本格式检查（10 分）— 确定性检查
  二、内容准确性 — LLM 逐点评分（90 分）— 基于官方评分标准 320 分映射

总分 100 分
"""

import os
import json
import re
from typing import Tuple, Dict, Any

try:
    import openai
except ImportError:
    openai = None

# ============================================================================
# 环境与 LLM 配置
# ============================================================================

def _load_env(answer_dir: str) -> dict:
    """从 answer_dir 和 query 根目录加载 .env 配置"""
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
            max_tokens=8192,
            temperature=0,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        print(f"[RUBRIC] LLM Judge 调用失败: {e}")
        return ""


# ============================================================================
# 工具函数
# ============================================================================

def _read_file(path: str) -> str:
    """安全读取文件"""
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return ""
    return ""


def _find_answer(answer_dir: str) -> str:
    """寻找考生答案文本"""
    candidates = ["answer.md", "答案.md", "student_answer.md", "解答.md"]
    for fn in candidates:
        p = os.path.join(answer_dir, fn)
        if os.path.exists(p):
            return _read_file(p)
    if not os.path.isdir(answer_dir):
        return ""
    for fn in sorted(os.listdir(answer_dir)):
        low = fn.lower()
        if (low.endswith(".md") or low.endswith(".txt")) and "query" not in low and "readme" not in low:
            return _read_file(os.path.join(answer_dir, fn))
    return ""


def _extract_json(text: str) -> str:
    """从 LLM 输出中提取 JSON 字符串"""
    text = text.strip()
    m = re.search(r"```(?:json)?\s*\n?(.*?)```", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    m2 = re.search(r"\{.*\}", text, re.DOTALL)
    if m2:
        return m2.group(0).strip()
    return text


def _count_questions(answer_text: str) -> int:
    """粗略统计答案覆盖了多少道大题（1-8 题）"""
    patterns = [
        r"(?:^|\n)\s*(?:一|1)[、\.．\s]",
        r"(?:^|\n)\s*(?:二|2)[、\.．\s]",
        r"(?:^|\n)\s*(?:三|3)[、\.．\s]",
        r"(?:^|\n)\s*(?:四|4)[、\.．\s]",
        r"(?:^|\n)\s*(?:五|5)[、\.．\s]",
        r"(?:^|\n)\s*(?:六|6)[、\.．\s]",
        r"(?:^|\n)\s*(?:七|7)[、\.．\s]",
        r"(?:^|\n)\s*(?:八|8)[、\.．\s]",
    ]
    return sum(1 for pat in patterns if re.search(pat, answer_text))


# ============================================================================
# 嵌入式评分标准（来自官方评分标准 PDF，整理为结构化给分点）
#
# 试卷共 8 大题，每题 40 分，总计 320 分。
# 每个给分点仅"满分/0分"两档，不给部分分。
# ============================================================================

SCORING_RUBRIC = r"""
## 评分总原则
1. 评分标准唯一有效，仅依据明确列出的给分点。不自行补充、合并、推断给分点。
2. 公式/结论驱动给分：指定公式、中间结论、最终结果是否"明确出现"。出现→给分，未出现/写错/不完整→不给分。
3. 不做善意推断。未明确写出的内容一律视为未作答。
4. 等价性判定严格：必须数学上严格等价，不引入额外假设，不遗漏物理量。允许不同但严格等价的数学表达形式。
5. 每个给分点只能满分或0分，不给部分分。

## 一、光学（40分）
题意：平凸透镜曲面方程（极坐标→直角坐标）、插入平凹透镜后凹面方程、光束半径比。

### (1) 平凸透镜曲面 — 20分
- [Q1-1] 建立光程等式（费马原理/等光程条件）（4分）
- [Q1-2] 得到极坐标方程 r(θ) = n·r₀/(1 − n·cosθ) 或严格等价（含圆锥曲线参数形式均可）（4分）
- [Q1-3] 将极坐标方程化为直角坐标形式（4分）
- [Q1-4] 给出二次曲线标准形式（旋转二次曲面/椭圆/双曲线，含参数明确）（4分）
- [Q1-5] 明确适用范围（θ 范围或几何限制）（4分）

### (2) 平凹透镜与光束半径比 — 20分
- [Q1-6] 建立平凹透镜的等光程条件（4分）
- [Q1-7] 得到凹面极坐标方程 r'(θ) = n'·r₀'/(1 − n'·cosθ) 或严格等价（4分）
- [Q1-8] 化为直角坐标标准形式（4分）
- [Q1-9] 建立入射/出射光线几何关系（2分）
- [Q1-10] 正确计算 sinθ 对应的截面位移关系（2分）
- [Q1-11] 给出半径比 R_in/R_out 的解析公式（2分）
- [Q1-12] 明确 θ_max 的约束与最终结果（2分）

## 二、热学（40分）
题意：竖直管中气体被水银封闭，缓慢加热两个过程的功和热量。

### (1) 过程A — 18分
- [Q2-1] 初始体积 V₁ = Sh（2分）
- [Q2-2] 初始温度 T₁ = T₀ = 400 K（2分）
- [Q2-3] 压力平衡 p = p₀ + ρgh（或 p₀ = 75.0 cmHg, ρgh = 25.0 cmHg, 故 p = 100 cmHg = 4ρgh）（2分）
- [Q2-4] 说明过程A为等压过程（压力不变）（2分）
- [Q2-5] 末态体积 V₂ = 2Sh（水银上移 h，气柱变为 2h）（2分）
- [Q2-6] 计算功 W_A = p(V₂ − V₁) = 4ρghSh 或直接数值（3分）
- [Q2-7] 末态温度 T₂ = 2T₀ = 800 K（2分）
- [Q2-8] 数值 W_A ≈ 33.3 J（三位有效数字）（3分）

### (2) 过程B — 22分
- [Q2-9] 过程B中变量关系：p(x) = p₀ + ρgx, V(x) = S(l − x)（或等价参数化，其中 x 为水银柱高度）（2分）
- [Q2-10] 利用理想气体状态方程得到 T 与 x 的关系（2分）
- [Q2-11] dT/dx 分析（或等价方法）说明过程可缓慢稳定发生（2分）
- [Q2-12] 物质的量 n 的计算（n ≈ 0.0100 mol 或等价）（2分）
- [Q2-13] 末态参数正确（p_f = p₀, V_f = Sl, T_f ≈ 900 K 或等价）（2分）
- [Q2-14] 温度变化 ΔT_B 正确（2分）
- [Q2-15] 内能变化 ΔU_B = nC_V · ΔT_B，含数值 ≈ 20.8 J（2分）
- [Q2-16] ΔU_B 数值正确（2分）
- [Q2-17] 过程B做功 W_B 积分或计算，数值 ≈ 29.2 J（2分）
- [Q2-18] W_B 数值正确（2分）
- [Q2-19] Q_B = ΔU_B + W_B ≈ 50.0 J（2分）

## 三、力学 — 超球碰撞（40分）
题意：均质超球在两平行板间完全弹性碰撞（无滑动），求三次碰撞后的 v_x 和 ω_z。J = 2mr²/5。

### (1) 第一次碰撞 — 20分
- [Q3-1] 冲量-动量定理/动量关系正确写出（2分）
- [Q3-2] 角动量关系（冲量矩与角动量变化量）正确写出（2分）
- [Q3-3] 转动惯量 J = 2mr²/5 正确代入（2分）
- [Q3-4] 无滑动条件/接触点切向速度弹性恢复条件正确列出（3分）
- [Q3-5] 能量守恒方程正确列出（3分）
- [Q3-6] v₁ₓ 正确表达式（如 v₁ₓ = (3/7)v₀ₓ + (4/7)rω₀z 或严格等价）（4分）
- [Q3-7] ω₁z 正确表达式（如 ω₁z = (10/(7r))v₀ₓ − (3/7)ω₀z 或严格等价）（4分）

### (2) 第二次碰撞 — 12分
- [Q3-8] 利用上下板碰撞对称性或递推关系正确建立（2分）
- [Q3-9] v₂ₓ 正确表达式（如 v₂ₓ = (−31/49)v₀ₓ + (24/49)rω₀z 或严格等价）（4分）
- [Q3-10] ω₂z 正确表达式（如 ω₂z = (−60/(49r))v₀ₓ − (31/49)ω₀z 或严格等价）（4分）
- [Q3-11] 法向速度反弹关系 v₂y = −v₁y 说明（2分）

### (3) 第三次碰撞 — 8分
- [Q3-12] v₃ₓ 正确表达式（如 v₃ₓ = (−333/343)v₀ₓ − (52/343)rω₀z 或严格等价）（4分）
- [Q3-13] ω₃z 正确表达式（如 ω₃z = (−130/(343r))v₀ₓ + (333/343)ω₀z 或严格等价）（4分）

## 四、电磁学 — 磁矩相互作用（40分）
题意：两小磁针 A、B，A 固定在原点（磁矩沿 x 轴），B 在正下方。求势能、稳定角、平衡位置。

### (1) 势能 — 14分
- [Q4-1] 磁偶极子场的正确表达（Biot-Savart/标准偶极场公式）（4分）
- [Q4-2] 势能 U = −μ_B · B 或等价偶极-偶极相互作用势能表达（4分）
- [Q4-3] 正确化简得到 U(θ, z) 的解析式（4分）
- [Q4-4] U 中包含正确的 μ₀μ²/(4πz³) 因子和角度 cosθ 依赖（2分）

### (2) 稳定平衡角 — 13分
- [Q4-5] dU/dθ = 0 条件正确列出（3分）
- [Q4-6] 求出 θ = 0 和 θ = π 两个极值点（4分）
- [Q4-7] d²U/dθ² 判稳分析（3分）
- [Q4-8] 明确给出稳定平衡角 θ_稳 = π（或根据符号约定的等价值）（3分）

### (3) 受力平衡与稳定性 — 13分
- [Q4-9] θ = θ_稳 代入后求 F_z = −dU/dz（4分）
- [Q4-10] 平衡条件 F_z + mg = 0（或 F_z = mg）正确列出（3分）
- [Q4-11] 平衡位置 z_eq 表达式正确（z_eq = [3μ₀μ²/(4πmg)]^{1/4} 或等价）（3分）
- [Q4-12] 稳定性分析（d²U_eff/dz² 正负判定），结论：不稳定平衡（3分）

## 五、原子激光冷却（40分）
题意：⁴⁰K 原子塞曼减速。给定 m = 40u, T = 350°C = 623 K, Γ = 5.00×10⁶ s⁻¹, λ = 670 nm, β = −1.00×10¹⁰ Hz/T。

### (1) 方均根速率 — 8分
- [Q5-1] 动能关系 ½mv² = ½k_BT（一维自由度）正确列出（4分）
- [Q5-2] v₀ = √(k_BT/m) 数值 ≈ 360 m/s（4分）

### (2) 加速度与距离 — 12分
- [Q5-3] 每次散射获得动量 p = h/λ 正确（2分）
- [Q5-4] 散射力 F = Γ·h/λ 正确（2分）
- [Q5-5] 加速度 a = Γh/(mλ) 数值 ≈ 7.44×10⁴ m/s² 或 ≈ 4.5×10⁴ m/s²（4分）
- [Q5-6] 减速距离 d = v₀²/(2a) 数值 ≈ 0.87 m（4分）

### (3) 频率偏移 — 8分
- [Q5-7] 多普勒频移公式 Δf = v₀/λ 正确（4分）
- [Q5-8] Δf ≈ 537 MHz 数值正确（4分）

### (4) B(z) 关系 — 12分
- [Q5-9] 共振条件正确列出（如 f_L + v(z)/λ = f₀(0) + βB(z)）（3分）
- [Q5-10] 利用 z = 0 边界条件确定激光频率 f_L（3分）
- [Q5-11] B(z) = [v(z) − v₀]/(βλ)，v(z) = √(v₀² − 2az) 正确（3分）
- [Q5-12] B_max ≈ 0.0537 T 数值正确（3分）

## 六、同轴圆筒电磁（40分）
题意：无限长同轴带电圆筒（r₁, r₂），求 E、B（旋转时）、点电荷达外筒条件、角动量守恒。

### (1) 电场 — 2分
- [Q6-1] E(r) 分区表达正确，r₁ < r < r₂ 时 E = q/(2πε₀r)（2分）

### (2) 磁场 — 4分
- [Q6-2] 旋转等效面电流密度 K = qω/(2π) 正确（2分）
- [Q6-3] B(r) 分区表达正确，r₁ < r < r₂ 时 B = μ₀qω/(2π)（2分）

### (3) 点电荷到达外筒条件 — 11分
- [Q6-4] 电势能 U(r) 表达式正确（3分）
- [Q6-5] 规范角动量守恒 L_c = μr²φ̇ + QrA_φ = const 正确（3分）
- [Q6-6] 有效势能分析或能量守恒方程正确列出（3分）
- [Q6-7] 给出 ω（或等价量）满足的到达 r₂ 判据（2分）

### (4) 角动量与力矩 — 23分
- [Q6-4i] 内圆筒角速度 Ω_内 表达式正确（4分）
- [Q6-4ii-a] 安培定律/法拉第定律得到感应场正确（3分）
- [Q6-4ii-b] 电磁角动量密度计算正确（3分）
- [Q6-4ii-c] 外力矩冲量矩 J 表达式正确（3分）
- [Q6-4iii-a] 机械角动量分量计算正确（3分）
- [Q6-4iii-b] 电磁场角动量正确（3分）
- [Q6-4iii-c] 总角动量 L 表达式正确（4分）

## 七、汽车力学（40分）
题意：汽车力学模型，求正压力、加速度、数值计算。

### (1) 正压力与最大加速度 — 16分
- [Q7-1] 水平方向（沿斜面）合力方程正确（2分）
- [Q7-2] 竖直方向（垂直斜面）力平衡正确（2分）
- [Q7-3] 力矩平衡方程正确列出（3分）
- [Q7-4] N_前 表达式正确（含 M, m, a, g, θ, h, L）（3分）
- [Q7-5] N_后 表达式正确（3分）
- [Q7-6] a_安全 表达式正确（N_前 = 0 条件推得）（3分）

### (2) 力矩驱动加速度 — 16分
- [Q7-7] 后轮受力分析（摩擦力提供驱动力）正确（2分）
- [Q7-8] 车轮转动方程正确（如 τ_轮 = (J/r)a + f·r 或等价）（3分）
- [Q7-9] 整体平动方程正确（3分）
- [Q7-10] 联立求得 a = τ_轮/[r(M + 3m)] − g sinθ 或等价（4分）
- [Q7-11] 变速比关系 τ_轮 = r_i · τ_发（2分）
- [Q7-12] 摩擦力条件确认不滑动（2分）

### (3) 数值计算 — 8分
- [Q7-13] a(0°) ≈ 5.6 m/s²（2分）
- [Q7-14] a(30°) ≈ 0.66 m/s²（2分）
- [Q7-15] μ_min(0°) 数值正确（≈ 1.09 或等价）（2分）
- [Q7-16] μ_min(30°) 数值正确（≈ 1.25 或等价）（2分）

## 八、电动汽车（40分）
题意：永磁直流电机特性、v(t) 关系、能量效率计算。

### (1) 电机特性 — 13分
- [Q8-1] 反电动势 ε = Blr_线圈·ω 正确（2分）
- [Q8-2] 电流 I = (V − ε)/(R_线圈 + R_内) 正确（2分）
- [Q8-3] τ(ω) 线性关系表达（含 τ_max 和 ω_max）正确（3分）
- [Q8-4] τ_max 表达式正确（2分）
- [Q8-5] ω_max 表达式正确（2分）
- [Q8-6] P_max = τ_max · ω_max/4 正确（2分）

### (2) v(t) 关系 — 16分
- [Q8-7] 运动方程中正确代入 τ_轮(v)（3分）
- [Q8-8] 建立 dv/dt 的常微分方程正确（3分）
- [Q8-9] 求解得到 v(t) = v_max(1 − e^{−t/τ_c}) 或等价指数趋近形式（5分）
- [Q8-10] v_max 和 τ_c 用已知量正确表示（5分）

### (3) 数值计算 — 11分
- [Q8-11] 加速到 100 km/h 的时间 t ≈ 6.1 s（3分）
- [Q8-12] 电池消耗能量 E 积分计算正确（3分）
- [Q8-13] E ≈ 1.1 kWh 数值正确（3分）
- [Q8-14] 效率 η ≈ 18%（或 17%−19%）数值正确（2分）
"""


# ============================================================================
# 维度一：文件交付与基本格式（10分）
# ============================================================================

def _check_file_delivery(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    确定性检查文件交付和基本格式：
    - answer.md 存在 (3分)
    - 内容长度 > 1000 字符 (2分)
    - 覆盖 ≥ 4 道大题 (3分)
    - 包含数学公式/推导符号 (2分)
    """
    score = 0
    details = {}

    answer_text = _find_answer(answer_dir)

    # 1. answer.md 存在
    answer_path = os.path.join(answer_dir, "answer.md")
    if os.path.exists(answer_path):
        score += 3
        details["answer.md存在"] = "3/3"
    elif answer_text:
        score += 1
        details["answer.md存在"] = "1/3 — 存在其他文本文件但不是 answer.md"
    else:
        details["answer.md存在"] = "0/3 — 未找到答案文件"
        return score, {"分数": score, "满分": 10, "详情": details}

    # 2. 内容长度
    text_len = len(answer_text.strip())
    if text_len >= 1000:
        score += 2
        details["内容长度"] = f"2/2 — {text_len} 字符"
    elif text_len >= 200:
        score += 1
        details["内容长度"] = f"1/2 — {text_len} 字符（偏短）"
    else:
        details["内容长度"] = f"0/2 — {text_len} 字符（过短）"

    # 3. 覆盖题数
    q_count = _count_questions(answer_text)
    if q_count >= 4:
        score += 3
        details["题目覆盖"] = f"3/3 — 覆盖 {q_count} 道大题"
    elif q_count >= 2:
        score += 2
        details["题目覆盖"] = f"2/3 — 覆盖 {q_count} 道大题"
    elif q_count >= 1:
        score += 1
        details["题目覆盖"] = f"1/3 — 覆盖 {q_count} 道大题"
    else:
        details["题目覆盖"] = "0/3 — 未识别到题目结构"

    # 4. 数学公式检测
    math_patterns = [
        r"[=≈∝∫∑∏]", r"\^", r"sqrt", r"\\frac", r"\\int",
        r"[²³⁴₀₁₂]", r"×10", r"[πμρθωΔε]",
    ]
    math_hits = sum(1 for p in math_patterns if re.search(p, answer_text))
    if math_hits >= 3:
        score += 2
        details["数学推导"] = "2/2 — 含充分数学表达"
    elif math_hits >= 1:
        score += 1
        details["数学推导"] = "1/2 — 数学表达偏少"
    else:
        details["数学推导"] = "0/2 — 未发现数学公式"

    return score, {"分数": score, "满分": 10, "详情": details}


# ============================================================================
# 维度二：内容准确性 — LLM 逐点评分（90分）
# ============================================================================

def _build_llm_prompt(answer_text: str) -> str:
    """构造 LLM 逐点评分 prompt"""
    prompt = f"""你是正式考试阅卷系统（LLM-as-Judge）。
严格、逐条、机械地按照下面的《评分标准》对考生答案评分。

## 评分规则（必须遵守）
1. 评分标准唯一有效；仅依据明确列出的给分点，不得自行补充/合并/推断。
2. 公式/中间结论/最终结果驱动给分：在考生答案中明确出现即得分，未出现/错误/不完整即 0 分。
3. 不做善意推断；未明确写出的内容一律视为未作答。
4. 等价性判定严格：必须数学严格等价、无额外假设、无遗漏物理量。
5. 每个给分点只能满分或0分，不给部分分。
6. 原始满分 320 分（8 题 × 40 分）。

## 评分标准
{SCORING_RUBRIC}

## 考生答案
{answer_text[:30000]}

## 输出要求
请严格按如下 JSON 格式输出（不要输出其他文字）：
{{
  "questions": [
    {{
      "id": "Q1",
      "name": "光学",
      "max": 40,
      "earned": <该题得分整数>,
      "points": [
        {{"id": "Q1-1", "max": 4, "earned": <0或4>, "reason": "<简短判定理由>"}},
        ...
      ]
    }},
    {{
      "id": "Q2",
      "name": "热学",
      "max": 40,
      "earned": <该题得分整数>,
      "points": [...]
    }},
    {{
      "id": "Q3",
      "name": "超球碰撞",
      "max": 40,
      "earned": <该题得分整数>,
      "points": [...]
    }},
    {{
      "id": "Q4",
      "name": "磁矩相互作用",
      "max": 40,
      "earned": <该题得分整数>,
      "points": [...]
    }},
    {{
      "id": "Q5",
      "name": "原子激光冷却",
      "max": 40,
      "earned": <该题得分整数>,
      "points": [...]
    }},
    {{
      "id": "Q6",
      "name": "同轴圆筒电磁",
      "max": 40,
      "earned": <该题得分整数>,
      "points": [...]
    }},
    {{
      "id": "Q7",
      "name": "汽车力学",
      "max": 40,
      "earned": <该题得分整数>,
      "points": [...]
    }},
    {{
      "id": "Q8",
      "name": "电动汽车",
      "max": 40,
      "earned": <该题得分整数>,
      "points": [...]
    }}
  ],
  "raw_score": <0-320整数，所有题 earned 之和>,
  "comment": "<简短总评，30字以内>"
}}

关键要求：
- questions 数组必须包含 Q1-Q8 全部 8 题
- 每题的 earned 等于该题各给分点 earned 之和
- raw_score 等于所有 8 题 earned 之和
- 如果考生未作答某题，该题 earned = 0，points 中每个点 earned 均为 0
"""
    return prompt


def _llm_content_scoring(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """LLM 逐点评分，raw_score/320 → 映射到 90 分"""
    answer_text = _find_answer(answer_dir)
    if not answer_text or len(answer_text.strip()) < 50:
        return 0, {
            "分数": 0, "满分": 90,
            "error": "答案文本过短或不存在",
        }

    config = _get_text_eval_config(answer_dir)
    if not config.get("api_key"):
        return 0, {
            "分数": 0, "满分": 90,
            "error": "LLM API Key 未配置",
        }

    prompt = _build_llm_prompt(answer_text)
    raw_resp = _call_llm_judge(prompt, config)

    if not raw_resp:
        return 0, {
            "分数": 0, "满分": 90,
            "error": "LLM 调用返回空结果",
        }

    # 解析 JSON
    try:
        cleaned = _extract_json(raw_resp)
        data = json.loads(cleaned)
    except (json.JSONDecodeError, Exception) as e:
        print(f"[RUBRIC] JSON 解析失败: {e}")
        print(f"[RUBRIC] 原始响应前500字: {raw_resp[:500]}")
        # 降级：尝试从文本中提取 raw_score
        m = re.search(r'"raw_score"\s*:\s*(\d+)', raw_resp)
        if m:
            raw = min(320, max(0, int(m.group(1))))
            mapped = round(raw / 320.0 * 90.0)
            return mapped, {
                "分数": mapped, "满分": 90,
                "raw_score": raw, "raw_total": 320,
                "warning": "JSON 解析失败，仅提取了 raw_score",
            }
        return 0, {
            "分数": 0, "满分": 90,
            "error": f"LLM 返回格式无法解析: {str(e)[:200]}",
        }

    raw_score = min(320, max(0, int(data.get("raw_score", 0))))
    mapped_score = round(raw_score / 320.0 * 90.0)

    # 构建各题报告
    questions_summary = {}
    for q in data.get("questions", []):
        qid = q.get("id", "?")
        qname = q.get("name", "")
        earned = q.get("earned", 0)
        qmax = q.get("max", 40)
        questions_summary[f"{qid} {qname}"] = f"{earned}/{qmax}"

    return mapped_score, {
        "分数": mapped_score,
        "满分": 90,
        "raw_score": raw_score,
        "raw_total": 320,
        "各题得分": questions_summary,
        "comment": data.get("comment", ""),
        "llm_model": config.get("model", ""),
        "points_detail": data.get("questions", []),
    }


# ============================================================================
# 主入口
# ============================================================================

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
    s1, r1 = _check_file_delivery(answer_dir)
    s2, r2 = _llm_content_scoring(answer_dir)

    total = min(100, s1 + s2)

    report = {
        "总分": total,
        "一、文件交付与格式 (10分)": r1,
        "二、内容准确性 (90分)": r2,
        "评语": "",
    }

    if "error" in r2:
        report["评语"] = f"内容评估未能完成: {r2['error']}。仅给出文件交付分。"
    elif total >= 80:
        report["评语"] = "优秀。大部分题目推导正确，公式完整。"
    elif total >= 60:
        report["评语"] = "良好。多数题目有正确推导，但存在部分遗漏或错误。"
    elif total >= 40:
        report["评语"] = "及格。部分题目作答正确，但整体完成度不足。"
    elif total >= 20:
        report["评语"] = "部分完成。仅少数题目有正确推导。"
    else:
        report["评语"] = "未完成。答案缺失或内容严重不足。"

    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """打印格式化的评分报告"""
    print("=" * 70)
    print("第38届全国中学生物理竞赛复赛 — 评分报告")
    print("=" * 70)
    print(f"\n总分: {score}/100")

    # 一、文件交付
    r1 = report.get("一、文件交付与格式 (10分)", {})
    print(f"\n{'─' * 50}")
    print(f"一、文件交付与格式: {r1.get('分数', 0)}/10")
    print(f"{'─' * 50}")
    for k, v in r1.get("详情", {}).items():
        print(f"  {k}: {v}")

    # 二、内容准确性
    r2 = report.get("二、内容准确性 (90分)", {})
    print(f"\n{'─' * 50}")
    print(f"二、内容准确性 (LLM 逐点评分): {r2.get('分数', 0)}/90")
    print(f"{'─' * 50}")
    if "error" in r2:
        print(f"  错误: {r2['error']}")
    else:
        raw = r2.get("raw_score", 0)
        print(f"  原始得分: {raw}/320")
        print(f"  映射得分: {r2.get('分数', 0)}/90")
        print(f"  评估模型: {r2.get('llm_model', 'N/A')}")
        print(f"  总评: {r2.get('comment', '')}")
        questions = r2.get("各题得分", {})
        if questions:
            print("\n  各题得分:")
            for qid, sc in questions.items():
                print(f"    {qid}: {sc}")

    # 总评语
    print(f"\n{'=' * 50}")
    print(f"评语: {report.get('评语', '')}")
    print("=" * 70)


if __name__ == "__main__":
    import sys
    test_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(__file__), "..", "gpt-5", "attempt_1")
    if os.path.isdir(test_dir):
        print(f"正在评估目录: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"目录不存在: {test_dir}")
    sys.exit(0)
