/**
 * capture-hero-screenshots.mjs — Viewport hero screenshots, forced light mode.
 */
import puppeteer from '/opt/data/portafolio/node_modules/puppeteer/lib/puppeteer/puppeteer.js';
import { statSync } from 'fs';

const CHROME_PATH = '/opt/data/profiles/ux-ui-designer/home/.cache/puppeteer/chrome/linux-150.0.7871.24/chrome-linux64/chrome';
const BASE_URL = 'http://localhost:9877';
const ASSETS_DIR = '/opt/data/portafolio/public/assets';

const PAGES = [
  { file: '2026-07-23-forma-and-space.html', slug: 'landing-forma-and-space' },
  { file: '2026-07-23-nexus-gaming.html', slug: 'landing-nexus-gaming' },
  { file: '2026-07-24-kairos-academy.html', slug: 'landing-kairos-academy' },
  { file: '2026-07-25-ora-wellness.html', slug: 'landing-ora-wellness' },
  { file: '2026-07-26-ember-and-vine.html', slug: 'landing-ember-and-vine' },
  { file: '2026-07-26-northbound-outdoors.html', slug: 'landing-northbound-outdoors' },
  { file: '2026-07-27-veridian-carbon.html', slug: 'landing-veridian-carbon' },
  { file: '2026-07-27-meridian.html', slug: 'landing-meridian' },
  { file: '2026-07-27-lumin-platform.html', slug: 'landing-lumin-platform' },
];

async function captureLanding(browser, pageInfo, isMobile) {
  const page = await browser.newPage();
  const url = `${BASE_URL}/${pageInfo.file}`;

  try {
    // Set viewport BEFORE navigation for proper mobile/desktop rendering
    const width = isMobile ? 390 : 1280;
    const height = isMobile ? 844 : 800;
    await page.setViewport({ width, height });

    await page.goto(url, { waitUntil: 'networkidle0', timeout: 30000 });

    // Force light mode by clearing localStorage theme preference
    // and explicitly setting data-theme to light
    await page.evaluate(() => {
      localStorage.removeItem('theme');
      localStorage.setItem('theme', 'light');
      document.documentElement.setAttribute('data-theme', 'light');
    });

    // Also force the dark mode toggle to light if it exists
    await page.evaluate(() => {
      const toggle = document.querySelector('[data-theme-toggle], .theme-toggle, #theme-toggle');
      if (toggle) {
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        if (isDark) toggle.click();
      }
    });

    await page.evaluate(() => document.fonts.ready);
    await new Promise(r => setTimeout(r, 1500));

    const suffix = isMobile ? '-m.png' : '.png';
    const outPath = `${ASSETS_DIR}/${pageInfo.slug}${suffix}`;
    await page.screenshot({ path: outPath, fullPage: false });
    const size = (statSync(outPath).size / 1024).toFixed(0);
    await page.close();
    return size;
  } catch (err) {
    await page.close();
    throw err;
  }
}

async function main() {
  console.log('🚀 Launching Chrome...');
  const browser = await puppeteer.launch({
    headless: true,
    executablePath: CHROME_PATH,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu', '--disable-crashpad-forwarding'],
  });

  console.log(`📸 Capturing hero viewport for ${PAGES.length} landing pages...\n`);

  for (const p of PAGES) {
    process.stdout.write(`  ${p.file} → `);
    try {
      const deskSize = await captureLanding(browser, p, false);
      const mobSize = await captureLanding(browser, p, true);
      console.log(`✅ D:${deskSize}KB M:${mobSize}KB`);
    } catch (err) {
      console.log(`❌ ${err.message.slice(0, 80)}`);
    }
  }

  await browser.close();
  console.log('\n✅ All hero screenshots captured!');
}

main().catch(e => { console.error(e); process.exit(1); });
