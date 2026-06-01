## Session State (May 2026)

### Products Built & Ready for Gumroad (10 total)

| Product | Package | Price | Notes |
|---------|---------|-------|-------|
| Freelance Rate Calculator | `build/Freelance-Rate-Calculator-v1.0.zip` | $12 | html, 9 files |
| SaaS Revenue Calculator | `build/SaaS-Revenue-Intelligence-v1.0.zip` | $15 | html, 9 files |
| Content Calendar Planner | `build/Content-Calendar-Planner-v1.0.zip` | $9 | html, 9 files |
| SEO Audit Pro (fixed v2.0) | `build/SEO-Audit-Pro-v1.0.zip` | $19 | html, 9 files — 6 bug fixes applied |
| SEO Audit Pro AI (v3.0) | `build/SEO-Audit-Pro-AI-v1.0.zip` | $29 | html, Anthropic API streaming, AI features |
| SMB Agent Blueprint | `build/SMB-Agent-Blueprint-v1.0.zip` | $19 | html, 9 files |
| Gumroad Factory | `build/Gumroad-Factory-v1.0.zip` | $25 | html, 9 files |
| BizPulse KPI Dashboard | `build/BizPulse-KPI-Dashboard-v2.1.zip` | $49 | html, also at `content/info-products/BizPulse-KPI-Dashboard-v2.1.zip` |
| Sales Pipeline Tracker Pro | `build/Sales-Pipeline-Tracker-Pro-Bundle.zip` | $49-$79 | Excel + docs + AI prompts — custom bundle format, not BizPulse template |
| business-kpi-dashboard.html | `build/business-kpi-dashboard.html` | — | Standalone HTML (duplicate of content/info-products/) |

### Active Code Files
- `build/SEO-Audit-Pro/SEO-Audit-Pro.html` — bug-fixed v2.0 (2031 lines, 6 fixes applied)
- `build/SEO-Audit-Pro-AI/SEO-Audit-Pro-AI.html` — AI v3.0 (2455 lines, Anthropic API integration)
- `content/info-products/` — 7 built HTML products + BizPulse zip
- `build/` — 7 Gumroad zips + unpacked dirs + 2 new user-added files

### User-Added Products (via GitHub)
- `build/Sales-Pipeline-Tracker-Pro-Bundle.zip` — custom structure: `sales-pipeline-bundle/{ product/, docs/, bonus/ }` with GUMROAD-LISTING.md inside
- `build/Sales-Pipeline-Tracker-Pro.xlsx` — standalone copy of the same file in the zip
- `build/BizPulse-KPI-Dashboard-v2.1.zip` — copy from `content/info-products/`
- `build/business-kpi-dashboard.html` — copy from `content/info-products/`

### 27 More Product Ideas in Pipeline
See `content/info-products/README.md` — categories: HTML tools (1 more), how-to guides (7), site templates (5), spreadsheet tools (5), research reports (5), bundles (4).

### Creating New Products
Each HTML ZIP follows BizPulse template: `Product-Name-v1.0.zip → Product-Name/{ main.html, README.txt, QUICK-START.txt, LICENSE.txt, bonus/{ GUMROAD-LISTING-COPY.txt, 2 bonus files } }`.

Excel/doc products may use custom bundle format as seen in Sales Pipeline Tracker Pro.

### Active Bug-fix Patterns (apply to any new HTML products)
1. `localStorage` wrapped in `try/catch` for sandboxed iframe fallback
2. Modal backdrop `onclick="if(event.target===this)..."` — target check, not just on overlay ID
3. Chart.js `chartVar.destroy()` before re-creating chart on same canvas
4. Score ring `stroke-dasharray` starts at full circumference in HTML, then rAF to correct offset
5. `oninput` instead of `onchange` on textareas for immediate state save
6. Double `requestAnimationFrame` instead of `setTimeout` for print/export timing
7. `updateModuleScoreDisplay()` called after each check toggle to keep big score in sync
