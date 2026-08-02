import { BellIcon, BookmarkIcon, CopyIcon, GlobeIcon, InputIcon } from "@radix-ui/react-icons";
import { BentoCard, BentoGrid } from "@spht/ui/magicui/bento-grid";

const decorativeBackground = (
  <div aria-hidden="true" className="absolute -right-20 -top-20 h-40 w-40 rounded-full bg-muted opacity-60 blur-3xl" />
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
