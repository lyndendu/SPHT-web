/** @type {import('next').NextConfig} */
const nextConfig = {
  transpilePackages: ['@spht/ui', '@spht/utils', '@spht/contracts'],
  images: {
    domains: ['lh3.googleusercontent.com'],
  },
}

module.exports = nextConfig
