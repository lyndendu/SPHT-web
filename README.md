# SPHT Platform

This repository is organized as a pnpm monorepo. The existing Next.js application is located in `apps/web`, while reusable UI, utility, validation, lint, and TypeScript configuration live in `packages`.

## Structure

```text
apps/
  web/                 Next.js application, API routes, auth, Prisma and assets
packages/
  ui/                  Reusable shadcn and Magic UI components and hooks
  utils/               Shared utility functions
  contracts/           Shared Zod schemas and contracts
  eslint-config/       Shared ESLint configuration
  tsconfig/            Shared TypeScript configuration
docs/
  legacy/              Original project documentation and npm lockfile
  superpowers/         Migration plans and implementation records
```

## Commands

```bash
corepack enable
pnpm install
pnpm dev
pnpm typecheck
pnpm lint
pnpm build
```

The web application runs at `http://localhost:3000`.

## Environment variables

The application retains its existing environment requirements, including:

```bash
DATABASE_URL=
NEXTAUTH_SECRET=
NEXTAUTH_URL=http://localhost:3000
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GITHUB_ID=
GITHUB_SECRET=
GITHUB_ACCESS_TOKEN=
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

The original README is preserved at [`docs/legacy/README-QuotesAI.md`](docs/legacy/README-QuotesAI.md).

## Database

The existing Prisma schema and migrations are preserved under `apps/web/prisma`. The datasource remains PostgreSQL as in the original repository.

## License

This project retains the original MIT license in [`License.md`](License.md).

## Aligned engineering foundation

- Node.js 24+ and pnpm 11.7.0
- Next.js 16, React 19, and TypeScript 5.9
- Tailwind CSS 4 with CSS-first configuration
- Zod 4 shared contracts
- Biome 2 for formatting, import organization, and baseline linting
- ESLint 9 for supplementary Next.js, React, Hooks, and accessibility checks
- React Compiler enabled

The existing Auth.js, Prisma/PostgreSQL, Stripe, API routes, Magic UI, and Framer Motion capabilities remain in place.
