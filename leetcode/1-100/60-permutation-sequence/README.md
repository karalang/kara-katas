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

**The two solvers run different K.** The factorial form is O(n²) and independent of `k`; the `next_permutation` form is O(k·n) and does *thousands of times* more work per query. To land both in the same ~80 ms window they use **factorial K = 500,000** (sink `69777768`) and **next-perm K = 333** (sink `46472`) — so they are **not** directly wall-time comparable at equal K. The fair cross-solver metric is **permutations resolved per second**, `K · 1000 / mean_ms`, over identical `(n, k)` inputs:

| solver (Kāra) | lane | K | mean | **perms/sec** |
|---|---|---:|---:|---:|
| factorial (closed form) | seq | 500,000 | 85.4 ms | **5.85 M/s** |
| next-perm (iterate) | seq | 333 | 77.8 ms | **4,281/s** |
| factorial (closed form) | auto-par | 500,000 | 27.9 ms | **17.9 M/s** |
| next-perm (iterate) | auto-par | 333 | 8.5 ms | **39,176/s** |

So on identical queries the O(n²) closed form resolves **≈1,370× more permutations per second** than iterating `next_permutation` (seq lane) — the measured price of algorithm choice, and exactly why the closed form is the canonical answer. (The gap narrows to ≈460× under auto-par because next-perm's heavier per-iter body parallelizes better — see below.)

> **A karac auto-par bug found here — now fixed (`99617752`, ledger `B-2026-07-03-34`):** the first cut fed the rotated `(n, k)` cases through captured fixed-size `Array[i64, 9]` lookup tables. Under the default auto-par build those tables miscompiled — a worker indexing `atab[k % m]` with a loop-derived index trapped `vec index out of bounds`, while a constant index and `Vec[i64]` tables were both fine. Root cause: a follow-on to the by-pointer array-capture fix `c3050fc8` (`B-2026-06-15-3`). The reduction worker's modulo bounds-check-elision *preflight* is a Vec-only optimization that reads `{ptr,len,cap}` field 1 as the length; a by-pointer array capture has no such header, so it read `element[1]` as a bogus length and trapped on it (`btab = [1,2,3,4]` → `element[1] = 2 < 4` → false panic). The fix skips the preflight for array captures (their length is the compile-time constant `N`, so the per-iter static-`N` check already suffices). The bench keeps `Vec[i64]` tables (the idiomatic choice, and what the numbers above were measured with); the `Array[i64, 9]` form now compiles and runs correctly on all lanes too.

Snapshot — Apple M5 Pro (6P+12E), Darwin 25.5.0, 2026-07-04, hyperfine `--warmup 5–10 --runs 30–50 -N`. karac 0.1.0, rustc 1.95.0, Apple clang 21.0.0, go 1.26.3. All numbers from the committed [`results.json`](bench/results.json).

### Runtime — seq lane

**Next-perm** is the clean apples-to-apples comparison — one buffer allocation per query, then in-place swaps (compute-bound):

| Implementation (next-perm, seq) | Wall time |
|---|---|
| c    nextperm         | **74.6 ± 0.7 ms** |
| rust nextperm         | 75.2 ± 1.4 ms |
| **kāra nextperm (seq)** | **77.8 ± 2.2 ms** |
| go   nextperm         | 107.7 ± 1.6 ms |

Kāra codegen lands **within 4% of C and Rust** (77.8 vs 74.6 / 75.2) — a compute-bound integer workload with almost no allocation is where Kāra's LLVM backend ties its native peers. Go trails by 1.44×.

**Factorial** tells a different story — it allocates three growing `Vec`s per query (`fact` / `digits` / `result`), so it is **allocation-bound**:

| Implementation (factorial, seq) | Wall time |
|---|---|
| go   factorial        | **32.2 ± 0.8 ms** |
| c    factorial        | 32.3 ± 1.4 ms |
| **kāra factorial (seq)** | **85.4 ± 2.7 ms** |
| rust factorial        | 101.3 ± 4.1 ms |

Here C and Go pre-size every buffer (`malloc(n)` / `make(…, n)`) and never realloc, while the Kāra and Rust mirrors grow `fact`/`result` by `push` — matching the kata's `Vec.new()` idiom — and pay the realloc churn, landing 2.6× behind the pre-sized floor. That the *same* codegen ties C on next-perm but trails it here isolates the cost to allocation growth, not arithmetic or dispatch (kata #57's `Vec.with_capacity` note is the same lever). Notably **Kāra edges Rust** (85.4 vs 101.3): on this buffer-growth-dominated loop Kāra's `Vec` growth schedule reallocs less than Rust's default.

> **Follow-up (compiler improvement, `23287e52` + `e9c33a8d`):** the numbers above predate three extensions to karac's automatic loop-fill pre-sizing pass — it now recognizes `while d <= n { … }` inclusive fills (previously only `<`), cumulative fills that *read* the buffer (`v.push(v[i-1] · i)`), and a pre-loop **seed push** (`fact.push(1)` before the counted loop). Together they auto-pre-size all three of the solver's Vecs (`fact` / `digits` / `result`) with **no source change**, taking the **factorial seq lane 2.09× faster** (measured 87.3 → 41.8 ms on a re-run) — within 1% of hand-written `with_capacity`, i.e. onto the pre-sized C/Go floor. These tables are the pre-improvement snapshot; a re-benchmark once that compiler build ships would show the factorial lane at C/Go parity.

### Runtime — auto-par regime

Both solvers' `total = total + <checksum>` reductions are auto-par-eligible, so `karac build` emits a `karac_par_reduce` by default:

| Solver | Kāra (auto-par) | Rust (rayon) | Kāra speedup vs own seq |
|---|---|---|---|
| factorial | **27.9 ± 3.4 ms** | 30.8 ± 3.7 ms | 3.06× |
| next-perm | **8.5 ± 0.7 ms** | 9.8 ± 0.5 ms | **9.15×** |

Kāra's zero-parallel-code auto-par **beats hand-written rayon on both** (1.10× / 1.16×). Next-perm scales far better (9.15× vs 3.06×) because each iteration does thousands of `next_permutation` steps — heavy enough to amortize the dispatch overhead — whereas factorial's tiny per-iter body leaves the reduction dominated by fan-out cost.

### Runtime — Python

| Run | Mean ± σ | projected to compiled K | vs Kāra seq |
|---|---|---|---|
| `py factorial` (K=50k) | 61.3 ± 1.0 ms | ~613 ms @ K=500k | ~7.2× slower |
| `py nextperm` (K=9) | 121.4 ± 1.4 ms | ~4.5 s @ K=333 | ~58× slower |

Python's factorial multiple is small (~7×) because the work is short CPython list ops on a tiny `n`; its next-perm multiple is large (~58×) because that solver is pure-Python per-step loops with no C-implemented shortcut to hide behind.

### Compile elapsed (cold)

| Compiler | Time |
|---|---|
| clang -O3 factorial          | **48.1 ± 1.4 ms** |
| **karac build factorial**    | **86.4 ± 2.0 ms** |
| **karac build nextperm**     | 89.1 ± 1.3 ms |
| rustc -O factorial           | 106.0 ± 2.3 ms |

Kāra compiles **1.23× faster than `rustc -O`** and sits at 1.80× of clang -O3 — same shape as the rest of the corpus.

### Binary size

| Implementation | Size |
|---|---|
| c    factorial (seq)          | 32.8 KiB |
| **kāra nextperm (seq)**       | **33.2 KiB** |
| **kāra factorial (seq)**      | **33.4 KiB** |
| **kāra factorial (auto-par)** | **312.2 KiB** |
| rust factorial (seq / rayon)  | 456.2 / 454.5 KiB |
| go   factorial (seq)          | 2434.2 KiB |

Kāra seq sits within 0.6 KiB of C's no-frills floor; the auto-par binary's +279 KiB is the par-scheduler runtime.

### Runtime memory (peak)

| Implementation | Peak |
|---|---|
| c / kāra / rust factorial (seq) | 1.1 MiB |
| **kāra next-perm (auto-par)** | **1.5 MiB** |
| **kāra factorial (auto-par)** | **2.9 MiB** |
| go   factorial (seq)          | 8.8 MiB |

Kāra seq's peak RSS matches C's 1.1 MiB (each buffer is freed inside the loop, so steady state is flat across K). The auto-par 2.9 / 1.5 MiB is the worker pool's per-thread scratch; factorial's is higher because each worker holds three live `Vec`s.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 factorial          | 2.5 MiB |
| **karac build factorial**    | **19.9 MiB** |
| rustc -O factorial           | 31.2 MiB |

Kāra's compile-memory footprint is ~8× clang's and ~1.6× lower than rustc's — same shape as the rest of the corpus.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline is the codegen-vs-Rust gap. This kata gives it on **two** workloads: on the compute-bound **next-perm** solver Kāra ties Rust (77.8 vs 75.2 ms, both within 4% of C), and on the allocation-bound **factorial** solver Kāra actually edges Rust (85.4 vs 101.3 ms) while both trail the pre-sized C/Go floor — and under auto-par Kāra beats hand-written rayon on both. C calibrates the LLVM/allocator floor, Go is the cross-runtime point, Python is the ergonomic foil.
