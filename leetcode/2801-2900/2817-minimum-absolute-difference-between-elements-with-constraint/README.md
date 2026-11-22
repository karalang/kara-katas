# 2817. Minimum Absolute Difference Between Elements With Constraint

You are given a **0-indexed** integer array `nums` and an integer `x`.

Find the **minimum absolute difference** between two elements in the
array that are at least `x` indices apart.

In other words, find two indices `i` and `j` such that
`abs(i - j) >= x` and `abs(nums[i] - nums[j])` is minimized.

Return *an integer denoting the **minimum** absolute difference between
two elements that are at least* `x` *indices apart.*

```
nums = [4,3,2,4],     x = 2  ->  0
nums = [5,3,2,10,15], x = 1  ->  1
nums = [1,2,3,4],     x = 3  ->  3
```

**Constraints:** `1 <= nums.length <= 10^5`; `1 <= nums[i] <= 10^9`;
`0 <= x < nums.length`.

## Approaches

| file | mechanism |
|---|---|
| `window.kara` ★ | a sliding set: walking i from x, nums[i - x] joins a `SortedSet` of the numbers at least x behind, and nums[i] is checked against its neighbours there, the first at or above it by `range(v, i64.MAX).next()` and the last at or below by `range_inclusive(i64.MIN, v).next_back()`, stopping at 0 |
| `window_map.kara` | a counted window: a `SortedMap` from each number at least x behind to how often it is there, asked for nums[i]'s `ceiling` and `floor` |
| `window_sorted.kara` | a sorted `Vec` for the window, each number put in its place found by `partition_point` and `insert`, nums[i] compared with the numbers either side of where it would go |
| `window_pairs.kara` | every far enough pair: for each i, each j from i + x on, by `abs`, stopping at 0; O(n^2), LeetCode's time limit aside |
| `window_solution.kara` | a Rust solution as LeetCode's Rust users write it, a `BTreeSet` queried by `range(v..).next()` and `range(..=v).next_back()`, `usize` indices and `i32` values, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's three examples; x = 0, a
number against itself; 2000 numbers rising by 7 with x = 1000, and
falling by 1000 with x = 1999; 3000 random arrays of 1 to 10 numbers up
to 20 with x below the count; and 50 of up to 1000 numbers up to 10^9,
the last two as checksums. `window.py` mirrors the ★ arm, with a list
kept in order by `bisect.insort` for the set, and its output is
byte-identical.

```
0
1
3
0
7000
1999000
3000 small arrays: checksum 669300623
50 large arrays: checksum 51344755
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every pair of indices i and j, in both orders, whose distance
|i - j| is at least x, and the least |nums[i] - nums[j]| among them; no
window and no set. It draws 2000 random arrays of 1 to 10 numbers up to
20 with x below the count, then 50 of up to 600 numbers up to 10^9, all
before any arm answers; the literal reading is asked only of the first
2000.

| | property |
|---|---|
| P1 | up to 10 numbers, the answer is the literal reading's |
| P2 | the difference of some pair at least x apart, and at least 0 |
| P3 | the numbers reversed: the same answer |
| P4 | every number v as 10^9 + 1 - v, turned within the range: the same answer |
| P5 | x one less: no larger; x = 0: 0 |
| P6 | each arm agrees with at least three of the other four |

P4 first multiplied every number by 3, which took the large cases past
`i32` and made the solution's `v - lo` overflow, a trap Kāra's checked
arithmetic reported where Rust's release build would wrap; the
statement allows only numbers up to 10^9, so the property now turns
the numbers within that range.

The differential prints `2050 cases: checksum 429042953, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. Nine are killed, each the same
way under both backends. M2 survives and is equivalent: a value equal to
v is found by the search below, which takes v itself, so the search
above may start at v + 1.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the number x behind never joining | P1 2000, P2 2050, P5 600, P6 2050 |
| M2 | ★: a neighbour above found only strictly above | survives: equivalent (above) |
| M3 | ★: the neighbour below taken as the smallest | P1 101, P3 265, P4 278, P5 39, P6 129 |
| M4 | map: the ceiling only, no floor | P1 421, P2 246, P3 927, P4 927, P6 453 |
| M5 | map: the window one number wider | P1 542, P2 547, P3 271, P6 547 |
| M6 | sorted: each number put at the front | P1 354, P3 516, P4 648, P5 134, P6 398 |
| M7 | sorted: only the number above compared | P1 421, P2 246, P3 927, P4 927, P6 453 |
| M8 | pairs: the pairs a step too far apart | P1 1224, P2 606, P5 465, P6 1227 |
| M9 | solution: the window counted from x + 1 | P1 967, P2 606, P3 561, P5 209, P6 971 |
| M10 | solution: the difference below counted one more | P1 421, P2 362, P3 927, P4 927, P6 453 |

## Benchmarks

The bench draws 10 arrays of 10^5 distinct numbers up to 10^9,
LeetCode's most, shuffled, with x from 0 to 10^5 - 1, all of them
first, then answers each 3 times by the ★ arm in all five languages;
the numbers are distinct so no answer stops early at 0. Rust's window
is a `BTreeSet`, as Kāra's is a `SortedSet`; C, Go and Python have no
ordered set in their libraries, so theirs is an array kept in order by
a binary search and a shift of the larger numbers, O(n) an insert,
which is the same answer by a costlier road. Every implementation
prints `10 arrays of 100000, 3 rounds: differences sum to 2361,
checksum 738633325`.

BENCHTAB

## Verification

All five arms print the same output as `window.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms and the harness checked clean as first written.
`SortedSet` has no `ceiling` or `floor`, which `SortedMap` has
(library/collections.md), so the ★ arm asks `range` and
`range_inclusive` as Rust's `BTreeSet` users do, and the map arm uses
the map's own.

LeetCode's Rust template took 19 `karac fix` edits in one run, the
wrapper included: `struct Solution {}` added for the `use` line;
`BTreeSet::new()` became `SortedSet.new()`; `range(v..)` became
`range_inclusive(v, i32.MAX)` and `range(..=v)` `range_inclusive(i32.MIN,
v)`, and the `Some(&hi)` and `Some(&lo)` patterns lost their `&` for a
`.cloned()` on the item; `i32::MAX` became `i32.MAX`; `x as usize`
became `x as i64`; `Vec<..>` became `Vec[..]`, `|&v|` lost its `&`,
`Solution::` took `.`, and the wrapper's `as i64` went, an `i32`
widening implicitly.
