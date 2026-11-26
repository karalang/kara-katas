# 1780. Check if Number is a Sum of Powers of Three

Given an integer `n`, return `true` if it is possible to represent `n`
as the sum of distinct powers of three. Otherwise, return `false`. An
integer `y` is a power of three if there exists an integer `x` such that
`y == 3^x`.

```
n = 12  ->  true    (12 = 3^1 + 3^2)
n = 91  ->  true    (91 = 3^0 + 3^2 + 3^4)
n = 21  ->  false
```

**Constraints:** `1 <= n <= 10^7`.

The arms are `fn check_powers_of_three(n: i32) -> bool`.

## Approaches

| file | mechanism |
|---|---|
| `check_powers_of_three.kara` ★ | n is a sum of distinct powers of three exactly when no digit of n in base 3 is a 2, so the digits are read off from the lowest. O(log n) |
| `check_powers_of_three_greedy.kara` | greedy from 3^14, the largest power of three not above 10^7: each power is taken when it fits, since the powers below it sum to less than it, and n is a sum when nothing is left. O(log n) |
| `check_powers_of_three_recursive.kara` | recursion on the lowest base-3 digit, a `match` on `n % 3` with a guard for 0: a 0 or 1 leaves `n / 3` to check, a 2 fails. O(log n) |
| `check_powers_of_three_sums.kara` | every sum of distinct powers of three up to n listed, each power doubling the list, and n looked for among them. O(n) |
| `check_powers_of_three_solution.kara` | a Rust solution as LeetCode's Rust users write it (`mut n: i32`, `n /= 3`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's three examples (`true true
false`); five edges, 1, 2, a power of three, one more than a power, and
every digit 1 in base 3 (`true false true true true`); the constraints'
most, 10^7, then the sum of every power of three below it and one more
than that (`the most: false true false`); and 3000 random numbers, half
of them sums of distinct powers and the rest one to three more (`3000
random cases: checksum 941003098`). `check_powers_of_three.py` mirrors
the ★ arm, and its output is byte-identical. Every arm gives the same
output under `karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`.

The Mend loop: the ★, greedy and recursive arms check clean as first
written. The sums arm was first written with `let mut power = 1`,
compared with the `i32` n and added into the `Vec[i32]` sums; check
named `power` an `i64`, since an operator or a method does not fix a
literal's type (design.md §8 Literals), and `karac fix` wrote `power:
i32`, 1 fix. The Rust solution takes one round of 4 fixes by `karac
fix`'s count, and its diff is: `struct Solution;` to `struct Solution
{}`, `mut n: i32` to `n: i32` with `let mut n = n;` at the body's start,
since a parameter's mode is written in its type, and `Solution::` to
`Solution.`. Every arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every choice of distinct powers of three up to n, kept when
it sums to n. LeetCode's examples, the edges, the constraints' most, and
1988 random numbers from 1 to a bound of 1 to 3000. Each arm meets six
properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | 3n and 3n + 1 give the same answer as n, while they are within the constraints |
| P3 | a number one more than a multiple of three, or a power of three, is a sum when n / 3 is |
| P4 | 3n + 2 is never a sum, while it is within the constraints |
| P5 | n is a sum exactly when the largest power of three not above it leaves less than itself, and that rest is 0 or a sum |
| P6 | the ★ arm's answer |

`karac fix` wrote `top: i32` for the differential's own largest power
below n, for the same reason as the sums arm, 1 fix. All 60,000 checks
pass on every arm: `2000 cases: checksum 557937801, 60000 checks over 5
arms: 0 failures`, under `karac __mir-run`, `karac run`, `karac build`
and `karac __mir-llvm-run`. Python, trying every choice of powers, gives
the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: a digit 1 taken as the one that fails | P1 326, P2 114, P3 73, P4 114, P5 280, P6 1304 |
| M2 | ★: the digits read in base 2 | P1 318, P2 550, P3 124, P5 402, P6 1272 |
| M3 | greedy: the largest power, 3^14, never tried | P1 1, P3 1, P5 1, P6 1 |
| M4 | greedy: a power equal to what is left never taken | P1 212, P5 19, P6 212 |
| M5 | recursive: a digit 1 taken as the one that fails | P1 326, P2 114, P3 73, P4 114, P5 280, P6 326 |
| M6 | recursive: 0 taken as no sum | P1 212, P5 19, P6 212 |
| M7 | sums: a power equal to n never listed | P1 19, P2 19, P5 67, P6 19 |
| M8 | sums: each power added twice over | P1 326, P2 114, P3 73, P4 114, P5 280, P6 326 |
| M9 | solution: a leading digit 2 let through | P1 144, P5 302, P6 144 |
| M10 | solution: n stepped down by 3, not divided | P1 1120, P2 667, P5 475, P6 1120 |

## Benchmarks

The bench runs the ★ arm on every n from 1 to 10^7, five rounds over,
folding the sums into a checksum. Every implementation prints `5 rounds
of 1 to 10000000: 163835 sums, checksum 10024802`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra is ahead of Rust here at 0.137 s against Rust's 0.145 s (0.137 s
with overflow checks on), C's 0.118 s and Go's 0.158 s; Python takes
11.0 s.
