# 2201. Count Artifacts That Can Be Extracted

There is an `n x n` **0-indexed** grid with some artifacts buried in
it. You are given the integer `n` and a **0-indexed** 2D integer array
`artifacts` describing the positions of the rectangular artifacts,
where `artifacts[i] = [r1i, c1i, r2i, c2i]` denotes that the `i`th
artifact is buried in the subgrid where `(r1i, c1i)` is the coordinate
of the **top-left** cell and `(r2i, c2i)` is the coordinate of the
**bottom-right** cell.

You will excavate some cells of the grid and remove all the mud from
them. If the cell has a part of an artifact buried underneath, it will
be uncovered. If all the parts of an artifact are uncovered, you can
extract it.

Given a **0-indexed** 2D integer array `dig` where `dig[i] = [ri, ci]`
indicates that you will excavate the cell `(ri, ci)`, return *the
number of artifacts that you can extract*.

The test cases are generated such that no two artifacts overlap, each
artifact covers at most 4 cells, and the entries of `dig` are unique.

```
n = 2, artifacts = [[0,0,0,0],[0,1,1,1]], dig = [[0,0],[0,1]]        ->  1
n = 2, artifacts = [[0,0,0,0],[0,1,1,1]], dig = [[0,0],[0,1],[1,1]]  ->  2
```

**Constraints:** `1 <= n <= 1000`; `1 <= artifacts.length, dig.length
<= min(n^2, 10^5)`; `artifacts[i].length == 4`; `dig[i].length ==
2`; `0 <= r1i, c1i, r2i, c2i, ri, ci <= n - 1`; `r1i <= r2i`; `c1i
<= c2i`.

The dug cells go into a set, each as one number r * n + c, and an
artifact counts when every cell of its rectangle is in the set. An
artifact covers at most 4 cells, so O(artifacts + dig).

## Approaches

| file | mechanism |
|---|---|
| `dig.kara` ★ | the dug cells in a `Set[i64]` as r * n + c, and each artifact's rectangle walked, counted when no cell is missing |
| `dig_grid.kara` | an n by n table of flags from `Vec.filled`, set for each dug cell, and each rectangle's flags `and`ed. O(n^2 + artifacts + dig) |
| `dig_owner.kara` | a `Map` from each covered cell to the artifact that owns it, and each artifact's count of buried cells; a dig takes one off its owner, and an owner reaching 0 is extracted. Each cell is counted once because artifacts never overlap and digs are unique |
| `dig_struct.kara` | a `struct Site` holding the dug set, asked `is_dug(r, c)`, and a `struct Artifact` built `from_row`, asked whether it is `uncovered` in the site |
| `dig_iter.kara` | the dug cells `map`ped and `collect`ed into a `Set`, then the artifacts `filter`ed by nested `all` over their rows and columns, and `count`ed |
| `dig_solution.kara` | LeetCode's Rust template: `i32` and two `Vec<Vec<i32>>` in, the dug cells as `(i32, i32)` pairs in a `HashSet` looked up by reference; carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples and four more
(a cell dug beside an artifact, the one cell of a 1 by 1 grid dug, a 2
by 2 missing one corner, and a 1 by 4 dug whole), each with its count;
then the count extracted and a checksum for 2000 random sites on grids
of 1 to 12, with 1 to 20 artifacts of the eight shapes of at most 4
cells tried and from one cell to half and one more dug; then the
constraints' largest, n = 1000 with 10^5 artifacts tried and 10^5 cells
dug. `dig.py` mirrors the ★ arm and its output is byte-identical.

`karac fix` carries the template in three rounds of 12, 1 and 1 edits:
first Rust's spellings (`Vec<..>` and `HashSet<..>` to brackets, `!`
to `not`, `&(r, c)` to `(r, c)`, `struct Solution;` to `struct
Solution {}`, and the `use std::collections::HashSet;` line dropped);
then `HashSet` to `Set`, which the first round's bracket edit exposes;
then the adapter's `as i64` on the template's `i32` answer dropped, since
an `i32` widens to `i64` implicitly.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every cell of every artifact looked for in the dig list
itself, one entry at a time; no set and no table. It checks 300 random
sites on grids of 1 to 8, with 1 to 10 artifacts tried and from one cell
to every cell dug; then 30 with every cell dug; then 30 on grids of 20
to 59, with 30 artifacts tried and half the cells dug. All 360 are drawn
before any arm answers.

| | property |
|---|---|
| P1 | the count is the statement read literally |
| P2 | it is at least 0 and at most the number of artifacts and of cells dug |
| P3 | the dig list reversed: the same count |
| P4 | the site transposed, rows for columns: the same count |
| P5 | the first artifact's missing cells dug too: one more, unless it was whole already |
| P6 | each arm agrees with at least three of the other five |

The transposed site is built with a typed binding in each closure: a
list literal a closure returns is a `Vec`, a closure cannot declare its
return type, and `collect` into a `Vec[Array[i64, 4]]` fails with no
fix; kara B-2026-11-15-38 asks for the closure's literal to follow the type
the `collect` wants.

The differential prints `360 cases: checksum 65701688, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
cases. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to each
other arm, each run under `karac __mir-llvm-run` and `karac __mir-run`.
Seventeen are kept, three to each Kāra arm and two to the Rust-template
arm. Each kept one is killed, fails the same way under both backends and
not by a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the dug cells stored transposed | P1 110, P5 155, P6 110 |
| M2 | ★: the artifact's last row not looked at | P1 207, P2 10, P4 190, P5 108, P6 207 |
| M5 | ★: the last dug cell left out | P1 78, P3 65, P5 198, P6 78 |
| M7 | grid: only the last cell decides | P1 158, P5 70, P6 158 |
| M8 | grid: any cell dug counts | P1 266, P2 20, P5 214, P6 266 |
| M9 | grid: only the first column looked at | P1 95, P4 132, P5 35, P6 95 |
| M12 | owner: the buried count from the sides, not the area | P1 28, P5 6, P6 28 |
| M13 | owner: counted one cell early | P1 241, P2 114, P5 122, P6 241 |
| M15 | owner: only the first row owned | P1 123, P4 140, P5 121, P6 123 |
| M17 | struct: a cell on the diagonal taken as dug | P1 51, P5 20, P6 51 |
| M18 | struct: the bottom row taken as the top | P1 100, P4 132, P5 28, P6 100 |
| M21 | struct: the site's width one more than the grid's | P1 141, P4 151, P5 174, P6 141 |
| M22 | iter: some row all dug is enough | P1 148, P4 172, P5 59, P6 148 |
| M24 | iter: the first dug cell left out | P1 77, P3 65, P5 27, P6 77 |
| M25 | iter: an artifact on the last row never counted | P1 120, P4 100, P5 59, P6 120 |
| M28 | solution: a dug cell's column taken as its row | P1 204, P4 3, P5 212, P6 204 |
| M29 | solution: the rows walked from the bottom up | P1 208, P2 10, P4 202, P5 121, P6 208 |
[('P1', 17), ('P2', 4), ('P3', 2), ('P4', 9), ('P5', 17), ('P6', 17)]

P1, P5 and P6 kill all seventeen, P4 nine, P2 four and P3 two. P3
reorders the dig list, and kills only the two edits that leave out a dug
cell by its place in the list (M5, M24). P2 kills the four that count an
artifact with a cell still buried and so can count more than there are
(M2, M8, M13, M29). P4 transposes the site, and kills the nine that
treat rows and columns differently; it misses the cells stored
transposed (M1), the diagonal (M17) and six whose error is the same
either way round (M5, M7, M8, M12, M13, M24).

Of the thirty-one, fourteen were not kept. One is equivalent: the grid
arm's 1 by 1 grid all dug from the start (M11), since every case digs at
least one cell. Four fail as M1 does: a cell or a dug cell's owner
looked up transposed in the owner, iter and template arms and the
template adapter swapping each dug cell's row and column (M16, M26, M27,
M31). Three fail alike in pairs: the right column left out in the struct
and iter arms (M19, M23), and the struct arm's miss below the top row
ignored (M20) as M18, both looking at the top row only. Six fail their
own way and are left out for the count: the ★ arm's lookup as r * (n -
1) + c, its one-cell artifacts never counted and its flag kept across
artifacts (M3, M4, M6), the grid arm's diagonal not marked (M10), the
owner arm's cells all owned by the first artifact (M14), and the
template adapter dropping the first artifact (M30).

## Verification

Every arm prints the same output as `dig.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 1.8 s to 2.6 s but the
template, 4.6 s, whose adapter copies each site into `Vec[Vec[i32]]`
rows. The differential takes 3.5 s.

## Benchmarks

The bench builds 8 sites of n = 1000 once, each with 20000 artifacts
tried and 300000 cells dug, then counts each one's extracted artifacts
10 times over with the ★ arm in all five languages. C has no set, so its
mirror carries an open-addressing table with a multiplicative hash,
grown from 16 by doubling; Kāra's `Set` and Rust's `HashSet` hash with
SipHash, and Go's map with its own hash. Every implementation prints
`10 passes over 8 sites: checksum 33526167`.

BENCHTAB
