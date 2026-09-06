/**
 * capture-static.mjs — Hero viewport screenshots for STATIC landing page.
 * Follows the required procedure: viewport 1280x800 (desktop) / 390x844 (mobile),
 * force light mode via localStorage key 'kairos-theme', fullPage: false.
 */
import puppeteer from '/opt/data/portafolio/node_modules/puppeteer/lib/puppeteer/puppeteer.js';
import { statSync } from 'fs';

const CHROME_PATH = '/opt/data/profiles/ux-ui-designer/home/.cache/puppeteer/chrome/linux-150.0.7871.24/chrome-linux64/chrome';
const URL = 'http://localhost:9877/2026-08-01-static-records.html';
const OUT_DIR = '/opt/data/landing-pages/screenshots';

async function capture(page, viewport, outPath) {
  await page.setViewport(viewport);
  await page.goto(URL, { waitUntil: 'networkidle0', timeout: 45000 });

  // CRITICAL: force light mode — page JS reads localStorage key 'kairos-theme'
  await page.evaluate(() => {
    localStorage.setItem('kairos-theme', 'light');
    document.documentElement.setAttribute('data-theme', 'light');
  });

  // Also force English language for consistent screenshots
  await page.evaluate(() => {
    localStorage.setItem('static-lang', 'en');
    location.reload();
  });
  await new Promise(r => setTimeout(r, 800));
  await page.evaluate(() => document.fonts.ready);
  await new Promise(r => setTimeout(r, 2000));

  await page.screenshot({ path: outPath, fullPage: false });
  const size = (statSync(outPath).size / 1024).toFixed(0);
  console.log(`  ${outPath.split('/').pop()} → ${size}KB`);
  return size;
}

async function main() {
  console.log('Launching Chrome...');
  const browser = await puppeteer.launch({
    headless: true,
    executablePath: CHROME_PATH,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu', '--disable-crashpad-forwarding'],
  });

  const desktop = await browser.newPage();
  await capture(desktop, { width: 1280, height: 800 }, `${OUT_DIR}/static-desktop.png`);
  await desktop.close();

  const mobile = await browser.newPage();
  await capture(mobile, { width: 390, height: 844 }, `${OUT_DIR}/static-mobile.png`);
  await mobile.close();

  await browser.close();
  console.log('Done.');
}

main().catch(e => { console.error(e); process.exit(1); });
