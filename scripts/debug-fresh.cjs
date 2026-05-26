const { chromium } = require('patchright');
const path = require('path');
const fs = require('fs');

const STATE_PATH = path.join(process.env.HOME, '.local/share/notebooklm-mcp/browser_state/state.json');

async function main() {
  const state = JSON.parse(fs.readFileSync(STATE_PATH, 'utf-8'));

  const browser = await chromium.launch({ channel: 'chrome', headless: true, args: ['--no-sandbox', '--disable-gpu'] });
  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
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

  // Navigate to notebooklm
  const response = await page.goto('https://notebooklm.google.com', { waitUntil: 'networkidle', timeout: 30000 });
  const url = page.url();

  console.log(`Status: ${response?.status()}`);
  console.log(`Final URL: ${url.substring(0, 120)}`);
  console.log(`Auth: ${url.startsWith('https://notebooklm.google.com/') ? '✅' : '❌'}`);

  // Check what cookies we have
  const ctxCookies = await context.cookies();
  const osid = ctxCookies.find(c => c.name === 'OSID');
  const sosid = ctxCookies.find(c => c.name === '__Secure-OSID');
  console.log(`\nOSID: ${osid ? `expires=${osid.expires}, domain=${osid.domain}` : 'NOT FOUND'}`);
  console.log(`__Secure-OSID: ${sosid ? `expires=${sosid.expires}, domain=${sosid.domain}` : 'NOT FOUND'}`);

  // Check what cookies are available at notebooklm domain
  const nlmCookies = await context.cookies(['https://notebooklm.google.com']);
  console.log(`\nCookies available at notebooklm domain:`);
  for (const c of nlmCookies) {
    console.log(`  ${c.name} (domain=${c.domain})`);
  }

  await browser.close();
}

main().catch(err => { console.error('Error:', err.message); process.exit(1); });
