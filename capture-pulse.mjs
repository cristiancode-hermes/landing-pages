import puppeteer from 'puppeteer';

const URL = 'http://localhost:9877/2026-08-04-pulse-health.html';
const DESKTOP_OUT = '/opt/data/landing-pages/screenshots/pulse-desktop.png';
const MOBILE_OUT = '/opt/data/landing-pages/screenshots/pulse-mobile.png';

async function capture() {
  // Fresh browser per project
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  try {
    // Desktop capture
    const desktopPage = await browser.newPage();
    await desktopPage.setViewport({ width: 1280, height: 800 });
    await desktopPage.goto(URL, { waitUntil: 'networkidle0', timeout: 30000 });

    // Force light mode
    await desktopPage.evaluate(() => {
      localStorage.setItem('kairos-theme', 'light');
      document.documentElement.setAttribute('data-theme', 'light');
    });
    await desktopPage.evaluate(() => document.fonts.ready);
    await new Promise(r => setTimeout(r, 2000));

    await desktopPage.screenshot({ path: DESKTOP_OUT, fullPage: false });
    console.log('Desktop screenshot saved:', DESKTOP_OUT);
    await desktopPage.close();

    // Mobile capture
    const mobilePage = await browser.newPage();
    await mobilePage.setViewport({ width: 390, height: 844 });
    await mobilePage.goto(URL, { waitUntil: 'networkidle0', timeout: 30000 });

    await mobilePage.evaluate(() => {
      localStorage.setItem('kairos-theme', 'light');
      document.documentElement.setAttribute('data-theme', 'light');
    });
    await mobilePage.evaluate(() => document.fonts.ready);
    await new Promise(r => setTimeout(r, 2000));

    await mobilePage.screenshot({ path: MOBILE_OUT, fullPage: false });
    console.log('Mobile screenshot saved:', MOBILE_OUT);
    await mobilePage.close();

  } finally {
    await browser.close();
  }
}

capture().catch(err => {
  console.error('Capture failed:', err);
  process.exit(1);
});
