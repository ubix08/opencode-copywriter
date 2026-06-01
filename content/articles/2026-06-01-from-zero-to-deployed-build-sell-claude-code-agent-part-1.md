---
title: "From Zero to Deployed: Build & Sell Your First Claude Code Agent (Part 1)"
description: "Build your first Claude Code agent from scratch — define its role, scope its permissions, wire up MCP tools, create auto-updating AGENTS.md, and land it in a Git repo. Part 1 of a 2-part series on building and selling agents."
date: 2026-06-01
lastUpdated: 2026-06-01
tags: [claude-code, agents, ai-agents, subagents, agent-teams, mcp, tutorial, anthropic]
author: Rachid Hakim
product: "SMB Agent Blueprint — Ready-to-Use Claude Code Agent Templates (gumroad.com/rachidhakim)"
leadMagnet: "Claude Code Agent Starter Template (Free Download)"
series: "Build & Sell Claude Code Agents"
seriesPart: 1
---

**Key Takeaways:**
- A Claude Code agent is a markdown file with YAML frontmatter — role, model, permissions, tools. Nothing more. You define the boundary, Claude fills the rest.
- The single biggest mistake in agent building is giving everything full tool access. Start maximum-restrictive and open up only what fails.
- Agent Teams (experimental, `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`) is the orchestration layer that turns individual agents into a system. But you need to understand a single agent before you can coordinate multiples.
- The 80/20 of agent value is in the SKILL.md: specific instructions beat generic prompts by a wide margin. One well-defined agent with tight instructions outperforms three loosely-defined agents every time.
- Every agent should have a companion `AGENTS.md` or `CLAUDE.md` that describes when to use it — not just what it does. This prevents the wrong agent being selected for a task.
- Cost: A well-scoped agent costs $0.30-2.00 per session depending on model choice and token consumption. The decision matrix below shows which model to pick for which task.

---

# From Zero to Deployed: Build & Sell Your First Claude Code Agent (Part 1)

This is Part 1 of a 2-part series on building, deploying, and selling Claude Code agents. Part 1 covers building and deploying your first agent. Part 2 covers packaging, pricing, and selling it.

> This guide assumes you have Claude Code installed (`npm install -g @anthropic-ai/claude-code`) and a working Anthropic API key. If you don't, the [Claude Code quickstart](https://docs.anthropic.com/en/docs/claude-code/overview) takes 2 minutes.

---

## What Is a Claude Code Agent?

A Claude Code agent is a markdown file with YAML frontmatter that defines:

- **Role** — what the agent does (reviewer, writer, researcher, etc.)
- **Model** — which model it uses (Sonnet 4.6, Opus 4.6, Haiku 4.5)
- **Permissions** — what tools it can access (Read, Edit, Bash, WebSearch, etc.)
- **Instructions** — how it approaches its work

That's it. The agent system in Claude Code is a thin orchestration layer on top of the same underlying LLM. The power comes from the constraints you define, not the complexity of the infrastructure.

### Agent vs Subagent vs Agent Teams

| Term | Meaning | File Location |
|------|---------|---------------|
| **Agent** | Claude Code with a specific role and permissions | `.claude/agents/researcher.md` |
| **Subagent** | Same as agent; spawned by orchestrator via Agent tool | Same as agent |
| **Agent Teams** | Experimental feature for multi-agent orchestration | Config in CLAUDE.md + agents/ |

There is no architectural difference between an "agent" and a "subagent." A subagent is simply an agent that another agent spawned. The distinction is about hierarchy, not capability.

---

## Step 1: Define the Agent's Purpose

Before writing a single line of config, answer three questions:

1. **What specific task does this agent do?** (Not "reviews code" — "reviews Ruby on Rails pull requests for SQL injection, N+1 queries, and missing validations")

2. **What tools does it absolutely need?** (A reviewer needs `Read`, `Glob`, `Grep`. It does NOT need `Edit`, `Bash`, or `WebSearch`.)

3. **What model does it need?** (Research? Haiku 4.5 is fine at 1/3 the cost. Code generation? Sonnet 4.6. Architecture? Opus 4.6.)

**Example scope document:**

```
Agent: rails-reviewer
Task: Review Rails PRs for security and performance issues
Tools needed: Read, Glob, Grep
Model: Haiku 4.5 (most reviews are pattern-matching, not creative)
Input: PR diff + related files
Output: Structured review with severity levels
```

This scoping document is your contract. Everything in the agent definition enforces these boundaries.

---

## Step 2: Create the Agent File

Agents live in `.claude/agents/` directory (or `.opencode/agents/` for OpenCode compatibility). Create one:

```bash
mkdir -p .claude/agents
```

**Example: `rails-reviewer.md`:**

```markdown
---
name: rails-reviewer
description: Reviews Ruby on Rails pull requests for security and performance issues
model: haiku-4-5
temperature: 0.1
permission:
  read: allow
  glob: allow
  grep: allow
  edit: deny
  bash: deny
  webSearch: deny
  webfetch: deny
---

# Rails PR Reviewer

You are a senior Rails developer reviewing a pull request.

## What to check (in priority order)

### Security
- SQL injection in raw SQL, `where`, `find_by_sql`, and `order` calls
- Mass assignment in `update`, `create`, `update_attributes` without strong params
- Cross-site scripting in `raw()`, `html_safe`, and `sanitize` calls
- Insecure direct object references (check `find` vs `current_user.resources.find`)
- Hardcoded secrets or API keys

### Performance
- N+1 queries (missing `includes` in loops)
- Missing database indexes on new foreign keys or polymorphic types
- Unscoped `all` or `each` on large tables
- Inefficient queries in callbacks

### Correctness
- Missing validations for new database columns
- Race conditions in counter caches or `update_all`
- Incorrect use of `save` vs `save!`
- Callback ordering issues

## Output format

For each finding:

```
SEVERITY: critical|major|minor
FILE: app/models/user.rb:42
ISSUE: One-line description
FIX: Specific code change suggestion
```

If the PR has no issues, output only: "No issues found in this PR."
```

### Key Decisions in This Agent

- **`model: haiku-4-5`** — Code review is primarily pattern matching, not creative work. Haiku 4.5 costs $1/1M input tokens vs Sonnet 4.6 at $3/1M. At an average of 25K tokens per review, that's $0.03 vs $0.08 per review. For 100 reviews/month, that saves $5.
- **`temperature: 0.1`** — Low temperature means deterministic, consistent output. You don't want creative reviews — you want reliable ones.
- **`edit: deny, bash: deny`** — The reviewer reads only. If it could edit, it might "fix" things during the review. If it could run bash, it could execute the PR's code during analysis — a security risk.
- **Specific instructions beat generic ones** — Notice the checklist format with concrete Rails-specific patterns (N+1 queries, strong params, counter caches). A generic "review this code for quality" prompt would produce vague output.

---

## Step 3: Scope Permissions Correctly

Permission scoping is the difference between a safe agent and a liability. The principle: deny everything, then allow only what's necessary.

### Permission Levels

| Value | Behavior |
|-------|----------|
| `allow` | Agent can use the tool without confirmation |
| `ask` | Agent can use the tool but asks for permission first |
| `deny` | Agent cannot use the tool at all |

### Permission Templates by Agent Type

**Researcher / Analyst (read-only):**

```yaml
permission:
  read: allow
  glob: allow
  grep: allow
  edit: deny
  bash: deny
  webSearch: ask
  webfetch: ask
```

**Writer / Developer (read-write, controlled commands):**

```yaml
permission:
  read: allow
  edit: allow
  glob: allow
  grep: allow
  bash:
    "npm run *": allow
    "git status": allow
    "git diff": allow
    "git add *": ask
    "git commit *": ask
    "*": deny
  webSearch: ask
```

**DevOps / Automation (broader bash access):**

```yaml
permission:
  read: allow
  edit: allow
  bash:
    "npm *": allow
    "docker *": allow
    "aws *": ask
    "kubectl *": ask
    "*": deny
```

### The Most Common Permission Mistakes

1. **Giving `bash: allow` to a reviewer.** Now it can execute the code it's reviewing — including potentially malicious PR code.
2. **Giving `webSearch: allow` to every agent.** Every web search consumes tokens and context. The researcher needs it. The reviewer doesn't.
3. **No bash restrictions at all.** `bash: allow` with no glob patterns means the agent can run anything — `rm -rf /`, `curl malware.example.com`, etc.
4. **Over-restricting the orchestrator.** The orchestrator agent needs `Agent` tool access to spawn subagents. Denying it breaks the multi-agent pattern entirely.

---

## Step 4: Wire Up MCP Tools

Agents are more powerful when they can access external tools via the Model Context Protocol. Configure MCP servers in `opencode.json` or `.claude/mcp.json`:

```json
{
  "mcpServers": {
    "brave-search": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-brave-search"],
      "env": ["BRAVE_API_KEY=your-key"]
    },
    "github": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": ["GITHUB_TOKEN=your-token"]
    }
  }
}
```

Then reference MCP tools in the agent's instructions:

```markdown
## Tools available
- `brave-search_web_search` — Search the web for current information
- `github_search_repositories` — Search GitHub for code patterns  
- `github_get_pull_request` — Read PR details and diffs
```

**MCP context cost:** Every MCP server adds tool definitions to the context window. The GitHub MCP server alone adds ~5,000 tokens. With the Brave Search server at ~2,000 tokens, you're at 7K tokens before the conversation starts. Be selective — 3-5 focused servers is the practical limit.

---

## Step 5: Add Auto-Updating AGENTS.md

An agent without context is a tool without instructions. Every agent directory should include an `AGENTS.md` that tells any LLM agent — not just Claude Code — what this agent is and when to use it.

```
.claude/agents/rails-reviewer/
  rails-reviewer.md           # The agent definition
  AGENTS.md                   # Project context for this agent
```

**Example `AGENTS.md` for the reviewer agent:**

```markdown
# Rails Reviewer Agent

## When to use
Use this agent when reviewing Ruby on Rails pull requests for security vulnerabilities, performance issues, or correctness problems.

## When NOT to use
- For frontend code review (use the frontend-reviewer agent)
- For architecture decisions (use the architect agent)
- For writing new code (use the developer agent)

## How to invoke
```bash
claude --agent rails-reviewer --prompt "Review PR #42"
```

Or in Agent Teams, the orchestrator can spawn it automatically.

## Model
Haiku 4.5 — sufficiently capable for pattern-matching review tasks at 1/3 the cost of Sonnet.

## Cost
~$0.03-0.08 per review session (25K-75K tokens at Haiku 4.5 rates).

## Dependencies
- GitHub MCP server (for reading PRs)
```

This file serves two purposes:
1. **Documentation** — for humans setting up the agent
2. **Discovery** — for other agents deciding which subagent to spawn

---

## Step 6: Test the Agent

Before wiring up orchestration, test the agent in isolation:

```bash
# Direct invocation
claude --agent rails-reviewer --prompt "Review the current state of app/models/user.rb for security issues"
```

### Test Checklist

- [ ] Agent invokes without errors
- [ ] Agent correctly follows permission boundaries
- [ ] Agent reads allowed files and directories
- [ ] Agent is denied from writing to files
- [ ] Agent is denied from running bash
- [ ] Output format matches the specification
- [ ] Agent maintains low temperature (consistent output on same input)
- [ ] Token consumption is within expected range

### Testing with the Plan Agent

Claude Code's built-in `plan` agent (read-only, exploratory) is useful for testing your custom agent's scope:

```
Switch to plan mode and review my rails-reviewer agent definition.
Does it have any permission gaps? Are the instructions specific enough?
```

---

## Step 7: Add Agent Teams Orchestration

Once the individual agent works, integrate it into Agent Teams. Enable the experimental feature:

```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

Then define an orchestrator in `.claude/agents/orchestrator.md`:

```markdown
---
name: orchestrator
description: Orchestrates multi-agent code reviews
model: sonnet-4-6
temperature: 0.3
permission:
  read: allow
  edit: deny
  bash: deny
  agent:
    rails-reviewer: allow
    developer: allow
---

# Code Review Orchestrator

You coordinate code reviews. When a pull request arrives:

1. Spawn `rails-reviewer` to analyze backend changes
2. Collect findings
3. If changes are needed, spawn `developer` with the reviewer's findings
4. Verify the fixes with `rails-reviewer` again
5. Summarize the full review cycle
```

### The Orchestration Pattern

The orchestrator follows a simple loop:

```
1. Receive PR URL or diff
2. Determine which agents are needed (based on changed files)
3. Spawn subagents in parallel (for independent file reviews)
4. Collect outputs
5. If issues found: spawn developer + verify cycle
6. Return structured report
```

This pattern is deliberately simple. Complex orchestration logic (retry queues, fallback agents, custom routing) adds complexity that isn't justified until you have 50+ reviews per week.

---

## Step 8: Deploy to Git

An agent is code. Treat it like code:

```bash
git add .claude/agents/
git commit -m "Add rails-reviewer agent: security-focused Rails PR reviewer"
```

### Team Distribution

For team environments, share agents via Git or a private registry:

- **Git submodules** — Share agent directories across repos
- **Internal package** — npm/GitHub package with agent files
- **Vendor directory** — `.claude/vendor/` with upstream agents

### Agent Directory Structure for Distribution

```
.claude/agents/
  orchestrator.md                     # Orchestrator agent
  rails-reviewer/
    rails-reviewer.md                 # Agent definition
    AGENTS.md                         # Context and usage docs
    README.md                         # Human-facing documentation
  developer/
    developer.md                      # Agent definition
    AGENTS.md                         # Context and usage docs
    skills/
      rails-best-practices.md         # Reference skill file
```

---

## The Decision Matrix: Which Model for Which Agent?

Not every agent needs Sonnet 4.6. Here's the cost/quality breakdown:

| Task Type | Model | Input Cost/1M Tokens | Quality | Best For |
|-----------|-------|---------------------|---------|----------|
| **Pattern matching** (reviews, linting, validation) | Haiku 4.5 | $1.00 | 85% | High-volume, low-creativity tasks |
| **Content generation** (drafts, docs, copy) | Sonnet 4.6 | $3.00 | 95% | Most agent work |
| **Architecture** (planning, design, complex refactors) | Opus 4.6 | $15.00 | 98% | High-consequence decisions |
| **Research** (web search, summarization) | Haiku 4.5 | $1.00 | 80% | Cheap, fast, good enough |

**Cost decision rule:** If you can define the task as a checklist, use Haiku. If the task requires judgment or creativity, use Sonnet. If the task involves multi-step reasoning with high stakes, use Opus.

---

## Part 1 Recap: What You Built

By the end of Part 1, you have:

1. A defined agent scope document
2. A `.claude/agents/rails-reviewer.md` file with permissions, model, and instructions
3. MCP server configuration for GitHub and Brave Search
4. An `AGENTS.md` for discovery and documentation
5. A tested agent that runs in isolation
6. An orchestrator for Agent Teams integration
7. A Git-tracked directory ready for team distribution

**Part 2** covers packaging this agent for sale — writing Gumroad listings, pricing strategies, customer acquisition channels, and the 10-agent template pack that turns this process into a repeatable system.

---

## About the Author

**Rachid Hakim** — I'm an ERP consultant turned AI builder. I've been building Claude Code agents since the early beta and ship practical tools for developers, freelancers, and indie hackers.

- **Products:** [Interactive HTML tools and technical guides](https://gumroad.com/rachidhakim) for devs and creators
- **Get the free Agent Starter Template:** A ready-to-use `rails-reviewer.md`, `AGENTS.md`, and orchestrator pattern from this guide
- **SMB Agent Blueprint ($19):** The complete 10-agent template pack with pricing guide, Gumroad listings, and automated deployment scripts
- **Follow me:** [@rachidhakim](https://x.com/rachidhakim) on X for daily AI dev workflows

---

*Built and tested with Claude Code v2.1.63+, Sonnet 4.6, and MCP SDK 2026.1.26. June 1, 2026.*
