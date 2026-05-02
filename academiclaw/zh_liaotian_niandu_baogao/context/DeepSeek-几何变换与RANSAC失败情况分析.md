### 用户

The key difference between an affine and a projective transformation (homography) is that:

答案选项组

Projective transforms allow parallel lines to meet

Affine transforms cannot represent rotation

Affine transforms allow perspective distortion

Projective transforms preserve parallelism
 
标记问题：问题 2
问题 21 分
RANSAC may fail in which of the following situations?

答案选项组

When the inlier ratio is extremely low

When the noise is Gaussian

When data points are normalized

When the model is affine
 
标记问题：问题 3
问题 31 分
Estimating an affine transformation requires at least ____ matching pairs？

 
标记问题：问题 4
问题 41 分
Estimating a homography matrix requires at least ____  matching pairs?

 
标记问题：问题 5
问题 51 分
In panorama assembly, “drift” refers to？

答案选项组

Accumulated alignment error over multiple images

Memory overflow during stitching

Excessive brightness blending

Camera lens distortion

---

### DeepSeek AI

<p>思考：</p><blockquote><p class="ds-markdown-paragraph"><span>首先，问题是关于计算机视觉和图像处理中的概念，特别是仿射变换和投影变换（单应性）的区别，以及RANSAC、变换估计和全景组装中的问题。</span></p><p class="ds-markdown-paragraph"><span>问题1：仿射变换和投影变换的关键区别是什么？</span></p><p class="ds-markdown-paragraph"><span>选项：</span></p><ul><li><p class="ds-markdown-paragraph"><span>投影变换允许平行线相交</span></p></li><li><p class="ds-markdown-paragraph"><span>仿射变换不能表示旋转</span></p></li><li><p class="ds-markdown-paragraph"><span>仿射变换允许透视失真</span></p></li><li><p class="ds-markdown-paragraph"><span>投影变换保持平行性</span></p></li></ul><p class="ds-markdown-paragraph"><span>我知道仿射变换包括平移、旋转、缩放和剪切，它们保持平行线平行。投影变换（单应性）包括透视变换，允许平行线在无限远处相交，就像在透视图中一样。所以，关键区别是投影变换允许平行线相交，而仿射变换保持平行性。</span></p><p class="ds-markdown-paragraph"><span>因此，正确答案应该是“Projective transforms allow parallel lines to meet”。</span></p><p class="ds-markdown-paragraph"><span>问题2：RANSAC在哪种情况下可能失败？</span></p><p class="ds-markdown-paragraph"><span>选项：</span></p><ul><li><p class="ds-markdown-paragraph"><span>当内点比例极低时</span></p></li><li><p class="ds-markdown-paragraph"><span>当噪声是高斯分布时</span></p></li><li><p class="ds-markdown-paragraph"><span>当数据点被归一化时</span></p></li><li><p class="ds-markdown-paragraph"><span>当模型是仿射时</span></p></li></ul><p class="ds-markdown-paragraph"><span>RANSAC（Random Sample Consensus）用于从包含异常值的数据中估计模型。它依赖于内点（inliers）的比例。如果内点比例极低，RANSAC可能无法找到足够的内部点来拟合模型，因此可能失败。高斯噪声通常不影响RANSAC，因为RANSAC设计用于处理异常值，而高斯噪声是随机噪声，不一定是异常值。数据点归一化通常有助于数值稳定性，但不会导致RANSAC失败。仿射模型本身不会导致RANSAC失败。</span></p><p class="ds-markdown-paragraph"><span>所以，正确答案应该是“When the inlier ratio is extremely low”。</span></p><p class="ds-markdown-paragraph"><span>问题3：估计仿射变换至少需要多少匹配对？</span></p><p class="ds-markdown-paragraph"><span>仿射变换有6个自由度（平移2个，旋转1个，缩放2个，剪切1个？）。实际上，仿射变换在二维中可以用一个2x3矩阵表示，有6个参数。每个匹配点对提供两个方程（x和y坐标）。因此，至少需要3个点对来求解6个方程。</span></p><p class="ds-markdown-paragraph"><span>所以，答案应该是3。</span></p><p class="ds-markdown-paragraph"><span>问题4：估计单应性矩阵至少需要多少匹配对？</span></p><p class="ds-markdown-paragraph"><span>单应性矩阵是一个3x3矩阵，但有8个自由度（因为尺度不变）。每个点对提供两个方程。因此，至少需要4个点对来求解8个方程。</span></p><p class="ds-markdown-paragraph"><span>所以，答案应该是4。</span></p><p class="ds-markdown-paragraph"><span>问题5：在全景组装中，“drift”指的是什么？</span></p><p class="ds-markdown-paragraph"><span>选项：</span></p><ul><li><p class="ds-markdown-paragraph"><span>累积的对齐误差超过多个图像</span></p></li><li><p class="ds-markdown-paragraph"><span>内存溢出 during stitching</span></p></li><li><p class="ds-markdown-paragraph"><span>过度亮度混合</span></p></li><li><p class="ds-markdown-paragraph"><span>相机镜头失真</span></p></li></ul><p class="ds-markdown-paragraph"><span>在全景拼接中，当将多个图像拼接在一起时，每个图像与下一个对齐，但小误差会累积，导致整体图像出现扭曲或偏移，这称为“drift”。所以，它指的是累积的对齐误差。</span></p><p class="ds-markdown-paragraph"><span>因此，正确答案应该是“Accumulated alignment error over multiple images”。</span></p><p class="ds-markdown-paragraph"><span>现在，我需要以JSON格式输出答案。问题是用中文写的，但答案应该基于内容。</span></p><p class="ds-markdown-paragraph"><span>对于问题3和4，我需要提供数字答案。</span></p><p class="ds-markdown-paragraph"><span>最终输出应该是一个JSON对象，包含每个问题的答案。</span></p></blockquote><br/><p class="ds-markdown-paragraph"><span>{</span><br><span>"question1": "Projective transforms allow parallel lines to meet",</span><br><span>"question2": "When the inlier ratio is extremely low",</span><br><span>"question3": 3,</span><br><span>"question4": 4,</span><br><span>"question5": "Accumulated alignment error over multiple images"</span><br><span>}</span></p>

