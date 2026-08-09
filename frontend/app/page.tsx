import Link from "next/link";
import { ArrowRight, Bot, CalendarClock, Users } from "lucide-react";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { api } from "@/lib/api";

export const dynamic = "force-dynamic";

export default async function DashboardPage() {
  let candidates: Awaited<ReturnType<typeof api.listCandidates>> = [];
  let sessions: Awaited<ReturnType<typeof api.listSessions>> = [];
  try {
    [candidates, sessions] = await Promise.all([
      api.listCandidates(),
      api.listSessions(),
    ]);
  } catch {
    // Backend may be offline; the cards below will show zeros and a hint.
  }

  const completed = sessions.filter((s) => s.status === "completed").length;

  return (
    <div className="space-y-8">
      <div className="space-y-2">
        <h1
          className="text-4xl font-bold tracking-tight text-[#e8e8ff]"
          style={{
            textShadow:
              "0 0 20px rgba(0,229,255,0.5), 0 0 50px rgba(0,229,255,0.2)",
          }}
        >
          Dashboard
        </h1>
        <p className="text-[#7a7aaa]">
          Manage candidates, schedule AI interviews, and review evaluations.
        </p>
      </div>

      {/* Decorative gradient divider */}
      <div className="h-[1px] w-full bg-gradient-to-r from-transparent via-neon-cyan/30 to-transparent" />

      <div className="grid gap-6 sm:grid-cols-3">
        <Card className="group hover:shadow-neon-cyan hover:border-[rgba(0,229,255,0.25)] transition-all duration-500">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-[#7a7aaa]">
              Candidates
            </CardTitle>
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-[rgba(0,229,255,0.08)] transition-all duration-300 group-hover:bg-[rgba(0,229,255,0.15)]">
              <Users className="h-4 w-4 text-neon-cyan" />
            </div>
          </CardHeader>
          <CardContent>
            <div
              className="text-3xl font-bold text-neon-cyan"
              style={{ textShadow: "0 0 15px rgba(0,229,255,0.5)" }}
            >
              {candidates.length}
            </div>
            <p className="mt-1 text-xs text-[#555577]">registered candidates</p>
          </CardContent>
        </Card>

        <Card className="group hover:shadow-neon-magenta hover:border-[rgba(255,0,229,0.25)] transition-all duration-500">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-[#7a7aaa]">
              Sessions
            </CardTitle>
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-[rgba(255,0,229,0.08)] transition-all duration-300 group-hover:bg-[rgba(255,0,229,0.15)]">
              <CalendarClock className="h-4 w-4 text-neon-magenta" />
            </div>
          </CardHeader>
          <CardContent>
            <div
              className="text-3xl font-bold text-neon-magenta"
              style={{ textShadow: "0 0 15px rgba(255,0,229,0.5)" }}
            >
              {sessions.length}
            </div>
            <p className="mt-1 text-xs text-[#555577]">total interviews</p>
          </CardContent>
        </Card>

        <Card className="group hover:shadow-neon-green hover:border-[rgba(57,255,20,0.25)] transition-all duration-500">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-[#7a7aaa]">
              Completed
            </CardTitle>
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-[rgba(57,255,20,0.08)] transition-all duration-300 group-hover:bg-[rgba(57,255,20,0.15)]">
              <Bot className="h-4 w-4 text-neon-green" />
            </div>
          </CardHeader>
          <CardContent>
            <div
              className="text-3xl font-bold text-neon-green"
              style={{ textShadow: "0 0 15px rgba(57,255,20,0.5)" }}
            >
              {completed}
            </div>
            <p className="mt-1 text-xs text-[#555577]">finished interviews</p>
          </CardContent>
        </Card>
      </div>

      <Card className="neon-border overflow-hidden">
        <CardHeader>
          <CardTitle className="text-neon-cyan">Get started</CardTitle>
          
        </CardHeader>
        <CardContent className="flex flex-wrap gap-3">
          <Button asChild>
            <Link href="/candidates/new">
              Add a candidate <ArrowRight className="ml-1 h-4 w-4" />
            </Link>
          </Button>
          <Button asChild variant="outline">
            <Link href="/sessions/new">Schedule an interview</Link>
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
