const puppeteer = require('/opt/data/node_modules/puppeteer');

const pages = [
  { file: '2026-07-29-passage-travel.html', fn: 'applyLanguage', mobileIds: 2 },
  { file: '2026-07-30-aura-fashion.html', fn: 'applyLanguage', mobileIds: 2 },
  { file: '2026-08-01-static-records.html', fn: 'applyLang', mobileIds: 1 },
  { file: '2026-08-04-pulse-health.html', fn: 'applyLang', mobileIds: 1 },
  { file: '2026-08-05-atrium-studio.html', fn: 'setLanguage', mobileIds: 1 },
  { file: '2026-08-13-lyra-dynamics.html', fn: 'applyLang', mobileIds: 2 },
];

(async () => {
  let failures = 0;
  for (const p of pages) {
    const url = `http://127.0.0.1:9877/${p.file}`;
    // ---- Desktop ----
    const b1 = await puppeteer.launch({
      executablePath: '/opt/data/chrome-linux64/chrome',
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu', '--disable-crashpad-forwarding'],
    });
    try {
      const page = await b1.newPage();
      await page.setViewport({ width: 1280, height: 800 });
      await page.goto(url, { waitUntil: 'networkidle0', timeout: 30000 });
      await page.evaluate(() => {
        ['theme', 'kairos-theme', 'darkMode'].forEach(k => localStorage.removeItem(k));
        localStorage.setItem('kairos-theme', 'light');
        document.documentElement.setAttribute('data-theme', 'light');
      });
      await page.evaluate(() => document.fonts.ready);
      await new Promise(r => setTimeout(r, 1500));

      const res = await page.evaluate(() => {
        const btns = document.querySelectorAll('.lang-select__btn');
        const opts = document.querySelectorAll('.lang-select__opt');
        if (btns.length === 0) return { error: 'no .lang-select__btn found' };
        const btn = btns[0];
        const menu = btn.parentElement.querySelector('.lang-select__menu');
        if (!menu) return { error: 'no menu' };
        btn.click();
        const opened = menu.classList.contains('open');
        const ariaExpanded = btn.getAttribute('aria-expanded');
        // pick an option (not the current one)
        let target = null;
        for (const o of menu.querySelectorAll('.lang-select__opt')) {
          if (o.getAttribute('aria-selected') !== 'true') { target = o; break; }
        }
        if (!target) return { error: 'no non-active option' };
        const targetLang = target.getAttribute('data-lang');
        target.click();
        const closedAfter = !menu.classList.contains('open');
        const cur = btn.querySelector('.lang-select__cur');
        return {
          btnCount: btns.length,
          optCount: opts.length,
          opened,
          ariaExpanded,
          targetLang,
          curAfter: cur ? cur.textContent : null,
          closedAfter,
          htmlLang: document.documentElement.lang,
        };
      });
      const label = res.error ? `❌ ${res.error}` : (res.opened && res.curAfter === res.targetLang.toUpperCase() && res.closedAfter ? '✅' : `⚠️ ${JSON.stringify(res)}`);
      console.log(`${p.file} DESKTOP: ${label} ${res.error ? '' : JSON.stringify({ btns: res.btnCount, opts: res.optCount, lang: res.targetLang, cur: res.curAfter })}`);
      if (res.error || !(res.opened && res.curAfter === res.targetLang.toUpperCase() && res.closedAfter)) failures++;
    } catch (e) {
      console.log(`${p.file} DESKTOP: ❌ EXC: ${e.message.slice(0, 120)}`);
      failures++;
    } finally {
      await b1.close();
    }

    // ---- Mobile (390×844) ----
    const b2 = await puppeteer.launch({
      executablePath: '/opt/data/chrome-linux64/chrome',
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu', '--disable-crashpad-forwarding'],
    });
    try {
      const page = await b2.newPage();
      await page.setViewport({ width: 390, height: 844 });
      await page.goto(url, { waitUntil: 'networkidle0', timeout: 30000 });
      await page.evaluate(() => {
        ['theme', 'kairos-theme', 'darkMode'].forEach(k => localStorage.removeItem(k));
        localStorage.setItem('kairos-theme', 'light');
        document.documentElement.setAttribute('data-theme', 'light');
      });
      await page.evaluate(() => document.fonts.ready);
      await new Promise(r => setTimeout(r, 1500));

      const res = await page.evaluate(() => {
        const btns = document.querySelectorAll('.lang-select__btn');
        const visible = Array.from(btns).filter(b => getComputedStyle(b).display !== 'none');
        // find the visible one (mobile menu may need opening)
        let btn = null;
        for (const b of visible) { const r = b.getBoundingClientRect(); if (r.width > 0 && r.height > 0 && r.right <= 400) { btn = b; break; } }
        if (!btn) return { error: 'no visible lang btn at 390px', btns: btns.length, visible: visible.length };
        const menu = btn.parentElement.querySelector('.lang-select__menu');
        btn.click();
        const opened = menu.classList.contains('open');
        const mw = menu.getBoundingClientRect();
        return {
          btnCount: btns.length,
          visibleCount: visible.length,
          opened,
          menuVisible: mw.width > 0 && mw.height > 0,
          menuRight: Math.round(mw.right),
          menuLeft: Math.round(mw.left),
          overflow: mw.right > 390 ? 'OVERFLOW' : 'ok',
        };
      });
      const label = res.error ? `❌ ${res.error}` : (res.opened && res.menuVisible && res.overflow === 'ok' ? '✅' : `⚠️ ${JSON.stringify(res)}`);
      console.log(`${p.file} MOBILE: ${label}`);
      if (res.error || !(res.opened && res.menuVisible && res.overflow === 'ok')) failures++;
    } catch (e) {
      console.log(`${p.file} MOBILE: ❌ EXC: ${e.message.slice(0, 120)}`);
      failures++;
    } finally {
      await b2.close();
    }
  }
  console.log(`\n${failures === 0 ? '✅ TODAS LAS PÁGINAS PASAN' : `❌ ${failures} FALLOS`}`);
  process.exit(failures === 0 ? 0 : 1);
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });
