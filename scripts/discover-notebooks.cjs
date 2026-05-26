const { chromium } = require('patchright');
const path = require('path');
const fs = require('fs');

const STATE_PATH = path.join(process.env.HOME, '.local/share/notebooklm-mcp/browser_state/state.json');
const PROFILE_DIR = path.join(process.env.HOME, '.local/share/notebooklm-mcp/chrome_profile');

async function main() {
  const state = JSON.parse(fs.readFileSync(STATE_PATH, 'utf-8'));

  const context = await chromium.launchPersistentContext(PROFILE_DIR, {
    channel: 'chrome',
    headless: true,
    args: ['--no-sandbox', '--disable-gpu'],
  });

  await context.addCookies(
    state.cookies.map(c => ({
      name: c.name, value: c.value,
      domain: c.domain, path: c.path || '/',
      httpOnly: c.httpOnly || false,
      secure: c.secure || false,
      sameSite: c.sameSite === 'no_restriction' ? 'None' : c.sameSite === 'lax' ? 'Lax' : c.sameSite === 'strict' ? 'Strict' : 'Lax',
      expires: Math.floor(c.expires || c.expirationDate || 0),
    }))
  );

  const page = await context.newPage();
  await page.goto('https://notebooklm.google.com', { waitUntil: 'networkidle', timeout: 30000 });

  // Extract full notebook details
  const notebooks = await page.evaluate(() => {
    const found = [];
    document.querySelectorAll('a[href*="/notebook/"]').forEach(a => {
      const href = a.href || '';
      const match = href.match(/\/notebook\/([a-f0-9-]{36})/);
      if (match) {
        const card = a.closest('[class*="card"], [class*="item"], [role="button"]') || a.parentElement?.closest('[class*="card"], [class*="item"]') || a.closest('li') || a;
        const allText = card?.textContent?.trim() || a.textContent?.trim() || '';
        const name = a.getAttribute('aria-label') || a.querySelector('[class*="title"], [class*="name"]')?.textContent?.trim() || allText.split('\n')[0]?.trim() || 'unnamed';
        found.push({
          uuid: match[1],
          name: name,
          url: href,
        });
      }
    });
    return found;
  });

  console.log('Notebooks:');
  for (const nb of notebooks) {
    console.log(`  ${nb.name}`);
    console.log(`    UUID: ${nb.uuid}`);
    console.log(`    URL:  ${nb.url}`);
    console.log();
  }

  await context.close();
}

main().catch(err => { console.error('Error:', err.message); process.exit(1); });
