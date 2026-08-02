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
    "apps/web/lib/auth.ts",
    '''import { PrismaAdapter } from "@auth/prisma-adapter";
import { nanoid } from "nanoid";
import NextAuth from "next-auth";
import Google from "next-auth/providers/google";

import { db } from "@/lib/db";

export const { handlers, auth, signIn, signOut } = NextAuth({
  adapter: PrismaAdapter(db),
  session: {
    strategy: "jwt",
  },
  pages: {
    signIn: "/login",
  },
  providers: [
    Google({
      clientId: process.env.GOOGLE_CLIENT_ID,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    }),
  ],
  callbacks: {
    async session({ token, session }) {
      if (session.user) {
        session.user.id = token.id;
        session.user.name = token.name;
        session.user.email = token.email;
        session.user.image = token.picture;
        session.user.username = token.username;
      }

      return session;
    },
    async jwt({ token, user }) {
      if (!token.email) {
        return token;
      }

      const dbUser = await db.user.findFirst({
        where: {
          email: token.email,
        },
      });

      if (!dbUser) {
        if (user) {
          token.id = user.id;
        }
        return token;
      }

      let username = dbUser.username;
      if (!username) {
        const updatedUser = await db.user.update({
          where: {
            id: dbUser.id,
          },
          data: {
            username: nanoid(10),
          },
        });
        username = updatedUser.username;
      }

      return {
        ...token,
        id: dbUser.id,
        name: dbUser.name,
        email: dbUser.email,
        picture: dbUser.image,
        username,
      };
    },
    authorized({ auth: session, request }) {
      const isAuthenticated = Boolean(session?.user);
      const pathname = request.nextUrl.pathname;
      const isAuthPage =
        pathname.startsWith("/login") || pathname.startsWith("/register");
      const isProtectedPage =
        pathname.startsWith("/dashboard") || pathname.startsWith("/editor");

      if (isAuthPage && isAuthenticated) {
        return Response.redirect(new URL("/dashboard", request.nextUrl));
      }

      if (isProtectedPage) {
        return isAuthenticated;
      }

      return true;
    },
  },
});
''',
)

write(
    "apps/web/lib/session.ts",
    '''import { auth } from "@/lib/auth";

export async function getCurrentUser() {
  const session = await auth();
  return session?.user;
}
''',
)

write(
    "apps/web/app/api/auth/[...nextauth]/route.ts",
    '''import { handlers } from "@/lib/auth";

export const { GET, POST } = handlers;
''',
)

write(
    "apps/web/proxy.ts",
    '''export { auth as proxy } from "@/lib/auth";

export const config = {
  matcher: ["/dashboard/:path*", "/editor/:path*", "/login", "/register"],
};
''',
)

write(
    "apps/web/components/user-auth-form.tsx",
    '''"use client";

import * as React from "react";
import { signIn } from "next-auth/react";

import { Icons } from "@/components/icons";
import { Button } from "@spht/ui/button";
import { useToast } from "@spht/ui/hooks/use-toast";
import { cn } from "@spht/utils";

interface UserAuthFormProps extends React.HTMLAttributes<HTMLDivElement> {}

export function UserAuthForm({ className, ...props }: UserAuthFormProps) {
  const [isLoading, setIsLoading] = React.useState(false);
  const { toast } = useToast();

  const loginWithGoogle = async () => {
    setIsLoading(true);

    try {
      await signIn("google", { redirectTo: "/dashboard" });
    } catch {
      toast({
        title: "There was a problem.",
        description: "There was an error logging in with Google.",
        variant: "destructive",
      });
      setIsLoading(false);
    }
  };

  return (
    <div className={cn("grid gap-6", className)} {...props}>
      <div className="relative">
        <div className="absolute inset-0 flex items-center">
          <span className="w-full border-t" />
        </div>
        <div className="relative flex justify-center text-xs uppercase">
          <span className="bg-background px-2 text-muted-foreground">
            continue with
          </span>
        </div>
      </div>
      <Button
        onClick={loginWithGoogle}
        variant="outline"
        type="button"
        disabled={isLoading}
      >
        {isLoading ? (
          <Icons.spinner className="mr-2 h-4 w-4 animate-spin" />
        ) : (
          <Icons.google className="mr-2 h-4 w-4" />
        )}{" "}
        Google
      </Button>
    </div>
  );
}
''',
)

write(
    "apps/web/app/(dashboard)/layout.tsx",
    '''import { notFound } from "next/navigation";

import { LoggedInNav } from "@/components/loggedin-nav";
import { ModeToggle } from "@/components/toggle";
import { SiteFooter } from "@/components/site-footer";
import { UserAccountNav } from "@/components/user-account-nav";
import { getCurrentUser } from "@/lib/session";

interface DashboardLayoutProps {
  children?: React.ReactNode;
}

export default async function DashboardLayout({
  children,
}: DashboardLayoutProps) {
  const user = await getCurrentUser();

  if (!user) {
    notFound();
  }

  return (
    <div className="flex min-h-screen flex-col space-y-6">
      <header className="sticky top-0 z-40 border-b bg-background">
        <div className="container flex h-16 items-center justify-between py-4">
          <LoggedInNav />
          <div className="mx-2 flex items-center gap-4">
            <ModeToggle />
            <UserAccountNav
              user={{
                name: user.name,
                image: user.image,
                email: user.email,
              }}
            />
          </div>
        </div>
      </header>
      <main className="flex w-full flex-1 flex-col justify-center">
        {children}
      </main>
      <SiteFooter className="border-t" />
    </div>
  );
}
''',
)

write(
    "packages/utils/tsconfig.json",
    '''{
  "extends": "@spht/tsconfig/base.json",
  "compilerOptions": {
    "types": ["node"]
  },
  "include": ["src/**/*.ts"]
}
''',
)

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
    "apps/web/eslint.config.mjs",
    '''import { defineConfig, globalIgnores } from "eslint/config";
import nextConfig from "@spht/eslint-config/next";

export default defineConfig([
  ...nextConfig,
  {
    rules: {
      "@typescript-eslint/no-unused-vars": "off",
    },
  },
  globalIgnores([".next/**", "out/**", "build/**", "next-env.d.ts"]),
]);
''',
)


def mutate_root(package: dict) -> None:
    package["packageManager"] = "pnpm@11.7.0"
    package["engines"] = {"node": ">=24"}


update_json("package.json", mutate_root)


def mutate_web(package: dict) -> None:
    dependencies = package["dependencies"]
    dependencies.pop("@next-auth/prisma-adapter", None)
    dependencies.pop("radix-ui", None)
    dependencies.pop("next-headers", None)
    package["scripts"]["lint"] = "eslint . --max-warnings=0"


update_json("apps/web/package.json", mutate_web)


def mutate_eslint_package(package: dict) -> None:
    package.setdefault("peerDependencies", {})["eslint"] = "^9.0.0"
    package.setdefault("peerDependencies", {})["typescript"] = ">=5.0.0 <6.1.0"


update_json("packages/eslint-config/package.json", mutate_eslint_package)

print("Modern framework compatibility fixes prepared.")
