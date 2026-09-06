#!/usr/bin/env python3
"""Analyze contrast ratio in landing page HTML files."""
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

landings = [
    ("veridian-carbon", "/opt/data/landing-pages/2026-07-27-veridian-carbon.html"),
    ("forma-and-space", "/opt/data/landing-pages/2026-07-23-forma-and-space.html"),
    ("nexus-gaming", "/opt/data/landing-pages/2026-07-23-nexus-gaming.html"),
    ("kairos-academy", "/opt/data/landing-pages/2026-07-24-kairos-academy.html"),
    ("ora-wellness", "/opt/data/landing-pages/2026-07-25-ora-wellness.html"),
    ("ember-and-vine", "/opt/data/landing-pages/2026-07-26-ember-and-vine.html"),
    ("northbound-outdoors", "/opt/data/landing-pages/2026-07-26-northbound-outdoors.html"),
]

for name, path in landings:
    with open(path) as f:
        content = f.read()
    
    colors = {}
    for match in re.finditer(r'--color-([a-z-]+):\s*#?([0-9a-fA-F]{3,8})\b', content):
        key, val = match.groups()
        colors[key.strip()] = val.strip()
    
    # Detect dark vs light mode
    is_dark = any('dark' in k and '#' in v for k, v in colors.items() if '#0' in v or '000' in v)
    
    # Default bg/text if not found
    bg = colors.get('bg', 'ffffff')
    text_primary = colors.get('text-primary', '000000')
    text_secondary = colors.get('text-secondary', text_primary)
    text_tertiary = colors.get('text-tertiary', text_secondary)
    surface = colors.get('surface', bg)
    heading_color = colors.get('text-heading') or colors.get('heading') or text_primary
    
    print(f"\n{'='*50}")
    print(f"  {name} {'🌙' if is_dark else '☀️'}")
    print(f"{'='*50}")
    
    pairs = [
        ("text-primary on bg", text_primary, bg),
        ("text-secondary on bg", text_secondary, bg),
        ("heading on bg", heading_color, bg),
        ("text-primary on surface", text_primary, surface),
        ("text-secondary on surface", text_secondary, surface),
    ]
    
    for label, fg, bg_c in pairs:
        try:
            fg_rgb = hex_to_rgb(fg)
            bg_rgb = hex_to_rgb(bg_c)
            if not fg_rgb or not bg_rgb:
                continue
            ratio = contrast_ratio(fg_rgb, bg_rgb)
            status = "✅" if ratio >= 4.5 else "⚠️" if ratio >= 3.0 else "❌"
            print(f"  {status} {label}: {fg} on {bg_c} = {ratio:.2f}:1", end="")
            if ratio < 4.5:
                print(f" — FAILS WCAG AA (needs 4.5:1)", end="")
            print()
        except Exception as e:
            print(f"  ? {label}: ERROR {e}")
    
    # Also check dark mode
    for mode in ('dark', 'light'):
        mode_colors = {}
        section = re.search(r'/\* {3,}Colors — (\w+ Mode)', content)
        if section:
            mode_start = section.start()
            mode_end = content.find('*/', mode_start)
            mode_section = content[mode_start:mode_end]
            for match in re.finditer(r'--color-([a-z-]+):\s*#?([0-9a-fA-F]{3,8})\b', mode_section):
                key, val = match.groups()
                mode_colors[key.strip()] = val.strip()
            if mode_colors:
                print(f"  [{mode} mode specific]")

print("\nDone!")
