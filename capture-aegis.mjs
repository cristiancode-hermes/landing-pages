/**
 * capture-aegis.mjs — Hero viewport screenshots for Aegis landing page.
 * Required procedure: viewport 1280x800 (desktop) / 390x844 (mobile),
 * force light mode via localStorage key 'kairos-theme', fullPage: false.
 */
import puppeteer from '/opt/data/portafolio/node_modules/puppeteer/lib/puppeteer/puppeteer.js';
import { statSync } from 'fs';

const CHROME_PATH = '/opt/data/profiles/ux-ui-designer/home/.cache/puppeteer/chrome/linux-150.0.7871.24/chrome-linux64/chrome';
const URL = 'http://127.0.0.1:9877/2026-08-02-aegis-vault.html';
const OUT_DIR = '/opt/data/landing-pages/screenshots';

async function capture(page, viewport, outPath) {
  await page.setViewport(viewport);
  await page.goto(URL, { waitUntil: 'networkidle0', timeout: 45000 });

  // CRITICAL: force light mode — page JS reads localStorage key 'kairos-theme'
  await page.evaluate(() => {
    localStorage.setItem('kairos-theme', 'light');
    document.documentElement.setAttribute('data-theme', 'light');
  });

  // Force English language for consistent screenshots
  await page.evaluate(() => {
    localStorage.setItem('aegis-lang', 'en');
    location.reload();
  });
  await new Promise(r => setTimeout(r, 800));
  await page.evaluate(() => document.fonts.ready);
  await new Promise(r => setTimeout(r, 2000));

  // ❌ Do NOT use fullPage: true — captures only visible viewport (hero section)
  await page.screenshot({ path: outPath, fullPage: false });
  const size = (statSync(outPath).size / 1024).toFixed(0);
  console.log(`  ${outPath.split('/').pop()} → ${size}KB`);
  return size;
}

async function main() {
  console.log('Launching Chrome...');
  const browser = await puppeteer.launch({
    headless: 'new',
    executablePath: CHROME_PATH,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--force-color-profile=srgb']
  });

  const page = await browser.newPage();

  console.log('Desktop capture (1280x800)...');
  await capture(page, { width: 1280, height: 800 }, `${OUT_DIR}/aegis-desktop.png`);

  console.log('Mobile capture (390x844)...');
  await capture(page, { width: 390, height: 844 }, `${OUT_DIR}/aegis-mobile.png`);

  await browser.close();
  console.log('Done.');
}

main().catch(e => { console.error(e); process.exit(1); });
