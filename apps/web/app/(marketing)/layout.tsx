import type { Metadata } from "next";
import Link from "next/link";
import { redirect } from "next/navigation";

import { MainNav } from "@/components/main-nav";
import MobileNav from "@/components/mobile-nav";
import { ModeToggle } from "@/components/toggle";
import { SiteFooter } from "@/components/site-footer";
import { getCurrentUser } from "@/lib/session";
import { buttonVariants } from "@spht/ui/button";
import { cn } from "@spht/utils";

export const metadata: Metadata = {
  title: "QuotesAI",
  description: "Popular quotes for every mood.",
};

export default async function MarketingLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const user = await getCurrentUser();

  if (user) {
    redirect("/dashboard");
  }

  return (
    <div className="flex min-h-screen flex-col">
      <header className="container sticky top-0 z-50 h-16 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="flex h-16 w-full items-center justify-between py-6">
          <MobileNav />
          <MainNav />
          <nav className="md:flex">
            <div className="flex gap-4">
              <ModeToggle />
              <Link
                href="/login"
                className={cn(
                  buttonVariants({ variant: "default", size: "sm" }),
                  "px-4",
                )}
              >
                Get Started
              </Link>
            </div>
          </nav>
        </div>
      </header>
      <main className="flex-1">{children}</main>
      <SiteFooter />
    </div>
  );
}
