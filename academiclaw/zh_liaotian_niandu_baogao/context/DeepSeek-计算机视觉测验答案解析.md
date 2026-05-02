### 用户

本-(2025-2026-1)-AI3619-01-计算机视觉
Quiz-8
Quiz-8
已开始： 11月24日 11:32
测验说明
注意：这是计时测验。您可以在参加测验时随时查看您的剩余时间，方法是按组合键 SHIFT、ALT 和 T... 重申一遍：SHIFT、ALT 和 T...
 
标记问题：问题 1
问题 11 分
When epipolar lines are perfectly horizontal, corresponding points between left and right images will:

答案选项组

Change only in the x-direction

Move in arbitrary directions

Change only in the y-direction

Completely overlap
 
标记问题：问题 2
问题 21 分
Decomposing the Essential Matrix allows recovery of:

答案选项组

Rotation R and translation direction t between cameras

Camera intrinsic parameters

The absolute scale of the scene

Depth values of all points
 
标记问题：问题 3
问题 31 分
The input to Structure-from-Motion (SfM) is:

 

答案选项组

Multiple images with point correspondences

A single image

Multiple images with camera intrinsics

A known 3D mesh
 
标记问题：问题 4
问题 41 分
The step in SfM that jointly optimizes all camera poses and 3D points is called:

答案选项组

Bundle Adjustment

RANSAC

EPnP

Rectification
 
标记问题：问题 5
问题 51 分
Reprojection error in SfM measures:

答案选项组

Distance between projected 3D point and its observed 2D location

3D Euclidean distance between true and reconstructed points

Image gradient difference

Difference between two fundamental matrices
未保存 
问题
尚未回答问题 1
尚未回答问题 2
尚未回答问题 3
尚未回答问题 4
尚未回答问题 5
运行时间：
尝试截止： 11月24日 23:59
59 分钟, 53 秒

---

### DeepSeek AI

<p>思考：</p><blockquote><p class="ds-markdown-paragraph"><span>我们逐个问题分析并给出答案。</span></p><p class="ds-markdown-paragraph"><span>问题1：当极线完美水平时，左右图像中的对应点会怎样？</span><br><span>解析：在立体视觉中，当两个相机的光轴平行且图像平面共面时，极线是水平的。这意味着对于左图像中的一个点，在右图像中对应的点位于相同的水平线（即相同的y坐标）上。因此，对应点只在x方向上变化（即视差）。</span><br><span>答案：Change only in the x-direction</span></p><p class="ds-markdown-paragraph"><span>问题2：分解本质矩阵可以恢复什么？</span><br><span>解析：本质矩阵E由相机的外参（旋转和平移）组成，满足 E = [t]_x R。通过分解本质矩阵，我们可以得到相机之间的旋转R和平移t的方向（注意，平移t的尺度无法确定，只能得到方向）。</span><br><span>答案：Rotation R and translation direction t between cameras</span></p><p class="ds-markdown-paragraph"><span>问题3：运动恢复结构（SfM）的输入是什么？</span><br><span>解析：SfM是从一系列图像中恢复3D结构和相机姿态的技术。其输入通常是多个图像（通常有重叠）以及这些图像之间的点对应关系（特征匹配）。有时也会已知相机内参，但并非必须（可以通过自标定得到）。但最基础的输入是多个图像和点对应。</span><br><span>答案：Multiple images with point correspondences</span></p><p class="ds-markdown-paragraph"><span>问题4：在SfM中，联合优化所有相机姿态和3D点的步骤叫什么？</span><br><span>解析：Bundle Adjustment（光束法平差）是SfM中的一个关键步骤，它通过最小化重投影误差来同时优化相机参数（姿态和内参）和3D点坐标。</span><br><span>答案：Bundle Adjustment</span></p><p class="ds-markdown-paragraph"><span>问题5：SfM中的重投影误差测量什么？</span><br><span>解析：重投影误差是指将3D点投影到图像平面上的位置与实际上观测到的2D点位置之间的差距（通常是欧氏距离）。</span><br><span>答案：Distance between projected 3D point and its observed 2D location</span></p><p class="ds-markdown-paragraph"><span>因此，答案如下：</span></p><ol start="1"><li><p class="ds-markdown-paragraph"><span>Change only in the x-direction</span></p></li><li><p class="ds-markdown-paragraph"><span>Rotation R and translation direction t between cameras</span></p></li><li><p class="ds-markdown-paragraph"><span>Multiple images with point correspondences</span></p></li><li><p class="ds-markdown-paragraph"><span>Bundle Adjustment</span></p></li><li><p class="ds-markdown-paragraph"><span>Distance between projected 3D point and its observed 2D location</span></p></li></ol></blockquote><br/><p class="ds-markdown-paragraph"><strong><span>答案：</span></strong></p><p class="ds-markdown-paragraph"><strong><span>问题 1</span></strong><br><span>正确答案：</span><strong><span>Change only in the x-direction</span></strong><br><span>解析：当极线水平时，对应点在左右图像中具有相同的纵坐标（y 坐标），仅横坐标（x 方向）存在差异，即视差。</span></p><p class="ds-markdown-paragraph"><strong><span>问题 2</span></strong><br><span>正确答案：</span><strong><span>Rotation R and translation direction t between cameras</span></strong><br><span>解析：本质矩阵 E 包含相机间的旋转和平移信息，分解 E 可以恢复旋转矩阵 R 和平移向量 t 的方向，但平移的尺度无法确定。</span></p><p class="ds-markdown-paragraph"><strong><span>问题 3</span></strong><br><span>正确答案：</span><strong><span>Multiple images with point correspondences</span></strong><br><span>解析：运动恢复结构（SfM）通过多张图像中匹配的点对应关系，估计相机姿态和场景的三维结构。</span></p><p class="ds-markdown-paragraph"><strong><span>问题 4</span></strong><br><span>正确答案：</span><strong><span>Bundle Adjustment</span></strong><br><span>解析：光束法平差（Bundle Adjustment）通过最小化重投影误差，联合优化所有相机参数和三维点坐标。</span></p><p class="ds-markdown-paragraph"><strong><span>问题 5</span></strong><br><span>正确答案：</span><strong><span>Distance between projected 3D point and its observed 2D location</span></strong><br><span>解析：重投影误差是三维点投影到图像平面后的位置与其实际观测到的二维位置之间的欧氏距离。</span></p><p class="ds-markdown-paragraph"><strong><span>总结：</span></strong></p><ol start="1"><li><p class="ds-markdown-paragraph"><span>Change only in the x-direction</span></p></li><li><p class="ds-markdown-paragraph"><span>Rotation R and translation direction t between cameras</span></p></li><li><p class="ds-markdown-paragraph"><span>Multiple images with point correspondences</span></p></li><li><p class="ds-markdown-paragraph"><span>Bundle Adjustment</span></p></li><li><p class="ds-markdown-paragraph"><span>Distance between projected 3D point and its observed 2D location</span></p></li></ol>

