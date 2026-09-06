# UX/UI Review — 2026-08-16 MORADA

## Resumen

Landing page standalone para **MORADA**, una plataforma de tableros visuales de diseño de hogar donde parejas, familias y arquitectos diseñan habitaciones juntos en un lienzo compartido. **Día de plantilla de marca real**: se cargó el template **Miro** de popular-web-designs (última plantilla real usada: SpaceX/LYRA el 08-13) y se reprodujo fielmente su lenguaje visual de canvas colaborativo pastel — el contraste completo con las últimas páginas oscuras (pelagia navy, solstice neo-brutalista, lyra monocromo).

## Arquetipo de superficie (claude-design surface-first)

**Decide/Learn** (landing; hero correcto) con toques **Explore** en la galería de la comunidad y momento **Compare** en pricing. Declarado antes de escribir tokens: "esta página convence, no monitorea".

## Mejoras implementadas

1. **Hero con arte CSS puro (sin imagen de stock)** — el mockup de tablero colaborativo (pin de foto, 3 notas pastel, swatches, cursor flotante con animación) está construido íntegramente en CSS/HTML. Es el "product story" de Miro: el canvas ES el producto.
2. **Grid de features asimétrico de 12 columnas** — 5 paneles pastel de spans variados (coral 7, teal 5, yellow 5, rose 4, moss 3), cada uno con contenido distinto (moodboard mini, tira de paletas, burbujas de comentario, chips de habitación, tarjeta de share). Nunca un card grid idéntico.
3. **Tokens de CTA separados del azul interactivo** (`--blue-cta`) — el modo oscuro necesitaba un azul brillante para links (#7f92ff) pero ese mismo azul como fondo de botón rompía contraste AA (2.82:1). Se añadió `--blue-cta: #4a5fe0` (5.24:1 con label blanco) y `--blue-cta-hover: #3d50cf` (6.47:1). Mismo patrón en `.plan.featured` y `.cookie .accept`.
4. **ink-3 oscurecido** — `#83889a` (3.53:1) → `#666b7a` (5.32:1 en blanco, 4.97:1 en surface) para captions en light mode. Verificación completa: **35/35 pares texto/fondo pasan WCAG AA** en ambos temas.
5. **i18n 6 idiomas con paridad verificada por brace-counting** — 121 keys × 6 idiomas idénticos (se añadió `feat.2.pick`), 118 refs data-i18n todas resueltas, meta SEO traducida por idioma.
6. **Cookies y screenshots** — banner de cookies con delay 3s, bottom-right (no tapa CTAs), clave localStorage `morada-cookie`. Capturas con `evaluateOnNewDocument` para inyectar localStorage ANTES de que el timer del banner se arme.
7. **Selector de idioma tipo `<select>` (v2 feedback de Cristian)** — se reemplazaron los 6 botones de idioma seguidos (EN/ES/FR/DE/IT/PT) por un `<select>` nativo estilizado con nombres completos (English, Español, Français, Deutsch, Italiano, Português), chevron CSS, `appearance:none`, focus-visible AA. Dos instancias: nav (compacto ~110px) y menu móvil (ancho completo). `applyLanguage()` ahora sincroniza `sel.value` en ambos. QA con teclado (ArrowDown + Enter) y cambio desde el select del menú móvil verificado.
8. **Demo interactiva "Pick a color" (v2 feedback de Cristian)** — el strip de paleta estático era solo 5 colores fijos; el copy prometía "pick a color → build a full room palette". Ahora hay un botón "Pick a color" (icono cuentagotas) que abre un `<input type="color">` nativo, y al elegir un color se genera una paleta armónica de 5 tonos (base + análogos ±30° + complementario + tinte/sombra) vía conversión hex↔HSL. Los 5 swatches son clickeables y navegables por teclado (tabindex + Enter/Espacio), con `data-hex` para evitar el bug de `input.value = "rgb(...)"` (input color solo acepta hex y lo convertía a #000000). Animación `palBump` en el cambio; `prefers-reduced-motion` la desactiva. Key `feat.2.pick` añadida a los 6 idiomas (paridad 121×6 verificada).

## Fixes de bugs durante la revisión

- **meta-desc sin id** → `applyLanguage()` crasheaba (`Cannot read properties of null (reading 'setAttribute')`) y el IntersectionObserver nunca disparaba (opacity 0 en el hero). Añadido `id="meta-desc"`.
- **Captura mobile recortada** → el viewport de captura debe medir nav + hero (la nav sticky de 65px consume parte del viewport y recortaba el fondo del canvas). Ahora mide ambos y usa `Math.min(navHeight + heroHeight, 1200)`.

## Paleta (derivada de Miro)

| Token | Color | Uso |
|---|---|---|
| `--ink` | `#1c1c1e` | Texto primario (17:1) |
| `--ink-2` | `#555a6a` | Texto secundario (6.4:1) |
| `--ink-3` | `#666b7a` | Captions (5.3:1) |
| `--blue` | `#3f55d9` | Links/interactivo |
| `--blue-cta` | `#3f55d9` | Fill de botones (5.98:1) |
| `--blue-cta` (dark) | `#4a5fe0` | Fill de botones dark (5.24:1) |
| `--coral/--teal/--yellow/--rose/--moss` | pasteles | Superficies de features (6.3–8.6:1 con su ink del mismo hue) |

## Tipografía

Inter (sustituto de Roobert PRO del template Miro) 400–700, display con tracking −0.035em, hero `clamp(2.4rem, 5.4vw, 4.1rem)` (65.6px max < 96px), line-length prose ≤65ch.

## Notas de accesibilidad

- Contraste verificado con script Python (35 pares, ambos temas) — todos ≥4.5:1
- Toggles: 1 theme-toggle, 1 cookieOk (verificado sin duplicados)
- `prefers-reduced-motion` desactiva TODAS las animaciones
- Focus visible en botones y inputs (outline 2px blue)
- HTML semántico (h1→h3, sections con aria-labels, details/summary para acordeones)

## Slop diagnostic (claude-design 10-tell)

**Score: 0.5/10** — ningún tell disparado. El único backdrop-filter es el blur del nav sticky (elevación funcional para legibilidad, no glassmorphism decorativo). Azul interactivo = elección de marca del template Miro, no hue genérico. Tipografía = Inter por sustitución de template (Roobert PRO no está en CDN), no default.

## Pendiente para futura iteración

- [ ] Añadir modo tour/onboarding de primer board (empty state del producto)
- [ ] Variantes de canvas (fondo papel, modo presentación)