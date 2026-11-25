# 1288. Remove Covered Intervals

Given an array `intervals` where `intervals[i] = [li, ri]` represent the
interval `[li, ri)`, remove all intervals that are covered by another
interval in the list.

The interval `[a, b)` is covered by the interval `[c, d)` if and only if
`c <= a` and `b <= d`.

Return the number of remaining intervals.

```
intervals = [[1,4],[3,6],[2,8]]  ->  2    [3,6) is covered by [2,8)
intervals = [[1,4],[2,3]]        ->  1
```

**Constraints:** `1 <= intervals.length <= 1000`, `intervals[i].length
== 2`, `0 <= li < ri <= 10^5`, all the given intervals are unique.

Each arm is `fn remove_covered_intervals(intervals: Vec[Vec[i32]]) ->
i32`, the Rust solution's taking `own Vec[Vec[i32]]`.

## Approaches

| file | mechanism |
|---|---|
| `remove_covered_intervals.kara` ★ | sorted by start, and by end from the longest down among equal starts, every interval that could cover another comes before it; so one sweep keeps the furthest end so far, and an interval is kept when it reaches past it. The sort is by `sort_by` with `a[0].cmp(b[0]).then(b[1].cmp(a[1]))` on a copy. O(n log n) |
| `remove_covered_intervals_pairs.kara` | every pair tried: an interval is kept unless some other starts at or before it and ends at or after it, asked by `any(..)` over the others inside a `filter(..)` over all, both on `enumerate()`. O(n^2) |
| `remove_covered_intervals_ends.kara` | the ★ sweep turned round: the intervals as `(start, end)` tuples sorted by end from the furthest down, and by start among equal ends, and one sweep keeping the leftmost start so far, an interval kept when it starts left of it. O(n log n) |
| `remove_covered_intervals_bucket.kara` | no sort: a table of 10^5 + 1 indexed by start holds the furthest end of the intervals starting there, the shorter ones being covered by it, and a walk over the starts in order keeps the furthest end so far. O(n + 10^5) |
| `remove_covered_intervals_solution.kara` | a Rust solution as LeetCode's Rust users write it (`mut intervals` sorted in place by `sort_unstable_by` with `a[0].cmp(&b[0]).then(b[1].cmp(&a[1]))`, and a `for` over the vector itself keeping the largest end), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's two examples and three
more (`2 1 2 2 1`); the constraints' most, 1000 intervals drawn over 0
to 10^5, 1000 nested in each other and 1000 each overlapping the next
(`10^3 intervals: 10 1 1000`); and 2000 random cases of 1 to 30 distinct
intervals over 0 to 10, 100 or 10^5 (`2000 random cases: 5928 in all,
checksum 214062291`). `remove_covered_intervals.py` mirrors the ★ arm,
and its output is byte-identical. Every arm gives the same output under
`karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`.

The Mend loop: the ★, pairs, ends and bucket arms check clean as first
written. The Rust solution takes one round of 18 fixes by `karac fix`'s
count: `struct Solution;` to `struct Solution {}`, the parameter `mut
intervals: Vec<Vec<i32>>` to `intervals: own Vec[Vec[i32]]` with a `let
mut intervals = intervals;` first in the body, `sort_unstable_by` to
`sort_by`, the `&` dropped from `cmp(&b[0])` and `cmp(&a[1])`, and
`Solution::` to `Solution.`. Its output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: one covered interval removed at a time, by the statement's
own `c <= a` and `b <= d`, the rest searched again until none is
covered, and what remains counted. Eleven edge cases (one interval, the
widest, intervals that touch, share a start or an end, overlap or nest)
and 1992 random cases of 1 to 30 distinct intervals over 0 to 10, 100 or
10^5.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | at least one interval is left, and no more than were given |
| P3 | the intervals reversed give the same answer |
| P4 | an interval from the first start to the last end added, it alone is left |
| P5 | every interval moved one to the right gives the same answer |
| P6 | the ★ arm's answer |

All 60,080 checks pass on every arm (P5 skips a case that reaches 10^5):
`2003 cases: checksum 44956058, 60080 checks over 5 arms: 0 failures`,
under `karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`. Python, testing every pair, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: equal starts sorted shortest first, so the longer comes after the shorter it covers | P1 687, P4 1833, P6 2748 |
| M2 | ★: an interval reaching exactly the furthest end so far kept | P1 716, P4 1837, P6 2864 |
| M3 | pairs: a cover must start strictly before | P1 687, P4 1833, P6 687 |
| M4 | pairs: an interval taken as covering itself | P1 2003, P2 2003, P4 2003, P6 2003 |
| M5 | ends: equal ends sorted by start from the right, so the wider comes after the one it covers | P1 716, P4 1837, P6 716 |
| M6 | ends: an interval starting exactly at the leftmost start so far kept | P1 687, P4 1833, P6 687 |
| M7 | bucket: the last interval at a start kept in the table, not the furthest | P1 407, P3 567, P4 142, P6 407 |
| M8 | bucket: the furthest end never moved on | P1 1854, P4 1937, P6 1854 |
| M9 | solution: the largest end never moved on | P1 1869, P4 1940, P6 1869 |
| M10 | solution: the largest end starting at 1, so an interval ending at 1 is lost | P1 11, P2 1, P4 1, P5 11, P6 11 |

## Benchmarks

The bench draws a pool of 10^5 intervals over 0 to 10^5 and runs the ★
arm on 3000 windows of 1000 of them, each window's place taken from the
checksum so far, so each round copies and sorts 1000 intervals. Every
implementation prints `3000 windows of 1000 intervals: checksum
149728894`.

BENCHTAB
