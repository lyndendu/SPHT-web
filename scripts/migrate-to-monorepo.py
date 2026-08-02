from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path.cwd()
WEB = ROOT / "apps/web"
UI = ROOT / "packages/ui/src"
UTILS = ROOT / "packages/utils/src"
CONTRACTS = ROOT / "packages/contracts/src"


def write(path: str | Path, content: str) -> None:
    target = ROOT / path if isinstance(path, str) else path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)


def write_json(path: str | Path, data: object) -> None:
    write(path, json.dumps(data, indent=2) + "\n")


def replace_in(path: Path, replacements: dict[str, str]) -> None:
    original = path.read_text()
    updated = original
    for old, new in replacements.items():
        updated = updated.replace(old, new)
    if updated != original:
        path.write_text(updated)


def move(source: str | Path, destination: str | Path) -> None:
    src = ROOT / source if isinstance(source, str) else source
    dst = ROOT / destination if isinstance(destination, str) else destination
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(dst))


# Preserve original documentation and npm lockfile verbatim.
(ROOT / "docs/legacy").mkdir(parents=True, exist_ok=True)
shutil.copy2(ROOT / "README.md", ROOT / "docs/legacy/README-QuotesAI.md")
shutil.copy2(ROOT / "package-lock.json", ROOT / "docs/legacy/package-lock.json")

# Create workspace directories.
for directory in [
    WEB,
    UI / "ui",
    UI / "magicui",
    UI / "hooks",
    UTILS,
    CONTRACTS,
    ROOT / "packages/tsconfig",
    ROOT / "packages/eslint-config",
]:
    directory.mkdir(parents=True, exist_ok=True)

# Move the Next.js application and app-owned configuration.
for name in ["app", "pages", "prisma", "public", "types"]:
    move(name, WEB / name)
for name in [
    "middleware.ts",
    "next.config.js",
    "postcss.config.js",
    "tailwind.config.ts",
    "components.json",
    ".eslintrc.json",
    "tsconfig.json",
]:
    move(name, WEB / name)

# Split app-specific components from reusable components.
app_components = WEB / "components"
app_components.mkdir(parents=True, exist_ok=True)
for child in list((ROOT / "components").iterdir()):
    if child.name not in {"ui", "magicui"}:
        move(child, app_components / child.name)
for child in list((ROOT / "components/ui").iterdir()):
    move(child, UI / "ui" / child.name)
for child in list((ROOT / "components/magicui").iterdir()):
    move(child, UI / "magicui" / child.name)
shutil.rmtree(ROOT / "components")

# Move generic React hooks into the UI package.
for child in list((ROOT / "hooks").iterdir()):
    move(child, UI / "hooks" / child.name)
shutil.rmtree(ROOT / "hooks")

# Split app server libraries from reusable utilities and contracts.
(WEB / "lib").mkdir(parents=True, exist_ok=True)
for name in ["auth.ts", "db.ts", "fonts.ts", "session.ts"]:
    move(ROOT / "lib" / name, WEB / "lib" / name)
move(ROOT / "lib/utils.ts", UTILS / "index.ts")
move(ROOT / "lib/validations/user.ts", CONTRACTS / "user.ts")
move(ROOT / "lib/validators/username.ts", CONTRACTS / "username.ts")
shutil.rmtree(ROOT / "lib")

# Preserve every original dependency in the web application package.
original_package = json.loads((ROOT / "package.json").read_text())
web_package = dict(original_package)
web_package["name"] = "@spht/web"
web_package["scripts"] = {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "typecheck": "tsc --noEmit",
    "prisma:generate": "prisma generate",
    "postinstall": "prisma generate",
}
web_package["dependencies"] = {
    "@spht/contracts": "workspace:*",
    "@spht/ui": "workspace:*",
    "@spht/utils": "workspace:*",
    **original_package.get("dependencies", {}),
}
web_package["devDependencies"] = {
    "@spht/eslint-config": "workspace:*",
    "@spht/tsconfig": "workspace:*",
    **original_package.get("devDependencies", {}),
}
write_json(WEB / "package.json", web_package)
(ROOT / "package-lock.json").unlink()

write_json(
    "package.json",
    {
        "name": "spht-platform",
        "version": "0.1.0",
        "private": True,
        "packageManager": "pnpm@9.15.4",
        "scripts": {
            "dev": "turbo dev --filter=@spht/web",
            "build": "turbo build",
            "start": "pnpm --filter @spht/web start",
            "lint": "turbo lint",
            "typecheck": "turbo typecheck",
            "prisma:generate": "pnpm --filter @spht/web prisma:generate",
        },
        "devDependencies": {"turbo": "^2.5.5"},
    },
)
write("pnpm-workspace.yaml", "packages:\n  - 'apps/*'\n  - 'packages/*'\n")
write_json(
    "turbo.json",
    {
        "$schema": "https://turbo.build/schema.json",
        "tasks": {
            "dev": {"cache": False, "persistent": True},
            "build": {
                "dependsOn": ["^build"],
                "outputs": [".next/**", "!.next/cache/**", "dist/**"],
            },
            "start": {"cache": False, "persistent": True},
            "lint": {"dependsOn": ["^lint"]},
            "typecheck": {"dependsOn": ["^typecheck"]},
        },
    },
)

# Shared TypeScript configuration.
write_json(
    "packages/tsconfig/package.json",
    {
        "name": "@spht/tsconfig",
        "version": "0.1.0",
        "private": True,
        "files": ["base.json", "nextjs.json"],
    },
)
write_json(
    "packages/tsconfig/base.json",
    {
        "$schema": "https://json.schemastore.org/tsconfig",
        "compilerOptions": {
            "target": "ES2020",
            "lib": ["dom", "dom.iterable", "esnext"],
            "allowJs": True,
            "skipLibCheck": True,
            "strict": True,
            "noEmit": True,
            "esModuleInterop": True,
            "module": "esnext",
            "moduleResolution": "bundler",
            "resolveJsonModule": True,
            "isolatedModules": True,
            "forceConsistentCasingInFileNames": True,
        },
    },
)
write_json(
    "packages/tsconfig/nextjs.json",
    {
        "$schema": "https://json.schemastore.org/tsconfig",
        "extends": "./base.json",
        "compilerOptions": {
            "jsx": "preserve",
            "incremental": True,
            "plugins": [{"name": "next"}],
        },
    },
)

# Shared ESLint configuration.
write_json(
    "packages/eslint-config/package.json",
    {
        "name": "@spht/eslint-config",
        "version": "0.1.0",
        "private": True,
        "main": "index.js",
        "exports": {".": "./index.js", "./next": "./next.js"},
        "peerDependencies": {
            "eslint": "^8.57.0",
            "eslint-config-next": "14.0.4",
        },
    },
)
write("packages/eslint-config/index.js", "module.exports = {\n  extends: ['eslint:recommended'],\n}\n")
write("packages/eslint-config/next.js", "module.exports = {\n  extends: ['next/core-web-vitals'],\n}\n")

# Reusable packages.
write_json(
    "packages/utils/package.json",
    {
        "name": "@spht/utils",
        "version": "0.1.0",
        "private": True,
        "sideEffects": False,
        "exports": {".": "./src/index.ts"},
        "scripts": {
            "lint": "eslint src --ext .ts",
            "typecheck": "tsc --noEmit",
        },
        "dependencies": {"clsx": "^2.1.0", "tailwind-merge": "^2.2.1"},
        "devDependencies": {
            "@spht/eslint-config": "workspace:*",
            "@spht/tsconfig": "workspace:*",
            "@types/node": "^20.11.24",
            "eslint": "^8.57.0",
            "typescript": "^5.3.3",
        },
    },
)
write_json(
    "packages/utils/tsconfig.json",
    {"extends": "@spht/tsconfig/base.json", "include": ["src/**/*.ts"]},
)
write_json(
    "packages/utils/.eslintrc.json",
    {"root": True, "extends": ["@spht/eslint-config"]},
)

write_json(
    "packages/contracts/package.json",
    {
        "name": "@spht/contracts",
        "version": "0.1.0",
        "private": True,
        "sideEffects": False,
        "exports": {
            ".": "./src/index.ts",
            "./user": "./src/user.ts",
            "./username": "./src/username.ts",
        },
        "scripts": {
            "lint": "eslint src --ext .ts",
            "typecheck": "tsc --noEmit",
        },
        "dependencies": {"zod": "^3.22.4"},
        "devDependencies": {
            "@spht/eslint-config": "workspace:*",
            "@spht/tsconfig": "workspace:*",
            "eslint": "^8.57.0",
            "typescript": "^5.3.3",
        },
    },
)
write_json(
    "packages/contracts/tsconfig.json",
    {"extends": "@spht/tsconfig/base.json", "include": ["src/**/*.ts"]},
)
write_json(
    "packages/contracts/.eslintrc.json",
    {"root": True, "extends": ["@spht/eslint-config"]},
)
write(
    CONTRACTS / "index.ts",
    "export { userNameSchema } from './user'\nexport { UsernameValidator } from './username'\n",
)

write_json(
    "packages/ui/package.json",
    {
        "name": "@spht/ui",
        "version": "0.1.0",
        "private": True,
        "sideEffects": False,
        "exports": {
            "./*": "./src/ui/*.tsx",
            "./magicui/*": "./src/magicui/*.tsx",
            "./hooks/*": "./src/hooks/*.ts",
        },
        "scripts": {
            "lint": "eslint src --ext .ts,.tsx",
            "typecheck": "tsc --noEmit",
        },
        "dependencies": {
            "@radix-ui/react-avatar": "^1.0.4",
            "@radix-ui/react-dialog": "^1.0.5",
            "@radix-ui/react-dropdown-menu": "^2.0.6",
            "@radix-ui/react-icons": "^1.3.0",
            "@radix-ui/react-label": "^2.0.2",
            "@radix-ui/react-navigation-menu": "^1.1.4",
            "@radix-ui/react-scroll-area": "^1.0.5",
            "@radix-ui/react-slot": "^1.0.2",
            "@radix-ui/react-toast": "^1.1.5",
            "@spht/utils": "workspace:*",
            "class-variance-authority": "^0.7.0",
            "framer-motion": "^11.0.8",
            "lucide-react": "^0.330.0",
            "vaul": "^0.9.0",
        },
        "peerDependencies": {"react": "^18.2.0", "react-dom": "^18.2.0"},
        "devDependencies": {
            "@spht/eslint-config": "workspace:*",
            "@spht/tsconfig": "workspace:*",
            "@types/react": "^18.2.61",
            "@types/react-dom": "^18.2.19",
            "eslint": "^8.57.0",
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "typescript": "^5.3.3",
        },
    },
)
write_json(
    "packages/ui/tsconfig.json",
    {
        "extends": "@spht/tsconfig/base.json",
        "compilerOptions": {"jsx": "preserve"},
        "include": ["src/**/*.ts", "src/**/*.tsx"],
    },
)
write_json(
    "packages/ui/.eslintrc.json",
    {"root": True, "extends": ["@spht/eslint-config"]},
)

# Update all consumers of moved shared code. Files are rewritten only when needed.
shared_replacements = {
    "@/lib/utils": "@spht/utils",
    "@/components/ui/": "@spht/ui/",
    "@/components/magicui/": "@spht/ui/magicui/",
    "@/hooks/": "@spht/ui/hooks/",
    "@/lib/validations/user": "@spht/contracts/user",
    "@/lib/validators/username": "@spht/contracts/username",
    "@/node_modules/next/link": "next/link",
}
for extension in ("*.ts", "*.tsx", "*.js"):
    for path in [*ROOT.glob(f"apps/web/**/{extension}"), *ROOT.glob(f"packages/**/{extension}")]:
        replace_in(path, shared_replacements)

# Correct package-internal and legacy relative imports.
relative_fixes = {
    UI / "magicui/bento-grid.tsx": {"@spht/ui/button": "../ui/button"},
    UI / "hooks/use-toast.ts": {"@spht/ui/toast": "../ui/toast"},
    UI / "ui/toaster.tsx": {
        "@spht/ui/toast": "./toast",
        "@spht/ui/hooks/use-toast": "../hooks/use-toast",
    },
    WEB / "components/main-nav.tsx": {"./ui/badge": "@spht/ui/badge"},
    WEB / "components/loggedin-nav.tsx": {"./ui/badge": "@spht/ui/badge"},
    WEB / "components/mobile-nav.tsx": {
        "./ui/button": "@spht/ui/button",
        "./ui/scroll-area": "@spht/ui/scroll-area",
    },
    WEB / "components/UserAvatar.tsx": {
        "../components/ui/avatar": "@spht/ui/avatar"
    },
}
for path, replacements in relative_fixes.items():
    replace_in(path, replacements)

# App workspace configuration.
write_json(
    WEB / "tsconfig.json",
    {
        "extends": "@spht/tsconfig/nextjs.json",
        "compilerOptions": {"baseUrl": ".", "paths": {"@/*": ["./*"]}},
        "include": [
            "next-env.d.ts",
            "**/*.ts",
            "**/*.tsx",
            ".next/types/**/*.ts",
            "pages/api/scrapper.js",
        ],
        "exclude": ["node_modules"],
    },
)
write_json(
    WEB / ".eslintrc.json",
    {"root": True, "extends": ["@spht/eslint-config/next"]},
)
write(
    WEB / "next.config.js",
    """/** @type {import('next').NextConfig} */
const nextConfig = {
  transpilePackages: ['@spht/ui', '@spht/utils', '@spht/contracts'],
  images: {
    domains: ['lh3.googleusercontent.com'],
  },
}

module.exports = nextConfig
""",
)

tailwind_path = WEB / "tailwind.config.ts"
tailwind = tailwind_path.read_text()
content_start = tailwind.index("  content: [")
content_end = tailwind.index("  ],", content_start) + len("  ],")
tailwind_content = """  content: [
    './app/**/*.{ts,tsx}',
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    '../../packages/ui/src/**/*.{ts,tsx}',
  ],"""
tailwind_path.write_text(
    tailwind[:content_start] + tailwind_content + tailwind[content_end:]
)

components_config = json.loads((WEB / "components.json").read_text())
components_config["tailwind"]["config"] = "tailwind.config.ts"
components_config["tailwind"]["css"] = "app/globals.css"
components_config["aliases"] = {
    "components": "@/components",
    "utils": "@spht/utils",
    "ui": "@spht/ui",
    "hooks": "@spht/ui/hooks",
}
write_json(WEB / "components.json", components_config)

# Repository tooling and final CI.
write(
    ".codesandbox/tasks.json",
    """{
  "setupTasks": [
    {"name": "Enable Corepack", "command": "corepack enable"},
    {"name": "Install Dependencies", "command": "pnpm install"}
  ],
  "tasks": {
    "dev": {"name": "dev", "command": "pnpm dev", "runAtStart": true},
    "build": {"name": "build", "command": "pnpm build"},
    "start": {"name": "start", "command": "pnpm start"},
    "lint": {"name": "lint", "command": "pnpm lint"},
    "typecheck": {"name": "typecheck", "command": "pnpm typecheck"}
  }
}
""",
)
write(
    ".devcontainer/devcontainer.json",
    """{
  "name": "SPHT Platform",
  "image": "mcr.microsoft.com/devcontainers/typescript-node:1-20-bullseye",
  "postCreateCommand": "corepack enable && pnpm install",
  "forwardPorts": [3000]
}
""",
)
write(
    ".github/dependabot.yml",
    """version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: weekly
  - package-ecosystem: "devcontainers"
    directory: "/"
    schedule:
      interval: weekly
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: weekly
""",
)
write(
    ".github/workflows/ci.yml",
    """name: CI

on:
  pull_request:
    branches:
      - main
  push:
    branches:
      - main

permissions:
  contents: read

jobs:
  verify:
    runs-on: ubuntu-latest
    env:
      DATABASE_URL: postgresql://postgres:postgres@localhost:5432/spht
      NEXTAUTH_SECRET: ci-secret
      NEXTAUTH_URL: http://localhost:3000
      NEXT_PUBLIC_APP_URL: http://localhost:3000
      GOOGLE_CLIENT_ID: ci-google-client
      GOOGLE_CLIENT_SECRET: ci-google-secret
      STRIPE_SECRET_KEY: sk_test_ci
      STRIPE_WEBHOOK_SECRET: whsec_ci
    steps:
      - name: Check out repository
        uses: actions/checkout@v4
      - name: Set up pnpm
        uses: pnpm/action-setup@v4
        with:
          version: 9.15.4
      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: pnpm
      - name: Install dependencies
        run: pnpm install --frozen-lockfile
      - name: Type check
        run: pnpm typecheck
      - name: Lint
        run: pnpm lint
      - name: Build
        run: pnpm build
""",
)
write(
    ".gitignore",
    """# dependencies
node_modules/
.pnp
.pnp.js
.yarn/install-state.gz

# testing
coverage/

# Next.js
.next/
out/

# production
build/
dist/

# Turborepo
.turbo/

# misc
.DS_Store
*.pem

# debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*

# environment files
.env
.env.*
!.env.example

# Vercel
.vercel/

# TypeScript
*.tsbuildinfo
next-env.d.ts
""",
)
write(
    "README.md",
    """# SPHT Platform

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
""",
)

print("Monorepo migration files prepared.")
