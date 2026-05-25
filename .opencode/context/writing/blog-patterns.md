# Technical Blog Post Patterns

## Article Structure (Standard)

```
H1: [Keyword-rich title, 50-60 chars]
  → Meta description (150-160 chars)
  → Key Takeaways box (3-5 bullets)
  → Hook paragraph (problem + promise, under 100 words)

H2: The Problem / Why This Matters
  → Context, pain points, who this affects

H2: [Core Concept or Solution Overview]
  → Answer-first: main point in first sentence
  → Explanation with example

H2: [Step-by-Step Implementation]
  → Numbered steps
  → Code blocks with language tags
  → Expected output after each major step

H2: [Common Pitfalls / Gotchas]
  → What goes wrong and how to fix it

H2: [Advanced / Optimization] (optional)
  → Performance tips, edge cases, alternatives

H2: Conclusion
  → Summary (1-2 sentences)
  → Call to action (try it, read more, share)

H2: FAQ
  → 3-5 questions, direct answers (1-2 sentences each)
```

## Article Variants

### Tutorial Pattern
- Focus: step-by-step, reproducible results
- Structure: Setup → Steps → Verification → Troubleshooting
- Code-heavy, minimal theory
- Every step has expected output

### Comparison Pattern
- Focus: X vs Y decision guide
- Structure: Criteria → Head-to-head → Verdict → When to choose each
- Include benchmarks, feature tables, pricing
- Clear recommendation with reasoning

### Deep-Dive Pattern
- Focus: how something works internally
- Structure: Overview → Architecture → Key components → Edge cases
- Diagrams or ASCII art for architecture
- Source code references with links

### Listicle Pattern (Technical)
- Focus: curated tools, techniques, or resources
- Structure: Intro → Items (each with pros/cons/use case) → Comparison table → Verdict
- Each item: name, what it does, when to use it, link
- Avoid generic "top 10" — be specific and opinionated

## SEO Elements

### Title Formulas
- How to [Action] in [Technology] (Step-by-Step)
- [X] vs [Y]: Which Should You Use in [Year]?
- The Complete Guide to [Topic]
- [Number] [Topic] Mistakes (and How to Fix Them)

### Internal Linking
- Link to related articles with descriptive anchor text
- 3-5 internal links per article
- Link from new articles to older ones (build clusters)
- Use exact-match or partial-match anchor text

### Image & Diagram Rules
- Minimum 1 image per 500 words
- Screenshots for UI steps, diagrams for architecture
- Alt text: descriptive, includes keyword naturally
- File names: hyphenated, descriptive (not screenshot-1.png)

## File Naming
- `YYYY-MM-DD-slug.md` in `content/articles/`
- Slug: lowercase, hyphenated, keyword-focused
- Include frontmatter: title, description, date, tags, author
