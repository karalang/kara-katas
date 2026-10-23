#!/usr/bin/env python3
"""Writes data/: a few SVG drawings (data/svg/) for a small pen-plotter
tool, and data/jobs.tsv, the script oracle.py and mini_svgpath.kara both
replay.

Each line of jobs.tsv is one step, its fields separated by tabs:

    job      <title>
    parse    <d>                 parse_path(d): its repr() and d(); the
                                 result becomes the current path
    tokens   <d>                 each token _tokenize_path(d) yields
    point    <pos>               the current path's point(pos)
    tangent  <pos>               its tangent(pos)
    length   [<error> [<depth>]] its length(), with error= and min_depth=
    bbox                         its boundingbox()
    seg      <i> <what> [<pos>]  segment i: repr, point, tangent, length
                                 or bbox
    keep     <name>              remember the current path as <name>
    use      <name>              make <name> the current path again
    eq       <name>              current == <name>, current != <name>
    append   <name> <i>          current.append(<name>[i])
    insert   <at> <name> <i>     current.insert(at, <name>[i])
    set      <at> <name> <i>     current[at] = <name>[i]
    del      <at>                del current[at]
    pop      [<at>]              current.pop([at])
    remove   <name> <i>          current.remove(<name>[i])
    index    <name> <i>          current.index(<name>[i])
    count    <name> <i>          current.count(<name>[i])
    has      <name> <i>          <name>[i] in current
    reverse                      current.reverse()
    slice    <a> <b>             current[a:b]
    len                          len(current)
    clear                        current.clear()
    plot     <svg> <out>         the plotter: every <path> in data/svg/<svg>
                                 measured and sampled to G-code in
                                 data/out/<out>

A <pos>, <error> or index is an int when it has no '.' or 'e' in it, a
float otherwise. In a <d> field a backslash escapes itself, a tab (\\t),
a newline (\\n) and a carriage return (\\r); anything else is literal.

Run: python3 -s -P -B mk.py"""
import os

os.makedirs("data/svg", exist_ok=True)

SVG = {
    "icons.svg": """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 24">
  <!-- a toolbar's icons, one 24x24 cell each -->
  <path id="heart" d="M12 21 C 5 15, 1 11, 4 6 C 6 3, 10 3, 12 7 C 14 3, 18 3, 20 6 C 23 11, 19 15, 12 21 Z"/>
  <path id="home" fill="none" d="M27 12 L36 4 L45 12 M29 10 V20 H43 V10 M34 20 v-5 h4 v5"/>
  <path id="check" stroke-width='2' d="m51 12 4.5 4.5L 66,6"/>
  <path id="ring" d="M84 12 a 6 6 0 1 0 -12 0 a 6 6 0 1 0 12 0 z"/>
  <path d="M88 4 l4 0 0 4 -4 0 z"/>
</svg>
""",
    "logo.svg": """<svg xmlns="http://www.w3.org/2000/svg" width="200" height="120">
  <path id="wave"
        d="M10,60 Q35,10 60,60 T110,60 T160,60 T190,60"/>
  <path id="swoosh" d="M20 100 C 60 70, 120 70, 180 100 S 120 115, 20 100"/>
  <path id="leaf" d="M100,20 A40,20 45 0,1 140,60 A40,20 45 0,1 100,20"/>
  <path id="badge" d="M30,20h30a10,10 0 0 1 10,10v20a10,10 0 0 1-10,10h-30a10,10 0 0 1-10-10v-20a10,10 0 0 1 10-10z"/>
</svg>
""",
    "floorplan.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200">
  <g id="walls">
    <path id="outer" d="M 0 0 H 300 V 200 H 0 Z"/>
    <path id="kitchen" d="M 0 0 h 120 v 80 h -120 z m 130 0 h 60 v 80 h -60 z"/>
    <path id="door" d="M 120 120 a 30 30 0 0 0 30 30 L 150 120"/>
    <path id="stairs" d="M200 120 h20 v10 h20 v10 h20 v10 h20 v10"/>
  </g>
</svg>
""",
    "broken.svg": """<svg xmlns="http://www.w3.org/2000/svg">
  <path id="ok" d="M 1 1 L 2 2"/>
  <path id="no-d" stroke="red"/>
  <path id="garbage" d="10 10 L 20 20"/>
  <path id="cut" d="M 0 0 L 10 10 L"/>
  <path id="bad-arc" d="M 0 0 A -5 5 0 0 1 10 10"/>
  <path id="flat-arc" d="M 0 0 A 0 5 0 0 1 10 10"/>
  <path id="comment" d="M 0 0 L 4 4 # then a comment"/>
  <path id="accent" d="M 0 0 L 5 \u00e9"/>
  <path id="empty" d=""/>
</svg>
""",
    "blank.svg": """<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10"></svg>
""",
}

for name, text in SVG.items():
    with open(os.path.join("data/svg", name), "w", encoding="utf-8") as f:
        f.write(text)

L = []


def esc(t):
    return t.replace("\\", "\\\\").replace("\t", "\\t").replace("\n", "\\n").replace("\r", "\\r")


def step(*f):
    L.append("\t".join(str(x) for x in f))


SPEC = [
    "M 100 100 L 300 100 L 200 300 z",
    "M100,200 C100,100 250,100 250,200 S400,300 400,200",
    "M200,300 Q400,50 600,300 T1000,300",
    "M300,200 h-150 a150,150 0 1,0 150,-150 z",
    "M275,175 v-150 a150,150 0 0,0 -150,150 z",
    "M600,350 l 50,-25 a25,25 -30 0,1 50,-25 l 50,-25 a25,50 -30 0,1 50,-25 "
    "l 50,-25 a25,75 -30 0,1 50,-25 l 50,-25 a25,100 -30 0,1 50,-25 l 50,-25",
    "M100,200 C100,100 400,100 400,200",
    "M100,500 C25,400 475,400 400,500",
    "M600,800 C625,700 725,700 750,800 S875,900 900,800",
]
SYNTAX = [
    "m 10 10 20 20 30 0", "M10 10 20 20", "M 0 0 L 10 0 10 10 0 10 z m 20 0 l 10 0",
    "M10-20L.5.5-1e2,3E-1", "M1.5.5.5.5", "M0,0l1-1-1-1z", "M 10 10 a20 20 0 1010 10",
    "\tM\n10\r10 L 20,20", "M 10 10 L 10 10", "M 5 5", "M 0 0 M 10 10 L 20 20",
    "M 0 0 A 0 10 0 0 1 10 10", "M 10 10 A 5 5 0 0 1 10 10", "M 0 0 A 1 1 0 0 1 10 0",
    "M 0 0 A 5 5 30 1 1 3 4", "M 0 0 A 5 5 0 2 1 10 10", "M 0 0 A 3 9 -60 1 0 6 6",
    "L 10 10 20 0", "C 0 10 10 10 10 0", "Q 5 5 10 0", "H 10 V 10", "l 10 10",
    "A 5 5 0 0 1 10 0", "S 10 10 20 0",
    "M 10 10 L 20 20 Z L 30 30", "M 10 10 Z Z", "m 10 10 z m 5 5 z",
    "M 0 0 S 10 10 20 0", "M 0 0 C 0 10 10 10 10 0 S 20 -10 20 0", "M 0 0 T 10 0",
    "M 0 0 Q 5 10 10 0 T 20 0 T 30 0", "M 0 0 C 1 1 2 2 3 3 T 10 0",
    "M 0 0 Q 5 5 10 0 S 15 5 20 0", "M 0 0 c 0 -5 5 -5 5 0 s 5 5 5 0 s 5 -5 5 0",
    "M 0 0 q 5 -5 10 0 t 10 0 t 10 0", "M 1e2 1E2 l -1e1 .5e1", "M 0.000001 1000000 L 1234567 0.00001234",
    "M 123456.5 0 L 0.0001 -0.0", "M -0 -0 l -0 -0", "M 0 0 L 1e400 0", "M 0 0 L 1e-400 5",
    "M 3 3 h 4 v 4 h -4 v -4", "M 0 0 V 5 H 5 v 5 h 5", "M 1 2 3 4 5 6 Z 7 8",
]
ERRORS = [
    "", "   ", "10 10 L 20 20", "M 10", "M 10 10 L 20", "M 10 10 L 20 20 x 30 30",
    "M 0 0 L 10 10 L", "M 0 0 z 10 10", "M 0 0 L . 5", "M 0 0 L - 5", "M 0 0 L e5 5",
    "M 0 0 A -5 5 0 0 1 10 10", "M 0 0 A 5 5 0 0 1", "M 0 0 A 5 5 0", "M 0 0 L 5 \u00e9",
    "M 0 0 L 10 10 # comment", "M,10,10", "M 10 10 L 1.5.5", "M 0 0 C 1 2 3 4",
    "M 0 0 Q 1 1", "M 0 0 L 1 1 2", "Z", "z M 1 1", "M 0 0 L 1 1 Z L 2 2 x", "M 0 0 H",
]

step("job", "the paths of the SVG specification")
for d in SPEC:
    step("parse", esc(d))
    step("bbox")

step("job", "the grammar")
for d in SYNTAX:
    step("parse", esc(d))

step("job", "broken paths")
for d in ERRORS:
    step("parse", esc(d))

step("job", "the tokenizer")
for d in SPEC[:3] + SYNTAX[:12] + ERRORS:
    step("tokens", esc(d))

step("job", "measuring the specification's paths")
for d in SPEC[:5] + SPEC[6:]:
    step("parse", esc(d))
    step("length", "1e-6")
    for pos in ["0", "0.0", "0.25", "0.5", "0.75", "1", "1.0"]:
        step("point", pos)
    for pos in ["0", "0.3", "1.0"]:
        step("tangent", pos)

step("job", "lengths to a given error")
step("parse", esc(SPEC[5]))
step("length", "1e-3")
step("length")
step("parse", esc(SPEC[5]))
step("length", "1e-6", "2")
step("parse", esc(SPEC[5]))
step("length", "1e-6")
for pos in ["0.1", "0.5", "0.9"]:
    step("point", pos)
step("parse", esc(SPEC[1]))
for err, depth in [("1e-2", "0"), ("1e-2", "5"), ("0.5", "0"), ("1", "1"), ("1e-9", "3")]:
    step("parse", esc(SPEC[1]))
    step("length", err, depth)

step("job", "segments one by one")
step("parse", esc("M 0 0 L 10 0 Q 15 5 10 10 C 5 15 0 15 0 10 A 5 5 0 0 1 0 0 Z"))
for i in range(-1, 7):
    step("seg", i, "repr")
for i in range(6):
    for what in ["point", "tangent"]:
        for pos in ["0", "0.5", "1"]:
            step("seg", i, what, pos)
    step("seg", i, "length")
    step("seg", i, "bbox")
step("parse", esc("M 0 0 A 0 5 0 0 1 10 10 A 5 5 0 0 1 10 10"))
for i in [1, 2]:
    for what in ["point", "tangent", "length", "bbox"]:
        step("seg", i, what, "0.5")
step("parse", esc("M 0 0 Q 10 0 20 0 Q 10 0 0 0 Q 10 10 20 20 Q 0 0 0 0"))
for i in range(1, 5):
    step("seg", i, "length")
    step("seg", i, "bbox")
step("parse", esc("M 0 0 Q 0 0 30 40 Q 30 40 30 40 Q -10 0 10 0"))
for i in range(1, 4):
    step("seg", i, "length")
step("parse", esc("L 10 10 Q 20 0 30 10 C 30 20 20 30 10 20"))
step("bbox")
step("point", "0.5")
for i in range(3):
    step("seg", i, "point", "0")
    step("seg", i, "tangent", "1")
    step("seg", i, "bbox")

step("job", "points beyond the ends")
step("parse", esc("M 0 0 L 10 0 L 10 10"))
for pos in ["-0.1", "0", "0.4", "0.5", "0.5000001", "0.9999999999", "1", "1.5", "2"]:
    step("point", pos)
step("parse", esc("L 10 0 L 10 10"))
for pos in ["-0.1", "0.5", "1.5"]:
    step("point", pos)
step("parse", esc("M 0 0 L 1 0 L 1 3"))
step("point", "0.999999999999999")
step("point", "0.25")
step("parse", esc("M 5 5 M 10 10"))
step("length")
for pos in ["0", "0.5", "1"]:
    step("point", pos)
    step("tangent", pos)
step("bbox")

step("job", "comparing paths")
step("parse", esc("M 0 0 L 10 0 L 10 10 Z"))
step("keep", "square")
step("parse", esc("M0,0 L10,0 10,10 z"))
step("eq", "square")
step("parse", esc("m 0 0 l 10 0 l 0 10 z"))
step("eq", "square")
step("parse", esc("M 0 0 L 10 0 L 10 10"))
step("eq", "square")
step("parse", esc("M 0 0 L 10 0 L 10 10 L 0 0"))
step("eq", "square")
step("parse", esc("M 0 0 C 1 1 2 2 3 3"))
step("keep", "c")
step("parse", esc("M 0 0 C 1 1 2 2 3 3 S 5 5 6 6"))
step("keep", "cs")
step("parse", esc("M 0 0 C 1 1 2 2 3 3 C 4 4 5 5 6 6"))
step("eq", "cs")
step("parse", esc("M 0 0 A 5 5 0 0 1 10 0"))
step("keep", "arc")
step("parse", esc("M 0 0 A 5 5 0 0 0 10 0"))
step("eq", "arc")
step("parse", esc("M 0 0 a 5 5 0 0 1 10 0"))
step("eq", "arc")
step("parse", esc("M 0 0 A 5 5 0.0 0 1 10 0"))
step("eq", "arc")
step("parse", esc("M 0 0 Q 1 1 2 2"))
step("keep", "q")
step("parse", esc("M 0 0 Q 1 1 2 2 T 4 0"))
step("keep", "qt")

step("job", "editing a path")
step("parse", esc("M 0 0 L 10 0 L 10 10 L 0 10 Z"))
step("keep", "box")
step("length")
step("point", "0.5")
step("append", "c", 1)
step("len")
step("length")
step("point", "0.5")
step("point", "0.9")
step("insert", 1, "qt", 2)
step("point", "0.5")
step("set", 0, "arc", 0)
step("point", "0.3")
step("del", 2)
step("point", "0.3")
step("pop")
step("pop", 0)
step("pop", 99)
step("index", "box", 3)
step("index", "c", 1)
step("count", "box", 2)
step("has", "box", 4)
step("has", "qt", 2)
step("remove", "box", 3)
step("remove", "box", 3)
step("slice", 1, 3)
step("slice", -2, 99)
step("reverse")
step("len")
step("bbox")
step("seg", 9, "repr")
step("del", 9)
step("set", -1, "q", 1)
step("parse", esc("M 0 0 L 4 0"))
step("keep", "line")
step("parse", esc("M 0 0 L 4 0"))
step("point", "0.5")
step("set", 1, "c", 1)
step("point", "0.5")
step("length")
step("clear")
step("len")
step("bbox")
step("point", "0.5")
step("use", "box")
step("len")
step("eq", "square")
step("use", "line")
step("length")

step("job", "the plotter")
for name in ["icons.svg", "logo.svg", "floorplan.svg", "broken.svg", "blank.svg"]:
    step("plot", name, name.replace(".svg", ".gcode"))

with open("data/jobs.tsv", "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")
