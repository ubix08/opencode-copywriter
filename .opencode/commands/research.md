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

Perform deep competitive research on this topic. Delegate to the **competitive-analyst** agent for the full competitive analysis pipeline, then synthesize the findings.

Key requirements:
- Minimum 5 competitors analyzed (top 5-10), score each against the 6-dimension framework
- Identify content, depth, angle, format, freshness, and trust gaps
- Build killer article blueprint with must-haves, differentiation, information gain, structure, and sourcing plan
- Save research report to content/research/YYYY-MM-DD-topic-research.md
- Deliver summary of top 3 differentiation opportunities and recommended article angle
