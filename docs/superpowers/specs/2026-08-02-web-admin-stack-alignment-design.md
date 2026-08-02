# SPHT Web/Admin Stack Alignment Design

## Purpose

Align `lyndendu/SPHT-web` with the engineering foundation used by `lyndendu/SPHT-admin` without removing or weakening the web application's existing full-stack capabilities. After the web upgrade is stable, align the Admin repository's Node.js and pnpm versions with Web.

## Scope and order

The work is intentionally split into two sequential phases.

1. Upgrade `SPHT-web` and validate it completely.
2. Upgrade only the Node.js and pnpm runtime declarations in `SPHT-admin` after Phase 1 is merged and stable.

No Admin runtime change is allowed before the Web upgrade passes its production verification.

## Current shared foundation

Both applications already use:

- Next.js 16.2.12
- React 19.2.8
- TypeScript 5.9.3
- pnpm workspaces
- Turborepo
- workspace packages under `packages/*`

The principal differences are Tailwind CSS, Zod, lint/format tooling, shared configuration package names, React Compiler configuration, and runtime versions.

## Phase 1: SPHT-web alignment

### Goals

Bring the Web repository close to the Admin engineering baseline while preserving its role as the public website, customer portal, and full-stack service.

### Preserved capabilities

The following must remain functional and must not be replaced as part of this upgrade:

- Auth.js / NextAuth authentication
- Prisma Client and existing Prisma schema
- PostgreSQL datasource
- Stripe integration
- Next.js API routes and server-side functionality
- Existing public pages, customer pages, static assets, Magic UI components, and Framer Motion effects
- Existing package boundaries for `@spht/contracts`, `@spht/ui`, and `@spht/utils`

### Engineering changes

#### Tailwind CSS

Upgrade the Web application and shared UI package from Tailwind CSS 3 to Tailwind CSS 4.

The migration must:

- use the Tailwind 4 PostCSS integration;
- update the global CSS entry point to the Tailwind 4 import model;
- explicitly scan the Web application and shared UI package sources;
- preserve existing CSS variables, dark mode behavior, typography, animations, and responsive layouts;
- remove obsolete Tailwind 3 configuration only after equivalent Tailwind 4 behavior is verified.

#### Zod and shared contracts

Upgrade Zod from version 3 to version 4 across the Web workspace, including `@spht/contracts`.

The migration must:

- keep existing exported contract names and import paths stable;
- update APIs that are incompatible with Zod 4 without changing the intended validation behavior;
- verify all authentication, username, user, form, API, and server-side validation paths;
- avoid changing business validation rules.

#### Biome and code quality

Adopt Biome 2 as the primary formatter and baseline linter, matching Admin.

The required structure is:

- `packages/biome-config` for shared Biome defaults;
- root scripts for `format`, `check`, and `check:fix`;
- package-level `check` scripts where needed;
- Husky and lint-staged for changed JavaScript and TypeScript files.

ESLint remains as a supplementary check for Next.js, accessibility, React, and project-specific rules that Biome does not replace. Biome owns formatting, import organization, and baseline linting. ESLint must not format files or duplicate rules already enforced by Biome. No existing useful validation rule may be silently removed.

#### Shared TypeScript configuration

Replace the current shared TypeScript configuration package with the Admin-aligned naming and structure:

- `packages/typescript-config/base.json`
- `packages/typescript-config/nextjs.json`
- package name `@spht/typescript-config`

All current consumers of `@spht/tsconfig` must be updated to `@spht/typescript-config`. Existing TypeScript strictness must not be reduced. All application and shared packages must continue to pass `tsc --noEmit`.

#### React Compiler

Enable React Compiler in the Web Next.js configuration using the same supported configuration pattern as Admin.

Compiler-related dependency and configuration changes must not alter server/client component boundaries or force unnecessary `use client` directives.

#### Workspace commands

The root workspace must expose a consistent command surface:

```bash
pnpm dev
pnpm build
pnpm start
pnpm lint
pnpm format
pnpm check
pnpm typecheck
pnpm prisma:generate
```

`check` is the canonical Biome formatting and baseline lint command. `lint` runs the supplementary ESLint rules.

#### CI

The Web CI must continue to use Node.js 24 and pnpm 11.7.0 with a frozen lockfile.

The required verification order is:

```bash
pnpm install --frozen-lockfile
pnpm prisma:generate
pnpm typecheck
pnpm check
pnpm lint
pnpm build
```

### UI package boundary

This phase does not merge Web and Admin UI packages.

Web keeps its website-oriented components, Magic UI elements, and Framer Motion dependencies. Admin keeps its richer internal-operation component set. The upgrade aligns engineering foundations, not visual component inventories.

The Web packages `@spht/ui`, `@spht/contracts`, and `@spht/utils` keep their existing names. A future cross-repository design-system consolidation will be handled separately.

### Data and behavior safety

No Prisma migration is part of this phase. The PostgreSQL provider and current schema remain unchanged.

No authentication provider, callback, environment variable, Stripe endpoint, webhook behavior, or database model may be removed. Build-time CI variables remain test placeholders and must not be introduced into source code.

### Phase 1 acceptance criteria

Phase 1 is complete only when:

- the application installs with the committed pnpm lockfile;
- Prisma Client generation succeeds;
- all workspace TypeScript checks pass;
- Biome checks pass;
- supplementary ESLint checks pass with zero warnings;
- the Next.js production build succeeds;
- Tailwind styles compile from both `apps/web` and `packages/ui`;
- existing authentication, Prisma, Stripe, API, and public-page code still compiles;
- the changes are reviewed through a pull request and merged into `SPHT-web/main`.

## Phase 2: SPHT-admin runtime alignment

Phase 2 begins only after Phase 1 is merged.

### Changes

Upgrade Admin from:

- Node.js 22 to Node.js 24;
- pnpm 10.14.0 to pnpm 11.7.0.

Update all authoritative runtime declarations, including:

- root `package.json`;
- `pnpm-lock.yaml`;
- GitHub Actions workflow;
- README requirements;
- devcontainer, version files, or deployment files if present.

No Admin application dependency, UI component, business behavior, route, or feature is changed in Phase 2 unless required for Node 24 or pnpm 11 compatibility.

### Phase 2 acceptance criteria

```bash
pnpm install --frozen-lockfile
pnpm typecheck
pnpm build
pnpm --filter @spht/admin check
```

All commands must pass on Node.js 24 and pnpm 11.7.0 before merging into `SPHT-admin/main`.

## Implementation strategy

Each phase uses its own feature branch and pull request. The Web branch is implemented and merged first. The Admin branch is created from the latest Admin `main` only after the Web merge.

Upgrades must be made in small, reviewable commits grouped by concern:

1. shared configuration and scripts;
2. Tailwind 4 migration;
3. Zod 4 migration;
4. React Compiler and package updates;
5. formatting and compatibility fixes;
6. CI and documentation;
7. final verification.

## Exclusions

This design does not include:

- merging the two repositories;
- merging the two `@spht/ui` implementations;
- changing PostgreSQL to MySQL;
- introducing a new backend service;
- adding TanStack Query to Web;
- adding Prisma or authentication to Admin;
- redesigning pages;
- changing business requirements;
- upgrading Admin dependencies beyond Node/pnpm compatibility needs.

## Rollback

Both upgrades are isolated in pull requests. If a compatibility issue cannot be resolved without changing behavior, the affected upgrade remains unmerged. Existing `main` branches remain the rollback point.
