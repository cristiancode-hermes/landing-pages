const puppeteer = require('puppeteer');
(async () => {
  const b = await puppeteer.launch({
    executablePath: '/opt/data/chrome-linux64/chrome',
    headless: true,
    args: ['--no-sandbox','--disable-setuid-sandbox','--disable-gpu','--disable-crashpad-forwarding']
  });

  // Desktop 1280x800
  let p = await b.newPage();
  await p.setViewport({width:1280,height:800});
  await p.evaluateOnNewDocument(()=>{localStorage.setItem('kairos-theme','light');localStorage.setItem('nido-cookie','ok');});
  await p.goto('http://127.0.0.1:9877/2026-08-17-nido.html',{waitUntil:'networkidle0',timeout:20000});
  await p.evaluate(()=>{document.documentElement.setAttribute('data-theme','light');});
  await new Promise(r=>setTimeout(r,1500));
  await p.screenshot({path:'/opt/data/landing-pages/screenshots/nido-desktop-after.png',fullPage:false});
  console.log('Desktop saved');

  // 750px — the overflow zone
  let p2 = await b.newPage();
  await p2.setViewport({width:750,height:900});
  await p2.evaluateOnNewDocument(()=>{localStorage.setItem('kairos-theme','light');localStorage.setItem('nido-cookie','ok');});
  await p2.goto('http://127.0.0.1:9877/2026-08-17-nido.html',{waitUntil:'networkidle0',timeout:20000});
  await p2.evaluate(()=>{document.documentElement.setAttribute('data-theme','light');});
  await new Promise(r=>setTimeout(r,1500));
  
  // Check if nav still overflows
  const navInfo = await p2.evaluate(()=>{
    const nav = document.querySelector('.nav-inner');
    const logo = document.querySelector('.nav-logo');
    const search = document.querySelector('.nav-search');
    const actions = document.querySelector('.nav-actions');
    return {
      vw: innerWidth,
      navSW: nav.scrollWidth,
      navCW: nav.clientWidth,
      overflow: nav.scrollWidth > nav.clientWidth,
      logoW: logo.offsetWidth,
      searchDisp: getComputedStyle(search).display,
      searchW: search.offsetWidth,
      actionsW: actions.offsetWidth
    };
  });
  console.log('750px nav:', JSON.stringify(navInfo));
  await p2.screenshot({path:'/opt/data/landing-pages/screenshots/nido-750-after.png',fullPage:false});
  console.log('750px saved');

  // Mobile 390x844
  let p3 = await b.newPage();
  await p3.setViewport({width:390,height:844});
  await p3.evaluateOnNewDocument(()=>{localStorage.setItem('kairos-theme','light');localStorage.setItem('nido-cookie','ok');});
  await p3.goto('http://127.0.0.1:9877/2026-08-17-nido.html',{waitUntil:'networkidle0',timeout:20000});
  await p3.evaluate(()=>{document.documentElement.setAttribute('data-theme','light');});
  await new Promise(r=>setTimeout(r,1500));
  await p3.screenshot({path:'/opt/data/landing-pages/screenshots/nido-mobile-after.png',fullPage:false});
  console.log('Mobile saved');

  await b.close();
  console.log('DONE');
})().catch(e=>{console.error('ERR',e.message);process.exit(1);});
