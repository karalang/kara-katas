#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_packaging: one PEP 440 job per line.

    <op> \t <payload>

Two ops exercise the vendored ``packaging.version.Version``:

  norm <version>      canonicalize one version string (or detect it is invalid);
  cmp  <a> \x1f <b>   order two version strings.

The version list below walks every PEP 440 feature: the optional ``v`` prefix,
epochs (``1!``), multi-segment release numbers, the pre-release spellings and
their normalization (``alpha``/``a``, ``beta``/``b``, ``c``/``pre``/``preview``
/``rc`` -> ``rc``), implicit pre-release numbers, post releases (``.post``,
``-N`` and ``rev``/``r``), dev releases, and local version segments (numeric and
alphabetic, which order differently). The ``cmp`` jobs pair neighbours and a few
spread-out versions so the comparison key is exercised across every rank.
"""
import os

VERSIONS = [
    "1.0",
    "1.0.0",
    "v2.3.4",
    "0.1",
    "1!2.0",
    "2!1.0",
    "1.0a1",
    "1.0alpha1",
    "1.0a",
    "1.0b2",
    "1.0beta2",
    "1.0c3",
    "1.0pre3",
    "1.0preview3",
    "1.0rc3",
    "1.0.post1",
    "1.0-1",
    "1.0rev2",
    "1.0r2",
    "1.0.dev4",
    "1.0a2.dev3",
    "1.0.post1.dev2",
    "1.0+ubuntu.1",
    "1.0+abc.5",
    "1.0+5",
    "1.0.0.0",
    "1.2.3.4.5",
    "10.20.30",
    "2.0.dev0",
    "1!1.0rc2.post3.dev4+local.7",
]

INVALID = [
    "",
    "foo",
    "1.0.0.0a.b",
    "1..0",
    "1.0+",
    "1.0-",
    "1.0.0rc",
    "01!1.0junk",
]

# cmp pairs: neighbours that differ by exactly one rank, plus a few long jumps.
PAIRS = [
    ("1.0", "1.0.0"),
    ("1.0", "1.1"),
    ("1.0a1", "1.0a2"),
    ("1.0a2", "1.0b1"),
    ("1.0b1", "1.0rc1"),
    ("1.0rc1", "1.0"),
    ("1.0.dev1", "1.0a1"),
    ("1.0", "1.0.post1"),
    ("1.0.post1", "1.0.post1.dev1"),
    ("1.0.post1.dev1", "1.0.post1"),
    ("1!1.0", "2.0"),
    ("1.0+1", "1.0+2"),
    ("1.0+abc", "1.0+1"),
    ("1.0+abc", "1.0+abd"),
    ("1.0+1.0", "1.0+1"),
    ("1.0", "1.0+1"),
    ("1.0alpha1", "1.0a1"),
    ("1.0preview", "1.0rc0"),
    ("1.0r1", "1.0.post1"),
]

US = "\x1f"

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    for v in VERSIONS:
        fh.write("norm\t" + v + "\n")
    for v in INVALID:
        fh.write("norm\t" + v + "\n")
    for a, b in PAIRS:
        fh.write("cmp\t" + a + US + b + "\n")
