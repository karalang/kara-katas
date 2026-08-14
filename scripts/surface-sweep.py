#!/usr/bin/env python3
"""surface-sweep.py — run every .kara in the corpus on all four surfaces and
report where they disagree.

WHY THIS EXISTS. The corpus is 272 katas, and only the most recent 24 carry a
differential harness. The other 248 are single-solver katas written before that
discipline existed: they were verified once, against the compiler of the day,
and never asked again. Meanwhile the compiler has moved — this month alone has
landed fixes to sub-word element stores, narrow-unsigned reads through generics
and arrays, float narrowing, and shadowed builtin variants.

So this sweeps the back catalogue as a REGRESSION CORPUS rather than as a
bug-finding one. It authors nothing and constructs no inputs; it only asks the
question every kata is supposed to answer continuously:

    karac run --interp  ==  karac run  ==  karac build  ==  KARAC_AUTO_PAR=0 build

The INTERPRETER is the oracle, on the evidence of the bug ledger: on essentially
every divergence recorded there the interpreter has been right and a compiled
backend wrong.

WHAT IT DELIBERATELY DOES NOT DO. `bench/` kernels are excluded — they are sized
to run for a second each in COMPILED form, which makes them minutes each under
the tree-walk interpreter, and they are verified by their own bench.sh sink
comparison anyway. Everything else is in scope.

A TIMEOUT IS NOT A DIVERGENCE and is reported separately; so is a program the
interpreter itself cannot run, since without an oracle there is nothing to
compare against.

Usage:
    python3 scripts/surface-sweep.py                  # everything
    python3 scripts/surface-sweep.py --filter 174     # paths matching a substring
    python3 scripts/surface-sweep.py --jobs 4         # parallelism (default: cores)
    python3 scripts/surface-sweep.py --timeout 60     # per-run seconds
    python3 scripts/surface-sweep.py --include-bench  # bench kernels too
"""

import argparse
import concurrent.futures
import os
import subprocess
import sys
import tempfile
from pathlib import Path


def run(cmd, cwd=None, env=None, timeout=60):
    try:
        p = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        return 124, b"", b"timeout"


def show(b, n=2):
    txt = b.decode("utf-8", "backslashreplace").strip()
    return " / ".join(txt.splitlines()[:n])


def check(path, repo, timeout):
    """Returns (kind, path, detail). kind in
    ok | divergence | timeout | interp_error | build_error.

    Every invocation runs in its OWN temporary directory with an absolute source
    path. Two programs in the same kata directory — `iterative.kara` and
    `recursive.kara`, say — otherwise race on whatever `karac build` writes
    beside the source, and the loser reports a build failure that has nothing to
    do with the compiler. That happened on the first run of this sweep, and it is
    exactly the kind of self-inflicted finding a parallel harness invents."""
    rel = str(path.relative_to(repo))
    src = str(path.resolve())
    with tempfile.TemporaryDirectory(prefix="ssweep-") as td:
        return _check_in(src, rel, Path(td), timeout)


def _check_in(src, rel, cwd, timeout):
    rc, so, se = run(["karac", "run", "--interp", src], cwd=cwd, timeout=timeout)
    if rc == 124:
        return ("timeout", rel, "interp timed out — no oracle, nothing compared")
    if rc != 0:
        return ("interp_error", rel, show(se or so))
    oracle = so

    results = {}
    rc, so, se = run(["karac", "run", src], cwd=cwd, timeout=timeout)
    if rc == 124:
        results["jit"] = ("timeout", b"")
    elif rc != 0:
        results["jit"] = ("error", se or so)
    else:
        results["jit"] = ("ok", so)

    for label, extra in (("build", {}), ("build_seq", {"KARAC_AUTO_PAR": "0"})):
        env = dict(os.environ, **extra)
        binp = cwd / f"out_{label}"
        rc, so, se = run(["karac", "build", src, "-o", str(binp)],
                         cwd=cwd, env=env, timeout=max(timeout, 180))
        if rc != 0 or not binp.exists():
            results[label] = ("build_error", se or so)
            continue
        rc, so, se = run([str(binp)], cwd=cwd, timeout=timeout)
        if rc == 124:
            results[label] = ("timeout", b"")
        elif rc != 0:
            results[label] = ("error", se or so)
        else:
            results[label] = ("ok", so)

    bad = []
    for surf, (state, out) in results.items():
        if state == "ok":
            if out != oracle:
                bad.append(f"{surf}: output differs\n"
                           f"        interp: {show(oracle)}\n"
                           f"        {surf}: {show(out)}")
        elif state == "timeout":
            bad.append(f"{surf}: timed out (interpreter did not)")
        else:
            bad.append(f"{surf}: {state} — {show(out)}")
    if bad:
        kind = "build_error" if all("build_error" in b or "error" in b for b in bad) else "divergence"
        if any("output differs" in b for b in bad):
            kind = "divergence"
        return (kind, rel, "\n      ".join(bad))
    return ("ok", rel, "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--filter", default="")
    ap.add_argument("--jobs", type=int, default=os.cpu_count() or 4)
    ap.add_argument("--timeout", type=int, default=60)
    ap.add_argument("--include-bench", action="store_true")
    args = ap.parse_args()

    repo = Path(__file__).resolve().parent.parent
    def in_package(p):
        """True if p belongs to a multi-file package (a kara.toml above it).
        `karac build <one module>` refuses those by design — with a very clear
        diagnostic — so sweeping them one file at a time reports a harness
        artifact, not a compiler failure. The package as a whole is covered by
        its own `karac build` in the kata's Running section."""
        for parent in p.parents:
            if (parent / "kara.toml").exists():
                return True
            if parent == repo:
                break
        return False

    def has_main(p):
        """A file with no `fn main` is a library target — apps/prism and
        apps/veil are WASM modules built by their own build.sh — and asking
        `karac build` for an executable reports a missing `main` that is the
        harness's mistake, not the compiler's."""
        try:
            return "fn main" in p.read_text(errors="replace")
        except OSError:
            return False

    files = sorted(p for p in repo.rglob("*.kara")
                   if (args.include_bench or "/bench/" not in str(p))
                   and not in_package(p)
                   and has_main(p)
                   and (not args.filter or args.filter in str(p)))
    print(f"sweeping {len(files)} programs on {args.jobs} jobs "
          f"(timeout {args.timeout}s/run)\n", file=sys.stderr)

    buckets = {"ok": [], "divergence": [], "timeout": [], "interp_error": [],
               "build_error": []}
    done = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as ex:
        futs = {ex.submit(check, p, repo, args.timeout): p for p in files}
        for fut in concurrent.futures.as_completed(futs):
            kind, rel, detail = fut.result()
            buckets[kind].append((rel, detail))
            done += 1
            if kind != "ok":
                print(f"  [{done}/{len(files)}] {kind.upper():13s} {rel}", file=sys.stderr)
            elif done % 25 == 0:
                print(f"  [{done}/{len(files)}]", file=sys.stderr)

    print(f"\n{len(files)} programs · {len(buckets['ok'])} clean · "
          f"{len(buckets['divergence'])} DIVERGENCES · "
          f"{len(buckets['build_error'])} build errors · "
          f"{len(buckets['timeout'])} timeouts · "
          f"{len(buckets['interp_error'])} interpreter errors")

    for kind, title in (
        ("divergence", "DIVERGENCES — a compiled surface disagrees with the interpreter"),
        ("build_error", "BUILD / RUN ERRORS — the interpreter ran it and a backend did not"),
        ("interp_error", "INTERPRETER ERRORS — no oracle, nothing compared"),
        ("timeout", "TIMEOUTS — not a divergence, just too slow for this budget"),
    ):
        if buckets[kind]:
            print(f"\n{title}:")
            for rel, detail in sorted(buckets[kind]):
                print(f"  {rel}")
                if detail:
                    print(f"      {detail}")
    return 1 if buckets["divergence"] or buckets["build_error"] else 0


if __name__ == "__main__":
    sys.exit(main())
