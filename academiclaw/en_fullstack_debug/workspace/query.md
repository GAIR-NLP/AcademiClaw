
# Query 3:
## Task Description

```
This task provides a pre-implemented pure frontend React app and a pure backend FastAPI service. Both can run independently, but the frontend-backend integration has not been completed yet, and some features do not work properly.

The application is a "Custom German Vocabulary Notebook" with only the "Verbs" module currently implemented. Key features include:
- Home page displays multiple word category entries (Verbs, Nouns, Adjectives, Prepositions, Adverbs), with only the "Verbs" entry functional
- Verb list page displays all saved German verbs, sorted alphabetically
- Each verb entry shows "German word + Chinese translation"
- Clicking the "View Conjugation" button expands the German verb conjugation table on the current page (no page navigation)
- Users can add new verb entries through the "Add Verb" form

Currently, the frontend and backend have not completed integration regarding API calls, data structures, or state updates.

Your task is:
1. Read and understand the provided frontend and backend code structure and implementation
2. Complete the frontend-backend integration so the frontend can correctly call the backend API
3. Fix issues caused by inconsistent interfaces or data structures
4. Modify the frontend and/or backend code with minimal necessary changes
5. Ensure the application's core functionality works correctly

Expected final results:
- Frontend can correctly load and display the verb list
- Verb list is sorted alphabetically
- Clicking "View Conjugation" correctly renders the verb conjugation table
- After adding a new verb, the list correctly updates and displays the new content
- Frontend-backend communication works without runtime errors

--------------------------------------------------
[Backend Code Structure (FastAPI)]

backend/
├── main.py
│   - FastAPI application entry point
│   - Defines REST API routes
│   - Provides the following endpoints:
│       GET  /verbs        Get all verbs (alphabetically sorted)
│       GET  /verbs/{id}   Get a single verb's details
│       POST /verbs        Add a new verb
│
├── models.py
│   - Defines data models (Pydantic)
│   - Includes:
│       Verb               Verb entity (id, word, meaning, conjugations)
│       Conjugations       Verb conjugation structure
│       Indikativ          Indicative mood (present, past, perfect)
│       Tense              Person conjugation (ich/du/er/wir/ihr/sie)
│
├── data.py
│   - Uses in-memory data storage for the initial verb list
│   - Provides sample verbs with their complete conjugations
│
└── README.md
    - Backend startup instructions (run with uvicorn)

--------------------------------------------------
[Frontend Code Structure (React + TypeScript)]

frontend/src/
├── api/
│   └── verbs.ts
│       - Encapsulates frontend HTTP requests to the backend
│       - Contains methods for fetching the verb list and adding new verbs
│
├── pages/
│   ├── Home.tsx
│   │   - Application home page
│   │   - Displays multiple word category entries (only Verbs is clickable)
│   │
│   └── VerbList.tsx
│       - Verb list page
│       - Responsible for loading verb data and rendering the list
│       - Contains "Back to Home" and "Add Verb" entry points
│
├── components/
│   ├── VerbItem.tsx
│   │   - Single verb entry component
│   │   - Displays word and Chinese translation
│   │   - Controls conjugation table expand/collapse
│   │
│   ├── ConjugationTable.tsx
│   │   - Verb conjugation table component
│   │   - Displays present, past, and perfect tense conjugations for 6 persons in table format
│   │
│   └── AddVerbModal.tsx
│       - Add verb form component
│       - Used to submit new verb data
│
├── types/
│   └── verb.ts
│       - Frontend TypeScript type definitions
│       - Defines Verb, Conjugations, and other interfaces
│
├── App.tsx
│   - Application entry component
│   - Controls switching between home page and verb list page
│
└── main.tsx
    - React application startup entry point
```

## Context

File list:
- All files in ./backend/
- All files in ./frontend/


**[Key Deliverable Files]**
- `frontend/package.json` — Frontend project dependency configuration (required)
- `backend/` — Backend code directory
- `frontend/` — Frontend code directory
