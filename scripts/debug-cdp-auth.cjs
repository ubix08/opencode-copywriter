const { chromium } = require('patchright');
const path = require('path');
const fs = require('fs');

const STATE_PATH = path.join(process.env.HOME, '.local/share/notebooklm-mcp/browser_state/state.json');
const USER_DATA_DIR = path.join(process.env.HOME, '.local/share/notebooklm-mcp/chrome_profile');

async function main() {
  const state = JSON.parse(fs.readFileSync(STATE_PATH, 'utf-8'));

  const browser = await chromium.launchPersistentContext(USER_DATA_DIR, {
    channel: 'chrome',
    headless: true,
    args: ['--no-sandbox', '--disable-gpu', '--disable-blink-features=AutomationControlled'],
  });

  // Use CDP to set cookies directly via Network.setCookie
  const page = await browser.newPage();
  const cdp = await page.context().newCDPSession(page);

  // First navigate to notebooklm to establish a secure context
  await page.goto('https://notebooklm.google.com/login', {
    waitUntil: 'domcontentloaded',
    timeout: 30000,
  });

  console.log(`Initial navigation: ${page.url()}`);

  // Inject cookies via CDP
  let injectedCount = 0;
  for (const c of state.cookies) {
    const params = {
      name: c.name,
      value: c.value,
      url: 'https://notebooklm.google.com',
      path: c.path || '/',
      secure: c.secure || false,
      httpOnly: c.httpOnly || false,
      sameSite: c.sameSite === 'no_restriction' ? 'None' : c.sameSite === 'lax' ? 'Lax' : c.sameSite === 'strict' ? 'Strict' : 'Unspecified',
    };
    if (c.expirationDate) params.expires = c.expirationDate;
    if (c.hostOnly) {
      // For hostOnly, use the exact host as URL
      params.url = `https://${c.domain}`;
    }
    try {
      const result = await cdp.send('Network.setCookie', params);
      if (result.success) injectedCount++;
    } catch (e) {
      // ignore
    }
  }
  console.log(`Injected ${injectedCount}/${state.cookies.length} cookies via CDP`);

  // Now reload the page
  await page.reload({ waitUntil: 'networkidle', timeout: 30000 });
  console.log(`After reload: ${page.url()}`);

  // Check cookies in context
  const ctxCookies = await browser.cookies();
  const nlmCookies = ctxCookies.filter(c => c.domain.includes('notebooklm'));
  console.log(`Cookies for notebooklm domain: ${nlmCookies.map(c => c.name).join(', ')}`);

  if (page.url().startsWith('https://notebooklm.google.com/')) {
    console.log('✅ Authenticated!');
    await page.screenshot({ path: '/tmp/nlm_cdp_auth.png', fullPage: true });
    const text = await page.evaluate(() => document.body.innerText.substring(0, 2000));
    console.log('Page content:', text.substring(0, 500));
  } else if (page.url().includes('accounts.google.com')) {
    console.log('❌ Redirected to Google login');
  } else {
    console.log(`Unknown redirect: ${page.url()}`);
  }

  await browser.close();
}

main().catch(err => { console.error('Error:', err.message); process.exit(1); });
