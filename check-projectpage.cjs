// Final visual check — portfolio project page for SALINA
const puppeteer = require('puppeteer');
const CHROME = '/opt/data/chrome-linux64/chrome';
const fs = require('fs');

(async () => {
  const browser = await puppeteer.launch({
    executablePath: CHROME, headless: true,
    args: ['--no-sandbox','--disable-setuid-sandbox','--disable-gpu','--disable-crashpad-forwarding']
  });
  const page = await browser.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  page.on('console', m => { if (m.type()==='error') errors.push(m.text()); });
  await page.setViewport({ width: 1280, height: 900 });
  await page.goto('https://cristiancode.dev/project/landing-2026-08-25-salina', { waitUntil: 'networkidle0', timeout: 45000 });
  await new Promise(r => setTimeout(r, 2500));
  const info = await page.evaluate(() => ({
    title: document.title,
    h1: (document.querySelector('h1')||{}).textContent || '',
    imgs: Array.from(document.querySelectorAll('img')).map(i => ({ src: i.src.slice(0,60), w: i.naturalWidth })),
    broken: Array.from(document.querySelectorAll('img')).filter(i => i.naturalWidth === 0).length,
    txt: document.body.innerText.slice(0, 300).replace(/\s+/g,' '),
  }));
  console.log('TITLE:', info.title);
  console.log('H1:', info.h1.slice(0,80));
  console.log('IMAGES:', JSON.stringify(info.imgs));
  console.log('BROKEN:', info.broken);
  console.log('TEXT:', info.txt.slice(0,200));
  console.log('ERRORS:', errors.length ? errors.join(' | ') : 'none');
  await page.screenshot({ path: '/opt/data/landing-pages/screenshots/salina-projectpage.png', fullPage: false });
  console.log('SHOT:', fs.statSync('/opt/data/landing-pages/screenshots/salina-projectpage.png').size, 'bytes');
  await browser.close();
})();