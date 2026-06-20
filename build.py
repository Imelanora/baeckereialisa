"""
Bäckerei Alisa – Website Generator
Generates all HTML pages into the same folder.
Run: python3 build.py
"""

import os

OUT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------
def head(title, extra_css="", base=""):
    return f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title} – Bäckerei Alisa</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;1,400;1,500&family=Jost:wght@300;400;500&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="{base}style.css" />
    {"<style>" + extra_css + "</style>" if extra_css else ""}
</head>
<body>
<script src="{base}nav.js"></script>
"""

def foot(year=2025, base=""):
    return f"""
<footer>
    <em>Bäckerei Alisa</em>
    Die etwas andere Bäckerei &nbsp;·&nbsp; © {year} &nbsp;·&nbsp; Alle Rechte vorbehalten
    <br><br><span style="opacity:0.5;">
        <a href="{base}rechtliches/impressum.html" style="color:inherit;text-decoration:none;">Impressum</a>
        &nbsp;·&nbsp;
        <a href="{base}rechtliches/datenschutz.html" style="color:inherit;text-decoration:none;">Datenschutz</a>
    </span>
</footer>
</body>
</html>"""

def page_hero_strip(label, title):
    return f"""
<div class="page-hero-strip" style="margin-top:72px;">
    <div class="page-hero-strip-text">
        <p class="section-label">{label}</p>
        <h1 class="section-title">{title}</h1>
    </div>
</div>"""

def slideshow_html(slides, slide_class, dots_id, height, interval_ms):
    """
    Renders a CSS/JS slideshow without arrow buttons.
    slides = list of (filename, caption_or_alt)
    """
    imgs = "\n".join(
        f'        <img src="{src}" alt="{cap}" class="{slide_class}" />'
        for src, cap in slides
    )
    captions_js = str([cap for _, cap in slides])
    has_caption = any(cap for _, cap in slides)
    caption_html = f'\n    <div class="ss-caption" id="{dots_id}-cap">{slides[0][1]}</div>' if has_caption else ""
    caption_css = f"""
.ss-caption {{ position:absolute; bottom:0; left:0; right:0; padding:1.2rem 2rem 3.5rem;
    background:linear-gradient(transparent,rgba(44,26,10,.7)); color:#fff;
    font-family:'Playfair Display',serif; font-style:italic; font-size:1.05rem; pointer-events:none; }}""" if has_caption else ""
    caption_js = f"document.getElementById('{dots_id}-cap').textContent = captions[cur];" if has_caption else ""

    return f"""<style>
.{slide_class}-wrap {{ position:relative; overflow:hidden; }}
.{slide_class}-track {{ display:flex; transition:transform .6s cubic-bezier(.4,0,.2,1); }}
.{slide_class} {{ min-width:100%; height:{height}; object-fit:cover; display:block; }}
.{dots_id}-dots {{ position:absolute; bottom:1.2rem; left:50%; transform:translateX(-50%); display:flex; gap:.6rem; z-index:10; }}
.{dots_id}-dot {{ width:11px; height:11px; border-radius:50%; background:rgba(255,255,255,.45);
    cursor:pointer; transition:background .2s,transform .2s; border:2px solid rgba(255,255,255,.6); padding:0; }}
.{dots_id}-dot.active {{ background:#fff; transform:scale(1.25); }}{caption_css}
</style>
<div class="{slide_class}-wrap">
    <div class="{slide_class}-track">
{imgs}
    </div>{caption_html}
    <div class="{dots_id}-dots" id="{dots_id}"></div>
</div>
<script>
(function(){{
    const captions = {captions_js};
    const slides   = document.querySelectorAll('.{slide_class}');
    const dotsWrap = document.getElementById('{dots_id}');
    let cur = 0;
    slides.forEach((_,i) => {{
        const d = document.createElement('button');
        d.className = '{dots_id}-dot' + (i===0?' active':'');
        d.setAttribute('aria-label','Bild '+(i+1));
        d.onclick = () => go(i);
        dotsWrap.appendChild(d);
    }});
    function go(n){{
        dotsWrap.children[cur].classList.remove('active');
        cur = (n + slides.length) % slides.length;
        document.querySelector('.{slide_class}-track').style.transform = `translateX(-${{cur*100}}%)`;
        dotsWrap.children[cur].classList.add('active');
        {caption_js}
    }}
    setInterval(() => go(cur+1), {interval_ms});
}})();
</script>"""


# ===========================================================================
# index.html  –  Homepage
# ===========================================================================
def build_index():
    # -----------------------------------------------------------------------
    # LADEN-DIASHOW  ·  Bilder hier anpassen:
    # Format:  ("dateiname.png", "")   ← leerer String = keine Beschriftung
    # Bilder müssen im gleichen Ordner wie die HTML-Dateien liegen.
    # Zeile hinzufügen = Bild dazu | Zeile löschen = Bild weg
    # Danach: python3 build.py  ausführen
    # -----------------------------------------------------------------------
    SHOP_SLIDES = [
        "bilder/bakery.png",
        "bilder/shop1.png",
        "bilder/cake3.png",
        "bilder/cake4.png",
    ]

    css = """
    .hero { position:relative; height:100vh; overflow:hidden; display:flex; align-items:center; justify-content:center; }
    .hero video { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; z-index:0; }
    .hero-overlay { position:absolute; inset:0; background:linear-gradient(to bottom,rgba(20,10,4,.35),rgba(20,10,4,.55)); z-index:1; }
    .hero-content { position:relative; z-index:10; text-align:center; color:#fff; padding:2rem; }
    .hero-badge { display:inline-block; font-size:.65rem; letter-spacing:.4em; text-transform:uppercase; color:var(--brown-mid); border:1px solid rgba(196,168,130,.5); padding:.4rem 1.4rem; margin-bottom:2rem; }
    .hero-title { font-family:'Playfair Display',serif; font-size:clamp(3.5rem,8vw,6.5rem); font-weight:400; line-height:1.0; letter-spacing:.02em; margin-bottom:.3rem; }
    .hero-title em { font-style:italic; color:var(--brown-mid); }
    .hero-sub { font-family:'Playfair Display',serif; font-size:1.15rem; font-style:italic; color:rgba(255,255,255,.7); letter-spacing:.12em; margin-bottom:2.5rem; }
    .hero-divider { width:40px; height:1px; background:var(--brown-mid); margin:0 auto 2.5rem; }
    .hero-cta { display:flex; gap:1.2rem; justify-content:center; flex-wrap:wrap; }
    .home-story { display:grid; grid-template-columns:1fr 1fr; gap:0; min-height:60vh; }
    .story-img { overflow:hidden; min-height:400px; }
    .story-img img { width:100%; height:100%; object-fit:cover; display:block; }
    .story-text-wrap { background:var(--bg2); padding:5rem 4rem; display:flex; flex-direction:column; justify-content:center; }
    .story-p { font-size:.9rem; line-height:2; color:var(--text); opacity:.8; margin-bottom:1rem; }
    .shop-ss-section { background:var(--bg); padding-bottom:4rem; }
    .shop-ss-section .ss-inner { max-width:1100px; margin:0 auto; }
    .quote-strip { background:var(--brown-dark); color:var(--brown-light); text-align:center; padding:4rem 2rem; }
    .quote-strip blockquote { font-family:'Playfair Display',serif; font-size:clamp(1.3rem,3vw,2rem); font-style:italic; font-weight:400; max-width:700px; margin:0 auto; line-height:1.5; opacity:.92; }
    .quote-strip cite { display:block; margin-top:1.2rem; font-size:.68rem; letter-spacing:.3em; text-transform:uppercase; color:var(--brown-mid); font-style:normal; }
    @media(max-width:720px) {
        .home-story { grid-template-columns:1fr; }
        .story-img { height:300px; min-height:unset; }
        .story-text-wrap { padding:3rem 1.5rem; }
    }
    """

    shop_ss = slideshow_html(
        [(s, "") for s in SHOP_SLIDES], "shop-slide", "shop-dots", "520px", 4500
    )

    html = head("Start", css) + f"""
<div class="hero">
    <video autoplay muted loop playsinline>
        <source src="hero.mp4" type="video/mp4">
    </video>
    <div class="hero-overlay"></div>
    <div class="hero-content">
        <div class="hero-badge">Handgemacht · Essen · Seit 2020</div>
        <h1 class="hero-title">Bäckerei<br><em>Alisa</em></h1>
        <p class="hero-sub">Die etwas andere Bäckerei</p>
        <div class="hero-divider"></div>
        <div class="hero-cta">
            <a class="btn btn-fill" href="showroom.html">Showroom entdecken</a>
            <a class="btn" href="bestellen.html">Torte bestellen</a>
        </div>
    </div>
    <div class="hero-scroll">
        <div class="scroll-line"></div>Scroll
    </div>
</div>

<div class="home-story">
    <div class="story-img">
        <img src="bilder/bakery.png" alt="Bäckerei Alisa – Tortenauswahl im Kühlregal" />
    </div>
    <div class="story-text-wrap">
        <p class="section-label">Unsere Geschichte</p>
        <h2 class="section-title">Backen mit<br><em>Herz & Seele</em></h2>
        <div class="divider-line"></div>
        <p class="story-p">Was einst als kleine Leidenschaft in der eigenen Küche begann, ist heute ein
            familiärer Handwerksbetrieb, der für seine außergewöhnlichen Torten bekannt ist. Als
            Familienbetrieb legen wir besonderen Wert auf persönliche Beratung, Herzlichkeit und Qualität,
            die man schmeckt – und für Designs, die man nicht vergisst.</p>
        <p class="story-p">Jede Torte wird mit größter Sorgfalt und ausschließlich aus hochwertigen Zutaten
            gefertigt. Kein Stück gleicht dem anderen – denn jede Bestellung ist so einzigartig wie der
            Anlass selbst.</p>
        <div style="margin-top:1.5rem;">
            <a class="btn btn-outline-dark" href="showroom.html">Unsere Kreationen ansehen</a>
        </div>
    </div>
</div>

<div class="shop-ss-section">
    <div style="text-align:center;padding:3.5rem 4rem 2rem;">
        <p class="section-label">Täglich frisch bei uns</p>
        <h2 class="section-title" style="text-align:center;">Immer in unserem <em>Laden</em></h2>
    </div>
    <div class="ss-inner">
        {shop_ss}
    </div>
</div>

<div class="quote-strip">
    <blockquote>„Jede Torte erzählt eine Geschichte – lassen Sie uns Ihre erzählen."</blockquote>
    <cite>Bäckerei Alisa · Die etwas andere Bäckerei</cite>
</div>
""" + foot()

    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("✓  index.html")


# ===========================================================================
# showroom.html
# ===========================================================================
def build_showroom():
    # -----------------------------------------------------------------------
    # SHOWROOM-DIASHOW  ·  Bilder hier anpassen:
    # Format:  ("dateiname.png", "Beschriftung die unten im Bild erscheint")
    # Bilder müssen im gleichen Ordner wie die HTML-Dateien liegen.
    # Zeile hinzufügen = Bild dazu | Zeile löschen = Bild weg
    # Danach: python3 build.py  ausführen
    # -----------------------------------------------------------------------
    SHOWROOM_SLIDES = [
        "bilder/torte1.PNG",
        "bilder/torte2.PNG",
        "bilder/torte3.PNG",
        "bilder/torte4.PNG",
        "bilder/torte5.PNG",
        "bilder/torte6.PNG",
        "bilder/torte7.PNG",
    ]

    flavors = [
        "Vanille & Sahne", "Schokolade", "Erdbeere", "Orange",
        "Zitrone & Limette", "Raffaello", "Karamell", "Kokos",
        "Kirsch", "Lotus Biscoff", "Cheesecake", "Nuss-Nougat", "Auf Anfrage",
    ]

    css = """
    .flavors-wrap { background:var(--brown-deep); padding:4rem; }
    .flavors-inner { max-width:1100px; margin:0 auto; }
    .flavors-wrap .section-label { color:var(--brown-mid); }
    .flavors-wrap .section-title { color:var(--brown-light); }
    .flavor-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(155px,1fr)); gap:1px; margin-top:1.5rem; background:rgba(196,168,130,.2); }
    .flavor-pill { background:transparent; padding:.8rem 1rem; font-size:.76rem; color:var(--brown-light); text-align:center; letter-spacing:.08em; opacity:.85; transition:opacity .2s,background .2s; }
    .flavor-pill:hover { opacity:1; background:rgba(196,168,130,.15); }
    .sr-slide-wrap { position:relative; overflow:hidden; background:var(--brown-deep); }
    .sr-slide-track { display:flex; transition:transform .6s cubic-bezier(.4,0,.2,1); }
    .sr-slide { min-width:100%; height:780px; object-fit:contain; display:block; background:var(--brown-deep); }
    .sr-dots-dots { position:absolute; bottom:1.2rem; left:50%; transform:translateX(-50%); display:flex; gap:.6rem; z-index:10; }
    .sr-dots-dot { width:11px; height:11px; border-radius:50%; background:rgba(255,255,255,.45); cursor:pointer; transition:background .2s,transform .2s; border:2px solid rgba(255,255,255,.6); padding:0; }
    .sr-dots-dot.active { background:#fff; transform:scale(1.25); }
    @media(max-width:720px) { .flavors-wrap { padding-left:1.5rem; padding-right:1.5rem; } .sr-slide { height:420px; } }
    """

    flavor_pills = "\n".join(f'                    <div class="flavor-pill">{f}</div>' for f in flavors)

    slide_imgs = "\n".join(
        f'        <img src="{s}" alt="" class="sr-slide" />'
        for s in SHOWROOM_SLIDES
    )

    html = head("Showroom", css)
    html += page_hero_strip("Unsere Kreationen", "Der <em>Showroom</em>")
    html += f"""
<div style="max-width:1100px;margin:0 auto;padding:2.5rem 4rem 1rem;">
    <p style="font-size:.87rem;line-height:2;opacity:.75;max-width:560px;">
        Von der klassischen Hochzeitstorte bis zur modernen Designer-Kreation –
        lassen Sie sich von unseren echten Kreationen inspirieren.
    </p>
</div>
<div style="max-width:1100px;margin:0 auto;padding:0 4rem;">
    <div class="sr-slide-wrap">
        <div class="sr-slide-track">
{slide_imgs}
        </div>
        <div class="sr-dots-dots" id="sr-dots"></div>
    </div>
</div>
<script>
(function(){{
    const slides = document.querySelectorAll('.sr-slide');
    const dotsWrap = document.getElementById('sr-dots');
    let cur = 0;
    slides.forEach((_,i) => {{
        const d = document.createElement('button');
        d.className = 'sr-dots-dot' + (i===0?' active':'');
        d.setAttribute('aria-label','Bild '+(i+1));
        d.onclick = () => go(i);
        dotsWrap.appendChild(d);
    }});
    function go(n){{
        dotsWrap.children[cur].classList.remove('active');
        cur = (n + slides.length) % slides.length;
        document.querySelector('.sr-slide-track').style.transform = `translateX(-${{cur*100}}%)`;
        dotsWrap.children[cur].classList.add('active');
    }}
    setInterval(() => go(cur+1), 5000);
}})();
</script>
<div class="flavors-wrap" style="margin-top:3rem;">
    <div class="flavors-inner">
        <p class="section-label">Verfügbare Geschmacksrichtungen</p>
        <h2 class="section-title">Unsere <em>Füllungen</em></h2>
        <div class="flavor-grid">
{flavor_pills}
        </div>
    </div>
</div>
"""
    html += foot()
    with open(os.path.join(OUT, "showroom.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("✓  showroom.html")


# ===========================================================================
# events.html
# ===========================================================================
def build_events():
    # -----------------------------------------------------------------------
    # EVENT-FOTOS  ·  Bilder hier anpassen:
    # Bilder müssen im Ordner bilder/ liegen.
    # Zeile hinzufügen = Bild dazu | Zeile löschen = Bild weg
    # Danach: python3 build.py  ausführen
    # -----------------------------------------------------------------------
    EVENT_PHOTOS = [
        "bilder/events1.PNG",
        "bilder/events2.jpg",
        "bilder/events3.jpg",
    ]

    css = """
    .events-header { max-width:1100px; margin:0 auto; padding:3rem 4rem 2rem; }
    .events-header p.body { font-size:.9rem; line-height:2; color:var(--text); opacity:.8; margin-bottom:.8rem; max-width:720px; }
    .events-anlass-list { display:flex; flex-wrap:wrap; gap:.5rem; margin-top:1.2rem; }
    .events-anlass { font-size:.7rem; letter-spacing:.15em; text-transform:uppercase;
        border:1px solid var(--brown-mid); color:var(--brown); padding:.35rem .9rem; }
    .events-photo-grid { max-width:1100px; margin:2rem auto 0; padding:0 4rem;
        display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:1rem; }
    .events-photo-grid img { width:100%; height:auto; display:block; }
    .events-cta { margin:3rem 4rem 0; padding:2.5rem 3rem; background:var(--brown-dark); color:var(--brown-light);
        display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:1rem; }
    .events-cta p { font-family:'Playfair Display',serif; font-size:1.3rem; font-style:italic; color:#fff; opacity:1; }
    @media(max-width:720px) {
        .events-header { padding:2rem 1.5rem; }
        .events-photo-grid { padding:0 1.5rem; grid-template-columns:1fr; }
        .events-cta { margin-left:1.5rem; margin-right:1.5rem; flex-direction:column; }
    }
    """

    photos = "\n".join(
        f'    <img src="{s}" alt="" />'
        for s in EVENT_PHOTOS
    )

    anlaesse = ["Hochzeiten", "Geburtstage", "Beerdigungen", "Firmenfeiern", "Taufen", "Jubiläen", "Und mehr …"]
    anlass_tags = "\n".join(f'        <span class="events-anlass">{a}</span>' for a in anlaesse)

    html = head("Events", css)
    html += page_hero_strip("Für jeden Anlass", "Wir kochen & backen für Ihr <em>Event</em>")
    html += f"""
<div class="events-header">
    <p class="section-label">Unser Angebot</p>
    <h2 class="section-title">Von der <em>Torte</em> bis zum warmen Gericht</h2>
    <p class="body">Egal ob Freude oder Trauer, klein oder groß – wir bereiten das Essen für Ihr nächstes Event
        liebevoll und frisch zu. Von kunstvoll dekorierten Torten über süßes Gebäck bis hin zu
        warmen Speisen: bei uns bekommen Sie alles aus einer Hand.</p>
    <p class="body">Wir begleiten Hochzeiten, Geburtstagsfeiern, Firmenfeiern, Beerdigungen, Taufen und viele
        weitere Anlässe – immer mit dem gleichen Anspruch an Qualität und Herzlichkeit.</p>
    <div class="events-anlass-list">
{anlass_tags}
    </div>
</div>

<div class="events-photo-grid">
{photos}
</div>

<div class="events-cta">
    <p>Bereit, Ihren Event unvergesslich zu machen?</p>
    <a class="btn" href="kontakt.html">Jetzt anfragen</a>
</div>
<div style="height:4rem;"></div>
"""
    html += foot()
    with open(os.path.join(OUT, "events.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("✓  events.html")


# ===========================================================================
# speisekarte.html
# ===========================================================================
def build_speisekarte():
    css = """
    .menu-wrap { max-width:1100px; margin:0 auto; padding:3rem 4rem 0; }
    .menu-section { margin-bottom:3rem; }
    .menu-section-title { font-size:.63rem; letter-spacing:.3em; text-transform:uppercase;
        color:var(--muted); background:var(--bg2); padding:.55rem 1rem; margin-bottom:1.2rem; display:inline-block; }
    .menu-cols { display:grid; grid-template-columns:1fr 1fr; gap:0 3rem; }
    .menu-item { padding:.75rem 0; border-bottom:1px solid #e8d9c5; }
    .menu-item-top { display:flex; justify-content:space-between; align-items:baseline; gap:1rem; }
    .menu-item-name { font-family:'Playfair Display',serif; font-size:.95rem; font-style:italic; color:var(--brown-dark); font-weight:500; }
    .menu-item-price { font-size:.82rem; color:var(--brown); white-space:nowrap; flex-shrink:0; }
    .menu-item-desc { font-size:.75rem; color:var(--muted); line-height:1.6; margin-top:.2rem; }
    .allergen-section { background:var(--brown-deep); padding:4rem; margin-top:3rem; }
    .allergen-inner { max-width:1100px; margin:0 auto; }
    .allergen-section .section-label { color:var(--brown-mid); }
    .allergen-section .section-title { color:var(--brown-light); }
    .allergen-cols { display:grid; grid-template-columns:repeat(3,1fr); gap:.5rem 2rem; margin-top:1.5rem; }
    .allergen-row { display:flex; gap:.7rem; padding:.5rem 0; border-bottom:1px solid rgba(196,168,130,.12); align-items:flex-start; }
    .allergen-code { width:22px; height:22px; border:1px solid rgba(196,168,130,.4); display:flex; align-items:center;
        justify-content:center; font-size:.68rem; font-weight:600; color:var(--brown-mid); flex-shrink:0; margin-top:1px; }
    .allergen-text { font-size:.76rem; color:var(--brown-light); line-height:1.5; }
    .allergen-note { max-width:1100px; margin:2rem auto 0; padding:0 4rem 3rem; font-size:.75rem; color:var(--brown-mid); line-height:1.8; }
    @media(max-width:720px) {
        .menu-wrap, .allergen-note { padding-left:1.5rem; padding-right:1.5rem; }
        .menu-cols { grid-template-columns:1fr; }
        .allergen-section { padding-left:1.5rem; padding-right:1.5rem; }
        .allergen-cols { grid-template-columns:1fr 1fr; }
    }
    """

    def section(title, items, cols=2):
        left = items[:len(items)//2 + len(items)%2] if cols == 2 else items
        right = items[len(items)//2 + len(items)%2:] if cols == 2 else []
        def render_items(lst):
            out = ""
            for item in lst:
                name = item[0]
                price = item[1]
                desc = item[2] if len(item) > 2 else ""
                out += f"""
            <div class="menu-item">
                <div class="menu-item-top">
                    <span class="menu-item-name">{name}</span>
                    <span class="menu-item-price">{price}</span>
                </div>
                {"" if not desc else f'<div class="menu-item-desc">{desc}</div>'}
            </div>"""
            return out
        if cols == 2:
            return f"""
    <div class="menu-section">
        <div class="menu-section-title">{title}</div>
        <div class="menu-cols">
            <div>{render_items(left)}</div>
            <div>{render_items(right)}</div>
        </div>
    </div>"""
        else:
            return f"""
    <div class="menu-section">
        <div class="menu-section-title">{title}</div>
        <div>{render_items(left)}</div>
    </div>"""

    fruehstueck = [
        ("Good Morning",           "5,90 €", "1 Kaffee, 2 halbe Brötchen belegt nach Wahl: Wurst, Käse, Ei, Thunfisch, Camembert, Nutella, Marmelade"),
        ("Frühstück in Paris",     "4,50 €", "1 Croissant mit Butter und Marmelade, 1 Kaffee"),
        ("Frühstück in New York",  "8,90 €", "Club Sandwich: 3 Lagen Toast mit Ei, Geflügelbacon, Salat, Tomate, Gurke"),
        ("Frühstück in California","8,90 €", "Club Sandwich: 3 Lagen Toast mit gegrilltem Lachs, Salat, Gurke, Tomate"),
        ("Frühstück in Berlin",    "5,90 €", "Bratwurst, 2 Spiegeleier, Brötchen"),
        ("Strammer Max",           "7,90 €", "Toast, Schinken, Spiegelei"),
        ("American",               "8,90 €", "Bratkartoffeln mit Spiegelei, Geflügelbacon und Toast"),
        ("Alisa's Frühstück",      "5,90 €", "3 verschiedene Sorten Wurst, Käse, Marmelade, 2 Brötchen, 1 große Tasse Kaffee oder Tee"),
    ]

    balkan = [
        ("Burek",                  "4,00 €", "Wahl aus: Fleisch, Kartoffel, Spinat, Käse"),
        ("Mantije mit Joghurt",    "5,90 €", "mit Fleisch, 10 Stück und Joghurt-Knoblauch Soße"),
        ("Paprika in Schmand",     "6,50 €", "Paprika mit Schmand in Sahnesoße, dazu Balkan Brot"),
        ("Menemen",                "6,50 €", "Gebratene Paprika mit Tomaten und Zwiebeln mit Rührei, dazu Balkan Brot"),
        ("Uštipci mit Schmand",    "6,90 €", "Teigbällchen mit Schmand"),
        ("Balkan Frühstück",       "8,50 €", "Paprika mit Schmand in Sahnesoße, Sucuk, Ei, Weißkäse, dazu Balkan Brot"),
        ("Bosnisches Frühstück",   "8,90 €", "Uštipci, bosnische Wurst, Weißkäse, Kajmak"),
    ]

    ruehrei = [
        ("Rührei Classic",         "4,90 €", "mit Butter und Brötchen"),
        ("Rührei mit Sucuk",       "6,90 €", "mit Balkan Brot"),
    ]

    burger = [
        ("Hamburger",              "5,50 €", "mit Salat, Zwiebeln, Tomate, Gurke, Soße"),
        ("Chicken Burger",         "5,50 €", "mit Salat, Zwiebeln, Tomate, Gurke, Soße"),
        ("Hähnchenbrust Burger",   "5,50 €", "mit Röstzwiebeln"),
    ]

    cevapcici = [
        ("Ćevapčići 5 Stück",     "5,50 €", "mit Zwiebel, Ajvar und Kajmak, wahlweise in Lepina oder mit Pommes"),
        ("Ćevapčići 7 Stück",     "6,50 €", "mit Zwiebel, Ajvar und Kajmak, wahlweise in Lepina oder mit Pommes"),
        ("Ćevapčići 10 Stück",    "10,50 €","mit Zwiebel, Ajvar und Kajmak, wahlweise in Lepina oder mit Pommes"),
    ]

    nudel = [
        ("Rigatoni mit Champignons",    "9,90 €",  "mit Brokkoli in Sahnesoße"),
        ("Rigatoni mit buntem Gemüse",  "9,90 €",  "in Sahnesoße"),
        ("Rigatoni mit Hähnchenbrust",  "12,90 €", "mit Brokkoli in Sahnesoße"),
        ("Rigatoni mit Lachs",          "15,90 €", "mit Spinat in Sahnesoße"),
    ]

    beilage = [
        ("Pommes",                      "3,00 €", ""),
        ("Pellkartoffeln mit Sourcream","4,50 €", ""),
        ("Sahnekartoffeln",             "4,50 €", ""),
        ("Pfannengemüse",               "3,50 €", ""),
        ("Sahne Gurken Salat",          "2,00 €", ""),
        ("Sahne Kraut Salat",           "2,00 €", ""),
        ("Coleslaw Salat",              "2,00 €", ""),
        ("Krautsalat mit Knoblauch",    "2,00 €", ""),
        ("Sour Cream",                  "1,00 €", ""),
        ("Ketchup / Mayo / Remoulade / Burger Soße / Senf", "0,50 €", ""),
    ]

    salat = [
        ("Cesar",                       "10,90 €","Salat, Tomate, Gurke, Hähnchenbrust"),
        ("Bunter Blattsalat mit Lachs", "12,90 €",""),
        ("Tomate Mozarella",            "3,90 €", "Rucola, Tomate, Mozarella mit Balsamico"),
        ("Bauernsalat",                 "5,90 €", "Gemischter Salat mit Weißkäse"),
        ("Gemischter Salat",            "3,90 €", ""),
        ("Krautsalat",                  "3,90 €", "mit Öl und Essig"),
        ("Eingelegte Paprika (Ovčavina)","3,90 €","in Schmand"),
        ("Eingelegte Paprika",          "3,90 €", "mit Knoblauch und Öl"),
    ]

    dessert = [
        ("Trilece",       "2,00 €", "Milchkuchen mit Karamell"),
        ("Krempita",      "2,00 €", "Vanillecremetorte"),
        ("Šampita",       "2,00 €", "Baiser-Dessert mit Biskuit-Boden"),
        ("Tulumbe",       "1,00 €", "Spritzgebäck"),
        ("Hurmasice",     "1,00 €", "in Sirup getränktes Gebäck"),
        ("Baklava",       "1,60 €", "mit Walnuss"),
        ("Apfel Pita",    "1,60 €", "Filoteig gefüllt mit Apfel"),
        ("Tortenstück",   "ab 2,00 €","Unsere vielfältige Tortenauswahl wartet auf Sie. Preise entnehmen Sie bitte aus der Kuchentheke."),
    ]

    kalt = [
        ("Mineralwasser",         "2,50 €", "0,25 Liter"),
        ("Softgetränk",           "2,50 €", "Cola, Fanta, Sprite – 0,33 Liter"),
        ("Bitter Lemon",          "2,50 €", "0,33 Liter"),
        ("Red Bull",              "2,50 €", "0,2 Liter"),
        ("Saft",                  "2,00 €", "Orange, Apfel – 0,33 Liter"),
        ("Ayran",                 "1,90 €", ""),
        ("Joghurt",               "1,90 €", ""),
        ("Hausgemachte Limonade", "3,50 €", "Zitrone, Blaubeere"),
    ]

    heiss = [
        ("Kaffee Crema",    "2,50 € / 2,90 €", "Klein / Groß"),
        ("Cappuccino",      "3,60 €", ""),
        ("Latte Macchiatto","3,80 €", ""),
        ("Heißer Kakao",    "3,20 €", "mit aufgeschäumter Milch"),
        ("Espresso",        "2,30 €", ""),
        ("Bosnischer Kaffe","2,50 €", ""),
        ("Tee",             "2,50 €", "diverse Sorten: Schwarzer Tee, Minze, Waldbeere, Kamille, etc."),
    ]

    allergens = [
        ("A", "Glutenhaltiges Getreide: Weizen"),
        ("B", "Krebstiere und daraus gewonnene Erzeugnisse"),
        ("C", "Eier und daraus gewonnene Erzeugnisse"),
        ("D", "Fische und daraus gewonnene Erzeugnisse"),
        ("E", "Erdnüsse und daraus gewonnene Erzeugnisse"),
        ("F", "Sojabohnen und daraus gewonnene Erzeugnisse"),
        ("G", "Milch und daraus gewonnene Erzeugnisse, einschließlich Lactose"),
        ("H", "Schalenfrüchte: Mandeln / Haselnüsse / Walnüsse / Pistazien"),
        ("I", "Sellerie und daraus gewonnene Erzeugnisse"),
        ("J", "Senf und daraus gewonnene Erzeugnisse"),
        ("K", "Sesamsamen und daraus gewonnene Erzeugnisse"),
        ("L", "Schwefeldioxid und Sulfite"),
        ("M", "Lupinen und daraus gewonnene Erzeugnisse"),
        ("N", "Weichtiere und daraus gewonnene Erzeugnisse"),
    ]

    allergen_rows = "\n".join(f"""
            <div class="allergen-row">
                <div class="allergen-code">{code}</div>
                <div class="allergen-text">{text}</div>
            </div>""" for code, text in allergens)

    html = head("Speisekarte", css)
    html += page_hero_strip("Preise & Speisen", "<em>Speisekarte</em>")
    html += f"""
<div class="menu-wrap">
    <p style="font-size:.85rem;line-height:2;opacity:.75;max-width:560px;margin-bottom:2.5rem;">
        Alle Preise in Euro inkl. MwSt. Allergene auf Anfrage oder siehe Legende.
    </p>

    {section("Frühstück", fruehstueck)}
    {section("Balkan Frühstück", balkan)}
    {section("Rührei", ruehrei, cols=1)}
    {section("Burger", burger, cols=1)}
    {section("Ćevapčići", cevapcici, cols=1)}
    {section("Nudel", nudel, cols=1)}
    {section("Zum Dazubestellen", beilage)}
    {section("Salat", salat)}
    {section("Dessert", dessert)}
    {section("Kalte Getränke", kalt)}
    {section("Heiße Getränke", heiss, cols=1)}
</div>

<div class="allergen-section">
    <div class="allergen-inner">
        <p class="section-label">Kennzeichnung</p>
        <h2 class="section-title">Allergene & <em>Zusatzstoffe</em></h2>
        <div class="allergen-cols">
{allergen_rows}
        </div>
    </div>
</div>
<p class="allergen-note">
    ⚠️ Trotz sorgfältiger Zubereitung können Spuren von Allergenen nicht ausgeschlossen werden.
    Bei schweren Allergien bitte persönlich Rücksprache halten.
</p>
"""
    html += foot()
    with open(os.path.join(OUT, "speisekarte.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("✓  speisekarte.html")


# ===========================================================================
# bestellen.html
# ===========================================================================
def build_bestellen():
    css = """
    .bestellen-outer { background:var(--bg2); }
    .bestellen-wrap { max-width:820px; margin:0 auto; padding:2.5rem 4rem 5rem; }
    .form-grid { display:grid; grid-template-columns:1fr 1fr; gap:.9rem; margin-top:2rem; }
    .form-group { display:flex; flex-direction:column; gap:.4rem; }
    .form-group.full { grid-column:1/-1; }
    label { font-size:.65rem; letter-spacing:.2em; text-transform:uppercase; color:var(--muted); }
    input[type=text], input[type=tel], input[type=date], select, textarea {
        width:100%; padding:.75rem 1rem; border:none; border-bottom:1px solid #ddd0be;
        background:transparent; font-family:'Jost',sans-serif; font-size:.88rem;
        color:var(--text); outline:none; transition:border .2s; -webkit-appearance:none; border-radius:0; }
    input[type=text]:focus, input[type=tel]:focus, input[type=date]:focus,
    select:focus, textarea:focus { border-bottom-color:var(--brown); }
    textarea { resize:vertical; min-height:90px; border:1px solid #ddd0be; padding:.75rem 1rem; background:var(--bg); }
    textarea:focus { border-color:var(--brown); }
    .form-submit { margin-top:2rem; text-align:right; }

    /* FLAVOR CHECKBOXES */
    .flavor-label { font-size:.65rem; letter-spacing:.2em; text-transform:uppercase; color:var(--muted); margin-bottom:.8rem; display:block; }
    .flavor-checks { display:flex; flex-wrap:wrap; gap:.5rem; }
    .flavor-chip { display:flex; align-items:center; gap:0; cursor:pointer; }
    .flavor-chip input[type=checkbox] { display:none; }
    .flavor-chip-box {
        display:inline-flex; align-items:center; gap:.45rem;
        padding:.38rem .85rem; border:1px solid #c4a882;
        font-size:.75rem; color:var(--brown); letter-spacing:.05em;
        transition:background .15s, color .15s, border-color .15s;
        user-select:none; cursor:pointer;
    }
    .flavor-chip input[type=checkbox]:checked + .flavor-chip-box {
        background:var(--brown); color:#fff; border-color:var(--brown);
    }
    .anfrage-field { margin-top:.8rem; display:none; }
    .anfrage-field.visible { display:block; }

    /* WHATSAPP CHECKBOX */
    .whatsapp-check { display:flex; align-items:flex-start; gap:.75rem; margin-top:1.2rem; grid-column:1/-1; cursor:pointer; }
    .whatsapp-check input[type=checkbox] { display:none; }
    .whatsapp-custom-box {
        width:20px; height:20px; min-width:20px; border:2px solid var(--brown-mid);
        display:flex; align-items:center; justify-content:center;
        margin-top:2px; transition:background .15s, border-color .15s; flex-shrink:0;
    }
    .whatsapp-check input[type=checkbox]:checked ~ .whatsapp-custom-box {
        background:var(--brown); border-color:var(--brown);
    }
    .whatsapp-check input[type=checkbox]:checked ~ .whatsapp-custom-box::after {
        content:'✓'; color:#fff; font-size:.75rem; line-height:1;
    }
    .whatsapp-check-label { font-size:.78rem; color:var(--muted); line-height:1.6; text-transform:none; letter-spacing:0; }
    .whatsapp-custom-box.error { border-color:#c0392b; background:rgba(192,57,43,.08); }
    .whatsapp-custom-box.shake {
        animation: shake .4s ease;
    }
    @keyframes shake {
        0%,100% { transform:translateX(0); }
        20%      { transform:translateX(-6px); }
        40%      { transform:translateX(6px); }
        60%      { transform:translateX(-4px); }
        80%      { transform:translateX(4px); }
    }
    @media(max-width:720px) { .bestellen-wrap { padding-left:1.5rem; padding-right:1.5rem; } .form-grid { grid-template-columns:1fr; } }
    """

    flavors = [
        "Vanille & Sahne", "Schokolade", "Erdbeere", "Orange",
        "Zitrone & Limette", "Raffaello", "Karamell", "Kokos",
        "Kirsch", "Lotus Biscoff", "Cheesecake", "Nuss-Nougat",
    ]
    flavor_chips = "\n".join(f"""
                <label class="flavor-chip">
                    <input type="checkbox" name="flavor" value="{f}" />
                    <span class="flavor-chip-box">{f}</span>
                </label>""" for f in flavors)

    html = head("Bestellen", css)
    html += page_hero_strip("Online bestellen", "Ihre <em>Torte</em> bestellen")
    html += f"""
<div class="bestellen-outer">
<div class="bestellen-wrap">
    <p style="font-size:.87rem;line-height:2;opacity:.75;max-width:560px;margin-top:.5rem;">
        Füllen Sie das Formular aus – wir melden uns innerhalb von 48 Stunden.
        Bitte mindestens 2 Wochen im Voraus anfragen.
    </p>
    <div class="form-grid">
        <div class="form-group"><label>Vorname</label><input type="text" placeholder="Ihr Vorname" /></div>
        <div class="form-group"><label>Nachname</label><input type="text" placeholder="Ihr Nachname" /></div>
        <div class="form-group full"><label>Telefonnummer</label><input type="tel" placeholder="+49 …" /></div>
        <div class="form-group"><label>Anlass</label>
            <select><option value="">Bitte wählen …</option>
                <option>Hochzeit</option><option>Geburtstag</option><option>Jubiläum</option>
                <option>Taufe / Kommunion</option><option>Firmenevent</option><option>Beerdigung</option><option>Sonstiges</option>
            </select>
        </div>
        <div class="form-group"><label>Abholtermin</label><input type="date" /></div>
        <div class="form-group"><label>Portionen</label>
            <select>
                <option>10–15 Personen</option><option>15–25 Personen</option>
                <option>25–40 Personen</option><option>40–60 Personen</option><option>60+ Personen</option>
            </select>
        </div>

        <div class="form-group full">
            <span class="flavor-label">Geschmacksrichtung (mehrere möglich)</span>
            <div class="flavor-checks">
{flavor_chips}
                <label class="flavor-chip">
                    <input type="checkbox" id="anfrage-cb" name="flavor" value="Auf Anfrage" />
                    <span class="flavor-chip-box">Auf Anfrage</span>
                </label>
            </div>
            <div class="anfrage-field" id="anfrage-field">
                <textarea placeholder="Beschreiben Sie Ihren Wunschgeschmack …" style="margin-top:.5rem;"></textarea>
            </div>
        </div>

        <div class="form-group full"><label>Weitere Wünsche & Vorstellungen</label>
            <textarea placeholder="Design, Farben, Besonderheiten …"></textarea>
        </div>
        <div class="form-group full" style="margin-top:.5rem;">
            <label class="whatsapp-check" for="consent-all">
                <input type="checkbox" id="consent-all" name="consent" required />
                <div class="whatsapp-custom-box"></div>
                <span class="whatsapp-check-label">Ich bin damit einverstanden, dass Bäckerei Alisa mich bezüglich meiner Anfrage <strong>telefonisch oder per WhatsApp</strong> kontaktiert. *</span>
            </label>
        </div>
    </div>
    <div class="form-submit">
        <button class="btn btn-outline-dark" id="submit-btn">
            Anfrage absenden
        </button>
    </div>
</div>
</div>
<script>
document.getElementById('anfrage-cb').addEventListener('change', function() {{
    const field = document.getElementById('anfrage-field');
    field.classList.toggle('visible', this.checked);
}});

document.getElementById('submit-btn').addEventListener('click', function() {{
    const cb = document.getElementById('consent-all');
    const box = cb.nextElementSibling;
    if (!cb.checked) {{
        box.classList.add('shake', 'error');
        setTimeout(() => box.classList.remove('shake'), 500);
        return;
    }}
    box.classList.remove('error');
    alert('Vielen Dank! Wir melden uns bald bei Ihnen. 🎂');
}});
</script>
"""
    html += foot()
    with open(os.path.join(OUT, "bestellen.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("✓  bestellen.html")


# ===========================================================================
# kontakt.html
# ===========================================================================
def build_kontakt():
    css = """
    .kontakt-wrap { max-width:1100px; margin:0 auto; padding:2.5rem 4rem 5rem; }
    .standorte-grid { display:grid; grid-template-columns:1fr 1fr; gap:3rem; margin-top:2rem; }
    .standort { background:var(--bg); border:1px solid #e8d9c5; padding:2rem 2rem 2.5rem; }
    .standort-name { font-family:'Playfair Display',serif; font-size:1.3rem; font-style:italic;
        color:var(--brown-dark); margin-bottom:1.5rem; padding-bottom:.8rem; border-bottom:1px solid #e8d9c5; }
    .kontakt-item { display:flex; gap:1rem; align-items:flex-start; padding:.9rem 0; border-bottom:1px solid #f0e6d8; }
    .kontakt-item:last-child { border-bottom:none; }
    .kontakt-icon { width:28px; height:28px; display:flex; align-items:center; justify-content:center; font-size:.95rem; flex-shrink:0; color:var(--brown); margin-top:1px; }
    .kontakt-label { font-size:.62rem; letter-spacing:.2em; text-transform:uppercase; color:var(--muted); margin-bottom:.2rem; }
    .kontakt-value { font-size:.85rem; color:var(--text); line-height:1.65; }
    .map-box { width:100%; height:200px; background:var(--bg2); display:flex; align-items:center;
        justify-content:center; border:1px solid #e8d9c5; font-family:'Playfair Display',serif;
        font-style:italic; color:var(--muted); font-size:.85rem; margin-top:1.5rem; }
    .social-strip { max-width:1100px; margin:2.5rem auto 0; padding:0 4rem;
        display:flex; align-items:center; gap:1rem; }
    .social-strip p { font-size:.82rem; color:var(--muted); }
    @media(max-width:720px) {
        .kontakt-wrap { padding-left:1.5rem; padding-right:1.5rem; }
        .standorte-grid { grid-template-columns:1fr; gap:1.5rem; }
        .social-strip { padding-left:1.5rem; padding-right:1.5rem; }
    }
    """

    def standort_html(name, items, map_id):
        rows = "\n".join(f"""
            <div class="kontakt-item">
                <div class="kontakt-icon">{icon}</div>
                <div><p class="kontakt-label">{label}</p><p class="kontakt-value">{value}</p></div>
            </div>""" for icon, label, value in items)
        return f"""
        <div class="standort">
            <p class="standort-name">{name}</p>
{rows}
            <div class="map-box" id="{map_id}">
                Google Maps hier einbetten –<br>
                &lt;iframe src="https://maps.google.com/..." ...&gt;&lt;/iframe&gt;
            </div>
        </div>"""

    standort1 = standort_html("Standort 1 – Essen Mitte", [
        ("📍", "Adresse",        "Musterstraße 12<br>45127 Essen"),
        ("📞", "Telefon",        "+49 (0)201 123 456 78"),
        ("✉️",  "E-Mail",         "info@baeckerei-alisa.de"),
        ("🕐", "Öffnungszeiten", "Di – Fr: 09:00 – 18:00 Uhr<br>Sa: 09:00 – 14:00 Uhr<br>So & Mo: geschlossen"),
    ], map_id="map-standort-1")

    standort2 = standort_html("Standort 2 – Essen Nord", [
        ("📍", "Adresse",        "Beispielweg 45<br>45144 Essen"),
        ("📞", "Telefon",        "+49 (0)201 987 654 32"),
        ("✉️",  "E-Mail",         "info@baeckerei-alisa.de"),
        ("🕐", "Öffnungszeiten", "Mo – Fr: 08:00 – 17:00 Uhr<br>Sa: 08:00 – 13:00 Uhr<br>So: geschlossen"),
    ], map_id="map-standort-2")

    html = head("Kontakt", css)
    html += page_hero_strip("Finden Sie uns", "<em>Kontakt</em> & Anfahrt")
    html += f"""
<div class="kontakt-wrap">
    <p class="section-label" style="margin-top:2rem;">Unsere zwei Standorte</p>
    <h2 class="section-title">Wir sind <em>zweimal</em> für Sie da</h2>
    <div class="standorte-grid">
        {standort1}
        {standort2}
    </div>
</div>
<div class="social-strip">
    <span style="font-size:1.1rem;">📱</span>
    <p>Folgen Sie uns auf Instagram: <strong>@baeckerei.alisa</strong></p>
</div>
<div style="height:4rem;"></div>
"""
    html += foot()
    with open(os.path.join(OUT, "kontakt.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("✓  kontakt.html")


# ===========================================================================
# impressum.html
# ===========================================================================
def build_impressum():
    css = """
    .legal-wrap { max-width:820px; margin:0 auto; padding:3rem 4rem 5rem; }
    .legal-wrap h2 { font-family:'Playfair Display',serif; font-size:1.1rem; font-weight:400;
        color:var(--brown-dark); margin:2rem 0 .6rem; }
    .legal-wrap p, .legal-wrap a { font-size:.87rem; line-height:2; color:var(--text); opacity:.8; }
    .legal-wrap a { color:var(--brown); }
    .legal-section { margin-bottom:1.5rem; padding-bottom:1.5rem; border-bottom:1px solid #e8d9c5; }
    .legal-section:last-child { border-bottom:none; }
    @media(max-width:720px) { .legal-wrap { padding-left:1.5rem; padding-right:1.5rem; } }
    """

    html = head("Impressum", css, base="../")
    html += page_hero_strip("Rechtliches", "<em>Impressum</em>")
    html += """
<div class="legal-wrap">

    <div class="legal-section">
        <h2>Angaben gemäß § 5 TMG</h2>
        <p>
            [Vollständiger Name / Firmenname]<br>
            [Straße und Hausnummer]<br>
            [PLZ] [Ort]
        </p>
    </div>

    <div class="legal-section">
        <h2>Kontakt</h2>
        <p>
            Telefon: [Telefonnummer]<br>
            E-Mail: [E-Mail-Adresse]
        </p>
    </div>

    <div class="legal-section">
        <h2>Umsatzsteuer-ID</h2>
        <p>
            Umsatzsteuer-Identifikationsnummer gemäß § 27a Umsatzsteuergesetz:<br>
            [USt-IdNr. oder Steuernummer]
        </p>
    </div>

    <div class="legal-section">
        <h2>Verantwortlich für den Inhalt nach § 55 Abs. 2 RStV</h2>
        <p>
            [Name der verantwortlichen Person]<br>
            [Anschrift wie oben]
        </p>
    </div>

    <div class="legal-section">
        <h2>Streitschlichtung</h2>
        <p>
            Die Europäische Kommission stellt eine Plattform zur Online-Streitbeilegung (OS) bereit:
            <a href="https://ec.europa.eu/consumers/odr/" target="_blank">https://ec.europa.eu/consumers/odr/</a><br>
            Unsere E-Mail-Adresse finden Sie oben im Impressum.
        </p>
        <p style="margin-top:.8rem;">
            Wir sind nicht bereit oder verpflichtet, an Streitbeilegungsverfahren vor einer
            Verbraucherschlichtungsstelle teilzunehmen.
        </p>
    </div>

    <div class="legal-section">
        <h2>Haftung für Inhalte</h2>
        <p>
            Als Diensteanbieter sind wir gemäß § 7 Abs. 1 TMG für eigene Inhalte auf diesen Seiten
            nach den allgemeinen Gesetzen verantwortlich. Nach §§ 8 bis 10 TMG sind wir als
            Diensteanbieter jedoch nicht verpflichtet, übermittelte oder gespeicherte fremde
            Informationen zu überwachen oder nach Umständen zu forschen, die auf eine rechtswidrige
            Tätigkeit hinweisen.
        </p>
    </div>

    <div class="legal-section">
        <h2>Haftung für Links</h2>
        <p>
            Unser Angebot enthält Links zu externen Websites Dritter, auf deren Inhalte wir keinen
            Einfluss haben. Deshalb können wir für diese fremden Inhalte auch keine Gewähr übernehmen.
            Für die Inhalte der verlinkten Seiten ist stets der jeweilige Anbieter oder Betreiber der
            Seiten verantwortlich.
        </p>
    </div>

    <div class="legal-section">
        <h2>Urheberrecht</h2>
        <p>
            Die durch die Seitenbetreiber erstellten Inhalte und Werke auf diesen Seiten unterliegen
            dem deutschen Urheberrecht. Die Vervielfältigung, Bearbeitung, Verbreitung und jede Art
            der Verwertung außerhalb der Grenzen des Urheberrechtes bedürfen der schriftlichen
            Zustimmung des jeweiligen Autors bzw. Erstellers.
        </p>
    </div>

</div>
"""
    html += foot(base="../")
    os.makedirs(os.path.join(OUT, "rechtliches"), exist_ok=True)
    with open(os.path.join(OUT, "rechtliches", "impressum.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("✓  rechtliches/impressum.html")


# ===========================================================================
# datenschutz.html
# ===========================================================================
def build_datenschutz():
    css = """
    .legal-wrap { max-width:820px; margin:0 auto; padding:3rem 4rem 5rem; }
    .legal-wrap h2 { font-family:'Playfair Display',serif; font-size:1.1rem; font-weight:400;
        color:var(--brown-dark); margin:2rem 0 .6rem; }
    .legal-wrap p, .legal-wrap a { font-size:.87rem; line-height:2; color:var(--text); opacity:.8; }
    .legal-wrap a { color:var(--brown); }
    .legal-section { margin-bottom:1.5rem; padding-bottom:1.5rem; border-bottom:1px solid #e8d9c5; }
    .legal-section:last-child { border-bottom:none; }
    @media(max-width:720px) { .legal-wrap { padding-left:1.5rem; padding-right:1.5rem; } }
    """

    html = head("Datenschutz", css, base="../")
    html += page_hero_strip("Rechtliches", "<em>Datenschutzerklärung</em>")
    html += """
<div class="legal-wrap">

    <div class="legal-section">
        <h2>1. Datenschutz auf einen Blick</h2>
        <p>
            Die folgenden Hinweise geben einen einfachen Überblick darüber, was mit Ihren
            personenbezogenen Daten passiert, wenn Sie diese Website besuchen.
            Personenbezogene Daten sind alle Daten, mit denen Sie persönlich identifiziert
            werden können.
        </p>
    </div>

    <div class="legal-section">
        <h2>2. Verantwortliche Stelle</h2>
        <p>
            Die verantwortliche Stelle für die Datenverarbeitung auf dieser Website ist:<br><br>
            [Name / Firmenname]<br>
            [Straße und Hausnummer]<br>
            [PLZ] [Ort]<br>
            Telefon: [Telefonnummer]<br>
            E-Mail: [E-Mail-Adresse]
        </p>
    </div>

    <div class="legal-section">
        <h2>3. Datenerfassung auf dieser Website</h2>
        <p>
            Diese Website erhebt und speichert automatisch Informationen in Server-Log-Dateien,
            die Ihr Browser automatisch übermittelt. Dies sind: Browsertyp und -version,
            verwendetes Betriebssystem, Referrer-URL, Hostname des zugreifenden Rechners,
            Uhrzeit der Serveranfrage und IP-Adresse. Eine Zusammenführung dieser Daten mit
            anderen Datenquellen wird nicht vorgenommen.
        </p>
    </div>

    <div class="legal-section">
        <h2>4. Kontaktformular</h2>
        <p>
            Wenn Sie uns per Kontaktformular Anfragen zukommen lassen, werden Ihre Angaben aus
            dem Anfrageformular inklusive der von Ihnen dort angegebenen Kontaktdaten zwecks
            Bearbeitung der Anfrage und für den Fall von Anschlussfragen bei uns gespeichert.
            Diese Daten geben wir nicht ohne Ihre Einwilligung weiter.
        </p>
    </div>

    <div class="legal-section">
        <h2>5. WhatsApp-Kontakt</h2>
        <p>
            Wenn Sie uns die Erlaubnis erteilen, Sie per WhatsApp zu kontaktieren, werden Ihre
            Telefonnummer und Ihre Anfrage an den WhatsApp-Dienst (Meta Platforms Ireland Limited)
            übermittelt. Bitte beachten Sie die Datenschutzrichtlinien von WhatsApp:
            <a href="https://www.whatsapp.com/legal/privacy-policy" target="_blank">
            whatsapp.com/legal/privacy-policy</a>
        </p>
    </div>

    <div class="legal-section">
        <h2>6. Ihre Rechte</h2>
        <p>
            Sie haben jederzeit das Recht auf unentgeltliche Auskunft über Ihre gespeicherten
            personenbezogenen Daten, deren Herkunft und Empfänger und den Zweck der
            Datenverarbeitung sowie ein Recht auf Berichtigung oder Löschung dieser Daten.
            Hierzu sowie zu weiteren Fragen zum Thema Datenschutz können Sie sich jederzeit
            unter der im Impressum angegebenen Adresse an uns wenden.
        </p>
    </div>

    <div class="legal-section">
        <h2>7. Hinweis</h2>
        <p>
            Diese Datenschutzerklärung wurde vereinfacht erstellt und dient als Platzhalter.
            Wir empfehlen, einen vollständigen und rechtssicheren Datenschutztext über einen
            Datenschutz-Generator oder einen Rechtsanwalt zu erstellen.
        </p>
    </div>

</div>
"""
    html += foot(base="../")
    os.makedirs(os.path.join(OUT, "rechtliches"), exist_ok=True)
    with open(os.path.join(OUT, "rechtliches", "datenschutz.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("✓  rechtliches/datenschutz.html")


# ===========================================================================
# Run all builders
# ===========================================================================
if __name__ == "__main__":
    build_index()
    build_showroom()
    build_events()
    build_speisekarte()
    build_bestellen()
    build_kontakt()
    build_impressum()
    build_datenschutz()
    print("\nAlle Seiten erfolgreich generiert!")
    print(f"Ordner: {OUT}")