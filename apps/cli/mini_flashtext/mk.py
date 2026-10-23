#!/usr/bin/env python3
r"""Writes data/jobs.tsv: a command stream driving a KeywordProcessor, one
command per line. oracle.py replays it through the vendored flashtext library;
mini_flashtext.kara replays it through the ported trie. The commands:

    case <0|1>        start a fresh processor (1 = case-sensitive)
    nwb <chars>       set the non-word-boundary set to exactly these chars
    add <kw>[|<clean>]  add a keyword (clean name defaults to the keyword)
    addlist <a,b,c>   add several keywords (clean name = keyword)
    rm <kw>           remove a keyword            -> True/False status
    has <word>        membership test             -> True/False
    get <word>        clean name for an exact term-> clean name or None
    len               number of distinct terms    -> count
    extract <text>    keywords found, in text order (joined by " | ")
    span <text>       the same with clean:start:end spans
    replace <text>    text with keywords swapped for their clean names

No flashtext import here (only literal commands). All input is ASCII; the trie,
boundary set and lowering are byte-level, so the port is integer/string only."""

COMMANDS = [
    "case 0",
    "add Big Apple|New York",
    "add Bay Area",
    "len",
    "has Big Apple",
    "has big apple",
    "has Big",
    "get Big Apple",
    "get nope",
    "extract I love Big Apple and Bay Area.",
    "extract i love big apple and bay area.",
    "replace I love Big Apple and bay area.",
    "span I love Big Apple and Bay Area.",
    "case 0",
    "add Big|B",
    "add Big Apple|BA",
    "extract Big and Big Apple here",
    "replace Big and Big Apple here",
    "case 1",
    "add Java|java-lang",
    "add java|coffee",
    "extract I code Java and java daily",
    "replace I code Java and java daily",
    "len",
    "case 0",
    "addlist python,golang,rust",
    "len",
    "extract i use python, golang and RUST today",
    "rm golang",
    "rm golang",
    "len",
    "extract golang and rust",
    "case 0",
    "add c++|cpp",
    "nwb +",
    "add c++|cpp",
    "extract i love c++ a lot",
    "case 0",
    "add new-york|NYC",
    "extract go to new-york now",
    "replace go to new-york now",
    "case 0",
    "add end",
    "extract this is the end",
    "replace this is the end",
    "extract endless summer",
]


def main():
    import os
    os.makedirs("data", exist_ok=True)
    with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
        for cmd in COMMANDS:
            fh.write(cmd + "\n")


main()
