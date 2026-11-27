# 1808. Maximize Number of Nice Divisors

You are given a positive integer `primeFactors`. You are asked to
construct a positive integer `n` that satisfies the following
conditions: the number of prime factors of `n` (not necessarily
distinct) is at most `primeFactors`, and the number of nice divisors of
`n` is maximized. A divisor of `n` is nice if it is divisible by every
prime factor of `n`; for `n = 12`, whose prime factors are `[2,2,3]`,
`6` and `12` are nice divisors, while `3` and `4` are not. Return the
number of nice divisors of `n`. Since that number can be too large,
return it modulo `10^9 + 7`.

```
primeFactors = 5  ->  6     (n = 200, prime factors [2,2,2,5,5], nice divisors 10, 20, 40, 50, 100, 200)
primeFactors = 8  ->  18
```

**Constraints:** `1 <= primeFactors <= 10^9`.

The arms are `fn max_nice_divisors(prime_factors: i32) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `max_nice_divisors.kara` ★ | a nice divisor takes every prime of `n` at least once, so prime exponents `e1..ek` give `e1 * .. * ek` nice divisors, and the answer is the largest product of parts summing to `primeFactors`: all 3s, with a 4 when 1 is left over and a 2 when 2 is. The power of 3 is taken by squaring, right to left over the exponent's bits. O(log n) |
| `max_nice_divisors_recursive.kara` | the same product, the remainder's part picked by a `match` on a tuple and the power of 3 by a recursion that halves the exponent. O(log n) |
| `max_nice_divisors_topdown.kara` | the same product, the power of 3 taken left to right over the exponent's 31 bits, squaring for each bit and multiplying by 3 for each set bit. O(log n) |
| `max_nice_divisors_table.kara` | the same product, the power read off a table of `3^(2^k)` for `k` from 0 to 30 built by squaring, one entry multiplied in for each set bit, and the remainder's part indexed from the array `[1, 4, 2]`. O(log n) |
| `max_nice_divisors_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `const MOD` and a `fn pow(mut a: i64, mut b: i64)` nested in the method, `1_000_000_007`, `b & 1` and `b >>= 1`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's two examples (`6 18`); the
edges, 1 to 7, which cover each remainder and the counts too small to
split, and the constraints' most, `10^9` and the two below it (`1 2 3 4
6 9 12 897135186 172851386 448567593`); every count from 1 to 2000 (`1
to 2000: checksum 774991023`); and 3000 at random to `10^9` (`3000 at
random to 10^9: checksum 854680120`). `max_nice_divisors.py` mirrors the
★ arm, and its output is byte-identical. Every arm gives the same output
under `karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`.

The Mend loop: the ★, recursive, topdown and table arms and the harness
check clean as first written. The Rust solution takes 15 fixes by `karac
fix`'s count, and its diff is: the nested `const MOD` and `fn pow` moved
above the `impl`, with `struct Solution {}` added; `pow`'s `mut a` and
`mut b` parameters to plain parameters rebound by `let mut a = a;` and
`let mut b = b;`; and `Solution::` to `Solution.` in the harness.
`1_000_000_007`, `b & 1` and `b >>= 1` are Kāra as they stand. Every
arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the largest product of parts summing to `primeFactors`, found
by trying every last part over a table of the best product for each
smaller total, in exact `i64` arithmetic, which holds up to 100 factors.
The cases are every count from 1 to 1000, `10^9` and the two below it,
and 997 at random to `10^9`. Each arm meets six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally, for up to 100 factors |
| P2 | from 2 factors on, three more factors multiply the answer by 3 |
| P3 | a remainder of 1 turns a part of 3 into a 4, so the answer times 3 is the answer for one factor fewer times 4, and a remainder of 2 adds a part of 2 to the answer for two fewer |
| P4 | for a multiple of 3, twice as many factors square the answer |
| P5 | the answer lies from 1 to `10^9 + 6`, and is the count itself up to 4 |
| P6 | the ★ arm's answer |

The differential checks clean as first written. All 60,000 checks pass
on every arm: `2000 cases: checksum 204291152, 60000 checks over 5 arms:
0 failures`, under `karac __mir-run`, `karac run`, `karac build` and
`karac __mir-llvm-run`. Python, running the ★ arm's mirror over the same
cases, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash. Two first
drafts survived because they compute the same answer, and were replaced:
the recursive arm's remainder of 2 written as one 3 fewer and a 6, which
is `3^(k - 1) * 6 = 3^k * 2`, and the solution's early return widened to
4 factors, whose answer is 4.

| | edit | failures by property |
|---|---|---|
| M1 | ★: a remainder of 1 left as a part of 1, not a 3 made a 4 | P1 33, P3 679, P5 1, P6 2716 |
| M2 | ★: the base never squared | P1 94, P2 978, P3 334, P4 508, P6 7976 |
| M3 | recursive: an odd step multiplied by 3, not by the squared base | P1 94, P2 978, P3 334, P4 508, P6 1994 |
| M4 | recursive: a remainder of 0 given a 4 in place of a 3 | P1 32, P2 1, P3 1329, P4 508, P6 666 |
| M5 | topdown: only the exponent's low 20 bits read | P4 75, P6 997 |
| M6 | topdown: a remainder of 2 left out | P1 32, P2 1, P3 652, P6 652 |
| M7 | table: the parts for remainders 1 and 2 swapped | P1 65, P2 1, P3 1331, P5 1, P6 1331 |
| M8 | table: each entry multiplied by 3, not squared | P1 88, P2 473, P3 162, P4 507, P6 1988 |
| M9 | solution: 5 factors answered as 5 by the early return | P1 1, P2 2, P3 1, P6 1 |
| M10 | solution: the exponent's second bit read in place of its first | P1 96, P2 1019, P3 345, P4 262, P6 1996 |

## Benchmarks

The bench makes `2 * 10^6` calls of the ★ arm, each count of prime
factors drawn from the checksum so far. It checks clean as first
written. Every implementation prints `2000000 calls: checksum
283274430`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.34 s against Rust's 0.34 s (0.34 s with overflow checks
on), C's 0.35 s and Go's 0.43 s; Python takes 7.5 s.
