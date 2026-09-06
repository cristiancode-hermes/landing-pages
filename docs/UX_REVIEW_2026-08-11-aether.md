# UX Review — 2026-08-11 AETHER Motors

**File:** `/opt/data/landing-pages/2026-08-11-aether-motors.html` (129 KB)
**Family/Style:** Automotive · precision poster / technical-drawing editorial (original, no brand template — the popular-web-designs catalog has no food/auto brand that fit; committed to an original "premium coachbuilder" aesthetic instead).
**Surface (claude-design):** Decide/Learn (primary) with a Compare sub-surface (trim spec table) and a Configure sub-surface (commission form). State: hero is correct here; no hero+3-card grid anywhere.

## Anti-repetition registry (audited 18 prior files)
- Restaurant+gold+brown taken (ember-and-vine) → picked **Automotive** (never used).
- Used dark accents: lime, green+blue, indigo+amber, gold, bronze, teal, rainbow → **racing red on carbon** is virgin.
- Fonts used: Cormorant, Anton+Space Mono, DM Sans/Serif, Fraunces, Barlow, Inter, Sora, Playfair, Bitter, Space Grotesk → **Bebas Neue + Figtree + IBM Plex Mono** (all fresh).
- All prior pages used opacity-fade reveals → **clip-path wipe reveal** + mouse parallax + magnetic buttons.

## Palette (OKLCH-informed, WCAG-verified)
- Light: `--bg #f5f5f2` (chroma ≈0), `--ink #15161a` (16.5:1), `--muted #565b63` (6.3:1), `--accent #d42b12`, `--accent-ink #b9200a` (6.1:1 on bg; white on it 6.6:1).
- Dark: `--bg #0e0f12`, `--ink #eef0f2` (16.8:1), `--muted #a0a5ad` (7.7:1), `--accent #ff4d2e` (5.8:1 on bg), button = bright accent + dark text (5.8:1).
- Strategy: **Committed** (carbon neutral + single racing-red accent ≤10%).

## Slop self-audit (10-tell)
Score **1/10** pre-final (generic-tech-hue: no — red chosen for brand; feature-grid: no; accent rail: no; glass: none; monument stats: no — spec strip is small mono text; icon topper: no; center stack: no — asymmetric 5/7 grid; default type: no — Bebas/Figtree/Plex Mono chosen; wrong surface: no). Only residual tell: none after fixes. Re-scored **0/10** post-fix.

## Real bugs found & fixed during QA (browser-verified)
1. **`data-i18n` on icon buttons** wrote visible textContent ("Toggle colour theme" wrapping over the header). Fix: `data-i18n-aria` attribute → sets aria-label only. Also **`.visually-hidden` utility was never defined**, exposing the lang label. Both fixed.
2. **Callout 3 overlapped the car tail** in the hero art. Repositioned to empty sky above the rear deck.
3. **CRITICAL — IntersectionObserver + clip-path = dead reveals.** Chromium computes IO intersection *including* `clip-path`: a fully-clipped `.wipe` element (inset 0 100%) reports 0% intersection and **never fires**, so all below-fold content would stay invisible forever. Proven empirically (rect in viewport, IO false; plain element, IO true). Fix: reveal driven by a rAF-throttled scroll handler checking `getBoundingClientRect().top < vh*0.92` (geometry unaffected by clip-path). Verified 42/42 reveals fire on scroll.
4. **CSS cascade bug on mobile hero:** the new `@media (max-width:820px)` block was placed *before* the base `.hero-grid` rule → equal specificity, later rule wins → two-column grid persisted at 390px with callouts overlapping the copy. Fix: moved the media block after the base rules. Verified via Puppeteer probe: 390px → `grid-template-columns: 342px`, callouts `display:none`, art below text.
5. **Strip redundancy:** announcement strip repeated the hero kicker; replaced right side with `WWW.AETHER.MOTORS`.

## Verification
- `validate-landing.py`: JS syntax OK · **157 keys × 6 langs, 0 missing, equal counts** · banned patterns CLEAN.
- Browser: **0 console errors**; ES/EN/FR/DE/IT/PT switch live (title/desc/OG/Twitter/lang attr + all visible strings); dark/light toggle persists via shared `kairos-theme` key; FAQ accordion (aria-expanded + grid-rows), trim CTA → preselects model radio, form validation (empty/bad email/success states), mobile menu, cookie banner, reveals 42/42.
- Contrast: all pairs ≥4.5:1 (light & dark) via independent checker.
- Screenshots: `screenshots/aether-desktop.png` (71.6 KB) + `aether-mobile.png` (39.5 KB) — hero viewport, light-forced, EN-locked; both verified visually (desktop: clean header, no overlap, premium; mobile: clean stack, no callouts, no overflow). Copied to portfolio `assets/landing-aether-motors.png`; portfolio `npm run build` → 1354 pages.

## Components delivered
Announcement strip · fixed header (lang select + theme toggle + mobile menu) · hero with inline-SVG GT technical drawing + 3 callouts + parallax + speed-line draw-in · spec strip (4, quiet mono) · editorial statement + FIG.01 chassis cutaway · **Compare** trim table (GT/GT-S/ONE, hot column, "Reserve" → preselects form) · atelier rows ×2 with SVG figures (brake disc, cabin) + spec pills · genuine 4-step process strip · asymmetric owner quotes · FAQ accordion (6) · commission form (model radios + 6 colour swatches + country + validation) · newsletter strip · 4-column footer · cookie banner (aether-cookie).

## Notes for next run
- If a future page uses clip-path reveals, do NOT pair them with IntersectionObserver (Chromium clips intersection). Scroll-position handler is the safe pattern; or keep reveals as opacity/transform only.
- Media queries must come AFTER the base rules they override — verify by computed-style probe at breakpoint, not by eye.
