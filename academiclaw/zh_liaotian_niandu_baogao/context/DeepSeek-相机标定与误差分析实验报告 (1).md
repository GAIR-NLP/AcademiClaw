### 用户

\documentclass[UTF8]{ctexart}

%=================================================
% 导入所需宏包
%=================================================
\usepackage{amsmath}          % AMS数学公式环境
\usepackage{amssymb}          % AMS数学符号
\usepackage{amsfonts}         % AMS数学字体
\usepackage[a4paper, margin=1in]{geometry} % 设置页面边距
\usepackage{hyperref}         % 创建超链接
\usepackage[UTF8]{ctex}
\usepackage{amsmath,amssymb}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{listings}
\usepackage{xcolor}
\usepackage{geometry}
\usepackage{float}
\usepackage{caption}

\geometry{left=2.5cm,right=2.5cm,top=2.5cm,bottom=2.5cm}

\lstset{
    language=Python,
    basicstyle=\ttfamily\small,
    keywordstyle=\color{blue},
    commentstyle=\color{green!60!black},
    stringstyle=\color{orange},
    numbers=left,
    numberstyle=\tiny\color{gray},
    frame=single,
    breaklines=true,
    showstringspaces=false,
    tabsize=4
}
%=================================================
% 定义一些常用命令
%=================================================
% 定义粗体向量和矩阵命令
\newcommand{\bvec}[1]{\boldsymbol{#1}}
\newcommand{\bmat}[1]{\boldsymbol{#1}}

%=================================================
% 文档开始
%=================================================
\begin{document}

%=================================================
% 标题部分
%=================================================
\title{计算机视觉：第二次作业}
\author{黄逸隽 523030910202}
\date{截止日期：2025年12月1日}
\maketitle

\hrule\vspace{1em}

%=================================================
% 问题与解答
%=================================================
\section*{书面作业 }

\subsection*{问题 1}
\noindent\textbf{证明：}

我们的目标是找到使误差函数 \(E(\bmat{A}, \bvec{T})\) 最小的 \(\bmat{A}\) 和 \(\bvec{T}\)，我们通过将 \(E(\bmat{A}, \bvec{T})\) 对 \(\bmat{A}\) 和 \(\bvec{T}\) 的偏导数设为零来求解。

\paragraph{1. 对 \(\bvec{T}\) 求偏导}
首先，我们计算 \(E\) 关于 \(\bvec{T}\) 的偏导数：
\[ \frac{\partial E}{\partial \bvec{T}} = \frac{\partial}{\partial \bvec{T}} \sum_{i=1}^{N} (\bvec{Y}_i - \bmat{A}\bvec{X}_i - \bvec{T})^T (\bvec{Y}_i - \bmat{A}\bvec{X}_i - \bvec{T}) \]
使用向量求导法则 \(\frac{\partial}{\partial \bvec{x}} (\bvec{v} - \bvec{x})^T(\bvec{v} - \bvec{x}) = -2(\bvec{v} - \bvec{x})\)，我们得到：
\[ \frac{\partial E}{\partial \bvec{T}} = \sum_{i=1}^{N} -2 (\bvec{Y}_i - \bmat{A}\bvec{X}_i - \bvec{T}) \]
令偏导数为零向量 \(\bvec{0}\)：
\[ \sum_{i=1}^{N} (\bvec{Y}_i - \bmat{A}\bvec{X}_i - \bvec{T}) = \bvec{0} \]
\[ \sum_{i=1}^{N} \bvec{Y}_i - \bmat{A} \sum_{i=1}^{N} \bvec{X}_i - \sum_{i=1}^{N} \bvec{T} = \bvec{0} \]
根据质心 \(\bar{\bvec{X}}\) 和 \(\bar{\bvec{Y}}\) 的定义，上式可以写为：
\[ N\bar{\bvec{Y}} - \bmat{A} (N\bar{\bvec{X}}) - N\bvec{T} = \bvec{0} \]
两边同除以 \(N\)，我们得到最优 \(\bvec{T}^*\) 和最优 \(\bmat{A}^*\) 之间的关系：
\begin{equation} \label{eq:T_star}
\bvec{T}^* = \bar{\bvec{Y}} - \bmat{A}^*\bar{\bvec{X}}
\end{equation}
这证明了第一个公式。

\paragraph{2. 对 \(\bmat{A}\) 求偏导}
现在，我们将式 \eqref{eq:T_star} 的关系代入原始误差函数 \(E\) 中，以消除 \(\bvec{T}\)。
\[
\begin{aligned}
E(\bmat{A}) &= \sum_{i=1}^{N} \|\bvec{Y}_i - \bmat{A}\bvec{X}_i - (\bar{\bvec{Y}} - \bmat{A}\bar{\bvec{X}})\|_2^2 \\
&= \sum_{i=1}^{N} \|(\bvec{Y}_i - \bar{\bvec{Y}}) - \bmat{A}(\bvec{X}_i - \bar{\bvec{X}})\|_2^2
\end{aligned}
\]
我们定义中心化坐标：\(\bvec{y}_i = \bvec{Y}_i - \bar{\bvec{Y}}\) 和 \(\bvec{x}_i = \bvec{X}_i - \bar{\bvec{X}}\)。误差函数简化为：
\[ E(\bmat{A}) = \sum_{i=1}^{N} \|\bvec{y}_i - \bmat{A}\bvec{x}_i\|_2^2 \]
现在，我们引入题目中定义的 \(3 \times N\) 矩阵 \(\mathcal{X} = [\bvec{x}_1, \dots, \bvec{x}_N]\) 和 \(\mathcal{Y} = [\bvec{y}_1, \dots, \bvec{y}_N]\)。误差函数可以写成矩阵的 Frobenius 范数形式：
\[ E(\bmat{A}) = \|\mathcal{Y} - \bmat{A}\mathcal{X}\|_F^2 \]
使用迹（trace）的性质，\(\|\bmat{M}\|_F^2 = \text{tr}(\bmat{M}^T\bmat{M})\)，我们有：
\[
\begin{aligned}
E(\bmat{A}) &= \text{tr}((\mathcal{Y} - \bmat{A}\mathcal{X})^T (\mathcal{Y} - \bmat{A}\mathcal{X})) \\
&= \text{tr}(\mathcal{Y}^T\mathcal{Y} - \mathcal{Y}^T\bmat{A}\mathcal{X} - \mathcal{X}^T\bmat{A}^T\mathcal{Y} + \mathcal{X}^T\bmat{A}^T\bmat{A}\mathcal{X})
\end{aligned}
\]
现在计算 \(E\) 关于 \(\bmat{A}\) 的偏导数。使用矩阵求导法则 \(\frac{\partial}{\partial \bmat{A}} \text{tr}(\bmat{B}\bmat{A}) = \bmat{B}^T\)，\(\frac{\partial}{\partial \bmat{A}} \text{tr}(\bmat{B}\bmat{A}^T\bmat{C}) = \bmat{C}\bmat{B}\) 和 \(\frac{\partial}{\partial \bmat{A}} \text{tr}(\bmat{B}^T\bmat{A}^T\bmat{C}\bmat{A}) = \bmat{C}\bmat{A}\bmat{B}^T + \bmat{C}^T\bmat{A}\bmat{B}\)：
\[ \frac{\partial E}{\partial \bmat{A}} = -2\mathcal{Y}\mathcal{X}^T + 2\bmat{A}\mathcal{X}\mathcal{X}^T \]
（注：展开式中的 \(\text{tr}(\mathcal{Y}^T\bmat{A}\mathcal{X})\) 和 \(\text{tr}(\mathcal{X}^T\bmat{A}^T\mathcal{Y})\) 是相等的标量，它们的和对 \(\bmat{A}\) 的导数是 \(2(\mathcal{Y}\mathcal{X}^T)^T = 2\mathcal{X}\mathcal{Y}^T\) ，然而从整个表达式来看，更直接的求导方式是得到 \(-2\mathcal{Y}\mathcal{X}^T\)。为保持一致性，我们直接对 Frobenius 范数求导。）

令偏导数为零矩阵 \(\bmat{0}\)：
\[ -2\mathcal{Y}\mathcal{X}^T + 2\bmat{A}\mathcal{X}\mathcal{X}^T = \bmat{0} \]
\[ \bmat{A}(\mathcal{X}\mathcal{X}^T) = \mathcal{Y}\mathcal{X}^T \]
假设矩阵 \(\mathcal{X}\mathcal{X}^T\) 是可逆的（这要求中心化的点集 \(\{\bvec{x}_i\}\) 不是共面或共线的），我们可以在等式右侧乘以其逆矩阵：
\[ \bmat{A}^* = (\mathcal{Y}\mathcal{X}^T)(\mathcal{X}\mathcal{X}^T)^{-1} \]
这证明了第二个公式。
\hfill \(\blacksquare\)

\vspace{2em}

\subsubsection*{(b) 证明}
证明估计该变换需要的最少对应点数量是4。
\vspace{1em}

\noindent\textbf{证明：}

我们通过分析变换中的未知数数量和每个点对应提供的约束数量来确定最少需要的点数。

\paragraph{1. 未知数数量}
变换 \((\bmat{A}, \bvec{T})\) 包含两个部分：
\begin{itemize}
    \item 旋转/缩放/错切矩阵 \(\bmat{A} \in \mathbb{R}^{3\times3}\)，包含 \(3 \times 3 = 9\) 个未知参数。
    \item 平移向量 \(\bvec{T} \in \mathbb{R}^3\)，包含 \(3 \times 1 = 3\) 个未知参数。
\end{itemize}
因此，总共有 \(9 + 3 = 12\) 个独立的未知参数需要求解。

\paragraph{2. 每组对应点提供的约束数量}
每一组对应点 \((\bvec{X}_i, \bvec{Y}_i)\) 提供一个矢量方程：
\[ \bvec{Y}_i = \bmat{A}\bvec{X}_i + \bvec{T} \]
这个方程是在 \(\mathbb{R}^3\) 空间中的，它可以分解为3个独立的标量方程：
\[
\begin{cases}
y_{i1} = a_{11}x_{i1} + a_{12}x_{i2} + a_{13}x_{i3} + t_1 \\
y_{i2} = a_{21}x_{i1} + a_{22}x_{i2} + a_{23}x_{i3} + t_2 \\
y_{i3} = a_{31}x_{i1} + a_{32}x_{i2} + a_{33}x_{i3} + t_3
\end{cases}
\]
所以，每一组对应点能够提供3个线性方程。

\paragraph{3. 求解所需的最少点数}
为了唯一地确定所有12个未知参数，我们需要的独立方程数量必须至少等于未知数的数量。设 \(N\) 为所需的最少对应点数量，则：
\[ \text{总方程数} \ge \text{总未知数} \]
\[ 3N \ge 12 \]
\[ N \ge 4 \]
因此，我们至少需要4组对应点。

\paragraph{4. 唯一解的条件}
拥有 \(N=4\) 组点只是一个必要条件，不是充分条件。为了得到唯一解，这些方程必须是线性无关的。从(a)部分的推导中，我们知道 \(\bmat{A}^*\) 的解为 \(\bmat{A}^* = (\mathcal{Y}\mathcal{X}^T)(\mathcal{X}\mathcal{X}^T)^{-1}\)。这个解存在的关键在于矩阵 \(\mathcal{X}\mathcal{X}^T\) 是可逆的。

矩阵 \(\mathcal{X}\mathcal{X}^T\) 是一个 \(3 \times 3\) 的矩阵，定义为 \(\sum_{i=1}^N \bvec{x}_i \bvec{x}_i^T\)，其中 \(\bvec{x}_i = \bvec{X}_i - \bar{\bvec{X}}\)。
为了使 \(\mathcal{X}\mathcal{X}^T\) 可逆，它的秩必须是3。这意味着由中心化向量 \(\{\bvec{x}_1, \dots, \bvec{x}_N\}\) 张成的子空间维度必须是3。
\begin{itemize}
    \item 如果 \(N < 4\)，例如 \(N=3\)，三个点 \(\bvec{X}_1, \bvec{X}_2, \bvec{X}_3\) 最多是共面的（通常是，除非它们共线）。它们的中心化向量 \(\bvec{x}_1, \bvec{x}_2, \bvec{x}_3\) 也将位于一个过原点的平面上，因此它们张成的空间维度最多为2，导致 \(\mathcal{X}\mathcal{X}^T\) 是奇异的。
    \item 如果 \(N=4\)，并且这4个点 \(\bvec{X}_1, \dots, \bvec{X}_4\) 是 \textbf{共面（coplanar）}的，那么它们的中心化向量 \(\{\bvec{x}_i\}\) 也将位于一个过原点的平面上。这样，它们张成的空间维度仍然是2，\(\mathcal{X}\mathcal{X}^T\) 依然是奇异的。
\end{itemize}
因此，为了保证 \(\mathcal{X}\mathcal{X}^T\) 满秩（秩为3），我们不仅需要 \(N \ge 4\)，还要求这4个点 \(\bvec{X}_1, \dots, \bvec{X}_4\) \textbf{不能共面（non-coplanar）}。当这4个点不共面时，它们构成的中心化向量可以张成整个 \(\mathbb{R}^3\) 空间，保证了 \(\mathcal{X}\mathcal{X}^T\) 的可逆性，从而可以唯一确定 \(\bmat{A}\) 和 \(\bvec{T}\)。

\textbf{结论：} 估计该3D仿射变换所需的最少对应点数量是4，并且这4个源点 \(\{\bvec{X}_i\}\) 不能共面。
\hfill \(\blacksquare\)

\section*{编程任务}
\section{任务简要说明}

\subsection{实验目标}
本次实验的目标是完成相机标定，通过一系列棋盘格图像推导出相机的内参矩阵，包括：
\begin{itemize}
    \item 焦距 $(f_x, f_y)$
    \item 主点坐标 $(c_x, c_y)$
    \item 每张图像对应的重投影误差
\end{itemize}

\subsection{标定流程}
标准的相机标定流程如下：
\begin{enumerate}
    \item 使用已知尺寸的棋盘格图案定义3D点的世界坐标
    \item 从不同视角拍摄棋盘格图像
    \item 检测棋盘格角点，获取每个3D点在不同图像中的像素坐标 $(u, v)$
    \item 使用线性代数方法求解相机参数
\end{enumerate}

\subsection{实验要求}
\begin{itemize}
    \item 只允许使用基本的 Python、NumPy 和 OpenCV 函数
    \item 允许使用 \texttt{cv2.findChessboardCorners} 等角点检测函数
    \item 不允许使用 \texttt{cv2.calibrateCamera} 等"魔法"函数求解内参（仅用于验证）
    \item 世界坐标可简化为 $(0,0), (1,0), (2,0), \ldots$，结果以棋盘格方格大小为单位
\end{itemize}

\section{核心实现说明}

\subsection{世界坐标点初始化}
棋盘格的世界坐标点定义在 $Z=0$ 的平面上，坐标按 $(0,0,0), (1,0,0), (2,0,0), \ldots$ 的方式排列：

\begin{lstlisting}
def init_world_points(pattern_size):
    # 生成棋盘格的世界坐标
    # 点排列为 (0,0,0), (1,0,0), (2,0,0), ... 在XY平面上 (Z=0)
    objp = np.zeros((pattern_size[0] * pattern_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2)
    return objp
\end{lstlisting}

\subsection{棋盘格角点检测}
本实验测试了两种角点检测方法：

\subsubsection{方法一：findChessboardCorners（传统方法）}
使用 OpenCV 的传统 \texttt{findChessboardCorners} 函数，并通过 \texttt{cornerSubPix} 进行亚像素精度优化：

\begin{lstlisting}
def detect_corners(image, pattern_size):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)
    if ret:
        # 亚像素精度优化
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        return corners.reshape(-1, 2)
    return None
\end{lstlisting}

\subsubsection{方法二：findChessboardCornersSB（基于扇区方法）}
使用 OpenCV 4.0+ 引入的 \texttt{findChessboardCornersSB} 函数（SB = Sector Based），该方法更加鲁棒：

\begin{lstlisting}
def detect_corners(image, pattern_size):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCornersSB(gray, pattern_size)
    if ret:
        return corners.reshape(-1, 2)
    return None
\end{lstlisting}

\subsubsection{两种方法对比}
\begin{table}[H]
\centering
\caption{两种角点检测方法对比}
\begin{tabular}{lcc}
\toprule
\textbf{特性} & \textbf{findChessboardCorners} & \textbf{findChessboardCornersSB} \\
\midrule
成功检测图像数 & 5/25 & 19/25 \\
对图像质量要求 & 高 & 低 \\
对棋盘格角度要求 & 严格 & 宽松 \\
处理模糊图像 & 较差 & 较好 \\
OpenCV版本要求 & 所有版本 & 4.0+ \\
\bottomrule
\end{tabular}
\end{table}

\subsection{单应性矩阵计算}
使用直接线性变换（DLT）算法计算每张图像的单应性矩阵 $\mathbf{H}$：

对于世界坐标 $(X, Y)$ 和图像坐标 $(u, v)$，有：
\begin{equation}
    \begin{bmatrix} u \\ v \\ 1 \end{bmatrix} \sim \mathbf{H} \begin{bmatrix} X \\ Y \\ 1 \end{bmatrix}
\end{equation}

构建方程组 $\mathbf{A}\mathbf{h} = \mathbf{0}$，使用 SVD 求解：

\begin{lstlisting}
def compute_homography(world_pts, image_pts):
    num_pts = world_pts.shape[0]
    A_h = []
    
    for i in range(num_pts):
        X, Y = world_pts[i, 0], world_pts[i, 1]
        u, v = image_pts[i, 0], image_pts[i, 1]
        
        # 每个点提供2个方程
        A_h.append([-X, -Y, -1, 0, 0, 0, u*X, u*Y, u])
        A_h.append([0, 0, 0, -X, -Y, -1, v*X, v*Y, v])
    
    A_h = np.array(A_h)
    
    # 使用SVD求解 Ah = 0
    _, _, Vt = np.linalg.svd(A_h)
    H = Vt[-1].reshape(3, 3)
    H = H / H[2, 2]  # 归一化
    
    return H
\end{lstlisting}

\subsection{张正友标定法求解内参}
使用张正友标定法，通过多张图像的单应性矩阵求解相机内参。

\subsubsection{构建约束矩阵}
定义向量 $\mathbf{v}_{ij}$：
\begin{equation}
    \mathbf{v}_{ij} = \begin{bmatrix}
        h_{1i}h_{1j} \\
        h_{1i}h_{2j} + h_{2i}h_{1j} \\
        h_{2i}h_{2j} \\
        h_{3i}h_{1j} + h_{1i}h_{3j} \\
        h_{3i}h_{2j} + h_{2i}h_{3j} \\
        h_{3i}h_{3j}
    \end{bmatrix}
\end{equation}

\begin{lstlisting}
def compute_v_ij(H, i, j):
    return np.array([
        H[0, i] * H[0, j],
        H[0, i] * H[1, j] + H[1, i] * H[0, j],
        H[1, i] * H[1, j],
        H[2, i] * H[0, j] + H[0, i] * H[2, j],
        H[2, i] * H[1, j] + H[1, i] * H[2, j],
        H[2, i] * H[2, j]
    ])
\end{lstlisting}

\subsubsection{求解内参矩阵}
根据约束条件 $\mathbf{h}_1^T \mathbf{B} \mathbf{h}_2 = 0$ 和 $\mathbf{h}_1^T \mathbf{B} \mathbf{h}_1 = \mathbf{h}_2^T \mathbf{B} \mathbf{h}_2$，构建矩阵 $\mathbf{V}$：

\begin{lstlisting}
# 构建V矩阵
V = []
for H in homographies:
    v12 = compute_v_ij(H, 0, 1)
    v11 = compute_v_ij(H, 0, 0)
    v22 = compute_v_ij(H, 1, 1)
    
    V.append(v12)
    V.append(v11 - v22)

V = np.array(V)

# 使用SVD求解 Vb = 0
_, _, Vt = np.linalg.svd(V)
b = Vt[-1]
\end{lstlisting}

从 $\mathbf{B} = \mathbf{K}^{-T}\mathbf{K}^{-1}$ 中提取内参：

\begin{lstlisting}
B11, B12, B22, B13, B23, B33 = b

# 计算内参
v0 = (B12 * B13 - B11 * B23) / (B11 * B22 - B12 * B12)
lambda_ = B33 - (B13 * B13 + v0 * (B12 * B13 - B11 * B23)) / B11
fx = np.sqrt(abs(lambda_ / B11))
fy = np.sqrt(abs(lambda_ * B11 / (B11 * B22 - B12 * B12)))
s = -B12 * fx * fx * fy / lambda_
u0 = s * v0 / fy - B13 * fx * fx / lambda_

# 构建内参矩阵 K
K = np.array([
    [fx, s, u0],
    [0, fy, v0],
    [0, 0, 1]
])
\end{lstlisting}

\section{实验结果}

\subsection{数据集信息}
\begin{itemize}
    \item 图像总数：25 张
    \item 棋盘格内角点尺寸：$31 \times 23 = 713$ 个点
\end{itemize}

\subsection{方法一结果：findChessboardCorners（传统方法）}

\subsubsection{检测信息}
\begin{itemize}
    \item 成功检测棋盘格：5 张
    \item 总检测角点数：$5 \times 713 = 3565$ 个点
\end{itemize}

\subsubsection{相机内参结果}

\begin{table}[H]
\centering
\caption{方法一：相机内参标定结果}
\begin{tabular}{lcc}
\toprule
\textbf{参数} & \textbf{本实验结果} & \textbf{OpenCV验证结果} \\
\midrule
焦距 $f_x$ & 910.4592 & -- \\
焦距 $f_y$ & 857.4488 & -- \\
主点 $c_x$ & 533.0859 & -- \\
主点 $c_y$ & 278.5895 & -- \\
倾斜因子 $s$ & 4.5027 & 0 \\
\bottomrule
\end{tabular}
\end{table}

内参矩阵 $\mathbf{K}$（方法一）：
\begin{equation}
    \mathbf{K}_1 = \begin{bmatrix}
        910.4592 & 4.5027 & 533.0859 \\
        0 & 857.4488 & 278.5895 \\
        0 & 0 & 1
    \end{bmatrix}
\end{equation}

\subsubsection{重投影误差}

\begin{table}[H]
\centering
\caption{方法一：每张图像的重投影误差}
\begin{tabular}{cc}
\toprule
\textbf{图像} & \textbf{误差 (pixels)} \\
\midrule
Image 1 & 4.3246 \\
Image 2 & 1.9470 \\
Image 3 & 2.6697 \\
Image 4 & 4.4122 \\
Image 5 & 5.3769 \\
\bottomrule
\end{tabular}
\end{table}

\textbf{误差统计（方法一）：}
\begin{itemize}
    \item 最小误差：1.9470 像素 (Image 2)
    \item 最大误差：5.3769 像素 (Image 5)
    \item 平均误差：约 3.75 像素
\end{itemize}

\subsection{方法二结果：findChessboardCornersSB（基于扇区方法）}

\subsubsection{检测信息}
\begin{itemize}
    \item 成功检测棋盘格：19 张
    \item 总检测角点数：$19 \times 713 = 13547$ 个点
\end{itemize}

\subsubsection{相机内参结果}

\begin{table}[H]
\centering
\caption{方法二：相机内参标定结果}
\begin{tabular}{lcc}
\toprule
\textbf{参数} & \textbf{本实验结果} & \textbf{OpenCV验证结果} \\
\midrule
焦距 $f_x$ & 832.4417 & 748.3523 \\
焦距 $f_y$ & 787.1441 & 699.0632 \\
主点 $c_x$ & 498.2376 & 449.5306 \\
主点 $c_y$ & 334.6547 & 342.4280 \\
倾斜因子 $s$ & -6.0127 & 0 \\
\bottomrule
\end{tabular}
\end{table}

内参矩阵 $\mathbf{K}$（方法二）：
\begin{equation}
    \mathbf{K}_2 = \begin{bmatrix}
        832.4417 & -6.0127 & 498.2376 \\
        0 & 787.1441 & 334.6547 \\
        0 & 0 & 1
    \end{bmatrix}
\end{equation}

\subsubsection{重投影误差}

\begin{table}[H]
\centering
\caption{方法二：每张图像的重投影误差}
\begin{tabular}{cc|cc}
\toprule
\textbf{图像} & \textbf{误差 (pixels)} & \textbf{图像} & \textbf{误差 (pixels)} \\
\midrule
Image 1 & 0.3116 & Image 11 & 1.6500 \\
Image 2 & 0.3924 & Image 12 & 1.5848 \\
Image 3 & 0.2388 & Image 13 & 1.7768 \\
Image 4 & 0.2583 & Image 14 & 1.8660 \\
Image 5 & 0.2467 & Image 15 & 5.3673 \\
Image 6 & 0.3047 & Image 16 & 1.4325 \\
Image 7 & 0.5164 & Image 17 & 0.6437 \\
Image 8 & 0.1832 & Image 18 & 0.3850 \\
Image 9 & 0.2719 & Image 19 & 0.5222 \\
Image 10 & 1.9801 & & \\
\bottomrule
\end{tabular}
\end{table}

\textbf{误差统计（方法二）：}
\begin{itemize}
    \item 最小误差：0.1832 像素 (Image 8)
    \item 最大误差：5.3673 像素 (Image 15)
    \item 大部分图像误差在 0.2 - 0.6 像素之间
\end{itemize}

\subsection{两种方法结果对比}

\begin{table}[H]
\centering
\caption{两种方法标定结果综合对比}
\begin{tabular}{lccc}
\toprule
\textbf{指标} & \textbf{方法一} & \textbf{方法二} & \textbf{评价} \\
\midrule
检测图像数 & 5 & 19 & 方法二更多 \\
焦距 $f_x$ & 910.46 & 832.44 & -- \\
焦距 $f_y$ & 857.45 & 787.14 & -- \\
主点 $c_x$ & 533.09 & 498.24 & 方法二更接近图像中心 \\
主点 $c_y$ & 278.59 & 334.65 & 方法二更接近图像中心 \\
平均重投影误差 & $\sim$3.75 px & $\sim$1.05 px & 方法二更小 \\
\bottomrule
\end{tabular}
\end{table}

\textbf{注：}图像尺寸为 $964 \times 686$，图像中心约为 $(482, 343)$。

\section{结果分析}

\subsection{两种角点检测方法分析}
\begin{enumerate}
    \item \textbf{方法一（findChessboardCorners）}：传统方法，对图像质量要求较高，只能检测到5张图像，导致标定数据量较少，结果稳定性较差。
    \item \textbf{方法二（findChessboardCornersSB）}：基于扇区的方法，更加鲁棒，能检测到19张图像，数据量充足，标定结果更加可靠。
\end{enumerate}

\subsection{内参对比分析}
本实验结果与 OpenCV 验证结果存在一定差异，主要原因如下：
\begin{enumerate}
    \item OpenCV 的 \texttt{calibrateCamera} 函数会同时估计畸变参数并进行非线性优化
    \item 本实验使用的是线性方法（张正友标定法），未考虑镜头畸变
    \item 主点位置的估计对噪声较为敏感
    \item 方法一由于数据量少（仅5张图像），结果受噪声影响更大
\end{enumerate}

\subsection{重投影误差分析}
\begin{itemize}
    \item \textbf{方法一}：平均误差约3.75像素，较大，主要因为数据量不足
    \item \textbf{方法二}：大部分图像误差在0.2-0.6像素之间，表明标定结果更可靠
    \item 部分图像误差较大（如Image 15），可能原因：
    \begin{itemize}
        \item 棋盘格位于图像边缘区域，畸变影响较大
        \item 棋盘格拍摄角度较大，导致透视变形
    \end{itemize}
    \item 根据作业要求，应尽量使用图像中心区域的点来减少畸变影响
\end{itemize}

\subsection{方法选择建议}
\begin{itemize}
    \item 如果图像质量较好且数量充足，两种方法均可使用
    \item 如果图像存在模糊、倾斜等问题，建议使用 \texttt{findChessboardCornersSB}
    \item 更多的有效图像可以提供更稳定的标定结果
\end{itemize}

\section{结论}

本实验成功实现了基于张正友标定法的相机标定算法，主要完成了以下工作：
\begin{enumerate}
    \item 实现了棋盘格角点检测和世界坐标初始化
    \item 测试了两种角点检测方法：\texttt{findChessboardCorners} 和 \texttt{findChessboardCornersSB}
    \item 使用 DLT 算法计算单应性矩阵
    \item 通过张正友标定法求解相机内参矩阵
    \item 计算了每张图像的重投影误差
\end{enumerate}

\subsection{最终结果}
基于方法二（findChessboardCornersSB，19张图像）的标定结果更为可靠：
\begin{itemize}
    \item 焦距：$f_x = 832.44$, $f_y = 787.14$
    \item 主点：$(c_x, c_y) = (498.24, 334.65)$
    \item 平均重投影误差：约 1.05 像素
\end{itemize}

标定结果与 OpenCV 验证结果基本一致，验证了算法的正确性。方法二由于能检测更多图像，提供了更稳定可靠的标定结果。

\end{document}

适当删除文档中的小标题和分节，让报告的文本内容看上去更连贯流畅

---

### DeepSeek AI

<p>思考：</p><blockquote><p class="ds-markdown-paragraph"><span>我们注意到原始文档使用了多个小标题和分节，现在需要适当删除，让报告更连贯流畅。我们将删除一些子标题，将内容合并为连续的段落，同时保持逻辑清晰。</span></p><p class="ds-markdown-paragraph"><span>修改计划：</span></p><ol start="1"><li><p class="ds-markdown-paragraph"><span>将“任务简要说明”和“核心实现说明”合并到“编程任务”部分，作为连贯的叙述。</span></p></li><li><p class="ds-markdown-paragraph"><span>将“实验结果”和“结果分析”合并，并删除其中的子标题，改为连续的段落描述。</span></p></li><li><p class="ds-markdown-paragraph"><span>将“结论”部分也进行连贯性调整。</span></p></li></ol><p class="ds-markdown-paragraph"><span>注意：我们保留章节标题（如“编程任务”），但删除其下的子节标题（如“实验目标”、“标定流程”等），将其内容合并为段落。</span></p><p class="ds-markdown-paragraph"><span>由于文档较长，我们只修改书面作业之后的部分，即从“编程任务”开始到结束。</span></p><p class="ds-markdown-paragraph"><span>注意：书面作业部分已经完成，我们只调整编程任务部分。</span></p><p class="ds-markdown-paragraph"><span>我们将按照以下结构重写编程任务部分：</span></p><ol start="1"><li><p class="ds-markdown-paragraph"><span>编程任务</span><br><span>简要介绍实验目标和流程，然后直接进入核心实现说明，将各小节合并为连贯的段落。</span></p></li><li><p class="ds-markdown-paragraph"><span>实验结果与分析</span><br><span>将实验结果和结果分析合并，用连贯的段落描述两种方法的结果和对比分析。</span></p></li><li><p class="ds-markdown-paragraph"><span>结论</span></p></li></ol><p class="ds-markdown-paragraph"><span>我们开始修改。</span></p></blockquote><br/><p class="ds-markdown-paragraph"><span>\documentclass[UTF8]{ctexart}</span></p><p class="ds-markdown-paragraph"><span>%=================================================</span><br><span>% 导入所需宏包</span><br><span>%=================================================</span><br><span>\usepackage{amsmath}          % AMS数学公式环境</span><br><span>\usepackage{amssymb}          % AMS数学符号</span><br><span>\usepackage{amsfonts}         % AMS数学字体</span><br><span>\usepackage[a4paper, margin=1in]{geometry} % 设置页面边距</span><br><span>\usepackage{hyperref}         % 创建超链接</span><br><span>\usepackage[UTF8]{ctex}</span><br><span>\usepackage{amsmath,amssymb}</span><br><span>\usepackage{graphicx}</span><br><span>\usepackage{booktabs}</span><br><span>\usepackage{listings}</span><br><span>\usepackage{xcolor}</span><br><span>\usepackage{geometry}</span><br><span>\usepackage{float}</span><br><span>\usepackage{caption}</span></p><p class="ds-markdown-paragraph"><span>\geometry{left=2.5cm,right=2.5cm,top=2.5cm,bottom=2.5cm}</span></p><p class="ds-markdown-paragraph"><span>\lstset{</span><br><span>language=Python,</span><br><span>basicstyle=\ttfamily\small,</span><br><span>keywordstyle=\color{blue},</span><br><span>commentstyle=\color{green!60!black},</span><br><span>stringstyle=\color{orange},</span><br><span>numbers=left,</span><br><span>numberstyle=\tiny\color{gray},</span><br><span>frame=single,</span><br><span>breaklines=true,</span><br><span>showstringspaces=false,</span><br><span>tabsize=4</span><br><span>}</span><br><span>%=================================================</span><br><span>% 定义一些常用命令</span><br><span>%=================================================</span><br><span>% 定义粗体向量和矩阵命令</span><br><span>\newcommand{\bvec}[1]{\boldsymbol{#1}}</span><br><span>\newcommand{\bmat}[1]{\boldsymbol{#1}}</span></p><p class="ds-markdown-paragraph"><span>%=================================================</span><br><span>% 文档开始</span><br><span>%=================================================</span><br><span>\begin{document}</span></p><p class="ds-markdown-paragraph"><span>%=================================================</span><br><span>% 标题部分</span><br><span>%=================================================</span><br><span>\title{计算机视觉：第二次作业}</span><br><span>\author{黄逸隽 523030910202}</span><br><span>\date{截止日期：2025年12月1日}</span><br><span>\maketitle</span></p><p class="ds-markdown-paragraph"><span>\hrule\vspace{1em}</span></p><p class="ds-markdown-paragraph"><span>%=================================================</span><br><span>% 问题与解答</span><br><span>%=================================================</span><br><span>\section*{书面作业 }</span></p><p class="ds-markdown-paragraph"><span>我们的目标是找到使误差函数 </span><span class="katex"></span><span> 最小的 </span><span class="katex"></span><span> 和 </span><span class="katex"></span><span>，我们通过将 </span><span class="katex"></span><span> 对 </span><span class="katex"></span><span> 和 </span><span class="katex"></span><span> 的偏导数设为零来求解。</span></p><p class="ds-markdown-paragraph"><span>首先，我们计算 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi>E</mi></mrow><annotation encoding="application/x-tex">E</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.6833em;"></span><span class="mord mathnormal" style="margin-right:0.05764em;">E</span></span></span></span><span> 关于 </span><span class="katex"></span><span> 的偏导数：</span></p><span class="katex-display ds-markdown-math"><span class="katex"></span></span><p class="ds-markdown-paragraph"><span>使用向量求导法则 </span><span class="katex"></span><span>，我们得到：</span></p><span class="katex-display ds-markdown-math"><span class="katex"></span></span><p class="ds-markdown-paragraph"><span>令偏导数为零向量 </span><span class="katex"></span><span>：</span></p><span class="katex-display ds-markdown-math"><span class="katex"></span></span><span class="katex-display ds-markdown-math"><span class="katex"></span></span><p class="ds-markdown-paragraph"><span>根据质心 </span><span class="katex"></span><span> 和 </span><span class="katex"></span><span> 的定义，上式可以写为：</span></p><span class="katex-display ds-markdown-math"><span class="katex"></span></span><p class="ds-markdown-paragraph"><span>两边同除以 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi>N</mi></mrow><annotation encoding="application/x-tex">N</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.6833em;"></span><span class="mord mathnormal" style="margin-right:0.10903em;">N</span></span></span></span><span>，我们得到最优 </span><span class="katex"></span><span> 和最优 </span><span class="katex"></span><span> 之间的关系：</span><br><span>\begin{equation} \label{eq:T_star}</span><br><span>\bvec{T}^* = \bar{\bvec{Y}} - \bmat{A}^*\bar{\bvec{X}}</span><br><span>\end{equation}</span><br><span>这证明了第一个公式。</span></p><p class="ds-markdown-paragraph"><span>现在，我们将式 \eqref{eq:T_star} 的关系代入原始误差函数 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi>E</mi></mrow><annotation encoding="application/x-tex">E</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.6833em;"></span><span class="mord mathnormal" style="margin-right:0.05764em;">E</span></span></span></span><span> 中，以消除 </span><span class="katex"></span><span>。</span></p><span class="katex-display ds-markdown-math"><span class="katex"></span></span><p class="ds-markdown-paragraph"><span>我们定义中心化坐标：</span><span class="katex"></span><span> 和 </span><span class="katex"></span><span>。误差函数简化为：</span></p><span class="katex-display ds-markdown-math"><span class="katex"></span></span><p class="ds-markdown-paragraph"><span>现在，我们引入题目中定义的 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mn>3</mn><mo>×</mo><mi>N</mi></mrow><annotation encoding="application/x-tex">3 \times N</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.7278em;vertical-align:-0.0833em;"></span><span class="mord">3</span><span class="mspace" style="margin-right:0.2222em;"></span><span class="mbin">×</span><span class="mspace" style="margin-right:0.2222em;"></span></span><span class="base"><span class="strut" style="height:0.6833em;"></span><span class="mord mathnormal" style="margin-right:0.10903em;">N</span></span></span></span><span> 矩阵 </span><span class="katex"></span><span> 和 </span><span class="katex"></span><span>。误差函数可以写成矩阵的 Frobenius 范数形式：</span></p><span class="katex-display ds-markdown-math"><span class="katex"></span></span><p class="ds-markdown-paragraph"><span>使用迹（trace）的性质，</span><span class="katex"></span><span>，我们有：</span></p><span class="katex-display ds-markdown-math"><span class="katex"></span></span><p class="ds-markdown-paragraph"><span>现在计算 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi>E</mi></mrow><annotation encoding="application/x-tex">E</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.6833em;"></span><span class="mord mathnormal" style="margin-right:0.05764em;">E</span></span></span></span><span> 关于 </span><span class="katex"></span><span> 的偏导数。使用矩阵求导法则 </span><span class="katex"></span><span>，</span><span class="katex"></span><span> 和 </span><span class="katex"></span><span>：</span></p><span class="katex-display ds-markdown-math"><span class="katex"></span></span><p class="ds-markdown-paragraph"><span>令偏导数为零矩阵 </span><span class="katex"></span><span>：</span></p><span class="katex-display ds-markdown-math"><span class="katex"></span></span><span class="katex-display ds-markdown-math"><span class="katex"></span></span><p class="ds-markdown-paragraph"><span>假设矩阵 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi mathvariant="script">X</mi><msup><mi mathvariant="script">X</mi><mi>T</mi></msup></mrow><annotation encoding="application/x-tex">\mathcal{X}\mathcal{X}^T</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.8413em;"></span><span class="mord mathcal" style="margin-right:0.14643em;">X</span><span class="mord"><span class="mord mathcal" style="margin-right:0.14643em;">X</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height:0.8413em;"><span style="top:-3.063em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mathnormal mtight" style="margin-right:0.13889em;">T</span></span></span></span></span></span></span></span></span></span></span><span> 是可逆的（这要求中心化的点集 </span><span class="katex"></span><span> 不是共面或共线的），我们可以在等式右侧乘以其逆矩阵：</span></p><span class="katex-display ds-markdown-math"><span class="katex"></span></span><p class="ds-markdown-paragraph"><span>这证明了第二个公式。</span><br><span>\hfill </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi mathvariant="normal">■</mi></mrow><annotation encoding="application/x-tex">\blacksquare</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.675em;"></span><span class="mord amsrm">■</span></span></span></span></p><p class="ds-markdown-paragraph"><span>\vspace{2em}</span></p><p class="ds-markdown-paragraph"><span>\noindent\textbf{证明：}</span></p><p class="ds-markdown-paragraph"><span>我们通过分析变换中的未知数数量和每个点对应提供的约束数量来确定最少需要的点数。</span></p><p class="ds-markdown-paragraph"><span>变换 </span><span class="katex"></span><span> 包含两个部分：</span><br><span>\begin{itemize}</span><br><span>\item 旋转/缩放/错切矩阵 </span><span class="katex"></span><span>，包含 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mn>3</mn><mo>×</mo><mn>3</mn><mo>=</mo><mn>9</mn></mrow><annotation encoding="application/x-tex">3 \times 3 = 9</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.7278em;vertical-align:-0.0833em;"></span><span class="mord">3</span><span class="mspace" style="margin-right:0.2222em;"></span><span class="mbin">×</span><span class="mspace" style="margin-right:0.2222em;"></span></span><span class="base"><span class="strut" style="height:0.6444em;"></span><span class="mord">3</span><span class="mspace" style="margin-right:0.2778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right:0.2778em;"></span></span><span class="base"><span class="strut" style="height:0.6444em;"></span><span class="mord">9</span></span></span></span><span> 个未知参数。</span><br><span>\item 平移向量 </span><span class="katex"></span><span>，包含 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mn>3</mn><mo>×</mo><mn>1</mn><mo>=</mo><mn>3</mn></mrow><annotation encoding="application/x-tex">3 \times 1 = 3</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.7278em;vertical-align:-0.0833em;"></span><span class="mord">3</span><span class="mspace" style="margin-right:0.2222em;"></span><span class="mbin">×</span><span class="mspace" style="margin-right:0.2222em;"></span></span><span class="base"><span class="strut" style="height:0.6444em;"></span><span class="mord">1</span><span class="mspace" style="margin-right:0.2778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right:0.2778em;"></span></span><span class="base"><span class="strut" style="height:0.6444em;"></span><span class="mord">3</span></span></span></span><span> 个未知参数。</span><br><span>\end{itemize}</span><br><span>因此，总共有 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mn>9</mn><mo>+</mo><mn>3</mn><mo>=</mo><mn>12</mn></mrow><annotation encoding="application/x-tex">9 + 3 = 12</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.7278em;vertical-align:-0.0833em;"></span><span class="mord">9</span><span class="mspace" style="margin-right:0.2222em;"></span><span class="mbin">+</span><span class="mspace" style="margin-right:0.2222em;"></span></span><span class="base"><span class="strut" style="height:0.6444em;"></span><span class="mord">3</span><span class="mspace" style="margin-right:0.2778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right:0.2778em;"></span></span><span class="base"><span class="strut" style="height:0.6444em;"></span><span class="mord">12</span></span></span></span><span> 个独立的未知参数需要求解。</span></p><p class="ds-markdown-paragraph"><span>每一组对应点 </span><span class="katex"></span><span> 提供一个矢量方程：</span></p><span class="katex-display ds-markdown-math"><span class="katex"></span></span><p class="ds-markdown-paragraph"><span>这个方程是在 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><msup><mi mathvariant="double-struck">R</mi><mn>3</mn></msup></mrow><annotation encoding="application/x-tex">\mathbb{R}^3</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.8141em;"></span><span class="mord"><span class="mord mathbb">R</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height:0.8141em;"><span style="top:-3.063em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">3</span></span></span></span></span></span></span></span></span></span></span><span> 空间中的，它可以分解为3个独立的标量方程：</span></p><span class="katex-display ds-markdown-math"><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><semantics><mrow><mo fence="true">{</mo><mtable rowspacing="0.36em" columnalign="left left" columnspacing="1em"><mtr><mtd><mstyle scriptlevel="0" displaystyle="false"><mrow><msub><mi>y</mi><mrow><mi>i</mi><mn>1</mn></mrow></msub><mo>=</mo><msub><mi>a</mi><mn>11</mn></msub><msub><mi>x</mi><mrow><mi>i</mi><mn>1</mn></mrow></msub><mo>+</mo><msub><mi>a</mi><mn>12</mn></msub><msub><mi>x</mi><mrow><mi>i</mi><mn>2</mn></mrow></msub><mo>+</mo><msub><mi>a</mi><mn>13</mn></msub><msub><mi>x</mi><mrow><mi>i</mi><mn>3</mn></mrow></msub><mo>+</mo><msub><mi>t</mi><mn>1</mn></msub></mrow></mstyle></mtd></mtr><mtr><mtd><mstyle scriptlevel="0" displaystyle="false"><mrow><msub><mi>y</mi><mrow><mi>i</mi><mn>2</mn></mrow></msub><mo>=</mo><msub><mi>a</mi><mn>21</mn></msub><msub><mi>x</mi><mrow><mi>i</mi><mn>1</mn></mrow></msub><mo>+</mo><msub><mi>a</mi><mn>22</mn></msub><msub><mi>x</mi><mrow><mi>i</mi><mn>2</mn></mrow></msub><mo>+</mo><msub><mi>a</mi><mn>23</mn></msub><msub><mi>x</mi><mrow><mi>i</mi><mn>3</mn></mrow></msub><mo>+</mo><msub><mi>t</mi><mn>2</mn></msub></mrow></mstyle></mtd></mtr><mtr><mtd><mstyle scriptlevel="0" displaystyle="false"><mrow><msub><mi>y</mi><mrow><mi>i</mi><mn>3</mn></mrow></msub><mo>=</mo><msub><mi>a</mi><mn>31</mn></msub><msub><mi>x</mi><mrow><mi>i</mi><mn>1</mn></mrow></msub><mo>+</mo><msub><mi>a</mi><mn>32</mn></msub><msub><mi>x</mi><mrow><mi>i</mi><mn>2</mn></mrow></msub><mo>+</mo><msub><mi>a</mi><mn>33</mn></msub><msub><mi>x</mi><mrow><mi>i</mi><mn>3</mn></mrow></msub><mo>+</mo><msub><mi>t</mi><mn>3</mn></msub></mrow></mstyle></mtd></mtr></mtable></mrow><annotation encoding="application/x-tex">\begin{cases}
y_{i1} = a_{11}x_{i1} + a_{12}x_{i2} + a_{13}x_{i3} + t_1 \\
y_{i2} = a_{21}x_{i1} + a_{22}x_{i2} + a_{23}x_{i3} + t_2 \\
y_{i3} = a_{31}x_{i1} + a_{32}x_{i2} + a_{33}x_{i3} + t_3
\end{cases}</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:4.32em;vertical-align:-1.91em;"></span><span class="minner"><span class="mopen"><span class="delimsizing mult"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:2.35em;"><span style="top:-2.2em;"><span class="pstrut" style="height:3.15em;"></span><span class="delimsizinginner delim-size4"><span>⎩</span></span></span><span style="top:-2.192em;"><span class="pstrut" style="height:3.15em;"></span><span style="height:0.316em;width:0.8889em;"><svg xmlns="http://www.w3.org/2000/svg" width="0.8889em" height="0.316em" style="width:0.8889em" viewBox="0 0 888.89 316" preserveAspectRatio="xMinYMin"><path d="M384 0 H504 V316 H384z M384 0 H504 V316 H384z"></path></svg></span></span><span style="top:-3.15em;"><span class="pstrut" style="height:3.15em;"></span><span class="delimsizinginner delim-size4"><span>⎨</span></span></span><span style="top:-4.292em;"><span class="pstrut" style="height:3.15em;"></span><span style="height:0.316em;width:0.8889em;"><svg xmlns="http://www.w3.org/2000/svg" width="0.8889em" height="0.316em" style="width:0.8889em" viewBox="0 0 888.89 316" preserveAspectRatio="xMinYMin"><path d="M384 0 H504 V316 H384z M384 0 H504 V316 H384z"></path></svg></span></span><span style="top:-4.6em;"><span class="pstrut" style="height:3.15em;"></span><span class="delimsizinginner delim-size4"><span>⎧</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height:1.85em;"><span></span></span></span></span></span></span><span class="mord"><span class="mtable"><span class="col-align-l"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:2.41em;"><span style="top:-4.41em;"><span class="pstrut" style="height:3.008em;"></span><span class="mord"><span class="mord"><span class="mord mathnormal" style="margin-right:0.03588em;">y</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:0.3117em;"><span style="top:-2.55em;margin-left:-0.0359em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mathnormal mtight">i</span><span class="mord mtight">1</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height:0.15em;"><span></span></span></span></span></span></span><span class="mspace" style="margin-right:0.2778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right:0.2778em;"></span><span class="mord"><span class="mord mathnormal">a</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:0.3011em;"><span style="top:-2.55em;margin-left:0em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight">11</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height:0.15em;"><span></span></span></span></span></span></span><span class="mord"><span class="mord mathnormal">x</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:0.3117em;"><span style="top:-2.55em;margin-left:0em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mathnormal mtight">i</span><span class="mord mtight">1</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height:0.15em;"><span></span></span></span></span></span></span><span class="mspace" style="margin-right:0.2222em;"></span><span class="mbin">+</span><span class="mspace" style="margin-right:0.2222em;"></span><span class="mord"><span class="mord mathnormal">a</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:0.3011em;"><span style="top:-2.55em;margin-left:0em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight">12</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height:0.15em;"><span></span></span></span></span></span></span><span class="mord"><span class="mord mathnormal">x</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:0.3117em;"><span style="top:-2.55em;margin-left:0em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mathnormal mtight">i</span><span class="mord mtight">2</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height:0.15em;"><span></span></span></span></span></span></span><span class="mspace" style="margin-right:0.2222em;"></span><span class="mbin">+</span><span class="mspace" style="margin-right:0.2222em;"></span><span class="mord"><span class="mord mathnormal">a</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:0.3011em;"><span style="top:-2.55em;margin-left:0em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight">13</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height:0.15em;"><span></span></span></span></span></span></span><span class="mord"><span class="mord mathnormal">x</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:0.3117em;"><span style="top:-2.55em;margin-left:0em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mathnormal mtight">i</span><span class="mord mtight">3</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height:0.15em;"><span></span></span></span></span></span></span><span class="mspace" style="margin-right:0.2222em;"></span><span class="mbin">+</span><span class="mspace" style="margin-right:0.2222em;"></span><span class="mord"><span class="mord mathnormal">t</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:0.3011em;"><span style="top:-2.55em;margin-left:0em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">1</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height:0.15em;"><span></span></span></span></span></span></span></span></span><span style="top:-2.97em;"><span class="pstrut" style="height:3.008em;"></span><span class="mord"><span class="mord"><span class="mord mathnormal" style="margin-right:0.03588em;">y</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:0.3117em;"><span style="top:-2.55em;margin-left:-0.0359em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mathnormal mtight">i</span><span class="mord mtight">2</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height:0.15em;"><span></span></span></span></span></span></span><span class="mspace" style="margin-right:0.2778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right:0.2778em;"></span><span class="mord"><span class="mord mathnormal">a</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:0.3011em;"><span style="top:-2.55em;margin-left:0em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight">21</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height:0.15em;"><span></span></span></span></span></span></span><span class="mord"><span class="mord mathnormal">x</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:0.3117em;"><span style="top:-2.55em;margin-left:0em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mathnormal mtight">i</span><span class="mord mtight">1</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height:0.15em;"><span></span></span></span></span></span></span><span class="mspace" style="margin-right:0.2222em;"></span><span class="mbin">+</span><span class="mspace" style="margin-right:0.2222em;"></span><span class="mord"><span class="mord mathnormal">a</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:0.3011em;"><span style="top:-2.55em;margin-left:0em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight">22</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height:0.15em;"><span></span></span></span></span></span></span><span class="mord"><span class="mord mathnormal">x</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:0.3117em;"><span style="top:-2.55em;margin-left:0em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mathnormal mtight">i</span><span class="mord mtight">2</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height:0.15em;"><span></span></span></span></span></span></span><span class="mspace" style="margin-right:0.2222em;"></span><span class="mbin">+</span><span class="mspace" style="margin-right:0.2222em;"></span><span class="mord"><span class="mord mathnormal">a</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:0.3011em;"><span style="top:-2.55em;margin-left:0em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight">23</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height:0.15em;"><span></span></span></span></span></span></span><span class="mord"><span class="mord mathnormal">x</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:0.3117em;"><span style="top:-2.55em;margin-left:0em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mathnormal mtight">i</span><span class="mord mtight">3</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height:0.15em;"><span></span></span></span></span></span></span><span class="mspace" style="margin-right:0.2222em;"></span><span class="mbin">+</span><span class="mspace" style="margin-right:0.2222em;"></span><span class="mord"><span class="mord mathnormal">t</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:0.3011em;"><span style="top:-2.55em;margin-left:0em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">2</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height:0.15em;"><span></span></span></span></span></span></span></span></span><span style="top:-1.53em;"><span class="pstrut" style="height:3.008em;"></span><span class="mord"><span class="mord"><span class="mord mathnormal" style="margin-right:0.03588em;">y</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:0.3117em;"><span style="top:-2.55em;margin-left:-0.0359em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mathnormal mtight">i</span><span class="mord mtight">3</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height:0.15em;"><span></span></span></span></span></span></span><span class="mspace" style="margin-right:0.2778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right:0.2778em;"></span><span class="mord"><span class="mord mathnormal">a</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:0.3011em;"><span style="top:-2.55em;margin-left:0em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight">31</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height:0.15em;"><span></span></span></span></span></span></span><span class="mord"><span class="mord mathnormal">x</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:0.3117em;"><span style="top:-2.55em;margin-left:0em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mathnormal mtight">i</span><span class="mord mtight">1</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height:0.15em;"><span></span></span></span></span></span></span><span class="mspace" style="margin-right:0.2222em;"></span><span class="mbin">+</span><span class="mspace" style="margin-right:0.2222em;"></span><span class="mord"><span class="mord mathnormal">a</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:0.3011em;"><span style="top:-2.55em;margin-left:0em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight">32</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height:0.15em;"><span></span></span></span></span></span></span><span class="mord"><span class="mord mathnormal">x</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:0.3117em;"><span style="top:-2.55em;margin-left:0em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mathnormal mtight">i</span><span class="mord mtight">2</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height:0.15em;"><span></span></span></span></span></span></span><span class="mspace" style="margin-right:0.2222em;"></span><span class="mbin">+</span><span class="mspace" style="margin-right:0.2222em;"></span><span class="mord"><span class="mord mathnormal">a</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:0.3011em;"><span style="top:-2.55em;margin-left:0em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight">33</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height:0.15em;"><span></span></span></span></span></span></span><span class="mord"><span class="mord mathnormal">x</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:0.3117em;"><span style="top:-2.55em;margin-left:0em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mathnormal mtight">i</span><span class="mord mtight">3</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height:0.15em;"><span></span></span></span></span></span></span><span class="mspace" style="margin-right:0.2222em;"></span><span class="mbin">+</span><span class="mspace" style="margin-right:0.2222em;"></span><span class="mord"><span class="mord mathnormal">t</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:0.3011em;"><span style="top:-2.55em;margin-left:0em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">3</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height:0.15em;"><span></span></span></span></span></span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height:1.91em;"><span></span></span></span></span></span></span></span><span class="mclose nulldelimiter"></span></span></span></span></span></span><p class="ds-markdown-paragraph"><span>所以，每一组对应点能够提供3个线性方程。</span></p><p class="ds-markdown-paragraph"><span>为了唯一地确定所有12个未知参数，我们需要的独立方程数量必须至少等于未知数的数量。设 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi>N</mi></mrow><annotation encoding="application/x-tex">N</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.6833em;"></span><span class="mord mathnormal" style="margin-right:0.10903em;">N</span></span></span></span><span> 为所需的最少对应点数量，则：</span></p><span class="katex-display ds-markdown-math"><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><semantics><mrow><mtext>总方程数</mtext><mo>≥</mo><mtext>总未知数</mtext></mrow><annotation encoding="application/x-tex">\text{总方程数} \ge \text{总未知数} </annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.8193em;vertical-align:-0.136em;"></span><span class="mord text"><span class="mord cjk_fallback">总方程数</span></span><span class="mspace" style="margin-right:0.2778em;"></span><span class="mrel">≥</span><span class="mspace" style="margin-right:0.2778em;"></span></span><span class="base"><span class="strut" style="height:0.6833em;"></span><span class="mord text"><span class="mord cjk_fallback">总未知数</span></span></span></span></span></span><span class="katex-display ds-markdown-math"><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><semantics><mrow><mn>3</mn><mi>N</mi><mo>≥</mo><mn>12</mn></mrow><annotation encoding="application/x-tex">3N \ge 12 </annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.8193em;vertical-align:-0.136em;"></span><span class="mord">3</span><span class="mord mathnormal" style="margin-right:0.10903em;">N</span><span class="mspace" style="margin-right:0.2778em;"></span><span class="mrel">≥</span><span class="mspace" style="margin-right:0.2778em;"></span></span><span class="base"><span class="strut" style="height:0.6444em;"></span><span class="mord">12</span></span></span></span></span><span class="katex-display ds-markdown-math"><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><semantics><mrow><mi>N</mi><mo>≥</mo><mn>4</mn></mrow><annotation encoding="application/x-tex">N \ge 4 </annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.8193em;vertical-align:-0.136em;"></span><span class="mord mathnormal" style="margin-right:0.10903em;">N</span><span class="mspace" style="margin-right:0.2778em;"></span><span class="mrel">≥</span><span class="mspace" style="margin-right:0.2778em;"></span></span><span class="base"><span class="strut" style="height:0.6444em;"></span><span class="mord">4</span></span></span></span></span><p class="ds-markdown-paragraph"><span>因此，我们至少需要4组对应点。</span></p><p class="ds-markdown-paragraph"><span>拥有 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi>N</mi><mo>=</mo><mn>4</mn></mrow><annotation encoding="application/x-tex">N=4</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.6833em;"></span><span class="mord mathnormal" style="margin-right:0.10903em;">N</span><span class="mspace" style="margin-right:0.2778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right:0.2778em;"></span></span><span class="base"><span class="strut" style="height:0.6444em;"></span><span class="mord">4</span></span></span></span><span> 组点只是一个必要条件，不是充分条件。为了得到唯一解，这些方程必须是线性无关的。从(a)部分的推导中，我们知道 </span><span class="katex"></span><span> 的解为 </span><span class="katex"></span><span>。这个解存在的关键在于矩阵 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi mathvariant="script">X</mi><msup><mi mathvariant="script">X</mi><mi>T</mi></msup></mrow><annotation encoding="application/x-tex">\mathcal{X}\mathcal{X}^T</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.8413em;"></span><span class="mord mathcal" style="margin-right:0.14643em;">X</span><span class="mord"><span class="mord mathcal" style="margin-right:0.14643em;">X</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height:0.8413em;"><span style="top:-3.063em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mathnormal mtight" style="margin-right:0.13889em;">T</span></span></span></span></span></span></span></span></span></span></span><span> 是可逆的。</span></p><p class="ds-markdown-paragraph"><span>矩阵 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi mathvariant="script">X</mi><msup><mi mathvariant="script">X</mi><mi>T</mi></msup></mrow><annotation encoding="application/x-tex">\mathcal{X}\mathcal{X}^T</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.8413em;"></span><span class="mord mathcal" style="margin-right:0.14643em;">X</span><span class="mord"><span class="mord mathcal" style="margin-right:0.14643em;">X</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height:0.8413em;"><span style="top:-3.063em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mathnormal mtight" style="margin-right:0.13889em;">T</span></span></span></span></span></span></span></span></span></span></span><span> 是一个 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mn>3</mn><mo>×</mo><mn>3</mn></mrow><annotation encoding="application/x-tex">3 \times 3</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.7278em;vertical-align:-0.0833em;"></span><span class="mord">3</span><span class="mspace" style="margin-right:0.2222em;"></span><span class="mbin">×</span><span class="mspace" style="margin-right:0.2222em;"></span></span><span class="base"><span class="strut" style="height:0.6444em;"></span><span class="mord">3</span></span></span></span><span> 的矩阵，定义为 </span><span class="katex"></span><span>，其中 </span><span class="katex"></span><span>。</span><br><span>为了使 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi mathvariant="script">X</mi><msup><mi mathvariant="script">X</mi><mi>T</mi></msup></mrow><annotation encoding="application/x-tex">\mathcal{X}\mathcal{X}^T</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.8413em;"></span><span class="mord mathcal" style="margin-right:0.14643em;">X</span><span class="mord"><span class="mord mathcal" style="margin-right:0.14643em;">X</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height:0.8413em;"><span style="top:-3.063em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mathnormal mtight" style="margin-right:0.13889em;">T</span></span></span></span></span></span></span></span></span></span></span><span> 可逆，它的秩必须是3。这意味着由中心化向量 </span><span class="katex"></span><span> 张成的子空间维度必须是3。</span><br><span>\begin{itemize}</span><br><span>\item 如果 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi>N</mi><mo>&lt;</mo><mn>4</mn></mrow><annotation encoding="application/x-tex">N &lt; 4</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.7224em;vertical-align:-0.0391em;"></span><span class="mord mathnormal" style="margin-right:0.10903em;">N</span><span class="mspace" style="margin-right:0.2778em;"></span><span class="mrel">&lt;</span><span class="mspace" style="margin-right:0.2778em;"></span></span><span class="base"><span class="strut" style="height:0.6444em;"></span><span class="mord">4</span></span></span></span><span>，例如 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi>N</mi><mo>=</mo><mn>3</mn></mrow><annotation encoding="application/x-tex">N=3</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.6833em;"></span><span class="mord mathnormal" style="margin-right:0.10903em;">N</span><span class="mspace" style="margin-right:0.2778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right:0.2778em;"></span></span><span class="base"><span class="strut" style="height:0.6444em;"></span><span class="mord">3</span></span></span></span><span>，三个点 </span><span class="katex"></span><span> 最多是共面的（通常是，除非它们共线）。它们的中心化向量 </span><span class="katex"></span><span> 也将位于一个过原点的平面上，因此它们张成的空间维度最多为2，导致 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi mathvariant="script">X</mi><msup><mi mathvariant="script">X</mi><mi>T</mi></msup></mrow><annotation encoding="application/x-tex">\mathcal{X}\mathcal{X}^T</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.8413em;"></span><span class="mord mathcal" style="margin-right:0.14643em;">X</span><span class="mord"><span class="mord mathcal" style="margin-right:0.14643em;">X</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height:0.8413em;"><span style="top:-3.063em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mathnormal mtight" style="margin-right:0.13889em;">T</span></span></span></span></span></span></span></span></span></span></span><span> 是奇异的。</span><br><span>\item 如果 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi>N</mi><mo>=</mo><mn>4</mn></mrow><annotation encoding="application/x-tex">N=4</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.6833em;"></span><span class="mord mathnormal" style="margin-right:0.10903em;">N</span><span class="mspace" style="margin-right:0.2778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right:0.2778em;"></span></span><span class="base"><span class="strut" style="height:0.6444em;"></span><span class="mord">4</span></span></span></span><span>，并且这4个点 </span><span class="katex"></span><span> 是 \textbf{共面（coplanar）}的，那么它们的中心化向量 </span><span class="katex"></span><span> 也将位于一个过原点的平面上。这样，它们张成的空间维度仍然是2，</span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi mathvariant="script">X</mi><msup><mi mathvariant="script">X</mi><mi>T</mi></msup></mrow><annotation encoding="application/x-tex">\mathcal{X}\mathcal{X}^T</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.8413em;"></span><span class="mord mathcal" style="margin-right:0.14643em;">X</span><span class="mord"><span class="mord mathcal" style="margin-right:0.14643em;">X</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height:0.8413em;"><span style="top:-3.063em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mathnormal mtight" style="margin-right:0.13889em;">T</span></span></span></span></span></span></span></span></span></span></span><span> 依然是奇异的。</span><br><span>\end{itemize}</span><br><span>因此，为了保证 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi mathvariant="script">X</mi><msup><mi mathvariant="script">X</mi><mi>T</mi></msup></mrow><annotation encoding="application/x-tex">\mathcal{X}\mathcal{X}^T</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.8413em;"></span><span class="mord mathcal" style="margin-right:0.14643em;">X</span><span class="mord"><span class="mord mathcal" style="margin-right:0.14643em;">X</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height:0.8413em;"><span style="top:-3.063em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mathnormal mtight" style="margin-right:0.13889em;">T</span></span></span></span></span></span></span></span></span></span></span><span> 满秩（秩为3），我们不仅需要 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi>N</mi><mo>≥</mo><mn>4</mn></mrow><annotation encoding="application/x-tex">N \ge 4</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.8193em;vertical-align:-0.136em;"></span><span class="mord mathnormal" style="margin-right:0.10903em;">N</span><span class="mspace" style="margin-right:0.2778em;"></span><span class="mrel">≥</span><span class="mspace" style="margin-right:0.2778em;"></span></span><span class="base"><span class="strut" style="height:0.6444em;"></span><span class="mord">4</span></span></span></span><span>，还要求这4个点 </span><span class="katex"></span><span> \textbf{不能共面（non-coplanar）}。当这4个点不共面时，它们构成的中心化向量可以张成整个 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><msup><mi mathvariant="double-struck">R</mi><mn>3</mn></msup></mrow><annotation encoding="application/x-tex">\mathbb{R}^3</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.8141em;"></span><span class="mord"><span class="mord mathbb">R</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height:0.8141em;"><span style="top:-3.063em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">3</span></span></span></span></span></span></span></span></span></span></span><span> 空间，保证了 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi mathvariant="script">X</mi><msup><mi mathvariant="script">X</mi><mi>T</mi></msup></mrow><annotation encoding="application/x-tex">\mathcal{X}\mathcal{X}^T</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.8413em;"></span><span class="mord mathcal" style="margin-right:0.14643em;">X</span><span class="mord"><span class="mord mathcal" style="margin-right:0.14643em;">X</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height:0.8413em;"><span style="top:-3.063em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mathnormal mtight" style="margin-right:0.13889em;">T</span></span></span></span></span></span></span></span></span></span></span><span> 的可逆性，从而可以唯一确定 </span><span class="katex"></span><span> 和 </span><span class="katex"></span><span>。</span></p><p class="ds-markdown-paragraph"><span>\textbf{结论：} 估计该3D仿射变换所需的最少对应点数量是4，并且这4个源点 </span><span class="katex"></span><span> 不能共面。</span><br><span>\hfill </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi mathvariant="normal">■</mi></mrow><annotation encoding="application/x-tex">\blacksquare</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.675em;"></span><span class="mord amsrm">■</span></span></span></span></p><p class="ds-markdown-paragraph"><span>\section*{编程任务}</span></p><p class="ds-markdown-paragraph"><span>本次实验的目标是完成相机标定，通过一系列棋盘格图像推导出相机的内参矩阵，包括焦距 $(f_x, f_y)$、主点坐标 $(c_x, c_y)$以及每张图像对应的重投影误差。</span></p><p class="ds-markdown-paragraph"><span>标准的相机标定流程如下：使用已知尺寸的棋盘格图案定义3D点的世界坐标，从不同视角拍摄棋盘格图像，检测棋盘格角点获取每个3D点在不同图像中的像素坐标 $(u, v)$，最后使用线性代数方法求解相机参数。实验要求只允许使用基本的 Python、NumPy 和 OpenCV 函数，允许使用 \texttt{cv2.findChessboardCorners} 等角点检测函数，但不允许使用 \texttt{cv2.calibrateCamera} 等"魔法"函数求解内参（仅用于验证）。世界坐标可简化为 $(0,0), (1,0), (2,0), \ldots$，结果以棋盘格方格大小为单位。</span></p><p class="ds-markdown-paragraph"><span>在核心实现方面，首先初始化棋盘格的世界坐标点，这些点定义在 $Z=0$ 的平面上，坐标按 $(0,0,0), (1,0,0), (2,0,0), \ldots$ 的方式排列：</span></p><p class="ds-markdown-paragraph"><span>\begin{lstlisting}</span><br><span>def init_world_points(pattern_size):</span><br><span># 生成棋盘格的世界坐标</span><br><span># 点排列为 (0,0,0), (1,0,0), (2,0,0), ... 在XY平面上 (Z=0)</span><br><span>objp = np.zeros((pattern_size[0] * pattern_size[1], 3), np.float32)</span><br><span>objp[:, :2] = np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2)</span><br><span>return objp</span><br><span>\end{lstlisting}</span></p><p class="ds-markdown-paragraph"><span>本实验测试了两种角点检测方法。第一种是传统的 \texttt{findChessboardCorners} 函数，并通过 \texttt{cornerSubPix} 进行亚像素精度优化：</span></p><p class="ds-markdown-paragraph"><span>\begin{lstlisting}</span><br><span>def detect_corners(image, pattern_size):</span><br><span>gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)</span><br><span>ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)</span><br><span>if ret:</span><br><span># 亚像素精度优化</span><br><span>criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)</span><br><span>corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)</span><br><span>return corners.reshape(-1, 2)</span><br><span>return None</span><br><span>\end{lstlisting}</span></p><p class="ds-markdown-paragraph"><span>第二种是使用 OpenCV 4.0+ 引入的 \texttt{findChessboardCornersSB} 函数（SB = Sector Based），该方法更加鲁棒：</span></p><p class="ds-markdown-paragraph"><span>\begin{lstlisting}</span><br><span>def detect_corners(image, pattern_size):</span><br><span>gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)</span><br><span>ret, corners = cv2.findChessboardCornersSB(gray, pattern_size)</span><br><span>if ret:</span><br><span>return corners.reshape(-1, 2)</span><br><span>return None</span><br><span>\end{lstlisting}</span></p><p class="ds-markdown-paragraph"><span>两种角点检测方法的对比显示，传统方法成功检测了5张图像，而基于扇区的方法成功检测了19张图像。基于扇区的方法对图像质量要求更低，对棋盘格角度要求更宽松，处理模糊图像效果更好。</span></p><p class="ds-markdown-paragraph"><span>接下来使用直接线性变换（DLT）算法计算每张图像的单应性矩阵 $\mathbf{H}$。对于世界坐标 $(X, Y)$ 和图像坐标 $(u, v)$，有：</span><br><span>\begin{equation}</span><br><span>\begin{bmatrix} u \ v \ 1 \end{bmatrix} \sim \mathbf{H} \begin{bmatrix} X \ Y \ 1 \end{bmatrix}</span><br><span>\end{equation}</span></p><p class="ds-markdown-paragraph"><span>构建方程组 $\mathbf{A}\mathbf{h} = \mathbf{0}$，使用 SVD 求解：</span></p><p class="ds-markdown-paragraph"><span>\begin{lstlisting}</span><br><span>def compute_homography(world_pts, image_pts):</span><br><span>num_pts = world_pts.shape[0]</span><br><span>A_h = []</span></p><div class="md-code-block md-code-block-light"><div class="md-code-block-banner-wrap"><div class="md-code-block-banner md-code-block-banner-lite"><div class="_121d384"><div class="d2a24f03"><span class="d813de27">text</span></div><div class="d2a24f03 _246a029"><div class="efa13877"><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon" style="margin-right: 4px;"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.14923 4.02032C7.11191 4.02032 7.87977 4.02017 8.49591 4.07599C9.12122 4.1327 9.65786 4.25188 10.1414 4.53107C10.7201 4.8653 11.2008 5.34591 11.535 5.92462C11.8142 6.40818 11.9333 6.94482 11.9901 7.57013C12.0459 8.18625 12.0457 8.9542 12.0457 9.91681C12.0457 10.8795 12.0459 11.6474 11.9901 12.2635C11.9333 12.8888 11.8142 13.4254 11.535 13.909C11.2008 14.4877 10.7201 14.9683 10.1414 15.3026C9.65786 15.5817 9.12122 15.7009 8.49591 15.7576C7.87977 15.8134 7.1119 15.8133 6.14923 15.8133C5.18661 15.8133 4.41868 15.8134 3.80255 15.7576C3.17724 15.7009 2.6406 15.5817 2.15704 15.3026C1.57834 14.9684 1.09772 14.4877 0.763489 13.909C0.484305 13.4254 0.365123 12.8888 0.308411 12.2635C0.252587 11.6474 0.252747 10.8795 0.252747 9.91681C0.252747 8.95419 0.252603 8.18625 0.308411 7.57013C0.365123 6.94482 0.484305 6.40818 0.763489 5.92462C1.09771 5.3459 1.57833 4.86529 2.15704 4.53107C2.6406 4.25188 3.17724 4.1327 3.80255 4.07599C4.41868 4.02018 5.1866 4.02032 6.14923 4.02032ZM6.14923 5.37775C5.16175 5.37775 4.46628 5.37761 3.9256 5.42657C3.39428 5.47473 3.07853 5.56574 2.83575 5.70587C2.46313 5.92106 2.15348 6.23071 1.93829 6.60333C1.79817 6.84611 1.70715 7.16185 1.659 7.69318C1.61004 8.23385 1.61017 8.92934 1.61017 9.91681C1.61017 10.9043 1.61002 11.5998 1.659 12.1404C1.70715 12.6717 1.79817 12.9875 1.93829 13.2303C2.15349 13.6029 2.46315 13.9126 2.83575 14.1277C3.07853 14.2679 3.39428 14.3589 3.9256 14.407C4.46628 14.456 5.16176 14.4559 6.14923 14.4559C7.13675 14.4559 7.83218 14.456 8.37286 14.407C8.90419 14.3589 9.21993 14.2679 9.46271 14.1277C9.83529 13.9126 10.145 13.6029 10.3602 13.2303C10.5003 12.9875 10.5913 12.6718 10.6395 12.1404C10.6884 11.5998 10.6883 10.9043 10.6883 9.91681C10.6883 8.92935 10.6884 8.23385 10.6395 7.69318C10.5913 7.16185 10.5003 6.84611 10.3602 6.60333C10.145 6.23072 9.8353 5.92107 9.46271 5.70587C9.21993 5.56574 8.90418 5.47473 8.37286 5.42657C7.83218 5.3776 7.13676 5.37775 6.14923 5.37775ZM9.80157 0.367981C10.7637 0.367981 11.5313 0.367886 12.1473 0.423645C12.7725 0.480313 13.3093 0.598765 13.7928 0.877747C14.3716 1.21192 14.852 1.69355 15.1863 2.27228C15.4655 2.75575 15.5857 3.29165 15.6424 3.91681C15.6982 4.53301 15.6971 5.30161 15.6971 6.26447V7.8299C15.6971 8.29265 15.6989 8.58994 15.6649 8.84845C15.4667 10.3525 14.4009 11.5738 12.9832 11.9988V10.5467C13.6973 10.1903 14.2104 9.49662 14.3192 8.67169C14.3387 8.52348 14.3406 8.3358 14.3406 7.8299V6.26447C14.3406 5.27707 14.3398 4.58149 14.2908 4.04083C14.2427 3.50969 14.1526 3.19373 14.0125 2.95099C13.7974 2.5785 13.4875 2.2687 13.1151 2.05353C12.8723 1.91347 12.5563 1.82237 12.0252 1.77423C11.4846 1.72528 10.7888 1.7254 9.80157 1.7254H7.71466C6.75614 1.72559 5.92659 2.27697 5.52325 3.07892H4.07013C4.54215 1.51132 5.99314 0.368192 7.71466 0.367981H9.80157Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">复制</span></span><div class="ds-focus-ring"></div></button><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M15.3695 11.411L15.1234 12.8866C14.8869 14.3042 13.6603 15.3436 12.223 15.3436H3.7767C2.33954 15.3434 1.11276 14.3042 0.876312 12.8866L0.630219 11.411L2.05405 11.1747L2.29916 12.6493C2.41969 13.3713 3.04472 13.9001 3.7767 13.9003H12.223C12.9551 13.9002 13.58 13.3713 13.7005 12.6493L13.9456 11.1747L15.3695 11.411ZM8.72202 8.994C8.77714 8.93934 8.83789 8.88106 8.90268 8.81627L12.4828 5.23424L13.5042 6.25572L9.92221 9.8358C9.63947 10.1185 9.3876 10.3732 9.15854 10.5575C8.91889 10.7503 8.6395 10.9224 8.28647 10.9784C8.09708 11.0083 7.9036 11.0083 7.7142 10.9784C7.36103 10.9224 7.08087 10.7503 6.84116 10.5575C6.61212 10.3732 6.36019 10.1185 6.07748 9.8358L2.49643 6.25572L3.51694 5.23424L7.09702 8.81627C7.16216 8.88142 7.22327 8.94006 7.27866 8.99498V1.3065H8.72202V8.994Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">下载</span></span><div class="ds-focus-ring"></div></button></div></div></div></div></div><pre>for i in range(num_pts):
    X, Y = world_pts[i, 0], world_pts[i, 1]
    u, v = image_pts[i, 0], image_pts[i, 1]
    
    # 每个点提供2个方程
    A_h.append([-X, -Y, -1, 0, 0, 0, u*X, u*Y, u])
    A_h.append([0, 0, 0, -X, -Y, -1, v*X, v*Y, v])

A_h = np.array(A_h)

# 使用SVD求解 Ah = 0
_, _, Vt = np.linalg.svd(A_h)
H = Vt[-1].reshape(3, 3)
H = H / H[2, 2]  # 归一化

return H</pre><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _33882ae"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _28d7e84"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg></div><p class="ds-markdown-paragraph"><span>\end{lstlisting}</span></p><p class="ds-markdown-paragraph"><span>然后使用张正友标定法，通过多张图像的单应性矩阵求解相机内参。定义向量 $\mathbf{v}</span><em><span>{ij}$：</span><br><span>\begin{equation}</span><br><span>\mathbf{v}</span></em><span>{ij} = \begin{bmatrix}</span><br><span>h_{1i}h_{1j} \</span><br><span>h_{1i}h_{2j} + h_{2i}h_{1j} \</span><br><span>h_{2i}h_{2j} \</span><br><span>h_{3i}h_{1j} + h_{1i}h_{3j} \</span><br><span>h_{3i}h_{2j} + h_{2i}h_{3j} \</span><br><span>h_{3i}h_{3j}</span><br><span>\end{bmatrix}</span><br><span>\end{equation}</span></p><p class="ds-markdown-paragraph"><span>\begin{lstlisting}</span><br><span>def compute_v_ij(H, i, j):</span><br><span>return np.array([</span><br><span>H[0, i] * H[0, j],</span><br><span>H[0, i] * H[1, j] + H[1, i] * H[0, j],</span><br><span>H[1, i] * H[1, j],</span><br><span>H[2, i] * H[0, j] + H[0, i] * H[2, j],</span><br><span>H[2, i] * H[1, j] + H[1, i] * H[2, j],</span><br><span>H[2, i] * H[2, j]</span><br><span>])</span><br><span>\end{lstlisting}</span></p><p class="ds-markdown-paragraph"><span>根据约束条件 $\mathbf{h}_1^T \mathbf{B} \mathbf{h}_2 = 0$ 和 $\mathbf{h}_1^T \mathbf{B} \mathbf{h}_1 = \mathbf{h}_2^T \mathbf{B} \mathbf{h}_2$，构建矩阵 $\mathbf{V}$：</span></p><p class="ds-markdown-paragraph"><span>\begin{lstlisting}</span></p><h1><span>构建V矩阵</span></h1><p class="ds-markdown-paragraph"><span>V = []</span><br><span>for H in homographies:</span><br><span>v12 = compute_v_ij(H, 0, 1)</span><br><span>v11 = compute_v_ij(H, 0, 0)</span><br><span>v22 = compute_v_ij(H, 1, 1)</span></p><div class="md-code-block md-code-block-light"><div class="md-code-block-banner-wrap"><div class="md-code-block-banner md-code-block-banner-lite"><div class="_121d384"><div class="d2a24f03"><span class="d813de27">text</span></div><div class="d2a24f03 _246a029"><div class="efa13877"><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon" style="margin-right: 4px;"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.14923 4.02032C7.11191 4.02032 7.87977 4.02017 8.49591 4.07599C9.12122 4.1327 9.65786 4.25188 10.1414 4.53107C10.7201 4.8653 11.2008 5.34591 11.535 5.92462C11.8142 6.40818 11.9333 6.94482 11.9901 7.57013C12.0459 8.18625 12.0457 8.9542 12.0457 9.91681C12.0457 10.8795 12.0459 11.6474 11.9901 12.2635C11.9333 12.8888 11.8142 13.4254 11.535 13.909C11.2008 14.4877 10.7201 14.9683 10.1414 15.3026C9.65786 15.5817 9.12122 15.7009 8.49591 15.7576C7.87977 15.8134 7.1119 15.8133 6.14923 15.8133C5.18661 15.8133 4.41868 15.8134 3.80255 15.7576C3.17724 15.7009 2.6406 15.5817 2.15704 15.3026C1.57834 14.9684 1.09772 14.4877 0.763489 13.909C0.484305 13.4254 0.365123 12.8888 0.308411 12.2635C0.252587 11.6474 0.252747 10.8795 0.252747 9.91681C0.252747 8.95419 0.252603 8.18625 0.308411 7.57013C0.365123 6.94482 0.484305 6.40818 0.763489 5.92462C1.09771 5.3459 1.57833 4.86529 2.15704 4.53107C2.6406 4.25188 3.17724 4.1327 3.80255 4.07599C4.41868 4.02018 5.1866 4.02032 6.14923 4.02032ZM6.14923 5.37775C5.16175 5.37775 4.46628 5.37761 3.9256 5.42657C3.39428 5.47473 3.07853 5.56574 2.83575 5.70587C2.46313 5.92106 2.15348 6.23071 1.93829 6.60333C1.79817 6.84611 1.70715 7.16185 1.659 7.69318C1.61004 8.23385 1.61017 8.92934 1.61017 9.91681C1.61017 10.9043 1.61002 11.5998 1.659 12.1404C1.70715 12.6717 1.79817 12.9875 1.93829 13.2303C2.15349 13.6029 2.46315 13.9126 2.83575 14.1277C3.07853 14.2679 3.39428 14.3589 3.9256 14.407C4.46628 14.456 5.16176 14.4559 6.14923 14.4559C7.13675 14.4559 7.83218 14.456 8.37286 14.407C8.90419 14.3589 9.21993 14.2679 9.46271 14.1277C9.83529 13.9126 10.145 13.6029 10.3602 13.2303C10.5003 12.9875 10.5913 12.6718 10.6395 12.1404C10.6884 11.5998 10.6883 10.9043 10.6883 9.91681C10.6883 8.92935 10.6884 8.23385 10.6395 7.69318C10.5913 7.16185 10.5003 6.84611 10.3602 6.60333C10.145 6.23072 9.8353 5.92107 9.46271 5.70587C9.21993 5.56574 8.90418 5.47473 8.37286 5.42657C7.83218 5.3776 7.13676 5.37775 6.14923 5.37775ZM9.80157 0.367981C10.7637 0.367981 11.5313 0.367886 12.1473 0.423645C12.7725 0.480313 13.3093 0.598765 13.7928 0.877747C14.3716 1.21192 14.852 1.69355 15.1863 2.27228C15.4655 2.75575 15.5857 3.29165 15.6424 3.91681C15.6982 4.53301 15.6971 5.30161 15.6971 6.26447V7.8299C15.6971 8.29265 15.6989 8.58994 15.6649 8.84845C15.4667 10.3525 14.4009 11.5738 12.9832 11.9988V10.5467C13.6973 10.1903 14.2104 9.49662 14.3192 8.67169C14.3387 8.52348 14.3406 8.3358 14.3406 7.8299V6.26447C14.3406 5.27707 14.3398 4.58149 14.2908 4.04083C14.2427 3.50969 14.1526 3.19373 14.0125 2.95099C13.7974 2.5785 13.4875 2.2687 13.1151 2.05353C12.8723 1.91347 12.5563 1.82237 12.0252 1.77423C11.4846 1.72528 10.7888 1.7254 9.80157 1.7254H7.71466C6.75614 1.72559 5.92659 2.27697 5.52325 3.07892H4.07013C4.54215 1.51132 5.99314 0.368192 7.71466 0.367981H9.80157Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">复制</span></span><div class="ds-focus-ring"></div></button><button role="button" aria-disabled="false" class="ds-atom-button ds-text-button ds-text-button--with-icon"><div class="ds-icon ds-atom-button__icon" style="font-size: 16px; width: 16px; height: 16px; margin-right: 3px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M15.3695 11.411L15.1234 12.8866C14.8869 14.3042 13.6603 15.3436 12.223 15.3436H3.7767C2.33954 15.3434 1.11276 14.3042 0.876312 12.8866L0.630219 11.411L2.05405 11.1747L2.29916 12.6493C2.41969 13.3713 3.04472 13.9001 3.7767 13.9003H12.223C12.9551 13.9002 13.58 13.3713 13.7005 12.6493L13.9456 11.1747L15.3695 11.411ZM8.72202 8.994C8.77714 8.93934 8.83789 8.88106 8.90268 8.81627L12.4828 5.23424L13.5042 6.25572L9.92221 9.8358C9.63947 10.1185 9.3876 10.3732 9.15854 10.5575C8.91889 10.7503 8.6395 10.9224 8.28647 10.9784C8.09708 11.0083 7.9036 11.0083 7.7142 10.9784C7.36103 10.9224 7.08087 10.7503 6.84116 10.5575C6.61212 10.3732 6.36019 10.1185 6.07748 9.8358L2.49643 6.25572L3.51694 5.23424L7.09702 8.81627C7.16216 8.88142 7.22327 8.94006 7.27866 8.99498V1.3065H8.72202V8.994Z" fill="currentColor"></path></svg></div><span><span class="code-info-button-text">下载</span></span><div class="ds-focus-ring"></div></button></div></div></div></div></div><pre>V.append(v12)
V.append(v11 - v22)</pre><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _33882ae"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" class="_9bc997d _28d7e84"><path d="M-5.24537e-07 0C-2.34843e-07 6.62742 5.37258 12 12 12L0 12L-5.24537e-07 0Z" fill="currentColor"></path></svg></div><p class="ds-markdown-paragraph"><span>V = np.array(V)</span></p><h1><span>使用SVD求解 Vb = 0</span></h1><p class="ds-markdown-paragraph"><span>_, _, Vt = np.linalg.svd(V)</span><br><span>b = Vt[-1]</span><br><span>\end{lstlisting}</span></p><p class="ds-markdown-paragraph"><span>从 $\mathbf{B} = \mathbf{K}^{-T}\mathbf{K}^{-1}$ 中提取内参：</span></p><p class="ds-markdown-paragraph"><span>\begin{lstlisting}</span><br><span>B11, B12, B22, B13, B23, B33 = b</span></p><h1><span>计算内参</span></h1><p class="ds-markdown-paragraph"><span>v0 = (B12 * B13 - B11 * B23) / (B11 * B22 - B12 * B12)</span><br><span>lambda_ = B33 - (B13 * B13 + v0 * (B12 * B13 - B11 * B23)) / B11</span><br><span>fx = np.sqrt(abs(lambda_ / B11))</span><br><span>fy = np.sqrt(abs(lambda_ * B11 / (B11 * B22 - B12 * B12)))</span><br><span>s = -B12 * fx * fx * fy / lambda_</span><br><span>u0 = s * v0 / fy - B13 * fx * fx / lambda_</span></p><h1><span>构建内参矩阵 K</span></h1><p class="ds-markdown-paragraph"><span>K = np.array([</span><br><span>[fx, s, u0],</span><br><span>[0, fy, v0],</span><br><span>[0, 0, 1]</span><br><span>])</span><br><span>\end{lstlisting}</span></p><p class="ds-markdown-paragraph"><span>在实验结果方面，我们使用了25张图像，棋盘格内角点尺寸为$31 \times 23 = 713$个点。传统方法只成功检测了5张图像，总检测角点数为3565个点，其相机内参结果为焦距 $f_x = 910.4592$、$f_y = 857.4488$，主点 $(c_x, c_y) = (533.0859, 278.5895)$，倾斜因子 $s = 4.5027$。重投影误差在1.9470到5.3769像素之间，平均误差约3.75像素。</span></p><p class="ds-markdown-paragraph"><span>基于扇区的方法成功检测了19张图像，总检测角点数为13547个点，其相机内参结果为焦距 $f_x = 832.4417$、$f_y = 787.1441$，主点 $(c_x, c_y) = (498.2376, 334.6547)$，倾斜因子 $s = -6.0127$。重投影误差大部分在0.2-0.6像素之间，最小误差0.1832像素，最大误差5.3673像素，平均误差约1.05像素。</span></p><p class="ds-markdown-paragraph"><span>两种方法的对比显示，基于扇区的方法在检测图像数量、主点位置准确性和重投影误差方面都优于传统方法。传统方法由于数据量少（仅5张图像），结果受噪声影响更大，而基于扇区的方法由于能检测更多图像，提供了更稳定可靠的标定结果。</span></p><p class="ds-markdown-paragraph"><span>本实验结果与 OpenCV 验证结果存在一定差异，主要原因是 OpenCV 的 \texttt{calibrateCamera} 函数会同时估计畸变参数并进行非线性优化，而本实验使用的是线性方法（张正友标定法），未考虑镜头畸变。此外，主点位置的估计对噪声较为敏感，方法一由于数据量少，结果受噪声影响更大。</span></p><p class="ds-markdown-paragraph"><span>在重投影误差分析方面，方法一的平均误差较大，主要因为数据量不足；方法二的大部分图像误差较小，表明标定结果更可靠。部分图像误差较大可能是由于棋盘格位于图像边缘区域，畸变影响较大，或者棋盘格拍摄角度较大导致透视变形。</span></p><p class="ds-markdown-paragraph"><span>本实验成功实现了基于张正友标定法的相机标定算法，完成了棋盘格角点检测和世界坐标初始化，测试了两种角点检测方法，使用 DLT 算法计算单应性矩阵，通过张正友标定法求解相机内参矩阵，并计算了每张图像的重投影误差。</span></p><p class="ds-markdown-paragraph"><span>基于方法二（findChessboardCornersSB，19张图像）的标定结果更为可靠：焦距 $f_x = 832.44$、$f_y = 787.14$，主点 $(c_x, c_y) = (498.24, 334.65)$，平均重投影误差约1.05像素。标定结果与 OpenCV 验证结果基本一致，验证了算法的正确性。方法二由于能检测更多图像，提供了更稳定可靠的标定结果。</span></p><p class="ds-markdown-paragraph"><span>\end{document}</span></p>

---

### 用户

What is the definition of optical flow?

答案选项组

The apparent motion of brightness patterns in the image

The true 3D motion field

The change of object depth

The direction of image gradients
 
标记问题：问题 2
问题 21 分
Which of the following is not a key assumption of Lucas–Kanade?

答案选项组

Constant depth within a local window

Brightness constancy

Small motion

Spatial coherence
 
标记问题：问题 3
问题 31 分
Which type of region is the best for tracking?

答案选项组

High-texture / corner region

Flat region

Edge region

Homogeneous region
 
标记问题：问题 4
问题 41 分
Which technique helps reduce errors in gradient computation during optical flow estimation?

答案选项组

Low-pass filtering

Sharpening filter

Increasing gamma

Histogram equalization

---

### DeepSeek AI

<p>思考：</p><blockquote><p class="ds-markdown-paragraph"><span>首先，问题是关于光流的定义。光流是计算机视觉中的一个概念，指的是图像中亮度模式的表观运动。它并不是真正的3D运动场，而是2D图像上的运动表现。</span></p><p class="ds-markdown-paragraph"><span>所以，对于问题1："What is the definition of optical flow?"，选项是：</span></p><ul><li><p class="ds-markdown-paragraph"><span>The apparent motion of brightness patterns in the image</span></p></li><li><p class="ds-markdown-paragraph"><span>The true 3D motion field</span></p></li><li><p class="ds-markdown-paragraph"><span>The change of object depth</span></p></li><li><p class="ds-markdown-paragraph"><span>The direction of image gradients</span></p></li></ul><p class="ds-markdown-paragraph"><span>正确答案应该是"The apparent motion of brightness patterns in the image"。</span></p><p class="ds-markdown-paragraph"><span>接下来，问题2："Which of the following is not a key assumption of Lucas–Kanade?" Lucas-Kanade方法用于光流估计，其关键假设包括：</span></p><ul><li><p class="ds-markdown-paragraph"><span>亮度恒定性（Brightness constancy）</span></p></li><li><p class="ds-markdown-paragraph"><span>小运动（Small motion）</span></p></li><li><p class="ds-markdown-paragraph"><span>空间一致性（Spatial coherence）</span></p></li></ul><p class="ds-markdown-paragraph"><span>但选项中有"Constant depth within a local window"，这不是Lucas-Kanade的直接假设。Lucas-Kanade假设在局部窗口内运动是一致的，但深度不一定恒定。深度恒定可能与其他方法相关，但不是Lucas-Kanade的核心假设。</span></p><p class="ds-markdown-paragraph"><span>所以，对于问题2，正确答案应该是"Constant depth within a local window"。</span></p><p class="ds-markdown-paragraph"><span>问题3："Which type of region is the best for tracking?" 在光流跟踪中，高纹理区域或角点区域通常更容易跟踪，因为它们有丰富的梯度信息。平坦区域或均匀区域缺乏纹理，难以跟踪。边缘区域可能只有一维梯度，不如角点稳定。</span></p><p class="ds-markdown-paragraph"><span>所以，正确答案应该是"High-texture / corner region"。</span></p><p class="ds-markdown-paragraph"><span>问题4："Which technique helps reduce errors in gradient computation during optical flow estimation?" 在光流估计中，梯度计算容易受噪声影响。低通滤波可以帮助平滑图像，减少噪声，从而减少梯度计算的误差。锐化滤波会增强高频噪声，增加误差。增加伽马或直方图均衡化可能改变图像对比度，但不直接减少梯度误差。</span></p><p class="ds-markdown-paragraph"><span>所以，正确答案应该是"Low-pass filtering"。</span></p><p class="ds-markdown-paragraph"><span>现在，总结答案：</span></p><ul><li><p class="ds-markdown-paragraph"><span>问题1: The apparent motion of brightness patterns in the image</span></p></li><li><p class="ds-markdown-paragraph"><span>问题2: Constant depth within a local window</span></p></li><li><p class="ds-markdown-paragraph"><span>问题3: High-texture / corner region</span></p></li><li><p class="ds-markdown-paragraph"><span>问题4: Low-pass filtering</span></p></li></ul></blockquote><br/><p class="ds-markdown-paragraph"><span>根据计算机视觉中的光流理论，以下是每个问题的正确答案和简要解释：</span></p><h3><span>问题 1: What is the definition of optical flow?</span></h3><ul><li><p class="ds-markdown-paragraph"><strong><span>正确答案</span></strong><span>: The apparent motion of brightness patterns in the image</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>解释</span></strong><span>: 光流定义为图像中亮度模式的表观运动，它反映了像素在图像平面上的运动矢量，而不是真实的3D运动场或其他物理量。</span></p></li></ul><h3><span>问题 2: Which of the following is not a key assumption of Lucas–Kanade?</span></h3><ul><li><p class="ds-markdown-paragraph"><strong><span>正确答案</span></strong><span>: Constant depth within a local window</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>解释</span></strong><span>: Lucas-Kanade 方法的关键假设包括亮度恒定性、小运动和空间一致性，但局部窗口内深度恒定不是其假设，这更适用于其他3D运动估计方法。</span></p></li></ul><h3><span>问题 3: Which type of region is the best for tracking?</span></h3><ul><li><p class="ds-markdown-paragraph"><strong><span>正确答案</span></strong><span>: High-texture / corner region</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>解释</span></strong><span>: 高纹理或角点区域具有丰富的梯度信息，能提供更可靠的特征点进行跟踪，而平坦区域、边缘区域或均匀区域缺乏足够的纹理变化，容易导致跟踪失败。</span></p></li></ul><h3><span>问题 4: Which technique helps reduce errors in gradient computation during optical flow estimation?</span></h3><ul><li><p class="ds-markdown-paragraph"><strong><span>正确答案</span></strong><span>: Low-pass filtering</span></p></li><li><p class="ds-markdown-paragraph"><strong><span>解释</span></strong><span>: 低通滤波可以平滑图像，减少噪声对梯度计算的影响，从而提高光流估计的准确性。其他选项如锐化滤波、增加伽马或直方图均衡化可能引入更多误差。</span></p></li></ul>

