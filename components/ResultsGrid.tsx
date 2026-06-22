"use client";

import type { SearchResult } from "@/lib/types";

const cap = (s: string) =>
  s.charAt(0).toUpperCase() + s.slice(1).replace(/-/g, " ");

export default function ResultsGrid({
  results,
  loading,
}: {
  results: SearchResult[];
  loading: boolean;
}) {
  if (loading) {
    return <div className="empty">Searching…</div>;
  }

  if (results.length === 0) {
    return (
      <div className="empty">
        No designs match that. Try a different prompt or clear your filters.
      </div>
    );
  }

  return (
    <div className="grid">
      {results.map((t) => (
        <article key={t.id} className="card">
          <div className="thumb">
            {/* Plain <img> keeps the scaffold dependency-light; switch to
                next/image once real assets and sizes are settled. */}
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src={t.imageUrl} alt={t.title} loading="lazy" />
          </div>
          <div className="card-body">
            <h3>{t.title}</h3>
            <div className="tags">
              <span className="tag">{cap(t.style)}</span>
              <span className="tag">{cap(t.bodyPart)}</span>
              <span className="tag">{cap(t.size)}</span>
            </div>
          </div>
        </article>
      ))}
    </div>
  );
}
