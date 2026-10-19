# 766. Toeplitz Matrix

Given an m by n `matrix`, return whether it is Toeplitz: whether every
diagonal running from top left to bottom right holds the same value
throughout.

```
[[1, 2, 3, 4], [5, 1, 2, 3], [9, 5, 1, 2]]  ->  true
[[1, 2], [2, 2]]                            ->  false
```

**Constraints:** m and n are from 1 to 20; every value is from 0 to 99.

## Approaches

The cells of one diagonal are those with the same row minus column. The
arms check that each such set holds one value in four ways.

| file | mechanism |
|---|---|
| `toeplitz_matrix.kara` ★ | every cell off the top row and left column equals the cell up and to its left; one pass, O(1) space |
| `toeplitz_matrix_diagonals.kara` | each diagonal walked from its start in the top row or left column and compared with its first cell |
| `toeplitz_matrix_keyed.kara` | a `Map` from row minus column to the first value met on that diagonal, every later cell checked against it |
| `toeplitz_matrix_shifted.kara` | each row, less its first value, compared as a slice with the row above, less its last; two rows at a time, as LeetCode's follow-up asks |
| `differential.kara` | the four arms against the definition, four properties |

Every arm borrows the matrix and prints the same 9 lines: the two
LeetCode examples; a 1 by 1 matrix, a single row and a single column,
all Toeplitz; a 3 by 2 matrix both ways; a 3 by 3 matrix broken only in
its last cell; then 300 random matrices of up to 20 by 20, half of them
with one cell changed, with how many are Toeplitz and a checksum.
`toeplitz_matrix.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which compares every pair of cells with the same row minus column. Each
of 1,800 random matrices is built from its diagonals with up to three
values, then a third are left Toeplitz, a third have one cell redrawn
and a third are redrawn entirely. The first 1,500, of up to 6 by 6, are
checked against the definition, and the last 300, of up to 40 by
40, against the other properties.

| | property |
|---|---|
| P1 | the answer is the definition's (the 1,500 small matrices) |
| P2 | the transpose has the same answer |
| P3 | the matrix turned half round has the same answer |
| P4 | the matrix as built from its diagonals is Toeplitz, and is not once a cell that shares its diagonal with another is changed |

It prints `1800 matrices (1235 Toeplitz), 4 arms, 27600 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error; the count is the ★
arm's.

## Mutation testing

Thirteen edits to the differential, three to each arm and a fourth to
the ★ arm, each run under `karac __mir-run`. All thirteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: column 1 never checked | P1 104, P2 153, P3 61, P4 394 |
| M2 | ★: the last row never checked | P1 106, P2 148, P3 68, P4 380 |
| M3 | ★: only a cell smaller than its neighbour caught | P1 71, P3 168, P4 379 |
| M4 | diagonals: the main diagonal never walked | P1 48, P3 62, P4 260 |
| M5 | diagonals: the diagonal from the second row never walked | P1 23, P2 55, P3 50, P4 178 |
| M6 | diagonals: each walk going straight down | P1 256, P2 100, P4 681 |
| M7 | keyed: cells keyed by row plus column | P1 353, P4 959 |
| M8 | keyed: diagonals either side of the main one merged | P1 285, P3 99, P4 768 |
| M9 | keyed: the left column never checked | P1 104, P2 153, P3 61, P4 394 |
| M10 | shifted: the second row never compared | P1 107, P2 153, P3 68, P4 346 |
| M11 | shifted: each row compared with the row above unshifted | P1 351, P2 41, P3 39, P4 954 |
| M12 | shifted: every row compared with the top row | P1 257, P2 106, P3 6, P4 747 |
| M13 | ★: a mismatch only ending its row | P1 437, P4 1142 |

P1 and P4 kill all thirteen. P2, the transpose, misses five: M3 compares
each cell with the same neighbour after transposing, still from below;
M4's main diagonal and M8's merged pair of diagonals map to themselves;
and M7 and M13 answer the same for a matrix and its transpose. P3, the
half turn, misses three: M6 asks that every column hold one value, which
a half turn keeps; M7 checks the other diagonals, which a half turn also
keeps; and M13 never answers false, since its `break` only ends the row
with the mismatch. M3 is seen by P3 because the half turn puts the other
cell of each pair below, and M4 because it moves the main diagonal
elsewhere unless the matrix is square. No first choice survived.

## Verification

Every arm prints the same output as `toeplitz_matrix.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`8a2af7d554`, whose last compiler change is `60d9973e03`. The runtime
archives were built after the last runtime change, `176f59738b`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends accept all four arms, the differential and,
through a copy, the bench. Each arm prints the same output under the
legacy interpreter, `karac run`, `karac build` and an auto-par build,
with a warning that `show` uses `matrix` after moving it, since legacy
predates borrowed parameters. The differential reports no failure under
the legacy interpreter and `karac build` but counts 1231 Toeplitz
matrices, not 1235. Its redrawn cell is written `matrix[r][c] = v` with
all three drawn from the generator, and legacy draws `v` before the two
indices, where core-semantics.md §8.2 evaluates a place's operands
before the value. A three-line program that stores a counter's third
value at the indices given by its first two shows it: every v2 lane
stores 3 at `[0][1]`, the legacy interpreter stores 1 at `[1][2]`, and
the legacy `karac build` of it crashes with a segmentation fault. Legacy
refuses the bench at `is_toeplitz_matrix(pool[k])`, as a move out of an
index; its timing below is of a copy whose parameter is `ref
Vec[Vec[i64]]`. Legacy is frozen, so all this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. Sixteen 200 by
200 Toeplitz matrices of values 0 to 9 are built once; each of
30,000 rounds takes the next of them, adds 0 or 1 to one random cell,
asks whether it is still Toeplitz and puts the cell back, so about half
the answers are true and the rest stop at the changed cell. Matrices ten
times LeetCode's side keep the check, rather than the random numbers,
the work. Every implementation prints `30000 rounds on 200 by
200: 15127 Toeplitz, checksum 34183567`, the Kāra program under `karac
__mir-run` included (in 265 s). The Python mirror holds the two rows it
compares in locals; the others index through the matrix.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.36 to 0.42 s |
| Rust (`rustc -O`) | 0.73 to 1.06 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.75 to 1.02 s |
| Go | 1.06 to 1.39 s |
| Python | 27.0 to 27.7 s |
| Kāra (`karac build --mir`) | 0.61 to 0.78 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, the one this kata measures now that legacy is
frozen. That edit is by hand, on top of the `scripts/new-bench.sh`
output. Under `karac __mir-llvm-run` the program prints the same line in
6.8 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

So at the medians of the interleaved runs the v2 build takes 0.70 s,
against C's 0.39, Rust's 0.92 (0.82 under overflow checks) and Go's
1.18. Under valgrind's cachegrind v2 runs 8.1 billion instructions, Rust
9.9 billion and C 3.4 billion: both checked languages pay for bounds
checks on the rows and the cells, which C does not have. The legacy
build of the copy ran 0.63 to 0.81 s, a median of 0.70 s in the
interleaved runs, so v2 and legacy take the same time, inside M2's limit
of twice legacy; new katas' benches are outside M2's frozen set in any
case. The comparison with C and Rust waits until after M4.

## Compiler findings

None new for v2. The legacy evaluation-order difference above is noted
under the freeze.
