---
name: optimize
agent: copywriter-orchestrator
description: Optimize an existing article for SEO and AI citations
---

@.opencode/context/core/quality-standards.md
@.opencode/context/writing/technical-voice.md
@.opencode/context/writing/seo-and-geo.md
@.opencode/context/writing/eeat-signals.md

You are the Copywriter Orchestrator.

**File to optimize:** $ARGUMENTS

Optimize this existing article for both Google rankings and AI citations. Follow this workflow:

1. Read the existing article and detect its format
2. Run the quality checklist from quality-standards.md:
   - Count fabricated vs sourced statistics
   - Check answer-first formatting
   - Measure paragraph lengths
   - Verify heading hierarchy
   - Assess E-E-A-T signals
   - Check for FAQ section
3. Research current data to replace any unsourced or outdated statistics (delegate to tech-researcher if needed)
4. Rewrite the article applying all optimization rules:
   - Answer-first formatting in every H2
   - Key Takeaways box near the top
   - Sourced statistics (minimum 3)
   - FAQ section with direct answers
   - Internal linking suggestions
   - E-E-A-T signal injection
5. Save the optimized version, preserving the original filename
6. Provide a before/after quality score comparison

Deliver the optimized article and a changelog summary of all improvements made.
