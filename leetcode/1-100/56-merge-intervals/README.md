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

Snapshot — M5 Pro, 2026-05-29, hyperfine `--warmup 5 --runs 30 --shell=none`. All four comparators single-threaded; the kāra row is `KARAC_AUTO_PAR=0`. Numbers below are with the karac Slice 6.4 mono fast path landed (see § Sort-dispatch history below for the pre-fix story).

| Implementation | Wall time |
|---|---|
| rust merge_intervals                  | **61.5 ± 1.2 ms** |
| **kāra merge_intervals (seq)**        | **65.0 ± 1.6 ms** |
| c    merge_intervals (clang -O3)      | 97.5 ± 1.0 ms |
| go   merge_intervals                  | 421.9 ± 1.9 ms |

Rust leads by **1.06×** over Kāra seq — well inside codegen-quality noise on a sort + sweep workload where both compilers now monomorphize the tuple-element comparator. **Kāra leads C by 1.50×** (was only 1.06× pre-fix); the qsort indirect-call penalty C carries is no longer offset on the Kāra side because Kāra no longer pays the equivalent runtime-callback cost on this N=16 workload. **Go trails by 6.49×**: `sort.Slice` still pays the per-compare closure indirect-call, and the `[]Interval` allocator has GC behind it that the manual-free mirrors don't carry.

#### Sort-dispatch history (kata 56 → karac Slice 6.4)

**Pre-fix (kata 56 ship 2026-05-29, commit `558edc1`):** Kāra seq landed at **91.5 ± 1.5 ms** — a 1.50× gap to Rust, with structurally identical evidence to kata 16 pre-Slice-6.1: C trailed Kāra by only 1.06× (both paying indirect-call-per-comparison), Kāra binary was 410.8 KiB (runtime archive's `karac_vec_sort_by` + dependent symbols stayed linked), and the only structural shift from kata 16-post-Slice-6.1 (1.06× of Rust) to kata 56 (1.50× of Rust) was the element-type change from i64 to `(i64, i64)`. Slice 6.1's mono fast path was gated on i64 element type only; this kata explicitly didn't fit. Filed as the natural-pull trigger for Slice 6.4 (tuple/struct elem mono sort) in karac's [`phase-7-codegen.md`](https://github.com/karalang/kara/blob/main/docs/implementation_checklist/phase-7-codegen.md).

**Post-fix (Slice 6.4 of the Vec[T] monomorphization roadmap, karac commit see tracker entry):** karac now accepts integer-tuple and integer-field-struct element types in the `should_use_mono_vec_sort_by_for` gate. The mono emitter is parameterised over `elem_ty`: loads/stores/GEPs use the LLVM struct stride (16 bytes for `(i64, i64)`, 24 for `(i64, i64, i64)`, etc.); the closure body's `.0` / `.1` tuple-index access routes through `compile_expr`'s existing extract path; for named structs the caller plumbs the Kāra type name so `var_type_names` lookups for `.field_name` access work. Closes the kata 56 gap end-to-end. Same architecture as Slice 6.1's i64 path; same A/B-against-the-experiment validation.

**Runtime length dispatch (also Slice 6.4):** call sites now emit BOTH the mono fast path AND a runtime-callback fallback, choosing per-call based on `if len > 64`. Insertion sort is O(N²) so it loses hard above ~N=64; without the dispatch, kata 1665's N=50000 workload would regress from 3.2 ms to 1.1 s. With the dispatch, kata 56 (N=16) takes the mono path each call (62-65 ms total) and kata 1665 (N=50000) takes the runtime path each call (3.8 ms, matching its pre-Slice-6.4 baseline). Cost: the seq binary stays at ~410 KiB instead of collapsing to ~33 KiB the way kata 16's did under Slice 6.1's pure-mono dispatch — both branches at the call site mean `karac_vec_sort_by` stays linked. A future slice can lift this by emitting a smaller typed runtime helper for the large-N path that doesn't drag the full runtime sort surface; for now the wall-time win is the load-bearing result.

### Runtime — auto-par regime

The `sum = sum + r.len()` reduction is auto-par-eligible:

| Implementation | Wall time | User-CPU |
|---|---|---|
| **kāra merge_intervals (auto-par default)** | **10.0 ± 0.9 ms** | 99.7 ms |

The auto-par binary is **6.5× faster than the kāra seq binary** (65.0 → 10.0 ms), spreading the K=1M case-rotation reduction across the perf cores (~10× user-CPU-to-wall ratio on M5 Pro). Both lanes' absolute times dropped post-Slice-6.4 (seq 91.5 → 65.0 ms, auto-par 10.7 → 10.0 ms) — each worker runs the faster mono body — and the ratio compressed because the seq baseline dropped more.

### Runtime — Python

| Run | Mean ± σ |
|---|---|
| `py merge_intervals` (K=100k) | 108.2 ± 0.6 ms |

Python at K=100k is 108 ms; projecting to the compiled mirrors' K=1M (~1.08 s) puts it **~16.6× slower than kāra seq** (was ~11.5× pre-Slice-6.4, widened by Kāra's mono-path speedup). CPython's `sorted(key=lambda x: x[0])` is a C-implemented stable sort with the key extracted in interpreter code per element; the per-iteration overhead is amortized over the heavy per-call sort+sweep work.

### Compile elapsed (cold)

`--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Compiler | Time |
|---|---|
| clang -O3 merge_intervals.c           | **50.3 ± 0.4 ms** |
| **karac build merge_intervals.kara**  | **75.9 ± 0.4 ms** |
| rustc -O merge_intervals.rs           | 129.8 ± 0.7 ms |

Kāra compiles **1.71× faster than `rustc -O`** and sits at **1.51× of clang -O3** — same shape as the rest of the corpus.

### Binary size

| Implementation | Size |
|---|---|
| c    merge_intervals            | 32.8 KiB |
| **kāra merge_intervals (seq)**  | **410.8 KiB** |
| **kāra merge_intervals (auto-par)** | **450.4 KiB** |
| rust merge_intervals            | 473.0 KiB |
| go   merge_intervals            | 2452.2 KiB |

Kāra seq stays at **410.8 KiB** post-Slice-6.4 — the runtime length dispatch (described in § Sort-dispatch history) means the call site emits BOTH the mono fast path AND a `karac_vec_sort_by` fallback for `len > 64`, so the runtime archive's sort surface stays linked. Kata 15/16 post-Slice-6.1 ship at 33.0 KiB because their dispatch path is pure-mono (no fallback needed — i64 sort was the v1 shape and small-N was the design assumption); kata 56's wider-elem dispatch had to carry the fallback because kata 1665's N=50000 workload made the fallback load-bearing. A future slice can lift the size hit by emitting a smaller typed runtime helper for the large-N path that doesn't drag the full runtime sort surface; the wall-time win is the load-bearing result for now.

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
| **karac build merge_intervals.kara** | **10.7 MiB** |
| rustc -O merge_intervals.rs          | 39.4 MiB |

Kāra's compile-memory footprint is ~4.1× clang's and ~3.7× lower than rustc's on this kata — same shape as the rest of the corpus.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio is the codegen-vs-Rust gap. C calibrates the LLVM-backend floor, Go is the cross-runtime data point, and Python is the ergonomic foil. On this kata the **Kāra/Rust 1.06× gap is the load-bearing result** — the kata's first ship at 1.50× was the natural-pull trigger for karac Slice 6.4, which extended Slice 6.1's i64 mono path to integer-tuple and integer-field-struct elements; the post-fix gap is within codegen-quality noise. Kāra now leads C by 1.50× on this kata (was only 1.06× pre-fix) because the qsort indirect-call penalty C carries is no longer offset on the Kāra side. The kata 1665 second witness (sort_by on `(i64, i64)` at N=50000) drove the runtime length dispatch (`if len > 64 { runtime } else { mono }`) — pure-mono insertion sort would have regressed kata 1665 from 3.2 ms to 1.1 s, so the dispatch is the correct safety net.
