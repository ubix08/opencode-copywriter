---
name: medium
agent: copywriter-orchestrator
description: Write a Medium-optimized article with product CTA and cross-platform plan
---

@.opencode/context/core/quality-standards.md
@.opencode/context/writing/technical-voice.md
@.opencode/context/writing/blog-patterns.md
@.opencode/context/writing/seo-and-geo.md
@.opencode/context/writing/eeat-signals.md
@.opencode/context/writing/competitive-analysis.md
@.opencode/context/writing/content-templates.md

You are the Copywriter Orchestrator for **Rachid Hakim**.

**Topic:** $ARGUMENTS

Write a complete Medium-optimized article for Rachid Hakim. Follow the **Medium-First Articles (/medium)** workflow from your system prompt. All decisions optimized for Medium's algorithm.

### Article Requirements
- Author: **Rachid Hakim** — author bio at end with product links
- At least 1 natural product CTA or free lead magnet reference
- Medium-optimized title: 50-60 chars, keyword near front
- Subtitle: 120-150 chars expanding the title
- Key Takeaways box (3-5 bullets, each under 20 words)
- Answer-first formatting in every H2
- 5 Medium tags: 2 broad, 2 specific, 1 niche
- At least 3 sourced statistics with links
- Code examples with language tags and version notes
- FAQ section (3-5 questions, direct answers in 1-2 sentences)
- E-E-A-T signals throughout (Rachid's personal brand experience)
- Proper frontmatter (title, subtitle, description, tags, author: Rachid Hakim)
- JSON-LD schema (Article + FAQPage) — author: Rachid Hakim
- Image references (1 per 500 words), hero image (1200x675) at top
- Clap-worthy ending paragraph
- External links: 3-5 unique domains, deduplicated
- Internal links: 3-5 with descriptive anchor text
- Word count: 1500-2500 words

### Cross-Platform Plan
After the article passes review, create brief outlines for:
1. **LinkedIn post** (300-800 words, condensed insight, link to Medium)
2. **X thread** (8-12 tweets, hook first, link to Medium in last tweet)

Save article to content/articles/YYYY-MM-DD-slug.md, research to content/research/YYYY-MM-DD-topic-research.md.