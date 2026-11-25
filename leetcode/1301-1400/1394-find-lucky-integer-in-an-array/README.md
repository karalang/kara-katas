# 1394. Find Lucky Integer in an Array

Given an array of integers `arr`, a lucky integer is an integer that has
a frequency in the array equal to its value.

Return the largest lucky integer in the array. If there is no lucky
integer return `-1`.

```
arr = [2,2,3,4]        ->  2
arr = [1,2,2,3,3,3]    ->  3
arr = [2,2,2,3,3]      ->  -1
```

**Constraints:** `1 <= arr.length <= 500` and `1 <= arr[i] <= 500`.

Each arm is `fn find_lucky(arr: Vec[i32]) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `find_lucky.kara` ★ | a count for each value from 1 to 500 in a `Vec`, read from the top down with `(1i32..=500).rev()`, the first value whose count is itself the answer. O(n + 500) |
| `find_lucky_map.kara` | the counts in a `Map`, each added to through `entry(x).or_insert(0)`, and the largest key whose count is itself found with `filter`, `map` and `max` over the entries, `unwrap_or(-1)` when there is none. O(n) |
| `find_lucky_sorted.kara` | the values sorted from the largest down with `sort_by`, and each run of equal values measured as it is passed; the first run as long as its value is the answer. O(n log n) |
| `find_lucky_tree.kara` | the counts in a `SortedMap`, each read with `get` and written back with `insert`, then walked from the largest key down with `iter().rev()`. O(n log n) |
| `find_lucky_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `HashMap` filled through `entry`, then `into_iter().filter(\|&(k, v)\| k == v).map(\|(k, _)\| k).max().unwrap_or(-1)`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's three examples, one 1,
five 5s and one 7 (`2 3 -1 1 5 -1`); the constraints' most, 500 values:
500 of 500, 499 of 499 and a 1, and two random arrays, from 1 to 500 and
from 1 to 30 (`500 values: 500 499 212 20`); and 2000 random arrays of 1
to 60 values from 1 to at most 12 or 500, half of them with a value
first written as many times as it is, so that it may be lucky (`2000
random arrays: 2186 in all, checksum 901199856`). `find_lucky.py`
mirrors the ★ arm, and its output is byte-identical. Every arm gives the
same output under `karac __mir-run`, `karac run`, `karac build` and
`karac __mir-llvm-run`.

The Mend loop: the map and sorted arms check clean as first written. The
★ arm's `for x in (1..=500).rev()` makes `x` an `i64`, since the range's
literal took the default, and returning it as the `i32` answer is
refused; `karac fix` writes the literal `1i32`. The tree arm read its
counts with `count.get(x).copied().unwrap_or(0)`, as in Rust; Kāra's
`Option` has no `copied`, and the diagnostic names `.cloned()` or `??`,
which `karac fix` applies as `.cloned()`. The Rust solution takes one
round of 13 fixes by `karac fix`'s count, from 9 errors: the `use
std::collections::HashMap;` line deleted, `struct Solution;` to `struct
Solution {}`, `Vec<i32>` and `HashMap<i32, i32>` to `Vec[i32]` and
`Map[i32, i32]`, `HashMap::new()` to `Map.new()`, `for &x in &arr` to
`for x in ref arr`, `|&(k, v)|` to `|(k, v)|`, and `Solution::` to
`Solution.`; the `entry(x).or_insert(0)` and the iterator chain stay.
Its output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: each value of the array counted by looking at every value,
and the largest whose count is itself, or -1. LeetCode's three examples
and 2000 arrays drawn as in the third line above. Every case is drawn
before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the values in reverse order: the same |
| P3 | one more of the answer, so it is lucky no longer: a smaller answer or -1; with no answer, -1 itself |
| P4 | the smallest value not in the array, written that many times: the larger of it and the answer |
| P5 | -1, or a value found in the array as many times as it is |
| P6 | the ★ arm's answer |

All 60,090 checks pass on every arm: `2003 arrays: checksum 560344655,
60090 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, counting with
`list.count`, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the counts read from the bottom up | P1 138, P3 138, P4 626, P6 552 |
| M2 | ★: each count set to 1, not added to | P1 1022, P3 1059, P4 1059, P5 841, P6 4088 |
| M3 | map: a count at least its value taken as lucky | P1 758, P3 1212, P5 758, P6 758 |
| M4 | map: the smallest lucky value taken | P1 138, P3 138, P4 626, P6 138 |
| M5 | sorted: the values sorted from the smallest up | P1 138, P3 138, P4 626, P6 138 |
| M6 | sorted: a run carried on through the smaller values after it | P1 612, P4 2003, P5 11, P6 612 |
| M7 | tree: the keys walked from the smallest up | P1 138, P3 138, P4 626, P6 138 |
| M8 | tree: a value's first count taken as 2 | P1 875, P4 1839, P5 462, P6 875 |
| M9 | solution: 0 when no value is lucky | P1 1377, P3 1377, P6 1377 |
| M10 | solution: a value's first count taken as 2 | P1 875, P4 1839, P5 462, P6 875 |

P1 and P6 kill all ten, P4 eight, P3 seven, P5 five, and P2 none: every
arm counts, so none can tell what order the values came in, and no edit
changes that. M1, M4, M5 and M7 make one mistake in four arms, the
smallest lucky value for the largest, and fail exactly alike, wrong only
where two values are lucky; their answer is still lucky, so P5 passes,
but they fail P4 when the planted value lies above their answer, which
they keep, and P3 when their answer made unlucky leaves a larger lucky
value to take. The edits that miscount (M2, M3, M6, M8, M10) answer
values that are not lucky, which P5 sees. M9, answering 0 for none,
fails only where P3 asks for -1 itself.

## Benchmarks

The bench draws 500 values from 1 to 40 once, so that most counts sit
near 12 and a lucky value comes and goes. Then 600000 rounds, each
giving one value a new one, all drawn from the checksum so far. Every
implementation prints `600000 rounds over 500 values: checksum
249076435`. The work is 500 counts and a scan down from 500, a round.
Rust and Kāra fill a fresh `Vec` of counts, C a `calloc` block, Go a
fresh slice and Python a list.

BENCHTAB
