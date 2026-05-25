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

Optimize this existing article for both Google rankings and AI citations. Follow this workflow:

1. Read the existing article and detect its format
2. Run the quality checklist from quality-standards.md
3. Quick competitive scan: search for the article's target topic and identify top 3-5 current ranking articles
4. Compare our article against competitors:
   - Where does it match or exceed competitors?
   - Where does it fall behind?
   - What do competitors have that we're missing?
5. Research current data to replace unsourced or outdated statistics
6. Rewrite the article applying all optimization rules:
   - Answer-first formatting in every H2
   - Key Takeaways box near the top
   - Sourced statistics (minimum 3)
   - FAQ section with direct answers
   - Internal linking suggestions
   - E-E-A-T signal injection
   - Competitive differentiation (fill gaps identified in step 4)
7. Save the optimized version, preserving the original filename
8. Provide a before/after quality score comparison and competitive positioning summary

Deliver the optimized article, a changelog, and a competitive positioning summary.
