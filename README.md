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
| 2 | AI Design Generator | 🟢 scaffolded (mock gen, variations, favorites) |
| 3 | Placement Preview ("Try It On") | ⚪ not started |
| 4 | Tattoo Guide | ⚪ not started |

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
  generate.py             # mock design generator (placeholder for image-gen API)
  favorites.py            # server-side saved collection (per-session, in-memory)
  templates/              # Jinja2: base, index (search), generate, favorites, fragments
  static/styles.css       # mobile-first dark theme
run.py                    # dev entrypoint
requirements.txt
```

## AI Design Generator — how it works (MVP)

- **Style presets** (fine-line, traditional, blackwork, watercolor, geometric, …) as chips.
- **Variations:** 4 per generate; **Regenerate** reseeds for a fresh set.
- **Mock engine:** deterministic placeholder images seeded by (prompt, style, seed,
  index). Swap `inkfind/generate.py` for a real image-gen API — `GeneratedDesign`
  contract stays stable.
- **Favorites:** tap ♥ to save to a personal collection (server-side per-session
  store today; DB-backed once accounts land).

## Smart Search — how it works (MVP)

- **Prompt search:** free text is tokenized and scored by overlap against each
  tattoo's title/style/tags. Stand-in for vector similarity search.
- **Filters:** exact match on style, body part, and size.
- **Image search:** UI stub only — wired to real embedding lookup later.

The `SearchResult` contract stays stable, so swapping the keyword matcher for a
real embeddings + vector-DB backend won't require UI changes.

---

🤖 Built with [Claude Code](https://claude.com/claude-code)
