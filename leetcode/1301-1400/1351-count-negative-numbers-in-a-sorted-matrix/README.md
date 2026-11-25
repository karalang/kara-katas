# 1351. Count Negative Numbers in a Sorted Matrix

Given an `m x n` matrix `grid` which is sorted in non-increasing order
both row-wise and column-wise, return the number of negative numbers in
`grid`.

```
grid = [[4,3,2,-1],[3,2,1,-1],[1,1,-1,-2],[-1,-1,-2,-3]]   ->  8
grid = [[3,2],[1,0]]                                        ->  0
```

**Constraints:** `1 <= m, n <= 100`, `-100 <= grid[i][j] <= 100`.

The arms are `fn count_negatives(grid: Vec[Vec[i32]]) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `count_negatives.kara` ★ | a staircase walk from the bottom-left corner: while the value there is negative, so is the rest of its row to the right, so count them and move up a row; otherwise move right. O(m + n) |
| `count_negatives_search.kara` | each row's first negative found by a binary search; the columns are sorted too, so a row's first negative is no later than the row above's, and each search stops there. O(m log n) |
| `count_negatives_cells.kara` | every cell looked at, the order not used. O(m * n) |
| `count_negatives_flat.kara` | the rows run together by `flat_map`, the negatives kept by `filter` and counted. O(m * n) |
| `count_negatives_solution.kara` | a Rust solution as LeetCode's Rust users write it (each row's negatives as `row.len() - row.partition_point(\|&x\| x >= 0)`, mapped and summed), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's two examples; one value,
negative and zero; every value negative; and 100 by 100, the
constraints' largest, from 100 down by random steps of 0 to 2 (`8 0 1 0
6 7415`); and 2000 random sorted grids of 1 to 30 rows and columns, most
of them small, from a top of -5 to 30 down by steps of 0 to 1, 0 to 3 or
0 to 20 (`2000 random grids: 46445 negatives in all, checksum
907219988`). `count_negatives.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run` and `karac __mir-llvm-run`.

The Mend loop: the ★, cells and flat arms check clean. The search arm
was written with Rust's `let (mut lo, mut hi) = (0, bound);`; `karac
check` says that `mut` goes before the whole pattern (E0001), and `karac
fix` writes `let mut (lo, hi)`. The Rust solution takes one round of 5
fixes by `karac fix`'s count: `struct Solution;` to `struct Solution
{}`, `Vec<..>` to `Vec[..]`, and `|&x|` to `|x|`. Every arm matches on
the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every number of the grid tested, the order not used. 2000
sorted grids of 1 to 6 rows and columns in four kinds, 500 each: from a
top of -5 to 30 down by random steps of 0 to 1; of 0 to 3; of 0 to 20;
and from a top of -2 to 2 by steps of 0 to 1, with many zeros. Every
grid is drawn before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the grid transposed, still sorted: the same answer |
| P3 | the grid turned half a turn and every value negated, still sorted: its negatives are the old positives, so with the old negatives and the zeros, every cell once |
| P4 | every value one lower: the zeros join the negatives |
| P5 | a row of -100, the least value, put below: n more |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 grids: checksum 1690610,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run` and `karac __mir-llvm-run`. Python, bisecting each row read
backwards, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash, and no two
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a row's first negative not counted | P1 1213, P2 887, P3 1991, P4 237, P5 2000, P6 4852 |
| M2 | ★: the bottom row never walked | P1 1213, P2 887, P3 1991, P4 235, P5 1146, P6 4852 |
| M3 | search: the bound carried one place too far left | P1 1008, P2 1182, P3 1588, P4 307, P6 1008 |
| M4 | search: the first row skipped | P1 864, P2 910, P3 1759, P4 317, P6 864 |
| M5 | cells: -1 not counted | P1 578, P3 766, P4 628, P6 578 |
| M6 | cells: the diagonal skipped | P1 930, P3 1753, P4 261, P5 850, P6 930 |
| M7 | flat: only the first column counted | P1 1050, P2 910, P3 1665, P4 376, P5 1669, P6 1050 |
| M8 | flat: the first negative found not counted | P1 1213, P3 1991, P4 71, P5 787, P6 1213 |
| M9 | solution: zeros counted as negatives | P1 520, P3 520, P4 587, P6 520 |
| M10 | solution: the non-negatives counted | P1 1931, P3 520, P4 520, P5 2000, P6 1931 |

P1, P3, P4 and P6 kill all ten, P5 six and P2 five. Turning the grid
and negating it (P3) asks the arm for the positives as well as the
negatives, and lowering it (P4) asks it to find the zeros among the
negatives, so any edit that miscounts a negative, a zero or a positive
fails both. Transposing (P2) catches the edits that treat rows and
columns differently (M1, M2, M3, M4, M7); an edit on the values (M5, M8,
M9, M10) or on the diagonal (M6) is the same either way round. A row of
-100 below (P5) catches the edits whose error changes with the new row:
the walk's bottom row, a row's first negative or the first one found
(M1, M2, M8), a diagonal cell in it (M6), its first value alone (M7),
and the non-negatives counted instead (M10).

## Benchmarks

The bench builds 50 grids of 100 by 100, the constraints' largest, each
from a top of 60 down by random steps of 0 to 1, once; then makes
300,000 rounds, each moving one cell of one grid, both drawn from the
checksum so far, as far as the order allows, up to the smaller of the
cells above and to the left or down to the larger of the cells below and
to the right, so no answer carries over; counting that grid's negatives
with the ★ arm's staircase walk, and folding the count plus the round
into the checksum. Every implementation prints `300000 rounds over 50
grids of 100 by 100: checksum 91546475`.

BENCHTAB
