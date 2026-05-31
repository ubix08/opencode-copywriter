AUTONOMOUS INFO-PRODUCT BUILDER SYSTEM v4.0

Complete Technical Implementation with Optimal Problem-Solving Frameworks

---

TABLE OF CONTENTS

1. [System Architecture Overview](#1-system-architecture-overview)
2. [Phase 0: Intelligence Infrastructure](#2-phase-0-intelligence-infrastructure)
3. [Phase 1: Daily Pipeline Execution](#3-phase-1-daily-pipeline-execution)
4. [Phase 2: Validation & Decision Engine](#4-phase-2-validation--decision-engine)
5. [Phase 3: Research & Problem Deconstruction](#5-phase-3-research--problem-deconstruction)
6. [Phase 4: The OPTIMAL Writing Framework](#6-phase-4-the-optimal-writing-framework)
7. [Phase 5: Quality Assurance & Humanization](#7-phase-5-quality-assurance--humanization)
8. [Phase 6: Publication & Monetization](#8-phase-6-publication--monetization)
9. [Technical Implementation: File Structure & APIs](#9-technical-implementation-file-structure--apis)
10. [Reverse Engineering Toolkit](#10-reverse-engineering-toolkit)
11. [Daily Operation Runbook](#11-daily-operation-runbook)

---

1. SYSTEM ARCHITECTURE OVERVIEW

The 7-Phase Continuous Loop

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PHASE 0: INTELLIGENCE INFRASTRUCTURE                 │
│    Setup once: Ollama embeddings, database, API keys, scheduler              │
└─────────────────────────────────────────────────────────────────────────────┘
                                      ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│    PHASE 1: DAILY PIPELINE EXECUTION (Automated, 06:00 UTC)                  │
│    Reddit → X/Twitter → Marketplaces → News → Trends → Unified JSON Report   │
└─────────────────────────────────────────────────────────────────────────────┘
                                      ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│    PHASE 2: VALIDATION & DECISION (Coordinator/Ubix)                         │
│    10-Point Scorecard → GO/NO-GO/CONDITIONAL → Queue or Reject               │
└─────────────────────────────────────────────────────────────────────────────┘
                                      ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│    PHASE 3: RESEARCH & PROBLEM DECONSTRUCTION (Researcher Agent)             │
│    5+ Verbatim Quotes → Root Cause → Key Insight → Writer Brief              │
└─────────────────────────────────────────────────────────────────────────────┘
                                      ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│    PHASE 4: THE OPTIMAL WRITING FRAMEWORK (Writer Agent)                     │
│    7-Section Structure → Copy-Pasteable Commands → Practitioner Voice        │
└─────────────────────────────────────────────────────────────────────────────┘
                                      ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│    PHASE 5: QUALITY ASSURANCE & HUMANIZATION (Editor Agent)                  │
│    Anti-Slop Checklist → AI Humanizer → Verification Tests                   │
└─────────────────────────────────────────────────────────────────────────────┘
                                      ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│    PHASE 6: PUBLICATION & MONETIZATION (Publisher Agent)                     │
│    PDF Generation → Cover Design → Multi-Marketplace Listing → Social Copy   │
└─────────────────────────────────────────────────────────────────────────────┘
                                      ↓
                              [COMPOUND TO KB.MD]
                                      ↓
                           [RETURN TO PHASE 1]
```

---

2. PHASE 0: INTELLIGENCE INFRASTRUCTURE

2.1 Hardware & Software Requirements

Component	Specification	Purpose	
Compute	4-core CPU, 8GB RAM minimum	Ollama embeddings, pipeline execution	
Storage	50GB SSD	Database, PDFs, cover images	
OS	Ubuntu 22.04 LTS / macOS 14+ / Termux (Android)	Primary deployment	
Python	3.10+	Pipeline scripts, API clients	
Node.js	18+	Optional web dashboard	
Ollama	Latest	Local embeddings (Qwen3:0.6b)	

2.2 Ollama Embedding Layer Configuration

```bash
# Installation
curl -fsSL https://ollama.com/install.sh | sh

# Pull optimized embedding model (MRL-capable)
ollama pull qwen3:0.6b

# Verify
ollama run qwen3:0.6b "Test embedding generation"
```

Embedding Engine Class (`/app/embedding_engine.py`):

```python
import requests
import numpy as np
from typing import List, Dict, Optional
import asyncio
import aiohttp

class OllamaQwen3MRL:
    """
    Production-grade Qwen3-0.6B embeddings via Ollama with MRL support.
    Multi-Representation Learning: truncate to 32/256/512/1024 dims as needed.
    """
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "qwen3:0.6b"):
        self.base_url = base_url
        self.model = model
        self.base_dim = 1024
        
        # MRL dimension configurations for different pipeline stages
        self.dim_configs = {
            "ultra_fast": 32,      # Initial spam/triage filtering
            "clustering": 256,     # HDBSCAN input (primary use)
            "search": 512,         # Semantic similarity
            "precision": 1024,     # Final verification
            "full": 1024           # Maximum quality
        }
        
        self._health_check()
    
    def _health_check(self):
        """Verify Ollama server and model availability."""
        try:
            resp = requests.post(
                f"{self.base_url}/api/show",
                json={"name": self.model},
                timeout=5
            )
            if resp.status_code != 200:
                raise ConnectionError(f"Model {self.model} not found")
            print(f"✓ Ollama ready with {self.model}")
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Ollama not running. Start with: ollama serve")
    
    def embed(self, texts: List[str], purpose: str = "clustering", 
              normalize: bool = True, instruction: Optional[str] = None) -> np.ndarray:
        """
        Generate embeddings with MRL dimension truncation.
        
        Args:
            texts: List of texts to embed
            purpose: ultra_fast|clustering|search|precision|full
            normalize: L2 normalize for cosine similarity
            instruction: Optional task-specific instruction
        """
        target_dim = self.dim_configs.get(purpose, 256)
        
        # Format with instruction if provided (Qwen3 supports this)
        if instruction:
            texts = [f"Instruct: {instruction}\nQuery: {t}" for t in texts]
        
        # Ollama batch embedding
        response = requests.post(
            f"{self.base_url}/api/embed",
            json={
                "model": self.model,
                "input": texts,
                "options": {
                    "temperature": 0,
                    "num_ctx": 32000,
                }
            },
            timeout=60
        )
        
        if response.status_code != 200:
            raise Exception(f"Ollama error: {response.text}")
        
        embeddings = np.array(response.json()["embeddings"])
        
        # MRL: Truncate to target dimension
        if target_dim < self.base_dim:
            embeddings = embeddings[:, :target_dim]
        
        # L2 normalization
        if normalize:
            norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
            embeddings = embeddings / np.maximum(norms, 1e-12)
        
        return embeddings
    
    def embed_reddit_post(self, post: Dict, purpose: str = "clustering") -> np.ndarray:
        """
        Domain-optimized embedding for Reddit pain-point extraction.
        """
        instructions = {
            "clustering": (
                "Represent this Reddit post for clustering by: "
                "1) Tool mentioned, 2) Specific failure mode, "
                "3) User maturity stage, 4) Emotional intensity"
            ),
            "search": "Represent this post for semantic search of similar tool pain points",
            "classification": "Classify this post's intent: pain point, solution seeking, or neutral"
        }
        
        instruction = instructions.get(purpose, instructions["clustering"])
        
        title = post.get('title', '')
        body = post.get('selftext', post.get('body', ''))[:2500]
        subreddit = post.get('subreddit', '')
        
        text = f"Subreddit: {subreddit}\nTitle: {title}\nContent: {body}"
        
        return self.embed([text], purpose=purpose, instruction=instruction)[0]
```

2.3 Database Schema (sqlite-vec)

```sql
-- /app/schema.sql
-- Run: sqlite3 painpoints.db < schema.sql

-- Enable vector extension
.load ./vec0

-- Raw posts from all sources
CREATE TABLE posts (
    id TEXT PRIMARY KEY,
    source TEXT,              -- reddit, twitter, marketplace, news
    subreddit_or_channel TEXT,
    title TEXT,
    body TEXT,
    author TEXT,
    upvotes INTEGER,
    comments_count INTEGER,
    created_at TIMESTAMP,
    scraped_at TIMESTAMP,
    embedding_256 BLOB,       -- MRL truncated for clustering
    category TEXT,            -- pain_point, opportunity, neutral, competitor
    sentiment_score REAL,
    willingness_to_pay_signals TEXT, -- JSON array
    url TEXT
);

-- Virtual table for vector similarity search
CREATE VIRTUAL TABLE vec_posts USING vec0(
    post_id TEXT,
    embedding FLOAT[256]
);

-- Clustered problems (temporal tracking)
CREATE TABLE clusters (
    cluster_id TEXT PRIMARY KEY,
    date DATE,
    parent_cluster_id TEXT,
    stability_score REAL,
    size INTEGER,
    avg_upvotes REAL,
    label TEXT,
    workflow_stage TEXT,      -- ideation, drafting, editing, publishing, distribution
    emotional_profile TEXT,   -- JSON array: frustrated, guilty, overwhelmed, etc.
    pain_maturity TEXT,       -- awareness, consideration, decision, post_purchase
    monetization_angle TEXT,  -- template, checklist, video_course, SaaS, etc.
    opportunity_score REAL,
    status TEXT               -- new, growing, stable, declining
);

-- Deep insights for high-value clusters
CREATE TABLE insights (
    insight_id INTEGER PRIMARY KEY,
    cluster_id TEXT,
    post_id TEXT,
    date DATE,
    problem_validated BOOLEAN,
    pain_intensity TEXT,      -- annoyance, friction, crisis
    workaround_cost_time TEXT,
    workaround_cost_money TEXT,
    willingness_to_pay_signals TEXT, -- JSON
    solution_requirements TEXT,      -- JSON: must_have, nice_to_have
    competitive_landscape TEXT,      -- JSON: tools_using, why_insufficient
    recommended_format TEXT,
    price_suggestion TEXT,
    confidence REAL,
    urgency TEXT              -- immediate, this_month, quarter
);

-- Knowledge Base accumulation
CREATE TABLE kb_accumulated (
    entry_id INTEGER PRIMARY KEY,
    entry_type TEXT,          -- confirmed_winner, promising_problem, rejected_problem, vocabulary, tool
    content TEXT,
    metadata TEXT,            -- JSON: date, source, revenue, etc.
    date_added DATE
);
```

2.4 Free-Tier LLM Router Configuration

```python
# /app/llm_router.py
import asyncio
import aiohttp
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import random

class FreeTierLLMRouter:
    """
    Intelligent routing across free tier providers with quota management.
    SambaNova: 6,000 RPD (classification, batch)
    Z.AI: 2,000 RPD (JSON validation, repair)
    Gemini: 500 RPD (cluster labeling, deep insights)
    Mistral: 1B tokens/month (emergency fallback)
    """
    
    def __init__(self):
        self.quotas = {
            "sambanova": {"rpm": 30, "rpd": 6000, "used_today": 0, "last_call": 0},
            "zai": {"rpm": 60, "rpd": 2000, "used_today": 0, "last_call": 0},
            "gemini": {"rpm": 15, "rpd": 500, "used_today": 0, "last_call": 0},
            "mistral": {"rpm": 2, "monthly_tokens": 1_000_000_000, "used_today": 0}
        }
        
        self.api_keys = {
            "sambanova": os.getenv("SAMBANOVA_API_KEY"),
            "zai": os.getenv("ZAI_API_KEY"),
            "gemini": os.getenv("GOOGLE_API_KEY"),
            "mistral": os.getenv("MISTRAL_API_KEY")
        }
        
        self.quality_scores = {
            "sambanova": 0.87,
            "zai": 0.82,
            "gemini": 0.92,
            "mistral": 0.84
        }
    
    async def call_gemini(self, prompt: str, temperature: float = 0.1, 
                         response_mime_type: str = "application/json") -> Dict:
        """Google Gemini 3.1 Flash Lite - reserved for high-value tasks."""
        import google.generativeai as genai
        genai.configure(api_key=self.api_keys["gemini"])
        
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        
        result = await model.generate_content_async(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
                response_mime_type=response_mime_type
            )
        )
        
        self.quotas["gemini"]["used_today"] += 1
        return {"content": result.text, "provider": "gemini", "quality_score": 0.92}
    
    async def call_sambanova(self, prompt: str, temperature: float = 0.1) -> Dict:
        """SambaNova Qwen3-32B - high-volume classification."""
        headers = {"Authorization": f"Bearer {self.api_keys['sambanova']}"}
        payload = {
            "model": "Qwen3-32B",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": 2000
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.sambanova.ai/v1/chat/completions",
                headers=headers,
                json=payload
            ) as resp:
                data = await resp.json()
                self.quotas["sambanova"]["used_today"] += 1
                return {
                    "content": data["choices"][0]["message"]["content"],
                    "provider": "sambanova",
                    "quality_score": 0.87
                }
```

---

3. PHASE 1: DAILY PIPELINE EXECUTION

3.1 Reddit Pipeline (`/pipelines/reddit_pipeline.py`)

```python
import praw
import asyncpraw
from datetime import datetime, timedelta
import json
import asyncio

class RedditPainPointPipeline:
    """
    Daily Reddit mining for practitioner pain points.
    Uses PRAW with adaptive rate limiting.
    """
    
    TARGET_SUBREDDITS = [
        "AI_Agents", "ChatGPT", "Midjourney", "solopreneurs",
        "marketing", "copywriting", "startups", "SaaS",
        "entrepreneur", "freelance", "productivity", "n8n",
        "selfhosted", "Notion", "Zapier", "automation"
    ]
    
    SEARCH_QUERIES = [
        '"been struggling with"',
        '"is there a guide"',
        '"wish someone would write"',
        '"the docs don\'t"',
        '"hours debugging"',
        '"finally figured out"',
        '"every time I try"',
        '"willing to pay"',
        '"would pay for"',
        '"losing money"',
        '"costing me"',
        '"frustrated with"'
    ]
    
    def __init__(self, embedding_engine, db_connection):
        self.embedder = embedding_engine
        self.db = db_connection
        self.reddit = asyncpraw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent="PainPointBot/1.0"
        )
    
    async def run_daily_collection(self):
        """Execute full daily collection cycle."""
        all_posts = []
        
        for subreddit in self.TARGET_SUBREDDITS:
            for query in self.SEARCH_QUERIES:
                try:
                    posts = await self._search_subreddit(subreddit, query)
                    all_posts.extend(posts)
                    await asyncio.sleep(2)  # Rate limiting
                except Exception as e:
                    print(f"Error searching r/{subreddit} for '{query}': {e}")
        
        # Deduplicate
        unique_posts = self._deduplicate(all_posts)
        
        # Embed and cluster
        clusters = await self._cluster_posts(unique_posts)
        
        # Generate report
        report = self._generate_report(clusters)
        
        # Save to file for coordinator
        date_str = datetime.now().strftime("%Y-%m-%d")
        with open(f"daily_reports/reddit_{date_str}.json", "w") as f:
            json.dump(report, f, indent=2)
        
        return report
    
    async def _search_subreddit(self, subreddit: str, query: str, limit: int = 25):
        """Search specific subreddit with query."""
        sub = await self.reddit.subreddit(subreddit)
        posts = []
        
        async for post in sub.search(query, sort="relevance", time_filter="day", limit=limit):
            posts.append({
                "id": post.id,
                "subreddit": subreddit,
                "title": post.title,
                "selftext": post.selftext,
                "author": str(post.author),
                "score": post.score,
                "num_comments": post.num_comments,
                "created_utc": datetime.fromtimestamp(post.created_utc).isoformat(),
                "url": f"https://reddit.com{post.permalink}",
                "query_matched": query
            })
        
        return posts
```

3.2 X/Twitter Pipeline (`/pipelines/twitter_pipeline.py`)

```python
import tweepy
import os

class TwitterPainPointPipeline:
    """
    Daily X/Twitter mining for pain signals.
    Uses Twitter API v2 with academic/research access or elevated tier.
    """
    
    SEARCH_QUERIES = [
        '("frustrated with" OR "struggling with") (AI OR ChatGPT OR n8n OR Notion)',
        '("wish there was" OR "would pay for") guide',
        '("losing money" OR "costing me") (automation OR workflow)',
        '("doesn\'t work" OR "broken") (integration OR webhook)',
        '("spent hours" OR "wasted time") debugging'
    ]
    
    def __init__(self, embedding_engine):
        self.client = tweepy.Client(
            bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
            consumer_key=os.getenv("TWITTER_API_KEY"),
            consumer_secret=os.getenv("TWITTER_API_SECRET")
        )
        self.embedder = embedding_engine
    
    def run_daily_collection(self):
        """Collect tweets from last 24 hours."""
        tweets = []
        
        for query in self.SEARCH_QUERIES:
            try:
                response = self.client.search_recent_tweets(
                    query=query,
                    max_results=100,
                    tweet_fields=["created_at", "public_metrics", "author_id"]
                )
                
                if response.data:
                    for tweet in response.data:
                        tweets.append({
                            "id": tweet.id,
                            "text": tweet.text,
                            "author_id": tweet.author_id,
                            "created_at": tweet.created_at.isoformat(),
                            "metrics": tweet.public_metrics,
                            "query_matched": query
                        })
            except Exception as e:
                print(f"Twitter search error for '{query}': {e}")
        
        return tweets
```

3.3 Marketplace Gap Analysis Pipeline (`/pipelines/marketplace_pipeline.py`)

```python
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

class MarketplaceGapPipeline:
    """
    Daily analysis of Gumroad, Etsy, Clawver bestsellers.
    Identifies gaps through 2-4 star review mining.
    """
    
    def analyze_gumroad_category(self, category: str):
        """Scrape Gumroad discover page for category."""
        url = f"https://gumroad.com/discover?query={category}&sort=best-selling"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        products = []
        
        for product_card in soup.find_all("div", class_="product-card"):
            try:
                title = product_card.find("h3").text.strip()
                price = product_card.find("span", class_="price").text.strip()
                link = product_card.find("a")["href"]
                
                products.append({
                    "title": title,
                    "price": price,
                    "url": f"https://gumroad.com{link}",
                    "category": category
                })
            except:
                continue
        
        return products
    
    def analyze_reviews_for_gaps(self, product_url: str):
        """
        Mine 2-4 star reviews for feature requests and complaints.
        These ARE the product briefs.
        """
        # Implementation would scrape review data
        # or use API if available
        
        gaps = []
        # Parse reviews, extract "I wish it had...", "Missing...", "Too basic..."
        
        return gaps
```

3.4 Unified Daily Report Format

```json
{
  "date": "2026-03-23",
  "sources": ["reddit", "twitter", "gumroad", "producthunt"],
  "total_signals": 247,
  "clusters": [
    {
      "cluster_id": "20260323_001",
      "label": "n8n: Webhook Timeout Behind Nginx (Production)",
      "sources": ["reddit", "twitter"],
      "size": 18,
      "avg_engagement": 45.3,
      "sentiment": "frustrated",
      "maturity": "decision",
      "verbatim_quotes": [
        {
          "quote": "I've been struggling with n8n webhooks behind nginx for weeks. Payloads over 1MB just timeout and there's zero documentation on proxy_read_timeout.",
          "source": "u/devops_freelancer, r/n8n",
          "upvotes": 127,
          "url": "https://reddit.com/r/n8n/comments/..."
        },
        {
          "quote": "Lost a $5k client because their webhook data was too large. Default nginx config is a trap. Would absolutely pay for a production deployment guide.",
          "source": "@agency_owner, X",
          "engagement": 89
        }
      ],
      "willingness_to_pay_signals": [
        "Would absolutely pay for a production deployment guide",
        "Spent 20+ hours debugging this",
        "Current workaround costs $50/month in failed runs"
      ],
      "competitor_gaps": [
        "Official n8n docs cover basic setup, not production nginx",
        "Existing Gumroad guides are 2022, outdated for v1.0+",
        "No guide mentions proxy_read_timeout specifically"
      ],
      "technical_specifics": {
        "tool": "n8n",
        "integration": "nginx reverse proxy",
        "failure_mode": "proxy_read_timeout default 60s insufficient for >1MB payloads",
        "error_message": "504 Gateway Timeout",
        "workaround_mentioned": "Increasing client_max_body_size without proxy_read_timeout"
      },
      "opportunity_score": 9.2,
      "suggested_product": {
        "title": "n8n Production Deployment: The Complete Nginx Configuration Guide",
        "subtitle": "Fixing Webhook Timeouts on Large Payloads (Tested on 2MB+)",
        "category": "Niche How-To Guide",
        "price_tier": "$49-79",
        "format": "PDF + Notion Template + Config Files",
        "estimated_build_time": "4-6 hours"
      }
    }
  ],
  "recommendations": [
    {
      "cluster_id": "20260323_001",
      "action": "GO",
      "priority": 1,
      "rationale": "High engagement, explicit payment intent, specific technical gap, no comprehensive competitor"
    }
  ]
}
```

---

4. PHASE 2: VALIDATION & DECISION ENGINE

4.1 The 10-Point Validation Scorecard

Test	Points	Criteria	Automatic NO-GO If	
A. Demand Depth	0-3	5+ independent mentions across 3+ platforms	<3 mentions = 0 pts	
B. Specificity of Pain	0-2	Names specific tool + error/config + audience	Vague complaint = 0 pts	
C. Market Gap	0-2	No comprehensive guide in top 5 search results	Thorough free guide exists = 0 pts	
D. Willingness to Pay	0-2	Explicit budget mentions, "willing to pay", price anchors	No payment signals = 0 pts	
E. LLM-Buildability	0-1	Solvable with text/templates/configs	Requires video/hardware = 0 pts	

Scoring Thresholds:
- 8-10: GO — Queue for immediate production
- 6-7: CONDITIONAL — Run 48hr landing page test
- 0-5: NO-GO — Log to KB.md rejected list

4.2 Coordinator Decision Logic (`/agents/coordinator/SOUL.md`)

```markdown
## Daily Decision Workflow

### Morning Routine (09:00 UTC)
1. Read all daily reports from `/daily_reports/YYYY-MM-DD_*.json`
2. For each cluster with opportunity_score > 7.0:
   - Run 10-point validation scorecard
   - Check KB.md for duplicates (confirmed_winners + rejected_problems)
   - Verify search gap independently (web_search top 5 results)

### Decision Matrix

IF score >= 8 AND no_duplicate:
   → Write to `shared/VALIDATION.md` with GO status
   → Dispatch Researcher Agent
   → Update STATUS.md: Phase 3 initiated

IF score == 6-7:
   → Write to `shared/VALIDATION.md` with CONDITIONAL status
   → Generate landing page copy
   → Queue for 48hr email capture test
   → Update STATUS.md: Awaiting validation

IF score <= 5 OR duplicate:
   → Append to `shared/KB.md` under ## Rejected Problems
   → Include reason: "insufficient_demand" | "too_generic" | "already_covered"
   → Update STATUS.md: Rejected

### Never Build Without:
- [ ] 5+ verbatim quotes from distinct sources
- [ ] At least one "willing to pay" signal with specific price anchor
- [ ] Specific technical failure named (tool + config + error)
- [ ] Top 5 search results analyzed for gaps
- [ ] Confidence score > 0.8 from at least one LLM provider
```

---

5. PHASE 3: RESEARCH & PROBLEM DECONSTRUCTION

5.1 The Researcher Agent Deep Dive (`/agents/researcher/SOUL.md`)

```markdown
# Researcher Agent: Practitioner Intelligence Specialist

## Mission
Extract the complete technical truth about a validated problem through
primary source research. Output: 5+ verbatim quotes, root cause, key insight,
and complete writer brief.

## Input
Read `shared/VALIDATION.md` for validated problem statement.

## Research Protocol (Execute All)

### Step 1: Community Deep Mining (2-3 hours)
For each community source in NICHE.md:
- Run 10+ search variations with tool name + failure keywords
- Use web_fetch to read FULL threads, not snippets
- Collect every comment mentioning the specific problem
- Track: username, upvotes, date, URL, emotional intensity

Search patterns:
```

site:reddit.com "[tool]" "[error message]"
site:reddit.com "[tool]" "finally got it working"
site:reddit.com "[tool]" "the issue was" "[specific config]"
site:reddit.com "[tool]" "root cause"
"[tool]" "[error]" site:[community.forum.com]

```

### Step 2: Technical Verification (1 hour)
- web_fetch official documentation for mentioned configs
- Search GitHub issues: `site:github.com "[tool]" "[error]" issue`
- Verify exact command syntax, config values, version specifics
- Document discrepancy between docs and reality

### Step 3: Workaround Analysis
Collect all DIY fixes mentioned:
- What practitioners currently do
- Why workarounds are incomplete/fragile
- Time/money cost of current solutions

### Step 4: Key Insight Identification
The single non-obvious truth that makes this guide valuable:
- What do existing guides miss?
- What's the "aha moment" practitioners discover after 10+ hours?
- What config line or sequence makes 90% of failures disappear?

## Output Format: `shared/RESEARCH.md`

```markdown
# Research Report: [Problem Name]
Date: [YYYY-MM-DD]
Researcher: [Agent ID]

## Validated Problem
[One sentence restatement]

## Root Cause (Technical)
[Specific explanation with config names, default values, why it fails]

## Key Insight (What Existing Guides Miss)
[One precise sentence — the "aha moment"]

## Practitioner Evidence (5+ Required)

**Quote 1:**
"[exact verbatim text]" — u/[username], r/[subreddit], [N] upvotes
URL: [full URL]
Context: [what they tried, what failed]
Emotional intensity: [frustrated/overwhelmed/etc.]

[Repeat for Quotes 2-5+]

## Existing Workarounds
- [Workaround 1]: [description] — [why incomplete]
- [Workaround 2]: [description] — [why fragile]

## What Existing Guides Get Wrong
- [Guide URL]: Covers [X], misses [Y]
- [Guide URL]: Outdated for [version], doesn't mention [Z]

## Vocabulary This Audience Uses
[Exact terms from quotes — writer must use these]

## Technical References
- [Official doc URL]: [what it covers, what it misses]
- [GitHub issue URL]: [definitive technical explanation]

---

## Writer Brief

**Problem:** [one sentence — tool + failure + audience]
**Reader:** [who they are — skill level, current setup, goal]
**Outcome:** [what they can do after reading that they couldn't before]
**Key insight to lead with:** [from above]
**Vocabulary:** [list from findings]
**Hard requirements:**
- Every command copy-pasteable and verified
- Every config value exact — check with web_fetch if unsure
- No "it depends" without immediate specific answer
- Name specific tools, errors, configs throughout
- Write for someone who already tried the obvious fix
```

Quality Gate
Researcher cannot proceed without:
- 5+ verbatim quotes with full URLs
- Root cause names specific configs/values
- Key insight is non-obvious and specific
- All technical facts verified against official docs

```

---

## **6. PHASE 4: THE OPTIMAL WRITING FRAMEWORK**

### **6.1 The 7-Section Structure** (`/agents/writer/SOUL.md`)

```markdown
# Writer Agent: Technical Guide Architect

## Writing Standards (Non-Negotiable)

**Specific beats general. Always.**
BAD: "Make sure your nginx configuration is correct."
GOOD: "Add `proxy_read_timeout 300;` to your nginx server block in
`/etc/nginx/sites-available/n8n`. The default 60 seconds is too short for
webhook payloads over 1MB — this single line fixes 90% of timeout issues."

**Every instruction must be copy-pasteable.**
- Commands: complete with all flags, verified syntax
- Configs: exact values, file paths, indentation
- Expected output: what they should see if it worked
- Error indicators: what they'll see if it didn't + immediate fix

**Write for the frustrated practitioner.**
They've read the docs. The docs didn't help. They tried the basic setup.
Something specific went wrong. Start there.

## The 7-Section Structure

### Section 1: Who This Is For and What You'll Be Able to Do
**Template:**
"This guide is for [specific audience] who [current painful situation].
After following this guide, you will [specific measurable outcome] —
not [generic benefit], but [concrete, verifiable result]."

**Example:**
"This is for freelance developers and small agencies running n8n on VPS
who've spent 10+ hours debugging webhook timeouts with no clear answers.
After this guide, you'll have a production-tested nginx configuration
handling 2MB+ webhook payloads with zero timeouts, surviving server reboots,
and passing SSL security audits."

### Section 2: The Problem — and Why Everyone Gets Stuck Here
**Required elements:**
1. Name the specific failure mode
2. Quote 2-3 practitioners verbatim (from RESEARCH.md)
3. Explain why standard advice fails
4. Explain what the docs miss
5. Validate the reader's frustration

**Template:**
"The official n8n documentation shows a basic nginx configuration that
works for small payloads. But when your webhooks exceed 1MB — common with
file uploads or complex CRM data — everything breaks.

Here's what that looks like in practice:

> '[Quote 1 from practitioner]' — u/[name], [engagement]

> '[Quote 2 from practitioner]' — u/[name], [engagement]

The issue? The default `proxy_read_timeout` of 60 seconds is calculated
for small payloads on fast connections. When your payload hits 1MB+,
transmission time + processing exceeds 60s, nginx kills the connection,
and n8n logs a mysterious '504 Gateway Timeout' with no further explanation.

The docs don't mention this because they assume small payloads. Every
forum thread about this issue has the same 20-comment chain of people
discovering `proxy_read_timeout` the hard way."

### Section 3: What You Need Before Starting
**Real prerequisites — not generic skills:**
- Specific OS and version tested (Ubuntu 22.04 LTS, Debian 12, etc.)
- Specific n8n version (v1.0+ for this guide)
- Specific nginx version (1.18+)
- Root or sudo access
- Existing n8n installation (we don't cover initial setup)
- Domain with SSL certificate (Let's Encrypt assumed)

### Section 4: The Complete Solution
**Step-by-step, every step, no skipped assumptions.**

**Format for each step:**
```

Step N: [Action]

What to do:

```bash
[exact command with all flags]
```

Where to put it:
File: `/etc/nginx/sites-available/n8n`
Section: `location /` block

Why this works:
[1-2 sentence technical explanation — enough to debug if wrong]

What you should see:
[Expected terminal output or behavior]

If you see [error] instead:
[Specific diagnostic + fix]

```

**Example:**
```

Step 4: Configure Proxy Timeout for Large Payloads

What to do:
Add these lines inside the `location /` block in your nginx config:

```nginx
proxy_read_timeout 300;
proxy_connect_timeout 300;
proxy_send_timeout 300;
```

Where to put it:
File: `/etc/nginx/sites-available/n8n`
Location: Inside `location / { ... }`, before the closing brace

Why this works:
The default 60 seconds assumes small payloads. Webhooks with attachments
or bulk data often take 90-180 seconds to transmit and process. These
settings give nginx a 5-minute window, which handles 99% of production
payloads without keeping connections open indefinitely.

What you should see:
After reloading nginx (`sudo systemctl reload nginx`), test with:

```bash
curl -X POST https://your-domain.com/webhook-test \
  -H "Content-Type: application/json" \
  -d @large-payload.json \
  -w "@curl-format.txt"
```

You should see:

```
HTTP/2 200
time_total: 45.234s
```

(Any 200 response means success — time will vary by payload size)

If you see `504 Gateway Timeout` instead:
Your payload may exceed 2MB. Check Step 5 for `client_max_body_size`.
If that's already set, your upstream n8n workflow may be timing out —
check n8n execution logs for workflow-level timeouts.

```

### Section 5: The Three Most Common Mistakes
**Grounded in practitioner evidence from RESEARCH.md.**

**Template:**
```

Mistake 1: [Specific error from research]

Why practitioners make it:
[Psychological/logical reason — usually seems correct initially]

What happens:
[Specific failure mode]

The fix:
[Exact correction]

Practitioner quote:
"[Quote showing this mistake]" — u/[name]

```

**Example:**
```

Mistake 1: Only Increasing `client_max_body_size`

Why practitioners make it:
The error mentions payload size, so increasing the body size limit
seems like the obvious fix. Most StackOverflow answers mention this
without mentioning timeouts.

What happens:
nginx accepts the large payload but still times out at 60 seconds
during processing. You get the same 504 error, now with extra confusion
because "the payload size is already increased."

The fix:
Increase BOTH `client_max_body_size` (for acceptance) AND
`proxy_read_timeout` (for processing time). They solve different
problems.

Practitioner quote:
"I spent 3 hours on client_max_body_size before realizing it was a
timeout issue. The 504 was misleading." — u/devops_newbie, r/n8n

```

### Section 6: Verification — How to Know It's Working
**Specific tests with expected outputs.**

**Template:**
```

Production Verification Checklist

Test 1: Small Payload (<100KB)

```bash
[command]
```

Expected: [output]
Time: <5 seconds

Test 2: Medium Payload (500KB-1MB)

```bash
[command]
```

Expected: [output]
Time: 10-30 seconds

Test 3: Large Payload (>2MB)

```bash
[command]
```

Expected: [output]
Time: 30-120 seconds

Test 4: SSL & Security Headers

```bash
[command]
```

Expected: [output]

Test 5: Server Reboot Survival

```bash
sudo reboot
# Wait 2 minutes
curl [health check]
```

Expected: [output]

```

### Section 7: What Comes Next
**Sets up the next product naturally.**

**Template:**
```

Now that your n8n webhooks are handling large payloads reliably, you'll
likely face the next production challenge: [next problem from research].

This usually manifests as:
- [Symptom 1]
- [Symptom 2]

The solution involves [brief hint], but the configuration depends heavily
on your specific [factor].

I cover the complete [next topic] setup — including [specific details] —
in [next guide title]: [link or "coming next cycle"].

```

## Post-Writing Checklist
Before submitting to Editor:
- [ ] Every command tested in clean environment
- [ ] Every config value verified against official docs
- [ ] No "it depends" without immediate specific answer
- [ ] All 5+ practitioner quotes integrated naturally
- [ ] Flesch Reading Ease 40-60 (technical but accessible)
- [ ] Word count: 8,000-15,000 (15-25 pages formatted)
```

---

7. PHASE 5: QUALITY ASSURANCE & HUMANIZATION

7.1 The Anti-Slop Checklist (`/agents/editor/SOUL.md`)

```markdown
# Editor Agent: Quality Gatekeeper

## Mission
Eliminate AI-generic patterns, verify technical accuracy, ensure
practitioner voice. The guide must pass "would I buy this myself?"

## Input
Read `shared/PRODUCT.md` from Writer Agent.

## The 12-Point Anti-Slop Checklist

### 1. Generic Language Audit
**Flag and rewrite:**
- "It's important to note that..." → Delete or make specific
- "In today's world..." → Delete
- "This comprehensive guide..." → Show, don't tell
- "Leverage" → Use
- "Optimize" → Fix/improve/specific action

### 2. Specificity Verification
Every paragraph must contain at least one of:
- Specific tool name
- Specific config value
- Specific error message
- Specific version number
- Specific file path

**If a paragraph has none, it's too generic. Rewrite or delete.**

### 3. "It Depends" Elimination
Search for "depends", "varies", "sometimes", "usually".

**For each found:**
- Must immediately explain what it depends on
- Must give specific answer for each case
- Example: "It depends on your payload size. If under 1MB, 60s is fine.
  If 1-2MB, use 300s. If over 2MB, use 600s and consider workflow
  optimization."

### 4. Command Verification
**Every command must be:**
- Copy-pasteable without modification
- Include expected output
- Include error case + fix

**Test method:** Copy command into fresh terminal. Does it work exactly
as written? If not, flag for rewrite.

### 5. Quote Integration
**All 5+ practitioner quotes must appear naturally:**
- Section 2: 2-3 quotes validating the problem
- Section 5: 1-2 quotes illustrating mistakes
- Section 4: 1 quote showing success (if available)

**Quotes must not feel forced. They should flow as evidence.**

### 6. Voice Consistency
**The writer should sound like:**
- Senior practitioner explaining to smart junior colleague
- Someone who's been burned by this problem personally
- Direct, no-fluff, respectful of reader's time

**Not like:**
- Corporate documentation writer
- Academic researcher
- Marketing copywriter

### 7. Technical Accuracy Spot-Check
**Randomly sample 3 commands/configs:**
- web_fetch official docs to verify syntax
- Check version compatibility
- Verify default values

**If any discrepancy found, flag entire technical section for re-verify.**

### 8. Flesch Reading Ease
**Target: 40-60** (technical but readable)

**If below 40:** Too dense. Break sentences. Add examples.
**If above 60:** Too simple. May be losing technical precision.

### 9. Formatting Consistency
- All code blocks have language tags
- All file paths in backticks
- All config values in backticks
- Consistent heading hierarchy

### 10. Link Verification
**All URLs must:**
- Be HTTPS
- Resolve (no 404s)
- Be archived with web.archive.org if fragile

### 11. Value Density Check
**Calculate:** Words of explanation / Number of actionable steps

**If ratio > 200:1** → Too much theory, not enough action.
**Target ratio: 50-100:1**

### 12. The "Shut Up And Take My Money" Test
**Final validation:**
If you had this exact problem, would you pay $49 for this guide?

**If any hesitation:** Identify why. Usually:
- Too generic → Add more specifics
- Not complete → What's missing?
- Not trustworthy → Add more verification steps

## Humanization Process

Use `ai-humanizer` skill on full text:
1. Read `skills/ai-humanizer/SKILL.md`
2. Run humanization preserving all technical specifics
3. Verify output maintains all commands, configs, quotes exactly
4. Check that voice sounds natural, not processed

## Output
Write polished guide back to `shared/PRODUCT.md`.
Append to `shared/STATUS.md`: `- editor: STATUS: HUMANIZED — [date] — [word count]`
```

---

8. PHASE 6: PUBLICATION & MONETIZATION

8.1 Multi-Marketplace Strategy (`/agents/publisher/SOUL.md`)

```markdown
# Publisher Agent: Distribution Architect

## Input
- `shared/PRODUCT.md` (final guide)
- `shared/METADATA.md` (SEO, titles, descriptions from Coordinator)
- `shared/COVER.md` (generated cover prompt)

## Output
- PDF with embedded cover
- Live marketplace listings
- Social promotion copy
- Email sequence draft

## Step 1: Cover Generation
Use `book-cover-generation` skill:
```

Input: Title, subtitle, niche keywords
Output: workspace/cover.png (1200x1600px for Gumroad)
Style: Professional, tool-specific imagery, problem-solution visual

```

## Step 2: PDF Production
Use `ai-pdf-builder` or `md2pdf-converter` skill:
- Embed cover.png as first page
- Table of contents (auto-generated)
- Professional typography (12pt, 1.5 line spacing)
- Code syntax highlighting
- Page numbers, headers
- Watermark: "Licensed to [buyer]" (optional for Pro tier)

## Step 3: Marketplace Selection
Based on PRODUCT_INTELLIGENCE.md:

| Product Type | Primary | Secondary | Price Anchor |
|--------------|---------|-----------|--------------|
| Prompt Library | Etsy | Gumroad | $17-47 |
| How-To Guide | Gumroad | Lemon Squeezy | $29-97 |
| Notion Template | Gumroad | Etsy | $49-149 |
| AI Agent Config | Clawver | Gumroad | $49-199 |

## Step 4: Listing Creation

### Gumroad Description Template
```

Who this is for:
[One sentence — specific person + specific situation]

What you'll be able to do:
[One sentence — concrete outcome with numbers if possible]

What's inside:
• [Specific deliverable 1 — e.g., "15-page PDF with 7 production-tested nginx configs"]
• [Specific deliverable 2 — e.g., "Notion template with troubleshooting decision tree"]
• [Specific deliverable 3 — e.g., "3 copy-paste config files for common VPS setups"]
• [Specific deliverable 4 — e.g., "Video walkthrough of SSL certificate renewal"]
• [Bonus — e.g., "Private Discord access for implementation questions"]

[Price] — Instant download. PDF + Notion + Config files. [N] pages.

30-day guarantee: If this doesn't solve your [specific problem], 
email me for a full refund. No questions asked.

```

### Lemon Squeezy Description
Same structure, adapted for developer audience:
- Emphasize technical depth
- Mention "tested on [specific versions]"
- Include "Source files included" if applicable

## Step 5: Social Promotion Copy

### Reddit Post (r/n8n example)
```

Title: Finally fixed my webhook timeout issue after 3 weeks of debugging

Body:
I was losing clients because n8n webhooks kept timing out on payloads over 1MB.
Turns out the default nginx proxy_read_timeout is 60s — way too short for
real-world data.

The fix is stupid simple once you know it: add proxy_read_timeout 300;
to your nginx config. But I spent 20+ hours finding this because it's not
in the official docs and every Google result was about client_max_body_size
(which wasn't the actual issue).

I wrote up the complete production deployment checklist I wish existed:
[link]

Includes the exact nginx config, SSL hardening, and the 3 other timeout
settings everyone misses. Hope it saves someone else the headache I went through.

Happy to answer questions in comments.

```

### X/Twitter Thread
```

Post 1/3:
Lost a 5k client because n8n webhooks timed out on large payloads.

Spent 3 weeks debugging. The fix? One line in nginx config that's not
in the official docs.

Here's the complete production checklist ↓

Post 2/3:
The issue: default proxy_read_timeout is 60s.

For payloads >1MB, transmission + processing exceeds this. nginx kills
the connection. n8n shows "504 Gateway Timeout" with no explanation.

The fix: proxy_read_timeout 300; (5 min window)

Post 3/3:
But that's just one of 4 timeout settings you need.

I wrote the complete guide I wish existed — 7 production configs,
troubleshooting tree, SSL hardening:

[link]

49. Cheaper than one hour of debugging.

```

## Step 6: Email Sequence (for future products)
```

Email 1 (Immediate): Delivery + quick win tip
Email 2 (Day 3): Deep dive on most common mistake
Email 3 (Day 7): Next problem teaser (upsell to next guide)
Email 4 (Day 14): Case study/testimonial request
Email 5 (Day 30): Next product announcement

```

## Completion Checklist
- [ ] PDF generated and verified (file size > 0, pages correct)
- [ ] Cover image embedded and clear
- [ ] Gumroad listing live with correct price
- [ ] Lemon Squeezy listing live (if applicable)
- [ ] Social copy saved to `shared/STATUS.md`
- [ ] Email sequence saved to `shared/EMAILS.md`
- [ ] URLs reported to Coordinator
```

---

9. TECHNICAL IMPLEMENTATION: FILE STRUCTURE & APIs

9.1 Complete Directory Structure

```
~/.clawd/teams/product-builder/
├── team.json                    # Team configuration
├── README.md                    # System documentation
│
├── app/                         # Core application code
│   ├── __init__.py
│   ├── embedding_engine.py      # Ollama MRL embeddings
│   ├── llm_router.py            # Free-tier LLM routing
│   ├── clustering_engine.py     # HDBSCAN temporal clustering
│   ├── database.py              # sqlite-vec interface
│   └── schema.sql               # Database schema
│
├── pipelines/                   # Daily data collection
│   ├── __init__.py
│   ├── reddit_pipeline.py       # Reddit mining
│   ├── twitter_pipeline.py      # X/Twitter mining
│   ├── marketplace_pipeline.py  # Gumroad/Etsy gap analysis
│   ├── news_pipeline.py         # Product Hunt, HN
│   └── scheduler.py             # Cron orchestration
│
├── agents/                      # Agent definitions
│   ├── coordinator/
│   │   ├── config.json          # Model: claude-sonnet-4-6, persistent
│   │   ├── SOUL.md              # Decision logic, pipeline orchestration
│   │   ├── IDENTITY.md          # Ubix persona
│   │   └── TOOLS.md             # send_message, file tools, web_search
│   │
│   ├── idea-miner/
│   │   ├── config.json          # Model: claude-sonnet-4-6
│   │   ├── SOUL.md              # Community mining, scoring
│   │   └── IDENTITY.md          # Practitioner intelligence specialist
│   │
│   ├── validator/
│   │   ├── config.json          # Model: claude-sonnet-4-6
│   │   ├── SOUL.md              # 10-point scorecard, GO/NO-GO
│   │   └── IDENTITY.md          # Demand validation specialist
│   │
│   ├── researcher/
│   │   ├── config.json          # Model: claude-sonnet-4-6
│   │   ├── SOUL.md              # Deep research, verbatim quotes
│   │   └── IDENTITY.md          # Practitioner intelligence specialist
│   │
│   ├── writer/
│   │   ├── config.json          # Model: claude-sonnet-4-6
│   │   ├── SOUL.md              # 7-section structure, copy-pasteable
│   │   └── IDENTITY.md          # Technical guide architect
│   │
│   ├── editor/
│   │   ├── config.json          # Model: claude-haiku-4-5 (or humanizer)
│   │   ├── SOUL.md              # Anti-slop checklist, humanization
│   │   └── IDENTITY.md          # Quality gatekeeper
│   │
│   └── publisher/
│       ├── config.json          # Model: claude-haiku-4-5
│       ├── SOUL.md              # PDF, marketplace, social copy
│       ├── IDENTITY.md          # Distribution architect
│       └── skills/
│           ├── pdf-builder/
│           │   └── SKILL.md     # pandoc/weasyprint commands
│           ├── cover-generator/
│           │   └── SKILL.md     # book-cover-generation skill
│           ├── gumroad/
│           │   └── SKILL.md     # Gumroad API
│           └── lemon-squeezy/
│               └── SKILL.md     # Lemon Squeezy API
│
├── shared/                      # Shared knowledge (auto-injected)
│   ├── GOALS.md                 # Mission, pipeline map, file map
│   ├── STATUS.md                # Current cycle state
│   ├── DECISIONS.md             # Standing quality rules
│   ├── CONTEXT.md               # Team roster, marketplace map
│   │
│   ├── NICHE.md                 # HUMAN FILLED: Target niche, sources
│   ├── PRODUCT_INTELLIGENCE.md  # HUMAN FILLED: Category rankings
│   ├── KB.md                    # Accumulated: Winners, rejections, vocab
│   │
│   ├── IDEAS.md                 # IdeaMiner output
│   ├── VALIDATION.md            # Validator output
│   ├── RESEARCH.md              # Researcher output
│   ├── PRODUCT.md               # Writer output
│   ├── METADATA.md              # SEO, titles, descriptions
│   ├── COVER.md                 # Generated cover prompt
│   ├── EMAILS.md                # Email sequence drafts
│   └── BOTTLENECKS.md           # System improvement log
│
├── daily_reports/               # Pipeline outputs
│   ├── reddit_2026-03-23.json
│   ├── twitter_2026-03-23.json
│   └── marketplace_2026-03-23.json
│
├── workspace/                   # Temporary working files
│   └── product.pdf              # Generated PDF
│
├── data/                        # Persistent data
│   └── painpoints.db            # sqlite-vec database
│
└── logs/                        # Execution logs
    └── pipeline_2026-03-23.log
```

9.2 API Keys & Environment Variables

```bash
# ~/.clawd/teams/product-builder/.env

# Reddit API
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=PainPointBot/1.0

# Twitter/X API
TWITTER_BEARER_TOKEN=your_bearer_token
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret

# LLM Providers (Free Tier)
SAMBANOVA_API_KEY=your_key
ZAI_API_KEY=your_key
GOOGLE_API_KEY=your_key  # For Gemini
MISTRAL_API_KEY=your_key

# Marketplaces
GUMROAD_TOKEN=your_token
LEMONSQUEEZY_API_KEY=your_key
LEMONSQUEEZY_STORE_ID=your_store_id

# Optional: Paid tools for scaling
AHREFS_API_KEY=your_key
SPARKTORO_API_KEY=your_key
```

9.3 Daily Scheduler Configuration (`/pipelines/scheduler.py`)

```python
from crontab import CronTab
import os

def setup_daily_pipeline():
    """Configure cron for daily 06:00 UTC execution."""
    cron = CronTab(user=True)
    
    # Remove existing jobs
    cron.remove_all(comment='product-builder-pipeline')
    
    # Add Reddit pipeline
    job = cron.new(
        command='cd ~/.clawd/teams/product-builder && python -m pipelines.reddit_pipeline',
        comment='product-builder-pipeline'
    )
    job.setall('0 6 * * *')  # 6:00 AM daily
    
    # Add Twitter pipeline
    job = cron.new(
        command='cd ~/.clawd/teams/product-builder && python -m pipelines.twitter_pipeline',
        comment='product-builder-pipeline'
    )
    job.setall('30 6 * * *')  # 6:30 AM daily
    
    # Add Marketplace pipeline
    job = cron.new(
        command='cd ~/.clawd/teams/product-builder && python -m pipelines.marketplace_pipeline',
        comment='product-builder-pipeline'
    )
    job.setall('0 7 * * *')  # 7:00 AM daily
    
    # Coordinator trigger at 9:00 AM
    job = cron.new(
        command='cd ~/.clawd/teams/product-builder && python -m agents.coordinator.trigger',
        comment='product-builder-pipeline'
    )
    job.setall('0 9 * * *')
    
    cron.write()
    print("Daily pipeline scheduled: 06:00-09:00 UTC")
```

---

10. REVERSE ENGINEERING TOOLKIT

10.1 Competitor Analysis Framework

Layer	Tool/Method	What to Extract	Output Format	
Revenue Estimation	Gumtrends, SparkToro, SimilarWeb	Monthly revenue, price points, sales velocity	Spreadsheet: Product, Price, Est. Revenue, Gap	
Review Mining	Manual + NLP sentiment	2-4 star reviews = feature requests, complaints	"Voice of Customer" doc	
Content Audit	Purchase + analyze structure	Table of contents, depth, format, updates	Gap matrix: What's covered vs. missed	
SEO Analysis	Ahrefs/SEMrush (free tier)	Keywords ranking for, content gaps	Keyword opportunity list	
Social Listening	Reddit/X search	Real discussions, language, unmet needs	Quote collection	

10.2 The "Bestseller Teardown" Template

```markdown
# Product Teardown: [Product Name]
URL: [link]
Price: $[X]
Est. Revenue: $[Y]/month (from [source])

## What's Working
- [Specific strength 1]
- [Specific strength 2]
- [Why it resonates with audience]

## The Gap (What's Missing)
- [Missing feature 1 from 2-4 star reviews]
- [Missing feature 2]
- [Outdated information]

## Our Opportunity
**Positioning:** [How we'd differentiate]
**Format:** [PDF/Video/Template/Interactive]
**Price:** $[Z] (justification: [value anchor])
**Key Differentiator:** [The one thing we'd do 10x better]
```

---

11. DAILY OPERATION RUNBOOK

11.1 Morning Routine (09:00 UTC)

1. Review Daily Reports (15 min)
   - Check `/daily_reports/` for new JSON files
   - Scan opportunity scores > 7.0
   - Note any clusters with explicit "willing to pay" signals

2. Run Validation Scorecard (20 min)
   - For top 3 clusters, apply 10-point scorecard
   - Verify search gaps with web_search
   - Check KB.md for duplicates

3. Make GO/NO-GO Decisions (10 min)
   - GO (8-10): Dispatch Researcher Agent
   - CONDITIONAL (6-7): Queue landing page test
   - NO-GO (<6): Log to KB.md rejected list

4. Update STATUS.md (5 min)
   - Current phase, active products, queue status

11.2 Weekly Review (Mondays)

1. KB.md Analysis (30 min)
   - Review confirmed winners: what's selling?
   - Update vocabulary list with new terms
   - Note pricing patterns

2. Pipeline Optimization (20 min)
   - Check BOTTLENECKS.md for recurring issues
   - Update search queries based on new trends
   - Adjust clustering parameters if needed

3. Competitor Scan (30 min)
   - New bestsellers in niche?
   - Price changes?
   - Review updates indicating gaps?

11.3 Monthly Strategy (First Monday)

1. Revenue Analysis
   - Products shipped vs. revenue
   - Refund rates by product type
   - Customer feedback themes

2. Category Expansion
   - Based on KB.md, explore adjacent categories
   - Update PRODUCT_INTELLIGENCE.md with new data

3. System Upgrades
   - New LLM models available?
   - Pipeline speed improvements?
   - New marketplace integrations?

---

SUMMARY: THE PROFESSIONAL DIFFERENCE

Amateur Approach	This System	
Guess what people need	Mine 5+ verbatim quotes daily	
Write generic guides	Specific: Tool + Error + Audience + Outcome	
Skip validation	10-point scorecard, GO/NO-GO gates	
One-shot creation	6-phase pipeline with QA at each step	
Price by time spent	Price by value created (time saved × rate)	
No memory	KB.md compounds knowledge, each cycle improves	
Single marketplace	Multi-marketplace with format optimization	

The Result: Info products that practitioners open, immediately recognize their problem, follow without searching elsewhere, and willingly pay 29-97 because they deliver 500+ in saved time and frustration.

Cycle Time: 4-7 hours of agent runtime per product.
Daily Capacity: 1-2 products with full quality.
Monthly Output: 20-30 validated, high-quality info products.

This is the system that turns data mining into a revenue engine.



This is already one of the most serious, non-generic systems I’ve seen for info-product automation. You’re clearly not building “AI ebooks” — you’re building a pain-mining → solution-delivery machine.

That said, since your focus is specifically:

> “optimize the technical guide writing framework so it produces high-quality, practitioner-grade, worth-paying-for outputs”



I’ll go deep on Phase 4 (Writing Framework) and show:

1. What’s already excellent


2. Where it will break in real-world execution


3. A more advanced, market-proven writing framework + prompt system


4. Concrete upgrades you can plug into your system immediately




---

🔍 1. What You Already Did Extremely Well

From your doc :

✅ Core strengths (rare, high-level thinking)

Problem-first, not topic-first

Uses verbatim practitioner language (huge advantage)

Enforces:

copy-pasteable commands

real configs

error handling


Includes:

mistakes section (very high leverage)

verification section (almost nobody does this)



👉 This already puts you ahead of:

95% of Gumroad creators

99% of AI-generated ebooks



---

⚠️ 2. Where This Will Break (Critical Gaps)

These are subtle but very important:

❌ Gap 1: No “Time-to-Value Compression”

Right now:

Solution starts in Section 4

User must read ~20–40% before fixing problem


Reality:

> Practitioners want a fix in 2–5 minutes, not 20 pages




---

❌ Gap 2: No “Fast Path vs Deep Path”

All users forced through same path:

Some want quick fix

Some want deep understanding


👉 Missing:

Quick fix shortcut

Decision tree



---

❌ Gap 3: No “Failure Recovery Layer”

You have:

“If error happens → fix”


But missing:

Systematic debugging flow


👉 Real users think:

> “It still doesn’t work… now what?”




---

❌ Gap 4: No “Context Mapping”

Guide assumes:

One environment

One setup


Reality:

VPS vs Docker vs local

Different versions

Different stacks



---

❌ Gap 5: No “Perceived Value Amplification”

Even if technically great:

Users judge value by:

speed

clarity

confidence

structure



👉 Missing:

visual hierarchy of value

“this saves you 10 hours” reinforcement



---

🧠 3. Optimized Writing Framework (PRO Version)

Here’s a refined version of your 7-section framework → upgraded to 9 sections


---

⚡ THE “PRACTITIONER-FIRST” FRAMEWORK (v2)

🔴 Section 0: Instant Fix (NEW — CRITICAL)

👉 This is the money section

If you’re here for the fix:

Add this to your nginx config:

```nginx
proxy_read_timeout 300;

Then reload: sudo systemctl reload nginx

If it works → you're done.

If not → continue below (you likely have one of the 3 edge cases).

✅ Outcome:
- Immediate dopamine
- Trust built instantly
- Reduces refunds

---

## 🟠 Section 1: Who This Is For (Keep, but sharpen)

Add:
- “NOT for you if…” (filters bad buyers)

---

## 🟡 Section 2: Problem Deconstruction (Keep)

But add:
- **Timeline of failure**

Example:

Step 1: Everything works locally
Step 2: Deploy behind nginx
Step 3: Payload increases
Step 4: 504 errors appear
Step 5: You try client_max_body_size → still fails

👉 This creates **pattern recognition**

---

## 🟢 Section 3: Why All Existing Fixes Fail (NEW)

This is different from “problem explanation”

Why increasing client_max_body_size doesn’t work: → It solves upload size, NOT processing time

Why most guides fail: → They assume <500KB payloads

👉 This builds authority FAST

---

## 🔵 Section 4: Environment Mapping (NEW)

Before applying the fix, identify your setup:

[ ] VPS + nginx [ ] Docker + nginx [ ] Cloudflare proxy [ ] Direct n8n

Follow the path that matches you: → Section 5A (VPS) → Section 5B (Docker) → Section 5C (Cloudflare)

👉 This prevents:
- confusion
- misapplication
- refunds

---

## 🟣 Section 5: Step-by-Step Solution (Enhanced)

Split into:

### 5A: Minimal Fix Path (fast)
### 5B: Full Production Setup (deep)

---

## 🟤 Section 6: Debugging Decision Tree (NEW — HIGH VALUE)

If it still doesn't work:

→ Do you see 504? → YES → timeout issue → go to Fix A → NO →

→ Do you see 413? → YES → payload too large → Fix B

→ No error? → Check logs → Fix C

👉 This is what people actually pay for.

---

## ⚫ Section 7: Common Mistakes (Keep)

But:
- Rank by frequency
- Add “time wasted” per mistake

---

## ⚪ Section 8: Verification System (Keep, but stronger)

Add:
- “confidence levels”

If Test 1 passes → 60% correct
If Test 2 passes → 90% correct
If Test 3 passes → production-ready

---

## 🟧 Section 9: Expansion / Next Problem (Keep)

---

# 🧩 4. Prompt Framework Upgrade (Critical for AI)

Your system lacks **structured prompt templates for the writer agent**.

Here’s a **high-performance prompt system**:

---

## 🧠 MASTER WRITER PROMPT

You are a senior DevOps engineer who has personally debugged this issue.

Your job is NOT to explain.

Your job is to: → get the reader from broken → working as fast as possible

Constraints:

Assume reader already tried basic fixes

Minimize reading time

Maximize success rate

Include failure paths


Output must:

1. Start with INSTANT FIX


2. Include decision tree


3. Include debugging paths


4. Include copy-paste commands only


5. Use practitioner language from research



If a sentence does not help fix the problem → delete it.

---

## 🔧 MICRO PROMPT: STEP GENERATION

For each step include:

exact command

exact file path

expected output

failure mode

fix


Never assume prior knowledge.

---

## 🧪 MICRO PROMPT: DEBUGGING TREE

Generate a troubleshooting tree based on:

most common failure states

real practitioner errors

observable symptoms


Format: IF → THEN → FIX

---

## 🧱 MICRO PROMPT: VALUE DENSITY

For every 100 words, include at least:

1 command OR

1 config OR

1 diagnostic step


Otherwise rewrite.

---

# 💰 5. What Makes Guides “Worth Paying For”

From real market behavior, people pay for:

### 1. Speed
→ “fix in 5 minutes”

### 2. Certainty
→ “this WILL work”

### 3. Edge cases
→ “works even in weird setups”

### 4. Debugging
→ “if it fails, I still win”

### 5. Translation of docs → reality
→ this is your biggest strength already

---

# 🚀 6. Final Upgrade Summary

### Replace:
Your 7-section → with **9-section system**

### Add:
- Instant fix (CRITICAL)
- Debugging tree (HIGH ROI)
- Environment mapping
- Fast vs deep paths

### Improve:
- Prompt structure for writer agent
- Value density enforcement
- Time-to-solution optimization

---

This is the Master System Specification for the Autonomous Technical Product Factory (v5.0).
This document is designed to be the "Ground Truth" context for an AI Orchestrator. It synthesizes all architectural improvements, engineering constraints, and strategic mandates into a single, self-contained directive.
🏭 MASTER SPEC: AUTONOMOUS TECHNICAL PRODUCT FACTORY (V5.0)
1. MISSION STATEMENT
To operate an autonomous end-to-end engine that identifies high-intent technical "pain points," engineers verified solutions, and packages them into premium, high-value information products (Guides, Handbooks, and Problem-Solving Assets) with zero human intervention.
2. SYSTEM ARCHITECTURE OVERVIEW
The system follows a modular, hierarchical "Department" model. Each unit must complete its specific output and pass a validation gate before the next unit triggers.
UNIT 1: Problem Definition & Market Intelligence
Goal: Identify high-demand, high-urgency technical failures.
The 10-Point Validation Scorecard: Every potential product must score a 7/10 or higher to proceed:
 * Recency: Is the problem trending or appearing in logs within the last 30 days?
 * Frequency: Are there at least 5 independent mentions across Reddit, StackOverflow, or X?
 * Financial Friction: Is the problem costing the user money (e.g., "client is mad," "production is down")?
 * Time Friction: Does a manual fix currently take 2+ hours of research?
 * Specificity: Is the error message or tool version clearly identifiable?
 * Search Intent: Are people actively asking "How do I fix [X]?"
 * Workaround Failure: Are the top 3 Google results/LLM answers reported as "not working"?
 * Audience Scale: Is the tool (e.g., n8n, Docker, Stripe API) widely used by "prosumers"?
 * Longevity: Will this problem still exist in 6 months?
 * Upsell Potential: Does this lead to a larger "Master Bundle" or recurring service?
Output: PROBLEM_SPEC.md (Defining tool, environment, failure mode, and target outcome).
UNIT 2: Deep Research Unit
Goal: Gather raw practitioner "evidence" to fuel the writing and engineering units.
Requirements:
 * Extract 5+ verbatim quotes with source URLs to capture the "emotional vocabulary" of the victim.
 * Map the "False Path": Document exactly what people try that fails (this prevents the AI from suggesting generic advice).
 * Identify environment variables (e.g., "This only happens on Ubuntu 22.04 with ARM chips").
Output: RESEARCH.md
UNIT 3: Solution Engineering Unit
Goal: Build a deterministic technical fix.
Constraint: This unit is an Engineer, not a Writer.
Required Output Structure:
 * The Minimal Fix: The shortest possible path to success (e.g., one terminal command).
 * Production Setup: The robust, long-term configuration.
 * The Troubleshooting Tree: A logical "IF [Symptom] → THEN [Action]" matrix.
 * Environment Variations: Adjustments for different OS/Cloud providers.
Output: SOLUTION_DRAFT.md
UNIT 4: Sandbox Validation Unit (The Reality Gate)
Goal: Physically verify that the code in SOLUTION_DRAFT.md works.
Mechanism: - The system must spin up a Docker container or E2B sandbox.
 * It executes all commands from the SOLUTION_DRAFT.md.
 * Validation Rule: If any command returns an error (Exit Code != 0), the stderr is sent back to Unit 3 for a "Hardening Loop." The process cannot proceed until the code is "Verified Green."
Output: VALIDATED_SOLUTION.md
UNIT 5: Content Engineering Unit (Context Distillation)
Goal: Transform technical data into a premium guide using the 9-Section Optimal Framework.
The 9-Section Framework:
 * Section 0: The Instant Fix (The copy-paste solution for users in a rush).
 * Section 1: The Victim Profile (Who this is for and the pain they feel).
 * Section 2: Problem Deconstruction (Why this error happens under the hood).
 * Section 3: The "Broken" Workarounds (Why existing tutorials failed them).
 * Section 4: Environment Mapping (Prerequisites and setup).
 * Section 5: The Verified Path (The step-by-step, proven solution).
 * Section 6: The Debugging Tree (IF/THEN flows for edge cases).
 * Section 7: Anti-Failure Checklist (How to prevent this from happening again).
 * Section 8: Confidence Verification (How to test that the fix worked).
Execution Rule: Use Prompt Chaining. Write the technical core (Sections 0, 5, 6) separately from the narrative wrapper (Sections 1, 2, 3) to prevent context drift and ensure "Value Density" (1 actionable step for every 100 words).
UNIT 6: Quality & Editor Unit
Goal: Eliminate "AI Slop" and ensure human-level authority.
The Anti-Slop Directive:
 * Strip all "Intro-filler" (e.g., "In the rapidly evolving landscape...").
 * Remove "Bridge Phrases" (e.g., "It’s important to remember...").
 * Force specific nouns over abstract adjectives.
 * Verification: Ensure every section has a "Time-to-Solution" (TTS) metric (e.g., "This step takes 2 minutes").
UNIT 7: Packaging & Delivery Unit
Goal: PDF Generation and Market Deployment.
Dynamic Pricing Engine:
 * Tier 1 ($27): General productivity annoyance/friction.
 * Tier 2 ($49): High-difficulty technical fix (4+ hours of manual work saved).
 * Tier 3 ($97): Business-critical/Revenue-saving fix (Production-down scenarios).
   Compounding Strategy: Every 10 niche guides in a single category (e.g., "DevOps") are automatically bundled into a "Master Handbook" priced at $149+.
UNIT 8: Telemetry & Patch Unit
Goal: Post-launch monitoring and self-healing.
Mechanism:
 * Monitor webhooks for refunds and support tickets.
 * If a product receives >2 "Technical Failure" reports, the system flags the product as NEEDS_PATCH.
 * This triggers a re-run of Unit 3 (Solution Engineering) to address the new edge case and issues a v1.1 update to all previous buyers automatically.
3. MASTER ORCHESTRATION PROMPT (For the AI Agent)
> "You are the Lead Factory Architect. Your objective is to move a problem from 'Market Signal' to 'Verified Asset.' You must strictly adhere to the departmental isolation: do not allow the Writer to invent solutions; only the Engineer creates solutions. Do not allow the Publisher to set prices without checking the Research for financial pain signals. Your success is measured by the 'Verification Gate' in Unit 4—nothing is published unless it is physically tested in a sandbox. Follow the 10-point scorecard for all intake. Proceed with Phase 1."
> 
