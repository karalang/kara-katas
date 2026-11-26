# 1283. Find the Smallest Divisor Given a Threshold

Given an array of integers `nums` and an integer `threshold`, we will
choose a positive integer divisor, divide all the array by it, and sum
the division's result. Find the smallest divisor such that the result
mentioned above is less than or equal to `threshold`.

Each result of the division is rounded to the nearest integer greater
than or equal to that element. (For example: `7/3 = 3` and `10/2 = 5`.)

The test cases are generated so that there will be an answer.

```
nums = [1,2,5,9], threshold = 6           ->  5
nums = [44,22,33,11,1], threshold = 5     ->  44
nums = [21212,10101,12121], threshold = 1000000  ->  1
```

With divisor 4 the first example sums `1 + 1 + 2 + 3 = 7`, over 6; with
5 it sums `1 + 1 + 1 + 2 = 5`.

**Constraints:** `1 <= nums.length <= 5 * 10^4`, `1 <= nums[i] <= 10^6`,
`nums.length <= threshold <= 10^6`.

Each arm is `fn smallest_divisor(nums: Vec[i32], threshold: i32) ->
i32`. A sum at divisor 1 can reach 5 * 10^10, past `i32`, so the arms
that sum from divisor 1 up keep it in an `i64`.

## Approaches

| file | mechanism |
|---|---|
| `smallest_divisor.kara` ★ | the sum of rounded-up quotients only falls as the divisor grows, and the largest number as divisor makes every quotient 1, a sum of n; so a binary search over 1 to the largest number for the first divisor whose sum is within the threshold, each quotient rounded up as `(x + d - 1) / d` and summed in an `i64`. O(n log max) |
| `smallest_divisor_float.kara` | the quotients rounded up in floating point, `(x as f64 / d as f64).ceil()`, summed by `map(..).sum()`, and a binary search over 1 to 10^6 written with both ends inclusive, keeping the best divisor that fits. O(n log 10^6) |
| `smallest_divisor_gallop.kara` | no divisor below the total over the threshold, rounded up, can fit, since each quotient is at least x / d; so the search starts there and gallops, steps of 1, 2, 4 and on until a divisor fits, then a binary search in the last step, each sum stopped once it passes the threshold. O(n log max) |
| `smallest_divisor_recursive.kara` | the binary search as a recursion whose answer lies in `lo..=hi`, the half holding it searched next, the sum of rounded-up quotients by a `fold`. O(n log max), log max calls deep |
| `smallest_divisor_solution.kara` | a Rust solution as LeetCode's Rust users write it (`left` and `right` bound in one `let (mut left, mut right)`, `mid = left + (right - left) / 2`, and the sum of `(x + mid - 1) / mid` taken in an `i32` by `map(\|&x\| ..).sum()`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's three examples and one
more (`5 44 1 3`); the constraints' most, 5 * 10^4 numbers up to 10^6,
against the tightest threshold, twice it and 10^6 (`5 * 10^4 numbers:
999957 333222 25647`); and 2000 random cases of 1 to 30 numbers up to
10, 1000 or 10^6 (`2000 random cases: 69935939 in all, checksum
605319870`). `smallest_divisor.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★, gallop and recursive arms check clean as first
written. The float arm's search started `let mut lo = 1; let mut hi =
1000000;`, and its only uses of `mid` before the return were casts, `mid
as f64`. A return fixes a literal's type and a literal defaults only
when nothing has by the end of the body (design.md §8 Literals), but the
cast settled them to `i64` first, so `best`, which starts as `hi`, was
refused at the return, the message naming `hi` and blaming an operator
or a method. With the cast's `mid` changed to a constant the arm checks
unannotated. `karac fix` writes `lo: i32` and `hi: i32`, 2 fixes. That
the cast settles a literal is B-2026-11-26-1. The Rust solution takes two
rounds of 14 fixes in all by `karac fix`'s count: `struct Solution;` to
`struct Solution {}`, `Vec<i32>` to `Vec[i32]`, `let (mut left, mut
right)` to `let mut (left, right)`, the `&` dropped from `\|&x\|`,
`Solution::` to `Solution.`, and then the tuple's `1` written `1i32`, a
tuple's literal being settled when the tuple is built (B-2026-11-10-30).
Its output matches on the first run. An earlier writing of this kata,
lost with its container, rounded up with `x.div_ceil(d)` as Rust writes
it, which every integer width then lacked (B-2026-11-21-56, fixed at
449dd49566); it now checks and runs.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the divisors 1, 2, 3 and on tried in turn, each quotient the
fewest copies of the divisor that reach the number, and the first
divisor whose sum is within the threshold answered; the walk stops at
1000. Ten edge cases (one number, the threshold at n, the largest
numbers, a threshold far past the sum) and 1993 random cases of 1 to 30
numbers up to 10, 1000 or 10^6, the threshold n, from n to n + 100, or
up to 10^6.

| | property |
|---|---|
| P1 | the statement read literally, or past 1000 when no divisor up to 1000 fits |
| P2 | the answer fits and the divisor one below it does not |
| P3 | the answer is from 1 to the largest number, which always fits |
| P4 | a threshold one larger never needs a larger divisor |
| P5 | the numbers reversed give the same answer |
| P6 | the ★ arm's answer |

All 60,080 checks pass on every arm (P4 skips a threshold of 10^6):
`2003 cases: checksum 269383200, 60080 checks over 5 arms: 0 failures`,
under `karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`. Python, binary-searching with `-(-x // d)`, gives the
same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each quotient rounded up as `(x + d) / d`, one too many whenever d divides x | P1 191, P2 280, P6 1120 |
| M2 | ★: a divisor whose sum equals the threshold taken as over it | P1 247, P2 562, P6 2248 |
| M3 | float: the quotients rounded down | P1 630, P2 1079, P6 1079 |
| M4 | float: the search's top at 1000, not 10^6 | P1 449, P2 449, P6 449 |
| M5 | gallop: the last binary search's low end moved past its middle, which may be the answer | P1 131, P2 318, P3 98, P4 10, P6 318 |
| M6 | gallop: the walk started one past the lower bound | P1 1003, P2 1015, P3 19, P6 1015 |
| M7 | recursive: the search's top the smallest number, not the largest | P1 551, P2 842, P6 842 |
| M8 | recursive: the quotients rounded down | P1 630, P2 1079, P6 1079 |
| M9 | solution: a sum equal to the threshold taken as over it | P1 247, P2 562, P6 562 |
| M10 | solution: the high end moved one below a divisor that fits | P1 346, P2 503, P6 503 |

## Benchmarks

The bench builds one array of 5 * 10^4 numbers up to 10^6 and runs the ★
arm against it for 150 thresholds from 5 * 10^4 to 10^6, each drawn from
the checksum so far, so each round is about 20 passes over the array.
Every implementation prints `150 rounds over 5 * 10^4 numbers: checksum
629319377`.

BENCHTAB
