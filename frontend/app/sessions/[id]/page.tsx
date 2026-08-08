import Link from "next/link";
import { ArrowLeft } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { api, type Question, type InterviewSession } from "@/lib/api";

import GenerateQuestions from "./generate-questions";

export const dynamic = "force-dynamic";

interface Props {
  params: { id: string };
}

export default async function SessionDetailPage({ params }: Props) {
  const sessionId = Number(params.id);
  let session: InterviewSession | null = null;
  let questions: Question[] = [];
  let error: string | null = null;

  try {
    session = await api.getSession(sessionId);
    questions = await api.listQuestionsForSession(sessionId);
  } catch (e) {
    error = e instanceof Error ? e.message : "Unable to load session.";
  }

  if (error && !session) {
    return (
      <div className="space-y-4">
        <Button asChild variant="outline" size="sm">
          <Link href="/sessions">
            <ArrowLeft className="mr-1 h-4 w-4" /> Back
          </Link>
        </Button>
        <Card>
          <CardContent className="py-10 text-destructive">{error}</CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <Button asChild variant="outline" size="icon">
          <Link href="/sessions">
            <ArrowLeft className="h-4 w-4" />
          </Link>
        </Button>
        <div className="flex-1">
          <h1 className="text-3xl font-bold tracking-tight">{session?.job_title}</h1>
          <p className="text-muted-foreground">Candidate #{session?.candidate_id}</p>
        </div>
        <Badge variant="secondary">{session?.status.replace("_", " ")}</Badge>
      </div>

      {session?.job_description && (
        <Card>
          <CardHeader>
            <CardTitle>Job description</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">{session.job_description}</p>
          </CardContent>
        </Card>
      )}

      <GenerateQuestions session={session} />

      <div className="space-y-3">
        <h2 className="text-xl font-semibold">Questions ({questions.length})</h2>
        {questions.length === 0 ? (
          <Card>
            <CardContent className="py-10 text-center text-muted-foreground">
              No questions yet. Generate a set with AI, or check back later.
            </CardContent>
          </Card>
        ) : (
          questions.map((q, index) => (
            <Card key={q.id}>
              <CardContent className="flex items-start justify-between gap-3 pt-6">
                <div className="flex gap-3">
                  <span className="text-sm font-semibold text-muted-foreground">{index + 1}.</span>
                  <p className="text-base font-medium">{q.content}</p>
                </div>
                <div className="flex shrink-0 gap-2">
                  <Badge variant="outline">{q.question_type}</Badge>
                  <Badge variant="secondary">{q.difficulty}</Badge>
                </div>
              </CardContent>
            </Card>
          ))
        )}
      </div>
    </div>
  );
}

