/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/ask',
        destination: 'http://localhost:8000/ask',
      },
      {
        source: '/ask/image',
        destination: 'http://localhost:8000/ask/image',
      },
    ]
  },
}

module.exports = nextConfig
