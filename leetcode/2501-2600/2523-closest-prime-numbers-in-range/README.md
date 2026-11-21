# 2523. Closest Prime Numbers in Range

Given two positive integers `left` and `right`, find the two integers
`num1` and `num2` such that:

- `left <= num1 < num2 <= right`.
- Both `num1` and `num2` are prime numbers.
- `num2 - num1` is the **minimum** amongst all other pairs satisfying
  the above conditions.

Return the positive integer array `ans = [num1, num2]`. If there are
multiple pairs satisfying these conditions, return the one with the
**smallest** `num1` value. If no such numbers exist, return `[-1, -1]`.

```
left = 10, right = 19  ->  [11, 13]
left = 4, right = 6    ->  [-1, -1]
```

**Constraints:** `1 <= left <= right <= 10^6`.

The closest pair is always two neighbouring primes of the range, since
a prime between them would make a closer pair, so one walk over the
primes in order, keeping the last one seen and moving the best only on
a strictly smaller gap, finds it with the smallest `num1`. The
approaches differ in how the primes are found.

## Approaches

| file | mechanism |
|---|---|
| `closest.kara` ★ | a sieve of Eratosthenes to `right`, then one walk over the range keeping the last prime. O(right log log right) |
| `closest_trial.kara` | trial division of each number of the range by the divisors to its square root, with no table; the walk stops at the first gap of at most 2, since only 2 and 3 are closer and they come first |
| `closest_segmented.kara` | a segmented sieve: the primes to the square root of `right` first, then only the range marked, each base prime crossing out its multiples from the first in the range. The table is the range's width |
| `closest_rec.kara` | recursion: divide and conquer over the range, each half reporting a `Stretch` (its first prime, its last, and its closest pair), the left half's pair, the straddling pair and the right half's preferred in that order on a tie. At most 21 deep |
| `closest_iter.kara` | iterators: the sieve's marks a `fold` over the numbers to the square root, crossing out by `step_by`; the range's primes a `filter`; the closest pair a `fold` over their `windows(2)` |
| `closest_solution.kara` | LeetCode's Rust template: `i32` in, `Vec<i32>` out; a `vec![true; n + 1]` sieve over `usize` indices and the best gap held as an `i32::MAX` sentinel; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 13 lines: LeetCode's two examples and eight
more; then 2000 random ranges of width 0 to 99 within 1 to `10^4`, and
30 of width 0 to 9999 within 1 to `10^6`, as how many have no pair, the
sum of the gaps, and a checksum; then the constraints' largest, 1 to
`10^6`. `closest.py` mirrors the ★ arm and its output is
byte-identical, and the mirror was checked on 3000 random ranges of
width 0 to 200 within 1 to 3000 against the closest of every pair of
primes found by trial division, ties to the smaller `num1`, and the two
agreed on every range.

`check` reported errors on two arms as first written. The rec arm wrote
`let (mut a, mut b) = ..`, Rust's placement of `mut`; the error says
that in Kāra `mut` goes before the whole pattern, and `karac fix`
rewrote it as `let mut (a, b) = ..`. The iter arm called `fold` on the
`Vec` that `windows(2)` returns; the error asks for an explicit
`.into_iter()`, which `karac fix` inserted. The same call drew three
more errors, `tuple index on non-tuple type` on the closure's `best`,
whose type could not be inferred without the receiver; they went away
with the fix. A warning also named the rec arm's first struct `Span`
as shadowing a prelude type, and the struct is called `Stretch`.

`check` first reports 5 errors on the template: `struct Solution;`,
`Vec<i32>` in angle brackets, the path `i32::MAX`, the `&&` operator,
and the path call `Solution::closest_primes`. `karac fix` carries it in
one call, reporting 11 edits: `struct Solution {}`; the brackets; `n`
cast `as i64` where it was `as usize`; `vec![true; n + 1]` becomes
`Vec.filled(n + 1, true)`; the two `vec![..]` literals written `[..]`;
`i32.MAX`; the index's `as usize` dropped; `and`; and
`Solution.closest_primes`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a prime is a number with exactly two divisors, counted in
pairs up to its square root; every pair of primes `num1 < num2` in the
range is tried, not only neighbours, and the pair with the smallest gap
and then the smallest `num1` wins. No sieve. It checks 300 random
ranges of width 0 to 40 within 1 to 500, 30 of width 0 to 100 within 1
to 50000, and 30 starting at 1 to 5 of width 0 to 9. All 360 are drawn
before any arm answers, and 77 of them have no pair.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | `[-1, -1]`, or two primes of the range, `num1 < num2`, a gap of 1 only for `[2, 3]` |
| P3 | the range one wider at each end, kept within 1 to `10^6`: a gap no larger |
| P4 | the range cut to the answer itself: the same answer |
| P5 | the range cut to end at the answer's `num2`: the same answer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases, 77 with no pair: checksum
224875573, 12960 checks over 6 arms: 0 failures` under every lane in
Verification; the checksum of the literal answers was checked against a
Python reading that builds the same cases and tries every pair of
primes. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a tie moving the pair | P1 69, P6 69 |
| M2 | ★: the sieve below the square root | P1 1, P2 1, P3 1, P6 1 |
| M4 | ★: right left out | P1 20, P4 269, P5 269, P6 20 |
| M7 | trial: the walk stopped at a gap of 4 | P1 65, P3 6, P6 65 |
| M9 | trial: divisors below the square root | P1 40, P2 40, P6 40 |
| M10 | trial: a tie moving the pair | P1 10, P6 10 |
| M12 | segmented: the first multiple one too far | P1 147, P2 147, P3 112, P6 147 |
| M13 | segmented: the crossing from the first multiple | P1 12, P3 1, P5 5, P6 12 |
| M14 | segmented: the root one short | P1 35, P2 35, P3 2, P4 6, P5 11, P6 35 |
| M17 | rec: the straddling pair never tried | P1 283, P6 283 |
| M18 | rec: a tie going right | P1 57, P6 57 |
| M19 | rec: the first prime taken from the right | P1 30, P3 9, P5 8, P6 30 |
| M22 | iter: windows of 3 | P1 100, P4 230, P5 230, P6 100 |
| M24 | iter: the range from left, 1 included | P1 5, P2 5, P6 5 |
| M25 | iter: the crossing stepped by p + 1 | P1 314, P2 314, P6 314 |
| M29 | solution: prev moved only on a new best | P1 56, P3 1, P6 56 |
| M31 | solution: the pair written backwards | P1 283, P2 283, P3 19, P4 283, P5 283, P6 283 |

P1 and P6 kill all seventeen, P3 eight, P2 seven, P5 six, and P4 four.

One of the first thirty-one edits survived and was replaced: the ★
arm's crossing from `2 p` rather than `p * p` marks the same composites,
every multiple below `p * p` having a smaller prime factor already
crossed out, so the edit is equivalent. It became the ★ arm's widest gap
kept (M6).

Fourteen are not kept, and none survives. Twelve fail exactly as a kept
one. Four read 1 as a prime, failing as the iter arm's range from
`left` with 1 included (M24): the ★ arm's walk from `left`, the trial
arm's 1 taken as prime, the rec arm's 1 left unmarked and the
template's 1 left prime (M3, M8, M21, M28). The ★ and trial arms' last
prime moved only on a new best (M5, M11) fail as the template's (M29);
the segmented, iter and template arms' tie moving the pair (M15, M23,
M27) as the ★ arm's (M1); the segmented arm's `right` left out (M16) as
the ★ arm's (M4); the iter arm's sieve to the square root only (M26) as
the ★ arm's sieve below the square root (M2), both leaving the square
of the largest prime unmarked when it is `right`; and the template's
crossing from `i * i + i` (M30) as the trial arm's divisors below the
square root (M9), both taking the squares of primes as primes. The ★
arm's widest gap kept (M6) and the rec arm's last prime taken from the
left (M20) fail in ways of their own, but their arms already hold their
kept edits.

## Verification

Every arm prints the same output as `closest.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.4 to 15.5 s and the differential 3.1 s; under `karac __mir-llvm-asan` the arms take 0.4 to 3.1 s and the differential 1.4 s; and under `karac run` the differential takes 0.9 s.

## Benchmarks

The bench makes 150 queries. Each asks the range of width `10^4` ending
at `right = check % 500000 + 500001`, from 500001 to `10^6`, and answers
it with a fresh sieve to `right`, folding the pair and the query into
the checksum. The bench uses the ★ arm in all five languages. Every
implementation prints `150 queries to 10^6: checksum 779334431`.

BENCHTAB
