# Runs data/jobs.jsonl through the vendored w3lib 2.5.0, then crawls
# data/site; the output is expected.out.
import json, os, re, sys, warnings
from urllib.parse import urljoin

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
warnings.simplefilter("ignore")
import w3lib.url, w3lib.html, w3lib.encoding, w3lib.http
from w3lib.url import canonicalize_url, url_query_cleaner, safe_download_url, parse_data_uri
from w3lib.html import get_base_url, get_meta_refresh, replace_entities, remove_tags, remove_comments, remove_tags_with_content, strip_html5_whitespace
from w3lib.encoding import html_to_unicode
from w3lib.http import headers_raw_to_dict, basic_auth_header

MODS = {"url": w3lib.url, "html": w3lib.html, "encoding": w3lib.encoding, "http": w3lib.http}
DATA = os.path.join(HERE, "data")


def dec(v):
    if not isinstance(v, dict):
        return v
    if "s" in v:
        return v["s"]
    if "b" in v:
        return bytes.fromhex(v["b"])
    if "f" in v:
        return float(v["f"])
    if "l" in v:
        return tuple(dec(x) for x in v["l"])
    if "d" in v:
        return {dec(k): dec(x) for k, x in v["d"]}


def jobs():
    for n, line in enumerate(open(os.path.join(DATA, "jobs.jsonl"), encoding="utf-8")):
        r = json.loads(line)
        f = getattr(MODS[r["m"]], r["f"])
        a = [dec(x) for x in r["a"]]
        k = {kk: dec(vv) for kk, vv in r["k"].items()}
        try:
            res = repr(f(*a, **k))
        except Exception as e:
            res = f"raised {type(e).__name__}: {e}"
        print(f"{n} {r['f']}: {res}")


TITLE_RE = re.compile(r"<title>(.*?)</title>", re.S | re.I)
HREF_RE = re.compile(r"""<a\s[^>]*?href\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))""", re.I)
IMG_RE = re.compile(r"""<img\s[^>]*?src\s*=\s*"([^"]*)\"""", re.I)
TRACKING = ["utm_source", "utm_medium", "utm_campaign", "ref"]


def crawl():
    site = {}
    for line in open(os.path.join(DATA, "site", "index.tsv")):
        url, name = line.rstrip("\n").split("\t")
        site[canonicalize_url(url)] = name
    start = "http://shop.example/"
    queue = [start]
    seen = {canonicalize_url(start)}
    fetched = 0
    while queue:
        url = queue.pop(0)
        key = canonicalize_url(url)
        print(f"GET {url}")
        if key not in site:
            print("   404 not in the site")
            continue
        raw = open(os.path.join(DATA, "site", site[key]), "rb").read()
        head, _, body = raw.partition(b"\r\n\r\n")
        status_line, _, rest = head.partition(b"\r\n")
        headers = headers_raw_to_dict(rest)
        status = int(status_line.split(b" ")[1])
        fetched += 1
        if status == 401:
            print(f"   401 {headers[b'WWW-Authenticate'][0].decode('latin-1')}; would retry with Authorization: {basic_auth_header('admin', 'pässwort').decode()}")
            continue
        ct = headers[b"Content-Type"][0].decode("latin-1") if b"Content-Type" in headers else None
        enc, text = html_to_unicode(ct, body)
        m = TITLE_RE.search(text)
        title = replace_entities(remove_tags(m.group(1))).strip() if m else None
        base = get_base_url(text, url)
        interval, refresh = get_meta_refresh(text, url)
        print(f"   {status} encoding={enc} title={title!r}")
        if base != url:
            print(f"   base {base}")
        targets = []
        if refresh is not None:
            print(f"   refresh after {interval!r}s to {refresh}")
            targets.append(refresh)
        visible = remove_tags_with_content(remove_comments(text), ["script", "style"])
        for g in HREF_RE.findall(visible):
            targets.append(g[0] or g[1] or g[2])
        for src in IMG_RE.findall(visible):
            if src.startswith("data:"):
                r = parse_data_uri(src)
                print(f"   inline {r.media_type} {r.media_type_parameters} {r.data!r}")
        for t in targets:
            href = strip_html5_whitespace(replace_entities(t))
            if href.split(":", 1)[0].lower() in ("mailto", "javascript", "data"):
                print(f"   skip {href!r}")
                continue
            absolute = url_query_cleaner(urljoin(base, href), TRACKING, remove=True)
            if "/files/" in absolute or "/etc/" in absolute:
                absolute = safe_download_url(absolute)
            c = canonicalize_url(absolute)
            host = w3lib.url.parse_url(c).netloc
            if host != "shop.example":
                print(f"   offsite {c}")
            elif c in seen:
                print(f"   seen {c}")
            else:
                print(f"   new {c}")
                seen.add(c)
                queue.append(c)
    print(f"fetched {fetched} pages, {len(seen)} urls seen")


if __name__ == "__main__":
    jobs()
    crawl()
