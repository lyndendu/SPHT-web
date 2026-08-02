from pathlib import Path

hero_path = Path("apps/web/app/(marketing)/hero/page.tsx")
hero = hero_path.read_text(encoding="utf-8")
hero = hero.replace(
    '            <a\n              href="/#features"',
    '            <Link\n              href="/#features"',
    1,
)
hero = hero.replace("            </a>\n", "            </Link>\n", 1)
hero_path.write_text(hero, encoding="utf-8")

main_nav_path = Path("apps/web/components/main-nav.tsx")
main_nav = main_nav_path.read_text(encoding="utf-8")
main_nav = main_nav.replace(
    '''                    <a
                      className="flex h-full w-full select-none flex-col justify-end rounded-md bg-gradient-to-b from-muted/50 to-muted p-6 no-underline outline-none focus:shadow-md"
                      href="/"
                    >''',
    '''                    <Link
                      className="flex h-full w-full select-none flex-col justify-end rounded-md bg-gradient-to-b from-muted/50 to-muted p-6 no-underline outline-none focus:shadow-md"
                      href="/"
                    >''',
    1,
)
main_nav = main_nav.replace("                    </a>\n", "                    </Link>\n", 1)
main_nav_path.write_text(main_nav, encoding="utf-8")

db_path = Path("apps/web/lib/db.ts")
db = db_path.read_text(encoding="utf-8")
db = db.replace("  // eslint-disable-next-line no-var, no-unused-vars\n", "")
db_path.write_text(db, encoding="utf-8")

print("Remaining source lint findings resolved.")
