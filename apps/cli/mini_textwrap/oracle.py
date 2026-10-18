#!/usr/bin/env python3
"""Runs data/jobs.tsv through Python's textwrap and prints expected.out."""
import textwrap

DECODE = {"⏎": "\n", "⇥": "\t", "¤": " ", "␍": "\r", "␋": "\x0b", "␌": "\x0c"}
ENCODE = {v: k for k, v in DECODE.items()}


def decode(field):
    if field.startswith("@"):
        with open("data/" + field[1:]) as f:
            return f.read()
    return "".join(DECODE.get(c, c) for c in field)


def show(s):
    return "".join(ENCODE.get(c, c) for c in s)


def options(spec):
    kw = {}
    if spec == "-":
        return kw
    names = {"ii": "initial_indent", "si": "subsequent_indent", "tabs": "expand_tabs",
             "ts": "tabsize", "rw": "replace_whitespace", "fse": "fix_sentence_endings",
             "blw": "break_long_words", "boh": "break_on_hyphens", "dw": "drop_whitespace",
             "ml": "max_lines", "ph": "placeholder"}
    for part in spec.split(","):
        key, value = part.split("=", 1)
        name = names[key]
        if key in ("ii", "si", "ph"):
            kw[name] = value
        elif key in ("ts", "ml"):
            kw[name] = int(value)
        else:
            kw[name] = value == "1"
    return kw


def lines(ls):
    for line in ls:
        print(f"  |{show(line)}|")


def run(fields):
    kind = fields[0]
    try:
        if kind == "wrap":
            out = textwrap.wrap(decode(fields[3]), width=int(fields[1]), **options(fields[2]))
            lines(out)
            print(f"({len(out)} lines)")
        elif kind == "fill":
            lines([textwrap.fill(decode(fields[3]), width=int(fields[1]), **options(fields[2]))])
        elif kind == "shorten":
            lines([textwrap.shorten(decode(fields[3]), width=int(fields[1]), **options(fields[2]))])
        elif kind == "dedent":
            lines([textwrap.dedent(decode(fields[1]))])
        elif kind == "indent":
            pred = None if fields[2] == "-" else (lambda line: True)
            lines([textwrap.indent(decode(fields[3]), decode(fields[1]), pred)])
        elif kind == "fmt":
            paras = decode(fields[2]).split("\n\n")
            for i, p in enumerate(paras):
                if i > 0:
                    print("  --")
                lines(textwrap.fill(p, width=int(fields[1])).split("\n"))
    except ValueError as e:
        print(f"ValueError: {e}")


with open("data/jobs.tsv") as f:
    for raw in f:
        fields = raw.rstrip("\n").split("\t")
        print("== " + " | ".join(fields))
        run(fields)
