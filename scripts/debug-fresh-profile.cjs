const { chromium } = require('patchright');
const path = require('path');
const fs = require('fs');

const STATE_PATH = path.join(process.env.HOME, '.local/share/notebooklm-mcp/browser_state/state.json');
const PROFILE_DIR = path.join(process.env.HOME, '.local/share/notebooklm-mcp/chrome_profile');

async function main() {
  const state = JSON.parse(fs.readFileSync(STATE_PATH, 'utf-8'));
  const profileExists = fs.existsSync(PROFILE_DIR);
  console.log(`Profile dir exists: ${profileExists}`);
  if (profileExists) {
    const files = fs.readdirSync(PROFILE_DIR);
    console.log(`Profile files: ${files.length}`);
  }

  const context = await chromium.launchPersistentContext(PROFILE_DIR, {
    channel: 'chrome',
    headless: true,
    args: ['--no-sandbox', '--disable-gpu'],
  });

  // Inject cookies - exactly as the MCP server does
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
  const url = page.url();
  console.log(`\nURL: ${url.substring(0, 120)}`);
  console.log(`Auth: ${url.startsWith('https://notebooklm.google.com/') ? '✅' : '❌'}`);

  if (url.startsWith('https://notebooklm.google.com/')) {
    const text = await page.evaluate(() => document.body.innerText.substring(0, 500));
    console.log(`\nPage title: ${text.split('\n')[0]}`);
    // Check for notebooks
    const notebooks = await page.evaluate(() => {
      const links = Array.from(document.querySelectorAll('a[href*="/notebook/"]'));
      return links.slice(0, 5).map(a => ({
        text: a.textContent?.trim(),
        href: a.href,
      }));
    });
    if (notebooks.length > 0) {
      console.log(`\nNotebooks found: ${notebooks.length}`);
      for (const nb of notebooks) {
        console.log(`  ${nb.text || 'unnamed'} → ${nb.href}`);
      }
    } else {
      console.log('\nNo notebook links on page');
      console.log('Page text preview:', text.substring(0, 300));
    }
  }

  await context.close();
}

main().catch(err => { console.error('Error:', err.message); process.exit(1); });
