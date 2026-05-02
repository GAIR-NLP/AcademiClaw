### 用户

## 工具1: cds_optimizer

### 基本信息

- **名称**: `cds_optimizer`
- **功能**: 优化编码序列(CDS)的密码子使用，提高在目标生物中的表达效率
- **底层库**: DnaChisel
- **代码位置**: `synth_tools/dna_chisel_wrapper.py`

### 输入参数

#### 类型1: 用户输入 (Required)

| 参数名 | 类型 | 描述 | 验证规则 | 示例 |
|--------|------|------|----------|------|
| `sequence` | string | DNA序列(ATCG格式) | • 只能包含ATCG<br>• 长度必须是3的倍数<br>• 自动清理空白字符 | `"ATGAAACGCATTAGCACC"` |
| `organism` | string | 目标表达生物 | • 限定枚举值:<br>  - e_coli<br>  - yeast<br>  - human<br>  - arabidopsis<br>  - s_cerevisiae<br>  - h_sapiens<br>  - a_thaliana | `"e_coli"` |

#### 类型2: 默认值 (Optional)

| 参数名 | 类型 | 默认值 | 配置来源 | 描述 |
|--------|------|--------|----------|------|
| `avoid_enzymes` | array | `[]` | `DNACHISEL_CONFIG['forbidden_enzymes']` | 要避免的限制性酶列表 |
| `gc_range` | array | `[0.4, 0.6]` | `DNACHISEL_CONFIG['default_gc_bounds']` | 目标GC含量范围 [min, max] |

**完整配置** (`config/tool_configs.py`):
```python
DNACHISEL_CONFIG = {
    "optimization_objectives": ["CodonOptimize", "AvoidHairpins", "AvoidPattern"],
    "constraints": ["EnforceGCContent", "EnforceTranslation", "AvoidPattern"],
    "default_gc_bounds": (0.3, 0.7),
    "window_size": 50,
    "forbidden_patterns": ["BsaI_site", "BbsI_site"],
    "species": "e_coli",
    "max_iterations": 100
}
```

#### 类型3: AI自动补全

| 参数名 | 补全策略 | 数据来源 | AI推理逻辑 | 示例 |
|--------|----------|----------|-----------|------|
| `organism` | 从用户描述提取 | 用户对话内容 | 关键词匹配:<br>• "大肠杆菌" → `e_coli`<br>• "酵母" → `yeast`<br>• "人源" → `human` | 用户: "优化用于大肠杆菌表达"<br>→ `organism="e_coli"` |
| `avoid_enzymes` | 根据后续工作流推断 | 工作流上下文 | 如果提到Golden Gate组装:<br>→ `["BsaI", "BbsI"]` | 用户: "需要Golden Gate组装"<br>→ `avoid_enzymes=["BsaI"]` |
| `gc_range` | 根据organism动态调整 | 生物学知识库 | 不同生物的最优GC范围:<br>• E.coli: [0.4, 0.6]<br>• Yeast: [0.45, 0.55]<br>• Human: [0.4, 0.55]<br>• Arabidopsis: [0.35, 0.45] | `organism="yeast"`<br>→ `gc_range=[0.45, 0.55]` |

### 输出参数

```json
{
  "success": true,
  "original_sequence": "ATGAAACGCATTAGCACC",
  "optimized_sequence": "ATGAAACGTCTGGCCCCT",
  "statistics": {
    "sequence_length": 18,
    "original_gc_content": 0.389,
    "optimized_gc_content": 0.556,
    "changes_made": 5,
    "change_percentage": 27.78
  },
  "organism": "e_coli",
  "avoided_enzymes": ["BsaI", "BbsI"]
}
```

### AI自动补全合理性分析

| 参数 | 评分 | 合理性 | 风险点 | 改进建议 |
|------|------|--------|--------|----------|
| `organism` | ⭐⭐⭐⭐⭐ (5/5) | **非常合理** | • 低: AI可准确从用户描述提取<br>• 但应该让用户确认 | 补全后明确告知用户:<br>"已选择organism=e_coli，根据您提到的'大肠杆菌表达'" |
| `avoid_enzymes` | ⭐⭐⭐⭐☆ (4/5) | **基本合理** | • 中: 如果用户未提到Golden Gate，不应自动添加<br>• 可能与用户实际需求不符 | 仅在用户明确提到Golden Gate/Type IIS assembly时自动添加 |
| `gc_range` | ⭐⭐⭐☆☆ (3/5) | **部分合理** | • 高: 固定默认值[0.4-0.6]不适合所有生物<br>• 真核生物可能需要更窄范围 | **必须改进**: 实现`SmartDefaults.get_gc_range(organism)`动态返回 |

---

## 工具2: overhang_designer

### 基本信息

- **名称**: `overhang_designer`
- **功能**: 为Golden Gate组装设计最优的4bp overhang序列
- **底层库**: GoldenHinges
- **代码位置**: `synth_tools/golden_hinges_wrapper.py`

### 输入参数

#### 类型1: 用户输入 (Required)

| 参数名 | 类型 | 描述 | 验证规则 | 示例 |
|--------|------|------|----------|------|
| `num_overhangs` | integer | 需要设计的overhang数量 | • 必须 ≥ 1<br>• 通常为片段数+1 | `3` |

#### 类型2: 默认值 (Optional)

| 参数名 | 类型 | 默认值 | 配置来源 | 描述 |
|--------|------|--------|----------|------|
| `enzyme` | string | `"BsaI"` | `GOLDENHINGES_CONFIG['enzyme']` | 使用的限制性酶 |
| `existing_overhangs` | array | `[]` | - | 已存在的overhang序列，需要避免冲突 |

**完整配置**:
```python
GOLDENHINGES_CONFIG = {
    "overhang_length": 4,              # 固定4bp (Golden Gate标准)
    "gc_content": {
        "min": 0.25,                   # 最小GC含量
        "max": 0.75                    # 最大GC含量
    },
    "differences": 2,                  # overhang间最小差异碱基数
    "max_fragment_size": 3000,
    "min_fragment_size": 500,
    "forbidden_overhangs": [],
    "enzyme": "BsaI",
    "max_radius": 20                   # 切割位点搜索半径
}
```

#### 类型3: AI自动补全

| 参数名 | 补全策略 | 数据来源 | AI推理逻辑 | 示例 |
|--------|----------|----------|-----------|------|
| `num_overhangs` | 根据片段数计算 | 组装策略 | **n+1规则**:<br>• 单片段插入: 2个(左右)<br>• n个片段组装: n+1个(包括载体) | 3个CDS片段 → `num_overhangs=4` |
| `enzyme` | 从前序工具继承 | `cds_optimizer`的`avoid_enzymes` | • 如果CDS优化避免了BsaI → 使用`"BsaI"`<br>• 如果避免了BsaI和BbsI → 使用`"BsmBI"` | `cds_optimizer`使用BsaI<br>→ `enzyme="BsaI"` |
| `existing_overhangs` | 从质粒框架提取 | 质粒框架定义 | 从`config/plasmid_frameworks.py`提取:<br>• pET28a → `["AATG", "TTAA"]`<br>• pUC19 → `["GCTT", "AATG"]` | framework="pET28a"<br>→ `existing_overhangs=["AATG", "TTAA"]` |

### 输出参数

```json
{
  "success": true,
  "designed_overhangs": ["AATG", "CCGA", "TTGC"],
  "enzyme": "BsaI",
  "statistics": {
    "requested": 3,
    "designed": 3,
    "existing_avoided": 2
  },
  "compatibility": {
    "enzyme": "BsaI",
    "overhang_length": 4,
    "gc_range": [0.25, 0.75]
  }
}
```

### AI自动补全合理性分析

| 参数 | 评分 | 合理性 | 风险点 | 改进建议 |
|------|------|--------|--------|----------|
| `num_overhangs` | ⭐⭐⭐⭐⭐ (5/5) | **非常合理** | • 极低: n+1规则是Golden Gate标准 | 补全时明确说明计算逻辑:<br>"3个片段需要4个overhangs (n+1规则)" |
| `enzyme` | ⭐⭐⭐⭐⭐ (5/5) | **非常合理** | • 低: 必须与CDS优化保持一致 | **强制验证**: 添加一致性检查器，确保整个工作流使用相同enzyme |
| `existing_overhangs` | ⭐⭐⭐⭐☆ (4/5) | **基本合理** | • 中: 如果用户使用非标准框架，提取可能失败 | 提取框架overhangs时，告知用户:<br>"从pET28a框架提取了2个固定overhangs" |

---

## 工具3: assembly_simulator

### 基本信息

- **名称**: `assembly_simulator`
- **功能**: 使用DnaCauldron模拟Golden Gate组装过程
- **底层库**: DnaCauldron
- **代码位置**: `synth_tools/dna_cauldron_wrapper.py`

### 输入参数

#### 类型1: 用户输入 (Required)

| 参数名 | 类型 | 描述 | 验证规则 | 支持的格式 |
|--------|------|------|----------|-----------|
| `fragments` | object | Fragment信息 | 必须包含序列和overhang | 支持4种格式（见下） |

**支持的fragments格式**:

```json
// 格式1: 来自overhang_designer
{
  "designed_overhangs": ["AATG", "GCTT"],
  "cds_sequence": "ATGAAA..."
}

// 格式2: 来自cds_optimizer
{
  "optimized_sequence": "ATGAAA...",
  "left_overhang": "AATG",
  "right_overhang": "GCTT"
}

// 格式3: 直接片段列表
{
  "fragments": [
    {
      "sequence": "ATGAAA...",
      "left_overhang": "AATG",
      "right_overhang": "GCTT"
    }
  ]
}

// 格式4: 简化格式
{
  "sequence": "ATGAAA...",
  "left_overhang": "AATG",
  "right_overhang": "GCTT"
}
```

#### 类型2: 默认值 (Optional)

| 参数名 | 类型 | 默认值 | 配置来源 | 描述 |
|--------|------|--------|----------|------|
| `framework` | string | `"pET28a"` | - | 质粒框架名称 |
| `enzyme` | string | `"BsaI"` | `DNACAULDRON_CONFIG['enzyme']` | 限制性酶 |
| `include_reports` | boolean | `true` | `DNACAULDRON_CONFIG['include_assembly_plots']` | 是否生成详细报告 |

**完整配置**:
```python
DNACAULDRON_CONFIG = {
    "assembly_type": "Type2sRestrictionAssembly",  # Golden Gate类型
    "enzyme": "BsaI",
    "allow_partial_assembly": False,               # 不允许部分组装
    "check_reverse_complement": True,              # 检查反向互补
    "include_fragments_plots": True,
    "include_assembly_plots": True,
    "max_constructs": 10                           # 最大构建体数量
}
```

#### 类型3: AI自动补全

| 参数名 | 补全策略 | 数据来源 | AI推理逻辑 | 示例 |
|--------|----------|----------|-----------|------|
| `fragments` | 从前序工具传递 | `cds_optimizer` + `overhang_designer` | 自动组合前序工具输出:<br>• optimized_sequence<br>• designed_overhangs | 自动构建fragments对象 |
| `framework` | 根据organism选择 | `cds_optimizer`的organism | **智能框架选择**:<br>• e_coli + His-tag → `"pET28a"`<br>• e_coli + GST-tag → `"pGEX-4T"`<br>• yeast → `"pYES2"`<br>• human → `"pcDNA3.1"` | organism="e_coli", tag="His"<br>→ `framework="pET28a"` |
| `enzyme` | 继承前序工具 | 整个工作流的enzyme | 必须与cds_optimizer和overhang_designer一致 | 全局enzyme="BsaI"<br>→ `enzyme="BsaI"` |

### 输出参数

```json
{
  "success": true,
  "enzyme": "BsaI",
  "framework": "pET28a",
  "message": "Assembly simulation completed successfully",
  "assembly_info": {
    "enzyme": "BsaI",
    "framework": "pET28a",
    "fragments_count": 1,
    "expected_constructs": 1
  },
  "detailed_report": {  // 仅当include_reports=true
    "assembly_method": "Golden Gate",
    "fragments_used": [
      {
        "name": "CDS_insert",
        "length": 18,
        "sequence": "GGTCTCNAATGATGAAA..."
      }
    ],
    "constructs_generated": [
      {
        "name": "pET28a_construct",
        "length": 5418,
        "circular": true
      }
    ],
    "warnings": []
  }
}
```

### AI自动补全合理性分析

| 参数 | 评分 | 合理性 | 风险点 | 改进建议 |
|------|------|--------|--------|----------|
| `fragments` | ⭐⭐⭐⭐⭐ (5/5) | **非常合理** | • 极低: 支持4种格式，容错性强<br>• 自动识别和转换 | **优秀设计**: 多格式支持极大简化了用户操作 |
| `framework` | ⭐⭐⭐☆☆ (3/5) | **部分合理** | • **高**: 默认pET28a仅适用于原核<br>• 真核表达会失败 | **必须改进**: 实现`SmartDefaults.get_framework(organism, tag)`:<br>• E.coli → pET28a/pET15b<br>• Yeast → pYES2/pGADT7<br>• Human → pcDNA3.1/pLVX |
| `enzyme` | ⭐⭐⭐⭐⭐ (5/5) | **非常合理** | • 低: 但缺少验证机制 | **必须添加**: WorkflowValidator验证整个工作流的enzyme一致性 |

---

## 工具4: plasmid_visualizer

### 基本信息

- **名称**: `plasmid_visualizer`
- **功能**: 生成质粒可视化图谱（环状或线性）
- **底层库**: DnaFeaturesViewer
- **代码位置**: `synth_tools/dna_visualizer_wrapper.py`

### 输入参数

#### 类型1: 用户输入 (Required)

| 参数名 | 类型 | 描述 | 验证规则 | 示例 |
|--------|------|------|----------|------|
| `sequence` | string | 完整质粒DNA序列 | 必须是有效的ATCG序列 | `"ATGAAACGC..."` (完整质粒) |

#### 类型2: 默认值 (Optional)

| 参数名 | 类型 | 默认值 | 配置来源 | 描述 |
|--------|------|--------|----------|------|
| `features` | array | `[]` | - | 特征注释列表（CDS, promoter, terminator等） |
| `plasmid_name` | string | `"Plasmid"` | - | 质粒名称 |
| `circular` | boolean | `true` | `DNAFEATUREVIEWER_CONFIG['circular_plot']` | 是否为环状质粒 |
| `output_format` | string | `"png"` | `DNAFEATUREVIEWER_CONFIG['default_format']` | 输出格式（png/svg/pdf） |

**完整配置**:
```python
DNAFEATUREVIEWER_CONFIG = {
    "figure_width": 12,
    "figure_height": 8,
    "circular_plot": True,
    "include_ruler": True,
    "feature_colors": {
        "CDS": "#ffcccc",
        "promoter": "#ccccff",
        "terminator": "#ccffcc",
        "origin": "#ffcc99",
        "resistance": "#ff9999"
    },
    "label_threshold": 100,
    "strand_in_label_threshold": 7,
    "dpi": 300
}
```

#### 类型3: AI自动补全

| 参数名 | 补全策略 | 数据来源 | AI推理逻辑 | 示例 |
|--------|----------|----------|-----------|------|
| `sequence` | 从assembly_simulator传递 | 组装后的完整序列 | 直接使用final_sequence | 自动传递组装结果 |
| `features` | 自动识别注释 | 序列分析 + 框架定义 | **智能特征识别**:<br>• T7 promoter: `TAATACGACTCACTATA`<br>• His6-tag: `CATCATCATCATCATCAT`<br>• Kan^R: 标准卡那霉素抗性基因<br>• ColE1 ori: 标准复制起点 | framework="pET28a"<br>→ 自动添加T7, His6, Kan, ori |
| `plasmid_name` | 智能命名 | 工作流上下文 | 命名规则:<br>`framework-gene-tag-modification`<br>例: `"pET28a-GFP-His6-optimized"` | 自动生成描述性名称 |
| `circular` | 根据类型推断 | 分子类型 | • 质粒框架 → `true`<br>• PCR产物 → `false`<br>• 线性化载体 → `false` | framework存在 → `circular=true` |

### 输出参数

```json
{
  "success": true,
  "plasmid_name": "pET28a-GFP-His6",
  "sequence_length": 5418,
  "circular": true,
  "output_format": "png",
  "image_path": "/home/redacted_service_user/tmpxxxx.png",
  "image_base64": "iVBORw0KGgoAAAANS..."  // 仅PNG格式
}
```

### AI自动补全合理性分析

| 参数 | 评分 | 合理性 | 风险点 | 改进建议 |
|------|------|--------|--------|----------|
| `sequence` | ⭐⭐⭐⭐⭐ (5/5) | **非常合理** | • 极低: 直接传递，无歧义 | 无需改进 |
| `features` | ⭐⭐⭐⭐☆ (4/5) | **基本合理** | • 中: 标准特征识别准确<br>• 复杂特征需要用户提供 | 扩展识别库，支持更多标准元件:<br>• RBS (核糖体结合位点)<br>• Multiple cloning site<br>• Epitope tags |
| `plasmid_name` | ⭐⭐⭐⭐⭐ (5/5) | **非常合理** | • 极低: 遵循标准命名规范 | 可以让用户自定义命名模板 |
| `circular` | ⭐⭐⭐⭐⭐ (5/5) | **非常合理** | • 极低: 质粒默认环状是标准 | 无需改进 |
| `output_format` | ⭐⭐⭐⭐☆ (4/5) | **基本合理** | • 低: PNG适合预览，但发表需要SVG | **改进**: 根据用途智能选择:<br>• 预览 → PNG (150 DPI)<br>• 分析 → PNG (300 DPI)<br>• 发表 → SVG (矢量)<br>• 打印 → PDF |

---

## 工具5: primer_designer

### 基本信息

- **名称**: `primer_designer`
- **功能**: 使用Primerize算法设计RNA合成引物
- **底层库**: Primerize
- **代码位置**: `synth_tools/primerize_wrapper.py`

### 输入参数

#### 类型1: 用户输入 (Required)

| 参数名 | 类型 | 描述 | 验证规则 | 示例 |
|--------|------|------|----------|------|
| `sequence` | string | RNA序列(ATCGU格式) | 必须包含ATCGU字符 | `"AUGAAACGCAUUAGCACC"` |

#### 类型2: 默认值 (Optional)

| 参数名 | 类型 | 默认值 | 配置来源 | 描述 |
|--------|------|--------|----------|------|
| `min_tm` | number | `60.0` | `PRIMERIZE_CONFIG['min_tm']` | 最小熔解温度(°C) |
| `min_length` | integer | `15` | `PRIMERIZE_CONFIG['min_length']` | 最小引物长度(bp) |
| `max_length` | integer | `60` | `PRIMERIZE_CONFIG['max_length']` | 最大引物长度(bp) |
| `prefix` | string | `"Primer"` | `PRIMERIZE_CONFIG['prefix']` | 引物名称前缀 |

**完整配置**:
```python
PRIMERIZE_CONFIG = {
    "min_tm": 60.0,                    # 适合大多数RNA合成
    "min_length": 15,                  # RNA合成最小长度
    "max_length": 60,                  # RNA合成最大长度
    "prefix": "Primer",
    "num_primers": None,               # None表示自动计算
    "default_format": "json"
}
```

#### 类型3: AI自动补全

| 参数名 | 补全策略 | 数据来源 | AI推理逻辑 | 示例 |
|--------|----------|----------|-----------|------|
| `sequence` | DNA转录为RNA | `cds_optimizer`的序列 | T → U转换:<br>`ATGAAA` → `AUGAAA` | DNA输入自动转录 |
| `min_tm` | 根据应用调整 | 用户描述的应用场景 | **应用场景优化**:<br>• 体外转录: 55-58°C<br>• RT-PCR: 58-62°C<br>• RNA结构探测: 50-55°C<br>• 默认: 60°C | 用户: "体外转录"<br>→ `min_tm=55` |
| `length_range` | 根据序列长度优化 | RNA序列长度 | **动态调整**:<br>• <100bp: [15, 40]<br>• 100-300bp: [20, 50]<br>• >300bp: [25, 60] | 150bp RNA<br>→ `min_length=20, max_length=50` |
| `prefix` | 根据项目命名 | 项目名称/基因名 | `"项目名-Primer"`<br>例: `"GFP-Primer"` | 项目="GFP"<br>→ `prefix="GFP-Primer"` |

### 输出参数

```json
{
  "success": true,
  "sequence": "AUGAAACGCAUUAGCACC",
  "parameters": {
    "min_tm": 60.0,
    "min_length": 15,
    "max_length": 60,
    "prefix": "Primer"
  },
  "primers": [
    {
      "index": 1,
      "name": "Primer_1",
      "sequence": "AUGAAACGCAUUAGC",  // 如果Primerize提供
      "tm": 62.5,
      "length": 15
    },
    {
      "index": 2,
      "name": "Primer_2",
      "sequence": "CAUUAGCACC",
      "tm": 58.3,
      "length": 10
    }
  ],
  "statistics": {
    "num_primers": 2,
    "misprime_score": 0.15  // 如果可用
  },
  "design_summary": "Primerize 1D design completed"
}
```

### AI自动补全合理性分析

| 参数 | 评分 | 合理性 | 风险点 | 改进建议 |
|------|------|--------|--------|----------|
| `sequence` | ⭐⭐⭐⭐☆ (4/5) | **基本合理** | • 低: DNA→RNA转换标准<br>• 但应该告知用户 | 转换时明确提示:<br>"已将DNA序列转录为RNA (T→U)" |
| `min_tm` | ⭐⭐⭐☆☆ (3/5) | **部分合理** | • **高**: 60°C不适合所有场景<br>• 体外转录通常55°C<br>• qPCR需要更高Tm | **必须改进**: 询问用户应用类型:<br>"请问引物用途: 体外转录/RT-PCR/结构探测?" |
| `length_range` | ⭐⭐⭐⭐☆ (4/5) | **基本合理** | • 低: [15-60]覆盖大多数场景<br>• 超长RNA可能需要更长引物 | 根据序列长度动态调整 |
| `prefix` | ⭐⭐⭐⭐⭐ (5/5) | **非常合理** | • 极低: 有意义的命名便于管理 | 无需改进 |

---

## AI自动补全合理性评估

### 总体评分: ⭐⭐⭐⭐☆ (4.2/5)

### 各工具评分汇总

| 工具 | 平均评分 | 最高分参数 | 最低分参数 | 主要风险 |
|------|---------|-----------|-----------|---------|
| **cds_optimizer** | 4.0/5 | organism (5/5) | gc_range (3/5) | GC范围固定不适配 |
| **overhang_designer** | 4.7/5 | num_overhangs, enzyme (5/5) | existing_overhangs (4/5) | 非标准框架提取失败 |
| **assembly_simulator** | 4.3/5 | fragments, enzyme (5/5) | framework (3/5) | 默认pET28a不适合真核 |
| **plasmid_visualizer** | 4.6/5 | sequence, circular, name (5/5) | features, output_format (4/5) | 复杂特征识别不足 |
| **primer_designer** | 4.0/5 | prefix (5/5) | min_tm (3/5) | Tm值不匹配应用场景 |

### 优势分析

| 优势 | 评分 | 说明 | 示例 |
|------|------|------|------|
| **参数传递自动化** | ⭐⭐⭐⭐⭐ | 工具间无缝传递数据 | optimized_sequence → assembly → visualization |
| **多格式兼容性** | ⭐⭐⭐⭐⭐ | assembly_simulator支持4种输入格式 | 来自不同来源的fragments都能处理 |
| **生物学规则遵循** | ⭐⭐⭐⭐⭐ | n+1规则、Golden Gate标准 | num_overhangs自动计算 |
| **命名规范** | ⭐⭐⭐⭐⭐ | 描述性、标准化的命名 | pET28a-GFP-His6-optimized |

### 风险点汇总

| 风险 | 严重性 | 发生概率 | 影响范围 | 解决优先级 |
|------|--------|---------|---------|----------|
| **organism未传递导致framework错误** | 🔴 高 | 中 (40%) | cds_optimizer → assembly_simulator | **P0 - 立即修复** |
| **enzyme不一致导致组装失败** | 🔴 高 | 低 (15%) | 整个工作流 | **P0 - 立即修复** |
| **GC范围不适配organism** | 🟡 中 | 高 (70%) | cds_optimizer | **P1 - 1周内** |
| **framework默认值不适合真核** | 🟡 中 | 中 (50%) | assembly_simulator | **P1 - 1周内** |
| **Tm值不匹配应用场景** | 🟡 中 | 中 (40%) | primer_designer | **P2 - 2周内** |
| **AI补全不透明** | 🟢 低 | 高 (80%) | 所有工具 | **P2 - 2周内** |

---

## 工作流参数一致性

### 全局参数定义

以下参数必须在整个工作流中保持一致：

| 全局参数 | 涉及工具 | 一致性要求 | 当前状态 | 验证机制 |
|---------|---------|-----------|---------|---------|
| `organism` | cds_optimizer, assembly_simulator | **强制一致** | ❌ 未验证 | 需要添加WorkflowValidator |
| `enzyme` | cds_optimizer, overhang_designer, assembly_simulator | **强制一致** | ❌ 未验证 | 需要添加enzyme链验证 |
| `framework` | assembly_simulator, plasmid_visualizer | **建议一致** | ❌ 未验证 | 建议添加提示 |

### 参数传递链

```
用户输入: sequence, organism
    ↓
[cds_optimizer]
    • sequence (用户输入)
    • organism (用户输入/AI推断)
    • avoid_enzymes (AI补全 - Golden Gate)
    • gc_range (默认/AI动态调整)
    ↓ 输出: optimized_sequence
    ↓
[overhang_designer]
    • num_overhangs (AI计算 - n+1规则)
    • enzyme (继承 - 与cds一致)
    • existing_overhangs (AI提取 - 框架)
    ↓ 输出: designed_overhangs
    ↓
[assembly_simulator]
    • fragments (自动组合 - 前序输出)
    • enzyme (继承 - 全局一致)
    • framework (AI选择 - 基于organism)
    • include_reports (默认true)
    ↓ 输出: final_sequence
    ↓
[plasmid_visualizer]
    • sequence (传递 - assembly输出)
    • features (AI识别 - 框架定义)
    • plasmid_name (AI生成 - 描述性)
    • circular (AI推断 - 类型判断)
    • output_format (默认/用户需求)
    ↓ 输出: image_path, image_base64

独立分支:
[primer_designer]
    • sequence (DNA→RNA转换)
    • min_tm (默认/AI应用调整)
    • min_length, max_length (默认/AI长度优化)
    • prefix (AI项目命名)
```
把这个改成md格式

---

### DeepSeek AI

<p>思考：</p><blockquote><p class="ds-markdown-paragraph"><span>我们有一个完整的工具集，每个工具都有输入参数，分为三类：用户输入、默认值、AI自动补全。</span><br><span>我们需要为每个工具分析AI自动补全的合理性，并给出改进建议。</span></p><p class="ds-markdown-paragraph"><span>注意：我们已经有了每个工具的输入参数和AI补全策略，现在需要以Markdown格式输出，并且按照工具分别分析。</span></p><p class="ds-markdown-paragraph"><span>由于内容较长，我们将按照工具逐个分析，并给出总体评估。</span></p><p class="ds-markdown-paragraph"><span>我们按照以下结构进行：</span></p><ol start="1"><li><p class="ds-markdown-paragraph"><span>每个工具的分析包括：参数名、评分（1-5星）、合理性、风险点、改进建议。</span></p></li><li><p class="ds-markdown-paragraph"><span>最后给出总体评估和风险汇总。</span></p></li></ol><p class="ds-markdown-paragraph"><span>我们已经有了每个工具的AI自动补全策略，现在需要对这些策略进行评分和评论。</span></p><p class="ds-markdown-paragraph"><span>注意：评分标准：</span><br><span>5星：非常合理，几乎无风险，符合生物学规则，用户体验好。</span><br><span>4星：基本合理，有少量风险，但可以通过明确提示或简单验证解决。</span><br><span>3星：部分合理，存在一定风险，需要改进策略。</span><br><span>2星：不太合理，风险较高，可能导致错误结果。</span><br><span>1星：不合理，有严重风险，必须修改。</span></p><p class="ds-markdown-paragraph"><span>我们将按照这个标准对每个工具的每个AI补全参数进行评分。</span></p><p class="ds-markdown-paragraph"><span>由于内容很多，我们只对每个工具的关键参数进行详细分析，而不是每个参数都同样详细。</span></p><p class="ds-markdown-paragraph"><span>我们开始吧。</span></p></blockquote><br/><h1><span>工具集AI自动补全合理性分析</span></h1><h2><span>工具1: cds_optimizer</span></h2><h3><span>AI自动补全合理性分析</span></h3><div class="ds-scroll-area _1210dd7 c03cafe9"><div class="ds-scroll-area__gutters" style="position: sticky; top: 0px; left: 0px; right: 0px; height: 0px; --container-height: 333px;"><div class="ds-scroll-area__horizontal-gutter" style="left: 0px; right: 0px; top: calc(var(--container-height) - 14px); height: 10px;"><div class="ds-scroll-area__horizontal-bar" style="left: 0px; width: 980.305px;"></div></div><div class="ds-scroll-area__vertical-gutter" style="right: 0px; top: 8px; bottom: calc(0px - var(--container-height) + 8px); width: 10px;"><div class="ds-scroll-area__vertical-bar" style="display: none;"></div></div></div><table><thead><tr><th><span>参数</span></th><th><span>评分</span></th><th><span>合理性</span></th><th><span>风险点</span></th><th><span>改进建议</span></th></tr></thead><tbody><tr><td>`organism`</td><td><span>⭐⭐⭐⭐⭐ (5/5)</span></td><td><strong><span>非常合理</span></strong></td><td><span>• 低: AI可准确从用户描述提取</span><br><span>• 但应该让用户确认</span></td><td><span>补全后明确告知用户:</span><br><span>"已选择organism=e_coli，根据您提到的'大肠杆菌表达'"</span></td></tr><tr><td>`avoid_enzymes`</td><td><span>⭐⭐⭐⭐☆ (4/5)</span></td><td><strong><span>基本合理</span></strong></td><td><span>• 中: 如果用户未提到Golden Gate，不应自动添加</span><br><span>• 可能与用户实际需求不符</span></td><td><span>仅在用户明确提到Golden Gate/Type IIS assembly时自动添加</span></td></tr><tr><td>`gc_range`</td><td><span>⭐⭐⭐☆☆ (3/5)</span></td><td><strong><span>部分合理</span></strong></td><td><span>• 高: 固定默认值[0.4-0.6]不适合所有生物</span><br><span>• 真核生物可能需要更窄范围</span></td><td><strong><span>必须改进</span></strong><span>: 实现</span>`SmartDefaults.get_gc_range(organism)`<span>动态返回</span></td></tr></tbody></table></div><hr><h2><span>工具2: overhang_designer</span></h2><h3><span>AI自动补全合理性分析</span></h3><div class="ds-scroll-area _1210dd7 c03cafe9"><div class="ds-scroll-area__gutters" style="position: sticky; top: 0px; left: 0px; right: 0px; height: 0px; --container-height: 258px;"><div class="ds-scroll-area__horizontal-gutter" style="left: 0px; right: 0px; top: calc(var(--container-height) - 14px); height: 10px;"><div class="ds-scroll-area__horizontal-bar" style="left: 0px; width: 965.264px;"></div></div><div class="ds-scroll-area__vertical-gutter" style="right: 0px; top: 8px; bottom: calc(0px - var(--container-height) + 8px); width: 10px;"><div class="ds-scroll-area__vertical-bar" style="display: none;"></div></div></div><table><thead><tr><th><span>参数</span></th><th><span>评分</span></th><th><span>合理性</span></th><th><span>风险点</span></th><th><span>改进建议</span></th></tr></thead><tbody><tr><td>`num_overhangs`</td><td><span>⭐⭐⭐⭐⭐ (5/5)</span></td><td><strong><span>非常合理</span></strong></td><td><span>• 极低: n+1规则是Golden Gate标准</span></td><td><span>补全时明确说明计算逻辑:</span><br><span>"3个片段需要4个overhangs (n+1规则)"</span></td></tr><tr><td>`enzyme`</td><td><span>⭐⭐⭐⭐⭐ (5/5)</span></td><td><strong><span>非常合理</span></strong></td><td><span>• 低: 必须与CDS优化保持一致</span></td><td><strong><span>强制验证</span></strong><span>: 添加一致性检查器，确保整个工作流使用相同enzyme</span></td></tr><tr><td>`existing_overhangs`</td><td><span>⭐⭐⭐⭐☆ (4/5)</span></td><td><strong><span>基本合理</span></strong></td><td><span>• 中: 如果用户使用非标准框架，提取可能失败</span></td><td><span>提取框架overhangs时，告知用户:</span><br><span>"从pET28a框架提取了2个固定overhangs"</span></td></tr></tbody></table></div><hr><h2><span>工具3: assembly_simulator</span></h2><h3><span>AI自动补全合理性分析</span></h3><div class="ds-scroll-area _1210dd7 c03cafe9"><div class="ds-scroll-area__gutters" style="position: sticky; top: 0px; left: 0px; right: 0px; height: 0px; --container-height: 333px;"><div class="ds-scroll-area__horizontal-gutter" style="left: 0px; right: 0px; top: calc(var(--container-height) - 14px); height: 10px;"><div class="ds-scroll-area__horizontal-bar" style="display: none;"></div></div><div class="ds-scroll-area__vertical-gutter" style="right: 0px; top: 8px; bottom: calc(0px - var(--container-height) + 8px); width: 10px;"><div class="ds-scroll-area__vertical-bar" style="display: none;"></div></div></div><table><thead><tr><th><span>参数</span></th><th><span>评分</span></th><th><span>合理性</span></th><th><span>风险点</span></th><th><span>改进建议</span></th></tr></thead><tbody><tr><td>`fragments`</td><td><span>⭐⭐⭐⭐⭐ (5/5)</span></td><td><strong><span>非常合理</span></strong></td><td><span>• 极低: 支持4种格式，容错性强</span><br><span>• 自动识别和转换</span></td><td><strong><span>优秀设计</span></strong><span>: 多格式支持极大简化了用户操作</span></td></tr><tr><td>`framework`</td><td><span>⭐⭐⭐☆☆ (3/5)</span></td><td><strong><span>部分合理</span></strong></td><td><span>• </span><strong><span>高</span></strong><span>: 默认pET28a仅适用于原核</span><br><span>• 真核表达会失败</span></td><td><strong><span>必须改进</span></strong><span>: 实现</span>`SmartDefaults.get_framework(organism, tag)`<span>:</span><br><span>• E.coli → pET28a/pET15b</span><br><span>• Yeast → pYES2/pGADT7</span><br><span>• Human → pcDNA3.1/pLVX</span></td></tr><tr><td>`enzyme`</td><td><span>⭐⭐⭐⭐⭐ (5/5)</span></td><td><strong><span>非常合理</span></strong></td><td><span>• 低: 但缺少验证机制</span></td><td><strong><span>必须添加</span></strong><span>: WorkflowValidator验证整个工作流的enzyme一致性</span></td></tr></tbody></table></div><hr><h2><span>工具4: plasmid_visualizer</span></h2><h3><span>AI自动补全合理性分析</span></h3><div class="ds-scroll-area _1210dd7 c03cafe9"><div class="ds-scroll-area__gutters" style="position: sticky; top: 0px; left: 0px; right: 0px; height: 0px; --container-height: 449px;"><div class="ds-scroll-area__horizontal-gutter" style="left: 0px; right: 0px; top: calc(var(--container-height) - 14px); height: 10px;"><div class="ds-scroll-area__horizontal-bar" style="display: none;"></div></div><div class="ds-scroll-area__vertical-gutter" style="right: 0px; top: 8px; bottom: calc(0px - var(--container-height) + 8px); width: 10px;"><div class="ds-scroll-area__vertical-bar" style="display: none;"></div></div></div><table><thead><tr><th><span>参数</span></th><th><span>评分</span></th><th><span>合理性</span></th><th><span>风险点</span></th><th><span>改进建议</span></th></tr></thead><tbody><tr><td>`sequence`</td><td><span>⭐⭐⭐⭐⭐ (5/5)</span></td><td><strong><span>非常合理</span></strong></td><td><span>• 极低: 直接传递，无歧义</span></td><td><span>无需改进</span></td></tr><tr><td>`features`</td><td><span>⭐⭐⭐⭐☆ (4/5)</span></td><td><strong><span>基本合理</span></strong></td><td><span>• 中: 标准特征识别准确</span><br><span>• 复杂特征需要用户提供</span></td><td><span>扩展识别库，支持更多标准元件:</span><br><span>• RBS (核糖体结合位点)</span><br><span>• Multiple cloning site</span><br><span>• Epitope tags</span></td></tr><tr><td>`plasmid_name`</td><td><span>⭐⭐⭐⭐⭐ (5/5)</span></td><td><strong><span>非常合理</span></strong></td><td><span>• 极低: 遵循标准命名规范</span></td><td><span>可以让用户自定义命名模板</span></td></tr><tr><td>`circular`</td><td><span>⭐⭐⭐⭐⭐ (5/5)</span></td><td><strong><span>非常合理</span></strong></td><td><span>• 极低: 质粒默认环状是标准</span></td><td><span>无需改进</span></td></tr><tr><td>`output_format`</td><td><span>⭐⭐⭐⭐☆ (4/5)</span></td><td><strong><span>基本合理</span></strong></td><td><span>• 低: PNG适合预览，但发表需要SVG</span></td><td><strong><span>改进</span></strong><span>: 根据用途智能选择:</span><br><span>• 预览 → PNG (150 DPI)</span><br><span>• 分析 → PNG (300 DPI)</span><br><span>• 发表 → SVG (矢量)</span><br><span>• 打印 → PDF</span></td></tr></tbody></table></div><hr><h2><span>工具5: primer_designer</span></h2><h3><span>AI自动补全合理性分析</span></h3><div class="ds-scroll-area _1210dd7 c03cafe9"><div class="ds-scroll-area__gutters" style="position: sticky; top: 0px; left: 0px; right: 0px; height: 0px; --container-height: 328px;"><div class="ds-scroll-area__horizontal-gutter" style="left: 0px; right: 0px; top: calc(var(--container-height) - 14px); height: 10px;"><div class="ds-scroll-area__horizontal-bar" style="display: none;"></div></div><div class="ds-scroll-area__vertical-gutter" style="right: 0px; top: 8px; bottom: calc(0px - var(--container-height) + 8px); width: 10px;"><div class="ds-scroll-area__vertical-bar" style="display: none;"></div></div></div><table><thead><tr><th><span>参数</span></th><th><span>评分</span></th><th><span>合理性</span></th><th><span>风险点</span></th><th><span>改进建议</span></th></tr></thead><tbody><tr><td>`sequence`</td><td><span>⭐⭐⭐⭐☆ (4/5)</span></td><td><strong><span>基本合理</span></strong></td><td><span>• 低: DNA→RNA转换标准</span><br><span>• 但应该告知用户</span></td><td><span>转换时明确提示:</span><br><span>"已将DNA序列转录为RNA (T→U)"</span></td></tr><tr><td>`min_tm`</td><td><span>⭐⭐⭐☆☆ (3/5)</span></td><td><strong><span>部分合理</span></strong></td><td><span>• </span><strong><span>高</span></strong><span>: 60°C不适合所有场景</span><br><span>• 体外转录通常55°C</span><br><span>• qPCR需要更高Tm</span></td><td><strong><span>必须改进</span></strong><span>: 询问用户应用类型:</span><br><span>"请问引物用途: 体外转录/RT-PCR/结构探测?"</span></td></tr><tr><td>`length_range`</td><td><span>⭐⭐⭐⭐☆ (4/5)</span></td><td><strong><span>基本合理</span></strong></td><td><span>• 低: [15-60]覆盖大多数场景</span><br><span>• 超长RNA可能需要更长引物</span></td><td><span>根据序列长度动态调整</span></td></tr><tr><td>`prefix`</td><td><span>⭐⭐⭐⭐⭐ (5/5)</span></td><td><strong><span>非常合理</span></strong></td><td><span>• 极低: 有意义的命名便于管理</span></td><td><span>无需改进</span></td></tr></tbody></table></div><hr><h2><span>AI自动补全合理性评估</span></h2><h3><span>总体评分: ⭐⭐⭐⭐☆ (4.2/5)</span></h3><h3><span>各工具评分汇总</span></h3><div class="ds-scroll-area _1210dd7 c03cafe9"><div class="ds-scroll-area__gutters" style="position: sticky; top: 0px; left: 0px; right: 0px; height: 0px; --container-height: 274px;"><div class="ds-scroll-area__horizontal-gutter" style="left: 0px; right: 0px; top: calc(var(--container-height) - 14px); height: 10px;"><div class="ds-scroll-area__horizontal-bar" style="display: none;"></div></div><div class="ds-scroll-area__vertical-gutter" style="right: 0px; top: 8px; bottom: calc(0px - var(--container-height) + 8px); width: 10px;"><div class="ds-scroll-area__vertical-bar" style="display: none;"></div></div></div><table><thead><tr><th><span>工具</span></th><th><span>平均评分</span></th><th><span>最高分参数</span></th><th><span>最低分参数</span></th><th><span>主要风险</span></th></tr></thead><tbody><tr><td><strong><span>cds_optimizer</span></strong></td><td><span>4.0/5</span></td><td><span>organism (5/5)</span></td><td><span>gc_range (3/5)</span></td><td><span>GC范围固定不适配</span></td></tr><tr><td><strong><span>overhang_designer</span></strong></td><td><span>4.7/5</span></td><td><span>num_overhangs, enzyme (5/5)</span></td><td><span>existing_overhangs (4/5)</span></td><td><span>非标准框架提取失败</span></td></tr><tr><td><strong><span>assembly_simulator</span></strong></td><td><span>4.3/5</span></td><td><span>fragments, enzyme (5/5)</span></td><td><span>framework (3/5)</span></td><td><span>默认pET28a不适合真核</span></td></tr><tr><td><strong><span>plasmid_visualizer</span></strong></td><td><span>4.6/5</span></td><td><span>sequence, circular, name (5/5)</span></td><td><span>features, output_format (4/5)</span></td><td><span>复杂特征识别不足</span></td></tr><tr><td><strong><span>primer_designer</span></strong></td><td><span>4.0/5</span></td><td><span>prefix (5/5)</span></td><td><span>min_tm (3/5)</span></td><td><span>Tm值不匹配应用场景</span></td></tr></tbody></table></div><h3><span>优势分析</span></h3><div class="ds-scroll-area _1210dd7 c03cafe9"><div class="ds-scroll-area__gutters" style="position: sticky; top: 0px; left: 0px; right: 0px; height: 0px; --container-height: 253px;"><div class="ds-scroll-area__horizontal-gutter" style="left: 0px; right: 0px; top: calc(var(--container-height) - 14px); height: 10px;"><div class="ds-scroll-area__horizontal-bar" style="display: none;"></div></div><div class="ds-scroll-area__vertical-gutter" style="right: 0px; top: 8px; bottom: calc(0px - var(--container-height) + 8px); width: 10px;"><div class="ds-scroll-area__vertical-bar" style="display: none;"></div></div></div><table><thead><tr><th><span>优势</span></th><th><span>评分</span></th><th><span>说明</span></th><th><span>示例</span></th></tr></thead><tbody><tr><td><strong><span>参数传递自动化</span></strong></td><td><span>⭐⭐⭐⭐⭐</span></td><td><span>工具间无缝传递数据</span></td><td><span>optimized_sequence → assembly → visualization</span></td></tr><tr><td><strong><span>多格式兼容性</span></strong></td><td><span>⭐⭐⭐⭐⭐</span></td><td><span>assembly_simulator支持4种输入格式</span></td><td><span>来自不同来源的fragments都能处理</span></td></tr><tr><td><strong><span>生物学规则遵循</span></strong></td><td><span>⭐⭐⭐⭐⭐</span></td><td><span>n+1规则、Golden Gate标准</span></td><td><span>num_overhangs自动计算</span></td></tr><tr><td><strong><span>命名规范</span></strong></td><td><span>⭐⭐⭐⭐⭐</span></td><td><span>描述性、标准化的命名</span></td><td><span>pET28a-GFP-His6-optimized</span></td></tr></tbody></table></div><h3><span>风险点汇总</span></h3><div class="ds-scroll-area _1210dd7 c03cafe9"><div class="ds-scroll-area__gutters" style="position: sticky; top: 0px; left: 0px; right: 0px; height: 0px; --container-height: 320px;"><div class="ds-scroll-area__horizontal-gutter" style="left: 0px; right: 0px; top: calc(var(--container-height) - 14px); height: 10px;"><div class="ds-scroll-area__horizontal-bar" style="display: none;"></div></div><div class="ds-scroll-area__vertical-gutter" style="right: 0px; top: 8px; bottom: calc(0px - var(--container-height) + 8px); width: 10px;"><div class="ds-scroll-area__vertical-bar" style="display: none;"></div></div></div><table><thead><tr><th><span>风险</span></th><th><span>严重性</span></th><th><span>发生概率</span></th><th><span>影响范围</span></th><th><span>解决优先级</span></th></tr></thead><tbody><tr><td><strong><span>organism未传递导致framework错误</span></strong></td><td><span>🔴 高</span></td><td><span>中 (40%)</span></td><td><span>cds_optimizer → assembly_simulator</span></td><td><strong><span>P0 - 立即修复</span></strong></td></tr><tr><td><strong><span>enzyme不一致导致组装失败</span></strong></td><td><span>🔴 高</span></td><td><span>低 (15%)</span></td><td><span>整个工作流</span></td><td><strong><span>P0 - 立即修复</span></strong></td></tr><tr><td><strong><span>GC范围不适配organism</span></strong></td><td><span>🟡 中</span></td><td><span>高 (70%)</span></td><td><span>cds_optimizer</span></td><td><strong><span>P1 - 1周内</span></strong></td></tr><tr><td><strong><span>framework默认值不适合真核</span></strong></td><td><span>🟡 中</span></td><td><span>中 (50%)</span></td><td><span>assembly_simulator</span></td><td><strong><span>P1 - 1周内</span></strong></td></tr><tr><td><strong><span>Tm值不匹配应用场景</span></strong></td><td><span>🟡 中</span></td><td><span>中 (40%)</span></td><td><span>primer_designer</span></td><td><strong><span>P2 - 2周内</span></strong></td></tr><tr><td><strong><span>AI补全不透明</span></strong></td><td><span>🟢 低</span></td><td><span>高 (80%)</span></td><td><span>所有工具</span></td><td><strong><span>P2 - 2周内</span></strong></td></tr></tbody></table></div><hr><h2><span>工作流参数一致性</span></h2><h3><span>全局参数定义</span></h3><p class="ds-markdown-paragraph"><span>以下参数必须在整个工作流中保持一致：</span></p><div class="ds-scroll-area _1210dd7 c03cafe9"><div class="ds-scroll-area__gutters" style="position: sticky; top: 0px; left: 0px; right: 0px; height: 0px; --container-height: 208px;"><div class="ds-scroll-area__horizontal-gutter" style="left: 0px; right: 0px; top: calc(var(--container-height) - 14px); height: 10px;"><div class="ds-scroll-area__horizontal-bar" style="display: none;"></div></div><div class="ds-scroll-area__vertical-gutter" style="right: 0px; top: 8px; bottom: calc(0px - var(--container-height) + 8px); width: 10px;"><div class="ds-scroll-area__vertical-bar" style="display: none;"></div></div></div><table><thead><tr><th><span>全局参数</span></th><th><span>涉及工具</span></th><th><span>一致性要求</span></th><th><span>当前状态</span></th><th><span>验证机制</span></th></tr></thead><tbody><tr><td>`organism`</td><td><span>cds_optimizer, assembly_simulator</span></td><td><strong><span>强制一致</span></strong></td><td><span>❌ 未验证</span></td><td><span>需要添加WorkflowValidator</span></td></tr><tr><td>`enzyme`</td><td><span>cds_optimizer, overhang_designer, assembly_simulator</span></td><td><strong><span>强制一致</span></strong></td><td><span>❌ 未验证</span></td><td><span>需要添加enzyme链验证</span></td></tr><tr><td>`framework`</td><td><span>assembly_simulator, plasmid_visualizer</span></td><td><strong><span>建议一致</span></strong></td><td><span>❌ 未验证</span></td><td><span>建议添加提示</span></td></tr></tbody></table></div><h3><span>参数传递链</span></h3><div class="md-code-block md-code-block-light"><div class="md-code-block-banner-wrap"><div class="md-code-block-banner md-code-block-banner-lite"><div class="_121d384"><div class="d2a24f03"><span class="d813de27">text</span></div><div class="d2a24f03 _246a029"><div class="efa13877"><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon" style="margin-right: 4px;"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.14923 4.02032C7.11191 4.02032 7.87977 4.02017 8.49591 4.07599C9.12122 4.1327 9.65786 4.25188 10.1414 4.53107C10.7201 4.8653 11.2008 5.34591 11.535 5.92462C11.8142 6.40818 11.9333 6.94482 11.9901 7.57013C12.0459 8.18625 12.0457 8.9542 12.0457 9.91681C12.0457 10.8795 12.0459 11.6474 11.9901 12.2635C11.9333 12.8888 11.8142 13.4254 11.535 13.909C11.2008 14.4877 10.7201 14.9683 10.1414 15.3026C9.65786 15.5817 9.12122 15.7009 8.49591 15.7576C7.87977 15.8134 7.1119 15.8133 6.14923 15.8133C5.18661 15.8133 4.41868 15.8134 3.80255 15.7576C3.17724 15.7009 2.6406 15.5817 2.15704 15.3026C1.57834 14.9684 1.09772 14.4877 0.763489 13.909C0.484305 13.4254 0.365123 12.8888 0.308411 12.2635C0.252587 11.6474 0.252747 10.8795 0.252747 9.91681C0.252747 8.95419 0.252603 8.18625 0.308411 7.57013C0.365123 6.94482 0.484305 6.40818 0.763489 5.92462C1.09771 5.3459 1.57833 4.86529 2.15704 4.53107C2.6406 4.25188 3.17724 4.1327 3.80255 4.07599C4.41868 4.02018 5.1866 4.02032 6.14923 4.02032ZM6.14923 5.37775C5.16175 5.37775 4.46628 5.37761 3.9256 5.42657C3.39428 5.47473 3.07853 5.56574 2.83575 5.70587C2.46313 5.92106 2.15348 6.23071 1.93829 6.60333C1.79817 6.84611 1.70715 7.16185 1.659 7.69318C1.61004 8.23385 1.61017 8.92934 1.61017 9.91681C1.61017 10.9043 1.61002 11.5998 1.659 12.1404C1.70715 12.6717 1.79817 12.9875 1.93829 13.2303C2.15349 13.6029 2.46315 13.9126 2.83575 14.1277C3.07853 14.2679 3.39428 14.3589 3.9256 14.407C4.46628 14.456 5.16176 14.4559 6.14923 14.4559C7.13675 14.4559 7.83218 14.456 8.37286 14.407C8.90419 14.3589 9.21993 14.2679 9.46271 14.1277C9.83529 13.9126 10.145 13.6029 10.3602 13.2303C10.5003 12.9875 10.5913 12.6718 10.6395 12.1404C10.6884 11.5998 10.6883 10.9043 10.6883 9.91681C10.6883 8.92935 10.6884 8.23385 10.6395 7.69318C10.5913 7.16185 10.5003 6.84611 10.3602 6.60333C10.145 6.23072 9.8353 5.92107 9.46271 5.70587C9.21993 5.56574 8.90418 5.47473 8.37286 5.42657C7.83218 5.3776 7.13676 5.37775 6.14923 5.37775ZM9.80157 0.367981C10.7637 0.367981 11.5313 0.367886 12.1473 0.423645C12.7725 0.480313 13.3093 0.598765 13.7928 0.877747C14.3716 1.21192 14.852 1.69355 15.1863 2.27228C15.4655 2.75575 15.5857 3.29165 15.6424 3.91681C15.6982 4.53301 15.6971 5.30161 15.6971 6.26447V7.8299C15.6971 8.29265 15.6989 8.58994 15.6649 8.84845C15.4667 10.3525 14.4009 11.5738 12.9832 11.9988V10.5467C13.6973 10.1903 14.2104 9.49662 14.3192 8.67169C14.3387 8.52348 14.3406 8.3358 14.3406 7.8299V6.26447C14.3406 5.27707 14.3398 4.58149 14.2908 4.04083C14.2427 3.50969 14.1526 3.19373 14.0125 2.95099C13.7974 2.5785 13.4875 2.2687 13.1151 2.05353C12.8723 1.91347 12.5563 1.82237 12.0252 1.77423C11.4846 1.72528 10.7888 1.7254 9.80157 1.7254H7.71466C6.75614 1.72559 5.92659 2.27697 5.52325 3.07892H4.07013C4.54215 1.51132 5.99314 0.368192 7.71466 0.367981H9.80157Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">复制</span></span><div class="ds-focus-ring"></div></button><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M15.3695 11.411L15.1234 12.8866C14.8869 14.3042 13.6603 15.3436 12.223 15.3436H3.7767C2.33954 15.3434 1.11276 14.3042 0.876312 12.8866L0.630219 11.411L2.05405 11.1747L2.29916 12.6493C2.41969 13.3713 3.04472 13.9001 3.7767 13.9003H12.223C12.9551 13.9002 13.58 13.3713 13.7005 12.6493L13.9456 11.1747L15.3695 11.411ZM8.72202 8.994C8.77714 8.93934 8.83789 8.88106 8.90268 8.81627L12.4828 5.23424L13.5042 6.25572L9.92221 9.8358C9.63947 10.1185 9.3876 10.3732 9.15854 10.5575C8.91889 10.7503 8.6395 10.9224 8.28647 10.9784C8.09708 11.0083 7.9036 11.0083 7.7142 10.9784C7.36103 10.9224 7.08087 10.7503 6.84116 10.5575C6.61212 10.3732 6.36019 10.1185 6.07748 9.8358L2.49643 6.25572L3.51694 5.23424L7.09702 8.81627C7.16216 8.88142 7.22327 8.94006 7.27866 8.99498V1.3065H8.72202V8.994Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">下载</span></span><div class="ds-focus-ring"></div></button></div></div></div></div></div><pre>用户输入: sequence, organism
    ↓
[cds_optimizer]
    • sequence (用户输入)
    • organism (用户输入/AI推断)
    • avoid_enzymes (AI补全 - Golden Gate)
    • gc_range (默认/AI动态调整)
    ↓ 输出: optimized_sequence
    ↓
[overhang_designer]
    • num_overhangs (AI计算 - n+1规则)
    • enzyme (继承 - 与cds一致)
    • existing_overhangs (AI提取 - 框架)
    ↓ 输出: designed_overhangs
    ↓
[assembly_simulator]
    • fragments (自动组合 - 前序输出)
    • enzyme (继承 - 全局一致)
    • framework (AI选择 - 基于organism)
    • include_reports (默认true)
    ↓ 输出: final_sequence
    ↓
[plasmid_visualizer]
    • sequence (传递 - assembly输出)
    • features (AI识别 - 框架定义)
    • plasmid_name (AI生成 - 描述性)
    • circular (AI推断 - 类型判断)
    • output_format (默认/用户需求)
    ↓ 输出: image_path, image_base64

独立分支:
[primer_designer]
    • sequence (DNA→RNA转换)
    • min_tm (默认/AI应用调整)
    • min_length, max_length (默认/AI长度优化)
    • prefix (AI项目命名)</pre><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _33882ae"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _28d7e84"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg></div>

---

### 用户

把所有内容转换为md格式

---

### DeepSeek AI

<p>思考：</p><blockquote><p class="ds-markdown-paragraph"><span>我们有一个包含五个工具的工具集，每个工具都有其基本信息、输入参数（分为用户输入、默认值和AI自动补全）、输出参数以及AI自动补全合理性分析。</span><br><span>现在需要将整个内容转换为markdown格式。注意，原始内容中已经有一部分是markdown表格，但我们需要统一格式，并确保所有内容都以markdown形式呈现。</span></p><p class="ds-markdown-paragraph"><span>步骤：</span></p><ol start="1"><li><p class="ds-markdown-paragraph"><span>将每个工具的信息按照以下结构组织：</span></p><ul><li><p class="ds-markdown-paragraph"><span>工具名称（作为标题）</span></p></li><li><p class="ds-markdown-paragraph"><span>基本信息（表格）</span></p></li><li><p class="ds-markdown-paragraph"><span>输入参数（分为三个子标题：用户输入、默认值、AI自动补全，每个部分用表格展示）</span></p></li><li><p class="ds-markdown-paragraph"><span>输出参数（用代码块展示JSON示例）</span></p></li><li><p class="ds-markdown-paragraph"><span>AI自动补全合理性分析（表格）</span></p></li></ul></li><li><p class="ds-markdown-paragraph"><span>最后，我们还有一个总体评估部分，包括总体评分、各工具评分汇总、优势分析、风险点汇总和工作流参数一致性。</span></p></li></ol><p class="ds-markdown-paragraph"><span>注意：原始内容中有些表格已经用markdown表示，有些是文本。我们将统一转换为markdown表格。</span></p><p class="ds-markdown-paragraph"><span>由于内容较长，我们将逐个工具进行转换。</span></p><p class="ds-markdown-paragraph"><span>开始转换：</span></p></blockquote><br/><h1><span>合成生物学工具集AI自动补全合理性分析报告</span></h1><h2><span>工具1: cds_optimizer</span></h2><h3><span>基本信息</span></h3><ul><li><p class="ds-markdown-paragraph"><strong><span>名称</span></strong><span>: </span>`cds_optimizer`</p></li><li><p class="ds-markdown-paragraph"><strong><span>功能</span></strong><span>: 优化编码序列(CDS)的密码子使用，提高在目标生物中的表达效率</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>底层库</span></strong><span>: DnaChisel</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>代码位置</span></strong><span>: </span>`synth_tools/dna_chisel_wrapper.py`</p></li></ul><h3><span>输入参数</span></h3><h4><span>用户输入 (Required)</span></h4><div class="ds-scroll-area _1210dd7 c03cafe9"><div class="ds-scroll-area__gutters" style="position: sticky; top: 0px; left: 0px; right: 0px; height: 0px; --container-height: 362px;"><div class="ds-scroll-area__horizontal-gutter" style="left: 0px; right: 0px; top: calc(var(--container-height) - 14px); height: 10px;"><div class="ds-scroll-area__horizontal-bar" style="display: none;"></div></div><div class="ds-scroll-area__vertical-gutter" style="right: 0px; top: 8px; bottom: calc(0px - var(--container-height) + 8px); width: 10px;"><div class="ds-scroll-area__vertical-bar" style="display: none;"></div></div></div><table><thead><tr><th><span>参数名</span></th><th><span>类型</span></th><th><span>描述</span></th><th><span>验证规则</span></th><th><span>示例</span></th></tr></thead><tbody><tr><td>`sequence`</td><td><span>string</span></td><td><span>DNA序列(ATCG格式)</span></td><td><span>• 只能包含ATCG</span><br><span>• 长度必须是3的倍数</span><br><span>• 自动清理空白字符</span></td><td>`"ATGAAACGCATTAGCACC"`</td></tr><tr><td>`organism`</td><td><span>string</span></td><td><span>目标表达生物</span></td><td><span>• 限定枚举值:</span><br><span>  - e_coli</span><br><span>  - yeast</span><br><span>  - human</span><br><span>  - arabidopsis</span><br><span>  - s_cerevisiae</span><br><span>  - h_sapiens</span><br><span>  - a_thaliana</span></td><td>`"e_coli"`</td></tr></tbody></table></div><h4><span>默认值 (Optional)</span></h4><div class="ds-scroll-area _1210dd7 c03cafe9"><div class="ds-scroll-area__gutters" style="position: sticky; top: 0px; left: 0px; right: 0px; height: 0px; --container-height: 137px;"><div class="ds-scroll-area__horizontal-gutter" style="left: 0px; right: 0px; top: calc(var(--container-height) - 14px); height: 10px;"><div class="ds-scroll-area__horizontal-bar" style="display: none;"></div></div><div class="ds-scroll-area__vertical-gutter" style="right: 0px; top: 8px; bottom: calc(0px - var(--container-height) + 8px); width: 10px;"><div class="ds-scroll-area__vertical-bar" style="display: none;"></div></div></div><table><thead><tr><th><span>参数名</span></th><th><span>类型</span></th><th><span>默认值</span></th><th><span>配置来源</span></th><th><span>描述</span></th></tr></thead><tbody><tr><td>`avoid_enzymes`</td><td><span>array</span></td><td>`[]`</td><td>`DNACHISEL_CONFIG['forbidden_enzymes']`</td><td><span>要避免的限制性酶列表</span></td></tr><tr><td>`gc_range`</td><td><span>array</span></td><td>`[0.4, 0.6]`</td><td>`DNACHISEL_CONFIG['default_gc_bounds']`</td><td><span>目标GC含量范围 [min, max]</span></td></tr></tbody></table></div><h4><span>AI自动补全</span></h4><div class="ds-scroll-area _1210dd7 c03cafe9"><div class="ds-scroll-area__gutters" style="position: sticky; top: 0px; left: 0px; right: 0px; height: 0px; --container-height: 383px;"><div class="ds-scroll-area__horizontal-gutter" style="left: 0px; right: 0px; top: calc(var(--container-height) - 14px); height: 10px;"><div class="ds-scroll-area__horizontal-bar" style="display: none;"></div></div><div class="ds-scroll-area__vertical-gutter" style="right: 0px; top: 8px; bottom: calc(0px - var(--container-height) + 8px); width: 10px;"><div class="ds-scroll-area__vertical-bar" style="display: none;"></div></div></div><table><thead><tr><th><span>参数名</span></th><th><span>补全策略</span></th><th><span>数据来源</span></th><th><span>AI推理逻辑</span></th><th><span>示例</span></th></tr></thead><tbody><tr><td>`organism`</td><td><span>从用户描述提取</span></td><td><span>用户对话内容</span></td><td><span>关键词匹配:</span><br><span>• "大肠杆菌" → </span>`e_coli`<br><span>• "酵母" → </span>`yeast`<br><span>• "人源" → </span>`human`</td><td><span>用户: "优化用于大肠杆菌表达"</span><br><span>→ </span>`organism="e_coli"`</td></tr><tr><td>`avoid_enzymes`</td><td><span>根据后续工作流推断</span></td><td><span>工作流上下文</span></td><td><span>如果提到Golden Gate组装:</span><br><span>→ </span>`["BsaI", "BbsI"]`</td><td><span>用户: "需要Golden Gate组装"</span><br><span>→ </span>`avoid_enzymes=["BsaI"]`</td></tr><tr><td>`gc_range`</td><td><span>根据organism动态调整</span></td><td><span>生物学知识库</span></td><td><span>不同生物的最优GC范围:</span><br><span>• E.coli: [0.4, 0.6]</span><br><span>• Yeast: [0.45, 0.55]</span><br><span>• Human: [0.4, 0.55]</span><br><span>• Arabidopsis: [0.35, 0.45]</span></td><td>`organism="yeast"`<br><span>→ </span>`gc_range=[0.45, 0.55]`</td></tr></tbody></table></div><h3><span>输出参数</span></h3><div class="md-code-block md-code-block-light"><div class="md-code-block-banner-wrap"><div class="md-code-block-banner md-code-block-banner-lite"><div class="_121d384"><div class="d2a24f03"><span class="d813de27">json</span></div><div class="d2a24f03 _246a029"><div class="efa13877"><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon" style="margin-right: 4px;"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.14923 4.02032C7.11191 4.02032 7.87977 4.02017 8.49591 4.07599C9.12122 4.1327 9.65786 4.25188 10.1414 4.53107C10.7201 4.8653 11.2008 5.34591 11.535 5.92462C11.8142 6.40818 11.9333 6.94482 11.9901 7.57013C12.0459 8.18625 12.0457 8.9542 12.0457 9.91681C12.0457 10.8795 12.0459 11.6474 11.9901 12.2635C11.9333 12.8888 11.8142 13.4254 11.535 13.909C11.2008 14.4877 10.7201 14.9683 10.1414 15.3026C9.65786 15.5817 9.12122 15.7009 8.49591 15.7576C7.87977 15.8134 7.1119 15.8133 6.14923 15.8133C5.18661 15.8133 4.41868 15.8134 3.80255 15.7576C3.17724 15.7009 2.6406 15.5817 2.15704 15.3026C1.57834 14.9684 1.09772 14.4877 0.763489 13.909C0.484305 13.4254 0.365123 12.8888 0.308411 12.2635C0.252587 11.6474 0.252747 10.8795 0.252747 9.91681C0.252747 8.95419 0.252603 8.18625 0.308411 7.57013C0.365123 6.94482 0.484305 6.40818 0.763489 5.92462C1.09771 5.3459 1.57833 4.86529 2.15704 4.53107C2.6406 4.25188 3.17724 4.1327 3.80255 4.07599C4.41868 4.02018 5.1866 4.02032 6.14923 4.02032ZM6.14923 5.37775C5.16175 5.37775 4.46628 5.37761 3.9256 5.42657C3.39428 5.47473 3.07853 5.56574 2.83575 5.70587C2.46313 5.92106 2.15348 6.23071 1.93829 6.60333C1.79817 6.84611 1.70715 7.16185 1.659 7.69318C1.61004 8.23385 1.61017 8.92934 1.61017 9.91681C1.61017 10.9043 1.61002 11.5998 1.659 12.1404C1.70715 12.6717 1.79817 12.9875 1.93829 13.2303C2.15349 13.6029 2.46315 13.9126 2.83575 14.1277C3.07853 14.2679 3.39428 14.3589 3.9256 14.407C4.46628 14.456 5.16176 14.4559 6.14923 14.4559C7.13675 14.4559 7.83218 14.456 8.37286 14.407C8.90419 14.3589 9.21993 14.2679 9.46271 14.1277C9.83529 13.9126 10.145 13.6029 10.3602 13.2303C10.5003 12.9875 10.5913 12.6718 10.6395 12.1404C10.6884 11.5998 10.6883 10.9043 10.6883 9.91681C10.6883 8.92935 10.6884 8.23385 10.6395 7.69318C10.5913 7.16185 10.5003 6.84611 10.3602 6.60333C10.145 6.23072 9.8353 5.92107 9.46271 5.70587C9.21993 5.56574 8.90418 5.47473 8.37286 5.42657C7.83218 5.3776 7.13676 5.37775 6.14923 5.37775ZM9.80157 0.367981C10.7637 0.367981 11.5313 0.367886 12.1473 0.423645C12.7725 0.480313 13.3093 0.598765 13.7928 0.877747C14.3716 1.21192 14.852 1.69355 15.1863 2.27228C15.4655 2.75575 15.5857 3.29165 15.6424 3.91681C15.6982 4.53301 15.6971 5.30161 15.6971 6.26447V7.8299C15.6971 8.29265 15.6989 8.58994 15.6649 8.84845C15.4667 10.3525 14.4009 11.5738 12.9832 11.9988V10.5467C13.6973 10.1903 14.2104 9.49662 14.3192 8.67169C14.3387 8.52348 14.3406 8.3358 14.3406 7.8299V6.26447C14.3406 5.27707 14.3398 4.58149 14.2908 4.04083C14.2427 3.50969 14.1526 3.19373 14.0125 2.95099C13.7974 2.5785 13.4875 2.2687 13.1151 2.05353C12.8723 1.91347 12.5563 1.82237 12.0252 1.77423C11.4846 1.72528 10.7888 1.7254 9.80157 1.7254H7.71466C6.75614 1.72559 5.92659 2.27697 5.52325 3.07892H4.07013C4.54215 1.51132 5.99314 0.368192 7.71466 0.367981H9.80157Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">复制</span></span><div class="ds-focus-ring"></div></button><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M15.3695 11.411L15.1234 12.8866C14.8869 14.3042 13.6603 15.3436 12.223 15.3436H3.7767C2.33954 15.3434 1.11276 14.3042 0.876312 12.8866L0.630219 11.411L2.05405 11.1747L2.29916 12.6493C2.41969 13.3713 3.04472 13.9001 3.7767 13.9003H12.223C12.9551 13.9002 13.58 13.3713 13.7005 12.6493L13.9456 11.1747L15.3695 11.411ZM8.72202 8.994C8.77714 8.93934 8.83789 8.88106 8.90268 8.81627L12.4828 5.23424L13.5042 6.25572L9.92221 9.8358C9.63947 10.1185 9.3876 10.3732 9.15854 10.5575C8.91889 10.7503 8.6395 10.9224 8.28647 10.9784C8.09708 11.0083 7.9036 11.0083 7.7142 10.9784C7.36103 10.9224 7.08087 10.7503 6.84116 10.5575C6.61212 10.3732 6.36019 10.1185 6.07748 9.8358L2.49643 6.25572L3.51694 5.23424L7.09702 8.81627C7.16216 8.88142 7.22327 8.94006 7.27866 8.99498V1.3065H8.72202V8.994Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">下载</span></span><div class="ds-focus-ring"></div></button></div></div></div></div></div><pre><span class="token punctuation">{</span>
  <span class="token property">"success"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
  <span class="token property">"original_sequence"</span><span class="token operator">:</span> <span class="token string">"ATGAAACGCATTAGCACC"</span><span class="token punctuation">,</span>
  <span class="token property">"optimized_sequence"</span><span class="token operator">:</span> <span class="token string">"ATGAAACGTCTGGCCCCT"</span><span class="token punctuation">,</span>
  <span class="token property">"statistics"</span><span class="token operator">:</span> <span class="token punctuation">{</span>
    <span class="token property">"sequence_length"</span><span class="token operator">:</span> <span class="token number">18</span><span class="token punctuation">,</span>
    <span class="token property">"original_gc_content"</span><span class="token operator">:</span> <span class="token number">0.389</span><span class="token punctuation">,</span>
    <span class="token property">"optimized_gc_content"</span><span class="token operator">:</span> <span class="token number">0.556</span><span class="token punctuation">,</span>
    <span class="token property">"changes_made"</span><span class="token operator">:</span> <span class="token number">5</span><span class="token punctuation">,</span>
    <span class="token property">"change_percentage"</span><span class="token operator">:</span> <span class="token number">27.78</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token property">"organism"</span><span class="token operator">:</span> <span class="token string">"e_coli"</span><span class="token punctuation">,</span>
  <span class="token property">"avoided_enzymes"</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token string">"BsaI"</span><span class="token punctuation">,</span> <span class="token string">"BbsI"</span><span class="token punctuation">]</span>
<span class="token punctuation">}</span></pre><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _33882ae"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _28d7e84"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg></div><h3><span>AI自动补全合理性分析</span></h3><div class="ds-scroll-area _1210dd7 c03cafe9"><div class="ds-scroll-area__gutters" style="position: sticky; top: 0px; left: 0px; right: 0px; height: 0px; --container-height: 333px;"><div class="ds-scroll-area__horizontal-gutter" style="left: 0px; right: 0px; top: calc(var(--container-height) - 14px); height: 10px;"><div class="ds-scroll-area__horizontal-bar" style="left: 0px; width: 980.305px;"></div></div><div class="ds-scroll-area__vertical-gutter" style="right: 0px; top: 8px; bottom: calc(0px - var(--container-height) + 8px); width: 10px;"><div class="ds-scroll-area__vertical-bar" style="display: none;"></div></div></div><table><thead><tr><th><span>参数</span></th><th><span>评分</span></th><th><span>合理性</span></th><th><span>风险点</span></th><th><span>改进建议</span></th></tr></thead><tbody><tr><td>`organism`</td><td><span>⭐⭐⭐⭐⭐ (5/5)</span></td><td><strong><span>非常合理</span></strong></td><td><span>• 低: AI可准确从用户描述提取</span><br><span>• 但应该让用户确认</span></td><td><span>补全后明确告知用户:</span><br><span>"已选择organism=e_coli，根据您提到的'大肠杆菌表达'"</span></td></tr><tr><td>`avoid_enzymes`</td><td><span>⭐⭐⭐⭐☆ (4/5)</span></td><td><strong><span>基本合理</span></strong></td><td><span>• 中: 如果用户未提到Golden Gate，不应自动添加</span><br><span>• 可能与用户实际需求不符</span></td><td><span>仅在用户明确提到Golden Gate/Type IIS assembly时自动添加</span></td></tr><tr><td>`gc_range`</td><td><span>⭐⭐⭐☆☆ (3/5)</span></td><td><strong><span>部分合理</span></strong></td><td><span>• 高: 固定默认值[0.4-0.6]不适合所有生物</span><br><span>• 真核生物可能需要更窄范围</span></td><td><strong><span>必须改进</span></strong><span>: 实现</span>`SmartDefaults.get_gc_range(organism)`<span>动态返回</span></td></tr></tbody></table></div><hr><h2><span>工具2: overhang_designer</span></h2><h3><span>基本信息</span></h3><ul><li><p class="ds-markdown-paragraph"><strong><span>名称</span></strong><span>: </span>`overhang_designer`</p></li><li><p class="ds-markdown-paragraph"><strong><span>功能</span></strong><span>: 为Golden Gate组装设计最优的4bp overhang序列</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>底层库</span></strong><span>: GoldenHinges</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>代码位置</span></strong><span>: </span>`synth_tools/golden_hinges_wrapper.py`</p></li></ul><h3><span>输入参数</span></h3><h4><span>用户输入 (Required)</span></h4><div class="ds-scroll-area _1210dd7 c03cafe9"><div class="ds-scroll-area__gutters" style="position: sticky; top: 0px; left: 0px; right: 0px; height: 0px; --container-height: 116px;"><div class="ds-scroll-area__horizontal-gutter" style="left: 0px; right: 0px; top: calc(var(--container-height) - 14px); height: 10px;"><div class="ds-scroll-area__horizontal-bar" style="display: none;"></div></div><div class="ds-scroll-area__vertical-gutter" style="right: 0px; top: 8px; bottom: calc(0px - var(--container-height) + 8px); width: 10px;"><div class="ds-scroll-area__vertical-bar" style="display: none;"></div></div></div><table><thead><tr><th><span>参数名</span></th><th><span>类型</span></th><th><span>描述</span></th><th><span>验证规则</span></th><th><span>示例</span></th></tr></thead><tbody><tr><td>`num_overhangs`</td><td><span>integer</span></td><td><span>需要设计的overhang数量</span></td><td><span>• 必须 ≥ 1</span><br><span>• 通常为片段数+1</span></td><td>`3`</td></tr></tbody></table></div><h4><span>默认值 (Optional)</span></h4><div class="ds-scroll-area _1210dd7 c03cafe9"><div class="ds-scroll-area__gutters" style="position: sticky; top: 0px; left: 0px; right: 0px; height: 0px; --container-height: 137px;"><div class="ds-scroll-area__horizontal-gutter" style="left: 0px; right: 0px; top: calc(var(--container-height) - 14px); height: 10px;"><div class="ds-scroll-area__horizontal-bar" style="display: none;"></div></div><div class="ds-scroll-area__vertical-gutter" style="right: 0px; top: 8px; bottom: calc(0px - var(--container-height) + 8px); width: 10px;"><div class="ds-scroll-area__vertical-bar" style="display: none;"></div></div></div><table><thead><tr><th><span>参数名</span></th><th><span>类型</span></th><th><span>默认值</span></th><th><span>配置来源</span></th><th><span>描述</span></th></tr></thead><tbody><tr><td>`enzyme`</td><td><span>string</span></td><td>`"BsaI"`</td><td>`GOLDENHINGES_CONFIG['enzyme']`</td><td><span>使用的限制性酶</span></td></tr><tr><td>`existing_overhangs`</td><td><span>array</span></td><td>`[]`</td><td><span>-</span></td><td><span>已存在的overhang序列，需要避免冲突</span></td></tr></tbody></table></div><h4><span>AI自动补全</span></h4><div class="ds-scroll-area _1210dd7 c03cafe9"><div class="ds-scroll-area__gutters" style="position: sticky; top: 0px; left: 0px; right: 0px; height: 0px; --container-height: 308px;"><div class="ds-scroll-area__horizontal-gutter" style="left: 0px; right: 0px; top: calc(var(--container-height) - 14px); height: 10px;"><div class="ds-scroll-area__horizontal-bar" style="left: 0px; width: 948.185px;"></div></div><div class="ds-scroll-area__vertical-gutter" style="right: 0px; top: 8px; bottom: calc(0px - var(--container-height) + 8px); width: 10px;"><div class="ds-scroll-area__vertical-bar" style="display: none;"></div></div></div><table><thead><tr><th><span>参数名</span></th><th><span>补全策略</span></th><th><span>数据来源</span></th><th><span>AI推理逻辑</span></th><th><span>示例</span></th></tr></thead><tbody><tr><td>`num_overhangs`</td><td><span>根据片段数计算</span></td><td><span>组装策略</span></td><td><strong><span>n+1规则</span></strong><span>:</span><br><span>• 单片段插入: 2个(左右)</span><br><span>• n个片段组装: n+1个(包括载体)</span></td><td><span>3个CDS片段 → </span>`num_overhangs=4`</td></tr><tr><td>`enzyme`</td><td><span>从前序工具继承</span></td><td>`cds_optimizer`<span>的</span>`avoid_enzymes`</td><td><span>• 如果CDS优化避免了BsaI → 使用</span>`"BsaI"`<br><span>• 如果避免了BsaI和BbsI → 使用</span>`"BsmBI"`</td><td>`cds_optimizer`<span>使用BsaI</span><br><span>→ </span>`enzyme="BsaI"`</td></tr><tr><td>`existing_overhangs`</td><td><span>从质粒框架提取</span></td><td><span>质粒框架定义</span></td><td><span>从</span>`config/plasmid_frameworks.py`<span>提取:</span><br><span>• pET28a → </span>`["AATG", "TTAA"]`<br><span>• pUC19 → </span>`["GCTT", "AATG"]`</td><td><span>framework="pET28a"</span><br><span>→ </span>`existing_overhangs=["AATG", "TTAA"]`</td></tr></tbody></table></div><h3><span>输出参数</span></h3><div class="md-code-block md-code-block-light"><div class="md-code-block-banner-wrap"><div class="md-code-block-banner md-code-block-banner-lite"><div class="_121d384"><div class="d2a24f03"><span class="d813de27">json</span></div><div class="d2a24f03 _246a029"><div class="efa13877"><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon" style="margin-right: 4px;"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.14923 4.02032C7.11191 4.02032 7.87977 4.02017 8.49591 4.07599C9.12122 4.1327 9.65786 4.25188 10.1414 4.53107C10.7201 4.8653 11.2008 5.34591 11.535 5.92462C11.8142 6.40818 11.9333 6.94482 11.9901 7.57013C12.0459 8.18625 12.0457 8.9542 12.0457 9.91681C12.0457 10.8795 12.0459 11.6474 11.9901 12.2635C11.9333 12.8888 11.8142 13.4254 11.535 13.909C11.2008 14.4877 10.7201 14.9683 10.1414 15.3026C9.65786 15.5817 9.12122 15.7009 8.49591 15.7576C7.87977 15.8134 7.1119 15.8133 6.14923 15.8133C5.18661 15.8133 4.41868 15.8134 3.80255 15.7576C3.17724 15.7009 2.6406 15.5817 2.15704 15.3026C1.57834 14.9684 1.09772 14.4877 0.763489 13.909C0.484305 13.4254 0.365123 12.8888 0.308411 12.2635C0.252587 11.6474 0.252747 10.8795 0.252747 9.91681C0.252747 8.95419 0.252603 8.18625 0.308411 7.57013C0.365123 6.94482 0.484305 6.40818 0.763489 5.92462C1.09771 5.3459 1.57833 4.86529 2.15704 4.53107C2.6406 4.25188 3.17724 4.1327 3.80255 4.07599C4.41868 4.02018 5.1866 4.02032 6.14923 4.02032ZM6.14923 5.37775C5.16175 5.37775 4.46628 5.37761 3.9256 5.42657C3.39428 5.47473 3.07853 5.56574 2.83575 5.70587C2.46313 5.92106 2.15348 6.23071 1.93829 6.60333C1.79817 6.84611 1.70715 7.16185 1.659 7.69318C1.61004 8.23385 1.61017 8.92934 1.61017 9.91681C1.61017 10.9043 1.61002 11.5998 1.659 12.1404C1.70715 12.6717 1.79817 12.9875 1.93829 13.2303C2.15349 13.6029 2.46315 13.9126 2.83575 14.1277C3.07853 14.2679 3.39428 14.3589 3.9256 14.407C4.46628 14.456 5.16176 14.4559 6.14923 14.4559C7.13675 14.4559 7.83218 14.456 8.37286 14.407C8.90419 14.3589 9.21993 14.2679 9.46271 14.1277C9.83529 13.9126 10.145 13.6029 10.3602 13.2303C10.5003 12.9875 10.5913 12.6718 10.6395 12.1404C10.6884 11.5998 10.6883 10.9043 10.6883 9.91681C10.6883 8.92935 10.6884 8.23385 10.6395 7.69318C10.5913 7.16185 10.5003 6.84611 10.3602 6.60333C10.145 6.23072 9.8353 5.92107 9.46271 5.70587C9.21993 5.56574 8.90418 5.47473 8.37286 5.42657C7.83218 5.3776 7.13676 5.37775 6.14923 5.37775ZM9.80157 0.367981C10.7637 0.367981 11.5313 0.367886 12.1473 0.423645C12.7725 0.480313 13.3093 0.598765 13.7928 0.877747C14.3716 1.21192 14.852 1.69355 15.1863 2.27228C15.4655 2.75575 15.5857 3.29165 15.6424 3.91681C15.6982 4.53301 15.6971 5.30161 15.6971 6.26447V7.8299C15.6971 8.29265 15.6989 8.58994 15.6649 8.84845C15.4667 10.3525 14.4009 11.5738 12.9832 11.9988V10.5467C13.6973 10.1903 14.2104 9.49662 14.3192 8.67169C14.3387 8.52348 14.3406 8.3358 14.3406 7.8299V6.26447C14.3406 5.27707 14.3398 4.58149 14.2908 4.04083C14.2427 3.50969 14.1526 3.19373 14.0125 2.95099C13.7974 2.5785 13.4875 2.2687 13.1151 2.05353C12.8723 1.91347 12.5563 1.82237 12.0252 1.77423C11.4846 1.72528 10.7888 1.7254 9.80157 1.7254H7.71466C6.75614 1.72559 5.92659 2.27697 5.52325 3.07892H4.07013C4.54215 1.51132 5.99314 0.368192 7.71466 0.367981H9.80157Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">复制</span></span><div class="ds-focus-ring"></div></button><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M15.3695 11.411L15.1234 12.8866C14.8869 14.3042 13.6603 15.3436 12.223 15.3436H3.7767C2.33954 15.3434 1.11276 14.3042 0.876312 12.8866L0.630219 11.411L2.05405 11.1747L2.29916 12.6493C2.41969 13.3713 3.04472 13.9001 3.7767 13.9003H12.223C12.9551 13.9002 13.58 13.3713 13.7005 12.6493L13.9456 11.1747L15.3695 11.411ZM8.72202 8.994C8.77714 8.93934 8.83789 8.88106 8.90268 8.81627L12.4828 5.23424L13.5042 6.25572L9.92221 9.8358C9.63947 10.1185 9.3876 10.3732 9.15854 10.5575C8.91889 10.7503 8.6395 10.9224 8.28647 10.9784C8.09708 11.0083 7.9036 11.0083 7.7142 10.9784C7.36103 10.9224 7.08087 10.7503 6.84116 10.5575C6.61212 10.3732 6.36019 10.1185 6.07748 9.8358L2.49643 6.25572L3.51694 5.23424L7.09702 8.81627C7.16216 8.88142 7.22327 8.94006 7.27866 8.99498V1.3065H8.72202V8.994Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">下载</span></span><div class="ds-focus-ring"></div></button></div></div></div></div></div><pre><span class="token punctuation">{</span>
  <span class="token property">"success"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
  <span class="token property">"designed_overhangs"</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token string">"AATG"</span><span class="token punctuation">,</span> <span class="token string">"CCGA"</span><span class="token punctuation">,</span> <span class="token string">"TTGC"</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
  <span class="token property">"enzyme"</span><span class="token operator">:</span> <span class="token string">"BsaI"</span><span class="token punctuation">,</span>
  <span class="token property">"statistics"</span><span class="token operator">:</span> <span class="token punctuation">{</span>
    <span class="token property">"requested"</span><span class="token operator">:</span> <span class="token number">3</span><span class="token punctuation">,</span>
    <span class="token property">"designed"</span><span class="token operator">:</span> <span class="token number">3</span><span class="token punctuation">,</span>
    <span class="token property">"existing_avoided"</span><span class="token operator">:</span> <span class="token number">2</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token property">"compatibility"</span><span class="token operator">:</span> <span class="token punctuation">{</span>
    <span class="token property">"enzyme"</span><span class="token operator">:</span> <span class="token string">"BsaI"</span><span class="token punctuation">,</span>
    <span class="token property">"overhang_length"</span><span class="token operator">:</span> <span class="token number">4</span><span class="token punctuation">,</span>
    <span class="token property">"gc_range"</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token number">0.25</span><span class="token punctuation">,</span> <span class="token number">0.75</span><span class="token punctuation">]</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span></pre><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _33882ae"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _28d7e84"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg></div><h3><span>AI自动补全合理性分析</span></h3><div class="ds-scroll-area _1210dd7 c03cafe9"><div class="ds-scroll-area__gutters" style="position: sticky; top: 0px; left: 0px; right: 0px; height: 0px; --container-height: 258px;"><div class="ds-scroll-area__horizontal-gutter" style="left: 0px; right: 0px; top: calc(var(--container-height) - 14px); height: 10px;"><div class="ds-scroll-area__horizontal-bar" style="left: 0px; width: 965.264px;"></div></div><div class="ds-scroll-area__vertical-gutter" style="right: 0px; top: 8px; bottom: calc(0px - var(--container-height) + 8px); width: 10px;"><div class="ds-scroll-area__vertical-bar" style="display: none;"></div></div></div><table><thead><tr><th><span>参数</span></th><th><span>评分</span></th><th><span>合理性</span></th><th><span>风险点</span></th><th><span>改进建议</span></th></tr></thead><tbody><tr><td>`num_overhangs`</td><td><span>⭐⭐⭐⭐⭐ (5/5)</span></td><td><strong><span>非常合理</span></strong></td><td><span>• 极低: n+1规则是Golden Gate标准</span></td><td><span>补全时明确说明计算逻辑:</span><br><span>"3个片段需要4个overhangs (n+1规则)"</span></td></tr><tr><td>`enzyme`</td><td><span>⭐⭐⭐⭐⭐ (5/5)</span></td><td><strong><span>非常合理</span></strong></td><td><span>• 低: 必须与CDS优化保持一致</span></td><td><strong><span>强制验证</span></strong><span>: 添加一致性检查器，确保整个工作流使用相同enzyme</span></td></tr><tr><td>`existing_overhangs`</td><td><span>⭐⭐⭐⭐☆ (4/5)</span></td><td><strong><span>基本合理</span></strong></td><td><span>• 中: 如果用户使用非标准框架，提取可能失败</span></td><td><span>提取框架overhangs时，告知用户:</span><br><span>"从pET28a框架提取了2个固定overhangs"</span></td></tr></tbody></table></div><hr><h2><span>工具3: assembly_simulator</span></h2><h3><span>基本信息</span></h3><ul><li><p class="ds-markdown-paragraph"><strong><span>名称</span></strong><span>: </span>`assembly_simulator`</p></li><li><p class="ds-markdown-paragraph"><strong><span>功能</span></strong><span>: 使用DnaCauldron模拟Golden Gate组装过程</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>底层库</span></strong><span>: DnaCauldron</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>代码位置</span></strong><span>: </span>`synth_tools/dna_cauldron_wrapper.py`</p></li></ul><h3><span>输入参数</span></h3><h4><span>用户输入 (Required)</span></h4><div class="ds-scroll-area _1210dd7 c03cafe9"><div class="ds-scroll-area__gutters" style="position: sticky; top: 0px; left: 0px; right: 0px; height: 0px; --container-height: 91px;"><div class="ds-scroll-area__horizontal-gutter" style="left: 0px; right: 0px; top: calc(var(--container-height) - 14px); height: 10px;"><div class="ds-scroll-area__horizontal-bar" style="display: none;"></div></div><div class="ds-scroll-area__vertical-gutter" style="right: 0px; top: 8px; bottom: calc(0px - var(--container-height) + 8px); width: 10px;"><div class="ds-scroll-area__vertical-bar" style="display: none;"></div></div></div><table><thead><tr><th><span>参数名</span></th><th><span>类型</span></th><th><span>描述</span></th><th><span>验证规则</span></th><th><span>支持的格式</span></th></tr></thead><tbody><tr><td>`fragments`</td><td><span>object</span></td><td><span>Fragment信息</span></td><td><span>必须包含序列和overhang</span></td><td><span>支持4种格式（见下）</span></td></tr></tbody></table></div><p class="ds-markdown-paragraph"><strong><span>支持的fragments格式</span></strong><span>:</span></p><div class="md-code-block md-code-block-light"><div class="md-code-block-banner-wrap"><div class="md-code-block-banner md-code-block-banner-lite"><div class="_121d384"><div class="d2a24f03"><span class="d813de27">json</span></div><div class="d2a24f03 _246a029"><div class="efa13877"><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon" style="margin-right: 4px;"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.14923 4.02032C7.11191 4.02032 7.87977 4.02017 8.49591 4.07599C9.12122 4.1327 9.65786 4.25188 10.1414 4.53107C10.7201 4.8653 11.2008 5.34591 11.535 5.92462C11.8142 6.40818 11.9333 6.94482 11.9901 7.57013C12.0459 8.18625 12.0457 8.9542 12.0457 9.91681C12.0457 10.8795 12.0459 11.6474 11.9901 12.2635C11.9333 12.8888 11.8142 13.4254 11.535 13.909C11.2008 14.4877 10.7201 14.9683 10.1414 15.3026C9.65786 15.5817 9.12122 15.7009 8.49591 15.7576C7.87977 15.8134 7.1119 15.8133 6.14923 15.8133C5.18661 15.8133 4.41868 15.8134 3.80255 15.7576C3.17724 15.7009 2.6406 15.5817 2.15704 15.3026C1.57834 14.9684 1.09772 14.4877 0.763489 13.909C0.484305 13.4254 0.365123 12.8888 0.308411 12.2635C0.252587 11.6474 0.252747 10.8795 0.252747 9.91681C0.252747 8.95419 0.252603 8.18625 0.308411 7.57013C0.365123 6.94482 0.484305 6.40818 0.763489 5.92462C1.09771 5.3459 1.57833 4.86529 2.15704 4.53107C2.6406 4.25188 3.17724 4.1327 3.80255 4.07599C4.41868 4.02018 5.1866 4.02032 6.14923 4.02032ZM6.14923 5.37775C5.16175 5.37775 4.46628 5.37761 3.9256 5.42657C3.39428 5.47473 3.07853 5.56574 2.83575 5.70587C2.46313 5.92106 2.15348 6.23071 1.93829 6.60333C1.79817 6.84611 1.70715 7.16185 1.659 7.69318C1.61004 8.23385 1.61017 8.92934 1.61017 9.91681C1.61017 10.9043 1.61002 11.5998 1.659 12.1404C1.70715 12.6717 1.79817 12.9875 1.93829 13.2303C2.15349 13.6029 2.46315 13.9126 2.83575 14.1277C3.07853 14.2679 3.39428 14.3589 3.9256 14.407C4.46628 14.456 5.16176 14.4559 6.14923 14.4559C7.13675 14.4559 7.83218 14.456 8.37286 14.407C8.90419 14.3589 9.21993 14.2679 9.46271 14.1277C9.83529 13.9126 10.145 13.6029 10.3602 13.2303C10.5003 12.9875 10.5913 12.6718 10.6395 12.1404C10.6884 11.5998 10.6883 10.9043 10.6883 9.91681C10.6883 8.92935 10.6884 8.23385 10.6395 7.69318C10.5913 7.16185 10.5003 6.84611 10.3602 6.60333C10.145 6.23072 9.8353 5.92107 9.46271 5.70587C9.21993 5.56574 8.90418 5.47473 8.37286 5.42657C7.83218 5.3776 7.13676 5.37775 6.14923 5.37775ZM9.80157 0.367981C10.7637 0.367981 11.5313 0.367886 12.1473 0.423645C12.7725 0.480313 13.3093 0.598765 13.7928 0.877747C14.3716 1.21192 14.852 1.69355 15.1863 2.27228C15.4655 2.75575 15.5857 3.29165 15.6424 3.91681C15.6982 4.53301 15.6971 5.30161 15.6971 6.26447V7.8299C15.6971 8.29265 15.6989 8.58994 15.6649 8.84845C15.4667 10.3525 14.4009 11.5738 12.9832 11.9988V10.5467C13.6973 10.1903 14.2104 9.49662 14.3192 8.67169C14.3387 8.52348 14.3406 8.3358 14.3406 7.8299V6.26447C14.3406 5.27707 14.3398 4.58149 14.2908 4.04083C14.2427 3.50969 14.1526 3.19373 14.0125 2.95099C13.7974 2.5785 13.4875 2.2687 13.1151 2.05353C12.8723 1.91347 12.5563 1.82237 12.0252 1.77423C11.4846 1.72528 10.7888 1.7254 9.80157 1.7254H7.71466C6.75614 1.72559 5.92659 2.27697 5.52325 3.07892H4.07013C4.54215 1.51132 5.99314 0.368192 7.71466 0.367981H9.80157Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">复制</span></span><div class="ds-focus-ring"></div></button><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M15.3695 11.411L15.1234 12.8866C14.8869 14.3042 13.6603 15.3436 12.223 15.3436H3.7767C2.33954 15.3434 1.11276 14.3042 0.876312 12.8866L0.630219 11.411L2.05405 11.1747L2.29916 12.6493C2.41969 13.3713 3.04472 13.9001 3.7767 13.9003H12.223C12.9551 13.9002 13.58 13.3713 13.7005 12.6493L13.9456 11.1747L15.3695 11.411ZM8.72202 8.994C8.77714 8.93934 8.83789 8.88106 8.90268 8.81627L12.4828 5.23424L13.5042 6.25572L9.92221 9.8358C9.63947 10.1185 9.3876 10.3732 9.15854 10.5575C8.91889 10.7503 8.6395 10.9224 8.28647 10.9784C8.09708 11.0083 7.9036 11.0083 7.7142 10.9784C7.36103 10.9224 7.08087 10.7503 6.84116 10.5575C6.61212 10.3732 6.36019 10.1185 6.07748 9.8358L2.49643 6.25572L3.51694 5.23424L7.09702 8.81627C7.16216 8.88142 7.22327 8.94006 7.27866 8.99498V1.3065H8.72202V8.994Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">下载</span></span><div class="ds-focus-ring"></div></button></div></div></div></div></div><pre><span class="token comment">// 格式1: 来自overhang_designer</span>
<span class="token punctuation">{</span>
  <span class="token property">"designed_overhangs"</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token string">"AATG"</span><span class="token punctuation">,</span> <span class="token string">"GCTT"</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
  <span class="token property">"cds_sequence"</span><span class="token operator">:</span> <span class="token string">"ATGAAA..."</span>
<span class="token punctuation">}</span>

<span class="token comment">// 格式2: 来自cds_optimizer</span>
<span class="token punctuation">{</span>
  <span class="token property">"optimized_sequence"</span><span class="token operator">:</span> <span class="token string">"ATGAAA..."</span><span class="token punctuation">,</span>
  <span class="token property">"left_overhang"</span><span class="token operator">:</span> <span class="token string">"AATG"</span><span class="token punctuation">,</span>
  <span class="token property">"right_overhang"</span><span class="token operator">:</span> <span class="token string">"GCTT"</span>
<span class="token punctuation">}</span>

<span class="token comment">// 格式3: 直接片段列表</span>
<span class="token punctuation">{</span>
  <span class="token property">"fragments"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
    <span class="token punctuation">{</span>
      <span class="token property">"sequence"</span><span class="token operator">:</span> <span class="token string">"ATGAAA..."</span><span class="token punctuation">,</span>
      <span class="token property">"left_overhang"</span><span class="token operator">:</span> <span class="token string">"AATG"</span><span class="token punctuation">,</span>
      <span class="token property">"right_overhang"</span><span class="token operator">:</span> <span class="token string">"GCTT"</span>
    <span class="token punctuation">}</span>
  <span class="token punctuation">]</span>
<span class="token punctuation">}</span>

<span class="token comment">// 格式4: 简化格式</span>
<span class="token punctuation">{</span>
  <span class="token property">"sequence"</span><span class="token operator">:</span> <span class="token string">"ATGAAA..."</span><span class="token punctuation">,</span>
  <span class="token property">"left_overhang"</span><span class="token operator">:</span> <span class="token string">"AATG"</span><span class="token punctuation">,</span>
  <span class="token property">"right_overhang"</span><span class="token operator">:</span> <span class="token string">"GCTT"</span>
<span class="token punctuation">}</span></pre><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _33882ae"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _28d7e84"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg></div><h4><span>默认值 (Optional)</span></h4><div class="ds-scroll-area _1210dd7 c03cafe9"><div class="ds-scroll-area__gutters" style="position: sticky; top: 0px; left: 0px; right: 0px; height: 0px; --container-height: 204px;"><div class="ds-scroll-area__horizontal-gutter" style="left: 0px; right: 0px; top: calc(var(--container-height) - 14px); height: 10px;"><div class="ds-scroll-area__horizontal-bar" style="display: none;"></div></div><div class="ds-scroll-area__vertical-gutter" style="right: 0px; top: 8px; bottom: calc(0px - var(--container-height) + 8px); width: 10px;"><div class="ds-scroll-area__vertical-bar" style="display: none;"></div></div></div><table><thead><tr><th><span>参数名</span></th><th><span>类型</span></th><th><span>默认值</span></th><th><span>配置来源</span></th><th><span>描述</span></th></tr></thead><tbody><tr><td>`framework`</td><td><span>string</span></td><td>`"pET28a"`</td><td><span>-</span></td><td><span>质粒框架名称</span></td></tr><tr><td>`enzyme`</td><td><span>string</span></td><td>`"BsaI"`</td><td>`DNACAULDRON_CONFIG['enzyme']`</td><td><span>限制性酶</span></td></tr><tr><td>`include_reports`</td><td><span>boolean</span></td><td>`true`</td><td>`DNACAULDRON_CONFIG['include_assembly_plots']`</td><td><span>是否生成详细报告</span></td></tr></tbody></table></div><h4><span>AI自动补全</span></h4><div class="ds-scroll-area _1210dd7 c03cafe9"><div class="ds-scroll-area__gutters" style="position: sticky; top: 0px; left: 0px; right: 0px; height: 0px; --container-height: 358px;"><div class="ds-scroll-area__horizontal-gutter" style="left: 0px; right: 0px; top: calc(var(--container-height) - 14px); height: 10px;"><div class="ds-scroll-area__horizontal-bar" style="left: 0px; width: 965.908px;"></div></div><div class="ds-scroll-area__vertical-gutter" style="right: 0px; top: 8px; bottom: calc(0px - var(--container-height) + 8px); width: 10px;"><div class="ds-scroll-area__vertical-bar" style="display: none;"></div></div></div><table><thead><tr><th><span>参数名</span></th><th><span>补全策略</span></th><th><span>数据来源</span></th><th><span>AI推理逻辑</span></th><th><span>示例</span></th></tr></thead><tbody><tr><td>`fragments`</td><td><span>从前序工具传递</span></td><td>`cds_optimizer`<span> + </span>`overhang_designer`</td><td><span>自动组合前序工具输出:</span><br><span>• optimized_sequence</span><br><span>• designed_overhangs</span></td><td><span>自动构建fragments对象</span></td></tr><tr><td>`framework`</td><td><span>根据organism选择</span></td><td>`cds_optimizer`<span>的organism</span></td><td><strong><span>智能框架选择</span></strong><span>:</span><br><span>• e_coli + His-tag → </span>`"pET28a"`<br><span>• e_coli + GST-tag → </span>`"pGEX-4T"`<br><span>• yeast → </span>`"pYES2"`<br><span>• human → </span>`"pcDNA3.1"`</td><td><span>organism="e_coli", tag="His"</span><br><span>→ </span>`framework="pET28a"`</td></tr><tr><td>`enzyme`</td><td><span>继承前序工具</span></td><td><span>整个工作流的enzyme</span></td><td><span>必须与cds_optimizer和overhang_designer一致</span></td><td><span>全局enzyme="BsaI"</span><br><span>→ </span>`enzyme="BsaI"`</td></tr></tbody></table></div><h3><span>输出参数</span></h3><div class="md-code-block md-code-block-light"><div class="md-code-block-banner-wrap"><div class="md-code-block-banner md-code-block-banner-lite"><div class="_121d384"><div class="d2a24f03"><span class="d813de27">json</span></div><div class="d2a24f03 _246a029"><div class="efa13877"><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon" style="margin-right: 4px;"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.14923 4.02032C7.11191 4.02032 7.87977 4.02017 8.49591 4.07599C9.12122 4.1327 9.65786 4.25188 10.1414 4.53107C10.7201 4.8653 11.2008 5.34591 11.535 5.92462C11.8142 6.40818 11.9333 6.94482 11.9901 7.57013C12.0459 8.18625 12.0457 8.9542 12.0457 9.91681C12.0457 10.8795 12.0459 11.6474 11.9901 12.2635C11.9333 12.8888 11.8142 13.4254 11.535 13.909C11.2008 14.4877 10.7201 14.9683 10.1414 15.3026C9.65786 15.5817 9.12122 15.7009 8.49591 15.7576C7.87977 15.8134 7.1119 15.8133 6.14923 15.8133C5.18661 15.8133 4.41868 15.8134 3.80255 15.7576C3.17724 15.7009 2.6406 15.5817 2.15704 15.3026C1.57834 14.9684 1.09772 14.4877 0.763489 13.909C0.484305 13.4254 0.365123 12.8888 0.308411 12.2635C0.252587 11.6474 0.252747 10.8795 0.252747 9.91681C0.252747 8.95419 0.252603 8.18625 0.308411 7.57013C0.365123 6.94482 0.484305 6.40818 0.763489 5.92462C1.09771 5.3459 1.57833 4.86529 2.15704 4.53107C2.6406 4.25188 3.17724 4.1327 3.80255 4.07599C4.41868 4.02018 5.1866 4.02032 6.14923 4.02032ZM6.14923 5.37775C5.16175 5.37775 4.46628 5.37761 3.9256 5.42657C3.39428 5.47473 3.07853 5.56574 2.83575 5.70587C2.46313 5.92106 2.15348 6.23071 1.93829 6.60333C1.79817 6.84611 1.70715 7.16185 1.659 7.69318C1.61004 8.23385 1.61017 8.92934 1.61017 9.91681C1.61017 10.9043 1.61002 11.5998 1.659 12.1404C1.70715 12.6717 1.79817 12.9875 1.93829 13.2303C2.15349 13.6029 2.46315 13.9126 2.83575 14.1277C3.07853 14.2679 3.39428 14.3589 3.9256 14.407C4.46628 14.456 5.16176 14.4559 6.14923 14.4559C7.13675 14.4559 7.83218 14.456 8.37286 14.407C8.90419 14.3589 9.21993 14.2679 9.46271 14.1277C9.83529 13.9126 10.145 13.6029 10.3602 13.2303C10.5003 12.9875 10.5913 12.6718 10.6395 12.1404C10.6884 11.5998 10.6883 10.9043 10.6883 9.91681C10.6883 8.92935 10.6884 8.23385 10.6395 7.69318C10.5913 7.16185 10.5003 6.84611 10.3602 6.60333C10.145 6.23072 9.8353 5.92107 9.46271 5.70587C9.21993 5.56574 8.90418 5.47473 8.37286 5.42657C7.83218 5.3776 7.13676 5.37775 6.14923 5.37775ZM9.80157 0.367981C10.7637 0.367981 11.5313 0.367886 12.1473 0.423645C12.7725 0.480313 13.3093 0.598765 13.7928 0.877747C14.3716 1.21192 14.852 1.69355 15.1863 2.27228C15.4655 2.75575 15.5857 3.29165 15.6424 3.91681C15.6982 4.53301 15.6971 5.30161 15.6971 6.26447V7.8299C15.6971 8.29265 15.6989 8.58994 15.6649 8.84845C15.4667 10.3525 14.4009 11.5738 12.9832 11.9988V10.5467C13.6973 10.1903 14.2104 9.49662 14.3192 8.67169C14.3387 8.52348 14.3406 8.3358 14.3406 7.8299V6.26447C14.3406 5.27707 14.3398 4.58149 14.2908 4.04083C14.2427 3.50969 14.1526 3.19373 14.0125 2.95099C13.7974 2.5785 13.4875 2.2687 13.1151 2.05353C12.8723 1.91347 12.5563 1.82237 12.0252 1.77423C11.4846 1.72528 10.7888 1.7254 9.80157 1.7254H7.71466C6.75614 1.72559 5.92659 2.27697 5.52325 3.07892H4.07013C4.54215 1.51132 5.99314 0.368192 7.71466 0.367981H9.80157Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">复制</span></span><div class="ds-focus-ring"></div></button><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M15.3695 11.411L15.1234 12.8866C14.8869 14.3042 13.6603 15.3436 12.223 15.3436H3.7767C2.33954 15.3434 1.11276 14.3042 0.876312 12.8866L0.630219 11.411L2.05405 11.1747L2.29916 12.6493C2.41969 13.3713 3.04472 13.9001 3.7767 13.9003H12.223C12.9551 13.9002 13.58 13.3713 13.7005 12.6493L13.9456 11.1747L15.3695 11.411ZM8.72202 8.994C8.77714 8.93934 8.83789 8.88106 8.90268 8.81627L12.4828 5.23424L13.5042 6.25572L9.92221 9.8358C9.63947 10.1185 9.3876 10.3732 9.15854 10.5575C8.91889 10.7503 8.6395 10.9224 8.28647 10.9784C8.09708 11.0083 7.9036 11.0083 7.7142 10.9784C7.36103 10.9224 7.08087 10.7503 6.84116 10.5575C6.61212 10.3732 6.36019 10.1185 6.07748 9.8358L2.49643 6.25572L3.51694 5.23424L7.09702 8.81627C7.16216 8.88142 7.22327 8.94006 7.27866 8.99498V1.3065H8.72202V8.994Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">下载</span></span><div class="ds-focus-ring"></div></button></div></div></div></div></div><pre><span class="token punctuation">{</span>
  <span class="token property">"success"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
  <span class="token property">"enzyme"</span><span class="token operator">:</span> <span class="token string">"BsaI"</span><span class="token punctuation">,</span>
  <span class="token property">"framework"</span><span class="token operator">:</span> <span class="token string">"pET28a"</span><span class="token punctuation">,</span>
  <span class="token property">"message"</span><span class="token operator">:</span> <span class="token string">"Assembly simulation completed successfully"</span><span class="token punctuation">,</span>
  <span class="token property">"assembly_info"</span><span class="token operator">:</span> <span class="token punctuation">{</span>
    <span class="token property">"enzyme"</span><span class="token operator">:</span> <span class="token string">"BsaI"</span><span class="token punctuation">,</span>
    <span class="token property">"framework"</span><span class="token operator">:</span> <span class="token string">"pET28a"</span><span class="token punctuation">,</span>
    <span class="token property">"fragments_count"</span><span class="token operator">:</span> <span class="token number">1</span><span class="token punctuation">,</span>
    <span class="token property">"expected_constructs"</span><span class="token operator">:</span> <span class="token number">1</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token property">"detailed_report"</span><span class="token operator">:</span> <span class="token punctuation">{</span>  <span class="token comment">// 仅当include_reports=true</span>
    <span class="token property">"assembly_method"</span><span class="token operator">:</span> <span class="token string">"Golden Gate"</span><span class="token punctuation">,</span>
    <span class="token property">"fragments_used"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
      <span class="token punctuation">{</span>
        <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"CDS_insert"</span><span class="token punctuation">,</span>
        <span class="token property">"length"</span><span class="token operator">:</span> <span class="token number">18</span><span class="token punctuation">,</span>
        <span class="token property">"sequence"</span><span class="token operator">:</span> <span class="token string">"GGTCTCNAATGATGAAA..."</span>
      <span class="token punctuation">}</span>
    <span class="token punctuation">]</span><span class="token punctuation">,</span>
    <span class="token property">"constructs_generated"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
      <span class="token punctuation">{</span>
        <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"pET28a_construct"</span><span class="token punctuation">,</span>
        <span class="token property">"length"</span><span class="token operator">:</span> <span class="token number">5418</span><span class="token punctuation">,</span>
        <span class="token property">"circular"</span><span class="token operator">:</span> <span class="token boolean">true</span>
      <span class="token punctuation">}</span>
    <span class="token punctuation">]</span><span class="token punctuation">,</span>
    <span class="token property">"warnings"</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token punctuation">]</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span></pre><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _33882ae"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _28d7e84"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg></div><h3><span>AI自动补全合理性分析</span></h3><div class="ds-scroll-area _1210dd7 c03cafe9"><div class="ds-scroll-area__gutters" style="position: sticky; top: 0px; left: 0px; right: 0px; height: 0px; --container-height: 333px;"><div class="ds-scroll-area__horizontal-gutter" style="left: 0px; right: 0px; top: calc(var(--container-height) - 14px); height: 10px;"><div class="ds-scroll-area__horizontal-bar" style="display: none;"></div></div><div class="ds-scroll-area__vertical-gutter" style="right: 0px; top: 8px; bottom: calc(0px - var(--container-height) + 8px); width: 10px;"><div class="ds-scroll-area__vertical-bar" style="display: none;"></div></div></div><table><thead><tr><th><span>参数</span></th><th><span>评分</span></th><th><span>合理性</span></th><th><span>风险点</span></th><th><span>改进建议</span></th></tr></thead><tbody><tr><td>`fragments`</td><td><span>⭐⭐⭐⭐⭐ (5/5)</span></td><td><strong><span>非常合理</span></strong></td><td><span>• 极低: 支持4种格式，容错性强</span><br><span>• 自动识别和转换</span></td><td><strong><span>优秀设计</span></strong><span>: 多格式支持极大简化了用户操作</span></td></tr><tr><td>`framework`</td><td><span>⭐⭐⭐☆☆ (3/5)</span></td><td><strong><span>部分合理</span></strong></td><td><span>• </span><strong><span>高</span></strong><span>: 默认pET28a仅适用于原核</span><br><span>• 真核表达会失败</span></td><td><strong><span>必须改进</span></strong><span>: 实现</span>`SmartDefaults.get_framework(organism, tag)`<span>:</span><br><span>• E.coli → pET28a/pET15b</span><br><span>• Yeast → pYES2/pGADT7</span><br><span>• Human → pcDNA3.1/pLVX</span></td></tr><tr><td>`enzyme`</td><td><span>⭐⭐⭐⭐⭐ (5/5)</span></td><td><strong><span>非常合理</span></strong></td><td><span>• 低: 但缺少验证机制</span></td><td><strong><span>必须添加</span></strong><span>: WorkflowValidator验证整个工作流的enzyme一致性</span></td></tr></tbody></table></div><hr><h2><span>工具4: plasmid_visualizer</span></h2><h3><span>基本信息</span></h3><ul><li><p class="ds-markdown-paragraph"><strong><span>名称</span></strong><span>: </span>`plasmid_visualizer`</p></li><li><p class="ds-markdown-paragraph"><strong><span>功能</span></strong><span>: 生成质粒可视化图谱（环状或线性）</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>底层库</span></strong><span>: DnaFeaturesViewer</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>代码位置</span></strong><span>: </span>`synth_tools/dna_visualizer_wrapper.py`</p></li></ul><h3><span>输入参数</span></h3><h4><span>用户输入 (Required)</span></h4><div class="ds-scroll-area _1210dd7 c03cafe9"><div class="ds-scroll-area__gutters" style="position: sticky; top: 0px; left: 0px; right: 0px; height: 0px; --container-height: 91px;"><div class="ds-scroll-area__horizontal-gutter" style="left: 0px; right: 0px; top: calc(var(--container-height) - 14px); height: 10px;"><div class="ds-scroll-area__horizontal-bar" style="display: none;"></div></div><div class="ds-scroll-area__vertical-gutter" style="right: 0px; top: 8px; bottom: calc(0px - var(--container-height) + 8px); width: 10px;"><div class="ds-scroll-area__vertical-bar" style="display: none;"></div></div></div><table><thead><tr><th><span>参数名</span></th><th><span>类型</span></th><th><span>描述</span></th><th><span>验证规则</span></th><th><span>示例</span></th></tr></thead><tbody><tr><td>`sequence`</td><td><span>string</span></td><td><span>完整质粒DNA序列</span></td><td><span>必须是有效的ATCG序列</span></td><td>`"ATGAAACGC..."`<span> (完整质粒)</span></td></tr></tbody></table></div><h4><span>默认值 (Optional)</span></h4><div class="ds-scroll-area _1210dd7 c03cafe9"><div class="ds-scroll-area__gutters" style="position: sticky; top: 0px; left: 0px; right: 0px; height: 0px; --container-height: 253px;"><div class="ds-scroll-area__horizontal-gutter" style="left: 0px; right: 0px; top: calc(var(--container-height) - 14px); height: 10px;"><div class="ds-scroll-area__horizontal-bar" style="left: 0px; width: 1018.25px;"></div></div><div class="ds-scroll-area__vertical-gutter" style="right: 0px; top: 8px; bottom: calc(0px - var(--container-height) + 8px); width: 10px;"><div class="ds-scroll-area__vertical-bar" style="display: none;"></div></div></div><table><thead><tr><th><span>参数名</span></th><th><span>类型</span></th><th><span>默认值</span></th><th><span>配置来源</span></th><th><span>描述</span></th></tr></thead><tbody><tr><td>`features`</td><td><span>array</span></td><td>`[]`</td><td><span>-</span></td><td><span>特征注释列表（CDS, promoter, terminator等）</span></td></tr><tr><td>`plasmid_name`</td><td><span>string</span></td><td>`"Plasmid"`</td><td><span>-</span></td><td><span>质粒名称</span></td></tr><tr><td>`circular`</td><td><span>boolean</span></td><td>`true`</td><td>`DNAFEATUREVIEWER_CONFIG['circular_plot']`</td><td><span>是否为环状质粒</span></td></tr><tr><td>`output_format`</td><td><span>string</span></td><td>`"png"`</td><td>`DNAFEATUREVIEWER_CONFIG['default_format']`</td><td><span>输出格式（png/svg/pdf）</span></td></tr></tbody></table></div><h4><span>AI自动补全</span></h4><div class="ds-scroll-area _1210dd7 c03cafe9"><div class="ds-scroll-area__gutters" style="position: sticky; top: 0px; left: 0px; right: 0px; height: 0px; --container-height: 428px;"><div class="ds-scroll-area__horizontal-gutter" style="left: 0px; right: 0px; top: calc(var(--container-height) - 14px); height: 10px;"><div class="ds-scroll-area__horizontal-bar" style="display: none;"></div></div><div class="ds-scroll-area__vertical-gutter" style="right: 0px; top: 8px; bottom: calc(0px - var(--container-height) + 8px); width: 10px;"><div class="ds-scroll-area__vertical-bar" style="display: none;"></div></div></div><table><thead><tr><th><span>参数名</span></th><th><span>补全策略</span></th><th><span>数据来源</span></th><th><span>AI推理逻辑</span></th><th><span>示例</span></th></tr></thead><tbody><tr><td>`sequence`</td><td><span>从assembly_simulator传递</span></td><td><span>组装后的完整序列</span></td><td><span>直接使用final_sequence</span></td><td><span>自动传递组装结果</span></td></tr><tr><td>`features`</td><td><span>自动识别注释</span></td><td><span>序列分析 + 框架定义</span></td><td><strong><span>智能特征识别</span></strong><span>:</span><br><span>• T7 promoter: </span>`TAATACGACTCACTATA`<br><span>• His6-tag: </span>`CATCATCATCATCATCAT`<br><span>• Kan^R: 标准卡那霉素抗性基因</span><br><span>• ColE1 ori: 标准复制起点</span></td><td><span>framework="pET28a"</span><br><span>→ 自动添加T7, His6, Kan, ori</span></td></tr><tr><td>`plasmid_name`</td><td><span>智能命名</span></td><td><span>工作流上下文</span></td><td><span>命名规则:</span><br>`framework-gene-tag-modification`<br><span>例: </span>`"pET28a-GFP-His6-optimized"`</td><td><span>自动生成描述性名称</span></td></tr><tr><td>`circular`</td><td><span>根据类型推断</span></td><td><span>分子类型</span></td><td><span>• 质粒框架 → </span>`true`<br><span>• PCR产物 → </span>`false`<br><span>• 线性化载体 → </span>`false`</td><td><span>framework存在 → </span>`circular=true`</td></tr></tbody></table></div><h3><span>输出参数</span></h3><div class="md-code-block md-code-block-light"><div class="md-code-block-banner-wrap"><div class="md-code-block-banner md-code-block-banner-lite"><div class="_121d384"><div class="d2a24f03"><span class="d813de27">json</span></div><div class="d2a24f03 _246a029"><div class="efa13877"><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon" style="margin-right: 4px;"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.14923 4.02032C7.11191 4.02032 7.87977 4.02017 8.49591 4.07599C9.12122 4.1327 9.65786 4.25188 10.1414 4.53107C10.7201 4.8653 11.2008 5.34591 11.535 5.92462C11.8142 6.40818 11.9333 6.94482 11.9901 7.57013C12.0459 8.18625 12.0457 8.9542 12.0457 9.91681C12.0457 10.8795 12.0459 11.6474 11.9901 12.2635C11.9333 12.8888 11.8142 13.4254 11.535 13.909C11.2008 14.4877 10.7201 14.9683 10.1414 15.3026C9.65786 15.5817 9.12122 15.7009 8.49591 15.7576C7.87977 15.8134 7.1119 15.8133 6.14923 15.8133C5.18661 15.8133 4.41868 15.8134 3.80255 15.7576C3.17724 15.7009 2.6406 15.5817 2.15704 15.3026C1.57834 14.9684 1.09772 14.4877 0.763489 13.909C0.484305 13.4254 0.365123 12.8888 0.308411 12.2635C0.252587 11.6474 0.252747 10.8795 0.252747 9.91681C0.252747 8.95419 0.252603 8.18625 0.308411 7.57013C0.365123 6.94482 0.484305 6.40818 0.763489 5.92462C1.09771 5.3459 1.57833 4.86529 2.15704 4.53107C2.6406 4.25188 3.17724 4.1327 3.80255 4.07599C4.41868 4.02018 5.1866 4.02032 6.14923 4.02032ZM6.14923 5.37775C5.16175 5.37775 4.46628 5.37761 3.9256 5.42657C3.39428 5.47473 3.07853 5.56574 2.83575 5.70587C2.46313 5.92106 2.15348 6.23071 1.93829 6.60333C1.79817 6.84611 1.70715 7.16185 1.659 7.69318C1.61004 8.23385 1.61017 8.92934 1.61017 9.91681C1.61017 10.9043 1.61002 11.5998 1.659 12.1404C1.70715 12.6717 1.79817 12.9875 1.93829 13.2303C2.15349 13.6029 2.46315 13.9126 2.83575 14.1277C3.07853 14.2679 3.39428 14.3589 3.9256 14.407C4.46628 14.456 5.16176 14.4559 6.14923 14.4559C7.13675 14.4559 7.83218 14.456 8.37286 14.407C8.90419 14.3589 9.21993 14.2679 9.46271 14.1277C9.83529 13.9126 10.145 13.6029 10.3602 13.2303C10.5003 12.9875 10.5913 12.6718 10.6395 12.1404C10.6884 11.5998 10.6883 10.9043 10.6883 9.91681C10.6883 8.92935 10.6884 8.23385 10.6395 7.69318C10.5913 7.16185 10.5003 6.84611 10.3602 6.60333C10.145 6.23072 9.8353 5.92107 9.46271 5.70587C9.21993 5.56574 8.90418 5.47473 8.37286 5.42657C7.83218 5.3776 7.13676 5.37775 6.14923 5.37775ZM9.80157 0.367981C10.7637 0.367981 11.5313 0.367886 12.1473 0.423645C12.7725 0.480313 13.3093 0.598765 13.7928 0.877747C14.3716 1.21192 14.852 1.69355 15.1863 2.27228C15.4655 2.75575 15.5857 3.29165 15.6424 3.91681C15.6982 4.53301 15.6971 5.30161 15.6971 6.26447V7.8299C15.6971 8.29265 15.6989 8.58994 15.6649 8.84845C15.4667 10.3525 14.4009 11.5738 12.9832 11.9988V10.5467C13.6973 10.1903 14.2104 9.49662 14.3192 8.67169C14.3387 8.52348 14.3406 8.3358 14.3406 7.8299V6.26447C14.3406 5.27707 14.3398 4.58149 14.2908 4.04083C14.2427 3.50969 14.1526 3.19373 14.0125 2.95099C13.7974 2.5785 13.4875 2.2687 13.1151 2.05353C12.8723 1.91347 12.5563 1.82237 12.0252 1.77423C11.4846 1.72528 10.7888 1.7254 9.80157 1.7254H7.71466C6.75614 1.72559 5.92659 2.27697 5.52325 3.07892H4.07013C4.54215 1.51132 5.99314 0.368192 7.71466 0.367981H9.80157Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">复制</span></span><div class="ds-focus-ring"></div></button><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M15.3695 11.411L15.1234 12.8866C14.8869 14.3042 13.6603 15.3436 12.223 15.3436H3.7767C2.33954 15.3434 1.11276 14.3042 0.876312 12.8866L0.630219 11.411L2.05405 11.1747L2.29916 12.6493C2.41969 13.3713 3.04472 13.9001 3.7767 13.9003H12.223C12.9551 13.9002 13.58 13.3713 13.7005 12.6493L13.9456 11.1747L15.3695 11.411ZM8.72202 8.994C8.77714 8.93934 8.83789 8.88106 8.90268 8.81627L12.4828 5.23424L13.5042 6.25572L9.92221 9.8358C9.63947 10.1185 9.3876 10.3732 9.15854 10.5575C8.91889 10.7503 8.6395 10.9224 8.28647 10.9784C8.09708 11.0083 7.9036 11.0083 7.7142 10.9784C7.36103 10.9224 7.08087 10.7503 6.84116 10.5575C6.61212 10.3732 6.36019 10.1185 6.07748 9.8358L2.49643 6.25572L3.51694 5.23424L7.09702 8.81627C7.16216 8.88142 7.22327 8.94006 7.27866 8.99498V1.3065H8.72202V8.994Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">下载</span></span><div class="ds-focus-ring"></div></button></div></div></div></div></div><pre><span class="token punctuation">{</span>
  <span class="token property">"success"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
  <span class="token property">"plasmid_name"</span><span class="token operator">:</span> <span class="token string">"pET28a-GFP-His6"</span><span class="token punctuation">,</span>
  <span class="token property">"sequence_length"</span><span class="token operator">:</span> <span class="token number">5418</span><span class="token punctuation">,</span>
  <span class="token property">"circular"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
  <span class="token property">"output_format"</span><span class="token operator">:</span> <span class="token string">"png"</span><span class="token punctuation">,</span>
  <span class="token property">"image_path"</span><span class="token operator">:</span> <span class="token string">"/home/redacted_service_user/tmpxxxx.png"</span><span class="token punctuation">,</span>
  <span class="token property">"image_base64"</span><span class="token operator">:</span> <span class="token string">"iVBORw0KGgoAAAANS..."</span>  <span class="token comment">// 仅PNG格式</span>
<span class="token punctuation">}</span></pre><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _33882ae"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _28d7e84"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg></div><h3><span>AI自动补全合理性分析</span></h3><div class="ds-scroll-area _1210dd7 c03cafe9"><div class="ds-scroll-area__gutters" style="position: sticky; top: 0px; left: 0px; right: 0px; height: 0px; --container-height: 449px;"><div class="ds-scroll-area__horizontal-gutter" style="left: 0px; right: 0px; top: calc(var(--container-height) - 14px); height: 10px;"><div class="ds-scroll-area__horizontal-bar" style="display: none;"></div></div><div class="ds-scroll-area__vertical-gutter" style="right: 0px; top: 8px; bottom: calc(0px - var(--container-height) + 8px); width: 10px;"><div class="ds-scroll-area__vertical-bar" style="display: none;"></div></div></div><table><thead><tr><th><span>参数</span></th><th><span>评分</span></th><th><span>合理性</span></th><th><span>风险点</span></th><th><span>改进建议</span></th></tr></thead><tbody><tr><td>`sequence`</td><td><span>⭐⭐⭐⭐⭐ (5/5)</span></td><td><strong><span>非常合理</span></strong></td><td><span>• 极低: 直接传递，无歧义</span></td><td><span>无需改进</span></td></tr><tr><td>`features`</td><td><span>⭐⭐⭐⭐☆ (4/5)</span></td><td><strong><span>基本合理</span></strong></td><td><span>• 中: 标准特征识别准确</span><br><span>• 复杂特征需要用户提供</span></td><td><span>扩展识别库，支持更多标准元件:</span><br><span>• RBS (核糖体结合位点)</span><br><span>• Multiple cloning site</span><br><span>• Epitope tags</span></td></tr><tr><td>`plasmid_name`</td><td><span>⭐⭐⭐⭐⭐ (5/5)</span></td><td><strong><span>非常合理</span></strong></td><td><span>• 极低: 遵循标准命名规范</span></td><td><span>可以让用户自定义命名模板</span></td></tr><tr><td>`circular`</td><td><span>⭐⭐⭐⭐⭐ (5/5)</span></td><td><strong><span>非常合理</span></strong></td><td><span>• 极低: 质粒默认环状是标准</span></td><td><span>无需改进</span></td></tr><tr><td>`output_format`</td><td><span>⭐⭐⭐⭐☆ (4/5)</span></td><td><strong><span>基本合理</span></strong></td><td><span>• 低: PNG适合预览，但发表需要SVG</span></td><td><strong><span>改进</span></strong><span>: 根据用途智能选择:</span><br><span>• 预览 → PNG (150 DPI)</span><br><span>• 分析 → PNG (300 DPI)</span><br><span>• 发表 → SVG (矢量)</span><br><span>• 打印 → PDF</span></td></tr></tbody></table></div><hr><h2><span>工具5: primer_designer</span></h2><h3><span>基本信息</span></h3><ul><li><p class="ds-markdown-paragraph"><strong><span>名称</span></strong><span>: </span>`primer_designer`</p></li><li><p class="ds-markdown-paragraph"><strong><span>功能</span></strong><span>: 使用Primerize算法设计RNA合成引物</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>底层库</span></strong><span>: Primerize</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>代码位置</span></strong><span>: </span>`synth_tools/primerize_wrapper.py`</p></li></ul><h3><span>输入参数</span></h3><h4><span>用户输入 (Required)</span></h4><div class="ds-scroll-area _1210dd7 c03cafe9"><div class="ds-scroll-area__gutters" style="position: sticky; top: 0px; left: 0px; right: 0px; height: 0px; --container-height: 91px;"><div class="ds-scroll-area__horizontal-gutter" style="left: 0px; right: 0px; top: calc(var(--container-height) - 14px); height: 10px;"><div class="ds-scroll-area__horizontal-bar" style="display: none;"></div></div><div class="ds-scroll-area__vertical-gutter" style="right: 0px; top: 8px; bottom: calc(0px - var(--container-height) + 8px); width: 10px;"><div class="ds-scroll-area__vertical-bar" style="display: none;"></div></div></div><table><thead><tr><th><span>参数名</span></th><th><span>类型</span></th><th><span>描述</span></th><th><span>验证规则</span></th><th><span>示例</span></th></tr></thead><tbody><tr><td>`sequence`</td><td><span>string</span></td><td><span>RNA序列(ATCGU格式)</span></td><td><span>必须包含ATCGU字符</span></td><td>`"AUGAAACGCAUUAGCACC"`</td></tr></tbody></table></div><h4><span>默认值 (Optional)</span></h4><div class="ds-scroll-area _1210dd7 c03cafe9"><div class="ds-scroll-area__gutters" style="position: sticky; top: 0px; left: 0px; right: 0px; height: 0px; --container-height: 228px;"><div class="ds-scroll-area__horizontal-gutter" style="left: 0px; right: 0px; top: calc(var(--container-height) - 14px); height: 10px;"><div class="ds-scroll-area__horizontal-bar" style="display: none;"></div></div><div class="ds-scroll-area__vertical-gutter" style="right: 0px; top: 8px; bottom: calc(0px - var(--container-height) + 8px); width: 10px;"><div class="ds-scroll-area__vertical-bar" style="display: none;"></div></div></div><table><thead><tr><th><span>参数名</span></th><th><span>类型</span></th><th><span>默认值</span></th><th><span>配置来源</span></th><th><span>描述</span></th></tr></thead><tbody><tr><td>`min_tm`</td><td><span>number</span></td><td>`60.0`</td><td>`PRIMERIZE_CONFIG['min_tm']`</td><td><span>最小熔解温度(°C)</span></td></tr><tr><td>`min_length`</td><td><span>integer</span></td><td>`15`</td><td>`PRIMERIZE_CONFIG['min_length']`</td><td><span>最小引物长度(bp)</span></td></tr><tr><td>`max_length`</td><td><span>integer</span></td><td>`60`</td><td>`PRIMERIZE_CONFIG['max_length']`</td><td><span>最大引物长度(bp)</span></td></tr><tr><td>`prefix`</td><td><span>string</span></td><td>`"Primer"`</td><td>`PRIMERIZE_CONFIG['prefix']`</td><td><span>引物名称前缀</span></td></tr></tbody></table></div><h4><span>AI自动补全</span></h4><div class="ds-scroll-area _1210dd7 c03cafe9"><div class="ds-scroll-area__gutters" style="position: sticky; top: 0px; left: 0px; right: 0px; height: 0px; --container-height: 453px;"><div class="ds-scroll-area__horizontal-gutter" style="left: 0px; right: 0px; top: calc(var(--container-height) - 14px); height: 10px;"><div class="ds-scroll-area__horizontal-bar" style="display: none;"></div></div><div class="ds-scroll-area__vertical-gutter" style="right: 0px; top: 8px; bottom: calc(0px - var(--container-height) + 8px); width: 10px;"><div class="ds-scroll-area__vertical-bar" style="display: none;"></div></div></div><table><thead><tr><th><span>参数名</span></th><th><span>补全策略</span></th><th><span>数据来源</span></th><th><span>AI推理逻辑</span></th><th><span>示例</span></th></tr></thead><tbody><tr><td>`sequence`</td><td><span>DNA转录为RNA</span></td><td>`cds_optimizer`<span>的序列</span></td><td><span>T → U转换:</span><br>`ATGAAA`<span> → </span>`AUGAAA`</td><td><span>DNA输入自动转录</span></td></tr><tr><td>`min_tm`</td><td><span>根据应用调整</span></td><td><span>用户描述的应用场景</span></td><td><strong><span>应用场景优化</span></strong><span>:</span><br><span>• 体外转录: 55-58°C</span><br><span>• RT-PCR: 58-62°C</span><br><span>• RNA结构探测: 50-55°C</span><br><span>• 默认: 60°C</span></td><td><span>用户: "体外转录"</span><br><span>→ </span>`min_tm=55`</td></tr><tr><td>`length_range`</td><td><span>根据序列长度优化</span></td><td><span>RNA序列长度</span></td><td><strong><span>动态调整</span></strong><span>:</span><br><span>• &lt;100bp: [15, 40]</span><br><span>• 100-300bp: [20, 50]</span><br><span>• &gt;300bp: [25, 60]</span></td><td><span>150bp RNA</span><br><span>→ </span>`min_length=20, max_length=50`</td></tr><tr><td>`prefix`</td><td><span>根据项目命名</span></td><td><span>项目名称/基因名</span></td><td>`"项目名-Primer"`<br><span>例: </span>`"GFP-Primer"`</td><td><span>项目="GFP"</span><br><span>→ </span>`prefix="GFP-Primer"`</td></tr></tbody></table></div><h3><span>输出参数</span></h3><div class="md-code-block md-code-block-light"><div class="md-code-block-banner-wrap"><div class="md-code-block-banner md-code-block-banner-lite"><div class="_121d384"><div class="d2a24f03"><span class="d813de27">json</span></div><div class="d2a24f03 _246a029"><div class="efa13877"><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon" style="margin-right: 4px;"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.14923 4.02032C7.11191 4.02032 7.87977 4.02017 8.49591 4.07599C9.12122 4.1327 9.65786 4.25188 10.1414 4.53107C10.7201 4.8653 11.2008 5.34591 11.535 5.92462C11.8142 6.40818 11.9333 6.94482 11.9901 7.57013C12.0459 8.18625 12.0457 8.9542 12.0457 9.91681C12.0457 10.8795 12.0459 11.6474 11.9901 12.2635C11.9333 12.8888 11.8142 13.4254 11.535 13.909C11.2008 14.4877 10.7201 14.9683 10.1414 15.3026C9.65786 15.5817 9.12122 15.7009 8.49591 15.7576C7.87977 15.8134 7.1119 15.8133 6.14923 15.8133C5.18661 15.8133 4.41868 15.8134 3.80255 15.7576C3.17724 15.7009 2.6406 15.5817 2.15704 15.3026C1.57834 14.9684 1.09772 14.4877 0.763489 13.909C0.484305 13.4254 0.365123 12.8888 0.308411 12.2635C0.252587 11.6474 0.252747 10.8795 0.252747 9.91681C0.252747 8.95419 0.252603 8.18625 0.308411 7.57013C0.365123 6.94482 0.484305 6.40818 0.763489 5.92462C1.09771 5.3459 1.57833 4.86529 2.15704 4.53107C2.6406 4.25188 3.17724 4.1327 3.80255 4.07599C4.41868 4.02018 5.1866 4.02032 6.14923 4.02032ZM6.14923 5.37775C5.16175 5.37775 4.46628 5.37761 3.9256 5.42657C3.39428 5.47473 3.07853 5.56574 2.83575 5.70587C2.46313 5.92106 2.15348 6.23071 1.93829 6.60333C1.79817 6.84611 1.70715 7.16185 1.659 7.69318C1.61004 8.23385 1.61017 8.92934 1.61017 9.91681C1.61017 10.9043 1.61002 11.5998 1.659 12.1404C1.70715 12.6717 1.79817 12.9875 1.93829 13.2303C2.15349 13.6029 2.46315 13.9126 2.83575 14.1277C3.07853 14.2679 3.39428 14.3589 3.9256 14.407C4.46628 14.456 5.16176 14.4559 6.14923 14.4559C7.13675 14.4559 7.83218 14.456 8.37286 14.407C8.90419 14.3589 9.21993 14.2679 9.46271 14.1277C9.83529 13.9126 10.145 13.6029 10.3602 13.2303C10.5003 12.9875 10.5913 12.6718 10.6395 12.1404C10.6884 11.5998 10.6883 10.9043 10.6883 9.91681C10.6883 8.92935 10.6884 8.23385 10.6395 7.69318C10.5913 7.16185 10.5003 6.84611 10.3602 6.60333C10.145 6.23072 9.8353 5.92107 9.46271 5.70587C9.21993 5.56574 8.90418 5.47473 8.37286 5.42657C7.83218 5.3776 7.13676 5.37775 6.14923 5.37775ZM9.80157 0.367981C10.7637 0.367981 11.5313 0.367886 12.1473 0.423645C12.7725 0.480313 13.3093 0.598765 13.7928 0.877747C14.3716 1.21192 14.852 1.69355 15.1863 2.27228C15.4655 2.75575 15.5857 3.29165 15.6424 3.91681C15.6982 4.53301 15.6971 5.30161 15.6971 6.26447V7.8299C15.6971 8.29265 15.6989 8.58994 15.6649 8.84845C15.4667 10.3525 14.4009 11.5738 12.9832 11.9988V10.5467C13.6973 10.1903 14.2104 9.49662 14.3192 8.67169C14.3387 8.52348 14.3406 8.3358 14.3406 7.8299V6.26447C14.3406 5.27707 14.3398 4.58149 14.2908 4.04083C14.2427 3.50969 14.1526 3.19373 14.0125 2.95099C13.7974 2.5785 13.4875 2.2687 13.1151 2.05353C12.8723 1.91347 12.5563 1.82237 12.0252 1.77423C11.4846 1.72528 10.7888 1.7254 9.80157 1.7254H7.71466C6.75614 1.72559 5.92659 2.27697 5.52325 3.07892H4.07013C4.54215 1.51132 5.99314 0.368192 7.71466 0.367981H9.80157Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">复制</span></span><div class="ds-focus-ring"></div></button><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M15.3695 11.411L15.1234 12.8866C14.8869 14.3042 13.6603 15.3436 12.223 15.3436H3.7767C2.33954 15.3434 1.11276 14.3042 0.876312 12.8866L0.630219 11.411L2.05405 11.1747L2.29916 12.6493C2.41969 13.3713 3.04472 13.9001 3.7767 13.9003H12.223C12.9551 13.9002 13.58 13.3713 13.7005 12.6493L13.9456 11.1747L15.3695 11.411ZM8.72202 8.994C8.77714 8.93934 8.83789 8.88106 8.90268 8.81627L12.4828 5.23424L13.5042 6.25572L9.92221 9.8358C9.63947 10.1185 9.3876 10.3732 9.15854 10.5575C8.91889 10.7503 8.6395 10.9224 8.28647 10.9784C8.09708 11.0083 7.9036 11.0083 7.7142 10.9784C7.36103 10.9224 7.08087 10.7503 6.84116 10.5575C6.61212 10.3732 6.36019 10.1185 6.07748 9.8358L2.49643 6.25572L3.51694 5.23424L7.09702 8.81627C7.16216 8.88142 7.22327 8.94006 7.27866 8.99498V1.3065H8.72202V8.994Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">下载</span></span><div class="ds-focus-ring"></div></button></div></div></div></div></div><pre><span class="token punctuation">{</span>
  <span class="token property">"success"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
  <span class="token property">"sequence"</span><span class="token operator">:</span> <span class="token string">"AUGAAACGCAUUAGCACC"</span><span class="token punctuation">,</span>
  <span class="token property">"parameters"</span><span class="token operator">:</span> <span class="token punctuation">{</span>
    <span class="token property">"min_tm"</span><span class="token operator">:</span> <span class="token number">60.0</span><span class="token punctuation">,</span>
    <span class="token property">"min_length"</span><span class="token operator">:</span> <span class="token number">15</span><span class="token punctuation">,</span>
    <span class="token property">"max_length"</span><span class="token operator">:</span> <span class="token number">60</span><span class="token punctuation">,</span>
    <span class="token property">"prefix"</span><span class="token operator">:</span> <span class="token string">"Primer"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token property">"primers"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
    <span class="token punctuation">{</span>
      <span class="token property">"index"</span><span class="token operator">:</span> <span class="token number">1</span><span class="token punctuation">,</span>
      <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Primer_1"</span><span class="token punctuation">,</span>
      <span class="token property">"sequence"</span><span class="token operator">:</span> <span class="token string">"AUGAAACGCAUUAGC"</span><span class="token punctuation">,</span>  <span class="token comment">// 如果Primerize提供</span>
      <span class="token property">"tm"</span><span class="token operator">:</span> <span class="token number">62.5</span><span class="token punctuation">,</span>
      <span class="token property">"length"</span><span class="token operator">:</span> <span class="token number">15</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token punctuation">{</span>
      <span class="token property">"index"</span><span class="token operator">:</span> <span class="token number">2</span><span class="token punctuation">,</span>
      <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Primer_2"</span><span class="token punctuation">,</span>
      <span class="token property">"sequence"</span><span class="token operator">:</span> <span class="token string">"CAUUAGCACC"</span><span class="token punctuation">,</span>
      <span class="token property">"tm"</span><span class="token operator">:</span> <span class="token number">58.3</span><span class="token punctuation">,</span>
      <span class="token property">"length"</span><span class="token operator">:</span> <span class="token number">10</span>
    <span class="token punctuation">}</span>
  <span class="token punctuation">]</span><span class="token punctuation">,</span>
  <span class="token property">"statistics"</span><span class="token operator">:</span> <span class="token punctuation">{</span>
    <span class="token property">"num_primers"</span><span class="token operator">:</span> <span class="token number">2</span><span class="token punctuation">,</span>
    <span class="token property">"misprime_score"</span><span class="token operator">:</span> <span class="token number">0.15</span>  <span class="token comment">// 如果可用</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token property">"design_summary"</span><span class="token operator">:</span> <span class="token string">"Primerize 1D design completed"</span>
<span class="token punctuation">}</span></pre><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _33882ae"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _28d7e84"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg></div><h3><span>AI自动补全合理性分析</span></h3><div class="ds-scroll-area _1210dd7 c03cafe9"><div class="ds-scroll-area__gutters" style="position: sticky; top: 0px; left: 0px; right: 0px; height: 0px; --container-height: 328px;"><div class="ds-scroll-area__horizontal-gutter" style="left: 0px; right: 0px; top: calc(var(--container-height) - 14px); height: 10px;"><div class="ds-scroll-area__horizontal-bar" style="display: none;"></div></div><div class="ds-scroll-area__vertical-gutter" style="right: 0px; top: 8px; bottom: calc(0px - var(--container-height) + 8px); width: 10px;"><div class="ds-scroll-area__vertical-bar" style="display: none;"></div></div></div><table><thead><tr><th><span>参数</span></th><th><span>评分</span></th><th><span>合理性</span></th><th><span>风险点</span></th><th><span>改进建议</span></th></tr></thead><tbody><tr><td>`sequence`</td><td><span>⭐⭐⭐⭐☆ (4/5)</span></td><td><strong><span>基本合理</span></strong></td><td><span>• 低: DNA→RNA转换标准</span><br><span>• 但应该告知用户</span></td><td><span>转换时明确提示:</span><br><span>"已将DNA序列转录为RNA (T→U)"</span></td></tr><tr><td>`min_tm`</td><td><span>⭐⭐⭐☆☆ (3/5)</span></td><td><strong><span>部分合理</span></strong></td><td><span>• </span><strong><span>高</span></strong><span>: 60°C不适合所有场景</span><br><span>• 体外转录通常55°C</span><br><span>• qPCR需要更高Tm</span></td><td><strong><span>必须改进</span></strong><span>: 询问用户应用类型:</span><br><span>"请问引物用途: 体外转录/RT-PCR/结构探测?"</span></td></tr><tr><td>`length_range`</td><td><span>⭐⭐⭐⭐☆ (4/5)</span></td><td><strong><span>基本合理</span></strong></td><td><span>• 低: [15-60]覆盖大多数场景</span><br><span>• 超长RNA可能需要更长引物</span></td><td><span>根据序列长度动态调整</span></td></tr><tr><td>`prefix`</td><td><span>⭐⭐⭐⭐⭐ (5/5)</span></td><td><strong><span>非常合理</span></strong></td><td><span>• 极低: 有意义的命名便于管理</span></td><td><span>无需改进</span></td></tr></tbody></table></div><hr><h2><span>总体评估</span></h2><h3><span>总体评分: ⭐⭐⭐⭐☆ (4.2/5)</span></h3><h3><span>各工具评分汇总</span></h3><div class="ds-scroll-area _1210dd7 c03cafe9"><div class="ds-scroll-area__gutters" style="position: sticky; top: 0px; left: 0px; right: 0px; height: 0px; --container-height: 274px;"><div class="ds-scroll-area__horizontal-gutter" style="left: 0px; right: 0px; top: calc(var(--container-height) - 14px); height: 10px;"><div class="ds-scroll-area__horizontal-bar" style="display: none;"></div></div><div class="ds-scroll-area__vertical-gutter" style="right: 0px; top: 8px; bottom: calc(0px - var(--container-height) + 8px); width: 10px;"><div class="ds-scroll-area__vertical-bar" style="display: none;"></div></div></div><table><thead><tr><th><span>工具</span></th><th><span>平均评分</span></th><th><span>最高分参数</span></th><th><span>最低分参数</span></th><th><span>主要风险</span></th></tr></thead><tbody><tr><td><strong><span>cds_optimizer</span></strong></td><td><span>4.0/5</span></td><td><span>organism (5/5)</span></td><td><span>gc_range (3/5)</span></td><td><span>GC范围固定不适配</span></td></tr><tr><td><strong><span>overhang_designer</span></strong></td><td><span>4.7/5</span></td><td><span>num_overhangs, enzyme (5/5)</span></td><td><span>existing_overhangs (4/5)</span></td><td><span>非标准框架提取失败</span></td></tr><tr><td><strong><span>assembly_simulator</span></strong></td><td><span>4.3/5</span></td><td><span>fragments, enzyme (5/5)</span></td><td><span>framework (3/5)</span></td><td><span>默认pET28a不适合真核</span></td></tr><tr><td><strong><span>plasmid_visualizer</span></strong></td><td><span>4.6/5</span></td><td><span>sequence, circular, name (5/5)</span></td><td><span>features, output_format (4/5)</span></td><td><span>复杂特征识别不足</span></td></tr><tr><td><strong><span>primer_designer</span></strong></td><td><span>4.0/5</span></td><td><span>prefix (5/5)</span></td><td><span>min_tm (3/5)</span></td><td><span>Tm值不匹配应用场景</span></td></tr></tbody></table></div><h3><span>优势分析</span></h3><div class="ds-scroll-area _1210dd7 c03cafe9"><div class="ds-scroll-area__gutters" style="position: sticky; top: 0px; left: 0px; right: 0px; height: 0px; --container-height: 253px;"><div class="ds-scroll-area__horizontal-gutter" style="left: 0px; right: 0px; top: calc(var(--container-height) - 14px); height: 10px;"><div class="ds-scroll-area__horizontal-bar" style="display: none;"></div></div><div class="ds-scroll-area__vertical-gutter" style="right: 0px; top: 8px; bottom: calc(0px - var(--container-height) + 8px); width: 10px;"><div class="ds-scroll-area__vertical-bar" style="display: none;"></div></div></div><table><thead><tr><th><span>优势</span></th><th><span>评分</span></th><th><span>说明</span></th><th><span>示例</span></th></tr></thead><tbody><tr><td><strong><span>参数传递自动化</span></strong></td><td><span>⭐⭐⭐⭐⭐</span></td><td><span>工具间无缝传递数据</span></td><td><span>optimized_sequence → assembly → visualization</span></td></tr><tr><td><strong><span>多格式兼容性</span></strong></td><td><span>⭐⭐⭐⭐⭐</span></td><td><span>assembly_simulator支持4种输入格式</span></td><td><span>来自不同来源的fragments都能处理</span></td></tr><tr><td><strong><span>生物学规则遵循</span></strong></td><td><span>⭐⭐⭐⭐⭐</span></td><td><span>n+1规则、Golden Gate标准</span></td><td><span>num_overhangs自动计算</span></td></tr><tr><td><strong><span>命名规范</span></strong></td><td><span>⭐⭐⭐⭐⭐</span></td><td><span>描述性、标准化的命名</span></td><td><span>pET28a-GFP-His6-optimized</span></td></tr></tbody></table></div><h3><span>风险点汇总</span></h3><div class="ds-scroll-area _1210dd7 c03cafe9"><div class="ds-scroll-area__gutters" style="position: sticky; top: 0px; left: 0px; right: 0px; height: 0px; --container-height: 320px;"><div class="ds-scroll-area__horizontal-gutter" style="left: 0px; right: 0px; top: calc(var(--container-height) - 14px); height: 10px;"><div class="ds-scroll-area__horizontal-bar" style="display: none;"></div></div><div class="ds-scroll-area__vertical-gutter" style="right: 0px; top: 8px; bottom: calc(0px - var(--container-height) + 8px); width: 10px;"><div class="ds-scroll-area__vertical-bar" style="display: none;"></div></div></div><table><thead><tr><th><span>风险</span></th><th><span>严重性</span></th><th><span>发生概率</span></th><th><span>影响范围</span></th><th><span>解决优先级</span></th></tr></thead><tbody><tr><td><strong><span>organism未传递导致framework错误</span></strong></td><td><span>🔴 高</span></td><td><span>中 (40%)</span></td><td><span>cds_optimizer → assembly_simulator</span></td><td><strong><span>P0 - 立即修复</span></strong></td></tr><tr><td><strong><span>enzyme不一致导致组装失败</span></strong></td><td><span>🔴 高</span></td><td><span>低 (15%)</span></td><td><span>整个工作流</span></td><td><strong><span>P0 - 立即修复</span></strong></td></tr><tr><td><strong><span>GC范围不适配organism</span></strong></td><td><span>🟡 中</span></td><td><span>高 (70%)</span></td><td><span>cds_optimizer</span></td><td><strong><span>P1 - 1周内</span></strong></td></tr><tr><td><strong><span>framework默认值不适合真核</span></strong></td><td><span>🟡 中</span></td><td><span>中 (50%)</span></td><td><span>assembly_simulator</span></td><td><strong><span>P1 - 1周内</span></strong></td></tr><tr><td><strong><span>Tm值不匹配应用场景</span></strong></td><td><span>🟡 中</span></td><td><span>中 (40%)</span></td><td><span>primer_designer</span></td><td><strong><span>P2 - 2周内</span></strong></td></tr><tr><td><strong><span>AI补全不透明</span></strong></td><td><span>🟢 低</span></td><td><span>高 (80%)</span></td><td><span>所有工具</span></td><td><strong><span>P2 - 2周内</span></strong></td></tr></tbody></table></div><hr><h2><span>工作流参数一致性</span></h2><h3><span>全局参数定义</span></h3><p class="ds-markdown-paragraph"><span>以下参数必须在整个工作流中保持一致：</span></p><div class="ds-scroll-area _1210dd7 c03cafe9"><div class="ds-scroll-area__gutters" style="position: sticky; top: 0px; left: 0px; right: 0px; height: 0px; --container-height: 208px;"><div class="ds-scroll-area__horizontal-gutter" style="left: 0px; right: 0px; top: calc(var(--container-height) - 14px); height: 10px;"><div class="ds-scroll-area__horizontal-bar" style="display: none;"></div></div><div class="ds-scroll-area__vertical-gutter" style="right: 0px; top: 8px; bottom: calc(0px - var(--container-height) + 8px); width: 10px;"><div class="ds-scroll-area__vertical-bar" style="display: none;"></div></div></div><table><thead><tr><th><span>全局参数</span></th><th><span>涉及工具</span></th><th><span>一致性要求</span></th><th><span>当前状态</span></th><th><span>验证机制</span></th></tr></thead><tbody><tr><td>`organism`</td><td><span>cds_optimizer, assembly_simulator</span></td><td><strong><span>强制一致</span></strong></td><td><span>❌ 未验证</span></td><td><span>需要添加WorkflowValidator</span></td></tr><tr><td>`enzyme`</td><td><span>cds_optimizer, overhang_designer, assembly_simulator</span></td><td><strong><span>强制一致</span></strong></td><td><span>❌ 未验证</span></td><td><span>需要添加enzyme链验证</span></td></tr><tr><td>`framework`</td><td><span>assembly_simulator, plasmid_visualizer</span></td><td><strong><span>建议一致</span></strong></td><td><span>❌ 未验证</span></td><td><span>建议添加提示</span></td></tr></tbody></table></div><h3><span>参数传递链</span></h3><div class="md-code-block md-code-block-light"><div class="md-code-block-banner-wrap"><div class="md-code-block-banner md-code-block-banner-lite"><div class="_121d384"><div class="d2a24f03"><span class="d813de27">text</span></div><div class="d2a24f03 _246a029"><div class="efa13877"><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon" style="margin-right: 4px;"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.14923 4.02032C7.11191 4.02032 7.87977 4.02017 8.49591 4.07599C9.12122 4.1327 9.65786 4.25188 10.1414 4.53107C10.7201 4.8653 11.2008 5.34591 11.535 5.92462C11.8142 6.40818 11.9333 6.94482 11.9901 7.57013C12.0459 8.18625 12.0457 8.9542 12.0457 9.91681C12.0457 10.8795 12.0459 11.6474 11.9901 12.2635C11.9333 12.8888 11.8142 13.4254 11.535 13.909C11.2008 14.4877 10.7201 14.9683 10.1414 15.3026C9.65786 15.5817 9.12122 15.7009 8.49591 15.7576C7.87977 15.8134 7.1119 15.8133 6.14923 15.8133C5.18661 15.8133 4.41868 15.8134 3.80255 15.7576C3.17724 15.7009 2.6406 15.5817 2.15704 15.3026C1.57834 14.9684 1.09772 14.4877 0.763489 13.909C0.484305 13.4254 0.365123 12.8888 0.308411 12.2635C0.252587 11.6474 0.252747 10.8795 0.252747 9.91681C0.252747 8.95419 0.252603 8.18625 0.308411 7.57013C0.365123 6.94482 0.484305 6.40818 0.763489 5.92462C1.09771 5.3459 1.57833 4.86529 2.15704 4.53107C2.6406 4.25188 3.17724 4.1327 3.80255 4.07599C4.41868 4.02018 5.1866 4.02032 6.14923 4.02032ZM6.14923 5.37775C5.16175 5.37775 4.46628 5.37761 3.9256 5.42657C3.39428 5.47473 3.07853 5.56574 2.83575 5.70587C2.46313 5.92106 2.15348 6.23071 1.93829 6.60333C1.79817 6.84611 1.70715 7.16185 1.659 7.69318C1.61004 8.23385 1.61017 8.92934 1.61017 9.91681C1.61017 10.9043 1.61002 11.5998 1.659 12.1404C1.70715 12.6717 1.79817 12.9875 1.93829 13.2303C2.15349 13.6029 2.46315 13.9126 2.83575 14.1277C3.07853 14.2679 3.39428 14.3589 3.9256 14.407C4.46628 14.456 5.16176 14.4559 6.14923 14.4559C7.13675 14.4559 7.83218 14.456 8.37286 14.407C8.90419 14.3589 9.21993 14.2679 9.46271 14.1277C9.83529 13.9126 10.145 13.6029 10.3602 13.2303C10.5003 12.9875 10.5913 12.6718 10.6395 12.1404C10.6884 11.5998 10.6883 10.9043 10.6883 9.91681C10.6883 8.92935 10.6884 8.23385 10.6395 7.69318C10.5913 7.16185 10.5003 6.84611 10.3602 6.60333C10.145 6.23072 9.8353 5.92107 9.46271 5.70587C9.21993 5.56574 8.90418 5.47473 8.37286 5.42657C7.83218 5.3776 7.13676 5.37775 6.14923 5.37775ZM9.80157 0.367981C10.7637 0.367981 11.5313 0.367886 12.1473 0.423645C12.7725 0.480313 13.3093 0.598765 13.7928 0.877747C14.3716 1.21192 14.852 1.69355 15.1863 2.27228C15.4655 2.75575 15.5857 3.29165 15.6424 3.91681C15.6982 4.53301 15.6971 5.30161 15.6971 6.26447V7.8299C15.6971 8.29265 15.6989 8.58994 15.6649 8.84845C15.4667 10.3525 14.4009 11.5738 12.9832 11.9988V10.5467C13.6973 10.1903 14.2104 9.49662 14.3192 8.67169C14.3387 8.52348 14.3406 8.3358 14.3406 7.8299V6.26447C14.3406 5.27707 14.3398 4.58149 14.2908 4.04083C14.2427 3.50969 14.1526 3.19373 14.0125 2.95099C13.7974 2.5785 13.4875 2.2687 13.1151 2.05353C12.8723 1.91347 12.5563 1.82237 12.0252 1.77423C11.4846 1.72528 10.7888 1.7254 9.80157 1.7254H7.71466C6.75614 1.72559 5.92659 2.27697 5.52325 3.07892H4.07013C4.54215 1.51132 5.99314 0.368192 7.71466 0.367981H9.80157Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">复制</span></span><div class="ds-focus-ring"></div></button><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M15.3695 11.411L15.1234 12.8866C14.8869 14.3042 13.6603 15.3436 12.223 15.3436H3.7767C2.33954 15.3434 1.11276 14.3042 0.876312 12.8866L0.630219 11.411L2.05405 11.1747L2.29916 12.6493C2.41969 13.3713 3.04472 13.9001 3.7767 13.9003H12.223C12.9551 13.9002 13.58 13.3713 13.7005 12.6493L13.9456 11.1747L15.3695 11.411ZM8.72202 8.994C8.77714 8.93934 8.83789 8.88106 8.90268 8.81627L12.4828 5.23424L13.5042 6.25572L9.92221 9.8358C9.63947 10.1185 9.3876 10.3732 9.15854 10.5575C8.91889 10.7503 8.6395 10.9224 8.28647 10.9784C8.09708 11.0083 7.9036 11.0083 7.7142 10.9784C7.36103 10.9224 7.08087 10.7503 6.84116 10.5575C6.61212 10.3732 6.36019 10.1185 6.07748 9.8358L2.49643 6.25572L3.51694 5.23424L7.09702 8.81627C7.16216 8.88142 7.22327 8.94006 7.27866 8.99498V1.3065H8.72202V8.994Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">下载</span></span><div class="ds-focus-ring"></div></button></div></div></div></div></div><pre>用户输入: sequence, organism
    ↓
[cds_optimizer]
    • sequence (用户输入)
    • organism (用户输入/AI推断)
    • avoid_enzymes (AI补全 - Golden Gate)
    • gc_range (默认/AI动态调整)
    ↓ 输出: optimized_sequence
    ↓
[overhang_designer]
    • num_overhangs (AI计算 - n+1规则)
    • enzyme (继承 - 与cds一致)
    • existing_overhangs (AI提取 - 框架)
    ↓ 输出: designed_overhangs
    ↓
[assembly_simulator]
    • fragments (自动组合 - 前序输出)
    • enzyme (继承 - 全局一致)
    • framework (AI选择 - 基于organism)
    • include_reports (默认true)
    ↓ 输出: final_sequence
    ↓
[plasmid_visualizer]
    • sequence (传递 - assembly输出)
    • features (AI识别 - 框架定义)
    • plasmid_name (AI生成 - 描述性)
    • circular (AI推断 - 类型判断)
    • output_format (默认/用户需求)
    ↓ 输出: image_path, image_base64

独立分支:
[primer_designer]
    • sequence (DNA→RNA转换)
    • min_tm (默认/AI应用调整)
    • min_length, max_length (默认/AI长度优化)
    • prefix (AI项目命名)</pre><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _33882ae"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _28d7e84"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg></div>

