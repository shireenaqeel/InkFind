# InkFind — Dev Log

A running log of what we build, in order, with the decisions behind each step.
Newest entries at the top. Keep this updated as each slice progresses.

---

## 2026-06-23 — Slice 2: AI Design Generator (scaffold)

**Goal:** Prove MVP feature #2 end-to-end (UI → API → data) with mock generation, no real diffusion yet.

**What was built**
- Types: `GenerateRequest`, `GeneratedDesign` (`lib/types.ts`).
- Mock generator (`lib/generate.ts`): produces N deterministic placeholder
  variations seeded by (prompt, style, seed, index). FNV-1a hash → stable image URLs.
- API: `POST /api/generate` (`app/api/generate/route.ts`) with prompt/style validation.
- `/generate` page: prompt input, style-preset chips, 4 variations per run,
  one-tap **Regenerate** (reseeds), per-card **♥ save** and **Download**.
- Favorites: `useFavorites` hook (`lib/favorites.ts`) — localStorage-backed personal
  collection, synced across hook instances via a custom event. `/favorites` page.
- Shared `SiteHeader` with nav (Search / Generate / Favorites); home page refactored
  to use it.

**Decisions**
- **Mock generator as placeholder for image-gen API** — `GeneratedDesign` contract is
  stable so UI won't change when a real diffusion/image API lands.
- **Deterministic seeding** so "Regenerate" yields a fresh-but-reproducible set, and
  saved favorites have stable ids that dedupe correctly.
- **localStorage favorites (no auth yet)** — swap storage layer for an API-backed
  collection once accounts exist; hook surface stays the same.
- **Download via fetch→blob** with open-in-tab fallback for cross-origin placeholders.

**Verified**
- `npm run build` ✓ — routes: `/`, `/generate`, `/favorites`, `/api/generate`, `/api/search`.
- `POST /api/generate` seed=1 reproducible across runs; seed=2 differs (regenerate works).
- Validation: missing prompt → 400; bad style → descriptive error.
- All three pages return HTTP 200.

**Next up**
- Real image-gen API behind `/api/generate`.
- Then Slice 3: Placement Preview ("Try It On").

---

## 2026-06-23 — Slice 1: Smart Search & Discovery (scaffold)

**Goal:** Prove MVP feature #1 end-to-end (UI → API → data) with mock data, no AI yet.

**What was built**
- Next.js (App Router) + TypeScript app scaffolded from scratch.
- Domain model: `Style`, `BodyPart`, `Size` enums + `Tattoo` / `SearchResult` types (`lib/types.ts`).
- Mock catalog of 16 tattoos with style/body-part/size/tags (`lib/data/tattoos.ts`),
  placeholder images from picsum.photos.
- Keyword search matcher (`lib/search.ts`): exact-match filters + prompt scored by
  token overlap against title/style/tags. Sorted by relevance.
- API: `GET /api/search?prompt=&style=&bodyPart=&size=` (`app/api/search/route.ts`),
  validates filters against enums.
- UI (mobile-first): `SearchControls` (search bar + image-upload stub + filters) and
  `ResultsGrid` (responsive 2→4 column card grid). Filters re-run search on change;
  prompt runs on submit. Stale-response guard via request id.

**Decisions**
- **Next.js API routes as the backend layer** (instead of a separate Node/Python
  service) — keeps the slice in one app. Can be split into FastAPI/Node later. Stays
  within the suggested stack.
- **Keyword matcher as a placeholder for vector search** — `SearchResult` shape is
  stable so the UI won't change when real embeddings + vector DB land.
- **Plain `<img>`** for cards in the scaffold to stay dependency-light; switch to
  `next/image` once real assets/sizes are settled.
- **Next 16** — upgraded from initially-pinned 15.3.1 after npm flagged a security
  vuln (CVE-2025-66478). Builds clean on React 19.
- **Image-based search is a UI stub** (alert + "coming soon") — needs real embeddings.

**Verified**
- `npm run build` ✓ compiles, TypeScript clean.
- `GET /api/search?prompt=wolf` → 2 results (Minimalist Line Wolf, Geometric Wolf Head).
- `GET /api/search?style=watercolor&size=medium` → 2 results.
- Homepage returns HTTP 200.

**Next up**
- Wire real tattoo dataset / embeddings + a vector DB (Pinecone/Weaviate).
- Implement real image-based search.
- Then move to Slice 2: AI Design Generator.

---

## 2026-06-23 — Project context established

- Wrote `CLAUDE.md` distilling the MVP product plan + pitch deck (problem, market,
  business model, competitive positioning, 4-feature MVP, build philosophy).
- Initialized git + GitHub repo for sync.
