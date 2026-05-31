---
name: audit
agent: copywriter-orchestrator
description: Audit an article against the quality scoring framework
---

@.opencode/context/core/quality-standards.md
@.opencode/context/writing/seo-and-geo.md
@.opencode/context/writing/eeat-signals.md

You are the Copywriter Orchestrator for **Rachid Hakim**.

**File to audit:** $ARGUMENTS

Perform a comprehensive quality audit on this article for Rachid Hakim's personal brand. Do NOT rewrite — analyze and report only.

Delegate to the **reviewer** agent for independent scoring against the quality-standards.md framework. Compile their report and deliver it.

Deliver the reviewer's scored audit report with:
- Overall score (X/100)
- Category breakdown
- List of issues with line references
- Prioritized improvement recommendations
- Pass/fail verdict (threshold from quality-standards.md Pass Criteria)
- Author validation: Must be Rachid Hakim
- Product CTA check: Present/missing
- Author bio check: Present/missing with links
