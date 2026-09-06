const puppeteer = require('puppeteer');
(async () => {
  const b = await puppeteer.launch({
    executablePath: '/opt/data/chrome-linux64/chrome',
    headless: true,
    args: ['--no-sandbox','--disable-setuid-sandbox','--disable-gpu','--disable-crashpad-forwarding']
  });

  // Check multiple widths in the 760-920 overflow zone
  for (const w of [770, 800, 850, 900, 950]) {
    const p = await b.newPage();
    await p.setViewport({width:w,height:900});
    await p.evaluateOnNewDocument(()=>{localStorage.setItem('kairos-theme','light');localStorage.setItem('nido-cookie','ok');});
    await p.goto('http://127.0.0.1:9877/2026-08-17-nido.html',{waitUntil:'networkidle0',timeout:20000});
    await p.evaluate(()=>{document.documentElement.setAttribute('data-theme','light');});
    await new Promise(r=>setTimeout(r,1000));
    
    const navInfo = await p.evaluate(()=>{
      const nav = document.querySelector('.nav-inner');
      const logo = document.querySelector('.nav-logo');
      const search = document.querySelector('.nav-search');
      const actions = document.querySelector('.nav-actions');
      const kids = [];
      for(const ch of actions.children){
        kids.push({cls:ch.className.substring(0,20),w:ch.offsetWidth,disp:getComputedStyle(ch).display});
      }
      return {
        vw: innerWidth,
        navSW: nav.scrollWidth, navCW: nav.clientWidth, overflow: nav.scrollWidth > nav.clientWidth,
        logoW: logo.offsetWidth,
        searchDisp: getComputedStyle(search).display, searchW: search.offsetWidth,
        actionsW: actions.offsetWidth, kids
      };
    });
    console.log(`--- ${w}px ---`, JSON.stringify(navInfo));
    if (w === 850) {
      await p.screenshot({path:'/opt/data/landing-pages/screenshots/nido-850-after.png',fullPage:false});
    }
    await p.close();
  }

  await b.close();
  console.log('DONE');
})().catch(e=>{console.error('ERR',e.message);process.exit(1);});
