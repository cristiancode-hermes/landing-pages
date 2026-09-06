import puppeteer from 'puppeteer';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function capture() {
  const url = 'http://localhost:9877/2026-07-29-passage-travel.html';
  const outDir = path.join(__dirname, 'screenshots');

  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });

  try {
    // Desktop screenshot (hero only, not fullPage)
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 800 });

    // Force light mode
    await page.goto(url, { waitUntil: 'networkidle0' });
    await page.evaluate(() => {
      localStorage.setItem('kairos-theme', 'light');
      document.documentElement.setAttribute('data-theme', 'light');
    });
    await page.evaluate(() => document.fonts.ready);
    await new Promise(r => setTimeout(r, 2000));

    const desktopPath = path.join(outDir, 'passage-desktop.png');
    await page.screenshot({ path: desktopPath, fullPage: false });
    console.log(`Desktop hero screenshot saved: ${desktopPath}`);

    // Mobile screenshot
    const pageMobile = await browser.newPage();
    await pageMobile.setViewport({ width: 390, height: 844 });
    await pageMobile.goto(url, { waitUntil: 'networkidle0' });
    await pageMobile.evaluate(() => {
      localStorage.setItem('kairos-theme', 'light');
      document.documentElement.setAttribute('data-theme', 'light');
    });
    await pageMobile.evaluate(() => document.fonts.ready);
    await new Promise(r => setTimeout(r, 2000));

    const mobilePath = path.join(outDir, 'passage-mobile.png');
    await pageMobile.screenshot({ path: mobilePath, fullPage: false });
    console.log(`Mobile hero screenshot saved: ${mobilePath}`);

    await browser.close();

    // Check sizes
    const fs = await import('fs');
    const desktopSize = fs.statSync(desktopPath).size;
    const mobileSize = fs.statSync(mobilePath).size;
    console.log(`\nScreenshot sizes:`);
    console.log(`  Desktop: ${(desktopSize / 1024).toFixed(1)} KB ${desktopSize > 18000 && desktopSize < 900000 ? '✓ VALID' : '✗ SUSPICIOUS'}`);
    console.log(`  Mobile:  ${(mobileSize / 1024).toFixed(1)} KB ${mobileSize > 18000 && mobileSize < 900000 ? '✓ VALID' : '✗ SUSPICIOUS'}`);

  } catch(err) {
    console.error('Capture failed:', err);
    await browser.close().catch(() => {});
  }
}

capture();
