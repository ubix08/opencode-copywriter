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

  // Clear all existing cookies first
  await browser.clearCookies();

  // Inject each cookie individually with explicit URL
  for (const c of state.cookies) {
    const cookie = {
      name: c.name,
      value: c.value,
      httpOnly: c.httpOnly || false,
      secure: c.secure || false,
      sameSite: c.sameSite || 'Lax',
      expires: Math.floor(c.expires || c.expirationDate || 0),
    };
    if (c.hostOnly) {
      cookie.url = `${c.secure ? 'https' : 'http'}://${c.domain}${c.path || '/'}`;
    } else {
      cookie.url = `${c.secure ? 'https' : 'http'}://${c.domain.startsWith('.') ? 'www' : ''}${c.domain}${c.path || '/'}`;
    }
    try {
      await browser.addCookies([cookie]);
    } catch (e) {
      console.log(`Failed to set ${c.name}: ${e.message}`);
    }
  }

  const cookies = await browser.cookies();
  console.log(`\nCookies in context after injection (${cookies.length} total):`);
  for (const c of cookies) {
    console.log(`  ${c.name} domain=${c.domain} secure=${c.secure}`);
  }
  console.log();

  // Verify we have notebooklm cookies
  const nlmCookies = cookies.filter(c => c.domain.includes('notebooklm'));
  const googleCookies = cookies.filter(c => c.domain.includes('google.com') && !c.domain.includes('notebooklm'));
  console.log(`notebooklm cookies: ${nlmCookies.length}`);
  console.log(`google.com cookies: ${googleCookies.length}`);
  console.log();

  const page = await browser.newPage();
  await page.goto('https://notebooklm.google.com', {
    waitUntil: 'networkidle',
    timeout: 30000,
  });

  if (!page.url().startsWith('https://notebooklm.google.com/')) {
    console.log(`Redirected to: ${page.url()}`);
    await page.screenshot({ path: '/tmp/nlm_auth_debug.png' });
  } else {
    console.log('✅ Authenticated!');
  }

  await browser.close();
}

main().catch(err => { console.error('Error:', err.message); process.exit(1); });
