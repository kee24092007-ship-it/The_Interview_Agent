"use client";

import { useState } from "react";
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
import { api } from "@/lib/api";

export default function NewCandidatePage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [form, setForm] = useState({
    full_name: "",
    email: "",
    phone: "",
    skills: "",
    years_of_experience: "",
    resume_text: "",
    notes: "",
  });

  function update(field: keyof typeof form, value: string) {
    setForm((prev) => ({ ...prev, [field]: value }));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const created = await api.createCandidate({
        full_name: form.full_name,
        email: form.email,
        phone: form.phone || null,
        skills: form.skills || null,
        years_of_experience: form.years_of_experience ? Number(form.years_of_experience) : null,
        resume_text: form.resume_text || null,
        notes: form.notes || null,
      });
      router.push(`/candidates`);
      router.refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create candidate.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="mx-auto max-w-2xl space-y-6">
      <div>
        <h1
          className="text-3xl font-bold tracking-tight text-[#e8e8ff]"
          style={{ textShadow: "0 0 20px rgba(0,229,255,0.5), 0 0 50px rgba(0,229,255,0.2)" }}
        >
          Add Candidate
        </h1>
        <p className="text-[#7a7aaa]">Register a new candidate for interviews.</p>
      </div>

      <div className="h-[1px] w-full bg-gradient-to-r from-transparent via-neon-purple/30 to-transparent" />

      <form onSubmit={handleSubmit} className="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>Profile</CardTitle>
            <CardDescription>Basic contact and background details.</CardDescription>
          </CardHeader>
          <CardContent className="grid gap-4">
            <div className="grid gap-2">
              <Label htmlFor="full_name">Full name *</Label>
              <Input
                id="full_name"
                required
                value={form.full_name}
                onChange={(e) => update("full_name", e.target.value)}
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="email">Email *</Label>
              <Input
                id="email"
                type="email"
                required
                value={form.email}
                onChange={(e) => update("email", e.target.value)}
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="grid gap-2">
                <Label htmlFor="phone">Phone</Label>
                <Input id="phone" value={form.phone} onChange={(e) => update("phone", e.target.value)} />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="years">Years of experience</Label>
                <Input
                  id="years"
                  type="number"
                  min={0}
                  step="0.5"
                  value={form.years_of_experience}
                  onChange={(e) => update("years_of_experience", e.target.value)}
                />
              </div>
            </div>
            <div className="grid gap-2">
              <Label htmlFor="skills">Skills (comma separated)</Label>
              <Input id="skills" value={form.skills} onChange={(e) => update("skills", e.target.value)} />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="resume_text">Resume / summary</Label>
              <Textarea
                id="resume_text"
                rows={4}
                value={form.resume_text}
                onChange={(e) => update("resume_text", e.target.value)}
              />
            </div>
          </CardContent>
        </Card>

        {error && <p className="text-sm text-neon-red" style={{ textShadow: "0 0 8px rgba(255,23,68,0.4)" }}>{error}</p>}

        <div className="flex justify-end gap-3">
          <Button type="button" variant="ghost" onClick={() => router.back()}>
            Cancel
          </Button>
          <Button type="submit" disabled={loading}>
            {loading ? "Saving..." : "Create candidate"}
          </Button>
        </div>
      </form>
    </div>
  );
}
