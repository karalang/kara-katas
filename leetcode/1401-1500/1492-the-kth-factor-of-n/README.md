# 1492. The kth Factor of n

You are given two positive integers `n` and `k`. A factor of an integer
`n` is defined as an integer `i` where `n % i == 0`. Consider a list of
all factors of `n` sorted in ascending order, return the `k`th factor in
this list or return `-1` if `n` has less than `k` factors.

```
n = 12, k = 3  ->  3
n = 7, k = 2   ->  7
n = 4, k = 4   ->  -1
```

**Constraints:** `1 <= k <= n <= 1000`.

The arms are `fn kth_factor(n: i32, k: i32) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `kth_factor.kara` ★ | every i from 1 to n tried in order, counting those that divide n until the kth. O(n) |
| `kth_factor_sqrt.kara` | the factors up to the square root found in order; each pairs with n / i, so a k past them is read off the small ones backwards, a square's root counted once. O(√n) |
| `kth_factor_filter.kara` | an iterator: `(1..=n).filter(\|i\| n % i == 0).nth(k - 1) ?? -1`. O(n) |
| `kth_factor_recursive.kara` | recursion on the candidate, with the factors still to pass, one call per candidate. O(n) calls deep |
| `kth_factor_solution.kara` | a Rust solution as LeetCode's Rust users write it (`let mut k = k;` counted down), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read another way, five more properties |

Every arm prints the same 4 lines: LeetCode's three examples (`3 7 -1`);
seven edges, n = 1, the last factor of 1000 and one past it, a prime's
second factor, a square's middle factor, and 720's thirtieth factor and
one past it (`1 1000 -1 997 30 720 -1`); every n up to 200 with every k
up to n, folded in order (`n up to 200: 1098 factors found, checksum
439418545`); and 20000 random pairs up to the constraints' most (`20000
random pairs: checksum 409263499`). `kth_factor.py` mirrors the ★ arm,
and its output is byte-identical. Every arm gives the same output under
`karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`.

The Mend loop: the ★, filter and recursive arms check clean as first
written. The square-root arm was first written `let mut i = 1;` for a
counter tried as `while i * i <= n` and pushed into a `Vec[i32]`; a
comparison with an `i32` does not fix a literal's type (design.md §8
Literals), so check refused the push, naming `i`, and `karac fix`
declared it `i: i32`. The Rust solution takes one round of 2 fixes by
`karac fix`'s count, `struct Solution;` to `struct Solution {}` and
`Solution::` to `Solution.`. Every arm's output matches on the first
run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
another way: n's prime factors found, every product of their powers
built, the products sorted, and the kth of them taken, or -1. LeetCode's
examples, the edges, and 1990 random pairs, n up to 500 so that 2n stays
near the constraints, and k up to two past n's factor count. Each arm
meets six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read another way |
| P2 | a factor of n, or -1 exactly when n has fewer than k |
| P3 | the (k + 1)th factor is larger, or there is none |
| P4 | the kth factor times the kth from the other end is n |
| P5 | 2n has every factor of n, so its kth factor is no larger |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 cases: checksum 258782719,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, listing the
divisors by trial, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: each factor counted twice | P1 1742, P2 1020, P4 1452, P6 6968 |
| M2 | ★: n itself never tried | P1 306, P2 306, P4 634, P6 1224 |
| M3 | sqrt: a square's root counted as two factors | P1 38, P2 13, P3 14, P4 46, P5 10, P6 38 |
| M4 | sqrt: one factor fewer counted, so the last is never found | P1 687, P2 306, P4 1439, P6 687 |
| M5 | filter: the (k + 1)th factor taken | P1 1453, P2 306, P4 1452, P6 1453 |
| M6 | filter: 1 never counted | P1 1453, P2 306, P4 1452, P6 1453 |
| M7 | recursive: the factor before the kth taken | P1 1718, P2 595, P4 1452, P6 1718 |
| M8 | recursive: n itself never tried | P1 306, P2 306, P4 634, P6 306 |
| M9 | solution: the factor before the kth taken | P1 1388, P2 265, P3 330, P4 1452, P6 1388 |
| M10 | solution: 0 where there is no kth factor | P1 547, P2 547, P3 853, P5 547, P6 547 |

## Benchmarks

The bench makes 400 passes over every n up to 1000, each n's k from 1 to
40 chosen from the checksum so far, so most calls stop at a small factor
and some walk to n. Every implementation prints `400 passes over n up to
1000: checksum 784656293`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.40 s against Rust's 0.39 s (0.40 s with overflow checks
on), C's 0.42 s and Go's 0.40 s; Python takes 6.0 s.
