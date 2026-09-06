import puppeteer from 'puppeteer';
import { writeFileSync, mkdirSync, readFileSync, statSync } from 'fs';
import { join } from 'path';

const URL = 'http://localhost:9877/2026-08-11-aether-motors.html';
const OUT_DIR = '/opt/data/landing-pages/screenshots';
const PORTFOLIO_ASSETS = '/opt/data/portafolio/public/assets';

mkdirSync(OUT_DIR, { recursive: true });

async function capture() {
  const browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox'] });

  // Desktop
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 800 });
  await page.goto(URL, { waitUntil: 'networkidle0', timeout: 20000 });
  await page.evaluate(() => {
    localStorage.setItem('aether-lang', 'en');
    localStorage.setItem('aether-cookie', 'accepted');
    localStorage.setItem('kairos-theme', 'light');
  });
  await page.reload({ waitUntil: 'networkidle0', timeout: 20000 });
  await page.evaluate(() => {
    document.documentElement.setAttribute('data-theme', 'light');
  });
  await page.evaluate(() => document.fonts.ready);
  await new Promise(r => setTimeout(r, 2500));
  const desktopPath = join(OUT_DIR, 'aether-desktop.png');
  await page.screenshot({ path: desktopPath, fullPage: false });
  console.log('Desktop:', desktopPath, (statSync(desktopPath).size / 1024).toFixed(1) + 'KB');
  await page.close();

  // Portfolio copy
  try {
    const portfolioPath = join(PORTFOLIO_ASSETS, 'landing-aether-motors.png');
    writeFileSync(portfolioPath, readFileSync(desktopPath));
    console.log('Copied to portfolio:', portfolioPath);
  } catch (e) {
    console.log('Portfolio copy skipped:', e.message);
  }

  // Mobile
  const page2 = await browser.newPage();
  await page2.setViewport({ width: 390, height: 844 });
  await page2.goto(URL, { waitUntil: 'networkidle0', timeout: 20000 });
  await page2.evaluate(() => {
    localStorage.setItem('aether-lang', 'en');
    localStorage.setItem('aether-cookie', 'accepted');
    localStorage.setItem('kairos-theme', 'light');
  });
  await page2.reload({ waitUntil: 'networkidle0', timeout: 20000 });
  await page2.evaluate(() => {
    document.documentElement.setAttribute('data-theme', 'light');
  });
  await page2.evaluate(() => document.fonts.ready);
  await new Promise(r => setTimeout(r, 2500));
  const mobilePath = join(OUT_DIR, 'aether-mobile.png');
  await page2.screenshot({ path: mobilePath, fullPage: false });
  console.log('Mobile:', mobilePath, (statSync(mobilePath).size / 1024).toFixed(1) + 'KB');
  await page2.close();

  await browser.close();
}

capture().catch(e => { console.error(e); process.exit(1); });
