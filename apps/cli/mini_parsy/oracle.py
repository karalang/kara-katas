"""Runs data/jobs.txt through the vendored parsy 2.2 and the grammars in
grammars.py, printing what each job gives: the value's repr, or the error.

Run: python3 -I -B oracle.py > expected.out"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))
sys.path.insert(0, HERE)

from parsy import ParseError, line_info_at, string  # noqa: E402

import grammars  # noqa: E402
from grammars import GRAMMARS, START, STOP  # noqa: E402

BS = chr(92)


def unesc(s):
    out = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == BS:
            n = s[i + 1]
            if n == "n":
                out.append("\n")
            elif n == "t":
                out.append("\t")
            elif n == "r":
                out.append("\r")
            elif n == BS:
                out.append(BS)
            elif n == "x":
                j = s.index("}", i)
                out.append(chr(int(s[i + 3 : j], 16)))
                i = j + 1
                continue
            i += 2
            continue
        out.append(c)
        i += 1
    return "".join(out)


def tokens_of(spec):
    out = []
    for t in spec.split("|") if spec else []:
        if t == "START":
            out.append(START)
        elif t == "STOP":
            out.append(STOP)
        elif t.startswith("#"):
            out.append(int(t[1:]))
        else:
            out.append(unesc(t))
    return out


def read_doc(name):
    with open(os.path.join(HERE, "data", "docs", name), encoding="utf-8", newline="") as f:
        return f.read()


def shown(text):
    r = repr(text)
    if len(r) > 70:
        return f"<{len(text)} characters>"
    return r


def attempt(fn):
    try:
        return "  " + repr(fn())
    except ParseError as e:
        return f"  ! ParseError: {e}"
    except ValueError as e:
        return f"  ! ValueError: {e}"
    except AttributeError as e:
        return f"  ! AttributeError: {e}"


PIPES = {
    "logo": ("logo_lexer", "logo_program"),
    "eval": ("eval_lexer", "eval_tokens"),
    "query": ("query_lexer", "query_parser"),
}


def run(n, name, mode, arg):
    if mode == "tokens":
        stream = tokens_of(arg)
        print(f"== {n} {name} tokens {stream!r}")
        print(attempt(lambda: GRAMMARS[name]().parse(stream)))
        return
    if mode == "lineinfo":
        text, idx = arg.rsplit(" ", 1)
        text = unesc(text)
        print(f"== {n} line_info_at({text!r}, {idx})")
        print(attempt(lambda: line_info_at(text, int(idx))))
        return
    if mode == "become_twice":
        print(f"== {n} become twice")
        dec = GRAMMARS["forward_unset"]()
        other = string("X")
        dec.become(other)
        print(attempt(lambda: dec.parse("X")))
        print(attempt(lambda: dec.become(other)))
        return
    text = read_doc(arg[1:]) if arg.startswith("@") else unesc(arg)
    label = arg if arg.startswith("@") else shown(text)
    print(f"== {n} {name} {mode} {label}")
    if mode == "parse":
        print(attempt(lambda: GRAMMARS[name]().parse(text)))
    elif mode == "partial":
        print(attempt(lambda: GRAMMARS[name]().parse_partial(text)))
    elif mode == "partial_parse":
        # parse_partial, then parse on the same parser
        p = GRAMMARS[name]()
        print(attempt(lambda: p.parse_partial(text)))
        print(attempt(lambda: p.parse(text)))
    elif mode == "lines":
        p = GRAMMARS[name]()
        for k, line in enumerate(text.split("\n")):
            if line:
                print(f"  line {k + 1}:")
                print("  " + attempt(lambda: p.parse(line)))
    elif mode == "pipe":
        lexer, parser = PIPES[name]
        toks = None
        try:
            toks = GRAMMARS[lexer]().parse(text)
            print(f"  tokens {toks!r}")
        except ParseError as e:
            print(f"  ! ParseError: {e}")
        if toks is not None:
            print(attempt(lambda: GRAMMARS[parser]().parse(toks)))
    else:
        raise SystemExit(f"unknown mode {mode}")


def main():
    with open(os.path.join(HERE, "data", "jobs.txt"), encoding="utf-8") as f:
        jobs = [line.rstrip("\n").split("\t") for line in f if line.strip()]
    for n, job in enumerate(jobs, 1):
        name, mode = job[0], job[1]
        arg = job[2] if len(job) > 2 else ""
        run(n, name, mode, arg)


main()
