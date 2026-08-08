"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

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
import { Textarea } from "@/components/ui/textarea";
import { api, type Candidate } from "@/lib/api";

export default function NewSessionPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [form, setForm] = useState({
    candidate_id: "",
    job_title: "",
    job_description: "",
  });

  useEffect(() => {
    api
      .listCandidates()
      .then(setCandidates)
      .catch((e) => setLoadError(e instanceof Error ? e.message : "Failed to load candidates."));
  }, []);

  function update(field: keyof typeof form, value: string) {
    setForm((prev) => ({ ...prev, [field]: value }));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const created = await api.createSession({
        candidate_id: Number(form.candidate_id),
        job_title: form.job_title,
        job_description: form.job_description || null,
        status: "scheduled",
      });
      router.push(`/sessions/${created.id}`);
      router.refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create session.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="mx-auto max-w-2xl space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">New Interview Session</h1>
        <p className="text-muted-foreground">Schedule an AI interview for a candidate.</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>Session details</CardTitle>
            <CardDescription>Choose a candidate and the target role.</CardDescription>
          </CardHeader>
          <CardContent className="grid gap-4">
            {loadError && <p className="text-sm text-destructive">{loadError}</p>}
            <div className="grid gap-2">
              <Label htmlFor="candidate_id">Candidate *</Label>
              <select
                id="candidate_id"
                required
                value={form.candidate_id}
                onChange={(e) => update("candidate_id", e.target.value)}
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
              >
                <option value="" disabled>
                  Select a candidate
                </option>
                {candidates.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.full_name} &lt;{c.email}&gt;
                  </option>
                ))}
              </select>
            </div>
            <div className="grid gap-2">
              <Label htmlFor="job_title">Job title *</Label>
              <Input
                id="job_title"
                required
                value={form.job_title}
                onChange={(e) => update("job_title", e.target.value)}
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="job_description">Job description</Label>
              <Textarea
                id="job_description"
                rows={4}
                value={form.job_description}
                onChange={(e) => update("job_description", e.target.value)}
              />
            </div>
          </CardContent>
        </Card>

        {error && <p className="text-sm text-destructive">{error}</p>}

        <div className="flex justify-end gap-3">
          <Button type="button" variant="outline" onClick={() => router.back()}>
            Cancel
          </Button>
          <Button type="submit" disabled={loading || candidates.length === 0}>
            {loading ? "Creating..." : "Create session"}
          </Button>
        </div>
      </form>
    </div>
  );
}
