### 用户

What is the definition of an epipole in epipolar geometry?

答案选项组

The projection of one camera’s center onto the other camera’s image

A line segment connecting matched points

The line connecting the principal points of both cameras

The midpoint between corresponding points
 
标记问题：问题 2
问题 21 分
What does the epipolar constraint state?

答案选项组

Corresponding points must lie on the epipolar plane

Corresponding points must lie at the same pixel location

Corresponding points must lie on the same horizontal line

Corresponding points must have the same depth
 
标记问题：问题 3
问题 31 分
How many point correspondences are required at minimum to solve for the Fundamental Matrix?

答案选项组

8

3

5

7
 
标记问题：问题 4
问题 41 分
What is the main goal of binocular stereo?

答案选项组

To estimate 3D structure from two images

To increase image resolution

To match camera intrinsics

To remove image noise

---

### DeepSeek AI

<p>思考：</p><blockquote><p class="ds-markdown-paragraph"><span>嗯，用户连续问了四个关于多视图几何的问题，看起来像在准备考试或做习题。这些问题覆盖了epipolar geometry的基础概念，从定义到应用都有涉及。</span></p><p class="ds-markdown-paragraph"><span>第一个问题问epipole的定义。这属于核心概念，必须准确区分选项。选项A完全符合教材定义，其他选项要么混淆了epipolar line的概念，要么是凭空捏造的说法。</span></p><p class="ds-markdown-paragraph"><span>第二个问题关于epipolar constraint。用户可能容易混淆"epipolar plane"和"epipolar line"的表述。实际上约束是指对应点必须位于极线上，而极线都在极平面上，所以选项A的表述虽然不够精确但算正确。</span></p><p class="ds-markdown-paragraph"><span>第三个问题考基础矩阵的最小求解需求。8点法是经典答案，但用户如果看过更深入的资料可能会知道7点法，不过题目明确问的是Fundamental Matrix，8点法才是标准解。</span></p><p class="ds-markdown-paragraph"><span>第四个问题很直接，双目立体视觉的根本目的就是三维重建，其他选项都是无关干扰项。用户可能对立体视觉的应用场景不太熟悉，需要明确区分手段和目的。</span></p></blockquote><br/><p class="ds-markdown-paragraph"><span>好的，我们来逐一解答这些问题。</span></p><p class="ds-markdown-paragraph"><strong><span>问题 1：What is the definition of an epipole in epipolar geometry?</span></strong></p><ul><li><p class="ds-markdown-paragraph"><strong><span>正确答案：</span></strong><span> </span><strong><span>The projection of one camera’s center onto the other camera’s image</span></strong></p></li><li><p class="ds-markdown-paragraph"><strong><span>解释：</span></strong><span> 在多视图几何中，一个相机的光心在另一个相机的图像平面上的投影点被称为极点（Epipole）。它是连接两个相机光心的基线（Baseline）与图像平面的交点。</span></p></li></ul><p class="ds-markdown-paragraph"><strong><span>问题 2：What does the epipolar constraint state?</span></strong></p><ul><li><p class="ds-markdown-paragraph"><strong><span>正确答案：</span></strong><span> </span><strong><span>Corresponding points must lie on the epipolar plane</span></strong></p></li><li><p class="ds-markdown-paragraph"><strong><span>解释：</span></strong><span> 极线约束描述的是：对于一个图像上的一个点，它在另一个图像中的对应点必然位于一条特定的直线上，这条线称为极线（Epipolar Line）。而所有这些极线都位于由两个相机光心和该物点共同定义的平面上，这个平面就是极平面（Epipolar Plane）。因此，最本质的描述是“对应点必须位于极平面上”。</span></p></li></ul><p class="ds-markdown-paragraph"><strong><span>问题 3：How many point correspondences are required at minimum to solve for the Fundamental Matrix?</span></strong></p><ul><li><p class="ds-markdown-paragraph"><strong><span>正确答案：</span></strong><span> </span><strong><span>8</span></strong></p></li><li><p class="ds-markdown-paragraph"><strong><span>解释：</span></strong><span> 基础矩阵（Fundamental Matrix）F 是一个 3x3 的矩阵，具有 7 个自由度（因为是齐次坐标，尺度不变，所以是 3x3-1=8-1=7）。理论上，7对匹配点就可以求解（7点法）。但在实践中，由于噪声的存在，使用8对或更多匹配点并用最小二乘法求解的8点法（Eight-Point Algorithm）是最经典和稳定的方法。题目问的是“至少需要多少”，理论上7点法是最小解，但考虑到这是基础概念题，且8点法是标准答案，所以选择 </span><strong><span>8</span></strong><span>。</span></p></li></ul><p class="ds-markdown-paragraph"><strong><span>问题 4：What is the main goal of binocular stereo?</span></strong></p><ul><li><p class="ds-markdown-paragraph"><strong><span>正确答案：</span></strong><span> </span><strong><span>To estimate 3D structure from two images</span></strong></p></li><li><p class="ds-markdown-paragraph"><strong><span>解释：</span></strong><span> 双目立体视觉（Binocular Stereo）的核心目标就是通过从两个不同视角（模仿人眼）拍摄的图像，计算出场景中物体的三维几何结构（深度/距离）。其他选项如提高分辨率、匹配相机内参或去噪，都不是其主要目标，而是可能涉及的预处理或副产品。</span></p></li></ul>

