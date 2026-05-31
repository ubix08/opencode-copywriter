# Content Templates & Reusable Patterns for Rachid Hakim

## Key Takeaways Box
Place after intro paragraph, before first H2.

```markdown
**Key Takeaways:**
- [Specific, actionable insight — under 20 words]
- [Specific, actionable insight — under 20 words]
- [Specific, actionable insight — under 20 words]
- [Bonus:] [product name] automates this — grab it below.
```

## Author Bio Template (use at end of every article)

```markdown
**About the author:** Rachid Hakim is an AI product builder and former ERP consultant. He creates AI-powered digital tools for businesses and writes about building things that actually sell. Grab his free [resource name] at [link] or check out his full toolkit at [gumroad.com/rachidhakim](https://gumroad.com/rachidhakim).
```

## Product CTA Templates

### Soft CTA (bottom of article, after value delivery)
```markdown
---

**Want the shortcut?**

I built [Product Name] to solve exactly this problem. It's a [brief description] that does [specific thing]. Get it here: [Gumroad URL]

Or grab the free [lead magnet name] to get started: [link]
```

### Inline CTA (during relevant section)
```markdown
When I hit this problem building my [Product Name], I ended up automating the whole thing. Here's how [product] handles it...

*→ [Product Name] handles this automatically. [Link]*
```

### Lead Magnet CTA (top of article)
```markdown
---

**Before you dive in:** I put together a free [checklist/template/guide] for this. [Download it here] — no email required.
```

### Product Showcase CTA (within a dedicated section)
```markdown
## The Tool That Makes This Painless

I built [Product Name] because I was tired of doing [painful thing] manually. Here's what it does:

- [Feature 1]: [what it solves]
- [Feature 2]: [what it solves]
- [Feature 3]: [what it solves]

It's [$price] (one-time) and includes [bonus items].

**[Get [Product Name] →](Gumroad URL)**
```

## FAQ Section Template

```markdown
## Frequently Asked Questions

### What is [term/concept]?
[Direct answer in 1-2 sentences.]

### How do I [specific action]?
[Direct answer with method or approach.]

### Do I need to know how to code?
If the topic requires coding, say so honestly. If not, explain why.

### Is there a tool that handles this?
[If a product covers this:] Yes — I built [Product Name] to solve exactly this. [Link]

### How much does this cost?
[If the topic involves a paid product, answer honestly with pricing.]
```

## Medium Article Frontmatter Template

```yaml
---
title: [Keyword-rich title, 50-60 chars]
subtitle: [One-sentence expansion, 120-150 chars]
description: [SEO description, 150-160 chars]
date: YYYY-MM-DD
lastUpdated: YYYY-MM-DD
tags: [tag1, tag2, tag3, tag4, tag5]
author: Rachid Hakim
canonical: [Medium URL if republished elsewhere]
product: [product name and URL if applicable]
leadMagnet: [free resource name and URL]
---
```

## LinkedIn Post Template

```markdown
[Problem statement / surprising observation — 1-2 sentences]

Here's what I've learned after [timeframe / number of projects]:

[Key insight 1 — bolded]
[Explanation — 1-2 sentences]

[Key insight 2 — bolded]
[Explanation — 1-2 sentences]

[Key insight 3 — bolded]
[Explanation — 1-2 sentences]

The takeaway: [one-sentence conclusion]

I wrote the full breakdown on Medium: [link]

#AI #[SpecificTopic] #[RelevantHashtag]
```

## X Thread Template

```markdown
Tweet 1: [Hook — a surprising fact, question, or bold claim]
🧵

Tweet 2: [Context — the problem and who it affects]

Tweet 3: [Solution overview — what I built or discovered]

Tweet 4-N: [Step-by-step breakdown, each tweet self-contained]

Final tweet: [Summary + link to full Medium article + CTA]
⬇️ I wrote the full guide here: [Medium URL]
```

## Code Block Template
Every code block must include language tag and context.

```markdown
```yaml
# worker.yaml — Agent definition for [purpose]
name: [agent_name]
model: [provider/model]
prompt: |
  [agent instructions]
```

```python
# Python 3.12+
# [what this code does and why]
```

```bash
# Run this on Ubuntu 22.04+
# [commands with explanation]
```
```

## Comparison Table Template

```markdown
| Feature | Tool A | Tool B | [My Product] |
|---------|--------|--------|--------------|
| Core function | [detail] | [detail] | [detail] |
| Setup time | [time] | [time] | [time] |
| Cost | [$] | [$] | [$] |
| Best for | [use case] | [use case] | [use case] |
```

## Build-in-Public Revenue Table Template

```markdown
| Month | Products Live | Revenue | Build Time (hrs) | Lessons |
|-------|---------------|---------|------------------|---------|
| 1 | [count] | [$] | [hrs] | [key lesson] |
| 2 | [count] | [$] | [hrs] | [key lesson] |
```

## Lead Magnet Card Template

```markdown
---

**📦 Free Resource: [Name]**

What's inside:
✅ [Item 1]
✅ [Item 2]
✅ [Item 3]

→ [Download link (Gumroad free / Google Drive / email-gated)]
```

## Warning/Callout Template

```markdown
> ⚠️ **Real talk:** [Clear statement of limitation or risk]. [What I learned the hard way]. [How to avoid it].
```

## Changelog Entry Template

```markdown
## Changelog
- **YYYY-MM-DD**: Updated for [reason]. Added section on [new topic].
- **YYYY-MM-DD**: Initial publication.
```