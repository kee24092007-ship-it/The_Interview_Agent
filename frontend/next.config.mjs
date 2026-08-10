/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Proxy browser /api requests to the deployed FastAPI service.
  // NEXT_PUBLIC_API_URL can still override this for local/staging deployments.
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: `${process.env.NEXT_PUBLIC_API_URL || "https://the-interview-agent-dxin.onrender.com"}/:path*`,
      },
    ];
  },
};

export default nextConfig;
