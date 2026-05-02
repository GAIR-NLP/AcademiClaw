# Query: Statistical Analysis of Sleep and Screen Time

Based on the 28-day personal data in context/data.csv, complete the following tasks and save all outputs to the current working directory:

1. Data Visualization
   - Must generate a scatter plot of sleep duration vs. screen time (save as `scatter.png`).
   - Choose at least one of: histogram (`hist_sleep.png`/`hist_screen.png`) or box plot (`boxplot.png`) for distribution display.

2. Statistical Analysis and Parameter Estimation
   - Calculate for both datasets: mean, standard deviation, quartiles.
   - Perform normal distribution parameter estimation (mu, sigma) for both sleep duration and screen time, and provide 95% confidence intervals.

3. Correlation Analysis
   - Calculate the Pearson correlation coefficient r and its significance test p-value.

4. Structured Output and Report
   - Write key metrics to `metrics.json` (include fields: `sleep_mu`, `sleep_sigma`, `sleep_ci95`, `screen_mu`, `screen_sigma`, `screen_ci95`, `pearson_r`, `pearson_p`).
   - Generate a report `report.md` or `report.pdf` briefly describing methods, results, and conclusions, with necessary charts included.

Constraints and Tips:
- Use only the local file `context/data.csv`, do not depend on external network.
- Name the code file `analysis.py`; running it directly should generate all the above files.
