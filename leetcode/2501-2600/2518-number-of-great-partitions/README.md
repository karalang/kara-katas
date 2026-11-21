# 2518. Number of Great Partitions

You are given an array `nums` consisting of **positive** integers and an
integer `k`.

**Partition** the array into two ordered **groups** such that each
element is in exactly **one** group. A partition is called great if the
**sum** of elements of each group is greater than or equal to `k`.

Return *the number of **distinct** great partitions*. Since the answer
may be too large, return it **modulo** `10^9 + 7`.

Two partitions are considered distinct if some element `nums[i]` is in
different groups in the two partitions.

```
nums = [1,2,3,4], k = 4  ->  6
nums = [3,3,3], k = 4    ->  0
nums = [6,6], k = 2      ->  2
```

**Constraints:** `1 <= nums.length, k <= 1000`; `1 <= nums[i] <=
10^9`.

A partition is the subset in the first group. It fails when either
group sums below `k`; when the total is at least `2 k` the two groups
cannot both be short, and as many partitions leave the first group short
as the second, so the answer is `2^n` less twice the subsets summing
below `k`, and 0 when the total is below `2 k`. Those subsets are
counted by a knapsack over the sums below `k`, which the numbers of
`10^9` never enter. The approaches differ in how the knapsack is held.

## Approaches

| file | mechanism |
|---|---|
| `great.kara` ★ | one row of counts for the sums below `k`, each number added from the top sum down. O(n k) |
| `great_table.kara` | the full table, row `i` the counts for the first `i` numbers, built from the row above by leaving the number out or taking it in. O(n k) time and space |
| `great_sums.kara` | a `SortedMap` from each sum below `k` that some subset reaches to its count, every number adding a shifted copy of the sums it still fits under `k` |
| `great_rec.kara` | recursion: the subsets of the numbers from place `i` on that fit in a room, memoized over the place and the room, and `2^n` by halving the power. At most 1000 deep |
| `great_iter.kara` | iterators: the row of counts a `fold` over the numbers, each step a fresh row `map`ped from the last, the short subsets its `fold`ed sum, and `2^n` a `fold` too |
| `great_solution.kara` | LeetCode's Rust template: `Vec<i32>` and `i32` in, `i32` out; the total summed as `i64` through `map(\|&x\| x as i64)`, the knapsack a `vec![0i64; k]` walked from the top over `usize` sums, and the short count a `sum::<i64>()`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 15 lines: LeetCode's three examples and five
more; then 2000 random lists of 1 to 10 numbers to 20 with `k` from 1
to 30, and 2000 of 1 to 200 numbers to 10 and 2000 to `10^9`, each with
`k` to 1000, as the lists with none and a checksum; then the
constraints' largest, 1000 numbers with `k` 1000: all 1, all 1000, 1 to
1000, and random to `10^9`. `great.py` mirrors the ★ arm and its output
is byte-identical, and the mirror was checked on 3000 random lists of 1
to 10 numbers to 20 with `k` from 1 to 40 against a count of every
subset whose sum and whose complement's both reach `k`, and the two
agreed on every list.

`check` first reports 6 errors on the template: `struct Solution;`,
`Vec<i32>` in angle brackets, the `&x` patterns of the closure and of
`for &x in &nums`, the `&nums` borrow, and the turbofish in
`sum::<i64>()`. `karac fix` carries it in one call, reporting 12 edits:
`struct Solution {}`; the brackets; the two `&` patterns dropped; `for x
in ref nums`; the turbofish dropped, the binding's `i64` naming the
sum; `vec![0i64; k]` becomes `Vec.filled(k, 0)`; the two `as usize`
casts written `as i64`, an index being `i64`; and the wrapper's
lossless `as i64` dropped.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every partition, made by a recursion that puts each number
in the first group or the second, counted when both groups sum to at
least `k`. No knapsack and no complement. It checks 300 random lists of
1 to 10 numbers to 20 with `k` from 1 to 30; then 20 of 12 ones with
`k` from 1 to 7; and 40 of 8 numbers to `10^9` with `k` to 1000. All
360 are drawn before any arm answers, and 93 of them have no great
partition.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | even, and at most `2^n - 2` |
| P3 | the numbers in the reverse order: the same answer |
| P4 | every number doubled, and `k` doubled: the same answer |
| P5 | `k` one more: at most the answer |
| P6 | each arm agrees with at least three of the other five |

P2 holds because swapping the groups of a great partition gives another,
and neither group may be empty.

The differential prints `360 cases, 93 with no great partition:
checksum 391411075, 12960 checks over 6 arms: 0 failures` under every
lane in Verification; the checksum of the literal answers was checked
against a Python reading that builds the same cases and tries every
subset. On a failure it prints the first ten and then the count by
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
| M1 | ★: the total tested against k | P1 30, P2 30, P5 2, P6 30 |
| M3 | ★: the short taken once | P1 278, P2 161, P6 278 |
| M6 | ★: the last sum below k left out | P1 149, P2 11, P4 149, P6 149 |
| M8 | table: a number fitting only below s | P1 200, P6 200 |
| M9 | table: the last row left out | P1 132, P3 119, P6 132 |
| M11 | table: the sums from 1 | P1 278, P2 144, P3 119, P6 278 |
| M12 | sums: a sum of k kept | P1 148, P2 1, P5 5, P6 148 |
| M13 | sums: a reached sum overwritten | P1 127, P6 127 |
| M15 | sums: the first number skipped | P1 277, P2 17, P3 119, P5 5, P6 277 |
| M17 | rec: a number filling the room left out | P1 138, P4 138, P6 138 |
| M18 | rec: each end counted twice | P1 278, P2 47, P5 12, P6 278 |
| M21 | rec: a total of 2 k refused | P1 1, P6 1 |
| M22 | iter: the first row all ones | P1 267, P2 144, P4 278, P5 12, P6 267 |
| M24 | iter: 2^n begun at 2 | P1 278, P2 278, P6 278 |
| M25 | iter: the empty subset left out of the short | P1 278, P2 78, P6 278 |
| M27 | solution: the sums walked upward | P1 166, P2 55, P5 9, P6 166 |
| M31 | solution: each number taken in twice | P1 200, P2 72, P5 10, P6 200 |

P1 and P6 kill all seventeen, P2 twelve, P5 seven, and P3 and P4 three
each.

Two of the first thirty-one edits survived and were replaced: the table
and template arms' total tested against `2 k - 1`. A total of `2 k - 1`
leaves every subset or its complement short, so the knapsack already
counts `2^(n - 1)` short subsets and the answer comes out 0 without the
test; both edits are equivalent. They became the table arm's sums from 1
(M11) and the template's each number taken in twice (M31).

Fourteen are not kept, and none survives. Thirteen fail exactly as a
kept one. Six fail as the iter arm's `2^n` begun at 2 (M24), on every
list whose total reaches `2 k`: the ★ arm's `2^n` begun at 2 and empty
subset not counted, the rec arm's odd power not doubled and number
never left out, and the template's `all` begun at 2 and `dp[0]` left at
0 (M4, M5, M19, M20, M28, M30). The table arm's number never taken in
and the iter arm's number fitting only below `s` (M7, M23) fail as the
table arm's (M8); the table arm's `2^(n - 1)` and the sums arm's empty
subset twice (M10, M14) as the rec arm's each end counted twice (M18);
the ★ arm's sums walked upward (M2) as the template's (M27), each
counting a number more than once; the iter arm's last number left out
(M26) as the table arm's last row left out (M9); and the template's
`bad` taken once (M29) as the ★ arm's short taken once (M3). The sums
arm's short taken once and 1 more (M16) fails in a way of its own, but
its arm already holds its kept edits.

## Verification

Every arm prints the same output as `great.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 14.0 to 68.7 s and the differential 2.1 s; under `karac __mir-llvm-asan` the arms take 3.3 to 13.9 s and the differential 0.9 s; and under `karac run` the differential takes 0.5 s.

## Benchmarks

The bench builds 20 random lists of 1000 numbers from 1 to 1000 once
from its own generator, then makes 35 passes. Each pass asks every list
with `k` from 1 to 1000, `check % 1000 + 1`, folding each answer plus
the pass into the checksum. The bench uses the ★ arm in all five
languages. Every implementation prints `35 passes over 20 lists of 1000
numbers: checksum 437031791`.

BENCHTAB
