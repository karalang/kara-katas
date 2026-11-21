# 2513. Minimize the Maximum of Two Arrays

We have two arrays `arr1` and `arr2` which are initially empty. You need
to add positive integers to them such that they satisfy all the
following conditions:

- `arr1` contains `uniqueCnt1` **distinct** positive integers, each of
  which is **not divisible** by `divisor1`.
- `arr2` contains `uniqueCnt2` **distinct** positive integers, each of
  which is **not divisible** by `divisor2`.
- **No** integer is present in both `arr1` and `arr2`.

Given `divisor1`, `divisor2`, `uniqueCnt1`, and `uniqueCnt2`, return
*the **minimum possible maximum** integer that can be present in either
array*.

```
divisor1 = 2, divisor2 = 7, uniqueCnt1 = 1, uniqueCnt2 = 3  ->  4
divisor1 = 3, divisor2 = 5, uniqueCnt1 = 2, uniqueCnt2 = 1  ->  3
divisor1 = 2, divisor2 = 4, uniqueCnt1 = 8, uniqueCnt2 = 2  ->  15
```

**Constraints:** `2 <= divisor1, divisor2 <= 10^5`; `1 <= uniqueCnt1,
uniqueCnt2 < 10^9`; `2 <= uniqueCnt1 + uniqueCnt2 <= 10^9`.

Up to `x`, the first array can draw on the `x - x / d1` numbers that
`d1` does not divide, the second on `x - x / d2`, and the two together
on the `x - x / lcm` numbers that are not multiples of both, since a
number either array can take is handed out once. `x` is enough exactly
when all three reach their needs, and each only grows with `x`. The
approaches differ in how the least enough `x` is found.

## Approaches

| file | mechanism |
|---|---|
| `minimize.kara` ★ | a binary search for the least enough `x` in `[1, 2 (c1 + c2)]`, the gcd by Euclid's loop. O(log(c1 + c2) + log d) |
| `minimize_closed.kara` | a closed form: the least `x` with `x - x / d >= c` is `c + (c - 1) / (d - 1)`, and the answer the greatest of the three. O(log d) |
| `minimize_gallop.kara` | a galloping search: `x` doubled from 1 until enough, then the gap since the last short `x` bisected; no ceiling assumed |
| `minimize_rec.kara` | recursions: Euclid's gcd, and the binary search as a function of its range. About 31 deep |
| `minimize_iter.kara` | iterators: the gcd a `fold` over Euclid's steps, and the answer built bit by bit from the top by a `fold` that keeps each bit while the number stays short |
| `minimize_solution.kara` | LeetCode's Rust template: four `i32` in, `i32` out; the gcd a `fn` inside the method, a binary search over `i64` up to `i64::MAX / 4`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 14 lines: LeetCode's three examples and five
more; then 2000 random cases with divisors to 10 and counts to 50 in
all, and 2000 with divisors to `10^5` and counts to `10^9` in all, each
as the sum of the answers and a checksum; then the constraints'
largest, `10^9` in all split nine ways, over the divisor pairs (2, 3),
(2, 4), (99999, 100000) and (100000, 100000). `minimize.py` mirrors the
★ arm and its output is byte-identical, and the mirror was checked on
3000 random cases with divisors 2 to 9 and counts 1 to 30 against a
count, for each bound from 1 up, of the numbers only the first array,
only the second, or both can take, and the two agreed on every case.

`check` first reports 7 errors on the template: `struct Solution;`, the
`fn gcd` inside the method, the `mut lo` and `mut hi` inside `let (mut
lo, mut hi)`, `i64::MAX`, and two `&&`. `karac fix` carries it in one
call, reporting 11 edits: `struct Solution {}`; the nested `fn` moved
out to the top level, since Kāra has no nested items and it captures
nothing; `let mut (lo, hi) = (1, i64.MAX / 4)`, the `1i64` suffix
dropped; `and`; and the wrapper's lossless `as i64` dropped. The `lo as
i32` stands.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for each bound `m` from 1 up, a search that hands every
number from 1 to `m` in turn to the first array, the second, or
neither, as each array allows, until both are full; the answer is the
first `m` that can be filled. No count is divided out. It checks 300
random cases of divisors 2 to 6 and counts of 1 to 7 in all; then 20
with both divisors 2; and 40 with counts 4 and 4. All 360 are drawn
before any arm answers, and 182 of them use every number up to the
answer.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | from `c1 + c2` to `2 (c1 + c2) - 1` |
| P3 | the two arrays swapped, divisor with count: the same answer |
| P4 | one more number in the first array: the answer grows by 0 to 2 |
| P5 | the first divisor for both: the same answer as counts `c1 + c2 - 1` and 1 |
| P6 | each arm agrees with at least three of the other five |

P4 holds because each of the three counts grows by one at least every
second number, as no divisor is below 2. P5 holds because with one
divisor for both arrays every allowed number suits either, so only the
total need matters.

The differential prints `360 cases, 182 with no number to spare:
checksum 709933529, 12960 checks over 6 arms: 0 failures` under every
lane in Verification; the checksum of the literal answers was checked
against a Python reading that builds the same cases and counts the
numbers each array alone and both can take. On a failure it prints the
first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M4 | ★: an enough x passed over | P1 240, P2 182, P4 60, P6 240 |
| M5 | ★: the bound c1 + c2 | P1 178, P6 178 |
| M6 | ★: the second count one too many | P1 32, P3 121, P6 32 |
| M7 | closed: the least x one late | P1 119, P2 31, P6 119 |
| M8 | closed: a multiple every d | P1 111, P6 111 |
| M11 | closed: the larger divisor for the lcm | P1 135, P6 135 |
| M12 | gallop: x tripled | P1 60, P2 35, P4 51, P6 60 |
| M13 | gallop: the bisection begun one late | P1 115, P2 4, P4 25, P6 115 |
| M15 | gallop: the bisection turned round | P1 349, P2 239, P4 196, P6 349 |
| M17 | rec: a range of two taken low | P1 140, P2 81, P4 51, P6 140 |
| M19 | rec: the bound 2 c1 + c2 | P1 27, P3 53, P5 61, P6 27 |
| M20 | rec: the shared need one too many | P1 333, P2 33, P6 333 |
| M23 | iter: the bits kept the other way | P1 360, P2 360, P6 360 |
| M24 | iter: the one more left out | P1 360, P2 182, P6 360 |
| M25 | iter: the product for the lcm | P1 126, P5 80, P6 126 |
| M27 | solution: the shared need c1 | P1 270, P2 206, P5 189, P6 270 |
| M28 | solution: a step of two past a short x | P1 282, P2 15, P4 3, P6 282 |

P1 and P6 kill all seventeen, P2 eleven, P4 six, P5 three, and P3 two.

Fourteen are not kept, and none survives. Five fail exactly as a kept
one: the ★ and template arms' product for the lcm (M1, M29) as the iter
arm's (M25); and the ★, closed and gallop arms' shared need dropped or
taken as the larger count (M2, M9, M14) as the template's shared need
`c1` (M27), each blind to a number both arrays could take. Six fail as
one another, in three pairs: the gallop and rec arms' second need `c1`
(M16, M21); the iter and template arms' first need `c2` (M26, M30); and
the iter arm's bit 0 never set and the template's enough `x` passed
over (M22, M31). Three fail in ways of their own, but their arms
already hold their kept edits: the ★ arm's first count against `d2`
(M3), the closed arm's second count against `d1` (M10), and the rec
arm's first need one short (M18).

## Verification

Every arm prints the same output as `minimize.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.2 to 0.4 s and the differential 0.5 s; under `karac __mir-llvm-asan` the arms take 0.3 to 0.5 s and the differential 0.5 s; and under `karac run` the differential takes 0.6 s.

## Benchmarks

The bench builds `10^5` random cases once from its own generator,
divisors to `10^5` and counts to just under `10^9` in all, then makes
10 passes. Each pass asks every case with its first count raised by
`check % 1000`, folding each answer plus the pass into the checksum.
The bench uses the ★ arm in all five languages. Every implementation
prints `10 passes over 10^5 cases: checksum 589924930`.

BENCHTAB
