#!/usr/bin/env python3
"""Inject a "## Benchmarks" section into a kata README from its bench results.

Usage: inject-bench-readme.py <kata-dir> [<kata-dir> ...]

Reads <kata-dir>/bench/results.container-x86.json, builds a runtime table
(sequential lanes, sorted fastest-first, with a vs-Kāra column), and inserts a
"## Benchmarks" section just before "## Running" (or "## Notes", or at EOF).
Idempotent: if a "## Benchmarks" section already exists it is replaced.
"""
import json
import sys
import os
import re

LANG_LABEL = {
    "c": "C `clang -O3`",
    "rust": "Rust `-O`",
    "rust_ovf": "Rust `-O -C overflow-checks=on` (equal-safety)",
    "kara": "**Kāra (codegen)**",
    "go": "Go",
    "python": "Python (scale lane)",
}


def fmt_ms(ms):
    if ms >= 1000:
        return f"{ms/1000:.2f} s"
    return f"{ms:.1f} ms"


def build_section(res):
    kata = res["kata"]
    workload = kata.get("workload", "")
    sink = kata.get("sink", "")
    rows = []
    kara_mean = None
    for m in res["measurements"]:
        rt = m.get("runtime")
        if not rt or m.get("lane") not in (None, "seq"):
            continue
        rows.append((m["lang"], rt["mean_ms"]))
        if m["lang"] == "kara":
            kara_mean = rt["mean_ms"]
    # de-dup langs keeping first, sort by mean
    seen = {}
    for lang, mean in rows:
        if lang not in seen:
            seen[lang] = mean
    ordered = sorted(seen.items(), key=lambda kv: kv[1])

    lines = []
    lines.append("## Benchmarks")
    lines.append("")
    lines.append(
        "The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) "
        "carries a scaled cross-language variant — the same algorithm and a "
        "shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing "
        f"on the sink (`{sink}`). Workload: {workload}."
    )
    lines.append("")
    lines.append(
        "Runtime, sequential, one x86 container run (hyperfine, 30 runs; "
        "`KARAC_AUTO_PAR=0`):"
    )
    lines.append("")
    lines.append("| Impl | Mean | vs Kāra |")
    lines.append("|---|---|---|")
    for lang, mean in ordered:
        label = LANG_LABEL.get(lang, lang)
        ratio = f"{mean/kara_mean:.2f}×" if kara_mean else "—"
        lines.append(f"| {label} | {fmt_ms(mean)} | {ratio} |")
    lines.append("")
    lines.append(
        "Kāra checks integer overflow by default, so the honest baseline is "
        "`rustc -O -C overflow-checks=on`. Single-machine snapshot "
        "(`bench/results.container-x86.json`); see "
        "[`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with "
        "`bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane)."
    )
    lines.append("")
    return "\n".join(lines)


def inject(readme_path, section):
    with open(readme_path) as f:
        text = f.read()
    # strip an existing Benchmarks section (## Benchmarks .. next ## )
    text = re.sub(r"\n## Benchmarks\n.*?(?=\n## )", "\n", text, flags=re.DOTALL)
    anchor = None
    for a in ("## Running", "## Notes"):
        if a in text:
            anchor = a
            break
    block = section + "\n"
    if anchor:
        text = text.replace(anchor, block + anchor, 1)
    else:
        text = text.rstrip() + "\n\n" + block
    with open(readme_path, "w") as f:
        f.write(text)


def main():
    for kata_dir in sys.argv[1:]:
        rj = os.path.join(kata_dir, "bench", "results.container-x86.json")
        readme = os.path.join(kata_dir, "README.md")
        if not os.path.exists(rj):
            print(f"SKIP {kata_dir}: no results json")
            continue
        if not os.path.exists(readme):
            print(f"SKIP {kata_dir}: no README")
            continue
        with open(rj) as f:
            res = json.load(f)
        inject(readme, build_section(res))
        print(f"injected {readme}")


if __name__ == "__main__":
    main()
