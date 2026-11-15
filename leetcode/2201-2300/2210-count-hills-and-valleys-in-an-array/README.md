# 2210. Count Hills and Valleys in an Array

You are given a **0-indexed** integer array `nums`. An index `i` is part
of a **hill** in `nums` if the closest non-equal neighbors of `i` are
smaller than `nums[i]`. Similarly, an index `i` is part of a **valley**
in `nums` if the closest non-equal neighbors of `i` are larger than
`nums[i]`. Adjacent indices `i` and `j` are part of the **same** hill or
valley if `nums[i] == nums[j]`.

Note that for an index to be part of a hill or valley, it must have a
non-equal neighbor on **both** the left and right of the index.

Return *the number of hills and valleys in* `nums`.

```
nums = [2, 4, 1, 1, 6, 5]  ->  3
nums = [6, 6, 5, 5, 4, 1]  ->  0
```

**Constraints:** `3 <= nums.length <= 100`; `1 <= nums[i] <= 100`.

A run of equal numbers is one hill or valley or none, so a pass counts
each run once, at its end, against the last different number before it
and the next one after. O(n).

## Approaches

| file | mechanism |
|---|---|
| `hills.kara` ★ | one pass keeping `left`, the last number different from the current one; a number equal to the next is skipped, so a run is judged at its end |
| `hills_dedup.kara` | a copy squeezed by `Vec.dedup`, after which every hill or valley is a single number strictly above or below both neighbours |
| `hills_trend.kara` | an `enum Trend` of the way the numbers last moved, `Unknown` until the first change, every step against the last trend a turn |
| `hills_struct.kara` | a `struct Landscape` whose `neighbours` (`ref self`) walks out to the closest different number on each side, `None` when a side has none; each run asked at its first index |
| `hills_iter.kara` | the sign of each step by `windows(2)` and `signum`, the flat ones `filter`ed out, and the turns counted as neighbouring signs that differ |
| `hills_solution.kara` | LeetCode's Rust template: `Vec<i32>` in, `i32` out, `dedup` on a mutable copy and `windows(3)` over it with `&&` and `||`; carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples and four more
(three numbers alike, a plateau as a hill, a plateau valley at an end
that does not count, and a zigzag), each with its answer; then the most
and a checksum for 3000 random arrays of 3 to 30 numbers up to 3, 10 and
100 in turn; then the constraints' longest, 100 numbers as a zigzag, in
pairs, and all alike. `hills.py` mirrors the ★ arm and its output is
byte-identical.

`karac fix` carries the template in two rounds of 12 and 2 edits: first
`Vec<i32>` to `Vec[i32]` three times, the three `&&` and `||` to `and`
and `or`, `|&x|` to `|x|`, `struct Solution;` to `struct Solution {}`
and `Solution::` to `Solution.`; then `.into_iter()` after `windows(3)`,
since Kāra's `windows` returns a `Vec` of slices, and the adapter's
`as i64` on an `i32` result dropped.

The trend arm went through the fix loop as first written: it matched on
`(trend, step)` and then assigned `trend = step`, and a fieldless enum is
`Copy` only when it derives it. The check names the derive as the help,
and `karac fix` adds `#[derive(Copy, Clone)]`. Until kara
`B-2026-11-15-81` the fix wrote `#[derive(Copy)]` alone, which the check then
flagged at once as deprecated, since `Copy` needs `Clone` and a derive
never adds another, so a second round added `Clone`; the fix now writes
both in one round.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every index's closest different neighbour found on each side,
the index marked a hill or a valley by them, and each block of equal
marked neighbours counted once; no running state. It checks 300 random
arrays of 3 to 12 numbers up to 3, 10 and 100 in turn; then 30 made of
runs of 1 to 4 equal numbers; then 30 zigzags. All 360 are drawn before
any arm answers.

| | property |
|---|---|
| P1 | the count is the statement read literally |
| P2 | it is at most the runs of equal numbers less two |
| P3 | the array reversed: the same count |
| P4 | every number x made 101 - x, hills to valleys: the same count |
| P5 | every number written twice: the same count |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 579883197, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that marks
each index by its closest different neighbours and counts the marked
blocks. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-one edits to the differential, five to each Kāra arm and six to
the template arm, each run under `karac __mir-llvm-run` and `karac
__mir-run`. Seventeen are kept, three to each Kāra arm and two to the
Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: valleys not counted | P1 285, P4 170, P6 285 |
| M4 | ★: a hill taken as at least its left | P1 38, P2 25, P3 53, P4 69, P5 140, P6 38 |
| M5 | ★: the left starting at the second number | P1 206, P3 129, P5 206, P6 206 |
| M7 | dedup: the squeezed last number skipped | P1 256, P3 107, P6 256 |
| M8 | dedup: a hill against its left only | P1 127, P3 172, P4 172, P6 127 |
| M10 | dedup: the squeeze dropping each number after a 3 | P1 86, P3 70, P4 87, P5 86, P6 86 |
| M11 | trend: a first fall counted as a turn | P1 178, P2 61, P3 185, P4 355, P6 178 |
| M12 | trend: a flat step taken as falling | P1 60, P2 38, P3 102, P4 102, P5 252, P6 60 |
| M13 | trend: the trend never kept | P1 319, P6 319 |
| M17 | struct: no right walk | P1 93, P5 295, P6 93 |
| M18 | struct: a run asked at every index | P1 93, P2 55, P5 319, P6 93 |
| M19 | struct: a hill only above its right | P1 125, P3 172, P4 172, P6 125 |
| M21 | iter: flat steps kept | P1 165, P2 110, P5 333, P6 165 |
| M23 | iter: a step's size kept instead of its sign | P1 148, P6 148 |
| M24 | iter: turns counted as equal signs | P1 295, P6 295 |
| M28 | solution: the adapter's numbers capped at 50 | P1 40, P4 259, P6 40 |
| M29 | solution: a window's ends compared with each other | P1 198, P3 206, P4 210, P6 198 |

P1 and P6 kill all seventeen, P3 and P4 nine each, P5 seven and P2
five. P2 bounds the count by the runs, so it kills only the five edits
that count too many (M4, M11, M12, M18, M21). P4 turns hills into
valleys, so it kills the edits that treat the two apart or read a
number's size (M1, M8, M19, M28 among them). P3 kills the edits that
treat the two ends apart, and P5, writing every number twice, the ones
that count runs or flat steps wrongly.

Of the thirty-one, fourteen were not kept. Eleven are killed and fail as
a kept one does or their own way: only one kind of turn counted in the
trend, iter and template arms (M14, M25, M27) as M1; no squeeze in the
dedup and template arms and the ★ arm's run counted at each of its
numbers (M6, M26, M3) as M17; the trend arm's steps from the second pair
and the struct arm's first index never asked (M15, M20) as M5; the
template's windows four wide (M30) as M7; the dedup arm's valley weighed
against its left twice (M9) as M19; and the template's adapter dropping
the last number (M31) fails its own way and is left out for the count of
two. Three survive, and each is equivalent: the ★ arm's left number
always updated (M2) assigns the value it already holds when the two are
equal; the struct arm's left walk stopping at index 0 (M16) then reads
a neighbour equal to the number, which is neither above nor below it,
just as no neighbour is; and the iter arm's steps taken backwards (M22)
negates every sign, which leaves the pairs that differ unchanged.

## Verification

Every arm prints the same output as `hills.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.2 s to 0.5 s, and the
differential 0.5 s.

## Benchmarks

The bench builds 2000 arrays of 100 numbers once, up to 3, 10 and 100 in
turn, then counts every array 100 times over with the ★ arm in all five
languages. Every implementation prints `100 passes over 2000 arrays:
checksum 930333092`.

BENCHTAB
