# 2344. Minimum Deletions to Make Array Divisible

You are given two positive integer arrays `nums` and `numsDivide`. You
can delete any number of elements from `nums`.

Return *the **minimum** number of deletions such that the **smallest**
element in* `nums` ***divides** all the elements of* `numsDivide`. If
this is not possible, return `-1`.

Note that an integer `x` divides `y` if `y % x == 0`.

```
nums = [2,3,2,4,3], numsDivide = [9,6,9,3,15]   ->  2
nums = [4,3,6],     numsDivide = [8,2,6,10]     ->  -1
```

**Constraints:** `1 <= nums.length, numsDivide.length <= 10^5`;
`1 <= nums[i], numsDivide[i] <= 10^9`.

A value divides every value of `numsDivide` exactly when it divides
their gcd, so the question is the smallest value of `nums` that divides
one number. Deleting everything below it, and nothing else, leaves it
the smallest; its copies stay, since they divide too.

## Approaches

| file | mechanism |
|---|---|
| `divisible.kara` ★ | the gcd of `numsDivide`; `nums` sorted and scanned for the first value that divides it, whose place is the answer. O(n log n + m log max) |
| `divisible_scan.kara` | two scans, no sort: the least value that divides the gcd, then the count of values below it. O(n + m log max) |
| `divisible_heap.kara` | the values on a `PriorityQueue`, smallest first, popped and counted as deletions until one divides the gcd. O(n + d log n) for d deletions |
| `divisible_naive.kara` | no gcd: each value tried as the smallest kept, held to dividing every value of `numsDivide` in turn, and the fewest values below a candidate that passes. O(n (n + m)) |
| `divisible_iter.kara` | iterators: the gcd by `fold`, the least dividing value by `filter` and `min`, and the values below it by `filter` and `count`, all through `map` on the `Option` |
| `divisible_solution.kara` | LeetCode's Rust template: a nested `fn gcd` folded over `numsDivide`, `sort_unstable`, and `iter().position` mapped to `-1` through `map_or`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; a 1 against
`10^9`; no value dividing; `10^9` dividing itself after three
deletions; 2000 values against the multiples of 180; then 2000 random
cases of 1 to 12 values up to 2 to 31 against 1 to 6 multiples of a
base from 1 to 12, with a checksum, the answers' sum and how many are
possible. `divisible.py` mirrors the ★ arm and its output is
byte-identical, and the mirror was checked against the statement read
literally on 3000 random cases.

The gcd in the four arms that keep one was first written
`let (mut a, mut b) = (a, b);`, as in Rust. `check` refuses it, since
in Kāra `mut` goes before the whole pattern, and `karac fix` makes it
`let mut (a, b) = (a, b);` in three edits.

`karac fix` carries the template in one call, reporting 12 edits.
`check` first reports 6 errors and offers 10 edits for them: the
nested `fn gcd` moved out to the top level, two edits, since Kāra has
no nested items; `mut nums: Vec<i32>` to `nums: own Vec[i32]` with
`let mut nums = nums;` opening the body, two; the four brackets of the
two `Vec<i32>`s; and the `&` of `|acc, &x|` and `|&x|` dropped. The
other two follow from those: `sort_unstable` to `sort`, and the
wrapper's `as i64` on the `i32` answer dropped, since it widens on its
own. `fold`, `position` and `map_or` stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each value of `nums` tried as the smallest one kept, kept
only when it divides every value of `numsDivide` one by one, and the
deletions it needs counted as the values below it; the fewest of those,
or -1. No gcd and no sorting. It checks 300 random cases of 1 to 12
values up to 2 to 31 against 1 to 6 multiples of a base from 1 to 12;
then 30 of up to 300 values up to `10^6` against up to 50 multiples of
one of them; then 30 of up to 300 values up to 100 against up to 50
multiples of a base up to 100. All 360 are drawn before any arm
answers; 195 of the first 300 and 56 of the last 60 are possible.

| | property |
|---|---|
| P1 | up to 12 values, the answer is the literal reading's |
| P2 | -1 exactly when no value of `nums` divides every value of `numsDivide`, and otherwise from 0 to one less than the number of values |
| P3 | `nums` reversed: the same answer |
| P4 | every value of both arrays three times itself, where that stays within `i32`: the same answer |
| P5 | a 1 added to `nums`: 0 |
| P6 | each arm agrees with at least three of the other five |

P4 holds because `x` divides `y` exactly when `3x` divides `3y`, and
tripling keeps the order of the values. P5 holds because 1 divides
everything and nothing is below it.

The differential prints `360 cases: checksum 784005231, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and tests each candidate with `all`. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the gcd started at 1 | P1 92, P2 129, P4 122, P6 129 |
| M4 | ★: divisibility read the other way | P1 212, P2 178, P5 340, P6 240 |
| M6 | ★: only the last value of `numsDivide` | P1 49, P2 43, P6 52 |
| M7 | scan: the largest dividing value kept | P1 92, P5 210, P6 114 |
| M8 | scan: copies of the kept value deleted too | P1 195, P2 13, P5 360, P6 251 |
| M10 | scan: no dividing value read as 0 | P1 105, P2 109, P6 109 |
| M12 | heap: the first value that does not divide | P1 300, P2 128, P5 360, P6 360 |
| M13 | heap: two deletions counted per value | P1 28, P2 31, P6 58 |
| M15 | heap: one deletion too few | P1 195, P2 193, P5 360, P6 251 |
| M17 | naive: divisibility read the other way | P1 199, P2 251, P5 357, P6 255 |
| M18 | naive: the value just below never counted | P1 15, P4 17, P6 17 |
| M21 | naive: the best started at 0 | P1 133, P2 109, P6 167 |
| M22 | iter: a 1 never kept | P1 103, P2 41, P4 122, P5 360, P6 122 |
| M23 | iter: the values above counted | P1 183, P5 358, P6 239 |
| M26 | iter: the first value never kept | P1 29, P2 20, P3 47, P6 31 |
| M28 | solution: the sort left out | P1 115, P3 199, P5 279, P6 164 |
| M30 | solution: one deletion too many | P1 195, P2 12, P5 360, P6 251 |

P1 and P6 kill all seventeen, P2 thirteen, P5 ten, P4 three and P3
two. P2 misses the edits that still answer -1 exactly when nothing
divides and a count within range, only the wrong one: the largest
dividing value kept, the values above counted, the value just below
never counted, the sort left out. P5, a 1 added, fails where an edit
cannot answer 0 for it: the largest dividing value kept, the values
above counted, divisibility read the other way, a 1 never kept, a
deletion too many or too few. P4, both arrays tripled, fails where an
edit leans on the number 1 or on a gap of one: the gcd started at 1,
a 1 never kept, the value just below never counted. P3, `nums`
reversed, fails only where an edit depends on their order: the sort
left out and the first value never kept.

Of the thirty-one, fourteen were not kept. The gcd started at 1 in the
heap arm (M14) and the template (M31) fails as in the ★ arm (M1), which
is kept. The ★ arm's gcd returning the spent remainder (M2), the naive
arm's every value taken to divide (M20) and the template's gcd
returning 0 (M27) all answer 0 wherever the literal reading does not,
and fail as the naive arm's best started at 0 (M21), which is kept. The
sort left out of the ★ arm (M3) fails as in the template (M28); one
deletion too many in the ★ arm (M5) as in the template (M30); only the
last value of `numsDivide` in the ★ arm (M6) as the gcd of the last
value alone in the scan arm (M9); divisibility read the other way in
the ★ arm (M4) as in the scan arm (M11); the largest dividing value
kept in the scan arm (M7) as the most deletions kept in the naive arm
(M19); no dividing value read as 0 in the scan (M10), heap (M16) and
iter (M24) arms alike; and the first value that does not divide in the
heap (M12), iter (M25) and template (M29) arms alike. Of each group
only the first named is kept. The naive arm's copies of the kept value
deleted too and the iter arm's largest dividing value kept first failed
as the scan arm's M8 and M7, and were replaced by the value just below
never counted (M18) and a 1 never kept (M22).

## Verification

Every arm prints the same output as `divisible.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.26 to 0.35 s. The
differential takes 0.85 s there and 0.66 s under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 10 cases once, each `10^5` values from 1 to `10^6`
from a scramble, against `10^4` multiples of one of those values, then
makes 20 passes, pass `p` folding each answer plus `p` into the
checksum, with the ★ arm in all five languages. The answers range from
0 to 79990. Every implementation prints `20 passes over 10 cases of
10^5 values against 10^4: checksum 958794937`. Each copies and sorts
the `10^5` values on every call, as 64-bit integers: C with `qsort`,
Go with `slices.Sort`, Python with `sorted`, Rust and Kāra with their
stable `sort`.

BENCHTAB
