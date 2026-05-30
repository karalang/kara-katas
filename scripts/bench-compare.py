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
        base = cells(load(args.baseline))
        cur = cells(load(args.current))
    except (OSError, json.JSONDecodeError) as e:
        sys.stderr.write(f"bench-compare: {e}\n")
        return 2

    regressions, improvements, info, missing = [], [], [], []

    for key, cur_v in sorted(cur.items()):
        metric = key[-1]
        base_v = base.get(key)
        if base_v is None:
            missing.append((key, cur_v))
            continue
        if base_v == 0:
            continue
        delta = (cur_v - base_v) / base_v
        thr = thresholds.get(metric, 0.10)
        label = "/".join(key[:-1]) + f"  [{metric}]"
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

    dropped = [(k, base[k]) for k in base if k not in cur]

    print(f"baseline: {args.baseline}")
    print(f"current:  {args.current}\n")

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
