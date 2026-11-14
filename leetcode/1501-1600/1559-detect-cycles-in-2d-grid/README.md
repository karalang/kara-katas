# 1559. Detect Cycles in 2D Grid

Given a 2D array of characters `grid` of size `m x n`, find whether there
is a cycle of one value in `grid`. A cycle is a path of length 4 or more
that starts and ends at the same cell. From a cell you can move to one of
the cells next to it (up, down, left or right) if it has the same value
as the current cell. You cannot move back to the cell you visited in your
last move: the cycle `(1, 1) -> (1, 2) -> (1, 1)` is not valid.

```
grid = ["aaaa","abba","abba","aaaa"]   ->  true
grid = ["ccca","cdcc","ccec","fccc"]   ->  true
grid = ["abb","bzb","bba"]             ->  false
```

**Constraints:** `1 <= m, n <= 500`; `grid` holds lower-case English
letters only.

## Approaches

The cells of one letter and the pairs of them side by side make a graph,
and a walk that never steps straight back closes only in a graph with a
cycle. A grid has no triangles, so every cycle is 4 long or more and the
question is whether that graph is a forest.

| file | mechanism |
|---|---|
| `cycles.kara` ★ | a search on a stack (a list literal and `while let` on `pop`), each cell pushed with the cell it came from; a same-letter neighbour already seen that is not that cell closes a cycle. O(m n) |
| `cycles_union.kara` | union-find with path halving through a `mut ref Vec[i64]`: each cell joined to the same-letter cell on its right and below, and a pair already in one set closes a cycle. O(m n α) |
| `cycles_count.kara` | counting: a piece is a tree exactly when it has one edge fewer than cells, so each piece of one letter is flooded from a `VecDeque`, its cells and its neighbour pairs counted, and a piece with as many edges as cells has a cycle. O(m n) |
| `cycles_solution.kara` | LeetCode's Rust template (`contains_cycle(grid: Vec<Vec<char>>) -> bool`, a recursive search told the cell it came from, `usize::MAX` for none), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's three examples, then
`[aa, aa]`, `[a]`, `[ab, ba]`, a ring of `a` round a `b`, the same ring
broken at a corner, and one row of `a`; then the count of grids with a
cycle and a checksum for 3000 random grids of up to 6 by 6 over up to 3
letters, 300 of up to 60 by 60 and 30 of up to 200 by 200 over up to 26,
each grid over its own first few letters. `cycles.py` mirrors the ★ arm
and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: from every cell, the walks that never step straight back,
searched breadth first over (cell, cell before, steps up to 4), and a
walk back at its start after 4 steps or more is a cycle. It checks 3000
grids of 1 to 4 rows and 1 to 4 columns, each over its own first 1 to 3
letters, every random choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | a 2 by 2 block of one letter is a cycle, and a grid with no two neighbours alike has none |
| P3 | the grid transposed leaves the answer |
| P4 | the grid turned half way round leaves the answer |
| P5 | a row of `z` put under the grid leaves the answer, and two make a cycle when the grid is 2 or more wide |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 76251173, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the step straight back allowed | P1 1610, P5 510, P6 1610 |
| M2 | ★: a seen neighbour passed over | P1 880, P2 880, P5 2260, P6 880 |
| M3 | ★: never a step up | P1 27, P3 44, P4 49, P6 27 |
| M4 | union: only the neighbour on the right joined | P1 880, P2 880, P5 2260, P6 880 |
| M5 | union: nothing ever joined | P1 880, P2 880, P5 2260, P6 880 |
| M6 | union: `find` making a cell its own root | P1 2, P2 2, P3 2, P4 3, P6 2 |
| M7 | count: a cycle only at more edges than cells | P1 282, P2 282, P5 611, P6 282 |
| M8 | count: no edge counted | P1 880, P2 880, P5 2260, P6 880 |
| M9 | template: a neighbour in the parent's row or column taken as the parent | P1 673, P3 36, P4 39, P5 431, P6 673 |
| M10 | template: a search started from every cell, visited or not | P1 1610, P5 510, P6 1610 |

## Benchmarks

The bench builds 20 grids of 500 by 500 once: row 0 and every even
column `a`, a comb with no cycle, and the odd columns below random
letters from `b`, cut into straight runs by the comb's teeth. In half of
them two cells of an odd column are made `a`, joining two teeth into a
cycle at a random place. Each grid is asked 5 times by the ★ arm, in all
five languages. Kāra, Rust and Go keep the grid as rows of 32-bit
characters; C keeps it as one block of `uint32_t`. Every call allocates
its marks and its stack. Every implementation prints `5 passes over 20
grids of 500 by 500: 50 with a cycle, checksum 537832454`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5a1b79539` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.179 s |
| Kāra (`karac build`) | 0.268 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.273 s |
| Rust (`rustc -O`) | 0.286 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.332 s |
| Go | 0.346 s |
| Python | 11.8 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.30 s and 0.31 s on one run).

Kāra is 0.82x Rust under overflow checks by median. Not traced. The
search is a load of two rows per neighbour, a scattered mark and a push,
and C's single block saves the row lookup the others make; overflow
checks cost Rust 16% here, on the index arithmetic.

## Verification

All four arms print the same output as `cycles.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change. Checked at kara `5a1b79539`.

## Writing it

The union and count arms were written in Kāra and checked as written.
The ★ arm started its stack as `vec![(start, -1)]`, which checks with a
`deprecated vec![..]` warning, and one round of `karac fix` turned it
into the list literal.

The Rust template took four rounds of `karac fix`, 8 changed lines, then
1 added, then 5 and 2 changed:

1. the `Vec<..>` types to `Vec[..]`, `&Vec<..>` and `&mut Vec<..>`
   parameters to `ref` and `mut ref`, `&grid` and `&mut visited` at the
   call to `grid` and `mut visited`, `for &(di, dj)` to `for (di, dj)`,
   `!` to `not`, `&&` and `||` to `and` and `or`, `usize::MAX` to
   `usize.MAX`, and `Self::dfs` and `Solution::` to `Solution.`;
2. `struct Solution {}` added;
3. the inner `vec![false; n]` to `Vec.filled(n, false)`, the `usize`
   parameters to `i64` and `usize.MAX` with them to `i64.MAX`, the
   `as usize` casts to `as i64`, and `mut` added to the recursive call's
   `visited`;
4. the outer `vec![..; m]` to `Vec.filled(m, ..)`, and `ref` dropped from
   the `grid` parameter (a bare parameter already borrows).

The `usize::MAX` sentinel for no parent survives as `i64.MAX`, which no
cell index reaches, and the template's `i as i32 + di` arithmetic stays
as written. It checks and agrees with no hand edit.
