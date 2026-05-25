---
title: "How to Build an Agentic Operating System with Claude Code"
description: "Learn how to architect a multi-agent system using Claude Code's orchestration capabilities, MCP servers, and context management for automated workflows."
date: 2026-05-25
lastUpdated: 2026-05-25
tags: [claude-code, agentic-systems, mcp, ai-agents, automation, claude]
author: Technical Writing Team
---

**Key Takeaways:**
- Claude Code's Task tool enables multi-agent orchestration within a single session
- MCP servers extend agent capabilities with external tools like search, databases, and APIs
- Context files (.md) injected via @ references create domain-specific agent behavior
- A 3-layer architecture (commands → context → agents) separates concerns and scales cleanly
- Permission-based tool access prevents subagents from exceeding their intended scope

---

# How to Build an Agentic Operating System with Claude Code

An agentic operating system is a multi-agent architecture where specialized AI assistants coordinate research, writing, coding, and analysis workflows — all orchestrated through Claude Code's native task delegation, Model Context Protocol (MCP) servers, and context injection. This guide shows you how to build one from scratch.

## What Is an Agentic Operating System?

**Agentic operating system**: A software architecture where multiple AI agents, each with specialized roles and tool access, coordinate to complete complex workflows that a single agent cannot handle efficiently.

Unlike a single AI assistant that tries to do everything, an agentic OS delegates specific tasks to purpose-built agents. A researcher gathers information. A writer drafts content. A reviewer validates quality. An orchestrator coordinates them all.

The pattern mirrors how human teams work: specialization, delegation, and review cycles. Claude Code provides the primitives to build this system directly in your terminal.

## Why Claude Code for Agent Orchestration?

Claude Code ships with built-in multi-agent support that most coding agents lack:

- **Task delegation**: The `task` tool lets a primary agent spawn subagents with isolated context and specific instructions
- **MCP integration**: Model Context Protocol servers extend any agent with external capabilities — web search, database queries, API calls
- **Context injection**: `@file` references load domain knowledge directly into agent prompts
- **Permission system**: Fine-grained tool access control prevents subagents from exceeding their scope
- **Session hierarchy**: Parent-child session management lets you navigate between orchestrator and subagent work

According to Anthropic's documentation, Claude Code supports custom agents defined in `.opencode/agents/` (or `.claude/agents/`) with configurable models, permissions, and system prompts. This means you can define a researcher agent that only has `websearch` and `webfetch` access, while a writer agent only has `read` and `edit` access.

## The 3-Layer Architecture

Every agentic OS follows the same structural pattern:

```
User Input → Slash Command → Context Injection → Agent Execution → Output
```

### Layer 1: Commands (Entry Points)

Commands are the user interface. They live in `.opencode/commands/` and define:

- Which agent executes the task
- What context files to load
- The prompt template with `$ARGUMENTS` for dynamic input

```markdown
---
name: article
agent: copywriter-orchestrator
description: Write a complete technical article from scratch
---

@.opencode/context/core/quality-standards.md
@.opencode/context/writing/technical-voice.md

You are the Copywriter Orchestrator.

**Topic:** $ARGUMENTS

Write a complete technical article on this topic.
```

When a user runs `/article "MCP servers"`, OpenCode loads the command template, injects both context files, replaces `$ARGUMENTS` with "MCP servers", and routes everything to the orchestrator agent.

### Layer 2: Context (Domain Knowledge)

Context files are the system's memory. They live in `.opencode/context/` and contain:

- Quality standards and scoring frameworks
- Brand voice and style guidelines
- Structural patterns and templates
- SEO rules and optimization tactics
- E-E-A-T (Experience, Expertise, Authority, Trust) signals

Each file should be focused — 50-150 lines — and contain specific patterns, not general advice. For example:

```markdown
# Technical Writing Voice & Style Guide

## Core Personality
- **Tone**: Direct, helpful, authoritative
- **Voice**: Active, confident, no hedging
- **Stance**: Pragmatic over theoretical — show, don't tell

## Writing Rules
- Lead with the answer, then explain why
- Use concrete examples over abstract descriptions
- Short paragraphs: 1-4 sentences, max 150 words
```

### Layer 3: Agents (Execution)

Agents are the workers. They live in `.opencode/agents/` and define:

- Role and mission statement
- Tool permissions (what they can and cannot do)
- Workflow process (step-by-step execution method)
- Output standards (what "good" looks like)

```markdown
---
description: Researches technical topics and sources statistics
mode: subagent
permission:
  read: allow
  websearch: allow
  webfetch: allow
---

You are a Technical Researcher specialized in gathering accurate,
current information for technical content.

## Research Process
1. IDENTIFY the key research questions
2. SEARCH using web search for current results
3. GATHER detailed information from credible sources
4. ANALYZE findings for relevance and recency
5. SYNTHESIZE into structured insights
6. CITE all sources with links and dates
```

## Building Your First Agentic OS

### Step 1: Initialize the Project Structure

Create the directory skeleton:

```bash
mkdir -p my-agent-os/.opencode/{agents,commands,context/{core,writing}}
mkdir -p my-agent-os/content/articles
cd my-agent-os
```

### Step 2: Configure MCP Servers

Create `opencode.json` at the project root to define external tool access:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "brave-search": {
      "type": "local",
      "command": ["npx", "-y", "@modelcontextprotocol/server-brave-search"],
      "enabled": true,
      "environment": {
        "BRAVE_API_KEY": "your-api-key"
      }
    }
  }
}
```

This makes Brave Search available to any agent with `websearch: allow` permission. Add more MCP servers as your workflows grow — database connectors, Git tools, API clients.

### Step 3: Define Context Files

Start with two essential context files. First, quality standards:

```bash
cat > .opencode/context/core/quality-standards.md << 'EOF'
# Quality Standards

## Pass Criteria (minimum to publish)
- Answer-first formatting in every major section
- At least 3 sourced statistics with links
- Code blocks have language tags
- FAQ section with 3-5 direct answers
- Score 75+/100 on the full scoring framework
EOF
```

Second, voice and style:

```bash
cat > .opencode/context/writing/technical-voice.md << 'EOF'
# Technical Writing Voice

## Core Rules
- Tone: Direct, helpful, authoritative
- Lead with the answer, then explain
- Short paragraphs: max 150 words
- Use second person ("you") for instructions
- Name exact tools, versions, and commands
EOF
```

### Step 4: Create the Orchestrator Agent

The orchestrator is the central coordinator. It analyzes requests, delegates to subagents, and reviews output:

```bash
cat > .opencode/agents/orchestrator.md << 'EOF'
---
description: Orchestrates multi-agent workflows
mode: all
permission:
  read: allow
  edit: allow
  task: allow
  bash: allow
  websearch: allow
  webfetch: allow
---

You are the Orchestrator — a coordinator who delegates work
to specialized subagents and reviews output against quality standards.

## Workflow
1. ANALYZE the request type
2. VALIDATE that required context files are loaded
3. DELEGATE to the appropriate subagent
4. REVIEW output against quality-standards.md
5. DELIVER the final output

## Quality Gate
Verify all items from the Pass Criteria in quality-standards.md
before delivering any content.
EOF
```

Note `mode: all` — this agent works as both a primary agent (Tab-cycling) and a subagent (invoked by commands).

### Step 5: Create Subagents

Define specialized workers with restricted tool access:

```bash
cat > .opencode/agents/researcher.md << 'EOF'
---
description: Researches topics and sources statistics
mode: subagent
permission:
  read: allow
  websearch: allow
  webfetch: allow
---

You are a Technical Researcher. Gather credible sources,
verifiable statistics, and actionable insights.

## Source Quality Rules
- Official documentation > blog posts > forums
- Recent sources (within 2 years) preferred
- Primary sources > secondary summaries
- Never fabricate statistics
EOF
```

```bash
cat > .opencode/agents/writer.md << 'EOF'
---
description: Writes technical articles following loaded patterns
mode: subagent
permission:
  read: allow
  edit: allow
---

You are a Technical Writer. Create authoritative, well-structured
technical articles following the loaded voice and pattern guidelines.

## Writing Process
1. ANALYZE topic and audience level
2. REVIEW loaded voice and pattern guidelines
3. OUTLINE with H1/H2/H3 structure
4. WRITE following answer-first approach
5. INTEGRATE sourced statistics and code examples
6. SAVE to the correct output location
EOF
```

The researcher has no `edit` permission — it can only read and search. The writer has no `websearch` permission — it writes using research provided by the orchestrator. This separation of concerns prevents scope creep.

### Step 6: Create Slash Commands

Commands tie everything together. Each one loads specific context and routes to the orchestrator:

```bash
cat > .opencode/commands/article.md << 'EOF'
---
name: article
agent: orchestrator
description: Write a complete technical article
---

@.opencode/context/core/quality-standards.md
@.opencode/context/writing/technical-voice.md

You are the Orchestrator.

**Topic:** $ARGUMENTS

Write a complete technical article. Research the topic, develop
an outline, write the full article, and save to
content/articles/YYYY-MM-DD-slug.md.

Include: Key Takeaways box, answer-first formatting, 3+ sourced
statistics, code examples, FAQ section, and proper frontmatter.
EOF
```

### Step 7: Run the System

Start Claude Code in your project directory:

```bash
cd my-agent-os
opencode
```

Then execute commands:

```
/article "How to use MCP servers with Claude Code"
```

The orchestrator receives the loaded context, researches the topic, delegates writing to the writer subagent, reviews the output, and saves the final article.

## Advanced Patterns

### Permission-Based Tool Isolation

The permission system is your primary safety mechanism. Use it to create strict boundaries between agents:

```markdown
---
description: Code reviewer — read-only analysis
mode: subagent
permission:
  read: allow
  edit: deny
  bash: deny
---
```

This agent can read files and report findings but cannot modify anything or run commands.

### Context Selection Strategy

Don't load every context file into every command. Select based on task:

| Command | Context Files Loaded |
|---------|---------------------|
| `/article` | quality + voice + patterns + seo + eeat |
| `/audit` | quality + seo + eeat |
| `/brief` | quality + patterns + seo |
| `/optimize` | quality + voice + seo + eeat |

The `audit` command doesn't need voice guidelines because it's analyzing, not writing. The `brief` command doesn't need E-E-A-T signals because it's planning, not producing final content.

### Nested Delegation

Orchestrators can delegate to subagents that themselves delegate further:

```
Orchestrator
  → Researcher (gathers sources)
    → Scout subagent (clones dependency repos for source inspection)
  → Writer (drafts article using research)
  → Reviewer (validates against quality standards)
```

OpenCode's session hierarchy lets you navigate between parent and child sessions using keyboard shortcuts — `Up` to return to parent, `Down` to enter child, `Left`/`Right` to cycle between siblings.

### Model Routing

Different agents can use different models for cost and performance optimization:

```json
{
  "agent": {
    "orchestrator": {
      "model": "anthropic/claude-sonnet-4-20250514"
    },
    "researcher": {
      "model": "anthropic/claude-haiku-4-20250514"
    },
    "writer": {
      "model": "anthropic/claude-sonnet-4-20250514"
    }
  }
}
```

Use faster, cheaper models for research and summarization. Use more capable models for writing and quality review.

## Common Pitfalls

### Context Overload

Loading too many context files into a single command dilutes the agent's focus. Keep it to 2-4 files per command. If you need more, split the workflow into multiple commands.

### Permission Creep

Giving every agent full tool access defeats the purpose of specialization. Start restrictive — deny everything, then allow only what each agent needs. The researcher doesn't need `edit`. The writer doesn't need `websearch`. The reviewer needs neither.

### Redundant Criteria

Don't duplicate quality rules across agents, commands, and context files. Define them once in a context file and reference that file everywhere else. When criteria change, you update one file, not five.

### Missing Directory Errors

When agents save output to nested paths like `content/articles/YYYY-MM-DD-slug.md`, the directory may not exist. Always include "create directory if needed" in the save step, or pre-create the structure.

## What to Build Next

Once your agentic OS is running, extend it with:

- **More subagents**: Code reviewer, documentation writer, test generator, security auditor
- **More MCP servers**: Database connectors, CMS APIs, analytics platforms, CI/CD tools
- **More commands**: `/optimize`, `/audit`, `/brief`, `/repurpose`, `/translate`
- **Quality metrics**: Track scores over time to identify which context files produce the best results

The architecture scales linearly — add agents for new capabilities, add commands for new workflows, add context files for new domains. The orchestrator pattern remains the same regardless of complexity.

## FAQ

## What is the difference between an agent and a subagent in Claude Code?

Agents are defined by their `mode` field. `primary` agents are the main assistants you cycle through with Tab. `subagent` agents are specialized workers that primary agents invoke via the Task tool, or that users trigger with `@mention`. `all` mode agents can function as both.

## How do context files get injected into agent prompts?

Use the `@` syntax in command files. When you write `@.opencode/context/core/quality-standards.md` in a command, OpenCode reads that file and includes its full content in the prompt sent to the agent.

## Can subagents invoke other subagents?

Yes. Any agent with `task: allow` permission can delegate to other subagents. This enables nested delegation chains where an orchestrator delegates to a researcher, which delegates to a scout for source inspection.

## How do I prevent an agent from modifying files?

Set `edit: deny` in the agent's permission block. This blocks `write`, `edit`, and `apply_patch` tools. Combine with `bash: deny` to create a fully read-only analysis agent.

## What MCP servers are available for Claude Code?

Any MCP server that follows the Model Context Protocol specification works with Claude Code. Popular options include Brave Search, GitHub, Slack, PostgreSQL, and filesystem servers. You can also build custom MCP servers for your specific tools and APIs.
