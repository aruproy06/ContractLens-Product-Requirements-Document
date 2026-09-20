# ContractLens MVP

ContractLens turns contract text into a cited review workspace. This hackathon-ready MVP implements the P0 review path: document upload, clause segmentation, cited key-term extraction, deterministic date resolution, risk flags, obligations, deadline dashboard, version comparison, and grounded Q&A.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`. Upload a PDF, DOCX, or text document. For a no-install demo, use **Load demo contract**.

Useful API endpoints: `GET /api/health`, `GET /api/dashboard`, `POST /api/contracts/upload`, `POST /api/contracts/{id}/ask`, and `GET /api/contracts/{id}/audit-log`. Interactive OpenAPI documentation is available at `/docs`.

## Separate frontend (Next.js)

The `frontend/` application is the production-shaped React/TypeScript client for the same backend API. In a second terminal:

```powershell
cd frontend
Copy-Item .env.example .env.local
npm install
npm run dev
```

Open `http://localhost:3000`. It exposes the PRD's MVP dashboard, upload, source-linked terms and risks, obligation workflow, and grounded Q&A. The API allows this local frontend origin via CORS.

## Design guarantees

- Every extracted fact, risk, obligation, comparison, and answer includes a source citation.
- A citation quote is verified against its source clause before it is returned.
- Relative date calculations are deterministic Python code, never an LLM guess.
- Unsupported questions return “Not found in this document.”
- The UI consistently states that ContractLens is not legal advice.

This is a single-process demo store. Replace `InMemoryStore` with PostgreSQL/pgvector, enqueue `analyze_version` in a worker, and move files to encrypted object storage for production.
