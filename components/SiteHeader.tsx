"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const LINKS = [
  { href: "/", label: "Search" },
  { href: "/generate", label: "Generate" },
  { href: "/favorites", label: "Favorites" },
];

export default function SiteHeader({ tagline = true }: { tagline?: boolean }) {
  const pathname = usePathname();

  return (
    <header className="app-header">
      <div className="header-top">
        <Link href="/" className="brand">
          Ink<span className="ink">Find</span>
        </Link>
        <nav className="nav">
          {LINKS.map((l) => {
            const active =
              l.href === "/" ? pathname === "/" : pathname.startsWith(l.href);
            return (
              <Link
                key={l.href}
                href={l.href}
                className={active ? "nav-link active" : "nav-link"}
              >
                {l.label}
              </Link>
            );
          })}
        </nav>
      </div>
      {tagline && (
        <p>Find your next tattoo. Generate it. See it on you — before you commit.</p>
      )}
    </header>
  );
}
