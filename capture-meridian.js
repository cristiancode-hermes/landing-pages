const puppeteer = require('puppeteer');

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

(async () => {
  const url = 'http://localhost:9877/landings/2026-07-27-meridian.html';
  const slug = 'landing-meridian';

  const browser = await puppeteer.launch({ 
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
    headless: 'new'
  });

  // Desktop screenshot
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 800 });
  await page.goto(url, { waitUntil: 'networkidle0', timeout: 30000 });
  await sleep(1500);
  await page.screenshot({
    path: `/opt/data/portafolio/public/assets/${slug}.png`,
    fullPage: true
  });
  console.log(`Desktop: /opt/data/portafolio/public/assets/${slug}.png`);

  // Mobile screenshot
  await page.setViewport({ width: 390, height: 844 });
  await page.goto(url, { waitUntil: 'networkidle0', timeout: 30000 });
  await sleep(1500);
  await page.screenshot({
    path: `/opt/data/portafolio/public/assets/${slug}-m.png`,
    fullPage: true
  });
  console.log(`Mobile: /opt/data/portafolio/public/assets/${slug}-m.png`);

  await browser.close();
  console.log('Done!');
})().catch(err => { console.error(err); process.exit(1); });
