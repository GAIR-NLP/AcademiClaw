**Task: Analyze web server logs to identify security threats**

You are given Apache web server log files. Your task is to analyze these logs to identify potential security threats and generate a security report.

**Context:**
- Log files are in the `context/logs/` directory
- Logs follow Apache Common Log Format
- You should look for:
  - Suspicious IP addresses with unusual activity patterns
  - Potential SQL injection attempts
  - Directory traversal attempts
  - Unusual user agent strings
  - High-frequency requests from single IPs

**Requirements:**
1. Create a Python script `analyze_logs.py` that:
   - Parses all log files in the `context/logs/` directory
   - Identifies suspicious activities based on predefined patterns
   - Generates a security report `security_report.txt`
2. The security report should include:
   - Top 10 suspicious IP addresses with request counts
   - Detected attack patterns with examples
   - Timeline of suspicious activities
   - Recommendations for blocking/mitigation

**Important - Deliverable Location:**
- **Put all deliverables directly in this directory (outside of `context/`)**
- Do NOT put deliverables inside `context/` - they will not be evaluated

**Deliverable:**
- `analyze_logs.py` - Analysis script (in this directory, not in context/)
- `security_report.txt` - Generated security report (in this directory, not in context/)

**Evaluation:**
The analysis will be evaluated based on the accuracy of threat detection and completeness of the security report.