# 373. Find K Pairs with Smallest Sums

Given two integer arrays `nums1` and `nums2`, each sorted in non-decreasing
order, and an integer `k`, return the `k` pairs `(u, v)`, with `u` from
`nums1` and `v` from `nums2`, that have the smallest sums.

```
nums1 = [1, 7, 11], nums2 = [2, 4, 6], k = 3   -> [(1, 2), (1, 4), (1, 6)]
nums1 = [1, 1, 2], nums2 = [1, 2, 3], k = 2    -> [(1, 1), (1, 1)]
```

**Constraints:** `1 <= nums1.length, nums2.length <= 10^5`;
`-10^9 <= nums1[i], nums2[i] <= 10^9`; both arrays sorted;
`1 <= k <= 10^4`; `k <= nums1.length * nums2.length`.

## Approaches

Think of the pairs as a grid, row `i` being `nums1[i]` with every
`nums2[j]`. Each row's sums rise left to right and each column's rise top
to bottom. LeetCode accepts ties in any order; every arm here returns the
pairs in `(sum, i, j)` order, so all four print the same thing.

| file | mechanism | time |
|---|---|---|
| `k_smallest_pairs.kara` ★ | the next smallest pair is always the front of some row: keep each of the first `k` rows' fronts in a `PriorityQueue` of `(sum, i, j)`, pop the least, and push that row's next pair | O(k log min(k, n1)) |
| `k_smallest_pairs_lazy.kara` | start from `(0, 0)` alone; pop the least pair and push `(i, j + 1)`, and also `(i + 1, 0)` when `j = 0`; every pair has exactly one parent that comes before it, so each is pushed once | O(k log k) |
| `k_smallest_pairs_threshold.kara` | binary search the `k`-th smallest sum, counting the pairs at most a bound with two pointers; take every pair below it and enough pairs equal to it, then sort | O((n1 + n2) log R + p log p), `R` the range of sums and `p` the pairs at most the bound |
| `k_smallest_pairs_merge.kara` | a `k`-way merge of the first `k` rows with a column pointer per row, scanning the rows for the least front at each step | O(k · min(k, n1)) |
| `differential.kara` | the four arms against an oracle that sorts every pair, 60,000 checks, five properties | — |

`PriorityQueue.new()` pops the smallest element first, so the heap arms
need no `Reverse` wrapper as Rust's `BinaryHeap` would, and a tuple's
ordering gives the `(sum, i, j)` tie-break for free.

Every arm prints the same 11 lines: the two LeetCode examples, eight edge
cases (`k` above the number of pairs, `k = 1`, every pair, negative
values, all values equal, one row, one column, values at the bounds), and
the pair count and a checksum over 300 random cases with arrays of up to
300 values and `k` up to 2,000. `k_smallest_pairs.py` mirrors the ★ arm
with `heapq` and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms. The oracle builds every
pair, sorts the `(sum, i, j)` triples and keeps the first `k`. The test
draws 3,000 cases with arrays of up to 10 values, one in 50 with `nums1`
empty, and `k` up to three more than the number of pairs. Half the cases
draw values that rise by 0, 1 or 2, so equal values and equal sums are
common.

| | property |
|---|---|
| P1 | each arm gives the oracle's pairs, in order |
| P2 | each arm gives `min(k, n1 · n2)` pairs |
| P3 | the sums never fall, and every pair takes its first value from `nums1` and its second from `nums2` |
| P4 | swapping the arrays gives the same sums |
| P5 | the answer for `k - 1` is the answer for `k` without its last pair |

It prints `3000 cases, 60000 checks, 0 failures` under `karac __mir-run`,
`karac run --interp`, LLJIT, `karac build` and `KARAC_AUTO_PAR=1 karac
build`.

## Mutation testing

Eight edits to the copies inside `differential.kara`, each run under
`karac __mir-run`. Seven are killed; M3 survives because it is equivalent.

| # | mutation | how |
|---|---|---|
| M1 | front: the next pair is pushed with the old pair's sum | P1, P3 and P4, 6529 failures |
| M2 | lazy: pushes the next row's front from every pair, not only from column 0 | P1 to P4, 6071 failures |
| M3 | threshold: the search wants more than `k` pairs at the bound | survives |
| M4 | threshold: the count leaves out sums equal to the bound | P1, P2 and P5, 1997 failures |
| M5 | threshold: adds no pairs equal to the bound | P1, P2 and P5, 7510 failures |
| M6 | merge: a tie goes to the later row | P1, 1195 failures |
| M7 | merge: a row stops one column before its end | P1, P2 and P4, 5270 failures |
| M8 | oracle: never sorts | P1, 8596 failures |

M3 changes the binary search to find the least bound with more than `k`
pairs at or below it. When exactly `k` pairs are at most the `k`-th sum,
that moves the bound up to the next sum, but then the pairs strictly
below the new bound are exactly those `k`, and none at the bound are
added; in every other case the bound does not move. The answer is the
same either way.

## Verification

All four arms print the same output as `k_smallest_pairs.py` under
`karac run --interp`, `karac __mir-run` (the v2 MIR interpreter), LLJIT,
`karac build` and `KARAC_AUTO_PAR=1 karac build`.

## Benchmarks

The bench program answers 20 random pairs of sorted arrays of 100,000
values each with `k = 10,000`, the problem's largest, using the ★ arm. The
C mirror has a hand-written heap of triples ordered as tuples, Rust wraps
its `BinaryHeap` entries in `Reverse`, and Go uses `container/heap`. The
Kāra build and all four mirrors print `checksum 904034364`. Timings are
not taken yet; they need a quiet machine.

## Compiler findings

None.
