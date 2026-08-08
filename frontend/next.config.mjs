/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Allow calls to the FastAPI backend during SSR/build.
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/:path*`,
      },
    ];
  },
};

export default nextConfig;
