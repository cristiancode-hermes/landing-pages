#!/usr/bin/env python3
# Builds the CARRETE landing page as a single self-contained HTML file.
import os

out = "/opt/data/landing-pages/2026-08-22-carrete.html"

HEAD = '<!DOCTYPE html>\n<html lang="en" class="no-js" data-theme="light">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<title id="doc-title">CARRETE — Analog film, developed with care</title>\n<meta id="meta-desc" name="description" content="CARRETE is an analog photo lab in Lisbon. We develop, hand-scan and print your film rolls — 35mm, 120 and 4x5 — with emulsion-level care and fast turnaround.">\n<link rel="canonical" href="https://proyectos.cristiancode.dev/landings/2026-08-22-carrete.html">\n<meta property="og:type" content="website">\n<meta property="og:title" content="CARRETE — Analog film, developed with care">\n<meta property="og:description" content="Develop, hand-scan and print your film rolls — 35mm, 120 and 4x5 — with emulsion-level care in Lisbon.">\n<meta property="og:url" content="https://proyectos.cristiancode.dev/landings/2026-08-22-carrete.html">\n<meta property="twitter:card" content="summary_large_image">\n<meta property="twitter:title" content="CARRETE — Analog film lab">\n<meta property="twitter:description" content="Develop, hand-scan and print your rolls in Lisbon. 35mm, 120, 4x5.">\n<meta name="color-scheme" content="light dark">\n<link rel="icon" href="data:image/svg+xml,<svg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 100 100\'><rect width=\'100\' height=\'100\' fill=\'%230a0a0a\'/><rect x=\'18\' y=\'14\' width=\'64\' height=\'46\' rx=\'4\' fill=\'%23f2f2f2\'/><rect x=\'18\' y=\'26\' width=\'64\' height=\'4\' fill=\'%23C8102E\'/><circle cx=\'32\' cy=\'20\' r=\'7\' fill=\'%230a0a0a\' opacity=\'.25\'/><circle cx=\'50\' cy=\'20\' r=\'7\' fill=\'%230a0a0a\' opacity=\'.25\'/><circle cx=\'68\' cy=\'20\' r=\'7\' fill=\'%230a0a0a\' opacity=\'.25\'/></svg>">\n<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&display=swap" rel="stylesheet">\n<style>\n'

CSS = """/* ============================================================
   DESIGN SYSTEM — CARRETE · Analog photo lab
   Surface: Decide/Learn (landing). Process = real sequence,
            Film stocks + Pricing = Compare secondary.
   Derived from: Runway (popular-web-designs) — cinematic dark,
                 near-invisible UI, single typeface, zero shadows.
   Family: Photography
   Style: Darkroom cinematic — deep black canvas, cool slate text,
          REC red accent, one drenched safelight-amber band.
          Film grain, blinking REC, sprocket rhythm.
   Strategy: Drenched (dark surfaces ARE the brand) + one amber
             safelight band; red ≤10%.
   Type: Instrument Sans (geometric-humanist single family)
         + ui-monospace accents for film codes.
   ============================================================ */
:root{
  --bg:#fafafa; --surface:#f2f2f2; --ink:#1c1c1e; --muted:#59626e;
  --line:#e2e2e6; --line-strong:#cfcfd6;
  --stage:#0a0a0a; --stage-2:#111113; --stage-ink:#f5f5f3; --stage-muted:#a3abb6;
  --red:#C8102E; --red-hover:#A90E26; --red-ink:#ffffff; --red-link:#8a4d2c;
  --amber:#F2A516; --amber-ink:#141414;
  --mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  --sans:'Instrument Sans',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;
  --ease:cubic-bezier(.22,1,.36,1); --r:12px; --r-sm:6px;
}
[data-theme="dark"]{
  --bg:#0a0a0a; --surface:#141414; --ink:#f5f5f3; --muted:#a3abb6;
  --line:#26262a; --line-strong:#333338;
  --stage:#0a0a0a; --stage-2:#111113;
  --red:#C8102E; --red-hover:#D81B38; --red-ink:#ffffff; --red-link:#ff6b7a;
  --amber:#F2A516; --amber-ink:#141414;
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
html.no-js .rv{opacity:1;transform:none}
@keyframes marq{from{transform:translateX(0)}to{transform:translateX(-50%)}}
@keyframes recblink{0%,55%{opacity:1}56%,100%{opacity:.15}}
@keyframes grain{0%,100%{opacity:.05}45%{opacity:.11}70%{opacity:.07}}
@media (prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  .nav-blink,.hero-kicker .dot,.f-audio .rec{animation:none!important}
  .grain{animation:none!important;opacity:.06}
  .marquee-track{animation:none!important}
  .rv{transition:none!important;opacity:1;transform:none}
}
@media print{.rv{opacity:1;transform:none}}
body{font-family:var(--sans);background:var(--bg);color:var(--ink);line-height:1.6;-webkit-font-smoothing:antialiased;text-wrap:pretty}
h1,h2,h3,h4{font-weight:600;line-height:1.06;letter-spacing:-.03em;text-wrap:balance}
a{color:inherit;text-decoration:none}
button,input{font:inherit}
ul{list-style:none}
img,svg{display:block;max-width:100%}
.container{width:min(1120px,92%);margin-inline:auto}
.skip{position:absolute;left:-999px;top:0;background:var(--red);color:var(--red-ink);padding:.7rem 1.1rem;z-index:200;border-radius:0 0 var(--r-sm) 0}
.skip:focus{left:0;top:0}
.visually-hidden{position:absolute;width:1px;height:1px;margin:-1px;padding:0;border:0;clip:rect(0 0 0 0);overflow:hidden}
:focus-visible{outline:2px solid var(--red);outline-offset:3px;border-radius:3px}

/* Nav */
.nav{position:sticky;top:0;z-index:100;background:var(--bg);border-bottom:1px solid var(--line)}
.nav-inner{display:flex;align-items:center;justify-content:space-between;gap:1rem;padding:.85rem 0}
.brand{display:flex;align-items:center;gap:.6rem;font-weight:700;font-size:1.15rem;letter-spacing:-.02em}
.brand svg{width:26px;height:26px}
.brand em{font-style:normal;color:var(--red)}
.nav-links{display:flex;align-items:center;gap:1.4rem}
.nav-links a{font-size:.94rem;font-weight:500;color:var(--muted);transition:color .2s ease}
.nav-links a:hover{color:var(--ink)}
.nav-actions{display:flex;align-items:center;gap:.55rem}
.icon-btn{width:40px;height:40px;border-radius:50%;border:1px solid var(--line);background:var(--surface);color:var(--ink);display:grid;place-items:center;cursor:pointer;transition:border-color .2s ease,color .2s ease}
.icon-btn:hover{border-color:var(--red);color:var(--red)}
.burger{display:none}
.lang-select{position:relative}
.lang-select__btn{display:inline-flex;align-items:center;gap:.4rem;height:40px;padding:0 .9rem;border-radius:999px;border:1px solid var(--line);background:var(--surface);color:var(--ink);font-size:.84rem;font-weight:600;cursor:pointer;transition:border-color .2s ease}
.lang-select__btn:hover{border-color:var(--red)}
.lang-select__chevr{transition:transform .25s ease}
.lang-select__btn[aria-expanded="true"] .lang-select__chevr{transform:rotate(180deg)}
.lang-select__menu{position:absolute;right:0;top:calc(100% + 8px);min-width:176px;background:var(--surface);border:1px solid var(--line);border-radius:var(--r-sm);padding:.4rem;box-shadow:0 12px 32px rgba(10,10,10,.14);opacity:0;visibility:hidden;transform:translateY(-6px);transition:opacity .2s ease,transform .2s ease,visibility .2s;z-index:120}
.lang-select__menu.open{opacity:1;visibility:visible;transform:translateY(0)}
.lang-select__opt{display:flex;align-items:center;gap:.5rem;width:100%;padding:.55rem .75rem;border:none;background:none;border-radius:6px;font-size:.88rem;color:var(--ink);text-align:left;cursor:pointer;transition:background .15s ease}
.lang-select__opt:hover{background:rgba(200,16,46,.08)}
.lang-select__opt[aria-selected="true"]{color:var(--red);font-weight:700}
.lang-select__opt[aria-selected="true"]::after{content:'\\2713';margin-left:auto}
.mobile-menu{display:none;border-top:1px solid var(--line);padding:1rem 0 1.4rem}
.mobile-menu.open{display:block}
.mobile-menu a{display:block;padding:.65rem 0;color:var(--muted);font-weight:500}
.mobile-menu a:hover{color:var(--ink)}
.mobile-menu .m-cta{display:inline-flex;align-items:center;justify-content:center;padding:.72rem 1.15rem;margin-top:.6rem;color:var(--red-ink);font-weight:600;background:var(--red)}
.mobile-menu .lang-select{margin-top:1rem}
.nav-blink{width:8px;height:8px;border-radius:50%;background:var(--red);animation:recblink 2.4s infinite}

/* Buttons */
.btn{display:inline-flex;align-items:center;justify-content:center;gap:.5rem;padding:.78rem 1.3rem;border-radius:var(--r-sm);border:none;font-weight:600;font-size:.95rem;cursor:pointer;transition:background .2s var(--ease),color .2s var(--ease),transform .15s var(--ease)}
.btn:hover{transform:translateY(-1px)}
.btn-primary{background:var(--red);color:var(--red-ink)}
.btn-primary:hover{background:var(--red-hover)}
.btn-ghost{background:transparent;color:var(--ink);border:1px solid var(--line-strong)}
.btn-ghost:hover{border-color:var(--ink)}

/* Hero */
.hero{position:relative;background:var(--stage);color:var(--stage-ink);overflow:hidden}
.grain{position:absolute;inset:0;pointer-events:none;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2'/%3E%3C/filter%3E%3Crect width='140' height='140' filter='url(%23n)' opacity='0.6'/%3E%3C/svg%3E");opacity:.06;animation:grain 7s steps(2) infinite}
.hero-inner{position:relative;display:grid;grid-template-columns:1.02fr .98fr;gap:clamp(2rem,5vw,4rem);align-items:center;padding:clamp(4rem,10vw,7rem) 0 clamp(3.5rem,9vw,6rem)}
.hero-kicker{display:inline-flex;align-items:center;gap:.55rem;font-family:var(--mono);font-size:.74rem;letter-spacing:.16em;text-transform:uppercase;color:var(--stage-muted);margin-bottom:1.2rem}
.hero-kicker .dot{width:8px;height:8px;border-radius:50%;background:var(--red);animation:recblink 2.4s infinite}
.hero h1{font-size:clamp(2.4rem,6vw,5rem);line-height:1.0;letter-spacing:-.035em;margin-bottom:1.4rem}
.hero h1 .accent{color:#ff8d99;font-style:normal}
.hero-sub{font-size:clamp(1.02rem,1.6vw,1.18rem);color:var(--stage-muted);max-width:42ch;margin-bottom:2rem}
.hero-cta{display:flex;flex-wrap:wrap;gap:.8rem;align-items:center}
.hero-cta .btn-primary{color:#fff}
.hero-cta .btn-ghost{border-color:rgba(245,245,243,.28);color:var(--stage-ink)}
.hero-cta .btn-ghost:hover{border-color:var(--stage-ink)}
.hero-note{margin-top:1.4rem;font-family:var(--mono);font-size:.72rem;letter-spacing:.05em;color:var(--stage-muted)}
.hero-note a{color:var(--stage-ink);border-bottom:1px solid var(--stage-muted)}

/* Film strip art */
.film{position:relative}
.f-strip{position:relative;border-radius:var(--r);border:1px solid #26262a;background:var(--stage-2);overflow:hidden}
.f-frames{display:grid;grid-template-columns:repeat(3,1fr);gap:.66rem;padding:.9rem;margin:1.05rem .4rem .9rem}
.f-frame{aspect-ratio:3/4;border-radius:3px;background-position:center;background-size:cover;position:relative}
.f-frame::after{content:'';position:absolute;inset:0;border:1px solid rgba(255,255,255,.06);border-radius:3px}
.f-1{background-image:linear-gradient(135deg,#3a3a3e 0%,#6b6b70 46%,#2a2a2c 100%)}
.f-2{background-image:radial-gradient(circle at 30% 30%,#7a7a72 0%,#3e3c37 60%,#24231f 100%)}
.f-3{background-image:linear-gradient(180deg,#242424 0%,#5a5a58 55%,#141414 100%)}
.f-4{background-image:radial-gradient(ellipse at 70% 20%,#8a8580 0%,#4a4640 55%,#1f1e1b 100%)}
.f-5{background-image:linear-gradient(160deg,#2c2c30 0%,#8d8d86 50%,#48484c 100%)}
.f-6{background-image:radial-gradient(circle at 50% 75%,#6e6a62 0%,#35332f 55%,#171614 100%)}
.spk{position:absolute;left:0;right:0;background:repeating-linear-gradient(90deg,transparent 0 14px,#111113 14px 20px,transparent 20px 34px,#111113 34px 40px)}
.spk-t{top:0;height:14px}
.spk-b{bottom:0;height:14px}
.f-audio{display:flex;align-items:center;gap:.6rem;padding:.55rem .9rem;border-top:1px solid #1f1f22;font-family:var(--mono);font-size:.68rem;letter-spacing:.08em;color:var(--stage-muted)}
.f-audio .rec{width:7px;height:7px;border-radius:50%;background:var(--red);animation:recblink 1.8s infinite}

/* Marquee band */
.marquee{background:var(--stage);border-top:1px solid #1e1e21;border-bottom:1px solid #1e1e21;overflow:hidden;padding:1rem 0;color:var(--stage-ink)}
.marquee-track{display:flex;gap:3rem;width:max-content;animation:marq 36s linear infinite}
.marquee-track span{white-space:nowrap;font-family:var(--mono);font-size:.82rem;letter-spacing:.1em;text-transform:uppercase;color:var(--stage-muted)}
.marquee-track span b{color:var(--stage-ink);font-weight:500}

/* Section scaffolding */
.section{padding:clamp(3.5rem,8vw,6rem) 0}
.s-head{max-width:60ch;margin-bottom:clamp(2rem,4vw,3rem)}
.s-head .k{font-family:var(--mono);font-size:.74rem;letter-spacing:.16em;text-transform:uppercase;color:var(--red);margin-bottom:.7rem;font-weight:500}
.s-head h2{font-size:clamp(1.7rem,3.6vw,2.6rem)}
.s-head p{color:var(--muted);margin-top:.8rem;max-width:52ch}

/* Process (real 3-step sequence) */
.process-steps{display:grid;grid-template-columns:repeat(3,1fr);gap:1.25rem;counter-reset:step}
.step{position:relative;border:1px solid var(--line);border-radius:var(--r);background:var(--surface);padding:2rem 1.5rem 1.6rem}
.step::before{counter-increment:step;content:counter(step,decimal-leading-zero);position:absolute;top:1.4rem;right:1.4rem;font-family:var(--mono);font-size:.8rem;letter-spacing:.04em;color:var(--muted)}
.step h3{font-size:1.18rem;margin-bottom:.5rem}
.step p{font-size:.95rem;color:var(--muted)}
.step .tag{display:inline-block;margin-top:1rem;font-family:var(--mono);font-size:.7rem;letter-spacing:.07em;text-transform:uppercase;color:var(--red)}
.step.step-dk{background:var(--stage);color:var(--stage-ink);border-color:transparent}
.step.step-dk::before{color:var(--stage-muted)}
.step-dk p{color:var(--stage-muted)}
.step-dk .tag{color:#ff8d99}

/* Stocks compare */
.stocks{display:grid;grid-template-columns:repeat(3,1fr);gap:1.15rem}
.stock{border:1px solid var(--line);border-radius:var(--r);padding:1.6rem 1.4rem;display:flex;flex-direction:column;gap:.4rem;background:var(--surface)}
.stock .st-name{font-family:var(--mono);font-size:.8rem;letter-spacing:.1em;text-transform:uppercase;color:var(--red)}
.stock h4{font-size:1.15rem}
.stock .st-desc{font-size:.92rem;color:var(--muted);flex:1}
.stock .st-row{display:flex;justify-content:space-between;font-size:.9rem;border-top:1px solid var(--line);padding-top:.6rem;margin-top:.3rem}
.stock .st-row span{color:var(--muted)}
.stoch .st-row b,.stock .st-row b{font-weight:600}
.stock.stock-feat{background:var(--stage);color:var(--stage-ink);border-color:transparent}
.stock.stock-feat .st-name{color:#ff8d99}
.stock.stock-feat .st-desc{color:var(--stage-muted)}
.stock.stock-feat .st-row{border-color:#2a2a2e}
.stock .st-badge{display:inline-block;align-self:flex-start;font-family:var(--mono);font-size:.66rem;letter-spacing:.1em;text-transform:uppercase;background:var(--amber);color:var(--amber-ink);border-radius:999px;padding:.24rem .62rem;margin-bottom:.3rem}

/* Darkroom amber band */
.darkroom{background:var(--amber);color:var(--amber-ink);border-radius:var(--r);padding:clamp(2.4rem,5vw,3.6rem);position:relative;overflow:hidden}
.darkroom .k{font-family:var(--mono);font-size:.74rem;letter-spacing:.16em;text-transform:uppercase;margin-bottom:.7rem;color:#3a2d00}
.darkroom h2{font-size:clamp(1.6rem,3.4vw,2.4rem);letter-spacing:-.03em;max-width:22ch}
.darkroom p{max-width:46ch;margin:1rem 0 1.6rem;color:#3a2d00}
.darkroom-grid{display:grid;grid-template-columns:1.4fr 1fr;gap:2rem;align-items:center}
.darkroom .prints{display:grid;grid-template-columns:repeat(3,1fr);gap:.6rem}
.print{aspect-ratio:3/4;border-radius:4px;background-position:center;background-size:cover;box-shadow:0 14px 30px -16px rgba(60,40,0,.5)}
.pr-1{background-color:#C98A2B;background-image:radial-gradient(circle at 35% 35%,#E8B85A 0%,#9c6a1e 100%)}
.pr-2{background-color:#B67A22;background-image:linear-gradient(150deg,#f0ce80 0%,#8a5a12 100%)}
.pr-3{background-color:#d29a3d;background-image:radial-gradient(circle at 70% 25%,#f6d98f 0%,#7c4f0e 100%)}

/* Testimonial */
.testimonial{display:grid;grid-template-columns:1fr 3.2fr;gap:2rem;align-items:start}
.testimonial .t-badge{display:flex;align-items:center;gap:.6rem;font-family:var(--mono);font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
blockquote.quote{font-size:clamp(1.25rem,2.4vw,1.7rem);line-height:1.3;letter-spacing:-.02em;font-weight:500;margin-bottom:1.2rem}
.quote-cite{display:flex;align-items:center;gap:.9rem;color:var(--muted);font-size:.95rem}
.quote-cite .avatar{width:44px;height:44px;border-radius:50%;background:linear-gradient(135deg,#c8c8cc,#8f8f94);display:grid;place-items:center;color:#fff;font-weight:700}

/* Pricing compare */
.pricing{display:grid;grid-template-columns:repeat(3,1fr);gap:1.15rem;align-items:stretch}
.plan{border:1px solid var(--line);border-radius:var(--r);padding:1.7rem 1.5rem;display:flex;flex-direction:column;background:var(--surface)}
.plan h4{font-size:1.12rem;margin-bottom:.2rem}
.plan .tag{font-family:var(--mono);font-size:.7rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin-bottom:1.1rem}
.plan .price{font-size:1.9rem;font-weight:700;letter-spacing:-.03em}
.plan .price sub{font-size:.82rem;font-weight:500;color:var(--muted);letter-spacing:0}
.plan ul{flex:1;margin:1.1rem 0;display:grid;gap:.55rem}
.plan ul li{display:flex;gap:.55rem;font-size:.92rem;color:var(--muted)}
.plan ul li b{color:var(--ink);font-weight:600}
.plan ul li::before{content:'+';color:var(--red);font-weight:700}
.plan.plan-feat{background:var(--stage);color:var(--stage-ink);border-color:transparent}
.plan-feat ul li{color:var(--stage-muted)}
.plan-feat ul li b{color:var(--stage-ink)}
.plan-feat .price{color:var(--stage-ink)}
.plan-feat .plan-badge{display:inline-block;align-self:flex-start;background:var(--red);color:var(--red-ink);font-family:var(--mono);font-size:.66rem;letter-spacing:.1em;text-transform:uppercase;border-radius:999px;padding:.24rem .62rem;margin-bottom:.6rem}

/* FAQ */
.faq{max-width:760px}
.faq-item{border:1px solid var(--line);border-radius:var(--r);margin-bottom:.7rem;overflow:hidden;background:var(--surface)}
.faq-q{width:100%;display:flex;justify-content:space-between;align-items:center;gap:1rem;padding:1.05rem 1.2rem;background:none;border:none;color:var(--ink);font-weight:600;font-size:1rem;cursor:pointer;text-align:left;transition:background .2s ease}
.faq-q:hover{background:rgba(200,16,46,.04)}
.faq-q .chev{flex:none;color:var(--red);transition:transform .3s var(--ease)}
.faq-item.open .chev{transform:rotate(45deg)}
.faq-a{max-height:0;overflow:hidden;transition:max-height .36s var(--ease)}
.faq-a p{padding:0 1.2rem 1.2rem;color:var(--muted);font-size:.95rem}

/* Newsletter */
.nl{background:var(--stage);color:var(--stage-ink);border-radius:var(--r);padding:clamp(2.2rem,5vw,3.2rem);text-align:center}
.nl .k{font-family:var(--mono);font-size:.74rem;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);margin-bottom:.7rem}
.nl h2{font-size:clamp(1.5rem,3.2vw,2.2rem);margin-bottom:.7rem}
.nl p{color:var(--stage-muted);max-width:50ch;margin:0 auto 1.6rem}
.nl-form{display:flex;gap:.6rem;justify-content:center;flex-wrap:wrap;max-width:440px;margin:0 auto}
.nl-form input{flex:1;min-width:150px;padding:.8rem 1rem;border-radius:var(--r-sm);border:1px solid #333338;background:var(--stage-2);color:var(--stage-ink)}
.nl-form input::placeholder{color:var(--stage-muted)}
.nl-form input:focus{outline:2px solid var(--red);outline-offset:2px}
.nl-msg{margin-top:.8rem;font-size:.9rem;min-height:1.2em}
.nl-msg.ok{color:#7CC970}
.nl-msg.err{color:#ff8d99}

/* Footer */
.footer{background:var(--stage);color:var(--stage-ink);padding:3rem 0 2rem;border-top:1px solid #1e1e21}
.footer-grid{display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:2rem}
.footer .f-desc{color:var(--stage-muted);max-width:34ch;margin-top:.8rem;font-size:.92rem}
.footer h5{font-size:.85rem;letter-spacing:.08em;text-transform:uppercase;color:var(--stage-muted);margin-bottom:.9rem;font-weight:600}
.footer ul{display:grid;gap:.55rem}
.footer ul a{color:var(--stage-ink);font-size:.92rem;transition:color .2s ease}
.footer ul a:hover{color:var(--red)}
.footer .f-bot{border-top:1px solid #26262a;margin-top:2rem;padding-top:1.4rem;display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;font-size:.82rem;color:var(--stage-muted)}
.footer .f-bot a{color:var(--stage-muted);border-bottom:1px solid var(--stage-muted)}

/* Cookie banner */
.cookie{position:fixed;z-index:90;right:1rem;bottom:1rem;max-width:330px;background:var(--stage);color:var(--stage-ink);border:1px solid #2a2a2e;border-radius:var(--r);padding:1.1rem 1.2rem;box-shadow:0 18px 44px rgba(0,0,0,.35);transform:translateY(calc(100% + 2rem));transition:transform .5s var(--ease);visibility:hidden}
.cookie.show{transform:translateY(0);visibility:visible}
.cookie p{font-size:.85rem;color:var(--stage-muted);margin-bottom:.9rem}
.cookie .ck-acts{display:flex;gap:.5rem}
.cookie .ck-btn{padding:.5rem .85rem;border-radius:var(--r-sm);border:none;font-weight:600;font-size:.82rem;cursor:pointer}
.cookie .ck-ok{background:var(--red);color:var(--red-ink)}
.cookie .ck-no{background:transparent;color:var(--stage-ink);border:1px solid #333338}

/* Reveal */
.rv{opacity:0;transform:translateY(22px)}
.rv.in{opacity:1;transform:none;transition:opacity .6s var(--ease),transform .7s var(--ease)}

/* Responsive */
@media (max-width:920px){
  .nav-links{display:none}
  .nav-actions .btn{display:none}
  .burger{display:grid}
  .hero-inner{grid-template-columns:1fr;gap:2.2rem}
  .process-steps{grid-template-columns:1fr}
  .stocks{grid-template-columns:1fr}
  .pricing{grid-template-columns:1fr}
  .darkroom-grid{grid-template-columns:1fr}
  .testimonial{grid-template-columns:1fr;gap:1rem}
  .footer-grid{grid-template-columns:1fr 1fr}
}
@media (max-width:520px){
  .footer-grid{grid-template-columns:1fr}
  .f-frames{grid-template-columns:repeat(2,1fr)}
  .hero-cta{flex-direction:column;align-items:stretch}
  .hero-cta .btn{width:100%}
  .cookie{left:1rem;right:1rem;max-width:none}
}
</style>
</head>
<body>
"""

BODY = """
<a class="skip" href="#main" data-i18n="skip">Skip to content</a>

<nav class="nav" aria-label="Main">
  <div class="container nav-inner">
    <a class="brand" href="#hero" data-i18n-aria="brandAria" aria-label="CARRETE home">
      <svg viewBox="0 0 32 32" fill="none" aria-hidden="true"><rect x="3" y="5" width="26" height="20" rx="3" fill="none" stroke="currentColor" stroke-width="2"/><rect x="3" y="9" width="26" height="3.4" fill="var(--red)"/><circle cx="10" cy="7.6" r="1.7" fill="currentColor"/><circle cx="16" cy="7.6" r="1.7" fill="currentColor"/><circle cx="22" cy="7.6" r="1.7" fill="currentColor"/></svg>
      CAR<em>RE</em>TE
    </a>
    <ul class="nav-links">
      <li><a href="#process" data-i18n="nProcess">The process</a></li>
      <li><a href="#stocks" data-i18n="nStocks">Film stocks</a></li>
      <li><a href="#darkroom" data-i18n="nPrints">Prints</a></li>
      <li><a href="#pricing" data-i18n="nPricing">Pricing</a></li>
      <li><a href="#faq" data-i18n="nFaq">FAQ</a></li>
    </ul>
    <div class="nav-actions">
      <span class="nav-blink" aria-hidden="true"></span>
      <div class="lang-select">
        <button class="lang-select__btn" type="button" aria-haspopup="listbox" aria-expanded="false" data-i18n-aria="langLabel" aria-label="Choose language">
          <span class="lang-select__cur">EN</span>
          <svg class="lang-select__chevr" width="10" height="6" viewBox="0 0 10 6" fill="none" aria-hidden="true"><path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </button>
        <div class="lang-select__menu" role="listbox" aria-label="Choose language">
          <button class="lang-select__opt" role="option" data-lang="en" aria-selected="false">English</button>
          <button class="lang-select__opt" role="option" data-lang="es" aria-selected="false">Español</button>
          <button class="lang-select__opt" role="option" data-lang="fr" aria-selected="false">Français</button>
          <button class="lang-select__opt" role="option" data-lang="de" aria-selected="false">Deutsch</button>
          <button class="lang-select__opt" role="option" data-lang="it" aria-selected="false">Italiano</button>
          <button class="lang-select__opt" role="option" data-lang="pt" aria-selected="false">Português</button>
        </div>
      </div>
      <button class="icon-btn" id="themeToggle" type="button" data-i18n-aria="themeLabel" aria-label="Toggle theme">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>
      </button>
      <button class="icon-btn burger" id="burger" type="button" data-i18n-aria="menuLabel" aria-label="Open menu" aria-expanded="false">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
      </button>
    </div>
  </div>
  <div class="container">
    <div class="mobile-menu" id="mobileMenu">
      <a href="#process" data-i18n="nProcess">The process</a>
      <a href="#stocks" data-i18n="nStocks">Film stocks</a>
      <a href="#darkroom" data-i18n="nPrints">Prints</a>
      <a href="#pricing" data-i18n="nPricing">Pricing</a>
      <a href="#faq" data-i18n="nFaq">FAQ</a>
      <a class="m-cta" href="#pricing" data-i18n="brandSend">Start a roll</a>
      <div class="lang-select">
        <button class="lang-select__btn" type="button" aria-haspopup="listbox" aria-expanded="false" data-i18n-aria="langLabel" aria-label="Choose language">
          <span class="lang-select__cur">EN</span>
          <svg class="lang-select__chevr" width="10" height="6" viewBox="0 0 10 6" fill="none" aria-hidden="true"><path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </button>
        <div class="lang-select__menu" role="listbox" aria-label="Choose language">
          <button class="lang-select__opt" role="option" data-lang="en" aria-selected="false">English</button>
          <button class="lang-select__opt" role="option" data-lang="es" aria-selected="false">Español</button>
          <button class="lang-select__opt" role="option" data-lang="fr" aria-selected="false">Français</button>
          <button class="lang-select__opt" role="option" data-lang="de" aria-selected="false">Deutsch</button>
          <button class="lang-select__opt" role="option" data-lang="it" aria-selected="false">Italiano</button>
          <button class="lang-select__opt" role="option" data-lang="pt" aria-selected="false">Português</button>
        </div>
      </div>
    </div>
  </div>
</nav>

<main id="main">
  <section class="hero" id="hero">
    <div class="grain" aria-hidden="true"></div>
    <div class="container hero-inner">
      <div class="hero-copy rv">
        <span class="hero-kicker"><span class="dot" aria-hidden="true"></span><span data-i18n="heroKicker">Analog photo lab · Lisbon</span></span>
        <h1><span data-i18n="heroH1a">Your film,</span> <em class="accent" data-i18n="heroH1b">developed by hand</em> <span data-i18n="heroH1c">— never rushed.</span></h1>
        <p class="hero-sub" data-i18n="heroSub">We develop, hand-scan and print your rolls in downtown Lisbon. 35mm, 120 and large format, with emulsion-level care, honest turnaround times and a darkroom that never sleeps through a deadline.</p>
        <div class="hero-cta">
          <a class="btn btn-primary" href="#pricing" data-i18n="brandSend">Start a roll</a>
          <a class="btn btn-ghost" href="#darkroom" data-i18n="brandSee">See the prints</a>
        </div>
        <p class="hero-note" data-i18n="heroNote">C-41 · E-6 · B&amp;W — drop a roll or book online · <a href="#pricing" data-i18n="heroNoteLink">prices</a></p>
      </div>
      <div class="film rv">
        <div class="f-strip" role="img" data-i18n-aria="filmAria" aria-label="35mm film strip showing six developed frames">
          <div class="spk spk-t" aria-hidden="true"></div>
          <div class="f-frames">
            <div class="f-frame f-1"></div>
            <div class="f-frame f-2"></div>
            <div class="f-frame f-3"></div>
            <div class="f-frame f-4"></div>
            <div class="f-frame f-5"></div>
            <div class="f-frame f-6"></div>
          </div>
          <div class="spk spk-b" aria-hidden="true"></div>
          <div class="f-audio">
            <span class="rec" aria-hidden="true"></span>
            <span data-i18n="filmStock_1">recorded on 35mm · iso 400</span>
            <span style="margin-left:auto" data-i18n="filmStock_2">frame 00014</span>
          </div>
        </div>
      </div>
    </div>
  </section>

  <div class="marquee" aria-hidden="true">
    <div class="marquee-track">
      <span><b>PORTRA 400</b> · <b>HP5 PLUS</b> · <b>PRO 400H</b> · <b>GOLD 200</b> · <b>CINESTILL 800T</b> · <b>EKTAR 100</b> · <b>DELTA 3200</b> · <b>VELVIA 50</b> · </span>
      <span><b>PORTRA 400</b> · <b>HP5 PLUS</b> · <b>PRO 400H</b> · <b>GOLD 200</b> · <b>CINESTILL 800T</b> · <b>EKTAR 100</b> · <b>DELTA 3200</b> · <b>VELVIA 50</b> · </span>
    </div>
  </div>

  <section class="section" id="process">
    <div class="container">
      <div class="s-head rv">
        <span class="k" data-i18n="procK">The process</span>
        <h2 data-i18n="procT">Three stations, zero corners cut</h2>
        <p class="lead" data-i18n="procL">Every roll moves through the same careful chain. We tell you exactly what happens at each step, so you always know where your film is and when it's coming back.</p>
      </div>
      <div class="process-steps">
        <article class="step rv">
          <h3 data-i18n="p1t">Develop</h3>
          <p data-i18n="p1p">Fresh chemistry, temperature-held to the decimal, checked daily. We process C-41, E-6 and black-and-white in-house — never batched with other labs' film.</p>
          <span class="tag" data-i18n="p1tag">~ 90 min wet</span>
        </article>
        <article class="step step-dk rv">
          <h3 data-i18n="p2t">Hand-scan</h3>
          <p data-i18n="p2p">We don't rely on auto-settings. Each frame is scanned by an eye that reads shadow and highlight, corrected to match the negative — not a uniform factory curve.</p>
          <span class="tag" data-i18n="p2tag">TIF or JPEG</span>
        </article>
        <article class="step rv">
          <h3 data-i18n="p3t">Return</h3>
          <p data-i18n="p3p">Scans online in a private gallery, negatives sleeved and cut to order. Optional prints, done in our own safelight — nothing subcontracts out of the lab.</p>
          <span class="tag" data-i18n="p3tag">48h typical</span>
        </article>
      </div>
    </div>
  </section>

  <section class="section" id="stocks">
    <div class="container">
      <div class="s-head rv">
        <span class="k" data-i18n="stocksK">Film stocks</span>
        <h2 data-i18n="stocksT">One lab, three chemistries</h2>
        <p class="lead" data-i18n="stocksL">Whether it's color negative, black-and-white or slide, the development differs and we price it honestly. Here's what each process buys you.</p>
      </div>
      <div class="stocks">
        <article class="stock rv">
          <span class="st-name" data-i18n="st1name">C-41 — color neg</span>
          <h4 data-i18n="st1t">Color negative</h4>
          <p class="st-desc" data-i18n="st1d">Daylight-balanced, forgiving, the everyday workhorse. Ideal for travel, street and documentary rolls that live on Instagram and prints alike.</p>
          <div class="st-row"><span data-i18n="stDev">Processing</span><b data-i18n="st1dev">€5.50</b></div>
          <div class="st-row"><span data-i18n="stScan">Hand-scan</span><b data-i18n="st1scan">€8</b></div>
          <div class="st-row"><span data-i18n="stTurn">Turnaround</span><b data-i18n="st1turn">24–48h</b></div>
        </article>
        <article class="stock stock-feat rv">
          <span class="st-badge" data-i18n="stFeat">Most popular</span>
          <span class="st-name" data-i18n="st2name">B&amp;W — push/pull</span>
          <h4 data-i18n="st2t">Black &amp; white, any speed</h4>
          <p class="st-desc" data-i18n="st2d">We develop by hand and push or pull to match your shot. Grain and contrast are decisions we make together, not setbacks of a machine.</p>
          <div class="st-row"><span data-i18n="stDev">Processing</span><b data-i18n="st2dev">€7</b></div>
          <div class="st-row"><span data-i18n="stScan">Hand-scan</span><b data-i18n="st2scan">€8</b></div>
          <div class="st-row"><span data-i18n="stTurn">Turnaround</span><b data-i18n="st2turn">24h</b></div>
        </article>
        <article class="stock rv">
          <span class="st-name" data-i18n="st3name">E-6 — slide</span>
          <h4 data-i18n="st3t">Slide film</h4>
          <p class="st-desc" data-i18n="st3d">Delicate and demanding. Our E-6 line runs weekly, freshly mixed, for the transparencies that deserve to be held to the light.</p>
          <div class="st-row"><span data-i18n="stDev">Processing</span><b data-i18n="st3dev">€13</b></div>
          <div class="st-row"><span data-i18n="stScan">Hand-scan</span><b data-i18n="st3scan">€10</b></div>
          <div class="st-row"><span data-i18n="stTurn">Turnaround</span><b data-i18n="st3turn">1 week</b></div>
        </article>
      </div>
    </div>
  </section>

  <section class="section" id="darkroom">
    <div class="container">
      <div class="darkroom rv">
        <div class="darkroom-grid">
          <div>
            <span class="k" data-i18n="drK">The safelight room</span>
            <h2 data-i18n="drT">We print the frames worth holding</h2>
            <p data-i18n="drL">We run the same darkroom we scan in — real light over paper for the shots you care about. Grain is preserved, blacks stay deep, and nothing is passed through a printer's menu we wouldn't accept ourselves.</p>
            <a class="btn btn-primary" href="#pricing" data-i18n="drCta">Order a print</a>
          </div>
          <div class="prints" aria-hidden="true">
            <div class="print pr-1"></div>
            <div class="print pr-2"></div>
            <div class="print pr-3"></div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container testimonial">
      <div class="t-badge rv">
        <span style="width:8px;height:8px;border-radius:50%;background:var(--red);display:inline-block" aria-hidden="true"></span>
        <span data-i18n="tKick">From a regular</span>
      </div>
      <div class="rv">
        <blockquote class="quote" data-i18n="tQuote">"I shot a quarter of a century on digital because development was a chore. CARRETE made film feel like a craft again — they ring when frames are special, and they're right more than I'd like."</blockquote>
        <div class="quote-cite">
          <span class="avatar" aria-hidden="true">M</span>
          <span><strong data-i18n="tName">Marta Ibáñez</strong> · <span data-i18n="tRole">documentary photographer, customer since 2017</span></span>
        </div>
      </div>
    </div>
  </section>

  <section class="section" id="pricing">
    <div class="container">
      <div class="s-head rv">
        <span class="k" data-i18n="prK">Pricing</span>
        <h2 data-i18n="prT">Honest per-roll numbers</h2>
        <p class="lead" data-i18n="prL">No hidden fees, no minimum batches. Scans come back at full resolution, and every dev includes a free negative sleeve.</p>
      </div>
      <div class="pricing">
        <article class="plan rv">
          <h4 data-i18n="pl1t">Single roll</h4>
          <span class="tag" data-i18n="pl1tag">Pay as you go</span>
          <div class="price" data-i18n="pl1price">€14<sub> / roll</sub></div>
          <ul>
            <li data-i18n="pl1f1">Any C-41 or B&amp;W development</li>
            <li data-i18n="pl1f2">36-frame hand-scan TIF/JPEG</li>
            <li data-i18n="pl1f3">Free negatives sleeve</li>
            <li data-i18n="pl1f4">Online private gallery</li>
          </ul>
          <a class="btn btn-ghost" href="#faq" data-i18n="pl1cta">Start here</a>
        </article>
        <article class="plan plan-feat rv">
          <span class="plan-badge" data-i18n="plFeat">Best value</span>
          <h4 data-i18n="pl2t">The contact sheet</h4>
          <span class="tag" data-i18n="pl2tag">Heavy shooters</span>
          <div class="price" data-i18n="pl2price">€42<sub> / 3 rolls</sub></div>
          <ul>
            <li data-i18n="pl2f1">3 rolls, any mix of chemistries</li>
            <li data-i18n="pl2f2">Each scanned and color-corrected</li>
            <li data-i18n="pl2f3">Printed contact sheet included</li>
            <li data-i18n="pl2f4">Priority 24h turnaround</li>
            <li data-i18n="pl2f5">Free push/pull on the B&amp;W roll</li>
          </ul>
          <a class="btn btn-primary" href="#newsletter" data-i18n="pl2cta">Book the sheet</a>
        </article>
        <article class="plan rv">
          <h4 data-i18n="pl3t">The roll club</h4>
          <span class="tag" data-i18n="pl3tag">Subscription</span>
          <div class="price" data-i18n="pl3price">€29<sub> / month</sub></div>
          <ul>
            <li data-i18n="pl3f1">2 rolls a month, banked if unused</li>
            <li data-i18n="pl3f2">15% off prints and darkroom time</li>
            <li data-i18n="pl3f3">Occasional stock drops &amp; loaners</li>
            <li data-i18n="pl3f4">Pause or cancel anytime</li>
          </ul>
          <a class="btn btn-ghost" href="#newsletter" data-i18n="pl3cta">Join the club</a>
        </article>
      </div>
    </div>
  </section>

  <section class="section" id="faq">
    <div class="container">
      <div class="s-head rv">
        <span class="k" data-i18n="faqK">FAQ</span>
        <h2 data-i18n="faqT">Before you drop off a roll</h2>
      </div>
      <div class="faq">
        <div class="faq-item rv">
          <button class="faq-q" type="button" aria-expanded="false">
            <span data-i18n="fq1">How long does development actually take?</span>
            <svg class="chev" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>
          </button>
          <div class="faq-a"><p data-i18n="fa1">C-41 and black-and-white are usually ready in 24 to 48 hours, scans uploaded to a private online gallery as soon as they're finished. E-6 slide is run once a week and takes up to 7 days. If you have a hard deadline, tell us at the counter — we'll schedule around it instead of promising the impossible.</p></div>
        </div>
        <div class="faq-item rv">
          <button class="faq-q" type="button" aria-expanded="false">
            <span data-i18n="fq2">Do I need to book before bringing film?</span>
            <svg class="chev" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>
          </button>
          <div class="faq-a"><p data-i18n="fa2">For a single roll, walk-ins are welcome any open hour. For the contact sheet batch, a subscription or darkroom printing, we ask for a quick online booking so the chemistry and bench time are ready — it takes thirty seconds and keeps turnaround predictable.</p></div>
        </div>
        <div class="faq-item rv">
          <button class="faq-q" type="button" aria-expanded="false">
            <span data-i18n="fq3">Is my film safekept while I wait?</span>
            <svg class="chev" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>
          </button>
          <div class="faq-a"><p data-i18n="fa3">Yes. Film is logged on arrival, stored away from heat and light, and handled only by trained staff. Negatives are sleeved and returned or held in climate-controlled files for up to a year. We've never lost a roll — and we intend to keep that record.</p></div>
        </div>
        <div class="faq-item rv">
          <button class="faq-q" type="button" aria-expanded="false">
            <span data-i18n="fq4">Can you develop expired or underexposed film?</span>
            <svg class="chev" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>
          </button>
          <div class="faq-a"><p data-i18n="fa4">Absolutely — rescuing old rolls is one of our favourite jobs. For expired stock we may add compensating development or careful push/pull to lift the shadows. We'll look at the box and your story, recommend a plan, and check in before charging anything extra.</p></div>
        </div>
        <div class="faq-item rv">
          <button class="faq-q" type="button" aria-expanded="false">
            <span data-i18n="fq5">Where do you ship and do you take mail-in rolls?</span>
            <svg class="chev" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>
          </button>
          <div class="faq-a"><p data-i18n="fa5">We're in downtown Lisbon and accept mail-in rolls from anywhere in Portugal and the EU. Send rolls in a light-tight, padded box with a prepaid return label, and we ship negatives and prints back tracked. Scans arrive online first.</p></div>
        </div>
      </div>
    </div>
  </section>

  <section class="section" id="newsletter">
    <div class="container">
      <div class="nl rv">
        <span class="k" data-i18n="nlK">The negative letter</span>
        <h2 data-i18n="nlT">One dispatch, every other month</h2>
        <p data-i18n="nlP">A short letter with a film tip, a recommended stock and the frames we can't stop looking at. No inbox noise, and we never rent or sell the list.</p>
        <form class="nl-form" id="nlForm" novalidate>
          <label class="visually-hidden" for="nlEmail" data-i18n="nlLabel">Your email</label>
          <input id="nlEmail" type="email" name="email" data-i18n-ph="nlPh" data-i18n-aria="nlLabel" placeholder="you@example.com">
          <button class="btn btn-primary" type="submit" data-i18n="nlBtn">Subscribe</button>
        </form>
        <p class="nl-msg" id="nlMsg" role="status" aria-live="polite"></p>
      </div>
    </div>
  </section>
</main>

<footer class="footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <a class="brand" style="color:var(--stage-ink)" href="#hero">
          <svg viewBox="0 0 32 32" fill="none" aria-hidden="true"><rect x="3" y="5" width="26" height="20" rx="3" fill="none" stroke="currentColor" stroke-width="2"/><rect x="3" y="9" width="26" height="3.4" fill="var(--red)"/><circle cx="10" cy="7.6" r="1.7" fill="currentColor"/><circle cx="16" cy="7.6" r="1.7" fill="currentColor"/><circle cx="22" cy="7.6" r="1.7" fill="currentColor"/></svg>
          CAR<em>RE</em>TE
        </a>
        <p class="f-desc" data-i18n="fDesc">Analog film lab in downtown Lisbon. We develop, hand-scan and print — 35mm, 120 and large format — with care that shows.</p>
      </div>
      <div>
        <h5 data-i18n="fNavTitle">Lab</h5>
        <ul>
          <li><a href="#process" data-i18n="fNav1">The process</a></li>
          <li><a href="#stocks" data-i18n="fNav2">Film stocks</a></li>
          <li><a href="#pricing" data-i18n="fNav3">Pricing</a></li>
          <li><a href="#faq" data-i18n="fNav4">FAQ</a></li>
        </ul>
      </div>
      <div>
        <h5 data-i18n="fHorTitle">Hours</h5>
        <ul>
          <li><a href="#newsletter" data-i18n="fHor9">Tue – Sat · 10:00–19:00</a></li>
          <li><a href="#newsletter" data-i18n="fHor5">Sun – Mon · closed</a></li>
          <li><a href="#newsletter" data-i18n="fHor6">Drop-off sold all week</a></li>
        </ul>
      </div>
      <div>
        <h5 data-i18n="fContactTitle">Find us</h5>
        <ul>
          <li><a href="#main" data-i18n="fAdr">12 Rua do Alecrim<br>1200-017 Lisboa</a></li>
          <li><a href="mailto:ola@carrete.lab" data-i18n="fEmail">ola@carrete.lab</a></li>
        </ul>
      </div>
    </div>
    <div class="f-bot">
      <span data-i18n="fLegal1">Analog photography, developed in Lisbon.</span>
      <span data-i18n="fLegal2">© 2026 CARRETE LAB</span>
    </div>
  </div>
</footer>

<div class="cookie" id="cookieBanner" role="region" aria-label="Cookie notice">
  <p data-i18n="ckText">We use one small cookie to remember your language and theme. No tracking, promised.</p>
  <div class="ck-acts">
    <button class="ck-btn ck-ok" id="cookieOk" type="button" data-i18n="ckOk">Got it</button>
    <button class="ck-btn ck-no" id="cookieNo" type="button" data-i18n="ckNo">Essentials only</button>
  </div>
</div>

<script>
"""
