// Capture MORADA desktop + mobile screenshots — fresh browser per page (Impeccable pitfall)
const puppeteer = require('puppeteer');

const URL = 'http://127.0.0.1:9877/2026-08-16-morada.html';
const OUT_DIR = '/opt/data/landing-pages/screenshots';
const CHROME = '/opt/data/chrome-linux64/chrome';

async function prepPage(browser) {
  const page = await browser.newPage();
  // Set localStorage BEFORE page scripts run so the cookie timer never arms
  await page.evaluateOnNewDocument(() => {
    try {
      localStorage.setItem('kairos-theme', 'light');
      localStorage.setItem('morada-cookie', '1');
      localStorage.setItem('morada-lang', 'en');
    } catch (e) {}
  });
  await page.setViewport({ width: 1280, height: 800 });
  await page.goto(URL, { waitUntil: 'networkidle0', timeout: 30000 });
  await page.evaluate(() => {
    document.documentElement.setAttribute('data-theme', 'light');
    const cb = document.getElementById('cookieBanner');
    if (cb) { cb.classList.remove('show'); cb.style.display = 'none'; }
  });
  await page.evaluate(() => document.fonts.ready);
  await new Promise(r => setTimeout(r, 2000));
  return page;
}

async function triggerReveals(page) {
  await page.evaluate(async () => {
    const step = 300;
    for (let y = 0; y <= document.body.scrollHeight; y += step) {
      window.scrollTo(0, y);
      await new Promise(r => setTimeout(r, 180));
    }
    window.scrollTo(0, 0);
    await new Promise(r => setTimeout(r, 1200));
  });
}

async function captureDesktop() {
  const browser = await puppeteer.launch({
    executablePath: CHROME, headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu', '--disable-crashpad-forwarding'],
  });
  const page = await prepPage(browser);
  await triggerReveals(page);
  await page.screenshot({ path: OUT_DIR + '/morada-desktop.png', fullPage: false });
  console.log('desktop captured');
  await browser.close();
}

async function captureMobile() {
  const browser = await puppeteer.launch({
    executablePath: CHROME, headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu', '--disable-crashpad-forwarding'],
  });
  const page = await browser.newPage();
  await page.evaluateOnNewDocument(() => {
    try {
      localStorage.setItem('kairos-theme', 'light');
      localStorage.setItem('morada-cookie', '1');
      localStorage.setItem('morada-lang', 'en');
    } catch (e) {}
  });
  await page.setViewport({ width: 390, height: 844 });
  await page.goto(URL, { waitUntil: 'networkidle0', timeout: 30000 });
  await page.evaluate(() => {
    document.documentElement.setAttribute('data-theme', 'light');
    const cb = document.getElementById('cookieBanner');
    if (cb) { cb.classList.remove('show'); cb.style.display = 'none'; }
  });
  await page.evaluate(() => document.fonts.ready);
  await new Promise(r => setTimeout(r, 2000));
  await triggerReveals(page);
  // Measure hero with a TALL viewport so vh-based paddings are at final value
  await page.setViewport({ width: 390, height: 1500 });
  await new Promise(r => setTimeout(r, 400));
  const heroHeight = await page.evaluate(() => {
    window.scrollTo(0, 0);
    const hero = document.getElementById('hero');
    return hero ? Math.ceil(hero.getBoundingClientRect().height) : 844;
  });
  const navHeight = await page.evaluate(() => {
    const nav = document.querySelector('.nav');
    return nav ? Math.ceil(nav.getBoundingClientRect().height) : 64;
  });
  // Viewport must fit navbar + hero so the canvas bottom isn't clipped
  await page.setViewport({ width: 390, height: Math.min(navHeight + heroHeight, 1200) });
  await new Promise(r => setTimeout(r, 800));
  await page.screenshot({ path: OUT_DIR + '/morada-mobile.png', fullPage: false });
  console.log('mobile captured, hero height:', heroHeight, 'nav:', navHeight);
  await browser.close();
}

(async () => {
  await captureDesktop();
  await captureMobile();
  console.log('DONE');
})();