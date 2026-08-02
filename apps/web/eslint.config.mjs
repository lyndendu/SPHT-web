import { defineConfig, globalIgnores } from "eslint/config";
import nextConfig from "@spht/eslint-config/next";

export default defineConfig([
  ...nextConfig,
  {
    rules: {
      "@typescript-eslint/no-unused-vars": "off",
    },
  },
  globalIgnores([".next/**", "out/**", "build/**", "next-env.d.ts"]),
]);
