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

## Planned

- `bench/` parity workload — large `nums` (e.g., `n = 50_000` with values seeded to maximize teleport activity) plugged into a hyperfine harness alongside the existing `bfs_sieve.rs` sibling.
