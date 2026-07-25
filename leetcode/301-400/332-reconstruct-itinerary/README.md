# 332. Reconstruct Itinerary

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** Graph, Eulerian Path, DFS, Hash Map &nbsp;·&nbsp; **Source:** [leetcode.com/problems/reconstruct-itinerary](https://leetcode.com/problems/reconstruct-itinerary/)

Given a list of airline tickets `[from, to]`, reconstruct the itinerary in
order. All tickets belong to a man who departs from `JFK`, so the itinerary must
begin there. If multiple valid itineraries exist, return the one that is
**lexicographically smallest** when read as a single string.

```
[["MUC","LHR"],["JFK","MUC"],["SFO","SJC"],["LHR","SFO"]]
  →  JFK -> MUC -> LHR -> SFO -> SJC

[["JFK","SFO"],["JFK","ATL"],["SFO","ATL"],["ATL","JFK"],["ATL","SFO"]]
  →  JFK -> ATL -> JFK -> SFO -> ATL -> SFO
```

**Constraints:** `1 ≤ tickets.length ≤ 300`; airport codes are three uppercase
letters; at least one valid itinerary always exists.

## Approach — Hierholzer, not backtracking

Every ticket is an edge that must be used exactly once, so the itinerary is an
**Eulerian path**. The naive reading ("try every ordering, keep the smallest")
is exponential; Hierholzer's algorithm is linear:

1. Bucket destinations per origin and **sort each bucket** — visiting in sorted
   order is what makes the result lexicographically smallest.
2. Walk greedily along unused edges, keeping a per-airport cursor into its
   sorted bucket.
3. Emit each airport only once it becomes a **dead end**, then reverse. The
   post-order emission is what handles the case where the greedy walk strands
   itself before consuming every ticket.

The third case in `main` is the one that punishes a naive implementation: the
greedy walk reaches `SFO` with tickets still unused, and only the post-order
emission recovers the correct answer.

## Why this kata — nested heap-owning collections

`Map[String, Vec[String]]` is the densest ownership shape in the corpus: a map
whose values are vectors whose elements are heap strings, mutated in place
(read bucket → push → write back), re-read under recursion, and with an owned
`String` parameter that outlives the recursive descent.

That combination found a **high-severity use-after-free** in `karac`
(**B-2026-07-25-1**, now fixed). An owned `String` parameter consumed twice in
one function — `cursor.insert(airport, …)` inside the loop, then
`route.push(airport)` after the descent — had its header `cap` zeroed by the
first consume, which is the ownership bit the second consume reads. Seeing
`cap == 0`, the second consume took the parameter for a borrowed view, skipped
its defensive copy, and stored a raw alias into a buffer that died when the
recursive call returned. Silent garbage under `karac build`, an abort inside
`karac_string_clone` under the LLJIT, correct under the interpreter.

The kata was held out of the corpus until that was fixed, and the reduced
version lives on as [`oracle/recursive-owned-string-param-uaf`](../../../oracle/recursive-owned-string-param-uaf/)
with its ablation set.

## Verification

| Surface | Result |
|---|---|
| `karac run --interp` | ✅ matches `reconstruct_itinerary.py` |
| `karac run` (LLJIT) | ✅ |
| `karac build` (auto-par default) | ✅ |
| `karac build` + `KARAC_AUTO_PAR=0` | ✅ |

## Kāra features exercised

- **`Map[String, Vec[String]]` read-modify-write** — `adj.get(k)` into a local
  `Vec`, `push`, then `adj.insert(k, d)` back.
- **`Map.keys()` + `Vec[String].sort()`** — the per-bucket lexicographic sort.
- **Recursion with an owned `String` parameter** used after the descent.
- **`match` on `Option` with a `Vec.new()` fallback arm** — which is also what
  surfaced **B-2026-07-25-2** (match arms not binding a type variable from the
  sibling arm).
- **`mut ref` parameters** on a free function, with call-site `mut` markers.

---

**Bug ledger:** this kata surfaced `B-2026-07-25-1` (high, fixed) and
`B-2026-07-25-2` (fixed) — see the [`karac` bug ledger](../../../../kara/docs/bug-ledger.md).
