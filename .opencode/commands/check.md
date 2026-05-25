---
name: check
agent: copywriter-orchestrator
description: Quick validation of article structure and required elements
---

@.opencode/context/core/quality-standards.md
@.opencode/context/writing/blog-patterns.md
@.opencode/context/writing/seo-and-geo.md

You are the Copywriter Orchestrator.

**File to check:** $ARGUMENTS

Perform a quick structural validation of this article. This is NOT a full audit — it is a fast check for required elements and obvious issues.

### Checklist

1. **Frontmatter**: title, description (150-160 chars), date, lastUpdated, tags, author — all present?
2. **H1**: Exactly one, keyword-rich, 50-60 chars?
3. **Heading hierarchy**: H1 → H2 → H3, no skipped levels?
4. **Key Takeaways**: Box near top, 3-5 bullets, each under 20 words?
5. **FAQ section**: 3-5 questions, H2 headings, direct answers in 1-2 sentences?
6. **Sourced statistics**: At least 3, with working links and dates?
7. **Code blocks**: All have language tags?
8. **Paragraph length**: Any over 150 words? (count them)
9. **Internal links**: 3-5 with descriptive anchor text?
10. **External links**: 3-5 to authoritative sources?
11. **E-E-A-T signals**: Author bio, experience examples, date stamps?
12. **Meta description**: 150-160 chars, includes keyword, has CTA?

### Output Format

## Quick Check: [Article Title]

| Check | Status | Notes |
|-------|--------|-------|
| Frontmatter | ✅/❌ | [missing fields if any] |
| H1 | ✅/❌ | [issue if any] |
| Heading hierarchy | ✅/❌ | [skipped levels if any] |
| Key Takeaways | ✅/❌ | [issue if any] |
| FAQ section | ✅/❌ | [issue if any] |
| Sourced stats | ✅/❌ | [count found vs required] |
| Code blocks tagged | ✅/❌ | [untagged blocks if any] |
| Paragraph length | ✅/❌ | [count of long paragraphs] |
| Internal links | ✅/❌ | [count found vs required] |
| External links | ✅/❌ | [count found vs required] |
| E-E-A-T signals | ✅/❌ | [missing signals if any] |
| Meta description | ✅/❌ | [length and keyword check] |

**Result: [PASS — all checks green / FAIL — X checks failed]**

### Failed Checks (Fix These)
1. [Check name]: [specific issue and how to fix]

This check does NOT score content quality, verify accuracy, or assess competitive positioning. Use `/audit` for a full quality score.
