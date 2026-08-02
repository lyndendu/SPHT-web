import Image from "next/image";

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
