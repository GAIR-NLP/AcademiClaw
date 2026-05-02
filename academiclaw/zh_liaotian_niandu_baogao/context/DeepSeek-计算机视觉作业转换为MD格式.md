### 用户

把这份pdf输出成md格式

---

### DeepSeek AI

<p>思考：</p><blockquote><p class="ds-markdown-paragraph"><span>嗯，看到了一个计算机视觉的作业PDF文件。用户想要我把它转换成markdown格式。让我看看这个文件的内容是什么……</span></p><p class="ds-markdown-paragraph"><span>哦，这是一个作业，分为两个主要部分：编程作业和书面作业。编程作业占了85分，包括实现一个基于Bag-of-Visual-Words的图像分类流程。作业是使用Caltech-101数据集，需要提取SIFT特征、构建视觉词典、计算BoW直方图，最后用线性SVM进行分类。</span></p><p class="ds-markdown-paragraph"><span>还有书面作业部分，有两个问题。第一个是关于相机运动和深度对运动场影响的推导问题。第二个是关于光流方程的解集表示问题。</span></p><p class="ds-markdown-paragraph"><span>我需要把这个结构清晰地转换成markdown格式。markdown应该保持原PDF的层级结构，包括标题、子标题、任务列表等。编程作业的每个任务都有明确的说明，我应该用适当的markdown标记来呈现它们。</span></p><p class="ds-markdown-paragraph"><span>对于书面作业部分，那些数学公式可能需要特别注意。在markdown中，我可以使用LaTeX语法来表示这些公式，这样能保持数学表达式的清晰度。</span></p><p class="ds-markdown-paragraph"><span>我觉得可以用标题来表示不同部分，用列表来表示各个任务点，用代码块表示那些需要实现的函数名称。对于数学公式，就用$...$或</span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi mathvariant="normal">.</mi><mi mathvariant="normal">.</mi><mi mathvariant="normal">.</mi></mrow><annotation encoding="application/x-tex">...</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.1056em;"></span><span class="mord">...</span></span></span></span><span>包裹起来。</span></p><p class="ds-markdown-paragraph"><span>好，我大致知道怎么转换了。我会保持原文档的结构和内容，只是用markdown的语法重新组织一下，让它在markdown环境下更易读。</span></p></blockquote><br/><div class="md-code-block md-code-block-light"><div class="md-code-block-banner-wrap"><div class="md-code-block-banner md-code-block-banner-lite"><div class="_121d384"><div class="d2a24f03"><span class="d813de27">markdown</span></div><div class="d2a24f03 _246a029"><div class="efa13877"><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon" style="margin-right: 4px;"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.14923 4.02032C7.11191 4.02032 7.87977 4.02017 8.49591 4.07599C9.12122 4.1327 9.65786 4.25188 10.1414 4.53107C10.7201 4.8653 11.2008 5.34591 11.535 5.92462C11.8142 6.40818 11.9333 6.94482 11.9901 7.57013C12.0459 8.18625 12.0457 8.9542 12.0457 9.91681C12.0457 10.8795 12.0459 11.6474 11.9901 12.2635C11.9333 12.8888 11.8142 13.4254 11.535 13.909C11.2008 14.4877 10.7201 14.9683 10.1414 15.3026C9.65786 15.5817 9.12122 15.7009 8.49591 15.7576C7.87977 15.8134 7.1119 15.8133 6.14923 15.8133C5.18661 15.8133 4.41868 15.8134 3.80255 15.7576C3.17724 15.7009 2.6406 15.5817 2.15704 15.3026C1.57834 14.9684 1.09772 14.4877 0.763489 13.909C0.484305 13.4254 0.365123 12.8888 0.308411 12.2635C0.252587 11.6474 0.252747 10.8795 0.252747 9.91681C0.252747 8.95419 0.252603 8.18625 0.308411 7.57013C0.365123 6.94482 0.484305 6.40818 0.763489 5.92462C1.09771 5.3459 1.57833 4.86529 2.15704 4.53107C2.6406 4.25188 3.17724 4.1327 3.80255 4.07599C4.41868 4.02018 5.1866 4.02032 6.14923 4.02032ZM6.14923 5.37775C5.16175 5.37775 4.46628 5.37761 3.9256 5.42657C3.39428 5.47473 3.07853 5.56574 2.83575 5.70587C2.46313 5.92106 2.15348 6.23071 1.93829 6.60333C1.79817 6.84611 1.70715 7.16185 1.659 7.69318C1.61004 8.23385 1.61017 8.92934 1.61017 9.91681C1.61017 10.9043 1.61002 11.5998 1.659 12.1404C1.70715 12.6717 1.79817 12.9875 1.93829 13.2303C2.15349 13.6029 2.46315 13.9126 2.83575 14.1277C3.07853 14.2679 3.39428 14.3589 3.9256 14.407C4.46628 14.456 5.16176 14.4559 6.14923 14.4559C7.13675 14.4559 7.83218 14.456 8.37286 14.407C8.90419 14.3589 9.21993 14.2679 9.46271 14.1277C9.83529 13.9126 10.145 13.6029 10.3602 13.2303C10.5003 12.9875 10.5913 12.6718 10.6395 12.1404C10.6884 11.5998 10.6883 10.9043 10.6883 9.91681C10.6883 8.92935 10.6884 8.23385 10.6395 7.69318C10.5913 7.16185 10.5003 6.84611 10.3602 6.60333C10.145 6.23072 9.8353 5.92107 9.46271 5.70587C9.21993 5.56574 8.90418 5.47473 8.37286 5.42657C7.83218 5.3776 7.13676 5.37775 6.14923 5.37775ZM9.80157 0.367981C10.7637 0.367981 11.5313 0.367886 12.1473 0.423645C12.7725 0.480313 13.3093 0.598765 13.7928 0.877747C14.3716 1.21192 14.852 1.69355 15.1863 2.27228C15.4655 2.75575 15.5857 3.29165 15.6424 3.91681C15.6982 4.53301 15.6971 5.30161 15.6971 6.26447V7.8299C15.6971 8.29265 15.6989 8.58994 15.6649 8.84845C15.4667 10.3525 14.4009 11.5738 12.9832 11.9988V10.5467C13.6973 10.1903 14.2104 9.49662 14.3192 8.67169C14.3387 8.52348 14.3406 8.3358 14.3406 7.8299V6.26447C14.3406 5.27707 14.3398 4.58149 14.2908 4.04083C14.2427 3.50969 14.1526 3.19373 14.0125 2.95099C13.7974 2.5785 13.4875 2.2687 13.1151 2.05353C12.8723 1.91347 12.5563 1.82237 12.0252 1.77423C11.4846 1.72528 10.7888 1.7254 9.80157 1.7254H7.71466C6.75614 1.72559 5.92659 2.27697 5.52325 3.07892H4.07013C4.54215 1.51132 5.99314 0.368192 7.71466 0.367981H9.80157Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">复制</span></span><div class="ds-focus-ring"></div></button><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M15.3695 11.411L15.1234 12.8866C14.8869 14.3042 13.6603 15.3436 12.223 15.3436H3.7767C2.33954 15.3434 1.11276 14.3042 0.876312 12.8866L0.630219 11.411L2.05405 11.1747L2.29916 12.6493C2.41969 13.3713 3.04472 13.9001 3.7767 13.9003H12.223C12.9551 13.9002 13.58 13.3713 13.7005 12.6493L13.9456 11.1747L15.3695 11.411ZM8.72202 8.994C8.77714 8.93934 8.83789 8.88106 8.90268 8.81627L12.4828 5.23424L13.5042 6.25572L9.92221 9.8358C9.63947 10.1185 9.3876 10.3732 9.15854 10.5575C8.91889 10.7503 8.6395 10.9224 8.28647 10.9784C8.09708 11.0083 7.9036 11.0083 7.7142 10.9784C7.36103 10.9224 7.08087 10.7503 6.84116 10.5575C6.61212 10.3732 6.36019 10.1185 6.07748 9.8358L2.49643 6.25572L3.51694 5.23424L7.09702 8.81627C7.16216 8.88142 7.22327 8.94006 7.27866 8.99498V1.3065H8.72202V8.994Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">下载</span></span><div class="ds-focus-ring"></div></button></div></div></div></div></div><pre><span class="token title important"><span class="token punctuation">#</span> Computer Vision: Homework 2</span>

<span class="token bold"><span class="token punctuation">**</span><span class="token content">Due on December 29, 2025 at 23:59</span><span class="token punctuation">**</span></span>  
<span class="token italic"><span class="token punctuation">_</span><span class="token content">Fall 2025</span><span class="token punctuation">_</span></span>

<span class="token hr punctuation">---</span>

<span class="token title important"><span class="token punctuation">##</span> Programming Assignment (85 points)</span>

In this assignment, you will implement a Bag-of-Visual-Words (BoW) image classification pipeline on the provided image dataset (Caltech-101). You are given a Python skeleton file <span class="token code-snippet code keyword">`hw.py`</span>. You should only modify the parts marked with <span class="token code-snippet code keyword">`# TODO`</span>. Do not change any function signatures.

<span class="token bold"><span class="token punctuation">**</span><span class="token content">You are allowed to use:</span><span class="token punctuation">**</span></span>

<span class="token list punctuation">-</span> Python, NumPy
<span class="token list punctuation">-</span> OpenCV SIFT implementation (<span class="token code-snippet code keyword">`cv2.SIFT_create`</span>, <span class="token code-snippet code keyword">`detectAndCompute`</span>, <span class="token code-snippet code keyword">`cv2.imread`</span>, <span class="token code-snippet code keyword">`cv2.cvtColor`</span>, etc.)
<span class="token list punctuation">-</span> <span class="token code-snippet code keyword">`sklearn.cluster.KMeans`</span> or your own k‑means implementation
<span class="token list punctuation">-</span> <span class="token code-snippet code keyword">`sklearn.svm.LinearSVC`</span> for classification

<span class="token hr punctuation">---</span>

<span class="token title important"><span class="token punctuation">###</span> Task 0: Extract SIFT descriptors from the dataset (20 points)</span>

Using images in the Caltech-101 dataset (<span class="token url">[<span class="token content">download link</span>](<span class="token url">https://www.kaggle.com/datasets/imbikramsaha/caltech-101</span>)</span>), implement the function <span class="token code-snippet code keyword">`extract_sift_features`</span> in <span class="token code-snippet code keyword">`hw.py`</span>, which should:

<span class="token list punctuation">-</span> Read each image in grayscale using OpenCV.
<span class="token list punctuation">-</span> Detect and compute SIFT keypoints and descriptors using the official SIFT implementation.
<span class="token list punctuation">-</span> Collect all descriptors into a single NumPy array of shape \((N,128)\).
<span class="token list punctuation">-</span> Also return a list where each element contains the descriptors for a single image.

<span class="token italic"><span class="token punctuation">*</span><span class="token content">If an image has no detected keypoints, you may skip it or handle it in a reasonable way (e.g., return an all‑zero histogram later).</span><span class="token punctuation">*</span></span>

<span class="token hr punctuation">---</span>

<span class="token title important"><span class="token punctuation">###</span> Task 1: Build a visual vocabulary with k‑means (25 points)</span>

Using all SIFT descriptors from Task 0, implement <span class="token code-snippet code keyword">`build_codebook(descriptors, K)`</span> in <span class="token code-snippet code keyword">`hw.py`</span> that:

<span class="token list punctuation">-</span> Takes a NumPy array of shape \((N,128)\) containing all SIFT descriptors as input.
<span class="token list punctuation">-</span> Runs k‑means clustering with \(K\) clusters to obtain the visual vocabulary.
<span class="token list punctuation">-</span> Returns the cluster centers as a matrix of shape \((K,128)\) (each row is one visual word).

You may use <span class="token code-snippet code keyword">`sklearn.cluster.KMeans`</span> or your own k‑means implementation.

<span class="token hr punctuation">---</span>

<span class="token title important"><span class="token punctuation">###</span> Task 2: BoW histogram for a single image (20 points)</span>

Implement <span class="token code-snippet code keyword">`compute_bow_histogram(descriptors, codebook)`</span> that:

<span class="token list punctuation">-</span> Assigns each SIFT descriptor of an image to its nearest visual word (e.g., using Euclidean distance).
<span class="token list punctuation">-</span> Counts how many descriptors fall into each of the \(K\) clusters to form a histogram.
<span class="token list punctuation">-</span> Normalizes the histogram to sum to 1.

The function should return a 1D NumPy array of shape \((K,)\).

<span class="token hr punctuation">---</span>

<span class="token title important"><span class="token punctuation">###</span> Task 3: Train and evaluate a linear SVM (20 points)</span>

Using the BoW histograms:

<span class="token list punctuation">-</span> Implement <span class="token code-snippet code keyword">`build_features_for_dataset(...)`</span> to compute a BoW feature for each image in the training and test splits.
<span class="token list punctuation">-</span> Train a linear SVM classifier using the training features and labels (you may use <span class="token code-snippet code keyword">`sklearn.svm.LinearSVC`</span>).
<span class="token list punctuation">-</span> Evaluate the classification accuracy on the test set.

<span class="token bold"><span class="token punctuation">**</span><span class="token content">Report the final accuracy in your PDF report.</span><span class="token punctuation">**</span></span>

<span class="token hr punctuation">---</span>

<span class="token title important"><span class="token punctuation">##</span> Written Assignment (15 points)</span>

<span class="token list punctuation">1.</span> A camera moves with translational velocity \(T=(T_x,T_y,T_z)\) and no rotation. A 3D point \(P=(X,Y,Z)\) projects to image coordinates:
   \[
   x=\frac{fX}{Z},\qquad y=\frac{fY}{Z}.
   \]
   Its motion field is given by:
   \[
   v_x=\frac{fV_x-V_z x}{Z},\qquad v_y=\frac{fV_y-V_z y}{Z},
   \]
   where \(V=-T\). For two scene points \(P_1\) and \(P_2\) located at the same image position \((x,y)\) but with depths \(Z_1 \neq Z_2\), derive the ratio \(\frac{\|v(P_1)\|}{\|v(P_2)\|}\) in terms of \(Z_1\) and \(Z_2\).

<span class="token list punctuation">2.</span> Under brightness constancy, the optical flow \((u,v)\) satisfies the constraint \(I_x u + I_y v + I_t = 0\). At a pixel, assume \(I_x = a\), \(I_y = b\), and \(I_t = c\). Write the complete set of \((u,v)\) satisfying:
   \[
   au + bv + c = 0,
   \]
   and express this solution set as the parametric equation of a line in the \((u,v)\) space.</pre><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _33882ae"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _28d7e84"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg></div>

