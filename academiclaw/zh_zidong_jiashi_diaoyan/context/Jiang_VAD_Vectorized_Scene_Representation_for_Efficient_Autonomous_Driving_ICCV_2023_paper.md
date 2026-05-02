# VAD: Vectorized Scene Representation for Efficient Autonomous Driving

Bo Jiang\(^1\),*\(\diamondsuit\), Shaoyu Chen\(^1\),*\(\diamondsuit\), Qing Xu\(^2\), Bencheng Liao\(^1\),\(\diamondsuit\), Jiajie Chen\(^2\),  
Helong Zhou\(^2\), Qian Zhang\(^2\), Wenyu Liu\(^1\), Chang Huang\(^2\), Xinggang Wang\(^1\),\(\boxtimes\)

\(^1\) Huazhong University of Science & Technology \(^2\) Horizon Robotics  
(bjiang, shaoyuchen, bcliao, liuwy, xgwang)@hust.edu.cn  
(qing.xu, jiajie.chen, helong.zhou, qian01.zhang, chang.huang)@horizon.ai  

## Abstract

Autonomous driving requires a comprehensive understanding of the surrounding environment for reliable trajectory planning. Previous works rely on dense rasterized scene representation (e.g., agent occupancy and semantic map) to perform planning, which is computationally intensive and misses the instance-level structure information. In this paper, we propose VAD, an end-to-end vectorized paradigm for autonomous driving, which models the driving scene as a fully vectorized representation. The proposed vectorized paradigm has two significant advantages. On one hand, VAD exploits the vectorized agent motion and map elements as explicit instance-level planning constraints which effectively improves planning safety. On the other hand, VAD runs much faster than previous end-to-end planning methods by getting rid of computation-intensive rasterized representation and hand-designed post-processing steps. VAD achieves state-of-the-art end-to-end planning performance on the nuScenes dataset, outperforming the previous best method by a large margin. Our base model, VAD-Base, greatly reduces the average collision rate by 29.0% and runs 2.5\(\times\) faster. Besides, a lightweight variant, VAD-Tiny, greatly improves the inference speed (up to 9.3\(\times\)) while achieving comparable planning performance. We believe the excellent performance and the high efficiency of VAD are critical for the real-world deployment of an autonomous driving system. Code and models are available at https://github.com/hustvl/VAD for facilitating future research.

## 1. Introduction

Autonomous driving requires both comprehensive scene understanding for ensuring safety and high efficiency for real-world deployment. An autonomous vehicle needs to efficiently perceive the driving scene and perform reasonable planning based on the scene information. Traditional autonomous driving methods [23, 14, 7, 48] adopt a modular paradigm, where perception and planning are decoupled into standalone modules. The disadvantage is, the planning module cannot access the original sensor data, which contains rich semantic information. And since planning is fully based on preceding perception results, the error in perception may severely influence planning and can not be recognized and cured in the planning stage, which leads to the safety problem. Recently, end-to-end autonomous driving methods [19, 21, 2, 11] take sensor data as input for perception and output planning results with one holistic model. Some works [40, 9, 41] directly output planning results based on the sensor data without learning scene representation, which lacks interpretability and is difficult to optimize. Most works [19, 21, 2] transform the sensor data into rasterized scene representation (_e.g._, semantic map, occupancy map, flow map, and cost map) for planning. Though straightforward, rasterized representation is computationally intensive and misses critical instance-level structure information.

In this work, we propose VAD (**V**ectorized **A**utonomous **D**riving), an end-to-end vectorized paradigm for autonomous driving. VAD models the scene in a fully vectorized way (_i.e._, vectorized agent motion and map), getting rid of computationally intensive rasterized representation.

We argue that vectorized scene representation is superior to rasterized one. Vectorized map (represented as boundary vectors and lane vectors) provides road structure information (_e.g._, traffic flow, drivable boundary, and lane direction), and helps the autonomous vehicle narrow down the trajectory search space and plan a reasonable future trajectory. The motion of traffic participants (represented as agent motion vectors) provides instance-level restriction for collision avoidance. What's more, vectorized scene representation is efficient in terms of computation, which is important for real-world applications.

VAD takes full advantage of the vectorized information to guide planning both implicitly and explicitly. On one hand, VAD adopts map queries and agent queries to implicitly learn instance-level map features and agent motion features from sensor data, and extracts guidance information for planning via query interaction. On the other hand, VAD proposes three instance-level planning constraints based on the explicit vectorized scene representation: the ego-agent collision constraint for maintaining a safe distance between the ego vehicle and other dynamic agents both laterally and longitudinally; the ego-boundary overstepping constraint for pushing the planning trajectory away from the road boundary; and the ego-lane direction constraint for regularizing the future motion direction of the autonomous vehicle with vectorized lane direction. Our proposed framework and the vectorized planning constraints effectively improve the planning performance, without incurring large computational overhead.

Without fancy tricks or hand-designed post-processing steps, VAD achieves state-of-the-art (SOTA) end-to-end planning performance and the best efficiency on the challenging nuScenes [1] dataset. Compared with the previous SOTA method UniAD [21], our base model, VAD-Base, greatly reduces the average planning displacement error by 30.1% (1.03m _v.s._ 0.72m) and the average collision rate by 29.0% (0.31% _v.s._ 0.22%), while running 2.5\(\times\) faster (1.8 FPS _v.s._ 4.5 FPS). The lightweight variant, VAD-Tiny, runs 9.3\(\times\) faster (1.8 FPS _v.s._ 16.8 FPS) while achieving comparable planning performance, the average planning displacement error is 0.78m and the average collision rate is 0.38%. We also demonstrate the effectiveness of our design choices through thorough ablations.

Our key contributions are summarized as follows:

* We propose VAD, an end-to-end vectorized paradigm for autonomous driving. VAD models the driving scene as a fully vectorized representation, getting rid of computationally intensive dense rasterized representation and hand-designed post-processing steps.
* VAD implicitly and explicitly utilizes the vectorized scene information to improve planning safety, via query interaction and vectorized planning constraints.
* VAD achieves SOTA end-to-end planning performance, outperforming previous methods by a large margin. Not only that, because of the vectorized scene representation and our concise model design, VAD greatly improves the inference speed, which is critical for the real-world deployment of an autonomous driving system.

It's our belief that autonomous driving can be performed in a fully vectorized manner with high efficiency. We hope the impressive performance of VAD can reveal the potential of vectorized paradigm to the community.

## 2. Related Work

**Perception.** Accurate perception of the driving scene is the basis for autonomous driving. We mainly introduce some camera-based 3D object detection and online mapping methods which are most relevant to this paper. DETR3D [47] uses 3D queries to sample corresponding image features and accomplish detection without non-maximum suppression. PETR [31] introduces 3D positional encoding to image features and uses detection queries to learn object features via attention [46] mechanism. Recently, bird's-eye view (BEV) representation has become popular and has greatly contributed to the field of perception [26, 51, 17, 29, 8, 34, 28]. LSS [39] is a pioneering work that introduces depth prediction to project features from perspective view to BEV. BEVFormer [26] proposes spatial and temporal attention for better encoding the BEV feature map and achieves remarkable detection performance with camera input only. FIERY [17] and BEVerse [51] use the BEV feature map to predict dense map segmentation. HDMapNet [25] converts lane segmentation to vectorized map with post-processing steps. VectorMapNet [32] predicts map elements in an autoregressive way. MapTR [29] recognizes the permutation invariance of the map instance points and can predict all map elements simultaneously. LaneGAP [28] models the lane graph in a novel path-wise manner, which well preserves the continuity of the lane and encodes traffic information for planning. We leverage a group of BEV queries, agent queries, and map queries to accomplish scene perception following BEVFormer [26] and MapTR [29], and further use these query features and perception results in the motion prediction and planning stage. Details are shown in Sec. 3.

**Motion Prediction.** Traditional motion prediction takes perception ground truth (, agent history trajectories and HD map) as input. Some works [38, 3] render the driving scene as BEV images and adopt CNN-based networks to predict future motion. Some other works [37, 13, 33] use vectorized representation, and adopt GNN [27] or Transformer [46, 37, 33] to accomplish learning and prediction. Recent end-to-end works [51, 17, 15, 22] jointly perform perception and motion prediction. Some works [51, 17, 20] see future motion as dense occupancy and flow instead of agent-level future waypoints. ViP3D [15] predicts future motion based on the tracking results and HD map. PIP [22] proposes an interaction scheme between dynamic agents and static vectorized map, and achieves SOTA performance without relying on HD map. VAD learns vectorized agent motion by interacting between dynamic agents and static map elements, inspired by [22].

**Planning.** Recently, learning-based planning methods prevail. Some works [40, 9, 41] omit intermediate stages such as perception and motion prediction, and directly predict planning trajectories or control signals. Although this idea is straightforward and simple, they lack interpretability and are difficult to optimize. Reinforcement learning is quite up to the planning task and has become a promising research direction [45, 5, 4]. Explicit dense cost map has great interpretability and is widely used [2, 19, 11, 44]. The cost maps are constructed from the perception or motion prediction results, or come from a learning-based module. And hand-crafted rules are often adopted to select the best planning trajectory with minimum cost. The construction of a dense cost map is computationally intensive and the using of hand-crafted rules brings robustness and generalization problems. UniAD [21] effectively incorporates the information provided by various preceding tasks to assist planning in a goal-oriented spirit, and achieves remarkable performance in perception, prediction, and planning. PlanT [43] takes perception ground truth as input and encodes the scene in object-level representation for planning. In this paper, we explore the potential of vectorized scene representation for planning and get rid of dense maps or hand-designed post-processing steps.

## 3. Method

**Overview.** The overall framework of VAD is depicted in Fig. 2. Given multi-frame and multi-view image input, VAD first encodes the image features with a backbone network and utilizes a group of BEV queries to project the image features to the BEV features [26, 52, 39]. Second, VAD utilizes a group of agent queries and map queries to learn the vectorized scene representation, including vectorized map and vectorized agent motion (Sec. 3.1). Third, planning is performed based on the scene information (Sec. 3.2). Specifically, VAD uses an ego query to learn the implicit scene information through interaction with agent queries and map queries. Based on the ego query, ego status features, and high-level driving command, the Planning Head outputs the planning trajectory. Besides, VAD introduces three vectorized planning constraints to restrict the planning trajectory at the instance level (Sec. 3.3). VAD is fully differentiable and trained in an end-to-end manner (Sec. 3.4).

### 3.1 Vectorized Scene Learning

Perceiving traffic agents and map elements are important in driving scene understanding. VAD encodes the scene information into query features and represents the scene by map vectors and agent motion vectors.

**Vectorized Map.** Previous works [19, 21] use rasterized semantic maps to guide the planning, which misses critical instance-level structure information of the map. VAD utilizes a group of map queries [29] \(Q_{m}\) to extract map information from BEV feature map and predicts map vectors \(\hat{V}_{m}\in\mathbb{R}^{N_{m}\times N_{p}\times 2}\) and the class score for each map vector, where \(N_{m}\) and \(N_{p}\) denote the number of predicted map vectors and the points contained in each map vector. Three kinds of map elements are considered: lane divider, road boundary, and pedestrian crossing. The Lane divider provides direction information, and the road boundary indicates the drivable area. Map queries and map vectors are both leveraged to improve the planning performance (Sec. 3.2 and Sec. 3.3).

**Vectorized Agent Motion.** VAD first adopts a group of agent queries \(Q_{a}\) to learn agent-level features from the shared BEV feature map via deformable attention [53]. The agent's attributes (location, class score, orientation, _etc._) are decoded from the agent queries by an MLP-based decoder head. To enrich the agent features for motion prediction, VAD performs agent-agent and agent-map interaction [22, 37] via attention mechanism. Then VAD predicts future trajectories of each agent, represented as multi-modality motion vectors \(\hat{V}_{a}\in\mathbb{R}^{N_{a}\times N_{k}\times T_{f}\times 2}\). \(N_{a},N_{k}\), and \(T_{f}\) denote the number of predicted agents, the number of modalities, and the number of future timestamps. Each modality of the motion vector indicates a kind of driving intention. VAD outputs a probability score for each modality. The agent motion vectors are used to restrict the ego planning trajectory and avoid collision (Sec. 3.3). Meanwhile, the agent queries are sent into the planning module as scene information (Sec. 3.2).

### 3.2 Planning via Interaction

**Ego-Agent Interaction.** VAD utilizes a randomly initialized ego query \(Q_{\text{ego}}\) to learn the implicit scene features which are valuable for planning. In order to learn the location and motion information of other dynamic traffic participants, the ego query first interacts with the agent queries through a Transformer decoder [46], in which ego query serves as query of attention \(q\), and agent queries serve as key \(k\) and value \(v\). The ego position \(p_{\text{ego}}\) and agent positions \(p_{a}\) predicted by the perception module are encoded by a single layer MLP \(\text{PE}_{1}\), and serve as query position embedding \(q_{\text{pos}}\) and key position embedding \(k_{\text{pos}}\). The positional embeddings provide information on the relative position relationship between agents and the ego vehicle. The above process can be formulated as:

\[
\begin{split}
& Q^{\prime}_{\text{ego}}=\text{TransformerDecoder}(q,\; k,\; v,\; q_{\text{pos}},\; k_{\text{pos}}),\\
& q=Q_{\text{ego}},\; k=v=Q_{a},\\
& q_{\text{pos}}=\text{PE}_{1}(p_{\text{ego}}),\; k_{\text{pos}}=\text{PE}_{1}(p_{a}).
\end{split}
\]

**Ego-Map Interaction.** After interacting with agent queries, the updated ego query \(Q^{\prime}_{\text{ego}}\) further interacts with the map queries \(Q_{m}\) in a similar way. The only difference is we use a different MLP PE\({}_{2}\) to encode the positions of the ego vehicle and the map elements. The output ego query \(Q^{\prime}_{\text{ego}}\) contains both dynamic and static information of the driving scene. The process is formulated as:

\[
\begin{split}
& Q^{\prime\prime}_{\text{ego}}=\text{TransformerDecoder}(q,\; k,\; v,\; q_{\text{pos}},\; k_{\text{pos}}),\\
& q=Q^{\prime}_{\text{ego}},\; k=v=Q_{m},\\
& q_{\text{pos}}=\text{PE}_{2}(p_{\text{ego}}),\; k_{\text{pos}}=\text{PE}_{2}(p_{m}).
\end{split}
\]

**Planning Head.** Because VAD performs HD-map-free planning, a high-level driving command \(c\) is required for navigation. Following the common practice [19, 21], VAD uses three kinds of driving commands: _turn left_, _turn right_ and _go straight_. So the planning head takes the updated ego queries (\(Q^{\prime}_{\text{ego}},Q^{\prime\prime}_{\text{ego}}\)) and the current status of the ego vehicle \(s_{\text{ego}}\) (optional) as ego features \(f_{\text{ego}}\), as well as the driving command \(c\) as inputs, and outputs the planning trajectory \(\hat{V}_{\text{ego}}\in\mathbb{R}^{T_{f}\times 2}\). VAD adopts a simple MLP-based planning head. The decoding process is formulated as follows:

\[
\begin{split}
&\hat{V}_{\text{ego}}=\text{PlanHead}(\text{ft}=f_{\text{ego}},\; \text{cmd}=c),\\
&f_{\text{ego}}=[Q^{\prime}_{\text{ego}},\; Q^{\prime\prime}_{\text{ego}},\; s_{\text{ego}}].
\end{split}
\]

where [...] denotes concatenation operation, ft denotes features used for decoding, and cmd denotes the navigation driving command.

### 3.3 Vectorized Planning Constraint

Based on the learned map vector and motion vector, VAD regularizes the planning trajectory \(\hat{V}_{\text{ego}}\) with instance-level vectorized constraints during the training phase, as shown in Fig. 3.

**Ego-Agent Collision Constraint.** Ego-agent collision constraint explicitly considers the compatibility of the ego planning trajectory and the future trajectory of other vehicles, in order to improve planning safety and avoid collision. Unlike previous works [19, 21] that adopt dense occupancy maps, we utilize vectorized motion trajectories which both keep great interpretability and require less computation. Specifically, we first filter out low-confidence agent predictions by a threshold \(\epsilon_{a}\). For multi-modality motion prediction, we use the trajectory with the highest confidence score as the final prediction. We consider collision constraint as a safe boundary for the ego vehicle both laterally and longitudinally. Multiple cars may be close to each other (_e.g._, driving side by side) in the lateral direction, but a longer safety distance is required in the longitudinal direction. So we adopt different agent distance thresholds \(\delta_{X}\) and \(\delta_{Y}\) for different directions. For each future timestamp, we find the closest agent within a certain range \(\delta_{a}\) in both directions. Then for each direction \(i\in\{\text{X},\text{Y}\}\), if the distance \(d^{i}_{a}\) with the closet agent is less than the threshold \(\delta_{i}\), then the loss item of this constraint \(\mathcal{L}^{i}_{\text{col}}=\delta_{i}-d^{i}_{a}\), otherwise it is 0. The loss for ego-agent collision constraint can be formulated as:

\[
\begin{split}
\mathcal{L}_{\text{col}}&=\frac{1}{T_{f}}\sum_{t=1}^{T_{f}}\sum_{i}\mathcal{L}^{it}_{\text{col}},\; i\in\{\text{X},\text{Y}\},\\
\mathcal{L}^{it}_{\text{col}}&=\begin{cases}
\delta_{i}-d^{it}_{a}, &\text{if }d^{it}_{a}<\delta_{i}\\
0, &\text{if }d^{it}_{a}\geq\delta_{i}.
\end{cases}
\end{split}
\]

**Ego-Boundary Overstepping Constraint.** This constraint aims to push the planning trajectory away from the road boundary so that the trajectory can be kept in the drivable area. We first filter out low-confidence map predictions according to a threshold \(\epsilon_{m}\). Then for each future timestamp, we calculate the distance \(d^{i}_{bd}\) between the planning waypoint and its closest map boundary line. Then the loss for this constraint is formulated as:

\[
\begin{split}
\mathcal{L}_{\text{bd}}&=\frac{1}{T_{f}}\sum_{t=1}^{T_{f}}\mathcal{L}^{t}_{\text{bd}},\\
\mathcal{L}^{t}_{\text{bd}}&=\begin{cases}
\delta_{bd}-d^{t}_{bd}, &\text{if }d^{t}_{bd}<\delta_{bd}\\
0, &\text{if }d^{t}_{bd}\geq\delta_{bd},
\end{cases}
\end{split}
\]

where \(\delta_{bd}\) is the map boundary threshold.

**Ego-Lane Directional Constraint.** Ego-lane directional constraint comes from a prior that the vehicle's motion direction should be consistent with the lane direction where the vehicle locates. The directional constraint leverages the vectorized lane direction to regularize the motion direction of our planning trajectory. Specifically, first, we filter out low-confidence map predictions according to \(\epsilon_{m}\). Then we find the closest lane divider vector \(\hat{v}_{m}\in\mathbb{R}^{T_{f}\times 2\times 2}\) (within a certain range \(\delta_{\text{dir}}\)) from our planning waypoint at each future timestamp. Finally, the loss for this constraint is the angular difference averaged over time between the lane vector and the ego vector:

\[
\mathcal{L}_{\text{dir}}=\frac{1}{T_{f}}\sum_{t=1}^{T_{f}}\mathbb{P}_{\text{ang}}(\hat{v}^{t}_{m},\; \hat{v}^{t}_{\text{ego}}),
\]

in which \(\hat{v}_{\text{ego}}\in\mathbb{R}^{T_{f}\times 2\times 2}\) is the planning ego vectors. \(\hat{v}^{t}_{\text{ego}}\) denotes the ego vector starting from the planning waypoint at the previous timestamp \(t-1\) and pointing to the planning waypoint at the current timestamp \(t\). \(\text{F}_{\text{ang}}(v_{1},v_{2})\) denotes the angular difference between vector \(v_{1}\) and vector \(v_{2}\).

### 3.4 End-to-End Learning

**Vectorized Scene Learning Loss.** Vectorized scene learning includes vectorized map learning and vectorized motion prediction. For vectorized map learning, Manhattan distance is adopted to calculate the regression loss between the predicted map points and the ground truth map points. Besides, focal loss [30] is used as the map classification loss. The overall map loss is denoted as \(\mathcal{L}_{\text{map}}\).

For vectorized motion prediction, we use \(l_{1}\) loss as the regression loss to predict agent attributes (location, orientation, size, _etc._), and focal loss [30] to predict agent classes. For each agent who has matched with a ground truth agent, we predict \(N_{k}\) future trajectories and use the trajectory which has the minimum final displacement error (minFDE) as a representative prediction. Then we calculate \(l_{1}\) loss between this representative trajectory and the ground truth trajectory as the motion regression loss. And focal loss is adopted as the multi-modal motion classification loss. The overall motion prediction loss is denoted as \(\mathcal{L}_{\text{mot}}\).

**Vectorized Constraint Loss.** The vectorized constraint loss is composed of three constraints proposed in Sec. 3.3, _i.e._, ego-agent collision constraint \(\mathcal{L}_{\text{col}}\), ego-boundary over-stepping constraint \(\mathcal{L}_{\text{bd}}\), and ego-lane directional constraint \(\mathcal{L}_{\text{dir}}\), which regularize the planning trajectory \(\hat{V}_{\text{ego}}\) with vectorized scene representation.

**Imitation Learning Loss.** The imitation learning loss \(\mathcal{L}_{\text{imi}}\) is an \(l_{1}\) loss between the planning trajectory \(\hat{V}_{\text{ego}}\) and the ground truth ego trajectory \(V_{\text{ego}}\), aiming at guiding the planning trajectory with expert driving behavior. \(\mathcal{L}_{\text{imi}}\) is formulated as follows:

\[
\mathcal{L}_{\text{imi}}=\frac{1}{T_{f}}\sum_{t=1}^{T_{f}}||V^{t}_{\text{ego}}-\hat{V}^{t}_{\text{ego}}||_{1}.
\]

VAD is end-to-end trainable based on the proposed vectorized planning constraint. The overall loss for end-to-end learning is the weighted sum of vectorized scene learning loss, vectorized planning constraint loss, and imitation learning loss:

\[
\begin{split}
\mathcal{L}=\omega_{1}\mathcal{L}_{\text{map}}+\omega_{2}\mathcal{L}_{\text{mot}}+\omega_{3}\mathcal{L}_{\text{col}}+\\
\omega_{4}\mathcal{L}_{\text{bd}}+\omega_{5}\mathcal{L}_{\text{dir}}+\omega_{6}\mathcal{L}_{\text{imi}}.
\end{split}
\]

## 4. Experiments

We conduct experiments on the challenging public nuScenes [1] dataset, which contains 1000 driving scenes, and each scene roughly lasts for 20 seconds. nuScenes provides 1.4M 3D bounding boxes of 23 categories in total. The scene images are captured by 6 cameras covering 360° FOV horizontally, and the keyframes are annotated at 2Hz. Following previous works [19, 21], Displacement Error (DE) and Collision Rate (CR) are adopted to comprehensively evaluate the planning performance. For the closed-loop setting, we adopt CARLA simulator [12] and the Town05 [42] benchmark for simulation. Following previous works [42, 19], Route Completion (RC) and Driving Score (DS) are used to evaluate the planning performance.

### 4.1 Implementation Details

VAD uses 2-second history information and plans a 3-second future trajectory. ResNet50 [16] is adopted as the default backbone network for encoding image features. VAD performs vectorized mapping and motion prediction for a \(60\)m \(\times\) \(30\)m perception range longitudinally and laterally. We have two variants of VAD, which are VAD-Tiny and VAD-Base. VAD-Base is the default model for the experiments. The default number for BEV query, map query, and agent query is \(200\times 200\), \(100\times 20\), and \(300\), respectively. There is a total of 100 map vector queries, each containing 20 map points. The feature dimension and the default hidden size are 256. Compared with VAD-Base, VAD-Tiny has fewer BEV queries, which is \(100\times 100\). The number of BEV encoder layer and decoder layer of motion and map modules is reduced from 6 to 3, and the input image size is reduced from \(1280\times 720\) to \(640\times 360\).

As for training, the confidence thresholds \(\epsilon_{a}\) and \(\epsilon_{m}\) are set to 0.5, the distance thresholds \(\delta_{\text{a}},\delta_{\text{bd}}\) and \(\delta_{\text{dir}}\) are 3.0m, 1.0m, and 2.0m, respectively. The agent safety threshold \(\delta_{X}\) and \(\delta_{Y}\) are set to 1.5m and 3.0m. We use AdamW [36] optimizer and Cosine Annealing [35] scheduler to train VAD with weight decay 0.01 and initial learning rate \(2\times 10^{-4}\). VAD is trained for 60 epochs on 8 NVIDIA GeForce RTX 3090 GPUs with batch size 1 per GPU.

VAD-Base is adopted for the closed-loop evaluation. The input image size is \(640\times 320\). Following previous works [42, 19], the navigation information includes a sparse goal location and a corresponding discrete navigational command. This navigation information is encoded by an MLP and sent to the planning head as one of the input features. Besides, we add a traffic light classification branch to recognize the traffic signal. Specifically, it consists of a Resnet50 network and an MLP-based classification head. The input of this branch is the cropped front-view image, corresponding to the upper middle part of the image. The image feature map is flattened and also sent to the planning head to help the model realize the traffic light information.

### 4.2 Main Results

**Open-loop planning results.** As shown in Tab. 1, VAD shows great advantages in both performance and speed compared with the previous SOTA method [21]. On one hand, VAD-Tiny and VAD-Base greatly reduce the average planning displacement error by 0.25m and 0.31m. Meanwhile, VAD-Base greatly reduces the average collision rates by 29.0%. On the other hand, because VAD does not need many auxiliary tasks (_e.g._, tracking and occupancy prediction) and tedious post-processing steps, it achieves the fastest inference speed based on the vectorized scene representation. VAD-Tiny runs 9.3\(\times\) faster while keeping a comparable planning performance. VAD-Base achieves the best planning performance and still runs 2.5\(\times\) faster.It is worth noticing that in the main results, VAD omits ego status features to avoid shortcut learning in the open-loop planning [50], but the results of VAD using ego status features are still preserved in Tab. 1 for reference.

**Closed-loop planning results.** VAD outperforms previous SOTA vision-only end-to-end planning methods [42, 19] on the Town05 Short benchmark. Compared to ST-P3 [19], VAD greatly improves DS by 9.15 and has a better RC. On the Town05 Long benchmark, VAD achieves 30.31 DS, which is close to the LiDAR-based method [42], while significantly improving RC from 56.36 to 75.20. ST-P3 [19] obtains better RC but has a much worse DS.

### 4.3 Ablation Study

**Effectiveness of designs.** Tab. 2 shows the effectiveness of our design choices. First, because map can provide critical guidance for planning, the planning distance error is much larger without ego-map interaction (ID 1). Second, the ego-agent interaction and ego-map interaction provide implicit scene features for the ego query so that the ego car can realize others' driving intentions and plan safely. The collision rate becomes much higher without interaction (ID 1-2). Finally, the collision rate can be reduced with any of the vectorized planning constraints (ID 4-6). When utilizing the three constraints together, VAD achieves the lowest collision rate and the best planning accuracy (ID 7).

**Rasterized map representation.** We show the results of a VAD variant with rasterized map representation in Tab. 3. Specifically, this VAD variant utilizes map queries to perform BEV map segmentation instead of vectorized map detection, and the updated map queries are used in the planning transformer the same as VAD. As shown in Tab. 3, VAD with rasterized map representation suffers from a much higher collision rate.

**Runtime of each module.** We evaluate the runtime of each module of VAD-Tiny, and the results are shown in Tab. 5. Backbone and BEV Encoder take most of the runtime for feature extraction and transformation. Then motion module and map module take 34.6% of the total runtime to accomplish multi-agent vectorized motion prediction and vectorized map prediction. The runtime of the planning module is only 3.4ms, thanks to the sparse vectorized representation and concise model design.

### 4.4 Qualitative Results

We show three vectorized scene learning and planning results of VAD in Fig. 4. For a better understanding of the scene, we also provide raw surrounding camera images and project the planning trajectories to the front camera image. VAD can predict multi-modality agent motions and map elements accurately, as well as plan the ego future movements reasonably according to the vectorized scene representation. More visualizations are available in Appendix.

## 5. Conclusion

In this paper, we explore the fully vectorized representation of the driving scene, and how to effectively incorporate the vectorized scene information for better planning performance. The resulting end-to-end autonomous driving paradigm is termed VAD. VAD achieves both high performance and high efficiency, which are vital for the safety and deployment of an autonomous driving system. We hope the impressive performance of VAD can reveal the potential of vectorized paradigm to the community.

VAD predicts multi-modality motion trajectories for other dynamic agents, We use the most confident prediction in our collision constraint to improve planning safety. How to utilize the multi-modality motion predictions for planning, is worthy of future discussion. Besides, how to incorporate other traffic information (_e.g._, lane graph, road sign, traffic light, and speed limit) into this autonomous driving system, also deserves further exploration.

## Acknowledgement

This work was in part supported by the National Natural Science Foundation of China (No. 62276108).

## References

[1] Holger Caesar, Varun Bankiti, Alex H Lang, Sourabh Vora, Venice Erin Liong, Qiang Xu, Anush Krishnan, Yu Pan, Giancarlo Baldan, and Oscar Beijbom. nuscenes: A multi-modal dataset for autonomous driving. In _CVPR_, 2020.

[2] Sergio Casas, Abbas Sadat, and Raquel Urtasun. Mp3: A unified model to map, perceive, predict and plan. In _CVPR_, 2021.

[3] Yuning Chai, Benjamin Sapp, Mayank Bansal, and Dragomir Anguelov. Multipath: Multiple probabilistic anchor trajectory hypotheses for behavior prediction. _arXiv preprint arXiv:1910.05449_, 2019.

[4] Raphael Chekroun, Marin Toromanoff, Sascha Hornauer, and Fabien Moutarde. Gri: General reinforced imitation and its application to vision-based autonomous driving. _arXiv preprint arXiv:2111.08575_, 2021.

[5] Dian Chen, Vladlen Koltun, and Philipp Krahenbuhl. Learning to drive from a world on rails. In _ICCV_, 2021.

[6] Dian Chen, Brady Zhou, Vladlen Koltun, and Philipp Krahenbuhl. Learning by cheating. 2020.

[7] Long Chen, Lukas Platinsky, Stefanie Speichert, Blazej Osinski, Oliver Scheel, Yawei Ye, Hugo Grimmett, Luca Del Pero, and Peter Ondruska. What data do we need for training an av motion planner? In _ICRA_, 2021.

[8] Shaoyu Chen, Tianheng Cheng, Xinggang Wang, Wenming Meng, Qian Zhang, and Wenyu Liu. Efficient and robust 2d-to-bev representation learning via geometry-guided kernel transformer. _arXiv preprint arXiv:2206.04584_, 2022.

[9] Felipe Codevilla, Eder Santana, Antonio M Lopez, and Adrien Gaidon. Exploring the limitations of behavior cloning for autonomous driving. In _ICCV_, 2019.

[10] Felipe Codevilla, Eder Santana, Antonio M Lopez, and Adrien Gaidon. Exploring the limitations of behavior cloning for autonomous driving. 2019.

[11] Alexander Cui, Sergio Casas, Abbas Sadat, Renjie Liao, and Raquel Urtasun. Lookout: Diverse multi-future prediction and planning for self-driving. In _ICCV_, 2021.

[12] Alexey Dosovitskiy, German Ros, Felipe Codevilla, Antonio Lopez, and Vladlen Koltun. Carla: An open urban driving simulator. In _CoRL_, 2017.

[13] Jiyang Gao, Chen Sun, Hang Zhao, Yi Shen, Dragomir Anguelov, Congcong Li, and Cordelia Schmid. Vectornet: Encoding hd maps and agent dynamics from vectorized representation. In _CVPR_, 2020.

[14] David Gonzalez, Joshue Perez, Vicente Milanes, and Fawzi Nashashibi. A review of motion planning techniques for automated vehicles. _T-ITS_, 2015.

[15] Junru Gu, Chenxu Hu, Tianyuan Zhang, Xuanyao Chen, Yilun Wang, Yue Wang, and Hang Zhao. Vip3d: End-to-end visual trajectory prediction via 3d agent queries. _arXiv preprint arXiv:2208.01582_, 2022.

[16] Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. Deep residual learning for image recognition. In _Proceedings of the IEEE conference on computer vision and pattern recognition_, 2016.

[17] Anthony Hu, Zak Murez, Nikhil Mohan, Sofia Dudas, Jeffrey Hawke, Vijay Badrinarayanan, Roberto Cipolla, and Alex Kendall. Firey: Future instance prediction in bird's-eye view from surround monocular cameras. In _ICCV_, 2021.

[18] Peiyun Hu, Aaron Huang, John Dolan, David Held, and Deva Ramanan. Safe local motion planning with self-supervised freespace forecasting. In _CVPR_, 2021.

[19] Shengchao Hu, Li Chen, Penghao Wu, Hongyang Li, Junchi Yan, and Dacheng Tao. St-p3: End-to-end vision-based autonomous driving via spatial-temporal feature learning. In _ECCV_, 2022.

[20] Yihan Hu, Wenxin Shao, Bo Jiang, Jiajie Chen, Siqi Chai, Zhening Yang, Jingyu Qian, Helong Zhou, and Qiang Liu. Hope: Hierarchical spatial-temporal network for occupancy flow prediction. _arXiv preprint arXiv:2206.10118_, 2022.

[21] Yihan Hu, Jiazhi Yang, Li Chen, Keyu Li, Chonghao Sima, Xizhou Zhu, Siqi Chai, Senyao Du, Tianwei Lin, Wenhai Wang, et al. Goal-oriented autonomous driving. _arXiv preprint arXiv:2212.10156_, 2022.

[22] Bo Jiang, Shaoyu Chen, Xinggang Wang, Bencheng Liao, Tianheng Cheng, Jiajie Chen, Helong Zhou, Qian Zhang, Wenyu Liu, and Chang Huang. Perceive, interact, predict: Learning dynamic and static clues for end-to-end motion prediction. _arXiv preprint arXiv:2212.02181_, 2022.

[23] Alex Kendall, Jeffrey Hawke, David Janz, Przemyslaw Mazur, Daniele Reda, John-Mark Allen, Vinh-Dieu Lam, Alex Bewley, and Amar Shah. Learning to drive in a day. In _ICRA_, 2019.

[24] Tarasha Khurana, Peiyun Hu, Achal Dave, Jason Ziglar, David Held, and Deva Ramanan. Differentiable raycasting for self-supervised occupancy forecasting. 2022.

[25] Qi Li, Yue Wang, Yilun Wang, and Hang Zhao. Hdmapnet: An online hd map construction and evaluation framework. In _ICRA_, 2022.

[26] Zhiqi Li, Wenhai Wang, Hongyang Li, Enze Xie, Chonghao Sima, Tong Lu, Qiao Yu, and Jifeng Dai. Bevformer: Learning bird's-eye-view representation from multi-camera images via spatiotemporal transformers. _arXiv preprint arXiv:2203.17270_, 2022.

[27] Ming Liang, Bin Yang, Rui Hu, Yun Chen, Renjie Liao, Song Feng, and Raquel Urtasun. Learning lane graph representations for motion forecasting. In _ECCV_, 2020.

[28] Bencheng Liao, Shaoyu Chen, Bo Jiang, Tianheng Cheng, Qian Zhang, Wenyu Liu, Chang Huang, and Xinggang Wang. Lane graph as path: Continuity-preserving path-wise modeling for online lane graph construction. _arXiv preprint arXiv:2303.08815_, 2023.

[29] Bencheng Liao, Shaoyu Chen, Xinggang Wang, Tianheng Cheng, Qian Zhang, Wenyu Liu, and Chang Huang. Maptr: Structured modeling and learning for online vectorized hd map construction. _arXiv preprint arXiv:2208.14437_, 2022.

[30] Tsung-Yi Lin, Priya Goyal, Ross Girshick, Kaiming He, and Piotr Dollar. Focal loss for dense object detection. In _ICCV_, 2017.

[31] Yingfei Liu, Tiancai Wang, Xiangyu Zhang, and Jian Sun. Petr: Position embedding transformation for multi-view 3d object detection. _arXiv preprint arXiv:2203.05625_, 2022.

[32] Yicheng Liu, Yue Wang, Yilun Wang, and Hang Zhao. Vectornapnet: End-to-end vectorized hd map learning. _arXiv preprint arXiv:2206.08920_, 2022.

[33] Yicheng Liu, Jinghuai Zhang, Liangji Fang, Qinhong Jiang, and Bolei Zhou. Multimodal motion prediction with stacked transformers. In _CVPR_, 2021.

[34] Zhi Liu, Shaoyu Chen, Xiaojie Guo, Xinggang Wang, Tianheng Cheng, Hongmei Zhu, Qian Zhang, Wenyu Liu, and Yi Zhang. Vision-based uneven bev representation learning with polar rasterization and surface estimation. _CoRL_, 2022.

[35] Ilya Loshchilov and Frank Hutter. Sgdr: Stochastic gradient descent with warm restarts. _arXiv preprint arXiv:1608.03983_, 2016.

[36] Ilya Loshchilov and Frank Hutter. Decoupled weight decay regularization. _arXiv preprint arXiv:1711.05101_, 2017.

[37] Jiquan Ngiam, Benjamin Caine, Vijay Vasudevan, Zheng-dong Zhang, Hao-Tien Lewis Chiang, Jeffrey Ling, Rebecca Roelofs, Alex Bewley, Chenxi Liu, Ashish Venugopal, et al. Scene transformer: A unified architecture for predicting multiple agent trajectories. _arXiv preprint arXiv:2106.08417_, 2021.

[38] Tung Phan-Minh, Elena Corina Grigore, Freddy A Boulton, Oscar Beijbom, and Eric M Wolff. Covernet: Multimodal behavior prediction using trajectory sets. In _CVPR_, 2020.

[39] Jonah Philion and Sanja Fidler. Lift, splat, shoot: Encoding images from arbitrary camera rigs by implicitly unprojecting to 3d. In _ECCV_, 2020.

[40] Dean A Pomerleau. Alvinn: An autonomous land vehicle in a neural network. _NeurIPS_, 1988.

[41] Aditya Prakash, Kashyap Chitta, and Andreas Geiger. Multimodal fusion transformer for end-to-end autonomous driving. In _CVPR_, 2021.

[42] Aditya Prakash, Kashyap Chitta, and Andreas Geiger. Multimodal fusion transformer for end-to-end autonomous driving. 2021.

[43] Katrin Renz, Kashyap Chitta, Onriel-Bogdan Mercea, A Koepke, Zeynep Akata, and Andreas Geiger. Plant: Explainable planning transformers via object-level representations. _arXiv preprint arXiv:2210.14222_, 2022.

[44] Abbas Sadat, Sergio Casas, Mengye Ren, Xinyu Wu, Pranaab Dhawan, and Raquel Urtasun. Perceive, predict, and plan: Safe motion planning through interpretable semantic representations. In _ECCV_, 2020.

[45] Marin Toromanoff, Emilie Wirbel, and Fabien Moutarde. End-to-end model-free reinforcement learning for urban driving using implicit affordances. In _CVPR_, 2020.

[46] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Lukasz Kaiser, and Illia Polosukhin. Attention is all you need. _NeurIPS_, 2017.

[47] Yue Wang, Vitor Campagnolo Guizilini, Tianyuan Zhang, Yilun Wang, Hang Zhao, and Justin Solomon. Detr3d: 3d object detection from multi-view images via 3d-to-2d queries. In _CoRL_, 2022.

[48] Wenda Xu, Qian Wang, and John M Dolan. Autonomous vehicle motion planning via recurrent spline optimization. In _ICRA_, 2021.

[49] Wenyuan Zeng, Wenjie Luo, Simon Suo, Abbas Sadat, Bin Yang, Sergio Casas, and Raquel Urtasun. End-to-end interpretable neural motion planner. In _CVPR_, 2019.

[50] Jiang-Tian Zhai, Ze Feng, Jinhao Du, Yongqiang Mao, Jiang-Jiang Liu, Zichang Tan, Yifu Zhang, Xiaoqing Ye, and Jingdong Wang. Rethinking the open-loop evaluation of end-to-end autonomous driving in nuscenes. _arXiv preprint arXiv:2305.10430_, 2023.

[51] Yunpeng Zhang, Zheng Zhu, Wenzhao Zheng, Junjie Huang, Guan Huang, Jie Zhou, and Jiwen Lu. Beverse: Unified perception and prediction in birds-eye-view for vision-centric autonomous driving. _arXiv preprint arXiv:2205.09743_, 2022.

[52] Brady Zhou and Philipp Krahenbuhl. Cross-view transformers for real-time map-view semantic segmentation. In _CVPR_, 2022.

[53] Xizhou Zhu, Weijie Su, Lewei Lu, Bin Li, Xiaogang Wang, and Jifeng Dai. Deformable detr: Deformable transformers for end-to-end object detection. _arXiv preprint arXiv:2010.04159_, 2020.