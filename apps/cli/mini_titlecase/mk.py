#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_titlecase: one phrase per line.

The phrases cover the title-casing rules a CMS or publishing pipeline leans on:
the New York Times small-word list (lowercased mid-title, capitalized first and
last), hyphen and slash recursion, the Mc/Mac and Mr/Mrs/Ms/Dr prefixes, the
O'/d'/l' apostrophe form, acronym and mixed-case preservation (AT&T, iPhone),
inline-period and dotted-initial preservation, an all-caps line folded back
down, and subphrase capitalization after a colon.
"""
import os

JOBS = [
    "the quick brown fox",
    "a tale of two cities",
    "gone with the wind",
    "to be or not to be",
    "THE WINTER OF OUR DISCONTENT",
    "x-men: first class",
    "the man from U.N.C.L.E.",
    "it's a wonderful life",
    "O'Brien and O'Malley",
    "mcdonald's farm",
    "vs the world",
    "lord of the rings",
    "e.g. this and that",
    "a a a",
    "HELLO WORLD",
    "iPhone and iPad sales",
    "the lord of the rings: the two towers",
    "step by step",
    "mr smith goes to washington",
    "www.example.com here",
    "AT&T merger",
    "a man, a plan, a canal",
    "well-known fact",
    "http://example.com/path here",
    "and now for something",
]

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    for s in JOBS:
        fh.write(s + "\n")
