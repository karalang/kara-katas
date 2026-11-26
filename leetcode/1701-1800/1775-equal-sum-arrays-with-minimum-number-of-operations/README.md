# 1775. Equal Sum Arrays With Minimum Number of Operations

You are given two arrays of integers `nums1` and `nums2`, possibly of
different lengths. The values in the arrays are between `1` and `6`,
inclusive. In one operation, you can change any integer's value in any
of the arrays to any value between `1` and `6`, inclusive. Return the
minimum number of operations required to make the sum of values in
`nums1` equal to the sum of values in `nums2`. Return `-1` if it is not
possible to make the sum of the two arrays equal.

```
nums1 = [1,2,3,4,5,6], nums2 = [1,1,2,2,2,2]  ->  3
nums1 = [1,1,1,1,1,1,1], nums2 = [6]          ->  -1
nums1 = [6,6], nums2 = [1]                    ->  3
```

**Constraints:** `1 <= nums1.length, nums2.length <= 10^5`, and `1 <=
nums1[i], nums2[i] <= 6`.

The arms are `fn min_operations(nums1: Vec[i32], nums2: Vec[i32]) ->
i32`.

## Approaches

| file | mechanism |
|---|---|
| `min_operations.kara` ★ | with the smaller sum's list first, each of its numbers can rise by `6 - x` and each of the other's fall by `x - 1`; the gains are counted by size in six slots and the largest taken first until the gap is closed. O(n1 + n2) |
| `min_operations_sorted.kara` | every number's gain listed with `map` and `chain`, sorted largest first, and taken in turn until the gap is closed. O((n1 + n2) log(n1 + n2)) |
| `min_operations_heap.kara` | the gains in a max-first `PriorityQueue`, the largest popped until the gap is closed or none is left. O((n1 + n2) log(n1 + n2)) |
| `min_operations_pointers.kara` | two pointers: the smaller sum's list sorted up and the other sorted down, each step changing whichever next number closes more of the gap. O((n1 + n2) log(n1 + n2)) |
| `min_operations_solution.kara` | a Rust solution as LeetCode's Rust users write it (`(&nums1, &nums2)`, `[0; 6]`, `for &x in`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's three examples (`3 -1 3`);
five edges, equal already, one number each five apart, two each ten
apart, seven ones against one six, out of reach, and six ones against
one six (`0 1 2 -1 0`); the constraints' most, 100000 ones against
100000 sixes, and 100000 random dice against 100000 weighted high (`the
most: 100000 9844`); and 3000 random cases of 1 to 20 numbers against 1
to 20 (`3000 random cases: checksum 608225018`). `min_operations.py`
mirrors the ★ arm, and its output is byte-identical. Every arm gives the
same output under `karac __mir-run`, `karac run`, `karac build` and
`karac __mir-llvm-run`.

The Mend loop: the ★ and sorted arms check clean as first written. The
heap arm was first written with Rust's `BinaryHeap[i32]` and
`BinaryHeap.new()`; check named Kāra's `PriorityQueue`, which pops the
smallest first unless built max-first, and `karac fix` wrote
`PriorityQueue[i32]` and `PriorityQueue.max_first()`, 2 fixes. The
pointers arm's `std.mem.swap` became `mem.swap` and its `let (mut i, mut
j)` became `let mut (i, j)`, 5 fixes by `karac fix`'s count. The Rust
solution takes one round of 17 fixes, and its diff is: `struct
Solution;` to `struct Solution {}`, `Vec<i32>` to `Vec[i32]` in both
signatures, `(&nums1, &nums2)` to `(ref nums1, ref nums2)`, each `for &x
in` to `for x in`, `&&` to `and`, and `Solution::` to `Solution.`. Its
`[0; 6]` array and `as usize` indices stay. Every arm's output matches
on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every choice of which numbers to change, the changed ones
able to make any sum from 1 to 6 each and the rest keeping theirs, so
that the sums can be made equal when the two ranges of sums meet; the
fewest changes that do it, or -1. LeetCode's examples, the edges, and
1992 random cases of 1 to 7 numbers against 1 to 5, each side's dice
from its own range. Each arm meets six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | -1 exactly when one list's most is below the other's least, 0 exactly when the sums are equal, and never more changes than numbers |
| P3 | the lists swapped, and each reversed, give the same answer |
| P4 | the same die added to both lists never needs more changes |
| P5 | a change closes the gap by at most 5, so at least a fifth of it, rounded up, is needed |
| P6 | the ★ arm's answer |

`karac fix` dropped two `as i64` casts the `lossless_cast` lint found
widening implicitly in the differential's own checks. All 60,000 checks
pass on every arm: `2000 cases: checksum 100447859, 60000 checks over 5
arms: 0 failures`, under `karac __mir-run`, `karac run`, `karac build`
and `karac __mir-llvm-run`. Python, trying every choice of numbers to
change, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: the smallest gains taken first | P1 1213, P4 832, P6 4852 |
| M2 | ★: the larger sum's numbers counted as rising | P1 959, P2 613, P5 603, P6 3836 |
| M3 | sorted: the gains sorted smallest first | P1 1327, P4 1505, P6 1327 |
| M4 | sorted: one more change taken once the gap is closed | P1 541, P2 71, P3 1, P4 18, P6 541 |
| M5 | heap: the smallest gain popped first | P1 1327, P2 368, P4 1246, P5 368, P6 1327 |
| M6 | heap: each list's gains taken as the other's | P1 955, P2 619, P3 879, P5 609, P6 955 |
| M7 | pointers: the number after each one raised skipped | P1 82, P6 82 |
| M8 | pointers: the larger sum's list walked from its smallest | P1 624, P2 141, P4 394, P5 141, P6 624 |
| M9 | solution: the last change of each size never taken | P1 920, P2 814, P5 814, P6 920 |
| M10 | solution: a closed gap answered -1 | P1 523, P2 523, P4 68, P5 523, P6 523 |

## Benchmarks

The bench builds 40 lists of 100000 dice once, each from its own range,
and makes 400 calls of the ★ arm, each pair drawn from the checksum so
far. Every implementation prints `400 calls over 40 lists: checksum
223557719`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.12 s against Rust's 0.10 s (0.13 s with overflow checks
on), C's 0.09 s and Go's 0.15 s; Python takes 5.2 s.
