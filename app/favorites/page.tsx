"use client";

import Link from "next/link";
import SiteHeader from "@/components/SiteHeader";
import DesignCard from "@/components/DesignCard";
import { useFavorites } from "@/lib/favorites";

export default function FavoritesPage() {
  const { favorites, isFavorite, toggle } = useFavorites();

  return (
    <main className="container">
      <SiteHeader tagline={false} />

      <section className="generator">
        <h2 className="section-title">Your Collection</h2>
        <p className="section-sub">Designs you&apos;ve saved, stored on this device.</p>
      </section>

      {favorites.length === 0 ? (
        <div className="empty">
          No saved designs yet. Head to{" "}
          <Link href="/generate" className="nav-link active">
            Generate
          </Link>{" "}
          and tap ♥ on the ones you like.
        </div>
      ) : (
        <>
          <p className="result-meta">
            {favorites.length} saved {favorites.length === 1 ? "design" : "designs"}
          </p>
          <div className="grid">
            {favorites.map((d) => (
              <DesignCard
                key={d.id}
                design={d}
                saved={isFavorite(d.id)}
                onToggleSave={toggle}
              />
            ))}
          </div>
        </>
      )}
    </main>
  );
}
