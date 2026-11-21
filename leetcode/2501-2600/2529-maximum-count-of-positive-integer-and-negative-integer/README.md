# 2529. Maximum Count of Positive Integer and Negative Integer

Given an array `nums` sorted in **non-decreasing** order, return *the
maximum between the number of positive integers and the number of
negative integers.*

- In other words, if the number of positive integers in `nums` is `pos`
  and the number of negative integers is `neg`, then return the maximum
  of `pos` and `neg`.

**Note** that `0` is neither positive nor negative.

```
nums = [-2, -1, -1, 1, 2, 3]     ->  3
nums = [-3, -2, -1, 0, 0, 1, 2]  ->  3
nums = [5, 20, 66, 1314]         ->  4
```

**Constraints:** `1 <= nums.length <= 2000`; `-2000 <= nums[i] <= 2000`;
`nums` is sorted in a **non-decreasing order**.

The order puts the negatives in a prefix and the positives in a suffix,
with any zeros between them, so the two counts are two positions. The
approaches differ in how they find them, and one does not use the order
at all.

## Approaches

| file | mechanism |
|---|---|
| `count.kara` ★ | two binary searches, for the first number above -1 and the first above 0; the negatives the one, the positives `n` less the other. O(log n) |
| `count_tally.kara` | one pass counting each sign, the order not used. O(n) |
| `count_walk.kara` | two walks inward from the ends, from the left while the numbers are negative and from the right while they are positive. O(n) |
| `count_rec.kara` | the ★ arm's binary search as a recursion on the half still open, at most 12 deep |
| `count_iter.kara` | iterators: the negatives a `take_while` from the front, the positives a `take_while` over the list `rev`ersed, each `count`ed |
| `count_solution.kara` | LeetCode's Rust template: `Vec<i32>` in, `i32` out, each count from a `partition_point`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's three examples and five
more, among them a single 0, a single `-2000`, and zeros before one
positive; then 3000 random sorted lists of 1 to 40 numbers from -5 to 5
and 1000 of 1 to 2000 from -2000 to 2000, as the sum of the answers and
a checksum. `count.py` mirrors the ★ arm and its output is
byte-identical, and the mirror was checked on 5000 random sorted lists
of 1 to 30 numbers from -4 to 4 against the two signs counted one by
one, and the two agreed on every list.

`check` reported nothing on the five Kāra arms as first written.

`check` first reports 6 errors on the template: the unit struct
`struct Solution;`, Rust's `Vec<i32>`, the three `&x` closure patterns,
and the path call `Solution::maximum_count`. `karac fix` carries it in
one call, reporting 8 edits: `struct Solution {}`, the two brackets of
`Vec[i32]`, the three `&` dropped, `Solution.`, and the `as i64` on the
call's result, which an `i32` widens to without a cast. The library's
`partition_point` is the template's own.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the numbers above 0 counted, the numbers below 0 counted,
and the larger of the two counts. It checks 300 random sorted lists of
1 to 12 numbers from -3 to 3, and 60 of 1 to 200 from -2000 to 2000.
All 360 are drawn before any arm answers, and 4 of them hold no number
but 0.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is at most `n`, and at least half the nonzero numbers |
| P3 | every number negated, the list reversed: the same answer |
| P4 | a 0 put in its sorted place: the same answer |
| P5 | every number doubled in place: twice the answer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases, 4 with no sign: checksum 523107786,
12960 checks over 6 arms: 0 failures` under every lane in Verification;
the checksum of the literal answers was checked against a Python
reading that builds the same lists and counts the two signs. On a
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
| M4 | ★: the search not past the middle | P1 132, P2 10, P3 188, P4 139, P5 104, P6 132 |
| M5 | ★: the first not below instead of above | P1 183, P2 30, P3 202, P4 283, P6 183 |
| M6 | ★: the negatives alone | P1 132, P2 132, P3 283, P6 132 |
| M9 | tally: the first number skipped | P1 169, P2 63, P3 248, P4 18, P5 169, P6 169 |
| M10 | tally: the sum of the counts | P1 304, P6 304 |
| M11 | tally: a negative counted twice | P1 282, P2 122, P3 283, P6 282 |
| M14 | walk: the right walk stopped a number early | P1 75, P2 34, P3 156, P4 75, P5 75, P6 75 |
| M15 | walk: the walks compared by position | P1 230, P2 84, P3 283, P4 360, P6 230 |
| M16 | walk: the left walk one short | P1 17, P2 11, P3 35, P4 17, P5 17, P6 17 |
| M18 | rec: the comparison with above plus 1 | P1 194, P2 35, P3 202, P4 301, P6 194 |
| M19 | rec: the search ending a place late | P1 105, P2 7, P3 159, P4 113, P5 160, P6 105 |
| M20 | rec: the positives from n minus 1 | P1 132, P2 59, P3 283, P5 132, P6 132 |
| M22 | iter: the zeros taken as negatives | P1 133, P3 127, P4 263, P6 133 |
| M23 | iter: the positives from the front | P1 114, P2 114, P3 248, P4 18, P6 114 |
| M24 | iter: the positives by filter | P1 115, P3 127, P4 238, P6 115 |
| M29 | solution: the positives alone | P1 151, P2 151, P3 283, P6 151 |
| M30 | solution: the numbers halved on the way | P1 208, P2 143, P6 208 |

P1 and P6 kill all seventeen, P3 fifteen, P2 fourteen, P4 eleven, and
P5 six.

One of the first thirty-one edits survived and was replaced: the rec
arm's lower half taken as `lo..mid.max(lo)`, where `mid` is never below
`lo`, is the arm itself. It became the rec arm's comparison with
`above + 1` (M18).

Fourteen are not kept, and none survives. Eleven fail exactly as a kept
one. The zeros counted as negatives in the ★, rec and template arms and
the walk arm's left walk through zeros (M1, M17, M28, M12) fail as the
iter arm's zeros taken as negatives (M22); the zeros counted as
positives in the ★, tally, walk, iter and template arms (M2, M7, M13,
M26, M27) as the iter arm's positives by filter (M24), which counts the
zeros among them too; the tally arm's positives alone (M8) as the
template's (M29); and the iter arm's last number skipped (M25) as the
rec arm's positives from `n - 1` (M20), each one positive short. The
other three, the ★, rec and template arms' smaller count (M3, M21,
M31), fail in one way of their own, in arms that already hold their
kept edits.

## Verification

Every arm prints the same output as `count.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.2 to 2.9 s and the differential 0.5 s; under `karac __mir-llvm-asan` the arms take 0.6 to 0.9 s and the differential 0.6 s; and under `karac run` the differential takes 0.6 s.

## Benchmarks

The bench builds 1000 random sorted lists of 2000 numbers once from its
own generator, each drawn from -2000 to 2000 around a shift of its own
and clipped to that range, so the lists run from mostly negative to
mostly positive. Then it makes 3000 passes. Each pass asks every list,
starting at an offset the checksum so far picks, and folds each answer
plus the pass into the checksum. The bench uses the ★ arm in all five
languages. Every implementation prints `3000 passes over 1000 lists of
2000 numbers: checksum 92343018`.

BENCHTAB
