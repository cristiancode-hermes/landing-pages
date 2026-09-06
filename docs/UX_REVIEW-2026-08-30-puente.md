# UX/UI Review — PUENTE (2026-08-30)

## Resumen
1×1 de contraste en dark más tres extras. No es rediseño; `isFinalDesign` no se marca.

## Mejoras implementadas
1. **Dark `--teal` como texto (~1.49:1)** — `--teal` `#0B3D4A` se queda como fill del CTA. En dark, `.fit-num`, `.faq-q .ic` y `.lang-select__opt[aria-selected="true"]` usan `color: var(--link)` (`#8EC9D4`, ~9.6:1) sobre `--bg`/`--card`. Se cambia el TEXTO, no el fondo.
2. **Check del idioma** — `content:'\\2713'` (doble escape) pintaba el literal `\2713`. Ahora `content:'\2713'`.
3. **mailto NXDOMAIN** — `cita@puente.madrid` no resuelve. Buzón: `puente@cristiancode.dev`.
4. **Subject del CTA «Escribir para reservar»** — `visit.mail_subject` en 6 idiomas; `applyLang()` reescribe `#visitMail` href.

## Paleta (relevante)
| Token | Light | Dark | Uso |
|---|---|---|---|
| `--teal` / `--cta` | `#0B3D4A` | `#0B3D4A` | fill CTA, no texto sobre card oscura |
| `--link` | `#0B3D4A` | `#8EC9D4` | links + números/iconos accent en dark |
| `--bg` / `--card` | `#F3F5F7` / `#FFF` | `#0C1114` / `#141A1E` | canvas |

## Notas de accesibilidad
- Teal-on-card dark 1.49:1 → link-on-card ~9.6:1 (AA).
- Verificar `.fit-num`, `.faq-q .ic` y opción de idioma seleccionada en dark antes de isFinalDesign.
