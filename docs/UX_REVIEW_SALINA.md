# UX/UI Review — SALINA (2026-08-25) · 1×1

## Resumen
Revisión puntual de la carta de mar (newsletter) y del muted-on-dark. El mailto se pintaba como HTML crudo; el faint de light se reutilizaba como texto sobre `#0F252B`.

## Mejoras implementadas
1. **`news.honest` vía `data-i18n-html`** — el string lleva `<a href="mailto:hola@salinas.es">`. `textContent` lo escapaba. Ahora `innerHTML` + key en `HTML_KEYS`.
2. **EN ya no hereda ES/PT/IT/DE/FR** — el bloque `en` tenía 5 `news.honest` apilados (gana el último = ES). Queda una sola cadena en inglés.
3. **Muted-on-dark `#B5C9C6`** — `--teal-faint` dark pasa de `#3A4B4F` (1.74:1 sobre `#0F252B`) a `#B5C9C6` (9.19:1). El fondo de footer/prov no se toca.
4. **Cookie OK con tinta fija** — el botón blanco ya no usa `color:var(--teal)` (en dark `#7FA7A2` sobre `#fff` = 2.64:1). Texto `#0F252B` en ambos temas (~15.9:1).
5. **Estrellas del shop en fila** — vivían en `.who` pero el CSS solo dimensionaba `.listing .meta .star svg`. Los SVG sin size (default 300×150) se apilaban en vertical. Ahora `.listing .star` es `inline-flex nowrap` con SVG 13×13.

## Paleta (dark, bandas fijas)
| Token | Color | Uso | Contraste |
|---|---|---|---|
| footer/prov bg | `#0F252B` | banda (sin cambio) | — |
| `--teal-faint` dark | `#B5C9C6` | muted text on band | 9.19:1 |
| cookie OK ink | `#0F252B` | texto sobre `#fff` | 15.91:1 |

## Notas de accesibilidad
- Mailto clicable, visible como enlace (no markup crudo).
- Muted footer/prov cumple WCAG AA (small text).
- Cambiar idioma ES/EN/FR vuelve a inyectar el `<a>` real.

## Pendiente
- Nada bloqueante. Recapture de portfolio no hace falta: el hero light no cambia.
