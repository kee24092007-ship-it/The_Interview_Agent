"use client";

import { useState } from "react";
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

export default function GenerateQuestions({ session }: { session: InterviewSession | null }) {
  const router = useRouter();
  const [count, setCount] = useState(8);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (!session) return null;

  async function handleGenerate() {
    if (!session) return;
    setLoading(true);
    setError(null);
    try {
      await api.generateQuestions(session.id, {
        job_title: session.job_title,
        job_description: session.job_description,
        count,
      });
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
          Generate a tailored set of interview questions using the AI.
        </CardDescription>
      </CardHeader>
      <CardContent className="flex flex-wrap items-end gap-4">
        <div className="w-40">
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
        <Button onClick={handleGenerate} disabled={loading}>
          {loading ? (
            <>
              <Loader2 className="mr-1 h-4 w-4 animate-spin" /> Generating...
            </>
          ) : (
            "Generate questions"
          )}
        </Button>
        {error && <p className="w-full text-sm text-destructive">{error}</p>}
      </CardContent>
    </Card>
  );
}
