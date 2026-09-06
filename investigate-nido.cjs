// Investigate NIDO header overflow 700-900px + hero text contrast
const puppeteer = require('puppeteer');

const URL = 'http://127.0.0.1:9877/2026-08-17-nido.html';
const CHROME = '/opt/data/chrome-linux64/chrome';

const PREP = function () {
  try {
    localStorage.setItem('kairos-theme', 'light');
    localStorage.setItem('nido-cookie', 'ok');
  } catch (e) {}
};

(async () => {
  const browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu', '--disable-crashpad-forwarding'],
  });

  // Test multiple widths in the 700-900 range
  const widths = [700, 720, 740, 760, 780, 800, 850, 900];
  
  for (const w of widths) {
    const page = await browser.newPage();
    await page.setViewport({ width: w, height: 900 });
    await page.evaluateOnNewDocument(PREP);
    await page.goto(URL, { waitUntil: 'networkidle0', timeout: 30000 });
    await page.evaluate(() => {
      document.documentElement.setAttribute('data-theme', 'light');
    });
    await new Promise(r => setTimeout(r, 1000));
    
    const info = await page.evaluate(() => {
      const nav = document.querySelector('.nav-inner');
      const logo = document.querySelector('.nav-logo');
      const search = document.querySelector('.nav-search');
      const actions = document.querySelector('.nav-actions');
      
      // Measure each nav-actions child
      const kids = [];
      for (const ch of actions.children) {
        const cs = getComputedStyle(ch);
        kids.push({
          cls: ch.className.substring(0, 25),
          w: ch.offsetWidth,
          display: cs.display,
          visibility: cs.visibility
        });
      }
      
      return {
        vw: window.innerWidth,
        navScrollW: nav.scrollWidth,
        navClientW: nav.clientWidth,
        overflow: nav.scrollWidth > nav.clientWidth,
        logoW: logo.offsetWidth,
        searchW: search.offsetWidth,
        searchDisplay: getComputedStyle(search).display,
        actionsW: actions.offsetWidth,
        actionsKids: kids
      };
    });
    
    console.log(`--- ${w}px ---`);
    console.log(JSON.stringify(info, null, 2));
    
    // Screenshot at 750px specifically
    if (w === 750 || w === 740) {
      await page.screenshot({ path: `/opt/data/landing-pages/screenshots/nido-header-${w}.png`, fullPage: false });
      console.log(`Screenshot saved: nido-header-${w}.png`);
    }
    
    await page.close();
  }

  // Also test hero contrast
  const page2 = await browser.newPage();
  await page2.setViewport({ width: 1280, height: 800 });
  await page2.evaluateOnNewDocument(PREP);
  await page2.goto(URL, { waitUntil: 'networkidle0', timeout: 30000 });
  await page2.evaluate(() => {
    document.documentElement.setAttribute('data-theme', 'light');
    localStorage.setItem('kairos-theme', 'light');
  });
  await new Promise(r => setTimeout(r, 1500));
  
  const heroInfo = await page2.evaluate(() => {
    const h1 = document.querySelector('.hero h1');
    const em = document.querySelector('.hero h1 em');
    const sub = document.querySelector('.hero-sub');
    const badge = document.querySelector('.hero-badge');
    const shade = document.querySelector('.hero-shade');
    
    const h1Style = getComputedStyle(h1);
    const subStyle = sub ? getComputedStyle(sub) : null;
    const emStyle = em ? getComputedStyle(em) : null;
    const badgeStyle = badge ? getComputedStyle(badge) : null;
    const shadeStyle = shade ? getComputedStyle(shade) : null;
    
    return {
      h1: { color: h1Style.color, fontSize: h1Style.fontSize, textShadow: h1Style.textShadow },
      em: em ? { color: emStyle.color, fontFamily: emStyle.fontFamily } : null,
      sub: sub ? { color: subStyle.color, fontSize: subStyle.fontSize } : null,
      badge: badge ? { color: badgeStyle.color, bg: badgeStyle.backgroundColor } : null,
      shadeBg: shadeStyle ? shadeStyle.background : null
    };
  });
  
  console.log('\n=== HERO TEXT STYLES ===');
  console.log(JSON.stringify(heroInfo, null, 2));
  
  await page2.screenshot({ path: '/opt/data/landing-pages/screenshots/nido-hero-contrast.png', fullPage: false });
  console.log('Hero screenshot saved');
  
  await browser.close();
})().catch(e => { console.error('ERR', e.message); process.exit(1); });
