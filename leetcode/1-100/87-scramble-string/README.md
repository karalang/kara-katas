# 87. Scramble String

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** String · Dynamic Programming &nbsp;·&nbsp; **Source:** [leetcode.com/problems/scramble-string](https://leetcode.com/problems/scramble-string/)

`s2` is a **scramble** of `s1` if `s1` can be turned into `s2` by this recursive process: split the string into two non-empty parts, optionally swap them, and recursively scramble each part. Given equal-length `s1` and `s2`, decide whether `s2` is a scramble of `s1`.

```
great  ~  rgeat   ->  true    (gr|eat -> gr|eat, then g|r swapped -> rg|eat)
abcde  ~  caebd   ->  false
```

**Constraints:** `1 ≤ s1.length ≤ 30`; `s1.length == s2.length`; lowercase letters.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **Recursive split + char-count pruning** ★ | [`scramble_string.kara`](scramble_string.kara) ✓ via `karac run` / `karac build` | [`scramble_string.py`](scramble_string.py) ✓ |
| **Top-down memoised (`O(n⁴)`)** | [`scramble_string_memo.kara`](scramble_string_memo.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output across all fourteen test cases, under default (auto-par on) and `KARAC_AUTO_PAR=0` builds alike, and both approaches agree with each other, with the Python mirror, **and with a definitive brute-force scramble enumeration** (generate every scramble of `s1`, test membership). Both compile with **zero diagnostics**.

## The recursion, and taming it with a memo

`s2` is a scramble of `s1` iff there is **some** split point `k` where either

```
(no swap)  s1[..k] scrambles to s2[..k]     AND  s1[k..] scrambles to s2[k..]
(swap)     s1[..k] scrambles to s2[len-k..] AND  s1[k..] scrambles to s2[..len-k]
```

**Recursive split + char-count pruning** ([`scramble_string.kara`](scramble_string.kara), the ★) works over index windows of two `Vec[u8]` (no substring copies): a call is `scramble(s1, i1, s2, i2, len)`. Two prunes keep the branching alive:

1. an **identical window** is trivially a scramble (early `true`), and
2. two windows with a different **letter multiset** can never match — the anagram check (early `false`) that kills almost every dead branch.

Only survivors fan out over the `len − 1` split points, each tried with and without the swap. Without the multiset prune this is exponential; with it, the LeetCode-scale inputs are fine.

**Top-down memoised** ([`scramble_string_memo.kara`](scramble_string_memo.kara)) caches each `(i1, i2, len)` window result in a flat tri-state memo (`-1` unknown / `0` false / `1` true) — a single `Vec[i64]` of length `n·n·(n+1)`, indexed by `(i1·n + i2)·(n+1) + len`, threaded `mut ref` through the recursion. There are `O(n³)` distinct windows and each does `O(n)` split work, so the whole search is `O(n⁴)`. The two cheap prunes still run before the cache write. A distinct surface — a flat 3D memo with tri-state cells — that must agree with the ★ byte-for-byte.

## Kāra features exercised

- **Window-indexed recursion over `Vec[u8]`** — `scramble(s1, i1, s2, i2, len)` recurses on index windows without copying substrings; `String.bytes()` builds the byte vectors.
- **Byte → letter-index arithmetic into a stack `Array[i64, 26]`** — `(s1[i1 + k] as i64) - 97` maps `'a'..'z'` into a fixed 26-slot count table (a stack `Array`, re-zeroed each call — *not* a per-call `Vec`, which would heap-allocate inside the hot recursion; see the profiling note under Benchmarks) for the multiset prune (`u8` → `i64` cast, the path hardened by ledger `B-2026-07-11-2`).
- **Flat 3D memo with tri-state cells** — the memoised variant threads a `mut ref Vec[i64]` sized `n·n·(n+1)`, computing the linear index `(i1·n + i2)·(n+1) + len` and reading/writing `-1`/`0`/`1` (index-assignment into a mutable Vec, kata [#80](../80-remove-duplicates-from-sorted-array-ii/)'s surface).
- **Short-circuit `and` over recursive calls** — `scramble(...) and scramble(...)` relies on `and` short-circuiting so the second (expensive) recursion only runs when the first succeeds.
- **Auto-parallelised batch reduction** — the benchmark's `for k in 0..K { sum += one(k) }` is an associative reduction the default build **auto-parallelises** with no parallel source (see Benchmarks).

**v1 note.** Test strings are short (`≤ 12`); the per-case sink folds each boolean outcome into a running polynomial hash. Both solvers verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`, and both agree with the brute-force enumeration on every case.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   scramble_string.kara
karac build scramble_string.kara && ./scramble_string

# The memoised variant (identical output):
karac run scramble_string_memo.kara

# Python
python3 scramble_string.py

# Verify they all agree
diff <(karac run scramble_string.kara) <(python3 scramble_string.py)              && echo OK
diff <(karac run scramble_string.kara) <(karac run scramble_string_memo.kara)     && echo OK
```

## Benchmarks
Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`scramble_string.{kara,rs,c,py}`, `go-seq/main.go`, plus the par-lane `scramble_string_par.c`, `rayon/`, `go-par/`).

> ✅ **M5 re-bench (2026-11-01).** Measured on the corpus's **Apple M5 Pro reference machine** (arm64, 6P+12E = 18 logical cores; clang 21 / rustc 1.95 / go 1.26) with **karac g6697158fa** (0.9.0-dev.14057, the v2/MIR backend; the legacy backend was deleted 2026-10-23). The first M5 snapshot (2026-07-11) replaced an earlier x86-64 cloud-container one; there kāra tied the C floor on the seq lane. On the MIR backend it no longer does: the seq lane went from 0.95× to **1.09× `rustc -O`** (0.94× → 1.08× C) and the par lane from 1.03× to **1.39× rayon**, because the MIR build retires **1.67× legacy's instructions** (1.13× its cycles), filed as [`B-2026-11-01-18`](../../../../kara/docs/bugs-v2.md). Auto-par still fires, 6.4× ahead of Go, a 12.6× self-speedup. `bench/results.json` records the M5 host.

**Two lanes over one workload.** A batch of **K = 60,000 independent** memoised scramble decisions: each iteration builds a **length-12** string and a per-iteration coprime-step permutation of it (`s2[j] = s1[(j·5 + iter) % 12]`, so no call hoists), runs the **O(n⁴)** top-down memoised scramble, and folds the **filled memo state** into a work-sensitive per-iteration checksum (so the sink reflects the actual recursion, not just the boolean). The K checksums are combined through an **associative sum** (order-independent, so parallel and sequential produce the same total). This is a **compute-bound** recursion — the memo is the only allocation — so it parallel-scales cleanly, in contrast to [#86](../86-partition-list/)'s allocation-bound list workload. All nine seq + par mirrors must agree on `27504985190000` before timing.

- **Seq lane** — single-threaded: kāra (`KARAC_AUTO_PAR=0`) vs `rustc -O` / `clang -O3` / `go build` per-core.
- **Par lane** — the *same* batch, parallel: the default `karac build` **auto-parallelises the `for k in 0..K` sum reduction with no hand-written parallel code** (verified in the emitted IR (`KARAC_MIR_LL`): the default build calls `karac_mir_task_spawn`, the `KARAC_AUTO_PAR=0` twin does not), raced against hand-tuned C-pthreads, rayon, and goroutines.

**Equal data structure.** Every mirror uses **1D heap arrays** — kāra `Vec`, Rust `Vec`, C `malloc`, Go slice — for the strings and the memo. **Equal safety:** the seq lane includes a `rustc -O -C overflow-checks=on` row (kata [#69](../69-sqrtx/)'s discipline).

#### Seq lane — single-threaded (`--warmup 3 --runs 20`; M5 Pro, karac g6697158fa, 2026-11-01)

| Implementation | Wall time |
|---|---|
| rust scramble_string (rustc -O, overflow-checks=on) | **449.8 ± 3.4 ms** |
| rust scramble_string (rustc -O)                      | 479.0 ± 3.2 ms |
| c    scramble_string (clang -O3)                     | 482.4 ± 3.8 ms |
| **kāra scramble_string (`KARAC_AUTO_PAR=0`)**        | **521.7 ± 4.5 ms** |
| go   scramble_string                                 | 601.4 ± 2.6 ms |

Single-threaded, kāra is now **4th of five**: 1.08× behind the C floor, 1.09× behind plain `rustc -O` and 1.16× behind equal-safety `rust_ovf` (overflow-checked Rust edging plain `-O` is a repeatable quirk of this branchy loop), still 1.15× ahead of Go. Against the 2026-07-28 feed that is a real slip relative to every comparator (Kāra/Rust 0.95× → 1.09×, Kāra/C 0.94× → 1.08×, Kāra/Go 0.74× → 0.87×). The cause is instruction count: on the MIR backend the kata retires **5.09 G instructions to the last legacy build's 3.04 G (1.67×)**, but only 1.13× its cycles (2.01 G vs 1.77 G) — the memoized recursion is memory-latency-bound, so most of the extra work still hides in the stall shadow, just no longer all of it ([`B-2026-11-01-18`](../../../../kara/docs/bugs-v2.md); the July legacy build's parity was itself latency-masked, `B-2026-07-10-5`, same regime as [#78](../78-subsets/)/[#80](../80-remove-duplicates-from-sorted-array-ii/)).

> **Profiling note.** An earlier draft of this kata had kāra ~1.22× behind C. Profiling on this container (the production-representative target) split the gap in two: (1) a **self-inflicted** part — the char-count table was written as a per-call `Vec.new()` instead of a stack `Array[i64, 26]` (the shape C/Rust use), heap-allocating on every recursive call; fixing it recovered ~9% and the 826→727 ms above. (2) A **residual codegen** part — at *equal safety* kāra's hot `scramble` emits **24 bounds/overflow-check branches to `rust_ovf`'s 15** (LLVM elides rustc's but not kāra's); this is the known instruction-density gap tracked in the kara repo's ledger as `B-2026-07-10-5`, to which this kata's data was added. Python at K=4000 was ~1.3 s, timed separately (not re-run 2026-11-01).

#### Par lane — auto-par vs hand-tuned, NOT comparable to seq (`--warmup 5 --runs 30`; M5 Pro, karac g6697158fa, 2026-11-01)

| Implementation | Wall time |
|---|---|
| rust scramble_string (rayon `into_par_iter`)           | **29.6 ± 0.6 ms** |
| c    scramble_string (pthreads — metal floor)          | 34.6 ± 2.3 ms |
| **kāra scramble_string (auto-par, NO parallel code)**  | **41.3 ± 1.0 ms** |
| go   scramble_string (goroutines + WaitGroup)          | 266.1 ± 3.9 ms |

The payoff: this compute-bound recursion parallel-scales cleanly, and kāra's **default build auto-parallelises it with zero parallel source** — no threads, no rayon, just `for k in 0..K { sum += one(k) }` — for a **12.6× self-speedup** over its own seq lane (521.7 → 41.3 ms) on the M5's 18 cores. It lands 1.19× behind the raw-pthreads floor and **1.39× behind hand-tuned rayon** (fastest here at 29.6 ms), and is **6.4× ahead of the goroutine version** (266.1 ms). Against the 2026-07-28 feed that is a slip relative to rayon and C (Kāra/rayon 1.03× → 1.39×, Kāra/C 0.99× → 1.19×; flat against Go, 0.15× → 0.16×). The par build's instruction count is flat across worker counts (5.10 G at 1 worker, 5.12 G at 18), so the par loss is the seq gap carried across the cores, not a scheduling cost ([`B-2026-11-01-18`](../../../../kara/docs/bugs-v2.md)). See [`bench/results.json`](bench/results.json).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — single-threaded on this recursion-heavy DP, and in the par lane kāra's zero-code auto-par vs hand-tuned rayon. C calibrates the metal floor in both lanes, Go the other native data point, Python (a fraction of the iteration count, timed separately) the ergonomic foil.

## Bug ledger

**Surfaced [`B-2026-11-01-18`](../../../../kara/docs/bugs-v2.md)** (perf, open). On the MIR backend (karac g6697158fa, 2026-11-01) this kata's scramble DP retires 1.67× the last legacy build's instructions at 1.13× its cycles: the seq lane went from 0.95× to 1.09× `rustc -O` and the par lane from 1.03× to 1.39× rayon. Unattributed.
