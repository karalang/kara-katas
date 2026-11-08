#!/usr/bin/env python3
"""Plays data/script.txt against the vendored Lancaster stemmer
(nltk/stem/lancaster.py from NLTK 3.10.4) and prints the report
mini_lancaster.kara must reproduce byte for byte (README.md has the rules).

Every stem comes from the module; the index, the script and its messages
are the port's own, and README.md gives them in full.

Run from this directory: python3 -I -B oracle.py > expected.out"""
import os
import re
import sys

sys.path.insert(0, "vendor")
from nltk.stem.lancaster import LancasterStemmer  # noqa: E402

USAGE = {
    "stem": "usage: stem WORD...",
    "stem-repeat": "usage: stem-repeat PIECE COUNT",
    "use": "usage: use RULES [prefix]",
    "index": "usage: index DOC",
    "classes": "usage: classes [MIN]",
    "top": "usage: top COUNT",
    "query": "usage: query WORD...",
}

# What a token loses at either end.
PUNCT = ".,;:!?\"'()[]{}«»#"


class Bad(Exception):
    """A problem the port reports in its own words."""


def count(word):
    if not re.fullmatch("[0-9]{1,6}", word):
        raise Bad(f"bad count {word}")
    return int(word)


def tokens(text):
    out = []
    for t in text.split():
        t = t.strip(PUNCT)
        if t:
            out.append(t)
    return out


class Player:
    def __init__(self):
        self.stemmer = LancasterStemmer()
        # name -> (stem -> occurrences, stem -> lower-cased tokens)
        self.docs = {}

    def run(self, words):
        cmd = words[0]
        if cmd not in USAGE:
            raise Bad(f"unknown command {cmd}")
        args = words[1:]
        if cmd in ("stem", "query"):
            ok = len(args) >= 1
        elif cmd == "classes":
            ok = len(args) <= 1
        elif cmd == "use":
            ok = len(args) == 1 or (len(args) == 2 and args[1] == "prefix")
        else:
            ok = len(args) == len(USAGE[cmd].split()) - 2
        if not ok:
            raise Bad(USAGE[cmd])
        return getattr(self, cmd.replace("-", "_"))(args)

    def stem(self, args):
        return [f"{w} -> {self.stemmer.stem(w)}" for w in args]

    def stem_repeat(self, args):
        n = count(args[1])
        word = args[0] * n
        s = self.stemmer.stem(word)
        return [f'{args[0]} x {n}: {len(word)} chars -> {len(s)} chars, ending "{s[-8:]}"']

    def use(self, args):
        name, prefix = args[0], len(args) == 2
        if name == "default":
            rules = None
        else:
            path = os.path.join("data", "rules", name + ".rules")
            if not os.path.exists(path):
                raise Bad(f"no rules {path}")
            with open(path, encoding="utf-8", newline="") as fh:
                text = fh.read()
            rules = tuple(
                line for line in text.split("\n") if line and not line.startswith("#")
            )
        st = LancasterStemmer(rule_tuple=rules, strip_prefix_flag=prefix)
        try:
            st.parseRules()
        except ValueError as e:
            raise Bad(f"ValueError: {e}")
        self.stemmer = st
        self.docs = {}
        how = " with prefixes" if prefix else ""
        return [
            f"using {name}{how}: {len(st._rule_tuple)} rules "
            f"under {len(st.rule_dictionary)} letters"
        ]

    def index(self, args):
        path = os.path.join("data", "docs", args[0] + ".txt")
        if not os.path.exists(path):
            raise Bad(f"no document {path}")
        with open(path, encoding="utf-8", newline="") as fh:
            toks = tokens(fh.read())
        counts, forms = {}, {}
        for t in toks:
            s = self.stemmer.stem(t)
            counts[s] = counts.get(s, 0) + 1
            forms.setdefault(s, set()).add(t.lower())
        self.docs[args[0]] = (counts, forms)
        return [f"indexed {args[0]}: {len(toks)} tokens, {len(counts)} stems"]

    def classes(self, args):
        least = count(args[0]) if args else 2
        forms = {}
        for _, f in self.docs.values():
            for s, ws in f.items():
                forms.setdefault(s, set()).update(ws)
        out = [
            f"{s}: {' '.join(sorted(ws))}"
            for s, ws in sorted(forms.items())
            if len(ws) >= least
        ]
        return out or ["no classes"]

    def top(self, args):
        n = count(args[0])
        if not self.docs:
            return ["index is empty"]
        totals = {}
        for c, _ in self.docs.values():
            for s, k in c.items():
                totals[s] = totals.get(s, 0) + k
        ranked = sorted(totals.items(), key=lambda p: (-p[1], p[0]))
        return [f"{s} {k}" for s, k in ranked[:n]]

    def query(self, args):
        stems = [self.stemmer.stem(w) for w in args]
        hits = []
        for name, (c, _) in self.docs.items():
            if all(s in c for s in stems):
                hits.append((-sum(c[s] for s in stems), name))
        hits.sort()
        out = ["stems: " + " ".join(stems)]
        out += [f"{name} {-neg}" for neg, name in hits]
        if not hits:
            out.append("no document matches")
        return out


def main():
    with open(os.path.join("data", "script.txt"), encoding="utf-8", newline="") as fh:
        lines = fh.read().split("\n")
    p = Player()
    for no, line in enumerate(lines, 1):
        words = [w for w in line.split(" ") if w]
        if not words or words[0].startswith("#"):
            continue
        print("> " + " ".join(words))
        try:
            out = p.run(words)
        except Bad as e:
            out = [f"error: script.txt:{no}: {e}"]
        for o in out:
            print("  " + o)


main()
