"""Step 1 (starter): collect weather news from an RSS feed and push it through the pipeline.
Add more collectors here (X, Reddit, YouTube...) that call service.ingest()."""
import urllib.request
import xml.etree.ElementTree as ET


def parse_rss(xml_text):
    """Return a list of headline strings from RSS 2.0 XML."""
    root = ET.fromstring(xml_text)
    out = []
    for item in root.iter("item"):
        title = (item.findtext("title") or "").strip()
        desc = (item.findtext("description") or "").strip()
        if title:
            out.append((title + ". " + desc).strip(". ") if desc else title)
    return out


def fetch_feed(url, timeout=10):
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return parse_rss(r.read().decode("utf-8", "replace"))


def collect(con, url):
    """Fetch a feed and store each headline as a 'News RSS' report. Returns stored reports."""
    from backend import service
    return [service.ingest(con, text, "News RSS", 3000) for text in fetch_feed(url)]
