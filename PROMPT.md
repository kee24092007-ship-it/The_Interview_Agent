Create a full-stack AI Interview Agent project with these exact specifications:

1. Backend (FastAPI):
   - Root directory: `backend`.
   - Structure: `backend/app/main.py`, `app/routers`, `app/models`, `app/schemas`, `app/config.py`.
   - Use `pydantic-settings` for environment variables (`.env`).
   - Database: SQLite (`interview_agent.db`) with SQLAlchemy ORM.
   - Models: Candidate, Session, Question, Answer, Evaluation.
   - API Routes: `/candidates`, `/sessions`, `/questions`, `/answers`, `/evaluations` with full CRUD.
   - Require `uvicorn`, `fastapi`, `python-dotenv`, `sqlalchemy`, `openai`, `pydantic-settings` in `requirements.txt`.
   - Include `seed.py` to create a default test candidate.
   - Include `CORS` middleware allowing `http://localhost:3000` and the production Vercel domain.

2. Frontend (Next.js 14):
   - Root directory: `frontend`.
   - TypeScript, Tailwind CSS, shadcn/ui components.
   - Pages: `/candidates`, `/candidates/new` (form), `/sessions/[id]` (individual session with AI-generated questions).
   - Create a `lib/api.ts` that reads from `NEXT_PUBLIC_API_BASE_URL`.

3. Deployment Configuration:
   - Provide a `render.yaml` configuration for the backend (FastAPI).
   - Provide a `vercel.json` and project settings for the frontend (Next.js).

4. Documentation:
   - Write a comprehensive README.md with setup steps, `.env` requirements, and how to run the backend and frontend simultaneously.
