"""Appends data_files() to mini_polib.kara, after the MARK line: each file
data/files.txt lists, as hex, so the program writes its own inputs.

Run from this directory, after mk.py: python3 -I -B gen_kara.py"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "mini_polib.kara")
MARK = "\n// ------------------------------------------------------------ the data\n"


def main():
    src = open(SRC, encoding="utf-8").read()
    at = src.find(MARK)
    if at >= 0:
        src = src[:at]
    names = [n for n in open(os.path.join(HERE, "data", "files.txt")).read().split("\n") if n]
    out = [
        "",
        "// The catalogs mk.py wrote, as hex, so the program carries its inputs.",
        "fn data_files() -> Vec[(String, String)] {",
        "    let mut v: Vec[(String, String)] = Vec.new();",
    ]
    for n in names:
        h = open(os.path.join(HERE, "data", n), "rb").read().hex()
        out.append("    let mut h = String.new();")
        for i in range(0, len(h), 2000):
            out.append(f'    h.push_str("{h[i:i + 2000]}");')
        out.append(f'    v.push(("{n}".to_string(), h));')
    out.append("    v")
    out.append("}")
    open(SRC, "w", encoding="utf-8").write(src + MARK + "\n".join(out) + "\n")


main()
