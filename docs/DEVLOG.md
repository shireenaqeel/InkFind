# InkFind — Dev Log

A running log of what we build, in order, with the decisions behind each step.
Newest entries at the top. Keep this updated as each slice progresses.

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
