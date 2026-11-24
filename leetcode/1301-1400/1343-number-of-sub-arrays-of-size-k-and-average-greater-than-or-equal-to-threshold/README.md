# 1343. Number of Sub-arrays of Size K and Average Greater than or Equal to Threshold

Given an array of integers `arr` and two integers `k` and `threshold`,
return the number of sub-arrays of size `k` and average greater than or
equal to `threshold`.

```
arr = [2,2,2,2,5,5,5,8], k = 3, threshold = 4               ->  3
arr = [11,13,17,23,29,31,7,5,2,3], k = 3, threshold = 5     ->  6
```

**Constraints:** `1 <= arr.length <= 10^5`, `1 <= arr[i] <= 10^4`, `1 <=
k <= arr.length`, `0 <= threshold <= 10^4`.

The arms are `fn num_of_subarrays(arr: Vec[i32], k: i32, threshold: i32)
-> i32`.

## Approaches

| file | mechanism |
|---|---|
| `num_of_subarrays.kara` ★ | an average of at least threshold is a sum of at least k * threshold, so a sliding window keeps the sum of the last k values, adding the one coming in and taking off the one leaving, and counts the windows that reach it. O(n) |
| `num_of_subarrays_prefix.kara` | the running sums before each place, so the window from i is `before[i + k] - before[i]`. O(n) |
| `num_of_subarrays_windows.kara` | every window from `windows(k)`, each summed afresh, kept by `filter` and counted. O(n * k) |
| `num_of_subarrays_average.kara` | the window's average taken by integer division, which rounds down, so it reaches a whole threshold exactly when the true average does; the first window summed from the slice `arr[0..k]`. O(n) |
| `num_of_subarrays_solution.kara` | a Rust solution as LeetCode's Rust users write it (`let k = k as usize;`, the first window summed by `arr[..k].iter().sum::<i32>()`, the target `threshold * k as i32`, and the rest by `for i in k..arr.len()` adding `arr[i] - arr[i - k]`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's two examples, one value,
and 10^5 values, the constraints' longest, at random from 1 to 10^4
(their average is about 4698), with k = 1000 and threshold 4700, with k
= 1 and threshold 0, and with k the whole length and threshold 4697
(`3 6 1 50931 100000 1`); and 1000 random arrays of 1 to 300 values,
most of them short, from 1 to 10 or to 10^4, with k from 1 to the length
(`1000 random arrays: checksum 976348281`). `num_of_subarrays.py`
mirrors the ★ arm, and its output is byte-identical. Every arm gives the
same output under `karac __mir-run`, `karac run` and `karac
__mir-llvm-run`.

The Mend loop: three Kāra arms check clean. The windows arm was written
`arr.windows(k).filter(..)`; `windows` returns a `Vec[Slice[T]]`, not an
iterator (docs/library/collections.md), and `karac check` says so
(E0236) with the fix, which `karac fix` applies: `.into_iter()` before
the `filter`. The Rust solution takes one round of 9 fixes by `karac
fix`'s count, from 5 errors: `struct Solution;` to `struct Solution {}`,
each `Vec<..>` to `Vec[..]`, the turbofish in `sum::<i32>()` removed and
the binding annotated `sum: i32` instead, `usize` to `i64`, and
`Solution::` to `Solution.`. Both match on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every sub-array of k values summed afresh, its average taken
as a floating-point quotient and compared with the threshold. 2000 arrays
of 1 to 10 values in four kinds, 500 each: from 1 to 3; from 1 to 100;
every value the same, from 1 to 5; and alternating, the even places from
50 to 100 and the odd ones from 1 to 10. k is drawn from 1 to the
length, the threshold from 0 to one above the largest value, and every
case before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the array read backwards: the same answer |
| P3 | every value and the threshold one higher: the same answer |
| P4 | the threshold one higher: no more windows |
| P5 | k = 1: the number of values that reach the threshold |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 arrays: checksum 899688492,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run` and `karac __mir-llvm-run`. Python, comparing each sum with k *
threshold, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash, and no two
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a sum equal to the need not counted | P1 228, P5 394, P6 912 |
| M2 | ★: the value leaving taken off one place late | P1 473, P2 310, P3 62, P5 1031, P6 1892 |
| M3 | prefix: each window one value short at its start | P1 867, P2 136, P3 127, P5 1532, P6 867 |
| M4 | prefix: the last window never tried | P1 1254, P2 204, P5 1265, P6 1254 |
| M5 | windows: windows of k + 1 values | P1 1464, P3 64, P5 1723, P6 1464 |
| M6 | windows: the sum compared with the threshold itself | P1 638, P3 16, P6 638 |
| M7 | average: the first window never counted | P1 1314, P2 204, P5 1472, P6 1314 |
| M8 | average: later averages rounded up | P1 71, P2 47, P6 71 |
| M9 | solution: the loop started one window late | P1 926, P2 298, P5 1393, P6 926 |
| M10 | solution: the target set for one value fewer | P1 660, P3 43, P5 1141, P6 660 |

P1 and P6 kill all ten, P5 eight, P2 six, P3 five and P4 none. Windows
of one value (P5) are a count anyone can check, and catch every edit
that is wrong at k = 1: a value equal to the threshold left out (M1),
the window holding an extra value (M2, M5), none (M3), or none counted
at the end, the start or the second place (M4, M7, M9), and a target of
zero (M10); comparing a sum with the threshold itself (M6) and rounding
an average of one value up (M8) change nothing there. Reading backwards
(P2) catches the edits that treat the first window or the last
differently from the rest (M2, M3, M4, M7, M8, M9). Raising every value
and the threshold by one (P3) moves each average by exactly one, which
catches the edits whose comparison does not move with it: a sum of k + 1
or k - 1 values (M2, M5, M3), the threshold not multiplied (M6), or
multiplied by k - 1 (M10). Every edit still asks a larger sum of a
higher threshold, so P4 catches nothing. M8 is the weakest: rounding up
changes a verdict only when a later window's average falls strictly
between the threshold less one and the threshold, 71 of the 2000 cases.

## Benchmarks

The bench builds 10 arrays of 10^5 values, the constraints' longest, at
random from 1 to 10^4, once; then makes 60 passes, each setting one
value of every array from the checksum so far and drawing k from 1 to
1000 and the threshold from 4500 to 4899 from it too, so no answer
carries over, answering every array with the ★ arm's sliding window and
folding the answer plus the pass into the checksum. Every implementation
prints `60 passes over 10 arrays of 10^5: checksum 499337203`.

BENCHTAB
