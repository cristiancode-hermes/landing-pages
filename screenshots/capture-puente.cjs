const puppeteer = require('puppeteer');
const { writeFileSync, mkdirSync, readFileSync, statSync } = require('fs');
const { join } = require('path');

const SLUG = '2026-08-30-puente';
const PAGE_FILE = '2026-08-30-puente.html';
const URL = `http://127.0.0.1:9877/${PAGE_FILE}`;
const OUT_DIR = '/opt/data/landing-pages/screenshots';
const PORTFOLIO = '/opt/data/portafolio/public/assets';
mkdirSync(OUT_DIR, { recursive: true });

const CHROME = '/opt/data/chrome-linux64/chrome';

async function seed(page) {
  await page.evaluateOnNewDocument(() => {
    localStorage.setItem('kairos-theme', 'light');
    localStorage.setItem('puente-lang', 'es');
    localStorage.setItem('puente-cookie', '1');
    document.documentElement.setAttribute('data-theme', 'light');
  });
}

async function afterLoad(page) {
  await page.evaluate(() => {
    localStorage.setItem('kairos-theme', 'light');
    localStorage.setItem('puente-lang', 'es');
    localStorage.setItem('puente-cookie', '1');
    document.documentElement.setAttribute('data-theme', 'light');
    const b = document.getElementById('cookieBanner');
    if (b) { b.classList.remove('show'); b.style.display = 'none'; }
    document.querySelectorAll('.rv').forEach((el) => el.classList.add('in'));
  });
  await page.evaluate(() => document.fonts.ready);
  await new Promise((r) => setTimeout(r, 2000));
  await page.evaluate(() => window.scrollTo({ top: 0, behavior: 'instant' }));
  await new Promise((r) => setTimeout(r, 400));
}

async function launch() {
  return puppeteer.launch({
    executablePath: CHROME,
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu', '--disable-crashpad-forwarding'],
  });
}

(async () => {
  let browser = await launch();
  let page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 800 });
  await seed(page);
  await page.goto(URL, { waitUntil: 'networkidle0', timeout: 45000 });
  await afterLoad(page);
  const desktopPath = join(OUT_DIR, `${SLUG}-desktop.png`);
  await page.screenshot({ path: desktopPath, fullPage: false });
  console.log('Desktop', (statSync(desktopPath).size / 1024).toFixed(1) + 'KB', desktopPath);
  await browser.close();

  browser = await launch();
  page = await browser.newPage();
  await page.setViewport({ width: 390, height: 1500 });
  await seed(page);
  await page.goto(URL, { waitUntil: 'networkidle0', timeout: 45000 });
  await afterLoad(page);
  const dims = await page.evaluate(() => {
    const hero = document.getElementById('hero');
    const nav = document.querySelector('.nav');
    const heroH = hero ? Math.ceil(hero.getBoundingClientRect().height) : 844;
    const navH = nav ? Math.ceil(nav.getBoundingClientRect().height) : 64;
    return { heroH, navH };
  });
  const h = Math.min(dims.navH + dims.heroH, 1200);
  console.log('mobile measure', dims, 'viewportH', h);
  await page.setViewport({ width: 390, height: h });
  await new Promise((r) => setTimeout(r, 800));
  await page.evaluate(() => window.scrollTo({ top: 0, behavior: 'instant' }));
  const mobilePath = join(OUT_DIR, `${SLUG}-mobile.png`);
  await page.screenshot({ path: mobilePath, fullPage: false });
  console.log('Mobile', (statSync(mobilePath).size / 1024).toFixed(1) + 'KB', mobilePath);
  await browser.close();

  writeFileSync(join(PORTFOLIO, `landing-${SLUG}.png`), readFileSync(desktopPath));
  writeFileSync(join(PORTFOLIO, `landing-${SLUG}-m.png`), readFileSync(mobilePath));
  console.log('copied to portfolio public/assets');
})().catch((e) => { console.error(e); process.exit(1); });
