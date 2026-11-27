# 1837. Sum of Digits in Base K

Given an integer `n` (in base `10`) and a base `k`, return the sum of
the digits of `n` after converting `n` from base `10` to base `k`. After
converting, each digit should be interpreted as a base `10` number, and
the sum should be returned in base `10`.

```
n = 34, k = 6   ->  9
n = 10, k = 10  ->  1
```

**Constraints:** `1 <= n <= 100`, `2 <= k <= 10`.

The arms are `fn sum_base(n: i64, k: i64) -> i64`.

## Approaches

| file | mechanism |
|---|---|
| `sum_base.kara` ★ | the digits of `n` in base `k` are its remainders by `k`, the last digit first, `n` divided by `k` after each. O(log_k n) |
| `sum_base_recursive.kara` | the ★ arm's walk as recursion: the last digit of `n` and the sum of the digits of `n / k`. O(log_k n) |
| `sum_base_place.kara` | the digits read from the first: the largest power of `k` at most `n` found, and the digit at each place, `n / place % k`, from it down to 1. O(log_k n) |
| `sum_base_digits.kara` | `n` written out in base `k` as a string of its digits, which are all below 10, and the digits of the string summed. O(log_k n) |
| `sum_base_solution.kara` | a Rust solution as LeetCode's Rust users write it (`mut n` divided down, the remainders summed), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's two examples; seven edges,
the least `n`, `n` equal to `k`, one less than `k`, and a power of it,
100 in base 2 and base 10, and 99 in base 10 (`1 1 6 1 3 1 18`); the
constraints whole, every `n` from 1 to 100 in every base from 2 to 10,
and the most of the sums (`every case: checksum 491581379, the most
18`); and 3000 random cases of `n` from 1 to 100 in a base from 2 to 10
(`3000 random cases: checksum 957790009`). `sum_base.py` mirrors the ★
arm, and its output is byte-identical. Every arm gives the same output
under `karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`.

The Mend loop: every arm and the harness check clean as first written.
The Rust solution takes 16 fixes by `karac fix`'s count, and its diff
is: `struct Solution {}` added above the `impl`; `mut n: i32` to `n:
i32` with `let mut n = n;` at the body's start; `let mut sum = 0` to
`let mut sum: i32 = 0`, the sum returned as an `i32`; `Solution::` to
`Solution.` at the harness's 11 calls; and the harness's `as i64` taken
off the result where it is added to the checksum. The `as i64` on `let s
= Solution.sum_base(..) as i64`, which gives `s` its type, stays. The
solution takes `i32`s, so its harness passes `n as i32` and `k as i32`.
Every arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: `n` written in base `k` by counting up to it from 0 in base
`k`, a digit at a time with a carry, and the digits of what is written
summed as base 10 numbers. It runs 2000 random cases of `n` from 1 to
100 in a base from 2 to 10. Each arm meets six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | from 1 to `n`, and `n` less the sum a multiple of `k - 1` |
| P3 | `n * k`, its digits with a 0 after them, gives the same sum |
| P4 | a 1 put before the digits adds 1 |
| P5 | in base 10, the sum of the decimal digits |
| P6 | the ★ arm's answer |

It checks clean as first written. All 60,000 checks pass on every arm:
`2000 cases: checksum 243013143, 60000 checks over 5 arms: 0 failures`,
under `karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`. Python, over the same cases, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: each digit counted one more | P1 2000, P2 1534, P3 2000, P4 2000, P5 2000, P6 8000 |
| M2 | ★: the leading digits left out once what is left is at most `k` | P1 2000, P2 1591, P4 1004, P5 2000, P6 8000 |
| M3 | recursive: every other digit skipped | P1 1716, P2 1242, P3 1668, P4 965, P5 1807, P6 1716 |
| M4 | recursive: the first digit counted as 0 | P1 2000, P2 1591, P4 1004, P5 2000, P6 2000 |
| M5 | place: the first place one power short when `n` is a power of `k` | P1 59, P2 59, P3 19, P4 59, P5 38, P6 59 |
| M6 | place: each place's digit taken with the digits before it | P1 1917, P2 1917, P3 2000, P4 2000, P5 1829, P6 1917 |
| M7 | digits: each digit written one more | P1 2000, P2 1534, P3 2000, P4 2000, P5 2000, P6 2000 |
| M8 | digits: `n` divided by `k + 1` after each digit | P1 1426, P2 1204, P3 1807, P4 1741, P5 894, P6 1426 |
| M9 | solution: the digits taken in base `k + 1` | P1 1875, P2 1389, P3 1620, P4 1293, P5 1829, P6 1875 |
| M10 | solution: `n` cut by `k` after each digit, not divided | P1 1809, P2 1259, P3 1547, P4 1981, P5 1661, P6 1809 |

## Benchmarks

The bench makes `2 * 10^7` calls of the ★ arm, each `n` from 1 to 100
and base from 2 to 10 drawn from the checksum so far. It checks clean as
first written. Every implementation prints `20000000 calls: checksum
294927554`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.74 s against Rust's 0.62 s (0.63 s with overflow checks
on), C's 0.64 s and Go's 0.71 s; Python takes 6.7 s.
