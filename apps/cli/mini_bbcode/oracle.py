#!/usr/bin/env python3
"""Replays data/jobs.tsv through the vendored bbcode library and writes
expected.out. Each @JOB block is a named BBCode input; the oracle renders it
with bbcode.Parser(replace_links=False).format() and prints, per job,

    === <name> ===
    <rendered HTML, with backslash/newline/tab escaped onto one line>

mini_bbcode.kara reproduces this byte-for-byte on every backend. The tokenizer
walks left-to-right with a tag stack and looks tags up by name — never an
iteration over a hash map — so the output is deterministic. Run: python3 -I."""
import sys

sys.path.insert(0, "vendor")
import bbcode  # noqa: E402


def read_blocks(path):
    jobs = []
    name = None
    body = None
    for line in open(path, encoding="utf-8").read().split("\n"):
        if line.startswith("@JOB "):
            name = line[5:]
            body = []
        elif line == "@END":
            jobs.append((name, "\n".join(body)))
            name = None
            body = None
        elif body is not None:
            body.append(line)
    return jobs


def esc(s):
    return s.replace("\\", "\\\\").replace("\n", "\\n").replace("\t", "\\t")


def main():
    parser = bbcode.Parser(replace_links=False)
    out = []
    for name, inp in read_blocks("data/jobs.tsv"):
        out.append("=== %s ===" % name)
        out.append(esc(parser.format(inp)))
    sys.stdout.write("\n".join(out) + "\n")


main()
