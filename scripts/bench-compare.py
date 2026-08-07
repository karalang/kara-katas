#!/usr/bin/env python3
"""Regression-check a bench feed against a committed baseline.

Compares two consolidated bench-results.json files (or two per-kata
results.json files) cell-by-cell — matched on
(kata, lang, approach, lane, mode, metric) — and reports every metric that
moved beyond its threshold. Deterministic metrics (binary size, compile
elapsed, compile/runtime peak memory) get a tight threshold; runtime wall-time
is noisy, so it gets a loose one and is reported as INFO unless it blows past a
hard ceiling.

Usage:
    scripts/bench-compare.py --baseline bench-baseline.json [--current bench-results.json]
    scripts/bench-compare.py --baseline a/results.json --current b/results.json

Exit status:
    0  no regressions past threshold (improvements are reported, never fail)
    1  at least one metric regressed past its threshold
    2  usage / file error

Thresholds are relative (fraction). Override per-metric with --threshold
metric=frac (repeatable). A regression is a *worsening*: larger is worse for
every metric here (more bytes, more ms, more RSS).
"""

import argparse
import json
import sys
from datetime import datetime

# Default relative-change thresholds. Deterministic metrics move only on a real
# code change, so even a few percent is signal. Runtime wall-time swings with
# machine load, so its bar is high and informational.
DEFAULT_THRESHOLDS = {
    "binary_bytes": 0.05,
    "compile_elapsed_ms": 0.15,
    "compile_peak_rss_bytes": 0.15,
    "runtime_peak_rss_bytes": 0.15,
    "runtime_mean_ms": 0.30,
}
# Metrics whose regressions fail the run (exit 1). Runtime wall-time is
# advisory only — it reports but never fails, to keep CI stable.
HARD_FAIL = {
    "binary_bytes",
    "compile_elapsed_ms",
    "compile_peak_rss_bytes",
    "runtime_peak_rss_bytes",
}


def load(path):
    with open(path) as fh:
        doc = json.load(fh)
    # Accept either a consolidated feed ({katas:[...]}) or a single per-kata
    # results.json — normalize to a list of per-kata docs.
    if isinstance(doc, dict) and "katas" in doc:
        return doc["katas"]
    return [doc]


def identities(katas):
    """{kata_id: (workload, sink)} — what each kata's numbers were MEASURED ON.

    B-2026-08-05-34. The cell join below matches on (kata, lang, approach,
    lane, mode, metric) and nothing else, so it will happily divide a 500,000
    -iteration run by a 50,000-iteration one and report a 9x "slowdown". That
    is not hypothetical: comparing the committed baseline against the current
    feed, katas 1, 5 and 3629 have all changed BOTH workload and sink, and
    their bogus ratios (16.5x, 9.5x, 8.8x) were the top three entries in a
    corpus median that got read as a compiler regression. Dropping them alone
    moved that median 1.175x -> 1.128x.

    Sink is the stronger signal of the two — it is the program's own output, so
    a changed sink means the two runs did not compute the same thing — but
    workload is checked too, since a run can do more work for the same answer.
    """
    return {
        k.get("kata", {}).get("id", "?"): (
            k.get("kata", {}).get("workload"),
            k.get("kata", {}).get("sink"),
        )
        for k in katas
    }


def provenance(katas):
    """{kata_id: (measured_at, karac_version)} — WHEN each row was measured.

    B-2026-08-05-34, open item (2). Neither feed in this repo is a snapshot.
    bench-baseline.json's 33 rows span 2026-05-31..06-06 and
    bench-results.json's span 2026-06-15..08-05, because both are rolling
    accumulations where each kata carries whenever it was last benched. So the
    window a corpus figure actually measures is per-kata and is never the
    window the reader is told about.

    That is not a cosmetic complaint. The audit of this row rebuilt a "base"
    compiler at ONE commit (218dd7d7, chosen as last-commit-at-or-before the
    file's generated_at) and reported that the baseline's own absolutes did not
    reproduce — #1665 off by 6x. They reproduce fine: #8/#9/#11 were measured
    2026-06-01, whose commit is 5d5ce72f, 227 src/runtime commits earlier, and
    at THAT commit all three land within 5% with byte-identical binary sizes.
    The 6x was two 2026-06-07 commits (the AOT arithmetic-fault traps and the
    lean panic-free sort) landing between the measurement and the chosen base.

    So a base commit must be picked PER KATA from that kata's own measured_at.
    This function surfaces the timestamps that make that possible.

    `karac` is carried alongside because it is the better handle when present:
    the version stamp now renders as `0.1.0-dev.<count>+g<sha>`, which names the
    commit outright. It is absent from older rows (all 33 baseline rows and 227
    of 246 current ones read a bare `karac 0.1.0`), which is exactly why the
    timestamp fallback has to exist.
    """
    return {
        k.get("kata", {}).get("id", "?"): (
            (k.get("env") or {}).get("measured_at"),
            (k.get("env") or {}).get("karac"),
        )
        for k in katas
    }


def span_days(stamps):
    """Calendar span of a set of ISO-8601 timestamps, or None if unusable."""
    ds = sorted(s for s in stamps if s)
    if not ds:
        return None
    try:
        lo = datetime.fromisoformat(ds[0].replace("Z", "+00:00"))
        hi = datetime.fromisoformat(ds[-1].replace("Z", "+00:00"))
    except ValueError:
        return None
    return (ds[0], ds[-1], (hi - lo).total_seconds() / 86400.0)


def cells(katas):
    """Flatten to {(kata_id, lang, approach, lane, mode, metric): value}."""
    out = {}
    for k in katas:
        kid = k.get("kata", {}).get("id", "?")
        for m in k.get("measurements", []):
            base = (kid, m["lang"], m["approach"], m["lane"], m["mode"])
            if m.get("binary_bytes") is not None:
                out[base + ("binary_bytes",)] = m["binary_bytes"]
            if m.get("runtime_peak_rss_bytes") is not None:
                out[base + ("runtime_peak_rss_bytes",)] = m["runtime_peak_rss_bytes"]
            rt = m.get("runtime") or {}
            if rt.get("mean_ms") is not None:
                out[base + ("runtime_mean_ms",)] = rt["mean_ms"]
        for c in k.get("compile", []):
            # compile rows are lane-agnostic; slot them under lane "-"
            base = (kid, c["lang"], c["approach"], "-", c["mode"])
            el = c.get("elapsed") or {}
            if el.get("mean_ms") is not None:
                out[base + ("compile_elapsed_ms",)] = el["mean_ms"]
            if c.get("compile_peak_rss_bytes") is not None:
                out[base + ("compile_peak_rss_bytes",)] = c["compile_peak_rss_bytes"]
    return out


def fmt(metric, v):
    if v is None:
        return "—"
    if metric.endswith("_bytes"):
        return f"{v/1024:.1f} KiB" if v < 1 << 20 else f"{v/(1<<20):.1f} MiB"
    if metric.endswith("_ms"):
        return f"{v:.1f} ms"
    return str(v)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline", required=True)
    ap.add_argument("--current", default="bench-results.json")
    ap.add_argument(
        "--threshold", action="append", default=[],
        help="metric=fraction, e.g. binary_bytes=0.02 (repeatable)",
    )
    ap.add_argument(
        "--all", action="store_true",
        help="also list unchanged/improved cells, not just regressions",
    )
    ap.add_argument(
        "--max-span-days", type=float, default=1.0,
        help="a feed whose rows span more than this is a rolling accumulation, "
             "not a snapshot; reported loudly (default: 1)",
    )
    args = ap.parse_args()

    thresholds = dict(DEFAULT_THRESHOLDS)
    for t in args.threshold:
        try:
            name, frac = t.split("=")
            thresholds[name] = float(frac)
        except ValueError:
            sys.stderr.write(f"bad --threshold {t!r}; want metric=fraction\n")
            return 2

    try:
        base_docs = load(args.baseline)
        cur_docs = load(args.current)
        base = cells(base_docs)
        cur = cells(cur_docs)
        base_ids = identities(base_docs)
        cur_ids = identities(cur_docs)
        base_prov = provenance(base_docs)
        cur_prov = provenance(cur_docs)
    except (OSError, json.JSONDecodeError) as e:
        sys.stderr.write(f"bench-compare: {e}\n")
        return 2

    # Katas whose workload or sink moved are NOT comparable — see identities().
    # Excluded from the ratio arithmetic entirely rather than reported with a
    # caveat, because the failure mode is that a caveat gets aggregated away.
    incomparable = {}
    for kid, cur_id in cur_ids.items():
        base_id = base_ids.get(kid)
        if base_id is not None and base_id != cur_id:
            incomparable[kid] = (base_id, cur_id)

    regressions, improvements, info, missing = [], [], [], []

    for key, cur_v in sorted(cur.items()):
        if key[0] in incomparable:
            continue
        metric = key[-1]
        base_v = base.get(key)
        if base_v is None:
            missing.append((key, cur_v))
            continue
        if base_v == 0:
            continue
        delta = (cur_v - base_v) / base_v
        thr = thresholds.get(metric, 0.10)
        # Every ratio carries the window it was actually measured over. A ratio
        # quoted without its dates is how this row's corpus figure survived two
        # months: the reader assumed one window and the rows carried dozens.
        b_at = (base_prov.get(key[0]) or (None, None))[0]
        c_at = (cur_prov.get(key[0]) or (None, None))[0]
        window = f"  {b_at[:10]}→{c_at[:10]}" if b_at and c_at else ""
        label = "/".join(key[:-1]) + f"  [{metric}]{window}"
        line = (
            f"  {label}\n"
            f"      {fmt(metric, base_v)} → {fmt(metric, cur_v)}  "
            f"({delta*100:+.1f}%)"
        )
        if delta > thr:
            regressions.append((metric, line))
        elif delta < -thr:
            improvements.append(line)
        else:
            info.append(line)

    dropped = [(k, base[k]) for k in base if k not in cur and k[0] not in incomparable]

    print(f"baseline: {args.baseline}")
    print(f"current:  {args.current}\n")

    # Printed before everything else, unconditionally. The workload/sink guard
    # below invalidates SPECIFIC rows; this invalidates the INTERPRETATION of
    # every row at once, because a feed that is not a snapshot cannot answer
    # "what changed between X and Y" no matter how clean each ratio is.
    compared = [k for k in cur_ids if k in base_ids and k not in incomparable]
    for side, prov, path in (
        ("baseline", base_prov, args.baseline),
        ("current ", cur_prov, args.current),
    ):
        sp = span_days([prov.get(k, (None, None))[0] for k in compared])
        if sp is None:
            print(f"⚠  {side}: no measured_at timestamps — provenance unknown, "
                  f"a base commit cannot be picked for these rows")
            continue
        lo, hi, days = sp
        flag = "  ⛔ ROLLING ACCUMULATION, NOT A SNAPSHOT" if days > args.max_span_days else ""
        print(f"   {side}: {lo[:10]} … {hi[:10]}  ({days:.1f}d span){flag}")
    print(f"   {len(compared)} kata(s) compared\n")

    rolling = [
        s for s, p in (("baseline", base_prov), ("current", cur_prov))
        if (sp := span_days([p.get(k, (None, None))[0] for k in compared]))
        and sp[2] > args.max_span_days
    ]
    if rolling:
        print(f"⛔ {' and '.join(rolling)} spans more than {args.max_span_days:g} day(s). "
              f"Each kata's numbers were taken at a DIFFERENT compiler commit, so:\n"
              f"     • no single 'before' or 'after' commit describes this feed;\n"
              f"     • a corpus-wide median over it is a median of different windows;\n"
              f"     • to reproduce a row, rebuild at ITS OWN measured_at (below),\n"
              f"       not at one commit chosen from the file's generated_at.\n"
              f"   Per-kata baseline timestamps:")
        for kid in sorted(compared, key=lambda k: (base_prov.get(k, ("",))[0] or "")):
            at, ver = base_prov.get(kid, (None, None))
            stamp = ver if ver and "+g" in ver else "no sha in version stamp"
            print(f"     kata {kid:<6} {at}  ({stamp})")
        print()

    # Printed early and unconditionally: an excluded kata is the one thing a
    # reader must not miss, and burying it behind --all is how the artifact
    # this guard exists for went unnoticed for two months.
    if incomparable:
        print(f"⛔ NOT COMPARABLE ({len(incomparable)}) — workload or sink "
              f"changed since the baseline; excluded from every ratio below:\n")
        for kid, ((bw, bs), (cw, cs)) in sorted(incomparable.items()):
            print(f"  kata {kid}")
            if bs != cs:
                print(f"      sink     {bs!r} → {cs!r}")
            if bw != cw:
                print(f"      workload {bw!r}\n               → {cw!r}")
        print("  Re-baseline these katas, or compare them against a baseline "
              "taken on the same workload.\n")

    if regressions:
        print(f"🔴 REGRESSIONS ({len(regressions)}) — worsened past threshold:\n")
        for _, line in regressions:
            print(line)
        print()
    if improvements:
        print(f"🟢 improvements ({len(improvements)}):\n")
        for line in improvements:
            print(line)
        print()
    if args.all and info:
        print(f"·  within threshold ({len(info)}):\n")
        for line in info:
            print(line)
        print()
    if missing:
        print(f"⚠  {len(missing)} cell(s) in current with no baseline (new): "
              + ", ".join("/".join(k[:-1]) + f"[{k[-1]}]" for k, _ in missing[:8])
              + (" …" if len(missing) > 8 else ""))
    if dropped:
        print(f"⚠  {len(dropped)} baseline cell(s) absent from current (removed/not re-run)")

    hard = [m for m, _ in regressions if m in HARD_FAIL]
    if hard:
        print(f"\nFAIL: {len(hard)} deterministic-metric regression(s).")
        return 1
    print("\nOK: no deterministic regressions past threshold.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
