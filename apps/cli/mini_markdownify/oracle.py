# Runs data/jobs.tsv through markdownify itself; the output is expected.out.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from markdownify import markdownify  # noqa: E402

import mk  # noqa: E402


def field(s):
    return s.replace("∅", "").replace("⏎", "\n").replace("⇥", "\t").replace("␣", " ")


def convert(html, opts):
    try:
        return markdownify(html, **mk.OPTIONS[opts])
    except Exception as e:  # noqa: BLE001
        return "raised %s: %s" % (type(e).__name__, e)


def main():
    with open("data/jobs.tsv", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]
    for line in lines:
        if line.startswith("#"):
            print(line)
            continue
        print("-- " + line.replace("\t", " | "))
        w = line.split("\t")
        if w[0] == "page":
            with open("data/pages/" + w[1], encoding="utf-8") as f:
                html = f.read()
            print(convert(html, w[2]))
            print("-- end")
        elif w[0] == "frag":
            print("   " + repr(convert(field(w[2]), w[1])))


main()
