# Runs data/jobs.tsv through xmltodict itself; the output is expected.out.
import json
import os
import sys
from collections import OrderedDict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import xmltodict  # noqa: E402


def read(path):
    with open("data/" + path, "rb") as f:
        return f.read()


# The postprocessors, force_list functions and preprocessors a job can
# name.
def pp_int(path, key, value):
    try:
        return key, int(value)
    except (ValueError, TypeError):
        return key, value


def pp_typed(path, key, value):
    try:
        return key, int(value)
    except (ValueError, TypeError):
        pass
    if value == "true":
        return key, True
    if value == "false":
        return key, False
    return key, value


def pp_drop(path, key, value):
    if key.startswith("@x") or key == "guid" or key == "#comment":
        return None
    return key, value


def pp_lower(path, key, value):
    return key.lower(), value


def fl_deep(path, key, value):
    return len(path) >= 2 and not isinstance(value, str)


def pre_skip_admins(key, value):
    if key == "admins":
        return None
    return key, value


def pre_upper(key, value):
    return key.upper(), value


POST = {"int": pp_int, "typed": pp_typed, "drop": pp_drop, "lower": pp_lower}
PRE = {"skip_admins": pre_skip_admins, "upper": pre_upper}


def parse_opts(o):
    kw = dict(o)
    if "postprocessor" in kw:
        kw["postprocessor"] = POST[kw["postprocessor"]]
    if isinstance(kw.get("force_list"), list):
        kw["force_list"] = tuple(kw["force_list"])
    if kw.get("force_list") == "deep":
        kw["force_list"] = fl_deep
    if kw.get("dict_constructor") == "OrderedDict":
        kw["dict_constructor"] = OrderedDict
    return kw


def unparse_opts(o):
    kw = dict(o)
    if "preprocessor" in kw:
        kw["preprocessor"] = PRE[kw["preprocessor"]]
    return kw


def failure(e):
    return "raised %s: %s" % (type(e).__name__, e)


def show(text):
    for line in text.split("\n"):
        print("   | " + line)


def do_parse(path, o):
    try:
        print("   " + repr(xmltodict.parse(read(path), **parse_opts(o))))
    except Exception as e:  # noqa: BLE001
        print("   " + failure(e))


def do_json(path, o):
    try:
        d = xmltodict.parse(read(path), **parse_opts(o))
    except Exception as e:  # noqa: BLE001
        print("   " + failure(e))
        return
    show(json.dumps(d, indent=2))


def do_stream(path, depth, limit):
    seen = [0]

    def handle(p, item):
        seen[0] += 1
        print("   path:%s item:%s" % (p, item))
        return limit == 0 or seen[0] < limit

    try:
        r = xmltodict.parse(read(path), item_depth=depth, item_callback=handle)
        print("   %d items, result %r" % (seen[0], r))
    except Exception as e:  # noqa: BLE001
        print("   " + failure(e) + " after %d items" % seen[0])


def do_unparse(d, o):
    try:
        out = xmltodict.unparse(d, **unparse_opts(o))
    except Exception as e:  # noqa: BLE001
        print("   " + failure(e))
        return
    show(out)


def as_list(v):
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def s3report(path):
    d = xmltodict.parse(read(path), force_list=("Contents",), postprocessor=pp_typed)
    r = d["ListBucketResult"]
    print("   bucket %s, prefix %r, %d keys, truncated %s" % (r["Name"], r["Prefix"] or "", r["KeyCount"], r["IsTruncated"]))
    if r["IsTruncated"]:
        print("   continue with %s" % r.get("NextContinuationToken"))
    by_dir = {}
    by_class = {}
    largest = None
    for c in r["Contents"]:
        key = c["Key"]
        size = c["Size"]
        top = key.rsplit("/", 1)[0] + "/" if "/" in key else "(root)"
        n, t = by_dir.get(top, (0, 0))
        by_dir[top] = (n + 1, t + size)
        cls = c.get("StorageClass", "STANDARD")
        by_class[cls] = by_class.get(cls, 0) + size
        if largest is None or size > largest[1]:
            largest = (key, size)
    for top in sorted(by_dir):
        n, t = by_dir[top]
        print("     %-16s %2d objects %9d bytes" % (top, n, t))
    for cls in sorted(by_class):
        print("     %-12s %9d bytes" % (cls, by_class[cls]))
    print("   largest %s (%d bytes)" % largest)
    for p in as_list(r.get("CommonPrefixes")):
        print("   common prefix %s" % p["Prefix"])


def feedreport(path):
    d = xmltodict.parse(read(path))
    ch = d["rss"]["channel"]
    print("   %s <%s> lang %s, self %s" % (ch["title"], ch["link"], ch["language"], ch["atom:link"]["@href"]))
    for it in as_list(ch.get("item")):
        guid = it.get("guid")
        if isinstance(guid, dict):
            perma = guid.get("@isPermaLink", "true") == "true"
            gid = guid["#text"]
        else:
            perma = True
            gid = guid
        cats = as_list(it.get("category"))
        body = it.get("content:encoded") or it.get("description") or ""
        print("   - %s" % it["title"])
        print("     by %s, %s" % (it.get("dc:creator", "unknown"), it.get("pubDate", "undated")))
        print("     tags %s; guid %s (%s); %d chars of body" % (", ".join(cats) or "none", gid, "permalink" if perma else "opaque", len(body)))
        enc = it.get("enclosure")
        if enc:
            print("     enclosure %s, %s, %s bytes" % (enc["@url"], enc["@type"], enc["@length"]))


def gpxreport(path):
    pts = []

    def handle(p, item):
        attrs = p[-1][1]
        pts.append((attrs["lat"], attrs["lon"], int(item["ele"]), item["time"]))
        return True

    xmltodict.parse(read(path), item_depth=4, item_callback=handle)
    climb = 0
    drop = 0
    for a, b in zip(pts, pts[1:]):
        if b[2] > a[2]:
            climb += b[2] - a[2]
        else:
            drop += a[2] - b[2]
    print("   %d points from %s to %s" % (len(pts), pts[0][3], pts[-1][3]))
    print("   start %s,%s end %s,%s" % (pts[0][0], pts[0][1], pts[-1][0], pts[-1][1]))
    print("   climbed %d m, descended %d m, highest %d m" % (climb, drop, max(p[2] for p in pts)))


def soapreport(path):
    ns = {"http://schemas.xmlsoap.org/soap/envelope/": "soap", "https://www.example.org/stock": None, "urn:example:tx": "tx"}
    d = xmltodict.parse(read(path), process_namespaces=True, namespaces=ns)
    env = d["soap:Envelope"]
    tx = env["soap:Header"]["tx:Transaction"]
    print("   transaction %s, must understand %s" % (tx["#text"], tx["@soap:mustUnderstand"]))
    resp = env["soap:Body"]["GetPriceResponse"]
    for p in as_list(resp["Price"]):
        print("   %s %s %s" % (resp["Symbol"], p["@currency"], p["#text"]))


def manifestreport(path):
    ns = {"http://schemas.android.com/apk/res/android": "android"}
    d = xmltodict.parse(read(path), process_namespaces=True, namespaces=ns, force_list=("uses-permission", "activity", "action", "category"))
    m = d["manifest"]
    print("   package %s version %s (%s)" % (m["@package"], m["@android:versionName"], m["@android:versionCode"]))
    for p in m.get("uses-permission", []):
        print("   permission %s" % p["@android:name"].rsplit(".", 1)[-1])
    app = m["application"]
    for a in app.get("activity", []):
        flt = a.get("intent-filter", {})
        acts = [x["@android:name"] for x in flt.get("action", [])]
        cats = [x["@android:name"] for x in flt.get("category", [])]
        launcher = "android.intent.action.MAIN" in acts and "android.intent.category.LAUNCHER" in cats
        print("   activity %s exported=%s launcher=%s" % (a["@android:name"], a.get("@android:exported", "false"), launcher))


def main():
    with open("data/jobs.tsv", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]
    for line in lines:
        if line.startswith("== "):
            print(line)
            continue
        f = line.split("\t")
        print("-- " + " ".join(f))
        if f[0] == "parse":
            do_parse(f[1], json.loads(f[2]))
        elif f[0] == "json":
            do_json(f[1], json.loads(f[2]))
        elif f[0] == "stream":
            do_stream(f[1], int(f[2]), int(f[3]))
        elif f[0] == "roundtrip":
            try:
                d = xmltodict.parse(read(f[1]), **parse_opts(json.loads(f[2])))
            except Exception as e:  # noqa: BLE001
                print("   " + failure(e))
                continue
            do_unparse(d, json.loads(f[3]))
        elif f[0] == "unparse":
            with open("data/" + f[1], encoding="utf-8") as fh:
                d = json.load(fh)
            do_unparse(d, json.loads(f[2]))
        elif f[0] == "s3report":
            s3report(f[1])
        elif f[0] == "feedreport":
            feedreport(f[1])
        elif f[0] == "gpxreport":
            gpxreport(f[1])
        elif f[0] == "soapreport":
            soapreport(f[1])
        elif f[0] == "manifestreport":
            manifestreport(f[1])


main()
