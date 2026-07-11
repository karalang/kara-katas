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

> ✅ **M5-confirmed (2026-07-11).** Re-measured on the corpus's **Apple M5 Pro reference machine** (arm64, 6P+12E = 18 logical cores; clang 21 / rustc 1.95 / go 1.26; karac from current `main`), replacing the earlier x86-64 cloud-container snapshot. On the M5 kāra improves to **tie the C floor** on the seq lane (it was 4th on the container) — though honestly that parity is *latency-masked*: kāra retires 1.74× C's instructions, but this memoized `O(n⁴)` recursion is memory-latency-bound (IPC ~1.2-2.1), so they hide in the stall shadow (`B-2026-07-10-5`). Par-lane auto-par lands within 1.16× of rayon, 5.5× ahead of Go, an 11.4× self-speedup. `bench/results.json` records the M5 host.

**Two lanes over one workload.** A batch of **K = 60,000 independent** memoised scramble decisions: each iteration builds a **length-12** string and a per-iteration coprime-step permutation of it (`s2[j] = s1[(j·5 + iter) % 12]`, so no call hoists), runs the **O(n⁴)** top-down memoised scramble, and folds the **filled memo state** into a work-sensitive per-iteration checksum (so the sink reflects the actual recursion, not just the boolean). The K checksums are combined through an **associative sum** (order-independent, so parallel and sequential produce the same total). This is a **compute-bound** recursion — the memo is the only allocation — so it parallel-scales cleanly, in contrast to [#86](../86-partition-list/)'s allocation-bound list workload. All nine seq + par mirrors must agree on `27504985190000` before timing.

- **Seq lane** — single-threaded: kāra (`KARAC_AUTO_PAR=0`) vs `rustc -O` / `clang -O3` / `go build` per-core.
- **Par lane** — the *same* batch, parallel: the default `karac build` **auto-parallelises the `for k in 0..K` sum reduction with no hand-written parallel code**, raced against hand-tuned C-pthreads, rayon, and goroutines.

**Equal data structure.** Every mirror uses **1D heap arrays** — kāra `Vec`, Rust `Vec`, C `malloc`, Go slice — for the strings and the memo. **Equal safety:** the seq lane includes a `rustc -O -C overflow-checks=on` row (kata [#69](../69-sqrtx/)'s discipline).

#### Seq lane — single-threaded (`--warmup 3 --runs 20`)

| Implementation | Wall time |
|---|---|
| rust scramble_string (rustc -O, overflow-checks=on) | **389.9 ± 6.0 ms** |
| rust scramble_string (rustc -O)                      | 414.1 ± 6.0 ms |
| **kāra scramble_string (`KARAC_AUTO_PAR=0`)**        | **418.0 ± 6.0 ms** |
| c    scramble_string (clang -O3)                     | 418.8 ± 6.0 ms |
| go   scramble_string                                 | 550.7 ± 10.0 ms |

Single-threaded, kāra **ties the C floor** (418.0 vs 418.8 ms) and plain `rustc -O` (414.1), 1.32× ahead of Go, with only equal-safety `rust_ovf` clearly ahead (1.07×; overflow-checked Rust edging plain `-O` is a repeatable quirk of this branchy loop). The honest nuance: this is **latency-masked parity** — kāra retires **3.95 G instructions to C's 2.28 G (1.74×)**, but the memoized recursion is memory-bound (IPC 2.09 vs C 1.19), so the extra work executes in the stall shadow and the clocks tie (the `B-2026-07-10-5` latency-hidden regime, same as [#78](../78-subsets/)/[#80](../80-remove-duplicates-from-sorted-array-ii/)).

> **Profiling note.** An earlier draft of this kata had kāra ~1.22× behind C. Profiling on this container (the production-representative target) split the gap in two: (1) a **self-inflicted** part — the char-count table was written as a per-call `Vec.new()` instead of a stack `Array[i64, 26]` (the shape C/Rust use), heap-allocating on every recursive call; fixing it recovered ~9% and the 826→727 ms above. (2) A **residual codegen** part — at *equal safety* kāra's hot `scramble` emits **24 bounds/overflow-check branches to `rust_ovf`'s 15** (LLVM elides rustc's but not kāra's); this is the known instruction-density gap tracked in the kara repo's ledger as `B-2026-07-10-5`, to which this kata's data was added. Python at K=4000 is ~1.3 s, timed separately.

#### Par lane — auto-par vs hand-tuned, NOT comparable to seq (`--warmup 5 --runs 30`)

| Implementation | Wall time |
|---|---|
| rust scramble_string (rayon `into_par_iter`)           | **31.7 ± 2.0 ms** |
| c    scramble_string (pthreads — metal floor)          | 35.3 ± 2.0 ms |
| **kāra scramble_string (auto-par, NO parallel code)**  | **36.8 ± 2.0 ms** |
| go   scramble_string (goroutines + WaitGroup)          | 204.4 ± 8.0 ms |

The payoff: this compute-bound recursion parallel-scales cleanly, and kāra's **default build auto-parallelises it with zero parallel source** — no threads, no rayon, just `for k in 0..K { sum += one(k) }` — for an **11.4× self-speedup** over its own seq lane (418.0 → 36.8 ms) on the M5's 18 cores. It **ties the raw-pthreads floor** (36.8 vs 35.3 ms, 1.04×), lands 1.16× behind hand-tuned rayon (fastest here at 31.7 ms), and is **5.5× ahead of the goroutine version** (204.4 ms). Kāra's free auto-par sits within a whisker of hand-tuned parallel Rust and *at* the metal floor. See [`bench/results.json`](bench/results.json).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — single-threaded on this recursion-heavy DP, and in the par lane kāra's zero-code auto-par vs hand-tuned rayon. C calibrates the metal floor in both lanes, Go the other native data point, Python (a fraction of the iteration count, timed separately) the ergonomic foil.
