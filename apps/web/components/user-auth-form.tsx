"use client";

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
