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

### Phase 1: Analyze the Source
1. Read the existing article and identify:
   - Core topic and target audience
   - Valuable information worth preserving (facts, code, examples)
   - What's wrong: hallucinated stats, poor structure, wrong voice, missing elements
2. Score it against quality-standards.md to establish a baseline

### Phase 2: Competitive Context
3. Quick competitive scan: search for the topic and identify top 3-5 ranking articles
4. Note what competitors do well that the source article misses

### Phase 3: Research & Verify
5. Research current statistics and sources to replace any unsourced or outdated claims
6. Verify any technical claims from the source article — flag anything inaccurate

### Phase 4: Rewrite
7. Write a completely new article following the full workflow:
   - Answer-first formatting in every H2
   - Key Takeaways box near the top
   - Sourced statistics (minimum 3) with working links
   - Code examples with language tags and version notes
   - FAQ section (3-5 questions, direct answers)
   - E-E-A-T signals throughout
   - Proper frontmatter (title, description, date, lastUpdated, tags, author)
8. Preserve only accurate, valuable content from the original — everything else is rebuilt

### Phase 5: Quality & Delivery
9. Score the new article against quality-standards.md (target: 75+/100)
10. Save to the same filename, overwriting the original
11. Provide a before/after score comparison and a summary of what was changed

Deliver the rewritten article, a changelog of major changes, and a quality score comparison.
