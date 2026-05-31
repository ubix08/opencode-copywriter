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
- **Command**: [/article /optimize /audit /brief /rewrite /cluster /check]
- **Topic**: [topic description]
- **Target file**: [path if applicable]

## Phase 0: Pre-Flight Check
Status: [pending / in-progress / complete / skipped]
- Structural issues found: [count]
- Critical failures: [list if any]

## Phase 1: Competitive Research (competitive-analyst)
Status: [pending / in-progress / complete / skipped]
- Primary keyword: [keyword]
- Search intent: [informational/commercial/transactional]
- Competitors analyzed: [count]
- Top differentiation opportunities:
  1. [opportunity]
  2. [opportunity]
  3. [opportunity]
- Research report: content/research/YYYY-MM-DD-topic-research.md

## Phase 2: NotebookLM Research (notebooklm)
Status: [pending / in-progress / complete / skipped]
- Notebooks queried: [names]
- Key findings: [source-grounded answers]

## Phase 3: Topic Research (tech-researcher)
Status: [pending / in-progress / complete / skipped]
- Key findings:
  1. [finding with source]
  2. [finding with source]
- Sourced statistics:
  1. [stat] — [source URL, date]
  2. [stat] — [source URL, date]
- Recommended angle: [unique perspective]

## Phase 4: Writing (tech-writer)
Status: [pending / in-progress / complete / skipped]
- Article: content/articles/YYYY-MM-DD-slug.md
- Word count: [count]
- External links: [count unique domains]
- Internal links: [count]
- Image references: [count]

## Phase 5: Fact-Check
Status: [pending / in-progress / complete / skipped]
- Statistics verified: [count]
- Code examples verified: [count]
- Technical claims verified: [count]
- Issues found: [count]

## Phase 6: Review (reviewer)
Status: [pending / in-progress / complete / skipped]
- Overall score: [X/100]
- Verdict: [PASS / FAIL]
- Critical fixes: [list if any]
- Fix iterations: [0/1/2]

## Phase 7: Iterative Fix Loop
Status: [pending / in-progress / complete / skipped]
- Iteration: [1/2]
- Pre-fix score: [X/100]
- Post-fix score: [X/100]
- Remaining issues: [list]

## Phase 8: Author Validation
Status: [pending / in-progress / complete / skipped]
- Author name: [name]
- Verdict: [valid / generic placeholder]
- Action: [passed / rejected]

## Phase 9: Link Audit
Status: [pending / in-progress / complete / skipped]
- Internal links: [count with descriptive anchor text]
- External unique domains: [count]

## Phase 10: Image Fetch
Status: [pending / in-progress / complete / skipped]
- Placeholders found: [count]
- Images replaced: [count]

## Phase 11: Delivery (orchestrator)
Status: [pending / in-progress / complete]
- Final deliverables: [list files]
- Final reviewer score: [X/100]
- Final verdict: [PASS / FAIL]
- Word count: [count]
- Notes: [any issues, limitations, or follow-up recommendations]
```

## Rules

- Each agent should only update its own phase section
- Do not delete previous phases — append or update status only
- If a phase fails, set status to "failed" and add a note explaining why
- The orchestrator is responsible for creating and cleaning up this file
- Archive completed sessions to content/research/sessions/ if needed for reference
- **Self-assessed scores are invalid** — only reviewer scores count. Do not record self-assessments in the session.
