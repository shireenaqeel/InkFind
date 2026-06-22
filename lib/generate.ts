import type { GenerateRequest, GeneratedDesign, Style } from "@/lib/types";

// Mock AI design generator.
//
// MVP scaffold strategy: instead of calling a diffusion model, we produce
// deterministic placeholder images seeded by (prompt, style, seed, index). This
// lets the full generate → vary → regenerate → save loop work end-to-end with no
// AI dependency. Swap `generate()` internals for a real image-gen API later; the
// GeneratedDesign contract stays the same so the UI doesn't change.

const DEFAULT_COUNT = 4;
const MAX_COUNT = 8;

// Tiny stable string hash → used to seed placeholder image URLs.
function hash(str: string): number {
  let h = 2166136261;
  for (let i = 0; i < str.length; i++) {
    h ^= str.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
}

function slug(prompt: string, style: Style, seed: number, index: number): string {
  const base = `${style}-${prompt}-${seed}-${index}`.toLowerCase();
  return `${hash(base)}`;
}

export function generate(req: GenerateRequest): GeneratedDesign[] {
  const prompt = (req.prompt ?? "").trim();
  const style = req.style;
  const seed = req.seed ?? 0;
  const count = Math.min(Math.max(req.count ?? DEFAULT_COUNT, 1), MAX_COUNT);
  const createdAt = Date.now();

  return Array.from({ length: count }, (_, index) => {
    const s = slug(prompt, style, seed, index);
    return {
      id: s,
      prompt,
      style,
      // Placeholder render; deterministic per seed so "regenerate" yields a new set.
      imageUrl: `https://picsum.photos/seed/${s}/600/800`,
      createdAt,
    };
  });
}
