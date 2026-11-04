# 3629. Minimum Jumps to Reach End via Prime Teleportation

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array, Hash Table, Math, BFS, Number Theory &nbsp;·&nbsp; **Source:** [leetcode.com/problems/minimum-jumps-to-reach-end-via-prime-teleportation](https://leetcode.com/problems/minimum-jumps-to-reach-end-via-prime-teleportation/)

You start at index `0` of `nums` and must reach index `n - 1`. From any index `i` you may either:

- **Adjacent step** — jump to `i + 1` or `i - 1` (if in bounds), or
- **Prime teleport** — if `nums[i]` is itself a prime `p`, jump to any `j ≠ i` with `nums[j] % p == 0`.

Return the minimum number of jumps required.

**Constraints:** `1 ≤ n ≤ 10⁵`, `1 ≤ nums[i] ≤ 10⁶`.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| BFS + merged-factors sieve + per-prime bucket | O(n + cap log log cap) time, O(n + cap · ω̄) space | [`bfs_sieve.kara`](bfs_sieve.kara) ✓ | [`bfs_sieve.py`](bfs_sieve.py) ✓ |

## Why a sieve + bucket?

Naive teleport expansion is O(n²): when many entries share a common prime factor (e.g., a `nums` full of even numbers), each visit to a prime-valued index would scan every other index for divisibility. The standard trick keeps BFS linear:

1. Build a **per-number prime-factor table**. `factors[k]` holds the ascending distinct prime factors of `k`. The same sieve pass that identifies primes also stamps each composite's distinct primes — one structure, no separate factorization step.
2. For every `j`, walk `factors[nums[j]]` and append `j` to `bucket[p]` for each prime `p`.
3. The first time BFS visits an index whose value *is* the prime `p` (detected by `factors[v][0] == v` — the smallest prime factor of a prime is itself), **drain `bucket[p]`** via `Map.remove`. That prime's whole bucket contributes at most once across the entire search.

The merged-factors variant (one `Vec[Vec[i64]]` table) was chosen over the textbook smallest-prime-factor sieve (`Vec[i64]` with a separate `distinct_prime_factors` helper) because it's tighter for *this* problem: the only number-theoretic queries we need are "is this prime?" and "what are its distinct prime factors?" — both direct lookups in `factors`. The textbook SPF version has lower memory (8 MB vs ~48 MB at `cap = 10⁶`) and is more reusable across other number-theoretic problems (Euler's totient, Möbius, divisor count); the merged table is simpler at the call site and removes one inner factorization loop. For LC 3629 specifically the simplicity wins; for a competitive-programming template the SPF version generalizes better.

Note: the LeetCode hint says "for each prime `p` dividing `nums[i]`," but the problem text is stricter — teleport only fires when `nums[i]` is itself prime. We follow the problem text. (Both formulations agree on the BFS layer count, since when `nums[i]` is prime, `nums[i]` is the only prime dividing it.)

## Kāra features exercised

- **Nested `Vec[Vec[i64]]`** — factor table with read/write through indexed access (`factors[j].push(i)`); `Vec.filled` deep-clones the inner `Vec.new()` so each slot is independent storage.
- **`Map` entry-or-insert-then-mutate** — `bucket.entry(p).or_insert(Vec.new()).push(j)`, the canonical insert-or-modify idiom.
- **One-shot `Map.remove`** — `match bucket.remove(v) { Some(indices) => …, None => {} }` consumes a prime's bucket exactly once.
- **`VecDeque[T]` as BFS frontier** — `push_back` / `pop_front` with `(i64, i64)` tuple payloads destructured via `let (i, d) = node`.
- **`and` short-circuit** — guards out-of-bounds `visited[i - 1]` and empty-`factors[v]` indexed accesses without a separate materialization step.

## Bug ledger

**Surfaced [`B-2026-06-15-3`](../../../../kara/docs/bug-ledger.md)** (auto-par compile-time blow-up, fixed `c3050fc8`). This kata's auto-parallelized reduction captured a fixed-size sieve array **by value** into the per-branch worker env; LLVM's `-O2` store-merging then scalarized the multi-KB copy and went super-linear — `karac build` ballooned to **60 s / 639 MiB** (vs ~95 ms normally). The compile-elapsed numbers below are post-fix; the fix captures array-typed reduction captures by pointer (a read-only shared input whose parent frame outlives the join).

**Surfaced [`B-2026-11-04-38`](../../../../kara/docs/bugs-v2.md)** (perf, low, open). Seq peak RSS rose from 59.9 MiB to 88.9 MiB between the 2026-07-28 feed and karac gf0017054a (2026-11-04), while Rust held at 60.1 MiB.

## Running

```bash
karac run bfs_sieve.kara
python3 bfs_sieve.py
diff <(karac run bfs_sieve.kara) <(python3 bfs_sieve.py) && echo OK
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, and Go, on the M5 Pro with karac `0.8.0-dev.14374+gf0017054a` (gf0017054a, the v2/MIR backend), measured 2026-11-04. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`bfs_sieve.{kara,rs,c}`, `go-seq/main.go`, and the par mirrors `rayon/`, `bfs_sieve_par.c`, `go-par/`). Python rows run only with `KARA_BENCH_INCLUDE_PY=1`, which this run did not set, so its figures below are labelled with their own date.

**Workload.** N = 50,000 deterministically-seeded `nums` with values up to 10⁶ chosen to maximize teleport activity (every node has ≥1 prime factor); K = 50 outer iterations amortize per-process startup. The full O(cap log log cap) sieve over `cap = 10⁶` dominates wall-clock; that's intentional — the sieve + bucket build is the hot path the kata's data structure exists to support. Sink is the BFS layer count summed across iterations; every compiled mirror, seq and par, must agree on `24350` before any timing begins.

### Runtime

Seq lane, M5 Pro, 2026-11-04, hyperfine `--warmup 2 --runs 10`. Kāra is the `KARAC_AUTO_PAR=0` twin:

| Implementation | Wall time | Kāra / this |
|---|---|---|
| c    bfs_sieve (clang -O3) | 1800.3 ± 32.1 ms | 1.02× |
| **kāra bfs_sieve (codegen, seq)** | **1837.1 ± 36.9 ms** | — |
| rust bfs_sieve `-O -C overflow-checks=on` (equal-safety) | 1996.0 ± 19.7 ms | 0.92× |
| rust bfs_sieve `-O` | 2009.7 ± 28.5 ms | 0.91× |
| go   bfs_sieve | 4176.2 ± 34.5 ms | 0.44× |
| py   bfs_sieve (last measured 2026-06-05, not re-run) | 15719.7 ± 871.8 ms | n/a |

Par lane, `--warmup 5 --runs 30`. Kāra is the default auto-parallelised build; its IR has a `@karac_mir_task_spawn` call that the `KARAC_AUTO_PAR=0` build's does not:

| Implementation | Wall time | Kāra / this |
|---|---|---|
| rust bfs_sieve (rayon, `overflow-checks=on`, equal-safety) | 426.0 ± 9.2 ms | 1.17× |
| rust bfs_sieve (rayon) | 431.6 ± 4.9 ms | 1.15× |
| **kāra bfs_sieve (auto-par)** | **496.4 ± 6.0 ms** | — |
| c    bfs_sieve (pthreads) | 840.7 ± 17.5 ms | 0.59× |
| go   bfs_sieve (goroutines) | 1732.7 ± 28.9 ms | 0.29× |

Single-threaded, Kāra is now **ahead of Rust (0.91×)**, level with C (1.02×), and well ahead of Go (0.44×). Against the previous feed (2026-07-28) those ratios were 1.11× Rust, 1.20× C and 0.54× Go. Under auto-par, Kāra is **1.15× rayon**, down from 2.13×, and ahead of hand-written pthreads C (0.59×, from 1.06×) and goroutines (0.29×, from 0.52×). Auto-par runs 3.70× faster than Kāra's own seq twin. Against the legacy backend (exact counts, dd86e3955, `KARAC_AUTO_PAR=0`) the seq build executes 0.97× the instructions in 0.92× the cycles.

### Compile elapsed (cold)

`--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Compiler | Time |
|---|---|
| **karac build bfs_sieve.kara** | **208.1 ± 3.2 ms** |
| rustc -O bfs_sieve.rs          | 150.9 ± 3.1 ms |
| clang -O3 bfs_sieve.c          | 54.3 ± 0.6 ms |

`karac build` (the default, auto-par build) is **1.38× rustc -O** and **3.83× clang** on this kata. On the previous feed (2026-07-28) it was 0.76× rustc.

### Binary size

| Implementation | Seq | Par |
|---|---|---|
| c    bfs_sieve | 33.2 KiB | 33.4 KiB |
| **kāra bfs_sieve** | **67.2 KiB** | **393.5 KiB** |
| rust bfs_sieve | 474.4 KiB | 455.2 KiB |
| go   bfs_sieve | 2434.5 KiB | 2451.5 KiB |

Kāra's seq binary is 68,824 B, 2.0× clang's and 7.1× smaller than rustc's. The par binary is 402,952 B, 1.2× smaller than the rayon build. The seq binary was 302,536 B on the previous feed; B-2026-10-28-36 (fixed) is that history.

### Runtime memory (peak)

| Implementation | Seq | Par |
|---|---|---|
| c    bfs_sieve  | 82.0 MiB | 1435.3 MiB |
| **kāra bfs_sieve (codegen)** | **88.9 MiB** | **1396.3 MiB** |
| rust bfs_sieve  | 60.1 MiB | 1036.2 MiB |
| go   bfs_sieve  | 125.1 MiB | 1648.9 MiB |
| py   bfs_sieve (last measured 2026-06-05, not re-run) | 493.6 MiB | n/a |

Kāra's seq peak is **1.48× Rust's** and 1.09× C's. It rose from 59.9 MiB on the previous feed while Rust held at 60.1 MiB (see Bug ledger). The par lanes all hold about 1.0–1.6 GiB: Kāra 1.36 GiB, rayon 1.01 GiB, pthreads C 1.40 GiB, goroutines 1.61 GiB. The bench's seq working set is dominated by the `factors: Vec[Vec[i64]]` table at `cap = 10⁶` (~48 MiB the kata's commentary calls out).

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| **`karac build bfs_sieve.kara`** | **96.6 MiB** |
| `rustc -O bfs_sieve.rs`          | 45.4 MiB |
| `clang -O3 bfs_sieve.c`          | 2.6 MiB |

Kāra's compile-memory footprint is **96.6 MiB** on this kata, 2.1× rustc's. On the previous feed it was 0.58× rustc's.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why Rust is in the harness`](../../1-100/1-two-sum/README.md#why-rust-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratios for v1 are the codegen-vs-Rust figures above (0.91× seq, 1.15× against rayon). C calibrates the LLVM-backend floor — though note its seq RSS runs 36% above Rust's here, probably the cost of the mirror's direct-addressed `bucket` array (inferred, not measured). Go is the cross-runtime data point; Python is the ergonomic foil.
