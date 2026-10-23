# 867. Transpose Matrix

Given a 2D integer array `matrix`, return the transpose of `matrix`. The
transpose of a matrix is the matrix flipped over its main diagonal,
switching the matrix's row and column indices.

```
matrix = [[1,2,3],[4,5,6],[7,8,9]]  ->  [[1,4,7],[2,5,8],[3,6,9]]
matrix = [[1,2,3],[4,5,6]]          ->  [[1,4],[2,5],[3,6]]
```

**Constraints:** `m == matrix.length`; `n == matrix[i].length`;
`1 <= m, n <= 1000`; `1 <= m * n <= 10^5`; `-10^9 <= matrix[i][j] <= 10^9`.

## Approaches

| file | mechanism |
|---|---|
| `transpose_matrix.kara` ★ | one column at a time: row c of the transpose is column c of the matrix, the entries of every row at that column, top to bottom. O(rows * cols) |
| `transpose_matrix_filled.kara` | the transpose is made first, cols rows of rows zeros, and the matrix is read once in its own order, each entry (r, c) written to (c, r): reads along the rows and writes down the columns, the opposite of the ★ arm |
| `transpose_matrix_flat.kara` | through one flat array: the matrix laid out row after row, entry (r, c) at r * cols + c, copied to c * rows + r of a second array, which is cut back into cols rows of rows entries |
| `transpose_matrix_iter.kara` | the ★ arm's loops as iterators: each column index maps to the column it names, collected from every row's entry at that index, and the columns are collected into the transpose |
| `transpose_matrix_blocks.kara` | in square tiles: the matrix is cut into tiles of 8 by 8 entries, smaller at the right and bottom edges, and each tile is copied into the transpose, made first, so that a tile's reads and writes stay within a few cache lines |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's two examples; five more
(a single entry, one row, one column, LeetCode's extreme values, and a
5 by 2 matrix); four random matrices of 10^5 entries, LeetCode's
largest, as 100,000 by 1, 1 by 100,000, 1,000 by 100 and 316 by 316,
with the shape and a checksum before and after; and 1,000 random
matrices of 1 to 20 rows and columns, 107,864 entries in all, with a
checksum of their transposes. `transpose_matrix.py` mirrors the ★ arm
and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every entry at row r, column c is placed in a `Map` at row c,
column r, and the rows are read back out in order of their indices. Its
792 matrices are every shape up to 8 by 8, three times each with random
values, and 600 random matrices of up to 30 by 30; they hold 151,272
entries in all.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | transposed twice, the matrix again |
| P3 | the transpose has cols rows of rows entries each |
| P4 | a row added below the matrix is a column added on the right of its transpose |
| P5 | the rows taken in reverse order reverse every row of the transpose |
| P6 | the matrix split between two columns transposes to the two halves' transposes, one above the other |

It prints `792 matrices of 151272 entries, 23760 checks over 5 arms: 0
failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the last row left out | P1 792, P2 792, P3 792, P4 792, P5 749 |
| M2 | ★: each new row put first | P1 757, P2 789, P4 757, P6 593 |
| M3 | ★: the rows read bottom to top | P1 749, P2 789, P4 792 |
| M4 | filled: each row's entries read right to left | P1 757, P2 789, P4 757, P6 593 |
| M5 | filled: the last column never written | P1 792, P2 792, P4 792, P6 593 |
| M6 | filled: the first row never written | P1 792, P2 792, P5 749 |
| M7 | flat: the entries copied in place | P1 717, P4 757, P5 717, P6 566 |
| M8 | flat: each row cut one short | P1 792, P2 792, P3 792, P4 792, P5 749 |
| M9 | flat: the first row read for every row | P1 749, P2 789, P4 792, P5 749 |
| M10 | iter: each row's entries read right to left | P1 757, P2 789, P4 757, P6 593 |
| M11 | iter: the first row skipped | P1 792, P2 792, P3 792, P5 749 |
| M12 | iter: the columns taken right to left | P1 757, P2 789, P4 757, P6 593 |
| M13 | blocks: a column skipped after every tile | P1 448, P2 550, P4 448, P6 298 |
| M14 | blocks: each tile's last column left out | P1 792, P2 792, P4 792, P6 546 |
| M15 | blocks: a tile row read from its first column | P1 757, P2 789, P4 757, P6 546 |

P1 kills all fifteen. A mutation that reorders entries fails every
matrix but the ones its reordering cannot see, which is where the
counts 757 and 749 come from: the matrices with more than one column
(M2, M4, M10, M12, M15) and with more than one row (M3, M9), as read
from these counts rather than counted separately.
P3 sees only the mutations that change the shape (M1, M8, M11). M13
fails only the 448 matrices wider than 8 columns, where a second tile
starts. A first M2, the first column left out, made the transpose of a
one-column matrix empty, and the differential then stopped with an
index out of bounds instead of counting a failure; it was replaced.

## Verification

Every arm prints the same output as `transpose_matrix.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build and the runtime archives are at kara
`292a4ca2f0`. Under `karac __mir-run` the arms take 3 to 5 s each and
the differential 6 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The frozen legacy backends refuse all five arms and the bench program
at a `*` on a `for` element, saying the value is not a reference, where
v2 yields a reference. They run the differential, which has no such
`*`, and report 0 failures, but `karac run --legacy --interp` counts
149,105 entries where every other lane counts 151,272. Legacy is
frozen, so both are noted, not filed.

## Benchmarks

The bench program uses the ★ arm, in all five languages: a random 1,000
by 100 matrix, LeetCode's largest, built once, and 6,000 transposes in a
row, each of the last one, with a checksum of one entry after each and
of the whole matrix at the end. Every language keeps a row as its own
array of 64-bit entries (LeetCode's C and Rust signatures use 32-bit
ones) and builds the transpose as Kāra does: Rust and Go push onto empty
vectors, C allocates each row at its final size and frees the old
matrix. Every implementation prints `6000 transposes of a 1000 x 100
matrix: 1000 x 100, checksum 722928690`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.91 to 1.05 s | 0.96 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.95 to 1.06 s | 0.97 s |
| Rust (`rustc -O`) | 1.57 to 1.70 s | 1.66 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.62 to 1.83 s | 1.68 s |
| Rust (the same with `-C target-cpu=x86-64-v3`) | 1.59 to 1.87 s | 1.73 s |
| Go | 7.01 to 7.32 s | 7.09 s |
| Python | 22.6 s | |
| Kāra (`karac build --mir`) | 0.56 to 0.68 s | 0.64 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 866's does. The frozen legacy `karac build`
refuses the bench program (see Verification), so there is no legacy
time.

v2 is the fastest here, and the reasons are not the transpose itself.
Half of C's time is the kernel's: `/usr/bin/time` shows 0.41 s of user
time, 0.49 s of system time and 492,309 minor page faults, against v2's
0.62 s of user time, no system time and 498 faults. glibc gives the
freed matrix back to the system at every round and takes it again at
the next, so C's user time alone is two thirds of v2's. Rust runs 21.2
billion instructions under valgrind's cachegrind, against C's 3.6
billion and v2's 8.3 billion, with 131 million mispredicted branches to
v2's 4.4 million: its `push` onto an empty vector grows it by
reallocating, with a capacity check on every entry. The x86-64-v3 builds
change nothing. Why Go takes 7.1 s, and where v2's instructions go
beyond C's, was not traced; the comparison with C and Rust waits until
after M4.
