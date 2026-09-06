import puppeteer from 'puppeteer';
import { writeFileSync, mkdirSync, readFileSync, statSync } from 'fs';
import { join } from 'path';

const SLUG = '2026-09-04-calibre';
const PAGE = '2026-09-04-calibre.html';
const URL = `http://localhost:9877/${PAGE}`;
const OUT = '/opt/data/landing-pages/screenshots';
const PORTFOLIO = '/opt/data/portafolio/public/assets';
mkdirSync(OUT, { recursive: true });

const CHROME = '/opt/data/chrome-linux64/chrome';
const LAUNCH = {
  executablePath: CHROME,
  headless: true,
  args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu', '--disable-crashpad-forwarding'],
};

function seed(page) {
  return page.evaluateOnNewDocument(() => {
    localStorage.setItem('calibre-lang', 'en');
    localStorage.setItem('calibre-cookie', 'accepted');
    localStorage.setItem('kairos-theme', 'light');
    document.documentElement.setAttribute('data-theme', 'light');
  });
}

async function prep(page) {
  await page.evaluate(() => {
    localStorage.setItem('kairos-theme', 'light');
    document.documentElement.setAttribute('data-theme', 'light');
  });
  await page.evaluate(() => document.fonts.ready);
  await new Promise((r) => setTimeout(r, 2200));
}

async function main() {
  // Desktop
  const b1 = await puppeteer.launch(LAUNCH);
  const p1 = await b1.newPage();
  await p1.setViewport({ width: 1280, height: 800 });
  await seed(p1);
  await p1.goto(URL, { waitUntil: 'networkidle0', timeout: 30000 });
  await prep(p1);
  // scroll reveal: down (instant) then back to top
  await p1.evaluate(() => window.scrollTo({ top: 1600, behavior: 'instant' }));
  await new Promise((r) => setTimeout(r, 700));
  await p1.evaluate(() => document.getElementById('hero').scrollIntoView({ block: 'start', behavior: 'instant' }));
  await new Promise((r) => setTimeout(r, 900));
  const dPath = join(OUT, `${SLUG}-desktop.png`);
  await p1.screenshot({ path: dPath, fullPage: false });
  console.log('Desktop:', dPath, (statSync(dPath).size / 1024).toFixed(1) + 'KB');
  await b1.close();

  // Mobile — measure hero + nav at tall viewport, then fit
  const b2 = await puppeteer.launch(LAUNCH);
  const p2 = await b2.newPage();
  await p2.setViewport({ width: 390, height: 1500 });
  await seed(p2);
  await p2.goto(URL, { waitUntil: 'networkidle0', timeout: 30000 });
  await prep(p2);
  await p2.evaluate(() => window.scrollTo({ top: 0, behavior: 'instant' }));
  const dims = await p2.evaluate(() => {
    const h = document.getElementById('hero');
    const n = document.querySelector('.nav');
    const hr = h ? h.getBoundingClientRect() : null;
    const nr = n ? n.getBoundingClientRect() : null;
    return { hero: hr ? Math.ceil(hr.height) : 844, nav: nr ? Math.ceil(nr.height) : 64 };
  });
  console.log('HeroH', dims.hero, 'NavH', dims.nav);
  const vh = Math.min(dims.hero + dims.nav, 1500);
  await p2.setViewport({ width: 390, height: vh });
  await new Promise((r) => setTimeout(r, 900));
  const mPath = join(OUT, `${SLUG}-mobile.png`);
  await p2.screenshot({ path: mPath, fullPage: false });
  console.log('Mobile:', mPath, (statSync(mPath).size / 1024).toFixed(1) + 'KB', 'vh', vh);
  await b2.close();

  // copy to portfolio
  const d = readFileSync(dPath);
  const m = readFileSync(mPath);
  writeFileSync(join(PORTFOLIO, `landing-${SLUG}.png`), d);
  writeFileSync(join(PORTFOLIO, `landing-${SLUG}-m.png`), m);
  console.log('Copied to', PORTFOLIO, d.length, m.length);
}

main().catch((e) => { console.error(e); process.exit(1); });