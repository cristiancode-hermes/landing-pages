// SALINA capture — desktop + mobile (hero viewports, fresh browser per page)
const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const URL = 'http://127.0.0.1:9877/2026-08-25-salina.html';
const OUT = '/opt/data/landing-pages/screenshots';
const CHROME = '/opt/data/chrome-linux64/chrome';
const SLUG = 'salina';

async function forceLight(page) {
  await page.evaluate(() => {
    localStorage.setItem('kairos-theme', 'light');
    document.documentElement.setAttribute('data-theme', 'light');
  });
  await page.evaluate(() => document.fonts.ready);
  await new Promise(r => setTimeout(r, 2200));
}

async function measureHero(page, fallback) {
  return await page.evaluate((fb) => {
    window.scrollTo(0, 0);
    const sec = document.getElementById('hero') || document.querySelector('.hero');
    return sec ? Math.ceil(sec.getBoundingClientRect().height) : fb;
  }, fallback);
}

async function desktop() {
  const browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu', '--disable-crashpad-forwarding']
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 900 }); // tall first for stable vh
  await page.goto(URL, { waitUntil: 'networkidle0', timeout: 30000 });
  await forceLight(page);
  const h = await measureHero(page, 800);
  await page.setViewport({ width: 1280, height: Math.min(h, 900) });
  await new Promise(r => setTimeout(r, 900));
  const out = path.join(OUT, `${SLUG}-desktop.png`);
  await page.screenshot({ path: out, fullPage: false });
  await browser.close();
  console.log('desktop hero h=', h, '->', out, fs.statSync(out).size, 'bytes');
}

async function mobile() {
  const browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu', '--disable-crashpad-forwarding']
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 390, height: 1500 }); // tall: vh paddings at final value
  await page.goto(URL, { waitUntil: 'networkidle0', timeout: 30000 });
  await forceLight(page);
  const h = await measureHero(page, 844);
  await page.setViewport({ width: 390, height: Math.min(h, 1200) });
  await new Promise(r => setTimeout(r, 900));
  const out = path.join(OUT, `${SLUG}-mobile.png`);
  await page.screenshot({ path: out, fullPage: false });
  await browser.close();
  console.log('mobile hero h=', h, '->', out, fs.statSync(out).size, 'bytes');
}

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  await desktop();
  await mobile();
  console.log('DONE');
})().catch(e => { console.error(e); process.exit(1); });