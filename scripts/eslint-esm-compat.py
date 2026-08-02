from pathlib import Path

Path("packages/eslint-config/next.mjs").write_text(
    'import nextVitals from "eslint-config-next/core-web-vitals.js";\n\n'
    'const nextConfig = [...nextVitals];\n\n'
    'export default nextConfig;\n',
    encoding="utf-8",
)

print("Next ESLint ESM entrypoint updated.")
