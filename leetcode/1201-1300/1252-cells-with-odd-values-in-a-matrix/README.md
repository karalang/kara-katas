# 1252. Cells with Odd Values in a Matrix

There is an `m x n` matrix that is initialized to all `0`'s. There is
also a 2D array `indices` where each `indices[i] = [ri, ci]` represents a
0-indexed location to perform some increment operations on the matrix.

For each location `indices[i]`, do **both** of the following:

1. Increment **all** the cells on row `ri`.
2. Increment **all** the cells on column `ci`.

Given `m`, `n`, and `indices`, return *the number of odd-valued cells in
the matrix after applying the increment to all locations in* `indices`.

```
m = 2, n = 3, indices = [[0,1],[1,1]]  ->  6
m = 2, n = 2, indices = [[1,1],[0,0]]  ->  0
```

**Constraints:** `1 <= m, n <= 50`; `1 <= indices.length <= 100`;
`0 <= ri < m`; `0 <= ci < n`.

The arms are `fn odd_cells(m: i64, n: i64, indices: Vec[Vec[i64]]) -> i64`,
the places borrowed, as LeetCode's `[r, c]` lists.

## Approaches

| file | mechanism |
|---|---|
| `odd_cells.kara` ★ | the matrix itself, a `Vec.filled` of `Vec.filled` rows: every cell of each place's row and column raised by one, then the odd cells counted |
| `odd_cells_counts.kara` | by counts: how often each row and each column was raised, and a cell odd when its row's count and its column's add to an odd number |
| `odd_cells_formula.kara` | by a formula: each row and column a `bool` flipped with `not`, and the count odd rows times even columns plus even rows times odd columns |
| `odd_cells_bits.kara` | by bits: the odd rows and the odd columns each a `u64` mask flipped with `^=`, the formula's counts read with `count_ones` |
| `odd_cells_solution.kara` | a Rust solution as LeetCode's Rust users write it (`vec![vec![0; n as usize]; m as usize]`, `flatten`, `\|&&x\|`, `Vec<Vec<i32>>`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's two examples; the total
and a checksum of the counts for 1000 random matrices of 1 to 50 rows and
columns with 1 to 100 places (`total 292343, checksum 920274776`); and
three 50 by 50 matrices at the constraints' top: the corner 99 times
(98), row `i % 50` and column `i % 37` for `i` to 99 (1300), and the 50
places of row 0 with 49 of column 0 (98). `odd_cells.py` mirrors the ★
arm, and its output is byte-identical. Every arm gives the same output
under `karac run` and `karac build`, and under the AddressSanitizer
build.

The Mend loop: the ★, counts and formula arms checked clean as first
written. The bits arm was first written with Rust's `rows.count_ones() as
i64`, and `karac fix` drops the two casts, since `count_ones` already
gives an `i64`. The solution arm takes one round of fixes, 11 edits by
`karac fix`'s count (`struct Solution;` to `struct Solution {}`,
`Vec<Vec<i32>>` to `Vec[Vec[i32]]`, the two `vec!` to `Vec.filled(m,
Vec.filled(n, 0))`, `.flatten()` over rows borrowed from the matrix to
`.flat_map(|v| v.iter())`, `|&&x|` to `|x|`, and, in the harness's own
call, the `as i64` on an `i32` that widens by itself). All five check
clean.

## Gaps

None found: every arm, as written, checks after its fixes, and runs and
builds alike.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally, cell by cell: a cell's value one for each place on its row
and one for each place on its column, and the cells whose value is odd
counted. 2000 cases of 1 to 8 rows and columns with 1 to 12 places.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the matrix transposed, rows and columns swapped in every place, gives the same count |
| P3 | the places in reverse order give the same count |
| P4 | every place given twice leaves no odd cell |
| P5 | the rows turned upside down give the same count |
| P6 | the ★ arm's count |

All 60,000 checks pass on every arm: `2000 matrices: checksum 997475331,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python, from the
parities of the rows and columns, gives the same checksum.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: the last row left out of each column's raise | P1 1768, P2 1510, P5 765, P6 7072 |
| S2 | ★: the even cells counted | P1 1384, P4 2000, P6 5536 |
| C1 | counts: a cell odd when its row's count and its column's are both odd | P1 1832, P6 1832 |
| C2 | counts: a row raised by two | P1 1434, P2 1768, P6 1434 |
| F1 | formula: `m` and `n` swapped | P1 1009, P6 1009 |
| F2 | formula: a row set odd rather than flipped | P1 1090, P2 1417, P4 2000, P6 1090 |
| B1 | bits: a row's bit set with `\|=` rather than flipped | P1 1090, P2 1417, P4 2000, P6 1090 |
| B2 | bits: even rows times even columns in the formula | P1 1462, P2 1768, P4 2000, P6 1462 |
| L1 | solution: the first column left out of each row's raise | P1 1756, P2 1480, P6 1756 |
| L2 | solution: a column's cells set to 1 rather than raised | P1 1844, P2 1548, P3 1054, P4 2000, P6 1844 |

All ten are caught, every one by P1, the statement read literally, and
by P6, which fails on the other four arms too when the ★ arm is the one
mutated (S1, S2). P2, the matrix transposed, catches the seven that
treat rows and columns differently (S1, C2, F2, B1, B2, L1, L2). P4,
every place given twice, catches the five that leave an odd cell or
count one where every value is even: the even cells counted (S2), a row
set rather than flipped (F2, B1), even rows times even columns (B2), and
a cell set to 1 (L2). P5, the rows upside down, catches only S1, whose
missing row is the last; L1's missing column would need the columns
turned around. P3, the places reversed, catches only L2, where a cell
set to 1 forgets what came before it. C1 and F1 keep every property but
P1 and P6: both are as symmetric in rows and columns as the true count,
and both see only parities.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (the matrix itself, every cell of each place's row and column raised
by one, then the odd cells counted) on 1000 random lists of 100 places
in a 50 by 50 matrix built once, each asked 40 times; every count folded
into a checksum. Every program prints `40 rounds of 1000 lists of 100
places in 50 by 50: checksum 76291480`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.410 to 0.468 s | 0.444 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.402 to 0.473 s | 0.423 s |
| Rust (`rustc -O`) | 0.266 to 0.325 s | 0.299 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.471 to 0.558 s | 0.496 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.433 to 0.494 s | 0.459 s |
| C (`clang -O3`) | 0.130 to 0.164 s | 0.139 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.112 to 0.155 s | 0.118 s |
| Go | 0.753 to 0.847 s | 0.812 s |
| Python | 18.11 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra is about 15% ahead of Rust with overflow checks on (0.423 s
against 0.496 s), and the two ranges overlap. Kāra takes about 3.0x C's
time (0.423 s against 0.139 s); Go takes about 1.9x Kāra's time. Python
takes about 43x Kāra's time. No profile was taken.
