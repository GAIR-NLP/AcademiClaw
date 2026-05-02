# Extract Task List from Meeting Minutes

Please read the dataset.py file in the workspace directory to understand the dataset preparation method. Your task is to extract action items from meeting transcription text (transcript) and model task dependency relationships.

## Task Requirements

### 1. Action Item Extraction and Normalization

Each action item must include:
- `task_id`: Task ID
- `assignee`: Person responsible
- `action`: Action description
- `object`: Action object (may be empty)
- `deadline`: Due date (if present)
- `source_span`: Position in original text

Output format: `action_items.json` (JSON format task list)

### 2. Task Dependency Modeling

- Automatically infer dependencies between tasks (semantic, temporal, logical dependencies)
- Build an acyclic dependency graph (DAG)
- Output format: `dependency_graph.json` (JSON object containing an edges list)

### 3. Provide Meeting Transcription Text

- Save the meeting transcription text used for extraction as `transcript.txt`

## Deliverables

After completing the task, save all deliverables in the current directory:

1. `action_items.json` - Structured task list (JSON format)
2. `dependency_graph.json` - Task dependency graph (JSON format, containing edges array)
3. `transcript.txt` - Meeting transcription text (for span grounding verification)
