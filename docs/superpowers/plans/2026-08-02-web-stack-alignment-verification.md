# SPHT Web Stack Alignment Verification

The merged Web engineering foundation is verified through the permanent repository CI with Node.js 24 and pnpm 11.7.0.

```bash
pnpm install --frozen-lockfile
pnpm prisma:generate
pnpm typecheck
pnpm check
pnpm lint
pnpm build
```

The verification retains Auth.js, Prisma with the PostgreSQL datasource, Stripe, API routes, Magic UI, and Framer Motion.
