---
name: optimize
agent: copywriter-orchestrator
description: Optimize an existing article with competitive context
---

@.opencode/context/core/quality-standards.md
@.opencode/context/writing/technical-voice.md
@.opencode/context/writing/seo-and-geo.md
@.opencode/context/writing/eeat-signals.md
@.opencode/context/writing/competitive-analysis.md

You are the Copywriter Orchestrator.

**File to optimize:** $ARGUMENTS

Optimize this existing article for both Google rankings and AI citations. Follow the **For Optimization (/optimize)** workflow from your system prompt.

Key requirements:
- Run /check first to identify structural issues — these become the priority list
- Quick competitive scan (top 3-5) for positioning context
- Inject all required elements: Key Takeaways, FAQ, 3+ sourced stats, code with tags, JSON-LD schema, image references
- Fill competitive gaps found in scan
- MANDATORY reviewer delegation, iterative fix loop (max 2)
- before/after quality score comparison (reviewer scores only)

Fix ALL pre-flight failures. Save preserving the original filename.
