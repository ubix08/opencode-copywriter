/**
 * Injects Google NotebookLM cookies into the Chrome profile used by notebooklm-mcp.
 *
 * Usage:
 *   node scripts/inject-notebooklm-cookies.cjs /path/to/cookies.json
 *
 * The cookies JSON should be an array exported from a browser
 * (EditThisCookie extension or similar).
 */
const { chromium } = require('patchright');
const fs = require('fs');
const path = require('path');

const COOKIES_PATH = process.argv[2];
if (!COOKIES_PATH) {
  console.error('Usage: node scripts/inject-notebooklm-cookies.cjs <cookies.json>');
  process.exit(1);
}

const DATA_DIR = path.join(process.env.HOME, '.local/share/notebooklm-mcp');
const USER_DATA_DIR = path.join(DATA_DIR, 'chrome_profile');
const STATE_PATH = path.join(DATA_DIR, 'browser_state', 'state.json');

async function main() {
  const raw = JSON.parse(fs.readFileSync(COOKIES_PATH, 'utf-8'));
  if (!Array.isArray(raw)) {
    console.error('Error: cookies.json must be a JSON array');
    process.exit(1);
  }

  console.log(`Injecting ${raw.length} cookies into ${USER_DATA_DIR}...`);

  const browser = await chromium.launchPersistentContext(USER_DATA_DIR, {
    headless: true,
    args: ['--no-sandbox', '--disable-gpu'],
  });

  const page = await browser.newPage();
  await page.goto('https://notebooklm.google.com', {
    waitUntil: 'networkidle',
    timeout: 60000,
  });
  await page.waitForTimeout(3000);

  let ok = 0, fail = 0;
  for (const c of raw) {
    try {
      await browser.addCookies([{
        name: c.name,
        value: c.value,
        domain: c.domain,
        path: c.path || '/',
        secure: c.secure || false,
        httpOnly: c.httpOnly || false,
        sameSite: c.sameSite === 'lax' ? 'Lax' : c.sameSite === 'strict' ? 'Strict' : 'None',
        expires: Math.round(c.expirationDate || (Date.now() / 1000 + 86400 * 365)),
      }]);
      ok++;
    } catch (e) {
      fail++;
    }
  }

  // Save storage state (so notebooklm-mcp reports authenticated)
  const state = await browser.storageState();
  fs.mkdirSync(path.dirname(STATE_PATH), { recursive: true });
  fs.writeFileSync(STATE_PATH, JSON.stringify(state, null, 2));

  await page.close();
  await browser.close();

  console.log(`\nDone: ${ok} injected, ${fail} failed`);
  console.log(`State saved to ${STATE_PATH}`);
}

main().catch(err => { console.error(err); process.exit(1); });
