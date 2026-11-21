# 2498. Frog Jump II

You are given a **0-indexed** integer array `stones` sorted in
**strictly increasing order** representing the positions of stones in a
river.

A frog, initially on the first stone, wants to travel to the last stone
and then return to the first stone. However, it can jump to any stone
**at most once**.

The **length** of a jump is the absolute difference between the
position of the stone the frog is currently on and the position of the
stone to which the frog jumps.

- More formally, if the frog is at `stones[i]` and is jumping to
  `stones[j]`, the length of the jump is `|stones[i] - stones[j]|`.

The **cost** of a path is the **maximum length of a jump** among all
jumps in the path.

Return *the **minimum** cost of a path for the frog*.

```
stones = [0,2,5,6,7]  ->  5
stones = [0,3,9]      ->  9
```

**Constraints:** `2 <= stones.length <= 10^5`; `0 <= stones[i] <= 10^9`;
`stones[0] == 0`; `stones` is sorted in a strictly increasing order.

Using a stone between the ends never makes a jump longer, so every one
is used on the way out or the way back. Two neighbours on the same way
leave the other way a jump over both, at least as long as the span of
any two-stone alternation would ask, so the best is to alternate: out
on one stone of every two, back on the rest. Every jump then spans two
neighbouring gaps, and with only two stones the one jump is the gap.
The approaches differ in how they find that cost.

## Approaches

| file | mechanism |
|---|---|
| `frog.kara` ★ | the first gap, then every span `stones[i] - stones[i - 2]`, the largest kept. O(n) |
| `frog_search.kara` | binary search on the cost: a guess is enough when the frog can go out on every other stone and back on the rest with no longer jump, walked stone by stone. O(n log(last stone)) |
| `frog_paths.kara` | the two paths built as lists, the even places and the last stone out, the last and the odd places back to the first, and the longest jump on either. O(n) |
| `frog_rec.kara` | recursion from the end: the cost up to stone `i` the larger of its span over one stone and the cost up to `i - 1`. O(n), O(n) deep |
| `frog_iter.kara` | iterators: the stones `zip`ped with themselves `skip(2)` along, `map`ped to spans and `fold`ed from the first gap. O(n) |
| `frog_solution.kara` | LeetCode's Rust template: `Vec<i32>` in, `i32` out; the first gap, then `windows(3)`, the largest `w[2] - w[0]`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 14 lines: LeetCode's two examples and seven
more; then 2000 random rows of 2 to 50 stones with gaps to 10 and 2000
with gaps to `10^6`, each as a checksum; then the constraints' largest,
`10^5` stones: 0 to 99999; random gaps to `10^4`, the last stone under
`10^9`; and spread evenly to near `10^9`. `frog.py` mirrors the ★ arm
and its output is byte-identical, and the mirror was checked on 3000
random rows of 2 to 8 stones against every way of giving each middle
stone to the way out, the way back or neither, and the two agreed on
every row.

`check` first reports 2 errors on the template: `struct Solution;` and
`Vec<i32>`. `karac fix` carries it in one call, reporting 4 edits:
`struct Solution {}`; the brackets; and the wrapper's `as i64` on the
template's answer is dropped, since an `i32` widens to `i64` on its
own. `stones.windows(3)` and the `w[2] - w[0]` it gives stand as
written.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every stone between the ends is given one of three lots, the
way out, the way back or unused, by counting in base 3; each lot's path
is walked from the first stone to the last, and the least of the
longest jumps is taken. Nothing alternates. It checks 300 random rows
of 2 to 8 stones with gaps to 3 or to `10^6`; then 20 of two stones;
and 40 of 9 stones with gaps to `10^4`. All 360 are drawn before any
arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | at least the widest gap, and at most the last stone |
| P3 | every stone doubled: twice the answer |
| P4 | the row turned round, each stone's distance from the last: the same answer |
| P5 | every stone doubled and one put halfway between each two: twice the widest gap |
| P6 | each arm agrees with at least three of the other five |

P2 holds because one of the two ways must cross the widest gap, and no
jump passes the last stone. P5 holds because, with a stone between
every two old ones, alternating puts the old neighbours one jump apart,
twice their gap, and every new stone between them.

The differential prints `360 cases: checksum 586346434, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the
checksum of the literal answers was checked against a Python reading
that builds the same cases and tries the same lots. On a failure it
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
| M3 | ★: the last stone left out | P1 114, P2 30, P4 159, P5 123, P6 114 |
| M5 | ★: the loop begun at 3 | P1 92, P2 18, P4 159, P5 119, P6 92 |
| M6 | ★: only the last span kept | P1 150, P2 40, P4 222, P5 201, P6 150 |
| M7 | search: the way back begun at the third stone | P1 46, P4 81, P6 46 |
| M8 | search: the way back one jump to the last | P1 208, P4 180, P5 289, P6 208 |
| M9 | search: the search's top one short | P1 94, P2 54, P3 101, P5 61, P6 94 |
| M12 | paths: the last left off the way out | P1 71, P4 52, P5 123, P6 71 |
| M13 | paths: the way back on even places | P1 85, P4 101, P6 85 |
| M16 | paths: the first jump of each path skipped | P1 211, P2 87, P4 85, P5 119, P6 211 |
| M17 | rec: the first gap never asked | P1 61, P2 61, P6 61 |
| M18 | rec: spans of neighbours | P1 299, P5 360, P6 299 |
| M20 | rec: the recursion two back | P1 82, P4 101, P6 82 |
| M24 | iter: the least kept | P1 299, P2 226, P4 209, P5 360, P6 299 |
| M25 | iter: spans read backwards | P1 299, P2 197, P4 249, P5 360, P6 299 |
| M26 | iter: only the first span | P1 167, P2 59, P4 222, P5 197, P6 167 |
| M28 | solution: neighbours' gaps | P1 299, P2 62, P4 120, P5 360, P6 299 |
| M31 | solution: every span one more | P1 299, P2 40, P3 299, P5 360, P6 299 |

P1 and P6 kill all seventeen, P4 and P5 thirteen each, P2 eleven, and
P3 two.

Fourteen are not kept, and none survives. Eleven fail exactly as a
kept one: the ★, iter and template arms' first gap never asked (M1,
M23, M27) as the rec arm's (M17), wrong on the 61 rows whose answer is
the first gap; the ★ arm's spans of neighbours and the iter arm's
stones zipped one along (M2, M22) as the rec arm's spans of neighbours
(M18); the ★, rec and template arms' least kept (M4, M21, M29) as the
iter arm's (M24); the paths arm's only the way out asked (M15) as its
way back on even places (M13), since both leave the odd stones' jumps
unasked; the rec arm's rest never asked (M19) as the ★ arm's only the
last span kept (M6); and the template's windows of four (M30) as the ★
arm's last stone left out (M3), since both lose the last span. Three
fail in ways of their own, but their arms already hold their three:
the search arm's jump equal to the guess refused on the way out and
guess that fits passed over (M10, M11), and the paths arm's last left
off the way back (M14).

One edit was replaced before this table was drawn. The paths arm's
first left off the way back survived every check: the way back then
ends at the second stone, but the jump it drops, the first gap, is
never longer than the way out's first jump over it, which every row of
three or more stones makes, and with two stones the way out is that
gap. It was replaced by the last left off the way back (M14).

## Verification

Every arm prints the same output as `frog.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.8 to 2.2 s and the differential 1.2 s; under `karac __mir-llvm-asan` the arms take 0.5 to 0.8 s and the differential 0.8 s; and under `karac run` the differential takes 0.5 s.

## Benchmarks

The bench builds 20 rows of `10^5` stones once from its own generator,
gaps from 1 to `10^4`; then makes 55 passes. Each moves one stone of
every row to a place between its neighbours chosen by the checksum so
far, asks, and puts it back, folding the answer plus the pass into the
checksum. The bench uses the ★ arm in all five languages, the same one
pass over each row. Every implementation prints `55 passes over 20 rows
of 10^5: checksum 711984492`.

BENCHTAB
