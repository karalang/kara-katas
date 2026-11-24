# 1331. Rank Transform of an Array

Given an array of integers `arr`, replace each element with its rank. The
rank represents how large the element is. The rank has the following
rules: rank is an integer starting from 1; the larger the element, the
larger the rank, and if two elements are equal, their rank must be the
same; rank should be as small as possible.

```
arr = [40,10,20,30]                  ->  [4,1,2,3]
arr = [100,100,100]                  ->  [1,1,1]
arr = [37,12,28,9,100,56,80,5,12]    ->  [5,3,4,2,8,6,7,1,3]
```

**Constraints:** `0 <= arr.length <= 10^5`, `-10^9 <= arr[i] <= 10^9`.

The arms are `fn array_rank_transform(arr: Vec[i32]) -> Vec[i32]`.

## Approaches

| file | mechanism |
|---|---|
| `array_rank_transform.kara` ★ | the values copied, sorted and their repeats removed with `dedup`; each value's rank is one more than its place in that list, found by `binary_search`. O(n log n) |
| `array_rank_transform_map.kara` | the values sorted, and walked in order, each value not yet seen given the next rank in a `Map`; every value then looked up there. O(n log n) |
| `array_rank_transform_order.kara` | the places sorted by their values, then walked in that order, the rank going up by one each time the value does; no list of distinct values and no map. O(n log n) |
| `array_rank_transform_tree.kara` | the values gathered into a `SortedSet`, which keeps them in order without repeats; its walk gives each value its rank in a `SortedMap`. O(n log n) |
| `array_rank_transform_solution.kara` | a Rust solution as LeetCode's Rust users write it (`sort_unstable()` and `dedup()` on a clone, a `HashMap<i32, i32>` collected from `enumerate()` with the pattern `\|(i, &x)\|`, and every value looked up as `rank[x]`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's three examples; no values,
and the constraints' extremes (`[] [3, 1, 2, 1]`); 10^5 values, the
constraints' longest, counting down in pairs (`10^5 values: first 50000,
last 1, checksum 262409426`); and 600 random arrays of 0 to 3000 values,
most of them short, from 3, 1000 or 2 * 10^9 + 1 possible values (`600
random arrays: highest rank 2787, checksum 524778286`).
`array_rank_transform.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run` and `karac __mir-llvm-run`.

The Mend loop: the four Kāra arms check clean. The Rust arm takes one
round of 12 fixes from 7 errors: the `use std::collections::HashMap;`
line deleted, `struct Solution;` to `struct Solution {}`, `Vec<i32>` to
`Vec[i32]`, `HashMap<i32, i32>` to `Map[i32, i32]`, `sort_unstable` to
`sort`, `|(i, &x)|` to `|(i, x)|`, and `Solution::` to `Solution.`. Its
output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: a value's rank is one more than the number of different values
below it. 2000 arrays of 0 to 8 values in four kinds, 500 each: values
from 0 to 2; within 5 of 0; each one of -10^9, -1, 0, 1 or 10^9; and
rising by 1 to 3 from a start within 50. Every array and the amount it is
moved by are drawn before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the array read backwards: the ranks backwards |
| P3 | every value moved by one amount up to 1000 either way: the same ranks |
| P4 | every value negated: the ranks turned over, the highest rank plus one less each |
| P5 | the array twice over: its ranks twice over |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 arrays: checksum 883511616,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run` and `karac __mir-llvm-run`. Python, counting the different smaller
values, gives the same checksum.

## Mutation testing

Twelve edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`. Two are left out. The ★ arm
keeping the repeats in its sorted list fails the same checks as the Rust
arm keeping them (M9) apart from P6, which fails four times as often when
the ★ arm is the one edited; and the Rust arm ranking each value by its
place in the input fails exactly the checks of the tree arm keeping the
values in arrival order (M7), the same answer reached two ways. The ten
kept, two to each arm, are each killed, fail the same way under both
backends and not by a crash, and no two fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the repeats removed before the sort | P1 594, P4 594, P5 1510, P6 2376 |
| M2 | ★: ranks counted from 0 | P1 1782, P4 1782, P6 7128 |
| M3 | map: every value given the next rank, repeats too | P1 879, P4 879, P5 1604, P6 879 |
| M4 | map: the values sorted largest first | P1 1510, P6 1510 |
| M5 | order: a rank jumping to the place after a tie | P1 694, P4 778, P5 1510, P6 694 |
| M6 | order: the places sorted by size, sign dropped | P1 804, P2 463, P3 947, P4 1510, P5 463, P6 804 |
| M7 | tree: the values kept in arrival order, repeats too | P1 1091, P2 1466, P4 1568, P5 1782, P6 1091 |
| M8 | tree: the answers given from the last value back | P1 1474, P6 1474 |
| M9 | solution: the repeats kept | P1 879, P4 879, P5 1782, P6 879 |
| M10 | solution: the clone never sorted | P1 981, P2 1432, P4 1510, P5 1510, P6 981 |

P1 and P6 kill all ten, P4 eight, P5 seven, P2 three and P3 one. Negating
(P4) turns the order over, so it catches every edit that is wrong about
repeats or ties (M1, M3, M5, M9) and the ranks counted from 0 (M2), but
misses the two that reverse something outright (M4, M8): each turns the
negated array's answer over the same way it turns the original's, so the
two wrong answers still stand in the relation P4 asks for. Doubling the array
(P5) gives every value a repeat, so it catches each edit that mishandles
repeats. Reading backwards (P2) catches only the edits whose answer
depends on where a value sits (M6, M7, M10), and moving every value (P3)
only the one that ties the answer to where 0 lies (M6).

## Benchmarks

The bench builds 20 arrays of 10^5 values, the constraints' longest,
alternately from 1 to 10^9 and from 1 to 1000, so half have many repeats,
once; then makes 15 passes, each setting one value of every array from the
checksum so far, so no answer carries over, answering it with the ★ arm and
folding two of its ranks plus the pass into the checksum. Each call copies
the array, sorts and dedups the copy, and searches it in every language. C
sorts with `qsort` and Go with `slices.Sort`, the kata convention, and
both trail: on a shared Linux container with two compiler gates running,
C took 7.3 s, Go 5.9 s, Kāra 2.1 s and Rust 1.2 s. `qsort` calls its
comparator through a pointer for every comparison, where Rust's and
Kāra's sorts compare `i32`s inline. Every implementation prints `15 passes
over 20 arrays of 10^5: checksum 929651315`.

BENCHTAB
