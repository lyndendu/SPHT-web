# SPHT Web Monorepo Structure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert the existing Next.js repository into a pnpm monorepo where the current application lives in `apps/web` and reusable code lives in focused `packages`, without removing existing application behavior or assets.

**Architecture:** Keep Next.js pages, route handlers, authentication, middleware, Prisma, app-specific components, and public assets inside `apps/web`. Extract framework-compatible reusable UI primitives, animation primitives, generic React hooks, utility functions, validation contracts, and shared lint/TypeScript configuration into workspace packages. Use pnpm workspaces and Turborepo at the repository root.

**Tech Stack:** Next.js 14, React 18, TypeScript, Tailwind CSS, shadcn/ui, NextAuth, Prisma, PostgreSQL, pnpm workspaces, Turborepo.

## Global Constraints

- Apply changes directly to `main`, as explicitly requested by the repository owner.
- Do not delete application features, source content, database models, migrations, media assets, or configuration intent.
- Keep the Prisma datasource provider as `postgresql`; database migration is outside this structural refactor.
- Keep app-specific server code in `apps/web`.
- Move only genuinely reusable code to `packages`.
- Update every affected import, alias, Tailwind scan path, shadcn alias, build script, and workspace configuration.
- Use one atomic migration commit after this plan commit.
- Verify install, type checking, linting, and production build through CI before claiming success.

---

### Task 1: Establish workspace configuration

**Files:**
- Create: `package.json`
- Create: `pnpm-workspace.yaml`
- Create: `turbo.json`
- Create: `packages/tsconfig/base.json`
- Create: `packages/tsconfig/nextjs.json`
- Create: `packages/tsconfig/package.json`
- Create: `packages/eslint-config/index.js`
- Create: `packages/eslint-config/next.js`
- Create: `packages/eslint-config/package.json`

**Interfaces:**
- Produces workspace package names `@spht/tsconfig` and `@spht/eslint-config`.
- Root scripts delegate `dev`, `build`, `lint`, and `typecheck` through Turborepo.

- [ ] Add root workspace metadata and package-manager declaration.
- [ ] Define `apps/*` and `packages/*` workspaces.
- [ ] Define Turborepo tasks and cache outputs.
- [ ] Add reusable TypeScript and ESLint configurations.

### Task 2: Relocate the existing Next.js application

**Files:**
- Move existing application source and configuration to: `apps/web/**`
- Keep repository-level files at root: `.github/**`, `.gitignore`, `License.md`, `README.md`, workspace files, and `docs/**`.

**Interfaces:**
- Produces workspace package `@spht/web`.
- Preserves Next.js App Router routes, Pages API routes, authentication, middleware, Prisma schema/migrations, and all public assets.

- [ ] Move `app`, app-specific `components`, `pages`, `lib`, `types`, `prisma`, `public`, and application configuration into `apps/web`.
- [ ] Move binary assets by retaining their original Git blob contents.
- [ ] Create `apps/web/package.json` with the existing dependency set and workspace dependencies.
- [ ] Update `apps/web/tsconfig.json`, `.eslintrc.json`, `next.config.js`, `tailwind.config.ts`, and `components.json` for the new paths.

### Task 3: Extract reusable packages

**Files:**
- Create: `packages/ui/**`
- Create: `packages/utils/**`
- Create: `packages/contracts/**`

**Interfaces:**
- `@spht/ui/*` exports reusable UI and Magic UI components plus generic hooks.
- `@spht/utils` exports `cn`, `formatDate`, and `absoluteUrl`.
- `@spht/contracts/*` exports reusable Zod schemas.

- [ ] Move `components/ui/**` and `components/magicui/**` to `packages/ui/src/**`.
- [ ] Move generic hooks to `packages/ui/src/hooks/**`.
- [ ] Move `lib/utils.ts` to `packages/utils/src/index.ts`.
- [ ] Move reusable user and username Zod schemas to `packages/contracts/src/**`.
- [ ] Add package manifests, exports, and TypeScript configuration.
- [ ] Update all consuming imports in `apps/web` and inside packages.

### Task 4: Preserve app-specific boundaries

**Files:**
- Keep under `apps/web`: authentication, database client, session helpers, middleware, Prisma, navigation, account UI, auth form, marketing components, route code, and application types.

**Interfaces:**
- App code may consume packages.
- Packages must not import from `apps/web`.

- [ ] Confirm no shared package imports `@/` or any `apps/web` path.
- [ ] Confirm Next.js server-only modules remain in the app workspace.
- [ ] Confirm `next.config.js` transpiles workspace TypeScript packages.
- [ ] Confirm Tailwind scans shared UI sources.

### Task 5: Update automation and documentation

**Files:**
- Modify: `.codesandbox/tasks.json`
- Modify: `.devcontainer/devcontainer.json`
- Modify: `.github/dependabot.yml`
- Create: `.github/workflows/ci.yml`
- Modify: `README.md`

**Interfaces:**
- CI runs `pnpm install --frozen-lockfile`, `pnpm typecheck`, `pnpm lint`, and `pnpm build`.

- [ ] Point development tasks at root workspace scripts.
- [ ] Configure dependency updates for the workspace root.
- [ ] Document the final directory structure and commands.
- [ ] Add CI verification for pushes to `main`.

### Task 6: Verify the migration

**Files:**
- Inspect all changed files and the final Git tree.

**Interfaces:**
- Verification evidence is the CI workflow associated with the migration commit.

- [ ] Compare the pre-migration and post-migration commits to confirm all existing files are represented in the final tree.
- [ ] Confirm only intended root files remain outside `apps` and `packages`.
- [ ] Wait for CI and inspect failed job logs if any command fails.
- [ ] Fix structural failures and rerun verification before reporting completion.
