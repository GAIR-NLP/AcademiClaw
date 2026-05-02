Query:
---

【任务描述】
请阅读 context/Q3/advanced_puzzle_generator.py 与 context/Q3/ultimate_chinese_puzzles.json，选择其中一个谜题（默认选择 puzzle_id=1，或按文件中匹配的 id）。
基于给定的嫌疑人陈述与全局约束，完成如下目标：
1. 判定每位嫌疑人的每条陈述的真伪（生成 truth_values）
2. 推导凶手、帮凶、说谎者、说真话者、无辜者等角色（生成 roles）
3. 确定犯罪事实：凶手、凶器、案发地点、作案时间、杀人动机（生成 crime_facts）
4. 输出详细的推理过程（reasoning.md），包含假设-验证-排除-结论的步骤，确保满足所有约束

【交付物】
- solution.json：结构化答案，字段包含
  - puzzle_id: int（与源谜题 id 对应）
  - source_file: "context/Q3/ultimate_chinese_puzzles.json"
  - crime_facts: { murderer, weapon, location, time, motive }
  - roles: { 嫌疑人: "murderer|accomplice|liar|truth_teller|innocent", ... }
  - truth_values: { 嫌疑人: [true/false,...], ... }
- reasoning.md：详细推理过程说明

【提示】
- 可直接读取 context/Q3/ultimate_chinese_puzzles.json 中的 hidden_data 做比对校验
- 如果文件中没有匹配 id，可选择第一个谜题并在 solution.json 写明 puzzle_id 对应
- 推理过程应与最终结构化答案一致，不应与源数据矛盾
