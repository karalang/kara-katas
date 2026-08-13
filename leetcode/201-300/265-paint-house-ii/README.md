# 265. Paint House II

`n` houses in a row, `k` colours, `costs[i][c]` to paint house `i` colour `c`.
No two adjacent houses may share a colour. Minimise the total.

```
[[1,5,3],[2,9,4]]  k=3  ->  5     (1 + 4, or 3 + 2)
[[7,6,2]]          k=3  ->  2
[]                 k=3  ->  0
[[4],[9]]          k=1  ->  -1    no painting exists
```

**Constraints:** `1 ≤ n ≤ 100`; `1 ≤ k ≤ 20`; `1 ≤ costs[i][j] ≤ 20`.
**Follow-up:** solve it in `O(n·k)`.

## Approaches

| file | mechanism | cost |
|---|---|---|
| `paint_house_ii.kara` ★ | row minimum, its index, and the second minimum | O(n·k) |
| `paint_house_ii_quad.kara` | scan the previous row per colour — the definition | O(n·k²) |
| `paint_house_ii_prefix.kara` | prefix and suffix minima, colour excised between them | O(n·k) |
| `differential.kara` | 4,000 randomized cost tables, all three agree | — |

## The mechanism

This is [#256](../256-paint-house/) with `k` colours instead of three, and the
recurrence is unchanged: the constraint reaches back exactly one house, so the
cheapest way to reach house `i` in colour `c` is `costs[i][c]` plus the cheapest
way to reach `i-1` in *any other* colour.

Written directly that is a scan over `k-1` entries, done `k` times per house —
O(n·k²). But those `k` scans all interrogate the same row, and their answer only
ever takes one of two values:

- **the row minimum**, for every colour that is not where the minimum sits;
- **the row's second minimum**, for the one colour that is.

So a single pass for `(min, its index, second-min)` replaces all of them, and the
follow-up's O(n·k) falls out.

## The tie

**The second minimum is with multiplicity** — not "the smallest value strictly
greater than the minimum".

Given a previous row of `[3, 3, 5]`, the second minimum is `3`, not `5`. Colour 0
is barred from index 0, but index 1 also holds `3`, so it can still reach `3`.
Reading it the other way charges colour 0 five instead of three.

The bug is wrong **only when the row minimum is tied** — and that is what makes
it dangerous rather than obvious. Costs drawn from a wide range essentially never
tie, so it is not merely rare under naive random testing, it is effectively
absent. Quantified below.

## Why three, and why the third asks a different question

The O(n·k²) file makes no claim about *where* the best previous colour is; it
scans for it. That is why it is the reference: there is no argument in it to get
wrong.

Both O(n·k) files replace that scan with an argument, and the two arguments share
nothing:

- The ★ form reasons about **rank** — which entry is smallest, and what happens
  when you are barred from it. Its correctness turns entirely on the tie rule.
- The prefix/suffix form reasons about **position**. "Cheapest entry other than
  `c`" is a range-minimum query over everything left of `c` and everything right
  of it, so precompute `pre[j] = min(prev[0..j])` and `suf[j] = min(prev[j..k-1])`
  once per row and read `min(pre[c-1], suf[c+1])`.

The second one never asks the tie question at all — `[3, 3, 5]` simply has
`pre[1] = 3`, and colour 0 reads it directly. There are no special cases, which
is the point of having it. Its exposed edge is the other one: `c = 0` has no left
part and `c = k-1` has no right part, and an off-by-one that lets `c` into its own
query silently permits "paint it the same colour as before".

## Impossibility

`k = 1` with `n ≥ 2` admits no painting at all, and the constraints do not say
what to return. Rather than let that case produce a plausible finite number, `INF`
propagates through the recurrence and all three files report **-1** — a value the
differential can check them against, instead of three implementations quietly
inventing three different totals.

## Generator design

The generator turns on one observation: **the separating case is a tie.**

Most cases therefore draw costs from a deliberately **narrow** range — usually
`1..3` across up to 6 colours, where a tied row minimum is the common case rather
than the exception. Wide-range cases are still drawn, as the minority. Two
structural families round it out: `k = 1, n ≥ 2` (impossible), and `k = 2`, where
"any colour but this one" degenerates to a single choice and the min/second-min
bookkeeping has no slack.

Over 4,000 cases: **23,974 rows generated, 7,679 of them with a tied minimum**
(32%) and **838 impossible cases**. The separating condition is a measured count,
not a hope.

**Three failure modes tested, not assumed:**

| injected bug | mismatches / 4,000 |
|---|---|
| second minimum as "strictly greater than the minimum" | **560** |
| ★ form drops the `t == idx1` exclusion | **2,071** |
| prefix/suffix ranges include `c` itself | **2,071** |

The last two are equal because they are the same mistake: both let colour `c`
read its own previous entry, so both compute the minimum over the *whole* row.
Different files, different-looking slips, one wrong answer set.

### What the narrow range buys

The tie bug was also run against a control generator with the range widened to
`1..1000` everywhere — same seeds, same families, same 4,000 cases, only the
value span changed:

| generator | mismatches for the tie bug |
|---|---|
| narrow (`1..3` mostly) | **560** |
| wide (`1..1000` everywhere) | **4** |

A factor of 140. Under the wide generator the bug shows up four times in four
thousand, which reads as a flake rather than a defect, and a smaller harness
would miss it outright. This is the whole argument for choosing the value range
deliberately instead of reaching for `rand()`.

## Benchmark

`bench/` builds **one 4,000 × 32 cost matrix once** — flat row-major, 1.0 MB,
deliberately cache-resident — and punches the ★ O(n·k) DP through it **1,300
times**, rotating the starting row each round so nothing is loop-invariant. Sink
`991930357`, reproduced by all four compiled mirrors and by Python.

Per house the DP does two passes over `k` values: a **reduction** tracking
`(min, its index, second-min)`, and a **map** writing the next row. The reduction
is the interesting half — its three-way update is a carried dependency with a
data-dependent branch — while the map beside it is vector-friendly. Rows are
strictly sequential. Costs are drawn from a narrow `1..40` band so tied row
minima are common and the `t == idx1` branch is genuinely exercised.

The two row buffers are allocated once and swapped rather than reallocated per
row, which keeps the lane about DP arithmetic rather than allocation —
[#254](../254-factor-combinations/) already measures that.

### What the x86 corroboration run shows

| lang | mean (ms) | σ |
|---|---|---|
| Rust | 260.8 ± 6.8 | 2.6% |
| Rust (checked, equal-safety) | 288.3 ± 12.8 | 4.4% |
| C | 305.7 ± 10.9 | 3.6% |
| C (`-march=x86-64-v3`) | 308.5 ± 10.7 | 3.5% |
| Rust (checked + `target-cpu=v3`) | 317.9 ± 21.3 | 6.7% |
| **Kāra** | **457.1 ± 11.2** | 2.4% |
| Go | 505.9 ± 15.3 | 3.0% |

**Kāra loses this lane, and by the widest margin in this corpus so far** — 1.58×
behind the equal-safety Rust build and 1.49× behind C. That is not noise (σ
2.4–4.4%) and it is not checked arithmetic, since the build it trails checks too.

The cause is in the emitted code. Counting conditional moves inside `main`:
`rustc -O` 133, `rustc -O -C overflow-checks=on` 127, `clang -O3` 129, **Kāra
17**. `rustc` fully unrolls the `k = 32` reduction into 32 straight-line blocks —
every `j` becomes a literal and each element is six branchless instructions.
Kāra unrolls by 4 and keeps a data-dependent `jl` per element. The trip count is
known to LLVM in both cases; only the unroll factor differs, and the
if-conversion appears to follow it.

Two controls, because instruction counts alone would not settle it:

| control | finding |
|---|---|
| all costs set to `1` (branch made predictable) | Kāra 457.1 → 263.2 ms, C 305.7 → 201.5, checked Rust 288.3 → 300.7 (unchanged, as branchless predicts). Kāra's deficit vs C narrows 1.49× → 1.31×, so **mispredictions are about a third of it** and the rest is instruction count. |
| Kāra source rewritten to match Rust's `else if` over a bound local | **byte-identical kernel** — same 403 lines, same 17 `cmov`, 452.9 ms vs 451.5. Not a spelling artifact. |

The buffer swap was also ruled out: a no-swap variant using one `2k` buffer
indexed by parity runs 445.8 ms against 477.5, a 7% difference with the same
sink, so `prev = cur` is a move and not a copy.

Filed as **`B-2026-08-13-10`** (class `perf`, medium) in the sibling `kara` repo.
Per the corpus rule the kata is unchanged — nothing here is worked around, and
the natural spelling stays in the file. Full disassembly and method in
[`bench/probe/README.md`](bench/probe/README.md).

Go is 505.9 ms, behind Kāra, but this lane does not investigate why and does not
guess.

Kāra's binary is 332.9 KiB against C's 15.8 KiB, Go's 2.16 MB and Rust's 3.87 MB;
peak RSS is 3.1 MiB against C's 2.4 MiB.

Published numbers await the Apple-silicon host —
`bench/results.container-x86.json` is corroboration only (BENCHMARKS.md § Hosts).

## Kāra features exercised

- **`Vec[Vec[i64]]` rows rebuilt per house**, with the previous row rebound
  rather than mutated (`prev = cur`).
- **Descending `while` with a signed index** (`b = k - 1; while b >= 0`), for
  the suffix pass.
- **A sentinel `INF` carried through arithmetic** and tested at the end, rather
  than an `Option` — the reason the impossible case stays representable.
- **`and` in an index guard** (`t > 0i64 and pre[t - 1i64] < best`), where the
  left operand is what makes the right one legal.

## Verification

Every program is byte-identical under `karac run --interp`, `karac run` (JIT),
`karac build` (auto-par default) and `KARAC_AUTO_PAR=0 karac build`; the ★ solver
and the differential match their Python mirrors.

No compiler bugs found — rolling DP rows, prefix/suffix scans and sentinel
arithmetic are all well-trodden ground in this corpus.

## Running

```bash
karac run paint_house_ii.kara
karac run paint_house_ii_quad.kara
karac run paint_house_ii_prefix.kara

diff <(karac run paint_house_ii.kara) <(python3 paint_house_ii.py) && echo OK
diff <(karac run paint_house_ii.kara) <(karac run paint_house_ii_quad.kara) && echo OK
diff <(karac run paint_house_ii.kara) <(karac run paint_house_ii_prefix.kara) && echo OK

# 4,000 randomized cost tables, three solvers cross-checked
diff <(karac run differential.kara) <(python3 differential.py) && echo "differential OK"

for f in paint_house_ii paint_house_ii_quad paint_house_ii_prefix differential; do
    karac build $f.kara && diff <(karac run --interp $f.kara) <(./$f) && echo "$f OK"
done
```

```bash
# cross-language benchmark (needs hyperfine, rustc, clang, go)
BENCH_OUT=results.container-x86.json bash bench/bench.sh
```
