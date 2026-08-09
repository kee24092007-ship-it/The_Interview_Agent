/**
 * Lightweight API client for the FastAPI backend.
 * Uses the NEXT_PUBLIC_API_URL env var if present, otherwise localhost:8000.
 */

export interface Candidate {
  id: number;
  full_name: string;
  email: string;
  phone: string | null;
  resume_text: string | null;
  skills: string | null;
  years_of_experience: number | null;
  notes: string | null;
  created_at: string;
}

export interface InterviewSession {
  id: number;
  candidate_id: number;
  job_title: string;
  job_description: string | null;
  status: "scheduled" | "in_progress" | "completed" | "cancelled";
  started_at: string | null;
  ended_at: string | null;
  created_at: string;
}

export interface Question {
  id: number;
  session_id: number;
  content: string;
  question_type: string;
  difficulty: string;
  order: number;
  created_at: string;
}

export interface Evaluation {
  id: number;
  session_id: number;
  answer_id: number | null;
  score: number;
  communication_score: number | null;
  technical_score: number | null;
  feedback: string | null;
  strengths: string | null;
  improvements: string | null;
  created_at: string;
}

const API_BASE =
  typeof window === "undefined"
    ? (process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, "") ??
      "http://localhost:8000")
    : "/api";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options?.headers ?? {}),
    },
    ...options,
  });
  if (!res.ok) {
    let detail = res.statusText;
    try {
      const body = await res.json();
      detail = body.detail ?? detail;
    } catch {
      // ignore non-JSON error bodies
    }
    throw new Error(
      typeof detail === "string" ? detail : JSON.stringify(detail),
    );
  }
  if (res.status === 204) return undefined as T;
  return res.json() as Promise<T>;
}

export const api = {
  // Candidates
  listCandidates: (params?: { limit?: number; offset?: number }) =>
    request<Candidate[]>(
      `/candidates${params ? `?limit=${params.limit ?? 50}&offset=${params.offset ?? 0}` : ""}`,
    ),
  getCandidate: (id: number) => request<Candidate>(`/candidates/${id}`),
  createCandidate: (data: Partial<Candidate>) =>
    request<Candidate>("/candidates", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  updateCandidate: (id: number, data: Partial<Candidate>) =>
    request<Candidate>(`/candidates/${id}`, {
      method: "PATCH",
      body: JSON.stringify(data),
    }),
  deleteCandidate: (id: number) =>
    request<void>(`/candidates/${id}`, { method: "DELETE" }),

  // Sessions
  listSessions: (params?: { limit?: number; offset?: number }) =>
    request<InterviewSession[]>(
      `/sessions${params ? `?limit=${params.limit ?? 50}&offset=${params.offset ?? 0}` : ""}`,
    ),
  getSession: (id: number) => request<InterviewSession>(`/sessions/${id}`),
  createSession: (data: Partial<InterviewSession>) =>
    request<InterviewSession>("/sessions", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  updateSession: (id: number, data: Partial<InterviewSession>) =>
    request<InterviewSession>(`/sessions/${id}`, {
      method: "PATCH",
      body: JSON.stringify(data),
    }),
  startSession: (id: number) =>
    request<InterviewSession>(`/sessions/${id}/start`, { method: "POST" }),
  completeSession: (id: number) =>
    request<InterviewSession>(`/sessions/${id}/complete`, { method: "POST" }),
  generateQuestions: (
    id: number,
    data: {
      job_title: string;
      job_description?: string | null;
      candidate_skills?: string | null;
      count?: number;
    },
  ) =>
    request<Question[]>(`/sessions/${id}/questions/generate`, {
      method: "POST",
      body: JSON.stringify(data),
    }),

  // Questions
  listQuestionsForSession: (
    id: number,
    params?: { limit?: number; offset?: number },
  ) =>
    request<Question[]>(
      `/questions/session/${id}${params ? `?limit=${params.limit ?? 50}&offset=${params.offset ?? 0}` : ""}`,
    ),
};
