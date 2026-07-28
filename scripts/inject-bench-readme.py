#!/usr/bin/env python3
"""Inject a "## Benchmarks" section into a kata README from its bench results.

Usage: inject-bench-readme.py <kata-dir> [<kata-dir> ...]

Reads <kata-dir>/bench/results.json — the canonical M5 host feed. (The older
results.container-x86.json is a corroborating second host, not the source of
published claims; see BENCHMARKS.md § Hosts.) Builds a runtime table per
sequential approach, sorted fastest-first with a vs-Kāra column, and inserts a
"## Benchmarks" section just before "## Running" (or "## Notes", or at EOF).
Idempotent: an existing "## Benchmarks" section is replaced.

Three things this script is deliberately careful about, each a bug that shipped
once already:

1. **Two ovf encodings.** The equal-safety Rust twin is `lang="rust_ovf"` in the
   current harness but `lang="rust", approach="<stem>_ovf"` in 43 older katas.
   Reading the raw lang would label a checked-Rust number as plain `rustc -O`.
   Both encodings are normalised to `rust_ovf` here.

2. **Multi-approach katas.** 74 katas carry more than one sequential approach
   (e.g. brute_force and hash_map). De-duplicating by lang alone silently
   compares Kāra's brute_force against Rust's hash_map. Rows are grouped by
   approach and each gets its own table.

3. **Missing equal-safety lane.** 73 katas have no overflow-checks twin at all.
   Those tables say so in the caveat line rather than presenting wrapping
   `rustc -O` as if it were the honest baseline.
"""
import json
import sys
import os
import re

LANG_LABEL = {
    "c": "C `clang -O3`",
    "c_v3": "C `clang -O3 -march=x86-64-v3` (matched ISA)",
    "rust": "Rust `-O`",
    "rust_ovf": "Rust `-O -C overflow-checks=on` (equal-safety)",
    "rust_v3": "Rust `-O -C overflow-checks=on -C target-cpu=x86-64-v3` (matched safety + ISA)",
    "kara": "**Kāra (codegen)**",
    "go": "Go",
    "python": "Python (scale lane)",
}

# Fastest-first is the row order, but ties and near-ties read better with a
# stable secondary order, so keep a canonical lang ranking for tie-breaks.
LANG_ORDER = ["kara", "c", "c_v3", "rust", "rust_ovf", "rust_v3", "go", "python"]


def fmt_ms(ms):
    if ms >= 1000:
        return f"{ms / 1000:.2f} s"
    return f"{ms:.1f} ms"


# The equal-safety Rust twin has been encoded FOUR different ways as the harness
# evolved. Reading the raw lang labels a checked-Rust number as plain `rustc -O`,
# which is the misattribution this whole lane exists to prevent. Enumerated from
# the bench.sh files rather than guessed — each of the first three counts was an
# undercount that had to be corrected after the fact:
#   lang="rust_ovf"                                — current harness, 128
#   lang="rust", approach="<stem>_ovf"             —  43
#   lang="rust", approach="<stem>_rschk"           —  22 (build_rust_checked)
#   lang="rust", approach="<stem>_overflow_checks" —   2 (#69, #70)
# Before adding a fifth spelling, prefer `ovf_rt_cmds` in scripts/bench-lib.sh,
# which registers under lang="rust_ovf" and needs no suffix at all.
OVF_SUFFIXES = ("_ovf", "_rschk", "_overflow_checks", "_chk")


def normalise(m):
    """Return (lang, approach) with every ovf encoding folded into rust_ovf."""
    lang, app = m["lang"], m["approach"]
    if lang == "rust":
        for suf in OVF_SUFFIXES:
            if app.endswith(suf):
                return "rust_ovf", app[: -len(suf)]
    return lang, app


def collect(res):
    """-> {approach: {lang: mean_ms}} over the sequential lane."""
    by_app = {}
    for m in res.get("measurements", []):
        rt = m.get("runtime")
        if not rt or m.get("lane") not in (None, "seq"):
            continue
        lang, app = normalise(m)
        # first writer wins: a lang should not appear twice per approach, but if
        # it does, the earlier record is the one the other lanes were joined on.
        by_app.setdefault(app, {}).setdefault(lang, rt["mean_ms"])
    return by_app


def table(langs):
    kara = langs.get("kara")
    rows = sorted(
        langs.items(),
        key=lambda kv: (kv[1], LANG_ORDER.index(kv[0]) if kv[0] in LANG_ORDER else 99),
    )
    out = ["| Impl | Mean | vs Kāra |", "|---|---|---|"]
    for lang, mean in rows:
        label = LANG_LABEL.get(lang, lang)
        ratio = f"{mean / kara:.2f}×" if kara else "—"
        out.append(f"| {label} | {fmt_ms(mean)} | {ratio} |")
    return out


def build_section(res):
    kata = res.get("kata", {})
    env = res.get("env", {})
    workload = kata.get("workload", "")
    sink = kata.get("sink", "")
    by_app = {a: l for a, l in collect(res).items() if "kara" in l}
    if not by_app:
        return None

    host = env.get("host", "unknown host")
    cores = env.get("cores")
    when = (env.get("measured_at") or "")[:10]
    # env.karac is "karac 0.1.0" on every build ever made — printing it implies a
    # precision it does not have. Only env.karac_build (content hash + mtime,
    # added 2026-07-28) actually identifies the toolchain.
    karac = env.get("karac_build", "")
    if karac:
        karac = "karac " + karac.split()[0]

    lines = ["## Benchmarks", ""]
    lines.append(
        "The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) "
        "carries a scaled cross-language variant — the same algorithm and a "
        "shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing "
        f"on the sink (`{sink}`). Workload: {workload}."
    )
    lines.append("")

    host_str = f"{host} ({cores})" if cores else host
    lines.append(
        f"Runtime, sequential lane on {host_str}"
        + (f", {when}" if when else "")
        + " (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):"
    )
    lines.append("")

    multi = len(by_app) > 1
    for app in sorted(by_app):
        if multi:
            lines.append(f"**`{app}`**")
            lines.append("")
        lines.extend(table(by_app[app]))
        lines.append("")

    # Honesty: only claim an equal-safety comparison when the lane is present.
    has_ovf = all("rust_ovf" in l for l in by_app.values())
    some_ovf = any("rust_ovf" in l for l in by_app.values())
    if has_ovf:
        caveat = (
            "Kāra checks integer overflow by default, so the honest Rust baseline "
            "is the `-C overflow-checks=on` row, not `rustc -O`."
        )
    elif some_ovf:
        caveat = (
            "Kāra checks integer overflow by default, so the honest Rust baseline "
            "is `-C overflow-checks=on`. **Not every approach above carries that "
            "twin yet** — where it is absent the only Rust row is wrapping "
            "`rustc -O`, which is not an equal-safety comparison."
        )
    else:
        caveat = (
            "**This kata has no equal-safety Rust twin yet.** Kāra checks integer "
            "overflow by default while `rustc -O` silently wraps, so the Rust row "
            "above is *not* an equal-safety comparison and flatters Rust by "
            "whatever the check costs on this workload."
        )
    lines.append(
        caveat
        + " Single-machine snapshot (`bench/results.json`"
        + (f", {karac}" if karac else "")
        + "); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology and "
        "caveats. Re-run with `bash bench/bench.sh` (add "
        "`KARA_BENCH_INCLUDE_PY=1` for the Python lane)."
    )
    lines.append("")
    return "\n".join(lines)


# Opening sentence of every generated section. Together with "carries no ###
# subheading" this is what distinguishes a section this script owns from a
# hand-written analysis that merely shares the heading.
GEN_SIG = "The kata's tiny fixed inputs aren't a workload"

SECTION_RE = re.compile(r"\n## Benchmarks\n(.*?)(?=\n## |\Z)", re.DOTALL)


def is_generated(body):
    return GEN_SIG in body and "\n### " not in body


def inject(readme_path, section):
    """Replace the generated Benchmarks section, or report why it was skipped.

    Returns one of: "replaced", "inserted", "skipped-handwritten".

    This function refuses to touch hand-written analysis. 66 katas keep their
    benchmark numbers in prose with ### subsections under the same "##
    Benchmarks" heading; an earlier version of this script matched on the
    heading alone, and because `\\n## ` does not match `\\n### `, the strip ran
    to EOF and deleted the whole analysis (138 lines on #1). Numbers that live
    in prose have to be edited by a human — silently overwriting them with a
    generated table is the same class of mistake as blind-sed'ing a results
    value on a non-unique anchor.
    """
    with open(readme_path) as f:
        text = f.read()

    target = None
    for m in SECTION_RE.finditer(text):
        if is_generated(m.group(1)):
            target = m
            break

    if target is not None:
        # Replace with "" not "\n": the match begins at the newline separating
        # the previous section, and the prefix already retains it. Substituting
        # "\n" re-adds it, so every re-injection grew the file by a blank line.
        text = text[: target.start()] + text[target.end() :]
        outcome = "replaced"
    elif SECTION_RE.search(text):
        return "skipped-handwritten"
    else:
        outcome = "inserted"

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
    return outcome


def main():
    for kata_dir in sys.argv[1:]:
        rj = os.path.join(kata_dir, "bench", "results.json")
        readme = os.path.join(kata_dir, "README.md")
        if not os.path.exists(rj):
            print(f"SKIP {kata_dir}: no bench/results.json")
            continue
        if not os.path.exists(readme):
            print(f"SKIP {kata_dir}: no README")
            continue
        with open(rj) as f:
            res = json.load(f)
        section = build_section(res)
        if section is None:
            print(f"SKIP {kata_dir}: no kara row in the sequential lane")
            continue
        outcome = inject(readme, section)
        if outcome == "skipped-handwritten":
            print(
                f"SKIP {readme}: Benchmarks section is hand-written "
                "(prose/### subsections) — update it by hand"
            )
        else:
            print(f"{outcome} {readme}")


if __name__ == "__main__":
    main()
