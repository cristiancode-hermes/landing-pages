/**
 * capture-screenshots.mjs — Captura screenshots de todas las landing pages mejoradas.
 */
import puppeteer from '/opt/data/portafolio/node_modules/puppeteer/lib/puppeteer/puppeteer.js';
import { statSync } from 'fs';

const CHROME_PATH = '/opt/data/profiles/ux-ui-designer/home/.cache/puppeteer/chrome/linux-150.0.7871.24/chrome-linux64/chrome';
const BASE_URL = 'http://localhost:9876';
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

async function main() {
  console.log('🚀 Launching Chrome...');
  const browser = await puppeteer.launch({
    headless: true,
    executablePath: CHROME_PATH,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu', '--disable-crashpad-forwarding'],
  });

  console.log(`📸 Capturing ${PAGES.length} landing pages...\n`);

  for (const p of PAGES) {
    const page = await browser.newPage();
    const url = `${BASE_URL}/${p.file}`;
    process.stdout.write(`  ${p.file} → `);
    try {
      await page.goto(url, { waitUntil: 'networkidle0', timeout: 25000 });
      await new Promise(r => setTimeout(r, 1500));

      // Desktop
      await page.setViewport({ width: 1280, height: 800 });
      const deskPath = `${ASSETS_DIR}/${p.slug}.png`;
      await page.screenshot({ path: deskPath, fullPage: true });

      // Mobile
      await page.setViewport({ width: 390, height: 844 });
      await new Promise(r => setTimeout(r, 1000));
      const mobPath = `${ASSETS_DIR}/${p.slug}-m.png`;
      await page.screenshot({ path: mobPath, fullPage: true });

      const dSize = statSync(deskPath).size;
      const mSize = statSync(mobPath).size;
      console.log(`✅ D:${(dSize/1024).toFixed(0)}KB M:${(mSize/1024).toFixed(0)}KB`);
    } catch (err) {
      console.log(`❌ ${err.message.slice(0, 60)}`);
    } finally {
      await page.close();
    }
  }

  await browser.close();
  console.log('\n✅ All screenshots captured!');
}

main().catch(e => { console.error(e); process.exit(1); });
