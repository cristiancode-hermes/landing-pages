import re, sys
from pathlib import Path
html = Path('/opt/data/landing-pages/2026-08-25-salina.html').read_text()
langs = ['en','es','fr','de','it','pt']

def extract_block(src, lang):
    m = re.search(r'^\s*%s:\s*\{' % re.escape(lang), src, re.M)
    if not m: return None
    depth = 0; j = m.end() - 1
    while j < len(src):
        c = src[j]
        if c == '{': depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0: return src[m.end()-1:j+1]
        j += 1
    return None

def keys_of(b): return set(re.findall(r"'([A-Za-z][A-Za-z0-9.]+)':", b))

blocks = {l: keys_of(extract_block(html,l)) for l in langs}
# dedupe: naive block extractor may over-capture if urls contain braces; paranoia check
base = blocks['en']
ok = True
for l in langs:
    miss = base - blocks[l]; extra = blocks[l] - base
    print(f"{l}: {len(blocks[l])} keys miss={len(miss)} extra={len(extra)}")
    if miss: print('  MISSING', sorted(miss)); ok=False
    if extra: print('  EXTRA(keys above)', sorted(extra))
print('PARITY:', 'OK' if ok else 'FAIL')
refs = set(re.findall(r'data-i18n(?:-html|-aria|-ph)?="([^"]+)"', html))
un = refs - base
print('HTML refs:', len(refs), 'unresolved:', len(un))
if un: print('  UNRESOLVED', sorted(un)); ok=False
print('DICT-only (JS-applied):', sorted(k for k in base if k not in refs))
sys.exit(0 if ok else 2)
