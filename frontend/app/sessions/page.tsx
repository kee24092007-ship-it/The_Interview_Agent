import Link from "next/link";
import { Plus } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import type { InterviewSession } from "@/lib/api";
import { api } from "@/lib/api";

export const dynamic = "force-dynamic";

const statusVariant: Record<
  string,
  "secondary" | "success" | "warning" | "destructive"
> = {
  scheduled: "secondary",
  in_progress: "warning",
  completed: "success",
  cancelled: "destructive",
};

export default async function SessionsPage() {
  let sessions: InterviewSession[] = [];
  let error: string | null = null;
  try {
    sessions = await api.listSessions({ limit: 50, offset: 0 });
  } catch (e) {
    error = e instanceof Error ? e.message : "Unable to load sessions.";
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">
            Interview Sessions
          </h1>
          <p className="text-muted-foreground">
            Scheduled and completed AI interviews.
          </p>
        </div>
        <Button asChild>
          <Link href="/sessions/new">
            <Plus className="mr-1 h-4 w-4" /> New session
          </Link>
        </Button>
      </div>

      {error && (
        <Card>
          <CardContent className="py-6 text-sm text-destructive">
            {error}
          </CardContent>
        </Card>
      )}

      {sessions.length === 0 && !error && (
        <Card>
          <CardContent className="py-16 text-center text-muted-foreground">
            No sessions yet. Schedule your first AI interview.
          </CardContent>
        </Card>
      )}

      <div className="grid gap-4 md:grid-cols-2">
        {sessions.map((session) => (
          <Link key={session.id} href={`/sessions/${session.id}`}>
            <Card className="transition-shadow hover:shadow-md">
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div>
                    <CardTitle>{session.job_title}</CardTitle>
                    <CardDescription>
                      {session.candidate_id ? `Candidate #${session.candidate_id}` : "Deleted candidate"}
                    </CardDescription>
                  </div>
                  <Badge variant={statusVariant[session.status] ?? "secondary"}>
                    {session.status.replace("_", " ")}
                  </Badge>
                </div>
              </CardHeader>
              <CardContent>
                <p className="line-clamp-2 text-sm text-muted-foreground">
                  {session.job_description ?? "No job description provided."}
                </p>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
