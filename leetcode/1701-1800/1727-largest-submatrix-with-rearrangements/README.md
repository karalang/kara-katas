# 1727. Largest Submatrix With Rearrangements

You are given a binary matrix `matrix` of size `m x n`, and you are
allowed to rearrange the **columns** of the `matrix` in any order.

Return *the area of the largest submatrix within* `matrix` *where
**every** element of the submatrix is* `1` *after reordering the
columns optimally.*

```
matrix = [[0,0,1],[1,1,1],[1,0,1]]   ->  4
matrix = [[1,0,1,0,1]]               ->  3
matrix = [[1,1,0],[1,0,1]]           ->  2
```

**Constraints:** `m == matrix.length`; `n == matrix[i].length`;
`1 <= m * n <= 10^5`; `matrix[i][j]` is either `0` or `1`.

## Approaches

| file | mechanism |
|---|---|
| `submatrix.kara` ★ | a column's height at a row is the run of ones ending there; with a row as the bottom, the heights sorted ascending, the column at k and all after it reach its height, a submatrix `n - k` wide. O(m n log n) |
| `submatrix_order.kara` | no sort: the columns ordered by height at one row keep their order at the next among those that grow, and those that fall to zero go to the end, so each row's order comes from the last in one pass. O(m n) |
| `submatrix_counts.kara` | a height is at most m, so each row's heights are counted into buckets and summed from the tallest down, giving for each height how many columns reach it. O(m (n + m)) |
| `submatrix_solution.kara` | a Rust solution as LeetCode's Rust users write it, the heights written into `mut matrix` itself, then `for row in matrix.iter_mut()` sorted with `sort_unstable_by(\|a, b\| b.cmp(a))` and `ans.max(h * (j as i32 + 1))`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 8 lines: LeetCode's three examples, a single
zero, and 316 rows of 316 ones; then the areas summed and a checksum for
3000 random matrices of up to 5 by 5, 300 of up to 50 by 50, and 5 of
up to 316 by 316, each cell a one with a chance of 3 in 4.
`submatrix.py` mirrors the ★ arm and its output is byte-identical.

```
4
3
2
0
99856
3000 matrices of up to 5 by 5: areas sum to 13953, checksum 631345605
300 matrices of up to 50 by 50: areas sum to 14728, checksum 80394731
5 matrices of up to 316 by 316: areas sum to 1055, checksum 757022129
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every order of the columns, built by swaps, and in each every
submatrix of rows r1 to r2 and columns c1 to c2 whose cells are all
ones; the largest area among them. It checks 3000 random matrices of 1
to 4 rows and 1 to 4 columns, each cell a one with a chance of 2 in 3.
Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the columns in reverse order give the same answer |
| P3 | the rows in reverse order give the same answer |
| P4 | every row repeated, twice in a row, doubles the answer |
| P5 | each arm agrees with at least two of the other three |

P3 holds because a run of rows stays a run when the rows are turned
round, though every arm counts its heights downward. The differential
prints `3000 problems: checksum 211455340, 60000 checks over 4 arms: 0
failures` under every lane in Verification, and a Python reading of the
statement, every `itertools.permutations` of the columns and every
submatrix, gives the same checksum. On a failure it prints the first
ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. M2 and M5 both give each height one
column fewer than reach it, from the two ends of the order, and fail the
very same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the heights not sorted | P1 1384, P2 1376, P5 1384 |
| M2 | ★: a submatrix one column narrower than the columns that reach its height | P1 2873, P5 2873 |
| M3 | ★: a zero keeps the column's height instead of ending it | P1 757, P5 757 |
| M4 | order: a column that falls keeps its height | P1 793, P3 207, P5 793 |
| M5 | order: the k-th column counted k wide, not k + 1 | P1 2873, P5 2873 |
| M6 | order: the order never updated from the first row | P1 1377, P2 1376, P5 1377 |
| M7 | counts: the width only the columns of exactly that height | P1 231, P3 407, P5 231 |
| M8 | counts: the buckets summed from the shortest up | P1 1899, P5 1899 |
| M9 | solution: a one takes the height above it without adding itself | P1 1796, P3 1390, P4 2600, P5 1796 |
| M10 | solution: each row sorted shortest first | P1 1857, P5 1857 |

## Benchmarks

The bench draws 20 random 316 by 316 matrices, `m * n` just under
LeetCode's `10^5`, each cell a one with a chance of 7 in 8 so that the
columns grow tall, all of them first, then answers each 50 times by the
★ arm in all five languages. Every implementation prints `20 matrices of
316 by 316, 50 rounds: areas sum to 1059000, checksum 793917993`. Each
row's heights are copied and sorted: Kāra and Rust use their stable
sorts, Go `sort.Slice`, Python `sorted`, and C `qsort`, all giving the
same sorted heights. The C build also runs clean under gcc's
AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| Kāra (`karac build`) | 0.847 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.847 s |
| Rust (`rustc -O`) | 0.962 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.978 s |
| Go | 3.676 s |
| C (`clang -O3`) | 3.852 s |
| Python | 13 s |

The sequential Kāra build is 12% faster than Rust and 13% faster than
Rust with overflow checks on, the equal-safety comparison
(BENCHMARKS.md).

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.846 s and 0.851 s on one
run).

## Verification

All four arms print the same output as `submatrix.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

The ★, order and counts arms checked clean as first written.

LeetCode's Rust template took one `karac fix` of 10 edits. Rust's
`mut matrix: Vec<Vec<i32>>` is an owned parameter the body changes;
`karac check`'s E0002 says a parameter's mode goes in its type, and the
fix wrote `matrix: own Vec[Vec[i32]]` with `let mut matrix = matrix;`
at the body's start, and declared the bridge's parameter `own` too,
since it hands the matrix on. It also added `struct Solution {}`, wrote
`Vec<Vec<i32>>` as `Vec[Vec[i32]]`, `sort_unstable_by` as `sort_by`
and `|(j, &h)|` as `|(j, h)|`, and declared `ans: i32`, whose literal
met only `ans.max(..)`, a method, which does not fix a literal's type.
`matrix.iter_mut()` over the rows and `j as i32 + 1` carried over as
written.

The differential checked clean as first written. `arm_name` in it
indexes a list of string literals for a `Str`, as #1662's does
(B-2026-11-19-131).
