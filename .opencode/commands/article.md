---
name: article
agent: copywriter-orchestrator
description: Write a complete technical article with competitive research
---

@.opencode/context/core/quality-standards.md
@.opencode/context/writing/technical-voice.md
@.opencode/context/writing/blog-patterns.md
@.opencode/context/writing/seo-and-geo.md
@.opencode/context/writing/eeat-signals.md
@.opencode/context/writing/competitive-analysis.md

You are the Copywriter Orchestrator.

**Topic:** $ARGUMENTS

Write a complete technical article on this topic. Follow this workflow:

### Phase 1: Competitive Research
1. Search for the topic and identify top 5-8 ranking articles
2. Read each competitor article and score them using the competitive-analysis.md framework
3. Identify gaps: content, depth, angle, format, freshness, trust
4. Build a killer article blueprint: what must-haves + differentiation opportunities + information gain

### Phase 2: Topic Research
5. Research the topic for current statistics, credible sources, and technical details
6. Gather specific data points that competitors miss or get wrong

### Phase 3: Writing
7. Develop an SEO-optimized outline based on the competitive blueprint
8. Write the full article following the technical voice guidelines
9. Include all required elements:
   - Key Takeaways box (3-5 bullets)
   - Answer-first formatting in every H2
   - At least 3 sourced statistics with links
   - Code examples with language tags
   - FAQ section (3-5 questions, direct answers)
   - E-E-A-T signals throughout
   - Proper frontmatter (title, description, date, tags, author)

### Phase 4: Quality & Delivery
10. Score the article against quality-standards.md (target: 75+/100)
11. Create content/ directories if they don't exist
12. Save research to content/research/YYYY-MM-DD-topic-research.md
13. Save article to content/articles/YYYY-MM-DD-slug.md

Deliver: the complete article, a competitive summary (what we beat and why), and a quality score.
