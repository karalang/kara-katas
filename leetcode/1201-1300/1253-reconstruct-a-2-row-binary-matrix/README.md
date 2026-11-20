# 1253. Reconstruct a 2-Row Binary Matrix

Given the following details of a matrix with `n` columns and `2` rows:

- The matrix is a binary matrix, which means each element in the matrix
  can be `0` or `1`.
- The sum of elements of the 0-th (upper) row is given as `upper`.
- The sum of elements of the 1-st (lower) row is given as `lower`.
- The sum of elements in the i-th column (0-indexed) is `colsum[i]`,
  where `colsum` is given as an integer array with length `n`.

Your task is to reconstruct the matrix with `upper`, `lower` and
`colsum`. Return it as a 2-D integer array. If there are more than one
valid solution, any of them will be accepted. If no valid solution
exists, return an empty 2-D array.

```
upper = 2, lower = 1, colsum = [1,1,1]                      ->  [[1,1,0],[0,0,1]]
upper = 2, lower = 3, colsum = [2,2,1,1]                    ->  []
upper = 5, lower = 5, colsum = [2,1,2,0,1,0,1,2,0,1]        ->  [[1,1,1,0,1,0,0,1,0,0],[1,0,1,0,0,0,1,1,0,1]]
```

**Constraints:** `1 <= colsum.length <= 10^5`; `0 <= upper, lower <=
colsum.length`; `0 <= colsum[i] <= 2`.

The arms are `fn reconstruct_matrix(upper: i64, lower: i64, colsum:
Vec[i64]) -> Vec[Vec[i64]]`, the column sums borrowed.

## Approaches

| file | mechanism |
|---|---|
| `reconstruct_matrix.kara` ★ | greedy in two passes: the 2s counted first, since each takes a 1 from both rows, then each column of 1 giving its 1 to the upper row while it has room left after the 2s, and to the lower row after |
| `reconstruct_matrix_balance.kara` | greedy in one pass: what each row still has to give in a two-element array, a 2 taking from both and a 1 going to whichever has more left, chosen by a `match` with a guard; a count below zero, or left over, means no matrix |
| `reconstruct_matrix_lift.kara` | by lifting: every column's 1 put in the lower row first, then 1s lifted to the upper row from the right until it holds `upper` |
| `reconstruct_matrix_iter.kara` | by iterators: the upper row a `map` over `colsum` whose closure counts down the 1s the row still takes, the lower row the column sums less the upper, with `zip` |
| `reconstruct_matrix_solution.kara` | a Rust solution as LeetCode's Rust users write it (`vec![vec![0; n]; 2]`, `let (mut u, mut l)`, `\|\|`, `Vec<Vec<i32>>`, the one-pass greedy), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

The arms need not build the same matrix, and LeetCode accepts any, so
the harness judges each answer: a matrix of two rows of 0s and 1s whose
rows add to `upper` and `lower` and whose columns add to `colsum`, the
empty answer, or wrong. Every arm prints the same 3 lines: LeetCode's
three examples (`matrix [] matrix`); for 1000 random cases of 1 to 2000
columns, each with its own share of 2s and half of them with row sums
moved by -1 to 1, the matrices built, the wrong answers and a checksum
of the verdicts (`677 built, 0 wrong, checksum 522091707`); and three
cases at the constraints' top, 100000 columns of 2s, 100000 of 1s split
evenly, and the same with the upper row one short. `reconstruct_matrix.py`
mirrors the ★ arm, and its output is byte-identical. Every arm gives the
same output under `karac run` and `karac build`, and under the
AddressSanitizer build.

The Mend loop: the four Kāra arms checked clean as first written, the
`map` closure in the iterator arm counting down a captured `take`
included. The solution arm takes one round of fixes, 18 edits by `karac
fix`'s count (`struct Solution;` to `struct Solution {}`, `Vec<i32>` and
`Vec<Vec<i32>>` to brackets, `vec![vec![0; n]; 2]` to `Vec.filled(2,
Vec.filled(n, 0))`, `let (mut u, mut l)` to `let mut (u, l)`, the two
`||` to `or`, and the two `return vec![]` to `return Vec.new()`). The
same round took the `.to_string()` off the harness's three string arms
of a `match` that gives a `String`. All five check clean.

## Gaps

None found: every arm, as written, checks after its fixes, and runs and
builds alike.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every matrix of two rows of 0s and 1s as long as `colsum`
tried, and a matrix exists when one has the row and column sums. 2000
cases of 1 to 6 columns, each with its own share of 2s and half of them
with row sums moved, each arm's answer judged as in the harness.

| | property |
|---|---|
| P1 | the statement read literally: a matrix when one exists, the empty answer when none does |
| P2 | the columns reversed give the same verdict |
| P3 | `upper` and `lower` swapped give the same verdict |
| P4 | a column of 2 added, with both row sums raised by 1, gives the same verdict |
| P5 | a column of 0 added gives the same verdict |
| P6 | the ★ arm's verdict |

All 60,000 checks pass on every arm: `2000 cases: checksum 408966771,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python, trying every
upper row, gives the same checksum.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: the upper row's last 1 left to the lower row | P1 456, P3 536, P6 1824 |
| S2 | ★: no check that the lower row can take the 2s | P1 58, P3 122, P6 232 |
| B1 | balance: a 1 to the upper row while it has any left | P1 149, P2 167, P3 233, P4 285, P6 149 |
| B2 | balance: only the upper row checked for leftovers | P1 170, P3 180, P6 170 |
| T1 | lift: the lifting started one column before the end | P1 133, P2 156, P3 254, P4 133, P5 133, P6 133 |
| T2 | lift: an upper row already over `upper` let through | P1 67, P3 124, P6 67 |
| I1 | iterators: one 1 too many taken by the upper row | P1 434, P3 536, P6 434 |
| I2 | iterators: row sums over the column total let through | P1 353, P6 353 |
| L1 | solution: a 1 to the row with less left | P1 713, P6 713 |
| L2 | solution: a 2 not counted against the lower row | P1 869, P2 2, P3 31, P4 462, P6 869 |

All ten are caught, every one by P1, the statement read literally, and
by P6, which fails on the other four arms too when the ★ arm is the one
mutated (S1, S2). P3, the row sums swapped, catches the eight that treat
the two rows differently; L1 and I2 treat them alike, and only P1 and P6
catch those. P2 and P4, the columns reversed and a column of 2 added,
catch the three whose answer hangs on the order of the columns or on
how many 2s come first: the upper row served first in one pass (B1), the
lifting started one column short (T1), and a 2 left off the lower row's
count (L2). P5, a column of 0 added, catches only T1, whose column left
out becomes the 0.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (the 2s counted first, then each column of 1 giving its 1 to the
upper row while it has room, and to the lower after) on 20 random cases
of 100000 columns built once, each with its own share of 2s and half of
them with no matrix; each asked 50 times, every answer folded into a
checksum. Every program prints `50 rounds of 20 cases of 100000 columns:
checksum 401563080`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.388 to 0.456 s | 0.425 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.387 to 0.455 s | 0.432 s |
| Rust (`rustc -O`) | 0.342 to 0.437 s | 0.381 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.633 to 0.759 s | 0.685 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.664 to 0.764 s | 0.683 s |
| C (`clang -O3`) | 0.564 to 0.627 s | 0.583 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.540 to 0.602 s | 0.559 s |
| Go | 0.523 to 0.616 s | 0.564 s |
| Python | 11.87 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on takes about 1.6x Kāra's time. Kāra
is about 26% ahead of C (0.432 s against 0.583 s); Kāra is about 23%
ahead of Go (0.432 s against 0.564 s). Python takes about 27x Kāra's
time. No profile was taken.
