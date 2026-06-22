"use client";

import { useState } from "react";
import SiteHeader from "@/components/SiteHeader";
import DesignCard from "@/components/DesignCard";
import { useFavorites } from "@/lib/favorites";
import { STYLES, type GeneratedDesign, type Style } from "@/lib/types";

const cap = (s: string) =>
  s.charAt(0).toUpperCase() + s.slice(1).replace(/-/g, " ");

export default function GeneratePage() {
  const [prompt, setPrompt] = useState("");
  const [style, setStyle] = useState<Style>("fine-line");
  const [designs, setDesigns] = useState<GeneratedDesign[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const { isFavorite, toggle } = useFavorites();

  async function runGenerate(seed: number) {
    if (!prompt.trim()) {
      setError("Describe the tattoo you want to generate.");
      return;
    }
    setError(null);
    setLoading(true);
    try {
      const res = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: prompt.trim(), style, count: 4, seed }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error ?? "Generation failed");
      setDesigns(data.designs ?? []);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Generation failed");
      setDesigns([]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="container">
      <SiteHeader tagline={false} />

      <section className="generator">
        <h2 className="section-title">AI Design Generator</h2>
        <p className="section-sub">
          Describe an idea, pick a style, and generate original variations.
        </p>

        <form
          className="searchbar"
          onSubmit={(e) => {
            e.preventDefault();
            runGenerate(Date.now());
          }}
        >
          <input
            type="text"
            value={prompt}
            placeholder='e.g. "a phoenix rising with peony flowers"'
            onChange={(e) => setPrompt(e.target.value)}
            aria-label="Describe the tattoo to generate"
          />
          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? "Generating…" : "Generate"}
          </button>
        </form>

        <div className="presets">
          {STYLES.map((s) => (
            <button
              key={s}
              type="button"
              className={s === style ? "chip active" : "chip"}
              onClick={() => setStyle(s)}
            >
              {cap(s)}
            </button>
          ))}
        </div>

        {error && <p className="error">{error}</p>}
      </section>

      {designs.length > 0 && (
        <>
          <div className="result-meta-row">
            <p className="result-meta">
              {designs.length} variations · {cap(style)}
            </p>
            <button
              type="button"
              className="btn btn-ghost"
              onClick={() => runGenerate(Date.now())}
              disabled={loading}
            >
              ↻ Regenerate
            </button>
          </div>

          <div className="grid">
            {designs.map((d) => (
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

      {!loading && designs.length === 0 && !error && (
        <div className="empty">
          Your generated designs will appear here. Tap a ♥ to save favorites.
        </div>
      )}
    </main>
  );
}
