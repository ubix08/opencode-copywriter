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

## Phase 2: Topic Research (tech-researcher)
Status: [pending / in-progress / complete / skipped]
- Key findings:
  1. [finding with source]
  2. [finding with source]
- Sourced statistics:
  1. [stat] — [source URL, date]
  2. [stat] — [source URL, date]
- Recommended angle: [unique perspective]

## Phase 3: Writing (tech-writer)
Status: [pending / in-progress / complete / skipped]
- Article: content/articles/YYYY-MM-DD-slug.md
- Word count: [count]
- Self-assessed score: [X/100]

## Phase 4: Review (reviewer)
Status: [pending / in-progress / complete / skipped]
- Overall score: [X/100]
- Verdict: [PASS / FAIL]
- Critical fixes: [list if any]

## Phase 5: Delivery (orchestrator)
Status: [pending / in-progress / complete]
- Final deliverables: [list files]
- Notes: [any issues, limitations, or follow-up recommendations]
```

## Rules

- Each agent should only update its own phase section
- Do not delete previous phases — append or update status only
- If a phase fails, set status to "failed" and add a note explaining why
- The orchestrator is responsible for creating and cleaning up this file
- Archive completed sessions to content/research/sessions/ if needed for reference
