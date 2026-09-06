import puppeteer from 'puppeteer';
import { writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';

const URL = 'http://localhost:9877/2026-08-07-paideia-academy.html';
const OUT_DIR = '/opt/data/landing-pages/screenshots';
const PORTFOLIO_ASSETS = '/opt/data/portafolio/public/assets';

mkdirSync(OUT_DIR, { recursive: true });

async function capture() {
  const browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox'] });
  const page = await browser.newPage();

  // Desktop
  await page.setViewport({ width: 1280, height: 800 });
  await page.goto(URL, { waitUntil: 'networkidle0', timeout: 15000 });
  // Force light mode
  await page.evaluate(() => {
    localStorage.setItem('paideia-lang', 'en');
    localStorage.setItem('paideia-cookie', 'accepted');
    document.documentElement.setAttribute('data-theme', 'light');
  });
  await page.evaluate(() => document.fonts.ready);
  await new Promise(r => setTimeout(r, 2000));
  const desktopPath = join(OUT_DIR, 'paideia-desktop.png');
  await page.screenshot({ path: desktopPath, fullPage: false });
  console.log('Desktop:', desktopPath, `${(await (await import('fs')).statSync(desktopPath).size / 1024).toFixed(1)}KB`);

  // Copy to portfolio if available
  try {
    const portfolioPath = join(PORTFOLIO_ASSETS, 'landing-paideia-academy.png');
    writeFileSync(portfolioPath, (await (await import('fs')).readFileSync(desktopPath)));
    console.log('Copied to portfolio:', portfolioPath);
  } catch (e) {
    console.log('Portfolio copy skipped:', e.message);
  }

  // Mobile
  await page.setViewport({ width: 390, height: 844 });
  await page.goto(URL, { waitUntil: 'networkidle0', timeout: 15000 });
  await page.evaluate(() => {
    localStorage.setItem('paideia-lang', 'en');
    localStorage.setItem('paideia-cookie', 'accepted');
  });
  await page.evaluate(() => document.fonts.ready);
  await new Promise(r => setTimeout(r, 2000));
  const mobilePath = join(OUT_DIR, 'paideia-mobile.png');
  await page.screenshot({ path: mobilePath, fullPage: false });
  console.log('Mobile:', mobilePath, `${(await (await import('fs')).statSync(mobilePath).size / 1024).toFixed(1)}KB`);

  await browser.close();
}

capture().catch(console.error);
