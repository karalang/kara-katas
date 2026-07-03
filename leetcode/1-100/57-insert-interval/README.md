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

Two-lane kata (BENCH.md § Implicit auto-par): the `sum = sum + r.len()` accumulator is the slice-1 allow-list reduction shape, so `karac build` may emit a `karac_par_reduce` dispatch by default. The bench builds two kara binaries — `KARAC_AUTO_PAR=0` for the within-lane seq comparison, default for the auto-par regime — reported in separate tables.

Snapshot — Apple M5 Pro (6P+12E), Darwin 25.5.0, 2026-07-03, hyperfine `--warmup 5 --runs 30 -N`. karac 0.1.0, rustc 1.95.0, Apple clang 21.0.0, go 1.26.3.

### Runtime — seq lane

All four single-threaded; the kāra row is `KARAC_AUTO_PAR=0`.

| Implementation | Wall time |
|---|---|
| c    insert_interval (clang -O3)     | **22.1 ± 1.1 ms** |
| go   insert_interval                 | 38.5 ± 0.7 ms |
| **kāra insert_interval (seq)**       | **77.1 ± 3.2 ms** |
| rust insert_interval                 | 79.9 ± 3.1 ms |

The load-bearing result is **Kāra vs Rust: 77.1 vs 79.9 ms — Kāra leads by 1.04×**, inside noise. This is an *allocation-bound* workload: with no sort, each call's cost is dominated by allocating and growing a fresh `Vec[(i64, i64)]` from empty (`Vec.new()` + `push`), and Kāra's allocator + move-elision keep it level with Rust's `Vec` doing the identical growth. This is the cleanest "Kāra ties Rust on the natural idiom" data point in the corpus precisely *because* there's no sort to route through a runtime callback.

**C's 3.48× lead is a benchmark-fairness note worth stating.** A naive C mirror that returns only the interval *count* lets clang prove the result buffer is a dead `malloc`/`free` pair and elide the allocation entirely — which clocked C at **3.7 ms (a 20× artifact)**. The committed [`insert_interval.c`](bench/insert_interval.c) forces the allocation to escape through a `volatile` sink read from the materialized buffer, so all four seq lanes genuinely allocate. C's remaining lead is real but structural: it `malloc`s the max size (`n+1`) **once**, while the Kāra and Rust mirrors grow a `Vec` from empty with reallocations — the natural idiom the kata solution uses. Go's 38.5 ms sits between, with its GC'd slice `append`.

### Runtime — auto-par regime

The `sum = sum + r.len()` reduction is auto-par-eligible:

| Implementation | Wall time | User-CPU |
|---|---|---|
| **kāra insert_interval (auto-par default)** | **28.1 ± 3.2 ms** | 393 ms |
| rust insert_interval (rayon par_iter) | 26.5 ± 4.4 ms | 414 ms |
| go   insert_interval (goroutines) — count-only floor | 3.1 ± 0.1 ms | 10 ms |
| c    insert_interval (pthreads) — count-only floor | 1.6 ± 0.1 ms | 4 ms |

Kāra auto-par (28.1 ms) **matches Rust's hand-written rayon (26.5 ms), 1.06×** — again the apples-to-apples pair (both allocate a real `Vec` per iter). But the auto-par binary is only **2.7× faster than the kāra seq binary** (77.1 → 28.1 ms), well below [kata #56](../56-merge-intervals/)'s 6.7×. That gap *is* the story: with the O(N log N) sort gone, each iteration does far less work, so the fixed per-iteration parallel-dispatch overhead amortizes much worse — there's less to spread across the perf cores (User-CPU is only ~14× wall). The `c`/`go` par rows are **count-only floors** (no allocation, by design — the bare-metal ceiling), which is why they sit ~17× below the allocating lanes; they are not apples-to-apples with kāra/rust here.

### Runtime — Python

| Run | Mean ± σ |
|---|---|
| `py insert_interval` (K=100k) | 59.2 ± 0.4 ms |

Python at K=100k is 59 ms; projecting to K=1M (~592 ms) puts it **~7.7× slower than kāra seq**. Lighter multiple than a sort-heavy kata because CPython's per-call overhead is amortized over less native work when there's no `sorted()` to lean on.

### Compile elapsed (cold)

`--warmup 1 --runs 10 --prepare 'rm -f <artifact>'`:

| Compiler | Time |
|---|---|
| clang -O3 insert_interval.c          | **53.7 ± 2.1 ms** |
| **karac build insert_interval.kara** | **90.1 ± 1.0 ms** |
| rustc -O insert_interval.rs          | 126.1 ± 5.2 ms |

Kāra compiles **1.40× faster than `rustc -O`** and sits at **1.68× of clang -O3** — same shape as the rest of the corpus.

### Binary size

| Implementation | Size |
|---|---|
| c    insert_interval (seq)           | 32.8 KiB |
| **kāra insert_interval (seq)**       | **33.3 KiB** |
| **kāra insert_interval (auto-par)**  | **312.8 KiB** |
| rust insert_interval (seq)           | 455.7 KiB |
| go   insert_interval (seq)           | 2434.2 KiB |

Kāra seq sits at **33.3 KiB** — within 0.5 KiB of C's no-frills 32.8 KiB, because with no sort there's no `karac_vec_sort_by` runtime fallback to drag `slice::sort_by`'s panic/backtrace machinery into the link (the floor katas 15/16/56 had to `-dead_strip` away). The auto-par binary's +279 KiB over seq is the par-scheduler runtime, not a sort floor.

### Runtime memory (peak)

| Implementation | Peak |
|---|---|
| c    insert_interval (seq)           | 1.0 MiB |
| **kāra insert_interval (seq)**       | **1.1 MiB** |
| rust insert_interval (seq)           | 1.1 MiB |
| **kāra insert_interval (auto-par)**  | **2.3 MiB** |
| go   insert_interval (seq)           | 9.5 MiB |

Kāra seq's peak RSS is within a page of Rust and C — the per-iter `Vec[(i64, i64)]` output is allocated and freed inside `insert_interval` so steady state stays flat across K=1M. The auto-par regime's 2.3 MiB is the worker pool's per-thread scratch.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 insert_interval.c          | 2.6 MiB |
| **karac build insert_interval.kara** | **20.7 MiB** |
| rustc -O insert_interval.rs          | 31.0 MiB |

Kāra's compile-memory footprint is ~8× clang's and ~1.5× lower than rustc's on this kata — same shape as the rest of the corpus.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio is the codegen-vs-Rust gap. On this kata the **Kāra/Rust 1.04× seq tie (and 1.06× auto-par tie) is the load-bearing result** — an allocation-bound sweep with no sort, where Kāra's `Vec` allocation + move-elision land level with Rust's. C calibrates the LLVM-backend floor (and here doubled as a lesson in dead-allocation elision — see § Runtime seq lane), Go is the cross-runtime data point, and Python is the ergonomic foil.
