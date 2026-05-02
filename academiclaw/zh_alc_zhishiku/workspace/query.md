# 1. Query（任务描述）

给定 `context/context.txt` 的中文自然语言文本，构造一个 ALC 知识库 $K=\langle T,A\rangle$。

## 核心任务：抽取为 ALC
请输出以下内容，并**保存到当前目录下的 `alc_kb.txt` 文件中**：

- **TBox**：概念包含公理，形如 `C ⊑ D`
- **ABox**：断言，形如 `C(a)` 或 `R(a,b)`

**要求：**
1. 个体（individual）直接使用原文出现的命名（例如 `霍·阿·布恩蒂亚`、`马孔多`、`梅尔加德斯`、`吉卜赛人` 等），不使用额外命名规范。
2. **每一条** TBox/ABox 语句行末追加原文证据，便于核查：
   - `ALC语句  // evidence: "原文片段"`
   其中注释仅作为核查材料，不属于 ALC 语句本体。
3. 尽可能完整抽取 `context.txt` 中“显式可确定”的信息。

## 追加任务：理解 ALC 的表达边界
在 `alc_kb.txt` 的最后部分（标记为 `Non-ALC Statements`），列举出 `context.txt` 叙事部分中 **至少五条**“无法用标准 ALC（仅 TBox/ABox，且断言只允许 `C(a)` 与 `R(a,b)`）直接表达”的语句或信息点，并逐条解释为什么。

## 输出文件格式示例 (alc_kb.txt)

```text
=== TBOX ===
人物 ⊑ ⊤ // evidence: "..."
...

=== ABOX ===
人物(霍·阿·布恩蒂亚) // evidence: "..."
...

=== Non-ALC Statements ===
1. 原文: "..."
   原因: ...
...
```

## 参考文件
请阅读目录下的 context/context.txt。

### 5. context/context.txt
（内容为提供的 Context.txt 原文，此处省略具体文本以节省篇幅，实际生成时会包含完整内容）