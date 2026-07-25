# 347. Top K Frequent Elements

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Hash Map, Sorting, Counting &nbsp;·&nbsp; **Source:** [leetcode.com/problems/top-k-frequent-elements](https://leetcode.com/problems/top-k-frequent-elements/)

Given an integer array `nums` and an integer `k`, return the `k` most frequent
elements.

```
nums = [1,1,1,2,2,3], k = 2  →  [1,2]
nums = [1],           k = 1  →  [1]
```

**Constraints:** `1 ≤ nums.length ≤ 10⁵`; `k` is in `[1, number of distinct
elements]`. LeetCode accepts the answer in **any order**; both implementations
here impose a total order — **count descending, then key ascending** — so the
output is deterministic and directly diffable against the oracle.

## Approaches

Both files run the *same* three steps: tally into a `Map`, recover the distinct
keys with a `keys()` walk, insertion-sort by `(count desc, key asc)`, take `k`.
Only the map's halves differ, and that is the entire point.

| Approach | File | Map halves |
|---|---|---|
| **Scalar-keyed** ★ | [`top_k_frequent.kara`](top_k_frequent.kara) | `Map[i64, i64]` — both halves scalar |
| String-keyed | [`top_k_frequent_words.kara`](top_k_frequent_words.kara) | `Map[String, i64]` — heap key half |
| Reference oracles | [`top_k_frequent.py`](top_k_frequent.py), [`top_k_frequent_words.py`](top_k_frequent_words.py) | known-correct answers |

## Why this kata

Chosen by **compiler surface, not sequence** — and specifically to put live
coverage under an **open** ledger entry.

`keys()` lowers two different ways depending on the map's halves. When both
halves are scalar it becomes an inline bucket walk with no runtime iterator
call (ledger B-2026-07-24-2, `bef6bbc`). When either half is heap-allocated it
does not, and still materializes an intermediate keys Vec — **B-2026-07-25-4,
still open**.

Until now the corpus only covered the fast side (#387 exercises scalar
`keys()`). This kata covers both halves of that fork with one algorithm, so the
two files must agree on every answer; any divergence is a compiler bug rather
than an algorithm difference.

The split is visible in the linked binaries — the scalar build never pulls the
runtime iterator in at all:

```console
$ nm top_k_frequent       | grep -c karac_map_iter     # scalar halves
0
$ nm top_k_frequent_words | grep -c karac_map_iter     # heap key half
3     # karac_map_iter_new / _next / _free
```

No new bugs surfaced. Both variants were correct on the first compile and agree
with their oracles across all four surfaces, which is the useful signal: the
heap-half path is *slow*, not *wrong*.

## Verification

| Surface | `top_k_frequent` | `top_k_frequent_words` |
|---|---|---|
| `karac run --interp` | ✅ | ✅ |
| `karac run` (LLJIT) | ✅ | ✅ |
| `karac build` (auto-par default) | ✅ | ✅ |
| `karac build` + `KARAC_AUTO_PAR=0` | ✅ | ✅ |

Eight checks, all byte-identical to the Python oracles — including the
count-tie cases (resolved by key ascending), the all-counts-equal case, and
`k` larger than the number of distinct keys.

## Kāra features exercised

- **`Map[i64, i64]` vs `Map[String, i64]`** — the same `insert` / `get` /
  `keys()` surface across the scalar and heap-half lowering fork.
- **`for k in counts.keys()`** feeding a `Vec` the loop then sorts in place.
- **Index assignment during insertion sort** (`vals[b + 1i64] = prev`) — the
  shift-right idiom, on both `Vec[i64]` and `Vec[String]`.
- **`break` out of a `while`** as the insertion-sort inner-loop exit.
- **`not` for boolean negation** (Kāra rejects `!`).
- **`.clone()` on `String` map keys** — required where a key is both looked up
  and inserted, and where a `Vec[String]` element is read out while the vector
  stays live.
- **`String.new()` + `+` accumulation** with f-string interpolation to render
  the result list.
