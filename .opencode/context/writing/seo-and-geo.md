# SEO & AI Citation Optimization (GEO)

## Google Ranking Optimization

### On-Page SEO Checklist
- Target keyword in: H1, first 100 words, URL slug, meta description, image alt text
- Keyword density: 1-2% (natural, no stuffing)
- Semantic keywords: related terms, synonyms, topic variations
- Heading hierarchy: H1 → H2 → H3, no skips, one H1 only
- Paragraph length: max 150 words, average 50-80
- Sentence length: average 15-20 words, max 30
- Internal links: 3-5 with descriptive anchor text
- External links: 3-5 to authoritative sources
- Readability: Flesch score 50-70 (technical audience)

### Content Freshness
- `lastUpdated` date in frontmatter
- Version notes when tools/dependencies change
- "Updated for [Year]" in title when significantly revised
- Changelog section for major revisions

## AI Citation Optimization (GEO/AEO)

### What AI Extractors Look For
AI platforms (ChatGPT, Perplexity, Gemini, Google AI Overviews) extract:
- Direct answers to specific questions
- Structured data (tables, lists, numbered steps)
- Statistics with sources
- Definitions and explanations
- Step-by-step instructions

### Optimization Tactics

#### 1. Key Takeaways Box
Place near top (after intro), 3-5 bullets, each under 20 words.
Format:
```
**Key Takeaways:**
- [Point 1: specific, actionable]
- [Point 2: specific, actionable]
- [Point 3: specific, actionable]
```

#### 2. FAQ Section (Direct-Answer Format)
Each FAQ:
- H2: exact question phrasing
- 1-2 sentence direct answer first
- Optional: expansion paragraph after

Example:
```
## What is the difference between X and Y?
X handles [specific function] while Y focuses on [different function].
Choose X when [condition], Y when [other condition].
```

#### 3. Definition Blocks
For every technical term the audience might not know:
```
**Term**: Concise definition in one sentence.
```

#### 4. Citation Tiers
- Tier 1 (best): Original research, official documentation, primary data
- Tier 2: Reputable industry publications, recognized experts
- Tier 3: Well-known blogs, community resources
- Avoid: Forums, social media, unverified claims

#### 5. Structured Content
- Use tables for comparisons
- Use numbered lists for procedures
- Use bullet lists for features/benefits
- Use code blocks with language tags
- Each list item should be self-contained and quotable

#### 6. Information Gain
What does this article add that the top 5 results don't?
- Original data or benchmarks
- First-hand experience and screenshots
- Unique perspective or methodology
- Updated information where others are stale
- Synthesis of multiple sources with new conclusions

## JSON-LD Schema (Include in HTML/MDX output)
- Article schema: headline, description, author, datePublished, dateModified
- FAQPage schema: all FAQ questions and answers
- BreadcrumbList schema: site hierarchy
