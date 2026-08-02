import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const resolve = (...parts) => path.join(root, ...parts);
const readJson = (file) => JSON.parse(fs.readFileSync(resolve(file), "utf8"));
const writeJson = (file, value) => {
  fs.mkdirSync(path.dirname(resolve(file)), { recursive: true });
  fs.writeFileSync(resolve(file), `${JSON.stringify(value, null, 2)}\n`);
};
const write = (file, content) => {
  fs.mkdirSync(path.dirname(resolve(file)), { recursive: true });
  fs.writeFileSync(resolve(file), content);
};

function replaceConfigDependency(pkg) {
  pkg.devDependencies ??= {};
  if (pkg.devDependencies["@spht/tsconfig"]) {
    delete pkg.devDependencies["@spht/tsconfig"];
  }
  pkg.devDependencies["@spht/typescript-config"] = "workspace:*";
  return pkg;
}

const rootPkg = readJson("package.json");
rootPkg.scripts = {
  ...rootPkg.scripts,
  format: "biome format --write .",
  check: "biome check .",
  "check:fix": "biome check --write .",
  prepare: "husky",
};
rootPkg.devDependencies = {
  ...rootPkg.devDependencies,
  "@biomejs/biome": "^2.5.6",
  husky: "^9.1.7",
  "lint-staged": "^16.4.0",
  typescript: "^5.9.3",
};
rootPkg["lint-staged"] = {
  "*.{js,jsx,ts,tsx,json,css,md}": ["biome check --write --no-errors-on-unmatched"],
};
writeJson("package.json", rootPkg);

const appPkg = replaceConfigDependency(readJson("apps/web/package.json"));
appPkg.scripts = {
  ...appPkg.scripts,
  format: "biome format --write .",
  check: "biome check .",
  "check:fix": "biome check --write .",
};
appPkg.dependencies = {
  ...appPkg.dependencies,
  "tailwind-merge": "^3.6.0",
  "tw-animate-css": "^1.4.0",
  zod: "^4.4.3",
};
appPkg.devDependencies = {
  ...appPkg.devDependencies,
  "@tailwindcss/postcss": "^4.3.3",
  "babel-plugin-react-compiler": "^1.0.0",
  tailwindcss: "^4.1.5",
};
delete appPkg.devDependencies.autoprefixer;
delete appPkg.dependencies["tailwindcss-animate"];
delete appPkg.devDependencies["tailwindcss-animate"];
writeJson("apps/web/package.json", appPkg);

const uiPkg = replaceConfigDependency(readJson("packages/ui/package.json"));
uiPkg.scripts = {
  ...uiPkg.scripts,
  format: "biome format --write src",
  check: "biome check src",
};
writeJson("packages/ui/package.json", uiPkg);

const contractsPkg = replaceConfigDependency(readJson("packages/contracts/package.json"));
contractsPkg.scripts = {
  ...contractsPkg.scripts,
  format: "biome format --write src",
  check: "biome check src",
};
contractsPkg.dependencies = {
  ...contractsPkg.dependencies,
  zod: "^4.4.3",
};
writeJson("packages/contracts/package.json", contractsPkg);

const utilsPkg = replaceConfigDependency(readJson("packages/utils/package.json"));
utilsPkg.scripts = {
  ...utilsPkg.scripts,
  format: "biome format --write src",
  check: "biome check src",
};
utilsPkg.dependencies = {
  ...utilsPkg.dependencies,
  "tailwind-merge": "^3.6.0",
};
writeJson("packages/utils/package.json", utilsPkg);

writeJson("packages/typescript-config/package.json", {
  name: "@spht/typescript-config",
  version: "0.1.0",
  private: true,
  files: ["base.json", "nextjs.json"],
});
writeJson("packages/typescript-config/base.json", {
  $schema: "https://json.schemastore.org/tsconfig",
  compilerOptions: {
    allowJs: true,
    esModuleInterop: true,
    forceConsistentCasingInFileNames: true,
    isolatedModules: true,
    lib: ["dom", "dom.iterable", "esnext"],
    module: "ESNext",
    moduleResolution: "Bundler",
    noEmit: true,
    resolveJsonModule: true,
    skipLibCheck: true,
    strict: true,
    target: "ES2020",
  },
});
writeJson("packages/typescript-config/nextjs.json", {
  $schema: "https://json.schemastore.org/tsconfig",
  extends: "./base.json",
  compilerOptions: {
    incremental: true,
    jsx: "preserve",
    plugins: [{ name: "next" }],
  },
});
fs.rmSync(resolve("packages/tsconfig"), { recursive: true, force: true });

for (const file of [
  "apps/web/tsconfig.json",
  "packages/ui/tsconfig.json",
  "packages/contracts/tsconfig.json",
  "packages/utils/tsconfig.json",
]) {
  const config = readJson(file);
  config.extends = config.extends.replace("@spht/tsconfig/", "@spht/typescript-config/");
  writeJson(file, config);
}

writeJson("packages/biome-config/package.json", {
  name: "@spht/biome-config",
  version: "0.1.0",
  private: true,
  files: ["biome.json"],
});
writeJson("packages/biome-config/biome.json", {
  $schema: "https://biomejs.dev/schemas/2.5.6/schema.json",
  formatter: {
    enabled: true,
    indentStyle: "space",
    indentWidth: 2,
    lineEnding: "lf",
    lineWidth: 120,
  },
  linter: {
    enabled: true,
    rules: { recommended: true },
  },
  assist: {
    enabled: true,
    actions: {
      source: { organizeImports: "on" },
    },
  },
});
writeJson("biome.json", {
  $schema: "https://biomejs.dev/schemas/2.5.6/schema.json",
  extends: ["./packages/biome-config/biome.json"],
  files: {
    ignoreUnknown: true,
    includes: ["**", "!**/.next", "!**/node_modules", "!docs/legacy/**"],
  },
});
write(".husky/pre-commit", "pnpm exec lint-staged\n");

write(
  "apps/web/postcss.config.js",
  `module.exports = {\n  plugins: {\n    "@tailwindcss/postcss": {},\n  },\n};\n`,
);

const oldCss = fs
  .readFileSync(resolve("apps/web/app/globals.css"), "utf8")
  .replace(/^@tailwind base;\s*@tailwind components;\s*@tailwind utilities;\s*/m, "")
  .trimStart();
const cssHeader = `@import "tailwindcss";\n@import "tw-animate-css";\n\n@source "../**/*.{js,ts,jsx,tsx,mdx}";\n@source "../../../packages/ui/src/**/*.{js,ts,jsx,tsx,mdx}";\n\n@custom-variant dark (&:is(.dark *));\n\n@theme inline {\n  --color-background: hsl(var(--background));\n  --color-foreground: hsl(var(--foreground));\n  --color-card: hsl(var(--card));\n  --color-card-foreground: hsl(var(--card-foreground));\n  --color-popover: hsl(var(--popover));\n  --color-popover-foreground: hsl(var(--popover-foreground));\n  --color-primary: hsl(var(--primary));\n  --color-primary-foreground: hsl(var(--primary-foreground));\n  --color-secondary: hsl(var(--secondary));\n  --color-secondary-foreground: hsl(var(--secondary-foreground));\n  --color-muted: hsl(var(--muted));\n  --color-muted-foreground: hsl(var(--muted-foreground));\n  --color-accent: hsl(var(--accent));\n  --color-accent-foreground: hsl(var(--accent-foreground));\n  --color-destructive: hsl(var(--destructive));\n  --color-destructive-foreground: hsl(var(--destructive-foreground));\n  --color-border: hsl(var(--border));\n  --color-input: hsl(var(--input));\n  --color-ring: hsl(var(--ring));\n  --radius-lg: var(--radius);\n  --radius-md: calc(var(--radius) - 2px);\n  --radius-sm: calc(var(--radius) - 4px);\n  --animate-accordion-down: accordion-down 0.2s ease-out;\n  --animate-accordion-up: accordion-up 0.2s ease-out;\n  --animate-meteor-effect: meteor 5s linear infinite;\n  --animate-border-beam: border-beam calc(var(--duration) * 1s) infinite linear;\n  --animate-shine-pulse: shine-pulse 2s ease-in-out infinite;\n}\n\n@utility container {\n  width: 100%;\n  margin-inline: auto;\n  padding-inline: 2rem;\n  @media (width >= 40rem) { max-width: 40rem; }\n  @media (width >= 48rem) { max-width: 48rem; }\n  @media (width >= 64rem) { max-width: 64rem; }\n  @media (width >= 80rem) { max-width: 80rem; }\n  @media (width >= 96rem) { max-width: 1400px; }\n}\n\n@keyframes shine-pulse {\n  0%, 100% { background-position: 0% 0%; }\n  50% { background-position: 100% 100%; }\n}\n\n@keyframes border-beam {\n  100% { offset-distance: 100%; }\n}\n\n@keyframes meteor {\n  0% { transform: rotate(215deg) translateX(0); opacity: 1; }\n  70% { opacity: 1; }\n  100% { transform: rotate(215deg) translateX(-500px); opacity: 0; }\n}\n\n@keyframes accordion-down {\n  from { height: 0; }\n  to { height: var(--radix-accordion-content-height); }\n}\n\n@keyframes accordion-up {\n  from { height: var(--radix-accordion-content-height); }\n  to { height: 0; }\n}\n\n`;
write("apps/web/app/globals.css", `${cssHeader}${oldCss}\n`);
fs.rmSync(resolve("apps/web/tailwind.config.ts"), { force: true });

const nextConfigPath = resolve("apps/web/next.config.js");
let nextConfig = fs.readFileSync(nextConfigPath, "utf8");
if (!nextConfig.includes("reactCompiler:")) {
  nextConfig = nextConfig.replace("const nextConfig = {", "const nextConfig = {\n  reactCompiler: true,");
}
fs.writeFileSync(nextConfigPath, nextConfig);

const turbo = readJson("turbo.json");
turbo.tasks.check = { dependsOn: ["^check"] };
turbo.tasks.format = { cache: false };
writeJson("turbo.json", turbo);

const ciPath = resolve(".github/workflows/ci.yml");
let ci = fs.readFileSync(ciPath, "utf8");
if (!ci.includes('HUSKY: "0"')) {
  ci = ci.replace("    env:\n", '    env:\n      HUSKY: "0"\n');
}
if (!ci.includes("- name: Generate Prisma Client")) {
  ci = ci.replace(
    "      - name: Type check\n        run: pnpm typecheck",
    "      - name: Generate Prisma Client\n        run: pnpm prisma:generate\n\n      - name: Type check\n        run: pnpm typecheck\n\n      - name: Biome check\n        run: pnpm check",
  );
}
fs.writeFileSync(ciPath, ci);

const readmePath = resolve("README.md");
let readme = fs.readFileSync(readmePath, "utf8");
const section = `\n## Aligned engineering foundation\n\n- Node.js 24+ and pnpm 11.7.0\n- Next.js 16, React 19, and TypeScript 5.9\n- Tailwind CSS 4 with CSS-first configuration\n- Zod 4 shared contracts\n- Biome 2 for formatting, import organization, and baseline linting\n- ESLint 9 for supplementary Next.js, React, Hooks, and accessibility checks\n- React Compiler enabled\n\nThe existing Auth.js, Prisma/PostgreSQL, Stripe, API routes, Magic UI, and Framer Motion capabilities remain in place.\n`;
if (!readme.includes("## Aligned engineering foundation")) {
  readme += section;
}
fs.writeFileSync(readmePath, readme);

console.log("Web stack alignment files prepared.");
