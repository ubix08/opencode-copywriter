/**
 * Direct cookie injection - writes cookies directly into Chrome's SQLite database.
 * This bypasses Playwright's addCookies API which has issues with secure/session cookies.
 */
const { chromium } = require('patchright');
const fs = require('fs');
const path = require('path');
const Database = require('better-sqlite3');

const COOKIES_PATH = process.argv[2] || '/tmp/notebooklm_cookies.json';
const USER_DATA_DIR = path.join(process.env.HOME, '.local/share/notebooklm-mcp/chrome_profile');
const STATE_DIR = path.join(process.env.HOME, '.local/share/notebooklm-mcp/browser_state');

async function main() {
  const raw = JSON.parse(fs.readFileSync(COOKIES_PATH, 'utf-8'));
  console.log(`Loaded ${raw.length} cookies`);

  // Start fresh
  fs.rmSync(USER_DATA_DIR, { recursive: true, force: true });
  fs.rmSync(STATE_DIR, { recursive: true, force: true });

  // First, launch browser to create the profile structure
  const browser = await chromium.launchPersistentContext(USER_DATA_DIR, {
    channel: 'chrome',
    headless: true,
    args: ['--no-sandbox', '--disable-gpu'],
  });
  const page = await browser.newPage();
  await page.goto('https://www.google.com', { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.close();
  await browser.close();

  // Now write cookies directly to the SQLite database
  const dbPath = path.join(USER_DATA_DIR, 'Default', 'Cookies');
  console.log(`Opening cookie DB: ${dbPath}`);

  const db = new Database(dbPath);
  db.pragma('journal_mode = WAL');

  let inserted = 0;
  for (const c of raw) {
    const now = Math.floor(Date.now() / 1000000);
    const expires = Math.round(c.expirationDate || (now + 86400 * 365));
    const isSecure = c.secure ? 1 : 0;
    const isHttpOnly = c.httpOnly ? 1 : 0;
    const hasExpires = 1;
    const isPersistent = c.session === false ? 1 : 1;
    const priority = 1;
    const samesite = c.sameSite === 'lax' ? 1 : c.sameSite === 'strict' ? 2 : 0;
    const sourceScheme = isSecure ? 2 : 0;

    // Map sameSite enum for Chrome
    let samesite_enum = 0; // Unspecified
    if (c.sameSite === 'lax') samesite_enum = 1;
    else if (c.sameSite === 'strict') samesite_enum = 2;

    try {
      db.prepare(`
        INSERT OR REPLACE INTO cookies
          (creation_utc, host_key, top_frame_site_key, name, value, 
           encrypted_value, path, expires_utc, is_secure, is_httponly, 
           last_access_utc, has_expires, is_persistent, priority, 
           samesite, source_scheme, source_port, is_same_party)
        VALUES
          (?, ?, '', ?, ?, '', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 443, 0)
      `).run(
        now, c.domain, c.name, c.value,
        c.path || '/', expires * 1000000, isSecure, isHttpOnly,
        now, hasExpires, isPersistent, priority,
        samesite_enum, sourceScheme
      );
      inserted++;
    } catch (e) {
      console.log(`  Failed to insert ${c.name}: ${e.message}`);
    }
  }

  db.close();
  console.log(`Direct DB insert: ${inserted} cookies`);

  // Now verify by launching browser and checking if auth works
  console.log('\nVerifying authentication...');
  const browser2 = await chromium.launchPersistentContext(USER_DATA_DIR, {
    channel: 'chrome',
    headless: true,
    args: ['--no-sandbox', '--disable-gpu'],
  });
  const page2 = await browser2.newPage();

  await page2.goto('https://notebooklm.google.com', {
    waitUntil: 'networkidle',
    timeout: 60000,
  });

  const finalUrl = page2.url();
  console.log(`Final URL: ${finalUrl}`);

  if (finalUrl.startsWith('https://notebooklm.google.com/')) {
    console.log('✅ Authentication successful!');
    await page2.waitForTimeout(3000);

    // Save state for MCP server
    const state = await browser2.storageState();
    fs.mkdirSync(STATE_DIR, { recursive: true });
    fs.writeFileSync(path.join(STATE_DIR, 'state.json'), JSON.stringify(state, null, 2));
    console.log(`State saved (${state.cookies?.length || 0} cookies)`);

    // Discover notebooks
    const notebooks = await page2.evaluate(() => {
      const found = [];
      document.querySelectorAll('a[href*="/notebook/"]').forEach(a => {
        const href = a.getAttribute('href') || a.href || '';
        const match = href.match(/\/notebook\/([a-f0-9-]{36})/);
        if (match) {
          const name = a.textContent?.trim() || a.getAttribute('aria-label') || '';
          found.push({ uuid: match[1], name, url: `https://notebooklm.google.com/notebook/${match[1]}` });
        }
      });
      return found;
    });

    if (notebooks.length > 0) {
      console.log(`\n📚 Found ${notebooks.length} notebook(s):`);
      for (const nb of notebooks) {
        console.log(`  [${nb.uuid}] ${nb.name || '(unnamed)'}`);
        console.log(`    ${nb.url}`);
      }
    } else {
      console.log('\nNo notebooks found on dashboard (account may be empty)');
      const text = await page2.evaluate(() => document.body.innerText);
      text.split('\n').filter(l => l.trim()).slice(0, 20).forEach((l, i) => console.log(`  ${i+1}. ${l}`));
    }
  } else {
    console.log('❌ Authentication failed');
  }

  await page2.close();
  await browser2.close();
}

main().catch(err => { console.error('Error:', err.message); process.exit(1); });
