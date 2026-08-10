"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Plus } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardTitle } from "@/components/ui/card";
import CandidateCard from "./candidate-card";
import { api, type Candidate } from "@/lib/api";

export default function CandidatesPage() {
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadCandidates() {
      setLoading(true);
      setError(null);
      try {
        const list = await api.listCandidates({ limit: 50, offset: 0 });
        setCandidates(list);
      } catch (e) {
        setError(e instanceof Error ? e.message : "Unable to load candidates.");
      } finally {
        setLoading(false);
      }
    }

    loadCandidates();
  }, []);

  function handleDelete(id: number) {
    setCandidates((prev) => prev.filter((candidate) => candidate.id !== id));
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
          <CandidateCard
            key={candidate.id}
            candidate={candidate}
            onDeleted={() => handleDelete(candidate.id)}
          />
        ))}
      </div>
    </div>
  );
}
