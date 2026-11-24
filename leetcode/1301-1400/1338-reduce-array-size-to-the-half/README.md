# 1338. Reduce Array Size to The Half

You are given an integer array `arr`. You can choose a set of integers
and remove all the occurrences of these integers in the array. Return the
minimum size of the set so that at least half of the integers of the
array are removed.

```
arr = [3,3,3,3,5,5,5,2,2,7]  ->  2
arr = [7,7,7,7,7,7]          ->  1
```

**Constraints:** `2 <= arr.length <= 10^5`, `arr.length` is even, `1 <=
arr[i] <= 10^5`.

The arms are `fn min_set_size(arr: Vec[i32]) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `min_set_size.kara` ★ | each value counted in a `Map` with `counts[x] = counts.get(x).unwrap_or(0) + 1`; the counts sorted largest first, and the values taken, most frequent first, until at least half the array is gone. O(n log n) |
| `min_set_size_bucket.kara` | no map and no sort: each value counted in an array indexed by value, then each count tallied by how many values have it, and the counts walked from the largest possible down. O(n + largest value) |
| `min_set_size_heap.kara` | the counts from a `Map` filled by `entry(x).or_insert(0)` poured into `PriorityQueue.max_first_from`, which builds the heap in one pass, and popped until at least half the array is gone. O(n + k log k) for k distinct values |
| `min_set_size_runs.kara` | a sorted copy of the array, where each value's copies stand together, read as runs; the run lengths sorted largest first and taken until half is gone. O(n log n) |
| `min_set_size_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `HashMap<i32, i32>` filled by `*m.entry(x).or_insert(0) += 1`, `into_values()` collected and sorted largest first with `sort_unstable_by(\|a, b\| b.cmp(a))`, and the first place where the running total reaches half returned from an `enumerate`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's two examples, two
different values, and two pairs (`2 1 1 1`); 10^5 values, the
constraints' longest, all different and drawn at random from 1 to 10^5
(`10^5 values: 50000 9725`); and 400 random arrays of 2 to 3000 values,
an even count, most of them short, from 1 to 3, to 50 or to 10^5, half
of them skewed toward small values (`400 random arrays: checksum
418839902`). `min_set_size.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run` and `karac __mir-llvm-run`. A `Map`'s walk order is random
per run, so every arm that reads a `Map` sorts its counts before using
them.

The Mend loop: the four Kāra arms check clean. The Rust arm takes one
round of 17 fixes by `karac fix`'s count, from 10 errors: the `use
std::collections::HashMap;` line deleted, `struct Solution;` to `struct
Solution {}`, each `Vec<..>` to `Vec[..]`, `HashMap<i32, i32>` and
`HashMap::new()` to `Map[i32, i32]` and `Map.new()`, `for &x` and `(i,
&c)` to `for x` and `(i, c)`, `sort_unstable_by` to `sort_by`, and
`Solution::` to `Solution.`. Its output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every set of the values the array holds is tried, as a bit
mask over the distinct values, and the smallest set whose removal takes
away at least half the array is kept. 2000 arrays of 2, 4, 6 or 8 values
in four kinds, 500 each: from 1 to 3; from 1 to 8; all different; and
one value making up half or one short of half, the rest from 1 to 5.
Each array is shuffled, so equal values do not always stand together,
and drawn before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the array read backwards: the same answer |
| P3 | every value x made the largest + 1 - x: the same answer |
| P4 | the array twice over: the same answer |
| P5 | as many copies of one new value added as the array has values: one |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 arrays: checksum 120721736,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run` and `karac __mir-llvm-run`. Python, counting with a `Counter`, gives
the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash, and no two
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the counts taken smallest first | P1 917, P5 1907, P6 3668 |
| M2 | ★: each value taken as one copy | P1 1027, P4 1289, P5 2000, P6 4108 |
| M3 | bucket: stopped two short of half | P1 1176, P4 1176, P6 1176 |
| M4 | bucket: a count taken never used up | P1 4, P6 4 |
| M5 | heap: every count one too many | P1 673, P4 533, P6 673 |
| M6 | heap: exactly half not enough | P1 1471, P5 2000, P6 1471 |
| M7 | runs: the runs taken by value, largest value first | P1 551, P3 675, P6 551 |
| M8 | runs: each run measured from the array's start | P1 735, P6 735 |
| M9 | solution: the set's size counted from 0 | P1 2000, P5 2000, P6 2000 |
| M10 | solution: a quarter taken for half | P1 735, P4 136, P6 735 |

P1 and P6 kill all ten, P4 four, P5 four, P3 one and P2 none. The flood
of one new value (P5) has a one-value answer, which catches the edits
that take the smallest count first (M1), count values instead of copies
(M2), need more than half (M6), or count from 0 (M9). The array twice
over (P4) doubles every count but not a fixed error, so it catches the
edits off by a constant: two short of half (M3), a count one too many
(M5), each value one copy (M2), and a quarter for half (M10), whose
rounding changes. Turning the values over (P3) catches only the run walk
that goes by value (M7), and reading backwards (P2) nothing, since no arm
here cares where a value stands. M4 is the weakest: taking the largest
count again changes the answer only when three or more values are
needed, since two copies of a count below half still fall short or
reach half as the true second count does, and only 4 of the 2000 short
arrays need three values that way.

## Benchmarks

The bench builds 20 arrays of 10^5 values, the constraints' longest,
alternately from 1 to 10^5 and from 1 to 1000, once; then makes 30
passes, each setting one value of every array from the checksum so far,
so no answer carries over, answering every array with the ★ arm and
folding the answer plus the pass into the checksum. Rust counts in a
`HashMap`, Go in a `map`, and C, which has no map, in an open-addressing
table. Every implementation prints `30 passes over 20 arrays of 10^5:
checksum 564061910`.

BENCHTAB
