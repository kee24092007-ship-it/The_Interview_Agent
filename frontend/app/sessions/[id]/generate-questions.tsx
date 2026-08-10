"use client";

import { useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { Loader2, Sparkles } from "lucide-react";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { api, type InterviewSession } from "@/lib/api";

const QUESTION_TYPE_OPTIONS = [
  { label: "Behavioral", value: "behavioral" },
  { label: "Technical", value: "technical" },
  { label: "Situational", value: "situational" },
  { label: "Strengths", value: "strengths" },
];

export default function GenerateQuestions({
  session,
  candidateSkills,
  existingCount,
}: {
  session: InterviewSession | null;
  candidateSkills?: string | null;
  existingCount?: number;
}) {
  const router = useRouter();
  const [count, setCount] = useState(8);
  const [questionTypes, setQuestionTypes] = useState<string[]>([
    "behavioral",
    "technical",
    "situational",
  ]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const buttonLabel = existingCount ? "Generate more questions" : "Generate questions";

  const selectedTypeLabels = useMemo(
    () => QUESTION_TYPE_OPTIONS.filter((option) => questionTypes.includes(option.value)).map((option) => option.label),
    [questionTypes],
  );

  if (!session) return null;

  function toggleQuestionType(type: string) {
    setQuestionTypes((prev) =>
      prev.includes(type) ? prev.filter((item) => item !== type) : [...prev, type],
    );
  }

  async function handleGenerate() {
    if (!session || questionTypes.length === 0) return;
    setLoading(true);
    setError(null);
    setSuccess(null);
    try {
      const generated = await api.generateQuestions(session.id, {
        job_title: session.job_title,
        job_description: session.job_description,
        candidate_skills: candidateSkills || null,
        count,
        question_types: questionTypes,
      });
      setSuccess(`Generated ${generated.length} question${generated.length === 1 ? "" : "s"}.`);
      router.refresh();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to generate questions.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Sparkles className="h-5 w-5 text-primary" /> AI Question Bank
        </CardTitle>
        <CardDescription>
          Create a tailored interview question set from the role details and candidate profile.
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid gap-4 md:grid-cols-3">
          <div className="space-y-2">
            <Label htmlFor="count">Number of questions</Label>
            <Input
              id="count"
              type="number"
              min={1}
              max={25}
              value={count}
              onChange={(e) => setCount(Number(e.target.value))}
            />
          </div>
          <div className="md:col-span-2 space-y-2">
            <Label>Question types</Label>
            <div className="grid gap-2 sm:grid-cols-2">
              {QUESTION_TYPE_OPTIONS.map((option) => (
                <label
                  key={option.value}
                  className="inline-flex cursor-pointer items-center rounded-lg border border-input bg-background px-3 py-2 text-sm transition hover:border-primary"
                >
                  <input
                    type="checkbox"
                    checked={questionTypes.includes(option.value)}
                    onChange={() => toggleQuestionType(option.value)}
                    className="mr-2 h-4 w-4 rounded border-input text-primary focus:ring-primary"
                  />
                  {option.label}
                </label>
              ))}
            </div>
          </div>
        </div>

        {candidateSkills && (
          <p className="text-sm text-muted-foreground">
            Candidate skills: <span className="font-medium">{candidateSkills}</span>
          </p>
        )}

        <div className="flex flex-wrap items-center gap-3">
          <Button onClick={handleGenerate} disabled={loading || questionTypes.length === 0}>
            {loading ? (
              <>
                <Loader2 className="mr-1 h-4 w-4 animate-spin" /> Generating...
              </>
            ) : (
              buttonLabel
            )}
          </Button>
          {selectedTypeLabels.length > 0 && (
            <p className="text-sm text-muted-foreground">
              Selected types: {selectedTypeLabels.join(", ")}
            </p>
          )}
        </div>

        {success && <p className="text-sm text-foreground/90">{success}</p>}
        {error && <p className="text-sm text-destructive">{error}</p>}
      </CardContent>
    </Card>
  );
}
