"use client";

import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@spht/ui/sheet";
import { cn } from "@spht/utils";
import Link, { LinkProps } from "next/link";
import { useRouter } from "next/navigation";

import React from "react";
import { Icons } from "./icons";
import { Button } from "@spht/ui/button";
import { ScrollArea } from "@spht/ui/scroll-area";

function MobileNav() {
  const [open, setOpen] = React.useState(false);

  return (
    <MobileLink
    href="/"
    className="flex items-center lg:hidden sm:block md:hidden"
    onOpenChange={setOpen}
  >
    <Icons.logo className="mr-2 h-6 w-6" />
    <span className="font-bold">QuotesAI</span>
  </MobileLink>
  );
}

interface MobileLinkProps extends LinkProps {
  onOpenChange?: (open: boolean) => void;
  children: React.ReactNode;
  className?: string;
}

function MobileLink({
  href,
  onOpenChange,
  className,
  children,
  ...props
}: MobileLinkProps) {
  const router = useRouter();
  return (
    <Link
      href={href}
      onClick={() => {
        router.push(href.toString());
        onOpenChange?.(false);
      }}
      className={cn(className)}
      {...props}
    >
      {children}
    </Link>
  );
}
export default MobileNav;
