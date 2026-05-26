/**
 * Creates state.json in the format Playwright's storageState() uses.
 * The notebooklm-mcp server loads this on startup via loadAuthState() → addCookies().
 */
const fs = require('fs');
const path = require('path');

const COOKIES_PATH = process.argv[2] || '/tmp/notebooklm_cookies.json';
const STATE_PATH = path.join(process.env.HOME, '.local/share/notebooklm-mcp/browser_state/state.json');

function sameSite(c) {
  const s = (c.sameSite || 'unspecified').toLowerCase();
  if (s === 'lax' || s === 'Lax') return 'Lax';
  if (s === 'strict' || s === 'Strict') return 'Strict';
  return 'None';
}

const raw = JSON.parse(fs.readFileSync(COOKIES_PATH, 'utf-8'));

const state = {
  cookies: raw.map(c => ({
    name: c.name,
    value: c.value,
    domain: c.domain,
    path: c.path || '/',
    expires: c.expirationDate || -1,
    httpOnly: c.httpOnly || false,
    secure: c.secure || false,
    sameSite: sameSite(c),
  })),
  origins: [
    {
      origin: 'https://notebooklm.google.com',
      localStorage: [],
    },
  ],
};

fs.mkdirSync(path.dirname(STATE_PATH), { recursive: true });
fs.writeFileSync(STATE_PATH, JSON.stringify(state, null, 2));

console.log(`Written ${state.cookies.length} cookies to ${STATE_PATH}`);
console.log('Cookies:');
state.cookies.forEach(c => console.log(`  ${c.domain}: ${c.name}`));
