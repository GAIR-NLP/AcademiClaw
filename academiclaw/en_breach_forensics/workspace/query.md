[Query Description]

**Title:** Incident Response: Proprietary App Breach Investigation

**Role:** Senior Security Analyst.

**Scenario:**
Our SIEM system detected a suspicious outbound connection from our internal file server (`103.45.12.99`) at 03:00 AM. 
Management believes the **File Upload** feature was exploited, but we don't know how.

**Resources:**
You have access to the server logs (`nginx_access.log`), the complete application source code (`.py` files), and the storage directory (`uploads/`).

**Mission:**
Perform a "Black Box" investigation to determine the extent of the breach and secure the system.

**Objectives:**

1.  **Forensic Decryption (The "What"):**
    *   Locate the attacker's entry point in `nginx_access.log`.
    *   The User-Agent string contains an obfuscated payload. **Reverse-engineer the obfuscation logic** by analyzing the application source code configuration to find the decryption method/keys.
    *   Report the **exact cleartext command** the attacker executed.

2.  **Threat Hunting (The "Where"):**
    *   Audit the `uploads/` directory. Identify any file that poses a security threat.
    *   Explain *technically* why this file is dangerous despite having a safe extension.

3.  **Vulnerability Patching (The "Fix"):**
    *   Modify `upload_server.py` to prevent this attack vector.
    *   **Constraint:** You must encapsulate your fix in a function named **`validate_image_header(file_stream)`**.
    *   *Requirement:* The fix must be robust enough to reject "spoofed" files (like the one you found) while allowing legitimate images.

4.  **Containment:**
    *   Write a script `cleanup.sh` to remove the identified malware and block the attacker's IP.

**Deliverables:**

1.  `Incident_Report.md`: Analysis of the attack vector and the decrypted payload.
2.  `secure_upload.py`: The patched server code.
3.  `cleanup.sh`: The containment script.

[Context]:

The following files are available in the `context/` directory:

- `context/uploads/` — the storage directory containing uploaded files
- `context/nginx_access.log` — the server access logs
- `context/upload_server.py` — the application source code
- `context/config.py` — the application configuration