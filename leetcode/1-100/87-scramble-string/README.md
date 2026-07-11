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
- **Byte → letter-index arithmetic** — `(s1[i1 + k] as i64) - 97` maps `'a'..'z'` into a 26-slot `Vec[i64]` count table for the multiset prune (`u8` → `i64` cast, the path hardened by ledger `B-2026-07-11-2`).
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

> ⚠️ **Machine caveat.** Measured on a **shared x86-64 Linux cloud container** (Intel Xeon @ 2.80 GHz, 4 vCPU, Linux 6.18.5; karac from current `main`). These are container numbers only — this kata has **no M5 `results.json` yet**; it will be re-benched on the corpus's Apple M5 Pro and the canonical table added then. Don't compare absolute times/sizes/RSS against sibling katas' M5 tables; [`bench/results.container-x86.json`](bench/results.container-x86.json) records the real host.

**Two lanes over one workload.** A batch of **K = 60,000 independent** memoised scramble decisions: each iteration builds a **length-12** string and a per-iteration coprime-step permutation of it (`s2[j] = s1[(j·5 + iter) % 12]`, so no call hoists), runs the **O(n⁴)** top-down memoised scramble, and folds the **filled memo state** into a work-sensitive per-iteration checksum (so the sink reflects the actual recursion, not just the boolean). The K checksums are combined through an **associative sum** (order-independent, so parallel and sequential produce the same total). This is a **compute-bound** recursion — the memo is the only allocation — so it parallel-scales cleanly, in contrast to [#86](../86-partition-list/)'s allocation-bound list workload. All nine seq + par mirrors must agree on `27504985190000` before timing.

- **Seq lane** — single-threaded: kāra (`KARAC_AUTO_PAR=0`) vs `rustc -O` / `clang -O3` / `go build` per-core.
- **Par lane** — the *same* batch, parallel: the default `karac build` **auto-parallelises the `for k in 0..K` sum reduction with no hand-written parallel code**, raced against hand-tuned C-pthreads, rayon, and goroutines.

**Equal data structure.** Every mirror uses **1D heap arrays** — kāra `Vec`, Rust `Vec`, C `malloc`, Go slice — for the strings and the memo. **Equal safety:** the seq lane includes a `rustc -O -C overflow-checks=on` row (kata [#69](../69-sqrtx/)'s discipline).

#### Seq lane — single-threaded (`--warmup 3 --runs 20`)

| Implementation | Wall time |
|---|---|
| rust scramble_string (rustc -O, overflow-checks=on) | 643.8 ± 10.1 ms |
| c    scramble_string (clang -O3)                     | 679.5 ± 11.4 ms |
| rust scramble_string (rustc -O)                      | 708.0 ± 8.3 ms |
| **kāra scramble_string (`KARAC_AUTO_PAR=0`)**        | **826.6 ± 27.7 ms** |
| go   scramble_string                                 | 1115.9 ± 66.5 ms |

Single-threaded, kāra trails the C/Rust cluster by ~1.17–1.28× on this recursion-heavy DP — the branchy `O(n⁴)` memoised search is where its codegen gives up the most ground — while staying well ahead of Go (~1.35×). (Curiously, overflow-checked Rust edged plain `-O` on this run; both are within a few percent.) Python at K=4000 is ~1.3 s, timed separately.

#### Par lane — auto-par vs hand-tuned, NOT comparable to seq (`--warmup 5 --runs 30`)

| Implementation | Wall time |
|---|---|
| c    scramble_string (pthreads — metal floor)          | 175.3 ± 8.6 ms |
| rust scramble_string (rayon `into_par_iter`)           | 185.3 ± 4.4 ms |
| **kāra scramble_string (auto-par, NO parallel code)**  | **218.2 ± 8.6 ms** |
| go   scramble_string (goroutines + WaitGroup)          | 595.6 ± 20.4 ms |

The payoff: this compute-bound recursion parallel-scales cleanly, and kāra's **default build auto-parallelises it with zero parallel source** — no threads, no rayon, just `for k in 0..K { sum += one(k) }` — for a **3.79× self-speedup** over its own seq lane (826.6 → 218.2 ms) on 4 vCPU. That closes most of the single-threaded gap: in the par lane kāra lands ~1.18× behind hand-tuned rayon and ~1.24× off the raw-pthreads floor (versus ~1.20–1.28× behind them single-threaded), and it is **2.7× ahead of the goroutine version** (595.6 ms — Go's per-iteration allocation and scheduler overhead don't recover under parallelism). The auto-par lifts kāra from *behind* the native seq cluster to *within a whisker of* hand-tuned parallel Rust, for free. Records in [`results.container-x86.json`](bench/results.container-x86.json).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — single-threaded on this recursion-heavy DP, and in the par lane kāra's zero-code auto-par vs hand-tuned rayon. C calibrates the metal floor in both lanes, Go the other native data point, Python (a fraction of the iteration count, timed separately) the ergonomic foil.
