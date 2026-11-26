# 1477. Find Two Non-overlapping Sub-arrays Each With Target Sum

You are given an array of integers `arr` and an integer `target`.

You have to find two non-overlapping sub-arrays of `arr` each with a sum
equal `target`. There can be multiple answers so you have to find an
answer where the sum of the lengths of the two sub-arrays is minimum.

Return the minimum sum of the lengths of the two required sub-arrays, or
return `-1` if you cannot find such two sub-arrays.

```
arr = [3,2,2,4,3],       target = 3   ->  2
arr = [7,3,4,7],         target = 7   ->  2
arr = [4,3,2,6,2,3,4],   target = 6   ->  -1
```

**Constraints:** `1 <= arr.length <= 10^5`, `1 <= arr[i] <= 1000` and `1
<= target <= 10^8`.

The arms are `fn min_sum_of_lengths(arr: Vec[i32], target: i32) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `min_sum_of_lengths.kara` ★ | one sliding window, since every value is positive, shrunk from the left until its sum is at most the target; beside it the shortest window of the target sum ending at or before each place, so each window of the target sum pairs with the shortest one ending before it starts. O(n) |
| `min_sum_of_lengths_two_pass.kara` | the same window run twice, over the array and over it reversed, giving the shortest window ending at or before each place and the shortest starting at or after it; the answer the least of the two summed across each cut. O(n) |
| `min_sum_of_lengths_prefix.kara` | prefix sums in a `Map[i64, i64]` from each sum to the place it was reached: a window of the target sum ends at `i` when the sum up to `i` less the target was reached before. O(n) |
| `min_sum_of_lengths_intervals.kara` | every window of the target sum listed as `(start, end)`, so by start; the shortest from each on kept from the back, and each window paired with the shortest starting after it ends, found by `windows.partition_point(\|x\| x.0 <= w.1)`. O(n log n) |
| `min_sum_of_lengths_solution.kara` | a Rust solution as LeetCode's Rust users write it (`vec![i32::MAX; n]`, `let (mut l, mut sum) = (0usize, 0);`, `&&`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's three examples; seven
edges, one value, two values each the target, every value 1, the only
two windows overlapping, the target more than the whole sum, LeetCode's
earlier example `[3,1,1,1,5,1,2,1]` and a pair that is not the two
shortest windows (`[1,1,1,2,2,2,4,4]` with target 6 is 6, not 5); the
constraints' most, 100000 values from 1 to 1000 for the targets 1000,
5000, 100000 and 10^8 (`100000 values: 2 14 363 -1`); and 3000 random
arrays of 1 to 60 values from 1 to top, top from 1 to 20, the target
from 1 to 40, each answer folded into a checksum (`3000 random arrays:
1011 with no pair, checksum 441076225`). `min_sum_of_lengths.py` mirrors
the ★ arm, and its output is byte-identical. Every arm gives the same
output under `karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`.

The Mend loop: the ★, two-pass, prefix and intervals arms check clean as
first written. The harness was first written passing `big.clone()` to
each arm, and check warned that the parameter only borrows it (W0300),
so the clone was dropped. The Rust solution takes one round of 14 fixes
by `karac fix`'s count, and its diff is: `struct Solution;` to `struct
Solution {}`, `Vec<i32>` to `Vec[i32]`, `vec![i32::MAX; n]` to
`Vec.filled(n, i32.MAX)`, each other `i32::MAX` to `i32.MAX`, `let (mut
l, mut sum) = (0usize, 0);` to `let mut (l, sum) = (0, 0);`, and `&&` to
`and`. Rust's `as i32` stays. Every arm's output matches on the first
run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every sub-array of the target sum, each sum added up value by
value, and of every two of them with no place in common, the least sum
of their lengths. LeetCode's examples, the edges, and 1990 random
arrays, half of 1 to 10 values from 1 to 3 with the target from 1 to 6,
so windows of the target sum crowd and overlap, and half of 1 to 40
values from 1 to top, top from 1 to 20, with the target from 1 to 40.
Each arm meets six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | the array reversed has the same answer |
| P3 | every value and the target doubled has the same answer |
| P4 | the array twice with a value more than the target between is twice the shortest window of the target sum, or -1 |
| P5 | no pair, or from 2 to the length; and a value more than the target at each end changes nothing |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 cases: checksum 914478402,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, pairing the
windows by `itertools.combinations`, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: a window starting at place 1 never paired | P1 21, P2 31, P5 21, P6 84 |
| M2 | ★: the shortest so far forgets every earlier window | P1 566, P4 1244, P6 2264 |
| M3 | two pass: the two sides of each cut overlap by one place | P1 258, P2 80, P5 84, P6 258 |
| M4 | two pass: a window one more than the target kept | P1 203, P3 203, P4 272, P6 203 |
| M5 | prefix: the shortest so far forgets every earlier window | P1 566, P4 1244, P6 566 |
| M6 | prefix: each window one place short | P1 1058, P4 1579, P5 454, P6 1058 |
| M7 | intervals: a window paired with one starting where it ends | P1 301, P5 41, P6 301 |
| M8 | intervals: each window paired with the next one after, not the shortest | P1 129, P2 55, P4 423, P6 129 |
| M9 | solution: the shortest so far forgets every earlier window | P1 130, P2 55, P4 432, P6 130 |
| M10 | solution: each window one place short | P1 1058, P4 1579, P5 454, P6 1058 |

## Benchmarks

The bench makes one array of 100000 values from 1 to 1000 once; then
makes 400 passes, each punching one value and asking the ★ arm for a
target from 500 to 20499, both chosen from the checksum so far. The C
mirror `malloc`s the table of shortest windows each call, Kāra and Rust
make it by `Vec.filled` and `vec!`, and Go by `make`. Every
implementation prints `400 passes over 100000 values: checksum
318374698`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.43 s against Rust's 0.40 s (0.45 s with overflow checks
on), C's 0.37 s and Go's 0.55 s; Python takes 10.2 s.
