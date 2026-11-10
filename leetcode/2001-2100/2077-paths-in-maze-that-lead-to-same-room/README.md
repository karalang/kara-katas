# 2077. Paths in Maze That Lead to Same Room

A maze consists of `n` rooms numbered from `1` to `n`, and some rooms
are connected by corridors. You are given a 2D integer array `corridors`
where `corridors[i] = [room1_i, room2_i]` indicates that there is a
corridor connecting `room1_i` and `room2_i`, allowing a person in the
maze to go from `room1_i` to `room2_i` and vice versa.

The designer of the maze wants to know how confusing the maze is. The
confusion score of the maze is the number of different cycles of length
3. For example, `1 → 2 → 3 → 1` is a cycle of length 3, but `1 → 2 → 3
→ 4` and `1 → 2 → 3 → 2 → 1` are not.

Two cycles are considered to be different if one or more of the rooms
visited in the first cycle is not in the second cycle.

Return the confusion score of the maze.

```
n = 5, corridors = [[1,2],[5,2],[4,1],[2,4],[3,1],[3,4]]  ->  2
n = 4, corridors = [[1,2],[3,4]]                          ->  0
```

**Constraints:** `2 <= n <= 1000`; `1 <= corridors.length <= 5 · 10^4`;
`corridors[i].length == 2`; `1 <= room1_i, room2_i <= n`; `room1_i !=
room2_i`; there are no duplicate corridors.

A cycle of length 3 is a triangle of rooms, each pair joined, and two
are the same when they visit the same three rooms, so the score is the
number of triangles. Turning every corridor to lead from its lower room
to its higher meets each triangle `a < b < c` once, at its corridor `a -
b`, as a room `c` above `b` that both reach: a corridor's triangles are
the rooms the two ends' upward sets share. The approaches differ in how
they hold those sets and count what they share.

## Approaches

| file | mechanism |
|---|---|
| `maze.kara` ★ | each room's rooms above it a `Set`, and every corridor's triangles the `len()` of its two rooms' sets' `intersection`. O(E · d), d the most corridors at a room |
| `maze_matrix.kara` | an adjacency matrix of `bool`s, and for every corridor each room above its higher end looked up in both rows. O(E · n) |
| `maze_bits.kara` | each room's rooms above it as bits in a row of `u64` words, and a corridor's triangles its rows `&`ed word by word and `count_ones()`ed. O(E · n / 64) |
| `maze_merge.kara` | each room's rooms above it in a sorted `Vec`, and a corridor's two lists walked at once with two cursors over `Slice`s |
| `maze_pairs.kara` | the corridors as a `Set` of `(low, high)` tuples, and for each room every pair of its rooms above it looked up. O(Σ d²) |
| `maze_solution.kara` | LeetCode's Rust template (`use std::collections::HashSet`, `vec![HashSet::new(); n + 1]` of both ends' neighbours, `for c in &corridors`, every corridor's `intersection(&..).count()` summed and divided by 3), carried by `karac fix` in four rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and five
more, each maze and its score; then the sum and a checksum of the scores
of 300 random mazes of 2 to 60 rooms and up to 200 corridors, each to a
room up to 3, 10 or 60 on; then the score of the largest maze the
generator draws, 1000 rooms and 37944 corridors. `maze.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every three rooms `a < b < c` looked at, and counted when all
three of their corridors are in the list. It checks 300 random mazes of
2 to 12 rooms and up to 40 corridors; then 20 with every corridor, and
20 with none or one. All 340 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the score is the statement read literally |
| P2 | the corridors listed backwards, each written the other way round, give the same score |
| P3 | the rooms numbered backwards give the same score |
| P4 | a new corridor raises the score by the rooms both its ends reach |
| P5 | two copies of the maze side by side score twice as much |
| P6 | each arm agrees with at least three of the other five |

The differential prints `340 mazes: checksum 669331150, 12240 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal scores was checked against a Python reading of the same
mazes. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-five edits to the differential, five to eight to each of its
arms, each run under `karac __mir-llvm-run` and `karac __mir-run`.
Seventeen are kept, three to each Kāra arm and two to the Rust-template
arm. Each kept one is killed, fails the same way under both backends and
not by a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the corridors kept as written, not turned up | P1 171, P4 54, P6 171 |
| M2 | ★: the first room skipped | P1 205, P3 120, P4 142, P5 205, P6 205 |
| M3 | ★: the higher room's set counted whole | P1 171, P4 151, P6 171 |
| M4 | matrix: one way of each corridor marked | P1 224, P2 191, P3 184, P4 137, P6 224 |
| M5 | matrix: the last room never the third | P1 207, P3 120, P4 59, P5 207, P6 207 |
| M6 | matrix: the corridor taken as written | P1 203, P2 219, P3 219, P4 120, P6 203 |
| M7 | bits: the corridors written high room first not counted | P1 208, P2 216, P3 192, P4 128, P6 208 |
| M8 | bits: the higher room's row shifted down a room | P1 147, P3 144, P4 128, P6 147 |
| M9 | bits: one triangle a corridor at most | P1 156, P3 88, P4 99, P6 156 |
| M10 | merge: the lists sorted backwards | P1 130, P3 121, P4 113, P6 130 |
| M11 | merge: the wrong cursor moved past a smaller room | P1 241, P4 142, P6 241 |
| M12 | merge: the walk stopping before the first list's last room | P1 238, P3 115, P4 78, P6 238 |
| M13 | pairs: a pair looked up as it comes | P1 189, P2 214, P3 157, P4 117, P6 189 |
| M14 | pairs: a room's first room above left out | P1 233, P2 113, P3 107, P4 88, P6 233 |
| M15 | pairs: each room paired with the next alone | P1 183, P3 114, P4 116, P6 183 |
| M16 | solution: one end's neighbours counted | P1 271, P2 150, P4 146, P5 67, P6 271 |
| M17 | solution: the adapter's score one more | P1 340, P5 340, P6 340 |

P1 and P6 kill all seventeen, P4 sixteen, P3 twelve, P2 six and P5
four. P4 sees almost every edit, since a new corridor's triangles are
the rooms its two ends share, which every edit to how the sets are kept
or met miscounts. P3, which numbers the rooms backwards, turns every
corridor round and puts the rooms above a room below it: it sees an
edit that leans on the order of the rooms, a room skipped (M2, M5), a
list's end missed (M12, M14, M15), sorted the wrong way (M10) or shifted
(M8). P2, which writes each corridor the other way round, sees an arm
that reads a corridor as written (M4, M6, M7, M13). P5 sees what does not
double with the maze: the first or last room missed (M2, M5), a constant
added (M17).

Of the thirty-five, eighteen were not kept, and none survives. Seven
fail as a kept one. Five score every maze 0 or a whole multiple of its
score, which P5, being linear, cannot tell from the right one, and fail
as M11: the ★ arm's corridor led both ways, the matrix arm's every room
looked at, the merge arm's shared room counted twice, the pairs arm's
every pair taken both ways and its corridors stored high room first.
The bits arm's corridor's rooms as written fails as M1, and the merge
arm's higher room's list taken twice as M3. Five fail alike and none is
kept, an edit that counts something other than the shared rooms (P1
324, P3 169, P4 229): the ★ arm's union and its lower room's set met
with itself, the bits arm's either row, lower row twice and `^`. Five
are killed with checks of their own but were left out because their arm
keeps three or two: the matrix arm's room joined to either end (P1 193,
P3 169, P4 191), the pairs arm's pairs with no corridor (P1 254, P3 169,
P4 170), and the Rust arm's score divided by two (P1 191, P4 115, P5
120), each corridor recorded at one end (P1 220, P4 134, P5 88) and the
adapter's first corridor dropped (P1 205, P2 96, P4 39, P5 205). One
crashes and is not kept: the bits arm's words one short, `(n + 1) / 64`,
a row of no words indexed past its end.

## Verification

Every arm prints the same output as `maze.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them.

Under `karac __mir-run` the arms take 1.1 s to 4.1 s, the matrix and
merge arms the slowest, and the differential 2.3 s (timed while other
work shared the machine).

The ★ arm met one compiler gap. It counted a corridor's triangles as
Rust does, `up[a].intersection(up[b]).count()`. Rust's set operations
give an iterator; Kāra's give a set, which has no `count`, and the
checker said only "no method 'count' on type 'Set'". It now says why and
offers `len()`, which `karac fix` wrote. Fixed in kara 78ecc3f4ab, test
`tests/kata_2077_set_count.rs`. The Rust arm's `count()` took the same
edit.

The bits arm was written with `count_ones() as i64`; `count_ones()` is
already an `i64`, and `karac fix` dropped the cast.

The Rust arm was written as LeetCode's Rust template. `karac fix` carries
it in four rounds of 9, 1, 2 and 5 edits: Rust's spellings (`Vec<..>` to
brackets, the `use` deleted, `&corridors` to `ref corridors`, the `&` of
`&adj[b]` dropped, `::` to `.`, `struct Solution;` to `struct Solution
{}`); then `HashSet` to `Set`; then `vec![..; n + 1]` to `Vec.filled`
and `count()` to `len()`; then `as usize` to `as i64`, as an index is.
The fixed arm reads as the template does.

## Benchmarks

The bench scores 30 mazes of 1000 rooms and about 38000 corridors each,
every corridor to a room up to 60 on, with the ★ arm in all five
languages. Kāra builds each intersection as a `Set` and Python as a
`set`; Rust counts `intersection(..)` as an iterator, Go loops over a
`map` and probes the other, and C does the same over open-addressing
tables. Every implementation prints `30 mazes: sum 13422709, checksum
798806721`.

BENCHTAB
