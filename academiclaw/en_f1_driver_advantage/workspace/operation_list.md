# F1 Driver Stable Advantage Index Analysis Operation Reference

## Operation Steps

### 1. Understand Task Requirements
- Read the `query.md` file to understand the task objectives
- Review `data_intro.md` for the data structure

### 2. Analyze Data
- Examine the datasets in the `f1_2023_data` directory
- Understand the data formats and field definitions
- Analyze data quality and completeness

### 3. Implement Analysis
- Implement the stable advantage index calculation based on data characteristics
- Account for environmental factors affecting lap times
- Calculate relative advantages between drivers

### 4. Generate Output Files
- `stable_advantage.csv`: Contains the stable advantage index for each driver
- `teammate_comparison.csv`: Contains teammate comparisons
- `generalization_report.csv`: Contains generalization evaluation results

## Data Format Reference

### stable_advantage.csv
```csv
driver_id,driver_name,StableAdv_mean_s_per_lap,StableAdv_low_s_per_lap,StableAdv_high_s_per_lap,sample_laps_used
Lewis Hamilton,Lewis Hamilton,0.5,-0.1,1.1,120
Max Verstappen,Max Verstappen,1.2,0.8,1.6,115
```

### teammate_comparison.csv
```csv
season,team_id,team_name,driver_id_a,driver_id_b,adv_diff_mean_s_per_lap,adv_diff_low_s_per_lap,adv_diff_high_s_per_lap,laps_used_a,laps_used_b
2023,Mercedes,Mercedes,Lewis Hamilton,George Russell,0.3,0.1,0.5,120,118
2023,Red Bull,Red Bull,Max Verstappen,Sergio Perez,0.8,0.5,1.1,115,110
```

### generalization_report.csv
```csv
protocol,fold_id,n_laps_test,error_mae_s,error_rmse_s,interval_coverage,median_interval_width_s
LOCO,Monaco,50,0.2,0.3,0.9,0.4
LOCO,Silverstone,48,0.15,0.25,0.95,0.3
```

## Notes
- Ensure output formats are correct
- Consider the temporal nature of data and circuit characteristics
- Pay attention to calculation consistency and reasonableness
- Do not include standard answer content
- Ensure file encoding is UTF-8
