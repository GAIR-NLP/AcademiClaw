### 用户

\documentclass[11pt, letterpaper]{article}
\usepackage[utf8]{inputenc}
\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage{amssymb}
\usepackage{graphicx}
\usepackage{float}
\usepackage{listings}
\usepackage{xcolor}
\usepackage{geometry}
\usepackage{subcaption}
\usepackage{amsmath, amssymb, amsfonts}
\usepackage{geometry}
\usepackage{graphicx}

% Set page margins
\geometry{
    letterpaper,
    total={6.5in, 9in},
    left=1in,
    top=1in,
}

% --- Header ---
\title{Computer Vision: Homework 1}
\author{HuangYijun}

% --- Document Start ---
\begin{document}

\maketitle
\hrulefill
\vspace{1em}

\section{Written Assignment}

Let the camera's coordinate system be centered at the pinhole (the origin), with the z-axis being the optical axis pointing towards the image plane. The image plane is located at $z=f$, where $f$ is the effective focal length.

The perspective projection equations that map a 3D point $(X, Y, Z)$ to a 2D image point $(x, y)$ are:
\begin{equation}
x = f \frac{X}{Z} \quad \text{and} \quad y = f \frac{Y}{Z}
\label{eq:projection}
\end{equation}

A circular disk in 3D space can be described by its center $(X_c, Y_c, Z_c)$, its radius $R$, and the plane it lies on. Since the disk's plane is parallel to the image plane, all points $(X, Y, Z)$ on the circumference of the disk must have the same constant depth, $Z = Z_c$.

The equation for this circle in its 3D plane is:
\begin{equation}
(X - X_c)^2 + (Y - Y_c)^2 = R^2 \quad (\text{with } Z = Z_c)
\label{eq:3dcircle}
\end{equation}

To find the shape of the image, we can express the 3D coordinates $X$ and $Y$ in terms of the image coordinates $x$ and $y$ using the projection equations \eqref{eq:projection}. Since $Z = Z_c$ for all points on the circle:
\begin{equation}
X = x \frac{Z_c}{f} \quad \text{and} \quad Y = y \frac{Z_c}{f}
\label{eq:inverse_projection}
\end{equation}

Now, we substitute these expressions for $X$ and $Y$ into the 3D circle equation \eqref{eq:3dcircle}:
\begin{align*}
\left(x \frac{Z_c}{f} - X_c\right)^2 + \left(y \frac{Z_c}{f} - Y_c\right)^2 &= R^2 \\
\left(\frac{Z_c}{f}\right)^2 \left(x - \frac{f X_c}{Z_c}\right)^2 + \left(\frac{Z_c}{f}\right)^2 \left(y - \frac{f Y_c}{Z_c}\right)^2 &= R^2 \\
\end{align*}
Dividing both sides by $\left(\frac{Z_c}{f}\right)^2$:
\begin{equation}
\left(x - \frac{f X_c}{Z_c}\right)^2 + \left(y - \frac{f Y_c}{Z_c}\right)^2 = \frac{R^2}{\left(\frac{Z_c}{f}\right)^2} = \left(\frac{f R}{Z_c}\right)^2
\label{eq:image_circle}
\end{equation}

This is the standard equation of a circle in the 2D image plane, $(x-x_c')^2 + (y-y_c')^2 = (R')^2$, where:
\begin{itemize}
    \item The center of the image circle is $(x_c', y_c') = \left(f \frac{X_c}{Z_c}, f \frac{Y_c}{Z_c}\right)$, which is the perspective projection of the 3D circle's center.
    \item The radius of the image circle is $R' = \left| \frac{f R}{Z_c} \right|$. The radius is scaled by the factor $f/Z_c$.
\end{itemize}

\paragraph{Conclusion} The image of a circular disk lying in a plane parallel to the image plane is also a circular disk.

\hrulefill
\vspace{1em}

\subsection*{(b) The vanishing points of lines on a plane}


\paragraph{Case 1: Plane $B=1$, $A=C=D=0 \implies y=0$}
This is the horizontal plane passing through the optical center. Any line lying \textit{on} this plane must have a direction vector $\mathbf{d}$ that is also on this plane. This implies that the $Y$ component of the direction vector must be zero, i.e., $d_Y = 0$.

Let's choose three different line directions in this plane:
\begin{enumerate}
    \item \textbf{Direction $\mathbf{d_1} = (1, 0, 1)$}: A line moving away and to the positive X direction.
    \begin{equation*}
    (x_{vp1}, y_{vp1}) = \left(f \frac{1}{1}, f \frac{0}{1}\right) = (f, 0)
    \end{equation*}
    \item \textbf{Direction $\mathbf{d_2} = (-1, 0, 1)$}: A line moving away and to the negative X direction.
    \begin{equation*}
    (x_{vp2}, y_{vp2}) = \left(f \frac{-1}{1}, f \frac{0}{1}\right) = (-f, 0)
    \end{equation*}
    \item \textbf{Direction $\mathbf{d_3} = (\sqrt{3}, 0, 1)$}: A line moving away at 60 degrees from the Z-axis in the XZ plane.
    \begin{equation*}
    (x_{vp3}, y_{vp3}) = \left(f \frac{\sqrt{3}}{1}, f \frac{0}{1}\right) = (f\sqrt{3}, 0)
    \end{equation*}
\end{enumerate}
For any direction $\mathbf{d} = (d_X, 0, d_Z)$ on this plane, the vanishing point is $(f \frac{d_X}{d_Z}, 0)$. This means all vanishing points lie on the line $y=0$ in the image plane (the horizontal axis).

\paragraph{Case 2: Plane $A=1$, $B=C=D=0 \implies x=0$}
This is the vertical plane passing through the optical center. Any line on this plane must have a direction vector $\mathbf{d}$ with $d_X = 0$.

Let's choose three different line directions in this plane:
\begin{enumerate}
    \item \textbf{Direction $\mathbf{d_1} = (0, 1, 1)$}: A line moving away and up.
    \begin{equation*}
    (x_{vp1}, y_{vp1}) = \left(f \frac{0}{1}, f \frac{1}{1}\right) = (0, f)
    \end{equation*}
    \item \textbf{Direction $\mathbf{d_2} = (0, -1, 1)$}: A line moving away and down.
    \begin{equation*}
    (x_{vp2}, y_{vp2}) = \left(f \frac{0}{1}, f \frac{-1}{1}\right) = (0, -f)
    \end{equation*}
    \item \textbf{Direction $\mathbf{d_3} = (0, 0, 1)$}: A line moving straight away (this line lies on both planes $x=0$ and $y=0$).
    \begin{equation*}
    (x_{vp3}, y_{vp3}) = \left(f \frac{0}{1}, f \frac{0}{1}\right) = (0, 0)
    \end{equation*}
\end{enumerate}
For any direction $\mathbf{d} = (0, d_Y, d_Z)$ on this plane, the vanishing point is $(0, f \frac{d_Y}{d_Z})$. This means all vanishing points lie on the line $x=0$ in the image plane (the vertical axis).


\hrulefill
\vspace{1em}

\subsection*{(c) General relationship for any plane}

Let the 3D plane be $\Pi: Ax + By + Cz + D = 0$.
A line $\mathbf{L}(t) = \mathbf{P_0} + t\mathbf{d}$ lies on this plane if its starting point $\mathbf{P_0}=(X_0, Y_0, Z_0)$ is on the plane and its direction vector $\mathbf{d}=(d_X, d_Y, d_Z)$ is parallel to the plane.
The condition for $\mathbf{d}$ to be parallel to the plane is that it must be perpendicular to the plane's normal vector $\mathbf{n} = (A, B, C)$. This gives the constraint:
\begin{equation*}
\mathbf{n} \cdot \mathbf{d} = 0 \implies Ad_X + Bd_Y + Cd_Z = 0
\end{equation*}

The vanishing point for a line with direction $\mathbf{d}$ has image coordinates $(x_{vp}, y_{vp})$ where $x_{vp} = f \frac{d_X}{d_Z}$ and $y_{vp} = f \frac{d_Y}{d_Z}$. From these, we can write $d_X = \frac{x_{vp}}{f}d_Z$ and $d_Y = \frac{y_{vp}}{f}d_Z$.

Now, substitute these into the dot product constraint, assuming $d_Z \neq 0$ (i.e., the line is not parallel to the image plane):
\begin{align*}
A\left(\frac{x_{vp}}{f}d_Z\right) + B\left(\frac{y_{vp}}{f}d_Z\right) + Cd_Z &= 0 \\
\left(\frac{A}{f}x_{vp} + \frac{B}{f}y_{vp} + C\right)d_Z &= 0 \\
\frac{A}{f}x_{vp} + \frac{B}{f}y_{vp} + C &= 0
\end{align*}
Multiplying by $f$, we get the equation of a line in the image plane:
\begin{equation}
Ax_{vp} + By_{vp} + Cf = 0
\end{equation}

This is the equation of a line in the image plane. This line is called the \textbf{vanishing line} or the \textbf{horizon line} of the 3D plane $\Pi$.

\paragraph{Conclusion}
The vanishing points of ALL lines that lie on a 3D plane $Ax + By + Cz + D = 0$ themselves lie on a single line in the image plane. The equation of this vanishing line is given by $Ax + By + Cf = 0$. Note that the parameter $D$, which controls the plane's distance from the origin, does not affect the location of its vanishing line. This is expected, as parallel planes share the same vanishing line.
\section{Programming Assignment: SIFT Implementation}
This report describes the implementation of the Scale-Invariant Feature Transform (SIFT) algorithm, including Difference-of-Gaussian (DoG) keypoint detection, orientation assignment, and descriptor computation.
\subsection{Implementation Overview}
The SIFT algorithm was implemented in three main parts:
\begin{enumerate}
    \item \textbf{DoG Keypoint Detection}: Building Gaussian and DoG pyramids, followed by extrema detection and filtering
    \item \textbf{Orientation Assignment}: Computing dominant orientations for rotation invariance
    \item \textbf{Descriptor Computation}: Generating 128-dimensional feature descriptors
\end{enumerate}
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
\end{itemize}

\subsection{Experimental Results}
\subsubsection{Command Line Output}
\begin{lstlisting}[caption=Program execution output]
PS C:\Users\yeros\Desktop\CV\Homework-1> python h1_sift.py --image example.jpg
detected keypoints: 36
oriented keypoints: 43
descriptors: (43, 128)
Saved: sift_keypoints_vis.png
\end{lstlisting}
\subsubsection{Visual Results}
\begin{figure}[H]
    \centering
    \includegraphics[width=0.8\textwidth]{sift_keypoints_vis.png}
    \caption{SIFT keypoints visualization.}
    \label{fig:sift_keypoints}
\end{figure}


\section{Conclusion}
The SIFT implementation successfully demonstrates all three core components of the algorithm. The DoG keypoint detection identified stable feature points, the orientation assignment provided rotation invariance, and the descriptor computation generated distinctive 128-dimensional feature vectors. The experimental results show reasonable performance with appropriate keypoint density and successful multi-orientation detection, validating the correctness of the implementation.
\end{document}
\end{document}
帮我把这份latex格式报告缩减一半的内容且不要删除核心部分和结果展示

---

### DeepSeek AI

<p>思考：</p><blockquote><p class="ds-markdown-paragraph"><span>我们首先需要将报告缩减一半，但保留核心内容和结果展示。我们将删除一些冗余的细节，合并一些段落，并简化语言。</span><br><span>注意：我们不会删除任何核心步骤和结果，但会尽量精简描述。</span></p><p class="ds-markdown-paragraph"><span>步骤：</span></p><ol start="1"><li><p class="ds-markdown-paragraph"><span>精简“Written Assignment”部分，保留主要公式和结论。</span></p></li><li><p class="ds-markdown-paragraph"><span>精简“Programming Assignment”部分，保留每个步骤的核心思想，删除一些重复的细节。</span></p></li><li><p class="ds-markdown-paragraph"><span>确保结果展示（如图表和命令行输出）保留。</span></p></li></ol><p class="ds-markdown-paragraph"><span>由于我们无法实际运行代码，我们只根据提供的文本进行精简。</span></p><p class="ds-markdown-paragraph"><span>我们开始修改。</span></p></blockquote><br/><p class="ds-markdown-paragraph"><span>\documentclass[11pt, letterpaper]{article}</span><br><span>\usepackage[utf8]{inputenc}</span><br><span>\usepackage{amsmath}</span><br><span>\usepackage{graphicx}</span><br><span>\usepackage{float}</span><br><span>\usepackage{geometry}</span></p><p class="ds-markdown-paragraph"><span>\geometry{</span><br><span>letterpaper,</span><br><span>total={6.5in, 9in},</span><br><span>left=1in,</span><br><span>top=1in,</span><br><span>}</span></p><p class="ds-markdown-paragraph"><span>\title{Computer Vision: Homework 1}</span><br><span>\author{HuangYijun}</span></p><p class="ds-markdown-paragraph"><span>\begin{document}</span></p><p class="ds-markdown-paragraph"><span>\maketitle</span><br><span>\hrulefill</span></p><p class="ds-markdown-paragraph"><span>\section{Written Assignment}</span></p><p class="ds-markdown-paragraph"><span>\subsection*{(a) Circular Disk Projection}</span><br><span>Camera coordinate system: origin at pinhole, z-axis as optical axis. Image plane at $z=f$. Perspective projection:</span><br><span>\begin{equation}</span><br><span>x = f \frac{X}{Z}, \quad y = f \frac{Y}{Z}</span><br><span>\end{equation}</span></p><p class="ds-markdown-paragraph"><span>Circular disk in 3D: center $(X_c, Y_c, Z_c)$, radius $R$, parallel to image plane ($Z=Z_c$ constant). Circle equation:</span><br><span>\begin{equation}</span><br><span>(X - X_c)^2 + (Y - Y_c)^2 = R^2</span><br><span>\end{equation}</span></p><p class="ds-markdown-paragraph"><span>Using inverse projection $X = x Z_c/f$, $Y = y Z_c/f$:</span><br><span>\begin{equation}</span><br><span>\left(x - \frac{f X_c}{Z_c}\right)^2 + \left(y - \frac{f Y_c}{Z_c}\right)^2 = \left(\frac{f R}{Z_c}\right)^2</span><br><span>\end{equation}</span></p><p class="ds-markdown-paragraph"><span>\textbf{Conclusion:} Image is a circle centered at $(f X_c/Z_c, f Y_c/Z_c)$ with radius $|f R/Z_c|$.</span></p><p class="ds-markdown-paragraph"><span>\subsection*{(b) Vanishing Points on Planes}</span><br><span>\textbf{Case 1: Plane y=0} (horizontal through optical center)\</span><br><span>Direction vectors: $\mathbf{d}=(d_X,0,d_Z)$\</span><br><span>Vanishing points: $(f d_X/d_Z, 0)$ → all on horizontal axis</span></p><p class="ds-markdown-paragraph"><span>\textbf{Case 2: Plane x=0} (vertical through optical center)\</span><br><span>Direction vectors: $\mathbf{d}=(0,d_Y,d_Z)$\</span><br><span>Vanishing points: $(0, f d_Y/d_Z)$ → all on vertical axis</span></p><p class="ds-markdown-paragraph"><span>\subsection*{(c) General Vanishing Line}</span><br><span>Plane: $Ax + By + Cz + D = 0$, normal $\mathbf{n}=(A,B,C)$\</span><br><span>Direction vector $\mathbf{d}=(d_X,d_Y,d_Z)$ parallel to plane: $\mathbf{n}\cdot\mathbf{d}=0$</span></p><p class="ds-markdown-paragraph"><span>Using vanishing point coordinates $x_{vp}=f d_X/d_Z$, $y_{vp}=f d_Y/d_Z$:</span><br><span>\begin{equation}</span><br><span>A x_{vp} + B y_{vp} + C f = 0</span><br><span>\end{equation}</span></p><p class="ds-markdown-paragraph"><span>\textbf{Conclusion:} Vanishing points of all lines on a plane lie on this line. Parameter $D$ doesn't affect the vanishing line.</span></p><p class="ds-markdown-paragraph"><span>\section{Programming Assignment: SIFT Implementation}</span></p><p class="ds-markdown-paragraph"><span>\subsection{Implementation Overview}</span><br><span>Three main components:</span><br><span>\begin{enumerate}</span><br><span>\item DoG Keypoint Detection</span><br><span>\item Orientation Assignment</span><br><span>\item Descriptor Computation</span><br><span>\end{enumerate}</span></p><p class="ds-markdown-paragraph"><span>\subsection{Key Components}</span></p><p class="ds-markdown-paragraph"><span>\textbf{DoG Keypoint Detection:}</span><br><span>\begin{itemize}</span><br><span>\item Gaussian pyramid: $\sigma_{o,i} = \sigma \cdot 2^o \cdot k^i$ with $k=2^{1/s}$</span><br><span>\item DoG pyramid: difference of consecutive Gaussians</span><br><span>\item Extrema detection in $3\times3\times3$ neighborhood</span><br><span>\item Contrast filtering ($|D(x)| &lt; 0.03$)</span><br><span>\item Edge suppression using Hessian criterion</span><br><span>\end{itemize}</span></p><p class="ds-markdown-paragraph"><span>\textbf{Orientation Assignment:}</span><br><span>\begin{itemize}</span><br><span>\item Gradient computation in $3\sigma$ window</span><br><span>\item Gaussian weighting ($\sigma_{\text{ori}}=1.5\sigma$)</span><br><span>\item 36-bin histogram with smoothing and peak detection</span><br><span>\item Parabolic interpolation for peak refinement</span><br><span>\end{itemize}</span></p><p class="ds-markdown-paragraph"><span>\textbf{Descriptor Computation:}</span><br><span>\begin{itemize}</span><br><span>\item $16\times16$ sampling region scaled by $\sigma$</span><br><span>\item Gradient rotation by $-\theta$ for invariance</span><br><span>\item $4\times4$ grid with 8-bin orientation histograms</span><br><span>\item Trilinear interpolation and Gaussian weighting</span><br><span>\item L2 normalization with clamping at 0.2</span><br><span>\end{itemize}</span></p><p class="ds-markdown-paragraph"><span>\subsection{Results}</span><br><span>\begin{lstlisting}</span><br><span>detected keypoints: 36</span><br><span>oriented keypoints: 43</span><br><span>descriptors: (43, 128)</span><br><span>Saved: sift_keypoints_vis.png</span><br><span>\end{lstlisting}</span></p><p class="ds-markdown-paragraph"><span>\begin{figure}[H]</span><br><span>\centering</span><br><span>\includegraphics[width=0.6\textwidth]{sift_keypoints_vis.png}</span><br><span>\caption{SIFT keypoints visualization}</span><br><span>\end{figure}</span></p><p class="ds-markdown-paragraph"><span>\subsection{Conclusion}</span><br><span>Implementation successfully demonstrates all SIFT components: stable keypoint detection via DoG, rotation invariance through orientation assignment, and distinctive 128D descriptors. Results validate correctness with appropriate keypoint density.</span></p><p class="ds-markdown-paragraph"><span>\end{document}</span></p>

---

### 用户

\section{Written Assignment}

Let the camera's coordinate system be centered at the pinhole (the origin), with the z-axis being the optical axis pointing towards the image plane. The image plane is located at $z=f$, where $f$ is the effective focal length.

The perspective projection equations that map a 3D point $(X, Y, Z)$ to a 2D image point $(x, y)$ are:
\begin{equation}
x = f \frac{X}{Z} \quad \text{and} \quad y = f \frac{Y}{Z}
\label{eq:projection}
\end{equation}

A circular disk in 3D space can be described by its center $(X_c, Y_c, Z_c)$, its radius $R$, and the plane it lies on. Since the disk's plane is parallel to the image plane, all points $(X, Y, Z)$ on the circumference of the disk must have the same constant depth, $Z = Z_c$.

The equation for this circle in its 3D plane is:
\begin{equation}
(X - X_c)^2 + (Y - Y_c)^2 = R^2 \quad (\text{with } Z = Z_c)
\label{eq:3dcircle}
\end{equation}

To find the shape of the image, we can express the 3D coordinates $X$ and $Y$ in terms of the image coordinates $x$ and $y$ using the projection equations \eqref{eq:projection}. Since $Z = Z_c$ for all points on the circle:
\begin{equation}
X = x \frac{Z_c}{f} \quad \text{and} \quad Y = y \frac{Z_c}{f}
\label{eq:inverse_projection}
\end{equation}

Now, we substitute these expressions for $X$ and $Y$ into the 3D circle equation \eqref{eq:3dcircle}:
\begin{align*}
\left(x \frac{Z_c}{f} - X_c\right)^2 + \left(y \frac{Z_c}{f} - Y_c\right)^2 &= R^2 \\
\left(\frac{Z_c}{f}\right)^2 \left(x - \frac{f X_c}{Z_c}\right)^2 + \left(\frac{Z_c}{f}\right)^2 \left(y - \frac{f Y_c}{Z_c}\right)^2 &= R^2 \\
\end{align*}
Dividing both sides by $\left(\frac{Z_c}{f}\right)^2$:
\begin{equation}
\left(x - \frac{f X_c}{Z_c}\right)^2 + \left(y - \frac{f Y_c}{Z_c}\right)^2 = \frac{R^2}{\left(\frac{Z_c}{f}\right)^2} = \left(\frac{f R}{Z_c}\right)^2
\label{eq:image_circle}
\end{equation}

This is the standard equation of a circle in the 2D image plane, $(x-x_c')^2 + (y-y_c')^2 = (R')^2$, where:
\begin{itemize}
    \item The center of the image circle is $(x_c', y_c') = \left(f \frac{X_c}{Z_c}, f \frac{Y_c}{Z_c}\right)$, which is the perspective projection of the 3D circle's center.
    \item The radius of the image circle is $R' = \left| \frac{f R}{Z_c} \right|$. The radius is scaled by the factor $f/Z_c$.
\end{itemize}

\paragraph{Conclusion} The image of a circular disk lying in a plane parallel to the image plane is also a circular disk.

\hrulefill
\vspace{1em}

\subsection*{(b) The vanishing points of lines on a plane}


\paragraph{Case 1: Plane $B=1$, $A=C=D=0 \implies y=0$}
This is the horizontal plane passing through the optical center. Any line lying \textit{on} this plane must have a direction vector $\mathbf{d}$ that is also on this plane. This implies that the $Y$ component of the direction vector must be zero, i.e., $d_Y = 0$.

Let's choose three different line directions in this plane:
\begin{enumerate}
    \item \textbf{Direction $\mathbf{d_1} = (1, 0, 1)$}: A line moving away and to the positive X direction.
    \begin{equation*}
    (x_{vp1}, y_{vp1}) = \left(f \frac{1}{1}, f \frac{0}{1}\right) = (f, 0)
    \end{equation*}
    \item \textbf{Direction $\mathbf{d_2} = (-1, 0, 1)$}: A line moving away and to the negative X direction.
    \begin{equation*}
    (x_{vp2}, y_{vp2}) = \left(f \frac{-1}{1}, f \frac{0}{1}\right) = (-f, 0)
    \end{equation*}
    \item \textbf{Direction $\mathbf{d_3} = (\sqrt{3}, 0, 1)$}: A line moving away at 60 degrees from the Z-axis in the XZ plane.
    \begin{equation*}
    (x_{vp3}, y_{vp3}) = \left(f \frac{\sqrt{3}}{1}, f \frac{0}{1}\right) = (f\sqrt{3}, 0)
    \end{equation*}
\end{enumerate}
For any direction $\mathbf{d} = (d_X, 0, d_Z)$ on this plane, the vanishing point is $(f \frac{d_X}{d_Z}, 0)$. This means all vanishing points lie on the line $y=0$ in the image plane (the horizontal axis).

\paragraph{Case 2: Plane $A=1$, $B=C=D=0 \implies x=0$}
This is the vertical plane passing through the optical center. Any line on this plane must have a direction vector $\mathbf{d}$ with $d_X = 0$.

Let's choose three different line directions in this plane:
\begin{enumerate}
    \item \textbf{Direction $\mathbf{d_1} = (0, 1, 1)$}: A line moving away and up.
    \begin{equation*}
    (x_{vp1}, y_{vp1}) = \left(f \frac{0}{1}, f \frac{1}{1}\right) = (0, f)
    \end{equation*}
    \item \textbf{Direction $\mathbf{d_2} = (0, -1, 1)$}: A line moving away and down.
    \begin{equation*}
    (x_{vp2}, y_{vp2}) = \left(f \frac{0}{1}, f \frac{-1}{1}\right) = (0, -f)
    \end{equation*}
    \item \textbf{Direction $\mathbf{d_3} = (0, 0, 1)$}: A line moving straight away (this line lies on both planes $x=0$ and $y=0$).
    \begin{equation*}
    (x_{vp3}, y_{vp3}) = \left(f \frac{0}{1}, f \frac{0}{1}\right) = (0, 0)
    \end{equation*}
\end{enumerate}
For any direction $\mathbf{d} = (0, d_Y, d_Z)$ on this plane, the vanishing point is $(0, f \frac{d_Y}{d_Z})$. This means all vanishing points lie on the line $x=0$ in the image plane (the vertical axis).


\hrulefill
\vspace{1em}

\subsection*{(c) General relationship for any plane}

Let the 3D plane be $\Pi: Ax + By + Cz + D = 0$.
A line $\mathbf{L}(t) = \mathbf{P_0} + t\mathbf{d}$ lies on this plane if its starting point $\mathbf{P_0}=(X_0, Y_0, Z_0)$ is on the plane and its direction vector $\mathbf{d}=(d_X, d_Y, d_Z)$ is parallel to the plane.
The condition for $\mathbf{d}$ to be parallel to the plane is that it must be perpendicular to the plane's normal vector $\mathbf{n} = (A, B, C)$. This gives the constraint:
\begin{equation*}
\mathbf{n} \cdot \mathbf{d} = 0 \implies Ad_X + Bd_Y + Cd_Z = 0
\end{equation*}

The vanishing point for a line with direction $\mathbf{d}$ has image coordinates $(x_{vp}, y_{vp})$ where $x_{vp} = f \frac{d_X}{d_Z}$ and $y_{vp} = f \frac{d_Y}{d_Z}$. From these, we can write $d_X = \frac{x_{vp}}{f}d_Z$ and $d_Y = \frac{y_{vp}}{f}d_Z$.

Now, substitute these into the dot product constraint, assuming $d_Z \neq 0$ (i.e., the line is not parallel to the image plane):
\begin{align*}
A\left(\frac{x_{vp}}{f}d_Z\right) + B\left(\frac{y_{vp}}{f}d_Z\right) + Cd_Z &= 0 \\
\left(\frac{A}{f}x_{vp} + \frac{B}{f}y_{vp} + C\right)d_Z &= 0 \\
\frac{A}{f}x_{vp} + \frac{B}{f}y_{vp} + C &= 0
\end{align*}
Multiplying by $f$, we get the equation of a line in the image plane:
\begin{equation}
Ax_{vp} + By_{vp} + Cf = 0
\end{equation}

This is the equation of a line in the image plane. This line is called the \textbf{vanishing line} or the \textbf{horizon line} of the 3D plane $\Pi$.

\paragraph{Conclusion}
The vanishing points of ALL lines that lie on a 3D plane $Ax + By + Cz + D = 0$ themselves lie on a single line in the image plane. The equation of this vanishing line is given by $Ax + By + Cf = 0$. Note that the parameter $D$, which controls the plane's distance from the origin, does not affect the location of its vanishing line. This is expected, as parallel planes share the same vanishing line.把这份书面作业进行简化，但是保留核心的数学公式，减少语言描述的推导

---

### DeepSeek AI

<p>思考：</p><blockquote><p class="ds-markdown-paragraph"><span>我们只需要保留核心的数学推导和结论，去掉一些冗长的文字描述，但确保每一步的关键步骤和公式都保留。</span><br><span>对于(a)部分，我们保留投影方程、圆的方程、代入过程以及得到的图像圆方程。</span><br><span>对于(b)部分，我们保留两个特殊平面的例子，但可以简化文字描述，只给出关键的方向向量和 vanishing point 的计算。</span><br><span>对于(c)部分，保留一般平面的推导，从平面方程和方向向量的约束开始，到 vanishing line 的方程。</span></p><p class="ds-markdown-paragraph"><span>注意：我们不需要删除任何数学公式，但可以删除一些解释性的文字，同时保持逻辑连贯。</span></p></blockquote><br/><p class="ds-markdown-paragraph"><span>\section{Written Assignment}</span></p><p class="ds-markdown-paragraph"><span>\subsection*{(a) Circular Disk Projection}</span></p><p class="ds-markdown-paragraph"><span>Camera coordinate system: origin at pinhole, z-axis as optical axis. Image plane at $z=f$. Perspective projection:</span><br><span>\begin{equation}</span><br><span>x = f \frac{X}{Z}, \quad y = f \frac{Y}{Z}</span><br><span>\end{equation}</span></p><p class="ds-markdown-paragraph"><span>Circular disk in 3D: center $(X_c, Y_c, Z_c)$, radius $R$, plane parallel to image plane ($Z=Z_c$ constant):</span><br><span>\begin{equation}</span><br><span>(X - X_c)^2 + (Y - Y_c)^2 = R^2</span><br><span>\end{equation}</span></p><p class="ds-markdown-paragraph"><span>Using inverse projection $X = x Z_c/f$, $Y = y Z_c/f$:</span><br><span>\begin{align</span>*<span>}</span><br><span>\left(x \frac{Z_c}{f} - X_c\right)^2 + \left(y \frac{Z_c}{f} - Y_c\right)^2 &amp;= R^2 \</span><br><span>\left(\frac{Z_c}{f}\right)^2 \left(x - \frac{f X_c}{Z_c}\right)^2 + \left(\frac{Z_c}{f}\right)^2 \left(y - \frac{f Y_c}{Z_c}\right)^2 &amp;= R^2</span><br><span>\end{align</span>*<span>}</span></p><p class="ds-markdown-paragraph"><span>Dividing by $\left(\frac{Z_c}{f}\right)^2$:</span><br><span>\begin{equation}</span><br><span>\left(x - \frac{f X_c}{Z_c}\right)^2 + \left(y - \frac{f Y_c}{Z_c}\right)^2 = \left(\frac{f R}{Z_c}\right)^2</span><br><span>\end{equation}</span></p><p class="ds-markdown-paragraph"><span>\textbf{Conclusion:} Image is a circle centered at $(f X_c/Z_c, f Y_c/Z_c)$ with radius $|f R/Z_c|$.</span></p><p class="ds-markdown-paragraph"><span>\subsection*{(b) Vanishing Points on Planes}</span></p><p class="ds-markdown-paragraph"><span>\textbf{Case 1: Plane y=0} (horizontal through optical center)\</span><br><span>Direction vectors: $\mathbf{d}=(d_X,0,d_Z)$\</span><br><span>Vanishing points: $(f d_X/d_Z, 0)$ → all on horizontal axis</span></p><p class="ds-markdown-paragraph"><span>\textbf{Case 2: Plane x=0} (vertical through optical center)\</span><br><span>Direction vectors: $\mathbf{d}=(0,d_Y,d_Z)$\</span><br><span>Vanishing points: $(0, f d_Y/d_Z)$ → all on vertical axis</span></p><p class="ds-markdown-paragraph"><span>\subsection*{(c) General Vanishing Line}</span></p><p class="ds-markdown-paragraph"><span>Plane: $Ax + By + Cz + D = 0$, normal $\mathbf{n}=(A,B,C)$\</span><br><span>Direction vector constraint: $\mathbf{n}\cdot\mathbf{d}=0 \implies Ad_X + Bd_Y + Cd_Z = 0$</span></p><p class="ds-markdown-paragraph"><span>Vanishing point coordinates: $x_{vp}=f d_X/d_Z$, $y_{vp}=f d_Y/d_Z$\</span><br><span>Substitute $d_X = x_{vp}d_Z/f$, $d_Y = y_{vp}d_Z/f$:</span><br><span>\begin{align</span>*<span>}</span><br><span>A\left(\frac{x_{vp}}{f}d_Z\right) + B\left(\frac{y_{vp}}{f}d_Z\right) + Cd_Z &amp;= 0 \</span><br><span>\frac{A}{f}x_{vp} + \frac{B}{f}y_{vp} + C &amp;= 0</span><br><span>\end{align</span>*<span>}</span></p><p class="ds-markdown-paragraph"><span>Multiplying by $f$:</span><br><span>\begin{equation}</span><br><span>Ax_{vp} + By_{vp} + Cf = 0</span><br><span>\end{equation}</span></p><p class="ds-markdown-paragraph"><span>\textbf{Conclusion:} Vanishing points of all lines on plane $Ax + By + Cz + D = 0$ lie on line $Ax + By + Cf = 0$. Parameter $D$ doesn't affect vanishing line (parallel planes share vanishing line).</span></p>

---

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
\end{itemize}简化对算法的描述，合并小标题但不要删除关键内容和公式

---

### DeepSeek AI

<p>思考：</p><blockquote><p class="ds-markdown-paragraph"><span>我们首先将三个部分（A、B、C）合并为一个部分，并简化描述，但保留关键步骤和公式。</span><br><span>注意：我们不需要删除公式，但可以简化文字描述，同时保持内容的连贯性。</span><br><span>我们将使用更紧凑的列表和更简洁的语言。</span></p></blockquote><br/><p class="ds-markdown-paragraph"><span>\section{SIFT Implementation}</span></p><p class="ds-markdown-paragraph"><span>\subsection{Algorithm Overview}</span><br><span>The SIFT implementation consists of three core components:</span></p><p class="ds-markdown-paragraph"><span>\subsection{Keypoint Detection and Description}</span></p><p class="ds-markdown-paragraph"><span>\textbf{DoG Keypoint Detection:}</span><br><span>\begin{itemize}</span><br><span>\item Gaussian pyramid: $\sigma_{o,i} = \sigma \cdot 2^o \cdot k^i$ where $k = 2^{1/s}$</span><br><span>\item DoG computation: $D(x,y,\sigma) = G(x,y,k\sigma) - G(x,y,\sigma)$</span><br><span>\item Extrema detection in $3 \times 3 \times 3$ scale-space neighborhood</span><br><span>\item Contrast filtering: $|D(x)| &lt; 0.03$</span><br><span>\item Edge suppression: $\frac{(\text{Tr}(H))^2}{\det(H)} &lt; \frac{(r+1)^2}{r}$ with $r=10$</span><br><span>\end{itemize}</span></p><p class="ds-markdown-paragraph"><span>\textbf{Orientation Assignment:}</span><br><span>\begin{itemize}</span><br><span>\item Gradient computation in $3\sigma$ window using Sobel operators</span><br><span>\item Gaussian weighting with $\sigma_{\text{ori}} = 1.5\sigma$</span><br><span>\item 36-bin orientation histogram with smoothing</span><br><span>\item Peak detection with 80% threshold</span><br><span>\item Parabolic interpolation: $\text{offset} = \frac{0.5(h_{\text{left}} - h_{\text{right}})}{h_{\text{left}} - 2h_{\text{center}} + h_{\text{right}}}$</span><br><span>\end{itemize}</span></p><p class="ds-markdown-paragraph"><span>\textbf{Descriptor Computation:}</span><br><span>\begin{itemize}</span><br><span>\item $16 \times 16$ sampling region scaled by $\sigma$</span><br><span>\item Gradient rotation by $-\theta$ for invariance</span><br><span>\item $4 \times 4$ spatial grid with 8 orientation bins</span><br><span>\item Trilinear interpolation for spatial and orientation dimensions</span><br><span>\item Gaussian weighting with $\sigma = 0.5 \times \text{window_size}$</span><br><span>\item Normalization: L2 → clamp (0.2) → L2 renormalization</span><br><span>\end{itemize}</span></p>

