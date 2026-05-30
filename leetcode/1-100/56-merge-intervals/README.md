# 56. Merge Intervals

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array, Sorting &nbsp;·&nbsp; **Source:** [leetcode.com/problems/merge-intervals](https://leetcode.com/problems/merge-intervals/)

Given an array of closed intervals `[(start, end), ...]`, merge any that overlap (or touch — `[1,4]` and `[4,5]` merge into `[1,5]` per LeetCode's closed-interval semantics) and return the disjoint union in start order.

```
([(1,3),(2,6),(8,10),(15,18)])  → [(1,6), (8,10), (15,18)]
([(1,4),(4,5)])                  → [(1,5)]              (touching merges)
([(8,10),(1,3),(2,6)])           → [(1,6), (8,10)]      (sort first)
```

**Constraints:** `1 ≤ intervals.length ≤ 10^4`, `0 ≤ start_i ≤ end_i ≤ 10^4`.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| Sort by `start`, then sweep merging while `next.start <= cur_end` | O(n log n) time, O(n) extra (sorted copy + output) | [`merge_intervals.kara`](merge_intervals.kara) ✓ via `karac run` / `karac build` | [`merge_intervals.py`](merge_intervals.py) ✓ |

`✓` runs end-to-end today. Interpreter and codegen produce identical output to the Python mirror across all nine test cases.

## Why sort + sweep?

Brute force compares every pair O(n²); sorting first reduces the problem to a single linear pass because once the input is sorted by `start`, any interval that overlaps the running `(cur_start, cur_end)` window must do so at the *left* edge — the next interval's `start <= cur_end` is the necessary-and-sufficient overlap test. Three branches per sweep step:

```
next.start <= cur_end and next.end > cur_end ⇒ extend the running pair
next.start <= cur_end and next.end <= cur_end ⇒ nested, no change
next.start > cur_end                          ⇒ emit running pair, reset
```

The "nested, no change" branch is what makes the sweep work — without `next.end > cur_end` guarding the extend, a nested interval like `[1,10] [2,3]` would *shrink* the running window to `[1,3]`. Pinned by test case 7 (the case that catches the bug if the guard is missing).

The closed-interval semantics for "touching" (`[1,4]` + `[4,5]` → `[1,5]`) are LeetCode's stated rule and pinned by test cases 2 + 8. The `<=` in the overlap test is the only line of code that enforces it; flipping to `<` produces half-open behavior.

## Kāra features exercised

- **`Vec[(i64, i64)]` element type** — both the input `Vec.from_slice` copy and the output `Vec.push((cur_start, cur_end))` use the tuple-typed Vec; tuple literals `(start, start + width)` (in the bench's `build_case`) and the destructure pattern `let (actual, minimum) = t` (used in [kata #1665](../../1601-1700/1665-minimum-initial-energy-to-finish-tasks/)'s sweep) both ride this same shape.
- **`Vec[(i64, i64)].sort_by(|a, b| a.0.cmp(b.0))`** — sort by primary-tuple-component, the canonical "sort intervals/records by their first key" idiom. Kāra v1 currently routes this through `karac_vec_sort_by`'s runtime callback path because Slice 6.1's mono fast path is gated on i64 elem type. The bench below quantifies the gap this leaves on the table — this kata is the **natural-pull trigger for Slice 6.4** (tuple/struct elem mono sort) in karac's [`phase-7-codegen.md`](https://github.com/karalang/kara/blob/main/docs/implementation_checklist/phase-7-codegen.md).
- **Tuple field access `interval.0` / `interval.1`** — `.N` indexing on a tuple value (not a tuple type's named field), the same shape kata #1665's `(b.1 - b.0).cmp(a.1 - a.0)` uses for arithmetic on tuple components.
- **Early `return` from inside a function** — `if n == 0i64 { return result; }` short-circuits when the input is empty, same shape as kata [#1](../1-two-sum/)'s brute-force `return [i, j]` and kata [#16](../16-3sum-closest/)'s exact-hit return.
- **Scalar `+` reduction in the bench** — `sum = sum + r.len()` is the slice-1 auto-par-on-reduction allow-list shape recognized by default in `karac build` and lowered to a `karac_par_reduce` dispatch.

## Running

```bash
# Kāra — interpreter and codegen produce the same output today.
karac run   merge_intervals.kara
karac build merge_intervals.kara && ./merge_intervals

# Python
python3 merge_intervals.py

# Verify they agree
diff <(./merge_intervals) <(python3 merge_intervals.py) && echo OK
diff <(karac run merge_intervals.kara) <(python3 merge_intervals.py) && echo OK
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`merge_intervals.{kara,rs,c,py}`, `go-seq/main.go`).

**Workload.** M = 8 distinct test cases, each a `Vec[(i64, i64)]` of N = 16 intervals drawn from a deterministic 31-bit LCG: each interval is `(start, start + width)` where `start` is sampled from `[0, 50]` and `width` from `[1, 10]`. The bounded-width construction guarantees `start <= end` and produces a mix of overlapping / disjoint cases so the sweep does real merging work. Built once into a `Vec[Vec[(i64, i64)]]` before the timed loop. K = 1,000,000 outer iterations rotate `idx = k % M` and call `merge_intervals` on that case. Per call: a `Vec.from_slice` copy of N pairs, an O(N log N) sort by first tuple component, an O(N) sweep, and one `Vec[(i64, i64)]` output. The sink — the running total of every returned `Vec`'s `.len()` — is **3,000,000** across all five mirrors; bench.sh fails loudly on mismatch.

Same M=8/N=16/K=1M shape as katas [#15](../15-3sum/) and [#16](../16-3sum-closest/), so cross-kata wall-time comparisons stay meaningful. The key difference: this kata sorts a **tuple-typed Vec**, not a `Vec[i64]`. Kata 15/16's `sort_by(|a, b| a.cmp(b))` on `Vec[i64]` hits karac's Slice 6.1 mono fast path (per-call-site `__vec_i64_sort_by_mono_<id>` emitted into the user binary); this kata's `sort_by(|a, b| a.0.cmp(b.0))` on `Vec[(i64, i64)]` does NOT — the mono gate is i64-elem-only in v1. Both kara binaries built by bench.sh route through `karac_vec_sort_by`'s runtime callback per comparison.

Two-lane kata (BENCH.md § Implicit auto-par): the `sum = sum + r.len()` accumulator is the slice-1 allow-list reduction shape, so `karac build` may emit a `karac_par_reduce` dispatch by default. The bench builds two kara binaries — `KARAC_AUTO_PAR=0` for the within-lane seq comparison, default for the auto-par regime — and reports them in separate tables per the two-lane discipline.

### Runtime — seq lane

Snapshot — M5 Pro, 2026-05-29, hyperfine `--warmup 5 --runs 30 --shell=none`. All four comparators single-threaded; the kāra row is `KARAC_AUTO_PAR=0`.

| Implementation | Wall time |
|---|---|
| rust merge_intervals                  | **61.1 ± 0.9 ms** |
| **kāra merge_intervals (seq)**        | **91.5 ± 1.5 ms** |
| c    merge_intervals (clang -O3)      | 96.3 ± 0.9 ms |
| go   merge_intervals                  | 416.3 ± 14.6 ms |

Rust leads by **1.50×** over Kāra seq — the same shape that kata 16 originally showed pre-Slice-6.1 (1.55× there). The cause is the same too: `karac_vec_sort_by`'s per-compare callback through `extern "C" fn` pointer, while Rust's `sort_by` monomorphizes the comparator inline. The diagnosis is grounded in three corroborating signals:

1. **C trails Kāra by 1.06×** (96.3 vs 91.5 ms), not the typical 1.14–1.17× of the corpus norm. C also pays a `qsort` indirect-call-per-comparison, the same cost-shape Kāra has on this kata; with both paying the same dispatch cost, they land close. Compare kata 16 post-Slice-6.1 where Kāra leads C by **1.69×** (because Kāra no longer pays the indirection there).

2. **Kāra binary size is 410.8 KiB** — well above kata 16's post-Slice-6.1 33.0 KiB. The runtime archive's `karac_vec_sort_by` + the comparator-fat-pointer + drop helpers + dependent symbols all stay linked because nothing eliminates them. Kata 16 post-Slice-6.1 DCE'd them by routing around `karac_vec_sort_by` entirely.

3. **The sort_by call site is the only difference from kata 16 post-Slice-6.1.** Both katas use the same M/N/K shape, the same allocator-stress profile (per-call `Vec[T]` output), the same sweep-over-sorted-data inner loop. Kata 16 with i64 elements lands at 1.06× of Rust; kata 56 with tuple elements lands at 1.50× of Rust. The element-type change is the *only* variable that shifted.

This kata is the **natural-pull trigger for Slice 6.4** (`Vec[(i64, i64)] / Vec[(i64, i64, i64)] / Vec[struct S]` mono sort) in karac's [`phase-7-codegen.md`](https://github.com/karalang/kara/blob/main/docs/implementation_checklist/phase-7-codegen.md) Slice 6 trigger entry. Once Slice 6.4 ships with tuple-element support — where the mono path emits insertion sort with the comparator's tuple-field-access body inlined — this kata should drop from 91.5 ms to ~62 ms (matching kata 16's 1.06× of Rust) and the binary should collapse from 410 KiB to ~33 KiB (matching kata 16's DCE story).

Go trails further at **4.55× behind Kāra seq**: `sort.Slice` also pays a per-comparison closure indirect-call, the `[]Interval` allocator has GC behind it, and Go's tuple-equivalent (the struct value `Interval{Start, End}`) carries a 16-byte payload per element that loads twice per compare. Go's combined cost compounds — even though it pays the same dispatch overhead as Kāra and C, its allocator and GC tax stack on top.

### Runtime — auto-par regime

The `sum = sum + r.len()` reduction is auto-par-eligible:

| Implementation | Wall time | User-CPU |
|---|---|---|
| **kāra merge_intervals (auto-par default)** | **10.7 ± 1.1 ms** | 120.9 ms |

The auto-par binary is **8.6× faster than the kāra seq binary** (91.5 → 10.7 ms), spreading the K=1M case-rotation reduction across the perf cores (~11× user-CPU-to-wall ratio on M5 Pro). When Slice 6.4 lands, the auto-par lane's absolute time should also drop (each worker runs the faster mono body) but the ratio against seq will compress because the seq baseline drops more.

### Runtime — Python

| Run | Mean ± σ |
|---|---|
| `py merge_intervals` (K=100k) | 105.5 ± 0.9 ms |

Python at K=100k is 106 ms; projecting to the compiled mirrors' K=1M (~1.06 s) puts it **~11.5× slower than kāra seq**. CPython's `sorted(key=lambda x: x[0])` is a C-implemented stable sort with the key extracted in interpreter code per element; the per-iteration overhead is amortized over the heavy per-call sort+sweep work. Once Slice 6.4 ships, kāra seq's wall time drops ~30 ms and the python ratio widens to ~17×.

### Compile elapsed (cold)

`--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Compiler | Time |
|---|---|
| clang -O3 merge_intervals.c           | **50.1 ± 0.5 ms** |
| **karac build merge_intervals.kara**  | **72.7 ± 0.4 ms** |
| rustc -O merge_intervals.rs           | 128.5 ± 0.6 ms |

Kāra compiles **1.77× faster than `rustc -O`** and sits at **1.45× of clang -O3** — same shape as the rest of the corpus.

### Binary size

| Implementation | Size |
|---|---|
| c    merge_intervals            | 32.8 KiB |
| **kāra merge_intervals (seq)**  | **410.8 KiB** |
| **kāra merge_intervals (auto-par)** | **450.4 KiB** |
| rust merge_intervals            | 473.0 KiB |
| go   merge_intervals            | 2452.2 KiB |

Kāra seq lands at **410.8 KiB** — within 62 KiB of Rust but well above C's 32.8 KiB. This is the second piece of trigger evidence: kata 15/16 post-Slice-6.1 both ship at 33.0 KiB because `karac_vec_sort_by` and its transitive runtime archive surface get DCE'd; this kata can't DCE them because the runtime path is still load-bearing. The auto-par delta (+39.6 KiB over seq) is the additional `karac_par_reduce` surface. When Slice 6.4 lands, the seq binary should collapse to ~33 KiB matching kata 15/16.

### Runtime memory (peak)

| Implementation | Peak |
|---|---|
| c    merge_intervals            | 1.1 MiB |
| **kāra merge_intervals (seq)**  | **1.1 MiB** |
| rust merge_intervals            | 1.2 MiB |
| **kāra merge_intervals (auto-par)** | **2.2 MiB** |
| go   merge_intervals            | 9.8 MiB |

Kāra seq's peak RSS is within 16 KiB of C and Rust — the per-iter `Vec[(i64, i64)]` output is allocated and freed inside `merge_intervals` so steady state stays flat across K=1M. The auto-par regime's 2.2 MiB is the worker pool's per-thread scratch + partials.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 merge_intervals.c          | 2.6 MiB |
| **karac build merge_intervals.kara** | **10.4 MiB** |
| rustc -O merge_intervals.rs          | 39.1 MiB |

Kāra's compile-memory footprint is ~4.0× clang's and ~3.8× lower than rustc's on this kata — same shape as the rest of the corpus.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio is the codegen-vs-Rust gap. C calibrates the LLVM-backend floor, Go is the cross-runtime data point, and Python is the ergonomic foil. On this kata the **Kāra/Rust 1.50× gap is the load-bearing result** — and the way kata 56 sits structurally identical to kata 16-pre-Slice-6.1 (1.55× behind Rust, ~410 KiB binary, C close behind) is the trigger evidence for karac's Slice 6.4. Kata 16 post-Slice-6.1 demonstrates what the post-fix shape looks like (1.06× of Rust, 33 KiB binary, C left far behind); this kata sits exactly where kata 16 was before the fix landed, and the kata 56 → Slice 6.4 → re-bench loop is the same shape as the kata 16 → Slice 6.1 → re-bench loop that already shipped.
