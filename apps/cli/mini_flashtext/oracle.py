#!/usr/bin/env python3
r"""Replays data/jobs.tsv through the vendored flashtext KeywordProcessor and
writes expected.out. Each line is a command (see mk.py); the oracle keeps one
live processor, applies each command, and prints

    <command line> => <result>

one line per command. mini_flashtext.kara reproduces this byte-for-byte on every
backend. The library's extract/replace walk the trie purely by key lookup, so
the output is deterministic and does not depend on Python's dict order."""
import sys

sys.path.insert(0, "vendor")
from flashtext import KeywordProcessor  # noqa: E402


def run(line, state):
    sp = line.find(" ")
    if sp == -1:
        op, arg = line, ""
    else:
        op, arg = line[:sp], line[sp + 1:]
    kp = state["kp"]
    if op == "case":
        state["kp"] = KeywordProcessor(case_sensitive=(arg == "1"))
        return line + " => ok"
    if op == "nwb":
        kp.set_non_word_boundaries(set(arg))
        return line + " => ok"
    if op == "add":
        bar = arg.find("|")
        kw, clean = (arg, None) if bar == -1 else (arg[:bar], arg[bar + 1:])
        st = kp.add_keyword(kw, clean)
        return line + " => " + ("True" if st else "False")
    if op == "addlist":
        kp.add_keywords_from_list([k for k in arg.split(",") if k])
        return line + " => ok"
    if op == "rm":
        return line + " => " + ("True" if kp.remove_keyword(arg) else "False")
    if op == "has":
        return line + " => " + ("True" if (arg in kp) else "False")
    if op == "get":
        g = kp.get_keyword(arg)
        return line + " => " + (g if g is not None else "None")
    if op == "len":
        return line + " => " + str(len(kp))
    if op == "extract":
        return line + " => " + " | ".join(kp.extract_keywords(arg))
    if op == "span":
        r = kp.extract_keywords(arg, span_info=True)
        return line + " => " + " | ".join("%s:%d:%d" % (c, a, b) for (c, a, b) in r)
    if op == "replace":
        return line + " => " + kp.replace_keywords(arg)
    return line + " => ?"


def main():
    state = {"kp": KeywordProcessor(case_sensitive=False)}
    out = []
    for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
        if line == "":
            continue
        out.append(run(line, state))
    sys.stdout.write("\n".join(out) + "\n")


main()
