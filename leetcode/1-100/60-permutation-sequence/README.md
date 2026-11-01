# 60. Permutation Sequence

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** Math, Recursion &nbsp;·&nbsp; **Source:** [leetcode.com/problems/permutation-sequence](https://leetcode.com/problems/permutation-sequence/)

The set `{1, 2, …, n}` has `n!` distinct permutations. Listed in lexicographic order and labelled `1 … n!`, return the **k-th** permutation sequence as a string.

```
n = 3  →  "123", "132", "213", "231", "312", "321"
                              ↑ k = 3  →  "213"

n = 4, k = 9   →  "2314"
n = 3, k = 1   →  "123"
```

**Constraints:** `1 ≤ n ≤ 9`, `1 ≤ k ≤ n!` (so `k ≤ 9! = 362880`, well inside i64).

This is the **closed-form dual of [kata #31](../31-next-permutation/)**: #31 steps *one* permutation forward in place; here we jump straight to the k-th without walking the `k-1` in between.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| **Factorial number system** — fix each digit by the block `(k-1) / (n-1-pos)!` it falls into, then recurse on the remainder | O(n²) time (pick-and-shift), O(n) space | [`permutation_sequence.kara`](permutation_sequence.kara) ✓ via `karac run` / `karac build` | [`permutation_sequence.py`](permutation_sequence.py) ✓ |
| **next_permutation iteration** — start from `1…n`, step forward `k-1` times (kata #31's four-move scan) | O(k·n) time, O(n) space | [`permutation_sequence_nextperm.kara`](permutation_sequence_nextperm.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter and codegen produce identical output, the two solvers agree with each other, and the factorial solver agrees with the Python mirror across all seven cases (`n = 1…9`, including both extreme ranks `k = 1` and `k = n!`).

## Why two solvers?

**Factorial number system** ([`permutation_sequence.kara`](permutation_sequence.kara)) is the O(n²) closed form. The insight: sorted lexicographically, the `n!` permutations split into `n` contiguous blocks by their **first** element, each block holding exactly `(n-1)!` permutations. So the leading digit is fixed by which block the rank lands in — `idx = (k-1) / (n-1)!` — and the remainder `(k-1) % (n-1)!` re-poses the identical problem on the `n-1` digits left over. Working 0-indexed (`kk = k - 1`), at position `pos` the block size is `(n-1-pos)!`; `idx = kk / block` selects the digit to emit from the still-available pool and `kk = kk % block` descends into that block. The available digits live in a sorted `Vec[i64]` of `1…n`, and `digits.remove(idx)` pulls the chosen one out while shifting the tail down — the O(n) shift per step is the whole cost, giving O(n²).

**next_permutation iteration** ([`permutation_sequence_nextperm.kara`](permutation_sequence_nextperm.kara)) is the brute-but-honest dual: start from the first permutation `1,2,…,n` and step forward one lexicographic permutation at a time, `k-1` times, landing on the k-th. The step is [kata #31](../31-next-permutation/)'s four-move scan verbatim — pivot → successor → swap → reverse-suffix — here over a `mut ref Vec[i64]` so it mutates the caller's array in place. No wrap branch is needed: `k ≤ n!` guarantees we never step past the last permutation, so the pivot always exists. It is O(k·n) — up to `9! · 9 ≈ 3.3M` primitive ops at the bound, still instant, but asymptotically worse than the factorial form. It earns its place by exercising the exact #31 step and showing the incremental counterpart of the closed form.

## Kāra features exercised

- **`Vec[i64].remove(idx) -> i64` — index removal with tail-shift** (factorial) — `digits.remove(idx)` pulls the selected digit out of the pool and shifts the remainder down, returning the removed value. This is the delicate index-removal path on both surfaces (interpreter `method_call_seq.rs` and codegen `vec_method.rs` load + memmove + `len--`); the pool stays sorted for the next pick and both surfaces agree byte-for-byte.
- **`mut ref Vec[i64]` parameter mutated in place** (nextperm) — `fn next_permutation(a: mut ref Vec[i64], len)` swaps and reverses through the borrowed vector; the call site writes `mut a` (the `ref` is implied by the callee's signature), the same in-place-mutation shape as kata #37's `board: mut ref Vec[Vec[i64]]`.
- **Factorial table built by data-dependent `push`** — `fact[i] = fact[i-1] * i` folded into a growing `Vec[i64]`, then indexed as `fact[n - 1 - pos]` — a read whose index depends on the loop position, not a constant.
- **f-string accumulation into a `String`** — `result = f"{result}{digit}"` appends each emitted digit, the same accumulator pattern the corpus uses to build diffable output lines.
- **`for x in a.iter()` over `Vec[i64]`** (nextperm) — iterate the final array to render it, versus the factorial solver which builds the string as it picks.

## Running

```bash
# Kāra — interpreter and codegen produce the same output today.
karac run   permutation_sequence.kara
karac build permutation_sequence.kara && ./permutation_sequence

# The next_permutation approach (identical output):
karac run permutation_sequence_nextperm.kara

# Python
python3 permutation_sequence.py

# Verify they all agree
diff <(karac run permutation_sequence.kara) <(python3 permutation_sequence.py)                    && echo OK
diff <(karac run permutation_sequence.kara) <(karac run permutation_sequence_nextperm.kara)       && echo OK

# Full cross-language benchmark (both solvers × Kāra / Rust / C / Go / Python + auto-par lanes)
bench/bench.sh
```

## Benchmarks

Unusually, this kata benchmarks **both solvers** — the O(n²) factorial closed form *and* the O(k·n) `next_permutation` walk — each across Kāra, Rust, C, Go, and Python, in a seq lane and an auto-par lane. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`permutation_sequence{,_nextperm}.{kara,rs,c,py}`, `go-seq{,-np}/main.go`, `rayon{,-np}/`).

**Workload.** M = 9 rotated `(n, k)` cases (`n ∈ {6…9}`, `k` from small up to `n!`), selected by `idx = k % M`. Each iteration builds the k-th permutation of `1…n` into a fresh integer buffer and folds a **position-weighted checksum** `Σ perm[i]·(i+1)` over its digits into the running total. Two traps this avoids, both familiar from the interval/spiral katas:

- **Rotating `(n, k)` defeats loop-invariant code motion.** A fixed `(n, k)` makes `get_permutation` a hoistable invariant; rotating over 9 cases forces real work every iteration.
- **The checksum reads *every* output digit**, so no mirror can dead-code the digit picks.

**The two solvers run different K.** The factorial form is O(n²) and independent of `k`; the `next_permutation` form is O(k·n) and does *thousands of times* more work per query. K was picked so both land in a comparable window — **factorial K = 500,000** (sink `69777768`) and **next-perm K = 333** (sink `46472`); post-pre-sizing the factorial lane runs ~44 ms and next-perm ~74 ms. They are **not** directly wall-time comparable at equal K, so the fair cross-solver metric is **permutations resolved per second**, `K · 1000 / mean_ms`, over identical `(n, k)` inputs:

| solver (Kāra) | lane | K | mean | **perms/sec** |
|---|---|---:|---:|---:|
| factorial (closed form) | seq | 500,000 | 44.4 ms | **11.3 M/s** |
| next-perm (iterate) | seq | 333 | 74.4 ms | **4,473/s** |
| factorial (closed form) | auto-par | 500,000 | 9.4 ms | **53.4 M/s** |
| next-perm (iterate) | auto-par | 333 | 11.4 ms | **29,300/s** |

So on identical queries the O(n²) closed form resolves **≈2,520× more permutations per second** than iterating `next_permutation` (seq lane) — the measured price of algorithm choice, and exactly why the closed form is the canonical answer. (Under auto-par the ratio is ≈1,820×: the closed form parallelizes to 53 M/s while next-perm's heavier per-iter body scales less cleanly — see below.)

> **A karac auto-par bug found here — now fixed (`99617752`, ledger `B-2026-07-03-34`):** the first cut fed the rotated `(n, k)` cases through captured fixed-size `Array[i64, 9]` lookup tables. Under the default auto-par build those tables miscompiled — a worker indexing `atab[k % m]` with a loop-derived index trapped `vec index out of bounds`, while a constant index and `Vec[i64]` tables were both fine. Root cause: a follow-on to the by-pointer array-capture fix `c3050fc8` (`B-2026-06-15-3`). The reduction worker's modulo bounds-check-elision *preflight* is a Vec-only optimization that reads `{ptr,len,cap}` field 1 as the length; a by-pointer array capture has no such header, so it read `element[1]` as a bogus length and trapped on it (`btab = [1,2,3,4]` → `element[1] = 2 < 4` → false panic). The fix skips the preflight for array captures (their length is the compile-time constant `N`, so the per-iter static-`N` check already suffices). The bench keeps `Vec[i64]` tables (the idiomatic choice, and what the numbers above were measured with); the `Array[i64, 9]` form now compiles and runs correctly on all lanes too.

Measured 2026-10-31 (`measured_at` 2026-11-01T02:21Z) — Apple M5 Pro (6P+12E), Darwin 25.6.0, hyperfine, 30 seq / 50 par runs. karac `g6697158fa` (0.9.0-dev.14057, v2/MIR backend; the auto-par `Array`-capture fix `99617752` and the loop-fill pre-sizing extensions `23287e52` + `e9c33a8d` date from the 2026-07-04 snapshot — see the factorial discussion below), rustc 1.95.0, Apple clang 21.0.0, go 1.26.3. All numbers from the committed [`results.json`](bench/results.json) unless marked otherwise.

### Runtime — seq lane

**Next-perm** is the clean apples-to-apples comparison — one buffer allocation per query, then in-place swaps (compute-bound):

| Implementation (next-perm, seq) | Wall time |
|---|---|
| **kāra nextperm (seq)** | **74.4 ± 1.3 ms** |
| c    nextperm         | 77.8 ± 1.2 ms |
| rust nextperm (`overflow-checks=on`) | 78.1 ± 0.9 ms |
| rust nextperm         | 78.3 ± 0.9 ms |
| go   nextperm         | 111.2 ± 2.5 ms |

Kāra codegen lands **~4–5% ahead of C and Rust** (74.4 vs 77.8 / 78.3; Kāra/C 0.96×, Kāra/Rust 0.95×) — a compute-bound integer workload with almost no allocation is where Kāra's LLVM backend ties or edges its native peers. Against the previous run (2026-07-28, legacy backend) the ratios are flat (Kāra/Rust 0.96× → 0.95×, Kāra/C 0.96× → 0.96×). Go trails by 1.49×.

**Factorial** allocates three `Vec`s per query (`fact` / `digits` / `result`) — and this is where a **compiler optimization** the kata surfaced pays off:

| Implementation (factorial, seq) | Wall time |
|---|---|
| c    factorial        | **33.1 ± 1.9 ms** |
| go   factorial        | 36.7 ± 0.5 ms |
| **kāra factorial (seq)** | **44.4 ± 2.0 ms** |
| rust factorial (`overflow-checks=on`) | 103.5 ± 3.9 ms |
| rust factorial        | 104.2 ± 4.0 ms |

C and Go pre-size every buffer (`malloc(n)` / `make(…, n)`) and never realloc. The **idiomatic Rust mirror grows its Vecs by `push`** (`Vec::new()`, matching the kata's `Vec.new()`) and pays the realloc churn — 104 ms, 3.1× behind C. Kāra writes the *same* `Vec.new()` idiom, yet lands at **44.4 ms — 2.35× ahead of Rust** and only 1.34× behind C (1.21× behind Go). Against the previous run (2026-07-28, legacy backend) the ratios are flat: Kāra/Rust 0.39× → 0.43×, Kāra/C 1.30× → 1.34×, Kāra/Go 1.37× → 1.21×. The difference is that **karac's automatic loop-fill pre-sizing pass rewrites `Vec.new()` → `with_capacity` for a counted push-loop**, so all three buffers are single-allocated with no source change — the growth cost the Rust programmer would have to eliminate by hand (`Vec::with_capacity`). Building this kata drove three extensions to that pass (`23287e52` + `e9c33a8d`): it now covers `while d <= n` inclusive fills (previously only `<`), cumulative fills that *read* the buffer (`fact.push(fact[i-1]·i)`), and a pre-loop **seed push** (`fact.push(1)`), which together are what let all three of the solver's Vecs pre-size. The residual 1.34× behind C is the **safe-by-default tax** — bounds- and overflow-checks — the same checked-vs-release gap kata #57/#59 measured, not allocation: with the growth gone, this lane is now compute-bound like next-perm. (Rust reaches the same floor with an explicit `with_capacity`; the point is that Kāra's compiler gets there from the naïve source.)

### Runtime — auto-par regime

Both solvers' `total = total + <checksum>` reductions are auto-par-eligible, so the default `karac build` parallelises both — verified in the emitted IR (`KARAC_MIR_LL`): each default build carries a call of `karac_mir_task_spawn`, neither `KARAC_AUTO_PAR=0` build does:

| Solver | Kāra (auto-par) | Rust (rayon) | Kāra speedup vs own seq |
|---|---|---|---|
| factorial | **9.4 ± 1.1 ms** | 30.3 ± 3.1 ms | 4.7× |
| next-perm | 11.4 ± 0.4 ms | **10.0 ± 0.4 ms** | 6.6× |

On **factorial**, Kāra's zero-parallel-code auto-par is **3.2× faster than hand-written rayon** (9.4 vs 30.3 ms; Kāra/rayon 0.41× → 0.31× against the previous run) — it carries the pre-sizing win from the seq lane into every worker, while the rayon mirror still grows its Vecs per iteration. On **next-perm** (a ~10 ms dispatch-bound workload where the per-iter body is a heavy `next_permutation` walk with a single tiny fill) the two are close, rayon ahead by 1.13× (10.0 vs 11.4 ms) — a gap now larger than either side's ±0.4 ms σ, and flat against the previous run (1.10×). Both parallelize well over their own seq lanes (4.7× / 6.6×).

### Runtime — Python

| Run | Mean ± σ | projected to compiled K | vs Kāra seq |
|---|---|---|---|
| `py factorial` (K=50k) | 60.9 ± 0.7 ms (last measured 2026-07-04, not re-run) | ~609 ms @ K=500k | ~14× slower |
| `py nextperm` (K=9) | 120.5 ± 1.1 ms (last measured 2026-07-04, not re-run) | ~4.5 s @ K=333 | ~60× slower |

The "vs Kāra seq" column divides the 2026-07-04 Python figures by this run's Kāra seq times (a cross-session ratio). Python's factorial multiple (~14×) doubled from the pre-pre-sizing snapshot precisely because Kāra's factorial seq lane got 2× faster; its next-perm multiple (~60×) is larger still because that solver is pure-Python per-step loops with no C-implemented shortcut to hide behind.

### Compile elapsed (cold)

| Compiler | Time |
|---|---|
| clang -O3 factorial          | **52.7 ± 1.2 ms** |
| rustc -O factorial           | 111.8 ± 1.8 ms |
| **karac build nextperm**     | 175.5 ± 2.3 ms |
| **karac build factorial**    | **178.8 ± 1.8 ms** |

Compile now favours `rustc -O`: karac is **1.60× slower than `rustc -O`** on factorial and 3.40× clang -O3 (the 2026-07-04 snapshot had karac 1.12× faster than rustc). The same flip shows across the corpus under the MIR backend (tracked as [`B-2026-10-31-41`](../../../../kara/docs/bugs-v2.md)).

### Binary size

| Implementation | Size |
|---|---|
| c    factorial (seq)          | 32.8 KiB |
| **kāra nextperm (seq)**       | **295.8 KiB** |
| **kāra factorial (seq)**      | **295.8 KiB** |
| **kāra factorial (auto-par)** | **377.1 KiB** |
| rust factorial (seq / rayon)  | 456.3 / 454.5 KiB |
| go   factorial (seq)          | 2434.2 KiB |

Kāra seq is **295.8 KiB** — 1.5× under Rust's 456.3 KiB but 9× C's 32.8 KiB; every MIR-backend Kāra binary is ~300–390 KB where the legacy backend's were ~34 KB (tracked as [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md)). The auto-par binary's +81 KiB over seq is the par-scheduler runtime.

### Runtime memory (peak)

| Implementation | Peak |
|---|---|
| **kāra factorial (seq)**      | **1.05 MiB** |
| c    factorial (seq)          | 1.09 MiB |
| rust factorial (seq)          | 1.14 MiB |
| **kāra next-perm (auto-par)** | **1.47 MiB** |
| **kāra factorial (auto-par)** | **2.08 MiB** |
| go   factorial (seq)          | 8.92 MiB |

Kāra seq's peak RSS (1.05 MiB) now sits ~48 KiB under C's 1.09 MiB (each buffer is freed inside the loop, so steady state is flat across K). The auto-par 2.08 / 1.47 MiB is the worker pool's per-thread scratch; factorial's is higher because each worker holds three live `Vec`s (now single-allocated, which also trims this from the pre-pre-sizing 2.9 MiB).

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 factorial          | 2.5 MiB |
| rustc -O factorial           | 31.1 MiB |
| **karac build factorial**    | **61.1 MiB** |

Kāra's compile-memory footprint is ~24× clang's and ~2.0× rustc's (the 2026-07-04 snapshot had it ~1.5× *under* rustc) — same flip as compile elapsed above.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline is the codegen-vs-Rust gap. This kata gives it on **two** workloads: on the compute-bound **next-perm** solver Kāra edges Rust (74.4 vs 78.3 ms, and C's 77.8), and on the allocation-heavy **factorial** solver Kāra is **2.35× ahead of the idiomatic Rust mirror** (44.4 vs 104.2 ms) — because karac's pre-sizing pass single-allocates the buffers the naïve `Vec::new()` Rust grows, landing Kāra within 1.34× of C — and under auto-par Kāra beats hand-written rayon on factorial (3.2×) and trails it by 1.13× on next-perm. C calibrates the LLVM/allocator floor, Go is the cross-runtime point, Python is the ergonomic foil. Kāra edging its semantic peer here is a compiler-optimization win, not a codegen-quality one: idiomatic-source-to-idiomatic-source, karac's automatic pre-sizing does what the Rust author would do by hand.
