# Content Templates & Reusable Patterns

## Key Takeaways Box
Place after intro paragraph, before first H2.

```markdown
**Key Takeaways:**
- [Specific, actionable point — under 20 words]
- [Specific, actionable point — under 20 words]
- [Specific, actionable point — under 20 words]
```

## FAQ Section Template
Each FAQ uses H2 heading with direct answer in first 1-2 sentences.

```markdown
## What is [term/concept]?
[Direct answer in 1-2 sentences. Define the term clearly.]

[Optional: expansion paragraph with context, examples, or caveats.]

## How do I [action]?
[Direct answer: the method or approach in 1-2 sentences.]

[Optional: step-by-step breakdown or code example.]

## When should I use X vs Y?
[Direct answer: the decision criteria in 1-2 sentences.]

[Optional: comparison table or specific scenarios.]
```

## Definition Block Template
For technical terms the audience may not know.

```markdown
**Term**: Concise definition in one sentence, using plain language.
```

## Author Bio Template
Place at end of article or in frontmatter.

```markdown
**About the author:** [Name] is a [role] at [company] with [X] years of experience in [domain]. They have [specific credential or achievement]. Read more of their work on [topic1] and [topic2].
```

## Code Block Template
Every code block must include:
- Language tag
- Version note (if applicable)
- Comments explaining "why", not "what"

````markdown
```python
# Python 3.12+
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
async def health_check():
    # Return status for load balancer health probes
    return {"status": "ok", "version": "1.0.0"}
```
````

## Comparison Table Template
Use for head-to-head comparisons.

```markdown
| Feature | Option A | Option B | Winner |
|---------|----------|----------|--------|
| [Criterion 1] | [Detail] | [Detail] | [A/B/Tie] |
| [Criterion 2] | [Detail] | [Detail] | [A/B/Tie] |
| Performance | [Metric] | [Metric] | [A/B/Tie] |
| Ease of use | [Assessment] | [Assessment] | [A/B/Tie] |
```

## Step-by-Step Template
Use numbered lists for procedures.

```markdown
1. **[Action verb]** — [What to do and why]
   ```[language]
   [command or code]
   ```
   Expected output: `[result]`

2. **[Action verb]** — [What to do and why]
   ```[language]
   [command or code]
   ```
   Expected output: `[result]`
```

## Internal Link Template
Use descriptive anchor text, not "click here" or "read more."

```markdown
- For setup instructions, see [how to configure X in our getting started guide](/articles/YYYY-MM-DD-slug)
- Learn more about [advanced caching strategies](/articles/YYYY-MM-DD-slug)
- Compare [X vs Y performance benchmarks](/articles/YYYY-MM-DD-slug)
```

## Warning/Callout Template
For deprecated features, breaking changes, or important caveats.

```markdown
> **Warning:** [Clear statement of the risk]. [What happens if ignored]. [How to avoid or mitigate].
```

## Changelog Entry Template
For articles that are updated significantly.

```markdown
## Changelog
- **YYYY-MM-DD**: Updated for [tool] v[X.Y]. Replaced deprecated [feature] with [replacement]. Added section on [new topic].
- **YYYY-MM-DD**: Initial publication.
```

## Frontmatter Template
```yaml
---
title: [Keyword-rich title, 50-60 chars]
description: [Meta description, 150-160 chars, includes keyword and CTA]
date: YYYY-MM-DD
lastUpdated: YYYY-MM-DD
tags: [primary-tag, secondary-tag, tertiary-tag]
author: [Author Name]
---
```
