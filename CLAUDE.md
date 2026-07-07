# CLAUDE.md — kara-katas

Guidance for Claude Code (and human contributors) working in this repo.

## What this repo is

Classic algorithm problems (LeetCode-style) plus a few bespoke/backend programs,
implemented in **[Kāra](https://github.com/karalang/kara)** and mirrored,
algorithm-for-algorithm, in **C, Rust, Go, and Python**. It does double duty:

1. **Compiler dogfood** — real, varied Kāra code that exercises the compiler and
   surfaces bugs (small programs surface a disproportionate share of compiler
   defects).
2. **Benchmark corpus** — Kāra's compiled output vs mainstream languages on
   identical workloads (`karac build` / `rustc -O` / `clang -O3` / `go build`).

This is a **content repo, not the compiler**. Direct commits to `main` are fine
here (no worktree dance). The compiler lives in the sibling `kara/` repo — any
compiler fix and any bug-ledger entry (`docs/bug-ledger.jsonl`) goes **there**.

## Layout

```
leetcode/<range>/<n-name>/   one kata: README.md (spec) + <name>.kara (+ variants)
                            + <name>.c/.rs/.py + go-seq/ + bench/ (bench.sh, results.json)
bespoke/  backend/           non-leetcode katas and small services
oracle/                     focused compiler-behavior demonstrations
scripts/                    bench-all.sh, bench-graph.py, consolidate-bench.sh, …
graphs/  bench-results.json  consolidated benchmark feed + rendered charts
BENCHMARKS.md               methodology + caveats
```

## Commands

```bash
karac run  path/to/kata.kara         # interpret (fast iteration)
karac build path/to/kata.kara        # native binary (writes to CWD)
brew install hyperfine               # benching; also needs karac, rustc, clang, go
bash scripts/bench-all.sh            # run the cross-language benchmark suite
python3 scripts/bench-graph.py       # redraw graphs/*.svg from bench-results.json
```

## Developing Kāra katas — through the Mend loop

New Kāra here is authored and verified **through the Mend loop**, not hand-fixed:
run `karac check --output=json`, apply `karac fix` for machine-applicable
diagnostics as the primary fix path, feed the rest back, then verify the result
against an **oracle**. "It compiles" is not the bar.

Katas already *are* the canonical Mend task+oracle shape:

- `README.md` = the spec (the "write X" prompt).
- The **C/Rust/Go/Python mirror** (or a known expected output) = the oracle —
  the Kāra output must match it exactly.

The full task+oracle format (oracle types, granularity rule, scored outcomes,
and the practice-vs-measurement rule) is defined authoritatively in the sibling
kara repo at `examples/mend/TASK_FORMAT.md`.

## Verification rules (non-negotiable)

- **A/B run == build.** Every kata must produce **identical output under
  `karac run` and `karac build`.** A run/build divergence is a compiler bug, not
  a kata quirk.
- **Auto-par is a third surface.** Verify under the **default** build (which
  auto-parallelizes) *and* `KARAC_AUTO_PAR=0` — effect-analysis bugs diverge only
  under auto-par. So the full A/B set is: `run` vs `build` vs default-auto-par
  `build`, all byte-identical to the reference-language output.
- **Cross-language parity.** The C/Rust/Go/Python mirrors must implement the
  **same algorithm** as the Kāra version (honest benchmarking) and produce the
  same output.

## Katas are bug-finders — never route around

The point of a kata is to find compiler gaps by writing **natural** Kāra. When a
kata hits a `karac` limitation:

- **Fix the compiler** (in the `kara/` repo) or open a `docs/bug-ledger.jsonl`
  entry there. **Never** work around the gap in the kata — no contorted phrasing
  to dodge a codegen bug, no `KARAC_AUTO_PAR=0`-only "pass," no deleting the
  natural approach.
- Probe **every** canonical way to write the problem; each is a distinct
  bug-finding surface.
- Keep the kata idiomatic. A kata that's been twisted to avoid a bug has stopped
  doing its job.

## Benchmark-design pitfalls

- A **vectorizable refill loop** or a **csel-on-converging-pointer** distorts
  sequential benches — the optimizer erases the work you meant to measure.
  Prefer **build-once + punch** workloads.
- Frame comparisons as an **equal-safety tie** (Kāra checks integer overflow by
  default; `rustc -O` silently wraps — compare against
  `rustc -O -C overflow-checks=on` where it matters). See BENCHMARKS.md.
- Don't blind-`sed`/replace an expected-output or `results.json` value on a
  non-unique anchor — it silently corrupts sibling entries. Edit the specific
  record.

## Honesty rule

The Mend machine-fix **rate** is a statistic only over **fresh, blind** LLM
authorship (`kara/examples/mend/harness/mend_batch.py`, live) — a model that
never saw the diagnostics. Authoring by anyone who already knows the language is
biased and counts as dogfooding + gap-finding, **never** as the rate. Do not
quote a machine-fix rate from non-blind authoring. Benchmark numbers are only
honest with the caveats in BENCHMARKS.md attached.
