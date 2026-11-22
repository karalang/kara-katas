# 2799. Count Complete Subarrays in an Array

You are given an array `nums` consisting of **positive** integers.

We call a subarray of an array **complete** if the following condition
is satisfied:

- The number of **distinct** elements in the subarray is equal to the
  number of distinct elements in the whole array.

Return *the number of **complete** subarrays*.

A **subarray** is a contiguous non-empty part of an array.

```
nums = [1, 3, 1, 2, 2]  ->  4
nums = [5, 5, 5, 5]     ->  10
```

**Constraints:** `1 <= nums.length <= 1000`, `1 <= nums[i] <= 2000`.

## Approaches

A subarray is complete when it holds all d distinct numbers of the
array, and then so does every subarray that contains it; so for each
end the complete subarrays are those starting at or before some last
start.

| file | mechanism |
|---|---|
| `complete.kara` ★ | a window slid along the ends, its counts in a `Map`; for each end the start moved on while the window would stay complete without its first number, and every start up to the window's counted. O(n) |
| `complete_starts.kara` | by every start: a `Set` grown along the ends until it holds all d numbers, and then every end from there on complete, n - end of them, with no need to go further. O(n^2) |
| `complete_first.kara` | by first places, from the right: for each start the first place at or after it of each number, in a `Map`, and their multiset in a `SortedMap`, so that the subarrays from the start are complete from its last key on. O(n log n) |
| `complete_table.kara` | the ★ arm's window with its counts in a table over the numbers, up to 2000, and the numbers it holds counted as they come. O(n + V) |
| `complete_solution.kara` | a Rust solution as LeetCode's Rust users write it, d by a `HashSet`, then a window over a `HashMap` shrunk from the left while it stays complete, `ans += n - r` for each shrink, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 6 lines: LeetCode's two examples; 1000
numbers, LeetCode's most, all different, so that only the whole is
complete; 1000 numbers going round 1 to 10; 3000 random arrays of 1 to
12 numbers from 1 to 4; and 50 of 1000 numbers, from 1 to 2000 or from
1 to 20, the last two with the sum of the counts and a checksum.
`complete.py` mirrors the ★ arm and its output is byte-identical.

```
4
10
1
491536
3000 small arrays: complete sum to 25799, checksum 518997146
50 arrays of 1000: complete sum to 10815894, checksum 393908843
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every subarray, and each counted when every number of the
array is found in it; no window and no distinct count. It draws 2000
random arrays of 1 to 12 numbers from 1 to 4, then 50 of up to 1000
numbers, from 1 to 2000 or from 1 to 20, all before any arm answers; the
literal reading is asked only of the first 2000.

| | property |
|---|---|
| P1 | up to 12 numbers, the count is the literal reading's |
| P2 | every number 1000 more: the same count |
| P3 | the numbers reversed: the same count |
| P4 | the first number put again at the end: at least one more |
| P5 | from 1 to n(n + 1) / 2, and n(n + 1) / 2 when every number is the first |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 241302952, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases, each subarray's set against the whole's,
gives the same checksum. On a failure it prints the first ten and then
the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. Three are killed by an index out of bounds,
which both backends report at the same line.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the starts counted one short | P1 2000, P3 1270, P5 2050, P6 2050 |
| M2 | ★: the start moved past a number held once | killed under both: runtime error: index out of bounds |
| M3 | starts: only the first complete end counted | P1 1342, P3 1270, P4 937, P5 1899, P6 1376 |
| M4 | starts: each start's own number left out | P1 2000, P3 1270, P5 2050, P6 2050 |
| M5 | first: a number's old place never dropped | P1 1342, P3 1270, P4 937, P5 1899, P6 1376 |
| M6 | first: the least first place read, not the greatest | P1 1792, P3 1270, P6 1842 |
| M7 | table: a number's first coming never counted | P1 2000, P3 351, P4 1764, P5 2050, P6 2050 |
| M8 | table: the start moved while its number is held at all | killed under both: runtime error: index out of bounds |
| M9 | solution: the ends counted from the end itself | P1 2000, P3 1270, P5 2050, P6 2050 |
| M10 | solution: a number run out kept in the window | killed under both: runtime error: index out of bounds |

## Benchmarks

The bench draws 2000 arrays of 1000 numbers, LeetCode's most, half from
1 to 2000 and half from 1 to 20, all of them first, then answers each 20
times by the ★ arm in all five languages; C, having no map, keeps the
window's counts in a table over the numbers, as `complete_table.kara`
does, so its row measures the table against the others' maps. Every
implementation prints `2000 arrays of 1000, 20 rounds: complete sum to
8639730880, checksum 942766283`.

BENCHTAB

## Verification

All five arms print the same output as `complete.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The table arm checked clean as first written. The ★ arm took d as
`nums.iter().collect::[Set[i64]]().len()`, Rust's turbofish; `karac
check` refused it, Kāra having no call-site type arguments, and `karac
fix` made it `Set[i64].from_iter(nums.iter())` and then, the iterator
giving `ref i64`, `Set[i64].from_iter(nums.iter().cloned())`, both in
one run. The starts and first arms, written with `from_iter` from the
start, took the same `.cloned()` from `karac fix`.

LeetCode's Rust template took 19 `karac fix` edits, the wrapper
included: `use std::collections::{HashMap, HashSet}` became `struct
Solution {}`; the `Vec<..>`s became `Vec[..]`; `nums.iter().collect::
<HashSet<_>>()` became `Set.from_iter(nums.iter())`; `HashMap<i32, i32>`
became `Map[i32, i32]`; `ans` took the type `i32`; `get_mut(&nums[l])`
and `remove(&nums[l])` dropped their `&`; the wrapper's `|&v|` dropped
its `&` and its `as i64` on the answer, an `i32` widening by itself; and
`Solution::` became `Solution.`.
