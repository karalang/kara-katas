# 2274. Maximum Consecutive Floors Without Special Floors

Alice manages a company and has rented some floors of a building as
office space. Alice has decided some of these floors should be
**special floors**, used for relaxation only.

You are given two integers `bottom` and `top`, which denote that Alice
has rented all the floors from `bottom` to `top` (**inclusive**). You
are also given the integer array `special`, where `special[i]` denotes
a special floor that Alice has designated for relaxation.

Return *the **maximum** number of consecutive floors without a special
floor*.

```
bottom = 2, top = 9, special = [4,6]     ->  3
bottom = 6, top = 8, special = [7,6,8]   ->  0
```

**Constraints:** `1 <= special.length <= 10^5`; `1 <= bottom <=
special[i] <= top <= 10^9`; all the values of `special` are
**unique**.

The special floors cut the building into runs: the floors below the
lowest, the floors above the highest, and the floors strictly between
each two neighbours. With the special floors sorted, each run is a
difference. O(n log n) for the sort; the floors themselves, up to
10^9, are never visited.

## Approaches

| file | mechanism |
|---|---|
| `floors.kara` ★ | a sorted clone; the runs at the two ends, then `floors[i] - floors[i - 1] - 1` for each neighbour |
| `floors_sentinel.kara` | the floor below the bottom and the floor above the top pushed in beside the special ones, so after the sort every run lies between two neighbours, read by `windows(2)` |
| `floors_set.kara` | the special floors into a `SortedSet`, and a walk up it from the floor below the bottom, the last run ending at the top |
| `floors_struct.kara` | `struct Climb` of the last special floor passed and the longest run; `pass` (`mut ref self`) takes the next floor up and `reach` closes the run to the top |
| `floors_iter.kara` | in chains: the sorted floors `zip`ped with themselves one along, each pair's run by `map`, and a `fold` from the longer of the two end runs |
| `floors_solution.kara` | LeetCode's Rust template: `i32` floors and `mut special: Vec<i32>` in, `i32` out; `sort_unstable`, the two ends, then `windows(2)`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and five
more (one floor, 0; one special in the middle, 5; specials at both
ends, 8; one at the top, 9; the widest run between two specials, 9),
each with its run; then 2000 random buildings of up to 10, 100, 10^4 or
10^9 floors with up to 20 special floors 1 to 3, 50 or 10^6 apart, with
a checksum; then three of the constraints' largest, 10^5 special
floors: random, up to 2 * 10^4 apart under 10^9 floors (143512579);
every floor from 1 to 10^5 (0); and every third floor up to 3 * 10^5
(2). `floors.py` mirrors the ★ arm and its output is byte-identical.

`karac fix` carries the template in one round, reporting 13 edits: `mut
special: Vec<i32>` to `special: own Vec[i32]` with `let mut special =
special;` as the body's first line, `sort_unstable` to `sort`, `struct
Solution;` to `struct Solution {}`, and in the adapter `&Vec<i64>` to a
bare `Vec[i64]`, `|&x|` to `|x|`, `Solution::` to `Solution.` and the
`as i64` dropped.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every floor from the bottom to the top visited in turn, each
looked for among the special floors, and the longest run of floors not
found. No sort and no differences. It checks 300 random buildings of 1
to 40 floors starting at one of the first 20, with up to 8 special
floors 1 to 1, 3 or 10 apart; then 30 with every floor special; then 30
with one. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the run is the literal reading's |
| P2 | the building turned upside down, each special floor `f` made `bottom + top - f`: the same run |
| P3 | every floor moved 10^8 up: the same run |
| P4 | at least 0, at most the floors that are not special, and at least those floors shared out over the runs, one more than the special floors |
| P5 | one floor more at the top: the run, or the run above the highest special floor grown by one when that is longer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 275396108, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that keeps
the free floors in a `set` and tries every range of them. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M3 | ★: the run above the last one short | P1 152, P2 219, P4 27, P5 263, P6 152 |
| M4 | ★: a gap counting a special floor | P1 86, P4 52, P6 86 |
| M5 | ★: the first gap missed | P1 9, P2 9, P4 6, P6 9 |
| M7 | sentinel: no floor below | P1 67, P2 219, P4 55, P6 67 |
| M9 | sentinel: never sorted | P1 360, P4 360, P5 360, P6 360 |
| M11 | sentinel: the best started at 1 | P1 87, P4 87, P6 87 |
| M13 | set: the walk from the bottom | P1 67, P2 219, P4 19, P6 67 |
| M16 | set: the walk down the set | P1 199, P4 166, P5 170, P6 199 |
| M17 | set: the run to the top one long | P1 263, P2 230, P4 177, P5 298, P6 263 |
| M18 | struct: never sorted | P1 162, P2 197, P4 119, P5 105, P6 162 |
| M21 | struct: the run to the top left out | P1 152, P2 219, P4 142, P5 263, P6 152 |
| M22 | struct: only the last run kept | P1 27, P2 128, P4 17, P6 27 |
| M24 | iter: each floor against the one two along | P1 84, P4 49, P6 84 |
| M25 | iter: the ends left out | P1 236, P4 220, P5 323, P6 236 |
| M27 | iter: the least kept | P1 147, P4 142, P5 180, P6 147 |
| M30 | solution: the run below the first one long | P1 179, P2 230, P4 121, P6 179 |
| M31 | solution: only the last gap kept | P1 128, P2 45, P4 120, P5 171, P6 128 |

P1, P4 and P6 kill all seventeen, P2 ten, P5 nine, and P3 none. P4 is
as strong as P1 here: every edit either counts a special floor, runs
past the building, or misses the longest run by enough that the free
floors shared out over the runs exceed it. P2 catches the edits that
treat the two ends unalike, which turning the building over swaps. P5
catches an edit whose run at the top does not grow by exactly one with
the building, or whose answer moves when only the top run changes.
Moving every floor up changes nothing for any edit here: none reads a
floor except against another floor or an end.

Of the thirty-one, fourteen were not kept, and none crashes or differs
between the backends. All fourteen fail as a kept one does: the ★,
iter and template arms' never sorted (M1, M23, M28) as the struct arm's
(M18); the ★ arm's run below left out and the sentinel arm's first gap
skipped (M2, M10) as the sentinel arm's no floor below (M7); the ★
arm's run below one short, the sentinel arm's floor below at the bottom
and the struct arm's climb from the bottom (M6, M12, M20) as the set
arm's walk from the bottom (M13); the sentinel arm's floor above at the
top (M8) as the ★ arm's run above one short (M3); the set arm's and the
template's run to the top left out (M14, M29) as the struct arm's
(M21); the set arm's floor below never moved and the struct arm's last
floor never moved (M15, M19) as the sentinel arm's never sorted (M9),
each wrong in all 360; and the iter arm's run counting a special floor
(M26) as the ★ arm's (M4).

One edit of the first draft was replaced because it failed as another
did: the template's gap counting a special floor, as the ★ arm's M4. It
is now M30.

## Verification

Every arm prints the same output as `floors.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the differential takes 0.5 s, the ★ arm 0.7 s,
the struct arm 0.8 s, the sentinel arm 0.9 s, the template 1.3 s, the
iter arm 1.5 s, and the set arm 7.7 s, the 3 * 10^5 inserts of the long
cases into the `SortedSet` taking most of it; compiled, the set arm
takes 0.3 s like the others.

## Benchmarks

The bench answers 50 buildings of the constraints' largest, 10^5
special floors 1 to 2 * 10^4 apart under 10^9 floors, shuffled, with
the ★ arm in all five languages. Every implementation prints `50
buildings of 10^5: checksum 725323008`. Each builds its floors from the
same generator and sorts a copy per call: C by `qsort`, Go by
`sort.Slice`.

BENCHTAB
