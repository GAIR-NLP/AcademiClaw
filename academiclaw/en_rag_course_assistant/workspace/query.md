### [Query System Implementation - RAG Course Assistant]

You need to implement a RAG-based course assistant system.

**Functional Requirements:**
- Document parsing: Support PDF, PPTX, DOCX, TXT, preserving metadata such as page numbers/slides/paragraphs.
- Text splitting: Support chunk_size and chunk_overlap.
- Vector database: Generate embeddings and write to ChromaDB, support Top-K retrieval.
- RAG Agent:
  - Define a system prompt (course assistant role, no fabrication allowed)
  - Retrieve and format context (including filename + page number/slide)
  - Answers must be evidence-based with citations

**Runtime Requirements:**
- Running `python process_data.py` should complete database building
- Running `python main.py` should enable interactive Q&A
- Regardless of whether data/ contains files of a certain format, all four loaders must be implemented

**Deliverables:**
- `process_data.py` — Completes data processing and database building
- `main.py` — Supports interactive Q&A with citations
- `vector_store.py` — Vector storage module
- `rag_agent.py` — RAG Agent core logic
- `config.py` — Configuration file
- `vector_db/` — Built vector database
