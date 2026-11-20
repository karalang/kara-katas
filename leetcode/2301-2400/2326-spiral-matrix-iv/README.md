# 2326. Spiral Matrix IV

You are given two integers `m` and `n`, which represent the dimensions
of a matrix.

You are also given the `head` of a linked list of integers.

Generate an `m x n` matrix that contains the integers in the linked
list presented in **spiral** order **(clockwise)**, starting from the
**top-left** of the matrix. If there are remaining empty spaces, fill
them with `-1`.

Return *the generated matrix*.

```
m = 3, n = 5, head = [3,0,2,6,8,1,7,9,4,2,5,5,0]  ->  [[3,0,2,6,8],[5,0,-1,-1,1],[5,2,4,9,7]]
m = 1, n = 4, head = [0,1,2]                      ->  [[0,1,2,-1]]
```

**Constraints:** `1 <= m, n <= 10^5`; `1 <= m * n <= 10^5`; the number
of nodes in the list is in the range `[1, m * n]`; `0 <= Node.val <=
1000`.

A walker that turns clockwise whenever the next cell is off the grid
or already written visits the cells in spiral order, and since no
value is `-1`, a cell still `-1` is one not yet written. O(m n).

## Approaches

| file | mechanism |
|---|---|
| `spiral.kara` ★ | a walker with a table of four moves writes each value and turns clockwise when the next cell is off the grid or not `-1` |
| `spiral_rings.kara` | four bounds close in as the top row, the right column, the bottom row and the left column are written in turn, each only while the list lasts and the bounds have not crossed |
| `spiral_order.kara` | the cells in spiral order listed first by peeling rings by index, with no list in sight, and the values then laid along that order |
| `spiral_rec.kara` | recursion on the list: `lay` writes one value and calls itself on the rest with the next cell and heading, the grid passed down by `mut ref`; a call frame per value |
| `spiral_iter.kara` | iterators: each ring's cells four ranges `chain`ed, `flat_map`ped over the rings, and `zip`ped with the list's values gathered into a `Vec` |
| `spiral_solution.kara` | LeetCode's Rust template: its `ListNode` of `i32` behind `Option<Box<ListNode>>`, an `i32` walker turning by a table of moves, and `usize` indices; carried by `karac fix` with two casts written by hand |
| `differential.kara` | the six arms against the statement read literally, six properties |

Shared `ListNode` is `shared struct ListNode { val: i64, mut next:
Option[ListNode] }`, LeetCode's list as Kāra writes one; the template
keeps its own.

Every arm prints the same 7 lines: LeetCode's two examples; one cell; a
column of five with three values; a full 4 by 4; 300 by 300 with 50000
values, folded to a checksum and the count of `-1`s; then 1000 random
grids of 1 to 8 by 1 to 8, each with 1 to `m n` values, with a checksum
and the `-1`s in all. `spiral.py` mirrors the ★ arm and its output is
byte-identical.

`karac fix` carries the template in 45 edits but for two casts. `check`
first reports eighteen errors, each with its edit: the brackets of the
five `Option<Box<ListNode>>` and three `Vec<..>`; `struct Solution;` to
`struct Solution {}`; the three `mut` in `let (mut r, mut c, mut d)`
moved before the pattern; the four `||` to `or`; and `Solution::` and
`Box::new` to `.`. The rest follow from those: `Box[ListNode]` to
`ListNode` and the `Box.new(..)` round the new node dropped, since a
struct's own type in a field is already a pointer; `vec![vec![-1; n as
usize]; m as usize]` to `Vec.filled`, its two `as i64` then dropped as
widening on their own; and `cur = node.next` to `cur = ref node.next`.

`fix` stops on the walker's `r += dirs[d].0;` and `c += dirs[d].1;`:
the table's literals kept the default `i64`, and `r` and `c` are
`i32`. `check` says to write `as i32`, which is how the template stands,
with no edit to make it. The same with a plain local, `let k = 1; r +=
k;`, gets a message naming `k`'s literal and an edit to declare it
`k: i32`; through a tuple field of an indexed element it gets neither,
which ledger row B-2026-11-18-92 records. Before the compound assignment,
`let (nr, nc) = (r + dirs[d].0, c + dirs[d].1);` passes, the literal
taking `i32` from the first use it meets.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each cell's place in the clockwise order written as a key,
its ring, the least of its distances to the four edges, then its side
in the order top, right, bottom, left, then how far along that side;
the cells sorted by key, and the list's values laid along them, `-1`
where the list runs out. No walker and no bounds. It checks 300 random
grids of 1 to 8 by 1 to 8 with 1 to `m n` values from 0 to 1000; then
30 of 1 to 12 by 1 to 12 with a value for every cell, from 0 to 3; then
30 of up to 30 by 30. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the grid is the literal reading's |
| P2 | the grid is `m` by `n`, and its cells other than `-1` hold exactly the list's first values, as many as fit |
| P3 | a grid one larger on every side, with `2 (m + n) + 4` values of 1000 in front of the list: a ring of 1000 round the same grid |
| P4 | values of 1000 after the list until there are `m n`: the same grid with 1000 for every `-1` |
| P5 | every value plus 1: the same grid with every cell other than `-1` one more |
| P6 | each arm agrees with at least three of the other five |

P3's ring is exactly the outer ring of the larger grid, so the list
after it starts at the top left of the inside heading right, as on the
grid alone.

The differential prints `360 cases: checksum 839143370, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal grids was checked against a Python reading that builds
the same cases and lists the spiral by four closing bounds. On a
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
| M3 | ★: a 0 written as `-1` | P1 33, P2 33, P4 33, P5 33, P6 33 |
| M5 | ★: the values from the second | P1 360, P2 360, P3 358, P4 360, P6 360 |
| M6 | ★: a cell holding 1000 taken as free | P3 360, P4 108 |
| M7 | rings: the bottom row written left to right | P1 158, P6 158 |
| M10 | rings: a column passed over on the right | P1 168, P2 76, P3 360, P4 278, P6 168 |
| M11 | rings: no ring of one row | P1 55, P2 55, P4 102, P6 55 |
| M13 | order: the left column listed from the top | P1 109, P6 109 |
| M15 | order: the bottom row listed from the last column | P1 168, P2 168, P3 360, P4 278, P6 168 |
| M16 | order: the top row listed right to left | P1 309, P6 309 |
| M17 | rec: every other value skipped | P1 314, P2 314, P3 360, P4 353, P6 314 |
| M18 | rec: a written 0 taken as free | P1 13, P2 13, P4 13, P5 13, P6 13 |
| M21 | rec: each value written plus its column | P1 281, P2 281, P3 360, P4 247, P6 281 |
| M24 | iter: the middle ring of an odd side left out | P1 114, P2 114, P4 200, P6 114 |
| M25 | iter: the values laid from the end | P1 313, P3 359, P4 289, P6 313 |
| M26 | iter: the top row one short | P1 288, P2 81, P3 360, P4 360, P6 288 |
| M27 | solution: each value raised by its heading | P1 246, P2 246, P3 360, P4 260, P6 246 |
| M29 | solution: a written 0 the only reason to turn | P1 102, P2 102, P3 360, P4 214, P5 19, P6 102 |

P1 and P6 kill sixteen, P4 fourteen, P2 twelve, P3 ten and P5 three.
M6 is the one P1 misses: a value of 1000 is one draw in 1001, and only
P3's ring and P4's filling, both of 1000s, put one where the walker
meets it. P2, the values the list's first ones, misses the edits that
lay the right values in the wrong cells: a row or column the wrong way
round, the values from the end. P3, the grid inside a ring, compares an
arm with itself, so it misses the edits that treat every ring alike, a
row or column the wrong way round, a ring of one row or the middle one
left out, and catches the ones whose error moves with the grid: the
outer ring written wrong, a value tied to its column or heading, the
list cut or skipped. P4, the list run on to fill the grid, fails
wherever the cells the list does not reach are wrong too, which is
nearly every edit. P5, every value plus 1, fails only where a 0 is
treated apart.

Of the thirty-one, fourteen were not kept. Four are equivalent and
killed by nothing: the rings arm's left column written with no column
left (M8), the order arm's bottom row of a one-row ring listed again
(M12), and the iter arm's bottom row of a one-row ring and left column
of a one-column ring kept (M22, M23). Each writes or lists cells again
only after every cell of the grid has its turn, and a list of at most
`m n` values has run out by then. Five pairs fail alike, and none of
them is kept: a written cell no reason to turn in the ★ arm (M1) and
the value written after the rest in the rec arm (M19); the last value
never written in the ★ (M2) and template (M28) arms; each value
written plus its row in the ★ (M4) and template (M31) arms; and the
right column begun one row up in the rings (M9) and order (M14) arms.
The rec arm's (M20) and the template's (M30) cell holding 1000 taken
as free fail as the ★ arm's (M6).

M2, M4, M5, M6, M16, M17, M20, M21, M28, M30 and M31 replace edits that
crashed. A walker moves on after a turn without looking again, so an
edit that starts it heading down, or takes the first or last column or
the last row as off the grid, or writes into the mirrored row, sends it
off the grid on some case, and the order arm's left column one short
leaves its order shorter than a full list; each stops on an index out
of bounds. M30 replaces a second edit too, the template's values from
the second written `match head { Some(h) => h.next, None => None }`,
which `karac check` refuses: `head`, a bare parameter, is borrowed, so
the first arm is a `ref Option[ListNode]` and the second an
`Option[ListNode]`.

The second group of cases was first 30 grids of one or two rows or
columns, and the rec arm's written 0 taken as free (M18) survived it:
a written cell blocks the walker only at the end of a ring, which such
a grid hardly reaches. Full grids of 1 to 12 by 1 to 12 with values
from 0 to 3 kill it.

## Verification

Every arm prints the same output as `spiral.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★, rings, order and template arms take 0.7
s, the iter arm 1.3 s and the recursive arm, a call for each of the
50000 values of the 300 by 300 grid, 1.4 s. The differential takes 3.3
s there and 0.9 s under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 10 lists of 90000 to 99990 values once, then makes 30
passes, laying list `k` in pass `p` into a grid of `10^5` cells whose
shape, from 50 by 2000 to 1000 by 100, changes with `p + k`, with the ★
arm in all five languages. Every implementation prints `30 passes over
10 lists in grids of 10^5 cells: checksum 219333753`. Each walks a
linked list of 64-bit values, Kāra's `shared struct`, Rust's
`Option<Box<..>>`, C's and Go's pointers and Python's objects, and
builds a fresh grid as a list of rows for every call. Kāra hands each
call the head by `clone`, which for a `shared struct` counts one more
reference; the others pass a reference or a pointer.

BENCHTAB
