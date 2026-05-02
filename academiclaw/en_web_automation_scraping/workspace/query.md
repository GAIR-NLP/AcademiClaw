## Query Description

You are a Web automation testing expert. Your task is to write a Python script using **Playwright (Sync API)** to perform specific filtering operations on the `csrankings.org` website and extract data related to Shanghai Jiao Tong University (SJTU).

**Core Task Objective:**
Visit `https://csrankings.org/`, analyze the page DOM structure and interaction logic, filter ranking data for the **2020-2025** period, **World** scope, and **Artificial Intelligence (AI)** field, and extract SJTU's metrics.

**Specific Execution Steps:**

1.  **DOM Analysis (Reasoning)**:
    *   Analyze the HTML structure and infer the locators for "year dropdown", "region dropdown", "field checkboxes", and "data table rows".

2.  **Interaction Logic (Interaction)**:
    *   **Region Setting**: Switch Region to "World" (note the default value may differ).
    *   **Year Setting**: Lock the time range to [2020, 2025].
    *   **Field Filtering**:
        *   Select only **AI and its sub-fields** (Artificial intelligence, Computer vision, Machine learning, NLP, The Web & Information retrieval).
    *   *Note*: This website uses Client-side Rendering. After clicking controls, the URL Hash updates and the DOM table refreshes. The script must include appropriate **wait mechanisms** to ensure data loading is complete.

3.  **Data Extraction (Extraction)**:
    *   Locate "Shanghai Jiao Tong University" in the filtered table.
    *   Extract the following three fields:
        *   **Rank** (ranking)
        *   **Count** (geometric mean paper count)
        *   **Faculty** (faculty count)

**Output Requirements:**
After script execution, it must **only** print a valid JSON object to standard output (`stdout`) in the following format (do not output other debug logs):

```json
{
  "final_url": "Complete page URL at script end (including parameters)",
  "data": {
    "institution": "Shanghai Jiao Tong University",
    "rank": 4,
    "count": 10.5,
    "faculty": 45
  }
}
```

---

## Context
[dom_snippets.html](../context/dom_snippets.html)
This contains key HTML structure snippets of the target webpage. The model should read this content to infer interaction logic. This was obtained by directly previewing the source code in a browser.
