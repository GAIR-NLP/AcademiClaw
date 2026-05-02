Query:
---

【Query 描述】
请访问相关票房数据网站，为我分析并预测电影《阿凡达：火与烬》(Avatar: Fire and Ash)未来几日的票房表现。

**任务要求：**
1. 访问提供的票房数据网站，获取《阿凡达：火与烬》的实时票房数据
2. 收集并整理该电影的关键票房指标（如：首日票房、累计票房、排片占比、上座率等）
3. 分析票房走势，结合以下因素进行预测：
   - 历史数据趋势（日票房变化曲线）
   - 同档期竞争影片情况
   - 前作《阿凡达》系列的票房表现参考
   - 当前市场热度和口碑评分
4. 给出未来3-7天的票房预测，并说明预测依据

**输出文件要求：**

需要输出以下文件，便于评分时参考各阶段的工作成果：

### 1. 原始数据采集记录 `raw_data_collection.json`
记录从各网站采集的原始数据，便于验证数据来源的真实性：
```json
{
  "collection_timestamp": "YYYY-MM-DD HH:MM:SS",
  "sources": [
    {
      "source_name": "数据源名称（如：猫眼专业版）",
      "source_url": "访问的具体URL",
      "access_time": "访问时间ISO格式",
      "data_extracted": {
        "raw_fields": ["提取的原始字段列表"],
        "screenshot_saved": true/false,
        "extraction_method": "数据提取方式描述"
      },
      "raw_content": {
        "票房相关原始数据..."
      }
    }
  ],
  "total_sources_accessed": "访问的数据源总数",
  "data_collection_duration_seconds": "数据采集耗时（秒）"
}
```

### 2. 竞品分析数据 `competitor_analysis.json`
记录同档期竞争影片的详细数据：
```json
{
  "analysis_date": "YYYY-MM-DD",
  "target_movie": "阿凡达：火与烬",
  "competitors": [
    {
      "movie_name": "竞争影片名称",
      "release_date": "上映日期",
      "total_box_office": "累计票房",
      "daily_box_office": "当日票房",
      "market_share": "市场占比(%)",
      "screening_ratio": "排片占比(%)",
      "audience_score": "观众评分",
      "genre": "影片类型",
      "distributor": "发行公司"
    }
  ],
  "market_summary": {
    "total_daily_market": "当日大盘总票房",
    "target_market_share": "目标影片市场占比",
    "competition_intensity": "竞争激烈程度(high/medium/low)",
    "analysis_notes": "竞争态势分析备注"
  }
}
```

### 3. 历史对比数据 `historical_comparison.json`
记录与前作及类似影片的对比数据：
```json
{
  "comparison_date": "YYYY-MM-DD",
  "target_movie": {
    "name": "阿凡达：火与烬",
    "release_date": "上映日期",
    "days_since_release": "上映天数",
    "current_total": "当前累计票房"
  },
  "predecessor_comparison": [
    {
      "movie_name": "阿凡达 (2009)",
      "same_period_box_office": "同期票房（上映N天时）",
      "final_box_office": "最终票房",
      "comparison_ratio": "当前影片/前作同期 比值",
      "market_context": "当时市场环境描述"
    },
    {
      "movie_name": "阿凡达：水之道 (2022)",
      "same_period_box_office": "同期票房",
      "final_box_office": "最终票房",
      "comparison_ratio": "比值",
      "market_context": "市场环境"
    }
  ],
  "similar_movies_reference": [
    {
      "movie_name": "类似大片名称",
      "release_year": "上映年份",
      "genre": "类型",
      "same_period_performance": "同期表现",
      "final_performance": "最终表现",
      "relevance_score": "参考相关度(1-10)"
    }
  ],
  "trend_analysis": {
    "vs_predecessor_trend": "与前作对比趋势(better/similar/worse)",
    "market_position": "市场定位分析",
    "key_differences": ["与前作的关键差异点"]
  }
}
```

### 4. 数据摘要 `box_office_data.json`
整合后的结构化数据摘要：
```json
{
  "movie_name": "阿凡达：火与烬",
  "movie_name_en": "Avatar: Fire and Ash",
  "report_date": "YYYY-MM-DD",
  "report_generation_time": "YYYY-MM-DD HH:MM:SS",
  "data_sources": ["url1", "url2", ...],
  "current_data": {
    "total_box_office": "累计票房（亿元）",
    "total_box_office_usd": "累计票房（美元，如有）",
    "daily_box_office": "当日票房（万元）",
    "release_date": "上映日期",
    "release_days": "上映天数",
    "screening_ratio": "排片占比(%)",
    "attendance_rate": "上座率(%)",
    "avg_audience_per_show": "场均人次",
    "maoyan_score": "猫眼评分",
    "maoyan_want_to_see": "猫眼想看人数",
    "douban_score": "豆瓣评分",
    "douban_rating_count": "豆瓣评分人数"
  },
  "daily_trend": [
    {
      "date": "YYYY-MM-DD",
      "day_number": "上映第N天",
      "day_type": "weekday/weekend/holiday",
      "box_office": "票房（万元）",
      "screening_ratio": "排片占比(%)",
      "attendance_rate": "上座率(%)",
      "daily_change_rate": "环比变化率(%)"
    }
  ],
  "predictions": [
    {
      "date": "YYYY-MM-DD",
      "day_number": "上映第N天",
      "day_type": "weekday/weekend/holiday",
      "predicted_box_office": "预测票房（万元）",
      "predicted_box_office_range": {
        "low": "最低预测",
        "high": "最高预测"
      },
      "confidence": "high/medium/low",
      "prediction_basis": "预测依据简述"
    }
  ],
  "final_prediction": {
    "prediction_horizon": "预测周期（如：上映30天）",
    "min_estimate": "最低预测（亿元）",
    "max_estimate": "最高预测（亿元）",
    "most_likely": "最可能票房（亿元）",
    "confidence_level": "置信水平",
    "key_assumptions": ["关键假设1", "关键假设2"]
  },
  "metadata": {
    "analyst": "AI Assistant",
    "methodology_version": "v1.0",
    "last_updated": "YYYY-MM-DD HH:MM:SS"
  }
}
```

### 5. 分析报告 `box_office_analysis.md`
markdown格式的完整的分析报告（主输出文件），模板以context形式给出（若要增加任务难度，可选择不给）


**最终输出文件清单：**

| 序号 | 文件名 | 类型 | 说明 | 必需 |
|------|--------|------|------|------|
| 1 | `raw_data_collection.json` | JSON | 原始数据采集记录 | ✓ |
| 2 | `competitor_analysis.json` | JSON | 竞品分析数据 | ✓ |
| 3 | `historical_comparison.json` | JSON | 历史对比数据 | ✓ |
| 4 | `box_office_data.json` | JSON | 数据摘要（结构化） | ✓ |
| 5 | `box_office_analysis.md` | Markdown | 完整分析报告（主文件） | ✓ |

【Context】
- `context/links.md` 
- `context/analysis_template.md` (分析报告模板)