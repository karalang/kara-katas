# Runs the selectors in data/ through cssselect 1.2.0 (the copy in
# cssselect/, unchanged) and parsel's translator (parsel/csstranslator.py,
# unchanged), and prints what mini_cssselect prints.
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "parsel"))

import mk  # noqa: E402
import cssselect  # noqa: E402
import csstranslator  # noqa: E402

DATA = os.path.join(HERE, "data")

GENERIC = cssselect.GenericTranslator()
HTML = cssselect.HTMLTranslator()
PARSEL = csstranslator.HTMLTranslator()


def err(e):
    return "%s: %s" % (type(e).__name__, e)


def translate(tr, css):
    try:
        return tr.css_to_xpath(css)
    except Exception as e:  # the type is printed
        return "error " + err(e)


def spider_entries(rel, text):
    out = []
    for i, line in enumerate(text.split("\n"), 1):
        if not line.strip() or line.startswith("#"):
            continue
        name, sel = line.split(" = ", 1)
        out.append((i, "%s = %s" % (name, sel), sel))
    return out


def css_entries(text):
    out = []
    pending = ""
    start = 0
    for i, line in enumerate(text.split("\n"), 1):
        s = line.strip()
        if not s or s == "}" or s.startswith("@"):
            continue
        if s.startswith("/*") and s.endswith("*/"):
            continue
        if "{" in s:
            if not pending:
                start = i
            sel = (pending + s[:s.index("{")]).strip()
            pending = ""
            out.append((start, sel, sel))
        elif s.endswith(","):
            if not pending:
                start = i
            pending += s + " "
    return out


def line_entries(text):
    return [(i, line, line) for i, line in enumerate(text.split("\n"), 1) if line]


def read(rel):
    with open(os.path.join(DATA, rel), encoding="utf-8", newline="") as f:
        return f.read()


def main():
    mk.main()
    files = []
    for name in sorted(os.listdir(os.path.join(DATA, "spiders"))):
        rel = "spiders/" + name
        files.append((rel, spider_entries(rel, read(rel))))
    files.append(("theme.css", css_entries(read("theme.css"))))
    files.append(("broken.txt", line_entries(read("broken.txt"))))

    summary = []
    cascade = []
    for rel, entries in files:
        print("== %s" % rel)
        perrs = 0
        terrs = 0
        for line, label, css in entries:
            print("%s:%d %s" % (rel, line, label))
            try:
                sels = cssselect.parse(css)
            except Exception as e:
                print("  error: " + err(e))
                perrs += 1
                continue
            for s in sels:
                print("  tree: %r" % (s,))
                print("  canonical: %s  specificity: %s" % (s.canonical(), s.specificity()))
                if rel == "theme.css":
                    cascade.append((s.specificity(), s.canonical()))
            g = translate(GENERIC, css)
            h = translate(HTML, css)
            p = translate(PARSEL, css)
            print("  generic: " + g)
            print("  html: " + ("= generic" if h == g else h))
            print("  parsel: " + ("= html" if p == h else p))
            if p.startswith("error "):
                terrs += 1
        summary.append("%s: %d selectors, %d parse errors, %d translation errors"
                       % (rel, len(entries), perrs, terrs))
    print("== summary")
    for line in summary:
        print(line)
    print("== cascade (theme.css, by specificity)")
    for spec, canon in sorted(cascade, key=lambda c: c[0]):
        print("%s %s" % (spec, canon))


if __name__ == "__main__":
    main()
