---
title: "OpenCode 2026: Complete Installation, Configuration & Usage Guide"
description: "Install OpenCode on any OS via 7 methods, connect 75+ LLM providers, configure AGENTS.md, wire up MCP servers, build custom agents, and avoid every gotcha I found testing across macOS and Linux."
date: 2026-06-01
lastUpdated: 2026-06-01
tags: [opencode, ai-coding-agent, open-source, llm, mcp, agents, terminal-tui, developer-tools]
author: Rachid Hakim
product: "Build Custom AI Coding Tools — Practical Guide (gumroad.com/rachidhakim)"
leadMagnet: "OpenCode Configuration Cheat Sheet (PDF)"
---

**Key Takeaways:**
- Seven install methods exist, but the one-liner (`curl -fsSL https://opencode.ai/install | bash`) is the fastest path on macOS/Linux. For Windows, use WSL + npm or Scoop.
- OpenCode v1.15.13 (May 2026): 168K GitHub stars, 460+ contributors, 815 releases, 7.5M+ monthly users.
- The TUI has two built-in agents (`plan` and `build`) switchable via Tab. Start every new project in `plan` mode before switching to `build`.
- AGENTS.md is the single highest-leverage configuration step. Run `/init` as soon as you open a project.
- MCP servers add ~500-5K tokens each. Configure only what you need — 3-5 focused servers is the sweet spot.
- OpenCode does NOT store your code or context data. Privacy is a design constraint, not an afterthought.
- The npm package is `opencode-ai`, not `opencode`. This is the most common install mistake.

---

# OpenCode 2026: Complete Installation, Configuration & Usage Guide

OpenCode is the open-source AI coding agent built for the terminal. With 168K+ GitHub stars, 460 contributors, and 7.5 million monthly users as of May 2026, it has become the default AI coding assistant for developers who want to work in their terminal without leaving their editor or switching to a separate chat UI.

Unlike Claude Code (Anthropic's proprietary offering) or Cursor (a fork of VS Code with AI baked in), OpenCode is:
- **Provider-agnostic** — supports 75+ LLM providers including OpenAI, Google Gemini, Anthropic, Ollama, OpenCode Zen, and DeepSeek
- **Terminal-native** — runs as a TUI or CLI, not an IDE fork
- **Open source** — MIT license, inspectable, forkable, self-hostable
- **Privacy-first** — by design, OpenCode stores no code or context data on its servers

This guide covers the full setup from fresh install to production configuration, tested across macOS 15 and Ubuntu 24.04 LTS.

> **Tested on:** macOS 15 (Apple Silicon) and Ubuntu 24.04 LTS (x86_64). OpenCode v1.15.13. All commands verified May 30, 2026.

---

## 1. System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| **OS** | macOS 12+, Linux, Windows (WSL preferred) | macOS 14+ or Ubuntu 22.04+ |
| **Node.js** (npm install) | 18+ | 22+ |
| **Go** (go install) | 1.22+ | 1.23+ |
| **Docker** (Docker install) | Engine 20+ | Engine 24+ |
| **Terminal** | True color + Unicode | Ghostty, Alacritty, Kitty, iTerm2, WezTerm |
| **Disk space** | 200MB | 500MB (with MCP servers) |

**Terminal compatibility note:** The default macOS Terminal.app has known rendering issues with the TUI. If you're on macOS, use iTerm2, Ghostty, Alacritty, or WezTerm for the best experience.

---

## 2. Installation — 7 Methods, Ranked

OpenCode ships as a compiled binary (via the install script) or as an npm package. The install script is recommended for most users because it bundles the runtime and requires no dependency management.

### Method 1: Install Script (Recommended — macOS/Linux)

```bash
curl -fsSL https://opencode.ai/install | bash
```

This script downloads the precompiled binary matching your OS and architecture, places it in your PATH, and handles permissions. It does NOT require Node.js, Go, or any package manager.

**Custom install directory:**

```bash
OPENCODE_INSTALL_DIR=/usr/local/bin curl -fsSL https://opencode.ai/install | bash
XDG_BIN_DIR=$HOME/.local/bin curl -fsSL https://opencode.ai/install | bash
```

The script checks directories in this priority:
1. `$OPENCODE_INSTALL_DIR`
2. `$XDG_BIN_DIR`
3. `$HOME/bin` (if it exists or can be created)
4. `$HOME/.opencode/bin` (default fallback)

### Method 2: npm (Node.js Users)

```bash
npm install -g opencode-ai@latest
# or with alternative package managers
bun add -g opencode-ai
pnpm add -g opencode-ai
yarn global add opencode-ai
```

**⚠️ Common pitfall:** The npm package is `opencode-ai`, not `opencode`. `npm install -g opencode` installs a completely different package. I made this mistake on my first install.

If you see permission errors, configure npm's global prefix:

```bash
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.zshrc  # or ~/.bashrc
source ~/.zshrc
```

### Method 3: Homebrew (macOS/Linux — Always Up-to-Date)

Two Homebrew options exist:

```bash
# Recommended: Official tap (always latest)
brew install anomalyco/tap/opencode

# Alternative: Homebrew core formula (updated less frequently)
brew install opencode
```

The `anomalyco/tap/opencode` tap is maintained by the OpenCode team and ships releases within hours of tagging. The core formula is maintained by the Homebrew team and can lag by 1-2 weeks.

### Method 4: Docker (Isolated / CI/CD)

```bash
docker run -it --rm \
  -v "$(pwd)":/workspace \
  -w /workspace \
  -e OPENAI_API_KEY="$OPENAI_API_KEY" \
  ghcr.io/anomalyco/opencode:latest
```

The `-it` flags are required for the interactive TUI. Mount your project directory so OpenCode can read and write files. Set environment variables for your LLM provider keys.

### Method 5: Go Install (From Source)

```bash
go install github.com/opencode-ai/opencode@latest
```

Ensure `$GOPATH/bin` (default: `$HOME/go/bin`) is in your PATH:

```bash
export PATH="$PATH:$(go env GOPATH)/bin"
```

This method compiles from source and gives you the raw binary. Useful if you want to verify the build or apply patches.

### Method 6: Scoop/Chocolatey (Windows)

```bash
# Scoop
scoop install opencode

# Chocolatey
choco install opencode
```

For Windows, WSL is strongly recommended over native Windows. The TUI has path and shell compatibility issues on Windows without WSL.

### Method 7: Arch Linux (AUR)

```bash
sudo pacman -S opencode           # Stable
paru -S opencode-bin              # Latest from AUR
```

### Verification

```bash
opencode --version
# Expected: 1.15.13 or later
opencode --help
# Shows available commands
```

---

## 3. First Launch & Provider Setup

### Step 1: Start the TUI

```bash
cd your-project
opencode
```

On first launch, OpenCode opens its Terminal User Interface (TUI) and displays a startup screen prompting you to connect a provider.

### Step 2: Connect a Provider

**Option A: Interactive `/connect` command (Recommended for first time)**

Inside the TUI, type:

```
/connect
```

This opens an interactive provider picker. Select from:
- **OpenCode** (recommended — curated Zen models optimized for coding, no API key needed)
- **Anthropic** (Claude Sonnet 4.6, Opus 4.6)
- **OpenAI** (GPT-5.4, o3)
- **Google Gemini** (Gemini 2.5 Pro, Flash)
- **Ollama** (local models)
- **DeepSeek**, **Mistral**, **Groq**, and 70+ more

**Option B: Environment variables (For automation)**

```bash
# OpenCode Zen (recommended — minimal setup)
# No env var needed — uses opencode.ai/auth

# OpenAI
export OPENAI_API_KEY="sk-your-key-here"

# Google Gemini
export GOOGLE_API_KEY="your-google-api-key"

# Anthropic (limited access for third-party tools as of Jan 2026)
export ANTHROPIC_API_KEY="sk-ant-your-key-here"

# DeepSeek
export DEEPSEEK_API_KEY="your-deepseek-key"
```

**Option C: CLI auth login**

```bash
opencode auth login
```

This opens your browser for OAuth-based provider authentication. Credentials are stored at `~/.local/share/opencode/auth.json`.

### Step 3: Configure Default Model

Set your preferred model in `~/.config/opencode/opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "providers": {
    "openai": {
      "models": ["gpt-5.4"]
    }
  }
}
```

Or use the OpenCode Zen models (curated by the OpenCode team):

```json
{
  "providers": {
    "opencode": {
      "model": "zen-v2"
    }
  }
}
```

### Step 4: Run `/init` (Highest Leverage Step)

Before doing anything else, run:

```
/init
```

This tells OpenCode to scan your project files, analyze the codebase, and create or update `AGENTS.md` — a markdown file that serves as the project's persistent context for every future session.

**Example AGENTS.md** (auto-generated by `/init`):

```markdown
# Project: My App

## Tech Stack
- Frontend: React 19, TypeScript, Vite
- Backend: Node.js 24, Express, PostgreSQL
- Testing: Vitest, Playwright
- CI/CD: GitHub Actions

## Commands
- Build: `npm run build`
- Test: `npm run test`
- Dev: `npm run dev`
- Lint: `npm run lint`

## Conventions
- Use functional components with hooks
- Import order: React → third-party → local
- Test files co-located with source files
```

Commit this file to Git. It reduces repeated prompt boilerplate, makes agent behavior consistent across sessions, and is the single highest-leverage configuration step in the entire OpenCode workflow.

---

## 4. The Two Built-In Agents: Plan vs Build

OpenCode ships with two agents switchable via the `Tab` key in the TUI:

| Agent | Mode | File Access | Bash | Best For |
|-------|------|-------------|------|----------|
| **plan** | Analysis | Read-only (denies edits by default) | Ask permission | Code exploration, architecture review, planning |
| **build** | Development | Full access | Allowed | Implementation, refactoring, debugging |

### Why Start in Plan Mode

For every new project or unfamiliar codebase, start with `plan`. Ask questions like:

```
Summarize this repository's architecture.
What are the main entry points?
Point out the build and deployment pipeline.
Do not edit anything yet.
```

The `plan` agent cannot write files or run destructive commands — it explores. Switch to `build` only after the codebase map in the agent's response matches your understanding.

### The General Subagent

There's a hidden third agent called `general`, used internally for complex multi-step searches. Invoke it with:

```
@general [your complex task]
```

Use this when a single agent turn won't suffice — for example, refactoring a function across multiple files where each step depends on the previous output.

---

## 5. AGENTS.md: The Configuration File You Can't Skip

AGENTS.md is OpenCode's mechanism for persistent project context. Claude Code users will recognize it as the equivalent of CLAUDE.md — in fact, OpenCode supports CLAUDE.md as a fallback if no AGENTS.md exists.

### File Hierarchy

OpenCode loads rule files in this priority:

1. **Project AGENTS.md** — `./AGENTS.md` (traverses up to git root)
2. **Project CLAUDE.md** — `./CLAUDE.md` (fallback if no AGENTS.md)
3. **Global AGENTS.md** — `~/.config/opencode/AGENTS.md`
4. **Global CLAUDE.md** — `~/.claude/CLAUDE.md` (fallback)

Both project and global files are loaded (they compose, not override). Use the global file for personal preferences (tool preferences, communication style) and the project file for team conventions.

### Referencing Additional Files

For larger projects, keep AGENTS.md concise and reference detailed guidelines via `opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": [
    "CONTRIBUTING.md",
    "docs/development-standards.md",
    "packages/*/AGENTS.md"
  ]
}
```

Glob patterns in `instructions` let you maintain modular rule files per package or concern — especially useful in monorepos.

### Disabling Claude Code Compatibility

If you work in a mixed team where some members use Claude Code and others use OpenCode, you may want to keep both CLAs and AGENTS.md files. If you exclusively use OpenCode, disable the fallback loading:

```bash
export OPENCODE_DISABLE_CLAUDE_CODE=1
```

---

## 6. MCP Server Configuration

The Model Context Protocol lets OpenCode connect to external tools — databases, APIs, CI systems — as if they were built-in tools. MCP servers are configured in `opencode.json`.

### Local MCP Server Example

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "github": {
      "type": "local",
      "command": ["npx", "-y", "@modelcontextprotocol/server-github"],
      "enabled": true,
      "environment": {
        "GITHUB_TOKEN": "{env:GITHUB_TOKEN}"
      }
    },
    "filesystem": {
      "type": "local",
      "command": ["npx", "-y", "@modelcontextprotocol/server-filesystem", "."],
      "timeout": 5000
    }
  }
}
```

### Remote MCP Server Example

```json
{
  "mcp": {
    "sentry": {
      "type": "remote",
      "url": "https://mcp.sentry.dev/mcp",
      "oauth": {}
    },
    "company-tools": {
      "type": "remote",
      "url": "https://mcp.yourcompany.com/sse",
      "headers": {
        "Authorization": "Bearer {env:MCP_API_KEY}"
      }
    }
  }
}
```

### MCP Context Cost Guide

Every MCP server consumes context tokens. Use selectively:

| Server | Token Cost | Keep Enabled? |
|--------|-----------|---------------|
| GitHub | ~5K | Only when working on CI/issues |
| PostgreSQL | ~2K | Only when doing DB work |
| Filesystem | ~500 | Always (low cost, high value) |
| Playwright | ~3K | On-demand |
| Slack | ~1K | On-demand |
| Sentry | ~2K | Only when debugging errors |

**Strategy:** Disable all MCP servers globally, then enable per-agent:

```json
{
  "mcp": {
    "github": { "type": "local", "command": ["npx", "-y", "@modelcontextprotocol/server-github"] }
  },
  "tools": {
    "github_*": false
  },
  "agent": {
    "devops": {
      "tools": {
        "github_*": true
      }
    }
  }
}
```

### Variable Substitution

Use `{env:VARIABLE_NAME}` in config values instead of hardcoding secrets:

```json
{
  "environment": {
    "OPENAI_API_KEY": "{env:OPENAI_API_KEY}"
  }
}
```

---

## 7. Building Custom Agents

You can define custom agents beyond the built-in `plan` and `build`. Agents are defined in markdown files with YAML frontmatter.

### Agent File Locations

- **Global:** `~/.config/opencode/agents/review.md`
- **Per-project:** `.opencode/agents/review.md`

### Example: Code Review Agent

```markdown
---
description: Reviews code for quality, security, and performance
mode: subagent
model: openai/gpt-5.4
temperature: 0.1
permission:
  edit: deny
  bash: deny
  read: allow
  glob: allow
  grep: allow
  webSearch: deny
---

# Code Reviewer

You are a senior code reviewer. Focus on:

1. **Security** — SQL injection, XSS, auth bypasses, hardcoded secrets
2. **Performance** — N+1 queries, memory leaks, unnecessary allocations
3. **Maintainability** — Dead code, excessive complexity, missing error handling
4. **Correctness** — Off-by-one errors, race conditions, edge cases

Format each finding as:
- **Severity**: critical / major / minor
- **File**: path:line
- **Issue**: one-line description
- **Suggestion**: specific code change

Never make edits. Output only the review.
```

### Configuring Agent Permissions

Permissions control what each agent can do. This is OpenCode's security model at the agent level:

```json
{
  "agent": {
    "reviewer": {
      "permission": {
        "read": "allow",
        "edit": "deny",
        "bash": "deny",
        "webSearch": "deny"
      }
    },
    "writer": {
      "permission": {
        "read": "allow",
        "edit": "allow",
        "bash": {
          "git status": "allow",
          "git diff": "allow",
          "*": "ask"
        }
      }
    }
  }
}
```

---

## 8. Configuration File Reference

OpenCode loads configuration from multiple locations with increasing priority:

| Priority | Location | Purpose |
|----------|----------|---------|
| Lowest | Remote `.well-known/opencode` | Organizational defaults |
| | `~/.config/opencode/opencode.json` | Global user preferences |
| | `$OPENCODE_CONFIG` | Custom config file |
| | `./opencode.json` | Project-specific settings |
| | `.opencode/` directory | Agents, commands, plugins |
| | `$OPENCODE_CONFIG_CONTENT` | Runtime overrides |
| Highest | macOS managed preferences | Admin-enforced settings |

### Full Config Example

```json
{
  "$schema": "https://opencode.ai/config.json",
  "providers": {
    "opencode": { "model": "zen-v2" },
    "openai": {
      "apiKey": "{env:OPENAI_API_KEY}",
      "models": ["gpt-5.4"]
    },
    "anthropic": {
      "apiKey": "{env:ANTHROPIC_API_KEY}",
      "models": ["claude-sonnet-4-6"]
    }
  },
  "mcp": {
    "github": {
      "type": "local",
      "command": ["npx", "-y", "@modelcontextprotocol/server-github"],
      "enabled": true
    }
  },
  "agent": {
    "defaults": {
      "permission": {
        "bash": "ask",
        "edit": "ask"
      }
    }
  },
  "tools": {
    "WebSearch": true,
    "Bash": "ask",
    "Edit": "ask"
  },
  "notifications": {
    "mode": "passive"
  }
}
```

### Config Schema

The full schema is defined at [opencode.ai/config.json](https://opencode.ai/config.json). Key sections:

- **providers:** LLM provider configuration (API keys, model selection)
- **mcp:** External tool configuration via MCP
- **agent:** Per-agent permissions and settings
- **tools:** Global tool permissions
- **notifications:** Notification mode (passive, intrusive, off)
- **instructions:** Additional AGENTS.md references

---

## 9. Known Issues & Troubleshooting

### "command not found: opencode"

**Cause:** The install directory is not in your PATH.

**Fix:** Reopen your terminal, or manually add the install directory:

```bash
# If installed via script
export PATH="$HOME/.opencode/bin:$PATH"

# If installed via npm
export PATH="$(npm config get prefix)/bin:$PATH"
```

### "Cannot find module" or "opencode-ai not found"

**Cause:** You installed `opencode` instead of `opencode-ai` from npm.

**Fix:** `npm uninstall -g opencode && npm install -g opencode-ai@latest`

### TUI rendering issues

**Cause:** The terminal doesn't support true color or Unicode.

**Fix:** Switch to a modern terminal: Ghostty, Alacritty, Kitty, iTerm2, WezTerm.

### "Error: Node.js version too old"

**Cause:** npm install method requires Node.js 18+.

**Fix:** `node --version` to check. Upgrade via `nvm install 22 && nvm use 22`, or use the install script method (no Node.js required).

### "API key not found"

**Cause:** Environment variable not set or not exported.

**Fix:** `export OPENAI_API_KEY="sk-your-key"` — must be `export`ed, not just assigned. Add to `~/.zshrc` or `~/.bashrc` for persistence.

### Provider connection fails

**Cause:** Provider-specific issues:

- **Anthropic:** Restricted OpenCode access in January 2026. Use OpenCode Zen, OpenAI, or Google Gemini as alternatives.
- **OpenCode Zen:** Requires auth via `opencode.ai/auth` — run `/connect` in the TUI and follow the browser flow.

### Global AGENTS.md not loading

**Cause:** The `globalFiles()` path resolution can have issues on some systems. Verified non-bug on Windows (Bun's `xdgConfig` correctly resolves to `~/.config/`), but if you hit it:

**Fix:** Add the global file explicitly in `opencode.json`:

```json
{
  "instructions": ["~/.config/opencode/AGENTS.md"]
}
```

---

## 10. CLI Reference (Quick Commands)

```bash
# Open the TUI
opencode

# Non-interactive prompt
opencode "Refactor this function to use async/await"

# Agent management
opencode agent list
opencode agent create
opencode agent edit [agent-name]

# GitHub automation
opencode github install
opencode github run --event pull_request

# MCP management
opencode mcp auth [server-name]
opencode mcp list

# Provider authentication
opencode auth login
opencode auth logout
opencode auth status

# Utility
opencode doctor          # System diagnostics
opencode debug paths     # Show config file locations
opencode update          # Self-update (install script method)
```

---

## About the Author

**Rachid Hakim** — I'm an ERP consultant turned AI builder. I use OpenCode daily alongside Claude Code and have built this guide from real usage across macOS and Linux. Every command was verified on a clean install.

- **Products:** [Interactive HTML tools and technical guides](https://gumroad.com/rachidhakim) for devs and creators
- **Get the OpenCode Configuration Cheat Sheet:** A single-page PDF with all config snippets, agent templates, and MCP recipes from this guide — free download
- **Build Custom AI Coding Tools:** The full system for creating, configuring, and selling your own OpenCode-based toolchains
- **Follow me:** [@rachidhakim](https://x.com/rachidhakim) on X for daily AI dev workflows

---

*Installed and verified on June 1, 2026. OpenCode ships frequently — check the [changelog](https://opencode.ai/changelog) before following commands verbatim.*
