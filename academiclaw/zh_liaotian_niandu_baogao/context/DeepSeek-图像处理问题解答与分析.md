### 用户

In blob detection, the characteristic scale is directly proportional to

答案选项组

The size of blob

The intensity difference of blob

The edge sharpness of blob
 
标记问题：问题 2
问题 21 分
SlFT descriptor is robust to scale and in-plane rotation.

答案选项组

True

False
 
标记问题：问题 3
问题 31 分
Affine transformations map parallel lines to parallel lines.

答案选项组

True

False
 
标记问题：问题 4
问题 41 分
What is the degree of freedom of similarity transformation?

 
标记问题：问题 5
问题 51 分
Select all (2D) rotation matrices.

A.

B.

C.

D.

答案选项组

A

B

C

D

---

### DeepSeek AI

<p>思考：</p><blockquote><p class="ds-markdown-paragraph"><span>首先，问题是关于计算机视觉中的 blob 检测和特征描述符。让我们逐个回答。</span></p><p class="ds-markdown-paragraph"><span>问题 1: In blob detection, the characteristic scale is directly proportional to</span></p><p class="ds-markdown-paragraph"><span>选项是：</span></p><ul><li><p class="ds-markdown-paragraph"><span>The size of blob</span></p></li><li><p class="ds-markdown-paragraph"><span>The intensity difference of blob</span></p></li><li><p class="ds-markdown-paragraph"><span>The edge sharpness of blob</span></p></li></ul><p class="ds-markdown-paragraph"><span>在 blob 检测中，特征尺度（characteristic scale）通常与 blob 的大小相关。特征尺度是指在哪个尺度上 blob 被检测到，它对应于 blob 的尺寸。例如，在 Laplacian of Gaussian (LoG) 或 Difference of Gaussians (DoG)  blob 检测中，特征尺度与 blob 的半径或直径成正比。所以，答案应该是 "The size of blob"。</span></p><p class="ds-markdown-paragraph"><span>问题 2: SIFT descriptor is robust to scale and in-plane rotation.</span></p><p class="ds-markdown-paragraph"><span>SIFT 描述符被设计为对尺度和平面内旋转具有鲁棒性。SIFT 通过检测关键点并计算方向来实现旋转不变性，并通过尺度空间实现尺度不变性。所以，这个说法是正确的。答案应该是 "True"。</span></p><p class="ds-markdown-paragraph"><span>问题 3: Affine transformations map parallel lines to parallel lines.</span></p><p class="ds-markdown-paragraph"><span>仿射变换确实将平行线映射为平行线。这是仿射变换的一个基本性质。仿射变换包括平移、旋转、缩放和剪切，所有这些都保持平行性。所以，答案应该是 "True"。</span></p><p class="ds-markdown-paragraph"><span>问题 4: What is the degree of freedom of similarity transformation?</span></p><p class="ds-markdown-paragraph"><span>相似变换（similarity transformation）在 2D 中包括平移、旋转和均匀缩放。相似变换的自由度是：平移有 2 个自由度（tx, ty），旋转有 1 个自由度（θ），缩放有 1 个自由度（s）。所以总共有 4 个自由度。在 3D 中，相似变换有 7 个自由度，但问题没有指定维度，但从上下文看，可能是指 2D，因为问题中提到了 "2D rotation matrices" 在问题 5 中。所以对于 2D 相似变换，自由度是 4。</span></p><p class="ds-markdown-paragraph"><span>问题 5: Select all (2D) rotation matrices.</span></p><p class="ds-markdown-paragraph"><span>选项是 A, B, C, D，但没有给出矩阵的具体内容。我需要从答案选项组中选择。既然问题没有显示矩阵，我假设在原始问题中矩阵是给出的，但在这里没有复制。或许我需要回想一下 2D 旋转矩阵的形式。</span></p><p class="ds-markdown-paragraph"><span>一个 2D 旋转矩阵是：</span></p><span class="katex-display ds-markdown-math"><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><semantics><mrow><mo fence="true">[</mo><mtable rowspacing="0.16em" columnalign="center center" columnspacing="1em"><mtr><mtd><mstyle scriptlevel="0" displaystyle="false"><mrow><mi>cos</mi><mo>⁡</mo><mi>θ</mi></mrow></mstyle></mtd><mtd><mstyle scriptlevel="0" displaystyle="false"><mrow><mo>−</mo><mi>sin</mi><mo>⁡</mo><mi>θ</mi></mrow></mstyle></mtd></mtr><mtr><mtd><mstyle scriptlevel="0" displaystyle="false"><mrow><mi>sin</mi><mo>⁡</mo><mi>θ</mi></mrow></mstyle></mtd><mtd><mstyle scriptlevel="0" displaystyle="false"><mrow><mi>cos</mi><mo>⁡</mo><mi>θ</mi></mrow></mstyle></mtd></mtr></mtable><mo fence="true">]</mo></mrow><annotation encoding="application/x-tex">\begin{bmatrix} \cos \theta &amp; -\sin \theta \\ \sin \theta &amp; \cos \theta \end{bmatrix} </annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:2.4em;vertical-align:-0.95em;"></span><span class="minner"><span class="mopen delimcenter" style="top:0em;"><span class="delimsizing size3">[</span></span><span class="mord"><span class="mtable"><span class="col-align-c"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:1.45em;"><span style="top:-3.61em;"><span class="pstrut" style="height:3em;"></span><span class="mord"><span class="mop">cos</span><span class="mspace" style="margin-right:0.1667em;"></span><span class="mord mathnormal" style="margin-right:0.02778em;">θ</span></span></span><span style="top:-2.41em;"><span class="pstrut" style="height:3em;"></span><span class="mord"><span class="mop">sin</span><span class="mspace" style="margin-right:0.1667em;"></span><span class="mord mathnormal" style="margin-right:0.02778em;">θ</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height:0.95em;"><span></span></span></span></span></span><span class="arraycolsep" style="width:0.5em;"></span><span class="arraycolsep" style="width:0.5em;"></span><span class="col-align-c"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:1.45em;"><span style="top:-3.61em;"><span class="pstrut" style="height:3em;"></span><span class="mord"><span class="mord">−</span><span class="mspace" style="margin-right:0.1667em;"></span><span class="mop">sin</span><span class="mspace" style="margin-right:0.1667em;"></span><span class="mord mathnormal" style="margin-right:0.02778em;">θ</span></span></span><span style="top:-2.41em;"><span class="pstrut" style="height:3em;"></span><span class="mord"><span class="mop">cos</span><span class="mspace" style="margin-right:0.1667em;"></span><span class="mord mathnormal" style="margin-right:0.02778em;">θ</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height:0.95em;"><span></span></span></span></span></span></span></span><span class="mclose delimcenter" style="top:0em;"><span class="delimsizing size3">]</span></span></span></span></span></span></span><p class="ds-markdown-paragraph"><span>或者有时是它的转置，但标准是上述形式。任何正交矩阵且行列式为 1 的 2x2 矩阵是旋转矩阵。</span></p><p class="ds-markdown-paragraph"><span>由于选项没有提供，我无法直接选择。但问题说 "答案选项组 A B C D"，所以我需要根据标准答案来判断。</span></p><p class="ds-markdown-paragraph"><span>或许在上下文中，选项是给定的，但在这里缺失了。既然这是一个多项选择，我可能需要假设哪些是旋转矩阵。</span></p><p class="ds-markdown-paragraph"><span>但为了这个练习，我可以说旋转矩阵是那些满足 R^T R = I 且 det(R) = 1 的矩阵。</span></p><p class="ds-markdown-paragraph"><span>既然问题没有提供矩阵，我可能无法具体回答。但或许在原始问题中，矩阵是列出的。</span></p><p class="ds-markdown-paragraph"><span>对于问题 5，既然它是标记问题，我可能需要等待用户提供更多信息，但作为 AI，我应该基于常识回答。</span></p><p class="ds-markdown-paragraph"><span>或许在问题 5 中，选项是矩阵，但在这里没有显示。让我检查一下问题文本。</span></p><p class="ds-markdown-paragraph"><span>在用户消息中，问题 5 是："Select all (2D) rotation matrices." 然后有 "A. B. C. D." 和 "答案选项组 A B C D"，但没有矩阵内容。这可能是一个错误。</span></p><p class="ds-markdown-paragraph"><span>或许在上下文中，矩阵是隐含的，或者我需要从答案中选择。</span></p><p class="ds-markdown-paragraph"><span>另一个想法：或许 "答案选项组" 意味着对于问题 5，我需要从 A,B,C,D 中选择哪些是旋转矩阵，但既然没有矩阵，我无法决定。</span></p><p class="ds-markdown-paragraph"><span>为了推进，我假设问题 5 的正确答案是那些符合旋转矩阵定义的选项。</span></p><p class="ds-markdown-paragraph"><span>但在实际中，我可能需要跳过或基于常见知识。</span></p><p class="ds-markdown-paragraph"><span>或许对于问题 5，标准旋转矩阵是像 [cosθ -sinθ; sinθ cosθ] 这样的矩阵。</span></p><p class="ds-markdown-paragraph"><span>既然问题没有提供，我将在回答中说明这一点。</span></p><p class="ds-markdown-paragraph"><span>现在，对于问题 4，自由度是 4。</span></p><p class="ds-markdown-paragraph"><span>让我整理答案。</span></p></blockquote><br/><p class="ds-markdown-paragraph"><span>根据您的查询，我将逐个回答每个问题。对于问题 5，由于您没有提供具体的矩阵选项，我无法直接选择，但我会解释如何识别 2D 旋转矩阵。</span></p><h3><span>问题 1: In blob detection, the characteristic scale is directly proportional to</span></h3><p class="ds-markdown-paragraph"><span>在 blob 检测中，特征尺度（characteristic scale）是指检测到 blob 的尺度，它与 blob 的物理尺寸直接相关。例如，在 Laplacian of Gaussian (LoG) 或 Difference of Gaussians (DoG) 方法中，特征尺度与 blob 的半径或直径成正比。因此，特征尺度与 blob 的大小直接比例。</span></p><ul><li><p class="ds-markdown-paragraph"><strong><span>答案</span></strong><span>: The size of blob</span></p></li></ul><h3><span>问题 2: SIFT descriptor is robust to scale and in-plane rotation.</span></h3><p class="ds-markdown-paragraph"><span>SIFT（Scale-Invariant Feature Transform）描述符被设计为对尺度变化和平面内旋转具有鲁棒性。它通过尺度空间检测关键点并计算方向来实现尺度不变性和旋转不变性。</span></p><ul><li><p class="ds-markdown-paragraph"><strong><span>答案</span></strong><span>: True</span></p></li></ul><h3><span>问题 3: Affine transformations map parallel lines to parallel lines.</span></h3><p class="ds-markdown-paragraph"><span>仿射变换（包括平移、旋转、缩放和剪切）具有保持平行线的性质，即平行线在变换后仍然平行。</span></p><ul><li><p class="ds-markdown-paragraph"><strong><span>答案</span></strong><span>: True</span></p></li></ul><h3><span>问题 4: What is the degree of freedom of similarity transformation?</span></h3><p class="ds-markdown-paragraph"><span>相似变换在 2D 空间中包括平移（2 个自由度）、旋转（1 个自由度）和均匀缩放（1 个自由度），因此总自由度为 4。在 3D 空间中，相似变换有 7 个自由度，但根据上下文（问题 5 涉及 2D 旋转矩阵），这里假设为 2D。</span></p><ul><li><p class="ds-markdown-paragraph"><strong><span>答案</span></strong><span>: 4</span></p></li></ul><h3><span>问题 5: Select all (2D) rotation matrices.</span></h3><p class="ds-markdown-paragraph"><span>由于您没有提供具体的矩阵选项 A、B、C、D，我无法直接选择。但一般来说，一个 2D 旋转矩阵应满足以下形式：</span></p><span class="katex-display ds-markdown-math"><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><semantics><mrow><mo fence="true">[</mo><mtable rowspacing="0.16em" columnalign="center center" columnspacing="1em"><mtr><mtd><mstyle scriptlevel="0" displaystyle="false"><mrow><mi>cos</mi><mo>⁡</mo><mi>θ</mi></mrow></mstyle></mtd><mtd><mstyle scriptlevel="0" displaystyle="false"><mrow><mo>−</mo><mi>sin</mi><mo>⁡</mo><mi>θ</mi></mrow></mstyle></mtd></mtr><mtr><mtd><mstyle scriptlevel="0" displaystyle="false"><mrow><mi>sin</mi><mo>⁡</mo><mi>θ</mi></mrow></mstyle></mtd><mtd><mstyle scriptlevel="0" displaystyle="false"><mrow><mi>cos</mi><mo>⁡</mo><mi>θ</mi></mrow></mstyle></mtd></mtr></mtable><mo fence="true">]</mo></mrow><annotation encoding="application/x-tex">\begin{bmatrix}
\cos \theta &amp; -\sin \theta \\
\sin \theta &amp; \cos \theta
\end{bmatrix}</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:2.4em;vertical-align:-0.95em;"></span><span class="minner"><span class="mopen delimcenter" style="top:0em;"><span class="delimsizing size3">[</span></span><span class="mord"><span class="mtable"><span class="col-align-c"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:1.45em;"><span style="top:-3.61em;"><span class="pstrut" style="height:3em;"></span><span class="mord"><span class="mop">cos</span><span class="mspace" style="margin-right:0.1667em;"></span><span class="mord mathnormal" style="margin-right:0.02778em;">θ</span></span></span><span style="top:-2.41em;"><span class="pstrut" style="height:3em;"></span><span class="mord"><span class="mop">sin</span><span class="mspace" style="margin-right:0.1667em;"></span><span class="mord mathnormal" style="margin-right:0.02778em;">θ</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height:0.95em;"><span></span></span></span></span></span><span class="arraycolsep" style="width:0.5em;"></span><span class="arraycolsep" style="width:0.5em;"></span><span class="col-align-c"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:1.45em;"><span style="top:-3.61em;"><span class="pstrut" style="height:3em;"></span><span class="mord"><span class="mord">−</span><span class="mspace" style="margin-right:0.1667em;"></span><span class="mop">sin</span><span class="mspace" style="margin-right:0.1667em;"></span><span class="mord mathnormal" style="margin-right:0.02778em;">θ</span></span></span><span style="top:-2.41em;"><span class="pstrut" style="height:3em;"></span><span class="mord"><span class="mop">cos</span><span class="mspace" style="margin-right:0.1667em;"></span><span class="mord mathnormal" style="margin-right:0.02778em;">θ</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height:0.95em;"><span></span></span></span></span></span></span></span><span class="mclose delimcenter" style="top:0em;"><span class="delimsizing size3">]</span></span></span></span></span></span></span><p class="ds-markdown-paragraph"><span>或等价形式。旋转矩阵是正交矩阵（行列式为 1，且满足 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><msup><mi>R</mi><mi>T</mi></msup><mi>R</mi><mo>=</mo><mi>I</mi></mrow><annotation encoding="application/x-tex">R^T R = I</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.8413em;"></span><span class="mord"><span class="mord mathnormal" style="margin-right:0.00773em;">R</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height:0.8413em;"><span style="top:-3.063em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mathnormal mtight" style="margin-right:0.13889em;">T</span></span></span></span></span></span></span></span><span class="mord mathnormal" style="margin-right:0.00773em;">R</span><span class="mspace" style="margin-right:0.2778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right:0.2778em;"></span></span><span class="base"><span class="strut" style="height:0.6833em;"></span><span class="mord mathnormal" style="margin-right:0.07847em;">I</span></span></span></span><span>）。请检查您的选项是否符合这些条件。如果您能提供具体的矩阵，我可以协助判断。</span></p><p class="ds-markdown-paragraph"><span>如果您需要进一步澄清或提供问题 5 的矩阵选项，请随时告知！</span></p>

