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

## Running

```bash
karac run bfs_sieve.kara
python3 bfs_sieve.py
diff <(karac run bfs_sieve.kara) <(python3 bfs_sieve.py) && echo OK
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`bfs_sieve.{kara,rs,c}`, `go-seq/main.go`). The Python mirror is gated behind `KARA_BENCH_INCLUDE_PY=1`.

**Workload.** N = 50,000 deterministically-seeded `nums` with values up to 10⁶ chosen to maximize teleport activity (every node has ≥1 prime factor); K = 3 outer iterations amortize per-process startup. The full O(cap log log cap) sieve over `cap = 10⁶` dominates wall-clock; that's intentional — the sieve + bucket build is the hot path the kata's data structure exists to support. Sink is the BFS layer count summed across iterations; all five mirrors must agree on `1461` before any timing begins.

### Runtime

Snapshot — M5 Pro, 2026-05-25, hyperfine `--warmup 2 --runs 10 --shell=none`:

| Implementation | Wall time |
|---|---|
| c    bfs_sieve (clang -O3) | **127.1 ± 3.8 ms** |
| rust bfs_sieve            | **141.1 ± 1.0 ms** |
| **kāra bfs_sieve (codegen)** | **152.7 ± 2.2 ms** |
| go   bfs_sieve            | 279.7 ± 3.8 ms |
| py   bfs_sieve            | 1009 ± 34 ms |

Kāra runs **1.08× of Rust** and **1.20× of clang -O3** — close-to-parity on the sieve + bucket + BFS hot path. The gap traces to two places: the `Map[i64, Vec[i64]]` bucket dispatch path (kara's per-entry probing vs rust's `HashMap::entry`) and the per-element RC-aware Vec push in the inner `factors[j].push(i)` loop. Both are general-runtime costs the kata exercises heavily; closing them tightens this gap further without per-kata changes. Python is **~6.6× slower than kāra codegen** — the algorithm-dominated regime at N=50k where compiled-with-codegen languages put the same lap on CPython.

### Compile elapsed (cold)

`--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Compiler | Time |
|---|---|
| **karac build bfs_sieve.kara** | **71.2 ± 0.4 ms** |
| rustc -O bfs_sieve.rs          | 149.3 ± 0.9 ms |
| clang -O3 bfs_sieve.c          | 53.7 ± 0.4 ms |

Kāra compiles **2.10× faster than rustc -O** and **1.33× of clang -O3** — same shape as the rest of the kata corpus.

### Binary size

| Implementation | Size |
|---|---|
| c    bfs_sieve | 33.2 KiB |
| **kāra bfs_sieve** | **278.8 KiB** |
| rust bfs_sieve | 474.4 KiB |
| go   bfs_sieve | 2434.5 KiB |

Kāra carries the `Map[i64, Vec[i64]]` + `Vec[Vec[i64]]` + `VecDeque[(i64, i64)]` runtime surface that the sieve + bucket + BFS algorithm requires — the 278.8 KiB sits well under Rust's 474.4 KiB despite Rust having tighter per-symbol size with `rustc -O`'s mature pipeline. The kāra binary is **post-`__TEXT,__jittmpl` segment re-scope** (karac `e76f42b`, 2026-05-25); pre-fix would have been ~294.7 KiB.

### Runtime memory (peak)

| Implementation | Peak |
|---|---|
| c    bfs_sieve  | 82.0 MiB |
| **kāra bfs_sieve (codegen)** | **59.9 MiB** |
| rust bfs_sieve  | 60.1 MiB |
| go   bfs_sieve  | 102.5 MiB |
| py   bfs_sieve  | 133.1 MiB |

Kāra is **at parity with Rust** and **27% under C** on peak RSS — the difference traces to kara's `Map` using a tighter chained-hash table layout than the C mirror's typedef'd `struct HashEntry[1<<20]` direct-addressed array (a hand-optimization the C mirror uses to avoid implementing chaining). The bench's working set is dominated by the `factors: Vec[Vec[i64]]` table at `cap = 10⁶` (~48 MiB the kata's commentary calls out); the remaining ~12 MiB is the bucket + BFS queue + visited flags.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| **`karac build bfs_sieve.kara`** | **10.8 MiB** |
| `rustc -O bfs_sieve.rs`          | 45.5 MiB |
| `clang -O3 bfs_sieve.c`          | 2.6 MiB |

Kāra's compile-memory footprint is ~4.2× clang's and ~4.2× lower than rustc's on this kata.
