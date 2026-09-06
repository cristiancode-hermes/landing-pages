#!/usr/bin/env python3
"""Validate the STATIC landing page: i18n completeness, banned patterns, z-index."""
import re

path = '/opt/data/landing-pages/2026-08-01-static-records.html'
with open(path, encoding='utf-8') as f:
    html = f.read()

print(f"File size: {len(html)/1024:.1f} KB")
print(f"Lines: {html.count(chr(10))}")

# Parse JS object literal: split into language blocks, extract quoted keys per block
m = re.search(r'var I18N = \{(.*?)\n      \};', html, re.S)
assert m, "I18N dict not found"
body = m.group(1)

# Top-level language blocks: en: { ... }, es: { ... }
lang_blocks = re.findall(r'^\s{8}([a-z]{2}): \{(.*?)\n\s{8}\},?$', body, re.S | re.M)
langs = [b[0] for b in lang_blocks]
print(f"Languages found: {langs}")
assert len(langs) == 6, f"expected 6 languages, got {len(langs)}"

key_sets = []
for name, block in lang_blocks:
    keys = set(re.findall(r"^\s{10}([A-Za-z0-9_]+):", block, re.M))
    key_sets.append(keys)
    print(f"  {name}: {len(keys)} keys")

base = key_sets[0]
ok = True
for i, ks in enumerate(key_sets[1:], 1):
    missing = base - ks
    extra = ks - base
    if missing or extra:
        ok = False
        print(f"  MISMATCH in {langs[i]}: missing={missing} extra={extra}")
assert ok, "language key mismatch!"
print(f"Keys per language: {len(base)} — all 6 languages consistent")

attrs = set(re.findall(r'data-i18n="([^"]+)"', html))
# Keys referenced dynamically in JS (e.g. I18N[currentLang].newsErr)
js_used = set(re.findall(r'\.([A-Za-z0-9_]+)\b', re.search(r'function initNewsletter\(\).*?function initCookie\(\)', html, re.S).group(0)))
missing_attrs = attrs - base
extra_attrs = base - attrs - {'metaTitle','metaDesc','ogTitle','ogDesc','twTitle','twDesc'} - js_used
print(f"data-i18n attrs used: {len(attrs)}")
print(f"keys used dynamically in JS: {sorted(js_used & base)}")
print(f"attrs without dict entry: {missing_attrs if missing_attrs else 'none'}")
print(f"dict keys never used in HTML or JS (non-meta): {extra_attrs if extra_attrs else 'none'}")
assert not missing_attrs, "orphan data-i18n attrs!"
assert not extra_attrs, "unused dict keys!"

ph = set(re.findall(r'data-i18n-placeholder="([^"]+)"', html))
print(f"placeholder keys: {ph - base if ph - base else 'all valid'}")
assert not (ph - base), "bad placeholder key!"

assert 'lorem' not in html.lower(), "LOREM FOUND!"
print("No lorem ipsum")

banned = {
    'gradient text': r'background-clip:\s*text',
    'glassmorphism': r'backdrop-filter',
    'side-stripe': r'border-left:\s*[2-9]px',
}
for name, pat in banned.items():
    hits = re.findall(pat, html, re.I)
    print(f"banned [{name}]: {'FOUND ' + str(len(hits)) if hits else 'clean'}")
    assert not hits, f"banned pattern: {name}"

z = sorted(set(int(x) for x in re.findall(r'z-index:\s*(\d+)', html)))
print(f"z-index values: {z}")
assert max(z) <= 70, "z-index too high!"
print("z-index scale sane")

print("\nALL CHECKS PASSED")
