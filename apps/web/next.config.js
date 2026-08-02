/** @type {import("next").NextConfig} */
const nextConfig = {
  transpilePackages: ["@spht/ui", "@spht/utils", "@spht/contracts"],
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "lh3.googleusercontent.com",
        pathname: "/**",
      },
      {
        protocol: "https",
        hostname: "cdn.magicui.design",
        pathname: "/companies/**",
      },
    ],
    dangerouslyAllowSVG: true,
    contentDispositionType: "attachment",
    contentSecurityPolicy: "default-src 'self'; script-src 'none'; sandbox;",
  },
};

module.exports = nextConfig;
