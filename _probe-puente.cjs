const puppeteer = require('/opt/data/node_modules/puppeteer');
const fs = require('fs');
const outDir = '/opt/data/landing-pages/_qa-puente';
fs.mkdirSync(outDir, { recursive: true });

(async () => {
  const browser = await puppeteer.launch({
    executablePath: '/opt/data/chrome-linux64/chrome',
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu', '--disable-crashpad-forwarding'],
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 800 });
  await page.evaluateOnNewDocument(() => {
    localStorage.setItem('kairos-theme', 'dark');
    localStorage.setItem('puente-lang', 'es');
    localStorage.setItem('puente-cookie', '1');
  });
  await page.goto('http://127.0.0.1:9877/2026-08-30-puente.html', { waitUntil: 'networkidle0' });
  await page.evaluate(() => {
    document.documentElement.setAttribute('data-theme', 'dark');
    localStorage.setItem('kairos-theme', 'dark');
  });
  await page.evaluate(() => document.fonts.ready);
  await new Promise((r) => setTimeout(r, 800));

  const probe = await page.evaluate(() => {
    const rgb = (c) => {
      const m = String(c).match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
      return m ? [+m[1], +m[2], +m[3]] : c;
    };
    const lum = ([r, g, b]) => {
      const s = [r, g, b].map((v) => {
        v /= 255;
        return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
      });
      return 0.2126 * s[0] + 0.7152 * s[1] + 0.0722 * s[2];
    };
    const ratio = (fg, bg) => {
      const L1 = lum(rgb(fg)), L2 = lum(rgb(bg));
      const hi = Math.max(L1, L2), lo = Math.min(L1, L2);
      return (hi + 0.05) / (lo + 0.05);
    };
    const info = (sel) => {
      const el = document.querySelector(sel);
      if (!el) return { sel, missing: true };
      const s = getComputedStyle(el);
      let node = el;
      let bg = s.backgroundColor;
      while (bg === 'rgba(0, 0, 0, 0)' && node.parentElement) {
        node = node.parentElement;
        bg = getComputedStyle(node).backgroundColor;
      }
      if (bg === 'rgba(0, 0, 0, 0)') bg = getComputedStyle(document.body).backgroundColor;
      return {
        sel,
        color: s.color,
        bg,
        text: (el.textContent || '').slice(0, 24),
        ratio: +ratio(s.color, bg).toFixed(2),
      };
    };
    const el = document.querySelector('.lang-select__opt[aria-selected="true"]');
    const after = el ? getComputedStyle(el, '::after') : null;
    const visit = document.getElementById('visitMail');
    return {
      theme: document.documentElement.getAttribute('data-theme'),
      tokens: {
        teal: getComputedStyle(document.documentElement).getPropertyValue('--teal').trim(),
        link: getComputedStyle(document.documentElement).getPropertyValue('--link').trim(),
        bg: getComputedStyle(document.documentElement).getPropertyValue('--bg').trim(),
        card: getComputedStyle(document.documentElement).getPropertyValue('--card').trim(),
      },
      fit: info('.fit-num'),
      faq: info('.faq-q .ic'),
      lang: info('.lang-select__opt[aria-selected="true"]'),
      after: after ? { content: after.content, color: after.color } : null,
      visitHref: visit && visit.getAttribute('href'),
    };
  });
  console.log('DARK_PROBE', JSON.stringify(probe, null, 2));

  await page.evaluate(() => {
    const el = document.querySelector('#ajuste');
    if (el) el.scrollIntoView({ block: 'start', behavior: 'instant' });
  });
  await new Promise((r) => setTimeout(r, 500));
  await page.screenshot({ path: outDir + '/dark-fit.png', fullPage: false });

  await page.evaluate(() => window.scrollTo({ top: 0, behavior: 'instant' }));
  await new Promise((r) => setTimeout(r, 200));
  await page.click('.lang-select__btn');
  await new Promise((r) => setTimeout(r, 300));
  await page.screenshot({ path: outDir + '/dark-lang.png', fullPage: false });

  await page.evaluate(() => {
    const en = document.querySelector('.lang-select__opt[data-lang="en"]');
    if (en) en.click();
  });
  await new Promise((r) => setTimeout(r, 200));
  const enHref = await page.evaluate(() => ({
    lang: document.documentElement.lang,
    href: document.getElementById('visitMail') && document.getElementById('visitMail').getAttribute('href'),
    cta: document.getElementById('visitMail') && document.getElementById('visitMail').textContent,
    checkContent: getComputedStyle(document.querySelector('.lang-select__opt[aria-selected="true"]'), '::after').content,
  }));
  console.log('EN_VISIT', JSON.stringify(enHref));

  await page.evaluate(() => {
    document.documentElement.setAttribute('data-theme', 'light');
    localStorage.setItem('kairos-theme', 'light');
  });
  await new Promise((r) => setTimeout(r, 200));
  const light = await page.evaluate(() => {
    const el = document.querySelector('.fit-num');
    return { color: getComputedStyle(el).color, theme: document.documentElement.getAttribute('data-theme') };
  });
  console.log('LIGHT_FIT', JSON.stringify(light));
  await page.screenshot({ path: outDir + '/light-hero.png', fullPage: false });

  await browser.close();
})().catch((e) => {
  console.error(e);
  process.exit(1);
});
