#!/usr/bin/env python3
"""Screen a kata for CODE-PLACEMENT sensitivity (kara B-2026-08-07-25).

WHY THIS EXISTS. On arm64 a kata's runtime can be a function of its code's
address mod 64. kata:170 spans 0.970..1.269 across placements -- a 1.31x range
-- so the single number in its README and in bench-results.json is ONE DRAW
from a wide distribution. A reader who rebuilds it on their own machine can
land ~30% away from our published figure with nothing on file to explain it.
The corpus has never been checked for how common that is.

WHAT IT MEASURES. Not a headline number -- a SPREAD. The kata is built at
several code placements via `KARAC_TEXT_PAD` (kara c538a878), which moves
`main` by a chosen number of bytes while leaving every instruction of the
program identical, and the ratio of the slowest placement to the fastest is
reported. Cycles come from kara's `scripts/pmc.c`; MIN over runs is the
statistic, because min is the robust one under a noisy host and the effect
being screened for is large.

FOUR PLACEMENTS, NOT EIGHT, IS DELIBERATE. This is a screen: it has to be
cheap enough to run over the whole corpus, and it only has to separate
"tight" from "needs a proper look". Four points 16 bytes apart across one
64-byte period recover 1.23x of kata:170's true 1.30x and 1.02x of kata:71's
1.03x -- enough to rank and flag, not enough to quote. Anything it flags gets
the 8-placement treatment by hand.

Usage:
    placement-spread.py --kata 170                 # one kata by id
    placement-spread.py --all --out spread.json    # whole corpus
"""
import argparse
import json
import os
import pathlib
import re
import shutil
import statistics
import subprocess
import sys
import tempfile

PADS = [4, 20, 36, 52]
NUM = re.compile(r"instructions=(\d+) cycles=(\d+)")
ROOT = pathlib.Path(__file__).resolve().parent.parent


def find_pmc():
    for c in (ROOT.parent / "kara/scripts/pmc.c",):
        if c.exists():
            out = pathlib.Path(tempfile.gettempdir()) / "kk_pmc"
            if not out.exists() or c.stat().st_mtime > out.stat().st_mtime:
                subprocess.run(["cc", "-O2", "-o", str(out), str(c)], check=True)
            return str(out)
    raise SystemExit("pmc.c not found next to the kara checkout")


def run_once(pmc, binary, timeout):
    p = subprocess.run([pmc, binary], capture_output=True, text=True, timeout=timeout)
    m = NUM.search(p.stderr)
    if not m:
        raise RuntimeError(f"no counters: {p.stderr[:200]!r}")
    return int(m.group(2)), p.stdout.strip()


def screen(src, sink, karac, pmc, runs, timeout):
    """-> dict for one .kara bench source, or {'error': ...}.

    INTERLEAVED, and this is not a detail. Timing each placement as its own
    consecutive BLOCK lets machine drift over the block accumulate into the
    spread and be read as placement: on the first corpus run, done that way,
    kata:71 reported 1.1976 against a hand-measured truth of 1.0318. kara
    B-2026-08-07-10 records the same trap producing a convincing false 2.8%
    step on x86 that dissolved to 1.004 once interleaved. Every round therefore
    runs every placement once, in a rotated order.

    The CONTROL arm is a second, independently built binary at the first pad --
    byte-identical content, different file. Its ratio against that pad is the
    floor: whatever it reports is what this kata's measurement noise looks like
    on this host right now, and a `spread` that does not clear `control` is not
    evidence of anything.
    """
    work = tempfile.mkdtemp(prefix="pspread-")
    try:
        stem = pathlib.Path(src).stem
        outs = {}
        arms = []  # (name, pad, path)
        for pad in PADS + [PADS[0]]:
            name = f"pad{pad}" if len(arms) < len(PADS) else "control"
            env = dict(os.environ, KARAC_AUTO_PAR="0", KARAC_TEXT_PAD=str(pad))
            b = subprocess.run([karac, "build", str(src)], cwd=work, env=env,
                               capture_output=True, text=True, timeout=600)
            out = pathlib.Path(work) / stem
            if b.returncode != 0 or not out.exists():
                return {"error": f"build failed at pad={pad}: {b.stderr.strip()[:200]}"}
            binary = str(pathlib.Path(work) / f"{stem}.{name}")
            out.rename(binary)
            arms.append((name, pad, binary))

        cyc = {name: [] for name, _, _ in arms}
        for name, _, binary in arms:  # warm: first exec of a fresh binary is XProtect-scanned
            _, got = run_once(pmc, binary, timeout)
            outs[name] = got
        for r in range(runs):
            for name, _, binary in arms[r % len(arms):] + arms[: r % len(arms)]:
                c, got = run_once(pmc, binary, timeout)
                if got != outs[name]:
                    return {"error": f"{name} is not deterministic: {got!r} vs {outs[name]!r}"}
                cyc[name].append(c)
        mins = {name: min(v) for name, v in cyc.items()}
        real = {pad: mins[f"pad{pad}"] for pad in PADS}
        ctrl_hi = max(mins["control"], mins[f"pad{PADS[0]}"])
        ctrl_lo = min(mins["control"], mins[f"pad{PADS[0]}"])

        # The load-bearing check is that every PLACEMENT agrees with every other:
        # the binaries differ only in where the code sits, so a disagreement is a
        # miscompile, and it is worth far more than a timing number. The feed's
        # `kata.sink` is only advisory here -- it is recorded per KATA while a
        # kata may carry several approaches with different sinks (kata:1's
        # brute_force and hash_map), so a mismatch against it is a note, not a
        # failure.
        answers = set(outs.values())
        if len(answers) > 1:
            return {"error": f"OUTPUT DIFFERS ACROSS PLACEMENTS (miscompile): {sorted(answers)!r}"}
        got = next(iter(answers))
        lo, hi = min(real.values()), max(real.values())
        out = {
            "pads": real,
            "min_cycles": lo,
            "max_cycles": hi,
            "spread": hi / lo,
            "control": ctrl_hi / ctrl_lo,
            "excess": (hi / lo) / (ctrl_hi / ctrl_lo),
            "median_cycles": statistics.median(real.values()),
            "output": got,
        }
        if sink is not None and got != sink:
            out["sink_note"] = f"feed sink {sink!r} != program output {got!r} (multi-approach kata?)"
        return out
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kata", action="append", default=[])
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--runs", type=int, default=5)
    ap.add_argument("--timeout", type=float, default=120.0)
    ap.add_argument("--karac", default="karac")
    ap.add_argument("--out", default=None)
    ap.add_argument("--feed", default=str(ROOT / "bench-results.json"))
    args = ap.parse_args()

    pmc = find_pmc()
    feed = json.load(open(args.feed))
    want = set(args.kata)
    katas = [k for k in feed["katas"] if args.all or k["kata"]["id"] in want]
    if not katas:
        raise SystemExit("no katas selected (use --kata ID or --all)")

    results = []
    for k in katas:
        kid, slug, group = k["kata"]["id"], k["kata"]["slug"], k["kata"]["group"]
        sink = k["kata"].get("sink")
        dirs = list((ROOT / "leetcode").glob(f"{group}/{kid}-*/bench"))
        if not dirs:
            results.append({"id": kid, "slug": slug, "error": "no bench dir"})
            continue
        for src in sorted(dirs[0].glob("*.kara")):
            try:
                r = screen(src, sink, args.karac, pmc, args.runs, args.timeout)
            except Exception as e:  # a screen must never abort the sweep
                r = {"error": f"{type(e).__name__}: {e}"}
            r.update({"id": kid, "slug": slug, "source": str(src.relative_to(ROOT))})
            results.append(r)
            tag = r.get("error") or (f"spread {r['spread']:.4f}  ctrl {r['control']:.4f}"
                                     f"  excess {r['excess']:.4f}")
            print(f"  kata:{kid:<5} {src.stem:<22} {tag}", flush=True)

    ok = [r for r in results if "spread" in r]
    if ok:
        ok.sort(key=lambda r: -r["spread"])
        print(f"\n{len(ok)} screened, {len(results) - len(ok)} failed")
        print(f"median spread {statistics.median(r['spread'] for r in ok):.4f}")
        print(f"median control {statistics.median(r['control'] for r in ok):.4f}")
        print("widest by EXCESS over own control:")
        for r in sorted(ok, key=lambda x: -x["excess"])[:14]:
            print(f"  excess {r['excess']:.4f}  spread {r['spread']:.4f}  ctrl {r['control']:.4f}"
                  f"  kata:{r['id']} {r['slug']}")
    if args.out:
        pathlib.Path(args.out).write_text(json.dumps(
            {"pads": PADS, "runs": args.runs, "results": results}, indent=1) + "\n")
        print(f"\nwrote {args.out}")


main()
