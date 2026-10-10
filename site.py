"""Axon Global Services static site.

One class. Static methods. Plain HTML, one stylesheet, one menu script, one self-hosted grotesque.
"""

from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path


class Site:
    """Generate, audit, and measure the static site."""

    ROOT = Path(__file__).resolve().parent
    OUT = ROOT / "site"
    REPORTS = ROOT / "reports"
    ORIGIN = "https://undercl0ck.github.io/project-web-ac/"
    MAILTO = (
        "mailto:AxonInfo@AxonCyber.com"
        "?subject=Request%20a%2015-minute%20briefing"
    )
    ACTION = "Request a 15-minute briefing"
    PHONE = "(202) 248-5050"
    EMAIL = "AxonInfo@AxonCyber.com"
    SOURCE = "https://axoncyber.com/how-we-engage/"

    PAGES = (
        {"slug": "", "nav": None, "title": "Home", "home": True},
        {"slug": "capabilities", "nav": "Capabilities", "title": "Capabilities"},
        {"slug": "who", "nav": "Who it is for", "title": "Who it is for"},
        {"slug": "clients", "nav": "Clients", "title": "Our Clients"},
        {"slug": "credentials", "nav": "Credentials", "title": "Credentials"},
        {"slug": "recognition", "nav": "Recognitions", "title": "Recognitions"},
        {"slug": "recognition-2", "nav": None, "title": "Recognitions, continued"},
        {"slug": "recognition-3", "nav": None, "title": "Recognitions, continued"},
        {"slug": "news", "nav": "News", "title": "News"},
        {"slug": "faq", "nav": "FAQs", "title": "FAQs"},
        {"slug": "government", "nav": "Government Quals", "title": "Government Quals"},
        {"slug": "fyi", "nav": "FYI", "title": "FYI"},
        {"slug": "proof", "nav": "Proof", "title": "Proof"},
        {"slug": "authority", "nav": "Authority", "title": "Authority"},
        {"slug": "insights", "nav": "Insights", "title": "Insights"},
        {"slug": "about", "nav": "About", "title": "About"},
        {"slug": "engage", "nav": "Engage", "title": "Engage"},
        {"slug": "sitemap", "nav": None, "title": "Sitemap"},
    )

    # Six top-level items. The briefing link stays in the mast, beside this menu.
    MENU = (
        {"label": "Capabilities", "slug": "capabilities", "children": ()},
        {"label": "Who it is for", "slug": "who", "children": ()},
        {
            "label": "Credentials",
            "slug": "credentials",
            "children": (
                ("Clients", "clients"),
                ("Recognitions", "recognition"),
                ("Government Quals", "government"),
            ),
        },
        {
            "label": "Insights",
            "slug": "insights",
            "children": (
                ("News", "news"),
                ("FYI", "fyi"),
                ("FAQs", "faq"),
            ),
        },
        {
            "label": "About",
            "slug": "about",
            "children": (
                ("Proof", "proof"),
                ("Authority", "authority"),
            ),
        },
        {"label": "Engage", "slug": "engage", "children": ()},
    )

    OFFERINGS = (
        {
            "id": "training",
            "name": "Cyber Enterprise Risk Management Training",
            "card": "Cyber Enterprise Risk Management Training",
            "card_line": "For directors and the C-suite, on site or by webinar.",
            "home": True,
            "body": (
                "By NACD® credentialed experts, on site or webinar. "
                "For board members or C-suite executives."
            ),
        },
        {
            "id": "board-view",
            "name": "Board View Cyber Risk Assessment",
            "card": "Board View Cyber Risk Assessment",
            "card_line": "A third-party report of material threats, written for the board.",
            "home": True,
            "body": (
                "A third-party report of material cyber threats the organization "
                "had not already identified, written for the board."
            ),
        },
        {
            "id": "ma",
            "name": "M&A Risk Assessment",
            "card": "M&A Risk Assessment",
            "card_line": "A report on whether a company being acquired is already compromised.",
            "home": True,
            "body": (
                "A report on whether a company being acquired is compromised, "
                "including whether intellectual property has been taken."
            ),
        },
        {
            "id": "supply",
            "name": "Supply Chain Risk Assessment",
            "card": "Supply Chain Risk Assessment",
            "card_line": "A report on which suppliers present a cyber risk.",
            "home": True,
            "body": "A report identifying suppliers that present a cyber risk to the organization.",
        },
        {
            "id": "program",
            "name": "Cybersecurity Program Assessment",
            "card": "Cybersecurity Program Assessment",
            "card_line": "A report of gaps between the program and current threats.",
            "home": True,
            "body": "A third-party report of gaps between the current program and current threats.",
        },
        {
            "id": "external",
            "name": "External Security Posture Assessment (dark-web and deep-net search)",
            "card": "External Security Posture Assessment",
            "card_line": "What is visible from outside, including a dark-web and deep-net search.",
            "home": True,
            "body": (
                "A report of what is visible from outside the organization, "
                "including a dark-web and deep-net search for compromises."
            ),
        },
        {
            "id": "internal",
            "name": "Internal Security Posture Assessment",
            "card": "Internal Security Posture Assessment",
            "card_line": "",
            "home": False,
            "body": (
                "A third-party review of logs for espionage and other threats "
                "that do not match a known signature."
            ),
        },
        {
            "id": "proactive",
            "name": "Cyber Proactive Defense",
            "card": "Cyber Proactive Defense",
            "card_line": "",
            "home": False,
            "body": (
                "Discrete services performed within U.S. or international law, "
                "directed at stopping an attack."
            ),
        },
    )

    BANNED = (
        "did you know",
        "liability shield",
        "127 unique",
        "127 benefit",
        "no one else",
        "18 differentiator",
        "18 material",
        "cage code",
        "uei:",
        "34 million",
        "$34",
        "48 hour",
        "72 hour",
        "within 48",
        "within 72",
        "falcon",
        "drone",
        "binary rain",
        "grumpy gears",
        "handshake",
        "nothing was added",
        "prior engagement",
        "prior capabilities",
        "not an axon finding",
        "ready to publish",
        "no proof is printed",
        "not published",
        "no claim",
        "as printed",
        "9.5",
        "blockquote",
        "unverified",
        "x-content-type-options",
    )

    CLIENTS = (
        "american bar association",
        "akin gump",
        "autozone",
        "bank of america",
        "blue cross",
        "coca cola",
        "coca-cola",
        "capital one",
        "carnival",
        "care first",
        "comcast",
        "cmi group",
        "discovery channel",
        "department of justice",
        "exelon",
        "federal trade commission",
        "globes international",
        "finish line",
        "general electric",
        "general motors",
        "humana",
        "hispanic national bar",
        "jones day",
        "levis strauss",
        "levi strauss",
        "lewis & brisbois",
        "liberty mutual",
        "manpower",
        "marriott",
        "mass mutual",
        "mcdonald",
        "money gram",
        "moneygram",
        "mutual of omaha",
        "northern trust",
        "people lease",
        "prudential",
        "pscu",
        "tommy hilfiger",
        "home depot",
        "time warner",
        "walt disney",
        "walgreens",
        "walmart",
        "wells fargo",
        "wyndham",
        "7-eleven",
    )

    @staticmethod
    def build() -> int:
        Site.render()
        problems = Site.audit()
        header = Site.header_scan()
        weight = Site.weights()
        Site.REPORTS.mkdir(parents=True, exist_ok=True)
        (Site.REPORTS / "header-scan.json").write_text(
            json.dumps(header, indent=2) + "\n", encoding="utf-8"
        )
        (Site.REPORTS / "page-weight.json").write_text(
            json.dumps(weight, indent=2) + "\n", encoding="utf-8"
        )
        if problems:
            for item in problems:
                print("AUDIT", item)
            return 1
        over = [row for row in weight["pages"] if not row["under_limit"]]
        if over:
            for row in over:
                print("WEIGHT", row["path"], row["total_bytes"])
            return 1
        print("pages", len(list(Site.OUT.rglob("*.html"))))
        for row in weight["pages"]:
            print(f"{row['total_bytes']:7d}  {row['path']}")
        return 0

    @staticmethod
    def render() -> None:
        font_dir = Site.OUT / "assets" / "fonts"
        font_dir.mkdir(parents=True, exist_ok=True)
        font = Site.ROOT / "fonts" / "libre-franklin-latin.woff2"
        (font_dir / "libre-franklin-latin.woff2").write_bytes(font.read_bytes())
        ofl = Site.ROOT / "fonts" / "OFL.txt"
        if ofl.exists():
            (font_dir / "OFL.txt").write_text(ofl.read_text(encoding="utf-8"), encoding="utf-8")
        media_out = Site.OUT / "assets" / "media"
        media_out.mkdir(parents=True, exist_ok=True)
        for src in sorted((Site.ROOT / "media").glob("*.webp")):
            (media_out / src.name).write_bytes(src.read_bytes())
        logo_dir = Site.ROOT / "media" / "logos"
        if logo_dir.is_dir():
            for src in sorted(logo_dir.iterdir()):
                if src.suffix.lower() in {".svg", ".webp", ".png"}:
                    (media_out / src.name).write_bytes(src.read_bytes())
        css_path = Site.OUT / "assets" / "site.css"
        css_path.write_text(Site.css(), encoding="utf-8")
        (Site.OUT / "assets" / "menu.js").write_text(Site.menu_script(), encoding="utf-8")
        (Site.OUT / "favicon.png").write_bytes((Site.ROOT / "media" / "favicon-32.png").read_bytes())
        (Site.OUT / "apple-touch-icon.png").write_bytes(
            (Site.ROOT / "media" / "favicon-180.png").read_bytes()
        )
        (Site.OUT / ".nojekyll").write_text("", encoding="utf-8")
        (Site.OUT / "robots.txt").write_text(Site.robots(), encoding="utf-8")
        (Site.OUT / "sitemap.xml").write_text(Site.sitemap_xml(), encoding="utf-8")
        for page in Site.PAGES:
            html = Site.document(page, Site.body(page))
            path = Site.page_path(page["slug"])
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(html, encoding="utf-8")
        missing = Site.document(
            {"slug": "", "nav": None, "title": "Not found", "missing": True},
            Site.missing_body(),
        )
        (Site.OUT / "404.html").write_text(missing, encoding="utf-8")

    @staticmethod
    def page_path(slug: str) -> Path:
        if slug == "":
            return Site.OUT / "index.html"
        return Site.OUT / slug / "index.html"

    @staticmethod
    def href(from_slug: str, to_slug: str) -> str:
        if to_slug == "":
            return "./" if from_slug == "" else "../"
        if from_slug == "":
            return to_slug + "/"
        if from_slug == to_slug:
            return "./"
        return "../" + to_slug + "/"

    @staticmethod
    def canonical(slug: str) -> str:
        if slug == "":
            return Site.ORIGIN
        return Site.ORIGIN + slug + "/"

    @staticmethod
    def folio(slug: str) -> str:
        for index, item in enumerate(Site.MENU, start=1):
            slugs = {item["slug"], *[dest for _label, dest in item["children"]]}
            if slug in slugs or (item["slug"] == "credentials" and slug.startswith("recognition")):
                return f"{index:02d}"
        return ""

    @staticmethod
    def current(slug: str, dest: str) -> bool:
        if slug == dest:
            return True
        return dest == "recognition" and slug.startswith("recognition")

    @staticmethod
    def action_link() -> str:
        return f'<a class="action" href="{Site.MAILTO}">{Site.ACTION}</a>'

    @staticmethod
    def mark(large: bool = False) -> str:
        if not large:
            return (
                '<svg class="mark" viewBox="0 0 160 160" aria-hidden="true">'
                '<rect x="14" y="32" width="108" height="108" fill="none" stroke="currentColor" stroke-width="1"/>'
                '<rect x="38" y="12" width="108" height="108" fill="none" stroke="currentColor" stroke-width="1"/>'
                '<rect x="58" y="50" width="60" height="60" fill="currentColor"/>'
                "</svg>"
            )
        return (
            '<svg class="mark mark-lg" viewBox="0 0 520 640" aria-hidden="true">'
            '<rect x="28" y="78" width="330" height="470" fill="none" stroke="currentColor" stroke-width="1.5"/>'
            '<rect x="118" y="18" width="360" height="430" fill="none" stroke="currentColor" stroke-width="1.5"/>'
            '<rect x="62" y="168" width="300" height="430" fill="none" stroke="currentColor" stroke-width="1.5"/>'
            '<rect x="154" y="118" width="250" height="330" fill="currentColor"/>'
            '<g class="mass">'
            '<rect class="recess" x="196" y="196" width="168" height="210"/>'
            '<rect x="196" y="196" width="168" height="210" fill="none" stroke="currentColor" stroke-width="1.5"/>'
            '<rect class="signal-edge" x="196" y="196" width="168" height="4"/>'
            "</g></svg>"
        )

    @staticmethod
    def hero_photo(slug: str) -> str:
        row = next(item for item in Site.catalog() if item["id"] == "hero-briefing")
        sizes = "(max-width: 800px) calc(100vw - 1.5rem), 28rem"
        return f'<figure class="hero-photo">{Site.image(slug, row, sizes)}</figure>'

    @staticmethod
    def wordmark(slug: str) -> str:
        src = Site.media_src(slug, "mark-logo.webp")
        small = Site.media_src(slug, "mark-logo-96.webp")
        return (
            f'<a class="wordmark" href="{Site.href(slug, "")}">'
            f'<img class="logo" src="{src}" srcset="{small} 96w, {src} 200w" '
            'sizes="48px" alt="Axon Global Services" width="200" height="180">'
            '<span class="wordmark-type">'
            '<span class="wordmark-name">Axon</span>'
            '<span class="wordmark-line">Global Services</span>'
            "</span></a>"
        )

    @staticmethod
    def close_band() -> str:
        return f"""
<aside class="close" aria-label="Briefing">
<div class="frame close-grid">
<div>
<p class="eyebrow">Briefing</p>
<h2>{Site.ACTION}</h2>
<p>The request opens an email to {Site.EMAIL}.</p>
</div>
<p class="close-action">{Site.action_link()}</p>
</div>
</aside>
"""

    @staticmethod
    def document(page: dict, main: str) -> str:
        slug = page["slug"]
        title = escape(page["title"])
        body_class = ' class="opening"' if page.get("home") else ""
        depth = "" if slug == "" else "../"
        description = escape(
            "Training on site or by webinar, and assessments explained in plain business language."
            if page.get("home")
            else "Axon Global Services. Board training and pre-emptive cyber risk work."
        )
        csp = (
            "default-src 'self'; base-uri 'none'; object-src 'none'; "
            "form-action 'none'; script-src 'self'; style-src 'self'; "
            "img-src 'self' data:; font-src 'self'; connect-src 'none'; "
            "frame-src 'none'; worker-src 'none'; manifest-src 'self'; "
            "upgrade-insecure-requests"
        )
        folio = Site.folio(slug)
        folio_html = f'<p class="folio">{folio}</p>' if folio else '<p class="folio"></p>'
        if page.get("home"):
            content = main
        else:
            content = f'<div class="paper"><div class="frame page">{main}</div></div>'
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} — Axon Global Services</title>
<meta name="description" content="{description}">
<meta name="referrer" content="no-referrer">
<meta http-equiv="Content-Security-Policy" content="{csp}">
<meta name="color-scheme" content="light">
<meta name="theme-color" content="#0e0d0b">
<link rel="canonical" href="{escape(Site.canonical(slug))}">
<link rel="icon" href="{depth}favicon.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="{depth}apple-touch-icon.png">
<link rel="stylesheet" href="{depth}assets/site.css">
</head>
<body{body_class}>
<a class="skip" href="#content">Skip to content</a>
<div class="wrap">
<header class="mast">
<div class="frame">
<div class="mast-top">
{Site.wordmark(slug)}
{folio_html}
<p class="mast-action">{Site.action_link()}</p>
</div>
<nav class="nav" aria-label="Pages">{Site.primary_nav(slug)}</nav>
</div>
</header>
<main id="content">
{content}
</main>
{Site.close_band()}
<footer class="colophon">
<div class="frame foot">
<div class="foot-brand">{Site.wordmark(slug)}</div>
<nav class="foot-nav" aria-label="Footer">{Site.footer_nav(slug)}</nav>
<div class="foot-side">
<p><a href="tel:+12022485050">{Site.PHONE}</a></p>
<p><a href="mailto:{Site.EMAIL}">{Site.EMAIL}</a></p>
</div>
<div class="foot-legal">
<p>© 2026 Axon Global Services</p>
<p><a href="{Site.href(slug, "sitemap")}">Sitemap</a></p>
</div>
</div>
</footer>
</div>
<script src="{depth}assets/menu.js"></script>
</body>
</html>
"""

    @staticmethod
    def menu_links(slug: str, item: dict) -> str:
        here = Site.current(slug, item["slug"]) or any(
            Site.current(slug, dest) for _label, dest in item["children"]
        )
        current = ' aria-current="page"' if Site.current(slug, item["slug"]) else ""
        if not item["children"]:
            return (
                f'<a class="menu-label" href="{Site.href(slug, item["slug"])}"{current}>'
                f'{escape(item["label"])}</a>'
            )
        parent = (
            f'<a href="{Site.href(slug, item["slug"])}"{current}>{escape(item["label"])}</a>'
        )
        links = [parent]
        for text, dest in item["children"]:
            child = ' aria-current="page"' if Site.current(slug, dest) else ""
            links.append(f'<a href="{Site.href(slug, dest)}"{child}>{escape(text)}</a>')
        edge = " menu-end" if item["slug"] in {"insights", "about"} else ""
        state = " here" if here else ""
        panel_id = "menu-" + item["slug"]
        return (
            f'<div class="menu{edge}{state}">'
            f'<button type="button" class="menu-trigger" aria-expanded="false" '
            f'aria-controls="{panel_id}">{escape(item["label"])}</button>'
            f'<div class="menu-panel" id="{panel_id}" hidden>{"".join(links)}</div>'
            "</div>"
        )

    @staticmethod
    def primary_nav(slug: str) -> str:
        groups = "".join(Site.menu_links(slug, item) for item in Site.MENU)
        return (
            '<button type="button" class="nav-toggle" aria-expanded="false" '
            'aria-controls="nav-groups" aria-label="Open menu">'
            '<span class="nav-bars" aria-hidden="true"></span>'
            "</button>"
            f'<div class="nav-groups" id="nav-groups">{groups}</div>'
        )

    @staticmethod
    def footer_nav(slug: str) -> str:
        groups = []
        for item in Site.MENU:
            links = []
            current = ' aria-current="page"' if Site.current(slug, item["slug"]) else ""
            links.append(
                f'<a href="{Site.href(slug, item["slug"])}"{current}>{escape(item["label"])}</a>'
            )
            for text, dest in item["children"]:
                child = ' aria-current="page"' if Site.current(slug, dest) else ""
                links.append(
                    f'<a href="{Site.href(slug, dest)}"{child}>{escape(text)}</a>'
                )
            groups.append(f'<div class="foot-group">{"".join(links)}</div>')
        return "".join(groups)

    @staticmethod
    def row(number: str, title: str, inner: str, element_id: str = "") -> str:
        ident = f' id="{escape(element_id)}"' if element_id else ""
        return (
            f'<section class="row"{ident}>'
            f'<p class="num">{escape(number)}</p>'
            f'<div class="row-body"><h2>{title}</h2>{inner}</div>'
            "</section>"
        )

    @staticmethod
    def body(page: dict) -> str:
        slug = page["slug"]
        writers = {
            "": Site.home_body,
            "capabilities": Site.capabilities_body,
            "who": Site.who_body,
            "clients": Site.clients_body,
            "credentials": Site.credentials_body,
            "recognition": Site.recognition_body,
            "recognition-2": Site.recognition_body,
            "recognition-3": Site.recognition_body,
            "news": Site.news_body,
            "faq": Site.faq_body,
            "government": Site.government_body,
            "fyi": Site.fyi_body,
            "proof": Site.proof_body,
            "authority": Site.authority_body,
            "insights": Site.insights_body,
            "about": Site.about_body,
            "engage": Site.engage_body,
            "sitemap": Site.sitemap_body,
        }
        return writers[slug](slug)

    @staticmethod
    def plate(index: int) -> str:
        shift = (index - 1) * 16
        return (
            '<div class="card-plate" aria-hidden="true">'
            '<svg viewBox="0 0 320 140" preserveAspectRatio="xMidYMid slice">'
            f'<rect x="{16 + shift}" y="22" width="190" height="130" fill="none" stroke="#f3efe6" stroke-width="1"/>'
            f'<rect x="{78 + shift}" y="-6" width="160" height="108" fill="none" stroke="#f3efe6" stroke-width="1"/>'
            f'<rect x="{96 + shift}" y="40" width="72" height="72" fill="#f3efe6"/>'
            f'<rect x="{96 + shift}" y="40" width="72" height="3" fill="#c6a36a"/>'
            "</svg></div>"
        )

    @staticmethod
    def home_body(_slug: str) -> str:
        cards = []
        index = 0
        for offer in Site.OFFERINGS:
            if not offer["home"]:
                continue
            index += 1
            cards.append(
                '<li class="card">'
                f"{Site.plate(index)}"
                '<div class="card-body">'
                f'<p class="idx">{index:02d}</p>'
                f'<h3><a href="capabilities/#{escape(offer["id"])}">{escape(offer["card"])}</a></h3>'
                f"<p>{escape(offer['card_line'])}</p>"
                "</div></li>"
            )
        data = Site.bundle()
        recognized = escape(data["who_credentials"][1])
        return f"""
<section class="hero">
<div class="frame">
<div class="hero-grid">
<div class="hero-copy">
<h1 class="hero-title">We train boards and general counsel on cyber risk, and deliver a written risk report before a breach.</h1>
<p class="hero-sub">Training on site or by webinar, and assessments explained in plain business language.</p>
<div class="hero-cta">
{Site.action_link()}
<a class="hero-phone" href="tel:+12022485050">{Site.PHONE}</a>
</div>
</div>
{Site.hero_photo("")}
</div>
</div>
</section>
<div class="paper">
<section class="trust">
<div class="frame">
<p class="eyebrow">Recognized by</p>
{Site.pictures("", Site.seal_rows(), "seal-grid")}
<p class="trust-line">{recognized}</p>
</div>
</section>
<div class="frame">
<section class="proofband">
<h2>Our Clients</h2>
{Site.client_logo_row("", Site.HOME_LOGOS)}
<p class="logo-more"><a href="{Site.href("", "clients")}">All clients</a></p>
{Site.figures()}
</section>
<section class="services">
<h2>Services</h2>
<ol class="cards">{"".join(cards)}</ol>
</section>
</div>
</div>
"""

    @staticmethod
    def capabilities_body(_slug: str) -> str:
        blocks = []
        for index, offer in enumerate(Site.OFFERINGS, start=1):
            blocks.append(
                f'<li class="offering" id="{escape(offer["id"])}">'
                f"{Site.plate(index)}"
                '<div class="offering-body">'
                f'<p class="idx">{index:02d}</p>'
                f"<h2>{escape(offer['name'])}</h2>"
                f"<p>{escape(offer['body'])}</p>"
                "</div></li>"
            )
        return f"""
<h1>Capabilities</h1>
<p class="lede">Eight lines of board training and pre-emptive cyber risk work.</p>
<ol class="offerings">{"".join(blocks)}</ol>
"""

    @staticmethod
    def who_body(_slug: str) -> str:
        rows = (
            (
                "Fortune 500 boards",
                "Oversight of cyber risk. The work is a briefing and an assessment, not a tool rollout.",
            ),
            (
                "General counsel",
                "Counsel reads with the board. The briefing is written for that table.",
            ),
            (
                "CISOs and executive teams",
                "A board-level view of the program, separate from day-to-day operations.",
            ),
            (
                "Private equity",
                "A view of cyber risk in a transaction, before close.",
            ),
            (
                "Government and critical-infrastructure readers",
                "The same training and pre-emptive assessments, read from a public-interest seat.",
            ),
        )
        blocks = []
        for index, (title, line) in enumerate(rows, start=1):
            blocks.append(Site.row(f"{index:02d}", escape(title), f"<p>{escape(line)}</p>"))
        data = Site.bundle()
        photos = [
            row for row in Site.catalog()
            if row["id"] in {"who-speaker", "who-room"}
        ]
        seals = [row for row in Site.catalog() if row["id"] == "who-ftc"]
        lines = "".join(f"<li>{escape(line)}</li>" for line in data["who_credentials"])
        return f"""
<h1>Who it is for</h1>
<p class="lede">Five readers. The work is board training and pre-emptive cyber risk assessment.</p>
{"".join(blocks)}
{Site.row("06", escape(data["who_credentials_heading"]), f"<ul class=\"plain\">{lines}</ul>")}
{Site.row("07", escape(data["who_value_heading"]), f"<p>{Site.linked(data['who_value'])}</p>")}
{Site.pictures("who", seals, "seal-grid")}
{Site.pictures("who", photos, "photo-grid")}
"""

    @staticmethod
    def proof_body(slug: str) -> str:
        data = Site.bundle()
        return f"""
<h1>Proof</h1>
<p class="lede">{escape(data["who_credentials_heading"])}</p>
{Site.pictures(slug, Site.seal_rows(), "seal-grid")}
<ul class="plain">{"".join(f"<li>{escape(line)}</li>" for line in data["who_credentials"])}</ul>
{Site.figures()}
<h2>Our Clients</h2>
{Site.client_logo_row(slug)}
"""

    @staticmethod
    def authority_body(slug: str) -> str:
        data = Site.bundle()
        lines = []
        for line in data["government_lines"]:
            if line in {"Government Qualifications", "View our Extended Capabilities"}:
                continue
            if line.startswith("Below are the NAICS"):
                break
            lines.append(f"<li>{escape(line)}</li>")
        creds = "".join(f"<li>{escape(line)}</li>" for line in data["who_credentials"])
        return f"""
<h1>Authority</h1>
<p class="lede">{escape(data["who_credentials_heading"])}</p>
{Site.pictures(slug, Site.seal_rows(), "seal-grid")}
<ul class="plain">{creds}</ul>
<h2>Government qualifications</h2>
<ul class="plain">{"".join(lines)}</ul>
<p><a href="{Site.href(slug, "government")}">Government Quals</a></p>
<p><a href="{Site.href(slug, "recognition")}">Recognitions</a></p>
"""

    @staticmethod
    def insights_body(_slug: str) -> str:
        notes = (
            {
                "title": "Board oversight is a disclosure item",
                "body": (
                    "Regulation S-K Item 106 asks a registrant to describe its processes for "
                    "assessing, identifying, and managing material cybersecurity risks, and to "
                    "describe the board’s oversight of those risks, including any board committee "
                    "responsible for that oversight."
                ),
                "sources": (
                    (
                        "17 CFR § 229.106 (Cornell LII / eCFR text)",
                        "https://www.law.cornell.edu/cfr/text/17/229.106",
                    ),
                    (
                        "Federal Register, Aug. 4, 2023, 88 FR 51896, doc. 2023-16194",
                        "https://www.govinfo.gov/content/pkg/FR-2023-08-04/html/2023-16194.htm",
                    ),
                ),
            },
            {
                "title": "A material incident is a Form 8-K item",
                "body": (
                    "The same adopting release requires an Item 1.05 Form 8-K within four business "
                    "days after the registrant determines a cybersecurity incident is material. "
                    "The item covers nature, scope, and timing, and the impact or reasonably likely "
                    "impact. Filing may be delayed if the Attorney General determines that immediate "
                    "disclosure would pose a substantial risk to national security or public safety."
                ),
                "sources": (
                    (
                        "Federal Register, Aug. 4, 2023, 88 FR 51896, doc. 2023-16194",
                        "https://www.govinfo.gov/content/pkg/FR-2023-08-04/html/2023-16194.htm",
                    ),
                ),
            },
            {
                "title": "Govern sits beside the other enterprise risks",
                "body": (
                    "NIST Cybersecurity Framework 2.0 adds a Govern function beside Identify, Protect, "
                    "Detect, Respond, and Recover. NIST describes governance as how an organization "
                    "makes and carries out informed decisions on cybersecurity strategy, and treats "
                    "cybersecurity as a major source of enterprise risk for senior leaders to consider "
                    "alongside other enterprise risks."
                ),
                "sources": (
                    (
                        "NIST, Feb. 26, 2024, “NIST Releases Version 2.0 of Its Landmark Cybersecurity Framework”",
                        "https://www.nist.gov/news-events/news/2024/02/nist-releases-version-20-landmark-cybersecurity-framework",
                    ),
                ),
            },
        )
        blocks = []
        for index, note in enumerate(notes, start=1):
            sources = "".join(
                f'<li><a href="{escape(url)}">{escape(label)}</a></li>'
                for label, url in note["sources"]
            )
            inner = (
                f"<p>{escape(note['body'])}</p>"
                f'<ul class="sources">{sources}</ul>'
            )
            blocks.append(Site.row(f"{index:02d}", escape(note["title"]), inner))
        return f"""
<h1>Insights</h1>
<p class="lede">Short board notes. Each one is a reading of a public document.</p>
{"".join(blocks)}
"""

    @staticmethod
    def about_body(slug: str) -> str:
        data = Site.bundle()
        lines = "".join(f"<li>{escape(line)}</li>" for line in data["who_credentials"])
        logo = next(row for row in Site.catalog() if row["id"] == "mark-logo")
        return f"""
<h1>About</h1>
<p class="lede">Axon Global Services prepares board training and pre-emptive cyber risk work for the readers on Who it is for.</p>
<figure class="portrait">{Site.image(slug, logo, "12rem")}</figure>
<ul class="plain">{lines}</ul>
"""

    @staticmethod
    def engage_body(_slug: str) -> str:
        return f"""
<h1>{Site.ACTION}</h1>
<p class="lede">The briefing request opens an email.</p>
<dl class="brief">
<dt>Phone</dt>
<dd><a href="tel:+12022485050">{Site.PHONE}</a></dd>
<dt>Email</dt>
<dd><a href="mailto:{Site.EMAIL}">{Site.EMAIL}</a></dd>
<dt>Address</dt>
<dd>10 G St. NE, Suite 600<br>Washington, DC 20002</dd>
</dl>
"""

    @staticmethod
    def sitemap_body(slug: str) -> str:
        items = []
        for page in Site.PAGES:
            label = "Sitemap" if page["slug"] == "sitemap" else page["title"]
            current = ' aria-current="page"' if page["slug"] == "sitemap" else ""
            items.append(
                f'<li><a href="{Site.href(slug, page["slug"])}"{current}>{escape(label)}</a></li>'
            )
        return f"""
<h1>Sitemap</h1>
<ol class="map">{"".join(items)}</ol>
"""

    @staticmethod
    def bundle() -> dict:
        return json.loads((Site.ROOT / "content" / "pages.json").read_text(encoding="utf-8"))

    @staticmethod
    def catalog() -> list:
        data = json.loads((Site.ROOT / "content" / "assets.json").read_text(encoding="utf-8"))
        return data["assets"]

    @staticmethod
    def media_src(slug: str, filename: str) -> str:
        return f"{'' if slug == '' else '../'}assets/media/{filename}"

    @staticmethod
    def linked(text: str) -> str:
        parts = re.split(r"(https://[^\s]+)", text)
        out = []
        for part in parts:
            if part.startswith("https://"):
                href = part.rstrip(".,);")
                tail = part[len(href):]
                out.append(f'<a href="{escape(href)}">{escape(href)}</a>{escape(tail)}')
            else:
                out.append(escape(part))
        return "".join(out)

    @staticmethod
    def seal_rows() -> list:
        return [
            row for row in Site.catalog()
            if row["kind"] == "seal" and row["page"] == "https://axoncyber.com/"
        ]

    @staticmethod
    def image(slug: str, row: dict, sizes: str) -> str:
        src = Site.media_src(slug, row["file"])
        width = int(row["width"])
        small_name = Path(row["file"]).stem + "-sm.webp"
        small = Site.ROOT / "media" / small_name
        if small.exists() and width > 640:
            srcset = f'{Site.media_src(slug, small_name)} 640w, {src} {width}w'
        else:
            srcset = f"{src} {width}w"
        return (
            f'<img src="{src}" srcset="{srcset}" sizes="{sizes}" '
            f'alt="{escape(row["alt"])}" width="{width}" height="{row["height"]}">'
        )

    @staticmethod
    def pictures(slug: str, rows: list, kind: str) -> str:
        sizes = {
            "seal-grid": "(max-width: 767px) 40vw, 12rem",
            "photo-grid": "(max-width: 767px) 46vw, (max-width: 1023px) 30vw, 22rem",
            "recog-grid": "(max-width: 767px) 46vw, (max-width: 1023px) 30vw, 20rem",
        }.get(kind, "(max-width: 767px) 100vw, 40rem")
        items = [f"<li>{Site.image(slug, row, sizes)}</li>" for row in rows]
        return f'<ul class="{kind}">{"".join(items)}</ul>'

    # Recognizable wordmarks for the home band. The full list stays on /clients/.
    HOME_LOGOS = (
        "Google",
        "Microsoft",
        "Coca Cola",
        "McDonalds",
        "Walmart",
        "Target",
        "Ford",
        "Bank of America",
        "Wells Fargo",
        "Delta",
        "Dell",
        "Intel",
        "The Home Depot",
        "General Motors",
        "General Electric",
        "Capital One",
    )

    @staticmethod
    def client_logo_row(slug: str, names: tuple | None = None) -> str:
        rows = json.loads((Site.ROOT / "content" / "client-logos.json").read_text(encoding="utf-8"))
        if names:
            by_name = {row["name"]: row for row in rows}
            rows = [by_name[name] for name in names]
        items = []
        for row in rows:
            name = escape(row["name"])
            if row.get("file"):
                src = Site.media_src(slug, row["file"])
                items.append(
                    f'<li><img src="{src}" alt="{name}" width="160" height="48"></li>'
                )
            else:
                items.append(f'<li class="logo-fallback"><span>{name}</span></li>')
        return f'<ul class="logo-row">{"".join(items)}</ul>'

    @staticmethod
    def figures() -> str:
        data = Site.bundle()
        rows = (
            ("2003", data["who_credentials"][3]),
            ("over 220", data["clients_intro"][0]),
            ("over 200", data["clients_intro"][2]),
        )
        items = []
        for mark, line in rows:
            items.append(
                f'<li><p class="figure-mark">{escape(mark)}</p><p>{escape(line)}</p></li>'
            )
        return f'<ul class="figures">{"".join(items)}</ul>'

    @staticmethod
    def recognition_groups() -> list:
        rows = [row for row in Site.catalog() if row["kind"] == "recognition"]
        rows.sort(key=lambda row: row["id"])
        groups = []
        current = []
        size = 0
        for row in rows:
            if current and size + row["bytes"] > 860_000:
                groups.append(current)
                current = []
                size = 0
            current.append(row)
            size += row["bytes"]
        if current:
            groups.append(current)
        return groups

    @staticmethod
    def clients_body(slug: str) -> str:
        data = Site.bundle()
        intro = "".join(f"<p>{Site.linked(line)}</p>" for line in data["clients_intro"])
        photos = [row for row in Site.catalog() if row["id"].startswith("client-")]
        return f"""
<h1>Our Clients</h1>
{intro}
{Site.client_logo_row(slug)}
{Site.pictures(slug, photos, "photo-grid")}
"""

    @staticmethod
    def credentials_body(slug: str) -> str:
        data = Site.bundle()
        lines = "".join(f"<li>{escape(line)}</li>" for line in data["who_credentials"])
        return f"""
<h1>Credentials</h1>
<p class="lede">{escape(data["who_credentials_heading"])}</p>
{Site.pictures(slug, Site.seal_rows(), "seal-grid")}
<ul class="plain">{lines}</ul>
<p>{Site.linked(data["who_value"])}</p>
"""

    @staticmethod
    def recognition_body(slug: str) -> str:
        index = {"recognition": 0, "recognition-2": 1, "recognition-3": 2}[slug]
        groups = Site.recognition_groups()
        parts = ("recognition", "recognition-2", "recognition-3")
        links = []
        for number, part in enumerate(parts):
            label = "Recognitions" if number == 0 else f"Continued {number + 1}"
            current = ' aria-current="page"' if part == slug else ""
            links.append(f'<a href="{Site.href(slug, part)}"{current}>{label}</a>')
        lede = '<p class="lede">General Photos, Letters, and Other</p>' if index == 0 else ""
        title = "Recognitions" if index == 0 else "Recognitions, continued"
        return f"""
<h1>{title}</h1>
{lede}
{Site.pictures(slug, groups[index], "recog-grid")}
<nav class="part-nav" aria-label="Recognition pages">{"".join(links)}</nav>
"""

    @staticmethod
    def news_body(slug: str) -> str:
        posts = json.loads((Site.ROOT / "content" / "news.json").read_text(encoding="utf-8"))
        months = Site.bundle()["archive_months"]
        month_links = "".join(
            f'<a href="{escape(url)}">{escape(label)}</a>' for label, url in months
        )
        items = []
        for post in posts:
            excerpt = f"<p>{escape(post['excerpt'])}</p>" if post.get("excerpt") else ""
            items.append(
                "<li>"
                f'<a href="{escape(post["source"])}">'
                f'<time datetime="{escape(post["date"])}">{escape(post["date"])}</time>'
                f"<span>{escape(post['title'])}</span></a>"
                f"{excerpt}</li>"
            )
        return f"""
<h1>News</h1>
<p class="lede">Supporting Documentation for Axon Discourses, Awards and Recognitions</p>
<nav class="month-nav" aria-label="News archive">{month_links}</nav>
<ol class="archive">{"".join(items)}</ol>
"""

    @staticmethod
    def faq_body(_slug: str) -> str:
        data = Site.bundle()
        intro = "".join(f"<p>{escape(line)}</p>" for line in data["faq_intro"])
        questions = "".join(f"<li>{escape(line)}</li>" for line in data["faq_questions"])
        quotes = []
        for item in data["faq_quotes"]:
            note = f"<p>{escape(item['note'])}</p>" if item.get("note") else ""
            quotes.append(f"<li><p>{escape(item['quote'])}</p>{note}</li>")
        lessons = "".join(f"<li>{escape(line)}</li>" for line in data["faq_lessons"])
        lesson_intro = "".join(f"<p>{escape(line)}</p>" for line in data["faq_lessons_intro"])
        return f"""
<h1>FAQs</h1>
{intro}
<ol class="plain">{questions}</ol>
<h2>Top Quotes</h2>
<p>{escape(data["faq_disclaimer"])}</p>
<ul class="plain">{"".join(quotes)}</ul>
<h2>Top Lessons Learned</h2>
{lesson_intro}
<ul class="plain">{lessons}</ul>
"""

    @staticmethod
    def government_body(_slug: str) -> str:
        lines = Site.bundle()["government_lines"]
        quals = []
        codes = []
        note = ""
        mode = "quals"
        for line in lines:
            if line == "Government Qualifications":
                continue
            if line.startswith("Below are the NAICS"):
                mode = "codes"
                note = line
                continue
            if line == "View our Extended Capabilities":
                codes.append(
                    '<li><a href="https://axoncyber.com/extended-capabilities/">'
                    f"{escape(line)}</a></li>"
                )
                continue
            target = codes if mode == "codes" else quals
            target.append(f"<li>{escape(line)}</li>")
        return f"""
<h1>Government Quals</h1>
<ul class="plain">{"".join(quals)}</ul>
<p>{escape(note)}</p>
<ul class="plain codes">{"".join(codes)}</ul>
"""

    @staticmethod
    def fyi_body(_slug: str) -> str:
        data = Site.bundle()
        paragraph = escape(data["fyi_paragraph"])
        paragraph = paragraph.replace(
            "Morrison &amp; Foerster, LLP",
            '<a href="https://www.youtube.com/watch?v=0K6npguJuuc&amp;sns=em">Morrison &amp; Foerster, LLP</a>',
        )
        paragraph = paragraph.replace(
            "DLA Piper LLP",
            '<a href="https://www.dlapiper.com/en/uk/focus/eu-data-protection-regulation/key-changes/">DLA Piper LLP</a>',
        )
        paragraph = paragraph.replace(
            "AxonInfo@AxonCyber.com",
            '<a href="mailto:AxonInfo@AxonCyber.com">AxonInfo@AxonCyber.com</a>',
        )
        readings = []
        for item in data["fyi_readings"]:
            text = escape(item["text"])
            if item.get("href"):
                readings.append(f'<li><a href="{escape(item["href"])}">{text}</a></li>')
            else:
                readings.append(f"<li>{text}</li>")
        return f"""
<h1>FYI</h1>
<h2>{escape(data["fyi_heading"])}</h2>
<p>{paragraph}</p>
<h2>Further Reading</h2>
<ul class="plain">{"".join(readings)}</ul>
"""

    @staticmethod
    def missing_body() -> str:
        return f"""
<h1>Not found</h1>
<p class="lede">This page is not on the site.</p>
<p><a href="./">Home</a></p>
"""

    @staticmethod
    def robots() -> str:
        return (
            "User-agent: *\n"
            "Allow: /\n"
            f"Sitemap: {Site.ORIGIN}sitemap.xml\n"
        )

    @staticmethod
    def sitemap_xml() -> str:
        urls = []
        for page in Site.PAGES:
            loc = Site.canonical(page["slug"])
            urls.append(
                "  <url>\n"
                f"    <loc>{escape(loc)}</loc>\n"
                "  </url>"
            )
        body = "\n".join(urls)
        return (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"{body}\n"
            "</urlset>\n"
        )

    @staticmethod
    def favicon() -> str:
        return (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
            '<rect width="32" height="32" fill="#0e0d0b"/>'
            '<rect x="4" y="9" width="16" height="16" fill="none" stroke="#f3efe6" stroke-width="1"/>'
            '<rect x="12" y="5" width="16" height="16" fill="none" stroke="#f3efe6" stroke-width="1"/>'
            '<rect x="13" y="13" width="8" height="8" fill="#f3efe6"/>'
            "</svg>\n"
        )

    @staticmethod
    def menu_script() -> str:
        return """(function () {
  var toggle = document.querySelector(".nav-toggle");
  var groups = document.getElementById("nav-groups");
  if (!toggle || !groups) return;

  function drawer() {
    return window.getComputedStyle(toggle).display !== "none";
  }

  function panelFor(button) {
    var id = button.getAttribute("aria-controls");
    return id ? document.getElementById(id) : null;
  }

  function setTrigger(button, open) {
    button.setAttribute("aria-expanded", open ? "true" : "false");
    var panel = panelFor(button);
    if (panel) panel.hidden = !open;
    button.parentNode.classList.toggle("is-open", open);
  }

  function closeTriggers(except) {
    var buttons = groups.querySelectorAll(".menu-trigger");
    Array.prototype.forEach.call(buttons, function (button) {
      if (button !== except) setTrigger(button, false);
    });
  }

  function setDrawer(open) {
    if (!drawer()) return;
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    document.body.classList.toggle("nav-open", open);
    if (!open) closeTriggers(null);
  }

  toggle.addEventListener("click", function () {
    var open = toggle.getAttribute("aria-expanded") !== "true";
    setDrawer(open);
    if (open) {
      var first = groups.querySelector("a, button");
      if (first) first.focus();
    } else {
      toggle.focus();
    }
  });

  groups.addEventListener("click", function (event) {
    var button = event.target.closest(".menu-trigger");
    if (!button || !groups.contains(button)) return;
    var open = button.getAttribute("aria-expanded") !== "true";
    closeTriggers(button);
    setTrigger(button, open);
  });

  document.addEventListener("keydown", function (event) {
    if (event.key !== "Escape") return;
    var openTrigger = groups.querySelector('.menu-trigger[aria-expanded="true"]');
    if (openTrigger) {
      setTrigger(openTrigger, false);
      openTrigger.focus();
      return;
    }
    if (drawer() && toggle.getAttribute("aria-expanded") === "true") {
      setDrawer(false);
      toggle.focus();
    }
  });

  window.addEventListener("resize", function () {
    if (!drawer()) {
      document.body.classList.remove("nav-open");
      toggle.setAttribute("aria-expanded", "false");
      toggle.setAttribute("aria-label", "Open menu");
    }
  });
})();
"""

    @staticmethod
    def css() -> str:
        return """@font-face {
  font-family: "Libre Franklin";
  src: url("fonts/libre-franklin-latin.woff2") format("woff2");
  font-weight: 100 900;
  font-style: normal;
  font-display: swap;
}
:root {
  --ink: #0e0d0b;
  --bone: #f3efe6;
  --quiet: #5e584e;
  --quiet-dark: #b7b1a6;
  --signal: #c6a36a;
  --rule: rgba(14, 13, 11, 0.22);
  --rule-dark: rgba(243, 239, 230, 0.28);
}
* { box-sizing: border-box; }
html { background: var(--ink); }
body {
  margin: 0;
  background: var(--ink);
  color: var(--bone);
  font-family: "Libre Franklin", "Helvetica Neue", Helvetica, Arial, sans-serif;
  font-size: 1.0625rem;
  line-height: 1.5;
  font-weight: 400;
  -webkit-font-smoothing: antialiased;
}
.skip {
  position: absolute;
  left: -999px;
  top: 0;
}
.skip:focus {
  left: 1rem;
  top: 1rem;
  background: var(--bone);
  color: var(--ink);
  z-index: 3;
  min-height: 44px;
  min-width: 44px;
  display: inline-flex;
  align-items: center;
  padding: 0 0.75rem;
}
.wrap { min-height: 100vh; display: flex; flex-direction: column; }
main { flex: 1; }
.frame { width: min(76rem, calc(100% - 4rem)); margin: 0 auto; }
a {
  color: inherit;
  display: inline-block;
  min-height: 44px;
  min-width: 44px;
  max-width: 100%;
  box-sizing: border-box;
  overflow-wrap: anywhere;
  text-underline-offset: 0.22em;
}
button {
  font: inherit;
  color: inherit;
  background: transparent;
  border: 0;
  padding: 0;
  cursor: pointer;
}
a:focus-visible, button:focus-visible {
  outline: 2px solid var(--ink);
  outline-offset: 2px;
}
.mast :focus-visible,
.hero :focus-visible,
.close :focus-visible,
.colophon :focus-visible {
  outline: 2px solid var(--bone);
  outline-offset: 2px;
}
.skip:focus-visible {
  outline: 2px solid var(--ink);
  outline-offset: 2px;
}
.mast { background: var(--ink); color: var(--bone); }
.mast-top {
  display: grid;
  grid-template-columns: 1fr auto auto;
  gap: 0.75rem 1.5rem;
  align-items: center;
  min-height: 5.5rem;
  padding-top: 0.85rem;
}
.wordmark {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  min-height: 44px;
  text-decoration: none;
  color: inherit;
}
.wordmark-name {
  display: block;
  font-weight: 600;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  font-size: 0.92rem;
  line-height: 1;
  padding-bottom: 0.28rem;
  border-bottom: 1px solid currentColor;
}
.wordmark-line {
  display: block;
  margin-top: 0.3rem;
  font-weight: 450;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  font-size: 0.58rem;
  line-height: 1.2;
}
.mark { width: 2.35rem; height: 2.35rem; display: block; flex: none; }
.folio {
  margin: 0;
  font-size: 0.75rem;
  letter-spacing: 0.16em;
  color: var(--quiet-dark);
  min-width: 1.5rem;
}
.mast-action { margin: 0; }
.nav {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.15rem 0.35rem;
  border-top: 1px solid var(--rule-dark);
  padding: 0.2rem 0 0.35rem;
}
.nav-toggle { display: none; }
.nav a, .foot-nav a {
  display: inline-flex;
  align-items: center;
  min-height: 44px;
  padding: 0 0.55rem;
  text-decoration: none;
  font-size: 0.82rem;
  letter-spacing: 0.04em;
}
.nav a[aria-current="page"], .foot-nav a[aria-current="page"] {
  box-shadow: inset 0 -1px 0 currentColor;
}
.action {
  display: inline-flex;
  align-items: center;
  min-height: 44px;
  color: var(--signal);
  text-decoration: none;
  font-weight: 560;
  box-shadow: inset 0 -1px 0 var(--signal);
}
.paper .action, .page .action {
  color: var(--ink);
  box-shadow: inset 0 -1px 0 var(--signal);
}
.hero {
  min-height: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1.1rem 0 1.6rem;
  background: var(--ink);
  color: var(--bone);
}
.hero > .frame { display: flex; flex: 1; }
.hero-grid {
  flex: 1;
  display: grid;
  grid-template-columns: minmax(0, 1.25fr) minmax(12rem, 0.75fr);
  gap: 1.25rem 3rem;
  align-items: center;
}
.hero-title {
  margin: 0;
  max-width: 18ch;
  font-weight: 560;
  font-size: clamp(2rem, 2.7vw + 0.7rem, 3.45rem);
  letter-spacing: -0.038em;
  line-height: 1.02;
}
.hero-sub {
  margin: 0.9rem 0 0;
  max-width: 36rem;
  color: var(--quiet-dark);
  font-size: 1.12rem;
}
.hero-cta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.35rem 1.15rem;
  margin-top: 1.15rem;
}
.hero-cta .action {
  color: var(--ink);
  background: var(--signal);
  box-shadow: none;
  min-height: 48px;
  padding: 0.7rem 1.15rem;
  font-weight: 600;
  text-decoration: none;
}
.hero-phone {
  display: inline-flex;
  align-items: center;
  min-height: 44px;
  text-decoration: none;
  font-weight: 560;
}
.hero-photo { margin: 0; min-width: 0; }
.hero-photo img {
  display: block;
  width: 100%;
  height: auto;
  background: transparent;
}
.mark-lg { width: 100%; height: auto; max-height: min(26rem, 52vh); }
.recess { fill: var(--ink); }
.mark-lg .mass {
  animation: settle 1.2s cubic-bezier(.16, .84, .32, 1) 1 both;
}
.signal-edge { fill: var(--signal); }
@keyframes settle {
  from { transform: translate(18px, 20px); opacity: 0; }
  to { transform: none; opacity: 1; }
}
@media (prefers-reduced-motion: reduce) {
  .mark-lg .mass { animation: none; }
}
.paper { background: var(--bone); color: var(--ink); }
.paper .frame { padding-bottom: 4rem; }
.page h1 {
  margin: 0;
  padding-top: 2.75rem;
  max-width: 14ch;
  font-weight: 560;
  font-size: clamp(3.3rem, 7vw, 5.8rem);
  letter-spacing: -0.046em;
  line-height: 0.9;
  border: 0;
}
.lede { max-width: 38rem; margin: 1.35rem 0 2.25rem; font-size: 1.15rem; }
.row {
  display: grid;
  grid-template-columns: 4.25rem minmax(0, 1fr);
  gap: 0.5rem 1.75rem;
  padding: 2.1rem 0;
  border-top: 1px solid var(--ink);
}
.num {
  margin: 0.35rem 0 0;
  font-size: 0.78rem;
  letter-spacing: 0.14em;
  font-weight: 500;
}
.row h2 {
  margin: 0 0 0.7rem;
  font-size: clamp(1.45rem, 2.2vw, 2rem);
  font-weight: 560;
  letter-spacing: -0.03em;
  line-height: 1.12;
  text-transform: none;
}
p { margin: 0 0 0.75rem; }
.quiet { color: var(--quiet); font-size: 0.92rem; }
.colophon .quiet { color: var(--quiet-dark); }
.strip, .cards, .slots, .sources, .map, .brief {
  list-style: none;
  margin: 0;
  padding: 0;
}
.strip, .cards {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  border-top: 1px solid var(--ink);
  border-left: 1px solid var(--ink);
  margin-top: 0.4rem;
}
.strip li, .card {
  margin: 0;
  min-height: 13.5rem;
  padding: 1.25rem 1.15rem 1.35rem;
  border-right: 1px solid var(--ink);
  border-bottom: 1px solid var(--ink);
  display: flex;
  flex-direction: column;
}
.card .idx {
  margin: 0 0 auto;
  font-size: 1.85rem;
  font-weight: 500;
  letter-spacing: -0.04em;
  color: var(--quiet);
}
.card h3 {
  margin: 1.4rem 0 0.45rem;
  font-size: 1.22rem;
  font-weight: 560;
  letter-spacing: -0.02em;
  line-height: 1.2;
}
.card h3 a { text-decoration: none; }
.card p, .strip li p { margin: 0; }
.offerings {
  list-style: none;
  margin: 0.4rem 0 0;
  padding: 0;
  display: grid;
  grid-template-columns: 1fr 1fr;
  border-top: 1px solid var(--ink);
  border-left: 1px solid var(--ink);
}
.offering {
  min-height: 18.5rem;
  padding: 1.35rem 1.35rem 1.55rem;
  border-right: 1px solid var(--ink);
  border-bottom: 1px solid var(--ink);
  display: flex;
  flex-direction: column;
}
.offering .idx {
  margin: 0 0 auto;
  font-size: 3.4rem;
  font-weight: 500;
  letter-spacing: -0.05em;
  line-height: 0.9;
  color: var(--quiet);
}
.offering h2 {
  margin: 1.75rem 0 0.55rem;
  font-size: 1.5rem;
  font-weight: 560;
  letter-spacing: -0.03em;
  line-height: 1.15;
  text-transform: none;
}
.offering p { margin: 0; max-width: 36rem; }
.slot {
  margin: 0 0 0.4rem;
  font-size: 0.95rem;
  font-weight: 560;
  letter-spacing: 0.18em;
  text-transform: uppercase;
}
.slots {
  display: grid;
  grid-template-columns: 1fr 1fr;
  border-top: 1px solid var(--ink);
  border-left: 1px solid var(--ink);
  margin-top: 0.5rem;
}
.slots li {
  min-height: 10rem;
  padding: 1.2rem 1.1rem 1.3rem;
  border-right: 1px solid var(--ink);
  border-bottom: 1px solid var(--ink);
}
.slot-page {
  margin-top: 1.5rem;
  min-height: 18rem;
  border: 1px solid var(--ink);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}
.sources li { margin: 0.15rem 0; }
.table-wrap { overflow-x: auto; max-width: 100%; }
table { width: 100%; border-collapse: collapse; font-size: 0.95rem; }
caption {
  caption-side: bottom;
  text-align: left;
  color: var(--quiet);
  font-size: 0.85rem;
  padding: 0.7rem 0;
}
th, td {
  text-align: left;
  vertical-align: top;
  padding: 0.35rem 0.8rem 0.35rem 0;
  border-bottom: 1px solid var(--rule);
  font-weight: 400;
}
th {
  font-size: 0.72rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  padding-top: 0.8rem;
}
.brief {
  display: grid;
  grid-template-columns: 8rem minmax(0, 1fr);
  gap: 0.35rem 1.25rem;
  margin: 0;
}
.brief dt {
  margin: 0;
  padding-top: 0.7rem;
  font-size: 0.72rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}
.brief dd { margin: 0; }
.end-action { margin: 2.4rem 0 0.5rem; }
.map { margin-top: 1.5rem; }
.map li { border-top: 1px solid var(--rule); }
.map a {
  display: flex;
  align-items: center;
  width: 100%;
  min-height: 52px;
  text-decoration: none;
  font-size: 1.45rem;
  font-weight: 520;
  letter-spacing: -0.03em;
}
.colophon {
  background: var(--ink);
  color: var(--bone);
}
.foot {
  display: grid;
  grid-template-columns: 1.3fr 1fr 1fr;
  gap: 1.5rem 2rem;
  padding: 3rem 0 1.4rem;
}
.foot-nav { display: flex; flex-direction: column; align-items: flex-start; }
.foot-side p { margin: 0; }
.foot-action { margin-top: 0.6rem; }
.foot-legal {
  grid-column: 1 / -1;
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  border-top: 1px solid var(--rule-dark);
  padding-top: 0.85rem;
  color: var(--quiet-dark);
  font-size: 0.85rem;
}
.foot-legal p { margin: 0; }
.foot-legal a, .foot-side a, .colophon .wordmark { color: var(--bone); }
.credential-strip { padding-top: 2.4rem; }
.credential-strip h2 {
  margin: 0 0 0.8rem;
  font-size: clamp(1.45rem, 2.2vw, 2rem);
  font-weight: 560;
  letter-spacing: -0.03em;
}
.seal-grid, .photo-grid, .recog-grid, .name-wall, .plain {
  list-style: none;
  margin: 0.6rem 0 1.4rem;
  padding: 0;
}
.seal-grid, .photo-grid, .recog-grid, .name-wall {
  display: grid;
  border-top: 1px solid var(--ink);
  border-left: 1px solid var(--ink);
}
.seal-grid { grid-template-columns: repeat(4, minmax(0, 1fr)); }
.photo-grid, .recog-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }
.name-wall { grid-template-columns: repeat(3, minmax(0, 1fr)); }
.seal-grid li, .photo-grid li, .recog-grid li, .name-wall li {
  margin: 0;
  min-height: 8.75rem;
  padding: 1rem;
  border-right: 1px solid var(--ink);
  border-bottom: 1px solid var(--ink);
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bone);
}
.name-wall li {
  justify-content: flex-start;
  font-weight: 560;
  letter-spacing: -0.02em;
  line-height: 1.25;
}
.seal-grid img, .photo-grid img, .recog-grid img {
  display: block;
  width: 100%;
  height: 8.75rem;
  object-fit: contain;
}
.photo-grid li, .recog-grid li { background: var(--ink); }
.photo-grid img, .recog-grid img { height: 12rem; }
.portrait { margin: 0 0 1.4rem; max-width: 22rem; }
.portrait img { display: block; width: 100%; height: auto; }
.logo-row {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  list-style: none;
  margin: 0.6rem 0 1.4rem;
  padding: 0;
  background: transparent;
}
.logo-row li {
  box-sizing: border-box;
  width: 160px;
  max-width: 160px;
  height: 48px;
  min-height: 48px;
  margin: 0;
  padding: 0 0.45rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: 1px solid var(--ink);
}
.logo-row img {
  display: block;
  width: auto;
  height: 48px;
  max-width: 148px;
  max-height: 48px;
  object-fit: contain;
  background: transparent;
}
.logo-row .logo-fallback {
  padding: 0 0.3rem;
  font-weight: 560;
  font-size: 0.68rem;
  letter-spacing: -0.02em;
  line-height: 1.05;
  text-align: center;
  overflow: hidden;
}
.logo-more { margin: -0.2rem 0 1.2rem; }
.logo-more a { font-weight: 560; text-decoration: none; }
.plain li { margin: 0; padding: 0.85rem 0; border-top: 1px solid var(--rule); }
.month-nav, .part-nav { display: flex; flex-wrap: wrap; gap: 0.2rem 0.35rem; margin: 0 0 1.4rem; }
.month-nav a, .part-nav a {
  display: inline-flex;
  align-items: center;
  min-height: 44px;
  padding: 0 0.55rem;
  text-decoration: none;
}
.archive { list-style: none; margin: 0; padding: 0; }
.archive li { border-top: 1px solid var(--rule); padding: 0.35rem 0 0.8rem; }
.archive a {
  display: flex;
  align-items: baseline;
  gap: 1rem;
  min-height: 44px;
  text-decoration: none;
  font-weight: 520;
}
.archive time { flex: none; color: var(--quiet); font-size: 0.85rem; }
.archive p { margin: 0.15rem 0 0; color: var(--quiet); }
.opening main { display: flex; flex-direction: column; }
.opening .hero { flex: 1; min-height: 0; }
@media (max-width: 800px) {
  .frame { width: min(76rem, calc(100% - 1.5rem)); }
  .mast-top { grid-template-columns: 1fr auto; min-height: 0; padding-top: 0.35rem; }
  .hero { min-height: 0; padding: 0.35rem 0 1.25rem; }
  .hero-grid { grid-template-columns: 1fr; gap: 0.85rem; }
  .hero-title { font-size: clamp(1.7rem, 6.4vw, 2.15rem); max-width: 22ch; }
  .hero-sub { margin-top: 0.55rem; font-size: 1rem; }
  .hero-cta { margin-top: 0.75rem; }
  .hero-grid { align-content: start; }
  .hero-photo { margin-top: 0.35rem; }
  .offerings { grid-template-columns: 1fr; }
  .offering { min-height: 0; }
  .page h1 { max-width: none; font-size: clamp(2.7rem, 12vw, 3.5rem); padding-top: 1.7rem; }
  .row { grid-template-columns: 1fr; gap: 0.25rem; padding: 1.5rem 0; }
  .strip, .cards, .slots { grid-template-columns: 1fr; }
  .strip li, .card, .slots li { min-height: 0; }
  .brief { grid-template-columns: 1fr; }
  .foot { grid-template-columns: 1fr; padding-top: 2.2rem; }
  .foot-legal { flex-direction: column; }
  .seal-grid, .photo-grid, .recog-grid, .name-wall { grid-template-columns: 1fr 1fr; }
  .seal-grid li { min-height: 9rem; }
  .seal-grid img { width: 6.25rem; height: 6.25rem; }
  .name-wall { grid-template-columns: 1fr 1fr; }
  .archive a { flex-direction: column; gap: 0.15rem; align-items: flex-start; }
  .close-grid { grid-template-columns: 1fr; align-items: start; padding: 2.2rem 0 2.4rem; }
  .cards, .figures, .offerings { grid-template-columns: 1fr; }
  .folio, .mast-action { display: none; }
}
body {
  font-size: clamp(1rem, 0.94rem + 0.22vw, 1.125rem);
  padding-left: env(safe-area-inset-left);
  padding-right: env(safe-area-inset-right);
  overflow-x: clip;
}
.mast { padding-top: env(safe-area-inset-top); }
.colophon { padding-bottom: env(safe-area-inset-bottom); }
.logo { width: 3rem; height: auto; max-width: 3rem; display: block; object-fit: cover; }
.nav { display: flex; position: relative; }
.nav-groups { display: flex; flex-wrap: wrap; align-items: center; gap: 0 0.1rem; }
.nav-bars, .nav-bars::before, .nav-bars::after {
  display: block;
  width: 18px;
  height: 2px;
  background: currentColor;
  position: relative;
  transition: transform 160ms ease, top 160ms ease, background-color 160ms ease;
}
.nav-bars::before, .nav-bars::after { content: ""; position: absolute; left: 0; }
.nav-bars::before { top: -6px; }
.nav-bars::after { top: 6px; }
.nav-toggle[aria-expanded="true"] .nav-bars { background: transparent; }
.nav-toggle[aria-expanded="true"] .nav-bars::before { top: 0; transform: rotate(45deg); }
.nav-toggle[aria-expanded="true"] .nav-bars::after { top: 0; transform: rotate(-45deg); }
.menu-trigger, a.menu-label, .menu-panel a {
  display: flex;
  align-items: center;
  min-height: 44px;
  min-width: 44px;
  padding: 0 0.7rem;
  text-decoration: none;
  text-align: left;
  font-size: 0.92rem;
  cursor: pointer;
}
.menu-trigger::after {
  content: "";
  width: 0.38rem;
  height: 0.38rem;
  margin-left: 0.45rem;
  border-right: 1px solid currentColor;
  border-bottom: 1px solid currentColor;
  transform: translateY(-0.12rem) rotate(45deg);
  transition: transform 160ms ease;
}
.menu.is-open > .menu-trigger::after { transform: translateY(0.08rem) rotate(225deg); }
.menu.here > .menu-trigger, a.menu-label[aria-current="page"] { box-shadow: inset 0 -1px 0 currentColor; }
.menu-panel[hidden] { display: none !important; }
.menu.is-open > .menu-panel { display: flex; flex-direction: column; }
.menu-panel a { width: 100%; }
.page h1 { font-size: clamp(2.75rem, 4.2vw + 1.1rem, 5.75rem); }
.lede { font-size: clamp(1.12rem, 0.4vw + 1rem, 1.38rem); max-width: 40rem; }
.eyebrow {
  margin: 0 0 0.8rem;
  font-size: 0.72rem;
  letter-spacing: 0.16em;
  text-transform: uppercase;
}
.trust { padding: 1.45rem 0 0.2rem; }
.trust-line { max-width: 46rem; margin: 0.15rem 0 0; }
.proofband, .services { margin-top: 2.6rem; }
.proofband h2, .services h2 {
  margin: 0 0 0.9rem;
  font-size: clamp(1.7rem, 1.2vw + 1.2rem, 2.35rem);
  font-weight: 560;
  letter-spacing: -0.03em;
}
.seal-grid li { min-height: 11.5rem; }
.seal-grid img { width: 8.5rem; height: 8.5rem; max-width: 86%; object-fit: contain; }
.name-wall { grid-template-columns: repeat(4, minmax(0, 1fr)); }
.name-wall li {
  min-height: 4.25rem;
  padding: 0.55rem 0.7rem;
  justify-content: center;
  text-align: center;
  font-size: clamp(0.82rem, 0.3vw + 0.74rem, 0.98rem);
  font-weight: 560;
  letter-spacing: -0.02em;
  line-height: 1.2;
}
.figures {
  list-style: none;
  margin: 1.35rem 0 0;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  border-top: 1px solid var(--ink);
  border-left: 1px solid var(--ink);
}
.figures li {
  margin: 0;
  padding: 1.15rem 1.05rem 1.25rem;
  border-right: 1px solid var(--ink);
  border-bottom: 1px solid var(--ink);
}
.figure-mark {
  margin: 0 0 0.5rem;
  font-size: clamp(1.85rem, 1.4vw + 1rem, 2.7rem);
  font-weight: 560;
  letter-spacing: -0.045em;
  line-height: 0.95;
}
.card, .offering { padding: 0; overflow: hidden; }
.card-plate { height: 7.25rem; background: var(--ink); }
.card-plate svg { display: block; width: 100%; height: 100%; }
.card-body, .offering-body { display: flex; flex-direction: column; flex: 1; padding: 1.15rem 1.15rem 1.35rem; }
.card .idx { margin: 0 0 0.85rem; }
.card h3 { margin: 0 0 0.4rem; }
.offering .idx { margin: 0 0 1rem; font-size: 2.4rem; }
.offering h2 { margin: 0 0 0.5rem; }
.close { background: var(--ink); color: var(--bone); border-top: 1px solid var(--rule-dark); }
.close-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 1.25rem 2rem;
  align-items: end;
  padding: 3rem 0 3.2rem;
}
.close h2 {
  margin: 0.15rem 0 0.55rem;
  max-width: 16ch;
  font-size: clamp(2rem, 3vw + 1rem, 3.35rem);
  font-weight: 560;
  letter-spacing: -0.04em;
  line-height: 0.95;
}
.close p { margin: 0; max-width: 36rem; }
.close .action {
  color: var(--ink);
  background: var(--signal);
  box-shadow: none;
  min-height: 48px;
  padding: 0.7rem 1.15rem;
  font-weight: 600;
  text-decoration: none;
}
.foot-nav { display: grid; grid-template-columns: 1fr 1fr; gap: 0.35rem 1.2rem; }
.foot-group { display: flex; flex-direction: column; align-items: flex-start; }
.foot-group a { text-decoration: none; }
@media (min-width: 1024px) {
  .menu { position: relative; }
  .menu.is-open > .menu-panel {
    position: absolute;
    z-index: 8;
    top: 100%;
    left: 0;
    min-width: 15.5rem;
    background: var(--ink);
    border: 1px solid var(--rule-dark);
    padding: 0.3rem 0;
    box-shadow: none;
  }
  .menu-end.is-open > .menu-panel { left: auto; right: 0; }
}
@media (max-width: 1100px) {
  .cards, .figures { grid-template-columns: 1fr 1fr; }
  .name-wall { grid-template-columns: repeat(3, minmax(0, 1fr)); }
}
@media (max-width: 1023px) {
  .hero-grid { align-items: start; }
  .hero-title { font-size: clamp(1.85rem, 3.2vw, 2.45rem); }
  .mark-lg { max-height: min(16rem, 34vh); }
  .mast .frame { position: relative; }
  .folio, .mast-action { display: none; }
  .nav {
    position: absolute;
    top: 0.35rem;
    right: 0;
    width: 44px;
    min-height: 44px;
    border-top: 0;
    padding: 0;
    z-index: 4;
  }
  .nav-toggle {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 44px;
    height: 44px;
  }
  .nav-groups {
    display: none;
    position: absolute;
    top: 44px;
    right: 0;
    width: min(22rem, calc(100vw - 1.5rem));
    background: var(--ink);
    border: 1px solid var(--rule-dark);
    padding: 0.2rem 0;
  }
  body.nav-open { overflow: hidden; }
  body.nav-open .nav-groups {
    display: flex;
    flex-direction: column;
    align-items: stretch;
  }
  .menu-trigger, a.menu-label, .menu-panel a { min-height: 56px; }
  .menu.is-open > .menu-panel {
    position: static;
    min-width: 0;
    background: transparent;
    border: 0;
    padding: 0 0 0.15rem 0.75rem;
  }
  .cards, .figures, .offerings { grid-template-columns: 1fr; }
  .name-wall { grid-template-columns: 1fr 1fr; }
  .close-grid { grid-template-columns: 1fr; align-items: start; }
  .seal-grid li { min-height: 9rem; }
  .seal-grid img { width: 6.25rem; height: 6.25rem; }
}
p, h1, h2, h3, li, dd {
  overflow-wrap: anywhere;
}
@media (max-width: 700px) {
  .logo-row li { height: 40px; min-height: 40px; }
  .logo-row img { height: 40px; max-height: 40px; }
}
@media (max-width: 390px) {
  .frame { width: min(76rem, calc(100% - 1.25rem)); }
  .wordmark-name { letter-spacing: 0.12em; }
  .wordmark-line { letter-spacing: 0.1em; }
}
@media (prefers-reduced-motion: reduce) {
  .mark-lg .mass,
  .nav-bars, .nav-bars::before, .nav-bars::after,
  .menu-trigger::after {
    animation: none;
    transition: none;
  }
}
"""

    @staticmethod
    def audit() -> list[str]:
        problems = []
        html_files = sorted(Site.OUT.rglob("*.html"))
        if len(html_files) < 9:
            problems.append(f"expected at least 9 html files, found {len(html_files)}")
        blob_parts = []
        nacd_files = []
        for path in html_files:
            text = path.read_text(encoding="utf-8")
            blob_parts.append(text)
            lowered = text.casefold()
            if "<form" in lowered:
                problems.append(f"form in {path.name}")
            if Site.ACTION not in text:
                problems.append(f"missing action in {path}")
            if "content-security-policy" not in lowered:
                problems.append(f"missing csp in {path}")
            if 'name="referrer" content="no-referrer"' not in text:
                problems.append(f"missing referrer policy in {path}")
            scripts = re.findall(r"<script\b([^>]*)>", text, re.I)
            expected = ' src="' + ("../" if path.parent != Site.OUT else "") + 'assets/menu.js"'
            rel = str(path.relative_to(Site.OUT))
            if scripts != [expected]:
                problems.append(f"unexpected script in {rel}")
            if re.search(r"<script\b[^>]*>\s*[^<\s]", text, re.I):
                problems.append(f"inline script in {rel}")
            if "NACD" in text:
                nacd_files.append(str(path.relative_to(Site.OUT)))
            for phrase in Site.BANNED:
                if phrase in lowered:
                    problems.append(f"banned phrase {phrase!r} in {path}")
        if "capabilities/index.html" not in nacd_files:
            problems.append(f"NACD missing from capabilities: {nacd_files}")
        caps = (Site.OUT / "capabilities" / "index.html").read_text(encoding="utf-8")
        if caps.count("By NACD® credentialed experts") != 1:
            problems.append("NACD credential line is missing")
        if "NACD-credentialed" in caps:
            problems.append("old NACD-credentialed wording remains")
        if re.search(r"<h[1-6][^>]*>[^<]*NACD", caps):
            problems.append("NACD appears in a heading")
        blob = "\n".join(blob_parts).casefold()
        for page in Site.PAGES:
            if page["nav"] and page["nav"].casefold() not in blob:
                problems.append(f"missing nav label {page['nav']}")
        if (Site.ROOT / "CNAME").exists() or (Site.OUT / "CNAME").exists():
            problems.append("CNAME present")
        home = (Site.OUT / "index.html").read_text(encoding="utf-8")
        for needle in (
            "We train boards and general counsel on cyber risk, and deliver a written risk report before a breach.",
            "Training on site or by webinar, and assessments explained in plain business language.",
            "Services",
            Site.ACTION,
            Site.PHONE,
        ):
            if needle not in home:
                problems.append(f"home missing {needle}")
        if "Board brief" in home or ">Buyer<" in home or ">Deliverable<" in home:
            problems.append("old hero copy remains")
        if 'aria-label="Open menu"' not in home or "<button" not in home:
            problems.append("menu toggle is not a labeled button")
        if "checkbox" in home:
            problems.append("menu still uses a checkbox")
        if home.count('class="card"') != 6:
            problems.append("home card count is not 6")
        if "gtag" in blob or "google-analytics" in blob or "plausible" in blob:
            problems.append("analytics marker")
        for offer in Site.OFFERINGS:
            if escape(offer["name"]) not in caps:
                problems.append(f"missing offering {offer['name']}")
        if Site.SOURCE in caps or "Source map" in caps:
            problems.append("capabilities still prints a source map")
        if ">Slot<" in blob or ">Secondary<" in "\n".join(blob_parts):
            problems.append("internal note remains in the html")
        if len(Site.MENU) != 6:
            problems.append("menu is not six items")
        proof = (Site.OUT / "proof" / "index.html").read_text(encoding="utf-8")
        if ">Slot<" in proof or "over 220" not in proof:
            problems.append("proof is missing the live figures")
        authority = (Site.OUT / "authority" / "index.html").read_text(encoding="utf-8")
        if ">Slot<" in authority or "Government qualifications" not in authority:
            problems.append("authority is missing the live qualifications")
        about = (Site.OUT / "about" / "index.html").read_text(encoding="utf-8")
        if "Slot" in about or "mark-logo.webp" not in about:
            problems.append("about is missing the logo")
        if "viewport-fit=cover" not in home or "mark-logo.webp" not in home:
            problems.append("home logo or viewport-fit missing")
        if "Recognized by" not in home:
            problems.append("home is missing the recognition band")
        if len(Site.recognition_groups()) != 3:
            problems.append("recognition archive is not split into 3 pages")
        css = (Site.OUT / "assets" / "site.css").read_text(encoding="utf-8")
        if re.search(r"url\(\s*https?:", css):
            problems.append("stylesheet requests a third party")
        if "@keyframes drift" in css or "animation: drift" in css:
            problems.append("client row still animates")
        if re.search(r"grayscale|sepia|mix-blend-mode|duotone", css):
            problems.append("image color treatment remains")
        if "max-width: 160px" not in css or "height: 48px" not in css:
            problems.append("logo box size missing")
        if "outline: 2px solid var(--ink)" not in css or "outline: 2px solid var(--bone)" not in css:
            problems.append("focus rings missing")
        if "outline-offset: 2px" not in css:
            problems.append("focus offset missing")
        faq = (Site.OUT / "faq" / "index.html").read_text(encoding="utf-8")
        fyi = (Site.OUT / "fyi" / "index.html").read_text(encoding="utf-8")
        news = (Site.OUT / "news" / "index.html").read_text(encoding="utf-8")
        if "safe harbor" not in faq:
            problems.append("faq missing safe harbor")
        if "safe haven" not in fyi:
            problems.append("fyi missing safe haven")
        if "[poop]" in faq or "[fill in the blank]" in faq or "[ELT]" in faq or "[bad actors]" in faq:
            problems.append("faq still has editorial brackets")
        if "Would it stand up to review by your board, your regulator, or a court?" not in faq:
            problems.append("faq review question missing")
        if "Generals Counsel" not in faq or "Conducted" not in home:
            problems.append("source wording drifted")
        if re.search(r"\[\d+\]", news):
            problems.append("news still has citation marks")
        repo_text = "\n".join(
            path.read_text(encoding="utf-8", errors="ignore")
            for path in Site.ROOT.rglob("*")
            if path.is_file()
            and path.suffix in {".py", ".md", ".html", ".css", ".yml", ".txt", ".svg"}
            and "fonts" not in path.parts
            and Site.REPORTS not in path.parents
            and ".git" not in path.parts
        ).casefold()
        for phrase in ("golden" + "-ratio", "gregs" + "-hvac"):
            if phrase in repo_text or phrase in blob:
                problems.append(f"{phrase} still mentioned")
        return problems

    @staticmethod
    def header_scan() -> dict:
        pages = []
        meta_re = re.compile(r"<meta\s+([^>]+)>", re.I)
        attr_re = re.compile(r'([:\w-]+)\s*=\s*"([^"]*)"')
        for path in sorted(Site.OUT.rglob("*.html")):
            text = path.read_text(encoding="utf-8")
            metas = []
            for match in meta_re.finditer(text):
                attrs = dict(attr_re.findall(match.group(1)))
                metas.append(attrs)
            pages.append(
                {
                    "path": str(path.relative_to(Site.OUT)),
                    "meta": metas,
                    "forms": len(re.findall(r"<form\b", text, re.I)),
                    "scripts": len(re.findall(r"<script\b", text, re.I)),
                    "external_urls": sorted(set(re.findall(r"https?://[^\"'\s>]+", text))),
                }
            )
        return {
            "method": "Static scan of built HTML. These are document policies, not HTTP response headers.",
            "limitation": (
                "GitHub Pages cannot set custom HTTP response headers. "
                "This site does not add meta tags that impersonate headers browsers ignore. "
                "The document policies that are actually available are the meta content-security policy "
                "and the meta referrer policy."
            ),
            "https": (
                "github.io Pages sites are served over HTTPS. This repo ships no CNAME, "
                "so the host stays a github.io name, where GitHub enforces HTTPS."
            ),
            "set_in_html": [
                "Content-Security-Policy via meta http-equiv",
                "referrer policy via meta name=referrer (no-referrer)",
            ],
            "github_pages_cannot_set": [
                "Custom HTTP response headers. Pages has no header config for a repository.",
                "Content-Security-Policy as an HTTP header. The meta element is the available control. Meta CSP ignores frame-ancestors, sandbox, report-uri, and report-to.",
                "Referrer-Policy as an HTTP header. The meta referrer element is the available control.",
                "X-Frame-Options, X-Content-Type-Options, and Permissions-Policy.",
                "Cross-Origin-Opener-Policy, Cross-Origin-Resource-Policy, and Cross-Origin-Embedder-Policy.",
                "A custom HSTS policy. On github.io, GitHub sends its own strict-transport-security.",
            ],
            "pages": pages,
        }

    @staticmethod
    def weights() -> dict:
        css = (Site.OUT / "assets" / "site.css").stat().st_size
        font = (Site.OUT / "assets" / "fonts" / "libre-franklin-latin.woff2").stat().st_size
        js = (Site.OUT / "assets" / "menu.js").stat().st_size
        limit = 1_048_576
        rows = []
        for path in sorted(Site.OUT.rglob("*.html")):
            text = path.read_text(encoding="utf-8")
            html_bytes = path.stat().st_size
            seen = set()
            image_bytes = 0
            for icon_name in ("favicon.png", "apple-touch-icon.png"):
                icon = (Site.OUT / icon_name).resolve()
                if icon.is_file() and icon not in seen:
                    seen.add(icon)
                    image_bytes += icon.stat().st_size
            for tag in re.findall(r"<img\b[^>]*>", text):
                urls = []
                src = re.search(r'\bsrc="([^"]+)"', tag)
                if src:
                    urls.append(src.group(1))
                srcset = re.search(r'\bsrcset="([^"]+)"', tag)
                if srcset:
                    urls.extend(part.strip().split()[0] for part in srcset.group(1).split(","))
                best = None
                best_size = -1
                for url in urls:
                    if url.startswith(("http:", "https:", "data:")):
                        continue
                    image = (path.parent / url).resolve()
                    if image.is_file() and image.stat().st_size > best_size:
                        best = image
                        best_size = image.stat().st_size
                if best is not None and best not in seen:
                    seen.add(best)
                    image_bytes += best_size
            total = html_bytes + css + font + image_bytes + js
            rows.append(
                {
                    "path": str(path.relative_to(Site.OUT)),
                    "html_bytes": html_bytes,
                    "css_bytes": css,
                    "font_bytes": font,
                    "image_bytes": image_bytes,
                    "js_bytes": js,
                    "total_bytes": total,
                    "limit_bytes": limit,
                    "under_limit": total < limit,
                }
            )
        return {
            "method": "Uncompressed bytes of the HTML file plus the shared stylesheet, the menu script, the self-hosted font, the favicon, and the largest image candidate referenced by each img element.",
            "limit_bytes": limit,
            "pages": rows,
        }


if __name__ == "__main__":
    raise SystemExit(Site.build())
