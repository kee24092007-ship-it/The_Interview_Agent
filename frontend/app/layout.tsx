import type { Metadata } from "next";
import Link from "next/link";
import { Inter } from "next/font/google";
import { Bot } from "lucide-react";

import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "AI Interview Agent",
  description: "Full-stack AI-powered interview management platform",
};

const navLinks = [
  { href: "/", label: "Dashboard" },
  { href: "/candidates", label: "Candidates" },
  { href: "/candidates/new", label: "Add Candidate" },
  { href: "/sessions", label: "Sessions" },
  { href: "/sessions/new", label: "New Session" },
];

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.className} min-h-screen bg-[#0a0a0f] text-[#e8e8ff] bg-grid`}>
        <header className="sticky top-0 z-50 border-b border-[rgba(0,229,255,0.08)] bg-[rgba(5,5,15,0.75)] backdrop-blur-xl">
          <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4">
            <Link href="/" className="group flex items-center gap-2.5 font-semibold">
              <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-[rgba(0,229,255,0.1)] transition-all duration-300 group-hover:bg-[rgba(0,229,255,0.2)] group-hover:shadow-neon-cyan-sm">
                <Bot className="h-5 w-5 text-neon-cyan" />
              </div>
              <span className="text-lg font-bold tracking-wide text-[#e8e8ff] transition-all duration-300 group-hover:text-neon-cyan group-hover:neon-text">
                AI Interview Agent
              </span>
            </Link>
            <nav className="flex items-center gap-0.5">
              {navLinks.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  className="relative rounded-lg px-3 py-2 text-sm font-medium text-[#8888aa] transition-all duration-300 hover:bg-[rgba(0,229,255,0.06)] hover:text-neon-cyan"
                >
                  {link.label}
                </Link>
              ))}
            </nav>
          </div>
          {/* Animated gradient line */}
          <div className="h-[1px] w-full overflow-hidden bg-[rgba(0,229,255,0.06)]">
            <div
              className="h-full w-1/3 animate-glow-line"
              style={{
                background: "linear-gradient(90deg, transparent, #00e5ff, #b14aed, #ff00e5, transparent)",
              }}
            />
          </div>
        </header>
        <main className="mx-auto max-w-6xl px-4 py-8">{children}</main>
      </body>
    </html>
  );
}
