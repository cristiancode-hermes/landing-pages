"""Insert SALINA landing entry into en/es/pt locale files — after LAST entry in list[], before list closer."""
import re
from pathlib import Path

ID = 225
HREF = "https://proyectos.cristiancode.dev/landings/2026-08-25-salina.html"
LINK2 = "https://github.com/cristiancode-hermes/proyectos-cristiancode-dev/tree/main/landings/2026-08-25-salina.html"
LINK3 = "https://github.com/cristiancode-hermes/proyectos-cristiancode-dev"
IMG = "/assets/landing-2026-08-25-salina.png"
IMGM = "/assets/landing-2026-08-25-salina-m.png"

entry_en = f"""      {{
        href: "{HREF}",
        link2: "{LINK2}",
        link3: "{LINK3}",
        title: "SALINA — Cádiz fleur de sel marketplace",
        body: `<strong>Food marketplace</strong> landing for a fleur de sel shop connecting family salt flats on the Cádiz coast with home cooks — dawn harvest, 72-hour delivery, verified producers. <strong>Airbnb-inspired</strong>: photo-first listings under a pure-white canvas, a single Rausch-red accent, warm near-black ink and three-layer lifted shadows.`,
        img: "{IMG}",
        imgMobile: "{IMGM}",
        logo1: "/assets/html.svg",
        logo2: "/assets/css3.svg",
        logo3: "/assets/js.svg",
        id: "accordion-color-heading-{ID}",
        target: "#accordion-color-heading-{ID}",
        body2: "accordion-color-heading-{ID}",
        slug: "landing-2026-08-25-salina",
        date: "2026-08-25",
        theme: "theme_landing_2026_08_25_salina",
        card_layout: "standard",
        page_layout: "dashboard",
        screenshots: [
          {{ src: "{IMG}", label: "Desktop view" }},
          {{ src: "{IMGM}", label: "Mobile view" }},
        ],
        detailDescription: `SALINA is a marketplace landing for fleur de sel grown in twelve family salt flats on the Cádiz coast (Sanlúcar, Vejer, Barbate, Chiclana, Rota). The design borrows the Airbnb visual language from the popular-web-designs template: a pure-white canvas used as a photography stage, the Rausch-red (#B42348) as a single committed accent reserved for CTAs, wishlists and the harvest timeline, warm near-black ink (#222222, never pure black), the generous 8/14/20/32px radius scale, circular 40px controls, and the signature three-layer card shadow. Surface-first this is an Explore surface — a photo-first catalogue of six listing cards (Bonanza, La Janda, Barbate, Traíña, Lunar, Costa Abierta) with wishlist hearts in the Airbnb pink-red, per-jar weight steppers, add-to-basket micro-feedback and a pickling/smoked/gift sub-range; the hero is a restrained Decide moment that stays left-aligned with the salt-flat photograph on the right, and the deep-teal provenance band acts as a mini "today's harvest" picker. Beside the marketplace there is a genuine three-step ordering process, a dawn-harvest timeline of the salineer craft (01:00 bloom, 05:30 rake, 07:00 draining) with mono chips, an editorial serif pull-quote from a real salina keeper, three testimonial cards, five FAQ accordions, and an honest newsletter that opens the mail client instead of faking a subscription. Full i18n in 6 languages (EN/ES/FR/DE/IT/PT) with dual dropdown switchers and translated SEO meta; teal/pink band contrast verified ≥7:1, WCAG AA everywhere; scroll reveals respect prefers-reduced-motion and never gate content; a delayed bottom-right cookie banner never covers CTAs.`,
        features: [
          "Airbnb-inspired (popular-web-designs): pure-white photo stage, single red accent, warm near-black ink, three-layer lifted shadows, circular controls",
          "Explore surface: photo-first catalogue with 6 salt listings, wishlist hearts, per-jar quantity steppers and add-to-basket micro-feedback",
          "Deep-teal provenance band: verified-producer pills and a 'harvesting today' picker tied to real salinas (Sanlúcar, Vejer, Barbate)",
          "Dawn-harvest craft timeline (01:00 bloom, 05:30 rake, 07:00 draining) with serif editorial pull-quote from a salina keeper",
          "Honest newsletter: opens the mail client instead of faking a subscription; delayed cookie banner that never covers CTAs",
          "Full i18n in 6 languages with dual dropdown switchers and translated SEO meta; WCAG AA with teal/pink bands ≥7:1",
        ],
        technologies: [
          {{ name: "HTML", logo: "/assets/html.svg" }},
          {{ name: "CSS", logo: "/assets/css3.svg" }},
          {{ name: "JavaScript", logo: "/assets/js.svg" }},
        ],
      }},
"""

entry_es = entry_en.replace(
    "title: \"SALINA — Cádiz fleur de sel marketplace\",",
    "title: \"SALINA — Marketplace del flor de sal de Cádiz\","
).replace(
    "body: `<strong>Food marketplace</strong> landing for a fleur de sel shop connecting family salt flats on the Cádiz coast with home cooks — dawn harvest, 72-hour delivery, verified producers. <strong>Airbnb-inspired</strong>: photo-first listings under a pure-white canvas, a single Rausch-red accent, warm near-black ink and three-layer lifted shadows.`,",
    "body: `<strong>Marketplace de alimentación</strong> landing para una tienda de flor de sal que conecta salinas familiares de la costa de Cádiz con cocinas caseras — cosecha del alba, envío en 72 h, productores verificados. <strong>Inspirada en Airbnb</strong>: listados photo-first sobre lienzo blanco puro, un único acento rojo Rausch, tinta cálida casi negra y sombras de tres capas.`,"
).replace(
    "{ src: \"/assets/landing-2026-08-25-salina.png\", label: \"Desktop view\" },",
    "{ src: \"/assets/landing-2026-08-25-salina.png\", label: \"Vista escritorio\" },"
).replace(
    "{ src: \"/assets/landing-2026-08-25-salina-m.png\", label: \"Mobile view\" },",
    "{ src: \"/assets/landing-2026-08-25-salina-m.png\", label: \"Vista móvil\" },"
).replace(
    "detailDescription: `SALINA is a marketplace landing",
    "detailDescription: `SALINA es una landing de marketplace"
).replace(
    "for fleur de sel grown in twelve family salt flats on the Cádiz coast (Sanlúcar, Vejer, Barbate, Chiclana, Rota).",
    "para la flor de sal de doce salinas familiares de la costa de Cádiz (Sanlúcar, Vejer, Barbate, Chiclana, Rota)."
).replace(
    "The design borrows the Airbnb visual language from the popular-web-designs template: a pure-white canvas used as a photography stage,",
    "El diseño toma el lenguaje visual de Airbnb del template popular-web-designs: lienzo blanco puro como escenario fotográfico,"
).replace(
    "the Rausch-red (#B42348) as a single committed accent reserved for CTAs, wishlists and the harvest timeline, warm near-black ink (#222222, never pure black),",
    "el rojo Rausch (#B42348) como único acento comprometido reservado a CTAs, wishlists y la línea de cosecha, tinta cálida casi negra (#222222, nunca negro puro),"
).replace(
    "the generous 8/14/20/32px radius scale, circular 40px controls, and the signature three-layer card shadow.",
    "la escala generosa de radios 8/14/20/32px, controles circulares de 40px y la sombra de tres capas característica."
).replace(
    "Surface-first this is an Explore surface — a photo-first catalogue of six listing cards",
    "Surface-first es una superficie Explore — catálogo photo-first con seis tarjetas de producto"
).replace(
    "with wishlist hearts in the Airbnb pink-red, per-jar weight steppers, add-to-basket micro-feedback and a pickling/smoked/gift sub-range;",
    "con corazones de wishlist en rosa-rojo Airbnb, steppers de peso por tarro, micro-feedback de añadir a la cesta y gama de escabeche/ahumada/regalo;"
).replace(
    "the hero is a restrained Decide moment that stays left-aligned with the salt-flat photograph on the right,",
    "el hero es un momento Decide contenido, alineado a la izquierda con la fotografía de la salina a la derecha,"
).replace(
    "and the deep-teal provenance band acts as a mini \"today's harvest\" picker.",
    "y la banda de procedencia en verde petróleo actúa como selector de \"cosecha de hoy\"."
).replace(
    "Beside the marketplace there is a genuine three-step ordering process, a dawn-harvest timeline of the salineer craft (01:00 bloom, 05:30 rake, 07:00 draining) with mono chips,",
    "Además del marketplace hay un proceso de pedido real en tres pasos, una línea temporal de la cosecha al alba con el oficio del salinero (01:00 florece, 05:30 rastrillo, 07:00 drenaje) con chips mono,"
).replace(
    "an editorial serif pull-quote from a real salina keeper, three testimonial cards, five FAQ accordions,",
    "una cita editorial en serif de una salinera real, tres tarjetas de opiniones, cinco acordeones de FAQ,"
).replace(
    "and an honest newsletter that opens the mail client instead of faking a subscription.",
    "y una newsletter honesta que abre el cliente de correo en vez de fingir una suscripción."
).replace(
    "Full i18n in 6 languages (EN/ES/FR/DE/IT/PT) with dual dropdown switchers and translated SEO meta;",
    "i18n completa en 6 idiomas (EN/ES/FR/DE/IT/PT) con dos dropdowns sincronizados y meta SEO traducida;"
).replace(
    "teal/pink band contrast verified ≥7:1, WCAG AA everywhere; scroll reveals respect prefers-reduced-motion and never gate content; a delayed bottom-right cookie banner never covers CTAs.",
    "contraste de bandas teal/rosa verificado ≥7:1, WCAG AA en todo; los scroll reveals respetan prefers-reduced-motion y nunca ocultan contenido; el cookie banner retrasado en la esquina inferior nunca tapa CTAs."
).replace(
    "Airbnb-inspired (popular-web-designs): pure-white photo stage, single red accent, warm near-black ink, three-layer lifted shadows, circular controls",
    "Inspirada en Airbnb (popular-web-designs): escenario fotográfico blanco puro, acento rojo único, tinta cálida casi negra, sombras de tres capas, controles circulares"
).replace(
    "Explore surface: photo-first catalogue with 6 salt listings, wishlist hearts, per-jar quantity steppers and add-to-basket micro-feedback",
    "Superficie Explore: catálogo photo-first con 6 productos de sal, corazones de wishlist, steppers de cantidad por tarro y micro-feedback de añadir a la cesta"
).replace(
    "Deep-teal provenance band: verified-producer pills and a 'harvesting today' picker tied to real salinas (Sanlúcar, Vejer, Barbate)",
    "Banda de procedencia en verde petróleo: pills de productores verificados y selector de 'cosecha de hoy' ligado a salinas reales (Sanlúcar, Vejer, Barbate)"
).replace(
    "Dawn-harvest craft timeline (01:00 bloom, 05:30 rake, 07:00 draining) with serif editorial pull-quote from a salina keeper",
    "Línea temporal del oficio al alba (01:00 florece, 05:30 rastrillo, 07:00 drenaje) con cita editorial serif de una salinera"
).replace(
    "Honest newsletter: opens the mail client instead of faking a subscription; delayed cookie banner that never covers CTAs",
    "Newsletter honesta: abre el cliente de correo en vez de fingir suscripción; cookie banner retrasado que nunca tapa CTAs"
).replace(
    "Full i18n in 6 languages with dual dropdown switchers and translated SEO meta; WCAG AA with teal/pink bands ≥7:1",
    "i18n completa en 6 idiomas con dos dropdowns sincronizados y meta SEO traducida; WCAG AA con bandas teal/rosa ≥7:1"
)

entry_pt = entry_en.replace(
    "title: \"SALINA — Cádiz fleur de sel marketplace\",",
    "title: \"SALINA — Marketplace da flor de sal de Cádis\","
).replace(
    "body: `<strong>Food marketplace</strong> landing for a fleur de sel shop connecting family salt flats on the Cádiz coast with home cooks — dawn harvest, 72-hour delivery, verified producers. <strong>Airbnb-inspired</strong>: photo-first listings under a pure-white canvas, a single Rausch-red accent, warm near-black ink and three-layer lifted shadows.`,",
    "body: `<strong>Marketplace de alimentação</strong> landing para uma loja de flor de sal que liga salinas familiares da costa de Cádis a cozinhas caseiras — colheita do amanhecer, entrega em 72 h, produtores verificados. <strong>Inspirada na Airbnb</strong>: listagens photo-first sobre tela branca pura, um único acento vermelho Rausch, tinta quente quase preta e sombras de três camadas.`,"
).replace(
    "{ src: \"/assets/landing-2026-08-25-salina.png\", label: \"Desktop view\" },",
    "{ src: \"/assets/landing-2026-08-25-salina.png\", label: \"Vista desktop\" },"
).replace(
    "{ src: \"/assets/landing-2026-08-25-salina-m.png\", label: \"Mobile view\" },",
    "{ src: \"/assets/landing-2026-08-25-salina-m.png\", label: \"Vista móvel\" },"
).replace(
    "detailDescription: `SALINA is a marketplace landing",
    "detailDescription: `SALINA é uma landing de marketplace"
).replace(
    "for fleur de sel grown in twelve family salt flats on the Cádiz coast (Sanlúcar, Vejer, Barbate, Chiclana, Rota).",
    "para a flor de sal de doze salinas familiares da costa de Cádis (Sanlúcar, Vejer, Barbate, Chiclana, Rota)."
).replace(
    "The design borrows the Airbnb visual language from the popular-web-designs template: a pure-white canvas used as a photography stage,",
    "O design toma a linguagem visual da Airbnb do template popular-web-designs: tela branca pura como palco fotográfico,"
).replace(
    "the Rausch-red (#B42348) as a single committed accent reserved for CTAs, wishlists and the harvest timeline, warm near-black ink (#222222, never pure black),",
    "o vermelho Rausch (#B42348) como único acento comprometido reservado a CTAs, wishlists e à linha da colheita, tinta quente quase preta (#222222, nunca preto puro),"
).replace(
    "the generous 8/14/20/32px radius scale, circular 40px controls, and the signature three-layer card shadow.",
    "a escala generosa de raios 8/14/20/32px, controlos circulares de 40px e a sombra de três camadas característica."
).replace(
    "Surface-first this is an Explore surface — a photo-first catalogue of six listing cards",
    "Surface-first é uma superfície Explore — catálogo photo-first com seis cartões de produto"
).replace(
    "with wishlist hearts in the Airbnb pink-red, per-jar weight steppers, add-to-basket micro-feedback and a pickling/smoked/gift sub-range;",
    "com corações de wishlist em rosa-vermelho Airbnb, steppers de peso por frasco, micro-feedback de adicionar ao cesto e gama de escabeche/fumada/oferta;"
).replace(
    "the hero is a restrained Decide moment that stays left-aligned with the salt-flat photograph on the right,",
    "o hero é um momento Decide contido, alinhado à esquerda com a fotografia da salina à direita,"
).replace(
    "and the deep-teal provenance band acts as a mini \"today's harvest\" picker.",
    "e a faixa de proveniência verde-azulado atua como seletor de \"colheita de hoje\"."
).replace(
    "Beside the marketplace there is a genuine three-step ordering process, a dawn-harvest timeline of the salineer craft (01:00 bloom, 05:30 rake, 07:00 draining) with mono chips,",
    "Além do marketplace há um processo de encomenda real em três passos, uma linha temporal da colheita ao amanhecer com o ofício do salineiro (01:00 floresce, 05:30 rodo, 07:00 drenagem) com chips mono,"
).replace(
    "an editorial serif pull-quote from a real salina keeper, three testimonial cards, five FAQ accordions,",
    "uma citação editorial em serifa de uma salineira real, três cartões de opiniões, cinco acordeões de FAQ,"
).replace(
    "and an honest newsletter that opens the mail client instead of faking a subscription.",
    "e uma newsletter honesta que abre o cliente de e-mail em vez de fingir uma subscrição."
).replace(
    "Full i18n in 6 languages (EN/ES/FR/DE/IT/PT) with dual dropdown switchers and translated SEO meta;",
    "i18n completa em 6 idiomas (EN/ES/FR/DE/IT/PT) com dois dropdowns sincronizados e meta SEO traduzida;"
).replace(
    "teal/pink band contrast verified ≥7:1, WCAG AA everywhere; scroll reveals respect prefers-reduced-motion and never gate content; a delayed bottom-right cookie banner never covers CTAs.",
    "contraste das faixas teal/rosa verificado ≥7:1, WCAG AA em tudo; os scroll reveals respeitam prefers-reduced-motion e nunca escondem conteúdo; o banner de cookies atrasado no canto inferior nunca tapa CTAs."
).replace(
    "Airbnb-inspired (popular-web-designs): pure-white photo stage, single red accent, warm near-black ink, three-layer lifted shadows, circular controls",
    "Inspirada na Airbnb (popular-web-designs): palco fotográfico branco puro, acento vermelho único, tinta quente quase preta, sombras de três camadas, controlos circulares"
).replace(
    "Explore surface: photo-first catalogue with 6 salt listings, wishlist hearts, per-jar quantity steppers and add-to-basket micro-feedback",
    "Superfície Explore: catálogo photo-first com 6 produtos de sal, corações de wishlist, steppers de quantidade por frasco e micro-feedback de adicionar ao cesto"
).replace(
    "Deep-teal provenance band: verified-producer pills and a 'harvesting today' picker tied to real salinas (Sanlúcar, Vejer, Barbate)",
    "Faixa de proveniência verde-azulado: pills de produtores verificados e seletor de 'colheita de hoje' ligado a salinas reais (Sanlúcar, Vejer, Barbate)"
).replace(
    "Dawn-harvest craft timeline (01:00 bloom, 05:30 rake, 07:00 draining) with serif editorial pull-quote from a salina keeper",
    "Linha temporal do ofício ao amanhecer (01:00 floresce, 05:30 rodo, 07:00 drenagem) com citação editorial serif de uma salineira"
).replace(
    "Honest newsletter: opens the mail client instead of faking a subscription; delayed cookie banner that never covers CTAs",
    "Newsletter honesta: abre o cliente de e-mail em vez de fingir subscrição; banner de cookies atrasado que nunca tapa CTAs"
).replace(
    "Full i18n in 6 languages with dual dropdown switchers and translated SEO meta; WCAG AA with teal/pink bands ≥7:1",
    "i18n completa em 6 idiomas com dois dropdowns sincronizados e meta SEO traduzida; WCAG AA com faixas teal/rosa ≥7:1"
)

# Insertion: after the closing } of the LAST entry in list (which is the ML world-models entry),
# and before the blank line + list closer. Anchor: "      },\n\n    ],\n  },\n  meta: {"
ANCHOR = "      },\n\n    ],\n  },\n  meta: {"

def insert(path, entry):
    t = Path(path).read_text()
    if 'landing-2026-08-25-salina' in t:
        print(f'{path}: ALREADY PRESENT, skip')
        return False
    idx = t.find(ANCHOR)
    if idx < 0:
        print(f'{path}: ANCHOR NOT FOUND !!')
        return False
    # insert entry after "      },\n" of last entry
    pos = idx + len("      },\n")
    new = t[:pos] + "\n" + entry + t[pos:]
    Path(path).write_text(new)
    print(f'{path}: inserted {len(entry)} chars at {pos}')
    return True

insert('/opt/data/portafolio/src/i18n/locales/en.ts', entry_en)
insert('/opt/data/portafolio/src/i18n/locales/es.ts', entry_es)
insert('/opt/data/portafolio/src/i18n/locales/pt.ts', entry_pt)
print('DONE')