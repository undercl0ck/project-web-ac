"""Axon Global Services static site.

One class. Static methods. Plain HTML, one stylesheet, one menu script, one self-hosted grotesque.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass, fields, is_dataclass
from datetime import date
from html import escape
from pathlib import Path
from urllib.parse import urlsplit


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
        {"slug": "recognition-2", "nav": None, "title": "Recognitions (2 of 3)"},
        {"slug": "recognition-3", "nav": None, "title": "Recognitions (3 of 3)"},
        {"slug": "news", "nav": "News", "title": "News"},
        {"slug": "faq", "nav": "FAQs", "title": "FAQs"},
        {"slug": "government", "nav": "Government Quals", "title": "Government Quals"},
        {"slug": "fyi", "nav": "FYI", "title": "FYI"},
        {"slug": "proof", "nav": "Proof", "title": "Proof"},
        {"slug": "authority", "nav": "Authority", "title": "Authority"},
        {"slug": "insights", "nav": "Insights", "title": "Insights"},
        {"slug": "about", "nav": "About", "title": "About"},
        {"slug": "engage", "nav": "Engage", "title": "Engage"},
        {"slug": "extended-capabilities", "nav": None, "title": "Extended Capabilities"},
        {"slug": "how-we-engage", "nav": None, "title": "How We Engage"},
        {"slug": "our-ceo", "nav": None, "title": "Our CEO & Global CTO"},
        {"slug": "sitemap", "nav": None, "title": "Sitemap"},
    )

    REDIRECTS = {
        "our-ceo": ("about", "#leadership"),
        "faqs": ("faq", ""),
        "contact": ("engage", ""),
    }
    NOINDEX_SLUGS = frozenset({"faqs", "contact"})

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
            "audience": "For board members and C-suite executives.",
            "receive": "You receive cyber risk training for your board or executive team, on site or by webinar.",
            "home": True,
            "body": (
                "Designed for Board members or C-Suite executives (on site or via Webinar). "
                "By NACD® credentialed experts."
            ),
        },
        {
            "id": "board-view",
            "name": "Board View Cyber Risk Assessment",
            "card": "Board View Cyber Risk Assessment",
            "card_line": "A third-party report of material threats, written for the board.",
            "audience": "For boards and their committees.",
            "receive": "You receive a third-party report on material cyber threats you did not know about.",
            "home": True,
            "body": (
                "A third-party report identifying material cyber threats previously "
                "unknown to your organization based on NACD ® and World Economic Forum ® "
                "and Global D&O ISAO © Cyber Risk Recommendations for Boards."
            ),
        },
        {
            "id": "ma",
            "name": "M&A Risk Assessment",
            "card": "M&A Risk Assessment",
            "card_line": "A report on whether a company being acquired is already compromised.",
            "audience": "For deal teams, general counsel and private equity.",
            "receive": "You receive a report on whether a target company is already compromised or breached.",
            "home": True,
            "body": (
                "a report detailing whether a target company is compromised or breached "
                "(e.g. identifying if i.p. has been stolen)."
            ),
        },
        {
            "id": "supply",
            "name": "Supply Chain Risk Assessment",
            "card": "Supply Chain Risk Assessment",
            "card_line": "A report on which suppliers present a cyber risk.",
            "audience": "For general counsel, security leaders and procurement.",
            "receive": "You receive a report on which suppliers present a cyber risk to your organization.",
            "home": True,
            "body": (
                "A report identifying which suppliers are infecting your organization "
                "and if they present a cyber risk."
            ),
        },
        {
            "id": "program",
            "name": "Cybersecurity Program Assessment",
            "card": "Cybersecurity Program Assessment",
            "card_line": "A report of gaps between the program and current threats.",
            "audience": "For executive teams and security leaders.",
            "receive": "You receive a third-party report on gaps between your program and current threats.",
            "home": True,
            "body": (
                "An expedient third-party report identifying gaps between current "
                "programs versus current threats."
            ),
        },
        {
            "id": "external",
            "name": "External Security Posture Assessment",
            "card": "External Security Posture Assessment",
            "card_line": "What is visible from outside, including a dark-web and deep-net search.",
            "audience": "For boards, general counsel and security leaders.",
            "receive": "You receive a report on what outsiders can see, including a dark-web and deep-net search.",
            "home": True,
            "body": (
                'A report detailing what bad actors can see from the "outside-in" '
                "(includes dark-web, deep-net search for compromises)."
            ),
        },
        {
            "id": "internal",
            "name": "Internal Security Posture Assessment",
            "card": "Internal Security Posture Assessment",
            "card_line": "",
            "audience": "For security leaders and executive teams.",
            "receive": "You receive a secure third-party log review for espionage and unsignatured threats.",
            "home": False,
            "body": (
                "A third-party, secure, and expedient review of logs identifying "
                "espionage and other unsignatured threats."
            ),
        },
        {
            "id": "proactive",
            "name": "Cyber Proactive Defense®",
            "card": "Cyber Proactive Defense",
            "card_line": "",
            "audience": "For general counsel and security leaders who need to act on a finding.",
            "receive": "You receive discrete services, within U.S. and/or international law, that stop the attack.",
            "home": False,
            "body": (
                "Discrete services performed within the U.S. and/or international law "
                "that stop the attack or eliminate liability. "
                "We then offer a strategy for Axon to neutralize these threats "
                "within U.S. and/or international law."
            ),
        },
    )

    # Home shows the first six. Capabilities uses that order, then Internal and Defense.
    HOME_ORDER = ("training", "board-view", "supply", "ma", "external", "program")
    CAP_ORDER = HOME_ORDER + ("internal", "proactive")
    # Short label drawn on the card. Each word is contained in that service's full name.
    WORDS = {
        "training": "Training",
        "board-view": "Board",
        "supply": "Supply",
        "ma": "M&A",
        "external": "External",
        "program": "Program",
        "internal": "Internal",
        "proactive": "Defense",
    }

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
        for src in sorted((Site.ROOT / "media").glob("seal-*.svg")):
            (media_out / src.name).write_bytes(src.read_bytes())
        bimi_src = Site.ROOT / "bimi" / "axon-bimi.svg"
        bimi_out = Site.OUT / "bimi"
        bimi_out.mkdir(parents=True, exist_ok=True)
        (bimi_out / "axon-bimi.svg").write_bytes(bimi_src.read_bytes())
        logo_dir = Site.ROOT / "media" / "logos"
        if logo_dir.is_dir():
            for src in sorted(logo_dir.iterdir()):
                if src.suffix.lower() in {".svg", ".webp", ".png"}:
                    (media_out / src.name).write_bytes(src.read_bytes())
        css_path = Site.OUT / "assets" / "site.css"
        css_path.write_text(Site.css(), encoding="utf-8")
        (Site.OUT / "assets" / "menu.js").write_text(Site.menu_script(), encoding="utf-8")
        for name in (
            "favicon.ico",
            "favicon.svg",
            "favicon.png",
            "favicon-192.png",
            "favicon-512.png",
        ):
            src = Site.ROOT / "media" / name
            if name == "favicon.png":
                src = Site.ROOT / "media" / "favicon-32.png"
            (Site.OUT / name).write_bytes(src.read_bytes())
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
        for article in Site.articles():
            if article["kind"] != "news":
                continue
            page = {"slug": article["slug"], "nav": None, "title": article["title"]}
            path = Site.page_path(article["slug"])
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(Site.document(page, Site.article_body(article)), encoding="utf-8")
        for note in Site.insight_notes():
            slug = "insights/" + note["slug"]
            page = {"slug": slug, "nav": None, "title": note["title"]}
            path = Site.page_path(slug)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(Site.document(page, Site.insight_article(note)), encoding="utf-8")
        missing = Site.document(
            {"slug": "", "nav": None, "title": "Not found", "missing": True},
            Site.missing_body(),
        )
        (Site.OUT / "404.html").write_text(missing, encoding="utf-8")
        for stub in (
            {"slug": "faqs", "nav": None, "title": "FAQs"},
            {"slug": "contact", "nav": None, "title": "Contact"},
        ):
            html = Site.document(stub, Site.redirect_stub_body(stub))
            path = Site.page_path(stub["slug"])
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(html, encoding="utf-8")

    @staticmethod
    def page_path(slug: str) -> Path:
        if slug == "":
            return Site.OUT / "index.html"
        return Site.OUT / slug / "index.html"

    @staticmethod
    def depth(slug: str) -> str:
        if slug == "":
            return ""
        return "../" * len([part for part in slug.split("/") if part])

    @staticmethod
    def href(from_slug: str, to_slug: str) -> str:
        origin = Path(from_slug or ".")
        target = Path(to_slug or ".")
        rel = os.path.relpath(target, origin).replace("\\", "/")
        if rel == ".":
            return "./"
        return rel + "/"

    @staticmethod
    def canonical(slug: str) -> str:
        if slug == "":
            return Site.ORIGIN
        return Site.ORIGIN + slug + "/"

    @staticmethod
    def mount() -> str:
        path = urlsplit(Site.ORIGIN).path
        if not path.endswith("/"):
            path += "/"
        return path

    @staticmethod
    def mount_urls(html: str) -> str:
        def one(url: str) -> str:
            if url.startswith(("https:", "http:", "mailto:", "tel:", "#", "/")):
                return url
            if url.startswith("./"):
                url = url[2:]
            return Site.mount() + url

        def repl(match: re.Match) -> str:
            attr, value = match.group(1), match.group(2)
            if attr == "srcset":
                items = []
                for part in value.split(","):
                    piece = part.strip()
                    if not piece:
                        continue
                    bits = piece.split()
                    bits[0] = one(bits[0])
                    items.append(" ".join(bits))
                value = ", ".join(items)
            else:
                value = one(value)
            return f'{attr}="{value}"'

        return re.sub(r'\b(srcset|href|src)="([^"]*)"', repl, html)

    @staticmethod
    def folio(slug: str) -> str:
        top = slug.split("/")[0] if slug else ""
        for index, item in enumerate(Site.MENU, start=1):
            slugs = {item["slug"], *[dest for _label, dest in item["children"]]}
            if top in slugs or (item["slug"] == "credentials" and top.startswith("recognition")):
                return f"{index:02d}"
        return ""

    @staticmethod
    def current(slug: str, dest: str) -> bool:
        if slug == dest or slug.startswith(dest + "/"):
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
        depth = Site.depth(slug)
        description = escape(
            "Axon Global Services trains boards and general counsel on cyber risk and delivers written board-level risk assessments."
            if page.get("home")
            else "Axon Global Services. Board training and pre-emptive cyber risk work."
        )
        og_description = (
            f'<meta property="og:description" content="{description}">\n'
            if page.get("home")
            else ""
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
        refresh = ""
        redirect = Site.REDIRECTS.get(slug)
        if redirect:
            dest, frag = redirect
            refresh = (
                '<meta http-equiv="refresh" content="0; url='
                + Site.href(slug, dest)
                + frag
                + '">\n'
            )
        robots = ""
        if slug in Site.NOINDEX_SLUGS:
            robots = '<meta name="robots" content="noindex">\n'
        if page.get("home"):
            content = main
        else:
            content = f'<div class="paper"><div class="frame page">{main}</div></div>'
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{refresh}{robots}<title>{title} — Axon Global Services</title>
<meta name="description" content="{description}">
{og_description}<meta name="referrer" content="no-referrer">
<meta http-equiv="Content-Security-Policy" content="{csp}">
<meta name="color-scheme" content="light">
<meta name="theme-color" content="#0e0d0b">
<link rel="canonical" href="{escape(Site.canonical(slug))}">
<link rel="icon" href="{depth}favicon.ico" sizes="16x16 32x32 48x48">
<link rel="icon" href="{depth}favicon.svg" type="image/svg+xml">
<link rel="icon" href="{depth}favicon-192.png" type="image/png" sizes="192x192">
<link rel="icon" href="{depth}favicon-512.png" type="image/png" sizes="512x512">
<link rel="apple-touch-icon" href="{depth}apple-touch-icon.png" sizes="180x180">
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
        if page.get("missing"):
            html = Site.mount_urls(html)
        return html

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
            "extended-capabilities": Site.imported_body,
            "how-we-engage": Site.imported_body,
            "our-ceo": Site.ceo_redirect_body,
            "sitemap": Site.sitemap_body,
        }
        return writers[slug](slug)

    # 160-grid line icons for the square cards. Ink only, no fills. Decorative.
    ICONS = {
        "training": (
            '<rect x="28" y="22" width="22" height="18"/>'
            '<rect x="69" y="22" width="22" height="18"/>'
            '<rect x="110" y="22" width="22" height="18"/>'
            '<rect x="32" y="62" width="96" height="36"/>'
            '<rect x="28" y="120" width="22" height="18"/>'
            '<rect x="69" y="120" width="22" height="18"/>'
            '<rect x="110" y="120" width="22" height="18"/>'
        ),
        "board-view": (
            '<rect x="46" y="16" width="68" height="128"/>'
            '<path d="M62 48 H98"/>'
            '<path d="M62 76 H98"/>'
            '<path d="M54 68 V84"/>'
            '<path d="M62 104 H98"/>'
            '<path d="M62 128 H98"/>'
        ),
        "supply": (
            '<circle cx="30" cy="80" r="16"/>'
            '<circle cx="80" cy="80" r="16"/>'
            '<circle cx="130" cy="80" r="16"/>'
            '<path d="M46 80 H64"/>'
            '<path d="M96 80 H114"/>'
        ),
        "ma": (
            '<rect x="24" y="28" width="68" height="68"/>'
            '<rect x="68" y="64" width="68" height="68"/>'
        ),
        "external": (
            '<circle cx="68" cy="62" r="34"/>'
            '<path d="M92 86 L132 126"/>'
        ),
        "program": (
            '<path d="M28 46 L40 58 L60 34"/>'
            '<path d="M76 46 H136"/>'
            '<path d="M28 84 L40 96 L60 72"/>'
            '<path d="M76 84 H136"/>'
            '<path d="M28 122 L40 134 L60 110"/>'
            '<path d="M76 122 H136"/>'
        ),
        "internal": (
            '<rect x="40" y="16" width="80" height="128"/>'
            '<path d="M56 44 H108"/>'
            '<path d="M56 68 H96"/>'
            '<path d="M56 92 H116"/>'
            '<path d="M56 116 H88"/>'
        ),
        "proactive": (
            '<path d="M124 24 V136"/>'
            '<path d="M24 80 H96"/>'
            '<path d="M78 58 L100 80 L78 102"/>'
        ),
    }

    @staticmethod
    def icon(offer_id: str) -> str:
        return (
            '<svg class="svc-icon" viewBox="0 0 160 160" width="160" height="160" '
            'fill="none" stroke="currentColor" stroke-width="3" '
            'stroke-linecap="square" stroke-linejoin="miter" aria-hidden="true">'
            f"{Site.ICONS[offer_id]}</svg>"
        )

    @staticmethod
    def service_card(offer: dict, slug: str, *, full: bool) -> str:
        name = offer["name"]
        word = Site.WORDS[offer["id"]]
        if word not in name:
            raise RuntimeError(f"{word!r} is not inside {name!r}")
        name_id = f'{offer["id"]}-name'
        tag = "h2" if full else "p"
        parts = [f'<{tag} class="svc-name" id="{name_id}">{escape(name)}</{tag}>']
        if offer.get("audience") and offer.get("receive"):
            parts.append(f'<p class="svc-for">{escape(offer["audience"])}</p>')
            parts.append(f'<p class="svc-get">{escape(offer["receive"])}</p>')
        if full:
            anchor = f' id="{escape(offer["id"])}"'
            parts.append(f'<p class="svc-body">{escape(offer["body"])}</p>')
        else:
            anchor = ""
        return (
            f'<li class="icon-card">'
            f'<article class="card" tabindex="0" aria-labelledby="{name_id}"{anchor}>'
            f'<div class="icon-card-stage">{Site.icon(offer["id"])}'
            f'<span class="svc-word" aria-hidden="true">{escape(word)}</span></div>'
            f'<div class="icon-card-panel">{"".join(parts)}</div>'
            "</article></li>"
        )

    @staticmethod
    def home_body(_slug: str) -> str:
        by_id = {offer["id"]: offer for offer in Site.OFFERINGS}
        cards = [Site.service_card(by_id[offer_id], "", full=False) for offer_id in Site.HOME_ORDER]
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
<ol class="svc-grid">{"".join(cards)}</ol>
</section>
</div>
</div>
"""

    @staticmethod
    def capabilities_body(_slug: str) -> str:
        by_id = {offer["id"]: offer for offer in Site.OFFERINGS}
        blocks = [
            Site.service_card(by_id[offer_id], "capabilities", full=True)
            for offer_id in Site.CAP_ORDER
        ]
        return f"""
<h1>Capabilities</h1>
<p class="lede">Eight lines of board training and pre-emptive cyber risk work.</p>
<ol class="svc-grid">{"".join(blocks)}</ol>
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
{Site.row("07", escape(data["who_value_heading"]), Site.value_block("who"))}
{Site.pictures("who", seals, "seal-grid")}
{Site.pictures("who", photos, "photo-grid")}
"""

    @staticmethod
    def proof_body(slug: str) -> str:
        data = Site.bundle()
        segments = "".join(
            f"<li>{escape(line)}</li>" for line in Site.who_we_are().proof.client_segments
        )
        return f"""
<h1>Proof</h1>
<p class="lede">{escape(data["who_credentials_heading"])}</p>
{Site.pictures(slug, Site.seal_rows(), "seal-grid")}
<ul class="plain">{"".join(f"<li>{escape(line)}</li>" for line in data["who_credentials"])}</ul>
{Site.figures()}
<section id="clients">
<h2>Our Clients</h2>
<ul class="plain">{segments}</ul>
{Site.client_logo_row(slug)}
</section>
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
    def insight_notes() -> tuple:
        return (
            {
                "slug": "board-oversight",
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
                "slug": "material-incident",
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
                "slug": "nist-govern",
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

    @staticmethod
    def insights_body(slug: str) -> str:
        items = []
        for note in Site.insight_notes():
            items.append(
                "<li>"
                f'<a href="{Site.href(slug, "insights/" + note["slug"])}">'
                f"{escape(note['title'])}</a></li>"
            )
        return f"""
<h1>Insights</h1>
<p class="lede">Short board notes. Each one is a reading of a public document.</p>
<ol class="archive">{"".join(items)}</ol>
"""

    @staticmethod
    def insight_article(note: dict) -> str:
        slug = "insights/" + note["slug"]
        sources = "".join(
            f'<li><a class="external" rel="external" href="{escape(url)}">{escape(label)}</a></li>'
            for label, url in note["sources"]
        )
        return f"""
<h1>{escape(note["title"])}</h1>
<div class="article">
<p>{escape(note["body"])}</p>
<ul class="sources">{sources}</ul>
</div>
<p class="back"><a href="{Site.href(slug, "insights")}">Insights</a></p>
"""

    @staticmethod
    def articles() -> list:
        data = json.loads((Site.ROOT / "content" / "articles.json").read_text(encoding="utf-8"))
        return data["articles"]

    @staticmethod
    def expand_refs(html: str, from_slug: str) -> str:
        def href_sub(match: re.Match) -> str:
            target = match.group(1)
            slug, _, frag = target.partition("#")
            if slug == "home":
                slug = ""
            url = Site.href(from_slug, slug)
            if frag:
                url = f"{url}#{frag}"
            return f'href="{url}"'

        html = re.sub(r'href="site:([^"]*)"', href_sub, html)

        def src_sub(match: re.Match) -> str:
            return f'src="{Site.media_src(from_slug, match.group(1))}"'

        return re.sub(r'src="media:([^"]+)"', src_sub, html)

    @staticmethod
    def wrap_bare_tokens(html: str) -> str:
        parts = re.split(r"(<[^>]+>)", html)
        token = re.compile(
            r"https?://[^\s<]+|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            re.I,
        )
        in_anchor = 0
        out = []
        for part in parts:
            if part.startswith("<"):
                match = re.match(r"<\s*(/?)\s*([a-zA-Z0-9]+)", part)
                if match and match.group(2).lower() == "a":
                    in_anchor += -1 if match.group(1) else 1
                out.append(part)
                continue
            if in_anchor > 0:
                out.append(part)
                continue
            out.append(
                token.sub(
                    lambda item: f'<span class="break-anywhere">{item.group(0)}</span>',
                    part,
                )
            )
        return "".join(out)

    @staticmethod
    def article_body(article: dict) -> str:
        slug = article["slug"]
        when = ""
        if article.get("date"):
            when = (
                f'<p class="lede"><time datetime="{escape(article["date"])}">'
                f'{escape(article["date"])}</time></p>'
            )
        source = ""
        if article.get("source"):
            source = f'<p class="source-note">Original source: {escape(article["source"])}</p>'
        body = Site.wrap_bare_tokens(Site.expand_refs(article.get("html") or "", slug))
        back = Site.href(slug, article.get("back") or "news")
        label = escape(article.get("back_label") or "News")
        return f"""
<h1>{escape(article["title"])}</h1>
{when}
{source}
<div class="article">{body}</div>
<p class="back"><a href="{back}">{label}</a></p>
"""

    @staticmethod
    def imported_body(slug: str) -> str:
        article = next(item for item in Site.articles() if item["slug"] == slug)
        return Site.article_body(article)

    @staticmethod
    def ceo_redirect_body(slug: str) -> str:
        dest, frag = Site.REDIRECTS[slug]
        href = Site.href(slug, dest) + frag
        return f"""
<h1>Our CEO &amp; Global CTO</h1>
<p><a href="{href}">Leadership</a></p>
"""

    @staticmethod
    def redirect_stub_body(page: dict) -> str:
        slug = page["slug"]
        dest, frag = Site.REDIRECTS[slug]
        href = Site.href(slug, dest) + frag
        label = next(item["title"] for item in Site.PAGES if item["slug"] == dest)
        return f"""
<h1>{escape(page["title"])}</h1>
<p><a href="{href}">{escape(label)}</a></p>
"""

    @staticmethod
    def portrait_sizes() -> str:
        cap = Site.PORTRAIT_MAX_REM * 16
        gutter = Site.NARROW_FRAME_GUTTER_REM * 16
        edge = int(cap + gutter) - 1
        return (
            f"(max-width: {edge}px) calc(100vw - {Site.NARROW_FRAME_GUTTER_REM}rem), "
            f"{Site.PORTRAIT_MAX_REM}rem"
        )

    @staticmethod
    def team_photo_sizes(width: int) -> str:
        gutter = Site.NARROW_FRAME_GUTTER_REM
        return (
            f"(max-width: 390px) calc(100vw - {gutter}rem), "
            f"(max-width: 640px) calc(100vw - 1.5rem), "
            f"(max-width: 800px) {width}px, "
            "calc((min(76rem, 100vw - 4rem) - 7.75rem) / 2)"
        )

    @staticmethod
    def about_body(slug: str) -> str:
        about = Site.who_we_are().about
        leader, team = about.leader, about.team
        creds = "".join(f"<li>{escape(line)}</li>" for line in Site.bundle()["who_credentials"])
        bio = "".join(f"<p>{escape(text)}</p>" for text in leader.bio)
        roles = "".join(
            f"<p>{escape(group.lead)}</p>"
            f'<ul class="plain">{"".join(f"<li>{escape(line)}</li>" for line in group.lines)}</ul>'
            for group in (team.executive, team.cyber_response)
        )
        clients = (
            f'<p><a href="{Site.href(slug, "proof")}#clients">{escape(team.closing)}</a></p>'
        )
        portrait = Site.image(slug, leader.portrait, Site.portrait_sizes())
        leadership = (
            f'<figure class="portrait">{portrait}</figure>'
            f'<div class="prose"><h3>{escape(leader.name)}</h3>'
            f'<p class="quiet">{escape(leader.role)}</p>{bio}</div>'
        )
        photo = Site.image(slug, team.photo, Site.team_photo_sizes(int(team.photo["width"])))
        team_copy = (
            f'<div class="prose"><p>{escape(team.nda)}</p></div>'
            f'<div class="team-split">'
            f'<div class="prose">{roles}{clients}</div>'
            f'<figure class="team-photo">{photo}</figure>'
            f"</div>"
        )
        return f"""
<h1>{escape(about.title)}</h1>
<p class="lede">{escape(about.subtitle)}</p>
<p class="prose">{escape(about.intro)}</p>
<ul class="plain">{creds}</ul>
{Site.row("01", "Leadership", leadership, "leadership")}
{Site.row("02", "Team", team_copy, "team")}
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
            href = Site.href(slug, page["slug"])
            if page["slug"] == "our-ceo":
                href = Site.href(slug, "about") + "#leadership"
                current = ""
            items.append(
                f'<li><a href="{href}"{current}>{escape(label)}</a></li>'
            )
        news = []
        for article in Site.articles():
            if article["kind"] != "news":
                continue
            news.append(
                f'<li><a href="{Site.href(slug, article["slug"])}">{escape(article["title"])}</a></li>'
            )
        notes = []
        for note in Site.insight_notes():
            notes.append(
                "<li>"
                f'<a href="{Site.href(slug, "insights/" + note["slug"])}">'
                f"{escape(note['title'])}</a></li>"
            )
        return f"""
<h1>Sitemap</h1>
<ol class="map">{"".join(items)}</ol>
<h2>News</h2>
<ol class="map">{"".join(news)}</ol>
<h2>Insights</h2>
<ol class="map">{"".join(notes)}</ol>
"""

    PORTRAIT_MAX_REM = 22
    NARROW_FRAME_GUTTER_REM = 1.25
    TEAM_PHOTO_ID = "uscert-our-team"
    WHO_WE_ARE_CANON_SHA256 = "39ff90094c2ae54279b22f482907c82eaffb5551900d639df997838528cee2b4"

    @dataclass(frozen=True)
    class RoleList:
        lead: str
        lines: tuple[str, ...]

    @dataclass(frozen=True)
    class Team:
        nda: str
        executive: Site.RoleList
        cyber_response: Site.RoleList
        closing: str
        photo: dict

    @dataclass(frozen=True)
    class Leader:
        name: str
        role: str
        portrait: dict
        bio: tuple[str, ...]

    @dataclass(frozen=True)
    class AboutCopy:
        title: str
        subtitle: str
        intro: str
        leader: Site.Leader
        team: Site.Team

    @dataclass(frozen=True)
    class ProofCopy:
        client_segments: tuple[str, ...]

    @dataclass(frozen=True)
    class WhoWeAre:
        about: Site.AboutCopy
        proof: Site.ProofCopy

    @staticmethod
    def who_we_are() -> Site.WhoWeAre:
        raw = json.loads((Site.ROOT / "content" / "who-we-are.json").read_text(encoding="utf-8"))
        canon = json.dumps(raw, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
        digest = hashlib.sha256(canon.encode("ascii")).hexdigest()
        if digest != Site.WHO_WE_ARE_CANON_SHA256:
            raise SystemExit(
                "content/who-we-are.json no longer matches the owner-approved copy. "
                "The lock is a sha256 of canonical JSON, not the file bytes. "
                "Restore it (git diff content/who-we-are.json). "
                f"Set WHO_WE_ARE_CANON_SHA256 = {digest!r} only for wording the owner supplied."
            )
        about = raw["about"]
        leader = about["leader"]
        team = about["team"]
        row = Site.media_row(leader["portrait"])
        photo = Site.media_row(Site.TEAM_PHOTO_ID)
        narrow = Path(photo["file"]).stem + "-300.webp"
        if int(photo["width"]) > 300 and not (Site.ROOT / "media" / narrow).is_file():
            raise SystemExit(f"missing media/{narrow}; the team photo needs its 300w candidate")
        return Site.WhoWeAre(
            about=Site.AboutCopy(
                title=about["title"],
                subtitle=about["subtitle"],
                intro=about["intro"],
                leader=Site.Leader(
                    name=leader["name"],
                    role=leader["role"],
                    portrait=row,
                    bio=tuple(leader["bio"]),
                ),
                team=Site.Team(
                    nda=team["nda"],
                    executive=Site.RoleList(
                        team["executive"]["lead"],
                        tuple(team["executive"]["lines"]),
                    ),
                    cyber_response=Site.RoleList(
                        team["cyber_response"]["lead"],
                        tuple(team["cyber_response"]["lines"]),
                    ),
                    closing=team["closing"],
                    photo=photo,
                ),
            ),
            proof=Site.ProofCopy(tuple(raw["proof"]["client_segments"])),
        )

    @staticmethod
    def _strings(record) -> tuple[str, ...]:
        out = []
        for field in fields(record):
            value = getattr(record, field.name)
            if isinstance(value, str):
                out.append(value)
            elif isinstance(value, tuple):
                out.extend(value)
            elif is_dataclass(value):
                out.extend(Site._strings(value))
        return tuple(out)

    @staticmethod
    def bundle() -> dict:
        return json.loads((Site.ROOT / "content" / "pages.json").read_text(encoding="utf-8"))

    @staticmethod
    def catalog() -> list:
        data = json.loads((Site.ROOT / "content" / "assets.json").read_text(encoding="utf-8"))
        return data["assets"]

    @staticmethod
    def media_src(slug: str, filename: str) -> str:
        return f"{Site.depth(slug)}assets/media/{filename}"

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
    def media_row(asset_id: str) -> dict:
        row = next((item for item in Site.catalog() if item["id"] == asset_id), None)
        if row is None:
            raise SystemExit(f"no catalog row for {asset_id}")
        media = Site.ROOT / "media"
        if not (media / row["file"]).is_file():
            raise SystemExit(f"missing media/{row['file']}")
        small = Path(row["file"]).stem + "-sm.webp"
        if int(row["width"]) > 640 and not (media / small).is_file():
            raise SystemExit(f"missing media/{small}; the image needs its 640w candidate")
        return row

    @staticmethod
    def image(slug: str, row: dict, sizes: str) -> str:
        src = Site.media_src(slug, row["file"])
        width = int(row["width"])
        stem = Path(row["file"]).stem
        parts = []
        narrow_name = stem + "-300.webp"
        if width > 300 and (Site.ROOT / "media" / narrow_name).is_file():
            parts.append(f"{Site.media_src(slug, narrow_name)} 300w")
        small_name = stem + "-sm.webp"
        if width > 640 and (Site.ROOT / "media" / small_name).is_file():
            parts.append(f"{Site.media_src(slug, small_name)} 640w")
        parts.append(f"{src} {width}w")
        return (
            f'<img src="{src}" srcset="{", ".join(parts)}" sizes="{sizes}" '
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
    def value_block(slug: str) -> str:
        text = Site.bundle()["who_value"]
        government, rest = text.split(" Axon is also executing", 1)
        infra, training = rest.split(" Axon Global has provided", 1)
        infra = "Axon is also executing" + infra
        training = "Axon Global has provided" + training
        line_200, line_300 = training.split(" and over 300 ", 1)
        line_300 = "over 300 " + line_300
        cut = line_300.find(" https://")
        if cut != -1:
            line_300 = line_300[:cut].rstrip()
        if "while simultaneously" not in government:
            raise SystemExit("government line drifted from the source")
        if "Cybersecurity Infrastructure Security Agency" not in government:
            raise SystemExit("agency name drifted from the source")
        proof = Site.href(slug, "proof") + "#clients"
        authority = Site.href(slug, "authority")
        return f"""
<div class="mandate">
<div class="mandate-row">
<p class="mandate-label">Government work</p>
<p>{escape(government.strip())}</p>
</div>
<div class="mandate-row">
<p class="mandate-label">Critical infrastructure</p>
<p>{escape(infra.strip())}</p>
</div>
<div class="mandate-row">
<p class="mandate-label">Board training</p>
<div>
<ul class="mandate-pair">
<li><p class="mandate-num">200+</p><p>{escape(line_200.strip())}</p></li>
<li><p class="mandate-num">300+</p><p>{escape(line_300.strip())} <a href="{proof}">our clients</a></p></li>
</ul>
<p class="mandate-links"><a href="{authority}">See awards and recognitions</a></p>
</div>
</div>
</div>
"""

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
{Site.value_block(slug)}
"""

    @staticmethod
    def recognition_body(slug: str) -> str:
        index = {"recognition": 0, "recognition-2": 1, "recognition-3": 2}[slug]
        groups = Site.recognition_groups()
        parts = ("recognition", "recognition-2", "recognition-3")
        links = []
        titles = ("Recognitions", "Recognitions (2 of 3)", "Recognitions (3 of 3)")
        for number, part in enumerate(parts):
            current = ' aria-current="page"' if part == slug else ""
            links.append(f'<a href="{Site.href(slug, part)}"{current}>{titles[number]}</a>')
        lede = '<p class="lede">General Photos, Letters, and Other</p>' if index == 0 else ""
        title = titles[index]
        return f"""
<h1>{title}</h1>
{lede}
{Site.pictures(slug, groups[index], "recog-grid")}
<nav class="part-nav" aria-label="Recognition pages">{"".join(links)}</nav>
"""

    _NEWS_MONTHS = {
        "january": 1,
        "february": 2,
        "march": 3,
        "april": 4,
        "may": 5,
        "june": 6,
        "july": 7,
        "august": 8,
        "september": 9,
        "october": 10,
        "november": 11,
        "december": 12,
    }

    @staticmethod
    def news_stamp(post: dict) -> str | None:
        """ISO day from a title dateline. None when the post does not state one day."""
        title = (post.get("title") or "").strip()
        match = re.match(r"(20\d{2})\s+([A-Za-z]+)\s+(\d{1,2})\b(.*)$", title)
        if not match:
            return None
        year, month_name, day, rest = match.groups()
        if re.match(r"\s*[-–—]\s*\d", rest):
            return None
        month = Site._NEWS_MONTHS.get(month_name.casefold())
        if month is None:
            return None
        try:
            stamped = date(int(year), month, int(day)).isoformat()
        except ValueError:
            return None
        excerpt = post.get("excerpt") or ""
        other = re.search(r"(20\d{2})\s+([A-Za-z]+)\s+(\d{1,2})\b", excerpt)
        if other:
            excerpt_month = Site._NEWS_MONTHS.get(other.group(2).casefold())
            if excerpt_month is None:
                return None
            try:
                excerpt_day = date(int(other.group(1)), excerpt_month, int(other.group(3))).isoformat()
            except ValueError:
                return None
            if excerpt_day != stamped:
                return None
        return stamped

    @staticmethod
    def news_body(slug: str) -> str:
        posts = json.loads((Site.ROOT / "content" / "news.json").read_text(encoding="utf-8"))
        months = Site.bundle()["archive_months"]
        month_links = "".join(
            f'<a href="#{escape(key)}">{escape(label)}</a>' for label, key in months
        )
        groups: dict[str, list] = {}
        order: list[str] = []
        for post in posts:
            key = (post.get("date") or "")[:7]
            if key not in groups:
                order.append(key)
                groups[key] = []
            groups[key].append(post)
        sections = []
        for key in order:
            items = []
            for post in groups[key]:
                excerpt = (
                    f"<p>{Site.wrap_bare_tokens(escape(post['excerpt']))}</p>"
                    if post.get("excerpt")
                    else ""
                )
                stamp = Site.news_stamp(post)
                time = (
                    f'<time datetime="{escape(stamp)}">{escape(stamp)}</time>'
                    if stamp
                    else ""
                )
                article = "news/" + post["source"].rstrip("/").split("/")[-1]
                items.append(
                    "<li>"
                    f'<a href="{Site.href(slug, article)}">'
                    f"{time}"
                    f"<span>{escape(post['title'])}</span></a>"
                    f"{excerpt}</li>"
                )
            sections.append(
                f'<section id="{escape(key)}"><ol class="archive">{"".join(items)}</ol></section>'
            )
        return f"""
<h1>News</h1>
<p class="lede">Supporting Documentation for Axon Discourses, Awards and Recognitions</p>
<nav class="month-nav" aria-label="News archive">{month_links}</nav>
{"".join(sections)}
"""

    class Disclosure:
        def __init__(self, anchor: str, trigger: str, panel: str) -> None:
            if not trigger or not panel:
                raise ValueError("disclosure needs a trigger and a panel")
            if not re.fullmatch(r"[a-z0-9-]+", anchor):
                raise ValueError("disclosure anchor is not a slug")
            self.anchor = anchor
            self.trigger = trigger
            self.panel = panel

    @staticmethod
    def quote_excluded(entry: dict) -> bool:
        blob = f"{entry.get('quote', '')} {entry.get('note', '')}".casefold()
        return "[poop]" in blob or "[fill in the blank]" in blob

    @staticmethod
    def quote_disclosures(entries: list[dict]) -> list[Disclosure]:
        items: list[Site.Disclosure] = []
        seen: set[str] = set()
        for entry in entries:
            if Site.quote_excluded(entry):
                continue
            quote = entry["quote"]
            note = entry["note"]
            if not quote or not note:
                raise ValueError("empty quote or note")
            folded = quote.casefold()
            for mark in ("'", "\u2018", "\u2019", "\u201c", "\u201d", '"'):
                folded = folded.replace(mark, "")
            words = re.findall(r"[a-z0-9]+", folded)[:5]
            anchor = "quote-" + "-".join(words)
            if anchor in seen:
                raise ValueError("duplicate disclosure anchor")
            seen.add(anchor)
            items.append(Site.Disclosure(anchor, quote, note))
        return items

    @staticmethod
    def accordion(items: list[Disclosure]) -> str:
        rows = []
        for item in items:
            anchor = escape(item.anchor)
            panel_id = escape(f"{item.anchor}-panel")
            rows.append(
                '<li class="faq-item">'
                "<h3>"
                f'<button type="button" class="faq-trigger" id="{anchor}" '
                f'aria-expanded="true" aria-controls="{panel_id}">'
                f'<span class="faq-text">{escape(item.trigger)}</span>'
                '<span class="faq-icon" aria-hidden="true"></span>'
                "</button>"
                "</h3>"
                f'<div class="faq-panel" id="{panel_id}" role="region" '
                f'aria-labelledby="{anchor}">'
                f'<div class="faq-answer"><p class="quiet">{escape(item.panel)}</p></div>'
                "</div>"
                "</li>"
            )
        return '<ul class="faq">' + "".join(rows) + "</ul>"

    @staticmethod
    def faq_body(_slug: str) -> str:
        data = Site.bundle()
        intro = "".join(f"<p>{escape(line)}</p>" for line in data["faq_intro"])
        quotes = Site.accordion(Site.quote_disclosures(data["faq_quotes"]))
        lessons = "".join(f"<li>{escape(line)}</li>" for line in data["faq_lessons"])
        lesson_intro = "".join(f"<p>{escape(line)}</p>" for line in data["faq_lessons_intro"])
        return f"""
<h1>FAQs</h1>
{intro}
<h2>Top Quotes</h2>
<p>{escape(data["faq_disclaimer"])}</p>
{quotes}
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
                    '<li><a href="'
                    + Site.href(_slug, "extended-capabilities")
                    + f'">{escape(line)}</a></li>'
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
            '<a class="external" rel="external" href="https://www.youtube.com/watch?v=0K6npguJuuc&amp;sns=em">Morrison &amp; Foerster, LLP</a>',
        )
        paragraph = paragraph.replace(
            "DLA Piper LLP",
            '<a class="external" rel="external" href="https://www.dlapiper.com/en/uk/focus/eu-data-protection-regulation/key-changes/">DLA Piper LLP</a>',
        )
        paragraph = paragraph.replace(
            "AxonInfo@AxonCyber.com",
            '<a href="mailto:AxonInfo@AxonCyber.com">AxonInfo@AxonCyber.com</a>',
        )
        readings = []
        for item in data["fyi_readings"]:
            text = escape(item["text"])
            if item.get("href"):
                readings.append(
                    f'<li><a class="external" rel="external" href="{escape(item["href"])}">{text}</a></li>'
                )
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
        slugs = [page["slug"] for page in Site.PAGES if page["slug"] != "our-ceo"]
        slugs += [article["slug"] for article in Site.articles() if article["kind"] == "news"]
        slugs += ["insights/" + note["slug"] for note in Site.insight_notes()]
        urls = []
        for slug in slugs:
            loc = Site.canonical(slug)
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
(function () {
  var cards = document.querySelectorAll(".icon-card");
  if (!cards.length) return;
  var fine = window.matchMedia("(hover: hover) and (pointer: fine)");
  var wide = window.matchMedia("(min-width: 761px)");

  function cardOf(node) {
    if (!node || !node.closest) return null;
    return node.classList && node.classList.contains("icon-card") ? node : node.closest(".icon-card");
  }

  function waitMs() {
    return window.matchMedia("(prefers-reduced-motion: reduce)").matches ? 0 : 120;
  }

  Array.prototype.forEach.call(cards, function (card) {
    card.addEventListener("pointerenter", function () {
      if (!fine.matches) return;
      clearTimeout(card._hotTimer);
      card._hotTimer = setTimeout(function () {
        if (!card.classList.contains("is-suppressed")) card.classList.add("is-hot");
      }, waitMs());
    });
    card.addEventListener("pointerleave", function () {
      clearTimeout(card._hotTimer);
      card.classList.remove("is-hot");
      card.classList.remove("is-suppressed");
    });
  });

  document.addEventListener("keydown", function (event) {
    if (event.key !== "Escape" || !fine.matches) return;
    var hovered = null;
    Array.prototype.forEach.call(cards, function (card) {
      if (card.matches(":hover")) hovered = card;
    });
    var focused = cardOf(document.activeElement);
    var card = focused || hovered;
    if (!card) return;
    clearTimeout(card._hotTimer);
    card.classList.remove("is-hot");
    card.classList.add("is-suppressed");
    if (focused && document.activeElement && card.contains(document.activeElement)) {
      document.activeElement.blur();
    }
  });

  document.addEventListener("focusin", function (event) {
    var card = cardOf(event.target);
    if (card) card.classList.remove("is-suppressed");
  });

  function openFromHash() {
    var id = (location.hash || "").replace(/^#/, "");
    if (!id) return;
    var node = document.getElementById(id);
    var card = cardOf(node);
    if (!card) return;
    card.classList.remove("is-suppressed");
    card.classList.add("is-open");
  }

  openFromHash();
  window.addEventListener("hashchange", openFromHash);

  function lockRows() {
    Array.prototype.forEach.call(document.querySelectorAll(".svc-grid"), function (grid) {
      var items = grid.querySelectorAll(".icon-card");
      Array.prototype.forEach.call(items, function (card) {
        card.style.minHeight = "";
        var article = card.querySelector(".card");
        if (article) article.style.minHeight = "";
      });
      if (!fine.matches || !wide.matches) return;
      var rows = [];
      Array.prototype.forEach.call(items, function (card) {
        var top = Math.round(card.getBoundingClientRect().top);
        var row = rows.length && Math.abs(rows[rows.length - 1].top - top) < 2 ? rows[rows.length - 1] : null;
        if (!row) {
          row = { top: top, items: [] };
          rows.push(row);
        }
        var article = card.querySelector(".card");
        var panel = card.querySelector(".icon-card-panel");
        var border = article ? parseFloat(getComputedStyle(article).borderTopWidth) || 0 : 0;
        var square = Math.round(card.getBoundingClientRect().width);
        var openH = Math.max(square, Math.ceil(panel.scrollHeight + border));
        row.items.push({ card: card, article: article, openH: openH });
      });
      rows.forEach(function (row) {
        var tall = 0;
        row.items.forEach(function (item) {
          if (item.openH > tall) tall = item.openH;
        });
        var px = tall + "px";
        row.items.forEach(function (item) {
          item.card.style.minHeight = px;
          if (item.article) item.article.style.minHeight = px;
        });
      });
    });
  }

  lockRows();
  window.addEventListener("resize", lockRows);
  if (fine.addEventListener) fine.addEventListener("change", lockRows);
  if (wide.addEventListener) wide.addEventListener("change", lockRows);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(lockRows);
})();
(function () {
  var lists = document.querySelectorAll(".faq");
  if (!lists.length) return;

  function triggerIn(node) {
    var item = node && node.closest ? node.closest(".faq-item") : null;
    return item ? item.querySelector(".faq-trigger") : null;
  }

  function setOpen(trigger, open) {
    trigger.setAttribute("aria-expanded", open ? "true" : "false");
  }

  function openFromHash() {
    var id = (location.hash || "").replace(/^#/, "");
    var trigger = id ? triggerIn(document.getElementById(id)) : null;
    if (trigger) setOpen(trigger, true);
  }

  Array.prototype.forEach.call(lists, function (list) {
    Array.prototype.forEach.call(list.querySelectorAll(".faq-trigger"), function (trigger) {
      setOpen(trigger, false);
    });
    list.addEventListener("click", function (event) {
      var trigger = event.target.closest(".faq-trigger");
      if (!trigger || !list.contains(trigger)) return;
      setOpen(trigger, trigger.getAttribute("aria-expanded") !== "true");
    });
  });
  openFromHash();
  lists[0].getBoundingClientRect();
  Array.prototype.forEach.call(lists, function (list) {
    list.classList.add("faq-live");
  });
  window.addEventListener("hashchange", openFromHash);
})();
"""

    @staticmethod
    def css() -> str:
        text = """@font-face {
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
  font-size: clamp(1rem, 0.945rem + 0.2vw, 1.125rem);
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
.skip:focus,
.skip:focus-visible {
  outline: 2px solid var(--bone);
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
  font-size: 0.75rem;
  line-height: 1.2;
}
.mark { width: 2.35rem; height: 2.35rem; display: block; flex: none; }
.folio {
  margin: 0;
  font-size: 1em;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--quiet-dark);
  min-width: 1.5rem;
}
.mast-action { margin: 0; }
.mast-action .action {
  color: var(--ink);
  background: var(--signal);
  box-shadow: none;
  border: 1px solid var(--ink);
  min-height: 48px;
  padding: calc(0.7rem - 1px) calc(1.15rem - 1px);
  font-weight: 600;
  text-decoration: none;
  white-space: nowrap;
}
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
  font-size: 1rem;
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
  color: var(--bone);
  font-size: 1.125rem;
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
  border: 1px solid var(--ink);
  min-height: 48px;
  padding: calc(0.7rem - 1px) calc(1.15rem - 1px);
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
  font-size: 1em;
  letter-spacing: 0.14em;
  font-weight: 500;
  text-transform: uppercase;
}
.row h2 {
  margin: 0 0 0.7rem;
  font-size: clamp(1.45rem, 2.2vw, 2rem);
  font-weight: 560;
  letter-spacing: -0.03em;
  line-height: 1.12;
  text-transform: none;
}
.row h3 {
  margin: 0 0 0.15rem;
  font-size: clamp(1.2rem, 0.5vw + 1.05rem, 1.45rem);
  font-weight: 560;
  letter-spacing: -0.02em;
  line-height: 1.15;
}
p { margin: 0 0 0.75rem; }
main p { max-width: 27em; }
.quiet { color: var(--quiet); }
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
.offering p { margin: 0; max-width: 27em; }
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
.sources > li > a { display: block; max-width: 27em; }
.table-wrap { overflow-x: auto; max-width: 100%; }
table { width: 100%; border-collapse: collapse; }
caption {
  caption-side: bottom;
  text-align: left;
  color: var(--quiet);
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
  font-size: 0.75rem;
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
  font-size: 0.75rem;
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
  max-width: 27em;
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
.seal-grid { grid-template-columns: repeat(5, minmax(0, 1fr)); }
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
.prose { max-width: 40rem; }
main .prose,
main .prose li,
main ul:not([class]) > li { max-width: 27em; }
.portrait img { display: block; width: 100%; height: auto; }
.team-split {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  gap: 1.5rem 1.75rem;
  align-items: start;
}
.team-photo { margin: 0; min-width: 0; }
.team-photo img { display: block; width: 100%; max-width: 617px; height: auto; aspect-ratio: 617 / 462; }
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
  height: auto;
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  background: transparent;
}
.logo-row .logo-fallback {
  padding: 0 0.3rem;
  font-weight: 560;
  font-size: 1em;
  letter-spacing: -0.02em;
  line-height: 1.15;
  text-align: center;
  overflow: hidden;
}
.logo-more { margin: -0.2rem 0 1.2rem; }
.logo-more a { font-weight: 560; text-decoration: none; }
.plain li { margin: 0; padding: 0.85rem 0; border-top: 1px solid var(--rule); }
.plain > li { padding-right: max(0px, calc(100% - 27em)); }
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
  max-width: 27em;
  min-height: 44px;
  text-decoration: none;
  font-weight: 520;
}
.archive time { flex: none; color: var(--quiet); }
.archive p { margin: 0.15rem 0 0; color: var(--quiet); }
.article { overflow-wrap: normal; }
.article-figure { margin: 1rem 0; }
.article img, .article-figure img { max-width: 100%; height: auto; }
.source-note { color: var(--quiet); overflow-wrap: anywhere; }
.break-anywhere { overflow-wrap: anywhere; }
.back { margin-top: 2rem; }
a.external::after { content: " (external)"; }
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
  .team-split { grid-template-columns: minmax(0, 1fr); }
  .team-photo img { margin-inline: auto; }
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
  font-size: 1rem;
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
.lede { font-size: clamp(1.12rem, 0.4vw + 1rem, 1.38rem); max-width: 27em; }
.eyebrow {
  margin: 0 0 0.8rem;
  font-size: 0.75rem;
  letter-spacing: 0.16em;
  text-transform: uppercase;
}
.trust { padding: 1.45rem 0 0.2rem; }
.trust-line { max-width: 27em; margin: 0.15rem 0 0; }
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
  white-space: nowrap;
}
.mandate { border-top: 1px solid var(--ink); margin: 1.4rem 0 0; }
.mandate-row {
  display: grid;
  grid-template-columns: 9.25rem minmax(0, 1fr);
  gap: 0.75rem 1.5rem;
  align-items: start;
  padding: 1rem 0;
  border-bottom: 1px solid var(--ink);
}
.mandate-label { margin: 0; font-weight: 560; }
.mandate-row > p,
.mandate-pair p { margin: 0; }
.mandate-pair {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem 1.5rem;
  list-style: none;
  margin: 0;
  padding: 0;
}
.mandate-pair li { margin: 0; padding-left: 0.95rem; position: relative; }
.mandate-pair li::before {
  content: "";
  position: absolute;
  left: 0;
  top: 1.7rem;
  width: 0.4rem;
  height: 0.4rem;
  border-radius: 50%;
  background: currentColor;
}
.mandate-pair .mandate-num {
  margin: 0 0 0.35rem;
  font-size: 64px;
  line-height: 1;
  font-weight: 560;
  letter-spacing: -0.04em;
  white-space: nowrap;
}
.mandate-pair p { word-break: normal; hyphens: none; }
@media (max-width: 760px) {
  .logo-row .logo-fallback {
    width: 160px;
    max-width: 160px;
    height: auto;
    min-height: 40px;
    padding: 8px 16px;
    overflow: visible;
    white-space: normal;
  }
  .logo-row .logo-fallback span {
    min-width: 0;
    max-width: 100%;
  }
  .mandate-row {
    grid-template-columns: 1fr;
    row-gap: 12px;
    padding: 16px 0;
    border-bottom: 1px solid var(--ink);
  }
  .mandate-row > p,
  .mandate-pair,
  .mandate-pair p {
    text-align: left;
  }
  .mandate-pair {
    grid-template-columns: 1fr 1fr;
    column-gap: 24px;
    row-gap: 24px;
  }
  .mandate-pair li { padding-left: 0; }
  .mandate-pair li::before { content: none; }
  .mandate-pair .mandate-num {
    white-space: nowrap;
    font-size: clamp(44px, 12vw, 64px);
  }
}
.mandate-links { display: flex; flex-direction: column; align-items: flex-start; margin-top: 0.35rem; }
.mandate-links a {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  min-height: 44px;
  width: max-content;
  max-width: 100%;
  color: inherit;
  text-decoration: none;
  font-weight: 560;
}
.mandate-links a::after { content: "→"; }
.card, .offering { padding: 0; overflow: hidden; }
.svc-icon {
  display: block;
  width: 2rem;
  height: 2rem;
  margin: 0 0 0.85rem;
  color: var(--ink);
}
.svc-icon svg { display: block; width: 2rem; height: 2rem; }
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
  border: 1px solid var(--ink);
  min-height: 48px;
  padding: calc(0.7rem - 1px) calc(1.15rem - 1px);
  font-weight: 600;
  text-decoration: none;
}
.foot-nav { display: grid; grid-template-columns: max-content max-content; gap: 0.35rem 1.2rem; }
.foot-nav a { white-space: nowrap; }
.foot-group { display: flex; flex-direction: column; align-items: flex-start; }
.foot-group a { text-decoration: none; }
@media (min-width: 1024px) {
  body { font-size: 1.125rem; }
  .nav a, .foot-nav a, .menu-trigger { font-size: 1.125rem; }
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
  .wordmark {
    justify-self: start;
    width: max-content;
    max-width: calc(100% - 44px - 16px);
    height: 44px;
    min-height: 44px;
  }
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
body, p, h1, h2, h3, h4, h5, h6, li, dd {
  word-break: normal;
  overflow-wrap: normal;
  hyphens: none;
}
@media (max-width: 700px) {
  .logo-row li { height: 40px; min-height: 40px; }
}
@media (max-width: 480px) {
  .hero { padding-top: 2.15rem; }
}
@media (max-width: 1023px) {
  .logo-row {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
  }
  .logo-row li {
    flex: 0 0 160px;
    width: 160px;
    height: 40px;
    min-height: 40px;
  }
  .seal-grid,
  .photo-grid,
  .recog-grid {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    border: 0;
    margin-left: auto;
    margin-right: auto;
  }
  .seal-grid li,
  .photo-grid li,
  .recog-grid li {
    flex: 0 0 50%;
    width: 50%;
    max-width: 50%;
    border: 0 solid var(--ink);
    border-right-width: 1px;
    border-bottom-width: 1px;
  }
  .seal-grid li:nth-child(odd),
  .photo-grid li:nth-child(odd),
  .recog-grid li:nth-child(odd) {
    border-left-width: 1px;
  }
  .seal-grid li:nth-child(-n + 2),
  .photo-grid li:nth-child(-n + 2),
  .recog-grid li:nth-child(-n + 2) {
    border-top-width: 1px;
  }
  .portrait,
  .hero-photo {
    margin-left: auto;
    margin-right: auto;
  }
}
@media (max-width: 390px) {
  .frame { width: min(76rem, calc(100% - 1.25rem)); }
  .wordmark-name { letter-spacing: 0.12em; }
  .wordmark-line { letter-spacing: 0.1em; }
}
@media (prefers-reduced-motion: reduce) {
  .mark-lg .mass,
  .nav-bars, .nav-bars::before, .nav-bars::after,
  .menu-trigger::after,
  .icon-card .svc-icon,
  .icon-card-panel,
  .svc-word,
  .svc-grid .card {
    animation: none;
    transition: none;
  }
}
.svc-grid {
  list-style: none;
  margin: 0.4rem 0 0;
  padding: 0;
  display: grid;
  grid-template-columns: 1fr;
  gap: 28px;
  justify-content: start;
  border: 0;
}
.svc-grid > li {
  display: flex;
  margin: 0;
  padding: 0;
  border: 0;
  min-width: 0;
}
.svc-grid .card {
  position: relative;
  box-sizing: border-box;
  display: block;
  width: 100%;
  margin: 0;
  padding: 4px 0 16px;
  border: 0;
  border-top: 1px solid var(--ink);
  border-radius: 0;
  background: #e4dccb;
  color: var(--ink);
  outline: 1px solid #5e584e;
  outline-offset: -1px;
  transition: background-color 120ms, outline-color 120ms;
}
.svc-grid .icon-card:hover .card,
.svc-grid .icon-card.is-hot .card,
.svc-grid .icon-card.is-open .card,
.svc-grid .icon-card:focus-within .card {
  background: #ddd4c1;
  outline-color: #0e0d0b;
}
.icon-card-stage {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}
.svc-grid .svc-icon {
  display: block;
  width: 96px;
  height: 96px;
  margin: 0;
  flex: none;
  color: var(--ink);
}
@media (forced-colors: active) {
  .svc-icon { color: CanvasText; }
  .svc-grid .svc-icon { color: CanvasText; }
}
.svc-word {
  margin: 0;
  color: var(--ink);
  font-size: 22px;
  font-weight: 600;
  line-height: 28px;
  letter-spacing: 0;
  text-align: center;
}
.icon-card-panel { padding: 16px 24px 24px; }
.svc-grid .svc-name,
.svc-grid .svc-for,
.svc-grid .svc-get,
.svc-grid .svc-body {
  margin: 0;
  max-width: none;
  color: var(--ink);
  font-size: 16px;
  font-weight: 400;
  line-height: 22px;
  letter-spacing: 0;
  text-transform: none;
}
.svc-grid .svc-name {
  margin: 0 0 8px;
  font-size: 22px;
  font-weight: 600;
  line-height: 28px;
}
.svc-grid .svc-for,
.svc-grid .svc-get,
.svc-grid .svc-body { margin: 0 0 8px; }
.svc-grid .icon-card:has(.card:focus-visible),
.svc-grid .icon-card:focus-within {
  outline: 2px solid var(--ink);
  outline-offset: 2px;
}
@media (min-width: 761px) {
  .svc-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); column-gap: 40px; row-gap: 32px; }
}
@media (min-width: 1280px) {
  .svc-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }
}
@media (max-width: 760px) {
  .svc-word,
  .svc-grid .svc-name {
    font-size: 20px;
    line-height: 26px;
  }
  .icon-card-panel > :last-child { margin-bottom: 0; }
}
@media (hover: none), (pointer: coarse) {
  .icon-card-panel > :last-child { margin-bottom: 0; }
}
@media (hover: hover) and (pointer: fine) and (min-width: 761px) {
  .svc-grid {
    grid-template-columns: minmax(0, 368px);
    column-gap: 48px;
    row-gap: 48px;
    align-items: start;
    justify-content: start;
  }
  .svc-grid > li,
  .svc-grid .card {
    width: min(368px, 100%);
    height: auto;
    aspect-ratio: 1;
    padding: 0;
    overflow: hidden;
  }
  .icon-card-stage,
  .icon-card-panel {
    position: absolute;
    inset: 0;
    box-sizing: border-box;
    transition: opacity 140ms ease;
    transition-delay: 0s;
  }
  .icon-card-stage {
    z-index: 1;
    justify-content: center;
    gap: 16px;
    padding: 0;
    opacity: 1;
    pointer-events: none;
  }
  .svc-grid .svc-icon {
    position: static;
    width: 160px;
    height: 160px;
  }
  .icon-card-panel {
    z-index: 2;
    padding: 28px 24px;
    overflow: auto;
    opacity: 0;
    pointer-events: none;
  }
  .svc-grid .svc-for,
  .svc-grid .svc-get,
  .svc-grid .svc-body {
    font-size: 18px;
    line-height: 28px;
  }
  .icon-card.is-hot:not(.is-suppressed) .icon-card-stage,
  .icon-card:focus-within:not(.is-suppressed) .icon-card-stage,
  .icon-card.is-open:not(.is-suppressed) .icon-card-stage {
    opacity: 0;
    transition: opacity 160ms ease;
  }
  .icon-card.is-hot:not(.is-suppressed) .icon-card-panel,
  .icon-card:focus-within:not(.is-suppressed) .icon-card-panel,
  .icon-card.is-open:not(.is-suppressed) .icon-card-panel {
    opacity: 1;
    pointer-events: auto;
    transition: opacity 160ms ease;
  }
}
@media (hover: hover) and (pointer: fine) and (min-width: 761px) {
  .svc-grid { grid-template-columns: repeat(2, minmax(0, 368px)); }
}
@media (hover: hover) and (pointer: fine) and (min-width: 1280px) {
  .svc-grid { grid-template-columns: repeat(3, minmax(0, 368px)); }
}
@media (prefers-reduced-motion: reduce) {
  .icon-card-stage,
  .icon-card-panel,
  .svc-grid .svc-icon,
  .svc-word,
  .svc-grid .card,
  .icon-card.is-hot:not(.is-suppressed) .icon-card-stage,
  .icon-card.is-hot:not(.is-suppressed) .icon-card-panel,
  .icon-card:focus-within:not(.is-suppressed) .icon-card-stage,
  .icon-card:focus-within:not(.is-suppressed) .icon-card-panel,
  .icon-card.is-open:not(.is-suppressed) .icon-card-stage,
  .icon-card.is-open:not(.is-suppressed) .icon-card-panel {
    transition: none;
  }
}
.faq {
  list-style: none;
  margin: 0.6rem 0 1.4rem;
  padding: 0;
  border-bottom: 1px solid var(--rule);
}
.faq-item { border-top: 1px solid var(--rule); }
.faq-item > h3 { margin: 0; font: inherit; }
.faq-trigger {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
  width: 100%;
  min-height: 44px;
  padding: 0.75rem 0;
  text-align: left;
  color: var(--ink);
  cursor: auto;
  scroll-margin-top: 1rem;
}
.faq-icon { display: none; }
.faq-panel { display: grid; grid-template-rows: 1fr; }
.faq-answer { min-height: 0; overflow: hidden; }
.faq-answer > p { max-width: 27em; margin: 0; padding-bottom: 1rem; }
.faq-answer > p.quiet { color: var(--quiet); }
.faq-item:has(> h3 > [aria-expanded="false"]) > .faq-panel {
  grid-template-rows: 0fr;
  visibility: hidden;
}
.faq-live .faq-trigger { cursor: pointer; }
.faq-live .faq-icon {
  display: block;
  position: relative;
  flex: none;
  width: 24px;
  height: 24px;
  margin-top: calc(0.75em - 12px);
  transition: transform 200ms ease-out;
}
.faq-icon::before,
.faq-icon::after {
  content: "";
  position: absolute;
  left: 4px;
  top: calc(50% - 0.75px);
  width: 16px;
  height: 1.5px;
  background: currentColor;
}
.faq-icon::after { transform: rotate(90deg); }
.faq-live [aria-expanded="true"] > .faq-icon { transform: rotate(45deg); }
.faq-live .faq-panel { transition: grid-template-rows 200ms ease-out, visibility 200ms ease-out; }
@media (hover: hover) {
  .faq-live .faq-trigger:hover .faq-text {
    text-decoration-line: underline;
    text-decoration-thickness: 1px;
    text-underline-offset: 0.22em;
  }
}
@media (prefers-reduced-motion: reduce) {
  .faq-live .faq-item .faq-icon,
  .faq-live .faq-item .faq-panel { transition: none; }
}

"""
        portrait = ".portrait { margin: 0 0 1.4rem; max-width: 22rem; }"
        frame = ".frame { width: min(76rem, calc(100% - 1.25rem)); }"
        if portrait not in text or frame not in text:
            raise SystemExit("portrait cap or narrow frame gutter left the stylesheet")
        text = text.replace(
            portrait,
            f".portrait {{ margin: 0 0 1.4rem; max-width: {Site.PORTRAIT_MAX_REM}rem; }}",
            1,
        )
        text = text.replace(
            frame,
            f".frame {{ width: min(76rem, calc(100% - {Site.NARROW_FRAME_GUTTER_REM}rem)); }}",
            1,
        )
        photo = Site.media_row(Site.TEAM_PHOTO_ID)
        width, height = int(photo["width"]), int(photo["height"])
        team_photo = (
            ".team-photo img { display: block; width: 100%; max-width: 617px; "
            "height: auto; aspect-ratio: 617 / 462; }"
        )
        if team_photo not in text:
            raise SystemExit("team photo rule left the stylesheet")
        text = text.replace(
            team_photo,
            ".team-photo img { display: block; width: 100%; "
            f"max-width: {width}px; height: auto; aspect-ratio: {width} / {height}; }}",
            1,
        )
        return text

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
            rel_path = path.relative_to(Site.OUT)
            ups = "../" * (len(rel_path.parts) - 1)
            rel = str(rel_path)
            if rel == "404.html":
                expected = f' src="{Site.mount()}assets/menu.js"'
            else:
                expected = f' src="{ups}assets/menu.js"'
            if scripts != [expected]:
                problems.append(f"unexpected script in {rel}")
            if re.search(r"<script\b[^>]*>\s*[^<\s]", text, re.I):
                problems.append(f"inline script in {rel}")
            if "NACD" in text:
                nacd_files.append(str(path.relative_to(Site.OUT)))
            for phrase in Site.BANNED:
                if phrase not in lowered:
                    continue
                kept = rel in ("how-we-engage/index.html",) and phrase in ("72 hour", "within 72")
                if not kept:
                    problems.append(f"banned phrase {phrase!r} in {path}")
            for href in re.findall(r'href="([^"]*)"', text, re.I):
                if href.startswith("site:") or href.startswith("media:"):
                    problems.append(f"unexpanded ref {href} in {rel}")
                if "axoncyber.com" in href.casefold() and not href.casefold().startswith("mailto:"):
                    problems.append(f"old site href in {rel}")
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
        if "Internal Security Posture Assessment" in home or "Cyber Proactive Defense" in home:
            problems.append("internal or defense card is on home")
        for line in (
            "For security leaders and executive teams.",
            "You receive a secure third-party log review for espionage and unsignatured threats.",
            "For general counsel and security leaders who need to act on a finding.",
            "You receive discrete services, within U.S. and/or international law, that stop the attack.",
        ):
            if line not in caps:
                problems.append(f"missing card line {line!r}")
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
        who = Site.who_we_are()
        for slug, record in (("about", who.about), ("proof", who.proof)):
            html = Site.page_path(slug).read_text(encoding="utf-8")
            for text in Site._strings(record):
                if escape(text) not in html:
                    problems.append(f"{slug} is missing restored copy {text[:48]!r}")
        if who.about.leader.portrait["file"] not in about:
            problems.append("about is missing the leader portrait")
        team_photo = who.about.team.photo
        if team_photo["file"] not in about or 'alt="US-CERT team"' not in about:
            problems.append("about is missing the US-CERT team photo")
        if f"{Path(team_photo['file']).stem}-300.webp 300w" not in about:
            problems.append("about team photo is missing its 300w candidate")
        ceo = (Site.OUT / "our-ceo" / "index.html").read_text(encoding="utf-8")
        if 'http-equiv="refresh" content="0; url=../about/#leadership"' not in ceo:
            problems.append("our-ceo refresh is missing")
        if 'href="../about/#leadership"' not in ceo:
            problems.append("our-ceo link is missing")
        if "linkedin.com/in/israelmartinezcybersecurity" in ceo:
            problems.append("our-ceo still publishes the archived bio")
        sitemap_xml = (Site.OUT / "sitemap.xml").read_text(encoding="utf-8")
        if "our-ceo" in sitemap_xml:
            problems.append("sitemap lists our-ceo")
        not_found = (Site.OUT / "404.html").read_text(encoding="utf-8")
        mount = Site.mount()
        for needle in (
            f"{mount}assets/site.css",
            f"{mount}assets/menu.js",
            f"{mount}favicon.ico",
            f"{mount}favicon.svg",
            f"{mount}favicon-192.png",
            f"{mount}favicon-512.png",
            f"{mount}apple-touch-icon.png",
            f'href="{mount}"',
        ):
            if needle not in not_found:
                problems.append(f"404 missing {needle}")
        if "<base" in not_found:
            problems.append("404 contains a base tag")
        if f"{mount}assets/site.css" in home:
            problems.append("home stylesheet is mount-absolute")
        for slug, dest in (("faqs", "../faq/"), ("contact", "../engage/")):
            stub = (Site.OUT / slug / "index.html").read_text(encoding="utf-8")
            if f'http-equiv="refresh" content="0; url={dest}"' not in stub:
                problems.append(f"{slug} refresh is missing")
            if f'href="{dest}"' not in stub:
                problems.append(f"{slug} link is missing")
            if 'name="robots" content="noindex"' not in stub:
                problems.append(f"{slug} noindex is missing")
        if (Site.OUT / "assets" / "media" / "ceo-portrait.webp").exists():
            problems.append("ceo portrait still in site assets")
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
        if "safe harbor" not in "\n".join(Site.bundle()["faq_questions"]).casefold():
            problems.append("faq questions missing safe harbor")
        if "<!--" in faq or "Is cyber espionage something we should report?" in faq:
            problems.append("faq still ships the held-back questions")
        if "safe haven" not in fyi:
            problems.append("fyi missing safe haven")
        if "[poop]" in faq or "[fill in the blank]" in faq or "[ELT]" in faq or "[bad actors]" in faq:
            problems.append("faq still has editorial brackets")
        if "Would it stand up to review by your board, your regulator, or a court?" not in faq:
            problems.append("faq review question missing")
        if "General Counsel" not in faq or "Conducted" not in home:
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
            for icon_name in ("favicon.ico", "apple-touch-icon.png"):
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
                    if url.startswith("/"):
                        mount = Site.mount()
                        if not url.startswith(mount):
                            continue
                        image = (Site.OUT / url[len(mount):]).resolve()
                    else:
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
