// Capture REMO 2026-09-01: desktop + mobile, light-forced, hero viewport only.
// Fresh page per viewport (2 pages, same browser OK); fullPage:false ALWAYS.
import puppeteer from 'puppeteer';
import { writeFileSync, readFileSync, mkdirSync, statSync } from 'fs';
import { join } from 'path';

const PAGE = '2026-09-01-remo.html';
const SLUG = '2026-09-01-remo';
const URL = `http://127.0.0.1:9877/${PAGE}`;
const OUT = '/opt/data/landing-pages/screenshots';
const PORT = '/opt/data/portafolio/public/assets';
mkdirSync(OUT, { recursive: true });

const CHROME = '/opt/data/chrome-linux64/chrome';

const prep = async (page) => {
  await page.evaluate(() => {
    document.documentElement.setAttribute('data-theme', 'light');
  });
  await page.evaluate(() => document.fonts.ready);
  await new Promise((r) => setTimeout(r, 2400));
};

const seed = (page) => page.evaluateOnNewDocument(() => {
  localStorage.setItem('kairos-theme', 'light');
  localStorage.setItem('remo-lang', 'en');
  localStorage.setItem('remo-cookie', 'accepted');
  document.documentElement.setAttribute('data-theme', 'light');
});

const browser = await puppeteer.launch({
  executablePath: CHROME,
  headless: 'new',
  args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu', '--disable-crashpad-forwarding'],
});

// ---------- Desktop 1280x800 ----------
const page = await browser.newPage();
await page.setViewport({ width: 1280, height: 800 });
await seed(page);
await page.goto(URL, { waitUntil: 'networkidle0', timeout: 25000 });
await prep(page);
const errs = [];
page.on('pageerror', (e) => errs.push(String(e)));
const theme = await page.evaluate(() => document.documentElement.getAttribute('data-theme'));
const h1 = await page.evaluate(() => document.querySelector('h1') ? document.querySelector('h1').innerText : 'NONE');
console.log('desktop theme:', theme, '| h1:', h1.replace(/\n/g, ' / '));
const desktopPath = join(OUT, `${SLUG}-desktop.png`);
await page.screenshot({ path: desktopPath, fullPage: false });
console.log('Desktop:', desktopPath, (statSync(desktopPath).size / 1024).toFixed(1) + 'KB');

// ---------- Mobile: measure nav+hero at tall viewport ----------
const m = await browser.newPage();
await m.setViewport({ width: 390, height: 1500 });
await seed(m);
await m.goto(URL, { waitUntil: 'networkidle0', timeout: 25000 });
await prep(m);
const dims = await m.evaluate(() => {
  window.scrollTo({ top: 0, behavior: 'instant' });
  const hero = document.getElementById('hero');
  const nav = document.querySelector('.nav');
  return {
    hero: Math.ceil(hero.getBoundingClientRect().height),
    nav: Math.ceil(nav.getBoundingClientRect().height),
  };
});
const vh = Math.min(dims.nav + dims.hero, 1200);
await m.setViewport({ width: 390, height: vh });
await new Promise((r) => setTimeout(r, 900));
await m.evaluate(() => window.scrollTo({ top: 0, behavior: 'instant' }));
await new Promise((r) => setTimeout(r, 600));
const mobilePath = join(OUT, `${SLUG}-mobile.png`);
await m.screenshot({ path: mobilePath, fullPage: false });
console.log('Mobile:', mobilePath, (statSync(mobilePath).size / 1024).toFixed(1) + 'KB', `| viewport ${390}x${vh} (nav ${dims.nav} + hero ${dims.hero})`);

// mobile interaction probes
const mProbes = await m.evaluate(() => {
  const out = {};
  const t = getComputedStyle(document.querySelector('.theme-toggle'));
  out.toggleVisible = t.display !== 'none';
  const lg = document.querySelector('.nav-actions .lang-select__btn');
  out.langVisible = getComputedStyle(lg).display !== 'none';
  const mb = document.getElementById('menuToggle') || document.querySelector('.menu-toggle');
  if (mb) { mb.click(); }
  return new Promise((res) => setTimeout(() => {
    const mm = document.getElementById('mobileMenu');
    out.menuOpen = mm.classList.contains('open');
    const pill = mm.querySelector('a.btn-primary');
    const pc = pill ? getComputedStyle(pill) : null;
    out.menuPillColor = pc ? pc.color : 'n/a';
    out.menuPillBg = pc ? pc.backgroundColor : 'n/a';
    out.menuPillPadL = pc ? pc.paddingLeft : 'n/a';
    out.cookieVisible = document.getElementById('cookieBanner').className;
    res(out);
  }, 300));
});
console.log('mobile probes:', JSON.stringify(mProbes));

console.log('pageerrors:', errs.length ? errs.slice(0, 5) : 'NONE');

// copy to portfolio with FULL dated slug names
for (const [s, d] of [
  [desktopPath, join(PORT, `landing-${SLUG}.png`)],
  [mobilePath, join(PORT, `landing-${SLUG}-m.png`)],
]) {
  writeFileSync(d, readFileSync(s));
  console.log('copied:', d, (statSync(d).size / 1024).toFixed(1) + 'KB');
}

await browser.close();