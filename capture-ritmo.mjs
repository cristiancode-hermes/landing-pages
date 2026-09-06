import puppeteer from 'puppeteer';
import { writeFileSync, mkdirSync, readFileSync, statSync } from 'fs';
import { join } from 'path';

const URL = 'http://localhost:9877/2026-08-10-ritmo-fitness.html';
const OUT_DIR = '/opt/data/landing-pages/screenshots';
const PORTFOLIO_ASSETS = '/opt/data/portafolio/public/assets';

mkdirSync(OUT_DIR, { recursive: true });

async function capture() {
  const browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox'] });
  const page = await browser.newPage();

  // Desktop
  await page.setViewport({ width: 1280, height: 800 });
  await page.goto(URL, { waitUntil: 'networkidle0', timeout: 20000 });
  await page.evaluate(() => {
    localStorage.setItem('ritmo-lang', 'en');
    localStorage.setItem('ritmo-cookie', 'accepted');
    localStorage.setItem('kairos-theme', 'light');
    document.documentElement.setAttribute('data-theme', 'light');
  });
  await page.evaluate(() => document.fonts.ready);
  await new Promise(r => setTimeout(r, 2200));
  const desktopPath = join(OUT_DIR, 'ritmo-desktop.png');
  await page.screenshot({ path: desktopPath, fullPage: false });
  console.log('Desktop:', desktopPath, (statSync(desktopPath).size / 1024).toFixed(1) + 'KB');

  // Copy to portfolio
  try {
    const portfolioPath = join(PORTFOLIO_ASSETS, 'landing-ritmo-fitness.png');
    writeFileSync(portfolioPath, readFileSync(desktopPath));
    console.log('Copied to portfolio:', portfolioPath);
  } catch (e) {
    console.log('Portfolio copy skipped:', e.message);
  }

  // Mobile
  await page.setViewport({ width: 390, height: 844 });
  await page.goto(URL, { waitUntil: 'networkidle0', timeout: 20000 });
  await page.evaluate(() => {
    localStorage.setItem('ritmo-lang', 'en');
    localStorage.setItem('ritmo-cookie', 'accepted');
    localStorage.setItem('kairos-theme', 'light');
    document.documentElement.setAttribute('data-theme', 'light');
  });
  await page.evaluate(() => document.fonts.ready);
  await new Promise(r => setTimeout(r, 2200));
  const mobilePath = join(OUT_DIR, 'ritmo-mobile.png');
  await page.screenshot({ path: mobilePath, fullPage: false });
  console.log('Mobile:', mobilePath, (statSync(mobilePath).size / 1024).toFixed(1) + 'KB');

  await browser.close();
}

capture().catch(e => { console.error(e); process.exit(1); });
