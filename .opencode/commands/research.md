---
name: research
agent: copywriter-orchestrator
description: Analyze competitors and build a killer article blueprint
---

@.opencode/context/core/quality-standards.md
@.opencode/context/writing/competitive-analysis.md
@.opencode/context/writing/seo-and-geo.md

You are the Copywriter Orchestrator.

**Topic to research:** $ARGUMENTS

Perform deep competitive research on this topic. Follow this workflow:

1. Search for the topic and identify the top 5-10 ranking articles
2. Read each competitor article in full
3. Score each against the 6-dimension framework from competitive-analysis.md:
   - Content Depth, Technical Accuracy, SEO Structure, AI Citation Readiness, E-E-A-T, Uniqueness
4. Identify gaps across all competitors:
   - Content gaps (topics no one covers)
   - Depth gaps (topics covered superficially)
   - Angle gaps (perspectives no one considers)
   - Format gaps (missing examples, tables, diagrams)
   - Freshness gaps (outdated information)
   - Trust gaps (unsourced claims, no credentials)
5. Synthesize findings into a killer article blueprint:
   - Must-have elements (table stakes from top competitors)
   - Differentiation opportunities (where we can win)
   - Information gain strategy (unique value we'll add)
   - Recommended structure based on gap analysis
   - Sourcing plan (specific stats and sources to include)
6. Save the complete research report to content/research/YYYY-MM-DD-topic-research.md

Deliver a summary of the top 3 differentiation opportunities and the recommended article angle.
