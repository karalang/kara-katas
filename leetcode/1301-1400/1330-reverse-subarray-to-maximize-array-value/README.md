# 1330. Reverse Subarray To Maximize Array Value

You are given an integer array `nums`. The value of this array is defined
as the sum of `|nums[i] - nums[i + 1]|` for all `0 <= i < nums.length -
1`. You are allowed to select any subarray of the given array and reverse
it. You can perform this operation only once. Find the maximum possible
value of the final array.

```
nums = [2,3,1,5,4]        ->  10
nums = [2,4,9,24,2,1,10]  ->  68
```

**Constraints:** `1 <= nums.length <= 3 * 10^4`, `-10^5 <= nums[i] <=
10^5`, and the answer fits in a 32-bit integer.

The arms are `fn max_value_after_reverse(nums: Vec[i32]) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `max_value_after_reverse.kara` ★ | a reversal changes only the two neighbour pairs at its ends. Reversing a prefix or a suffix changes one pair, tried at every place; reversing from inside to inside gains at best twice the gap between the largest smaller value of any pair and the smallest larger value of any pair. O(n) |
| `max_value_after_reverse_signs.kara` | a reversal from after pair (a, b) through pair (c, d) gains `\|a - c\| + \|b - d\| - \|a - b\| - \|c - d\|`, and `\|x\|` is the larger of x and -x, so the gain is the best of four signed sums, each split into a part of the left pair and a part of the right; one pass keeps the best left part of each of the four. O(n) |
| `max_value_after_reverse_pairs.kara` | every reversal tried, each from l through r, its gain read from the two pairs at its ends. O(n^2) |
| `max_value_after_reverse_iter.kara` | the ★ arm's three gains written as iterator folds over the neighbour pairs, `nums.iter().zip(nums[1..].iter())`. O(n) |
| `max_value_after_reverse_solution.kara` | a Rust solution as LeetCode's Rust users write it (`windows(2)` over the pairs, `i32::MIN` and `i32::MAX` for the running bounds, the bounds and gains kept with `.max(..)` and `.min(..)`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's two examples; one value;
two; all equal; a rise that a reversal of a suffix helps; 400 values
swinging between the constraints' extremes; and a climb of 400 from
-99000 (`10 68 0 8 0 17 79800000 590535`); then 600 random arrays of 1
to 400 values, most of them short, within 10, 1000 or 100000 either side
of 0 (`600 random arrays: values total 38790078, checksum 542371776`).
The longest arrays are 400 long, not the constraints' `3 * 10^4`,
because the pairs arm is quadratic and every arm runs the same harness
under the interpreter too. `max_value_after_reverse.py` mirrors the ★
arm, and its output is byte-identical. Every arm gives the same output
under `karac __mir-run`, `karac run` and `karac __mir-llvm-run`.

The Mend loop: the ★, signs and iter arms check clean. The pairs arm,
written with `let mut total = 0;`, takes 3 fixes from 1 error: a literal
keeps the default `i64` whatever it is added to, so `total`, `gain` and
`g` are annotated `i32`. The Rust arm takes one round of 11 fixes from 7
errors: `struct Solution;` to `struct Solution {}`, `Vec<i32>` to
`Vec[i32]`, `let (mut mx, mut mn)` to `let mut (mx, mn)`, `i32::MIN` and
`i32::MAX` to `i32.MIN` and `i32.MAX`, `total` and `res` annotated `i32`,
and `Solution::` to `Solution.`. Its output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every subarray reversed in a copy, the copy's value summed,
and the largest value kept. 2000 arrays of 1 to 8 values in four kinds,
500 each: values within 3 of 0; within 20; within 1000; and rising by 0
to 9 from a start within 50. Every array and the amount it is moved by
are drawn before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the array read backwards: the same answer |
| P3 | every value negated: the same answer |
| P4 | every value moved by one amount up to 1000 either way: the same answer |
| P5 | every value doubled: twice the answer |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 arrays: checksum 204732651,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run` and `karac __mir-llvm-run`. Python, reversing every subarray, gives
the same checksum.

## Mutation testing

Thirteen edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`. Three are left out. The iter arm
taking a loss when no reversal gains survives every check, and is
equivalent: reversing the first value alone is a prefix reversal that
gains 0, so the best prefix or suffix gain is never below 0. The ★ arm's
inside gain not doubled fails the same checks as the iter arm's M7 apart
from P6, which fails four times as often when the ★ arm is the one
edited; and the iter arm reversing no suffix fails exactly the checks of
the signs arm's M4. The ten kept, two to each arm, are each killed, fail
the same way under both backends and not by a crash, and no two fail the
same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the prefix reversal's first value set beside the wrong end | P1 297, P2 569, P6 1188 |
| M2 | ★: the largest smaller value started at 0 | P1 381, P3 842, P4 962, P6 1524 |
| M3 | signs: two of the four sign pairs never tried | P1 437, P2 614, P3 614, P6 437 |
| M4 | signs: no suffix reversed | P1 334, P2 681, P6 334 |
| M5 | pairs: no two neighbours swapped | P1 551, P6 551 |
| M6 | pairs: the right end's pair dropped beside the last value | P1 651, P2 987, P6 651 |
| M7 | iter: the smallest larger value taken as the largest | P1 618, P6 618 |
| M8 | iter: the first gap left out of the sum | P1 1627, P2 1402, P6 1627 |
| M9 | solution: the suffix reversal's last value set beside the wrong end | P1 291, P2 569, P6 291 |
| M10 | solution: the larger value of each pair taken for the bound | P1 1205, P3 1370, P6 1205 |

P1 and P6 kill all ten, P2 six, P3 three, P4 one and P5 none. Reading
the array backwards (P2) turns a prefix into a suffix, so it catches
every edit that treats the two ends differently (M1, M4, M6, M8, M9) and
one that drops a sign pair (M3). Negating (P3) swaps each pair's smaller
and larger value, which catches a bound taken from the wrong one (M10), a
bound started at 0 (M2), and the dropped sign pair (M3). Moving every
value (P4) catches only the bound started at 0, the one edit that ties
the answer to where 0 lies. Doubling (P5) catches none: every edit here
is linear in the values, so it doubles its own wrong answer.

## Benchmarks

The bench builds 20 arrays of `3 * 10^4` values, the constraints'
longest, within 30000 of 0, so every answer fits an `i32`, once; then
makes 75 passes, each setting one value of every array from the checksum
so far, so no answer carries over, answering it with the ★ arm and
folding the answer plus the pass into the checksum. Every language reads
the array in place, with no copy. Every implementation prints `75 passes
over 20 arrays of 3 * 10^4: checksum 580844537`.

BENCHTAB
