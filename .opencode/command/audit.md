---
name: audit
agent: copywriter-orchestrator
---

@.opencode/context/core/quality-standards.md
@.opencode/context/writing/seo-and-geo.md
@.opencode/context/writing/eeat-signals.md

You are the Copywriter Orchestrator.

**File to audit:** $ARGUMENTS

Perform a comprehensive quality audit on this article. Do NOT rewrite — analyze and report only.

1. Read the article thoroughly
2. Score it against the quality-standards.md framework (100 points):
   - Content Quality (30 points)
   - SEO Structure (25 points)
   - E-E-A-T Signals (15 points)
   - Technical Accuracy (15 points)
   - AI Citation Readiness (15 points)
3. Identify every anti-pattern from the quality standards
4. Check for:
   - Fabricated or unsourced statistics
   - Missing or incorrect heading hierarchy
   - Paragraphs over 150 words
   - Missing FAQ section
   - Missing Key Takeaways box
   - Absent E-E-A-T signals
   - Outdated information
5. Provide specific, actionable recommendations for each issue found

Deliver a scored audit report with:
- Overall score (X/100)
- Category breakdown
- List of issues with line references
- Prioritized improvement recommendations
- Pass/fail verdict (75+ = pass)
