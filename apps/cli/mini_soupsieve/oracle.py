# Runs data/jobs.tsv through soupsieve itself on bs4's html.parser tree;
# the output is expected.out.
import os
import sys
import warnings

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import soupsieve as sv  # noqa: E402
from bs4 import BeautifulSoup  # noqa: E402

warnings.simplefilter("ignore")


def field(s):
    for a, b in [("∅", ""), ("⏎", "\n"), ("⇥", "\t"), ("␣", " "), ("␀", "\x00"), ("␁", "\x01"), ("␉", "\x09"), ("␡", "\x7f")]:
        s = s.replace(a, b)
    return s


def pairs(s):
    if s == "-":
        return None
    d = {}
    for p in s.split("¦"):
        k, v = p.split("=", 1)
        d[field(k)] = field(v)
    return d


PAGES = {}


def page(name):
    if name not in PAGES:
        with open("data/pages/" + name, encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
        PAGES[name] = (soup, soup.find_all())
    return PAGES[name]


def desc(tags, el):
    if el is None:
        return "None"
    if isinstance(el, BeautifulSoup):
        return "[document]"
    i = next(k for k, t in enumerate(tags) if t is el)
    s = "%d:%s" % (i, el.name)
    if el.get("id") is not None:
        s += "#" + el.get("id")
    for c in el.get("class") or []:
        s += "." + c
    return s


def node(name, which):
    soup, tags = page(name)
    return soup if which == "-" else tags[int(which)]


def raised(e):
    return "raised %s: %s" % (type(e).__name__, e)


def run(w):
    soup, tags = page(w[1]) if w[0] not in ("parse", "escape") else (None, None)
    if w[0] == "parse":
        return repr(sv.compile(field(w[1])).selectors)
    if w[0] == "escape":
        return repr(sv.escape(field(w[1])))
    if w[0] == "select":
        # soupsieve.select() drops its custom= argument on the way to
        # compile(), so the jobs compile first, as code using custom
        # selectors has to.
        compiled = sv.compile(field(w[4]), namespaces=pairs(w[5]), custom=pairs(w[6]))
        found = compiled.select(node(w[1], w[2]), limit=int(w[3]))
        return "%d: %s" % (len(found), " ".join(desc(tags, t) for t in found))
    if w[0] == "helper":
        found = sv.select(field(w[3]), node(w[1], w[2]), custom=pairs(w[4]))
        return "%d: %s" % (len(found), " ".join(desc(tags, t) for t in found))
    if w[0] == "one":
        return desc(tags, sv.select_one(field(w[3]), node(w[1], w[2])))
    if w[0] == "match":
        el = node(w[1], w[2])
        return "%s %s" % (desc(tags, el), sv.match(field(w[3]), el))
    if w[0] == "closest":
        el = node(w[1], w[2])
        return "%s -> %s" % (desc(tags, el), desc(tags, sv.closest(field(w[3]), el)))
    if w[0] == "filter":
        el = node(w[1], w[2])
        found = sv.filter(field(w[3]), el)
        return "%s: %d: %s" % (desc(tags, el), len(found), " ".join(desc(tags, t) for t in found))
    if w[0] == "attr":
        out = []
        for t in sv.select(field(w[2]), soup):
            v = t.get(w[3])
            out.append(desc(tags, t) + "=" + ("None" if v is None else repr(" ".join(v) if isinstance(v, list) else v)))
        return " ".join(out)
    raise SystemExit("bad job " + w[0])


def main():
    with open("data/jobs.tsv", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]
    for line in lines:
        if line.startswith("#"):
            print(line)
            continue
        print("-- " + line.replace("\t", " | "))
        try:
            print("   " + run(line.split("\t")))
        except Exception as e:  # noqa: BLE001
            print("   " + raised(e))


main()
