# 1591. Strange Printer II

There is a strange printer with the following two special requirements:

- On each turn, the printer will print a solid rectangular pattern of a
  single color on the grid. This will cover up the existing colors in
  the rectangle.
- Once the printer has used a color for the above operation, the same
  color cannot be used again.

You are given an `m x n` matrix `targetGrid`, where `targetGrid[row][col]`
is the color in the position `(row, col)` of the grid.

Return `true` if it is possible to print the matrix `targetGrid`,
otherwise, return `false`.

```
targetGrid = [[1,1,1,1],[1,2,2,1],[1,2,2,1],[1,1,1,1]]  ->  true
targetGrid = [[1,1,1,1],[1,1,3,3],[1,1,3,4],[5,5,1,4]]  ->  true
targetGrid = [[1,2,1],[2,1,2],[1,2,1]]                  ->  false
```

**Constraints:** `m == targetGrid.length`; `n == targetGrid[i].length`;
`1 <= m, n <= 60`; `1 <= targetGrid[row][col] <= 60`.

## Approaches

A colour printed once covers its whole bounding rectangle, so any other
colour seen inside that rectangle was printed after it. The grid can be
printed exactly when those orders have no cycle.

| file | mechanism |
|---|---|
| `printer.kara` ★ | each colour's bounding rectangle in four `Vec.filled(61, ..)`, the orders as a 61 by 61 matrix of `bool`, and Kahn's algorithm: colours with nothing left before them taken one at a time from a `Vec`. O(C (mn + C)) |
| `printer_dfs.kara` | the rectangles as a `Box` struct in a `Map[i32, Box]` (updated through `get_mut`), each colour's later colours as a list deduplicated by a `Set`, searched depth first by recursion with three states. O(C mn) |
| `printer_peel.kara` | printing backwards: the colours left in a `SortedSet`, and the first whose rectangle holds only itself and freed cells taken off by freeing its cells, until none is left or none can come off. O(C^2 mn) |
| `printer_solution.kara` | LeetCode's Rust template (`[usize; 4]` bounds per colour with `usize::MAX`, a `Vec<HashSet<usize>>` graph, Kahn's algorithm over a `VecDeque`), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and three
more (one cell, a two by two checkerboard, and three nested prints),
then the count printable and a checksum for 3000 random grids of up to 4
by 4 in 4 colours, 300 of up to 20 by 20 in 20 colours, and 30 of up to
60 by 60 in 60 colours. Each grid is printed by random rectangles of
random colours (a colour may come twice), the first covering the whole
grid, and a third of the time one cell is then redrawn. `printer.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every order of the colours present, each printed as the
rectangle that just covers its cells, and the result compared with the
grid. A larger rectangle never helps: its extra cells hold other colours
in the grid, so a later print covers them again. It checks 3000 grids of
1 to 3 by 1 to 4 cells in colours 1 to 4, each printed by 1 to 4 random
rectangles and a third of the time one cell redrawn, every random choice
drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the grid turned upside down leaves the answer |
| P3 | the grid transposed leaves the answer |
| P4 | the colours renamed (`k` made `61 - k`) leave the answer |
| P5 | a row repeated next to itself leaves the answer |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 901713060, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

Five first choices were replaced. Four were equivalent: a cycle needs
two colours, so `taken >= 59` in the ★ arm and `seen + 1 >= total` in
the template are right exactly when `==` is; and a DFS colour reset to
unseen after it finishes, or recursed into only once finished, is still
met again from the outer loop. Mixing up `i` and `j` in the template's
bounds was killed only by an index panic.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the rectangle's last row left out | P1 53, P2 38, P3 42, P5 26, P6 53 |
| M2 | ★: only colours above `k` taken as printed after it | P1 103, P6 103 |
| M3 | ★: each order lowers the count twice | P1 719, P6 719 |
| M4 | dfs: a colour met on the path not taken as a cycle | P1 103, P6 103 |
| M5 | dfs: a cycle found at a finished colour, not one on the path | P1 483, P4 687, P6 483 |
| M6 | peel: a freed cell counted as in the way | P1 721, P6 721 |
| M7 | peel: a rectangle taken off stops after its first row | P1 211, P3 216, P6 211 |
| M8 | template: each order raises the earlier colour's count | P1 721, P6 721 |
| M9 | template: absent colours start the queue | P1 2897, P6 2897 |
| M10 | dfs: a colour taken as printed after itself | P1 2897, P6 2897 |

## Benchmarks

The bench runs the ★ arm on 4000 grids of 60 by 60, each printed by the
60 colours in a random order as random rectangles, every other one then
given one cell redrawn, all drawn first, in all five languages. Every
implementation prints `4000 grids of 60 by 60: 3102 printable, checksum
890086898`. In the C mirror each grid row is its own malloc, as each
Kāra row is a `Vec`; the 61 by 61 order matrix and the counts are
allocated per call.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5dc4418bbd` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.167 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.233 s |
| Kāra (`karac build`) | 0.234 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.254 s |
| Rust (`rustc -O`) | 0.268 s |
| Go | 0.335 s |
| Python | 7.6 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is below its real time (0.219 s and 0.256 s on one run).

## Verification

All four arms print the same output as `printer.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`5dc4418bbd`.

## Writing it

The peel arm was written in Kāra and checked as written. The ★ arm wrote
`(1..61).filter(|k| before[*k] == 0)`, and `karac fix` dropped the `*`,
as a range hands the closure each number by value. The DFS arm wrote
`other as i64`, and `karac fix` dropped the cast.

The Rust template took four rounds of `karac fix`:

1. `use std::collections::{HashSet, VecDeque}` dropped,
   `struct Solution;` to `struct Solution {}`, the `<..>` types to
   `[..]`, `usize::MAX` to `usize.MAX`, `::new()` to `.new()`, `!` to
   `not`, `&&` to `and`, the `|&&p|` and `&d` patterns to plain names,
   and `Solution::` to `Solution.`;
2. `HashSet[usize]` to `Set[usize]`;
3. the `usize` types, casts and `usize.MAX` to `i64`, and the
   `vec![false; 61]`, `vec![Set.new(); 61]` and `vec![0; 61]` to
   `Vec.filled(..)`;
4. the last `vec![[i64.MAX, 0, i64.MAX, 0]; 61]` to `Vec.filled(..)`.

It then checks and agrees with no hand edit.
