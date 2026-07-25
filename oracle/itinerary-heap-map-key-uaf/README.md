# itinerary-heap-map-key-uaf

**Compiler-behavior demonstration — an OPEN, high-severity codegen bug.**
Sibling of the (now fixed) `recursive-owned-string-param-uaf`, and *not* closed
by that fix.

[`repro.kara`](repro.kara) is the natural LeetCode #332 Reconstruct Itinerary
solution — Hierholzer over a `Map[String, Vec[String]]`. [`oracle.py`](oracle.py)
is the reference implementation of the same algorithm.

| Surface | Result |
|---|---|
| `karac run --interp` | ✅ matches `oracle.py` exactly |
| `karac run` (LLJIT) | 💥 aborts in `karac_string_clone` — `ptr::copy_nonoverlapping` precondition violated |
| `karac build` | ❌ interior itinerary entries are freed-buffer garbage |
| `karac build` + `KARAC_AUTO_PAR=0` | ❌ same garbage |

Expected (all four surfaces should print this):

```
JFK -> MUC -> LHR -> SFO -> SJC
JFK -> ATL -> JFK -> SFO -> ATL -> SFO
JFK -> ATL -> JFK -> SFO -> ATL -> SFO
JFK -> AAA
```

Observed under `karac build` (first case): `JFK -> JFK -> JFK -> JFK -> SJC` —
first and last entries survive, the interior collapses.

## What is already ruled out

Each piece works in isolation under `karac build`; only the whole chain fails.

| Isolated piece | Result |
|---|---|
| Graph build alone (`adj.get(froms[i])` → `push` → `adj.insert(froms[i], d)`) | ✅ correct |
| Sort pass alone (read each key's `Vec`, `sort()`, write back) | ✅ correct |
| The fixed `recursive-owned-string-param-uaf` repro (same `visit`, **literal** map keys) | ✅ correct since B-2026-07-25-1 |

`route` is **already corrupt inside `find_itinerary`**, immediately after
`visit` returns — before the reversal and before the `show` string concat, so
neither of those is implicated.

## The one structural difference from the fixed sibling

The fixed repro seeded its map from **string literals** in `main`
(`adj.insert("JFK", a)`) — rodata keys with `cap == 0`. Here the keys are
`froms[i]`, **heap** `String` elements read out of a `ref Vec[String]`
parameter. That is the leading hypothesis for the residual defect, not a
conclusion: it is the difference, but it has not been shown to be the cause.

Tracked in the sibling `kara` repo as ledger **B-2026-07-25-3**. LeetCode #332
stays out of the kata corpus until this is fixed — its build output would
violate the repo's *A/B run == build* invariant.
