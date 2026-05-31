# Rachid Hakim — Content Patterns & Article Structures

## Article Structure (Medium — Standard)

```
H1: [Keyword-rich title, 50-60 chars, promises a specific outcome]
  → Subtitle (1 sentence expanding the title)
  → Image (hero photo, 1200x675, aligned to the topic)
  
  → Hook paragraph: The problem, who has it, why it hurts RIGHT NOW
  → Key Takeaways box (3-5 bullets, each under 20 words)
  
H2: The Problem / Why This Matters
  → Context, specific pain points, real numbers
  → Connect to my experience: "When I was building [product], I hit this exact wall..."

H2: [Core Concept or Solution]
  → Answer-first: main point in first sentence
  → My take: "Here's what I've found works after shipping [X] products..."
  → Explanation with real example from my work

H2: [Step-by-Step Implementation]
  → Numbered steps with clear outcomes
  → Code blocks with language tags and version notes
  → Screenshots or terminal output
  → Common gotchas and how I fixed them

H2: [The Tool/Product That Makes This Easier] (subtle, value-first)
  → "I built [product] to solve exactly this. Here's how it works..."
  → Show the product in action, solving the problem
  → Link to product (or free lead magnet)

H2: [Advanced / Edge Cases] (optional)
  → What breaks at scale and how to handle it
  → Alternative approaches I've tried

H2: Conclusion
  → Summary of what you learned (1-2 sentences)
  → CTA: "I wrote a full guide on this in my [product]. Get it here."
  → Author bio with product links

H2: FAQ
  → 3-5 questions, direct answers (1-2 sentences each)
  → Include one FAQ that naturally mentions a product
```

## Medium-Specific Rules

### Formatting
- Use Medium's header levels: H1 for title only, H2 for section heads, H3 for subsections
- Bold key terms, italicize emphasis
- Pull quotes for memorable statements: > "I spent 12 hours building this once. Never again."
- Code blocks with language tags (Medium supports syntax highlighting)
- Bullet lists and numbered lists for scannability
- Medium clap-worthy moment at the end: "If this helped, clap 50 times and follow me."

### Images
- Featured image at the top: 1200x675 px, relevant, high contrast
- Inline screenshots of real tools/products
- Diagrams for architecture/flow explanations
- Alt text on every image with keywords
- Minimum 1 image per 500 words

### CTA Strategy
- Soft CTA in first 200 words: "I've got a free template for this — link at the bottom."
- Primary CTA at bottom: free lead magnet (checklist, template, mini-guide)
- Secondary CTA: paid product link
- Email capture: "Subscribe to my Substack for the full breakdown"

### Tags
- 5 Medium tags: 2 broad (Productivity, AI), 2 specific (AI Tools, Automation), 1 niche (Agentic AI)
- First tag should match the primary publication

### Publications
- Publish in relevant Medium publications for reach (Towards Data Science, Better Programming, The Startup, etc.)
- If no publication accepts, self-publish with strong SEO title

## Article Variants

### Tutorial Pattern (How-to)
- Focus: step-by-step with screenshots
- Structure: Setup → Steps → Verification → Troubleshooting
- Code-heavy where relevant
- Every step has expected output
- End with: "I automated this whole process. [Product link]"

### Product Showcase Pattern
- Focus: demonstrating a specific product I built
- Structure: Problem → Why I built it → How it works → Real results → How to get it
- Include pricing, features, and honest limitations
- Use real screenshots and data from the product
- No hype — let the product's utility speak

### Comparison Pattern (X vs Y)
- Focus: AI tool comparison for business users
- Structure: Criteria → Head-to-head → Verdict → When to use each
- Benchmarks from my actual usage, not published specs
- Honest recommendation with reasoning
- CTA: "I built a tool to track this — here it is"

### Deep-Dive Pattern
- Focus: how a concept works internally
- Structure: Overview → Architecture → Key components → Edge cases
- Diagrams for architecture
- Source code references with links to my GitHub
- End with practical application: "Here's how I use this in [product]"

### Listicle Pattern
- Focus: curated AI tools or techniques
- Structure: Intro → Items (each with pros/cons/use case) → Comparison → Verdict
- Each item: name, what it does, when to use it, link
- If one item is my product, disclose it honestly
- Avoid generic — be specific and opinionated

### Build-in-Public Pattern
- Focus: transparently sharing product creation journey
- Structure: The idea → The build → The launch → The revenue → The lessons
- Include real numbers: time spent, money made, failures encountered
- Revenue screenshots or analytics
- Authentic over polished

### Newsletter Pattern (Substack)
- Focus: personal, conversational, exclusive
- Structure: Personal anecdote → The insight → Practical application → What's coming
- Shorter than Medium: 1000-1500 words
- Email-friendly formatting
- Include subscriber-only content or early access

### X Thread Pattern
- Focus: bite-sized, viral-optimized
- Structure: Hook (1-2 tweets) → 5-10 detail tweets → Link to full article
- Each tweet is self-contained and quotable
- Numbers and data in screenshots
- Last tweet links to Medium article or product

## SEO Elements

### Title Formulas
- How I Built [X] with AI (and Made $Y in Month One)
- The Complete Guide to [Topic] for Busy Professionals
- I Tried [Tool A] vs [Tool B] for 30 Days — Here's the Winner
- How to [Solve Problem] Without [Expensive/Boring Alternative]
- [Number] AI Tools Every [Professional Type] Should Use in [Year]

### Internal Linking
- Link to my other Medium articles (content clusters)
- Link to my products (Gumroad) with descriptive anchor text
- Link to Substack for newsletter signup
- 2-4 internal links per article

### File Naming
- `YYYY-MM-DD-slug.md` in `content/articles/`
- Slug: lowercase, hyphenated, keyword-focused
- Include frontmatter: title, description, date, tags, author (Rachid Hakim), product_link