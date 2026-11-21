# 1605. Find Valid Matrix Given Row and Column Sums

You are given two arrays `rowSum` and `colSum` of non-negative integers
where `rowSum[i]` is the sum of the elements in the `i`th row and
`colSum[j]` is the sum of the elements of the `j`th column of a 2D
matrix. In other words, you do not know the elements of the matrix, but
you do know the sums of each row and column.

Find any matrix of **non-negative** integers of size
`rowSum.length x colSum.length` that satisfies the `rowSum` and `colSum`
requirements.

Return *a 2D array representing* ***any*** *matrix that fulfills the
requirements*. It's guaranteed that **at least one** matrix that
fulfills the requirements exists.

```
rowSum = [3,8],    colSum = [4,7]    ->  [[3,0],[1,7]]
rowSum = [5,7,10], colSum = [8,6,8]  ->  [[0,5,0],[6,1,0],[2,0,8]]
```

**Constraints:** `1 <= rowSum.length, colSum.length <= 500`;
`0 <= rowSum[i], colSum[i] <= 10^8`;
`sum(rowSum) == sum(colSum)`.

## Approaches

Any matrix that meets the sums is an answer. Each arm here gives the
same one, the northwest corner: every cell, in reading order, takes the
smaller of what its row and its column still need. Whichever runs out
is finished, and since the two lists add to the same total, the last
cell finishes both. LeetCode's second example shows another answer;
the one printed here is `[[5,0,0],[3,4,0],[0,2,8]]`.

| file | mechanism |
|---|---|
| `restore.kara` ★ | the two sums taken `own` and walked cell by cell, row by row, each row a `Vec.filled` pushed onto the matrix. O(rows * cols) |
| `restore_walk.kara` | the northwest corner walk: one `(i, j)` walk over a zeroed `Vec.filled(rows, Vec.filled(cols, 0))`, down when the row is met and right when the column is. O(rows + cols) steps after the zeroed matrix |
| `restore_columns.kara` | column by column: each column built by `iter_mut().map(..)` over what the rows still need, the closure writing both the row's need and the column's remainder, and the columns turned into rows by `(0..rows).map(..)` at the end. O(rows * cols) |
| `restore_solution.kara` | LeetCode's Rust template (`mut` parameters, `vec![vec![0; n]; m]`, `std::cmp::min`), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and four more
(one cell, a row of sum zero, one row, one column), each with the check
that its rows and columns add up, then the cells, the count valid and a
checksum of the matrices for 3000 problems of up to 4 by 4 cells from 0
to 9, 300 of up to 100 by 100 cells to 1000, and 3 of up to 500 by 500
cells to 100000. Each problem's sums are made from a random matrix, which
is then forgotten. `restore.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: the answer's shape, each entry not negative, and each row and
each column added up and compared with its sum. It checks 3000 problems
made from matrices of 1 to 4 by 1 to 4 cells from 0 to 9, every random
choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer meets the statement read literally |
| P2 | the problem transposed is answered with the answer transposed |
| P3 | every sum tripled is answered with every cell tripled |
| P4 | a row of sum zero added is answered with a row of zeros added |
| P5 | the answer has at most rows + cols - 1 cells that are not zero |
| P6 | each arm agrees with at least two of the other three |

P2 to P5 hold for the northwest corner, not for every valid answer: P6
is what would catch an arm that answers validly but differently.

The differential prints `3000 problems: checksum 494008727, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. M9 is the one only P6 kills: the
template filling each row from the right gives the northeast corner, an
answer as valid as the one asked for, and the property checks cannot tell
it from a right one.

The first M4, the walk stepping right only while its row still needed
something, was killed only by an index panic, and was replaced.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a column never told what it gave | P1 1672, P2 1672, P5 239, P6 1672 |
| M2 | ★: no cell above 9 | P1 960, P3 2805, P5 1108, P6 1365 |
| M3 | ★: the last row never filled | P1 3000, P2 3000, P4 2919, P6 3000 |
| M4 | walk: the last column never filled | P1 2934, P2 2682, P6 2934 |
| M5 | walk: each cell given its row's whole need | P1 2115, P2 2748, P6 2115 |
| M6 | columns: a row never told what it gave | P1 1672, P2 1672, P5 235, P6 1672 |
| M7 | columns: the columns turned into rows back to front | P1 2115, P2 2733, P6 2172 |
| M8 | template: a cell given one more than its column needs | P1 2184, P2 2769, P3 2184, P6 2184 |
| M9 | template: each row filled from the right | P6 1672 |
| M10 | columns: a fifth of each column held back | P1 2763, P2 2615, P3 2490, P6 2763 |

## Benchmarks

The bench makes 100 problems made from 1000 by 1000 matrices of cells from 0 to 1000, all of it first. Then: greedy cell by cell, a fresh Vec per row. Every implementation prints `100 problems of 1000 by 1000: 199900 cells not zero, checksum 91870405`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5bb1708545` on LLVM 22:

| | median |
|---|---|
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.302 s |
| Kāra (`karac build`) | 0.302 s |
| C (`clang -O3`) | 0.357 s |
| Rust (`rustc -O`) | 0.360 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.376 s |
| Go | 0.823 s |
| Python | 29 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its user time is not above its real time (0.296 s and 0.296 s on one run).

## Verification

All four arms print the same output as `restore.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`21cdf88b69`.

## Writing it

The ★ and columns arms were written in Kāra and checked as written. The
walk arm wrote Rust's `let (mut i, mut j) = (0, 0)`, and `karac fix` made
it `let mut (i, j) = (0, 0)`. The shared harness wrote a nested
`collect::[Vec[String]]()` with a type list, and `karac fix` made it
`Vec[String].from_iter(..)`, then warned that the `f"{x}"` it left inside
the f-string's hole is a nested f-string, deprecated; that was written
`x.to_string()` by hand. `karac fix` also dropped five `as i64` casts the
harness did not need. Its two sums, `Vec.filled(rows, 0)` added to with
`i32` cells, were refused as `Vec[i64]` passed for `Vec[i32]`, with
advice to annotate and no fix; they were annotated by hand. The
differential wrote `filter(|x| **x != 0)` and `karac fix` took a `*` off.

The Rust template took one `karac fix` of 15 edits: `struct Solution;`
to `struct Solution {}`, the `<..>` types to `[..]`, each `mut`
parameter to `own` with a `let mut` rebinding it, `vec![vec![0; n]; m]`
to `Vec.filled(m, Vec.filled(n, 0))`, `std::cmp::min` to `min`, and
`Solution::` to `Solution.`. It then checks and agrees with no hand edit.
