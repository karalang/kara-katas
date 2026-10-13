# 498. Diagonal Traverse

Given an `m x n` matrix `mat`, return an array of all the elements of
the array in a diagonal order.

```
mat = [[1,2,3],[4,5,6],[7,8,9]]  ->  [1,2,4,7,5,3,6,8,9]
mat = [[1,2],[3,4]]              ->  [1,2,3,4]
```

The order zigzags: up and to the right along the first diagonal, down
and to the left along the next, and so on.

**Constraints:** `m == mat.length`; `n == mat[i].length`;
`1 <= m, n <= 10^4`; `1 <= m * n <= 10^4`; `-10^5 <= mat[i][j] <= 10^5`.

## Approaches

Every arm is `fn find_diagonal_order(mat: Vec[Vec[i64]]) -> Vec[i64]`.
The cells of diagonal `d` are those with row + column = `d`.

| file | mechanism |
|---|---|
| `diagonal_traverse.kara` ★ | walking the zigzag one cell at a time; a step that would leave the matrix turns instead (going up: down at the last column, right at the top row; going down: right at the last row, down at the first column) |
| `diagonal_traverse_reverse.kara` | each diagonal collected from its top end, every even diagonal reversed before it is added (`Vec.reverse`, `extend`) |
| `diagonal_traverse_sorted.kara` | every cell as a tuple `(d, row or -row, value)`, sorted; the row rises on odd diagonals and falls on even ones, then `iter().map(...).collect()` keeps the values |
| `diagonal_traverse_direct.kara` | each diagonal walked once from the end the zigzag starts it at, between its top and bottom rows: no reversing and no stepping off the edge |
| `differential.kara` | the four arms on 1,500 random matrices, five properties |

Every arm prints the same 9 lines: the two LeetCode examples, one
cell, one row, one column, a wide and a tall matrix, three by five,
and for 300 random matrices of 1 to 12 by 1 to 12 the count of cells
and a checksum of the order. `diagonal_traverse.py` mirrors the ★ arm
and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random matrices: 1 to 15 by 1 to 15, then 1 to 3 rows, then 1 to
3 columns, in turn, with values from -100,000 to 100,000. P2 to P5 run
each arm on a matrix of the same shape holding each cell's label, row
× n + column, so that the order says which cell came where.

| | property |
|---|---|
| P1 | the order is the reference's, which checks every cell of the matrix for each diagonal in turn |
| P2 | every cell comes out exactly once |
| P3 | the transpose reads each diagonal the other way |
| P4 | each step goes one cell along the diagonal or on to the next diagonal |
| P5 | the top-left cell comes first and the bottom-right cell last |

A case whose labels fail P2 is not checked for P3 to P5, which read
the order as a list of cells.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the walk starts going down | P1 1050 |
| M2 | ★: the walk stops one cell short | P1 1500, P2 1500 |
| M3 | reverse: the odd diagonals are the ones reversed | P1 1050 |
| M4 | reverse: a diagonal stops above the last row | P1 1500, P2 1500 |
| M5 | sorted: every diagonal sorts by rising row | P1 1020 |
| M6 | sorted: the cells sort by the row key before the diagonal | P1 1242, P3 1405, P4 1242, P5 1242 |
| M7 | direct: past the last column a diagonal starts a row too low | P1 1263, P2 1263, P3 217 |
| M8 | direct: an even diagonal leaves out its bottom cell | P1 1500, P2 1500 |

M1 and M3 make the mirror image of the zigzag, every diagonal read the
other way, and M5 reads every diagonal downward. Each is still a walk
over every cell, one diagonal after the next, that starts top left and
ends bottom right, and the mirror image of the transpose is still the
transpose's mirror image, so only P1 sees them. That is what the
reference is for. The other five drop or misorder cells, which P2
catches on its own. M1 and M3 fail the same 1,050 cases: the ones of
more than one row and more than one column, where the two directions
differ. M7 loses cells from every matrix of two or more rows. A single row of
two or more cells loses none, but its transpose is a column that does,
and P3 sees that on 217 such cases.

## Verification

All four arms print the same output as `diagonal_traverse.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file, the bench program included.
The differential prints `30000 checks, 0 failures` on both. The four
arms and the differential also run clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak.

The frozen legacy backends agree on all four arms: `karac run
--interp`, LLJIT, legacy `karac build` and a `KARAC_AUTO_PAR=1` build
print the same output, and the differential prints `30000 checks, 0
failures` under `karac run --interp` and legacy `karac build`. Legacy
`karac build` warns on the differential that `mat` is "moved here,
used again here", where the harness lends the matrix to one arm after
another; the output is right all the same. The bench program does not
build on legacy (see Benchmarks). Legacy is frozen, so this is noted,
not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 100 matrices of 10,000
cells (the problem's most) once, ten of each of ten shapes from 1 by
10,000 to 10,000 by 1 (1, 4, 10, 25, 50, 100, 200, 400, 1,000 and
10,000 rows), with values from -100,000 to 100,000. Then it traverses each 100
times, folding every traversal into a checksum with each value weighed
by its place. Every implementation prints `100 matrices of 10000
cells, 100 times each: checksum 397396001`, the Kāra program under
`karac __mir-run` included (in 84 s).

Every mirror pushes onto a fresh growable array for each traversal, as
the ★ arm pushes onto `Vec.new()`: Rust `Vec::new()`, Go `append`,
Python `append`, and C an array it doubles with `realloc`. Spot
timings on a shared 4-core container, three runs each (two for
Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.30 to 0.36 s |
| Rust (`rustc -O`) | 0.35 to 0.44 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.45 to 0.51 s |
| Go | 0.86 to 0.98 s |
| Python | 18.0 to 18.8 s |
| Kāra (`karac build --mir`) | 0.50 to 0.57 s |

The legacy `karac build` refuses this program: "cannot move out of an
index expression", on `find_diagonal_order(all[k])`, which v2 reads as
a borrow. So `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend. That edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`d9a7136c58`. Under `karac __mir-llvm-run` the program prints the same
line in 2.3 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

## Compiler findings

None. Every arm, the differential and the bench program ran first time
on the v2 backends.
