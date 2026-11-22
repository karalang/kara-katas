# 2768. Number of Black Blocks

You are given two integers `m` and `n` representing the dimensions of a
**0-indexed** `m x n` grid.

You are also given a **0-indexed** 2D integer matrix `coordinates`,
where `coordinates[i] = [x, y]` indicates that the cell with coordinates
`[x, y]` is colored **black**. All cells in the grid that do not appear
in `coordinates` are **white**.

A block is defined as a `2 x 2` submatrix of the grid. More formally, a
block with cell `[x, y]` as its top-left corner where `0 <= x < m - 1`
and `0 <= y < n - 1` contains the coordinates `[x, y]`, `[x + 1, y]`,
`[x, y + 1]`, and `[x + 1, y + 1]`.

Return *a **0-indexed** integer array* `arr` *of size* `5` *such that*
`arr[i]` *is the number of blocks that contains exactly* `i` ***black***
*cells*.

```
m = 3, n = 3, coordinates = [[0, 0]]                  ->  [3, 1, 0, 0, 0]
m = 3, n = 3, coordinates = [[0, 0], [1, 1], [0, 2]]  ->  [0, 2, 2, 0, 0]
```

**Constraints:** `2 <= m <= 10^5`, `2 <= n <= 10^5`, `0 <=
coordinates.length <= 10^4`, `coordinates[i].length == 2`, `0 <=
coordinates[i][0] < m`, `0 <= coordinates[i][1] < n`, `coordinates`
contains pairwise distinct coordinates.

## Approaches

The grid can hold `10^10` blocks, but a black cell lies in at most four,
so only the blocks beside the black cells need counting; every other
block has none.

| file | mechanism |
|---|---|
| `blocks.kara` ★ | each black cell counted into every block it lies in, in a `Map` keyed by the block's top-left corner through `entry`; the blocks in the map counted by how many black cells each holds, and the rest have none. O(c), c the black cells |
| `blocks_sorted.kara` | no hashing: every block a black cell lies in written down as one number, `x * n + y` of its top-left corner, into a `Vec`; sorted, each block's black cells are a run of equal numbers, and the run's length is the count. O(c log c) |
| `blocks_set.kara` | the black cells in a `Set` of pairs; from each black cell every block it lies in is looked at, its four cells asked of the set, and the block counted only from its first black cell in reading order, found by `find`. O(c) |
| `blocks_rows.kara` | the black cells grouped by row in a `SortedMap` from each row to its columns, each list sorted in place through `values_mut`; only the rows of blocks touching a black row are looked at, and in them only the blocks beside a black column, each cell asked by `binary_search`. O(c log c) |
| `blocks_solution.kara` | a Rust solution as LeetCode's Rust users write it, a `HashMap<i64, i32>` keyed by `i * n + j`, each cell's four corners tried by `dx` and `dy` in `0..2` and kept inside the grid, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples; the
greatest grid, `10^5` by `10^5`, with no black cell and with its four
corners black; 100 by 100 all black, `10^4` cells, LeetCode's most, and
a checkerboard over it; 3000 random grids of 2 to 6 by 2 to 6, each at
a density of its own and listed in a random order; and 10 grids up to
`10^5` by `10^5`, each with `10^4` distinct black cells in a square of
side 101 to 1000, the last two with the counts summed and a checksum.
`blocks.py` mirrors the ★ arm and its output is byte-identical.

```
[3, 1, 0, 0, 0]
[0, 2, 2, 0, 0]
[9999800001, 0, 0, 0, 0]
[9999799997, 4, 0, 0, 0]
[0, 0, 0, 0, 9801]
[0, 0, 9801, 0, 0]
3000 small grids: counts sum to [3848, 6251, 6788, 6154, 3923], checksum 806226308
10 grids of 10^4 cells: counts sum to [22398760221, 293427, 39608, 2655, 4848], checksum 494427987
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the grid drawn whole as rows of cells, each black cell
marked, and every block's four cells looked at, the blocks counted by
how many are black; no map. It draws 2000 random grids of 2 to 8 by 2
to 8, then 60 of up to `10^5` by `10^5` with up to 500 black cells, all
before any arm answers; the literal reading is asked only of the first
2000.

| | property |
|---|---|
| P1 | up to 8 by 8, the counts are the literal reading's |
| P2 | the grid transposed: the same counts |
| P3 | the grid turned upside down: the same counts |
| P4 | the black cells listed in reverse: the same counts |
| P5 | no count below 0, the counts summing to (m - 1) (n - 1), and the black cells over all blocks the blocks each black cell lies in |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2060 cases: checksum 227048773, 61800 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases by the same whole grid gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. M1 and M6 fail the same checks. The first M4
and M6, the sorted arm's rows spaced by m and the set arm's bottom-right
corner never asked, crashed, one on an index out of bounds and one on an
unwrap of None, and were replaced.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: every block taken for one with none | P1 1976, P5 2036, P6 2036 |
| M2 | ★: the blocks with the cell in their left column left out | P1 1976, P2 1806, P5 2036, P6 2036 |
| M3 | sorted: a run cut off at two | P1 1478, P5 1200, P6 1478 |
| M4 | sorted: a lone last key never counted | P1 684, P2 40, P3 521, P5 744, P6 744 |
| M5 | set: a block counted from every black cell in it | P1 1848, P5 1859, P6 1859 |
| M6 | set: each block counted one black cell short | P1 1976, P5 2036, P6 2036 |
| M7 | rows: the row of blocks above a black row skipped | P1 551, P2 882, P3 590, P5 611, P6 611 |
| M8 | rows: the columns left unsorted | P1 1597, P2 1757, P4 1791, P5 1638, P6 1638 |
| M9 | solution: blocks past the right edge kept | P1 1736, P2 1753, P5 1736, P6 1736 |
| M10 | solution: only the cell's own row of blocks tried | P1 1935, P2 1725, P3 1583, P5 1995, P6 1995 |

## Benchmarks

The bench draws 100 grids up to `10^5` by `10^5`, each with `10^4`
distinct black cells, LeetCode's most, in a square of side 101 to 1000,
all of them first, then answers each 5 times by the ★ arm in all five
languages: the blocks are in Kāra's `Map`, Rust's `HashMap`, a Go map
and a Python dict, each keyed by a pair, and in C an open-addressing
table with linear probing, its used slots listed and cleared after each
grid. Every implementation prints `100 grids of 10^4 cells, 5 rounds:
counts sum to [1365904485715, 15209130, 1790445, 254840, 111365],
checksum 137764781`.

BENCHTAB

## Verification

All five arms print the same output as `blocks.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The ★, sorted and set arms checked clean as first written. The rows arm
took two `karac fix` edits. It kept its block rows unrepeated by
`block_rows.last() != Some(bx)`, an `Option[ref i64]` against an
`Option[i64]`, and `karac check` refused it; `karac fix` wrote
`.cloned()`. It asked `binary_search(y).is_ok()`, as Rust's
`binary_search` gives a `Result`; Kāra's gives the index as an
`Option[i64]`, and `karac check` warned that `is_ok` on an `Option` is
deprecated and means `is_some`, which `karac fix` wrote.

LeetCode's Rust template took 29 `karac fix` edits, the wrapper
included: `use std::collections::HashMap` became `struct Solution {}`;
the `Vec<..>`s became `Vec[..]`; `HashMap<i64, i32>` and
`HashMap::new()` became `Map[i64, i32]` and `Map.new()`; `&&` became
`and`; `vec![0i64; 5]` became `Vec.filled(5, 0)`; the `&v` patterns
dropped their `&`; `cnt.len() as i64` dropped its cast, a length being
an `i64`; and `Solution::` became `Solution.`. The `as usize` index and
the `as i64` widenings stayed.
