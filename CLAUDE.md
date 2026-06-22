# InkFind — Project Context

AI-powered tattoo discovery, design generation, and placement-preview platform, built for the Indian market. Tagline: *"Find your next tattoo. Generate it. See it on you — before you commit."* Source docs in repo: `InkFind_MVP_Product_Plan.docx` and `InkFind_Pitch_Deck.pptx` — this file is the condensed engineering summary distilled from both.

## What InkFind is (one-liner)
A single product that takes a user from *"I like this idea"* to *"I know exactly where and how this will look on me"* — before they ever sit in the tattoo chair. It combines four things that today live in scattered places: a tattoo-specific search engine, a generative AI design tool, an on-body placement preview, and an educational tattoo guide.

## The problem it solves
Getting a tattoo is permanent, but the decision is usually made with little support.
- **41% of tattoo regret (global) comes down to placement** — *where* the design sits on the body. No mainstream tool lets you preview a design on a photo of your own body first. (Source: Tattoo Pathway survey, 2024.)
- **In India, discovery = scrolling scattered Instagram pages + DM-ing studios on WhatsApp.** There is no dedicated platform. Instagram shows pictures but can't tell you if a design suits your body, and can't generate anything new.
- **Budget-conscious customers default to cheaper, under-regulated parlors** where hygiene and ink-safety checks rarely happen. (Karnataka FDA flagged heavy-metal contamination in tattoo ink, March 2025 — this is why the Tattoo Guide's hygiene/safety checklist matters.)

## Market context (why now)
- India tattoo market projected ~**$100M (~₹830 crore) by 2026**.
- Asia-Pacific is the fastest-growing tattoo region globally, ~**12.6% CAGR** (ahead of North America & Europe).
- Demand concentrated in **Delhi, Mumbai, Bengaluru**, driven by young professionals.
- Unlike US/Europe, India has **no digital-first layer** for tattoo discovery yet — demand is outpacing the tooling. (Sources: Fortune Business Insights, Cognitive Market Research, Custom Market Insights, 2025–26.)

## Competitive positioning
InkFind is the only option that closes the *full loop*. Versus alternatives:
| Capability | Instagram/WhatsApp | Generic AI image tools | India booking apps | InkFind |
|---|---|---|---|---|
| Real tattoo-specific search | partial | no | rare | ✓ |
| AI design generation | no | yes (generic) | no | ✓ |
| Preview on your own body | no | no | rare | ✓ |
| Style-based placement guide | no | no | no | ✓ |

## Business model (context — not all MVP)
Three layered revenue streams:
1. **Freemium generations** — free search + limited AI generations; **₹149–₹299/month** unlocks unlimited generations + HD downloads (UPI & Indian gateways). *This is the MVP monetization.*
2. **Studio & artist directory** — paid placement for studios/artists (Phase 2).
3. **Booking hand-off commission** — commission when a saved design becomes a studio visit, handed off via WhatsApp/Instagram (Phase 3).

## Target market
India first. Pricing in ₹, UPI/Razorpay/PayU payments, Hindi/regional-language UI as a stretch goal. Discovery today happens through scattered Instagram pages and WhatsApp DMs — that fragmentation is the core problem this product solves.

## Suggested tech stack
- Frontend: React / Next.js
- Backend: Node.js or Python (FastAPI)
- Search: Vector database (Pinecone / Weaviate) over tattoo image embeddings
- Generation: Fine-tuned diffusion model or image-gen API
- Placement preview: Canvas-based image compositing & warping
- Payments: Razorpay or PayU (UPI, cards, wallets)
- Database: PostgreSQL
- Hosting: AWS or GCP (Mumbai/Hyderabad region for low latency)

None of this is fixed — treat it as a credible starting point, not a locked architecture. Flag better alternatives if you see them.

## MVP features — build in this order
1. **Smart Search & Discovery** — prompt-based + image-based search, filters by style/body part/size.
2. **AI Design Generator** — style presets (fine-line, traditional, blackwork, watercolor, geometric), multiple variations, regenerate, save favorites.
3. **Placement Preview ("Try It On")** — upload a body-part photo, drag/resize/rotate a design onto it, skin-tone & lighting blend.
4. **Tattoo Guide** — style-to-placement suitability, pain/healing-time reference, size + aftercare basics, hygiene & safety checklist for picking a studio.

## Core user journey (the loop the MVP must prove)
The four MVP features are buildable independently, but value compounds when chained:
1. **Describe or upload inspo** — search by text prompt or reference image.
2. **Generate or pick a design** — create something new, or shortlist a match.
3. **Preview it on your body** — drag the design onto a photo of the placement area.
4. **Save, learn & book confidently** — check the guide, save favorites, move forward informed.

Keep this flow in mind: a feature isn't "done" only in isolation — the north star is a user moving smoothly through all four steps.

## How to build this
- Build one vertical slice at a time — a feature should work end-to-end (UI → API → data) with mock/sample data before wiring in real AI generation or vector search.
- Don't build Phase 2/3 features yet (saved collections, artist directory, community gallery, cost estimator, AR preview, style quiz) unless explicitly asked — they come after the MVP loop works.
- Mobile-first responsive UI; most users will be on phones.
- Ask before introducing a new major dependency or changing the suggested stack.

## Roadmap (for context — not to build yet)
- **Phase 2 — Engagement:** saved collections, studio & artist directory (Delhi/Mumbai/Bengaluru first), community gallery, cost estimator in ₹.
- **Phase 3 — Expansion:** live AR camera preview, style-matching quiz, direct WhatsApp/Instagram hand-off & booking, multi-angle preview.
