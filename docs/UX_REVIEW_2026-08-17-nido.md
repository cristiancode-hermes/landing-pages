# UX/UI Review — NIDO (2026-08-17)

## Resumen

Landing page de marketplace inmobiliario/hostelería **NIDO** ("quédate donde se sienta tuyo") generada por el cron diario. Se usó la plantilla real de **Airbnb** de popular-web-designs (3ª página desde Miro → patrón "every 3rd/4th page usa un brand template"). Archivo: `2026-08-17-nido.html` (165 KB).

## Decisiones de diseño

**Surface-first (claude-design):** superficie **Explore** — la composición es una experiencia de búsqueda (search card + chips de categoría + grid de listings), NO un hero-monumento. Sin hero-metrics, sin cards idénticas, sin center-stack.

**Paleta (fiel a Airbnb):** lienzo blanco `#fff`, tinta cálida `#222222`, acento único Rausch Red `#FF385C` solo para momentos de marca/iconos, CTA de texto en negro (patrón Primary Dark de Airbnb, 16.7:1) con hover `#D70466` (5.16:1 con blanco — mantiene AA en hover). Secundario `#6a6a6a` (5.6:1). Dark mode "Moonlight" `#141414`/`#1e1e1e` con sub `#b0b0b0` (9.7:1).

**Tipografía:** DM Sans (sustituto CDN de Airbnb Cereal VF) pesos 500-700 + **Lora** serif itálica para momentos editoriales (pull-quotes, kickers, em del h1) — eje de contraste serif/sans, no dos sans similares.

**Layout Airbnb signatures:** nav sticky con search pill central, barra de category chips scrollable, hero con foto a sangre + search card flotante (absolute ≥1120px, apilada ≤760px), tarjetas de listing con shadow de 3 capas y radios 20px, drawer de wishlist, footer de 4 columnas.

## Mejoras implementadas

1. **Search card flotante en desktop** — la composición inicial (flex-wrap) apilaba copy+card en 2 filas a 1280px, empujando el botón Search bajo el fold (hero 872px). Fix: `position:absolute` en ≥1120px con reserva de espacio para el copy → hero 448px, todo visible en 800px de alto. Determinístico y fiel al layering de Airbnb.
2. **CTA con contraste AA** — texto blanco sobre coral #FF385C da ~3.7:1 (falla 4.5:1); se usó el patrón Primary Dark (#222 bg) para CTAs con texto y coral solo para iconos; hover/pressed #D70466.
3. **Aria labels dinámicos i18n** — los aria-labels de wishlist/close/steppers/menu se generan por idioma (`a11ySave` + nombre de la propiedad, `a11yClose`, `a11yGMinus/Plus`, `a11yMenu`) en los 6 idiomas.
4. **Fix de comillas en DE** — 3 strings alemanes con comillas tipográficas mal balanceadas rompían el parseo del script (SyntaxError silencioso que mataba TODOS los listeners). Detectado con `node --check` + escáner de comillas por línea.
5. **Paridad i18n verificada** — 189 keys × 6 idiomas, 175 refs data-i18n del HTML, cero unresolved; verificación con script de brace/quote-counting (no regex plano).

## Slop diagnostic (puntuación 1/10 — bajo)

- 3. Feature-tile grid: NO — grid de 12 colores con feature tile a sangre + 2 wide + 7 standard (variedad estructural real).
- 8. Center stack: NO — copy izquierda + card derecha + chips horizontales.
- 9. Default type: NO — DM Sans + Lora elegidos (con sustituto documentado de Cereal VF).
- 10. Wrong surface: NO — Explore conduce la composición.
- Sin gradient text, sin glassmorphism (solo blur puntual en badges sobre foto), sin side-stripe, sin eyebrows en mayúsculas (kickers serif itálicos una vez por sección), sin markers numerados.

## Pendiente para futura iteración

- [ ] QA del dark mode en profundidad (verificado en build, falta captura dark).
- [ ] Los nombres de propiedades (p.ej. "The Glass Cabin") se mantienen en EN en todos los idiomas — intencional para consistencia de búsqueda, documentar si se quiere localizar.
- [ ] Considerar carrusel swipe en las fotos de las cards en mobile (hoy hover zoom + wishlist).

## Paleta de colores

| Token | Color | Uso |
|---|---|---|
| `--red` | `#FF385C` | Iconos, momentos de marca, botón circular de búsqueda |
| `--red-deep` | `#D70466` | Hover/pressed de CTAs coral (5.16:1 con blanco) |
| `--ink` | `#222222` | Texto principal (warm near-black; 16:1 sobre blanco) |
| `--sub` | `#6a6a6a` | Texto secundario (5.6:1 sobre blanco) |
| `--bg` | `#ffffff` | Lienzo |
| `--surface-2` | `#f2f2f2` | Controles circulares, hover chips |
| `--line` | `#ebebeb` / `#dddddd` | Bordes |
| Dark `--bg` | `#141414` | Moonlight |
| Dark `--sub` | `#b0b0b0` | Secundario dark (9.7:1) |

## Notas de accesibilidad

- Contraste body ≥4.5:1 verificado en las combinaciones principales de ambos temas (tokens arriba).
- Focus visible en todos los interactivos (outline 2px ink).
- `prefers-reduced-motion: reduce` en TODAS las animaciones (reveals, heroZoom, heartPop, transitions).
- Nav transparente: al ser bg sólido sticky no hay superposición de nav sobre hero → sin necesidad de override blanco.
- Skip link, landmarks semánticos, aria-pressed en chips/hearts, role=dialog en overlays.