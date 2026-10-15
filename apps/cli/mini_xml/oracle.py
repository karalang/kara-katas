# The oracle: the same report as mini_xml, made with Python 3.13's
# xml.etree.ElementTree (and the expat parser under it). Run it from this
# directory after mk.py.
import os
import xml.etree.ElementTree as ET

DOCS = ["feed.xml", "pom.xml", "icon.svg", "config.xml", "sitemap.xml"]

def dump(e, depth):
    line = "  " * depth + e.tag + "".join(f" {k}={v!r}" for k, v in e.attrib.items())
    if e.text and e.text.strip():
        line += f" text={e.text!r}"
    if e.tail and e.tail.strip():
        line += f" tail={e.tail!r}"
    print(line)
    for c in e:
        dump(c, depth + 1)

def show(e):
    if e is None:
        return "None"
    t = (e.text or "").strip()
    return e.tag + (f" {t!r}" if t else "")

trees = {}
for name in DOCS:
    root = ET.parse("data/" + name).getroot()
    trees[name] = root
    print(f"== {name}")
    dump(root, 0)
    print("-- serialized")
    print(ET.tostring(root, encoding="unicode"))

print("== queries")
for line in open("data/queries.txt").read().split("\n")[:-1]:
    name, method, path = line.split("|")
    root = trees[name]
    print(f"{name} {method} {path}")
    if method == "findall":
        for e in root.findall(path):
            print("  " + show(e))
    elif method == "find":
        print("  " + show(root.find(path)))
    elif method == "findtext":
        print(f"  {root.findtext(path)!r}")
    elif method == "itertext":
        print(f"  {''.join(root.find(path).itertext())!r}")

print("== errors")
for name in sorted(os.listdir("data/bad")):
    try:
        ET.parse("data/bad/" + name)
        print(f"{name}: parsed")
    except ET.ParseError as e:
        print(f"{name}: {e}")
