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
- **Scalar `+` reduction in the bench** — `sum = sum + r.len()` is the slice-1 auto-par-on-reduction allow-list shape recognized by default in `karac build` and lowered to an M4 task-runtime dispatch (`karac_mir_task_spawn`; `karac_par_reduce` before the v2 backend).

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

Same M=8/N=16/K=1M shape as katas [#15](../15-3sum/) and [#16](../16-3sum-closest/), so cross-kata wall-time comparisons stay meaningful. The key difference: this kata sorts a **tuple-typed Vec**, not a `Vec[i64]`. Kata 15/16's `sort_by(|a, b| a.cmp(b))` on `Vec[i64]` hits karac's Slice 6.1 mono fast path (per-call-site `__vec_i64_sort_by_mono_<id>` emitted into the user binary); this kata's `sort_by(|a, b| a.0.cmp(b.0))` on `Vec[(i64, i64)]` originally did NOT — the mono gate was i64-elem-only in v1, which is the story § Sort-dispatch history tells. Post-Slice-6.4 the gate accepts integer tuples, so at N=16 every call takes the mono fast path; the `len > 64` runtime fallback now resolves to the lean non-panicking sort entry, so on the legacy backend the seq binary collapsed to the no-sort floor (under v2/MIR it is 295.8 KiB — see § Binary size).

Two-lane kata (BENCH.md § Implicit auto-par): the `sum = sum + r.len()` accumulator is the slice-1 allow-list reduction shape, so `karac build` parallelises it by default — the default build carries two calls of `karac_mir_task_spawn` and the `KARAC_AUTO_PAR=0` twin none (verified in the emitted IR, `KARAC_MIR_LL`). The bench builds two kara binaries — `KARAC_AUTO_PAR=0` for the within-lane seq comparison, default for the auto-par regime — and reports them in separate tables per the two-lane discipline.

### Runtime — seq lane

M5 Pro, measured 2026-10-31 with karac `g6697158fa` (the v2/MIR backend; [`bench/results.json`](bench/results.json) `measured_at` 2026-11-01T02:17Z UTC), hyperfine `--warmup 5 --runs 30 --shell=none`. All comparators single-threaded; the kāra row is `KARAC_AUTO_PAR=0`.

| Implementation | Wall time |
|---|---|
| rust merge_intervals                  | **75.1 ± 1.3 ms** |
| rust merge_intervals (`overflow-checks=on`) | 75.9 ± 2.2 ms |
| **kāra merge_intervals (seq)**        | **102.9 ± 3.1 ms** |
| c    merge_intervals (clang -O3)      | 111.8 ± 2.3 ms |
| go   merge_intervals                  | 462.7 ± 10.9 ms |

Rust leads by **1.37×** over Kāra seq (checked Rust costs it only 1.01×, so the gap is not overflow checking). **Kāra still leads C, by 1.09×** — the qsort indirect-call penalty C carries on every comparison — and **Go trails Kāra by 4.49×**: `sort.Slice` still pays the per-compare closure indirect-call, and the `[]Interval` allocator has GC behind it that the manual-free mirrors don't carry (Go's 462.7 ms wall is 509.7 ms of CPU, 459.4 user + 50.4 system).

Against the July legacy-backend feed the language ratios moved Kāra/Rust 1.05× → 1.37×, Kāra/C 0.73× → 0.92×, Kāra/Go 0.19× → 0.22×; that slowdown happened inside the legacy era, not in the MIR switch — the v2/MIR build runs 0.76× the instructions and 0.81× the cycles of the last legacy build (`dd86e3955`). The June snapshot's "1.06× behind Rust, 1.52× ahead of C" (Rust 60.4 / Kāra 64.1 / C 97.3 / Go 403.4 ms) no longer holds.

#### Sort-dispatch history (kata 56 → karac Slice 6.4)

**Pre-fix (kata 56 ship 2026-05-29, commit `558edc1`):** Kāra seq landed at **91.5 ± 1.5 ms** — a 1.50× gap to Rust, with structurally identical evidence to kata 16 pre-Slice-6.1: C trailed Kāra by only 1.06× (both paying indirect-call-per-comparison), Kāra binary was 410.8 KiB as then measured (runtime archive's `karac_vec_sort_by` + dependent symbols stayed linked; ~116 KiB of that reading was transient archive contamination — see § Binary size), and the only structural shift from kata 16-post-Slice-6.1 (1.06× of Rust) to kata 56 (1.50× of Rust) was the element-type change from i64 to `(i64, i64)`. Slice 6.1's mono fast path was gated on i64 element type only; this kata explicitly didn't fit. Filed as the natural-pull trigger for Slice 6.4 (tuple/struct elem mono sort) in karac's [`phase-7-codegen.md`](https://github.com/karalang/kara/blob/main/docs/implementation_checklist/phase-7-codegen.md).

**Post-fix (Slice 6.4 of the Vec[T] monomorphization roadmap, karac commit see tracker entry):** karac now accepts integer-tuple and integer-field-struct element types in the `should_use_mono_vec_sort_by_for` gate. The mono emitter is parameterised over `elem_ty`: loads/stores/GEPs use the LLVM struct stride (16 bytes for `(i64, i64)`, 24 for `(i64, i64, i64)`, etc.); the closure body's `.0` / `.1` tuple-index access routes through `compile_expr`'s existing extract path; for named structs the caller plumbs the Kāra type name so `var_type_names` lookups for `.field_name` access work. Closes the kata 56 gap end-to-end. Same architecture as Slice 6.1's i64 path; same A/B-against-the-experiment validation.

**Runtime length dispatch (also Slice 6.4):** call sites now emit BOTH the mono fast path AND a runtime-callback fallback, choosing per-call based on `if len > 64`. Insertion sort is O(N²) so it loses hard above ~N=64; without the dispatch, kata 1665's N=50000 workload would regress from 3.2 ms to 1.1 s. With the dispatch, kata 56 (N=16) takes the mono path each call (~64 ms total) and kata 1665 (N=50000) takes the runtime path each call (3.8 ms, matching its pre-Slice-6.4 baseline). With the lean non-panicking large-N sort entry now landed, the seq binary collapses to ~33 KiB the way kata 16's did under Slice 6.1's *pure-mono* dispatch — the runtime fallback no longer drags `karac_vec_sort_by`'s `slice::sort_by` → libstd panic/backtrace machinery (~262 KiB) into the link, so `-dead_strip` carves it away. (The ~410 KiB figures earlier snapshots quoted included a further ~116 KiB of transient archive contamination — see § Binary size.) This applies to *every* dual-path sort call site: kata 15/16/18 seq binaries collapse to the same ~33 KiB floor today.

*Note (31 Oct 2026):* the ~33 KiB floor above is a legacy-backend result; every v2/MIR Kāra binary is ~300–390 KB (kara ledger [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md)), and this kata's seq binary is 295.8 KiB.

### Runtime — auto-par regime

The `sum = sum + r.len()` reduction is auto-par-eligible. Same run, hyperfine `--runs 50`; each comparator is its own explicit-parallel mirror:

| Implementation | Wall time | User-CPU |
|---|---|---|
| c    merge_intervals (pthreads — metal floor) | **8.9 ± 1.5 ms** | 94.5 ms |
| rust merge_intervals (rayon `par_iter`) | 16.7 ± 2.9 ms | 233.3 ms |
| **kāra merge_intervals (auto-par default)** | **19.5 ± 2.8 ms** | 211.8 ms |
| go   merge_intervals (goroutines + WaitGroup) | 181.9 ± 3.3 ms | 855.7 ms (+ 372.5 ms system) |

Kāra's implicit auto-par lands **1.17× behind rayon** (about one σ apart; both rows carry σ ≈ 2.8–2.9 ms), **2.18× behind the hand-written pthreads floor**, and **9.35× ahead of Go**, with less user-CPU than rayon (211.8 vs 233.3 ms). The auto-par binary is **5.29× faster than the kāra seq binary** (102.9 → 19.5 ms), spreading the K=1M case-rotation reduction across the cores (~11× user-CPU-to-wall ratio on M5 Pro). Against the July legacy-backend feed the par lane improved against C and Go — Kāra/C 3.20× → 2.18×, Kāra/Go 0.15× → 0.11× — and is flat against rayon (1.25× → 1.17×).

### Runtime — Python

| Run | Mean ± σ |
|---|---|
| `py merge_intervals` (K=100k) | 103.5 ± 0.6 ms (last measured 2026-06-05, not re-run) |

Python at K=100k was 104 ms in that run; projecting to the compiled mirrors' K=1M (~1.04 s) put it **~16.1× slower than that run's kāra seq** (was ~11.5× pre-Slice-6.4, widened by Kāra's mono-path speedup); against this run's kāra seq (102.9 ms) the same projection is ~10×, across sessions. CPython's `sorted(key=lambda x: x[0])` is a C-implemented stable sort with the key extracted in interpreter code per element; the per-iteration overhead is amortized over the heavy per-call sort+sweep work.

### Compile elapsed (cold)

Same run, `--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Compiler | Time |
|---|---|
| clang -O3 merge_intervals.c           | **57.1 ± 0.6 ms** |
| rustc -O merge_intervals.rs           | 142.4 ± 3.5 ms |
| **karac build merge_intervals.kara**  | **215.0 ± 4.7 ms** |

Kāra now compiles **1.51× slower than `rustc -O`** and sits at **3.77× of clang -O3** (in June it compiled 1.63× faster than rustc).

### Binary size

| Implementation | Size |
|---|---|
| c    merge_intervals (seq / pthreads par) | 32.8 / 33.1 KiB |
| **kāra merge_intervals (seq)**  | **295.8 KiB** |
| **kāra merge_intervals (auto-par)** | **393.2 KiB** |
| rust merge_intervals (seq / rayon par) | 473.0 / 454.9 KiB |
| go   merge_intervals (seq / par) | 2452.2 / 2452.8 KiB |

> **Correction (2026-06-05).** Earlier snapshots quoted kāra seq at 410.8 KiB and auto-par at 450.4 KiB. Those binaries were linked against a transiently contaminated runtime archive (an `rlib`+`staticlib` dual-emission build that defeated cross-module DCE — see [kata 15 § Binary size](../15-3sum/README.md) for the full breakdown). Rebuilt against the clean archive: **seq 420,608 → 301,792 B (−118,816 B)** — the same recovery delta as katas 15/16/18 — and **par 461,200 → 319,520 B (−141,680 B)**, landing both at the corpus-standard sort-kata sizes (15/16 seq 294.8, par 312.0 KiB).

Binary size: every v2/MIR Kāra binary is ~300–390 KB where legacy's were ~34 KB (tracked as kara ledger [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md)). Kāra seq is **295.8 KiB** (legacy's 33.5 KiB no-sort floor, described above, no longer applies), 1.60× under Rust's 473.0 KiB and 9.0× over C's 32.8 KiB. The auto-par binary carries the worker-pool dispatch + scheduler surface on top, landing at **393.2 KiB** — +97.5 KiB over seq.

### Runtime memory (peak)

| Implementation | Peak |
|---|---|
| c    merge_intervals (seq / pthreads par) | 1.0 / 1.4 MiB |
| **kāra merge_intervals (seq)**  | **1.1 MiB** |
| rust merge_intervals (seq / rayon par) | 1.1 / 2.5 MiB |
| **kāra merge_intervals (auto-par)** | **2.0 MiB** |
| go   merge_intervals (seq / par) | 9.4 / 13.5 MiB |

Kāra seq's peak RSS ties Rust and sits a few pages over C (single-shot `/usr/bin/time -l` readings are page-level noisy) — the per-iter `Vec[(i64, i64)]` output is allocated and freed inside `merge_intervals` so steady state stays flat across K=1M. The auto-par regime's 2.0 MiB is the worker pool's per-thread scratch + partials, under rayon's 2.5 MiB.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 merge_intervals.c          | 2.6 MiB |
| rustc -O merge_intervals.rs          | 39.3 MiB |
| **karac build merge_intervals.kara** | **59.3 MiB** |

Kāra's compile-memory footprint is ~23× clang's and 1.51× rustc's on this kata (in June it was 13.9 MiB, ~2.8× under rustc).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio is the codegen-vs-Rust gap. C calibrates the LLVM-backend floor, Go is the cross-runtime data point, and Python is the ergonomic foil. On this kata the **Kāra/Rust gap is the load-bearing result** — the kata's first ship at 1.50× was the natural-pull trigger for karac Slice 6.4, which extended Slice 6.1's i64 mono path to integer-tuple and integer-field-struct elements and brought the gap to 1.06× (June 2026, legacy backend). On the 2026-10-31 v2/MIR re-bench it is 1.37× (§ Runtime — seq lane). Kāra still leads C, by 1.09× (1.52× in June, 1.06× pre-fix), because the qsort indirect-call penalty C carries is no longer offset on the Kāra side. The kata 1665 second witness (sort_by on `(i64, i64)` at N=50000) drove the runtime length dispatch (`if len > 64 { runtime } else { mono }`) — pure-mono insertion sort would have regressed kata 1665 from 3.2 ms to 1.1 s, so the dispatch is the correct safety net.
