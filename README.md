# CareerPilot AI 🚀
A portfolio MVP for AI-powered career discovery: resume parsing, candidate profiles, semantic job search, explainable recommendations, RAG-style job context, and a conversational career agent.

## Stack
Python 3.11 · FastAPI · Streamlit · SQLAlchemy · SQLite · scikit-learn TF-IDF · optional Sentence Transformers · optional OpenAI tool calling · Docker.

## Run locally (Windows PowerShell)
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
uvicorn backend.main:app --reload --port 8000
```
Open a second terminal, activate `.venv`, then:
```powershell
streamlit run frontend/app.py
```
UI: http://localhost:8501 · API docs: http://localhost:8000/docs

## Optional AI setup
The app works without paid credentials using a local fallback agent and TF-IDF retrieval. To enable hosted LLM tool calling, put your key in `.env`:
```env
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4.1-mini
```
To use dense semantic embeddings:
```powershell
pip install sentence-transformers
```
Then set `USE_SENTENCE_TRANSFORMERS=true` in `.env`. First startup downloads the model; otherwise it falls back to TF-IDF.

## Docker
```bash
docker compose up --build
```
UI port 8501, API port 8000. Stop with `docker compose down`.

## Features
- PDF, DOCX and TXT resume text extraction and heuristic skill detection.
- Persistent profile, preferences and chat history in SQLite.
- Semantic-ish retrieval baseline with TF-IDF; optional dense embeddings.
- Explainable weighted recommendations: 55% retrieval, 30% skill overlap, 10% location, 5% work mode.
- Career assistant that retrieves relevant jobs and, with OpenAI configured, can call a `search_jobs` tool.
- Tiny Precision@5 / Recall@5 evaluation smoke test.
- FastAPI Swagger documentation.

## API
`GET /health`, `GET /jobs`, `GET /profile`, `PUT /profile`, `POST /resume/parse`, `POST /search`, `GET /recommendations`, `POST /chat`, `GET /chat/history`, `POST /evaluation/run`.

## Project structure
```text
backend/
  api/routes.py
  services/{agent,embeddings,evaluation,ranking,resume_parser}.py
  config.py database.py main.py models.py schemas.py seed.py
frontend/app.py
data/sample_jobs.json
tests/test_api.py
```

## Important limitations
The included listings are synthetic demo data, not live vacancies. Resume skill extraction is heuristic. Scanned-PDF OCR is not included. TF-IDF is a lexical baseline, not a dense semantic model. Optional LLM answers may be incorrect and must be checked. Evaluation uses a tiny hand-labelled demo set and is not evidence of production quality. This is a portfolio MVP, not a hiring decision system.

## Before publishing
Replace the GitHub URL if you add one, add your own screenshots, run tests, and never commit `.env`, API keys, resumes, or personal data. Be ready to explain each module and the trade-offs.

## Run tests
```powershell
python -m pytest -q
```
