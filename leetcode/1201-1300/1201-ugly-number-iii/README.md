# 1201. Ugly Number III

An ugly number is a positive integer that is divisible by `a`, `b`, or
`c`. Given four integers `n`, `a`, `b`, and `c`, return the `n`-th ugly
number.

```
n = 3, a = 2, b = 3, c = 5    ->  4     2, 3, 4, 5, 6, 8, 9, 10, ...
n = 4, a = 2, b = 3, c = 4    ->  6     2, 3, 4, 6, 8, 9, 10, 12, ...
n = 5, a = 2, b = 11, c = 13  ->  10    2, 4, 6, 8, 10, 11, 12, 13, ...
```

**Constraints:** `1 <= n, a, b, c <= 10^9`; `1 <= a * b * c <= 10^18`;
the result is in the range `[1, 2 * 10^9]`.

The arms are `fn nth_ugly_number(n: i64, a: i64, b: i64, c: i64) ->
i64`. The two Rust arms keep the method LeetCode gives Rust users, on
`i32`, inside `impl Solution`, and a one-line `nth_ugly_number` calls
it.

## Approaches

The numbers up to `x` divisible by `a`, `b` or `c` number `x/a + x/b +
x/c - x/lcm(a,b) - x/lcm(b,c) - x/lcm(a,c) + x/lcm(a,b,c)`, by inclusion
and exclusion, and the count only grows with `x`; the answer is the
least `x` whose count reaches `n`. `a * b * c <= 10^18` keeps every
least common multiple inside `i64`.

| file | mechanism |
|---|---|
| `nth_ugly_number.kara` ★ | a binary search on the answer, from 1 to `n * min(a, b, c)`, for the least `x` whose count reaches `n`; the count a closure over the four least common multiples. O(log(n * min)) |
| `nth_ugly_number_lifting.kara` | binary lifting: the largest `x` whose count stays below `n` built a bit at a time, from `2^30` down, and the answer the number after it; `gcd` as a loop |
| `nth_ugly_number_estimate.kara` | an estimate, then steps: `n` over the density of the ugly numbers, in `f64`, lands within a few of the answer; from the ugly number at or below it, counted exactly, the walk steps one ugly number up or down at a time to the `n`-th |
| `nth_ugly_number_subsets.kara` | the count over the seven nonempty subsets of `{a, b, c}` as bitmasks, each subset's least common multiple added or taken away by the parity of its size, and a binary search over 1 to `2 * 10^9` that keeps the best answer found |
| `nth_ugly_number_solution.kara` | a Rust solution as LeetCode's Rust users write it (the arguments widened to `i64`, a nested `fn gcd`, the count as a closure, `let (mut lo, mut hi) = (1i64, 2_000_000_000i64)`), carried to Kāra by `karac fix` |
| `nth_ugly_number_methods.kara` | another Rust solution, the helpers as associated functions (`gcd` with `mut a: i64, mut b: i64`, `lcm`, `count`) called through `Self::`, the upper bound `min(min(a, b), c) * n as i64` and the midpoint by `>> 1`, carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six more properties |

Every arm prints the same 13 lines: LeetCode's three examples; LeetCode's
largest, `n = 10^9` with `b` and `c` near `2 * 10^8` and `3 * 10^8`
(`1999999984`); `a = b = c = 1` for `n = 1` and `10^9`; `a = b = c = 2`
for `n = 10^9`, the result's top, `2 * 10^9`; `a, b, c = 2, 4, 8` (`10`);
`a = b = c = 10^6`, whose product is the constraints' `10^18`; two primes
near `10^9` with `c = 1`, a least common multiple near `10^18`; `6, 10,
15`, no one dividing another (`24`); 1000 random small cases (`1000 small
cases: total 455995, checksum 275673175`); and 1000 random large ones,
`a`, `b`, `c` up to `10^6` and `n` up to the most that keeps the result
within `2 * 10^9` (`1000 large cases: total 595569973407, checksum
221250266`). `nth_ugly_number.py` mirrors the ★ arm with `math.gcd`, and
its output is byte-identical. Every arm gives the same output under
`karac run` and `karac build`, and under the AddressSanitizer build.

The Mend loop: the ★, lifting, estimate and subsets arms check clean as
written. The solution arm takes one round of 10 fixes (among them
`struct Solution;` to `struct Solution {}`, the nested `fn gcd` moved out
to the top level, `let (mut lo, mut hi)` to `let mut (lo, hi)`, the
suffixes of `1i64` and `2_000_000_000i64` dropped, `Solution::` to
`Solution.`, and the `as i64` on the widened call dropped), and the
methods arm one round of 15 (among them the `use std::cmp::min` dropped,
`mut a: i64` to `a: i64` with a `let mut a = a;`, each `Self::gcd`,
`Self::lcm` and `Self::count` to `Solution.gcd`, `Solution.lcm` and
`Solution.count`, and `n as i64` to `n`, the widening now implicit).
Both outputs match.

## Gaps

One, fixed in kara B-2026-11-18-40 at 2e40b2fffa. A Kāra author who
writes the methods arm by hand writes `Self.gcd(a, b)`, as design.md's
keyword table has `Self` for the current type in an expression. Inside
`impl Solution` that was refused with MIR's "a type that failed to check
is not lowered yet" (E0516), a message about the compiler and not about
the program, and the same inside a trait's default body, where there is
no type name to write instead and so no way to call another associated
function of `Self` at all. `Self.f(..)`, `Self.CONST`, `Self.Variant(..)`
and the matching patterns now name the `impl`'s type, and in a default
body the implementing type.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the positive integers walked from 1, each divisible by `a`,
`b` or `c` counted, until the `n`-th. 2000 random cases, `a`, `b` and `c`
from 1 to 12, 30 or 100 and `n` from 1 to 40.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | divisible by `a`, `b` or `c`, at least 1, and at most `n * min(a, b, c)` |
| P3 | `a`, `b` and `c` turned round, `(c, a, b)`, give the same |
| P4 | the `(n + 1)`-th is greater |
| P5 | `a`, `b` and `c` tripled triple the answer |
| P6 | `c` replaced by a multiple of `a` gives what `c = a` gives |
| P7 | the ★ arm's answer |

All 84,000 checks pass on every arm: `2000 cases: checksum 104454231,
84000 checks over 6 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. A Python reading of
the same cases, walking the integers, gives the same checksum.

## Mutation testing

Twelve edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both. All
twelve are caught.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: the three-way multiple never added back | P1 221, P6 344, P7 1105 |
| S2 | ★: a count of exactly `n` not enough | P1 1550, P7 7750 |
| L1 | lifting: the number after it never taken | P1 2000, P2 1578, P5 2000, P7 2000 |
| L2 | lifting: a count of `n` still below | P1 2000, P2 450, P7 2000 |
| E1 | estimate: the walk up stops one short | P1 915, P2 54, P3 95, P4 244, P5 161, P6 97, P7 915 |
| E2 | estimate: the first rank counted one high | P1 2000, P2 60, P7 2000 |
| U1 | subsets: every subset added | P1 1193, P4 501, P6 1432, P7 1193 |
| U2 | subsets: the product for the least common multiple | P1 858, P4 178, P5 728, P6 1322, P7 858 |
| X1 | solution: a count of exactly `n` still below | P1 2000, P2 450, P7 2000 |
| X2 | solution: `lcm(a, b)` for `lcm(a, c)` | P1 891, P2 156, P3 1129, P4 98, P6 1462, P7 891 |
| M1 | methods: the three-way multiple taken away | P1 228, P5 5, P6 354, P7 228 |
| M2 | methods: the upper bound one short | P1 443, P2 207, P4 7, P5 450, P7 443 |

A mutation of the ★ arm fails P7 on all six arms, the ★ arm against the
other five. L2 and X1 are one fault in two arms, the search taking the
`n`-th for one below, and fail alike. S2 and E2 each answer with a
neighbouring ugly number, the `(n + 1)`-th or the `(n - 1)`-th, so only
the literal reading catches them, and P2 only where E2's `(n - 1)`-th is
the `0` before the first. P6, `c` replaced by a multiple of `a`, catches
more of S1, M1, U1, U2 and X2 than the literal reading does, probably
because a `c` that shares `a`'s factors makes the least common multiples
those mutations get wrong small enough to count (inferred, not traced).
M2 fails on the 443 cases whose answer is `n * min(a, b, c)` itself,
where the first `n` ugly numbers are all multiples of the least of the
three. P3
catches only X2, whose `lcm(a, b)` for `lcm(a, c)` is not symmetric, and
E1, probably because the density, summed in another order, rounds the
estimate to the other side of the answer, which E1's short walk up then
misses (inferred, not traced).

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (a binary search on the answer, the count by inclusion and exclusion
over the least common multiples) on 50000 random queries, drawn once,
with a, b and c up to 10^6, 1000 and 30 in turn and n up to the most the
constraints allow; then 10 rounds over the queries, each answer folded
into a checksum. Every program prints `10 rounds of 50000 queries:
checksum 454541870`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.407 to 0.477 s | 0.422 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.410 to 0.450 s | 0.433 s |
| Rust (`rustc -O`) | 0.427 to 0.473 s | 0.440 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.425 to 0.457 s | 0.440 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.427 to 0.461 s | 0.436 s |
| C (`clang -O3`) | 0.412 to 0.452 s | 0.432 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.413 to 0.438 s | 0.423 s |
| Go | 0.564 to 0.604 s | 0.587 s |
| Python | 6.211 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on runs level with Kāra (0.440 s
against 0.433 s), and the two ranges overlap. C runs level with Kāra
(0.432 s against 0.433 s); Kāra is about 26% ahead of Go (0.433 s
against 0.587 s). Python takes about 14x Kāra's time. No profile was
taken.
