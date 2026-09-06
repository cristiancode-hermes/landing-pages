#!/usr/bin/env python3
# Composes the CARRETE landing page: loads HEAD+CSS+BODY from _build_carrete.py
# and appends the I18N object + JS, then writes the final file.
import os, importlib.util

spec = importlib.util.spec_from_file_location("b", "/opt/data/landing-pages/_build_carrete.py")
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)

out = b.out
HEAD, CSS, BODY = b.HEAD, b.CSS, b.BODY

JS_BODY = r"""
var SHORT_TITLES = {
  es: { t: "CARRETE — Laboratorio analógico de fotografía", d: "Laboratorio analógico en el centro de Lisboa. Revelamos, digitalizamos y positivamos tus carretes — 35mm, 120 y gran formato — con cuidado y plazos honestos." },
  en: { t: "CARRETE — Analog film, developed with care", d: "CARRETE is an analog photo lab in Lisbon. We develop, hand-scan and print your film rolls — 35mm, 120 and 4x5 — with emulsion-level care." },
  fr: { t: "CARRETE — Laboratoire argentique", d: "CARRETE est un laboratoire argentique au centre de Lisbonne. Nous développons, scannons et tirons vos pellicules — 35mm, 120 et grand format." },
  de: { t: "CARRETE — Analoges Fotolabor", d: "CARRETE ist ein analoges Fotolabor in der Innenstadt von Lissabon. Wir entwickeln, scannen und drucken deine Filme — 35mm, 120 und Großformat." },
  it: { t: "CARRETE — Laboratorio fotografico analogico", d: "CARRETE è un laboratorio analogico nel centro di Lisbona. Sviluppiamo, scansioniamo e stampiamo i tuoi rullini — 35mm, 120 e grande formato." },
  pt: { t: "CARRETE — Laboratório fotográfico analógico", d: "A CARRETE é um laboratório analógico no centro de Lisboa. Revelamos, digitalizamos e positivamos os seus rolos — 35mm, 120 e grande formato." }
};
var LS_KEY='carrete-lang';
var THEME_KEY='kairos-theme';
var CK_KEY='carrete-cookie';
document.documentElement.classList.remove('no-js');

function detectLang(){
  var s=null;try{s=localStorage.getItem(LS_KEY);}catch(e){}
  if(s&&I18N[s])return s;
  var nav=(navigator.language||'en').toLowerCase().slice(0,2);
  return I18N[nav]?nav:'en';
}
function setLang(lang){
  var t=I18N[lang];
  document.documentElement.lang=lang;
  var title=document.getElementById('doc-title');if(title&&SHORT_TITLES[lang])title.textContent=SHORT_TITLES[lang].t;
  var desc=document.getElementById('meta-desc');if(desc&&SHORT_TITLES[lang])desc.setAttribute('content',SHORT_TITLES[lang].d);
  var ogt=document.querySelector('meta[property="og:title"]');if(ogt&&SHORT_TITLES[lang])ogt.setAttribute('content',SHORT_TITLES[lang].t);
  var ogd=document.querySelector('meta[property="og:description"]');if(ogd&&SHORT_TITLES[lang])ogd.setAttribute('content',SHORT_TITLES[lang].d);
  document.querySelectorAll('[data-i18n]').forEach(function(el){
    var k=el.getAttribute('data-i18n');if(t[k]!==undefined)el.innerHTML=t[k];
  });
  document.querySelectorAll('[data-i18n-ph]').forEach(function(el){
    var k=el.getAttribute('data-i18n-ph');if(t[k]!==undefined)el.setAttribute('placeholder',t[k]);
  });
  document.querySelectorAll('[data-i18n-aria]').forEach(function(el){
    var k=el.getAttribute('data-i18n-aria');if(t[k]!==undefined)el.setAttribute('aria-label',t[k]);
  });
  document.querySelectorAll('.lang-select__cur').forEach(function(el){el.textContent=lang.toUpperCase();});
  document.querySelectorAll('.lang-select__opt').forEach(function(opt){
    opt.setAttribute('aria-selected',opt.getAttribute('data-lang')===lang?'true':'false');
  });
  try{localStorage.setItem(LS_KEY,lang);}catch(e){}
}
function closeLangMenus(){
  document.querySelectorAll('.lang-select').forEach(function(sel){
    var m=sel.querySelector('.lang-select__menu'),bb=sel.querySelector('.lang-select__btn');
    if(m)m.classList.remove('open');if(bb)bb.setAttribute('aria-expanded','false');
  });
}
document.querySelectorAll('.lang-select').forEach(function(sel){
  var bb=sel.querySelector('.lang-select__btn'),m=sel.querySelector('.lang-select__menu');
  if(!bb||!m)return;
  bb.addEventListener('click',function(e){e.stopPropagation();var open=m.classList.toggle('open');bb.setAttribute('aria-expanded',open?'true':'false');});
  m.querySelectorAll('.lang-select__opt').forEach(function(o){
    o.addEventListener('click',function(){setLang(o.getAttribute('data-lang'));closeLangMenus();});
  });
});
document.addEventListener('click',function(e){
  var inside=false;
  document.querySelectorAll('.lang-select').forEach(function(sel){if(sel.contains(e.target))inside=true;});
  if(!inside)closeLangMenus();
});
document.addEventListener('keydown',function(e){if(e.key==='Escape')closeLangMenus();});

function applyTheme(th){
  document.documentElement.setAttribute('data-theme',th);
  try{localStorage.setItem(THEME_KEY,th);}catch(e){}
}
function initTheme(){
  var s=null;try{s=localStorage.getItem(THEME_KEY);}catch(e){}
  applyTheme(s==='dark'?'dark':'light');
  var bt=document.getElementById('themeToggle');
  if(bt)bt.addEventListener('click',function(){
    var cur=document.documentElement.getAttribute('data-theme')==='dark'?'dark':'light';
    applyTheme(cur==='dark'?'light':'dark');
  });
}

var burger=document.getElementById('burger'),mmenu=document.getElementById('mobileMenu');
if(burger&&mmenu){
  burger.addEventListener('click',function(){
    var open=mmenu.classList.toggle('open');
    burger.setAttribute('aria-expanded',open?'true':'false');
  });
}

/* FAQ accordion */
document.querySelectorAll('.faq-item').forEach(function(item){
  var q=item.querySelector('.faq-q'),a=item.querySelector('.faq-a');
  if(!q||!a)return;
  q.addEventListener('click',function(){
    var open=item.classList.contains('open');
    document.querySelectorAll('.faq-item.open').forEach(function(o){
      o.classList.remove('open');
      var oq=o.querySelector('.faq-q'),oa=o.querySelector('.faq-a');
      if(oq)oq.setAttribute('aria-expanded','false');
      if(oa)oa.style.maxHeight='0';
    });
    if(!open){item.classList.add('open');q.setAttribute('aria-expanded','true');a.style.maxHeight=a.scrollHeight+'px';}
  });
});

/* Reveal on scroll (rAF throttle, geometry-based) */
var revealEls=document.querySelectorAll('.rv');
function revealCheck(){
  var vh=window.innerHeight||document.documentElement.clientHeight;
  revealEls.forEach(function(el){
    if(el.classList.contains('in'))return;
    var r=el.getBoundingClientRect();
    if(r.top<vh*0.92&&r.bottom>0)el.classList.add('in');
  });
}
var revealTicking=false;
function onScrollReveal(){
  if(revealTicking)return;revealTicking=true;
  requestAnimationFrame(function(){revealTicking=false;revealCheck();});
}
window.addEventListener('scroll',onScrollReveal,{passive:true});
onScrollReveal();

/* Newsletter */
var nlForm=document.getElementById('nlForm'),nlMsg=document.getElementById('nlMsg');
if(nlForm&&nlMsg){
  nlForm.addEventListener('submit',function(e){
    e.preventDefault();
    var em=nlForm.querySelector('input[type=email]');
    var cur=document.documentElement.lang||'en';
    var ok=em&&/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(em.value);
    nlMsg.className='nl-msg '+(ok?'ok':'err');
    nlMsg.textContent=I18N[cur][ok?'nlOk':'nlErr'];
    if(ok){nlForm.reset();try{localStorage.setItem('carrete-sub','1');}catch(e){}}
  });
}

/* Cookie banner */
var ck=document.getElementById('cookieBanner');
function showCookie(){if(ck)ck.classList.add('show');}
function hideCookie(){if(ck)ck.classList.remove('show');}
function setCookieSeen(){try{localStorage.setItem(CK_KEY,'1');}catch(e){}}
(function(){
  if(!ck)return;
  var seen=null;try{seen=localStorage.getItem(CK_KEY);}catch(e){}
  if(seen){ck.style.display='none';return;}
  var tm=setTimeout(function(){if(!document.hidden)showCookie();},2600);
  var ok=document.getElementById('cookieOk'),no=document.getElementById('cookieNo');
  if(ok)ok.addEventListener('click',function(){setCookieSeen();hideCookie();clearTimeout(tm);});
  if(no)no.addEventListener('click',function(){setCookieSeen();hideCookie();clearTimeout(tm);});
})();

/* Boot */
setLang(detectLang());
initTheme();
"""

with open("/opt/data/landing-pages/_i18n_carrete.json", encoding="utf-8") as f:
    I18N_JSON = f.read()

# Replace guards for JSON->JS: we already emitted as JS in the JSON file? No — JSON.
# We'll convert the JSON string into a JS object literal by wrapping and stripping quotes on keys.
import json
data = json.loads(I18N_JSON)

def js_obj(d, indent="  "):
    parts=[]
    for k,v in d.items():
        parts.append(indent*2+'%s: "%s"'%(k, v.replace('\\','\\\\').replace('"','\\"')))
    return "{\n" + ",\n".join(parts) + "\n" + indent + "}"

langs = ["es","en","fr","de","it","pt"]
segments = ["var I18N = {"]
for L in langs:
    seg = data[L]
    # inject short-titles/meta come from SHORT_TITLES at runtime; but validation
    # requires meta_title/meta_desc keys present in each section. Add them.
    st = SHORT_TITLES_META = {
      "es":("CARRETE — Laboratorio analógico de fotografía","Laboratorio analógico en el centro de Lisboa. Revelamos, digitalizamos y positivamos tus carretes."),
      "en":("CARRETE — Analog film, developed with care","CARRETE is an analog photo lab in Lisbon. We develop, hand-scan and print your film rolls with care."),
      "fr":("CARRETE — Laboratoire argentique","CARRETE est un laboratoire argentique au centre de Lisbonne."),
      "de":("CARRETE — Analoges Fotolabor","CARRETE ist ein analoges Fotolabor in der Innenstadt von Lissabon."),
      "it":("CARRETE — Laboratorio fotografico analogico","CARRETE è un laboratorio analogico nel centro di Lisbona."),
      "pt":("CARRETE — Laboratório fotográfico analógico","A CARRETE é um laboratório analógico no centro de Lisboa.")
    }[L]
    full = {"meta_title": st[0], "meta_desc": st[1]}
    full.update(seg)
    segments.append("  %s: %s,\n" % (L, js_obj(full, indent="  ")))
segments.append("};")
I18N_JS = "\n".join(segments)

html = HEAD + CSS + BODY + I18N_JS + "\n" + JS_BODY + "\n</script>\n</body>\n</html>\n"

os.makedirs("/opt/data/landing-pages", exist_ok=True)
with open(out, "w", encoding="utf-8") as f:
    f.write(html)
print("WROTE", out, len(html), "bytes")
