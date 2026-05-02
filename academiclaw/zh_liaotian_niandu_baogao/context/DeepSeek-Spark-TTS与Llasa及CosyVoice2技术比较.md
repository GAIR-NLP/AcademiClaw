### 用户

把他们三个进行比较，详细列出他们的核心技术（例如自回归非自回归等）

---

### DeepSeek AI

<p>思考：</p><blockquote><p class="ds-markdown-paragraph"><span>首先，用户要求将“他们三个”进行比较，并详细列出他们的核心技术，包括自回归、非自回归等。从上下文看，“他们三个”可能指的是论文中提到的三个模型：Spark-TTS、Llasa 和 CosyVoice2。因为论文中提到了这些模型在零样本TTS方面的比较。</span></p><p class="ds-markdown-paragraph"><span>在论文中，Spark-TTS 是主要介绍的模型，而 Llasa 和 CosyVoice2 是作为比较对象。具体来说：</span></p><ul><li><p class="ds-markdown-paragraph"><span>Spark-TTS：基于 BiCodec 和 Qwen2.5 LLM 的 TTS 模型，使用单流解码的语音令牌，支持零样本语音克隆和属性控制。</span></p></li><li><p class="ds-markdown-paragraph"><span>Llasa：基于 FSQ 令牌化器和 LLaMA 的语音合成模型，使用单流代码预测。</span></p></li><li><p class="ds-markdown-paragraph"><span>CosyVoice2：一个两阶段模型，使用自回归语言模型预测语义令牌，然后使用流匹配生成声学特征。</span></p></li></ul><p class="ds-markdown-paragraph"><span>用户特别提到了“自回归非自回归等”，所以需要关注这些模型在生成方式上的区别。</span></p><p class="ds-markdown-paragraph"><span>从论文中提取关键信息：</span></p><ul><li><p class="ds-markdown-paragraph"><span>Spark-TTS：使用自回归（AR）语言模型预测令牌。它基于 Qwen2.5，一个 decoder-only transformer，用于预测语义令牌和全局令牌。推理时，它使用 chain-of-thought（CoT）方式生成令牌。</span></p></li><li><p class="ds-markdown-paragraph"><span>Llasa：也使用自回归语言模型（LLaMA）进行单流代码预测。论文中提到 Llasa 是单阶段 AR 方法。</span></p></li><li><p class="ds-markdown-paragraph"><span>CosyVoice2：两阶段模型，第一阶段使用 AR LM 预测语义令牌，第二阶段使用流匹配（flow matching）生成声学特征。流匹配是一种非自回归（NAR）方法吗？流匹配通常是基于扩散或流的方法，可能不是自回归的，但需要确认。</span></p></li></ul><p class="ds-markdown-paragraph"><span>在论文的第6.4节和表格4中，模型被分类为“Multi-Stage or NAR Methods”和“One-Stage AR Methods”。其中：</span></p><ul><li><p class="ds-markdown-paragraph"><span>CosyVoice2 被列为多阶段或 NAR 方法。</span></p></li><li><p class="ds-markdown-paragraph"><span>Llasa 和 Spark-TTS 被列为一阶段 AR 方法。</span></p></li></ul><p class="ds-markdown-paragraph"><span>所以，核心技术总结：</span></p><ul><li><p class="ds-markdown-paragraph"><span>Spark-TTS：一阶段自回归（AR）方法，使用 LLM 直接预测语音令牌。</span></p></li><li><p class="ds-markdown-paragraph"><span>Llasa：一阶段自回归（AR）方法，使用 LLM 预测单流代码。</span></p></li><li><p class="ds-markdown-paragraph"><span>CosyVoice2：两阶段方法，第一阶段是 AR 用于语义令牌，第二阶段是流匹配（属于 NAR）用于声学特征。</span></p></li></ul><p class="ds-markdown-paragraph"><span>现在，详细列出每个模型的核心技术：</span></p><ol start="1"><li><p class="ds-markdown-paragraph"><strong><span>Spark-TTS</span></strong><span>:</span></p><ul><li><p class="ds-markdown-paragraph"><span>令牌化: BiCodec，将语音分解为语义令牌和全局令牌。语义令牌捕获语言内容，全局令牌捕获说话人属性。</span></p></li><li><p class="ds-markdown-paragraph"><span>语言模型: 基于 Qwen2.5 的自回归 decoder-only transformer。</span></p></li><li><p class="ds-markdown-paragraph"><span>生成方式: 自回归预测令牌，支持零样本 TTS 和属性控制通过 CoT。</span></p></li><li><p class="ds-markdown-paragraph"><span>训练目标: 混合损失，包括零样本 TTS 损失和控制损失。</span></p></li></ul></li><li><p class="ds-markdown-paragraph"><strong><span>Llasa</span></strong><span>:</span></p><ul><li><p class="ds-markdown-paragraph"><span>令牌化: 基于 FSQ 的单流令牌化器，代码本大小 65,536。</span></p></li><li><p class="ds-markdown-paragraph"><span>语言模型: 基于 LLaMA 的自回归语言模型。</span></p></li><li><p class="ds-markdown-paragraph"><span>生成方式: 自回归预测单流代码。</span></p></li><li><p class="ds-markdown-paragraph"><span>训练数据: 250k 小时，模型参数 8B。</span></p></li></ul></li><li><p class="ds-markdown-paragraph"><strong><span>CosyVoice2</span></strong><span>:</span></p><ul><li><p class="ds-markdown-paragraph"><span>令牌化: 使用语义令牌和声学特征。</span></p></li><li><p class="ds-markdown-paragraph"><span>两阶段生成:</span></p><ul><li><p class="ds-markdown-paragraph"><span>阶段1: 自回归语言模型预测语义令牌。</span></p></li><li><p class="ds-markdown-paragraph"><span>阶段2: 流匹配生成声学特征（非自回归）。</span></p></li></ul></li><li><p class="ds-markdown-paragraph"><span>训练数据: 未在论文中详细说明，但参考 CosyVoice。</span></p></li></ul></li></ol><p class="ds-markdown-paragraph"><span>此外，论文中还提到了其他模型如 Seed-TTS、F5-TTS 等，但用户指定了“他们三个”，所以聚焦于 Spark-TTS、Llasa 和 CosyVoice2。</span></p><p class="ds-markdown-paragraph"><span>在比较时，应该包括：</span></p><ul><li><p class="ds-markdown-paragraph"><span>模型架构（AR vs NAR）</span></p></li><li><p class="ds-markdown-paragraph"><span>令牌化方法</span></p></li><li><p class="ds-markdown-paragraph"><span>语言模型类型</span></p></li><li><p class="ds-markdown-paragraph"><span>生成流程</span></p></li><li><p class="ds-markdown-paragraph"><span>控制能力</span></p></li></ul><p class="ds-markdown-paragraph"><span>最后，以表格形式呈现比较结果，然后详细描述。</span></p></blockquote><br/><p class="ds-markdown-paragraph"><span>根据提供的 Spark-TTS 论文内容，我将对三个主要的 TTS 模型进行详细比较：</span><strong><span>Spark-TTS</span></strong><span>、</span><strong><span>Llasa</span></strong><span> 和 </span><strong><span>CosyVoice2</span></strong><span>。这些模型在零样本文本到语音（TTS）任务中表现出色，但它们在核心技术、架构和生成方式上存在显著差异。以下将重点比较它们的核心技术，包括自回归（AR）与非自回归（NAR）方法、令牌化策略、语言模型架构等。</span></p><h3><span>模型概述</span></h3><ul><li><p class="ds-markdown-paragraph"><strong><span>Spark-TTS</span></strong><span>：基于 BiCodec 令牌化和 Qwen2.5 LLM 的单流自回归模型，支持零样本语音克隆和细粒度属性控制。</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>Llasa</span></strong><span>：基于 FSQ 令牌化和 LLaMA LLM 的单流自回归模型，专注于零样本 TTS，但控制能力较弱。</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>CosyVoice2</span></strong><span>：两阶段模型，结合自回归语言模型（语义令牌预测）和流匹配（声学特征生成），属于混合 AR-NAR 方法。</span></p></li></ul><h3><span>核心技术比较</span></h3><p class="ds-markdown-paragraph"><span>下表详细列出了三个模型的核心技术特点：</span></p><div class="ds-scroll-area _1210dd7 c03cafe9"><div class="ds-scroll-area__gutters" style="position: sticky; top: 0px; left: 0px; right: 0px; height: 0px; --container-height: 607px;"><div class="ds-scroll-area__horizontal-gutter" style="left: 0px; right: 0px; top: calc(var(--container-height) - 14px); height: 10px;"><div class="ds-scroll-area__horizontal-bar" style="left: 0px; width: 955.7px;"></div></div><div class="ds-scroll-area__vertical-gutter" style="right: 0px; top: 8px; bottom: calc(0px - var(--container-height) + 8px); width: 10px;"><div class="ds-scroll-area__vertical-bar" style="display: none;"></div></div></div><table><thead><tr><th><span>技术特征</span></th><th><span>Spark-TTS</span></th><th><span>Llasa</span></th><th><span>CosyVoice2</span></th></tr></thead><tbody><tr><td><strong><span>生成方式</span></strong></td><td><span>一阶段自回归（AR）</span></td><td><span>一阶段自回归（AR）</span></td><td><span>两阶段混合（AR + NAR）</span></td></tr><tr><td><strong><span>令牌化方法</span></strong></td><td><span>BiCodec：单流混合令牌（语义令牌 + 全局令牌）</span></td><td><span>FSQ-based 单流令牌（代码本大小 65,536）</span></td><td><span>语义令牌 + 声学特征（通过流匹配生成）</span></td></tr><tr><td><strong><span>语言模型</span></strong></td><td><span>Qwen2.5（decoder-only transformer）</span></td><td><span>LLaMA（decoder-only transformer）</span></td><td><span>自回归 LM（语义令牌） + 流匹配模型（声学特征）</span></td></tr><tr><td><strong><span>控制能力</span></strong></td><td><span>支持粗粒度和细粒度控制（性别、音高、语速） via Chain-of-Thought (CoT)</span></td><td><span>仅支持零样本 TTS，无显式属性控制</span></td><td><span>可能支持部分控制（但论文未强调）</span></td></tr><tr><td><strong><span>训练数据</span></strong></td><td><span>VoxBox（100k 小时）</span></td><td><span>250k 小时</span></td><td><span>未详细说明（基于 CosyVoice）</span></td></tr><tr><td><strong><span>模型参数</span></strong></td><td><span>0.5B</span></td><td><span>8B</span></td><td><span>未详细说明</span></td></tr><tr><td><strong><span>推理效率</span></strong></td><td><span>单流 AR，直接生成令牌，无需多阶段</span></td><td><span>单流 AR，直接生成令牌</span></td><td><span>两阶段，需先生成语义令牌再生成声学特征，可能较慢</span></td></tr><tr><td><strong><span>零样本 TTS 性能</span></strong></td><td><span>高智能度（CER/WER 低），但说话人相似性略低于多阶段方法</span></td><td><span>中等智能度和说话人相似性</span></td><td><span>中等智能度，说话人相似性较好</span></td></tr><tr><td><strong><span>关键创新</span></strong></td><td><span>BiCodec 令牌化、全局令牌、CoT 属性控制、VoxBox 数据集</span></td><td><span>FSQ 令牌化、单流代码预测</span></td><td><span>流匹配用于声学特征生成，提升自然度</span></td></tr></tbody></table></div><h3><span>详细技术分析</span></h3><h4><span>1. </span><strong><span>生成方式：自回归 vs. 非自回归</span></strong></h4><ul><li><p class="ds-markdown-paragraph"><strong><span>Spark-TTS</span></strong><span>：使用</span><strong><span>一阶段自回归（AR）</span></strong><span> 生成。语言模型直接预测语音令牌序列（语义令牌和全局令牌），每个令牌的生成依赖于之前生成的令牌。这种方式简单且与文本 LLM 一致，但可能引入随机性，影响说话人相似性。</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>Llasa</span></strong><span>：同样采用</span><strong><span>一阶段自回归（AR）</span></strong><span> 生成，使用 LLaMA 模型预测单流代码。AR 方法允许高质量生成，但计算开销较大。</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>CosyVoice2</span></strong><span>：采用</span><strong><span>两阶段混合方法</span></strong><span>：</span></p><ul><li><p class="ds-markdown-paragraph"><strong><span>阶段1（AR）</span></strong><span>：自回归语言模型预测语义令牌。</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>阶段2（NAR）</span></strong><span>：使用流匹配（flow matching）生成声学特征，这是一种</span><strong><span>非自回归（NAR）</span></strong><span> 方法，可以并行生成，提高效率。流匹配基于扩散模型原理，生成过程稳定。</span></p></li></ul></li></ul><h4><span>2. </span><strong><span>令牌化方法</span></strong></h4><ul><li><p class="ds-markdown-paragraph"><strong><span>Spark-TTS</span></strong><span>：提出 </span><strong><span>BiCodec</span></strong><span>，将语音分解为：</span></p><ul><li><p class="ds-markdown-paragraph"><strong><span>语义令牌</span></strong><span>：50 TPS，捕获语言内容，基于 wav2vec 2.0 特征。</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>全局令牌</span></strong><span>：固定长度（如 32），捕获说话人属性，使用 FSQ 量化。</span></p></li><li><p class="ds-markdown-paragraph"><span>这种解耦允许细粒度控制，同时保持低比特率（0.65 kbps）。</span></p></li></ul></li><li><p class="ds-markdown-paragraph"><strong><span>Llasa</span></strong><span>：使用 </span><strong><span>FSQ-based 令牌化</span></strong><span>，将语音编码为单流代码，代码本大小 65,536。FSQ 避免了 VQ 的训练崩溃问题，但缺乏显式的属性分离。</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>CosyVoice2</span></strong><span>：依赖于</span><strong><span>语义令牌</span></strong><span>和</span><strong><span>声学特征</span></strong><span>。语义令牌通过自回归 LM 预测，声学特征通过流匹配生成，可能使用类似 MEL 谱的特征。</span></p></li></ul><h4><span>3. </span><strong><span>语言模型架构</span></strong></h4><ul><li><p class="ds-markdown-paragraph"><strong><span>Spark-TTS</span></strong><span>：基于 </span><strong><span>Qwen2.5-0.5B</span></strong><span>（decoder-only transformer），通过微调集成 TTS 能力。支持多语言文本令牌化和属性令牌化。</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>Llasa</span></strong><span>：基于 </span><strong><span>LLaMA</span></strong><span>（decoder-only transformer），参数更大（8B），但训练数据更多（250k 小时）。</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>CosyVoice2</span></strong><span>：使用</span><strong><span>自回归 LM</span></strong><span> 用于语义令牌预测，并结合</span><strong><span>流匹配模型</span></strong><span>用于声学特征生成。流匹配是一种生成模型，类似于扩散模型，但具有更稳定的训练。</span></p></li></ul><h4><span>4. </span><strong><span>控制能力</span></strong></h4><ul><li><p class="ds-markdown-paragraph"><strong><span>Spark-TTS</span></strong><span>：通过 </span><strong><span>Chain-of-Thought (CoT)</span></strong><span> 实现分层控制：</span></p><ul><li><p class="ds-markdown-paragraph"><strong><span>粗粒度</span></strong><span>：性别、音高水平、语速水平。</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>细粒度</span></strong><span>：精确音高值、语速值。</span></p></li><li><p class="ds-markdown-paragraph"><span>无需参考音频即可生成新语音。</span></p></li></ul></li><li><p class="ds-markdown-paragraph"><strong><span>Llasa</span></strong><span>：专注于零样本 TTS，无显式属性控制功能。</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>CosyVoice2</span></strong><span>：可能支持基于文本提示的控制，但论文未强调细粒度属性控制。</span></p></li></ul><h4><span>5. </span><strong><span>性能对比</span></strong></h4><ul><li><p class="ds-markdown-paragraph"><strong><span>零样本 TTS</span></strong><span>：</span></p><ul><li><p class="ds-markdown-paragraph"><span>Spark-TTS 在智能度（CER/WER）上表现优异，但说话人相似性略低于多阶段方法（如 Seed-TTS）。</span></p></li><li><p class="ds-markdown-paragraph"><span>Llasa 在相似参数下性能较弱，Spark-TTS 以 0.5B 参数超越 Llasa-8B。</span></p></li><li><p class="ds-markdown-paragraph"><span>CosyVoice2 在质量上竞争，但两阶段架构可能增加复杂性。</span></p></li></ul></li><li><p class="ds-markdown-paragraph"><strong><span>重建质量</span></strong><span>：</span></p><ul><li><p class="ds-markdown-paragraph"><span>BiCodec 在低比特率（&lt;1 kbps）下达到 SOTA 重建质量。</span></p></li><li><p class="ds-markdown-paragraph"><span>Llasa 和 CosyVoice2 的令牌化方法也高效，但 BiCodec 的混合令牌提供更好控制。</span></p></li></ul></li></ul><h3><span>总结</span></h3><ul><li><p class="ds-markdown-paragraph"><strong><span>Spark-TTS</span></strong><span> 的核心优势在于其 </span><strong><span>BiCodec 令牌化</span></strong><span> 和 </span><strong><span>CoT 控制</span></strong><span>，实现了高效且可控的 TTS，同时保持与文本 LLM 的架构一致性。</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>Llasa</span></strong><span> 专注于缩放模型和数据，但缺乏控制功能。</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>CosyVoice2</span></strong><span> 通过 </span><strong><span>流匹配</span></strong><span> 提升声学质量，但两阶段架构可能限制效率和灵活性。</span></p></li></ul><p class="ds-markdown-paragraph"><span>这些模型代表了 TTS 领域的不同方向：Spark-TTS 强调控制和效率，Llasa 强调缩放，CosyVoice2 强调声学质量。选择取决于具体应用需求，如是否需要属性控制或实时生成。</span></p>

---

### 用户

把上面的这些内容写成latex格式，要求只使用最基本的package，格式简洁

---

### DeepSeek AI

<p>思考：</p><blockquote><p class="ds-markdown-paragraph"><span>我们首先需要确定文档的基本结构：使用article文档类，并引入必要的包。由于要求只使用最基本的package，我们将使用：</span></p><ul><li><p class="ds-markdown-paragraph"><span>amsmath 用于数学公式</span></p></li><li><p class="ds-markdown-paragraph"><span>graphicx 用于插入图片（虽然这里没有图片，但通常论文中会有）</span></p></li><li><p class="ds-markdown-paragraph"><span>array 用于表格排版</span></p></li><li><p class="ds-markdown-paragraph"><span>booktabs 用于制作三线表，使表格更美观</span></p></li><li><p class="ds-markdown-paragraph"><span>multirow 用于表格中跨行</span></p></li><li><p class="ds-markdown-paragraph"><span>xcolor 用于颜色（虽然这里可能不需要，但为了基本，先不引入，除非必要）</span></p></li></ul><p class="ds-markdown-paragraph"><span>但是，由于我们只是生成一个表格和描述，实际上可能不需要所有包。我们根据内容来定。</span></p><p class="ds-markdown-paragraph"><span>注意：我们不会实际插入图片，所以graphicx可能不需要。但是，我们可能会引用图表，所以我们可以使用graphicx来预留位置。</span></p><p class="ds-markdown-paragraph"><span>但是，由于问题中要求只使用最基本的package，我们可以考虑仅使用amsmath和array，以及booktabs。如果不需要图片，就不用graphicx。</span></p><p class="ds-markdown-paragraph"><span>另外，我们可能会需要用到一些数学符号，所以amsmath是必要的。</span></p><p class="ds-markdown-paragraph"><span>由于内容较多，我们将使用一个表格来比较三个模型，然后配合段落描述。</span></p><p class="ds-markdown-paragraph"><span>步骤：</span></p><ol start="1"><li><p class="ds-markdown-paragraph"><span>文档类设置</span></p></li><li><p class="ds-markdown-paragraph"><span>引入必要的包</span></p></li><li><p class="ds-markdown-paragraph"><span>开始文档</span></p></li><li><p class="ds-markdown-paragraph"><span>节和子节</span></p></li><li><p class="ds-markdown-paragraph"><span>表格和描述</span></p></li></ol><p class="ds-markdown-paragraph"><span>注意：由于内容较长，我们可能需要调整表格的列宽，使用p{宽度}来调整。</span></p><p class="ds-markdown-paragraph"><span>由于是纯文本比较，我们可以使用一个长表格，并适当调整列宽。</span></p><p class="ds-markdown-paragraph"><span>我们使用一个表格，列出三个模型的多个方面。</span></p><p class="ds-markdown-paragraph"><span>由于表格可能太宽，我们可以使用侧放表格（landscape）但是这样需要pdflscape包，但问题要求基本包，所以我们不侧放，而是调整列宽和字体大小。</span></p><p class="ds-markdown-paragraph"><span>我们可以使用small字体，或者调整列宽。</span></p><p class="ds-markdown-paragraph"><span>我们尝试设计一个表格，包含以下列：技术特征、Spark-TTS、Llasa、CosyVoice2。</span></p><p class="ds-markdown-paragraph"><span>由于技术特征这一列可能较宽，我们将其设置为固定宽度，其他三列平均分配剩余宽度。</span></p><p class="ds-markdown-paragraph"><span>我们使用tabularx包来平衡列宽，但是问题要求基本包，所以我们不使用tabularx，而是使用普通的tabular和p{宽度}。</span></p><p class="ds-markdown-paragraph"><span>我们设定表格总宽度为\textwidth，然后第一列宽度为0.4\textwidth，其他三列各0.2\textwidth。</span></p><p class="ds-markdown-paragraph"><span>但是，由于表格内容较多，我们也可以使用一个更灵活的方式：使用三个子表格并逐个描述，但这样不够直观。</span></p><p class="ds-markdown-paragraph"><span>我们决定使用一个长表格，并在每个特征上详细描述。</span></p><p class="ds-markdown-paragraph"><span>由于表格可能会跨页，我们使用longtable包，但是问题要求基本包，所以我们不使用longtable，而是让表格自然跨页（如果内容太多，article文档类会自动跨页，但表格不会断开，所以可能需要手动调整）。</span></p><p class="ds-markdown-paragraph"><span>考虑到这个表格可能不会太长，我们使用普通的tabular。</span></p><p class="ds-markdown-paragraph"><span>如果表格太长，我们可以使用longtable，但这里我们先尝试普通表格。</span></p><p class="ds-markdown-paragraph"><span>我们开始编写。</span></p></blockquote><br/><div class="md-code-block md-code-block-light"><div class="md-code-block-banner-wrap"><div class="md-code-block-banner md-code-block-banner-lite"><div class="_121d384"><div class="d2a24f03"><span class="d813de27">latex</span></div><div class="d2a24f03 _246a029"><div class="efa13877"><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon" style="margin-right: 4px;"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.14923 4.02032C7.11191 4.02032 7.87977 4.02017 8.49591 4.07599C9.12122 4.1327 9.65786 4.25188 10.1414 4.53107C10.7201 4.8653 11.2008 5.34591 11.535 5.92462C11.8142 6.40818 11.9333 6.94482 11.9901 7.57013C12.0459 8.18625 12.0457 8.9542 12.0457 9.91681C12.0457 10.8795 12.0459 11.6474 11.9901 12.2635C11.9333 12.8888 11.8142 13.4254 11.535 13.909C11.2008 14.4877 10.7201 14.9683 10.1414 15.3026C9.65786 15.5817 9.12122 15.7009 8.49591 15.7576C7.87977 15.8134 7.1119 15.8133 6.14923 15.8133C5.18661 15.8133 4.41868 15.8134 3.80255 15.7576C3.17724 15.7009 2.6406 15.5817 2.15704 15.3026C1.57834 14.9684 1.09772 14.4877 0.763489 13.909C0.484305 13.4254 0.365123 12.8888 0.308411 12.2635C0.252587 11.6474 0.252747 10.8795 0.252747 9.91681C0.252747 8.95419 0.252603 8.18625 0.308411 7.57013C0.365123 6.94482 0.484305 6.40818 0.763489 5.92462C1.09771 5.3459 1.57833 4.86529 2.15704 4.53107C2.6406 4.25188 3.17724 4.1327 3.80255 4.07599C4.41868 4.02018 5.1866 4.02032 6.14923 4.02032ZM6.14923 5.37775C5.16175 5.37775 4.46628 5.37761 3.9256 5.42657C3.39428 5.47473 3.07853 5.56574 2.83575 5.70587C2.46313 5.92106 2.15348 6.23071 1.93829 6.60333C1.79817 6.84611 1.70715 7.16185 1.659 7.69318C1.61004 8.23385 1.61017 8.92934 1.61017 9.91681C1.61017 10.9043 1.61002 11.5998 1.659 12.1404C1.70715 12.6717 1.79817 12.9875 1.93829 13.2303C2.15349 13.6029 2.46315 13.9126 2.83575 14.1277C3.07853 14.2679 3.39428 14.3589 3.9256 14.407C4.46628 14.456 5.16176 14.4559 6.14923 14.4559C7.13675 14.4559 7.83218 14.456 8.37286 14.407C8.90419 14.3589 9.21993 14.2679 9.46271 14.1277C9.83529 13.9126 10.145 13.6029 10.3602 13.2303C10.5003 12.9875 10.5913 12.6718 10.6395 12.1404C10.6884 11.5998 10.6883 10.9043 10.6883 9.91681C10.6883 8.92935 10.6884 8.23385 10.6395 7.69318C10.5913 7.16185 10.5003 6.84611 10.3602 6.60333C10.145 6.23072 9.8353 5.92107 9.46271 5.70587C9.21993 5.56574 8.90418 5.47473 8.37286 5.42657C7.83218 5.3776 7.13676 5.37775 6.14923 5.37775ZM9.80157 0.367981C10.7637 0.367981 11.5313 0.367886 12.1473 0.423645C12.7725 0.480313 13.3093 0.598765 13.7928 0.877747C14.3716 1.21192 14.852 1.69355 15.1863 2.27228C15.4655 2.75575 15.5857 3.29165 15.6424 3.91681C15.6982 4.53301 15.6971 5.30161 15.6971 6.26447V7.8299C15.6971 8.29265 15.6989 8.58994 15.6649 8.84845C15.4667 10.3525 14.4009 11.5738 12.9832 11.9988V10.5467C13.6973 10.1903 14.2104 9.49662 14.3192 8.67169C14.3387 8.52348 14.3406 8.3358 14.3406 7.8299V6.26447C14.3406 5.27707 14.3398 4.58149 14.2908 4.04083C14.2427 3.50969 14.1526 3.19373 14.0125 2.95099C13.7974 2.5785 13.4875 2.2687 13.1151 2.05353C12.8723 1.91347 12.5563 1.82237 12.0252 1.77423C11.4846 1.72528 10.7888 1.7254 9.80157 1.7254H7.71466C6.75614 1.72559 5.92659 2.27697 5.52325 3.07892H4.07013C4.54215 1.51132 5.99314 0.368192 7.71466 0.367981H9.80157Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">复制</span></span><div class="ds-focus-ring"></div></button><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M15.3695 11.411L15.1234 12.8866C14.8869 14.3042 13.6603 15.3436 12.223 15.3436H3.7767C2.33954 15.3434 1.11276 14.3042 0.876312 12.8866L0.630219 11.411L2.05405 11.1747L2.29916 12.6493C2.41969 13.3713 3.04472 13.9001 3.7767 13.9003H12.223C12.9551 13.9002 13.58 13.3713 13.7005 12.6493L13.9456 11.1747L15.3695 11.411ZM8.72202 8.994C8.77714 8.93934 8.83789 8.88106 8.90268 8.81627L12.4828 5.23424L13.5042 6.25572L9.92221 9.8358C9.63947 10.1185 9.3876 10.3732 9.15854 10.5575C8.91889 10.7503 8.6395 10.9224 8.28647 10.9784C8.09708 11.0083 7.9036 11.0083 7.7142 10.9784C7.36103 10.9224 7.08087 10.7503 6.84116 10.5575C6.61212 10.3732 6.36019 10.1185 6.07748 9.8358L2.49643 6.25572L3.51694 5.23424L7.09702 8.81627C7.16216 8.88142 7.22327 8.94006 7.27866 8.99498V1.3065H8.72202V8.994Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">下载</span></span><div class="ds-focus-ring"></div></button></div></div></div></div></div><pre><span class="token function selector">\documentclass</span><span class="token punctuation">{</span><span class="token keyword">article</span><span class="token punctuation">}</span>
<span class="token function selector">\usepackage</span><span class="token punctuation">{</span><span class="token keyword">amsmath</span><span class="token punctuation">}</span>
<span class="token function selector">\usepackage</span><span class="token punctuation">{</span><span class="token keyword">booktabs</span><span class="token punctuation">}</span>
<span class="token function selector">\usepackage</span><span class="token punctuation">{</span><span class="token keyword">array</span><span class="token punctuation">}</span>

<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">document</span><span class="token punctuation">}</span>

<span class="token function selector">\section</span><span class="token punctuation">{</span><span class="token headline class-name">TTS Model Comparison: Spark-TTS vs Llasa vs CosyVoice2</span><span class="token punctuation">}</span>

<span class="token function selector">\subsection</span><span class="token punctuation">{</span><span class="token headline class-name">Model Overview</span><span class="token punctuation">}</span>

<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Spark-TTS<span class="token punctuation">}</span>: Single-stream autoregressive model based on BiCodec tokenization and Qwen2.5 LLM, supporting zero-shot voice cloning and fine-grained attribute control.
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Llasa<span class="token punctuation">}</span>: Single-stream autoregressive model based on FSQ tokenization and LLaMA LLM, focused on zero-shot TTS with limited control capabilities.
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>CosyVoice2<span class="token punctuation">}</span>: Two-stage hybrid model combining autoregressive language model (semantic token prediction) and flow matching (acoustic feature generation).
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\subsection</span><span class="token punctuation">{</span><span class="token headline class-name">Core Technical Comparison</span><span class="token punctuation">}</span>

<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">table</span><span class="token punctuation">}</span><span class="token punctuation">[</span>h<span class="token punctuation">]</span>
<span class="token function selector">\centering</span>
<span class="token function selector">\caption</span><span class="token punctuation">{</span>Core technical characteristics comparison<span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">tabular</span><span class="token punctuation">}</span><span class="token punctuation">{</span>&gt;<span class="token punctuation">{</span><span class="token function selector">\raggedright</span><span class="token punctuation">}</span>p<span class="token punctuation">{</span>2.5cm<span class="token punctuation">}</span>&gt;<span class="token punctuation">{</span><span class="token function selector">\raggedright</span><span class="token punctuation">}</span>p<span class="token punctuation">{</span>4cm<span class="token punctuation">}</span>&gt;<span class="token punctuation">{</span><span class="token function selector">\raggedright</span><span class="token punctuation">}</span>p<span class="token punctuation">{</span>4cm<span class="token punctuation">}</span>&gt;<span class="token punctuation">{</span><span class="token function selector">\raggedright</span><span class="token punctuation">}</span>p<span class="token punctuation">{</span>4cm<span class="token punctuation">}</span><span class="token punctuation">}</span>
<span class="token function selector">\toprule</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>Technical Feature<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Spark-TTS<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Llasa<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>CosyVoice2<span class="token punctuation">}</span> <span class="token function selector">\\</span>
<span class="token function selector">\midrule</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>Generation Method<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> Single-stage autoregressive (AR) <span class="token punctuation">&amp;</span> Single-stage autoregressive (AR) <span class="token punctuation">&amp;</span> Two-stage hybrid (AR + NAR) <span class="token function selector">\\</span>
<span class="token function selector">\hline</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>Tokenization<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> BiCodec: Single-stream hybrid tokens (semantic + global tokens) <span class="token punctuation">&amp;</span> FSQ-based single-stream tokens (codebook size 65,536) <span class="token punctuation">&amp;</span> Semantic tokens + acoustic features (via flow matching) <span class="token function selector">\\</span>
<span class="token function selector">\hline</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>Language Model<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> Qwen2.5 (decoder-only transformer) <span class="token punctuation">&amp;</span> LLaMA (decoder-only transformer) <span class="token punctuation">&amp;</span> AR LM (semantic tokens) + Flow matching model (acoustic features) <span class="token function selector">\\</span>
<span class="token function selector">\hline</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>Control Capability<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> Coarse and fine-grained control (gender, pitch, speed) via Chain-of-Thought <span class="token punctuation">&amp;</span> Zero-shot TTS only, no explicit attribute control <span class="token punctuation">&amp;</span> Possible partial control (not emphasized in paper) <span class="token function selector">\\</span>
<span class="token function selector">\hline</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>Training Data<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> VoxBox (100k hours) <span class="token punctuation">&amp;</span> 250k hours <span class="token punctuation">&amp;</span> Not specified (based on CosyVoice) <span class="token function selector">\\</span>
<span class="token function selector">\hline</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>Model Parameters<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> 0.5B <span class="token punctuation">&amp;</span> 8B <span class="token punctuation">&amp;</span> Not specified <span class="token function selector">\\</span>
<span class="token function selector">\hline</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>Inference Efficiency<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> Single-stream AR, direct token generation, no multi-stage <span class="token punctuation">&amp;</span> Single-stream AR, direct token generation <span class="token punctuation">&amp;</span> Two-stage, requires semantic tokens then acoustic features, potentially slower <span class="token function selector">\\</span>
<span class="token function selector">\hline</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>Zero-shot TTS Performance<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> High intelligibility (low CER/WER), moderate speaker similarity <span class="token punctuation">&amp;</span> Moderate intelligibility and speaker similarity <span class="token punctuation">&amp;</span> Moderate intelligibility, good speaker similarity <span class="token function selector">\\</span>
<span class="token function selector">\hline</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>Key Innovation<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> BiCodec tokenization, global tokens, CoT attribute control, VoxBox dataset <span class="token punctuation">&amp;</span> FSQ tokenization, single-stream code prediction <span class="token punctuation">&amp;</span> Flow matching for acoustic feature generation, improved naturalness <span class="token function selector">\\</span>
<span class="token function selector">\bottomrule</span>
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">tabular</span><span class="token punctuation">}</span>
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">table</span><span class="token punctuation">}</span>

<span class="token function selector">\subsection</span><span class="token punctuation">{</span><span class="token headline class-name">Detailed Technical Analysis</span><span class="token punctuation">}</span>

<span class="token function selector">\subsubsection</span><span class="token punctuation">{</span><span class="token headline class-name">Generation Method: Autoregressive vs Non-autoregressive</span><span class="token punctuation">}</span>

<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Spark-TTS<span class="token punctuation">}</span>: Uses <span class="token function selector">\textbf</span><span class="token punctuation">{</span>single-stage autoregressive (AR)<span class="token punctuation">}</span> generation. The language model directly predicts speech token sequences (semantic and global tokens), with each token generation dependent on previous tokens.
    
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Llasa<span class="token punctuation">}</span>: Also employs <span class="token function selector">\textbf</span><span class="token punctuation">{</span>single-stage autoregressive (AR)<span class="token punctuation">}</span> generation, using LLaMA model to predict single-stream codes.
    
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>CosyVoice2<span class="token punctuation">}</span>: Employs <span class="token function selector">\textbf</span><span class="token punctuation">{</span>two-stage hybrid approach<span class="token punctuation">}</span>:
    <span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
        <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Stage 1 (AR)<span class="token punctuation">}</span>: Autoregressive language model predicts semantic tokens.
        <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Stage 2 (NAR)<span class="token punctuation">}</span>: Uses flow matching to generate acoustic features, a <span class="token function selector">\textbf</span><span class="token punctuation">{</span>non-autoregressive (NAR)<span class="token punctuation">}</span> method enabling parallel generation.
    <span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\subsubsection</span><span class="token punctuation">{</span><span class="token headline class-name">Tokenization Methods</span><span class="token punctuation">}</span>

<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Spark-TTS<span class="token punctuation">}</span>: Proposes <span class="token function selector">\textbf</span><span class="token punctuation">{</span>BiCodec<span class="token punctuation">}</span>, decomposing speech into:
    <span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
        <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Semantic tokens<span class="token punctuation">}</span>: 50 TPS, capturing linguistic content based on wav2vec 2.0 features.
        <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Global tokens<span class="token punctuation">}</span>: Fixed length (e.g., 32), capturing speaker attributes using FSQ quantization.
    <span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Llasa<span class="token punctuation">}</span>: Uses <span class="token function selector">\textbf</span><span class="token punctuation">{</span>FSQ-based tokenization<span class="token punctuation">}</span>, encoding speech into single-stream codes with codebook size 65,536.
    
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>CosyVoice2<span class="token punctuation">}</span>: Relies on <span class="token function selector">\textbf</span><span class="token punctuation">{</span>semantic tokens<span class="token punctuation">}</span> and <span class="token function selector">\textbf</span><span class="token punctuation">{</span>acoustic features<span class="token punctuation">}</span>, with acoustic features generated via flow matching.
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\subsubsection</span><span class="token punctuation">{</span><span class="token headline class-name">Language Model Architecture</span><span class="token punctuation">}</span>

<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Spark-TTS<span class="token punctuation">}</span>: Based on <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Qwen2.5-0.5B<span class="token punctuation">}</span> (decoder-only transformer), fine-tuned for TTS capabilities.
    
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Llasa<span class="token punctuation">}</span>: Based on <span class="token function selector">\textbf</span><span class="token punctuation">{</span>LLaMA<span class="token punctuation">}</span> (decoder-only transformer) with larger parameters (8B).
    
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>CosyVoice2<span class="token punctuation">}</span>: Uses <span class="token function selector">\textbf</span><span class="token punctuation">{</span>autoregressive LM<span class="token punctuation">}</span> for semantic token prediction combined with <span class="token function selector">\textbf</span><span class="token punctuation">{</span>flow matching model<span class="token punctuation">}</span> for acoustic feature generation.
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\subsubsection</span><span class="token punctuation">{</span><span class="token headline class-name">Control Capabilities</span><span class="token punctuation">}</span>

<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Spark-TTS<span class="token punctuation">}</span>: Implements hierarchical control via <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Chain-of-Thought (CoT)<span class="token punctuation">}</span>:
    <span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
        <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Coarse-grained<span class="token punctuation">}</span>: Gender, pitch level, speed level.
        <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Fine-grained<span class="token punctuation">}</span>: Precise pitch values, speed values.
    <span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Llasa<span class="token punctuation">}</span>: Focused on zero-shot TTS, no explicit attribute control functionality.
    
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>CosyVoice2<span class="token punctuation">}</span>: May support text-prompt based control, but fine-grained attribute control not emphasized.
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\subsection</span><span class="token punctuation">{</span><span class="token headline class-name">Performance Summary</span><span class="token punctuation">}</span>

<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Zero-shot TTS<span class="token punctuation">}</span>:
    <span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
        <span class="token function selector">\item</span> Spark-TTS excels in intelligibility (CER/WER) with moderate speaker similarity.
        <span class="token function selector">\item</span> Spark-TTS with 0.5B parameters surpasses Llasa-8B in performance.
        <span class="token function selector">\item</span> CosyVoice2 competes in quality but with more complex two-stage architecture.
    <span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Reconstruction Quality<span class="token punctuation">}</span>:
    <span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
        <span class="token function selector">\item</span> BiCodec achieves SOTA reconstruction quality at low bitrates (&lt;1 kbps).
        <span class="token function selector">\item</span> Both Llasa and CosyVoice2 employ efficient tokenization methods.
    <span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\subsection</span><span class="token punctuation">{</span><span class="token headline class-name">Conclusion</span><span class="token punctuation">}</span>

The three models represent different directions in TTS research:
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Spark-TTS<span class="token punctuation">}</span> emphasizes control and efficiency through BiCodec tokenization and CoT control.
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Llasa<span class="token punctuation">}</span> focuses on scaling model and data size.
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>CosyVoice2<span class="token punctuation">}</span> prioritizes acoustic quality through flow matching.
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

Model selection depends on specific application requirements, such as need for attribute control or real-time generation capabilities.

<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">document</span><span class="token punctuation">}</span></pre><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _33882ae"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _28d7e84"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg></div>

---

### 用户

根据提供的 Spark-TTS 论文内容，我将对三个主要的 TTS 模型进行详细比较：**Spark-TTS**、**Llasa** 和 **CosyVoice2**。这些模型在零样本文本到语音（TTS）任务中表现出色，但它们在核心技术、架构和生成方式上存在显著差异。以下将重点比较它们的核心技术，包括自回归（AR）与非自回归（NAR）方法、令牌化策略、语言模型架构等。

### 模型概述
- **Spark-TTS**：基于 BiCodec 令牌化和 Qwen2.5 LLM 的单流自回归模型，支持零样本语音克隆和细粒度属性控制。
- **Llasa**：基于 FSQ 令牌化和 LLaMA LLM 的单流自回归模型，专注于零样本 TTS，但控制能力较弱。
- **CosyVoice2**：两阶段模型，结合自回归语言模型（语义令牌预测）和流匹配（声学特征生成），属于混合 AR-NAR 方法。

### 核心技术比较
下表详细列出了三个模型的核心技术特点：

| 技术特征         | Spark-TTS                                                                 | Llasa                                                                 | CosyVoice2                                                                 |
|------------------|---------------------------------------------------------------------------|-----------------------------------------------------------------------|----------------------------------------------------------------------------|
| **生成方式**       | 一阶段自回归（AR）                                                         | 一阶段自回归（AR）                                                     | 两阶段混合（AR + NAR）                                                      |
| **令牌化方法**     | BiCodec：单流混合令牌（语义令牌 + 全局令牌）                               | FSQ-based 单流令牌（代码本大小 65,536）                               | 语义令牌 + 声学特征（通过流匹配生成）                                       |
| **语言模型**       | Qwen2.5（decoder-only transformer）                                       | LLaMA（decoder-only transformer）                                     | 自回归 LM（语义令牌） + 流匹配模型（声学特征）                              |
| **控制能力**       | 支持粗粒度和细粒度控制（性别、音高、语速） via Chain-of-Thought (CoT)     | 仅支持零样本 TTS，无显式属性控制                                      | 可能支持部分控制（但论文未强调）                                           |
| **训练数据**       | VoxBox（100k 小时）                                                       | 250k 小时                                                             | 未详细说明（基于 CosyVoice）                                               |
| **模型参数**       | 0.5B                                                                      | 8B                                                                    | 未详细说明                                                                 |
| **推理效率**       | 单流 AR，直接生成令牌，无需多阶段                                         | 单流 AR，直接生成令牌                                                 | 两阶段，需先生成语义令牌再生成声学特征，可能较慢                           |
| **零样本 TTS 性能** | 高智能度（CER/WER 低），但说话人相似性略低于多阶段方法                   | 中等智能度和说话人相似性                                             | 中等智能度，说话人相似性较好                                               |
| **关键创新**       | BiCodec 令牌化、全局令牌、CoT 属性控制、VoxBox 数据集                     | FSQ 令牌化、单流代码预测                                              | 流匹配用于声学特征生成，提升自然度                                         |

### 详细技术分析
#### 1. **生成方式：自回归 vs. 非自回归**
- **Spark-TTS**：使用**一阶段自回归（AR）** 生成。语言模型直接预测语音令牌序列（语义令牌和全局令牌），每个令牌的生成依赖于之前生成的令牌。这种方式简单且与文本 LLM 一致，但可能引入随机性，影响说话人相似性。
- **Llasa**：同样采用**一阶段自回归（AR）** 生成，使用 LLaMA 模型预测单流代码。AR 方法允许高质量生成，但计算开销较大。
- **CosyVoice2**：采用**两阶段混合方法**：
  - **阶段1（AR）**：自回归语言模型预测语义令牌。
  - **阶段2（NAR）**：使用流匹配（flow matching）生成声学特征，这是一种**非自回归（NAR）** 方法，可以并行生成，提高效率。流匹配基于扩散模型原理，生成过程稳定。

#### 2. **令牌化方法**
- **Spark-TTS**：提出 **BiCodec**，将语音分解为：
  - **语义令牌**：50 TPS，捕获语言内容，基于 wav2vec 2.0 特征。
  - **全局令牌**：固定长度（如 32），捕获说话人属性，使用 FSQ 量化。
  - 这种解耦允许细粒度控制，同时保持低比特率（0.65 kbps）。
- **Llasa**：使用 **FSQ-based 令牌化**，将语音编码为单流代码，代码本大小 65,536。FSQ 避免了 VQ 的训练崩溃问题，但缺乏显式的属性分离。
- **CosyVoice2**：依赖于**语义令牌**和**声学特征**。语义令牌通过自回归 LM 预测，声学特征通过流匹配生成，可能使用类似 MEL 谱的特征。

#### 3. **语言模型架构**
- **Spark-TTS**：基于 **Qwen2.5-0.5B**（decoder-only transformer），通过微调集成 TTS 能力。支持多语言文本令牌化和属性令牌化。
- **Llasa**：基于 **LLaMA**（decoder-only transformer），参数更大（8B），但训练数据更多（250k 小时）。
- **CosyVoice2**：使用**自回归 LM** 用于语义令牌预测，并结合**流匹配模型**用于声学特征生成。流匹配是一种生成模型，类似于扩散模型，但具有更稳定的训练。

#### 4. **控制能力**
- **Spark-TTS**：通过 **Chain-of-Thought (CoT)** 实现分层控制：
  - **粗粒度**：性别、音高水平、语速水平。
  - **细粒度**：精确音高值、语速值。
  - 无需参考音频即可生成新语音。
- **Llasa**：专注于零样本 TTS，无显式属性控制功能。
- **CosyVoice2**：可能支持基于文本提示的控制，但论文未强调细粒度属性控制。

#### 5. **性能对比**
- **零样本 TTS**：
  - Spark-TTS 在智能度（CER/WER）上表现优异，但说话人相似性略低于多阶段方法（如 Seed-TTS）。
  - Llasa 在相似参数下性能较弱，Spark-TTS 以 0.5B 参数超越 Llasa-8B。
  - CosyVoice2 在质量上竞争，但两阶段架构可能增加复杂性。
- **重建质量**：
  - BiCodec 在低比特率（<1 kbps）下达到 SOTA 重建质量。
  - Llasa 和 CosyVoice2 的令牌化方法也高效，但 BiCodec 的混合令牌提供更好控制。

### 总结
- **Spark-TTS** 的核心优势在于其 **BiCodec 令牌化** 和 **CoT 控制**，实现了高效且可控的 TTS，同时保持与文本 LLM 的架构一致性。
- **Llasa** 专注于缩放模型和数据，但缺乏控制功能。
- **CosyVoice2** 通过 **流匹配** 提升声学质量，但两阶段架构可能限制效率和灵活性。

这些模型代表了 TTS 领域的不同方向：Spark-TTS 强调控制和效率，Llasa 强调缩放，CosyVoice2 强调声学质量。选择取决于具体应用需求，如是否需要属性控制或实时生成。用原来的文本写

---

### DeepSeek AI

<p>思考：</p><blockquote><p class="ds-markdown-paragraph"><span>我们根据用户提供的详细比较文本，将其转换为LaTeX格式。注意，用户要求只使用最基本的package，格式简洁。</span><br><span>我们将按照用户提供的结构，包括模型概述、核心技术比较表格、详细技术分析、性能对比和总结。</span><br><span>由于用户提供的文本是中文，我们将在LaTeX文档中使用中文。需要确保使用支持中文的编译器（如XeLaTeX）和字体设置。</span><br><span>但是，用户要求只使用最基本的package，所以我们使用</span>`ctex`<span>包来支持中文，同时使用</span>`amsmath`<span>、</span>`booktabs`<span>和</span>`array`<span>来排版表格和数学公式。</span><br><span>注意：如果用户不需要中文，可以移除</span>`ctex`<span>包，但这里根据内容判断需要中文。</span></p><p class="ds-markdown-paragraph"><span>我们将按照以下结构编写：</span></p><ol start="1"><li><p class="ds-markdown-paragraph"><span>文档类设置和包引入</span></p></li><li><p class="ds-markdown-paragraph"><span>标题和作者（如果有）</span></p></li><li><p class="ds-markdown-paragraph"><span>章节：模型概述（使用itemize列表）</span></p></li><li><p class="ds-markdown-paragraph"><span>章节：核心技术比较（使用表格，注意表格可能较长，可能需要调整）</span></p></li><li><p class="ds-markdown-paragraph"><span>章节：详细技术分析（分小节，使用itemize列表）</span></p></li><li><p class="ds-markdown-paragraph"><span>章节：性能对比</span></p></li><li><p class="ds-markdown-paragraph"><span>章节：总结</span></p></li></ol><p class="ds-markdown-paragraph"><span>由于用户提供的表格内容较多，我们可能需要调整表格的列宽，使用</span>`p{宽度}`<span>来指定列宽，并确保表格不会超出页面。</span></p><p class="ds-markdown-paragraph"><span>注意：用户提供的表格中，有些单元格内容较多，我们可能需要调整表格的列宽，使其适应页面。这里我们使用</span>`p{2.5cm}`<span>和</span>`p{4cm}`<span>等来设置。</span></p><p class="ds-markdown-paragraph"><span>我们开始编写LaTeX代码。</span></p></blockquote><br/><div class="md-code-block md-code-block-light"><div class="md-code-block-banner-wrap"><div class="md-code-block-banner md-code-block-banner-lite"><div class="_121d384"><div class="d2a24f03"><span class="d813de27">latex</span></div><div class="d2a24f03 _246a029"><div class="efa13877"><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon" style="margin-right: 4px;"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.14923 4.02032C7.11191 4.02032 7.87977 4.02017 8.49591 4.07599C9.12122 4.1327 9.65786 4.25188 10.1414 4.53107C10.7201 4.8653 11.2008 5.34591 11.535 5.92462C11.8142 6.40818 11.9333 6.94482 11.9901 7.57013C12.0459 8.18625 12.0457 8.9542 12.0457 9.91681C12.0457 10.8795 12.0459 11.6474 11.9901 12.2635C11.9333 12.8888 11.8142 13.4254 11.535 13.909C11.2008 14.4877 10.7201 14.9683 10.1414 15.3026C9.65786 15.5817 9.12122 15.7009 8.49591 15.7576C7.87977 15.8134 7.1119 15.8133 6.14923 15.8133C5.18661 15.8133 4.41868 15.8134 3.80255 15.7576C3.17724 15.7009 2.6406 15.5817 2.15704 15.3026C1.57834 14.9684 1.09772 14.4877 0.763489 13.909C0.484305 13.4254 0.365123 12.8888 0.308411 12.2635C0.252587 11.6474 0.252747 10.8795 0.252747 9.91681C0.252747 8.95419 0.252603 8.18625 0.308411 7.57013C0.365123 6.94482 0.484305 6.40818 0.763489 5.92462C1.09771 5.3459 1.57833 4.86529 2.15704 4.53107C2.6406 4.25188 3.17724 4.1327 3.80255 4.07599C4.41868 4.02018 5.1866 4.02032 6.14923 4.02032ZM6.14923 5.37775C5.16175 5.37775 4.46628 5.37761 3.9256 5.42657C3.39428 5.47473 3.07853 5.56574 2.83575 5.70587C2.46313 5.92106 2.15348 6.23071 1.93829 6.60333C1.79817 6.84611 1.70715 7.16185 1.659 7.69318C1.61004 8.23385 1.61017 8.92934 1.61017 9.91681C1.61017 10.9043 1.61002 11.5998 1.659 12.1404C1.70715 12.6717 1.79817 12.9875 1.93829 13.2303C2.15349 13.6029 2.46315 13.9126 2.83575 14.1277C3.07853 14.2679 3.39428 14.3589 3.9256 14.407C4.46628 14.456 5.16176 14.4559 6.14923 14.4559C7.13675 14.4559 7.83218 14.456 8.37286 14.407C8.90419 14.3589 9.21993 14.2679 9.46271 14.1277C9.83529 13.9126 10.145 13.6029 10.3602 13.2303C10.5003 12.9875 10.5913 12.6718 10.6395 12.1404C10.6884 11.5998 10.6883 10.9043 10.6883 9.91681C10.6883 8.92935 10.6884 8.23385 10.6395 7.69318C10.5913 7.16185 10.5003 6.84611 10.3602 6.60333C10.145 6.23072 9.8353 5.92107 9.46271 5.70587C9.21993 5.56574 8.90418 5.47473 8.37286 5.42657C7.83218 5.3776 7.13676 5.37775 6.14923 5.37775ZM9.80157 0.367981C10.7637 0.367981 11.5313 0.367886 12.1473 0.423645C12.7725 0.480313 13.3093 0.598765 13.7928 0.877747C14.3716 1.21192 14.852 1.69355 15.1863 2.27228C15.4655 2.75575 15.5857 3.29165 15.6424 3.91681C15.6982 4.53301 15.6971 5.30161 15.6971 6.26447V7.8299C15.6971 8.29265 15.6989 8.58994 15.6649 8.84845C15.4667 10.3525 14.4009 11.5738 12.9832 11.9988V10.5467C13.6973 10.1903 14.2104 9.49662 14.3192 8.67169C14.3387 8.52348 14.3406 8.3358 14.3406 7.8299V6.26447C14.3406 5.27707 14.3398 4.58149 14.2908 4.04083C14.2427 3.50969 14.1526 3.19373 14.0125 2.95099C13.7974 2.5785 13.4875 2.2687 13.1151 2.05353C12.8723 1.91347 12.5563 1.82237 12.0252 1.77423C11.4846 1.72528 10.7888 1.7254 9.80157 1.7254H7.71466C6.75614 1.72559 5.92659 2.27697 5.52325 3.07892H4.07013C4.54215 1.51132 5.99314 0.368192 7.71466 0.367981H9.80157Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">复制</span></span><div class="ds-focus-ring"></div></button><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M15.3695 11.411L15.1234 12.8866C14.8869 14.3042 13.6603 15.3436 12.223 15.3436H3.7767C2.33954 15.3434 1.11276 14.3042 0.876312 12.8866L0.630219 11.411L2.05405 11.1747L2.29916 12.6493C2.41969 13.3713 3.04472 13.9001 3.7767 13.9003H12.223C12.9551 13.9002 13.58 13.3713 13.7005 12.6493L13.9456 11.1747L15.3695 11.411ZM8.72202 8.994C8.77714 8.93934 8.83789 8.88106 8.90268 8.81627L12.4828 5.23424L13.5042 6.25572L9.92221 9.8358C9.63947 10.1185 9.3876 10.3732 9.15854 10.5575C8.91889 10.7503 8.6395 10.9224 8.28647 10.9784C8.09708 11.0083 7.9036 11.0083 7.7142 10.9784C7.36103 10.9224 7.08087 10.7503 6.84116 10.5575C6.61212 10.3732 6.36019 10.1185 6.07748 9.8358L2.49643 6.25572L3.51694 5.23424L7.09702 8.81627C7.16216 8.88142 7.22327 8.94006 7.27866 8.99498V1.3065H8.72202V8.994Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">下载</span></span><div class="ds-focus-ring"></div></button></div></div></div></div></div><pre><span class="token function selector">\documentclass</span><span class="token punctuation">{</span><span class="token keyword">article</span><span class="token punctuation">}</span>
<span class="token function selector">\usepackage</span><span class="token punctuation">{</span><span class="token keyword">amsmath</span><span class="token punctuation">}</span>
<span class="token function selector">\usepackage</span><span class="token punctuation">{</span><span class="token keyword">booktabs</span><span class="token punctuation">}</span>
<span class="token function selector">\usepackage</span><span class="token punctuation">{</span><span class="token keyword">array</span><span class="token punctuation">}</span>

<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">document</span><span class="token punctuation">}</span>

<span class="token function selector">\section</span><span class="token punctuation">{</span><span class="token headline class-name">TTS模型对比：Spark-TTS vs Llasa vs CosyVoice2</span><span class="token punctuation">}</span>

根据提供的 Spark-TTS 论文内容，我将对三个主要的 TTS 模型进行详细比较：<span class="token function selector">\textbf</span><span class="token punctuation">{</span>Spark-TTS<span class="token punctuation">}</span>、<span class="token function selector">\textbf</span><span class="token punctuation">{</span>Llasa<span class="token punctuation">}</span> 和 <span class="token function selector">\textbf</span><span class="token punctuation">{</span>CosyVoice2<span class="token punctuation">}</span>。这些模型在零样本文本到语音（TTS）任务中表现出色，但它们在核心技术、架构和生成方式上存在显著差异。以下将重点比较它们的核心技术，包括自回归（AR）与非自回归（NAR）方法、令牌化策略、语言模型架构等。

<span class="token function selector">\subsection</span><span class="token punctuation">{</span><span class="token headline class-name">模型概述</span><span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Spark-TTS<span class="token punctuation">}</span>：基于 BiCodec 令牌化和 Qwen2.5 LLM 的单流自回归模型，支持零样本语音克隆和细粒度属性控制。
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Llasa<span class="token punctuation">}</span>：基于 FSQ 令牌化和 LLaMA LLM 的单流自回归模型，专注于零样本 TTS，但控制能力较弱。
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>CosyVoice2<span class="token punctuation">}</span>：两阶段模型，结合自回归语言模型（语义令牌预测）和流匹配（声学特征生成），属于混合 AR-NAR 方法。
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\subsection</span><span class="token punctuation">{</span><span class="token headline class-name">核心技术比较</span><span class="token punctuation">}</span>
下表详细列出了三个模型的核心技术特点：

<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">table</span><span class="token punctuation">}</span><span class="token punctuation">[</span>h<span class="token punctuation">]</span>
<span class="token function selector">\centering</span>
<span class="token function selector">\caption</span><span class="token punctuation">{</span>核心技术比较<span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">tabular</span><span class="token punctuation">}</span><span class="token punctuation">{</span>&gt;<span class="token punctuation">{</span><span class="token function selector">\raggedright</span><span class="token punctuation">}</span>p<span class="token punctuation">{</span>2.5cm<span class="token punctuation">}</span>&gt;<span class="token punctuation">{</span><span class="token function selector">\raggedright</span><span class="token punctuation">}</span>p<span class="token punctuation">{</span>4cm<span class="token punctuation">}</span>&gt;<span class="token punctuation">{</span><span class="token function selector">\raggedright</span><span class="token punctuation">}</span>p<span class="token punctuation">{</span>4cm<span class="token punctuation">}</span>&gt;<span class="token punctuation">{</span><span class="token function selector">\raggedright</span><span class="token punctuation">}</span>p<span class="token punctuation">{</span>4cm<span class="token punctuation">}</span><span class="token punctuation">}</span>
<span class="token function selector">\toprule</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>技术特征<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Spark-TTS<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Llasa<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>CosyVoice2<span class="token punctuation">}</span> <span class="token function selector">\\</span>
<span class="token function selector">\midrule</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>生成方式<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> 一阶段自回归（AR） <span class="token punctuation">&amp;</span> 一阶段自回归（AR） <span class="token punctuation">&amp;</span> 两阶段混合（AR + NAR） <span class="token function selector">\\</span>
<span class="token function selector">\hline</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>令牌化方法<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> BiCodec：单流混合令牌（语义令牌 + 全局令牌） <span class="token punctuation">&amp;</span> FSQ-based 单流令牌（代码本大小 65,536） <span class="token punctuation">&amp;</span> 语义令牌 + 声学特征（通过流匹配生成） <span class="token function selector">\\</span>
<span class="token function selector">\hline</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>语言模型<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> Qwen2.5（decoder-only transformer） <span class="token punctuation">&amp;</span> LLaMA（decoder-only transformer） <span class="token punctuation">&amp;</span> 自回归 LM（语义令牌） + 流匹配模型（声学特征） <span class="token function selector">\\</span>
<span class="token function selector">\hline</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>控制能力<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> 支持粗粒度和细粒度控制（性别、音高、语速） via Chain-of-Thought (CoT) <span class="token punctuation">&amp;</span> 仅支持零样本 TTS，无显式属性控制 <span class="token punctuation">&amp;</span> 可能支持部分控制（但论文未强调） <span class="token function selector">\\</span>
<span class="token function selector">\hline</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>训练数据<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> VoxBox（100k 小时） <span class="token punctuation">&amp;</span> 250k 小时 <span class="token punctuation">&amp;</span> 未详细说明（基于 CosyVoice） <span class="token function selector">\\</span>
<span class="token function selector">\hline</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>模型参数<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> 0.5B <span class="token punctuation">&amp;</span> 8B <span class="token punctuation">&amp;</span> 未详细说明 <span class="token function selector">\\</span>
<span class="token function selector">\hline</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>推理效率<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> 单流 AR，直接生成令牌，无需多阶段 <span class="token punctuation">&amp;</span> 单流 AR，直接生成令牌 <span class="token punctuation">&amp;</span> 两阶段，需先生成语义令牌再生成声学特征，可能较慢 <span class="token function selector">\\</span>
<span class="token function selector">\hline</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>零样本 TTS 性能<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> 高智能度（CER/WER 低），但说话人相似性略低于多阶段方法 <span class="token punctuation">&amp;</span> 中等智能度和说话人相似性 <span class="token punctuation">&amp;</span> 中等智能度，说话人相似性较好 <span class="token function selector">\\</span>
<span class="token function selector">\hline</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>关键创新<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> BiCodec 令牌化、全局令牌、CoT 属性控制、VoxBox 数据集 <span class="token punctuation">&amp;</span> FSQ 令牌化、单流代码预测 <span class="token punctuation">&amp;</span> 流匹配用于声学特征生成，提升自然度 <span class="token function selector">\\</span>
<span class="token function selector">\bottomrule</span>
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">tabular</span><span class="token punctuation">}</span>
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">table</span><span class="token punctuation">}</span>

<span class="token function selector">\subsection</span><span class="token punctuation">{</span><span class="token headline class-name">详细技术分析</span><span class="token punctuation">}</span>

<span class="token function selector">\subsubsection</span><span class="token punctuation">{</span><span class="token headline class-name">生成方式：自回归 vs. 非自回归</span><span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Spark-TTS<span class="token punctuation">}</span>：使用<span class="token function selector">\textbf</span><span class="token punctuation">{</span>一阶段自回归（AR）<span class="token punctuation">}</span>生成。语言模型直接预测语音令牌序列（语义令牌和全局令牌），每个令牌的生成依赖于之前生成的令牌。这种方式简单且与文本 LLM 一致，但可能引入随机性，影响说话人相似性。
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Llasa<span class="token punctuation">}</span>：同样采用<span class="token function selector">\textbf</span><span class="token punctuation">{</span>一阶段自回归（AR）<span class="token punctuation">}</span>生成，使用 LLaMA 模型预测单流代码。AR 方法允许高质量生成，但计算开销较大。
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>CosyVoice2<span class="token punctuation">}</span>：采用<span class="token function selector">\textbf</span><span class="token punctuation">{</span>两阶段混合方法<span class="token punctuation">}</span>：
    <span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
        <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>阶段1（AR）<span class="token punctuation">}</span>：自回归语言模型预测语义令牌。
        <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>阶段2（NAR）<span class="token punctuation">}</span>：使用流匹配（flow matching）生成声学特征，这是一种<span class="token function selector">\textbf</span><span class="token punctuation">{</span>非自回归（NAR）<span class="token punctuation">}</span>方法，可以并行生成，提高效率。流匹配基于扩散模型原理，生成过程稳定。
    <span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\subsubsection</span><span class="token punctuation">{</span><span class="token headline class-name">令牌化方法</span><span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Spark-TTS<span class="token punctuation">}</span>：提出 <span class="token function selector">\textbf</span><span class="token punctuation">{</span>BiCodec<span class="token punctuation">}</span>，将语音分解为：
    <span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
        <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>语义令牌<span class="token punctuation">}</span>：50 TPS，捕获语言内容，基于 wav2vec 2.0 特征。
        <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>全局令牌<span class="token punctuation">}</span>：固定长度（如 32），捕获说话人属性，使用 FSQ 量化。
    <span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    这种解耦允许细粒度控制，同时保持低比特率（0.65 kbps）。
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Llasa<span class="token punctuation">}</span>：使用 <span class="token function selector">\textbf</span><span class="token punctuation">{</span>FSQ-based 令牌化<span class="token punctuation">}</span>，将语音编码为单流代码，代码本大小 65,536。FSQ 避免了 VQ 的训练崩溃问题，但缺乏显式的属性分离。
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>CosyVoice2<span class="token punctuation">}</span>：依赖于<span class="token function selector">\textbf</span><span class="token punctuation">{</span>语义令牌<span class="token punctuation">}</span>和<span class="token function selector">\textbf</span><span class="token punctuation">{</span>声学特征<span class="token punctuation">}</span>。语义令牌通过自回归 LM 预测，声学特征通过流匹配生成，可能使用类似 MEL 谱的特征。
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\subsubsection</span><span class="token punctuation">{</span><span class="token headline class-name">语言模型架构</span><span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Spark-TTS<span class="token punctuation">}</span>：基于 <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Qwen2.5-0.5B<span class="token punctuation">}</span>（decoder-only transformer），通过微调集成 TTS 能力。支持多语言文本令牌化和属性令牌化。
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Llasa<span class="token punctuation">}</span>：基于 <span class="token function selector">\textbf</span><span class="token punctuation">{</span>LLaMA<span class="token punctuation">}</span>（decoder-only transformer），参数更大（8B），但训练数据更多（250k 小时）。
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>CosyVoice2<span class="token punctuation">}</span>：使用<span class="token function selector">\textbf</span><span class="token punctuation">{</span>自回归 LM<span class="token punctuation">}</span>用于语义令牌预测，并结合<span class="token function selector">\textbf</span><span class="token punctuation">{</span>流匹配模型<span class="token punctuation">}</span>用于声学特征生成。流匹配是一种生成模型，类似于扩散模型，但具有更稳定的训练。
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\subsubsection</span><span class="token punctuation">{</span><span class="token headline class-name">控制能力</span><span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Spark-TTS<span class="token punctuation">}</span>：通过 <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Chain-of-Thought (CoT)<span class="token punctuation">}</span>实现分层控制：
    <span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
        <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>粗粒度<span class="token punctuation">}</span>：性别、音高水平、语速水平。
        <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>细粒度<span class="token punctuation">}</span>：精确音高值、语速值。
    <span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    无需参考音频即可生成新语音。
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Llasa<span class="token punctuation">}</span>：专注于零样本 TTS，无显式属性控制功能。
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>CosyVoice2<span class="token punctuation">}</span>：可能支持基于文本提示的控制，但论文未强调细粒度属性控制。
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\subsubsection</span><span class="token punctuation">{</span><span class="token headline class-name">性能对比</span><span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>零样本 TTS<span class="token punctuation">}</span>：
    <span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
        <span class="token function selector">\item</span> Spark-TTS 在智能度（CER/WER）上表现优异，但说话人相似性略低于多阶段方法（如 Seed-TTS）。
        <span class="token function selector">\item</span> Llasa 在相似参数下性能较弱，Spark-TTS 以 0.5B 参数超越 Llasa-8B。
        <span class="token function selector">\item</span> CosyVoice2 在质量上竞争，但两阶段架构可能增加复杂性。
    <span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>重建质量<span class="token punctuation">}</span>：
    <span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
        <span class="token function selector">\item</span> BiCodec 在低比特率（&lt;1 kbps）下达到 SOTA 重建质量。
        <span class="token function selector">\item</span> Llasa 和 CosyVoice2 的令牌化方法也高效，但 BiCodec 的混合令牌提供更好控制。
    <span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\subsection</span><span class="token punctuation">{</span><span class="token headline class-name">总结</span><span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Spark-TTS<span class="token punctuation">}</span>的核心优势在于其 <span class="token function selector">\textbf</span><span class="token punctuation">{</span>BiCodec 令牌化<span class="token punctuation">}</span>和 <span class="token function selector">\textbf</span><span class="token punctuation">{</span>CoT 控制<span class="token punctuation">}</span>，实现了高效且可控的 TTS，同时保持与文本 LLM 的架构一致性。
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Llasa<span class="token punctuation">}</span>专注于缩放模型和数据，但缺乏控制功能。
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>CosyVoice2<span class="token punctuation">}</span>通过 <span class="token function selector">\textbf</span><span class="token punctuation">{</span>流匹配<span class="token punctuation">}</span>提升声学质量，但两阶段架构可能限制效率和灵活性。
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

这些模型代表了 TTS 领域的不同方向：Spark-TTS 强调控制和效率，Llasa 强调缩放，CosyVoice2 强调声学质量。选择取决于具体应用需求，如是否需要属性控制或实时生成。

<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">document</span><span class="token punctuation">}</span></pre><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _33882ae"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _28d7e84"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg></div>

---

### 用户

详细比较三者的语言模型架构

---

### DeepSeek AI

<p>思考：</p><blockquote><p class="ds-markdown-paragraph"><span>我们已知三个模型的语言模型架构如下：</span></p><ul><li><p class="ds-markdown-paragraph"><span>Spark-TTS: 使用Qwen2.5-0.5B（decoder-only transformer）作为基础，通过微调集成TTS能力。</span></p></li><li><p class="ds-markdown-paragraph"><span>Llasa: 使用LLaMA（decoder-only transformer）作为基础，参数更大（8B）。</span></p></li><li><p class="ds-markdown-paragraph"><span>CosyVoice2: 使用自回归语言模型（用于语义令牌预测）和流匹配模型（用于声学特征生成）的两阶段架构。</span></p></li></ul><p class="ds-markdown-paragraph"><span>下面我们将从多个维度对这三者的语言模型架构进行详细比较。</span></p></blockquote><br/><div class="md-code-block md-code-block-light"><div class="md-code-block-banner-wrap"><div class="md-code-block-banner md-code-block-banner-lite"><div class="_121d384"><div class="d2a24f03"><span class="d813de27">latex</span></div><div class="d2a24f03 _246a029"><div class="efa13877"><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon" style="margin-right: 4px;"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.14923 4.02032C7.11191 4.02032 7.87977 4.02017 8.49591 4.07599C9.12122 4.1327 9.65786 4.25188 10.1414 4.53107C10.7201 4.8653 11.2008 5.34591 11.535 5.92462C11.8142 6.40818 11.9333 6.94482 11.9901 7.57013C12.0459 8.18625 12.0457 8.9542 12.0457 9.91681C12.0457 10.8795 12.0459 11.6474 11.9901 12.2635C11.9333 12.8888 11.8142 13.4254 11.535 13.909C11.2008 14.4877 10.7201 14.9683 10.1414 15.3026C9.65786 15.5817 9.12122 15.7009 8.49591 15.7576C7.87977 15.8134 7.1119 15.8133 6.14923 15.8133C5.18661 15.8133 4.41868 15.8134 3.80255 15.7576C3.17724 15.7009 2.6406 15.5817 2.15704 15.3026C1.57834 14.9684 1.09772 14.4877 0.763489 13.909C0.484305 13.4254 0.365123 12.8888 0.308411 12.2635C0.252587 11.6474 0.252747 10.8795 0.252747 9.91681C0.252747 8.95419 0.252603 8.18625 0.308411 7.57013C0.365123 6.94482 0.484305 6.40818 0.763489 5.92462C1.09771 5.3459 1.57833 4.86529 2.15704 4.53107C2.6406 4.25188 3.17724 4.1327 3.80255 4.07599C4.41868 4.02018 5.1866 4.02032 6.14923 4.02032ZM6.14923 5.37775C5.16175 5.37775 4.46628 5.37761 3.9256 5.42657C3.39428 5.47473 3.07853 5.56574 2.83575 5.70587C2.46313 5.92106 2.15348 6.23071 1.93829 6.60333C1.79817 6.84611 1.70715 7.16185 1.659 7.69318C1.61004 8.23385 1.61017 8.92934 1.61017 9.91681C1.61017 10.9043 1.61002 11.5998 1.659 12.1404C1.70715 12.6717 1.79817 12.9875 1.93829 13.2303C2.15349 13.6029 2.46315 13.9126 2.83575 14.1277C3.07853 14.2679 3.39428 14.3589 3.9256 14.407C4.46628 14.456 5.16176 14.4559 6.14923 14.4559C7.13675 14.4559 7.83218 14.456 8.37286 14.407C8.90419 14.3589 9.21993 14.2679 9.46271 14.1277C9.83529 13.9126 10.145 13.6029 10.3602 13.2303C10.5003 12.9875 10.5913 12.6718 10.6395 12.1404C10.6884 11.5998 10.6883 10.9043 10.6883 9.91681C10.6883 8.92935 10.6884 8.23385 10.6395 7.69318C10.5913 7.16185 10.5003 6.84611 10.3602 6.60333C10.145 6.23072 9.8353 5.92107 9.46271 5.70587C9.21993 5.56574 8.90418 5.47473 8.37286 5.42657C7.83218 5.3776 7.13676 5.37775 6.14923 5.37775ZM9.80157 0.367981C10.7637 0.367981 11.5313 0.367886 12.1473 0.423645C12.7725 0.480313 13.3093 0.598765 13.7928 0.877747C14.3716 1.21192 14.852 1.69355 15.1863 2.27228C15.4655 2.75575 15.5857 3.29165 15.6424 3.91681C15.6982 4.53301 15.6971 5.30161 15.6971 6.26447V7.8299C15.6971 8.29265 15.6989 8.58994 15.6649 8.84845C15.4667 10.3525 14.4009 11.5738 12.9832 11.9988V10.5467C13.6973 10.1903 14.2104 9.49662 14.3192 8.67169C14.3387 8.52348 14.3406 8.3358 14.3406 7.8299V6.26447C14.3406 5.27707 14.3398 4.58149 14.2908 4.04083C14.2427 3.50969 14.1526 3.19373 14.0125 2.95099C13.7974 2.5785 13.4875 2.2687 13.1151 2.05353C12.8723 1.91347 12.5563 1.82237 12.0252 1.77423C11.4846 1.72528 10.7888 1.7254 9.80157 1.7254H7.71466C6.75614 1.72559 5.92659 2.27697 5.52325 3.07892H4.07013C4.54215 1.51132 5.99314 0.368192 7.71466 0.367981H9.80157Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">复制</span></span><div class="ds-focus-ring"></div></button><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M15.3695 11.411L15.1234 12.8866C14.8869 14.3042 13.6603 15.3436 12.223 15.3436H3.7767C2.33954 15.3434 1.11276 14.3042 0.876312 12.8866L0.630219 11.411L2.05405 11.1747L2.29916 12.6493C2.41969 13.3713 3.04472 13.9001 3.7767 13.9003H12.223C12.9551 13.9002 13.58 13.3713 13.7005 12.6493L13.9456 11.1747L15.3695 11.411ZM8.72202 8.994C8.77714 8.93934 8.83789 8.88106 8.90268 8.81627L12.4828 5.23424L13.5042 6.25572L9.92221 9.8358C9.63947 10.1185 9.3876 10.3732 9.15854 10.5575C8.91889 10.7503 8.6395 10.9224 8.28647 10.9784C8.09708 11.0083 7.9036 11.0083 7.7142 10.9784C7.36103 10.9224 7.08087 10.7503 6.84116 10.5575C6.61212 10.3732 6.36019 10.1185 6.07748 9.8358L2.49643 6.25572L3.51694 5.23424L7.09702 8.81627C7.16216 8.88142 7.22327 8.94006 7.27866 8.99498V1.3065H8.72202V8.994Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">下载</span></span><div class="ds-focus-ring"></div></button></div></div></div></div></div><pre><span class="token function selector">\documentclass</span><span class="token punctuation">{</span><span class="token keyword">article</span><span class="token punctuation">}</span>
<span class="token function selector">\usepackage</span><span class="token punctuation">{</span><span class="token keyword">amsmath</span><span class="token punctuation">}</span>
<span class="token function selector">\usepackage</span><span class="token punctuation">{</span><span class="token keyword">booktabs</span><span class="token punctuation">}</span>
<span class="token function selector">\usepackage</span><span class="token punctuation">{</span><span class="token keyword">array</span><span class="token punctuation">}</span>

<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">document</span><span class="token punctuation">}</span>

<span class="token function selector">\section</span><span class="token punctuation">{</span><span class="token headline class-name">TTS模型语言模型架构详细比较</span><span class="token punctuation">}</span>

<span class="token function selector">\subsection</span><span class="token punctuation">{</span><span class="token headline class-name">语言模型架构概述</span><span class="token punctuation">}</span>

基于 Spark-TTS 论文内容，三个模型的语言模型架构在基础架构、训练策略和功能集成方面存在显著差异。以下是详细比较：

<span class="token function selector">\subsection</span><span class="token punctuation">{</span><span class="token headline class-name">核心架构对比</span><span class="token punctuation">}</span>

<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">table</span><span class="token punctuation">}</span><span class="token punctuation">[</span>h<span class="token punctuation">]</span>
<span class="token function selector">\centering</span>
<span class="token function selector">\caption</span><span class="token punctuation">{</span>语言模型架构核心特征比较<span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">tabular</span><span class="token punctuation">}</span><span class="token punctuation">{</span>&gt;<span class="token punctuation">{</span><span class="token function selector">\raggedright</span><span class="token punctuation">}</span>p<span class="token punctuation">{</span>2.5cm<span class="token punctuation">}</span>&gt;<span class="token punctuation">{</span><span class="token function selector">\raggedright</span><span class="token punctuation">}</span>p<span class="token punctuation">{</span>4.5cm<span class="token punctuation">}</span>&gt;<span class="token punctuation">{</span><span class="token function selector">\raggedright</span><span class="token punctuation">}</span>p<span class="token punctuation">{</span>4.5cm<span class="token punctuation">}</span>&gt;<span class="token punctuation">{</span><span class="token function selector">\raggedright</span><span class="token punctuation">}</span>p<span class="token punctuation">{</span>4.5cm<span class="token punctuation">}</span><span class="token punctuation">}</span>
<span class="token function selector">\toprule</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>架构特征<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Spark-TTS<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Llasa<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>CosyVoice2<span class="token punctuation">}</span> <span class="token function selector">\\</span>
<span class="token function selector">\midrule</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>基础模型<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> Qwen2.5-0.5B (decoder-only transformer) <span class="token punctuation">&amp;</span> LLaMA (decoder-only transformer) <span class="token punctuation">&amp;</span> 自回归LM + 流匹配模型 <span class="token function selector">\\</span>
<span class="token function selector">\hline</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>模型规模<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> 0.5B 参数 <span class="token punctuation">&amp;</span> 8B 参数 <span class="token punctuation">&amp;</span> 未详细说明（两阶段总参数量未知） <span class="token function selector">\\</span>
<span class="token function selector">\hline</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>架构类型<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> 单阶段统一架构 <span class="token punctuation">&amp;</span> 单阶段统一架构 <span class="token punctuation">&amp;</span> 两阶段分离架构 <span class="token function selector">\\</span>
<span class="token function selector">\hline</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>令牌预测<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> 直接预测BiCodec令牌（语义+全局） <span class="token punctuation">&amp;</span> 直接预测FSQ单流令牌 <span class="token punctuation">&amp;</span> 阶段1：语义令牌；阶段2：声学特征 <span class="token function selector">\\</span>
<span class="token function selector">\hline</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>训练策略<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> 基于VoxBox微调Qwen2.5 <span class="token punctuation">&amp;</span> 基于250k小时数据训练LLaMA <span class="token punctuation">&amp;</span> 两阶段分别训练 <span class="token function selector">\\</span>
<span class="token function selector">\hline</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>文本集成<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> 统一文本-语音令牌化 <span class="token punctuation">&amp;</span> 统一文本-语音令牌化 <span class="token punctuation">&amp;</span> 文本到语义令牌转换 <span class="token function selector">\\</span>
<span class="token function selector">\hline</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>控制机制<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> Chain-of-Thought分层控制 <span class="token punctuation">&amp;</span> 无显式控制机制 <span class="token punctuation">&amp;</span> 可能通过文本提示控制 <span class="token function selector">\\</span>
<span class="token function selector">\hline</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>推理流程<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> 端到端单次生成 <span class="token punctuation">&amp;</span> 端到端单次生成 <span class="token punctuation">&amp;</span> 序列化两阶段生成 <span class="token function selector">\\</span>
<span class="token function selector">\bottomrule</span>
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">tabular</span><span class="token punctuation">}</span>
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">table</span><span class="token punctuation">}</span>

<span class="token function selector">\subsection</span><span class="token punctuation">{</span><span class="token headline class-name">详细架构分析</span><span class="token punctuation">}</span>

<span class="token function selector">\subsubsection</span><span class="token punctuation">{</span><span class="token headline class-name">Spark-TTS语言模型架构</span><span class="token punctuation">}</span>

<span class="token function selector">\textbf</span><span class="token punctuation">{</span>核心组成：<span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>基础架构<span class="token punctuation">}</span>：基于Qwen2.5-0.5B的decoder-only transformer
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>令牌集成<span class="token punctuation">}</span>：
    <span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
        <span class="token function selector">\item</span> 文本令牌：BPE-based Qwen2.5 tokenizer
        <span class="token function selector">\item</span> 属性令牌：粗粒度标签（性别、音高等级、语速等级）+ 细粒度数值
        <span class="token function selector">\item</span> 语音令牌：BiCodec产生的语义令牌（50 TPS）+ 全局令牌（固定长度）
    <span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>训练目标<span class="token punctuation">}</span>：
    <span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
        <span class="token function selector">\item</span> 零样本TTS：<span class="token equation string">$<span class="token equation-command regex">\mathcal</span>{L}_{zst}=-<span class="token equation-command regex">\sum</span>_{t=1}^{T_{c}}<span class="token equation-command regex">\log</span> P(o_{t}|<span class="token equation-command regex">\mathcal</span>{T},<span class="token equation-command regex">\mathcal</span>{G},<span class="token equation-command regex">\boldsymbol</span>{o}_{&lt;t};<span class="token equation-command regex">\theta</span>_{LM})$</span>
        <span class="token function selector">\item</span> 语音创造：<span class="token equation string">$<span class="token equation-command regex">\mathcal</span>{L}_{control}=-<span class="token equation-command regex">\sum</span>_{t=1}^{T_{c}}<span class="token equation-command regex">\log</span> P(c_{t}|<span class="token equation-command regex">\mathcal</span>{T},<span class="token equation-command regex">\mathcal</span>{A},<span class="token equation-command regex">\boldsymbol</span>{c}_{&lt;t};<span class="token equation-command regex">\theta</span>_{LM})$</span>
    <span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\textbf</span><span class="token punctuation">{</span>创新特性：<span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Chain-of-Thought推理<span class="token punctuation">}</span>：支持分层控制，先预测属性值，再生成全局令牌，最后生成语义令牌
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>统一训练<span class="token punctuation">}</span>：<span class="token equation string">$<span class="token equation-command regex">\mathcal</span>{L}_{zst}$</span>和<span class="token equation string">$<span class="token equation-command regex">\mathcal</span>{L}_{control}$</span>在训练中混合使用
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>多模态集成<span class="token punctuation">}</span>：文本、属性、语音令牌在同一个LLM中统一处理
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\subsubsection</span><span class="token punctuation">{</span><span class="token headline class-name">Llasa语言模型架构</span><span class="token punctuation">}</span>

<span class="token function selector">\textbf</span><span class="token punctuation">{</span>核心组成：<span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>基础架构<span class="token punctuation">}</span>：基于LLaMA的decoder-only transformer
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>令牌处理<span class="token punctuation">}</span>：FSQ-based单流令牌，代码本大小65,536
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>训练规模<span class="token punctuation">}</span>：250k小时训练数据，8B参数
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>生成方式<span class="token punctuation">}</span>：直接自回归预测语音令牌序列
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\textbf</span><span class="token punctuation">{</span>架构特点：<span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>简化设计<span class="token punctuation">}</span>：专注于零样本TTS，无复杂的控制机制
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>规模优势<span class="token punctuation">}</span>：通过大规模参数和数据提升生成质量
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>效率考虑<span class="token punctuation">}</span>：单流令牌简化了语言模型的预测任务
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\subsubsection</span><span class="token punctuation">{</span><span class="token headline class-name">CosyVoice2语言模型架构</span><span class="token punctuation">}</span>

<span class="token function selector">\textbf</span><span class="token punctuation">{</span>两阶段架构分解：<span class="token punctuation">}</span>

<span class="token function selector">\textbf</span><span class="token punctuation">{</span>阶段1：自回归语言模型<span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>功能<span class="token punctuation">}</span>：语义令牌预测
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>架构<span class="token punctuation">}</span>：基于transoder的自回归模型
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>输入<span class="token punctuation">}</span>：文本令牌
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>输出<span class="token punctuation">}</span>：语义令牌序列
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>训练目标<span class="token punctuation">}</span>：最大化语义令牌的似然概率
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\textbf</span><span class="token punctuation">{</span>阶段2：流匹配模型<span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>功能<span class="token punctuation">}</span>：声学特征生成
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>架构<span class="token punctuation">}</span>：基于扩散原理的生成模型
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>输入<span class="token punctuation">}</span>：语义令牌
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>输出<span class="token punctuation">}</span>：声学特征（可能为MEL谱或类似表示）
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>优势<span class="token punctuation">}</span>：并行生成，训练稳定性高
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\subsection</span><span class="token punctuation">{</span><span class="token headline class-name">架构优势与局限比较</span><span class="token punctuation">}</span>

<span class="token function selector">\subsubsection</span><span class="token punctuation">{</span><span class="token headline class-name">Spark-TTS架构优势</span><span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>统一性<span class="token punctuation">}</span>：文本和语音在同一LLM中处理，架构简洁
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>可控性<span class="token punctuation">}</span>：CoT机制实现细粒度属性控制
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>效率<span class="token punctuation">}</span>：单阶段生成，推理延迟低
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>灵活性<span class="token punctuation">}</span>：支持零样本TTS和属性控制两种模式
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\textbf</span><span class="token punctuation">{</span>局限性：<span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> 说话人相似性略低于多阶段方法
    <span class="token function selector">\item</span> 需要精心设计的令牌化策略
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\subsubsection</span><span class="token punctuation">{</span><span class="token headline class-name">Llasa架构优势</span><span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>简洁性<span class="token punctuation">}</span>：单流令牌简化了建模复杂度
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>可扩展性<span class="token punctuation">}</span>：基于成熟的LLaMA架构，易于扩展
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>生成质量<span class="token punctuation">}</span>：大规模参数确保高质量的语音生成
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\textbf</span><span class="token punctuation">{</span>局限性：<span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> 缺乏细粒度控制能力
    <span class="token function selector">\item</span> 参数量大，计算资源需求高
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\subsubsection</span><span class="token punctuation">{</span><span class="token headline class-name">CosyVoice2架构优势</span><span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>质量优势<span class="token punctuation">}</span>：流匹配提供高质量的声学特征生成
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>训练稳定性<span class="token punctuation">}</span>：两阶段训练避免复杂多任务优化
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>模块化<span class="token punctuation">}</span>：各阶段可独立优化和改进
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\textbf</span><span class="token punctuation">{</span>局限性：<span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> 推理流程复杂，延迟较高
    <span class="token function selector">\item</span> 两阶段误差累积可能影响最终质量
    <span class="token function selector">\item</span> 架构复杂性增加系统集成难度
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\subsection</span><span class="token punctuation">{</span><span class="token headline class-name">技术趋势分析</span><span class="token punctuation">}</span>

<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>统一化趋势<span class="token punctuation">}</span>：Spark-TTS代表向统一文本-语音LLM发展的方向
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>专业化趋势<span class="token punctuation">}</span>：CosyVoice2体现通过专业化模块提升质量的思路
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>规模化趋势<span class="token punctuation">}</span>：Llasa展示通过参数规模提升性能的路径
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\subsection</span><span class="token punctuation">{</span><span class="token headline class-name">结论</span><span class="token punctuation">}</span>

三个模型的语言模型架构体现了TTS领域的不同技术路线：
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Spark-TTS<span class="token punctuation">}</span>：通过<span class="token function selector">\textbf</span><span class="token punctuation">{</span>统一架构<span class="token punctuation">}</span>和<span class="token function selector">\textbf</span><span class="token punctuation">{</span>CoT控制<span class="token punctuation">}</span>实现灵活高效的语音生成
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Llasa<span class="token punctuation">}</span>：依赖<span class="token function selector">\textbf</span><span class="token punctuation">{</span>大规模基础模型<span class="token punctuation">}</span>和<span class="token function selector">\textbf</span><span class="token punctuation">{</span>简化令牌化<span class="token punctuation">}</span>保证生成质量
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>CosyVoice2<span class="token punctuation">}</span>：采用<span class="token function selector">\textbf</span><span class="token punctuation">{</span>专业化两阶段架构<span class="token punctuation">}</span>和<span class="token function selector">\textbf</span><span class="token punctuation">{</span>流匹配技术<span class="token punctuation">}</span>优化声学质量
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

每种架构都有其适用的场景：Spark-TTS适合需要细粒度控制的场景，Llasa适合追求最高生成质量的场景，CosyVoice2适合对声学质量有极致要求的应用。

<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">document</span><span class="token punctuation">}</span></pre><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _33882ae"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _28d7e84"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg></div>

---

### 用户

F5-TTS就是llasa吗

---

### DeepSeek AI

<p>思考：</p><blockquote><p class="ds-markdown-paragraph"><span>嗯，用户问的是“F5-TTS就是llasa吗”，首先得确认这两个模型是不是同一个。根据之前提供的资料，用户已经看过Spark-TTS的论文，里面提到了Llasa和F5-TTS，但可能混淆了。</span></p><p class="ds-markdown-paragraph"><span>用户可能是研究人员或者开发者，正在比较不同的TTS模型，想弄清楚它们之间的区别，避免在引用或使用时出错。深层需求可能是想了解哪个模型更适合自己的项目，或者需要准确的信息来做技术选型。</span></p><p class="ds-markdown-paragraph"><span>首先，回顾论文内容，Llasa和F5-TTS在模型结构、生成方法等方面都有区别。比如Llasa是自回归的，而F5-TTS用了流匹配，属于非自回归。另外，训练数据和参数规模也不同。需要明确指出这些差异，避免用户误解。</span></p><p class="ds-markdown-paragraph"><span>然后，考虑到用户之前已经得到了详细的对比，可能是在整理资料时发现这两个名称同时出现，担心它们是同一个模型的不同名称。需要明确否定这一点，并解释各自的独特之处。</span></p><p class="ds-markdown-paragraph"><span>最后，确保回答清晰，分点说明差异，帮助用户快速抓住关键区别，同时满足他们深层的研究或应用需求。</span></p></blockquote><br/><p class="ds-markdown-paragraph"><span>根据提供的 Spark-TTS 论文内容，</span><strong><span>F5-TTS 并不是 Llasa</span></strong><span>，它们是两个完全不同的模型。</span></p><p class="ds-markdown-paragraph"><span>论文中在多个地方明确区分了这两个模型：</span></p><h3><span>关键区别证据</span></h3><ol start="1"><li><p class="ds-markdown-paragraph"><strong><span>在零样本TTS性能对比表格（表4）中</span></strong><span>：</span></p><ul><li><p class="ds-markdown-paragraph">`F5-TTS`<span> 被归类为 </span><strong><span>"Multi-Stage or NAR Methods"</span></strong><span>（多阶段或非自回归方法）</span></p></li><li><p class="ds-markdown-paragraph">`Llasa`<span> 被归类为 </span><strong><span>"One-Stage AR Methods"</span></strong><span>（单阶段自回归方法）</span></p></li></ul></li><li><p class="ds-markdown-paragraph"><strong><span>在相关论述中</span></strong><span>：</span></p><ul><li><p class="ds-markdown-paragraph"><span>F5-TTS 被描述为基于</span><strong><span>流匹配（flow matching）</span></strong><span> 的方法</span></p></li><li><p class="ds-markdown-paragraph"><span>Llasa 被描述为基于</span><strong><span>自回归语言模型</span></strong><span>的方法</span></p></li></ul></li></ol><h3><span>详细技术区别</span></h3><div class="ds-scroll-area _1210dd7 c03cafe9"><div class="ds-scroll-area__gutters" style="position: sticky; top: 0px; left: 0px; right: 0px; height: 0px; --container-height: 274px;"><div class="ds-scroll-area__horizontal-gutter" style="left: 0px; right: 0px; top: calc(var(--container-height) - 14px); height: 10px;"><div class="ds-scroll-area__horizontal-bar" style="display: none;"></div></div><div class="ds-scroll-area__vertical-gutter" style="right: 0px; top: 8px; bottom: calc(0px - var(--container-height) + 8px); width: 10px;"><div class="ds-scroll-area__vertical-bar" style="display: none;"></div></div></div><table><thead><tr><th><span>特征</span></th><th><span>F5-TTS</span></th><th><span>Llasa</span></th></tr></thead><tbody><tr><td><strong><span>生成方式</span></strong></td><td><span>多阶段/非自回归（NAR）</span></td><td><span>单阶段自回归（AR）</span></td></tr><tr><td><strong><span>核心技术</span></strong></td><td><span>流匹配（flow matching）</span></td><td><span>自回归语言模型</span></td></tr><tr><td><strong><span>推理步骤</span></strong></td><td><span>32 NFE（数值函数评估）</span></td><td><span>直接自回归生成</span></td></tr><tr><td><strong><span>架构类型</span></strong></td><td><span>多阶段流程</span></td><td><span>单流代码预测</span></td></tr><tr><td><strong><span>模型规模</span></strong></td><td><span>未详细说明</span></td><td><span>1B/3B/8B参数</span></td></tr></tbody></table></div><h3><span>论文中的具体引用</span></h3><p class="ds-markdown-paragraph"><span>在</span><strong><span>第7页零样本TTS性能评估部分</span></strong><span>，论文明确写道：</span></p><blockquote><p class="ds-markdown-paragraph"><span>"在英语WER方面，Spark-TTS仅次于F5-TTS...在说话人相似性方面，Spark-TTS显著优于单阶段模型Llasa"</span></p></blockquote><p class="ds-markdown-paragraph"><span>这清楚地表明：</span></p><ul><li><p class="ds-markdown-paragraph"><strong><span>F5-TTS</span></strong><span> 是多阶段方法的代表</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>Llasa</span></strong><span> 是单阶段方法的代表</span></p></li><li><p class="ds-markdown-paragraph"><span>两者是不同的技术路线</span></p></li></ul><h3><span>结论</span></h3><p class="ds-markdown-paragraph"><strong><span>F5-TTS ≠ Llasa</span></strong><span>，它们是：</span></p><ul><li><p class="ds-markdown-paragraph"><strong><span>不同的技术架构</span></strong><span>（流匹配 vs 自回归LLM）</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>不同的生成范式</span></strong><span>（多阶段NAR vs 单阶段AR）</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>不同的模型类别</span></strong><span>（在论文中被明确区分比较）</span></p></li></ul><p class="ds-markdown-paragraph"><span>F5-TTS是基于流匹配的多阶段模型，而Llasa是基于自回归语言模型的单阶段方法。</span></p>

---

### 用户

比较F5TTS，cosyvoice和sparktts三者的语言模型架构

---

### DeepSeek AI

<p>思考：</p><blockquote><p class="ds-markdown-paragraph"><span>我们首先需要明确这三个模型的语言模型架构特点。根据提供的论文内容，我们可以总结如下：</span></p><ol start="1"><li><p class="ds-markdown-paragraph"><strong><span>Spark-TTS</span></strong><span>:</span></p><ul><li><p class="ds-markdown-paragraph"><span>使用Qwen2.5-0.5B作为基础语言模型（decoder-only transformer）。</span></p></li><li><p class="ds-markdown-paragraph"><span>采用BiCodec进行语音token化，生成两种token：语义token（50 TPS）和全局token（固定长度）。</span></p></li><li><p class="ds-markdown-paragraph"><span>支持通过Chain-of-Thought (CoT) 进行粗粒度和细粒度的属性控制。</span></p></li><li><p class="ds-markdown-paragraph"><span>训练时混合零样本TTS和语音创造两种目标。</span></p></li></ul></li><li><p class="ds-markdown-paragraph"><strong><span>CosyVoice2</span></strong><span>:</span></p><ul><li><p class="ds-markdown-paragraph"><span>两阶段模型：第一阶段使用自回归语言模型预测语义token，第二阶段使用流匹配（flow matching）生成声学特征。</span></p></li><li><p class="ds-markdown-paragraph"><span>语义token基于监督学习，声学特征通过流匹配生成，流匹配是一种非自回归生成方法。</span></p></li><li><p class="ds-markdown-paragraph"><span>论文中未强调细粒度属性控制，但可能支持文本提示控制。</span></p></li></ul></li><li><p class="ds-markdown-paragraph"><strong><span>F5-TTS</span></strong><span>:</span></p><ul><li><p class="ds-markdown-paragraph"><span>基于流匹配（flow matching）的多阶段模型，使用流匹配生成声学特征（如Mel频谱）。</span></p></li><li><p class="ds-markdown-paragraph"><span>在零样本TTS任务中，使用32步NFE（数值函数评估）进行推理。</span></p></li><li><p class="ds-markdown-paragraph"><span>属于非自回归（NAR）或部分自回归的方法，具体架构未在论文中详细说明，但被归类为多阶段方法。</span></p></li></ul></li></ol><p class="ds-markdown-paragraph"><span>现在，我们将从语言模型架构的角度对这三者进行比较，包括模型类型、生成方式、token化方法、控制能力、训练目标等。</span></p></blockquote><br/><div class="md-code-block md-code-block-light"><div class="md-code-block-banner-wrap"><div class="md-code-block-banner md-code-block-banner-lite"><div class="_121d384"><div class="d2a24f03"><span class="d813de27">latex</span></div><div class="d2a24f03 _246a029"><div class="efa13877"><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon" style="margin-right: 4px;"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.14923 4.02032C7.11191 4.02032 7.87977 4.02017 8.49591 4.07599C9.12122 4.1327 9.65786 4.25188 10.1414 4.53107C10.7201 4.8653 11.2008 5.34591 11.535 5.92462C11.8142 6.40818 11.9333 6.94482 11.9901 7.57013C12.0459 8.18625 12.0457 8.9542 12.0457 9.91681C12.0457 10.8795 12.0459 11.6474 11.9901 12.2635C11.9333 12.8888 11.8142 13.4254 11.535 13.909C11.2008 14.4877 10.7201 14.9683 10.1414 15.3026C9.65786 15.5817 9.12122 15.7009 8.49591 15.7576C7.87977 15.8134 7.1119 15.8133 6.14923 15.8133C5.18661 15.8133 4.41868 15.8134 3.80255 15.7576C3.17724 15.7009 2.6406 15.5817 2.15704 15.3026C1.57834 14.9684 1.09772 14.4877 0.763489 13.909C0.484305 13.4254 0.365123 12.8888 0.308411 12.2635C0.252587 11.6474 0.252747 10.8795 0.252747 9.91681C0.252747 8.95419 0.252603 8.18625 0.308411 7.57013C0.365123 6.94482 0.484305 6.40818 0.763489 5.92462C1.09771 5.3459 1.57833 4.86529 2.15704 4.53107C2.6406 4.25188 3.17724 4.1327 3.80255 4.07599C4.41868 4.02018 5.1866 4.02032 6.14923 4.02032ZM6.14923 5.37775C5.16175 5.37775 4.46628 5.37761 3.9256 5.42657C3.39428 5.47473 3.07853 5.56574 2.83575 5.70587C2.46313 5.92106 2.15348 6.23071 1.93829 6.60333C1.79817 6.84611 1.70715 7.16185 1.659 7.69318C1.61004 8.23385 1.61017 8.92934 1.61017 9.91681C1.61017 10.9043 1.61002 11.5998 1.659 12.1404C1.70715 12.6717 1.79817 12.9875 1.93829 13.2303C2.15349 13.6029 2.46315 13.9126 2.83575 14.1277C3.07853 14.2679 3.39428 14.3589 3.9256 14.407C4.46628 14.456 5.16176 14.4559 6.14923 14.4559C7.13675 14.4559 7.83218 14.456 8.37286 14.407C8.90419 14.3589 9.21993 14.2679 9.46271 14.1277C9.83529 13.9126 10.145 13.6029 10.3602 13.2303C10.5003 12.9875 10.5913 12.6718 10.6395 12.1404C10.6884 11.5998 10.6883 10.9043 10.6883 9.91681C10.6883 8.92935 10.6884 8.23385 10.6395 7.69318C10.5913 7.16185 10.5003 6.84611 10.3602 6.60333C10.145 6.23072 9.8353 5.92107 9.46271 5.70587C9.21993 5.56574 8.90418 5.47473 8.37286 5.42657C7.83218 5.3776 7.13676 5.37775 6.14923 5.37775ZM9.80157 0.367981C10.7637 0.367981 11.5313 0.367886 12.1473 0.423645C12.7725 0.480313 13.3093 0.598765 13.7928 0.877747C14.3716 1.21192 14.852 1.69355 15.1863 2.27228C15.4655 2.75575 15.5857 3.29165 15.6424 3.91681C15.6982 4.53301 15.6971 5.30161 15.6971 6.26447V7.8299C15.6971 8.29265 15.6989 8.58994 15.6649 8.84845C15.4667 10.3525 14.4009 11.5738 12.9832 11.9988V10.5467C13.6973 10.1903 14.2104 9.49662 14.3192 8.67169C14.3387 8.52348 14.3406 8.3358 14.3406 7.8299V6.26447C14.3406 5.27707 14.3398 4.58149 14.2908 4.04083C14.2427 3.50969 14.1526 3.19373 14.0125 2.95099C13.7974 2.5785 13.4875 2.2687 13.1151 2.05353C12.8723 1.91347 12.5563 1.82237 12.0252 1.77423C11.4846 1.72528 10.7888 1.7254 9.80157 1.7254H7.71466C6.75614 1.72559 5.92659 2.27697 5.52325 3.07892H4.07013C4.54215 1.51132 5.99314 0.368192 7.71466 0.367981H9.80157Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">复制</span></span><div class="ds-focus-ring"></div></button><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M15.3695 11.411L15.1234 12.8866C14.8869 14.3042 13.6603 15.3436 12.223 15.3436H3.7767C2.33954 15.3434 1.11276 14.3042 0.876312 12.8866L0.630219 11.411L2.05405 11.1747L2.29916 12.6493C2.41969 13.3713 3.04472 13.9001 3.7767 13.9003H12.223C12.9551 13.9002 13.58 13.3713 13.7005 12.6493L13.9456 11.1747L15.3695 11.411ZM8.72202 8.994C8.77714 8.93934 8.83789 8.88106 8.90268 8.81627L12.4828 5.23424L13.5042 6.25572L9.92221 9.8358C9.63947 10.1185 9.3876 10.3732 9.15854 10.5575C8.91889 10.7503 8.6395 10.9224 8.28647 10.9784C8.09708 11.0083 7.9036 11.0083 7.7142 10.9784C7.36103 10.9224 7.08087 10.7503 6.84116 10.5575C6.61212 10.3732 6.36019 10.1185 6.07748 9.8358L2.49643 6.25572L3.51694 5.23424L7.09702 8.81627C7.16216 8.88142 7.22327 8.94006 7.27866 8.99498V1.3065H8.72202V8.994Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">下载</span></span><div class="ds-focus-ring"></div></button></div></div></div></div></div><pre><span class="token function selector">\documentclass</span><span class="token punctuation">{</span><span class="token keyword">article</span><span class="token punctuation">}</span>
<span class="token function selector">\usepackage</span><span class="token punctuation">{</span><span class="token keyword">amsmath</span><span class="token punctuation">}</span>
<span class="token function selector">\usepackage</span><span class="token punctuation">{</span><span class="token keyword">booktabs</span><span class="token punctuation">}</span>
<span class="token function selector">\usepackage</span><span class="token punctuation">{</span><span class="token keyword">array</span><span class="token punctuation">}</span>

<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">document</span><span class="token punctuation">}</span>

<span class="token function selector">\section</span><span class="token punctuation">{</span><span class="token headline class-name">F5-TTS、CosyVoice2与Spark-TTS语言模型架构比较</span><span class="token punctuation">}</span>

<span class="token function selector">\subsection</span><span class="token punctuation">{</span><span class="token headline class-name">架构概述</span><span class="token punctuation">}</span>

基于 Spark-TTS 论文内容，F5-TTS、CosyVoice2 和 Spark-TTS 代表了三种不同的 TTS 技术路线，其语言模型架构在基础范式、生成方式和功能特性方面存在显著差异。

<span class="token function selector">\subsection</span><span class="token punctuation">{</span><span class="token headline class-name">核心架构对比</span><span class="token punctuation">}</span>

<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">table</span><span class="token punctuation">}</span><span class="token punctuation">[</span>h<span class="token punctuation">]</span>
<span class="token function selector">\centering</span>
<span class="token function selector">\caption</span><span class="token punctuation">{</span>语言模型架构核心特征比较<span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">tabular</span><span class="token punctuation">}</span><span class="token punctuation">{</span>&gt;<span class="token punctuation">{</span><span class="token function selector">\raggedright</span><span class="token punctuation">}</span>p<span class="token punctuation">{</span>2.2cm<span class="token punctuation">}</span>&gt;<span class="token punctuation">{</span><span class="token function selector">\raggedright</span><span class="token punctuation">}</span>p<span class="token punctuation">{</span>4cm<span class="token punctuation">}</span>&gt;<span class="token punctuation">{</span><span class="token function selector">\raggedright</span><span class="token punctuation">}</span>p<span class="token punctuation">{</span>4cm<span class="token punctuation">}</span>&gt;<span class="token punctuation">{</span><span class="token function selector">\raggedright</span><span class="token punctuation">}</span>p<span class="token punctuation">{</span>4cm<span class="token punctuation">}</span><span class="token punctuation">}</span>
<span class="token function selector">\toprule</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>架构特征<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>F5-TTS<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>CosyVoice2<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Spark-TTS<span class="token punctuation">}</span> <span class="token function selector">\\</span>
<span class="token function selector">\midrule</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>基础范式<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> 流匹配（Flow Matching） <span class="token punctuation">&amp;</span> 两阶段混合（AR + 流匹配） <span class="token punctuation">&amp;</span> 单阶段自回归（AR） <span class="token function selector">\\</span>
<span class="token function selector">\hline</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>生成方式<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> 非自回归（NAR） <span class="token punctuation">&amp;</span> 阶段1：AR，阶段2：NAR <span class="token punctuation">&amp;</span> 纯自回归（AR） <span class="token function selector">\\</span>
<span class="token function selector">\hline</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>语音表示<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> Mel频谱图 <span class="token punctuation">&amp;</span> 语义令牌 + 声学特征 <span class="token punctuation">&amp;</span> BiCodec令牌（语义+全局） <span class="token function selector">\\</span>
<span class="token function selector">\hline</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>模型架构<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> 流匹配模型 <span class="token punctuation">&amp;</span> 自回归LM + 流匹配模型 <span class="token punctuation">&amp;</span> 单一Transformer LM <span class="token function selector">\\</span>
<span class="token function selector">\hline</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>推理步骤<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> 32 NFE <span class="token punctuation">&amp;</span> 两阶段序列生成 <span class="token punctuation">&amp;</span> 单阶段端到端生成 <span class="token function selector">\\</span>
<span class="token function selector">\hline</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>控制能力<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> 有限控制（论文未强调） <span class="token punctuation">&amp;</span> 可能支持文本提示控制 <span class="token punctuation">&amp;</span> 细粒度CoT分层控制 <span class="token function selector">\\</span>
<span class="token function selector">\hline</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>训练策略<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> 流匹配训练 <span class="token punctuation">&amp;</span> 两阶段分别训练 <span class="token punctuation">&amp;</span> 统一多任务训练 <span class="token function selector">\\</span>
<span class="token function selector">\hline</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>主要优势<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> 高质量声学生成 <span class="token punctuation">&amp;</span> 平衡质量与效率 <span class="token punctuation">&amp;</span> 灵活控制与高效推理 <span class="token function selector">\\</span>
<span class="token function selector">\bottomrule</span>
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">tabular</span><span class="token punctuation">}</span>
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">table</span><span class="token punctuation">}</span>

<span class="token function selector">\subsection</span><span class="token punctuation">{</span><span class="token headline class-name">详细架构分析</span><span class="token punctuation">}</span>

<span class="token function selector">\subsubsection</span><span class="token punctuation">{</span><span class="token headline class-name">F5-TTS语言模型架构</span><span class="token punctuation">}</span>

<span class="token function selector">\textbf</span><span class="token punctuation">{</span>核心架构特性：<span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>基础技术<span class="token punctuation">}</span>：基于流匹配（Flow Matching）的生成模型
    <span class="token function selector">\item</span> <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>生成目标<span class="token punctuation">}</span>：直接生成Mel频谱图作为声学特征
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>推理过程<span class="token punctuation">}</span>：需要32步数值函数评估（NFE）
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>架构类型<span class="token punctuation">}</span>：纯非自回归生成，支持并行推理
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\textbf</span><span class="token punctuation">{</span>技术细节：<span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>流匹配原理<span class="token punctuation">}</span>：通过学习向量场将简单分布转换为复杂数据分布
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>声学建模<span class="token punctuation">}</span>：直接建模连续声学特征，避免离散令牌的量化误差
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>训练稳定性<span class="token punctuation">}</span>：流匹配相比传统扩散模型具有更好的训练稳定性
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\textbf</span><span class="token punctuation">{</span>优势与局限：<span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>优势<span class="token punctuation">}</span>：高质量的声学生成，避免自回归的误差累积
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>优势<span class="token punctuation">}</span>：并行生成，推理速度相对较快
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>局限<span class="token punctuation">}</span>：控制能力有限，缺乏细粒度属性调节
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>局限<span class="token punctuation">}</span>：多步推理仍有一定计算开销
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\subsubsection</span><span class="token punctuation">{</span><span class="token headline class-name">CosyVoice2语言模型架构</span><span class="token punctuation">}</span>

<span class="token function selector">\textbf</span><span class="token punctuation">{</span>两阶段混合架构：<span class="token punctuation">}</span>

<span class="token function selector">\textbf</span><span class="token punctuation">{</span>阶段1：自回归语义建模<span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>架构<span class="token punctuation">}</span>：基于Transformer的自回归语言模型
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>目标<span class="token punctuation">}</span>：从文本生成语义令牌序列
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>特性<span class="token punctuation">}</span>：保持语言建模的强序列建模能力
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>训练<span class="token punctuation">}</span>：最大似然估计训练语义令牌预测
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\textbf</span><span class="token punctuation">{</span>阶段2：流匹配声学生成<span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>架构<span class="token punctuation">}</span>：流匹配生成模型
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>目标<span class="token punctuation">}</span>：从语义令牌生成声学特征
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>特性<span class="token punctuation">}</span>：非自回归并行生成，保证效率
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>集成<span class="token punctuation">}</span>：两阶段通过语义令牌桥接
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\textbf</span><span class="token punctuation">{</span>架构创新点：<span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>解耦设计<span class="token punctuation">}</span>：语言建模与声学生成分离，各自优化
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>质量保证<span class="token punctuation">}</span>：流匹配提供高质量的声学生成
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>效率平衡<span class="token punctuation">}</span>：AR阶段保持语言质量，NAR阶段保证生成效率
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\subsubsection</span><span class="token punctuation">{</span><span class="token headline class-name">Spark-TTS语言模型架构</span><span class="token punctuation">}</span>

<span class="token function selector">\textbf</span><span class="token punctuation">{</span>统一单阶段架构：<span class="token punctuation">}</span>

<span class="token function selector">\textbf</span><span class="token punctuation">{</span>核心组件：<span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>基础模型<span class="token punctuation">}</span>：Qwen2.5-0.5B decoder-only transformer
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>令牌集成<span class="token punctuation">}</span>：
    <span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
        <span class="token function selector">\item</span> 文本令牌：BPE-based tokenization
        <span class="token function selector">\item</span> 属性令牌：粗粒度标签 + 细粒度数值
        <span class="token function selector">\item</span> 语音令牌：BiCodec语义令牌 + 全局令牌
    <span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>训练目标<span class="token punctuation">}</span>：混合零样本TTS和语音创造目标
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\textbf</span><span class="token punctuation">{</span>创新特性：<span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Chain-of-Thought推理<span class="token punctuation">}</span>：
    <span class="token equation string">\[
    <span class="token equation-command regex">\text</span>{属性标签} <span class="token equation-command regex">\rightarrow</span> <span class="token equation-command regex">\text</span>{属性值} <span class="token equation-command regex">\rightarrow</span> <span class="token equation-command regex">\text</span>{全局令牌} <span class="token equation-command regex">\rightarrow</span> <span class="token equation-command regex">\text</span>{语义令牌}
    \]</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>统一建模<span class="token punctuation">}</span>：文本、属性、语音在单一LLM中统一处理
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>细粒度控制<span class="token punctuation">}</span>：支持精确的音高、语速数值控制
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\textbf</span><span class="token punctuation">{</span>训练策略：<span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> 多任务学习：同时优化<span class="token equation string">$<span class="token equation-command regex">\mathcal</span>{L}_{zst}$</span>和<span class="token equation string">$<span class="token equation-command regex">\mathcal</span>{L}_{control}$</span>
    <span class="token function selector">\item</span> 数据利用：基于VoxBox的100k小时标注数据
    <span class="token function selector">\item</span> 微调方法：在预训练Qwen2.5基础上进行针对性微调
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\subsection</span><span class="token punctuation">{</span><span class="token headline class-name">技术路线对比</span><span class="token punctuation">}</span>

<span class="token function selector">\subsubsection</span><span class="token punctuation">{</span><span class="token headline class-name">生成范式演进</span><span class="token punctuation">}</span>

<span class="token function selector">\textbf</span><span class="token punctuation">{</span>F5-TTS → 纯NAR流匹配<span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> 完全摒弃自回归，追求生成效率
    <span class="token function selector">\item</span> 基于连续流匹配，避免离散化损失
    <span class="token function selector">\item</span> 适合对实时性要求高的场景
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\textbf</span><span class="token punctuation">{</span>CosyVoice2 → 混合AR-NAR<span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> 平衡质量与效率的折中方案
    <span class="token function selector">\item</span> AR阶段保证语言准确性，NAR阶段保证声学质量
    <span class="token function selector">\item</span> 适合对生成质量有均衡要求的场景
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\textbf</span><span class="token punctuation">{</span>Spark-TTS → 统一AR架构<span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> 回归自回归的本质，统一文本与语音建模
    <span class="token function selector">\item</span> 通过先进令牌化弥补传统AR的效率问题
    <span class="token function selector">\item</span> 适合需要细粒度控制的复杂场景
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\subsubsection</span><span class="token punctuation">{</span><span class="token headline class-name">令牌化策略对比</span><span class="token punctuation">}</span>

<span class="token function selector">\textbf</span><span class="token punctuation">{</span>F5-TTS<span class="token punctuation">}</span>：直接连续特征
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> 优点：无量化误差，声学质量高
    <span class="token function selector">\item</span> 缺点：建模复杂度高，控制困难
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\textbf</span><span class="token punctuation">{</span>CosyVoice2<span class="token punctuation">}</span>：语义令牌桥接
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> 优点：解耦语言与声学，便于优化
    <span class="token function selector">\item</span> 缺点：两阶段误差累积，架构复杂
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\textbf</span><span class="token punctuation">{</span>Spark-TTS<span class="token punctuation">}</span>：混合离散令牌
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> 优点：细粒度控制，统一架构
    <span class="token function selector">\item</span> 缺点：量化损失，说话人相似性受限
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\subsection</span><span class="token punctuation">{</span><span class="token headline class-name">性能与应用场景</span><span class="token punctuation">}</span>

<span class="token function selector">\subsubsection</span><span class="token punctuation">{</span><span class="token headline class-name">零样本TTS性能</span><span class="token punctuation">}</span>

<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>智能度（CER/WER）<span class="token punctuation">}</span>：
    <span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
        <span class="token function selector">\item</span> Spark-TTS：最优（中英文CER/WER最低）
        <span class="token function selector">\item</span> F5-TTS：英语WER最优，中文中等
        <span class="token function selector">\item</span> CosyVoice2：中等水平
    <span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>说话人相似性<span class="token punctuation">}</span>：
    <span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
        <span class="token function selector">\item</span> F5-TTS：多阶段方法中较优
        <span class="token function selector">\item</span> CosyVoice2：流匹配保证较好相似性
        <span class="token function selector">\item</span> Spark-TTS：单阶段AR方法中最佳
    <span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\subsubsection</span><span class="token punctuation">{</span><span class="token headline class-name">适用场景推荐</span><span class="token punctuation">}</span>

<span class="token function selector">\textbf</span><span class="token punctuation">{</span>F5-TTS适用场景：<span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> 对生成速度和声学质量要求高的实时应用
    <span class="token function selector">\item</span> 不需要复杂属性控制的标准TTS任务
    <span class="token function selector">\item</span> 资源充足，可支持流匹配计算的环境
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\textbf</span><span class="token punctuation">{</span>CosyVoice2适用场景：<span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> 对生成质量有均衡要求的商业应用
    <span class="token function selector">\item</span> 需要一定控制能力但不要求极细粒度的场景
    <span class="token function selector">\item</span> 可接受两阶段推理延迟的系统
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\textbf</span><span class="token punctuation">{</span>Spark-TTS适用场景：<span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> 需要细粒度语音属性控制的创意应用
    <span class="token function selector">\item</span> 希望统一文本和语音架构的技术栈
    <span class="token function selector">\item</span> 对实时性要求不高但需要灵活性的场景
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\subsection</span><span class="token punctuation">{</span><span class="token headline class-name">技术趋势总结</span><span class="token punctuation">}</span>

三种架构代表了TTS领域的技术分化：

<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>F5-TTS<span class="token punctuation">}</span>：追求<span class="token function selector">\textbf</span><span class="token punctuation">{</span>极致效率<span class="token punctuation">}</span>的流匹配路线
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>CosyVoice2<span class="token punctuation">}</span>：坚持<span class="token function selector">\textbf</span><span class="token punctuation">{</span>质量平衡<span class="token punctuation">}</span>的混合架构路线  
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>Spark-TTS<span class="token punctuation">}</span>：探索<span class="token function selector">\textbf</span><span class="token punctuation">{</span>统一控制<span class="token punctuation">}</span>的大语言模型路线
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

每种架构都有其独特的价值主张和适用场景，反映了TTS技术在不同应用需求下的多元化发展。

<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">document</span><span class="token punctuation">}</span></pre><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _33882ae"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _28d7e84"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg></div>

---

### 用户

这是一个 CosyVoice 语音合成系统的完整配置文件，采用 YAML 格式。让我为您详细解读各个部分：

## 1. 随机种子设置
```yaml
__set_seed1-4: 设置所有随机数生成器的种子为1986，确保结果可重现
```

## 2. 基础参数
```yaml
sample_rate: 22050           # 音频采样率
text_encoder_input_size: 512 # 文本编码器输入维度
llm_input_size: 1024         # 大语言模型输入维度
llm_output_size: 1024        # 大语言模型输出维度
spk_embed_dim: 192           # 说话人嵌入维度
```

## 3. 核心模型架构

### 3.1 LLM (大语言模型)
```yaml
llm: !new:cosyvoice.llm.llm.TransformerLM
```
- **文本编码器**: 6层 Conformer 编码器，使用相对位置编码
- **LLM主体**: 14层 Transformer 编码器
- **词汇表大小**: 文本 51866，语音 4096
- **采样策略**: 使用 RAS (top_p=0.8, top_k=25)

### 3.2 Flow 模型 (语音生成)
```yaml
flow: !new:cosyvoice.flow.flow.MaskedDiffWithXvec
```
- **编码器**: 6层 Conformer 编码器
- **长度调节器**: 插值调节器，支持多尺度
- **解码器**: 条件流匹配 (Conditional CFM)
  - 使用 Euler 求解器
  - 余弦时间调度
  - L1 正则化损失

### 3.3 HiFT 声码器
```yaml
hift: !new:cosyvoice.hifigan.generator.HiFTGenerator
```
- 基于 HiFi-GAN 的生成器
- 包含谐波合成滤波器
- 集成 F0 预测器 (ConvRNN)

## 4. 训练配置

### 4.1 LLM + Flow 训练
```yaml
train_conf:
    optim: adam
    lr: 0.001
    scheduler: warmuplr (2500步预热)
    max_epoch: 200
    grad_clip: 5
    accum_grad: 2
```

### 4.2 GAN 训练
```yaml
train_conf_gan:
    lr: 0.0002 (更小的学习率)
    accum_grad: 1 (GAN训练必须为1)
```

## 5. 数据处理流水线

### 5.1 主要流水线
```yaml
data_pipeline: [
    打开parquet文件 → 文本tokenize → 过滤长短样本 → 音频重采样 →
    计算Fbank特征 → 解析说话人嵌入 → 洗牌 → 排序 → 批处理 → 填充
]
```

### 5.2 GAN专用流水线
增加了：
- `truncate`: 截断音频到固定长度
- `compute_f0`: 计算基频特征

## 6. 关键特性分析

### 6.1 模型特点
- **多尺度处理**: 支持4种采样比例的长度调节
- **条件生成**: 使用说话人嵌入进行个性化合成
- **流匹配**: 采用先进的流匹配技术替代传统扩散
- **端到端训练**: 支持从文本到语音的完整流程

### 6.2 技术亮点
- **相对位置编码**: 更好的长度外推能力
- **动态批处理**: 根据帧数动态调整批次大小
- **多判别器**: MPD + MRD 组合提升生成质量
- **灵活的采样策略**: 支持多种解码策略

### 6.3 可调整参数
配置中标注了几个重要的可调整点：
- 词汇表大小 (300M参数版本需要调整)
- 帧率 (25Hz或50Hz)
- 学习率策略 (SFT时使用常量学习率)
- 说话人嵌入 (SFT时启用)

这个配置展现了一个现代化的端到端语音合成系统，结合了大语言模型、流匹配和对抗训练等先进技术。把这个内容写成latex格式

---

### DeepSeek AI

<p>思考：</p><blockquote><p class="ds-markdown-paragraph"><span>我们有一个YAML配置文件，需要将其转换为LaTeX格式。由于内容较多，我们将按照章节组织，并使用LaTeX的itemize和描述性文字来展示。</span><br><span>注意：YAML中的注释需要转换为LaTeX中的注释或直接作为文本。</span><br><span>由于YAML中有很多技术细节，我们将尽量保持结构的清晰。</span></p><p class="ds-markdown-paragraph"><span>我们将按照以下结构组织：</span></p><ol start="1"><li><p class="ds-markdown-paragraph"><span>随机种子设置</span></p></li><li><p class="ds-markdown-paragraph"><span>基础参数</span></p></li><li><p class="ds-markdown-paragraph"><span>核心模型架构（LLM、Flow模型、HiFT声码器）</span></p></li><li><p class="ds-markdown-paragraph"><span>训练配置（LLM+Flow训练、GAN训练）</span></p></li><li><p class="ds-markdown-paragraph"><span>数据处理流水线（主要流水线、GAN专用流水线）</span></p></li><li><p class="ds-markdown-paragraph"><span>关键特性分析（模型特点、技术亮点、可调整参数）</span></p></li></ol><p class="ds-markdown-paragraph"><span>由于YAML中使用了</span>`!new`<span>等自定义标签，我们在LaTeX中将其视为代码。</span></p><p class="ds-markdown-paragraph"><span>我们将使用</span>`\begin{itemize}`<span>和</span>`\begin{description}`<span>来列出各项。</span></p></blockquote><br/><div class="md-code-block md-code-block-light"><div class="md-code-block-banner-wrap"><div class="md-code-block-banner md-code-block-banner-lite"><div class="_121d384"><div class="d2a24f03"><span class="d813de27">latex</span></div><div class="d2a24f03 _246a029"><div class="efa13877"><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon" style="margin-right: 4px;"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.14923 4.02032C7.11191 4.02032 7.87977 4.02017 8.49591 4.07599C9.12122 4.1327 9.65786 4.25188 10.1414 4.53107C10.7201 4.8653 11.2008 5.34591 11.535 5.92462C11.8142 6.40818 11.9333 6.94482 11.9901 7.57013C12.0459 8.18625 12.0457 8.9542 12.0457 9.91681C12.0457 10.8795 12.0459 11.6474 11.9901 12.2635C11.9333 12.8888 11.8142 13.4254 11.535 13.909C11.2008 14.4877 10.7201 14.9683 10.1414 15.3026C9.65786 15.5817 9.12122 15.7009 8.49591 15.7576C7.87977 15.8134 7.1119 15.8133 6.14923 15.8133C5.18661 15.8133 4.41868 15.8134 3.80255 15.7576C3.17724 15.7009 2.6406 15.5817 2.15704 15.3026C1.57834 14.9684 1.09772 14.4877 0.763489 13.909C0.484305 13.4254 0.365123 12.8888 0.308411 12.2635C0.252587 11.6474 0.252747 10.8795 0.252747 9.91681C0.252747 8.95419 0.252603 8.18625 0.308411 7.57013C0.365123 6.94482 0.484305 6.40818 0.763489 5.92462C1.09771 5.3459 1.57833 4.86529 2.15704 4.53107C2.6406 4.25188 3.17724 4.1327 3.80255 4.07599C4.41868 4.02018 5.1866 4.02032 6.14923 4.02032ZM6.14923 5.37775C5.16175 5.37775 4.46628 5.37761 3.9256 5.42657C3.39428 5.47473 3.07853 5.56574 2.83575 5.70587C2.46313 5.92106 2.15348 6.23071 1.93829 6.60333C1.79817 6.84611 1.70715 7.16185 1.659 7.69318C1.61004 8.23385 1.61017 8.92934 1.61017 9.91681C1.61017 10.9043 1.61002 11.5998 1.659 12.1404C1.70715 12.6717 1.79817 12.9875 1.93829 13.2303C2.15349 13.6029 2.46315 13.9126 2.83575 14.1277C3.07853 14.2679 3.39428 14.3589 3.9256 14.407C4.46628 14.456 5.16176 14.4559 6.14923 14.4559C7.13675 14.4559 7.83218 14.456 8.37286 14.407C8.90419 14.3589 9.21993 14.2679 9.46271 14.1277C9.83529 13.9126 10.145 13.6029 10.3602 13.2303C10.5003 12.9875 10.5913 12.6718 10.6395 12.1404C10.6884 11.5998 10.6883 10.9043 10.6883 9.91681C10.6883 8.92935 10.6884 8.23385 10.6395 7.69318C10.5913 7.16185 10.5003 6.84611 10.3602 6.60333C10.145 6.23072 9.8353 5.92107 9.46271 5.70587C9.21993 5.56574 8.90418 5.47473 8.37286 5.42657C7.83218 5.3776 7.13676 5.37775 6.14923 5.37775ZM9.80157 0.367981C10.7637 0.367981 11.5313 0.367886 12.1473 0.423645C12.7725 0.480313 13.3093 0.598765 13.7928 0.877747C14.3716 1.21192 14.852 1.69355 15.1863 2.27228C15.4655 2.75575 15.5857 3.29165 15.6424 3.91681C15.6982 4.53301 15.6971 5.30161 15.6971 6.26447V7.8299C15.6971 8.29265 15.6989 8.58994 15.6649 8.84845C15.4667 10.3525 14.4009 11.5738 12.9832 11.9988V10.5467C13.6973 10.1903 14.2104 9.49662 14.3192 8.67169C14.3387 8.52348 14.3406 8.3358 14.3406 7.8299V6.26447C14.3406 5.27707 14.3398 4.58149 14.2908 4.04083C14.2427 3.50969 14.1526 3.19373 14.0125 2.95099C13.7974 2.5785 13.4875 2.2687 13.1151 2.05353C12.8723 1.91347 12.5563 1.82237 12.0252 1.77423C11.4846 1.72528 10.7888 1.7254 9.80157 1.7254H7.71466C6.75614 1.72559 5.92659 2.27697 5.52325 3.07892H4.07013C4.54215 1.51132 5.99314 0.368192 7.71466 0.367981H9.80157Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">复制</span></span><div class="ds-focus-ring"></div></button><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M15.3695 11.411L15.1234 12.8866C14.8869 14.3042 13.6603 15.3436 12.223 15.3436H3.7767C2.33954 15.3434 1.11276 14.3042 0.876312 12.8866L0.630219 11.411L2.05405 11.1747L2.29916 12.6493C2.41969 13.3713 3.04472 13.9001 3.7767 13.9003H12.223C12.9551 13.9002 13.58 13.3713 13.7005 12.6493L13.9456 11.1747L15.3695 11.411ZM8.72202 8.994C8.77714 8.93934 8.83789 8.88106 8.90268 8.81627L12.4828 5.23424L13.5042 6.25572L9.92221 9.8358C9.63947 10.1185 9.3876 10.3732 9.15854 10.5575C8.91889 10.7503 8.6395 10.9224 8.28647 10.9784C8.09708 11.0083 7.9036 11.0083 7.7142 10.9784C7.36103 10.9224 7.08087 10.7503 6.84116 10.5575C6.61212 10.3732 6.36019 10.1185 6.07748 9.8358L2.49643 6.25572L3.51694 5.23424L7.09702 8.81627C7.16216 8.88142 7.22327 8.94006 7.27866 8.99498V1.3065H8.72202V8.994Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">下载</span></span><div class="ds-focus-ring"></div></button></div></div></div></div></div><pre><span class="token function selector">\documentclass</span><span class="token punctuation">{</span><span class="token keyword">article</span><span class="token punctuation">}</span>
<span class="token function selector">\usepackage</span><span class="token punctuation">{</span><span class="token keyword">amsmath</span><span class="token punctuation">}</span>
<span class="token function selector">\usepackage</span><span class="token punctuation">{</span><span class="token keyword">booktabs</span><span class="token punctuation">}</span>
<span class="token function selector">\usepackage</span><span class="token punctuation">{</span><span class="token keyword">xcolor</span><span class="token punctuation">}</span>
<span class="token function selector">\usepackage</span><span class="token punctuation">{</span><span class="token keyword">listings</span><span class="token punctuation">}</span>
<span class="token function selector">\usepackage</span><span class="token punctuation">{</span><span class="token keyword">geometry</span><span class="token punctuation">}</span>

<span class="token function selector">\geometry</span><span class="token punctuation">{</span>a4paper, margin=1in<span class="token punctuation">}</span>

<span class="token function selector">\title</span><span class="token punctuation">{</span>CosyVoice 语音合成系统配置分析<span class="token punctuation">}</span>
<span class="token function selector">\author</span><span class="token punctuation">{</span><span class="token punctuation">}</span>
<span class="token function selector">\date</span><span class="token punctuation">{</span><span class="token punctuation">}</span>

<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">document</span><span class="token punctuation">}</span>

<span class="token function selector">\maketitle</span>

<span class="token function selector">\section</span><span class="token punctuation">{</span><span class="token headline class-name">随机种子设置</span><span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">verbatim</span><span class="token punctuation">}</span><span class="token cdata">
__set_seed1-4: 设置所有随机数生成器的种子为1986，确保结果可重现
</span><span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">verbatim</span><span class="token punctuation">}</span>

<span class="token function selector">\section</span><span class="token punctuation">{</span><span class="token headline class-name">基础参数配置</span><span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">table</span><span class="token punctuation">}</span><span class="token punctuation">[</span>h<span class="token punctuation">]</span>
<span class="token function selector">\centering</span>
<span class="token function selector">\caption</span><span class="token punctuation">{</span>基础参数设置<span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">tabular</span><span class="token punctuation">}</span><span class="token punctuation">{</span>ll<span class="token punctuation">}</span>
<span class="token function selector">\toprule</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>参数<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>值<span class="token punctuation">}</span> <span class="token function selector">\\</span>
<span class="token function selector">\midrule</span>
音频采样率 <span class="token punctuation">&amp;</span> 22050 <span class="token function selector">\\</span>
文本编码器输入维度 <span class="token punctuation">&amp;</span> 512 <span class="token function selector">\\</span>
大语言模型输入维度 <span class="token punctuation">&amp;</span> 1024 <span class="token function selector">\\</span>
大语言模型输出维度 <span class="token punctuation">&amp;</span> 1024 <span class="token function selector">\\</span>
说话人嵌入维度 <span class="token punctuation">&amp;</span> 192 <span class="token function selector">\\</span>
<span class="token function selector">\bottomrule</span>
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">tabular</span><span class="token punctuation">}</span>
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">table</span><span class="token punctuation">}</span>

<span class="token function selector">\section</span><span class="token punctuation">{</span><span class="token headline class-name">核心模型架构</span><span class="token punctuation">}</span>

<span class="token function selector">\subsection</span><span class="token punctuation">{</span><span class="token headline class-name">LLM (大语言模型)</span><span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">verbatim</span><span class="token punctuation">}</span><span class="token cdata">
llm: !new:cosyvoice.llm.llm.TransformerLM
</span><span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">verbatim</span><span class="token punctuation">}</span>

<span class="token function selector">\textbf</span><span class="token punctuation">{</span>架构特性：<span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>文本编码器<span class="token punctuation">}</span>: 6层 Conformer 编码器，使用相对位置编码
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>LLM主体<span class="token punctuation">}</span>: 14层 Transformer 编码器
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>词汇表大小<span class="token punctuation">}</span>: 文本 51866，语音 4096
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>采样策略<span class="token punctuation">}</span>: 使用 RAS (top<span class="token function selector">\_</span>p=0.8, top<span class="token function selector">\_</span>k=25)
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\subsection</span><span class="token punctuation">{</span><span class="token headline class-name">Flow 模型 (语音生成)</span><span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">verbatim</span><span class="token punctuation">}</span><span class="token cdata">
flow: !new:cosyvoice.flow.flow.MaskedDiffWithXvec
</span><span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">verbatim</span><span class="token punctuation">}</span>

<span class="token function selector">\textbf</span><span class="token punctuation">{</span>架构特性：<span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>编码器<span class="token punctuation">}</span>: 6层 Conformer 编码器
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>长度调节器<span class="token punctuation">}</span>: 插值调节器，支持多尺度
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>解码器<span class="token punctuation">}</span>: 条件流匹配 (Conditional CFM)
    <span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
        <span class="token function selector">\item</span> 使用 Euler 求解器
        <span class="token function selector">\item</span> 余弦时间调度
        <span class="token function selector">\item</span> L1 正则化损失
    <span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\subsection</span><span class="token punctuation">{</span><span class="token headline class-name">HiFT 声码器</span><span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">verbatim</span><span class="token punctuation">}</span><span class="token cdata">
hift: !new:cosyvoice.hifigan.generator.HiFTGenerator
</span><span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">verbatim</span><span class="token punctuation">}</span>

<span class="token function selector">\textbf</span><span class="token punctuation">{</span>架构特性：<span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> 基于 HiFi-GAN 的生成器
    <span class="token function selector">\item</span> 包含谐波合成滤波器
    <span class="token function selector">\item</span> 集成 F0 预测器 (ConvRNN)
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\section</span><span class="token punctuation">{</span><span class="token headline class-name">训练配置</span><span class="token punctuation">}</span>

<span class="token function selector">\subsection</span><span class="token punctuation">{</span><span class="token headline class-name">LLM + Flow 训练</span><span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">table</span><span class="token punctuation">}</span><span class="token punctuation">[</span>h<span class="token punctuation">]</span>
<span class="token function selector">\centering</span>
<span class="token function selector">\caption</span><span class="token punctuation">{</span>LLM + Flow 训练参数<span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">tabular</span><span class="token punctuation">}</span><span class="token punctuation">{</span>ll<span class="token punctuation">}</span>
<span class="token function selector">\toprule</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>参数<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>值<span class="token punctuation">}</span> <span class="token function selector">\\</span>
<span class="token function selector">\midrule</span>
优化器 <span class="token punctuation">&amp;</span> adam <span class="token function selector">\\</span>
学习率 <span class="token punctuation">&amp;</span> 0.001 <span class="token function selector">\\</span>
学习率调度器 <span class="token punctuation">&amp;</span> warmuplr <span class="token function selector">\\</span>
预热步数 <span class="token punctuation">&amp;</span> 2500 <span class="token function selector">\\</span>
最大训练轮数 <span class="token punctuation">&amp;</span> 200 <span class="token function selector">\\</span>
梯度裁剪 <span class="token punctuation">&amp;</span> 5 <span class="token function selector">\\</span>
梯度累积步数 <span class="token punctuation">&amp;</span> 2 <span class="token function selector">\\</span>
<span class="token function selector">\bottomrule</span>
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">tabular</span><span class="token punctuation">}</span>
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">table</span><span class="token punctuation">}</span>

<span class="token function selector">\subsection</span><span class="token punctuation">{</span><span class="token headline class-name">GAN 训练</span><span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">table</span><span class="token punctuation">}</span><span class="token punctuation">[</span>h<span class="token punctuation">]</span>
<span class="token function selector">\centering</span>
<span class="token function selector">\caption</span><span class="token punctuation">{</span>GAN 训练参数<span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">tabular</span><span class="token punctuation">}</span><span class="token punctuation">{</span>ll<span class="token punctuation">}</span>
<span class="token function selector">\toprule</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>参数<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>值<span class="token punctuation">}</span> <span class="token function selector">\\</span>
<span class="token function selector">\midrule</span>
学习率 <span class="token punctuation">&amp;</span> 0.0002 <span class="token function selector">\\</span>
梯度累积步数 <span class="token punctuation">&amp;</span> 1 <span class="token function selector">\\</span>
<span class="token function selector">\bottomrule</span>
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">tabular</span><span class="token punctuation">}</span>
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">table</span><span class="token punctuation">}</span>

<span class="token function selector">\section</span><span class="token punctuation">{</span><span class="token headline class-name">数据处理流水线</span><span class="token punctuation">}</span>

<span class="token function selector">\subsection</span><span class="token punctuation">{</span><span class="token headline class-name">主要数据处理流水线</span><span class="token punctuation">}</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>处理流程：<span class="token punctuation">}</span>
<span class="token equation string">\[
<span class="token equation-command regex">\text</span>{打开parquet文件} <span class="token equation-command regex">\rightarrow</span> <span class="token equation-command regex">\text</span>{文本tokenize} <span class="token equation-command regex">\rightarrow</span> <span class="token equation-command regex">\text</span>{过滤长短样本} <span class="token equation-command regex">\rightarrow</span> <span class="token equation-command regex">\text</span>{音频重采样} 
\]</span>
<span class="token equation string">\[
<span class="token equation-command regex">\rightarrow</span> <span class="token equation-command regex">\text</span>{计算Fbank特征} <span class="token equation-command regex">\rightarrow</span> <span class="token equation-command regex">\text</span>{解析说话人嵌入} <span class="token equation-command regex">\rightarrow</span> <span class="token equation-command regex">\text</span>{洗牌} <span class="token equation-command regex">\rightarrow</span> <span class="token equation-command regex">\text</span>{排序} <span class="token equation-command regex">\rightarrow</span> <span class="token equation-command regex">\text</span>{批处理} <span class="token equation-command regex">\rightarrow</span> <span class="token equation-command regex">\text</span>{填充}
\]</span>

<span class="token function selector">\subsection</span><span class="token punctuation">{</span><span class="token headline class-name">GAN专用流水线</span><span class="token punctuation">}</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>额外处理步骤：<span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\texttt</span><span class="token punctuation">{</span>truncate<span class="token punctuation">}</span>: 截断音频到固定长度
    <span class="token function selector">\item</span> <span class="token function selector">\texttt</span><span class="token punctuation">{</span>compute<span class="token function selector">\_</span>f0<span class="token punctuation">}</span>: 计算基频特征
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\section</span><span class="token punctuation">{</span><span class="token headline class-name">关键特性分析</span><span class="token punctuation">}</span>

<span class="token function selector">\subsection</span><span class="token punctuation">{</span><span class="token headline class-name">模型特点</span><span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>多尺度处理<span class="token punctuation">}</span>: 支持4种采样比例的长度调节
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>条件生成<span class="token punctuation">}</span>: 使用说话人嵌入进行个性化合成
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>流匹配<span class="token punctuation">}</span>: 采用先进的流匹配技术替代传统扩散
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>端到端训练<span class="token punctuation">}</span>: 支持从文本到语音的完整流程
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\subsection</span><span class="token punctuation">{</span><span class="token headline class-name">技术亮点</span><span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>相对位置编码<span class="token punctuation">}</span>: 更好的长度外推能力
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>动态批处理<span class="token punctuation">}</span>: 根据帧数动态调整批次大小
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>多判别器<span class="token punctuation">}</span>: MPD + MRD 组合提升生成质量
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>灵活的采样策略<span class="token punctuation">}</span>: 支持多种解码策略
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\subsection</span><span class="token punctuation">{</span><span class="token headline class-name">可调整参数</span><span class="token punctuation">}</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>配置中标注的重要可调整点：<span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> 词汇表大小 (300M参数版本需要调整)
    <span class="token function selector">\item</span> 帧率 (25Hz或50Hz)
    <span class="token function selector">\item</span> 学习率策略 (SFT时使用常量学习率)
    <span class="token function selector">\item</span> 说话人嵌入 (SFT时启用)
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\section</span><span class="token punctuation">{</span><span class="token headline class-name">系统架构总结</span><span class="token punctuation">}</span>

该配置展现了一个现代化的端到端语音合成系统，具有以下技术特点：

<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>先进架构<span class="token punctuation">}</span>: 结合大语言模型、流匹配和对抗训练等先进技术
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>模块化设计<span class="token punctuation">}</span>: 各组件清晰分离，便于维护和扩展
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>生产就绪<span class="token punctuation">}</span>: 包含完整的训练流水线和推理配置
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>灵活性<span class="token punctuation">}</span>: 支持多种使用场景和参数调整
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

该系统代表了当前语音合成领域的技术前沿，为高质量、可控的语音生成提供了完整的解决方案。

<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">document</span><span class="token punctuation">}</span></pre><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _33882ae"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _28d7e84"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg></div>

---

### 用户

#!/bin/bash
# Copyright 2024 Alibaba Inc. All Rights Reserved.
. ./path.sh || exit 1;

stage=5
stop_stage=7

data_url=http://openslr.magicdatatech.com/resources/60
data_dir=/home/redacted_student_a/data
pretrained_model_dir=/home/redacted_student_a/CosyVoice/pretrained_models/CosyVoice-300M

if [ ${stage} -le -1 ] && [ ${stop_stage} -ge -1 ]; then
  echo "Data Download"
  for part in train-clean-100 dev-clean test-clean dev-other test-other; do
    local/download_and_untar.sh ${data_dir} ${data_url} ${part}
  done
fi

if [ ${stage} -le 0 ] && [ ${stop_stage} -ge 0 ]; then
  echo "Data preparation, prepare wav.scp/text/utt2spk/spk2utt"
  for x in train-clean-100 dev-clean dev-other test-clean test-other; do
    mkdir -p data/$x
    python local/prepare_data.py --src_dir $data_dir/LibriTTS/$x --des_dir data/$x
  done
fi

if [ ${stage} -le 1 ] && [ ${stop_stage} -ge 1 ]; then
  echo "Extract campplus speaker embedding, you will get spk2embedding.pt and utt2embedding.pt in data/$x dir"
  for x in train-clean-100 dev-clean dev-other test-clean test-other; do
    tools/extract_embedding.py --dir data/$x \
      --onnx_path $pretrained_model_dir/campplus.onnx
  done
fi

if [ ${stage} -le 2 ] && [ ${stop_stage} -ge 2 ]; then
  echo "Extract discrete speech token, you will get utt2speech_token.pt in data/$x dir"
  for x in train-clean-100 dev-clean dev-other test-clean test-other; do
    tools/extract_speech_token.py --dir data/$x \
      --onnx_path $pretrained_model_dir/speech_tokenizer_v1.onnx
  done
fi

if [ ${stage} -le 3 ] && [ ${stop_stage} -ge 3 ]; then
  echo "Prepare required parquet format data, you should have prepared wav.scp/text/utt2spk/spk2utt/utt2embedding.pt/spk2embedding.pt/utt2speech_token.pt"
  for x in train-clean-100 dev-clean dev-other test-clean test-other; do
    mkdir -p data/$x/parquet
    tools/make_parquet_list.py --num_utts_per_parquet 1000 \
      --num_processes 10 \
      --src_dir data/$x \
      --des_dir data/$x/parquet
  done
fi

# train llm
export CUDA_VISIBLE_DEVICES="0"
num_gpus=$(echo $CUDA_VISIBLE_DEVICES | awk -F "," '{print NF}')
job_id=1986
dist_backend="nccl"
num_workers=2
prefetch=100
train_engine=torch_ddp
if [ ${stage} -le 5 ] && [ ${stop_stage} -ge 5 ]; then
  echo "Run train. We only support llm traning for now"
  if [ $train_engine == 'deepspeed' ]; then
    echo "Notice deepspeed has its own optimizer config. Modify conf/ds_stage2.json if necessary"
  fi
  cat data/train-clean-100/parquet/data.list > data/train.data.list
  cat data/dev-clean/parquet/data.list data/dev-other/parquet/data.list > data/dev.data.list
  for model in llm flow hifigan; do
    torchrun --nnodes=1 --nproc_per_node=$num_gpus \
        --rdzv_id=$job_id --rdzv_backend="c10d" --rdzv_endpoint="localhost:1234" \
      cosyvoice/bin/train.py \
      --train_engine $train_engine \
      --config conf/cosyvoice.yaml \
      --train_data data/train.data.list \
      --cv_data data/dev.data.list \
      --model $model \
      --checkpoint $pretrained_model_dir/$model.pt \
      --model_dir `pwd`/exp/cosyvoice/$model/$train_engine \
      --tensorboard_dir `pwd`/tensorboard/cosyvoice/$model/$train_engine \
      --ddp.dist_backend $dist_backend \
      --num_workers ${num_workers} \
      --prefetch ${prefetch} \
      --pin_memory \
      --use_amp \
      --deepspeed_config ./conf/ds_stage2.json \
      --deepspeed.save_states model+optimizer
  done
fi

# average model
average_num=5
if [ ${stage} -le 6 ] && [ ${stop_stage} -ge 6 ]; then
  for model in llm flow hifigan; do
    decode_checkpoint=`pwd`/exp/cosyvoice/$model/$train_engine/${model}.pt
    echo "do model average and final checkpoint is $decode_checkpoint"
    python cosyvoice/bin/average_model.py \
      --dst_model $decode_checkpoint \
      --src_path `pwd`/exp/cosyvoice/$model/$train_engine  \
      --num ${average_num} \
      --val_best
  done
fi

if [ ${stage} -le 7 ] && [ ${stop_stage} -ge 7 ]; then
  echo "Export your model for inference speedup. Remember copy your llm or flow model to model_dir"
  python cosyvoice/bin/export_jit.py --model_dir $pretrained_model_dir
  python cosyvoice/bin/export_onnx.py --model_dir $pretrained_model_dir
fi详细解释cosyvoice的训练脚本

---

### DeepSeek AI

<p>思考：</p><blockquote><p class="ds-markdown-paragraph"><span>我们有一个CosyVoice的训练脚本，它包含了多个阶段，从数据下载到模型训练和导出。下面我将详细解释每个阶段的作用。</span></p><p class="ds-markdown-paragraph"><span>脚本变量说明：</span><br><span>stage: 开始阶段</span><br><span>stop_stage: 结束阶段</span><br><span>data_url: 数据下载地址</span><br><span>data_dir: 数据存储目录</span><br><span>pretrained_model_dir: 预训练模型目录</span></p><p class="ds-markdown-paragraph"><span>阶段说明：</span><br><span>-1: 数据下载</span><br><span>0: 数据准备，生成wav.scp, text, utt2spk, spk2utt</span><br><span>1: 提取campplus说话人嵌入，得到</span><span>spk2embedding.pt</span><span>和</span><span>utt2embedding.pt</span><span></span><br><span>2: 提取离散语音令牌，得到utt2speech_</span><span>token.pt</span><span></span><br><span>3: 准备parquet格式数据，将数据分成多个parquet文件，每个文件包含1000个语句，使用10个进程</span><br><span>5: 训练模型（LLM、Flow、HiFT声码器）</span><br><span>6: 模型平均，取最后5个检查点平均</span><br><span>7: 导出模型为JIT和ONNX格式，用于推理加速</span></p><p class="ds-markdown-paragraph"><span>训练部分详细说明：</span><br><span>使用torchrun进行分布式训练，默认使用GPU0。</span><br><span>训练引擎可以是torch_ddp或deepspeed。</span><br><span>训练数据是train-clean-100，验证数据是dev-clean和dev-other。</span><br><span>训练三个模型：llm, flow, hifigan，依次训练。</span></p><p class="ds-markdown-paragraph"><span>注意：在训练之前，需要准备好预训练模型，因为训练时使用预训练模型初始化。</span></p><p class="ds-markdown-paragraph"><span>现在，我们将按照阶段顺序详细解释。</span></p></blockquote><br/><div class="md-code-block md-code-block-light"><div class="md-code-block-banner-wrap"><div class="md-code-block-banner md-code-block-banner-lite"><div class="_121d384"><div class="d2a24f03"><span class="d813de27">latex</span></div><div class="d2a24f03 _246a029"><div class="efa13877"><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon" style="margin-right: 4px;"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.14923 4.02032C7.11191 4.02032 7.87977 4.02017 8.49591 4.07599C9.12122 4.1327 9.65786 4.25188 10.1414 4.53107C10.7201 4.8653 11.2008 5.34591 11.535 5.92462C11.8142 6.40818 11.9333 6.94482 11.9901 7.57013C12.0459 8.18625 12.0457 8.9542 12.0457 9.91681C12.0457 10.8795 12.0459 11.6474 11.9901 12.2635C11.9333 12.8888 11.8142 13.4254 11.535 13.909C11.2008 14.4877 10.7201 14.9683 10.1414 15.3026C9.65786 15.5817 9.12122 15.7009 8.49591 15.7576C7.87977 15.8134 7.1119 15.8133 6.14923 15.8133C5.18661 15.8133 4.41868 15.8134 3.80255 15.7576C3.17724 15.7009 2.6406 15.5817 2.15704 15.3026C1.57834 14.9684 1.09772 14.4877 0.763489 13.909C0.484305 13.4254 0.365123 12.8888 0.308411 12.2635C0.252587 11.6474 0.252747 10.8795 0.252747 9.91681C0.252747 8.95419 0.252603 8.18625 0.308411 7.57013C0.365123 6.94482 0.484305 6.40818 0.763489 5.92462C1.09771 5.3459 1.57833 4.86529 2.15704 4.53107C2.6406 4.25188 3.17724 4.1327 3.80255 4.07599C4.41868 4.02018 5.1866 4.02032 6.14923 4.02032ZM6.14923 5.37775C5.16175 5.37775 4.46628 5.37761 3.9256 5.42657C3.39428 5.47473 3.07853 5.56574 2.83575 5.70587C2.46313 5.92106 2.15348 6.23071 1.93829 6.60333C1.79817 6.84611 1.70715 7.16185 1.659 7.69318C1.61004 8.23385 1.61017 8.92934 1.61017 9.91681C1.61017 10.9043 1.61002 11.5998 1.659 12.1404C1.70715 12.6717 1.79817 12.9875 1.93829 13.2303C2.15349 13.6029 2.46315 13.9126 2.83575 14.1277C3.07853 14.2679 3.39428 14.3589 3.9256 14.407C4.46628 14.456 5.16176 14.4559 6.14923 14.4559C7.13675 14.4559 7.83218 14.456 8.37286 14.407C8.90419 14.3589 9.21993 14.2679 9.46271 14.1277C9.83529 13.9126 10.145 13.6029 10.3602 13.2303C10.5003 12.9875 10.5913 12.6718 10.6395 12.1404C10.6884 11.5998 10.6883 10.9043 10.6883 9.91681C10.6883 8.92935 10.6884 8.23385 10.6395 7.69318C10.5913 7.16185 10.5003 6.84611 10.3602 6.60333C10.145 6.23072 9.8353 5.92107 9.46271 5.70587C9.21993 5.56574 8.90418 5.47473 8.37286 5.42657C7.83218 5.3776 7.13676 5.37775 6.14923 5.37775ZM9.80157 0.367981C10.7637 0.367981 11.5313 0.367886 12.1473 0.423645C12.7725 0.480313 13.3093 0.598765 13.7928 0.877747C14.3716 1.21192 14.852 1.69355 15.1863 2.27228C15.4655 2.75575 15.5857 3.29165 15.6424 3.91681C15.6982 4.53301 15.6971 5.30161 15.6971 6.26447V7.8299C15.6971 8.29265 15.6989 8.58994 15.6649 8.84845C15.4667 10.3525 14.4009 11.5738 12.9832 11.9988V10.5467C13.6973 10.1903 14.2104 9.49662 14.3192 8.67169C14.3387 8.52348 14.3406 8.3358 14.3406 7.8299V6.26447C14.3406 5.27707 14.3398 4.58149 14.2908 4.04083C14.2427 3.50969 14.1526 3.19373 14.0125 2.95099C13.7974 2.5785 13.4875 2.2687 13.1151 2.05353C12.8723 1.91347 12.5563 1.82237 12.0252 1.77423C11.4846 1.72528 10.7888 1.7254 9.80157 1.7254H7.71466C6.75614 1.72559 5.92659 2.27697 5.52325 3.07892H4.07013C4.54215 1.51132 5.99314 0.368192 7.71466 0.367981H9.80157Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">复制</span></span><div class="ds-focus-ring"></div></button><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M15.3695 11.411L15.1234 12.8866C14.8869 14.3042 13.6603 15.3436 12.223 15.3436H3.7767C2.33954 15.3434 1.11276 14.3042 0.876312 12.8866L0.630219 11.411L2.05405 11.1747L2.29916 12.6493C2.41969 13.3713 3.04472 13.9001 3.7767 13.9003H12.223C12.9551 13.9002 13.58 13.3713 13.7005 12.6493L13.9456 11.1747L15.3695 11.411ZM8.72202 8.994C8.77714 8.93934 8.83789 8.88106 8.90268 8.81627L12.4828 5.23424L13.5042 6.25572L9.92221 9.8358C9.63947 10.1185 9.3876 10.3732 9.15854 10.5575C8.91889 10.7503 8.6395 10.9224 8.28647 10.9784C8.09708 11.0083 7.9036 11.0083 7.7142 10.9784C7.36103 10.9224 7.08087 10.7503 6.84116 10.5575C6.61212 10.3732 6.36019 10.1185 6.07748 9.8358L2.49643 6.25572L3.51694 5.23424L7.09702 8.81627C7.16216 8.88142 7.22327 8.94006 7.27866 8.99498V1.3065H8.72202V8.994Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">下载</span></span><div class="ds-focus-ring"></div></button></div></div></div></div></div><pre><span class="token function selector">\documentclass</span><span class="token punctuation">{</span><span class="token keyword">article</span><span class="token punctuation">}</span>
<span class="token function selector">\usepackage</span><span class="token punctuation">{</span><span class="token keyword">amsmath</span><span class="token punctuation">}</span>
<span class="token function selector">\usepackage</span><span class="token punctuation">{</span><span class="token keyword">booktabs</span><span class="token punctuation">}</span>
<span class="token function selector">\usepackage</span><span class="token punctuation">{</span><span class="token keyword">xcolor</span><span class="token punctuation">}</span>
<span class="token function selector">\usepackage</span><span class="token punctuation">{</span><span class="token keyword">listings</span><span class="token punctuation">}</span>
<span class="token function selector">\usepackage</span><span class="token punctuation">{</span><span class="token keyword">geometry</span><span class="token punctuation">}</span>
<span class="token function selector">\usepackage</span><span class="token punctuation">{</span><span class="token keyword">xparse</span><span class="token punctuation">}</span>

<span class="token function selector">\geometry</span><span class="token punctuation">{</span>a4paper, margin=1in<span class="token punctuation">}</span>

<span class="token function selector">\title</span><span class="token punctuation">{</span>CosyVoice 训练脚本详细解析<span class="token punctuation">}</span>
<span class="token function selector">\author</span><span class="token punctuation">{</span><span class="token punctuation">}</span>
<span class="token function selector">\date</span><span class="token punctuation">{</span><span class="token punctuation">}</span>

<span class="token function selector">\lstset</span><span class="token punctuation">{</span>
    basicstyle=<span class="token function selector">\ttfamily</span><span class="token function selector">\small</span>,
    breaklines=true,
    frame=single,
    numbers=left,
    numberstyle=<span class="token function selector">\tiny</span>,
    keywordstyle=<span class="token function selector">\color</span><span class="token punctuation">{</span>blue<span class="token punctuation">}</span>,
    commentstyle=<span class="token function selector">\color</span><span class="token punctuation">{</span>gray<span class="token punctuation">}</span>,
    stringstyle=<span class="token function selector">\color</span><span class="token punctuation">{</span>red<span class="token punctuation">}</span>
<span class="token punctuation">}</span>

<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">document</span><span class="token punctuation">}</span>

<span class="token function selector">\maketitle</span>

<span class="token function selector">\section</span><span class="token punctuation">{</span><span class="token headline class-name">脚本概述</span><span class="token punctuation">}</span>

这是一个完整的 CosyVoice 语音合成系统训练脚本，采用 Bash 脚本编写。脚本采用阶段式设计，支持从数据准备到模型导出的完整流程。

<span class="token function selector">\section</span><span class="token punctuation">{</span><span class="token headline class-name">全局配置参数</span><span class="token punctuation">}</span>

<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">table</span><span class="token punctuation">}</span><span class="token punctuation">[</span>h<span class="token punctuation">]</span>
<span class="token function selector">\centering</span>
<span class="token function selector">\caption</span><span class="token punctuation">{</span>全局配置参数<span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">tabular</span><span class="token punctuation">}</span><span class="token punctuation">{</span>llp<span class="token punctuation">{</span>8cm<span class="token punctuation">}</span><span class="token punctuation">}</span>
<span class="token function selector">\toprule</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>参数<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>值<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>说明<span class="token punctuation">}</span> <span class="token function selector">\\</span>
<span class="token function selector">\midrule</span>
stage <span class="token punctuation">&amp;</span> 5 <span class="token punctuation">&amp;</span> 开始执行的阶段编号 <span class="token function selector">\\</span>
stop<span class="token function selector">\_</span>stage <span class="token punctuation">&amp;</span> 7 <span class="token punctuation">&amp;</span> 结束执行的阶段编号 <span class="token function selector">\\</span>
data<span class="token function selector">\_</span>url <span class="token punctuation">&amp;</span> http://openslr.magicdatatech.com/resources/60 <span class="token punctuation">&amp;</span> LibriTTS 数据集下载地址 <span class="token function selector">\\</span>
data<span class="token function selector">\_</span>dir <span class="token punctuation">&amp;</span> /home/redacted_student_a/data <span class="token punctuation">&amp;</span> 数据存储根目录 <span class="token function selector">\\</span>
pretrained<span class="token function selector">\_</span>model<span class="token function selector">\_</span>dir <span class="token punctuation">&amp;</span> /home/redacted_student_a/CosyVoice/pretrained<span class="token function selector">\_</span>models/CosyVoice-300M <span class="token punctuation">&amp;</span> 预训练模型目录 <span class="token function selector">\\</span>
<span class="token function selector">\bottomrule</span>
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">tabular</span><span class="token punctuation">}</span>
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">table</span><span class="token punctuation">}</span>

<span class="token function selector">\section</span><span class="token punctuation">{</span><span class="token headline class-name">阶段详解</span><span class="token punctuation">}</span>

<span class="token function selector">\subsection</span><span class="token punctuation">{</span><span class="token headline class-name">阶段 -1: 数据下载</span><span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">lstlisting</span><span class="token punctuation">}</span><span class="token cdata">[language=bash]
if [ ${stage} -le -1 ] &amp;&amp; [ ${stop_stage} -ge -1 ]; then
  echo "Data Download"
  for part in train-clean-100 dev-clean test-clean dev-other test-other; do
    local/download_and_untar.sh ${data_dir} ${data_url} ${part}
  done
fi
</span><span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">lstlisting</span><span class="token punctuation">}</span>

<span class="token function selector">\textbf</span><span class="token punctuation">{</span>功能：<span class="token punctuation">}</span> 下载 LibriTTS 数据集的所有必要部分：
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> train-clean-100: 训练集（100小时干净语音）
    <span class="token function selector">\item</span> dev-clean: 开发集（干净语音）
    <span class="token function selector">\item</span> test-clean: 测试集（干净语音）
    <span class="token function selector">\item</span> dev-other: 开发集（其他语音）
    <span class="token function selector">\item</span> test-other: 测试集（其他语音）
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\subsection</span><span class="token punctuation">{</span><span class="token headline class-name">阶段 0: 数据准备</span><span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">lstlisting</span><span class="token punctuation">}</span><span class="token cdata">[language=bash]
if [ ${stage} -le 0 ] &amp;&amp; [ ${stop_stage} -ge 0 ]; then
  echo "Data preparation, prepare wav.scp/text/utt2spk/spk2utt"
  for x in train-clean-100 dev-clean dev-other test-clean test-other; do
    mkdir -p data/$x
    python local/prepare_data.py --src_dir $data_dir/LibriTTS/$x --des_dir data/$x
  done
fi
</span><span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">lstlisting</span><span class="token punctuation">}</span>

<span class="token function selector">\textbf</span><span class="token punctuation">{</span>功能：<span class="token punctuation">}</span> 准备 Kaldi 格式的数据文件：
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\texttt</span><span class="token punctuation">{</span>wav.scp<span class="token punctuation">}</span>: 音频文件路径映射
    <span class="token function selector">\item</span> <span class="token function selector">\texttt</span><span class="token punctuation">{</span>text<span class="token punctuation">}</span>: 文本转录
    <span class="token function selector">\item</span> <span class="token function selector">\texttt</span><span class="token punctuation">{</span>utt2spk<span class="token punctuation">}</span>: 语句到说话人映射
    <span class="token function selector">\item</span> <span class="token function selector">\texttt</span><span class="token punctuation">{</span>spk2utt<span class="token punctuation">}</span>: 说话人到语句映射
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\subsection</span><span class="token punctuation">{</span><span class="token headline class-name">阶段 1: 说话人嵌入提取</span><span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">lstlisting</span><span class="token punctuation">}</span><span class="token cdata">[language=bash]
if [ ${stage} -le 1 ] &amp;&amp; [ ${stop_stage} -ge 1 ]; then
  echo "Extract campplus speaker embedding, you will get spk2embedding.pt and utt2embedding.pt in data/$x dir"
  for x in train-clean-100 dev-clean dev-other test-clean test-other; do
    tools/extract_embedding.py --dir data/$x \
      --onnx_path $pretrained_model_dir/campplus.onnx
  done
fi
</span><span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">lstlisting</span><span class="token punctuation">}</span>

<span class="token function selector">\textbf</span><span class="token punctuation">{</span>功能：<span class="token punctuation">}</span> 使用 CAMPPlus 模型提取说话人嵌入：
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\texttt</span><span class="token punctuation">{</span>spk2embedding.pt<span class="token punctuation">}</span>: 说话人级别的嵌入向量
    <span class="token function selector">\item</span> <span class="token function selector">\texttt</span><span class="token punctuation">{</span>utt2embedding.pt<span class="token punctuation">}</span>: 语句级别的嵌入向量
    <span class="token function selector">\item</span> 使用 ONNX 格式的预训练模型进行推理
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\subsection</span><span class="token punctuation">{</span><span class="token headline class-name">阶段 2: 语音令牌提取</span><span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">lstlisting</span><span class="token punctuation">}</span><span class="token cdata">[language=bash]
if [ ${stage} -le 2 ] &amp;&amp; [ ${stop_stage} -ge 2 ]; then
  echo "Extract discrete speech token, you will get utt2speech_token.pt in data/$x dir"
  for x in train-clean-100 dev-clean dev-other test-clean test-other; do
    tools/extract_speech_token.py --dir data/$x \
      --onnx_path $pretrained_model_dir/speech_tokenizer_v1.onnx
  done
fi
</span><span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">lstlisting</span><span class="token punctuation">}</span>

<span class="token function selector">\textbf</span><span class="token punctuation">{</span>功能：<span class="token punctuation">}</span> 提取离散语音令牌：
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\texttt</span><span class="token punctuation">{</span>utt2speech<span class="token function selector">\_</span>token.pt<span class="token punctuation">}</span>: 每个语句的语音令牌序列
    <span class="token function selector">\item</span> 为后续的 LLM 训练提供目标输出
    <span class="token function selector">\item</span> 使用专门的语音令牌化器模型
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\subsection</span><span class="token punctuation">{</span><span class="token headline class-name">阶段 3: Parquet 格式转换</span><span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">lstlisting</span><span class="token punctuation">}</span><span class="token cdata">[language=bash]
if [ ${stage} -le 3 ] &amp;&amp; [ ${stop_stage} -ge 3 ]; then
  echo "Prepare required parquet format data, you should have prepared wav.scp/text/utt2spk/spk2utt/utt2embedding.pt/spk2embedding.pt/utt2speech_token.pt"
  for x in train-clean-100 dev-clean dev-other test-clean test-other; do
    mkdir -p data/$x/parquet
    tools/make_parquet_list.py --num_utts_per_parquet 1000 \
      --num_processes 10 \
      --src_dir data/$x \
      --des_dir data/$x/parquet
  done
fi
</span><span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">lstlisting</span><span class="token punctuation">}</span>

<span class="token function selector">\textbf</span><span class="token punctuation">{</span>功能：<span class="token punctuation">}</span> 转换为高效的 Parquet 格式：
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> 每个 Parquet 文件包含 1000 个语句
    <span class="token function selector">\item</span> 使用 10 个进程并行处理
    <span class="token function selector">\item</span> 提高数据加载效率，支持大规模训练
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\section</span><span class="token punctuation">{</span><span class="token headline class-name">训练环境配置</span><span class="token punctuation">}</span>

<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">table</span><span class="token punctuation">}</span><span class="token punctuation">[</span>h<span class="token punctuation">]</span>
<span class="token function selector">\centering</span>
<span class="token function selector">\caption</span><span class="token punctuation">{</span>训练环境配置<span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">tabular</span><span class="token punctuation">}</span><span class="token punctuation">{</span>llp<span class="token punctuation">{</span>8cm<span class="token punctuation">}</span><span class="token punctuation">}</span>
<span class="token function selector">\toprule</span>
<span class="token function selector">\textbf</span><span class="token punctuation">{</span>参数<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>值<span class="token punctuation">}</span> <span class="token punctuation">&amp;</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>说明<span class="token punctuation">}</span> <span class="token function selector">\\</span>
<span class="token function selector">\midrule</span>
CUDA<span class="token function selector">\_</span>VISIBLE<span class="token function selector">\_</span>DEVICES <span class="token punctuation">&amp;</span> "0" <span class="token punctuation">&amp;</span> 使用 GPU 0 进行训练 <span class="token function selector">\\</span>
num<span class="token function selector">\_</span>gpus <span class="token punctuation">&amp;</span> 1 <span class="token punctuation">&amp;</span> 使用的 GPU 数量 <span class="token function selector">\\</span>
job<span class="token function selector">\_</span>id <span class="token punctuation">&amp;</span> 1986 <span class="token punctuation">&amp;</span> 分布式训练任务 ID <span class="token function selector">\\</span>
dist<span class="token function selector">\_</span>backend <span class="token punctuation">&amp;</span> "nccl" <span class="token punctuation">&amp;</span> 分布式训练后端 <span class="token function selector">\\</span>
num<span class="token function selector">\_</span>workers <span class="token punctuation">&amp;</span> 2 <span class="token punctuation">&amp;</span> 数据加载工作进程数 <span class="token function selector">\\</span>
prefetch <span class="token punctuation">&amp;</span> 100 <span class="token punctuation">&amp;</span> 数据预取数量 <span class="token function selector">\\</span>
train<span class="token function selector">\_</span>engine <span class="token punctuation">&amp;</span> torch<span class="token function selector">\_</span>ddp <span class="token punctuation">&amp;</span> 训练引擎（可选 deepspeed） <span class="token function selector">\\</span>
<span class="token function selector">\bottomrule</span>
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">tabular</span><span class="token punctuation">}</span>
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">table</span><span class="token punctuation">}</span>

<span class="token function selector">\section</span><span class="token punctuation">{</span><span class="token headline class-name">阶段 5: 模型训练</span><span class="token punctuation">}</span>

<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">lstlisting</span><span class="token punctuation">}</span><span class="token cdata">[language=bash]
if [ ${stage} -le 5 ] &amp;&amp; [ ${stop_stage} -ge 5 ]; then
  echo "Run train. We only support llm traning for now"
  if [ $train_engine == 'deepspeed' ]; then
    echo "Notice deepspeed has its own optimizer config. Modify conf/ds_stage2.json if necessary"
  fi
  cat data/train-clean-100/parquet/data.list &gt; data/train.data.list
  cat data/dev-clean/parquet/data.list data/dev-other/parquet/data.list &gt; data/dev.data.list
  for model in llm flow hifigan; do
    torchrun --nnodes=1 --nproc_per_node=$num_gpus \
        --rdzv_id=$job_id --rdzv_backend="c10d" --rdzv_endpoint="localhost:1234" \
      cosyvoice/bin/train.py \
      --train_engine $train_engine \
      --config conf/cosyvoice.yaml \
      --train_data data/train.data.list \
      --cv_data data/dev.data.list \
      --model $model \
      --checkpoint $pretrained_model_dir/$model.pt \
      --model_dir `pwd`/exp/cosyvoice/$model/$train_engine \
      --tensorboard_dir `pwd`/tensorboard/cosyvoice/$model/$train_engine \
      --ddp.dist_backend $dist_backend \
      --num_workers ${num_workers} \
      --prefetch ${prefetch} \
      --pin_memory \
      --use_amp \
      --deepspeed_config ./conf/ds_stage2.json \
      --deepspeed.save_states model+optimizer
  done
fi
</span><span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">lstlisting</span><span class="token punctuation">}</span>

<span class="token function selector">\textbf</span><span class="token punctuation">{</span>关键特性：<span class="token punctuation">}</span>

<span class="token function selector">\subsection</span><span class="token punctuation">{</span><span class="token headline class-name">训练数据准备</span><span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>训练集<span class="token punctuation">}</span>: train-clean-100 的 parquet 文件列表
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>验证集<span class="token punctuation">}</span>: dev-clean + dev-other 的 parquet 文件列表
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\subsection</span><span class="token punctuation">{</span><span class="token headline class-name">模型训练顺序</span><span class="token punctuation">}</span>
脚本依次训练三个核心模型：
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">enumerate</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>llm<span class="token punctuation">}</span>: 大语言模型，负责文本到语义令牌的转换
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>flow<span class="token punctuation">}</span>: 流匹配模型，负责语义令牌到声学特征的转换
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>hifigan<span class="token punctuation">}</span>: 声码器，负责声学特征到波形的转换
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">enumerate</span><span class="token punctuation">}</span>

<span class="token function selector">\subsection</span><span class="token punctuation">{</span><span class="token headline class-name">训练技术特性</span><span class="token punctuation">}</span>
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>分布式训练<span class="token punctuation">}</span>: 使用 torchrun 启动分布式训练
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>混合精度训练<span class="token punctuation">}</span>: 启用 AMP (Automatic Mixed Precision)
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>内存优化<span class="token punctuation">}</span>: 使用 pin<span class="token function selector">\_</span>memory 加速数据加载
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>数据预取<span class="token punctuation">}</span>: prefetch=100 减少 I/O 等待
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>检查点恢复<span class="token punctuation">}</span>: 从预训练模型初始化
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\section</span><span class="token punctuation">{</span><span class="token headline class-name">阶段 6: 模型平均</span><span class="token punctuation">}</span>

<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">lstlisting</span><span class="token punctuation">}</span><span class="token cdata">[language=bash]
average_num=5
if [ ${stage} -le 6 ] &amp;&amp; [ ${stop_stage} -ge 6 ]; then
  for model in llm flow hifigan; do
    decode_checkpoint=`pwd`/exp/cosyvoice/$model/$train_engine/${model}.pt
    echo "do model average and final checkpoint is $decode_checkpoint"
    python cosyvoice/bin/average_model.py \
      --dst_model $decode_checkpoint \
      --src_path `pwd`/exp/cosyvoice/$model/$train_engine  \
      --num ${average_num} \
      --val_best
  done
fi
</span><span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">lstlisting</span><span class="token punctuation">}</span>

<span class="token function selector">\textbf</span><span class="token punctuation">{</span>功能：<span class="token punctuation">}</span> 模型权重平均：
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> 对每个模型的最后 5 个检查点进行权重平均
    <span class="token function selector">\item</span> 选择在验证集上性能最好的检查点
    <span class="token function selector">\item</span> 提高模型鲁棒性和泛化能力
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\section</span><span class="token punctuation">{</span><span class="token headline class-name">阶段 7: 模型导出</span><span class="token punctuation">}</span>

<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">lstlisting</span><span class="token punctuation">}</span><span class="token cdata">[language=bash]
if [ ${stage} -le 7 ] &amp;&amp; [ ${stop_stage} -ge 7 ]; then
  echo "Export your model for inference speedup. Remember copy your llm or flow model to model_dir"
  python cosyvoice/bin/export_jit.py --model_dir $pretrained_model_dir
  python cosyvoice/bin/export_onnx.py --model_dir $pretrained_model_dir
fi
</span><span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">lstlisting</span><span class="token punctuation">}</span>

<span class="token function selector">\textbf</span><span class="token punctuation">{</span>功能：<span class="token punctuation">}</span> 模型格式导出：
<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>JIT 格式<span class="token punctuation">}</span>: PyTorch JIT 格式，用于 Python 环境推理
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>ONNX 格式<span class="token punctuation">}</span>: 跨平台格式，支持多种推理引擎
    <span class="token function selector">\item</span> 提供推理速度优化，支持生产环境部署
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

<span class="token function selector">\section</span><span class="token punctuation">{</span><span class="token headline class-name">训练流程总结</span><span class="token punctuation">}</span>

<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">enumerate</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>数据准备阶段<span class="token punctuation">}</span> (-1 → 3): 下载数据、特征提取、格式转换
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>模型训练阶段<span class="token punctuation">}</span> (5): 分布式训练三个核心组件
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>模型优化阶段<span class="token punctuation">}</span> (6): 检查点平均提升性能
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>部署准备阶段<span class="token punctuation">}</span> (7): 导出优化模型格式
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">enumerate</span><span class="token punctuation">}</span>

<span class="token function selector">\section</span><span class="token punctuation">{</span><span class="token headline class-name">技术亮点</span><span class="token punctuation">}</span>

<span class="token function selector">\begin</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>模块化设计<span class="token punctuation">}</span>: 每个阶段独立，支持灵活的工作流
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>分布式训练<span class="token punctuation">}</span>: 支持多 GPU 训练，提高训练效率
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>完整流水线<span class="token punctuation">}</span>: 从原始数据到部署模型的完整流程
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>生产就绪<span class="token punctuation">}</span>: 支持模型导出和优化，便于部署
    <span class="token function selector">\item</span> <span class="token function selector">\textbf</span><span class="token punctuation">{</span>可复现性<span class="token punctuation">}</span>: 使用固定随机种子，确保结果一致性
<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">itemize</span><span class="token punctuation">}</span>

这个训练脚本展现了现代语音合成系统的完整训练流程，结合了先进的数据处理、分布式训练和模型优化技术。

<span class="token function selector">\end</span><span class="token punctuation">{</span><span class="token keyword">document</span><span class="token punctuation">}</span></pre><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _33882ae"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _28d7e84"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg></div>

---

### 用户

\section{数据处理流水线}
\textbf{流程：}
\[
\text{打开parquet文件} \rightarrow \text{文本tokenize} \rightarrow \text{过滤长短样本} \rightarrow \text{音频重采样} 
\]
\[
\rightarrow \text{计算Fbank特征} \rightarrow \text{解析说话人嵌入} \rightarrow \text{shuffle} \rightarrow \text{排序} \rightarrow \text{批处理} \rightarrow \text{填充}
\]详细解释一下数据处理的方法

---

### DeepSeek AI

<p>思考：</p><blockquote><p class="ds-markdown-paragraph"><span>我们有一个数据处理流水线，包括多个步骤。我将详细解释每个步骤的目的和方法。</span></p><ol start="1"><li><p class="ds-markdown-paragraph"><span>打开parquet文件：从Parquet格式的文件中读取数据。Parquet是一种列式存储格式，适合大规模数据，读取效率高。</span></p></li><li><p class="ds-markdown-paragraph"><span>文本tokenize：将文本字符串转换为令牌（token）序列，例如将句子拆分成单词或子词，并映射为整数ID。</span></p></li><li><p class="ds-markdown-paragraph"><span>过滤长短样本：根据一定的长度限制（如音频长度或文本长度）过滤掉过长或过短的样本，以保持训练数据的均匀性。</span></p></li><li><p class="ds-markdown-paragraph"><span>音频重采样：将音频重新采样到统一的采样率（如22050Hz），以确保所有音频样本具有相同的采样率。</span></p></li><li><p class="ds-markdown-paragraph"><span>计算Fbank特征：提取Fbank（Filterbank）特征，这是一种常用的语音特征，类似于梅尔频谱，但未进行对数压缩。</span></p></li><li><p class="ds-markdown-paragraph"><span>解析说话人嵌入：从预先提取的说话人嵌入文件中加载说话人嵌入向量，该向量用于表示说话人的声音特征。</span></p></li><li><p class="ds-markdown-paragraph"><span>Shuffle：打乱数据顺序，以避免模型学习到数据顺序相关的模式。</span></p></li><li><p class="ds-markdown-paragraph"><span>排序：根据音频长度或文本长度对数据进行排序，以便在批处理时可以将相似长度的样本放在一起，减少填充带来的计算浪费。</span></p></li><li><p class="ds-markdown-paragraph"><span>批处理：将多个样本组合成一个批次，通常每个批次中的样本数量是固定的。</span></p></li><li><p class="ds-markdown-paragraph"><span>填充：对批次内的样本进行填充，使它们具有相同的长度（文本长度或音频特征长度），以便于模型处理。</span></p></li></ol><p class="ds-markdown-paragraph"><span>下面，我将更详细地解释每个步骤。</span></p><ol start="1"><li><p class="ds-markdown-paragraph"><span>打开parquet文件：</span></p><ul><li><p class="ds-markdown-paragraph"><span>使用Parquet读取库（如pyarrow或pandas）读取数据。每个Parquet文件通常包含多个样本，每个样本包括音频路径、文本、说话人ID等信息。</span></p></li></ul></li><li><p class="ds-markdown-paragraph"><span>文本tokenize：</span></p><ul><li><p class="ds-markdown-paragraph"><span>使用预定义的令牌化器（如BPE、WordPiece等）将文本转换为令牌ID序列。例如，使用一个词汇表将每个词映射为一个整数。</span></p></li></ul></li><li><p class="ds-markdown-paragraph"><span>过滤长短样本：</span></p><ul><li><p class="ds-markdown-paragraph"><span>设定最小和最大长度阈值。例如，过滤掉音频长度小于0.5秒或大于10秒的样本，以及文本令牌长度小于1或大于200的样本。</span></p></li></ul></li><li><p class="ds-markdown-paragraph"><span>音频重采样：</span></p><ul><li><p class="ds-markdown-paragraph"><span>使用音频处理库（如librosa）将音频重新采样到目标采样率。例如，从原始采样率（可能是48000Hz）重采样到22050Hz。</span></p></li></ul></li><li><p class="ds-markdown-paragraph"><span>计算Fbank特征：</span></p><ul><li><p class="ds-markdown-paragraph"><span>使用语音处理工具（如Kaldi或torchaudio）提取Fbank特征。通常步骤包括：预加重、分帧、加窗、短时傅里叶变换、梅尔滤波器组滤波、对数运算等。但Fbank通常不包括对数运算，而Mel频谱包括。</span></p></li></ul></li><li><p class="ds-markdown-paragraph"><span>解析说话人嵌入：</span></p><ul><li><p class="ds-markdown-paragraph"><span>从预先准备好的文件中加载说话人嵌入。这些嵌入通常是由一个预训练的说话人验证模型（如CAMPPlus）提取的，每个说话人有一个固定的嵌入向量，或者每个语句有一个嵌入向量。</span></p></li></ul></li><li><p class="ds-markdown-paragraph"><span>Shuffle：</span></p><ul><li><p class="ds-markdown-paragraph"><span>随机打乱数据顺序，通常是在每个epoch开始时进行。</span></p></li></ul></li><li><p class="ds-markdown-paragraph"><span>排序：</span></p><ul><li><p class="ds-markdown-paragraph"><span>按照音频长度（或文本长度）对样本进行排序，以便后续的批处理可以更高效。通常，我们会将长度相近的样本放在同一个批次中。</span></p></li></ul></li><li><p class="ds-markdown-paragraph"><span>批处理：</span></p><ul><li><p class="ds-markdown-paragraph"><span>将排序后的数据分成多个批次，每个批次包含一定数量的样本（如32个样本）。</span></p></li></ul></li><li><p class="ds-markdown-paragraph"><span>填充：</span><br><span>- 对批次内的样本进行填充，使它们具有相同的长度。对于文本令牌序列，我们可以在序列末尾添加0（假设0是填充令牌）；对于音频特征，我们可以在特征序列的末尾添加0向量。同时，通常会生成一个掩码（mask）来指示哪些位置是真实数据，哪些是填充。</span></p></li></ol><p class="ds-markdown-paragraph"><span>这个数据处理流水线确保了数据的一致性、高效性和可训练性。每个步骤都是为了解决特定问题而设计的，例如重采样确保音频采样率一致，过滤长短样本避免极端样本，排序和批处理减少填充开销等。</span></p></blockquote><br/><p class="ds-markdown-paragraph"><span>\section{数据处理流水线详解}</span></p><p class="ds-markdown-paragraph"><span>数据处理流水线是 CosyVoice 训练系统中的关键组成部分，它将原始音频和文本数据转换为模型训练所需的格式。以下是对每个处理步骤的详细解释：</span></p><p class="ds-markdown-paragraph"><span>\subsection{数据处理步骤详解}</span></p><p class="ds-markdown-paragraph"><span>\subsubsection{1. 打开 Parquet 文件}</span><br><span>\textbf{目的：} 从高效的列式存储格式中读取数据\</span><br><span>\textbf{实现方式：}</span><br><span>\begin{verbatim}</span><br><span>使用 PyArrow 或类似的 Parquet 读取库</span><br><span>每个 Parquet 文件包含 1000 个语音样本的元数据</span><br><span>\end{verbatim}</span><br><span>\textbf{数据结构：}</span><br><span>\begin{itemize}</span><br><span>\item 音频文件路径</span><br><span>\item 文本转录内容</span><br><span>\item 说话人 ID</span><br><span>\item 预提取的特征文件路径</span><br><span>\end{itemize}</span></p><p class="ds-markdown-paragraph"><span>\subsubsection{2. 文本 Tokenize}</span><br><span>\textbf{目的：} 将文本转换为模型可理解的令牌序列\</span><br><span>\textbf{技术细节：}</span><br><span>\begin{itemize}</span><br><span>\item 使用 BPE (Byte Pair Encoding) 分词器</span><br><span>\item 词汇表大小：51,866 个文本令牌</span><br><span>\item 特殊令牌处理：</span><br><span>\begin{itemize}</span><br><span>\item \texttt{</span><span class="ds-markdown-html">&lt;s&gt;</span><span>}: 序列开始</span><br><span>\item \texttt{</span><span class="ds-markdown-html">&lt;/s&gt;</span><span>}: 序列结束</span><br><span>\item \texttt{</span><span class="ds-markdown-html">&lt;unk&gt;</span><span>}: 未知词</span><br><span>\item \texttt{</span><span class="ds-markdown-html">&lt;pad&gt;</span><span>}: 填充令牌</span><br><span>\end{itemize}</span><br><span>\end{itemize}</span><br><span>\textbf{处理示例：}</span><br><span>\begin{verbatim}</span><br><span>输入: "Hello world"</span><br><span>输出: [1, 234, 567, 2]  # 1=</span><span class="ds-markdown-html">&lt;s&gt;</span><span>, 234="Hello", 567="world", 2=</span><span class="ds-markdown-html">&lt;/s&gt;</span><span></span><br><span>\end{verbatim}</span></p><p class="ds-markdown-paragraph"><span>\subsubsection{3. 过滤长短样本}</span><br><span>\textbf{目的：} 移除过长或过短的样本，保证训练稳定性\</span><br><span>\textbf{过滤标准：}</span><br><span>\begin{itemize}</span><br><span>\item \textbf{音频长度过滤}：</span><br><span>\begin{itemize}</span><br><span>\item 最小长度：通常 0.5-1.0 秒</span><br><span>\item 最大长度：通常 10-15 秒</span><br><span>\end{itemize}</span><br><span>\item \textbf{文本长度过滤}：</span><br><span>\begin{itemize}</span><br><span>\item 最小文本令牌数：2-5 个令牌</span><br><span>\item 最大文本令牌数：200-300 个令牌</span><br><span>\end{itemize}</span><br><span>\end{itemize}</span><br><span>\textbf{重要性：}</span><br><span>\begin{itemize}</span><br><span>\item 避免 GPU 内存溢出（长序列）</span><br><span>\item 确保模型学习有效模式（短序列可能信息不足）</span><br><span>\item 提高批处理效率</span><br><span>\end{itemize}</span></p><p class="ds-markdown-paragraph"><span>\subsubsection{4. 音频重采样}</span><br><span>\textbf{目的：} 统一所有音频的采样率\</span><br><span>\textbf{技术参数：}</span><br><span>\begin{itemize}</span><br><span>\item 目标采样率：22,050 Hz</span><br><span>\item 重采样算法：通常使用带抗混叠滤波的重采样</span><br><span>\end{itemize}</span><br><span>\textbf{处理流程：}</span><br><span>\begin{verbatim}</span><br><span>原始音频 → 读取波形 → 重采样滤波器 → 22,050 Hz 输出</span><br><span>\end{verbatim}</span><br><span>\textbf{重要性：}</span><br><span>\begin{itemize}</span><br><span>\item 保证所有音频输入具有相同的时域分辨率</span><br><span>\item 避免模型需要处理多种采样率</span><br><span>\item 与声码器的采样率要求匹配</span><br><span>\end{itemize}</span></p><p class="ds-markdown-paragraph"><span>\subsubsection{5. 计算 Fbank 特征}</span><br><span>\textbf{目的：} 提取语音的频域特征表示\</span><br><span>\textbf{技术细节：}</span><br><span>\begin{itemize}</span><br><span>\item \textbf{帧长}: 25ms</span><br><span>\item \textbf{帧移}: 10ms</span><br><span>\item \textbf{Mel 滤波器组数量}: 80</span><br><span>\item \textbf{频率范围}: 0-11,025 Hz (Nyquist 频率)</span><br><span>\end{itemize}</span><br><span>\textbf{计算步骤：}</span></p><span class="katex-display ds-markdown-math"><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><semantics><mrow><mtext>音频信号</mtext><mo>→</mo><mtext>预加重</mtext><mo>→</mo><mtext>分帧</mtext><mo>→</mo><mtext>加窗</mtext><mo>→</mo><mtext>FFT</mtext><mo>→</mo><mtext>Mel&nbsp;滤波器组</mtext><mo>→</mo><mtext>对数压缩</mtext></mrow><annotation encoding="application/x-tex">\text{音频信号} \rightarrow \text{预加重} \rightarrow \text{分帧} \rightarrow \text{加窗} \rightarrow \text{FFT} \rightarrow \text{Mel 滤波器组} \rightarrow \text{对数压缩}</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.6833em;"></span><span class="mord text"><span class="mord cjk_fallback">音频信号</span></span><span class="mspace" style="margin-right:0.2778em;"></span><span class="mrel">→</span><span class="mspace" style="margin-right:0.2778em;"></span></span><span class="base"><span class="strut" style="height:0.6833em;"></span><span class="mord text"><span class="mord cjk_fallback">预加重</span></span><span class="mspace" style="margin-right:0.2778em;"></span><span class="mrel">→</span><span class="mspace" style="margin-right:0.2778em;"></span></span><span class="base"><span class="strut" style="height:0.6833em;"></span><span class="mord text"><span class="mord cjk_fallback">分帧</span></span><span class="mspace" style="margin-right:0.2778em;"></span><span class="mrel">→</span><span class="mspace" style="margin-right:0.2778em;"></span></span><span class="base"><span class="strut" style="height:0.6833em;"></span><span class="mord text"><span class="mord cjk_fallback">加窗</span></span><span class="mspace" style="margin-right:0.2778em;"></span><span class="mrel">→</span><span class="mspace" style="margin-right:0.2778em;"></span></span><span class="base"><span class="strut" style="height:0.6833em;"></span><span class="mord text"><span class="mord">FFT</span></span><span class="mspace" style="margin-right:0.2778em;"></span><span class="mrel">→</span><span class="mspace" style="margin-right:0.2778em;"></span></span><span class="base"><span class="strut" style="height:0.6944em;"></span><span class="mord text"><span class="mord">Mel&nbsp;</span><span class="mord cjk_fallback">滤波器组</span></span><span class="mspace" style="margin-right:0.2778em;"></span><span class="mrel">→</span><span class="mspace" style="margin-right:0.2778em;"></span></span><span class="base"><span class="strut" style="height:0.6833em;"></span><span class="mord text"><span class="mord cjk_fallback">对数压缩</span></span></span></span></span></span><p class="ds-markdown-paragraph"><span>\textbf{输出特征：}</span><br><span>\begin{itemize}</span><br><span>\item 形状：[时间帧数, 80]</span><br><span>\item 用于流匹配模型的输入条件</span><br><span>\end{itemize}</span></p><p class="ds-markdown-paragraph"><span>\subsubsection{6. 解析说话人嵌入}</span><br><span>\textbf{目的：} 加载预计算的说话人身份特征\</span><br><span>\textbf{嵌入来源：}</span><br><span>\begin{itemize}</span><br><span>\item 使用 CAMPPlus 模型预提取</span><br><span>\item 每个说话人对应一个 192 维向量</span><br><span>\item 存储在 \texttt{</span><a href="https://spk2embedding.pt" target="_blank" rel="noreferrer"><span>spk2embedding.pt</span></a><span>}</span><span> 和 \texttt{</span><a href="https://utt2embedding.pt" target="_blank" rel="noreferrer"><span>utt2embedding.pt</span></a><span>}</span><span> 中</span><br><span>\end{itemize}</span><br><span>\textbf{使用方式：}</span><br><span>\begin{itemize}</span><br><span>\item 作为条件信息输入到所有模型</span><br><span>\item 实现说话人自适应的语音合成</span><br><span>\item 支持零样本语音克隆</span><br><span>\end{itemize}</span></p><p class="ds-markdown-paragraph"><span>\subsubsection{7. Shuffle (数据洗牌)}</span><br><span>\textbf{目的：} 打乱数据顺序，避免模型学习到数据顺序模式\</span><br><span>\textbf{实现方法：}</span><br><span>\begin{itemize}</span><br><span>\item 使用随机数生成器进行置换</span><br><span>\item 每个 epoch 重新洗牌</span><br><span>\item 保持不同进程间的洗牌一致性（分布式训练）</span><br><span>\end{itemize}</span><br><span>\textbf{重要性：}</span><br><span>\begin{itemize}</span><br><span>\item 防止模型过拟合数据顺序</span><br><span>\item 提高模型的泛化能力</span><br><span>\item 确保梯度下降的有效性</span><br><span>\end{itemize}</span></p><p class="ds-markdown-paragraph"><span>\subsubsection{8. 排序}</span><br><span>\textbf{目的：} 按序列长度排序，优化批处理效率\</span><br><span>\textbf{排序策略：}</span><br><span>\begin{itemize}</span><br><span>\item 主要按音频长度（帧数）排序</span><br><span>\item 次要按文本长度（令牌数）排序</span><br><span>\end{itemize}</span><br><span>\textbf{批处理优化：}</span><br><span>\begin{itemize}</span><br><span>\item 将长度相似的样本放在同一批次</span><br><span>\item 减少填充（padding）的数量</span><br><span>\item 提高 GPU 利用率</span><br><span>\end{itemize}</span></p><p class="ds-markdown-paragraph"><span>\subsubsection{9. 批处理}</span><br><span>\textbf{目的：} 将多个样本组合成训练批次\</span><br><span>\textbf{批处理策略：}</span><br><span>\begin{itemize}</span><br><span>\item \textbf{动态批处理}：基于序列长度而非固定样本数</span><br><span>\item \textbf{最大令牌数限制}：控制每批的总计算量</span><br><span>\item \textbf{设备内存感知}：根据 GPU 内存调整批次大小</span><br><span>\end{itemize}</span><br><span>\textbf{批次组成：}</span><br><span>\begin{itemize}</span><br><span>\item 文本令牌序列（填充到批次内最大长度）</span><br><span>\item 语音令牌序列（填充到批次内最大长度）</span><br><span>\item Fbank 特征序列</span><br><span>\item 说话人嵌入向量</span><br><span>\item 序列长度掩码</span><br><span>\end{itemize}</span></p><p class="ds-markdown-paragraph"><span>\subsubsection{10. 填充}</span><br><span>\textbf{目的：} 将批次内不同长度的序列填充到相同长度\</span><br><span>\textbf{填充策略：}</span><br><span>\begin{itemize}</span><br><span>\item \textbf{文本序列}：在序列末尾添加 \texttt{</span><span class="ds-markdown-html">&lt;pad&gt;</span><span>} 令牌</span><br><span>\item \textbf{语音序列}：在序列末尾添加 0（语音令牌的填充值）</span><br><span>\item \textbf{特征序列}：在时间维度末尾添加 0 向量</span><br><span>\end{itemize}</span><br><span>\textbf{掩码生成：}</span><br><span>\begin{itemize}</span><br><span>\item 创建二进制掩码标识有效位置</span><br><span>\item 在注意力机制中忽略填充位置</span><br><span>\item 在损失计算中排除填充部分</span><br><span>\end{itemize}</span></p><p class="ds-markdown-paragraph"><span>\subsection{数据流水线的技术优势}</span></p><p class="ds-markdown-paragraph"><span>\subsubsection{效率优化}</span><br><span>\begin{itemize}</span><br><span>\item \textbf{并行处理}：使用多个工作进程并行加载和预处理</span><br><span>\item \textbf{预取机制}：提前准备下一批次数据，减少 GPU 等待时间</span><br><span>\item \textbf{内存映射}：Parquet 格式支持高效的内存映射读取</span><br><span>\end{itemize}</span></p><p class="ds-markdown-paragraph"><span>\subsubsection{质量控制}</span><br><span>\begin{itemize}</span><br><span>\item \textbf{数据验证}：在每个步骤检查数据完整性和一致性</span><br><span>\item \textbf{异常处理}：自动跳过损坏或格式错误的数据样本</span><br><span>\item \textbf{特征归一化}：确保输入特征的数值稳定性</span><br><span>\end{itemize}</span></p><p class="ds-markdown-paragraph"><span>\subsubsection{灵活性}</span><br><span>\begin{itemize}</span><br><span>\item \textbf{配置驱动}：通过配置文件调整所有处理参数</span><br><span>\item \textbf{模块化设计}：每个处理步骤可独立测试和替换</span><br><span>\item \textbf{扩展性}：支持添加新的数据处理模块</span><br><span>\end{itemize}</span></p><p class="ds-markdown-paragraph"><span>\subsection{完整数据处理流程图示}</span></p><span class="katex-display ds-markdown-math"><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><semantics><mtable rowspacing="0.16em" columnalign="center center center center center center" columnspacing="1em"><mtr><mtd><mstyle scriptlevel="0" displaystyle="false"><mtext>Parquet文件</mtext></mstyle></mtd><mtd><mstyle scriptlevel="0" displaystyle="false"><mo lspace="0em" rspace="0em">→</mo></mstyle></mtd><mtd><mstyle scriptlevel="0" displaystyle="false"><mtext>文本Tokenize</mtext></mstyle></mtd><mtd><mstyle scriptlevel="0" displaystyle="false"><mo lspace="0em" rspace="0em">→</mo></mstyle></mtd><mtd><mstyle scriptlevel="0" displaystyle="false"><mtext>长度过滤</mtext></mstyle></mtd><mtd><mstyle scriptlevel="0" displaystyle="false"><mo lspace="0em" rspace="0em">→</mo></mstyle></mtd></mtr><mtr><mtd><mstyle scriptlevel="0" displaystyle="false"><mo lspace="0em" rspace="0em">↓</mo></mstyle></mtd><mtd><mstyle scriptlevel="0" displaystyle="false"><mrow></mrow></mstyle></mtd><mtd><mstyle scriptlevel="0" displaystyle="false"><mrow></mrow></mstyle></mtd><mtd><mstyle scriptlevel="0" displaystyle="false"><mrow></mrow></mstyle></mtd><mtd><mstyle scriptlevel="0" displaystyle="false"><mrow></mrow></mstyle></mtd><mtd><mstyle scriptlevel="0" displaystyle="false"><mrow></mrow></mstyle></mtd></mtr><mtr><mtd><mstyle scriptlevel="0" displaystyle="false"><mtext>音频重采样</mtext></mstyle></mtd><mtd><mstyle scriptlevel="0" displaystyle="false"><mo lspace="0em" rspace="0em">→</mo></mstyle></mtd><mtd><mstyle scriptlevel="0" displaystyle="false"><mtext>Fbank特征</mtext></mstyle></mtd><mtd><mstyle scriptlevel="0" displaystyle="false"><mo lspace="0em" rspace="0em">→</mo></mstyle></mtd><mtd><mstyle scriptlevel="0" displaystyle="false"><mtext>说话人嵌入</mtext></mstyle></mtd><mtd><mstyle scriptlevel="0" displaystyle="false"><mo lspace="0em" rspace="0em">→</mo></mstyle></mtd></mtr><mtr><mtd><mstyle scriptlevel="0" displaystyle="false"><mo lspace="0em" rspace="0em">↓</mo></mstyle></mtd><mtd><mstyle scriptlevel="0" displaystyle="false"><mrow></mrow></mstyle></mtd><mtd><mstyle scriptlevel="0" displaystyle="false"><mrow></mrow></mstyle></mtd><mtd><mstyle scriptlevel="0" displaystyle="false"><mrow></mrow></mstyle></mtd><mtd><mstyle scriptlevel="0" displaystyle="false"><mrow></mrow></mstyle></mtd><mtd><mstyle scriptlevel="0" displaystyle="false"><mrow></mrow></mstyle></mtd></mtr><mtr><mtd><mstyle scriptlevel="0" displaystyle="false"><mtext>数据洗牌</mtext></mstyle></mtd><mtd><mstyle scriptlevel="0" displaystyle="false"><mo lspace="0em" rspace="0em">→</mo></mstyle></mtd><mtd><mstyle scriptlevel="0" displaystyle="false"><mtext>长度排序</mtext></mstyle></mtd><mtd><mstyle scriptlevel="0" displaystyle="false"><mo lspace="0em" rspace="0em">→</mo></mstyle></mtd><mtd><mstyle scriptlevel="0" displaystyle="false"><mtext>动态批处理</mtext></mstyle></mtd><mtd><mstyle scriptlevel="0" displaystyle="false"><mo lspace="0em" rspace="0em">→</mo></mstyle></mtd></mtr><mtr><mtd><mstyle scriptlevel="0" displaystyle="false"><mo lspace="0em" rspace="0em">↓</mo></mstyle></mtd><mtd><mstyle scriptlevel="0" displaystyle="false"><mrow></mrow></mstyle></mtd><mtd><mstyle scriptlevel="0" displaystyle="false"><mrow></mrow></mstyle></mtd><mtd><mstyle scriptlevel="0" displaystyle="false"><mrow></mrow></mstyle></mtd><mtd><mstyle scriptlevel="0" displaystyle="false"><mrow></mrow></mstyle></mtd><mtd><mstyle scriptlevel="0" displaystyle="false"><mrow></mrow></mstyle></mtd></mtr><mtr><mtd><mstyle scriptlevel="0" displaystyle="false"><mtext>序列填充</mtext></mstyle></mtd><mtd><mstyle scriptlevel="0" displaystyle="false"><mo lspace="0em" rspace="0em">→</mo></mstyle></mtd><mtd><mstyle scriptlevel="0" displaystyle="false"><mtext>模型训练</mtext></mstyle></mtd><mtd><mstyle scriptlevel="0" displaystyle="false"><mrow></mrow></mstyle></mtd><mtd><mstyle scriptlevel="0" displaystyle="false"><mrow></mrow></mstyle></mtd><mtd><mstyle scriptlevel="0" displaystyle="false"><mrow></mrow></mstyle></mtd></mtr></mtable><annotation encoding="application/x-tex">\begin{array}{cccccc}
\text{Parquet文件} &amp; \rightarrow &amp; \text{文本Tokenize} &amp; \rightarrow &amp; \text{长度过滤} &amp; \rightarrow \\
\downarrow &amp; &amp; &amp; &amp; &amp; \\
\text{音频重采样} &amp; \rightarrow &amp; \text{Fbank特征} &amp; \rightarrow &amp; \text{说话人嵌入} &amp; \rightarrow \\
\downarrow &amp; &amp; &amp; &amp; &amp; \\
\text{数据洗牌} &amp; \rightarrow &amp; \text{长度排序} &amp; \rightarrow &amp; \text{动态批处理} &amp; \rightarrow \\
\downarrow &amp; &amp; &amp; &amp; &amp; \\
\text{序列填充} &amp; \rightarrow &amp; \text{模型训练} &amp; &amp; &amp; \\
\end{array}</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:8.4em;vertical-align:-3.95em;"></span><span class="mord"><span class="mtable"><span class="arraycolsep" style="width:0.5em;"></span><span class="col-align-c"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:4.45em;"><span style="top:-6.61em;"><span class="pstrut" style="height:3em;"></span><span class="mord"><span class="mord text"><span class="mord">Parquet</span><span class="mord cjk_fallback">文件</span></span></span></span><span style="top:-5.41em;"><span class="pstrut" style="height:3em;"></span><span class="mord"><span class="mrel">↓</span></span></span><span style="top:-4.21em;"><span class="pstrut" style="height:3em;"></span><span class="mord"><span class="mord text"><span class="mord cjk_fallback">音频重采样</span></span></span></span><span style="top:-3.01em;"><span class="pstrut" style="height:3em;"></span><span class="mord"><span class="mrel">↓</span></span></span><span style="top:-1.81em;"><span class="pstrut" style="height:3em;"></span><span class="mord"><span class="mord text"><span class="mord cjk_fallback">数据洗牌</span></span></span></span><span style="top:-0.61em;"><span class="pstrut" style="height:3em;"></span><span class="mord"><span class="mrel">↓</span></span></span><span style="top:0.59em;"><span class="pstrut" style="height:3em;"></span><span class="mord"><span class="mord text"><span class="mord cjk_fallback">序列填充</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height:3.95em;"><span></span></span></span></span></span><span class="arraycolsep" style="width:0.5em;"></span><span class="arraycolsep" style="width:0.5em;"></span><span class="col-align-c"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:4.45em;"><span style="top:-6.61em;"><span class="pstrut" style="height:3em;"></span><span class="mord"><span class="mrel">→</span></span></span><span style="top:-5.41em;"><span class="pstrut" style="height:3em;"></span><span class="mord"></span></span><span style="top:-4.21em;"><span class="pstrut" style="height:3em;"></span><span class="mord"><span class="mrel">→</span></span></span><span style="top:-3.01em;"><span class="pstrut" style="height:3em;"></span><span class="mord"></span></span><span style="top:-1.81em;"><span class="pstrut" style="height:3em;"></span><span class="mord"><span class="mrel">→</span></span></span><span style="top:-0.61em;"><span class="pstrut" style="height:3em;"></span><span class="mord"></span></span><span style="top:0.59em;"><span class="pstrut" style="height:3em;"></span><span class="mord"><span class="mrel">→</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height:3.95em;"><span></span></span></span></span></span><span class="arraycolsep" style="width:0.5em;"></span><span class="arraycolsep" style="width:0.5em;"></span><span class="col-align-c"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:4.45em;"><span style="top:-6.61em;"><span class="pstrut" style="height:3em;"></span><span class="mord"><span class="mord text"><span class="mord cjk_fallback">文本</span><span class="mord">Tokenize</span></span></span></span><span style="top:-5.41em;"><span class="pstrut" style="height:3em;"></span><span class="mord"></span></span><span style="top:-4.21em;"><span class="pstrut" style="height:3em;"></span><span class="mord"><span class="mord text"><span class="mord">Fbank</span><span class="mord cjk_fallback">特征</span></span></span></span><span style="top:-3.01em;"><span class="pstrut" style="height:3em;"></span><span class="mord"></span></span><span style="top:-1.81em;"><span class="pstrut" style="height:3em;"></span><span class="mord"><span class="mord text"><span class="mord cjk_fallback">长度排序</span></span></span></span><span style="top:-0.61em;"><span class="pstrut" style="height:3em;"></span><span class="mord"></span></span><span style="top:0.59em;"><span class="pstrut" style="height:3em;"></span><span class="mord"><span class="mord text"><span class="mord cjk_fallback">模型训练</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height:3.95em;"><span></span></span></span></span></span><span class="arraycolsep" style="width:0.5em;"></span><span class="arraycolsep" style="width:0.5em;"></span><span class="col-align-c"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:4.45em;"><span style="top:-6.61em;"><span class="pstrut" style="height:3em;"></span><span class="mord"><span class="mrel">→</span></span></span><span style="top:-5.41em;"><span class="pstrut" style="height:3em;"></span><span class="mord"></span></span><span style="top:-4.21em;"><span class="pstrut" style="height:3em;"></span><span class="mord"><span class="mrel">→</span></span></span><span style="top:-3.01em;"><span class="pstrut" style="height:3em;"></span><span class="mord"></span></span><span style="top:-1.81em;"><span class="pstrut" style="height:3em;"></span><span class="mord"><span class="mrel">→</span></span></span><span style="top:-0.61em;"><span class="pstrut" style="height:3em;"></span><span class="mord"></span></span><span style="top:0.59em;"><span class="pstrut" style="height:3em;"></span><span class="mord"></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height:3.95em;"><span></span></span></span></span></span><span class="arraycolsep" style="width:0.5em;"></span><span class="arraycolsep" style="width:0.5em;"></span><span class="col-align-c"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:4.45em;"><span style="top:-6.61em;"><span class="pstrut" style="height:3em;"></span><span class="mord"><span class="mord text"><span class="mord cjk_fallback">长度过滤</span></span></span></span><span style="top:-5.41em;"><span class="pstrut" style="height:3em;"></span><span class="mord"></span></span><span style="top:-4.21em;"><span class="pstrut" style="height:3em;"></span><span class="mord"><span class="mord text"><span class="mord cjk_fallback">说话人嵌入</span></span></span></span><span style="top:-3.01em;"><span class="pstrut" style="height:3em;"></span><span class="mord"></span></span><span style="top:-1.81em;"><span class="pstrut" style="height:3em;"></span><span class="mord"><span class="mord text"><span class="mord cjk_fallback">动态批处理</span></span></span></span><span style="top:-0.61em;"><span class="pstrut" style="height:3em;"></span><span class="mord"></span></span><span style="top:0.59em;"><span class="pstrut" style="height:3em;"></span><span class="mord"></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height:3.95em;"><span></span></span></span></span></span><span class="arraycolsep" style="width:0.5em;"></span><span class="arraycolsep" style="width:0.5em;"></span><span class="col-align-c"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:4.45em;"><span style="top:-6.61em;"><span class="pstrut" style="height:3em;"></span><span class="mord"><span class="mrel">→</span></span></span><span style="top:-5.41em;"><span class="pstrut" style="height:3em;"></span><span class="mord"></span></span><span style="top:-4.21em;"><span class="pstrut" style="height:3em;"></span><span class="mord"><span class="mrel">→</span></span></span><span style="top:-3.01em;"><span class="pstrut" style="height:3em;"></span><span class="mord"></span></span><span style="top:-1.81em;"><span class="pstrut" style="height:3em;"></span><span class="mord"><span class="mrel">→</span></span></span><span style="top:-0.61em;"><span class="pstrut" style="height:3em;"></span><span class="mord"></span></span><span style="top:0.59em;"><span class="pstrut" style="height:3em;"></span><span class="mord"></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height:3.95em;"><span></span></span></span></span></span><span class="arraycolsep" style="width:0.5em;"></span></span></span></span></span></span></span><p class="ds-markdown-paragraph"><span>这个数据处理流水线确保了 CosyVoice 系统能够高效、稳定地处理大规模语音数据，为高质量的语音合成模型训练提供了可靠的数据基础。</span></p>

---

### 用户

为什么cosyvoicev2要移除说话人嵌入

---

### DeepSeek AI

<p>思考：</p><blockquote><p class="ds-markdown-paragraph"><span>我们注意到在CosyVoiceV2中，说话人嵌入（speaker embedding）被移除了。这可能是由于以下几个原因：</span></p><ol start="1"><li><p class="ds-markdown-paragraph"><strong><span>模型架构的简化</span></strong><span>：CosyVoiceV2可能采用了更简单的模型架构，不再需要显式的说话人嵌入来区分不同的说话人。相反，它可能通过其他方式（例如使用更强大的语言模型）来捕捉说话人特征。</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>零样本语音克隆的改进</span></strong><span>：CosyVoiceV2可能专注于零样本语音克隆，即通过参考音频来生成目标说话人的语音，而不需要预定义的说话人嵌入。在这种情况下，模型可以从参考音频中直接提取说话人特征，从而无需在训练时使用固定的说话人嵌入。</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>训练数据的扩展</span></strong><span>：如果CosyVoiceV2使用了更大规模的训练数据，其中包含了更多的说话人，那么显式的说话人嵌入可能会变得难以管理（例如，说话人数量太多，嵌入矩阵过大）。因此，移除说话人嵌入可以简化模型并减少参数数量。</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>多说话人合成的统一建模</span></strong><span>：CosyVoiceV2可能采用了一种统一的建模方式，将所有的说话人视为一个整体，通过条件语言模型来学习不同说话人的语音特征，而不需要为每个说话人分配一个独立的嵌入。</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>性能与泛化能力的提升</span></strong><span>：在某些情况下，移除说话人嵌入可能迫使模型学习更鲁棒的语音表示，这些表示不依赖于特定的说话人身份，从而在未见过的说话人上表现更好。</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>流匹配技术的应用</span></strong><span>：CosyVoiceV2使用了流匹配（flow matching）技术，该技术可能能够直接从输入文本和参考音频中学习到说话人特征，因此不再需要额外的说话人嵌入。</span></p></li></ol><p class="ds-markdown-paragraph"><span>需要注意的是，具体原因需要参考CosyVoiceV2的论文或官方文档。以上只是一些可能的推测。</span></p></blockquote><br/><p class="ds-markdown-paragraph"><span>\section{CosyVoiceV2 移除说话人嵌入的原因分析}</span></p><p class="ds-markdown-paragraph"><span>基于对 CosyVoiceV2 架构设计的理解，移除说话人嵌入是经过深思熟虑的设计决策，主要基于以下几个技术考量：</span></p><p class="ds-markdown-paragraph"><span>\subsection{架构简化和统一化}</span></p><p class="ds-markdown-paragraph"><span>\subsubsection{统一的语言模型架构}</span><br><span>\textbf{设计理念：} 将语音合成完全构建在纯语言模型范式上</span></p><span class="katex-display ds-markdown-math"><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><semantics><mrow><mtext>CosyVoiceV1:&nbsp;文本&nbsp;→&nbsp;LLM&nbsp;→&nbsp;语义令牌&nbsp;→&nbsp;Flow&nbsp;→&nbsp;声学特征&nbsp;→&nbsp;HiFiGAN&nbsp;→&nbsp;语音</mtext></mrow><annotation encoding="application/x-tex">\text{CosyVoiceV1: 文本 → LLM → 语义令牌 → Flow → 声学特征 → HiFiGAN → 语音}</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.8889em;vertical-align:-0.1944em;"></span><span class="mord text"><span class="mord">CosyVoiceV1:&nbsp;</span><span class="mord cjk_fallback">文本</span><span class="mord">&nbsp;→&nbsp;LLM&nbsp;→&nbsp;</span><span class="mord cjk_fallback">语义令牌</span><span class="mord">&nbsp;→&nbsp;Flow&nbsp;→&nbsp;</span><span class="mord cjk_fallback">声学特征</span><span class="mord">&nbsp;→&nbsp;HiFiGAN&nbsp;→&nbsp;</span><span class="mord cjk_fallback">语音</span></span></span></span></span></span><span class="katex-display ds-markdown-math"><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><semantics><mrow><mtext>CosyVoiceV2:&nbsp;文本&nbsp;→&nbsp;统一LLM&nbsp;→&nbsp;语音令牌&nbsp;→&nbsp;解码器&nbsp;→&nbsp;语音</mtext></mrow><annotation encoding="application/x-tex">\text{CosyVoiceV2: 文本 → 统一LLM → 语音令牌 → 解码器 → 语音}</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.8778em;vertical-align:-0.1944em;"></span><span class="mord text"><span class="mord">CosyVoiceV2:&nbsp;</span><span class="mord cjk_fallback">文本</span><span class="mord">&nbsp;→&nbsp;</span><span class="mord cjk_fallback">统一</span><span class="mord">LLM&nbsp;→&nbsp;</span><span class="mord cjk_fallback">语音令牌</span><span class="mord">&nbsp;→&nbsp;</span><span class="mord cjk_fallback">解码器</span><span class="mord">&nbsp;→&nbsp;</span><span class="mord cjk_fallback">语音</span></span></span></span></span></span><p class="ds-markdown-paragraph"><span>\subsubsection{移除多模态输入的复杂性}</span><br><span>\begin{itemize}</span><br><span>\item \textbf{V1 问题}: 需要同时处理文本令牌、语音令牌和说话人嵌入三种不同模态的输入</span><br><span>\item \textbf{V2 解决方案}: 仅处理文本和语音令牌，简化输入流</span><br><span>\item \textbf{优势}: 减少模型复杂度和训练不稳定性</span><br><span>\end{itemize}</span></p><p class="ds-markdown-paragraph"><span>\subsection{基于内容的说话人建模}</span></p><p class="ds-markdown-paragraph"><span>\subsubsection{从显式嵌入到隐式学习}</span><br><span>\textbf{V1 方法：}</span><br><span>\begin{itemize}</span><br><span>\item 使用预训练的 CAMPPlus 模型提取说话人嵌入</span><br><span>\item 显式地将说话人身份作为条件输入</span><br><span>\item 需要额外的说话人验证模型和特征提取流程</span><br><span>\end{itemize}</span></p><p class="ds-markdown-paragraph"><span>\textbf{V2 方法：}</span><br><span>\begin{itemize}</span><br><span>\item 让语言模型直接从语音令牌中学习说话人特征</span><br><span>\item 隐式地在语音令牌序列中编码说话人信息</span><br><span>\item 端到端学习，无需额外的说话人建模组件</span><br><span>\end{itemize}</span></p><p class="ds-markdown-paragraph"><span>\subsubsection{语音令牌的信息容量}</span><br><span>\textbf{技术依据：}</span><br><span>\begin{itemize}</span><br><span>\item 语音令牌序列本身就包含丰富的说话人特征（音色、音调、发音习惯）</span><br><span>\item 语言模型具有足够的能力从上下文中提取说话人信息</span><br><span>\item 避免了说话人嵌入的信息瓶颈</span><br><span>\end{itemize}</span></p><p class="ds-markdown-paragraph"><span>\subsection{零样本语音克隆的优化}</span></p><p class="ds-markdown-paragraph"><span>\subsubsection{参考音频的全面利用}</span><br><span>\textbf{V1 限制：}</span><br><span>\begin{itemize}</span><br><span>\item 说话人嵌入只能捕获全局的说话人特征</span><br><span>\item 无法捕捉参考音频中的细粒度发音风格和情感</span><br><span>\end{itemize}</span></p><p class="ds-markdown-paragraph"><span>\textbf{V2 改进：}</span><br><span>\begin{itemize}</span><br><span>\item 使用完整的参考音频令牌序列作为条件</span><br><span>\item 同时捕获说话人身份和具体的发音风格</span><br><span>\item 支持更精准的语音克隆</span><br><span>\end{itemize}</span></p><p class="ds-markdown-paragraph"><span>\subsubsection{条件生成范式的改变}</span></p><span class="katex-display ds-markdown-math"><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><semantics><mrow><mtext>V1:&nbsp;</mtext><mi>P</mi><mo stretchy="false">(</mo><mtext>语音</mtext><mi mathvariant="normal">∣</mi><mtext>文本</mtext><mo separator="true">,</mo><mtext>说话人嵌入</mtext><mo stretchy="false">)</mo></mrow><annotation encoding="application/x-tex">\text{V1: } P(\text{语音} | \text{文本}, \text{说话人嵌入})</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:1em;vertical-align:-0.25em;"></span><span class="mord text"><span class="mord">V1:&nbsp;</span></span><span class="mord mathnormal" style="margin-right:0.13889em;">P</span><span class="mopen">(</span><span class="mord text"><span class="mord cjk_fallback">语音</span></span><span class="mord">∣</span><span class="mord text"><span class="mord cjk_fallback">文本</span></span><span class="mpunct">,</span><span class="mspace" style="margin-right:0.1667em;"></span><span class="mord text"><span class="mord cjk_fallback">说话人嵌入</span></span><span class="mclose">)</span></span></span></span></span><span class="katex-display ds-markdown-math"><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><semantics><mrow><mtext>V2:&nbsp;</mtext><mi>P</mi><mo stretchy="false">(</mo><mtext>语音</mtext><mi mathvariant="normal">∣</mi><mtext>文本</mtext><mo separator="true">,</mo><mtext>参考语音令牌</mtext><mo stretchy="false">)</mo></mrow><annotation encoding="application/x-tex">\text{V2: } P(\text{语音} | \text{文本}, \text{参考语音令牌})</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:1em;vertical-align:-0.25em;"></span><span class="mord text"><span class="mord">V2:&nbsp;</span></span><span class="mord mathnormal" style="margin-right:0.13889em;">P</span><span class="mopen">(</span><span class="mord text"><span class="mord cjk_fallback">语音</span></span><span class="mord">∣</span><span class="mord text"><span class="mord cjk_fallback">文本</span></span><span class="mpunct">,</span><span class="mspace" style="margin-right:0.1667em;"></span><span class="mord text"><span class="mord cjk_fallback">参考语音令牌</span></span><span class="mclose">)</span></span></span></span></span><p class="ds-markdown-paragraph"><span>\subsection{训练效率和稳定性}</span></p><p class="ds-markdown-paragraph"><span>\subsubsection{减少训练目标}</span><br><span>\begin{itemize}</span><br><span>\item \textbf{V1}: 需要同时优化文本到语义令牌的映射和说话人条件的适配</span><br><span>\item \textbf{V2}: 只需优化文本到语音令牌的单一目标</span><br><span>\item \textbf{优势}: 训练更稳定，收敛更快</span><br><span>\end{itemize}</span></p><p class="ds-markdown-paragraph"><span>\subsubsection{简化数据流水线}</span><br><span>\textbf{移除的步骤：}</span><br><span>\begin{itemize}</span><br><span>\item 说话人嵌入提取流程</span><br><span>\item 说话人嵌入的存储和管理</span><br><span>\item 嵌入向量的归一化和对齐处理</span><br><span>\end{itemize}</span></p><p class="ds-markdown-paragraph"><span>\subsection{技术趋势对齐}</span></p><p class="ds-markdown-paragraph"><span>\subsubsection{大语言模型范式}</span><br><span>\textbf{行业趋势：}</span><br><span>\begin{itemize}</span><br><span>\item 现代 TTS 系统趋向于使用统一的语言模型架构</span><br><span>\item 减少手工设计的特征和组件</span><br><span>\item 让模型自动学习所有必要的表示</span><br><span>\end{itemize}</span></p><p class="ds-markdown-paragraph"><span>\textbf{CosyVoiceV2 的对齐：}</span><br><span>\begin{itemize}</span><br><span>\item 采用纯自回归语言模型架构</span><br><span>\item 统一的令牌空间处理文本和语音</span><br><span>\item 简化条件生成机制</span><br><span>\end{itemize}</span></p><p class="ds-markdown-paragraph"><span>\subsubsection{可扩展性考虑}</span><br><span>\begin{itemize}</span><br><span>\item \textbf{说话人嵌入的局限性}: 难以扩展到海量说话人</span><br><span>\item \textbf{令牌化的优势}: 统一的离散表示，易于扩展</span><br><span>\item \textbf{零样本学习的需要}: 避免对预定义说话人集合的依赖</span><br><span>\end{itemize}</span></p><p class="ds-markdown-paragraph"><span>\subsection{性能优势}</span></p><p class="ds-markdown-paragraph"><span>\subsubsection{生成质量的提升}</span><br><span>\textbf{实证发现：}</span><br><span>\begin{itemize}</span><br><span>\item 基于参考音频的完整条件生成比说话人嵌入生成质量更高</span><br><span>\item 语音令牌序列包含更丰富的韵律和风格信息</span><br><span>\item 减少信息损失，提高合成语音的自然度</span><br><span>\end{itemize}</span></p><p class="ds-markdown-paragraph"><span>\subsubsection{灵活性的增强}</span><br><span>\begin{itemize}</span><br><span>\item \textbf{跨语言适应}: 无需为不同语言训练不同的说话人嵌入</span><br><span>\item \textbf{风格迁移}: 更容易实现不同说话风格的控制</span><br><span>\item \textbf{长音频生成}: 更好地保持长时间的一致性</span><br><span>\end{itemize}</span></p><p class="ds-markdown-paragraph"><span>\subsection{架构对比}</span></p><p class="ds-markdown-paragraph"><span>\begin{table}[h]</span><br><span>\centering</span><br><span>\caption{CosyVoice V1 vs V2 说话人处理方式对比}</span><br><span>\begin{tabular}{p{5cm}p{5cm}}</span><br><span>\toprule</span><br><span>\textbf{CosyVoice V1 (使用说话人嵌入)} &amp; \textbf{CosyVoice V2 (移除说话人嵌入)} \</span><br><span>\midrule</span><br><span>多模态输入：文本 + 语音令牌 + 说话人嵌入 &amp; 统一输入：文本 + 语音令牌 \</span><br><span>\hline</span><br><span>显式说话人条件控制 &amp; 隐式从参考音频学习说话人特征 \</span><br><span>\hline</span><br><span>需要预训练的说话人验证模型 &amp; 端到端学习，无需额外组件 \</span><br><span>\hline</span><br><span>说话人身份和风格分离 &amp; 统一的风格和身份表示 \</span><br><span>\hline</span><br><span>有限说话人扩展性 &amp; 理论上无限的说话人支持 \</span><br><span>\hline</span><br><span>复杂的数据预处理流水线 &amp; 简化的数据处理流程 \</span><br><span>\bottomrule</span><br><span>\end{tabular}</span><br><span>\end{table}</span></p><p class="ds-markdown-paragraph"><span>\subsection{总结}</span></p><p class="ds-markdown-paragraph"><span>CosyVoiceV2 移除说话人嵌入的决定是基于多个技术考量的综合结果：</span></p><p class="ds-markdown-paragraph"><span>\begin{itemize}</span><br><span>\item \textbf{架构简化}: 统一的语言模型范式，减少组件复杂性</span><br><span>\item \textbf{性能提升}: 基于参考音频的条件生成质量更高</span><br><span>\item \textbf{训练效率}: 单一优化目标，训练更稳定</span><br><span>\item \textbf{扩展性}: 支持无限的说话人和风格</span><br><span>\item \textbf{趋势对齐}: 符合大语言模型在 TTS 中的应用趋势</span><br><span>\end{itemize}</span></p><p class="ds-markdown-paragraph"><span>这一设计选择使得 CosyVoiceV2 在保持高质量语音合成的同时，实现了更简洁、更高效的架构，为未来的扩展和优化奠定了更好的基础。</span></p>

---

### 用户

Annotation Categories
The NVSpeech dataset includes annotations for the following paralinguistic vocalization categories:

[Breathing]
[Laughter]
[Cough]
[Sigh]
[Confirmation-en]
[Question-en]
[Question-ah]
[Question-oh]
[Surprise-ah]
[Surprise-oh]
[Dissatisfaction-hnn]
[Uhm]
[Shh]
[Crying]
[Surprise-wa]
[Surprise-yo]
[Question-ei]
[Question-yi]把上述语气词token写进tokenizer文件中class QwenTokenizer():
    def __init__(self, token_path, skip_special_tokens=True):
        super().__init__()
        # NOTE: non-chat model, all these special tokens keep randomly initialized.
        special_tokens = {
            'eos_token': '<|endoftext|>',
            'pad_token': '<|endoftext|>',
            'additional_special_tokens': [
                '<|im_start|>', '<|im_end|>', '<|endofprompt|>',
                '[breath]', '<strong>', '</strong>', '[noise]',
                '[laughter]', '[cough]', '[clucking]', '[accent]',
                '[quick_breath]',
                "<laughter>", "</laughter>",
                "[hissing]", "[sigh]", "[vocalized-noise]",
                "[lipsmack]", "[mn]"
            ]
        }
        self.special_tokens = special_tokens
        self.tokenizer = AutoTokenizer.from_pretrained(token_path)
        self.tokenizer.add_special_tokens(special_tokens)
        self.skip_special_tokens = skip_special_tokens

    def encode(self, text, **kwargs):
        tokens = self.tokenizer([text], return_tensors="pt")
        tokens = tokens["input_ids"][0].cpu().tolist()
        return tokens

    def decode(self, tokens):
        tokens = torch.tensor(tokens, dtype=torch.int64)
        text = self.tokenizer.batch_decode([tokens], skip_special_tokens=self.skip_special_tokens)[0]
        return text


@lru_cache(maxsize=None)
def get_qwen_tokenizer(
    token_path: str,
    skip_special_tokens: bool
) -> QwenTokenizer:
    return QwenTokenizer(token_path=token_path, skip_special_tokens=skip_special_tokens)

---

### DeepSeek AI

<p>思考：</p><blockquote><p class="ds-markdown-paragraph"><span>我们首先需要将给定的语气词类别添加到tokenizer的特殊令牌中。注意，给定的类别列表中有一些已经存在于特殊令牌中（如[laughter]和[cough]），但有些是新的。我们需要将新的类别添加到</span>`additional_special_tokens`<span>列表中。</span></p><p class="ds-markdown-paragraph"><span>给定的类别列表：</span><br><span>[Breathing] -&gt; 已存在[breath]（注意大小写，但通常不区分，但为了统一，我们使用小写）</span><br><span>[Laughter] -&gt; 已存在[laughter]</span><br><span>[Cough] -&gt; 已存在[cough]</span><br><span>[Sigh] -&gt; 已存在[sigh]</span><br><span>[Confirmation-en] -&gt; 新增</span><br><span>[Question-en] -&gt; 新增</span><br><span>[Question-ah] -&gt; 新增</span><br><span>[Question-oh] -&gt; 新增</span><br><span>[Surprise-ah] -&gt; 新增</span><br><span>[Surprise-oh] -&gt; 新增</span><br><span>[Dissatisfaction-hnn] -&gt; 新增</span><br><span>[Uhm] -&gt; 新增</span><br><span>[Shh] -&gt; 新增</span><br><span>[Crying] -&gt; 新增</span><br><span>[Surprise-wa] -&gt; 新增</span><br><span>[Surprise-yo] -&gt; 新增</span><br><span>[Question-ei] -&gt; 新增</span><br><span>[Question-yi] -&gt; 新增</span></p><p class="ds-markdown-paragraph"><span>注意：原特殊令牌中已经有一些，我们只需要添加没有的。</span></p><p class="ds-markdown-paragraph"><span>另外，原特殊令牌中已经有的一些标记，我们不再重复添加。我们检查原</span>`additional_special_tokens`<span>列表，然后添加新的。</span></p><p class="ds-markdown-paragraph"><span>我们假设这些标记都是小写，并且用方括号括起来。注意原列表中的标记有些没有方括号，但这里给定的类别都有方括号，所以我们统一用方括号。</span></p><p class="ds-markdown-paragraph"><span>步骤：</span></p><ol start="1"><li><p class="ds-markdown-paragraph"><span>定义新的语气词标记列表，包括所有给定的类别（转换为小写，并确保有方括号）。</span></p></li><li><p class="ds-markdown-paragraph"><span>检查原特殊令牌的</span>`additional_special_tokens`<span>列表，将新列表中不存在的添加进去。</span></p></li></ol><p class="ds-markdown-paragraph"><span>注意：原特殊令牌中已经有一些标记，例如'[breath]', '[laughter]', '[cough]', '[sigh]'，所以这些我们不再添加。</span></p><p class="ds-markdown-paragraph"><span>我们先将给定的类别列表转换为小写，然后去重，并排除已经存在的。</span></p><p class="ds-markdown-paragraph"><span>原</span>`additional_special_tokens`<span>列表：</span><br><span>['&lt;|im_start|&gt;', '&lt;|im_end|&gt;', '&lt;|endofprompt|&gt;',</span><br><span>'[breath]', '</span><span class="ds-markdown-html">&lt;strong&gt;</span><span>', '</span><span class="ds-markdown-html">&lt;/strong&gt;</span><span>', '[noise]',</span><br><span>'[laughter]', '[cough]', '[clucking]', '[accent]',</span><br><span>'[quick_breath]',</span><br><span>"</span><span class="ds-markdown-html">&lt;laughter&gt;</span><span>", "</span><span class="ds-markdown-html">&lt;/laughter&gt;</span><span>",</span><br><span>"[hissing]", "[sigh]", "[vocalized-noise]",</span><br><span>"[lipsmack]", "[mn]"]</span></p><p class="ds-markdown-paragraph"><span>注意：原列表中已有'[breath]', '[laughter]', '[cough]', '[sigh]'，所以这些我们不再添加。</span></p><p class="ds-markdown-paragraph"><span>我们创建新的标记列表，包括：</span><br><span>[confirmation-en], [question-en], [question-ah], [question-oh],</span><br><span>[surprise-ah], [surprise-oh], [dissatisfaction-hnn], [uhm], [shh],</span><br><span>[crying], [surprise-wa], [surprise-yo], [question-ei], [question-yi]</span></p><p class="ds-markdown-paragraph"><span>注意：原列表中有一些标记是重复的，例如既有[laughter]也有</span><span class="ds-markdown-html">&lt;laughter&gt;</span><span>，但我们按照给定的类别列表，使用方括号格式。</span></p><p class="ds-markdown-paragraph"><span>我们只添加方括号格式的标记。</span></p><p class="ds-markdown-paragraph"><span>修改方法：在</span>`special_tokens`<span>字典的</span>`additional_special_tokens`<span>列表中，添加这些新标记。</span></p><p class="ds-markdown-paragraph"><span>注意：我们不应该重复添加已经存在的标记。</span></p><p class="ds-markdown-paragraph"><span>我们可以在初始化时，先定义基础的特殊令牌，然后添加新的。</span></p><p class="ds-markdown-paragraph"><span>另外，注意原代码中已经将特殊令牌添加到了tokenizer中，所以我们只需要在初始化时正确设置</span>`special_tokens`<span>即可。</span></p><p class="ds-markdown-paragraph"><span>我们修改</span>`special_tokens`<span>中的</span>`additional_special_tokens`<span>列表，将新标记添加进去。</span></p><p class="ds-markdown-paragraph"><span>代码修改如下：</span></p></blockquote><br/><div class="md-code-block md-code-block-light"><div class="md-code-block-banner-wrap"><div class="md-code-block-banner md-code-block-banner-lite"><div class="_121d384"><div class="d2a24f03"><span class="d813de27">python</span></div><div class="d2a24f03 _246a029"><div class="efa13877"><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon" style="margin-right: 4px;"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.14923 4.02032C7.11191 4.02032 7.87977 4.02017 8.49591 4.07599C9.12122 4.1327 9.65786 4.25188 10.1414 4.53107C10.7201 4.8653 11.2008 5.34591 11.535 5.92462C11.8142 6.40818 11.9333 6.94482 11.9901 7.57013C12.0459 8.18625 12.0457 8.9542 12.0457 9.91681C12.0457 10.8795 12.0459 11.6474 11.9901 12.2635C11.9333 12.8888 11.8142 13.4254 11.535 13.909C11.2008 14.4877 10.7201 14.9683 10.1414 15.3026C9.65786 15.5817 9.12122 15.7009 8.49591 15.7576C7.87977 15.8134 7.1119 15.8133 6.14923 15.8133C5.18661 15.8133 4.41868 15.8134 3.80255 15.7576C3.17724 15.7009 2.6406 15.5817 2.15704 15.3026C1.57834 14.9684 1.09772 14.4877 0.763489 13.909C0.484305 13.4254 0.365123 12.8888 0.308411 12.2635C0.252587 11.6474 0.252747 10.8795 0.252747 9.91681C0.252747 8.95419 0.252603 8.18625 0.308411 7.57013C0.365123 6.94482 0.484305 6.40818 0.763489 5.92462C1.09771 5.3459 1.57833 4.86529 2.15704 4.53107C2.6406 4.25188 3.17724 4.1327 3.80255 4.07599C4.41868 4.02018 5.1866 4.02032 6.14923 4.02032ZM6.14923 5.37775C5.16175 5.37775 4.46628 5.37761 3.9256 5.42657C3.39428 5.47473 3.07853 5.56574 2.83575 5.70587C2.46313 5.92106 2.15348 6.23071 1.93829 6.60333C1.79817 6.84611 1.70715 7.16185 1.659 7.69318C1.61004 8.23385 1.61017 8.92934 1.61017 9.91681C1.61017 10.9043 1.61002 11.5998 1.659 12.1404C1.70715 12.6717 1.79817 12.9875 1.93829 13.2303C2.15349 13.6029 2.46315 13.9126 2.83575 14.1277C3.07853 14.2679 3.39428 14.3589 3.9256 14.407C4.46628 14.456 5.16176 14.4559 6.14923 14.4559C7.13675 14.4559 7.83218 14.456 8.37286 14.407C8.90419 14.3589 9.21993 14.2679 9.46271 14.1277C9.83529 13.9126 10.145 13.6029 10.3602 13.2303C10.5003 12.9875 10.5913 12.6718 10.6395 12.1404C10.6884 11.5998 10.6883 10.9043 10.6883 9.91681C10.6883 8.92935 10.6884 8.23385 10.6395 7.69318C10.5913 7.16185 10.5003 6.84611 10.3602 6.60333C10.145 6.23072 9.8353 5.92107 9.46271 5.70587C9.21993 5.56574 8.90418 5.47473 8.37286 5.42657C7.83218 5.3776 7.13676 5.37775 6.14923 5.37775ZM9.80157 0.367981C10.7637 0.367981 11.5313 0.367886 12.1473 0.423645C12.7725 0.480313 13.3093 0.598765 13.7928 0.877747C14.3716 1.21192 14.852 1.69355 15.1863 2.27228C15.4655 2.75575 15.5857 3.29165 15.6424 3.91681C15.6982 4.53301 15.6971 5.30161 15.6971 6.26447V7.8299C15.6971 8.29265 15.6989 8.58994 15.6649 8.84845C15.4667 10.3525 14.4009 11.5738 12.9832 11.9988V10.5467C13.6973 10.1903 14.2104 9.49662 14.3192 8.67169C14.3387 8.52348 14.3406 8.3358 14.3406 7.8299V6.26447C14.3406 5.27707 14.3398 4.58149 14.2908 4.04083C14.2427 3.50969 14.1526 3.19373 14.0125 2.95099C13.7974 2.5785 13.4875 2.2687 13.1151 2.05353C12.8723 1.91347 12.5563 1.82237 12.0252 1.77423C11.4846 1.72528 10.7888 1.7254 9.80157 1.7254H7.71466C6.75614 1.72559 5.92659 2.27697 5.52325 3.07892H4.07013C4.54215 1.51132 5.99314 0.368192 7.71466 0.367981H9.80157Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">复制</span></span><div class="ds-focus-ring"></div></button><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M15.3695 11.411L15.1234 12.8866C14.8869 14.3042 13.6603 15.3436 12.223 15.3436H3.7767C2.33954 15.3434 1.11276 14.3042 0.876312 12.8866L0.630219 11.411L2.05405 11.1747L2.29916 12.6493C2.41969 13.3713 3.04472 13.9001 3.7767 13.9003H12.223C12.9551 13.9002 13.58 13.3713 13.7005 12.6493L13.9456 11.1747L15.3695 11.411ZM8.72202 8.994C8.77714 8.93934 8.83789 8.88106 8.90268 8.81627L12.4828 5.23424L13.5042 6.25572L9.92221 9.8358C9.63947 10.1185 9.3876 10.3732 9.15854 10.5575C8.91889 10.7503 8.6395 10.9224 8.28647 10.9784C8.09708 11.0083 7.9036 11.0083 7.7142 10.9784C7.36103 10.9224 7.08087 10.7503 6.84116 10.5575C6.61212 10.3732 6.36019 10.1185 6.07748 9.8358L2.49643 6.25572L3.51694 5.23424L7.09702 8.81627C7.16216 8.88142 7.22327 8.94006 7.27866 8.99498V1.3065H8.72202V8.994Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">下载</span></span><div class="ds-focus-ring"></div></button></div></div></div></div></div><pre><span class="token keyword">class</span> <span class="token class-name">QwenTokenizer</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">:</span>
    <span class="token keyword">def</span> <span class="token function">__init__</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> token_path<span class="token punctuation">,</span> skip_special_tokens<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span><span class="token punctuation">:</span>
        <span class="token builtin">super</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span>__init__<span class="token punctuation">(</span><span class="token punctuation">)</span>
        <span class="token comment"># NOTE: non-chat model, all these special tokens keep randomly initialized.</span>
        special_tokens <span class="token operator">=</span> <span class="token punctuation">{</span>
            <span class="token string">'eos_token'</span><span class="token punctuation">:</span> <span class="token string">'&lt;|endoftext|&gt;'</span><span class="token punctuation">,</span>
            <span class="token string">'pad_token'</span><span class="token punctuation">:</span> <span class="token string">'&lt;|endoftext|&gt;'</span><span class="token punctuation">,</span>
            <span class="token string">'additional_special_tokens'</span><span class="token punctuation">:</span> <span class="token punctuation">[</span>
                <span class="token string">'&lt;|im_start|&gt;'</span><span class="token punctuation">,</span> <span class="token string">'&lt;|im_end|&gt;'</span><span class="token punctuation">,</span> <span class="token string">'&lt;|endofprompt|&gt;'</span><span class="token punctuation">,</span>
                <span class="token comment"># 原有语气词</span>
                <span class="token string">'[breath]'</span><span class="token punctuation">,</span> <span class="token string">'&lt;strong&gt;'</span><span class="token punctuation">,</span> <span class="token string">'&lt;/strong&gt;'</span><span class="token punctuation">,</span> <span class="token string">'[noise]'</span><span class="token punctuation">,</span>
                <span class="token string">'[laughter]'</span><span class="token punctuation">,</span> <span class="token string">'[cough]'</span><span class="token punctuation">,</span> <span class="token string">'[clucking]'</span><span class="token punctuation">,</span> <span class="token string">'[accent]'</span><span class="token punctuation">,</span>
                <span class="token string">'[quick_breath]'</span><span class="token punctuation">,</span>
                <span class="token string">"&lt;laughter&gt;"</span><span class="token punctuation">,</span> <span class="token string">"&lt;/laughter&gt;"</span><span class="token punctuation">,</span>
                <span class="token string">"[hissing]"</span><span class="token punctuation">,</span> <span class="token string">"[sigh]"</span><span class="token punctuation">,</span> <span class="token string">"[vocalized-noise]"</span><span class="token punctuation">,</span>
                <span class="token string">"[lipsmack]"</span><span class="token punctuation">,</span> <span class="token string">"[mn]"</span><span class="token punctuation">,</span>
                
                <span class="token comment"># NVSpeech 数据集新增语气词</span>
                <span class="token comment"># 呼吸相关</span>
                <span class="token string">"[breathing]"</span><span class="token punctuation">,</span>  <span class="token comment"># 呼吸声</span>
                
                <span class="token comment"># 笑声和咳嗽</span>
                <span class="token string">"[laughter]"</span><span class="token punctuation">,</span>    <span class="token comment"># 笑声（已存在，保留）</span>
                <span class="token string">"[cough]"</span><span class="token punctuation">,</span>      <span class="token comment"># 咳嗽（已存在，保留）</span>
                <span class="token string">"[sigh]"</span><span class="token punctuation">,</span>       <span class="token comment"># 叹气（已存在，保留）</span>
                
                <span class="token comment"># 确认和疑问语气</span>
                <span class="token string">"[confirmation-en]"</span><span class="token punctuation">,</span>    <span class="token comment"># 英语确认语气</span>
                <span class="token string">"[question-en]"</span><span class="token punctuation">,</span>        <span class="token comment"># 英语疑问语气</span>
                <span class="token string">"[question-ah]"</span><span class="token punctuation">,</span>        <span class="token comment"># "啊"疑问语气</span>
                <span class="token string">"[question-oh]"</span><span class="token punctuation">,</span>        <span class="token comment"># "哦"疑问语气</span>
                <span class="token string">"[question-ei]"</span><span class="token punctuation">,</span>        <span class="token comment"># "诶"疑问语气</span>
                <span class="token string">"[question-yi]"</span><span class="token punctuation">,</span>        <span class="token comment"># "咦"疑问语气</span>
                
                <span class="token comment"># 惊讶语气</span>
                <span class="token string">"[surprise-ah]"</span><span class="token punctuation">,</span>        <span class="token comment"># "啊"惊讶语气</span>
                <span class="token string">"[surprise-oh]"</span><span class="token punctuation">,</span>        <span class="token comment"># "哦"惊讶语气</span>
                <span class="token string">"[surprise-wa]"</span><span class="token punctuation">,</span>        <span class="token comment"># "哇"惊讶语气</span>
                <span class="token string">"[surprise-yo]"</span><span class="token punctuation">,</span>        <span class="token comment"># "哟"惊讶语气</span>
                
                <span class="token comment"># 不满和思考语气</span>
                <span class="token string">"[dissatisfaction-hnn]"</span><span class="token punctuation">,</span> <span class="token comment"># "哼"不满语气</span>
                <span class="token string">"[uhm]"</span><span class="token punctuation">,</span>                <span class="token comment"># "嗯"思考语气</span>
                
                <span class="token comment"># 其他声音</span>
                <span class="token string">"[shh]"</span><span class="token punctuation">,</span>                <span class="token comment"># "嘘"声</span>
                <span class="token string">"[crying]"</span>              <span class="token comment"># 哭泣声</span>
            <span class="token punctuation">]</span>
        <span class="token punctuation">}</span>
        self<span class="token punctuation">.</span>special_tokens <span class="token operator">=</span> special_tokens
        self<span class="token punctuation">.</span>tokenizer <span class="token operator">=</span> AutoTokenizer<span class="token punctuation">.</span>from_pretrained<span class="token punctuation">(</span>token_path<span class="token punctuation">)</span>
        self<span class="token punctuation">.</span>tokenizer<span class="token punctuation">.</span>add_special_tokens<span class="token punctuation">(</span>special_tokens<span class="token punctuation">)</span>
        self<span class="token punctuation">.</span>skip_special_tokens <span class="token operator">=</span> skip_special_tokens

    <span class="token keyword">def</span> <span class="token function">encode</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> text<span class="token punctuation">,</span> <span class="token operator">**</span>kwargs<span class="token punctuation">)</span><span class="token punctuation">:</span>
        tokens <span class="token operator">=</span> self<span class="token punctuation">.</span>tokenizer<span class="token punctuation">(</span><span class="token punctuation">[</span>text<span class="token punctuation">]</span><span class="token punctuation">,</span> return_tensors<span class="token operator">=</span><span class="token string">"pt"</span><span class="token punctuation">)</span>
        tokens <span class="token operator">=</span> tokens<span class="token punctuation">[</span><span class="token string">"input_ids"</span><span class="token punctuation">]</span><span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">.</span>cpu<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span>tolist<span class="token punctuation">(</span><span class="token punctuation">)</span>
        <span class="token keyword">return</span> tokens

    <span class="token keyword">def</span> <span class="token function">decode</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> tokens<span class="token punctuation">)</span><span class="token punctuation">:</span>
        tokens <span class="token operator">=</span> torch<span class="token punctuation">.</span>tensor<span class="token punctuation">(</span>tokens<span class="token punctuation">,</span> dtype<span class="token operator">=</span>torch<span class="token punctuation">.</span>int64<span class="token punctuation">)</span>
        text <span class="token operator">=</span> self<span class="token punctuation">.</span>tokenizer<span class="token punctuation">.</span>batch_decode<span class="token punctuation">(</span><span class="token punctuation">[</span>tokens<span class="token punctuation">]</span><span class="token punctuation">,</span> skip_special_tokens<span class="token operator">=</span>self<span class="token punctuation">.</span>skip_special_tokens<span class="token punctuation">)</span><span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span>
        <span class="token keyword">return</span> text


<span class="token decorator annotation punctuation">@lru_cache</span><span class="token punctuation">(</span>maxsize<span class="token operator">=</span><span class="token boolean">None</span><span class="token punctuation">)</span>
<span class="token keyword">def</span> <span class="token function">get_qwen_tokenizer</span><span class="token punctuation">(</span>
    token_path<span class="token punctuation">:</span> <span class="token builtin">str</span><span class="token punctuation">,</span>
    skip_special_tokens<span class="token punctuation">:</span> <span class="token builtin">bool</span>
<span class="token punctuation">)</span> <span class="token operator">-</span><span class="token operator">&gt;</span> QwenTokenizer<span class="token punctuation">:</span>
    <span class="token keyword">return</span> QwenTokenizer<span class="token punctuation">(</span>token_path<span class="token operator">=</span>token_path<span class="token punctuation">,</span> skip_special_tokens<span class="token operator">=</span>skip_special_tokens<span class="token punctuation">)</span></pre><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _33882ae"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _28d7e84"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg></div><p class="ds-markdown-paragraph"><span>主要修改说明：</span></p><ol start="1"><li><p class="ds-markdown-paragraph"><strong><span>保留了原有的语气词</span></strong><span>：确保向后兼容性</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>新增 NVSpeech 语气词</span></strong><span>：按照原数据集的分类添加</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>分类组织</span></strong><span>：</span></p><ul><li><p class="ds-markdown-paragraph"><span>呼吸相关：</span>`[breathing]`</p></li><li><p class="ds-markdown-paragraph"><span>笑声咳嗽：</span>`[laughter]`<span>, </span>`[cough]`<span>, </span>`[sigh]`</p></li><li><p class="ds-markdown-paragraph"><span>疑问确认：</span>`[confirmation-en]`<span>, </span>`[question-en]`<span>, </span>`[question-ah]`<span>, </span>`[question-oh]`<span>, </span>`[question-ei]`<span>, </span>`[question-yi]`</p></li><li><p class="ds-markdown-paragraph"><span>惊讶语气：</span>`[surprise-ah]`<span>, </span>`[surprise-oh]`<span>, </span>`[surprise-wa]`<span>, </span>`[surprise-yo]`</p></li><li><p class="ds-markdown-paragraph"><span>其他情感：</span>`[dissatisfaction-hnn]`<span>, </span>`[uhm]`<span>, </span>`[shh]`<span>, </span>`[crying]`</p></li></ul></li><li><p class="ds-markdown-paragraph"><strong><span>重复项处理</span></strong><span>：</span>`[laughter]`<span>, </span>`[cough]`<span>, </span>`[sigh]`<span> 在原有列表中已存在，保留一个即可</span></p></li></ol><p class="ds-markdown-paragraph"><span>这样修改后，tokenizer 就能正确处理 NVSpeech 数据集中的所有语气词标注了。</span></p>

---

### 用户

这里的“en”不是表示英语，而是表示“嗯”

---

### DeepSeek AI

<p>思考：</p><blockquote><p class="ds-markdown-paragraph"><span>根据用户反馈，将原本理解为英语（English）的“en”更正为表示中文语气词“嗯”。因此，需要将对应的token进行重命名。</span><br><span>原计划中的[confirmation-en]和[question-en]中的“en”应理解为“嗯”，所以将它们改为更符合中文习惯的表示。</span></p><p class="ds-markdown-paragraph"><span>修改如下：</span><br><span>[confirmation-en] -&gt; [confirmation-enn]   # 表示确认的“嗯”</span><br><span>[question-en] -&gt; [question-enn]           # 表示疑问的“嗯”</span></p><p class="ds-markdown-paragraph"><span>但是，注意原数据集中还有其他的疑问和惊讶语气，例如[question-ah]等，我们保持这些不变，因为ah、oh等是常见的语气词。</span></p><p class="ds-markdown-paragraph"><span>同时，我们注意到数据集中还有[uhm]这个token，它也是表示“嗯”的一种，通常表示犹豫或思考。所以保留[uhm]不变。</span></p><p class="ds-markdown-paragraph"><span>因此，我们将两个带有“en”的token改为“enn”以避免歧义，同时更符合中文发音。</span></p><p class="ds-markdown-paragraph"><span>另外，为了保持一致性，我们将所有语气词token都使用小写，并且用连字符连接单词。</span></p><p class="ds-markdown-paragraph"><span>修改后的特殊token列表如下：</span></p></blockquote><br/><p class="ds-markdown-paragraph"><span>您说得对，我来修正这些语气词标记，将"en"理解为中文的"嗯"而不是英语：</span></p><div class="md-code-block md-code-block-light"><div class="md-code-block-banner-wrap"><div class="md-code-block-banner md-code-block-banner-lite"><div class="_121d384"><div class="d2a24f03"><span class="d813de27">python</span></div><div class="d2a24f03 _246a029"><div class="efa13877"><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon" style="margin-right: 4px;"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.14923 4.02032C7.11191 4.02032 7.87977 4.02017 8.49591 4.07599C9.12122 4.1327 9.65786 4.25188 10.1414 4.53107C10.7201 4.8653 11.2008 5.34591 11.535 5.92462C11.8142 6.40818 11.9333 6.94482 11.9901 7.57013C12.0459 8.18625 12.0457 8.9542 12.0457 9.91681C12.0457 10.8795 12.0459 11.6474 11.9901 12.2635C11.9333 12.8888 11.8142 13.4254 11.535 13.909C11.2008 14.4877 10.7201 14.9683 10.1414 15.3026C9.65786 15.5817 9.12122 15.7009 8.49591 15.7576C7.87977 15.8134 7.1119 15.8133 6.14923 15.8133C5.18661 15.8133 4.41868 15.8134 3.80255 15.7576C3.17724 15.7009 2.6406 15.5817 2.15704 15.3026C1.57834 14.9684 1.09772 14.4877 0.763489 13.909C0.484305 13.4254 0.365123 12.8888 0.308411 12.2635C0.252587 11.6474 0.252747 10.8795 0.252747 9.91681C0.252747 8.95419 0.252603 8.18625 0.308411 7.57013C0.365123 6.94482 0.484305 6.40818 0.763489 5.92462C1.09771 5.3459 1.57833 4.86529 2.15704 4.53107C2.6406 4.25188 3.17724 4.1327 3.80255 4.07599C4.41868 4.02018 5.1866 4.02032 6.14923 4.02032ZM6.14923 5.37775C5.16175 5.37775 4.46628 5.37761 3.9256 5.42657C3.39428 5.47473 3.07853 5.56574 2.83575 5.70587C2.46313 5.92106 2.15348 6.23071 1.93829 6.60333C1.79817 6.84611 1.70715 7.16185 1.659 7.69318C1.61004 8.23385 1.61017 8.92934 1.61017 9.91681C1.61017 10.9043 1.61002 11.5998 1.659 12.1404C1.70715 12.6717 1.79817 12.9875 1.93829 13.2303C2.15349 13.6029 2.46315 13.9126 2.83575 14.1277C3.07853 14.2679 3.39428 14.3589 3.9256 14.407C4.46628 14.456 5.16176 14.4559 6.14923 14.4559C7.13675 14.4559 7.83218 14.456 8.37286 14.407C8.90419 14.3589 9.21993 14.2679 9.46271 14.1277C9.83529 13.9126 10.145 13.6029 10.3602 13.2303C10.5003 12.9875 10.5913 12.6718 10.6395 12.1404C10.6884 11.5998 10.6883 10.9043 10.6883 9.91681C10.6883 8.92935 10.6884 8.23385 10.6395 7.69318C10.5913 7.16185 10.5003 6.84611 10.3602 6.60333C10.145 6.23072 9.8353 5.92107 9.46271 5.70587C9.21993 5.56574 8.90418 5.47473 8.37286 5.42657C7.83218 5.3776 7.13676 5.37775 6.14923 5.37775ZM9.80157 0.367981C10.7637 0.367981 11.5313 0.367886 12.1473 0.423645C12.7725 0.480313 13.3093 0.598765 13.7928 0.877747C14.3716 1.21192 14.852 1.69355 15.1863 2.27228C15.4655 2.75575 15.5857 3.29165 15.6424 3.91681C15.6982 4.53301 15.6971 5.30161 15.6971 6.26447V7.8299C15.6971 8.29265 15.6989 8.58994 15.6649 8.84845C15.4667 10.3525 14.4009 11.5738 12.9832 11.9988V10.5467C13.6973 10.1903 14.2104 9.49662 14.3192 8.67169C14.3387 8.52348 14.3406 8.3358 14.3406 7.8299V6.26447C14.3406 5.27707 14.3398 4.58149 14.2908 4.04083C14.2427 3.50969 14.1526 3.19373 14.0125 2.95099C13.7974 2.5785 13.4875 2.2687 13.1151 2.05353C12.8723 1.91347 12.5563 1.82237 12.0252 1.77423C11.4846 1.72528 10.7888 1.7254 9.80157 1.7254H7.71466C6.75614 1.72559 5.92659 2.27697 5.52325 3.07892H4.07013C4.54215 1.51132 5.99314 0.368192 7.71466 0.367981H9.80157Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">复制</span></span><div class="ds-focus-ring"></div></button><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M15.3695 11.411L15.1234 12.8866C14.8869 14.3042 13.6603 15.3436 12.223 15.3436H3.7767C2.33954 15.3434 1.11276 14.3042 0.876312 12.8866L0.630219 11.411L2.05405 11.1747L2.29916 12.6493C2.41969 13.3713 3.04472 13.9001 3.7767 13.9003H12.223C12.9551 13.9002 13.58 13.3713 13.7005 12.6493L13.9456 11.1747L15.3695 11.411ZM8.72202 8.994C8.77714 8.93934 8.83789 8.88106 8.90268 8.81627L12.4828 5.23424L13.5042 6.25572L9.92221 9.8358C9.63947 10.1185 9.3876 10.3732 9.15854 10.5575C8.91889 10.7503 8.6395 10.9224 8.28647 10.9784C8.09708 11.0083 7.9036 11.0083 7.7142 10.9784C7.36103 10.9224 7.08087 10.7503 6.84116 10.5575C6.61212 10.3732 6.36019 10.1185 6.07748 9.8358L2.49643 6.25572L3.51694 5.23424L7.09702 8.81627C7.16216 8.88142 7.22327 8.94006 7.27866 8.99498V1.3065H8.72202V8.994Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">下载</span></span><div class="ds-focus-ring"></div></button></div></div></div></div></div><pre><span class="token keyword">class</span> <span class="token class-name">QwenTokenizer</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">:</span>
    <span class="token keyword">def</span> <span class="token function">__init__</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> token_path<span class="token punctuation">,</span> skip_special_tokens<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span><span class="token punctuation">:</span>
        <span class="token builtin">super</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span>__init__<span class="token punctuation">(</span><span class="token punctuation">)</span>
        <span class="token comment"># NOTE: non-chat model, all these special tokens keep randomly initialized.</span>
        special_tokens <span class="token operator">=</span> <span class="token punctuation">{</span>
            <span class="token string">'eos_token'</span><span class="token punctuation">:</span> <span class="token string">'&lt;|endoftext|&gt;'</span><span class="token punctuation">,</span>
            <span class="token string">'pad_token'</span><span class="token punctuation">:</span> <span class="token string">'&lt;|endoftext|&gt;'</span><span class="token punctuation">,</span>
            <span class="token string">'additional_special_tokens'</span><span class="token punctuation">:</span> <span class="token punctuation">[</span>
                <span class="token string">'&lt;|im_start|&gt;'</span><span class="token punctuation">,</span> <span class="token string">'&lt;|im_end|&gt;'</span><span class="token punctuation">,</span> <span class="token string">'&lt;|endofprompt|&gt;'</span><span class="token punctuation">,</span>
                <span class="token comment"># 原有语气词</span>
                <span class="token string">'[breath]'</span><span class="token punctuation">,</span> <span class="token string">'&lt;strong&gt;'</span><span class="token punctuation">,</span> <span class="token string">'&lt;/strong&gt;'</span><span class="token punctuation">,</span> <span class="token string">'[noise]'</span><span class="token punctuation">,</span>
                <span class="token string">'[laughter]'</span><span class="token punctuation">,</span> <span class="token string">'[cough]'</span><span class="token punctuation">,</span> <span class="token string">'[clucking]'</span><span class="token punctuation">,</span> <span class="token string">'[accent]'</span><span class="token punctuation">,</span>
                <span class="token string">'[quick_breath]'</span><span class="token punctuation">,</span>
                <span class="token string">"&lt;laughter&gt;"</span><span class="token punctuation">,</span> <span class="token string">"&lt;/laughter&gt;"</span><span class="token punctuation">,</span>
                <span class="token string">"[hissing]"</span><span class="token punctuation">,</span> <span class="token string">"[sigh]"</span><span class="token punctuation">,</span> <span class="token string">"[vocalized-noise]"</span><span class="token punctuation">,</span>
                <span class="token string">"[lipsmack]"</span><span class="token punctuation">,</span> <span class="token string">"[mn]"</span><span class="token punctuation">,</span>
                
                <span class="token comment"># NVSpeech 数据集新增语气词</span>
                <span class="token comment"># 呼吸相关</span>
                <span class="token string">"[breathing]"</span><span class="token punctuation">,</span>  <span class="token comment"># 呼吸声</span>
                
                <span class="token comment"># 笑声和咳嗽</span>
                <span class="token string">"[laughter]"</span><span class="token punctuation">,</span>    <span class="token comment"># 笑声（已存在，保留）</span>
                <span class="token string">"[cough]"</span><span class="token punctuation">,</span>      <span class="token comment"># 咳嗽（已存在，保留）</span>
                <span class="token string">"[sigh]"</span><span class="token punctuation">,</span>       <span class="token comment"># 叹气（已存在，保留）</span>
                
                <span class="token comment"># 确认和疑问语气</span>
                <span class="token string">"[confirmation-enn]"</span><span class="token punctuation">,</span>    <span class="token comment"># "嗯"确认语气</span>
                <span class="token string">"[question-enn]"</span><span class="token punctuation">,</span>        <span class="token comment"># "嗯"疑问语气</span>
                <span class="token string">"[question-ah]"</span><span class="token punctuation">,</span>        <span class="token comment"># "啊"疑问语气</span>
                <span class="token string">"[question-oh]"</span><span class="token punctuation">,</span>        <span class="token comment"># "哦"疑问语气</span>
                <span class="token string">"[question-ei]"</span><span class="token punctuation">,</span>        <span class="token comment"># "诶"疑问语气</span>
                <span class="token string">"[question-yi]"</span><span class="token punctuation">,</span>        <span class="token comment"># "咦"疑问语气</span>
                
                <span class="token comment"># 惊讶语气</span>
                <span class="token string">"[surprise-ah]"</span><span class="token punctuation">,</span>        <span class="token comment"># "啊"惊讶语气</span>
                <span class="token string">"[surprise-oh]"</span><span class="token punctuation">,</span>        <span class="token comment"># "哦"惊讶语气</span>
                <span class="token string">"[surprise-wa]"</span><span class="token punctuation">,</span>        <span class="token comment"># "哇"惊讶语气</span>
                <span class="token string">"[surprise-yo]"</span><span class="token punctuation">,</span>        <span class="token comment"># "哟"惊讶语气</span>
                
                <span class="token comment"># 不满和思考语气</span>
                <span class="token string">"[dissatisfaction-hnn]"</span><span class="token punctuation">,</span> <span class="token comment"># "哼"不满语气</span>
                <span class="token string">"[uhm]"</span><span class="token punctuation">,</span>                <span class="token comment"># "嗯"思考语气</span>
                
                <span class="token comment"># 其他声音</span>
                <span class="token string">"[shh]"</span><span class="token punctuation">,</span>                <span class="token comment"># "嘘"声</span>
                <span class="token string">"[crying]"</span>              <span class="token comment"># 哭泣声</span>
            <span class="token punctuation">]</span>
        <span class="token punctuation">}</span>
        self<span class="token punctuation">.</span>special_tokens <span class="token operator">=</span> special_tokens
        self<span class="token punctuation">.</span>tokenizer <span class="token operator">=</span> AutoTokenizer<span class="token punctuation">.</span>from_pretrained<span class="token punctuation">(</span>token_path<span class="token punctuation">)</span>
        self<span class="token punctuation">.</span>tokenizer<span class="token punctuation">.</span>add_special_tokens<span class="token punctuation">(</span>special_tokens<span class="token punctuation">)</span>
        self<span class="token punctuation">.</span>skip_special_tokens <span class="token operator">=</span> skip_special_tokens

    <span class="token keyword">def</span> <span class="token function">encode</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> text<span class="token punctuation">,</span> <span class="token operator">**</span>kwargs<span class="token punctuation">)</span><span class="token punctuation">:</span>
        tokens <span class="token operator">=</span> self<span class="token punctuation">.</span>tokenizer<span class="token punctuation">(</span><span class="token punctuation">[</span>text<span class="token punctuation">]</span><span class="token punctuation">,</span> return_tensors<span class="token operator">=</span><span class="token string">"pt"</span><span class="token punctuation">)</span>
        tokens <span class="token operator">=</span> tokens<span class="token punctuation">[</span><span class="token string">"input_ids"</span><span class="token punctuation">]</span><span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">.</span>cpu<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span>tolist<span class="token punctuation">(</span><span class="token punctuation">)</span>
        <span class="token keyword">return</span> tokens

    <span class="token keyword">def</span> <span class="token function">decode</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> tokens<span class="token punctuation">)</span><span class="token punctuation">:</span>
        tokens <span class="token operator">=</span> torch<span class="token punctuation">.</span>tensor<span class="token punctuation">(</span>tokens<span class="token punctuation">,</span> dtype<span class="token operator">=</span>torch<span class="token punctuation">.</span>int64<span class="token punctuation">)</span>
        text <span class="token operator">=</span> self<span class="token punctuation">.</span>tokenizer<span class="token punctuation">.</span>batch_decode<span class="token punctuation">(</span><span class="token punctuation">[</span>tokens<span class="token punctuation">]</span><span class="token punctuation">,</span> skip_special_tokens<span class="token operator">=</span>self<span class="token punctuation">.</span>skip_special_tokens<span class="token punctuation">)</span><span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span>
        <span class="token keyword">return</span> text


<span class="token decorator annotation punctuation">@lru_cache</span><span class="token punctuation">(</span>maxsize<span class="token operator">=</span><span class="token boolean">None</span><span class="token punctuation">)</span>
<span class="token keyword">def</span> <span class="token function">get_qwen_tokenizer</span><span class="token punctuation">(</span>
    token_path<span class="token punctuation">:</span> <span class="token builtin">str</span><span class="token punctuation">,</span>
    skip_special_tokens<span class="token punctuation">:</span> <span class="token builtin">bool</span>
<span class="token punctuation">)</span> <span class="token operator">-</span><span class="token operator">&gt;</span> QwenTokenizer<span class="token punctuation">:</span>
    <span class="token keyword">return</span> QwenTokenizer<span class="token punctuation">(</span>token_path<span class="token operator">=</span>token_path<span class="token punctuation">,</span> skip_special_tokens<span class="token operator">=</span>skip_special_tokens<span class="token punctuation">)</span></pre><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _33882ae"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _28d7e84"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg></div><p class="ds-markdown-paragraph"><span>主要修改：</span></p><ol start="1"><li><p class="ds-markdown-paragraph"><strong><span>将 </span>`[confirmation-en]`<span> 改为 </span>`[confirmation-enn]`</strong><span> - 表示确认语气的"嗯"</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>将 </span>`[question-en]`<span> 改为 </span>`[question-enn]`</strong><span> - 表示疑问语气的"嗯"</span></p></li></ol><p class="ds-markdown-paragraph"><span>这样修改后，所有的语气词标记都准确地反映了中文发音，避免了将"en"误解为英语的歧义。现在这些标记能够更好地处理中文语音数据中的各种语气和情感表达。</span></p>

