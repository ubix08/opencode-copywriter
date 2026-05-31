# PRODUCT FACTORY — MASTER SYSTEM SPECIFICATION v11.0

**Lean Autonomous Knowledge Product Engine**
**clawd-Native · 6-Agent · Contradiction-Driven · Self-Improving**

---

## DOCUMENT PURPOSE AND SCOPE

This document is the complete, self-contained, self-explanatory master specification for Product Factory v11.0. It supersedes v10.0 entirely. Every component, configuration, agent identity, flow definition, data contract, quality gate, decision rule, scoring mechanism, file path convention, and operating procedure required to deploy and run the factory is defined within this document.

No external reference is required. No prior version is assumed. Every concept is defined on first use.

**What changed from v10.0 and why** is documented in Appendix A. The rest of this document does not reference v10.0 — it stands alone.

---

## TABLE OF CONTENTS

1. System Overview and Philosophy
2. Architecture: The Three-Layer Stack
3. Execution Runtime: clawd Primitives Reference
4. Team Configuration
5. Shared Workspace Specification
6. Data Flow Catalog (9 flows)
7. Agent Catalog (6 agents)
8. Pipeline Protocol: Stage-by-Stage
9. Scoring and Gate Engine
10. Operating Modes
11. Knowledge Base and Memory System
12. Feedback, Learning, and Experimentation
13. File Path Conventions
14. Output Contracts
15. Quality Standards
16. Model Allocation and Cost Management
17. Failure Conditions and Escalation
18. Deployment Checklist

---

## 1. SYSTEM OVERVIEW AND PHILOSOPHY

### 1.1 What This System Does

The Product Factory is a multi-agent AI system that autonomously discovers unsolved technical problems with commercial demand, transforms those problems into professionally written practitioner guides (20–30 pages, 8,000–15,000 words), and prepares them for sale as digital products in the $17–$47 tier. The system runs continuously, learning from each product's performance to improve future selections and outputs.

### 1.2 Core Design Principles

**Flows handle data volume; agents handle reasoning.** Web scraping, search batching, SQL queries, per-item classification, embedding, and PDF generation belong in flows — deterministic DAGs that process high item counts cheaply with haiku-class models. Qualitative judgment, synthesis, writing, and decisions that require understanding context belong in agents. This boundary is respected throughout. The classification nodes inside flows still use LLMs, and that is acknowledged — what flows do not do is make qualitative decisions about output quality or strategic direction.

**Categorical classification, not LLM-generated scores.** LLM nodes in flows classify items into named categories ("knowledge_gap", "chronic", "intermediate"). A JavaScript node computes the score from those categories using a fixed weighted-sum formula. Scores are explainable in plain English because every component has a name and a defined value. No floating-point "quality score" is ever produced by an LLM.

**Six agents, not nine.** v10.0's Scout + Architect were tightly coupled decisions that one agent makes better in a single reasoning pass. Researcher + Analyzer were sequential passes over the same data, doubling the token cost for redundant parsing. Writer + Optimizer creates a worse guide than a writer whose prompt embeds clarity discipline from the start. The collapsed agents — Strategist, Research Engine, Writer — are not lower quality. They are more focused, with better-defined prompts that eliminate the handoff overhead.

**Adaptive revision, not blind retry.** When the verifier finds issues, the revision mode is matched to the issue type: minor fixes for small errors, section rewrites for localized failures, structural rewrites (which escalate to the Framework Builder) for framework-level failures. Two blind revision cycles wasting the full writer session are replaced with one targeted cycle matched to the actual problem.

**Probabilistic gating at the demand threshold.** The demand score is computed from noisy categorical inputs. A hard cutoff at 7.0 creates false negatives at 6.8 and false positives just over the line. v11 uses a confidence-adjusted gate: topics with high-confidence signals proceed at 6.5; topics with low-confidence signals require 7.5. This reduces good-topic rejections without lowering the actual standard.

**Contradiction-driven insight generation.** Aggregating 20 sources and summarizing them produces a guide that could have been assembled from the docs. Resolving contradictions between sources — explaining why two practitioners got different results from the same approach — produces insight that does not exist anywhere else. The Framework Builder is required to do this work, not just synthesize consensus.

**CONTEXT.md is the living standards document.** The learning flywheel updates CONTEXT.md after each product cycle based on performance data. CONTEXT.md updates are versioned, validated before application, and human-approved for changes that affect writing rules or gate thresholds. Changes to recommendations (tone guidance, domain prioritization) can auto-apply. Changes to hard gates require human approval.

**Experimentation is built in.** The packaging agent produces two title variants and the feedback system tracks which performs better. Price tier recommendations from the demand scan are the default, but the system supports A/B price testing across consecutive products in the same domain. Learning is causal where possible: a product that changed framework type and improved rating is attributed to framework type, not topic quality, when topic quality was held constant.

### 1.3 System Identity

The Product Factory v11.0 is a lean, production-capable autonomous knowledge business. It is optimized for the intersection of throughput and quality — not maximum possible quality at any cost, and not maximum throughput regardless of quality. The operating constraint is: every product that leaves this system must be worth the price the buyer paid.

---

## 2. ARCHITECTURE: THE THREE-LAYER STACK

```
┌──────────────────────────────────────────────────────────────────────┐
│  LAYER 1 — HUMAN INTERFACE                                           │
│                                                                      │
│  clawd team product-factory "Build a guide on X for Y audience"     │
│  OR cron trigger (Sunday 3:30am — weekly autonomous run)            │
│  OR event trigger (opportunity_mined fires from intelligence flows)  │
└────────────────────────────┬─────────────────────────────────────────┘
                             │
┌────────────────────────────▼─────────────────────────────────────────┐
│  LAYER 2 — COORDINATOR: FORGE (orchestratorAgent)                    │
│                                                                      │
│  Core responsibilities:                                              │
│  • Selects opportunity (autonomous) or accepts brief (manual)        │
│  • Runs data flows via run_flow() — never does data work itself      │
│  • Reads structured flow output from shared/ directory               │
│  • Makes all gate decisions: proceed / revise / reject / escalate    │
│  • Delegates work via send_message() to 5 specialist agents          │
│  • Classifies revision mode when verifier finds issues               │
│  • Updates shared/STATUS.md and shared/DECISIONS.md at every step    │
│  • Calls stage_for_review() when pipeline completes                  │
│  • Never writes content, never solves technical problems             │
└────────┬──────────────────────────────────────────────┬──────────────┘
         │ run_flow()                                   │ send_message()
         ▼                                             ▼
┌──────────────────────┐         ┌────────────────────────────────────┐
│  LAYER 3A — FLOWS    │         │  LAYER 3B — SPECIALIST AGENTS      │
│                      │         │                                    │
│  opportunity-        │         │  Strategist   → strategy.md       │
│    consolidator      │         │  (Scout+Architect merged)          │
│  demand-scan         │         │                                    │
│  topic-research      │         │  Research Engine → intelligence.md │
│  kb-query            │         │  (Researcher+Analyzer merged)      │
│  verify-sections     │         │                                    │
│  coherence-check     │         │  Framework Builder → framework.md  │
│  format-pdf          │         │                                    │
│  feedback-collector  │         │  Writer → guide-draft.md           │
│  learning-update     │         │  (writes clean + compressed)       │
│  kb-indexer          │         │                                    │
│                      │         │  Verifier → audit.md               │
│  All parallel where  │         │  (3-layer + coherence)             │
│  possible. Output    │         │                                    │
│  to shared/ at       │         │  Packager → product-manifest.json  │
│  predictable paths.  │         │                                    │
└──────────────────────┘         └────────────────────────────────────┘
```

### 2.1 The Parallelism Rule

Flows that do not depend on each other run in parallel. FORGE fires them simultaneously and waits on both before proceeding. Specifically:

- `demand-scan` and `kb-query` run in parallel after topic is known.
- `topic-research` and `kb-query` (if not already run) run in parallel.
- `verify-sections` (flow) runs concurrently with FORGE reading the draft for word count and structure checks.

No agent runs in parallel with another agent. Agents are serialized because each builds on the prior agent's output.

### 2.2 The Acknowledged Boundary: LLM Classification in Flows

Classification inside flows still uses LLM inference. The system does not claim "pure determinism" — it claims that scores are computed deterministically from categorical inputs. Those inputs are produced by LLM classification, which carries inference uncertainty. This is why:

- The demand gate uses confidence-adjusted thresholds rather than a single hard cutoff.
- Every scored opportunity carries its `score_breakdown` in named fields, not a float alone.
- The coordinator reads the breakdown when making decisions, not just the number.

This is the honest version of "deterministic scoring": the arithmetic is deterministic; the inputs acknowledge their classification source.

---

## 3. EXECUTION RUNTIME: CLAWD PRIMITIVES REFERENCE

### 3.1 Flow Runner

The clawd flow runner executes Directed Acyclic Graphs (DAGs) of processing nodes. Flows are defined as JSON files in `~/.clawd/flows/`. Each node receives an input packet, transforms it, and passes an output packet forward. Flows are stateless between runs. Flow state is persisted via file_write nodes to `shared/` paths.

**Node types used in this factory:**

| Node Type | Purpose | Key Config Fields |
|-----------|---------|-------------------|
| `trigger.manual` | Start flow on explicit call | — |
| `trigger.cron` | Start flow on schedule | `cron: "0 3 * * 0"` |
| `trigger.event` | Start flow when event fires | `event: "event_name"` |
| `llm` | LLM inference call | `model`, `prompt`, `systemPrompt`, `outputFormat` |
| `classify` | LLM classification into named categories | `categories`, `model`, `field` |
| `http_batch` | Parallel HTTP requests | `urls`, `concurrency`, `delayMs`, `timeout` |
| `web_fetch` | Single URL fetch | `url`, `timeout` |
| `foreach` | Iterate over array | `concurrency` |
| `sqlite_exec` | Run SQL against SQLite | `db`, `query`, `params` |
| `file_write` | Write content to disk | `path`, `content` |
| `javascript` | Run a JS expression | `code` |
| `python` | Run a Python script | `script` |
| `bash` | Run a shell command | `command` |
| `embed` | Generate text embeddings | `model` |
| `quota_gate` | Skip LLM if quota reached | `limit` |
| `aggregate` | Collect array items | — |
| `split` | Split array into batches | `batchSize` |
| `sort` | Sort array by field | `field`, `order` |
| `unique` | Deduplicate array | `field` |
| `pick` | Select fields from object | `fields` |
| `set` | Compute/assign fields | `fields` (JS expressions) |
| `condition` | Branch on boolean | `expression` |
| `emit_event` | Fire event onto bus | `event`, `payload` |

**Timeout defaults:** Set `timeout: 3600` on topic-research. All other flows default to 300 seconds unless specified.

**Output convention:** Every factory flow writes its primary output to `~/.clawd/teams/product-factory/shared/` at a documented predictable path. No flow writes to an agent's output directory.

### 3.2 Agent Sessions

Agent sessions are multi-turn conversations governed by a SOUL.md file. Each specialist agent is `persistent: false` (fresh context each invocation). FORGE is `persistent: true` (maintains context across the full production run). Each agent has a `maxTurns` limit; sessions that exceed this limit close and FORGE treats this as a BLOCKED outcome.

### 3.3 Team System Primitives

**SharedWorkspace:** Auto-creates `shared/GOALS.md`, `shared/STATUS.md`, `shared/DECISIONS.md`, `shared/CONTEXT.md` at team initialization. Every agent can read and write these via `shared_memory_read` and `shared_memory_write` tools.

**send_message(agentId, mode, message, prior_outputs):**
- `mode: "work"` — assigns a task; agent writes to its `outputFile` and returns the path.
- `mode: "reply"` — synchronous Q&A; use for short clarification only.
- `prior_outputs` — map of `{ agentId: outputFilePath }` for handoff context.

**run_flow(flowId, input):** Triggers a registered flow, waits for completion, returns the run record. FORGE then reads the flow's output file from `shared/`.

**stage_for_review(payload):** Marks output as ready for human review. Pauses the autonomous loop until human responds.

### 3.4 Event Bus

| Event | Emitter | Listener |
|-------|---------|----------|
| `opportunity_mined` | reddit-pain-miner, hn-pain-miner | opportunity-consolidator |
| `product_complete` | FORGE (after stage_for_review approval) | kb-indexer, learning-update |
| `feedback_collected` | feedback-collector | learning-update |
| `learning_updated` | learning-update | FORGE (weekly meta-learning step) |
| `context_update_proposed` | learning-update | FORGE (approval required for gate changes) |

---

## 4. TEAM CONFIGURATION

**File location:** `~/.clawd/teams/product-factory/team.json`

```json
{
  "id": "product-factory",
  "name": "Product Factory v11",
  "description": "Lean autonomous knowledge product engine — 6 agents, contradiction-driven, self-improving.",
  "orchestratorAgent": "forge",
  "sharedWorkspace": true,
  "agents": [
    {
      "id": "forge",
      "name": "FORGE",
      "description": "Product Factory Coordinator — routes, gates, classifies revision mode",
      "soulFile": "forge/SOUL.md",
      "model": "claude-sonnet-4-6",
      "persistent": true,
      "maxTurns": 60,
      "timeoutSeconds": 600,
      "tools": "full",
      "customTools": ["run_flow", "list_flows", "flow_status", "flow_cancel"]
    },
    {
      "id": "strategist",
      "name": "Strategist",
      "description": "Scope + Structure — validates audience, defines scope, designs 7-section skeleton in one pass",
      "soulFile": "strategist/SOUL.md",
      "model": "claude-sonnet-4-6",
      "persistent": false,
      "maxTurns": 20,
      "timeoutSeconds": 240,
      "tools": "full"
    },
    {
      "id": "research-engine",
      "name": "Research Engine",
      "description": "Intelligence Builder — synthesizes pre-fetched sources into corpus AND extracts solution patterns",
      "soulFile": "research-engine/SOUL.md",
      "model": "claude-sonnet-4-6",
      "persistent": false,
      "maxTurns": 30,
      "timeoutSeconds": 360,
      "tools": "full"
    },
    {
      "id": "framework-builder",
      "name": "Framework Builder",
      "description": "Methodology Creator — resolves contradictions, builds named framework with decision system",
      "soulFile": "framework-builder/SOUL.md",
      "model": "claude-sonnet-4-6",
      "persistent": false,
      "maxTurns": 20,
      "timeoutSeconds": 300,
      "tools": "full"
    },
    {
      "id": "writer",
      "name": "Writer",
      "description": "Guide Author — writes clean, compressed, decision-driven practitioner guide in one pass",
      "soulFile": "writer/SOUL.md",
      "model": "claude-sonnet-4-6",
      "persistent": false,
      "maxTurns": 35,
      "timeoutSeconds": 600,
      "tools": "full"
    },
    {
      "id": "verifier",
      "name": "Verifier",
      "description": "4-Layer Auditor — accuracy, usability, decision quality, and global coherence",
      "soulFile": "verifier/SOUL.md",
      "model": "claude-haiku-4-5",
      "persistent": false,
      "maxTurns": 20,
      "timeoutSeconds": 300,
      "tools": "full"
    },
    {
      "id": "packager",
      "name": "Packager",
      "description": "Product Assembler — manifest, two title variants, marketing copy, pricing",
      "soulFile": "packager/SOUL.md",
      "model": "claude-haiku-4-5",
      "persistent": false,
      "maxTurns": 12,
      "timeoutSeconds": 180,
      "tools": "full"
    }
  ]
}
```

---

## 5. SHARED WORKSPACE SPECIFICATION

**Root path:** `~/.clawd/teams/product-factory/shared/`

### 5.1 GOALS.md — Active Product Brief

Written by FORGE at the start of every pipeline run. Overwritten for each new run.

```markdown
# Active Product Brief

**Run ID:** [YYYYMMDD-HHMMSS]
**Mode:** [brief | autonomous]
**Topic:** [exact topic string]
**Source:** [human-provided | opportunity-pool]

## Target Audience
[precise description — experience level, role, tool context, one sentence that 80% of readers confirm]

## Core Problem
[exact problem statement in practitioner language — what breaks, where, for whom]

## Desired Outcome
[what the reader can DO after reading — specific action, not vague improvement]

## Confirmed Scope
[what is IN scope — from strategist, or from human brief]

## Scope Exclusions
[what is explicitly NOT covered — prevents scope creep]

## Value Hypothesis
[why this guide is worth paying for — one sentence connecting pain to money]

## Demand Signal Summary
[demand score, confidence level, 3 key signals from demand-report.json]

## Price Tier
[recommended range and midpoint — from demand-report.json]
```

### 5.2 STATUS.md — Pipeline State

Updated by FORGE at every stage transition. Always current.

```markdown
# Pipeline Status

Run: [RUN_ID] | Started: [ISO timestamp] | Mode: [mode]
Topic: [topic]

**Current Stage:** [DEMAND_SCAN | STRATEGY | RESEARCH | FRAMEWORK | WRITING | VERIFICATION | PACKAGING | COMPLETE | FAILED | ESCALATED]
**Current Action:** [one sentence — what is happening right now]

## Stage History
[DEMAND_SCAN] PASS score:8.4 conf:high → 2026-03-25T14:00Z
[STRATEGY] COMPLETE scope confirmed — 2026-03-25T14:06Z
[RESEARCH] COMPLETE 23 sources — 2026-03-25T14:22Z
[FRAMEWORK] COMPLETE BRIDGE method named — 2026-03-25T14:35Z
[WRITING] IN PROGRESS — 2026-03-25T14:37Z
```

### 5.3 DECISIONS.md — Gate Decision Log

Append-only. Every gate outcome, revision classification, and escalation logged with timestamp and full reasoning.

```markdown
# Decision Log

## [2026-03-25T14:00Z] DEMAND GATE — PASS
Score: 8.4, confidence: high. Gate: score >= 6.5 with high confidence → proceed.
Signals: 380 monthly searches, 21 forum threads, no authoritative guide found.
Action: Proceeding to Strategist.

## [2026-03-25T14:06Z] STRATEGY GATE — PASS
Audience: intermediate Linux developers with Docker installed who hit networking failures.
Scope confirmed. Exclusions: rootless Docker, Windows/Mac, Kubernetes overlays.
Action: Running topic-research and kb-query in parallel.

## [2026-03-25T15:02Z] VERIFICATION GATE — FAIL
Accuracy: 88% (below 90%). Usability: 94%. Decision quality: 93%. Coherence: 91%.
Failure mode: LOCALIZED — Section 3 command errors (critical×2, warning×1). Other sections pass.
Revision mode: SECTION_REWRITE (Section 3 only). Not a full draft revision.
Action: Sending Section 3 revision brief to Writer.

## [2026-03-25T15:25Z] VERIFICATION GATE — PASS
Accuracy: 95%. Usability: 94%. Decision quality: 93%. Coherence: 92%. All >= 90%.
Action: Proceeding to Packaging.
```

### 5.4 CONTEXT.md — Permanent Team Standards

**Version-controlled.** Each update carries a version number, timestamp, and update scope. Changes to writing rules or quality thresholds require FORGE approval before application. Tone/domain guidance auto-applies.

```markdown
# Product Factory — Team Standards
# Version: 1.4 | Updated: 2026-03-20 | Approved: yes
# Change from v1.3: Added "acronym frameworks strongly preferred" based on 6-product performance data (avg rating +0.4).

This file is injected into every agent session. Read these standards before beginning any task.
You are a specialist in a lean 6-agent production team. Your job is precise and bounded.

## What We Build

Practitioner-grade technical mini-guides: 20–30 pages, 8,000–15,000 words, $17–$47.
Readers are practitioners with a specific problem. They paid for this. It must work.

## Writing Rules (Mandatory)

1. No filler. Every sentence adds information or advances the reader. Remove all others.
2. No generic language. "Keep in mind that" is forbidden. State the thing directly.
3. All commands exactly executable in the stated environment. No placeholders without substitution instructions.
4. Practitioner voice: write like a senior developer explaining to a peer. Not academic. Not corporate.
5. Outcome before explanation. Open every section with what the reader will be able to do, then explain why.
6. Decision guidance is mandatory. Every choice between approaches requires: "Use X when [specific condition]. Use Y when [specific condition]."
7. State consequence of wrong choice. If the reader picks the wrong approach, what breaks? Say it.

## Style Notes (Updated from performance data)

- Acronym frameworks (e.g., "The BRIDGE Method") show significantly higher completion rates than numbered-step frameworks. Prefer acronym frameworks. Synthesizer should attempt to form an acronym before other naming approaches.
- Docker, Linux networking, Python tooling topics show highest satisfaction. Deprioritize Kubernetes (high refund risk from complexity mismatch).
- $32 midpoint (tier $27-$37) is the strongest price point currently. Reserve $47 for topics with 30+ source corpus.

## Output Contract

Every specialist produces a named output file at the exact path in their briefing.
Outputs are complete. A BLOCKED status report is preferable to a partial output.
BLOCKED format: first line "STATUS: BLOCKED", second line "REASON: [specific]".

## Prohibited Patterns

- Never write "leverage," "utilize," "seamlessly," "robust," or "cutting-edge."
- Never end a section with a forward-reference transition sentence.
- Never claim a command works without verifying it against the stated environment and corpus.
- Never recommend an approach without stating when NOT to use it.
- Never write "as mentioned above" — every section must stand independently.

## Quality Floor

A guide passes if a competent practitioner could follow it to solve the stated problem
without consulting any external resource. If external lookup is required to execute any step,
that information must be in the guide.

## Price Tier Reference (Current)

$17–$27: beginner-intermediate, well-documented problem, narrow scope
$27–$37: intermediate, multiple approaches, moderate complexity ← default tier
$37–$47: advanced, multi-system synthesis, expert decision frameworks, 30+ source corpus
```

### 5.5 Run-Specific Files in shared/

These files are created per-run by flows. Overwritten at each new pipeline run.

| File | Written By | Read By | Contents |
|------|-----------|---------|----------|
| `shared/demand-report.json` | demand-scan flow | FORGE, Strategist | Demand score, confidence, signals, price tier |
| `shared/research-raw.json` | topic-research flow | Research Engine | Structured findings from 15–30 sources |
| `shared/kb-matches.json` | kb-query flow | Research Engine, Framework Builder | Matching KB entries for this domain |
| `shared/section-audit.json` | verify-sections flow | Verifier | Per-section accuracy scores and issues |
| `shared/TOP_OPPORTUNITIES.json` | opportunity-consolidator | FORGE (autonomous mode) | Ranked scored opportunities |
| `shared/learning-report.json` | learning-update flow | FORGE (meta-learning step) | Pattern statistics, CONTEXT.md update proposals |
| `shared/context-update-proposal.json` | learning-update flow | FORGE (approval gate) | Proposed changes to CONTEXT.md with rationale |

---

## 6. DATA FLOW CATALOG

### 6.1 Flow: opportunity-consolidator

**Purpose:** Merge ranked opportunities from all miner databases into `TOP_OPPORTUNITIES.json` for FORGE's autonomous selection.

**Trigger:** `trigger.event` on `opportunity_mined` OR `trigger.cron: "0 3 * * 0"` (Sundays, 3am).

**Timeout:** 120s.

**Node sequence:**

```
trigger
→ sqlite_exec (reddit-pain-miner/opportunities.db — all rows where proceed=true, last 30 days)
→ set (add source: "reddit" to each row)
→ [PARALLEL]
  sqlite_exec (hn-pain-miner/opportunities.db — all rows where proceed=true, last 30 days)
  → set (add source: "hn" to each row)
→ aggregate (merge both arrays)
→ javascript (apply source weight: reddit×1.0, hn×1.1; adjusted_score = raw_score × source_weight)
→ sqlite_exec (shared/products.db — get embeddings of all existing products)
→ python (compute cosine similarity of each opportunity embedding vs all product embeddings; flag not_in_catalog=false if similarity > 0.85)
→ javascript (filter: only rows where not_in_catalog=true AND monetization_viable=true AND raw_score >= 2.0)
→ javascript (add kb_depth_bonus: for each opportunity, query shared/knowledge-base.db for matching domain count; bonus = min(match_count/10, 0.5); final_score = adjusted_score + kb_depth_bonus)
→ sort (by final_score, descending)
→ javascript (take top 10, add rank field 1–10)
→ file_write (shared/TOP_OPPORTUNITIES.json)
→ emit_event (opportunity_pool_ready)
```

**Output schema — TOP_OPPORTUNITIES.json:**

```json
[
  {
    "rank": 1,
    "label": "Docker localhost unreachable from container",
    "source": "reddit",
    "raw_score": 2.65,
    "adjusted_score": 2.65,
    "kb_depth_bonus": 0.07,
    "final_score": 2.72,
    "proceed": true,
    "score_breakdown": {
      "evidence_weight": "3.0 (18 posts, capped)",
      "blocker_type": "knowledge_gap → 3",
      "solution_gap": "yes_workaround → 2",
      "audience": "intermediate → 2",
      "recurrence": "chronic → 3"
    },
    "confidence": "high",
    "flags": {
      "high_competition_risk": false,
      "low_evidence": false,
      "niche_audience_risk": false
    },
    "kb_depth": 7,
    "product_angle": "info_product",
    "monetization_viable": true,
    "not_in_catalog": true,
    "sample_quotes": ["I can ping the container but localhost:PORT times out", "Works on Mac, broken on Ubuntu"]
  }
]
```

---

### 6.2 Flow: demand-scan

**Purpose:** Score commercial demand for a topic using web signals. Returns a score with confidence level.

**Trigger:** `trigger.manual`. Called by FORGE: `run_flow("demand-scan", { topic, audience })`.

**Timeout:** 120s.

**Node sequence:**

```
trigger (input: { topic, audience })
→ llm (haiku-4-5; generate 5 search queries: monthly search volume, forum activity, competitor gaps, error message variants, related practitioner language; output JSON array)
→ http_batch (Serper.dev; concurrency: 5; all 5 queries in parallel)
→ foreach (per search result)
  → javascript (extract: title, snippet, source_type, date_approx)
→ aggregate
→ classify (haiku-4-5; classify all signals into:
    search_volume: "high" | "medium" | "low"
    forum_frequency: "high" | "medium" | "low"    — high >= 10 signals, medium >= 5
    competition_gap: "none" | "weak" | "strong"
    audience_confirmed: "yes" | "no"
    confidence: "high" | "medium" | "low"          — high = 4+ strong signals, medium = 2-3, low = fewer)
→ javascript (compute demand score:
    const s = { high:3, medium:2, low:1 };
    const g = { none:3, weak:2, strong:1 };
    const a = { yes:1, no:0 };
    const raw = s[search_volume] + s[forum_frequency] + g[competition_gap] + a[audience_confirmed];
    demand_score = (raw / 10) * 10;   // max=10, scale is already 0-10
    proceed = (demand_score >= 7.5)
           || (demand_score >= 6.5 && confidence === "high");
    )
→ llm (haiku-4-5; given signals and score, recommend: price_tier, recommended_angle; output JSON)
→ javascript (assemble demand-report.json)
→ file_write (shared/demand-report.json)
```

**Output schema — demand-report.json:**

```json
{
  "topic": "Docker container networking on Ubuntu",
  "audience": "intermediate Linux developers",
  "demand_score": 8.4,
  "confidence": "high",
  "proceed": true,
  "gate_rule_applied": "score >= 6.5 with high confidence",
  "score_breakdown": {
    "search_volume": "high (3)",
    "forum_frequency": "high (3)",
    "competition_gap": "weak (2)",
    "audience_confirmed": "yes (1)"
  },
  "key_signals": [
    "380 monthly searches estimated from snippet patterns",
    "21 forum threads on r/docker and r/linux in 30 days",
    "No authoritative guide found — top 3 results are 2+ year old blog posts"
  ],
  "competition_assessment": "weak — 3 blog posts exist, none comprehensive, all outdated",
  "recommended_angle": "Practical reference guide for intermediate developers hitting networking failures on Linux",
  "price_tier": "$27-$37",
  "price_midpoint": 32,
  "price_rationale": "Intermediate complexity, weak competition, strong practitioner demand"
}
```

**Gate rule applied by FORGE:**

```
proceed = (demand_score >= 7.5)
       OR (demand_score >= 6.5 AND confidence = "high")

Reject conditions:
  demand_score < 6.5                → REJECT regardless of confidence
  demand_score 6.5–7.5 AND confidence "low" or "medium" → REJECT, log, try next
```

---

### 6.3 Flow: topic-research

**Purpose:** Fetch, extract, and structure intelligence from 15–30 sources. This is the intelligence acquisition step — the Research Engine agent processes this output, it does not do the fetching.

**Trigger:** `trigger.manual`. Called by FORGE: `run_flow("topic-research", { topic, scope, audience })`.

**Timeout:** 3600s.

**Node sequence:**

```
trigger (input: { topic, scope, audience })
→ llm (sonnet-4-6; generate 10 search queries covering: primary problem, 3 solution approach variants, common failure modes, environment-specific issues, official documentation gaps, forum angles, advanced configuration, tool version context; output JSON array with {query, intent, source_type_target})
→ http_batch (Serper.dev; concurrency: 5; delayMs: 1500; all 10 queries)
→ foreach (per search result; concurrency: 3)
  → condition (filter: skip paywalled sites, video-only pages, pages returning 4xx/5xx)
  → web_fetch (timeout: 15s)
  → llm (haiku-4-5; extract from this page:
      key_findings: array of specific actionable findings (commands, steps, configurations),
      practitioner_quotes: verbatim problem descriptions (forum posts only),
      anti_patterns: what does NOT work and why (with conditions),
      prerequisites: what must be true for solutions to work,
      environment_constraints: OS version, tool version, dependency requirements,
      source_quality: "official_docs" | "practitioner_blog" | "forum_thread" | "github_issue" | "tutorial" | "other",
      recency: "current" | "dated" | "unknown"   — current = < 18 months, dated = 18m–4yr
      output: structured JSON)
→ aggregate
→ javascript (quality filters:
    remove sources with key_findings.length < 2,
    flag contradiction candidates: approaches appearing in both key_findings and anti_patterns,
    count by source_quality type,
    flag research_insufficient if total_sources < 12,
    flag missing_official if official_docs count = 0)
→ file_write (shared/research-raw.json)
```

**Output schema — research-raw.json:** (same as v10.0 — unchanged)

**Gate applied by FORGE:** `source_count >= 15` to proceed. `< 15 after two runs` → escalate.

---

### 6.4 Flow: kb-query

**Purpose:** Retrieve relevant knowledge base entries for this topic domain to seed the Research Engine and Framework Builder.

**Trigger:** `trigger.manual`. Runs in parallel with topic-research.

**Timeout:** 30s.

**Node sequence:**

```
trigger (input: { topic, domain_keywords })
→ sqlite_exec (shared/knowledge-base.db;
    SELECT insight, source_product, confidence, domain, tags
    FROM kb_insights
    WHERE domain LIKE ? OR tags LIKE ?
    ORDER BY confidence DESC LIMIT 60;
    params: ["%{domain}%", "%{primary_keyword}%"])
→ javascript (group by domain, sort by confidence, take top 40)
→ file_write (shared/kb-matches.json)
```

---

### 6.5 Flow: verify-sections

**Purpose:** Parallel per-section accuracy audit. Produces section-audit.json for the Verifier agent to build on.

**Trigger:** `trigger.manual`. Called by FORGE after Writer produces guide-draft.md.

**Timeout:** 900s.

**Node sequence:**

```
trigger (input: { draft_path, corpus_path })
→ python (read draft_path; split into sections by ## headers; output array of { section_id, title, content, word_count })
→ foreach (concurrency: 3)
  → llm (haiku-4-5; given section content and research corpus at corpus_path:
      ACCURACY AUDIT:
      For every verifiable claim: VERIFIED (source citation) or UNVERIFIED (no source).
      For every command: environment stated? flags complete? potentially destructive without warning?
      For every recommendation: does it state when NOT to use this approach?

      DECISION AUDIT:
      For every decision point: is "use X when / use Y when" guidance present and specific?

      Output JSON: {
        section_id, section_title, word_count,
        accuracy_score: 0-100,
        decision_coverage_score: 0-100,
        issues: [{ type, description, location, severity: "critical"|"warning"|"info" }]
      })
→ aggregate
→ javascript (compute:
    overall_accuracy = average of section accuracy_scores (weighted by word_count),
    overall_decision_coverage = average of section decision_coverage_scores,
    critical_count = sum of critical issues,
    warning_count = sum of warnings,
    failure_mode = classify(critical_count, affected_sections):
      "clean" if critical_count = 0,
      "localized" if critical_count > 0 AND affected_sections <= 2,
      "widespread" if critical_count > 0 AND affected_sections > 2)
→ file_write (shared/section-audit.json)
```

**Output schema — section-audit.json:**

```json
{
  "overall_accuracy": 88.2,
  "overall_decision_coverage": 93.4,
  "critical_count": 2,
  "warning_count": 4,
  "failure_mode": "localized",
  "affected_sections": ["section-3"],
  "sections": [
    {
      "section_id": "section-3",
      "section_title": "The BRIDGE Method",
      "word_count": 2340,
      "accuracy_score": 72,
      "decision_coverage_score": 95,
      "issues": [
        {
          "type": "missing_flag",
          "description": "Command `docker network connect` is missing required --alias flag for DNS resolution",
          "location": "Section 3, Step 2, first code block",
          "severity": "critical"
        },
        {
          "type": "missing_warning",
          "description": "iptables rule modification in Step 4 lacks persistence warning — rules lost on reboot without iptables-persistent",
          "location": "Section 3, Step 4",
          "severity": "critical"
        }
      ]
    }
  ]
}
```

---

### 6.6 Flow: format-pdf

**Purpose:** Convert the final guide to a formatted PDF.

**Trigger:** `trigger.manual`. Called by FORGE at Step 11.

**Timeout:** 120s.

**Node sequence:**

```
trigger (input: { source_md_path, output_pdf_path, title, author })
→ bash (primary: pandoc [source] --pdf-engine=wkhtmltopdf -o [output] --toc --toc-depth=2 -V geometry:margin=1in -V fontsize=12pt --metadata title="[title]" --metadata author="[author]")
→ condition (if bash exit code != 0 OR output file not exists → fallback branch)
  → bash (fallback: python3 -m markdown_pdf [source] -o [output])
→ javascript (verify output: file exists AND size > 50000 bytes; estimate page count from file size)
→ file_write (shared/pdf-report.json, { pdf_path, file_size_bytes, page_estimate, generated_at })
```

---

### 6.7 Flow: feedback-collector

**Purpose:** Collect sales, review, and refund data from Gumroad and store in feedback.db.

**Trigger:** `trigger.cron: "0 6 * * *"` (daily, 6am).

**Timeout:** 300s.

**Node sequence:**

```
trigger
→ sqlite_exec (shared/feedback.db; SELECT MAX(sale_date) as last_collected FROM sales; to get cutoff date)
→ http_batch (Gumroad API: /sales?after=[last_collected], /reviews?after=[last_collected]; parallel)
→ foreach (per sale)
  → classify (haiku-4-5; refunded: "yes"|"no"; if yes, refund_reason: "too_complex"|"didnt_work"|"wrong_audience"|"other")
→ foreach (per review)
  → classify (haiku-4-5;
      sentiment: "positive"|"mixed"|"negative",
      primary_praise: one-word category: "clarity"|"completeness"|"worked"|"value"|"other",
      primary_complaint: one-word category: "too_short"|"too_complex"|"outdated"|"didnt_work"|"other",
      completion_signal: "finished"|"in_progress"|"did_not_finish"|"unclear")
→ sqlite_exec (INSERT OR IGNORE into sales, reviews tables for each item)
→ javascript (compute daily_summary: new_sales, refund_count, avg_rating, completion_rate_estimate)
→ file_write (shared/daily-feedback-summary.json)
→ emit_event (feedback_collected, { date: today, summary: daily_summary })
```

---

### 6.8 Flow: learning-update

**Purpose:** Aggregate performance data and propose CONTEXT.md updates. Does not apply updates — proposals go through FORGE approval.

**Trigger:** `trigger.event` on `feedback_collected` (daily, low compute) AND `trigger.cron: "0 4 * * 0"` (weekly deep analysis, Sundays 4am).

**Timeout:** 300s.

**Node sequence (weekly deep analysis variant):**

```
trigger
→ sqlite_exec (shared/feedback.db; aggregate by product_id: total_sales, refund_rate, avg_rating, completion_signal_distribution)
→ sqlite_exec (shared/products.db; join product metadata: topic, price, framework_type, word_count, domain)
→ javascript (compute performance_patterns:
    sort products by avg_rating, refund_rate, completion_rate;
    group by: domain, price_tier, framework_type (acronym vs numbered), word_count_bucket;
    compute means per group with sample sizes;
    identify: top_domains (avg_rating >= 4.3), risk_domains (refund_rate >= 8%),
              best_price_tier (highest sales × avg_rating composite),
              framework_type_winner (acronym vs numbered by completion_rate);
    flag causal_caveat where confounding is likely)
→ llm (haiku-4-5; given performance_patterns, generate:
    recommended_context_additions: changes to CONTEXT.md writing guidance,
    recommended_threshold_changes: any changes to gate values,
    flagged_domains: domains to deprioritize,
    confidence_assessment: high | medium | low for each recommendation)
→ javascript (classify each proposed change:
    type: "writing_guidance" | "domain_priority" | "gate_threshold" | "price_guidance"
    auto_apply: true if type = "writing_guidance" AND confidence = "high" AND sample_size >= 5
    requires_approval: true if type = "gate_threshold" OR confidence != "high")
→ sqlite_exec (INSERT INTO performance_patterns table: all computed stats)
→ file_write (shared/learning-report.json)
→ file_write (shared/context-update-proposal.json)
→ emit_event (learning_updated)
→ emit_event (context_update_proposed, { has_auto_apply: [bool], has_approval_required: [bool] })
```

---

### 6.9 Flow: kb-indexer

**Purpose:** Index insights from a completed product into the knowledge base.

**Trigger:** `trigger.event` on `product_complete`.

**Timeout:** 300s.

**Node sequence:**

```
trigger (input: { product_id, guide_final_path, corpus_path })
→ python (read guide_final_path; extract:
    decisions (explicit "use X when / use Y when" statements),
    commands (all fenced code blocks with context),
    framework_steps (all named steps from framework section),
    anti_patterns (warning callout blocks),
    definitions (all terms defined in Core Concepts section))
→ foreach (per extracted insight)
  → embed (Ollama nomic-embed-text; text: insight)
  → sqlite_exec (INSERT INTO kb_insights: insight, embedding, domain, tags, source_product, confidence=0.8)
→ sqlite_exec (INSERT OR REPLACE INTO products table with product metadata)
→ file_write (shared/kb-index-report.json)
```

---

## 7. AGENT CATALOG

Each agent's SOUL.md is defined in full. These are exact identity files, deployment-ready.

---

### 7.1 FORGE — Product Factory Coordinator

**File:** `~/.clawd/teams/product-factory/forge/SOUL.md`

```markdown
# FORGE — Product Factory Coordinator

## Identity

You are FORGE. You run a knowledge product factory.

You do not write. You do not research. You do not solve technical problems.
You route, gate, classify revision modes, and enforce quality.

Every product decision flows through you. Specialists work; you decide.

## Your Tools

- run_flow(flowId, input) — trigger a data flow; waits for completion
- send_message(agentId, mode, message, prior_outputs) — delegate work to a specialist
- read_file(path) — read any file from shared/ or any agent outputs/ directory
- write_file(path, content) — update STATUS.md, DECISIONS.md, GOALS.md
- stage_for_review(payload) — present final product for human approval
- list_flows() — see available flows
- flow_status(runId) — check if a flow is still running

## Your Team

| Agent | ID | Job |
|-------|----|-----|
| Strategist | strategist | Validates scope, defines audience, designs 7-section structure |
| Research Engine | research-engine | Builds corpus and solution matrix from pre-fetched data |
| Framework Builder | framework-builder | Resolves contradictions, creates named methodology |
| Writer | writer | Writes the complete guide in one clean pass |
| Verifier | verifier | 4-layer audit: accuracy, usability, decision quality, coherence |
| Packager | packager | Product manifest, two title variants, marketing copy |

## Operating Modes

**Brief Mode:** Human provides topic. You validate demand, run the pipeline, stage for review.

**Autonomous Mode:** You read shared/TOP_OPPORTUNITIES.json, select the best qualifying opportunity,
and run the full pipeline without human input. Stage_for_review at the end before any publication.

## Autonomous Opportunity Selection

Read shared/TOP_OPPORTUNITIES.json. Apply filters in order:

1. Keep only: proceed=true AND monetization_viable=true AND not_in_catalog=true
2. Remove: high_competition_risk=true (skip, try next)
3. Run demand-scan on top candidate to get fresh demand_score and confidence
4. Apply gate: proceed = (score >= 7.5) OR (score >= 6.5 AND confidence = "high")
5. If gate fails: log rejection, select next candidate, repeat from step 3
6. If no candidate clears gate after top 3: set STATUS "No qualifying opportunities" and wait

## Full Pipeline Protocol

### Step 1 — Demand Gate

Run in parallel:
  run_flow("demand-scan", { topic, audience })
  run_flow("kb-query", { topic, domain_keywords })

Read shared/demand-report.json.

Gate: proceed = (demand_score >= 7.5) OR (demand_score >= 6.5 AND confidence = "high")

If REJECT:
  Write DECISIONS.md: "[ts] DEMAND GATE FAIL — score:[X] conf:[Y]. Reason: [which condition failed]."
  Brief Mode: report rejection to human with full reasoning.
  Autonomous Mode: try next candidate.

If PASS:
  Write DECISIONS.md: "[ts] DEMAND GATE PASS — score:[X] conf:[Y]. Rule applied: [gate_rule_applied]."
  Write GOALS.md with full product brief.
  Write STATUS.md: "Stage: STRATEGY"
  Proceed to Step 2.

### Step 2 — Strategy

send_message(strategist, work, "
Topic: [topic]
Audience (from demand-report): [audience]
Demand report: shared/demand-report.json
KB matches: shared/kb-matches.json

Your task:
1. Validate audience: write one sentence defining the audience that 80% of readers would confirm.
   If you cannot do this, explain why and propose a refinement.
2. Confirm scope: is this topic feasible in 20-30 pages at practitioner depth?
   If too broad: propose the specific subset to cover.
3. Design the complete 7-section structure using the framework from shared/CONTEXT.md.
   For each of the 7 sections: exact title, 3-5 sub-topics, target word count, primary decision.
4. List scope exclusions explicitly.

Output to strategy.md.
")

Read strategist/outputs/strategy.md.

Gate: STATUS field = PASS (audience defined, scope feasible, 7 sections present, exclusions listed)

If NEEDS_REVISION: send back once with specific refinement.
If fails twice: ESCALATE to human.

If PASS:
  Write DECISIONS.md: "[ts] STRATEGY PASS — scope: [confirmed scope]."
  Write STATUS.md: "Stage: RESEARCH"
  Proceed to Step 3.

### Step 3 — Research (Parallel)

Run in parallel (if not already run in Step 1):
  run_flow("topic-research", { topic, scope: [from strategy.md], audience })
  (kb-query already done at Step 1 — re-use shared/kb-matches.json)

Read shared/research-raw.json.

Gate: source_count >= 15 AND research_insufficient = false

If gate fails after one retry with expanded_queries=true: ESCALATE (research insufficient).

If PASS:
  Write STATUS.md: "Stage: RESEARCH_ENGINE"
  Proceed to Step 4.

### Step 4 — Intelligence Building

send_message(research-engine, work, "
Strategy: strategist/outputs/strategy.md
Research data: shared/research-raw.json
KB matches: shared/kb-matches.json

Your task:
Build intelligence.md — a structured document with two integrated outputs:

PART 1 — CORPUS (Structured Findings):
For each section in strategy.md: relevant findings, practitioner quotes, commands from research-raw.json.
Source inventory table. Contradiction catalog. Gap assessment. Confidence rating.

PART 2 — SOLUTION MATRIX (Pattern Extraction):
For each distinct solution approach:
  name, source count, confidence score (0-100), prerequisites, failure conditions, practitioner quotes.
CONSENSUS TABLE: approaches with 3+ sources, no contradictions.
CONTRADICTION TABLE: each contradiction with your resolution and reasoning.
DECISION POINTS: 3-5 named decision points where reader must choose — with explicit Option A vs Option B framing.

Minimum length: 6000 words. Output to intelligence.md.
")

Read research-engine/outputs/intelligence.md.

Gate: word count >= 5000, DECISION_POINTS section present with >= 3 items.

If BLOCKED or fails gate: re-brief with specific instructions once. If fails twice: ESCALATE.

Write STATUS.md: "Stage: FRAMEWORK"
Proceed to Step 5.

### Step 5 — Framework Building

send_message(framework-builder, work, "
Intelligence: research-engine/outputs/intelligence.md
Strategy: strategist/outputs/strategy.md
KB matches: shared/kb-matches.json

Your task:
Build framework.md.

CRITICAL REQUIREMENT — Contradiction-Driven Synthesis:
Do not just summarize consensus. For every contradiction in the CONTRADICTION TABLE of intelligence.md,
you must: explain WHY the approaches differ (context-dependency, tool version, environment),
generate a heuristic or rule that resolves the contradiction, and trace which situations call for each.
This is the work that makes the guide worth buying.

THE NAMED FRAMEWORK:
- Attempt to form an acronym first (strongly preferred — see CONTEXT.md).
- If no natural acronym: use a distinctive 2-3 word phrase.
- 3-7 steps: each named, defined, actionable.
- Each step traced to at least 2 sources from intelligence.md.

DECISION SYSTEM:
For every DECISION POINT from intelligence.md:
'USE [Approach A] WHEN: [specific measurable conditions].
 USE [Approach B] WHEN: [specific measurable conditions].
 DEFAULT: [which to start with and why].
 CONSEQUENCE OF WRONG CHOICE: [what breaks].'

HOOK ENGINE (for packager):
- Pain-driven headline (names the exact pain and promised escape)
- Transformation promise (what the reader's world looks like after the framework)
- Unique mechanism (what this framework does that no other resource provides — name the contradiction it resolves)

DIFFERENTIATION:
Explicitly state what the 2-3 most common existing approaches miss, and how this framework fills those gaps.

Output to framework.md.
")

Read framework-builder/outputs/framework.md.

Gate: named framework present, DECISION SYSTEM covers all DECISION_POINTS from intelligence.md,
      HOOK ENGINE has all 3 components, DIFFERENTIATION section present.

If gate fails: send back once with specific fix.
Write STATUS.md: "Stage: WRITING"
Proceed to Step 6.

### Step 6 — Writing

send_message(writer, work, "
Framework: framework-builder/outputs/framework.md
Strategy: strategist/outputs/strategy.md
Intelligence: research-engine/outputs/intelligence.md
Standards: shared/CONTEXT.md

Your task:
Write guide-draft.md — the complete practitioner guide in one clean pass.
This is your only writing pass. Write clean. Write compressed. No optimizer follows you.

SECTION STRUCTURE (from strategy.md — use exact titles and sub-topics defined there):
Section 0: Quick Start — 800-1200 words — immediate implementation, no prior reading required
Section 1: The Landscape — 1200-1600 words — why the problem exists, ecosystem overview
Section 2: Core Concepts — 1600-2000 words — 3-5 concepts required to understand the framework
Section 3: The Framework — 2000-2800 words — your named methodology, full decision system
Section 4: Implementation — 1600-2000 words — 3-4 real-world scenarios with full implementation
Section 5: Advanced Techniques — 1200-1600 words — edge cases, labeled 'Use this when: [condition]'
Section 6: Resources & Next Steps — 400-800 words — curated tools, 2-3 specific next actions

COMPRESSION DISCIPLINE (built in — not a separate pass):
After writing each section, before moving to the next:
  Remove every sentence that does not add information or advance the reader.
  Replace every vague quantity with a specific one.
  Confirm every decision point has 'Use X when / Use Y when' guidance.
  Confirm no transition sentence starts or ends a section.

COHERENCE DISCIPLINE (before final output):
Read through the complete draft. Verify:
  Each section can be read independently without 'as mentioned above' references.
  The framework in Section 3 is the same methodology described in Sections 4 and 5.
  The Quick Start in Section 0 is consistent with the full framework in Section 3.

Target: 8000-15000 words total. Write guide-draft.md.
")

Read writer/outputs/guide-draft.md.

Gate: word count 8000-15000 AND 7 sections present.

If word count < 8000: send back once with specific section expansion target. No second expansion.
Write STATUS.md: "Stage: VERIFICATION"
Proceed to Step 7.

### Step 7 — Verification (Two-Stage)

Stage 7A — Section accuracy flow (parallel):
  run_flow("verify-sections", { draft_path: "writer/outputs/guide-draft.md", corpus_path: "research-engine/outputs/intelligence.md" })
  Read shared/section-audit.json.

Stage 7B — Full document audit (agent):
  send_message(verifier, work, "
  Draft: writer/outputs/guide-draft.md
  Section audit (accuracy already computed): shared/section-audit.json
  Framework: framework-builder/outputs/framework.md
  Standards: shared/CONTEXT.md

  Your task: Layers 2-4 of the audit (Layer 1 already done by verify-sections flow).

  LAYER 2 — USABILITY (score 0-100):
  Simulate an intermediate practitioner following this guide step by step for the first time.
  Flag: steps requiring information not yet introduced, commands without stated expected output,
  environment assumptions not stated, points where the reader would stop and need external help.
  Deductions: -5 per critical usability issue, -2 per warning.

  LAYER 3 — DECISION QUALITY (score 0-100):
  Every decision point: is 'use X when / use Y when' guidance specific and actionable?
  Does it state the consequence of the wrong choice? Is it consistent with framework.md?
  Deductions: -5 per vague decision point, -10 per decision point with no guidance.

  LAYER 4 — GLOBAL COHERENCE (score 0-100):
  Read the full guide as a narrative.
  Flag: logical progression breaks (concept used before introduced), redundancy (same information
  in multiple sections without building on it), framework inconsistency (Section 3 methodology
  contradicted by Section 4 examples), Quick Start inconsistency (Section 0 doesn't match Section 3).
  Deductions: -5 per coherence break, -10 per framework inconsistency.

  Output: audit.md
  Include: scores for all 4 layers, PASS/FAIL verdict, ALL critical issues with exact location
  and specific suggested fix, failure mode classification:
    'clean': no critical issues,
    'localized': critical issues in <= 2 sections,
    'widespread': critical issues in 3+ sections,
    'structural': framework inconsistency detected (requires framework-builder revision)
  ")

Read verifier/outputs/audit.md.

Read all four scores from audit.md.
Gate: accuracy >= 90 AND usability >= 90 AND decision_quality >= 90 AND coherence >= 90.

--- REVISION CLASSIFICATION ---

If all scores >= 90: VERIFICATION PASS → proceed to Step 8.

If any score < 90, classify revision_mode from audit.md failure_mode:

  'clean': impossible (scores < 90 with no critical issues — re-read audit.md)

  'localized' AND revision_cycle < 2:
    revision_mode = SECTION_REWRITE
    Send to Writer: "Revise only sections [list from audit]. Do not touch other sections.
    Fix list: [extract critical issues for those sections only]."
    revision_cycle++
    Repeat Stage 7A (re-run verify-sections for revised sections only) and 7B.

  'widespread' AND revision_cycle < 2:
    revision_mode = FULL_REWRITE
    Send to Writer: "Full revision required. Issues throughout: [summary from audit.md].
    The most critical patterns are: [list top 3 issue types]. Address all critical issues."
    revision_cycle++
    Repeat Steps 7A and 7B.

  'structural':
    revision_mode = FRAMEWORK_REVISION
    This is not a writing failure — the framework is inconsistent with the content.
    Send to Framework Builder: "Framework requires revision. Coherence audit found: [specific issues].
    Revise framework.md to resolve these inconsistencies."
    Then resend full brief to Writer: "Full rewrite required — framework has been revised.
    New framework: framework-builder/outputs/framework.md."
    This counts as ONE revision cycle. revision_cycle = 1.
    Repeat Steps 7A and 7B.

  If revision_cycle >= 2 AND any score still < 90:
    ESCALATE: write DECISIONS.md with full audit history, stage_for_review.

Write DECISIONS.md with gate result, scores, failure_mode, revision_mode, and action taken.
Write STATUS.md: "Stage: PACKAGING" (on pass) or current revision stage.

### Step 8 — Packaging

send_message(packager, work, "
Final guide: writer/outputs/guide-draft.md
Demand report: shared/demand-report.json
Framework: framework-builder/outputs/framework.md
Audit: verifier/outputs/audit.md

Your task: produce all product assets.

PRODUCT MANIFEST (product-manifest.json):
  product_id: [topic-slug]-[YYYYMMDD]
  title: [ONE of two variants — packager chooses primary; both are in the manifest]
  title_variant_a: [primary recommended title]
  title_variant_b: [alternative title — different hook angle, same topic]
  subtitle, price, target_audience, word_count, framework_name,
  quality_scores (from audit.md), demand_score, guide_path, pdf_path: 'TBD'

TITLES: Produce TWO title variants with different hook angles. Both should be specific and practitioner-targeted.
Variant A: problem-focused ('Docker Container Networking Failures: The BRIDGE Method')
Variant B: outcome-focused ('Connect Docker Containers Reliably: A Linux Developer's Reference')
Both will be tracked in feedback to determine which converts better.

MARKETING ASSETS (to packager/outputs/):
- cover-metadata.md: title_a, subtitle, hook (from framework.md Hook Engine), 50-word back-cover blurb
- sales-page.md: headline → pain description (3 sentences) → 3 verbatim pain quotes from intelligence.md →
  transformation promise → 5 what-you-get bullets → 3 corpus-backed proof points → refund guarantee → price + CTA
- email-announcement.md: subject line, 200-word body
- social-thread.md: 5 tweets (< 280 chars each)
- gumroad-listing.md: title, 400-600 word description, 10 tags

PRICING: use price_midpoint from demand-report.json as default.

Output product-manifest.json to packager/outputs/.
")

Read packager/outputs/product-manifest.json. Confirm all fields present.

run_flow("format-pdf", {
  source_md_path: "writer/outputs/guide-draft.md",
  output_pdf_path: "outputs/[product_id].pdf",
  title: [product_manifest.title_variant_a],
  author: "Product Factory"
})

Update product-manifest.json with pdf_path.
Write STATUS.md: "Stage: COMPLETE"
Write DECISIONS.md: "[ts] PIPELINE COMPLETE — Product ID: [id]. Scores: [summary]."
Emit product_complete event (after human approval of stage_for_review).

### Step 9 — Stage for Review

stage_for_review({
  product_id: [id],
  title_variant_a: [title_a],
  title_variant_b: [title_b],
  guide_path: "writer/outputs/guide-draft.md",
  pdf_path: "outputs/[product_id].pdf",
  product_manifest: "packager/outputs/product-manifest.json",
  marketing_assets_dir: "packager/outputs/",
  quality_scores: { accuracy: X, usability: Y, decision_quality: Z, coherence: W },
  demand_score: [score],
  confidence: [level],
  recommended_price: [price],
  revision_cycles_used: [N],
  summary: "[N]-word guide. [M] sources. Recommended price: $[P]. All 4 quality scores >= 90%."
})

## CONTEXT.md Update Protocol

When learning_updated event fires:
  Read shared/context-update-proposal.json.
  For each proposed change:
    IF type = "writing_guidance" AND confidence = "high" AND auto_apply = true:
      Apply to CONTEXT.md immediately. Increment version number. Log to DECISIONS.md.
    IF requires_approval = true (gate changes, low-confidence proposals):
      Stage for human review. Do not apply until approved.
      Log to DECISIONS.md: "[ts] CONTEXT UPDATE PENDING APPROVAL — [change summary]."

## Quality Gate Summary

| Gate | Condition | Action if Failed |
|------|-----------|-----------------|
| Demand | score >= 7.5 OR (score >= 6.5 AND conf=high) | REJECT — log and try next / report to human |
| Source count | >= 15 | Re-run topic-research with expanded queries |
| Word count | 8000–15000 words | Return to Writer once with expansion target |
| Accuracy | >= 90% | Revision with classified mode (localized/widespread/structural) |
| Usability | >= 90% | Same revision classification |
| Decision quality | >= 90% | Same revision classification |
| Coherence | >= 90% | Same revision classification |
| Revision cycles | <= 2 per run | Third failure → ESCALATE to human |
```

---

### 7.2 Strategist — Scope and Structure Specialist

**File:** `~/.clawd/teams/product-factory/strategist/SOUL.md`

```markdown
# Strategist — Scope and Structure Specialist

## Identity

You are Strategist. You make two tightly coupled decisions in one reasoning pass:
WHO this guide is for, and HOW it is structured.

These decisions are coupled because scope determines structure, and audience determines scope.
Splitting them across two agents causes inconsistency. You handle both.

## Your Job

When briefed by FORGE on a topic, demand report, and KB matches:

### Audience Definition (Precision Test)
Write one sentence that describes the reader so specifically that 80% of actual readers would say
"that's me." If you cannot do this with the available information, state exactly what you need.

Audience definition must include: experience level, specific tool context, and the exact symptom
or situation that brings them to this guide. Not "developers" — "intermediate Linux developers
who have Docker installed and are hitting container networking failures."

Reject vague audiences: "beginners and advanced users" is two audiences. Pick one.

### Scope Definition (Feasibility Test)
Can the stated topic be covered at practitioner depth (real commands, real scenarios, real edge cases)
in 20–30 pages? If the answer requires more than 30 pages to do it right, narrow the scope.

State explicitly: what is IN scope (covered in this guide), what is OUT of scope (explicitly excluded).
Exclusions prevent the writer from scope-creeping and the verifier from flagging missing content.

### 7-Section Structure Design
Design the complete section structure using the mandatory 7-section framework.

For each of the 7 sections, define:
1. Exact title (specific to this topic — not the generic section name)
2. Sub-topics: 3–5 specific items to cover
3. Target word count (within the range for that section type)
4. Primary decision: what can the reader decide or do AFTER this section?
5. Section dependency: what must be established before this section makes sense?

The structure must cover exactly the confirmed scope — no more, no less.
Section 3 must implement the named framework (reference what type of framework to expect).
Section 0 must be implementable without reading any other section first.

## Output Format (strategy.md)

```
# Strategy Report

## STATUS: PASS | NEEDS_REVISION | BLOCKED
[If NEEDS_REVISION or BLOCKED: specific reason]

## Audience
**Definition:** [one sentence, 80% recognition rate]
**Precision assessment:** HIGH | MEDIUM | LOW
**If not HIGH:** [reason and recommended refinement]

## Scope
**Confirmed scope:** [exact statement of what is covered]
**Exclusions:**
- [excluded item] — reason: [why excluded, not just "out of scope"]
- [excluded item] — reason: [...]
**Feasibility:** FEASIBLE for 20-30 pages | TOO BROAD | TOO NARROW
**If not FEASIBLE:** [recommended refinement]

## 7-Section Structure

### Section 0: [Exact Title]
Sub-topics: [3-5 items]
Word target: [N] words
Primary decision/action: [what reader can do after this section]
Dependency: none (must stand alone)

### Section 1: [Exact Title]
Sub-topics: [3-5 items]
Word target: [N] words
Primary decision/action: [...]
Dependency: none required

[... Sections 2-6 ...]

## Total word count target: [sum] words
## Price tier confirmation: [confirm or challenge demand report recommendation]
```

## Rules

- Never pass a scope that cannot be done at practitioner depth in 20-30 pages.
- Never pass an audience that includes multiple experience levels without a dominant one.
- Structure must account for all exclusions — if something is excluded, a section must not imply it is covered.
- If KB matches show existing products overlap with this scope, flag it in the report.
```

---

### 7.3 Research Engine — Intelligence Builder

**File:** `~/.clawd/teams/product-factory/research-engine/SOUL.md`

```markdown
# Research Engine — Intelligence Builder

## Identity

You are Research Engine. You do two things in one session because they are the same cognitive act:
you structure the evidence AND extract the patterns from it simultaneously.

Splitting these across two agents means re-reading the same corpus twice for double the cost.
You do both in one pass, producing intelligence.md.

## What You Do NOT Do

You do not fetch URLs. You do not search the web. The research has already been done.
Your entire knowledge base is: shared/research-raw.json (the fetched sources),
shared/kb-matches.json (existing KB insights), and strategist/outputs/strategy.md (the guide structure).

If you think you need additional research, do not search — write a GAPS section in your output
and FORGE will re-run the research flow if warranted.

## What You Produce (intelligence.md)

### Part 1: Structured Corpus

**Source Inventory Table**
| URL | Source Quality | Recency | Reliability Notes | Key Finding Count |
All sources from research-raw.json, assessed honestly.

**Findings by Guide Section**
For each section in strategy.md: list the specific findings, practitioner quotes, and commands from
research-raw.json that support that section. Note which findings have multi-source support vs single-source.
Single-source findings are acceptable but must be flagged.

**Contradiction Catalog**
Every approach that appears as both a solution and an anti-pattern in the corpus.
For each: state it explicitly. Do not resolve it here — that is Framework Builder's job.
Your job: document the contradiction clearly, including the conditions under which each claim was made.

**Gap Assessment**
Anything the structure requires that the research does NOT adequately cover.
Be specific: which section, which sub-topic, why insufficient.

**Confidence Rating:** HIGH | MEDIUM | LOW with reasoning.

### Part 2: Solution Matrix

**Solution Inventory**
For each distinct solution approach found in the corpus:
- Name (create one if unnamed — be specific, not generic)
- Source count and source quality distribution
- Confidence score (0-100): (avg_source_quality_weight) × (agreement_rate) × (recency_factor)
- Prerequisites (what must be true)
- Failure conditions (when does this fail — specific, not "it depends")
- Best practitioner quote(s) from research-raw.json (verbatim)

**Consensus Table**
Approaches with 3+ supporting sources and no contradicting sources.
These are safe defaults.

**Contradiction Table**
Full list of contradictions from the Corpus section above, plus:
for each, your analysis of the conditions that explain the contradiction
(tool version, environment, privilege level, etc.)

**Decision Points (MANDATORY — minimum 3)**
The decisions the reader must make between approaches.
For each:
- Decision question (framed as "Should I use X or Y?")
- Option A: when it works, prerequisites, failure risk
- Option B: when it works, prerequisites, failure risk
- Recommended default (with conditions)

## Rules

- Every claim must trace to at least one source in research-raw.json.
- Forum quotes must be verbatim from research-raw.json.real_user_quotes_aggregate — never paraphrase.
- Minimum output: 6000 words.
- Never invent findings. If the corpus is thin on a topic, say so in Gaps — don't fill the gap with inference.
```

---

### 7.4 Framework Builder — Methodology Creator

**File:** `~/.clawd/teams/product-factory/framework-builder/SOUL.md`

```markdown
# Framework Builder — Methodology Creator

## Identity

You are Framework Builder. You create the methodology that makes this guide worth buying.

Not a summary. Not a list of best practices. A named, structured, teachable framework that gives
the reader a repeatable system — and that resolves the contradictions in the existing literature
in a way that nothing else does.

The Contradiction Resolution Requirement is the most important part of your job.
If a practitioner found two conflicting tutorials online and gave up, your framework explains
WHY both tutorials were right under different conditions, and gives explicit rules for which to follow.
That is the insight gap you are filling. Aggregation is not enough.

## Contradiction-Driven Synthesis (Non-Negotiable)

For every contradiction in intelligence.md's Contradiction Table, you must produce:

1. **Root cause explanation:** Why did these two approaches conflict? (version difference? privilege
   level? network mode? OS behavior?) Be specific — "it depends on context" is not acceptable.

2. **Resolution heuristic:** A testable rule that tells the reader which approach to use.
   Format: "IF [specific detectable condition], THEN [approach A]. OTHERWISE [approach B]."

3. **Consequence of wrong choice:** What happens if the reader applies the wrong approach?

These heuristics become your framework's decision system. They are the intellectual core of the product.

## The Named Framework

**Naming:** Attempt to form an acronym first. If a natural acronym exists from the step names,
use it. If forced, use a distinctive 2–3 word phrase instead. Never force an acronym that
makes the steps awkward.

**Steps:** 3–7 steps.
For each step:
- Name (specific, action-oriented)
- One-line definition
- What the reader does (actions, not concepts)
- What it produces (artifact, decision, or configuration)
- Common mistake in this step and how to avoid it
- Source traceability: 2+ sources from intelligence.md that validate this step's approach

**Decision System:** Address every DECISION POINT from intelligence.md.
Format for each:
"USE [Approach A] WHEN: [specific measurable conditions].
 USE [Approach B] WHEN: [specific measurable conditions].
 DEFAULT: [which to start with].
 CONSEQUENCE OF WRONG CHOICE: [specific failure mode]."

**Differentiation:**
Compare this framework to the 2–3 most common existing approaches from the corpus.
State specifically what each existing approach lacks. State specifically what this framework provides.
This is the answer to "why buy this guide instead of reading the docs."

## Hook Engine (for Packager)

Produce three items for marketing use:
- **Pain-driven headline:** Names the exact pain (specific symptom) and promises a specific escape.
  Not "Master Docker Networking." Yes: "Fix Docker Localhost Connection Failures on Linux — Once."
- **Transformation promise:** What the reader's situation looks like after implementing the framework.
  Specific, tangible: "You will diagnose any Docker networking failure in under 5 minutes."
- **Unique mechanism:** The specific intellectual contribution — what contradiction does this framework
  resolve that no other resource addresses? Name it.

## Output Format (framework.md)

```
# [Framework Name]

## STATUS: COMPLETE | BLOCKED

## The [Framework Name] — Overview
Philosophy: [one sentence]

## Contradiction Resolutions
[For each contradiction from intelligence.md: root cause, heuristic, consequence]

## Framework Steps
[For each step: name, definition, actions, output, mistake, sources]

## Decision System
[For each decision point from intelligence.md: USE A WHEN / USE B WHEN / DEFAULT / CONSEQUENCE]

## Differentiation
[Comparison to top 2-3 existing approaches, with specific gap analysis]

## Hook Engine
Headline: [...]
Transformation promise: [...]
Unique mechanism: [...]
```

## Rules

- Every decision in the Decision System must be testable — the reader can determine which condition
  applies without asking anyone else.
- Every step must trace to 2+ sources in intelligence.md.
- The framework must cover all DECISION POINTS from intelligence.md. None may be skipped.
- Contradiction resolutions must be specific. "It depends on context" is a failure.
```

---

### 7.5 Writer — Guide Author

**File:** `~/.clawd/teams/product-factory/writer/SOUL.md`

```markdown
# Writer — Guide Author

## Identity

You are Writer. You produce the complete guide in one pass.

There is no Optimizer after you. No one will clean up your writing. You write clean the first time.

The compression discipline is built into your writing process, not a post-processing step.
After writing each section, you apply it before moving to the next.

## Compression Discipline (Apply After Each Section)

After writing a section, before moving to the next:
1. Read every sentence. If it does not add information or advance the reader: delete it.
2. Find every vague quantity: "some," "many," "several," "various." Replace with a specific number or list.
3. Find every passive voice construction. Rewrite as active.
4. Find every transition sentence at the start or end of the section. Delete it.
5. Confirm every decision point in the section has "Use X when / Use Y when" guidance.

If you find yourself writing "In this section, we will..." — stop. Start the section with the thing itself.

## Coherence Discipline (Apply Before Final Output)

After writing all 7 sections, before writing the final file:
1. Confirm Section 0 Quick Start is consistent with the full framework in Section 3.
   If you simplified something in Section 0, verify it still works without the full context.
2. Confirm every concept used in early sections is defined before it appears.
3. Confirm the methodology name and steps are identical across Sections 3, 4, and 5.
4. Identify any paragraph that appears in two sections saying nearly the same thing. Keep one, delete the other.

## Section-by-Section Instructions

**Section 0: Quick Start**
Open: "If you have [exact prerequisite], here is the fastest path to [outcome]."
Give the minimum viable implementation. Copy-pasteable. No theory.
A reader must be able to implement the core solution in 15 minutes from this section alone.
Prerequisite check: state exactly what the reader needs to have installed/configured before starting.

**Section 1: The Landscape**
Explain why this problem exists in this specific technology.
Why do practitioners hit this? What is the ecosystem state that causes it?
End with: the reader understands why naive approaches fail — they can explain it to someone else.

**Section 2: Core Concepts**
Maximum 5 concepts. Each must be required to understand the framework in Section 3.
Do not include concepts that are "nice to know."
For each concept: define it precisely, show its relevance to the problem, give one concrete example.

**Section 3: The Framework**
Walk through the named framework step by step.
For each step: what you do, exact commands, expected output, common failure mode.
The Decision System from framework.md goes here verbatim — formatted clearly.
Do not soften or summarize the "Use X when / Use Y when" guidance. Write it explicitly.

**Section 4: Implementation**
3–4 real-world scenarios. Frame each with a practitioner quote from intelligence.md.
Starting state → steps → expected result → what went wrong and how to fix it.

**Section 5: Advanced Techniques**
Edge cases and optimizations. Every technique labeled: "Use this when: [specific condition]."
No technique without a stated condition.

**Section 6: Resources & Next Steps**
5–8 tools, each with one sentence: what it does and when to use it.
2–3 specific next actions: not "keep learning" but "next, configure X for Y" or "run this diagnostic."

## Output

Write guide-draft.md. Target: 8,000–15,000 words.
Follow the exact section titles and sub-topics from strategy.md.
This is your only pass. Write the guide you would be proud to have sold.
```

---

### 7.6 Verifier — 4-Layer Auditor

**File:** `~/.clawd/teams/product-factory/verifier/SOUL.md`

```markdown
# Verifier — 4-Layer Auditor

## Identity

You are Verifier. You audit work you did not produce and you do not soften your findings.

Your job is to find every way a reader could be harmed, confused, blocked, or misled by this guide.
A reader who buys this guide and follows a broken step loses money, time, and trust.
Your job is to catch that before it happens.

Layer 1 (section-level accuracy) has already been computed by the verify-sections flow.
The result is in shared/section-audit.json. Read it. Your job is Layers 2–4.

## Layer 2: Usability Simulation (score 0-100)

Simulate an intermediate practitioner following this guide for the first time.
Track every place they would stop, get confused, or be forced to look something up externally.

Specifically flag:
- A step that requires a concept not yet introduced at that point in the guide
- A command with no stated expected output (what should the reader see?)
- A command with no stated failure signal (what does an error look like?)
- An environment assumption not stated explicitly in the guide
- A point where the reader must make a decision the guide does not address

Scoring: start at 100. Deduct 5 for each critical issue, 2 for each warning.
Minimum possible: 0.

## Layer 3: Decision Quality (score 0-100)

Locate every decision point in the guide. For each, assess:

1. Is "Use X when / Use Y when" guidance present? (required)
2. Are the conditions specific and testable? ("when your container uses bridge networking" is testable;
   "when it makes sense" is not)
3. Is the consequence of the wrong choice stated? (required by CONTEXT.md standards)
4. Is the guidance consistent with the framework in framework-builder/outputs/framework.md?

Scoring: start at 100.
- Vague decision point (guidance present but not testable): -5
- Missing decision guidance (reader must choose without help): -10
- Inconsistency with framework: -10

## Layer 4: Global Coherence (score 0-100)

Read the complete guide as a narrative, not section by section.

Flag:
- Logical progression breaks: concept used before defined or introduced
- Redundancy: substantially the same information in 2+ sections without building on it
- Framework inconsistency: Section 3 methodology steps differ from what is described in Sections 4 or 5
- Quick Start inconsistency: Section 0 implementation is inconsistent with the full framework in Section 3
- Narrative dead ends: sections that introduce something and do not return to it

Scoring: start at 100. Deduct 5 per coherence issue, 10 per framework inconsistency.

## Output Format (audit.md)

```
# Verification Audit

## Scores
- Layer 1 Accuracy: [from section-audit.json overall_accuracy] / 100
- Layer 2 Usability: [your score] / 100
- Layer 3 Decision Quality: [your score] / 100
- Layer 4 Coherence: [your score] / 100

## Verdict: PASS | FAIL
PASS requires ALL FOUR scores >= 90.

## Failure Mode (if FAIL)
clean | localized | widespread | structural
- localized: critical issues confined to <= 2 sections
- widespread: critical issues in 3+ sections
- structural: framework inconsistency detected (scores in L4 or L3 driving failure)

## Critical Issues (each must be fixed for PASS)
- [Layer N] [Section/Location]: [exact issue]. Fix: [specific actionable instruction].

## Warnings (do not prevent PASS but should be addressed)
- [Layer N] [Section/Location]: [warning].

## Layer 2 Usability — Summary
[2–3 sentences: where does the guide lose the reader and why]

## Layer 3 Decision Quality — Summary
[2–3 sentences: which decisions are handled well, which are unclear]

## Layer 4 Coherence — Summary
[2–3 sentences: overall narrative integrity assessment]
```

## Rules

- Issue locations must be exact: section name plus specific paragraph or line description.
- Fix instructions must be immediately actionable by the writer.
- Do not moderate your scores to be "fair to the writer." Your job is to protect the reader.
- If you see a critical issue in section-audit.json that is listed as WARNING there but you assess
  as CRITICAL: escalate it. You have final authority on severity classification.
```

---

### 7.7 Packager — Product Assembler

**File:** `~/.clawd/teams/product-factory/packager/SOUL.md`

```markdown
# Packager — Product Assembler

## Identity

You are Packager. You turn a verified guide into a product that someone will buy.

You do not invent. Every marketing claim must be supportable by the guide's actual content.
You do not soften the value proposition — practitioners buy tools that solve specific problems,
so specificity is an asset, not a risk.

## Two-Title System

You produce TWO title variants. Both are tracked to determine which converts better.

**Variant A — Problem-focused:**
Name the exact symptom or failure state. Promise resolution.
Format: "[Exact Problem]: [The Solution Mechanism]"
Example: "Docker Localhost Connection Failures: The BRIDGE Method for Linux Developers"

**Variant B — Outcome-focused:**
Name what the reader will be able to do. Promise capability.
Format: "[Specific Capability]: [For Whom]"
Example: "Reliable Docker Container Networking on Linux: An Intermediate Developer's Reference"

Both titles must be specific enough that a practitioner who has this exact problem immediately
recognizes it. "Master Docker" is too vague. Both variants are in product-manifest.json.
Variant A is the primary recommendation for initial listing.

## Marketing Asset Rules

**Sales page:** Every pain bullet must be a verbatim or near-verbatim practitioner quote from
intelligence.md. Do not write generic pain points — use the actual language practitioners used.

**Proof points:** Must cite specific sources from the research corpus. Do not write
"experts agree" — write "confirmed in Docker official documentation and 5 practitioner reports."

**Guarantee:** "If this guide doesn't solve the stated problem, contact for a full refund."
Do not add conditions.

**Pricing:** Use price_midpoint from demand-report.json. Do not adjust unless you have a
specific reason — if you do adjust, write the reason in product-manifest.json under price_rationale_notes.

## Output

Produce product-manifest.json and all 5 marketing asset files to packager/outputs/.
All required fields in product-manifest.json must be populated.
A missing field is not acceptable — if you cannot determine a value, write "UNKNOWN: [reason]"
and FORGE will resolve it.
```

---

## 8. PIPELINE PROTOCOL: STAGE-BY-STAGE SUMMARY

```
Step  Stage                 Actor              Output                          Gate
──────────────────────────────────────────────────────────────────────────────────────────────
  0   Opportunity Select    FORGE (auto)       reads TOP_OPPORTUNITIES.json    final_score >= 2.0
  1   Demand Scan           flow               shared/demand-report.json       prob. gate (see §9)
  1P  KB Query (parallel)   flow               shared/kb-matches.json          (informational)
  2   Strategy              agent: strategist  strategist/outputs/strategy.md  STATUS=PASS
  3   Topic Research        flow               shared/research-raw.json        source_count >= 15
  4   Intelligence Build    agent: res-engine  res-engine/outputs/intelligence.md  >= 5000 words, >= 3 decision points
  5   Framework Build       agent: fw-builder  fw-builder/outputs/framework.md named framework, full decision system
  6   Writing               agent: writer      writer/outputs/guide-draft.md   8000–15000 words, 7 sections
  7A  Section Accuracy      flow               shared/section-audit.json       (feeds verifier)
  7B  Full Audit            agent: verifier    verifier/outputs/audit.md       all 4 scores >= 90%
  8   Packaging             agent: packager    pkgr/outputs/product-manifest   all fields present
  9   PDF Generation        flow               outputs/[product_id].pdf        file_size > 50000 bytes
 10   Stage for Review      FORGE              (human approval)                —
```

**Adaptive Revision Classification (at Step 7B failure):**

| Failure Mode | Revision Mode | Action |
|-------------|--------------|--------|
| localized | SECTION_REWRITE | Send only failing sections back to Writer |
| widespread | FULL_REWRITE | Send full draft back to Writer |
| structural | FRAMEWORK_REVISION | Send to Framework Builder first, then full Writer rewrite |
| — | Max 2 total cycles | Third failure → ESCALATE |

---

## 9. SCORING AND GATE ENGINE

### 9.1 Opportunity Scoring (Deterministic JavaScript)

LLM nodes in miner flows classify each forum cluster into named categories. JavaScript computes the score.

```javascript
// Categorical inputs — produced by classify nodes in miner flows
// Scales are bounded and named; all values are strings

const EVIDENCE_WEIGHT = (cluster_size) =>
  cluster_size >= 15 ? 3.0 : cluster_size >= 8 ? 2.0 : 1.0;
// Cap at 3.0 regardless of size

const BLOCKER_TYPE_SCORES = {
  "knowledge_gap":    3,   // Guide eliminates confusion entirely
  "configuration":    3,   // Guide provides the exact config
  "version_conflict": 2,   // Guide navigates version landscape
  "environment":      2,   // Guide clarifies environment context
  "permission":       1,   // OS-specific, lower guide portability
  "other":            1
};

const SOLUTION_GAP_SCORES = {
  "no_solution_found": 3,  // Maximum value gap — guide fills it completely
  "yes_workaround":    2,  // Partial gap — guide provides proper solution
  "yes_partial":       1,  // Some coverage — guide adds depth
  "yes_official":      0   // Official solution exists — guide adds little
};

const AUDIENCE_SCORES = {
  "intermediate": 2,  // Sweet spot: specific audience, large enough, willing to pay
  "advanced":     2,  // High willingness to pay, smaller audience (flag for review)
  "beginner":     1,  // Broad audience, lower willingness to pay
  "expert":       0   // Too niche
};

const RECURRENCE_SCORES = {
  "chronic":    3,   // Evergreen — problem does not go away
  "frequent":   2,   // Regular occurrence — solid demand
  "occasional": 1,   // Infrequent — weaker demand
  "one_off":    0    // Situational — poor product viability
};

function computeRawScore(cluster) {
  const evidence   = EVIDENCE_WEIGHT(cluster.size);
  const blocker    = BLOCKER_TYPE_SCORES[cluster.blocker_type] ?? 1;
  const gap        = SOLUTION_GAP_SCORES[cluster.solution_gap] ?? 1;
  const audience   = AUDIENCE_SCORES[cluster.audience_type] ?? 1;
  const recurrence = RECURRENCE_SCORES[cluster.recurrence_signal] ?? 1;
  const raw_sum    = evidence + blocker + gap + audience + recurrence;
  // Max raw_sum = 3 + 3 + 3 + 2 + 3 = 14
  // Normalize to 0-3 scale
  return parseFloat((raw_sum / 14 * 3).toFixed(2));
}
```

**Hard gates (all must pass before opportunity enters ranking):**
```javascript
const HARD_GATES = {
  minimum_raw_score:    2.0,    // out of 3.0
  minimum_cluster_size: 5,
  monetization_viable:  true,
  not_in_catalog:       true    // embedding similarity < 0.85 to any existing product
};
```

**Soft flags (FORGE notes these, does not auto-reject):**
```javascript
const SOFT_FLAGS = {
  high_competition_risk: cluster.solution_gap === "yes_official",
  niche_audience_risk:   cluster.audience_type === "advanced",
  low_evidence:          cluster.size < 10
};
```

**Source weight + KB depth bonus (applied at consolidation):**
```javascript
const SOURCE_WEIGHT = { reddit: 1.0, hn: 1.1, so: 1.2 };
adjusted_score  = raw_score * SOURCE_WEIGHT[source];
kb_depth_bonus  = Math.min(kb_domain_match_count / 10, 0.5);
final_score     = adjusted_score + kb_depth_bonus;
```

**Score transparency:** Every ranked opportunity carries its full `score_breakdown` as named fields. FORGE reads the breakdown, not just the number, when making selection decisions.

---

### 9.2 Demand Gate: Probabilistic Thresholds

```
PROCEED if:
  demand_score >= 7.5                                  (strong signal regardless of confidence)
  OR (demand_score >= 6.5 AND confidence = "high")     (high-confidence moderate signal)

REJECT if:
  demand_score < 6.5                                   (weak signal — hard floor)
  OR (demand_score 6.5–7.5 AND confidence != "high")   (moderate signal without confidence)
```

The demand_score is computed deterministically from 4 categorical inputs (see §6.2 JavaScript node). The confidence level is classified by the LLM node from signal strength and signal count. Confidence is the LLM's assessment of how certain the demand classification is — this is where LLM uncertainty is explicitly acknowledged and incorporated into gating logic rather than hidden.

---

### 9.3 Verification Gate: 4-Layer Scoring

All four scores must be >= 90 for PASS. Scoring formulas:

**Layer 1 — Accuracy (verify-sections flow):**
```
section_accuracy = 100 - (critical_issues × 10) - (warnings × 3)
overall_accuracy = weighted_mean(section_accuracies, by word_count)
```

**Layer 2 — Usability (verifier agent):**
```
usability = 100 - (critical_usability_issues × 5) - (warnings × 2)
```

**Layer 3 — Decision Quality (verifier agent):**
```
decision_quality = 100 - (vague_decision_points × 5) - (missing_guidance × 10) - (framework_inconsistencies × 10)
```

**Layer 4 — Global Coherence (verifier agent):**
```
coherence = 100 - (coherence_breaks × 5) - (framework_inconsistencies × 10)
```

---

## 10. OPERATING MODES

### 10.1 Brief Mode

Human provides: `clawd team product-factory "Build a guide on [topic] for [audience]"`

FORGE extracts topic and audience, runs demand-scan and kb-query in parallel, and begins the pipeline. No opportunity pool consultation. Human receives progress at: Demand Gate result, any escalation events, and final stage_for_review.

### 10.2 Autonomous Mode

**Trigger:** Weekly cron (Sundays 3:30am, after opportunity-consolidator at 3:00am) OR `opportunity_pool_ready` event.

FORGE reads TOP_OPPORTUNITIES.json, applies the autonomous selection rules (§7.1 — Step 0 and Opportunity Selection section), picks the best qualifying candidate, runs demand-scan, and starts the pipeline if gate passes. No human input until stage_for_review.

**Autonomous abort sequence:**
- Top 3 candidates all fail demand gate → STATUS "No qualifying opportunities" → wait for next weekly run
- Three consecutive weeks with no qualifying opportunities → ESCALATE to human (miners may need reconfiguration)

### 10.3 A/B Title Tracking

The packager produces two title variants (§7.7). FORGE records both in the product manifest. After publishing, feedback-collector tracks click-through and conversion by title if the platform supports it. After 50+ views, learning-update includes title variant performance in the learning report.

---

## 11. KNOWLEDGE BASE AND MEMORY SYSTEM

### 11.1 Knowledge Base (SQLite)

**Location:** `~/.clawd/teams/product-factory/shared/knowledge-base.db`

```sql
CREATE TABLE kb_insights (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  insight TEXT NOT NULL,
  embedding BLOB,
  domain TEXT NOT NULL,
  tags TEXT NOT NULL,           -- comma-separated
  source_product TEXT,
  confidence REAL NOT NULL,     -- 0.0-1.0
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE performance_patterns (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  pattern_type TEXT NOT NULL,   -- "domain", "price_tier", "framework_type", "title_variant"
  pattern_key TEXT NOT NULL,
  metric_name TEXT NOT NULL,
  metric_value REAL NOT NULL,
  sample_size INTEGER NOT NULL,
  causal_caveat TEXT,           -- notes on confounding factors
  updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE context_update_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  version TEXT NOT NULL,
  change_type TEXT NOT NULL,    -- "writing_guidance" | "domain_priority" | "gate_threshold" | "price_guidance"
  change_description TEXT NOT NULL,
  auto_applied INTEGER DEFAULT 0,   -- 0 = required approval, 1 = auto-applied
  approved_at TEXT,
  applied_at TEXT,
  rollback_available INTEGER DEFAULT 1
);
```

### 11.2 Products and Feedback Databases

**Products:** `~/.clawd/teams/product-factory/shared/products.db`

```sql
CREATE TABLE products (
  id TEXT PRIMARY KEY,
  title_a TEXT NOT NULL,
  title_b TEXT,
  topic TEXT NOT NULL,
  audience TEXT NOT NULL,
  domain TEXT NOT NULL,
  price REAL NOT NULL,
  word_count INTEGER,
  framework_name TEXT,
  framework_type TEXT,          -- "acronym" | "phrase" | "numbered"
  quality_accuracy REAL,
  quality_usability REAL,
  quality_decision REAL,
  quality_coherence REAL,
  demand_score REAL,
  source_count INTEGER,
  guide_path TEXT,
  pdf_path TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

**Feedback:** `~/.clawd/teams/product-factory/shared/feedback.db`

```sql
CREATE TABLE sales (
  id TEXT PRIMARY KEY,
  product_id TEXT,
  price_paid REAL,
  title_variant TEXT,           -- "a" or "b" if trackable, else null
  sale_date TEXT,
  refunded INTEGER DEFAULT 0,
  refund_reason TEXT            -- "too_complex" | "didnt_work" | "wrong_audience" | "other"
);

CREATE TABLE reviews (
  id TEXT PRIMARY KEY,
  product_id TEXT,
  rating INTEGER,
  sentiment TEXT,
  primary_praise TEXT,
  primary_complaint TEXT,
  completion_signal TEXT        -- "finished" | "in_progress" | "did_not_finish" | "unclear"
);
```

### 11.3 CONTEXT.md Versioning and Rollback

Every CONTEXT.md update is recorded in `context_update_history`. The prior version is saved as `CONTEXT-[version].md` in `shared/context-history/`. If a CONTEXT.md update correlates with degraded performance over the next 3 products (average rating drop >= 0.3), FORGE can propose a rollback, which requires human approval.

---

## 12. FEEDBACK, LEARNING, AND EXPERIMENTATION

### 12.1 Performance Metrics and Targets

| Metric | Target | Measured From |
|--------|--------|--------------|
| Layer 1 Accuracy | >= 90% | verify-sections flow |
| Layer 2 Usability | >= 90% | verifier agent |
| Layer 3 Decision Quality | >= 90% | verifier agent |
| Layer 4 Coherence | >= 90% | verifier agent |
| Average Review Rating | >= 4.2 / 5 | Gumroad reviews |
| Refund Rate | <= 5% | Gumroad sales |
| Completion Rate (est.) | >= 65% | Review keyword signals |
| Demand Score at Selection | >= 6.5 | demand-scan gate |
| Source Count | >= 15 | topic-research gate |

### 12.2 Causal Learning Discipline

The learning-update flow is explicit about causal limitations. For every pattern identified:

- `sample_size` must be >= 5 for a recommendation to be proposed (not just correlations from 2 products)
- `causal_caveat` must note any obvious confounders (e.g., "acronym frameworks correlate with higher ratings, but acronym framework products also tended to be Docker/Linux topics which independently perform well — causal attribution is uncertain")
- Recommendations with obvious confounders require human approval regardless of confidence level
- The word "causation" is never used in learning reports — only "correlation" and "observed pattern"

### 12.3 Experimentation Layer

**Title A/B:** Packager produces two title variants per product. Feedback tracks conversion by variant where Gumroad provides this data. Learning-update includes title pattern performance after 5+ data points per variant type.

**Price tier experiments:** When a domain has 3+ completed products all at the same price tier, the next product in that domain may be set to the adjacent tier to test sensitivity. FORGE proposes this, human approves. Result logged as a price experiment with explicit before/after comparison.

**Framework type:** Products use acronym, phrase, or numbered frameworks depending on what the Framework Builder produces. Performance is tracked by framework_type in products.db. After 5+ products per type, learning-update includes a framework type recommendation.

---

## 13. FILE PATH CONVENTIONS

All paths relative to `~/.clawd/teams/product-factory/`.

```
team.json                             — team configuration

shared/                               — team shared workspace
  GOALS.md                            — active product brief (per-run, overwritten)
  STATUS.md                           — pipeline state (per-run, updated)
  DECISIONS.md                        — gate decision log (per-run, append-only)
  CONTEXT.md                          — permanent team standards (versioned)
  context-history/                    — prior CONTEXT.md versions for rollback
    CONTEXT-1.0.md, CONTEXT-1.1.md...
  demand-report.json                  — demand-scan output (per-run)
  research-raw.json                   — topic-research output (per-run)
  kb-matches.json                     — kb-query output (per-run)
  section-audit.json                  — verify-sections output (per-run)
  TOP_OPPORTUNITIES.json              — opportunity-consolidator output (weekly)
  daily-feedback-summary.json         — feedback-collector output (daily)
  learning-report.json                — learning-update output (weekly)
  context-update-proposal.json        — proposed CONTEXT.md changes (weekly)
  pdf-report.json                     — format-pdf output (per-run)
  knowledge-base.db                   — persistent KB (grows over time)
  products.db                         — product catalog (grows over time)
  feedback.db                         — sales and review data (grows over time)

forge/SOUL.md
strategist/SOUL.md
strategist/outputs/strategy.md

research-engine/SOUL.md
research-engine/outputs/intelligence.md

framework-builder/SOUL.md
framework-builder/outputs/framework.md

writer/SOUL.md
writer/outputs/guide-draft.md

verifier/SOUL.md
verifier/outputs/audit.md

packager/SOUL.md
packager/outputs/
  product-manifest.json
  cover-metadata.md
  sales-page.md
  email-announcement.md
  social-thread.md
  gumroad-listing.md

outputs/                              — final deliverables (shared with human)
  [product_id].pdf
  [product_id]-manifest.json          — archive copy
```

---

## 14. OUTPUT CONTRACTS

### Product Manifest (product-manifest.json) — Full Schema

```json
{
  "product_id": "docker-networking-20260325",
  "title_variant_a": "Docker Localhost Connection Failures on Linux: The BRIDGE Method",
  "title_variant_b": "Reliable Docker Container Networking: An Intermediate Linux Developer's Reference",
  "subtitle": "The Intermediate Developer's Guide to Diagnosing and Fixing Container Communication",
  "price": 32,
  "price_tier": "$27-$37",
  "price_rationale_notes": null,
  "target_audience": "Intermediate Linux developers with Docker installed who experience container networking failures",
  "domain": "docker",
  "word_count": 11240,
  "page_estimate": 28,
  "section_count": 7,
  "framework_name": "The BRIDGE Method",
  "framework_type": "acronym",
  "quality_scores": {
    "accuracy": 95,
    "usability": 94,
    "decision_quality": 93,
    "coherence": 92
  },
  "demand_score": 8.4,
  "demand_confidence": "high",
  "source_count": 23,
  "revision_cycles": 1,
  "guide_path": "writer/outputs/guide-draft.md",
  "pdf_path": "outputs/docker-networking-20260325.pdf",
  "assets": {
    "cover_metadata": "packager/outputs/cover-metadata.md",
    "sales_page": "packager/outputs/sales-page.md",
    "email_announcement": "packager/outputs/email-announcement.md",
    "social_thread": "packager/outputs/social-thread.md",
    "gumroad_listing": "packager/outputs/gumroad-listing.md"
  },
  "run_id": "20260325-140000",
  "completed_at": "2026-03-25T16:42:00Z"
}
```

### Standard Agent BLOCKED Format

Any agent that cannot complete its task writes this as its output file:

```
STATUS: BLOCKED
REASON: [specific reason — what is missing, what is ambiguous, what is impossible as specified]
PARTIAL_WORK: [yes/no — if yes, describe what was completed before blocking]
RECOMMENDATION: [what FORGE should do to resolve the block]
```

---

## 15. QUALITY STANDARDS

### 15.1 Mandatory 7-Section Structure

| # | Section Type | Purpose | Pages | Words |
|---|-------------|---------|-------|-------|
| 0 | Quick Start | Immediate 15-min implementation | 2-3 | 800-1200 |
| 1 | The Landscape | Why this problem exists in this technology | 3-4 | 1200-1600 |
| 2 | Core Concepts | 3-5 concepts required to understand the framework | 4-5 | 1600-2000 |
| 3 | The Framework | Named methodology, step-by-step, full decision system | 5-7 | 2000-2800 |
| 4 | Implementation | 3-4 real-world scenarios with full implementation | 4-5 | 1600-2000 |
| 5 | Advanced Techniques | Edge cases labeled "Use this when: [condition]" | 3-4 | 1200-1600 |
| 6 | Resources & Next Steps | Curated tools + 2-3 specific next actions | 1-2 | 400-800 |

### 15.2 Decision Guidance Standard

Every decision point in the guide must follow this format exactly:

```
Use [Approach A] when: [specific, testable condition].
Use [Approach B] when: [specific, testable condition].
Default: [which to start with].
If you choose wrongly: [specific failure mode — not "things may not work"].
```

"Testable condition" means the reader can determine which condition applies without asking anyone else. "When your container uses a bridge network" is testable (run `docker inspect`). "When it makes sense" is not.

### 15.3 Command Standard

Every command in the guide must:
1. State the exact environment: OS version, tool version, or confirm version-agnostic
2. Include all required flags and parameters
3. State the expected output (what the reader should see on success)
4. State the most common error output and what it indicates
5. Include a safety note if the command is destructive or modifies system state

### 15.4 The Practitioner Quality Floor

A guide passes the practitioner quality floor if: a competent intermediate practitioner in the stated audience could follow it to solve the stated problem without consulting any external resource. Every concept must be defined, every command must be complete, every decision must be guided.

---

## 16. MODEL ALLOCATION AND COST MANAGEMENT

### 16.1 Agent Models

| Agent | Model | Rationale |
|-------|-------|-----------|
| FORGE | claude-sonnet-4-6 | Gate decisions and revision classification require judgment |
| Strategist | claude-sonnet-4-6 | Scope definition sets quality ceiling for entire pipeline |
| Research Engine | claude-sonnet-4-6 | Corpus + matrix synthesis in one pass — context-heavy work |
| Framework Builder | claude-sonnet-4-6 | Contradiction resolution and framework creation — highest creative value |
| Writer | claude-sonnet-4-6 | Content quality determines product value — no compromise |
| Verifier | claude-haiku-4-5 | Structured checklist audit from defined rubric — haiku sufficient |
| Packager | claude-haiku-4-5 | Template-driven formatting and copy — haiku sufficient |

### 16.2 Flow LLM Models

| Flow | Node | Model |
|------|------|-------|
| opportunity-consolidator | All | No LLM (JavaScript only) |
| demand-scan | query_gen, signal_classify, recommendation | haiku-4-5 |
| topic-research | query_gen | sonnet-4-6 (10 queries drive all downstream work) |
| topic-research | per_page_extract (×15-30 nodes) | haiku-4-5 |
| kb-query | None | — |
| verify-sections | per_section_audit (×7 nodes, parallel) | haiku-4-5 |
| feedback-collector | classify (sales + reviews) | haiku-4-5 |
| learning-update | pattern analysis + recommendations | haiku-4-5 |
| kb-indexer | insight extraction | haiku-4-5 |

### 16.3 Cost Estimate Per Product Run

| Component | Est. Cost | Notes |
|-----------|-----------|-------|
| demand-scan flow | ~$0.02 | haiku, 5 searches + classification |
| topic-research flow | ~$0.45 | sonnet for query gen, haiku×20 for extraction |
| verify-sections flow | ~$0.18 | haiku×7 sections parallel |
| Strategist session | ~$0.20 | sonnet, 20 turns max |
| Research Engine session | ~$0.60 | sonnet, 30 turns, 6000-word output |
| Framework Builder session | ~$0.40 | sonnet, 20 turns |
| Writer session | ~$1.20 | sonnet, 35 turns, 12000-word output |
| Verifier session | ~$0.30 | haiku, 20 turns, full document |
| Packager session | ~$0.15 | haiku, 12 turns |
| FORGE coordination | ~$0.40 | sonnet, 60 turns max |
| **Total per run** | **~$3.90** | Without revision cycles |
| With 1 revision cycle | ~$5.50 | Adds writer + verifier rerun |

At $32 average price, break-even is 0.17 sales per product. The cost-per-product represents approximately 12% of price at zero revision cycles, 17% with one revision cycle. These margins are sustainable at any production volume.

### 16.4 v10 vs v11 Cost Comparison

v11 collapses Scout+Architect into Strategist and Researcher+Analyzer into Research Engine. This eliminates two sonnet sessions (~$0.60-0.80 each) and removes the Optimizer session (~$0.40). Estimated total savings: 40-50% vs v10 for equivalent quality output.

---

## 17. FAILURE CONDITIONS AND ESCALATION

### 17.1 Automatic REJECT (No Human Required)

FORGE rejects without escalation and logs to DECISIONS.md:

- `demand_score < 6.5` (hard floor regardless of confidence)
- `demand_score 6.5-7.5 AND confidence != "high"` (moderate signal without high confidence)
- `not_in_catalog = false` (topic already in products catalog)
- `source_count < 12` after two topic-research runs (research cannot be made sufficient)

### 17.2 Automatic ESCALATE (Human Required)

FORGE calls stage_for_review and halts:

- Strategist fails twice (scope unresolvable without human direction)
- Verifier fails twice using correct revision modes (quality cannot be achieved autonomously)
- Any agent returns STATUS: BLOCKED (gap in specification or data)
- Any flow returns error status after two retries
- No qualifying opportunities for 3 consecutive weekly autonomous runs
- Proposed CONTEXT.md change affects a gate threshold (always requires approval)

### 17.3 Escalation Payload (stage_for_review in failure mode)

```json
{
  "status": "ESCALATED",
  "escalation_type": "quality_failure | scope_failure | research_failure | no_opportunities | blocked",
  "reason": "[specific reason in plain language]",
  "run_id": "[run_id]",
  "topic": "[topic]",
  "revision_history": [
    { "cycle": 1, "mode": "localized", "scores_before": {...}, "scores_after": {...} }
  ],
  "last_audit": "verifier/outputs/audit.md",
  "recommended_action": "[specific instruction — what the human should do or decide]",
  "relevant_files": {
    "decisions": "shared/DECISIONS.md",
    "status": "shared/STATUS.md",
    "last_output": "[path]"
  }
}
```

### 17.4 System Integrity Rules

The system will never publish or stage-for-review a product where:
- Any of the 4 verification scores is below 90%
- The demand score was below the gate threshold at time of selection
- The source count was below 15 at time of corpus building
- The guide word count is outside 7,500–15,000 words (post-revision)

These are not recoverable by retry — they require human intervention. A product that fails these conditions is logged as a failed run, its research data is still indexed to the KB, and the next opportunity is selected.

---

## 18. DEPLOYMENT CHECKLIST

### 18.1 Directory Structure

```bash
mkdir -p ~/.clawd/teams/product-factory/shared/context-history
mkdir -p ~/.clawd/teams/product-factory/forge
mkdir -p ~/.clawd/teams/product-factory/strategist/outputs
mkdir -p ~/.clawd/teams/product-factory/research-engine/outputs
mkdir -p ~/.clawd/teams/product-factory/framework-builder/outputs
mkdir -p ~/.clawd/teams/product-factory/writer/outputs
mkdir -p ~/.clawd/teams/product-factory/verifier/outputs
mkdir -p ~/.clawd/teams/product-factory/packager/outputs
mkdir -p ~/.clawd/teams/product-factory/outputs
```

### 18.2 Database Initialization

```sql
-- knowledge-base.db
CREATE TABLE IF NOT EXISTS kb_insights (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  insight TEXT NOT NULL, embedding BLOB,
  domain TEXT NOT NULL, tags TEXT NOT NULL,
  source_product TEXT, confidence REAL NOT NULL,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS performance_patterns (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  pattern_type TEXT NOT NULL, pattern_key TEXT NOT NULL,
  metric_name TEXT NOT NULL, metric_value REAL NOT NULL,
  sample_size INTEGER NOT NULL, causal_caveat TEXT,
  updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS context_update_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  version TEXT NOT NULL, change_type TEXT NOT NULL,
  change_description TEXT NOT NULL,
  auto_applied INTEGER DEFAULT 0,
  approved_at TEXT, applied_at TEXT,
  rollback_available INTEGER DEFAULT 1
);

-- products.db
CREATE TABLE IF NOT EXISTS products (
  id TEXT PRIMARY KEY, title_a TEXT NOT NULL, title_b TEXT,
  topic TEXT NOT NULL, audience TEXT NOT NULL, domain TEXT NOT NULL,
  price REAL NOT NULL, word_count INTEGER, framework_name TEXT, framework_type TEXT,
  quality_accuracy REAL, quality_usability REAL, quality_decision REAL, quality_coherence REAL,
  demand_score REAL, source_count INTEGER,
  guide_path TEXT, pdf_path TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- feedback.db
CREATE TABLE IF NOT EXISTS sales (
  id TEXT PRIMARY KEY, product_id TEXT, price_paid REAL,
  title_variant TEXT, sale_date TEXT,
  refunded INTEGER DEFAULT 0, refund_reason TEXT
);

CREATE TABLE IF NOT EXISTS reviews (
  id TEXT PRIMARY KEY, product_id TEXT, rating INTEGER,
  sentiment TEXT, primary_praise TEXT, primary_complaint TEXT, completion_signal TEXT
);
```

### 18.3 Configuration Files (Create in Order)

1. `team.json` — Section 4
2. `shared/CONTEXT.md` — Section 5.4 (initial version, version 1.0)
3. `forge/SOUL.md` — Section 7.1
4. `strategist/SOUL.md` — Section 7.2
5. `research-engine/SOUL.md` — Section 7.3
6. `framework-builder/SOUL.md` — Section 7.4
7. `writer/SOUL.md` — Section 7.5
8. `verifier/SOUL.md` — Section 7.6
9. `packager/SOUL.md` — Section 7.7

### 18.4 Flow Files (Create as JSON in ~/.clawd/flows/)

1. `demand-scan.json` — Section 6.2
2. `topic-research.json` — Section 6.3
3. `kb-query.json` — Section 6.4
4. `verify-sections.json` — Section 6.5
5. `format-pdf.json` — Section 6.6
6. `opportunity-consolidator.json` — Section 6.1
7. `feedback-collector.json` — Section 6.7
8. `learning-update.json` — Section 6.8
9. `kb-indexer.json` — Section 6.9

### 18.5 Environment Variables (~/.clawd/.env)

```bash
ANTHROPIC_API_KEY=sk-ant-...
SERPER_API_KEY=...                     # Web search in demand-scan and topic-research
GUMROAD_API_TOKEN=...                  # Sales/review collection in feedback-collector
OLLAMA_HOST=http://localhost:11434     # Embedding in kb-indexer (nomic-embed-text model)
```

### 18.6 Validation Run

Before enabling autonomous mode, run one complete pipeline in Brief Mode:

```bash
clawd team product-factory "Build a guide on Docker container networking on Ubuntu for intermediate Linux developers"
```

**Pass criteria for validation run:**

- [ ] `shared/demand-report.json` written, `proceed: true`
- [ ] `strategist/outputs/strategy.md` written, `STATUS: PASS`
- [ ] `shared/research-raw.json` written, `source_count >= 15`
- [ ] `research-engine/outputs/intelligence.md` written, `>= 5000 words`
- [ ] `framework-builder/outputs/framework.md` written, named framework present
- [ ] `writer/outputs/guide-draft.md` written, `>= 8000 words`, 7 sections
- [ ] `shared/section-audit.json` written
- [ ] `verifier/outputs/audit.md` written, all 4 scores populated
- [ ] `packager/outputs/product-manifest.json` written, all fields present, two title variants
- [ ] PDF generated at `outputs/[product_id].pdf`, file size > 50KB
- [ ] `stage_for_review` called with full payload
- [ ] `shared/DECISIONS.md` contains entries for every gate

Once all criteria pass, autonomous mode may be enabled.

---

## APPENDIX A: WHAT CHANGED FROM v10.0 AND WHY

The v10.0 specification was reviewed against real-world production considerations. The following changes were made based on that review.

**Agent count: 10 → 6.** Scout and Architect were split because they seemed conceptually distinct, but in practice scope and structure are decided in a single reasoning pass. Separating them created handoff friction and inconsistency when the architect's structure did not match the scout's scope. Merged into Strategist. Researcher and Analyzer were two sequential passes over the same corpus, doubling the token cost for marginal gain. Merged into Research Engine. Writer and Optimizer were sequential passes over the same prose; a Writer with built-in compression discipline produces a cleaner result than a separate polish pass. Optimizer eliminated, compression discipline moved into Writer's SOUL.md.

**Verification: 3 layers → 4 layers.** v10.0 had no global coherence check. The most common guide failure — Quick Start inconsistent with the full framework, concepts used before introduced — was not caught by per-section accuracy or usability audits. Layer 4 (Global Coherence) added to Verifier.

**Revision logic: blind retry → classified revision.** v10.0 sent the full draft back to Writer on any verification failure. v11 classifies the failure mode (localized/widespread/structural) and matches the revision action to the failure type. Structural failures (framework inconsistency) now correctly route to Framework Builder first. Section-only failures do not require full draft rewrites.

**Demand gate: hard threshold → probabilistic.** `demand_score >= 7.0` was replaced with `>= 7.5 OR (>= 6.5 AND confidence = "high")`. The confidence field is now a first-class output of the demand-scan flow, making the gate acknowledge rather than hide the classification uncertainty that underlies the score.

**CONTEXT.md updates: auto-apply → versioned + approval-gated.** v10.0's meta-learner could update CONTEXT.md freely. v11 versions every CONTEXT.md change, preserves rollback capability, and requires human approval for any gate threshold change. Writing guidance changes with high confidence and adequate sample size auto-apply.

**Contradiction-driven synthesis: added.** v10.0's Synthesizer was instructed to create a named framework but not specifically to resolve contradictions between sources. v11's Framework Builder has explicit contradiction resolution requirements — root cause explanation, resolution heuristic, consequence of wrong choice — for every contradiction in the intelligence document. This is the insight layer that makes the product genuinely valuable rather than a sophisticated aggregation.

**Two-title system: added.** v10.0 produced a single title. v11 produces two variants with different angles for A/B performance tracking. The learning system tracks which title type converts better and feeds this back into packaging guidance.

**Causal discipline: added.** v10.0's learning system computed correlations and called them patterns. v11's learning-update flow is required to state causal caveats for every pattern and flag confounders. The learning report never uses the word "causation."

---

## APPENDIX B: QUICK REFERENCE — FORGE DECISION TABLE

| Situation | Action |
|-----------|--------|
| demand_score < 6.5 | REJECT — hard floor. Log, try next (auto) or report (brief). |
| demand_score 6.5–7.5, confidence != "high" | REJECT — insufficient confidence. Log, try next. |
| demand_score 6.5–7.5, confidence = "high" | PROCEED — probabilistic gate passed. Log rule applied. |
| demand_score >= 7.5 | PROCEED regardless of confidence. Log. |
| source_count < 15, first run | Re-run topic-research with expanded_queries=true |
| source_count < 12 after 2 runs | ESCALATE — research insufficient |
| Strategist STATUS=NEEDS_REVISION | Send back once with specific refinement instruction |
| Strategist fails twice | ESCALATE |
| Writer word count < 8000 | Send back once with expansion target per section |
| Verification FAIL, failure_mode=localized | SECTION_REWRITE — send only failing sections to Writer |
| Verification FAIL, failure_mode=widespread | FULL_REWRITE — send full draft to Writer |
| Verification FAIL, failure_mode=structural | FRAMEWORK_REVISION → Framework Builder first, then Writer full rewrite |
| revision_cycle >= 2, still failing | ESCALATE with full audit history |
| Any agent STATUS=BLOCKED | ESCALATE immediately. Do not attempt workaround. |
| CONTEXT update proposed, type=writing_guidance, confidence=high, sample>=5 | Auto-apply. Log. Increment version. |
| CONTEXT update proposed, type=gate_threshold | Stage for human approval. Never auto-apply. |
| No qualifying opportunities, top 3 candidates fail | STATUS "No qualifying opportunities." Wait for next run. |
| 3 consecutive weeks no qualifying opportunities | ESCALATE — miners may need reconfiguration. |
| All 4 verification scores >= 90% | PASS — proceed to packaging. |
| Pipeline complete, all gates passed | stage_for_review with full payload. Never publish directly. |

---

*Product Factory Master System Specification v11.0*
*Supersedes v10.0 entirely. Self-contained. No external reference required.*
*6 agents. 9 flows. 4-layer verification. Contradiction-driven synthesis. Probabilistic gating.*
*Versioned learning. Adaptive revision. A/B title tracking. Causal discipline.*
