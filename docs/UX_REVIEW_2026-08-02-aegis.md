# UX Review — Aegis Landing Page (2026-08-02)

## Product
**Aegis** — self-custody crypto savings platform (bitcoin + stablecoins, daily yield, audited smart contracts).

## Design Direction
- **Brand template:** Coinbase (from `popular-web-designs` skill) — clean, trustworthy fintech: blue/white/near-black binary palette, 56px pill CTAs, ultra-tight 1.0 display line-height, minimal shadow system with depth from section contrast.
- **Surface archetype (claude-design):** **Decide/Learn** — landing page where the hero is earned: asymmetric composition (copy left, live portfolio preview card right), NOT center-stack. Secondary **Compare** surface: full comparison table (Aegis vs traditional bank) as the "why us" proof.
- **Family:** Crypto/Fintech (first time used in the landing-pages collection).

## Design System
- **Colors (Committed strategy):** Coinbase Blue `#0052ff` as the *only* functional accent (CTAs, links, active states, chart line, checkmarks) on white `#ffffff` / near-black `#0a0b0d` surfaces, cool-gray `#eef0f3` secondary surfaces, dark cards `#282b31`. In dark mode the blue lightens to `#578bfa` to hold 7:1 contrast on `#0a0b0d`.
- **Typography:** DM Sans (CoinbaseDisplay/Sans substitute) — display 400 weight at 1.0 line-height, body 400/600. Mono stack (`ui-monospace…`) for all financial figures (balance, APY, ticker prices).
- **Contrast:** body `#0a0b0d` on white = 21:1; muted `#5b616e` = 5.3:1; blue text on white = 5.9:1; blue on dark = 7:1. All ≥ WCAG AA.
- **Motion:** marquee price ticker (pauses on hover), count-up stats (ease-out-quart), SVG chart stroke-draw, scroll reveals (IntersectionObserver), pill hover micro-interactions. Every animation has a `prefers-reduced-motion` fallback; content is never gated behind animation.

## Anti-Slop Self-Audit (impeccable + claude-design 10-tell)
Score: **1/10** (no compositional tells).
- ✅ No gradient text, no glassmorphism, no accent rails, no icon toppers, no eyebrow-on-every-section, no numbered section markers (the 3-step process is a *real* sequence, so its STEP 01/02/03 labels are earned), no default Inter (DM Sans chosen via Coinbase template), no generic indigo.
- ✅ The "hero metric" template avoided: hero leads with a benefit statement + product mockup; stats live in a quiet strip below, not in the hero.
- ✅ Identical card grids avoided: process uses bordered steps, security uses a 2×2 icon grid on dark, testimonials use an asymmetric 1-lead + 2-stack composition, compare uses a real table.

## Implementation Notes / Fixes Made During QA
1. **Cookie banner occlusion (found via browser_vision):** initially bottom-left, it covered the hero CTAs on desktop and the headline on mobile. Moved to bottom-right, slimmed, and delayed to 3.2s so first-view content is unobstructed.
2. **Count-up data-loss bug (found via accessibility snapshot):** the balance count-up wrote `textContent` on the parent, destroying the inline `+12.4%` pill. Fixed by wrapping the number in its own `<span data-count>` so number and pill are siblings.
3. **Count-up formatter bug:** `€1.8B` would animate to `€1800.0M` and `2,840,000` to `2.8M`. Rewrote the formatter with explicit B / M / locale branches.
4. **Floating chip overlap:** the "Your keys, on-device" chip overlapped the change pill; repositioned above the card edge.
5. **Missing `.visually-hidden`:** table caption class was referenced but undefined; added the utility.
6. **Mobile hero order:** card was `order: -1` (before the copy); removed so the value proposition leads on mobile.

## Verification
- `node --check` on extracted JS: **syntax OK**.
- Browser console: **0 errors** after full page load.
- i18n: all 6 languages switch live, key sets identical (~122 keys/lang), all 114 `data-i18n` refs resolve; SEO meta (title/desc/OG/Twitter) per language; browser-language detection + localStorage persistence.
- Theme: light/dark toggle persists via shared `kairos-theme` key (capture pipeline compatible).
- Screenshots: `screenshots/aegis-desktop.png` (113KB) and `aegis-mobile.png` (55KB) — both well above the 18KB failure threshold; visually verified via vision analysis (hero, dark mode, mobile).

## Components Delivered
Sticky nav with language select + theme toggle + mobile menu · asymmetric hero with animated portfolio preview (chart + allocations) · price marquee ticker · stats strip (count-up) · 3-step process · comparison table (Aegis vs bank) · dark security section (2×2) · asymmetric testimonials · FAQ accordion (6) · CTA band with newsletter validation · 4-column footer · delayed cookie banner. No floating CTA (would fight the cookie banner corner); cookie banner fills that role.
