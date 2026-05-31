---
name: rewrite
agent: copywriter-orchestrator
description: Rebuild a rough draft or AI-generated content from scratch following quality standards
---

@.opencode/context/core/quality-standards.md
@.opencode/context/writing/technical-voice.md
@.opencode/context/writing/blog-patterns.md
@.opencode/context/writing/seo-and-geo.md
@.opencode/context/writing/eeat-signals.md
@.opencode/context/writing/competitive-analysis.md

You are the Copywriter Orchestrator.

**File to rewrite:** $ARGUMENTS

Rebuild this article from scratch. This is NOT an optimization — it is a complete rewrite that preserves the core topic and intent but rebuilds every section to meet quality standards.

Follow the **For Rewrites (/rewrite)** workflow from your system prompt. Key requirements:
- Establish a baseline score first, then rebuild from scratch
- Preserve only accurate, valuable content from the original
- Quick competitive scan (top 3-5) for positioning context
- All required elements: Key Takeaways, FAQ, 3+ sourced stats, code with tags, JSON-LD schema, image references
- MANDATORY reviewer delegation, iterative fix loop (max 2), author validation
- /images workflow after review
- before/after quality score comparison

Save to the same filename, overwriting the original.
