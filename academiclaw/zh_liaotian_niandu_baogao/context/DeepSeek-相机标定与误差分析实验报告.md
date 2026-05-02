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

帮我把这份报告的分小节适当变为完整连贯的段落，提高文本内容的连续性和连贯性

---

### DeepSeek AI

<p>思考：</p><blockquote><p class="ds-markdown-paragraph"><span>我们首先将分小节的文本整合成连贯的段落，同时保持逻辑清晰。我们将按照以下结构进行重组：</span></p><ol start="1"><li><p class="ds-markdown-paragraph"><span>引言：介绍实验目标、流程和要求。</span></p></li><li><p class="ds-markdown-paragraph"><span>方法：详细说明世界坐标初始化、角点检测（两种方法）、单应性矩阵计算、张正友标定法。</span></p></li><li><p class="ds-markdown-paragraph"><span>结果：分别展示两种方法的结果，包括内参和重投影误差，并进行对比。</span></p></li><li><p class="ds-markdown-paragraph"><span>分析：对两种角点检测方法、内参对比、重投影误差进行分析，并给出方法选择建议。</span></p></li><li><p class="ds-markdown-paragraph"><span>结论：总结实验工作和最终结果。</span></p></li></ol><p class="ds-markdown-paragraph"><span>我们将尽量使段落之间过渡自然，避免使用过多的列举和标题，而是用连贯的叙述将内容串联起来。</span></p></blockquote><br/><p class="ds-markdown-paragraph"><span>\documentclass[UTF8]{ctexart}</span></p><p class="ds-markdown-paragraph"><span>%=================================================</span><br><span>% 导入所需宏包</span><br><span>%=================================================</span><br><span>\usepackage{amsmath}          % AMS数学公式环境</span><br><span>\usepackage{amssymb}          % AMS数学符号</span><br><span>\usepackage{amsfonts}         % AMS数学字体</span><br><span>\usepackage[a4paper, margin=1in]{geometry} % 设置页面边距</span><br><span>\usepackage{hyperref}         % 创建超链接</span><br><span>\usepackage[UTF8]{ctex}</span><br><span>\usepackage{amsmath,amssymb}</span><br><span>\usepackage{graphicx}</span><br><span>\usepackage{booktabs}</span><br><span>\usepackage{listings}</span><br><span>\usepackage{xcolor}</span><br><span>\usepackage{geometry}</span><br><span>\usepackage{float}</span><br><span>\usepackage{caption}</span></p><p class="ds-markdown-paragraph"><span>\geometry{left=2.5cm,right=2.5cm,top=2.5cm,bottom=2.5cm}</span></p><p class="ds-markdown-paragraph"><span>\lstset{</span><br><span>language=Python,</span><br><span>basicstyle=\ttfamily\small,</span><br><span>keywordstyle=\color{blue},</span><br><span>commentstyle=\color{green!60!black},</span><br><span>stringstyle=\color{orange},</span><br><span>numbers=left,</span><br><span>numberstyle=\tiny\color{gray},</span><br><span>frame=single,</span><br><span>breaklines=true,</span><br><span>showstringspaces=false,</span><br><span>tabsize=4</span><br><span>}</span><br><span>%=================================================</span><br><span>% 定义一些常用命令</span><br><span>%=================================================</span><br><span>% 定义粗体向量和矩阵命令</span><br><span>\newcommand{\bvec}[1]{\boldsymbol{#1}}</span><br><span>\newcommand{\bmat}[1]{\boldsymbol{#1}}</span></p><p class="ds-markdown-paragraph"><span>%=================================================</span><br><span>% 文档开始</span><br><span>%=================================================</span><br><span>\begin{document}</span></p><p class="ds-markdown-paragraph"><span>%=================================================</span><br><span>% 标题部分</span><br><span>%=================================================</span><br><span>\title{计算机视觉：第二次作业}</span><br><span>\author{黄逸隽 523030910202}</span><br><span>\date{截止日期：2025年12月1日}</span><br><span>\maketitle</span></p><p class="ds-markdown-paragraph"><span>\hrule\vspace{1em}</span></p><p class="ds-markdown-paragraph"><span>%=================================================</span><br><span>% 问题与解答</span><br><span>%=================================================</span><br><span>\section*{书面作业 }</span></p><p class="ds-markdown-paragraph"><span>\subsection*{问题 1}</span><br><span>\noindent\textbf{证明：}</span></p><p class="ds-markdown-paragraph"><span>我们的目标是找到使误差函数 </span><span class="katex"></span><span> 最小的 </span><span class="katex"></span><span> 和 </span><span class="katex"></span><span>，我们通过将 </span><span class="katex"></span><span> 对 </span><span class="katex"></span><span> 和 </span><span class="katex"></span><span> 的偏导数设为零来求解。</span></p><p class="ds-markdown-paragraph"><span>首先，我们计算 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi>E</mi></mrow><annotation encoding="application/x-tex">E</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.6833em;"></span><span class="mord mathnormal" style="margin-right:0.05764em;">E</span></span></span></span><span> 关于 </span><span class="katex"></span><span> 的偏导数：</span></p><span class="katex-display ds-markdown-math"><span class="katex"></span></span><p class="ds-markdown-paragraph"><span>使用向量求导法则 </span><span class="katex"></span><span>，我们得到：</span></p><span class="katex-display ds-markdown-math"><span class="katex"></span></span><p class="ds-markdown-paragraph"><span>令偏导数为零向量 </span><span class="katex"></span><span>：</span></p><span class="katex-display ds-markdown-math"><span class="katex"></span></span><span class="katex-display ds-markdown-math"><span class="katex"></span></span><p class="ds-markdown-paragraph"><span>根据质心 </span><span class="katex"></span><span> 和 </span><span class="katex"></span><span> 的定义，上式可以写为：</span></p><span class="katex-display ds-markdown-math"><span class="katex"></span></span><p class="ds-markdown-paragraph"><span>两边同除以 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi>N</mi></mrow><annotation encoding="application/x-tex">N</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.6833em;"></span><span class="mord mathnormal" style="margin-right:0.10903em;">N</span></span></span></span><span>，我们得到最优 </span><span class="katex"></span><span> 和最优 </span><span class="katex"></span><span> 之间的关系：</span><br><span>\begin{equation} \label{eq:T_star}</span><br><span>\bvec{T}^* = \bar{\bvec{Y}} - \bmat{A}^*\bar{\bvec{X}}</span><br><span>\end{equation}</span><br><span>这证明了第一个公式。</span></p><p class="ds-markdown-paragraph"><span>接下来，我们将式 \eqref{eq:T_star} 的关系代入原始误差函数 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi>E</mi></mrow><annotation encoding="application/x-tex">E</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.6833em;"></span><span class="mord mathnormal" style="margin-right:0.05764em;">E</span></span></span></span><span> 中，以消除 </span><span class="katex"></span><span>。</span></p><span class="katex-display ds-markdown-math"><span class="katex"></span></span><p class="ds-markdown-paragraph"><span>我们定义中心化坐标：</span><span class="katex"></span><span> 和 </span><span class="katex"></span><span>。误差函数简化为：</span></p><span class="katex-display ds-markdown-math"><span class="katex"></span></span><p class="ds-markdown-paragraph"><span>现在，我们引入题目中定义的 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mn>3</mn><mo>×</mo><mi>N</mi></mrow><annotation encoding="application/x-tex">3 \times N</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.7278em;vertical-align:-0.0833em;"></span><span class="mord">3</span><span class="mspace" style="margin-right:0.2222em;"></span><span class="mbin">×</span><span class="mspace" style="margin-right:0.2222em;"></span></span><span class="base"><span class="strut" style="height:0.6833em;"></span><span class="mord mathnormal" style="margin-right:0.10903em;">N</span></span></span></span><span> 矩阵 </span><span class="katex"></span><span> 和 </span><span class="katex"></span><span>。误差函数可以写成矩阵的 Frobenius 范数形式：</span></p><span class="katex-display ds-markdown-math"><span class="katex"></span></span><p class="ds-markdown-paragraph"><span>使用迹（trace）的性质，</span><span class="katex"></span><span>，我们有：</span></p><span class="katex-display ds-markdown-math"><span class="katex"></span></span><p class="ds-markdown-paragraph"><span>现在计算 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi>E</mi></mrow><annotation encoding="application/x-tex">E</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.6833em;"></span><span class="mord mathnormal" style="margin-right:0.05764em;">E</span></span></span></span><span> 关于 </span><span class="katex"></span><span> 的偏导数。使用矩阵求导法则 </span><span class="katex"></span><span>，</span><span class="katex"></span><span> 和 </span><span class="katex"></span><span>：</span></p><span class="katex-display ds-markdown-math"><span class="katex"></span></span><p class="ds-markdown-paragraph"><span>（注：展开式中的 </span><span class="katex"></span><span> 和 </span><span class="katex"></span><span> 是相等的标量，它们的和对 </span><span class="katex"></span><span> 的导数是 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mn>2</mn><mo stretchy="false">(</mo><mi mathvariant="script">Y</mi><msup><mi mathvariant="script">X</mi><mi>T</mi></msup><msup><mo stretchy="false">)</mo><mi>T</mi></msup><mo>=</mo><mn>2</mn><mi mathvariant="script">X</mi><msup><mi mathvariant="script">Y</mi><mi>T</mi></msup></mrow><annotation encoding="application/x-tex">2(\mathcal{Y}\mathcal{X}^T)^T = 2\mathcal{X}\mathcal{Y}^T</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:1.0913em;vertical-align:-0.25em;"></span><span class="mord">2</span><span class="mopen">(</span><span class="mord mathcal" style="margin-right:0.08222em;">Y</span><span class="mord"><span class="mord mathcal" style="margin-right:0.14643em;">X</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height:0.8413em;"><span style="top:-3.063em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mathnormal mtight" style="margin-right:0.13889em;">T</span></span></span></span></span></span></span></span><span class="mclose"><span class="mclose">)</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height:0.8413em;"><span style="top:-3.063em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mathnormal mtight" style="margin-right:0.13889em;">T</span></span></span></span></span></span></span></span><span class="mspace" style="margin-right:0.2778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right:0.2778em;"></span></span><span class="base"><span class="strut" style="height:0.9386em;vertical-align:-0.0972em;"></span><span class="mord">2</span><span class="mord mathcal" style="margin-right:0.14643em;">X</span><span class="mord"><span class="mord mathcal" style="margin-right:0.08222em;">Y</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height:0.8413em;"><span style="top:-3.063em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mathnormal mtight" style="margin-right:0.13889em;">T</span></span></span></span></span></span></span></span></span></span></span><span> ，然而从整个表达式来看，更直接的求导方式是得到 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mo>−</mo><mn>2</mn><mi mathvariant="script">Y</mi><msup><mi mathvariant="script">X</mi><mi>T</mi></msup></mrow><annotation encoding="application/x-tex">-2\mathcal{Y}\mathcal{X}^T</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.9386em;vertical-align:-0.0972em;"></span><span class="mord">−</span><span class="mord">2</span><span class="mord mathcal" style="margin-right:0.08222em;">Y</span><span class="mord"><span class="mord mathcal" style="margin-right:0.14643em;">X</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height:0.8413em;"><span style="top:-3.063em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mathnormal mtight" style="margin-right:0.13889em;">T</span></span></span></span></span></span></span></span></span></span></span><span>。为保持一致性，我们直接对 Frobenius 范数求导。）</span></p><p class="ds-markdown-paragraph"><span>令偏导数为零矩阵 </span><span class="katex"></span><span>：</span></p><span class="katex-display ds-markdown-math"><span class="katex"></span></span><span class="katex-display ds-markdown-math"><span class="katex"></span></span><p class="ds-markdown-paragraph"><span>假设矩阵 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi mathvariant="script">X</mi><msup><mi mathvariant="script">X</mi><mi>T</mi></msup></mrow><annotation encoding="application/x-tex">\mathcal{X}\mathcal{X}^T</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.8413em;"></span><span class="mord mathcal" style="margin-right:0.14643em;">X</span><span class="mord"><span class="mord mathcal" style="margin-right:0.14643em;">X</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height:0.8413em;"><span style="top:-3.063em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mathnormal mtight" style="margin-right:0.13889em;">T</span></span></span></span></span></span></span></span></span></span></span><span> 是可逆的（这要求中心化的点集 </span><span class="katex"></span><span> 不是共面或共线的），我们可以在等式右侧乘以其逆矩阵：</span></p><span class="katex-display ds-markdown-math"><span class="katex"></span></span><p class="ds-markdown-paragraph"><span>这证明了第二个公式。</span><br><span>\hfill </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi mathvariant="normal">■</mi></mrow><annotation encoding="application/x-tex">\blacksquare</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.675em;"></span><span class="mord amsrm">■</span></span></span></span></p><p class="ds-markdown-paragraph"><span>\vspace{2em}</span></p><p class="ds-markdown-paragraph"><span>\subsubsection*{(b) 证明}</span><br><span>证明估计该变换需要的最少对应点数量是4。</span><br><span>\vspace{1em}</span></p><p class="ds-markdown-paragraph"><span>\noindent\textbf{证明：}</span></p><p class="ds-markdown-paragraph"><span>我们通过分析变换中的未知数数量和每个点对应提供的约束数量来确定最少需要的点数。</span></p><p class="ds-markdown-paragraph"><span>变换 </span><span class="katex"></span><span> 包含两个部分：旋转/缩放/错切矩阵 </span><span class="katex"></span><span>，包含 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mn>3</mn><mo>×</mo><mn>3</mn><mo>=</mo><mn>9</mn></mrow><annotation encoding="application/x-tex">3 \times 3 = 9</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.7278em;vertical-align:-0.0833em;"></span><span class="mord">3</span><span class="mspace" style="margin-right:0.2222em;"></span><span class="mbin">×</span><span class="mspace" style="margin-right:0.2222em;"></span></span><span class="base"><span class="strut" style="height:0.6444em;"></span><span class="mord">3</span><span class="mspace" style="margin-right:0.2778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right:0.2778em;"></span></span><span class="base"><span class="strut" style="height:0.6444em;"></span><span class="mord">9</span></span></span></span><span> 个未知参数；平移向量 </span><span class="katex"></span><span>，包含 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mn>3</mn><mo>×</mo><mn>1</mn><mo>=</mo><mn>3</mn></mrow><annotation encoding="application/x-tex">3 \times 1 = 3</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.7278em;vertical-align:-0.0833em;"></span><span class="mord">3</span><span class="mspace" style="margin-right:0.2222em;"></span><span class="mbin">×</span><span class="mspace" style="margin-right:0.2222em;"></span></span><span class="base"><span class="strut" style="height:0.6444em;"></span><span class="mord">1</span><span class="mspace" style="margin-right:0.2778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right:0.2778em;"></span></span><span class="base"><span class="strut" style="height:0.6444em;"></span><span class="mord">3</span></span></span></span><span> 个未知参数。因此，总共有 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mn>9</mn><mo>+</mo><mn>3</mn><mo>=</mo><mn>12</mn></mrow><annotation encoding="application/x-tex">9 + 3 = 12</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.7278em;vertical-align:-0.0833em;"></span><span class="mord">9</span><span class="mspace" style="margin-right:0.2222em;"></span><span class="mbin">+</span><span class="mspace" style="margin-right:0.2222em;"></span></span><span class="base"><span class="strut" style="height:0.6444em;"></span><span class="mord">3</span><span class="mspace" style="margin-right:0.2778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right:0.2778em;"></span></span><span class="base"><span class="strut" style="height:0.6444em;"></span><span class="mord">12</span></span></span></span><span> 个独立的未知参数需要求解。</span></p><p class="ds-markdown-paragraph"><span>每一组对应点 </span><span class="katex"></span><span> 提供一个矢量方程：</span><span class="katex"></span><span>。这个方程是在 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><msup><mi mathvariant="double-struck">R</mi><mn>3</mn></msup></mrow><annotation encoding="application/x-tex">\mathbb{R}^3</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.8141em;"></span><span class="mord"><span class="mord mathbb">R</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height:0.8141em;"><span style="top:-3.063em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">3</span></span></span></span></span></span></span></span></span></span></span><span> 空间中的，它可以分解为3个独立的标量方程，所以每一组对应点能够提供3个线性方程。为了唯一地确定所有12个未知参数，我们需要的独立方程数量必须至少等于未知数的数量。设 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi>N</mi></mrow><annotation encoding="application/x-tex">N</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.6833em;"></span><span class="mord mathnormal" style="margin-right:0.10903em;">N</span></span></span></span><span> 为所需的最少对应点数量，则 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mn>3</mn><mi>N</mi><mo>≥</mo><mn>12</mn></mrow><annotation encoding="application/x-tex">3N \ge 12</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.8193em;vertical-align:-0.136em;"></span><span class="mord">3</span><span class="mord mathnormal" style="margin-right:0.10903em;">N</span><span class="mspace" style="margin-right:0.2778em;"></span><span class="mrel">≥</span><span class="mspace" style="margin-right:0.2778em;"></span></span><span class="base"><span class="strut" style="height:0.6444em;"></span><span class="mord">12</span></span></span></span><span>，即 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi>N</mi><mo>≥</mo><mn>4</mn></mrow><annotation encoding="application/x-tex">N \ge 4</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.8193em;vertical-align:-0.136em;"></span><span class="mord mathnormal" style="margin-right:0.10903em;">N</span><span class="mspace" style="margin-right:0.2778em;"></span><span class="mrel">≥</span><span class="mspace" style="margin-right:0.2778em;"></span></span><span class="base"><span class="strut" style="height:0.6444em;"></span><span class="mord">4</span></span></span></span><span>。因此，我们至少需要4组对应点。</span></p><p class="ds-markdown-paragraph"><span>拥有 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi>N</mi><mo>=</mo><mn>4</mn></mrow><annotation encoding="application/x-tex">N=4</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.6833em;"></span><span class="mord mathnormal" style="margin-right:0.10903em;">N</span><span class="mspace" style="margin-right:0.2778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right:0.2778em;"></span></span><span class="base"><span class="strut" style="height:0.6444em;"></span><span class="mord">4</span></span></span></span><span> 组点只是一个必要条件，不是充分条件。为了得到唯一解，这些方程必须是线性无关的。从(a)部分的推导中，我们知道 </span><span class="katex"></span><span> 的解为 </span><span class="katex"></span><span>。这个解存在的关键在于矩阵 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi mathvariant="script">X</mi><msup><mi mathvariant="script">X</mi><mi>T</mi></msup></mrow><annotation encoding="application/x-tex">\mathcal{X}\mathcal{X}^T</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.8413em;"></span><span class="mord mathcal" style="margin-right:0.14643em;">X</span><span class="mord"><span class="mord mathcal" style="margin-right:0.14643em;">X</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height:0.8413em;"><span style="top:-3.063em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mathnormal mtight" style="margin-right:0.13889em;">T</span></span></span></span></span></span></span></span></span></span></span><span> 是可逆的。矩阵 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi mathvariant="script">X</mi><msup><mi mathvariant="script">X</mi><mi>T</mi></msup></mrow><annotation encoding="application/x-tex">\mathcal{X}\mathcal{X}^T</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.8413em;"></span><span class="mord mathcal" style="margin-right:0.14643em;">X</span><span class="mord"><span class="mord mathcal" style="margin-right:0.14643em;">X</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height:0.8413em;"><span style="top:-3.063em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mathnormal mtight" style="margin-right:0.13889em;">T</span></span></span></span></span></span></span></span></span></span></span><span> 是一个 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mn>3</mn><mo>×</mo><mn>3</mn></mrow><annotation encoding="application/x-tex">3 \times 3</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.7278em;vertical-align:-0.0833em;"></span><span class="mord">3</span><span class="mspace" style="margin-right:0.2222em;"></span><span class="mbin">×</span><span class="mspace" style="margin-right:0.2222em;"></span></span><span class="base"><span class="strut" style="height:0.6444em;"></span><span class="mord">3</span></span></span></span><span> 的矩阵，定义为 </span><span class="katex"></span><span>，其中 </span><span class="katex"></span><span>。为了使 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi mathvariant="script">X</mi><msup><mi mathvariant="script">X</mi><mi>T</mi></msup></mrow><annotation encoding="application/x-tex">\mathcal{X}\mathcal{X}^T</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.8413em;"></span><span class="mord mathcal" style="margin-right:0.14643em;">X</span><span class="mord"><span class="mord mathcal" style="margin-right:0.14643em;">X</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height:0.8413em;"><span style="top:-3.063em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mathnormal mtight" style="margin-right:0.13889em;">T</span></span></span></span></span></span></span></span></span></span></span><span> 可逆，它的秩必须是3。这意味着由中心化向量 </span><span class="katex"></span><span> 张成的子空间维度必须是3。</span></p><p class="ds-markdown-paragraph"><span>如果 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi>N</mi><mo>&lt;</mo><mn>4</mn></mrow><annotation encoding="application/x-tex">N &lt; 4</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.7224em;vertical-align:-0.0391em;"></span><span class="mord mathnormal" style="margin-right:0.10903em;">N</span><span class="mspace" style="margin-right:0.2778em;"></span><span class="mrel">&lt;</span><span class="mspace" style="margin-right:0.2778em;"></span></span><span class="base"><span class="strut" style="height:0.6444em;"></span><span class="mord">4</span></span></span></span><span>，例如 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi>N</mi><mo>=</mo><mn>3</mn></mrow><annotation encoding="application/x-tex">N=3</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.6833em;"></span><span class="mord mathnormal" style="margin-right:0.10903em;">N</span><span class="mspace" style="margin-right:0.2778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right:0.2778em;"></span></span><span class="base"><span class="strut" style="height:0.6444em;"></span><span class="mord">3</span></span></span></span><span>，三个点 </span><span class="katex"></span><span> 最多是共面的（通常是，除非它们共线）。它们的中心化向量 </span><span class="katex"></span><span> 也将位于一个过原点的平面上，因此它们张成的空间维度最多为2，导致 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi mathvariant="script">X</mi><msup><mi mathvariant="script">X</mi><mi>T</mi></msup></mrow><annotation encoding="application/x-tex">\mathcal{X}\mathcal{X}^T</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.8413em;"></span><span class="mord mathcal" style="margin-right:0.14643em;">X</span><span class="mord"><span class="mord mathcal" style="margin-right:0.14643em;">X</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height:0.8413em;"><span style="top:-3.063em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mathnormal mtight" style="margin-right:0.13889em;">T</span></span></span></span></span></span></span></span></span></span></span><span> 是奇异的。如果 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi>N</mi><mo>=</mo><mn>4</mn></mrow><annotation encoding="application/x-tex">N=4</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.6833em;"></span><span class="mord mathnormal" style="margin-right:0.10903em;">N</span><span class="mspace" style="margin-right:0.2778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right:0.2778em;"></span></span><span class="base"><span class="strut" style="height:0.6444em;"></span><span class="mord">4</span></span></span></span><span>，并且这4个点 </span><span class="katex"></span><span> 是 \textbf{共面（coplanar）}的，那么它们的中心化向量 </span><span class="katex"></span><span> 也将位于一个过原点的平面上。这样，它们张成的空间维度仍然是2，</span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi mathvariant="script">X</mi><msup><mi mathvariant="script">X</mi><mi>T</mi></msup></mrow><annotation encoding="application/x-tex">\mathcal{X}\mathcal{X}^T</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.8413em;"></span><span class="mord mathcal" style="margin-right:0.14643em;">X</span><span class="mord"><span class="mord mathcal" style="margin-right:0.14643em;">X</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height:0.8413em;"><span style="top:-3.063em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mathnormal mtight" style="margin-right:0.13889em;">T</span></span></span></span></span></span></span></span></span></span></span><span> 依然是奇异的。因此，为了保证 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi mathvariant="script">X</mi><msup><mi mathvariant="script">X</mi><mi>T</mi></msup></mrow><annotation encoding="application/x-tex">\mathcal{X}\mathcal{X}^T</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.8413em;"></span><span class="mord mathcal" style="margin-right:0.14643em;">X</span><span class="mord"><span class="mord mathcal" style="margin-right:0.14643em;">X</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height:0.8413em;"><span style="top:-3.063em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mathnormal mtight" style="margin-right:0.13889em;">T</span></span></span></span></span></span></span></span></span></span></span><span> 满秩（秩为3），我们不仅需要 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi>N</mi><mo>≥</mo><mn>4</mn></mrow><annotation encoding="application/x-tex">N \ge 4</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.8193em;vertical-align:-0.136em;"></span><span class="mord mathnormal" style="margin-right:0.10903em;">N</span><span class="mspace" style="margin-right:0.2778em;"></span><span class="mrel">≥</span><span class="mspace" style="margin-right:0.2778em;"></span></span><span class="base"><span class="strut" style="height:0.6444em;"></span><span class="mord">4</span></span></span></span><span>，还要求这4个点 </span><span class="katex"></span><span> \textbf{不能共面（non-coplanar）}。当这4个点不共面时，它们构成的中心化向量可以张成整个 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><msup><mi mathvariant="double-struck">R</mi><mn>3</mn></msup></mrow><annotation encoding="application/x-tex">\mathbb{R}^3</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.8141em;"></span><span class="mord"><span class="mord mathbb">R</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height:0.8141em;"><span style="top:-3.063em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">3</span></span></span></span></span></span></span></span></span></span></span><span> 空间，保证了 </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi mathvariant="script">X</mi><msup><mi mathvariant="script">X</mi><mi>T</mi></msup></mrow><annotation encoding="application/x-tex">\mathcal{X}\mathcal{X}^T</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.8413em;"></span><span class="mord mathcal" style="margin-right:0.14643em;">X</span><span class="mord"><span class="mord mathcal" style="margin-right:0.14643em;">X</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height:0.8413em;"><span style="top:-3.063em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mathnormal mtight" style="margin-right:0.13889em;">T</span></span></span></span></span></span></span></span></span></span></span><span> 的可逆性，从而可以唯一确定 </span><span class="katex"></span><span> 和 </span><span class="katex"></span><span>。</span></p><p class="ds-markdown-paragraph"><span>\textbf{结论：} 估计该3D仿射变换所需的最少对应点数量是4，并且这4个源点 </span><span class="katex"></span><span> 不能共面。</span><br><span>\hfill </span><span class="katex"><span class="katex-mathml"><math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi mathvariant="normal">■</mi></mrow><annotation encoding="application/x-tex">\blacksquare</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.675em;"></span><span class="mord amsrm">■</span></span></span></span></p><p class="ds-markdown-paragraph"><span>\section*{编程任务}</span><br><span>\section{任务简要说明}</span></p><p class="ds-markdown-paragraph"><span>本次实验的目标是完成相机标定，通过一系列棋盘格图像推导出相机的内参矩阵，包括焦距 $(f_x, f_y)$、主点坐标 $(c_x, c_y)$ 以及每张图像对应的重投影误差。标准的相机标定流程通常包括：使用已知尺寸的棋盘格图案定义3D点的世界坐标，从不同视角拍摄棋盘格图像，检测棋盘格角点以获取每个3D点在不同图像中的像素坐标 $(u, v)$，最后使用线性代数方法求解相机参数。</span></p><p class="ds-markdown-paragraph"><span>实验要求只允许使用基本的 Python、NumPy 和 OpenCV 函数，允许使用 \texttt{cv2.findChessboardCorners} 等角点检测函数，但不允许使用 \texttt{cv2.calibrateCamera} 等“魔法”函数求解内参（仅用于验证）。世界坐标可简化为 $(0,0), (1,0), (2,0), \ldots$，结果以棋盘格方格大小为单位。</span></p><p class="ds-markdown-paragraph"><span>\section{核心实现说明}</span></p><p class="ds-markdown-paragraph"><span>在实现过程中，首先初始化棋盘格的世界坐标点。棋盘格的世界坐标点定义在 $Z=0$ 的平面上，坐标按 $(0,0,0), (1,0,0), (2,0,0), \ldots$ 的方式排列，具体实现如下：</span></p><p class="ds-markdown-paragraph"><span>\begin{lstlisting}</span><br><span>def init_world_points(pattern_size):</span><br><span># 生成棋盘格的世界坐标</span><br><span># 点排列为 (0,0,0), (1,0,0), (2,0,0), ... 在XY平面上 (Z=0)</span><br><span>objp = np.zeros((pattern_size[0] * pattern_size[1], 3), np.float32)</span><br><span>objp[:, :2] = np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2)</span><br><span>return objp</span><br><span>\end{lstlisting}</span></p><p class="ds-markdown-paragraph"><span>\subsection{棋盘格角点检测}</span><br><span>本实验测试了两种角点检测方法。第一种是使用 OpenCV 的传统 \texttt{findChessboardCorners} 函数，并通过 \texttt{cornerSubPix} 进行亚像素精度优化。第二种是使用 OpenCV 4.0+ 引入的 \texttt{findChessboardCornersSB} 函数（SB = Sector Based），该方法更加鲁棒。</span></p><p class="ds-markdown-paragraph"><span>\begin{lstlisting}</span></p><h1><span>方法一：findChessboardCorners</span></h1><p class="ds-markdown-paragraph"><span>def detect_corners(image, pattern_size):</span><br><span>gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)</span><br><span>ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)</span><br><span>if ret:</span><br><span># 亚像素精度优化</span><br><span>criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)</span><br><span>corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)</span><br><span>return corners.reshape(-1, 2)</span><br><span>return None</span></p><h1><span>方法二：findChessboardCornersSB</span></h1><p class="ds-markdown-paragraph"><span>def detect_corners(image, pattern_size):</span><br><span>gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)</span><br><span>ret, corners = cv2.findChessboardCornersSB(gray, pattern_size)</span><br><span>if ret:</span><br><span>return corners.reshape(-1, 2)</span><br><span>return None</span><br><span>\end{lstlisting}</span></p><p class="ds-markdown-paragraph"><span>两种角点检测方法对比如下表所示。可以看出，方法二（\texttt{findChessboardCornersSB}）在成功检测图像数、对图像质量的要求、对棋盘格角度的要求以及处理模糊图像等方面均优于方法一。</span></p><p class="ds-markdown-paragraph"><span>\begin{table}[H]</span><br><span>\centering</span><br><span>\caption{两种角点检测方法对比}</span><br><span>\begin{tabular}{lcc}</span><br><span>\toprule</span><br><span>\textbf{特性} &amp; \textbf{findChessboardCorners} &amp; \textbf{findChessboardCornersSB} \</span><br><span>\midrule</span><br><span>成功检测图像数 &amp; 5/25 &amp; 19/25 \</span><br><span>对图像质量要求 &amp; 高 &amp; 低 \</span><br><span>对棋盘格角度要求 &amp; 严格 &amp; 宽松 \</span><br><span>处理模糊图像 &amp; 较差 &amp; 较好 \</span><br><span>OpenCV版本要求 &amp; 所有版本 &amp; 4.0+ \</span><br><span>\bottomrule</span><br><span>\end{tabular}</span><br><span>\end{table}</span></p><p class="ds-markdown-paragraph"><span>\subsection{单应性矩阵计算}</span><br><span>使用直接线性变换（DLT）算法计算每张图像的单应性矩阵 $\mathbf{H}$。对于世界坐标 $(X, Y)$ 和图像坐标 $(u, v)$，有 $\begin{bmatrix} u \ v \ 1 \end{bmatrix} \sim \mathbf{H} \begin{bmatrix} X \ Y \ 1 \end{bmatrix}$。构建方程组 $\mathbf{A}\mathbf{h} = \mathbf{0}$，使用 SVD 求解。</span></p><p class="ds-markdown-paragraph"><span>\subsection{张正友标定法求解内参}</span><br><span>使用张正友标定法，通过多张图像的单应性矩阵求解相机内参。首先构建约束矩阵，定义向量 $\mathbf{v}_{ij}$。根据约束条件 $\mathbf{h}_1^T \mathbf{B} \mathbf{h}_2 = 0$ 和 $\mathbf{h}_1^T \mathbf{B} \mathbf{h}_1 = \mathbf{h}_2^T \mathbf{B} \mathbf{h}_2$，构建矩阵 $\mathbf{V}$，并使用 SVD 求解。最后从 $\mathbf{B} = \mathbf{K}^{-T}\mathbf{K}^{-1}$ 中提取内参。</span></p><p class="ds-markdown-paragraph"><span>\section{实验结果}</span></p><p class="ds-markdown-paragraph"><span>\subsection{数据集信息}</span><br><span>实验使用了25张棋盘格图像，棋盘格内角点尺寸为 $31 \times 23 = 713$ 个点。</span></p><p class="ds-markdown-paragraph"><span>\subsection{方法一结果：findChessboardCorners（传统方法）}</span><br><span>方法一成功检测了5张图像的棋盘格，总检测角点数为 $5 \times 713 = 3565$ 个点。相机内参标定结果如表所示，内参矩阵 $\mathbf{K}_1$ 为：</span><br><span>\begin{equation}</span><br><span>\mathbf{K}_1 = \begin{bmatrix}</span><br><span>910.4592 &amp; 4.5027 &amp; 533.0859 \</span><br><span>0 &amp; 857.4488 &amp; 278.5895 \</span><br><span>0 &amp; 0 &amp; 1</span><br><span>\end{bmatrix}</span><br><span>\end{equation}</span></p><p class="ds-markdown-paragraph"><span>重投影误差方面，最小误差为1.9470像素（Image 2），最大误差为5.3769像素（Image 5），平均误差约为3.75像素。</span></p><p class="ds-markdown-paragraph"><span>\subsection{方法二结果：findChessboardCornersSB（基于扇区方法）}</span><br><span>方法二成功检测了19张图像的棋盘格，总检测角点数为 $19 \times 713 = 13547$ 个点。相机内参标定结果如表所示，内参矩阵 $\mathbf{K}_2$ 为：</span><br><span>\begin{equation}</span><br><span>\mathbf{K}_2 = \begin{bmatrix}</span><br><span>832.4417 &amp; -6.0127 &amp; 498.2376 \</span><br><span>0 &amp; 787.1441 &amp; 334.6547 \</span><br><span>0 &amp; 0 &amp; 1</span><br><span>\end{bmatrix}</span><br><span>\end{equation}</span></p><p class="ds-markdown-paragraph"><span>重投影误差方面，最小误差为0.1832像素（Image 8），最大误差为5.3673像素（Image 15），大部分图像误差在0.2-0.6像素之间。</span></p><p class="ds-markdown-paragraph"><span>\subsection{两种方法结果对比}</span><br><span>两种方法标定结果综合对比如下表所示。可以看出，方法二在检测图像数、内参估计的合理性（主点更接近图像中心）以及平均重投影误差方面均优于方法一。</span></p><p class="ds-markdown-paragraph"><span>\begin{table}[H]</span><br><span>\centering</span><br><span>\caption{两种方法标定结果综合对比}</span><br><span>\begin{tabular}{lccc}</span><br><span>\toprule</span><br><span>\textbf{指标} &amp; \textbf{方法一} &amp; \textbf{方法二} &amp; \textbf{评价} \</span><br><span>\midrule</span><br><span>检测图像数 &amp; 5 &amp; 19 &amp; 方法二更多 \</span><br><span>焦距 $f_x$ &amp; 910.46 &amp; 832.44 &amp; -- \</span><br><span>焦距 $f_y$ &amp; 857.45 &amp; 787.14 &amp; -- \</span><br><span>主点 $c_x$ &amp; 533.09 &amp; 498.24 &amp; 方法二更接近图像中心 \</span><br><span>主点 $c_y$ &amp; 278.59 &amp; 334.65 &amp; 方法二更接近图像中心 \</span><br><span>平均重投影误差 &amp; $\sim$3.75 px &amp; $\sim$1.05 px &amp; 方法二更小 \</span><br><span>\bottomrule</span><br><span>\end{tabular}</span><br><span>\end{table}</span></p><p class="ds-markdown-paragraph"><span>\section{结果分析}</span></p><p class="ds-markdown-paragraph"><span>在角点检测方法方面，方法一（传统方法）对图像质量要求较高，只能检测到5张图像，导致标定数据量较少，结果稳定性较差。而方法二（基于扇区的方法）更加鲁棒，能检测到19张图像，数据量充足，标定结果更加可靠。</span></p><p class="ds-markdown-paragraph"><span>在内参对比方面，本实验结果与 OpenCV 验证结果存在一定差异，主要原因包括：OpenCV 的 \texttt{calibrateCamera} 函数会同时估计畸变参数并进行非线性优化；本实验使用的是线性方法（张正友标定法），未考虑镜头畸变；主点位置的估计对噪声较为敏感；方法一由于数据量少（仅5张图像），结果受噪声影响更大。</span></p><p class="ds-markdown-paragraph"><span>在重投影误差分析方面，方法一的平均误差约3.75像素，较大，主要因为数据量不足；方法二的大部分图像误差在0.2-0.6像素之间，表明标定结果更可靠。部分图像误差较大（如Image 15），可能原因是棋盘格位于图像边缘区域，畸变影响较大，或者棋盘格拍摄角度较大，导致透视变形。根据作业要求，应尽量使用图像中心区域的点来减少畸变影响。</span></p><p class="ds-markdown-paragraph"><span>在方法选择建议方面，如果图像质量较好且数量充足，两种方法均可使用；但如果图像存在模糊、倾斜等问题，建议使用 \texttt{findChessboardCornersSB}。更多的有效图像可以提供更稳定的标定结果。</span></p><p class="ds-markdown-paragraph"><span>\section{结论}</span></p><p class="ds-markdown-paragraph"><span>本实验成功实现了基于张正友标定法的相机标定算法，完成了棋盘格角点检测和世界坐标初始化，测试了两种角点检测方法，使用 DLT 算法计算单应性矩阵，通过张正友标定法求解相机内参矩阵，并计算了每张图像的重投影误差。</span></p><p class="ds-markdown-paragraph"><span>基于方法二（findChessboardCornersSB，19张图像）的标定结果更为可靠：焦距 $f_x = 832.44$, $f_y = 787.14$；主点 $(c_x, c_y) = (498.24, 334.65)$；平均重投影误差约 1.05 像素。标定结果与 OpenCV 验证结果基本一致，验证了算法的正确性。方法二由于能检测更多图像，提供了更稳定可靠的标定结果。</span></p><p class="ds-markdown-paragraph"><span>\end{document}</span></p>

