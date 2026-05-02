### 用户

\section{问题三：有向图的模块度}

\subsection*{问题重述}

在有向图$G$中，模块度定义为：
$$Q_d = \frac{1}{m} \sum_{i,j} \left[ A_{ij} - \frac{k_i^{\text{out}} k_j^{\text{in}}}{m} \right] \delta(c_i, c_j)$$

其中：$m$为总边权重；$A_{ij}$为从节点$i$到节点$j$的边权重；$k_i^{\text{out}} = \sum_j A_{ij}$为节点$i$的出度；$k_i^{\text{in}} = \sum_j A_{ji}$为节点$i$的入度；$\delta(c_i, c_j) = 1$当且仅当节点$i$和$j$属于同一社区，否则为0。

现需证明：将节点$i$移动到社区$\mathcal{C}$的模块度增益为：
$$\Delta Q_d(i \to \mathcal{C}) = \frac{k_{i,\text{in}}}{m} - \frac{k_i^{\text{out}} k_{\text{tot}}^{\text{in}} + k_i^{\text{in}} k_{\text{tot}}^{\text{out}}}{m^2}$$

其中：$k_{i,\text{in}} = \sum_{j \in \mathcal{C}} (A_{ij} + A_{ji})$为节点$i$与社区$\mathcal{C}$中所有节点之间的双向边权重之和；$k_{\text{tot}}^{\text{out}} = \sum_{j \in \mathcal{C}} k_j^{\text{out}}$为社区$\mathcal{C}$的总出度；$k_{\text{tot}}^{\text{in}} = \sum_{j \in \mathcal{C}} k_j^{\text{in}}$为社区$\mathcal{C}$的总入度。

\subsection*{证明}

假设初始时节点$i$单独构成一个社区（即社区$\{i\}$），而社区$\mathcal{C}$为另一个不包含$i$的社区。将节点$i$移动到社区$\mathcal{C}$即表示将$i$合并到$\mathcal{C}$中，形成新社区$\mathcal{C} \cup \{i\}$，同时原社区$\{i\}$消失。该操作引起的模块度变化为：
$$\Delta Q_d(i \to \mathcal{C}) = Q(\mathcal{C} \cup \{i\}) - Q(\mathcal{C}) - Q(\{i\})$$

移动前，社区$\mathcal{C}$的贡献为$Q(\mathcal{C}) = \frac{1}{m} \sum_{u,v \in \mathcal{C}} \left[ A_{uv} - \frac{k_u^{\text{out}} k_v^{\text{in}}}{m} \right]$，社区$\{i\}$的贡献（节点$i$自环项）为$Q(\{i\}) = \frac{1}{m} \left[ A_{ii} - \frac{k_i^{\text{out}} k_i^{\text{in}}}{m} \right]$。合并后的社区$\mathcal{C} \cup \{i\}$的贡献为：
$$Q(\mathcal{C} \cup \{i\}) = \frac{1}{m} \sum_{u,v \in \mathcal{C} \cup \{i\}} \left[ A_{uv} - \frac{k_u^{\text{out}} k_v^{\text{in}}}{m} \right]$$

将其展开为四部分：$u, v \in \mathcal{C}$（与$Q(\mathcal{C})$相同）；$u \in \mathcal{C}, v = i$（涉及从$\mathcal{C}$中节点到$i$的边）；$u = i, v \in \mathcal{C}$（涉及从$i$到$\mathcal{C}$中节点的边）；$u = i, v = i$（节点$i$的自环）。因此：
$$\begin{aligned}
Q(\mathcal{C} \cup \{i\}) &= \frac{1}{m} \Bigg[ \sum_{u,v \in \mathcal{C}} \left( A_{uv} - \frac{k_u^{\text{out}} k_v^{\text{in}}}{m} \right) + \sum_{u \in \mathcal{C}} \left( A_{ui} - \frac{k_u^{\text{out}} k_i^{\text{in}}}{m} \right) \\
&\quad + \sum_{v \in \mathcal{C}} \left( A_{iv} - \frac{k_i^{\text{out}} k_v^{\text{in}}}{m} \right) + \left( A_{ii} - \frac{k_i^{\text{out}} k_i^{\text{in}}}{m} \right) \Bigg]
\end{aligned}$$

计算$Q(\mathcal{C} \cup \{i\}) - Q(\mathcal{C})$得：
$$Q(\mathcal{C} \cup \{i\}) - Q(\mathcal{C}) = \frac{1}{m} \Bigg[ \sum_{u \in \mathcal{C}} \left( A_{ui} - \frac{k_u^{\text{out}} k_i^{\text{in}}}{m} \right) + \sum_{v \in \mathcal{C}} \left( A_{iv} - \frac{k_i^{\text{out}} k_v^{\text{in}}}{m} \right) + \left( A_{ii} - \frac{k_i^{\text{out}} k_i^{\text{in}}}{m} \right) \Bigg]$$

再减去$Q(\{i\})$，注意到$A_{ii}$项和$\frac{k_i^{\text{out}} k_i^{\text{in}}}{m}$项相互抵消，得：
$$\Delta Q_d(i \to \mathcal{C}) = \frac{1}{m} \left[ \sum_{u \in \mathcal{C}} \left( A_{ui} - \frac{k_u^{\text{out}} k_i^{\text{in}}}{m} \right) + \sum_{v \in \mathcal{C}} \left( A_{iv} - \frac{k_i^{\text{out}} k_v^{\text{in}}}{m} \right) \right]$$

对于实际连接部分，有$\sum_{u \in \mathcal{C}} A_{ui} + \sum_{v \in \mathcal{C}} A_{iv} = k_{i,\text{in}}$（根据$k_{i,\text{in}}$定义）。对于期望连接部分：
$$\sum_{u \in \mathcal{C}} \frac{k_u^{\text{out}} k_i^{\text{in}}}{m} + \sum_{v \in \mathcal{C}} \frac{k_i^{\text{out}} k_v^{\text{in}}}{m} = \frac{k_i^{\text{in}} \sum_{u \in \mathcal{C}} k_u^{\text{out}} + k_i^{\text{out}} \sum_{v \in \mathcal{C}} k_v^{\text{in}}}{m} = \frac{k_i^{\text{in}} k_{\text{tot}}^{\text{out}} + k_i^{\text{out}} k_{\text{tot}}^{\text{in}}}{m}$$

其中$k_{\text{tot}}^{\text{out}} = \sum_{u \in \mathcal{C}} k_u^{\text{out}}$，$k_{\text{tot}}^{\text{in}} = \sum_{v \in \mathcal{C}} k_v^{\text{in}}$。代入得：
$$\Delta Q_d(i \to \mathcal{C}) = \frac{k_{i,\text{in}}}{m} - \frac{1}{m} \cdot \frac{k_i^{\text{in}} k_{\text{tot}}^{\text{out}} + k_i^{\text{out}} k_{\text{tot}}^{\text{in}}}{m} = \frac{k_{i,\text{in}}}{m} - \frac{k_i^{\text{out}} k_{\text{tot}}^{\text{in}} + k_i^{\text{in}} k_{\text{tot}}^{\text{out}}}{m^2}$$

上述推导表明，在假设节点$i$初始单独成社区的条件下，将其移动到社区$\mathcal{C}$的模块度增益即为所求公式。该公式由两部分组成：第一项$\frac{k_{i,\text{in}}}{m}$反映节点$i$与社区$\mathcal{C}$的实际连接强度；第二项$-\frac{k_i^{\text{out}} k_{\text{tot}}^{\text{in}} + k_i^{\text{in}} k_{\text{tot}}^{\text{out}}}{m^2}$反映在随机零模型下节点$i$与社区$\mathcal{C}$的期望连接强度。当实际连接显著大于期望连接时，模块度增益为正，移动操作可优化社区划分。该公式为有向图中社区检测算法（如Louvain算法）提供了局部优化的理论依据。证毕。

\end{document}

---

### DeepSeek AI

<p>思考：</p><blockquote><p class="ds-markdown-paragraph"><span>我们被问到证明对于有向图，将节点i移动到社区C的模块度增益为：</span><br><span>ΔQ_d(i → C) = (k_{i,in}/m) - (</span></p></blockquote><br/><div class="_245c867"><div class="_5ab5d64"><div class="ds-icon _970ac5e dea47b2e" style="font-size: 16px; width: 16px; height: 16px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M8.00195 6.64454C8.75029 6.64454 9.35735 7.25169 9.35742 8.00001C9.35742 8.74838 8.75033 9.35548 8.00195 9.35548C7.2537 9.35533 6.64746 8.74829 6.64746 8.00001C6.64753 7.25178 7.25374 6.64468 8.00195 6.64454Z" fill="currentColor"></path><path fill-rule="evenodd" clip-rule="evenodd" d="M9.97168 1.29981C11.5854 0.718916 13.271 0.642197 14.3145 1.68555C15.3578 2.72902 15.2811 4.41466 14.7002 6.02833C14.4708 6.66561 14.1505 7.32937 13.75 8.00001C14.1505 8.67062 14.4708 9.33444 14.7002 9.97169C15.2811 11.5854 15.3579 13.271 14.3145 14.3145C13.271 15.3579 11.5854 15.2811 9.97168 14.7002C9.33443 14.4708 8.67062 14.1505 8 13.75C7.32936 14.1505 6.66561 14.4708 6.02832 14.7002C4.41464 15.2811 2.72902 15.3578 1.68555 14.3145C0.642186 13.271 0.718901 11.5854 1.29981 9.97169C1.52918 9.33454 1.84868 8.67049 2.24902 8.00001C1.84869 7.32953 1.52918 6.66544 1.29981 6.02833C0.718882 4.41459 0.6421 2.729 1.68555 1.68555C2.729 0.642112 4.41459 0.718887 6.02832 1.29981C6.66544 1.52918 7.32953 1.8487 8 2.24903C8.67048 1.84869 9.33454 1.52919 9.97168 1.29981ZM12.9404 9.2129C12.4391 9.893 11.8616 10.5681 11.2148 11.2149C10.5681 11.8616 9.89299 12.4391 9.21289 12.9404C9.62535 13.1579 10.0271 13.338 10.4121 13.4766C11.9146 14.0174 12.9173 13.8738 13.3955 13.3955C13.8737 12.9173 14.0174 11.9146 13.4766 10.4121C13.338 10.0271 13.1579 9.62535 12.9404 9.2129ZM3.05859 9.2129C2.84124 9.62523 2.662 10.0272 2.52344 10.4121C1.98255 11.9146 2.1263 12.9172 2.60449 13.3955C3.08281 13.8737 4.08548 14.0174 5.58789 13.4766C5.97267 13.338 6.37392 13.1577 6.78613 12.9404C6.10627 12.4393 5.43171 11.8614 4.78516 11.2149C4.13826 10.5679 3.55995 9.89313 3.05859 9.2129ZM7.99902 3.792C7.23182 4.31419 6.45309 4.95512 5.7041 5.70411C4.95512 6.45309 4.31418 7.23184 3.79199 7.99903C4.31434 8.76666 4.95474 9.54653 5.7041 10.2959C6.45312 11.0449 7.23274 11.6848 8 12.207C8.76728 11.6848 9.54686 11.0449 10.2959 10.2959C11.0449 9.54686 11.6848 8.76729 12.207 8.00001C11.6848 7.23275 11.0449 6.45312 10.2959 5.70411C9.54653 4.95475 8.76665 4.31434 7.99902 3.792ZM5.58789 2.52344C4.08536 1.98255 3.08275 2.12625 2.60449 2.6045C2.12624 3.08275 1.98255 4.08536 2.52344 5.5879C2.66192 5.97253 2.84143 6.37409 3.05859 6.78614C3.55986 6.10611 4.13843 5.43189 4.78516 4.78516C5.4319 4.13843 6.10609 3.55987 6.78613 3.0586C6.37408 2.84144 5.97252 2.66192 5.58789 2.52344ZM13.3955 2.6045C12.9172 2.12631 11.9146 1.98257 10.4121 2.52344C10.0272 2.66201 9.62522 2.84125 9.21289 3.0586C9.89313 3.55996 10.5679 4.13827 11.2148 4.78516C11.8614 5.43172 12.4392 6.10627 12.9404 6.78614C13.1577 6.37393 13.338 5.97267 13.4766 5.5879C14.0174 4.08549 13.8736 3.08281 13.3955 2.6045Z" fill="currentColor"></path></svg></div><span class="_5255ff8 _4d41763">已停止</span><div class="ds-icon" style="font-size: 14px; width: 14px; height: 14px;"><svg width="14" height="14" viewBox="0 0 14 14" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M11.8486 5.5L11.4238 5.92383L8.69727 8.65137C8.44157 8.90706 8.21562 9.13382 8.01172 9.29785C7.79912 9.46883 7.55595 9.61756 7.25 9.66602C7.08435 9.69222 6.91565 9.69222 6.75 9.66602C6.44405 9.61756 6.20088 9.46883 5.98828 9.29785C5.78438 9.13382 5.55843 8.90706 5.30273 8.65137L2.57617 5.92383L2.15137 5.5L3 4.65137L3.42383 5.07617L6.15137 7.80273C6.42595 8.07732 6.59876 8.24849 6.74023 8.3623C6.87291 8.46904 6.92272 8.47813 6.9375 8.48047C6.97895 8.48703 7.02105 8.48703 7.0625 8.48047C7.07728 8.47813 7.12709 8.46904 7.25977 8.3623C7.40124 8.24849 7.57405 8.07732 7.84863 7.80273L10.5762 5.07617L11 4.65137L11.8486 5.5Z" fill="currentColor"></path></svg></div></div><div class="c99b79f8" style="opacity: 0;"></div></div><div class="c2b72bb8"></div><div class="e1675d8b ds-think-content _767406f"><div class="ddd26891 _9b52f6c" style="width: 16px; height: 16px;"><div class="a510c7ce _0652043"></div></div><div class="_9ecc93a"></div><div class="ds-markdown" style="--ds-md-zoom: 1.143;"><p class="ds-markdown-paragraph"><span>我们被问到证明对于有向图，将节点i移动到社区C的模块度增益为：</span><br><span>ΔQ_d(i → C) = (k_{i,in}/m) - (</span></p></div></div><div class="_8f7678d"></div>

---

### 用户

In image segmentation, the term grouping mainly refers to:

答案选项组

Clustering pixels into perceptually coherent regions

Assigning a single label to the whole image

Detecting object boundaries only

Compressing image information
 
标记问题：问题 2
问题 21 分
Bottom-up image segmentation is primarily driven by:

答案选项组

Low-level feature similarity

High-level object semantics

Pixel-wise supervision

Predefined object categories
 
标记问题：问题 3
问题 31 分
In graph-based segmentation, edge weights usually encode:

答案选项组

Pixel similarity based on appearance and proximity

Physical distance only

Object-level semantic similarity

Gradient magnitude
 
标记问题：问题 4
问题 41 分
A key limitation of minimizing the standard graph cut (min-cut) objective is that it:

答案选项组

Tends to isolate small sets of pixels

Produces overly large segments

Is computationally infeasible

Requires supervised labels

---

### DeepSeek AI

<p>思考：</p><blockquote><p class="ds-markdown-paragraph"><span>嗯，用户发来的是关于图像分割的四道选择题，看起来像是课程测试或者自学测验。让我逐一分析每个问题。</span></p><p class="ds-markdown-paragraph"><span>第一个问题问的是“grouping”在图像分割中的主要含义。图像分割的本质就是把具有相似特征的像素归类到一起，形成有意义的区域。其他选项明显不符合定义，比如给整张图贴标签是分类任务，只检测边界是边缘检测，压缩信息则是编码领域的事。</span></p><p class="ds-markdown-paragraph"><span>第二个问题关于自底向上分割的驱动因素。自底向上就是从像素级特征开始合并，所以依赖的是颜色、纹理这些低层特征相似性。高层的语义信息那是自上而下方法关注的。</span></p><p class="ds-markdown-paragraph"><span>第三个问题考察图割方法中边的权重设置。经典算法如Normalized Cut里，边的权重确实同时考虑外观相似度和空间接近度，这样才能有效聚类。单纯用物理距离或梯度都不全面。</span></p><p class="ds-markdown-paragraph"><span>第四个问题涉及标准最小割的缺陷。这个在教材里常提到，由于只考虑割的代价，容易切出特别小的孤立点或碎片区域。后来改进的归一化割就是为了避免这个问题。</span></p><p class="ds-markdown-paragraph"><span>用户可能正在学习计算机视觉课程，或者准备相关考试。这些问题都比较基础，但如果不理解核心概念容易选错。需要确保解释清晰准确，帮助ta巩固知识点。</span></p></blockquote><br/><p class="ds-markdown-paragraph"><span>以下是对您提出的图像分割相关选择题的分析与解答：</span></p><h3><span>问题 1</span></h3><p class="ds-markdown-paragraph"><strong><span>问题</span></strong><span>： In image segmentation, the term grouping mainly refers to:</span><br><span></span><strong><span>正确选项</span></strong><span>： </span><strong><span>Clustering pixels into perceptually coherent regions</span></strong><span></span><br><span></span><strong><span>分析</span></strong><span>：“Grouping”（分组）在图像分割中是一个核心概念，指的是根据颜色、纹理、亮度等特征的相似性，将像素聚类成在感知上连贯的区域，从而形成有意义的图像部分或对象。</span></p><h3><span>问题 2</span></h3><p class="ds-markdown-paragraph"><strong><span>问题</span></strong><span>： Bottom-up image segmentation is primarily driven by:</span><br><span></span><strong><span>正确选项</span></strong><span>： </span><strong><span>Low-level feature similarity</span></strong><span></span><br><span></span><strong><span>分析</span></strong><span>： 自底向上分割是一种数据驱动的方法，它从像素或超像素开始，主要依据低层特征（如颜色、强度、纹理的相似性）的相似度进行合并，最终形成区域。它不依赖于先验的语义信息。</span></p><h3><span>问题 3</span></h3><p class="ds-markdown-paragraph"><strong><span>问题</span></strong><span>： In graph-based segmentation, edge weights usually encode:</span><br><span></span><strong><span>正确选项</span></strong><span>： </span><strong><span>Pixel similarity based on appearance and proximity</span></strong><span></span><br><span></span><strong><span>分析</span></strong><span>： 在图割等基于图的分割方法中，图像被建模为图，像素或区域是节点，连接节点的边上的权重通常编码了像素之间的相似性。这种相似性综合了外观（如颜色、强度）和空间邻近度两个核心因素。</span></p><h3><span>问题 4</span></h3><p class="ds-markdown-paragraph"><strong><span>问题</span></strong><span>： A key limitation of minimizing the standard graph cut (min-cut) objective is that it:</span><br><span></span><strong><span>正确选项</span></strong><span>： </span><strong><span>Tends to isolate small sets of pixels</span></strong><span></span><br><span></span><strong><span>分析</span></strong><span>： 最小割的目标是最小化将一个图切成两个子集时切割边的总权重。一个主要缺陷是，它倾向于切割出非常小的、孤立的节点或像素组，因为切断与少数像素的连接代价通常很低。这会导致不理想的、过小的分割片段。为此，后续提出了归一化割（Normalized Cut）等改进方案。</span></p>

