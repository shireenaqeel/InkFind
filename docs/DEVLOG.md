# InkFind — Dev Log

A running log of what we build, in order, with the decisions behind each step.
Newest entries at the top. Keep this updated as each slice progresses.

---

## 2026-07-28 — Real AI generation (Replicate/FLUX) behind /generate

**Goal:** Replace the mock generator's placeholder images with real image
generation — the first mock→real backend swap — without changing the UI or the
`GeneratedDesign` contract.

**What was built**
- `imagegen.py` — Replicate integration. Default model **FLUX.1 [schnell]** (fast,
  cheap, up to 4 images/call, `seed` for reproducible regenerate). Per-style prompt
  modifiers (`STYLE_PROMPTS`) steer the look; uses Replicate's `Prefer: wait` with a
  short poll fallback. Model overridable via `REPLICATE_MODEL`.
- `generate.py` — now calls `imagegen` when a token is set, else falls back to the
  deterministic picsum mock. **Any failure degrades gracefully to the mock** (logged),
  so the app never breaks. Also fixed regenerate to actually reseed: a fresh random
  `seed` per call (unless pinned), with ids still stable within a batch for dedupe.
- Config via `.env` (`load_dotenv()` in `main.py`); `.env.example` documents
  `REPLICATE_API_TOKEN` + `REPLICATE_MODEL`. Deps: `httpx`, `python-dotenv`.
- UI: `/generate` shows a **Live AI / Demo mode** badge (from `imagegen.is_enabled()`),
  an "Inking your designs…" HTMX spinner (`hx-indicator`), and disables the
  Generate/Regenerate buttons mid-request (`hx-disabled-elt`).

**Decisions**
- **Replicate** (user's pick) — model choice + tattoo-specific fine-tunes/LoRAs, swap
  via one env var. **Mock fallback** kept so the repo runs with zero keys and demos work.
- **Optional-by-default**: no token → identical behavior to before. The token is the
  only thing standing between demo and live.
- **URLs used as-is** — Replicate output URLs are hosted ~1h. Fine for MVP; a later
  step should download + persist images so saved favorites don't expire (noted below).

**Verified**
- No token: `is_enabled()` False; `generate()` returns 4 deterministic picsum designs;
  regenerate now yields a different set; `/generate` shows the Demo badge; POST
  `/generate` + `/api/generate` return 4.
- Dummy token: real path is attempted, 401 is caught, and it **falls back to mock** (4
  designs, picsum URLs) with a logged warning — graceful degradation confirmed.
- Real end-to-end (valid token) is pending a key from the user.

**Next up**
- Add a valid `REPLICATE_API_TOKEN` to `.env` and confirm live generations.
- Persist generated images (download to storage) so favorites survive URL expiry.
- Freemium generation limits (₹ plan) once accounts land.

---

## 2026-07-25 — Slice 4: Tattoo Guide

**Goal:** Prove MVP feature #4 — the educational layer that lets someone walk into a
studio informed. Completes the MVP loop (search/generate → try on → **learn & book
confidently**).

**What was built**
- `guide.py` — a curated, deterministic knowledge base: per-style placement
  suitability + blurbs, per-body-part pain (1–5) & healing reference, aftercare
  steps, and an India-specific **hygiene & safety checklist** (cites the March 2025
  Karnataka FDA heavy-metal ink flags from the product plan). Plus `assess(style,
  body_part)` → a suitability verdict, and `guide_data()` for the API.
- `GET /guide` page (`templates/guide.html`) + nav link "Guide": an interactive
  **style→placement matcher** (two selects, HTMX-swaps a verdict fragment
  `_assessment.html`), then style cards, a pain/healing table, aftercare, and the
  checklist. Deep-linkable via `/guide?style=&bodyPart=`.
- `GET /guide/assess` HTMX fragment; `GET /api/guide` JSON (full base, or a single
  verdict when passed `style`+`bodyPart`; 400 on unknown values).
- Loop touch: the Try It On page now links to the guide with the style preselected
  ("Not sure a spot suits the style? → guide").

**Decisions**
- **Content as data, not prose in a template** (`guide.py`) — keeps it testable, lets
  the matcher and the JSON API share one source, and makes it swappable for a CMS/DB
  later without touching the UI.
- **Suitability is rule-based, not ML** — a style's `detail` (fine/bold) crossed with
  a small high-friction set drives the verdict. Honest for an MVP and easy to reason
  about; a data/ML ranking can slot behind the same `assess()` signature.
- **Explicitly framed as general guidance, not medical advice** — pain/healing numbers
  are rough, widely-cited references with per-person caveats in the UI.
- **India-first safety framing** — the checklist leads on ink safety and single-use
  needles because budget parlours are the product's stated risk; it's the reason this
  feature exists, not filler.

**Verified**
- TestClient: `/guide` 200 and includes the matcher, checklist, and the Karnataka
  reference; `/guide?style=watercolor&bodyPart=wrist` preselects and renders a
  "Tricky" (level-warn) verdict; `/guide/assess` for traditional/arm → "Great fit"
  (level-good); `/api/guide` returns the full base (8 styles, 8 body parts) and a
  single verdict when parametrised; unknown style → 400; nav shows "Guide"; `/`,
  `/generate`, `/try-on`, `/favorites` still 200.

**Next up**
- MVP feature set is complete end-to-end on mock data. Next: replace the mocks with
  real backends — image-gen behind `/generate`, embeddings + vector DB behind search
  — and add accounts so favorites/collections persist beyond a session.

---

## 2026-07-24 — Slice 3: Placement Preview ("Try It On")

**Goal:** Prove MVP feature #3 — let a user preview a design on a photo of their
own body before committing. This is the feature that most directly attacks the
"41% of regret is placement" problem.

**What was built**
- New page `GET /try-on` (`main.py`, `templates/tryon.html`) + nav link "Try On".
- Canvas compositor (`static/tryon.js`): upload a body-part photo → it becomes the
  background; a design overlays on top with **drag to reposition** (Pointer Events,
  so touch + mouse), **size / rotation / opacity** sliders, and a **skin-blend**
  mode (Normal / Multiply / Overlay). **Download** exports the composite as PNG.
- Wired the **core loop**: every search result and every generated/saved design now
  has a "Try it on →" link that opens `/try-on?design=&prompt=&style=` with the
  design **preloaded** onto the canvas (`_macros.html`). Generate/Search → Try It On.

**Decisions**
- **Client-side compositing (vanilla JS), not a server round-trip.** Canvas warping/
  blending is inherently browser-side, and keeping the body photo on-device is the
  right privacy default (esp. for the India market). The server's role is the
  server-rendered page + the query-param preload that carries the loop. No new deps.
- **Transform stored as fractions of the canvas** (position 0..1, size as a % of
  canvas width) so swapping the photo for one with different pixel dimensions
  doesn't make the design jump.
- **`crossOrigin="anonymous"` on preloaded designs** so a picsum/remote design
  doesn't taint the canvas and block PNG export; uploaded designs are data URLs.
- **Multiply as the default blend** — approximates ink sitting in skin. It's a
  stand-in for real skin-tone/lighting compositing; the slider set is the seam a
  better blend model slots into later.
- **Delta-based drag** (grab-and-nudge) rather than snap-to-finger, so the design
  doesn't jump to the touch point on first contact.

**Verified**
- TestClient: `/try-on` 200 and renders the canvas + loads `tryon.js`;
  `/static/tryon.js` 200; preload params (`design`/`prompt`/`style`) land in the
  page's `data-*`; an invalid `style` is dropped to `""`; search **and** generated
  cards both carry `/try-on?design=` links; nav shows "Try On"; `/`, `/generate`,
  `/favorites` still 200.

**Next up**
- Slice 4: Tattoo Guide (style→placement suitability, pain/healing, aftercare,
  hygiene & safety checklist) — completes the MVP loop.
- Real image-gen behind `/generate`; transparent-PNG designs will make the blend
  read much better than opaque placeholder photos.

---

## 2026-07-13 — Port to Python (FastAPI + Jinja2 + HTMX)

**Goal:** Re-platform the app to be Python-first per request ("can we do this
entirely in Python?"). Ported Slices 1 & 2 with identical behavior and data.

**What was built** (`inkfind/` package)
- Domain model ported to dataclasses/constants (`models.py`) — `STYLES`,
  `BODY_PARTS`, `SIZES`, `Tattoo`, `SearchResult`, `GeneratedDesign`.
- Same 16-tattoo mock catalog (`data.py`), keyword search matcher (`search.py`),
  and mock generator (`generate.py`) — the FNV-1a hash was ported exactly, so
  placeholder picsum image URLs are **byte-for-byte identical** to the TS version.
- FastAPI app (`main.py`): server-rendered pages + HTMX fragments for Search,
  Generate, and Favorites. Original JSON contracts preserved under `/api/search`
  and `/api/generate` for a future real frontend.
- Templates (Jinja2) + ported dark-theme CSS (`static/styles.css`, copied from
  the Next.js `globals.css`).
- Favorites moved from browser localStorage to a server-side per-session store
  (`favorites.py`), keyed by an `inkfind_sid` cookie. In-memory for now.

**Decisions**
- **FastAPI + HTMX over Streamlit/Gradio** — keeps a real mobile-first web UX and
  server-rendered Python for ~90% of the UI; only chip selection uses a few lines
  of vanilla JS. The placement-preview canvas (Slice 3) will need browser JS
  regardless of stack, so this minimizes JS rather than pretending it away.
- **Server-side favorites** — fits HTMX naturally without client state; swap the
  in-memory store for a DB once accounts land (same list/toggle/is_favorite API).
- **Next.js scaffold left in place** (`app/`, `components/`, `lib/`) but superseded
  by the Python app; can be removed once the Python version is confirmed as the path.

**Verified**
- `uvicorn inkfind.main:app` boots; `/`, `/search`, `/generate`, `/favorites`,
  `/static/styles.css` all return HTTP 200.
- TestClient end-to-end: home renders 16 catalog cards; `search?prompt=wolf` → 2
  (matches TS); `style=blackwork` → 2; generate → 4 variations; empty prompt →
  error; save→collection→unsave favorites loop works; `/api/*` JSON parity holds
  and generated `imageUrl` matches the hashed picsum seed.

**Next up**
- Decide whether to delete the Next.js scaffold.
- Real image-gen API behind `/generate`; then Slice 3: Placement Preview.

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
