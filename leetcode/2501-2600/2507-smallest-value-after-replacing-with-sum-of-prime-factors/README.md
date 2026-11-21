# 2507. Smallest Value After Replacing With Sum of Prime Factors

You are given a positive integer `n`.

Continuously replace `n` with the sum of its **prime factors**.

- Note that if a prime factor divides `n` multiple times, it should be
  included in the sum as many times as it divides `n`.

Return *the smallest value* `n` *will take on.*

```
n = 15  ->  5    (15 -> 3 + 5 = 8 -> 2 + 2 + 2 = 6 -> 2 + 3 = 5)
n = 3   ->  3
```

**Constraints:** `2 <= n <= 10^5`.

For `n = a b` with `a, b >= 2`, `a + b <= a b`, with equality only at
`2 2`; so the sum of the prime factors never exceeds `n`, and equals it
only when `n` is a prime or 4. The values only fall, then, until they
stop, and the smallest value is the last: no `n` to `10^5` takes more
than 11 steps. The approaches differ in how they find the prime
factors and how they repeat the step.

## Approaches

| file | mechanism |
|---|---|
| `smallest.kara` ★ | trial division up to the square root of what is left, the leftover above 1 a prime; repeated in a `loop` until the sum equals `n`. O(sqrt(n)) a step |
| `smallest_primes.kara` | the primes to the square root of `n` sieved once, then each step divides by primes only |
| `smallest_odd.kara` | the twos taken out at once by `trailing_zeros` and a shift, then trial division by odd numbers only; the steps in a `while` that compares the next sum |
| `smallest_rec.kara` | recursions: the factor sum of `rest` from divisor `p` up, `p` plus the sum of `rest / p` when `p` divides it, else the sum from `p + 1`; and the smallest value of the sum when it is not `n`. About 330 deep at most |
| `smallest_iter.kara` | iterators: the factor sum `fold`ed over the divisors to the square root, carrying what is left and the sum; the steps a `scan` over the open range `0..` that ends at the first unchanged sum, its `last` value the answer |
| `smallest_solution.kara` | LeetCode's Rust template: `mut n: i32` in, `i32` out; trial division in a `loop` that returns at the first sum equal to `n`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's two examples and eight
more (2, 4, 6, 8, 12, the prime 99991, `2^16` and `10^5`); then every
`n` from 2 to 20000, as a count of those already smallest, which are
the primes and 4, and a checksum; then 2000 random `n` to `10^5`, as a
count of those that end at 5 and a checksum. `smallest.py` mirrors the
★ arm and its output is byte-identical, and the mirror was checked on
every `n` from 2 to `10^5` against repeated steps that take the prime
factors from a sieve of smallest prime factors, and the two agreed on
every `n`.

`check` first reports 2 errors on the template: `struct Solution;` and
the `mut n` parameter. `karac fix` carries it in one call, reporting 6
edits: `struct Solution {}`; the parameter becomes `n: i32` with `let
mut n = n;` as the body's first line, a scalar being copied in already;
`let mut s = 0` and `let mut i = 2` given `: i32`, which their literals
would otherwise not be beside the `i32` comparisons; and the wrapper's
lossless `as i64` dropped.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every number from 2 up to what is left is tried in turn, a
prime factor when it divides and no smaller number from 2 divides it,
divided out as often as it goes and added each time; the sum replaces
`n` until it leaves `n` unchanged. No square root bounds the search. It
checks 300 random `n` to 2000; then 2 to 21; and 40 random `n` to
`10^5`. All 360 are drawn before any arm answers, and 48 of them are
already their smallest.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is at most `n`, and is 4 or a prime |
| P3 | the answer is its own answer |
| P4 | the answer for the sum of `n`'s prime factors is the same |
| P5 | the answer for `2 n` is the answer for that sum plus 2, while `2 n` is at most `10^5` |
| P6 | each arm agrees with at least three of the other five |

P5 holds because the prime factors of `2 n` are those of `n` and one
more 2, so its first step lands on the sum plus 2.

The differential prints `360 cases, 48 already smallest: checksum
169785230, 12960 checks over 6 arms: 0 failures` under every lane in
Verification; the checksum of the literal answers was checked against a
Python reading that builds the same cases and runs trial division. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the last prime left out | P1 359, P2 327, P4 55, P5 98, P6 359 |
| M2 | ★: each prime counted once | P1 238, P4 118, P5 179, P6 238 |
| M4 | ★: a sum one short taken as no change | P1 110, P2 110, P4 1, P5 2, P6 110 |
| M7 | primes: the sieve one short | P1 9, P2 9, P4 19, P5 23, P6 9 |
| M8 | primes: a square left whole | P1 85, P2 52, P4 14, P5 14, P6 85 |
| M10 | primes: every prime but 2 | P1 278, P2 198, P4 166, P5 319, P6 278 |
| M12 | odd: a two worth 3 | P1 290, P2 155, P4 125, P5 257, P6 290 |
| M13 | odd: divisors from 5 | P1 233, P2 125, P4 112, P5 106, P6 233 |
| M14 | odd: divisors stepped by 4 | P1 132, P2 60, P4 85, P5 79, P6 132 |
| M17 | rec: the leftover dropped | P1 360, P2 360, P6 360 |
| M18 | rec: a prime counted once | P1 184, P4 90, P5 135, P6 184 |
| M19 | rec: a square left whole | P1 88, P2 43, P4 16, P5 19, P6 88 |
| M22 | iter: the root never tried | P1 121, P2 121, P4 7, P5 3, P6 121 |
| M23 | iter: the leftover dropped | P1 359, P2 338, P4 29, P5 64, P6 359 |
| M24 | iter: each divisor once | P1 124, P4 65, P5 103, P6 124 |
| M28 | solution: trial from 3 | P1 246, P2 188, P4 108, P5 204, P6 246 |
| M30 | solution: one step only | P1 265, P2 265, P3 265, P4 265, P5 279, P6 265 |

P1 and P6 kill all seventeen, P4 and P5 sixteen each, P2 fourteen, and
P3 one, the template's one step only.

Two of the first thirty-one edits were replaced, both in the odd arm,
for crashing: with the twos counted once each, or the leftover prime
dropped, a sum can reach 0 (2 sums to 1 and 1 to 0, or a prime to 0),
and `0.trailing_zeros()` is 64, a shift out of range that Kāra stops
with a runtime error on both backends. They became a two worth 3 (M12)
and the leftover taken as 2 (M16), whose sums never fall below 2.

Fourteen are not kept, and none survives. Eight fail exactly as a kept
one: the ★ arm's trial from 3 (M3) as the template's (M28); the ★, odd
and rec arms' one step only and the iter arm's first step only (M5,
M15, M20, M25) as the template's one step only (M30); the primes arm's
last prime left out and the template's leftover dropped (M9, M27) as
the ★ arm's last prime left out (M1); and the template's each prime
counted once (M29) as the rec arm's prime counted once (M18). Five fail
as one another, in two sets: the ★ and template arms' divisors stepped
by 2 and the rec arm's next divisor two along (M6, M31, M21), each
trying even divisors only; and the primes and iter arms' even sum taken
as the end (M11, M26). The odd arm's leftover taken as 2 (M16) fails in
a way of its own, but its arm already holds its kept edits.

## Verification

Every arm prints the same output as `smallest.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.3 to 2.0 s and the differential 0.9 s; under `karac __mir-llvm-asan` the arms take 0.3 to 1.2 s and the differential 0.6 s; and under `karac run` the differential takes 0.4 s.

## Benchmarks

The bench makes 14 passes, each asking every `n` from 2 to `10^5`
once, starting from the place the checksum so far picks and wrapping
around, and folding each answer plus the pass into the checksum. The
bench uses the ★ arm in all five languages. Every implementation prints
`14 passes over 2 to 10^5: checksum 360671065`.

BENCHTAB
