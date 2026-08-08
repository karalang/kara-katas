#!/usr/bin/env python3
"""Join placement spread against claim margin (kara B-2026-08-07-25).

A wide placement spread is not by itself a problem, and a narrow margin against
a comparator is not either. What is a problem is the COMBINATION: a kata that
claims parity to within 0.1% while its own number swings 5% across code
placements is publishing a margin smaller than its measurement error, and a
reader who rebuilds it can get the opposite result.

So the flag is `spread - 1 >= margin`: the placement range is at least as large
as the distance being claimed. That ratio, not the spread, is what decides
whether a kata's README needs a caveat.

    placement-risk.py                       # uses ./placement-spread.json
    placement-risk.py --threshold 1.0       # tighten/loosen the flag
"""
import argparse
import json
import pathlib
import statistics

ROOT = pathlib.Path(__file__).resolve().parent.parent
COMPARATORS = ("rust_ovf", "rust", "c", "go")


def margins(feed):
    """{(kata_id, approach): (margin, comparator, ratio)} over the seq lane."""
    out = {}
    for k in feed["katas"]:
        kid = k["kata"]["id"]
        idx = {}
        for m in k["measurements"]:
            if m["lane"] != "seq":
                continue
            if m["lang"] == "kara" and m.get("mode") != "codegen":
                continue
            if m["lang"] != "kara" and m.get("mode") != "native":
                continue
            v = (m.get("runtime") or {}).get("mean_ms")
            if v:
                idx[(m["lang"], m.get("approach"))] = v
        for (lang, app), v in idx.items():
            if lang != "kara":
                continue
            best = None
            for c in COMPARATORS:
                cv = idx.get((c, app))
                if not cv:
                    continue
                g = abs(v / cv - 1.0)
                if best is None or g < best[0]:
                    best = (g, c, v / cv)
            if best:
                out[(kid, app)] = best
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spread", default=str(ROOT / "placement-spread.json"))
    ap.add_argument("--feed", default=str(ROOT / "bench-results.json"))
    ap.add_argument("--threshold", type=float, default=1.0,
                    help="flag when (spread-1)/margin >= this")
    args = ap.parse_args()

    spread = json.load(open(args.spread))
    marg = margins(json.load(open(args.feed)))

    rows = []
    for r in spread["results"]:
        if "spread" not in r:
            continue
        stem = pathlib.Path(r["source"]).stem
        # The screen names a source file; the feed names an approach. They agree
        # for single-approach katas and the stem IS the approach for the rest.
        m = marg.get((r["id"], stem))
        if m is None:
            cands = [v for (kid, _), v in marg.items() if kid == r["id"]]
            m = min(cands) if cands else None
        if m is None:
            continue
        margin, comp, ratio = m
        # `excess` is spread net of the kata's own control: run-to-run noise
        # averages out of a published hyperfine mean, placement does not.
        excess = r.get("excess", r["spread"]) - 1.0
        risk = excess / margin if margin > 1e-9 else float("inf")
        rows.append((risk, r["id"], r["slug"], stem, r.get("excess", r["spread"]), margin, comp, ratio))

    rows.sort(reverse=True)
    sp = [r[4] for r in rows]
    print(f"{len(rows)} kata/approach pairs joined")
    print(f"placement spread: median {statistics.median(sp):.4f}  "
          f"p90 {sorted(sp)[int(len(sp) * 0.9)]:.4f}  max {max(sp):.4f}")
    for t in (1.01, 1.02, 1.05, 1.10):
        print(f"  spread >= {t:.2f}: {sum(1 for s in sp if s >= t):>3}")

    flagged = [r for r in rows if r[0] >= args.threshold]
    print(f"\nFLAGGED (placement range >= claimed margin): {len(flagged)}\n")
    print(f"{'risk':>7} {'kata':>6} {'approach':<18} {'excess':>7} {'margin':>7} "
          f"{'vs':<9} {'ratio':>6}  slug")
    for risk, kid, slug, stem, s, margin, comp, ratio in flagged[:40]:
        rr = "inf" if risk == float("inf") else f"{risk:.1f}x"
        print(f"{rr:>7} {kid:>6} {stem[:17]:<18} {s:>7.4f} {margin * 100:>6.1f}% "
              f"{comp:<9} {ratio:>6.3f}  {slug[:34]}")


main()
