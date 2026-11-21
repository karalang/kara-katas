# 2499. Minimum Total Cost to Make Arrays Unequal

You are given two **0-indexed** integer arrays `nums1` and `nums2`, of
equal length `n`.

In one operation, you can swap the values of any two indices of
`nums1`. The **cost** of this operation is the **sum** of the indices.

Find the **minimum** total cost of performing the given operation
**any** number of times such that `nums1[i] != nums2[i]` for all
`0 <= i <= n - 1` after performing all the operations.

Return *the **minimum total cost** such that* `nums1` *and* `nums2`
*satisfy the above condition*. In case it is not possible, return `-1`.

```
nums1 = [1,2,3,4,5], nums2 = [1,2,3,4,5]  ->  10
nums1 = [2,2,2,1,3], nums2 = [1,2,2,3,3]  ->  10
nums1 = [1,2,2],     nums2 = [1,2,2]      ->  -1
```

**Constraints:** `n == nums1.length == nums2.length`; `1 <= n <= 10^5`;
`1 <= nums1[i], nums2[i] <= n`.

Every place where the arrays agree must take part in a swap, so its
index is paid at least once. That is also enough when no value holds
more than half of the agreeing places: they can be paired among
themselves, two different values to a swap, or each swapped through
index 0, which costs nothing. When one value, the mode, holds more,
each place short must be made up by another place whose two values
both differ from the mode, and the cheapest are the lowest such
indices; if there are too few, the answer is -1. The approaches differ
in how they find the mode and the places that help.

## Approaches

| file | mechanism |
|---|---|
| `unequal.kara` ★ | a count per value in a `Vec` of n + 1, the mode its largest, then the lowest helping places while the mode holds more than half. O(n) |
| `unequal_map.kara` | the agreeing values counted in a `Map`, the mode the entry with the greatest count (a tie at the top cannot hold more than half), then places taken while the mode holds more than half of those in play. O(n) expected |
| `unequal_sort.kara` | the agreeing values gathered and sorted, the mode the longest run, then the lowest helping places. O(n log n) |
| `unequal_rec.kara` | the mode kept as the counts grow, then a recursion from index `j` that takes `j` when it helps and asks the rest for what is still short, -1 when the places run out. O(n), O(n) deep |
| `unequal_iter.kara` | iterators: the agreeing indices `filter`ed and `sum`med, the mode `fold`ed from the counts, the helping places `filter`ed and `take`n as many as are short |
| `unequal_solution.kara` | LeetCode's Rust template: `Vec<i32>` twice in, `i64` out; counts in a `vec![0usize; n + 1]` with the mode kept as they come, then helping places added to the swaps until the mode holds no more than half; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 18 lines: LeetCode's three examples and six
more; then, for each chance of agreeing from none in 4 to all, 2000
random pairs of 1 to 40 places with values to 3 or to `n`, as a count
of those that can be made unequal and a checksum; then the
constraints' largest, `10^5` places: two copies of 1 to `n`; values to
2 agreeing three times in four; a 7 on both sides of every third place
and random values elsewhere; and the same with the 7 on two places of
every three. `unequal.py` mirrors the ★ arm and its output is
byte-identical, and the mirror was checked on 3000 random pairs of 1 to
6 places against a least-cost search over every order of nums1 that
swaps reach, and the two agreed on every pair.

`check` first reports 9 errors on the template: `struct Solution;`,
the two `Vec<i32>`, the four `mut` bindings inside
`let (mut ans, mut swaps, mut mode, mut mode_cnt) = ...`, and the two
`&&`. `karac fix` carries it in one call, reporting 16 edits: `struct
Solution {}`; the brackets; `vec![0usize; n + 1]` becomes
`Vec.filled(n + 1, 0usize)`; the pattern becomes `let mut (ans, swaps,
mode, mode_cnt) = (0, 0usize, 0usize, 0usize)`, the `0i64` written `0`;
the two `ans += i as i64` lose their casts; and `&&` becomes `and`.
The `as usize` casts of the values and the `usize` counters stand.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every order of nums1 that swaps can reach is a state, coded
as one number in base 7, each swap of places `i` and `j` an edge of
cost `i + j`, and a least-cost search from the given order, a
`PriorityQueue` of states by cost so far, stops at the first order that
differs from nums2 everywhere, -1 if none is reached. No value is
counted. It checks 300 random pairs of 1 to 6 places, values to 3 or to
`n`, agreeing with a chance from none in 4 to all; then 20 of one
place; and 40 of 6 places with values to 3 agreeing three times in
four. All 360 are drawn before any arm answers, and 184 of them can be
made unequal.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | -1, or at least the sum of the agreeing places' indices and at most the sum of all of them |
| P3 | the two arrays exchanged: the same answer |
| P4 | every value `v` written `n + 1 - v` in both: the same answer |
| P5 | nums2 made a copy of nums1: -1 when one value fills more than half the places, else the sum of all the indices |
| P6 | each arm agrees with at least three of the other five |

P3 holds because a swap in nums1 that makes the arrays differ is the
same swap made in nums2: what matters is which values meet at each
place. P5 holds because every place then agrees, so every index is
paid, and no other place is left to help.

The differential prints `360 cases, 184 can: checksum 275791435, 12960
checks over 6 arms: 0 failures` under every lane in Verification; the
checksum of the literal answers was checked against a Python reading
that builds the same cases and runs the same search. On a failure it
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
| M1 | ★: the mode's count not doubled | P1 204, P5 188, P6 204 |
| M3 | ★: agreeing places allowed to help | P1 50, P2 26, P5 68, P6 50 |
| M5 | ★: the mode looked for below n | P1 103, P4 70, P5 101, P6 103 |
| M8 | map: the agreeing places not put in play | P1 166, P5 172, P6 166 |
| M9 | map: helping places paid one more | P1 42, P2 9, P6 42 |
| M10 | map: the mode's value never kept | P1 54, P6 54 |
| M12 | sort: the first run taken as the mode | P1 34, P4 54, P5 44, P6 34 |
| M13 | sort: runs one short | P1 201, P5 177, P6 201 |
| M14 | sort: the agreeing values unsorted | P1 34, P5 39, P6 34 |
| M19 | rec: places running out answered 0 | P1 176, P5 188, P6 176 |
| M20 | rec: the mode never moved from the first | P1 15, P5 22, P6 15 |
| M21 | rec: the agreeing cost dropped | P1 156, P2 152, P5 172, P6 156 |
| M23 | iter: a helping place may hold the mode in nums2 | P1 31, P3 53, P6 31 |
| M24 | iter: the helping places not paid | P1 28, P6 28 |
| M26 | iter: the agreeing places found where they differ | P1 316, P2 113, P3 50, P5 360, P6 316 |
| M28 | solution: the helping stopped only past half | P1 41, P6 41 |
| M31 | solution: exactly half answered -1 | P1 146, P5 105, P6 146 |

P1 and P6 kill all seventeen, P5 twelve, P2 four, and P3 and P4 two
each.

Fourteen are not kept, and none survives. Six fail exactly as a kept
one: the ★ and sort arms' helping place that may hold the mode in
nums2 (M2, M16) as the iter arm's (M23), each caught by P3 too, since
exchanging the arrays moves the mode to the side the edit still asks;
the ★ and template arms' agreeing places not paid (M4, M30) as the rec
arm's agreeing cost dropped (M21); the rec arm's helping place paid one
more (M18) as the map arm's (M9); and the iter arm's mode looked for
below n (M22) as the ★ arm's (M5), which P4 sees when renumbering moves
the mode to n. Five fail as one another, in two sets: the map, rec and
template arms' helping place that never counts (M7, M17, M27), which
answers -1 on each of the 42 cases where places had to be made up
and could be; and the ★
arm's one place short let pass and the iter arm's one helping place
too few let pass (M6, M25). Three fail in ways of their own, but their
arms already hold their kept edits: the map arm's last place never
asked (M11), the sort arm's shortfall against every place (M15), and
the template's helping place that may hold the mode in nums1 (M29).

## Verification

Every arm prints the same output as `unequal.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.8 to 3.8 s and the differential 0.9 s; under `karac __mir-llvm-asan` the arms take 0.8 to 1.2 s and the differential 0.8 s; and under `karac run` the differential takes 0.6 s.

## Benchmarks

The bench builds 20 pairs of arrays of `10^5` values to 4 once from its
own generator, nums2 agreeing with nums1 at about half the places and
random elsewhere; then makes 33 passes. Each sets one place of every
nums2 from the checksum so far, to nums1's value there or to another,
asks, and puts it back, folding the answer plus 1 plus the pass into
the checksum. The bench uses the ★ arm in all five languages, each
counting into a fresh array of `n + 1` on every ask. Every
implementation prints `33 passes over 20 pairs of 10^5: checksum
739014482`.

BENCHTAB
