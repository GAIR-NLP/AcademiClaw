# 谜语解谜任务

## 任务目标
给定一组中文谜语，请为每个条目输出你预测的"谜底"。

## 输入
- `query.json` 中包含数组 `items`，每个 item 具有：
  - `id`
  - `category`
  - `riddle`

## 输出（你的提交）
请生成一个 JSON 文件 `submission.json`，格式如下：

```json
{
  "predictions": [
    {"id": "动物类/001", "prediction": "狼"},
    {"id": "水果类/003", "prediction": "香蕉"}
  ]
}
```

### 要求
- 输出必须是合法 JSON。
- `predictions` 数组中的每个元素必须包含 `id` 和 `prediction` 字段。
- `id` 必须与 `query.json` 中的 `id` 一致。
- `prediction` 必须仅包含**最终简短答案字符串**（不要包含解释）。
- 请为 `query.json` 中的所有谜语提供预测答案。

## 参考
- `submission_example.json` 提供了提交格式的示例。
- `operation_list.md` 提供了操作参考。
