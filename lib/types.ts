// Shared domain types for the tattoo catalog and search.

// Style presets mirror the AI Generator presets so search & generation stay aligned.
export const STYLES = [
  "fine-line",
  "traditional",
  "blackwork",
  "watercolor",
  "geometric",
  "minimalist",
  "tribal",
  "realism",
] as const;
export type Style = (typeof STYLES)[number];

export const BODY_PARTS = [
  "arm",
  "forearm",
  "back",
  "chest",
  "leg",
  "ankle",
  "wrist",
  "neck",
] as const;
export type BodyPart = (typeof BODY_PARTS)[number];

export const SIZES = ["small", "medium", "large"] as const;
export type Size = (typeof SIZES)[number];

export interface Tattoo {
  id: string;
  title: string;
  style: Style;
  bodyPart: BodyPart;
  size: Size;
  // Free-text tags power prompt matching until real image embeddings land.
  tags: string[];
  imageUrl: string;
}

export interface SearchFilters {
  style?: Style;
  bodyPart?: BodyPart;
  size?: Size;
}

export interface SearchQuery {
  prompt?: string;
  filters?: SearchFilters;
}

export interface SearchResult extends Tattoo {
  // 0..1 relevance from the (currently keyword-based) matcher.
  score: number;
}

// --- AI Design Generator ---

export interface GenerateRequest {
  prompt: string;
  style: Style;
  count?: number; // variations to produce (default 4)
  seed?: number; // changes on "regenerate" to get fresh variations
}

export interface GeneratedDesign {
  id: string; // stable per (prompt, style, seed, index) so favorites dedupe
  prompt: string;
  style: Style;
  imageUrl: string;
  createdAt: number;
}

