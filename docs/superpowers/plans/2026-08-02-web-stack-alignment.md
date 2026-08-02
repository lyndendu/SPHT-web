# SPHT Web Stack Alignment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Align `SPHT-web` with the `SPHT-admin` engineering foundation while preserving the Web application's authentication, Prisma/PostgreSQL, Stripe, API routes, public pages, Magic UI, and Framer Motion behavior.

**Architecture:** Keep the existing `apps/web` full-stack Next.js application and its domain packages intact. Replace only the shared engineering foundation: TypeScript configuration naming, Tailwind 4 integration, Zod 4, Biome, React Compiler, workspace scripts, hooks, and CI. ESLint remains a supplementary Next.js/React/accessibility check.

**Tech Stack:** Next.js 16.2.12, React 19.2.8, TypeScript 5.9.3, Tailwind CSS 4, Zod 4, Biome 2, ESLint 9, Prisma 5, Auth.js 5 beta, Stripe 15, pnpm 11.7.0, Turborepo 2.

## Global Constraints

- Keep Node.js at version 24 or newer and pnpm at exactly 11.7.0.
- Do not change the PostgreSQL provider or create a Prisma migration.
- Do not remove or replace Auth.js, Prisma, Stripe, API routes, environment-variable contracts, website pages, Magic UI, or Framer Motion.
- Keep package names `@spht/ui`, `@spht/contracts`, and `@spht/utils` unchanged.
- Rename `@spht/tsconfig` to `@spht/typescript-config` and update every consumer.
- Use Biome for formatting, import organization, and baseline linting.
- Keep ESLint for supplementary Next.js, React, React Hooks, and accessibility checks with zero warnings.
- Preserve existing CSS variables, dark mode behavior, custom animations, responsive layouts, and shared UI source scanning.
- Every commit must leave the branch in a reviewable state; final merge requires frozen-lockfile install, Prisma generation, typecheck, Biome, ESLint, and production build success.

---

## File Map

### Files created

- `packages/typescript-config/package.json` — shared TypeScript configuration package metadata.
- `packages/typescript-config/base.json` — strict workspace TypeScript defaults.
- `packages/typescript-config/nextjs.json` — Next.js compiler settings.
- `packages/biome-config/package.json` — shared Biome configuration package metadata.
- `packages/biome-config/biome.json` — shared formatting and baseline lint rules.
- `biome.json` — root Biome entry extending the shared configuration.
- `.husky/pre-commit` — changed-file quality gate.

### Files modified

- `package.json` — root scripts and engineering dependencies.
- `apps/web/package.json` — Tailwind 4, Zod 4, React Compiler, Biome/Husky integration, and package references.
- `packages/ui/package.json` — Zod/Tailwind-compatible UI dependency versions and config references.
- `packages/contracts/package.json` — Zod 4 and shared configuration references.
- `packages/utils/package.json` — shared configuration references.
- `apps/web/tsconfig.json` — new TypeScript config package reference.
- `packages/ui/tsconfig.json` — new TypeScript config package reference.
- `packages/contracts/tsconfig.json` — new TypeScript config package reference.
- `packages/utils/tsconfig.json` — new TypeScript config package reference.
- `apps/web/postcss.config.js` — Tailwind 4 PostCSS plugin.
- `apps/web/app/globals.css` — Tailwind 4 import, source scanning, theme tokens, and custom animations.
- `apps/web/next.config.js` — React Compiler and existing transpiled package configuration.
- `turbo.json` — `check` and `format` tasks.
- `.github/workflows/ci.yml` — final verification order.
- `pnpm-lock.yaml` — resolved dependency graph for pnpm 11.7.0.
- `README.md` — aligned commands and engineering requirements.

### Files removed after equivalent behavior is proven

- `apps/web/tailwind.config.ts` — Tailwind 3 configuration replaced by CSS-first Tailwind 4 configuration.
- `packages/tsconfig/package.json`
- `packages/tsconfig/base.json`
- `packages/tsconfig/nextjs.json`

---

### Task 1: Establish the implementation branch and record the baseline

**Files:**
- Modify: `docs/superpowers/plans/2026-08-02-web-stack-alignment.md`

**Interfaces:**
- Consumes: approved design in `docs/superpowers/specs/2026-08-02-web-admin-stack-alignment-design.md`.
- Produces: an isolated feature branch based on the latest `main` and a baseline verification record in the pull request.

- [ ] **Step 1: Create an isolated branch from the latest main**

```bash
git fetch origin main
git switch -c feat/align-web-admin-stack origin/main
```

- [ ] **Step 2: Install and verify the pre-upgrade baseline**

```bash
corepack enable
corepack prepare pnpm@11.7.0 --activate
pnpm install --frozen-lockfile
pnpm prisma:generate
pnpm typecheck
pnpm lint
pnpm build
```

Expected: every existing command passes before dependency or configuration changes are made.

- [ ] **Step 3: Record immutable safety checks**

```bash
grep -F 'provider = "postgresql"' apps/web/prisma/schema.prisma
grep -F 'next-auth' apps/web/package.json
grep -F 'stripe' apps/web/package.json
test -d apps/web/app/api
test -d packages/ui/src/magicui
```

Expected: all checks exit with status 0.

- [ ] **Step 4: Commit the implementation plan to the feature branch**

```bash
git add docs/superpowers/plans/2026-08-02-web-stack-alignment.md
git commit -m "docs: add Web stack alignment implementation plan"
```

---

### Task 2: Replace the shared TypeScript configuration package

**Files:**
- Create: `packages/typescript-config/package.json`
- Create: `packages/typescript-config/base.json`
- Create: `packages/typescript-config/nextjs.json`
- Modify: `apps/web/tsconfig.json`
- Modify: `packages/ui/tsconfig.json`
- Modify: `packages/contracts/tsconfig.json`
- Modify: `packages/utils/tsconfig.json`
- Modify: `apps/web/package.json`
- Modify: `packages/ui/package.json`
- Modify: `packages/contracts/package.json`
- Modify: `packages/utils/package.json`
- Remove: `packages/tsconfig/package.json`
- Remove: `packages/tsconfig/base.json`
- Remove: `packages/tsconfig/nextjs.json`

**Interfaces:**
- Consumes: current strict compiler settings from `packages/tsconfig`.
- Produces: package `@spht/typescript-config` exporting `base.json` and `nextjs.json`.

- [ ] **Step 1: Demonstrate the old package is still referenced**

```bash
grep -R '"@spht/tsconfig' apps packages --include='package.json' --include='tsconfig.json'
```

Expected: references are found in the application and shared packages.

- [ ] **Step 2: Create `packages/typescript-config/package.json`**

```json
{
  "name": "@spht/typescript-config",
  "version": "0.1.0",
  "private": true,
  "files": ["base.json", "nextjs.json"]
}
```

- [ ] **Step 3: Create strict shared compiler configurations**

`packages/typescript-config/base.json`:

```json
{
  "$schema": "https://json.schemastore.org/tsconfig",
  "compilerOptions": {
    "allowJs": true,
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "isolatedModules": true,
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "noEmit": true,
    "resolveJsonModule": true,
    "skipLibCheck": true,
    "strict": true,
    "target": "ES2020",
    "lib": ["dom", "dom.iterable", "esnext"]
  }
}
```

`packages/typescript-config/nextjs.json`:

```json
{
  "$schema": "https://json.schemastore.org/tsconfig",
  "extends": "./base.json",
  "compilerOptions": {
    "incremental": true,
    "jsx": "preserve",
    "plugins": [{ "name": "next" }]
  }
}
```

- [ ] **Step 4: Update every consumer**

Replace:

```text
@spht/tsconfig/base.json
@spht/tsconfig/nextjs.json
```

with:

```text
@spht/typescript-config/base.json
@spht/typescript-config/nextjs.json
```

Add `@spht/typescript-config: "workspace:*"` to the relevant package `devDependencies` and remove `@spht/tsconfig`.

- [ ] **Step 5: Remove the old package and verify no stale references remain**

```bash
rm -rf packages/tsconfig
! grep -R '@spht/tsconfig' apps packages --include='package.json' --include='tsconfig.json'
pnpm install
pnpm typecheck
```

Expected: no stale references; all TypeScript checks pass.

- [ ] **Step 6: Commit**

```bash
git add package.json pnpm-lock.yaml apps/web/package.json apps/web/tsconfig.json packages
git commit -m "refactor: align shared TypeScript configuration"
```

---

### Task 3: Introduce Biome while retaining supplementary ESLint

**Files:**
- Create: `packages/biome-config/package.json`
- Create: `packages/biome-config/biome.json`
- Create: `biome.json`
- Create: `.husky/pre-commit`
- Modify: `package.json`
- Modify: `apps/web/package.json`
- Modify: `packages/ui/package.json`
- Modify: `packages/contracts/package.json`
- Modify: `packages/utils/package.json`
- Modify: `turbo.json`

**Interfaces:**
- Consumes: existing ESLint flat configurations from `@spht/eslint-config`.
- Produces: `pnpm format`, `pnpm check`, and `pnpm check:fix`; ESLint remains available through `pnpm lint`.

- [ ] **Step 1: Verify the new commands do not exist yet**

```bash
! pnpm run | grep -E '^  (check|format|check:fix)'
```

Expected: command returns status 0 because the scripts are absent.

- [ ] **Step 2: Add the shared Biome configuration**

`packages/biome-config/package.json`:

```json
{
  "name": "@spht/biome-config",
  "version": "0.1.0",
  "private": true,
  "files": ["biome.json"]
}
```

`packages/biome-config/biome.json`:

```json
{
  "$schema": "https://biomejs.dev/schemas/2.5.6/schema.json",
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineEnding": "lf",
    "lineWidth": 120
  },
  "linter": {
    "enabled": true,
    "rules": { "preset": "recommended" }
  },
  "organizeImports": { "enabled": true }
}
```

`biome.json`:

```json
{
  "$schema": "https://biomejs.dev/schemas/2.5.6/schema.json",
  "extends": ["./packages/biome-config/biome.json"],
  "files": {
    "ignoreUnknown": true,
    "includes": ["**", "!**/.next", "!**/node_modules", "!docs/legacy"]
  }
}
```

- [ ] **Step 3: Add workspace scripts and dependencies**

Root `package.json` scripts:

```json
{
  "format": "biome format --write .",
  "check": "biome check .",
  "check:fix": "biome check --write .",
  "prepare": "husky"
}
```

Root development dependencies:

```json
{
  "@biomejs/biome": "^2.5.6",
  "husky": "^9.1.7",
  "lint-staged": "^16.4.0"
}
```

Root `lint-staged`:

```json
{
  "*.{js,jsx,ts,tsx,json,css,md}": ["biome check --write --no-errors-on-unmatched"]
}
```

- [ ] **Step 4: Configure the pre-commit hook**

`.husky/pre-commit`:

```sh
pnpm exec lint-staged
```

- [ ] **Step 5: Add Turbo tasks**

Add `check` and `format` tasks to `turbo.json`; `check` depends on `^check`, while `format` is uncached.

- [ ] **Step 6: Apply only safe automatic fixes**

```bash
pnpm install
pnpm check:fix
pnpm check
pnpm lint
pnpm typecheck
```

Expected: Biome, ESLint, and TypeScript all pass. If Biome reports a rule conflict with an intentional existing pattern, add a narrowly scoped configuration override rather than changing behavior.

- [ ] **Step 7: Commit**

```bash
git add package.json pnpm-lock.yaml turbo.json biome.json .husky packages apps/web/package.json
git commit -m "chore: adopt Biome workspace tooling"
```

---

### Task 4: Migrate the Web application from Tailwind 3 to Tailwind 4

**Files:**
- Modify: `apps/web/package.json`
- Modify: `apps/web/postcss.config.js`
- Modify: `apps/web/app/globals.css`
- Remove: `apps/web/tailwind.config.ts`
- Modify: `pnpm-lock.yaml`

**Interfaces:**
- Consumes: existing CSS variables, container settings, colors, radii, keyframes, animations, dark-mode selector, and `packages/ui/src` source path.
- Produces: Tailwind 4 CSS-first configuration with the same utility names used by existing pages and components.

- [ ] **Step 1: Capture utilities that must survive the migration**

```bash
grep -F 'border-border' apps/web/app/globals.css
grep -F 'bg-background' apps/web/app/globals.css
grep -F 'border-beam' apps/web/tailwind.config.ts
grep -F '../../packages/ui/src' apps/web/tailwind.config.ts
```

Expected: all four checks succeed.

- [ ] **Step 2: Upgrade Tailwind dependencies**

```bash
pnpm --filter @spht/web remove autoprefixer tailwindcss-animate
pnpm --filter @spht/web add -D tailwindcss@^4.1.5 @tailwindcss/postcss@^4.1.5
pnpm --filter @spht/web add tw-animate-css@^1.4.0
```

- [ ] **Step 3: Replace the PostCSS configuration**

`apps/web/postcss.config.js`:

```js
module.exports = {
  plugins: {
    "@tailwindcss/postcss": {},
  },
};
```

- [ ] **Step 4: Convert `globals.css` to Tailwind 4 CSS-first configuration**

The top of the file must contain:

```css
@import "tailwindcss";
@import "tw-animate-css";
@source "../**/*.{js,ts,jsx,tsx,mdx}";
@source "../../../packages/ui/src/**/*.{js,ts,jsx,tsx,mdx}";
@custom-variant dark (&:is(.dark *));
```

Add an `@theme inline` block mapping existing semantic utilities to the unchanged HSL variables, including `--color-background`, `--color-foreground`, `--color-border`, `--color-input`, `--color-ring`, primary, secondary, destructive, muted, accent, popover, and card values. Preserve the existing `:root`, `.dark`, radius variables, `@layer base`, mobile helper, and custom keyframes/animation names.

- [ ] **Step 5: Remove the Tailwind 3 config only after the CSS mappings exist**

```bash
rm apps/web/tailwind.config.ts
pnpm install
pnpm --filter @spht/web build
```

Expected: Next.js completes CSS compilation and generates the production routes without unknown utility errors.

- [ ] **Step 6: Verify shared UI scanning and semantic utility output**

```bash
test ! -f apps/web/tailwind.config.ts
grep -F '@source "../../../packages/ui/src' apps/web/app/globals.css
grep -F -- '--color-background' apps/web/app/globals.css
grep -F 'border-beam' apps/web/app/globals.css
pnpm typecheck
pnpm check
pnpm lint
```

- [ ] **Step 7: Commit**

```bash
git add apps/web/package.json apps/web/postcss.config.js apps/web/app/globals.css apps/web/tailwind.config.ts pnpm-lock.yaml
git commit -m "refactor: migrate Web styles to Tailwind CSS 4"
```

---

### Task 5: Upgrade Zod contracts from version 3 to version 4

**Files:**
- Modify: `apps/web/package.json`
- Modify: `packages/contracts/package.json`
- Modify: validation source files under `apps/web/**` and `packages/contracts/src/**` only when Zod 4 compilation requires it.
- Modify: `pnpm-lock.yaml`

**Interfaces:**
- Consumes: existing exports from `@spht/contracts`, including `./user` and `./username`.
- Produces: the same exported schemas and inferred types backed by Zod 4.4.3.

- [ ] **Step 1: Inventory existing Zod usage and exports**

```bash
grep -R "from \"zod\"\|from 'zod'" apps/web packages/contracts --include='*.ts' --include='*.tsx'
cat packages/contracts/src/index.ts
cat packages/contracts/src/user.ts
cat packages/contracts/src/username.ts
```

Expected: all validation entry points are listed before changing the dependency.

- [ ] **Step 2: Upgrade the workspace dependency**

```bash
pnpm --filter @spht/web add zod@^4.4.3
pnpm --filter @spht/contracts add zod@^4.4.3
pnpm install
```

- [ ] **Step 3: Run the compiler to expose real incompatibilities**

```bash
pnpm typecheck
```

Expected: either pass immediately or fail only at concrete Zod 4 API incompatibilities.

- [ ] **Step 4: Apply minimal compatibility changes**

Keep schema names, import paths, field constraints, error messages, and inferred type names unchanged. Do not loosen `.min`, `.max`, `.email`, `.regex`, `.optional`, `.nullable`, `.refine`, or object shape rules. Update only signatures rejected by Zod 4.

- [ ] **Step 5: Verify contracts and server code**

```bash
pnpm --filter @spht/contracts typecheck
pnpm --filter @spht/web typecheck
pnpm prisma:generate
pnpm build
```

Expected: contracts, authentication-related code, API routes, and production build pass.

- [ ] **Step 6: Commit**

```bash
git add apps/web/package.json packages/contracts package.json pnpm-lock.yaml apps/web
git commit -m "refactor: upgrade Web validation contracts to Zod 4"
```

---

### Task 6: Enable React Compiler and align Next.js package handling

**Files:**
- Modify: `apps/web/package.json`
- Modify: `apps/web/next.config.js`
- Modify: `pnpm-lock.yaml`

**Interfaces:**
- Consumes: existing `transpilePackages` and image security configuration.
- Produces: React Compiler enabled without changing server/client component boundaries.

- [ ] **Step 1: Verify React Compiler is not currently enabled**

```bash
! grep -F 'reactCompiler' apps/web/next.config.js
```

Expected: status 0.

- [ ] **Step 2: Add the compiler dependency**

```bash
pnpm --filter @spht/web add -D babel-plugin-react-compiler@^1.0.0
```

- [ ] **Step 3: Enable the compiler without removing existing settings**

Add to `nextConfig`:

```js
reactCompiler: true,
```

Keep `transpilePackages: ["@spht/ui", "@spht/utils", "@spht/contracts"]` and the existing `images` configuration unchanged.

- [ ] **Step 4: Verify component boundaries and build**

```bash
pnpm typecheck
pnpm lint
pnpm build
```

Expected: no new requirement to add `use client`; production build passes.

- [ ] **Step 5: Commit**

```bash
git add apps/web/package.json apps/web/next.config.js pnpm-lock.yaml
git commit -m "chore: enable React Compiler for Web"
```

---

### Task 7: Align workspace commands, CI, and documentation

**Files:**
- Modify: `package.json`
- Modify: `apps/web/package.json`
- Modify: `packages/ui/package.json`
- Modify: `packages/contracts/package.json`
- Modify: `packages/utils/package.json`
- Modify: `turbo.json`
- Modify: `.github/workflows/ci.yml`
- Modify: `README.md`
- Modify: `pnpm-lock.yaml`

**Interfaces:**
- Consumes: commands introduced in Tasks 2–6.
- Produces: stable root command surface and CI enforcement in the required order.

- [ ] **Step 1: Ensure package scripts expose their own checks**

Each workspace package must expose appropriate `typecheck`, `check`, and supplementary `lint` scripts. Packages without Next.js-specific rules may use Biome for `check` and keep their existing ESLint base rules for `lint`.

- [ ] **Step 2: Align root scripts**

The root must expose exactly these public commands:

```json
{
  "dev": "turbo dev --filter=@spht/web",
  "build": "turbo build",
  "start": "pnpm --filter @spht/web start",
  "lint": "turbo lint",
  "format": "biome format --write .",
  "check": "biome check .",
  "check:fix": "biome check --write .",
  "typecheck": "turbo typecheck",
  "prisma:generate": "pnpm --filter @spht/web prisma:generate",
  "prepare": "husky"
}
```

- [ ] **Step 3: Update CI verification order**

`.github/workflows/ci.yml` must run:

```yaml
- run: pnpm install --frozen-lockfile
- run: pnpm prisma:generate
- run: pnpm typecheck
- run: pnpm check
- run: pnpm lint
- run: pnpm build
```

Keep Node.js 24, Corepack pnpm 11.7.0, test-only environment variables, pnpm-store cache, Next.js cache, and telemetry disabling.

- [ ] **Step 4: Update README requirements and commands**

Document Node.js 24+, pnpm 11.7.0, Tailwind CSS 4, Zod 4, Biome primary checks, ESLint supplementary checks, and the unchanged PostgreSQL/Prisma/Auth.js/Stripe requirements.

- [ ] **Step 5: Run the complete local-equivalent verification**

```bash
pnpm install --frozen-lockfile
pnpm prisma:generate
pnpm typecheck
pnpm check
pnpm lint
pnpm build
```

Expected: all six commands pass in order.

- [ ] **Step 6: Re-run safety assertions**

```bash
grep -F 'provider = "postgresql"' apps/web/prisma/schema.prisma
grep -F 'next-auth' apps/web/package.json
grep -F 'stripe' apps/web/package.json
test -d apps/web/app/api
test -d packages/ui/src/magicui
```

Expected: all checks exit with status 0.

- [ ] **Step 7: Commit**

```bash
git add package.json apps packages turbo.json biome.json .husky .github/workflows/ci.yml README.md pnpm-lock.yaml
git commit -m "ci: enforce aligned Web engineering checks"
```

---

### Task 8: Pull-request verification and merge

**Files:**
- Modify only files required by concrete CI diagnostics.

**Interfaces:**
- Consumes: completed aligned Web branch.
- Produces: merged `SPHT-web/main` that satisfies every Phase 1 acceptance criterion.

- [ ] **Step 1: Push and open the implementation pull request**

```bash
git push -u origin feat/align-web-admin-stack
```

PR body must summarize preserved capabilities, engineering changes, dependency migrations, and the exact verification commands.

- [ ] **Step 2: Inspect every GitHub Actions step**

Expected successful steps:

```text
Install dependencies
Generate Prisma Client
Type check
Biome check
Supplementary ESLint
Production build
```

- [ ] **Step 3: Fix only concrete failures**

For each failure, retrieve the failed job log, make the smallest compatibility correction, run the relevant targeted command, then rerun the complete verification sequence before pushing.

- [ ] **Step 4: Review the final diff for prohibited changes**

```bash
git diff origin/main...HEAD -- apps/web/prisma apps/web/app/api
```

Expected: no Prisma schema migration, provider change, API deletion, authentication removal, or Stripe removal.

- [ ] **Step 5: Merge only after all checks are green**

Use a merge commit or squash according to repository policy. Record the merged commit SHA and CI run in the completion summary.

- [ ] **Step 6: Gate Phase 2**

Do not create the Admin runtime-upgrade branch until the Web merge is complete and the merged Web commit has a successful permanent CI result.
