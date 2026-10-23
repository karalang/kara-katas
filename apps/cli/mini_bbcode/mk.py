#!/usr/bin/env python3
"""Writes data/jobs.tsv: a sequence of named BBCode inputs in a block format
that preserves significant blank lines (list/code bodies span lines). No
library import — the inputs are literal here. Run: python3 -s -P -B mk.py"""
import os

JOBS = [
    ("bold", "[b]hello[/b]"),
    ("nest", "[b]bold [i]and italic[/i][/b]"),
    ("escape", "a < b & c > d \"q\" 'p'"),
    ("cosmetic", "well--- really -- ... (c) (reg) (tm)"),
    ("newlines", "line one\nline two\nline three"),
    ("standalone", "above[hr]below"),
    ("list", "[list]\n[*]first\n[*]second\n[/list]"),
    ("olist", "[list=1]\n[*]one\n[*]two\n[/list]"),
    ("quote", "[quote]  spaced out  [/quote]"),
    ("code", "[code]if a < b:\n    return &amp;[/code]"),
    ("code_embed", "[code]not [b]bold[/b] here[/code]"),
    ("center", "[center]middle[/center]"),
    ("color_name", "[color=red]red text[/color]"),
    ("color_hex6", "[color=#00FF00]green[/color]"),
    ("color_hex3", "[color=#abc]short[/color]"),
    ("color_bad", "[color=123]nope[/color]"),
    ("color_free", "[color red]free[/color]"),
    ("url_abs", "[url]http://example.com/path[/url]"),
    ("url_opt", "[url=http://example.com]visit[/url]"),
    ("url_www", "[url]www.example.com[/url]"),
    ("url_js", "[url]javascript:alert(1)[/url]"),
    ("url_rel", "[url]/relative/path.html[/url]"),
    ("url_optesc", "[url=a<b]link[/url]"),
    ("sub_sup", "H[sub]2[/sub]O and x[sup]2[/sup]"),
    ("strike_u", "[s]gone[/s] and [u]under[/u]"),
    ("unrecognized", "a [blink]tag[/blink] b"),
    ("unclosed", "start [b]never ends"),
    ("empty_tag", "x [] y [/] z"),
    ("same_close", "[list]\n[*]a[*]b\n[/list]"),
    ("deep", "[b][i][u]deep[/u][/i][/b]"),
    ("mixed", "Hi [b]there[/b]!\nA [color=blue]test[/color] with --- dashes."),
    ("quote_author", '[quote author="Dan Watson"]quoted[/quote]'),
    ("adjacent", "[b]one[/b][i]two[/i]"),
    ("text_bracket", "array[0] and dict[key]"),
]


def main():
    os.makedirs("data", exist_ok=True)
    out = []
    for name, inp in JOBS:
        out.append("@JOB " + name)
        out.extend(inp.split("\n"))
        out.append("@END")
    with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")


main()
