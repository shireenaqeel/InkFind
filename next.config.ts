import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Mock tattoo images are served from picsum.photos for the scaffold.
  // Swap these for real CDN / S3 origins when wiring the actual catalog.
  images: {
    remotePatterns: [
      { protocol: "https", hostname: "picsum.photos" },
      { protocol: "https", hostname: "fastly.picsum.photos" },
    ],
  },
};

export default nextConfig;
