#!/usr/bin/env python3
"""Check that every bench's PAR row measures a binary built with auto-par ON.

WHY THIS EXISTS. `scripts/new-bench.sh` stamps out a seq-only harness whose
`build_kara()` sets `KARAC_AUTO_PAR=0` — correct for a kata with one lane. When
a par lane is added by hand it is natural to point the new row at the binary
that helper already produces, and the result compiles the `#[par_order_free]`
source with the auto-parallelizer switched off. `KARAC_AUTO_PAR=0` is that
pass's kill switch and the attribute is an opt-in hint TO the pass, not an
explicit `par {}` block, so what comes out is an ordinary sequential binary and
the par row silently measures the seq lane.

It is worse than a wrong number, because it is INTERMITTENT: the generated
helper rebuilds only when the source or `karac` is newer than the output, so a
binary left over from an auto-par build survives and the run reports honest
figures. Whether a bench measures what it claims then depends on file mtimes.
Measured on kata 277: 0.30s with the switch on, 0.07s with it off, same source.

THE RULE. A row tagged `--lane par --mode codegen` must not name a binary whose
only producer sets `KARAC_AUTO_PAR=0`.
"""

import re
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, check=True).stdout.strip()
FILES = subprocess.run(["git", "ls-files", "--", "*/bench/bench.sh"],
                       capture_output=True, text=True, check=True, cwd=ROOT).stdout.split()

PAR_ROW = re.compile(r'--lane par --mode codegen[^\n]*\n?[^\n]*--cmd "([^"]+)"')
# The `{` may be followed by a trailing comment, so anchor on the brace, not
# on end-of-line.
FUNC = re.compile(r'^([A-Za-z_][A-Za-z0-9_]*)\(\)\s*\{[^\n]*$(.*?)^\}$', re.M | re.S)
OUT_LOCAL = re.compile(r'local out="([^"]+)"')
BUILD_O = re.compile(r'(KARAC_AUTO_PAR=0\s+)?karac build[^\n]*?-o "([^"]+)"')


def norm(path, stem):
    """Collapse the two spellings of the stem variable so paths compare equal."""
    return (path.replace("${STEM}", stem).replace("${stem}", stem)
                .replace("$STEM", stem).replace("./", ""))


def producers(text, stem):
    """{normalized output path: set of bools — was auto-par killed for it}."""
    out = {}
    for name, body in FUNC.findall(text):
        killed = "KARAC_AUTO_PAR=0" in body
        for p in OUT_LOCAL.findall(body):
            out.setdefault(norm(p, stem), set()).add(killed)
    # Top-level `karac build ... -o PATH` lines, outside any helper.
    stripped = FUNC.sub("", text)
    for kill, p in BUILD_O.findall(stripped):
        out.setdefault(norm(p, stem), set()).add(bool(kill))
    return out


def main():
    bad = []
    checked = 0
    for rel in FILES:
        text = open(f"{ROOT}/{rel}").read()
        m = PAR_ROW.search(text)
        if not m:
            continue
        checked += 1
        stem_m = re.search(r'^STEM=(\S+)', text, re.M)
        stem = stem_m.group(1) if stem_m else "STEM"
        path = norm(m.group(1), stem)
        kinds = producers(text, stem).get(path)
        if kinds is None:
            # The binary is produced some way this checker cannot see. Not a
            # failure — say so rather than pretend the file was verified.
            print(f"lint-par-lane: NOTE — {rel}: could not locate the producer "
                  f"of '{path}'; not verified")
            continue
        if kinds == {True}:
            bad.append((rel, path))

    if bad:
        print("lint-par-lane: FAIL — a PAR row measures a binary built with "
              "KARAC_AUTO_PAR=0 (so it measures the SEQ lane):", file=sys.stderr)
        for rel, path in bad:
            print(f"  {rel}  ->  {path}", file=sys.stderr)
        print(file=sys.stderr)
        print("  Fix: give the par binary its own helper that runs plain "
              "`karac build` (no KARAC_AUTO_PAR=0) and writes a distinct path,",
              file=sys.stderr)
        print("  e.g. target/<stem>_par_kara, then point the par row at it.",
              file=sys.stderr)
        return 1

    print(f"lint-par-lane: OK — {checked} bench(es) with a PAR row build it "
          f"with auto-par ON")
    return 0


sys.exit(main())
