### 用户

Why is upsampling required in FCN-based segmentation models?

答案选项组

To restore spatial resolution of the output

To increase model depth

To reduce computation

To normalize feature distributions
 
标记问题：问题 2
问题 21 分
Which of the following is a learnable upsampling method?

答案选项组

Transposed convolution

Nearest-neighbor interpolation

Bilinear interpolation

Max pooling
 
标记问题：问题 3
问题 31 分
Dice loss is particularly useful because it

答案选项组

Measures overlap between prediction and ground truth

Speeds up training

Penalizes incorrect boundaries more heavily

Requires no ground-truth labels
 
标记问题：问题 4
问题 41 分
Encoder–decoder architectures (e.g., U-Net) help segmentation mainly by

答案选项组

Gradually restoring spatial resolution

Using larger batch sizes

Eliminating pooling layers

Removing skip connections
 
标记问题：问题 5
问题 51 分
Dense CRFs differ from standard CRFs because they

答案选项组

Model long-range pixel interactions using dense pairwise potentials

Only model pairwise relationships between neighboring pixels

Ignore color and appearance information in pairwise terms

Eliminate the need for inference during prediction

---

### DeepSeek AI

<p>思考：</p><blockquote><p class="ds-markdown-paragraph"><span>嗯，用户正在做一组关于图像分割模型的选择题，看起来像是考试或作业题。这些题目涉及FCN、上采样方法、损失函数、网络结构和CRF等计算机视觉概念。用户可能是在复习相关知识，或者正在完成某个课程的作业。</span></p><p class="ds-markdown-paragraph"><span>第一题问为什么FCN分割模型需要上采样。FCN会通过池化降低分辨率，最终需要恢复到原始图像尺寸才能进行像素级预测，所以应该是为了恢复空间分辨率。其他选项如增加深度、减少计算或归一化特征都不符合上采样的主要目的。</span></p><p class="ds-markdown-paragraph"><span>第二题问哪种上采样方法是可学习的。最近邻插值和双线性插值都是固定算法，最大池化是下采样。转置卷积有可学习的参数，可以通过训练优化，所以应该是正确答案。</span></p><p class="ds-markdown-paragraph"><span>第三题问Dice损失函数的优势。Dice系数衡量预测和真实标签的重叠程度，特别适合处理类别不平衡的分割任务。其他选项如加速训练、惩罚边界错误或无标签需求都不准确。</span></p><p class="ds-markdown-paragraph"><span>第四题问编码器-解码器结构如U-Net的主要优势。这类结构通过解码器逐步恢复空间分辨率，同时使用跳跃连接融合浅层特征。其他选项如更大批次、消除池化或移除跳跃连接都不对。</span></p><p class="ds-markdown-paragraph"><span>第五题问密集CRF与标准CRF的区别。传统CRF通常只考虑相邻像素关系，而密集CRF使用密集连接建模长距离像素交互。其他选项都不准确描述了密集CRF的特点。</span></p><p class="ds-markdown-paragraph"><span>这些问题都比较基础，但覆盖了分割模型的关键概念。用户如果理解这些原理，应该能轻松作答。从问题顺序看，可能是按照教学逻辑排列的，从基础结构到具体组件再到后处理。</span></p></blockquote><br/><p class="ds-markdown-paragraph"><strong><span>问题1：</span></strong><span> To restore spatial resolution of the output</span><br><strong><span>问题2：</span></strong><span> Transposed convolution</span><br><strong><span>问题3：</span></strong><span> Measures overlap between prediction and ground truth</span><br><strong><span>问题4：</span></strong><span> Gradually restoring spatial resolution</span><br><strong><span>问题5：</span></strong><span> Model long-range pixel interactions using dense pairwise potentials</span></p>

