/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Proxy browser /api requests to the same production FastAPI service used
  // by server-side rendering. Vercel should not inherit a stale
  // NEXT_PUBLIC_API_URL value that points at a different database/service.
  async rewrites() {
    const backendUrl = process.env.VERCEL
      ? "https://the-interview-agent-dxin.onrender.com"
      : process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

    return [
      {
        source: "/api/:path*",
        destination: `${backendUrl}/:path*`,
      },
    ];
  },
};

export default nextConfig;
