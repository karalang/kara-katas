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
| BFS + merged-factors sieve + per-prime bucket | O(n + cap log log cap) time, O(n + cap · ω̄) space | [`bfs_sieve.kara`](bfs_sieve.kara) ✓ via `karac run` (spec-canonical, no workarounds) | [`bfs_sieve.py`](bfs_sieve.py) ✓ |

`✓` runs end-to-end today.

### Status

- **`karac run` (interpreter): RUNS, spec-canonical** — Kāra and Python both emit `2 / 2 / 3 / 0` for the four test cases. Source is in its spec-canonical shape as of 2026-05-10 — every workaround from prior rounds has been retired against the corresponding interpreter fix. See "Workaround history" below for the audit trail.
- **`karac build` (codegen): UNVERIFIED** — the current `karac` binary is built without the `llvm` feature; `karac build` reports "requires the llvm feature; falling back to type check." The originally-recorded `compile_slice_index` panic at `src/codegen.rs:12015` (the `nums: Slice[i64]` parameter not registered in `slice_elem_types`, tracked as sub-item (h)) cannot be exercised from this binary. Re-test once `karac` is rebuilt with `--features llvm`.

### Workaround history

Five source-level workarounds have been retired across the LeetCode 3629 fix rounds. The kata file is now spec-canonical against the documented Kāra surface.

| # | Workaround that was applied | Replaced by | Cleared by |
|---|---|---|---|
| 1 | `for k in 0..n { let v = nums[k]; ... }` index loop | `for v in nums.iter() { ... }` | `Slice[T]` Iterator impl (round-2 sub-item (g), wip-list2 Theme 6) |
| 2 | `for _ in 0..n { visited.push(false); }` + `for _ in 0..=cap { factors.push(Vec.new()); }` init loops | `Vec.filled(n, false)` + `Vec.filled(cap + 1, Vec.new())` | `Vec.filled(n, val)` interpreter dispatch (commit `17f7c34`); the nested-Vec form additionally required a deep-clone fix in `eval_vec_filled` so each slot gets independent `Arc<RwLock<...>>` storage |
| 3 | `let mut j = i; while j <= cap { ... j = j + i; }` step-by loop | `for j in (i..=cap).step_by(i) { ... }` | `Range` / `RangeInclusive` Iterator impl (commit `c18fbec`) |
| 4 | `let prev = visited[i - 1]; if prev == false { ... }` materialization for OOB guard | `if i > 0 and not visited[i - 1] { ... }` | `and` / `or` short-circuit (commit `c6bddc9`) — interpreter + codegen both fixed |
| 5 | `let smallest_prime = if v >= 2 { factors[v][0] } else { 0 }; if v >= 2 and smallest_prime == v` materialization for empty-Vec guard | `if v >= 2 and factors[v][0] == v { ... }` | `and` / `or` short-circuit (commit `c6bddc9`) |
| 6 | `Vec[(i64, i64)]` + head cursor for BFS frontier | `VecDeque[(i64, i64)]` with `push_back` / `pop_front` | `VecDeque[T]` user-facing prelude (commit `4227e21`) |

The original round-3 diagnoses for workarounds #4 and #5 (auto-deref through indexed access) were ultimately wrong — those proved to work in isolation. The real blocker was non-short-circuiting `and`/`or` reaching an out-of-bounds slot and crashing the inner `not` / `==` on the resulting sentinel. The `c6bddc9` fix landed both the interpreter and codegen short-circuit machinery in lockstep.

`Vec.filled` shipped with a deep-clone helper (`deep_clone_value`) so nested-collection element types (`Vec[Vec[i64]]`, `Vec[Map[K,V]]`, …) get independent storage per slot. Without it, the interpreter's `Arc<RwLock<...>>` storage would alias every slot to the same underlying Vec — silently wrong, especially for sieve-style code where each `factors[k]` must be its own append target.

### Why a sieve + bucket?

Naive teleport expansion is O(n²): when many entries share a common prime factor (e.g., a `nums` full of even numbers), each visit to a prime-valued index would scan every other index for divisibility. The standard trick keeps BFS linear:

1. Build a **per-number prime-factor table**. `factors[k]` holds the ascending distinct prime factors of `k`. The same sieve pass that identifies primes also stamps each composite's distinct primes — one structure, no separate factorization step.
2. For every `j`, walk `factors[nums[j]]` and append `j` to `bucket[p]` for each prime `p`.
3. The first time BFS visits an index whose value *is* the prime `p` (detected by `factors[v][0] == v` — the smallest prime factor of a prime is itself), **drain `bucket[p]`** via `Map.remove`. That prime's whole bucket contributes at most once across the entire search.

The merged-factors variant (one `Vec[Vec[i64]]` table) was chosen over the textbook smallest-prime-factor sieve (`Vec[i64]` with a separate `distinct_prime_factors` helper) because it's tighter for *this* problem: the only number-theoretic queries we need are "is this prime?" and "what are its distinct prime factors?" — both direct lookups in `factors`. The textbook SPF version has lower memory (8 MB vs ~48 MB at `cap = 10⁶`) and is more reusable across other number-theoretic problems (Euler's totient, Möbius, divisor count); the merged table is simpler at the call site and removes one inner factorization loop. For LC 3629 specifically the simplicity wins; for a competitive-programming template the SPF version generalizes better.

Note: the LeetCode hint says "for each prime `p` dividing `nums[i]`," but the problem text is stricter — teleport only fires when `nums[i]` is itself prime. We follow the problem text. (Both formulations agree on the BFS layer count, since when `nums[i]` is prime, `nums[i]` is the only prime dividing it.)

## Kāra features exercised

`bfs_sieve.kara` exercises a representative cross-section of Kāra's collection machinery:

- **Nested Vec construction and access** — `Vec[Vec[i64]]` for the factor table, with `factors[i].is_empty()` and `factors[j].push(i)` for read/write through indexed access (the `IndexMut` dispatch path per `design.md:5165`).
- **Map with chained entry-or-insert-then-mutate** — `bucket.entry(p).or_insert(Vec.new()).push(j)`, the canonical insert-or-modify idiom from `design.md § Entry[K, V]`.
- **One-shot Map drain** — `match bucket.remove(v) { Some(indices) => ..., None => {} }` for consuming a prime's bucket exactly once.
- **`VecDeque[T]` as a BFS frontier** — `push_back` at the producer side, `pop_front` at the consumer side.
- **Tuple destructuring through indexed access** — `let (i, d) = queue[head]`.
- **`for ... in xs.into_iter()`** — owned consumption of the bucket's index list.
- **`Slice[i64]` parameter coercion** — test cases declared as `Array[i64, N]` flow into the slice parameter without explicit coercion.

No strings; no shared structs; no closures. The kata is deliberately a workout for nested collection ergonomics specifically.

## API shape

Each solution exposes a pure `min_jumps(nums) -> i64` (Python: `-> int`) and a thin `report` that prints. `main` calls `report` per test case. Logic is separate from I/O so the function is testable once a harness exists.

## Output format

One integer per line — the minimum jump count for each test case. Kāra and Python output is line-for-line identical so the files can be diffed directly.

```
2
2
3
0
```

## Running

```bash
# Kāra
karac run bfs_sieve.kara

# Python (3.10+ for PEP 604 union syntax)
python3 bfs_sieve.py
```

## Planned

- `bfs_sieve.rs` Rust sibling — once added, completes the {Kāra, Python, Rust} triad used elsewhere in the package.
- `bench/` parity workload — large `nums` (e.g., `n = 50_000` with values seeded to maximize teleport activity) so this kata can join the hyperfine harness alongside `1-two-sum`.
