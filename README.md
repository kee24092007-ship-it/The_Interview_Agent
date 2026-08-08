# AI Interview Agent

A full-stack platform for AI-powered technical interviews. Manage candidates,
schedule interview sessions, generate tailored question banks with AI, collect
answers, and get AI evaluations.

## Tech Stack

| Layer     | Technology                                                       |
| --------- | ---------------------------------------------------------------- |
| Backend   | Python 3.11+, FastAPI, SQLAlchemy 2.x, Pydantic v2, SQLite (dev) |
| Frontend  | Next.js 14, TypeScript, Tailwind CSS, shadcn/ui                  |
| AI        | OpenAI-compatible chat API (falls back to local heuristics)      |

## Project Structure

```
.
├── backend/                 FastAPI application
│   ├── app/
│   │   ├── main.py          App entry point & router registration
│   │   ├── config.py        Settings (pydantic-settings, reads .env)
│   │   ├── database.py      SQLAlchemy engine / session / Base
│   │   ├── models/          ORM models (Candidate, InterviewSession,
│   │   │                    Question, Answer, Evaluation)
│   │   ├── schemas/         Pydantic request/response schemas + enums
│   │   ├── routers/         REST endpoints for each resource
│   │   └── services/ai.py   AI question generation & answer evaluation
│   ├── requirements.txt
│   ├── run.bat / run.sh     One-command dev server startup
│   └── .env.example         Backend env template
├── frontend/                Next.js application
│   ├── app/                 App Router pages (dashboard, candidates, sessions)
│   ├── components/ui/       shadcn/ui primitives (Button, Card, Input, ...)
│   ├── lib/api.ts           Typed client for the FastAPI backend
│   ├── lib/utils.ts         cn() classname helper
│   └── .env.local.example   Frontend env template
├── .env.example             Root API-key template (see below)
└── README.md
```

## Data Models

- **Candidate** – a person being interviewed (name, email, resume, skills, experience).
- **InterviewSession** – one interview run linking a `Candidate` to a `job_title`/`job_description`, with a status lifecycle (`scheduled → in_progress → completed`).
- **Question** – an interview question within a session (content, type, difficulty, ordering).
- **Answer** – a candidate's response to a question (text / transcript / audio reference).
- **Evaluation** – AI scoring and feedback at either the answer or session level.

## Prerequisites

- Python 3.11 or newer
- Node.js 18+ and npm

## Setup

### 1. Environment variables

Copy the templates and fill in your values:

```bash
cp .env.example backend/.env          # Windows: copy .env.example backend\.env
# Then set OPENAI_API_KEY inside backend/.env to enable live AI features.
```

The app runs with **no API key** using deterministic local fallbacks for question
generation and evaluation — useful for development and demos.

### 2. Backend

```bash
cd backend

# Windows
run.bat

# macOS / Linux
bash run.sh
```

Or manually:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- API docs (Swagger UI): http://localhost:8000/docs
- Health check: http://localhost:8000/health
- Optional sample data: `python -m app.seed`

### 3. Frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000

## API Endpoints (summary)

| Method | Endpoint                                  | Description                          |
| ------ | ----------------------------------------- | ------------------------------------ |
| GET    | `/candidates`                             | List candidates                      |
| POST   | `/candidates`                             | Create a candidate                   |
| POST   | `/sessions`                               | Create an interview session          |
| POST   | `/sessions/{id}/start`                    | Start a session                      |
| POST   | `/sessions/{id}/complete`                 | Complete a session                   |
| POST   | `/sessions/{id}/questions/generate`       | Generate & persist questions via AI  |
| GET    | `/questions/session/{id}`                 | List a session's questions           |
| POST   | `/answers`                                | Submit an answer                     |
| POST   | `/answers/{id}/evaluate`                  | Run AI evaluation on an answer       |
| GET    | `/evaluations/session/{id}`               | List a session's evaluations         |

## AI Features

- `POST /sessions/{id}/questions/generate` generates a JSON array of interview
  questions tailored to the role, job description and candidate skills.
- `POST /answers/{id}/evaluate` scores communication and technical quality and
  returns feedback, strengths and improvements.

Both call the OpenAI API when `OPENAI_API_KEY` is set, otherwise they fall back
to local heuristics so the whole pipeline works offline.

## License

Private / internal project.
