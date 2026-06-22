import { TATTOOS } from "@/lib/data/tattoos";
import type { SearchQuery, SearchResult, Tattoo } from "@/lib/types";

// Keyword-based stand-in for vector similarity search.
//
// MVP scaffold strategy: filters are exact-match, and the free-text prompt is
// scored against each tattoo's title/style/tags by simple token overlap. This
// keeps the UI → API → data slice honest end-to-end without any AI dependency.
// Swap `scorePrompt` for an embeddings + vector-DB lookup later; the shape of
// SearchResult stays the same so the UI doesn't change.

function tokenize(text: string): string[] {
  return text
    .toLowerCase()
    .split(/[^a-z0-9]+/)
    .filter(Boolean);
}

function searchableText(t: Tattoo): string[] {
  return tokenize([t.title, t.style, t.bodyPart, t.size, ...t.tags].join(" "));
}

function scorePrompt(prompt: string, t: Tattoo): number {
  const queryTokens = tokenize(prompt);
  if (queryTokens.length === 0) return 1; // no prompt = everything is equally relevant
  const haystack = new Set(searchableText(t));
  const hits = queryTokens.filter((tok) => haystack.has(tok)).length;
  return hits / queryTokens.length;
}

export function search(query: SearchQuery): SearchResult[] {
  const { prompt = "", filters = {} } = query;

  const filtered = TATTOOS.filter((t) => {
    if (filters.style && t.style !== filters.style) return false;
    if (filters.bodyPart && t.bodyPart !== filters.bodyPart) return false;
    if (filters.size && t.size !== filters.size) return false;
    return true;
  });

  const hasPrompt = tokenize(prompt).length > 0;

  return filtered
    .map((t) => ({ ...t, score: scorePrompt(prompt, t) }))
    // When a prompt is given, drop zero-relevance results; otherwise keep all.
    .filter((r) => !hasPrompt || r.score > 0)
    .sort((a, b) => b.score - a.score);
}
