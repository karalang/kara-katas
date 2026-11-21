# 2485. Find the Pivot Integer

Given a positive integer `n`, find **the pivot integer** `x` such that:

- The sum of all elements between `1` and `x` inclusively equals the
  sum of all elements between `x` and `n` inclusively.

Return *the pivot integer* `x`. If no such integer exists, return `-1`.
It is guaranteed that there will be at most one pivot index for the
given input.

```
n = 8  ->  6
n = 1  ->  1
n = 4  ->  -1
```

**Constraints:** `1 <= n <= 1000`.

The sum of 1 to `x` is `x (x + 1) / 2` and the sum of `x` to `n` is
`n (n + 1) / 2 - x (x - 1) / 2`; they are equal exactly when `x^2` is
`n (n + 1) / 2`. So the pivot is that total's square root when it is a
whole number, and there is none otherwise. Up to 1000 only 1, 8, 49
and 288 have one.

## Approaches

| file | mechanism |
|---|---|
| `pivot.kara` ★ | by the square root: the total `n (n + 1) / 2`, its `f64` root rounded to a whole number, and the square checked. O(1) |
| `pivot_scan.kara` | by running sums: each `x` from 1 to `n` tried in turn, the left sum grown by `x` and the right one, begun at the total, shrunk by the `x` before it, so both include `x` when compared. O(n) |
| `pivot_bisect.kara` | by bisection: the left sum grows with `x` and the right one shrinks, so the least `x` whose left sum is no smaller is found by halving 1 to `n`, and it is the pivot exactly when the two are equal. O(log n) |
| `pivot_pointers.kara` | by two pointers: one from 1 and one from `n`, each with the sum of what it has passed, the side behind moving on until they meet, where the two sums are equal exactly at the pivot. O(n) |
| `pivot_iter.kara` | iterators: `find` over 1 to `n` for the `x` whose `(1..x + 1).sum()` equals `(x..n + 1).sum()`, both summed afresh, and `unwrap_or(-1)`. O(n^2) |
| `pivot_solution.kara` | LeetCode's Rust template: `i32` in and out; the total, its root by `f64` `sqrt` and an `as i32` cast, and the square checked; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's three examples; then
five more, the next two counts with a pivot, 49 and 288, two without,
and the constraints' largest, 1000; then every count from 1 to 1000,
the constraints' whole range, as the counts with a pivot and their
pivots; and 3000 random counts from 1 to 1000, as a checksum. `pivot.py`
mirrors the ★ arm and its output is byte-identical, and the mirror was
checked for every count from 1 to 1000 against every `x` tried with
both sums added up, which also found no count with two pivots. The two
agreed on every count.

`check` first reports 2 errors on the template, the name `Solution`
undeclared where the `impl` and the wrapper use it, and `karac fix`
carries it in one call, reporting 2 edits: `struct Solution {}` is
added, since LeetCode's template leaves it out; and the wrapper's `as
i64` on the `i32` answer goes, since an `i32` widens by itself. The
`as f64` and `as i32` casts, `sqrt()` on an `f64` and the `if` as the
body's value stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every `x` from 1 to `n` tried in turn, both sums added up
afresh, and the first `x` where they are equal taken, -1 when none is.
No formula is used. It checks the four counts with a pivot up to 1000,
each with the counts up to two either side of it that are at least 1,
18 in all, then 342 random counts from 1 to 1000; 6 of the 360 have a
pivot. All are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | an answer other than -1 is a pivot: between 1 and `n`, its square the sum of 1 to `n` |
| P3 | -1 only when no `y` from 1 to `n` has a square that is the sum |
| P4 | a pivot `x` for `n` of 288 or less: the count `3 n + 4 x + 1` has the pivot `2 n + 3 x + 1` |
| P5 | a pivot for `n`: none for `n - 1` or `n + 1` |
| P6 | each arm agrees with at least three of the other five |

P2 and P3 are the square-root reading checked from either side. P4
holds because `x^2 = n (n + 1) / 2` is Pell's equation `(2 n + 1)^2 -
8 x^2 = 1` in disguise, whose solutions step on by `(3, 8; 1, 3)`,
which in `n` and `x` is the step given; it takes 1 to 8, 8 to 49, 49
to 288 and 288 to 1681, past the constraints' 1000, where every arm
reads the count the same way. P5 holds because the totals for `n - 1`
and `n + 1` are `n` and `n + 1` away from `x^2`, while the nearest other
squares are `2 x - 1` and `2 x + 1` away, and with `x` about `0.71 n`
that is farther whenever `n` is 8 or more, as every count with a pivot
but 1 is; beside 1, the count 2 has the total 3.

The differential prints `360 cases: checksum 50726426, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and adds up the same sums. On a failure it prints the
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
| M1 | ★: the total as n squared over 2 | P1 8, P2 4, P3 4, P4 4, P6 8 |
| M3 | ★: a root at least the total's | P1 197, P2 197, P5 163, P6 197 |
| M4 | ★: the total of 1 to n - 1 | P1 14, P2 10, P3 4, P4 9, P5 4, P6 14 |
| M7 | scan: the left sum short of x | P1 9, P2 3, P3 6, P4 3, P6 9 |
| M8 | scan: the right sum losing one more | P1 7, P2 3, P3 4, P4 5, P6 7 |
| M9 | scan: the right sum begun one over | P1 10, P2 4, P3 6, P6 10 |
| M14 | bisect: the high end one too far down | P1 2, P3 2, P4 4, P6 2 |
| M15 | bisect: the left sum one short | P1 12, P2 8, P3 4, P4 9, P5 4, P6 12 |
| M16 | bisect: none answered as minus the meeting place | P1 354, P2 354, P4 96, P5 360, P6 354 |
| M17 | pointers: the right sum begun one short | P1 8, P2 2, P3 6, P6 8 |
| M18 | pointers: the right sum one over each step | P1 6, P2 2, P3 4, P4 3, P6 6 |
| M20 | pointers: the answer one over | P1 6, P2 6, P4 6, P6 6 |
| M23 | iter: the right sum without n | P1 14, P2 8, P3 6, P4 7, P6 14 |
| M24 | iter: 1 never tried | P1 2, P3 2, P6 2 |
| M25 | iter: none answered 0 | P1 354, P2 354, P4 112, P5 360, P6 354 |
| M27 | solution: the root one under | P1 6, P3 6, P6 6 |
| M30 | solution: a root at most the total's | P1 354, P2 354, P5 360, P6 354 |

P1 and P6 kill all seventeen, P2 fourteen, P3 twelve, P4 eleven, and P5 six.

Fourteen are not kept. Eleven fail exactly as a kept one. The ★ arm's
and the template's none answered 0 (M2, M29) fail as the iter arm's
(M25); the ★ arm's root one over and the template's total not halved
(M5, M28) as the template's root one under (M27); the scan arm's last
`x` never tried (M10) as the iter arm's 1 never tried (M24); the scan
arm's answer one over (M11) as the pointers arm's (M20); the bisect
arm's right sum without `x` and the iter arm's left and right sums
without `x` (M13, M22, M26) as the scan arm's left sum short of `x`
(M7); the pointers arm's left sum begun at 0 (M19) as the scan arm's
right sum begun one over (M9); and the pointers arm's stopping a place
apart (M21) as the scan arm's right sum losing one more (M8). The other
three, the ★ arm's root of half the total, the bisect arm's pivot passed
over and the template's root of `n` (M6, M12, M31), fail the same checks
as one another, P1, P3 and P6 on four cases and P4 on two, so at most
one of them could be kept, and the arms they belong to already hold
their share with failures of their own.

One edit was replaced before this table was drawn: the pointers arm's
left side moving on a tie, which survived every check. It changes which
side moves only when the two sums are equal before the sides meet, which
happens at some step for most counts, yet a Python copy of the arm with
and without the edit gives the same answer for every count from 1 to
4000, four times the constraints' bound, so it was taken as equivalent
there. It was replaced by the right sum begun one short (M17).

## Verification

Every arm prints the same output as `pivot.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.2 to 0.5 s, but for the iter arm's 237 s (its O(n^2) sums, 4000 counts up to 1000 summed afresh), and the differential 26 s; under `karac __mir-llvm-asan` the arms take 0.3 to 0.7 s, the iter arm 192 s, and the differential 22 s; and under `karac run` the differential takes 0.6 s.

## Benchmarks

The bench makes 24000 passes over every count from 1 to 1000, each pass
starting at a count chosen by the checksum so far, so no pass repeats
the last, folding each answer plus the pass into the checksum. The
bench uses the ★ arm in all five languages; C takes the root with
`__builtin_sqrt` of a `__builtin_fabs` and rounds by adding a half, so
its link needs no `-lm`, as the bench script builds it. The work per
answer is a multiplication, a root and a comparison, so the bench
measures the call and the checksum's arithmetic as much as the answer.
Every implementation prints `24000 passes over every count from 1 to
1000: checksum 413123399`.

BENCHTAB
