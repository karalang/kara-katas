#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_snowball (tab-separated: op then arg).

Each job is `stem <word>` — run the Porter stemmer on <word>, print the stem.
The word list is chosen to exercise every Porter step: the Step 1a plural
rules (sses/ies/ss/s), the Step 1b past/gerund rules with their e-insert and
consonant-undouble sub-cases, the Step 1c y->i rule, the Step 2/3/4 suffix
derivations across all Among entries, the Step 5 final-e and double-l rules,
and the word-initial / post-vowel y->Y consonant mapping.

mk.py writes only literal inputs (no library import); oracle.py replays every
job against the vendored snowballstemmer library. Words are ASCII lowercase.
See README.md."""
import os

os.makedirs("data", exist_ok=True)

WORDS = [
    # Step 1a — plurals
    "caresses", "ponies", "ties", "caress", "cats", "buses", "glasses",
    "stresses", "flies", "dies", "boss", "ss", "s",
    # Step 1b — -eed / -ed / -ing with sub-cases
    "feed", "agreed", "freed", "plastered", "bled", "motoring", "sing",
    "conflated", "troubled", "sized", "hopping", "tanned", "falling",
    "hissing", "fizzed", "failing", "filing", "fitting", "batting",
    "spying", "meeting", "guaranteed", "disabled", "controlling",
    # Step 1c — y -> i
    "happy", "sky", "cry", "crying", "enjoy", "enjoying", "say",
    "trying", "played", "study", "carry",
    # Step 2
    "relational", "conditional", "rational", "valenci", "hesitanci",
    "digitizer", "conformabli", "radicalli", "differentli", "vilely",
    "analogousli", "vietnamization", "predication", "operator", "feudalism",
    "decisiveness", "hopefulness", "callousness", "formaliti",
    "sensitiviti", "sensibiliti", "organization", "nationalism",
    # Step 3
    "triplicate", "formative", "formalize", "electriciti", "electrical",
    "hopeful", "goodness", "duplicate", "activate",
    # Step 4
    "revival", "allowance", "inference", "airliner", "gyroscopic",
    "adjustable", "defensible", "irritant", "replacement", "adjustment",
    "dependent", "adoption", "homologou", "communism", "angulariti",
    "homologous", "effective", "bowdlerize", "consignment", "disturbance",
    "management", "abstraction", "presumption", "resumption", "embracement",
    # Step 5
    "probate", "rate", "cease", "controll", "roll", "doze", "probable",
    "generalize", "sensational", "rational",
    # y-mapping edge cases
    "y", "yy", "by", "yoyo", "boyish", "playing", "layer", "beauty",
    # common real words
    "running", "jumps", "easily", "fairly", "happily", "generously",
    "connection", "connected", "connecting", "connect", "relate",
    "related", "relatedness", "universal", "university", "universe",
    "argument", "arguments", "agreement", "dependency", "frequently",
    "determination", "determined", "experimental", "experiment",
    "realization", "consistency", "consistent", "distribution",
    "distributed", "distributing", "generalization", "specialization",
    "normalize", "normalized", "normalization", "optimization", "optimizer",
]

lines = ["stem\t%s" % w for w in WORDS]
with open("data/jobs.tsv", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
