# Session Context

This file is used to share context between agents during multi-step workflows.
Agents should read this file at the start of their work and update it with their findings.

## How It Works

1. The orchestrator creates or clears this file at the start of a workflow
2. Each subagent reads the current state, adds its findings, and saves back
3. The next agent reads the accumulated context and builds on it
4. The orchestrator cleans up or archives the file when the workflow completes

## Session Template

```markdown
# Session: [Workflow Type] — [Topic]
Started: YYYY-MM-DD HH:MM
Status: [in-progress / complete / failed]

## Request
- **Command**: [/article /medium /optimize /audit /brief /rewrite /cluster /product-content /repurpose /check]
- **Topic**: [topic description]
- **Target platform**: [Medium / LinkedIn / X / Substack / Threads]
- **Target product**: [product name if applicable]
- **Target file**: [path if applicable]

## Phase 0: Pre-Flight Check
Status: [pending / in-progress / complete / skipped]
- Structural issues found: [count]
- Critical failures: [list if any]

## Phase 1: Competitive Positioning (competitive-analyst)
Status: [pending / in-progress / complete / skipped]
- Primary angle: [keyword/angle]
- Competitors analyzed: [count]
- Top differentiation opportunities:
  1. [opportunity]
  2. [opportunity]
  3. [opportunity]
- Positioning report: content/research/YYYY-MM-DD-topic-positioning.md

## Phase 2: Topic Research (tech-researcher)
Status: [pending / in-progress / complete / skipped]
- Key findings:
  1. [finding with source]
  2. [finding with source]
- Sourced statistics:
  1. [stat] — [source URL, date]
  2. [stat] — [source URL, date]
- Product angle: [how product X relates]

## Phase 3: Writing (tech-writer)
Status: [pending / in-progress / complete / skipped]
- Platform: [Medium / LinkedIn / X / Substack]
- Article: content/articles/YYYY-MM-DD-slug.md
- Word count: [count]
- Product references: [which products, how integrated]
- CTA type: [lead magnet / product / newsletter signup]

## Phase 4: Fact-Check
Status: [pending / in-progress / complete / skipped]
- Statistics verified: [count]
- Code examples verified: [count]
- Technical claims verified: [count]
- Product claims verified: [count]

## Phase 5: Review (reviewer)
Status: [pending / in-progress / complete / skipped]
- Overall score: [X/100]
- Verdict: [PASS / FAIL]
- Critical fixes: [list if any]
- Fix iterations: [0/1/2]

## Phase 6: Iterative Fix Loop
Status: [pending / in-progress / complete / skipped]
- Iteration: [1/2]
- Pre-fix score: [X/100]
- Post-fix score: [X/100]
- Remaining issues: [list]

## Phase 7: Author Validation
Status: [pending / in-progress / complete / skipped]
- Author name: Rachid Hakim
- Bio included: [yes / no]
- Product links: [present / missing]

## Phase 8: Platform Formatting
Status: [pending / in-progress / complete / skipped]
- Medium tags: [5 tags listed]
- LinkedIn formatting: [done / n/a]
- X thread count: [N tweets / n/a]

## Phase 9: Repurposing (if applicable)
Status: [pending / in-progress / complete / skipped]
- LinkedIn post: [done / n/a]
- X thread: [done / n/a]
- Substack issue: [done / n/a]

## Phase 10: Delivery (orchestrator)
Status: [pending / in-progress / complete]
- Final deliverables: [list files]
- Final reviewer score: [X/100]
- Final verdict: [PASS / FAIL]
- Product CTA included: [yes / no]
- Notes: [any issues, limitations, or follow-up recommendations]

## Phase 11: Promotion (orchestrator / social)
Status: [pending / in-progress / complete / skipped]
- Social repurposing: [done / n/a] — files saved to content/social/YYYY-MM-DD-slug/
- Directory submissions: [planned / submitted / n/a]
- Community sharing: [planned / posted / n/a]
- Email notification: [sent / n/a]
- Medium cross-post: [republished / n/a]
- Promotion plan: content/promotion/YYYY-MM-DD-slug-promotion.md
```

## Rules

- Each agent should only update its own phase section
- Do not delete previous phases — append or update status only
- If a phase fails, set status to "failed" and add a note explaining why
- The orchestrator is responsible for creating and cleaning up this file
- Archive completed sessions to content/research/sessions/ if needed for reference
- **Self-assessed scores are invalid** — only reviewer scores count. Do not record self-assessments in the session.
- **Author is always Rachid Hakim** — if any agent strips or changes this, it's an automatic fail