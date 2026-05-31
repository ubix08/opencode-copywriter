I now have a thorough picture of the entire system. Let me write the strategic analysis.

---

# Product Factory × clawd — Strategic Integration Analysis

## Executive Overview

You've built something unusually coherent here. The `hybrid-architecture-analysis.md` document — which you either produced or received — has already identified the correct architectural division. The flows you've shipped (`reddit-pain-miner`, `hn-pain-miner`) are real, working intelligence infrastructure. The factory spec (through v9.0) is the business logic layer sitting above it. The integration strategy is clear, and the path is shorter than it might seem.

Let me analyze each layer precisely, then give you the concrete implementation strategy.

---

## What You Actually Have

**clawd's execution primitives:**
- **Flow Runner**: deterministic DAG engine — `foreach`, `condition`, `llm`, `embed`, `sqlite_exec`, `classify`, `quota_gate`, `http_batch`, `python`, `javascript`, `file_write`. Stateless, packet-based, cheap per-node with haiku.
- **Agent Sessions**: multi-turn reasoning with full tool access, persistent context, SOUL.md identity.
- **Team System**: orchestratorAgent gets `send_message` (delegate to specialists), `run_flow` (trigger data flows), `shared_memory_read/write`, `stage_for_review`. SharedWorkspace auto-creates GOALS/STATUS/DECISIONS/CONTEXT.md.
- **Flow Scheduler**: cron + event triggers already wired in `gateway.ts`.
- **Event Bus**: `getDefaultBus()` — flows can emit events that other flows or agents react to.

**What you've already built (the flows):**
Both `reddit-pain-miner` and `hn-pain-miner` are production-grade. They correctly implement: HTTP scraping → dedup (MinHash LSH) → per-post LLM classification → embedding (local Ollama) → HDBSCAN clustering → quota-gated LLM labeling with Gemini/SambaNova fallback → scored opportunity output to SQLite + JSON files. These are already your **Market Signal Detection (Phase -1)** and the foundation of the factory's intelligence layer. The architecture is already correct — `reddit-pain-miner` runs nightly at 2am, `hn-pain-miner` is manual-triggered. Both output `opportunities-<date>.json` to their respective flow directories.

**What the factory spec provides:**
It's a 9-agent pipeline (v9.0 framing) that takes an opportunity → product brief → research → synthesis → writing → verification → optimization → packaging → distribution. The spec has evolved through several versions, culminating in v9.0's semi-autonomous mode where the system self-selects topics from its own opportunity pool. The `factory-team.md` and `hybrid-architecture-analysis.md` documents correctly identify the mapping onto clawd primitives.

---

## The Critical Architectural Decision: What Goes Where

The hybrid-architecture doc is right on every call. Here's the complete and precise mapping for your specific situation:

### Flows handle (already working or near-trivial to add):
- `reddit-pain-miner` (✅ done) — nightly opportunity mining
- `hn-pain-miner` (✅ done) — manual HN intelligence run
- `opportunity-ranker` (new) — reads both DBs, merges, produces unified TOP_OPPORTUNITIES.json → writes to `shared/`
- `topic-research` (new) — given a topic string, runs web_search batch + forum scrape → saves `shared/research.json`
- `kb-query` (new) — sqlite_exec against the accumulated knowledge DB → saves `shared/kb-matches.json`
- `format-pdf` (new) — takes a markdown path, runs a bash node (pandoc or markdown-pdf) → outputs PDF
- `kb-index` (new, event-triggered) — triggered by `product_complete` event, indexes the new product into the KB for future retrieval
- `demand-scan` (new) — quick web_search → LLM extract → demand score → saves `shared/demand-report.json`

### Agents handle (the factory team):
- **FORGE** (Coordinator/orchestratorAgent): receives human brief OR reads TOP_OPPORTUNITIES.json and self-selects, runs data flows, makes gate decisions, delegates via `send_message`, writes STATUS/DECISIONS, calls `stage_for_review`
- **scout**: validates topic demand and angle, refines scope → `scout-report.md`
- **architect**: designs ebook structure, 7-section skeleton, prereqs → `structure.md`
- **researcher**: given structure + research.json, selects and synthesizes 15-30 sources → `raw-corpus.md` (this is research-intensive — this is where sonnet earns its cost)
- **analyzer**: pattern extraction across sources, SOLUTION_MATRIX → `solution-matrix.md`
- **synthesizer**: creates the named framework, methodology, decision trees → `synthesized-framework.md`
- **writer**: produces the full draft from the framework → `guide-draft.md`
- **verifier**: 3-layer audit (accuracy + usability + decision quality) → `audit.md` with scores
- **optimizer**: compression, clarity, decision-driven rewrite → `guide-final.md`
- **packager**: product manifest, cover metadata, distribution copy → `product-manifest.json`

---

## The Implementation Strategy

### Phase 1 — Wire the intelligence layer to the factory (1-2 days)

The flows already produce scored opportunities. What's missing is a bridge: the coordinator needs to read them. Two options:

**Option A (recommended — zero new code):** FORGE reads opportunity files directly from the filesystem. On startup or when asked, it does `read_file("flows/reddit-pain-miner/opportunities-<date>.json")` + `read_file("flows/hn-pain-miner/opportunities-<date>.json")`, merges, and selects the highest-scoring opportunity matching `product_angle: "info_product"` or `"template"`. This is pure coordinator logic in SOUL.md, no new flow needed.

**Option B (cleaner long-term):** Add an `opportunity-ranker` flow that consolidates both DBs into `shared/TOP_OPPORTUNITIES.json` weekly. Triggered by cron or by event after either miner runs. This is about 20 nodes and uses only existing node types.

### Phase 2 — Build the team config (1 day)

The team YAML/JSON needs these agents, each with a SOUL.md. Based on cost management for your Termux setup:

```json
FORGE (coordinator) — sonnet-4-6, persistent=true, maxTurns=60
  customTools: ["run_flow", "list_flows", "flow_status"]

scout      — sonnet-4-6, persistent=false, maxTurns=15
architect  — sonnet-4-6, persistent=false, maxTurns=15
researcher — sonnet-4-6, persistent=false, maxTurns=25  ← web_search heavy
analyzer   — sonnet-4-6, persistent=false, maxTurns=15
synthesizer— sonnet-4-6, persistent=false, maxTurns=15
writer     — sonnet-4-6, persistent=false, maxTurns=30  ← output is large
verifier   — haiku-4-5, persistent=false, maxTurns=15   ← structured audit, cheaper
optimizer  — sonnet-4-6, persistent=false, maxTurns=15
packager   — haiku-4-5, persistent=false, maxTurns=10   ← formatting, cheapest
```

The SharedWorkspace gives you GOALS/STATUS/DECISIONS/CONTEXT.md for free. CONTEXT.md becomes your STANDARDS.md — write it once with writing rules, output contracts, quality bar, format specs. Every agent gets it injected.

### Phase 3 — Build the data flows (2-3 days)

The three highest-priority flows to build next:

**`forge-topic-research`** — the most important. This is what turns "Docker container networking" into a 15-30 source corpus that the researcher agent can use. Structure: `trigger.manual` → `llm` (expand topic into 8-10 search queries) → `http_batch` (Serper.dev, your existing search integration) → `foreach` (per-result fetch via `web_fetch`) → `llm` (extract key findings per source) → `aggregate` → `file_write("shared/research.json")`. The researcher agent never needs to do web searches itself — it gets clean, pre-fetched intelligence.

**`forge-demand-scan`** — quick scoring before committing. 5 nodes: search → extract signals → LLM score → write `shared/demand-report.json`. Coordinator runs this first on any candidate topic. If score < 7, reject immediately, select next opportunity.

**`forge-format-pdf`** — terminal step. `trigger.manual` (coordinator calls it) → `bash` node running pandoc or similar → `file_write` → emit `product_complete` event. Packager calls this indirectly by telling coordinator the guide is ready; coordinator fires the flow.

### Phase 4 — The autonomous loop (post-validation)

Once Phase 1-3 is working and you've run 2-3 products through the pipeline manually, you add the autonomous mode. This is purely a FORGE SOUL.md change: instead of waiting for a human brief, FORGE wakes up on a weekly cron (or on `opportunity_mined` event from the miners), reads TOP_OPPORTUNITIES.json, applies the Build/Skip Decision Engine (Opportunity Score = Pain × Demand × Monetization × Differentiation), and kicks off the pipeline autonomously if score threshold is met. No new infrastructure. Just coordinator behavior.

---

## The Three Gaps That Actually Matter

After reading everything carefully, there are three real gaps between the factory spec and what clawd provides:

**Gap 1: No `web_fetch` batching in flows for deep research.** The `topic-research` flow needs to fetch 15-30 full pages. Your `http_batch` node handles this, but you'll want to be careful about rate limits and total timeout. Set `timeout: 3600` on the flow and use `delayMs: 1500` in the batch. This is solvable.

**Gap 2: No PDF generation node out of the box.** The `format-pdf` flow needs a bash node running pandoc (or you use the existing clawd pdf skill from the computer use context). On Termux/ARM64, pandoc is available via `pkg install pandoc`. The bash node should work. If not, pure-JS markdown-to-HTML-to-PDF via puppeteer is your fallback — but that's heavier. Simplest: have packager produce the final `.md` and use a flow with `bash` node calling a Python markdown converter you already know works on your setup.

**Gap 3: The KB — the factory spec assumes a vector KB for solution retrieval.** The `factory-team.md` spec's most powerful feature (the `retrieve_relevant()` call that reconstructs solutions from accumulated intelligence) requires a vector database. Your flow already does HDBSCAN on embeddings, so you have the tooling. The question is whether to build a persistent vector KB or just use the SQLite clusters DB plus keyword search. For the first 5-10 products, SQLite full-text search on the clusters tables is entirely sufficient. The coordinator tells the `kb-query` flow what topic to search; the flow does `SELECT * FROM clusters WHERE label LIKE ?` plus a simple TF-IDF rank. Add vector retrieval later when the KB has enough data to benefit from it.

---

## The Correct SOUL.md Structure for FORGE

This is the most important single file to get right. Based on your actual clawd primitives:

```markdown
# FORGE — Product Factory Coordinator

## Identity
You are FORGE. You run a knowledge product factory.
You don't write. You don't research. You route, gate, and enforce quality.

## Operating Modes
- **Brief Mode**: Human provides a topic → you validate and run the pipeline.
- **Autonomous Mode**: You read shared/TOP_OPPORTUNITIES.json, 
  score candidates, select the best, and run the pipeline unprompted.

## Pipeline Protocol

1. **Demand Gate** (always first)
   run_flow("forge-demand-scan", { topic }) 
   Read shared/demand-report.json. Score < 7 → REJECT, log to DECISIONS.md, 
   select next candidate or report to human.

2. **Brief Assembly**
   Write to shared/GOALS.md: the topic, target audience, core problem, 
   desired outcome, estimated price tier.
   Update STATUS.md: "Stage: SCOUT | Demand: <score>"

3. **Scout** → send_message(scout, work, brief)
   Read scout-report.md. If scope too broad: send back once. 
   If fails twice: escalate to human.

4. **Research Flow**
   run_flow("forge-topic-research", { topic, scope: scoutScope })
   Read shared/research.json. Confirm source count ≥ 15.

5. **Architect** → send_message(architect, work, { structure brief + research path })
   Read structure.md. Confirm 7-section skeleton present.

6. **Researcher Agent** → send_message(researcher, work, { structure.md + research.json path })
   (Note: researcher BUILDS the corpus from pre-fetched data, does not web search directly)
   Read raw-corpus.md.

7. **Analyzer** → send_message(analyzer, work, { corpus path })
   Read solution-matrix.md. Confidence scores present?

8. **Synthesizer** → send_message(synthesizer, work, { matrix path })
   Read synthesized-framework.md. Named framework present?

9. **Writer** → send_message(writer, work, { framework + structure paths })
   Read guide-draft.md. Word count ≥ 8000?

10. **Verifier** → send_message(verifier, work, { draft path + corpus path })
    Read audit.md. ALL scores ≥ 90%? 
    If fail: send_message(writer, revise with specific audit notes). Max 2 cycles.

11. **Optimizer** → send_message(optimizer, work, { draft + audit paths })
    Read guide-final.md.

12. **Packager** → send_message(packager, work, { final guide path + demand report })
    Read product-manifest.json. All assets present?
    run_flow("forge-format-pdf", { source: guide-final.md })

13. **stage_for_review** — present the product manifest + PDF path.
    Never publish directly.

## Quality Gates
- Demand < 7: REJECT immediately
- Research sources < 15: return to research flow
- Accuracy/Usability/Decision Quality < 90%: max 2 revisions before escalation
- Word count < 8000: send back to writer

## State Protocol
- Log every gate decision to shared/DECISIONS.md with timestamp and reasoning
- Update shared/STATUS.md at every stage transition
- Max 2 revision cycles per specialist — if exceeded, escalate to human with full details
```

---

## Summary: What to Build and In What Order

The sequencing, optimized for your Termux/mobile dev workflow:

1. **Create the team config file** — `~/.clawd/teams/product-factory/team.json` with the 10 agents above. This is JSON editing, no compilation.

2. **Write SOUL.md files** for each agent (FORGE first, then writer/verifier as the quality-critical pair). Total: ~2-3 hours of focused writing.

3. **Write shared/CONTEXT.md** — the permanent standards file. Copy the output contract and writing rules from the factory spec into clawd-friendly markdown. Every agent gets this automatically.

4. **Build `forge-demand-scan` flow** — 6 nodes, uses Serper.dev (already integrated). Quick win, validates the flow→coordinator handoff pattern.

5. **Build `forge-topic-research` flow** — 12-15 nodes, the core intelligence-gathering flow. This is the most complex new piece of infrastructure.

6. **Run the first product end-to-end in Brief Mode** — human provides a topic, FORGE coordinates manually. This validates the entire pipeline before you invest in autonomy.

7. **Add `forge-format-pdf` flow** — once you've confirmed a full product runs through successfully.

8. **Enable Autonomous Mode** — update FORGE's SOUL.md, add the opportunity-reading logic, set a weekly cron or wire an event from the miners to trigger FORGE.

The entire factory is buildable with zero new clawd code. The flow node types you need (`http_batch`, `llm`, `sqlite_exec`, `python`, `bash`, `file_write`, `foreach`, `quota_gate`) are all already registered in `src/flow/nodes/registry.ts`. The team primitives (`send_message`, `run_flow`, `stage_for_review`, SharedWorkspace) are all live. The intelligence layer (two miners, SQLite opportunity databases) is already running.

You're building on a complete foundation. The factory isn't a new project — it's a deployment target for infrastructure you've already shipped.


######

Let me read the v9.0 spec carefully before evaluating.

Good. Now I have the full picture. Here's the deep evaluation.

---

# v9.0 Flow Integration Evaluation — Full Analysis

## How the Spec Defines Each Phase and What It Actually Implies for Execution

The critical question for each phase is: **is this work data-volume work, or is it reasoning work?** The two flow files you shipped are the reference model — they handle 100-200 posts per run, do embedding, clustering, LLM classification per item, and produce a scored JSON. That's the bar for what a flow should do.

Here's the v9.0 phase-by-phase breakdown:

---

### Phase -1 — Market Signal Detection

**What the spec says:** System continuously scans Reddit, StackOverflow, GitHub issues, product reviews, YouTube comments, competitor gaps. Outputs `OPPORTUNITY_POOL.json` with frequency score, pain intensity, monetization potential, audience size.

**Honest assessment:** This is 100% flow territory. You've already built 60-70% of it. `reddit-pain-miner` and `hn-pain-miner` are both operational instances of exactly this phase.

**The gaps vs what you have:**
- Reddit ✅ (done)
- HN ✅ (done)
- StackOverflow ❌ — needs a new flow. SO has a public API (`api.stackexchange.com/2.3/questions?tagged=X&sort=votes`). Same pattern as HN: fetch → filter by votes → classify → embed → cluster → label. About 80% the same code as `hn-pain-miner`.
- GitHub issues ❌ — GitHub API (`/repos/{owner}/{repo}/issues?state=open&sort=comments`). Biggest repos per tech stack. Similar pattern.
- Product reviews ❌ — scraping G2/Capterra/AppSumo is harder (no clean API, needs browser or HTML parse). This is a medium-effort flow.
- YouTube comments ❌ — YouTube Data API v3. Feasible but requires API key. Medium.
- Search intent ❌ — Serper.dev autocomplete or "People Also Ask" scraping. Lightweight flow.

**Integration verdict:** All of Phase -1 should be flows. Each source is a separate flow with the same internal structure as your existing miners. They all write to their own SQLite DB and emit `opportunity_mined` event on completion.

---

### Phase 0 — Autonomous Brief Generation

**What the spec says:** Cluster signals from the opportunity pool, define product angle, do economic pre-validation (willingness to pay, time saved, competition), output `AUTO_PRODUCT_BRIEF.md`. Also contains the Build/Skip Decision Engine: `Opportunity Score = Pain × Demand × Monetization × Differentiation`.

**The key question:** Is the scoring formula computational or reasoning-based?

The first part — **reading the opportunity pool, merging scores, computing the composite formula, and filtering by threshold** — is deterministic. Pure flow: `sqlite_exec` (read opportunities from all miners), `javascript` (score = pain × demand × monetization × differentiation), `filter` (score > threshold), `sort`, `file_write` → `shared/TOP_OPPORTUNITIES.json`. No LLM needed for this part.

The second part — **clustering signals into coherent product angles, estimating willingness to pay, checking competitor saturation** — requires judgment. These are not computable from structured fields alone. An agent needs to reason: "These 3 opportunity clusters are all variants of the same underlying problem — they should be one product, not three." Or: "This opportunity looks high-score but the market is saturated — I've seen 5 similar products already." That's FORGE's job.

**The split:**
- `opportunity-consolidator` flow: merge all miner outputs, apply the numeric formula, produce `TOP_OPPORTUNITIES.json` with pre-computed scores → 8-10 nodes, pure data.
- FORGE (agent): reads `TOP_OPPORTUNITIES.json`, reasons about clustering, saturation, differentiation angle, writes `AUTO_PRODUCT_BRIEF.md` to `shared/GOALS.md`.

**Integration verdict:** Phase 0 = hybrid. The mechanical scoring is a flow. The strategic brief generation is FORGE.

---

### Phase 1 — Intelligence Gathering

**What the spec says:** 15-30 sources across docs, forums, GitHub, tutorials, videos. Output: `RAW_DATA_CORPUS.md` with source inventory, raw findings by topic, contradictions, gaps.

**Volume analysis:** 15-30 pages fetched, each chunked into findings. This is exactly the scale where agents start to fail — they run out of context window, they hallucinate source attributions, they skip sources when the context gets heavy. The spec itself acknowledges this is multi-source parallel work.

**The right model:**
- `forge-topic-research` flow: takes topic + scope → generates 8-10 search queries (one `llm` node) → `http_batch` on Serper.dev → `foreach` per result → `web_fetch` per URL → `llm` node per page (extract key findings, quotes, anti-patterns) → `aggregate` all findings → `file_write("shared/research-raw.json")`.
- This is identical in structure to the miner flows but for deep-fetching instead of post-scraping.

Then the **researcher agent** receives `research-raw.json` — clean, structured, all source attributions preserved — and writes `RAW_DATA_CORPUS.md` in the 7-section format with source inventory table, contradictions analysis, gaps. The agent does the synthesis and formatting; the flow did the fetching.

**Why not let the researcher agent do the fetching directly?** Because 15-30 web_fetch calls in a single agent session: (a) blows the context window with raw HTML, (b) loses deterministic source attribution, (c) can't be checkpointed, (d) costs significantly more at sonnet rates vs haiku for the extraction nodes.

**Integration verdict:** Phase 1 = flow for data acquisition, agent for corpus structuring. The flow can use haiku-4-5 for per-page extraction (cheap), sonnet only where needed.

---

### Phase 2 — Solution Mining & Extraction

**What the spec says:** Pattern recognition across sources, best practice extraction, contradiction identification, consensus building. Output: `SOLUTION_MATRIX.md` with frequency/consensus/complexity/effectiveness scores per solution approach.

**Volume analysis:** Input is `RAW_DATA_CORPUS.md` (one structured document). The Analyzer agent reads one file and produces one analysis. This is pure reasoning work — no volume, no batching, no data movement. The agent needs to read across 15-30 source summaries and identify which solutions appear in multiple sources, which contradict, which have consensus.

There's no meaningful flow to build here. The "pattern recognition" is LLM reasoning against a document. A flow would just be a single `llm` node reading the file — at which point you've just added overhead for no benefit. Do this entirely in the analyzer agent.

**Integration verdict:** Pure agent. No flow needed.

---

### Phase 3 — Traceable Synthesis

**What the spec says:** Framework creation, methodology design, step consolidation, named framework, decision trees. Output: `SYNTHESIZED_FRAMEWORK.md` with framework name, core philosophy, N-step system, decision tree, methodology comparison.

**Same as Phase 2:** Input is one document, output is one document, the work is reasoning. No volume, no batching. The synthesizer agent receives `SOLUTION_MATRIX.md` and reasons its way to an original framework.

**The one exception:** The spec mentions "parallel subtasks" in the automation upgrade — evaluating multiple approaches in parallel. This *could* be a mini-flow that fans out to 3-4 `llm` nodes evaluating different framework angles simultaneously, then a merge node picks the best. But in practice, this is low-value complexity for this phase — the synthesizer agent can do this in a multi-turn loop more flexibly.

**Integration verdict:** Pure agent.

---

### Phase 4 — Content Engineering

**What the spec says:** 7-section structure, value-dense writing, Hook Engine (headline + transformation promise + unique mechanism), Differentiation Engine (named framework + decision system + comparative advantage). Output: `DRAFT_EBOOK.md` (8,000-15,000 words).

**The hidden volume problem:** 15,000 words in a single agent session is near or at the output limit for a single turn. The writer needs to produce this in chunks. This is where a structural flow can help — not for intelligence processing, but for output management.

**The right model:** A `forge-chapter-writer` flow that takes `STRUCTURE.md` and iterates: foreach section → `llm` node (write section N, given framework + section brief + word target) → `file_write` per section → final `aggregate` to assemble `DRAFT_EBOOK.md`. This produces each section independently, keeps each LLM call focused, and allows section-level checkpointing. The writer agent then does a pass-through review for voice consistency and transition quality — it reads the assembled draft and patches seams and tone issues, which is a focused reasoning task.

Alternatively — and this is valid — you skip the flow and give the writer agent 30 maxTurns with explicit section-by-section instructions. The agent writes section 0, saves it, writes section 1, etc. This is simpler to implement and still keeps outputs clean. The flow only wins if you need parallelism (write multiple sections simultaneously) or if the writer keeps running into context limits.

**The Hook Engine and Differentiation Engine** from the v9.0 spec: these are pre-writing generation steps. They fit naturally as the first 2-3 turns of the writer agent session, not as a separate flow. Writer receives brief → generates hooks/differentiators → writes. That's a focused session, not a data processing task.

**Integration verdict:** Primarily agent. Optional `forge-chapter-writer` flow for section-by-section generation if context limits become a real problem in practice — but defer this until you hit the problem, not before.

---

### Phase 5 — Multi-Layer Verification

**What the spec says:** 3 layers — accuracy validation (source traceability, cross-reference, citation integrity), usability simulation (can a beginner follow this?), decision validity check (are trade-offs real?). Output: `VERIFICATION_REPORT.md` with three scores, all must be ≥90%.

**Volume question:** The verifier reads one document (`DRAFT_EBOOK.md`, ~15,000 words). This is at the edge of comfortable context for a single turn. A structural flow could help: split the draft into sections, verify each section independently in parallel, then aggregate the scores.

**`forge-verify-sections` flow:** `split` node (sections of the draft) → `foreach` with `concurrency: 3` → `llm` node per section (verify accuracy + flag issues) → `aggregate` → `llm` node (final score computation + VERIFICATION_REPORT assembly). This parallelizes verification and keeps each LLM call focused on one section.

However — the usability simulation and decision validity checks require reading the *whole document* for coherence. You can't verify "does the progression make sense?" by looking at one section. So the complete flow would be: section-level accuracy in parallel (flow) + whole-document usability/decision check (verifier agent reading the flow's output report). That's the cleanest split.

**Integration verdict:** Hybrid. `forge-verify-sections` flow for parallel per-section accuracy audit. Verifier agent for usability simulation and decision validity (whole-document reasoning). Verifier agent reads flow output and writes the final consolidated `VERIFICATION_REPORT.md`.

---

### Phase 6 — Publishing + Distribution

**What the spec says:** PDF generation, cover design, landing page copy, sales page, email funnel, social threads, deployment to Gumroad/Lemon Squeezy.

**Clear split:**
- PDF generation → `forge-format-pdf` flow (bash node, pandoc, deterministic) ✅
- Cover metadata/specification → packager agent (reasoning about title, subtitle, value prop)
- Landing page copy, sales page, email funnel, social threads → packager agent with sub-delegation to writer if needed (these are LLM creative tasks)
- Deployment to Gumroad/Lemon Squeezy → these require API calls with authentication. A `forge-publish` flow handles this: `http` nodes to Gumroad API + Lemon Squeezy API, attaches the PDF, sets price from the demand report, writes listing. Pure automation, zero reasoning needed.

**Integration verdict:** Hybrid. `forge-format-pdf` and `forge-publish` flows. Packager agent for all creative/marketing copy generation.

---

### Phase 7 — Feedback Ingestion

**What the spec says:** Collect reviews, refund reasons, engagement metrics, completion rates. Output: `FEEDBACK_DATA.json`.

**This is almost entirely flow territory.** Polling Gumroad API for sales/reviews → classify reviews (positive/negative/refund) → extract reasons → store in `feedback.db`. This runs on a schedule (daily or weekly). Zero reasoning required at collection time.

**Integration verdict:** Pure flow. `forge-feedback-collector` — cron-triggered, Gumroad/LemonSqueezy API poll → classify → store.

---

### Phase 8 — Learning & Optimization Engine

**What the spec says:** Topic selection optimization (what sells, what fails), framework evolution (which structures perform better), writing style adaptation, pricing optimization. Memory structure includes `opportunity_history`, `success_patterns`, `failure_patterns`, `pricing_performance`, `audience_segments`.

**The hardest phase to classify correctly.** The spec calls this an "agent" (Meta-Learning Engine). But what does it actually do?

The *computational* part — "product X with framework type Y and price $Z had conversion rate W" — is pure SQL aggregation. A `forge-learning-update` flow reads `feedback.db` + `products.db`, computes stats, updates `MEMORY.json`. No reasoning needed for the data aggregation.

The *reasoning* part — "based on patterns, the system should change its topic selection criteria and writing style preferences" — is where an agent is genuinely needed. The meta-learning agent reads `MEMORY.json` (the stats), reasons about what patterns they imply, and writes updated guidance to `shared/CONTEXT.md`. This is the key: **CONTEXT.md is the living standards document**. When the meta-learner updates it, every future agent session gets the new guidance injected automatically. This is the learning flywheel in concrete form.

**Integration verdict:** Hybrid. `forge-learning-update` flow for statistical aggregation. Meta-learner agent for pattern interpretation and CONTEXT.md updates. Runs after each product cycle.

---

## Complete Phase


Same v9.0 spec — confirmed. Now let me complete the full evaluation I was mid-way through.

---

# v9.0 → clawd Hybrid Integration: Complete Phase-by-Phase Map

## The Governing Principle

Before going through each phase, one rule to lock in firmly:

**A task belongs in a flow if:** it processes multiple items, is structurally repetitive, benefits from checkpointing, doesn't require cross-item judgment, and would bloat an agent's context window with raw data.

**A task belongs in an agent if:** it requires reading something once and reasoning about it, making a qualitative judgment, writing an output that requires voice/creativity, or deciding between options based on nuanced criteria.

This is the exact same principle your two existing flows already embody. The reddit and HN miners never "think" — they process, classify, embed, cluster, and score. Thinking happens when FORGE reads their output.

---

## Phase-by-Phase Verdict

### Phase -1 — Market Signal Detection
**Verdict: 100% Flow layer**

This is the most natural fit in the entire spec. The v9.0 spec describes it as an "Agent: Signal Miner" but that's a naming choice, not an architectural requirement. What it actually does — scrape sources, classify posts, embed, cluster, score, persist — is identical to what your two existing flows already do. You've already built Phase -1 twice.

**What you have vs what's missing:**

| Source | Status | Flow needed |
|--------|--------|-------------|
| Reddit | ✅ `reddit-pain-miner` | done |
| Hacker News | ✅ `hn-pain-miner` | done |
| StackOverflow | ❌ | `so-pain-miner` — SO has a clean public API (`api.stackexchange.com/2.3/questions`), same pattern as HN, ~80% code reuse |
| GitHub Issues | ❌ | `github-issue-miner` — GitHub REST API, filter by comment count, same classify→embed→cluster pipeline |
| Product Reviews | ❌ | `review-miner` — G2/AppSumo scraping, harder (no API), medium effort |
| YouTube Comments | ❌ | `yt-comment-miner` — YouTube Data API v3, needs key |
| Search Intent | ❌ | `search-intent-miner` — Serper.dev "People Also Ask" extraction, lightest of all, ~8 nodes |

All five missing miners share the same internal DAG as your existing flows. Build `so-pain-miner` first — it's the closest to `hn-pain-miner` structurally and gives you the widest developer audience signal coverage.

**The consolidation step:** After miners run, a separate `opportunity-consolidator` flow merges all SQLite DBs, normalizes scores across sources, deduplicates overlapping opportunities (same problem detected on Reddit and SO → one entry, higher confidence), and writes `shared/TOP_OPPORTUNITIES.json`. This is pure `sqlite_exec` + `javascript` + `file_write`. No LLM needed. It emits an `opportunities_ready` event that FORGE can listen to.

---

### Phase 0 — Autonomous Brief Generation + Build/Skip Decision Engine
**Verdict: Hybrid — flow for scoring, FORGE for strategy**

The spec defines two distinct sub-tasks here that have different natures:

**Sub-task A — Numeric scoring:** `Opportunity Score = Pain × Demand × Monetization × Differentiation`. All four factors are computable from the structured fields in `TOP_OPPORTUNITIES.json` (pain_intensity, opportunity_score, monetization_angle, cluster_size). This is 3 nodes: `sqlite_exec` or `file_read` → `javascript` (formula) → `filter` (threshold) → sorted output. Flow. No LLM.

**Sub-task B — Strategic brief writing:** Clustering related opportunities into one product angle, estimating competition saturation, choosing beginner vs advanced framing, estimating price tier. This requires reasoning across the opportunity pool, cross-referencing against `MEMORY.json` (what has already been built, what failed), and making a qualitative call. FORGE reads the scored opportunities and writes `AUTO_PRODUCT_BRIEF.md` to `shared/GOALS.md`. Pure agent work.

The key insight: **the flow tells FORGE what the numbers say. FORGE decides what to do.** FORGE never touches raw opportunity data — it only reads pre-scored, pre-filtered candidates.

---

### Phase 1 — Intelligence Gathering
**Verdict: Flow for data acquisition, agent for corpus structuring**

The spec requires 15-30 sources. This is the phase where doing it purely in an agent session causes real problems: context window fills with raw HTML, per-source LLM calls at sonnet rates get expensive, and you can't checkpoint mid-fetch.

**`forge-topic-research` flow:**
```
trigger.manual (topic, scope, depth_level)
  → llm [haiku] (expand topic into 8-12 search queries)
  → http_batch [Serper.dev] (parallel search, all queries)
  → javascript (extract top 3 URLs per query, deduplicate → 15-30 URLs)
  → foreach [concurrency: 3]
      → web_fetch (full page content)
      → llm [haiku] (extract: key findings, quotes, solution hints, 
                     anti-patterns, source type, reliability estimate)
  → aggregate (collect all per-source findings)
  → python (deduplicate findings, sort by reliability)
  → file_write → shared/research-raw.json
  → emit research_complete
```

The haiku LLM nodes here do extraction only — they're cheap and fast. The researcher agent then receives `research-raw.json` (clean, structured, all attributions preserved) and writes `RAW_DATA_CORPUS.md` with the source inventory table, contradictions analysis, and gaps identification. That structured analysis is the reasoning step.

**Why this split pays off:** The flow handles the 15-30 fetch+extract operations cheaply. The researcher agent does one focused reasoning pass on structured input instead of wrestling with raw HTML across 30 URLs. Per-source extraction at haiku rates vs having sonnet manage the whole fetch sequence — significant cost difference at scale.

---

### Phase 2 — Solution Mining & Extraction
**Verdict: Pure agent**

Input: one `RAW_DATA_CORPUS.md`. Output: one `SOLUTION_MATRIX.md`. No volume, no batching. The analyzer reads across source summaries and reasons about frequency, consensus, contradiction patterns. This is exactly what the agent session is built for — one document in, one structured analysis out.

A flow here would just be: `file_read` → `llm` → `file_write`. That's not a flow, that's overhead. The analyzer agent does this natively with better context retention across the reasoning steps.

---

### Phase 3 — Traceable Synthesis
**Verdict: Pure agent**

Same as Phase 2. One document in (`SOLUTION_MATRIX.md`), one framework out (`SYNTHESIZED_FRAMEWORK.md`). The synthesizer needs to hold the entire solution matrix in mind while designing the named framework, creating the decision tree, and resolving contradictions. That's sustained multi-step reasoning, not data processing.

The v9.0 spec's "parallel subtasks" note — evaluating multiple framework angles simultaneously — could theoretically be a mini fan-out flow, but in practice a synthesizer agent with 15 turns can generate 3 candidate frameworks, self-evaluate them, and pick the strongest. More flexible, simpler, and avoids the coordination overhead of a parallel flow for a task with 3 items.

---

### Phase 4 — Content Engineering
**Verdict: Primarily agent, with optional section-writer flow for long output management**

The Hook Engine (headline + transformation promise + unique mechanism) and Differentiation Engine (named framework + decision system + comparative advantage) are the first 2-3 turns of the writer's session. They're creative reasoning tasks that benefit from having the full brief in context. No flow.

The actual writing — 8,000-15,000 words across 7 sections — is where you need to be thoughtful. A single agent turn can't reliably produce 15,000 coherent words. The writer needs to work section by section.

**Two valid approaches:**

Option A (simpler): Writer agent with 30+ maxTurns. SOUL.md instructs it to write one section at a time, save each to a named file (`section-0-quickstart.md`, etc.), then assemble. Coordinator reads the assembled draft. This works fine and is simpler to implement.

Option B (flow, better at scale): `forge-section-writer` flow — takes `STRUCTURE.md` + `SYNTHESIZED_FRAMEWORK.md` → `split` (7 sections) → `foreach [concurrency: 2]` → `llm [sonnet]` per section (write section with word target + voice guidelines from CONTEXT.md) → `aggregate` → `file_write("guide-draft.md")`. This parallelizes writing, enforces word targets per section, and produces a predictable output in less wall-clock time.

Recommendation: start with Option A. Move to Option B if the writer agent consistently runs into context or turn limits in practice.

---

### Phase 5 — Multi-Layer Verification
**Verdict: Hybrid — flow for parallel accuracy audit, agent for usability + decision validity**

The spec defines 3 verification layers:
1. **Accuracy validation** — source traceability, cross-reference, citation integrity. This is mechanical and can be parallelized per section.
2. **Usability simulation** — can a beginner follow this? Are implicit assumptions exposed? Requires reading the whole document for coherence.
3. **Decision validity** — are trade-offs real and fairly represented? Requires whole-document reasoning.

Layers 2 and 3 cannot be done per-section — they require whole-document understanding. Layer 1 can be parallelized.

**`forge-verify-accuracy` flow:**
```
trigger.manual (draft_path)
  → file_read → python (split into sections)
  → foreach [concurrency: 3]
      → llm [haiku] (check: every claim has source attribution,
                     no commands that don't match any cited source,
                     no version numbers that conflict across sources)
      → javascript (extract: issues[], confidence_score)
  → aggregate
  → python (compute overall accuracy score, merge all issues)
  → file_write → shared/accuracy-report.json
```

The verifier agent then reads `accuracy-report.json` + the full `guide-draft.md` and does the usability simulation and decision validity passes, then writes the consolidated `VERIFICATION_REPORT.md` with all three scores. If accuracy < 90%, it flags the specific sections and FORGE routes back to writer with the flagged issues.

---

### Phase 6 — Publishing + Distribution
**Verdict: Flow for mechanical operations, packager agent for creative assets**

Clear split:

**Flow — `forge-format-pdf`:** bash node → pandoc (or Python markdown converter) → output PDF. Deterministic, zero reasoning. Runs after packager completes.

**Flow — `forge-publish`:** HTTP nodes → Gumroad API (create product, upload PDF, set price from demand-report) + Lemon Squeezy API. Pure automation. Packager agent provides the product manifest; the flow handles the API calls.

**Packager agent:** Receives `guide-final.md` + `demand-report.json` → generates landing page copy, sales page, email sequence, social threads, cover metadata, pricing recommendation. All creative/LLM work.

---

### Phase 7 — Feedback Ingestion
**Verdict: Pure flow**

Cron-triggered `forge-feedback-collector`:
```
trigger.cron (daily, 6am)
  → http [Gumroad API] (get sales, reviews, refunds since last run)
  → http [LemonSqueezy API] (same)
  → javascript (normalize response formats)
  → foreach
      → classify [haiku] (review sentiment: positive/negative/refund)
      → llm [haiku] (extract: main complaint or praise, one sentence)
  → aggregate
  → sqlite_exec (INSERT into feedback.db)
  → javascript (compute: conversion_rate, avg_rating, refund_rate)
  → file_write → shared/feedback-summary.json
  → emit feedback_ingested
```

No reasoning required. All classification at haiku rates. The meta-learner agent reads `feedback-summary.json` in Phase 8.

---

### Phase 8 — Learning & Optimization Engine
**Verdict: Hybrid — flow for statistical aggregation, meta-learner agent for pattern interpretation**

**`forge-learning-update` flow** (triggered by `feedback_ingested` event):
```
sqlite_exec (SELECT product metrics, feedback, opportunity_history)
  → python (compute: success_patterns, failure_patterns, 
            avg_conversion_by_topic_category, avg_conversion_by_price_tier,
            framework_type_performance, avg_refund_by_audience_segment)
  → javascript (build MEMORY.json delta: what changed since last run)
  → file_write → shared/MEMORY.json
  → emit memory_updated
```

**Meta-learner agent** (triggered by `memory_updated`):
Reads `MEMORY.json` + current `shared/CONTEXT.md` → reasons about what the patterns imply for future product decisions → writes updated guidance back to `shared/CONTEXT.md`.

This is the learning flywheel's concrete mechanism: **CONTEXT.md is the living standards document injected into every agent session**. When the meta-learner updates it — "avoid Docker topics, saturation detected" or "step-by-step framework outperforms conceptual frameworks for this audience" — every future factory run automatically incorporates that knowledge. No manual prompt engineering required.

---

## Complete Integration Map

Here's the full picture in one place:

```
PHASE -1: MARKET SIGNAL DETECTION
  ├── reddit-pain-miner      [flow, cron daily 2am]     ✅ DONE
  ├── hn-pain-miner          [flow, manual]              ✅ DONE
  ├── so-pain-miner          [flow, cron daily 3am]      🔨 BUILD NEXT
  ├── github-issue-miner     [flow, cron weekly]         📋 PLANNED
  ├── search-intent-miner    [flow, cron weekly]         📋 PLANNED
  └── opportunity-consolidator [flow, event: *_mined]   🔨 BUILD NEXT

PHASE 0: BRIEF GENERATION
  ├── opportunity-scorer     [flow — formula, filtering] 🔨 BUILD
  └── FORGE                  [agent — strategy, brief]   📝 SOUL.md

PHASE 1: INTELLIGENCE GATHERING
  ├── forge-topic-research   [flow — fetch+extract]      🔨 BUILD
  └── researcher             [agent — corpus structuring] 📝 SOUL.md

PHASE 2: SOLUTION ANALYSIS
  └── analyzer               [agent — pure reasoning]    📝 SOUL.md

PHASE 3: SYNTHESIS
  └── synthesizer            [agent — pure reasoning]    📝 SOUL.md

PHASE 4: CONTENT ENGINEERING
  ├── forge-section-writer   [flow — optional, later]    📋 DEFER
  └── writer                 [agent — primary]           📝 SOUL.md

PHASE 5: VERIFICATION
  ├── forge-verify-accuracy  [flow — parallel per-section] 🔨 BUILD
  └── verifier               [agent — usability + decisions] 📝 SOUL.md

PHASE 6: PUBLISHING
  ├── forge-format-pdf       [flow — pandoc bash node]   🔨 BUILD
  ├── forge-publish          [flow — Gumroad/LS API]     📋 PLANNED
  └── packager               [agent — marketing copy]    📝 SOUL.md

PHASE 7: FEEDBACK INGESTION
  └── forge-feedback-collector [flow, cron daily]        📋 PLANNED

PHASE 8: LEARNING ENGINE
  ├── forge-learning-update  [flow — stats aggregation]  📋 PLANNED
  └── meta-learner           [agent — CONTEXT.md updates] 📝 SOUL.md
```

**Legend:**
- ✅ DONE — already shipped
- 🔨 BUILD NEXT — highest priority, needed to run first product
- 📝 SOUL.md — agent, needs team config + soul file
- 📋 PLANNED — build after first end-to-end run validates the pattern

---

## The Minimum Viable Factory

To run your first product end-to-end, you need exactly:

**Flows (new):** `opportunity-consolidator`, `opportunity-scorer`, `forge-topic-research`, `forge-verify-accuracy`, `forge-format-pdf`

**Team config + SOUL.md files:** FORGE, researcher, analyzer, synthesizer, writer, verifier, optimizer, packager

**Shared files:** `CONTEXT.md` (standards, writing rules, output contracts)

Everything else — the additional miners, feedback collection, learning engine, publish flow — builds on top of a validated working pipeline. The architecture is sound. The primitive-to-phase mapping is clean. And critically, every flow you need uses only node types already registered in clawd's registry. Zero new infrastructure code required.


##$###

This is a deep review request — let me read the spec one more time with fresh critical eyes before writing the analysis.

Now let me read the earlier versions in the product-factory.md for fuller context on what evolved and what was carried forward uncritically.

Good. I have everything I need. This is the honest critical review.

---

# Honest Critical Review: v9.0 Master Spec

Let me be direct about what this spec gets right, what it gets wrong, and where the gaps between ambition and reality are the most dangerous.

---

## What the Spec Gets Genuinely Right

Before the critique, the things that deserve credit.

**The departmental isolation principle** (from v7.5, carried into v9.0) is the best idea in the entire spec. Research never synthesizes. Analyzer never writes. Writer never researches. This is sound software architecture thinking applied to agent design — it limits each agent's context, prevents role confusion, and makes each agent's output auditable. This is worth keeping unconditionally.

**The 7-section ebook structure** is a real, usable output framework. It's opinionated in the right ways — Quick Start first is smart (immediate value), progressive disclosure from landscape to advanced techniques matches how practitioners actually read technical guides. This is solid product design.

**The three-mode operating model** (Fully Autonomous, Semi-Autonomous, Manual Override) is the right way to frame deployment risk. A system that can *only* run fully autonomously would be dangerous to ship. Having these three modes explicitly acknowledged is good.

**Phase -1's signal taxonomy** (Pain, Friction, Demand, Gap, Inefficiency) is well-observed. These five types map to real behavior patterns in technical communities. You've already implemented this in your flows — the classification labels in your reddit/HN miners reflect the same taxonomy.

---

## Critical Problem 1: The Autonomy Claim is Architecturally Ungrounded

This is the most important critique.

v9.0's headline claim is: *"The system does not wait for problems — it detects, validates, prioritizes, and solves them autonomously."*

This sounds powerful. But read what the spec actually defines for Phase -1 and Phase 0, and ask: **where exactly does human judgment get removed, and what replaces it?**

Phase -1 produces an `OPPORTUNITY_POOL.json` with pain scores and monetization potential. Phase 0 runs a formula: `Opportunity Score = Pain × Demand × Monetization × Differentiation`.

Here's the problem: **Differentiation is not computable from forum scraping data.** The formula has four factors. Three of them (Pain, Demand, Monetization potential) are rough proxies derivable from signal frequency and classifier outputs. But Differentiation — whether your product would be genuinely different from what already exists — requires knowing what already exists in the market. The spec never defines how Differentiation is measured or sourced. It's listed as a factor in the formula but has no data pipeline feeding it.

This means the Build/Skip Decision Engine, which is presented as the economic brain of v9.0, is computing `Score = known × known × known × undefined`. In practice, the system will either ignore Differentiation (turning it into a constant that distorts the score) or hallucinate a value for it. Neither is acceptable for a decision with production cost implications.

**What should replace it:** The Differentiation factor needs an explicit data source — a competitor scan flow that searches for existing guides/products on the identified topic, counts them, reads their positioning, and returns a saturation score. This is buildable. But it's missing from the spec entirely.

---

## Critical Problem 2: The Opportunity Scoring Formula is Naive

`Opportunity Score = Pain × Demand × Monetization × Differentiation`

Multiplicative formulas with four uncalibrated factors have a known failure mode: **extreme values in one factor dominate the product**. If Pain = 10 and Demand = 10 but Monetization = 1 (e.g., a problem everyone has but nobody pays to solve), the score is 100 × Differentiation — still high. The system would greenlight it.

The inverse is worse: a highly monetizable topic (Monetization = 10) with low pain signal (Pain = 2) scores 2 × Demand × 10 × Differentiation — potentially still high enough to proceed, even though low pain means users don't feel urgent need to buy a guide.

The spec sets thresholds as HIGH/MEDIUM/LOW with no numeric definitions. What is HIGH? What threshold separates MEDIUM from LOW? This is entirely unspecified. In implementation, this gets filled in arbitrarily by whoever writes the LLM prompt, making the "Decision Engine" label misleading — it's just a prompt instruction dressed as a formula.

**What should replace it:** A weighted additive model with empirically calibrated weights, explicit numeric thresholds, and a minimum-floor rule (any factor below floor = automatic reject regardless of total score). Example: `Score = (0.35 × Pain) + (0.30 × Demand) + (0.20 × Monetization) + (0.15 × Differentiation)`. Reject if Pain < 3 OR Demand < 3 regardless of total. This is less impressive-sounding but dramatically more reliable.

---

## Critical Problem 3: Phase 1's Source Count Requirement is a False Quality Gate

The spec mandates 15–30 sources across ≥5 source types. If fewer than 15 sources are found, return to Phase 1.

This sounds rigorous. It isn't.

**Source count is not a proxy for information quality.** For a narrow, well-documented topic (e.g., "configuring Nginx reverse proxy for Node.js"), 5 excellent sources covering the full solution space are worth more than 20 sources where 15 of them say the same thing. Conversely, for an emerging topic, 15 sources might not exist — and forcing the system to find them leads to source padding: including low-quality pages, tangentially related content, or duplicate sources from the same domain just to hit the number.

The deeper issue: **the 15-source rule creates a perverse incentive to prioritize source count over source quality**. A system trying to meet this gate will grab whatever it can find, inflating the corpus with noise that then propagates through every downstream phase.

**What should replace it:** Replace the source count gate with a coverage gate. The Research agent should verify that the corpus covers: (a) at least 2 independent explanations of the core solution, (b) at least 1 source addressing failure modes, (c) at least 1 source with working code/commands, (d) at least 1 source showing version/environment context. These four coverage requirements are meaningful. Source count is not.

---

## Critical Problem 4: The Self-Critique Loop is Circular

Phase 5 in v9.0 introduces a "Self-Critique Loop" where the system asks itself: *"What is weak here? What is unclear? What would confuse a beginner?"* Then auto-corrects.

This is the most conceptually flawed part of the spec.

Self-critique by the same model that produced the content has a fundamental limitation: **the model's blind spots in production are the same blind spots in critique**. If the writer agent made an assumption that was invisible to it (e.g., assumed the reader has Docker installed, never mentioned it), the same model asking "what would confuse a beginner?" will likely not surface that assumption — because it was invisible to the writer for the same reason it would be invisible to the critic.

This is not a theoretical concern. Research on LLM self-evaluation consistently shows that self-critique improves surface-level issues (grammar, structure, completeness of explicitly requested elements) but fails to catch the errors it most needs to catch — the ones the model couldn't see in the first place.

**What should replace it:** The verification phase needs a *role inversion*, not self-critique. Instead of the verifier asking "what's wrong with this document," give the verifier agent a specific adversarial identity: "You are a developer with 3 months of experience who has never used [topic technology]. You are following this guide for the first time. Document every moment where you are confused, every assumption made without explanation, every command that requires prior knowledge not provided." This is a different cognitive frame that surfaces different categories of problems.

Additionally, the verifier should compare the guide's claimed solution against the original pain signals from Phase -1. A guide that technically answers the question asked but doesn't address the actual frustration documented in the signal corpus has failed even if it's technically accurate.

---

## Critical Problem 5: The Learning Flywheel Has No Cold Start Strategy

Phase 8 is described as the system's most powerful feature — a learning engine that optimizes topic selection, framework design, writing style, and pricing based on performance data.

The spec never addresses the cold start problem: **the system cannot learn until it has data, and it has no data until it has shipped products**. The first 5-10 products are produced with no learning signal at all. More importantly, there's no strategy for what happens during this period — the spec simply assumes the learning engine is operational from day one.

This is a significant gap because the system's early decisions (which topics to pursue, what price to set) are the ones made with the least information, under the most uncertainty. The learning engine is most needed early but is least useful early.

**What should replace it:** An explicit bootstrapping strategy:
- Products 1-3: Manual Override Mode only. Human provides brief. Purpose is to validate the pipeline end-to-end, not to make good autonomous decisions.
- Products 4-10: Semi-Autonomous Mode. System generates briefs; human approves/rejects with brief written rationale. The rationale is ingested as pre-seed learning data.
- Products 11+: Autonomous Mode becomes available, now with actual performance data and human rationale to learn from.

The spec should specify a minimum product count before Phase 8 has meaningful signal — probably 10-15 completed products — and explicitly acknowledge that before that threshold, human oversight is not optional, it's required for system health.

---

## Critical Problem 6: Feedback Ingestion Assumes Metrics That Don't Exist Yet

Phase 7 lists these feedback sources: reviews, refund reasons, engagement metrics, completion rates.

For a Gumroad/Lemon Squeezy product, you get: sales count, revenue, and customer reviews (text). That's it. You do not get:
- **Completion rates** — there's no delivery mechanism that tracks whether someone finished reading the PDF.
- **Engagement metrics** — not available for a downloaded file.
- **Refund reasons** — available only if the customer explicitly writes one, which most don't.

The spec assumes a SaaS-level instrumentation layer that doesn't exist for a PDF product sold on a marketplace. Two of the four listed data sources are either unavailable or extremely sparse in the product context described.

**What should replace it:** Be honest about what data is actually collectable. Design the feedback loop around what you *can* get: sales velocity (how many sold in first 7 days vs first 30 days), refund rate (the ratio, not the reasons), and review sentiment (classifiable). For completion and engagement, the only realistic path is an optional post-download survey — a single question ("Did you solve your problem with this guide? Yes/Partially/No") linked from the product delivery email. Low response rate expected, but even 10% response gives a signal.

---

## Critical Problem 7: The Pipeline is Strictly Linear in a Domain That Isn't

The spec defines a strict linear DAG: Phase -1 → Phase 0 → Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6 → Phase 7 → Phase 8.

Technical content creation is not linear. The most common real failure pattern is: you get to Phase 4 (writing) and discover the synthesized framework from Phase 3 has a gap — a whole category of user problems it doesn't address that the writer notices while trying to write about them. In a linear pipeline, this requires going all the way back to Phase 3 (and potentially Phase 1 if the gap is a missing source type). But the spec's iteration model doesn't address backward jumps beyond one phase.

More critically: **the spec defines maximum revision cycles only for Phase 5** (verifier sends back to writer, max 2 cycles). What happens when the synthesizer produces a weak framework and the writer rejects it? What happens when Phase 1 produces a corpus that the analyzer deems insufficient for solution extraction? These backward-loop conditions exist in every real pipeline run but are not specified.

**What should replace it:** Explicit backward-loop rules for each quality gate, not just Phase 5. Each phase should define: (a) what conditions trigger a backward loop, (b) exactly which phase it returns to, (c) the maximum loop count before human escalation. The pipeline is not a waterfall — it's a DAG with bidirectional edges, and those edges need to be specified.

---

## Critical Problem 8: No Topic Saturation Detection or Duplicate Prevention

The system can autonomously build the same product twice. Phase -1 will find high pain signals around the same topics repeatedly (Docker networking, Kubernetes setup, Python environment management — these appear in forums indefinitely). Without a mechanism to check whether a guide on this exact topic already exists in the product catalog, the system will greenlight the same topic every cycle.

The spec mentions this in the Global Failure Conditions section ("Redundant product") but provides no mechanism to detect redundancy. There's no query against an existing product catalog, no similarity check against previously built topics, no saturation threshold.

This is a real production failure mode — not a theoretical one.

**What should replace it:** A `products.db` table storing every shipped product's topic, angle, target audience, and topic embedding. Before Phase 0 completes the brief, run a similarity check: if cosine similarity between the candidate topic embedding and any existing product embedding exceeds 0.85, flag as potential duplicate and require human confirmation before proceeding.

---

## Efficiency Assessment: The Spec is Over-Engineered in the Wrong Places

The spec has 10+ explicitly named "engines" (Hook Engine, Differentiation Engine, Learning Engine, Economic Decision Engine, etc.). This language creates the impression of modular, powerful machinery. In practice, most of these "engines" are single prompts with no real algorithmic separation from the agent session they're embedded in.

The complexity budget is spent in the wrong places. The spec is highly detailed about:
- The 7-section ebook structure (good — this is the actual deliverable)
- Phase naming and identity labels (irrelevant to execution)
- The Learning Engine's five memory categories (medium value)

But severely underspecified on:
- How Differentiation is measured (critical — see Problem 1)
- How duplicate detection works (critical — see Problem 8)
- What the actual numeric thresholds are for the Build/Skip engine (critical — see Problem 2)
- What happens when Phase 1 can't find enough quality sources on a niche topic (important)
- How the system handles topics that evolve rapidly (versioning — e.g., a guide about a tool that released a new major version)

The ratio is inverted. Heavy on presentation, light on operational logic.

---

## The Fundamental Structural Issue: v9.0 is v7.5 + Autonomy Layer Without Addressing the Autonomy Challenges

Reading the full version history in the file, the evolution is: v7.5 (research-synthesis pipeline) → v8.0 (decision-driven writing) → v9.0 (autonomous operation). Each version adds a new layer on top.

The problem is that v9.0 grafts autonomy onto a pipeline that was designed for human-in-the-loop operation. The v7.5 spec's foundational gate was: *"If the input is NOT a human-provided PRODUCT_BRIEF, reject."* v9.0 removes this gate without replacing the quality controls it provided. A human writing a product brief brings tacit market knowledge, competitive awareness, and judgment about what audience they're serving. Replacing that with `Pain × Demand × Monetization × Differentiation` only works if all four factors are reliably measured — and they're not (see Problems 1, 2).

The honest version of v9.0 would acknowledge: autonomy is a deployment mode, not a quality upgrade. The pipeline quality is unchanged from v7.5. What v9.0 adds is a front-end that removes the human from the brief generation step — which is fine, but only if the brief-generation logic is as good as a thoughtful human. Currently, it isn't, for the reasons detailed above.

---

## Summary Table: What to Keep, Fix, and Add

| Aspect | Assessment | Action |
|--------|-----------|--------|
| Departmental isolation principle | ✅ Solid | Keep unchanged |
| 7-section ebook structure | ✅ Solid | Keep unchanged |
| Three operating modes | ✅ Correct framing | Keep, add bootstrapping sequence |
| Signal taxonomy (Phase -1) | ✅ Well-observed | Keep, add competitor scan |
| Opportunity score formula | ⚠️ Naive | Replace with weighted additive + floors |
| Differentiation factor | ❌ Ungrounded | Add competitor scan flow as data source |
| Source count gate (≥15) | ❌ Wrong proxy | Replace with coverage gate |
| Self-critique loop | ❌ Circular | Replace with role-inversion adversarial review |
| Feedback data sources | ❌ Assumes unavailable metrics | Redesign around actually collectable data |
| Learning flywheel cold start | ❌ Unaddressed | Add explicit bootstrapping sequence |
| Backward-loop iteration rules | ❌ Underspecified | Define per-phase loop conditions and max counts |
| Duplicate/saturation detection | ❌ Named but not implemented | Add topic embedding similarity check vs products.db |
| Pipeline linearity | ⚠️ Too rigid | Document all valid backward edges explicitly |

The spec is a strong conceptual foundation with serious operational gaps at the decision-critical junctions. It's worth implementing — but not as written. The fixes above are not cosmetic. Several of them (Differentiation sourcing, source quality gate, feedback data reality) need to be resolved before the autonomy claims become meaningful.



#####

Let me read all the scoring-related content across every document carefully.

Now let me look carefully at how scoring is actually implemented in the flow JSONs.

Now I have everything I need. Let me write the complete honest review.

---

# Deep Scoring Review: Every Layer, Every Problem, Every Fix

## What the System Actually Has Right Now

Before critiquing, let me map every scoring formula that actually exists across all documents, because they are scattered and inconsistent.

**Reddit flow (`score_opp` node):**
```
final_score = opportunity_score × maturity_multiplier × urgency_boost

maturity_multiplier: awareness=1, consideration=2, decision=3, post_purchase=2.5
urgency_boost: 1 + (0.3 if "frustrated") + (0.2 if "guilty")
```

**HN flow (`score_rank` node):**
```
final_score = opportunity_score × maturity_multiplier × (1 + log1p(cluster_size) × 0.1)

maturity_multiplier: awareness=1, consideration=2, decision=3
```

**factory-team.md (Build/Skip gate):**
```
MI Coordinator threshold: score > 100/243
Knowledge Sufficiency gate: technical_hints ≥ 3, diy_workarounds ≥ 2
```

**v9.0 spec (Phase 0 Decision Engine):**
```
Opportunity Score = Pain × Demand × Monetization × Differentiation
```

**factory-team.md first section (Feasibility score):**
```
Feasibility: 3 (high, pure text), 2 (medium, lightweight code), 1 (low, stateful)
Rule: Feasibility < 2 requires Demand = 3 AND Pain = 3
```

These are five different scoring systems, defined in different documents, none of which feed directly into each other. They don't share a data schema. They use different scale ranges. The v9.0 formula references `Pain` and `Demand` as variables but the flow already computes `opportunity_score` from the LLM classifier — nobody defines whether `opportunity_score` IS `Pain` or is a combination of Pain × Demand already. The `100/243` threshold in factory-team.md has no visible derivation. It implies a maximum possible score of 243 from some unstated formula.

This is the core problem: **the scoring system is not one system. It is five systems that were designed at different times and never reconciled.**

---

## Problem 1: `opportunity_score` Is a Black Box

Both flows receive `opportunity_score` from the LLM classifier (Gemini or SambaNova fallback). The LLM prompt asks for a float between 0.0 and 1.0. That's it.

The LLM has no explicit instructions on what scale this score represents, what criteria to weigh, or how to anchor its judgment. The prompt says: `"opportunity_score": <0.0-1.0>`. The LLM makes up a number.

This matters because `opportunity_score` is the base multiplier for the entire final score calculation. If the LLM outputs 0.8 for a moderate opportunity and 0.85 for a strong one, the 6% difference gets multiplied through the maturity multiplier and urgency boosts, producing scores that appear precise (e.g., `2.38` vs `2.55`) but are grounded in a single uncalibrated floating-point guess.

**The numbers look quantitative. They are not. They are dressed-up LLM opinions with no calibration baseline.**

Concrete example from the Reddit prompt:
```
"opportunity_score": <0.0-1.0>
```
And from the HN prompt (same thing):
```
"opportunity_score": <0.0-1.0>
```

No anchoring. No criteria. No examples. The LLM is free to interpret the scale any way it wants, and it will — differently each run, differently across models, differently across topics.

---

## Problem 2: The Maturity Multiplier Is Structurally Backwards

Both flows use:
```
maturity_multiplier: awareness=1, consideration=2, decision=3
```

The logic is: if someone is at the "decision" stage, multiply their pain score by 3, because they're closest to buying.

This is a fundamental misread of the buyer journey applied to the wrong problem.

Pain signals from forums are overwhelmingly `awareness` and `consideration` stage. Someone posting "I can't get Docker to connect to localhost" on Reddit is expressing awareness-level pain — they know they have a problem, they don't know the solution. According to the current formula, this cluster scores **3× lower** than a cluster where people are comparing two specific tools before buying.

But here's the reality: **awareness-stage pain clusters are exactly what you want to build ebooks for.** People at the decision stage already know enough to evaluate options. People at the awareness stage are lost and will pay for a clear guide that leads them through. The maturity multiplier is penalizing your best product opportunities.

The correct interpretation of maturity for info-product selection is the opposite:
- `awareness`: High value — people are confused, they need a guide, they'll pay for clarity
- `consideration`: Medium value — they're researching, a good comparison guide has value
- `decision`: Lower value for info products — they're almost done, they don't need a guide, they need a specific answer

The Reddit flow multiplies `decision × 3` and `awareness × 1`. It should be closer to the reverse if the product is a how-to guide.

---

## Problem 3: The Urgency Boost Is Arbitrary and Fragile

Reddit flow:
```
urgency_boost = 1 + (0.3 if "frustrated") + (0.2 if "guilty")
```

The 0.3 and 0.2 coefficients have no derivation. Why 0.3 for frustrated? Why 0.2 for guilty? Why not 0.4 and 0.1? There is no documented reasoning.

More critically: `emotional_profile` is a list generated by the same LLM classifier that generated `opportunity_score`. So the urgency boost is: **an LLM's opinion (opportunity_score) multiplied by a boost factor derived from the same LLM's opinion about emotions (emotional_profile)**. One LLM hallucination compounds another.

The HN flow doesn't use emotional_profile at all — it uses `log1p(cluster_size) × 0.1` instead. This is actually better because cluster size is a real measured quantity (count of posts), not an LLM opinion. But the coefficient 0.1 is still arbitrary, and `log1p` dampens cluster size to near-irrelevance (a cluster of 20 posts gives `log1p(20) × 0.1 ≈ 0.3` bonus, barely meaningful).

The two flows use structurally different bonus calculations for the same purpose, producing incomparable scores across sources.

---

## Problem 4: The `100/243` Threshold Is a Ghost Number

`factory-team.md` states: "Input: Scored opportunities from MI Coordinator (score > 100/243)."

243 implies a maximum possible score. What formula produces a max of 243?

If Pain ∈ [1,3], Demand ∈ [1,3], Feasibility ∈ [1,3], and some fourth factor ∈ [1,3], then 3×3×3×3 = 81. Not 243.

If there are five factors each rated 1-3: 3^5 = 243. So this is an implicit five-factor multiplicative formula with all factors on a 1-3 scale. But these five factors are never defined anywhere in the document. The threshold exists without its formula.

This is not a minor gap. It means the gate that controls which opportunities enter the product pipeline is based on a threshold derived from a formula that isn't written down anywhere.

---

## Problem 5: The v9.0 Formula Introduces New Undefined Variables

`Opportunity Score = Pain × Demand × Monetization × Differentiation`

- **Pain**: derivable from `opportunity_score` or `pain_category` from the flows. Possible but requires a mapping.
- **Demand**: derivable from `cluster_size` or `maturity`. Possible.
- **Monetization**: partially derivable from `monetization_angle`. But "monetization angle" is a category label, not a score. How do you score `info_product` vs `SaaS` vs `service`? Not defined.
- **Differentiation**: not collected anywhere in the current data pipeline. There is no source that measures how many competing products already exist on this topic. This factor is completely ungrounded.

All four factors have scale undefined. Is Pain on a 1-10 scale? 0-1? 1-3? The spec says nothing. Since they're multiplied, the choice of scale dramatically changes the output and the meaning of any threshold.

---

## Problem 6: Cross-Source Scores Are Not Comparable

Reddit's `final_score` and HN's `final_score` are computed with different formulas (emotional_profile boost vs log cluster size boost). They cannot be directly compared or merged. An opportunity scored 2.8 from Reddit and 2.6 from HN cannot be meaningfully combined into a unified ranking without knowing they were computed differently.

When the `opportunity-consolidator` flow eventually reads both DBs to produce `TOP_OPPORTUNITIES.json`, merging these scores directly would be wrong. A Reddit score of 2.8 and an HN score of 2.8 do not represent the same thing.

---

## The Alternative: An Evidence-Based Scoring Strategy

Here's a complete replacement that eliminates all the above problems. The key design principle is: **every score comes from a counted, measurable observation — not from an LLM floating-point opinion.**

### The Core Shift: Count Evidence, Don't Score Opinions

Instead of asking the LLM "how strong is this opportunity on a 0-1 scale," ask it structured classification questions whose answers are countable categories. Then score the categories deterministically in the JavaScript node, not in the LLM.

---

### Step 1: Fix the LLM Classifier Prompt

Replace the current open-ended `opportunity_score: <0.0-1.0>` with explicit criteria questions:

**For post-level classification (the `classify` node — currently just `pain_point` vs other):**

```json
{
  "is_pain": true/false,
  "pain_type": "blocked | slow | confused | expensive | broken",
  "has_attempted_solution": true/false,
  "mentions_money_lost_or_wasted": true/false,
  "question_is_specific": true/false
}
```

Each field is a binary or categorical answer. LLMs are reliable at binary classification. They are unreliable at continuous scoring.

**For cluster-level labeling (the `label_llm` node):**

Replace:
```json
{"opportunity_score": 0.73, "pain_maturity": "consideration", ...}
```

With:
```json
{
  "pain_label": "Docker networking localhost unreachable",
  "pain_category": "tooling",
  "blocker_type": "configuration | knowledge_gap | compatibility | undocumented",
  "solution_exists": "yes_official | yes_workaround | partial | no",
  "audience_type": "beginner | intermediate | advanced",
  "monetization_angle": "ebook | checklist | template | tool | course",
  "recurrence_signal": "one_off | recurring | chronic",
  "summary": "one sentence"
}
```

Now every field is a named category. There are no floating-point opinions.

---

### Step 2: Score Deterministically in JavaScript

Instead of multiplying LLM-generated floats, build the final score from the counted, classified observations:

```javascript
// In the score_opp node — fully deterministic

const BLOCKER_SCORE = {
  knowledge_gap:    3,  // People don't know how — perfect for a guide
  configuration:    2,  // Needs step-by-step — good for a guide
  undocumented:     2,  // Missing docs — guide fills the gap
  compatibility:    1   // Environment-specific — harder to generalize
};

const SOLUTION_SCORE = {
  no:              3,  // No solution exists — highest gap
  partial:         3,  // Partial solution — guide adds value
  yes_workaround:  2,  // Workaround exists — guide can systematize it
  yes_official:    1   // Official solution exists — lower differentiation
};

const AUDIENCE_SCORE = {
  beginner:        3,  // Largest audience, most willing to pay for clarity
  intermediate:    2,
  advanced:        1   // Smallest audience, often solve it themselves
};

const RECURRENCE_SCORE = {
  chronic:         3,  // Problem keeps coming back — high demand over time
  recurring:       2,
  one_off:         1
};

const MONETIZATION_SCORE = {
  ebook:           3,
  course:          3,
  template:        2,
  checklist:       2,
  tool:            1   // Tool = higher buildability cost
};

return items.map(cluster => {
  // Base: pure count of pain posts (real evidence, not LLM opinion)
  const evidence_weight = Math.min(cluster.size / 5, 3);  
  // caps at 3 for clusters with 15+ posts

  const blocker    = BLOCKER_SCORE[cluster.blocker_type]     || 1;
  const gap        = SOLUTION_SCORE[cluster.solution_exists] || 1;
  const audience   = AUDIENCE_SCORE[cluster.audience_type]   || 2;
  const recurrence = RECURRENCE_SCORE[cluster.recurrence_signal] || 1;
  const monetize   = MONETIZATION_SCORE[cluster.monetization_angle] || 2;

  // Weighted sum — NOT multiplicative
  const raw_score = (
    evidence_weight * 0.30 +  // How many people have this problem
    blocker        * 0.25 +  // Is it a knowledge gap (best) or env issue (harder)?
    gap            * 0.20 +  // Does a good solution already exist?
    audience       * 0.15 +  // Is the audience large?
    recurrence     * 0.10    // Is this a permanent or temporary problem?
  );
  // monetize is a gate, not a score component — filter below

  return {
    ...cluster,
    score_breakdown: { evidence_weight, blocker, gap, audience, recurrence },
    raw_score: Math.round(raw_score * 100) / 100,  // 0–3 scale
    monetization_viable: monetize >= 2,
    proceed: raw_score >= 2.0 && monetize >= 2
  };
}).filter(c => c.monetization_viable)
  .sort((a, b) => b.raw_score - a.raw_score);
```

**Why weighted sum instead of multiplication:**
With multiplication, one low factor kills the entire score. A `knowledge_gap` opportunity with a large audience but a moderate recurrence signal (chronic=3, knowledge_gap=3, but recurrence=1) scores `3×3×3×1×3 = 81` vs `3×3×3×3×3 = 243`. The single low factor cuts the score by 67%.

With weighted sum: `(3×0.30) + (3×0.25) + (3×0.20) + (3×0.15) + (1×0.10) = 0.9+0.75+0.6+0.45+0.1 = 2.8`. Still a strong score. The low recurrence signal contributes proportionally — it doesn't veto the opportunity.

**Why evidence_weight is capped at 3:** `cluster.size` can range from 5 to 200+. You want large clusters to score better than small ones, but you don't want a 200-post cluster to overwhelm all other factors. The cap at 15 posts / 3 points keeps it proportional.

---

### Step 3: Fix the Threshold — Make It Explicit and Named

Replace `score > 100/243` with:

```javascript
// Gate definitions — each has a clear English meaning

const HARD_GATES = {
  minimum_raw_score:     2.0,   // Out of 3.0
  minimum_cluster_size:  5,     // At least 5 posts expressing this pain
  monetization_viable:   true   // Must have a viable product angle
};

const SOFT_FLAGS = {
  // These don't reject, but flag for human review
  high_competition_risk: cluster.solution_exists === 'yes_official',
  niche_audience_risk:   cluster.audience_type === 'advanced',
  low_evidence:          cluster.size < 10
};
```

Now any developer reading this understands exactly why an opportunity was rejected: "raw_score was 1.8, below the 2.0 minimum" is meaningful. "score was 87, below 100/243" is not.

---

### Step 4: Fix Cross-Source Comparability

Since both flows now use identical categorical inputs and identical JavaScript scoring, scores are directly comparable across Reddit and HN. The `opportunity-consolidator` flow can safely merge and rank them.

Add a source-weight adjustment in the consolidator only — not in the individual miners:

```javascript
const SOURCE_WEIGHT = {
  reddit: 1.0,  // General developer community
  hn:     1.1,  // Slightly higher signal quality (more senior audience)
  so:     1.2   // Stack Overflow — highest intent signal (people actively debugging)
};

// In consolidator:
const adjusted_score = cluster.raw_score * SOURCE_WEIGHT[cluster.source];
```

This is one multiplication applied once at merge time, not baked into each flow. Clean and auditable.

---

### Step 5: Replace the v9.0 Formula With a Two-Stage Gate

Instead of `Pain × Demand × Monetization × Differentiation` (four undefined factors multiplied together), use a two-stage filter:

**Stage 1 — Hard gates (automated, no LLM):**
```
raw_score >= 2.0          (evidence + blocker type + gap + audience + recurrence)
cluster_size >= 5         (minimum evidence threshold)
monetization_viable = true (has a buildable product angle)
not_in_catalog = true     (topic embedding not already in products.db)
```

All four must pass. These are computable from real data.

**Stage 2 — Soft scoring for prioritization (after hard gates pass):**
```
priority_score = adjusted_score × (1 + kb_depth_bonus)

kb_depth_bonus = count of matching insights in KB / 10
  (capped at 0.5 — if you already have lots of KB data on this topic, it's easier to build)
```

The KB depth bonus replaces `Differentiation` in the original formula with something actually measurable: how much internal knowledge you already have about this domain. If your KB has 20 insights about Docker networking, a Docker networking opportunity gets a +0.2 bonus. If you have 0 KB entries, no bonus — it's buildable but will require more research.

---

### Step 6: Scoring Transparency — Mandatory

Every scored opportunity should carry its breakdown as a readable field:

```json
{
  "label": "Docker localhost unreachable from container",
  "raw_score": 2.65,
  "adjusted_score": 2.65,
  "proceed": true,
  "score_breakdown": {
    "evidence_weight": "3.0 (18 posts)",
    "blocker_type": "knowledge_gap → 3",
    "solution_gap": "yes_workaround → 2",
    "audience": "intermediate → 2",
    "recurrence": "chronic → 3"
  },
  "flags": {
    "high_competition_risk": false,
    "low_evidence": false
  },
  "kb_depth": 7,
  "kb_depth_bonus": 0.07
}
```

This is what FORGE reads. When FORGE makes a Build/Skip decision, it reads `score_breakdown` and `flags` in plain English — not a float. FORGE can then reason: "evidence_weight is 3 (18 posts), knowledge gap type means a guide will be highly valuable, chronic recurrence means this problem won't go away, no competition risk flag." This is a decision FORGE can actually make with confidence, because every component is named and interpretable.

---

## Summary: What Changes and Why

| Current | Problem | Replacement |
|---------|---------|-------------|
| `opportunity_score: 0.0-1.0` from LLM | Uncalibrated floating-point opinion | 5 categorical fields, scored deterministically |
| Maturity multiplier (awareness×1, decision×3) | Backwards for info-product selection | Removed; recurrence_signal replaces maturity |
| Urgency boost (frustrated×0.3) | Arbitrary, compounds LLM noise | Removed entirely |
| Multiplicative formula | One low factor kills score | Weighted sum with named weights |
| `score > 100/243` | Threshold from undefined formula | Two named hard gates with English meaning |
| v9.0 `Pain × Demand × Monetization × Differentiation` | Two undefined factors, all undefined scales | Two-stage filter: hard gates + priority score |
| Cross-source incomparable scores | Reddit and HN use different bonuses | Identical base formula + source weight at merge |
| No score transparency | FORGE reads a float | Every opportunity carries readable breakdown |

The core principle replacing everything: **count real evidence, classify into named categories, score deterministically, make thresholds readable.** An LLM's job in this pipeline is to classify posts and clusters into named buckets — not to invent scores. The JavaScript nodes do the arithmetic. No hallucination possible in a deterministic formula.