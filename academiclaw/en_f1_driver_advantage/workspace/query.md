# Benchmark 2 (Revised): Driver "Environment-Stripped" Stable Advantage Index

Description
- **Scoring is based solely on submitted result files (numerical values, structure, consistency, verifiable prediction performance)**; no specific model type is required or checked.
- Participants may use any modeling/inference/machine learning method; the scorer only reads output files and performs automated calculations.

Objective
- Estimate the "driver stable advantage" metric from multi-session lap time data (unit: seconds/lap, higher is better), and provide uncertainty intervals.
- Additionally provide: teammate comparison (within-team differences and significance/confidence intervals), and cross-circuit or cross-session prediction generalization evaluation results (measured by error and interval coverage).

Allowed Data Resources
- Session data (CSV): lap times, pit stop markers, etc.
- Tire data (CSV): compound, tire_age_laps, etc.
- Weather data (CSV): air_temp, track_temp, humidity, wind_speed, rain_intensity, etc.
- Circuit data (CSV): circuit characteristics
- Driver/team data (CSV): driver_id, team_id, etc.
- Data dictionary, version log (Markdown)
- Prohibited: external data sources (race penalties, radio communications, dedicated telemetry signals, or other unprovided resources)

Unified Primary Key & Filtering (Reference; not scored but recommended)
- Primary key: {season, round, session_type, circuit_id, driver_id, stint_id, lap_number}
- Recommended filtering:
  - Exclude laps with is_pit_in==True or is_pit_out==True
  - Exclude laps with lap_time<=0 or extreme outliers (must be reflected in the anomaly list)
  - Wet condition identification: rain_intensity>0 or compound in {Inter, Wet}

---

## Required Output Files and Format (scoring is strictly based on the following files)

1) stable_advantage.csv
- Purpose: Submit the final "stable advantage" metric (method-agnostic).
- Columns:
  - driver_id
  - driver_name (optional but recommended)
  - StableAdv_mean_s_per_lap (stable advantage mean, in seconds/lap, higher is better)
  - StableAdv_low_s_per_lap (interval lower bound, e.g. 95%)
  - StableAdv_high_s_per_lap (interval upper bound, e.g. 95%)
  - sample_laps_used (number of laps used for estimation; used for scoring weight and quality checks)
- Row granularity: one row per driver_id

2) teammate_comparison.csv
- Purpose: Provide within-team comparison output (only numerical values and consistency are scored).
- Columns:
  - season (can be extended for multi-season; recommended even for single season)
  - team_id
  - team_name (optional)
  - driver_id_a, driver_id_b (two teammates, deduplicated by lexicographic order)
  - adv_diff_mean_s_per_lap = StableAdv_mean(a) - StableAdv_mean(b)
  - adv_diff_low_s_per_lap
  - adv_diff_high_s_per_lap
  - laps_used_a, laps_used_b
- Row granularity: one row per (team_id, driver_id_a, driver_id_b)

3) generalization_report.csv
- Purpose: Submit "generalization evaluation" results (method-agnostic; only checks whether results are reasonable and measurable).
- Evaluation protocol (fixed for automated scoring):
  - Submit at least one of two holdout protocols; submitting both yields a higher score ceiling:
    1) Leave-One-Circuit-Out (LOCO): hold out by circuit_id
    2) Leave-One-SessionType-Out (LOSO): hold out by session_type
- Columns:
  - protocol in {LOCO, LOSO}
  - fold_id (e.g. the held-out circuit_id or session_type)
  - n_laps_test
  - error_mae_s (MAE on test set for lap_time, in seconds)
  - error_rmse_s (optional)
  - interval_coverage (proportion of true lap_time falling within prediction interval; leave blank if no prediction interval is provided, but this affects the score)
  - median_interval_width_s (median interval width on test set; leave blank if not provided but affects score)
- Row granularity: one row per fold (must cover at least 80% of all circuits or all session types)

4) lap_level_predictions.parquet (or .csv; parquet recommended)
- Purpose: Used by the scorer to "recompute" generalization error and coverage, preventing submission of summary-only numbers.
- Content: For each test sample lap, output its prediction and interval (no specific model required).
- Columns:
  - season, round, session_type, circuit_id, driver_id, lap_number
  - lap_time_s_true
  - lap_time_s_pred_mean
  - lap_time_s_pred_low
  - lap_time_s_pred_high
  - split_tag (e.g. train/test, used to identify test set samples in generalization evaluation; if the same lap appears in multiple folds, include fold_id)
  - fold_id (aligned with generalization_report; optional but strongly recommended)
- Row granularity: one row per lap (must include at least all test sample laps; recommended to include all laps with labels)

5) anomalies.csv
- Purpose: List of anomalous/excluded laps (only checked for completeness and reasonableness; the detection method is not evaluated).
- Columns:
  - season, round, session_type, circuit_id, driver_id, lap_number
  - reason in {pit_in, pit_out, invalid_time, outlier, missing_feature, wet_excluded, other}
- Row granularity: one row per excluded lap

6) manifest.json
- Purpose: Metadata (not scored for methodology, but used by the scorer to interpret interval semantics and protocol).
- Recommended fields:
  - dataset_version (reference version number or date from the version log)
  - season_range
  - interval_level (e.g. 0.95)
  - wet_handling in {excluded, modeled_together, modeled_separately}
  - protocols_included (LOCO/LOSO)
  - units declaration (time in seconds, temperature in Celsius)

---


**[Deliverable File Requirements]**
- `lap_level_predictions.csv` — Per-lap prediction data
- `schedule.csv` — Schedule data
- `circuits.csv` — Circuit data
- `laps.csv` — Lap time data
Please save the above files in the current directory.
