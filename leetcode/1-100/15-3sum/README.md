# 15. 3Sum

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array, Two Pointers, Sorting &nbsp;·&nbsp; **Source:** [leetcode.com/problems/3sum](https://leetcode.com/problems/3sum/)

Given an integer array `nums`, return all distinct triplets `[nums[i], nums[j], nums[k]]` (with `i`, `j`, `k` pairwise distinct) such that `nums[i] + nums[j] + nums[k] == 0`. The result must not contain duplicate triplets.

```
([-1, 0, 1, 2, -1, -4])  → [[-1, -1, 2], [-1, 0, 1]]
([0, 1, 1])              → []        (no zero-sum triplet)
([0, 0, 0])              → [[0, 0, 0]]
```

**Constraints:** `3 ≤ nums.length ≤ 3000`, `-10^5 ≤ nums[i] ≤ 10^5`.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| Sort, then fix `s[i]` and two-pointer the suffix for `-s[i]` | O(n²) time, O(1) extra (+ output) | [`three_sum.kara`](three_sum.kara) ✓ via `karac run` / `karac build` | [`three_sum.py`](three_sum.py) ✓ |

`✓` runs end-to-end today. Interpreter and codegen produce identical output to the Python mirror across all nine test cases.

## Why sort + two-pointer?

Brute force is O(n³) — every `(i, j, k)`. Sorting the array first unlocks an O(n²) shape: fix the smallest element `s[i]`, then collapse the search for the remaining pair into a single linear crawl over the sorted suffix `s[i+1 .. n)`:

```
sum < 0  ⇒  low value too small  → advance lo
sum > 0  ⇒  high value too big   → retreat hi
sum == 0 ⇒  record triplet, then step both inward
```

The sort costs O(n log n) but is dominated by the O(n²) pair search, so the whole algorithm is O(n²). Sorting earns its keep twice: it makes the pair search a two-pointer crawl (same dominance argument as kata [#11](../11-container-with-most-water/)), **and** it makes duplicate-suppression a cheap adjacent-value check instead of a `HashSet` of seen triplets:

- **Outer dedup:** if `s[i] == s[i-1]`, every triplet whose smallest element is this value was already enumerated on the previous `i` — skip it.
- **Inner dedup:** after recording a hit, walk `lo` forward past any repeat of the value just consumed and `hi` backward likewise, so the next pair uses fresh values.

The `s[i] > 0` early-out closes the loop: once the smallest of the three is positive, the (sorted) suffix is all `≥ s[i] > 0` and the sum can never return to zero.

## Kāra features exercised

- **`Vec.from_slice(Slice[i64])` + in-place `sort_by`** — `three_sum` copies the input into an owned `Vec[i64]` and sorts it with `s.sort_by(|a, b| a.cmp(b))`, the same closure-taking comparator kata [#1665](../../1601-1700/1665-minimum-initial-energy-to-finish-tasks/) uses (here the simpler `i64.cmp` form). As of karac Slice 6.1, this exact pattern (Vec[i64].sort_by + inline-closure comparator + no captures) routes through the monomorphized fast path — see § Runtime — seq lane for the bench impact. Verified to compile and run under both `karac run` and `karac build`.
- **`Vec[Vec[i64]]` construction + return** — each triplet is a fresh `Vec[i64]` (`t.push(...)` ×3) pushed onto the result `Vec[Vec[i64]]`; the whole nested structure is returned by value, the same owned-nested-`Vec` shape kata [#14](../14-longest-common-prefix/)'s bench builds.
- **Two-pointer crawl with `lo`/`hi` cursors** — the inner loop indexes `s[lo]` / `s[hi]` directly and advances the side that moves the sum toward zero, the same index-as-cursor pattern as kata [#11](../11-container-with-most-water/) and kata [#88](../88-merge-sorted-array/).
- **`and` short-circuit in the dedup guards** — `while lo < hi and s[lo] == s[lo - 1i64]` leans on `and`'s short-circuit: when `lo == hi` the loop bound is `false` and the `s[lo - 1]` read behind it never runs out of bounds.
- **`continue` / `break` in `while`** — the outer dedup `continue`s past a repeated smallest value and `break`s on the `s[i] > 0` early-out.
- **`Vec[i64].len()` reduction in the bench** — `sum = sum + r.len()` is the slice-1 auto-par-on-reduction allow-list shape (associative + commutative `+`), recognized by default in `karac build` and lowered to a `karac_par_reduce` dispatch.

## Running

```bash
# Kāra — interpreter and codegen produce the same output today.
karac run   three_sum.kara
karac build three_sum.kara && ./three_sum

# Python
python3 three_sum.py

# Verify they agree
diff <(./three_sum) <(python3 three_sum.py) && echo OK
diff <(karac run three_sum.kara) <(python3 three_sum.py) && echo OK
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`three_sum.{kara,rs,c,py}`, `go-seq/main.go`).

**Workload.** M = 8 distinct test cases, each a `Vec[i64]` of N = 16 values drawn from a deterministic 31-bit LCG into the range `[-10, 10]`, built once into a `Vec[Vec[i64]]` before the timed loop. K = 1,000,000 outer iterations rotate `idx = k % M` and call `three_sum` on that case, so the call is never loop-invariant (LLVM can't hoist it) and the eight distinct inputs keep the branch predictor from fully learning any single sort/two-pointer pattern. Each call does a `Vec.from_slice` copy, an O(N log N) sort, an O(N²) two-pointer scan, and allocates a `Vec[Vec[i64]]` of however many zero-sum triplets the case holds (each triplet a 3-element `Vec[i64]`). Across the eight cases there are 71 triplets, so the sink — the running total of every returned `Vec`'s `.len()` — is `(K / M) × 71` = `125000 × 71` = **8,875,000**; all five mirrors must agree before any timing begins. The LCG stays inside i64 with no wraparound (`1103515245 × state` never exceeds ~2.37×10¹⁸ < i64::MAX), so every mirror reproduces the same stream and the same triplet counts.

This leans harder on the allocator than kata 13 / 14 (nested `Vec[Vec[i64]]` output freed at end-of-iter scope) and harder on the *sort* than any prior corpus kata — which is what makes the seq-lane comparison below interesting.

Two-lane kata (BENCH.md § Implicit auto-par): the `sum = sum + r.len()` accumulator is the slice-1 allow-list reduction shape, so `karac build` may emit a `karac_par_reduce` dispatch by default. The bench builds two kara binaries — `KARAC_AUTO_PAR=0` for the within-lane seq comparison, default for the auto-par regime — and reports them in separate tables per the two-lane discipline.

### Runtime — seq lane

Snapshot — M5 Pro, 2026-05-30, hyperfine `--warmup 5 --runs 30 --shell=none`. All four comparators single-threaded; the kāra row is `KARAC_AUTO_PAR=0`. Numbers below are with the karac Slice 6.1 mono fast path for `Vec[i64].sort_by` landed (the kata 15 / 16 idiom — surfaced by [kata 16](../16-3sum-closest/) and shipped together).

| Implementation | Wall time |
|---|---|
| **kāra three_sum (seq)** | **210.7 ± 5.3 ms** |
| rust three_sum           | 234.3 ± 5.6 ms |
| c    three_sum (clang -O3)| 266.2 ± 5.4 ms |
| go   three_sum           | 380.3 ± 8.9 ms |

This is a sort-bound, allocation-heavy workload, and on the seq lane **Kāra leads Rust by 1.11×** (210.7 vs 234.3 ms). Pre-Slice-6.1 the two were tied at ~244 ms because Kāra's faster small-Vec alloc path was offsetting Rust's monomorphized-sort win; with Kāra now monomorphizing the sort too, both compilers monomorphize the comparator, both ship a fully-inlined insertion sort vs ipnsort, and Kāra's allocator edge stops being offset, so it inches ahead. **C now trails Kāra by 1.26×** (266.2 vs 210.7 ms) and lands slowest of the three static-compiled mirrors: `qsort`'s indirect comparator call lands per comparison — the same runtime-callback shape Kāra carried pre-Slice-6.1 — and there's no way to eliminate it without giving up the standard-library sort. (At kata 15's first ship Rust and C tied at 262.5 ms; on this re-bench Rust's sort pulls it clear of C while Kāra's mono sort + allocator edge keeps it ahead of both.) Go trails at **1.81×**: `sort.Slice` also pays a per-comparison closure indirect-call, and the `[][]int64` triplet output adds GC pressure the manual-free mirrors don't carry.

This kata's tie-with-Rust history (and the pre-mono numbers) is the comparison point [kata 16](../16-3sum-closest/)'s Slice 6.1 trigger story relies on — kata 15's tie was the natural-occurring evidence that *something* was holding Kāra back on sort_by-heavy workloads; kata 16 removed the allocation-dominance offset and exposed it as a sort-dispatch gap; Slice 6.1 closed both.

### Runtime — auto-par regime

The `sum = sum + r.len()` reduction is auto-par-eligible; the default `karac build` recognizes it and emits a `karac_par_reduce` dispatch. NOT comparable to the single-thread rows above (BENCH.md two-lane discipline) — reported separately so the production-default Kāra behavior stays visible:

| Implementation | Wall time | User-CPU |
|---|---|---|
| **kāra three_sum (auto-par default)** | **27.7 ± 1.8 ms** | 381.1 ms |

The auto-par binary is **7.6× faster than the kāra seq binary** (210.7 → 27.7 ms), spreading the K=1M case-rotation reduction across the perf cores (~13.8× user-CPU-to-wall ratio on M5 Pro). This is the legitimate-win case (BENCH.md kata #4 path): a real wall-time speedup at the cost of the `karac_par_reduce` machinery's **+40 KiB binary** over the seq lane (see § Binary size — both lanes now carry the sort runtime, so the par-reduce surface is a small marginal add) and +1.8 MiB peak RSS. The per-worker allocator contention of the nested-`Vec` output still caps the speedup below the perf-core count — a sort+allocate body parallelizes less cleanly than a pure arithmetic reduction, but the win is still substantial.

### Runtime — Python

| Run | Mean ± σ |
|---|---|
| `py three_sum` (K=100k) | 273.7 ± 1.0 ms |

Python at K=100k is 274 ms; projecting to the compiled mirrors' K=1M (~2.74 s) puts it **~13.0× slower than kāra seq**. That gap is narrower than the corpus norm (kata 14 sits at ~37×) because the hot path here is dominated by `sorted()` — a C-implemented builtin — so CPython spends most of its time in the same kind of native sort the compiled mirrors run, and the per-iteration interpreter overhead is amortized over heavier per-call work. The nested-`Vec` output here means the per-iter allocator cost dominates on the Kāra side too, so the Slice 6.1 mono sort moved Kāra's wall time less than it moved kata 16's (kata 16 dropped 34 ms; kata 15 dropped 14 ms). Against the auto-par regime the cross-lane ratio is ~99×.

### Compile elapsed (cold)

`--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Compiler | Time |
|---|---|
| clang -O3 three_sum.c           | **52.5 ± 0.5 ms** |
| **karac build three_sum.kara**  | **76.6 ± 1.4 ms** |
| rustc -O three_sum.rs           | 126.7 ± 1.1 ms |

Kāra compiles **1.65× faster than `rustc -O`** and sits at **1.46× of clang -O3** — same shape as the rest of the corpus.

### Binary size

| Implementation | Size |
|---|---|
| c    three_sum            | 32.8 KiB |
| **kāra three_sum (seq)**  | **410.8 KiB** |
| **kāra three_sum (auto-par)** | **450.8 KiB** |
| rust three_sum            | 472.8 KiB |
| go   three_sum            | 2452.2 KiB |

**Correction (2026-05-30 re-bench).** An earlier snapshot of this section reported the seq binary at 33.0 KiB, on the reasoning that the Slice 6.1 mono fast path lets `karac_vec_sort_by` and its transitive runtime surface get DCE'd. The current seq binary is **410.8 KiB**. This is **an expected consequence of a separate fix, not a DCE failure**: a later toolchain change gave the sort runtime's ordering-violation panic a *symbolized* backtrace, so any program that reaches `s.sort_by(...)` now links the DWARF symbolizer (`gimli` + `addr2line` + `object` + `rustc_demangle`), ~260 KiB of `__text`. A minimal Kāra program with no `sort_by` still builds to **32.7 KiB with none of that surface** — so the cost is the sort-panic symbolizer specifically, confirmed identical on kata [#16](../16-3sum-closest/) which returns a *scalar* (no nested `Vec`) yet also lands at 410.8 KiB. Kata 16's § Binary size has the full disassembly breakdown and the no-sort control. The *runtime* half of the Slice 6.1 win is intact — the seq lane still leads Rust (see § Runtime — seq lane). The auto-par row adds only **+40 KiB** over seq for the `karac_par_reduce` + worker-pool surface, since the seq binary already carries the symbolizer that dominates the image. Kāra still ships under Rust's 472.8 KiB on both rows; C's 32.8 KiB (no runtime archive, no symbolized panics) is the floor.

### Runtime memory (peak)

| Implementation | Peak |
|---|---|
| c    three_sum            | 1.2 MiB |
| **kāra three_sum (seq)**  | **1.2 MiB** |
| rust three_sum            | 1.3 MiB |
| **kāra three_sum (auto-par)** | **3.0 MiB** |
| go   three_sum            | 9.3 MiB |

Kāra seq's peak RSS (1,278,288 B) sits between C (1,261,904 B) and Rust (1,311,056 B), within ~50 KiB of both — the per-iter `Vec[Vec[i64]]` is allocated and freed inside `three_sum`, so steady state stays flat across the K=1M loop. The auto-par regime's 3.0 MiB is the worker pool's per-thread scratch + partials. Go's 9.3 MiB carries its GC roots + scheduler arena.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 three_sum.c          | 2.6 MiB |
| **karac build three_sum.kara** | **11.1 MiB** |
| rustc -O three_sum.rs          | 38.3 MiB |

Kāra's compile-memory footprint is ~4.3× clang's and ~3.5× lower than rustc's on this kata.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio is the codegen-vs-Rust gap. C calibrates the LLVM-backend floor, Go is the cross-runtime data point, and Python is the ergonomic foil. On this sort-bound kata **Kāra leads Rust by 1.11×** — pre-Slice-6.1 the two were tied because Kāra's runtime-callback sort dispatch (which kata 16 surfaced as the residual gap) was offsetting Kāra's allocator edge. With both compilers monomorphizing the comparator post-Slice-6.1, the allocator edge stops being offset and Kāra inches ahead. The full story — how the tie here pointed at the kata-16 trigger event — is in [kata 16's README § Sort-dispatch history](../16-3sum-closest/README.md).
