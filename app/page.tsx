"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import SiteHeader from "@/components/SiteHeader";
import SearchControls from "@/components/SearchControls";
import ResultsGrid from "@/components/ResultsGrid";
import type { SearchFilters, SearchResult } from "@/lib/types";

export default function Home() {
  const [prompt, setPrompt] = useState("");
  const [filters, setFilters] = useState<SearchFilters>({});
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(true);

  // Track in-flight request so a newer search supersedes an older one.
  const reqId = useRef(0);

  const runSearch = useCallback(
    async (p: string, f: SearchFilters) => {
      const id = ++reqId.current;
      setLoading(true);

      const params = new URLSearchParams();
      if (p.trim()) params.set("prompt", p.trim());
      if (f.style) params.set("style", f.style);
      if (f.bodyPart) params.set("bodyPart", f.bodyPart);
      if (f.size) params.set("size", f.size);

      try {
        const res = await fetch(`/api/search?${params.toString()}`);
        const data = await res.json();
        if (id === reqId.current) setResults(data.results ?? []);
      } catch {
        if (id === reqId.current) setResults([]);
      } finally {
        if (id === reqId.current) setLoading(false);
      }
    },
    [],
  );

  // Initial load — show the full catalog.
  useEffect(() => {
    runSearch("", {});
  }, [runSearch]);

  // Re-run automatically when filters change (prompt re-runs on submit).
  const handleFiltersChange = (next: SearchFilters) => {
    setFilters(next);
    runSearch(prompt, next);
  };

  return (
    <main className="container">
      <SiteHeader />

      <SearchControls
        prompt={prompt}
        filters={filters}
        onPromptChange={setPrompt}
        onFiltersChange={handleFiltersChange}
        onSubmit={() => runSearch(prompt, filters)}
      />

      {!loading && (
        <p className="result-meta">
          {results.length} {results.length === 1 ? "design" : "designs"}
          {prompt.trim() ? ` for "${prompt.trim()}"` : ""}
        </p>
      )}

      <ResultsGrid results={results} loading={loading} />
    </main>
  );
}
