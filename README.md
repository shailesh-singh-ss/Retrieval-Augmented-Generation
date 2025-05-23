# RAG Pipeline

A complete Retrieval-Augmented Generation system using Google’s Gemini model (with ChromaDB and SQLModel).

---

## 1. Prerequisites

- Python 3.10+
- [Docker & Docker-Compose](https://docs.docker.com/)
- A Google API key with access to Gemini
- (Optional) A virtual environment tool (venv, conda, etc.)

## 2. Setup & Installation

1. Clone the repo  
   `git clone https://github.com/your_org/retrieval-augmented-generation.git`  
   `cd retrieval-augmented-generation`

2. Create & activate a venv  
   `python -m venv .venv`  
   Windows: `.venv\Scripts\activate`  
   Unix/macOS: `source .venv/bin/activate`

3. Install dependencies  
   `pip install -r requirements.txt`

4. Copy & configure environment  
   `cp .env.example .env`  
   Fill in your `GEMINI_API_KEY`, `GEMINI_MODEL`, etc.

5. Initialize the metadata database  
   `python -c "from app.main import on_startup; import asyncio; asyncio.run(on_startup())"`

## 3. Running the Service

### a) Locally with Uvicorn

```bash
export CHROMA_HOST=localhost
export CHROMA_PORT=8000
# ...other env vars
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

### b) Using Docker-Compose

```bash
docker-compose up --build
```

This will start:
- **ChromaDB** on port `8000`
- **RAG API** on port `8001`

---

## 4. API Usage

Base URL: `http://<host>:8001/api/v1`

### Health check  
GET  `/health/`  
Response:  
```json
{ "status": "healthy" }
```

### Upload documents  
POST `/documents/upload`  
Form-data: one or more files under key `files`  
```bash
curl -F "files=@./doc1.pdf" -F "files=@./notes.txt" \
  http://localhost:8001/api/v1/documents/upload
```

### Query endpoint  
POST `/query/query`  
Body (JSON):
```json
{ "query": "What is RAG?" }
```
Response model:  
```json
{
  "answer": "...",
  "sources": [{"source":"file.pdf","page":1}],
  "relevant_chunks": [ { "text": "...", "source":"...", "page":1, "chunk_id":0, "score":0.1 } ]
}
```

### Metadata endpoint  
POST `/query/metadata`  
Returns the last retrieved chunk metadata:
```json
{ "metadata": [ { "source":"...", "page":1, "chunk_id":0, "score":0.1, "text":"..." } ] }
```

---

## 5. Testing

From project root:

- Run all tests  
  `pytest -q`

- Run only unit tests  
  `pytest tests/unit -q`

- Run only integration tests  
  `pytest tests/integration -q`

---

## 6. Configuration & LLM Providers

All settings live in `.env`. Key variables:

- `GEMINI_API_KEY` / `GEMINI_MODEL`  
- `EMBEDDING_MODEL` (e.g. `textembedding-gecko@001`)
- `CHUNK_SIZE`, `CHUNK_OVERLAP`, `MAX_DOCUMENTS`, `MAX_PAGES`

### Switching to another LLM (e.g. OpenAI)

1. Implement a new LLM class in `app/core/llm.py` (e.g. `OpenAILLM`) with a `generate_response(prompt, context)` method.
2. Update `QueryService.__init__` to choose your provider based on an env var (e.g. `LLM_PROVIDER=openai`).
3. Adjust `.env` and restart the service.

```python
# app/core/llm.py
class OpenAILLM:
    def __init__(self):
        import openai
        openai.api_key = settings.openai_api_key
    def generate_response(self, prompt, context):
        # call openai.ChatCompletion.create(...)
        ...
```

---

Enjoy building with RAG!// filepath: README.md

# RAG Pipeline

A complete Retrieval-Augmented Generation system using Google’s Gemini model (with ChromaDB and SQLModel).

---

## 1. Prerequisites

- Python 3.10+
- [Docker & Docker-Compose](https://docs.docker.com/)
- A Google API key with access to Gemini
- (Optional) A virtual environment tool (venv, conda, etc.)

## 2. Setup & Installation

1. Clone the repo  
   `git clone https://github.com/your_org/retrieval-augmented-generation.git`  
   `cd retrieval-augmented-generation`

2. Create & activate a venv  
   `python -m venv .venv`  
   Windows: `.venv\Scripts\activate`  
   Unix/macOS: `source .venv/bin/activate`

3. Install dependencies  
   `pip install -r requirements.txt`

4. Copy & configure environment  
   `cp .env.example .env`  
   Fill in your `GEMINI_API_KEY`, `GEMINI_MODEL`, etc.

5. Initialize the metadata database  
   `python -c "from app.main import on_startup; import asyncio; asyncio.run(on_startup())"`

## 3. Running the Service

### a) Locally with Uvicorn

```bash
export CHROMA_HOST=localhost
export CHROMA_PORT=8000
# ...other env vars
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

### b) Using Docker-Compose

```bash
docker-compose up --build
```

This will start:
- **ChromaDB** on port `8000`
- **RAG API** on port `8001`

---

## 4. API Usage

Base URL: `http://<host>:8001/api/v1`

### Health check  
GET  `/health/`  
Response:  
```json
{ "status": "healthy" }
```

### Upload documents  
POST `/documents/upload`  
Form-data: one or more files under key `files`  
```bash
curl -F "files=@./doc1.pdf" -F "files=@./notes.txt" \
  http://localhost:8001/api/v1/documents/upload
```

### Query endpoint  
POST `/query/query`  
Body (JSON):
```json
{ "query": "What is RAG?" }
```
Response model:  
```json
{
  "answer": "...",
  "sources": [{"source":"file.pdf","page":1}],
  "relevant_chunks": [ { "text": "...", "source":"...", "page":1, "chunk_id":0, "score":0.1 } ]
}
```

### Metadata endpoint  
POST `/query/metadata`  
Returns the last retrieved chunk metadata:
```json
{ "metadata": [ { "source":"...", "page":1, "chunk_id":0, "score":0.1, "text":"..." } ] }
```

---

## 5. Testing

From project root:

- Run all tests  
  `pytest -q`

- Run only unit tests  
  `pytest tests/unit -q`

- Run only integration tests  
  `pytest tests/integration -q`

---

## 6. Configuration & LLM Providers

All settings live in `.env`. Key variables:

- `GEMINI_API_KEY` / `GEMINI_MODEL`  
- `EMBEDDING_MODEL` (e.g. `textembedding-gecko@001`)
- `CHUNK_SIZE`, `CHUNK_OVERLAP`, `MAX_DOCUMENTS`, `MAX_PAGES`

### Switching to another LLM (e.g. OpenAI)

1. Implement a new LLM class in `app/core/llm.py` (e.g. `OpenAILLM`) with a `generate_response(prompt, context)` method.
2. Update `QueryService.__init__` to choose your provider based on an env var (e.g. `LLM_PROVIDER=openai`).
3. Adjust `.env` and restart the service.

```python
# app/core/llm.py
class OpenAILLM:
    def __init__(self):
        import openai
        openai.api_key = settings.openai_api_key
    def generate_response(self, prompt, context):
        # call openai.ChatCompletion.create(...)
        ...
```

---

Enjoy building with RAG!