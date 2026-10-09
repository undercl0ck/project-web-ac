"""Axon Global Services static site.

The private repo undercl0ck/golden-ratio-web-design was not readable
(GitHub API 404; not in the owner's visible repo list). This file is the
fallback: one class, static methods, plain HTML and one stylesheet.
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
            "name": "Cyber Enterprise Risk Management Training (NACD-credentialed, on site or webinar)",
            "card": "Cyber Enterprise Risk Management Training",
            "card_line": "For directors and the C-suite, on site or by webinar.",
            "home": True,
            "body": (
                "For board members or C-suite executives, on site or by webinar. "
                "The prior page says the experts are NACD-credentialed. "
                "That wording is tagged unverified and is not stated as fact."
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

    UNVERIFIED = (
        {
            "line": 'why customer surveys consistently score our cyber risk briefings as "9.5 out of 10".',
            "url": "https://axoncyber.com/",
        },
        {
            "line": "National Association of Corporate Directors (NACD), Full Board Members, and Faculty",
            "url": "https://axoncyber.com/who-we-are/",
        },
        {
            "line": "NACD® as a Board Leadership Fellow",
            "url": "https://axoncyber.com/our-ceo-global-cto/",
        },
        {
            "line": "Recognized by the U.S. Secret Service and the Department of Homeland Security (DHS)",
            "url": "https://axoncyber.com/who-we-are/",
        },
        {
            "line": "Hence, we are recognized by the U.S. Secret Service as leaders in our field.",
            "url": "https://axoncyber.com/what-we-do/",
        },
        {
            "line": "DHS certified in Cyber Counter Terrorism and Defense",
            "url": "https://axoncyber.com/who-we-are/",
        },
        {
            "line": "Founded in 2003",
            "url": "https://axoncyber.com/who-we-are/",
        },
        {
            "line": "graduate of the Federally Certified 8(a) program",
            "url": "https://axoncyber.com/who-we-are/",
        },
        {
            "line": (
                "Axon is also executing critical infrastructure security cyber-monitoring; "
                "threat intelligence; and defending critical infrastructure under The Task Force "
                "on National and Homeland Security, established under a bi-partisan U.S. Congressional Committee."
            ),
            "url": "https://axoncyber.com/who-we-are/",
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
        css_path = Site.OUT / "assets" / "site.css"
        css_path.parent.mkdir(parents=True, exist_ok=True)
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
    def asset(from_slug: str, name: str) -> str:
        prefix = "" if from_slug == "" else "../"
        return prefix + name

    @staticmethod
    def canonical(slug: str) -> str:
        if slug == "":
            return Site.ORIGIN
        return Site.ORIGIN + slug + "/"

    @staticmethod
    def action_link() -> str:
        return f'<a class="action" href="{Site.MAILTO}">{Site.ACTION}</a>'

    @staticmethod
    def document(page: dict, main: str) -> str:
        slug = page["slug"]
        title = escape(page["title"])
        depth = "" if slug == "" else "../"
        body_class = ' class="opening"' if page.get("home") else ""
        nav = Site.nav(slug)
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
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Axon Global Services</title>
<meta name="description" content="{description}">
<meta name="referrer" content="no-referrer">
<meta http-equiv="Content-Security-Policy" content="{csp}">
<meta http-equiv="X-Content-Type-Options" content="nosniff">
<meta name="color-scheme" content="light">
<link rel="canonical" href="{escape(Site.canonical(slug))}">
<link rel="icon" href="{depth}favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{depth}assets/site.css">
</head>
<body{body_class}>
<a class="skip" href="#content">Skip to content</a>
<div class="wrap">
<header class="mast">
<p class="brand"><a href="{Site.href(slug, "")}">Axon Global Services</a></p>
<nav class="nav" aria-label="Pages">{nav}</nav>
<p class="mast-action">{Site.action_link()}</p>
</header>
<main id="content">
{main}
</main>
<footer class="colophon">
<p class="secondary">Secondary <a href="tel:+12022485050">{Site.PHONE}</a> <a href="mailto:{Site.EMAIL}">{Site.EMAIL}</a></p>
<p><a href="{Site.href(slug, "sitemap")}">Sitemap</a></p>
<p>© 2026 Axon Global Services</p>
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
                "<li class=\"card\">"
                f'<p class="idx">{index:02d}</p>'
                f'<h3><a href="capabilities/#{escape(offer["id"])}">{escape(offer["card"])}</a></h3>'
                f'<p>{escape(offer["card_line"])}</p>'
                "</li>"
            )
        slots = (
            ("Record", "Slot", "No claim"),
            ("Credential", "Slot", "No claim"),
            ("Outcome", "Slot", "No claim"),
        )
        strip = []
        for label, value, note in slots:
            strip.append(
                "<li>"
                f"<p>{escape(label)}</p>"
                f"<p class=\"slot\">{escape(value)}</p>"
                f"<p class=\"quiet\">{escape(note)}</p>"
                "</li>"
            )
        return f"""
<p class="kicker">Axon Global Services</p>
<h1>Board brief</h1>
<div class="open-rule" aria-hidden="true"></div>
<dl class="brief">
<dt>Buyer</dt>
<dd>Fortune 500 boards, general counsel, CISOs and executive teams, private equity, and government or critical-infrastructure readers.</dd>
<dt>Deliverable</dt>
<dd>Board training and pre-emptive cyber risk work.</dd>
<dt>Action</dt>
<dd>{Site.action_link()}</dd>
</dl>
<h2>Proof</h2>
<ul class="strip">
{"".join(strip)}
</ul>
<h2>Services</h2>
<ol class="cards">
{"".join(cards)}
</ol>
"""

    @staticmethod
    def capabilities_body(slug: str) -> str:
        blocks = []
        for offer in Site.OFFERINGS:
            tag = ""
            if offer["id"] == "training":
                tag = '<p class="tag">Unverified — NACD credential wording</p>'
            blocks.append(
                f'<section id="{escape(offer["id"])}">'
                f'<h2>{escape(offer["name"])}</h2>'
                f"{tag}"
                f'<p>{escape(offer["body"])}</p>'
                "</section>"
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
        return f"""
<h1>Capabilities</h1>
<p class="lede">Eight offerings. The list matches the prior engagement page. Nothing was added.</p>
{"".join(blocks)}
<h2>Source map</h2>
<div class="table-wrap">
<table>
<caption>Each offering, the page that names it, and whether the home brief shows it.</caption>
<thead><tr><th>Offering</th><th>Source URL</th><th>Home card</th></tr></thead>
<tbody>
{"".join(rows)}
</tbody>
</table>
</div>
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
        items = []
        for title, line in rows:
            items.append(f"<li><h2>{escape(title)}</h2><p>{escape(line)}</p></li>")
        return f"""
<h1>Who it is for</h1>
<p class="lede">Five readers. The work is board training and pre-emptive cyber risk assessment.</p>
<ol class="readers">
{"".join(items)}
</ol>
<p class="end-action">{Site.action_link()}</p>
"""

    @staticmethod
    def proof_body(_slug: str) -> str:
        claims = []
        for item in Site.UNVERIFIED:
            claims.append(
                "<article class=\"claim\">"
                '<p class="tag">Unverified</p>'
                f"<blockquote>{escape(item['line'])}</blockquote>"
                f'<p class="quiet">Prior-site line. Date seen Oct 9, 2026. <a href="{escape(item["url"])}">{escape(item["url"])}</a></p>'
                "</article>"
            )
        slots = (
            "Client names. Slot. No name is printed.",
            "Outcome figures. Slot. No figure is printed.",
            "Training counts. Slot. No count is printed.",
            "Delivery timing. Slot. No hour count is printed.",
            "Corporate identifiers and contract vehicles. Slot. Not printed.",
        )
        slot_html = "".join(f"<li><p class=\"slot\">Slot</p><p>{escape(line)}</p></li>" for line in slots)
        return f"""
<h1>Proof</h1>
<p class="lede">Lines below are prior-site wording. Each one is tagged unverified. They are not findings of this site.</p>
{"".join(claims)}
<h2>Slots</h2>
<ul class="slots">
{slot_html}
</ul>
<p class="end-action">{Site.action_link()}</p>
"""

    @staticmethod
    def authority_body(_slug: str) -> str:
        return f"""
<h1>Authority</h1>
<div class="slot-page">
<p class="slot">Slot</p>
<p>Recognition letters, memberships, faculty appointments, and agency records are not printed on this page.</p>
<p>When a record is ready to publish, it replaces this slot. Until then the slot is empty.</p>
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
        for note in notes:
            sources = "".join(
                f'<li><a href="{escape(url)}">{escape(label)}</a></li>'
                for label, url in note["sources"]
            )
            blocks.append(
                "<article class=\"note\">"
                '<p class="kicker">Board note</p>'
                f"<h2>{escape(note['title'])}</h2>"
                f"<p>{escape(note['body'])}</p>"
                f"<ul class=\"sources\">{sources}</ul>"
                '<p class="quiet">Not an Axon finding.</p>'
                "</article>"
            )
        return f"""
<h1>Insights</h1>
<p class="lede">Short board notes. Each one is a reading of a public document.</p>
{"".join(blocks)}
<p class="end-action">{Site.action_link()}</p>
"""

    @staticmethod
    def about_body(_slug: str) -> str:
        slots = []
        for number in (1, 2, 3):
            slots.append(
                "<li>"
                f"<p class=\"slot\">Slot {number:02d}</p>"
                "<p>Name and biography are not published.</p>"
                "</li>"
            )
        return f"""
<h1>About</h1>
<p class="lede">Axon Global Services prepares board training and pre-emptive cyber risk work for the readers on Who it is for.</p>
<p>Phone, email, and the published street address are on Engage.</p>
<h2>Practitioners</h2>
<ul class="slots">
{"".join(slots)}
</ul>
<p class="end-action">{Site.action_link()}</p>
"""

    @staticmethod
    def engage_body(_slug: str) -> str:
        return f"""
<h1>{Site.ACTION}</h1>
<p class="lede">The request opens an email. This page has no form and does not store a name, a message, or a visit.</p>
<p class="end-action" id="request">{Site.action_link()}</p>
<h2>Secondary</h2>
<dl class="brief">
<dt>Phone</dt>
<dd><a href="tel:+12022485050">{Site.PHONE}</a></dd>
<dt>Email</dt>
<dd><a href="mailto:{Site.EMAIL}">{Site.EMAIL}</a></dd>
<dt>Address</dt>
<dd>10 G St. NE, Suite 600<br>Washington, DC 20002<p class="quiet">As printed on the prior capabilities page.</p></dd>
</dl>
"""

    @staticmethod
    def sitemap_body(slug: str) -> str:
        items = []
        for page in Site.PAGES:
            if page["slug"] == "sitemap":
                continue
            items.append(
                f'<li><a href="{Site.href(slug, page["slug"])}">{escape(page["title"])}</a></li>'
            )
        items.append("<li><a href=\"./\" aria-current=\"page\">Sitemap</a></li>")
        return f"""
<h1>Sitemap</h1>
<ul class="map">
{"".join(items)}
</ul>
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
            '<rect width="32" height="32" fill="#f4f1ea"/>'
            '<path d="M6 16h20" stroke="#141311" stroke-width="1"/>'
            "</svg>\n"
        )

    @staticmethod
    def css() -> str:
        return """:root {
  --bone: #f4f1ea;
  --ink: #141311;
  --quiet: #5c574e;
  --signal: #8e2f2c;
  --rule: rgba(20, 19, 17, 0.28);
}
* { box-sizing: border-box; }
html { background: var(--bone); color: var(--ink); }
body {
  margin: 0;
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
  font-size: 1.0625rem;
  line-height: 1.45;
  font-weight: 400;
  background: var(--bone);
  color: var(--ink);
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
  z-index: 2;
}
.wrap {
  width: min(68rem, calc(100% - 3rem));
  margin: 0 auto;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
main { flex: 1; padding-bottom: 3rem; }
a { color: inherit; }
a:focus-visible { outline: 1px solid var(--signal); outline-offset: 3px; }
.mast {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: baseline;
  gap: 0.65rem 1.25rem;
  padding: 1.1rem 0 0;
  margin-bottom: 1.75rem;
}
.brand { margin: 0; font-size: 0.95rem; letter-spacing: 0.01em; order: 1; }
.brand a { text-decoration: none; }
.mast-action { order: 2; margin: 0; }
.nav {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem 0.9rem;
  order: 3;
  flex: 1 0 100%;
  border-bottom: 1px solid var(--ink);
  padding: 0.15rem 0 0.75rem;
}
.nav a {
  text-decoration: none;
  font-size: 0.78rem;
  letter-spacing: 0.03em;
}
.nav a[aria-current="page"] { border-bottom: 1px solid var(--ink); }
.action {
  color: var(--signal);
  text-decoration: none;
  border-bottom: 1px solid var(--signal);
  font-weight: 500;
}
.kicker {
  margin: 0 0 0.4rem;
  font-size: 0.72rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}
h1 {
  margin: 0;
  font-weight: 500;
  font-size: 2.6rem;
  letter-spacing: -0.03em;
  line-height: 1.05;
}
body:not(.opening) h1 {
  border-bottom: 1px solid var(--ink);
  padding-bottom: 0.75rem;
}
h2 {
  margin: 0 0 0.7rem;
  font-size: 0.72rem;
  font-weight: 500;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}
h3 { margin: 0 0 0.4rem; font-size: 1.05rem; font-weight: 500; line-height: 1.25; }
h3 a { text-decoration: none; }
p { margin: 0 0 0.8rem; }
.lede { max-width: 38rem; margin: 1rem 0 1.6rem; }
.open-rule {
  height: 1px;
  background: var(--ink);
  margin: 0.85rem 0 1.2rem;
  transform-origin: left center;
  animation: draw 0.9s cubic-bezier(.2, .7, .2, 1) 1 both;
}
@keyframes draw {
  from { transform: scaleX(0); }
  to { transform: scaleX(1); }
}
@media (prefers-reduced-motion: reduce) {
  .open-rule { animation: none; }
}
.brief {
  display: grid;
  grid-template-columns: 8.5rem 1fr;
  gap: 0.85rem 1.25rem;
  margin: 0 0 2rem;
  max-width: 44rem;
}
.brief dt {
  margin: 0;
  padding-top: 0.2rem;
  font-size: 0.72rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}
.brief dd { margin: 0; }
.strip, .cards, .readers, .slots, .map, .sources {
  list-style: none;
  margin: 0;
  padding: 0;
}
.strip, .cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
}
.strip { border-top: 1px solid var(--ink); margin-bottom: 2.25rem; }
.strip li, .card {
  border-right: 1px solid var(--ink);
  border-bottom: 1px solid var(--ink);
  padding: 0.9rem 1rem 1.1rem;
  margin: 0;
}
.strip li:nth-child(3n + 1), .card:nth-child(3n + 1) { border-left: 1px solid var(--ink); }
.cards { margin-bottom: 0.5rem; }
.card p { margin: 0; }
.idx, .quiet { color: var(--quiet); font-size: 0.82rem; }
.idx { margin-bottom: 0.7rem; letter-spacing: 0.08em; }
.slot { font-size: 0.72rem; letter-spacing: 0.14em; text-transform: uppercase; margin-bottom: 0.35rem; }
.tag {
  color: var(--signal);
  font-size: 0.72rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  margin-bottom: 0.35rem;
}
section { padding: 1.15rem 0; border-top: 1px solid var(--rule); }
section h2 {
  font-size: 1.15rem;
  letter-spacing: 0;
  text-transform: none;
  font-weight: 500;
  line-height: 1.3;
}
.readers li, .slots li, .claim, .note {
  border-top: 1px solid var(--ink);
  padding: 1rem 0 1.1rem;
}
.readers h2, .note h2 {
  font-size: 1.15rem;
  letter-spacing: 0;
  text-transform: none;
  font-weight: 500;
}
.claim blockquote {
  margin: 0 0 0.45rem;
  font-size: 1.02rem;
}
.sources { margin: 0.3rem 0 0.6rem; }
.sources li { margin: 0.2rem 0; }
.sources a, .table-wrap a, .quiet a { overflow-wrap: anywhere; }
.table-wrap { overflow-x: auto; border-top: 1px solid var(--ink); }
table { width: 100%; border-collapse: collapse; font-size: 0.92rem; }
caption { text-align: left; caption-side: bottom; color: var(--quiet); font-size: 0.82rem; padding: 0.6rem 0; }
th, td {
  text-align: left;
  vertical-align: top;
  padding: 0.7rem 0.6rem 0.7rem 0;
  border-bottom: 1px solid var(--rule);
  font-weight: 400;
}
th { font-size: 0.72rem; letter-spacing: 0.08em; text-transform: uppercase; }
.slot-page {
  border-top: 1px solid var(--ink);
  border-bottom: 1px solid var(--ink);
  padding: 1.25rem 0;
  margin: 1.2rem 0 1.5rem;
  max-width: 36rem;
}
.end-action { margin-top: 1.8rem; }
.map li { padding: 0.45rem 0; border-bottom: 1px solid var(--rule); }
.colophon {
  border-top: 1px solid var(--ink);
  padding: 1rem 0 1.4rem;
  color: var(--quiet);
  font-size: 0.85rem;
}
.colophon p { margin: 0.2rem 0; }
.secondary a { color: var(--quiet); }
@media (max-width: 800px) {
  .strip, .cards { grid-template-columns: 1fr; }
  .strip li, .card { border-left: 1px solid var(--ink); }
}
@media (max-width: 480px) {
  .wrap { width: min(68rem, calc(100% - 1.4rem)); }
  h1 { font-size: 1.85rem; }
  .brief { grid-template-columns: 1fr; gap: 0.15rem; }
  .brief dd { margin-bottom: 0.85rem; }
}
"""

    @staticmethod
    def audit() -> list[str]:
        problems = []
        html_files = sorted(Site.OUT.rglob("*.html"))
        if len(html_files) < 9:
            problems.append(f"expected at least 9 html files, found {len(html_files)}")
        blob_parts = []
        required = [page["nav"] for page in Site.PAGES if page["nav"]]
        for path in html_files:
            text = path.read_text(encoding="utf-8")
            blob_parts.append(text)
            if "<form" in text.lower():
                problems.append(f"form in {path.name}")
            if Site.ACTION not in text:
                problems.append(f"missing action in {path}")
            if "content-security-policy" not in text.lower():
                problems.append(f"missing csp in {path}")
            if 'name="referrer" content="no-referrer"' not in text:
                problems.append(f"missing referrer policy in {path}")
            if re.search(r"<script", text, re.I):
                problems.append(f"script in {path}")
            lowered = text.casefold()
            for phrase in Site.BANNED:
                if phrase in lowered:
                    problems.append(f"banned phrase {phrase!r} in {path}")
            for name in Site.CLIENTS:
                if name in lowered:
                    problems.append(f"client name {name!r} in {path}")
            for token in ("dell", "ford", "intel", "google", "walmart", "target", "delta", "usg"):
                if re.search(rf"\b{token}\b", lowered):
                    problems.append(f"client token {token!r} in {path}")
        blob = "\n".join(blob_parts).casefold()
        for label in required:
            if label.casefold() not in blob:
                problems.append(f"missing nav label {label}")
        if (Site.ROOT / "CNAME").exists() or (Site.OUT / "CNAME").exists():
            problems.append("CNAME present")
        home = (Site.OUT / "index.html").read_text(encoding="utf-8")
        for needle in ("Buyer", "Deliverable", "No claim", "Services"):
            if needle not in home:
                problems.append(f"home missing {needle}")
        if home.count('class="card"') != 6:
            problems.append("home card count is not 6")
        if "gtag" in blob or "google-analytics" in blob or "plausible" in blob:
            problems.append("analytics marker")
        caps = (Site.OUT / "capabilities" / "index.html").read_text(encoding="utf-8")
        for offer in Site.OFFERINGS:
            if escape(offer["name"]) not in caps:
                problems.append(f"missing offering {offer['name']}")
        if caps.count(Site.SOURCE) < 8:
            problems.append("source map incomplete")
        proof = (Site.OUT / "proof" / "index.html").read_text(encoding="utf-8")
        if proof.count(">Unverified<") < len(Site.UNVERIFIED):
            problems.append("proof tags missing")
        authority = (Site.OUT / "authority" / "index.html").read_text(encoding="utf-8")
        if authority.count(">Slot<") < 1:
            problems.append("authority is not a slot")
        about = (Site.OUT / "about" / "index.html").read_text(encoding="utf-8")
        if about.count("not published") < 3:
            problems.append("practitioner slots missing")
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
            "https": "github.io Pages sites are served over HTTPS. This repo ships no CNAME, so the host stays a github.io name, where GitHub enforces HTTPS.",
            "set_in_html": [
                "Content-Security-Policy via meta http-equiv",
                "referrer policy via meta name=referrer (no-referrer)",
                "X-Content-Type-Options via meta http-equiv (browsers do not reliably honor this meta; it is a marker only)",
            ],
            "github_pages_response_observed": {
                "sample": "https://undercl0ck.github.io/gregs-hvac/ on Oct 9, 2026",
                "present": [
                    "strict-transport-security: max-age=31556952",
                    "access-control-allow-origin: *",
                    "cache-control",
                ],
                "absent_on_that_response": [
                    "content-security-policy",
                    "referrer-policy",
                    "x-frame-options",
                    "x-content-type-options",
                    "permissions-policy",
                    "cross-origin-opener-policy",
                    "cross-origin-resource-policy",
                    "cross-origin-embedder-policy",
                ],
            },
            "github_pages_cannot_set": [
                "Custom HTTP response headers. Pages has no _headers file and no per-repo header config.",
                "Content-Security-Policy as an HTTP header. The meta element is the available control. Meta CSP ignores frame-ancestors, sandbox, report-uri, and report-to, so those cannot be enforced here.",
                "Referrer-Policy as an HTTP header. The meta referrer element is the available control.",
                "X-Frame-Options.",
                "X-Content-Type-Options as a reliable control. The meta form is not a standard browser hook.",
                "Permissions-Policy.",
                "Cross-Origin-Opener-Policy, Cross-Origin-Resource-Policy, and Cross-Origin-Embedder-Policy.",
                "A custom HSTS policy. On github.io, GitHub sends its own strict-transport-security. A CNAME would leave that default host, so this repo does not add one.",
            ],
            "pages": pages,
        }

    @staticmethod
    def weights() -> dict:
        css = (Site.OUT / "assets" / "site.css").stat().st_size
        icon = (Site.OUT / "favicon.svg").stat().st_size
        limit = 1_048_576
        rows = []
        for path in sorted(Site.OUT.rglob("*.html")):
            html_bytes = path.stat().st_size
            total = html_bytes + css + icon
            rows.append(
                {
                    "path": str(path.relative_to(Site.OUT)),
                    "html_bytes": html_bytes,
                    "css_bytes": css,
                    "image_bytes": icon,
                    "js_bytes": 0,
                    "total_bytes": total,
                    "limit_bytes": limit,
                    "under_limit": total < limit,
                }
            )
        return {
            "method": "Uncompressed bytes of the HTML file plus the shared stylesheet plus the SVG mark. No other assets are referenced.",
            "limit_bytes": limit,
            "pages": rows,
        }


if __name__ == "__main__":
    raise SystemExit(Site.build())
