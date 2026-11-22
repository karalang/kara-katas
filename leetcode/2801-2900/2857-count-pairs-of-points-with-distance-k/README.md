# 2857. Count Pairs of Points With Distance k

You are given a **2D** integer array `coordinates` and an integer `k`,
where `coordinates[i] = [xi, yi]` are the coordinates of the `ith`
point in a 2D plane.

We define the **distance** between two points `(x1, y1)` and `(x2, y2)`
as `(x1 XOR x2) + (y1 XOR y2)` where `XOR` is the bitwise `XOR`
operation.

Return *the number of pairs* `(i, j)` *such that* `i < j` *and the
distance between points* `i` *and* `j` *is equal to* `k`.

```
coordinates = [[1,2],[4,2],[1,3],[5,2]], k = 5            ->  2
coordinates = [[1,3],[1,3],[1,3],[1,3],[1,3]], k = 0      ->  10
```

**Constraints:** `2 <= coordinates.length <= 50000`; `0 <= xi, yi <=
10^6`; `0 <= k <= 100`.

## Approaches

| file | mechanism |
|---|---|
| `pairs.kara` ★ | the two XORs add up to k, so a point's partner differs from it by a in x and by k - a in y for some a from 0 to k; each point looks up its k + 1 candidates among the points before it, counted in a `Map[(i64, i64), i64]`, and is then counted itself |
| `pairs_sorted.kara` | no map: each point packed into one key, x * 2^21 + y, the keys sorted, and every point's k + 1 candidates counted by two `partition_point` searches; each pair is counted from both ends and, for k = 0, each point with itself, which come off before halving |
| `pairs_counts.kara` | all the points counted first in a `SortedMap`, then each distinct point with c copies met with its k + 1 candidates: c times the candidate's count, or c(c - 1) when it is the point itself, which only k = 0 allows; the sum, from both ends, halved |
| `pairs_rows.kara` | the points seen so far filed by row, a `Map` from x to a `Map` from y to a count, built with `entry(x).or_insert(Map.new())`; each point visits the rows x ^ a and looks for y ^ (k - a) in each |
| `pairs_solution.kara` | a Rust solution as LeetCode's Rust users write it: a `HashMap<(i32, i32), i32>` of the points seen, `for i in 0..=k` over the split, `cnt.get(&(x1, y1)).unwrap_or(&0)` added, and `*cnt.entry((x2, y2)).or_insert(0) += 1`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 4 lines: LeetCode's two examples; 50000
copies of one point, LeetCode's most, at k = 0, and 50000 points along
a line at k = 1; then 3000 random cases of 2 to 9 points in an 8 x 8
square with k up to 10, and 10 of 10^4 to 5 x 10^4 points with k up to
100, every other one in a 64 x 64 square and the rest up to 10^6, as a
total of pairs and a checksum. `pairs.py` mirrors the ★ arm and its
output is byte-identical.

```
2 10
1249975000 25000
3000 short cases: 3455 pairs, checksum 250773282
10 long cases: 15955284 pairs, checksum 671276077
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every pair i < j, its distance taken and compared with
k. It draws 2000 random cases of 2 to 12 points in a 16 x 16 square
with k up to 15, then 50 of up to 300 points with k up to 100, every
other one in a 64 x 64 square and the rest up to 10^6, all before any
arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the points in reverse order: the same answer |
| P3 | every x XORed with one mask and every y with another: the same answer |
| P4 | x and y swapped in every point: the same answer |
| P5 | the points given twice: four times the answer, and n more for k = 0 |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases, 6327 pairs: checksum 938928490,
61500 checks over 5 arms: 0 failures` under every lane in
Verification, and a Python reading of the same cases gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the split of k stopping one short | P1 203, P4 302, P5 139, P6 203 |
| M2 | ★: each point counted before it looks | P1 1003, P5 139, P6 1003 |
| M3 | sorted: keys packed too tight, x * 16 + y | P1 32, P3 29, P4 29, P5 18, P6 32 |
| M4 | sorted: each point's match with itself kept for k = 0 | P1 139, P5 139, P6 139 |
| M5 | counts: a point's copies paired with themselves too | P1 139, P5 139, P6 139 |
| M6 | counts: the partner's count taken once, not c times | P1 47, P5 864, P6 47 |
| M7 | rows: only the point's own row searched | P1 904, P4 907, P5 1911, P6 904 |
| M8 | rows: y moved by a, not k - a | P1 952, P5 1911, P6 952 |
| M9 | solution: y1 taken from x2 | P1 994, P2 766, P3 673, P4 620, P5 968, P6 994 |
| M10 | solution: a new point counted twice | P1 882, P2 37, P5 999, P6 882 |

## Benchmarks

The bench draws 10 cases of 50000 points, LeetCode's most, every other
one in a 256 x 256 square and the rest up to 10^6, with k up to 100,
all of them first, then answers each 3 times by the ★ arm in all five
languages. Kāra, Rust, Go and Python key a hash map by the point; C,
which has none, uses an open-addressing table of (x, y) keys with a
splitmix64 hash, cleared for every case. Every implementation prints
`10 cases of 50000 points, 3 rounds: 19626285 pairs, checksum
191932424`.

BENCHTAB

## Verification

All five arms print the same output as `pairs.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as first written. The differential's
literal reading took the two points as `let (p, q) = (coordinates[i],
coordinates[j])`, and `karac check` reported E0515 twice, a `Vec`
moved out of the collection that still owns it; `karac fix` wrote
`ref` before each, as the binding is only read.

LeetCode's Rust template took 22 `karac fix` edits in one run, the
wrapper included: `use std::collections::HashMap` became `struct
Solution {}`; `Vec<..>` and `HashMap<(i32, i32), i32>` became `Vec[..]`
and `Map[(i32, i32), i32]`; `HashMap::new` became `Map.new`; the two
`&`s in `cnt.get(&(x1, y1)).unwrap_or(&0)` went; `let mut ans = 0`
took `: i32`, the type the function returns; `|&v|` lost its `&`;
`Solution::` took `.`, and the wrapper's `as i64` went, an `i32`
widening.
