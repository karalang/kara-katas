# 2427. Number of Common Factors

Given two positive integers `a` and `b`, return *the number of **common**
factors of* `a` *and* `b`.

An integer `x` is a **common factor** of `a` and `b` if `x` divides both
`a` and `b`.

```
a = 12, b = 6   ->  4     (1, 2, 3, 6)
a = 25, b = 30  ->  2     (1, 5)
```

**Constraints:** `1 <= a, b <= 1000`.

A number divides both `a` and `b` exactly when it divides their greatest
common divisor, so the common factors are the divisors of `gcd(a, b)`.
Euclid's algorithm finds the gcd, and its divisors pair up as `d` and
`g / d` with `d <= sqrt(g)`, so the count needs at most 31 steps here.

## Approaches

| file | mechanism |
|---|---|
| `factors.kara` ★ | the gcd by Euclid's algorithm in a loop, then `d` walked up to `sqrt(g)`, each divisor counting 2 for itself and `g / d`, a square root 1. O(log min(a, b) + sqrt(g)) |
| `factors_naive.kara` | the statement read directly: every `x` from 1 to the smaller of `a` and `b`, counted when it divides both. O(min(a, b)) |
| `factors_sets.kara` | the divisors of `a` and of `b` each gathered into a `SortedSet[i64]`, walking to the square root and keeping `d` and `n / d`, and the size of their `intersection`. O(sqrt(a) + sqrt(b)) |
| `factors_primes.kara` | the gcd by recursion, factored by trial division: `p1^e1 ... pk^ek` has `(e1 + 1) ... (ek + 1)` divisors, a prime left over above the square root counting twice. O(log min(a, b) + sqrt(g)) |
| `factors_iter.kara` | iterators: the gcd as the first `x` from the smaller value down, by `rev` and `find`, that divides both, then its divisors by `filter` and `count`. O(min(a, b)) |
| `factors_solution.kara` | LeetCode's Rust template: the gcd by a recursive associated function called through `Self::gcd`, and its divisors counted over `1..=g` by `filter(\|&x\| ..)` and `count() as i32`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples; 1 and 1; the
constraints' largest, 1000 twice; two primes; one dividing the other;
720 and 840, whose gcd 120 has 16 divisors; then every pair from 1 to
200, and 3000 random pairs from 1 to 1000, the second a multiple of a
random factor of the first half the time, each as a checksum and the
total. `factors.py` mirrors the ★ arm and its output is byte-identical,
and the mirror was checked on every `a` from 1 to 1000 against every
seventh `b` against every `x` tested.

`check` first reports 4 errors on the template, and `karac fix` carries
it in one call, reporting 4 edits: each `Self::gcd` written
`Solution.gcd`, since Kāra names the type and writes a path with `.`;
the `&` of the pattern `|&x|` dropped; and `struct Solution;` given its
braces. The inclusive range `1..=g`, the recursion, `if b == 0 { a }
else { .. }` on one line and `count() as i32` stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every `x` from 1 to the larger of `a` and `b` tried, and
counted when it divides both. No gcd is taken. It checks 300 random
pairs from 1 to 1000, drawn as the harness draws them; then 30 pairs of
one value twice; then 30 pairs of products of the primes 2, 3, 5 and 7
up to 1000, rich in divisors. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | `a` and `b` swapped: the same answer |
| P3 | both multiplied by the least prime from 2 to 13 that does not divide both: twice the answer |
| P4 | `b` replaced by `a + b`: the same answer |
| P5 | no more than the factors of `a` alone, and exactly 1 against 1 |
| P6 | each arm agrees with at least three of the other five |

P3 holds because a prime `q` that does not divide the gcd makes it `q
g`, whose divisors are those of `g` and `q` times each of them. It takes
the values past 1000, up to 13000, outside the constraints; every arm
holds for any positive values. P4 holds because `gcd(a, a + b)` is
`gcd(a, b)`, and P5 because every common factor is a factor of `a`, and
only 1 divides 1.

The differential prints `360 cases: checksum 203418081, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and tests every `x`. On a failure it prints the first
ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: the square root never reached | P1 204, P3 204, P5 360, P6 204 |
| M4 | ★: the remainder halved | P1 191, P2 212, P3 219, P4 174, P5 17, P6 191 |
| M6 | ★: the gcd itself never counted | P1 180, P3 180, P5 360, P6 180 |
| M8 | naive: a factor of either counted | P1 317, P3 297, P4 320, P5 273, P6 317 |
| M9 | naive: half the range tried | P1 51, P3 51, P4 8, P5 360, P6 51 |
| M11 | naive: odd factors counted twice | P1 360, P3 246, P5 360, P6 360 |
| M12 | sets: only the small divisors | P1 61, P3 27, P4 7, P6 61 |
| M15 | sets: the divisors of a taken for b | P1 317, P2 283, P3 88, P5 353, P6 317 |
| M16 | sets: the difference counted | P1 255, P2 283, P3 88, P5 352, P6 255 |
| M18 | primes: a last prime of 2 missed | P1 47, P3 227, P6 47 |
| M19 | primes: only even trial divisors after 2 | P1 43, P3 44, P6 43 |
| M21 | primes: the count started at 2 | P1 360, P5 360, P6 360 |
| M22 | iter: the least common factor taken as the gcd | P1 180, P3 360, P6 180 |
| M24 | iter: a factor of a taken as the gcd | P1 263, P2 259, P3 82, P4 160, P6 263 |
| M26 | iter: 1 never counted | P1 360, P3 360, P5 360, P6 360 |
| M30 | solution: the gcd capped at 500 | P1 21, P3 32, P6 21 |
| M31 | solution: a off by one | P1 261, P2 208, P3 324, P4 221, P5 153, P6 261 |


P1 and P6 kill all seventeen, P3 sixteen, P5 eleven, P4 six and P2
five.

Fourteen are not kept. Seven fail exactly as a kept one: the ★ arm's
square root counted twice (M1) as its square root never reached (M2),
since both miscount only a square gcd, by one each way; the ★ arm's gcd
of `a` with itself (M5) as the sets arm's divisors of `a` taken for `b`
(M15), both counting the factors of `a`; the naive arm's smaller value
never tried (M7) as its half the range tried (M9), since no factor lies
between half the smaller value and the value itself; the naive arm's 1
never tried, the iter arm's gcd itself never counted and the template's
(M10, M23, M27) as the iter arm's 1 never counted (M26), each one short
everywhere; and the iter arm's multiples of the gcd counted (M25) as its
least common factor taken as the gcd (M22), both answering 1. Seven fail
apart from every kept one and were left out because those arms keep
their share already: the ★ arm's 1 never counted (M3); the sets arm's
square root never reached and union counted (M13, M14); the primes
arm's exponent counted, not one more, and each prime divided out once
(M17, M20); and the template's remainder of 1 taken as the end and
remainder of 1 counted (M28, M29).

## Verification

Every arm prints the same output as `factors.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.3 to 0.9 s, but for the iter
arm, which takes 3.1 s there and 0.4 s under `karac run`: it finds the
gcd by trying every value down from the smaller one through a closure.
The differential takes 1.6 s under `karac __mir-run`, 0.8 s under
`karac __mir-llvm-asan` and 0.6 s under `karac run`.

## Benchmarks

The bench answers every pair from 1 to 1000, the whole of the
constraints, in 5 passes, pass `p` pairing `a` with the `b` that many
places on, wrapping past 1000, and folds each answer plus the pass into
the checksum. Nothing is built ahead: each call takes its gcd and walks
its divisors afresh. The bench uses the ★ arm, Euclid's gcd and a walk
to its square root, in all five languages. Every implementation prints
`5 passes over 10^6 pairs: checksum 860816479`.

BENCHTAB
