# AcademiClaw 任务概览

> 本文件对 AcademiClaw benchmark 中全部 80 个 query 进行一句话简要说明。

## English Tasks（49 个）

| # | 任务名称 | 简要说明 |
|---|---------|---------|
| 1 | en_a3c_ppo_training | 实现并训练 A3C 和 PPO 强化学习算法，在 Pendulum-v1 上达到收敛。 |
| 2 | en_ai_science_report | 撰写 AI 在科研中应用的 LaTeX 格式学术分析报告。 |
| 3 | en_bibtex_reference_gen | 为 41 篇论文检索并编写完整的 BibTeX 引用条目。 |
| 4 | en_blackhole_visualization | 用 Three.js 实现星际穿越风格的黑洞可视化单页 HTML。 |
| 5 | en_breach_forensics | 分析服务器日志和源码，还原入侵过程并修补上传漏洞。 |
| 6 | en_bvh_path_tracing | 补全 BVH 光线追踪渲染器的核心交叉与渲染逻辑。 |
| 7 | en_checkers_alphabeta_pruning | 实现带 Alpha-Beta 剪枝的 Minimax 跳棋 AI 并胜率超 80%。 |
| 8 | en_chip_edge_detection | 实现高分辨率芯片环形内边缘检测算法并满足精度要求。 |
| 9 | en_cmo_proof | 完成 CMO 2024 第6题关于序列宽度下界的数学证明。 |
| 10 | en_data_analysis_study_plan | 设计面向数据分析面试的 30 天个性化学习计划。 |
| 11 | en_ddqn_mountaincar | 实现 Double DQN 算法并在 MountainCar-v0 上 200 步内登顶。 |
| 12 | en_dijkstra_optimize | 重构并优化 Dijkstra 算法实现，提交性能对比报告。 |
| 13 | en_distributed_consistency_design | 设计分布式电商系统的数据一致性解决方案。 |
| 14 | en_docker_env_config | 为 Python 项目编写 Dockerfile 解决环境依赖问题。 |
| 15 | en_document_qa_citation | 基于 PDF 报告回答 4 个问题并标注页码来源。 |
| 16 | en_dqn_implementation | 补全 DQN 和 Double DQN 代码模板中的 TODO 逻辑。 |
| 17 | en_dqn_migration | 将 TensorFlow DQN 代码迁移到 PyTorch 并添加调参可视化。 |
| 18 | en_emotion_recognition | 改进面部情感识别 CNN 模型以显著提升验证准确率。 |
| 19 | en_f1_driver_advantage | 从 F1 圈速数据中估计车手稳定优势指数并进行泛化评估。 |
| 20 | en_fullstack_debug | 调试并完成 React + FastAPI 德语词汇本应用的前后端联调。 |
| 21 | en_geometry_circles | 求解两圆相交几何题中弦 MN 的最大值。 |
| 22 | en_graph_algorithms | 实现 Dijkstra、Bellman-Ford 等五种图算法并对比性能。 |
| 23 | en_ksat_random_walk | 将 2-SAT 随机游走算法推广到 k-SAT 并完成六道证明题。 |
| 24 | en_lc3_calculator | 用 LC-3 汇编实现基于栈的计算器，支持加乘模异或等运算。 |
| 25 | en_locking_dance_choreo | 为 Funk 曲目编排 8x8 拍 Locking 舞蹈动作方案。 |
| 26 | en_log_security_analysis | 编写脚本分析 Apache 日志并生成安全威胁报告。 |
| 27 | en_mahjong_rl_agent | 设计基于强化学习的麻将出牌 AI 并实现标准接口。 |
| 28 | en_meeting_task_extraction | 从会议记录中提取结构化任务列表和依赖关系图。 |
| 29 | en_omniasr_deployment | 在 Ascend 平台上部署 omnilingual-asr 语音识别模型。 |
| 30 | en_os_lab3_debug | 定位并修复操作系统课 Lab3 的代码缺陷使其通过测试。 |
| 31 | en_os_lab3_report | 撰写 ChCore Lab3 进程与线程实验的完整课程报告。 |
| 32 | en_paper_presentation | 分析多篇论文并用 python-pptx 生成学术分析 PPT。 |
| 33 | en_pokemon_game | 开发单文件 HTML5 宝可梦 Gen3 风格的地图与回合制战斗游戏。 |
| 34 | en_ppo_pendulum | 实现 PPO 算法在 Pendulum-v1 连续动作空间上训练至收敛。 |
| 35 | en_privacy_audit | 构建基于 LLM 的 Reddit 隐私信息识别与审计系统。 |
| 36 | en_qwen_quantization_deploy | 完成 Qwen2.5-1.5B 模型的混合精度量化部署全流程。 |
| 37 | en_rag_course_assistant | 实现基于 RAG 的课程问答助手，支持多格式文档解析与检索。 |
| 38 | en_robocasa_camera_move | 在 Robocasa 仿真环境中实现动态相机位姿控制与离屏渲染。 |
| 39 | en_sift_algorithm_report | 撰写涵盖原理、实现、匹配及改进对比的 SIFT 算法研究报告。 |
| 40 | en_sift_homework_report | 完成包含透视投影证明和 SIFT 实验分析的课程作业报告。 |
| 41 | en_sleep_screen_stats | 对睡眠与屏幕时间数据进行统计分析、参数估计及可视化。 |
| 42 | en_speculative_decoding | 实现支持随机采样的投机解码推理引擎并验证加速效果。 |
| 43 | en_speech_model_report | 撰写语音基础模型技术演进与前沿架构的综述报告。 |
| 44 | en_sphere_uformer_export | 将 RGB 和深度图按 Sphere UFormer 输入格式导出为点云 npy 文件。 |
| 45 | en_stock_greedy_algo | 用反悔贪心和最小堆实现含手续费的股票最大收益算法。 |
| 46 | en_svd_model_merging | 实现基于 SVD 的各向同性多任务模型合并算法 Iso-C 和 Iso-CTS。 |
| 47 | en_time_tracking_dashboard | 实现响应式时间追踪仪表盘前端并支持日/周/月视图切换。 |
| 48 | en_tts_research_report | 撰写文本转语音前沿技术与架构演进的综述报告。 |
| 49 | en_web_automation_scraping | 用 Playwright 自动化操作 csrankings 网站并提取 SJTU 排名数据。 |

## 中文 Tasks（31 个）

| # | 任务名称 | 简要说明 |
|---|---------|---------|
| 1 | zh_alc_zhishiku | 从《百年孤独》文本中构建 ALC 描述逻辑知识库。 |
| 2 | zh_bisai_tongji | 解析比赛 CSV 数据并生成队伍统计与实力预测报告。 |
| 3 | zh_chepai_shibie | 实现中国车牌 GUI 识别系统，准确率需达 85% 以上。 |
| 4 | zh_chuanxi_diaoyan | 规划 8 人 7 天川西学术调研并应对突发事件动态重构方案。 |
| 5 | zh_datika_yueju | 批量识别 46 张高中物理答题卡并计算学生得分。 |
| 6 | zh_esp32_fenxi | 分析 ESP32 嵌入式项目代码并生成技术分析报告。 |
| 7 | zh_excel_zhengli | 对奖学金 Excel 汇总表进行清洗、去重、排序与排版美化。 |
| 8 | zh_gailv_daan | 为概率统计考试试卷编写完整的参考答案与知识点说明。 |
| 9 | zh_geci_chuangzuo | 以古典诗词为素材创作融合意象的现代歌词。 |
| 10 | zh_hangzhou_lvyou | 为首次杭州 3 天旅行规划轻松的自然与文化行程攻略。 |
| 11 | zh_huaxue_jingsai | 解答第 36 届中国化学奥林匹克初赛全部题目。 |
| 12 | zh_jiazu_tupu | 从《百年孤独》中提取完整的布恩迪亚家族谱系。 |
| 13 | zh_jidi_fuxi | 整合 13 份极地课件生成复习笔记和模拟试卷。 |
| 14 | zh_liaotian_niandu_baogao | 基于 107 条聊天记录生成主题分析与用户画像年度报告。 |
| 15 | zh_majiang_jisuanqi | 实现支持多种规则的立直麻将晋级条件计算器。 |
| 16 | zh_miti_tuili | 通过逻辑推理判定谜题中各嫌疑人陈述真伪与犯罪事实。 |
| 17 | zh_miyu_jiemi | 为一组中文谜语给出正确谜底。 |
| 18 | zh_peiyang_jihua | 基于课程数据生成 AI 专业培养计划的学期排课方案。 |
| 19 | zh_piaofang_yuce_fenxi | 采集并分析《阿凡达：火与烬》票房数据并预测走势。 |
| 20 | zh_readme_shengcheng | 为 Web 项目编写包含 7 个章节的完整 README 文档。 |
| 21 | zh_shengwu_zongshu | 撰写不少于 5000 字的生物数据库综述报告并输出 PDF。 |
| 22 | zh_shuangpin_jiucuo | 在 100 条双拼编码中定位每条多余字母的索引。 |
| 23 | zh_shuju_baogao | 下载公开数据并生成含可视化和分析的完整数据报告。 |
| 24 | zh_shujuwajue_xuanti | 制定数据挖掘课程项目的选题策划与展示方案。 |
| 25 | zh_wangzhe_elo_baogao | 撰写王者荣耀 ELO 匹配机制研究与实战策略报告。 |
| 26 | zh_wuli_jingsai | 完成第 38 届全国中学生物理竞赛复赛试题的完整解答。 |
| 27 | zh_xushi_xuxie | 模仿上半部分的修改风格续写优化下半部分叙事文章。 |
| 28 | zh_yanjiang_zhuanhua | 将量子计算学术论文转化为面向高中生的通俗演讲稿。 |
| 29 | zh_yuyanxue_aosai | 解答第 22 届国际语言学奥赛五道个人赛题目。 |
| 30 | zh_zidong_jiashi_diaoyan | 基于 5 篇文献撰写自动驾驶产业与技术路线调研报告。 |
| 31 | zh_zuowen_pingfen | 按评分细则为约 111 篇作文逐篇打分并撰写评语。 |
