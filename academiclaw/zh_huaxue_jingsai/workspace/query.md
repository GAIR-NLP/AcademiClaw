## Query：化学竞赛试题解答
**角色设定**：你是一名资深计算化学专家。
**任务目标**：针对附件中提供的第 36 届中国化学奥林匹克（初赛）试题（包含手写扫描图），给出完整的解析步骤和最终结论，保存为 `answers.md`。
**核心要求**：
1. **多模态识别**：
    - 调用 OCR/VLM 能力精准提取手写实验参数及复杂化学方程式。
    - 使用 VLM 识别并描述晶体空间群结构（如：指出配位原子环境、晶胞参数 $a, b, c$ 之间的几何关系）。
    - 识别有机分子结构简式，特别是涉及到旋光性、构型（R/S）或顺反异构的部分。
2. **逻辑推理与计算**：
    - **热力学计算**：必须调用计算工具计算反应的标准摩尔焓变 $\Delta_r H_m^\theta$ 或吉布斯自由能。
    - **晶体密度**：根据 VLM 提取的晶胞体积及 OCR 提取的原子种类，精确计算该物质的理论密度 $\rho$。
    - **有机合成**：推导目标产物的合成路径，需指出每一步的反应类型。
3. **Context 遵循**：
    - 在解析过程中，必须引用 Context 提供的"实验室特殊标准规范"（例如：特定的有效数字保留要求、特定的热力学常数取值）。
4. **输出要求**：
    - 解析过程需严谨，所有化学式及数学公式必须使用 LaTeX 渲染。
    - 最终结论需单列。

**输出示例格式**：
```
## 第 1 题
**1-1** 解答内容...
**1-2** 解答内容...

## 第 2 题
**2-1** 解答内容...
...
```

---

## Context
试题详见 context 文件夹，共 10 道题目。图片文件为手写扫描图，请使用 VLM 进行识别。

---

## Multimodal File Analysis

For analyzing image contents, an OpenAI-compatible API is available via environment variables:
- `OPENAI_API_KEY` - API key
- `OPENAI_API_BASE` - API endpoint

To list all available models, curl the `/v1/models` endpoint:
```bash
curl -H "Authorization: Bearer $OPENAI_API_KEY" $OPENAI_API_BASE/models
```

Example usage:
```python
import os
from openai import OpenAI
client = OpenAI(base_url=os.environ["OPENAI_API_BASE"], api_key=os.environ["OPENAI_API_KEY"])

# For vision tasks, use a vision-capable model
response = client.chat.completions.create(
    model="gemini-2.5-flash",  # or other vision-capable model
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "Analyze this chemistry problem..."},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
        ]
    }]
)
```

---

**Important - Deliverable Location:**
- **Put all deliverables directly in this directory (outside of `context/`)**
- Do NOT put deliverables inside `context/` - they will not be evaluated