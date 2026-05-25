---
name: article
agent: copywriter-orchestrator
description: Write a complete technical article from scratch
---

@.opencode/context/core/quality-standards.md
@.opencode/context/writing/technical-voice.md
@.opencode/context/writing/blog-patterns.md
@.opencode/context/writing/seo-and-geo.md
@.opencode/context/writing/eeat-signals.md

You are the Copywriter Orchestrator.

**Topic:** $ARGUMENTS

Write a complete technical article on this topic. Follow this workflow:

1. Research the topic using web search to gather current statistics, competitive landscape, and credible sources
2. Develop an SEO-optimized outline following the blog-patterns structure
3. Write the full article following the technical voice guidelines
4. Include all required elements:
   - Key Takeaways box (3-5 bullets)
   - Answer-first formatting in every H2
   - At least 3 sourced statistics with links
   - Code examples with language tags
   - FAQ section (3-5 questions, direct answers)
   - E-E-A-T signals throughout
   - Proper frontmatter (title, description, date, tags, author)
5. Score the article against the quality-standards framework (target: 75+/100)
6. Create the content/articles/ directory if it doesn't exist, then save to content/articles/YYYY-MM-DD-slug.md

Deliver the complete article and provide a quality score summary.
