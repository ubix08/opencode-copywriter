# Master Project Specification — AI Gumroad Product Factory
## Version 1.0.0 | OpenCode-Native | Self-Contained Scaffolding Spec

---

## 0. How to Use This Document

This specification is **self-contained and executable**. A coding agent (OpenCode / Claude Code) reading this document has everything needed to scaffold the entire project from scratch.

**Scaffolding entry point:**
```
/scaffold
```
This single command builds the full directory tree, all config files, all agent definitions, all slash commands, and all context documents in one pass.

**Runtime entry point after scaffold:**
```
/ideate → /build-product → /package → /publish → /log-sale
```

**Goal:** Ship one Gumroad digital product per day. Reach $1 in revenue as fast as possible. Scale to $500/month through product accumulation and compounding traffic.

---

## 1. Project Overview

### 1.1 Mission
An AI-augmented digital product factory that automatically ideates, builds, packages, and publishes digital products to Gumroad. The system uses OpenCode agents to replace the manual workflow of a solo digital product creator.

### 1.2 Target
- **Platform:** Gumroad (gumroad.com)
- **Product types:** Scripts, prompt packs, cheatsheets, templates, micro-tools, guides
- **Price range:** $5–$49 per product
- **Revenue goal:** $1 first week → $100 first month → $500/month by month 3
- **Infrastructure:** Contabo VPS 4-core / 7GB RAM / Ubuntu 22.04 + OpenCode

### 1.3 Core Principle
**One sharp pain. One specific person. One afternoon to build.**

Every product must pass the "5-dollar skip test": would a busy professional pay $5 to skip the 2 hours it took to build this? If yes, ship it.

### 1.4 Operator Profile
- Strong systems thinking, modest coding skills
- ERP consultant background (SAP, Oracle, business process expertise)
- Comfortable with Python, TypeScript basics
- Runs OpenCode on VPS, deploys via CLI
- Wants deterministic pipelines, not improvised workflows

---

## 2. System Architecture

### 2.1 Three-Layer Design

```
┌──────────────────────────────────────────────────────────────────┐
│  LAYER 1 — Python Scripts (scripts/)                             │
│  $0 LLM cost. Runs on cron or command.                           │
│                                                                   │
│  trend_scan.py → score_ideas.py → package_product.py             │
│       │                │                    │                     │
│       ▼                ▼                    ▼                     │
│  raw_ideas.json  scored_ideas.json   products/{slug}/            │
├──────────────────────────────────────────────────────────────────┤
│  LAYER 2 — OpenCode Agents (.opencode/agents/)                   │
│  LLM-powered. Invoked via /command or @mention.                  │
│                                                                   │
│  @agent-0-scout      (Haiku, low cost)   — trend discovery       │
│  @agent-1-ideator    (Haiku, low cost)   — idea generation       │
│  @agent-2-researcher (Sonnet, moderate)  — demand validation     │
│  @agent-3-builder    (Sonnet, moderate)  — product creation      │
│  @agent-4-packager   (Sonnet, moderate)  — landing page + files  │
│  @agent-5-publisher  (Sonnet, moderate)  — Gumroad listing       │
├──────────────────────────────────────────────────────────────────┤
│  LAYER 3 — Context Docs (.opencode/context/factory/)             │
│  Reference knowledge base for agents.                            │
│                                                                   │
│  agent-0-scout.md       → trend sources, query templates         │
│  agent-1-ideator.md     → idea scoring rubric, niche map         │
│  agent-2-researcher.md  → demand signals, pricing benchmarks     │
│  agent-3-builder.md     → product type templates, build guides   │
│  agent-4-packager.md    → file formats, ZIP structure, previews  │
│  agent-5-publisher.md   → Gumroad listing formulas, SEO rules    │
└──────────────────────────────────────────────────────────────────┘
```

### 2.2 Component Inventory

| Component | File(s) | Language | Role |
|---|---|---|---|
| Trend Scanner | scripts/trend_scan.py | Python | Reddit/HN/Google Trends pain signal collector |
| Idea Scorer | scripts/score_ideas.py | Python | Deterministic scoring of raw ideas |
| Product Packager | scripts/package_product.py | Python | ZIP builder, preview generator |
| Gumroad Publisher | scripts/publish_gumroad.py | Python | Gumroad API product creator |
| Sales Logger | scripts/log_sale.py | Python | Revenue tracker, stats updater |
| Master Orchestrator | scripts/run_factory.py | Python | Pipeline CLI controller |
| VPS Setup | scripts/setup-vps.sh | Bash | One-time infrastructure bootstrap |
| Cron Installer | scripts/setup-cron.sh | Bash | Schedule recurring trend scans |
| OpenCode Config | opencode.json | JSON | MCP servers, instructions |
| Agent: Scout | .opencode/agents/agent-0-scout.md | Markdown | Trend discovery agent |
| Agent: Ideator | .opencode/agents/agent-1-ideator.md | Markdown | Idea generation agent |
| Agent: Researcher | .opencode/agents/agent-2-researcher.md | Markdown | Demand validation agent |
| Agent: Builder | .opencode/agents/agent-3-builder.md | Markdown | Product creation agent |
| Agent: Packager | .opencode/agents/agent-4-packager.md | Markdown | File packaging agent |
| Agent: Publisher | .opencode/agents/agent-5-publisher.md | Markdown | Gumroad publishing agent |
| Commands (12) | .opencode/commands/*.md | Markdown | Slash commands for workflow |
| Context Docs (8) | .opencode/context/factory/*.md | Markdown | Agent reference knowledge |

---

## 3. Core Data Flow

### 3.1 Full Pipeline

```
START
  │
  ▼
┌─────────────────────────────────────────────────────────────┐
│  SCAN (Layer 1 — Script)                                     │
│                                                              │
│  trend_scan.py:                                              │
│  ├── Reddit RSS (r/entrepreneur, r/digitalnomad,             │
│  │   r/consulting, r/sap, r/excel, r/learnpython)           │
│  ├── Hacker News Algolia API ("pain", "annoying", "wish")   │
│  ├── Google Trends RSS (CSV, automation, Python, ERP)       │
│  └── Deduplicates via seen_signals.json (MD5 of title+url)  │
│                                                              │
│  Output: ideas/raw_signals.json                              │
└─────────────────────────────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────────────────────────────┐
│  SCORE (Layer 1 — Script)                                    │
│                                                              │
│  score_ideas.py:                                             │
│  ├── REJECT  → vague pain, requires SaaS subscription,      │
│  │             needs audience/following, requires API key   │
│  ├── HOLD    → good idea but needs more research            │
│  └── ACCEPT  → specific pain + buildable in <4hrs +         │
│                deliverable is a file + no ongoing support   │
│      ├── Type: script / prompt_pack / template /            │
│      │         cheatsheet / guide / micro_tool              │
│      └── Score: pain_score + buildability + monetizability  │
│                                                              │
│  Output: ideas/scored_ideas.json + ideas/rejected_ideas.json│
└─────────────────────────────────────────────────────────────┘
  │
  ▼ (Agent reviews scored ideas, picks top candidate)
  │
┌─────────────────────────────────────────────────────────────┐
│  VALIDATE (Layer 2 — OpenCode Agent @researcher)            │
│                                                              │
│  Uses Brave Search MCP to:                                   │
│  ├── Confirm the pain exists (forum threads, questions)     │
│  ├── Check competition (existing Gumroad/Etsy products)     │
│  ├── Benchmark pricing ($5–$49 range validation)            │
│  └── Identify positioning angle (faster/cheaper/simpler)   │
│                                                              │
│  Output: ideas/validated/{slug}_research.json               │
└─────────────────────────────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────────────────────────────┐
│  BUILD (Layer 2 — OpenCode Agent @builder)                  │
│                                                              │
│  Depending on product type:                                  │
│  ├── Script → Python .py file, tested, commented            │
│  ├── Prompt Pack → .md or .txt, 10–20 prompts, categorized  │
│  ├── Template → .xlsx / .docx / .md structured file         │
│  ├── Cheatsheet → single-page PDF-ready .md                 │
│  ├── Guide → multi-section .md, 800–2000 words              │
│  └── Micro-Tool → Python CLI with argparse, README          │
│                                                              │
│  Output: products/{slug}/src/                               │
└─────────────────────────────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────────────────────────────┐
│  PACKAGE (Layer 1 — Script + Agent @packager)               │
│                                                              │
│  package_product.py:                                         │
│  ├── Creates products/{slug}/dist/{slug}_v1.zip             │
│  ├── Generates preview sample (first 20% of content)        │
│  ├── Writes README.md inside ZIP                            │
│  └── Generates thumbnail prompt for cover image             │
│                                                              │
│  Agent @packager:                                            │
│  ├── Writes Gumroad listing copy (title, description, tags) │
│  ├── Writes 3 bullet "what you get" points                  │
│  └── Suggests price tier ($5/$9/$15/$25/$39/$49)            │
│                                                              │
│  Output: products/{slug}/dist/ + products/{slug}/listing.md │
└─────────────────────────────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────────────────────────────┐
│  PUBLISH (Layer 2 — Script + Agent @publisher)              │
│                                                              │
│  publish_gumroad.py:                                         │
│  ├── Calls Gumroad API v2 (create product)                  │
│  ├── Uploads ZIP file as product attachment                 │
│  ├── Sets price, description, tags from listing.md          │
│  ├── Sets product as published (not draft)                  │
│  └── Returns product URL + product_id                       │
│                                                              │
│  Output: products/{slug}/published.json                     │
└─────────────────────────────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────────────────────────────┐
│  LOG (Layer 1 — Script)                                      │
│                                                              │
│  /log-sale won|pending|live {slug} ${amount}                 │
│  ├── Appends to sales/stats.json                            │
│  ├── Updates sales/tracker.md dashboard                     │
│  └── Shows running totals (products live, revenue, goal %)  │
└─────────────────────────────────────────────────────────────┘
  │
  ▼
END (loop back to SCAN — new product tomorrow)
```

---

## 4. Niche Map — Priority Verticals

These are pre-validated niches ordered by operator fit (ERP background + Python skills):

| Priority | Niche | Buyer | Pain | Product Type | Price |
|---|---|---|---|---|---|
| 1 | ERP / SAP consultants | Freelance SAP consultants | No reusable templates, reinventing deliverables every project | Template pack | $25–$49 |
| 2 | Python beginners | Self-taught devs | Exercises with no feedback loop | Prompt pack / guide | $9–$19 |
| 3 | Excel power users | Office analysts | Repetitive tasks, no automation | Python script | $9–$25 |
| 4 | Freelancers | Solo service providers | Proposal / contract boilerplate | Template pack | $9–$19 |
| 5 | n8n / automation | No-code builders | Workflow templates are scattered | Template JSON pack | $15–$39 |
| 6 | Data analysts | Junior analysts | Cleaning messy CSVs manually | Python script | $9–$25 |
| 7 | AI prompt users | Knowledge workers | Prompt engineering from scratch | Prompt pack | $5–$15 |

---

## 5. Script Deep-Dive

### 5.1 trend_scan.py — Signal Collector

**Purpose:** Collect pain signals from free public sources.

**Sources:**

| Source | Auth | Method | Keywords |
|---|---|---|---|
| Reddit RSS | None | feedparser | "how do I", "annoying", "wish there was", "does anyone" |
| HN Algolia API | None | requests | "pain", "tedious", "automate", "template" |
| Google Trends RSS | None | feedparser | CSV, Python, SAP, automation, ERP |

**Deduplication:** MD5 hash of (title + url) stored in `ideas/seen_signals.json`.

**Output:** `ideas/raw_signals.json` — array of signal objects.

**Signal schema:**
```json
{
  "id": "md5hash",
  "source": "reddit|hn|gtrends",
  "title": "string",
  "url": "string",
  "body_snippet": "string (first 500 chars)",
  "upvotes": 0,
  "fetched_at": "ISO8601",
  "keywords_matched": ["string"]
}
```

**Dependencies:** feedparser, requests, rich

---

### 5.2 score_ideas.py — Idea Scorer

**Purpose:** Apply deterministic rules to score each pain signal as a product idea.

**Scoring Dimensions (0–10 each):**

| Dimension | What It Measures | Signals |
|---|---|---|
| pain_score | How acute and specific the pain is | Upvotes, "every day", "hours", "hate this" |
| buildability | Can be built in under 4 hours | File deliverable, no backend, no auth |
| monetizability | Would someone pay for this | Professional context, time saved, recurring need |
| operator_fit | Matches operator's skills (ERP/Python) | SAP, Excel, Python, consulting, data keywords |

**Total score = (pain × 0.35) + (buildability × 0.30) + (monetizability × 0.25) + (fit × 0.10)**

**Decision rules:**
- Score ≥ 7.0 → ACCEPT
- Score 4.0–6.9 → HOLD
- Score < 4.0 → REJECT

**REJECT overrides (regardless of score):**
- Requires SaaS subscription to deliver
- Requires audience/social following
- Ongoing support implied ("maintain", "update weekly")
- Legal/compliance product (liability risk)

**Output:** `ideas/scored_ideas.json`, `ideas/rejected_ideas.json`

**Scored idea schema:**
```json
{
  "id": "md5hash",
  "signal_id": "md5hash",
  "title": "string",
  "product_concept": "string",
  "product_type": "script|prompt_pack|template|cheatsheet|guide|micro_tool",
  "niche": "string",
  "scores": {
    "pain": 8,
    "buildability": 9,
    "monetizability": 7,
    "operator_fit": 10,
    "total": 8.35
  },
  "decision": "ACCEPT|HOLD|REJECT",
  "suggested_price": 15,
  "estimated_build_hours": 2.5,
  "scored_at": "ISO8601"
}
```

**Dependencies:** rich

---

### 5.3 package_product.py — Product Packager

**Purpose:** Turn built product files into a distributable ZIP with preview.

**Actions:**
1. Reads `products/{slug}/src/` directory
2. Generates `products/{slug}/dist/preview_{slug}.md` (first 20% of content)
3. Writes `products/{slug}/src/README.md` from listing.md if not present
4. Creates `products/{slug}/dist/{slug}_v1.zip` containing all src/ files
5. Outputs packaging manifest to `products/{slug}/dist/manifest.json`

**Manifest schema:**
```json
{
  "slug": "string",
  "version": "1.0",
  "files_included": ["string"],
  "zip_path": "string",
  "preview_path": "string",
  "file_size_kb": 0,
  "packaged_at": "ISO8601"
}
```

**Dependencies:** zipfile (stdlib), pathlib (stdlib), rich

---

### 5.4 publish_gumroad.py — Gumroad Publisher

**Purpose:** Create and publish a product on Gumroad via API v2.

**Gumroad API reference:**
- Base URL: `https://api.gumroad.com/v2`
- Auth: Bearer token via `GUMROAD_ACCESS_TOKEN` env var
- Create product: `POST /products`
- Upload file: `PUT /products/{id}/files` (multipart)
- Enable product: `PUT /products/{id}` with `{"published": true}`

**Input:** Reads `products/{slug}/listing.md` + `products/{slug}/dist/{slug}_v1.zip`

**Listing.md format (parsed by script):**
```
# TITLE
{product title}

# DESCRIPTION
{full description}

# PRICE
{integer in cents, e.g. 1500 for $15}

# TAGS
{comma-separated tags}

# SUMMARY
{one-line summary for card view}
```

**Output:** `products/{slug}/published.json`

```json
{
  "gumroad_id": "string",
  "product_url": "https://gumroad.com/l/{id}",
  "title": "string",
  "price_cents": 1500,
  "published_at": "ISO8601",
  "status": "live"
}
```

**Dependencies:** requests, python-dotenv, rich

---

### 5.5 run_factory.py — Master Orchestrator

**Purpose:** CLI frontend for running pipeline stages.

| Command | Action |
|---|---|
| `scan` | Run trend_scan.py |
| `score` | Run score_ideas.py |
| `show` | Display top 5 scored ideas table |
| `package <slug>` | Run package_product.py for a product |
| `publish <slug>` | Run publish_gumroad.py for a product |
| `stats` | Show sales/tracker.md summary |
| `full` | Run scan + score + show sequentially |

**Dependencies:** rich, subprocess

---

### 5.6 log_sale.py — Revenue Tracker

**Purpose:** Record sales events and update running totals.

**Usage:** `python scripts/log_sale.py <event> <slug> <amount>`

**Events:** `live` (product published), `sale` (sale recorded), `refund`

**Output:** Appends to `sales/stats.json`, regenerates `sales/tracker.md`

**Tracker dashboard format:**
```
# Gumroad Factory — Revenue Tracker

## Totals
- Products live: N
- Total revenue: $X.XX
- Goal ($500/mo): X%
- Win rate: X% (sales/views est.)

## Products Live
| Slug | Title | Price | Sales | Revenue |
|------|-------|-------|-------|---------|

## Recent Sales
| Date | Slug | Amount |
|------|------|--------|
```

---

## 6. OpenCode Configuration

### 6.1 opencode.json
```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "brave-search": {
      "type": "local",
      "command": ["npx", "-y", "@modelcontextprotocol/server-brave-search"],
      "enabled": true,
      "environment": {
        "BRAVE_API_KEY": "${BRAVE_API_KEY}"
      }
    }
  },
  "instructions": ["AGENTS.md"]
}
```

### 6.2 .env (template — never commit)
```
GUMROAD_ACCESS_TOKEN=your_token_here
BRAVE_API_KEY=your_key_here
```

### 6.3 AGENTS.md (injected into all agents)
```markdown
# Gumroad Factory — Project Instructions

## Mission
Build and publish one digital product per day on Gumroad.
Target: $1 first week → $500/month by month 3.

## Product Philosophy
- One sharp pain. One specific person. One afternoon to build.
- Deliverable must be a FILE (not a service, not a SaaS).
- "5-dollar skip test": would a busy professional pay $5 to skip building this?

## Operator Skills
- Strong: ERP/SAP consulting, business process, Python scripting, systems design
- Moderate: TypeScript, markdown, CLI tools
- Avoid: frontend UI, mobile apps, anything requiring ongoing maintenance

## Directory Structure
ideas/          → raw and scored ideas
products/       → one folder per product slug
  {slug}/
    src/        → source files (built product)
    dist/       → ZIP + preview
    listing.md  → Gumroad copy
    published.json → live product metadata
sales/          → revenue tracking
scripts/        → Python automation scripts
.opencode/      → agents, commands, context

## Queue Files
ideas/raw_signals.json       → raw pain signals from trend_scan.py
ideas/scored_ideas.json      → scored + qualified ideas
ideas/rejected_ideas.json    → rejected ideas (log only)
ideas/validated/{slug}.json  → per-idea research by @researcher
sales/stats.json             → all sale events
sales/tracker.md             → revenue dashboard

## Tool Selection by Product Type
script        → Python, argparse CLI, README, requirements.txt
prompt_pack   → .md file, 10-20 prompts, organized by use case
template      → .xlsx or .md, structured, fill-in-the-blank format
cheatsheet    → single .md page, table-heavy, print-ready structure
guide         → multi-section .md, 800-2000 words, actionable steps
micro_tool    → Python CLI + README + example input/output

## Pricing Tiers
$5   → impulse buy, single-use utility
$9   → low-friction professional tool
$15  → solid value, 30min+ time saved
$25  → professional template pack, ERP/consulting niche
$39  → comprehensive toolkit, multiple files
$49  → premium pack, clear ROI for consultants

## Non-Negotiables
- Never build products requiring a paid API key to USE
- Never promise "updated regularly" unless automated
- Always include a README in every ZIP
- Always include a preview file (first 20% of content)
- Gumroad listing description must be 150-300 words
```

---

## 7. OpenCode Agents

### 7.1 @agent-0-scout — Trend Scanner (Haiku)

```markdown
---
name: agent-0-scout
description: Scans public sources for pain signals and product opportunities
model: claude-haiku-4-20250514
temperature: 0.1
maxSteps: 6
---

You are the Scout agent for the Gumroad Factory.
Your job: run trend_scan.py, read raw_signals.json, summarize top 10 strongest pain signals.

## Permissions
- bash: python scripts/trend_scan.py (allow)
- bash: python scripts/run_factory.py scan (allow)
- bash: cat ideas/raw_signals.json (allow)
- bash: * (deny)
- read: allow
- edit: allow
- webfetch: deny
- websearch: deny

## Output Format
After running, present a table:
| # | Pain Signal | Source | Keywords | Strength |
Show top 10 by upvotes/engagement. Do not invent signals. Read only from raw_signals.json.
```

---

### 7.2 @agent-1-ideator — Idea Generator (Haiku)

```markdown
---
name: agent-1-ideator
description: Converts pain signals into scored product ideas
model: claude-haiku-4-20250514
temperature: 0.2
maxSteps: 6
---

You are the Ideator agent for the Gumroad Factory.
Your job: read scored_ideas.json, present ACCEPT-tier ideas, help operator pick the best one.

## Permissions
- bash: python scripts/score_ideas.py (allow)
- bash: python scripts/run_factory.py score (allow)
- bash: python scripts/run_factory.py show (allow)
- bash: cat ideas/scored_ideas.json (allow)
- bash: * (deny)
- read: allow
- edit: allow
- webfetch: deny
- websearch: deny

## Output Format
Present top 5 ACCEPT ideas as a decision table:
| # | Concept | Type | Score | Price | Build Hours | Fit |
Ask operator: "Which should we build today? Reply with number or describe your own."
```

---

### 7.3 @agent-2-researcher — Demand Validator (Sonnet)

```markdown
---
name: agent-2-researcher
description: Validates product demand using Brave Search and competitor analysis
model: claude-sonnet-4-20250514
temperature: 0.3
maxSteps: 8
---

You are the Researcher agent for the Gumroad Factory.
Your job: validate that a product idea has real demand before we spend time building it.

## Permissions
- bash: * (deny)
- bash: mkdir ideas/validated (allow)
- read: allow
- edit: allow
- websearch: allow (Brave Search MCP)
- webfetch: allow (read competitor pages)

## Validation Workflow
1. Search: "{product topic} Gumroad" — count competing products, note prices
2. Search: "{pain signal} reddit" — find threads confirming the pain
3. Search: "{product topic} buy template|script|guide" — confirm purchase intent
4. Check: is there a gap (no good solution at this price point)?
5. Output: ideas/validated/{slug}_research.json

## Research Output Schema
{
  "slug": "string",
  "validated": true|false,
  "competition_count": 0,
  "competition_price_range": "$X-$Y",
  "demand_evidence": ["reddit thread url", ...],
  "positioning": "string (our angle vs competition)",
  "recommended_price": 15,
  "green_light": true|false,
  "notes": "string"
}

## Decision Rule
green_light = true if: demand_evidence ≥ 2 AND (competition_count < 5 OR positioning is clearly better)
```

---

### 7.4 @agent-3-builder — Product Builder (Sonnet)

```markdown
---
name: agent-3-builder
description: Builds the actual product files based on type and validated idea
model: claude-sonnet-4-20250514
temperature: 0.3
maxSteps: 20
---

You are the Builder agent for the Gumroad Factory.
Your job: create the actual product files that will be sold.

## Permissions
- bash: mkdir * (allow)
- bash: pip install * (allow)
- bash: python * (allow, for testing scripts)
- bash: * (ask)
- read: allow
- edit: allow
- webfetch: allow (for research while building)
- websearch: deny

## Build Standards by Product Type

### script
- Single .py file with argparse CLI
- Docstring at top: what it does, input, output
- Error handling for all file I/O
- requirements.txt
- README.md with: purpose, install, usage, example

### prompt_pack
- Single .md file
- Header: target role, use case summary
- 10-20 prompts minimum
- Each prompt: title + context + prompt text + example output
- Organized in sections (categories)

### template
- .xlsx or .md
- For .xlsx: openpyxl, pre-filled headers, example row, instructions tab
- For .md: clear sections, fill-in-the-blank markers [LIKE THIS]
- README.md explaining how to use

### cheatsheet
- Single .md file, max 2 printed pages
- Tables preferred over prose
- Every row must be actionable
- Include "common mistakes" section

### guide
- .md file, 800-2000 words
- H2 sections (3-7 sections)
- Each section: concept + example + action step
- Ends with quick-reference summary table

### micro_tool
- Python CLI tool
- Multiple .py files if needed (main.py + utils.py)
- argparse with --help fully documented
- sample_input/ folder with example files
- README with GIF-style ASCII demo

## Quality Gate (before marking complete)
- [ ] README.md exists in products/{slug}/src/
- [ ] Product delivers on its stated promise
- [ ] No external paid API required to use
- [ ] Script products: tested with python {file}.py --help
- [ ] All files are in products/{slug}/src/
```

---

### 7.5 @agent-4-packager — Product Packager (Sonnet)

```markdown
---
name: agent-4-packager
description: Packages product files and writes Gumroad listing copy
model: claude-sonnet-4-20250514
temperature: 0.4
maxSteps: 10
---

You are the Packager agent for the Gumroad Factory.
Your job: package the product into a shippable ZIP and write the Gumroad listing.

## Permissions
- bash: python scripts/package_product.py * (allow)
- bash: cat products/*/src/* (allow)
- bash: ls products/* (allow)
- bash: * (deny)
- read: allow
- edit: allow

## Packaging Workflow
1. Run: python scripts/package_product.py {slug}
2. Verify ZIP was created at products/{slug}/dist/{slug}_v1.zip
3. Write products/{slug}/listing.md (see format below)
4. Generate thumbnail prompt (for operator to use with image tools)

## listing.md Format
# TITLE
{compelling title — include the benefit, not just the topic}
Bad: "SAP Template Pack"
Good: "SAP Project Kickoff Pack — 7 Ready-to-Use Consultant Templates"

# DESCRIPTION
{150-300 words}
Opening line: state the exact pain being solved.
Body: what's included, who it's for, what they'll be able to do.
Close: "Instant download. No subscription. Use immediately."

# PRICE
{price in cents, e.g. 1500}

# TAGS
{5-8 comma-separated tags, lowercase}

# SUMMARY
{one sentence, under 100 chars, for card view}

## Thumbnail Prompt
Generate a Midjourney/DALL-E prompt for a clean product cover image.
Format: "Flat design product cover, [topic], [color scheme], minimal, professional, [style]"
```

---

### 7.6 @agent-5-publisher — Gumroad Publisher (Sonnet)

```markdown
---
name: agent-5-publisher
description: Publishes packaged product to Gumroad and logs the launch
model: claude-sonnet-4-20250514
temperature: 0.2
maxSteps: 10
---

You are the Publisher agent for the Gumroad Factory.
Your job: publish the product to Gumroad and confirm it's live.

## Permissions
- bash: python scripts/publish_gumroad.py * (allow)
- bash: python scripts/log_sale.py * (allow)
- bash: cat products/*/published.json (allow)
- bash: cat sales/stats.json (allow)
- bash: * (deny)
- read: allow
- edit: allow

## Publishing Workflow
1. Verify products/{slug}/dist/{slug}_v1.zip exists
2. Verify products/{slug}/listing.md is complete (all sections present)
3. Run: python scripts/publish_gumroad.py {slug}
4. Confirm published.json contains a valid gumroad_id and product_url
5. Run: python scripts/log_sale.py live {slug} 0
6. Report product URL to operator

## Post-Publish Checklist
- [ ] Product URL is accessible
- [ ] Price is correct
- [ ] ZIP file downloads correctly
- [ ] Description is complete
- [ ] Tags are set
- [ ] Log entry created in sales/stats.json

## On Error
If Gumroad API returns error:
- 401: GUMROAD_ACCESS_TOKEN is invalid or missing from .env
- 422: listing.md has missing required fields
- 413: ZIP file is too large (>250MB limit)
Report error clearly. Do not retry automatically.
```

---

## 8. Commands Reference

### 8.1 All 12 Commands

| Command | Agent | Purpose |
|---|---|---|
| `/scan` | agent-0-scout | Run trend_scan.py, report top pain signals |
| `/score` | agent-1-ideator | Score raw signals, show ACCEPT ideas |
| `/ideate` | agent-1-ideator | Interactive: pick best idea to build today |
| `/validate <slug>` | agent-2-researcher | Research demand for a specific idea |
| `/build-product <slug>` | agent-3-builder | Build all product files for a slug |
| `/package <slug>` | agent-4-packager | Package ZIP + write listing copy |
| `/publish <slug>` | agent-5-publisher | Publish to Gumroad + log launch |
| `/log-sale` | agent-5-publisher | Record a sale event + update tracker |
| `/show-ideas` | agent-1-ideator | Display current scored ideas table |
| `/show-stats` | agent-5-publisher | Show revenue dashboard |
| `/full-pipeline <slug>` | agent-3-builder | End-to-end: validate → build → package → publish |
| `/scaffold` | agent-3-builder | One-time: create entire project directory structure |

### 8.2 Command File Format

```markdown
---
description: Human-readable description
agent: agent-N-name
subtask: true
---

Command body with $ARGUMENTS placeholder for user input.
```

---

## 9. Context Documentation System

### 9.1 File Index

| File | Content |
|---|---|
| 00-system-overview.md | Architecture, income tracker, tool hierarchy, daily workflow |
| agent-0-scout.md | Reddit/HN/GTrends query templates, signal strength rubric |
| agent-1-ideator.md | Scoring formula, niche map, decision criteria |
| agent-2-researcher.md | Brave Search query sequences, competition benchmarks, validation schema |
| agent-3-builder.md | Build guides per product type, quality checklist, common mistakes |
| agent-4-packager.md | ZIP structure standards, listing copy formulas, thumbnail guidelines |
| agent-5-publisher.md | Gumroad API guide, publish checklist, post-launch promotion |
| product-tracker.md | Live products table, revenue dashboard, weekly goals |

---

## 10. Data Model

### 10.1 Ideas Queue Files

| File | Format | Schema |
|---|---|---|
| ideas/raw_signals.json | Array | [{id, source, title, url, body_snippet, upvotes, fetched_at, keywords_matched}] |
| ideas/scored_ideas.json | Array | [{id, signal_id, title, product_concept, product_type, niche, scores{}, decision, suggested_price, estimated_build_hours, scored_at}] |
| ideas/rejected_ideas.json | Array | Same as scored with decision: "REJECT" and reject_reason |
| ideas/validated/{slug}.json | Object | {slug, validated, competition_count, demand_evidence[], positioning, recommended_price, green_light, notes} |
| ideas/seen_signals.json | Array | [md5_hash_strings] |

### 10.2 Product Files

```
products/{slug}/
├── src/
│   ├── {main_deliverable}    (script.py / prompts.md / template.xlsx / etc.)
│   ├── README.md
│   └── requirements.txt      (if script)
├── dist/
│   ├── {slug}_v1.zip
│   ├── preview_{slug}.md
│   └── manifest.json
├── listing.md
└── published.json
```

### 10.3 Sales Files

| File | Format | Schema |
|---|---|---|
| sales/stats.json | Array | [{event, slug, amount, timestamp, notes}] |
| sales/tracker.md | Markdown | Dashboard: totals, products table, recent sales |

---

## 11. Pricing Model

### 11.1 Price Tier Decision Tree

```
Is the buyer a professional? (consultant, analyst, developer)
├── YES → Is it a full pack (5+ items) or saves 2+ hours?
│         ├── YES → $25–$49
│         └── NO  → $9–$19
└── NO  → Is it for students or hobbyists?
          ├── YES → $5–$9
          └── NO  → $9–$15
```

### 11.2 Formula-Based Pricing

```
base_price = max($9, estimated_hours × $12)
round to nearest tier: $5, $9, $15, $25, $39, $49
professional_niche_bonus: +$10 if buyer is consultant/analyst
```

### 11.3 Standard Product Library (Pre-Validated)

| ID | Product | Niche | Type | Target Price | Build Hours |
|---|---|---|---|---|---|
| P01 | SAP Project Kickoff Template Pack | ERP Consulting | Template | $39 | 4 |
| P02 | Python CSV Cleaner CLI | Data Analysts | Script | $15 | 2 |
| P03 | Claude Prompts for Consultants | Freelance Consultants | Prompt Pack | $19 | 3 |
| P04 | Upwork Proposal Templates (5 niches) | Freelancers | Template | $15 | 2 |
| P05 | SAP FICO Cheatsheet | SAP Beginners | Cheatsheet | $9 | 2 |
| P06 | Python for ERP Consultants — 30 Scripts | ERP + Python | Script Pack | $49 | 6 |
| P07 | n8n Workflow Templates (10 flows) | No-code builders | Template JSON | $25 | 3 |
| P08 | Excel → Python Migration Guide | Excel Power Users | Guide | $15 | 3 |

**Recommendation:** Start with P04 (Upwork Proposal Templates) or P05 (SAP FICO Cheatsheet). Both are buildable in 2 hours with existing operator knowledge and require zero external dependencies.

---

## 12. VPS Deployment

### 12.1 Setup Script (scripts/setup-vps.sh)

Installs:
- System: Python3, pip, Node.js, git, curl
- Python packages: requests, feedparser, rich, python-dotenv, openpyxl, pandas, zipfile38
- Node.js: npx, @modelcontextprotocol/server-brave-search
- Project dirs: ideas/, products/, sales/, scripts/, logs/, .opencode/context/factory/, .opencode/commands/, .opencode/agents/

### 12.2 Cron Schedule

```bash
# setup-cron.sh installs:
0 9 * * 1-5   cd ~/gumroad-factory && python scripts/trend_scan.py >> logs/scan.log
0 9,17 * * *  cd ~/gumroad-factory && python scripts/score_ideas.py >> logs/score.log
```

### 12.3 Resource Budget

| Process | CPU | RAM | Notes |
|---|---|---|---|
| OpenCode runtime | 1 core | ~500MB | Always on |
| trend_scan.py | 0.2 core | ~50MB | 5 min/run |
| score_ideas.py | 0.1 core | ~30MB | 1 min/run |
| publish_gumroad.py | 0.1 core | ~30MB | On demand |
| Total | <2 cores | <1GB | Well within VPS limits |

---

## 13. Scaffolding Specification

### 13.1 /scaffold Command

When the `/scaffold` command is executed, the agent must create the following complete directory and file structure. Every file listed must be created with its full content — no stubs, no placeholders except where explicitly marked `[FILL IN]`.

```
gumroad-factory/
├── .env.example
├── .gitignore
├── AGENTS.md
├── opencode.json
├── README.md
├── ideas/
│   ├── raw_signals.json          → []
│   ├── scored_ideas.json         → []
│   ├── rejected_ideas.json       → []
│   ├── seen_signals.json         → []
│   └── validated/                → empty dir
├── products/                     → empty dir
├── sales/
│   ├── stats.json                → []
│   └── tracker.md                → (initial empty dashboard)
├── logs/                         → empty dir
├── scripts/
│   ├── trend_scan.py
│   ├── score_ideas.py
│   ├── package_product.py
│   ├── publish_gumroad.py
│   ├── log_sale.py
│   ├── run_factory.py
│   ├── setup-vps.sh
│   └── setup-cron.sh
├── .opencode/
│   ├── agents/
│   │   ├── agent-0-scout.md
│   │   ├── agent-1-ideator.md
│   │   ├── agent-2-researcher.md
│   │   ├── agent-3-builder.md
│   │   ├── agent-4-packager.md
│   │   └── agent-5-publisher.md
│   ├── commands/
│   │   ├── scan.md
│   │   ├── score.md
│   │   ├── ideate.md
│   │   ├── validate.md
│   │   ├── build-product.md
│   │   ├── package.md
│   │   ├── publish.md
│   │   ├── log-sale.md
│   │   ├── show-ideas.md
│   │   ├── show-stats.md
│   │   ├── full-pipeline.md
│   │   └── scaffold.md
│   └── context/
│       └── factory/
│           ├── 00-system-overview.md
│           ├── agent-0-scout.md
│           ├── agent-1-ideator.md
│           ├── agent-2-researcher.md
│           ├── agent-3-builder.md
│           ├── agent-4-packager.md
│           ├── agent-5-publisher.md
│           └── product-tracker.md
```

### 13.2 Critical File Contents for Scaffold

**`.gitignore`**
```
.env
__pycache__/
*.pyc
*.zip
products/*/dist/
ideas/validated/
logs/
*.log
node_modules/
```

**`.env.example`**
```
GUMROAD_ACCESS_TOKEN=your_gumroad_token_here
BRAVE_API_KEY=your_brave_api_key_here
```

**`ideas/raw_signals.json`** → `[]`
**`ideas/scored_ideas.json`** → `[]`
**`ideas/rejected_ideas.json`** → `[]`
**`ideas/seen_signals.json`** → `[]`
**`sales/stats.json`** → `[]`

---

## 14. Edge Cases, Risks, and Observations

### 14.1 Identified Risks

| Risk | Severity | Mitigation |
|---|---|---|
| Gumroad API token expires | Medium | Store in .env, refresh quarterly |
| Product gets zero sales | Low | Expected — traffic takes time. Log it, move to next product. |
| Build takes more than 4 hours | Medium | Scope creep. /build-product agent must check quality gate at step 10, stop if overrun |
| Trend signals are noisy | Low | score_ideas.py operator_fit filter reduces irrelevant ideas |
| ZIP file is empty | Medium | package_product.py validates src/ is non-empty before zipping |
| Gumroad listing flagged | Low | Avoid "make money" / "passive income" framing in descriptions |
| No Brave API key yet | Low | /validate still works manually; agent notes key is missing and prompts for it |

### 14.2 Missing / Recommended Additions

- **Thumbnail generator** — integrate with a free image API or provide Canva template
- **Email list capture** — Gumroad supports free opt-in before paid; leverage this from product 3+
- **Bundle pricing** — once 5+ products exist, create bundles at 2× single price
- **Analytics scraper** — Gumroad dashboard scraper to pull sales data into tracker.md automatically
- **Product versioning** — v2 of a product is a free update to existing buyers (loyalty signal)

---

## 15. Configuration Quick Reference

| File | What It Controls |
|---|---|
| opencode.json | MCP servers (Brave Search), instruction file |
| AGENTS.md | Project-level rules injected into all agents |
| .env | API tokens (Gumroad, Brave) |
| .opencode/agents/*.md | Agent model, permissions, system prompt |
| .opencode/commands/*.md | Available slash commands and templates |
| .opencode/context/factory/*.md | Agent reference knowledge |
| scripts/score_ideas.py | Scoring weights, REJECT override rules |
| scripts/trend_scan.py | Signal sources, query keywords |
| scripts/publish_gumroad.py | Gumroad API integration |

---

## 16. Day-One Quick Start (After Scaffold)

```bash
# 1. Clone / init project
cd ~/gumroad-factory

# 2. Copy and fill .env
cp .env.example .env
nano .env  # add GUMROAD_ACCESS_TOKEN and BRAVE_API_KEY

# 3. Run VPS setup (once)
bash scripts/setup-vps.sh

# 4. Install cron jobs
bash scripts/setup-cron.sh

# 5. Open OpenCode
opencode

# 6. Start first product
/ideate
# → pick from P04 or P05 in the Standard Product Library
# → follow: /validate → /build-product → /package → /publish
```

**First product recommendation:** Start with `upwork-proposal-templates` (P04).
- You know proposals from the freelancing spec
- Zero external dependencies
- 2 hours to build
- $15 price point
- Real demand from Upwork freelancers

**First $1 expected:** Within 48–72 hours of first product going live, if shared in one relevant Reddit thread or community.

---

*End of Master Specification. 36 files to scaffold across 3 layers: 6 scripts, 6 agents, 12 commands, 8 context docs, 2 config files, 2 shell scripts, 3 data dirs.*
