# UX/UI Review — CITA (2026-08-19)

1x1 de Cristian, 2026-08-21. `isFinalDesign` no está → bugfixes de interacción/contraste, sin rediseño de identidad.

## Resumen

Tres bugs de ESTA, todos corregidos en `/opt/data/landing-pages/2026-08-19-cita.html` (copiado a `proyectos-cristiancode-dev/landings/`).

## Mejoras implementadas

1. **Pricing CTAs muertos** — `Start free` / `Get started` eran `href="#"` (salto al top). Ahora apuntan a `#signup` (newsletter). Logo a `#main`. Cero `href="#"`.
2. **Nav móvil: pill invisible + CTA ausente a 390px** — dos causas:
   - `.mobile-menu a { color: var(--ink) }` (0,1,1) ganaba a `.btn-primary` (0,1,0) → `#242424` sobre `#242424` (1.00:1). En dark, `#f5f5f4` sobre `#f5f5f4`.
   - `.nav-actions > .btn-primary { display:none }` a ≤900px también escondía el CTA del drawer.
   Fix: quitar el hide genérico (el desktop ya tiene `.nav-desktop-only`) y override `.mobile-menu a.btn-primary { color: var(--cta-ink); background: var(--cta) }`.
3. **Hero Book inertes** — de `<span class="book">` a `<button type="button">` con demo (toggle Booked, `aria-pressed`, teclado). Booked blanco sobre `#0f6a32` = 6.71:1.
4. **Newsletter primer paint** — el markup salía con `class="nl-msg ok"` y `class="nl-msg err"`, así que se veían a la vez “Thanks…” y “Please enter a valid email.”. Ahora solo `nl-msg`; JS añade `ok`/`err` al submit.
5. **Cookie vs CTAs a 390px** — la barra fija full-bleed abajo (rect 708–828) tapaba Get started / Start free (810–859). En ≤700px se ancla bajo el nav (`--nav-h`); overlap medido = false. Desktop sigue bottom-right, no `left:1rem`.

## Verificación Puppeteer (390×844)

| Check | Resultado |
|---|---|
| Pricing hrefs | `#signup` / `#signup` |
| Drawer CTA light | visible, blanco sobre `#242424`, **15.52:1** |
| Drawer CTA dark | visible, `#111` sobre `#f5f5f4`, **17.31:1** |
| Book click | `BUTTON`, `aria-pressed=true`, texto Booked |
| `href="#"` | 0 |
| i18n | 83 keys × 6 idiomas, paridad OK |

## Paleta (sin cambios de identidad)

| Token | Light | Dark | Uso |
|---|---|---|---|
| `--cta` / `--cta-ink` | `#242424` / `#fff` | `#f5f5f4` / `#111` | pills primarios |
| Booked | `#0f6a32` / `#fff` | igual (fijo) | estado demo del mock |

## Pendiente

- No hay `isFinalDesign.true` — Cristian no lo pidió en este 1x1.
- Hero visual sigue `order:-1` en ≤900px (propuesta de valor debajo del mock). Fuera de alcance de este ticket.
