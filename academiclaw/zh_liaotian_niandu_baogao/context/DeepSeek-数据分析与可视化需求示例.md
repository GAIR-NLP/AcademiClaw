### 用户

每位同学需要提交至少 5 个基于真实场景的需求（Query）。这些需求应来自你日常工作、学习或生活中与大模型互动时遇到的实际问题。

⚠️ 重要提示：不能使用已有 benchmark 的数据！


---

✅ 提交要求

每个 Query 必须包含以下 4 个元素（缺少任何一个元素将不得分）：

1. Query（任务描述）
- 对任务进行详细、清晰的描述
- 说明任务的目标和预期输出
- 确保描述足够详细，使他人能够理解任务要求
  
2. Context（上下文文件）
- 提供完成任务所需的所有相关文件
- Context 必须包含解决 Query 的所有必要信息
- 文件格式可以是：代码文件、数据集、文档、网页链接等
  
Context 示例：
- 如果 Query 是"解决某个 GitHub Issue"，Context 应包括：
  - GitHub Issue 的链接
  - 相关的代码文件
- 如果 Query 是"修改前端网页"，Context 应包括：
  - 原始 HTML、CSS、JavaScript 文件
  - 相关的配置文件
    
3. 参考答案（Reference Answer）
- 提供任务的理想输出或正确答案
- 可以是：
  - 完整的代码实现
  - 详细的报告文档
  - 修改后的文件
  - 问题的解决方案
    
4. Rubric（评分标准）
- 提供明确的评判标准，用于判断答案的好坏
- 最佳形式：一个可执行的评分函数
  - 输入：待评估的答案
  - 输出：评分（score）
- 也可以是：
  - 详细的评分点列表（每个点包含具体要求和权重）
  - 可验证的检查项（例如：文件是否存在、代码是否能运行、loss 是否小于某个阈值）
给我十个这样的数据

---

### DeepSeek AI

<p>思考：</p><blockquote><p class="ds-markdown-paragraph"><span>哦，用户需要10个基于真实场景的Query示例，每个都要包含Query、Context、参考答案和Rubric四个要素。不能使用已有benchmark的数据，得全部原创。</span></p><p class="ds-markdown-paragraph"><span>让我想想怎么组织这些例子。可以覆盖不同的领域，比如代码、数据分析、学术写作、日常生活、技术问题解决等，这样能展示大模型的多方面能力。每个例子都要有真实感，确实像是日常会遇到的任务。</span></p><p class="ds-markdown-paragraph"><span>第一个例子可以用代码调试的场景，用户提供了出错的代码文件，需要模型修复bug。第二个可以用数据分析，给一个数据集让模型分析并可视化。第三个可以是学术相关的，比如整理文献笔记。第四个可以是生活助手类的，比如制定旅行计划。第五个可以是技术文档编写。第六个可以是数学问题求解。第七个可以是正则表达式生成。第八个可以是代码重构。第九个可以是API使用示例。第十个可以是文本处理任务。</span></p><p class="ds-markdown-paragraph"><span>每个例子的结构要完整：Query要详细描述任务，Context提供必要文件或数据，参考答案给出理想解决方案，Rubric要有可执行的评分标准。特别是Rubric部分，要尽量具体可衡量，比如代码是否能运行、输出是否符合格式要求等。</span></p><p class="ds-markdown-paragraph"><span>让我开始具体构思每个例子的内容，确保它们都是真实场景，并且互不重复。</span></p></blockquote><br/><p class="ds-markdown-paragraph"><span>以下是我为您准备的10个基于真实场景的Query示例，每个都包含完整的四个要素：</span></p><hr><h2><strong><span>示例 1：代码调试与优化</span></strong></h2><p class="ds-markdown-paragraph"><strong><span>Query（任务描述）</span></strong><span></span><br><span>我有一个Python脚本，原本用于处理CSV文件并生成统计报告。最近升级了pandas版本后，脚本出现了兼容性问题。请帮我：</span></p><ol start="1"><li><p class="ds-markdown-paragraph"><span>识别并修复所有因pandas版本升级导致的错误</span></p></li><li><p class="ds-markdown-paragraph"><span>优化代码性能，特别是大数据量处理部分</span></p></li><li><p class="ds-markdown-paragraph"><span>添加适当的错误处理和日志记录</span></p></li><li><p class="ds-markdown-paragraph"><span>确保代码符合PEP 8规范</span></p></li></ol><p class="ds-markdown-paragraph"><strong><span>Context（上下文文件）</span></strong></p><div class="md-code-block md-code-block-light"><div class="md-code-block-banner-wrap"><div class="md-code-block-banner md-code-block-banner-lite"><div class="_121d384"><div class="d2a24f03"><span class="d813de27">python</span></div><div class="d2a24f03 _246a029"><div class="efa13877"><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon" style="margin-right: 4px;"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.14923 4.02032C7.11191 4.02032 7.87977 4.02017 8.49591 4.07599C9.12122 4.1327 9.65786 4.25188 10.1414 4.53107C10.7201 4.8653 11.2008 5.34591 11.535 5.92462C11.8142 6.40818 11.9333 6.94482 11.9901 7.57013C12.0459 8.18625 12.0457 8.9542 12.0457 9.91681C12.0457 10.8795 12.0459 11.6474 11.9901 12.2635C11.9333 12.8888 11.8142 13.4254 11.535 13.909C11.2008 14.4877 10.7201 14.9683 10.1414 15.3026C9.65786 15.5817 9.12122 15.7009 8.49591 15.7576C7.87977 15.8134 7.1119 15.8133 6.14923 15.8133C5.18661 15.8133 4.41868 15.8134 3.80255 15.7576C3.17724 15.7009 2.6406 15.5817 2.15704 15.3026C1.57834 14.9684 1.09772 14.4877 0.763489 13.909C0.484305 13.4254 0.365123 12.8888 0.308411 12.2635C0.252587 11.6474 0.252747 10.8795 0.252747 9.91681C0.252747 8.95419 0.252603 8.18625 0.308411 7.57013C0.365123 6.94482 0.484305 6.40818 0.763489 5.92462C1.09771 5.3459 1.57833 4.86529 2.15704 4.53107C2.6406 4.25188 3.17724 4.1327 3.80255 4.07599C4.41868 4.02018 5.1866 4.02032 6.14923 4.02032ZM6.14923 5.37775C5.16175 5.37775 4.46628 5.37761 3.9256 5.42657C3.39428 5.47473 3.07853 5.56574 2.83575 5.70587C2.46313 5.92106 2.15348 6.23071 1.93829 6.60333C1.79817 6.84611 1.70715 7.16185 1.659 7.69318C1.61004 8.23385 1.61017 8.92934 1.61017 9.91681C1.61017 10.9043 1.61002 11.5998 1.659 12.1404C1.70715 12.6717 1.79817 12.9875 1.93829 13.2303C2.15349 13.6029 2.46315 13.9126 2.83575 14.1277C3.07853 14.2679 3.39428 14.3589 3.9256 14.407C4.46628 14.456 5.16176 14.4559 6.14923 14.4559C7.13675 14.4559 7.83218 14.456 8.37286 14.407C8.90419 14.3589 9.21993 14.2679 9.46271 14.1277C9.83529 13.9126 10.145 13.6029 10.3602 13.2303C10.5003 12.9875 10.5913 12.6718 10.6395 12.1404C10.6884 11.5998 10.6883 10.9043 10.6883 9.91681C10.6883 8.92935 10.6884 8.23385 10.6395 7.69318C10.5913 7.16185 10.5003 6.84611 10.3602 6.60333C10.145 6.23072 9.8353 5.92107 9.46271 5.70587C9.21993 5.56574 8.90418 5.47473 8.37286 5.42657C7.83218 5.3776 7.13676 5.37775 6.14923 5.37775ZM9.80157 0.367981C10.7637 0.367981 11.5313 0.367886 12.1473 0.423645C12.7725 0.480313 13.3093 0.598765 13.7928 0.877747C14.3716 1.21192 14.852 1.69355 15.1863 2.27228C15.4655 2.75575 15.5857 3.29165 15.6424 3.91681C15.6982 4.53301 15.6971 5.30161 15.6971 6.26447V7.8299C15.6971 8.29265 15.6989 8.58994 15.6649 8.84845C15.4667 10.3525 14.4009 11.5738 12.9832 11.9988V10.5467C13.6973 10.1903 14.2104 9.49662 14.3192 8.67169C14.3387 8.52348 14.3406 8.3358 14.3406 7.8299V6.26447C14.3406 5.27707 14.3398 4.58149 14.2908 4.04083C14.2427 3.50969 14.1526 3.19373 14.0125 2.95099C13.7974 2.5785 13.4875 2.2687 13.1151 2.05353C12.8723 1.91347 12.5563 1.82237 12.0252 1.77423C11.4846 1.72528 10.7888 1.7254 9.80157 1.7254H7.71466C6.75614 1.72559 5.92659 2.27697 5.52325 3.07892H4.07013C4.54215 1.51132 5.99314 0.368192 7.71466 0.367981H9.80157Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">复制</span></span><div class="ds-focus-ring"></div></button><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M15.3695 11.411L15.1234 12.8866C14.8869 14.3042 13.6603 15.3436 12.223 15.3436H3.7767C2.33954 15.3434 1.11276 14.3042 0.876312 12.8866L0.630219 11.411L2.05405 11.1747L2.29916 12.6493C2.41969 13.3713 3.04472 13.9001 3.7767 13.9003H12.223C12.9551 13.9002 13.58 13.3713 13.7005 12.6493L13.9456 11.1747L15.3695 11.411ZM8.72202 8.994C8.77714 8.93934 8.83789 8.88106 8.90268 8.81627L12.4828 5.23424L13.5042 6.25572L9.92221 9.8358C9.63947 10.1185 9.3876 10.3732 9.15854 10.5575C8.91889 10.7503 8.6395 10.9224 8.28647 10.9784C8.09708 11.0083 7.9036 11.0083 7.7142 10.9784C7.36103 10.9224 7.08087 10.7503 6.84116 10.5575C6.61212 10.3732 6.36019 10.1185 6.07748 9.8358L2.49643 6.25572L3.51694 5.23424L7.09702 8.81627C7.16216 8.88142 7.22327 8.94006 7.27866 8.99498V1.3065H8.72202V8.994Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">下载</span></span><div class="ds-focus-ring"></div></button></div></div></div></div></div><pre><span class="token comment"># data_processor.py</span>
<span class="token keyword">import</span> pandas <span class="token keyword">as</span> pd
<span class="token keyword">import</span> numpy <span class="token keyword">as</span> np

<span class="token keyword">def</span> <span class="token function">process_data</span><span class="token punctuation">(</span>input_file<span class="token punctuation">)</span><span class="token punctuation">:</span>
    df <span class="token operator">=</span> pd<span class="token punctuation">.</span>read_csv<span class="token punctuation">(</span>input_file<span class="token punctuation">)</span>
    
    <span class="token comment"># 旧版本pandas的写法</span>
    df<span class="token punctuation">[</span><span class="token string">'category'</span><span class="token punctuation">]</span> <span class="token operator">=</span> df<span class="token punctuation">[</span><span class="token string">'type'</span><span class="token punctuation">]</span><span class="token punctuation">.</span>applymap<span class="token punctuation">(</span><span class="token builtin">str</span><span class="token punctuation">.</span>upper<span class="token punctuation">)</span>
    
    <span class="token comment"># 分组统计</span>
    stats <span class="token operator">=</span> df<span class="token punctuation">.</span>groupby<span class="token punctuation">(</span><span class="token string">'category'</span><span class="token punctuation">)</span><span class="token punctuation">.</span>agg<span class="token punctuation">(</span><span class="token punctuation">{</span>
        <span class="token string">'value'</span><span class="token punctuation">:</span> <span class="token punctuation">[</span><span class="token string">'mean'</span><span class="token punctuation">,</span> <span class="token string">'std'</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
        <span class="token string">'count'</span><span class="token punctuation">:</span> <span class="token string">'sum'</span>
    <span class="token punctuation">}</span><span class="token punctuation">)</span>
    
    <span class="token comment"># 处理缺失值</span>
    df<span class="token punctuation">.</span>fillna<span class="token punctuation">(</span>method<span class="token operator">=</span><span class="token string">'ffill'</span><span class="token punctuation">,</span> inplace<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span>
    
    <span class="token comment"># 保存结果</span>
    stats<span class="token punctuation">.</span>to_excel<span class="token punctuation">(</span><span class="token string">'output.xlsx'</span><span class="token punctuation">)</span>
    
    <span class="token keyword">return</span> df<span class="token punctuation">,</span> stats

<span class="token comment"># 测试数据：test_data.csv（部分内容）</span>
<span class="token comment"># id,name,type,value,count</span>
<span class="token comment"># 1,Item1,A,10.5,100</span>
<span class="token comment"># 2,Item2,B,20.3,150</span>
<span class="token comment"># 3,Item3,A,15.2,80</span>
<span class="token comment"># 4,Item4,C,,200</span></pre><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _33882ae"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _28d7e84"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg></div><p class="ds-markdown-paragraph"><strong><span>参考答案（Reference Answer）</span></strong></p><div class="md-code-block md-code-block-light"><div class="md-code-block-banner-wrap"><div class="md-code-block-banner md-code-block-banner-lite"><div class="_121d384"><div class="d2a24f03"><span class="d813de27">python</span></div><div class="d2a24f03 _246a029"><div class="efa13877"><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon" style="margin-right: 4px;"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.14923 4.02032C7.11191 4.02032 7.87977 4.02017 8.49591 4.07599C9.12122 4.1327 9.65786 4.25188 10.1414 4.53107C10.7201 4.8653 11.2008 5.34591 11.535 5.92462C11.8142 6.40818 11.9333 6.94482 11.9901 7.57013C12.0459 8.18625 12.0457 8.9542 12.0457 9.91681C12.0457 10.8795 12.0459 11.6474 11.9901 12.2635C11.9333 12.8888 11.8142 13.4254 11.535 13.909C11.2008 14.4877 10.7201 14.9683 10.1414 15.3026C9.65786 15.5817 9.12122 15.7009 8.49591 15.7576C7.87977 15.8134 7.1119 15.8133 6.14923 15.8133C5.18661 15.8133 4.41868 15.8134 3.80255 15.7576C3.17724 15.7009 2.6406 15.5817 2.15704 15.3026C1.57834 14.9684 1.09772 14.4877 0.763489 13.909C0.484305 13.4254 0.365123 12.8888 0.308411 12.2635C0.252587 11.6474 0.252747 10.8795 0.252747 9.91681C0.252747 8.95419 0.252603 8.18625 0.308411 7.57013C0.365123 6.94482 0.484305 6.40818 0.763489 5.92462C1.09771 5.3459 1.57833 4.86529 2.15704 4.53107C2.6406 4.25188 3.17724 4.1327 3.80255 4.07599C4.41868 4.02018 5.1866 4.02032 6.14923 4.02032ZM6.14923 5.37775C5.16175 5.37775 4.46628 5.37761 3.9256 5.42657C3.39428 5.47473 3.07853 5.56574 2.83575 5.70587C2.46313 5.92106 2.15348 6.23071 1.93829 6.60333C1.79817 6.84611 1.70715 7.16185 1.659 7.69318C1.61004 8.23385 1.61017 8.92934 1.61017 9.91681C1.61017 10.9043 1.61002 11.5998 1.659 12.1404C1.70715 12.6717 1.79817 12.9875 1.93829 13.2303C2.15349 13.6029 2.46315 13.9126 2.83575 14.1277C3.07853 14.2679 3.39428 14.3589 3.9256 14.407C4.46628 14.456 5.16176 14.4559 6.14923 14.4559C7.13675 14.4559 7.83218 14.456 8.37286 14.407C8.90419 14.3589 9.21993 14.2679 9.46271 14.1277C9.83529 13.9126 10.145 13.6029 10.3602 13.2303C10.5003 12.9875 10.5913 12.6718 10.6395 12.1404C10.6884 11.5998 10.6883 10.9043 10.6883 9.91681C10.6883 8.92935 10.6884 8.23385 10.6395 7.69318C10.5913 7.16185 10.5003 6.84611 10.3602 6.60333C10.145 6.23072 9.8353 5.92107 9.46271 5.70587C9.21993 5.56574 8.90418 5.47473 8.37286 5.42657C7.83218 5.3776 7.13676 5.37775 6.14923 5.37775ZM9.80157 0.367981C10.7637 0.367981 11.5313 0.367886 12.1473 0.423645C12.7725 0.480313 13.3093 0.598765 13.7928 0.877747C14.3716 1.21192 14.852 1.69355 15.1863 2.27228C15.4655 2.75575 15.5857 3.29165 15.6424 3.91681C15.6982 4.53301 15.6971 5.30161 15.6971 6.26447V7.8299C15.6971 8.29265 15.6989 8.58994 15.6649 8.84845C15.4667 10.3525 14.4009 11.5738 12.9832 11.9988V10.5467C13.6973 10.1903 14.2104 9.49662 14.3192 8.67169C14.3387 8.52348 14.3406 8.3358 14.3406 7.8299V6.26447C14.3406 5.27707 14.3398 4.58149 14.2908 4.04083C14.2427 3.50969 14.1526 3.19373 14.0125 2.95099C13.7974 2.5785 13.4875 2.2687 13.1151 2.05353C12.8723 1.91347 12.5563 1.82237 12.0252 1.77423C11.4846 1.72528 10.7888 1.7254 9.80157 1.7254H7.71466C6.75614 1.72559 5.92659 2.27697 5.52325 3.07892H4.07013C4.54215 1.51132 5.99314 0.368192 7.71466 0.367981H9.80157Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">复制</span></span><div class="ds-focus-ring"></div></button><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M15.3695 11.411L15.1234 12.8866C14.8869 14.3042 13.6603 15.3436 12.223 15.3436H3.7767C2.33954 15.3434 1.11276 14.3042 0.876312 12.8866L0.630219 11.411L2.05405 11.1747L2.29916 12.6493C2.41969 13.3713 3.04472 13.9001 3.7767 13.9003H12.223C12.9551 13.9002 13.58 13.3713 13.7005 12.6493L13.9456 11.1747L15.3695 11.411ZM8.72202 8.994C8.77714 8.93934 8.83789 8.88106 8.90268 8.81627L12.4828 5.23424L13.5042 6.25572L9.92221 9.8358C9.63947 10.1185 9.3876 10.3732 9.15854 10.5575C8.91889 10.7503 8.6395 10.9224 8.28647 10.9784C8.09708 11.0083 7.9036 11.0083 7.7142 10.9784C7.36103 10.9224 7.08087 10.7503 6.84116 10.5575C6.61212 10.3732 6.36019 10.1185 6.07748 9.8358L2.49643 6.25572L3.51694 5.23424L7.09702 8.81627C7.16216 8.88142 7.22327 8.94006 7.27866 8.99498V1.3065H8.72202V8.994Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">下载</span></span><div class="ds-focus-ring"></div></button></div></div></div></div></div><pre><span class="token comment"># data_processor_optimized.py</span>
<span class="token keyword">import</span> pandas <span class="token keyword">as</span> pd
<span class="token keyword">import</span> numpy <span class="token keyword">as</span> np
<span class="token keyword">import</span> logging
<span class="token keyword">from</span> typing <span class="token keyword">import</span> Tuple<span class="token punctuation">,</span> Optional
<span class="token keyword">import</span> warnings

<span class="token comment"># 配置日志</span>
logging<span class="token punctuation">.</span>basicConfig<span class="token punctuation">(</span>
    level<span class="token operator">=</span>logging<span class="token punctuation">.</span>INFO<span class="token punctuation">,</span>
    <span class="token builtin">format</span><span class="token operator">=</span><span class="token string">'%(asctime)s - %(levelname)s - %(message)s'</span>
<span class="token punctuation">)</span>
logger <span class="token operator">=</span> logging<span class="token punctuation">.</span>getLogger<span class="token punctuation">(</span>__name__<span class="token punctuation">)</span>

<span class="token keyword">def</span> <span class="token function">process_data</span><span class="token punctuation">(</span>input_file<span class="token punctuation">:</span> <span class="token builtin">str</span><span class="token punctuation">)</span> <span class="token operator">-</span><span class="token operator">&gt;</span> Tuple<span class="token punctuation">[</span>pd<span class="token punctuation">.</span>DataFrame<span class="token punctuation">,</span> pd<span class="token punctuation">.</span>DataFrame<span class="token punctuation">]</span><span class="token punctuation">:</span>
    <span class="token triple-quoted-string string">"""
    处理CSV文件并生成统计报告
    
    Args:
        input_file: 输入CSV文件路径
        
    Returns:
        Tuple[清洗后的DataFrame, 统计DataFrame]
    """</span>
    <span class="token keyword">try</span><span class="token punctuation">:</span>
        <span class="token comment"># 1. 读取数据（使用chunking处理大文件）</span>
        logger<span class="token punctuation">.</span>info<span class="token punctuation">(</span><span class="token string-interpolation"><span class="token string">f"开始处理文件: </span><span class="token interpolation"><span class="token punctuation">{</span>input_file<span class="token punctuation">}</span></span><span class="token string">"</span></span><span class="token punctuation">)</span>
        
        <span class="token comment"># 对于大文件，可以使用chunksize</span>
        df <span class="token operator">=</span> pd<span class="token punctuation">.</span>read_csv<span class="token punctuation">(</span>input_file<span class="token punctuation">,</span> dtype<span class="token operator">=</span><span class="token punctuation">{</span><span class="token string">'id'</span><span class="token punctuation">:</span> <span class="token string">'int32'</span><span class="token punctuation">}</span><span class="token punctuation">)</span>
        logger<span class="token punctuation">.</span>info<span class="token punctuation">(</span><span class="token string-interpolation"><span class="token string">f"成功读取数据，行数: </span><span class="token interpolation"><span class="token punctuation">{</span><span class="token builtin">len</span><span class="token punctuation">(</span>df<span class="token punctuation">)</span><span class="token punctuation">}</span></span><span class="token string">"</span></span><span class="token punctuation">)</span>
        
        <span class="token comment"># 2. 修复版本兼容性问题</span>
        <span class="token comment"># applymap -&gt; map（对于Series）或apply（对于DataFrame）</span>
        <span class="token keyword">if</span> <span class="token string">'type'</span> <span class="token keyword">in</span> df<span class="token punctuation">.</span>columns<span class="token punctuation">:</span>
            <span class="token comment"># 使用更高效的方法</span>
            df<span class="token punctuation">[</span><span class="token string">'category'</span><span class="token punctuation">]</span> <span class="token operator">=</span> df<span class="token punctuation">[</span><span class="token string">'type'</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token builtin">str</span><span class="token punctuation">.</span>upper<span class="token punctuation">(</span><span class="token punctuation">)</span>
        <span class="token keyword">else</span><span class="token punctuation">:</span>
            logger<span class="token punctuation">.</span>warning<span class="token punctuation">(</span><span class="token string">"未找到'type'列"</span><span class="token punctuation">)</span>
            df<span class="token punctuation">[</span><span class="token string">'category'</span><span class="token punctuation">]</span> <span class="token operator">=</span> <span class="token string">''</span>
        
        <span class="token comment"># 3. 处理缺失值（使用copy避免SettingWithCopyWarning）</span>
        df <span class="token operator">=</span> df<span class="token punctuation">.</span>copy<span class="token punctuation">(</span><span class="token punctuation">)</span>
        numeric_cols <span class="token operator">=</span> df<span class="token punctuation">.</span>select_dtypes<span class="token punctuation">(</span>include<span class="token operator">=</span><span class="token punctuation">[</span>np<span class="token punctuation">.</span>number<span class="token punctuation">]</span><span class="token punctuation">)</span><span class="token punctuation">.</span>columns
        
        <span class="token keyword">for</span> col <span class="token keyword">in</span> numeric_cols<span class="token punctuation">:</span>
            <span class="token keyword">if</span> df<span class="token punctuation">[</span>col<span class="token punctuation">]</span><span class="token punctuation">.</span>isna<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token builtin">any</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">:</span>
                <span class="token comment"># 使用前向填充，但仅对数值列</span>
                df<span class="token punctuation">[</span>col<span class="token punctuation">]</span> <span class="token operator">=</span> df<span class="token punctuation">[</span>col<span class="token punctuation">]</span><span class="token punctuation">.</span>ffill<span class="token punctuation">(</span><span class="token punctuation">)</span>
                logger<span class="token punctuation">.</span>info<span class="token punctuation">(</span><span class="token string-interpolation"><span class="token string">f"列'</span><span class="token interpolation"><span class="token punctuation">{</span>col<span class="token punctuation">}</span></span><span class="token string">'的缺失值已填充"</span></span><span class="token punctuation">)</span>
        
        <span class="token comment"># 4. 优化分组统计</span>
        <span class="token comment"># 检查必要的列是否存在</span>
        required_cols <span class="token operator">=</span> <span class="token punctuation">[</span><span class="token string">'category'</span><span class="token punctuation">,</span> <span class="token string">'value'</span><span class="token punctuation">,</span> <span class="token string">'count'</span><span class="token punctuation">]</span>
        missing_cols <span class="token operator">=</span> <span class="token punctuation">[</span>col <span class="token keyword">for</span> col <span class="token keyword">in</span> required_cols <span class="token keyword">if</span> col <span class="token keyword">not</span> <span class="token keyword">in</span> df<span class="token punctuation">.</span>columns<span class="token punctuation">]</span>
        
        <span class="token keyword">if</span> missing_cols<span class="token punctuation">:</span>
            error_msg <span class="token operator">=</span> <span class="token string-interpolation"><span class="token string">f"缺少必要列: </span><span class="token interpolation"><span class="token punctuation">{</span>missing_cols<span class="token punctuation">}</span></span><span class="token string">"</span></span>
            logger<span class="token punctuation">.</span>error<span class="token punctuation">(</span>error_msg<span class="token punctuation">)</span>
            <span class="token keyword">raise</span> ValueError<span class="token punctuation">(</span>error_msg<span class="token punctuation">)</span>
        
        <span class="token comment"># 使用命名聚合（pandas 0.25+）</span>
        stats <span class="token operator">=</span> df<span class="token punctuation">.</span>groupby<span class="token punctuation">(</span><span class="token string">'category'</span><span class="token punctuation">,</span> observed<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span><span class="token punctuation">.</span>agg<span class="token punctuation">(</span>
            mean_value<span class="token operator">=</span><span class="token punctuation">(</span><span class="token string">'value'</span><span class="token punctuation">,</span> <span class="token string">'mean'</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
            std_value<span class="token operator">=</span><span class="token punctuation">(</span><span class="token string">'value'</span><span class="token punctuation">,</span> <span class="token string">'std'</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
            total_count<span class="token operator">=</span><span class="token punctuation">(</span><span class="token string">'count'</span><span class="token punctuation">,</span> <span class="token string">'sum'</span><span class="token punctuation">)</span>
        <span class="token punctuation">)</span><span class="token punctuation">.</span>reset_index<span class="token punctuation">(</span><span class="token punctuation">)</span>
        
        <span class="token comment"># 5. 保存结果（使用openpyxl引擎）</span>
        <span class="token keyword">try</span><span class="token punctuation">:</span>
            stats<span class="token punctuation">.</span>to_excel<span class="token punctuation">(</span><span class="token string">'output.xlsx'</span><span class="token punctuation">,</span> index<span class="token operator">=</span><span class="token boolean">False</span><span class="token punctuation">,</span> engine<span class="token operator">=</span><span class="token string">'openpyxl'</span><span class="token punctuation">)</span>
            logger<span class="token punctuation">.</span>info<span class="token punctuation">(</span><span class="token string">"统计结果已保存到output.xlsx"</span><span class="token punctuation">)</span>
        <span class="token keyword">except</span> Exception <span class="token keyword">as</span> e<span class="token punctuation">:</span>
            logger<span class="token punctuation">.</span>error<span class="token punctuation">(</span><span class="token string-interpolation"><span class="token string">f"保存Excel文件失败: </span><span class="token interpolation"><span class="token punctuation">{</span><span class="token builtin">str</span><span class="token punctuation">(</span>e<span class="token punctuation">)</span><span class="token punctuation">}</span></span><span class="token string">"</span></span><span class="token punctuation">)</span>
            <span class="token comment"># 降级保存为CSV</span>
            stats<span class="token punctuation">.</span>to_csv<span class="token punctuation">(</span><span class="token string">'output.csv'</span><span class="token punctuation">,</span> index<span class="token operator">=</span><span class="token boolean">False</span><span class="token punctuation">)</span>
            logger<span class="token punctuation">.</span>info<span class="token punctuation">(</span><span class="token string">"结果已保存到output.csv"</span><span class="token punctuation">)</span>
        
        <span class="token keyword">return</span> df<span class="token punctuation">,</span> stats
        
    <span class="token keyword">except</span> FileNotFoundError<span class="token punctuation">:</span>
        logger<span class="token punctuation">.</span>error<span class="token punctuation">(</span><span class="token string-interpolation"><span class="token string">f"文件未找到: </span><span class="token interpolation"><span class="token punctuation">{</span>input_file<span class="token punctuation">}</span></span><span class="token string">"</span></span><span class="token punctuation">)</span>
        <span class="token keyword">raise</span>
    <span class="token keyword">except</span> pd<span class="token punctuation">.</span>errors<span class="token punctuation">.</span>EmptyDataError<span class="token punctuation">:</span>
        logger<span class="token punctuation">.</span>error<span class="token punctuation">(</span><span class="token string">"文件为空"</span><span class="token punctuation">)</span>
        <span class="token keyword">raise</span>
    <span class="token keyword">except</span> Exception <span class="token keyword">as</span> e<span class="token punctuation">:</span>
        logger<span class="token punctuation">.</span>error<span class="token punctuation">(</span><span class="token string-interpolation"><span class="token string">f"处理数据时发生错误: </span><span class="token interpolation"><span class="token punctuation">{</span><span class="token builtin">str</span><span class="token punctuation">(</span>e<span class="token punctuation">)</span><span class="token punctuation">}</span></span><span class="token string">"</span></span><span class="token punctuation">)</span>
        <span class="token keyword">raise</span>

<span class="token keyword">if</span> __name__ <span class="token operator">==</span> <span class="token string">"__main__"</span><span class="token punctuation">:</span>
    <span class="token comment"># 测试代码</span>
    <span class="token keyword">try</span><span class="token punctuation">:</span>
        result_df<span class="token punctuation">,</span> result_stats <span class="token operator">=</span> process_data<span class="token punctuation">(</span><span class="token string">"test_data.csv"</span><span class="token punctuation">)</span>
        <span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string">"数据处理完成！"</span><span class="token punctuation">)</span>
        <span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string">"\n统计结果:"</span><span class="token punctuation">)</span>
        <span class="token keyword">print</span><span class="token punctuation">(</span>result_stats<span class="token punctuation">)</span>
    <span class="token keyword">except</span> Exception <span class="token keyword">as</span> e<span class="token punctuation">:</span>
        <span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string-interpolation"><span class="token string">f"处理失败: </span><span class="token interpolation"><span class="token punctuation">{</span>e<span class="token punctuation">}</span></span><span class="token string">"</span></span><span class="token punctuation">)</span></pre><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _33882ae"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _28d7e84"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg></div><p class="ds-markdown-paragraph"><strong><span>Rubric（评分标准）</span></strong></p><div class="md-code-block md-code-block-light"><div class="md-code-block-banner-wrap"><div class="md-code-block-banner md-code-block-banner-lite"><div class="_121d384"><div class="d2a24f03"><span class="d813de27">python</span></div><div class="d2a24f03 _246a029"><div class="efa13877"><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon" style="margin-right: 4px;"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.14923 4.02032C7.11191 4.02032 7.87977 4.02017 8.49591 4.07599C9.12122 4.1327 9.65786 4.25188 10.1414 4.53107C10.7201 4.8653 11.2008 5.34591 11.535 5.92462C11.8142 6.40818 11.9333 6.94482 11.9901 7.57013C12.0459 8.18625 12.0457 8.9542 12.0457 9.91681C12.0457 10.8795 12.0459 11.6474 11.9901 12.2635C11.9333 12.8888 11.8142 13.4254 11.535 13.909C11.2008 14.4877 10.7201 14.9683 10.1414 15.3026C9.65786 15.5817 9.12122 15.7009 8.49591 15.7576C7.87977 15.8134 7.1119 15.8133 6.14923 15.8133C5.18661 15.8133 4.41868 15.8134 3.80255 15.7576C3.17724 15.7009 2.6406 15.5817 2.15704 15.3026C1.57834 14.9684 1.09772 14.4877 0.763489 13.909C0.484305 13.4254 0.365123 12.8888 0.308411 12.2635C0.252587 11.6474 0.252747 10.8795 0.252747 9.91681C0.252747 8.95419 0.252603 8.18625 0.308411 7.57013C0.365123 6.94482 0.484305 6.40818 0.763489 5.92462C1.09771 5.3459 1.57833 4.86529 2.15704 4.53107C2.6406 4.25188 3.17724 4.1327 3.80255 4.07599C4.41868 4.02018 5.1866 4.02032 6.14923 4.02032ZM6.14923 5.37775C5.16175 5.37775 4.46628 5.37761 3.9256 5.42657C3.39428 5.47473 3.07853 5.56574 2.83575 5.70587C2.46313 5.92106 2.15348 6.23071 1.93829 6.60333C1.79817 6.84611 1.70715 7.16185 1.659 7.69318C1.61004 8.23385 1.61017 8.92934 1.61017 9.91681C1.61017 10.9043 1.61002 11.5998 1.659 12.1404C1.70715 12.6717 1.79817 12.9875 1.93829 13.2303C2.15349 13.6029 2.46315 13.9126 2.83575 14.1277C3.07853 14.2679 3.39428 14.3589 3.9256 14.407C4.46628 14.456 5.16176 14.4559 6.14923 14.4559C7.13675 14.4559 7.83218 14.456 8.37286 14.407C8.90419 14.3589 9.21993 14.2679 9.46271 14.1277C9.83529 13.9126 10.145 13.6029 10.3602 13.2303C10.5003 12.9875 10.5913 12.6718 10.6395 12.1404C10.6884 11.5998 10.6883 10.9043 10.6883 9.91681C10.6883 8.92935 10.6884 8.23385 10.6395 7.69318C10.5913 7.16185 10.5003 6.84611 10.3602 6.60333C10.145 6.23072 9.8353 5.92107 9.46271 5.70587C9.21993 5.56574 8.90418 5.47473 8.37286 5.42657C7.83218 5.3776 7.13676 5.37775 6.14923 5.37775ZM9.80157 0.367981C10.7637 0.367981 11.5313 0.367886 12.1473 0.423645C12.7725 0.480313 13.3093 0.598765 13.7928 0.877747C14.3716 1.21192 14.852 1.69355 15.1863 2.27228C15.4655 2.75575 15.5857 3.29165 15.6424 3.91681C15.6982 4.53301 15.6971 5.30161 15.6971 6.26447V7.8299C15.6971 8.29265 15.6989 8.58994 15.6649 8.84845C15.4667 10.3525 14.4009 11.5738 12.9832 11.9988V10.5467C13.6973 10.1903 14.2104 9.49662 14.3192 8.67169C14.3387 8.52348 14.3406 8.3358 14.3406 7.8299V6.26447C14.3406 5.27707 14.3398 4.58149 14.2908 4.04083C14.2427 3.50969 14.1526 3.19373 14.0125 2.95099C13.7974 2.5785 13.4875 2.2687 13.1151 2.05353C12.8723 1.91347 12.5563 1.82237 12.0252 1.77423C11.4846 1.72528 10.7888 1.7254 9.80157 1.7254H7.71466C6.75614 1.72559 5.92659 2.27697 5.52325 3.07892H4.07013C4.54215 1.51132 5.99314 0.368192 7.71466 0.367981H9.80157Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">复制</span></span><div class="ds-focus-ring"></div></button><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M15.3695 11.411L15.1234 12.8866C14.8869 14.3042 13.6603 15.3436 12.223 15.3436H3.7767C2.33954 15.3434 1.11276 14.3042 0.876312 12.8866L0.630219 11.411L2.05405 11.1747L2.29916 12.6493C2.41969 13.3713 3.04472 13.9001 3.7767 13.9003H12.223C12.9551 13.9002 13.58 13.3713 13.7005 12.6493L13.9456 11.1747L15.3695 11.411ZM8.72202 8.994C8.77714 8.93934 8.83789 8.88106 8.90268 8.81627L12.4828 5.23424L13.5042 6.25572L9.92221 9.8358C9.63947 10.1185 9.3876 10.3732 9.15854 10.5575C8.91889 10.7503 8.6395 10.9224 8.28647 10.9784C8.09708 11.0083 7.9036 11.0083 7.7142 10.9784C7.36103 10.9224 7.08087 10.7503 6.84116 10.5575C6.61212 10.3732 6.36019 10.1185 6.07748 9.8358L2.49643 6.25572L3.51694 5.23424L7.09702 8.81627C7.16216 8.88142 7.22327 8.94006 7.27866 8.99498V1.3065H8.72202V8.994Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">下载</span></span><div class="ds-focus-ring"></div></button></div></div></div></div></div><pre><span class="token keyword">def</span> <span class="token function">evaluate_solution</span><span class="token punctuation">(</span>answer_code<span class="token punctuation">:</span> <span class="token builtin">str</span><span class="token punctuation">)</span> <span class="token operator">-</span><span class="token operator">&gt;</span> <span class="token builtin">int</span><span class="token punctuation">:</span>
    <span class="token triple-quoted-string string">"""
    评分函数（满分100）
    """</span>
    score <span class="token operator">=</span> <span class="token number">0</span>
    
    <span class="token comment"># 1. 代码是否能正常运行（30分）</span>
    <span class="token keyword">try</span><span class="token punctuation">:</span>
        <span class="token keyword">exec</span><span class="token punctuation">(</span><span class="token builtin">open</span><span class="token punctuation">(</span><span class="token string">'test_data.py'</span><span class="token punctuation">)</span><span class="token punctuation">.</span>read<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span> <span class="token builtin">globals</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
        <span class="token comment"># 创建测试文件</span>
        test_csv <span class="token operator">=</span> <span class="token string">"id,name,type,value,count\n1,Item1,A,10.5,100\n2,Item2,B,20.3,150"</span>
        <span class="token keyword">with</span> <span class="token builtin">open</span><span class="token punctuation">(</span><span class="token string">'test_temp.csv'</span><span class="token punctuation">,</span> <span class="token string">'w'</span><span class="token punctuation">)</span> <span class="token keyword">as</span> f<span class="token punctuation">:</span>
            f<span class="token punctuation">.</span>write<span class="token punctuation">(</span>test_csv<span class="token punctuation">)</span>
        
        <span class="token comment"># 导入并测试</span>
        <span class="token keyword">import</span> data_processor_optimized <span class="token keyword">as</span> dpo
        df<span class="token punctuation">,</span> stats <span class="token operator">=</span> dpo<span class="token punctuation">.</span>process_data<span class="token punctuation">(</span><span class="token string">'test_temp.csv'</span><span class="token punctuation">)</span>
        score <span class="token operator">+=</span> <span class="token number">30</span>
    <span class="token keyword">except</span> Exception <span class="token keyword">as</span> e<span class="token punctuation">:</span>
        <span class="token keyword">return</span> score
    
    <span class="token comment"># 2. 修复了版本兼容性问题（20分）</span>
    <span class="token keyword">if</span> <span class="token string">'applymap'</span> <span class="token keyword">not</span> <span class="token keyword">in</span> answer_code <span class="token keyword">and</span> <span class="token string">'.str.'</span> <span class="token keyword">in</span> answer_code<span class="token punctuation">:</span>
        score <span class="token operator">+=</span> <span class="token number">20</span>
    
    <span class="token comment"># 3. 包含错误处理（15分）</span>
    required_handling <span class="token operator">=</span> <span class="token punctuation">[</span><span class="token string">'try:'</span><span class="token punctuation">,</span> <span class="token string">'except:'</span><span class="token punctuation">,</span> <span class="token string">'logging'</span><span class="token punctuation">,</span> <span class="token string">'logger'</span><span class="token punctuation">]</span>
    checks <span class="token operator">=</span> <span class="token punctuation">[</span>item <span class="token keyword">in</span> answer_code <span class="token keyword">for</span> item <span class="token keyword">in</span> required_handling<span class="token punctuation">]</span>
    <span class="token keyword">if</span> <span class="token builtin">sum</span><span class="token punctuation">(</span>checks<span class="token punctuation">)</span> <span class="token operator">&gt;=</span> <span class="token number">3</span><span class="token punctuation">:</span>
        score <span class="token operator">+=</span> <span class="token number">15</span>
    
    <span class="token comment"># 4. 性能优化（15分）</span>
    optimizations <span class="token operator">=</span> <span class="token punctuation">[</span><span class="token string">'chunksize'</span><span class="token punctuation">,</span> <span class="token string">'dtype'</span><span class="token punctuation">,</span> <span class="token string">'select_dtypes'</span><span class="token punctuation">,</span> <span class="token string">'observed=True'</span><span class="token punctuation">]</span>
    optim_count <span class="token operator">=</span> <span class="token builtin">sum</span><span class="token punctuation">(</span><span class="token number">1</span> <span class="token keyword">for</span> opt <span class="token keyword">in</span> optimizations <span class="token keyword">if</span> opt <span class="token keyword">in</span> answer_code<span class="token punctuation">)</span>
    score <span class="token operator">+=</span> <span class="token builtin">min</span><span class="token punctuation">(</span><span class="token number">15</span><span class="token punctuation">,</span> optim_count <span class="token operator">*</span> <span class="token number">5</span><span class="token punctuation">)</span>
    
    <span class="token comment"># 5. 代码规范（10分）</span>
    <span class="token keyword">import</span> pep8
    checker <span class="token operator">=</span> pep8<span class="token punctuation">.</span>Checker<span class="token punctuation">(</span><span class="token string">'data_processor_optimized.py'</span><span class="token punctuation">,</span> ignore<span class="token operator">=</span><span class="token punctuation">[</span><span class="token string">'E501'</span><span class="token punctuation">]</span><span class="token punctuation">)</span>
    errors <span class="token operator">=</span> <span class="token builtin">list</span><span class="token punctuation">(</span>checker<span class="token punctuation">.</span>check_all<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
    <span class="token keyword">if</span> errors <span class="token operator">&lt;=</span> <span class="token number">5</span><span class="token punctuation">:</span>
        score <span class="token operator">+=</span> <span class="token number">10</span>
    <span class="token keyword">elif</span> errors <span class="token operator">&lt;=</span> <span class="token number">10</span><span class="token punctuation">:</span>
        score <span class="token operator">+=</span> <span class="token number">5</span>
    
    <span class="token comment"># 6. 文档和类型提示（10分）</span>
    <span class="token keyword">if</span> <span class="token string">'def process_data(input_file: str)'</span> <span class="token keyword">in</span> answer_code<span class="token punctuation">:</span>
        score <span class="token operator">+=</span> <span class="token number">5</span>
    <span class="token keyword">if</span> <span class="token string">'"""处理CSV文件'</span> <span class="token keyword">in</span> answer_code<span class="token punctuation">:</span>
        score <span class="token operator">+=</span> <span class="token number">5</span>
    
    <span class="token keyword">return</span> <span class="token builtin">min</span><span class="token punctuation">(</span><span class="token number">100</span><span class="token punctuation">,</span> score<span class="token punctuation">)</span>

<span class="token comment"># 评分项详细列表</span>
<span class="token triple-quoted-string string">"""
1. 代码可运行性（30分）
   - 能成功导入并执行
   - 处理测试数据不报错

2. 版本兼容性修复（20分）
   - 修复applymap问题（10分）
   - 使用合适的替代方法（10分）

3. 错误处理（15分）
   - try-except结构（5分）
   - 日志记录（5分）
   - 具体异常类型处理（5分）

4. 性能优化（15分）
   - 大文件处理考虑（5分）
   - 内存优化（5分）
   - 分组优化（5分）

5. 代码规范（10分）
   - PEP 8合规性（10分）

6. 文档（10分）
   - 函数文档字符串（5分）
   - 类型提示（5分）
"""</span></pre><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _33882ae"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _28d7e84"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg></div><hr><h2><strong><span>示例 2：数据分析与可视化</span></strong></h2><p class="ds-markdown-paragraph"><strong><span>Query（任务描述）</span></strong><span></span><br><span>我有一份某电商平台2023年的销售数据，请帮我：</span></p><ol start="1"><li><p class="ds-markdown-paragraph"><span>分析月度销售趋势和季节性规律</span></p></li><li><p class="ds-markdown-paragraph"><span>识别销售额最高的商品类别和区域</span></p></li><li><p class="ds-markdown-paragraph"><span>分析客户购买行为（如客单价、复购率）</span></p></li><li><p class="ds-markdown-paragraph"><span>生成可视化图表，包括：</span></p><ul><li><p class="ds-markdown-paragraph"><span>月度销售额折线图</span></p></li><li><p class="ds-markdown-paragraph"><span>商品类别销售额饼图</span></p></li><li><p class="ds-markdown-paragraph"><span>区域销售额热力图</span></p></li><li><p class="ds-markdown-paragraph"><span>客户价值分布直方图</span></p></li></ul></li><li><p class="ds-markdown-paragraph"><span>提供业务改进建议</span></p></li></ol><p class="ds-markdown-paragraph"><strong><span>Context（上下文文件）</span></strong></p><div class="md-code-block md-code-block-light"><div class="md-code-block-banner-wrap"><div class="md-code-block-banner md-code-block-banner-lite"><div class="_121d384"><div class="d2a24f03"><span class="d813de27">csv</span></div><div class="d2a24f03 _246a029"><div class="efa13877"><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon" style="margin-right: 4px;"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.14923 4.02032C7.11191 4.02032 7.87977 4.02017 8.49591 4.07599C9.12122 4.1327 9.65786 4.25188 10.1414 4.53107C10.7201 4.8653 11.2008 5.34591 11.535 5.92462C11.8142 6.40818 11.9333 6.94482 11.9901 7.57013C12.0459 8.18625 12.0457 8.9542 12.0457 9.91681C12.0457 10.8795 12.0459 11.6474 11.9901 12.2635C11.9333 12.8888 11.8142 13.4254 11.535 13.909C11.2008 14.4877 10.7201 14.9683 10.1414 15.3026C9.65786 15.5817 9.12122 15.7009 8.49591 15.7576C7.87977 15.8134 7.1119 15.8133 6.14923 15.8133C5.18661 15.8133 4.41868 15.8134 3.80255 15.7576C3.17724 15.7009 2.6406 15.5817 2.15704 15.3026C1.57834 14.9684 1.09772 14.4877 0.763489 13.909C0.484305 13.4254 0.365123 12.8888 0.308411 12.2635C0.252587 11.6474 0.252747 10.8795 0.252747 9.91681C0.252747 8.95419 0.252603 8.18625 0.308411 7.57013C0.365123 6.94482 0.484305 6.40818 0.763489 5.92462C1.09771 5.3459 1.57833 4.86529 2.15704 4.53107C2.6406 4.25188 3.17724 4.1327 3.80255 4.07599C4.41868 4.02018 5.1866 4.02032 6.14923 4.02032ZM6.14923 5.37775C5.16175 5.37775 4.46628 5.37761 3.9256 5.42657C3.39428 5.47473 3.07853 5.56574 2.83575 5.70587C2.46313 5.92106 2.15348 6.23071 1.93829 6.60333C1.79817 6.84611 1.70715 7.16185 1.659 7.69318C1.61004 8.23385 1.61017 8.92934 1.61017 9.91681C1.61017 10.9043 1.61002 11.5998 1.659 12.1404C1.70715 12.6717 1.79817 12.9875 1.93829 13.2303C2.15349 13.6029 2.46315 13.9126 2.83575 14.1277C3.07853 14.2679 3.39428 14.3589 3.9256 14.407C4.46628 14.456 5.16176 14.4559 6.14923 14.4559C7.13675 14.4559 7.83218 14.456 8.37286 14.407C8.90419 14.3589 9.21993 14.2679 9.46271 14.1277C9.83529 13.9126 10.145 13.6029 10.3602 13.2303C10.5003 12.9875 10.5913 12.6718 10.6395 12.1404C10.6884 11.5998 10.6883 10.9043 10.6883 9.91681C10.6883 8.92935 10.6884 8.23385 10.6395 7.69318C10.5913 7.16185 10.5003 6.84611 10.3602 6.60333C10.145 6.23072 9.8353 5.92107 9.46271 5.70587C9.21993 5.56574 8.90418 5.47473 8.37286 5.42657C7.83218 5.3776 7.13676 5.37775 6.14923 5.37775ZM9.80157 0.367981C10.7637 0.367981 11.5313 0.367886 12.1473 0.423645C12.7725 0.480313 13.3093 0.598765 13.7928 0.877747C14.3716 1.21192 14.852 1.69355 15.1863 2.27228C15.4655 2.75575 15.5857 3.29165 15.6424 3.91681C15.6982 4.53301 15.6971 5.30161 15.6971 6.26447V7.8299C15.6971 8.29265 15.6989 8.58994 15.6649 8.84845C15.4667 10.3525 14.4009 11.5738 12.9832 11.9988V10.5467C13.6973 10.1903 14.2104 9.49662 14.3192 8.67169C14.3387 8.52348 14.3406 8.3358 14.3406 7.8299V6.26447C14.3406 5.27707 14.3398 4.58149 14.2908 4.04083C14.2427 3.50969 14.1526 3.19373 14.0125 2.95099C13.7974 2.5785 13.4875 2.2687 13.1151 2.05353C12.8723 1.91347 12.5563 1.82237 12.0252 1.77423C11.4846 1.72528 10.7888 1.7254 9.80157 1.7254H7.71466C6.75614 1.72559 5.92659 2.27697 5.52325 3.07892H4.07013C4.54215 1.51132 5.99314 0.368192 7.71466 0.367981H9.80157Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">复制</span></span><div class="ds-focus-ring"></div></button><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M15.3695 11.411L15.1234 12.8866C14.8869 14.3042 13.6603 15.3436 12.223 15.3436H3.7767C2.33954 15.3434 1.11276 14.3042 0.876312 12.8866L0.630219 11.411L2.05405 11.1747L2.29916 12.6493C2.41969 13.3713 3.04472 13.9001 3.7767 13.9003H12.223C12.9551 13.9002 13.58 13.3713 13.7005 12.6493L13.9456 11.1747L15.3695 11.411ZM8.72202 8.994C8.77714 8.93934 8.83789 8.88106 8.90268 8.81627L12.4828 5.23424L13.5042 6.25572L9.92221 9.8358C9.63947 10.1185 9.3876 10.3732 9.15854 10.5575C8.91889 10.7503 8.6395 10.9224 8.28647 10.9784C8.09708 11.0083 7.9036 11.0083 7.7142 10.9784C7.36103 10.9224 7.08087 10.7503 6.84116 10.5575C6.61212 10.3732 6.36019 10.1185 6.07748 9.8358L2.49643 6.25572L3.51694 5.23424L7.09702 8.81627C7.16216 8.88142 7.22327 8.94006 7.27866 8.99498V1.3065H8.72202V8.994Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">下载</span></span><div class="ds-focus-ring"></div></button></div></div></div></div></div><pre><span class="token value"># sales_data_2023.csv（部分示例）</span>
<span class="token value">order_id</span><span class="token punctuation">,</span><span class="token value">customer_id</span><span class="token punctuation">,</span><span class="token value">order_date</span><span class="token punctuation">,</span><span class="token value">product_category</span><span class="token punctuation">,</span><span class="token value">region</span><span class="token punctuation">,</span><span class="token value">quantity</span><span class="token punctuation">,</span><span class="token value">unit_price</span><span class="token punctuation">,</span><span class="token value">payment_method</span>
<span class="token value">1001</span><span class="token punctuation">,</span><span class="token value">C001</span><span class="token punctuation">,</span><span class="token value">2023-01-05</span><span class="token punctuation">,</span><span class="token value">Electronics</span><span class="token punctuation">,</span><span class="token value">North</span><span class="token punctuation">,</span><span class="token value">2</span><span class="token punctuation">,</span><span class="token value">599.99</span><span class="token punctuation">,</span><span class="token value">Credit Card</span>
<span class="token value">1002</span><span class="token punctuation">,</span><span class="token value">C002</span><span class="token punctuation">,</span><span class="token value">2023-01-07</span><span class="token punctuation">,</span><span class="token value">Clothing</span><span class="token punctuation">,</span><span class="token value">South</span><span class="token punctuation">,</span><span class="token value">1</span><span class="token punctuation">,</span><span class="token value">89.50</span><span class="token punctuation">,</span><span class="token value">PayPal</span>
<span class="token value">1003</span><span class="token punctuation">,</span><span class="token value">C001</span><span class="token punctuation">,</span><span class="token value">2023-01-15</span><span class="token punctuation">,</span><span class="token value">Electronics</span><span class="token punctuation">,</span><span class="token value">North</span><span class="token punctuation">,</span><span class="token value">1</span><span class="token punctuation">,</span><span class="token value">799.99</span><span class="token punctuation">,</span><span class="token value">Credit Card</span>
<span class="token value">1004</span><span class="token punctuation">,</span><span class="token value">C003</span><span class="token punctuation">,</span><span class="token value">2023-01-20</span><span class="token punctuation">,</span><span class="token value">Home &amp; Kitchen</span><span class="token punctuation">,</span><span class="token value">East</span><span class="token punctuation">,</span><span class="token value">3</span><span class="token punctuation">,</span><span class="token value">49.99</span><span class="token punctuation">,</span><span class="token value">Cash</span>
<span class="token value">1005</span><span class="token punctuation">,</span><span class="token value">C004</span><span class="token punctuation">,</span><span class="token value">2023-02-03</span><span class="token punctuation">,</span><span class="token value">Books</span><span class="token punctuation">,</span><span class="token value">West</span><span class="token punctuation">,</span><span class="token value">5</span><span class="token punctuation">,</span><span class="token value">19.99</span><span class="token punctuation">,</span><span class="token value">Debit Card</span>
<span class="token value">...（更多数据）</span>

<span class="token value"># region_coordinates.csv</span>
<span class="token value">region</span><span class="token punctuation">,</span><span class="token value">latitude</span><span class="token punctuation">,</span><span class="token value">longitude</span>
<span class="token value">North</span><span class="token punctuation">,</span><span class="token value">40.7128</span><span class="token punctuation">,</span><span class="token value">-74.0060</span>
<span class="token value">South</span><span class="token punctuation">,</span><span class="token value">33.7490</span><span class="token punctuation">,</span><span class="token value">-84.3880</span>
<span class="token value">East</span><span class="token punctuation">,</span><span class="token value">38.9072</span><span class="token punctuation">,</span><span class="token value">-77.0369</span>
<span class="token value">West</span><span class="token punctuation">,</span><span class="token value">34.0522</span><span class="token punctuation">,</span><span class="token value">-118.2437</span>

<span class="token value"># 任务要求：</span>
<span class="token value"># 1. 使用Python进行分析</span>
<span class="token value"># 2. 图表需美观且信息清晰</span>
<span class="token value"># 3. 输出分析报告（Markdown格式）</span></pre><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _33882ae"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _28d7e84"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg></div><p class="ds-markdown-paragraph"><strong><span>参考答案（Reference Answer）</span></strong></p><div class="md-code-block md-code-block-light"><div class="md-code-block-banner-wrap"><div class="md-code-block-banner md-code-block-banner-lite"><div class="_121d384"><div class="d2a24f03"><span class="d813de27">python</span></div><div class="d2a24f03 _246a029"><div class="efa13877"><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon" style="margin-right: 4px;"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.14923 4.02032C7.11191 4.02032 7.87977 4.02017 8.49591 4.07599C9.12122 4.1327 9.65786 4.25188 10.1414 4.53107C10.7201 4.8653 11.2008 5.34591 11.535 5.92462C11.8142 6.40818 11.9333 6.94482 11.9901 7.57013C12.0459 8.18625 12.0457 8.9542 12.0457 9.91681C12.0457 10.8795 12.0459 11.6474 11.9901 12.2635C11.9333 12.8888 11.8142 13.4254 11.535 13.909C11.2008 14.4877 10.7201 14.9683 10.1414 15.3026C9.65786 15.5817 9.12122 15.7009 8.49591 15.7576C7.87977 15.8134 7.1119 15.8133 6.14923 15.8133C5.18661 15.8133 4.41868 15.8134 3.80255 15.7576C3.17724 15.7009 2.6406 15.5817 2.15704 15.3026C1.57834 14.9684 1.09772 14.4877 0.763489 13.909C0.484305 13.4254 0.365123 12.8888 0.308411 12.2635C0.252587 11.6474 0.252747 10.8795 0.252747 9.91681C0.252747 8.95419 0.252603 8.18625 0.308411 7.57013C0.365123 6.94482 0.484305 6.40818 0.763489 5.92462C1.09771 5.3459 1.57833 4.86529 2.15704 4.53107C2.6406 4.25188 3.17724 4.1327 3.80255 4.07599C4.41868 4.02018 5.1866 4.02032 6.14923 4.02032ZM6.14923 5.37775C5.16175 5.37775 4.46628 5.37761 3.9256 5.42657C3.39428 5.47473 3.07853 5.56574 2.83575 5.70587C2.46313 5.92106 2.15348 6.23071 1.93829 6.60333C1.79817 6.84611 1.70715 7.16185 1.659 7.69318C1.61004 8.23385 1.61017 8.92934 1.61017 9.91681C1.61017 10.9043 1.61002 11.5998 1.659 12.1404C1.70715 12.6717 1.79817 12.9875 1.93829 13.2303C2.15349 13.6029 2.46315 13.9126 2.83575 14.1277C3.07853 14.2679 3.39428 14.3589 3.9256 14.407C4.46628 14.456 5.16176 14.4559 6.14923 14.4559C7.13675 14.4559 7.83218 14.456 8.37286 14.407C8.90419 14.3589 9.21993 14.2679 9.46271 14.1277C9.83529 13.9126 10.145 13.6029 10.3602 13.2303C10.5003 12.9875 10.5913 12.6718 10.6395 12.1404C10.6884 11.5998 10.6883 10.9043 10.6883 9.91681C10.6883 8.92935 10.6884 8.23385 10.6395 7.69318C10.5913 7.16185 10.5003 6.84611 10.3602 6.60333C10.145 6.23072 9.8353 5.92107 9.46271 5.70587C9.21993 5.56574 8.90418 5.47473 8.37286 5.42657C7.83218 5.3776 7.13676 5.37775 6.14923 5.37775ZM9.80157 0.367981C10.7637 0.367981 11.5313 0.367886 12.1473 0.423645C12.7725 0.480313 13.3093 0.598765 13.7928 0.877747C14.3716 1.21192 14.852 1.69355 15.1863 2.27228C15.4655 2.75575 15.5857 3.29165 15.6424 3.91681C15.6982 4.53301 15.6971 5.30161 15.6971 6.26447V7.8299C15.6971 8.29265 15.6989 8.58994 15.6649 8.84845C15.4667 10.3525 14.4009 11.5738 12.9832 11.9988V10.5467C13.6973 10.1903 14.2104 9.49662 14.3192 8.67169C14.3387 8.52348 14.3406 8.3358 14.3406 7.8299V6.26447C14.3406 5.27707 14.3398 4.58149 14.2908 4.04083C14.2427 3.50969 14.1526 3.19373 14.0125 2.95099C13.7974 2.5785 13.4875 2.2687 13.1151 2.05353C12.8723 1.91347 12.5563 1.82237 12.0252 1.77423C11.4846 1.72528 10.7888 1.7254 9.80157 1.7254H7.71466C6.75614 1.72559 5.92659 2.27697 5.52325 3.07892H4.07013C4.54215 1.51132 5.99314 0.368192 7.71466 0.367981H9.80157Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">复制</span></span><div class="ds-focus-ring"></div></button><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M15.3695 11.411L15.1234 12.8866C14.8869 14.3042 13.6603 15.3436 12.223 15.3436H3.7767C2.33954 15.3434 1.11276 14.3042 0.876312 12.8866L0.630219 11.411L2.05405 11.1747L2.29916 12.6493C2.41969 13.3713 3.04472 13.9001 3.7767 13.9003H12.223C12.9551 13.9002 13.58 13.3713 13.7005 12.6493L13.9456 11.1747L15.3695 11.411ZM8.72202 8.994C8.77714 8.93934 8.83789 8.88106 8.90268 8.81627L12.4828 5.23424L13.5042 6.25572L9.92221 9.8358C9.63947 10.1185 9.3876 10.3732 9.15854 10.5575C8.91889 10.7503 8.6395 10.9224 8.28647 10.9784C8.09708 11.0083 7.9036 11.0083 7.7142 10.9784C7.36103 10.9224 7.08087 10.7503 6.84116 10.5575C6.61212 10.3732 6.36019 10.1185 6.07748 9.8358L2.49643 6.25572L3.51694 5.23424L7.09702 8.81627C7.16216 8.88142 7.22327 8.94006 7.27866 8.99498V1.3065H8.72202V8.994Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">下载</span></span><div class="ds-focus-ring"></div></button></div></div></div></div></div><pre><span class="token comment"># sales_analysis.py</span>
<span class="token keyword">import</span> pandas <span class="token keyword">as</span> pd
<span class="token keyword">import</span> numpy <span class="token keyword">as</span> np
<span class="token keyword">import</span> matplotlib<span class="token punctuation">.</span>pyplot <span class="token keyword">as</span> plt
<span class="token keyword">import</span> seaborn <span class="token keyword">as</span> sns
<span class="token keyword">from</span> datetime <span class="token keyword">import</span> datetime
<span class="token keyword">import</span> warnings
warnings<span class="token punctuation">.</span>filterwarnings<span class="token punctuation">(</span><span class="token string">'ignore'</span><span class="token punctuation">)</span>

<span class="token comment"># 设置中文字体和样式</span>
plt<span class="token punctuation">.</span>rcParams<span class="token punctuation">[</span><span class="token string">'font.sans-serif'</span><span class="token punctuation">]</span> <span class="token operator">=</span> <span class="token punctuation">[</span><span class="token string">'SimHei'</span><span class="token punctuation">]</span>
plt<span class="token punctuation">.</span>rcParams<span class="token punctuation">[</span><span class="token string">'axes.unicode_minus'</span><span class="token punctuation">]</span> <span class="token operator">=</span> <span class="token boolean">False</span>
sns<span class="token punctuation">.</span>set_style<span class="token punctuation">(</span><span class="token string">"whitegrid"</span><span class="token punctuation">)</span>

<span class="token keyword">class</span> <span class="token class-name">SalesAnalyzer</span><span class="token punctuation">:</span>
    <span class="token keyword">def</span> <span class="token function">__init__</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> data_path<span class="token punctuation">,</span> region_path<span class="token punctuation">)</span><span class="token punctuation">:</span>
        <span class="token triple-quoted-string string">"""
        初始化分析器
        
        Args:
            data_path: 销售数据路径
            region_path: 区域坐标数据路径
        """</span>
        self<span class="token punctuation">.</span>df <span class="token operator">=</span> pd<span class="token punctuation">.</span>read_csv<span class="token punctuation">(</span>data_path<span class="token punctuation">,</span> parse_dates<span class="token operator">=</span><span class="token punctuation">[</span><span class="token string">'order_date'</span><span class="token punctuation">]</span><span class="token punctuation">)</span>
        self<span class="token punctuation">.</span>regions <span class="token operator">=</span> pd<span class="token punctuation">.</span>read_csv<span class="token punctuation">(</span>region_path<span class="token punctuation">)</span>
        self<span class="token punctuation">.</span>_preprocess_data<span class="token punctuation">(</span><span class="token punctuation">)</span>
        
    <span class="token keyword">def</span> <span class="token function">_preprocess_data</span><span class="token punctuation">(</span>self<span class="token punctuation">)</span><span class="token punctuation">:</span>
        <span class="token triple-quoted-string string">"""数据预处理"""</span>
        <span class="token comment"># 计算总销售额</span>
        self<span class="token punctuation">.</span>df<span class="token punctuation">[</span><span class="token string">'total_sales'</span><span class="token punctuation">]</span> <span class="token operator">=</span> self<span class="token punctuation">.</span>df<span class="token punctuation">[</span><span class="token string">'quantity'</span><span class="token punctuation">]</span> <span class="token operator">*</span> self<span class="token punctuation">.</span>df<span class="token punctuation">[</span><span class="token string">'unit_price'</span><span class="token punctuation">]</span>
        
        <span class="token comment"># 提取月份和季度</span>
        self<span class="token punctuation">.</span>df<span class="token punctuation">[</span><span class="token string">'year_month'</span><span class="token punctuation">]</span> <span class="token operator">=</span> self<span class="token punctuation">.</span>df<span class="token punctuation">[</span><span class="token string">'order_date'</span><span class="token punctuation">]</span><span class="token punctuation">.</span>dt<span class="token punctuation">.</span>to_period<span class="token punctuation">(</span><span class="token string">'M'</span><span class="token punctuation">)</span>
        self<span class="token punctuation">.</span>df<span class="token punctuation">[</span><span class="token string">'quarter'</span><span class="token punctuation">]</span> <span class="token operator">=</span> self<span class="token punctuation">.</span>df<span class="token punctuation">[</span><span class="token string">'order_date'</span><span class="token punctuation">]</span><span class="token punctuation">.</span>dt<span class="token punctuation">.</span>quarter
        self<span class="token punctuation">.</span>df<span class="token punctuation">[</span><span class="token string">'month'</span><span class="token punctuation">]</span> <span class="token operator">=</span> self<span class="token punctuation">.</span>df<span class="token punctuation">[</span><span class="token string">'order_date'</span><span class="token punctuation">]</span><span class="token punctuation">.</span>dt<span class="token punctuation">.</span>month
        
        <span class="token comment"># 计算客户价值</span>
        customer_stats <span class="token operator">=</span> self<span class="token punctuation">.</span>df<span class="token punctuation">.</span>groupby<span class="token punctuation">(</span><span class="token string">'customer_id'</span><span class="token punctuation">)</span><span class="token punctuation">.</span>agg<span class="token punctuation">(</span><span class="token punctuation">{</span>
            <span class="token string">'total_sales'</span><span class="token punctuation">:</span> <span class="token string">'sum'</span><span class="token punctuation">,</span>
            <span class="token string">'order_id'</span><span class="token punctuation">:</span> <span class="token string">'nunique'</span>
        <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">.</span>rename<span class="token punctuation">(</span>columns<span class="token operator">=</span><span class="token punctuation">{</span><span class="token string">'order_id'</span><span class="token punctuation">:</span> <span class="token string">'order_count'</span><span class="token punctuation">}</span><span class="token punctuation">)</span>
        customer_stats<span class="token punctuation">[</span><span class="token string">'avg_order_value'</span><span class="token punctuation">]</span> <span class="token operator">=</span> customer_stats<span class="token punctuation">[</span><span class="token string">'total_sales'</span><span class="token punctuation">]</span> <span class="token operator">/</span> customer_stats<span class="token punctuation">[</span><span class="token string">'order_count'</span><span class="token punctuation">]</span>
        self<span class="token punctuation">.</span>customer_stats <span class="token operator">=</span> customer_stats
        
    <span class="token keyword">def</span> <span class="token function">monthly_trend_analysis</span><span class="token punctuation">(</span>self<span class="token punctuation">)</span><span class="token punctuation">:</span>
        <span class="token triple-quoted-string string">"""月度趋势分析"""</span>
        monthly_sales <span class="token operator">=</span> self<span class="token punctuation">.</span>df<span class="token punctuation">.</span>groupby<span class="token punctuation">(</span><span class="token string">'year_month'</span><span class="token punctuation">)</span><span class="token punctuation">[</span><span class="token string">'total_sales'</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token builtin">sum</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span>reset_index<span class="token punctuation">(</span><span class="token punctuation">)</span>
        monthly_sales<span class="token punctuation">[</span><span class="token string">'year_month'</span><span class="token punctuation">]</span> <span class="token operator">=</span> monthly_sales<span class="token punctuation">[</span><span class="token string">'year_month'</span><span class="token punctuation">]</span><span class="token punctuation">.</span>dt<span class="token punctuation">.</span>to_timestamp<span class="token punctuation">(</span><span class="token punctuation">)</span>
        
        plt<span class="token punctuation">.</span>figure<span class="token punctuation">(</span>figsize<span class="token operator">=</span><span class="token punctuation">(</span><span class="token number">12</span><span class="token punctuation">,</span> <span class="token number">6</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
        plt<span class="token punctuation">.</span>plot<span class="token punctuation">(</span>monthly_sales<span class="token punctuation">[</span><span class="token string">'year_month'</span><span class="token punctuation">]</span><span class="token punctuation">,</span> monthly_sales<span class="token punctuation">[</span><span class="token string">'total_sales'</span><span class="token punctuation">]</span><span class="token punctuation">,</span> 
                marker<span class="token operator">=</span><span class="token string">'o'</span><span class="token punctuation">,</span> linewidth<span class="token operator">=</span><span class="token number">2</span><span class="token punctuation">,</span> markersize<span class="token operator">=</span><span class="token number">6</span><span class="token punctuation">)</span>
        plt<span class="token punctuation">.</span>title<span class="token punctuation">(</span><span class="token string">'2023年月度销售趋势'</span><span class="token punctuation">,</span> fontsize<span class="token operator">=</span><span class="token number">16</span><span class="token punctuation">,</span> fontweight<span class="token operator">=</span><span class="token string">'bold'</span><span class="token punctuation">)</span>
        plt<span class="token punctuation">.</span>xlabel<span class="token punctuation">(</span><span class="token string">'月份'</span><span class="token punctuation">,</span> fontsize<span class="token operator">=</span><span class="token number">12</span><span class="token punctuation">)</span>
        plt<span class="token punctuation">.</span>ylabel<span class="token punctuation">(</span><span class="token string">'销售额（元）'</span><span class="token punctuation">,</span> fontsize<span class="token operator">=</span><span class="token number">12</span><span class="token punctuation">)</span>
        plt<span class="token punctuation">.</span>grid<span class="token punctuation">(</span><span class="token boolean">True</span><span class="token punctuation">,</span> alpha<span class="token operator">=</span><span class="token number">0.3</span><span class="token punctuation">)</span>
        plt<span class="token punctuation">.</span>tight_layout<span class="token punctuation">(</span><span class="token punctuation">)</span>
        plt<span class="token punctuation">.</span>savefig<span class="token punctuation">(</span><span class="token string">'monthly_sales_trend.png'</span><span class="token punctuation">,</span> dpi<span class="token operator">=</span><span class="token number">300</span><span class="token punctuation">,</span> bbox_inches<span class="token operator">=</span><span class="token string">'tight'</span><span class="token punctuation">)</span>
        plt<span class="token punctuation">.</span>show<span class="token punctuation">(</span><span class="token punctuation">)</span>
        
        <span class="token keyword">return</span> monthly_sales
    
    <span class="token keyword">def</span> <span class="token function">category_analysis</span><span class="token punctuation">(</span>self<span class="token punctuation">)</span><span class="token punctuation">:</span>
        <span class="token triple-quoted-string string">"""商品类别分析"""</span>
        category_sales <span class="token operator">=</span> self<span class="token punctuation">.</span>df<span class="token punctuation">.</span>groupby<span class="token punctuation">(</span><span class="token string">'product_category'</span><span class="token punctuation">)</span><span class="token punctuation">[</span><span class="token string">'total_sales'</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token builtin">sum</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span>sort_values<span class="token punctuation">(</span>ascending<span class="token operator">=</span><span class="token boolean">False</span><span class="token punctuation">)</span>
        
        plt<span class="token punctuation">.</span>figure<span class="token punctuation">(</span>figsize<span class="token operator">=</span><span class="token punctuation">(</span><span class="token number">10</span><span class="token punctuation">,</span> <span class="token number">10</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
        colors <span class="token operator">=</span> plt<span class="token punctuation">.</span>cm<span class="token punctuation">.</span>Set3<span class="token punctuation">(</span>np<span class="token punctuation">.</span>linspace<span class="token punctuation">(</span><span class="token number">0</span><span class="token punctuation">,</span> <span class="token number">1</span><span class="token punctuation">,</span> <span class="token builtin">len</span><span class="token punctuation">(</span>category_sales<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
        wedges<span class="token punctuation">,</span> texts<span class="token punctuation">,</span> autotexts <span class="token operator">=</span> plt<span class="token punctuation">.</span>pie<span class="token punctuation">(</span>category_sales<span class="token punctuation">.</span>values<span class="token punctuation">,</span> labels<span class="token operator">=</span>category_sales<span class="token punctuation">.</span>index<span class="token punctuation">,</span>
                                          autopct<span class="token operator">=</span><span class="token string">'%1.1f%%'</span><span class="token punctuation">,</span> colors<span class="token operator">=</span>colors<span class="token punctuation">,</span>
                                          startangle<span class="token operator">=</span><span class="token number">90</span><span class="token punctuation">,</span> textprops<span class="token operator">=</span><span class="token punctuation">{</span><span class="token string">'fontsize'</span><span class="token punctuation">:</span> <span class="token number">10</span><span class="token punctuation">}</span><span class="token punctuation">)</span>
        
        <span class="token comment"># 美化百分比标签</span>
        <span class="token keyword">for</span> autotext <span class="token keyword">in</span> autotexts<span class="token punctuation">:</span>
            autotext<span class="token punctuation">.</span>set_color<span class="token punctuation">(</span><span class="token string">'white'</span><span class="token punctuation">)</span>
            autotext<span class="token punctuation">.</span>set_fontweight<span class="token punctuation">(</span><span class="token string">'bold'</span><span class="token punctuation">)</span>
        
        plt<span class="token punctuation">.</span>title<span class="token punctuation">(</span><span class="token string">'商品类别销售额占比'</span><span class="token punctuation">,</span> fontsize<span class="token operator">=</span><span class="token number">16</span><span class="token punctuation">,</span> fontweight<span class="token operator">=</span><span class="token string">'bold'</span><span class="token punctuation">)</span>
        plt<span class="token punctuation">.</span>savefig<span class="token punctuation">(</span><span class="token string">'category_sales_pie.png'</span><span class="token punctuation">,</span> dpi<span class="token operator">=</span><span class="token number">300</span><span class="token punctuation">,</span> bbox_inches<span class="token operator">=</span><span class="token string">'tight'</span><span class="token punctuation">)</span>
        plt<span class="token punctuation">.</span>show<span class="token punctuation">(</span><span class="token punctuation">)</span>
        
        <span class="token keyword">return</span> category_sales
    
    <span class="token keyword">def</span> <span class="token function">region_analysis</span><span class="token punctuation">(</span>self<span class="token punctuation">)</span><span class="token punctuation">:</span>
        <span class="token triple-quoted-string string">"""区域分析"""</span>
        region_sales <span class="token operator">=</span> self<span class="token punctuation">.</span>df<span class="token punctuation">.</span>groupby<span class="token punctuation">(</span><span class="token string">'region'</span><span class="token punctuation">)</span><span class="token punctuation">[</span><span class="token string">'total_sales'</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token builtin">sum</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span>reset_index<span class="token punctuation">(</span><span class="token punctuation">)</span>
        
        <span class="token comment"># 合并坐标数据</span>
        region_sales <span class="token operator">=</span> pd<span class="token punctuation">.</span>merge<span class="token punctuation">(</span>region_sales<span class="token punctuation">,</span> self<span class="token punctuation">.</span>regions<span class="token punctuation">,</span> on<span class="token operator">=</span><span class="token string">'region'</span><span class="token punctuation">)</span>
        
        plt<span class="token punctuation">.</span>figure<span class="token punctuation">(</span>figsize<span class="token operator">=</span><span class="token punctuation">(</span><span class="token number">10</span><span class="token punctuation">,</span> <span class="token number">8</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
        scatter <span class="token operator">=</span> plt<span class="token punctuation">.</span>scatter<span class="token punctuation">(</span>region_sales<span class="token punctuation">[</span><span class="token string">'longitude'</span><span class="token punctuation">]</span><span class="token punctuation">,</span> region_sales<span class="token punctuation">[</span><span class="token string">'latitude'</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
                             s<span class="token operator">=</span>region_sales<span class="token punctuation">[</span><span class="token string">'total_sales'</span><span class="token punctuation">]</span><span class="token operator">/</span><span class="token number">1000</span><span class="token punctuation">,</span>  <span class="token comment"># 大小表示销售额</span>
                             c<span class="token operator">=</span>region_sales<span class="token punctuation">[</span><span class="token string">'total_sales'</span><span class="token punctuation">]</span><span class="token punctuation">,</span>       <span class="token comment"># 颜色表示销售额</span>
                             cmap<span class="token operator">=</span><span class="token string">'YlOrRd'</span><span class="token punctuation">,</span> alpha<span class="token operator">=</span><span class="token number">0.7</span><span class="token punctuation">,</span>
                             edgecolors<span class="token operator">=</span><span class="token string">'black'</span><span class="token punctuation">,</span> linewidth<span class="token operator">=</span><span class="token number">0.5</span><span class="token punctuation">)</span>
        
        <span class="token comment"># 添加标签</span>
        <span class="token keyword">for</span> idx<span class="token punctuation">,</span> row <span class="token keyword">in</span> region_sales<span class="token punctuation">.</span>iterrows<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">:</span>
            plt<span class="token punctuation">.</span>annotate<span class="token punctuation">(</span><span class="token string-interpolation"><span class="token string">f"</span><span class="token interpolation"><span class="token punctuation">{</span>row<span class="token punctuation">[</span><span class="token string">'region'</span><span class="token punctuation">]</span><span class="token punctuation">}</span></span><span class="token string">\n¥</span><span class="token interpolation"><span class="token punctuation">{</span>row<span class="token punctuation">[</span><span class="token string">'total_sales'</span><span class="token punctuation">]</span><span class="token punctuation">:</span><span class="token format-spec">,.0f</span><span class="token punctuation">}</span></span><span class="token string">"</span></span><span class="token punctuation">,</span>
                        <span class="token punctuation">(</span>row<span class="token punctuation">[</span><span class="token string">'longitude'</span><span class="token punctuation">]</span><span class="token punctuation">,</span> row<span class="token punctuation">[</span><span class="token string">'latitude'</span><span class="token punctuation">]</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
                        fontsize<span class="token operator">=</span><span class="token number">9</span><span class="token punctuation">,</span> ha<span class="token operator">=</span><span class="token string">'center'</span><span class="token punctuation">)</span>
        
        plt<span class="token punctuation">.</span>colorbar<span class="token punctuation">(</span>scatter<span class="token punctuation">,</span> label<span class="token operator">=</span><span class="token string">'销售额（元）'</span><span class="token punctuation">)</span>
        plt<span class="token punctuation">.</span>title<span class="token punctuation">(</span><span class="token string">'区域销售额热力图'</span><span class="token punctuation">,</span> fontsize<span class="token operator">=</span><span class="token number">16</span><span class="token punctuation">,</span> fontweight<span class="token operator">=</span><span class="token string">'bold'</span><span class="token punctuation">)</span>
        plt<span class="token punctuation">.</span>xlabel<span class="token punctuation">(</span><span class="token string">'经度'</span><span class="token punctuation">)</span>
        plt<span class="token punctuation">.</span>ylabel<span class="token punctuation">(</span><span class="token string">'纬度'</span><span class="token punctuation">)</span>
        plt<span class="token punctuation">.</span>grid<span class="token punctuation">(</span><span class="token boolean">True</span><span class="token punctuation">,</span> alpha<span class="token operator">=</span><span class="token number">0.3</span><span class="token punctuation">)</span>
        plt<span class="token punctuation">.</span>tight_layout<span class="token punctuation">(</span><span class="token punctuation">)</span>
        plt<span class="token punctuation">.</span>savefig<span class="token punctuation">(</span><span class="token string">'region_sales_heatmap.png'</span><span class="token punctuation">,</span> dpi<span class="token operator">=</span><span class="token number">300</span><span class="token punctuation">,</span> bbox_inches<span class="token operator">=</span><span class="token string">'tight'</span><span class="token punctuation">)</span>
        plt<span class="token punctuation">.</span>show<span class="token punctuation">(</span><span class="token punctuation">)</span>
        
        <span class="token keyword">return</span> region_sales
    
    <span class="token keyword">def</span> <span class="token function">customer_behavior_analysis</span><span class="token punctuation">(</span>self<span class="token punctuation">)</span><span class="token punctuation">:</span>
        <span class="token triple-quoted-string string">"""客户行为分析"""</span>
        <span class="token comment"># 计算复购率</span>
        customer_orders <span class="token operator">=</span> self<span class="token punctuation">.</span>df<span class="token punctuation">.</span>groupby<span class="token punctuation">(</span><span class="token string">'customer_id'</span><span class="token punctuation">)</span><span class="token punctuation">[</span><span class="token string">'order_id'</span><span class="token punctuation">]</span><span class="token punctuation">.</span>nunique<span class="token punctuation">(</span><span class="token punctuation">)</span>
        repeat_customers <span class="token operator">=</span> <span class="token punctuation">(</span>customer_orders <span class="token operator">&gt;</span> <span class="token number">1</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token builtin">sum</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
        repurchase_rate <span class="token operator">=</span> repeat_customers <span class="token operator">/</span> <span class="token builtin">len</span><span class="token punctuation">(</span>customer_orders<span class="token punctuation">)</span> <span class="token operator">*</span> <span class="token number">100</span>
        
        <span class="token comment"># 客户价值分布</span>
        plt<span class="token punctuation">.</span>figure<span class="token punctuation">(</span>figsize<span class="token operator">=</span><span class="token punctuation">(</span><span class="token number">12</span><span class="token punctuation">,</span> <span class="token number">5</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
        
        plt<span class="token punctuation">.</span>subplot<span class="token punctuation">(</span><span class="token number">1</span><span class="token punctuation">,</span> <span class="token number">2</span><span class="token punctuation">,</span> <span class="token number">1</span><span class="token punctuation">)</span>
        plt<span class="token punctuation">.</span>hist<span class="token punctuation">(</span>self<span class="token punctuation">.</span>customer_stats<span class="token punctuation">[</span><span class="token string">'total_sales'</span><span class="token punctuation">]</span><span class="token punctuation">,</span> bins<span class="token operator">=</span><span class="token number">30</span><span class="token punctuation">,</span> 
                edgecolor<span class="token operator">=</span><span class="token string">'black'</span><span class="token punctuation">,</span> alpha<span class="token operator">=</span><span class="token number">0.7</span><span class="token punctuation">)</span>
        plt<span class="token punctuation">.</span>title<span class="token punctuation">(</span><span class="token string">'客户总价值分布'</span><span class="token punctuation">,</span> fontsize<span class="token operator">=</span><span class="token number">14</span><span class="token punctuation">)</span>
        plt<span class="token punctuation">.</span>xlabel<span class="token punctuation">(</span><span class="token string">'总消费额（元）'</span><span class="token punctuation">)</span>
        plt<span class="token punctuation">.</span>ylabel<span class="token punctuation">(</span><span class="token string">'客户数量'</span><span class="token punctuation">)</span>
        
        plt<span class="token punctuation">.</span>subplot<span class="token punctuation">(</span><span class="token number">1</span><span class="token punctuation">,</span> <span class="token number">2</span><span class="token punctuation">,</span> <span class="token number">2</span><span class="token punctuation">)</span>
        plt<span class="token punctuation">.</span>hist<span class="token punctuation">(</span>self<span class="token punctuation">.</span>customer_stats<span class="token punctuation">[</span><span class="token string">'avg_order_value'</span><span class="token punctuation">]</span><span class="token punctuation">,</span> bins<span class="token operator">=</span><span class="token number">30</span><span class="token punctuation">,</span>
                edgecolor<span class="token operator">=</span><span class="token string">'black'</span><span class="token punctuation">,</span> alpha<span class="token operator">=</span><span class="token number">0.7</span><span class="token punctuation">,</span> color<span class="token operator">=</span><span class="token string">'green'</span><span class="token punctuation">)</span>
        plt<span class="token punctuation">.</span>title<span class="token punctuation">(</span><span class="token string">'客单价分布'</span><span class="token punctuation">,</span> fontsize<span class="token operator">=</span><span class="token number">14</span><span class="token punctuation">)</span>
        plt<span class="token punctuation">.</span>xlabel<span class="token punctuation">(</span><span class="token string">'平均订单金额（元）'</span><span class="token punctuation">)</span>
        plt<span class="token punctuation">.</span>ylabel<span class="token punctuation">(</span><span class="token string">'客户数量'</span><span class="token punctuation">)</span>
        
        plt<span class="token punctuation">.</span>tight_layout<span class="token punctuation">(</span><span class="token punctuation">)</span>
        plt<span class="token punctuation">.</span>savefig<span class="token punctuation">(</span><span class="token string">'customer_distribution.png'</span><span class="token punctuation">,</span> dpi<span class="token operator">=</span><span class="token number">300</span><span class="token punctuation">,</span> bbox_inches<span class="token operator">=</span><span class="token string">'tight'</span><span class="token punctuation">)</span>
        plt<span class="token punctuation">.</span>show<span class="token punctuation">(</span><span class="token punctuation">)</span>
        
        <span class="token keyword">return</span> <span class="token punctuation">{</span>
            <span class="token string">'total_customers'</span><span class="token punctuation">:</span> <span class="token builtin">len</span><span class="token punctuation">(</span>self<span class="token punctuation">.</span>customer_stats<span class="token punctuation">)</span><span class="token punctuation">,</span>
            <span class="token string">'repeat_customers'</span><span class="token punctuation">:</span> repeat_customers<span class="token punctuation">,</span>
            <span class="token string">'repurchase_rate'</span><span class="token punctuation">:</span> repurchase_rate<span class="token punctuation">,</span>
            <span class="token string">'avg_order_value'</span><span class="token punctuation">:</span> self<span class="token punctuation">.</span>customer_stats<span class="token punctuation">[</span><span class="token string">'avg_order_value'</span><span class="token punctuation">]</span><span class="token punctuation">.</span>mean<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
            <span class="token string">'median_order_value'</span><span class="token punctuation">:</span> self<span class="token punctuation">.</span>customer_stats<span class="token punctuation">[</span><span class="token string">'avg_order_value'</span><span class="token punctuation">]</span><span class="token punctuation">.</span>median<span class="token punctuation">(</span><span class="token punctuation">)</span>
        <span class="token punctuation">}</span>
    
    <span class="token keyword">def</span> <span class="token function">generate_report</span><span class="token punctuation">(</span>self<span class="token punctuation">)</span><span class="token punctuation">:</span>
        <span class="token triple-quoted-string string">"""生成分析报告"""</span>
        <span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string">"="</span> <span class="token operator">*</span> <span class="token number">60</span><span class="token punctuation">)</span>
        <span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string">"                2023年电商销售分析报告"</span><span class="token punctuation">)</span>
        <span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string">"="</span> <span class="token operator">*</span> <span class="token number">60</span><span class="token punctuation">)</span>
        
        <span class="token comment"># 基本统计</span>
        <span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string-interpolation"><span class="token string">f"\n📊 基本统计信息:"</span></span><span class="token punctuation">)</span>
        <span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string-interpolation"><span class="token string">f"   总订单数: </span><span class="token interpolation"><span class="token punctuation">{</span><span class="token builtin">len</span><span class="token punctuation">(</span>self<span class="token punctuation">.</span>df<span class="token punctuation">)</span><span class="token punctuation">:</span><span class="token format-spec">,</span><span class="token punctuation">}</span></span><span class="token string">"</span></span><span class="token punctuation">)</span>
        <span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string-interpolation"><span class="token string">f"   总客户数: </span><span class="token interpolation"><span class="token punctuation">{</span>self<span class="token punctuation">.</span>df<span class="token punctuation">[</span><span class="token string">'customer_id'</span><span class="token punctuation">]</span><span class="token punctuation">.</span>nunique<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">:</span><span class="token format-spec">,</span><span class="token punctuation">}</span></span><span class="token string">"</span></span><span class="token punctuation">)</span>
        <span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string-interpolation"><span class="token string">f"   总销售额: ¥</span><span class="token interpolation"><span class="token punctuation">{</span>self<span class="token punctuation">.</span>df<span class="token punctuation">[</span><span class="token string">'total_sales'</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token builtin">sum</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">:</span><span class="token format-spec">,.2f</span><span class="token punctuation">}</span></span><span class="token string">"</span></span><span class="token punctuation">)</span>
        <span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string-interpolation"><span class="token string">f"   平均客单价: ¥</span><span class="token interpolation"><span class="token punctuation">{</span>self<span class="token punctuation">.</span>df<span class="token punctuation">[</span><span class="token string">'total_sales'</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token builtin">sum</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token operator">/</span>self<span class="token punctuation">.</span>df<span class="token punctuation">[</span><span class="token string">'customer_id'</span><span class="token punctuation">]</span><span class="token punctuation">.</span>nunique<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">:</span><span class="token format-spec">,.2f</span><span class="token punctuation">}</span></span><span class="token string">"</span></span><span class="token punctuation">)</span>
        
        <span class="token comment"># 月度趋势</span>
        monthly_sales <span class="token operator">=</span> self<span class="token punctuation">.</span>monthly_trend_analysis<span class="token punctuation">(</span><span class="token punctuation">)</span>
        best_month <span class="token operator">=</span> monthly_sales<span class="token punctuation">.</span>loc<span class="token punctuation">[</span>monthly_sales<span class="token punctuation">[</span><span class="token string">'total_sales'</span><span class="token punctuation">]</span><span class="token punctuation">.</span>idxmax<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">]</span>
        <span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string-interpolation"><span class="token string">f"\n📈 销售趋势分析:"</span></span><span class="token punctuation">)</span>
        <span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string-interpolation"><span class="token string">f"   销售额最高月份: </span><span class="token interpolation"><span class="token punctuation">{</span>best_month<span class="token punctuation">[</span><span class="token string">'year_month'</span><span class="token punctuation">]</span><span class="token punctuation">.</span>strftime<span class="token punctuation">(</span><span class="token string">'%Y-%m'</span><span class="token punctuation">)</span><span class="token punctuation">}</span></span><span class="token string">"</span></span><span class="token punctuation">)</span>
        <span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string-interpolation"><span class="token string">f"   最高月销售额: ¥</span><span class="token interpolation"><span class="token punctuation">{</span>best_month<span class="token punctuation">[</span><span class="token string">'total_sales'</span><span class="token punctuation">]</span><span class="token punctuation">:</span><span class="token format-spec">,.2f</span><span class="token punctuation">}</span></span><span class="token string">"</span></span><span class="token punctuation">)</span>
        <span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string-interpolation"><span class="token string">f"   月均销售额: ¥</span><span class="token interpolation"><span class="token punctuation">{</span>monthly_sales<span class="token punctuation">[</span><span class="token string">'total_sales'</span><span class="token punctuation">]</span><span class="token punctuation">.</span>mean<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">:</span><span class="token format-spec">,.2f</span><span class="token punctuation">}</span></span><span class="token string">"</span></span><span class="token punctuation">)</span>
        
        <span class="token comment"># 商品类别</span>
        category_sales <span class="token operator">=</span> self<span class="token punctuation">.</span>category_analysis<span class="token punctuation">(</span><span class="token punctuation">)</span>
        <span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string-interpolation"><span class="token string">f"\n🏷️ 商品类别分析:"</span></span><span class="token punctuation">)</span>
        <span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string">"   销售额Top 3类别:"</span><span class="token punctuation">)</span>
        <span class="token keyword">for</span> i<span class="token punctuation">,</span> <span class="token punctuation">(</span>category<span class="token punctuation">,</span> sales<span class="token punctuation">)</span> <span class="token keyword">in</span> <span class="token builtin">enumerate</span><span class="token punctuation">(</span>category_sales<span class="token punctuation">.</span>head<span class="token punctuation">(</span><span class="token number">3</span><span class="token punctuation">)</span><span class="token punctuation">.</span>items<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span> <span class="token number">1</span><span class="token punctuation">)</span><span class="token punctuation">:</span>
            <span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string-interpolation"><span class="token string">f"     </span><span class="token interpolation"><span class="token punctuation">{</span>i<span class="token punctuation">}</span></span><span class="token string">. </span><span class="token interpolation"><span class="token punctuation">{</span>category<span class="token punctuation">}</span></span><span class="token string">: ¥</span><span class="token interpolation"><span class="token punctuation">{</span>sales<span class="token punctuation">:</span><span class="token format-spec">,.2f</span><span class="token punctuation">}</span></span><span class="token string">"</span></span><span class="token punctuation">)</span>
        
        <span class="token comment"># 区域分析</span>
        region_sales <span class="token operator">=</span> self<span class="token punctuation">.</span>region_analysis<span class="token punctuation">(</span><span class="token punctuation">)</span>
        <span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string-interpolation"><span class="token string">f"\n📍 区域销售分析:"</span></span><span class="token punctuation">)</span>
        <span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string">"   各区域销售额:"</span><span class="token punctuation">)</span>
        <span class="token keyword">for</span> _<span class="token punctuation">,</span> row <span class="token keyword">in</span> region_sales<span class="token punctuation">.</span>sort_values<span class="token punctuation">(</span><span class="token string">'total_sales'</span><span class="token punctuation">,</span> ascending<span class="token operator">=</span><span class="token boolean">False</span><span class="token punctuation">)</span><span class="token punctuation">.</span>iterrows<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">:</span>
            <span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string-interpolation"><span class="token string">f"     </span><span class="token interpolation"><span class="token punctuation">{</span>row<span class="token punctuation">[</span><span class="token string">'region'</span><span class="token punctuation">]</span><span class="token punctuation">}</span></span><span class="token string">: ¥</span><span class="token interpolation"><span class="token punctuation">{</span>row<span class="token punctuation">[</span><span class="token string">'total_sales'</span><span class="token punctuation">]</span><span class="token punctuation">:</span><span class="token format-spec">,.2f</span><span class="token punctuation">}</span></span><span class="token string">"</span></span><span class="token punctuation">)</span>
        
        <span class="token comment"># 客户行为</span>
        customer_metrics <span class="token operator">=</span> self<span class="token punctuation">.</span>customer_behavior_analysis<span class="token punctuation">(</span><span class="token punctuation">)</span>
        <span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string-interpolation"><span class="token string">f"\n👥 客户行为分析:"</span></span><span class="token punctuation">)</span>
        <span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string-interpolation"><span class="token string">f"   复购率: </span><span class="token interpolation"><span class="token punctuation">{</span>customer_metrics<span class="token punctuation">[</span><span class="token string">'repurchase_rate'</span><span class="token punctuation">]</span><span class="token punctuation">:</span><span class="token format-spec">.1f</span><span class="token punctuation">}</span></span><span class="token string">%"</span></span><span class="token punctuation">)</span>
        <span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string-interpolation"><span class="token string">f"   平均客单价: ¥</span><span class="token interpolation"><span class="token punctuation">{</span>customer_metrics<span class="token punctuation">[</span><span class="token string">'avg_order_value'</span><span class="token punctuation">]</span><span class="token punctuation">:</span><span class="token format-spec">,.2f</span><span class="token punctuation">}</span></span><span class="token string">"</span></span><span class="token punctuation">)</span>
        <span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string-interpolation"><span class="token string">f"   中位数客单价: ¥</span><span class="token interpolation"><span class="token punctuation">{</span>customer_metrics<span class="token punctuation">[</span><span class="token string">'median_order_value'</span><span class="token punctuation">]</span><span class="token punctuation">:</span><span class="token format-spec">,.2f</span><span class="token punctuation">}</span></span><span class="token string">"</span></span><span class="token punctuation">)</span>
        
        <span class="token comment"># 业务建议</span>
        <span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string-interpolation"><span class="token string">f"\n💡 业务改进建议:"</span></span><span class="token punctuation">)</span>
        <span class="token keyword">print</span><span class="token punctuation">(</span><span class="token triple-quoted-string string">"""
    1. **聚焦优势品类**: 加大Electronics和Clothing品类的推广力度
    2. **区域拓展**: 考虑在South区域增加营销投入，提升市场份额
    3. **客户留存**: 针对复购客户推出忠诚度计划
    4. **季节策略**: Q4是销售高峰，提前备货并策划促销活动
    5. **支付优化**: 分析不同支付方式的转化率，优化支付体验
        """</span><span class="token punctuation">)</span>
        
        <span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string">"="</span> <span class="token operator">*</span> <span class="token number">60</span><span class="token punctuation">)</span>
        <span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string">"分析完成！图表已保存为PNG文件。"</span><span class="token punctuation">)</span>
        <span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string">"="</span> <span class="token operator">*</span> <span class="token number">60</span><span class="token punctuation">)</span>

<span class="token comment"># 执行分析</span>
<span class="token keyword">if</span> __name__ <span class="token operator">==</span> <span class="token string">"__main__"</span><span class="token punctuation">:</span>
    analyzer <span class="token operator">=</span> SalesAnalyzer<span class="token punctuation">(</span><span class="token string">"sales_data_2023.csv"</span><span class="token punctuation">,</span> <span class="token string">"region_coordinates.csv"</span><span class="token punctuation">)</span>
    analyzer<span class="token punctuation">.</span>generate_report<span class="token punctuation">(</span><span class="token punctuation">)</span></pre><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _33882ae"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _28d7e84"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg></div><p class="ds-markdown-paragraph"><strong><span>Rubric（评分标准）</span></strong></p><div class="md-code-block md-code-block-light"><div class="md-code-block-banner-wrap"><div class="md-code-block-banner md-code-block-banner-lite"><div class="_121d384"><div class="d2a24f03"><span class="d813de27">python</span></div><div class="d2a24f03 _246a029"><div class="efa13877"><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon" style="margin-right: 4px;"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.14923 4.02032C7.11191 4.02032 7.87977 4.02017 8.49591 4.07599C9.12122 4.1327 9.65786 4.25188 10.1414 4.53107C10.7201 4.8653 11.2008 5.34591 11.535 5.92462C11.8142 6.40818 11.9333 6.94482 11.9901 7.57013C12.0459 8.18625 12.0457 8.9542 12.0457 9.91681C12.0457 10.8795 12.0459 11.6474 11.9901 12.2635C11.9333 12.8888 11.8142 13.4254 11.535 13.909C11.2008 14.4877 10.7201 14.9683 10.1414 15.3026C9.65786 15.5817 9.12122 15.7009 8.49591 15.7576C7.87977 15.8134 7.1119 15.8133 6.14923 15.8133C5.18661 15.8133 4.41868 15.8134 3.80255 15.7576C3.17724 15.7009 2.6406 15.5817 2.15704 15.3026C1.57834 14.9684 1.09772 14.4877 0.763489 13.909C0.484305 13.4254 0.365123 12.8888 0.308411 12.2635C0.252587 11.6474 0.252747 10.8795 0.252747 9.91681C0.252747 8.95419 0.252603 8.18625 0.308411 7.57013C0.365123 6.94482 0.484305 6.40818 0.763489 5.92462C1.09771 5.3459 1.57833 4.86529 2.15704 4.53107C2.6406 4.25188 3.17724 4.1327 3.80255 4.07599C4.41868 4.02018 5.1866 4.02032 6.14923 4.02032ZM6.14923 5.37775C5.16175 5.37775 4.46628 5.37761 3.9256 5.42657C3.39428 5.47473 3.07853 5.56574 2.83575 5.70587C2.46313 5.92106 2.15348 6.23071 1.93829 6.60333C1.79817 6.84611 1.70715 7.16185 1.659 7.69318C1.61004 8.23385 1.61017 8.92934 1.61017 9.91681C1.61017 10.9043 1.61002 11.5998 1.659 12.1404C1.70715 12.6717 1.79817 12.9875 1.93829 13.2303C2.15349 13.6029 2.46315 13.9126 2.83575 14.1277C3.07853 14.2679 3.39428 14.3589 3.9256 14.407C4.46628 14.456 5.16176 14.4559 6.14923 14.4559C7.13675 14.4559 7.83218 14.456 8.37286 14.407C8.90419 14.3589 9.21993 14.2679 9.46271 14.1277C9.83529 13.9126 10.145 13.6029 10.3602 13.2303C10.5003 12.9875 10.5913 12.6718 10.6395 12.1404C10.6884 11.5998 10.6883 10.9043 10.6883 9.91681C10.6883 8.92935 10.6884 8.23385 10.6395 7.69318C10.5913 7.16185 10.5003 6.84611 10.3602 6.60333C10.145 6.23072 9.8353 5.92107 9.46271 5.70587C9.21993 5.56574 8.90418 5.47473 8.37286 5.42657C7.83218 5.3776 7.13676 5.37775 6.14923 5.37775ZM9.80157 0.367981C10.7637 0.367981 11.5313 0.367886 12.1473 0.423645C12.7725 0.480313 13.3093 0.598765 13.7928 0.877747C14.3716 1.21192 14.852 1.69355 15.1863 2.27228C15.4655 2.75575 15.5857 3.29165 15.6424 3.91681C15.6982 4.53301 15.6971 5.30161 15.6971 6.26447V7.8299C15.6971 8.29265 15.6989 8.58994 15.6649 8.84845C15.4667 10.3525 14.4009 11.5738 12.9832 11.9988V10.5467C13.6973 10.1903 14.2104 9.49662 14.3192 8.67169C14.3387 8.52348 14.3406 8.3358 14.3406 7.8299V6.26447C14.3406 5.27707 14.3398 4.58149 14.2908 4.04083C14.2427 3.50969 14.1526 3.19373 14.0125 2.95099C13.7974 2.5785 13.4875 2.2687 13.1151 2.05353C12.8723 1.91347 12.5563 1.82237 12.0252 1.77423C11.4846 1.72528 10.7888 1.7254 9.80157 1.7254H7.71466C6.75614 1.72559 5.92659 2.27697 5.52325 3.07892H4.07013C4.54215 1.51132 5.99314 0.368192 7.71466 0.367981H9.80157Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">复制</span></span><div class="ds-focus-ring"></div></button><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M15.3695 11.411L15.1234 12.8866C14.8869 14.3042 13.6603 15.3436 12.223 15.3436H3.7767C2.33954 15.3434 1.11276 14.3042 0.876312 12.8866L0.630219 11.411L2.05405 11.1747L2.29916 12.6493C2.41969 13.3713 3.04472 13.9001 3.7767 13.9003H12.223C12.9551 13.9002 13.58 13.3713 13.7005 12.6493L13.9456 11.1747L15.3695 11.411ZM8.72202 8.994C8.77714 8.93934 8.83789 8.88106 8.90268 8.81627L12.4828 5.23424L13.5042 6.25572L9.92221 9.8358C9.63947 10.1185 9.3876 10.3732 9.15854 10.5575C8.91889 10.7503 8.6395 10.9224 8.28647 10.9784C8.09708 11.0083 7.9036 11.0083 7.7142 10.9784C7.36103 10.9224 7.08087 10.7503 6.84116 10.5575C6.61212 10.3732 6.36019 10.1185 6.07748 9.8358L2.49643 6.25572L3.51694 5.23424L7.09702 8.81627C7.16216 8.88142 7.22327 8.94006 7.27866 8.99498V1.3065H8.72202V8.994Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">下载</span></span><div class="ds-focus-ring"></div></button></div></div></div></div></div><pre><span class="token keyword">def</span> <span class="token function">evaluate_analysis</span><span class="token punctuation">(</span>answer_code<span class="token punctuation">:</span> <span class="token builtin">str</span><span class="token punctuation">)</span> <span class="token operator">-</span><span class="token operator">&gt;</span> <span class="token builtin">int</span><span class="token punctuation">:</span>
    <span class="token triple-quoted-string string">"""
    评分函数（满分100）
    """</span>
    score <span class="token operator">=</span> <span class="token number">0</span>
    
    <span class="token keyword">try</span><span class="token punctuation">:</span>
        <span class="token comment"># 1. 代码完整性（20分）</span>
        required_methods <span class="token operator">=</span> <span class="token punctuation">[</span>
            <span class="token string">'monthly_trend_analysis'</span><span class="token punctuation">,</span>
            <span class="token string">'category_analysis'</span><span class="token punctuation">,</span> 
            <span class="token string">'region_analysis'</span><span class="token punctuation">,</span>
            <span class="token string">'customer_behavior_analysis'</span><span class="token punctuation">,</span>
            <span class="token string">'generate_report'</span>
        <span class="token punctuation">]</span>
        
        method_count <span class="token operator">=</span> <span class="token builtin">sum</span><span class="token punctuation">(</span><span class="token number">1</span> <span class="token keyword">for</span> method <span class="token keyword">in</span> required_methods <span class="token keyword">if</span> method <span class="token keyword">in</span> answer_code<span class="token punctuation">)</span>
        score <span class="token operator">+=</span> <span class="token builtin">min</span><span class="token punctuation">(</span><span class="token number">20</span><span class="token punctuation">,</span> method_count <span class="token operator">*</span> <span class="token number">4</span><span class="token punctuation">)</span>
        
        <span class="token comment"># 2. 数据预处理（15分）</span>
        preprocessing_checks <span class="token operator">=</span> <span class="token punctuation">[</span>
            <span class="token string">'parse_dates'</span><span class="token punctuation">,</span>  <span class="token comment"># 日期解析</span>
            <span class="token string">'total_sales'</span><span class="token punctuation">,</span>  <span class="token comment"># 计算销售额</span>
            <span class="token string">'groupby'</span><span class="token punctuation">,</span>      <span class="token comment"># 分组统计</span>
            <span class="token string">'dt.'</span><span class="token punctuation">,</span>          <span class="token comment"># 日期处理</span>
        <span class="token punctuation">]</span>
        
        check_count <span class="token operator">=</span> <span class="token builtin">sum</span><span class="token punctuation">(</span><span class="token number">1</span> <span class="token keyword">for</span> check <span class="token keyword">in</span> preprocessing_checks <span class="token keyword">if</span> check <span class="token keyword">in</span> answer_code<span class="token punctuation">)</span>
        score <span class="token operator">+=</span> <span class="token builtin">min</span><span class="token punctuation">(</span><span class="token number">15</span><span class="token punctuation">,</span> check_count <span class="token operator">*</span> <span class="token number">4</span><span class="token punctuation">)</span>
        
        <span class="token comment"># 3. 可视化质量（25分）</span>
        visualization_checks <span class="token operator">=</span> <span class="token punctuation">[</span>
            <span class="token string">'plt.figure'</span><span class="token punctuation">,</span>   <span class="token comment"># 创建图形</span>
            <span class="token string">'plt.savefig'</span><span class="token punctuation">,</span>  <span class="token comment"># 保存图片</span>
            <span class="token string">'plt.title'</span><span class="token punctuation">,</span>    <span class="token comment"># 标题</span>
            <span class="token string">'plt.xlabel'</span><span class="token punctuation">,</span>   <span class="token comment"># 坐标轴标签</span>
            <span class="token string">'color'</span><span class="token punctuation">,</span>        <span class="token comment"># 颜色设置</span>
            <span class="token string">'marker'</span><span class="token punctuation">,</span>       <span class="token comment"># 标记点</span>
            <span class="token string">'tight_layout'</span><span class="token punctuation">,</span> <span class="token comment"># 布局优化</span>
        <span class="token punctuation">]</span>
        
        viz_count <span class="token operator">=</span> <span class="token builtin">sum</span><span class="token punctuation">(</span><span class="token number">1</span> <span class="token keyword">for</span> check <span class="token keyword">in</span> visualization_checks <span class="token keyword">if</span> check <span class="token keyword">in</span> answer_code<span class="token punctuation">)</span>
        score <span class="token operator">+=</span> <span class="token builtin">min</span><span class="token punctuation">(</span><span class="token number">25</span><span class="token punctuation">,</span> viz_count <span class="token operator">*</span> <span class="token number">4</span><span class="token punctuation">)</span>
        
        <span class="token comment"># 4. 分析深度（20分）</span>
        analysis_checks <span class="token operator">=</span> <span class="token punctuation">[</span>
            <span class="token string">'seasonal'</span><span class="token punctuation">,</span>     <span class="token comment"># 季节性分析</span>
            <span class="token string">'repurchase'</span><span class="token punctuation">,</span>   <span class="token comment"># 复购率</span>
            <span class="token string">'customer_id'</span><span class="token punctuation">,</span>  <span class="token comment"># 客户分析</span>
            <span class="token string">'category'</span><span class="token punctuation">,</span>     <span class="token comment"># 品类分析</span>
            <span class="token string">'region'</span><span class="token punctuation">,</span>       <span class="token comment"># 区域分析</span>
            <span class="token string">'quarter'</span><span class="token punctuation">,</span>      <span class="token comment"># 季度分析</span>
        <span class="token punctuation">]</span>
        
        analysis_count <span class="token operator">=</span> <span class="token builtin">sum</span><span class="token punctuation">(</span><span class="token number">1</span> <span class="token keyword">for</span> check <span class="token keyword">in</span> analysis_checks <span class="token keyword">if</span> check <span class="token keyword">in</span> answer_code<span class="token punctuation">)</span>
        score <span class="token operator">+=</span> <span class="token builtin">min</span><span class="token punctuation">(</span><span class="token number">20</span><span class="token punctuation">,</span> analysis_count <span class="token operator">*</span> <span class="token number">4</span><span class="token punctuation">)</span>
        
        <span class="token comment"># 5. 业务洞察（10分）</span>
        <span class="token keyword">if</span> <span class="token string">'业务改进建议'</span> <span class="token keyword">in</span> answer_code <span class="token keyword">or</span> <span class="token string">'business recommendation'</span> <span class="token keyword">in</span> answer_code<span class="token punctuation">.</span>lower<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">:</span>
            score <span class="token operator">+=</span> <span class="token number">10</span>
        
        <span class="token comment"># 6. 代码质量（10分）</span>
        quality_checks <span class="token operator">=</span> <span class="token punctuation">[</span>
            <span class="token string">'class '</span><span class="token punctuation">,</span>       <span class="token comment"># 使用类</span>
            <span class="token string">'def __init__'</span><span class="token punctuation">,</span> <span class="token comment"># 初始化方法</span>
            <span class="token string">'try:'</span><span class="token punctuation">,</span>         <span class="token comment"># 错误处理</span>
            <span class="token string">'docstring'</span><span class="token punctuation">,</span>    <span class="token comment"># 文档字符串</span>
        <span class="token punctuation">]</span>
        
        quality_count <span class="token operator">=</span> <span class="token builtin">sum</span><span class="token punctuation">(</span><span class="token number">1</span> <span class="token keyword">for</span> check <span class="token keyword">in</span> quality_checks <span class="token keyword">if</span> check <span class="token keyword">in</span> answer_code<span class="token punctuation">)</span>
        score <span class="token operator">+=</span> <span class="token builtin">min</span><span class="token punctuation">(</span><span class="token number">10</span><span class="token punctuation">,</span> quality_count <span class="token operator">*</span> <span class="token number">3</span><span class="token punctuation">)</span>
        
    <span class="token keyword">except</span> Exception <span class="token keyword">as</span> e<span class="token punctuation">:</span>
        <span class="token keyword">pass</span>
    
    <span class="token keyword">return</span> <span class="token builtin">min</span><span class="token punctuation">(</span><span class="token number">100</span><span class="token punctuation">,</span> score<span class="token punctuation">)</span>

<span class="token comment"># 详细的评分点列表</span>
<span class="token triple-quoted-string string">"""
评分维度：
1. 代码完整性（20分）
   - 包含所有要求的分析方法（每个4分）
   
2. 数据预处理（15分）
   - 正确的日期解析（4分）
   - 销售额计算（4分）
   - 数据聚合（4分）
   - 特征工程（3分）

3. 可视化质量（25分）
   - 图表类型多样（5分）
   - 图表美观度（5分）
   - 标签和标题完整（5分）
   - 颜色搭配合理（5分）
   - 图片保存功能（5分）

4. 分析深度（20分）
   - 趋势分析（4分）
   - 类别分析（4分）
   - 区域分析（4分）
   - 客户行为分析（4分）
   - 季节性分析（4分）

5. 业务洞察（10分）
   - 提供具体建议（10分）

6. 代码质量（10分）
   - 面向对象设计（3分）
   - 错误处理（3分）
   - 文档完整（2分）
   - 代码规范（2分）
"""</span></pre><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _33882ae"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _28d7e84"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg></div><hr><h2><strong><span>示例 3：学术论文笔记整理</span></strong></h2><p class="ds-markdown-paragraph"><strong><span>Query（任务描述）</span></strong><span></span><br><span>我收集了10篇关于深度学习的论文，需要整理成结构化的笔记。请帮我：</span></p><ol start="1"><li><p class="ds-markdown-paragraph"><span>从每篇论文中提取关键信息：</span></p><ul><li><p class="ds-markdown-paragraph"><span>论文标题、作者、发表年份</span></p></li><li><p class="ds-markdown-paragraph"><span>研究问题/目标</span></p></li><li><p class="ds-markdown-paragraph"><span>核心方法/模型架构</span></p></li><li><p class="ds-markdown-paragraph"><span>主要贡献/创新点</span></p></li><li><p class="ds-markdown-paragraph"><span>实验结果（关键指标）</span></p></li><li><p class="ds-markdown-paragraph"><span>局限性和未来工作</span></p></li></ul></li><li><p class="ds-markdown-paragraph"><span>创建对比表格，比较不同论文的方法和效果</span></p></li><li><p class="ds-markdown-paragraph"><span>生成文献综述摘要，总结该领域的研究进展</span></p></li><li><p class="ds-markdown-paragraph"><span>用Markdown格式输出，支持在Obsidian或Notion中导入</span></p></li></ol><p class="ds-markdown-paragraph"><strong><span>Context（上下文文件）</span></strong></p><div class="md-code-block md-code-block-light"><div class="md-code-block-banner-wrap"><div class="md-code-block-banner md-code-block-banner-lite"><div class="_121d384"><div class="d2a24f03"><span class="d813de27">text</span></div><div class="d2a24f03 _246a029"><div class="efa13877"><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon" style="margin-right: 4px;"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.14923 4.02032C7.11191 4.02032 7.87977 4.02017 8.49591 4.07599C9.12122 4.1327 9.65786 4.25188 10.1414 4.53107C10.7201 4.8653 11.2008 5.34591 11.535 5.92462C11.8142 6.40818 11.9333 6.94482 11.9901 7.57013C12.0459 8.18625 12.0457 8.9542 12.0457 9.91681C12.0457 10.8795 12.0459 11.6474 11.9901 12.2635C11.9333 12.8888 11.8142 13.4254 11.535 13.909C11.2008 14.4877 10.7201 14.9683 10.1414 15.3026C9.65786 15.5817 9.12122 15.7009 8.49591 15.7576C7.87977 15.8134 7.1119 15.8133 6.14923 15.8133C5.18661 15.8133 4.41868 15.8134 3.80255 15.7576C3.17724 15.7009 2.6406 15.5817 2.15704 15.3026C1.57834 14.9684 1.09772 14.4877 0.763489 13.909C0.484305 13.4254 0.365123 12.8888 0.308411 12.2635C0.252587 11.6474 0.252747 10.8795 0.252747 9.91681C0.252747 8.95419 0.252603 8.18625 0.308411 7.57013C0.365123 6.94482 0.484305 6.40818 0.763489 5.92462C1.09771 5.3459 1.57833 4.86529 2.15704 4.53107C2.6406 4.25188 3.17724 4.1327 3.80255 4.07599C4.41868 4.02018 5.1866 4.02032 6.14923 4.02032ZM6.14923 5.37775C5.16175 5.37775 4.46628 5.37761 3.9256 5.42657C3.39428 5.47473 3.07853 5.56574 2.83575 5.70587C2.46313 5.92106 2.15348 6.23071 1.93829 6.60333C1.79817 6.84611 1.70715 7.16185 1.659 7.69318C1.61004 8.23385 1.61017 8.92934 1.61017 9.91681C1.61017 10.9043 1.61002 11.5998 1.659 12.1404C1.70715 12.6717 1.79817 12.9875 1.93829 13.2303C2.15349 13.6029 2.46315 13.9126 2.83575 14.1277C3.07853 14.2679 3.39428 14.3589 3.9256 14.407C4.46628 14.456 5.16176 14.4559 6.14923 14.4559C7.13675 14.4559 7.83218 14.456 8.37286 14.407C8.90419 14.3589 9.21993 14.2679 9.46271 14.1277C9.83529 13.9126 10.145 13.6029 10.3602 13.2303C10.5003 12.9875 10.5913 12.6718 10.6395 12.1404C10.6884 11.5998 10.6883 10.9043 10.6883 9.91681C10.6883 8.92935 10.6884 8.23385 10.6395 7.69318C10.5913 7.16185 10.5003 6.84611 10.3602 6.60333C10.145 6.23072 9.8353 5.92107 9.46271 5.70587C9.21993 5.56574 8.90418 5.47473 8.37286 5.42657C7.83218 5.3776 7.13676 5.37775 6.14923 5.37775ZM9.80157 0.367981C10.7637 0.367981 11.5313 0.367886 12.1473 0.423645C12.7725 0.480313 13.3093 0.598765 13.7928 0.877747C14.3716 1.21192 14.852 1.69355 15.1863 2.27228C15.4655 2.75575 15.5857 3.29165 15.6424 3.91681C15.6982 4.53301 15.6971 5.30161 15.6971 6.26447V7.8299C15.6971 8.29265 15.6989 8.58994 15.6649 8.84845C15.4667 10.3525 14.4009 11.5738 12.9832 11.9988V10.5467C13.6973 10.1903 14.2104 9.49662 14.3192 8.67169C14.3387 8.52348 14.3406 8.3358 14.3406 7.8299V6.26447C14.3406 5.27707 14.3398 4.58149 14.2908 4.04083C14.2427 3.50969 14.1526 3.19373 14.0125 2.95099C13.7974 2.5785 13.4875 2.2687 13.1151 2.05353C12.8723 1.91347 12.5563 1.82237 12.0252 1.77423C11.4846 1.72528 10.7888 1.7254 9.80157 1.7254H7.71466C6.75614 1.72559 5.92659 2.27697 5.52325 3.07892H4.07013C4.54215 1.51132 5.99314 0.368192 7.71466 0.367981H9.80157Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">复制</span></span><div class="ds-focus-ring"></div></button><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M15.3695 11.411L15.1234 12.8866C14.8869 14.3042 13.6603 15.3436 12.223 15.3436H3.7767C2.33954 15.3434 1.11276 14.3042 0.876312 12.8866L0.630219 11.411L2.05405 11.1747L2.29916 12.6493C2.41969 13.3713 3.04472 13.9001 3.7767 13.9003H12.223C12.9551 13.9002 13.58 13.3713 13.7005 12.6493L13.9456 11.1747L15.3695 11.411ZM8.72202 8.994C8.77714 8.93934 8.83789 8.88106 8.90268 8.81627L12.4828 5.23424L13.5042 6.25572L9.92221 9.8358C9.63947 10.1185 9.3876 10.3732 9.15854 10.5575C8.91889 10.7503 8.6395 10.9224 8.28647 10.9784C8.09708 11.0083 7.9036 11.0083 7.7142 10.9784C7.36103 10.9224 7.08087 10.7503 6.84116 10.5575C6.61212 10.3732 6.36019 10.1185 6.07748 9.8358L2.49643 6.25572L3.51694 5.23424L7.09702 8.81627C7.16216 8.88142 7.22327 8.94006 7.27866 8.99498V1.3065H8.72202V8.994Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">下载</span></span><div class="ds-focus-ring"></div></button></div></div></div></div></div><pre># papers/
# ├── paper1.pdf (或摘要文本)
# ├── paper2.txt
# └── ...

# paper1摘要示例：
"""
Title: Attention Is All You Need
Authors: Vaswani et al.
Year: 2017
Abstract: We propose a new simple network architecture, the Transformer, 
based solely on attention mechanisms, dispensing with recurrence and 
convolutions entirely. Experiments on two machine translation tasks show 
these models to be superior in quality while being more parallelizable 
and requiring significantly less time to train.

Key Contributions:
1. Introduced Transformer architecture with multi-head self-attention
2. Positional encoding to capture sequence order
3. Achieved state-of-the-art on WMT 2014 English-to-German translation

Results: 28.4 BLEU on WMT 2014 English-to-German, 41.8 BLEU on English-to-French

Limitations: Quadratic complexity with sequence length
"""

# paper2摘要示例：
"""
Title: BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding
Authors: Devlin et al.
Year: 2018
Abstract: We introduce a new language representation model called BERT, 
which stands for Bidirectional Encoder Representations from Transformers. 
BERT is designed to pre-train deep bidirectional representations from 
unlabeled text by jointly conditioning on both left and right context 
in all layers.

Key Contributions:
1. Masked Language Model (MLM) pre-training
2. Next Sentence Prediction (NSP) task
3. Fine-tuning approach for various NLP tasks

Results: GLUE score 80.5% (average), MultiNLI accuracy 86.7%

Limitations: Large computational requirements
"""</pre><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _33882ae"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _28d7e84"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg></div><p class="ds-markdown-paragraph"><strong><span>参考答案（Reference Answer）</span></strong></p><div class="md-code-block md-code-block-light"><div class="md-code-block-banner-wrap"><div class="md-code-block-banner md-code-block-banner-lite"><div class="_121d384"><div class="d2a24f03"><span class="d813de27">markdown</span></div><div class="d2a24f03 _246a029"><div class="efa13877"><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon" style="margin-right: 4px;"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.14923 4.02032C7.11191 4.02032 7.87977 4.02017 8.49591 4.07599C9.12122 4.1327 9.65786 4.25188 10.1414 4.53107C10.7201 4.8653 11.2008 5.34591 11.535 5.92462C11.8142 6.40818 11.9333 6.94482 11.9901 7.57013C12.0459 8.18625 12.0457 8.9542 12.0457 9.91681C12.0457 10.8795 12.0459 11.6474 11.9901 12.2635C11.9333 12.8888 11.8142 13.4254 11.535 13.909C11.2008 14.4877 10.7201 14.9683 10.1414 15.3026C9.65786 15.5817 9.12122 15.7009 8.49591 15.7576C7.87977 15.8134 7.1119 15.8133 6.14923 15.8133C5.18661 15.8133 4.41868 15.8134 3.80255 15.7576C3.17724 15.7009 2.6406 15.5817 2.15704 15.3026C1.57834 14.9684 1.09772 14.4877 0.763489 13.909C0.484305 13.4254 0.365123 12.8888 0.308411 12.2635C0.252587 11.6474 0.252747 10.8795 0.252747 9.91681C0.252747 8.95419 0.252603 8.18625 0.308411 7.57013C0.365123 6.94482 0.484305 6.40818 0.763489 5.92462C1.09771 5.3459 1.57833 4.86529 2.15704 4.53107C2.6406 4.25188 3.17724 4.1327 3.80255 4.07599C4.41868 4.02018 5.1866 4.02032 6.14923 4.02032ZM6.14923 5.37775C5.16175 5.37775 4.46628 5.37761 3.9256 5.42657C3.39428 5.47473 3.07853 5.56574 2.83575 5.70587C2.46313 5.92106 2.15348 6.23071 1.93829 6.60333C1.79817 6.84611 1.70715 7.16185 1.659 7.69318C1.61004 8.23385 1.61017 8.92934 1.61017 9.91681C1.61017 10.9043 1.61002 11.5998 1.659 12.1404C1.70715 12.6717 1.79817 12.9875 1.93829 13.2303C2.15349 13.6029 2.46315 13.9126 2.83575 14.1277C3.07853 14.2679 3.39428 14.3589 3.9256 14.407C4.46628 14.456 5.16176 14.4559 6.14923 14.4559C7.13675 14.4559 7.83218 14.456 8.37286 14.407C8.90419 14.3589 9.21993 14.2679 9.46271 14.1277C9.83529 13.9126 10.145 13.6029 10.3602 13.2303C10.5003 12.9875 10.5913 12.6718 10.6395 12.1404C10.6884 11.5998 10.6883 10.9043 10.6883 9.91681C10.6883 8.92935 10.6884 8.23385 10.6395 7.69318C10.5913 7.16185 10.5003 6.84611 10.3602 6.60333C10.145 6.23072 9.8353 5.92107 9.46271 5.70587C9.21993 5.56574 8.90418 5.47473 8.37286 5.42657C7.83218 5.3776 7.13676 5.37775 6.14923 5.37775ZM9.80157 0.367981C10.7637 0.367981 11.5313 0.367886 12.1473 0.423645C12.7725 0.480313 13.3093 0.598765 13.7928 0.877747C14.3716 1.21192 14.852 1.69355 15.1863 2.27228C15.4655 2.75575 15.5857 3.29165 15.6424 3.91681C15.6982 4.53301 15.6971 5.30161 15.6971 6.26447V7.8299C15.6971 8.29265 15.6989 8.58994 15.6649 8.84845C15.4667 10.3525 14.4009 11.5738 12.9832 11.9988V10.5467C13.6973 10.1903 14.2104 9.49662 14.3192 8.67169C14.3387 8.52348 14.3406 8.3358 14.3406 7.8299V6.26447C14.3406 5.27707 14.3398 4.58149 14.2908 4.04083C14.2427 3.50969 14.1526 3.19373 14.0125 2.95099C13.7974 2.5785 13.4875 2.2687 13.1151 2.05353C12.8723 1.91347 12.5563 1.82237 12.0252 1.77423C11.4846 1.72528 10.7888 1.7254 9.80157 1.7254H7.71466C6.75614 1.72559 5.92659 2.27697 5.52325 3.07892H4.07013C4.54215 1.51132 5.99314 0.368192 7.71466 0.367981H9.80157Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">复制</span></span><div class="ds-focus-ring"></div></button><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M15.3695 11.411L15.1234 12.8866C14.8869 14.3042 13.6603 15.3436 12.223 15.3436H3.7767C2.33954 15.3434 1.11276 14.3042 0.876312 12.8866L0.630219 11.411L2.05405 11.1747L2.29916 12.6493C2.41969 13.3713 3.04472 13.9001 3.7767 13.9003H12.223C12.9551 13.9002 13.58 13.3713 13.7005 12.6493L13.9456 11.1747L15.3695 11.411ZM8.72202 8.994C8.77714 8.93934 8.83789 8.88106 8.90268 8.81627L12.4828 5.23424L13.5042 6.25572L9.92221 9.8358C9.63947 10.1185 9.3876 10.3732 9.15854 10.5575C8.91889 10.7503 8.6395 10.9224 8.28647 10.9784C8.09708 11.0083 7.9036 11.0083 7.7142 10.9784C7.36103 10.9224 7.08087 10.7503 6.84116 10.5575C6.61212 10.3732 6.36019 10.1185 6.07748 9.8358L2.49643 6.25572L3.51694 5.23424L7.09702 8.81627C7.16216 8.88142 7.22327 8.94006 7.27866 8.99498V1.3065H8.72202V8.994Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">下载</span></span><div class="ds-focus-ring"></div></button></div></div></div></div></div><pre><span class="token title important"><span class="token punctuation">#</span> 深度学习论文笔记整理</span>

<span class="token title important"><span class="token punctuation">##</span> 📚 论文概览</span>

<span class="token table"><span class="token table-header-row"><span class="token punctuation">|</span><span class="token table-header important"> 序号 </span><span class="token punctuation">|</span><span class="token table-header important"> 标题 </span><span class="token punctuation">|</span><span class="token table-header important"> 作者 </span><span class="token punctuation">|</span><span class="token table-header important"> 年份 </span><span class="token punctuation">|</span><span class="token table-header important"> 核心方法 </span><span class="token punctuation">|</span><span class="token table-header important"> 关键指标 </span><span class="token punctuation">|</span>
</span><span class="token table-line"><span class="token punctuation">|</span><span class="token punctuation">------</span><span class="token punctuation">|</span><span class="token punctuation">------</span><span class="token punctuation">|</span><span class="token punctuation">------</span><span class="token punctuation">|</span><span class="token punctuation">------</span><span class="token punctuation">|</span><span class="token punctuation">----------</span><span class="token punctuation">|</span><span class="token punctuation">----------</span><span class="token punctuation">|</span>
</span><span class="token table-data-rows"><span class="token punctuation">|</span><span class="token table-data"> 1 </span><span class="token punctuation">|</span><span class="token table-data"> Attention Is All You Need </span><span class="token punctuation">|</span><span class="token table-data"> Vaswani et al. </span><span class="token punctuation">|</span><span class="token table-data"> 2017 </span><span class="token punctuation">|</span><span class="token table-data"> Transformer + Multi-head Attention </span><span class="token punctuation">|</span><span class="token table-data"> BLEU: 28.4 (EN-DE) </span><span class="token punctuation">|</span>
<span class="token punctuation">|</span><span class="token table-data"> 2 </span><span class="token punctuation">|</span><span class="token table-data"> BERT: Pre-training of Deep Bidirectional Transformers </span><span class="token punctuation">|</span><span class="token table-data"> Devlin et al. </span><span class="token punctuation">|</span><span class="token table-data"> 2018 </span><span class="token punctuation">|</span><span class="token table-data"> BERT + MLM + NSP </span><span class="token punctuation">|</span><span class="token table-data"> GLUE: 80.5% </span><span class="token punctuation">|</span>
<span class="token punctuation">|</span><span class="token table-data"> 3 </span><span class="token punctuation">|</span><span class="token table-data"> ... </span><span class="token punctuation">|</span><span class="token table-data"> ... </span><span class="token punctuation">|</span><span class="token table-data"> ... </span><span class="token punctuation">|</span><span class="token table-data"> ... </span><span class="token punctuation">|</span><span class="token table-data"> ... </span><span class="token punctuation">|</span>
</span></span>
<span class="token title important"><span class="token punctuation">##</span> 📄 详细笔记</span>

<span class="token title important"><span class="token punctuation">###</span> 1. Attention Is All You Need (2017)</span>

<span class="token bold"><span class="token punctuation">**</span><span class="token content">基本信息</span><span class="token punctuation">**</span></span>
<span class="token list punctuation">-</span> <span class="token bold"><span class="token punctuation">**</span><span class="token content">作者</span><span class="token punctuation">**</span></span>: Vaswani et al.
<span class="token list punctuation">-</span> <span class="token bold"><span class="token punctuation">**</span><span class="token content">发表会议</span><span class="token punctuation">**</span></span>: NeurIPS 2017
<span class="token list punctuation">-</span> <span class="token bold"><span class="token punctuation">**</span><span class="token content">链接</span><span class="token punctuation">**</span></span>: <span class="token url">[<span class="token content">arXiv:1706.03762</span>](<span class="token url">https://arxiv.org/abs/1706.03762</span>)</span>

<span class="token bold"><span class="token punctuation">**</span><span class="token content">研究问题</span><span class="token punctuation">**</span></span>
如何设计一个完全基于注意力机制的序列转换模型，避免RNN和CNN的局限性？

<span class="token bold"><span class="token punctuation">**</span><span class="token content">核心方法</span><span class="token punctuation">**</span></span>
<span class="token list punctuation">1.</span> <span class="token bold"><span class="token punctuation">**</span><span class="token content">Transformer架构</span><span class="token punctuation">**</span></span>:
   <span class="token list punctuation">-</span> Encoder-Decoder结构
   <span class="token list punctuation">-</span> 完全基于注意力机制
<span class="token list punctuation">2.</span> <span class="token bold"><span class="token punctuation">**</span><span class="token content">Multi-head Self-Attention</span><span class="token punctuation">**</span></span>:
   <span class="token list punctuation">-</span> 并行计算注意力头
   <span class="token list punctuation">-</span> 公式: $\text{Attention}(Q,K,V) = \text{softmax}(\frac{QK^T}{\sqrt{d_k}})V$
<span class="token list punctuation">3.</span> <span class="token bold"><span class="token punctuation">**</span><span class="token content">Positional Encoding</span><span class="token punctuation">**</span></span>:
   <span class="token list punctuation">-</span> 正弦和余弦函数编码位置信息
   <span class="token list punctuation">-</span> $PE_{(pos,2i)} = \sin(pos/10000^{2i/d_{model}})$

<span class="token bold"><span class="token punctuation">**</span><span class="token content">主要贡献</span><span class="token punctuation">**</span></span>
<span class="token list punctuation">-</span> ✅ 首次提出完全基于注意力的序列模型
<span class="token list punctuation">-</span> ✅ 引入Multi-head Attention机制
<span class="token list punctuation">-</span> ✅ 实现高度并行化训练
<span class="token list punctuation">-</span> ✅ 在机器翻译任务上取得SOTA

<span class="token bold"><span class="token punctuation">**</span><span class="token content">实验结果</span><span class="token punctuation">**</span></span>
<span class="token table"><span class="token table-header-row"><span class="token punctuation">|</span><span class="token table-header important"> 任务 </span><span class="token punctuation">|</span><span class="token table-header important"> 指标 </span><span class="token punctuation">|</span><span class="token table-header important"> 结果 </span><span class="token punctuation">|</span>
</span><span class="token table-line"><span class="token punctuation">|</span><span class="token punctuation">------</span><span class="token punctuation">|</span><span class="token punctuation">------</span><span class="token punctuation">|</span><span class="token punctuation">------</span><span class="token punctuation">|</span>
</span><span class="token table-data-rows"><span class="token punctuation">|</span><span class="token table-data"> WMT 2014 EN-DE </span><span class="token punctuation">|</span><span class="token table-data"> BLEU </span><span class="token punctuation">|</span><span class="token table-data"> 28.4 </span><span class="token punctuation">|</span>
<span class="token punctuation">|</span><span class="token table-data"> WMT 2014 EN-FR </span><span class="token punctuation">|</span><span class="token table-data"> BLEU </span><span class="token punctuation">|</span><span class="token table-data"> 41.8 </span><span class="token punctuation">|</span>
<span class="token punctuation">|</span><span class="token table-data"> 训练速度 </span><span class="token punctuation">|</span><span class="token table-data"> 相比之前 </span><span class="token punctuation">|</span><span class="token table-data"> 快8倍 </span><span class="token punctuation">|</span>
</span></span>
<span class="token bold"><span class="token punctuation">**</span><span class="token content">局限性</span><span class="token punctuation">**</span></span>
<span class="token list punctuation">-</span> ❌ 注意力复杂度O(n²)随序列长度增加
<span class="token list punctuation">-</span> ❌ 需要大量训练数据
<span class="token list punctuation">-</span> ❌ 位置编码可能不是最优方案

<span class="token bold"><span class="token punctuation">**</span><span class="token content">未来工作方向</span><span class="token punctuation">**</span></span>
<span class="token list punctuation">-</span> 降低注意力计算复杂度
<span class="token list punctuation">-</span> 探索更好的位置表示方法
<span class="token list punctuation">-</span> 扩展到更长的序列

<span class="token hr punctuation">---</span>

<span class="token title important"><span class="token punctuation">###</span> 2. BERT: Pre-training of Deep Bidirectional Transformers (2018)</span>

<span class="token bold"><span class="token punctuation">**</span><span class="token content">基本信息</span><span class="token punctuation">**</span></span>
<span class="token list punctuation">-</span> <span class="token bold"><span class="token punctuation">**</span><span class="token content">作者</span><span class="token punctuation">**</span></span>: Devlin et al.
<span class="token list punctuation">-</span> <span class="token bold"><span class="token punctuation">**</span><span class="token content">发表会议</span><span class="token punctuation">**</span></span>: NAACL 2019
<span class="token list punctuation">-</span> <span class="token bold"><span class="token punctuation">**</span><span class="token content">链接</span><span class="token punctuation">**</span></span>: <span class="token url">[<span class="token content">arXiv:1810.04805</span>](<span class="token url">https://arxiv.org/abs/1810.04805</span>)</span>

<span class="token bold"><span class="token punctuation">**</span><span class="token content">研究问题</span><span class="token punctuation">**</span></span>
如何预训练深度双向Transformer，用于多种自然语言理解任务？

<span class="token bold"><span class="token punctuation">**</span><span class="token content">核心方法</span><span class="token punctuation">**</span></span>
<span class="token list punctuation">1.</span> <span class="token bold"><span class="token punctuation">**</span><span class="token content">Masked Language Model (MLM)</span><span class="token punctuation">**</span></span>:
   <span class="token list punctuation">-</span> 随机遮蔽15%的token
   <span class="token list punctuation">-</span> 预测被遮蔽的token
<span class="token list punctuation">2.</span> <span class="token bold"><span class="token punctuation">**</span><span class="token content">Next Sentence Prediction (NSP)</span><span class="token punctuation">**</span></span>:
   <span class="token list punctuation">-</span> 判断两个句子是否连续
<span class="token list punctuation">3.</span> <span class="token bold"><span class="token punctuation">**</span><span class="token content">Fine-tuning范式</span><span class="token punctuation">**</span></span>:
   <span class="token list punctuation">-</span> 在预训练模型上添加任务特定层
   <span class="token list punctuation">-</span> 端到端微调

<span class="token bold"><span class="token punctuation">**</span><span class="token content">主要贡献</span><span class="token punctuation">**</span></span>
<span class="token list punctuation">-</span> ✅ 提出双向预训练的概念
<span class="token list punctuation">-</span> ✅ 统一的微调框架
<span class="token list punctuation">-</span> ✅ 在11个NLP任务上取得SOTA
<span class="token list punctuation">-</span> ✅ 开源大规模预训练模型

<span class="token bold"><span class="token punctuation">**</span><span class="token content">实验结果</span><span class="token punctuation">**</span></span>
<span class="token table"><span class="token table-header-row"><span class="token punctuation">|</span><span class="token table-header important"> 任务 </span><span class="token punctuation">|</span><span class="token table-header important"> 指标 </span><span class="token punctuation">|</span><span class="token table-header important"> BERT-Base </span><span class="token punctuation">|</span><span class="token table-header important"> BERT-Large </span><span class="token punctuation">|</span>
</span><span class="token table-line"><span class="token punctuation">|</span><span class="token punctuation">------</span><span class="token punctuation">|</span><span class="token punctuation">------</span><span class="token punctuation">|</span><span class="token punctuation">-----------</span><span class="token punctuation">|</span><span class="token punctuation">------------</span><span class="token punctuation">|</span>
</span><span class="token table-data-rows"><span class="token punctuation">|</span><span class="token table-data"> GLUE (平均) </span><span class="token punctuation">|</span><span class="token table-data"> Accuracy </span><span class="token punctuation">|</span><span class="token table-data"> 80.5% </span><span class="token punctuation">|</span><span class="token table-data"> 82.1% </span><span class="token punctuation">|</span>
<span class="token punctuation">|</span><span class="token table-data"> SQuAD v1.1 </span><span class="token punctuation">|</span><span class="token table-data"> F1 </span><span class="token punctuation">|</span><span class="token table-data"> 88.5 </span><span class="token punctuation">|</span><span class="token table-data"> 90.9 </span><span class="token punctuation">|</span>
<span class="token punctuation">|</span><span class="token table-data"> MultiNLI </span><span class="token punctuation">|</span><span class="token table-data"> Accuracy </span><span class="token punctuation">|</span><span class="token table-data"> 84.6% </span><span class="token punctuation">|</span><span class="token table-data"> 86.7% </span><span class="token punctuation">|</span>
</span></span>
<span class="token bold"><span class="token punctuation">**</span><span class="token content">局限性</span><span class="token punctuation">**</span></span>
<span class="token list punctuation">-</span> ❌ 训练计算成本高
<span class="token list punctuation">-</span> ❌ [MASK] token在微调时不会出现
<span class="token list punctuation">-</span> ❌ 最大序列长度512限制

<span class="token bold"><span class="token punctuation">**</span><span class="token content">未来工作方向</span><span class="token punctuation">**</span></span>
<span class="token list punctuation">-</span> 更高效的预训练方法
<span class="token list punctuation">-</span> 处理更长文档
<span class="token list punctuation">-</span> 多语言扩展

<span class="token hr punctuation">---</span>

<span class="token title important"><span class="token punctuation">##</span> 📊 方法对比</span>

<span class="token table"><span class="token table-header-row"><span class="token punctuation">|</span><span class="token table-header important"> 特性 </span><span class="token punctuation">|</span><span class="token table-header important"> Transformer </span><span class="token punctuation">|</span><span class="token table-header important"> BERT </span><span class="token punctuation">|</span><span class="token table-header important"> GPT </span><span class="token punctuation">|</span>
</span><span class="token table-line"><span class="token punctuation">|</span><span class="token punctuation">------</span><span class="token punctuation">|</span><span class="token punctuation">------------</span><span class="token punctuation">|</span><span class="token punctuation">------</span><span class="token punctuation">|</span><span class="token punctuation">-----</span><span class="token punctuation">|</span>
</span><span class="token table-data-rows"><span class="token punctuation">|</span><span class="token table-data"> <span class="token bold"><span class="token punctuation">**</span><span class="token content">架构</span><span class="token punctuation">**</span></span> </span><span class="token punctuation">|</span><span class="token table-data"> Encoder-Decoder </span><span class="token punctuation">|</span><span class="token table-data"> Encoder-only </span><span class="token punctuation">|</span><span class="token table-data"> Decoder-only </span><span class="token punctuation">|</span>
<span class="token punctuation">|</span><span class="token table-data"> <span class="token bold"><span class="token punctuation">**</span><span class="token content">注意力</span><span class="token punctuation">**</span></span> </span><span class="token punctuation">|</span><span class="token table-data"> Bidirectional </span><span class="token punctuation">|</span><span class="token table-data"> Bidirectional </span><span class="token punctuation">|</span><span class="token table-data"> Unidirectional </span><span class="token punctuation">|</span>
<span class="token punctuation">|</span><span class="token table-data"> <span class="token bold"><span class="token punctuation">**</span><span class="token content">预训练任务</span><span class="token punctuation">**</span></span> </span><span class="token punctuation">|</span><span class="token table-data"> N/A </span><span class="token punctuation">|</span><span class="token table-data"> MLM + NSP </span><span class="token punctuation">|</span><span class="token table-data"> LM </span><span class="token punctuation">|</span>
<span class="token punctuation">|</span><span class="token table-data"> <span class="token bold"><span class="token punctuation">**</span><span class="token content">典型应用</span><span class="token punctuation">**</span></span> </span><span class="token punctuation">|</span><span class="token table-data"> 机器翻译 </span><span class="token punctuation">|</span><span class="token table-data"> 文本分类 </span><span class="token punctuation">|</span><span class="token table-data"> 文本生成 </span><span class="token punctuation">|</span>
<span class="token punctuation">|</span><span class="token table-data"> <span class="token bold"><span class="token punctuation">**</span><span class="token content">复杂度</span><span class="token punctuation">**</span></span> </span><span class="token punctuation">|</span><span class="token table-data"> O(n²) </span><span class="token punctuation">|</span><span class="token table-data"> O(n²) </span><span class="token punctuation">|</span><span class="token table-data"> O(n²) </span><span class="token punctuation">|</span>
<span class="token punctuation">|</span><span class="token table-data"> <span class="token bold"><span class="token punctuation">**</span><span class="token content">参数规模</span><span class="token punctuation">**</span></span> </span><span class="token punctuation">|</span><span class="token table-data"> 65M </span><span class="token punctuation">|</span><span class="token table-data"> 110M/340M </span><span class="token punctuation">|</span><span class="token table-data"> 117M/1.5B </span><span class="token punctuation">|</span>
</span></span>
<span class="token title important"><span class="token punctuation">##</span> 🔬 技术演进脉络</span>

```mermaid
graph LR
    A[RNN/LSTM] --&gt; B[Transformer 2017]
    B --&gt; C[GPT 2018]
    B --&gt; D[BERT 2018]
    D --&gt; E[RoBERTa 2019]
    D --&gt; F[XLNet 2019]
    E --&gt; G[T5 2019]
    F --&gt; G
    C --&gt; H[GPT-2 2019]
    H --&gt; I[GPT-3 2020]</pre><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _33882ae"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _28d7e84"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg></div><h2><span>📈 研究趋势总结</span></h2><h3><span>1. 架构演变</span></h3><ul><li><p class="ds-markdown-paragraph"><strong><span>2017</span></strong><span>: Transformer奠基</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>2018</span></strong><span>: 预训练范式确立（BERT/GPT）</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>2019</span></strong><span>: 模型规模化（GPT-2, XLNet）</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>2020</span></strong><span>: 超大模型时代（GPT-3）</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>2021+</span></strong><span>: 高效化、多模态发展</span></p></li></ul><h3><span>2. 关键技术突破</span></h3><ul><li><p class="ds-markdown-paragraph"><strong><span>注意力机制</span></strong><span>: 从加法注意力到缩放点积注意力</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>预训练策略</span></strong><span>: 从单向LM到双向MLM</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>模型规模</span></strong><span>: 参数从百万级到千亿级</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>应用范围</span></strong><span>: 从NLP扩展到多模态</span></p></li></ul><h3><span>3. 当前挑战</span></h3><ul><li><p class="ds-markdown-paragraph"><strong><span>计算成本</span></strong><span>: 训练大模型能耗高</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>可解释性</span></strong><span>: 黑盒模型决策不透明</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>偏见问题</span></strong><span>: 训练数据中的社会偏见</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>部署难度</span></strong><span>: 大模型推理延迟高</span></p></li></ul><h3><span>4. 未来方向</span></h3><ul><li><p class="ds-markdown-paragraph"><strong><span>绿色AI</span></strong><span>: 开发更高效的架构</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>可解释AI</span></strong><span>: 提高模型透明度</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>负责任AI</span></strong><span>: 减少偏见和有害内容</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>边缘AI</span></strong><span>: 轻量化模型部署</span></p></li></ul><h2><span>🗂️ 知识图谱</span></h2><div class="md-code-block md-code-block-light"><div class="md-code-block-banner-wrap"><div class="md-code-block-banner md-code-block-banner-lite"><div class="_121d384"><div class="d2a24f03"><span class="d813de27">yaml</span></div><div class="d2a24f03 _246a029"><div class="efa13877"><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon" style="margin-right: 4px;"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.14923 4.02032C7.11191 4.02032 7.87977 4.02017 8.49591 4.07599C9.12122 4.1327 9.65786 4.25188 10.1414 4.53107C10.7201 4.8653 11.2008 5.34591 11.535 5.92462C11.8142 6.40818 11.9333 6.94482 11.9901 7.57013C12.0459 8.18625 12.0457 8.9542 12.0457 9.91681C12.0457 10.8795 12.0459 11.6474 11.9901 12.2635C11.9333 12.8888 11.8142 13.4254 11.535 13.909C11.2008 14.4877 10.7201 14.9683 10.1414 15.3026C9.65786 15.5817 9.12122 15.7009 8.49591 15.7576C7.87977 15.8134 7.1119 15.8133 6.14923 15.8133C5.18661 15.8133 4.41868 15.8134 3.80255 15.7576C3.17724 15.7009 2.6406 15.5817 2.15704 15.3026C1.57834 14.9684 1.09772 14.4877 0.763489 13.909C0.484305 13.4254 0.365123 12.8888 0.308411 12.2635C0.252587 11.6474 0.252747 10.8795 0.252747 9.91681C0.252747 8.95419 0.252603 8.18625 0.308411 7.57013C0.365123 6.94482 0.484305 6.40818 0.763489 5.92462C1.09771 5.3459 1.57833 4.86529 2.15704 4.53107C2.6406 4.25188 3.17724 4.1327 3.80255 4.07599C4.41868 4.02018 5.1866 4.02032 6.14923 4.02032ZM6.14923 5.37775C5.16175 5.37775 4.46628 5.37761 3.9256 5.42657C3.39428 5.47473 3.07853 5.56574 2.83575 5.70587C2.46313 5.92106 2.15348 6.23071 1.93829 6.60333C1.79817 6.84611 1.70715 7.16185 1.659 7.69318C1.61004 8.23385 1.61017 8.92934 1.61017 9.91681C1.61017 10.9043 1.61002 11.5998 1.659 12.1404C1.70715 12.6717 1.79817 12.9875 1.93829 13.2303C2.15349 13.6029 2.46315 13.9126 2.83575 14.1277C3.07853 14.2679 3.39428 14.3589 3.9256 14.407C4.46628 14.456 5.16176 14.4559 6.14923 14.4559C7.13675 14.4559 7.83218 14.456 8.37286 14.407C8.90419 14.3589 9.21993 14.2679 9.46271 14.1277C9.83529 13.9126 10.145 13.6029 10.3602 13.2303C10.5003 12.9875 10.5913 12.6718 10.6395 12.1404C10.6884 11.5998 10.6883 10.9043 10.6883 9.91681C10.6883 8.92935 10.6884 8.23385 10.6395 7.69318C10.5913 7.16185 10.5003 6.84611 10.3602 6.60333C10.145 6.23072 9.8353 5.92107 9.46271 5.70587C9.21993 5.56574 8.90418 5.47473 8.37286 5.42657C7.83218 5.3776 7.13676 5.37775 6.14923 5.37775ZM9.80157 0.367981C10.7637 0.367981 11.5313 0.367886 12.1473 0.423645C12.7725 0.480313 13.3093 0.598765 13.7928 0.877747C14.3716 1.21192 14.852 1.69355 15.1863 2.27228C15.4655 2.75575 15.5857 3.29165 15.6424 3.91681C15.6982 4.53301 15.6971 5.30161 15.6971 6.26447V7.8299C15.6971 8.29265 15.6989 8.58994 15.6649 8.84845C15.4667 10.3525 14.4009 11.5738 12.9832 11.9988V10.5467C13.6973 10.1903 14.2104 9.49662 14.3192 8.67169C14.3387 8.52348 14.3406 8.3358 14.3406 7.8299V6.26447C14.3406 5.27707 14.3398 4.58149 14.2908 4.04083C14.2427 3.50969 14.1526 3.19373 14.0125 2.95099C13.7974 2.5785 13.4875 2.2687 13.1151 2.05353C12.8723 1.91347 12.5563 1.82237 12.0252 1.77423C11.4846 1.72528 10.7888 1.7254 9.80157 1.7254H7.71466C6.75614 1.72559 5.92659 2.27697 5.52325 3.07892H4.07013C4.54215 1.51132 5.99314 0.368192 7.71466 0.367981H9.80157Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">复制</span></span><div class="ds-focus-ring"></div></button><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M15.3695 11.411L15.1234 12.8866C14.8869 14.3042 13.6603 15.3436 12.223 15.3436H3.7767C2.33954 15.3434 1.11276 14.3042 0.876312 12.8866L0.630219 11.411L2.05405 11.1747L2.29916 12.6493C2.41969 13.3713 3.04472 13.9001 3.7767 13.9003H12.223C12.9551 13.9002 13.58 13.3713 13.7005 12.6493L13.9456 11.1747L15.3695 11.411ZM8.72202 8.994C8.77714 8.93934 8.83789 8.88106 8.90268 8.81627L12.4828 5.23424L13.5042 6.25572L9.92221 9.8358C9.63947 10.1185 9.3876 10.3732 9.15854 10.5575C8.91889 10.7503 8.6395 10.9224 8.28647 10.9784C8.09708 11.0083 7.9036 11.0083 7.7142 10.9784C7.36103 10.9224 7.08087 10.7503 6.84116 10.5575C6.61212 10.3732 6.36019 10.1185 6.07748 9.8358L2.49643 6.25572L3.51694 5.23424L7.09702 8.81627C7.16216 8.88142 7.22327 8.94006 7.27866 8.99498V1.3065H8.72202V8.994Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">下载</span></span><div class="ds-focus-ring"></div></button></div></div></div></div></div><pre><span class="token key atrule">核心概念</span><span class="token punctuation">:</span>
  <span class="token punctuation">-</span> <span class="token key atrule">注意力机制</span><span class="token punctuation">:</span>
    <span class="token punctuation">-</span> 自注意力
    <span class="token punctuation">-</span> 多头注意力
    <span class="token punctuation">-</span> 交叉注意力
  <span class="token punctuation">-</span> <span class="token key atrule">Transformer组件</span><span class="token punctuation">:</span>
    <span class="token punctuation">-</span> Encoder Block
    <span class="token punctuation">-</span> Decoder Block
    <span class="token punctuation">-</span> Feed<span class="token punctuation">-</span>Forward Network
    <span class="token punctuation">-</span> Layer Normalization
  <span class="token punctuation">-</span> <span class="token key atrule">预训练策略</span><span class="token punctuation">:</span>
    <span class="token punctuation">-</span> 语言模型
    <span class="token punctuation">-</span> 掩码语言模型
    <span class="token punctuation">-</span> 下一句预测
    <span class="token punctuation">-</span> 对比学习
<span class="token key atrule">关键模型</span><span class="token punctuation">:</span>
  <span class="token punctuation">-</span> <span class="token key atrule">基础架构</span><span class="token punctuation">:</span> Transformer
  <span class="token punctuation">-</span> <span class="token key atrule">编码器系列</span><span class="token punctuation">:</span> BERT<span class="token punctuation">,</span> RoBERTa<span class="token punctuation">,</span> ALBERT
  <span class="token punctuation">-</span> <span class="token key atrule">解码器系列</span><span class="token punctuation">:</span> GPT<span class="token punctuation">,</span> GPT<span class="token punctuation">-</span><span class="token number">2</span><span class="token punctuation">,</span> GPT<span class="token punctuation">-</span><span class="token number">3</span>
  <span class="token punctuation">-</span> <span class="token key atrule">编码器-解码器</span><span class="token punctuation">:</span> T5<span class="token punctuation">,</span> BART
<span class="token key atrule">应用领域</span><span class="token punctuation">:</span>
  <span class="token punctuation">-</span> 自然语言理解
  <span class="token punctuation">-</span> 文本生成
  <span class="token punctuation">-</span> 机器翻译
  <span class="token punctuation">-</span> 问答系统
  <span class="token punctuation">-</span> 文本摘要</pre><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _33882ae"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _28d7e84"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg></div><h2><span>📎 参考文献</span></h2><ol start="1"><li><p class="ds-markdown-paragraph"><span>Vaswani, A., et al. "Attention is all you need." NeurIPS 2017.</span></p></li><li><p class="ds-markdown-paragraph"><span>Devlin, J., et al. "BERT: Pre-training of deep bidirectional transformers for language understanding." NAACL 2019.</span></p></li><li><p class="ds-markdown-paragraph"><span>Radford, A., et al. "Improving language understanding by generative pre-training." 2018.</span></p></li><li><p class="ds-markdown-paragraph"><span>Liu, Y., et al. "RoBERTa: A robustly optimized BERT pretraining approach." arXiv 2019.</span></p></li><li><p class="ds-markdown-paragraph"><span>Brown, T., et al. "Language models are few-shot learners." NeurIPS 2020.</span></p></li></ol><hr><p class="ds-markdown-paragraph"><em><span>最后更新: 2024年1月15日</span></em><span></span><br><span></span><em><span>整理者: [您的姓名]</span></em><span></span><br><span></span><em><span>标签: #深度学习 #Transformer #NLP #论文笔记</span></em></p><div class="md-code-block md-code-block-light"><div class="md-code-block-banner-wrap"><div class="md-code-block-banner md-code-block-banner-lite"><div class="_121d384"><div class="d2a24f03"><span class="d813de27">text</span></div><div class="d2a24f03 _246a029"><div class="efa13877"><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon" style="margin-right: 4px;"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.14923 4.02032C7.11191 4.02032 7.87977 4.02017 8.49591 4.07599C9.12122 4.1327 9.65786 4.25188 10.1414 4.53107C10.7201 4.8653 11.2008 5.34591 11.535 5.92462C11.8142 6.40818 11.9333 6.94482 11.9901 7.57013C12.0459 8.18625 12.0457 8.9542 12.0457 9.91681C12.0457 10.8795 12.0459 11.6474 11.9901 12.2635C11.9333 12.8888 11.8142 13.4254 11.535 13.909C11.2008 14.4877 10.7201 14.9683 10.1414 15.3026C9.65786 15.5817 9.12122 15.7009 8.49591 15.7576C7.87977 15.8134 7.1119 15.8133 6.14923 15.8133C5.18661 15.8133 4.41868 15.8134 3.80255 15.7576C3.17724 15.7009 2.6406 15.5817 2.15704 15.3026C1.57834 14.9684 1.09772 14.4877 0.763489 13.909C0.484305 13.4254 0.365123 12.8888 0.308411 12.2635C0.252587 11.6474 0.252747 10.8795 0.252747 9.91681C0.252747 8.95419 0.252603 8.18625 0.308411 7.57013C0.365123 6.94482 0.484305 6.40818 0.763489 5.92462C1.09771 5.3459 1.57833 4.86529 2.15704 4.53107C2.6406 4.25188 3.17724 4.1327 3.80255 4.07599C4.41868 4.02018 5.1866 4.02032 6.14923 4.02032ZM6.14923 5.37775C5.16175 5.37775 4.46628 5.37761 3.9256 5.42657C3.39428 5.47473 3.07853 5.56574 2.83575 5.70587C2.46313 5.92106 2.15348 6.23071 1.93829 6.60333C1.79817 6.84611 1.70715 7.16185 1.659 7.69318C1.61004 8.23385 1.61017 8.92934 1.61017 9.91681C1.61017 10.9043 1.61002 11.5998 1.659 12.1404C1.70715 12.6717 1.79817 12.9875 1.93829 13.2303C2.15349 13.6029 2.46315 13.9126 2.83575 14.1277C3.07853 14.2679 3.39428 14.3589 3.9256 14.407C4.46628 14.456 5.16176 14.4559 6.14923 14.4559C7.13675 14.4559 7.83218 14.456 8.37286 14.407C8.90419 14.3589 9.21993 14.2679 9.46271 14.1277C9.83529 13.9126 10.145 13.6029 10.3602 13.2303C10.5003 12.9875 10.5913 12.6718 10.6395 12.1404C10.6884 11.5998 10.6883 10.9043 10.6883 9.91681C10.6883 8.92935 10.6884 8.23385 10.6395 7.69318C10.5913 7.16185 10.5003 6.84611 10.3602 6.60333C10.145 6.23072 9.8353 5.92107 9.46271 5.70587C9.21993 5.56574 8.90418 5.47473 8.37286 5.42657C7.83218 5.3776 7.13676 5.37775 6.14923 5.37775ZM9.80157 0.367981C10.7637 0.367981 11.5313 0.367886 12.1473 0.423645C12.7725 0.480313 13.3093 0.598765 13.7928 0.877747C14.3716 1.21192 14.852 1.69355 15.1863 2.27228C15.4655 2.75575 15.5857 3.29165 15.6424 3.91681C15.6982 4.53301 15.6971 5.30161 15.6971 6.26447V7.8299C15.6971 8.29265 15.6989 8.58994 15.6649 8.84845C15.4667 10.3525 14.4009 11.5738 12.9832 11.9988V10.5467C13.6973 10.1903 14.2104 9.49662 14.3192 8.67169C14.3387 8.52348 14.3406 8.3358 14.3406 7.8299V6.26447C14.3406 5.27707 14.3398 4.58149 14.2908 4.04083C14.2427 3.50969 14.1526 3.19373 14.0125 2.95099C13.7974 2.5785 13.4875 2.2687 13.1151 2.05353C12.8723 1.91347 12.5563 1.82237 12.0252 1.77423C11.4846 1.72528 10.7888 1.7254 9.80157 1.7254H7.71466C6.75614 1.72559 5.92659 2.27697 5.52325 3.07892H4.07013C4.54215 1.51132 5.99314 0.368192 7.71466 0.367981H9.80157Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">复制</span></span><div class="ds-focus-ring"></div></button><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M15.3695 11.411L15.1234 12.8866C14.8869 14.3042 13.6603 15.3436 12.223 15.3436H3.7767C2.33954 15.3434 1.11276 14.3042 0.876312 12.8866L0.630219 11.411L2.05405 11.1747L2.29916 12.6493C2.41969 13.3713 3.04472 13.9001 3.7767 13.9003H12.223C12.9551 13.9002 13.58 13.3713 13.7005 12.6493L13.9456 11.1747L15.3695 11.411ZM8.72202 8.994C8.77714 8.93934 8.83789 8.88106 8.90268 8.81627L12.4828 5.23424L13.5042 6.25572L9.92221 9.8358C9.63947 10.1185 9.3876 10.3732 9.15854 10.5575C8.91889 10.7503 8.6395 10.9224 8.28647 10.9784C8.09708 11.0083 7.9036 11.0083 7.7142 10.9784C7.36103 10.9224 7.08087 10.7503 6.84116 10.5575C6.61212 10.3732 6.36019 10.1185 6.07748 9.8358L2.49643 6.25572L3.51694 5.23424L7.09702 8.81627C7.16216 8.88142 7.22327 8.94006 7.27866 8.99498V1.3065H8.72202V8.994Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">下载</span></span><div class="ds-focus-ring"></div></button></div></div></div></div></div><pre>
**Rubric（评分标准）**
```python
def evaluate_literature_notes(answer_text: str) -&gt; int:
    """
    评分函数（满分100）
    """
    score = 0
    
    # 1. 结构完整性（30分）
    sections = [
        '论文概览',
        '详细笔记',
        '方法对比',
        '研究趋势总结',
        '参考文献'
    ]
    
    section_count = sum(1 for section in sections if section in answer_text)
    score += min(30, section_count * 6)
    
    # 2. 信息提取完整性（25分）
    required_info = [
        '作者', '年份', '研究问题', '核心方法',
        '主要贡献', '实验结果', '局限性'
    ]
    
    # 检查是否在详细笔记部分包含这些信息
    info_count = sum(1 for info in required_info if info in answer_text)
    score += min(25, info_count * 4)
    
    # 3. 格式规范性（20分）
    format_checks = [
        '|',  # 表格
        '**', # 粗体
        '- ', # 列表
        '# ', # 标题
        '```', # 代码块
    ]
    
    format_count = sum(1 for check in format_checks if check in answer_text)
    score += min(20, format_count * 4)
    
    # 4. 分析深度（15分）
    analysis_indicators = [
        '对比',
        '总结',
        '趋势',
        '演进',
        '挑战',
        '未来方向'
    ]
    
    analysis_count = sum(1 for indicator in analysis_indicators if indicator in answer_text)
    score += min(15, analysis_count * 3)
    
    # 5. 可读性和组织（10分）
    if len(answer_text.split('\n')) &gt; 50:  # 内容足够详细
        score += 5
    
    # 检查是否有清晰的层次结构
    heading_levels = sum(1 for line in answer_text.split('\n') if line.startswith('#'))
    if heading_levels &gt;= 10:
        score += 5
    
    return min(100, score)

# 详细评分标准
"""
1. 结构完整性（30分）
   - 论文概览表格（6分）
   - 详细笔记（每篇论文）（6分）
   - 方法对比表格（6分）
   - 研究趋势总结（6分）
   - 参考文献列表（6分）

2. 信息提取完整性（25分）
   - 提取了所有要求的论文信息（每项4分，最多25分）
   - 信息准确无误

3. 格式规范性（20分）
   - 使用Markdown格式（5分）
   - 包含表格（5分）
   - 层次结构清晰（5分）
   - 代码块或图表（5分）

4. 分析深度（15分）
   - 对比分析（5分）
   - 趋势总结（5分）
   - 未来展望（5分）

5. 可读性（10分）
   - 内容详实（5分）
   - 结构清晰（5分）

额外加分项：
- 包含知识图谱或流程图（+5分）
- 包含引用链接（+5分）
- 包含标签分类（+5分）
"""</pre><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _33882ae"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _28d7e84"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg></div><p class="ds-markdown-paragraph"><span>由于篇幅限制，我已经提供了3个完整示例。如果您需要完整的10个示例，我可以继续提供剩余的7个。每个示例都遵循相同的格式：Query、Context、参考答案、Rubric。</span></p><p class="ds-markdown-paragraph"><strong><span>其他7个示例的主题包括：</span></strong><span></span><br><span>4. 旅行行程规划与预算</span><br><span>5. 技术面试准备指南</span><br><span>6. 健身计划制定</span><br><span>7. 个人财务分析</span><br><span>8. 博客文章写作</span><br><span>9. API集成开发</span><br><span>10. 学习计划制定</span></p><p class="ds-markdown-paragraph"><span>您希望我继续提供剩余的示例吗？</span></p>

