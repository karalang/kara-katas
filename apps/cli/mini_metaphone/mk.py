#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_metaphone: one `dm <word>` job per line. Each
job asks for the Double Metaphone (primary, secondary) codes of an ASCII word.
`oracle.py` replays the list against the vendored Metaphone library and prints
`primary|secondary` per line; mini_metaphone.kara reproduces it byte-for-byte.

The word list is drawn from the library's own test suite (ASCII entries only;
the non-ASCII names it also tests exercise NFD normalisation, which is the
documented boundary) plus a spread chosen to reach the many letter contexts the
algorithm branches on — the C/CH/CC/CZ/CIA/SCH/GH/GN/TH/TION/WR/WICZ/X/Z rules,
the silent GN/KN/PN/WR/PS word-starts, the initial-X and SUGAR/ISLAND special
cases, Slavo-Germanic detection, and the spanish `SAN `/`JOSE` space handling."""
import os

WORDS = [
    # straight from the library's test suite
    "aubrey", "richard", "Jose", "cambrillo", "otto", "maurice", "auto",
    "maisey", "catherine", "geoff", "Chile", "katherine", "steven", "zhang",
    "bob", "ray", "Tux", "bryan", "bryce", "Rapelje", "solilijs", "Dallas",
    "Schwein", "dave", "eric", "Parachute", "brian", "randy", "Through",
    "Nowhere", "heidi", "Arnow", "Thumbail", "tolled", "told", "Smith",
    "Schmidt", "Jablonski", "Yablonsky", "Bartosz", "Bartosch", "Bartos",
    # extra contexts: silent starts, special cases, germanic, italian, spanish
    "gnome", "knight", "pneumatic", "wright", "psalm", "xavier", "caesar",
    "chianti", "michael", "czerny", "focaccia", "accident", "bacci", "school",
    "sugar", "island", "mclaughlin", "thomas", "nation", "campbell", "edge",
    "van gogh", "san jacinto", "biaggi", "tagliaro", "cabrillo", "filipowicz",
    "breaux", "resnais", "laugh", "cough", "hugh", "dumb", "thames",
]


def main():
    os.makedirs("data", exist_ok=True)
    with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
        for w in WORDS:
            fh.write("dm\t" + w + "\n")


main()
