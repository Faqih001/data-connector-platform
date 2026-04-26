import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* Memory and performance optimizations */
  staticPageGenerationTimeout: 120,
  experimental: {
    optimizePackageImports: ["@tanstack/react-table"],
  },
  /* Build optimization */
  onDemandEntries: {
    maxInactiveAge: 60 * 1000,  // 1 minute
    pagesBufferLength: 2,       // Minimal buffer
  },
};

export default nextConfig;
