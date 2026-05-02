### 用户

\subsection{Implementation Overview}
The SIFT algorithm was implemented in three main parts:
\subsection{Part A: DoG Keypoint Detection}
\subsubsection{Design Choices and Main Ideas}
The DoG keypoint detection was implemented following these key steps:
\begin{itemize}
    \item \textbf{Gaussian Pyramid Construction}: Built using the formula $\sigma_{o,i} = \sigma \cdot 2^o \cdot k^i$ where $k = 2^{1/s}$ and $s = \text{num\_scales}$. Each octave contains $s+3$ images to ensure sufficient DoG images for extrema detection.
    
    \item \textbf{DoG Pyramid}: Computed as the difference between consecutive Gaussian images: $D(x,y,\sigma) = G(x,y,k\sigma) - G(x,y,\sigma)$
    
    \item \textbf{Extrema Detection}: Searched for local maxima and minima in a $3 \times 3 \times 3$ neighborhood across scale space, excluding border pixels and the first/last DoG layers.
    
    \item \textbf{Contrast Filtering}: Removed low-contrast keypoints with $|D(x)| < 0.03$.
    
    \item \textbf{Edge Response Suppression}: Applied Hessian-based edge suppression using the criterion:
    $$\frac{(\text{Tr}(H))^2}{\det(H)} < \frac{(r+1)^2}{r}$$
    where $r = 10$ and $\det(H) > 0$.
\end{itemize}
\subsection{Part B: Orientation Assignment}
\subsubsection{Design Choices and Main Ideas}
The orientation assignment ensures rotation invariance through:
\begin{itemize}
    \item \textbf{Gradient Computation}: Calculated image gradients using Sobel operators in a window of radius $3\sigma$ around each keypoint.
    
    \item \textbf{Gaussian Weighting}: Applied Gaussian weights with $\sigma_{\text{ori}} = 1.5\sigma$ to emphasize gradients closer to the keypoint center.
    
    \item \textbf{Orientation Histogram}: Built a 36-bin histogram covering $[0, 2\pi)$ with bilinear interpolation for smooth bin assignment.
    
    \item \textbf{Histogram Smoothing}: Applied multiple smoothing iterations using a $[0.25, 0.5, 0.25]$ kernel.
    
    \item \textbf{Peak Detection}: Identified the dominant orientation from the highest peak, and created additional keypoints for peaks exceeding 80\% of the maximum value.
    
    \item \textbf{Parabolic Interpolation}: Refined peak locations using parabolic fitting:
    $$\text{offset} = \frac{0.5(h_{\text{left}} - h_{\text{right}})}{h_{\text{left}} - 2h_{\text{center}} + h_{\text{right}}}$$
\end{itemize}

\subsection{Part C: SIFT Descriptor Computation}
\subsubsection{Design Choices and Main Ideas}
The 128-dimensional SIFT descriptor computation involved:
\begin{itemize}
    \item \textbf{Sampling Region}: Defined a $16 \times 16$ pixel sampling grid around each keypoint, scaled by $\sigma$ (each cell covers $3\sigma$ pixels).
    
    \item \textbf{Gradient Rotation}: Rotated gradient orientations by $-\theta$ (keypoint's dominant orientation) to achieve rotation invariance, without rotating the image patch itself.
    
    \item \textbf{Spatial Organization}: Divided the region into a $4 \times 4$ grid of cells, each contributing an 8-bin orientation histogram.
    
    \item \textbf{Trilinear Interpolation}: Distributed gradient contributions using trilinear interpolation across:
    \begin{itemize}
        \item Spatial dimensions (x, y coordinates within cells)
        \item Orientation dimension (8 orientation bins)
    \end{itemize}
    
    \item \textbf{Gaussian Weighting}: Applied Gaussian weighting with $\sigma = 0.5 \times \text{window\_size}$ to reduce boundary effects.
    
    \item \textbf{Normalization Pipeline}:
    \begin{enumerate}
        \item L2 normalize to unit length
        \item Clamp values above 0.2 to reduce illumination effects
        \item Re-normalize to unit length
    \end{enumerate}
\end{itemize}略微简化对算法的描述，合并小标题但不要删除关键内容和公式

---

### DeepSeek AI

<p>思考：</p><blockquote><p class="ds-markdown-paragraph"><span>我们有两个主要部分：DoG关键点检测和SIFT描述子计算。为了简化，我们可以将Part B（方向分配）与Part C（描述子计算）合并，因为方向分配是描述子计算的前置步骤。同时，我们保留关键公式和步骤，但可以适当合并一些条目。</span></p><p class="ds-markdown-paragraph"><span>修改后的结构如下：</span></p><ol start="1"><li><p class="ds-markdown-paragraph"><span>DoG关键点检测（包括高斯金字塔、DoG金字塔、极值检测、对比度过滤和边缘响应抑制）</span></p></li><li><p class="ds-markdown-paragraph"><span>方向分配与描述子计算（包括梯度计算、方向直方图、关键点方向、描述子生成和归一化）</span></p></li></ol><p class="ds-markdown-paragraph"><span>注意：我们保留所有公式，但可以简化文字描述。</span></p></blockquote><br/><p class="ds-markdown-paragraph"><span>\subsection{Implementation Overview}</span><br><span>The SIFT algorithm was implemented in three main parts: DoG Keypoint Detection, Orientation Assignment, and SIFT Descriptor Computation.</span></p><p class="ds-markdown-paragraph"><span>\subsection{Keypoint Detection and Description}</span><br><span>\subsubsection{Design Choices and Main Ideas}</span></p><p class="ds-markdown-paragraph"><span>\textbf{DoG Keypoint Detection:}</span><br><span>\begin{itemize}</span><br><span>\item \textbf{Gaussian Pyramid}: Built using $\sigma_{o,i} = \sigma \cdot 2^o \cdot k^i$ where $k = 2^{1/s}$, with each octave containing $s+3$ images to ensure sufficient DoG images</span><br><span>\item \textbf{DoG Pyramid}: Computed as $D(x,y,\sigma) = G(x,y,k\sigma) - G(x,y,\sigma)$</span><br><span>\item \textbf{Extrema Detection}: Local maxima/minima in $3 \times 3 \times 3$ neighborhood across scale space</span><br><span>\item \textbf{Keypoint Filtering}:</span><br><span>\begin{itemize}</span><br><span>\item Contrast filtering: $|D(x)| &lt; 0.03$</span><br><span>\item Edge suppression: $\frac{(\text{Tr}(H))^2}{\det(H)} &lt; \frac{(r+1)^2}{r}$ where $r = 10$</span><br><span>\end{itemize}</span><br><span>\end{itemize}</span></p><p class="ds-markdown-paragraph"><span>\textbf{Orientation Assignment and Descriptor Computation:}</span><br><span>\begin{itemize}</span><br><span>\item \textbf{Orientation Assignment}:</span><br><span>\begin{itemize}</span><br><span>\item Gradient computation using Sobel operators in $3\sigma$ window</span><br><span>\item Gaussian weighting with $\sigma_{\text{ori}} = 1.5\sigma$</span><br><span>\item 36-bin orientation histogram with bilinear interpolation</span><br><span>\item Peak detection with parabolic refinement: $\text{offset} = \frac{0.5(h_{\text{left}} - h_{\text{right}})}{h_{\text{left}} - 2h_{\text{center}} + h_{\text{right}}}$</span><br><span>\end{itemize}</span></p><div class="md-code-block md-code-block-light"><div class="md-code-block-banner-wrap"><div class="md-code-block-banner md-code-block-banner-lite"><div class="_121d384"><div class="d2a24f03"><span class="d813de27">text</span></div><div class="d2a24f03 _246a029"><div class="efa13877"><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon" style="margin-right: 4px;"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.14923 4.02032C7.11191 4.02032 7.87977 4.02017 8.49591 4.07599C9.12122 4.1327 9.65786 4.25188 10.1414 4.53107C10.7201 4.8653 11.2008 5.34591 11.535 5.92462C11.8142 6.40818 11.9333 6.94482 11.9901 7.57013C12.0459 8.18625 12.0457 8.9542 12.0457 9.91681C12.0457 10.8795 12.0459 11.6474 11.9901 12.2635C11.9333 12.8888 11.8142 13.4254 11.535 13.909C11.2008 14.4877 10.7201 14.9683 10.1414 15.3026C9.65786 15.5817 9.12122 15.7009 8.49591 15.7576C7.87977 15.8134 7.1119 15.8133 6.14923 15.8133C5.18661 15.8133 4.41868 15.8134 3.80255 15.7576C3.17724 15.7009 2.6406 15.5817 2.15704 15.3026C1.57834 14.9684 1.09772 14.4877 0.763489 13.909C0.484305 13.4254 0.365123 12.8888 0.308411 12.2635C0.252587 11.6474 0.252747 10.8795 0.252747 9.91681C0.252747 8.95419 0.252603 8.18625 0.308411 7.57013C0.365123 6.94482 0.484305 6.40818 0.763489 5.92462C1.09771 5.3459 1.57833 4.86529 2.15704 4.53107C2.6406 4.25188 3.17724 4.1327 3.80255 4.07599C4.41868 4.02018 5.1866 4.02032 6.14923 4.02032ZM6.14923 5.37775C5.16175 5.37775 4.46628 5.37761 3.9256 5.42657C3.39428 5.47473 3.07853 5.56574 2.83575 5.70587C2.46313 5.92106 2.15348 6.23071 1.93829 6.60333C1.79817 6.84611 1.70715 7.16185 1.659 7.69318C1.61004 8.23385 1.61017 8.92934 1.61017 9.91681C1.61017 10.9043 1.61002 11.5998 1.659 12.1404C1.70715 12.6717 1.79817 12.9875 1.93829 13.2303C2.15349 13.6029 2.46315 13.9126 2.83575 14.1277C3.07853 14.2679 3.39428 14.3589 3.9256 14.407C4.46628 14.456 5.16176 14.4559 6.14923 14.4559C7.13675 14.4559 7.83218 14.456 8.37286 14.407C8.90419 14.3589 9.21993 14.2679 9.46271 14.1277C9.83529 13.9126 10.145 13.6029 10.3602 13.2303C10.5003 12.9875 10.5913 12.6718 10.6395 12.1404C10.6884 11.5998 10.6883 10.9043 10.6883 9.91681C10.6883 8.92935 10.6884 8.23385 10.6395 7.69318C10.5913 7.16185 10.5003 6.84611 10.3602 6.60333C10.145 6.23072 9.8353 5.92107 9.46271 5.70587C9.21993 5.56574 8.90418 5.47473 8.37286 5.42657C7.83218 5.3776 7.13676 5.37775 6.14923 5.37775ZM9.80157 0.367981C10.7637 0.367981 11.5313 0.367886 12.1473 0.423645C12.7725 0.480313 13.3093 0.598765 13.7928 0.877747C14.3716 1.21192 14.852 1.69355 15.1863 2.27228C15.4655 2.75575 15.5857 3.29165 15.6424 3.91681C15.6982 4.53301 15.6971 5.30161 15.6971 6.26447V7.8299C15.6971 8.29265 15.6989 8.58994 15.6649 8.84845C15.4667 10.3525 14.4009 11.5738 12.9832 11.9988V10.5467C13.6973 10.1903 14.2104 9.49662 14.3192 8.67169C14.3387 8.52348 14.3406 8.3358 14.3406 7.8299V6.26447C14.3406 5.27707 14.3398 4.58149 14.2908 4.04083C14.2427 3.50969 14.1526 3.19373 14.0125 2.95099C13.7974 2.5785 13.4875 2.2687 13.1151 2.05353C12.8723 1.91347 12.5563 1.82237 12.0252 1.77423C11.4846 1.72528 10.7888 1.7254 9.80157 1.7254H7.71466C6.75614 1.72559 5.92659 2.27697 5.52325 3.07892H4.07013C4.54215 1.51132 5.99314 0.368192 7.71466 0.367981H9.80157Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">复制</span></span><div class="ds-focus-ring"></div></button><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M15.3695 11.411L15.1234 12.8866C14.8869 14.3042 13.6603 15.3436 12.223 15.3436H3.7767C2.33954 15.3434 1.11276 14.3042 0.876312 12.8866L0.630219 11.411L2.05405 11.1747L2.29916 12.6493C2.41969 13.3713 3.04472 13.9001 3.7767 13.9003H12.223C12.9551 13.9002 13.58 13.3713 13.7005 12.6493L13.9456 11.1747L15.3695 11.411ZM8.72202 8.994C8.77714 8.93934 8.83789 8.88106 8.90268 8.81627L12.4828 5.23424L13.5042 6.25572L9.92221 9.8358C9.63947 10.1185 9.3876 10.3732 9.15854 10.5575C8.91889 10.7503 8.6395 10.9224 8.28647 10.9784C8.09708 11.0083 7.9036 11.0083 7.7142 10.9784C7.36103 10.9224 7.08087 10.7503 6.84116 10.5575C6.61212 10.3732 6.36019 10.1185 6.07748 9.8358L2.49643 6.25572L3.51694 5.23424L7.09702 8.81627C7.16216 8.88142 7.22327 8.94006 7.27866 8.99498V1.3065H8.72202V8.994Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">下载</span></span><div class="ds-focus-ring"></div></button></div></div></div></div></div><pre>\item \textbf{Descriptor Computation}:
\begin{itemize}
    \item $16 \times 16$ sampling grid scaled by $\sigma$ (each cell covers $3\sigma$ pixels)
    \item Gradient rotation by $-\theta$ for rotation invariance
    \item $4 \times 4$ grid of cells with 8-bin orientation histograms
    \item Trilinear interpolation across spatial and orientation dimensions
    \item Normalization pipeline: L2 normalize → clamp values &gt; 0.2 → re-normalize
\end{itemize}</pre><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _33882ae"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _28d7e84"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg></div><p class="ds-markdown-paragraph"><span>\end{itemize}</span></p>

