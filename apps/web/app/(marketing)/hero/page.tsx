import { BentoDemo } from "@/components/bento-features";
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
            <Link
              href="/#features"
              className={cn(
                buttonVariants({ variant: "outline", size: "lg" }),
                "mt-sm-2",
              )}
            >
              Let&apos;s Explore 👇🏻
            </Link>
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
