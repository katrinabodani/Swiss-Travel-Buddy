/** @type {import('next').NextConfig} */
const nextConfig = {
    async rewrites() {
      return [
        {
          source: "/ask",
          destination: "http://localhost:8000/ask", // FastAPI
        },
      ];
    },
  };
  
  module.exports = nextConfig;
  