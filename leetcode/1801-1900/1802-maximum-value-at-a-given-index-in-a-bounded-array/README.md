# 1802. Maximum Value at a Given Index in a Bounded Array

You are given three positive integers `n`, `index` and `maxSum`.
Construct an array `nums` (0-indexed) of length `n` such that every
`nums[i]` is a positive integer, `|nums[i] - nums[i+1]| <= 1` for every
`0 <= i < n - 1`, the sum of all of `nums` does not exceed `maxSum`, and
`nums[index]` is as large as it can be. Return `nums[index]` of that
array.

```
n = 4, index = 2, maxSum = 6    ->  2
n = 6, index = 1, maxSum = 10   ->  3
```

**Constraints:** `1 <= n <= maxSum <= 10^9` and `0 <= index < n`.

The arms are `fn max_value(n: i32, index: i32, max_sum: i32) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `max_value.kara` ★ | a binary search on the value at `index`: the least sum a top of `v` needs is a slope down by one on each side to 1 and then ones, each side's sum worked out in closed form. O(log maxSum) |
| `max_value_layers.kara` | the pyramid grown one layer at a time from all ones: raising the top from `v` to `v + 1` costs the places within `v - 1` of `index`, and once the slope reaches both ends every layer costs `n`, so the rest is one division. O(sqrt(maxSum)) |
| `max_value_bits.kara` | the value built a bit at a time from the highest, each bit kept when the pyramid it gives still fits, each side a triangular number less the part cut off below 1. O(log maxSum) |
| `max_value_gallop.kara` | a galloping search: the top doubled until its pyramid no longer fits, then halved back between the last two, the cost counted above a floor of ones as triangles cut at the array's ends. O(log maxSum) |
| `max_value_solution.kara` | a Rust solution as LeetCode's Rust users write it (a closure `|x: i64, cnt: i64| -> i64`, `let (mut lo, mut hi) = (1i64, max_sum)`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's two examples (`2 3`); six
edges, one place, every place a 1, one unit to spare, the index at
either end, and a pyramid that fits exactly (`7 1 2 5 5 3`); the
constraints' most, one place and `10^9`, `10^9` places and `10^9`, and
the middle of `10^5` places and `10^9` (`the most: 1000000000 1 31622`);
and 3000 random cases of 1 to 30 places, any index and a sum up to 399
above `n` (`3000 random cases: checksum 6861705`). `max_value.py`
mirrors the ★ arm, and its output is byte-identical. Every arm gives the
same output under `karac __mir-run`, `karac run`, `karac build` and
`karac __mir-llvm-run`.

The Mend loop: the ★ and gallop arms check clean as first written. The
layers arm ends `(top + spare / n as i64) as i32`, and the bits arm's
closure compares `v + slope(v, index as i64) + slope(v, (n - 1 - index)
as i64) <= max_sum as i64`; check warns that each of those casts is a
widening Kāra does implicitly (`lossless_cast`), and `karac fix` removed
them, 1 fix and 3. The Rust solution takes one round of 7 fixes by
`karac fix`'s count, and its diff is: `struct Solution;` to `struct
Solution {}`, the closure's `-> i64` removed, `let (mut lo, mut hi) =
(1i64, max_sum);` to `let mut (lo, hi) = (1, max_sum);`, and
`Solution::` to `Solution.`. Its `(n as i64, index as i64, max_sum as
i64)` shadowing stays. Every arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every array of `n` positive numbers, each within 1 of the one
before, whose sum is at most `maxSum`, built a place at a time, and the
largest number any of them has at `index`. LeetCode's examples, the
edges, the constraints' most, 500 random cases of up to 1000 places and
a sum of up to `10^6` above `n`, and 1489 of up to 6 places and a sum of
up to 24. Each arm meets six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally, for at most 6 places and a sum of at most 24 |
| P2 | the index counted from the other end gives the same answer |
| P3 | a sum one larger gives the same answer or one more |
| P4 | the answer's pyramid, summed place by place, fits, and the one a step higher does not, for at most `10^5` places |
| P5 | the answer is no more than what is left after a 1 at every other place, and no less than an even spread of the sum gives |
| P6 | the ★ arm's answer |

The differential was first written with `n as i64`, `index as i64` and
`max_sum as i64` in three calls, and `karac fix` removed the 9 casts
(`lossless_cast`). All 57,465 checks pass on every arm: `2000 cases:
checksum 490747183, 57465 checks over 5 arms: 0 failures`, under `karac
__mir-run`, `karac run`, `karac build` and `karac __mir-llvm-run`.
Python, running the ★ arm's mirror over the same cases, gives the same
checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: the value at the index left out of the sum | P1 1229, P4 1559, P5 352, P6 6240 |
| M2 | ★: the ones past a slope's foot left out | P1 109, P4 453, P5 56, P6 1816 |
| M3 | layers: the left slope one place wider | P1 450, P2 640, P4 704, P6 704 |
| M4 | layers: a layer that uses the last unit refused | P1 168, P4 171, P6 171 |
| M5 | bits: the lowest bit never set | P1 730, P3 340, P4 989, P5 251, P6 990 |
| M6 | bits: one step too many cut off a short side | P1 1376, P3 6, P4 1545, P5 776, P6 1546 |
| M7 | gallop: the halving stopped a step early | P1 661, P3 271, P4 920, P5 181, P6 920 |
| M8 | gallop: the top's own cost above its 1 taken one too large | P1 658, P4 664, P5 244, P6 664 |
| M9 | solution: the ones counted without the slope they replace | P1 225, P2 85, P3 10, P4 570, P6 570 |
| M10 | solution: the left side started at the top, not one below | P1 450, P2 640, P4 704, P6 704 |

## Benchmarks

The bench builds 4000 random cases once, up to `10^6` places with a sum
of up to `10^9`, and makes 1000000 calls of the ★ arm, each case drawn
from the checksum so far. It checks clean as first written. Every
implementation prints `1000000 calls over 4000 cases: checksum
157445864`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.22 s against Rust's 0.22 s (0.23 s with overflow checks
on), C's 0.21 s and Go's 0.22 s; Python takes 11.2 s.
