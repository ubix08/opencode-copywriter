---
title: "OpenClaw 2026: The Complete Installation & Deployment Guide — From Local to Production VPS"
description: "Install OpenClaw on macOS, Linux, or a $6 VPS. Covers the one-liner, npm, Docker, onboarding wizard, Anthropic/OpenAI config, Tailscale, systemd hardening, Docker sandbox, and every gotcha I hit so you don't have to."
date: 2026-06-01
lastUpdated: 2026-06-01
tags: [openclaw, ai-agent, personal-ai, self-hosted, vps-deployment, tailscale, docker, claude, anthropic, automation]
author: Rachid Hakim
product: "Deploy & Self-Host AI Agents — Complete VPS Guide (gumroad.com/rachidhakim)"
leadMagnet: "OpenClaw Production Deployment Checklist (PDF)"
---

**Key Takeaways:**
- OpenClaw hit 350K+ GitHub stars in 5 months — but most "guides" are news articles, not practical tutorials. This one is tested on a real VPS.
- The one-liner installer works 90% of the time on clean machines. For VPS deployments, use npm or Docker instead.
- The gateway binds to loopback by default. Keep it that way. Access via Tailscale or SSH tunnel — never expose port 18789 to the internet.
- Docker sandboxing for agent execution is the single most important security control. Enable it before connecting any messaging channel.
- Expected VPS cost: $6-12/month (DigitalOcean/Hetzner). Expected API cost: $0-20/month depending on usage.
- Three known bugs can break a fresh install. I cover the fix for each one.

---

# OpenClaw 2026: The Complete Installation & Deployment Guide

OpenClaw (formerly Moltbot, originally Clawdbot) is a self-hosted open-source personal AI agent created by Peter Steinberger. It gives an LLM direct access to your file system, browser, shell, and scheduling engine — then wraps it in a conversational interface that works through Telegram, WhatsApp, Discord, iMessage, or Slack. It reached 350,000 GitHub stars by April 2026 and became the fastest-growing open-source project in history.

But most content about OpenClaw is news coverage. "Look at how many stars!" "NVIDIA's CEO called it important!" "Here's what it does in theory."

This guide is the opposite. It's tested against a real VPS and covers:

- Four installation methods and when each one breaks
- The onboarding wizard — both interactive and non-interactive (for automation)
- Connecting Anthropic, OpenAI, DeepSeek, and Ollama models
- VPS deployment with Tailscale for zero-port-exposure access
- Production hardening: Docker sandbox, systemd security directives, DOCKER-USER iptables rules
- Every bug and gotcha I encountered on three separate install attempts

> **Tested on:** macOS 15 (Apple Silicon) and Ubuntu 24.04 LTS (x86_64) — DigitalOcean $12 droplet (2 vCPU, 2GB RAM). OpenClaw v2026.5.31. All commands verified.

---

## 1. Installation: Four Methods, Three Failure Modes

OpenClaw is a Node.js application distributed via npm. There is no Homebrew formula, no APT repo, and no standalone binary. Understanding this up front saves you the confusion I had on the first attempt.

### Method 1: One-Liner (Recommended for macOS/Linux Desktops)

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

This script:
1. Detects your OS via `uname -s`
2. Installs Homebrew on macOS if missing (prompts first)
3. Installs Node 24 via Homebrew if your Node is older than 22.14
4. Runs `npm install -g openclaw@latest`
5. Optionally runs `openclaw onboard --install-daemon`

**When this fails:**
- On Ubuntu/Debian VPS, this script fails roughly 30% of the time due to permission issues (confirmed by Sphere Inc.'s deployment testing and my own experience). If you see `EACCES` errors, use Method 2 or 3 instead.
- On shared or corporate-managed machines where you don't have sudo, use Method 4 (sandboxed install).

### Method 2: npm Global Install (Recommended for VPS and Dev Machines)

```bash
npm install -g openclaw@latest
openclaw onboard --install-daemon
```

**Common EACCES fix for macOS:**

```bash
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.zshrc
source ~/.zshrc
npm install -g openclaw@latest
```

**Common EACCES fix for Linux:**

```bash
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
npm install -g openclaw@latest
```

### Method 3: Docker (Recommended for Production VPS)

```bash
# Clone the setup repo
git clone https://github.com/openclaw/openclaw.git
cd openclaw

# Install dependencies and build
pnpm install
pnpm openclaw setup

# Run via Docker Compose
OPENCLAW_IMAGE=ghcr.io/openclaw/openclaw:latest \
pnpm openclaw gateway docker-setup

# Or use the official docker-setup script
curl -fsSL https://openclaw.ai/docker-setup.sh | bash
```

Docker is the recommended path for VPS deployments because container isolation limits blast radius if the agent process is compromised. The gateway inside the container binds to all interfaces by default (`lan` mode) — this is correct for Docker because the port mapping needs to reach the gateway inside the container. External access is blocked at the host level using DOCKER-USER iptables rules (covered in Section 5).

### Method 4: Sandboxed Install (No Sudo, No Global npm)

```bash
curl -fsSL https://openclaw.ai/install-cli.sh | bash
```

This puts everything under `~/.openclaw/` — npm package, dependencies, and a project-local Node binary. The `openclaw` command is available at `~/.local/bin/openclaw`. Update by re-running the installer rather than `npm install -g`.

### Verification

```bash
openclaw --version
# Expected: 2026.5.31 or later
```

### Known Bug #1: Missing Module Dependencies (v2026.4.20-4.21)

If you install and see `Error: Cannot find module '@larksuiteoapi/node-sdk'` or `Error: Cannot find module 'nostr-tools'`, you hit the packaged dependency bug from the 2026.4.20 / 2026.4.21 releases. Fix:

```bash
npm install -g openclaw@latest   # upgrade to latest
openclaw doctor --fix            # installs missing runtime deps
openclaw gateway restart
```

If you're stuck on an affected version and can't upgrade, a temporary workaround:

```bash
npm install -g nostr-tools @slack/web-api @whiskeysockets/baileys
```

The permanent fix shipped in 2026.4.22 with lazy/activation-time dependency loading.

---

## 2. Onboarding: The Wizard That Does Everything

After installation, run onboarding. This is not optional — `openclaw --version` succeeds without it, but nothing else works.

### Interactive (Recommended for First Setup)

```bash
openclaw onboard
```

The wizard walks through:
1. **Model provider** — choose Anthropic (API key or CLI auth), OpenAI (API or OAuth), DeepSeek, Ollama, custom, or skip
2. **Workspace** — defaults to `~/.openclaw/workspace`, seeds bootstrap files (SOUL.md, AGENTS.md, TOOLS.md, IDENTITY.md)
3. **Gateway** — port (18789), bind (loopback default), auth mode (auto-generates token)
4. **Channels** — Telegram, WhatsApp, Discord, Slack, Signal, iMessage, and more
5. **Daemon** — installs the gateway as a background service
6. **Skills** — installs recommended default skills
7. **Health check** — verifies the gateway is running

### Non-Interactive (For Automation / Repeatable Deployments)

```bash
openclaw onboard --non-interactive \
  --auth-choice anthropic-api-key \
  --anthropic-api-key "$ANTHROPIC_API_KEY" \
  --install-daemon \
  --accept-risk
```

For Ollama (local models):

```bash
openclaw onboard --non-interactive \
  --auth-choice ollama \
  --custom-base-url "http://127.0.0.1:11434" \
  --custom-model-id "qwen3.5:27b" \
  --accept-risk
```

For skipping model setup entirely (configure later):

```bash
openclaw onboard --non-interactive \
  --auth-choice skip \
  --install-daemon \
  --accept-risk
```

### Secrets Management

By default, onboarding stores API keys as plaintext in `~/.openclaw/agents/<agent-name>/agent/auth-profiles.json`. For production, use key refs instead:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
openclaw onboard --non-interactive \
  --auth-choice anthropic-api-key \
  --secret-input-mode ref \
  --accept-risk
```

This stores an environment variable reference instead of the key value. The key is read at runtime from `ANTHROPIC_API_KEY`.

### Gateway Token

Onboarding auto-generates a gateway token. You'll need this to connect the Control UI or CLI to the gateway. Retrieve it:

```bash
openclaw config get gateway.auth.token
```

If you need to set it manually (e.g., for a known value you can commit to `.env`):

```bash
openclaw config set gateway.auth.token "your-token" --strict-json
```

**Important:** Gateway changes (port, bind, auth) require a gateway restart — they don't hot-reload like most other config fields.

---

## 3. Post-Onboarding Verification

Before connecting any channels, verify the gateway is running and responsive.

### Check Gateway Status

```bash
openclaw status
# Expected: Gateway running (PID: 12345) — bound to 127.0.0.1:18789
```

### Check the Service

```bash
# Linux (systemd)
systemctl --user status openclaw-gateway.service

# macOS (launchd)
launchctl list | grep openclaw
```

### View Logs

```bash
# Linux
journalctl --user -u openclaw-gateway.service -f --since "5 minutes ago"

# macOS
log show --predicate 'process == "openclaw"' --last 5m
```

### Test With a Smoke Request

```bash
openclaw agent \
  --local \
  --session-id smoke-test \
  --message "Reply with exactly: Hello from OpenClaw" \
  --timeout 60
```

If this succeeds, OpenClaw is fully operational. If it fails with a model auth error, your API key is invalid or the model identifier is wrong.

### Run the Doctor

```bash
openclaw doctor --non-interactive
```

This checks for common configuration problems. Pay attention to:

- **Gateway auth mode** — should be set (not "none" unless loopback-only)
- **Command owner** — should be configured before connecting external channels
- **Session store** — should exist (the onboarding wizard creates it)
- **Plaintext tokens** — consider switching to secret refs for production

---

## 4. VPS Deployment — The Practical Path

Running OpenClaw on a VPS is more secure than running it on your laptop (no local attack surface), but requires careful configuration. Here's the exact path I tested on a $12/month DigitalOcean droplet.

### Specs That Actually Work

| Provider | Plan | Specs | Price/mo | Notes |
|----------|------|-------|----------|-------|
| DigitalOcean | Basic | 1 vCPU, 1GB RAM | $6 | Minimum viable, add swap |
| DigitalOcean | Basic | 2 vCPU, 2GB RAM | $12 | Comfortable for light use |
| Hetzner | CX22 | 2 vCPU, 4GB RAM | €3.79 (~$4) | Best value |
| Oracle Cloud | Always Free ARM | up to 4 OCPU, 24GB RAM | $0 | ARM-only, finicky signup |

I tested on a 2 vCPU, 2GB RAM DigitalOcean droplet with Ubuntu 24.04. The 1GB RAM option works but requires adding swap (below) — otherwise you'll hit OOM during the initial `npm install`.

**Important:** Use a separate VPS provider account from your production infrastructure. If OpenClaw triggers TOS violations (runaway API calls, outbound spam, content moderation issues), the provider may suspend your entire account. A $6 droplet is not worth risking your main infrastructure.

### Step-by-Step VPS Setup

#### 1. Provision the Droplet

```bash
# Create a DigitalOcean droplet:
# - Region: closest to you
# - Image: Ubuntu 24.04 LTS
# - Size: $12/mo (2 vCPU, 2GB RAM)
# - Authentication: SSH key
```

#### 2. Add Swap (Required for 1GB RAM Droplets)

```bash
fallocate -l 2G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab
```

Verify: `free -h` should show 2GB swap.

#### 3. Install Node.js and OpenClaw

```bash
# Update system
apt update && apt upgrade -y

# Install Node 22
curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
apt install -y nodejs

# Verify
node -v   # v22.x.x minimum, v24 preferred

# Install OpenClaw
npm install -g openclaw@latest
```

#### 4. Run Onboarding

```bash
openclaw onboard --non-interactive \
  --auth-choice anthropic-api-key \
  --anthropic-api-key "$ANTHROPIC_API_KEY" \
  --install-daemon \
  --accept-risk
```

#### 5. Verify Gateway Is Running

```bash
systemctl --user status openclaw-gateway.service
journalctl --user -u openclaw-gateway.service -n 20 --no-pager
```

The gateway should be running on `127.0.0.1:18789` — confirmed by:

```bash
ss -tulpn | grep 18789
# Expected: LISTEN 127.0.0.1:18789
```

#### 6. Configure `.openclaw` Directory Permissions

```bash
chmod 700 ~/.openclaw
```

This prevents other users on the system from reading your config, credentials, and session data.

### Accessing the Control UI

The gateway binds to loopback by default. To access the dashboard, you have three options:

#### Option A: SSH Tunnel (Simplest)

```bash
ssh -L 18789:127.0.0.1:18789 user@your-droplet-ip
```

Then open `http://127.0.0.1:18789` in your browser. Keep the SSH session open.

**Pro tip:** Add this to `~/.ssh/config` so you don't have to remember the command:

```
Host openclaw
    HostName your-droplet-ip
    User root
    LocalForward 18789 127.0.0.1:18789
```

Then: `ssh openclaw`

#### Option B: Tailscale Serve (Recommended — No Port Exposure)

```bash
# Install Tailscale on the VPS
curl -fsSL https://tailscale.com/install.sh | sh
tailscale up

# Configure Gateway to use Tailscale Serve
openclaw config set gateway.tailscale.mode serve
openclaw gateway restart
```

Then access `https://<tailscale-hostname>:18789` from any device on your tailnet. Tailscale handles TLS and identity-based authentication automatically. No ports exposed to the public internet.

#### Option C: Tailnet Bind (Alternative)

```bash
openclaw config set gateway.bind tailnet
openclaw gateway restart
```

Access at `http://<tailscale-ip>:18789` — requires gateway token for auth.

---

## 5. Production Hardening

If you're connecting OpenClaw to messaging channels or leaving it running on a VPS, these hardening steps are not optional.

### 5.1 Enable Docker Sandboxing

This is the single most important security control. When enabled, every agent tool execution (shell commands, file writes) runs inside a disposable Docker container — not on your host.

**Install Docker (if not already):**

```bash
curl -fsSL https://get.docker.com | sh
usermod -aG docker $USER
# Log out and back in for group change to take effect
```

**Add sandbox config to `~/.openclaw/openclaw.json`:**

```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "all",
        "docker": {
          "network": "none",
          "readOnlyRoot": true,
          "capDrop": ["ALL"],
          "pidsLimit": 100,
          "memory": "512m"
        }
      }
    }
  }
}
```

| Setting | What it does |
|---------|-------------|
| `mode: "all"` | Every agent session runs in a sandbox |
| `network: "none"` | Sandbox containers have no network access |
| `readOnlyRoot: true` | Root filesystem is read-only inside the sandbox |
| `capDrop: ["ALL"]` | Drops all Linux capabilities inside the container |
| `pidsLimit: 100` | Prevents fork bombs |
| `memory: "512m"` | Hard memory limit per agent session |

**Verify sandboxing is active:**

```bash
openclaw doctor --non-interactive | grep sandbox
# Expected: sandbox: enabled (mode: all, docker)
```

### 5.2 Fix the Docker-UFW Bypass

By design, Docker manipulates iptables directly, bypassing UFW entirely. If you run OpenClaw with Docker and publish port 18789, that port is accessible from the internet even if UFW blocks it.

**The fix — DOCKER-USER iptables rules:**

```bash
# Block all external traffic to Docker containers
iptables -I DOCKER-USER -i eth0 -j DROP

# Allow loopback traffic (so localhost can reach Docker containers)
iptables -I DOCKER-USER -i lo -j RETURN

# Make rules persistent
apt install -y iptables-persistent
netfilter-persistent save
```

Verify:

```bash
iptables -L DOCKER-USER -n -v
# Expected: DROP on eth0, RETURN on lo
```

### 5.3 Configure a Command Owner

Without a command owner, *anyone* who can message your OpenClaw on a connected channel can run privileged commands. Before connecting Telegram or WhatsApp:

```bash
openclaw config set agents.defaults.commandOwner "your-phone-number-or-username" --strict-json
```

For Telegram, this is your Telegram username. For WhatsApp, your phone number (with country code).

### 5.4 Hardened systemd Service

If you installed via npm and `--install-daemon`, OpenClaw already has a systemd user service. But the defaults are not hardened. Create or edit:

```bash
sudo mkdir -p /etc/systemd/system/
sudo tee /etc/systemd/system/openclaw-gateway.service << 'EOF'
[Unit]
Description=OpenClaw Gateway
After=network-online.target docker.service
Wants=network-online.target
Requires=docker.service

[Service]
Type=simple
User=openclaw
Group=openclaw
ExecStart=/usr/bin/openclaw gateway run
Restart=always
RestartSec=10

# Security hardening
NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=/home/openclaw/.openclaw
CapabilityBoundingSet=
ProtectKernelTunables=yes
ProtectKernelModules=yes
ProtectControlGroups=yes
RestrictSUIDSGID=yes
MemoryMax=2G

[Install]
WantedBy=multi-user.target
EOF
```

Apply and verify:

```bash
sudo systemctl daemon-reload
sudo systemctl enable openclaw-gateway.service
sudo systemctl start openclaw-gateway.service

# Check systemd security score (lower is more secure)
sudo systemd-analyze security openclaw-gateway.service
# Expected: ~5.0-5.5 (default is ~9.6)
```

### 5.5 Baseline Security Checklist

- [ ] SSH password authentication disabled: `PasswordAuthentication no` in `/etc/ssh/sshd_config`
- [ ] SSH root login disabled: `PermitRootLogin no`
- [ ] UFW default deny: `ufw default deny incoming`
- [ ] UFW allow only SSH (and HTTP/HTTPS if using reverse proxy): `ufw allow 22/tcp`
- [ ] Fail2ban installed: `apt install -y fail2ban`
- [ ] Unattended upgrades enabled: `dpkg-reconfigure --priority=low unattended-upgrades`
- [ ] mDNS/Bonjour disabled: `export OPENCLAW_DISABLE_BONJOUR=1` in service environment
- [ ] Gateway token stored as env var, not in config file: use `${OPENCLAW_GATEWAY_TOKEN}` in config
- [ ] `.openclaw` directory permissions: `chmod 700 ~/.openclaw`

---

## 6. Connecting LLM Providers

### Anthropic (Recommended)

```bash
# Option A: API key
openclaw onboard --non-interactive \
  --auth-choice anthropic-api-key \
  --anthropic-api-key "$ANTHROPIC_API_KEY"

# Option B: Claude CLI auth (reuses your Claude subscription)
openclaw models auth login --provider anthropic --method cli --set-default

# Option C: Setup token (from Claude Code CLI)
openclaw models auth setup-token --provider anthropic
```

Model refs:
- `anthropic/claude-opus-4-6` — best quality
- `anthropic/claude-sonnet-4-6` — best balance (recommended)
- `claude-cli/claude-sonnet-4-6` — via Claude CLI auth

### OpenAI

```bash
# API key
openclaw onboard --non-interactive \
  --auth-choice openai-api-key \
  --openai-api-key "$OPENAI_API_KEY"

# OAuth (reuses ChatGPT subscription)
openclaw onboard --non-interactive \
  --auth-choice openai-codex-oauth
```

Model refs: `openai/gpt-5.4`, `openai/gpt-5.5`

### DeepSeek (Cheapest for Testing)

```bash
openclaw onboard --non-interactive \
  --auth-choice deepseek-api-key \
  --deepseek-api-key "$DEEPSEEK_API_KEY"
```

Model refs: `deepseek/deepseek-v4-flash`

### Ollama (Local, Free)

```bash
openclaw onboard --non-interactive \
  --auth-choice ollama \
  --custom-base-url "http://127.0.0.1:11434" \
  --custom-model-id "llama3.3:70b"
```

### Setting the Default Model

```bash
openclaw config set agents.defaults.model.primary "anthropic/claude-sonnet-4-6" --strict-json
```

---

## 7. Connecting Messaging Channels

Each channel requires a bot token or credentials from the platform.

### Telegram (Easiest)

1. Create a bot via [@BotFather](https://t.me/BotFather) on Telegram
2. Copy the bot token
3. Configure:

```bash
openclaw config set channels.telegram.botToken "your-bot-token" --strict-json
openclaw gateway restart
```

### WhatsApp (Requires Persistent Connection)

WhatsApp uses the Baileys library, which requires a persistent WebSocket connection to WhatsApp's servers. This means:

- The gateway must stay running 24/7 (it will, since it's a daemon)
- The VPS must allow outbound WebSocket connections (most do by default)
- You'll scan a QR code during first-time pairing

### Discord

1. Create a Discord application at https://discord.com/developers
2. Create a bot, copy the token
3. Configure:

```bash
openclaw config set channels.discord.token "your-discord-token" --strict-json
```

---

## 8. Troubleshooting: The Problems I Actually Hit

### "Error: Cannot find module '@larksuiteoapi/node-sdk'"

**Root cause:** Packaged dependency bug in v2026.4.20-4.21. The npm package ships bundled plugin directories (feishu, nostr, slack, telegram, whatsapp) but doesn't declare their runtime dependencies in the root `package.json`.

**Fix:** `npm install -g openclaw@latest && openclaw doctor --fix && openclaw gateway restart`

### "Gateway start blocked: set gateway.mode=local"

**Root cause:** After a fresh install, the config file exists but `gateway.mode` is not set. The gateway refuses to start without an explicit mode.

**Fix:** `openclaw config set gateway.mode local --strict-json` or re-run `openclaw onboard`

### "Refusing to bind gateway ... without auth"

**Root cause:** You changed `gateway.bind` from `loopback` to `lan` or `tailnet` without configuring auth.

**Fix:** Set a gateway token first: `openclaw config set gateway.auth.mode token --strict-json` and `openclaw config set gateway.auth.token "your-token" --strict-json`

### "Another gateway instance is already listening"

**Root cause:** Port 18789 is already in use — either another OpenClaw process or a different service.

**Fix:** `ss -tulpn | grep 18789` to find the process, then `kill <PID>` or change the port with `openclaw config set gateway.port 18790`

### Gateway accessible from public IP (Docker deploy)

**Root cause:** Docker's port mapping bypasses UFW. The gateway inside the container binds to `0.0.0.0` and Docker publishes the port on all host interfaces.

**Fix:** Add DOCKER-USER iptables rules (see Section 5.2). Verify with `iptables -L DOCKER-USER -n -v`.

### OAuth token refresh failed (Claude subscription)

**Root cause:** Claude CLI auth tokens can expire. This happens intermittently.

**Fix:** Re-run `openclaw models auth setup-token --provider anthropic` on the gateway host. If the Claude CLI lives on a different machine, use `openclaw models auth paste-token --provider anthropic`.

### Out of memory on 1GB droplet

**Root cause:** Node.js + OpenClaw gateway + Docker sandbox can exceed 1GB RAM under load. Many guides recommend a $6 droplet but omit this limitation.

**Fix:** Add swap (Section 4, Step 2). Set `MemoryMax=1G` in the systemd unit. Use API-based models instead of local models. Or upgrade to a 2GB droplet ($12/month).

---

## 9. Production Deployment Checklist (Free Download)

This article covers the critical path, but a production deployment has more edge cases: TLS termination, backup strategy, log rotation, monitoring, alerting, and update procedures.

I've compiled a **Production Deployment Checklist** — a single-page PDF with all 47 check items organized by phase (Pre-Deploy, Install, Harden, Connect, Monitor). It includes the exact `ssh config`, `systemd unit`, `iptables rules`, and `openclaw.json` snippets from this guide.

[Download the Production Deployment Checklist (Free — No Email Required)](https://gumroad.com/rachidhakim)

If you want the full deployment playbook with production-tested nginx configs, Docker Compose overlays, logrotate configs, Prometheus metrics setup, and Terraform templates for repeatable deployments across DO/Hetzner/Oracle, check out:

[Deploy & Self-Host AI Agents — Complete VPS Guide ($15)](https://gumroad.com/rachidhakim)

---

*Installed and verified on June 1, 2026. OpenClaw releases ship approximately every 2 days — check the [release notes](https://github.com/openclaw/openclaw/releases) before following any command in this guide verbatim.*
