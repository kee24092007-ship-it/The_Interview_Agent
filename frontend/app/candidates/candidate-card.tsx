"use client";

import { useEffect, useState } from "react";
import { Trash2 } from "lucide-react";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { api, type Candidate } from "@/lib/api";

interface CandidateCardProps {
  candidate: Candidate;
  onDeleted?: () => void;
}

export default function CandidateCard({ candidate, onDeleted }: CandidateCardProps) {
  const [loading, setLoading] = useState(false);
  const [deleted, setDeleted] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!deleted || !onDeleted) return;
    const timer = window.setTimeout(() => onDeleted(), 1500);
    return () => window.clearTimeout(timer);
  }, [deleted, onDeleted]);

  async function handleDelete() {
    setLoading(true);
    setError(null);
    try {
      await api.deleteCandidate(candidate.id);
      setDeleted(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete candidate.");
    } finally {
      setLoading(false);
    }
  }

  if (deleted) {
    return (
      <Card className="border-neon-red/20 bg-[#111118]">
        <CardContent className="py-6 text-center text-sm text-neon-green">
          Candidate deleted successfully.
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="group hover:shadow-neon-cyan-sm hover:border-[rgba(0,229,255,0.2)] transition-all duration-300">
      <CardHeader>
        <div className="flex items-start justify-between gap-3">
          <div>
            <CardTitle className="group-hover:text-neon-cyan transition-colors duration-300">
              {candidate.full_name}
            </CardTitle>
            <CardDescription>{candidate.email}</CardDescription>
          </div>
          <Button
            type="button"
            variant="ghost"
            size="icon"
            aria-label="Delete candidate"
            onClick={handleDelete}
            disabled={loading}
            className="hover:bg-[rgba(255,23,68,0.1)] hover:text-neon-red"
          >
            <Trash2 className="h-4 w-4 text-neon-red/60 hover:text-neon-red transition-colors" />
          </Button>
        </div>
      </CardHeader>
      <CardContent className="space-y-3">
        <div className="flex flex-wrap gap-2">
          <span className="rounded-full border border-[#444] bg-[#0f1116] px-2 py-1 text-xs font-semibold text-[#a0a8d3]">
            {candidate.years_of_experience ?? 0} yrs exp
          </span>
          {candidate.skills &&
            candidate.skills
              .split(",")
              .slice(0, 4)
              .map((skill) => (
                <span
                  key={skill.trim()}
                  className="rounded-full border border-[#333] bg-[#0f1116] px-2 py-1 text-xs text-[#c5d0ff]"
                >
                  {skill.trim()}
                </span>
              ))}
        </div>
        {candidate.resume_text && (
          <p className="line-clamp-2 text-sm text-[#7a7aaa]">
            {candidate.resume_text}
          </p>
        )}
        {error && <p className="text-sm text-destructive">{error}</p>}
      </CardContent>
    </Card>
  );
}
