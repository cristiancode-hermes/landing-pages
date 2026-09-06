#!/usr/bin/env python3
"""Analyze contrast ratio in landing page HTML files - standalone check for meridian."""
import re, sys

def hex_to_rgb(h):
    h = h.lstrip('#')
    if len(h) == 3:
        h = ''.join(c*2 for c in h)
    if len(h) < 6:
        return None
    return tuple(int(h[i:i+2], 16) for i in (0,2,4))

def relative_luminance(r, g, b):
    def linearize(c):
        c = c/255.0
        return c/12.92 if c <= 0.04045 else ((c+0.055)/1.055)**2.4
    return 0.2126*linearize(r) + 0.7152*linearize(g) + 0.0722*linearize(b)

def contrast_ratio(c1, c2):
    l1, l2 = relative_luminance(*c1), relative_luminance(*c2)
    lighter, darker = max(l1,l2), min(l1,l2)
    return (lighter+0.05)/(darker+0.05)

path = "/opt/data/landing-pages/2026-07-27-meridian.html"
with open(path) as f:
    content = f.read()

# Extract light mode colors
light_colors = {}
for match in re.finditer(r'--color-([a-z-]+):\s*#?([0-9a-fA-F]{6})\b', content):
    key = match.group(1).strip()
    val = match.group(2).strip()
    if not key.endswith('-dark') and not key.endswith('-light') and not key.endswith('-hover') and not key.endswith('-ghost') and not key.endswith('-text'):
        if key in ('bg', 'surface', 'surface-alt', 'elevated', 'text-primary', 'text-secondary', 'text-tertiary', 'accent'):
            light_colors[key] = val

# Extract dark mode colors
dark_colors = {}
for match in re.finditer(r'--color-([a-z-]+-dark):\s*#?([0-9a-fA-F]{6})\b', content):
    key = match.group(1).strip().replace('-dark', '')
    val = match.group(2).strip()
    if key in ('bg', 'surface', 'text-primary', 'text-secondary', 'text-tertiary', 'accent'):
        dark_colors[key] = val

print("=" * 60)
print("  MERIDIAN — Contrast Check")
print("=" * 60)

def check_pair(label, fg_hex, bg_hex, mode):
    fg_rgb = hex_to_rgb(fg_hex)
    bg_rgb = hex_to_rgb(bg_hex)
    if not fg_rgb or not bg_rgb:
        print(f"  ? {label}: could not parse colors ({fg_hex}, {bg_hex})")
        return
    ratio = contrast_ratio(fg_rgb, bg_rgb)
    status = "✅" if ratio >= 4.5 else "⚠️" if ratio >= 3.0 else "❌"
    extra = ""
    if ratio < 4.5 and ratio >= 3.0:
        extra = " — large text OK, small text FAILS (needs 4.5:1)"
    elif ratio < 3.0:
        extra = " — FAILS (needs 3.0:1 minimum)"
    elif ratio >= 4.5:
        extra = " — WCAG AA pass"
    print(f"  {status} {mode} {label}: {fg_hex} on {bg_hex} = {ratio:.2f}:1{extra}")

print("\n  ── Light Mode ──")
bg = light_colors.get('bg', 'FFFFFF')
surface = light_colors.get('surface', bg)
check_pair("text-primary on bg", light_colors.get('text-primary', '000000'), bg, "☀️")
check_pair("text-secondary on bg", light_colors.get('text-secondary', '000000'), bg, "☀️")
check_pair("text-primary on surface", light_colors.get('text-primary', '000000'), surface, "☀️")
check_pair("text-secondary on surface", light_colors.get('text-secondary', '000000'), surface, "☀️")
check_pair("accent on bg", light_colors.get('accent', '000000'), bg, "☀️")
check_pair("accent-hover on bg", light_colors.get('accent-hover', '000000') if 'accent-hover' in light_colors else 'C8A055', bg, "☀️")

print("\n  ── Dark Mode ──")
bg_d = dark_colors.get('bg', '000000')
surface_d = dark_colors.get('surface', bg_d)
check_pair("text-primary on bg", dark_colors.get('text-primary', 'FFFFFF'), bg_d, "🌙")
check_pair("text-secondary on bg", dark_colors.get('text-secondary', 'FFFFFF'), bg_d, "🌙")
check_pair("text-primary on surface", dark_colors.get('text-primary', 'FFFFFF'), surface_d, "🌙")
check_pair("text-secondary on surface", dark_colors.get('text-secondary', 'FFFFFF'), surface_d, "🌙")
check_pair("accent on bg", dark_colors.get('accent', 'FFFFFF'), bg_d, "🌙")

print("\n  Done!")
