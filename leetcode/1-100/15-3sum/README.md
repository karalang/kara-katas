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

- **`Vec.from_slice(Slice[i64])` + in-place `sort_by`** — `three_sum` copies the input into an owned `Vec[i64]` and sorts it with `s.sort_by(|a, b| a.cmp(b))`, the same closure-taking comparator kata [#1665](../../1601-1700/1665-minimum-initial-energy-to-finish-tasks/) uses (here the simpler `i64.cmp` form). Verified to compile and run under both `karac run` and `karac build`.
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

Snapshot — M5 Pro, 2026-05-29, hyperfine `--warmup 5 --runs 30 --shell=none`. All four comparators single-threaded; the kāra row is `KARAC_AUTO_PAR=0`.

| Implementation | Wall time |
|---|---|
| **kāra three_sum (seq)** | **243.3 ± 4.4 ms** |
| rust three_sum           | 246.0 ± 13.0 ms |
| c    three_sum (clang -O3)| 277.7 ± 10.0 ms |
| go   three_sum           | 410.1 ± 20.4 ms |

This is a sort-bound, allocation-heavy workload, and on the seq lane **kāra and Rust are tied** (243.3 vs 246.0 ms — a 1.01× ratio, inside Rust's σ). Both monomorphize the comparator: kāra's `sort_by(|a, b| a.cmp(b))` specializes the comparison into the sort, and Rust's `sort_unstable` does the same. The per-call work is otherwise identical (a length-N copy, the sort, an O(N²) crawl, and a nested-`Vec` output), so the two land on top of each other.

C trails at **1.14×**, and the reason is the sort API rather than codegen quality: the idiomatic C mirror uses `qsort`, whose comparator is an indirect function-pointer call *per comparison* — exactly the call kāra and Rust inline away. A hand-rolled inlined C sort would close the gap, but `qsort` is what a C programmer reaches for, so it's the fair baseline. Go trails further at **1.69×**: `sort.Slice` also pays a per-comparison closure indirect-call, and the `[][]int64` triplet output adds GC pressure the manual-free mirrors don't carry.

### Runtime — auto-par regime

The `sum = sum + r.len()` reduction is auto-par-eligible; the default `karac build` recognizes it and emits a `karac_par_reduce` dispatch. NOT comparable to the single-thread rows above (BENCH.md two-lane discipline) — reported separately so the production-default Kāra behavior stays visible:

| Implementation | Wall time | User-CPU |
|---|---|---|
| **kāra three_sum (auto-par default)** | **33.9 ± 3.3 ms** | 380.5 ms |

The auto-par binary is **7.2× faster than the kāra seq binary** (243.3 → 33.9 ms), spreading the K=1M case-rotation reduction across the perf cores (~11× user-CPU-to-wall ratio on M5 Pro). This is the legitimate-win case (BENCH.md kata #4 path): a real wall-time speedup at the cost of the `karac_par_reduce` machinery's +17 KiB binary and +1.8 MiB peak RSS. The per-worker allocator contention of the nested-`Vec` output caps the speedup below this kata's ~11-core CPU spread — a sort+allocate body parallelizes less cleanly than a pure arithmetic reduction, but the win is still substantial.

### Runtime — Python

| Run | Mean ± σ |
|---|---|
| `py three_sum` (K=100k) | 280.9 ± 1.3 ms |

Python at K=100k is 281 ms; projecting to the compiled mirrors' K=1M (~2.81 s) puts it **~11.5× slower than kāra seq**. That gap is narrower than the corpus norm (kata 14 sits at ~37×) because the hot path here is dominated by `sorted()` — a C-implemented builtin — so CPython spends most of its time in the same kind of native sort the compiled mirrors run, and the per-iteration interpreter overhead is amortized over heavier per-call work. Against the auto-par regime the cross-lane ratio is ~83×.

### Compile elapsed (cold)

`--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Compiler | Time |
|---|---|
| clang -O3 three_sum.c           | **54.6 ± 0.6 ms** |
| **karac build three_sum.kara**  | **74.5 ± 0.9 ms** |
| rustc -O three_sum.rs           | 132.5 ± 0.7 ms |

Kāra compiles **1.78× faster than `rustc -O`** and sits at **1.36× of clang -O3** — same shape as the rest of the corpus.

### Binary size

| Implementation | Size |
|---|---|
| c    three_sum            | 32.8 KiB |
| **kāra three_sum (seq)**  | **359.4 KiB** |
| **kāra three_sum (auto-par)** | **376.6 KiB** |
| rust three_sum            | 472.8 KiB |
| go   three_sum            | 2452.2 KiB |

The seq binary is markedly heavier than allocation-light katas (kata 14's seq is 81.5 KiB) because `sort_by` pulls in the generic comparison-sort machinery + closure trampoline, and `Vec.from_slice` / `Vec[Vec[i64]]` add nested-`Vec` runtime surface. That same surface is why the auto-par delta is only **+17 KiB** here (vs the +280 KiB kata 14 pays): the seq binary already carries most of what the reduction dispatch needs, so `karac_par_reduce` lands on top of an already-large image. Kāra still ships well under Rust's 472.8 KiB on both rows.

### Runtime memory (peak)

| Implementation | Peak |
|---|---|
| c    three_sum            | 1.2 MiB |
| **kāra three_sum (seq)**  | **1.2 MiB** |
| rust three_sum            | 1.2 MiB |
| **kāra three_sum (auto-par)** | **3.0 MiB** |
| go   three_sum            | 9.7 MiB |

Kāra seq's peak RSS is byte-for-byte identical to Rust's (1,294,672 B) and within 50 KiB of C — the per-iter `Vec[Vec[i64]]` is allocated and freed inside `three_sum`, so steady state stays flat across the K=1M loop. The auto-par regime's 3.0 MiB is the worker pool's per-thread scratch + partials. Go's 9.7 MiB carries its GC roots + scheduler arena.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 three_sum.c          | 2.6 MiB |
| **karac build three_sum.kara** | **10.8 MiB** |
| rustc -O three_sum.rs          | 38.1 MiB |

Kāra's compile-memory footprint is ~4.1× clang's and ~3.5× lower than rustc's on this kata.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio is the codegen-vs-Rust gap. C calibrates the LLVM-backend floor, Go is the cross-runtime data point, and Python is the ergonomic foil. On this sort-bound kata the Kāra/Rust tie is the load-bearing result — two monomorphizing compilers landing on the same wall time on a workload where the comparator-dispatch strategy is what separates the field.
