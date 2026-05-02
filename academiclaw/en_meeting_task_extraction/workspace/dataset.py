from datasets import load_dataset
import json

# 加载数据集
meetingbank = load_dataset("huuuyeah/meetingbank")
train_data = meetingbank['train']

# 创建要保存的数据列表
data_to_save = []

for idx, item in enumerate(train_data):
    data_to_save.append({
        "meeting_id": item["id"],
        "transcript": item["transcript"]
    })
    
    # 可选：限制处理的数量（用于测试）
    # if idx >= 100:
    #     break

# 保存为JSON文件
with open("meetingbank_data.json", "w", encoding="utf-8") as f:
    json.dump(data_to_save, f, ensure_ascii=False, indent=2)

print(f"已保存 {len(data_to_save)} 条数据到 meetingbank_data.json")