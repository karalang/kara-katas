# 57. Insert Interval

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array &nbsp;·&nbsp; **Source:** [leetcode.com/problems/insert-interval](https://leetcode.com/problems/insert-interval/)

Given a list of closed intervals `[(start, end), ...]` already sorted by `start` and pairwise non-overlapping, plus one new interval, insert the new interval and merge any it overlaps (or touches — closed-interval semantics: `[1,3]` and `[3,5]` merge into `[1,5]`). Return the disjoint union in start order.

```
([(1,3),(6,9)], (2,5))                        → [(1,5), (6,9)]
([(1,2),(3,5),(6,7),(8,10),(12,16)], (4,8))   → [(1,2), (3,10), (12,16)]
([], (5,7))                                    → [(5,7)]
```

**Constraints:** `0 ≤ intervals.length ≤ 10^4`, `-10^5 ≤ start_i ≤ end_i ≤ 10^5`, input sorted by `start` with no overlap.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| **Linear three-phase sweep** — emit the left run, absorb the overlap window into the new interval, emit the right run | O(n) time, O(n) output | [`insert_interval.kara`](insert_interval.kara) ✓ via `karac run` / `karac build` | [`insert_interval.py`](insert_interval.py) ✓ |
| **Binary-search the merge window** — bisect for the first/last interval the new one touches, then splice | O(log n + k) search + O(n) copy | [`insert_interval_binary.kara`](insert_interval_binary.kara) ✓ | — |
| **Reduce to Merge Intervals** — push the new interval, sort by `start`, run the kata-56 sweep | O(n log n) | [`insert_interval_sort.kara`](insert_interval_sort.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter and codegen produce identical output across all ten test cases, and all three approaches agree with each other and with the Python mirror.

## Why three phases?

The input is already sorted by `start` and disjoint, so the answer is the concatenation of three contiguous runs:

```
[ intervals that end before new_start ]  ++  [ one merged interval ]  ++  [ intervals that start after new_end ]
        left run — untouched                    the overlap window              right run — untouched
```

The **linear** solution walks left-to-right and switches phase as it goes: push while `cur.end < new_start`, then absorb while `cur.start <= new_end` (widening `new_start`/`new_end` to `min`/`max`), then push the rest. The `<=` in the absorb test is what enforces closed-interval touching — `[1,3]` + new `[3,6]` merge because `3 <= 3`; flipping to `<` gives half-open behavior. Pinned by test cases 6 + 7.

The two guards in the absorb phase (`cur.0 < new_start` and `cur.1 > new_end`) are both needed for the **nested** case: new `[3,5]` inside existing `[1,10]` must leave the window at `[1,10]`, not shrink it to `[3,5]`. Pinned by test case 8 — the case that catches the bug if either guard is dropped.

The **binary-search** solution ([`insert_interval_binary.kara`](insert_interval_binary.kara)) notes that both phase boundaries are monotone predicates over sorted data, so each can be found by a lower-bound bisect instead of a linear scan: `lo = first i with intervals[i].end >= new_start`, `hi = first i with intervals[i].start > new_end`. The window is exactly `intervals[lo .. hi]`; the search is O(log n), the copy O(n). Kāra v1 has no predicate `partition_point`, and `Slice.binary_search` searches for an *equal key* rather than a partition point (its codegen path is integer/String-element-only anyway — tuple elements fall to an interpreter-only Err), so the two bisects are written out with the canonical `while lo < hi { mid = lo + (hi-lo)/2; ... }` lower-bound loop.

The **sort** solution ([`insert_interval_sort.kara`](insert_interval_sort.kara)) throws the precondition away and reduces to [kata #56](../56-merge-intervals/): push the new interval, `sort_by(|a, b| a.0.cmp(b.0))`, sweep. Asymptotically worse, but the shortest correct answer and a useful independent cross-check.

## Kāra features exercised

- **`Slice[(i64, i64)]` parameter + `Vec[(i64, i64)]` output** — the tuple-typed collection shape from [kata #56](../56-merge-intervals/); `Vec.push((new_start, new_end))` builds tuple literals, `Vec.from_slice(intervals)` copies (sort variant).
- **Tuple field access on an index result** — `intervals[i].0` / `.1`, i.e. `.N` indexing on the value produced by `Slice`-index. Both the let-bound form (`let cur = intervals[i]; cur.1`) and the fully inline form (`intervals[i].1` inside a `while` condition) lower correctly on interpreter *and* codegen — the index-then-field placeholder trap does **not** fire for tuple elements here, which this kata verifies directly.
- **`Vec[(i64, i64)].sort_by(|a, b| a.0.cmp(b.0))`** (sort variant) — sort by primary tuple component, routed through karac's Slice 6.4 integer-tuple mono sort path (the fix [kata #56](../56-merge-intervals/) triggered).
- **Manual lower-bound bisect** (binary variant) — `let mid = lo + (hi - lo) / 2i64` overflow-safe midpoint plus the branch-on-predicate loop; pure i64 index arithmetic over a sorted `Slice`.
- **`break` out of a `while`** — the linear solution switches phase by `break`-ing the current loop when its predicate fails, rather than folding the condition into the `while` header; same control-flow shape as an early `return`.
- **Empty-`Array` literal with explicit length** — `let case3: Array[(i64, i64), 0] = [];` exercises the zero-length array-to-slice path (the "insert into nothing" edge case).

## Running

```bash
# Kāra — interpreter and codegen produce the same output today.
karac run   insert_interval.kara
karac build insert_interval.kara && ./insert_interval

# The two alternative approaches (identical output):
karac run insert_interval_binary.kara
karac run insert_interval_sort.kara

# Python
python3 insert_interval.py

# Verify they all agree
diff <(karac run insert_interval.kara)        <(python3 insert_interval.py)        && echo OK
diff <(karac run insert_interval.kara)        <(karac run insert_interval_binary.kara) && echo OK
diff <(karac run insert_interval.kara)        <(karac run insert_interval_sort.kara)   && echo OK

# Full cross-language benchmark (Kāra / Rust / C / Go / Python + auto-par lanes)
bench/bench.sh
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`insert_interval.{kara,rs,c,py}`, `go-seq/main.go`, plus the par-lane `insert_interval_par.c`, `go-par/`, `rayon/`).

**Workload.** M = 8 distinct cases, each a `Vec[(i64, i64)]` of N = 16 intervals that are **already sorted and pairwise disjoint** — #57's precondition. `build_case` walks a cursor forward, placing each interval after a gap of `[2, 5]` (so the list is strictly disjoint) with width `[1, 6]`, both drawn from a deterministic 31-bit LCG. Each case carries a per-case `new_interval` (independent seed) that overlaps a middle run `intervals[lo .. hi]`. K = 1,000,000 outer iterations rotate `idx = k % M` and call `insert_interval` on that case. Per call: a linear O(N) three-phase sweep and one fresh `Vec[(i64, i64)]` output — **no sort** (the precondition removes it, which is the whole point of #57 vs #56). The sink — the running total of every returned `Vec`'s `.len()` — is **11,500,000** across all mirrors; `bench.sh` fails loudly on mismatch.

Same M=8/N=16/K=1M shape as [kata #56](../56-merge-intervals/), so cross-kata wall-time comparisons stay meaningful. The key structural difference: #56's per-call cost is dominated by an O(N log N) `sort_by`; this kata's is a pure O(N) sweep, so the workload isolates the **allocation + tuple index + field-access + `Vec.push`** path with no sort-dispatch in the picture.

Two-lane kata (BENCH.md § Implicit auto-par): the `sum = sum + r.len()` accumulator is the slice-1 allow-list reduction shape, so the default `karac build` parallelises it — verified in the emitted IR (`KARAC_MIR_LL`): the default build carries a call of `karac_mir_task_spawn`, the `KARAC_AUTO_PAR=0` build does not. The bench builds both kara binaries — `KARAC_AUTO_PAR=0` for the within-lane seq comparison, default for the auto-par regime — reported in separate tables.

Measured 2026-10-31 (`measured_at` 2026-11-01T02:19Z) — Apple M5 Pro (6P+12E), Darwin 25.6.0, hyperfine `--warmup 5`, 30 seq / 50 par runs. karac `g6697158fa` (0.9.0-dev.14057, v2/MIR backend), rustc 1.95.0, Apple clang 21.0.0, go 1.26.3. All numbers below are from the committed [`results.json`](bench/results.json) unless marked otherwise.

### Runtime — seq lane

All single-threaded; the kāra rows are `KARAC_AUTO_PAR=0`.

| Implementation | Wall time |
|---|---|
| c    insert_interval (clang -O3)     | **22.6 ± 1.2 ms** |
| **kāra insert_interval (with_capacity)** | **25.2 ± 1.4 ms** |
| **kāra insert_interval (seq, `Vec.new()`)** | **44.5 ± 1.0 ms** |
| go   insert_interval                 | 52.2 ± 0.7 ms |
| rust insert_interval (`overflow-checks=on`) | 79.4 ± 2.8 ms |
| rust insert_interval                 | 80.4 ± 5.3 ms |

The load-bearing result is **Kāra vs Rust on the natural idiom: 44.5 vs 80.4 ms — Kāra leads by 1.81× (Kāra/Rust 0.55×)**, and it is also ahead of Go (0.85×). Against the previous run (2026-07-28, legacy backend) that is a sharp improvement in every ratio: Kāra/Rust 0.90× → 0.55×, Kāra/C 3.42× → 1.97×, Kāra/Go 2.15× → 0.85×. This is an *allocation-bound* workload: with no sort, each call's cost is dominated by allocating and growing a fresh `Vec[(i64, i64)]` from empty (`Vec.new()` + `push`), and Kāra now does that grow-from-empty path well ahead of Rust's `Vec` doing the identical growth. Because there's no sort to route through a runtime callback, this is the cleanest "Kāra vs Rust on the natural idiom" data point in the corpus. **When the output is pre-sized (`with_capacity`), Kāra comes within 1.11× of C — see § Optimization below.**

**C's 1.97× lead over `Vec.new()` is a benchmark-fairness note worth stating.** A naive C mirror that returns only the interval *count* lets clang prove the result buffer is a dead `malloc`/`free` pair and elide the allocation entirely — which clocked C at **3.7 ms (a 20× artifact)** in the 2026-07-03 probe. The committed [`insert_interval.c`](bench/insert_interval.c) forces the allocation to escape through a `volatile` sink read from the materialized buffer, so all seq lanes genuinely allocate. C's remaining lead is real but structural: it `malloc`s the max size (`n+1`) **once**, while the `Vec.new()` kāra and rust mirrors grow from empty with reallocations. That structural gap is exactly what the pre-sized variant closes.

### Optimization — pre-sizing the output

The output length of `insert_interval` is bounded by `n + 1`, known before the sweep starts. The default solution returns `Vec.new()` and grows it by `push` (reallocating 0 → 1 → 2 → 4 → 8 → 16 each call); reserving that bound up front with `Vec.with_capacity(intervals.len() + 1)` removes every realloc. The only line that changes is the `result` binding — see [`bench/insert_interval_cap.kara`](bench/insert_interval_cap.kara).

| kāra seq variant | Wall time | Peak RSS | vs C |
|---|---|---|---|
| `Vec.new()` (default) | 44.5 ± 1.0 ms | 1.05 MiB | 1.97× behind |
| **`Vec.with_capacity(n+1)`** | **25.2 ± 1.4 ms** | **1.05 MiB** | **1.11× behind** |
| c insert_interval | 22.6 ± 1.2 ms | 1.05 MiB | — |

**Pre-sizing is a 1.77× speedup (44.5 → 25.2 ms) that lands Kāra at 1.11× of C** — most of the seq gap to C is the grow-from-empty realloc tax, not codegen quality. (The previous run had it at 2.92× and 1.17×; the MIR backend shrank the realloc tax itself, so pre-sizing now buys less.) Peak RSS no longer separates the two variants: all three rows peak at 1.05 MiB (1 098 064 bytes for both kāra builds, 1 098 040 for C), where the 2026-07-03 snapshot had `Vec.new()` a page higher (1.1 vs 1.0 MiB) from the doubling transient. This is the same lever [kata #153](../../101-200/153-find-minimum-in-rotated-sorted-array/) documents `Vec.with_capacity` closing. The default solution keeps `Vec.new()` for teaching clarity; pre-sizing is the drop-in a perf-conscious caller applies (and exactly what Rust's `Vec::with_capacity` would do for the rust mirror too). A possible *compiler-level* follow-on would be for karac to statically bound the push-count and emit the reservation itself, which `rustc` does not do — filed as a speculative codegen idea, not attempted.

### Runtime — auto-par regime

The `sum = sum + r.len()` reduction is auto-par-eligible:

| Implementation | Wall time | User-CPU |
|---|---|---|
| **kāra insert_interval (auto-par default)** | **12.4 ± 1.4 ms** | 127 ms |
| rust insert_interval (rayon par_iter) | 24.7 ± 4.1 ms | 351 ms |
| go   insert_interval (goroutines) — count-only floor | 3.1 ± 0.1 ms | 10 ms |
| c    insert_interval (pthreads) — count-only floor | 1.6 ± 0.1 ms | 4 ms |

Kāra auto-par (12.4 ms) **is 1.99× faster than Rust's hand-written rayon (24.7 ms), Kāra/rayon 0.50×** — the apples-to-apples pair (both allocate a real `Vec` per iter, both `Vec.new()`), and on 0.36× of rayon's user-CPU. Against the previous run that is a sharp improvement: Kāra/rayon 1.14× → 0.50×. The auto-par binary is **3.6× faster than the kāra `Vec.new()` seq binary** (44.5 → 12.4 ms), still below [kata #56](../56-merge-intervals/)'s 6.7× (2026-07-03 figure): with the O(N log N) sort gone, each iteration does far less work, so the fixed per-iteration parallel-dispatch overhead amortizes worse — there's less to spread across the perf cores (User-CPU is ~10× wall). The `c`/`go` par rows are **count-only floors** (no allocation, by design — the bare-metal ceiling), which is why they sit far below the allocating lanes; they are not apples-to-apples with kāra/rust here.

### Runtime — Python

| Run | Mean ± σ |
|---|---|
| `py insert_interval` (K=100k) | 58.3 ± 2.3 ms (last measured 2026-07-03, not re-run) |

Python at K=100k was 58 ms; projecting to K=1M (~583 ms) puts it **~13× slower than this run's kāra `Vec.new()` seq** (and ~23× slower than the pre-sized variant) — cross-session ratios, since Python was not re-run. Lighter multiple than a sort-heavy kata because CPython's per-call overhead is amortized over less native work when there's no `sorted()` to lean on.

### Compile elapsed (cold)

`--warmup 1 --runs 10 --prepare 'rm -f <artifact>'`:

| Compiler | Time |
|---|---|
| clang -O3 insert_interval.c          | **53.9 ± 0.8 ms** |
| rustc -O insert_interval.rs          | 127.6 ± 2.9 ms |
| **karac build insert_interval.kara** | **178.7 ± 5.5 ms** |

Compile now favours `rustc -O`: karac is **1.40× slower than `rustc -O`** and **3.32× clang -O3** (the previous run had karac 1.06× faster than rustc). The same flip shows across the corpus under the MIR backend (tracked as [`B-2026-10-31-41`](../../../../kara/docs/bugs-v2.md)).

### Binary size

| Implementation | Size |
|---|---|
| c    insert_interval (seq)           | 32.8 KiB |
| **kāra insert_interval (seq / with_capacity)** | **295.8 KiB** |
| **kāra insert_interval (auto-par)**  | **377.1 KiB** |
| rust insert_interval (seq)           | 455.7 KiB |
| go   insert_interval (seq)           | 2434.2 KiB |

Kāra seq is **295.8 KiB** — 1.5× under Rust's 455.7 KiB but 9× C's 32.8 KiB; every MIR-backend Kāra binary is ~300–390 KB where the legacy backend's were ~34 KB (tracked as [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md)). The pre-sized variant is the same size (302 880 bytes, though not byte-identical). The auto-par binary's +81 KiB over seq is the par-scheduler runtime, not a sort floor.

### Runtime memory (peak)

| Implementation | Peak |
|---|---|
| c    insert_interval (seq)           | 1.05 MiB |
| **kāra insert_interval (with_capacity)** | **1.05 MiB** |
| **kāra insert_interval (seq, `Vec.new()`)** | **1.05 MiB** |
| rust insert_interval (seq)           | 1.08 MiB |
| **kāra insert_interval (auto-par)**  | **2.09 MiB** |
| go   insert_interval (seq)           | 9.67 MiB |

Kāra seq's peak RSS ties C's to 24 bytes (1 098 064 vs 1 098 040) and sits under Rust's 1.08 MiB; the pre-sized variant now peaks at exactly the same bytes as `Vec.new()`. The auto-par regime's 2.09 MiB is the worker pool's per-thread scratch.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 insert_interval.c          | 2.5 MiB |
| rustc -O insert_interval.rs          | 31.0 MiB |
| **karac build insert_interval.kara** | **61.8 MiB** |

Kāra's compile-memory footprint is ~24× clang's and ~2.0× rustc's on this kata (the previous run had it ~1.2× *under* rustc) — same flip as compile elapsed above.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio is the codegen-vs-Rust gap. On this kata the **Kāra/Rust 0.55× seq lead (and 0.50× auto-par lead over rayon) is the load-bearing result** — an allocation-bound sweep with no sort, where Kāra's `Vec` allocation + push path now runs well ahead of Rust's. C calibrates the LLVM-backend floor (and here doubled as two lessons: dead-allocation elision, § Runtime seq lane, and the pre-sizing win that comes within 1.11× of it, § Optimization), Go is the cross-runtime data point, and Python is the ergonomic foil.
