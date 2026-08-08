import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
        neon: {
          cyan: "#00e5ff",
          magenta: "#ff00e5",
          purple: "#b14aed",
          green: "#39ff14",
          amber: "#ffb800",
          red: "#ff1744",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      boxShadow: {
        "neon-cyan":
          "0 0 10px rgba(0,229,255,0.4), 0 0 30px rgba(0,229,255,0.2), 0 0 60px rgba(0,229,255,0.08)",
        "neon-cyan-sm":
          "0 0 5px rgba(0,229,255,0.3), 0 0 15px rgba(0,229,255,0.1)",
        "neon-magenta":
          "0 0 10px rgba(255,0,229,0.4), 0 0 30px rgba(255,0,229,0.2)",
        "neon-purple":
          "0 0 10px rgba(177,74,237,0.4), 0 0 30px rgba(177,74,237,0.2)",
        "neon-green":
          "0 0 10px rgba(57,255,20,0.4), 0 0 30px rgba(57,255,20,0.2)",
        "neon-red":
          "0 0 10px rgba(255,23,68,0.4), 0 0 30px rgba(255,23,68,0.2)",
      },
      animation: {
        "neon-pulse": "neon-pulse 3s ease-in-out infinite",
        float: "float 4s ease-in-out infinite",
        "gradient-shift": "gradient-shift 6s ease infinite",
        shimmer: "shimmer 3s linear infinite",
        "glow-line": "glow-line 3s ease-in-out infinite",
      },
      keyframes: {
        "neon-pulse": {
          "0%, 100%": { opacity: "1", filter: "brightness(1)" },
          "50%": { opacity: "0.85", filter: "brightness(1.15)" },
        },
        float: {
          "0%, 100%": { transform: "translateY(0)" },
          "50%": { transform: "translateY(-6px)" },
        },
        "gradient-shift": {
          "0%": { backgroundPosition: "0% 50%" },
          "50%": { backgroundPosition: "100% 50%" },
          "100%": { backgroundPosition: "0% 50%" },
        },
        shimmer: {
          "0%": { backgroundPosition: "-200% 0" },
          "100%": { backgroundPosition: "200% 0" },
        },
        "glow-line": {
          "0%": { transform: "translateX(-100%)" },
          "100%": { transform: "translateX(100%)" },
        },
      },
    },
  },
  plugins: [],
};
export default config;
