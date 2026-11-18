# 2271. Maximum White Tiles Covered by a Carpet

You are given a 2D integer array `tiles` where `tiles[i] = [li, ri]`
represents that every tile `j` in the range `li <= j <= ri` is colored
white.

You are also given an integer `carpetLen`, the length of a single
carpet that can be placed **anywhere**.

Return *the **maximum** number of white tiles that can be covered by
the carpet*.

```
tiles = [[1,5],[10,11],[12,18],[20,25],[30,32]], carpetLen = 10  ->  9
tiles = [[10,11],[1,1]], carpetLen = 2                           ->  2
```

**Constraints:** `1 <= tiles.length <= 5 * 10^4`; `tiles[i].length ==
2`; `1 <= li <= ri <= 10^9`; `1 <= carpetLen <= 10^9`; the `tiles` are
**non-overlapping**.

A carpet that starts on a black tile can slide right to the next white
one without losing any, so some best carpet starts where a tile
starts. With the tiles sorted, a second index runs ahead over the
tiles each carpet covers whole, and only the next tile is cut. O(m log
m) for the sort.

## Approaches

| file | mechanism |
|---|---|
| `carpet.kara` ★ | a sorted clone, a carpet from each tile's start, a second index over the tiles covered whole with their sum kept as it moves, and the part of the next tile |
| `carpet_binary.kara` | prefix sums of the sorted tiles and a hand-written binary search for the first tile starting past the carpet, less the overhang of the one before |
| `carpet_ends.kara` | the mirror: a carpet ending at each tile's end, an index over the first tile it touches moving forward, that tile cut where the carpet starts |
| `carpet_struct.kara` | `struct Reach` of the sorted tiles, the first tile not covered whole and the sum before it; `lay` and `lift` (`mut ref self`) move it per tile |
| `carpet_iter.kara` | in chains: the prefix sums by `scan` into `extend`, each tile's carpet ended by `partition_point`, and `map` then `max` |
| `carpet_solution.kara` | LeetCode's Rust template: `Vec<Vec<i32>>` and `i32` in, `i32` out; `mut tiles` sorted by `sort_unstable`, an early `return` once the second index reaches the end; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and five
more (one tile longer than the carpet, 7; one shorter, 2; three tiles
touching, 5; a carpet of 1, 1; a carpet across a wide gap, 5), each
with its count; then 2000 random sets of 1 to 12 shuffled tiles,
lengths to 1, 5 or 20 and gaps to 0, 3 or 30, under carpets of 1 to
60, with a checksum; then the constraints' largest, 5 * 10^4 tiles,
lengths and gaps to 10^4, under carpets of 10^3 (1000), 10^6 (585213)
and 10^9 (234788536). `carpet.py` mirrors the ★ arm and its output is
byte-identical.

Each Kāra arm takes the tiles borrowed, as a parameter does by default,
and sorts a `clone()`.

`karac fix` carries the template in one round, reporting 21 edits:
`mut tiles: Vec<Vec<i32>>` to `tiles: own Vec[Vec[i32]]` with `let mut
tiles = tiles;` as the body's first line, `sort_unstable` to `sort`,
`let mut ans: i32 = 0` and `let mut cover: i32 = 0`, which the `i32`
returns name, `&&` to `and`, `struct Solution;` to `struct Solution
{}`, and in the adapter `&Vec<Vec<i64>>` to a bare `Vec[Vec[i64]]`,
`Vec<Vec<i32>>` to `Vec[Vec[i32]]`, `|&x|` to `|x|`, `Solution::` to
`Solution.` and the `as i64` dropped.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the carpet laid at every start from where it first touches a
tile to the last tile's end, each tile's overlap with it summed, the
most kept. No sort, and no start taken to be a tile's. It checks 300
random sets of 1 to 8 shuffled tiles, lengths to 1, 4 or 10 and gaps to
0, 2 or 10, under carpets of 1 to 30; then 30 of tiles touching end to
end; then 30 under a carpet longer than them all. All 360 are drawn
before any arm answers.

| | property |
|---|---|
| P1 | the count is the literal reading's |
| P2 | the tiles mirrored, each `[l, r]` made `[1000 - r, 1000 - l]`: the same count |
| P3 | the tiles moved 10^6 along: the same count |
| P4 | at most the carpet's length and the white tiles there are, and at least the longest tile's length or the carpet's, whichever is less |
| P5 | the carpet one longer: the same count or one more |
| P6 | each arm agrees with at least three of the other five |

P2 turns every carpet that starts at a tile's start into one that ends
at a tile's end, so the ★ arm and the ends arm check each other through
it. P4's lower bound is a carpet laid at the longest tile's start.

The differential prints `360 cases: checksum 14836622, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that keeps
the white cells in a `set` and intersects it with every carpet's range.
On a failure it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the last carpet kept | P1 281, P2 157, P4 118, P6 281 |
| M5 | ★: the carpet one longer | P1 100, P4 75, P6 100 |
| M6 | ★: never sorted | P1 129, P2 133, P4 90, P5 10, P6 129 |
| M7 | binary: every tile one short | P1 360, P4 223, P6 360 |
| M8 | binary: the last tile never found | P1 177, P2 77, P6 177 |
| M10 | binary: the overhang kept | P1 98, P2 56, P4 80, P5 17, P6 98 |
| M13 | ends: the first tile cut one less | P1 88, P2 4, P4 69, P5 3, P6 88 |
| M14 | ends: the first tile never cut | P1 95, P2 56, P4 77, P5 17, P6 95 |
| M16 | ends: never sorted | P1 140, P2 129, P4 103, P5 6, P6 140 |
| M17 | struct: the reach left behind | P1 32, P2 28, P4 32, P5 16, P6 32 |
| M19 | struct: the part one short | P1 46, P4 19, P5 27, P6 46 |
| M21 | struct: never lifted | P1 143, P2 24, P4 106, P5 16, P6 143 |
| M22 | iter: the sums never accumulated | P1 279, P2 155, P4 128, P5 12, P6 279 |
| M24 | iter: the overhang taken when it is not one | P1 278, P4 239, P6 278 |
| M26 | iter: the least kept | P1 291, P2 151, P4 133, P6 291 |
| M27 | solution: the early answer the last cover | P1 92, P2 102, P4 35, P5 21, P6 92 |
| M31 | solution: never sorted | P1 126, P2 132, P4 87, P5 9, P6 126 |

P1 and P6 kill all seventeen, P4 sixteen, P2 thirteen, P5 eleven, and
P3 none. P4 is nearly as strong as P1: almost every edit either counts
more than the carpet or the white tiles allow, or less than a carpet at
the longest tile's start would. P2 catches the edits that break the
symmetry between a carpet's two ends. P5 catches a count that jumps by
more than one as the carpet grows, as an overhang kept or a cut lost
does. Moving every tile along changes nothing for any edit here: none
reads a tile's position except against another's.

Of the thirty-one, fourteen were not kept, and none crashes or differs
between the backends. Five fail as a kept one does: the ★ arm's part of
the next tile left out and its part one short, and the template's part
left out (M2, M3, M28), as the struct arm's part one short (M19); the ★
arm's whole never shrinking (M4) as the struct arm's never lifted
(M21); and the ends arm's carpet one longer (M12) as the ★ arm's (M5).
Nine fail in ways of their own and are left out because their arms keep
enough: the binary arm's tile starting at the end left out and its
first tile left out (M9, M11), the ends arm's every tile one short
(M15), the struct arm's tile lifted twice over (M20), the iter arm's
sums from 1 and every tile before counted (M23, M25), the template's
tile taken off one short (M29), and the struct arm's and the template's
carpet one shorter (M18, M30), alike.

Five edits of the first draft were replaced. Three were equivalent: the
★ and struct arms' tile ending at the carpet's end not counted whole,
which the next tile's part then counts in full; and the struct arm's
tile lifted when the reach had not passed it, which happens only for a
carpet shorter than that tile, when the best is already the carpet's
whole length. Two stopped with an index out of bounds under both
backends: the ends arm's tile ending at the start dropped, which runs
the index past the last tile, and the iter arm's `partition_point`
with `<`, which finds no tile before the first. They are now M1, M13,
M18, M20 and M23.

## Verification

Every arm prints the same output as `carpet.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the differential takes 0.5 s, the ends arm 0.9
s, the ★ arm 1.0 s, the struct arm 1.2 s, the binary arm 1.8 s, the
template 2.4 s, and the iter arm 3.3 s.

## Benchmarks

The bench answers 30 sets of the constraints' largest, 5 * 10^4
tiles, lengths and gaps to 10^4, shuffled, under carpets of 10^3, 10^6
and 10^9 in turn, with the ★ arm in all five languages. Every
implementation prints `30 sets of 5 * 10^4: checksum 321164656`. Each
builds its tiles from the same generator and sorts a copy per call:
Rust's and Python's lists of pairs, Go's `[][]int64` by `sort.Slice`,
and C's array of two-field structs by `qsort`.

BENCHTAB
