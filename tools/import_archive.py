"""Turn the old Axon pages we still pointed at into local article HTML."""

from __future__ import annotations

import json
import re
import urllib.request
from html import escape
from html.parser import HTMLParser
from io import BytesIO
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
POSTS = Path("/tmp/axon-posts.json")
UA = {"User-Agent": "Mozilla/5.0 (compatible; AxonArchive/1.0)"}
MEDIA = ROOT / "media"

PAGE_MAP = {
    "recognitions": "recognition",
    "israel-info": "recognition",
    "news": "news",
    "news-blog": "news",
    "contact": "engage",
    "faqs": "faq",
    "how-we-engage": "how-we-engage",
    "extended-capabilities": "extended-capabilities",
    "our-ceo-global-cto": "our-ceo",
    "our-clients": "clients",
    "who-we-are": "about",
}

IMAGES = {
    "https://axoncyber.com/wp-content/uploads/2020/10/FullSizeRender-706x1024-1.jpg": "ceo-portrait",
    "https://axoncyber.com/wp-content/uploads/2020/10/florian-olivo-Ek9Znm8lQ1U-unsplash-scaled-1.jpg": "engage-room",
    "https://gearedup.games/wp-content/uploads/2020/10/Screen-Shot-2017-04-24-at-8.24.46-PM.png": "ceo-screen",
}

SKIP_IMAGES = ("pixel.png",)


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as response:
        return response.read()


def save_image(url: str, stem: str) -> tuple[str, int, int] | None:
    try:
        raw = fetch(url)
    except Exception as exc:
        print("IMAGE FAIL", url, type(exc).__name__, exc)
        return None
    image = Image.open(BytesIO(raw))
    bands = image.getbands()
    if image.mode == "P" and "transparency" in image.info:
        image = image.convert("RGBA")
    elif "A" in bands and image.mode != "RGBA":
        image = image.convert("RGBA")
    elif image.mode not in ("RGB", "RGBA"):
        image = image.convert("RGB")
    if image.mode == "RGBA":
        alpha = image.getchannel("A")
        if alpha.getextrema() == (255, 255):
            image = image.convert("RGB")
    image.thumbnail((1600, 1600), Image.Resampling.LANCZOS)
    dest = MEDIA / f"{stem}.webp"
    image.save(dest, "WEBP", quality=75, method=6)
    print("IMAGE", dest.name, image.mode, image.size, dest.stat().st_size)
    return dest.name, image.size[0], image.size[1]


def classify(href: str, post_slugs: set[str]) -> tuple[str, str]:
    raw = (href or "").strip()
    if not raw or raw == "#":
        return ("drop", raw)
    lower = raw.casefold()
    if lower.startswith("mailto:") or lower.startswith("tel:"):
        return ("keep", raw)
    if "@" in raw and "://" not in raw and not raw.startswith("/"):
        return ("keep", "mailto:" + raw)
    parsed = urlparse(raw)
    if parsed.scheme in ("http", "https") and "google." in parsed.netloc and parsed.path.startswith("/url"):
        target = parse_qs(parsed.query).get("q", [""])[0]
        if target:
            return classify(target, post_slugs)
    if raw.startswith("/") or raw.startswith("#"):
        host = "axoncyber.com"
        path = parsed.path if raw.startswith("/") else raw
        query_host = ""
    else:
        host = parsed.netloc.casefold().removeprefix("www.")
        path = parsed.path
        query_host = host
    if query_host and "axoncyber.com" not in query_host:
        return ("external", raw)
    parts = [part for part in path.split("/") if part]
    if not parts:
        return ("internal", "home")
    if (
        len(parts) >= 4
        and re.fullmatch(r"20\d{2}", parts[0])
        and re.fullmatch(r"\d{2}", parts[1])
        and parts[3] in post_slugs
    ):
        return ("internal", "news/" + parts[3])
    if len(parts) == 2 and re.fullmatch(r"20\d{2}", parts[0]) and re.fullmatch(r"\d{2}", parts[1]):
        return ("internal", f"news#{parts[0]}-{parts[1]}")
    if len(parts) == 1 and parts[0] in PAGE_MAP:
        return ("internal", PAGE_MAP[parts[0]])
    return ("unknown", raw)


class Cleaner(HTMLParser):
    DROP = {"script", "style", "noscript"}
    MAP = {
        "h1": "h2",
        "h2": "h2",
        "h3": "h3",
        "h4": "h4",
        "h5": "h4",
        "h6": "h4",
        "p": "p",
        "ul": "ul",
        "ol": "ol",
        "li": "li",
        "strong": "strong",
        "b": "b",
        "em": "em",
        "i": "i",
        "br": "br",
    }

    def __init__(self, post_slugs: set[str], images: dict[str, tuple[str, int, int]]):
        super().__init__(convert_charrefs=True)
        self.post_slugs = post_slugs
        self.images = images
        self.parts: list = []
        self.stack: list[str] = []
        self.drop = 0
        self.saw_video = False
        self.links: list[tuple[str, str, str]] = []
        self.missing_images: list[str] = []

    def handle_starttag(self, tag, attrs):
        self._start(tag, attrs)

    def handle_startendtag(self, tag, attrs):
        self._start(tag, attrs, end=True)

    def _start(self, tag, attrs, end=False):
        tag = tag.lower()
        if self.drop:
            if tag in self.DROP and not end:
                self.drop += 1
            return
        if tag in self.DROP:
            if not end:
                self.drop = 1
            return
        if tag == "video":
            self.saw_video = True
            return
        if tag in ("source", "iframe", "svg", "form", "input", "button"):
            return
        data = dict(attrs)
        if tag == "img":
            src = data.get("src") or ""
            if not src or src.endswith(SKIP_IMAGES):
                return
            saved = self.images.get(src)
            if saved is None:
                self.missing_images.append(src)
                self.parts.append(("missing-img", src, data.get("alt") or ""))
                return
            filename, width, height = saved
            alt = data.get("alt") or ""
            self.parts.append(("img", filename, alt, width, height))
            return
        if tag == "a":
            kind, dest = classify(data.get("href") or "", self.post_slugs)
            self.links.append((data.get("href") or "", kind, dest))
            if kind == "drop":
                return
            if kind == "unknown":
                self.parts.append(("unknown", dest))
                return
            self.stack.append("a")
            self.parts.append(("start-a", kind, dest))
            return
        mapped = self.MAP.get(tag)
        if mapped == "br":
            self.parts.append(("br",))
            return
        if mapped:
            self.stack.append(mapped)
            self.parts.append(("start", mapped))

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in self.DROP and self.drop:
            self.drop -= 1
            return
        if self.drop:
            return
        mapped = "a" if tag == "a" else self.MAP.get(tag)
        if mapped == "br" or mapped is None:
            return
        if self.stack and self.stack[-1] == mapped:
            self.stack.pop()
            self.parts.append(("end", mapped))

    def handle_data(self, data):
        if self.drop or not data:
            return
        text = re.sub(r"\s+", " ", data)
        if text:
            self.parts.append(("text", text))

    def html(self) -> str:
        while self.stack:
            self.parts.append(("end", self.stack.pop()))
        out = []
        for part in self.parts:
            kind = part[0]
            if kind == "text":
                out.append(escape(part[1]))
            elif kind == "br":
                out.append("<br>")
            elif kind == "start":
                out.append(f"<{part[1]}>")
            elif kind == "end":
                out.append(f"</{part[1]}>")
            elif kind == "start-a":
                link_kind, dest = part[1], part[2]
                if link_kind == "internal":
                    out.append(f'<a href="site:{escape(dest, quote=True)}">')
                elif link_kind == "keep":
                    out.append(f'<a href="{escape(dest, quote=True)}">')
                else:
                    out.append(
                        f'<a class="external" rel="external" href="{escape(dest, quote=True)}">'
                    )
            elif kind == "img":
                filename, alt, width, height = part[1], part[2], part[3], part[4]
                out.append(
                    '<figure class="article-figure">'
                    f'<img src="media:{filename}" alt="{escape(alt, quote=True)}" '
                    f'width="{width}" height="{height}">'
                    "</figure>"
                )
            elif kind == "missing-img":
                src, alt = part[1], part[2]
                label = alt or "Image"
                out.append(
                    f'<p class="source-note">{escape(label)} is not included. '
                    f"Original file: {escape(src)}</p>"
                )
            elif kind == "unknown":
                out.append(
                    f'<p class="source-note">Link not carried over. Original file: {escape(part[1])}</p>'
                )
        html = "".join(out)
        html = re.sub(r"<(p|h2|h3|h4|li)>(?: |\u00a0)*</\1>", "", html)
        return html


def clean(html: str, post_slugs: set[str], images: dict) -> Cleaner:
    parser = Cleaner(post_slugs, images)
    parser.feed(html)
    parser.close()
    return parser


def main() -> None:
    posts = json.loads(POSTS.read_text(encoding="utf-8"))
    news = json.loads((ROOT / "content" / "news.json").read_text(encoding="utf-8"))
    by_link = {post["link"].rstrip("/"): post for post in posts}
    post_slugs = {post["slug"] for post in posts}
    saved: dict[str, tuple[str, int, int]] = {}
    image_failures = []
    for url, stem in IMAGES.items():
        result = save_image(url, stem)
        if result is None:
            image_failures.append(url)
        else:
            saved[url] = result

    articles = []
    rewrites = []
    external = []
    unknowns = []
    for item in news:
        source = item["source"].rstrip("/")
        post = by_link[source]
        parser = clean(post["content"]["rendered"], post_slugs, saved)
        html = parser.html()
        if parser.saw_video and "nov-interview" not in html:
            html += (
                "<p>The original page contains one video, nov-interview.mp4 "
                "(307,383,808 bytes). Original file: "
                "https://axoncyber.com/wp-content/uploads/2024/11/nov-interview.mp4. "
                "The file is not included on this page.</p>"
            )
        slug = "news/" + post["slug"]
        articles.append(
            {
                "kind": "news",
                "slug": slug,
                "title": item["title"],
                "date": item["date"],
                "source": item["source"],
                "html": html,
                "back": "news",
                "back_label": "News",
            }
        )
        for href, kind, dest in parser.links:
            if kind == "internal":
                rewrites.append({"source": href, "now": dest, "on": "/" + slug + "/"})
            elif kind == "external":
                external.append({"url": href, "on": "/" + slug + "/"})
            elif kind == "unknown":
                unknowns.append({"source": href, "on": "/" + slug + "/"})

    page_files = {
        "extended-capabilities": (
            "Extended Capabilities",
            "government",
            "Government Quals",
        ),
        "how-we-engage": (
            "How We Engage",
            "extended-capabilities",
            "Extended Capabilities",
        ),
        "our-ceo-global-cto": (
            "Our CEO & Global CTO",
            "news",
            "News",
        ),
    }
    for source_slug, (title, back, back_label) in page_files.items():
        payload = json.loads(Path(f"/tmp/page-{source_slug}.json").read_text(encoding="utf-8"))
        parser = clean(payload["html"], post_slugs, saved)
        dest_slug = PAGE_MAP[source_slug]
        articles.append(
            {
                "kind": "page",
                "slug": dest_slug,
                "title": title,
                "date": "",
                "source": payload["link"],
                "html": parser.html(),
                "back": back,
                "back_label": back_label,
            }
        )
        for href, kind, dest in parser.links:
            page_on = "/" + dest_slug + "/"
            if kind == "internal":
                rewrites.append({"source": href, "now": dest, "on": page_on})
            elif kind == "external":
                external.append({"url": href, "on": page_on})
            elif kind == "unknown":
                unknowns.append({"source": href, "on": page_on})

    pages = json.loads((ROOT / "content" / "pages.json").read_text(encoding="utf-8"))
    month_changes = []
    months = []
    for label, url in pages["archive_months"]:
        match = re.search(r"/(20\d{2})/(\d{2})/?$", url)
        if not match:
            raise SystemExit(f"month url {url}")
        key = f"{match.group(1)}-{match.group(2)}"
        months.append([label, key])
        month_changes.append({"source": url, "now": f"/news/#{key}", "on": "/news/"})
    pages["archive_months"] = months
    who = pages["who_value"]
    cut = who.find(" https://")
    if cut != -1:
        pages["who_value"] = who[:cut].rstrip()
    (ROOT / "content" / "pages.json").write_text(
        json.dumps(pages, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (ROOT / "content" / "articles.json").write_text(
        json.dumps({"articles": articles}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    source_map = {
        "created": [
            {"path": "/" + article["slug"] + "/", "source": article["source"]}
            for article in articles
        ],
        "retargeted": rewrites + month_changes,
        "external_kept": external,
        "unknown": unknowns,
        "image_failures": image_failures,
        "who_value_removed": [
            "https://axoncyber.com/our-clients/",
            "https://axoncyber.com/recognitions/",
        ],
    }
    (ROOT / "content" / "source-map.json").write_text(
        json.dumps(source_map, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print("articles", len(articles), "rewrites", len(rewrites), "external", len(external))
    print("unknown", unknowns)
    print("image failures", image_failures)
    blob = json.dumps(articles)
    if re.search(r'href=\\"https?://[^\\"]*axoncyber', blob) or "href=\\\"http://www.axoncyber" in blob:
        raise SystemExit("axon href survived")


if __name__ == "__main__":
    main()
