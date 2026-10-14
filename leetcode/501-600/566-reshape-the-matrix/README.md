# 566. Reshape the Matrix

In MATLAB, there is a handy function called `reshape` which can reshape
an `m x n` matrix into a new one with a different size `r x c` keeping
its original data. You are given an `m x n` matrix `mat` and two
integers `r` and `c` representing the number of rows and the number of
columns of the wanted reshaped matrix. The reshaped matrix should be
filled with all the elements of the original matrix in the same
row-traversing order as they were. If the reshape operation with given
parameters is possible and legal, output the new reshaped matrix;
otherwise, output the original matrix.

```
mat = [[1,2],[3,4]], r = 1, c = 4  ->  [[1,2,3,4]]
mat = [[1,2],[3,4]], r = 2, c = 4  ->  [[1,2],[3,4]]
```

**Constraints:** `1 <= m, n <= 100`; `-1000 <= mat[i][j] <= 1000`; `1 <=
r, c <= 300`.

## Approaches

Every arm is `fn matrix_reshape(mat: Vec[Vec[i64]], r: i64, c: i64) ->
Vec[Vec[i64]]`, and every arm returns a copy of `mat` when `m * n != r *
c`.

| file | mechanism |
|---|---|
| `matrix_reshape.kara` ★ | index arithmetic: the k-th value in row-major order is at row k / c, column k % c of the new matrix and row k / n, column k % n of the old; each new row built by `push`; O(m * n) |
| `matrix_reshape_flat.kara` | the rows laid end to end in one `Vec` by `flat_map(\|row\| row.iter())`, and each new row a slice of it copied with `to_vec()` |
| `matrix_reshape_cursor.kara` | an r by c matrix of zeros written through a cursor that moves along its row and wraps to the next; no division |
| `matrix_reshape_fromfn.kara` | the ★ arm's arithmetic as two nested `Vec.from_fn` calls whose closures read `mat` |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 11 lines: nine reshapes at the edges (the two
examples, the same shape, one value, a row to a column and back, 2 by
3 to 3 by 2, the extreme values, and a count that is close but wrong), a
count of kept matrices and a checksum over 300 random matrices of 1 to
8 by 1 to 8, each reshaped to a shape that fits or, one time in four,
one column too wide, and the problem's largest, 100 by 100 reshaped to
1 by 10000, then 10000 by 1, then back. `matrix_reshape.py` mirrors the
★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
the statement read literally: every value read row by row onto a list,
then the new matrix filled row by row from the front of that list, or
the original kept when the counts differ. Each arm is held to the
properties below on 1,000 random matrices of 1 to 6 by 1 to 6, values
from -1000 to 1000 or from -1 to 1, each reshaped in turn to a shape
with the same count or to any shape of 1 to 12 by 1 to 12, which mostly
does not fit.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | when the counts match, r rows of c values each; otherwise the original |
| P3 | the answer reshaped back to m by n is the original |
| P4 | the answer's values in row-major order are the original's |
| P5 | reshaped first to one long row and then to r by c, the answer is the same; a shape that does not fit keeps the long row |

It prints `1000 cases, 4 arms, 20000 checks, 0 failures` under `karac
__mir-run` and `karac __mir-llvm-run`, and runs clean under `karac
__mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac
__mir-llvm-run`. All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the values read column by column | P1 345, P3 625, P4 345 |
| M2 | ★: a reshape to one row refused | P1 59, P2 59, P3 46 |
| M3 | flat: each new row one value short | P1 511, P2 511, P3 1000, P4 511, P5 404 |
| M4 | flat: the rows in reverse order | P1 389, P3 750, P4 389 |
| M5 | cursor: the row never advanced | P1 398, P3 882, P4 398 |
| M6 | cursor: every value negated | P1 502, P3 485, P4 502, P5 502 |
| M7 | fromfn: the values laid down column by column | P1 310, P3 625, P4 310 |
| M8 | fromfn: a shape that does not fit gives the first row only | P1 426, P2 426, P3 426, P4 426 |
| E1 | ★: each row given room for c values up front | 0 |
| E2 | flat: the count compared the other way round | 0 |
| E3 | cursor: the wrap tested with `>=`, not `==` | 0 |
| E4 | fromfn: the position named once in a block | 0 |

P3 is the strongest property here: reshaping back runs the arm a second
time, on the answer, so a mutant that is right on some shapes is usually
wrong on the way back, and M3 fails it on every case. It sees M6 only on
the shapes that do not fit: when both reshapes fit, negating twice gives
the values back, and when the first does not, the answer is the
untouched original and reshaping it back negates it. P2 sees only the
three mutants that change a shape: M2, M3 and M8. P5 compares the arm
with itself, so a mutant that is wrong the same way by both routes
passes it; it sees M3, whose short rows compound, and M6, whose second
negation undoes the first. M2 fails only where the wanted shape is one
row and the original has more. E1 is safe because room reserved is not
length, E3 because the cursor never passes c.

## Verification

Every arm prints the same output as `matrix_reshape.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. `karac check`
passes on every arm, the differential and the bench program.

The frozen legacy backends: `karac run --interp`, `karac run` and `karac
build` stop every arm and the differential at type checking, on `*x`
over `iter()` of a `Vec[i64]` ("unary '*' requires 'ref T' ... found
'i64'"), in the harness's checksum loop and in the cursor arm's
`out[row][col] = *x`, as for kata 545. Legacy refuses the bench program
too (see Benchmarks). Legacy is frozen, so these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 20 random 100 by 100 matrices
once (the problem's most), values from -1000 to 1000. Then 800 times
over every matrix is reshaped to the next of ten shapes in turn: 1 by
10000, 4 by 2500, 25 by 400, 50 by 200, 100 by 100, 200 by 50, 400 by
25, 2500 by 4 and 10000 by 1, which all fit, and 99 by 101, which does
not and gives back a copy. Every implementation prints `20 matrices of
100 by 100, 800 rounds: 160000000 cells, checksum 176394086`, the Kāra
program under `karac __mir-run` included (90 s).

Rust and Go build each new row by pushing, as the Kāra arm does, and
copy the matrix for the shape that does not fit; C allocates each row at
its final size, and Python appends to lists. Spot timings on a shared
4-core container, three runs each (two for Python; `bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.98 to 1.00 s |
| Rust (`rustc -O`) | 1.59 to 1.98 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.66 to 1.93 s |
| Go | 3.80 to 3.90 s |
| Python | 13.8 to 15.2 s |
| Kāra (`karac build --mir`) | 1.45 to 1.70 s |

The legacy `karac build` refuses this program, since it moves
`mats[(round * 7 + g) % count]` out of the index where v2 borrows it. So
`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`2d241d9b05`. Under `karac __mir-llvm-run` the program prints the same
line in 4.3 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

Re-timed on 2026-10-14 at kara `2d241d9b05`. The row first published
here, 1.81 to 1.96 s, was taken with a runtime archive older than kara
`8969be0434`, which runs `main` on a second thread, and once a process
has two threads glibc's `malloc` and `free` take a lock on every call.
Linked against that older runtime and against the current one by the
same compiler, three runs each, the program takes 2.00 to 2.23 and
1.51 to 1.79 s: the older runtime alone costs this program about 21%.

The Kāra row is level with Rust's. C allocates each new row at its final
size where the others grow theirs by pushing, the likeliest reason it is
faster (not measured). Go's rows also grow by `append`; why Go takes
about twice Rust's time was not looked into.

## Compiler findings

kara B-2026-10-14-18 (open), filed from this kata: `karac check` accepts
`mat.iter().flatten().collect()` on a `Vec[Vec[i64]]`, but the spec's
`flatten` takes only an iterator whose items are themselves iterators
(`where Self.Item: Iterator`), and both MIR backends refuse it ("`ref
Vec[i64]` does not implement `Iterator`"). A program that passes `karac
check` does not run. The flat arm uses the spec's spelling,
`flat_map(|row| row.iter())`, which runs everywhere on v2. The row asks
whether the spec should instead widen `flatten` to items that can be
iterated, as Rust's does, since flattening a `Vec[Vec[T]]` is its common
use.
