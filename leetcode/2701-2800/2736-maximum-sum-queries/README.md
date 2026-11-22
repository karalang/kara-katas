# 2736. Maximum Sum Queries

You are given two **0-indexed** integer arrays `nums1` and `nums2`, each
of length `n`, and a **1-indexed 2D array** `queries` where `queries[i] =
[x_i, y_i]`.

For the `i`-th query, find the **maximum value** of `nums1[j] +
nums2[j]` among all indices `j` `(0 <= j < n)`, where `nums1[j] >= x_i`
and `nums2[j] >= y_i`, or **-1** if there is no `j` satisfying the
constraints.

Return *an array* `answer` *where* `answer[i]` *is the answer to the*
`i`-th *query.*

```
nums1 = [4, 3, 1, 2], nums2 = [2, 4, 9, 5], queries = [[4, 1], [1, 3], [2, 5]]  ->  [6, 10, 7]
nums1 = [3, 2, 5],    nums2 = [2, 3, 4],    queries = [[4, 4], [3, 2], [1, 1]]  ->  [9, 9, 9]
nums1 = [2, 1],       nums2 = [2, 3],       queries = [[3, 3]]                  ->  [-1]
```

**Constraints:** `1 <= n <= 10^5`, `1 <= nums1[i], nums2[i] <= 10^9`,
`1 <= queries.length <= 10^5`, `1 <= x_i, y_i <= 10^9`.

## Approaches

| file | mechanism |
|---|---|
| `queries.kara` ★ | offline: the pairs sorted by nums1 falling and the queries by x falling, so each query sees exactly the pairs let in before it. The pairs let in are kept on a stack with nums2 rising and sums falling: a pair whose nums2 is no more than the top's is beaten by the top and dropped, otherwise it pops every top whose sum it reaches. A query's answer is the first entry with nums2 >= y, by binary search. O((n + q) log(n + q)) |
| `queries_scan.kara` | each query looks at every pair, by `filter`, `map` and `max`, with `unwrap_or(-1)`. O(n q) |
| `queries_fenwick.kara` | offline as the ★ arm; the nums2 values ranked highest first, and a Fenwick tree over the ranks keeps the largest sum of each prefix, so "nums2 >= y" is a prefix of ranks. O((n + q) log n) |
| `queries_segment.kara` | online, in the queries' own order: a merge-sort tree over the pairs sorted by nums2, each node holding its pairs sorted by nums1 with suffix maxima of sums in a `struct Node`; a query takes the O(log n) nodes covering nums2 >= y and binary-searches nums1 >= x in each. O(n log^2 n) to build, O(log^2 n) a query |
| `queries_solution.kara` | a Rust solution as LeetCode's Rust users write it, `into_iter().zip`, `sort_unstable_by`, a `Vec<(usize, i32, i32)>` of queries, `while let Some(&(_, ts)) = st.last()` and `partition_point`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 5 lines: LeetCode's three examples; 1000
random cases of 1 to 20 pairs and 1 to 20 queries with values up to 30;
and 10 cases of 2000 pairs and 2000 queries with values up to `10^9`,
each batch with the sum of its answers and a checksum. `queries.py`
mirrors the ★ arm and its output is byte-identical.

```
[6, 10, 7]
[9, 9, 9]
[-1]
1000 small cases: answers sum to 369143, checksum 768440007
10 cases of 2000 pairs: answers sum to 39137699138460, checksum 604638929
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: each query answered by trying every index, in a plain loop.
It draws 600 random cases of 1 to 15 pairs and queries with values up to
20, then 100 of up to 300 with values up to `10^9`, all before any arm
answers.

| | property |
|---|---|
| P1 | the answers are the literal reading's |
| P2 | the pairs listed in reverse order: the same answers |
| P3 | the queries listed in reverse order: the answers reversed |
| P4 | nums1 and nums2 swapped, and each query's x and y: the same answers |
| P5 | each answer is -1 or at least x + y; and a query of (1, 1) added at the end answers the largest sum of all |
| P6 | each arm agrees with at least three of the other four |

The differential prints `700 cases: checksum 487556542, 21000 checks over
5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. M2 and M7 fail the same checks, both leaving
out a pair whose nums1 is exactly x; so do M3, M6 and M9, each leaving
out one whose nums2 is exactly y.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the top's sum answered, not the first that reaches y | P1 306, P4 437, P5 351, P6 306 |
| M2 | ★: pairs with nums1 equal to x left out | P1 199, P4 306, P5 1, P6 199 |
| M3 | scan: nums2 equal to y left out | P1 208, P4 306, P5 1, P6 208 |
| M4 | scan: 0 for none | P1 550, P5 550, P6 550 |
| M5 | fenwick: each pair put one rank too low | P1 446, P4 492, P5 50, P6 446 |
| M6 | fenwick: values equal to y left out | P1 208, P4 306, P5 1, P6 208 |
| M7 | segment: nums1 equal to x left out | P1 199, P4 306, P5 1, P6 199 |
| M8 | segment: each leaf's sum taken as its nums1 | P1 657, P4 630, P5 700, P6 657 |
| M9 | solution: nums2 equal to y skipped | P1 208, P4 306, P5 1, P6 208 |
| M10 | solution: pairs let in by nums2, not nums1 | P1 537, P2 93, P4 583, P5 21, P6 537 |

## Benchmarks

The bench draws 10 cases of `10^5` pairs and `10^5` queries, LeetCode's
most, with values up to `10^9`, all of them first, then answers each 3
times by the ★ arm in all five languages. C sorts with `qsort`, Go with
`slices.SortStableFunc`, and Rust and Kāra with `sort_by`; the order of
equal keys does not change any answer. Every implementation prints `10
cases of 100000 pairs and queries, 3 rounds: answers sum to
5989363080311121, checksum 946147484`.

BENCHTAB

## Verification

All five arms print the same output as `queries.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as first written.

LeetCode's Rust template took one `karac fix` of 42 edits, the wrapper
included: `struct Solution {}` added; `nums1` and `nums2` became `own`
parameters, since `into_iter()` consumes them; `sort_unstable_by` became
`sort_by` and `cmp(&x.0)` lost its `&`; `usize` in the queries' tuple
became `i64`; `vec![-1; queries.len()]` became `Vec.filled(..)`; `while
let Some(&(_, ts)) = st.last()` became `while let Some((_, ts)) =
st.last().cloned()`; the `&(b, _)` and `&v` patterns dropped their `&`;
`&&` and `||` became `and` and `or`; and `Solution::` became `Solution.`.
