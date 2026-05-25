---
name: cluster
agent: copywriter-orchestrator
description: Plan a content cluster with pillar page and supporting articles
---

@.opencode/context/core/quality-standards.md
@.opencode/context/writing/blog-patterns.md
@.opencode/context/writing/seo-and-geo.md
@.opencode/context/writing/competitive-analysis.md

You are the Copywriter Orchestrator.

**Topic for content cluster:** $ARGUMENTS

Plan a complete content cluster for this topic. A content cluster consists of one pillar page (comprehensive, broad coverage) and 4-8 supporting articles (specific, focused subtopics) that all interlink.

### Phase 1: Landscape Analysis
1. Search for the topic and identify what content already exists
2. Map the topic space: what subtopics, questions, and angles are covered
3. Identify gaps where no comprehensive resource exists

### Phase 2: Cluster Architecture
4. Design the pillar page:
   - Title: broad, authoritative, keyword-focused
   - Scope: comprehensive overview of the entire topic
   - Target word count: 3000-5000 words
   - Role: hub that links to all supporting articles

5. Design 4-8 supporting articles:
   - Each covers one specific subtopic in depth
   - Each links back to the pillar page
   - Each links to 2-3 other supporting articles where relevant
   - Target word count: 1500-3000 words each

### Phase 3: Internal Linking Strategy
6. Map the internal linking structure:
   - Pillage → all supporting articles (contextual anchor text)
   - Each supporting article → pillar page (exact-match or partial-match anchor)
   - Supporting articles → related supporting articles (where topical overlap exists)

### Phase 4: Deliverable

## Content Cluster: [Topic]

### Pillar Page
- **Title**: [Proposed title]
- **Target keyword**: [primary keyword]
- **Scope**: [What it covers]
- **Estimated word count**: [3000-5000]
- **H2 Outline**: [Proposed sections]

### Supporting Articles
| # | Title | Target Keyword | Word Count | Links To |
|---|-------|---------------|------------|----------|
| 1 | [Title] | [keyword] | [count] | Pillar, #[X], #[Y] |
| 2 | [Title] | [keyword] | [count] | Pillar, #[X], #[Y] |
| 3 | [Title] | [keyword] | [count] | Pillar, #[X], #[Y] |
| 4 | [Title] | [keyword] | [count] | Pillar, #[X], #[Y] |

### Internal Linking Map
```
Pillar Page
├── → Supporting Article 1
├── → Supporting Article 2
├── → Supporting Article 3
└── → Supporting Article 4

Supporting Article 1 → Pillar, Article 2, Article 3
Supporting Article 2 → Pillar, Article 1, Article 4
[etc.]
```

### Competitive Context
- [What competitors have in this space]
- [Where our cluster can win]
- [Recommended publishing order]

### Sourcing Plan
- [Key statistics and sources needed across the cluster]
- [Shared sources that multiple articles can reference]

Save the cluster plan to content/research/YYYY-MM-DD-topic-cluster.md.
