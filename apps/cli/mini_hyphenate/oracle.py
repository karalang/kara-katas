#!/usr/bin/env python3
r"""Replays data/jobs.tsv through the vendored Hyphenate library and writes
expected.out: one line per word, the word split at Liang hyphenation points and
joined by '-'. mini_hyphenate.kara reproduces this byte-for-byte on every
backend."""
import sys

sys.path.insert(0, "vendor")
import hyphenate as H  # noqa: E402


def main():
    out = []
    for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
        if line == "":
            continue
        out.append("-".join(H.hyphenate_word(line)))
    sys.stdout.write("\n".join(out) + "\n")


main()
