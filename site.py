"""Axon Global Services static site.

One class. Static methods. Plain HTML, one stylesheet, one self-hosted grotesque.
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
        {"slug": "", "nav": "Home", "title": "Board brief", "home": True},
        {"slug": "capabilities", "nav": "Capabilities", "title": "Capabilities"},
        {"slug": "who", "nav": "Who it is for", "title": "Who it is for"},
        {"slug": "proof", "nav": "Proof", "title": "Proof"},
        {"slug": "authority", "nav": "Authority", "title": "Authority"},
        {"slug": "insights", "nav": "Insights", "title": "Insights"},
        {"slug": "about", "nav": "About", "title": "About"},
        {"slug": "engage", "nav": "Engage", "title": "Engage"},
        {"slug": "sitemap", "nav": None, "title": "Sitemap"},
    )

    OFFERINGS = (
        {
            "id": "training",
            "name": "Cyber Enterprise Risk Management Training",
            "card": "Cyber Enterprise Risk Management Training",
            "card_line": "For directors and the C-suite, on site or by webinar.",
            "home": True,
            "body": (
                "NACD-credentialed, on site or webinar. "
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
        "safe harbor",
        "safe haven",
        "liability shield",
        "127 unique",
        "127 benefit",
        "gdpr",
        "no one else",
        "18 differentiator",
        "18 material",
        "cage code",
        "uei:",
        "naics",
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
        "israel martinez",
        "over 150",
        "trained over",
        "over 200",
        "over 220",
        "220 of the",
        "300 executive",
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
        "2003",
        "8(a)",
        "secret service",
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
        css_path = Site.OUT / "assets" / "site.css"
        css_path.write_text(Site.css(), encoding="utf-8")
        (Site.OUT / "favicon.svg").write_text(Site.favicon(), encoding="utf-8")
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
        shown = [page for page in Site.PAGES if page["nav"]]
        for index, page in enumerate(shown, start=1):
            if page["slug"] == slug:
                return f"{index:02d}"
        return ""

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
    def wordmark(slug: str) -> str:
        return (
            f'<a class="wordmark" href="{Site.href(slug, "")}">'
            f"{Site.mark(False)}"
            '<span class="wordmark-type">'
            '<span class="wordmark-name">Axon</span>'
            '<span class="wordmark-line">Global Services</span>'
            "</span></a>"
        )

    @staticmethod
    def document(page: dict, main: str) -> str:
        slug = page["slug"]
        title = escape(page["title"])
        body_class = ' class="opening"' if page.get("home") else ""
        depth = "" if slug == "" else "../"
        description = escape(
            "Axon Global Services. Board training and pre-emptive cyber risk work."
        )
        csp = (
            "default-src 'self'; base-uri 'none'; object-src 'none'; "
            "form-action 'none'; script-src 'none'; style-src 'self'; "
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
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Axon Global Services</title>
<meta name="description" content="{description}">
<meta name="referrer" content="no-referrer">
<meta http-equiv="Content-Security-Policy" content="{csp}">
<meta name="color-scheme" content="light">
<meta name="theme-color" content="#0e0d0b">
<link rel="canonical" href="{escape(Site.canonical(slug))}">
<link rel="icon" href="{depth}favicon.svg" type="image/svg+xml">
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
<nav class="nav" aria-label="Pages">{Site.nav(slug)}</nav>
</div>
</header>
<main id="content">
{content}
</main>
<footer class="colophon">
<div class="frame foot">
<div class="foot-brand">{Site.wordmark(slug)}</div>
<nav class="foot-nav" aria-label="Footer">{Site.nav(slug)}</nav>
<div class="foot-side">
<p class="quiet">Secondary</p>
<p><a href="tel:+12022485050">{Site.PHONE}</a></p>
<p><a href="mailto:{Site.EMAIL}">{Site.EMAIL}</a></p>
<p class="foot-action">{Site.action_link()}</p>
</div>
<div class="foot-legal">
<p>© 2026 Axon Global Services</p>
<p><a href="{Site.href(slug, "sitemap")}">Sitemap</a></p>
</div>
</div>
</footer>
</div>
</body>
</html>
"""

    @staticmethod
    def nav(slug: str) -> str:
        parts = []
        for page in Site.PAGES:
            if not page["nav"]:
                continue
            current = ' aria-current="page"' if page["slug"] == slug else ""
            parts.append(
                f'<a href="{Site.href(slug, page["slug"])}"{current}>{escape(page["nav"])}</a>'
            )
        return "".join(parts)

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
            "proof": Site.proof_body,
            "authority": Site.authority_body,
            "insights": Site.insights_body,
            "about": Site.about_body,
            "engage": Site.engage_body,
            "sitemap": Site.sitemap_body,
        }
        return writers[slug](slug)

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
                f'<p class="idx">{index:02d}</p>'
                f'<h3><a href="capabilities/#{escape(offer["id"])}">{escape(offer["card"])}</a></h3>'
                f"<p>{escape(offer['card_line'])}</p>"
                "</li>"
            )
        slots = ("Record", "Credential", "Outcome")
        strip = "".join(
            "<li>"
            f'<p class="slot">Slot</p>'
            f"<p>{escape(label)}</p>"
            "</li>"
            for label in slots
        )
        return f"""
<section class="hero">
<div class="frame">
<div class="hero-grid">
<h1 class="hero-title">Board<br>brief</h1>
<div class="hero-mark">{Site.mark(True)}</div>
<div class="hero-facts">
<dl>
<dt>Buyer</dt>
<dd>Fortune 500 boards, general counsel, CISOs and executive teams, private equity, and government or critical-infrastructure readers.</dd>
<dt>Deliverable</dt>
<dd>Board training and pre-emptive cyber risk work.</dd>
</dl>
<p class="hero-action">{Site.action_link()}</p>
</div>
</div>
</div>
</section>
<div class="paper">
<div class="frame">
{Site.row("01", "Proof", f'<ul class="strip">{strip}</ul>')}
{Site.row("02", "Services", f'<ol class="cards">{"".join(cards)}</ol>')}
</div>
</div>
"""

    @staticmethod
    def capabilities_body(_slug: str) -> str:
        blocks = []
        for index, offer in enumerate(Site.OFFERINGS, start=1):
            blocks.append(
                f'<li class="offering" id="{escape(offer["id"])}">'
                f'<p class="idx">{index:02d}</p>'
                f"<h2>{escape(offer['name'])}</h2>"
                f"<p>{escape(offer['body'])}</p>"
                "</li>"
            )
        rows = []
        for offer in Site.OFFERINGS:
            home = "Yes" if offer["home"] else "No"
            rows.append(
                "<tr>"
                f"<td>{escape(offer['name'])}</td>"
                f'<td><a href="{escape(Site.SOURCE)}">{escape(Site.SOURCE)}</a></td>'
                f"<td>{home}</td>"
                "</tr>"
            )
        table = (
            '<div class="table-wrap"><table>'
            "<caption>Each offering and the page that names it.</caption>"
            "<thead><tr><th>Offering</th><th>Source URL</th><th>Home card</th></tr></thead>"
            f"<tbody>{''.join(rows)}</tbody></table></div>"
        )
        return f"""
<h1>Capabilities</h1>
<p class="lede">Eight lines of board training and pre-emptive cyber risk work.</p>
<ol class="offerings">{"".join(blocks)}</ol>
{Site.row("09", "Source map", table)}
<p class="end-action">{Site.action_link()}</p>
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
        return f"""
<h1>Who it is for</h1>
<p class="lede">Five readers. The work is board training and pre-emptive cyber risk assessment.</p>
{"".join(blocks)}
<p class="end-action">{Site.action_link()}</p>
"""

    @staticmethod
    def proof_body(_slug: str) -> str:
        slots = (
            "Record",
            "Credential",
            "Outcome",
            "Names",
            "Counts",
            "Timing",
            "Identifiers",
        )
        items = "".join(
            f'<li><p class="slot">Slot</p><p>{escape(line)}</p></li>' for line in slots
        )
        return f"""
<h1>Proof</h1>
<p class="lede">Record, credential, and outcome.</p>
<ul class="slots">{items}</ul>
<p class="end-action">{Site.action_link()}</p>
"""

    @staticmethod
    def authority_body(_slug: str) -> str:
        return f"""
<h1>Authority</h1>
<div class="slot-page">
<p class="slot">Slot</p>
<p>Letters, memberships, and appointments.</p>
</div>
<p class="end-action">{Site.action_link()}</p>
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
<p class="end-action">{Site.action_link()}</p>
"""

    @staticmethod
    def about_body(_slug: str) -> str:
        slots = "".join(
            f'<li><p class="slot">Slot {number:02d}</p><p>Practitioner</p></li>'
            for number in (1, 2, 3)
        )
        return f"""
<h1>About</h1>
<p class="lede">Axon Global Services prepares board training and pre-emptive cyber risk work for the readers on Who it is for.</p>
<p>Phone, email, and the street address are on Engage.</p>
{Site.row("01", "Practitioners", f'<ul class="slots">{slots}</ul>')}
<p class="end-action">{Site.action_link()}</p>
"""

    @staticmethod
    def engage_body(_slug: str) -> str:
        secondary = (
            "<dl class=\"brief\">"
            "<dt>Phone</dt>"
            f'<dd><a href="tel:+12022485050">{Site.PHONE}</a></dd>'
            "<dt>Email</dt>"
            f'<dd><a href="mailto:{Site.EMAIL}">{Site.EMAIL}</a></dd>'
            "<dt>Address</dt>"
            "<dd>10 G St. NE, Suite 600<br>Washington, DC 20002</dd>"
            "</dl>"
        )
        return f"""
<h1>{Site.ACTION}</h1>
<p class="lede">The briefing request opens an email.</p>
{Site.row("01", "Briefing", f'<p id="request">{Site.action_link()}</p>')}
{Site.row("02", "Secondary", secondary)}
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
<p class="end-action">{Site.action_link()}</p>
"""

    @staticmethod
    def missing_body() -> str:
        return f"""
<h1>Not found</h1>
<p class="lede">This page is not on the site.</p>
<p><a href="./">Home</a></p>
<p class="end-action">{Site.action_link()}</p>
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
a:focus-visible { outline: 1px solid var(--signal); outline-offset: 3px; }
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
  gap: 0.15rem 0.35rem;
  border-top: 1px solid var(--rule-dark);
  padding: 0.2rem 0 0.35rem;
}
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
  min-height: calc(100svh - 8.75rem);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0.6rem 0 1.5rem;
  background: var(--ink);
  color: var(--bone);
}
.hero > .frame {
  display: flex;
  flex: 1;
}
.hero-grid {
  flex: 1;
  display: grid;
  grid-template-columns: minmax(0, 1.05fr) minmax(16rem, 0.95fr);
  grid-template-areas:
    "title mark"
    "facts mark";
  gap: 1.25rem 3rem;
  align-items: stretch;
}
.hero-title {
  grid-area: title;
  align-self: end;
  margin: 0;
  font-weight: 560;
  font-size: clamp(3.6rem, 6.6vw, 6.75rem);
  letter-spacing: -0.045em;
  line-height: 0.86;
}
.hero-mark {
  grid-area: mark;
  display: flex;
  align-items: stretch;
  justify-content: flex-end;
  min-height: 0;
}
.hero-facts {
  grid-area: facts;
  align-self: end;
  max-width: 38rem;
}
.hero-facts dl {
  display: grid;
  grid-template-columns: 7.25rem minmax(0, 1fr);
  gap: 0.85rem 1.15rem;
  margin: 0 0 1.1rem;
}
.hero-facts dt {
  margin: 0;
  padding-top: 0.2rem;
  font-size: 0.72rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--quiet-dark);
}
.hero-facts dd { margin: 0; }
.hero-action { margin: 0; }
.mark-lg { width: 100%; height: 100%; max-height: calc(100svh - 11rem); }
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
@media (max-width: 800px) {
  .frame { width: min(76rem, calc(100% - 1.5rem)); }
  .mast-top { grid-template-columns: 1fr auto; min-height: 0; padding-top: 0.85rem; }
  .mast-action { grid-column: 1 / -1; }
  .hero { min-height: 0; padding-bottom: 1.75rem; }
  .hero-grid {
    grid-template-columns: 1fr;
    grid-template-areas:
      "title"
      "mark"
      "facts";
    gap: 1.25rem;
  }
  .hero-title { font-size: clamp(3.35rem, 16vw, 4.6rem); }
  .hero-mark { justify-content: flex-start; }
  .mark-lg { width: min(100%, 22rem); height: auto; max-height: none; }
  .hero-facts dl { grid-template-columns: 1fr; gap: 0.2rem; }
  .hero-facts dd { margin-bottom: 0.85rem; }
  .offerings { grid-template-columns: 1fr; }
  .offering { min-height: 0; }
  .page h1 { max-width: none; font-size: clamp(2.7rem, 12vw, 3.5rem); padding-top: 1.7rem; }
  .row { grid-template-columns: 1fr; gap: 0.25rem; padding: 1.5rem 0; }
  .strip, .cards, .slots { grid-template-columns: 1fr; }
  .strip li, .card, .slots li { min-height: 0; }
  .brief { grid-template-columns: 1fr; }
  .foot { grid-template-columns: 1fr; padding-top: 2.2rem; }
  .foot-legal { flex-direction: column; }
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
            if re.search(r"<script", text, re.I):
                problems.append(f"script in {path}")
            if "NACD" in text:
                nacd_files.append(str(path.relative_to(Site.OUT)))
            for phrase in Site.BANNED:
                if phrase in lowered:
                    problems.append(f"banned phrase {phrase!r} in {path}")
            for name in Site.CLIENTS:
                if name in lowered:
                    problems.append(f"client name {name!r} in {path}")
            for token in ("dell", "ford", "intel", "google", "walmart", "target", "delta", "usg"):
                if re.search(rf"\b{token}\b", lowered):
                    problems.append(f"client token {token!r} in {path}")
        if nacd_files != ["capabilities/index.html"]:
            problems.append(f"NACD appears in {nacd_files}")
        caps = (Site.OUT / "capabilities" / "index.html").read_text(encoding="utf-8")
        if caps.count("NACD-credentialed") != 1:
            problems.append("NACD-credentialed count is not 1")
        if re.search(r"<h[1-6][^>]*>[^<]*NACD", caps):
            problems.append("NACD appears in a heading")
        blob = "\n".join(blob_parts).casefold()
        for page in Site.PAGES:
            if page["nav"] and page["nav"].casefold() not in blob:
                problems.append(f"missing nav label {page['nav']}")
        if (Site.ROOT / "CNAME").exists() or (Site.OUT / "CNAME").exists():
            problems.append("CNAME present")
        home = (Site.OUT / "index.html").read_text(encoding="utf-8")
        for needle in ("Buyer", "Deliverable", "Services", Site.ACTION):
            if needle not in home:
                problems.append(f"home missing {needle}")
        if home.count('class="card"') != 6:
            problems.append("home card count is not 6")
        if "gtag" in blob or "google-analytics" in blob or "plausible" in blob:
            problems.append("analytics marker")
        for offer in Site.OFFERINGS:
            if escape(offer["name"]) not in caps:
                problems.append(f"missing offering {offer['name']}")
        if caps.count(Site.SOURCE) < 8:
            problems.append("source map incomplete")
        proof = (Site.OUT / "proof" / "index.html").read_text(encoding="utf-8")
        if proof.count("<blockquote") or proof.count(">Slot<") < 1:
            problems.append("proof is not slots only")
        authority = (Site.OUT / "authority" / "index.html").read_text(encoding="utf-8")
        if authority.count(">Slot<") < 1:
            problems.append("authority is not a slot")
        about = (Site.OUT / "about" / "index.html").read_text(encoding="utf-8")
        if about.count("Slot 0") < 3:
            problems.append("practitioner slots missing")
        css = (Site.OUT / "assets" / "site.css").read_text(encoding="utf-8")
        if re.search(r"url\(\s*https?:", css):
            problems.append("stylesheet requests a third party")
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
        icon = (Site.OUT / "favicon.svg").stat().st_size
        font = (Site.OUT / "assets" / "fonts" / "libre-franklin-latin.woff2").stat().st_size
        limit = 1_048_576
        rows = []
        for path in sorted(Site.OUT.rglob("*.html")):
            html_bytes = path.stat().st_size
            total = html_bytes + css + icon + font
            rows.append(
                {
                    "path": str(path.relative_to(Site.OUT)),
                    "html_bytes": html_bytes,
                    "css_bytes": css,
                    "font_bytes": font,
                    "image_bytes": icon,
                    "js_bytes": 0,
                    "total_bytes": total,
                    "limit_bytes": limit,
                    "under_limit": total < limit,
                }
            )
        return {
            "method": "Uncompressed bytes of the HTML file plus the shared stylesheet, the self-hosted font, and the SVG mark.",
            "limit_bytes": limit,
            "pages": rows,
        }


if __name__ == "__main__":
    raise SystemExit(Site.build())
