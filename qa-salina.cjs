// SALINA functional QA via Puppeteer (console errors, i18n, theme, interactions)
const puppeteer = require('puppeteer');
const CHROME = '/opt/data/chrome-linux64/chrome';
const URL = 'http://127.0.0.1:9877/2026-08-25-salina.html';

(async () => {
  const browser = await puppeteer.launch({
    executablePath: CHROME, headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu', '--disable-crashpad-forwarding']
  });
  const page = await browser.newPage();
  const errors = [];
  page.on('console', m => { if (m.type() === 'error') errors.push('console: ' + m.text()); });
  page.on('pageerror', e => errors.push('pageerror: ' + e.message));
  await page.setViewport({ width: 1280, height: 900 });
  await page.goto(URL, { waitUntil: 'networkidle0', timeout: 30000 });
  await page.evaluate(() => { localStorage.setItem('kairos-theme', 'light'); document.documentElement.setAttribute('data-theme','light'); });
  await page.evaluate(() => document.fonts.ready);
  await new Promise(r => setTimeout(r, 2200));

  const counts = await page.evaluate(() => ({
    listings: document.querySelectorAll('.listing').length,
    faq: document.querySelectorAll('.faq-item').length,
    wish: document.querySelectorAll('.wish').length,
    langSel: document.querySelectorAll('.lang-select').length,
    themeToggles: document.querySelectorAll('#themeToggle').length,
    broken: Array.from(document.querySelectorAll('img')).filter(i => i.naturalWidth === 0).map(i => i.src.slice(0, 70)),
  }));
  console.log('COUNTS', JSON.stringify(counts));
  console.log('lang', await page.evaluate(() => document.documentElement.lang),
              '| theme', await page.evaluate(() => document.documentElement.getAttribute('data-theme')));

  // language switch to EN
  await page.evaluate(() => { document.querySelector('#langSel .lang-select__btn').click(); });
  await new Promise(r => setTimeout(r, 300));
  await page.evaluate(() => { document.querySelector('#langMenu .lang-select__opt[data-lang="en"]').click(); });
  await new Promise(r => setTimeout(r, 700));
  console.log('EN h1:', await page.evaluate(() => document.querySelector('#hero-title').textContent.replace(/\s+/g,' ').slice(0, 70)));
  console.log('EN meta:', await page.evaluate(() => document.querySelector('#meta-desc').getAttribute('content').slice(0, 60)));

  // switch to DE (apostrophe-heavy none; check no raw keys visible)
  await page.evaluate(() => { document.querySelector('#langSel .lang-select__btn').click(); });
  await new Promise(r => setTimeout(r, 250));
  await page.evaluate(() => { document.querySelector('#langMenu .lang-select__opt[data-lang="de"]').click(); });
  await new Promise(r => setTimeout(r, 700));
  const rawKeys = await page.evaluate(() => Array.from(document.querySelectorAll('[data-i18n]')).filter(el => el.textContent.startsWith('nav.') || el.textContent.startsWith('hero.')).length);
  console.log('DE raw keys leaked:', rawKeys);

  // theme toggle
  const t0 = await page.evaluate(() => document.documentElement.getAttribute('data-theme'));
  await page.evaluate(() => document.querySelector('#themeToggle').click());
  await new Promise(r => setTimeout(r, 500));
  const t1 = await page.evaluate(() => document.documentElement.getAttribute('data-theme'));
  console.log('THEME', t0, '->', t1);

  // dark-mode CTA contrast check (btn-red text vs bg)
  const ctaDark = await page.evaluate(() => {
    const b = document.querySelector('.hero-cta .btn-red');
    const cs = getComputedStyle(b);
    return { color: cs.color, bg: cs.backgroundColor, text: b.textContent.trim() };
  });
  console.log('CTA dark mode computed:', JSON.stringify(ctaDark));

  // FAQ open
  await page.evaluate(() => document.querySelectorAll('.faq-q')[0].click());
  await new Promise(r => setTimeout(r, 400));
  console.log('FAQ open:', await page.evaluate(() => document.querySelectorAll('.faq-item')[0].classList.contains('open')));

  // wish + qty
  await page.evaluate(() => document.querySelectorAll('.wish')[0].click());
  console.log('WISH active:', await page.evaluate(() => document.querySelectorAll('.wish')[0].classList.contains('active')));
  await page.evaluate(() => { document.querySelectorAll('.qty button[data-step="1"]')[0].click(); document.querySelectorAll('.qty button[data-step="1"]')[0].click(); });
  console.log('QTY:', await page.evaluate(() => document.querySelectorAll('.qty input')[0].value));

  // cookie banner
  await page.evaluate(() => { localStorage.removeItem('salina-cookie'); const c = document.querySelector('#cookieBanner'); if (c) c.classList.add('show'); });
  await new Promise(r => setTimeout(r, 400));
  const cRect = await page.evaluate(() => { const c = document.querySelector('#cookieBanner'); const r = c.getBoundingClientRect(); return { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) }; });
  const ctaRect = await page.evaluate(() => { const a = document.querySelector('.hero-cta a.btn-red'); const r = a.getBoundingClientRect(); return { y: Math.round(r.y), h: Math.round(r.height) }; });
  console.log('COOKIE rect:', JSON.stringify(cRect), '| hero CTA rect:', JSON.stringify(ctaRect));
  console.log('COOKIE overlaps CTA:', cRect.y < ctaRect.y + ctaRect.h && cRect.y + cRect.h > ctaRect.y);

  // mobile menu
  await page.evaluate(() => document.querySelector('#burger').click());
  await new Promise(r => setTimeout(r, 400));
  console.log('MOBILE MENU open:', await page.evaluate(() => document.querySelector('#mobileMenu').classList.contains('open')));
  await page.evaluate(() => document.querySelector('#menuClose').click());
  await new Promise(r => setTimeout(r, 300));

  // newsletter honest submit
  await page.evaluate(() => { const i = document.querySelector('#newsEmail'); i.value = 'qa@salinas.es'; });
  await page.evaluate(() => document.querySelector('#newsForm').dispatchEvent(new Event('submit', { cancelable: true })));
  await new Promise(r => setTimeout(r, 400));
  console.log('NEWS msg:', await page.evaluate(() => document.querySelector('#nlMsg').textContent.slice(0, 60)));

  console.log('ERRORS:', errors.length ? errors.join(' | ') : 'none');
  await browser.close();
})();