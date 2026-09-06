const puppeteer = require('/opt/data/node_modules/puppeteer');

// Páginas afectadas: 6 transformadas + tanda (mobile row)
const pages = [
  { file: '2026-07-29-passage-travel.html', slug: 'passage-travel' },
  { file: '2026-07-30-aura-fashion.html', slug: 'aura-fashion' },
  { file: '2026-08-01-static-records.html', slug: 'static-records' },
  { file: '2026-08-04-pulse-health.html', slug: 'pulse-health' },
  { file: '2026-08-05-atrium-studio.html', slug: 'atrium-studio' },
  { file: '2026-08-12-tanda-savings.html', slug: 'tanda-savings' },
  { file: '2026-08-13-lyra-dynamics.html', slug: '2026-08-13-lyra-dynamics' },
];

const OUT = '/opt/data/portafolio/public/assets';
const BASE = 'http://127.0.0.1:9877';

async function capture(browser, url, viewport) {
  const page = await browser.newPage();
  await page.setViewport(viewport);
  await page.goto(url, { waitUntil: 'networkidle0', timeout: 30000 });
  await page.evaluate(() => {
    ['theme', 'kairos-theme', 'darkMode', 'aura-theme'].forEach(k => localStorage.removeItem(k));
    localStorage.setItem('kairos-theme', 'light');
    document.documentElement.setAttribute('data-theme', 'light');
  });
  await page.evaluate(() => document.fonts.ready);
  await new Promise(r => setTimeout(r, 2000));
  // cerrar cookie banner si existe (evitar que salga en la captura)
  const closed = await page.evaluate(() => {
    const banners = document.querySelectorAll('[class*="cookie"], [id*="cookie"], [class*="Cookie"]');
    let n = 0;
    banners.forEach(b => {
      if (b.offsetWidth > 0 && b.offsetHeight > 0) {
        const accept = b.querySelector('button');
        if (accept) { accept.click(); n++; }
      }
    });
    return n;
  });
  await new Promise(r => setTimeout(r, 800));
  const shot = await page.screenshot({ fullPage: false });
  await page.close();
  return { shot, cookiesClosed: closed };
}

(async () => {
  for (const p of pages) {
    const url = `${BASE}/${p.file}`;
    const outD = `${OUT}/landing-${p.slug}.png`;
    const outM = `${OUT}/landing-${p.slug}-m.png`;

    // Desktop — browser fresco por página
    const b1 = await puppeteer.launch({
      executablePath: '/opt/data/chrome-linux64/chrome',
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu', '--disable-crashpad-forwarding'],
    });
    try {
      const r1 = await capture(b1, url, { width: 1280, height: 800 });
      require('fs').writeFileSync(outD, r1.shot);
      console.log(`DESKTOP ${p.slug}: ${r1.shot.length} bytes (cookies=${r1.cookiesClosed})`);
    } finally { await b1.close(); }

    // Mobile — browser fresco
    const b2 = await puppeteer.launch({
      executablePath: '/opt/data/chrome-linux64/chrome',
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu', '--disable-crashpad-forwarding'],
    });
    try {
      const r2 = await capture(b2, url, { width: 390, height: 844 });
      require('fs').writeFileSync(outM, r2.shot);
      console.log(`MOBILE  ${p.slug}: ${r2.shot.length} bytes (cookies=${r2.cookiesClosed})`);
    } finally { await b2.close(); }
  }
  console.log('DONE');
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });
