import { NextResponse } from "next/server";
import { search } from "@/lib/search";
import {
  BODY_PARTS,
  SIZES,
  STYLES,
  type BodyPart,
  type SearchFilters,
  type Size,
  type Style,
} from "@/lib/types";

// GET /api/search?prompt=...&style=...&bodyPart=...&size=...
// Returns matched tattoos from the mock catalog. Swap `search()` internals for
// a real vector-DB lookup later — the request/response contract stays the same.
export function GET(request: Request) {
  const { searchParams } = new URL(request.url);

  const prompt = searchParams.get("prompt") ?? "";

  const filters: SearchFilters = {};
  const style = searchParams.get("style");
  const bodyPart = searchParams.get("bodyPart");
  const size = searchParams.get("size");

  // Validate filters against known enums; ignore anything unexpected.
  if (style && (STYLES as readonly string[]).includes(style)) {
    filters.style = style as Style;
  }
  if (bodyPart && (BODY_PARTS as readonly string[]).includes(bodyPart)) {
    filters.bodyPart = bodyPart as BodyPart;
  }
  if (size && (SIZES as readonly string[]).includes(size)) {
    filters.size = size as Size;
  }

  const results = search({ prompt, filters });

  return NextResponse.json({ count: results.length, results });
}
