# Competitive Research & Analysis Methodology

## Research Pipeline (4 Phases)

### Phase 1: Discovery — Find What's Ranking
Search for the target topic and identify:
- Top 5-10 organic results (not ads, not aggregators)
- AI Overview content sources (what AI platforms cite)
- Forum/community threads (Reddit, Hacker News, Stack Overflow)
- YouTube videos with high engagement
- Official documentation pages

For each result, capture:
- URL, title, publish date, last-updated date
- Author/organization and their credibility
- Word count and content type (tutorial, comparison, opinion, docs)
- Target keyword and secondary keywords
- Estimated traffic (if available from search data)

### Phase 2: Deep Analysis — Score Every Competitor
Score each article against these dimensions:

#### Content Depth (0-10)
- 1-3: Surface-level, definitions only, no examples
- 4-6: Basic explanation, some examples, missing edge cases
- 7-8: Comprehensive, real examples, covers most scenarios
- 9-10: Definitive guide, original research, covers edge cases and alternatives

#### Technical Accuracy (0-10)
- 1-3: Outdated, incorrect code, broken links
- 4-6: Mostly correct but missing version info, some deprecated patterns
- 7-8: Accurate, versioned, tested examples
- 9-10: Benchmarked, source-referenced, includes failure modes

#### SEO Structure (0-10)
- 1-3: No heading hierarchy, no meta, poor URL
- 4-6: Basic headings, some keywords, no schema
- 7-8: Proper H1-H3, keyword placement, internal links
- 9-10: Full optimization, schema markup, perfect technical SEO

#### AI Citation Readiness (0-10)
- 1-3: No structured data, no FAQ, no definitions
- 4-6: Some lists, basic FAQ, no direct answers
- 7-8: Key takeaways, FAQ with answers, definition blocks
- 9-10: Fully structured, quotable snippets, citation-ready tables

#### E-E-A-T Signals (0-10)
- 1-3: Anonymous author, no credentials, no sources
- 4-6: Named author, some sources, minimal experience shown
- 7-8: Credible author, sourced statistics, first-hand examples
- 9-10: Recognized expert, original data, transparent methodology

#### Uniqueness / Information Gain (0-10)
- 1-3: Repackages existing content, no original insight
- 4-6: Some original examples, mostly derivative
- 7-8: Unique perspective, original analysis, new synthesis
- 9-10: Breakthrough insight, original research, paradigm shift

### Phase 3: Gap Analysis — Find What's Missing
For each competitor, identify:
- **Content gaps**: Topics they don't cover that readers need
- **Depth gaps**: Topics they cover superficially that deserve deep treatment
- **Angle gaps**: Perspectives they don't consider (beginner, advanced, cost, security)
- **Format gaps**: Missing code examples, diagrams, comparison tables, videos
- **Freshness gaps**: Outdated information, deprecated tools, old versions
- **Trust gaps**: Unsourced claims, no author credentials, no testing dates

### Phase 4: Synthesis — Build the Killer Blueprint
Combine findings into an article strategy:

#### Must-Have Elements (table stakes)
Everything the top 3 results do well. Your article must match or exceed these.

#### Differentiation Opportunities (win factors)
What no competitor does well. This is where you win.

#### Information Gain Strategy
What unique value your article adds that no one else provides:
- Original benchmarks or data
- First-hand case studies
- New methodology or framework
- Synthesis of multiple approaches with clear recommendations
- Updated information where all competitors are stale

#### Target Structure
The optimal heading hierarchy based on what works across competitors + your gaps.

#### Sourcing Plan
Specific statistics, studies, and sources to include that competitors miss.

## Competitive Analysis Output Format

Save research to `content/research/TOPIC-research.md`:

```markdown
# Competitive Research: [Topic]
Date: YYYY-MM-DD

## Search Landscape
- Primary keyword: [keyword]
- Search intent: [informational/commercial/transactional]
- Top ranking content types: [tutorial, comparison, docs, etc.]

## Competitor Analysis

### 1. [Title] — [URL]
- Author/Org: [name]
- Date: [published] / [updated]
- Word count: [estimated]
- Scores: Depth X/10, Accuracy X/10, SEO X/10, AI X/10, E-E-A-T X/10, Unique X/10
- Strengths: [what they do well]
- Weaknesses: [where they fall short]
- Gaps: [what they're missing]

### 2. [Title] — [URL]
[repeat for each competitor]

## Gap Summary
### Content Gaps
- [Topic no one covers well]

### Depth Gaps
- [Topic everyone covers superficially]

### Angle Gaps
- [Perspective no one considers]

### Freshness Gaps
- [Outdated information across competitors]

## Killer Article Blueprint
### Must-Have Elements
- [Table stakes from top competitors]

### Differentiation Opportunities
- [Where we can win]

### Information Gain
- [Unique value we'll add]

### Recommended Structure
H1: [title]
H2: [sections based on gap analysis]

### Sourcing Plan
- [Specific stats and sources to include]
```

## Research Quality Rules
- Analyze minimum 5 competitors, ideally 8-10
- Score objectively — don't inflate weaknesses to make gaps look bigger
- Include at least one official documentation page in analysis
- Check AI Overview sources, not just organic rankings
- Note commercial intent (affiliate articles, product pitches) vs. genuine guides
- Flag any competitor with fabricated statistics or inaccurate claims
- Prioritize recent content (last 12 months) but include evergreen authorities
