const { chromium } = require('patchright');
const fs = require('fs');
const path = require('path');

const COOKIES_PATH = process.argv[2] || '/tmp/notebooklm_cookies.json';
const USER_DATA_DIR = path.join(process.env.HOME, '.local/share/notebooklm-mcp/chrome_profile');
const STATE_DIR = path.join(process.env.HOME, '.local/share/notebooklm-mcp/browser_state');

async function main() {
  const raw = JSON.parse(fs.readFileSync(COOKIES_PATH, 'utf-8'));
  console.log(`Loaded ${raw.length} cookies from ${COOKIES_PATH}`);

  // Start fresh - clear the old profile state
  fs.rmSync(USER_DATA_DIR, { recursive: true, force: true });
  fs.rmSync(STATE_DIR, { recursive: true, force: true });
  fs.mkdirSync(USER_DATA_DIR, { recursive: true });
  fs.mkdirSync(STATE_DIR, { recursive: true });

  const browser = await chromium.launchPersistentContext(USER_DATA_DIR, {
    channel: 'chrome',
    headless: true,
    args: ['--no-sandbox', '--disable-gpu', '--disable-blink-features=AutomationControlled'],
  });

  // First navigate to google.com to establish a session
  const page = await browser.newPage();
  await page.goto('https://www.google.com', { waitUntil: 'networkidle', timeout: 30000 });

  // Add ALL cookies
  let ok = 0, fail = 0;
  for (const c of raw) {
    const sameSite = c.sameSite === 'lax' ? 'Lax' : c.sameSite === 'strict' ? 'Strict' : 'None';
    try {
      await browser.addCookies([{
        name: c.name,
        value: c.value,
        domain: c.domain.startsWith('.') ? c.domain : c.domain,
        path: c.path || '/',
        secure: c.secure ?? false,
        httpOnly: c.httpOnly ?? false,
        sameSite: sameSite,
        expires: Math.round(c.expirationDate || (Date.now() / 1000 + 86400 * 365)),
      }]);
      ok++;
    } catch (e) {
      fail++;
    }
  }
  console.log(`Cookies: ${ok} set, ${fail} failed`);

  // Now navigate to NotebookLM
  console.log('\nNavigating to NotebookLM...');
  const resp = await page.goto('https://notebooklm.google.com', {
    waitUntil: 'networkidle',
    timeout: 60000,
  });

  const finalUrl = page.url();
  console.log(`Final URL: ${finalUrl}`);

  if (finalUrl.startsWith('https://notebooklm.google.com/')) {
    console.log('✅ Successfully authenticated!');
    await page.waitForTimeout(3000);

    // Try to discover notebooks
    const notebooks = await page.evaluate(() => {
      const found = [];
      document.querySelectorAll('a[href*="/notebook/"]').forEach(a => {
        const href = a.getAttribute('href') || a.href || '';
        const match = href.match(/\/notebook\/([a-f0-9-]{36})/);
        if (match) {
          const name = a.textContent?.trim() || a.getAttribute('aria-label') || '';
          const card = a.closest('[class*="card"], [class*="item"], li, [role="button"]');
          const desc = card?.textContent?.trim()?.slice(0, 200) || '';
          found.push({ uuid: match[1], name, desc });
        }
      });
      return found;
    });

    if (notebooks.length > 0) {
      console.log(`\n📚 Found ${notebooks.length} notebook(s):`);
      for (const nb of notebooks) {
        console.log(`  [${nb.uuid}] ${nb.name || '(unnamed)'}`);
        console.log(`    https://notebooklm.google.com/notebook/${nb.uuid}`);
      }
    } else {
      console.log('\nNo notebooks found on dashboard');
      console.log('\nPage title:', await page.title());
    }

    // Save storage state so MCP server recognizes auth
    const state = await browser.storageState();
    fs.writeFileSync(path.join(STATE_DIR, 'state.json'), JSON.stringify(state, null, 2));
    console.log(`\n✅ State saved (${state.cookies?.length || 0} cookies, ${state.origins?.length || 0} origins)`);

  } else {
    console.log('❌ Not authenticated - redirected to login');
    console.log('Cookies may be expired or invalid.');
  }

  await page.close();
  await browser.close();
}

main().catch(err => { console.error('Error:', err.message); process.exit(1); });
