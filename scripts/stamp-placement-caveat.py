#!/usr/bin/env python3
"""Stamp a placement caveat onto katas whose margin is narrower than their own
placement range (kara B-2026-08-07-25).

A kata that reports 0.999x against equal-safety Rust while its own runtime moves
47% with code placement alone is publishing a margin far smaller than its
measurement error. The figure is not wrong -- it is one draw -- but a reader has
no way to know that, and rebuilding the kata locally can hand them the opposite
result. This puts that on the page, for the katas where it actually decides the
claim.

WHERE IT WRITES, AND WHY EXACTLY THERE. The block goes IMMEDIATELY BEFORE the
`## Benchmarks` heading, never inside the section. Two machines own that
section and both would eat an insertion:
  * `inject-bench-readme.py` matches `\\n## Benchmarks\\n(.*?)(?=\\n## |\\Z)` and
    REPLACES the body, so anything written inside a generated section is lost on
    the next injection (6 of the katas this flags have generated sections).
  * `stamp-bench-staleness.py` reads the FIRST ISO date inside that section to
    decide whether the section is stale, and its own stamp regex swallows a run
    of `>` blockquote lines.
So the text below also carries NO ISO date and NO bug id -- `B-2026-08-07-25`
contains `2026-08-07`, which that date regex would happily read as this
section's snapshot date and silently suppress its staleness banner.

Idempotent: an existing block is replaced, so re-running after a re-screen
refreshes the numbers rather than stacking notices.

    stamp-placement-caveat.py --check      # list what would change, write nothing
    stamp-placement-caveat.py              # write
"""
import argparse
import importlib.util
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
MARKER = "<!-- placement-caveat -->"
BLOCK_RE = re.compile(re.escape(MARKER) + r"\n(?:[^\n]+\n)+?\n", re.MULTILINE)
HEADING = "\n## Benchmarks\n"

COMP_LABEL = {
    "rust_ovf": "`rustc -O -C overflow-checks=on`",
    "rust": "`rustc -O`",
    "c": "`clang -O3`",
    "go": "`go build`",
}


def load_margins():
    spec = importlib.util.spec_from_file_location(
        "placement_risk", ROOT / "scripts" / "placement-risk.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["placement_risk"] = mod
    src = (ROOT / "scripts" / "placement-risk.py").read_text().replace("\nmain()\n", "\n")
    exec(compile(src, str(ROOT / "scripts" / "placement-risk.py"), "exec"), mod.__dict__)
    return mod.margins(json.load(open(ROOT / "bench-results.json")))


def block_for(excess, margin, comp):
    return (
        f"{MARKER}\n"
        f"**Measurement caveat — code placement.** This kata's runtime moves by up to "
        f"**{excess * 100:.0f}%** with code placement alone: rebuilt with its machine code "
        f"sitting at a different address, the same program, same compiler and same input "
        f"runs that much faster or slower. That is wider than the **{margin * 100:.1f}%** "
        f"margin against {COMP_LABEL.get(comp, comp)} quoted below, so read that comparison "
        f"as a tie rather than as a result. Measured across four code placements against a "
        f"same-binary control — see [`placement-spread.json`](../../../placement-spread.json) "
        f"and [BENCHMARKS.md](../../../BENCHMARKS.md#code-placement-arm64).\n\n"
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--min-excess", type=float, default=0.05)
    ap.add_argument("--min-risk", type=float, default=3.0)
    args = ap.parse_args()

    marg = load_margins()
    spread = json.load(open(ROOT / "placement-spread.json"))

    seen, changed, skipped = set(), [], []
    for r in spread["results"]:
        if "spread" not in r or r["id"] in seen:
            continue
        stem = pathlib.Path(r["source"]).stem
        cand = [v for (kid, _), v in marg.items() if kid == r["id"]]
        m = marg.get((r["id"], stem)) or (min(cand) if cand else None)
        if m is None:
            continue
        margin, comp, _ratio = m
        excess = r.get("excess", r["spread"]) - 1.0
        risk = excess / margin if margin > 1e-9 else float("inf")
        if excess < args.min_excess or risk < args.min_risk:
            continue
        seen.add(r["id"])

        readme = ROOT / pathlib.Path(r["source"]).parent.parent / "README.md"
        if not readme.exists():
            skipped.append((r["id"], "no README"))
            continue
        text = readme.read_text()
        if HEADING not in text:
            skipped.append((r["id"], "no '## Benchmarks' heading"))
            continue
        stripped = BLOCK_RE.sub("", text)
        block = block_for(excess, margin, comp)
        out = stripped.replace(HEADING, "\n" + block + HEADING.lstrip("\n"), 1)
        if out != text:
            changed.append((r["id"], r["slug"], excess, margin))
            if not args.check:
                readme.write_text(out)

    verb = "would stamp" if args.check else "stamped"
    print(f"{verb} {len(changed)} kata README(s)")
    for kid, slug, excess, margin in sorted(changed, key=lambda c: -c[2]):
        print(f"  kata:{kid:<5} excess {excess * 100:>5.1f}%  margin {margin * 100:>4.1f}%  {slug}")
    for kid, why in skipped:
        print(f"  SKIP kata:{kid} — {why}")


main()
