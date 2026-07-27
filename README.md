# InkFind

AI-powered tattoo discovery, design generation & placement preview — **built for India**.

> Find your next tattoo. Generate it. See it on you — before you commit.

InkFind takes a user from *"I like this idea"* to *"I know exactly where and how this
will look on me"* — combining a tattoo-specific search engine, a generative AI design
tool, an on-body placement preview, and an educational tattoo guide into one flow.

See [`CLAUDE.md`](./CLAUDE.md) for the full product/market context and build philosophy.

## Status

Building the MVP one vertical slice at a time (UI → API → data with mock data first).

| # | MVP feature | Status |
|---|-------------|--------|
| 1 | Smart Search & Discovery | 🟢 scaffolded (mock data, keyword matcher) |
| 2 | AI Design Generator | 🟢 real generation (Replicate/FLUX) + mock fallback |
| 3 | Placement Preview ("Try It On") | 🟢 scaffolded (canvas: drag/resize/rotate/blend + download) |
| 4 | Tattoo Guide | 🟢 scaffolded (style→placement matcher, pain/healing, aftercare, hygiene checklist) |

Detailed progress + decisions: [`docs/DEVLOG.md`](./docs/DEVLOG.md).

## Tech stack

**Python-first** (ported from the initial Next.js scaffold — see the DEVLOG).

- **Framework:** FastAPI + Jinja2 templates + HTMX (server-rendered, mobile-first)
- **API:** FastAPI routes; JSON contracts preserved under `/api/*`
- **Data:** mock catalog today → PostgreSQL + vector DB (Pinecone/Weaviate) later
- **Hosting (planned):** AWS/GCP, Mumbai/Hyderabad region

## Getting started

```bash
python -m venv .venv
.venv/Scripts/activate        # Windows (PowerShell: .venv\Scripts\Activate.ps1)
# source .venv/bin/activate   # macOS/Linux
pip install -r requirements.txt

python run.py                 # http://127.0.0.1:8000
# or: uvicorn inkfind.main:app --reload
```

## Project structure

```
inkfind/
  main.py                 # FastAPI app: pages + HTMX fragments + /api/* JSON
  models.py               # domain types + style/body-part/size constants
  data.py                 # mock tattoo catalog (16 designs)
  search.py               # keyword matcher (placeholder for vector search)
  generate.py             # design generator — real (via imagegen) with mock fallback
  imagegen.py             # Replicate/FLUX image generation (optional, token-gated)
  favorites.py            # server-side saved collection (per-session, in-memory)
  guide.py                # tattoo guide knowledge base + style/placement matcher
  templates/              # Jinja2: base, index (search), generate, tryon, guide, favorites, fragments
  static/styles.css       # mobile-first dark theme
  static/tryon.js         # client-side placement-preview canvas compositor
run.py                    # dev entrypoint
requirements.txt
```

## AI Design Generator — how it works (MVP)

- **Style presets** (fine-line, traditional, blackwork, watercolor, geometric, …) as chips.
- **Variations:** 4 per generate; **Regenerate** reseeds for a fresh set.
- **Real generation:** with a `REPLICATE_API_TOKEN` set, `/generate` produces real
  images via Replicate (default FLUX.1 [schnell]; per-style prompt tuning in
  `inkfind/imagegen.py`, model swappable via `REPLICATE_MODEL`). A **Live AI** badge
  and an "Inking…" spinner show while it runs.
- **Mock fallback:** with no token — or if a generation fails — it falls back to
  deterministic placeholder images, so the app always works. The `GeneratedDesign`
  contract is identical either way, so the UI never changes.
- **Favorites:** tap ♥ to save to a personal collection (server-side per-session
  store today; DB-backed once accounts land).

> To enable real generation: copy `.env.example` to `.env`, add your
> `REPLICATE_API_TOKEN` (from https://replicate.com/account/api-tokens), and restart.

## Placement Preview ("Try It On") — how it works (MVP)

- **Upload a body-part photo** — it becomes the canvas background. The photo stays
  entirely **on-device**; nothing is uploaded.
- **Place the design:** drag to reposition (touch + mouse), plus size, rotation and
  opacity sliders and a **skin-blend** mode (Normal / Multiply / Overlay) that
  approximates ink sitting in skin. **Download** exports the composite as a PNG.
- **The loop:** any search result or generated design has a "Try it on →" link that
  opens `/try-on` with that design **preloaded** onto the canvas.
- **Client-side by design:** canvas compositing is inherently browser-side
  (`static/tryon.js`) — the seam where a real skin-tone/lighting blend model slots in.

## Tattoo Guide — how it works (MVP)

- **Style→placement matcher:** pick a style + body part and get a suitability verdict
  (Great fit / Workable / Tricky) with the reasoning — fine-detail styles are flagged
  on high-friction spots where they blur soonest. Deep-linkable via
  `/guide?style=&bodyPart=`.
- **Reference content:** styles at a glance, a pain (1–5) + healing table per body
  part, aftercare basics, and a **hygiene & safety checklist** tuned for India (it
  cites the March 2025 Karnataka FDA heavy-metal-in-ink flags).
- **Data-driven:** all content lives in `inkfind/guide.py`; `GET /api/guide` returns
  the whole knowledge base, or a single verdict when passed `style` + `bodyPart`.

## Smart Search — how it works (MVP)

- **Prompt search:** free text is tokenized and scored by overlap against each
  tattoo's title/style/tags. Stand-in for vector similarity search.
- **Filters:** exact match on style, body part, and size.
- **Image search:** UI stub only — wired to real embedding lookup later.

The `SearchResult` contract stays stable, so swapping the keyword matcher for a
real embeddings + vector-DB backend won't require UI changes.

---

🤖 Built with [Claude Code](https://claude.com/claude-code)
