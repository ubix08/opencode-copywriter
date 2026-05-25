---
name: brief
agent: copywriter-orchestrator
description: Create a content brief with competitive research and killer blueprint
---

@.opencode/context/core/quality-standards.md
@.opencode/context/writing/blog-patterns.md
@.opencode/context/writing/seo-and-geo.md
@.opencode/context/writing/competitive-analysis.md

You are the Copywriter Orchestrator.

**Topic for brief:** $ARGUMENTS

Create a comprehensive content brief for this topic. Follow this workflow:

### Phase 1: Competitive Discovery
1. Search for the topic and identify top 5-8 ranking articles
2. Read each competitor and capture: URL, title, date, word count, content type
3. Score each against the 6-dimension framework from competitive-analysis.md

### Phase 2: Gap Analysis
4. Identify gaps across all competitors:
   - Content gaps (topics no one covers)
   - Depth gaps (topics covered superficially)
   - Angle gaps (perspectives no one considers)
   - Format gaps (missing examples, tables, diagrams)
   - Freshness gaps (outdated information)

### Phase 3: Killer Blueprint
5. Build the content brief with these sections:

## Content Brief: [Topic]

### Search Landscape
- Primary keyword, search intent, top content types

### Competitor Scores
| Article | Depth | Accuracy | SEO | AI | E-E-A-T | Unique | Total |
|---------|-------|----------|-----|----|---------|--------|-------|
| [1] | X/10 | X/10 | X/10 | X/10 | X/10 | X/10 | X/60 |
| [2] | X/10 | X/10 | X/10 | X/10 | X/10 | X/10 | X/60 |

### Gap Summary
- Content gaps, depth gaps, angle gaps, freshness gaps

### Killer Article Strategy
#### Must-Have Elements (table stakes)
[What top 3 competitors do well — we must match]

#### Differentiation Opportunities (win factors)
[What no competitor does well — we lead here]

#### Information Gain
[Unique value we'll add that no one else provides]

### Recommended SEO Outline
```
H1: [Proposed title]
H2: [Section 1 — based on gap analysis]
H2: [Section 2 — differentiation area]
H2: [Section 3 — depth gap we fill]
H2: FAQ
```

### Sourcing Plan
[3-5 specific statistics and sources competitors miss]

### Target Audience & Angle
[Skill level, role, pain points, unique perspective]

### Estimated Word Count
[Based on competitor analysis + gap coverage]

Save the brief to content/research/YYYY-MM-DD-topic-brief.md.
