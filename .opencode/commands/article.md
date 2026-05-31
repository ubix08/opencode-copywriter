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

Write a complete technical article on this topic. Follow the **For New Articles (/article)** workflow from your system prompt. Ensure all required elements are included:

- Key Takeaways box (3-5 bullets, each under 20 words)
- Answer-first formatting in every H2
- At least 3 sourced statistics with links
- Code examples with language tags and version notes
- FAQ section (3-5 questions, direct answers in 1-2 sentences)
- E-E-A-T signals throughout
- Proper frontmatter (title, description, date, lastUpdated, tags, author)
- Named author — no generic placeholders
- JSON-LD schema (Article + FAQPage)
- Image references (1 per 500 words)
- External links: 3-5 unique domains, deduplicated
- Internal links: 3-5 with descriptive anchor text
- Word count: 1500-3000 words

Save research to content/research/YYYY-MM-DD-topic-research.md and article to content/articles/YYYY-MM-DD-slug.md.
