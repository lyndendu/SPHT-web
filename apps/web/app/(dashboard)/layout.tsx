import { notFound } from "next/navigation";

import { LoggedInNav } from "@/components/loggedin-nav";
import { SiteFooter } from "@/components/site-footer";
import { ModeToggle } from "@/components/toggle";
import { UserAccountNav } from "@/components/user-account-nav";
import { getCurrentUser } from "@/lib/session";

interface DashboardLayoutProps {
  children?: React.ReactNode;
}

export default async function DashboardLayout({ children }: DashboardLayoutProps) {
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
      <main className="flex w-full flex-1 flex-col justify-center">{children}</main>
      <SiteFooter className="border-t" />
    </div>
  );
}
