### 用户

本-(2025-2026-1)-AI3619-01-计算机视觉
Quiz-10
Quiz-10
已开始： 12月8日 12:00
测验说明
注意：这是计时测验。您可以在参加测验时随时查看您的剩余时间，方法是按组合键 SHIFT、ALT 和 T... 重申一遍：SHIFT、ALT 和 T...
 
标记问题：问题 1
问题 11 分
In the Bag-of-Words image classification pipeline, what happens immediately after extracting SIFT/HOG descriptors?

答案选项组

Codebook clustering

Histogram equalization

Classifier learning

Bag-level pooling
 
标记问题：问题 2
问题 21 分
What is the main purpose of vector quantization in the Bag-of-Words model?

答案选项组

Assign each descriptor to the nearest codeword

Detect interest points

Train a classifier via SVM

Remove redundancies from image patches
 
标记问题：问题 3
问题 31 分
A visual vocabulary that is too large may lead to which problem?

答案选项组

Quantization artifacts and overfitting

Poor invariance to scale

Missing representative patches

Inability to cluster descriptors
 
标记问题：问题 4
问题 41 分
In a Bag-of-Features model, the final image representation is typically:

答案选项组

A histogram of visual word occurrences

A sequence of raw pixel values

A set of bounding boxes

A binary segmentation mask
未保存 
问题
尚未回答问题 1
尚未回答问题 2
尚未回答问题 3
尚未回答问题 4
运行时间：
尝试截止： 12月8日 23:59
59 分钟, 40 秒

---

### DeepSeek AI

<p>思考：</p><blockquote><p class="ds-markdown-paragraph"><span>嗯，这是一个关于计算机视觉中Bag-of-Words模型的测验，用户正在回答四道选择题。看起来用户可能是在参加一个限时测验，需要快速准确地完成这些问题。</span></p><p class="ds-markdown-paragraph"><span>问题都是关于Bag-of-Words图像分类流程的基本概念。第一个问题询问在提取SIFT/HOG描述符之后立即进行的步骤，这应该是创建视觉词典的步骤。第二个问题关于矢量量化的主要目的，这是为了将描述符分配到最近的视觉单词。第三个问题关于视觉词典过大的问题，这会导致量化伪影和过拟合。第四个问题关于Bag-of-Features模型的最终表示形式，这通常是一个视觉词出现频率的直方图。</span></p><p class="ds-markdown-paragraph"><span>这些问题都不难，都是Bag-of-Words模型的基本知识点。我可以直接给出正确答案并简要解释每个选项为什么对或错。对于这种测验类问题，直接明确的答案对用户最有帮助。</span></p><p class="ds-markdown-paragraph"><span>用户可能正在参加在线测验，需要快速确认答案。我会保持回答简洁明了，直接指出每个问题的正确答案，避免冗长的解释，但提供足够的理由说明为什么其他选项不正确。</span></p></blockquote><br/><p class="ds-markdown-paragraph"><strong><span>答案及解析</span></strong></p><p class="ds-markdown-paragraph"><strong><span>问题1</span></strong><br><span>在 Bag-of-Words 图像分类流程中，提取 SIFT/HOG 描述符后，下一步通常是 </span><strong><span>Codebook clustering</span></strong><span>（构建视觉词典）。</span><br><span>其他选项：</span></p><ul><li><p class="ds-markdown-paragraph"><span>Histogram equalization：直方图均衡化，通常在图像预处理中使用，不是 BoW 流程中的步骤。</span></p></li><li><p class="ds-markdown-paragraph"><span>Classifier learning：分类器学习，是在得到图像表示（如词袋直方图）之后进行的。</span></p></li><li><p class="ds-markdown-paragraph"><span>Bag-level pooling：池化操作在特征提取或表示聚合时可能用到，但 BoW 中一般在生成词典后进行特征量化与直方图生成。</span></p></li></ul><p class="ds-markdown-paragraph"><strong><span>正确答案：Codebook clustering</span></strong></p><hr><p class="ds-markdown-paragraph"><strong><span>问题2</span></strong><br><span>在 Bag-of-Words 模型中，矢量量化的主要目的是 </span><strong><span>Assign each descriptor to the nearest codeword</span></strong><span>，即把每个局部描述符映射到视觉词典中最近的视觉词（codeword）。</span><br><span>其他选项：</span></p><ul><li><p class="ds-markdown-paragraph"><span>Detect interest points：兴趣点检测是特征提取阶段的任务，在量化之前。</span></p></li><li><p class="ds-markdown-paragraph"><span>Train a classifier via SVM：分类器训练是在量化并生成图像表示之后进行的。</span></p></li><li><p class="ds-markdown-paragraph"><span>Remove redundancies from image patches：虽然量化可减少冗余，但不是其主要目的，主要目的是建立离散的视觉词表示。</span></p></li></ul><p class="ds-markdown-paragraph"><strong><span>正确答案：Assign each descriptor to the nearest codeword</span></strong></p><hr><p class="ds-markdown-paragraph"><strong><span>问题3</span></strong><br><span>视觉词典过大容易导致 </span><strong><span>Quantization artifacts and overfitting</span></strong><span>（量化伪影与过拟合），因为词典太大会使得直方图稀疏，并增加模型复杂度。</span><br><span>其他选项：</span></p><ul><li><p class="ds-markdown-paragraph"><span>Poor invariance to scale：尺度不变性主要与特征提取有关，不受词典大小直接影响。</span></p></li><li><p class="ds-markdown-paragraph"><span>Missing representative patches：词典过小才可能导致代表性不足。</span></p></li><li><p class="ds-markdown-paragraph"><span>Inability to cluster descriptors：过大的词典不会导致无法聚类，但可能增加计算负担。</span></p></li></ul><p class="ds-markdown-paragraph"><strong><span>正确答案：Quantization artifacts and overfitting</span></strong></p><hr><p class="ds-markdown-paragraph"><strong><span>问题4</span></strong><br><span>在 Bag-of-Features 模型中，最终图像表示通常是 </span><strong><span>A histogram of visual word occurrences</span></strong><span>（视觉词出现频率的直方图）。</span><br><span>其他选项：</span></p><ul><li><p class="ds-markdown-paragraph"><span>A sequence of raw pixel values：原始像素序列不属于 BoW 表示。</span></p></li><li><p class="ds-markdown-paragraph"><span>A set of bounding boxes：边界框集合常用于目标检测。</span></p></li><li><p class="ds-markdown-paragraph"><span>A binary segmentation mask：二值分割掩码用于图像分割任务。</span></p></li></ul><p class="ds-markdown-paragraph"><strong><span>正确答案：A histogram of visual word occurrences</span></strong></p><hr><p class="ds-markdown-paragraph"><span>希望这些解析能帮助你更好地理解 Bag-of-Words 模型的关键步骤。</span></p>

