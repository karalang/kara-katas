#!/usr/bin/env python3
r"""Writes data/jobs.tsv: one word per line to hyphenate. No hyphenate import
here (only literal words); oracle.py replays each through the vendored library
to produce expected.out (the word split at hyphenation points, joined by '-')."""

WORDS = [
    # short words (<=4 chars) are returned whole
    "a", "at", "cat", "fish", "the",
    # common words
    "computer", "dictionary", "algorithm", "beautiful", "hyphenation",
    "programming", "language", "software", "keyboard", "wonderful",
    "important", "different", "necessary", "available", "remember",
    # longer / technical
    "representation", "internationalization", "extraordinary", "phenomenon",
    "encyclopedia", "mississippi", "typography", "antidisestablishmentarianism",
    "counterrevolutionary", "supercalifragilistic", "onomatopoeia", "pseudonym",
    "bookkeeper", "strengths", "queueing", "rhythm", "mnemonic", "aardvark",
    "xylophone", "zeitgeist",
    # the library's exception words
    "associate", "associates", "declination", "obligatory", "philanthropic",
    "present", "presents", "project", "projects", "reciprocity",
    "recognizance", "reformation", "retribution", "table",
    # words with capitals (lowercased before hyphenating)
    "Hyphenation", "COMPUTER", "Representation",
    # words with a non-letter (never matches a pattern, mostly returned whole)
    "O'Brien", "re-enter",
]


def main():
    import os
    os.makedirs("data", exist_ok=True)
    with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
        for w in WORDS:
            fh.write(w + "\n")


main()
