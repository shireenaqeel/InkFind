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
| 2 | AI Design Generator | ⚪ not started |
| 3 | Placement Preview ("Try It On") | ⚪ not started |
| 4 | Tattoo Guide | ⚪ not started |

Detailed progress + decisions: [`docs/DEVLOG.md`](./docs/DEVLOG.md).

## Tech stack

- **Framework:** Next.js (App Router) + React + TypeScript
- **API:** Next.js route handlers (a dedicated FastAPI/Node service can be split out later)
- **Data:** mock catalog today → PostgreSQL + vector DB (Pinecone/Weaviate) later
- **Hosting (planned):** AWS/GCP, Mumbai/Hyderabad region

## Getting started

```bash
npm install
npm run dev      # http://localhost:3000
```

Other scripts:

```bash
npm run build    # production build
npm start        # serve the production build
```

## Project structure

```
app/
  layout.tsx              # root layout + metadata
  page.tsx                # Smart Search page (client)
  globals.css            # mobile-first styles
  api/search/route.ts    # GET /api/search — prompt + filters
components/
  SearchControls.tsx     # search bar, image-upload stub, filters
  ResultsGrid.tsx        # results grid + cards
lib/
  types.ts               # domain types + style/body-part/size enums
  search.ts              # keyword matcher (placeholder for vector search)
  data/tattoos.ts        # mock tattoo catalog
```

## Smart Search — how it works (MVP)

- **Prompt search:** free text is tokenized and scored by overlap against each
  tattoo's title/style/tags. Stand-in for vector similarity search.
- **Filters:** exact match on style, body part, and size.
- **Image search:** UI stub only — wired to real embedding lookup later.

The `SearchResult` contract stays stable, so swapping the keyword matcher for a
real embeddings + vector-DB backend won't require UI changes.

---

🤖 Built with [Claude Code](https://claude.com/claude-code)
