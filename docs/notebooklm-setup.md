# NotebookLM MCP Integration

Connects the opencode copywriting system to [Google NotebookLM](https://notebooklm.google.com) via the [`notebooklm-mcp`](https://github.com/PleasePrompto/notebooklm-skill) MCP server, enabling research queries against NotebookLM notebooks using Gemini 2.5.

## Architecture

```
opencode.json
  └── notebooklm MCP server (npx notebooklm-mcp@latest)
        └── Chrome browser (patchright)
              └── cookies loaded from state.json
                    └── authenticates with notebooklm.google.com
```

## Setup

### 1. Install Chrome

```bash
npx patchright install chrome
```

### 2. Auth: Export cookies from your local browser

On your local machine, export NotebookLM cookies as JSON using a cookie export extension (e.g., "EditThisCookie" or "Get cookies.txt"). You need the following critical cookies:

| Cookie | Domain | Purpose |
|--------|--------|---------|
| `OSID` | `notebooklm.google.com` | NotebookLM session |
| `__Secure-OSID` | `notebooklm.google.com` | NotebookLM secure session |
| `SID`/`__Secure-1PSID`/`__Secure-3PSID` | `.google.com` | Google auth |

Export all cookies (typically 20-25 entries) and transfer the JSON file to the server as `/tmp/notebooklm_cookies.json`.

### 3. Create auth state

```bash
node scripts/create-state-json.cjs /tmp/notebooklm_cookies.json
```

This converts the browser cookie export into Playwright's `state.json` format at `~/.local/share/notebooklm-mcp/browser_state/state.json`.

### 4. (First time only) Clear stale Chrome profile

The persistent profile at `~/.local/share/notebooklm-mcp/chrome_profile` can interfere with injected cookies. On first setup:

```bash
rm -rf ~/.local/share/notebooklm-mcp/chrome_profile
```

### 5. Verify auth

The MCP server's `get_health` tool will report `authenticated: True` after loading the state file.

### 6. Discover notebooks (optional)

```bash
node scripts/discover-notebooks.cjs
```

This prints all notebooks with their names and URLs.

## Usage

### Via the `notebooklm` agent

The agent wires into the copywriting workflow and provides tools for:

- `ask_question` — query a notebook with a question
- `add_notebook` / `list_notebooks` / `select_notebook` — manage notebooks
- `add_source` — ingest new sources into a notebook
- `generate_audio` / `get_audio_status` / `download_audio` — Audio Overviews

### In the copywriting workflow

1. Research phase: `notebooklm` agent is called first (before web search)
2. Fact-checking phase: sources are verified against NotebookLM notebooks
3. Rewrite phase: content is rewritten using notebook-sourced insights

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `get_health` shows `authenticated: False` | No state.json | Export cookies and run `create-state-json.cjs` |
| `get_health` shows `authenticated: True` but browser redirects to login | Stale Chrome profile | `rm -rf ~/.local/share/notebooklm-mcp/chrome_profile` and restart server |
| Cookies don't persist across restarts | expected — cookies are injected in-memory via `addCookies` | State.json is loaded on each startup; no action needed |
| `ask_question` fails with rate limit | Free account limit (50 queries/day) | Use `re_auth` to rotate accounts, or upgrade |
| Missing OSID/__Secure-OSID cookies | Export didn't include notebooklm.google.com domain | Re-export cookies with notebooklm.google.com included |

## Key Files

- `opencode.json` — MCP server configuration
- `.opencode/agents/notebooklm.md` — NotebookLM agent definition
- `scripts/create-state-json.cjs` — Converts cookie export to Playwright state.json
- `scripts/discover-notebooks.cjs` — Lists all notebooks from the dashboard
- `~/.local/share/notebooklm-mcp/browser_state/state.json` — Playwright storage state
- `~/.local/share/notebooklm-mcp/chrome_profile/` — Chrome persistent profile
