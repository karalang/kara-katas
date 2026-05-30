#!/usr/bin/env python3
"""Assemble a per-kata bench/results.json from the accumulator a bench.sh built
via scripts/bench-lib.sh.

Reads a single accumulator directory (passed as argv[1]) containing:

  meta.json      kata + env metadata (written by bench_begin)
  runtime.json   hyperfine --export-json for the runtime lane(s)   (optional)
  rt_map.tsv     name<TAB>lang<TAB>approach<TAB>lane<TAB>mode       (optional)
  compile.json   hyperfine --export-json for compile-elapsed       (optional)
  ce_map.tsv     name<TAB>lang<TAB>approach<TAB>mode                (optional)
  size.tsv       lang<TAB>approach<TAB>lane<TAB>mode<TAB>bytes      (optional)
  mem.tsv        lang<TAB>approach<TAB>lane<TAB>mode<TAB>metric<TAB>bytes
  cmem.tsv       lang<TAB>approach<TAB>mode<TAB>metric<TAB>bytes

The hyperfine `command` string is the join key back to the rt_map/ce_map
structure — the bench library writes both from the same rt_cmd/ce_cmd call, so
they never drift. Output is written to argv[2] (the kata's bench/results.json).

This script is intentionally dependency-free (stdlib only) so it runs anywhere a
bench.sh runs.
"""

import json
import os
import sys

SCHEMA_VERSION = 1


def read_json(path):
    if not os.path.exists(path):
        return None
    with open(path) as fh:
        return json.load(fh)


def read_tsv(path, ncols):
    """Yield tuples of exactly `ncols` fields; skip blank lines."""
    if not os.path.exists(path):
        return
    with open(path) as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line.strip():
                continue
            parts = line.split("\t")
            if len(parts) != ncols:
                sys.stderr.write(
                    f"bench-emit: malformed row in {os.path.basename(path)} "
                    f"(expected {ncols} cols, got {len(parts)}): {line!r}\n"
                )
                continue
            yield parts


def ms(seconds):
    return None if seconds is None else round(seconds * 1000.0, 4)


def runtime_block(result):
    """Map one hyperfine result object to a runtime sub-record (ms units)."""
    mean = result.get("mean")
    user = result.get("user")
    system = result.get("system")
    cpu_pct = None
    if mean and mean > 0 and user is not None and system is not None:
        cpu_pct = round((user + system) / mean * 100.0, 1)
    return {
        "mean_ms": ms(mean),
        "stddev_ms": ms(result.get("stddev")),
        "median_ms": ms(result.get("median")),
        "min_ms": ms(result.get("min")),
        "max_ms": ms(result.get("max")),
        "user_ms": ms(user),
        "system_ms": ms(system),
        "cpu_pct": cpu_pct,
        "runs": len(result.get("times", []) or []),
    }


def main():
    if len(sys.argv) != 3:
        sys.stderr.write("usage: bench-emit.py <accumulator-dir> <out.json>\n")
        return 2
    acc, out_path = sys.argv[1], sys.argv[2]

    meta = read_json(os.path.join(acc, "meta.json")) or {}

    # --- runtime lane: join hyperfine export to declared structure ---
    rt_export = read_json(os.path.join(acc, "runtime.json"))
    rt_by_command = {}
    if rt_export:
        for r in rt_export.get("results", []):
            rt_by_command[r.get("command")] = r

    # measurements keyed by (lang, approach, lane, mode)
    measurements = {}

    def m_slot(lang, approach, lane, mode):
        key = (lang, approach, lane, mode)
        if key not in measurements:
            measurements[key] = {
                "lang": lang,
                "approach": approach,
                "lane": lane,
                "mode": mode,
                "runtime": None,
                "binary_bytes": None,
                "runtime_peak_rss_bytes": None,
            }
        return measurements[key]

    unmatched = []
    for name, lang, approach, lane, mode in read_tsv(
        os.path.join(acc, "rt_map.tsv"), 5
    ):
        slot = m_slot(lang, approach, lane, mode)
        result = rt_by_command.get(name)
        if result is None:
            unmatched.append(name)
            continue
        slot["runtime"] = runtime_block(result)
    for name in unmatched:
        sys.stderr.write(
            f"bench-emit: rt_map command not found in hyperfine export: {name!r}\n"
        )

    for lang, approach, lane, mode, b in read_tsv(os.path.join(acc, "size.tsv"), 5):
        m_slot(lang, approach, lane, mode)["binary_bytes"] = int(b)

    for lang, approach, lane, mode, metric, b in read_tsv(
        os.path.join(acc, "mem.tsv"), 6
    ):
        # metric is fixed (runtime_peak_rss) but carried explicitly for clarity
        m_slot(lang, approach, lane, mode)["runtime_peak_rss_bytes"] = int(b)

    # --- compile lane: elapsed + peak rss, keyed by (lang, approach, mode) ---
    ce_export = read_json(os.path.join(acc, "compile.json"))
    ce_by_command = {}
    if ce_export:
        for r in ce_export.get("results", []):
            ce_by_command[r.get("command")] = r

    compile_recs = {}

    def c_slot(lang, approach, mode):
        key = (lang, approach, mode)
        if key not in compile_recs:
            compile_recs[key] = {
                "lang": lang,
                "approach": approach,
                "mode": mode,
                "elapsed": None,
                "compile_peak_rss_bytes": None,
            }
        return compile_recs[key]

    ce_unmatched = []
    for name, lang, approach, mode in read_tsv(os.path.join(acc, "ce_map.tsv"), 4):
        slot = c_slot(lang, approach, mode)
        result = ce_by_command.get(name)
        if result is None:
            ce_unmatched.append(name)
            continue
        slot["elapsed"] = runtime_block(result)
    for name in ce_unmatched:
        sys.stderr.write(
            f"bench-emit: ce_map command not found in hyperfine export: {name!r}\n"
        )

    for lang, approach, mode, metric, b in read_tsv(os.path.join(acc, "cmem.tsv"), 5):
        c_slot(lang, approach, mode)["compile_peak_rss_bytes"] = int(b)

    def sort_key_m(rec):
        return (rec["approach"], rec["lane"], rec["lang"], rec["mode"])

    def sort_key_c(rec):
        return (rec["approach"], rec["lang"], rec["mode"])

    doc = {
        "schema_version": SCHEMA_VERSION,
        "kata": meta.get("kata", {}),
        "env": meta.get("env", {}),
        "measurements": sorted(measurements.values(), key=sort_key_m),
        "compile": sorted(compile_recs.values(), key=sort_key_c),
    }

    with open(out_path, "w") as fh:
        json.dump(doc, fh, indent=2)
        fh.write("\n")
    sys.stderr.write(
        f"bench-emit: wrote {out_path} "
        f"({len(doc['measurements'])} measurements, {len(doc['compile'])} compile rows)\n"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
