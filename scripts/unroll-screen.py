#!/usr/bin/env python3
"""Screen the corpus for how much of Kāra's deficit to C is the UNROLLER
(kara B-2026-08-15-31).

WHY THIS EXISTS. Every kata compares `karac build` — which runs a `default<O2>`
LLVM pipeline — against `clang -O3`. Those are not the same optimisation
settings, and `-O3`'s loop unroller is the difference that shows up most. On
kata #246 the entire 1.57x deficit was the unroll: against
`clang -O3 -fno-unroll-loops` Kāra is 1.06x, and it is 11% AHEAD of `clang -O2`
on cycles. That raised the obvious question — how many other katas is this true
of — and this script answers it corpus-wide instead of one kata at a time.

WHAT IT MEASURES. Retired instructions, not wall time. Instruction counts are
deterministic, so ONE run per binary is exact and the whole screen is immune to
thermal drift and code placement (see BENCHMARKS.md § Code placement, which is
what makes wall-time screens of this kind unreliable on arm64). Three builds per
program row:

    kara          karac build, KARAC_AUTO_PAR=0   (the published sequential lane)
    c_o3          clang -O3                       (the published comparator)
    c_nounroll    clang -O3 -fno-unroll-loops     (equal-treatment C)

and all three must print the SAME sink or the row is dropped — the screen is
also a 278-way correctness check.

THE CAVEAT THAT MATTERS, and why every row carries a `class`. `-fno-unroll-loops`
does not isolate unrolling: on some loops it also removes the interleaving that
LLVM's vectoriser needs, so C loses SIMD as well. Reading every large mover as
"unrolling" would be wrong — #163 loses 8 NEON ops and 3.45x, which is
vectorisation, while #246 has zero SIMD in both builds and its 1.35x is purely
the scalar unroll. So each row counts NEON/SIMD ops in both C builds and is
labelled:

    pure-unroll     no SIMD lost  -> the B-2026-08-15-31 family
    vectorization   SIMD lost     -> a different question (Kāra's checked
                                     arithmetic forfeits vectorisation;
                                     BENCHMARKS.md § "the cost of the contract")

READ THE RESULT AS A SCREEN, NOT A HEADLINE. A row where C explodes without its
unroller (#190 goes 59.5M -> 1.62B instructions) says C depended on the unroll,
NOT that Kāra was rescued — Kāra is already within 1.14x of `clang -O3` there.
The actionable set is rows that read as "Kāra behind C" and land at parity once
C is treated equally.

    unroll-screen.py                    # whole corpus -> unroll-screen.json
    unroll-screen.py --kata 246         # one kata by id
    unroll-screen.py -o out.json
"""
import argparse
import json
import os
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PMC_SRC = ROOT.parent / "kara" / "scripts" / "pmc.c"
SIMD = re.compile(r"\s(ld1|st1|addv|uaddlv|cnt|tbl|zip1|uzp1)\s|\.16b|\.4s|\.8h|\.2d")


def build_pmc(workdir):
    """`pmc` reports the sink on stdout and `instructions=… cycles=…` on STDERR."""
    pmc = workdir / "pmc"
    if not pmc.exists():
        if not PMC_SRC.exists():
            sys.exit(f"unroll-screen: {PMC_SRC} not found (needs the sibling kara checkout)")
        subprocess.run(["cc", "-O2", "-o", str(pmc), str(PMC_SRC)], check=True)
    return pmc


def pmc_run(pmc, binary, timeout=300):
    try:
        r = subprocess.run([str(pmc), str(binary)], capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None, None
    if r.returncode != 0:
        return None, None
    hit = [l for l in r.stderr.splitlines() if "instructions=" in l]
    if not hit:
        return None, None
    return int(hit[-1].split("instructions=")[1].split()[0]), r.stdout.strip()


def simd_ops(binary):
    if not os.path.exists(binary):
        return None
    return len(SIMD.findall(subprocess.run(["objdump", "-d", str(binary)],
                                           capture_output=True, text=True).stdout))


def program_rows(only):
    """Every (kata, stem) with BOTH a C mirror and a Kāra kernel in bench/."""
    for rj in sorted(ROOT.glob("leetcode/*/*/bench/results.json")):
        b = rj.parent
        kid = json.load(open(rj))["kata"]["id"]
        if only and kid not in only:
            continue
        for csrc in sorted(b.glob("*.c")):
            stem = csrc.stem
            if stem.endswith("_par"):          # par lane is a different comparison
                continue
            ksrc = b / f"{stem}.kara"
            if not ksrc.exists():
                ksrc = b / f"{stem}_seq.kara"  # dual-lane katas (#270, #273)
            if ksrc.exists():
                yield kid, b, stem, csrc, ksrc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kata", action="append", default=[])
    ap.add_argument("-o", "--out", default=str(ROOT / "unroll-screen.json"))
    ap.add_argument("--work", default=None)
    args = ap.parse_args()

    work = pathlib.Path(args.work or (ROOT / "target" / "unroll-screen"))
    work.mkdir(parents=True, exist_ok=True)
    pmc = build_pmc(work)

    env = dict(os.environ, KARAC_AUTO_PAR="0")
    rows, skipped = [], []
    for kid, b, stem, csrc, ksrc in program_rows(set(args.kata)):
        tag = f"{kid}_{stem}"
        c_o3, c_nu, k_bin = work / f"{tag}_c_o3", work / f"{tag}_c_nu", work / f"{tag}_kara"
        try:
            subprocess.run(["clang", "-O3", str(csrc), "-o", str(c_o3), "-lm"], check=True,
                           capture_output=True, timeout=300)
            subprocess.run(["clang", "-O3", "-fno-unroll-loops", str(csrc), "-o", str(c_nu), "-lm"],
                           check=True, capture_output=True, timeout=300)
            subprocess.run(["karac", "build", str(csrc.with_suffix(".kara").parent / ksrc.name)],
                           cwd=work, check=True, capture_output=True, text=True, env=env, timeout=600)
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            skipped.append({"id": kid, "stem": stem, "skip": f"build failed ({type(e).__name__})"})
            continue
        produced = work / ksrc.stem
        if not produced.exists():
            skipped.append({"id": kid, "stem": stem, "skip": "karac emitted no binary"})
            continue
        produced.replace(k_bin)

        ik, sk = pmc_run(pmc, k_bin)
        i3, s3 = pmc_run(pmc, c_o3)
        inu, snu = pmc_run(pmc, c_nu)
        if None in (ik, i3, inu):
            skipped.append({"id": kid, "stem": stem, "skip": "run failed or timed out"})
            continue
        if not (sk == s3 == snu):
            # Never average over a disagreement — a mismatch means the three
            # builds are not doing the same work and the ratio is meaningless.
            skipped.append({"id": kid, "stem": stem, "skip": f"sink mismatch {sk!r}/{s3!r}/{snu!r}"})
            continue

        a, c = simd_ops(c_o3), simd_ops(c_nu)
        rows.append({
            "id": kid, "stem": stem, "dir": str(b.relative_to(ROOT)),
            "kara_instrs": ik, "c_o3_instrs": i3, "c_nounroll_instrs": inu,
            "kara_vs_c_o3": round(ik / i3, 4),
            "kara_vs_c_nounroll": round(ik / inu, 4),
            "c_unroll_effect": round(inu / i3, 4),
            "simd_ops_c_o3": a, "simd_ops_c_nounroll": c,
            "class": "vectorization" if (a is not None and c is not None and a > c) else "pure-unroll",
        })
        print(f"  {kid}:{stem:<24} vs -O3 {ik/i3:5.2f}  vs no-unroll {ik/inu:5.2f}  "
              f"C loses {inu/i3:5.2f}x", flush=True)

    rows.sort(key=lambda r: (int(r["id"]), r["stem"]))
    json.dump({
        "method": ("clang -O3 vs clang -O3 -fno-unroll-loops vs karac build (KARAC_AUTO_PAR=0); "
                   "retired-instruction counts via kara/scripts/pmc.c; one run per binary "
                   "(deterministic); all three builds must agree on the sink"),
        "rows": rows, "skipped": skipped,
    }, open(args.out, "w"), indent=1)
    print(f"\n{len(rows)} program-rows screened, {len(skipped)} skipped -> {args.out}")


if __name__ == "__main__":
    main()
