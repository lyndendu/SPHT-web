from __future__ import annotations

import json
from pathlib import Path


def write(path: str, content: str) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def update_json(path: str, mutate) -> None:
    target = Path(path)
    data = json.loads(target.read_text(encoding="utf-8"))
    mutate(data)
    target.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


write(
    "apps/web/app/(marketing)/hero/page.tsx",
    '''import { BentoDemo } from "@/components/bento-features";
import { Companies } from "@/components/social-proof";
import { buttonVariants } from "@spht/ui/button";
import BlurIn from "@spht/ui/magicui/blur-in";
import { BorderBeam } from "@spht/ui/magicui/border-beam";
import ShineBorder from "@spht/ui/magicui/shine-border";
import { cn } from "@spht/utils";
import Image from "next/image";
import Link from "next/link";

function HeroPage() {
  return (
    <>
      <section className="space-y-6 pb-8 pt-6 md:pb-12 md:pt-10 lg:py-20">
        <div className="container flex max-w-[64rem] flex-col items-center gap-4 text-center sm:mb-10 lg:mb-20">
          <ShineBorder
            className="absolute bg-muted px-4 py-1.5 text-center text-lg font-medium capitalize"
            color={["#A07CFE", "#FE8FB5", "#FFBE7B"]}
          >
            Introducing QuotesAI ✨
          </ShineBorder>

          <h1 className="mt-20 font-heading text-3xl sm:text-5xl md:text-6xl lg:text-7xl">
            Infusing Wisdom into Your Every Mood
          </h1>
          <p className="max-w-[42rem] leading-normal text-muted-foreground sm:text-xl sm:leading-8">
            Popular quotes for all categories from millions of books, people,
            and authors.
          </p>
          <div className="space-x-4">
            <Link href="/login" className={cn(buttonVariants({ size: "lg" }))}>
              Get Started
            </Link>
            <a
              href="/#features"
              className={cn(
                buttonVariants({ variant: "outline", size: "lg" }),
                "mt-sm-2",
              )}
            >
              Let&apos;s Explore 👇🏻
            </a>
          </div>
        </div>

        <div className="relative mx-auto aspect-[16/10] w-full max-w-[1000px] overflow-hidden rounded-xl border shadow-lg">
          <Image
            src="/darkoutput.png"
            alt="QuotesAI dashboard displayed in dark mode"
            fill
            priority
            sizes="(max-width: 1024px) 100vw, 1000px"
            className="hidden object-contain dark:block"
          />
          <Image
            src="/lightoutput.png"
            alt="QuotesAI dashboard displayed in light mode"
            fill
            priority
            sizes="(max-width: 1024px) 100vw, 1000px"
            className="object-contain dark:hidden"
          />
          <BorderBeam size={250} />
        </div>
      </section>

      <Companies />

      <section
        id="features"
        className="container space-y-6 bg-slate-50 py-8 dark:bg-transparent md:py-12 lg:py-10"
      >
        <div className="mx-auto flex max-w-[58rem] flex-col items-center space-y-4 text-center">
          <h3 className="pb-2 text-center text-sm font-semibold text-gray-500">
            FEATURES
          </h3>
        </div>
        <BentoDemo />
      </section>

      <section id="open-source" className="container py-8 md:py-12 lg:py-24">
        <div className="mx-auto flex max-w-[58rem] flex-col items-center justify-center gap-4 text-center">
          <h2 className="font-heading text-3xl leading-[1.1] sm:text-3xl md:text-6xl">
            QuotesAI - Unlock the Wisdom
          </h2>
          <p className="max-w-[85%] leading-normal text-muted-foreground sm:text-lg sm:leading-7">
            Let&apos;s try it now — {" "}
            <Link href="/login" className="underline underline-offset-4">
              Get Started
            </Link>
            .
          </p>
        </div>
      </section>
    </>
  );
}

export default HeroPage;
''',
)

write(
    "apps/web/components/bento-features.tsx",
    '''import { BentoCard, BentoGrid } from "@spht/ui/magicui/bento-grid";
import {
  BellIcon,
  BookmarkIcon,
  CopyIcon,
  GlobeIcon,
  InputIcon,
} from "@radix-ui/react-icons";

const decorativeBackground = (
  <div
    aria-hidden="true"
    className="absolute -right-20 -top-20 h-40 w-40 rounded-full bg-muted opacity-60 blur-3xl"
  />
);

const features = [
  {
    Icon: CopyIcon,
    name: "Share Your Favourite Quotes",
    description: "We allow you to copy your favourite quotes.",
    href: "/login",
    cta: "Learn more",
    background: decorativeBackground,
    className: "lg:row-start-1 lg:row-end-4 lg:col-start-2 lg:col-end-3",
  },
  {
    Icon: InputIcon,
    name: "Search for any Quotes",
    description: "Search through all your favourite books in one place.",
    href: "/login",
    cta: "Learn more",
    background: decorativeBackground,
    className: "lg:col-start-1 lg:col-end-2 lg:row-start-1 lg:row-end-3",
  },
  {
    Icon: GlobeIcon,
    name: "Multilingual",
    description: "Supports 100+ languages and counting.",
    href: "/login",
    cta: "Learn more",
    background: decorativeBackground,
    className: "lg:col-start-1 lg:col-end-2 lg:row-start-3 lg:row-end-4",
  },
  {
    Icon: BookmarkIcon,
    name: "Diverse source library",
    description: "Millions of words, infinite wisdom.",
    href: "/login",
    cta: "Learn more",
    background: decorativeBackground,
    className: "lg:col-start-3 lg:col-end-3 lg:row-start-1 lg:row-end-2",
  },
  {
    Icon: BellIcon,
    name: "Notifications",
    description: "Get notified every day with 10 new quotes in your inbox.",
    href: "/login",
    cta: "Learn more",
    background: decorativeBackground,
    className: "lg:col-start-3 lg:col-end-3 lg:row-start-2 lg:row-end-4",
  },
];

export function BentoDemo() {
  return (
    <BentoGrid className="lg:grid-rows-3">
      {features.map((feature) => (
        <BentoCard key={feature.name} {...feature} />
      ))}
    </BentoGrid>
  );
}
''',
)

write(
    "apps/web/components/social-proof.tsx",
    '''import Image from "next/image";

const companies = [
  "Google",
  "Microsoft",
  "Amazon",
  "Netflix",
  "YouTube",
  "Instagram",
  "Uber",
  "Spotify",
];

export function Companies() {
  return (
    <section id="companies">
      <div className="pb-10 pt-1">
        <div className="container mx-auto px-4 md:px-8">
          <h3 className="pb-2 text-center text-sm font-semibold text-gray-500">
            TRUSTED BY LEADING TEAMS
          </h3>
          <div className="relative mt-6">
            <div className="grid grid-cols-2 place-items-center gap-2 md:grid-cols-4 xl:grid-cols-8 xl:gap-4">
              {companies.map((company) => (
                <Image
                  key={company}
                  src={`https://cdn.magicui.design/companies/${company}.svg`}
                  width={160}
                  height={40}
                  sizes="160px"
                  className="h-10 w-40 object-contain px-2 dark:brightness-0 dark:invert"
                  alt={`${company} logo`}
                />
              ))}
            </div>
            <div className="pointer-events-none absolute inset-y-0 left-0 h-full w-1/3 bg-gradient-to-r from-white dark:from-black" />
            <div className="pointer-events-none absolute inset-y-0 right-0 h-full w-1/3 bg-gradient-to-l from-white dark:from-black" />
          </div>
        </div>
      </div>
    </section>
  );
}
''',
)

write(
    "apps/web/next.config.js",
    '''/** @type {import("next").NextConfig} */
const nextConfig = {
  transpilePackages: ["@spht/ui", "@spht/utils", "@spht/contracts"],
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "lh3.googleusercontent.com",
        pathname: "/**",
      },
      {
        protocol: "https",
        hostname: "cdn.magicui.design",
        pathname: "/companies/**",
      },
    ],
    dangerouslyAllowSVG: true,
    contentDispositionType: "attachment",
    contentSecurityPolicy: "default-src 'self'; script-src 'none'; sandbox;",
  },
};

module.exports = nextConfig;
''',
)

write(
    "apps/web/proxy.ts",
    '''import { withAuth, type NextRequestWithAuth } from "next-auth/middleware";
import { NextResponse } from "next/server";

export default withAuth(
  function proxy(request: NextRequestWithAuth) {
    const isAuthenticated = Boolean(request.nextauth.token);
    const pathname = request.nextUrl.pathname;
    const isAuthPage =
      pathname.startsWith("/login") || pathname.startsWith("/register");

    if (isAuthPage) {
      return isAuthenticated
        ? NextResponse.redirect(new URL("/dashboard", request.url))
        : NextResponse.next();
    }

    if (!isAuthenticated) {
      const from = `${pathname}${request.nextUrl.search}`;
      return NextResponse.redirect(
        new URL(`/login?from=${encodeURIComponent(from)}`, request.url),
      );
    }

    return NextResponse.next();
  },
  {
    callbacks: {
      authorized: () => true,
    },
  },
);

export const config = {
  matcher: ["/dashboard/:path*", "/editor/:path*", "/login", "/register"],
};
''',
)

middleware = Path("apps/web/middleware.ts")
if middleware.exists():
    middleware.unlink()

write(
    "packages/eslint-config/base.mjs",
    '''import js from "@eslint/js";
import tseslint from "typescript-eslint";

const baseConfig = [
  {
    ignores: ["dist/**", "node_modules/**", ".turbo/**"],
  },
  js.configs.recommended,
  {
    files: ["**/*.{ts,tsx}"],
    languageOptions: {
      parser: tseslint.parser,
      parserOptions: {
        ecmaVersion: "latest",
        sourceType: "module",
        ecmaFeatures: { jsx: true },
      },
    },
    rules: {
      "no-undef": "off",
      "no-unused-vars": "off",
    },
  },
];

export default baseConfig;
''',
)

write(
    "packages/eslint-config/next.mjs",
    '''import nextVitals from "eslint-config-next/core-web-vitals";

const nextConfig = [...nextVitals];

export default nextConfig;
''',
)

write(
    "apps/web/eslint.config.mjs",
    '''import { defineConfig, globalIgnores } from "eslint/config";
import nextConfig from "@spht/eslint-config/next";

export default defineConfig([
  ...nextConfig,
  globalIgnores([".next/**", "out/**", "build/**", "next-env.d.ts"]),
]);
''',
)

for package in ("ui", "contracts", "utils"):
    write(
        f"packages/{package}/eslint.config.mjs",
        '''import baseConfig from "@spht/eslint-config/base";

export default baseConfig;
''',
    )

for old_config in (
    "apps/web/.eslintrc.json",
    "packages/ui/.eslintrc.json",
    "packages/contracts/.eslintrc.json",
    "packages/utils/.eslintrc.json",
    "packages/eslint-config/index.js",
    "packages/eslint-config/next.js",
):
    path = Path(old_config)
    if path.exists():
        path.unlink()


def mutate_root(package: dict) -> None:
    package["engines"] = {"node": ">=24"}


update_json("package.json", mutate_root)


def mutate_web(package: dict) -> None:
    package["scripts"]["lint"] = "eslint . --max-warnings=0"
    package["dependencies"].pop("next-headers", None)


update_json("apps/web/package.json", mutate_web)


def mutate_shared(package: dict) -> None:
    package["scripts"]["lint"] = "eslint . --max-warnings=0"


for package_path in (
    "packages/ui/package.json",
    "packages/contracts/package.json",
    "packages/utils/package.json",
):
    update_json(package_path, mutate_shared)


def mutate_ui(package: dict) -> None:
    package["peerDependencies"] = {
        "react": ">=18.2.0 <20",
        "react-dom": ">=18.2.0 <20",
    }


update_json("packages/ui/package.json", mutate_ui)


def mutate_eslint_package(package: dict) -> None:
    package.pop("main", None)
    package["type"] = "module"
    package["exports"] = {
        "./base": "./base.mjs",
        "./next": "./next.mjs",
    }


update_json("packages/eslint-config/package.json", mutate_eslint_package)

write(
    ".devcontainer/devcontainer.json",
    json.dumps(
        {
            "name": "SPHT Platform",
            "image": "mcr.microsoft.com/devcontainers/typescript-node:1-24-bookworm",
            "postCreateCommand": "corepack enable && pnpm install",
            "forwardPorts": [3000],
        },
        indent=2,
    )
    + "\n",
)

print("Maintenance source and configuration fixes prepared.")
