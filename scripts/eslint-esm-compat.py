from pathlib import Path

Path("packages/eslint-config/next.mjs").write_text(
    'import nextVitalsModule from "eslint-config-next/core-web-vitals.js";\n\n'
    'const nextVitals = nextVitalsModule.default ?? nextVitalsModule;\n'
    'const nextConfig = Array.isArray(nextVitals) ? nextVitals : [nextVitals];\n\n'
    'export default nextConfig;\n',
    encoding="utf-8",
)

print("Next ESLint ESM export normalized.")
