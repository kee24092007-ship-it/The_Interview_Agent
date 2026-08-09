import Link from "next/link";
import { Plus, Trash2 } from "lucide-react";
import { revalidatePath } from "next/cache";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { api, type Candidate } from "@/lib/api";

export const dynamic = "force-dynamic";

async function deleteCandidate(id: number) {
  "use server";
  await api.deleteCandidate(id);
  revalidatePath("/candidates");
}

export default async function CandidatesPage() {
  let candidates: Candidate[] = [];
  let error: string | null = null;
  try {
    candidates = await api.listCandidates({ limit: 50, offset: 0 });
  } catch (e) {
    error = e instanceof Error ? e.message : "Unable to load candidates.";
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1
            className="text-3xl font-bold tracking-tight text-[#e8e8ff]"
            style={{
              textShadow:
                "0 0 20px rgba(0,229,255,0.5), 0 0 50px rgba(0,229,255,0.2)",
            }}
          >
            Candidates
          </h1>
          <p className="text-[#7a7aaa]">People registered for interviews.</p>
        </div>
        <Button asChild>
          <Link href="/candidates/new">
            <Plus className="mr-1 h-4 w-4" /> Add candidate
          </Link>
        </Button>
      </div>

      <div className="h-[1px] w-full bg-gradient-to-r from-transparent via-neon-cyan/30 to-transparent" />

      {error && (
        <Card className="border-neon-red/30">
          <CardContent className="py-6 text-sm text-neon-red">
            {error}
          </CardContent>
        </Card>
      )}

      {candidates.length === 0 && !error && (
        <Card>
          <CardContent className="py-16 text-center text-[#555577]">
            No candidates yet. Add your first candidate to get started.
          </CardContent>
        </Card>
      )}

      <div className="grid gap-4 md:grid-cols-2">
        {candidates.map((candidate) => (
          <Card
            key={candidate.id}
            className="group hover:shadow-neon-cyan-sm hover:border-[rgba(0,229,255,0.2)] transition-all duration-300"
          >
            <CardHeader>
              <div className="flex items-start justify-between">
                <div>
                  <CardTitle className="group-hover:text-neon-cyan transition-colors duration-300">
                    {candidate.full_name}
                  </CardTitle>
                  <CardDescription>{candidate.email}</CardDescription>
                </div>
                <form action={deleteCandidate.bind(null, candidate.id)}>
                  <Button
                    type="submit"
                    variant="ghost"
                    size="icon"
                    aria-label="Delete candidate"
                    className="hover:bg-[rgba(255,23,68,0.1)] hover:text-neon-red"
                  >
                    <Trash2 className="h-4 w-4 text-neon-red/60 hover:text-neon-red transition-colors" />
                  </Button>
                </form>
              </div>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex flex-wrap gap-2">
                <Badge variant="secondary">
                  {candidate.years_of_experience ?? 0} yrs exp
                </Badge>
                {candidate.skills &&
                  candidate.skills
                    .split(",")
                    .slice(0, 4)
                    .map((skill) => (
                      <Badge key={skill.trim()} variant="outline">
                        {skill.trim()}
                      </Badge>
                    ))}
              </div>
              {candidate.resume_text && (
                <p className="line-clamp-2 text-sm text-[#7a7aaa]">
                  {candidate.resume_text}
                </p>
              )}
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
