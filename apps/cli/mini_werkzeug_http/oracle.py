# Runs Werkzeug 3.1.3's header functions over data/ (as mk.py writes it)
# and prints what mini_werkzeug_http.kara prints. ETags.to_header joins
# frozensets, so the output depends on the str hash:
#     PYTHONHASHSEED=0 python3 -s -P oracle.py > expected.out
import json
import os
import warnings
from datetime import datetime, timezone

import markupsafe
from werkzeug.datastructures import (
    CharsetAccept,
    ContentSecurityPolicy,
    HeaderSet,
    LanguageAccept,
    MIMEAccept,
    ResponseCacheControl,
)
from werkzeug.http import (
    HTTP_STATUS_CODES,
    dump_cookie,
    dump_header,
    dump_options_header,
    generate_etag,
    http_date,
    parse_accept_header,
    parse_age,
    parse_cache_control_header,
    parse_content_range_header,
    parse_cookie,
    parse_csp_header,
    parse_date,
    parse_dict_header,
    parse_etags,
    parse_if_range_header,
    parse_list_header,
    parse_options_header,
    parse_range_header,
    parse_set_header,
    quote_etag,
    quote_header_value,
    remove_entity_headers,
    remove_hop_by_hop_headers,
    unquote_etag,
    unquote_header_value,
    dump_age,
)
from werkzeug.exceptions import RequestedRangeNotSatisfiable
from werkzeug.sansio.http import is_resource_modified


def dt_repr(d):
    return "None" if d is None else d.isoformat()


def show_accept(cls, value, extra):
    a = parse_accept_header(value, cls)
    print(f"  {a!r}")
    print(f"  header={a.to_header()!r} best={a.best!r} provided={a.provided}")
    matches = extra.split(",")
    for m in matches:
        try:
            print(f"  {m!r}: quality={a.quality(m)!r} in={m in a} find={a.find(m)}")
        except ValueError as e:
            print(f"  {m!r}: ! ValueError: {e}")
    try:
        print(f"  best_match={a.best_match(matches)!r} with default={a.best_match(matches, 'fallback')!r}")
    except ValueError as e:
        print(f"  best_match ! ValueError: {e}")
    if cls is MIMEAccept:
        print(f"  html={a.accept_html} xhtml={a.accept_xhtml} json={a.accept_json}")


REQ_CC = ["no_cache", "no_store", "max_age", "max_stale", "min_fresh", "no_transform", "only_if_cached", "stale_if_error"]
RESP_CC = ["no_cache", "public", "private", "must_revalidate", "proxy_revalidate", "s_maxage", "immutable",
           "must_understand", "stale_while_revalidate", "max_age", "no_store", "no_transform", "stale_if_error"]


def show_header(kind, value, extra):
    print(f"{kind} {value!r}")
    if kind == "list":
        r = parse_list_header(value)
        print(f"  {r!r} -> {dump_header(r)!r}")
    elif kind == "dict":
        r = parse_dict_header(value)
        print(f"  {r!r} -> {dump_header(r)!r}")
    elif kind == "options":
        v, o = parse_options_header(value)
        print(f"  {(v, o)!r} -> {dump_options_header(v, o)!r}")
    elif kind == "accept":
        show_accept(None, value, extra)
    elif kind == "mime":
        show_accept(MIMEAccept, value, extra)
    elif kind == "lang":
        show_accept(LanguageAccept, value, extra)
    elif kind == "charset":
        show_accept(CharsetAccept, value, extra)
    elif kind in ("cc", "rcc"):
        cls = ResponseCacheControl if kind == "rcc" else None
        c = parse_cache_control_header(value, cls=cls) if cls else parse_cache_control_header(value)
        print(f"  {c!r} provided={c.provided}")
        print("  " + " ".join(f"{p}={getattr(c, p)!r}" for p in (RESP_CC if kind == "rcc" else REQ_CC)))
        print(f"  header={c.to_header()!r}")
        if kind == "rcc":
            c.max_age = 120
            c.no_cache = True
            c.private = False
            c.public = True
            c.s_maxage = None
            print(f"  changed={c.to_header()!r}")
    elif kind == "csp":
        c = parse_csp_header(value)
        print(f"  {c!r}")
        print(f"  default_src={c.default_src!r} script_src={c.script_src!r} report_uri={c.report_uri!r}")
        print(f"  header={c.to_header()!r}")
    elif kind == "set":
        s = parse_set_header(value)
        print(f"  {s!r} len={len(s)} header={s.to_header()!r}")
        print(f"  'token' in={'token' in s} find('origin')={s.find('origin')}")
        s.add("X-New")
        s.discard("User-Agent")
        s.discard("token")
        print(f"  after={s.to_header()!r}")
    elif kind == "range":
        r = parse_range_header(value)
        if r is None:
            print("  None")
            return
        print(f"  units={r.units!r} ranges={r.ranges!r} header={r.to_header()!r}")
        for ln in extra.split(","):
            n = int(ln)
            cr = r.make_content_range(n)
            print(f"  {n}: for_length={r.range_for_length(n)!r} content_range={r.to_content_range_header(n)!r} made={None if cr is None else cr.to_header()!r}")
    elif kind == "crange":
        r = parse_content_range_header(value)
        if r is None:
            print("  None")
            return
        print(f"  units={r.units!r} start={r.start!r} stop={r.stop!r} length={r.length!r} header={r.to_header()!r} bool={bool(r)}")
    elif kind == "ifrange":
        r = parse_if_range_header(value)
        print(f"  etag={r.etag!r} date={dt_repr(r.date)} header={r.to_header()!r}")
    elif kind == "etags":
        e = parse_etags(value)
        print(f"  header={e.to_header()!r} bool={bool(e)} len={len(e)} star={e.star_tag}")
        for p in extra.split(","):
            print(f"  {p!r}: contains={e.contains(p)} weak={e.contains_weak(p)} raw={e.contains_raw(p)} is_weak={e.is_weak(p)}")
    elif kind == "date":
        d = parse_date(None if value == "NONE" else value)
        print(f"  {dt_repr(d)} -> {None if d is None else http_date(d)!r}")
    elif kind == "age":
        a = parse_age(value)
        if a is None:
            print("  None")
        else:
            print(f"  {int(a.total_seconds())} -> {dump_age(a)!r}")
    elif kind == "cookie":
        c = parse_cookie(value.encode().decode("latin1"))
        print(f"  {c!r}")
    elif kind == "quote":
        print(f"  {quote_header_value(value)!r} {quote_header_value(value, allow_token=False)!r} {unquote_header_value(value)!r}")
    elif kind == "etag":
        u = unquote_etag(value)
        try:
            q = repr(quote_etag(value)) + " " + repr(quote_etag(value, True))
        except ValueError as e:
            q = f"! ValueError: {e}"
        print(f"  unquote={u!r} quote={q}")
    elif kind == "strip":
        names = [x.strip() for x in value.split(",")]
        hs = [(n, "v") for n in names]
        remove_entity_headers(hs)
        print(f"  entity -> {[k for k, _ in hs]!r}")
        hs = [(n, "v") for n in names]
        remove_entity_headers(hs, allowed=("allow",))
        print(f"  entity(allow) -> {[k for k, _ in hs]!r}")
        hs = [(n, "v") for n in names]
        remove_hop_by_hop_headers(hs)
        print(f"  hop -> {[k for k, _ in hs]!r}")


def show_cookie(line):
    f = line.split("|")
    kw = {}
    key = ""
    value = ""
    for field in f:
        k, eq, v = field.partition("=")
        if k == "k":
            key = v
        elif k == "v":
            value = v
        elif k == "max_age":
            kw["max_age"] = int(v)
        elif k == "expires":
            kw["expires"] = int(v) if v.isdigit() else v
        elif k == "path":
            kw["path"] = v
        elif k == "nopath":
            kw["path"] = None
        elif k == "domain":
            kw["domain"] = v
        elif k == "samesite":
            kw["samesite"] = v
        elif k == "nosync":
            kw["sync_expires"] = False
        elif k in ("secure", "httponly", "partitioned"):
            kw[k] = True
    shown = value if len(value) <= 40 else value[:20] + f"...({len(value)} chars)"
    print(f"set_cookie {key!r} {shown!r} {kw!r}")
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        try:
            out = dump_cookie(key, value, **kw)
        except ValueError as e:
            print(f"  ! ValueError: {e}")
            return
    if len(out) > 200:
        print(f"  {out[:60]!r}...{out[-30:]!r} ({len(out)} chars)")
    else:
        print(f"  {out!r}")
    for m in w:
        print(f"  warning: {m.message}")


# ------------------------------------------------------------ the docs server

DOCS = {}
for line in open("data/docs.txt").read().splitlines():
    p, m, langs, types, cache = line.split("|")
    name = p[1:]
    DOCS[p] = {
        "mtime": int(m),
        "langs": langs.split(","),
        "types": types.split(","),
        "cache": cache,
        "text": {lang: open(f"data/docs/{name}.{lang}.txt", encoding="utf-8").read() for lang in langs.split(",")},
    }
ALL_LANGS = []
for d in DOCS.values():
    for lang in d["langs"]:
        if lang not in ALL_LANGS:
            ALL_LANGS.append(lang)


def render(path, lang, typ, text):
    if typ == "text/html":
        return f'<!doctype html><html lang="{lang}"><body><p>{markupsafe.escape(text)}</p></body></html>'
    if typ == "application/json":
        if path == "/status":
            return json.dumps({"status": text, "docs": len(DOCS)})
        return json.dumps({"lang": lang, "text": text})
    return text


def query_get(q, key):
    for part in q.split("&"):
        k, _, v = part.partition("=")
        if k == key:
            return v
    return None


def serve(method, path, query, hdrs, reqbody):
    env = {"HTTP_" + k.upper().replace("-", "_"): v for k, v in hdrs}
    get = lambda k: env.get("HTTP_" + k.upper().replace("-", "_"))
    out = []
    body = ""

    if path == "/prefs":
        lang = query_get(query, "lang")
        if lang not in ALL_LANGS:
            return 400, [("Content-Type", "text/plain; charset=utf-8")], f"unknown language: {lang}"
        remember = query_get(query, "remember") != "0"
        c = dump_cookie("lang", lang, max_age=31536000 if remember else None, httponly=True, samesite="lax", sync_expires=False)
        return 204, [("Set-Cookie", c), ("Vary", HeaderSet(["Cookie"]).to_header())], ""
    if path == "/whoami":
        c = parse_cookie(get("Cookie"))
        text = f"session={c.get('session')!r} all={c.getlist('session')!r} lang={c.get('lang')!r} count={len(list(c.items(multi=True)))}"
        return 200, [("Content-Type", "text/plain; charset=utf-8")], text
    if path == "/proxy/upstream":
        forward = list(hdrs)
        named = [x.lower() for x in parse_list_header(get("Connection") or "")]
        remove_hop_by_hop_headers(forward)
        forward = [(k, v) for k, v in forward if k.lower() not in named]
        upstream = [("Content-Type", "text/plain"), ("Connection", "close"), ("Keep-Alive", "timeout=5"),
                    ("Transfer-Encoding", "chunked"), ("X-Upstream", "1"), ("Upgrade", "h2c"), ("Trailer", "Expires"),
                    ("Content-Length", "5")]
        remove_hop_by_hop_headers(upstream)
        text = "forwarded: " + ", ".join(f"{k}={v}" for k, v in forward)
        return 200, upstream, text
    if path == "/negotiate":
        m = parse_accept_header(get("Accept"), MIMEAccept)
        e = parse_accept_header(get("Accept-Encoding"))
        lang = parse_accept_header(get("Accept-Language"), LanguageAccept)
        lines = [
            f"html={m.accept_html} xhtml={m.accept_xhtml} json={m.accept_json}",
            f"type={m.best_match(['text/html', 'application/json'])!r}",
            f"encoding={e.best_match(['br', 'gzip', 'identity'])!r} from {e.to_header()!r}",
            f"language={lang.best_match(['en-US', 'en', 'de'], default='en')!r}",
        ]
        return 200, [("Content-Type", "text/plain; charset=utf-8"), ("Vary", "Accept, Accept-Encoding, Accept-Language")], "\n".join(lines)
    if path == "/cache-check":
        c = parse_cache_control_header(get("Cache-Control"))
        lines = [repr(c)] + [f"{p}={getattr(c, p)!r}" for p in REQ_CC]
        r = ResponseCacheControl()
        r.no_store = True
        r.max_age = 0
        r.private = "Authorization"
        return 200, [("Content-Type", "text/plain; charset=utf-8"), ("Cache-Control", r.to_header())], "\n".join(lines)
    if path == "/csp":
        c = parse_csp_header(get("Content-Security-Policy-Report-Only"))
        c.img_src = "'self' data:"
        c.script_src = (c.script_src or "") + " 'nonce-r4nd0m'"
        c.report_uri = None
        c.default_src = None
        c.default_src = "'none'"
        return 200, [("Content-Security-Policy", c.to_header())], repr(c)

    doc = DOCS.get(path)
    if doc is None:
        return 404, [("Content-Type", "text/plain; charset=utf-8")], "Not Found"
    allowed = ["GET", "HEAD"] if path == "/status" else ["GET", "HEAD", "PUT"]
    if method == "OPTIONS":
        return 204, [("Allow", dump_header(allowed))], ""
    if method not in allowed:
        return 405, [("Allow", dump_header(allowed)), ("Content-Type", "text/plain; charset=utf-8")], "Method Not Allowed"

    if method == "PUT":
        lang = get("Content-Language")
        if lang not in doc["langs"]:
            return 400, [("Content-Type", "text/plain; charset=utf-8")], f"language not offered: {lang}"
        etag = generate_etag(doc["text"][lang].encode())
        im = parse_etags(get("If-Match"))
        if im and not im.contains(etag):
            return 412, [("ETag", quote_etag(etag))], "Precondition Failed"
        ius = parse_date(get("If-Unmodified-Since"))
        lm = datetime.fromtimestamp(doc["mtime"], timezone.utc)
        if ius is not None and lm > ius:
            return 412, [("Last-Modified", http_date(lm))], "Precondition Failed"
        doc["text"][lang] = reqbody
        doc["mtime"] += 1000
        return 204, [("ETag", quote_etag(generate_etag(doc["text"][lang].encode()))),
                     ("Last-Modified", http_date(doc["mtime"]))], ""

    cookies = parse_cookie(get("Cookie"))
    lang = cookies.get("lang")
    if lang not in doc["langs"]:
        lang = parse_accept_header(get("Accept-Language"), LanguageAccept).best_match(doc["langs"], default=doc["langs"][0])
    acc = parse_accept_header(get("Accept"), MIMEAccept)
    typ = acc.best_match(doc["types"]) if acc else doc["types"][0]
    if typ is None:
        return 406, [("Content-Type", "text/plain; charset=utf-8")], "Not Acceptable. Offered: " + ", ".join(doc["types"])
    cs = parse_accept_header(get("Accept-Charset"), CharsetAccept)
    if cs and cs.best_match(["utf-8"]) is None:
        return 406, [("Content-Type", "text/plain; charset=utf-8")], f"Not Acceptable. Charset: {cs.to_header()}"
    body = render(path, lang, typ, doc["text"][lang])
    data = body.encode()
    ctype = dump_options_header(typ, {"charset": "utf-8"}) if typ.startswith("text/") or typ == "application/json" else typ
    out.append(("Content-Type", ctype))
    out.append(("Content-Language", lang))
    if len(doc["langs"]) > 1 or len(doc["types"]) > 1:
        out.append(("Vary", HeaderSet(["Accept", "accept", "Accept-Language", "Cookie"]).to_header()))
    out.append(("ETag", quote_etag(generate_etag(data))))
    out.append(("Last-Modified", http_date(doc["mtime"])))
    out.append(("Cache-Control", parse_cache_control_header(doc["cache"], cls=ResponseCacheControl).to_header()))

    req_cc = parse_cache_control_header(get("Cache-Control"))
    if req_cc.no_cache or "no-cache" in parse_set_header(get("Pragma")):
        out.append(("Content-Length", str(len(data))))
        return 200, out, body
    status = 200
    accept_ranges = path == "/changelog"
    etag_h = dict(out)["ETag"]
    lm_h = dict(out)["Last-Modified"]

    def processable():
        return ("HTTP_IF_RANGE" not in env or not is_resource_modified(
            http_range=env.get("HTTP_RANGE"), http_if_range=env.get("HTTP_IF_RANGE"),
            http_if_modified_since=env.get("HTTP_IF_MODIFIED_SINCE"), http_if_none_match=env.get("HTTP_IF_NONE_MATCH"),
            http_if_match=env.get("HTTP_IF_MATCH"), etag=etag_h, last_modified=lm_h, ignore_if_range=False)) and "HTTP_RANGE" in env

    is206 = False
    if accept_ranges and len(data) != 0 and processable():
        r = parse_range_header(env.get("HTTP_RANGE"))
        rt = None if r is None else r.range_for_length(len(data))
        crh = None if r is None else r.to_content_range_header(len(data))
        if rt is None or crh is None:
            e = RequestedRangeNotSatisfiable(len(data))
            hs = [h for h in e.get_headers() if h[0] != "Content-Type"]
            return 416, [("Content-Type", "text/plain; charset=utf-8")] + hs, "Requested Range Not Satisfiable"
        out.append(("Content-Length", str(rt[1] - rt[0])))
        out.append(("Accept-Ranges", "bytes"))
        out.append(("Content-Range", crh))
        data = data[rt[0]:rt[1]]
        body = data.decode()
        status = 206
        is206 = True
    if not is206 and not is_resource_modified(
            http_range=env.get("HTTP_RANGE"), http_if_range=env.get("HTTP_IF_RANGE"),
            http_if_modified_since=env.get("HTTP_IF_MODIFIED_SINCE"), http_if_none_match=env.get("HTTP_IF_NONE_MATCH"),
            http_if_match=env.get("HTTP_IF_MATCH"), etag=etag_h, last_modified=lm_h):
        status = 412 if parse_etags(env.get("HTTP_IF_MATCH")) else 304
    if not any(k == "Content-Length" for k, _ in out):
        out.append(("Content-Length", str(len(data))))
    if accept_ranges and not is206:
        out.append(("Accept-Ranges", "bytes"))
    if status == 304:
        remove_entity_headers(out)
        body = ""
    return status, out, body


def main():
    print("# headers")
    for line in open("data/headers.txt", encoding="utf-8").read().split("\n")[:-1]:
        parts = line.split("\t")
        show_header(parts[0], parts[1], parts[2] if len(parts) > 2 else "")
    print("# cookies")
    for line in open("data/cookies.txt", encoding="utf-8").read().split("\n")[:-1]:
        show_cookie(line)
    print("# requests")
    for name in sorted(os.listdir("data/requests")):
        raw = open(f"data/requests/{name}", "rb").read().decode("utf-8")
        head, _, body = raw.partition("\r\n\r\n")
        lines = head.split("\r\n")
        method, target, _ = lines[0].split(" ")
        path, _, query = target.partition("?")
        hdrs = []
        for ln in lines[1:]:
            k, _, v = ln.partition(":")
            hdrs.append((k, v.strip()))
        print(f"== {name[:-5]}")
        print(f"> {method} {target}")
        status, out, text = serve(method, path, query, hdrs, body)
        print(f"< {status} {HTTP_STATUS_CODES[status]}")
        for k, v in out:
            print(f"< {k}: {v}")
        if text and method != "HEAD":
            print(f"| {text!r}")


main()
