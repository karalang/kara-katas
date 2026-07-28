#!/usr/bin/env python3
"""Stamp hand-written "## Benchmarks" sections with their snapshot date.

Usage: stamp-bench-staleness.py [--check] <kata-dir> [<kata-dir> ...]

167 kata READMEs carry a hand-written Benchmarks section — prose plus tables,
with ### subsections. 97 of them quote a snapshot date older than the kata's own
results.json and 60 quote no date at all, so a reader has no way to tell whether
the numbers in front of them are current. 130 additionally make a directional
claim about Kāra ("ahead of C", "leads Rust") resting on those numbers.

Those sections cannot simply be regenerated: the analysis in them is the
valuable part and does not rot the way the figures do. So this stamps a dated
notice at the top of each stale section instead, scoping the numbers as a
snapshot without touching a word of the argument.

Deliberately NOT stamped:
  * generated sections (inject-bench-readme.py keeps those current already)
  * sections whose quoted date is >= the kata's measured_at

Idempotent: an existing stamp is replaced, so re-running after a re-bench
refreshes the dates rather than stacking notices.
"""
import json
import sys
import os
import re

GEN_SIG = "The kata's tiny fixed inputs aren't a workload"
MARKER = "<!-- bench-staleness -->"
SECTION_RE = re.compile(r"(\n## Benchmarks\n)(.*?)(?=\n## |\Z)", re.DOTALL)
DATE_RE = re.compile(r"20\d\d-\d\d-\d\d")
# An existing stamp: the marker plus the blockquote that follows it.
STAMP_RE = re.compile(
    re.escape(MARKER) + r"\n(?:>[^\n]*\n)+\n?", re.MULTILINE
)


def is_generated(body):
    return GEN_SIG in body and "\n### " not in body


def build_stamp(readme_date, measured_at, has_claims):
    # No nested bold: the emphasis spans the whole lead clause, so the dates
    # inside it must stay plain or the markdown renders literal asterisks.
    if readme_date:
        when = f"are a {readme_date} snapshot; the feed was last measured {measured_at}"
    else:
        when = f"are undated; the feed was last measured {measured_at}"
    lines = [
        MARKER,
        f"> **Figures in this section {when}.** Where the two disagree, "
        "[`bench/results.json`](bench/results.json) and the "
        "[charts](../../../BENCHMARKS.md) are current; the numbers below are "
        "kept because the analysis around them explains *why* the shape is what "
        "it is, and that reasoning outlives the milliseconds.",
    ]
    if has_claims:
        lines.append(
            "> Comparative claims below (\"ahead of C\", \"leads Rust\", ratios) "
            "were true of the snapshot and have **not** been re-verified against "
            "the current feed — treat them as historical, not as the standing "
            "result."
        )
    return "\n".join(lines) + "\n"


CLAIM_RE = re.compile(
    r"(leads?\s+(?:C|Rust|Go)\b|ahead of\b|beats?\b|fastest\b|faster than\b"
    r"|outruns?\b|wins?\b|edges? out\b)",
    re.I,
)


def has_kara_claim(body):
    for s in re.split(r"(?<=[.!?])\s+", body):
        if CLAIM_RE.search(s) and re.search(r"k[āa]ra", s, re.I):
            return True
    return False


def process(kata_dir, check=False):
    rj = os.path.join(kata_dir, "bench", "results.json")
    rd = os.path.join(kata_dir, "README.md")
    if not (os.path.exists(rj) and os.path.exists(rd)):
        return "skip-missing"
    measured = json.load(open(rj)).get("env", {}).get("measured_at", "")[:10]
    if not measured:
        return "skip-no-date"

    text = open(rd).read()
    out = []
    last = 0
    changed = False

    for m in SECTION_RE.finditer(text):
        head, body = m.group(1), m.group(2)
        clean = STAMP_RE.sub("", body, count=1)
        if is_generated(clean):
            continue
        dates = sorted(set(DATE_RE.findall(STAMP_RE.sub("", body))))
        newest = dates[-1] if dates else None
        # Current prose needs no notice; drop any stamp it used to carry.
        # When no stamp is warranted the body is left byte-for-byte alone —
        # stripping leading whitespace here silently ate a blank line on every
        # section that did not need stamping.
        if newest is None or newest < measured:
            stamp = build_stamp(newest, measured, has_kara_claim(clean))
            new_body = stamp + "\n" + clean.lstrip("\n")
        else:
            new_body = clean
        if new_body != body:
            changed = True
        out.append((m.start(2), m.end(2), new_body))

    if not changed:
        return "unchanged"
    if check:
        return "would-stamp"

    buf = []
    for start, end, new_body in out:
        buf.append(text[last:start])
        buf.append(new_body)
        last = end
    buf.append(text[last:])
    open(rd, "w").write("".join(buf))
    return "stamped"


def main():
    args = sys.argv[1:]
    check = "--check" in args
    dirs = [a for a in args if a != "--check"]
    tally = {}
    for d in dirs:
        r = process(d, check)
        tally[r] = tally.get(r, 0) + 1
    for k, v in sorted(tally.items(), key=lambda kv: -kv[1]):
        print(f"  {k:16} {v}")


if __name__ == "__main__":
    main()
