# 57. Insert Interval

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array &nbsp;·&nbsp; **Source:** [leetcode.com/problems/insert-interval](https://leetcode.com/problems/insert-interval/)

Given a list of closed intervals `[(start, end), ...]` already sorted by `start` and pairwise non-overlapping, plus one new interval, insert the new interval and merge any it overlaps (or touches — closed-interval semantics: `[1,3]` and `[3,5]` merge into `[1,5]`). Return the disjoint union in start order.

```
([(1,3),(6,9)], (2,5))                        → [(1,5), (6,9)]
([(1,2),(3,5),(6,7),(8,10),(12,16)], (4,8))   → [(1,2), (3,10), (12,16)]
([], (5,7))                                    → [(5,7)]
```

**Constraints:** `0 ≤ intervals.length ≤ 10^4`, `-10^5 ≤ start_i ≤ end_i ≤ 10^5`, input sorted by `start` with no overlap.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| **Linear three-phase sweep** — emit the left run, absorb the overlap window into the new interval, emit the right run | O(n) time, O(n) output | [`insert_interval.kara`](insert_interval.kara) ✓ via `karac run` / `karac build` | [`insert_interval.py`](insert_interval.py) ✓ |
| **Binary-search the merge window** — bisect for the first/last interval the new one touches, then splice | O(log n + k) search + O(n) copy | [`insert_interval_binary.kara`](insert_interval_binary.kara) ✓ | — |
| **Reduce to Merge Intervals** — push the new interval, sort by `start`, run the kata-56 sweep | O(n log n) | [`insert_interval_sort.kara`](insert_interval_sort.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter and codegen produce identical output across all ten test cases, and all three approaches agree with each other and with the Python mirror.

## Why three phases?

The input is already sorted by `start` and disjoint, so the answer is the concatenation of three contiguous runs:

```
[ intervals that end before new_start ]  ++  [ one merged interval ]  ++  [ intervals that start after new_end ]
        left run — untouched                    the overlap window              right run — untouched
```

The **linear** solution walks left-to-right and switches phase as it goes: push while `cur.end < new_start`, then absorb while `cur.start <= new_end` (widening `new_start`/`new_end` to `min`/`max`), then push the rest. The `<=` in the absorb test is what enforces closed-interval touching — `[1,3]` + new `[3,6]` merge because `3 <= 3`; flipping to `<` gives half-open behavior. Pinned by test cases 6 + 7.

The two guards in the absorb phase (`cur.0 < new_start` and `cur.1 > new_end`) are both needed for the **nested** case: new `[3,5]` inside existing `[1,10]` must leave the window at `[1,10]`, not shrink it to `[3,5]`. Pinned by test case 8 — the case that catches the bug if either guard is dropped.

The **binary-search** solution ([`insert_interval_binary.kara`](insert_interval_binary.kara)) notes that both phase boundaries are monotone predicates over sorted data, so each can be found by a lower-bound bisect instead of a linear scan: `lo = first i with intervals[i].end >= new_start`, `hi = first i with intervals[i].start > new_end`. The window is exactly `intervals[lo .. hi]`; the search is O(log n), the copy O(n). Kāra v1 has no predicate `partition_point`, and `Slice.binary_search` searches for an *equal key* rather than a partition point (its codegen path is integer/String-element-only anyway — tuple elements fall to an interpreter-only Err), so the two bisects are written out with the canonical `while lo < hi { mid = lo + (hi-lo)/2; ... }` lower-bound loop.

The **sort** solution ([`insert_interval_sort.kara`](insert_interval_sort.kara)) throws the precondition away and reduces to [kata #56](../56-merge-intervals/): push the new interval, `sort_by(|a, b| a.0.cmp(b.0))`, sweep. Asymptotically worse, but the shortest correct answer and a useful independent cross-check.

## Kāra features exercised

- **`Slice[(i64, i64)]` parameter + `Vec[(i64, i64)]` output** — the tuple-typed collection shape from [kata #56](../56-merge-intervals/); `Vec.push((new_start, new_end))` builds tuple literals, `Vec.from_slice(intervals)` copies (sort variant).
- **Tuple field access on an index result** — `intervals[i].0` / `.1`, i.e. `.N` indexing on the value produced by `Slice`-index. Both the let-bound form (`let cur = intervals[i]; cur.1`) and the fully inline form (`intervals[i].1` inside a `while` condition) lower correctly on interpreter *and* codegen — the index-then-field placeholder trap does **not** fire for tuple elements here, which this kata verifies directly.
- **`Vec[(i64, i64)].sort_by(|a, b| a.0.cmp(b.0))`** (sort variant) — sort by primary tuple component, routed through karac's Slice 6.4 integer-tuple mono sort path (the fix [kata #56](../56-merge-intervals/) triggered).
- **Manual lower-bound bisect** (binary variant) — `let mid = lo + (hi - lo) / 2i64` overflow-safe midpoint plus the branch-on-predicate loop; pure i64 index arithmetic over a sorted `Slice`.
- **`break` out of a `while`** — the linear solution switches phase by `break`-ing the current loop when its predicate fails, rather than folding the condition into the `while` header; same control-flow shape as an early `return`.
- **Empty-`Array` literal with explicit length** — `let case3: Array[(i64, i64), 0] = [];` exercises the zero-length array-to-slice path (the "insert into nothing" edge case).

## Running

```bash
# Kāra — interpreter and codegen produce the same output today.
karac run   insert_interval.kara
karac build insert_interval.kara && ./insert_interval

# The two alternative approaches (identical output):
karac run insert_interval_binary.kara
karac run insert_interval_sort.kara

# Python
python3 insert_interval.py

# Verify they all agree
diff <(karac run insert_interval.kara)        <(python3 insert_interval.py)        && echo OK
diff <(karac run insert_interval.kara)        <(karac run insert_interval_binary.kara) && echo OK
diff <(karac run insert_interval.kara)        <(karac run insert_interval_sort.kara)   && echo OK
```

## Benchmarks

_Follow-up._ The 5-language benchmark harness (Kāra / Rust / C / Go / Python mirrors + `bench.sh` + `results.json`) that the rest of the corpus carries is not yet authored for this kata. The workload shape would mirror [kata #56](../56-merge-intervals/) (M distinct cases × K=1M outer iterations, sinking the running total of returned `Vec` lengths), with the added lever that this kata's **binary-search** solution turns the per-call left-scan from O(n) into O(log n) — the natural quantity to measure against the O(n) linear sweep at larger N.
