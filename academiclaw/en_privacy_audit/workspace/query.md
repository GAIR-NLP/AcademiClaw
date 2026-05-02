````markdown
### 1. Query (Task Description)

**Task Name**: Build an LLM-based automated Reddit privacy information identification and audit system.

**Detailed Description**:
You need to develop an end-to-end automation script that accomplishes the following tasks:

1. **Data Cleaning**: Parse the provided Reddit RSS XML data, extract post bodies, and remove HTML tags, escape characters, and Reddit-specific redundant suffixes such as "submitted by".
2. **Privacy Classification**: Use a large language model to classify and label the cleaned text according to 12 predefined privacy categories.
3. **Closed-loop Audit**: Call a higher-tier model as an "auditor" to verify the classification results, outputting JSON-format results of `Confirmed`, `False Positive`, or `Missing`.
4. **Visual Report**: Compute privacy distribution statistics and calculate system accuracy, false positive rate (FPR), and false negative rate (FNR), then generate distribution charts (e.g., Bar Chart).

**Expected Output**:

- A complete, runnable Python script.
- A structured CSV dataset containing at least 50 records (including original text, classification labels, and audit results).
- Two analysis charts (privacy distribution chart and confusion matrix/error rate chart).

```
